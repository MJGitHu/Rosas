import hashlib
import hmac
import json
import logging
import re
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

import oracledb
from flask import Blueprint, current_app, jsonify, request

from app.db import get_db_connection
from app.routes.reservas import FORMATOS, _find_schedule_conflict, _parse_schedule

pagos_bp = Blueprint("pagos", __name__)
logger = logging.getLogger(__name__)

PEN = Decimal("0.01")
HOLD_MINUTES = 30


class MercadoPagoAPIError(Exception):
    pass


def _mercado_pago_request(method, path, payload=None, idempotency_key=None):
    access_token = current_app.config["MERCADOPAGO_ACCESS_TOKEN"]
    if not access_token:
        raise MercadoPagoAPIError("Mercado Pago no está configurado en el servidor.")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    if idempotency_key:
        headers["X-Idempotency-Key"] = idempotency_key
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    api_request = Request(
        f"https://api.mercadopago.com{path}",
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urlopen(api_request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            if not isinstance(result, dict):
                raise MercadoPagoAPIError("Mercado Pago devolvió una respuesta no válida.")
            return result
    except HTTPError as error:
        raise MercadoPagoAPIError(
            f"Mercado Pago respondió con HTTP {error.code}."
        ) from None
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise MercadoPagoAPIError(
            "No se pudo completar la solicitud a Mercado Pago."
        ) from error


def _validate_contract(data):
    if not isinstance(data, dict):
        raise ValueError("El cuerpo de la solicitud debe ser JSON.")

    cliente = data.get("cliente")
    if not isinstance(cliente, dict):
        raise ValueError("Faltan los datos del cliente.")
    for field, max_length in {
        "nombre": 100,
        "apellido": 100,
        "telefono": 20,
        "email": 120,
    }.items():
        value = cliente.get(field)
        if not isinstance(value, str) or not value.strip() or len(value.strip()) > max_length:
            raise ValueError(
                f"El campo {field} es obligatorio y no puede exceder {max_length} caracteres."
            )

    email = cliente["email"].strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("Ingresa un correo electrónico válido.")

    service_key = data.get("servicio")
    service = FORMATOS.get(service_key) if isinstance(service_key, str) else None
    if service is None:
        raise ValueError("Selecciona un formato y duración válidos.")

    event_start, duration_minutes = _parse_schedule(
        data.get("fecha_evento"),
        data.get("hora_evento"),
        data.get("duracion_minutos"),
    )
    address = data.get("direccion_evento")
    details = data.get("detalles", "")
    payment_method = data.get("metodo_pago")
    if not isinstance(address, str) or not address.strip() or len(address.strip()) > 250:
        raise ValueError("La dirección es obligatoria y no puede exceder 250 caracteres.")
    if not isinstance(details, str) or len(details.strip()) > 500:
        raise ValueError("Los detalles no pueden exceder 500 caracteres.")
    if not isinstance(payment_method, str) or payment_method not in {"MERCADOPAGO", "PRUEBA"}:
        raise ValueError("Selecciona un método de pago válido.")

    base_price = Decimal(str(service["precios"][duration_minutes])).quantize(PEN)
    if payment_method == "PRUEBA":
        total = Decimal("1.00")
        amount_to_pay = Decimal("1.00")
        balance = Decimal("0.00")
    else:
        total = base_price
        amount_to_pay = (total * Decimal("0.50")).quantize(PEN)
        balance = total - amount_to_pay

    contract = {
        "cliente": {
            "nombre": cliente["nombre"].strip(),
            "apellido": cliente["apellido"].strip(),
            "telefono": cliente["telefono"].strip(),
            "email": email,
        },
        "servicio": service_key,
        "duracion_minutos": duration_minutes,
        "direccion_evento": address.strip(),
        "fecha_evento": event_start.date().isoformat(),
        "hora_evento": event_start.strftime("%H:%M"),
        "detalles": details.strip(),
        "metodo_pago": payment_method,
    }
    return contract, service, event_start, duration_minutes, total, amount_to_pay, balance


def _database_connection():
    try:
        connection = get_db_connection()
    except oracledb.Error:
        logger.exception("No se pudo conectar a Oracle para procesar un pago.")
        return None
    return connection


def _set_intent_status(external_reference, status, preference_id=None, init_point=None):
    connection = _database_connection()
    if connection is None:
        raise RuntimeError("No se pudo actualizar el estado del pago en Oracle.")
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE mercadopago_intents
                SET estado = :estado,
                    id_preferencia = COALESCE(:id_preferencia, id_preferencia),
                    init_point = COALESCE(:init_point, init_point)
                WHERE referencia_externa = :referencia_externa
                  AND estado = 'CREANDO'
                """,
                estado=status,
                id_preferencia=preference_id,
                init_point=init_point,
                referencia_externa=external_reference,
            )
        connection.commit()
    except oracledb.Error:
        connection.rollback()
        logger.exception("No se pudo actualizar el intento de pago en Oracle.")
        raise
    finally:
        connection.close()


@pagos_bp.route("/preferencias", methods=["POST"])
def crear_preferencia():
    try:
        validated = _validate_contract(request.get_json(silent=True))
    except ValueError as error:
        return jsonify({"status": "error", "message": str(error)}), 400

    contract, service, event_start, duration_minutes, total, amount_to_pay = validated[:6]
    if not current_app.config["MERCADOPAGO_ACCESS_TOKEN"]:
        return jsonify({
            "status": "error",
            "message": "Mercado Pago no está configurado en el servidor.",
        }), 503
    if not current_app.config["MERCADOPAGO_WEBHOOK_SECRET"]:
        return jsonify({
            "status": "error",
            "message": "Falta configurar la clave secreta del webhook de Mercado Pago.",
        }), 503
    webhook_url = current_app.config["MERCADOPAGO_WEBHOOK_URL"]
    parsed_webhook_url = urlsplit(webhook_url)
    if parsed_webhook_url.scheme != "https" or not parsed_webhook_url.netloc:
        return jsonify({
            "status": "error",
            "message": "La URL HTTPS del webhook de Mercado Pago no está configurada.",
        }), 503

    external_reference = str(uuid.uuid4())
    lima_timezone = timezone(timedelta(hours=-5))
    expires_from = datetime.now(lima_timezone)
    expires_to = expires_from + timedelta(minutes=HOLD_MINUTES)
    return_url = (
        f"{parsed_webhook_url.scheme}://{parsed_webhook_url.netloc}/"
        f"?payment_return=1&external_reference={external_reference}"
    )
    preference = {
        "items": [{
            "id": contract["servicio"],
            "title": f"{service['nombre']} - {duration_minutes} minutos",
            "quantity": 1,
            "currency_id": "PEN",
            "unit_price": float(amount_to_pay),
        }],
        "payer": {"email": contract["cliente"]["email"]},
        "external_reference": external_reference,
        "notification_url": webhook_url,
        "back_urls": {
            "success": return_url,
            "failure": return_url,
            "pending": return_url,
        },
        "auto_return": "approved",
        "expires": True,
        "expiration_date_from": expires_from.isoformat(timespec="seconds"),
        "expiration_date_to": expires_to.isoformat(timespec="seconds"),
        "statement_descriptor": "ROSASDEGUADALUPE",
    }

    connection = _database_connection()
    if connection is None:
        return jsonify({
            "status": "error",
            "message": "No se pudo conectar a la base de datos para reservar temporalmente el horario.",
        }), 503
    try:
        with connection.cursor() as cursor:
            cursor.execute("LOCK TABLE eventos_reservas IN EXCLUSIVE MODE")
            cursor.execute("LOCK TABLE mercadopago_intents IN EXCLUSIVE MODE")
            if _find_schedule_conflict(cursor, event_start, duration_minutes):
                connection.rollback()
                return jsonify({
                    "status": "error",
                    "message": "Ese horario ya no está disponible.",
                }), 409
            cursor.execute(
                """
                INSERT INTO mercadopago_intents (
                    referencia_externa, fecha_evento, hora_inicio, duracion_minutos,
                    contrato_json, monto_total, monto_pago, estado, expira_en
                ) VALUES (
                    :referencia_externa, :fecha_evento, :hora_inicio, :duracion_minutos,
                    :contrato_json, :monto_total, :monto_pago, 'CREANDO',
                    SYSTIMESTAMP + NUMTODSINTERVAL(:hold_minutes, 'MINUTE')
                )
                """,
                referencia_externa=external_reference,
                fecha_evento=datetime.combine(event_start.date(), datetime.min.time()),
                hora_inicio=event_start.strftime("%H:%M"),
                duracion_minutos=duration_minutes,
                contrato_json=json.dumps(contract, ensure_ascii=False),
                monto_total=total,
                monto_pago=amount_to_pay,
                hold_minutes=HOLD_MINUTES,
            )
        connection.commit()
    except oracledb.Error:
        connection.rollback()
        logger.exception("No se pudo retener el horario para crear un pago.")
        return jsonify({
            "status": "error",
            "message": "No se pudo reservar temporalmente el horario.",
        }), 500
    finally:
        connection.close()

    try:
        result = _mercado_pago_request(
            "POST",
            "/checkout/preferences",
            preference,
            idempotency_key=external_reference,
        )
        init_point = result.get("init_point")
        preference_id = result.get("id")
        parsed_init_point = urlsplit(init_point or "")
        if (
            not preference_id
            or parsed_init_point.scheme != "https"
            or not (
                (parsed_init_point.hostname or "").endswith(".mercadopago.com")
                or (parsed_init_point.hostname or "").endswith(".mercadopago.com.pe")
            )
        ):
            raise MercadoPagoAPIError("Mercado Pago devolvió una URL de pago no válida.")
        _set_intent_status(
            external_reference,
            "PENDIENTE",
            str(preference_id),
            init_point,
        )
    except (MercadoPagoAPIError, RuntimeError, oracledb.Error):
        try:
            _set_intent_status(external_reference, "ERROR")
        except (RuntimeError, oracledb.Error):
            logger.exception("No se pudo liberar un intento de pago fallido.")
        logger.exception("No se pudo crear la preferencia de Mercado Pago.")
        return jsonify({
            "status": "error",
            "message": "No se pudo iniciar el pago. Inténtalo nuevamente.",
        }), 502

    return jsonify({
        "status": "success",
        "data": {
            "referencia_externa": external_reference,
            "init_point": init_point,
            "monto_a_pagar": float(amount_to_pay),
            "moneda": "PEN",
        },
    }), 201


def _valid_webhook_signature(payment_id):
    signature = request.headers.get("x-signature", "")
    request_id = request.headers.get("x-request-id", "")
    secret = current_app.config["MERCADOPAGO_WEBHOOK_SECRET"]
    if not signature or not request_id or not secret:
        return False

    signature_parts = {}
    for part in signature.split(","):
        key, separator, value = part.strip().partition("=")
        if separator:
            signature_parts[key] = value
    timestamp = signature_parts.get("ts")
    received_signature = signature_parts.get("v1")
    if not timestamp or not received_signature:
        return False

    manifest = (
        f"id:{str(payment_id).lower()};request-id:{request_id};ts:{timestamp};"
    )
    expected_signature = hmac.new(
        secret.encode("utf-8"),
        manifest.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected_signature, received_signature)


def _persist_approved_payment(payment, payment_id):
    reference = payment.get("external_reference")
    if not isinstance(reference, str) or not reference:
        logger.warning("Pago aprobado sin referencia externa; no se creó una reserva.")
        return

    try:
        paid_amount = Decimal(str(payment.get("transaction_amount"))).quantize(PEN)
    except (InvalidOperation, TypeError):
        logger.warning("Pago con importe inválido; no se creó una reserva.")
        return

    connection = _database_connection()
    if connection is None:
        raise RuntimeError("No se pudo conectar a Oracle para confirmar el contrato.")
    try:
        with connection.cursor() as cursor:
            cursor.execute("LOCK TABLE eventos_reservas IN EXCLUSIVE MODE")
            cursor.execute("LOCK TABLE mercadopago_intents IN EXCLUSIVE MODE")
            cursor.execute(
                """
                SELECT contrato_json, monto_total, monto_pago, estado
                FROM mercadopago_intents
                WHERE referencia_externa = :referencia_externa
                FOR UPDATE
                """,
                referencia_externa=reference,
            )
            intent = cursor.fetchone()
            if intent is None:
                connection.rollback()
                logger.warning("Pago aprobado para una referencia externa desconocida.")
                return
            contract_json, total, expected_amount, state = intent
            if state == "APROBADO":
                connection.commit()
                return
            if state not in {"CREANDO", "PENDIENTE"}:
                connection.commit()
                logger.warning("Pago aprobado para un intento en estado %s.", state)
                return

            try:
                expected_amount = Decimal(str(expected_amount)).quantize(PEN)
            except (InvalidOperation, TypeError):
                raise RuntimeError("El importe esperado del intento de pago es inválido.")

            if (
                payment.get("status") != "approved"
                or payment.get("currency_id") != "PEN"
                or paid_amount != expected_amount
            ):
                cursor.execute(
                    """
                    UPDATE mercadopago_intents
                    SET estado = 'REQUIERE_REVISION', id_pago_mp = :id_pago_mp
                    WHERE referencia_externa = :referencia_externa
                    """,
                    id_pago_mp=str(payment_id),
                    referencia_externa=reference,
                )
                connection.commit()
                logger.error("Pago aprobado con moneda o importe distinto al esperado.")
                return

            try:
                if hasattr(contract_json, "read"):
                    contract_json = contract_json.read()
                contract = json.loads(contract_json)
                event_start, duration_minutes = _parse_schedule(
                    contract["fecha_evento"],
                    contract["hora_evento"],
                    contract["duracion_minutos"],
                )
            except (TypeError, ValueError, KeyError, json.JSONDecodeError) as error:
                raise RuntimeError("Los datos del contrato guardados en el intento son inválidos.") from error

            if _find_schedule_conflict(
                cursor,
                event_start,
                duration_minutes,
                exclude_reference=reference,
            ):
                cursor.execute(
                    """
                    UPDATE mercadopago_intents
                    SET estado = 'REQUIERE_REVISION', id_pago_mp = :id_pago_mp
                    WHERE referencia_externa = :referencia_externa
                    """,
                    id_pago_mp=str(payment_id),
                    referencia_externa=reference,
                )
                connection.commit()
                logger.error("Pago aprobado pero el horario ya no está disponible.")
                return

            service = FORMATOS[contract["servicio"]]
            cursor.execute(
                """
                SELECT id_formato FROM formatos_mariachi
                WHERE nombre_formato = :nombre_formato AND activo = 'S'
                """,
                nombre_formato=service["nombre"],
            )
            format_row = cursor.fetchone()
            cursor.execute(
                """
                SELECT id_zona FROM zonas_cobertura
                WHERE nombre_zona = 'Sin recargo por distancia' AND activo = 'S'
                """
            )
            zone_row = cursor.fetchone()
            if format_row is None or zone_row is None:
                raise RuntimeError("Los catálogos necesarios para crear la reserva no están disponibles.")

            cliente = contract["cliente"]
            cursor.execute(
                """
                MERGE INTO clientes c
                USING (SELECT :email email FROM dual) incoming
                   ON (c.email = incoming.email)
                WHEN MATCHED THEN UPDATE SET
                    nombre = :nombre, apellido = :apellido, telefono = :telefono
                WHEN NOT MATCHED THEN INSERT (nombre, apellido, telefono, email)
                VALUES (:nombre, :apellido, :telefono, :email)
                """,
                email=cliente["email"],
                nombre=cliente["nombre"],
                apellido=cliente["apellido"],
                telefono=cliente["telefono"],
            )
            cursor.execute(
                "SELECT id_cliente FROM clientes WHERE email = :email",
                email=cliente["email"],
            )
            client_row = cursor.fetchone()
            if client_row is None:
                raise RuntimeError("No se pudo asociar el cliente con el contrato.")

            total = Decimal(str(total)).quantize(PEN)
            amount_due = Decimal(str(expected_amount)).quantize(PEN)
            balance = total - amount_due
            code = f"RS-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}"
            cursor.execute(
                """
                INSERT INTO eventos_reservas (
                    codigo_reserva, id_cliente, id_formato, id_zona,
                    fecha_evento, hora_inicio, duracion_horas, direccion_evento,
                    tipo_evento, estado_reserva, monto_subtotal, recargo_zona,
                    monto_total, anticipo_requerido, saldo_pendiente,
                    notas_logistica, metodo_pago_preferido
                ) VALUES (
                    :codigo_reserva, :id_cliente, :id_formato, :id_zona,
                    :fecha_evento, :hora_inicio, :duracion_horas, :direccion_evento,
                    'Contratación web', 'ANTICIPO_PAGADO', :monto_subtotal, 0,
                    :monto_total, :anticipo_requerido, :saldo_pendiente,
                    :notas_logistica, :metodo_pago_preferido
                )
                """,
                codigo_reserva=code,
                id_cliente=client_row[0],
                id_formato=format_row[0],
                id_zona=zone_row[0],
                fecha_evento=datetime.combine(event_start.date(), datetime.min.time()),
                hora_inicio=event_start.strftime("%H:%M"),
                duracion_horas=duration_minutes / 60,
                direccion_evento=contract["direccion_evento"],
                monto_subtotal=total,
                monto_total=total,
                anticipo_requerido=amount_due,
                saldo_pendiente=balance,
                notas_logistica=contract["detalles"] or None,
                metodo_pago_preferido=contract["metodo_pago"],
            )
            cursor.execute(
                "SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = :codigo",
                codigo=code,
            )
            reservation_row = cursor.fetchone()
            if reservation_row is None:
                raise RuntimeError("No se pudo recuperar la reserva recién creada.")
            reservation_id = reservation_row[0]

            payment_type = "TOTAL_100" if contract["metodo_pago"] == "PRUEBA" else "ANTICIPO_50"
            cursor.execute(
                """
                INSERT INTO pagos (
                    id_reserva, tipo_pago, metodo_pago, monto_base,
                    comision_pasarela, monto_cobrado, referencia_transaccion,
                    estado_pago, fecha_pago
                ) VALUES (
                    :id_reserva, :tipo_pago, 'MERCADOPAGO', :monto_base,
                    0, :monto_cobrado, :referencia_transaccion,
                    'COMPLETADO', SYSTIMESTAMP
                )
                """,
                id_reserva=reservation_id,
                tipo_pago=payment_type,
                monto_base=amount_due,
                monto_cobrado=paid_amount,
                referencia_transaccion=str(payment_id),
            )
            cursor.execute(
                """
                UPDATE mercadopago_intents
                SET estado = 'APROBADO', id_pago_mp = :id_pago_mp,
                    id_reserva = :id_reserva
                WHERE referencia_externa = :referencia_externa
                """,
                id_pago_mp=str(payment_id),
                id_reserva=reservation_id,
                referencia_externa=reference,
            )
        connection.commit()
    except (oracledb.Error, RuntimeError):
        connection.rollback()
        logger.exception("No se pudo completar el contrato tras un pago aprobado.")
        raise
    finally:
        connection.close()


@pagos_bp.route("/webhook", methods=["POST"])
def recibir_webhook():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        body = {}
    notification_type = (
        request.args.get("topic")
        or request.args.get("type")
        or body.get("type")
    )
    if notification_type != "payment":
        return jsonify({"status": "ignored"}), 200
    notification_data = body.get("data")
    if not isinstance(notification_data, dict):
        notification_data = {}
    payment_id = (
        request.args.get("data.id")
        or request.args.get("id")
        or notification_data.get("id")
    )
    if not payment_id or not _valid_webhook_signature(payment_id):
        return jsonify({"status": "error", "message": "Notificación no válida."}), 401

    try:
        payment = _mercado_pago_request("GET", f"/v1/payments/{payment_id}")
        if payment.get("status") == "approved":
            _persist_approved_payment(payment, payment_id)
    except (MercadoPagoAPIError, RuntimeError, oracledb.Error):
        logger.exception("No se pudo procesar una notificación de pago de Mercado Pago.")
        return jsonify({"status": "error", "message": "No se pudo procesar el pago."}), 503
    return jsonify({"status": "ok"}), 200


@pagos_bp.route("/estado", methods=["GET"])
def consultar_estado():
    reference = request.args.get("referencia_externa", "")
    if not re.fullmatch(r"[0-9a-fA-F-]{36}", reference):
        return jsonify({"status": "error", "message": "Referencia de pago no válida."}), 400

    connection = _database_connection()
    if connection is None:
        return jsonify({"status": "error", "message": "No se pudo consultar el estado del pago."}), 503
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    CASE
                        WHEN i.estado IN ('CREANDO', 'PENDIENTE')
                         AND i.expira_en <= SYSTIMESTAMP THEN 'EXPIRADO'
                        ELSE i.estado
                    END,
                    r.codigo_reserva,
                    CASE
                        WHEN i.estado = 'PENDIENTE'
                         AND i.expira_en > SYSTIMESTAMP THEN i.init_point
                        ELSE NULL
                    END
                FROM mercadopago_intents i
                LEFT JOIN eventos_reservas r ON r.id_reserva = i.id_reserva
                WHERE i.referencia_externa = :referencia_externa
                """,
                referencia_externa=reference,
            )
            result = cursor.fetchone()
        if result is None:
            return jsonify({"status": "error", "message": "No se encontró el pago."}), 404
        return jsonify({
            "status": "success",
            "data": {
                "estado": result[0],
                "codigo_reserva": result[1],
                "init_point": result[2] if result[0] == "PENDIENTE" else None,
            },
        }), 200
    except oracledb.Error:
        logger.exception("No se pudo consultar el estado de un pago.")
        return jsonify({"status": "error", "message": "No se pudo consultar el estado del pago."}), 500
    finally:
        connection.close()
