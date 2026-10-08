# Auditoría del Repositorio - Rosas de Guadalupe

**Fecha de Auditoría:** 7 de Octubre de 2026  
**Auditor Técnico:** Tech Lead & Software Project Auditor  
**Proyecto:** Rosas de Guadalupe Management System  
**Repositorio GitHub:** [acarranzao1a-png/rosas_de_guadalupe_mvp](https://github.com/acarranzao1a-png/rosas_de_guadalupe_mvp)  
**Marco de Trabajo:** Scrum (Proyecto Jira `RS` - Sprints de 2 semanas - Velocidad: 20 SP)

---

## 1. Estructura de Carpetas

A continuación se detalla la estructura jerárquica de directorios del proyecto y el propósito técnico de cada uno:

- **`/` (Raíz del proyecto):** Contiene los archivos de metadatos, control de versiones ([`.gitignore`](file:///d:/rosas-de-guadalupe-rs/.gitignore)) y la documentación introductoria ([`README.md`](file:///d:/rosas-de-guadalupe-rs/README.md)).
- **`/backend`:** Alberga la aplicación servidora construida sobre Python y Flask.
  - **`/backend/app`:** Código fuente principal bajo el patrón *Application Factory*.
    - **`/backend/app/routes`:** Controladores REST (Blueprints) que exponen los endpoints de la API.
    - **`/backend/app/services`:** Capa de lógica de negocio pura, reglas de cotización y cálculos financieros independientes del transporte HTTP.
- **`/database`:** Contiene los artefactos de persistencia para Oracle Database.
  - **`/database/scripts`:** Scripts SQL versionados para la creación de esquemas (DDL) y datos semilla iniciales (DML).
  - **`/database/diagrams`:** Documentación y artefactos de modelado entidad-relación (ERD).
- **`/frontend`:** Aplicación cliente web desacoplada para anfitriones y cotización.
  - **`/frontend/public`:** Archivos estáticos accesibles directamente por el navegador (`index.html`).
  - **`/frontend/src`:** Recursos fuente organizados.
    - **`/frontend/src/css`:** Hojas de estilo y tokens de diseño visual.
    - **`/frontend/src/js`:** Lógica de interfaz de usuario y cliente de consumo de la API REST.
- **`/docs`:** Documentación técnica, decisiones de arquitectura (ADRs), especificaciones del marco ágil Scrum y reportes de auditoría.

---

## 2. Inventario de Archivos

### 2.1 Backend

| Ruta | Propósito | Lógica Negocio | Config | Docs | Líneas | Acción |
|---|---|:---:|:---:|:---:|:---:|---|
| `backend/run.py` | Punto de entrada para arrancar el servidor HTTP local de Flask en el puerto configurado. | No | Sí | No | 7 | Conservar |
| `backend/requirements.txt` | Declaración de dependencias de Python y versiones fijadas del ecosistema de backend. | No | Sí | No | 10 | Revisar |
| `backend/.env.example` | Plantilla pública con nombres de variables de entorno requeridas para desarrollo local. | No | Sí | Sí | 18 | Revisar |
| `backend/app/__init__.py` | Fábrica de la aplicación Flask (`create_app`), configuración de CORS y registro de Blueprints. | No | Sí | No | 32 | Conservar |
| `backend/app/config.py` | Clase centralizadora de variables de entorno y constantes de la aplicación con `python-dotenv`. | No | Sí | No | 25 | Revisar |
| `backend/app/db.py` | Gestión del pool de conexiones con Oracle Database mediante `oracledb` en Modo Thin. | No | Sí | Sí | 46 | Conservar |
| `backend/app/routes/__init__.py` | Módulo inicializador del paquete de rutas de Flask. | No | No | No | 1 | Conservar |
| `backend/app/routes/cotizaciones.py` | Endpoint REST (`POST /api/cotizaciones/calcular`) para recibir parámetros y calcular presupuestos. | Sí | No | No | 19 | Revisar |
| `backend/app/routes/reservas.py` | Endpoint REST (`GET /api/reservas/`) para listar eventos y reservas consultando a Oracle DB. | Sí | No | No | 49 | Revisar |
| `backend/app/services/calculator_service.py` | Reglas de negocio del cotizador: subtotal, anticipo 50%, saldo 50% y comisiones bancarias. | Sí | No | Sí | 35 | Revisar |

### 2.2 Base de Datos

| Ruta | Propósito | Tipo (DDL/DML/Docs) | Líneas | Acción |
|---|---|:---:|:---:|---|
| `database/scripts/01_schema_ddl.sql` | Definición de tablas maestras, llaves foráneas y constraints relacionales en Oracle. | DDL | 91 | Revisar |
| `database/scripts/02_seed_data.sql` | Población inicial de integrantes (las 6 músicas), formatos del show y zonas de cobertura. | DML | 35 | Conservar |
| `database/diagrams/README.md` | Resumen textual de las relaciones del modelo de datos ERD. | Docs | 8 | Revisar |
| `database/conexion_oracle.md` | Guía de configuración de extensiones de VS Code, cadenas de conexión EZConnect y troubleshooting. | Docs | 87 | Conservar |

### 2.3 Frontend

| Ruta | Propósito | Tipo (HTML/CSS/JS) | Líneas | Acción |
|---|---|:---:|:---:|---|
| `frontend/public/index.html` | Estructura web del cotizador interactivo, desglose 50/50 y fichas del mariachi femenino. | HTML | 184 | Conservar |
| `frontend/src/css/styles.css` | Sistema de diseño con paleta de borgoña, oro rosa, componentes glassmorphism y responsive design. | CSS | 373 | Conservar |
| `frontend/src/js/app.js` | Controlador cliente que ejecuta recálculos dinámicos en vivo y consume los endpoints de Flask. | JS | 123 | Revisar |

### 2.4 Documentación

| Ruta | Propósito | Líneas | Acción |
|---|---|:---:|---|
| `docs/arquitectura.md` | Especificación de capas del sistema, flujo de información y decisiones de arquitectura (ADRs). | 34 | Conservar |
| `docs/metodologia_scrum.md` | Definición del marco de trabajo Scrum, cadencia de sprints (2 semanas / 20 SP), eventos y DoD. | 21 | Conservar |

### 2.5 Configuración Raíz

| Ruta | Propósito | Líneas | Acción |
|---|---|:---:|---|
| `README.md` | Documentación maestra del repositorio, propuesta de valor, tecnologías, guía de instalación y equipo. | 154 | Revisar |
| `.gitignore` | Reglas de exclusión de Git para Python, Oracle Database, frontend, entornos locales e IDEs. | 91 | Revisar |

---

## 3. Análisis de Dependencias

### Contenido de `backend/requirements.txt`:
```text
Flask==3.0.3
Flask-Cors==4.0.1
oracledb==2.2.1
python-dotenv==1.0.1
marshmallow==3.21.3
pytest==8.2.2
```

### Versiones de Python Recomendadas:
- **Recomendada:** **Python 3.11** o **Python 3.12**.
- **Mínima soportada:** **Python 3.10**.
- **Justificación técnica:** `oracledb 2.2.1` y `Flask 3.0.3` ofrecen soporte optimizado para Python 3.11/3.12, beneficiándose de las mejoras del intérprete en velocidad de ejecución y manejo de asincronía.

### Evaluación de Librerías Utilizadas:
1. **`Flask==3.0.3`**: Microframework maduro, de baja sobrecarga y excelente rendimiento para arquitecturas modulares orientadas a APIs REST.
2. **`Flask-Cors==4.0.1`**: Imprescindible para evitar bloqueos por políticas CORS al consumir la API desde el cliente estático en puertos separados (ej. `localhost:3000` vs `localhost:5000`).
3. **`oracledb==2.2.1`**: Librería oficial de Oracle. Su principal ventaja arquitectónica es que opera en **Modo Thin** por defecto, eliminando la necesidad de instalar el binario de Oracle Instant Client (de más de 200 MB) en las máquinas de los 5 desarrolladores del equipo.
4. **`python-dotenv==1.0.1`**: Carga segura de variables de entorno para evitar *hardcoding* de credenciales.
5. **`marshmallow==3.21.3`**: Incluida en dependencias, pero **aún no está siendo utilizada en el código actual**. Se debe implementar para validar los JSON de entrada.
6. **`pytest==8.2.2`**: Incluida para pruebas automatizadas, pero actualmente la carpeta `backend/tests/` no ha sido creada.

---

## 4. Análisis del Código de Negocio

### 4.1 `backend/app/services/calculator_service.py`
- **Funcionalidad que implementa:**
  Calcula el subtotal musical (`precio_base_hora * duracion`), recargo de logística según la zona, monto total presupuestado, el **anticipo del 50%**, el **saldo del 50%** y la comisión por pasarela de pagos con tarjeta de crédito/débito.
- **¿Está completa o es un esqueleto?**
  La función matemática básica está completa y es funcional. Sin embargo, se encuentra desacoplada de la clase de configuración `Config`, lo que provoca que no lea los valores dinámicos definidos en el entorno.
- **¿Es correcta según las reglas del negocio (anticipo 50%, comisión 5% tarjeta)?**
  - **Anticipo 50%:** **CORRECTA**. Se calcula exactamente el `50%` del monto total (`anticipo = round(monto_total * 0.50, 2)`).
  - **Comisión por tarjeta:** **INCORRECTA**. En la línea 21 tiene codificado `0.035` (3.5%):
    ```python
    if metodo_pago in ["TARJETA_CREDITO", "TARJETA_DEBITO"]:
        comision_tarjeta = round(anticipo * 0.035, 2)  # <-- Requiere cambiar a 5% (0.05)
    ```
    La regla de negocio estipula una **comisión del 5%** para cobros con tarjeta.
- **¿Se puede conservar o debe reescribirse?**
  **Debe modificarse**. No requiere reescritura total: basta con parametrizar la comisión al **5%** (`0.05`), importar la tasa desde `app.config.Config` y añadir pruebas unitarias.

### 4.2 `backend/app/routes/cotizaciones.py`
- **Funcionalidad que implementa:**
  Expone el endpoint `POST /api/cotizaciones/calcular`, extrae los parámetros del cuerpo JSON (`precio_base_hora`, `duracion_horas`, `recargo_zona`, `metodo_pago`) e invoca a `calculator_service.py`.
- **¿Está completa o es un esqueleto?**
  **Esqueleto funcional**. Funciona para llamadas válidas pero carece de:
  - Validación de tipos y rangos de datos (un valor negativo o una cadena no numérica provoca un error `HTTP 500` no controlado).
  - Consulta directa de precios a la base de datos (confía ciegamente en el `precio_base_hora` que envía el cliente desde el frontend, lo cual representa un riesgo de seguridad de precios si el cliente es manipulado).
- **¿Es correcta según las reglas del negocio?**
  Parcialmente correcta: delega en el servicio, por lo que arrastra la comisión incorrecta del 3.5%.
- **¿Se puede conservar o debe reescribirse?**
  **Debe revisarse y modificarse**. Se recomienda implementar un esquema de validación con `marshmallow` y permitir que el precio base sea validado contra la tabla `formatos_mariachi` de Oracle DB.

### 4.3 `backend/app/routes/reservas.py`
- **Funcionalidad que implementa:**
  Expone el endpoint `GET /api/reservas/` que realiza una consulta SQL cruzada (`JOIN`) entre `eventos_reservas` y `clientes` en Oracle DB, con un fallback mock si la base de datos no está disponible.
- **¿Está completa o es un esqueleto?**
  **Esqueleto incompleto (MVP solo lectura)**. No implementa los verbos transaccionales críticos:
  - `POST /api/reservas/` para crear reservas.
  - `PUT /api/reservas/<id>` para transiciones de estado (`COTIZADA` -> `ANTICIPO_PAGADO` -> `CONFIRMADA` -> `LIQUIDADA`).
  - `POST /api/reservas/<id>/pagos` para registrar transacciones de anticipo y liquidación.
- **¿Es correcta según las reglas del negocio?**
  Solo cubre la consulta básica de reservas existentes; no implementa aún el flujo completo de contratación ni la validación de colisiones de agenda para la misma fecha y hora.
- **¿Se puede conservar o debe reescribirse?**
  **Debe conservarse como base y ampliarse** para completar el ciclo CRUD y transaccional exigido en los siguientes sprints del proyecto `RS`.

---

## 5. Análisis de la Base de Datos

### ¿El script `01_schema_ddl.sql` crea las tablas correctas?
El script crea actualmente **6 tablas relacionales coherentes** con integridad referencial:
1. `clientes`
2. `zonas_cobertura`
3. `formatos_mariachi`
4. `eventos_reservas`
5. `pagos`
6. `integrantes_mariachi`

### ¿Incluye las tablas requeridas por la auditoría?
| Tabla Solicitada | ¿Presente en el DDL? | Diagnóstico Técnico |
|---|:---:|---|
| **clientes** | **SÍ** | Implementada como `clientes` con restricciones de correo único y datos de contacto. |
| **reservas** | **SÍ** | Implementada como `eventos_reservas`, incluye relación con cliente, zona, formato y montos 50/50. |
| **pagos** | **SÍ** | Implementada como `pagos`, con llaves foráneas hacia la reserva y desglose de comisiones. |
| **anticipos** | **NO (Embebida)** | **No existe como tabla independiente**. Se modeló dentro de `eventos_reservas` (`anticipo_requerido`, `saldo_pendiente`) y en `pagos` con `tipo_pago = 'ANTICIPO_50'`. |
| **estados_reserva** | **NO (Check)** | **No existe como tabla catálogo**. Se implementó como una restricción de validación `CHECK (estado_reserva IN ('COTIZADA', 'ANTICIPO_PAGADO', 'CONFIRMADA', 'LIQUIDADA', 'CANCELADA'))`. |
| **formatos** | **SÍ** | Implementada como `formatos_mariachi` con tarifa base por hora y cantidad de músicas. |
| **tarifas** | **NO (Embebida)** | **No existe como tabla independiente**. Las tarifas están desnormalizadas dentro de `formatos_mariachi.precio_base_hora` y `zonas_cobertura.recargo_transporte`. |
| **canciones** | **NO** | **Ausente por completo**. No existe tabla de canciones, repertorio mariachi ni canciones seleccionadas para la serenata. |

### ¿Usa sintaxis de Oracle (VARCHAR2, NUMBER, SEQUENCE)?
- **Tipos de datos:** **SÍ**. Utiliza rigurosamente tipos específicos de Oracle: `VARCHAR2(100)`, `NUMBER(10,2)`, `CHAR(1)`, `DATE` y `TIMESTAMP`.
- **Secuencias / Autoincrementables:** Utiliza la sintaxis estándar moderna de Oracle 12c/18c/19c/21c/23ai:
  ```sql
  id_cliente NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
  ```
  Esto crea secuencias nativas de Oracle bajo el estándar ANSI/Oracle moderno sin requerir triggers `BEFORE INSERT`.

### ¿Falta alguna tabla?
Para cumplir con una arquitectura de dominio completa, faltan:
1. **`canciones` / `repertorio_mariachi`**: Catálogo de canciones disponibles (título, autor, género: ranchera, huapango, bolero, etc.).
2. **`reserva_canciones`**: Tabla intermedia (N:M) para asociar las canciones elegidas por el anfitrión para su evento.
3. **`estados_reserva`**: Tabla catálogo para normalizar estados si se requiere permitir nuevos estados dinámicos sin alterar el esquema (`ALTER TABLE`).
4. **`tarifas_temporada` (Opcional):** Para gestionar precios especiales en fechas de alta demanda (10 de Mayo, 12 de Diciembre, Navidad).

---

## 6. Archivos que NO deben estar en el repo

Tras la inspección del sistema de archivos local y el historial de Git, se detectaron los siguientes elementos que **deben eliminarse o excluirse explícitamente**:

1. **Directorio `.kilo/` (Presente en disco):**
   - **Diagnóstico:** Carpeta generada automáticamente por herramientas de entorno de ejecución con copias de trabajo (`worktrees`).
   - **Acción:** No debe subirse al repositorio remoto. Debe añadirse a [`.gitignore`](file:///d:/rosas-de-guadalupe-rs/.gitignore) y ser purgada del disco.
2. **Directorios `__pycache__/` y archivos `*.cpython-*.pyc` (Presentes en disco):**
   - **Diagnóstico:** Bytecode compilado de Python generado durante verificaciones locales.
   - **Acción:** Aunque actualmente están cubiertos por `.gitignore` y no están commiteados en Git, deben eliminarse periódicamente del disco local para evitar suciedad en el entorno.
3. **Archivos `.env` con credenciales reales (Riesgo preventivo):**
   - **Diagnóstico:** Actualmente **NO** hay archivos `.env` en el repositorio (solo existe `.env.example`, lo cual es correcto).
   - **Acción:** Mantener la política de seguridad estricta para que ningún desarrollador cometa un archivo `.env` con contraseñas de producción o de Oracle Cloud Wallet.
4. **Archivos temporales de red de Oracle (`sqlnet.log`, `*.trc`, `*.trm`):**
   - **Diagnóstico:** Logs que genera el cliente Oracle al fallar una conexión.
   - **Acción:** Mantener su exclusión activa en `.gitignore`.

---

## 7. Recomendaciones Finales

### Qué conservar tal cual:
- **`backend/run.py`** y **`backend/app/__init__.py`**: Arquitectura base limpia de Flask con soporte para CORS y Blueprints.
- **`backend/app/db.py`**: Conexión a Oracle Database en Modo Thin con pool de conexiones gestionado.
- **`database/conexion_oracle.md`**: Guía clara y detallada de conexión para VS Code y SQL Developer.
- **`database/scripts/02_seed_data.sql`**: Catálogo de las 6 integrantes del mariachi femenino y datos semilla.
- **`frontend/src/css/styles.css`**: Sistema de diseño visual bien logrado, accesible y acorde a la identidad institucional de "Rosas de Guadalupe".
- **`docs/arquitectura.md`** y **`docs/metodologia_scrum.md`**: Documentación clara para el gobierno ágil del equipo en Jira.

### Qué modificar:
1. **`backend/app/services/calculator_service.py`**:
   - Modificar la tasa de comisión de tarjeta del **3.5% al 5.0%** (`0.05`).
   - Conectar la lectura de la comisión a `app.config.Config` en lugar de mantenerla *hardcoded*.
2. **`frontend/src/js/app.js`**:
   - Ajustar el fallback de cálculo en el frontend para reflejar la comisión del **5%** en pagos con tarjeta.
3. **`backend/app/routes/cotizaciones.py`**:
   - Integrar validación de entradas con `marshmallow` para evitar fallos por datos no válidos.
4. **`backend/.gitignore`**:
   - Añadir la regla `.kilo/` para asegurar que ningún artefacto interno de worktrees se agregue inadvertidamente a Git.
5. **`database/scripts/01_schema_ddl.sql`**:
   - Evaluar si las entidades `canciones` y `tarifas` deben crearse antes de cerrar el Sprint 1.

### Qué eliminar:
- El directorio temporal `.kilo/` del disco local.
- Archivos residuales `*.pyc` y directorios `__pycache__/` generados en el árbol de trabajo.

### Qué crear (Faltantes Críticos):
1. **Script DDL para Repertorio Musical (`03_canciones_ddl.sql`):**
   - Tablas `canciones` y `reserva_canciones`.
2. **Endpoints transaccionales en `backend/app/routes/reservas.py`:**
   - Implementar `POST /api/reservas/` (creación de reserva en estado `COTIZADA`) y `POST /api/reservas/<id>/pagos` (registro de anticipo del 50%).
3. **Módulo de Pruebas Unitarias (`backend/tests/`):**
   - Crear `test_calculator.py` para probar automáticamente la regla del anticipo del 50% y la comisión del 5% con `pytest`.

---

## 8. Estado del README.md

| Criterio Evaluado | Estado | Observaciones del Auditor |
|---|:---:|---|
| **¿Está en español?** | **CUMPLE** | Redactado íntegramente en español neutro, técnico y formal. |
| **¿Incluye Título del Proyecto?** | **CUMPLE** | *"Rosas de Guadalupe Management System"*. |
| **¿Incluye Descripción comercial y de valor?** | **CUMPLE** | Detalla el propósito para el grupo de mariachi femenino (6 integrantes: 2 trompetas, vihuela, guitarrón, 2 cantantes) y la regla financiera 50/50. |
| **¿Incluye Características Principales (Features)?** | **CUMPLE** | Lista exhaustiva de funcionalidades (formatos, duración, zonas, 50% anticipo, 50% saldo, comisión por tarjeta). |
| **¿Incluye Tecnologías Utilizadas?** | **CUMPLE** | Especifica Frontend, Backend (Flask, python-oracledb Thin Mode) y Oracle Database. |
| **¿Incluye Requisitos Previos e Instalación?** | **CUMPLE** | Comandos paso a paso en bloques de código para clonación, entorno virtual `venv`, `pip`, `.env` y ejecución. |
| **¿Incluye Estructura del Proyecto?** | **CUMPLE** | Diagrama de árbol de carpetas con descripción de cada directorio. |
| **¿Incluye Sección del Equipo (5 integrantes)?** | **CUMPLE (Con Placeholders)** | Tabla estructurada con roles para los 5 integrantes del equipo, lista para asignar nombres definitivos. |

### ¿Qué le falta al `README.md`?
1. **Nombres definitivos del equipo:** Reemplazar los textos de marcador de posición `[Nombre del Integrante X]` por los nombres reales de los 5 desarrolladores.
2. **Enlace al tablero de Jira:** Agregar la URL directa al proyecto Jira `RS` de la organización para acceso rápido del equipo.
3. **Instrucciones para pruebas:** Añadir una subsección indicando cómo ejecutar las pruebas unitarias con `pytest`.
4. **Insignias de estado (Badges):** Incorporar badges visuales (versión de Python `3.11+`, licencia, estado de build o CI/CD).
