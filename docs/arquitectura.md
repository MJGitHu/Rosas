# Arquitectura del Sistema - Rosas de Guadalupe

## 1. Visión General

**Rosas de Guadalupe Management System** es una plataforma web modular full-stack orientada a la digitalización del ciclo de vida de contratación del grupo de mariachi femenino "Rosas de Guadalupe".

```
+----------------------------------------------------------------+
|                        Capa de Cliente                         |
|   HTML5 Semántico + Vanilla CSS (Variables HSL/Dark) + JS ES6  |
+----------------------------------------------------------------+
                               |
                               | HTTP / JSON REST
                               v
+----------------------------------------------------------------+
|                        Capa de Backend                         |
|      Python 3.10+ / Flask Framework / Flask-CORS / python-dotenv|
|      - Blueprint Cotizaciones                                  |
|      - Blueprint Reservas & Agenda                             |
|      - Servicio de Finanzas (50% Anticipo / 50% Liquidación)   |
+----------------------------------------------------------------+
                               |
                               | python-oracledb (Thin Mode)
                               v
+----------------------------------------------------------------+
|                   Capa de Persistencia                         |
|      Oracle Database (XE / Cloud Free Tier / 19c/21c/23ai)      |
|      - Tablas: CLIENTES, FORMATOS, RESERVAS, PAGOS, ZONAS      |
+----------------------------------------------------------------+
```

## 2. Decisiones Arquitectónicas (ADRs)

1. **Python Flask en el Backend**:
   - Ligero, rápido para iteración de sprints cortos y con soporte nativo de primera clase para Oracle mediante `python-oracledb`.
2. **Modo Thin de `python-oracledb`**:
   - Elimina la necesidad de descargar e instalar Oracle Instant Client nativo de cientos de megabytes en las máquinas de los 5 desarrolladores del equipo.
3. **Frontend Desacoplado**:
   - Frontend estático altamente optimizado, sin sobrecarga de dependencias complejas en el MVP, permitiendo posterior integración transparente con React o Vue si la velocidad del equipo lo amerita.
