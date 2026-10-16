# Rosas de Guadalupe Management System

Plataforma web integral orientada a modernizar y digitalizar el ciclo comercial, operativo y logístico del grupo musical de mariachi femenino **"Rosas de Guadalupe"** (conformado por 6 integrantes: 2 trompetas, vihuela, guitarrón y 2 cantantes). El sistema automatiza desde la cotización personalizada en tiempo real, validación de cobertura y disponibilidad de agenda, hasta el recaudo financiero escalonado (pago inicial del 50% en concepto de anticipo para reserva de fecha y liquidación del 50% restante al inicio del evento), reduciendo tiempos operativos, previniendo sobreventas de fechas y brindando total transparencia en comisiones e itinerarios.

---

## Gestión del Proyecto

El proyecto se gestiona en Jira bajo la clave **RS**.  
Enlace al tablero: https://upao-team-e2081s7v.atlassian.net/jira/software/projects/RS

---

## Características Principales (Features)

- **Selección de Servicios y Formatos**: Mariachi completo, Express 1, Express 2, Express dúo y Solista; cotización para duraciones de 30, 40 o 60 minutos.
- **Detalles del Evento**: Campo de texto para describir servicios adicionales o solicitudes especiales.
- **Horas Adicionales**: Se inician en 0; cada hora extra cuesta S/ 60 menos que la tarifa de 60 minutos del formato seleccionado.
- **Calculadora en Tiempo Real**: Ajuste por duración de presentación y recálculo automático de honorarios.
- **Validación de Cobertura y Logística**: Cálculo de recargos por desplazamiento según la zona geográfica (Urbana, Periferia Norte/Sur o Campestre/Foránea).
- **Gestión Financiera Escalonada (Regla 50/50)**:
  - Generación obligatoria del **Anticipo del 50%** para confirmar y bloquear la fecha en el calendario oficial.
  - Control del **Saldo Restante del 50%** a ser liquidado al arribo de la agrupación al evento.
- **Desglose de Pasarelas y Comisiones**: Cálculo transparente de comisiones bancarias por pago con tarjeta de crédito/débito (+5%) vs. transferencias SPEI o efectivo (0%).
- **Multi-métodos de Pago**: Integración conceptual y registro para Transferencia/SPEI, Tarjetas Bancarias y Efectivo.
- **Monitoreo de Elenco y Recursos**: Control de la asignación y disponibilidad de las 6 músicas que integran la agrupación.

---

## Tecnologías Utilizadas

- **Frontend**:
  - HTML5 Semántico y Accesible.
  - CSS3 Moderno con arquitectura de variables de diseño, glassmorphism y paleta institucional en tonos borgoña y oro rosa.
  - JavaScript Vanilla (ES6+) modular y reactivo para cálculos y consumo de API REST.
- **Backend**:
  - **Python 3.10+** con **Flask** para una arquitectura ligera y extensible basada en Blueprints.
  - **python-oracledb** en **Modo Thin** (alto rendimiento y portabilidad sin necesidad de binarios pesados del Instant Client).
  - **Flask-CORS** para habilitar la comunicación cross-origin con el cliente web.
  - **python-dotenv** para manejo seguro de credenciales y variables de entorno.
- **Base de Datos**:
  - **Oracle Database** (XE 18c/21c/23ai o Cloud Autonomous Transaction Processing).
  - Extensiones **Oracle Developer Tools for VS Code** y **Oracle SQL Developer Extension** para desarrollo y gestión desde el IDE.

---

## Requisitos Previos

Antes de ejecutar el proyecto localmente, asegúrate de contar con las siguientes herramientas instaladas:

1. **Git**: Para clonación y control de versiones ([git-scm.com](https://git-scm.com/)).
2. **Python 3.10 o superior**: Con el gestor de paquetes `pip` ([python.org](https://www.python.org/)).
3. **Oracle Database**: Instancia local de Oracle Database Express Edition (XE) o acceso a una instancia Oracle Cloud.
4. **Visual Studio Code**: Con las extensiones recomendadas:
   - `Oracle Developer Tools for VS Code` (`Oracle.oracledevtools`)
   - `Python` (`ms-python.python`)
5. **Navegador Web Moderno**: Chrome, Firefox, Edge o Safari.

---

## Instalación y Ejecución

Sigue estos pasos para poner en marcha el proyecto en tu entorno local de desarrollo:

### 1. Clonar el Repositorio

```bash
git clone https://github.com/acarranzao1a-png/rosas_de_guadalupe_mvp.git
cd rosas_de_guadalupe_mvp
```

### 2. Configurar la Base de Datos Oracle

1. Abre Visual Studio Code en la raíz del proyecto:
   ```bash
   code .
   ```
2. Conéctate a tu instancia de Oracle mediante la extensión **Oracle Developer Tools for VS Code** (consulta los detalles en [`database/conexion_oracle.md`](database/conexion_oracle.md)).
3. Ejecuta los scripts SQL en el siguiente orden estricto:
   - `database/scripts/01_schema_ddl.sql` (Crea tablas, secuencias y constraints).
   - `database/scripts/02_seed_data.sql` (Inserta integrantes, formatos y tarifas).

### 3. Configurar el Entorno Backend (Flask)

1. Ingresa a la carpeta del backend:
   ```bash
   cd backend
   ```
2. Crea y activa un entorno virtual de Python:
   - **En Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **En macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Instala las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```
4. Configura las variables de entorno:
   ```bash
   copy .env.example .env   # En Windows
   # cp .env.example .env    # En Linux/macOS
   ```
   *Edita `.env` con las credenciales de tu usuario de Oracle Database (`ORACLE_USER`, `ORACLE_PASSWORD`, `ORACLE_SERVICE_NAME`).*

5. Inicia el servidor de desarrollo de Flask:
   ```bash
   python run.py
   ```
   El servidor estará escuchando en `http://localhost:5000` con la API accesible en `http://localhost:5000/api/health`.

### 4. Ejecutar el Frontend

Dado que el frontend está desacoplado y estructurado con estándares web nativos, puedes abrirlo directamente o a través de un servidor estático:

- **Opción A (Rápida - Live Server en VS Code):**
  - Haz clic derecho sobre `frontend/public/index.html` y selecciona **Open with Live Server**.
- **Opción B (Python HTTP Server):**
  - En una nueva terminal:
    ```bash
    cd frontend/public
    python -m http.server 3000
    ```
  - Abre en tu navegador: `http://localhost:3000`

### Ejecutar pruebas unitarias

```bash
pytest .testing/ -v
```

---

## Estructura del Proyecto

```text
rosas_de_guadalupe_mvp/
│
├── backend/                       # Código fuente de la API REST en Python (Flask)
│   ├── app/
│   │   ├── routes/                # Controladores y Blueprints (cotizaciones, reservas)
│   │   ├── services/              # Lógica de negocio (cálculo de 50% anticipo, recargos y comisiones)
│   │   ├── config.py              # Gestión centralizada de variables de entorno
│   │   ├── db.py                  # Conexión y pooling con python-oracledb (Modo Thin)
│   │   └── __init__.py            # Fábrica de aplicaciones Flask (Application Factory)
│   ├── .env.example               # Plantilla de variables de entorno para desarrollo
│   ├── requirements.txt           # Manifiesto de dependencias de Python
│   └── run.py                     # Punto de entrada para ejecución del servidor
│
├── frontend/                      # Aplicación cliente web interactiva
│   ├── public/
│   │   └── index.html             # Estructura semántica de la plataforma y cotizador
│   └── src/
│       ├── css/
│       │   └── styles.css         # Sistema de diseño con paleta de borgoña y oro
│       └── js/
│           └── app.js             # Lógica reactiva del cotizador y consumo de la API
│
├── database/                      # Gestión de persistencia con Oracle Database
│   ├── scripts/
│   │   ├── 01_schema_ddl.sql      # Definición de tablas relacionales, llaves y constraints
│   │   ├── 02_seed_data.sql       # Catálogos maestros (las 6 integrantes, formatos, zonas)
│   │   └── 03_canciones_ddl.sql   # Repertorio musical, asignación N:M y estados de reserva
│   ├── diagrams/                  # Diagramas entidad-relación (ERD) del modelo de datos
│   └── conexion_oracle.md         # Manual paso a paso para conectar VS Code con Oracle DB
│
├── docs/                          # Documentación técnica y metodológica
│   ├── arquitectura.md            # Diagramas de capas y decisiones de diseño técnico
│   ├── auditoria_repo.md          # Informe exhaustivo de auditoría técnica del repositorio
│   └── metodologia_scrum.md       # Acuerdos de equipo, DoD y lineamientos de trabajo
│
├── .gitignore                     # Exclusiones de Git (entornos virtuales, .env, temporales Oracle)
└── README.md                      # Documento principal de bienvenida y guía del proyecto
```

---

## Equipo de Desarrollo

El proyecto es desarrollado y mantenido por un equipo ágil de 5 profesionales:

| Nombre | Rol / Especialidad | Responsabilidad Principal |
| :--- | :--- | :--- |
| **[Nombre del Integrante 1]** <!-- TODO: reemplazar con nombre real --> | Tech Lead & Backend Developer | Arquitectura Flask, API REST y revisión de código |
| **[Nombre del Integrante 2]** <!-- TODO: reemplazar con nombre real --> | Database Administrator / Oracle Specialist | Modelado relacional, optimización PL/SQL y DDLs |
| **[Nombre del Integrante 3]** <!-- TODO: reemplazar con nombre real --> | Frontend Developer | Maquetación UI/UX, reactividad y experiencia de usuario |
| **[Nombre del Integrante 4]** <!-- TODO: reemplazar con nombre real --> | Full-Stack Developer | Integración de pasarelas, cálculo de anticipos y servicios |
| **[Nombre del Integrante 5]** <!-- TODO: reemplazar con nombre real --> | QA & Scrum Master | Automatización de pruebas, aseguramiento de DoD y ceremonias |

---

## Documentación Adicional y Gestión Ágil (Jira)

La planificación, priorización y seguimiento de este proyecto se gestionan en **Jira**:

- **Clave del Proyecto en Jira**: `RS` (*Rosas de Guadalupe Software*).
- **Marco de Trabajo**: **Scrum** con iteraciones (Sprints) de **2 semanas**.
- **Capacidad y Velocidad de Referencia**: **20 Story Points (SP)** por Sprint para el equipo de 5 desarrolladores.
- **Artefactos del Proyecto**:
  - El *Product Backlog*, las *Historias de Usuario (User Stories)* con sus criterios de aceptación y los tableros activos se encuentran centralizados en el espacio de Jira del proyecto.
  - Consulta [`docs/metodologia_scrum.md`](docs/metodologia_scrum.md) para conocer las políticas de Definition of Done (DoD), ramas de Git y acuerdos de trabajo.
