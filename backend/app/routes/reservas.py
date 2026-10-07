from flask import Blueprint, request, jsonify
from app.db import get_db_connection
import uuid

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route("/", methods=["GET"])
def listar_reservas():
    # Retorna listado de reservas (desde Oracle DB o mock demostrativo)
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
    
    # Mock fallback si la base de datos no está levantada aún
    return jsonify({
        "status": "success",
        "modo": "offline_preview",
        "data": [
            {
                "codigo_reserva": "RS-2026-001",
                "cliente": "Elena Gómez",
                "fecha_evento": "2026-10-15",
                "monto_total": 3050.00,
                "estado": "ANTICIPO_PAGADO"
            }
        ]
    }), 200
