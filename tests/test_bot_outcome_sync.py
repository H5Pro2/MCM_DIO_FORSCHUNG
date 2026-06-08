import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from bot import Bot


class BotOutcomeSyncTests(unittest.TestCase):
    def test_sync_prefers_enriched_outcome_decomposition(self):
        bot = SimpleNamespace(
            stats=SimpleNamespace(
                data={
                    "last_outcome_decomposition": {
                        "reason": "tp_hit",
                        "plan_quality": 0.7,
                    },
                    "last_outcome_decomposition_enriched": {
                        "reason": "tp_hit",
                        "plan_quality": 0.7,
                        "open_hypothesis_learning_state": "open_hypothesis_carried",
                        "open_hypothesis_consequence_score": 0.66,
                    },
                }
            ),
            last_outcome_decomposition={},
        )

        Bot._sync_last_outcome_decomposition_from_stats(bot)

        self.assertEqual(
            bot.last_outcome_decomposition.get("open_hypothesis_learning_state"),
            "open_hypothesis_carried",
        )
        self.assertAlmostEqual(
            float(bot.last_outcome_decomposition.get("open_hypothesis_consequence_score")),
            0.66,
        )


if __name__ == "__main__":
    unittest.main()
