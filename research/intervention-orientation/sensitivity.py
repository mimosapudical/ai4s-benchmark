"""Predeclared fresh-seed/sample-size sweep; never changes the frozen task."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

from calibrate import ROOT, TASK, module
from generate import generate


def main(output):
    output.mkdir(parents=True, exist_ok=False)
    oracle = module(TASK / 'solution/solve.sh', 'PY_ORACLE')
    verifier = module(TASK / 'tests/test.sh', 'PY_VERIFIER')
    records = []
    started = time.monotonic()
    # Both algorithms and thresholds frozen before observing these results.
    for n_int in [25, 75, 200, 500]:
        for seed in [1101, 1102, 1103, 1104, 1105]:
            data, truth, generation = generate(seed, n_int=n_int, matched_samples=True)
            verifier.TRUTH = truth
            answer = {s['id']: oracle.infer(s) for s in data['systems']}
            reward, metrics = verifier.grade(answer)
            record = dict(n_interventional=n_int, n_observational=1500, seed=seed,
                          reward=reward, **metrics,
                          max_covariance_error=max(r['covariance_reconstruction_max_error'] for r in generation),
                          evidence_sha256=hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest())
            records.append(record)
            print(n_int, seed, reward, metrics['edge_accuracy'], flush=True)
    result = dict(checkout_sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  task_version='1.0.0', seconds=time.monotonic()-started, records=records,
                  frozen_task_changed=False, generator='numpy.default_rng/PCG64, separate structure/sample streams',
                  paired_design='same graph/parameters/observations per seed across n; nested intervention samples',
                  execution='native Python, float64; one BLAS thread requested by command')
    (output / 'summary.json').write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True)
    main(p.parse_args().output)
