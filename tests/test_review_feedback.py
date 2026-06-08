import unittest

from core.review_feedback import resolve_review_decision_feedback


class StatsStub:
    def __init__(self, feedback):
        self._feedback = dict(feedback or {})

    def get_attempt_feedback(self):
        return dict(self._feedback)


class BotStub:
    def __init__(self, feedback):
        self.stats = StatsStub(feedback)
        self.mcm_decision_episode_internal = {
            "review_notes": {
                "review_score": 0.42,
                "structural_bearing_quality": 0.42,
                "observation_quality": 0.20,
                "uncertainty_recognition_quality": 0.20,
            }
        }
        self.mcm_experience_space = {}


class ReviewFeedbackTests(unittest.TestCase):

    def test_dominant_hypothesis_trust_is_scoped_to_runtime_form(self):
        feedback = {
            "hypothesis_trust_priority": 0.20,
            "hypothesis_trust_score": 0.70,
            "dominant_hypothesis_trust_key": "fs_known",
            "dominant_hypothesis_trust_score": 0.90,
            "hypothesis_confirmation_without_action": 0.15,
            "hypothesis_observation_maturity": 0.50,
            "possibility_maturity": 0.20,
            "possibility_caution": 0.05,
            "hypothesis_observed_stability": 0.20,
        }
        bot = BotStub(feedback)

        matched = resolve_review_decision_feedback(
            bot=bot,
            runtime_result={"form_symbol_id": "fs_known"},
        )
        mismatched = resolve_review_decision_feedback(
            bot=bot,
            runtime_result={"form_symbol_id": "fs_other"},
        )

        self.assertTrue(matched.get("dominant_hypothesis_trust_matches_form"))
        self.assertFalse(mismatched.get("dominant_hypothesis_trust_matches_form"))
        self.assertGreater(
            matched.get("dominant_hypothesis_trust_score", 0.0),
            mismatched.get("dominant_hypothesis_trust_score", 1.0),
        )
        self.assertGreater(
            matched.get("possibility_action_support", 0.0),
            mismatched.get("possibility_action_support", 1.0),
        )
        self.assertGreater(
            matched.get("hypothesis_trust_priority", 0.0),
            mismatched.get("hypothesis_trust_priority", 1.0),
        )
        self.assertGreater(
            matched.get("hypothesis_trust_score", 0.0),
            mismatched.get("hypothesis_trust_score", 1.0),
        )
        self.assertGreater(
            mismatched.get("borrowed_dominant_hypothesis_pressure", 0.0),
            matched.get("borrowed_dominant_hypothesis_pressure", 1.0),
        )
        self.assertGreater(
            mismatched.get("borrowed_hypothesis_trust_pressure", 0.0),
            matched.get("borrowed_hypothesis_trust_pressure", 1.0),
        )


if __name__ == "__main__":
    unittest.main()
