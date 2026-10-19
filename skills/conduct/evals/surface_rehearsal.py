"""Generic scratch transport and journal for an executor-as-consumer rehearsal.

No workflow routing/approval/criteria decisions live in this transport. The
model supplies those decisions, full payloads and individual operations. JSON
journals are replay evidence, NOT a model runner or adapter certification.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
PARENT = Path('/tmp/opencode/jaiba-memory-surfaces/phase4-t021')
NAMESPACE = 'jaiba-owned-rehearsal'
PROJECT = 'fixture:code.example/Team/Greeting'
CONTEXT = 'checkout-A'
CONTRACT = 'jaiba-memory-surface/1.0.0'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


def address(category, logical_id, context=CONTEXT):
    return [NAMESPACE, PROJECT, category,
            context if category == 'executive' else None, logical_id]


def obj(category, logical_id, kind, body, context=CONTEXT):
    return dict(address=address(category, logical_id, context), type=kind,
                metadata={'owner': 'JAIBA', 'extension': {'retain': ['α', 7]}},
                relations=[], content=body)


class Session:
    def __init__(self, path):
        self.path = Path(path).resolve()
        if not self.path.is_relative_to(PARENT) or self.path == PARENT:
            raise ValueError('scratch-only transport')
        self.path.mkdir(parents=True, exist_ok=True)
        self.file = self.path / 'transport.json'
        self.state = json.loads(self.file.read_text()) if self.file.exists() else {
            'objects': {}, 'events': [], 'denied': [], 'sequence': 0,
            'revision_model': 'sha256 complete logical envelope; no normalization; serialized, NOT CAS',
            'binding': 'fixture-vault/1 (simulated external transport)',
            'ordinary_witness': {'namespace': 'ordinary-host', 'body': 'do not adopt or clear'},
        }

    def save(self):
        self.file.write_text(json.dumps(self.state, ensure_ascii=False, indent=2) + '\n')

    def note(self, phase, user, assistant, **evidence):
        self.state['events'].append(dict(kind='model-turn', phase=phase,
            synthetic_user=user, actual_executor_model_output=assistant, **evidence))
        self.save()

    def tool(self, operation, actor='conduct', **request):
        """Exact generic object operations; errors are recorded, never hidden."""
        before = copy.deepcopy(self.state['objects'])
        try:
            result = self._operate(operation, actor, request)
        except (ValueError, KeyError) as exc:
            result = {'outcome': str(exc).strip("'"), 'complete': False}
        self.state['sequence'] += 1
        self.state['events'].append(dict(kind='tool', sequence=self.state['sequence'],
            operation=operation, actor=actor, request=request, result=result,
            before_digest=digest(before), after_digest=digest(self.state['objects'])))
        self.save()
        return copy.deepcopy(result)

    def _operate(self, op, actor, r):
        objects = self.state['objects']
        if op == 'probe':
            return dict(outcome='ok', contract=CONTRACT, binding=self.state['binding'],
                        namespace=NAMESPACE, project=PROJECT, context=CONTEXT,
                        permissions='fixture-only', consistency='serialized writer',
                        limits='UTF-8 JSON, scratch disk capacity; no normalization',
                        capabilities=['catalog', 'read', 'create', 'update', 'append-log',
                                      'archive', 'clear-work'],
                        unexercised=['export', 'import'], mutable_conformance='NOT certified')
        scope = r.get('scope')
        a = r.get('address') or r.get('object', {}).get('address')
        if (scope or a)[:2] != [NAMESPACE, PROJECT]:
            raise ValueError('ownership-error')
        if actor in self.state['denied']:
            raise ValueError('permission-denied')
        if op == 'catalog':
            entries = [dict(address=o['address'], type=o['type'], revision=o['revision'],
                            locator={'exact_address': o['address']})
                       for o in objects.values() if o['address'][:len(scope)] == scope
                       and (not r.get('type') or o['type'] == r['type'])]
            entries.sort(key=lambda x: json.dumps(x['address']))
            offset = r.get('offset', 0)
            page = entries[offset:offset+2]
            end = offset + len(page)
            return dict(outcome='ok', entries=page, complete=end == len(entries),
                        continuation=None if end == len(entries) else end,
                        snapshot=digest(objects), scope=scope)
        key = json.dumps(a)
        old = objects.get(key)
        if op == 'read':
            return dict(outcome='ok', complete=True, object=old) if old else dict(
                outcome='not-found', complete=True, address=a)
        if op in ('create', 'update', 'append-log'):
            new = copy.deepcopy(r['object'])
            assert set(new) == {'address', 'type', 'metadata', 'relations', 'content'}
            if a[2] == 'executive' and actor != 'conduct':
                raise ValueError('single-writer-error')
            if a[2] == 'constitutive' and not (op == 'append-log' and actor == 'conduct'
                                              and new['type'] == 'log-entry'):
                raise ValueError('constitutive-authority-error')
            if op == 'create' and old:
                raise ValueError('conflict')
            if op == 'update':
                if not old:
                    raise ValueError('not-found')
                if old['revision'] != r['expected_revision']:
                    raise ValueError('conflict')
            new['revision'] = digest(new)
            if op == 'append-log' and old and new != old:
                raise ValueError('conflict')
            objects[key] = new
            self.materialize(new)
            return dict(outcome='ok', contract=CONTRACT, binding=self.state['binding'],
                        operation=op, address=a, request_id=r['request_id'],
                        previous_revision=old['revision'] if old else 'verified-absent',
                        resulting_revision=new['revision'], payload_digest=digest(new))
        if op == 'archive':
            log = objects.get(json.dumps(r['log_address']))
            if not log or log['revision'] != r['log_revision']:
                raise ValueError('verification-failed')
            if log['metadata'].get('inventory') != r['inventory']:
                raise ValueError('inventory-conflict')
            return dict(outcome='ok', contract=CONTRACT, binding=self.state['binding'],
                        address=a, close_id=r['close_id'], log_address=r['log_address'],
                        log_revision=r['log_revision'], inventory=r['inventory'])
        if op == 'clear-work':
            receipt = r['archive_receipt']
            log = objects.get(json.dumps(receipt['log_address']))
            if not log or log['revision'] != receipt['log_revision']:
                raise ValueError('verification-failed')
            inventory = receipt['inventory']
            scope = a[:4]
            current = [o for o in objects.values() if o['address'][:4] == scope]
            known = {json.dumps(i['address']): i['revision'] for i in inventory}
            if any(known.get(json.dumps(o['address'])) != o['revision'] for o in current):
                raise ValueError('inventory-conflict')
            if key not in known or not old or old['revision'] != known[key]:
                raise ValueError('conflict')
            del objects[key]
            if self.state.get('layout') != 'external':
                self.locator(old).unlink()
            return dict(outcome='ok', address=a, previous_revision=old['revision'],
                        request_id=r['request_id'], contract=CONTRACT,
                        binding=self.state['binding'], resulting_revision='verified-absent')
        raise ValueError('unsupported-operation')

    def locator(self, o):
        a = o['address']
        if a[2] == 'executive':
            name = {'prd': 'PRD.md', 'plan': 'plan.md', 'tasks': 'tasks.md',
                    'walkthrough': 'walkthrough.md'}[o['type']]
            return self.path / '.ai/work' / name
        return self.path / '.ai/memory' / o['metadata']['relative_path']

    def materialize(self, o):
        if self.state.get('layout', 'external') == 'external':
            return
        # External unrelated-context witness is not a second local work root.
        if o['address'][2] == 'executive' and o['address'][3] != CONTEXT:
            return
        p = self.locator(o)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(o['content'])

    def seed(self, objects, layout):
        assert not self.state['objects']
        self.state['layout'] = layout
        for o in objects:
            o = copy.deepcopy(o)
            o['revision'] = digest(o)
            self.state['objects'][json.dumps(o['address'])] = o
            self.materialize(o)
        if layout != 'external':
            (self.path / 'AGENTS.md').write_text('JAIBA synthetic marker; global contract reference.\n')
            work = self.path / '.ai/work'
            work.mkdir(parents=True, exist_ok=True)
            (work / '.gitignore').write_text('*\n!.gitignore\n')
        self.save()

    def catalog(self, category, context=CONTEXT, actor='conduct', kind=None):
        scope = [NAMESPACE, PROJECT, category]
        if category == 'executive':
            scope.append(context)
        entries, offset, snapshot = [], 0, None
        while True:
            result = self.tool('catalog', actor, scope=scope, type=kind, offset=offset)
            assert result['outcome'] == 'ok', result
            assert snapshot in (None, result['snapshot'])
            snapshot = result['snapshot']
            entries.extend(result['entries'])
            if result['complete']:
                assert result['continuation'] is None
                return entries
            offset = result['continuation']

    def read(self, a, actor='conduct'):
        result = self.tool('read', actor, address=a)
        assert result['outcome'] == 'ok' and result['complete'], result
        return result['object']

    def write(self, o, previous=None, operation=None):
        """Caller must supply intended object and baseline, no approval decision here."""
        a = o['address']
        baseline = self.tool('read', address=a)
        if previous is None:
            assert baseline['outcome'] == 'not-found', baseline
        else:
            assert baseline['object'] == previous, 'baseline changed'
        receipt = self.tool(operation or ('update' if previous else 'create'), object=o,
            expected_revision=previous['revision'] if previous else None,
            request_id=(o['metadata']['close_id'] if operation == 'append-log'
                        else f"model-request-{self.state['sequence']}"))
        assert receipt['outcome'] == 'ok', receipt
        actual = self.read(a)
        intended = dict(o, revision=digest(o))
        assert actual == intended and receipt['resulting_revision'] == actual['revision']
        return actual

    def command(self, argv):
        result = subprocess.run(argv, cwd=self.path, text=True, capture_output=True)
        self.state['events'].append(dict(kind='command', argv=argv, cwd=str(self.path),
            returncode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        self.save()
        return result


if __name__ == '__main__':
    # Children have a real callable scratch CLI, never a production MCP alias.
    session = Session(sys.argv[1])
    request = json.loads(sys.argv[2])
    print(json.dumps(session.tool(**request), ensure_ascii=False, indent=2))
