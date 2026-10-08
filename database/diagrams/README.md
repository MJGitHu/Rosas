# Diagramas de Base de Datos - Rosas de Guadalupe

En esta carpeta se gestionan los diagramas del modelo relacional (ERD) y el DDL completo del esquema **`ROSAS_ADMIN`** en **Oracle Database 21c (XEPDB1)**.

### Archivos Disponibles:

1. 📊 **[diagrama_er.html](file:///d:/rosas-de-guadalupe-rs/database/diagrams/diagrama_er.html)**: Visualizador interactivo HTML con soporte Pan/Zoom, tema oscuro institucional y tarjetas descriptivas de las 10 entidades.
2. 📄 **[diagrama_er.md](file:///d:/rosas-de-guadalupe-rs/database/diagrams/diagrama_er.md)**: Documentación técnica completa en Markdown con diagrama Mermaid, matriz de claves foráneas y cardinalidades.
3. 💾 **[esquema_completo.sql](file:///d:/rosas-de-guadalupe-rs/database/diagrams/esquema_completo.sql)**: Exportación DDL completa de las 10 tablas generada mediante `DBMS_METADATA.GET_DDL` de Oracle.
4. 💳 **[modelo_pagos.md](file:///d:/rosas-de-guadalupe-rs/database/diagrams/modelo_pagos.md)**: Diagrama y especificación de diseño detallado de la subtarea Jira **RS-137** (Pagos, Anticipos 1:1 y Estados de Reserva).

### Resumen de Entidades (10 Tablas):
- **CLIENTES** (1) ───< (N) **EVENTOS_RESERVAS**
- **FORMATOS_MARIACHI** (1) ───< (N) **EVENTOS_RESERVAS**
- **ZONAS_COBERTURA** (1) ───< (N) **EVENTOS_RESERVAS**
- **ESTADOS_RESERVA** (1) ───< (N) **EVENTOS_RESERVAS**
- **EVENTOS_RESERVAS** (1) ───|| (1) **ANTICIPOS** (Relación 1:1 estricta, anticipo 50%)
- **EVENTOS_RESERVAS** (1) ───< (N) **PAGOS** (Anticipos y saldos con comisión 5% en tarjeta)
- **EVENTOS_RESERVAS** (1) ───< (N) **RESERVA_CANCIONES** >─── (1) **CANCIONES** (Setlist N:M)
- **INTEGRANTES_MARIACHI** (Alineación oficial de 6 músicas profesionales)
