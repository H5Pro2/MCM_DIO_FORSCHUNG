import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import bot_gates.entry_decision as gate_module


class BotStub:
    pass


def supportive_inner_action_state(side):
    return {
        "decision": side,
        "allow_plan": True,
        "pre_action_phase": "act",
        "inner_outer_alignment": 0.72,
        "regulated_courage": 0.68,
        "action_clearance": 0.66,
        "action_inhibition": 0.08,
        "field_observation_need": 0.08,
        "pre_action_reorganization_pressure": 0.05,
        "trust_return_act_bridge": 0.48,
        "open_hypothesis_action_permission": 0.58,
        "possibility_action_support": 0.62,
        "possibility_reality_check_need": 0.08,
        "hypothesis_trust_score": 0.64,
        "hypothesis_trust_priority": 0.62,
        "dominant_hypothesis_trust_score": 0.58,
        "hypothesis_confirmation_without_action": 0.64,
        "hypothesis_rejection_without_action": 0.04,
        "hypothesis_observation_maturity": 0.70,
        "hypothesis_observed_stability": 0.55,
        "hypothesis_frustration_risk": 0.05,
        "hypothesis_distance_risk": 0.06,
        "contact_carrying_quality": 0.55,
        "contact_action_maturity": 0.50,
        "contact_overcoupling_risk": 0.08,
        "contact_reality_check": 0.10,
    }


def supportive_entry_fields(side):
    return {
        "entry_mode": "area_contact_entry",
        "entry_choice_state": "area_preferred",
        "area_direct_readiness": 0.55,
        "entry_choice_bearing": 0.55,
        "strategic_entry_fit": 0.55,
        "area_motor_restraint": 0.05,
        "form_symbol_state": {
            "form_symbol_action_trust": 0.45,
            "form_symbol_contact_maturity": 0.42,
        },
        "thought_state": {
            "maturity": 0.57,
            "thought_confirmation_score": 0.52,
        },
        "meta_regulation_state": supportive_inner_action_state(side),
    }


def long_brain_plan():
    return {
        "decision": "LONG",
        "entry_price": 100.0,
        "tp_price": 104.0,
        "sl_price": 98.0,
        "rr_value": 2.0,
        "energy": 0.77,
        "coherence": 0.41,
        "asymmetry": 1,
        "coh_zone": 1.0,
        "self_state": "stable",
        "attractor": "cooperate",
        "memory_center": 0.28,
        "memory_strength": 5,
        "vision": {"left_eye_field": 0.22},
        "filtered_vision": {"target_map": 0.61},
        "focus": {"focus_confidence": 0.66, "target_lock": 0.49},
        "world_state": {"tension_state": {"energy": 0.77}},
        "structure_perception_state": {"structure_quality": 0.81},
        "outer_visual_perception_state": {"signal_relevance": 0.58},
        "inner_field_perception_state": {"field_mean_energy": 0.31},
        "processing_state": {"processing_readiness": 0.73},
        "perception_state": {"structure_quality": 0.81},
        "felt_state": {"pressure": 0.19},
        **supportive_entry_fields("LONG"),
        "expectation_state": {"entry_expectation": 0.62, "target_expectation": 0.54},
        "state_signature": {"signature_key": "sig_runtime"},
        "entry_validity_band": {"lower": 99.5, "upper": 100.5},
        "target_conviction": 0.63,
        "risk_model_score": 0.38,
        "reward_model_score": 0.71,
        "signature_bias": 0.12,
        "signature_block": False,
        "signature_quality": 0.59,
        "signature_distance": 0.08,
        "context_cluster_id": "ctx_7",
        "context_cluster_bias": 0.14,
        "context_cluster_quality": 0.69,
        "context_cluster_distance": 0.11,
        "context_cluster_block": False,
        "inhibition_level": 0.09,
        "habituation_level": 0.04,
        "competition_bias": -0.03,
        "observation_mode": False,
        "long_score": 1.18,
        "short_score": -0.26,
    }


class BotGateFunktionsTests(unittest.TestCase):

    def test_evaluate_entry_decision_uses_runtime_tendency_then_brain_plan(self):
        original_runtime = gate_module.build_runtime_decision_tendency
        original_brain = gate_module.decide_mcm_brain_entry
        original_debug = gate_module.DEBUG

        calls = {"brain_calls": 0}

        def fake_runtime(window, candle_state, bot=None):
            return {
                "decision_tendency": "act",
                "proposed_decision": "LONG",
                "focus": {"focus_strength": 0.66},
            }

        def fake_brain(window, candle_state, bot=None):
            calls["brain_calls"] += 1
            return long_brain_plan()

        try:
            gate_module.build_runtime_decision_tendency = fake_runtime
            gate_module.decide_mcm_brain_entry = fake_brain
            gate_module.DEBUG = False

            result = gate_module.evaluate_entry_decision(
                BotStub(),
                [{"timestamp": 1, "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 10.0}],
                {"close": 100.5},
            )

            self.assertEqual(calls["brain_calls"], 1)
            self.assertEqual(result.get("decision"), "LONG")
            self.assertEqual(result.get("decision_tendency"), "act")
            self.assertEqual(float(result.get("rr_value", 0.0)), 2.0)
            self.assertEqual(result.get("inner_action_consent_state"), "inner_state_allows_action")
            self.assertEqual(result.get("state_signature", {}).get("signature_key"), "sig_runtime")
            self.assertEqual(result.get("context_cluster_id"), "ctx_7")
        finally:
            gate_module.build_runtime_decision_tendency = original_runtime
            gate_module.decide_mcm_brain_entry = original_brain
            gate_module.DEBUG = original_debug

    def test_evaluate_entry_decision_returns_none_when_runtime_tendency_is_missing(self):
        original_runtime = gate_module.build_runtime_decision_tendency
        original_brain = gate_module.decide_mcm_brain_entry
        original_debug = gate_module.DEBUG

        calls = {"brain_calls": 0}

        def fake_runtime(window, candle_state, bot=None):
            return None

        def fake_brain(window, candle_state, bot=None):
            calls["brain_calls"] += 1
            return long_brain_plan()

        try:
            gate_module.build_runtime_decision_tendency = fake_runtime
            gate_module.decide_mcm_brain_entry = fake_brain
            gate_module.DEBUG = False

            result = gate_module.evaluate_entry_decision(
                BotStub(),
                [{"timestamp": 2, "open": 100.0, "high": 101.0, "low": 98.0, "close": 99.0, "volume": 11.0}],
                {"close": 99.0},
            )

            self.assertIsNone(result)
            self.assertEqual(calls["brain_calls"], 0)
        finally:
            gate_module.build_runtime_decision_tendency = original_runtime
            gate_module.decide_mcm_brain_entry = original_brain
            gate_module.DEBUG = original_debug

    def test_evaluate_entry_decision_requires_explicit_decision_tendency(self):
        original_runtime = gate_module.build_runtime_decision_tendency
        original_brain = gate_module.decide_mcm_brain_entry
        original_debug = gate_module.DEBUG

        calls = {"brain_calls": 0}

        def fake_runtime(window, candle_state, bot=None):
            return {
                "decision": "LONG",
                "proposed_decision": "LONG",
                "allow_plan": True,
                "focus": {"focus_strength": 0.72},
                "meta_regulation_state": {"allow_plan": True, "pre_action_phase": "act"},
            }

        def fake_brain(window, candle_state, bot=None):
            calls["brain_calls"] += 1
            return long_brain_plan()

        try:
            gate_module.build_runtime_decision_tendency = fake_runtime
            gate_module.decide_mcm_brain_entry = fake_brain
            gate_module.DEBUG = False

            result = gate_module.evaluate_entry_decision(
                BotStub(),
                [{"timestamp": 5, "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 10.0}],
                {"close": 100.5},
            )

            self.assertEqual(calls["brain_calls"], 0)
            self.assertEqual(result.get("decision_tendency"), "hold")
            self.assertEqual(result.get("proposed_decision"), "LONG")
            self.assertEqual(result.get("decision"), None)
            self.assertFalse(result.get("execution_state", {}).get("execution_ready", True))
        finally:
            gate_module.build_runtime_decision_tendency = original_runtime
            gate_module.decide_mcm_brain_entry = original_brain
            gate_module.DEBUG = original_debug

    def test_evaluate_entry_decision_does_not_call_brain_when_allow_plan_is_false(self):
        original_runtime = gate_module.build_runtime_decision_tendency
        original_brain = gate_module.decide_mcm_brain_entry
        original_debug = gate_module.DEBUG

        calls = {"brain_calls": 0}

        def fake_runtime(window, candle_state, bot=None):
            return {
                "decision_tendency": "act",
                "proposed_decision": "LONG",
                "allow_plan": False,
                "focus": {"focus_strength": 0.66},
                "meta_regulation_state": {"allow_plan": False, "pre_action_phase": "observe"},
            }

        def fake_brain(window, candle_state, bot=None):
            calls["brain_calls"] += 1
            return long_brain_plan()

        try:
            gate_module.build_runtime_decision_tendency = fake_runtime
            gate_module.decide_mcm_brain_entry = fake_brain
            gate_module.DEBUG = False

            result = gate_module.evaluate_entry_decision(
                BotStub(),
                [{"timestamp": 4, "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 10.0}],
                {"close": 100.5},
            )

            self.assertEqual(calls["brain_calls"], 0)
            self.assertEqual(result.get("decision"), "WAIT")
            self.assertEqual(result.get("proposed_decision"), "LONG")
            self.assertEqual(result.get("decision_tendency"), "observe")
            self.assertEqual(result.get("rejection_reason"), "runtime_allow_plan_false")
        finally:
            gate_module.build_runtime_decision_tendency = original_runtime
            gate_module.decide_mcm_brain_entry = original_brain
            gate_module.DEBUG = original_debug

    def test_evaluate_entry_decision_converts_unconfirmed_brain_trade_to_withheld(self):
        original_runtime = gate_module.build_runtime_decision_tendency
        original_brain = gate_module.decide_mcm_brain_entry
        original_debug = gate_module.DEBUG

        calls = {"brain_calls": 0}

        def fake_runtime(window, candle_state, bot=None):
            return {
                "decision_tendency": "act",
                "proposed_decision": "LONG",
                "focus": {"focus_strength": 0.44},
            }

        def fake_brain(window, candle_state, bot=None):
            calls["brain_calls"] += 1
            return {
                "decision": "LONG",
                "entry_price": 100.0,
                "tp_price": 104.0,
                "sl_price": 98.0,
                "rr_value": 2.0,
                "focus": {"focus_strength": 0.44},
                "meta_regulation_state": {"pre_action_phase": "hold"},
            }

        try:
            gate_module.build_runtime_decision_tendency = fake_runtime
            gate_module.decide_mcm_brain_entry = fake_brain
            gate_module.DEBUG = False

            result = gate_module.evaluate_entry_decision(
                BotStub(),
                [{"timestamp": 3, "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 10.0}],
                {"close": 100.5},
            )

            self.assertEqual(calls["brain_calls"], 1)
            self.assertEqual(result.get("decision"), "WAIT")
            self.assertEqual(result.get("proposed_decision"), "LONG")
            self.assertEqual(result.get("decision_tendency"), "hold")
            self.assertEqual(result.get("rejection_reason"), "impulse_needs_inner_processing")
            self.assertFalse(result.get("execution_state", {}).get("execution_ready", True))
        finally:
            gate_module.build_runtime_decision_tendency = original_runtime
            gate_module.decide_mcm_brain_entry = original_brain
            gate_module.DEBUG = original_debug

    def test_open_hypothesis_reinterpret_seed_waits_for_replay(self):
        original_runtime = gate_module.build_runtime_decision_tendency
        original_brain = gate_module.decide_mcm_brain_entry
        original_debug = gate_module.DEBUG

        def fake_runtime(window, candle_state, bot=None):
            return {
                "decision_tendency": "act",
                "proposed_decision": "SHORT",
                "focus": {"focus_strength": 0.66},
            }

        def fake_brain(window, candle_state, bot=None):
            plan = long_brain_plan()
            plan["decision"] = "SHORT"
            plan["entry_price"] = 100.0
            plan["tp_price"] = 92.0
            plan["sl_price"] = 102.0
            plan["rr_value"] = 4.0
            plan["thought_seed_state"] = {
                "emergent_structure_state": "open_structural_hypothesis",
                "seed_metaregulator_state": "seed_reinterpret",
                "thought_confirmation_score": 0.27,
                "reality_binding_score": 0.30,
                "thought_structural_grounding": 0.24,
                "thought_open_hypothesis_pressure": 0.58,
                "thought_reality_lag": 0.34,
                "borrowed_open_hypothesis_pressure": 0.42,
                "reorganization_echo": 0.35,
                "consequence_echo": 0.08,
            }
            plan["meta_regulation_state"].update(
                {
                    "pre_action_phase": "act",
                    "previous_open_hypothesis_learning_state": "-",
                    "open_hypothesis_reifung_state": "open_hypothesis_neutral_memory",
                }
            )
            return plan

        try:
            gate_module.build_runtime_decision_tendency = fake_runtime
            gate_module.decide_mcm_brain_entry = fake_brain
            gate_module.DEBUG = False

            result = gate_module.evaluate_entry_decision(
                BotStub(),
                [{"timestamp": 6, "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 10.0}],
                {"close": 100.5},
            )

            self.assertEqual(result.get("decision"), "WAIT")
            self.assertEqual(result.get("proposed_decision"), "SHORT")
            self.assertIn(result.get("decision_tendency"), ("observe", "replan"))
            self.assertEqual(result.get("rejection_reason"), "open_hypothesis_needs_reality_contact")
        finally:
            gate_module.build_runtime_decision_tendency = original_runtime
            gate_module.decide_mcm_brain_entry = original_brain
            gate_module.DEBUG = original_debug

    def test_weak_open_hypothesis_action_ready_still_waits_for_contact(self):
        original_runtime = gate_module.build_runtime_decision_tendency
        original_brain = gate_module.decide_mcm_brain_entry
        original_debug = gate_module.DEBUG

        def fake_runtime(window, candle_state, bot=None):
            return {
                "decision_tendency": "act",
                "proposed_decision": "SHORT",
                "focus": {"focus_strength": 0.66},
            }

        def fake_brain(window, candle_state, bot=None):
            plan = long_brain_plan()
            plan["decision"] = "SHORT"
            plan["entry_price"] = 100.0
            plan["tp_price"] = 92.0
            plan["sl_price"] = 102.0
            plan["rr_value"] = 4.0
            plan["thought_seed_state"] = {
                "emergent_structure_state": "open_structural_hypothesis",
                "seed_metaregulator_state": "seed_action_ready",
                "thought_confirmation_score": 0.30,
                "reality_binding_score": 0.28,
                "thought_structural_grounding": 0.25,
                "thought_open_hypothesis_pressure": 0.50,
                "thought_reality_lag": 0.30,
                "borrowed_open_hypothesis_pressure": 0.28,
                "reorganization_echo": 0.25,
                "consequence_echo": 0.05,
            }
            plan["meta_regulation_state"].update(
                {
                    "pre_action_phase": "act",
                    "previous_open_hypothesis_learning_state": "-",
                    "open_hypothesis_reifung_state": "open_hypothesis_neutral_memory",
                }
            )
            return plan

        try:
            gate_module.build_runtime_decision_tendency = fake_runtime
            gate_module.decide_mcm_brain_entry = fake_brain
            gate_module.DEBUG = False

            result = gate_module.evaluate_entry_decision(
                BotStub(),
                [{"timestamp": 8, "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 10.0}],
                {"close": 100.5},
            )

            self.assertEqual(result.get("decision"), "WAIT")
            self.assertEqual(result.get("proposed_decision"), "SHORT")
            self.assertEqual(result.get("rejection_reason"), "open_hypothesis_needs_reality_contact")
        finally:
            gate_module.build_runtime_decision_tendency = original_runtime
            gate_module.decide_mcm_brain_entry = original_brain
            gate_module.DEBUG = original_debug

    def test_ordinary_structure_without_bearing_does_not_become_motor_action(self):
        decision = {
            "decision": "LONG",
            "entry_mode": "area_contact_entry",
            "entry_choice_state": "area_preferred",
            "area_direct_readiness": 0.18,
            "entry_choice_bearing": 0.20,
            "strategic_entry_fit": 0.18,
            "area_motor_restraint": 0.05,
            "meta_regulation_state": {
                "pre_action_phase": "act",
                "inner_outer_alignment": 0.46,
                "regulated_courage": 0.42,
                "action_clearance": 0.42,
                "action_inhibition": 0.10,
                "field_observation_need": 0.10,
                "pre_action_reorganization_pressure": 0.06,
                "possibility_action_support": 0.08,
                "possibility_reality_check_need": 0.18,
                "hypothesis_trust_score": 0.08,
                "hypothesis_trust_priority": 0.06,
                "hypothesis_confirmation_without_action": 0.12,
                "hypothesis_rejection_without_action": 0.22,
                "hypothesis_observation_maturity": 0.35,
                "hypothesis_observed_stability": 0.14,
            },
            "structure_perception_state": {"structure_quality": 0.22, "context_confidence": 0.18},
            "expectation_state": {"target_expectation": 0.20, "reflection_maturity": 0.18},
            "form_symbol_state": {"form_symbol_action_trust": 0.08, "form_symbol_contact_maturity": 0.10},
            "thought_state": {"thought_confirmation_score": 0.10},
            "thought_seed_state": {"emergent_structure_state": "ordinary_structure_reading"},
        }

        consent = gate_module._resolve_inner_action_consent(decision)

        self.assertFalse(consent.get("allowed", True))
        self.assertEqual(consent.get("reason"), "ordinary_structure_needs_bearing")

    def test_confirmed_hypothesis_seed_can_still_act(self):
        original_runtime = gate_module.build_runtime_decision_tendency
        original_brain = gate_module.decide_mcm_brain_entry
        original_debug = gate_module.DEBUG

        def fake_runtime(window, candle_state, bot=None):
            return {
                "decision_tendency": "act",
                "proposed_decision": "LONG",
                "focus": {"focus_strength": 0.66},
            }

        def fake_brain(window, candle_state, bot=None):
            plan = long_brain_plan()
            plan["thought_seed_state"] = {
                "emergent_structure_state": "confirmed_structural_interpretation",
                "seed_metaregulator_state": "seed_action_ready",
                "thought_confirmation_score": 0.62,
                "reality_binding_score": 0.58,
                "thought_structural_grounding": 0.55,
                "thought_open_hypothesis_pressure": 0.16,
                "thought_reality_lag": 0.08,
                "reorganization_echo": 0.05,
                "consequence_echo": 0.40,
            }
            return plan

        try:
            gate_module.build_runtime_decision_tendency = fake_runtime
            gate_module.decide_mcm_brain_entry = fake_brain
            gate_module.DEBUG = False

            result = gate_module.evaluate_entry_decision(
                BotStub(),
                [{"timestamp": 7, "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 10.0}],
                {"close": 100.5},
            )

            self.assertEqual(result.get("decision"), "LONG")
            self.assertEqual(result.get("decision_tendency"), "act")
            self.assertEqual(result.get("inner_action_consent_state"), "inner_state_allows_action")
        finally:
            gate_module.build_runtime_decision_tendency = original_runtime
            gate_module.decide_mcm_brain_entry = original_brain
            gate_module.DEBUG = original_debug

    def test_dominant_hypothesis_trust_is_scoped_to_current_form(self):
        base_meta = {
            "pre_action_phase": "act",
            "inner_outer_alignment": 0.34,
            "regulated_courage": 0.32,
            "action_clearance": 0.32,
            "action_inhibition": 0.08,
            "field_observation_need": 0.08,
            "pre_action_reorganization_pressure": 0.04,
            "possibility_action_support": 0.04,
            "possibility_reality_check_need": 0.10,
            "hypothesis_observed_stability": 0.18,
            "hypothesis_observation_maturity": 0.52,
            "dominant_hypothesis_trust_score": 0.90,
        }
        decision = {
            "decision": "LONG",
            "entry_mode": "area_contact_entry",
            "entry_choice_state": "area_preferred",
            "meta_regulation_state": dict(base_meta, dominant_hypothesis_trust_key="fs_old"),
            "form_symbol_state": {"form_symbol_id": "fs_current"},
            "structure_perception_state": {"structure_quality": 0.36, "context_confidence": 0.30},
            "expectation_state": {"target_expectation": 0.24, "reflection_maturity": 0.20},
            "thought_state": {"thought_confirmation_score": 0.12},
            "thought_seed_state": {"emergent_structure_state": "ordinary_structure_reading"},
        }

        mismatched = gate_module._resolve_inner_action_consent(decision)
        matched_decision = dict(decision)
        matched_decision["meta_regulation_state"] = dict(base_meta, dominant_hypothesis_trust_key="fs_current")
        matched = gate_module._resolve_inner_action_consent(matched_decision)

        self.assertLess(mismatched.get("strategy_confirmation", 1.0), matched.get("strategy_confirmation", 0.0))
        self.assertGreater(mismatched.get("strategy_rejection", 0.0), matched.get("strategy_rejection", 1.0))
        self.assertFalse(mismatched.get("allowed", True))


if __name__ == "__main__":
    unittest.main()
