import json
import sys
import tempfile
import types
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

api_stub = types.ModuleType("api")
api_stub.API_KEY = ""
api_stub.API_SECRET = ""
sys.modules.setdefault("api", api_stub)

import bot as bot_module
from trading.trade_stats import TradeStats


class BotTimeoutOutcomePersistenceTests(unittest.TestCase):
    
    def test_backtest_timeout_passes_outcome_decomposition_to_cancel_stats(self):
        with tempfile.TemporaryDirectory() as tmp:
            stats_path = Path(tmp) / "trade_stats.json"
            csv_path = Path(tmp) / "trade_equity.csv"
            attempt_path = Path(tmp) / "attempt_records.jsonl"
            outcome_path = Path(tmp) / "outcome_records.jsonl"

            bot = bot_module.Bot(filepath=str(Path(tmp) / "dummy.csv"))
            bot.stats = TradeStats(
                path=str(stats_path),
                csv_path=str(csv_path),
                attempt_path=str(attempt_path),
                outcome_path=str(outcome_path),
                reset=True,
            )
            bot.processed = 10
            bot.pending_entry = {
                "side": "LONG",
                "entry": 105.0,
                "tp": 107.0,
                "sl": 104.0,
                "risk": 1.0,
                "created_index": 0,
                "max_wait_bars": 0,
                "meta": {
                    "structure_perception_state": {
                        "structure_quality": 0.78,
                    },
                    "felt_state": {
                        "pressure": 0.31,
                    },
                    "thought_state": {
                        "maturity": 0.49,
                    },
                    "meta_regulation_state": {
                        "decision": "LONG",
                    },
                    "expectation_state": {
                        "entry_expectation": 0.57,
                    },
                },
            }

            saved_calls = []

            def fake_apply_outcome_stimulus(bot_obj, reason, position=None):
                bot_obj.last_outcome_decomposition = {
                    "reason": str(reason),
                    "execution_quality": 0.25,
                }
                return {"reason": reason}

            def fake_save_memory_state():
                saved_calls.append(True)
                return {"saved": True}

            original_apply = bot_module.apply_outcome_stimulus
            bot_module.apply_outcome_stimulus = fake_apply_outcome_stimulus
            bot._save_memory_state = fake_save_memory_state

            try:
                window = [
                    {"timestamp": 1, "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 10.0},
                    {"timestamp": 2, "open": 100.5, "high": 101.2, "low": 99.4, "close": 100.2, "volume": 11.0},
                ]
                bot._process_window(window)
            finally:
                bot_module.apply_outcome_stimulus = original_apply

            saved = json.loads(stats_path.read_text(encoding="utf-8"))
            records = [
                json.loads(line)
                for line in outcome_path.read_text(encoding="utf-8").splitlines()
                if str(line).strip()
            ]

            self.assertEqual(saved.get("last_outcome_decomposition"), {"reason": "timeout", "execution_quality": 0.25})
            self.assertEqual(int(saved.get("cancels", 0)), 1)
            self.assertNotIn("outcome_records", saved)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].get("cause"), "backtest_timeout")
            self.assertEqual(records[0].get("outcome_decomposition"), {"reason": "timeout", "execution_quality": 0.25})
            self.assertTrue(bool(saved_calls))

if __name__ == "__main__":
    unittest.main()
