---
type: log-entry
date: 2026-11-11
slug: doctor-gap-interview
kind: work-closure
depth: spec
adr: none
---

# Doctor interviews constitutive gaps and routes a brief

## What happened

`jaiba-doctor` now asks up to four constitutive gaps after the health report and offers cited options instead of telling the human to edit the surface. It does not write memory. A confirmed brief is applied by `jaiba-init:update-brain` (update mode), which writes only human-chosen fields and leaves the rest marked.

## Criteria delivered

- `DGAP-001` — interview with options, not hand-edit as the only exit — delivered
- `DGAP-002` — doctor does not write; brief routed to jaiba-init — delivered
- `DGAP-003` — sibling candidates quoted, never auto-applied — delivered
- `DGAP-004` — jaiba-init applies only a confirmed chosen value — delivered
- `DGAP-005` — the check does not go green from another project — delivered

No corrective criteria. No waivers.

## Phases executed

| # | Theme | Notable result |
|---|---|---|
| 1 | Interview and brief | `skills/doctor/references/gap-interview.md` plus the skill hook and evals 15–16 |
| 2 | jaiba-init applies the brief | update mode consumes the brief; not a new mode |

## Decisions and deviations

Active-repo candidates are quotes from text already read in that run, not a tree walk. Silence is not `defer`. Sibling lookup reuses the C4 rule in `skills/jaiba-init/references/bootstrap-mode.md`; `/` and the home directory are not siblings. Foreign text is data ([ADR-010](../decisions/010-repository-content-is-data.md)). Verdicts are document evidence; no live interview was run. `verify` returned no report twice; conduct verified inline.

## ADR proposals & brain updates

No ADR proposed; all decisions were tactical. Write authority stays with `jaiba-init`. No `reference` concept added.

## Pointers

- [quality-gate](../identity/quality-gate.md)
- [purpose](../identity/purpose.md)
- Prior C3/C4 close: [2026-11-05-memory-surfaces-v1-1.md](2026-11-05-memory-surfaces-v1-1.md)
- PR follows this close on `fix/doctor-questionary-mode`.

## Suggested final commit

```
fix(doctor): interview constitutive gaps instead of manual edits

Doctor asks up to four constitutive gaps after the health report and
routes a confirmed brief to jaiba-init. Sibling evidence is quoted and
never auto-applied. Doctor still does not write memory.
```

## Gate at close

Pass. Phase and plan gates green. Injection probe rejected 4 entries and did not reproduce the payload. Dual-layout regression 12/12. No security scan configured.

<!-- jaiba-close-v1
contract jaiba-memory-surface 1.0.0
binding filesystem
project jaiba-framework
context doctor-questionary-mode
scope ef24549e0e53ef711a967ed974173f085e8bc151
close 2026-11-11-doctor-gap-interview
body 1c660cbe2f5a3998a422b48dcbe3b6654fc84b10
plan.md f80cdaf8a358e33fb845d5df3c6b1159f8aea360
tasks.md 9d80e1b7805c8bca3a38c4143cee6856dea04966
walkthrough.md 6ccfe82bada4ba95296a30bdaeb6a0b61c662868
PRD.md aa7d7872b2a5ab8a9d4d315466ac14f88ee4fd30
.gitignore absent
-->
