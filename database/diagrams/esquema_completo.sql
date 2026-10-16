-- =============================================================================
-- ESQUEMA COMPLETO DDL: Rosas de Guadalupe Management System
-- MOTOR: Oracle Database 21c (PDB: XEPDB1) | ESQUEMA: ROSAS_ADMIN
-- TOTAL TABLAS: 11 (100% Interconectadas, 3NF, Cero Tablas Huérfanas)
-- COMPATIBILIDAD: Oracle SQL / dbdiagram.io / DBeaver / SQL Developer
-- =============================================================================

-- 1. TABLA: CLIENTES
CREATE TABLE clientes (
    id_cliente NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    apellido VARCHAR2(100) NOT NULL,
    telefono VARCHAR2(20) NOT NULL,
    email VARCHAR2(120) NOT NULL CONSTRAINT uq_cliente_email UNIQUE,
    direccion_referencia VARCHAR2(250),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABLA: ZONAS_COBERTURA
CREATE TABLE zonas_cobertura (
    id_zona NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_zona VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(200),
    recargo_transporte NUMBER(10,2) DEFAULT 0.00 NOT NULL,
    tiempo_estimado_traslado_min NUMBER DEFAULT 0,
    activo CHAR(1) DEFAULT 'S' CHECK (activo IN ('S', 'N'))
);

-- 3. TABLA: FORMATOS_MARIACHI
CREATE TABLE formatos_mariachi (
    id_formato NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_formato VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(300),
    num_musicos NUMBER DEFAULT 6 NOT NULL,
    precio_base_hora NUMBER(10,2) NOT NULL,
    incluye_equipo_audio CHAR(1) DEFAULT 'N' CHECK (incluye_equipo_audio IN ('S', 'N')),
    activo CHAR(1) DEFAULT 'S' CHECK (activo IN ('S', 'N'))
);

-- 4. TABLA: INTEGRANTES_MARIACHI (Elenco Artístico)
CREATE TABLE integrantes_mariachi (
    id_integrante NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_completo VARCHAR2(120) NOT NULL,
    instrumento_rol VARCHAR2(80) NOT NULL,
    telefono VARCHAR2(20),
    es_lider CHAR(1) DEFAULT 'N' CHECK (es_lider IN ('S', 'N')),
    activo CHAR(1) DEFAULT 'S' CHECK (activo IN ('S', 'N'))
);

-- 5. TABLA: ESTADOS_RESERVA (Catálogo de Estados de Flujo)
CREATE TABLE estados_reserva (
    id_estado NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo VARCHAR2(30) NOT NULL UNIQUE,
    nombre VARCHAR2(60) NOT NULL,
    descripcion VARCHAR2(200),
    es_final CHAR(1) DEFAULT 'N' CHECK (es_final IN ('S', 'N')),
    orden_flujo NUMBER(2) NOT NULL
);

-- 6. TABLA: EVENTOS_RESERVAS (Entidad Central Transaccional)
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
    tipo_evento VARCHAR2(50),
    estado_reserva VARCHAR2(30) DEFAULT 'COTIZADA' NOT NULL,
    monto_subtotal NUMBER(10,2) NOT NULL,
    recargo_zona NUMBER(10,2) DEFAULT 0.00 NOT NULL,
    monto_total NUMBER(10,2) NOT NULL,
    anticipo_requerido NUMBER(10,2) NOT NULL,
    saldo_pendiente NUMBER(10,2) NOT NULL,
    notas_logistica VARCHAR2(500),
    metodo_pago_preferido VARCHAR2(30) DEFAULT 'TRANSFERENCIA' NOT NULL
        CHECK (metodo_pago_preferido IN ('TRANSFERENCIA', 'EFECTIVO', 'TARJETA_CREDITO')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_reserva_estado CHECK (estado_reserva IN ('COTIZADA', 'ANTICIPO_PAGADO', 'CONFIRMADA', 'LIQUIDADA', 'CANCELADA')),
    CONSTRAINT fk_reserva_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    CONSTRAINT fk_reserva_formato FOREIGN KEY (id_formato) REFERENCES formatos_mariachi(id_formato),
    CONSTRAINT fk_reserva_zona FOREIGN KEY (id_zona) REFERENCES zonas_cobertura(id_zona),
    CONSTRAINT fk_reserva_estado FOREIGN KEY (estado_reserva) REFERENCES estados_reserva(codigo)
);

-- 7. TABLA: ANTICIPOS (Regla de Negocio 50/50 - Relación 1:1)
CREATE TABLE anticipos (
    id_anticipo NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva NUMBER NOT NULL UNIQUE,
    monto_anticipo NUMBER(10,2) NOT NULL,
    monto_saldo NUMBER(10,2) NOT NULL,
    porcentaje NUMBER(5,2) DEFAULT 50.00 NOT NULL,
    fecha_limite_saldo DATE NOT NULL,
    estado VARCHAR2(30) DEFAULT 'PENDIENTE' NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_anticipo_estado CHECK (estado IN ('PENDIENTE', 'PAGADO', 'VENCIDO', 'REEMBOLSADO')),
    CONSTRAINT fk_anticipos_reserva FOREIGN KEY (id_reserva) REFERENCES eventos_reservas(id_reserva) ON DELETE CASCADE
);

-- 8. TABLA: PAGOS (Libro Mayor de Transacciones / Abonos - 1:N)
CREATE TABLE pagos (
    id_pago NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva NUMBER NOT NULL,
    monto NUMBER(10,2) NOT NULL,
    metodo_pago VARCHAR2(30) NOT NULL,
    comision NUMBER(10,2) DEFAULT 0.00 NOT NULL,
    num_operacion VARCHAR2(100),
    tipo_pago VARCHAR2(20) NOT NULL,
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_pago_tipo CHECK (tipo_pago IN ('ANTICIPO', 'SALDO')),
    CONSTRAINT chk_pago_metodo CHECK (metodo_pago IN ('EFECTIVO', 'YAPE', 'PLIN', 'TRANSFERENCIA', 'TARJETA_CREDITO', 'TARJETA_DEBITO')),
    CONSTRAINT fk_pago_reserva FOREIGN KEY (id_reserva) REFERENCES eventos_reservas(id_reserva) ON DELETE CASCADE
);

-- 9. TABLA: CANCIONES (Catálogo del Repertorio Musical)
CREATE TABLE canciones (
    id_cancion NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR2(200) NOT NULL,
    autor VARCHAR2(150),
    genero VARCHAR2(50) NOT NULL,
    duracion_aprox NUMBER(3),
    es_cover CHAR(1) DEFAULT 'N' CHECK (es_cover IN ('S', 'N')),
    disponible CHAR(1) DEFAULT 'S' CHECK (disponible IN ('S', 'N')),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_genero CHECK (genero IN ('Ranchera', 'Cumbia', 'Rock', 'Pop', 'Huapango', 'Bolero', 'Litúrgica'))
);

-- 10. TABLA: RESERVA_CANCIONES (Tabla Asociativa M:N - Setlist / Dedicatorias)
CREATE TABLE reserva_canciones (
    id_reserva_cancion NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva NUMBER NOT NULL,
    id_cancion NUMBER NOT NULL,
    es_dedicatoria CHAR(1) DEFAULT 'N' CHECK (es_dedicatoria IN ('S', 'N')),
    orden NUMBER(3),
    observaciones VARCHAR2(300),
    CONSTRAINT fk_rc_reserva FOREIGN KEY (id_reserva) REFERENCES eventos_reservas(id_reserva) ON DELETE CASCADE,
    CONSTRAINT fk_rc_cancion FOREIGN KEY (id_cancion) REFERENCES canciones(id_cancion)
);

-- 11. TABLA: RESERVA_INTEGRANTES (Tabla Asociativa M:N - Elenco y Asistencia por Evento)
CREATE TABLE reserva_integrantes (
    id_reserva_integrante NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva NUMBER NOT NULL,
    id_integrante NUMBER NOT NULL,
    rol_en_evento VARCHAR2(80),
    asistencia_confirmada CHAR(1) DEFAULT 'S' CHECK (asistencia_confirmada IN ('S', 'N')),
    CONSTRAINT uq_reserva_integrante UNIQUE (id_reserva, id_integrante),
    CONSTRAINT fk_ri_reserva FOREIGN KEY (id_reserva) REFERENCES eventos_reservas(id_reserva) ON DELETE CASCADE,
    CONSTRAINT fk_ri_integrante FOREIGN KEY (id_integrante) REFERENCES integrantes_mariachi(id_integrante)
);
