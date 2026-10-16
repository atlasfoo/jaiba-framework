#!/usr/bin/env python3
"""Exercise the workflow's actual bash blocks against isolated command mocks."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[5]
WORKFLOW = ROOT / ".github/workflows/bump.yml"


def blocks():
    lines = WORKFLOW.read_text().splitlines()
    found = {}
    current = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("      - name: "):
            current = line.split(": ", 1)[1]
        if current in ("Bump version", "Publish GitHub Release") and line.strip() == "run: |":
            indent = len(line) - len(line.lstrip()) + 2
            i += 1
            body = []
            while i < len(lines) and (not lines[i].strip() or len(lines[i]) - len(lines[i].lstrip()) >= indent):
                body.append(lines[i][indent:] if lines[i].strip() else "")
                i += 1
            found[current] = "\n".join(body) + "\n"
            continue
        i += 1
    assert len(found) == 2, f"Expected two relevant run blocks; found {list(found)}"
    return found


MOCK = r'''#!/usr/bin/env python3
import os, sys, json
name=os.path.basename(sys.argv[0]); a=sys.argv[1:]; s=os.environ['STATE']; d=json.load(open(s)); mode=os.environ['CASE']
def save(): json.dump(d,open(s,'w'))
def log(x): open(os.environ['CALLS'],'a').write(x+'\n')
if name=='cz':
    log('cz '+ ' '.join(a))
    if mode=='no-bump': sys.exit(0)
    d['head']='bumped'; d['tags']['v2.0.0']={'subject':os.environ['MARKER'],'commit':'bumped'}; save(); sys.exit(0)
if name=='git':
    log('git '+' '.join(a))
    if a[:2]==['rev-parse','HEAD']: print(d['head']); sys.exit()
    if a[:2]==['rev-parse','refs/tags/v2.0.0^{}^']: print('sha'); sys.exit()
    if a[0]=='rev-parse' and a[1].startswith('refs/tags/'):
        tag=a[1].split('/')[2].split('^')[0]; print(d['tags'][tag]['commit']); sys.exit()
    if a[0]=='for-each-ref':
        for t,v in d['tags'].items(): print(t+' tag '+v['subject'])
        sys.exit()
    if a[0]=='tag' and a[1]=='--list': print('\n'.join(d['tags'])); sys.exit()
    if a[0]=='push':
        if mode=='push-failure': sys.exit(1)
        d['remote'].append(a[-1].split(':')[-1].removeprefix('refs/tags/')); save(); sys.exit()
    sys.exit(0)
if name=='gh':
    log('gh '+' '.join(a))
    if a[:2]==['api','--paginate']:
        if mode in ('api-error','auth-error'): print('API failure',file=sys.stderr); sys.exit(1)
        print('\n'.join(d['releases'])); sys.exit()
    if a[:2]==['release','create']:
        if mode=='create-failure' and not d.get('failed_once'):
            d['failed_once']=True; save(); sys.exit(1)
        tag=a[2];
        if tag not in d['remote']: print('tag absent',file=sys.stderr); sys.exit(1)
        d['releases'].append(tag); save(); sys.exit()
'''


def run_case(name, b, retry=False):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td); binpath = p / "bin"; binpath.mkdir()
        dispatcher = binpath / "dispatcher"; dispatcher.write_text(MOCK); dispatcher.chmod(0o755)
        for cmd in ("git", "gh", "cz"):
            (binpath / cmd).symlink_to(dispatcher)
        marker = "JAIBA release run 7 (sha)"
        state = {"head": "sha", "tags": {}, "remote": [], "releases": []}
        if name == "existing-release": state.update(head="bumped", tags={"v2.0.0":{"subject":marker,"commit":"bumped"}}, remote=["v2.0.0"], releases=["v2.0.0"])
        if name == "missing-remote": state.update(head="bumped", tags={"v2.0.0":{"subject":marker,"commit":"bumped"}})
        if retry: state.update(head="bumped", tags={"v2.0.0":{"subject":marker,"commit":"bumped"}}, remote=["v2.0.0"])
        sf=p/'state'; sf.write_text(__import__('json').dumps(state)); calls=p/'calls'; calls.write_text('')
        env=os.environ.copy(); env.update(PATH=str(binpath)+':'+env['PATH'], STATE=str(sf), CALLS=str(calls), CASE=name, MARKER=marker, GITHUB_RUN_ID='7', GITHUB_SHA='sha', RUNNER_TEMP=td, GITHUB_OUTPUT=str(p/'output'), GH_REPO='org/repo', GH_TOKEN='mock', RELEASE_TAG='v2.0.0')
        def execute(script): return subprocess.run(['bash','-e'], input=script, text=True, env=env, capture_output=True)
        bump=execute(b['Bump version'])
        assert bump.returncode == 0, f"{name}: bump: {bump.stderr}"
        out=(p/'output').read_text() if (p/'output').exists() else ''
        if name=='no-bump': assert not out and 'cz ' in calls.read_text(); return
        assert 'tag=v2.0.0' in out, (name,out)
        if 'push=true' in out:
            push=subprocess.run(['git','push','--atomic','origin','HEAD:refs/heads/master','refs/tags/v2.0.0:refs/tags/v2.0.0'],env=env,capture_output=True,text=True)
            if name=='push-failure': assert push.returncode; return
            assert push.returncode==0, name
        release=execute(b['Publish GitHub Release'])
        if name in ('api-error','auth-error','missing-remote'):
            assert release.returncode != 0, name; return
        if name=='create-failure':
            assert release.returncode != 0
            # Re-run the actual bump block as a workflow rerun, then publish again.
            cz_before=calls.read_text().count('cz ')
            again=execute(b['Bump version']); assert again.returncode==0 and calls.read_text().count('cz ')==cz_before
            release=execute(b['Publish GitHub Release'])
        assert release.returncode==0, f"{name}: {release.stderr}"
        state=__import__('json').loads(sf.read_text()); log=calls.read_text()
        if name=='new-bump': assert log.index('git push') < log.index('gh api')
        assert state['releases']==(['v2.0.0'] if name!='existing-release' else ['v2.0.0'])
        if name=='new-bump':
            assert 'gh release create v2.0.0 --verify-tag --title v2.0.0 --generate-notes' in log
            assert 'v1.0.0' not in log


def main():
    b=blocks()
    for case in ('new-bump','no-bump','existing-release','missing-remote','push-failure','api-error','auth-error','create-failure'):
        run_case(case,b)
        print(f"PASS {case}")

if __name__ == '__main__': main()
