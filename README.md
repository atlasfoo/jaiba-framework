# 🦀 JAIBA

**Joint-operations Artificial Intelligence Behavioral Architecture**

> *Un framework para desarrollo de software asistido por agentes de IA semiautónomos, diseñado para que el humano siempre esté en el ciclo.*

---

[![Framework](https://img.shields.io/badge/framework-agentic--dev-blue?style=flat-square)](.)
[![Paradigm](https://img.shields.io/badge/paradigm-spec--driven-orange?style=flat-square)](.)
[![Human in the loop](https://img.shields.io/badge/human-in%20the%20loop-green?style=flat-square)](.)
[![Greenfield](https://img.shields.io/badge/scope-greenfield%20%2B%20brownfield-purple?style=flat-square)](.)

---

## ¿Qué es JAIBA?

JAIBA es un framework de desarrollo ágil diseñado para equipos que trabajan con agentes de IA como copiloto en la construcción de software. No es una herramienta, ni un modelo de IA, ni un conjunto de prompts sueltos: es una **arquitectura de comportamiento** que define cómo organizar el contexto, cómo orquestar flujos de trabajo y cómo mantener al humano como decisor central en cada etapa significativa del desarrollo.

JAIBA parte de una premisa simple: **el código es el contexto**, y el agente debe entender el proyecto como lo entendería un desarrollador senior que lleva semanas trabajando en él.

### Principios fundamentales

| Principio | Descripción |
|---|---|
| 🧠 **Código como contexto** | El agente trabaja sobre la base real del proyecto: arquitectura, decisiones, dependencias y convenciones vivas en el repositorio. El contexto no se improvisa, se construye y se mantiene. |
| 👤 **Humano en el ciclo** | Ningún cambio significativo ocurre sin validación humana. El agente propone, razona y ejecuta tareas acotadas; el desarrollador aprueba, redirige y decide. |
| 📚 **Aprendizaje continuo** | El sistema está diseñado para capturar conocimiento: cada decisión arquitectónica, cada integración, cada cambio relevante queda registrado para alimentar futuros ciclos. |
| 🌱 **Greenfield y brownfield** | JAIBA funciona en proyectos nuevos desde cero y en sistemas legados existentes. El proceso de construcción del cerebro permite al agente adaptarse a cualquier base de código. |

---

## Arquitectura del sistema

JAIBA organiza su funcionamiento en dos capas: la **estructura de memoria** (el cerebro del agente) y la **librería de skills** (los flujos de trabajo ejecutables).

```
proyecto/
├── AGENTS.md                           ← Directrices de comportamiento del agente
├── .ai/                                ← Cerebro del agente
│   ├── memory/                         ← Memoria a largo plazo
│   │   ├── constitution.md             ← Resumen ejecutivo del proyecto
│   │   ├── adr-log.md                  ← Historial de decisiones arquitectónicas
│   │   ├── reference-index.md          ← Índice de dependencias y APIs externas
│   │   └── archive/                    ← Resúmenes archivados de planes cerrados
│   │       └── plans/
│   │           └── YYYY-MM-DD-slug.md
│   ├── specs/                          ← Memoria a mediano plazo
│   │   └── [nombre-de-spec]/
│   │       ├── PRD.md                  ← Requerimiento de negocio formalizado
│   │       └── user-stories.md         ← Checklist de historias de usuario
│   └── session/                        ← Memoria a corto plazo
│       ├── plan.md                     ← Plan activo
│       ├── tasks.md                    ← Checklist de tareas
│       ├── walkthrough.md              ← Bitácora de la sesión
│       └── <slug>-summary.md           ← Resumen del plan, hasta que cleanup lo archive
└── src/ ...                            ← Tu proyecto
```

---

## 🧠 Estructura de memoria: el cerebro del agente

La carpeta `.ai/` es el núcleo de JAIBA. Funciona como la memoria persistente del agente, dividida en tres horizontes temporales: largo, mediano y corto plazo.

---

### `AGENTS.md` — Directrices de comportamiento

Ubicado en la raíz del proyecto, `AGENTS.md` es el punto de entrada del agente: el archivo que define **cómo debe comportarse**, qué herramientas puede usar, qué convenciones debe respetar y cómo debe interactuar con el humano.

Su rol es de **configuración de comportamiento, no de contexto de proyecto**. La información del proyecto (arquitectura, stack, decisiones) vive en `.ai/memory/constitution.md`. `AGENTS.md` apunta hacia allá y se mantiene deliberadamente corto, estableciendo solo las reglas de operación.

Estructura típica de un `AGENTS.md` en JAIBA:

```markdown
# AGENTS.md

## Comportamiento general
- Actúa siempre dentro del skill activo y su modo declarado
- No modifiques código fuera del alcance acordado en el plan o spec activos
- Ante la duda, usa `skill: ask` antes de ejecutar

## Contexto del proyecto
El contexto completo del proyecto (arquitectura, stack, convenciones y dependencias)
está en `.ai/memory/constitution.md`. Léelo al inicio de cada sesión.

## Memoria y aprendizaje
- Consulta `.ai/memory/` antes de proponer soluciones
- Registra decisiones relevantes en `session/walkthrough.md`
- Propón actualizaciones al cerebro al cerrar planes o specs

## Restricciones
- No instales dependencias nuevas sin aprobación humana explícita
- No hagas commits ni push de forma autónoma (si el desarrollador lo pide, sí)
- Mantén el alcance acordado; si detectas trabajo fuera de él, notifica antes de proceder
```

> `AGENTS.md` es el contrato de operación del agente con el equipo. Debe ser la primera lectura de cualquier agente que se incorpore al proyecto.

---

### `memory/` — Memoria a largo plazo

Contiene el conocimiento estructural y permanente del proyecto. Es lo primero que el agente consulta al iniciar cualquier flujo.

#### `constitution.md`
El **resumen ejecutivo** del proyecto. Responde las preguntas más importantes sobre el sistema de un vistazo:

- ¿Qué hace este proyecto y para quién?
- ¿Cuál es su stack tecnológico y arquitectura?
- ¿Cuáles son las convenciones y reglas de alcance del equipo?
- ¿Cómo interactúa con sistemas externos?
- ¿Cuál es la postura del proyecto respecto a TDD y otras convenciones de planning?

> Es el equivalente al README técnico que un desarrollador nuevo debería leer antes de hacer su primer commit.

#### `adr-log.md`
El **historial de decisiones arquitectónicas** del proyecto (Architecture Decision Records). Cada entrada registra:

- La decisión tomada
- El contexto que la motivó
- Las alternativas consideradas
- Las consecuencias esperadas

> Permite al agente entender *por qué* el proyecto es como es, no solo *cómo* es.

#### `reference-index.md`
El **índice de dependencias externas**: APIs integradas, paquetes clave, servicios de terceros y librerías importantes. Para cada entrada documenta su propósito, dónde está configurada y cómo se usa dentro del proyecto.

> Evita que el agente "reinvente" integraciones que ya existen o use versiones incorrectas.

#### `archive/plans/`
**Resúmenes archivados** de los planes ya cerrados. Cada archivo es la salida del skill `planning:summarize`, archivada por el modo `cleanup` con el formato `YYYY-MM-DD-<slug>.md`. Funcionan como bitácora histórica del proyecto: un desarrollador (humano o agente) puede recorrer este directorio para entender qué se hizo, cuándo y por qué, sin tener que reconstruirlo de los commits.

> Los resúmenes se escriben para ser concisos por diseño — el detalle vivo está en el `walkthrough.md` durante la sesión; lo que sobrevive al cierre es la versión destilada.

---

### `specs/` — Memoria a mediano plazo

Almacena las especificaciones activas del proyecto, generadas a través del flujo **Specification**. Cada spec vive en su propia carpeta y representa una unidad de trabajo orientada a un requerimiento de negocio.

```
specs/
└── autenticacion-oauth/
    ├── PRD.md              ← Requerimiento de negocio formalizado
    └── user-stories.md     ← Checklist de historias de usuario
```

#### `PRD.md` (Product Requirements Document)
Define el **qué y el por qué** del requerimiento: el problema de negocio, los criterios de aceptación, los supuestos y las restricciones.

#### `user-stories.md`
Descompone el PRD en **historias de usuario concretas** con criterios de aceptación claros. Funciona como checklist de progreso durante la implementación.

> Una spec puede abarcar múltiples sesiones de trabajo. Permanece activa hasta ser archivada o completada.

---

### `session/` — Memoria a corto plazo

Contiene los artefactos del flujo **Planning**: el contexto de trabajo inmediato de una sesión o sprint acotado. Es independiente del flujo Specification y se enfoca en la ejecución táctica.

#### `plan.md`
El plan de trabajo activo: objetivo de la sesión, contexto relevante y alcance acordado con el humano.

#### `tasks.md`
La lista de tareas concretas derivadas del plan, organizada en **fases con cohesión arquitectónica**. Cada fase declara sus dependencias y deja el código en un estado reversible y construible (apto para un commit `chore(wip)` si el desarrollador así lo prefiere).

#### `walkthrough.md`
El registro narrativo de la sesión: decisiones tomadas, problemas encontrados y razonamientos del agente. Se actualiza al cerrar cada fase, no tarea por tarea. Sirve como bitácora para revisión humana y como fuente para construir el resumen final.

#### `<slug>-summary.md`
El resumen del plan, producido por `planning:summarize` cuando todas las tareas están completas. Vive temporalmente en `session/` para que el desarrollador pueda revisarlo junto al resto del material de la sesión, y luego es movido a `.ai/memory/archive/plans/` por el modo `cleanup`.

> Los archivos de `session/` son **efímeros**: al ejecutar `planning:cleanup`, el summary se archiva en `memory/` y los demás archivos se eliminan, dejando el espacio listo para el próximo plan.

---

## ⚙️ Skills: los flujos de trabajo

Los skills son las capacidades ejecutables del agente dentro de JAIBA. Cada skill implementa un flujo de trabajo específico con modos bien definidos, transiciones claras y puntos de validación humana.

---

### 📋 `skill: planning`

El flujo táctico de trabajo. Diseñado para tareas concretas que no requieren una especificación formal completa, pero sí organización y trazabilidad.

| Modo | Descripción |
|---|---|
| **`define`** | El agente colabora con el humano para definir el objetivo, el alcance y las tareas del plan. Investiga el código, detecta discrepancias entre el prompt/spec y la realidad del repositorio, pregunta para resolverlas y genera `plan.md` y `tasks.md`. |
| **`execute`** *(implícito)* | El agente trabaja sobre las tareas del plan activo, fase por fase. No requiere invocación explícita: se activa cuando hay un plan aprobado y el mensaje del desarrollador es una señal de continuación (`continúa`, `sigue`, `next`, `avanza`). Actualiza `tasks.md` y `walkthrough.md`, sugiere un commit `chore(wip)` al cierre de cada fase y se detiene en cada frontera de fase para revisión humana. |
| **`summarize`** | El agente cierra el plan: produce `<slug>-summary.md` con el resultado destilado del trabajo, evalúa si alguna decisión amerita una entrada de ADR (la propone, no la escribe), y sugiere un mensaje de commit final tipo conventional commit. |
| **`cleanup`** | El agente archiva el summary en `.ai/memory/archive/plans/<YYYY-MM-DD>-<slug>.md` y vacía `.ai/session/`. Es destructivo: requiere confirmación humana explícita. |

> **Reglas de oro del planning:**
> - El humano debe aprobar el plan antes de que el agente entre en modo `execute`. Nada se ejecuta sin un plan validado.
> - Antes de cada fase de `execute`, el agente revisa el `git status` y sugiere arrancar con un worktree limpio.
> - `summarize` y `cleanup` son pasos separados a propósito: el desarrollador debe poder leer el resumen antes de que se destruya la sesión.

---

### 📐 `skill: specification`

El flujo de desarrollo guiado por especificación. Para requerimientos de mayor complejidad o alcance que necesitan ser formalizados antes de implementarse.

| Modo | Descripción |
|---|---|
| **`brainstorm`** | Exploración abierta del requerimiento. El agente hace preguntas, identifica ambigüedades y ayuda a clarificar el problema de negocio. |
| **`define`** | Formalización de la spec: el agente redacta el `PRD.md` y el `user-stories.md` en base al brainstorm validado por el humano. |
| **`resolve`** | Modo consulta dentro de una spec activa: el humano puede hacer preguntas sobre el alcance, y el agente responde sin modificar código. |
| **`archive`** | Cierre formal de la spec: se marca como completada, se archiva su carpeta y se promueve conocimiento relevante a `memory/`. |

> Una spec bien definida es la mejor inversión antes de escribir una sola línea de código.

---

### 🔄 `skill: update-brain`

El flujo de mantenimiento del conocimiento. Actualiza los archivos de `memory/` a partir de análisis del proyecto o como respuesta a cambios significativos.

**Casos de uso:**

- **Inicialización:** El agente analiza el repositorio existente (código, README, configs, documentación) y genera los archivos de `memory/` por primera vez. Fundamental para onboarding en proyectos brownfield.
- **Mantenimiento estructural:** Cuando el proyecto evoluciona significativamente (nuevos módulos, nuevas integraciones, cambios de arquitectura), se re-analiza y actualiza `constitution.md` y `reference-index.md`.
- **Aplicación de ADRs propuestos:** Toma los ADRs propuestos por `planning:summarize` o `specification:archive` y los integra en `adr-log.md` tras validación humana.

> El cerebro es tan útil como tan actualizado esté. **Update Brain** es el skill que cierra el ciclo de aprendizaje a nivel proyecto, complementando los cierres individuales que hacen `planning:summarize` y `specification:archive`.

---

### ⚡ `skill: fast`

Ejecución directa sin planificación formal. Para tareas pequeñas, bien definidas y de bajo riesgo donde el overhead de crear un plan no se justifica.

- El agente actúa directamente sobre la solicitud del humano
- Registra un resumen mínimo en `walkthrough.md`
- No genera `plan.md` ni `tasks.md`

> Úsalo con criterio. Si la tarea tiene más de 2-3 pasos o toca múltiples archivos, considera usar **planning** en su lugar.

---

### 💬 `skill: ask`

Modo consulta pura. El agente responde preguntas, explica código, analiza arquitectura o evalúa opciones **sin modificar nada**.

- El agente no escribe ni edita código
- Puede consultar archivos del proyecto para dar respuestas contextualizadas
- Ideal para pair-programming conceptual, revisiones y toma de decisiones

> Separar el modo consulta del modo ejecución evita cambios accidentales y mantiene la intención del humano clara.

---

## Flujo de trabajo típico

```
                    ┌─────────────────────────────┐
                    │     Proyecto nuevo o legado  │
                    └──────────────┬──────────────┘
                                   │
                          skill: update-brain
                        (construir el cerebro)
                                   │
                    ┌──────────────▼──────────────┐
                    │        .ai/memory/ listo     │
                    └──────────────┬──────────────┘
                                   │
               ┌───────────────────┼───────────────────┐
               │                   │                   │
    Requerimiento            Tarea concreta        Pregunta /
    de negocio                 o fix               Exploración
               │                   │                   │
    skill: specification    skill: planning        skill: ask
    (brainstorm → define)   (define → execute      (respuesta sin
               │             → summarize            modificar)
               │             → cleanup)
               │                   │
               └─────────┬─────────┘
                         │
                skill: update-brain
               (consolidar aprendizajes
                a nivel proyecto)
                         │
                    ┌────▼────┐
                    │  repeat  │
                    └─────────┘
```

---

## Filosofía de diseño

### El agente como copiloto, no como piloto

JAIBA no busca automatizar el desarrollo. Busca amplificar la capacidad del desarrollador manteniendo la autoría humana sobre las decisiones que importan. El agente es un colaborador extraordinariamente productivo que necesita dirección, contexto y validación.

### La memoria como ciudadano de primera clase

El código fuente y los archivos `.ai/` son igualmente parte del proyecto. La memoria del agente no es un archivo temporal o un prompt desechable: es un artefacto de equipo que vive en el repositorio, evoluciona con el proyecto y es legible por cualquier colaborador humano.

### Los flujos como contratos

Cada skill define expectativas claras para el agente y para el humano. Saber en qué modo está operando el agente elimina ambigüedad y reduce errores por malentendidos de contexto.

---

## Ejemplos de uso

Los siguientes ejemplos están basados en **TripNest**, una aplicación de planificación de viajes construida con Python y Django. Ilustran los tres ciclos principales de trabajo en JAIBA.

---

### Ejemplo 1 — `skill: specification` · Requerimiento nuevo

El equipo quiere agregar un módulo de itinerarios colaborativos. Es un requerimiento con múltiples aristas de negocio, así que se inicia con una spec.

**Brainstorm:**
> 👤 *"Quiero que los usuarios puedan crear itinerarios y compartirlos con otras personas para que las editen juntos."*

El agente hace preguntas para acotar: ¿edición en tiempo real o asíncrona? ¿cualquier usuario puede editar o hay roles dentro del itinerario? ¿qué pasa si dos personas editan el mismo día del viaje a la vez?

**Define:**
El agente redacta `.ai/specs/itinerarios-colaborativos/PRD.md`:

```markdown
## Problema de negocio
Los usuarios necesitan coordinar planes de viaje con acompañantes sin
depender de herramientas externas (WhatsApp, Google Docs). Hoy no hay
forma de co-editar un itinerario dentro de TripNest.

## Solución propuesta
Agregar un sistema de colaboración por invitación sobre itinerarios
existentes, con roles (propietario / editor / lector) y control de
conflictos optimista (last-write-wins con historial de cambios).

## Criterios de aceptación
- El propietario puede invitar colaboradores por email
- Los editores pueden agregar, modificar y eliminar días y actividades
- Los lectores solo visualizan
- Los cambios se reflejan en menos de 5 segundos para todos los colaboradores activos
- El sistema registra quién hizo cada cambio
```

Y el `user-stories.md` resultante incluye historias como:
- `[ ]` Como propietario, quiero invitar a un colaborador por email para que pueda editar mi itinerario
- `[ ]` Como editor, quiero agregar una actividad a un día del itinerario
- `[ ]` Como lector, quiero ver el itinerario en modo solo lectura sin poder modificarlo
- `[ ]` Como propietario, quiero ver el historial de cambios de mi itinerario

**Resolve:**
Durante el desarrollo surge una duda: ¿el sistema de permisos debe integrarse con el sistema de autenticación existente o manejarse de forma independiente?

> 👤 *"¿Los roles de colaborador deben usar el sistema de permisos que ya tenemos con `django-guardian`?"*

El agente consulta `.ai/memory/reference-index.md`, confirma que `django-guardian` ya está integrado para permisos de objetos, y responde con una recomendación fundamentada **sin tocar código**.

---

### Ejemplo 2 — `skill: planning` dentro de una spec activa

Con la spec de itinerarios colaborativos aprobada, el equipo inicia la primera sesión de implementación: el modelo de datos y los permisos base.

**Define:**

> 👤 *"Arrancamos con la spec de itinerarios colaborativos. Quiero implementar el modelo de colaboradores y la lógica de permisos con django-guardian."*

El agente lee `.ai/specs/itinerarios-colaborativos/user-stories.md`, revisa el código (descubriendo que `Itinerary` usa `created_by` en lugar de `owner`, discrepancia que aclara con el desarrollador antes de seguir), y propone el siguiente `plan.md`:

```markdown
## Plan: Modelo de colaboradores e integración de permisos
**Spec activa:** itinerarios-colaborativos
**Historias cubiertas:**
- Invitar colaborador por email
- Asignar rol (propietario / editor / lector)

## Tareas (TDD activo)
Phase 1 — Domain model (reversible)
- [ ] Test fallido para creación de ItineraryCollaborator y validación de rol
- [ ] Implementar ItineraryCollaborator (FK a Itinerary y User, role CharField con choices)
- [ ] Migración
- [ ] Test fallido para permisos por rol
- [ ] Wire django-guardian (view/change/delete por rol)
```

> 👤 *"Aprobado, adelante."*

**Execute *(implícito en "continúa")*:**
El agente verifica `git status` (limpio), implementa la fase tarea por tarea respetando el orden TDD, actualiza `tasks.md` con el progreso, y al cierre de la fase escribe en `walkthrough.md`:

```markdown
## Phase 1 — Domain model   2026-05-26

**Outcome.** Modelo ItineraryCollaborator operativo con permisos por
rol usando django-guardian. Migración aplicada.

**Decisions.**
- role como CharField con choices (owner/editor/reader): los roles son
  fijos, no se espera extensibilidad en el corto plazo. Si se necesitan
  roles dinámicos en el futuro, se migrará a tabla separada.

**Quality gate.** Pass.
```

Y sugiere el commit `chore(wip): domain model for itinerary collaborators`, sin ejecutarlo. Hace una pausa.

**Summarize *(al cierre del plan)*:**
Cuando todas las fases están completas, el desarrollador dice *"cerremos esto"*. El agente produce `itinerarios-colaborativos-modelo-base-summary.md`, marca las historias correspondientes en `user-stories.md` como `[x]`, propone una entrada de ADR sobre la elección de `CharField` para `role`, y sugiere un commit final tipo `feat(itineraries): collaborator invitations with role-based access`.

**Cleanup:**
> 👤 *"adelante, limpia"*

El agente ejecuta `scripts/cleanup.sh` del skill, archivando el summary en `.ai/memory/archive/plans/2026-05-26-itinerarios-colaborativos-modelo-base.md` y vaciando `session/`.

---

### Ejemplo 3 — `skill: planning` independiente (fuera de spec)

Durante una revisión de código, el equipo detecta que las queries de itinerarios están generando problemas de N+1. No hay una spec abierta para esto: es una tarea técnica puntual.

**Define:**

> 👤 *"Tenemos un problema de N+1 en la vista de lista de itinerarios. Hay que optimizar las queries."*

El agente revisa el código relevante y propone:

```markdown
## Plan: Optimización de queries en listado de itinerarios

## Contexto
La vista `ItineraryListView` carga itinerarios con sus colaboradores y
actividades de forma lazy, generando N+1 queries por itinerario.

## Tareas
Phase 1 — Profiling (reversible)
- [ ] Test de regresión que cuenta queries con assertNumQueries
- [ ] Perfilar con django-debug-toolbar y documentar conteo base

Phase 2 — Fix (depends on: Phase 1)
- [ ] Agregar select_related('owner') y prefetch_related('collaborators', 'days__activities')
- [ ] Ajustar serializer si corresponde
- [ ] Verificar que assertNumQueries baja al rango esperado
```

**Execute → Summarize → Cleanup:**
El agente implementa los cambios fase por fase, verifica la reducción de queries y resume con un commit sugerido tipo `perf(itineraries): eliminate N+1 in list view`. Al tratarse de una optimización sin impacto en arquitectura, el summary indica explícitamente *"No ADR proposed; all decisions were tactical."*

---

## Glosario

| Término | Definición |
|---|---|
| **Cerebro** | El conjunto de archivos en `.ai/` que conforman el contexto persistente del agente |
| **Spec** | Una especificación formal de un requerimiento de negocio, con PRD e historias de usuario |
| **Plan** | Un plan de trabajo táctico acotado a una sesión o sprint corto |
| **Skill** | Un flujo de trabajo ejecutable con modos definidos y puntos de validación humana |
| **Summary** | El resumen archivable de un plan cerrado, producido por `planning:summarize` |
| **Update Brain** | El proceso de actualizar la memoria a largo plazo tras cambios significativos a nivel proyecto |
| **Human in the loop** | El principio de que el humano valida y aprueba antes de cada etapa significativa |

---

<div align="center">

**JAIBA** · Joint-operations Artificial Intelligence Behavioral Architecture

*El desarrollo con IA no debería ser magia negra. Debería ser ingeniería.*

🦀

</div>
# 🦀 JAIBA
