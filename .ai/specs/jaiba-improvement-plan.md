# JAIBA — Plan de Mejoras

> Documento de planificación. No es un artefacto del cerebro de un proyecto:
> es la hoja de ruta para evolucionar **el framework mismo**. Cada mejora se
> ejecutará como su propia spec dentro del repo de JAIBA, en Claude Code,
> entrando por la cadena del `conduct` (propose → spec) sobre ese repo.
>
> El framework vive en un solo repositorio, así que esto es una **secuencia de
> specs**, no una *mission*. El orden respeta las dependencias, no la
> preferencia.

---

## 1. Modelo objetivo (decisiones ya cerradas)

Estas decisiones son transversales. Cada spec las honra; no se re-litigan
dentro de cada `define`.

**Memoria en dos categorías (reemplaza largo/medio/corto plazo):**
- **Constitutiva** — qué / por qué / cómo / para quién / con quién / quality gate.
  Es `constitution.md` + `adr-log.md` + `reference-index.md`. Identidad estable.
- **Ejecutiva** — qué se está haciendo / cómo / estado actual del cambio.
  PRD (si aplica) + plan + tasks + walkthrough.

**Tres tiers físicos de almacenamiento:**

| Tier | Ubicación | Versionado | Contenido |
|---|---|---|---|
| Cerebro de proyecto | `.ai/` (in-repo) | sí | constitutiva + ejecutiva |
| Capa de herramientas | `.atl/` (in-repo) | no (gitignored) | `tool-layout.md` |
| Coordinación de mission | `~/.jaiba/$WORKSPACE/` o superficie externa | no por defecto | descomposición de mission, contratos compartidos, log de contrato |

**Unificación spec ↔ plan:** `specification` se disuelve dentro de `planning`.
Un triage interno decide la **profundidad** del cambio sobre un continuo:

```
inline (fast)  →  plan  →  spec  →  mission
   atómico       tarea     diseño    cross-componente
```

El humano **siempre** recibe un plan a aprobar; el triage decide la profundidad
del diseño que lo acompaña, no si hay validación.

**Archivo unificado:** un solo `.ai/memory/log/` append-only que funde el viejo
`archive/` (trabajo cerrado) y un changelog cronológico del cerebro.

**Componente = repositorio.** `constitution` describe alcance por sub-unidad
cuando el repo agrupa varias (libs de un turborepo, proyectos de una `.sln`).

**Costura cross-componente = contrato en protocolo estándar** (OpenAPI /
AsyncAPI / JSON), propiedad de la *mission*, referenciado por cada componente.

---

## 2. Roadmap y dependencias

```
Fase 0 · SPEC-02a  Fixes de doctor + .atl/tool-layout      [ENTREGADA]
Fase 1 · SPEC-01   Orquestador unificado + constitutiva/ejecutiva   [ENTREGADA — plan orquestador-unificado-memoria, ⊕ SPEC-03]
Fase 2 · SPEC-03   Batería de subagentes                   [ENTREGADA — absorbida por el plan de SPEC-01]
         SPEC-02b  ATL completo (indiza subagentes + skills externas)   [ENTREGADA — plan spec-02b-atl-completo]
Fase 3 · SPEC-05   Patrón OKF (serialización del modelo)   [ENTREGADA — plan okf-serializacion-cerebro]
Fase 4 · SPEC-04   Superficies de memoria pluggables   ┐ par
Fase 5 · SPEC-06   Mission / multicomponente            ┘ acoplado
```

```
SPEC-01 ⊕ SPEC-03 (fundación, entregadas juntas)
  ├─→ SPEC-02b (depende de SPEC-02a + esta entrega)
  ├─→ SPEC-05 ─→ SPEC-04 ─→ SPEC-06
  └─→ (constitution scope, reference-index contrato-interno: back-constraints de 06)
SPEC-02a  ── entregada
```

---

## 3. Specs

### SPEC-02a · Fixes de `doctor` + capa `.atl/`
**Prefijo sugerido:** `ATL` · **Fase 0** · **Profundidad: plan** · **Depende de:** nada

**Objetivo.** Corregir bugs reales del probe de toolchain y mover el estado de
máquina a una capa propia, antes de cualquier reorg.

**En alcance**
- `.ai/tools-state.md` → `.atl/tool-layout.md` (local, gitignored, siempre filesystem sin importar la superficie de memoria).
- Probe correcto en Windows: distinguir git bash de WSL; no asumir uno por el otro.
- *Enforcement* de AGENTS.md §6: el agente debe **leer y honrar** las anotaciones de `tool-layout` antes de invocar una skill cuya herramienta esté marcada ausente.

**Fuera de alcance**
- Indizar herramientas no-framework o subagentes (eso es SPEC-02b).

**Criterios de aceptación**
- `[x]` Happy: en Windows con git bash, el probe lo reporta como shell disponible y no referencia WSL.
- `[x]` Happy: antes de invocar una skill con herramienta ausente, el agente lo surface al humano (no descubre el gap por fallo).
- `[x]` Sad: si `.atl/tool-layout.md` no existe, el agente lo nota y sugiere `scaffold`, sin asumir toolchain completo.

**Abierto para su `define`**
- ¿`tool-layout` es per-repo o per-workspace? (un workspace multi-repo corre en una sola máquina; el toolchain es de máquina). Decisión que también afecta SPEC-06.

---

### SPEC-01 · Orquestador unificado + modelo constitutiva/ejecutiva
**Prefijo sugerido:** `ORC` · **Fase 1** · **Profundidad: spec (keystone)** · **Depende de:** nada (pero condiciona a 03, 04, 05, 06)

> **✅ ENTREGADA** (2026-07-05) por el plan `orquestador-unificado-memoria`,
> que absorbió SPEC-03 completa. Desviaciones aprobadas por el desarrollador
> respecto a lo escrito abajo: la skill unificada se llamó **`orchestrator`**
> (no `planning`; colisión con los plan modes nativos); la cadena es
> `propose → spec → tasks → execute → validate → summarize`;
> `summarize`+`archive` se **fusionaron en un paso** (invariante de dos pasos
> revocada explícitamente); `ask`/`fast` quedaron **implícitas-only**
> (el roadmap contemplaba `/fast` explícito); carpeta ejecutiva = `work/`;
> `log/` y `adr-log.md` permanecen **separados** (curado vs cronológico).
> Rename posterior (2026-07-06, inline sin plan — solo naming, sin cambio de
> comportamiento): `orchestrator` → **`conduct`** (verbo, no sustantivo de rol;
> más pegajoso; libera la metáfora de orquesta/dirección musical).

**Objetivo.** Disolver `specification` dentro de `planning`, introducir el triage
interno de profundidad y colapsar la memoria a constitutiva + ejecutiva.

**En alcance**
- **Modos de `planning`:** `brainstorm` (opcional) → `define` (con triage) → `execute` (implícito) → `summarize` → `archive`.
- **Triage interno** en `define`: blast radius → profundidad (inline / plan / spec). Una sola lógica de triage, compartida con `fast` (difieren en default y piso).
- **PRD absorbe user-stories** como segmento de criterios de aceptación, conservando numeración `<PREFIX>-NNN` y estructura happy/sad en Given/When/Then.
- **`plan`/`tasks` con alcance de spec** (uno por cambio, no uno por HU). Las **fases** son el artefacto multisesión / checkpoints.
- **`fast`** = carril inline de excepción. Explícito (`/fast`) o implícito (solicitud de cambio sobre sesión con trabajo activo). Free-standing no escribe ejecutiva; ajuste la registra tras confirmación.
- **Regla de ruteo** en arranque con trabajo activo: continuación → `execute` · pregunta → `ask` · solicitud de cambio → `fast`.
- **Memoria:** `.ai/memory/log/` unificado (cerrados + changelog). Carpeta ejecutiva renombrada desde `session/` (decidir nombre).
- **Esquema de criterios de aceptación** como dato estructurado (lo consume el subagente `verify` en SPEC-03).

**Fuera de alcance**
- Subagentes (SPEC-03), serialización OKF (SPEC-05), superficies (SPEC-04), mission (SPEC-06).

**Invariantes a preservar**
- `summarize` y `archive` siguen siendo **dos pasos**: el humano lee el resumen antes de destruir la ejecutiva.
- El plan se aprueba antes de `execute`. Human in the loop intacto.

**Criterios de aceptación**
- `[x]` Happy: un requerimiento cross-cutting profundo produce PRD + plan + tasks; uno superficial produce solo plan + tasks; el humano aprueba en ambos.
- `[x]` Happy: un cambio out-of-band atómico durante un plan activo entra por `fast` sin descarrilar el plan.
- `[x]` Sad: un cambio out-of-band **grande** durante un plan activo → `fast` lo surface y ofrece plegarlo como fase o park-and-replan; no crea un segundo plan en silencio.
- `[x]` Sad: ante un requerimiento ambiguo, `define` cuestiona antes de escribir; no inventa el triage.

**Back-constraints que debe dejar listos (los consumen 04/06)**
- `constitution` con alcance por sub-unidad.
- `reference-index` con categoría de **contrato interno cross-componente** (distinta de APIs externas).

**Abierto para su `define`**
- Nombre de la carpeta ejecutiva (`work/` / `current/` / `execution/`).
- ¿`log/` y `adr-log.md` permanecen separados (curado vs cronológico) o se funden?

---

### SPEC-03 · Batería de subagentes + contrato de invocación
**Prefijo sugerido:** `SUB` · **Fase 2** · **Profundidad: spec** · **Depende de:** SPEC-01

> **✅ ENTREGADA** (2026-07-05) — absorbida completa por el plan
> `orquestador-unificado-memoria` de SPEC-01 (decisión del desarrollador,
> 2026-07-03). Resoluciones de sus preguntas abiertas: catálogo de 6
> subagentes (3 ejecutores por carga cognitiva `high/medium/low` +
> `code-analyst`, `business-analyst`, `verify`); paralelismo por oleadas
> desde el grafo `depends-on` con fan-out ≤3, dos tareas solo en paralelo
> si no comparten archivos, y regla single-writer sobre `.ai/work/`.
> Contrato en `conduct/references/subagents.md`.

**Objetivo.** Dotar al framework de subagentes especialistas que `scaffold`
instala en la config global del agente, e invocarlos desde el orquestador para
descargar memoria del agente principal y habilitar paralelismo.

**En alcance**
- Catálogo base: análisis de código, análisis de negocio contra la superficie de memoria, ejecución de tareas (pequeña/mediana/grande), `verify` post-implementación.
- `verify` consume el **esquema de criterios** definido en SPEC-01.
- Instalación vía `scaffold` a la carpeta de config global del agente.
- Contrato de invocación: las skills workflow invocan subagentes (y viceversa); convención `requires:` para declarar herramientas (la indiza SPEC-02b).
- Soporte para fan-out paralelo (una tarea por subagente).

**Fuera de alcance**
- Indización de los subagentes en el ATL (SPEC-02b, justo después).

**Criterios de aceptación**
- `[x]` Happy: `execute` delega una fase a un subagente especialista y recupera el resultado sin cargar el contexto completo en el agente principal.
- `[x]` Happy: tras implementar, `verify` chequea los criterios de aceptación y reporta cumplido/incumplido por criterio.
- `[x]` Sad: si un subagente declara una herramienta ausente en `tool-layout`, se surface antes de invocarlo.

**Abierto para su `define`**
- Granularidad del catálogo (cuántos subagentes, frontera entre "mediana" y "grande").
- Política de paralelismo (límite de concurrencia, manejo de conflictos de escritura entre subagentes en el mismo repo).

---

### SPEC-02b · ATL completo (indización total)
**Prefijo sugerido:** `ATL` · **Fase 2** · **Profundidad: plan** · **Depende de:** SPEC-02a, y la entrega SPEC-01 ⊕ SPEC-03 (el plan `orquestador-unificado-memoria`, que absorbió SPEC-03)

**Objetivo.** Extender `doctor`/ATL para indizar **todas** las herramientas
disponibles para el agente, no solo las que declaran las skills del framework.

**En alcance**
- Indizar skills y subagentes **no integrados** al framework (caso `context7`: skill + subagente necesario para consulta de documentación al invocar un planning).
- Columna de provenance "Needed by" (skill / subagente / hook que declara cada herramienta).
- Señalar herramientas **requeridas pero ausentes** con su demandante.

**Criterios de aceptación**
- `[x]` Happy: una skill externa instalada (p. ej. context7) aparece indizada con sus `requires:` resueltos.
- `[x]` Happy: una herramienta requerida y ausente se reporta con quién la necesita.
- `[x]` Sad: el probe marca `[UNVERIFIED]` lo que no puede comprobar; nunca lo da por presente.

---

### SPEC-05 · Patrón OKF (serialización del cerebro)
**Prefijo sugerido:** `OKF` · **Fase 3** · **Profundidad: spec** · **Depende de:** SPEC-01

> **✅ ENTREGADA** (2026-08-01) por el plan `okf-serializacion-cerebro`.
> Sin desviaciones estructurales respecto a lo escrito abajo. La fase 6
> del plan dogfoodeó la entrega instrumentando el cerebro propio de este
> repo — ver `.ai/memory/log/2026-08-01-okf-serializacion-cerebro.md`.

**Objetivo.** Adoptar el **patrón** de OKF (no el formato literal v0.1) como
convención de serialización del modelo constitutiva/ejecutiva ya estabilizado.

**En alcance**
- Concepto-por-archivo, frontmatter, grafo cross-linked entre artefactos.
- `index.md` (listado) + `log.md`-style (historial) — alinea con el `.ai/memory/log/` de SPEC-01.
- Mapeo de cada artefacto: p. ej. `reference-index` deja de ser una tabla única y pasa a conceptos enlazados.
- ADR explícito que documente la apuesta (OKF v0.1 es draft; se toma el patrón, no la dependencia).

**Fuera de alcance**
- Backends de almacenamiento (SPEC-04). OKF deja storage/serving fuera de alcance — y nosotros también, aquí.

**Criterios de aceptación**
- `[x]` Happy: el cerebro se lee y escribe como grafo de conceptos enlazados; un agente nuevo lo navega desde `index.md`.
- `[x]` Sad: nada del framework queda atado a tooling propietario de OKF; el cambio es solo de convención de archivos.

---

### SPEC-04 · Superficies de memoria pluggables
**Prefijo sugerido:** `MEM` · **Fase 4** · **Profundidad: spec** · **Depende de:** SPEC-05 · **Acoplada con:** SPEC-06

**Objetivo.** Abstraer **dónde** vive la memoria, para que el desarrollador
configure la superficie (filesystem por defecto, claude-mem, obsidian, …) vía
una skill meta de memoria, con sus instrucciones de manipulación.

**En alcance**
- Skill meta que registra la superficie elegida y cómo escribir/leer cada artefacto en ella.
- Abstracción productor/consumidor (heredada del patrón OKF): toda skill pasa por la superficie, no lee markdown directo.
- Superficie filesystem por defecto: cerebro en `.ai/`; coordinación de mission en `~/.jaiba/$WORKSPACE/` (no versionada — tradeoff aceptado).
- Re-serialización por superficie: p. ej. `reference-index` markdown → filas SQLite en claude-mem.
- Una superficie puede cumplir el rol de **coordinación cross-componente** (requisito de SPEC-06).

**Fuera de alcance**
- `.atl/tool-layout.md` queda **siempre en filesystem local**, fuera de esta abstracción.

**Criterios de aceptación**
- `[ ]` Happy: con superficie filesystem, todo funciona como hoy (modulo reorg).
- `[ ]` Happy: cambiar a una superficie externa redirige lectura/escritura sin que las skills cambien su lógica.
- `[ ]` Sad: si la superficie configurada no está disponible, se surface y se ofrece fallback a filesystem; no se pierde trabajo en silencio.

**Abierto para su `define`**
- Cómo se computa la identidad `$WORKSPACE`.
- Contrato mínimo que una superficie debe implementar (CRUD de conceptos + log + grafo).

---

### SPEC-06 · Mission / multicomponente
**Prefijo sugerido:** `MIS` · **Fase 5** · **Profundidad: spec (capstone)** · **Depende de:** SPEC-01, SPEC-03, SPEC-04

**Objetivo.** Un nivel sobre spec que coordina cambios a través de **N
componentes** (repos), con descomposición en una spec por componente, sin repo
control-plane vacío.

**En alcance**
- **`mission`** como tramo del triage cuando el cambio cruza componentes (amplitud, no solo profundidad).
- Análisis del estado actual de cada componente → output: asignar una spec por componente (módulo nuevo → spec de endpoint en backend, spec de pantalla en frontend).
- Componente = repositorio. Aprovecha workspace multifolder del agente o centralizador en nube (ticketing/helpdesk como punto de entrada genérico).
- **Memoria de mission** en `~/.jaiba/$WORKSPACE/` (default) o superficie externa (recomendada para equipo).
- **Contrato compartido** propiedad de la mission, en protocolo estándar (OpenAPI/AsyncAPI/JSON); cada `reference-index` de componente lo referencia.
- **Control de cambios del contrato:** un componente emite un ajuste y los demás lo reciben (log de contrato append-only en default fs; mensajería activa en superficie externa/ticketing).
- **Doble gate humano:** aprobar la descomposición → aprobar cada spec.

**Fuera de alcance**
- Granularidad sub-repo como unidad de mission (descartada; se usa alcance en `constitution`).

**Criterios de aceptación**
- `[ ]` Happy: una mission descompone un módulo nuevo en spec-backend + spec-frontend, ambas referenciando el mismo contrato.
- `[ ]` Happy: backend ajusta el contrato; frontend recibe la notificación de cambio antes de cerrar su spec.
- `[ ]` Happy: entrada vía ticketing dispara el análisis multicomponente sin repo control-plane.
- `[ ]` Sad: trabajando en equipo con superficie filesystem (no persistente), el framework advierte el tradeoff y recomienda superficie externa.
- `[ ]` Sad: si un componente no tiene `.ai/`, la mission lo surface y rutea a `scaffold` antes de asignarle spec.

**Abierto para su `define`**
- Si el ticketing es solo trigger de lectura o también write-back (crear sub-issues, actualizar estado) — toca el límite "publicar/enviar requiere permiso".
- Resolución de conflictos cuando dos componentes proponen ajustes incompatibles al contrato.

---

## 4. Orden de ejecución en Claude Code

1. ~~**SPEC-02a**~~ — entregada.
2. ~~**SPEC-01**~~ — entregada (plan directo sobre el roadmap, ⊕ SPEC-03).
3. ~~**SPEC-03**~~ — entregada (absorbida por el plan de SPEC-01).
4. ~~**SPEC-02b**~~ — entregada (plan `spec-02b-atl-completo`) → siguiente: **SPEC-05**.
5. ~~**SPEC-05**~~ — entregada (plan `okf-serializacion-cerebro`) → siguiente: **SPEC-04**.
6. **SPEC-04** + **SPEC-06** (par acoplado; 04 primero, 06 sobre ella).

Cada spec lleva, al final de su sección, las preguntas que su propio `define`
debe resolver. Ninguna bloquea el plan; todas son internas a su ejecución.
