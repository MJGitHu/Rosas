-- =============================================================================
-- PROYECTO: Rosas de Guadalupe Management System
-- SCRIPT: 06_reserva_detalles_ddl_seed.sql
-- DESCRIPCION: Integración relacional completa:
--              1. Foreign Key entre EVENTOS_RESERVAS y ESTADOS_RESERVA
--              2. Tabla asociativa RESERVA_INTEGRANTES (M:N entre Reservas e Integrantes)
--              3. Semillas de repertorio (RESERVA_CANCIONES) e integrantes asignados
-- =============================================================================

-- 1. FOREIGN KEY: EVENTOS_RESERVAS -> ESTADOS_RESERVA
-- Permite validar y relacionar formalmente el estado de cada reserva
BEGIN
    EXECUTE IMMEDIATE 'ALTER TABLE eventos_reservas ADD CONSTRAINT fk_reserva_estado FOREIGN KEY (estado_reserva) REFERENCES estados_reserva(codigo)';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -2275 AND SQLCODE != -2260 THEN -- Ignorar si ya existe
            NULL;
        END IF;
END;
/

-- 2. TABLA ASOCIATIVA: RESERVA_INTEGRANTES
-- Conecta EVENTOS_RESERVAS con INTEGRANTES_MARIACHI para asignación de elenco y asistencia
BEGIN
    EXECUTE IMMEDIATE '
    CREATE TABLE reserva_integrantes (
        id_reserva_integrante NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        id_reserva NUMBER NOT NULL,
        id_integrante NUMBER NOT NULL,
        rol_en_evento VARCHAR2(80),
        asistencia_confirmada CHAR(1) DEFAULT ''S'' CHECK (asistencia_confirmada IN (''S'', ''N'')),
        CONSTRAINT uq_reserva_integrante UNIQUE (id_reserva, id_integrante),
        CONSTRAINT fk_ri_reserva FOREIGN KEY (id_reserva) REFERENCES eventos_reservas(id_reserva) ON DELETE CASCADE,
        CONSTRAINT fk_ri_integrante FOREIGN KEY (id_integrante) REFERENCES integrantes_mariachi(id_integrante)
    )';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -955 THEN -- Ignorar si la tabla ya existe (ORA-00955)
            RAISE;
        END IF;
END;
/

-- 3. DATOS SEMILLA: ASIGNACIÓN DE ELENCO MUSICAL A LAS RESERVAS DE PRUEBA
-- Asegura que todas las reservas tengan a las 6 músicas del mariachi asignadas
MERGE INTO reserva_integrantes dest
USING (
    SELECT r.id_reserva, i.id_integrante, i.instrumento_rol as rol
    FROM eventos_reservas r
    CROSS JOIN integrantes_mariachi i
    WHERE r.codigo_reserva IN ('RS-2026-001', 'RS-2026-002', 'RS-2026-003')
) src
ON (dest.id_reserva = src.id_reserva AND dest.id_integrante = src.id_integrante)
WHEN NOT MATCHED THEN
    INSERT (id_reserva, id_integrante, rol_en_evento, asistencia_confirmada)
    VALUES (src.id_reserva, src.id_integrante, src.rol, 'S');

-- 4. DATOS SEMILLA: REPERTORIO Y DEDICATORIAS EN RESERVA_CANCIONES
MERGE INTO reserva_canciones dest
USING (
    SELECT 
        (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-001') as id_reserva,
        1 as id_cancion, 'S' as es_dedicatoria, 1 as orden, 'Dedicada al agasajado por su cumpleaños' as obs FROM dual
    UNION ALL SELECT (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-001'), 3, 'N', 2, 'Canción tradicional de apertura' FROM dual
    UNION ALL SELECT (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-001'), 7, 'S', 3, 'Momento emotivo familiar' FROM dual
    UNION ALL SELECT (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-002'), 2, 'S', 1, 'Serenata especial de aniversario' FROM dual
    UNION ALL SELECT (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-002'), 5, 'N', 2, 'Cierre bailable con La Chona' FROM dual
    UNION ALL SELECT (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-003'), 8, 'S', 1, 'Entrada de la misa y ceremonia litúrgica' FROM dual
    UNION ALL SELECT (SELECT id_reserva FROM eventos_reservas WHERE codigo_reserva = 'RS-2026-003'), 1, 'N', 2, 'Brindis de gala' FROM dual
) src
ON (dest.id_reserva = src.id_reserva AND dest.id_cancion = src.id_cancion)
WHEN NOT MATCHED THEN
    INSERT (id_reserva, id_cancion, es_dedicatoria, orden, observaciones)
    VALUES (src.id_reserva, src.id_cancion, src.es_dedicatoria, src.orden, src.obs);

COMMIT;
