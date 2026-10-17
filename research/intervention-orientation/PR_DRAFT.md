# Proposed title

Add finite-sample interventional essential-graph recovery task

# PR body — preparation only; DO NOT OPEN YET

## Task proposal (new tasks only)

Pending human-approved proposal. Add the actual approved Discussion reference
only after proposal approval and all implementation/runtime validation gates
are complete. No approval has been asserted or fabricated.

## Task summary

Add one causal-discovery task in Applied Mathematics. Agents infer the
interventional essential graph of eight nine-variable Gaussian causal systems
from finite observational and known-target intervention statistics. Scoring
distinguishes warranted orientations from irreducible ambiguity.

The scientific asset includes covariance-matched observational equivalence,
randomized units/labels, deterministic legitimate-information likelihood
reference, and a separate mutilated-graph verifier. Public scoring requires
overall/worst-system/compelled/ambiguous accuracies of 0.95/0.83/0.90/0.90.

Native oracle runs pass 5/5 at 96/96 states. No-op, constant, corrupted,
malformed and reward-planting controls fail. Observational-only and
separate-regime-fit ablations earn 0. Paired sample-budget calibration is
reported without a uniform recovery guarantee.

## Validation and outstanding gates

Repository tests and native controls are described in `REPORT.md`. These are
not substitutes for real Harbor Docker trials. Docker/image execution,
container leakage isolation, frontier-agent difficulty and human proposal
approval are pending; this body must be updated with actual results before
submission. Strong agents may solve the small candidate space readily.

## Contributor checklist

- [x] Exactly one task directory with the five required files.
- [x] Deterministic native oracle and independent-code verifier checks.
- [x] Public scientific rubric and negative controls.
- [ ] Human-approved proposal Discussion.
- [ ] Docker image build and Harbor oracle/no-op trials on a supported host.
- [ ] Frontier-agent calibration and failure-taxonomy review.
- [ ] Independent scientific review, all relevant checks green, references updated.

This draft makes no claim that task inclusion guarantees paper authorship.
