# Methodology and bounded literature check — checked 2026-10-17

Search scope: primary JMLR/PMLR proceedings, NeurIPS proceedings and official
arXiv pages; queries combined interventional Markov equivalence, Gaussian joint
likelihood, finite-sample causal testing, and synthetic benchmark artifacts.
Both web search engines were used; recent-work discovery included 2025/2026.
No external full-text cache existed in this repository; no licensed copies
are republished. This is an attribution/hypothesis check, not a global novelty
search. No new identifiability theorem or new discovery algorithm is claimed.

## Exact graph theorem used by the verifier

Hauser & Bühlmann, *Characterization and Greedy Learning of Interventional
Markov Equivalence Classes of Directed Acyclic Graphs*, JMLR 13:2409–2464
(2012), published PDF, **Theorem 10, p. 2414**, and Definition 11, p. 2416:
https://jmlr.org/papers/volume13/hauser12a/hauser12a.pdf .
Full theorem and surrounding positive-density assumptions were checked.
For a conservative intervention family, interventional equivalence is
equivalent to observational equivalence of each mutilated DAG: same skeleton
and v-structures. Here D is the trusted generating DAG; D⁽ᴵ⁾ deletes arrows
entering I; I includes the empty target set, hence is conservative. Positive
Gaussian noise gives strictly positive densities. The verifier implements this
criterion directly and takes the directions common to every survivor. For our
single-node interventions, Theorem 10(iv) also justifies the oracle's shorter
equivalence-class grouping by directions incident to intervention targets.
Application valid under the stated causal sufficiency/perfect-intervention
model; not a theorem for confounding, unknown targets or soft interventions.

## Joint likelihood, not a marginal-correlation shortcut

Hauser & Bühlmann, *Jointly interventional and observational data: estimation
of interventional Markov equivalence classes of directed acyclic graphs*,
arXiv:1303.3216v1 (2013): https://arxiv.org/abs/1303.3216v1 . The abstract's
Gaussian shared-parameter likelihood and BIC-consistency scope were checked;
its full proof was not independently audited. Our oracle's objective is
derived directly below; we do not invoke consistency as a finite-sample bound.

For node j, pool samples only from regimes not intervening on j. Let Nⱼ be
their total sample count and Gⱼ = Σᵣ nᵣ Sᵣ their Gram matrix. For parent set P,
RSSⱼ(P) = Gⱼ[j,j] − Gⱼ[j,P] Gⱼ[P,P]⁻¹ Gⱼ[P,j]. Profiling unknown Gaussian
variance gives −2 log L = Σⱼ Nⱼ log(RSSⱼ/Nⱼ) + constants. The target density
terms are constant across candidate graphs; omitting them cannot favor one.
All candidate DAGs have twelve edges, so parameter-count penalties are equal.
This is the objective in `local_score`; known-zero means justify uncentered
moments. Non-target coefficient/variance sharing must not be dropped.

## Finite evidence and what is not established

Yan, Xu & Lipton, *Foundations of Testing for Finite-Sample Causal Discovery*,
ICML 2024, PMLR 235:55859–55900:
https://proceedings.mlr.press/v235/yan24g.html . The primary abstract confirms
the known-skeleton, causally sufficient, finite-intervention testing setting.
It motivates treating orientation as a noisy statistical decision rather than
an ideal query. Its anytime-valid testing framework is NOT implemented here;
neither our reward tolerance nor oracle accuracy inherits its error control.

Under each zero-mean IID Gaussian regime, nS has a Wishart distribution.
Consequently the supplied (n,S) is sufficient for this likelihood, but noisy.
Gaussian quadratic-form concentration depends on n, covariance conditioning
and signal separation. The generator does not impose a uniform lower bound on
every intervention's discriminating signal; the observed fresh-seed failure is
consistent with that limitation. Five repeated runs on fixed S only test
determinism. Five fresh seeds are exploratory, not a precise reliability estimate.

Lungu et al., *The relative value of interventional and observational samples
in Bayesian Causal Linear Gaussian Models*, arXiv:2603.26460v1 (27 March
2026), **Theorem 4.1**:
https://arxiv.org/html/2603.26460v1 . This recent **preprint**, not verified as
a top-venue publication, proves posterior-concentration statements for a
bivariate Bayesian model with fixed intervention value and smooth priors.
We checked those hypotheses. Our nine-node randomized-target likelihood is
different: the result motivates the sample-budget question but supplies no
rate or finite-sample guarantee for this task.

## Synthetic-artifact control

Herman, Wahl, Ninad & Runge, *Unitless Unrestricted Markov-Consistent SCM
Generation: Better Benchmark Datasets for Causal Discovery*, CLeaR 2025,
PMLR 275:1506–1531: https://proceedings.mlr.press/v275/herman25a.html .
The primary abstract discusses variance and R² ordering artifacts; it motivates
testing whether truth is encoded by the generator rather than the experiment.
We do not implement UUMC or claim its guarantees. Our covariance-first,
uniform-MEC-direction construction preserves one observational law across
possible true DAGs; randomized units alone would not establish this property.

## Loss and an actual impossibility principle

The task scores Hamming loss on essential-graph edge states. It is not ordinary
DAG SHD or SID: two DAGs differing only on an unidentifiable direction should
not be ranked as scientifically distinct recoveries. Reporting every edge as
undirected and reporting a fully oriented completion fail complementary gates.
Thresholds are a published benchmark design choice, not a significance test.

A two-point (Le Cam) argument explains the choice of target: if two causal
parameterizations induce exactly the same distributions in every supplied
regime, their data laws have total variation 0 and KL divergence 0. Any test
choosing between them has average error at least 1/2 under equal priors.
Therefore a uniformly reliable full-DAG score cannot require separating such
models. The graph theorem identifies model-class ambiguity; it does not supply
a positive finite-sample separation between *different* classes. No Fano bound,
minimax optimality, or 95% confidence claim is asserted for the current bank.
