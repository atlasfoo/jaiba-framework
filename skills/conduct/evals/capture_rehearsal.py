"""Lossless content-addressed packaging of an ACTUAL scratch journal.

Generation is explicit, never part of tests. Updating a capture requires a
new source-guided model rehearsal, not just changing expected assertions.
"""
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from surface_rehearsal import ROOT, Session, digest

FIXTURES = Path(__file__).parent / 'fixtures' / 'surface-rehearsal'


def pack(value, blobs):
    if isinstance(value, dict):
        encoded = {k: pack(v, blobs) for k, v in value.items()}
    elif isinstance(value, list):
        encoded = [pack(v, blobs) for v in value]
    else:
        encoded = value
    if len(json.dumps(encoded, ensure_ascii=False)) > 240:
        key = digest(encoded)
        blobs[key] = encoded
        return {'$blob': key}
    return encoded


def unpack(value, blobs):
    if isinstance(value, dict):
        if set(value) == {'$blob'}:
            encoded = blobs[value['$blob']]
            assert digest(encoded) == value['$blob']
            return unpack(encoded, blobs)
        return {k: unpack(v, blobs) for k, v in value.items()}
    if isinstance(value, list):
        return [unpack(v, blobs) for v in value]
    return value


def load(path):
    data = json.loads(path.read_text())
    value = unpack(data['journal'], data['blobs'])
    assert digest(value) == data['journal_digest']
    return value


def capture(root):
    FIXTURES.mkdir(parents=True, exist_ok=True)
    index = {'source_scratch': str(root), 'kind': 'actual executor-as-consumer synthetic rehearsal',
             'child_limit': 'Actual named dispatches rejected at depth 1; no child backend access tested.',
             'fixtures': {}}
    for layout in ('external', 'bundle', 'legacy'):
        s = Session(root / layout)
        assert s.state['events'][-1]['phase'] == 'summarize-complete'
        blobs = {}
        packed = pack(s.state, blobs)
        data = dict(journal_digest=digest(s.state), journal=packed, blobs=blobs)
        target = FIXTURES / f'{layout}.json'
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        assert load(target) == s.state
        index['fixtures'][layout] = dict(file=target.name, digest=digest(s.state),
                                        events=len(s.state['events']), sources=s.state['source_revisions'])
    (FIXTURES / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v['events'] for k, v in index['fixtures'].items()}))


if __name__ == '__main__':
    capture(Path(sys.argv[1]))
