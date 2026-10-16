# Reglas de Negocio - Rosas de Guadalupe Management System

Documento oficial que consolida la fuente de verdad técnica y de negocio para la plataforma de gestión y contratación de la agrupación musical femenina **"Rosas de Guadalupe"**. Este documento sirve como marco normativo para el desarrollo, validación de criterios de aceptación y respaldo en presentaciones ejecutivas.

---

## 1. Conformación del Grupo Musical
- Agrupación artística exclusivamente femenina integrada por 6 músicas profesionales:
  - 2 trompetistas
  - 1 vihuelista
  - 1 guitarronista
  - 2 cantantes (voz principal y coros/animación)

## 2. Formatos de Presentación
El catálogo comercial ofrece estos servicios y tarifas según la duración:

| Servicio / Formato | Integrantes | 30 minutos | 40 minutos | 60 minutos |
| --- | ---: | ---: | ---: | ---: |
| Mariachi completo | 6 | S/ 380 | S/ 480 | S/ 680 |
| Express 1 | 5 | S/ 340 | S/ 420 | S/ 600 |
| Express 2 | 4 | S/ 300 | S/ 360 | S/ 500 |
| Express dúo | - | S/ 250 | S/ 280 | S/ 420 |
| Solista | 1 | S/ 180 | S/ 220 | S/ 320 |

Cada hora adicional se cobra al precio de 60 minutos del formato seleccionado menos S/ 60.

## 3. Duraciones Permitidas
Las presentaciones se configuran estrictamente bajo los siguientes bloques temporales estandarizados:
- **30 minutos**
- **40 minutos**
- **60 minutos (1 hora)**

## 4. Tipos de Eventos / Ocasiones
El sistema categoriza la contratación según la naturaleza de la celebración para adecuar el vestuario, animación y repertorio protocolar:
- Serenata romántica
- Cumpleaños
- Boda
- 15 Años
- Aniversario corporativo
- Fiesta patronal
- Misa
- Ceremonia de honras / responso

## 5. Cobertura y Viáticos
- **Local / Regional:** Sin recargo adicional por desplazamiento dentro del perímetro urbano y conurbado establecido.
- **Nacional (Viaje interprovincial):** Recargo fijo de viáticos de traslado, calculados para cubrir peajes, combustible o pasajes terrestres/aéreos según la distancia.

## 6. Logística Incluida
- **Movilidad del elenco:** TODOS los servicios incluyen transporte y traslado integral de las integrantes y sus instrumentos.
- **Equipo de sonido propio:** TODOS los servicios incluyen equipamiento de audio y microfonía adaptado a la locación.
- **Sin costos ocultos:** La logística de traslado y audio se incluye sin cobro adicional inesperado para el anfitrión (salvo viáticos nacionales explícitamente cotizados).

## 7. Reglas Financieras
- **Anticipo obligatorio (50%):** Es indispensable el pago del 50% del presupuesto total para congelar la agenda y reservar formalmente la fecha y hora.
- **Saldo restante (50%):** El 50% pendiente se liquida momentos previos al inicio del show en la locación del evento.
- **Moneda de curso:** Todos los montos, cotizaciones y transacciones se expresan y procesan en **Soles peruanos (S/)**.
- **Comisión por pasarela de tarjeta (5%):** Se aplica un recargo adicional del **5% exclusivamente** para abonos procesados con **Tarjeta de Crédito**.
- **Exoneración de comisión (0%):** Los pagos realizados mediante **Efectivo**, **Yape / Plin** o **Transferencia bancaria** mantienen una comisión del **0%** (sin recargo adicional al monto cotizado).

## 8. Métodos de Pago
Canales financieros admitidos por la plataforma:
- **Efectivo:** Recaudo presencial en oficina o en el punto de encuentro.
- **Yape / Plin:** Billeteras digitales móviles directas (0% comisión adicional).
- **Transferencia o depósito bancario:** Cuenta de ahorros oficial (permite registrar el número de operación o comprobante digital para validación administrativa).
- **Tarjeta de crédito:** Procesamiento electrónico con recargo del 5% correspondiente al costo de la pasarela.

## 9. Repertorio Musical
- **Género ranchero tradicional:** Clásicos de la música mexicana, serenatas, mañanitas y sones.
- **Covers versionados:** Adaptaciones al estilo mariachi de temas populares de rock, pop y cumbia tropical.
- **Campo de dedicatorias y observaciones:** Espacio habilitado durante la contratación para que el cliente ingrese canciones predilectas, dedicatorias personalizadas o indicaciones logísticas especiales para el anfitrión.

## 10. Política de Cancelaciones
- **Con aviso anticipado >= 72 horas:** Retención del **20%** del anticipo por gastos operativos y reserva de fecha; devolución del **80%** restante al cliente.
- **Con aviso tardío < 72 horas:** Retención del **100%** del anticipo (sin reembolso), debido al bloqueo de agenda que impidió contratar otras presentaciones en ese horario.

## 11. Estados de Reserva
El ciclo de vida de cada contratación transita por los siguientes estados normalizados:
- **`COTIZADA`:** Presupuesto generado automáticamente en el sistema; fecha tentativa a la espera del pago de separación.
- **`ANTICIPO_PAGADO`:** Anticipo del 50% recibido y verificado; fecha y horario bloqueados en el calendario de la agrupación.
- **`CONFIRMADA`:** Logística de traslado, horario de llegada y canciones/dedicatorias validadas y aprobadas con la dirección del mariachi.
- **`LIQUIDADA`:** Saldo del 50% restante cobrado y cancelado en su totalidad; servicio concluido satisfactoriamente.
- **`CANCELADA`:** Reserva anulada por solicitud del anfitrión o caducada por vencimiento del plazo de anticipo.

---

## Referencia Cruzada con Jira (Proyecto `RS`)

Mapeo de correspondencia entre las reglas de negocio y los artefactos del proyecto en Jira:

| Regla del Negocio | Historia / Subtarea Jira | Estado en Jira | Observación / Criterio |
|---|---|---|---|
| **Conformación de 6 integrantes** | `RS-5` | Documentada como comentario | Integrantes: 2 trompetas, vihuela, guitarrón, 2 voces. |
| **Formatos disponibles** | `RS-15` (HU11) | En criterios de aceptación | Mariachi Completo, Cuarteto, Dúo con pistas, Solista. |
| **Duraciones permitidas** | `RS-15` (HU11) | En criterios de aceptación | 30 min, 40 min, 1 hora. |
| **Tipos de evento** | `RS-15` (HU11) | Documentada como comentario / Criterios | Serenata, Boda, Cumpleaños, 15 Años, Aniversario, etc. |
| **Cobertura Local / Nacional** | `RS-95` (HU05), Épica `RS-78` | Documentada como comentario / Criterios | Tarifas por viáticos de traslado territorial. |
| **Movilidad y sonido incluidos** | `RS-5` | Documentada como comentario | Todo servicio contempla movilidad y sonido propio. |
| **Anticipo 50%** | `RS-8` (HU04), `RS-10` (HU06) | En criterios de aceptación | Desglose obligatorio del 50% para congelar fecha. |
| **Saldo 50% previo al show** | `RS-10` (HU06), `RS-8` | Documentada como comentario | Liquidación restante antes de iniciar la presentación. |
| **Comisión 5% tarjeta** | `RS-8` (HU04), `RS-10` (HU06), `RS-129` | En criterios de aceptación | Recargo automático del 5% solo con Tarjeta de Crédito. |
| **Métodos de pago** | `RS-10` (HU06), `RS-128` | En criterios de aceptación | Efectivo, Yape/Plin, Transferencia y Tarjeta. |
| **Moneda en Soles (S/)** | `RS-8` (HU04) | Documentada como comentario | Unidad monetaria oficial del proyecto. |
| **Política de cancelaciones** | `RS-14`, Épica `RS-79` | Documentada como comentario | Reglas de retención del 20% (>=72h) y 100% (<72h). |
