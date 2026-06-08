import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.decision_regulation import build_meta_regulation_state


def stable_action_inputs():
    return (
        {
            "structure_quality": 0.8,
            "context_confidence": 0.8,
            "visual_clarity": 0.8,
            "visual_object_stability": 0.8,
            "market_balance": 0.5,
            "breakout_tension": 0.2,
        },
        {
            "processing_load": 0.2,
            "processing_alignment": 0.8,
            "processing_tension": 0.2,
            "field_perception_pressure": 0.2,
            "field_perception_support": 0.7,
            "field_perception_clarity": 0.7,
            "field_perception_focus": 0.7,
            "field_perception_stability": 0.7,
            "field_perception_fragmentation": 0.1,
            "field_perception_strain": 0.1,
            "visual_clarity": 0.8,
            "visual_object_stability": 0.8,
        },
        {
            "felt_pressure": 0.2,
            "felt_conflict": 0.1,
            "market_balance": 0.5,
            "breakout_tension": 0.2,
            "dominant_tension_cause": "-",
            "dominant_tension_value": 0.0,
            "pre_action_observation_need": 0.1,
            "experience_regulation": 0.6,
            "load_bearing_capacity": 0.7,
            "protective_courage": 0.7,
            "pressure_release": 0.2,
            "areal_support": 0.7,
        },
        {
            "decision": "LONG",
            "long_hypothesis": 1.25,
            "short_hypothesis": 0.1,
            "state_maturity": 0.7,
            "decision_conflict": 0.1,
            "rumination_depth": 0.1,
            "decision_readiness": 0.7,
            "memory_support": 0.2,
            "memory_inhibition": 0.0,
            "memory_conflict": 0.0,
            "cognitive_load": 0.2,
            "memory_compare_load": 0.1,
        },
        {
            "decision": "LONG",
            "proposed_decision": "LONG",
            "long_score": 1.25,
            "short_score": 0.1,
            "signal_quality": 0.7,
            "observation_mode": False,
        },
    )


class DecisionRegulationTests(unittest.TestCase):
    def test_stable_context_keeps_action_permission_after_refactor(self):
        meta = build_meta_regulation_state(*stable_action_inputs())

        self.assertEqual(meta.get("pre_action_phase"), "act")
        self.assertTrue(meta.get("allow_plan"))

    def test_uncertain_context_does_not_auto_promote_long_short_to_action(self):
        perception, processing, felt, thought, fused = stable_action_inputs()
        perception.update({"structure_quality": 0.3, "context_confidence": 0.2, "market_balance": 0.1, "breakout_tension": 0.7})
        processing.update(
            {
                "processing_load": 0.8,
                "processing_alignment": 0.2,
                "processing_tension": 0.8,
                "field_perception_pressure": 0.8,
                "field_perception_support": 0.1,
                "field_perception_clarity": 0.1,
                "field_perception_focus": 0.1,
                "field_perception_stability": 0.1,
                "field_perception_fragmentation": 0.8,
                "field_perception_strain": 0.8,
            }
        )
        felt.update(
            {
                "felt_pressure": 0.9,
                "felt_conflict": 0.6,
                "dominant_tension_cause": "uncertainty_pressure",
                "dominant_tension_value": 0.8,
                "pre_action_observation_need": 0.8,
                "experience_regulation": 0.1,
                "load_bearing_capacity": 0.1,
                "protective_courage": 0.1,
            }
        )
        thought.update({"state_maturity": 0.1, "decision_conflict": 0.8, "rumination_depth": 0.8, "decision_readiness": 0.1})
        fused.update({"long_score": 0.8, "signal_quality": 0.1})

        meta = build_meta_regulation_state(perception, processing, felt, thought, fused)

        self.assertFalse(meta.get("allow_plan"))
        self.assertIn(meta.get("pre_action_phase"), {"observe", "replan", "hold"})

    def test_opposing_raw_score_does_not_become_action_strength(self):
        perception, processing, felt, thought, fused = stable_action_inputs()
        perception.update({"structure_quality": 0.36, "context_confidence": 0.28})
        processing.update({"processing_alignment": 0.25, "field_perception_support": 0.18})
        felt.update({"felt_pressure": 0.68, "felt_conflict": 0.54, "pre_action_observation_need": 0.72})
        thought.update(
            {
                "long_hypothesis": 0.22,
                "short_hypothesis": -2.0,
                "state_maturity": 0.24,
                "decision_readiness": 0.22,
                "decision_conflict": 0.66,
            }
        )
        fused.update({"long_score": 0.22, "short_score": -2.0, "decision_strength": 0.0, "signal_quality": 0.18})

        meta = build_meta_regulation_state(perception, processing, felt, thought, fused)

        self.assertLess(meta.get("decision_strength", 0.0), 0.5)
        self.assertFalse(meta.get("allow_plan"))
        self.assertIn(meta.get("pre_action_phase"), {"observe", "replan", "hold"})

    def test_low_courage_does_not_block_mature_bearing_state(self):
        perception, processing, felt, thought, fused = stable_action_inputs()
        perception.update(
            {
                "structure_quality": 0.68,
                "context_confidence": 0.52,
                "visual_clarity": 0.56,
                "visual_object_stability": 0.54,
            }
        )
        processing.update(
            {
                "field_perception_support": 0.42,
                "field_perception_clarity": 0.48,
                "field_perception_stability": 0.46,
                "field_action_support": 0.05,
                "action_clearance": 0.50,
                "action_inhibition": 0.36,
                "processing_load": 0.36,
                "processing_tension": 0.28,
            }
        )
        felt.update(
            {
                "protective_courage": 0.12,
                "load_bearing_capacity": 0.62,
                "experience_regulation": 0.58,
                "felt_pressure": 0.30,
                "felt_conflict": 0.16,
                "pre_action_observation_need": 0.18,
            }
        )
        thought.update(
            {
                "long_hypothesis": 0.58,
                "short_hypothesis": 0.14,
                "state_maturity": 0.74,
                "decision_readiness": 0.80,
                "decision_conflict": 0.10,
                "rumination_depth": 0.08,
            }
        )
        fused.update({"long_score": 0.58, "short_score": 0.14, "signal_quality": 0.52})

        meta = build_meta_regulation_state(perception, processing, felt, thought, fused)

        self.assertNotEqual(meta.get("rejection_reason"), "courage_hold")
        self.assertIn(meta.get("pre_action_phase"), {"act", "act_watch", "observe", "replan"})

    def test_fused_decision_strength_does_not_bypass_thought_hypothesis(self):
        perception, processing, felt, thought, fused = stable_action_inputs()
        perception.update({"structure_quality": 0.34, "context_confidence": 0.24})
        processing.update({"processing_alignment": 0.22, "field_perception_support": 0.14})
        felt.update({"felt_pressure": 0.72, "felt_conflict": 0.58, "pre_action_observation_need": 0.74})
        thought.update(
            {
                "long_hypothesis": 0.18,
                "short_hypothesis": 0.12,
                "state_maturity": 0.22,
                "decision_readiness": 0.20,
                "decision_conflict": 0.62,
            }
        )
        fused.update({"long_score": 0.18, "short_score": 0.12, "decision_strength": 2.4, "signal_quality": 0.16})

        meta = build_meta_regulation_state(perception, processing, felt, thought, fused)

        self.assertLess(meta.get("decision_strength", 0.0), 0.5)
        self.assertFalse(meta.get("allow_plan"))
        self.assertIn(meta.get("pre_action_phase"), {"observe", "replan", "hold"})

    def test_open_hypothesis_feedback_reads_bot_outcome_decomposition(self):
        perception, processing, felt, thought, fused = stable_action_inputs()
        bot = SimpleNamespace(
            last_outcome_decomposition={
                "open_hypothesis_learning_state": "open_hypothesis_burdened",
                "open_hypothesis_consequence_score": 0.10,
                "open_hypothesis_burden_score": 0.72,
                "open_hypothesis_reorganization_score": 0.50,
                "open_hypothesis_replay_need": 0.44,
                "open_hypothesis_distance_need": 0.48,
                "open_hypothesis_reinterpretation_need": 0.52,
            }
        )

        meta = build_meta_regulation_state(perception, processing, felt, thought, fused, bot=bot)

        self.assertEqual(meta.get("previous_open_hypothesis_learning_state"), "open_hypothesis_burdened")
        self.assertGreater(float(meta.get("hypothesis_caution", 0.0)), 0.0)
        self.assertLess(float(meta.get("hypothesis_caution", 0.0)), 0.20)

    def test_plan_allowed_yields_to_metaregulator_reflection(self):
        perception, processing, felt, thought, fused = stable_action_inputs()
        perception.update(
            {
                "structure_quality": 0.72,
                "context_confidence": 0.46,
                "object_contact_depth": 0.06,
                "perceptual_distance": 0.10,
                "inner_outer_alignment": 0.16,
                "field_attachment": 0.30,
            }
        )
        processing.update(
            {
                "field_perception_support": 0.34,
                "field_perception_clarity": 0.50,
                "field_perception_stability": 0.48,
                "field_perception_strain": 0.34,
                "field_action_support": 0.17,
                "action_clearance": 0.46,
                "action_inhibition": 0.42,
                "plan_pressure": 0.70,
            }
        )
        felt.update(
            {
                "felt_pressure": 0.45,
                "felt_conflict": 0.20,
                "experience_regulation": 0.42,
                "load_bearing_capacity": 0.45,
                "protective_courage": 0.44,
                "nervous_context_overcoupling": 0.40,
                "nervous_overload_reflection_need": 0.32,
                "dominant_tension_cause": "-",
                "dominant_tension_value": 0.0,
                "pre_action_observation_need": 0.24,
            }
        )
        thought.update(
            {
                "long_hypothesis": 1.48,
                "short_hypothesis": 0.16,
                "state_maturity": 0.80,
                "decision_readiness": 0.72,
                "decision_conflict": 0.12,
                "rumination_depth": 0.10,
            }
        )
        fused.update({"long_score": 1.48, "signal_quality": 0.68})

        meta = build_meta_regulation_state(perception, processing, felt, thought, fused)

        self.assertFalse(meta.get("allow_plan"))
        self.assertIn(meta.get("pre_action_phase"), {"observe", "replan"})
        self.assertIn(
            meta.get("rejection_reason"),
            {"metaregulator_reflection_observe", "metaregulator_reflection_replan"},
        )


if __name__ == "__main__":
    unittest.main()
