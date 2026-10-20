# External memory eval scenarios

The JSON cases describe synthetic adapter states and fixture payloads; they are
authored scenarios, not executed behavioral evidence or a claim that a backend
conforms. To stage a scenario, create its repo, host-visible surface declaration,
registry, binding,
catalogue and adapter responses under a disposable scratch root; populate them
from the case's `context` and `expected_output`, not from this repository. Keep
all writes inside scratch. Run behavioral evaluation only with an independently
verified conforming adapter and explicit test authorization. Do not use the
current Engram draft as a conformance adapter. Current init documentation defines
the `migrate-surface` approval, staging, verification, activation and recovery
workflow. The fixture review case exercises only structural payload validation;
it does not execute migration actions. Runtime migration exercises are separate
and must use isolated mock storage, not a real backend.
