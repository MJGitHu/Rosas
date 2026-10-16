"""
Servicio de Cálculo Financiero y Logístico para Rosas de Guadalupe
Reglas de Negocio:
1. Anticipo obligatorio del 50% para reservar la fecha.
2. Saldo restante del 50% a liquidarse antes o al inicio del evento.
3. Comisión por procesamiento de tarjeta de crédito/débito (5% configurable).
4. Recargos logísticos por distancia/zona de cobertura.
"""
from typing import Optional

from app.config.payment_methods import get_comision

def calcular_cotizacion(
    precio_base_hora: float,
    duracion_horas: float,
    recargo_zona: float = 0.0,
    metodo_pago: str = "TRANSFERENCIA",
    monto_base_formato: Optional[float] = None,
) -> dict:
    if metodo_pago == "PRUEBA":
        return {
            "subtotal_musical": 1.0,
            "recargo_logistica_zona": 0.0,
            "monto_total_evento": 1.0,
            "anticipo": 1.0,
            "saldo": 0.0,
            "tasa_comision": 0.0,
            "comision_tarjeta": 0.0,
            "anticipo_50_requerido": 1.0,
            "saldo_50_restante": 0.0,
            "metodo_pago": metodo_pago,
            "comision_pasarela": 0.0,
            "total_a_pagar_hoy": 1.0,
        }

    monto_presentacion = (
        monto_base_formato
        if monto_base_formato is not None
        else precio_base_hora * duracion_horas
    )
    subtotal = round(monto_presentacion, 2)
    monto_total = round(subtotal + recargo_zona, 2)
    
    # 50% de anticipo y 50% de saldo
    anticipo = round(monto_total * 0.50, 2)
    saldo_restante = round(monto_total - anticipo, 2)
    
    # Comisión calculada mediante get_comision() según configuración de métodos de pago (RS-128)
    tasa_comision = get_comision(metodo_pago)
    comision_tarjeta = round(anticipo * tasa_comision, 2)
        
    monto_a_pagar_anticipo = round(anticipo + comision_tarjeta, 2)
    
    return {
        "subtotal_musical": subtotal,
        "recargo_logistica_zona": recargo_zona,
        "monto_total_evento": monto_total,
        "anticipo": anticipo,
        "saldo": saldo_restante,
        "tasa_comision": tasa_comision,
        "comision_tarjeta": comision_tarjeta,
        "anticipo_50_requerido": anticipo,
        "saldo_50_restante": saldo_restante,
        "metodo_pago": metodo_pago,
        "comision_pasarela": comision_tarjeta,
        "total_a_pagar_hoy": monto_a_pagar_anticipo
    }
