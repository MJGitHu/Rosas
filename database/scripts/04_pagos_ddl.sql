-- =============================================================================
-- PROYECTO: Rosas de Guadalupe Management System
-- SUBTAREA JIRA: RS-137 - Diseñar modelo de pagos, anticipos y estados
-- SCRIPT: 04_pagos_ddl.sql
-- DESCRIPCIÓN: 1. Creación/Recreación limpia de la tabla PAGOS según especificación RS-137.
--              2. Creación de la tabla ANTICIPOS (relación 1:1 con eventos_reservas).
-- AUTOR: Equipo de Desarrollo (Jira Project RS)
-- =============================================================================

-- =============================================================================
-- 1. TABLA: PAGOS (Esquema normalizado RS-137)
-- =============================================================================
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE pagos CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF; -- Ignorar si no existe
END;
/

CREATE TABLE pagos (
    id_pago         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva      NUMBER NOT NULL,
    monto           NUMBER(10,2) NOT NULL,
    metodo_pago     VARCHAR2(30) NOT NULL,
    comision        NUMBER(10,2) DEFAULT 0.00 NOT NULL,
    num_operacion   VARCHAR2(100),
    tipo_pago       VARCHAR2(20) NOT NULL,
    fecha_pago      TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_pago_reserva FOREIGN KEY (id_reserva) 
        REFERENCES eventos_reservas(id_reserva) ON DELETE CASCADE,
    CONSTRAINT chk_pago_tipo 
        CHECK (tipo_pago IN ('ANTICIPO', 'SALDO')),
    CONSTRAINT chk_pago_metodo 
        CHECK (metodo_pago IN ('EFECTIVO', 'YAPE', 'PLIN', 'TRANSFERENCIA', 'TARJETA_CREDITO', 'TARJETA_DEBITO'))
);

-- =============================================================================
-- 2. TABLA: ANTICIPOS (Relación 1:1 con eventos_reservas)
-- =============================================================================
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE anticipos CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF; -- Ignorar si no existe
END;
/

CREATE TABLE anticipos (
    id_anticipo         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva          NUMBER NOT NULL,
    monto_anticipo      NUMBER(10,2) NOT NULL,
    monto_saldo         NUMBER(10,2) NOT NULL,
    porcentaje          NUMBER(5,2) DEFAULT 50.00 NOT NULL,
    fecha_limite_saldo  DATE NOT NULL,
    estado              VARCHAR2(30) DEFAULT 'PENDIENTE' NOT NULL,
    fecha_creacion      TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_anticipos_reserva FOREIGN KEY (id_reserva) 
        REFERENCES eventos_reservas(id_reserva) ON DELETE CASCADE,
    CONSTRAINT uq_anticipos_reserva UNIQUE (id_reserva), -- Garantiza relación estricta 1:1
    CONSTRAINT chk_anticipo_estado 
        CHECK (estado IN ('PENDIENTE', 'PAGADO', 'VENCIDO', 'REEMBOLSADO'))
);

-- NOTA: La tabla ESTADOS_RESERVA ya existe en 03_canciones_ddl.sql, por lo que no se recrea aquí.
