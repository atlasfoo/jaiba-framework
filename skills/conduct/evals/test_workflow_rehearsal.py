"""Structural/action assertions on immutable historical turns + fixed-decision replay.

Requires /usr/bin/python3 only (stdlib; `json` parses the fenced
JSON-compatible blocks). Does not call an LLM, spawn children, contact a
backend, or claim adapter/model conformance.
"""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

from capture_rehearsal import FIXTURES, load
from surface_rehearsal import Session, ROOT, PARENT, address, digest
import rehearse_workflows as workflow
import rehearsal_fallbacks as fallback


def tools(events, operation=None):
    return [e for e in events if e['kind'] == 'tool' and
            (operation is None or e['operation'] == operation)]


def segment(events, phase):
    start = next(i for i, e in enumerate(events) if e.get('phase') == phase)
    end = next((i for i in range(start + 1, len(events)) if events[i]['kind'] == 'model-turn'), len(events))
    return events[start:end]


def frontmatter(content):
    """Minimal flat `key: value` frontmatter reader (no external YAML dependency)."""
    out = {}
    for line in content.split('---\n', 2)[1].splitlines():
        if ':' in line and not line.startswith((' ', '#')):
            key, _, value = line.partition(':')
            out[key.strip()] = value.strip().strip('\'"')
    return out


def yaml_json_block(content):
    """Fenced yaml block emitted as JSON (valid YAML); parsed with json."""
    return json.loads(re.search(r'```yaml\n(.*?)\n```', content, re.S)[1])


class HistoricalCapturedRehearsal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.journals = {p.stem: load(p) for p in FIXTURES.glob('*.json')
                        if p.name not in ('index.json', 'reviewed-source-drift.json')}
        assert set(cls.journals) == {'external', 'bundle', 'legacy'}

    def test_historical_source_profile_has_only_exact_reviewed_drift(self):
        manifest = json.loads((FIXTURES / 'reviewed-source-drift.json').read_text())
        provenance = {
            'skills/create-memory/references/filesystem-surface.md': 'T-083',
            'skills/create-memory/references/resolution.md': 'T-024',
            'skills/conduct/references/execute-mode.md': 'T-024',
            'skills/conduct/references/summarize-mode.md': 'T-024',
            'skills/create-memory/references/memory-surface-contract.md': 'T-083',
        }
        self.assertIn('predate T-023 and T-024', manifest['review_scope'])
        self.assertNotIn('T-033 is the provenance', manifest['review_scope'])
        index_path = FIXTURES / 'index.json'
        self.assertEqual(hashlib.sha256(index_path.read_bytes()).hexdigest(),
                         manifest['immutable_recordings_sha256_raw_bytes']['index.json'])
        index = json.loads(index_path.read_text())
        recorded = next(iter(index['fixtures'].values()))['sources']
        self.assertEqual(set(manifest['changed_sources']) | set(manifest['unchanged_source_paths']), set(recorded))
        for layout, journal in self.journals.items():
            self.assertEqual(journal['source_revisions'], recorded, f'{layout}: altered historical source profile')
            indexed = index['fixtures'][layout]
            packaged = json.loads((FIXTURES / indexed['file']).read_text())
            self.assertEqual(digest(journal), indexed['digest'], f'{layout}: journal/index mismatch')
            self.assertEqual(hashlib.sha256((FIXTURES / indexed['file']).read_bytes()).hexdigest(),
                             manifest['immutable_recordings_sha256_raw_bytes'][indexed['file']])
            self.assertEqual(indexed['events'], len(journal['events']))
            self.assertEqual(digest(journal), packaged['journal_digest'])
        for path, old in recorded.items():
            current = digest((ROOT / path).read_text())
            if path in manifest['changed_sources']:
                pair = manifest['changed_sources'][path]
                self.assertEqual(pair['recorded_source_sha256'], old)
                self.assertEqual(pair['current_source_sha256'], current, f'unreviewed future drift: {path}')
                task = provenance[path]
                self.assertEqual(pair['classification'], f'known post-recording {task} source change')
                self.assertTrue(pair['reason'].startswith(f'{task}:'))
            else:
                self.assertEqual(current, old, f'unreviewed future drift: {path}')
        self.assertEqual(set(manifest['changed_sources']), set(provenance))

    def test_historical_consumer_release_state_and_legacy_eval_scopes(self):
        canonical = (ROOT / 'skills/jaiba-configure/assets/jaiba-contract.md').read_bytes()
        self.assertEqual(canonical, (ROOT / 'skills/doctor/assets/jaiba-contract.md').read_bytes())
        text = canonical.decode()
        self.assertNotIn('`conduct`, `ask` and `fast` remain gated', text)
        self.assertIn('Draft categories are not conforming selectable mutable adapters.', text)
        self.assertIn('`jaiba-engram-memory` remains `memory-surface-draft`', text)
        for skill, last in [('conduct', 23), ('ask', 8), ('fast', 6)]:
            data = json.loads((ROOT / f'skills/{skill}/evals/evals.json').read_text())
            self.assertEqual(data['filesystem_scoped_eval_ids'], list(range(1, last + 1)))
            self.assertEqual([e['id'] for e in data['evals']], list(range(1, len(data['evals']) + 1)))
        for skill, eval_id in [('create-memory', 7), ('jaiba-init', 22),
                               ('jaiba-engram-memory', 4), ('conduct', 27)]:
            eval_path = ROOT / f'skills/{skill}/evals/evals.json'
            entry = next(e for e in json.loads(eval_path.read_text())['evals'] if e['id'] == eval_id)
            references = list(entry.get('files', []))
            references.extend(entry.get('context', {}).get(k) for k in ('fixture', 'validator'))
            for reference in filter(None, references):
                self.assertTrue((eval_path.parent / reference).resolve().is_file(),
                                f'{skill} eval {eval_id}: unresolved reference {reference}')

    def test_current_migration_source_guard_is_static_not_conformance(self):
        migration = (ROOT / 'skills/jaiba-init/references/surface-migration.md').read_text().lower()
        for required in ('complete target enumeration', 'full readback', 'new explicit\nhuman approval to activate this verified manifest revision',
                         'source remains authoritative', 'source and staging', 'same transaction',
                         'registry', 'stale-snapshot recovery'):
            self.assertIn(required, migration)
        self.assertNotIn('not implemented until phase5', migration)
        init = (ROOT / 'skills/jaiba-init/SKILL.md').read_text().lower()
        self.assertIn('migrate-surface', init)
        engram = (ROOT / 'skills/jaiba-engram-memory/SKILL.md').read_text().lower()
        self.assertIn('not selectable', engram)
        self.assertRegex(migration, r'adapter files,\s*test fixtures and host memory bookkeeping are not backend evidence')

    def test_propose_and_refusal_have_zero_artifact_mutations(self):
        for journal in self.journals.values():
            events = journal['events']
            spec_start = next(i for i, e in enumerate(events) if e.get('phase') == 'spec')
            self.assertFalse(any(e['operation'] in ('create', 'update', 'append-log', 'clear-work')
                                 for e in tools(events[:spec_start])))
            self.assertEqual(segment(events, 'propose')[0]['kind'], 'model-turn')
            self.assertFalse(tools(segment(events, 'spec-approval'), 'update'))
            self.assertFalse(tools(segment(events, 'summarize-refusal'), 'append-log'))
            self.assertFalse(tools(segment(events, 'summarize-refusal'), 'clear-work'))

    def test_full_artifact_schemas_approval_and_gate_provenance(self):
        for journal in self.journals.values():
            mutations = tools(journal['events'], 'create') + tools(journal['events'], 'update')
            kinds = {e['request']['object']['type'] for e in mutations}
            self.assertTrue({'prd', 'plan', 'tasks', 'walkthrough'} <= kinds)
            for e in mutations:
                o = e['request']['object']
                self.assertEqual(o['metadata']['extension'], {'retain': ['α', 7]})
                self.assertIn('relations', o)
                fm = frontmatter(o['content'])
                self.assertEqual(fm['type'], o['type'])
                if o['type'] == 'prd':
                    criteria = yaml_json_block(o['content'])['criteria']
                    self.assertEqual([c['id'] for c in criteria], ['GREET-001'])
                    self.assertTrue(criteria[0]['happy'] and criteria[0]['sad'])
                    self.assertEqual(set(criteria[0]['happy'][0]), {'given', 'when', 'then'})
                if o['type'] == 'tasks':
                    self.assertIn('`load: low` · `depends-on: none` · `covers: GREET-001`', o['content'])
                    self.assertIn(workflow.GATE_TEXT, o['content'])
                    self.assertIn(journal['gate_source']['revision'], o['content'])
            # Every verified regular mutation has full exact readback before later progress.
            events = journal['events']
            for i, e in enumerate(events):
                if e not in mutations or e['result']['outcome'] != 'ok':
                    continue
                later = tools(events[i+1:], 'read')
                read = next(x for x in later if x['request']['address'] == e['request']['object']['address'])
                if e['request']['request_id'] != 'divergence-assay':
                    self.assertEqual(read['result']['object']['revision'], e['result']['resulting_revision'])
                    expected = dict(e['request']['object'], revision=e['result']['resulting_revision'])
                    self.assertEqual(read['result']['object'], expected)

    def test_execute_divergence_stops_before_gate_or_checkbox(self):
        for journal in self.journals.values():
            events = segment(journal['events'], 'execute')
            # The first execute turn includes the deliberately divergent walkthrough ACK/read.
            self.assertTrue(tools(events, 'update'))
            stopped = [e for e in journal['events'] if e.get('phase') == 'execute' and
                       'Verification failed.' in e['actual_executor_model_output']][0]
            start = journal['events'].index(stopped)
            recovery = next(i for i, e in enumerate(journal['events']) if e.get('phase') == 'execute-recovery')
            blocked = journal['events'][start:recovery]
            self.assertFalse(any(e['kind'] == 'command' for e in blocked))
            self.assertFalse(tools(blocked, 'update'))
            self.assertIn('- [ ] **T-001**', tools(blocked, 'read')[0]['result']['object']['content'])

    def test_actual_dispatch_failure_is_not_child_backend_evidence(self):
        for journal in self.journals.values():
            report = next(e['report'] for e in journal['events'] if e.get('phase') == 'analyst-fallback')
            self.assertEqual(report['dispatch']['child_id'], None)
            self.assertIn('depth limit reached (1)', report['dispatch']['error'])
            self.assertEqual(report['dispatch']['child_backend_access'], 'not established')
            executor = next(e['report'] for e in journal['events'] if e.get('phase') == 'executor-fallback')
            self.assertEqual(executor['load'], 'low')
            self.assertEqual(executor['dispatch']['roles'], ['executor-low'])
            self.assertIn('NOT inheritance verified', executor['backend'])

    def test_validate_failure_and_recovery_use_full_criteria_not_ack(self):
        for journal in self.journals.values():
            events = journal['events']
            failure = segment(events, 'validate-failure')
            self.assertFalse(tools(failure, 'update'))
            self.assertIn('"status": "open"', tools(failure, 'read')[0]['result']['object']['content'])
            reports = [e['report'] for e in events if e.get('phase') == 'verify-role-local-rehearsal']
            self.assertEqual([r['verdict'] for r in reports], ['not verifiable', 'met'])
            self.assertEqual(reports[0]['observed_preflight']['outcome'], 'permission-denied')
            self.assertEqual(reports[1]['source_criteria'], journal['criteria_schema'])
            self.assertEqual(set(reports[1]['paths']), {'happy', 'sad'})
            self.assertEqual(reports[1]['gate']['returncode'], 0)
            self.assertIn('NOT child', reports[1]['actor'])
            self.assertFalse(reports[1]['executive_writes'])

    def test_ask_read_only_exact_context_and_failure_without_fallback(self):
        for journal in self.journals.values():
            span = journal['ask_evidence']
            events = journal['events'][span['start']:span['end']]
            self.assertTrue(tools(events, 'catalog'))
            self.assertFalse(any(e['kind'] == 'command' for e in events))
            self.assertTrue(all(e['operation'] in ('catalog', 'read') for e in tools(events)))
            for e in tools(events):
                self.assertEqual(e['before_digest'], e['after_digest'])
                a = e['request'].get('address', e['request'].get('scope'))
                self.assertEqual(a[3], 'checkout-A')
            answer = next(e for e in events if e.get('phase') == 'ask')
            self.assertIn('T-001 is checked', answer['actual_executor_model_output'])
            self.assertTrue(all(c['revision'] for c in answer['citations']))
            self.assertIn('not absence', next(e for e in events if e.get('phase') == 'ask-failure')['actual_executor_model_output'])

    def test_fast_actual_code_test_confirmation_handoff_conflict(self):
        for journal in self.journals.values():
            events = journal['events']
            start = next(i for i, e in enumerate(events) if e.get('phase') == 'fast')
            refused = next(i for i, e in enumerate(events) if e.get('phase') == 'fast-confirmation')
            before_confirm = events[start:refused]
            self.assertFalse(tools(before_confirm, 'update'))
            commands = [e for e in before_confirm if e['kind'] == 'command']
            self.assertEqual([e['returncode'] == 0 for e in commands], [False, True])
            self.assertIn('test_tax_rounding', commands[1]['stderr'])
            conflict = next(e for e in tools(events, 'update') if e['request']['request_id'] == 'fast-stale-handoff')
            self.assertEqual(conflict['result']['outcome'], 'conflict')
            self.assertEqual(conflict['before_digest'], conflict['after_digest'])
            self.assertTrue(all(e['actor'] == 'conduct' for e in tools(events, 'update')))
            lasttasks = [e for e in tools(events, 'update') if e['result']['outcome'] == 'ok' and
                         e['request']['object']['type'] == 'tasks'][-1]['request']['object']['content']
            self.assertIn('**T-001**', lasttasks)
            self.assertIn('**T-002**', lasttasks)

    def test_summarize_external_order_idempotency_and_isolation(self):
        j = self.journals['external']
        events = j['events']
        append = tools(events, 'append-log')
        self.assertEqual(len(append), 3)
        self.assertEqual(append[0]['result']['resulting_revision'], append[1]['result']['resulting_revision'])
        self.assertEqual(append[2]['result']['outcome'], 'conflict')
        clear = tools(events, 'clear-work')
        self.assertEqual(clear[0]['result']['outcome'], 'inventory-conflict')
        self.assertEqual(len([e for e in clear if e['result']['outcome'] == 'ok']), 4)
        self.assertTrue(all(e['actor'] == 'conduct' for e in append + clear))
        archive = tools(events, 'archive')[0]
        frozen = archive['result']['inventory']
        self.assertEqual(len(frozen), 4)
        self.assertTrue(all(i['payload_digest'] for i in frozen))
        self.assertLess(events.index(append[0]), events.index(archive))
        self.assertLess(events.index(archive), events.index(clear[0]))
        self.assertFalse(any(e['kind'] == 'command' and any('archive.sh' in a for a in e['argv']) for e in events))
        self.assertEqual(j['ordinary_witness']['namespace'], 'ordinary-host')
        self.assertEqual(len([o for o in j['objects'].values() if o['address'][2] == 'executive']), 1)
        for key, o in j['constitutive_baseline'].items():
            self.assertEqual(j['objects'][key], o)

    def test_filesystem_helper_keeps_both_layouts_full_artifacts_and_retry(self):
        for layout in ('bundle', 'legacy'):
            j = self.journals[layout]
            calls = [e for e in j['events'] if e['kind'] == 'command' and any('archive.sh' in a for a in e['argv'])]
            self.assertEqual([e['argv'][2] for e in calls], ['prepare', 'archive', 'archive'])
            self.assertTrue(all(e['returncode'] == 0 for e in calls))
            self.assertIn('jaiba-close-v1', j['filesystem_log'])
            self.assertTrue(all(e['argv'][-2:] == [address('executive', 'plan')[1], 'checkout-A'] for e in calls))
            for key, o in j['constitutive_baseline'].items():
                self.assertEqual(j['objects'][key], o)
            if layout == 'legacy':
                constitution = next(o for o in j['constitutive_baseline'].values() if o['type'] == 'project')
                self.assertFalse(constitution['content'].startswith('---'))


class ActionReplay(unittest.TestCase):
    def test_replay_historical_recorded_model_decisions_all_three_surfaces(self):
        PARENT.mkdir(parents=True, exist_ok=True)
        run = Path(tempfile.mkdtemp(prefix='replay-', dir=PARENT))
        for layout in ('external', 'bundle', 'legacy'):
            with self.subTest(layout=layout):
                s = Session(run / layout)
                workflow.seed(s, layout)
                s.state['run_kind'] = 'fixed-decision action replay; no fresh model or child dispatch'
                s.save()
                fallback.analysis(s)
                workflow.spec(s)
                workflow.tasks(s)
                fallback.executor(s)
                workflow.integrate(s)
                workflow.validation(s)
                fallback.verify(s)
                workflow.failed_verify(s)
                fallback.verify(s, True)
                workflow.validation(s, True)
                workflow.ask_fast(s)
                workflow.close(s)
                self.assertEqual(s.state['events'][-1]['phase'], 'summarize-complete')
                if layout == 'external':
                    self.assertFalse((s.path / '.ai').exists())
                    self.assertFalse((s.path / 'AGENTS.md').exists())
                else:
                    self.assertEqual([p.name for p in (s.path / '.ai/work').iterdir()], ['.gitignore'])
        print(f'Fixed-decision replay scratch: {run}')


if __name__ == '__main__':
    unittest.main(verbosity=2)
