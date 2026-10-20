"""Historical recorded protocol, replayable without a model API.

The packaged turns are historical executor-as-consumer rehearsal evidence.
This script replays their fixed decisions/actions, not fresh model compliance.
It does not claim current-source or adapter conformance. Run one stage at a
time; named children ran between stages in the original rehearsal only.
"""
import copy
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True

from surface_rehearsal import (Session, ROOT, NAMESPACE, PROJECT, CONTEXT,
                               address, obj, digest)

GATE = ['/usr/bin/python3', '-m', 'unittest', '-v', 'test_app.py']
GATE_TEXT = '/usr/bin/python3 -m unittest -v test_app.py'
SLUG = 'greeting'


def body(object_type, sections, **fields):
    header = dict(type=object_type, slug=SLUG, created='2026-10-18', **fields)
    return '---\n' + '\n'.join(f'{k}: {json.dumps(v)}' for k, v in header.items()) + '\n---\n\n' + sections


def payload(o, content):
    return {k: (content if k == 'content' else copy.deepcopy(v))
            for k, v in o.items() if k != 'revision'}


def seed(s, layout):
    facts = {
        'project': 'Greeting fixture; project identity fixture:code.example/Team/Greeting.',
        'architecture': 'One private Python module app.py with greet and tax helpers; no integration.',
        'purpose': 'Help an operator greet a named visitor.',
        'scope': 'Local greeting only. No network, persistence, accounts or authentication.',
        'quality-gate': f'Phase gate:\n{GATE_TEXT}\nPlan gate:\n{GATE_TEXT}\n',
        'convention': 'TDD disabled. Existing happy/sad tests define behavior. UTF-8; preserve unknown fields.',
        'decision': 'Keep this fixture offline; no external services.',
        'reference': 'Internal private contract app.greet(name); no external integrations.',
    }
    objects = []
    if layout == 'legacy':
        raw = '# Legacy constitution\n\n' + '\n\n'.join(f'## {k}\n{v}' for k, v in facts.items()
                                                           if k not in ('decision', 'reference'))
        for lid, kind, text, path in [
            ('constitution', 'project', raw, 'constitution.md'),
            ('decisions', 'decision', facts['decision'], 'adr-log.md'),
            ('references', 'reference', facts['reference'], 'reference-index.md')]:
            o = obj('constitutive', lid, kind, text)
            o['metadata'].update(relative_path=path,
                concept_views=list(facts)[:6] if lid == 'constitution' else [kind],
                representation='raw legacy document, no invented frontmatter')
            objects.append(o)
    else:
        for kind, text in facts.items():
            o = obj('constitutive', kind, kind, f'---\ntype: {kind}\n---\n{text}\n')
            o['metadata']['relative_path'] = f'identity/{kind}.md'
            objects.append(o)
        index = obj('constitutive', 'entry', 'index', '---\ntype: index\n---\n# Fixture index\n' +
                    '\n'.join(f'- [{k}](identity/{k}.md)' for k in facts) + '\n')
        index['metadata']['relative_path'] = 'index.md'
        objects.append(index)
    prior = obj('constitutive', 'prior-close', 'log-entry', 'Prior closure; prefix OLD; no GREET collision.\n')
    prior['metadata']['relative_path'] = 'log/2026-10-01-prior.md'
    objects.append(prior)
    objects.append(obj('executive', 'plan', 'plan', 'Other context B; never select this plan.\n', 'checkout-B'))
    s.seed(objects, layout)
    s.state['seed_objects'] = copy.deepcopy(s.state['objects'])
    sources = [ROOT / 'skills' / p for p in (
        'conduct/SKILL.md', 'ask/SKILL.md', 'fast/SKILL.md',
        'create-memory/references/memory-surface-contract.md',
        'create-memory/references/resolution.md', 'create-memory/references/filesystem-surface.md')]
    sources += sorted((ROOT / 'skills/conduct/references').glob('*.md'))
    sources += sorted((ROOT / 'skills/conduct/assets').glob('*template.md'))
    sources += sorted((ROOT / 'skills/ask/references').glob('*.md'))
    sources += sorted((ROOT / 'skills/fast/references').glob('*.md'))
    sources += [ROOT / 'skills/conduct/scripts/archive.sh']
    s.state['source_revisions'] = {str(p.relative_to(ROOT)): digest(p.read_text()) for p in sources}
    s.state['provenance'] = {
        'kind': 'executor-as-consumer synthetic model rehearsal; fixed-decision replay thereafter',
        'human_approval': 'Current user approved T-021 eval scope only; all developer turns below synthetic.',
        'backend': 'independent fake vault, not Engram; no inheritance claim or Phase6 assay',
        'effective_sources': 'explicit approved repository source selection, not a host installation test',
        'serialization': 'one rehearsal conductor; no concurrent fixture writers; child read-only except app.py task',
    }
    (s.path / 'app.py').write_text('def greet(name):\n    raise NotImplementedError\n\ndef tax(value):\n    return value * 0.075\n')
    (s.path / 'test_app.py').write_text('''import unittest
from app import greet, tax
class Behavior(unittest.TestCase):
    def test_greeting(self):
        self.assertEqual(greet('Ada'), 'Hello, Ada')
    def test_empty(self):
        with self.assertRaises(ValueError): greet('')
    def test_tax_existing(self):
        self.assertAlmostEqual(tax(10), 0.75)
''')
    s.save()
    s.tool('probe')
    # Layout selection is observed, not used as an external prerequisite.
    if layout == 'external':
        assert not (s.path / '.ai').exists() and not (s.path / 'AGENTS.md').exists()
    else:
        m = s.path / '.ai/memory'
        assert (m / 'index.md').exists() != (m / 'constitution.md').exists()
    for entry in s.catalog('constitutive'):
        s.read(entry['address'])
    assert not s.catalog('executive')
    s.note('propose', 'I want something welcoming for visitors.',
           'Do you need a local greeting for named visitors, or an account workflow? '
           'I will not save proposal artifacts; this conversation is volatile.')
    s.note('propose', 'Local greeting only; reject an empty name; no accounts. Prefix GREET is fine.',
           'Landed: greet a named visitor; reject an empty name. No accounts/network. '
           'This adds user-visible behavior, so spec depth. May I formalize it?',
           executive_objects_after=s.catalog('executive'))
    assert not s.catalog('executive')
    s.state['constitutive_baseline'] = {k: v for k, v in s.state['objects'].items()
                                          if v['address'][2] == 'constitutive'}
    s.save()


def spec(s):
    # Actual reports name either a dispatched child or the observed role-local blocker.
    assert (s.path / 'analysis-report.json').exists(), 'need analyst/fallback evidence'
    reports = json.loads((s.path / 'analysis-report.json').read_text())
    s.note('spec', 'Yes, formalize it.',
           'Spec depth: new greeting behavior. Both role-local inline fallback reports are consumed; '
           'the offline scope agrees and app.greet is currently unimplemented. '
           'I am writing full drafts only, not tasks or code.', analyst_reports=reports)
    criteria = {'criteria': [dict(id='GREET-001', title='Greet a named visitor',
        story='As an operator I want a greeting so visitors are welcomed.',
        happy=[dict(given='name Ada', when='greet is called', then='Hello, Ada is returned')],
        sad=[dict(given='empty name', when='greet is called', then='ValueError is raised')], status='open')]}
    s.state['criteria_schema'] = criteria
    refs = s.catalog('constitutive')
    gate_entry = next(e for e in refs if e['type'] == ('project' if s.state['layout'] == 'legacy' else 'quality-gate'))
    gate = s.read(gate_entry['address'])
    citation = (f"[gate](../memory/{gate['metadata']['relative_path']})" if s.state['layout'] != 'external'
                else json.dumps(dict(address=gate['address'], revision=gate['revision'])))
    s.state['gate_source'] = {'address': gate['address'], 'revision': gate['revision']}
    def verified_citation(kind):
        wanted = ('project' if kind in ('architecture', 'convention') else kind)
        wanted = wanted if s.state['layout'] == 'legacy' else kind
        entry = next(e for e in refs if e['type'] == wanted)
        concept = s.read(entry['address'])
        if s.state['layout'] == 'external':
            return json.dumps(dict(address=concept['address'], revision=concept['revision']))
        return f"[{kind}](../memory/{concept['metadata']['relative_path']}) (revision {concept['revision']})"
    architecture = verified_citation('architecture')
    convention = verified_citation('convention')
    decision = verified_citation('decision')
    reference = verified_citation('reference')
    previous_log = verified_citation('log-entry')
    prd = body('prd', '# PRD: Visitor greeting\n\n## Problem & context\nVisitors lack a greeting.\n\n'
        '## Goals / Non-goals\nGreet a name; no accounts.\n\n## Users\nOperator.\n\n'
        f'## Proposed solution\nA local greeting, with empty-name rejection; respects {reference}.\n\n'
        '## Scope\nIn: greeting. Out: accounts/network.\n\n## Assumptions & constraints\nOffline fixture.\n\n'
        '## Dependencies\nNo external integration.\n\n## Success metrics\nBoth existing behavior tests pass.\n\n'
        '## Acceptance criteria\n```yaml\n' + json.dumps(criteria, indent=2) + '\n```\n\n## Open questions\nNone.\n',
        status='draft', prefix='GREET', source='manual', **{'source-ref': ''})
    plan = body('plan', '# Plan: Visitor greeting\n\n## Objective\nGreet named visitors and reject an empty name. '
        'Remain offline.\n\n## Covered criteria\n- GREET-001 — greeting and rejection.\n\n'
        '## Scope\n**In:**\n- Implement private app.greet and run both existing tests.\n'
        f'**Out:**\n- Accounts and network.\n\n## Technical approach\nOne private helper in app.py; '
        f'follows {architecture} and {convention}. Respects {decision} and the private contract {reference}.\n\n'
        '## Discrepancies vs PRD\nNone.\n\n'
        f'## Sources consulted\n- {citation}\n- {architecture}\n- {convention}\n- {decision}\n'
        f'- {reference}\n- {previous_log}\n- Named analyst fallback reports: analysis-report.json.\n\n'
        '## Plan amendments\n', depth='spec', status='draft',
        prd=address('executive', 'prd') if s.state['layout'] == 'external' else 'PRD.md', criteria=['GREET-001'])
    s.write(obj('executive', 'prd', 'prd', prd))
    s.write(obj('executive', 'plan', 'plan', plan))
    frozen = digest(s.state['objects'])
    s.note('spec-approval', 'Not yet; do not approve or execute.',
           'Both drafts remain draft. No tasks or code will be written. Please approve the presented revisions explicitly.')
    assert frozen == digest(s.state['objects'])
    assert {e['type'] for e in s.catalog('executive')} == {'prd', 'plan'}
    s.note('spec-approval', 'I explicitly approve these draft revisions, unchanged.',
           'I will compare both revisions, persist status approved and verify full readback; tasks is a separate phase.',
           reviewed={e['type']: e['revision'] for e in s.catalog('executive')})
    for kind in ('prd', 'plan'):
        old = s.read(address('executive', kind))
        s.write(payload(old, old['content'].replace('status: "draft"', 'status: "approved"')), old)
    s.save()


def tasks(s):
    for kind in ('plan', 'prd'):
        assert 'status: "approved"' in s.read(address('executive', kind))['content']
    gate = s.read(s.state['gate_source']['address'])
    assert gate['revision'] == s.state['gate_source']['revision']
    convention = next(e for e in s.catalog('constitutive') if e['type'] == (
        'project' if s.state['layout'] == 'legacy' else 'convention'))
    s.read(convention['address'])
    s.note('tasks', 'Prepare the task graph.',
           'One mechanical task, load low, no dependencies, covers GREET-001. '
           'TDD disabled; existing tests cover both paths. Conduct alone creates tasks/walkthrough; '
           'gate commands below are copied verbatim with source address/revision.')
    text = body('tasks', '# Tasks: greeting\n\n## Gate Commands\n\n'
        f'Source: {json.dumps(s.state["gate_source"])}\nTDD: disabled\n\n'
        f'**Phase gate**\n- `{GATE_TEXT}`\n\n**Plan gate**\n- `{GATE_TEXT}`\n\n'
        '## Phase 1 — Greeting\n- **Depends on:** none\n- **Reversible:** yes\n'
        '- **Suggested commit:** `chore(wip): greeting`\n\n'
        '- [ ] **T-001** — Replace the unimplemented private greet helper in app.py with '
        'empty-name ValueError and Hello, name return; change only app.py.\n'
        '  `load: low` · `depends-on: none` · `covers: GREET-001`\n')
    s.write(obj('executive', 'tasks', 'tasks', text))
    s.write(obj('executive', 'walkthrough', 'walkthrough', body('walkthrough',
        '# Walkthrough: greeting\n\n## Phase 1 — Greeting\n')))
    s.command(GATE)  # Authorized fixture gate: initial red is evidence, not completion.
    assert s.state['events'][-1]['returncode'] != 0
    s.save()


def integrate(s):
    assert (s.path / 'executor-report.json').exists(), 'need executor dispatch/fallback evidence'
    for kind in ('plan', 'tasks', 'walkthrough'):
        s.read(address('executive', kind))
    report = json.loads((s.path / 'executor-report.json').read_text())
    source = (s.path / 'app.py').read_text()
    assert 'raise NotImplementedError' not in source and 'ValueError' in source
    s.note('execute', 'Continue; this is an isolated non-Git fixture workspace.',
           'The single runnable T-001 executor-low dispatch was blocked by the observed host depth limit. '
           'No child started or wrote files; the affected task ran inline sequentially. I reviewed its diff '
           'and report. Backend access was not required by the source-only execution envelope, '
           'not inheritance verified. I will record its result before checkbox progress.', child=report)
    old = s.read(address('executive', 'walkthrough'))
    intended = payload(old, old['content'] + '\n- T-001 — private greeting implemented inline; '
        'executor-low blocked: Subagent depth limit reached (1); no child ID/partial writes.\n')
    receipt = s.tool('update', object=intended, expected_revision=old['revision'], request_id='divergence-assay')
    assert receipt['outcome'] == 'ok'
    # Explicit test controller fault, not a consumer write: mutate full returned envelope.
    key = json.dumps(old['address'])
    s.state['objects'][key]['content'] += '\nInjected transport readback divergence.\n'
    bad = {k: v for k, v in s.state['objects'][key].items() if k != 'revision'}
    s.state['objects'][key]['revision'] = digest(bad)
    s.materialize(s.state['objects'][key])
    s.note('fault-controller', 'Inject acknowledged-write/readback divergence.',
           'Controlled transport fault injected; not an authorized workflow operation.')
    actual = s.read(old['address'])
    assert actual != dict(intended, revision=receipt['resulting_revision'])
    s.note('execute', 'The acknowledged walkthrough readback differs.',
           'Verification failed. Stop dependent checkbox and Phase-gate progress; reconcile exact reads. '
           'T-001 remains unchecked despite the source implementation.')
    assert '- [ ] **T-001**' in s.read(address('executive', 'tasks'))['content']
    s.note('execute-recovery', 'Synthetic reconciliation: restore only the intended walkthrough result at this current revision.',
           'I will compare the divergent revision, restore the approved intended content, and full-read back '
           'before running the gate or checking the task.')
    s.write(intended, actual)
    assert s.command(GATE).returncode == 0
    oldtasks = s.read(address('executive', 'tasks'))
    s.write(payload(oldtasks, oldtasks['content'].replace('- [ ] **T-001**', '- [x] **T-001**')), oldtasks)
    old = s.read(address('executive', 'walkthrough'))
    s.write(payload(old, old['content'] + '\n### Checkpoint — Phase 1\n**Outcome.** Greeting and rejection pass.\n'
        '**Decisions.** none\n**Deviations from plan.** Readback fault reconciled.\n'
        '**ADR candidates.** none\n**Gate.** Pass.\n'), old)
    assert s.command(GATE).returncode == 0
    s.note('execute', '', 'Phase complete; suggest chore(wip): greeting. No commit run. Pausing at the phase boundary.')


def validation(s, recovery=False):
    for kind in ('plan', 'tasks', 'prd', 'walkthrough'):
        s.read(address('executive', kind))
    assert '- [ ]' not in s.read(address('executive', 'tasks'))['content']
    assert s.command(GATE).returncode == 0  # Conductor's Plan gate, not the child report.
    if not recovery:
        s.state['denied'] = ['verify']
        s.note('validate', 'Validate the complete GREET-001 happy and sad paths.',
               'Plan gate passed. The named verify dispatch was blocked by the actual host depth limit; '
               'no child backend access is established. The inline role-local rehearsal uses exact '
               'criteria, covers mapping and a direct scoped read preflight. The fixture controller '
               'denies that synthetic actor to exercise a separate simulated permission failure.')
        s.save()
        return
    report = json.loads((s.path / 'verify-recovery.json').read_text())
    assert report['verdict'] == 'met'
    s.note('validate-recovery', 'Retry verification with restored fixture read permission.',
           'The recovered inline verifier fallback exercised happy and sad paths; I reviewed its evidence. '
           'Only conduct may update criteria. A fake write ACK without matching readback would not deliver anything.',
           verifier=report)
    prd = s.read(address('executive', 'prd'))
    s.write(payload(prd, prd['content'].replace('"status": "open"', '"status": "delivered"')), prd)
    s.note('validate', '', 'Synthetic validation passed, 1/1 criterion delivered in this fixture only. Ready to close?')


def failed_verify(s):
    report = json.loads((s.path / 'verify-failure.json').read_text())
    assert report['verdict'] == 'not verifiable'
    s.note('validate-failure', 'Verifier own-child access failed.',
           'GREET-001 is not verifiable through a child: actual spawn depth-limit error, no child access. '
           'The separate inline synthetic actor also observed permission-denied. '
           'No criterion is delivered, no closure. Restore access and retry; no backend fallback.', verifier=report)
    assert '"status": "open"' in s.read(address('executive', 'prd'))['content']
    s.state['denied'] = []
    s.save()


def ask_fast(s):
    baseline = digest(s.state['objects'])
    start = len(s.state['events'])
    s.catalog('executive', actor='ask')
    for kind in ('plan', 'tasks', 'walkthrough', 'prd'):
        s.read(address('executive', kind), actor='ask')
    s.note('ask', 'What work is active in this context?',
           f'Visitor greeting is active in {json.dumps(address("executive", "plan"))}; '
           'T-001 is checked and GREET-001 is delivered in the verified fixture PRD. '
           'No source or executive data changed while answering. Closure still needs confirmation.',
           citations=[dict(address=e['address'], revision=e['revision']) for e in s.catalog('executive', actor='ask')])
    s.state['denied'] = ['ask']
    result = s.tool('read', 'ask', address=address('executive', 'plan'))
    assert result['outcome'] == 'permission-denied'
    s.note('ask-failure', 'What work is active? (same question, read permission denied)',
           'The selected plan read failed with permission-denied. I cannot verify current work; '
           'this is not absence. I will not read checkout-B or local .ai as fallback.')
    s.state['denied'] = []
    assert baseline == digest(s.state['objects'])
    assert all(e.get('operation') in (None, 'catalog', 'read') for e in s.state['events'][start:])
    s.state['ask_evidence'] = {'start': start, 'end': len(s.state['events']), 'objects_digest': baseline}
    s.note('fast', 'Quick change: round the private tax calculation to two decimals; no new public API.',
           'Inline: one private helper plus its existing test module; no integration or schema ripple. '
           'This is adjacent to the fixture plan. I retain plan/tasks/walkthrough baselines, '
           'edit and test first, then ask confirmation before any executive update.')
    baselines = {k: s.read(address('executive', k)) for k in ('plan', 'tasks', 'walkthrough')}
    tests = s.path / 'test_app.py'
    tests.write_text(tests.read_text() + '\n    def test_tax_rounding(self):\n        self.assertEqual(tax(1), 0.07)\n')
    assert s.command(GATE).returncode != 0
    app = s.path / 'app.py'
    app.write_text(app.read_text().replace('return value * 0.075', 'return round(value * 0.075, 2)'))
    assert s.command(GATE).returncode == 0
    s.note('fast-confirmation', 'No, do not record it yet.',
           'The code/test change remains unrecorded. I can revert or correct it; no executive writes on refusal.')
    assert baseline == digest(s.state['objects'])
    s.note('fast-confirmation', 'The tested rounding is correct; record it now.',
           'Handoff to conduct with complete baseline objects/revisions and the proposed amendment. '
           'Fast will not write external executive objects; conduct is the sole writer.')
    old = baselines['plan']
    # Controller supplies a human edit between captured baseline and handoff.
    edited = payload(old, old['content'] + '\nHuman fixture annotation.\n')
    s.write(edited, old)
    result = s.tool('update', object=payload(old, old['content'] + '\nStale amendment.\n'),
                    expected_revision=old['revision'], request_id='fast-stale-handoff')
    assert result['outcome'] == 'conflict'
    s.note('fast-conflict', '', 'Conduct detected revision conflict. No amendment was applied, '
           'no blind retry or context switch. Re-review the new plan revision before authorizing an amendment.')
    current = s.read(old['address'])
    s.note('fast-recovery', 'I re-reviewed the annotated plan and approve the same amendment at its new revision.',
           'Conduct will preserve the human annotation and unknown fields, append next T-002 and '
           'Plan amendments/out-of-band walkthrough, then verify every full readback.')
    s.write(payload(current, current['content'] + '\n- 2026-10-18 — Round private tax helper (fast), confirmed after test.\n'), current)
    old = s.read(address('executive', 'tasks'))
    s.write(payload(old, old['content'] + '\n- [x] **T-002** — Round tax helper *(fast, out-of-band, 2026-10-18)*\n'
        '  `load: low` · `depends-on: none` · `covers: —`\n'), old)
    old = s.read(address('executive', 'walkthrough'))
    s.write(payload(old, old['content'] + '\n## Out-of-band change (fast) 2026-10-18\n'
        '**Change.** Private tax rounding requested mid-work; confirmed after refusal/review.\n'
        '**Scope touched.** app.py, test_app.py; T-002.\n**Gate.** Pass.\n'), old)
    s.save()


def close(s):
    entries = s.catalog('executive')
    frozen = [s.read(e['address']) for e in entries]
    inventory = [dict(address=o['address'], revision=o['revision'], payload_digest=digest(o)) for o in frozen]
    gate = s.read(s.state['gate_source']['address'])
    gate_pointer = (json.dumps(dict(address=gate['address'], revision=gate['revision']))
                    if s.state['layout'] == 'external' else
                    f"[quality gate](../{gate['metadata']['relative_path']}) (revision {gate['revision']})")
    summary = body('log-entry', '# Greeting fixture closed\n\n## What happened\n'
        'Named greeting and empty-name rejection implemented; private tax rounding confirmed.\n\n'
        '## Criteria delivered\n- GREET-001 — greeting/rejection — delivered (fixture only).\n\n'
        '## Phases executed\n1 — Greeting; both paths exercised.\n\n'
        '## Decisions and deviations\nReadback divergence and handoff conflict reconciled before progress.\n\n'
        '## ADR proposals & brain updates\nNo ADR proposed; all decisions were tactical.\n\n'
        f'## Pointers\n{gate_pointer}\nSynthetic rehearsal transcript; no real PRD delivery claimed.\n\n'
        '## Suggested final commit\n`feat: greet named visitors` (not executed).\n\n'
        '## Gate at close\nPass.\n', date='2026-10-18', kind='work-closure', depth='spec', adr='none')
    s.note('summarize-present', 'Close the work.', summary,
           proposed_log=address('constitutive', '2026-10-18-greeting'), close_id='2026-10-18-greeting',
           inventory=inventory, confirmation_question='Append this exact payload, verify it and clear only this unchanged inventory?')
    baseline = digest(s.state['objects'])
    s.note('summarize-refusal', 'No, keep it open.', 'No append or clear. All executive objects retained.')
    assert baseline == digest(s.state['objects'])
    s.note('summarize-confirmation', 'Yes, append that payload and clear only that inventory.',
           'I will append, exact full-read back, retain archive evidence, re-enumerate, then selectively clear.')
    if s.state['layout'] != 'external':
        import os
        import subprocess
        draft = s.path / '.ai/work/greeting-summary.md'
        draft.write_text(summary)
        env = dict(os.environ, JAIBA_ARCHIVE_FILESYSTEM='1', JAIBA_ARCHIVE_SERIALIZED='1')
        for mode in ('prepare', 'archive', 'archive'):
            argv = ['bash', str(ROOT / 'skills/conduct/scripts/archive.sh'), mode, SLUG, PROJECT, CONTEXT]
            if mode == 'prepare':
                # Prepare precedes the actual final presentation/confirmation.
                result = subprocess.run(argv, cwd=s.path, env=env, capture_output=True, text=True)
                assert result.returncode == 0, result.stderr
                s.state['events'].append(dict(kind='command', argv=argv, cwd=str(s.path),
                    env_attestations=['filesystem', 'serialized'], returncode=result.returncode,
                    stdout=result.stdout, stderr=result.stderr))
                s.note('summarize-prepared-presentation', 'Present prepared filesystem receipt before archive.',
                       draft.read_text(), synthetic_confirmation='Yes, append this prepared payload and clear this frozen inventory.')
            else:
                result = subprocess.run(argv, cwd=s.path, env=env, capture_output=True, text=True)
                assert result.returncode == 0, result.stderr
                s.state['events'].append(dict(kind='command', argv=argv, cwd=str(s.path),
                    env_attestations=['filesystem', 'serialized'], returncode=result.returncode,
                    stdout=result.stdout, stderr=result.stderr))
        assert list((s.path / '.ai/work').iterdir()) == [s.path / '.ai/work/.gitignore']
        log = s.path / '.ai/memory/log/2026-10-18-greeting.md'
        assert log.read_text().startswith(summary)
        # Reflect physical helper outcome in transport journal, not another write.
        s.state['filesystem_log'] = log.read_text()
        for o in frozen:
            del s.state['objects'][json.dumps(o['address'])]
    else:
        log = obj('constitutive', '2026-10-18-greeting', 'log-entry', summary)
        log['metadata'].update(close_id='2026-10-18-greeting', inventory=inventory)
        saved = s.write(log, operation='append-log')
        s.note('summarize-interruption', 'Interrupt after verified append, before clear.',
               'The immutable log is verified; executive work remains. Retry with the same close ID and identical payload.')
        assert s.catalog('executive') == entries
        receipt = s.tool('append-log', object=log, request_id='2026-10-18-greeting')
        assert receipt['resulting_revision'] == saved['revision']
        assert s.read(saved['address']) == saved
        conflict = s.tool('append-log', object=payload(saved, summary + 'changed'), request_id='2026-10-18-greeting')
        assert conflict['outcome'] == 'conflict'
        archive = s.tool('archive', address=address('executive', 'plan'),
            close_id='2026-10-18-greeting', log_address=saved['address'],
            log_revision=saved['revision'], inventory=inventory)
        assert archive['outcome'] == 'ok'
        # Changed inventory is caught even after a verified log; restore only by explicit synthetic reconciliation.
        old = s.read(address('executive', 'walkthrough'))
        changed = s.write(payload(old, old['content'] + '\nController inventory-change fault.\n'), old)
        blocked = s.tool('clear-work', address=address('executive', 'plan'),
                         archive_receipt=archive, request_id='blocked-clear')
        assert blocked['outcome'] == 'inventory-conflict'
        s.note('summarize-inventory-conflict', 'Synthetic confirmation to restore only the controller fault.',
               'Cleanup stopped with every object retained. Restore the exact frozen content after review, '
               'then re-read inventory; do not change the immutable closing log.')
        s.write(payload(old, old['content']), changed)
        assert s.catalog('executive') == entries
        for item in inventory:
            assert s.read(item['address'])['revision'] == item['revision']
            assert s.tool('clear-work', address=item['address'], archive_receipt=archive,
                          request_id='clear-' + item['address'][-1])['outcome'] == 'ok'
            assert s.tool('read', address=item['address'])['outcome'] == 'not-found'
        assert not s.catalog('executive')
        assert s.read(saved['address']) == saved
        assert not (s.path / '.ai').exists() and not (s.path / 'AGENTS.md').exists()
    for key, old in s.state['constitutive_baseline'].items():
        assert s.state['objects'][key] == old
        if s.state['layout'] != 'external':
            assert s.locator(old).read_text() == old['content']
    other = next(v for v in s.state['seed_objects'].values() if v['address'][3] == 'checkout-B')
    assert s.state['objects'][json.dumps(other['address'])] == other
    assert s.state['ordinary_witness'] == {'namespace': 'ordinary-host', 'body': 'do not adopt or clear'}
    s.note('summarize-complete', '', 'Verified closure of this fixture only; other context and ordinary witness intact. '
           'No migration, production backend assay, global installation or real project memory was performed.')
    s.save()


if __name__ == '__main__':
    s = Session(sys.argv[1])
    stage = sys.argv[2]
    if stage == 'seed':
        seed(s, sys.argv[3])
    else:
        {'spec': spec, 'tasks': tasks, 'integrate': integrate, 'validate': validation,
         'failed-verify': failed_verify, 'validate-recovery': lambda x: validation(x, True),
         'ask-fast': ask_fast, 'close': close}[stage](s)
    print(json.dumps({'stage': stage, 'scratch': str(s.path), 'events': len(s.state['events']),
                      'objects': len(s.state['objects'])}))
