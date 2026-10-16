-- =============================================================================
-- PROYECTO: Rosas de Guadalupe Management System
-- SUBTAREA JIRA: RS-137 - Diseñar modelo de pagos, anticipos y estados
-- SCRIPT: 05_pagos_seed.sql
-- DESCRIPCIÓN: Datos semilla con 3 reservas y 3 pagos en Soles (S/):
--              1. Tarjeta de Crédito (Comisión del 5%: S/ 70.00 sobre S/ 1,400.00)
--              2. Yape (Comisión 0%)
--              3. Transferencia Interbancaria Peruana (Comisión 0% con TRANSF-INTERBANCARIA)
-- AUTOR: Equipo de Desarrollo (Jira Project RS)
-- =============================================================================

-- =============================================================================
-- LIMPIEZA PREVIA (Idempotencia para reejecución)
-- =============================================================================
DELETE FROM pagos WHERE id_reserva IN (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva IN ('RS-2026-001', 'RS-2026-002', 'RS-2026-003'));
DELETE FROM anticipos WHERE id_reserva IN (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva IN ('RS-2026-001', 'RS-2026-002', 'RS-2026-003'));
DELETE FROM eventos_reservas WHERE codigo_reserva IN ('RS-2026-001', 'RS-2026-002', 'RS-2026-003');
DELETE FROM clientes WHERE email IN ('beatriz.mendoza@email.com', 'carlos.navarro@email.com', 'lucia.fernandez@email.com');
COMMIT;

-- =============================================================================
-- CASO 1: RESERVA CON ANTICIPO VÍA TARJETA DE CRÉDITO (COMISIÓN DEL 5%)
-- =============================================================================
-- 1.1 Cliente 1
INSERT INTO clientes (nombre, apellido, telefono, email, direccion_referencia)
VALUES ('Beatriz', 'Mendoza', '981234567', 'beatriz.mendoza@email.com', 'Urb. San Andrés, Trujillo');

-- 1.2 Reserva 1: 1 hora (S/ 2,800.00) en Zona Centro (S/ 0.00). Total: S/ 2,800.00
INSERT INTO eventos_reservas (
    codigo_reserva, id_cliente, id_formato, id_zona, fecha_evento,
    hora_inicio, duracion_horas, direccion_evento, tipo_evento, estado_reserva,
    monto_subtotal, recargo_zona, monto_total, anticipo_requerido, saldo_pendiente,
    notas_logistica
) VALUES (
    'RS-2026-001',
    (SELECT id_cliente FROM clientes WHERE email = 'beatriz.mendoza@email.com'),
    (SELECT id_formato FROM formatos_mariachi WHERE nombre_formato = 'Mariachi completo'),
    (SELECT id_zona FROM zonas_cobertura WHERE nombre_zona LIKE '%Centro%'),
    TO_DATE('2026-10-25', 'YYYY-MM-DD'),
    '20:00',
    1.0,
    'Av. Larco 1050, Salón Atenas',
    'Cumpleaños',
    'ANTICIPO_PAGADO',
    2800.00,
    0.00,
    2800.00,
    1400.00, -- Anticipo 50% en S/
    1400.00, -- Saldo 50% en S/
    'Acceso por puerta principal, sorpresa para la agasajada'
);

-- 1.3 Anticipo 1 (Proyección 50/50)
INSERT INTO anticipos (id_reserva, monto_anticipo, monto_saldo, porcentaje, fecha_limite_saldo, estado)
VALUES (
    (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-001'),
    1400.00,
    1400.00,
    50.00,
    TO_DATE('2026-10-25', 'YYYY-MM-DD'),
    'PAGADO'
);

-- 1.4 Pago 1: Tarjeta de Crédito (Comisión del 5% = S/ 70.00 sobre anticipo de S/ 1,400.00)
INSERT INTO pagos (id_reserva, monto, metodo_pago, comision, num_operacion, tipo_pago, fecha_pago)
VALUES (
    (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-001'),
    1400.00,
    'TARJETA_CREDITO',
    70.00, -- Comisión del 5% reglamentaria del proyecto RS
    'AUTH-VISA-982341',
    'ANTICIPO',
    CURRENT_TIMESTAMP
);


-- =============================================================================
-- CASO 2: RESERVA CON ANTICIPO VÍA YAPE (COMISIÓN 0%)
-- =============================================================================
-- 2.1 Cliente 2
INSERT INTO clientes (nombre, apellido, telefono, email, direccion_referencia)
VALUES ('Carlos', 'Navarro', '998765432', 'carlos.navarro@email.com', 'Urb. Primavera, Trujillo');

-- 2.2 Reserva 2: 40 minutos (S/ 2,200.00) + Recargo Zona Norte (S/ 250.00). Total: S/ 2,450.00
INSERT INTO eventos_reservas (
    codigo_reserva, id_cliente, id_formato, id_zona, fecha_evento,
    hora_inicio, duracion_horas, direccion_evento, tipo_evento, estado_reserva,
    monto_subtotal, recargo_zona, monto_total, anticipo_requerido, saldo_pendiente,
    notas_logistica
) VALUES (
    'RS-2026-002',
    (SELECT id_cliente FROM clientes WHERE email = 'carlos.navarro@email.com'),
    (SELECT id_formato FROM formatos_mariachi WHERE nombre_formato = 'Mariachi completo'),
    (SELECT id_zona FROM zonas_cobertura WHERE nombre_zona LIKE '%Norte%'),
    TO_DATE('2026-10-28', 'YYYY-MM-DD'),
    '21:30',
    0.75,
    'Calle Los Jazmines 340, Urb. Primavera',
    'Serenata romántica',
    'ANTICIPO_PAGADO',
    2200.00,
    250.00,
    2450.00,
    1225.00, -- Anticipo 50% en S/
    1225.00, -- Saldo 50% en S/
    'Llegar discretamente con instrumentos afinados'
);

-- 2.3 Anticipo 2 (Proyección 50/50)
INSERT INTO anticipos (id_reserva, monto_anticipo, monto_saldo, porcentaje, fecha_limite_saldo, estado)
VALUES (
    (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-002'),
    1225.00,
    1225.00,
    50.00,
    TO_DATE('2026-10-28', 'YYYY-MM-DD'),
    'PAGADO'
);

-- 2.4 Pago 2: Yape (Comisión 0%)
INSERT INTO pagos (id_reserva, monto, metodo_pago, comision, num_operacion, tipo_pago, fecha_pago)
VALUES (
    (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-002'),
    1225.00,
    'YAPE',
    0.00, -- Comisión 0%
    'YAPE-OP-849102',
    'ANTICIPO',
    CURRENT_TIMESTAMP
);


-- =============================================================================
-- CASO 3: RESERVA CON ANTICIPO VÍA TRANSFERENCIA INTERBANCARIA PERUANA (COMISIÓN 0%)
-- =============================================================================
-- 3.1 Cliente 3
INSERT INTO clientes (nombre, apellido, telefono, email, direccion_referencia)
VALUES ('Lucía', 'Fernández', '973344556', 'lucia.fernandez@email.com', 'Campiña de Moche, La Libertad');

-- 3.2 Reserva 3: 2 horas (S/ 5,200.00) + Recargo Campestre (S/ 600.00). Total: S/ 5,800.00
INSERT INTO eventos_reservas (
    codigo_reserva, id_cliente, id_formato, id_zona, fecha_evento,
    hora_inicio, duracion_horas, direccion_evento, tipo_evento, estado_reserva,
    monto_subtotal, recargo_zona, monto_total, anticipo_requerido, saldo_pendiente,
    notas_logistica
) VALUES (
    'RS-2026-003',
    (SELECT id_cliente FROM clientes WHERE email = 'lucia.fernandez@email.com'),
    (SELECT id_formato FROM formatos_mariachi WHERE nombre_formato = 'Mariachi completo'),
    (SELECT id_zona FROM zonas_cobertura WHERE nombre_zona LIKE '%Campestre%'),
    TO_DATE('2026-11-05', 'YYYY-MM-DD'),
    '18:00',
    2.0,
    'Fundo El Rosal, Campiña de Moche',
    'Boda',
    'ANTICIPO_PAGADO',
    5200.00,
    600.00,
    5800.00,
    2900.00, -- Anticipo 50% en S/
    2900.00, -- Saldo 50% en S/
    'Incluye equipo de sonido y microfonía profesional'
);

-- 3.3 Anticipo 3 (Proyección 50/50)
INSERT INTO anticipos (id_reserva, monto_anticipo, monto_saldo, porcentaje, fecha_limite_saldo, estado)
VALUES (
    (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-003'),
    2900.00,
    2900.00,
    50.00,
    TO_DATE('2026-11-05', 'YYYY-MM-DD'),
    'PAGADO'
);

-- 3.4 Pago 3: Transferencia Interbancaria (Comisión 0% con TRANSF-INTERBANCARIA)
INSERT INTO pagos (id_reserva, monto, metodo_pago, comision, num_operacion, tipo_pago, fecha_pago)
VALUES (
    (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-003'),
    2900.00,
    'TRANSFERENCIA',
    0.00, -- Comisión 0%
    'TRANSF-INTERBANCARIA-BCP-002194881029',
    'ANTICIPO',
    CURRENT_TIMESTAMP
);

COMMIT;
