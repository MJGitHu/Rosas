from datetime import datetime
from functools import wraps
import hmac
import logging
import secrets
import threading
import time
from urllib.parse import urlsplit

import oracledb
from flask import Blueprint, current_app, jsonify, request, session
from werkzeug.security import check_password_hash

from app.db import get_db_connection

admin_bp = Blueprint("admin", __name__)
logger = logging.getLogger(__name__)
LOGIN_WINDOW_SECONDS = 15 * 60
MAX_LOGIN_ATTEMPTS = 5
login_attempts = {}
login_attempts_lock = threading.Lock()


def _configuration_ready():
    secret_key = current_app.config.get("SECRET_KEY")
    return (
        isinstance(secret_key, str)
        and len(secret_key) >= 64
        and bool(current_app.config.get("ADMIN_USERNAME"))
        and bool(current_app.config.get("ADMIN_PASSWORD_HASH"))
    )


def _origin_allowed():
    origin = request.headers.get("Origin")
    if not origin:
        return True
    if origin in current_app.config["FRONTEND_ORIGINS"]:
        return True
    if origin == request.host_url.rstrip("/"):
        return True
    if current_app.config.get("FLASK_ENV", "").lower() != "development":
        return False

    parsed_origin = urlsplit(origin)
    if parsed_origin.scheme not in {"http", "https"} or not parsed_origin.hostname:
        return False

    forwarded_host = request.headers.get("X-Forwarded-Host", "").split(",", 1)[0].strip()
    if not forwarded_host:
        return False
    forwarded_proto = (
        request.headers.get("X-Forwarded-Proto", "").split(",", 1)[0].strip().lower()
        or request.scheme
    )
    if forwarded_proto not in {"http", "https"}:
        return False
    try:
        forwarded_origin = urlsplit(f"{forwarded_proto}://{forwarded_host}")
        return (
            forwarded_origin.hostname is not None
            and parsed_origin.scheme == forwarded_origin.scheme
            and parsed_origin.netloc.casefold() == forwarded_origin.netloc.casefold()
            and not parsed_origin.path
            and not parsed_origin.query
            and not parsed_origin.fragment
        )
    except ValueError:
        return False


def _login_rate_limited(client_ip):
    now = time.monotonic()
    with login_attempts_lock:
        expired_ips = [
            ip
            for ip, timestamps in login_attempts.items()
            if not timestamps or now - timestamps[-1] >= LOGIN_WINDOW_SECONDS
        ]
        for ip in expired_ips:
            login_attempts.pop(ip, None)

        recent_attempts = [
            timestamp
            for timestamp in login_attempts.get(client_ip, [])
            if now - timestamp < LOGIN_WINDOW_SECONDS
        ]
        login_attempts[client_ip] = recent_attempts
        return len(recent_attempts) >= MAX_LOGIN_ATTEMPTS


def _record_failed_login(client_ip):
    now = time.monotonic()
    with login_attempts_lock:
        login_attempts.setdefault(client_ip, []).append(now)


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return jsonify({"status": "error", "message": "Se requiere iniciar sesión."}), 401
        response = current_app.make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        return response

    return wrapped


@admin_bp.after_request
def prevent_admin_response_caching(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response


@admin_bp.route("/session", methods=["GET"])
def session_status():
    if session.get("is_admin"):
        return jsonify({
            "authenticated": True,
            "username": session.get("admin_username"),
            "csrf_token": session.get("csrf_token"),
        })
    return jsonify({"authenticated": False})


@admin_bp.route("/login", methods=["POST"])
def login():
    if not _origin_allowed():
        return jsonify({"status": "error", "message": "Origen no permitido."}), 403
    if not _configuration_ready():
        logger.error(
            "Falta una SECRET_KEY de 64 caracteres, ADMIN_USERNAME o ADMIN_PASSWORD_HASH."
        )
        return jsonify({
            "status": "error",
            "message": "La administración no está configurada en el servidor.",
        }), 503

    client_ip = request.remote_addr or "unknown"
    if _login_rate_limited(client_ip):
        return jsonify({
            "status": "error",
            "message": "Demasiados intentos. Espera 15 minutos antes de volver a intentarlo.",
        }), 429

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "El cuerpo de la solicitud debe ser JSON."}), 400
    username = data.get("username")
    password = data.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        _record_failed_login(client_ip)
        return jsonify({"status": "error", "message": "Usuario o contraseña incorrectos."}), 401

    username_matches = hmac.compare_digest(
        username.encode("utf-8"),
        current_app.config["ADMIN_USERNAME"].encode("utf-8"),
    )
    try:
        password_matches = check_password_hash(
            current_app.config["ADMIN_PASSWORD_HASH"], password
        )
    except (TypeError, ValueError):
        logger.exception("ADMIN_PASSWORD_HASH no es un hash de contraseña válido.")
        return jsonify({
            "status": "error",
            "message": "La configuración de administración no es válida.",
        }), 503

    if not (username_matches and password_matches):
        _record_failed_login(client_ip)
        return jsonify({"status": "error", "message": "Usuario o contraseña incorrectos."}), 401

    session.clear()
    session.permanent = True
    session["is_admin"] = True
    session["admin_username"] = current_app.config["ADMIN_USERNAME"]
    session["csrf_token"] = secrets.token_urlsafe(32)
    return jsonify({
        "authenticated": True,
        "username": session["admin_username"],
        "csrf_token": session["csrf_token"],
    })


@admin_bp.route("/logout", methods=["POST"])
@admin_required
def logout():
    if not _origin_allowed():
        return jsonify({"status": "error", "message": "Origen no permitido."}), 403
    csrf_token = request.headers.get("X-CSRF-Token", "")
    if not hmac.compare_digest(
        csrf_token.encode("utf-8"),
        session.get("csrf_token", "").encode("utf-8"),
    ):
        return jsonify({"status": "error", "message": "Token de seguridad inválido."}), 403
    session.clear()
    return jsonify({"authenticated": False})


@admin_bp.route("/reservas/<codigo_reserva>/marcar-pagado", methods=["POST"])
@admin_required
def marcar_reserva_pagada(codigo_reserva):
    if not _origin_allowed():
        return jsonify({"status": "error", "message": "Origen no permitido."}), 403
    csrf_token = request.headers.get("X-CSRF-Token", "")
    if not hmac.compare_digest(
        csrf_token.encode("utf-8"),
        session.get("csrf_token", "").encode("utf-8"),
    ):
        return jsonify({"status": "error", "message": "Token de seguridad inválido."}), 403

    try:
        conn = get_db_connection()
    except oracledb.Error:
        logger.exception("No se pudo conectar a Oracle para actualizar el estado del contrato.")
        return jsonify({
            "status": "error",
            "message": "No se pudo conectar a la base de datos.",
        }), 503
    if conn is None:
        return jsonify({
            "status": "error",
            "message": "La base de datos no está disponible.",
        }), 503

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE eventos_reservas
                SET estado_reserva = 'ANTICIPO_PAGADO'
                WHERE codigo_reserva = :codigo_reserva
                  AND estado_reserva = 'COTIZADA'
                """,
                codigo_reserva=codigo_reserva,
            )
            if cursor.rowcount != 1:
                conn.rollback()
                return jsonify({
                    "status": "error",
                    "message": "No se encontró un contrato pendiente para actualizar.",
                }), 409
        conn.commit()
    except oracledb.Error:
        conn.rollback()
        logger.exception("No se pudo marcar como pagado el contrato %s.", codigo_reserva)
        return jsonify({
            "status": "error",
            "message": "No se pudo actualizar el estado del contrato.",
        }), 500
    finally:
        conn.close()

    return jsonify({
        "status": "success",
        "data": {
            "codigo_reserva": codigo_reserva,
            "estado": "ANTICIPO_PAGADO",
            "mensaje": "Anticipo del 50% marcado como pagado.",
        },
    }), 200


@admin_bp.route("/reservas", methods=["GET"])
@admin_required
def listar_reservas_mes():
    month_value = request.args.get("mes", "")
    try:
        start_date = datetime.strptime(month_value, "%Y-%m")
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "El mes debe tener el formato AAAA-MM.",
        }), 400

    if start_date.strftime("%Y-%m") != month_value:
        return jsonify({
            "status": "error",
            "message": "El mes debe tener el formato AAAA-MM.",
        }), 400

    try:
        if start_date.month == 12:
            end_date = start_date.replace(year=start_date.year + 1, month=1)
        else:
            end_date = start_date.replace(month=start_date.month + 1)
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "El mes está fuera del rango admitido.",
        }), 400

    try:
        conn = get_db_connection()
    except oracledb.Error:
        logger.exception("Error conectando con Oracle para cargar el calendario administrativo.")
        return jsonify({
            "status": "error",
            "message": "No se pudo conectar a Oracle para cargar el calendario.",
        }), 500
    if conn is None:
        logger.error("No se puede cargar el calendario administrativo: Oracle no está disponible.")
        return jsonify({
            "status": "error",
            "message": "La base de datos no está disponible. No se mostraron datos de ejemplo.",
        }), 503

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT r.codigo_reserva,
                       c.nombre,
                       c.apellido,
                       c.telefono,
                       c.email,
                       f.nombre_formato,
                       r.fecha_evento,
                       r.hora_inicio,
                       r.duracion_horas,
                       r.direccion_evento,
                       r.tipo_evento,
                       r.estado_reserva,
                       r.monto_subtotal,
                       r.recargo_zona,
                       r.monto_total,
                       r.anticipo_requerido,
                       r.saldo_pendiente,
                       r.notas_logistica,
                       r.metodo_pago_preferido
                FROM eventos_reservas r
                JOIN clientes c ON c.id_cliente = r.id_cliente
                JOIN formatos_mariachi f ON f.id_formato = r.id_formato
                WHERE r.fecha_evento >= :start_date
                  AND r.fecha_evento < :end_date
                ORDER BY r.fecha_evento, r.hora_inicio
                """,
                start_date=start_date,
                end_date=end_date,
            )
            rows = cursor.fetchall()
        data = [
            {
                "codigo_reserva": row[0],
                "nombre": row[1],
                "apellido": row[2],
                "telefono": row[3],
                "email": row[4],
                "formato": row[5],
                "fecha_evento": row[6].strftime("%Y-%m-%d"),
                "hora_inicio": row[7],
                "duracion_horas": float(row[8]),
                "direccion_evento": row[9],
                "tipo_evento": row[10],
                "estado": row[11],
                "subtotal": float(row[12]),
                "recargo": float(row[13]),
                "total": float(row[14]),
                "anticipo": float(row[15]),
                "saldo_pendiente": float(row[16]),
                "detalles": row[17],
                "metodo_pago": row[18],
            }
            for row in rows
        ]
        return jsonify({"status": "success", "data": data})
    except oracledb.Error:
        logger.exception("Error consultando las reservas del calendario administrativo.")
        return jsonify({
            "status": "error",
            "message": "No se pudo cargar el calendario. Revisa la conexión y el esquema de Oracle.",
        }), 500
    finally:
        conn.close()
