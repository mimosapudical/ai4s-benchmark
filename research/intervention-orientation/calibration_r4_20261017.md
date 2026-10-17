# Round 4 — controlled paired sample-budget check

- Upstream/checkout SHA: `909274d50e91360991b5cc8c60edc3696de37f40`; task 1.0.0 unchanged; author-side generation adds optional matched sampling. Raw records: `audit_r4_20261017/summary.json`.
- Hypothesis: with graphs, parameters and observations fixed, more nested interventional samples improve finite-sample recovery on these five seeded banks.
- Command: `env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/intervention-orientation/sensitivity.py --output research/intervention-orientation/audit_r4_20261017`.
- Design: seeds 1101–1105; each has eight systems; 1500 observational samples and 25/75/200/500 samples per intervention. Separate PCG64 streams preserve each graph, its parameters, observational samples and intervention-sample prefixes across n. No seed is selected by solver performance.

| intervention n | reward-1 banks / 5 | mean edge-state accuracy | worst system across banks |
|---|---|---|---|
| 25 | 2 | 0.9708333333 | 0.5833333333 |
| 75 | 4 | 0.99375 | 0.75 |
| 200 | 5 | 0.9958333333 | 0.8333333333 |
| 500 | 5 | 0.9958333333 | 0.8333333333 |

- Exit 0, 23.70 seconds. Non-passes are scientific threshold failures, not setup failures. At n=200 and 500 one bank still has two edge errors; the disclosed tolerance accepts it. We do NOT claim exact recovery on every fresh graph.
- Orthogonal checks: hand-computable two-node/collider cases, both oracle and verifier class constructions on three-node examples, unit rescaling, matched structure/observations, and positive-semidefinite extra-sample Gram matrices pass. The first default-generation comparison test compared Python edge tuples with serialized JSON lists; it failed on representation, then passed after applying JSON round-trip normalization. The generated evidence bytes did not change (SHA-256 `375b8f9cdb80e8942aef8aa97288cd06fb825b3c899b81cee55425f8b9d0d411`).
- Interpretation: supports sample-budget sensitivity on this bounded matched family. The unpaired round-3 failure remains valid and retained. Five banks are too few for a reliable population pass-rate estimate; increased n is not guaranteed to cure arbitrarily weak signal.
- Relevant methodology: Yan et al., ICML 2024 (finite noisy interventions); Hauser & Bühlmann, JMLR 2012 Theorem 10 (the correct structural target); Herman et al., CLeaR 2025 (generator artifacts). Sources and exact theorem scope are in `METHODOLOGY.md`.
- Principle: finite Gaussian second moments are Wishart statistics; paired sampling controls structural nuisance variation, but does not turn an empirical table into a uniform concentration guarantee.
- Smallest next action: no scientific change. Freeze the five task files, rerun native controls on the committed revision, then submit the proposal for human review. Docker isolation and frontier-agent hardness remain separate outstanding gates.
