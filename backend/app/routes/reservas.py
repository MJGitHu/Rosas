from datetime import date, datetime
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
METODOS_PAGO = {"TRANSFERENCIA", "TARJETA_CREDITO", "EFECTIVO"}

@reservas_bp.route("/", methods=["GET"])
@admin_required
def listar_reservas():
    conn = get_db_connection()
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


@reservas_bp.route("/", methods=["POST"])
def crear_reserva():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "El cuerpo de la solicitud debe ser JSON."}), 400

    cliente = data.get("cliente")
    if not isinstance(cliente, dict):
        return jsonify({"status": "error", "message": "Faltan los datos del cliente."}), 400

    required_fields = {
        "nombre": 100,
        "apellido": 100,
        "telefono": 20,
        "email": 120,
    }
    for field, max_length in required_fields.items():
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
    try:
        duration_minutes = int(data.get("duracion_minutos"))
        additional_hours = int(data.get("horas_adicionales", 0))
        event_date = date.fromisoformat(data.get("fecha_evento", ""))
        event_time = datetime.strptime(data.get("hora_evento", ""), "%H:%M").strftime("%H:%M")
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "La duración, fecha u hora del evento no son válidas."}), 400

    if service is None or duration_minutes not in {30, 40, 60}:
        return jsonify({"status": "error", "message": "Selecciona un formato y duración válidos."}), 400
    if additional_hours < 0 or additional_hours > 6:
        return jsonify({"status": "error", "message": "Las horas adicionales deben estar entre 0 y 6."}), 400
    if event_date < date.today():
        return jsonify({"status": "error", "message": "La fecha del evento no puede estar en el pasado."}), 400

    address = data.get("direccion_evento")
    details = data.get("detalles", "")
    payment_method = data.get("metodo_pago")
    if not isinstance(address, str) or not address.strip() or len(address.strip()) > 250:
        return jsonify({"status": "error", "message": "La dirección es obligatoria y no puede exceder 250 caracteres."}), 400
    if not isinstance(details, str) or len(details.strip()) > 500:
        return jsonify({"status": "error", "message": "Los detalles no pueden exceder 500 caracteres."}), 400
    if not isinstance(payment_method, str) or payment_method not in METODOS_PAGO:
        return jsonify({"status": "error", "message": "Selecciona un método de pago válido."}), 400

    base_price = service["precios"][duration_minutes]
    additional_hour_price = service["precios"][60] - 60
    subtotal = round(base_price + additional_hours * additional_hour_price, 2)
    advance = round(subtotal * 0.5, 2)
    balance = round(subtotal - advance, 2)
    duration_hours = (duration_minutes + additional_hours * 60) / 60

    conn = get_db_connection()
    if conn is None:
        return jsonify({
            "status": "error",
            "message": "La base de datos no está disponible. El contrato no se guardó.",
        }), 503

    code = f"RS-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}"
    try:
        with conn.cursor() as cursor:
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
                    "message": "El catálogo de formatos no está actualizado. Ejecuta la migración de servicios.",
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
                    "message": "Falta la zona sin recargo en el catálogo. Ejecuta la migración de servicios.",
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
                WHEN NOT MATCHED THEN INSERT (
                    nombre, apellido, telefono, email
                ) VALUES (
                    :nombre, :apellido, :telefono, :email
                )
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
                raise RuntimeError("No se pudo obtener el cliente creado para la reserva.")

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
                    :notas_logistica, :metodo_pago_preferido
                )
                """,
                codigo_reserva=code,
                id_cliente=client_row[0],
                id_formato=format_row[0],
                id_zona=zone_row[0],
                fecha_evento=datetime.combine(event_date, datetime.min.time()),
                hora_inicio=event_time,
                duracion_horas=duration_hours,
                direccion_evento=address.strip(),
                monto_subtotal=subtotal,
                monto_total=subtotal,
                anticipo_requerido=advance,
                saldo_pendiente=balance,
                notas_logistica=details.strip() or None,
                metodo_pago_preferido=payment_method,
            )
        conn.commit()
    except oracledb.DatabaseError:
        conn.rollback()
        logger.exception("No se pudo guardar la reserva %s en Oracle.", code)
        return jsonify({
            "status": "error",
            "message": "Ocurrió un error al guardar el contrato en la base de datos.",
        }), 500
    except RuntimeError as error:
        conn.rollback()
        logger.exception("No se pudo completar la reserva %s.", code)
        return jsonify({"status": "error", "message": str(error)}), 500
    finally:
        conn.close()

    return jsonify({
        "status": "success",
        "data": {
            "codigo_reserva": code,
            "monto_total": subtotal,
            "anticipo_requerido": advance,
            "saldo_pendiente": balance,
        },
    }), 201
