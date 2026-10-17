#!/bin/sh
set -eu
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python -I - <<'PY_ORACLE'
import itertools
import json
import os
from pathlib import Path

import numpy as np


def enumerate_dags(n, edges):
    # Enumerate perfect elimination orders by removing simplicial sinks.
    # Deduplicate orientations: different elimination orders can yield one DAG.
    adjacency = {i: set() for i in range(n)}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    answers = set()

    def visit(remaining, arrows):
        if not remaining:
            answers.add(tuple(sorted(arrows)))
            return
        for v in sorted(remaining):
            neighbors = adjacency[v] & remaining
            if all(b in adjacency[a] for a, b in itertools.combinations(neighbors, 2)):
                visit(remaining - {v}, arrows + [(u, v) for u in neighbors])

    visit(set(range(n)), [])
    return sorted(answers)


def local_score(node, parents, regimes):
    # Non-target mechanisms share coefficients AND residual variance.
    usable = [r for r in regimes if node not in r['targets']]
    count = sum(r['n'] for r in usable)
    gram = sum(r['n'] * np.asarray(r['second_moment']) for r in usable)
    rss = gram[node, node]
    if parents:
        cross = gram[parents, node]
        rss -= cross @ np.linalg.solve(gram[np.ix_(parents, parents)], cross)
    if rss <= 0:
        raise ValueError('nonpositive residual variance')
    return count * np.log(rss / count)


def infer(system):
    edges = system['edges']
    dags = enumerate_dags(system['n_nodes'], edges)
    local = {}
    scores = []
    for dag in dags:
        score = 0.0
        for v in range(system['n_nodes']):
            pa = tuple(sorted(a for a, b in dag if b == v))
            if (v, pa) not in local:
                local[v, pa] = local_score(v, list(pa), system['regimes'])
            score += local[v, pa]
        scores.append(score)
    best = dags[int(np.argmin(scores))]
    targets = {t for r in system['regimes'] for t in r['targets']}
    incident = {e for e in best if e[0] in targets or e[1] in targets}
    equivalent = [set(d) for d in dags if incident <= set(d)]
    states = []
    for a, b in edges:
        values = {1 if (a, b) in d else -1 for d in equivalent}
        states.append(next(iter(values)) if len(values) == 1 else 0)
    return states


if __name__ == '__main__':
    workspace = Path(os.environ.get('TASK_WORKSPACE', '/workspace'))
    data = json.loads((workspace / 'evidence.json').read_text())
    result = {s['id']: infer(s) for s in data['systems']}
    (workspace / 'answer.json').write_text(json.dumps(result, sort_keys=True) + '\n')

PY_ORACLE
