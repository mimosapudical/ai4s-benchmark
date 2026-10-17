# Round 3 — unpaired sample-budget exploration; limited interpretation

- Upstream/checkout SHA: `909274d50e91360991b5cc8c60edc3696de37f40`; frozen task 1.0.0 unchanged; uncommitted author-side sweep. Raw records: `audit_r3_20261017/summary.json`.
- Hypothesis: more intervention samples should improve class recovery, but no uniform beta-min/distribution separation is assumed.
- Command at this revision: `env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/intervention-orientation/sensitivity.py --output research/intervention-orientation/audit_r3_20261017`.
- Exact results across seeds 1101–1105, eight systems per bank, fixed 1500 observation samples:

| intervention n | reward-1 banks / 5 | mean edge-state accuracy | worst system across banks |
|---|---|---|---|
| 25 | 3 | 0.9479166667 | 0.3333333333 |
| 75 | 3 | 0.9645833333 | 0.4166666667 |
| 200 | 4 | 0.9875 | 0.6666666667 |
| 500 | 4 | 0.9875 | 0.6666666667 |

- Exit 0, 24.60 seconds. Failures are actual likelihood/class-recovery failures, not environment/parser failures. At n=500, seed 1104 has 92/96 correct but worst-system accuracy 8/12; the worst-system gate rejects it.
- Audit correction: the first generator used one RNG for graph construction and data draws. Changing n consumes a different amount of randomness and changes later systems. This table is **not a controlled causal comparison of sample size**. It is still a valid record of those distinct sampled banks. Do not silently relabel it as paired data.
- Relevant methodology: Yan et al., ICML 2024 (finite-sample versus ideal orientation); Herman et al., CLeaR 2025 (generator artifacts); Lungu et al., arXiv:2603.26460v1 (bivariate sample allocation, only motivational here). None proves a rate for these graphs.
- Principle: a sample-budget contrast must hold graph/parameter distribution fixed; finite sampled results are not a concentration theorem.
- Smallest next change: add an optional separate sample RNG stream for the author-side paired sweep; leave default generation, frozen evidence, oracle, verifier and thresholds intact. Use `audit_r4_20261017`, with matched graph/parameters and nested samples.
