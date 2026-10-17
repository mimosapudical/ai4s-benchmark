# Round 2 — frozen-bank native calibration

- Upstream/checkout SHA: `909274d50e91360991b5cc8c60edc3696de37f40`; task version 1.0.0, uncommitted prototype. Exact task-file hashes are in `audit_r2_20261017/summary.json`.
- Hypothesis: the joint shared-mechanism likelihood identifies the supplied bank's interventional classes; trivial/invalid answers do not satisfy the same public criterion.
- Command: `python research/intervention-orientation/calibrate.py --output research/intervention-orientation/audit_r2_20261017`.
- Result: exit 0, 10.69 seconds, oracle 5/5 with overall/worst/directed/ambiguous accuracy all 1.0. Every repeated oracle answer was identical. Five reruns test execution determinism, not five independent datasets.
- Negatives: no-op/empty/malformed/boolean/duplicate/extra-key/symlink outputs fail as output-schema errors. All-undirected accuracy 44/96=45.83%, constant-forward 25/96=26.04%, corrupted truth 64/96=66.67%; all reward 0. Reward planting is erased on each verifier run.
- Scientific ablations: observational-only 44/96=45.83%; separate-regime regression 55/96=57.29%; both reward 0. These are author-written methods, NOT independent frontier-agent runs.
- Interpretation: supports correct fixed-bank computation and the importance of interventional information/shared mechanisms. It does not prove hardness for current frontier agents or uniformly reliable finite-sample recovery.
- Relevant sources: Hauser & Bühlmann JMLR 2012, Theorem 10 and Definition 11 (graph identifiability); Hauser & Bühlmann arXiv:1303.3216v1 (shared Gaussian likelihood); Yan et al., ICML 2024 (finite-sample causal testing). Exact scope is in `METHODOLOGY.md`.
- Principle: sufficient Gaussian statistics and the profiled sum of non-target mechanism log likelihoods; Hamming loss on the essential graph rather than an arbitrary DAG completion.
- Next smallest action: frozen-parameter/sample-budget audit on fresh data, not changing verifier thresholds. A later network-policy-only TOML change disables egress; rerun native calibration after final task configuration is fixed. Container isolation remains untested.
- Environment limitation: Docker absent; Harbor subsequently installed at 0.20.0 for schema loading only; no frontier attempt was launched.
