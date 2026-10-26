# Synthetic eval fixtures

These files are protocol-analysis inputs, not a backend dump, executable adapter,
or evidence of conformance. Use the `evals.json` prompts with the skill eval
runner; keep any scratch output under `/tmp/opencode/jaiba-memory-surfaces/<run>`.
Do not point an eval at a live Engram backend or use these fixtures to authorize
mutations. T009 owns authorized live conformance checks.

Large-object and digest cases specify computed properties rather than
fabricated expected hashes. Profile 2 retains one ordinary standard-JSON
UTF-8 snapshot (including its emitted whitespace/newline) for each logical or
control revision. Its padded standard base64 transport must strictly decode
and re-encode to the identical wire, and full readback bytes must equal that
retained snapshot; parsing and reserializing JSON is not an equality check.
Different standard serializers may produce different snapshots and byte
fingerprints for equivalent JSON values. Compute each snapshot's byte length
and SHA-256 with standard tools; never invent expected hashes.

`chunk-and-large-object-cases.json` includes profile-2 snapshot and failure
cases. `mixed-namespaces-and-schemas.json` retains explicitly labeled
profile-1 historical examples, and adds profile-2 boundary cases. JAIBA1
must not be decoded as profile 2, relabeled, or shape-sniffed. These fixtures
are inputs/specifications, not a behavioral harness or conformance evidence.
Local byte and literal precondition comparisons only establish results for
the exact fixture inputs and commands recorded in external T-040 evidence;
they do not run the skill, exercise Engram, or certify a binding/profile.

`profile-2-static-cases.json` and `run_profile2_static.py` are static local
fixture checks only. Their receipts and hashes document computations on these
fixture bytes; they do not execute the skill, call a backend, or establish
operational conformance.
