# Which causal arrows do the experiments actually identify?

You are auditing controlled perturbation studies of small modular causal
systems. Observational evidence has established the graph skeleton and absence
of unshielded colliders, but not the arrow directions. Use the supplied finite
observational and randomized-intervention samples to recover the **interventional
essential graph**, including edges whose direction remains unidentifiable.
This is a synthetic statistical-methods study, not empirical biological data.

## Inputs and scientific assumptions

`/workspace/evidence.json` contains eight independent systems. Each has:

- `id`, `n_nodes` (nodes numbered 0 through 8), and `edges`: the known skeleton,
  each undirected edge listed once as `[a,b]` with a < b, in fixed output order.
- `regimes`: observational (`targets: []`) and two single-node, perfect
  randomized intervention regimes. `n` is the finite number of IID samples;
  `second_moment` is the uncentered sample matrix XᵀX/n in node order.

The observational CPDAG has precisely the listed undirected edges, no other
edges, and no unshielded colliders. Every true graph is acyclic. There are no
latent common causes, selection effects, measurement error or feedback.
For each non-target node j the structural equation is
Xⱼ = Σₖ∈pa(j) βⱼₖ Xₖ + εⱼ, with independent εⱼ ∼ N(0,σⱼ²).
Unknown positive noise variances may differ between nodes. Coefficients and
noise variances of **non-target mechanisms remain the same across regimes**.
At a target node the entire equation is replaced by an independent, zero-mean
Gaussian randomization of unknown positive variance; all incoming edges are
removed. All means are known to be zero. Thus `n` and XᵀX/n are sufficient
statistics for the Gaussian likelihood; individual rows contain no additional
information for this model. Do not treat these matrices as population moments.

Variable scales and node labels are arbitrary. Neither equal noise variances,
a variance-based causal ordering, nor fully identifiable DAGs may be assumed.
Use all available legitimate inputs; do not inspect solution or verifier files.

## Required scientific output

Write `/workspace/answer.json`: exactly one JSON object with the eight system
IDs as keys. Each value is a list, matching that system's `edges` order:

- `1`: a → b is compelled in the interventional equivalence class;
- `-1`: b → a is compelled;
- `0`: both directions occur in that class and the edge remains undirected.

For example, `{"system_00": [1,0,-1,...], ...}` illustrates the schema only;
the ellipses are not valid JSON. Values must be integers, not booleans or floats.
No extra keys, duplicate keys, missing systems, NaN or executable scoring code.

Two DAGs are interventionally equivalent if for every supplied intervention
target set (including observation), deleting incoming edges to the targets
leaves graphs with the same skeleton and unshielded colliders. The essential
graph keeps a direction only when **every** DAG in this equivalence class
agrees. Do not submit an arbitrarily completed DAG as the essential graph.
Finite-sample uncertainty about which class is true is distinct from this
population-level ambiguity. Infer the class using the available evidence;
`0` denotes structural non-identifiability, not a generic low-confidence flag.

## Public scoring rule

The verifier independently computes the interventional essential graph from
the generating DAG and intervention design. An edge-state error (including
wrong orientation, missed orientation or overorientation) costs one unit.
Reward is 1 only if **all** these criteria hold:

- overall edge-state accuracy ≥ 0.95 (at most 4 errors across 96 edges);
- minimum per-system accuracy ≥ 0.83 (at most 2 errors per 12-edge system);
- accuracy on truly compelled edges ≥ 0.90;
- accuracy on truly ambiguous edges ≥ 0.90.

Otherwise reward is 0. Malformed, missing and empty output earn 0. Structural
ground truth, all thresholds and all penalties are fixed before calibration;
no runtime, implementation technique or hidden confidence rubric is scored.
NumPy and Python are available. GPU and network access are unnecessary.
