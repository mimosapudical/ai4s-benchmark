"""Native scientific calibration, explicitly not Harbor/container validation."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import types

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / 'tasks/applied-mathematics/causal-discovery/finite-sample-intervention-orientation'


def embedded(path, marker):
    lines = path.read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if "<<'" + marker + "'" in line)
    end = lines.index(marker, start + 1)
    return '\n'.join(lines[start + 1:end])


def module(path, marker):
    result = types.ModuleType('trusted_author_calibration')
    exec(compile(embedded(path, marker), str(path), 'exec'), result.__dict__)
    return result


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    evidence_text = embedded(TASK / 'environment/Dockerfile', 'EVIDENCE_JSON') + '\n'
    data = json.loads(evidence_text)
    oracle = module(TASK / 'solution/solve.sh', 'PY_ORACLE')
    verifier = module(TASK / 'tests/test.sh', 'PY_VERIFIER')
    records = []
    started = time.monotonic()
    with tempfile.TemporaryDirectory() as temporary:
        work = Path(temporary) / 'work'
        logs = Path(temporary) / 'logs'
        work.mkdir(); logs.mkdir()
        (work / 'evidence.json').write_text(evidence_text)
        env = {**os.environ, 'TASK_WORKSPACE': str(work), 'TASK_LOGS': str(logs),
               'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1'}

        def verify(name, answer=None, raw=None, expect=None, taxonomy='scientific'):
            path = work / 'answer.json'
            path.unlink(missing_ok=True)
            if raw is not None:
                path.write_text(raw)
            elif answer is not None:
                path.write_text(json.dumps(answer))
            # Deliberate agent-side reward planting must not change verifier outcome.
            (logs / 'reward.json').write_text('{"reward":1}')
            (logs / 'reward.txt').write_text('1')
            completed = subprocess.run(['sh', str(TASK / 'tests/test.sh')], env=env,
                                       capture_output=True, text=True, timeout=60)
            report = json.loads((logs / 'metrics.json').read_text())
            record = dict(name=name, exit_code=completed.returncode,
                          taxonomy=taxonomy, **report)
            records.append(record)
            (output / (name + '.log')).write_text(completed.stdout + completed.stderr)
            if expect is not None:
                assert report['reward'] == expect, record
            assert not (logs / 'reward.json').exists(), 'planted reward.json survived'
            assert completed.returncode == 0, record
            return record

        answers = []
        for repeat in range(5):
            completed = subprocess.run(['sh', str(TASK / 'solution/solve.sh')], env=env,
                                       capture_output=True, text=True, timeout=60)
            assert completed.returncode == 0, completed.stderr
            answer = json.loads((work / 'answer.json').read_text())
            answers.append(answer)
            verify(f'oracle_{repeat+1}', answer, expect=1)
        assert all(x == answers[0] for x in answers), 'oracle is not deterministic'
        verify('nop', expect=0, taxonomy='output_schema')
        verify('empty', raw='', expect=0, taxonomy='output_schema')
        verify('malformed', raw='{', expect=0, taxonomy='output_schema')
        verify('all_undirected', {s['id']: [0]*len(s['edges']) for s in data['systems']}, expect=0)
        verify('constant_forward', {s['id']: [1]*len(s['edges']) for s in data['systems']}, expect=0)
        corrupted = {c['id']: verifier.essential_states(c) for c in verifier.TRUTH}
        for values in corrupted.values():
            for j in range(4):
                values[j] = -values[j] if values[j] else 1
        verify('corrupted_truth', corrupted, expect=0)
        wrong_type = copy.deepcopy(answers[0]); wrong_type['system_00'][0] = True
        verify('boolean_state', wrong_type, expect=0, taxonomy='output_schema')
        verify('duplicate_key', raw='{"system_00":[],"system_00":[]}', expect=0, taxonomy='output_schema')
        verify('extra_key', {**answers[0], 'reward': 1}, expect=0, taxonomy='output_schema')
        # Legitimate ablations; not independent frontier-agent attempts.
        observation_only = copy.deepcopy(data)
        for s in observation_only['systems']:
            s['regimes'] = s['regimes'][:1]
        verify('observational_only', {s['id']: oracle.infer(s) for s in observation_only['systems']})
        # Scientific incomplete method: discard sharing of mechanisms between regimes.
        original_score = oracle.local_score

        def separate_score(v, parents, regimes):
            return sum(original_score(v, parents, [r]) for r in regimes if v not in r['targets'])

        oracle.local_score = separate_score
        verify('separate_regime_fit', {s['id']: oracle.infer(s) for s in data['systems']})
        oracle.local_score = original_score
        # Reject symlinks instead of loading arbitrary verifier or agent code.
        (work / 'answer.json').unlink()
        (work / 'answer.json').symlink_to(work / 'evidence.json')
        result = subprocess.run(['sh', str(TASK / 'tests/test.sh')], env=env,
                                capture_output=True, text=True, timeout=60)
        report = json.loads((logs / 'metrics.json').read_text())
        assert report['reward'] == 0 and result.returncode == 0
        records.append(dict(name='symlink', taxonomy='output_schema', **report))

    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(TASK.rglob('*')) if p.is_file()}
    summary = dict(upstream_sha='909274d50e91360991b5cc8c60edc3696de37f40',
                   checkout_sha=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                   task_version='1.0.0', task_files_sha256=manifest,
                   seconds=time.monotonic()-started, records=records,
                   execution='native shell; no Docker/Harbor isolation',
                   frontier_agent='not_available_environment_setup',
                   evidence_sha256=hashlib.sha256(evidence_text.encode()).hexdigest())
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    run(parser.parse_args().output)
