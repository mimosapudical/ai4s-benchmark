# Round 1 — setup failure, not scientific failure

- Upstream/checkout SHA: `909274d50e91360991b5cc8c60edc3696de37f40`; task version 1.0.0, uncommitted prototype.
- Hypothesis: shared-mechanism Gaussian likelihood can recover the interventional equivalence class from finite moments.
- Command: `python research/intervention-orientation/calibrate.py --output research/intervention-orientation/audit_r1_20261017`.
- Result: exit 1 before any solver execution. `IndexError` in `embedded`: the Docker COPY heredoc has a destination after its delimiter; extraction expected a bare newline.
- Taxonomy: author calibration parser/setup failure. No score, oracle run, or model failure occurred. The scientific hypothesis is untested in this round.
- Smallest change: parse heredoc by line delimiter; do not modify data, oracle, verifier or thresholds. Use a new round directory.
- Methodology: Hauser & Bühlmann (JMLR 2012), Theorem 10 supplies the identifiability criterion, not evidence about this failed run; Yan et al. (ICML 2024), *Foundations of Testing for Finite-Sample Causal Discovery*, distinguishes finite evidence from ideal orientation queries. Neither theorem can interpret a parser exception as scientific failure.
- Sources: https://jmlr.org/papers/v13/hauser12a.html ; https://proceedings.mlr.press/v235/yan24g.html .
