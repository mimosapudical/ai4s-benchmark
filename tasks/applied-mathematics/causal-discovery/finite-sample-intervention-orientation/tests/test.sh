#!/bin/sh
set -eu
logs="${TASK_LOGS:-/logs/verifier}"
mkdir -p "$logs"
rm -f "$logs/reward.txt" "$logs/reward.json" "$logs/metrics.json"
printf '0\n' > "$logs/reward.txt"
python -I - <<'PY_VERIFIER'
import itertools
import json
import os
import stat
from pathlib import Path

# Ground truth is inserted by the author-side generator, never the solver.
TRUTH = [{'dag': [[2, 0], [0, 4], [0, 5], [0, 7], [1, 3], [4, 1], [2, 4], [4, 3], [7, 5], [7, 6], [8, 6], [7, 8]], 'edges': [[0, 2], [0, 4], [0, 5], [0, 7], [1, 3], [1, 4], [2, 4], [3, 4], [5, 7], [6, 7], [6, 8], [7, 8]], 'id': 'system_00', 'n_nodes': 9, 'targets': [[], [3], [5]]}, {'dag': [[0, 3], [8, 0], [3, 1], [1, 5], [2, 6], [2, 8], [3, 5], [8, 3], [6, 4], [4, 7], [6, 7], [6, 8]], 'edges': [[0, 3], [0, 8], [1, 3], [1, 5], [2, 6], [2, 8], [3, 5], [3, 8], [4, 6], [4, 7], [6, 7], [6, 8]], 'id': 'system_01', 'n_nodes': 9, 'targets': [[], [5], [2]]}, {'dag': [[0, 3], [8, 0], [5, 1], [1, 7], [4, 2], [2, 5], [8, 3], [4, 5], [4, 6], [4, 8], [5, 7], [8, 6]], 'edges': [[0, 3], [0, 8], [1, 5], [1, 7], [2, 4], [2, 5], [3, 8], [4, 5], [4, 6], [4, 8], [5, 7], [6, 8]], 'id': 'system_02', 'n_nodes': 9, 'targets': [[], [0], [2]]}, {'dag': [[2, 0], [0, 8], [1, 6], [1, 7], [4, 2], [5, 2], [2, 8], [4, 3], [7, 3], [4, 5], [7, 4], [6, 7]], 'edges': [[0, 2], [0, 8], [1, 6], [1, 7], [2, 4], [2, 5], [2, 8], [3, 4], [3, 7], [4, 5], [4, 7], [6, 7]], 'id': 'system_03', 'n_nodes': 9, 'targets': [[], [6], [5]]}, {'dag': [[3, 0], [0, 6], [2, 1], [1, 3], [1, 7], [1, 8], [2, 7], [3, 6], [3, 8], [5, 4], [7, 4], [7, 5]], 'edges': [[0, 3], [0, 6], [1, 2], [1, 3], [1, 7], [1, 8], [2, 7], [3, 6], [3, 8], [4, 5], [4, 7], [5, 7]], 'id': 'system_04', 'n_nodes': 9, 'targets': [[], [5], [8]]}, {'dag': [[4, 0], [0, 6], [2, 1], [1, 7], [3, 2], [2, 7], [8, 2], [8, 3], [4, 6], [6, 5], [8, 5], [6, 8]], 'edges': [[0, 4], [0, 6], [1, 2], [1, 7], [2, 3], [2, 7], [2, 8], [3, 8], [4, 6], [5, 6], [5, 8], [6, 8]], 'id': 'system_05', 'n_nodes': 9, 'targets': [[], [7], [5]]}, {'dag': [[0, 7], [8, 0], [3, 1], [8, 1], [2, 5], [6, 2], [3, 4], [3, 6], [8, 3], [6, 4], [6, 5], [8, 7]], 'edges': [[0, 7], [0, 8], [1, 3], [1, 8], [2, 5], [2, 6], [3, 4], [3, 6], [3, 8], [4, 6], [5, 6], [7, 8]], 'id': 'system_06', 'n_nodes': 9, 'targets': [[], [2], [1]]}, {'dag': [[0, 1], [0, 3], [5, 0], [8, 0], [1, 3], [2, 4], [2, 5], [2, 6], [2, 7], [7, 4], [5, 6], [5, 8]], 'edges': [[0, 1], [0, 3], [0, 5], [0, 8], [1, 3], [2, 4], [2, 5], [2, 6], [2, 7], [4, 7], [5, 6], [5, 8]], 'id': 'system_07', 'n_nodes': 9, 'targets': [[], [4], [8]]}]


def equivalence_signature(arrows, targets):
    cut = {(a, b) for a, b in arrows if b not in targets}
    skeleton = frozenset(frozenset(e) for e in cut)
    colliders = set()
    for v in {x for e in arrows for x in e}:
        parents = sorted(a for a, b in cut if b == v)
        for a, b in itertools.combinations(parents, 2):
            if frozenset((a, b)) not in skeleton:
                colliders.add((a, v, b))
    return skeleton, frozenset(colliders)


def acyclic(arrows, n):
    remaining = set(range(n))
    while remaining:
        roots = {v for v in remaining if not any(b == v and a in remaining for a, b in arrows)}
        if not roots:
            return False
        remaining -= roots
    return True


def essential_states(case):
    # Independent brute-force orientation plus mutilated-graph criterion.
    edges, truth = case['edges'], {tuple(e) for e in case['dag']}
    targets = [set(t) for t in case['targets']]
    expected = [equivalence_signature(truth, t) for t in targets]
    survivors = []
    for bits in itertools.product((False, True), repeat=len(edges)):
        candidate = {tuple(e) if bit else tuple(reversed(e)) for e, bit in zip(edges, bits)}
        if not acyclic(candidate, case['n_nodes']):
            continue
        if all(equivalence_signature(candidate, t) == sig for t, sig in zip(targets, expected)):
            survivors.append(candidate)
    if not survivors:
        raise RuntimeError('invalid verifier truth')
    result = []
    for a, b in edges:
        directions = {(a, b) in d for d in survivors}
        result.append(0 if len(directions) == 2 else (1 if True in directions else -1))
    return result


def grade(answer):
    if type(answer) is not dict or set(answer) != {c['id'] for c in TRUTH}:
        raise ValueError('exact system keys required')
    correct = total = directed_ok = directed_n = ambiguous_ok = ambiguous_n = 0
    per_system = {}
    for case in TRUTH:
        predicted = answer[case['id']]
        if type(predicted) is not list or len(predicted) != len(case['edges']):
            raise ValueError('wrong state vector length')
        if any(type(x) is not int or x not in (-1, 0, 1) for x in predicted):
            raise ValueError('states must be integers -1, 0, 1')
        actual = essential_states(case)
        hits = sum(a == b for a, b in zip(predicted, actual))
        per_system[case['id']] = hits / len(actual)
        correct += hits
        total += len(actual)
        for a, b in zip(predicted, actual):
            if b:
                directed_n += 1
                directed_ok += a == b
            else:
                ambiguous_n += 1
                ambiguous_ok += a == 0
    metrics = dict(edge_accuracy=correct / total, worst_accuracy=min(per_system.values()),
                   directed_accuracy=directed_ok / directed_n,
                   ambiguous_accuracy=ambiguous_ok / ambiguous_n, per_system=per_system)
    passed = (metrics['edge_accuracy'] >= 0.95 and metrics['worst_accuracy'] >= 0.83
              and metrics['directed_accuracy'] >= 0.90 and metrics['ambiguous_accuracy'] >= 0.90)
    return int(passed), metrics


def read_answer(path):
    # Never follow an agent-controlled answer symlink or import its Python code.
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > 65536:
        raise ValueError('answer must be a small regular JSON file')

    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise ValueError('duplicate JSON key')
            result[k] = v
        return result

    return json.loads(path.read_text(), object_pairs_hook=unique)


if __name__ == '__main__':
    workspace = Path(os.environ.get('TASK_WORKSPACE', '/workspace'))
    logs = Path(os.environ.get('TASK_LOGS', '/logs/verifier'))
    logs.mkdir(parents=True, exist_ok=True)
    # Shell wrapper already clears both reward formats and writes fail-closed 0.
    try:
        reward, metrics = grade(read_answer(workspace / 'answer.json'))
        report = dict(reward=reward, failure_type=None if reward else 'scientific_threshold', **metrics)
    except (ValueError, OSError, TypeError, json.JSONDecodeError) as exc:
        reward, report = 0, dict(reward=0, failure_type='output_schema', detail=str(exc))
    print(json.dumps(report, sort_keys=True))
    (logs / 'metrics.json').write_text(json.dumps(report, sort_keys=True) + '\n')
    (logs / 'reward.txt').write_text(str(reward) + '\n')

PY_VERIFIER
