# Guía de Instalación y Replicación Local para el Equipo
## Rosas de Guadalupe Management System (Proyecto Jira: `RS`)

Esta guía paso a paso permite a cualquier integrante del equipo configurar y levantar el entorno completo de desarrollo (Base de Datos Oracle XE 21c, Backend en Flask y Frontend en Soles `S/`) en su máquina local con Windows para pruebas y la exposición técnica.

---

## Prerrequisitos en la Máquina Local
* Sistema Operativo: **Windows 10 o Windows 11 (64-bit)**.
* **Python 3.10+** instalado (con el launcher `py` o agregado al `PATH`).
* **Git** instalado.
* Terminal: **PowerShell** (ejecutar como Administrador para servicios).

---

## Paso 1: Instalar Oracle Database XE 21c en Windows

1. Descarga el instalador oficial de **Oracle Database 21c Express Edition (XE)** para Windows:
   * [Oracle Database XE Downloads](https://www.oracle.com/database/technologies/xe-downloads.html)
2. Descomprime el archivo zip y ejecuta `setup.exe` como Administrador.
3. Durante el asistente de instalación:
   * **Contraseña de SYS / SYSTEM:** Define una contraseña que recuerdes (ejemplo: `Admin2026!` o la que prefieras).
   * **Parámetros por defecto generados:**
     * Contenedor CDB (Base de datos raíz): `XE`
     * Pluggable Database (PDB donde vive la app): `XEPDB1`
     * Puerto del Listener: `1521`
4. Deja que la instalación finalice y reinicia la máquina si el asistente lo solicita.

---

## Paso 2: Verificar e Iniciar los Servicios de Oracle

Abre una consola de **PowerShell como Administrador** y comprueba que el servicio principal y el Listener de Oracle estén en ejecución:

```powershell
# 1. Consultar estado de los servicios
Get-Service Oracle*

# 2. Si no están en estado 'Running', iniciarlos con:
Start-Service OracleServiceXE
Start-Service OracleOraDB21Home1TNSListener
```

Para verificar que la base de datos conectable `XEPDB1` esté abierta en modo lectura/escritura:

```powershell
sqlplus / as sysdba
```
Dentro de SQL*Plus ejecuta:
```sql
ALTER PLUGGABLE DATABASE XEPDB1 OPEN;
EXIT;
```

---

## Paso 3: Crear el Usuario `ROSAS_ADMIN` en XEPDB1

Oracle 21c utiliza arquitectura multitenant. Nuestra aplicación no debe residir en la raíz (`XE`), sino en la base de datos conectable **`XEPDB1`**.

1. Conéctate como administrador desde PowerShell:
```powershell
sqlplus / as sysdba
```

2. Copia y pega este bloque completo en SQL*Plus:
```sql
ALTER SESSION SET CONTAINER = XEPDB1;

CREATE USER ROSAS_ADMIN IDENTIFIED BY "TU_CONTRASENA_LOCAL";
GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE, CREATE TRIGGER TO ROSAS_ADMIN;
ALTER USER ROSAS_ADMIN QUOTA UNLIMITED ON USERS;

COMMIT;
EXIT;
```

3. **Verifica la conexión del nuevo usuario:**
```powershell
sqlplus ROSAS_ADMIN@localhost:1521/XEPDB1
```
SQL*Plus solicitará la contraseña de forma interactiva. Si ves el prompt `SQL>`, escribe `EXIT;` para continuar.

---

---

## Paso 4: Ejecutar los Scripts SQL para Crear la Base de Datos

Tienes dos formas sencillas de ejecutar los scripts: **Opción A (por terminal con SQL\*Plus)** o **Opción B (desde Oracle SQL Developer)**.

### Opción A: Por Terminal (PowerShell)

Ubícate en la raíz del repositorio clonado y ejecuta los scripts en orden secuencial:

```powershell
Set-Location \ruta\a\rosas_de_guadalupe_mvp
sqlplus ROSAS_ADMIN@localhost:1521/XEPDB1
```

SQL*Plus solicitará la contraseña sin mostrarla. En el prompt `SQL>`, ejecuta cada script y confirma que termine correctamente antes de pasar al siguiente:

```sql
@database/scripts/01_schema_ddl.sql
@database/scripts/02_seed_data.sql
@database/scripts/03_canciones_ddl.sql
@database/scripts/04_pagos_ddl.sql
@database/scripts/05_pagos_seed.sql
@database/scripts/06_reserva_detalles_ddl_seed.sql
@database/scripts/07_catalogo_servicios.sql
@database/scripts/08_mercadopago_intents.sql
```

---

### Opción B: Desde Oracle SQL Developer (Interfaz Gráfica)

Puedes usar tanto el software independiente **Oracle SQL Developer Desktop** como la **Extensión oficial de SQL Developer para VS Code**:

> 💡 **Tip para VS Code, VSCodium o Forks (Cursor, Windsurf):**  
> Si usas VS Code estándar, puedes instalarla con:  
> `code --install-extension Oracle.sql-developer`  
> Si usas un fork de VS Code (como VSCodium o Cursor) donde el Marketplace de Microsoft no está disponible:  
> 1. Descarga el archivo VSIX oficial de Oracle: [sql-developer-win32-x64-26.3.0.vsix](https://download.oracle.com/otn_software/java/sqldeveloper/sql-developer-win32-x64-26.3.0.vsix)  
> 2. Instálalo desde el menú de Extensiones (`...` &rarr; *Install from VSIX...*) o por terminal con `code --install-extension <archivo>.vsix`.

#### 1. Crear la Conexión en SQL Developer
1. Abre **Oracle SQL Developer** (o el panel de Oracle en VS Code).
2. En el panel izquierdo **Conexiones**, haz clic en el ícono verde **`+` (Nueva Conexión)**.
3. Rellena exactamente los siguientes campos:

| Campo en SQL Developer | Valor Exacto | Notas Importantes |
| :--- | :--- | :--- |
| **Name (Nombre de Conexión)** | `Rosas de Guadalupe - Local` | O el nombre que prefieras |
| **Authentication Type** | `Default` | - |
| **Username (Usuario)** | `ROSAS_ADMIN` | El usuario creado en el Paso 3 |
| **Password (Contraseña)** | La definida localmente; no incluirla en el repositorio| Marcar casilla *"Guardar Contraseña"* |
| **Connection Type** | `Basic` | - |
| **Role** | `default` | **NO** usar SYSDBA |
| **Hostname** | `localhost` | O `127.0.0.1` |
| **Port** | `1521` | Puerto estándar del Listener |
| **Service Name** ⚠️ | `XEPDB1` | **¡CRÍTICO!** Selecciona **Service Name** (NO seleccionar SID) |

> ⚠️ **ERROR COMÚN A EVITAR (`ORA-12505`):**  
> Si dejas marcada la opción **SID** con `xe`, la conexión fallará o te conectará a la raíz del contenedor donde el usuario no existe. Asegúrate de marcar el radio button **Service Name** y escribir **`XEPDB1`**.

4. Haz clic en el botón **Probar (Test)** abajo a la izquierda. En el cuadro de estado inferior izquierdo debe decir: **`Estado: Correcto` (Success)**.
5. Haz clic en **Guardar** y luego en **Conectar**.

#### 2. Cargar y Ejecutar los Scripts en SQL Developer
Tienes dos opciones para dejar la base de datos 100% actualizada:

* **Método Rápido (Todo en uno):**  
  1. En SQL Developer, menú **Archivo &rarr; Abrir...** (`Ctrl + O`).
  2. Selecciona `database/diagrams/esquema_completo.sql`.
  3. Asegúrate de que en la esquina superior derecha de la hoja SQL esté seleccionada la conexión `Rosas de Guadalupe - Local`.
  4. Presiona la tecla **`F5`** (o clic en el ícono **Ejecutar Script** con la hoja y el triángulo verde).
  5. Luego abre y ejecuta `database/scripts/02_seed_data.sql`, `05_pagos_seed.sql` y `06_reserva_detalles_ddl_seed.sql` para tener los datos de prueba.

* **Método Paso a Paso:**  
  Abre y ejecuta con **`F5`** los scripts de la carpeta `database/scripts/` en orden:
  1. `01_schema_ddl.sql`
  2. `02_seed_data.sql`
  3. `03_canciones_ddl.sql`
  4. `04_pagos_ddl.sql`
  5. `05_pagos_seed.sql`
  6. `06_reserva_detalles_ddl_seed.sql`
  7. `07_catalogo_servicios.sql`
  8. `08_mercadopago_intents.sql`

#### 3. Verificar las Tablas Creadas
En el panel izquierdo, despliega la conexión **`Rosas de Guadalupe - Local` &rarr; `Tablas (Tables)`** y haz clic en el ícono de **Refrescar (`↻`)**.

Debes ver las **11 tablas del sistema**:
1. `ANTICIPOS`
2. `CANCIONES`
3. `CLIENTES`
4. `ESTADOS_RESERVA`
5. `EVENTOS_RESERVAS`
6. `FORMATOS_MARIACHI`
7. `INTEGRANTES_MARIACHI`
8. `PAGOS`
9. `RESERVA_CANCIONES`
10. `RESERVA_INTEGRANTES`
11. `ZONAS_COBERTURA`
12. `MERCADOPAGO_INTENTS`

*(Nota: Si ves tablas que empiezan por `ANNOTATIONS_%$`, son tablas internas de metadatos de Oracle 21c; no forman parte del sistema y se pueden ignorar).*

---

## Paso 5: Configurar `backend/.env`

El archivo `.env` contiene las variables de entorno locales de conexión (está protegido en `.gitignore` para no subir secretos al repositorio).

1. Crea `backend/.env` si todavía no existe y ábrelo para editar:
```powershell
if (-not (Test-Path backend\.env)) { New-Item -Path backend\.env -ItemType File | Out-Null }
code backend\.env
```

2. Agrega la configuración de conexión. Reemplaza el marcador por la contraseña que elegiste localmente; no la compartas ni la subas al repositorio:
```env
ORACLE_USER=ROSAS_ADMIN
ORACLE_PASSWORD="TU_CONTRASENA_LOCAL"
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=XEPDB1
ANTICIPO_PERCENTAGE=0.50
COMISION_TARJETA_PERCENTAGE=0.05
FLASK_DEBUG=1
PORT=5000
SECRET_KEY=PEGA_AQUI_UNA_CLAVE_ALEATORIA_DE_64_CARACTERES
ADMIN_USERNAME=administradora
ADMIN_PASSWORD_HASH=PEGA_AQUI_EL_HASH_GENERADO
SESSION_COOKIE_SECURE=0
MERCADOPAGO_ACCESS_TOKEN=PEGA_AQUI_EL_TOKEN_DEL_ENTORNO_ELEGIDO
MERCADOPAGO_WEBHOOK_URL=https://TU_DOMINIO/api/webhooks/mercadopago
MERCADOPAGO_WEBHOOK_SECRET=PEGA_AQUI_LA_CLAVE_SECRETA_DEL_WEBHOOK
FLASK_ENV=development
```

En el panel de Mercado Pago, configura el evento **Pagos** para la URL HTTPS indicada y copia su clave secreta a `MERCADOPAGO_WEBHOOK_SECRET`. El endpoint `/api/webhooks/mercadopago` acepta `POST`; las notificaciones `merchant_order` se reconocen y responden `200`, mientras que la reserva solo se crea tras verificar un pago aprobado. La URL debe apuntar al backend público. El retorno del checkout usa el mismo dominio de esa URL y la ruta raíz de la aplicación. No utilices `localhost` como webhook. También se conserva `/api/pagos/webhook` por compatibilidad.

El token productivo crea cobros reales: la opción **Prueba** también inicia un cobro real de S/ 1.00 cuando se configura un token productivo. Para validar sin cobrar, configura credenciales y eventos de prueba de Mercado Pago.

La clave secreta y el hash deben ser únicos por entorno. No pongas la contraseña de administración en `.env`: guarda solo su hash. En el Paso 6 se generan ambos valores; copia cada resultado en su variable correspondiente antes de iniciar Flask. La cuenta configurada en `ADMIN_USERNAME` es la única cuenta administrativa: no existe registro ni creación de usuarios desde la web. En desarrollo local por HTTP, deja `SESSION_COOKIE_SECURE=0`; para publicar bajo HTTPS, usa `SESSION_COOKIE_SECURE=1` y `FLASK_DEBUG=0`.

Para usar un túnel cambiante como localtunnel durante desarrollo, configura `FLASK_ENV=development` y reinicia Flask. El login administrativo aceptará dinámicamente el origen HTTPS si coincide con `X-Forwarded-Host` y `X-Forwarded-Proto` que envía el túnel; no se habilita CORS para todos los orígenes. Esta excepción solo se aplica al login en desarrollo; no uses `FLASK_ENV=development` en producción.

---

## Paso 6: Levantar el Backend Flask y Verificar Conexión

1. Instala las dependencias del backend:
```powershell
cd backend
py -m pip install -r requirements.txt
```
*(Las librerías principales son: `flask`, `flask-cors`, `oracledb`, `python-dotenv`).*

2. Genera los valores de seguridad. El segundo comando solicita la contraseña sin mostrarla:
```powershell
py -c "import secrets; print(secrets.token_hex(32))"
py -c "from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass('Contraseña de administración: ')))"
```
Copia los resultados a `SECRET_KEY` y `ADMIN_PASSWORD_HASH` en `.env`. No compartas estos valores.

3. Inicia el servidor Flask:
```powershell
py run.py
```
Verás un mensaje en consola indicando:
```text
[DB] Conexión establecida con Oracle Database en localhost:1521/XEPDB1
Servidor backend ejecutándose en http://localhost:5000
```

4. **Verificación de Salud (Health Check):**
Abre una nueva ventana de PowerShell o tu navegador y consulta:
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method GET
```
**Respuesta esperada:**
```json
{
  "app": "Rosas de Guadalupe Management System API",
  "database": "connected",
  "status": "online",
  "version": "1.0.0"
}
```

---

## Paso 7: Abrir y Probar la Aplicación

1. Abre `http://localhost:5000` en Google Chrome o Microsoft Edge. Flask sirve el frontend y la API desde el mismo origen para mantener protegida la sesión administrativa; no abras el HTML directamente ni uses Live Server para este flujo.
2. Verifica en la esquina superior derecha que el badge indique:
   * **`Backend: Conectado (Flask)`** (en verde/dorado).
3. Para entrar a administración, pulsa **Sesión de administración** e inicia sesión con `ADMIN_USERNAME` y la contraseña cuyo hash configuraste. El calendario muestra únicamente contratos leídos de Oracle; si Oracle no está disponible, se informa el error y no se muestran datos ficticios.
4. Prueba la calculadora interactiva de presupuestos:
   * Los montos deben figurar en **Soles (S/)** y mostrar el anticipo del 50% para Mercado Pago.
   * Al seleccionar **Prueba**, el total del contrato y el pago de hoy deben ser `S/ 1.00`, con saldo `S/ 0.00`.
   * Para probar Checkout Pro, usa credenciales de prueba y un webhook HTTPS público. No hagas pruebas con el token productivo, porque genera cobros reales.

---

## Preguntas Frecuentes y Solución de Problemas

### 1. Error `ORA-12541: TNS:no listener`
* El servicio del listener está detenido.
* **Solución:** Ejecuta en PowerShell como Administrador: `Start-Service OracleOraDB21Home1TNSListener` o `lsnrctl start`.

### 2. Error `ORA-01017: invalid username/password`
* La contraseña en Oracle distingue mayúsculas y minúsculas.
* **Solución:** Comprueba que estás usando `"Mariachi2026!"` (con comillas si se ejecuta en DDL de creación) y el usuario en mayúsculas `ROSAS_ADMIN`.

### 3. Error `ORA-12514: TNS:listener does not currently know of service requested`
* El servicio `XEPDB1` aún no se ha registrado con el listener o la PDB está cerrada.
* **Solución:** Entra a `sqlplus / as sysdba` y ejecuta `ALTER PLUGGABLE DATABASE XEPDB1 OPEN;`. Espera 30 segundos y reintenta.

### 4. Diagrama ER para Presentación
* En la carpeta `database/diagrams/` cuentas con:
  * **`diagrama_er.html`**: Visualizador interactivo en el navegador con zoom y tema institucional.
  * **`diagrama_er.md`**: Diagrama Mermaid y cardinalidades del modelo.
  * **`esquema_completo.sql`**: DDL completo de las 10 tablas.
