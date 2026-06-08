import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import MCM_Brain_Modell as brain


class RuntimeRegulationMappingTests(unittest.TestCase):
    def test_proposed_trade_does_not_act_when_meta_plan_is_not_allowed(self):
        original_entry_builder = brain._compute_runtime_entry_result

        def fake_entry_builder(**kwargs):
            return {
                "decision": "WAIT",
                "proposed_decision": "LONG",
                "meta_regulation_state": {
                    "allow_plan": False,
                    "allow_block": True,
                    "pre_action_phase": "hold",
                    "rejection_reason": "maturity_block",
                },
                "review_feedback_state": {
                    "act_push": 0.9,
                    "hold_pull": 0.0,
                    "observe_pull": 0.0,
                    "replan_pull": 0.0,
                    "tendency_hint": "act",
                },
            }

        try:
            brain._compute_runtime_entry_result = fake_entry_builder
            result, tendency, _ = brain._compute_runtime_result(
                window=[{"timestamp": 1, "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0}],
                candle_state={"timestamp": 1, "close": 1.0},
                bot=object(),
                tension_state={},
                visual_market_state={},
                structure_perception_state={},
                temporal_perception_state={},
            )
        finally:
            brain._compute_runtime_entry_result = original_entry_builder

        self.assertEqual(tendency, "hold")
        self.assertEqual(result.get("decision_tendency"), "hold")


if __name__ == "__main__":
    unittest.main()
