# Sprint 0 (MVP) — Proyecto RS "Página Rosas" (Rosas de Guadalupe)

> Documento de contexto para IA. Extraído de Jira el 15/10/2026 a las 10:59 (hora de Lima, UTC-5).
> Los textos de descripción, criterios de aceptación y tipo de tarea están copiados tal cual aparecen en Jira (sin parafrasear).
> Fuente: https://upao-team-e2o81s7v.atlassian.net (proyecto RS)

---

## 0. Datos generales del sprint

- **Nombre:** SCRUM Sprint 0 (id 2)
- **Estado:** active
- **Inicio:** 02/10/2026 23:30 (Lima) — **Fin:** 16/10/2026 23:30 (Lima). 14 días calendario.
- **Sprint Goal:** "Desplegar el MVP operativo que permita al cliente cotizar los formatos del mariachi, seleccionar la duración del show, registrar la reserva y procesar el anticipo del 50%."
- **Historias de usuario:** 7 — **Story Points:** 35 SP
- **Subtareas:** 43 — **Horas estimadas:** 152 h
- **Avance de subtareas (al corte):** 30 Finalizadas, 8 En curso, 5 Tareas por hacer
- **Campos usados:** Story Points = cf[10016]; Prioridad (escala 1–4) = cf[10043]; Criterios de aceptación = cf[10045]; Tipo de tarea = cf[10046] (texto libre)
- **Tipos de tarea oficiales del equipo:** Configuración, Análisis y diseño, Prototipado, Codificación, Test, Implantación

### Resumen de historias

| Key | Historia | Épica | SP | Prioridad cf[10043] | Prioridad Jira | Estado | Subtareas (finalizadas/total) | Horas |
|---|---|---|---|---|---|---|---|---|
| RS-5 | HU01 - Inf. Mariachi | RS-77 Catálogo Digital y Repertorio Musical | 1 | 4 | Highest | Finalizada | 5/5 | 14 |
| RS-8 | HU04 - Proceso de cotizacion | RS-78 Cotización, Tarifas y Pagos | 5 | 4 | Highest | En curso | 3/6 | 22 |
| RS-95 | HU05 - Reserva | RS-79 Sistema de Reservas y Gestión de Agenda | 8 | 4 | Medium | En curso | 6/8 | 30 |
| RS-10 | HU06 - Pago del anticipo | RS-78 Cotización, Tarifas y Pagos | 8 | 4 | Highest | En curso | 6/7 | 22 |
| RS-12 | HU08 - Gestion de calendario y reservas | RS-79 Sistema de Reservas y Gestión de Agenda | 5 | 3 | High | En curso | 3/6 | 26 |
| RS-15 | HU11 - Configuracion de la presentacion | RS-77 Catálogo Digital y Repertorio Musical | 3 | 4 | Highest | En curso | 4/5 | 18 |
| RS-82 | HU13 - Sesion de administracion | RS-140 Administración y Seguridad del Sistema | 5 | 3 | Medium | En curso | 3/6 | 20 |
| **Total** | | | **35** | | | | **30/43** | **152** |

---

## 1. RS-5 — HU01 - Inf. Mariachi

- **Épica:** RS-77 Catálogo Digital y Repertorio Musical
- **Story Points:** 1 — **Prioridad cf[10043]:** 4 — **Prioridad Jira:** Highest — **Estado:** Finalizada

### Descripción
Como cliente interesado, quiero visualizar la información del mariachi femenino Rosas de Guadalupe y sus formatos disponibles, para conocer la conformación instrumental y elegir la opción musical adecuada.

### Criterios de aceptación
1. Usuario consulta la información del mariachi, visualiza los datos que detalla que es una agrupación femenina completa de 6 integrantes (2 trompetas, vihuela, guitarrón y 2 voces).
2. Cuando se revisa el catálogo se muestran disponibles: Mariachi Completo, Cuarteto, Dúo con pistas y Cantante Solista.
3. Cuando se revisan los detalles se explicita que todo servicio incluye movilidad y equipo de sonido propio.

### Subtareas

#### RS-102 — Crear la sección informativa del mariachi femenino Rosas de Guadalupe
- **Tipo de tarea:** Codificación — **Horas:** 4 — **Responsable:** MIJAEL VILLAVICENCIO RABINES — **Estado:** Finalizada
- **Descripción:** Desarrollar en la página el bloque principal con la información general de la agrupación, destacando que es un mariachi femenino completo de 6 integrantes y presentando la descripción introductoria para el usuario interesado.

#### RS-103 — Diseñar la presentación visual de la sección de información y formatos
- **Tipo de tarea:** Diseño — **Horas:** 3 — **Responsable:** Fabrizio Montero — **Estado:** Finalizada
- **Descripción:** Ajustar el componente o vista para que la información del mariachi, la conformación instrumental y los formatos disponibles se presenten de manera ordenada y entendible en la página Rosas.

#### RS-104 — Incluir los detalles de servicio en la información y catálogo
- **Tipo de tarea:** Codificación — **Horas:** 2 — **Responsable:** Rony Fabrizio Lujan Holguin — **Estado:** Finalizada
- **Descripción:** Agregar en los detalles visibles para el usuario la aclaración de que todos los servicios incluyen movilidad y equipo de sonido propio, de acuerdo con los criterios de aceptación.

#### RS-105 — Publicar los formatos disponibles en el catálogo
- **Tipo de tarea:** Codificación — **Horas:** 3 — **Responsable:** JUAN JOSE TORRES MELGAREJO — **Estado:** Finalizada
- **Descripción:** Agregar en el catálogo la lista de formatos musicales disponibles: Mariachi Completo, Cuarteto, Dúo con pistas y Cantante Solista, asegurando que se muestren como opciones seleccionables o consultables.

#### RS-106 — Mostrar la conformación instrumental de la agrupación
- **Tipo de tarea:** Codificación — **Horas:** 2 — **Responsable:** JUAN JOSE TORRES MELGAREJO — **Estado:** Finalizada
- **Descripción:** Implementar la visualización de los integrantes e instrumentos que conforman el mariachi: 2 trompetas, vihuela, guitarrón y 2 voces, de forma clara y fácil de consultar.

---

## 2. RS-8 — HU04 - Proceso de cotizacion

- **Épica:** RS-78 Cotización, Tarifas y Pagos
- **Story Points:** 5 — **Prioridad cf[10043]:** 4 — **Prioridad Jira:** Highest — **Estado:** En curso

### Descripción
(Texto completo de la descripción en Jira, que incluye sus propias secciones.)

**Resumen**
Como cliente, quiero cotizar el costo total de mi presentación teniendo en cuenta el formato, la duración y la ubicación del evento, para conocer los montos exactos que debo abonar.

**Contexto**
El proceso corresponde a la cotización de una presentación.

**Criterios de aceptación** (sección dentro de la descripción)
- Se debe poder cotizar el costo total de la presentación.
- La cotización debe considerar:
  - el formato,
  - la duración,
  - la ubicación del evento.
- La cotización debe mostrar los montos exactos a abonar.

**Otra información**
HU04 - Proceso de cotizacion

### Criterios de aceptación (campo cf[10045])
1. El usuario selecciona el formato, duración y ubicación de la presentación.
2. El sistema calcula automáticamente el precio del servicio de acuerdo con el formato, duración y ubicación seleccionados.
3. El sistema muestra el monto total del servicio.
4. El sistema desglosa el anticipo obligatorio del 50% para reservar la fecha y el saldo restante del 50%.
5. El usuario selecciona el método de pago y el sistema aplica la comisión correspondiente cuando corresponda.
6. Si el usuario selecciona Tarjeta de Crédito, el sistema agrega automáticamente una comisión adicional del 5% al monto correspondiente.
7. Si el usuario selecciona un método sin comisión adicional, el sistema mantiene el monto calculado sin recargo.
8. Una vez aceptada la cotización, el sistema permite continuar con el proceso de reserva.

### Subtareas

#### RS-112 — Implementar el cálculo automático del costo según formato, duración y ubicación
- **Tipo de tarea:** codificación — **Horas:** 6 — **Responsable:** JUAN JOSE TORRES MELGAREJO — **Estado:** Finalizada
- **Descripción:** Desarrollar la lógica que determine el precio base y calcule automáticamente el monto total del servicio en función de los parámetros seleccionados.

#### RS-113 — Diseñar la interfaz de cotización de la presentación
- **Tipo de tarea:** prototipado — **Horas:** 4 — **Responsable:** Fabrizio Montero — **Estado:** Finalizada
- **Descripción:** Crear la pantalla/formulario donde el cliente pueda seleccionar el formato, la duración y la ubicación del evento, y visualizar el resultado de la cotización.

#### RS-114 — Mostrar el desglose del anticipo y el saldo restante
- **Tipo de tarea:** Codificación — **Horas:** 3 — **Responsable:** unforastero6741 — **Estado:** En curso
- **Descripción:** Presentar al usuario el detalle de pago con el anticipo obligatorio del 50% para reservar la fecha y el 50% restante como saldo pendiente.

#### RS-115 — Aplicar comisión según método de pago seleccionado
- **Tipo de tarea:** codificación — **Horas:** 3 — **Responsable:** MIJAEL VILLAVICENCIO RABINES — **Estado:** Tareas por hacer
- **Descripción:** Incorporar la lógica para agregar recargos cuando corresponda, incluyendo la comisión adicional del 5% si se selecciona Tarjeta de Crédito y sin recargo para métodos exentos de comisión.

#### RS-116 — Validar la aceptación de la cotización para continuar con la reserva
- **Tipo de tarea:** Codificación — **Horas:** 2 — **Responsable:** unforastero6741 — **Estado:** En curso
- **Descripción:** Permitir que, una vez aceptada la cotización, el sistema habilite el flujo para continuar con el proceso de reserva de la presentación.

#### RS-117 — Definir y configurar las reglas de precios por servicio
- **Tipo de tarea:** configuración — **Horas:** 4 — **Responsable:** Rony Fabrizio Lujan Holguin — **Estado:** Finalizada
- **Descripción:** Establecer la tabla o configuración de tarifas base para los distintos formatos, duraciones y ubicaciones, de modo que el cálculo de la cotización sea consistente y mantenible.

---

## 3. RS-95 — HU05 - Reserva

- **Épica:** RS-79 Sistema de Reservas y Gestión de Agenda
- **Story Points:** 8 — **Prioridad cf[10043]:** 4 — **Prioridad Jira:** Medium — **Estado:** En curso

### Descripción
Como cliente, quiero registrar una reserva indicando mis datos, ubicación, fecha y hora del evento, para solicitar una presentación y asegurar un horario disponible.

### Criterios de aceptación
1. El cliente ingresa sus datos de contacto necesarios para la contratación.
2. El cliente selecciona la fecha y hora de la presentación.
3. El cliente ingresa la ubicación o dirección donde se realizará el evento.
4. El sistema consulta la disponibilidad del mariachi para la fecha y hora seleccionadas.
5. El sistema impide seleccionar horarios que se encuentren ocupados.
6. El sistema considera el tiempo necesario para el traslado entre presentaciones al determinar la disponibilidad.
7. La reserva almacena la información del servicio seleccionado, los datos del cliente y los detalles del evento.
8. La reserva permanece pendiente hasta que se valide el pago del anticipo correspondiente.

### Subtareas

#### RS-118 — Diseñar formulario de captura de reserva
- **Tipo de tarea:** diseño — **Horas:** 5 — **Responsable:** Rony Fabrizio Lujan Holguin — **Estado:** Finalizada
- **Descripción:** Crear el formulario para registrar datos de contacto del cliente, ubicación del evento, fecha y hora de la presentación, y servicio seleccionado.

#### RS-119 — Considerar tiempos de traslado entre presentaciones
- **Tipo de tarea:** codificación — **Horas:** 4 — **Responsable:** Rony Fabrizio Lujan Holguin — **Estado:** Tareas por hacer
- **Descripción:** Incorporar el cálculo del tiempo de desplazamiento entre eventos para determinar correctamente la disponibilidad real del mariachi.

#### RS-120 — Bloquear horarios ocupados en la selección de reserva
- **Tipo de tarea:** codificación — **Horas:** 4 — **Responsable:** JUAN JOSE TORRES MELGAREJO — **Estado:** Finalizada
- **Descripción:** Evitar que el cliente pueda seleccionar franjas horarias que ya se encuentren reservadas o no disponibles.

#### RS-121 — Consultar disponibilidad del mariachi por fecha y hora
- **Tipo de tarea:** codificación — **Horas:** 4 — **Responsable:** MIJAEL VILLAVICENCIO RABINES — **Estado:** Tareas por hacer
- **Descripción:** Desarrollar la lógica para verificar si existe disponibilidad para la fecha y hora seleccionadas por el cliente.

#### RS-122 — Implementar validación de datos obligatorios de la reserva
- **Tipo de tarea:** Codificación — **Horas:** 3 — **Responsable:** unforastero6741 — **Estado:** Finalizada
- **Descripción:** Validar que el cliente ingrese los datos mínimos requeridos para la contratación y que los campos del evento tengan formato correcto antes de guardar la reserva.

#### RS-123 — Guardar información completa de la reserva
- **Tipo de tarea:** codificación — **Horas:** 4 — **Responsable:** Fabrizio Montero — **Estado:** Finalizada
- **Descripción:** Persistir en el sistema los datos del cliente, la ubicación del evento, la fecha y hora, el servicio seleccionado y el estado inicial de la reserva.

#### RS-124 — Definir estado pendiente hasta validar anticipo
- **Tipo de tarea:** codificación — **Horas:** 2 — **Responsable:** MIJAEL VILLAVICENCIO RABINES — **Estado:** Finalizada
- **Descripción:** Establecer que la reserva se cree en estado pendiente y permanezca así hasta que se confirme la validación del pago del anticipo.

#### RS-126 — Probar escenarios de disponibilidad y reserva
- **Tipo de tarea:** test — **Horas:** 4 — **Responsable:** JUAN JOSE TORRES MELGAREJO — **Estado:** Finalizada
- **Descripción:** Verificar con pruebas funcionales los casos de reserva disponible, horario ocupado, validación de datos, y consideración del tiempo de traslado.

---

## 4. RS-10 — HU06 - Pago del anticipo

- **Épica:** RS-78 Cotización, Tarifas y Pagos
- **Story Points:** 8 — **Prioridad cf[10043]:** 4 — **Prioridad Jira:** Highest — **Estado:** En curso

### Descripción
Como administradora o cliente, quiero registrar el pago del anticipo del 50% mediante diversos canales financieros, para formalizar y confirmar la reserva de la fecha.

### Criterios de aceptación
1. El cliente selecciona el medio mediante el cual realizará el pago.
2. El sistema admite los métodos de pago definidos por el negocio: efectivo, Yape/Plin, transferencia o depósito bancario y tarjeta de crédito.
3. Para pagos mediante transferencia, depósito o medios digitales que requieran comprobación, el cliente puede registrar el número de operación o comprobante.
4. Si el pago se realiza mediante tarjeta de crédito, el sistema aplica la comisión adicional del 5% correspondiente.
5. El sistema registra el monto abonado y el método de pago utilizado.
6. Una vez validado el pago del 50% del monto correspondiente, la reserva cambia a estado "Confirmada".

### Subtareas

#### RS-127 — Validar el anticipo y actualizar el estado de la reserva
- **Tipo de tarea:** Codificación — **Horas:** 4 — **Responsable:** JUAN JOSE TORRES MELGAREJO — **Estado:** Finalizada
- **Descripción:** Implementar la validación del pago equivalente al 50% del monto de la reserva y, una vez confirmado, cambiar el estado de la reserva a 'Confirmada'.

#### RS-128 — Configurar métodos de pago permitidos para el anticipo
- **Tipo de tarea:** Configuración — **Horas:** 3 — **Responsable:** unforastero6741 — **Estado:** Finalizada
- **Descripción:** Habilitar en el sistema los métodos de pago definidos por negocio: efectivo, Yape/Plin, transferencia o depósito bancario y tarjeta de crédito, mostrando solo opciones válidas durante el registro del anticipo.

#### RS-129 — Aplicar comisión del 5% para pagos con tarjeta de crédito
- **Tipo de tarea:** Codificación — **Horas:** 2 — **Responsable:** unforastero6741 — **Estado:** Finalizada
- **Descripción:** Calcular automáticamente la comisión adicional correspondiente al 5% cuando el anticipo se registre como pago con tarjeta de crédito, ajustando el total a registrar.

#### RS-130 — Implementar formulario de registro del anticipo
- **Tipo de tarea:** Codificación — **Horas:** 5 — **Responsable:** Rony Fabrizio Lujan Holguin — **Estado:** Finalizada
- **Descripción:** Crear la interfaz para que administradora o cliente seleccione el medio de pago del anticipo, ingrese el monto abonado y registre los datos requeridos según el método elegido.

#### RS-131 — Registrar número de operación o comprobante para pagos que lo requieran
- **Tipo de tarea:** Codificación — **Horas:** 3 — **Responsable:** Fabrizio Montero — **Estado:** Finalizada
- **Descripción:** Permitir adjuntar o ingresar el número de operación/comprobante para pagos por transferencia, depósito o medios digitales que necesiten validación posterior.

#### RS-137 — Diseñar modelo de pagos, anticipos y estados
- **Tipo de tarea:** Análisis y diseño — **Horas:** 2 — **Responsable:** unforastero6741 — **Estado:** Finalizada
- **Descripción:** (vacía en Jira — sin descripción)

#### RS-138 — Probar registro y validación del anticipo
- **Tipo de tarea:** Test — **Horas:** 3 — **Responsable:** unforastero6741 — **Estado:** En curso
- **Descripción:** (vacía en Jira — sin descripción)

---

## 5. RS-12 — HU08 - Gestion de calendario y reservas

- **Épica:** RS-79 Sistema de Reservas y Gestión de Agenda
- **Story Points:** 5 — **Prioridad cf[10043]:** 3 — **Prioridad Jira:** High — **Estado:** En curso

### Descripción
Como administradora, quiero consultar una agenda gráfica en formato calendario, para organizar las fechas del mariachi y evitar cruces de horario.

### Criterios de aceptación
1. Se visualiza el calendario mensual o semanal, se muestran las presentaciones agendadas identificadas por colores según su estado.
2. Cuando se intenta ingresar una nueva presentación y el horario coincide o deja menos de 45 minutos de margen de traslado con otro evento el sistema bloquea el registro por solapamiento logístico.

### Subtareas

#### RS-55 — Mostrar mensaje de bloqueo cuando exista conflicto de agenda
- **Tipo de tarea:** Codificación — **Horas:** 3 — **Responsable:** JUAN JOSE TORRES MELGAREJO — **Estado:** Finalizada
- **Descripción:** Definir y presentar una notificación clara al intentar crear una presentación rechazada por solapamiento una capacidad logística, indicando el motivo del bloqueo.

#### RS-56 — Validar solapamientos y margen mínimo de traslado antes de registrar una presentación
- **Tipo de tarea:** Codificación — **Horas:** 5 — **Responsable:** MIJAEL VILLAVICENCIO RABINES — **Estado:** Finalizada
- **Descripción:** Agregar la regla de negocio que bloquee nuevas reservas cuando coincidan en horario con otra presentación o cuando dejen menos de 45 minutos entre eventos por traslado logístico.

#### RS-57 — Implementar la consulta de reservas y presentaciones para el calendario
- **Tipo de tarea:** Codificación — **Horas:** 4 — **Responsable:** Rony Fabrizio Lujan Holguin — **Estado:** Tareas por hacer
- **Descripción:** Desarrollar la lógica de obtención de eventos agendados para alimentar la vista de calendario con los datos necesarios de fechas, horas y estado.

#### RS-58 — Diseñar la vista de calendario mensual y semanal
- **Tipo de tarea:** Prototipado — **Horas:** 6 — **Responsable:** Fabrizio Montero — **Estado:** Tareas por hacer
- **Descripción:** Crear la interfaz de agenda gráfica para administradora con navegación entre vista mensual y semanal, alineada a la organización de presentaciones del mariachi.

#### RS-59 — Listar presentaciones agendadas en el calendario con codificación por color
- **Tipo de tarea:** Codificación — **Horas:** 4 — **Responsable:** unforastero6741 — **Estado:** En curso
- **Descripción:** Mostrar los eventos del calendario identificando cada presentación según su estado mediante colores, conforme a los criterios de aceptación.

#### RS-60 — Probar la visualización del calendario y la regla de no solapamiento
- **Tipo de tarea:** Test — **Horas:** 4 — **Responsable:** MIJAEL VILLAVICENCIO RABINES — **Estado:** Finalizada
- **Descripción:** Verificar mediante pruebas funcionales que el calendario muestre correctamente los eventos y que la validación bloquee reservas conflictivas según la regla de 45 minutos.

---

## 6. RS-15 — HU11 - Configuracion de la presentacion

- **Épica:** RS-77 Catálogo Digital y Repertorio Musical
- **Story Points:** 3 — **Prioridad cf[10043]:** 4 — **Prioridad Jira:** Highest — **Estado:** En curso

### Descripción
Como cliente, quiero seleccionar el formato de la agrupación, la ocasión del evento, la duración del show e ingresar dedicatorias, para configurar la presentación musical de acuerdo con mis necesidades.

### Criterios de aceptación
1. El usuario selecciona el formato de presentación entre las opciones disponibles: Mariachi Completo, Cuarteto, Dúo con pistas o Cantante Solista.
2. El usuario selecciona el tiempo de presentación; las opciones válidas son 30 minutos, 40 minutos o 1 hora.
3. Cuando se despliega la lista de ocasiones, se permite seleccionar: Serenata, Boda, Cumpleaños, 15 Años, Aniversario, Fiesta Patronal, Misa o Ceremonia de honras/responso.
4. Si el cliente tiene canciones preferidas o indicaciones especiales, puede escribirlas en el campo de dedicatorias/observaciones.
5. Las preferencias y observaciones ingresadas se almacenan en el registro del evento.

### Subtareas

#### RS-107 — Cargar las opciones permitidas de formato, ocasión y duración
- **Tipo de tarea:** Codificación — **Horas:** 3 — **Responsable:** Rony Fabrizio Lujan Holguin — **Estado:** Finalizada
- **Descripción:** Configurar las listas desplegables con las opciones válidas: Mariachi Completo, Cuarteto, Dúo con pistas, Cantante Solista; Serenata, Boda, Cumpleaños, 15 Años, Aniversario, Fiesta Patronal, Misa, Ceremonia de honras/responso; y 30 minutos, 40 minutos, 1 hora.

#### RS-108 — Validar la selección y los campos opcionales de la presentación
- **Tipo de tarea:** Codificación — **Horas:** 3 — **Responsable:** JUAN JOSE TORRES MELGAREJO — **Estado:** Finalizada
- **Descripción:** Asegurar que las selecciones realizadas correspondan únicamente a valores permitidos y que el campo de dedicatorias/observaciones acepte texto libre para canciones preferidas o indicaciones especiales.

#### RS-109 — Diseñar el formulario de configuración de presentación
- **Tipo de tarea:** Prototipado — **Horas:** 5 — **Responsable:** JUAN JOSE TORRES MELGAREJO — **Estado:** Finalizada
- **Descripción:** Crear en la interfaz la sección para seleccionar formato de agrupación, ocasión del evento, duración del show y el campo de dedicatorias/observaciones.

#### RS-110 — Probar la configuración de presentación y el guardado de datos
- **Tipo de tarea:** Test — **Horas:** 3 — **Responsable:** unforastero6741 — **Estado:** En curso
- **Descripción:** Verificar que el formulario permita seleccionar correctamente las opciones, registrar observaciones y almacenar la información en el evento sin pérdida de datos.

#### RS-111 — Guardar la configuración de presentación en el registro del evento
- **Tipo de tarea:** Codificación — **Horas:** 4 — **Responsable:** Fabrizio Montero — **Estado:** Finalizada
- **Descripción:** Persistir en el backend las preferencias seleccionadas por el cliente para que queden asociadas al evento y puedan consultarse posteriormente.

---

## 7. RS-82 — HU13 - Sesion de administracion

- **Épica:** RS-140 Administración y Seguridad del Sistema
- **Story Points:** 5 — **Prioridad cf[10043]:** 3 — **Prioridad Jira:** Medium — **Estado:** En curso

### Descripción
Como administradora, quiero iniciar sesión de forma segura para acceder a las funciones de gestión de Rosas de Guadalupe.

### Criterios de aceptación
1. La administradora ingresa sus credenciales (usuario/correo y contraseña) en la pantalla de acceso, el sistema valida los datos y concede el ingreso exitoso al panel de gestión de Rosas de Guadalupe.
2. Si se ingresan credenciales incorrectas o campos vacíos, el sistema bloquea el ingreso y muestra mensajes de error y retroalimentación claros sin exponer información sensible.
3. Tras un inicio de sesión exitoso, el sistema gestiona y mantiene una sesión segura con caducidad por inactividad para proteger las operaciones administrativas.
4. Si un usuario no autenticado intenta acceder a rutas o funciones protegidas de administración, el sistema restringe el acceso de forma automática y lo redirige a la pantalla de inicio de sesión.
5. Cuando la administradora selecciona la opción de cerrar sesión, el sistema destruye la sesión activa de forma segura y redirige a la vista principal/login, impidiendo el reingreso mediante la navegación del historial.

### Subtareas

#### RS-132 — Restringir rutas y funciones administrativas a usuarios autenticados
- **Tipo de tarea:** Codificación — **Horas:** 4 — **Responsable:** JUAN JOSE TORRES MELGAREJO — **Estado:** Finalizada
- **Descripción:** Agregar protección de acceso para redirigir automáticamente a la pantalla de inicio de sesión cuando un usuario no autenticado intente entrar a rutas o funciones de administración.

#### RS-133 — Gestionar sesión segura con expiración por inactividad
- **Tipo de tarea:** Codificación — **Horas:** 3 — **Responsable:** unforastero6741 — **Estado:** En curso
- **Descripción:** Configurar la creación y mantenimiento de la sesión autenticada, incluyendo caducidad automática por inactividad y mecanismos para proteger las operaciones administrativas.

#### RS-134 — Implementar cierre de sesión seguro
- **Tipo de tarea:** Codificación — **Horas:** 2 — **Responsable:** Rony Fabrizio Lujan Holguin — **Estado:** Finalizada
- **Descripción:** Desarrollar la funcionalidad para destruir la sesión activa de forma segura, redirigir a la vista principal o login e impedir el reingreso mediante el historial de navegación.

#### RS-135 — Crear pantalla de inicio de sesión de administración
- **Tipo de tarea:** Prototipado — **Horas:** 4 — **Responsable:** unforastero6741 — **Estado:** Finalizada
- **Descripción:** Diseñar e implementar la vista/formulario para que la administradora ingrese usuario o correo y contraseña, incluyendo estados de carga, errores y validaciones básicas de campos vacíos.

#### RS-136 — Implementar validación de credenciales y autenticación segura
- **Tipo de tarea:** Codificación — **Horas:** 5 — **Responsable:** Fabrizio Montero — **Estado:** En curso
- **Descripción:** Desarrollar la lógica de backend para verificar las credenciales, autenticar a la administradora y devolver mensajes de error claros sin exponer información sensible.

#### RS-139 — Probar inicio, expiración y cierre de sesión
- **Tipo de tarea:** Test — **Horas:** 2 — **Responsable:** unforastero6741 — **Estado:** En curso
- **Descripción:** (vacía en Jira — sin descripción)

---

## 8. Resumen de subtareas por tipo de tarea (cf[10046])

| Tipo (sin distinguir mayúsculas) | Cantidad | Horas | Subtareas |
|---|---|---|---|
| Codificación | 29 | 100 | RS-102, 104, 105, 106, 112, 114, 115, 116, 119, 120, 121, 122, 123, 124, 127, 129, 130, 131, 55, 56, 57, 59, 107, 108, 111, 132, 133, 134, 136 |
| Test | 5 | 16 | RS-126, 138, 60, 110, 139 |
| Prototipado | 4 | 19 | RS-113, 58, 109, 135 |
| Configuración | 2 | 7 | RS-117, 128 |
| Análisis y diseño | 1 | 2 | RS-137 |
| Implantación | 0 | 0 | — |
| "Diseño" (no es una de las 6 categorías oficiales) | 2 | 8 | RS-103, 118 |
| **Total** | **43** | **152** | |

## 9. Observaciones de calidad de datos

- RS-137, RS-138 y RS-139 no tienen descripción en Jira.
- RS-103 y RS-118 usan el tipo "Diseño"/"diseño", que no está entre las 6 categorías oficiales.
- cf[10046] es texto libre: 11 subtareas tienen el valor en minúscula (RS-112, 113, 115, 117, 118, 119, 120, 121, 123, 124, 126).
- La descripción de RS-8 incluye su propia sección "Criterios de aceptación", distinta del campo cf[10045].
- RS-95 y RS-82 tienen prioridad cf[10043] alta (4 y 3) pero prioridad nativa de Jira "Medium".
- Las 7 historias no tienen responsable asignado; todas las subtareas sí lo tienen.
