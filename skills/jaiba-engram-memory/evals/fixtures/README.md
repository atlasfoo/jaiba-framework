# Synthetic eval fixtures

`run_jaiba3_static.py` is a local stdlib check of the `JAIBA3`
(`jaiba-engram-storage/3`) wire profile on synthetic bytes: strict decode,
9 vs 10 line framing, truncation, redaction, whitespace, bit flips, legacy
prefixes, topic-key length, chunk split/reassembly with corruption, missing
or reordered chunks, ownership labels, and catalogue reconciliation.

```bash
python3 -B run_jaiba3_static.py <evidence-dir>
```

It never calls Engram, never executes the skill, and is not operational
conformance. Keep scratch output under `/tmp/opencode/jaiba-memory-surfaces/<run>`.
Do not point an eval at a live Engram backend or use these files to authorize
mutations. Historical `JAIBA1`/`JAIBA2` fixtures were removed; those prefixes
are only used as rejected inputs.
