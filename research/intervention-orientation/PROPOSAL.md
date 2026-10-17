# Finite-sample recovery of interventionally identifiable causal orientations

**Status: proposal-ready specification, NOT submitted or human-approved. No task PR is authorized yet.**

## Scientific domain and asset

Primary domain: Applied Mathematics (`applied-mathematics`). Field: Causal
Discovery (`causal-discovery`). Author: Jingzhi Chen, GitHub `mimosapudical`.
Do not infer additional affiliation, publication history or author-fit credentials.

Build a controlled causal-discovery benchmark that distinguishes recovering an
identifiable arrow from inventing one in a statistically indistinguishable
class. The asset consists of a reproducible generator, frozen finite-sample
evidence, a likelihood oracle, an independently implemented graph-theoretic
verifier, and ambiguity-aware negative controls. It is a statistical-methods
benchmark, not a claim about a measured biological network or a new algorithm.

## Formulation choice (one task only)

| Candidate | Scientific value | Independent verification | Leakage/ambiguity risk | CPU/difficulty assessment |
|---|---|---|---|---|
| A. Interventional DAG recovery | Broad end-to-end structure learning | Easy with synthetic DAGs | Full-DAG target may demand unidentifiable arrows; synthetic noise-order shortcuts | Affordable; overlaps standard canned discovery pipelines |
| B. Observational equivalence + intervention orientation | Separates finite evidence from structural non-identifiability | Exact finite graph equivalence criterion | Controlled by matching observational laws across possible truths | Selected; 4 CPUs, no GPU; frontier difficulty still unmeasured |
| C. Invariance across heterogeneous environments | Valuable with unknown perturbations | More model-dependent when targets/mechanisms are unknown | Environment assumptions can silently determine the answer | Affordable in small systems, but extra assumptions obscure the core test |

Select B only. Sharing non-target mechanisms is part of known-target perfect
intervention semantics; this does not add an unknown-environment invariance task.

## Scientific question and inputs

Eight synthetic systems, each nine nodes and twelve skeleton edges in four
overlapping triangular modules. The observational essential graph is supplied
and has no compelled arrows. Each class has 144 DAGs. Two single-node perfect
randomizations only partially resolve it. Agents receive 1,500 observational
samples and 500 samples per intervention in the lossless-for-this-likelihood
form `(n, XᵀX/n)`. Means are known zero. The supplied second moments are finite
sample statistics, NOT population covariance matrices. No GPU or external data
service is required. The Gaussian family and known CPDAG deliberately isolate
the intervention-orientation problem rather than skeleton discovery.

Noise is independent, Gaussian and heteroscedastic. Non-target coefficients
and variances are shared across regimes; target equations are replaced.
Labels and variable units are randomized. The generator constructs a positive
definite observational covariance first, then independently samples the true
DAG uniformly from its MEC and reparameterizes to preserve that covariance.
Thus within this controlled family, observational variance cannot identify
which DAG was sampled. This is stronger than merely rescaling a conventional
SEM, but does not establish artifact freedom for every graph family.

## Output, verifier and public success criterion

One edge-state vector per system: +1 or -1 for a compelled direction and 0 for
a structurally ambiguous edge. Ground truth is the interventional essential
graph, not one arbitrary DAG completion. The frozen bank has 52 compelled and
44 ambiguous edges. A structural state mismatch costs one error; overall
accuracy must be ≥0.95, worst-system accuracy ≥0.83, compelled-edge accuracy
≥0.90 and ambiguous-edge accuracy ≥0.90. These are explicit benchmark
tolerances, not claimed confidence levels or theorem-derived constants.

The verifier uses only trusted generating DAGs and intervention target sets.
It enumerates all 2¹² orientations, rejects cycles, and compares skeletons and
unshielded colliders after deleting incoming target edges. It does not import
the oracle, generator, submitted code or a submitted score. The oracle instead
enumerates perfect-elimination orders, fits shared Gaussian mechanisms from
legitimate sample statistics, chooses a likelihood class, and reports its
compelled arrows. The implementations share a mathematical contract, not code.
They were developed in the same authoring session; independent human review
has not occurred and should precede claims of independently audited validity.

## Provenance, leakage boundary and negative controls

Synthetic assets are generated author-side with NumPy PCG64, seed 20261017.
The image contains only the evidence JSON, Python and NumPy. Neither generator,
generation seed, DAG, oracle nor verifier is copied into the image. Exactly
five task files are proposed. Scripts use isolated Python (`-I`) to avoid
workspace import shadowing. Reward formats are cleared before fail-closed
grading. Empty/malformed/boolean/duplicate-key output and answer symlinks fail.
Runtime environment and verifier networking are disabled.

Public repository source necessarily contains the reference solution and
trusted test DAGs. The benchmark assumes Harbor keeps those files unavailable
during the agent phase. Whole-repository mounts, source-trained memorization,
compromised runtime, background-process tampering or altered trusted verifier
files are outside the JSON verifier's threat model. Native calibration checks
reward planting and parser boundaries; it does NOT certify container isolation.

## Calibration and feasibility

Frozen task: oracle 5/5, each 96/96 correct. No-op, empty, malformed, all-zero,
constant-forward and four-errors-per-system corrupted truth all fail.
Observational-only method reaches 45.83%; a plausible separate-regime fit,
which omits cross-regime mechanism sharing, reaches 57.29%; both fail.

Fresh-dataset sensitivity uses seeds 1101–1105 and intervention sizes
25/75/200/500, fixed 1,500 observational samples. It does not change the frozen
task or thresholds. At 500 the oracle passes 4/5 fresh datasets, so fixed-bank
reproducibility is NOT a universal finite-sample recovery guarantee. A future
randomized benchmark would need a separately specified signal-strength/coverage
condition or uncertainty-aware scoring; do not silently resample difficult
cases, add oracle-dependent acceptance filters, or weaken thresholds.

Native calibration takes seconds per bank on CPU. The proposed container limit
is 4 CPUs, 4 GiB RAM, 2 GiB storage, 1,800 seconds for agents and 120 seconds for
the verifier. These configured limits have not been measured in Docker here.
Harbor 0.20.0 loads the task configuration; Docker is absent. Frontier agents
have not been run. The small 144-candidate search space may be easy for strong
agents: measured frontier difficulty and reviewer assessment remain mandatory.

## Relation to authorship

This is ownership of a scientific evaluation asset rather than a maintenance
patch. It is a credible proposal for an authorship conversation, **not evidence
of entitlement or currently confirmed authorship-grade difficulty**. Its value
depends on independent review, frontier-agent results, scientific scope approval
and the project's actual credit policy. Do not substitute PR merge count for
those decisions. Submit through https://ai4sbench.org/submit/ after reviewing
this specification. No approval or proposal reference has been fabricated.

## Literature and mathematical contract

See `METHODOLOGY.md` for theorem hypotheses, finite-sample limits, loss choices
and precise distinctions between proved statements and empirical evidence.
