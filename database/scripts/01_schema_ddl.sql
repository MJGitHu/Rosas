-- =============================================================================
-- PROYECTO: Rosas de Guadalupe Management System
-- SCRIPT: 01_schema_ddl.sql
-- DESCRIPCION: Definición de Tablas DDL, Constraints y Secuencias para Oracle DB
-- AUTOR: Equipo de Desarrollo (Jira Project RS)
-- =============================================================================

-- 1. TABLA: CLIENTES
CREATE TABLE clientes (
    id_cliente NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    apellido VARCHAR2(100) NOT NULL,
    telefono VARCHAR2(20) NOT NULL,
    email VARCHAR2(120) NOT NULL,
    direccion_referencia VARCHAR2(250),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_cliente_email UNIQUE (email)
);

-- 2. TABLA: ZONAS_COBERTURA (Logística y Recargos de Transporte)
CREATE TABLE zonas_cobertura (
    id_zona NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_zona VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(200),
    recargo_transporte NUMBER(10,2) DEFAULT 0.00 NOT NULL,
    tiempo_estimado_traslado_min NUMBER DEFAULT 0,
    activo CHAR(1) DEFAULT 'S' CHECK (activo IN ('S', 'N'))
);

-- 3. TABLA: FORMATOS_MARIACHI (Catálogo de Formatos Musicales)
CREATE TABLE formatos_mariachi (
    id_formato NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_formato VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(300),
    num_musicos NUMBER DEFAULT 6 NOT NULL,
    precio_base_hora NUMBER(10,2) NOT NULL,
    incluye_equipo_audio CHAR(1) DEFAULT 'N' CHECK (incluye_equipo_audio IN ('S', 'N')),
    activo CHAR(1) DEFAULT 'S' CHECK (activo IN ('S', 'N'))
);

-- 4. TABLA: EVENTOS_RESERVAS
CREATE TABLE eventos_reservas (
    id_reserva NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo_reserva VARCHAR2(20) NOT NULL UNIQUE,
    id_cliente NUMBER NOT NULL,
    id_formato NUMBER NOT NULL,
    id_zona NUMBER NOT NULL,
    fecha_evento DATE NOT NULL,
    hora_inicio VARCHAR2(10) NOT NULL,
    duracion_horas NUMBER(4,2) NOT NULL,
    direccion_evento VARCHAR2(250) NOT NULL,
    tipo_evento VARCHAR2(50), -- Boda, Cumpleaños, Serenata, Graduación, Corporativo
    estado_reserva VARCHAR2(20) DEFAULT 'COTIZADA' 
        CHECK (estado_reserva IN ('COTIZADA', 'ANTICIPO_PAGADO', 'CONFIRMADA', 'LIQUIDADA', 'CANCELADA')),
    monto_subtotal NUMBER(10,2) NOT NULL,
    recargo_zona NUMBER(10,2) DEFAULT 0.00 NOT NULL,
    monto_total NUMBER(10,2) NOT NULL,
    anticipo_requerido NUMBER(10,2) NOT NULL, -- 50% del total
    saldo_pendiente NUMBER(10,2) NOT NULL,    -- 50% restante
    notas_logistica VARCHAR2(500),
    metodo_pago_preferido VARCHAR2(30) DEFAULT 'TRANSFERENCIA' NOT NULL
        CHECK (metodo_pago_preferido IN ('TRANSFERENCIA', 'EFECTIVO', 'TARJETA_CREDITO')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reserva_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    CONSTRAINT fk_reserva_formato FOREIGN KEY (id_formato) REFERENCES formatos_mariachi(id_formato),
    CONSTRAINT fk_reserva_zona FOREIGN KEY (id_zona) REFERENCES zonas_cobertura(id_zona)
);

-- 5. TABLA: PAGOS (Gestión de Anticipos 50% y Liquidaciones 50%)
CREATE TABLE pagos (
    id_pago NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva NUMBER NOT NULL,
    tipo_pago VARCHAR2(20) NOT NULL CHECK (tipo_pago IN ('ANTICIPO_50', 'LIQUIDACION_50', 'TOTAL_100')),
    metodo_pago VARCHAR2(30) NOT NULL CHECK (metodo_pago IN ('TRANSFERENCIA', 'EFECTIVO', 'TARJETA_CREDITO', 'TARJETA_DEBITO', 'MERCADOPAGO')),
    monto_base NUMBER(10,2) NOT NULL,
    comision_pasarela NUMBER(10,2) DEFAULT 0.00 NOT NULL, -- Comisión por uso de tarjeta si aplica
    monto_cobrado NUMBER(10,2) NOT NULL,
    referencia_transaccion VARCHAR2(100),
    estado_pago VARCHAR2(20) DEFAULT 'COMPLETADO' CHECK (estado_pago IN ('PENDIENTE', 'COMPLETADO', 'RECHAZADO')),
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pago_reserva FOREIGN KEY (id_reserva) REFERENCES eventos_reservas(id_reserva)
);

-- 6. TABLA: INTEGRANTES_MARIACHI (Gestión de la alineación: 6 integrantes)
CREATE TABLE integrantes_mariachi (
    id_integrante NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_completo VARCHAR2(120) NOT NULL,
    instrumento_rol VARCHAR2(80) NOT NULL, -- 2 Trompetas, Vihuela, Guitarrón, 2 Cantantes
    telefono VARCHAR2(20),
    es_lider CHAR(1) DEFAULT 'N' CHECK (es_lider IN ('S', 'N')),
    activo CHAR(1) DEFAULT 'S' CHECK (activo IN ('S', 'N'))
);
