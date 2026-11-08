# Synthetic eval fixtures

`run_jaiba4_static.py` is a local stdlib check of the `JAIBA4`
(`jaiba-engram-storage/4`) wire profile and executive journal on synthetic bytes:
strict JAIBA4 single-line wire decode, framing across 9 vs 10 line responses,
direct (< 30,000 bytes) and chunked (> 30,000 bytes) roundtrips, fail-closed
corruption/tampering checks, deterministic executive delta folding across spec
and execute phases (`MSV-005`), criterion ID permanence enforcement on approved
PRDs (`MSV-005`), deterministic Markdown render extraction (`MSV-008`), legacy
`JAIBA3` read-only decoding without relabeling (`MSV-010`), write refusal on
unmigrated stores (`MSV-010`), lossless `JAIBA3 → JAIBA4` base and context-head
migration at `seq: 0` (`MSV-010`), and canonical `binding-path` calculation.

```bash
python3 -B run_jaiba4_static.py <evidence-dir>
```

`run_jaiba3_static.py` remains as the historical validator for the legacy
`JAIBA3` (`jaiba-engram-storage/3`) wire profile.

```bash
python3 -B run_jaiba3_static.py <evidence-dir>
```

These scripts never call Engram, never execute the skill, and are not operational
conformance. Keep scratch output under `/tmp/opencode/jaiba-memory-surfaces/<run>`.
Do not point an eval at a live Engram backend or use these files to authorize
mutations. Historical `JAIBA1`/`JAIBA2` prefixes are rejected inputs.
