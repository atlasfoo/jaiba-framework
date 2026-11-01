"""Explicit model-authored inline role rehearsals after observed spawn failures.

Not real children: the host rejected every named dispatch at depth 1. This
module retains that limitation and the independent simulated actor failure.
"""
import difflib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True

from surface_rehearsal import Session, address, digest
from rehearse_workflows import GATE

ERROR = 'Subagent depth limit reached (1). Increase "experimental.subagent_depth" to allow nested subagents.'


def blocked(roles):
    return dict(kind='actual-host-dispatch-error', roles=roles, error=ERROR,
                child_id=None, child_started=False, child_backend_access='not established',
                partial_writes='none; dispatch rejected before child creation',
                recovery='role-local inline sequential fallback; no host configuration change')


def analysis(s):
    before = digest(s.state['objects'])
    sources = []
    for entry in s.catalog('constitutive', actor='business-analyst-inline'):
        o = s.read(entry['address'], actor='business-analyst-inline')
        sources.append(dict(address=o['address'], revision=o['revision'], complete=True))
    files = {name: (s.path / name).read_text() for name in ('app.py', 'test_app.py')}
    report = dict(dispatch=blocked(['business-analyst', 'code-analyst']),
        memory=dict(sources=sources, result='Aligned: offline local greeting; no new integration; no standing decision conflict.',
                    layout=s.state['layout'], migration=False),
        code=dict(files=files, revisions={k: digest(v) for k, v in files.items()},
                  result='greet is a private unimplemented helper; two test calls, Ada happy and empty sad. '
                         'One app module and one existing test module; no external integration.',
                  backend='not required for source-only survey, not inheritance verified'))
    assert before == digest(s.state['objects'])
    (s.path / 'analysis-report.json').write_text(json.dumps(report, indent=2) + '\n')
    s.note('analyst-fallback', '', 'Both named analyst calls were rejected by the host depth limit. '
           'No child/job ID or partial write exists. I performed the same read-only survey and exact '
           'catalogue/full-read memory contrast inline; no executive artifacts written.', report=report)


def executor(s):
    p = s.path / 'app.py'
    before = p.read_text()
    # The executor model's explicit implementation choice; no workflow state machine.
    after = before.replace('    raise NotImplementedError',
        "    if not name:\n        raise ValueError('name required')\n    return f'Hello, {name}'")
    assert after != before
    p.write_text(after)
    result = s.command(GATE)
    assert result.returncode == 0, result.stderr
    report = dict(dispatch=blocked(['executor-low']), task='T-001', load='low',
        files=['app.py'], diff=''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                                         fromfile='app.py before', tofile='app.py after')),
        gate=dict(argv=GATE, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr),
        backend='not required; source excerpts suffice; NOT inheritance verified',
        executive_writes=False, decisions='Use ValueError for empty name and exact greeting format from tests.')
    (s.path / 'executor-report.json').write_text(json.dumps(report, indent=2) + '\n')
    s.note('executor-fallback', '', 'executor-low could not start at host depth 1. '
           'Implemented only app.py inline sequentially and ran the supplied gate; no executive writes.', report=report)


def verify(s, recovery=False):
    # This is a role-local simulated actor, explicitly NOT an actual child probe.
    preflight = s.tool('read', 'verify', address=address('executive', 'prd'))
    if not recovery:
        assert preflight['outcome'] == 'permission-denied'
        report = dict(dispatch=blocked(['verify']), verdict='not verifiable',
            criterion='GREET-001', actor='executor-model inline verify rehearsal, NOT child',
            observed_preflight=preflight, paths={'happy': 'not verifiable', 'sad': 'not verifiable'})
        target = 'verify-failure.json'
    else:
        assert preflight['outcome'] == 'ok' and preflight['complete']
        entries = s.catalog('executive', actor='verify')
        objects = [s.read(e['address'], actor='verify') for e in entries]
        schema = s.state['criteria_schema']
        prd = next(o for o in objects if o['type'] == 'prd')
        import re
        parsed = json.loads(re.search(r'```yaml\n(.*?)\n```', prd['content'], re.S)[1])
        assert parsed == schema
        tasks = next(o for o in objects if o['type'] == 'tasks')
        assert 'covers: GREET-001' in tasks['content']
        result = s.command(GATE)
        assert result.returncode == 0
        report = dict(dispatch=blocked(['verify']), verdict='met', criterion='GREET-001',
            actor='executor-model inline verify fallback, NOT child',
            source_criteria=parsed, source_objects=[dict(address=o['address'], revision=o['revision']) for o in objects],
            paths={'happy': 'test_greeting passed: Ada -> Hello, Ada',
                   'sad': 'test_empty passed: empty name -> ValueError'},
            gate=dict(argv=GATE, provenance=s.state['gate_source'], returncode=result.returncode,
                      stdout=result.stdout, stderr=result.stderr), executive_writes=False)
        target = 'verify-recovery.json'
    (s.path / target).write_text(json.dumps(report, indent=2) + '\n')
    s.note('verify-role-local-rehearsal', '', 'Actual named verify dispatch is unavailable at this nesting depth. '
           'This result is from the explicitly labeled inline fallback, not child backend inheritance.', report=report)


if __name__ == '__main__':
    s = Session(sys.argv[1])
    {'analysis': analysis, 'executor': executor, 'verify-failure': verify,
     'verify-recovery': lambda s: verify(s, True)}[sys.argv[2]](s)
    print(json.dumps({'fallback': sys.argv[2], 'scratch': str(s.path), 'events': len(s.state['events'])}))
