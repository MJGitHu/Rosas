# Guía de Conexión y Gestión de Oracle Database en VS Code

Esta guía detalla el procedimiento para configurar, conectar y ejecutar scripts de **Oracle Database** directamente desde **Visual Studio Code**, tanto para la administración de la base de datos como para la integración con el backend en Python (Flask).

---

## 1. Extensiones Recomendadas para VS Code / Forks

Para trabajar de forma productiva con Oracle Database en VS Code o sus forks (VSCodium, Cursor, Windsurf, etc.), tienes dos métodos de instalación:

### Método A: Instalación Automática desde el Marketplace Oficial
Si utilizas el VS Code estándar de Microsoft:
1. **Oracle Developer Tools for VS Code (Official)** (`Oracle.oracledevtools`)
2. **Oracle SQL Developer Extension for VS Code** (`Oracle.sql-developer`)

Instalación rápida por terminal:
```bash
code --install-extension Oracle.oracledevtools
code --install-extension Oracle.sql-developer
```

---

### Método B: Instalación Directa mediante VSIX (Para Open VSX, VSCodium o Forks)
En entornos donde el Marketplace oficial de Microsoft está restringido o se utiliza el registro alternativo Open VSX, puedes instalar la extensión oficial descargando el paquete VSIX compilado directamente por Oracle:

* **Enlace de Descarga Directa Oficial (Oracle CDN):**  
  [Descargar Oracle SQL Developer VSIX v26.3.0 (Win64)](https://download.oracle.com/otn_software/java/sqldeveloper/sql-developer-win32-x64-26.3.0.vsix)

#### ¿Cómo instalar el archivo `.vsix`?
1. **Por Terminal (PowerShell / CMD):**
   ```powershell
   # En VS Code estándar:
   code --install-extension sql-developer-win32-x64-26.3.0.vsix

   # En VSCodium:
   codium --install-extension sql-developer-win32-x64-26.3.0.vsix

   # En Cursor:
   cursor --install-extension sql-developer-win32-x64-26.3.0.vsix
   ```
2. **Por Interfaz Gráfica (GUI):**
   - Abre la pestaña de **Extensiones** (`Ctrl + Shift + X`).
   - Haz clic en el menú de los tres puntos (**`...`**) en la esquina superior derecha del panel de extensiones.
   - Selecciona **Instalar desde VSIX... (Install from VSIX...)**.
   - Busca y selecciona el archivo `sql-developer-win32-x64-26.3.0.vsix` descargado.

---

## 2. Parámetros y Cadena de Conexión

### 2.1. Formato de Parámetros Individuales (Modo Básico)

Al crear una nueva conexión en el panel de **Oracle Explorer** de VS Code, completa los siguientes campos:

| Parámetro | Valor Local Típico (Oracle XE) | Valor en Servidor / Contenedor |
| :--- | :--- | :--- |
| **Connection Type** | Basic | Basic / TNS |
| **Host Name** | `localhost` o `127.0.0.1` | `192.168.x.x` o hostname remoto |
| **Port** | `1521` | `1521` (o puerto configurado) |
| **Service Name / SID** | `XEPDB1` (Pluggable DB) o `XE` | `ORCL`, `FREEPDB1`, etc. |
| **User Name** | `ROSAS_ADMIN` (o usuario del proyecto) | `ROSAS_ADMIN` |
| **Password** | *[Contraseña configurada]* | *[Contraseña]* |
| **Role** | `Default` (o `SYSDBA` solo para inicializar) | `Default` |

> 💡 **Nota Importante sobre Oracle XE 18c/21c/23ai**:
> Siempre que sea posible, crea el esquema en la base de datos conectable (**PDB**, por ejemplo `XEPDB1` o `FREEPDB1`) y no en la raíz (`CDB$ROOT`).

### 2.2. Formato de Conexión EZConnect

Para herramientas de consola o cadenas de conexión directas:

```text
usuario/contraseña@host:puerto/nombre_servicio
```

**Ejemplo:**
```text
ROSAS_ADMIN/Mariachi2026!@localhost:1521/XEPDB1
```

### 2.3. Configuración para Python (`python-oracledb`)

El backend de este proyecto utiliza la librería moderna `oracledb` de Python. Por defecto opera en **Modo Thin** (ligero), lo que significa que **no requiere instalar el voluminoso Oracle Instant Client**:

```python
import oracledb

# Conexión directa en modo Thin
connection = oracledb.connect(
    user="ROSAS_ADMIN",
    password="Mariachi2026!",
    dsn="localhost:1521/XEPDB1"
)
print("Conectado a Oracle Database versión:", connection.version)
```

---

## 3. Comandos Básicos y Atajos en VS Code

Una vez conectado al árbol de Oracle Database en VS Code:

1. **Abrir nueva hoja de trabajo SQL (SQL Worksheet)**:
   - Haz clic derecho sobre tu conexión en el panel `Oracle Explorer` -> **Open SQL Worksheet**.
2. **Ejecutar la sentencia bajo el cursor**:
   - Presiona `Ctrl + Enter` (Windows/Linux) o `Cmd + Enter` (macOS).
3. **Ejecutar todo el script completo**:
   - Presiona `F5` o haz clic en el ícono de **Run Script** en la barra superior del editor.
4. **Explicar Plan de Ejecución (Explain Plan)**:
   - Presiona `F10` para analizar el rendimiento de una consulta antes de pasarla a producción.

---

## 4. Orden de Ejecución de Scripts del Proyecto

Los scripts SQL están versionados en la carpeta `database/scripts/`. Deben ejecutarse en el siguiente orden secuencial bajo el usuario `ROSAS_ADMIN` en `XEPDB1`:

1. **`database/scripts/01_schema_ddl.sql`**: Esquema base (Clientes, Formatos, Zonas, Eventos Reservas, Pagos, Integrantes).
2. **`database/scripts/02_seed_data.sql`**: Catálogos iniciales (6 integrantes femeninas, tarifas por formato, recargos de cobertura).
3. **`database/scripts/03_canciones_ddl.sql`**: Repertorio de canciones, tabla de estados de reserva y relación N:M `RESERVA_CANCIONES`.
4. **`database/scripts/04_pagos_ddl.sql`**: Refactorización de pagos y creación de tabla `ANTICIPOS` (regla del 50% 1:1).
5. **`database/scripts/05_pagos_seed.sql`**: Datos de prueba con 3 reservas, anticipos calculados y pagos registrados en Soles (S/).
6. **`database/scripts/06_reserva_detalles_ddl_seed.sql`**: Clave foránea de estados, tabla asociativa `RESERVA_INTEGRANTES` (elenco/asistencia) y setlist de prueba.

> 💡 **Atajo con Esquema Completo:**
> Si prefieres inicializar toda la base de datos limpia de un solo golpe, puedes ejecutar directamente:
> **`database/diagrams/esquema_completo.sql`** (crea las 11 tablas interconectadas con todas sus Primary Keys, Foreign Keys y restricciones de negocio).

---

## 5. Solución de Problemas Comunes (Troubleshooting)

- **`ORA-12541: TNS:no listener`**:
  - El servicio de escucha de Oracle no está activo. En Windows, verifica en `services.msc` que el servicio `OracleOraDB...TNSListener` esté en estado **En ejecución**.
- **`ORA-01017: invalid username/password`**:
  - Verifica mayúsculas y minúsculas en el usuario o contraseña. Recuerda que Oracle distingue entre mayúsculas y minúsculas si la contraseña fue creada entre comillas dobles.
- **`ORA-12514: TNS:listener does not currently know of service requested`**:
  - Verifica si estás usando el SID en lugar del Service Name. Para Oracle XE moderno suele ser `XEPDB1` o `FREEPDB1`.
- **`ORA-28000: the account is locked`**:
  - Ejecuta desde `sqlplus sys/contraseña as sysdba`:
    ```sql
    ALTER USER ROSAS_ADMIN ACCOUNT UNLOCK;
    ```
