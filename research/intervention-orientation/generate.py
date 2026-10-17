"""Author-side assets; never copied into the agent environment.

Finite Gaussian samples are compressed to sufficient statistics, not population
covariances. Direction is sampled AFTER covariance, uniformly within its MEC.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np


def generate(seed=20261017, count=8, n_obs=1500, n_int=500, matched_samples=False):
    rng = np.random.default_rng(seed)
    systems, truth, receipts = [], [], []
    # Four overlapping three-variable modules; articulation path 0-2-4-6-8.
    base = sorted({tuple(sorted(e)) for k in range(4)
                   for e in itertools.combinations((2*k, 2*k+1, 2*k+2), 2)})
    for case_id in range(count):
        n = 9
        perm = rng.permutation(n)
        edges = sorted(tuple(sorted((int(perm[a]), int(perm[b])))) for a, b in base)
        adjacent = {frozenset(e) for e in edges}
        dags = []
        # Independent data-generator enumeration, using a matrix transitive closure.
        for bits in itertools.product((0, 1), repeat=len(edges)):
            dag = [(a, b) if bit else (b, a) for (a, b), bit in zip(edges, bits)]
            parents = [[a for a, b in dag if b == v] for v in range(n)]
            if any(frozenset((a, b)) not in adjacent for p in parents
                   for a, b in itertools.combinations(p, 2)):
                continue
            reach = np.zeros((n, n), bool)
            for a, b in dag:
                reach[a, b] = True
            for k in range(n):
                reach |= reach[:, k, None] & reach[None, k, :]
            if not np.trace(reach):
                dags.append(dag)
        reference = dags[0]
        b_ref = np.zeros((n, n))
        for a, b in reference:
            b_ref[b, a] = rng.choice([-1, 1]) * rng.uniform(0.45, 0.95)
        noise = rng.uniform(0.6, 1.5, n)
        inv = np.linalg.inv(np.eye(n) - b_ref)
        covariance = inv @ np.diag(noise) @ inv.T
        scales = np.exp(rng.uniform(-1.2, 1.2, n)) / np.sqrt(np.diag(covariance))
        covariance *= scales[:, None] * scales[None, :]
        dag = dags[int(rng.integers(len(dags)))]
        b = np.zeros((n, n))
        variance = np.diag(covariance).copy()
        for v in range(n):
            p = [a for a, child in dag if child == v]
            if p:
                b[v, p] = np.linalg.solve(covariance[np.ix_(p, p)], covariance[p, v])
                variance[v] -= covariance[v, p] @ b[v, p]
        check = np.linalg.inv(np.eye(n) - b)
        reconstruction_error = float(np.max(np.abs(check @ np.diag(variance) @ check.T - covariance)))
        assert reconstruction_error < 1e-10
        # Pick module interior nodes: intervention coverage remains deliberately partial.
        targets = [int(perm[1]), int(perm[5])]
        regimes = []
        for regime_index, t in enumerate([None, *targets]):
            bi, vi = b.copy(), variance.copy()
            if t is not None:
                bi[t, :] = 0
                vi[t] = covariance[t, t] * 1.7
            n_samples = n_obs if t is None else n_int
            transform = np.linalg.inv(np.eye(n) - bi)
            sample_rng = (np.random.default_rng(np.random.SeedSequence([seed, case_id, regime_index, 95000]))
                          if matched_samples else rng)
            samples = sample_rng.normal(size=(n_samples, n)) * np.sqrt(vi)
            samples = samples @ transform.T
            regimes.append(dict(targets=[] if t is None else [t], n=n_samples,
                                second_moment=(samples.T @ samples / n_samples).tolist()))
        identifier = f'system_{case_id:02d}'
        systems.append(dict(id=identifier, n_nodes=n, edges=edges, regimes=regimes))
        truth.append(dict(id=identifier, n_nodes=n, edges=edges, dag=dag,
                          targets=[[], *[[t] for t in targets]]))
        receipts.append(dict(id=identifier, observational_mec_size=len(dags),
                             covariance_reconstruction_max_error=reconstruction_error,
                             minimum_noise_variance=float(min(variance))))
    return dict(version='1.0.0', systems=systems), truth, receipts


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--seed', type=int, default=20261017)
    p.add_argument('--n-obs', type=int, default=1500)
    p.add_argument('--n-int', type=int, default=500)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    evidence, truth, receipts = generate(args.seed, n_obs=args.n_obs, n_int=args.n_int)
    for name, value in [('evidence', evidence), ('truth', truth), ('generation', receipts)]:
        raw = (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()
        (args.output / (name + '.json')).write_bytes(raw)
        print(name, hashlib.sha256(raw).hexdigest())
