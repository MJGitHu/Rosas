# Mi Contexto de Jira - Proyecto RS (Rosas de Guadalupe)

> Generado el 07/10/2026 (hora de Lima) a partir de Jira, solo lectura.
> Fuente: https://upao-team-e2o81s7v.atlassian.net/issues/?jql=project%20%3D%20RS%20AND%20assignee%20%3D%20currentUser%28%29%20AND%20issuetype%20in%20subTaskIssueTypes%28%29%20ORDER%20BY%20key%20ASC
> Convención: "(vacío)" = el campo existe pero no tiene valor; "(no aplica)" = el campo no existe para ese tipo de incidencia; ⚠️ = dato no verificado en Jira.

## 1. Información General
- Proyecto: RS (Página Rosas) - "Rosas de Guadalupe Management System"
- Sprint activo: SCRUM Sprint 0 (estado: active). Del 03/10/2026 04:30 UTC al 17/10/2026 04:30 UTC (en hora de Lima: del 02/10/2026 23:30 al 16/10/2026 23:30)
- Sprint Goal: "Desplegar el MVP operativo que permita al cliente cotizar los formatos del mariachi, seleccionar la duración del show, registrar la reserva y procesar el anticipo del 50%."
- Mi usuario: unforastero6741
- Mi rol: Desarrollador
- Total de mis subtareas en el sprint: 12
- Total de horas estimadas: 34h
- Velocidad del equipo: 20 Story Points por sprint de 2 semanas (⚠️ dato del plan; el sprint activo suma 37 SP)
- Duración del sprint: 2 semanas (10 días laborables)
- Otras subtareas mías fuera de este sprint (SCRUM Sprint 1, futuro, sin tipo ni horas): RS-25, RS-52, RS-53, RS-63, RS-69, RS-86

## 2. Reglas del Negocio (aplican a todas mis tareas)

### 2.1 Reglas verificadas en Jira
- Anticipo obligatorio del 50% del monto total para reservar la fecha. (RS-8, RS-10)
- Saldo restante del 50%. (RS-8)
- Comisión adicional del 5% SOLO para pagos con Tarjeta de Crédito. (RS-8, RS-10)
- Si el método no tiene comisión, se mantiene el monto calculado sin recargo. (RS-8)
- Métodos de pago definidos por negocio: Efectivo, Yape/Plin, Transferencia o depósito bancario y Tarjeta de crédito. (RS-10, RS-128)
- Para transferencia, depósito o medios digitales que requieran comprobación, el cliente puede registrar el número de operación o comprobante. (RS-10)
- El sistema registra el monto abonado y el método de pago utilizado. (RS-10)
- Una vez validado el pago del 50%, la reserva cambia a estado "Confirmada". (RS-10)
- La reserva permanece pendiente hasta que se valide el pago del anticipo. (RS-95)
- El precio se calcula automáticamente según el formato, la duración y la ubicación. (RS-8)
- Una vez aceptada la cotización, se permite continuar con la reserva. (RS-8, RS-116)
- Formatos: Mariachi Completo, Cuarteto, Dúo con pistas, Cantante Solista. (RS-15)
- Duraciones permitidas: 30 minutos, 40 minutos, 1 hora. (RS-15)
- Ocasiones: Serenata, Boda, Cumpleaños, 15 Años, Aniversario, Fiesta Patronal, Misa o Ceremonia de honras/responso. (RS-15)
- Campo de dedicatorias/observaciones para canciones preferidas o indicaciones especiales; se almacena en el registro del evento. (RS-15)
- Disponibilidad: no se pueden seleccionar horarios ocupados y se considera el tiempo de traslado entre presentaciones. (RS-95)
- Solapamiento: se bloquea el registro si el horario coincide o deja menos de 45 minutos de margen de traslado con otro evento. (RS-12)
- Calendario mensual o semanal con presentaciones identificadas por colores según su estado. (RS-12)
- Cobertura territorial con viáticos (las tarifas se configuran por cobertura). (Épica RS-78)
- Sesión de administración segura: credenciales usuario/correo + contraseña; mensajes de error sin exponer información sensible; caducidad por inactividad; las rutas protegidas redirigen al login; al cerrar sesión se destruye la sesión y no se puede volver a entrar con el historial del navegador. (RS-82)
- (Sprint 1, no es del sprint activo) Recargo automático del 5% cuando el saldo se paga con Tarjeta de Crédito en el local. (RS-63)

### 2.2 Reglas indicadas por el usuario y NO encontradas en Jira (⚠️ verificar con el PO)
- Saldo del 50% se liquida previo al show.
- Todos los montos en Soles peruanos (S/).
- Mariachi Completo = 6 integrantes.
- Todos los servicios incluyen movilidad y sonido propio.
- Cobertura Local/Regional y Nacional (en Jira solo aparece "cobertura territorial/viáticos").
- "Aniversarios corporativos" (en Jira RS-15 dice solo "Aniversario").
- Política de cancelaciones: >= 72h retiene 20%, < 72h retiene 100% (la épica RS-79 menciona "políticas de cancelación/devolución" sin porcentajes).

## 3. Mis Subtareas Asignadas en el Sprint Activo

> Valores comunes a las 12 subtareas: Tipo de incidencia = Subtarea · Sprint = SCRUM Sprint 0 · Prioridad (cf[10043]) = (vacío) · Prioridad Jira = Medium · Story Points = (vacío) · Tiempo registrado = (vacío), sin registros de trabajo · Responsable = unforastero6741 · Criterios de aceptación = (no aplica para subtareas)

### RS-137 - Diseñar modelo de pagos, anticipos y estados
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-10 - HU06 - Pago del anticipo |
| **Épica Padre** | RS-78 - Cotización, Tarifas y Pagos |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer (⚠️ el cambio a "En curso" NO se aplicó; sin comentarios) |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Análisis y diseño |
| **Estimación original** | 2h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 2h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Media |
| **Descripción** | (vacío) |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-128 - Configurar métodos de pago permitidos para el anticipo
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-10 - HU06 - Pago del anticipo |
| **Épica Padre** | RS-78 - Cotización, Tarifas y Pagos |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Configuración |
| **Estimación original** | 3h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 3h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Media |
| **Descripción** | Habilitar en el sistema los métodos de pago definidos por negocio: efectivo, Yape/Plin, transferencia o depósito bancario y tarjeta de crédito, mostrando solo opciones válidas durante el registro del anticipo. |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-129 - Aplicar comisión del 5% para pagos con tarjeta de crédito
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-10 - HU06 - Pago del anticipo |
| **Épica Padre** | RS-78 - Cotización, Tarifas y Pagos |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Codificación |
| **Estimación original** | 2h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 2h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Media |
| **Descripción** | Calcular automáticamente la comisión adicional correspondiente al 5% cuando el anticipo se registre como pago con tarjeta de crédito, ajustando el total a registrar. |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-138 - Probar registro y validación del anticipo
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-10 - HU06 - Pago del anticipo |
| **Épica Padre** | RS-78 - Cotización, Tarifas y Pagos |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Test |
| **Estimación original** | 3h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 3h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Media |
| **Descripción** | (vacío) |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-114 - Mostrar el desglose del anticipo y el saldo restante
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-8 - HU04 - Proceso de cotizacion |
| **Épica Padre** | RS-78 - Cotización, Tarifas y Pagos |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Codificación |
| **Estimación original** | 3h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 3h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Media |
| **Descripción** | Presentar al usuario el detalle de pago con el anticipo obligatorio del 50% para reservar la fecha y el 50% restante como saldo pendiente. |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-116 - Validar la aceptación de la cotización para continuar con la reserva
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-8 - HU04 - Proceso de cotizacion |
| **Épica Padre** | RS-78 - Cotización, Tarifas y Pagos |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Codificación |
| **Estimación original** | 2h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 2h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Media |
| **Descripción** | Permitir que, una vez aceptada la cotización, el sistema habilite el flujo para continuar con el proceso de reserva de la presentación. |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-122 - Implementar validación de datos obligatorios de la reserva
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-95 - HU05 - Reserva |
| **Épica Padre** | RS-79 - Sistema de Reservas y Gestión de Agenda |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Codificación |
| **Estimación original** | 3h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 3h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Media |
| **Descripción** | Validar que el cliente ingrese los datos mínimos requeridos para la contratación y que los campos del evento tengan formato correcto antes de guardar la reserva. |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-133 - Gestionar sesión segura con expiración por inactividad
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-82 - HU13 - Sesion de administracion |
| **Épica Padre** | RS-79 - Sistema de Reservas y Gestión de Agenda |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Codificación |
| **Estimación original** | 3h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 3h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Media |
| **Descripción** | Configurar la creación y mantenimiento de la sesión autenticada, incluyendo caducidad automática por inactividad y mecanismos para proteger las operaciones administrativas. |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-135 - Crear pantalla de inicio de sesión de administración
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-82 - HU13 - Sesion de administracion |
| **Épica Padre** | RS-79 - Sistema de Reservas y Gestión de Agenda |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Prototipado |
| **Estimación original** | 4h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 4h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Alta (por la estimación de 4h) |
| **Descripción** | Diseñar e implementar la vista/formulario para que la administradora ingrese usuario o correo y contraseña, incluyendo estados de carga, errores y validaciones básicas de campos vacíos. |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-139 - Probar inicio, expiración y cierre de sesión
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-82 - HU13 - Sesion de administracion |
| **Épica Padre** | RS-79 - Sistema de Reservas y Gestión de Agenda |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Test |
| **Estimación original** | 2h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 2h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Media |
| **Descripción** | (vacío) |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-59 - Listar presentaciones agendadas en el calendario con codificación por color
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-12 - HU08 - Gestion de calendario y reservas |
| **Épica Padre** | RS-79 - Sistema de Reservas y Gestión de Agenda |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Codificación |
| **Estimación original** | 4h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 4h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Alta |
| **Descripción** | Mostrar los eventos del calendario identificando cada presentación según su estado mediante colores, conforme a los criterios de aceptación. |
| **Criterios de aceptación** | (no aplica para subtareas) |

### RS-110 - Probar la configuración de presentación y el guardado de datos
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Subtarea |
| **Historia Padre** | RS-15 - HU11 - Configuracion de la presentacion |
| **Épica Padre** | RS-77 - Catálogo Digital y Repertorio Musical |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | Tareas por hacer |
| **Prioridad (cf[10043])** | (vacío) |
| **Prioridad Jira** | Medium |
| **Story Points (cf[10016])** | (vacío) |
| **Tipo de tarea (cf[10046])** | Test |
| **Estimación original** | 3h |
| **Tiempo registrado** | (vacío) |
| **Tiempo restante** | 3h |
| **Responsable** | unforastero6741 |
| **Nivel de complejidad (inferido)** | Media |
| **Descripción** | Verificar que el formulario permita seleccionar correctamente las opciones, registrar observaciones y almacenar la información en el evento sin pérdida de datos. |
| **Criterios de aceptación** | (no aplica para subtareas) |

---

## 4. Historias de Usuario Padre (de mis subtareas)

> Nivel de complejidad inferido por Story Points: 3 = Baja, 5 = Media, 8 = Alta.
> Nota: los criterios están en formato de lista/texto, NO en Gherkin (Dado/Cuando/Entonces). Se copian tal cual están en Jira.

### RS-8 - HU04 - Proceso de cotizacion
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Historia |
| **Épica Padre** | RS-78 - Cotización, Tarifas y Pagos |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | En curso |
| **Prioridad (cf[10043])** | 4 |
| **Prioridad Jira** | Highest |
| **Story Points** | 5 |
| **Nivel de complejidad (inferido)** | Media |
| **Responsable** | Sin asignar |
| **Descripción** | Resumen: Como cliente, quiero cotizar el costo total de mi presentación teniendo en cuenta el formato, la duración y la ubicación del evento, para conocer los montos exactos que debo abonar. · Contexto: El proceso corresponde a la cotización de una presentación. · Criterios (en la descripción): Se debe poder cotizar el costo total de la presentación. La cotización debe considerar: el formato, la duración, la ubicación del evento. La cotización debe mostrar los montos exactos a abonar. · Otra información: HU04 - Proceso de cotizacion |

**Criterios de Aceptación (cf[10045]):**
- El usuario selecciona el formato, duración y ubicación de la presentación.
- El sistema calcula automáticamente el precio del servicio de acuerdo con el formato, duración y ubicación seleccionados.
- El sistema muestra el monto total del servicio.
- El sistema desglosa el anticipo obligatorio del 50% para reservar la fecha y el saldo restante del 50%.
- El usuario selecciona el método de pago y el sistema aplica la comisión correspondiente cuando corresponda.
- Si el usuario selecciona Tarjeta de Crédito, el sistema agrega automáticamente una comisión adicional del 5% al monto correspondiente.
- Si el usuario selecciona un método sin comisión adicional, el sistema mantiene el monto calculado sin recargo.
- Una vez aceptada la cotización, el sistema permite continuar con el proceso de reserva.

**Subtareas asociadas (solo las mías):**
| Key | Título | Tipo | Horas | Estado |
|---|---|---|---|---|
| RS-114 | Mostrar el desglose del anticipo y el saldo restante | Codificación | 3h | Tareas por hacer |
| RS-116 | Validar la aceptación de la cotización para continuar con la reserva | Codificación | 2h | Tareas por hacer |

---

### RS-10 - HU06 - Pago del anticipo
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Historia |
| **Épica Padre** | RS-78 - Cotización, Tarifas y Pagos |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | En curso |
| **Prioridad (cf[10043])** | 4 |
| **Prioridad Jira** | Highest |
| **Story Points** | 8 |
| **Nivel de complejidad (inferido)** | Alta |
| **Responsable** | Sin asignar |
| **Descripción** | Como administradora o cliente, quiero registrar el pago del anticipo del 50% mediante diversos canales financieros, para formalizar y confirmar la reserva de la fecha. |

**Criterios de Aceptación (cf[10045]):**
- El cliente selecciona el medio mediante el cual realizará el pago.
- El sistema admite los métodos de pago definidos por el negocio: efectivo, Yape/Plin, transferencia o depósito bancario y tarjeta de crédito.
- Para pagos mediante transferencia, depósito o medios digitales que requieran comprobación, el cliente puede registrar el número de operación o comprobante.
- Si el pago se realiza mediante tarjeta de crédito, el sistema aplica la comisión adicional del 5% correspondiente.
- El sistema registra el monto abonado y el método de pago utilizado.
- Una vez validado el pago del 50% del monto correspondiente, la reserva cambia a estado "Confirmada".

**Subtareas asociadas (solo las mías):**
| Key | Título | Tipo | Horas | Estado |
|---|---|---|---|---|
| RS-128 | Configurar métodos de pago permitidos para el anticipo | Configuración | 3h | Tareas por hacer |
| RS-129 | Aplicar comisión del 5% para pagos con tarjeta de crédito | Codificación | 2h | Tareas por hacer |
| RS-137 | Diseñar modelo de pagos, anticipos y estados | Análisis y diseño | 2h | Tareas por hacer |
| RS-138 | Probar registro y validación del anticipo | Test | 3h | Tareas por hacer |

---

### RS-12 - HU08 - Gestion de calendario y reservas
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Historia |
| **Épica Padre** | RS-79 - Sistema de Reservas y Gestión de Agenda |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | En curso |
| **Prioridad (cf[10043])** | 3 |
| **Prioridad Jira** | High |
| **Story Points** | 5 |
| **Nivel de complejidad (inferido)** | Media |
| **Responsable** | Sin asignar |
| **Descripción** | Como administradora, quiero consultar una agenda gráfica en formato calendario, para organizar las fechas del mariachi y evitar cruces de horario. |

**Criterios de Aceptación (cf[10045]):**
- Se visualiza el calendario mensual o semanal, se muestran las presentaciones agendadas identificadas por colores según su estado.
- Cuando se intenta ingresar una nueva presentación y el horario coincide o deja menos de 45 minutos de margen de traslado con otro evento el sistema bloquea el registro por solapamiento logístico.

**Subtareas asociadas (solo las mías):**
| Key | Título | Tipo | Horas | Estado |
|---|---|---|---|---|
| RS-59 | Listar presentaciones agendadas en el calendario con codificación por color | Codificación | 4h | Tareas por hacer |

---

### RS-15 - HU11 - Configuracion de la presentacion
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Historia |
| **Épica Padre** | RS-77 - Catálogo Digital y Repertorio Musical |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | En curso |
| **Prioridad (cf[10043])** | 4 |
| **Prioridad Jira** | Highest |
| **Story Points** | 3 |
| **Nivel de complejidad (inferido)** | Baja |
| **Responsable** | Sin asignar |
| **Descripción** | Como cliente, quiero seleccionar el formato de la agrupación, la ocasión del evento, la duración del show e ingresar dedicatorias, para configurar la presentación musical de acuerdo con mis necesidades. |

**Criterios de Aceptación (cf[10045]):**
- El usuario selecciona el formato de presentación entre las opciones disponibles: Mariachi Completo, Cuarteto, Dúo con pistas o Cantante Solista.
- El usuario selecciona el tiempo de presentación; las opciones válidas son 30 minutos, 40 minutos o 1 hora.
- Cuando se despliega la lista de ocasiones, se permite seleccionar: Serenata, Boda, Cumpleaños, 15 Años, Aniversario, Fiesta Patronal, Misa o Ceremonia de honras/responso.
- Si el cliente tiene canciones preferidas o indicaciones especiales, puede escribirlas en el campo de dedicatorias/observaciones.
- Las preferencias y observaciones ingresadas se almacenan en el registro del evento.

**Subtareas asociadas (solo las mías):**
| Key | Título | Tipo | Horas | Estado |
|---|---|---|---|---|
| RS-110 | Probar la configuración de presentación y el guardado de datos | Test | 3h | Tareas por hacer |

---

### RS-82 - HU13 - Sesion de administracion
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Historia |
| **Épica Padre** | RS-79 - Sistema de Reservas y Gestión de Agenda |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | En curso |
| **Prioridad (cf[10043])** | 3 |
| **Prioridad Jira** | Medium |
| **Story Points** | 5 |
| **Nivel de complejidad (inferido)** | Media |
| **Responsable** | Sin asignar |
| **Descripción** | Como administradora, quiero iniciar sesión de forma segura para acceder a las funciones de gestión de Rosas de Guadalupe. |

**Criterios de Aceptación (cf[10045]):**
- La administradora ingresa sus credenciales (usuario/correo y contraseña) en la pantalla de acceso, el sistema valida los datos y concede el ingreso exitoso al panel de gestión de Rosas de Guadalupe.
- Si se ingresan credenciales incorrectas o campos vacíos, el sistema bloquea el ingreso y muestra mensajes de error y retroalimentación claros sin exponer información sensible.
- Tras un inicio de sesión exitoso, el sistema gestiona y mantiene una sesión segura con caducidad por inactividad para proteger las operaciones administrativas.
- Si un usuario no autenticado intenta acceder a rutas o funciones protegidas de administración, el sistema restringe el acceso de forma automática y lo redirige a la pantalla de inicio de sesión.
- Cuando la administradora selecciona la opción de cerrar sesión, el sistema destruye la sesión activa de forma segura y redirige a la vista principal/login, impidiendo el reingreso mediante la navegación del historial.

**Subtareas asociadas (solo las mías):**
| Key | Título | Tipo | Horas | Estado |
|---|---|---|---|---|
| RS-133 | Gestionar sesión segura con expiración por inactividad | Codificación | 3h | Tareas por hacer |
| RS-135 | Crear pantalla de inicio de sesión de administración | Prototipado | 4h | Tareas por hacer |
| RS-139 | Probar inicio, expiración y cierre de sesión | Test | 2h | Tareas por hacer |

---

### RS-95 - HU05 - Reserva
| Campo | Valor |
|---|---|
| **Tipo de incidencia** | Historia |
| **Épica Padre** | RS-79 - Sistema de Reservas y Gestión de Agenda |
| **Sprint** | SCRUM Sprint 0 |
| **Estado** | En curso |
| **Prioridad (cf[10043])** | 4 |
| **Prioridad Jira** | Medium (⚠️ no coincide con cf[10043] = 4) |
| **Story Points** | 8 |
| **Nivel de complejidad (inferido)** | Alta |
| **Responsable** | Sin asignar |
| **Descripción** | Como cliente, quiero registrar una reserva indicando mis datos, ubicación, fecha y hora del evento, para solicitar una presentación y asegurar un horario disponible. |

**Criterios de Aceptación (cf[10045]):**
- El cliente ingresa sus datos de contacto necesarios para la contratación.
- El cliente selecciona la fecha y hora de la presentación.
- El cliente ingresa la ubicación o dirección donde se realizará el evento.
- El sistema consulta la disponibilidad del mariachi para la fecha y hora seleccionadas.
- El sistema impide seleccionar horarios que se encuentren ocupados.
- El sistema considera el tiempo necesario para el traslado entre presentaciones al determinar la disponibilidad.
- La reserva almacena la información del servicio seleccionado, los datos del cliente y los detalles del evento.
- La reserva permanece pendiente hasta que se valide el pago del anticipo correspondiente.

**Subtareas asociadas (solo las mías):**
| Key | Título | Tipo | Horas | Estado |
|---|---|---|---|---|
| RS-122 | Implementar validación de datos obligatorios de la reserva | Codificación | 3h | Tareas por hacer |

---

## 5. Épicas del Proyecto

> Las 4 épicas están en "Tareas por hacer", con responsable MIJAEL VILLAVICENCIO RABINES.

| Key | Nombre | Descripción | Historias vinculadas (sprint activo) |
|---|---|---|---|
| RS-77 | Catálogo Digital y Repertorio Musical | Módulo que agrupa la visualización de información del mariachi, catálogo de repertorio, galería multimedia de presentaciones y personalización de temas para eventos. | RS-5, RS-15 |
| RS-78 | Cotización, Tarifas y Pagos | Módulo para el cálculo dinámico de precios, configuración de tarifas por cobertura territorial/viáticos y pasarela/procesamiento de pagos y anticipos. | RS-8, RS-10 |
| RS-79 | Sistema de Reservas y Gestión de Agenda | Módulo encargado del flujo de reservas de fechas/horas, control de disponibilidad en calendario para evitar solapamientos y políticas de cancelación/devolución. | RS-12, RS-82, RS-95 |
| RS-80 | Notificaciones y Comunicación con Clientes | Módulo para el envío automatizado de confirmaciones, comprobantes, recordatorios previos al evento y mensajes post-venta vía WhatsApp y correo. | (ninguna en el sprint activo) |

---

## 6. Estructura del Repositorio (referencia rápida)

> ⚠️ Información proporcionada por el usuario; no proviene de Jira.

```text
/backend/              → Python + Flask
  /app/routes/         → Endpoints REST
  /app/services/       → Lógica de negocio
  /app/config.py       → Configuración
  /app/db.py           → Conexión Oracle
/database/scripts/     → Scripts SQL para Oracle (01, 02, 03 usados; siguiente: 04)
/database/diagrams/    → Diagramas ER
/frontend/             → HTML/CSS/JS vanilla
/docs/                 → Documentación
```

---

## 7. Numeración de Scripts SQL (estado actual)

> ⚠️ Información proporcionada por el usuario; no proviene de Jira.

| Número | Archivo | Tablas que crea |
|---|---|---|
| 01 | 01_schema_ddl.sql | clientes, zonas_cobertura, formatos_mariachi, eventos_reservas, pagos (preliminar), integrantes_mariachi |
| 02 | 02_seed_data.sql | Datos semilla (6 músicas, 3 formatos, 4 zonas) |
| 03 | 03_canciones_ddl.sql | canciones, reserva_canciones, estados_reserva |
| 04 | (disponible) | — |
| 05 | (disponible) | — |

---

## 8. Convenciones

> ⚠️ Información proporcionada por el usuario; no proviene de Jira.

- **Commits:** `RS-XXX: descripción breve`
- **Ramas:** `feature/RS-XXX-descripcion`
- **Montos:** siempre en Soles peruanos (S/)
- **Sintaxis SQL:** Oracle (VARCHAR2, NUMBER, GENERATED ALWAYS AS IDENTITY)
- **Backend:** Python 3.11+ / Flask 3.0.3
- **Base de datos:** Oracle Database
- **IDE:** VS Code con extensión Oracle SQL Developer

---

## 9. Glosario de Campos de Jira

| Campo | Descripción |
|---|---|
| cf[10043] | Prioridad numérica (4 = Must, 3 = Should, 2 = Could, 1 = Won't). En Jira se muestra como "Prioridad"; solo tiene valor en las historias. |
| cf[10016] | Story Points (Fibonacci: 1, 2, 3, 5, 8). En Jira se muestra como "Story point estimate"; solo tiene valor en las historias. |
| cf[10045] | Criterios de aceptación ("Criterios de aceptacion"). Formato previsto: Gherkin BDD; formato real: lista de viñetas o texto. |
| cf[10046] | Tipo de tarea (6 categorías). Es un campo de texto libre, no una lista desplegable. |

**Tipos de tarea válidos (cf[10046]):**
1. Configuración
2. Análisis y diseño
3. Prototipado
4. Codificación
5. Test
6. Implantación

---

## 10. Resumen de Mi Carga

| Métrica | Valor |
|---|---|
| Total de subtareas | 12 |
| Total de horas estimadas | 34h |
| Subtareas de tipo Prototipado | 1 |
| Subtareas de tipo Análisis y diseño | 1 |
| Subtareas de tipo Codificación | 6 |
| Subtareas de tipo Test | 3 |
| Subtareas de tipo Configuración | 1 |
| Subtareas de tipo Implantación | 0 |
| Horas registradas | 0h |
| Estado | 12 en "Tareas por hacer", 0 "En curso", 0 "Finalizada" |

**Distribución por historia padre:**
| Historia | Subtareas | Horas |
|---|---|---|
| RS-10 - HU06 Pago del anticipo | RS-128, RS-129, RS-137, RS-138 | 10h |
| RS-82 - HU13 Sesión de administración | RS-133, RS-135, RS-139 | 9h |
| RS-8 - HU04 Proceso de cotización | RS-114, RS-116 | 5h |
| RS-12 - HU08 Calendario y reservas | RS-59 | 4h |
| RS-15 - HU11 Configuración de la presentación | RS-110 | 3h |
| RS-95 - HU05 Reserva | RS-122 | 3h |
| **Total** | **12** | **34h** |

---

## 11. Orden de Trabajo Sugerido

| Orden | Key | Título | Tipo | Horas | Razón |
|---|---|---|---|---|---|
| 1 | RS-137 | Diseñar modelo de pagos, anticipos y estados | Análisis y diseño | 2h | Define el modelo de datos que necesitan RS-128, RS-129, RS-114 y RS-138 |
| 2 | RS-128 | Configurar métodos de pago permitidos para el anticipo | Configuración | 3h | Base para calcular la comisión y registrar el anticipo |
| 3 | RS-129 | Aplicar comisión del 5% para pagos con tarjeta de crédito | Codificación | 2h | Depende de los métodos de pago de RS-128 |
| 4 | RS-114 | Mostrar el desglose del anticipo y el saldo restante | Codificación | 3h | Usa el modelo de anticipo/saldo; también depende del cálculo de la cotización (RS-112, de Mijael) |
| 5 | RS-116 | Validar la aceptación de la cotización para continuar con la reserva | Codificación | 2h | Conecta la cotización (RS-8) con la reserva (RS-95) |
| 6 | RS-122 | Implementar validación de datos obligatorios de la reserva | Codificación | 3h | Sigue al flujo de RS-116 dentro de la reserva |
| 7 | RS-133 | Gestionar sesión segura con expiración por inactividad | Codificación | 3h | Backend de la sesión que usará la pantalla RS-135 |
| 8 | RS-59 | Listar presentaciones agendadas en el calendario con codificación por color | Codificación | 4h | La más compleja; mejor cuando el modelo de estados de reserva ya esté claro |
| 9 | RS-135 | Crear pantalla de inicio de sesión de administración | Prototipado | 4h | Va después de la codificación, según la regla; se apoya en RS-133 |
| 10 | RS-138 | Probar registro y validación del anticipo | Test | 3h | Necesita RS-128 y RS-129 terminadas |
| 11 | RS-110 | Probar la configuración de presentación y el guardado de datos | Test | 3h | Depende del formulario de RS-15 (lo desarrollan otros compañeros) |
| 12 | RS-139 | Probar inicio, expiración y cierre de sesión | Test | 2h | Necesita RS-133 y RS-135 terminadas |

> Las dependencias se dedujeron de los títulos y descripciones; en Jira no se revisaron vínculos de bloqueo.

---

## Pendientes detectados al generar este documento
- RS-137 sigue en "Tareas por hacer" y sin comentarios: la transición a "En curso" no se aplicó.
- RS-137, RS-138 y RS-139 no tienen descripción.
- Ninguna historia tiene criterios de aceptación en formato Gherkin.
- RS-95: la prioridad cf[10043] = 4 no coincide con la prioridad Jira "Medium".
- Ninguna subtarea tiene horas registradas (worklog).