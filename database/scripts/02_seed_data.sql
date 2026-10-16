-- =============================================================================
-- PROYECTO: Rosas de Guadalupe Management System
-- SCRIPT: 02_seed_data.sql
-- DESCRIPCION: Datos semilla iniciales (Integrantes, Formatos, Zonas de Cobertura)
-- =============================================================================

-- 1. INTEGRANTES DEL GRUPO MUSICAL FEMENINO (6 Integrantes)
INSERT INTO integrantes_mariachi (nombre_completo, instrumento_rol, es_lider, activo)
VALUES ('Guadalupe Morales', 'Directora Musical / Cantante Principal', 'S', 'S');

INSERT INTO integrantes_mariachi (nombre_completo, instrumento_rol, es_lider, activo)
VALUES ('Sofía Ramírez', 'Segunda Voz y Coros', 'N', 'S');

INSERT INTO integrantes_mariachi (nombre_completo, instrumento_rol, es_lider, activo)
VALUES ('Valeria Torres', 'Primera Trompeta', 'N', 'S');

INSERT INTO integrantes_mariachi (nombre_completo, instrumento_rol, es_lider, activo)
VALUES ('Camila Herrera', 'Segunda Trompeta', 'N', 'S');

INSERT INTO integrantes_mariachi (nombre_completo, instrumento_rol, es_lider, activo)
VALUES ('Daniela Castro', 'Vihuela Mexicana', 'N', 'S');

INSERT INTO integrantes_mariachi (nombre_completo, instrumento_rol, es_lider, activo)
VALUES ('Mariana Domínguez', 'Guitarrón', 'N', 'S');

-- 2. FORMATOS MUSICALES
INSERT INTO formatos_mariachi (nombre_formato, descripcion, num_musicos, precio_base_hora, incluye_equipo_audio, activo)
VALUES ('Mariachi completo', 'Tarifas: 30 min S/ 380, 40 min S/ 480, 60 min S/ 680', 6, 680.00, 'S', 'S');

INSERT INTO formatos_mariachi (nombre_formato, descripcion, num_musicos, precio_base_hora, incluye_equipo_audio, activo)
VALUES ('Express 1', '5 integrantes. Tarifas: 30 min S/ 340, 40 min S/ 420, 60 min S/ 600', 5, 600.00, 'S', 'S');

INSERT INTO formatos_mariachi (nombre_formato, descripcion, num_musicos, precio_base_hora, incluye_equipo_audio, activo)
VALUES ('Express 2', '4 integrantes. Tarifas: 30 min S/ 300, 40 min S/ 360, 60 min S/ 500', 4, 500.00, 'S', 'S');

INSERT INTO formatos_mariachi (nombre_formato, descripcion, num_musicos, precio_base_hora, incluye_equipo_audio, activo)
VALUES (CAST(UNISTR('Express d\00FAo') AS VARCHAR2(100)), '2 integrantes. Tarifas: 30 min S/ 250, 40 min S/ 280, 60 min S/ 420', 2, 420.00, 'S', 'S');

INSERT INTO formatos_mariachi (nombre_formato, descripcion, num_musicos, precio_base_hora, incluye_equipo_audio, activo)
VALUES ('Solista', '1 integrante. Tarifas: 30 min S/ 180, 40 min S/ 220, 60 min S/ 320', 1, 320.00, 'S', 'S');

-- 3. ZONAS DE COBERTURA Y RECARGOS LOGÍSTICOS
INSERT INTO zonas_cobertura (nombre_zona, descripcion, recargo_transporte, tiempo_estimado_traslado_min, activo)
VALUES ('Zona Centro / Urbana', 'Cobertura dentro del radio principal de la ciudad sin costo adicional', 0.00, 25, 'S');

INSERT INTO zonas_cobertura (nombre_zona, descripcion, recargo_transporte, tiempo_estimado_traslado_min, activo)
VALUES ('Sin recargo por distancia', 'Tarifas actuales sin cargo adicional por ubicación', 0.00, 0, 'S');

INSERT INTO zonas_cobertura (nombre_zona, descripcion, recargo_transporte, tiempo_estimado_traslado_min, activo)
VALUES ('Zona Norte / Periferia Cercana', 'Sectores residenciales y salones norte (hasta 15 km)', 250.00, 45, 'S');

INSERT INTO zonas_cobertura (nombre_zona, descripcion, recargo_transporte, tiempo_estimado_traslado_min, activo)
VALUES ('Zona Sur / Conurbada', 'Sectores residenciales y salones sur (hasta 15 km)', 250.00, 45, 'S');

INSERT INTO zonas_cobertura (nombre_zona, descripcion, recargo_transporte, tiempo_estimado_traslado_min, activo)
VALUES ('Zona Campestre / Foránea', 'Quintas, ranchos y haciendas fuera del perímetro urbano (hasta 35 km)', 600.00, 75, 'S');

COMMIT;
