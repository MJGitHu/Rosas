from flask import Blueprint, request, jsonify
from app.services.calculator_service import calcular_cotizacion

cotizaciones_bp = Blueprint("cotizaciones", __name__)

@cotizaciones_bp.route("/calcular", methods=["POST"])
def calcular():
    data = request.get_json() or {}
    precio_base_hora = float(data.get("precio_base_hora", 2800.0))
    duracion_horas = float(data.get("duracion_horas", 1.0))
    recargo_zona = float(data.get("recargo_zona", 0.0))
    metodo_pago = data.get("metodo_pago", "TRANSFERENCIA")
    
    resultado = calcular_cotizacion(precio_base_hora, duracion_horas, recargo_zona, metodo_pago)
    return jsonify({
        "status": "success",
        "data": resultado
    }), 200
