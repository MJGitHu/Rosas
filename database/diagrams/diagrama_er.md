# Diagrama Entidad-Relación (ERD) - Rosas de Guadalupe Management System

Este documento contiene el modelo de datos relacional completo implementado en **Oracle Database 21c (PDB: XEPDB1)** bajo el esquema **`ROSAS_ADMIN`**. Cubre las 10 tablas del sistema, sus claves primarias, foráneas, restricciones de negocio y cardinalidades.

---

## 1. Diagrama Entidad-Relación Completo (Mermaid)

```mermaid
erDiagram
    CLIENTES ||--o{ EVENTOS_RESERVAS : "registra (1:N)"
    FORMATOS_MARIACHI ||--o{ EVENTOS_RESERVAS : "contrata (1:N)"
    ZONAS_COBERTURA ||--o{ EVENTOS_RESERVAS : "ubica (1:N)"
    ESTADOS_RESERVA ||--o{ EVENTOS_RESERVAS : "clasifica_estado (1:N)"
    EVENTOS_RESERVAS ||--|| ANTICIPOS : "garantiza_anticipo_50 (1:1)"
    EVENTOS_RESERVAS ||--o{ PAGOS : "recibe_abonos (1:N)"
    EVENTOS_RESERVAS ||--o{ RESERVA_CANCIONES : "incluye_setlist (1:N)"
    CANCIONES ||--o{ RESERVA_CANCIONES : "interpretada_en (1:N)"

    CLIENTES {
        NUMBER id_cliente PK "Identity"
        VARCHAR2 nombre "Nombre(s)"
        VARCHAR2 apellido "Apellidos"
        VARCHAR2 telefono "Contacto WhatsApp/Cel"
        VARCHAR2 email UK "Correo único"
        VARCHAR2 direccion_referencia "Dirección del cliente"
        TIMESTAMP fecha_registro
    }

    ZONAS_COBERTURA {
        NUMBER id_zona PK "Identity"
        VARCHAR2 nombre_zona "Centro, Norte, Sur, Campestre"
        VARCHAR2 descripcion "Rango de cobertura"
        NUMBER recargo_transporte "Costo logística en S/"
        NUMBER tiempo_estimado_traslado_min "Minutos de viaje"
        CHAR activo "S / N"
    }

    FORMATOS_MARIACHI {
        NUMBER id_formato PK "Identity"
        VARCHAR2 nombre_formato "Serenata, 1 Hora, 2 Horas"
        VARCHAR2 descripcion "Detalle del espectáculo"
        NUMBER num_musicos "6 integrantes fijas"
        NUMBER precio_base_hora "Precio en Soles S/"
        CHAR incluye_equipo_audio "S / N"
        CHAR activo "S / N"
    }

    INTEGRANTES_MARIACHI {
        NUMBER id_integrante PK "Identity"
        VARCHAR2 nombre_completo "Nombre de la música"
        VARCHAR2 instrumento_rol "Voz, Trompeta, Vihuela, Guitarrón"
        VARCHAR2 telefono "Contacto interno"
        CHAR es_lider "S: Directora / N: Músico"
        CHAR activo "S / N"
    }

    ESTADOS_RESERVA {
        NUMBER id_estado PK "Identity"
        VARCHAR2 codigo UK "COTIZADA, ANTICIPO_PAGADO, CONFIRMADA, LIQUIDADA, CANCELADA"
        VARCHAR2 nombre "Nombre visible"
        VARCHAR2 descripcion "Significado en el flujo"
        CHAR es_final "S / N"
        NUMBER orden_flujo "1..5"
    }

    EVENTOS_RESERVAS {
        NUMBER id_reserva PK "Identity"
        VARCHAR2 codigo_reserva UK "RS-2026-XXX"
        NUMBER id_cliente FK "Ref a CLIENTES"
        NUMBER id_formato FK "Ref a FORMATOS_MARIACHI"
        NUMBER id_zona FK "Ref a ZONAS_COBERTURA"
        DATE fecha_evento "Fecha del espectáculo"
        VARCHAR2 hora_inicio "Hora acordada"
        NUMBER duracion_horas "Duración contratada"
        VARCHAR2 direccion_evento "Ubicación del evento"
        VARCHAR2 tipo_evento "Cumpleaños, Boda, 15 Años..."
        VARCHAR2 estado_reserva "Estado en flujo"
        NUMBER monto_subtotal "Costo base musical (S/)"
        NUMBER recargo_zona "Logística de traslado (S/)"
        NUMBER monto_total "Subtotal + Recargo (S/)"
        NUMBER anticipo_requerido "50% obligatorio (S/)"
        NUMBER saldo_pendiente "50% por liquidar (S/)"
        VARCHAR2 notas_logistica "Acceso, sorpresas, audio"
        TIMESTAMP fecha_creacion
    }

    ANTICIPOS {
        NUMBER id_anticipo PK "Identity"
        NUMBER id_reserva FK,UK "Relación 1:1 estricta"
        NUMBER monto_anticipo "50% en Soles (S/)"
        NUMBER monto_saldo "50% restante (S/)"
        NUMBER porcentaje "Default 50.00%"
        DATE fecha_limite_saldo "Fecha máxima pago saldo"
        VARCHAR2 estado "PENDIENTE, PAGADO, VENCIDO, REEMBOLSADO"
        TIMESTAMP fecha_creacion
    }

    PAGOS {
        NUMBER id_pago PK "Identity"
        NUMBER id_reserva FK "Ref a EVENTOS_RESERVAS"
        NUMBER monto "Monto abonado en Soles (S/)"
        VARCHAR2 metodo_pago "EFECTIVO, YAPE, PLIN, TRANSFERENCIA, TARJETA_CREDITO, TARJETA_DEBITO"
        NUMBER comision "5% en tarjeta, 0% en resto"
        VARCHAR2 num_operacion "Voucher / Ref bancaria"
        VARCHAR2 tipo_pago "ANTICIPO | SALDO"
        TIMESTAMP fecha_pago "Registro temporal"
    }

    CANCIONES {
        NUMBER id_cancion PK "Identity"
        VARCHAR2 titulo "Título de la canción"
        VARCHAR2 autor "Compositor"
        VARCHAR2 genero "Ranchera, Cumbia, Huapango, Bolero..."
        NUMBER duracion_aprox "Minutos aprox."
        CHAR es_cover "S / N"
        CHAR disponible "S / N"
        TIMESTAMP fecha_registro
    }

    RESERVA_CANCIONES {
        NUMBER id_reserva_cancion PK "Identity"
        NUMBER id_reserva FK "Ref a EVENTOS_RESERVAS"
        NUMBER id_cancion FK "Ref a CANCIONES"
        CHAR es_dedicatoria "S / N"
        NUMBER orden "Orden en el setlist"
        VARCHAR2 observaciones "Para quién va dedicada"
    }
```

---

## 2. Cardinalidades y Reglas de Negocio Implementadas

### 2.1 Contratación y Formatos (`clientes`, `formatos_mariachi`, `zonas_cobertura` ───< `eventos_reservas`)
* **1:N Clientes a Reservas:** Un cliente puede contratar múltiples presentaciones.
* **1:N Formatos a Reservas:** Formatos estándar con precios oficiales en Soles (`S/ 2,200`, `S/ 2,800`, `S/ 5,200`).
* **1:N Zonas a Reservas:** Tarifa plana para Zona Centro (`S/ 0.00`), Periferia Norte/Sur (`S/ 250.00`) y Campestre (`S/ 600.00`).

### 2.2 Política Financiera 50/50 y Relación 1:1 de Anticipos (`eventos_reservas` ||───|| `anticipos`)
* Cada reserva genera exactamente un registro en la tabla `anticipos` mediante la restricción `CONSTRAINT uq_anticipos_reserva UNIQUE (id_reserva)`.
* **Cálculo:** `monto_total = monto_subtotal + recargo_zona`.
* **Anticipo obligatorio:** `monto_total * 0.50` para bloquear la agenda.
* **Saldo restante:** `monto_total * 0.50` a liquidar antes de iniciar la presentación.

### 2.3 Pagos y Canales Peruanos (`eventos_reservas` 1───< N `pagos`)
* **Canales admitidos:** `EFECTIVO`, `YAPE`, `PLIN`, `TRANSFERENCIA`, `TARJETA_CREDITO`, `TARJETA_DEBITO`.
* **Regla de Comisión (RS-128 / RS-137):**
  * Tarjetas de Crédito / Débito: **5.00%** calculado sobre el monto abonado.
  * Transferencias y Billeteras digitales (Yape, Plin): **0.00%**.
* **Tipo de Pago:** Clasificado estrictamente en `ANTICIPO` o `SALDO`.

### 2.4 Repertorio Musical y Setlist (`eventos_reservas` N───M `canciones` vía `reserva_canciones`)
* Los clientes pueden armar un setlist personalizado de canciones disponibles en el repertorio, marcando aquellas que son **dedicatorias especiales**.

### 2.5 Integrantes del Mariachi (`integrantes_mariachi`)
* Tabla independiente que gestiona la conformación oficial de **6 músicas profesionales** (2 trompetas, 1 vihuela, 1 guitarrón, 2 cantantes/directora).

---

## 3. Matriz de Claves Foráneas (Integridad Referencial)

| Tabla Origen | Clave Foránea | Tabla Destino | Regla ON DELETE |
|---|---|---|---|
| `ANTICIPOS` | `id_reserva` | `EVENTOS_RESERVAS(id_reserva)` | `CASCADE` |
| `PAGOS` | `id_reserva` | `EVENTOS_RESERVAS(id_reserva)` | `CASCADE` |
| `EVENTOS_RESERVAS` | `id_cliente` | `CLIENTES(id_cliente)` | `NO ACTION` (Protege histórico) |
| `EVENTOS_RESERVAS` | `id_formato` | `FORMATOS_MARIACHI(id_formato)` | `NO ACTION` |
| `EVENTOS_RESERVAS` | `id_zona` | `ZONAS_COBERTURA(id_zona)` | `NO ACTION` |
| `RESERVA_CANCIONES` | `id_reserva` | `EVENTOS_RESERVAS(id_reserva)` | `NO ACTION` |
| `RESERVA_CANCIONES` | `id_cancion` | `CANCIONES(id_cancion)` | `NO ACTION` |

---

## 4. Archivos Relacionados
* [database/diagrams/diagrama_er.html](file:///d:/rosas-de-guadalupe-rs/database/diagrams/diagrama_er.html) - Visualizador interactivo HTML con Pan/Zoom.
* [database/diagrams/esquema_completo.sql](file:///d:/rosas-de-guadalupe-rs/database/diagrams/esquema_completo.sql) - Extracción DDL completa desde Oracle XE 21c (`DBMS_METADATA`).
* [database/diagrams/modelo_pagos.md](file:///d:/rosas-de-guadalupe-rs/database/diagrams/modelo_pagos.md) - Enfoque específico de la subtarea RS-137.
