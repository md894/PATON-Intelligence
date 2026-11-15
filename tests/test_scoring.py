import unittest

import pandas as pd

from src.scoring import DEFAULT_WEIGHTS, score_markets


class ScoreMarketsTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame(
            {
                "name": ["strong", "weak"],
                "market_attractiveness": [10, 1],
                "problem_urgency": [10, 1],
                "willingness_to_pay": [10, 1],
                "accessibility": [10, 1],
                "product_fit": [10, 1],
                "sales_cycle_months": [3, 24],
                "regulatory_complexity": [1, 10],
            }
        )

    def test_stronger_row_ranks_first(self):
        scored = score_markets(self.frame, DEFAULT_WEIGHTS)
        self.assertEqual(scored.iloc[0]["name"], "strong")
        self.assertEqual(scored.iloc[0]["opportunity_score"], 100.0)
        self.assertEqual(scored.iloc[1]["opportunity_score"], 0.0)

    def test_input_is_not_mutated(self):
        score_markets(self.frame, DEFAULT_WEIGHTS)
        self.assertNotIn("opportunity_score", self.frame.columns)

    def test_zero_weights_are_rejected(self):
        with self.assertRaises(ValueError):
            score_markets(self.frame, {key: 0 for key in DEFAULT_WEIGHTS})


if __name__ == "__main__":
    unittest.main()
