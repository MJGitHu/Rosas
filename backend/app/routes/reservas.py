from datetime import date, datetime, time, timedelta
import logging
import re
import uuid

import oracledb
from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from app.routes.admin import admin_required

reservas_bp = Blueprint("reservas", __name__)
logger = logging.getLogger(__name__)

FORMATOS = {
    "mariachi": {
        "nombre": "Mariachi completo",
        "precios": {30: 380, 40: 480, 60: 680},
    },
    "express-1": {
        "nombre": "Express 1",
        "precios": {30: 340, 40: 420, 60: 600},
    },
    "express-2": {
        "nombre": "Express 2",
        "precios": {30: 300, 40: 360, 60: 500},
    },
    "express-duo": {
        "nombre": "Express dúo",
        "precios": {30: 250, 40: 280, 60: 420},
    },
    "solista": {
        "nombre": "Solista",
        "precios": {30: 180, 40: 220, 60: 320},
    },
}
METODOS_PAGO = {"MERCADOPAGO", "PRUEBA"}
HORARIO_INICIO = time(11, 0)
HORARIO_FIN = time(1, 0)
TIEMPO_ENTRE_EVENTOS = timedelta(minutes=45)


def _parse_schedule(event_date_value, event_time_value, duration_value):
    if not isinstance(event_date_value, str) or not isinstance(event_time_value, str):
        raise ValueError("La fecha u hora del evento no son válidas.")
    if isinstance(duration_value, bool) or (
        isinstance(duration_value, float) and not duration_value.is_integer()
    ):
        raise ValueError("La duración seleccionada no es válida.")
    try:
        event_date = date.fromisoformat(event_date_value)
        event_time = datetime.strptime(event_time_value, "%H:%M").time()
        duration_minutes = int(duration_value)
    except (TypeError, ValueError):
        raise ValueError("La duración, fecha u hora del evento no son válidas.") from None

    if duration_minutes not in {30, 40, 60}:
        raise ValueError("Selecciona una duración válida.")
    if not (event_time >= HORARIO_INICIO or event_time <= HORARIO_FIN):
        raise ValueError("Los contratos solo pueden agendarse entre las 11:00 y la 01:00.")

    event_start = datetime.combine(event_date, event_time)
    if event_start < datetime.now():
        raise ValueError("La fecha y hora del evento no pueden estar en el pasado.")
    return event_start, duration_minutes


def _find_schedule_conflict(cursor, event_start, duration_minutes, exclude_reference=None):
    cursor.execute(
        """
        SELECT fecha_evento, hora_inicio, duracion_horas
        FROM eventos_reservas
        WHERE estado_reserva <> 'CANCELADA'
          AND fecha_evento >= :start_date
          AND fecha_evento < :end_date
        UNION ALL
        SELECT fecha_evento, hora_inicio, duracion_minutos / 60
        FROM mercadopago_intents
        WHERE estado IN ('CREANDO', 'PENDIENTE')
          AND expira_en > SYSTIMESTAMP
          AND fecha_evento >= :start_date
          AND fecha_evento < :end_date
          AND (:exclude_reference IS NULL OR referencia_externa <> :exclude_reference)
        """,
        start_date=datetime.combine(event_start.date() - timedelta(days=1), time.min),
        end_date=datetime.combine(event_start.date() + timedelta(days=2), time.min),
        exclude_reference=exclude_reference,
    )
    requested_end = event_start + timedelta(minutes=duration_minutes)
    for existing_date, existing_time, existing_duration in cursor.fetchall():
        if isinstance(existing_date, datetime):
            existing_date = existing_date.date()
        try:
            existing_start = datetime.combine(
                existing_date,
                datetime.strptime(existing_time, "%H:%M").time(),
            )
            existing_duration_minutes = round(float(existing_duration) * 60)
            existing_end = existing_start + timedelta(minutes=existing_duration_minutes)
        except (TypeError, ValueError) as error:
            raise RuntimeError("Una reserva existente tiene fecha, hora o duración inválida.") from error

        if (
            event_start < existing_end + TIEMPO_ENTRE_EVENTOS
            and requested_end + TIEMPO_ENTRE_EVENTOS > existing_start
        ):
            return True
    return False


@reservas_bp.route("/", methods=["POST"])
def crear_reserva():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "El cuerpo de la solicitud debe ser JSON."}), 400

    cliente = data.get("cliente")
    if not isinstance(cliente, dict):
        return jsonify({"status": "error", "message": "Faltan los datos del cliente."}), 400

    for field, max_length in {
        "nombre": 100,
        "apellido": 100,
        "telefono": 20,
        "email": 120,
    }.items():
        value = cliente.get(field)
        if not isinstance(value, str) or not value.strip() or len(value.strip()) > max_length:
            return jsonify({
                "status": "error",
                "message": f"El campo {field} es obligatorio y no puede exceder {max_length} caracteres.",
            }), 400

    email = cliente["email"].strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify({"status": "error", "message": "Ingresa un correo electrónico válido."}), 400

    service_key = data.get("servicio")
    service = FORMATOS.get(service_key) if isinstance(service_key, str) else None
    if service is None:
        return jsonify({"status": "error", "message": "Selecciona un formato válido."}), 400

    try:
        event_start, duration_minutes = _parse_schedule(
            data.get("fecha_evento"),
            data.get("hora_evento"),
            data.get("duracion_minutos"),
        )
    except ValueError as error:
        return jsonify({"status": "error", "message": str(error)}), 400

    address = data.get("direccion_evento")
    details = data.get("detalles", "")
    if not isinstance(address, str) or not address.strip() or len(address.strip()) > 250:
        return jsonify({
            "status": "error",
            "message": "La dirección es obligatoria y no puede exceder 250 caracteres.",
        }), 400
    if not isinstance(details, str) or len(details.strip()) > 500:
        return jsonify({
            "status": "error",
            "message": "Los detalles no pueden exceder 500 caracteres.",
        }), 400

    subtotal = round(service["precios"][duration_minutes], 2)
    advance = round(subtotal * 0.5, 2)
    balance = round(subtotal - advance, 2)
    code = f"RS-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}"

    try:
        conn = get_db_connection()
    except oracledb.Error:
        logger.exception("No se pudo conectar a Oracle para guardar una reserva pendiente.")
        return jsonify({
            "status": "error",
            "message": "No se pudo conectar a la base de datos. La reserva no se guardó.",
        }), 503
    if conn is None:
        return jsonify({
            "status": "error",
            "message": "La base de datos no está disponible. La reserva no se guardó.",
        }), 503

    try:
        with conn.cursor() as cursor:
            cursor.execute("LOCK TABLE eventos_reservas IN EXCLUSIVE MODE")
            cursor.execute("LOCK TABLE mercadopago_intents IN EXCLUSIVE MODE")
            if _find_schedule_conflict(cursor, event_start, duration_minutes):
                conn.rollback()
                return _busy_schedule_response(), 409

            cursor.execute(
                """
                SELECT id_formato
                FROM formatos_mariachi
                WHERE nombre_formato = :nombre_formato AND activo = 'S'
                """,
                nombre_formato=service["nombre"],
            )
            format_row = cursor.fetchone()
            if format_row is None:
                conn.rollback()
                return jsonify({
                    "status": "error",
                    "message": "El catálogo de formatos no está actualizado.",
                }), 409

            cursor.execute(
                """
                SELECT id_zona
                FROM zonas_cobertura
                WHERE nombre_zona = 'Sin recargo por distancia' AND activo = 'S'
                """
            )
            zone_row = cursor.fetchone()
            if zone_row is None:
                conn.rollback()
                return jsonify({
                    "status": "error",
                    "message": "Falta la zona sin recargo en el catálogo.",
                }), 409

            cursor.execute(
                """
                MERGE INTO clientes c
                USING (SELECT :email email FROM dual) incoming
                   ON (c.email = incoming.email)
                WHEN MATCHED THEN UPDATE SET
                    nombre = :nombre,
                    apellido = :apellido,
                    telefono = :telefono
                WHEN NOT MATCHED THEN INSERT (nombre, apellido, telefono, email)
                VALUES (:nombre, :apellido, :telefono, :email)
                """,
                email=email,
                nombre=cliente["nombre"].strip(),
                apellido=cliente["apellido"].strip(),
                telefono=cliente["telefono"].strip(),
            )
            cursor.execute(
                "SELECT id_cliente FROM clientes WHERE email = :email",
                email=email,
            )
            client_row = cursor.fetchone()
            if client_row is None:
                raise RuntimeError("No se pudo asociar el cliente con la reserva.")

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
                    'Contratación web', 'COTIZADA', :monto_subtotal, 0,
                    :monto_total, :anticipo_requerido, :saldo_pendiente,
                    :notas_logistica, 'PENDIENTE'
                )
                """,
                codigo_reserva=code,
                id_cliente=client_row[0],
                id_formato=format_row[0],
                id_zona=zone_row[0],
                fecha_evento=datetime.combine(event_start.date(), datetime.min.time()),
                hora_inicio=event_start.strftime("%H:%M"),
                duracion_horas=duration_minutes / 60,
                direccion_evento=address.strip(),
                monto_subtotal=subtotal,
                monto_total=subtotal,
                anticipo_requerido=advance,
                saldo_pendiente=balance,
                notas_logistica=details.strip() or None,
            )
        conn.commit()
    except oracledb.DatabaseError:
        conn.rollback()
        logger.exception("No se pudo guardar la reserva pendiente %s.", code)
        return jsonify({
            "status": "error",
            "message": "Ocurrió un error al guardar la reserva.",
        }), 500
    except RuntimeError as error:
        conn.rollback()
        logger.exception("No se pudo completar la reserva pendiente %s.", code)
        return jsonify({"status": "error", "message": str(error)}), 500
    finally:
        conn.close()

    return jsonify({
        "status": "success",
        "data": {
            "codigo_reserva": code,
            "estado": "COTIZADA",
            "monto_total": subtotal,
            "anticipo_requerido": advance,
            "saldo_pendiente": balance,
        },
    }), 201


def _busy_schedule_response():
    return jsonify({
        "status": "success",
        "available": False,
        "message": "Ese horario no está disponible; debe haber al menos 45 minutos entre contratos.",
    })


@reservas_bp.route("/disponibilidad", methods=["GET"])
def consultar_disponibilidad():
    try:
        event_start, duration_minutes = _parse_schedule(
            request.args.get("fecha"),
            request.args.get("hora"),
            request.args.get("duracion_minutos"),
        )
    except ValueError as error:
        return jsonify({"status": "error", "message": str(error)}), 400

    try:
        conn = get_db_connection()
    except oracledb.Error:
        logger.exception("No se pudo conectar a Oracle para comprobar disponibilidad.")
        return jsonify({
            "status": "error",
            "message": "No se pudo comprobar la disponibilidad. Inténtalo nuevamente.",
        }), 503
    if conn is None:
        return jsonify({
            "status": "error",
            "message": "No se puede comprobar la disponibilidad porque Oracle no está disponible.",
        }), 503

    try:
        with conn.cursor() as cursor:
            has_conflict = _find_schedule_conflict(cursor, event_start, duration_minutes)
        if has_conflict:
            return _busy_schedule_response()
        return jsonify({
            "status": "success",
            "available": True,
            "message": "El horario está disponible.",
        })
    except (oracledb.Error, RuntimeError):
        logger.exception("No se pudo comprobar la disponibilidad del horario solicitado.")
        return jsonify({
            "status": "error",
            "message": "No se pudo comprobar la disponibilidad. Inténtalo nuevamente.",
        }), 500
    finally:
        conn.close()

@reservas_bp.route("/", methods=["GET"])
@admin_required
def listar_reservas():
    try:
        conn = get_db_connection()
    except oracledb.Error:
        logger.exception("No se pudo conectar a Oracle para listar reservas.")
        return jsonify({
            "status": "error",
            "message": "No se pudo conectar a la base de datos.",
        }), 503
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT r.codigo_reserva, c.nombre || ' ' || c.apellido AS cliente, 
                           r.fecha_evento, r.monto_total, r.estado_reserva
                    FROM eventos_reservas r
                    JOIN clientes c ON r.id_cliente = c.id_cliente
                    ORDER BY r.fecha_evento ASC
                """)
                filas = cursor.fetchall()
                data = [
                    {
                        "codigo_reserva": f[0],
                        "cliente": f[1],
                        "fecha_evento": str(f[2]),
                        "monto_total": float(f[3]),
                        "estado": f[4]
                    } for f in filas
                ]
                return jsonify({"status": "success", "data": data}), 200
        finally:
            conn.close()

    return jsonify({
        "status": "error",
        "message": "La base de datos no está disponible.",
    }), 503
