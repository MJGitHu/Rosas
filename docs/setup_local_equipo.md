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

CREATE USER ROSAS_ADMIN IDENTIFIED BY "Mariachi2026!";
GRANT CONNECT, RESOURCE, DBA TO ROSAS_ADMIN;
ALTER USER ROSAS_ADMIN QUOTA UNLIMITED ON USERS;

COMMIT;
EXIT;
```

3. **Verifica la conexión del nuevo usuario:**
```powershell
sqlplus ROSAS_ADMIN/Mariachi2026!@localhost:1521/XEPDB1
```
Si ves el prompt `SQL>`, escribe `EXIT;` para continuar.

---

## Paso 4: Ejecutar los 5 Scripts SQL en Orden

Ubícate en la raíz del repositorio clonado en tu terminal (PowerShell) y ejecuta los 5 scripts en orden secuencial:

```powershell
# Asegúrate de estar en la carpeta raíz del proyecto
cd \ruta\a\rosas-de-guadalupe-rs

# 1. Esquema base DDL (clientes, zonas, formatos, reservas, elenco)
sqlplus ROSAS_ADMIN/Mariachi2026!@localhost:1521/XEPDB1 @database/scripts/01_schema_ddl.sql

# 2. Catálogos semilla (zonas de cobertura, formatos mariachi, 6 integrantes)
sqlplus ROSAS_ADMIN/Mariachi2026!@localhost:1521/XEPDB1 @database/scripts/02_seed_data.sql

# 3. Repertorio musical y estados de flujo (canciones, estados_reserva)
sqlplus ROSAS_ADMIN/Mariachi2026!@localhost:1521/XEPDB1 @database/scripts/03_canciones_ddl.sql

# 4. Modelo normalizado de pagos y anticipos 1:1 (RS-137)
sqlplus ROSAS_ADMIN/Mariachi2026!@localhost:1521/XEPDB1 @database/scripts/04_pagos_ddl.sql

# 5. Datos de prueba con 3 reservas, anticipos y pagos en Soles (S/)
sqlplus ROSAS_ADMIN/Mariachi2026!@localhost:1521/XEPDB1 @database/scripts/05_pagos_seed.sql
```

> **Verificación Rápida:** Puedes consultar el conteo de tablas ejecutando:
> ```powershell
> sqlplus ROSAS_ADMIN/Mariachi2026!@localhost:1521/XEPDB1
> ```
> ```sql
> SELECT table_name FROM user_tables ORDER BY table_name;
> SELECT 'reservas: ' || COUNT(*) FROM eventos_reservas;
> SELECT 'pagos: ' || COUNT(*) FROM pagos;
> EXIT;
> ```
> Debes ver **10 tablas** creadas y 3 reservas registradas.

---

## Paso 5: Configurar `backend/.env`

El archivo `.env` contiene las variables de entorno locales de conexión (está protegido en `.gitignore` para no subir secretos al repositorio).

1. Crea tu archivo local a partir de la plantilla:
```powershell
Copy-Item backend/.env.example backend/.env
```

2. Verifica que `backend/.env` contenga la siguiente configuración:
```env
ORACLE_USER=ROSAS_ADMIN
ORACLE_PASSWORD=Mariachi2026!
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=XEPDB1
ANTICIPO_PERCENTAGE=0.50
COMISION_TARJETA_PERCENTAGE=0.05
FLASK_DEBUG=1
PORT=5000
SECRET_KEY=cambia-esta-clave-en-produccion
```

---

## Paso 6: Levantar el Backend Flask y Verificar Conexión

1. Instala las dependencias del backend:
```powershell
cd backend
py -m pip install -r requirements.txt
```
*(Las librerías principales son: `flask`, `flask-cors`, `oracledb`, `python-dotenv`).*

2. Inicia el servidor Flask:
```powershell
py run.py
```
Verás un mensaje en consola indicando:
```text
[DB] Conexión establecida con Oracle Database en localhost:1521/XEPDB1
Servidor backend ejecutándose en http://localhost:5000
```

3. **Verificación de Salud (Health Check):**
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

## Paso 7: Abrir y Probar el Frontend

1. Abre el archivo `frontend/public/index.html` en Google Chrome o Microsoft Edge (puedes hacer doble clic en el archivo o usar la extensión *Live Server* de VS Code).
2. Verifica en la esquina superior derecha que el badge indique:
   * **`Backend: Conectado (Flask)`** (en verde/dorado).
3. Prueba la calculadora interactiva de presupuestos:
   * Todos los montos deben figurar en **Soles (S/)** (ejemplo: Subtotal `S/ 2,800.00`, Anticipo 50% `S/ 1,400.00`).
   * Al seleccionar **Tarjeta Crédito / Débito**, debe aplicar exactamente el **5% de comisión** sobre el anticipo (+S/ 70.00).
   * Al seleccionar **Transferencia Bancaria** o **Efectivo**, la comisión debe ser `S/ 0.00`.

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
