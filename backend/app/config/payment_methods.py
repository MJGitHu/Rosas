"""
Configuración de métodos de pago permitidos y tasas de comisión.
Subtarea Jira: RS-128 - Configurar métodos de pago permitidos para el anticipo.
Historia Jira: RS-10 - HU06: Pago del anticipo.
Proyecto: Rosas de Guadalupe Management System.
"""

# Lista de métodos de pago admitidos por el negocio para el registro y liquidación del anticipo
PAYMENT_METHODS = [
    {
        "codigo": "EFECTIVO",
        "label": "Efectivo",
        "tasa_comision": 0.00,
        "descripcion": "Pago presencial en efectivo sin recargo adicional"
    },
    {
        "codigo": "YAPE",
        "label": "Yape",
        "tasa_comision": 0.00,
        "descripcion": "Billetera digital móvil BCP (0% comisión)"
    },
    {
        "codigo": "PLIN",
        "label": "Plin",
        "tasa_comision": 0.00,
        "descripcion": "Billetera digital móvil interbancaria (0% comisión)"
    },
    {
        "codigo": "TRANSFERENCIA",
        "label": "Transferencia Bancaria",
        "tasa_comision": 0.00,
        "descripcion": "Transferencia a cuenta de ahorros o interbancaria CCI (0% comisión)"
    },
    {
        "codigo": "TARJETA_CREDITO",
        "label": "Tarjeta de Crédito",
        "tasa_comision": 0.05,
        "descripcion": "Procesamiento vía pasarela con recargo del 5% sobre el anticipo"
    },
    {
        "codigo": "TARJETA_DEBITO",
        "label": "Tarjeta de Débito",
        "tasa_comision": 0.05,
        "descripcion": "Procesamiento vía pasarela con recargo del 5% sobre el anticipo"
    },
    {
        "codigo": "MERCADOPAGO",
        "label": "Mercado Pago",
        "tasa_comision": 0.00,
        "descripcion": "Pago en línea mediante Checkout Pro de Mercado Pago"
    },
    {
        "codigo": "PRUEBA",
        "label": "Prueba",
        "tasa_comision": 0.00,
        "descripcion": "Pago total de prueba por S/ 1.00"
    }
]

# Mapa rápido para búsquedas O(1)
_METODOS_MAP = {metodo["codigo"]: metodo for metodo in PAYMENT_METHODS}


def get_comision(metodo_pago: str) -> float:
    """
    Retorna la tasa de comisión aplicable a un método de pago.
    
    Regla de Negocio (RS-8, RS-10, RS-129):
    - Tarjeta de Crédito / Débito: 5% (0.05) sobre el monto del anticipo.
    - Efectivo, Yape, Plin, Transferencia: 0% (0.00).
    
    Args:
        metodo_pago (str): Código o identificador del método de pago (ej. 'TARJETA_CREDITO', 'YAPE').
        
    Returns:
        float: Tasa de comisión (ej. 0.05 o 0.00). Retorna 0.00 si el método no es reconocido.
    """
    if not metodo_pago:
        return 0.00
    
    codigo_normalizado = str(metodo_pago).strip().upper()
    metodo = _METODOS_MAP.get(codigo_normalizado)
    if metodo:
        return float(metodo["tasa_comision"])
    
    return 0.00


def get_metodos_validos() -> list:
    """
    Retorna la lista de códigos de los métodos de pago válidos y habilitados en el sistema.
    
    Returns:
        list: Lista de strings con los códigos permitidos:
              ['EFECTIVO', 'YAPE', 'PLIN', 'TRANSFERENCIA', 'TARJETA_CREDITO', 'TARJETA_DEBITO']
    """
    return [metodo["codigo"] for metodo in PAYMENT_METHODS]
