"""
Servicio de Cálculo Financiero y Logístico para Rosas de Guadalupe
Reglas de Negocio:
1. Anticipo obligatorio del 50% para reservar la fecha.
2. Saldo restante del 50% a liquidarse antes o al inicio del evento.
3. Comisión por procesamiento de tarjeta de crédito/débito (3.5% configurable).
4. Recargos logísticos por distancia/zona de cobertura.
"""

def calcular_cotizacion(precio_base_hora: float, duracion_horas: float, recargo_zona: float = 0.0, metodo_pago: str = "TRANSFERENCIA") -> dict:
    subtotal = round(precio_base_hora * duracion_horas, 2)
    monto_total = round(subtotal + recargo_zona, 2)
    
    # 50% de anticipo y 50% de saldo
    anticipo = round(monto_total * 0.50, 2)
    saldo_restante = round(monto_total - anticipo, 2)
    
    # Comisión si se usa pasarela de tarjeta
    comision_tarjeta = 0.0
    if metodo_pago in ["TARJETA_CREDITO", "TARJETA_DEBITO"]:
        comision_tarjeta = round(anticipo * 0.035, 2)
        
    monto_a_pagar_anticipo = round(anticipo + comision_tarjeta, 2)
    
    return {
        "subtotal_musical": subtotal,
        "recargo_logistica_zona": recargo_zona,
        "monto_total_evento": monto_total,
        "anticipo_50_requerido": anticipo,
        "saldo_50_restante": saldo_restante,
        "metodo_pago": metodo_pago,
        "comision_pasarela": comision_tarjeta,
        "total_a_pagar_hoy": monto_a_pagar_anticipo
    }
