# Marco Ágil y Gestión del Proyecto (Scrum)

## 1. Parámetros del Proyecto en Jira

- **Clave del Proyecto en Jira**: `RS` (*Rosas de Guadalupe Software*)
- **Marco de Trabajo**: Scrum
- **Duración del Sprint**: 2 semanas (10 días hábiles)
- **Tamaño del Equipo de Desarrollo**: 5 Desarrolladores Full-Stack
- **Velocidad Estimada**: 20 Story Points (SP) por Sprint

## 2. Eventos y Ceremonias

| Ceremonia | Frecuencia | Duración Máxima | Objetivo |
| :--- | :--- | :--- | :--- |
| **Sprint Planning** | Inicio de Sprint (Lunes) | 2 horas | Seleccionar y estimar PBIs del backlog hasta completar los 20 SP. |
| **Daily Scrum** | Diario | 15 min | Sincronización del equipo: qué hice ayer, qué haré hoy, bloqueos. |
| **Sprint Review** | Fin de Sprint (Viernes) | 1 hora | Demostración en vivo de incrementos terminados al Product Owner. |
| **Retrospectiva** | Fin de Sprint (Viernes) | 45 min | Mejora continua del equipo (acciones de mejora para el próximo sprint). |

## 3. Definición de Hecho (Definition of Done - DoD)

Una Historia de Usuario se considera **Done** cuando:
1. El código cumple con los estándares de estilo del proyecto (PEP 8 en Python, ESLint/Prettier).
2. Los scripts de base de datos Oracle asociados están creados y probados en `database/scripts/`.
3. Pasa pruebas unitarias locales.
4. Pasa revisión de código (Pull Request aprobado por al menos 1 compañero).
5. Desplegado y verificado en el entorno de pruebas local.
