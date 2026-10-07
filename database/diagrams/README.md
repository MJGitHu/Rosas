# Diagramas de Base de Datos - Rosas de Guadalupe

En esta carpeta se almacenan los diagramas del modelo relacional (ERD) generados mediante Oracle SQL Developer, VS Code Data Tools o herramientas como Mermaid / PlantUML.

### Resumen del Modelo Relacional:

- **CLIENTES** (1) ───< (N) **EVENTOS_RESERVAS**
- **FORMATOS_MARIACHI** (1) ───< (N) **EVENTOS_RESERVAS**
- **ZONAS_COBERTURA** (1) ───< (N) **EVENTOS_RESERVAS**
- **EVENTOS_RESERVAS** (1) ───< (N) **PAGOS** (Anticipo 50% y Liquidación 50%)
- **INTEGRANTES_MARIACHI** (Catálogo de alineación de 6 músicas)
