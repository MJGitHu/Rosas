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
VALUES ('Serenata Tradicional (45 min)', 'Ideal para sorpresas de cumpleaños, reconciliación o aniversario (7 a 8 canciones)', 6, 2200.00, 'N', 'S');

INSERT INTO formatos_mariachi (nombre_formato, descripcion, num_musicos, precio_base_hora, incluye_equipo_audio, activo)
VALUES ('Show Completo 1 Hora', 'Presentación formal completa de 60 minutos con repertorio clásico y bailable', 6, 2800.00, 'N', 'S');

INSERT INTO formatos_mariachi (nombre_formato, descripcion, num_musicos, precio_base_hora, incluye_equipo_audio, activo)
VALUES ('Show Premium 2 Horas', 'Presentación extendida de 2 horas con animación, dedicatorias y equipo de microfonía', 6, 5200.00, 'S', 'S');

-- 3. ZONAS DE COBERTURA Y RECARGOS LOGÍSTICOS
INSERT INTO zonas_cobertura (nombre_zona, descripcion, recargo_transporte, tiempo_estimado_traslado_min, activo)
VALUES ('Zona Centro / Urbana', 'Cobertura dentro del radio principal de la ciudad sin costo adicional', 0.00, 25, 'S');

INSERT INTO zonas_cobertura (nombre_zona, descripcion, recargo_transporte, tiempo_estimado_traslado_min, activo)
VALUES ('Zona Norte / Periferia Cercana', 'Sectores residenciales y salones norte (hasta 15 km)', 250.00, 45, 'S');

INSERT INTO zonas_cobertura (nombre_zona, descripcion, recargo_transporte, tiempo_estimado_traslado_min, activo)
VALUES ('Zona Sur / Conurbada', 'Sectores residenciales y salones sur (hasta 15 km)', 250.00, 45, 'S');

INSERT INTO zonas_cobertura (nombre_zona, descripcion, recargo_transporte, tiempo_estimado_traslado_min, activo)
VALUES ('Zona Campestre / Foránea', 'Quintas, ranchos y haciendas fuera del perímetro urbano (hasta 35 km)', 600.00, 75, 'S');

COMMIT;
