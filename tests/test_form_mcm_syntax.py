import unittest

from core.form_language import _build_dio_form_language_state
from core.thought_memory import _update_thought_memory
from config import Config


class DummyBot:
    pass


class FormMcmSyntaxTests(unittest.TestCase):
    def test_form_mcm_syntax_token_binds_form_and_field(self):
        seed = {
            "thought_seed_id": "ts_test",
            "thought_trace_strength": 0.62,
            "thought_recall_potential": 0.55,
            "thought_confirmation_score": 0.51,
            "reality_binding_score": 0.48,
            "thought_structural_grounding": 0.46,
            "thought_consequence_balance": 0.20,
            "own_field_binding_pull": 0.45,
            "emergent_structure_state": "open_structural_hypothesis",
            "seed_metaregulator_state": "seed_focus",
            "thought_reifung_direction": "replay_maturation",
            "semantic_origin_state": "own_form_language",
            "form_symbol_anchor": "fs_test",
            "mcm_field_anchor": "quiet_field",
            "experience_memory_anchor": "context_test",
            "decision": "WAIT",
            "phase": "observe",
        }
        form = {
            "form_symbol_id": "fs_test",
            "form_symbol_compound_id": "fc_test",
            "form_symbol_semantic_density": 0.60,
            "form_symbol_semantic_compression": 0.58,
            "form_symbol_semantic_coherence": 0.54,
            "form_symbol_stability": 0.50,
        }
        meta = {
            "field_perception_label": "quiet_field",
            "structure_quality": 0.50,
            "context_confidence": 0.48,
            "visual_clarity": 0.52,
            "visual_object_stability": 0.50,
            "inner_outer_alignment": 0.47,
            "contact_carrying_quality": 0.44,
            "field_action_support": 0.40,
        }

        state = _build_dio_form_language_state(seed, form_state=form, meta_regulation_state=meta)

        self.assertTrue(state["dio_form_mcm_token"].startswith("fm_"))
        self.assertTrue(state["dio_form_mcm_family_token"].startswith("fmf_"))
        self.assertIn("form_mcm:", state["dio_dialogue_bridge_sentence"])
        self.assertIn("family:", state["dio_form_mcm_sentence"])
        self.assertGreater(state["form_to_mcm_recall"], 0.0)
        self.assertGreater(state["mcm_to_form_confirmation"], 0.0)
        self.assertGreater(state["visual_mcm_context_fit"], 0.0)
        self.assertGreaterEqual(state["visual_mcm_mismatch"], 0.0)
        self.assertIn(
            state["dio_form_mcm_syntax_state"],
            {
                "unbound_form_field_syntax",
                "form_field_mismatch_watch",
                "bound_form_field_memory",
                "emerging_form_field_recall",
                "partial_form_field_contact",
            },
        )


class FormMcmFamilyMemoryTests(unittest.TestCase):
    def test_form_mcm_family_feedback_accumulates_soft_reifung(self):
        prior_every_n = getattr(Config, "MCM_THOUGHT_MEMORY_SAVE_EVERY_N", 64)
        Config.MCM_THOUGHT_MEMORY_SAVE_EVERY_N = 999999
        try:
            bot = DummyBot()
            bot.mcm_thought_memory = {}
            bot.mcm_thought_family_memory = {}
            bot.mcm_form_mcm_family_memory = {}
            bot.mcm_thought_memory_summary = {}
            bot._thought_memory_loaded = True

            seed = {
                "thought_seed_id": "ts_family",
                "thought_seed_label": "seed",
                "dio_form_mcm_token": "fm_detail_a",
                "dio_form_mcm_family_token": "fmf_family_a",
                "dio_form_mcm_syntax_state": "bound_form_field_memory",
                "dio_form_mcm_sentence": "family:fmf_family_a|state:bound_form_field_memory",
                "form_to_mcm_recall": 0.62,
                "mcm_to_form_confirmation": 0.58,
                "visual_mcm_context_fit": 0.60,
                "visual_mcm_mismatch": 0.08,
                "hypothesis_reality_binding": 0.56,
                "form_mcm_syntax_density": 0.64,
                "thought_confirmation_score": 0.55,
                "thought_open_hypothesis_pressure": 0.20,
                "thought_consequence_balance": 0.25,
                "emergent_structure_state": "open_structural_hypothesis",
                "seed_metaregulator_state": "seed_focus",
                "thought_reifung_direction": "replay_maturation",
                "semantic_origin_state": "own_form_language",
                "form_symbol_anchor": "fs_test",
                "mcm_field_anchor": "quiet_field",
                "experience_memory_anchor": "context_test",
                "phase": "observe",
                "decision": "WAIT",
            }

            first = _update_thought_memory(bot, seed, timestamp=1, runtime_tick=1)
            second = _update_thought_memory(bot, {**seed, "thought_seed_id": "ts_family_2"}, timestamp=2, runtime_tick=2)

            self.assertIn("fmf_family_a", bot.mcm_form_mcm_family_memory)
            self.assertEqual(bot.mcm_form_mcm_family_memory["fmf_family_a"]["seen"], 2)
            self.assertGreater(second["form_mcm_family_recurrence"], first["form_mcm_family_recurrence"])
            self.assertGreater(second["form_mcm_family_maturity"], 0.0)
            self.assertGreater(second["form_mcm_family_trust"], 0.0)
            self.assertLess(second["form_mcm_family_caution"], 0.5)
        finally:
            Config.MCM_THOUGHT_MEMORY_SAVE_EVERY_N = prior_every_n


if __name__ == "__main__":
    unittest.main()
