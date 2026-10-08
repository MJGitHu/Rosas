# Auditoría Completa del Repositorio - Rosas de Guadalupe Management System

**Fecha de Auditoría:** 7 de Octubre de 2026  
**Auditor Técnico:** Tech Lead & Arquitecto de Software  
**Proyecto:** Rosas de Guadalupe Management System (Jira: `RS`)  
**Repositorio GitHub:** `acarranzao1a-png/rosas_de_guadalupe_mvp`  
**Objetivo:** Mapeo exhaustivo del estado actual del repositorio, dependencias, numeración de scripts SQL, modelos de datos, endpoints del backend y cliente frontend, para prevenir colisiones de numeración y duplicidad de lógica.

---

## PARTE 1: Estructura Completa de Carpetas y Archivos

Inventario detallado de todos los archivos del repositorio (excluyendo directorios de control de versiones `.git/`, temporales de entorno `.kilo/`, compilados `__pycache__/`, `*.pyc` y cachés locales).

| Ruta | Líneas | Estado Git | Propósito Técnico |
|---|:---:|:---:|---|
| `.gitignore` | 119 | Modificado (`M`) | Reglas de exclusión para Python, Oracle, IDEs, caches y `.testing/`. |
| `README.md` | 199 | Modificado (`M`) | Documentación principal, enlace a Jira `RS`, setup y diagramas. |
| `backend/.env.example` | 18 | Versionado (`Tracked`) | Plantilla de variables de entorno para desarrollo local. |
| `backend/requirements.txt` | 10 | Versionado (`Tracked`) | Manifiesto de dependencias de Python (Flask, oracledb, etc.). |
| `backend/run.py` | 7 | Versionado (`Tracked`) | Punto de entrada para arranque del servidor HTTP local de Flask. |
| `backend/app/__init__.py` | 32 | Versionado (`Tracked`) | Application Factory de Flask, configuración de CORS y Blueprints. |
| `backend/app/config.py` | 26 | Modificado (`M`) | Configuración del sistema, conexión Oracle y constantes de negocio. |
| `backend/app/db.py` | 46 | Versionado (`Tracked`) | Pool de conexiones a Oracle Database con `oracledb` en Modo Thin. |
| `backend/app/routes/__init__.py` | 1 | Versionado (`Tracked`) | Inicializador del paquete de rutas de Flask. |
| `backend/app/routes/cotizaciones.py` | 19 | Versionado (`Tracked`) | Endpoint REST para cotización reactiva de eventos. |
| `backend/app/routes/reservas.py` | 49 | Versionado (`Tracked`) | Endpoint REST para consulta de reservas desde Oracle DB. |
| `backend/app/services/__init__.py` | 0 | — | Directorio de servicios de lógica de negocio. |
| `backend/app/services/calculator_service.py` | 47 | Modificado (`M`) | Lógica de cálculo financiero: anticipo 50%, saldo 50% y comisión 5%. |
| `database/conexion_oracle.md` | 87 | Versionado (`Tracked`) | Manual de conexión para VS Code con Oracle Developer Tools y EZConnect. |
| `database/diagrams/README.md` | 8 | Versionado (`Tracked`) | Descripción conceptual del modelo relacional. |
| `database/scripts/01_schema_ddl.sql` | 91 | Versionado (`Tracked`) | DDL de tablas iniciales (clientes, zonas, formatos, reservas, pagos, elenco). |
| `database/scripts/02_seed_data.sql` | 50 | Versionado (`Tracked`) | Datos semilla de las 6 músicas, 3 formatos y 4 zonas de cobertura. |
| `database/scripts/03_canciones_ddl.sql` | 85 | Nuevo sin commitear (`Untracked - U`) | DDL para repertorio musical, reservas-canciones y catálogo de estados. |
| `docs/arquitectura.md` | 34 | Versionado (`Tracked`) | Documento de arquitectura técnica por capas y decisiones ADR. |
| `docs/auditoria_repo.md` | 268 | Nuevo sin commitear (`Untracked - U`) | Informe de auditoría inicial previa. |
| `docs/metodologia_scrum.md` | 21 | Versionado (`Tracked`) | Marco ágil de trabajo Scrum en Jira `RS`, sprints 2 semanas y 20 SP. |
| `frontend/public/index.html` | 184 | Versionado (`Tracked`) | Vista web del cotizador, desglose financiero 50/50 y elenco musical. |
| `frontend/src/css/styles.css` | 373 | Versionado (`Tracked`) | Sistema de diseño institucional en borgoña, oro rosa y glassmorphism. |
| `frontend/src/js/app.js` | 123 | Versionado (`Tracked`) | Lógica interactiva cliente y consumo de API con fallback offline. |

*Nota sobre suites de verificación:* La suite de pruebas unitarias y verificación con `pytest` se encuentra alojada de forma aislada en `.testing/` ([`test_calculator.py`](file:///d:/rosas-de-guadalupe-rs/.testing/test_calculator.py)), excluida en `.gitignore` para no interferir en el árbol productivo.

---

## PARTE 2: Análisis de Cada Archivo SQL

### Archivo: `database/scripts/01_schema_ddl.sql`
- **Propósito:** Crea el esquema de base de datos relacional inicial para Oracle Database con secuencias de identidad, llaves foráneas y tipos nativos.
- **Tablas:**
  1. `clientes`
  2. `zonas_cobertura`
  3. `formatos_mariachi`
  4. `eventos_reservas`
  5. `pagos` (definición preliminar)
  6. `integrantes_mariachi`
- **Datos semilla:** No contiene sentencias `INSERT`.
- **Constraints definidos:**
  - **PKs:** `id_cliente`, `id_zona`, `id_formato`, `id_reserva`, `id_pago`, `id_integrante` (todas con `GENERATED ALWAYS AS IDENTITY`).
  - **UNIQUE:** `uq_cliente_email (email)`, `codigo_reserva (codigo_reserva)`.
  - **FKs:**
    - `fk_reserva_cliente`: `eventos_reservas(id_cliente) -> clientes(id_cliente)`
    - `fk_reserva_formato`: `eventos_reservas(id_formato) -> formatos_mariachi(id_formato)`
    - `fk_reserva_zona`: `eventos_reservas(id_zona) -> zonas_cobertura(id_zona)`
    - `fk_pago_reserva`: `pagos(id_reserva) -> eventos_reservas(id_reserva)`
  - **CHECKs:**
    - `zonas_cobertura.activo IN ('S', 'N')`
    - `formatos_mariachi.incluye_equipo_audio IN ('S', 'N')`
    - `formatos_mariachi.activo IN ('S', 'N')`
    - `eventos_reservas.estado_reserva IN ('COTIZADA', 'ANTICIPO_PAGADO', 'CONFIRMADA', 'LIQUIDADA', 'CANCELADA')`
    - `pagos.tipo_pago IN ('ANTICIPO_50', 'LIQUIDACION_50', 'TOTAL_100')`
    - `pagos.metodo_pago IN ('TRANSFERENCIA', 'EFECTIVO', 'TARJETA_CREDITO', 'TARJETA_DEBITO', 'MERCADOPAGO')`
    - `pagos.estado_pago IN ('PENDIENTE', 'COMPLETADO', 'RECHAZADO')`
    - `integrantes_mariachi.es_lider IN ('S', 'N')`
    - `integrantes_mariachi.activo IN ('S', 'N')`
- **Referenciado en Python:** Sí. [`backend/app/routes/reservas.py`](file:///d:/rosas-de-guadalupe-rs/backend/app/routes/reservas.py#L14) realiza una consulta `SELECT` uniendo `eventos_reservas` y `clientes`.

---

### Archivo: `database/scripts/02_seed_data.sql`
- **Propósito:** Carga inicial de datos maestros de catálogos para permitir la cotización y visualización del grupo musical.
- **Tablas afectadas:**
  1. `integrantes_mariachi`
  2. `formatos_mariachi`
  3. `zonas_cobertura`
- **Registros insertados:** **13 registros**:
  - 6 integrantes oficiales (Guadalupe Morales, Sofía Ramírez, Valeria Torres, Camila Herrera, Daniela Castro, Mariana Domínguez).
  - 3 formatos (Serenata Tradicional $2,200, Show 1 Hora $2,800, Show Premium 2 Horas $5,200).
  - 4 zonas logísticas (Centro $0, Norte $250, Sur $250, Campestre $600).
- **Referenciado en Python:** Indirectamente. Los valores tarifarios coinciden con los valores por defecto del cotizador en [`backend/app/routes/cotizaciones.py`](file:///d:/rosas-de-guadalupe-rs/backend/app/routes/cotizaciones.py#L9) y del cliente web [`frontend/public/index.html`](file:///d:/rosas-de-guadalupe-rs/frontend/public/index.html).

---

### Archivo: `database/scripts/03_canciones_ddl.sql`
- **Propósito:** Modela el repertorio musical del mariachi, permite la asociación personalizada de temas y dedicatorias por evento, y normaliza los estados del flujo de reservas.
- **Tablas:**
  1. `canciones`
  2. `reserva_canciones` (intermedia N:M)
  3. `estados_reserva` (catálogo maestro)
- **Datos semilla:** Sí, incluye **13 registros insertados**:
  - 5 estados del flujo en `estados_reserva` (`COTIZADA`, `ANTICIPO_PAGADO`, `CONFIRMADA`, `LIQUIDADA`, `CANCELADA`).
  - 8 canciones emblemáticas en `canciones` ('El Rey', 'La Bikina', 'Cielito Lindo', 'Como la Flor', 'La Chona', 'Imagine', 'Amor Eterno', 'Ave María').
- **Constraints definidos:**
  - **PKs:** `id_cancion`, `id_reserva_cancion`, `id_estado` (`GENERATED ALWAYS AS IDENTITY`).
  - **UNIQUE:** `estados_reserva.codigo`.
  - **FKs:**
    - `fk_rc_reserva`: `reserva_canciones(id_reserva) -> eventos_reservas(id_reserva)`
    - `fk_rc_cancion`: `reserva_canciones(id_cancion) -> canciones(id_cancion)`
  - **CHECKs:**
    - `canciones.genero IN ('Ranchera', 'Cumbia', 'Rock', 'Pop', 'Huapango', 'Bolero', 'Litúrgica')`
    - `canciones.es_cover IN ('S', 'N')`
    - `canciones.disponible IN ('S', 'N')`
    - `reserva_canciones.es_dedicatoria IN ('S', 'N')`
    - `estados_reserva.es_final IN ('S', 'N')`
- **Referenciado en Python:** Aún no. Está preparado para la futura implementación de los endpoints de repertorio en Flask.

---

## PARTE 3: ¿Qué Tablas Existen y Cuáles se Necesitan?

Inventario comparativo entre las tablas requeridas por el negocio y las existentes en los scripts `.sql`:

| Tabla Necesaria | ¿Existe? | ¿En qué script? | Observación |
|---|:---:|---|---|
| **clientes** | **Sí** | `01_schema_ddl.sql` | Completa. Almacena anfitriones, teléfonos, correos y referencias. |
| **zonas_cobertura** | **Sí** | `01_schema_ddl.sql` | Completa. Catálogo con recargos logísticos y tiempos de traslado. |
| **formatos_mariachi** | **Sí** | `01_schema_ddl.sql` | Completa. Define horas, tarifas base y dotación instrumental. |
| **eventos_reservas** | **Sí** | `01_schema_ddl.sql` | Completa. Contrato de servicio, fecha, horas, montos y desglose 50/50. |
| **pagos** | **Sí (Parcial)** | `01_schema_ddl.sql` | **Requiere refactorización**. La versión en `01` es preliminar; la subtarea RS-137 requiere columnas explícitas: `num_operacion`, `comision` y `tipo_pago ('ANTICIPO', 'SALDO')`. |
| **integrantes_mariachi** | **Sí** | `01_schema_ddl.sql` | Completa. Registro de las 6 músicas y líder de la agrupación. |
| **canciones** | **Sí** | `03_canciones_ddl.sql` | Completa. Repertorio musical con autor, género y duración. |
| **reserva_canciones** | **Sí** | `03_canciones_ddl.sql` | Completa. Tabla asociativa N:M con dedicatorias y orden de setlist. |
| **estados_reserva** | **Sí** | `03_canciones_ddl.sql` | Completa. Catálogo normalizado para la máquina de estados. |
| **anticipos** | **NO** | *Pendiente (RS-137)* | **Faltante crítica**. No existe como tabla independiente. Se necesita para modelar la proyección financiera 1:1, fecha límite de saldo y estado del anticipo. |
| **tarifas** | **NO** | *No implementada* | **Opcional/Secundaria**. Las tarifas están desnormalizadas dentro de `formatos_mariachi.precio_base_hora` y `zonas_cobertura.recargo_transporte`. |

### Resumen de Tablas:
- **Tablas existentes en el diseño:** **9 tablas** (`clientes`, `zonas_cobertura`, `formatos_mariachi`, `eventos_reservas`, `pagos`, `integrantes_mariachi`, `canciones`, `reserva_canciones`, `estados_reserva`).
- **Tablas faltantes:** **2 tablas** (`anticipos` y `tarifas`).
- **Tablas faltantes críticas:**
  1. **`anticipos`:** Esencial para soportar la relación `1:1` con `eventos_reservas` que exige la subtarea Jira RS-137.

---

## PARTE 4: Análisis de la Numeración de Scripts

Revisión de los archivos en `database/scripts/`:

- `01_schema_ddl.sql` → **Usado** (Tracked en Git)
- `02_seed_data.sql` → **Usado** (Tracked en Git)
- `03_canciones_ddl.sql` → **Usado** (Untracked en Git)

### Diagnóstico de Colisiones:
- **Huecos en la secuencia:** Ninguno (la secuencia actual es 01, 02, 03).
- **Riesgo de Duplicidad Detectado:** La subtarea Jira **RS-137** solicita explícitamente generar un archivo con el nombre `03_pagos_ddl.sql`. Si se utilizara ese nombre, se crearía una **duplicidad de prefijo `03_`** con `03_canciones_ddl.sql`.
- **Siguiente número disponible en la secuencia:** **`04`**.

### Recomendación de Numeración para RS-137:
Para mantener un orden de ejecución lineal impecable en Oracle SQL Developer, se recomienda adoptar una de las dos siguientes alternativas:
- **Opción A (Recomendada):** Asignar a la subtarea RS-137 los números **`04_pagos_ddl.sql`** y **`05_pagos_seed.sql`**.
- **Opción B:** Renombrar `03_canciones_ddl.sql` a `05_canciones_ddl.sql` para que pagos quede como 03 y 04.

---

## PARTE 5: Análisis del Código Python

Inventario de módulos en `backend/`:

| Ruta | Propósito | Endpoints / Rutas que Expone | Importa de |
|---|---|---|---|
| `backend/run.py` | Entrada de ejecución local del servidor HTTP. | — | `app.create_app`, `app.config.Config` |
| `backend/app/__init__.py` | Fábrica de la aplicación Flask, CORS y pool DB. | `GET /api/health` | `flask.Flask`, `flask_cors.CORS`, `app.config.Config`, `app.db`, `app.routes.*` |
| `backend/app/db.py` | Pooling y ciclo de vida de conexión Oracle. | — | `oracledb`, `app.config.Config` |
| `backend/app/config.py` | Centralización de variables de entorno y reglas. | — | `os`, `dotenv.load_dotenv` |
| `backend/app/routes/cotizaciones.py` | Endpoint para cálculo dinámico de presupuestos. | `POST /api/cotizaciones/calcular` | `flask.Blueprint`, `flask.request`, `flask.jsonify`, `app.services.calculator_service` |
| `backend/app/routes/reservas.py` | Consulta y listado de reservas con SQL a Oracle. | `GET /api/reservas/` | `flask.Blueprint`, `flask.request`, `flask.jsonify`, `app.db.get_db_connection` |
| `backend/app/services/calculator_service.py` | Servicio con reglas financieras del negocio. | — | `app.config.Config` (con fallback de seguridad) |

### Resumen de Endpoints:
- **Endpoints implementados:** **3 endpoints**:
  1. `GET /api/health` → Chequeo de operatividad de la API.
  2. `POST /api/cotizaciones/calcular` → Cálculo del presupuesto, anticipo 50%, saldo 50% y comisión 5% tarjeta.
  3. `GET /api/reservas/` → Listado de reservas desde Oracle DB (o mock de contingencia).

- **Endpoints faltantes para completar el ciclo del MVP:** **8 endpoints**:
  1. `POST /api/reservas/` → Creación de nueva reserva en estado `COTIZADA`.
  2. `GET /api/reservas/<id>` → Consulta de detalle de una reserva específica.
  3. `PUT /api/reservas/<id>/estado` → Transición de estados (`COTIZADA` → `ANTICIPO_PAGADO` → `CONFIRMADA` → `LIQUIDADA`).
  4. `POST /api/reservas/<id>/pagos` → Registro de pagos de anticipo (50%) o liquidación (50%).
  5. `GET /api/reservas/<id>/pagos` → Historial de pagos y comisiones de una reserva.
  6. `GET /api/formatos/` → Consulta dinámica del catálogo de formatos desde Oracle DB.
  7. `GET /api/zonas/` → Consulta dinámica de zonas de cobertura y recargos logísticos.
  8. `GET /api/canciones/` → Consulta del repertorio para selección de canciones por el anfitrión.

---

## PARTE 6: Análisis del Frontend

Inventario de la aplicación cliente en `frontend/`:

| Ruta | Propósito | ¿Usa fetch a la API? | ¿Qué endpoints consume? |
|---|---|:---:|---|
| `frontend/public/index.html` | Estructura web del cotizador, desglose financiero 50/50 y tarjetas del elenco musical. | No (markup semántico) | — |
| `frontend/src/css/styles.css` | Sistema de diseño institucional, responsive design, variables de color y glassmorphism. | No (estilos visuales) | — |
| `frontend/src/js/app.js` | Controlador de interfaz, cálculo reactivo en vivo y comunicación HTTP asíncrona. | **Sí** | `GET http://localhost:5000/api/health`<br>`POST http://localhost:5000/api/cotizaciones/calcular` |

### Diagnóstico de Conexión y Funcionalidad:
- **¿El frontend está conectado al backend?** **SÍ**.
  - Al iniciar, consulta `GET /api/health` para encender el badge verde `"Backend: Conectado (Flask)"` en la cabecera.
  - Al cambiar cualquier parámetro del formulario (formato, horas, zona o método de pago), envía una petición `POST /api/cotizaciones/calcular` al backend. Si el backend está apagado, cuenta con un algoritmo de respaldo local para no interrumpir la experiencia de usuario.
- **Funcionalidades implementadas en el Frontend:**
  - Selector de formatos musicales y recálculo automático de duración.
  - Selector de zonas de cobertura con recargo de logística.
  - Selector de método de pago con advertencia de comisión por tarjeta (+5%).
  - Desglose financiero detallado: Subtotal, Recargo de zona, Presupuesto Total, Anticipo obligatorio del 50%, Comisión por pasarela y Saldo restante del 50% al evento.
  - Tarjetas informativas de las 6 músicas integrantes de la agrupación.
  - *Funcionalidad pendiente:* Modal o pantalla secundaria para captura de datos del anfitrión y dirección física al presionar *"Continuar con la Reserva"*.

---

## PARTE 7: Resumen Ejecutivo

| Aspecto | Valor |
|---|:---:|
| **Total de archivos auditados** | **23** |
| **Total de scripts SQL en `database/scripts/`** | **3** |
| **Último número de script SQL utilizado** | **`03`** (`03_canciones_ddl.sql`) |
| **Siguiente número correlativo disponible** | **`04`** |
| **Total de tablas actualmente en el diseño** | **9 tablas** |
| **Tablas faltantes para el modelo completo** | **2 tablas** (`anticipos` y `tarifas`) |
| **Endpoints REST implementados** | **3** |
| **Endpoints REST faltantes para el MVP** | **8** |
| **Frontend conectado al backend** | **Sí** (con fallback offline resiliente) |
| **Archivos modificados sin commitear** | 4 (`.gitignore`, `README.md`, `config.py`, `calculator_service.py`) |
| **Archivos nuevos untracked** | 2 (`03_canciones_ddl.sql`, `docs/auditoria_repo.md`) |
