"""Independent known-case checks; run outside the task's agent container."""
import itertools
import unittest

from calibrate import TASK, module


class ScientificTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.oracle = module(TASK / 'solution/solve.sh', 'PY_ORACLE')
        cls.verifier = module(TASK / 'tests/test.sh', 'PY_VERIFIER')

    def test_two_node_nonidentifiability_and_intervention(self):
        case = dict(n_nodes=2, edges=[[0, 1]], dag=[[0, 1]], targets=[[]])
        self.assertEqual(self.verifier.essential_states(case), [0])
        case['targets'].append([0])
        self.assertEqual(self.verifier.essential_states(case), [1])
        case['dag'] = [[1, 0]]
        self.assertEqual(self.verifier.essential_states(case), [-1])

    def test_unshielded_collider_is_observationally_compelled(self):
        case = dict(n_nodes=3, edges=[[0, 1], [1, 2]], dag=[[0, 1], [2, 1]], targets=[[]])
        self.assertEqual(self.verifier.essential_states(case), [1, -1])

    def test_oracle_class_conversion_against_mutilated_graphs(self):
        for edges in [[[0, 1], [1, 2]], [[0, 1], [0, 2], [1, 2]]]:
            dags = self.oracle.enumerate_dags(3, edges)
            self.assertEqual(len(dags), 3 if len(edges) == 2 else 6)
            for dag, target in itertools.product(dags, [[], [0], [1], [2]]):
                targets = set(target)
                incident = {e for e in dag if targets & set(e)}
                same = [set(d) for d in dags if incident <= set(d)]
                expected = []
                for a, b in edges:
                    values = {(a, b) in d for d in same}
                    expected.append(0 if len(values) == 2 else (1 if True in values else -1))
                case = dict(n_nodes=3, edges=edges, dag=dag, targets=[[], target])
                self.assertEqual(self.verifier.essential_states(case), expected)

    def test_cycle_rejected(self):
        self.assertFalse(self.verifier.acyclic({(0, 1), (1, 2), (2, 0)}, 3))

    def test_population_likelihood_is_unit_invariant(self):
        import numpy as np
        # X0 -> X1; randomized X0 changes variance while the X1 mechanism stays fixed.
        system = dict(n_nodes=2, edges=[[0, 1]], regimes=[
            dict(n=1000, targets=[], second_moment=[[1, 0.7], [0.7, 1.49]]),
            dict(n=500, targets=[0], second_moment=[[2, 1.4], [1.4, 1.98]])])
        self.assertEqual(self.oracle.infer(system), [1])

        for r in system['regimes']:
            scale = np.array([0.01, 100])
            r['second_moment'] = (np.asarray(r['second_moment']) * scale[:, None] * scale).tolist()
        self.assertEqual(self.oracle.infer(system), [1])

    def test_paired_sampling_holds_structure_fixed_and_nests_samples(self):
        import numpy as np
        from generate import generate
        small, t_small, _ = generate(1101, count=2, n_int=25, matched_samples=True)
        large, t_large, _ = generate(1101, count=2, n_int=75, matched_samples=True)
        self.assertEqual(t_small, t_large)
        for a, b in zip(small['systems'], large['systems']):
            self.assertEqual(a['regimes'][0], b['regimes'][0])
            for x, y in zip(a['regimes'][1:], b['regimes'][1:]):
                extra_gram = y['n'] * np.asarray(y['second_moment']) - x['n'] * np.asarray(x['second_moment'])
                self.assertGreater(np.linalg.eigvalsh(extra_gram).min(), -1e-8)

    def test_default_generator_exactly_reproduces_frozen_bank(self):
        import json
        from calibrate import embedded
        from generate import generate
        evidence, truth, _ = generate()
        self.assertEqual(json.loads(json.dumps(evidence)),
                         json.loads(embedded(TASK / 'environment/Dockerfile', 'EVIDENCE_JSON')))
        # JSON round trip normalizes generator tuples to the committed representation.
        self.assertEqual(json.loads(json.dumps(truth)), self.verifier.TRUTH)


if __name__ == '__main__':
    unittest.main()
