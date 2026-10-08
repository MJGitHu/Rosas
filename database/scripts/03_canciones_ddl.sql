-- =============================================================================
-- PROYECTO: Rosas de Guadalupe Management System
-- SCRIPT: 03_canciones_ddl.sql
-- DESCRIPCION: Tablas para Repertorio Musical, Asignación de Canciones y Estados
-- AUTOR: Equipo de Desarrollo (Jira Project RS)
-- =============================================================================

-- Tabla: canciones
-- Catálogo de canciones disponibles en el repertorio del mariachi
CREATE TABLE canciones (
    id_cancion       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo           VARCHAR2(200) NOT NULL,
    autor            VARCHAR2(150),
    genero           VARCHAR2(50) NOT NULL, -- Ranchera, Cumbia, Rock, Pop, Huapango, Bolero
    duracion_aprox   NUMBER(3), -- duración aproximada en minutos
    es_cover         CHAR(1) DEFAULT 'N', -- 'S' si es versión de otro artista
    disponible       CHAR(1) DEFAULT 'S', -- 'N' si está deshabilitada
    fecha_registro   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_genero CHECK (genero IN ('Ranchera', 'Cumbia', 'Rock', 'Pop', 'Huapango', 'Bolero', 'Litúrgica')),
    CONSTRAINT chk_es_cover CHECK (es_cover IN ('S', 'N')),
    CONSTRAINT chk_disponible CHECK (disponible IN ('S', 'N'))
);

-- Tabla intermedia: reserva_canciones
-- Asocia las canciones elegidas por el cliente a una reserva específica (relación N:M)
CREATE TABLE reserva_canciones (
    id_reserva_cancion  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva          NUMBER NOT NULL,
    id_cancion          NUMBER NOT NULL,
    es_dedicatoria      CHAR(1) DEFAULT 'N', -- 'S' si el cliente la pidió como dedicatoria
    orden               NUMBER(3), -- orden de interpretación en el setlist
    observaciones       VARCHAR2(300),
    CONSTRAINT fk_rc_reserva FOREIGN KEY (id_reserva) REFERENCES eventos_reservas(id_reserva),
    CONSTRAINT fk_rc_cancion FOREIGN KEY (id_cancion) REFERENCES canciones(id_cancion),
    CONSTRAINT chk_es_dedicatoria CHECK (es_dedicatoria IN ('S', 'N'))
);

-- Tabla catálogo: estados_reserva
-- Normaliza los estados del ciclo de vida de una reserva (evita CHECK hardcodeado)
CREATE TABLE estados_reserva (
    id_estado     NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo        VARCHAR2(30) NOT NULL UNIQUE,
    nombre        VARCHAR2(60) NOT NULL,
    descripcion   VARCHAR2(200),
    es_final      CHAR(1) DEFAULT 'N', -- 'S' si es un estado terminal (ej. CANCELADA, LIQUIDADA)
    orden_flujo   NUMBER(2) NOT NULL
);

-- Datos semilla para estados_reserva
INSERT INTO estados_reserva (codigo, nombre, descripcion, es_final, orden_flujo) VALUES
('COTIZADA', 'Cotizada', 'Servicio cotizado, esperando confirmación del cliente', 'N', 1);
INSERT INTO estados_reserva (codigo, nombre, descripcion, es_final, orden_flujo) VALUES
('ANTICIPO_PAGADO', 'Anticipo Pagado (50%)', 'Anticipo del 50% recibido, reserva separada', 'N', 2);
INSERT INTO estados_reserva (codigo, nombre, descripcion, es_final, orden_flujo) VALUES
('CONFIRMADA', 'Confirmada', 'Reserva confirmada formalmente', 'N', 3);
INSERT INTO estados_reserva (codigo, nombre, descripcion, es_final, orden_flujo) VALUES
('LIQUIDADA', 'Liquidada al 100%', 'Saldo del 50% cancelado, lista para el show', 'S', 4);
INSERT INTO estados_reserva (codigo, nombre, descripcion, es_final, orden_flujo) VALUES
('CANCELADA', 'Cancelada', 'Reserva anulada por el cliente', 'S', 5);

-- Datos semilla: catálogo inicial de canciones (ejemplo del repertorio de Rosas de Guadalupe)
INSERT INTO canciones (titulo, autor, genero, duracion_aprox, es_cover) VALUES
('El Rey', 'José Alfredo Jiménez', 'Ranchera', 3, 'N');
INSERT INTO canciones (titulo, autor, genero, duracion_aprox, es_cover) VALUES
('La Bikina', 'Rubén Fuentes', 'Ranchera', 3, 'N');
INSERT INTO canciones (titulo, autor, genero, duracion_aprox, es_cover) VALUES
('Cielito Lindo', 'Quirino Mendoza', 'Ranchera', 3, 'N');
INSERT INTO canciones (titulo, autor, genero, duracion_aprox, es_cover) VALUES
('Como la Flor', 'Selena', 'Cumbia', 4, 'S');
INSERT INTO canciones (titulo, autor, genero, duracion_aprox, es_cover) VALUES
('La Chona', 'Los Tucanes de Tijuana', 'Cumbia', 3, 'S');
INSERT INTO canciones (titulo, autor, genero, duracion_aprox, es_cover) VALUES
('Imagine', 'John Lennon', 'Rock', 3, 'S');
INSERT INTO canciones (titulo, autor, genero, duracion_aprox, es_cover) VALUES
('Amor Eterno', 'Juan Gabriel', 'Ranchera', 4, 'N');
INSERT INTO canciones (titulo, autor, genero, duracion_aprox, es_cover) VALUES
('Ave María', 'Franz Schubert', 'Litúrgica', 5, 'N');

COMMIT;

-- NOTA ARQUITECTÓNICA:
-- Este script complementa y amplía el esquema base definido en 01_schema_ddl.sql,
-- normalizando los estados del ciclo de vida de una reserva y permitiendo al anfitrión
-- seleccionar las canciones personalizadas y dedicatorias de su serenata.
