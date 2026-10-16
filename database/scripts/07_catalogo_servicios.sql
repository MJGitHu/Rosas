-- Actualiza los formatos y la zona sin recargo para la reserva web.
-- Ejecutar una vez en el esquema ROSAS_ADMIN después de las tablas base.

ALTER TABLE eventos_reservas MODIFY (duracion_horas NUMBER(4,2));

DECLARE
    v_columna NUMBER;
BEGIN
    SELECT COUNT(*)
      INTO v_columna
      FROM user_tab_columns
     WHERE table_name = 'EVENTOS_RESERVAS'
       AND column_name = 'METODO_PAGO_PREFERIDO';

    IF v_columna = 0 THEN
        EXECUTE IMMEDIATE q'[
            ALTER TABLE eventos_reservas ADD (
                metodo_pago_preferido VARCHAR2(30) DEFAULT 'TRANSFERENCIA' NOT NULL
                    CHECK (metodo_pago_preferido IN ('TRANSFERENCIA', 'EFECTIVO', 'TARJETA_CREDITO'))
            )
        ]';
    END IF;
END;
/

UPDATE formatos_mariachi
   SET activo = 'N'
 WHERE nombre_formato IN (
     '40 minutos',
     '1 hora',
     '2 horas',
     'Serenata Tradicional (45 min)',
     'Show Completo 1 Hora',
     'Show Premium 2 Horas'
 )
    OR ASCIISTR(nombre_formato) = 'Express d\00C3\00BAo';

MERGE INTO formatos_mariachi destino
USING (
    SELECT 'Mariachi completo' nombre_formato,
           'Tarifas: 30 min S/ 380, 40 min S/ 480, 60 min S/ 680' descripcion,
           6 num_musicos, 680 precio_base_hora FROM dual
    UNION ALL SELECT 'Express 1',
           '5 integrantes. Tarifas: 30 min S/ 340, 40 min S/ 420, 60 min S/ 600',
           5, 600 FROM dual
    UNION ALL SELECT 'Express 2',
           '4 integrantes. Tarifas: 30 min S/ 300, 40 min S/ 360, 60 min S/ 500',
           4, 500 FROM dual
    UNION ALL SELECT CAST(UNISTR('Express d\00FAo') AS VARCHAR2(100)),
           '2 integrantes. Tarifas: 30 min S/ 250, 40 min S/ 280, 60 min S/ 420',
           2, 420 FROM dual
    UNION ALL SELECT 'Solista',
           '1 integrante. Tarifas: 30 min S/ 180, 40 min S/ 220, 60 min S/ 320',
           1, 320 FROM dual
) origen
ON (destino.nombre_formato = origen.nombre_formato)
WHEN MATCHED THEN UPDATE SET
    descripcion = origen.descripcion,
    num_musicos = origen.num_musicos,
    precio_base_hora = origen.precio_base_hora,
    incluye_equipo_audio = 'S',
    activo = 'S'
WHEN NOT MATCHED THEN INSERT (
    nombre_formato, descripcion, num_musicos, precio_base_hora,
    incluye_equipo_audio, activo
) VALUES (
    origen.nombre_formato, origen.descripcion, origen.num_musicos,
    origen.precio_base_hora, 'S', 'S'
);

MERGE INTO zonas_cobertura destino
USING (
    SELECT 'Sin recargo por distancia' nombre_zona,
           'Tarifas actuales sin cargo adicional por ubicación' descripcion
    FROM dual
) origen
ON (destino.nombre_zona = origen.nombre_zona)
WHEN MATCHED THEN UPDATE SET
    descripcion = origen.descripcion,
    recargo_transporte = 0,
    tiempo_estimado_traslado_min = 0,
    activo = 'S'
WHEN NOT MATCHED THEN INSERT (
    nombre_zona, descripcion, recargo_transporte,
    tiempo_estimado_traslado_min, activo
) VALUES (
    origen.nombre_zona, origen.descripcion, 0, 0, 'S'
);

COMMIT;
