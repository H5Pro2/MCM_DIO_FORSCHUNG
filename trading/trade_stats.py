# ==================================================
# trade_stats.py
# ==================================================
# PERSISTENTE TRADE-STATISTIK
# - wird vom Bot bei EXIT aufgerufen
# - speichert aggregierte Werte in JSON
# - keine Abhängigkeit vom Bot-State
# ==================================================

import json
import os
import time
from config import Config
from core.hypothesis_learning import (
    derive_open_hypothesis_learning,
    refresh_observation_learning_summary,
    resolve_pending_observations,
)
from debug_tools.writers import dbr_append_text, dbr_debug, dbr_file_write_profile, dbr_resolve_path

class TradeStats:

    @staticmethod
    def _is_live_mode():
        return str(getattr(Config, "MODE", "LIVE")).upper() == "LIVE"

    @staticmethod
    def _live_equity_sync_enabled():
        return bool(getattr(Config, "LIVE_EQUITY_SYNC_ENABLED", True))

    @staticmethod
    def _fetch_live_account_equity():
        from trading.exchange_data import create_exchange, get_account_value

        exchange = create_exchange()
        return float(get_account_value(exchange, Config.USDT))

    def _resolve_start_equity(self):
        fallback_equity = float(getattr(Config, "START_EQUITY", 0.0) or 0.0)
        if not self._is_live_mode():
            return fallback_equity

        try:
            live_equity = self._fetch_live_account_equity()
            if live_equity > 0.0:
                dbr_debug(
                    f"LIVE_EQUITY_INIT | source=phemex_futures equity={live_equity:.8f}",
                    "mcm_live_equity_sync.csv",
                )
                return float(live_equity)
            dbr_debug(
                f"LIVE_EQUITY_INIT_FALLBACK | reason=non_positive_exchange_equity exchange_equity={live_equity:.8f} fallback={fallback_equity:.8f}",
                "mcm_live_equity_sync.csv",
            )
        except Exception as exc:
            dbr_debug(
                f"LIVE_EQUITY_INIT_FALLBACK | reason=exchange_error error={type(exc).__name__}:{str(exc).replace(';', '|')} fallback={fallback_equity:.8f}",
                "mcm_live_equity_sync.csv",
            )

        return fallback_equity

    def _sync_live_account_equity(self, reason="sync"):
        if not self._is_live_mode() or not self._live_equity_sync_enabled():
            return False

        try:
            live_equity = self._fetch_live_account_equity()
            if live_equity <= 0.0:
                dbr_debug(
                    f"LIVE_EQUITY_SYNC_SKIPPED | reason=non_positive_exchange_equity exchange_equity={live_equity:.8f}",
                    "mcm_live_equity_sync.csv",
                )
                return False

            start_equity = float(self.data.get("start_equity", 0.0) or 0.0)
            local_equity = float(self.data.get("current_equity", start_equity) or start_equity)
            self.data["current_equity"] = float(live_equity)
            self.data["pnl_netto"] = float(live_equity - start_equity)
            dbr_debug(
                f"LIVE_EQUITY_SYNC | reason={str(reason or 'sync')} start_equity={start_equity:.8f} live_equity={live_equity:.8f} local_equity_before={local_equity:.8f} pnl_netto={float(self.data.get('pnl_netto', 0.0) or 0.0):.8f}",
                "mcm_live_equity_sync.csv",
            )
            return True
        except Exception as exc:
            dbr_debug(
                f"LIVE_EQUITY_SYNC_FAILED | reason={str(reason or 'sync')} error={type(exc).__name__}:{str(exc).replace(';', '|')}",
                "mcm_live_equity_sync.csv",
            )
            return False

    def __init__(
        self,
        path="debug/trade_stats.json",
        csv_path="debug/trade_equity.csv",
        attempt_path="debug/attempt_records.jsonl",
        outcome_path="debug/outcome_records.jsonl",
        reset=True,
    ):
        self._attempt_record_path_explicit = str(attempt_path or "") != "debug/attempt_records.jsonl"
        self.path = dbr_resolve_path(path)
        self.csv_path = dbr_resolve_path(csv_path)
        self.attempt_path = dbr_resolve_path(attempt_path)
        self.outcome_path = dbr_resolve_path(outcome_path)
        self.exit_candidate_replay_path = dbr_resolve_path("debug/mcm_exit_candidate_replay.csv")
        self._outcome_records_cache = []

        start_equity = self._resolve_start_equity()

        self.data = {
            "trades": 0,
            "tp": 0,
            "sl": 0,
            "start_equity": float(start_equity),
            "current_equity": float(start_equity),
            "pnl_netto": 0.0,
            "pnl_tp": 0.0,
            "pnl_sl": 0.0,
            "cancels": 0,
            "attempts": 0,
            "attempts_submitted": 0,
            "attempts_filled": 0,
            "attempts_cancelled": 0,
            "attempts_timeout": 0,
            "attempts_blocked": 0,
            "attempts_skipped": 0,
            "attempts_observed": 0,
            "attempts_replanned": 0,
            "attempts_withheld": 0,
            "attempts_long": 0,
            "attempts_short": 0,
            "attempts_submitted_long": 0,
            "attempts_submitted_short": 0,
            "attempts_filled_long": 0,
            "attempts_filled_short": 0,
            "attempt_structure_zone": 0,
            "attempt_non_structure_zone": 0,
            "long_trades": 0,
            "short_trades": 0,
            "long_tp": 0,
            "long_sl": 0,
            "short_tp": 0,
            "short_sl": 0,
            "long_pnl": 0.0,
            "short_pnl": 0.0,
            "current_timestamp": None,
            "backtest_filepath": "",
            "backtest_processed_windows": 0,
            "backtest_total_windows": 0,
            "backtest_progress": 0.0,
            "backtest_complete": False,
            "backtest_stop_reason": "-",
            "last_outcome_decomposition": {},
            "recent_attempts": [],
            "pending_observations": [],
            "observation_learning": {
                "open": 0,
                "resolved": 0,
                "saved_loss": 0,
                "missed_gain": 0,
                "neutral": 0,
                "low_observations": 0,
                "zone_observations": 0,
                "maturity_trust": 0.0,
                "action_pressure": 0.0,
                "last_result": "-",
            },
            "entry_contact_learning": {
                "styles": {},
                "last_key": "-",
                "last_state": "-",
                "dominant_key": "-",
                "dominant_trust": 0.0,
            },
            "recent_observation_learning": [],
            "exploration_trades": 0,
            "exploration_tp": 0,
            "exploration_sl": 0,
            "exploration_cancels": 0,
            "exploration_pnl": 0.0,
            "matured_exits": 0,
            "matured_exit_pnl": 0.0,
            "exit_candidate_replay_count": 0,
            "exit_candidate_replay_actual_pnl": 0.0,
            "exit_candidate_replay_hypothetical_pnl": 0.0,
            "exit_candidate_replay_delta_pnl": 0.0,
            "exit_candidate_replay_saved_loss_count": 0,
            "exit_candidate_replay_saved_giveback_count": 0,
            "exit_candidate_replay_harmed_count": 0,
            "exit_candidate_replay_tp_cut_count": 0,
            "equity_peak": float(start_equity),
            "max_drawdown_abs": 0.0,
            "max_drawdown_pct": 0.0,
            "sensory_balance": {},
            "kpi_summary": {},
        }
        self._json_save_seq = 0

        if reset:
            # JSON zurücksetzen
            self._save(force=True)

            # CSV bei Neustart überschreiben
            if os.path.exists(self.csv_path):
                try:
                    os.remove(self.csv_path)
                except Exception:
                    pass

            if os.path.exists(self.attempt_path):
                try:
                    os.remove(self.attempt_path)
                except Exception:
                    pass

            if os.path.exists(self.outcome_path):
                try:
                    os.remove(self.outcome_path)
                except Exception:
                    pass
        else:
            self._load()
    # ─────────────────────────────────────────────
    
    def _load(self):
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                obj = json.load(f)
            if isinstance(obj, dict):
                self.data.update(obj)
                self.data.pop("attempt_records", None)
                self.data.pop("outcome_records", None)
        except Exception:
            pass
    # ─────────────────────────────────────────────
    def _normalize_record_value(self, value):
        if isinstance(value, dict):
            normalized = {}
            for key, item in value.items():
                if key is None:
                    continue
                normalized[str(key)] = self._normalize_record_value(item)
            return normalized

        if isinstance(value, list):
            return [self._normalize_record_value(item) for item in list(value or [])[:128]]

        if value is None or isinstance(value, (str, int, float, bool)):
            return value

        return str(value)

    # ─────────────────────────────────────────────
    def _append_record_file(self, path: str, record: dict):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            resolved_path = dbr_resolve_path(path)
            if resolved_path == self.outcome_path:
                self._remember_outcome_record(record)
            line = json.dumps(dict(record or {}), ensure_ascii=False) + "\n"
            dbr_append_text(
                path,
                line,
                operation="trade_stats_jsonl_append",
                extra=f"event={str((record or {}).get('event', '-'))}|status={str((record or {}).get('status', '-'))}",
            )
        except Exception:
            pass

    # ─────────────────────────────────────────────
    def _read_record_file(self, path: str, limit: int | None = None) -> list[dict]:
        records = []

        try:
            resolved_path = dbr_resolve_path(path)
            cache = list(getattr(self, "_outcome_records_cache", []) or [])
            if resolved_path == self.outcome_path and cache:
                records = [dict(item or {}) for item in cache if isinstance(item, dict)]
                if limit is not None:
                    return records[-max(1, int(limit or 1)):]
                return records

            if not os.path.exists(resolved_path):
                return records

            with open(resolved_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = str(line or "").strip()
                    if not line:
                        continue

                    try:
                        item = json.loads(line)
                    except Exception:
                        continue

                    if isinstance(item, dict):
                        records.append(item)
        except Exception:
            return []

        if limit is not None:
            return records[-max(1, int(limit or 1)):]

        return records

    # ─────────────────────────────────────────────
    def _structure_band(self, structure_quality: float) -> str:
        quality = float(structure_quality or 0.0)

        if quality >= 0.70:
            return "high"

        if quality >= 0.55:
            return "mid"

        return "low"

    # ─────────────────────────────────────────────
    def _derive_open_hypothesis_learning(self, record: dict, emergent_state: str | None = None) -> dict:
        return derive_open_hypothesis_learning(record, emergent_state=emergent_state)

    def _update_entry_contact_learning(
        self,
        *,
        side: str,
        reason: str,
        pnl: float = 0.0,
        trade_plan_state: dict = None,
        outcome_decomposition: dict = None,
    ) -> dict:
        def _f(value, default=0.0):
            try:
                if value is None:
                    return float(default)
                value = float(value)
                if value != value:
                    return float(default)
                return value
            except Exception:
                return float(default)

        def _clip(value):
            return max(0.0, min(1.0, _f(value)))

        def _feature_vector() -> dict:
            features = {
                "area_bearing_quality": trade_plan_state.get("area_bearing_quality", 0.0),
                "area_contact_timing_fit": trade_plan_state.get("area_contact_timing_fit", 0.0),
                "area_spacetime_fit": trade_plan_state.get("area_spacetime_fit", 0.0),
                "area_present_contact": trade_plan_state.get("area_present_contact", 0.0),
                "area_invalidity_pressure": trade_plan_state.get("area_invalidity_pressure", 0.0),
                "area_afterimage": trade_plan_state.get("area_afterimage", 0.0),
                "area_contact_distance_fit": trade_plan_state.get("area_contact_distance_fit", 0.0),
                "contact_entry_fit": trade_plan_state.get("contact_entry_fit", trade_plan_state.get("strategic_entry_fit", 0.0)),
                "entry_contact_bearing": trade_plan_state.get("entry_contact_bearing", 0.0),
                "area_contact_readiness": trade_plan_state.get("area_contact_readiness", 0.0),
                "receptive_contact_maturity": trade_plan_state.get("receptive_contact_maturity", 0.0),
                "receptive_contact_immaturity_pressure": trade_plan_state.get("receptive_contact_immaturity_pressure", 0.0),
                "visual_reality_bearing": trade_plan_state.get("visual_reality_bearing", 0.0),
                "real_area_contact_bearing": trade_plan_state.get("real_area_contact_bearing", 0.0),
                "felt_reality_bearing": trade_plan_state.get("felt_reality_bearing", 0.0),
                "form_mcm_reality_fit": trade_plan_state.get("form_mcm_reality_fit", 0.0),
                "energy_coherence_bearing": trade_plan_state.get("energy_coherence_bearing", 0.0),
                "structure_quality": outcome_decomposition.get("structure_quality", 0.0),
                "process_quality": outcome_decomposition.get("process_quality", 0.0),
                "position_consequence_burden": outcome_decomposition.get("position_consequence_burden", 0.0),
                "position_constructive_bearing": outcome_decomposition.get("position_constructive_bearing", 0.0),
            }
            return {key: float(_clip(value)) for key, value in features.items()}

        def _similarity(left: dict, right: dict) -> float:
            keys = [key for key in left.keys() if key in right]
            if not keys:
                return 0.0
            distance = sum(abs(_clip(left.get(key, 0.0)) - _clip(right.get(key, 0.0))) for key in keys) / max(1, len(keys))
            return _clip(1.0 - distance)

        side = str(side or "").upper().strip()
        if side not in ("LONG", "SHORT"):
            side = "-"
        reason = str(reason or "").strip().lower()
        trade_plan_state = dict(trade_plan_state or {})
        outcome_decomposition = dict(outcome_decomposition or {})

        location = str(
            trade_plan_state.get(
                "area_contact_location",
                trade_plan_state.get("strategic_entry_location", trade_plan_state.get("entry_contact_state", "-")),
            )
            or "-"
        ).strip() or "-"
        if location == "-":
            return {}

        key = f"{side}|{location}"
        learning = dict(self.data.get("entry_contact_learning", {}) or {})
        styles = dict(learning.get("styles", {}) or {})
        property_profiles = list(learning.get("property_profiles", []) or [])
        item = dict(styles.get(key, {}) or {})

        count = max(0, int(item.get("count", 0) or 0)) + 1
        tp_count = max(0, int(item.get("tp", 0) or 0))
        sl_count = max(0, int(item.get("sl", 0) or 0))
        cancel_count = max(0, int(item.get("cancel", 0) or 0))
        if reason == "tp_hit" or (reason == "matured_exit" and _f(pnl) >= 0.0):
            tp_count += 1
        elif reason == "sl_hit" or (reason == "matured_exit" and _f(pnl) < 0.0):
            sl_count += 1
        elif reason == "cancel":
            cancel_count += 1

        plan_quality = _clip(outcome_decomposition.get("plan_quality", 0.0))
        execution_quality = _clip(outcome_decomposition.get("execution_quality", 0.0))
        risk_fit_quality = _clip(outcome_decomposition.get("risk_fit_quality", 0.0))
        constructive_bearing = _clip(outcome_decomposition.get("position_constructive_bearing", 0.0))
        consequence_burden = _clip(outcome_decomposition.get("position_consequence_burden", 0.0))
        process_quality = _clip(
            (plan_quality * 0.28)
            + (execution_quality * 0.24)
            + (risk_fit_quality * 0.18)
            + (constructive_bearing * 0.30)
        )

        success_signal = 1.0 if reason == "tp_hit" or (reason == "matured_exit" and _f(pnl) >= 0.0) else 0.0
        burden_signal = 1.0 if reason == "sl_hit" or (reason == "matured_exit" and _f(pnl) < 0.0) else 0.0
        if reason == "cancel":
            burden_signal = max(burden_signal, 0.24 + consequence_burden * 0.28)

        old_trust = _clip(item.get("trust", 0.0))
        old_caution = _clip(item.get("caution", 0.0))
        old_maturity = _clip(item.get("maturity", 0.0))
        old_utility = _clip(item.get("utility", 0.0))

        trust_target = _clip((success_signal * 0.52) + (process_quality * 0.38) + (constructive_bearing * 0.10))
        caution_target = _clip((burden_signal * 0.58) + (consequence_burden * 0.32) + ((1.0 - process_quality) * 0.10))
        utility_target = _clip((success_signal * 0.42) + (constructive_bearing * 0.34) + (process_quality * 0.24) - (consequence_burden * 0.20))
        maturity_target = _clip(
            min(1.0, count / 18.0) * 0.38
            + max(success_signal, burden_signal) * 0.16
            + process_quality * 0.26
            + abs(trust_target - caution_target) * 0.20
        )

        alpha = max(0.08, min(0.22, 1.0 / max(2.0, count * 0.65)))
        trust = _clip((old_trust * (1.0 - alpha)) + (trust_target * alpha))
        caution = _clip((old_caution * (1.0 - alpha)) + (caution_target * alpha))
        maturity = _clip((old_maturity * (1.0 - alpha)) + (maturity_target * alpha))
        utility = _clip((old_utility * (1.0 - alpha)) + (utility_target * alpha))

        if trust >= caution + 0.10 and maturity >= 0.24:
            state = "contact_preference_carried"
        elif caution >= trust + 0.10:
            state = "contact_preference_careful"
        elif maturity >= 0.18:
            state = "contact_preference_forming"
        else:
            state = "contact_preference_open"

        item.update(
            {
                "key": key,
                "side": side,
                "location": location,
                "count": int(count),
                "tp": int(tp_count),
                "sl": int(sl_count),
                "cancel": int(cancel_count),
                "pnl_sum": _f(item.get("pnl_sum", 0.0)) + _f(pnl),
                "trust": float(trust),
                "caution": float(caution),
                "maturity": float(maturity),
                "utility": float(utility),
                "last_reason": reason,
                "last_pnl": float(_f(pnl)),
                "last_state": state,
                "last_process_quality": float(process_quality),
            }
        )
        styles[key] = item

        feature_vector = _feature_vector()
        matching_profiles = [
            dict(profile)
            for profile in property_profiles
            if isinstance(profile, dict) and str(profile.get("side", "-") or "-").upper().strip() in (side, "-")
        ]
        best_profile = {}
        best_similarity = 0.0
        for profile in matching_profiles:
            similarity = _similarity(feature_vector, dict(profile.get("features", {}) or {}))
            if similarity > best_similarity:
                best_similarity = float(similarity)
                best_profile = dict(profile)

        profile_count = max(0, int(best_profile.get("count", 0) or 0))
        if best_profile and best_similarity >= 0.64:
            profile = dict(best_profile)
            profile_id = str(profile.get("profile_id", "") or "")
        else:
            profile_id = f"ecp_{side.lower()}_{len(property_profiles) + 1:03d}"
            profile = {"profile_id": profile_id, "side": side, "features": dict(feature_vector)}
            profile_count = 0

        profile_count += 1
        profile_alpha = max(0.06, min(0.20, 1.0 / max(2.0, profile_count * 0.72)))
        previous_features = dict(profile.get("features", {}) or {})
        merged_features = {}
        for feature_key in sorted(set(previous_features.keys()) | set(feature_vector.keys())):
            merged_features[feature_key] = _clip(
                (_clip(previous_features.get(feature_key, feature_vector.get(feature_key, 0.0))) * (1.0 - profile_alpha))
                + (_clip(feature_vector.get(feature_key, previous_features.get(feature_key, 0.0))) * profile_alpha)
            )

        profile_tp = max(0, int(profile.get("tp", 0) or 0)) + (1 if success_signal > 0.0 else 0)
        profile_sl = max(0, int(profile.get("sl", 0) or 0)) + (1 if burden_signal >= 1.0 else 0)
        profile_cancel = max(0, int(profile.get("cancel", 0) or 0)) + (1 if reason == "cancel" else 0)
        profile_trust = _clip((_clip(profile.get("trust", 0.0)) * (1.0 - profile_alpha)) + (trust_target * profile_alpha))
        profile_caution = _clip((_clip(profile.get("caution", 0.0)) * (1.0 - profile_alpha)) + (caution_target * profile_alpha))
        profile_utility = _clip((_clip(profile.get("utility", 0.0)) * (1.0 - profile_alpha)) + (utility_target * profile_alpha))
        profile_maturity = _clip((_clip(profile.get("maturity", 0.0)) * (1.0 - profile_alpha)) + (maturity_target * profile_alpha))
        if profile_trust >= profile_caution + 0.10 and profile_maturity >= 0.24:
            profile_state = "property_profile_carried"
        elif profile_caution >= profile_trust + 0.10:
            profile_state = "property_profile_careful"
        elif profile_maturity >= 0.18:
            profile_state = "property_profile_forming"
        else:
            profile_state = "property_profile_open"
        profile.update(
            {
                "profile_id": profile_id,
                "side": side,
                "count": int(profile_count),
                "tp": int(profile_tp),
                "sl": int(profile_sl),
                "cancel": int(profile_cancel),
                "pnl_sum": _f(profile.get("pnl_sum", 0.0)) + _f(pnl),
                "features": dict(merged_features),
                "last_similarity": float(best_similarity),
                "trust": float(profile_trust),
                "caution": float(profile_caution),
                "maturity": float(profile_maturity),
                "utility": float(profile_utility),
                "last_reason": reason,
                "last_pnl": float(_f(pnl)),
                "last_state": profile_state,
            }
        )
        property_by_id = {
            str(existing.get("profile_id", "") or ""): dict(existing)
            for existing in property_profiles
            if isinstance(existing, dict) and str(existing.get("profile_id", "") or "")
        }
        property_by_id[profile_id] = profile
        ranked_property_profiles = sorted(
            property_by_id.values(),
            key=lambda value: (
                float(value.get("maturity", 0.0) or 0.0)
                + float(value.get("trust", 0.0) or 0.0)
                + float(value.get("utility", 0.0) or 0.0)
                - float(value.get("caution", 0.0) or 0.0)
            ),
            reverse=True,
        )[:80]

        ranked = sorted(
            styles.values(),
            key=lambda value: (
                float(value.get("maturity", 0.0) or 0.0)
                + float(value.get("trust", 0.0) or 0.0)
                + float(value.get("utility", 0.0) or 0.0)
                - float(value.get("caution", 0.0) or 0.0)
            ),
            reverse=True,
        )
        trimmed_styles = {str(value.get("key", "-") or "-"): dict(value) for value in ranked[:80] if isinstance(value, dict)}
        dominant = dict(ranked[0] if ranked else {})
        learning = {
            "styles": trimmed_styles,
            "property_profiles": [dict(profile) for profile in ranked_property_profiles],
            "last_key": key,
            "last_state": state,
            "last_property_profile_id": str(profile.get("profile_id", "-") or "-"),
            "last_property_profile_state": str(profile.get("last_state", "-") or "-"),
            "last_property_similarity": float(best_similarity),
            "dominant_key": str(dominant.get("key", "-") or "-"),
            "dominant_trust": float(dominant.get("trust", 0.0) or 0.0),
            "dominant_property_profile_id": str((ranked_property_profiles[0] if ranked_property_profiles else {}).get("profile_id", "-") or "-"),
            "dominant_property_trust": float((ranked_property_profiles[0] if ranked_property_profiles else {}).get("trust", 0.0) or 0.0),
        }
        self.data["entry_contact_learning"] = learning
        feedback = dict(item)
        feedback.update(
            {
                "property_profile_id": str(profile.get("profile_id", "-") or "-"),
                "property_profile_state": str(profile.get("last_state", "-") or "-"),
                "property_profile_similarity": float(best_similarity),
                "property_profile_trust": float(profile.get("trust", 0.0) or 0.0),
                "property_profile_caution": float(profile.get("caution", 0.0) or 0.0),
                "property_profile_maturity": float(profile.get("maturity", 0.0) or 0.0),
                "property_profile_utility": float(profile.get("utility", 0.0) or 0.0),
            }
        )
        return feedback

    def _rebuild_kpi_summary(self):
        trades = int(self.data.get("trades", 0) or 0)
        tp = int(self.data.get("tp", 0) or 0)
        sl = int(self.data.get("sl", 0) or 0)
        cancels = int(self.data.get("cancels", 0) or 0)
        attempts = int(self.data.get("attempts", 0) or 0)

        pnl_netto = float(self.data.get("pnl_netto", 0.0) or 0.0)
        pnl_tp = float(self.data.get("pnl_tp", 0.0) or 0.0)
        pnl_sl = float(self.data.get("pnl_sl", 0.0) or 0.0)

        avg_win = (pnl_tp / tp) if tp > 0 else 0.0
        avg_loss = (pnl_sl / sl) if sl > 0 else 0.0
        profit_factor = abs(pnl_tp / pnl_sl) if pnl_sl != 0 else 0.0
        expectancy = (pnl_netto / trades) if trades > 0 else 0.0
        winrate = (tp / trades) if trades > 0 else 0.0
        long_trades = int(self.data.get("long_trades", 0) or 0)
        short_trades = int(self.data.get("short_trades", 0) or 0)
        long_tp = int(self.data.get("long_tp", 0) or 0)
        long_sl = int(self.data.get("long_sl", 0) or 0)
        short_tp = int(self.data.get("short_tp", 0) or 0)
        short_sl = int(self.data.get("short_sl", 0) or 0)
        long_pnl = float(self.data.get("long_pnl", 0.0) or 0.0)
        short_pnl = float(self.data.get("short_pnl", 0.0) or 0.0)

        attempt_feedback = self.get_attempt_feedback()

        outcomes = self._read_record_file(self.outcome_path)

        band_stats = {
            "high": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0},
            "mid": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0},
            "low": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0},
        }
        emergent_structure_stats = {
            "confirmed_structure_contact": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "reading_sum": 0.0, "confirmation_sum": 0.0, "rr_sum": 0.0},
            "open_structure_contact": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "reading_sum": 0.0, "confirmation_sum": 0.0, "rr_sum": 0.0},
            "wide_range_without_structure": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "reading_sum": 0.0, "confirmation_sum": 0.0, "rr_sum": 0.0},
            "ordinary_structure_contact": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "reading_sum": 0.0, "confirmation_sum": 0.0, "rr_sum": 0.0},
        }
        open_hypothesis_learning_stats = {
            "open_hypothesis_carried": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "consequence_sum": 0.0, "burden_sum": 0.0, "reorganization_sum": 0.0, "replay_sum": 0.0, "distance_sum": 0.0, "reinterpretation_sum": 0.0, "grounding_sum": 0.0, "pressure_sum": 0.0, "lag_sum": 0.0},
            "open_hypothesis_burdened": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "consequence_sum": 0.0, "burden_sum": 0.0, "reorganization_sum": 0.0, "replay_sum": 0.0, "distance_sum": 0.0, "reinterpretation_sum": 0.0, "grounding_sum": 0.0, "pressure_sum": 0.0, "lag_sum": 0.0},
            "open_hypothesis_reorganizing": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "consequence_sum": 0.0, "burden_sum": 0.0, "reorganization_sum": 0.0, "replay_sum": 0.0, "distance_sum": 0.0, "reinterpretation_sum": 0.0, "grounding_sum": 0.0, "pressure_sum": 0.0, "lag_sum": 0.0},
        }
        open_hypothesis_reorganization_posture_stats = {
            "reinterpretation_dominant": {"count": 0, "pnl": 0.0},
            "distance_dominant": {"count": 0, "pnl": 0.0},
            "replay_dominant": {"count": 0, "pnl": 0.0},
            "low_reorganization_need": {"count": 0, "pnl": 0.0},
        }

        def _summary_f(*values, default=0.0):
            for value in values:
                try:
                    if value is None:
                        continue
                    return float(value)
                except Exception:
                    continue
            if default is None:
                return None
            return float(default)

        def _summary_clip(value):
            value = _summary_f(value)
            if value != value:
                value = 0.0
            return max(0.0, min(1.0, float(value)))

        def _summary_section(record: dict, name: str) -> dict:
            context = dict(record.get("context", {}) or {})
            value = record.get(name, context.get(name, {}))
            return dict(value or {}) if isinstance(value, dict) else {}

        def _normalize_emergent_structure_state(state: str) -> str:
            state = str(state or "").strip()
            aliases = {
                "confirmed_structural_interpretation": "confirmed_structure_contact",
                "open_structural_hypothesis": "open_structure_contact",
                "wide_target_without_structure": "wide_range_without_structure",
                "ordinary_structure_reading": "ordinary_structure_contact",
            }
            return aliases.get(state, state) if state else ""

        def _derive_emergent_structure(record: dict) -> dict:
            plan = _summary_section(record, "trade_plan")
            meta = _summary_section(record, "meta_regulation_state")
            contact = _summary_section(record, "active_mcm_contact_state")
            target = _summary_section(record, "target_expectation_state")
            decomposition = dict(record.get("outcome_decomposition", {}) or {})
            if not contact:
                contact = dict(meta.get("active_mcm_contact", {}) or {})

            rr_value = _summary_f(record.get("rr_value"), plan.get("rr_value"), default=0.0)
            structural_run_room = _summary_f(record.get("structural_run_room"), _summary_clip((rr_value - 1.6) / 3.2))
            target_expectation_value = _summary_f(
                record.get("target_expectation_value"),
                target.get(
                    "tp_reachability",
                    target.get(
                        "base_target_expectation",
                        (_summary_section(record, "experience") or {}).get("target_expectation", 0.0),
                    ),
                ),
            )
            reading = _summary_f(record.get("emergent_structure_reading"), default=None)
            if reading is None:
                reading = _summary_clip(
                    (_summary_clip(structural_run_room) * 0.24)
                    + (_summary_clip(meta.get("future_projection_depth", record.get("future_projection_depth", 0.0))) * 0.16)
                    + (_summary_clip(meta.get("mcm_spacetime_depth", record.get("mcm_spacetime_depth", 0.0))) * 0.14)
                    + (_summary_clip(meta.get("area_bearing_quality", record.get("area_bearing_quality", 0.0))) * 0.14)
                    + (_summary_clip(plan.get("entry_contact_bearing", plan.get("entry_choice_bearing", record.get("entry_choice_bearing", 0.0)))) * 0.12)
                    + (_summary_clip(contact.get("contact_action_maturity", meta.get("contact_action_maturity", 0.0))) * 0.10)
                    + (_summary_clip(target_expectation_value) * 0.10)
                    - (_summary_clip(meta.get("spacetime_unlocated_pressure", record.get("spacetime_unlocated_pressure", 0.0))) * 0.10)
                    - (_summary_clip(meta.get("contact_regime_mismatch", record.get("contact_regime_mismatch", 0.0))) * 0.08)
                )
            confirmation = _summary_f(record.get("emergent_structure_confirmation"), default=None)
            reason = str(record.get("reason", "") or "").strip().lower()
            if confirmation is None:
                confirmation = _summary_clip(
                    (_summary_clip(reading) * 0.42)
                    + (_summary_clip(decomposition.get("plan_quality", 0.0)) * 0.16)
                    + (_summary_clip(decomposition.get("execution_quality", 0.0)) * 0.14)
                    + (_summary_clip(decomposition.get("risk_fit_quality", 0.0)) * 0.12)
                    + (_summary_clip(decomposition.get("position_constructive_bearing", 0.0)) * 0.10)
                    + (0.12 if reason == "tp_hit" and rr_value >= 2.4 else 0.0)
                    - (0.10 if reason == "sl_hit" and rr_value >= 2.4 else 0.0)
                )
            state = _normalize_emergent_structure_state(record.get("emergent_structure_state", ""))
            if not state:
                if reading >= 0.52 and confirmation >= 0.50:
                    state = "confirmed_structure_contact"
                elif reading >= 0.44 and rr_value >= 2.4:
                    state = "open_structure_contact"
                elif rr_value >= 2.4 and reading < 0.34:
                    state = "wide_range_without_structure"
                else:
                    state = "ordinary_structure_contact"
            return {
                "state": state,
                "rr_value": float(rr_value),
                "structural_run_room": float(structural_run_room),
                "target_expectation_value": float(target_expectation_value),
                "reading": float(reading),
                "confirmation": float(confirmation),
            }

        for item in outcomes:
            record = dict(item or {})
            band = self._structure_band(record.get("structure_quality", 0.0))
            reason = str(record.get("reason", "") or "").strip().lower()
            emergent = _derive_emergent_structure(record)
            emergent_state = _normalize_emergent_structure_state(emergent.get("state", "ordinary_structure_contact"))
            if emergent_state not in emergent_structure_stats:
                emergent_structure_stats[emergent_state] = {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "reading_sum": 0.0, "confirmation_sum": 0.0, "rr_sum": 0.0}

            band_stats[band]["count"] += 1
            band_stats[band]["pnl"] += float(record.get("pnl", 0.0) or 0.0)
            emergent_structure_stats[emergent_state]["count"] += 1
            emergent_structure_stats[emergent_state]["pnl"] += float(record.get("pnl", 0.0) or 0.0)
            emergent_structure_stats[emergent_state]["reading_sum"] += float(emergent.get("reading", 0.0) or 0.0)
            emergent_structure_stats[emergent_state]["confirmation_sum"] += float(emergent.get("confirmation", 0.0) or 0.0)
            emergent_structure_stats[emergent_state]["rr_sum"] += float(emergent.get("rr_value", 0.0) or 0.0)
            open_learning = self._derive_open_hypothesis_learning(record, emergent_state=emergent_state)
            open_learning_state = str(open_learning.get("open_hypothesis_learning_state", "-") or "-")
            if open_learning_state in open_hypothesis_learning_stats:
                open_hypothesis_learning_stats[open_learning_state]["count"] += 1
                open_hypothesis_learning_stats[open_learning_state]["pnl"] += float(record.get("pnl", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["consequence_sum"] += float(open_learning.get("open_hypothesis_consequence_score", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["burden_sum"] += float(open_learning.get("open_hypothesis_burden_score", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["reorganization_sum"] += float(open_learning.get("open_hypothesis_reorganization_score", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["replay_sum"] += float(open_learning.get("open_hypothesis_replay_need", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["distance_sum"] += float(open_learning.get("open_hypothesis_distance_need", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["reinterpretation_sum"] += float(open_learning.get("open_hypothesis_reinterpretation_need", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["grounding_sum"] += float(record.get("thought_seed_structural_grounding", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["pressure_sum"] += float(record.get("thought_seed_open_hypothesis_pressure", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["lag_sum"] += float(record.get("thought_seed_reality_lag", 0.0) or 0.0)
                posture = str(open_learning.get("open_hypothesis_reorganization_posture", "-") or "-")
                if posture in open_hypothesis_reorganization_posture_stats:
                    open_hypothesis_reorganization_posture_stats[posture]["count"] += 1
                    open_hypothesis_reorganization_posture_stats[posture]["pnl"] += float(record.get("pnl", 0.0) or 0.0)

            if reason == "tp_hit":
                band_stats[band]["tp"] += 1
                emergent_structure_stats[emergent_state]["tp"] += 1
                if open_learning_state in open_hypothesis_learning_stats:
                    open_hypothesis_learning_stats[open_learning_state]["tp"] += 1
            elif reason == "sl_hit":
                band_stats[band]["sl"] += 1
                emergent_structure_stats[emergent_state]["sl"] += 1
                if open_learning_state in open_hypothesis_learning_stats:
                    open_hypothesis_learning_stats[open_learning_state]["sl"] += 1
            else:
                band_stats[band]["cancel"] += 1
                emergent_structure_stats[emergent_state]["cancel"] += 1
                if open_learning_state in open_hypothesis_learning_stats:
                    open_hypothesis_learning_stats[open_learning_state]["cancel"] += 1

        for band_name, payload in band_stats.items():
            count = int(payload.get("count", 0) or 0)
            tp_count = int(payload.get("tp", 0) or 0)
            payload["winrate"] = float(tp_count / count) if count > 0 else 0.0
            payload["avg_pnl"] = float(payload.get("pnl", 0.0) or 0.0) / count if count > 0 else 0.0

        for state_name, payload in emergent_structure_stats.items():
            count = int(payload.get("count", 0) or 0)
            tp_count = int(payload.get("tp", 0) or 0)
            payload["winrate"] = float(tp_count / count) if count > 0 else 0.0
            payload["avg_pnl"] = float(payload.get("pnl", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_reading"] = float(payload.get("reading_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_confirmation"] = float(payload.get("confirmation_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_rr"] = float(payload.get("rr_sum", 0.0) or 0.0) / count if count > 0 else 0.0

        for state_name, payload in open_hypothesis_learning_stats.items():
            count = int(payload.get("count", 0) or 0)
            tp_count = int(payload.get("tp", 0) or 0)
            payload["winrate"] = float(tp_count / count) if count > 0 else 0.0
            payload["avg_pnl"] = float(payload.get("pnl", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_consequence_score"] = float(payload.get("consequence_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_burden_score"] = float(payload.get("burden_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_reorganization_score"] = float(payload.get("reorganization_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_replay_need"] = float(payload.get("replay_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_distance_need"] = float(payload.get("distance_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_reinterpretation_need"] = float(payload.get("reinterpretation_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_structural_grounding"] = float(payload.get("grounding_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_open_hypothesis_pressure"] = float(payload.get("pressure_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_reality_lag"] = float(payload.get("lag_sum", 0.0) or 0.0) / count if count > 0 else 0.0

        proof = {
            "attempt_density": float(attempt_feedback.get("attempt_density", 0.0) or 0.0),
            "context_quality": float(attempt_feedback.get("context_quality", 0.0) or 0.0),
            "overtrade_pressure": float(attempt_feedback.get("overtrade_pressure", 0.0) or 0.0),
            "observe_share": float(attempt_feedback.get("observe_share", 0.0) or 0.0),
            "replan_share": float(attempt_feedback.get("replan_share", 0.0) or 0.0),
            "withheld_share": float(attempt_feedback.get("withheld_share", 0.0) or 0.0),
            "pressure_to_capacity": float(attempt_feedback.get("pressure_to_capacity", 0.0) or 0.0),
            "regulatory_load": float(attempt_feedback.get("regulatory_load", 0.0) or 0.0),
            "action_capacity": float(attempt_feedback.get("action_capacity", 0.0) or 0.0),
            "recovery_need": float(attempt_feedback.get("recovery_need", 0.0) or 0.0),
            "survival_pressure": float(attempt_feedback.get("survival_pressure", 0.0) or 0.0),
            "pressure_release": float(attempt_feedback.get("pressure_release", 0.0) or 0.0),
            "load_bearing_capacity": float(attempt_feedback.get("load_bearing_capacity", 0.0) or 0.0),
            "state_stability": float(attempt_feedback.get("state_stability", 0.0) or 0.0),
            "capacity_reserve": float(attempt_feedback.get("capacity_reserve", 0.0) or 0.0),
            "recovery_balance": float(attempt_feedback.get("recovery_balance", 0.0) or 0.0),
            "regulated_courage": float(attempt_feedback.get("regulated_courage", 0.0) or 0.0),
            "courage_gap": float(attempt_feedback.get("courage_gap", 0.0) or 0.0),
            "action_inhibition": float(attempt_feedback.get("action_inhibition", 0.0) or 0.0),
            "action_clearance": float(attempt_feedback.get("action_clearance", 0.0) or 0.0),
            "regulation_before_action": float(attempt_feedback.get("regulation_before_action", 0.0) or 0.0),
            "observation_learning_open": int(attempt_feedback.get("observation_learning_open", 0) or 0),
            "observation_learning_resolved": int(attempt_feedback.get("observation_learning_resolved", 0) or 0),
            "observation_saved_loss": int(attempt_feedback.get("observation_saved_loss", 0) or 0),
            "observation_missed_gain": int(attempt_feedback.get("observation_missed_gain", 0) or 0),
            "observation_neutral": int(attempt_feedback.get("observation_neutral", 0) or 0),
            "observation_low_count": int(attempt_feedback.get("observation_low_count", 0) or 0),
            "observation_maturity_trust": float(attempt_feedback.get("observation_maturity_trust", 0.0) or 0.0),
            "observation_action_pressure": float(attempt_feedback.get("observation_action_pressure", 0.0) or 0.0),
            "hypothesis_observed_outcome": str(attempt_feedback.get("hypothesis_observed_outcome", "hypothesis_observed_open") or "hypothesis_observed_open"),
            "hypothesis_confirmation_without_action": float(attempt_feedback.get("hypothesis_confirmation_without_action", 0.0) or 0.0),
            "hypothesis_rejection_without_action": float(attempt_feedback.get("hypothesis_rejection_without_action", 0.0) or 0.0),
            "hypothesis_neutral_without_action": float(attempt_feedback.get("hypothesis_neutral_without_action", 0.0) or 0.0),
            "hypothesis_observation_maturity": float(attempt_feedback.get("hypothesis_observation_maturity", 0.0) or 0.0),
            "possibility_maturity": float(attempt_feedback.get("possibility_maturity", 0.0) or 0.0),
            "possibility_caution": float(attempt_feedback.get("possibility_caution", 0.0) or 0.0),
            "hypothesis_trust_score": float(attempt_feedback.get("hypothesis_trust_score", 0.0) or 0.0),
            "hypothesis_trust_priority": float(attempt_feedback.get("hypothesis_trust_priority", 0.0) or 0.0),
            "hypothesis_frustration_risk": float(attempt_feedback.get("hypothesis_frustration_risk", 0.0) or 0.0),
            "hypothesis_distance_risk": float(attempt_feedback.get("hypothesis_distance_risk", 0.0) or 0.0),
            "hypothesis_trust_state": str(attempt_feedback.get("hypothesis_trust_state", "hypothesis_trust_unformed") or "hypothesis_trust_unformed"),
            "dominant_hypothesis_trust_key": str(attempt_feedback.get("dominant_hypothesis_trust_key", "-") or "-"),
            "dominant_hypothesis_trust_score": float(attempt_feedback.get("dominant_hypothesis_trust_score", 0.0) or 0.0),
            "dominant_hypothesis_action_readiness": float(attempt_feedback.get("dominant_hypothesis_action_readiness", 0.0) or 0.0),
            "dominant_hypothesis_trust_evidence": int(attempt_feedback.get("dominant_hypothesis_trust_evidence", 0) or 0),
            "dominant_possibility_variant_key": str(attempt_feedback.get("dominant_possibility_variant_key", "-") or "-"),
            "dominant_possibility_variant_trust": float(attempt_feedback.get("dominant_possibility_variant_trust", 0.0) or 0.0),
            "dominant_possibility_variant_caution": float(attempt_feedback.get("dominant_possibility_variant_caution", 0.0) or 0.0),
            "dominant_possibility_variant_maturity": float(attempt_feedback.get("dominant_possibility_variant_maturity", 0.0) or 0.0),
            "dominant_possibility_variant_evidence": int(attempt_feedback.get("dominant_possibility_variant_evidence", 0) or 0),
            "hypothesis_trust_family_count": int(attempt_feedback.get("hypothesis_trust_family_count", 0) or 0),
            "declined_hypothesis_resolved": int(attempt_feedback.get("declined_hypothesis_resolved", 0) or 0),
            "declined_hypothesis_saved_loss": int(attempt_feedback.get("declined_hypothesis_saved_loss", 0) or 0),
            "declined_hypothesis_missed_gain": int(attempt_feedback.get("declined_hypothesis_missed_gain", 0) or 0),
            "declined_hypothesis_confirmation_without_action": float(attempt_feedback.get("declined_hypothesis_confirmation_without_action", 0.0) or 0.0),
            "declined_hypothesis_rejection_without_action": float(attempt_feedback.get("declined_hypothesis_rejection_without_action", 0.0) or 0.0),
            "declined_hypothesis_maturity": float(attempt_feedback.get("declined_hypothesis_maturity", 0.0) or 0.0),
            "declined_long_hypothesis_count": int(attempt_feedback.get("declined_long_hypothesis_count", 0) or 0),
            "declined_long_hypothesis_confirmation": float(attempt_feedback.get("declined_long_hypothesis_confirmation", 0.0) or 0.0),
            "declined_long_hypothesis_rejection": float(attempt_feedback.get("declined_long_hypothesis_rejection", 0.0) or 0.0),
            "declined_long_hypothesis_maturity": float(attempt_feedback.get("declined_long_hypothesis_maturity", 0.0) or 0.0),
            "declined_short_hypothesis_count": int(attempt_feedback.get("declined_short_hypothesis_count", 0) or 0),
            "declined_short_hypothesis_confirmation": float(attempt_feedback.get("declined_short_hypothesis_confirmation", 0.0) or 0.0),
            "declined_short_hypothesis_rejection": float(attempt_feedback.get("declined_short_hypothesis_rejection", 0.0) or 0.0),
            "declined_short_hypothesis_maturity": float(attempt_feedback.get("declined_short_hypothesis_maturity", 0.0) or 0.0),
            "attempt_fill_rate": float(self.data.get("attempts_filled", 0) or 0) / max(1, attempts),
            "attempt_zone_share": float(self.data.get("attempt_structure_zone", 0) or 0) / max(1, attempts),
            "attempts_per_trade": float(attempts / max(1, trades)),
            "long_trade_share": float(long_trades / max(1, trades)),
            "short_trade_share": float(short_trades / max(1, trades)),
            "long_attempt_share": float(self.data.get("attempts_long", 0) or 0) / max(1, attempts),
            "short_attempt_share": float(self.data.get("attempts_short", 0) or 0) / max(1, attempts),
            "max_drawdown_abs": float(self.data.get("max_drawdown_abs", 0.0) or 0.0),
            "max_drawdown_pct": float(self.data.get("max_drawdown_pct", 0.0) or 0.0),
            "winrate": float(winrate),
            "profit_factor": float(profit_factor),
            "expectancy": float(expectancy),
            "avg_win": float(avg_win),
            "avg_loss": float(avg_loss),
        }

        sensory_balance = self._derive_sensory_balance_summary(proof)
        self.data["sensory_balance"] = dict(sensory_balance)

        self.data["kpi_summary"] = {
            "proof": dict(proof),
            "sensory_balance": dict(sensory_balance),
            "state_core": {
                "state_stability": float(proof.get("state_stability", 0.0) or 0.0),
                "capacity_reserve": float(proof.get("capacity_reserve", 0.0) or 0.0),
                "recovery_balance": float(proof.get("recovery_balance", 0.0) or 0.0),
                "context_quality": float(proof.get("context_quality", 0.0) or 0.0),
                "overtrade_pressure": float(proof.get("overtrade_pressure", 0.0) or 0.0),
            },
            "regulation_core": {
                "regulatory_load": float(proof.get("regulatory_load", 0.0) or 0.0),
                "action_capacity": float(proof.get("action_capacity", 0.0) or 0.0),
                "recovery_need": float(proof.get("recovery_need", 0.0) or 0.0),
                "survival_pressure": float(proof.get("survival_pressure", 0.0) or 0.0),
                "pressure_release": float(proof.get("pressure_release", 0.0) or 0.0),
                "load_bearing_capacity": float(proof.get("load_bearing_capacity", 0.0) or 0.0),
                "pressure_to_capacity": float(proof.get("pressure_to_capacity", 0.0) or 0.0),
                "regulated_courage": float(proof.get("regulated_courage", 0.0) or 0.0),
                "courage_gap": float(proof.get("courage_gap", 0.0) or 0.0),
                "action_inhibition": float(proof.get("action_inhibition", 0.0) or 0.0),
                "action_clearance": float(proof.get("action_clearance", 0.0) or 0.0),
                "regulation_before_action": float(proof.get("regulation_before_action", 0.0) or 0.0),
            },
            "flow": {
                "attempt_density": float(proof.get("attempt_density", 0.0) or 0.0),
                "attempt_fill_rate": float(proof.get("attempt_fill_rate", 0.0) or 0.0),
                "attempt_zone_share": float(proof.get("attempt_zone_share", 0.0) or 0.0),
                "attempts_per_trade": float(proof.get("attempts_per_trade", 0.0) or 0.0),
                "observe_share": float(proof.get("observe_share", 0.0) or 0.0),
                "replan_share": float(proof.get("replan_share", 0.0) or 0.0),
                "withheld_share": float(proof.get("withheld_share", 0.0) or 0.0),
            },
            "observation_learning": {
                "open": int(proof.get("observation_learning_open", 0) or 0),
                "resolved": int(proof.get("observation_learning_resolved", 0) or 0),
                "saved_loss": int(proof.get("observation_saved_loss", 0) or 0),
                "missed_gain": int(proof.get("observation_missed_gain", 0) or 0),
                "neutral": int(proof.get("observation_neutral", 0) or 0),
                "low_observations": int(proof.get("observation_low_count", 0) or 0),
                "maturity_trust": float(proof.get("observation_maturity_trust", 0.0) or 0.0),
                "action_pressure": float(proof.get("observation_action_pressure", 0.0) or 0.0),
                "hypothesis_observed_outcome": str(proof.get("hypothesis_observed_outcome", "hypothesis_observed_open") or "hypothesis_observed_open"),
                "hypothesis_confirmation_without_action": float(proof.get("hypothesis_confirmation_without_action", 0.0) or 0.0),
                "hypothesis_rejection_without_action": float(proof.get("hypothesis_rejection_without_action", 0.0) or 0.0),
                "hypothesis_neutral_without_action": float(proof.get("hypothesis_neutral_without_action", 0.0) or 0.0),
                "hypothesis_observation_maturity": float(proof.get("hypothesis_observation_maturity", 0.0) or 0.0),
                "possibility_maturity": float(proof.get("possibility_maturity", 0.0) or 0.0),
                "possibility_caution": float(proof.get("possibility_caution", 0.0) or 0.0),
                "hypothesis_trust_score": float(proof.get("hypothesis_trust_score", 0.0) or 0.0),
                "hypothesis_trust_priority": float(proof.get("hypothesis_trust_priority", 0.0) or 0.0),
                "hypothesis_frustration_risk": float(proof.get("hypothesis_frustration_risk", 0.0) or 0.0),
                "hypothesis_distance_risk": float(proof.get("hypothesis_distance_risk", 0.0) or 0.0),
                "hypothesis_trust_state": str(proof.get("hypothesis_trust_state", "hypothesis_trust_unformed") or "hypothesis_trust_unformed"),
                "dominant_hypothesis_trust_key": str(proof.get("dominant_hypothesis_trust_key", "-") or "-"),
                "dominant_hypothesis_trust_score": float(proof.get("dominant_hypothesis_trust_score", 0.0) or 0.0),
                "dominant_hypothesis_action_readiness": float(proof.get("dominant_hypothesis_action_readiness", 0.0) or 0.0),
                "dominant_hypothesis_trust_evidence": int(proof.get("dominant_hypothesis_trust_evidence", 0) or 0),
                "dominant_possibility_variant_key": str(proof.get("dominant_possibility_variant_key", "-") or "-"),
                "dominant_possibility_variant_trust": float(proof.get("dominant_possibility_variant_trust", 0.0) or 0.0),
                "dominant_possibility_variant_caution": float(proof.get("dominant_possibility_variant_caution", 0.0) or 0.0),
                "dominant_possibility_variant_maturity": float(proof.get("dominant_possibility_variant_maturity", 0.0) or 0.0),
                "dominant_possibility_variant_evidence": int(proof.get("dominant_possibility_variant_evidence", 0) or 0),
                "hypothesis_trust_family_count": int(proof.get("hypothesis_trust_family_count", 0) or 0),
                "declined_hypothesis_resolved": int(proof.get("declined_hypothesis_resolved", 0) or 0),
                "declined_hypothesis_saved_loss": int(proof.get("declined_hypothesis_saved_loss", 0) or 0),
                "declined_hypothesis_missed_gain": int(proof.get("declined_hypothesis_missed_gain", 0) or 0),
                "declined_hypothesis_confirmation_without_action": float(proof.get("declined_hypothesis_confirmation_without_action", 0.0) or 0.0),
                "declined_hypothesis_rejection_without_action": float(proof.get("declined_hypothesis_rejection_without_action", 0.0) or 0.0),
                "declined_hypothesis_maturity": float(proof.get("declined_hypothesis_maturity", 0.0) or 0.0),
                "declined_long_hypothesis_count": int(proof.get("declined_long_hypothesis_count", 0) or 0),
                "declined_long_hypothesis_confirmation": float(proof.get("declined_long_hypothesis_confirmation", 0.0) or 0.0),
                "declined_long_hypothesis_rejection": float(proof.get("declined_long_hypothesis_rejection", 0.0) or 0.0),
                "declined_long_hypothesis_maturity": float(proof.get("declined_long_hypothesis_maturity", 0.0) or 0.0),
                "declined_short_hypothesis_count": int(proof.get("declined_short_hypothesis_count", 0) or 0),
                "declined_short_hypothesis_confirmation": float(proof.get("declined_short_hypothesis_confirmation", 0.0) or 0.0),
                "declined_short_hypothesis_rejection": float(proof.get("declined_short_hypothesis_rejection", 0.0) or 0.0),
                "declined_short_hypothesis_maturity": float(proof.get("declined_short_hypothesis_maturity", 0.0) or 0.0),
            },
            "economics": {
                "winrate": float(proof.get("winrate", 0.0) or 0.0),
                "profit_factor": float(proof.get("profit_factor", 0.0) or 0.0),
                "expectancy": float(proof.get("expectancy", 0.0) or 0.0),
                "avg_win": float(proof.get("avg_win", 0.0) or 0.0),
                "avg_loss": float(proof.get("avg_loss", 0.0) or 0.0),
                "max_drawdown_abs": float(proof.get("max_drawdown_abs", 0.0) or 0.0),
                "max_drawdown_pct": float(proof.get("max_drawdown_pct", 0.0) or 0.0),
            },
            "direction_profile": {
                "long_trades": int(long_trades),
                "short_trades": int(short_trades),
                "long_tp": int(long_tp),
                "long_sl": int(long_sl),
                "short_tp": int(short_tp),
                "short_sl": int(short_sl),
                "long_pnl": float(long_pnl),
                "short_pnl": float(short_pnl),
                "long_winrate": float(long_tp / max(1, long_trades)),
                "short_winrate": float(short_tp / max(1, short_trades)),
                "long_trade_share": float(proof.get("long_trade_share", 0.0) or 0.0),
                "short_trade_share": float(proof.get("short_trade_share", 0.0) or 0.0),
                "attempts_long": int(self.data.get("attempts_long", 0) or 0),
                "attempts_short": int(self.data.get("attempts_short", 0) or 0),
                "attempts_submitted_long": int(self.data.get("attempts_submitted_long", 0) or 0),
                "attempts_submitted_short": int(self.data.get("attempts_submitted_short", 0) or 0),
                "attempts_filled_long": int(self.data.get("attempts_filled_long", 0) or 0),
                "attempts_filled_short": int(self.data.get("attempts_filled_short", 0) or 0),
                "long_attempt_share": float(proof.get("long_attempt_share", 0.0) or 0.0),
                "short_attempt_share": float(proof.get("short_attempt_share", 0.0) or 0.0),
            },
            "structure_bands": {
                "high": dict(band_stats["high"]),
                "mid": dict(band_stats["mid"]),
                "low": dict(band_stats["low"]),
            },
            "emergent_structure": {
                key: dict(value) for key, value in emergent_structure_stats.items()
            },
            "open_hypothesis_learning": {
                key: dict(value) for key, value in open_hypothesis_learning_stats.items()
            },
            "open_hypothesis_reorganization_posture": {
                key: dict(value) for key, value in open_hypothesis_reorganization_posture_stats.items()
            },
            "totals": {
                "trades": int(trades),
                "tp": int(tp),
                "sl": int(sl),
                "cancels": int(cancels),
                "attempts": int(attempts),
                "attempts_observed": int(self.data.get("attempts_observed", 0) or 0),
                "attempts_replanned": int(self.data.get("attempts_replanned", 0) or 0),
                "attempts_withheld": int(self.data.get("attempts_withheld", 0) or 0),
                "long_trades": int(long_trades),
                "short_trades": int(short_trades),
                "pnl_netto": float(pnl_netto),
            },
        }

    # ─────────────────────────────────────────────
    def _float_any(self, *values, default=0.0) -> float:
        for value in values:
            try:
                if value is None:
                    continue
                return float(value)
            except Exception:
                continue
        return float(default)

    def _clip01(self, value) -> float:
        value = self._float_any(value, default=0.0)
        if value != value:
            value = 0.0
        return max(0.0, min(1.0, float(value)))

    def _mean_recent(self, records: list, key: str, default=0.0) -> float:
        values = []
        for item in list(records or []):
            if not isinstance(item, dict) or key not in item:
                continue
            try:
                values.append(float(item.get(key, 0.0) or 0.0))
            except Exception:
                continue
        if not values:
            return float(default or 0.0)
        return float(sum(values) / len(values))

    def _last_recent(self, records: list, key: str, default=0.0) -> float:
        for item in reversed(list(records or [])):
            if not isinstance(item, dict) or key not in item:
                continue
            try:
                return float(item.get(key, 0.0) or 0.0)
            except Exception:
                continue
        return float(default or 0.0)

    def _sensory_state_label(self, score: float, high: str, mid: str, low: str) -> str:
        score = self._clip01(score)
        if score >= 0.66:
            return high
        if score >= 0.42:
            return mid
        return low

    def _derive_sensory_balance_summary(self, proof: dict) -> dict:
        recent = list(self.data.get("recent_attempts", []) or [])[-80:]
        last_outcome = dict(self.data.get("last_outcome_decomposition_enriched", {}) or {})

        structure_quality = self._mean_recent(recent, "structure_quality", last_outcome.get("structure_quality", 0.0))
        visual_grounding = self._mean_recent(recent, "visual_grounding_strength", last_outcome.get("visual_grounding_strength", 0.0))
        visual_binding = self._mean_recent(recent, "visual_object_binding", last_outcome.get("visual_object_binding", structure_quality))
        visual_gap = self._mean_recent(recent, "visual_grounding_gap", last_outcome.get("visual_grounding_gap", 0.0))
        visual_blind_load = self._mean_recent(recent, "visual_blind_action_load", last_outcome.get("visual_blind_action_load", 0.0))
        visual_contact_candidate = self._mean_recent(recent, "visual_contact_candidate", last_outcome.get("visual_contact_candidate", 0.0))
        visual_background_load = self._mean_recent(recent, "visual_background_load", last_outcome.get("visual_background_load", 0.0))
        visual_depth = self._mean_recent(recent, "visual_depth", last_outcome.get("visual_depth", 0.0))
        visual_object_presence = self._mean_recent(recent, "visual_object_presence", last_outcome.get("visual_object_presence", 0.0))
        visual_object_clarity = self._mean_recent(recent, "visual_object_clarity", last_outcome.get("visual_object_clarity", 0.0))
        visual_relation_coherence = self._mean_recent(recent, "visual_relation_coherence", last_outcome.get("visual_relation_coherence", 0.0))
        visual_readiness = self._mean_recent(recent, "visual_readiness", last_outcome.get("visual_readiness", 0.0))
        visual_object_distance = self._mean_recent(recent, "visual_object_distance", last_outcome.get("visual_object_distance", 0.0))
        visual_contact_nearness = self._mean_recent(recent, "visual_contact_nearness", last_outcome.get("visual_contact_nearness", 0.0))
        visual_lifecycle_stability = self._mean_recent(recent, "visual_lifecycle_stability", last_outcome.get("visual_lifecycle_stability", 0.0))
        visual_lifecycle_rejection = self._mean_recent(recent, "visual_lifecycle_rejection", last_outcome.get("visual_lifecycle_rejection", 0.0))
        visual_lifecycle_dissolution = self._mean_recent(recent, "visual_lifecycle_dissolution", last_outcome.get("visual_lifecycle_dissolution", 0.0))
        visual_object_binding_quality = self._mean_recent(recent, "visual_object_binding_quality", last_outcome.get("visual_object_binding_quality", 0.0))
        visual_cortex_grounding = self._mean_recent(recent, "visual_cortex_grounding", last_outcome.get("visual_cortex_grounding", 0.0))
        area_multisensory_coherence = self._mean_recent(recent, "area_multisensory_coherence", last_outcome.get("area_multisensory_coherence", 0.0))
        area_attention_need = self._mean_recent(recent, "area_attention_need", last_outcome.get("area_attention_need", 0.0))
        area_felt_depth = self._mean_recent(recent, "area_felt_depth", last_outcome.get("area_felt_depth", 0.0))
        area_overcoupling_risk = self._mean_recent(recent, "area_overcoupling_risk", last_outcome.get("area_overcoupling_risk", 0.0))
        visual_sight_label = ""
        visual_form_family = ""
        visual_cortex_label = ""
        dominant_visual_object = ""
        visual_relation_label = ""
        visual_lifecycle_label = ""
        visual_object_side = ""
        area_profile_state = ""
        for item in reversed(list(recent or [])):
            if not isinstance(item, dict):
                continue
            if not visual_sight_label:
                visual_sight_label = str(item.get("visual_sight_label", "") or "")
            if not visual_form_family:
                visual_form_family = str(item.get("visual_form_family", "") or "")
            if not visual_cortex_label:
                visual_cortex_label = str(item.get("visual_cortex_label", "") or "")
            if not dominant_visual_object:
                dominant_visual_object = str(item.get("dominant_visual_object", "") or "")
            if not visual_relation_label:
                visual_relation_label = str(item.get("visual_relation_label", "") or "")
            if not visual_lifecycle_label:
                visual_lifecycle_label = str(item.get("visual_lifecycle_label", "") or "")
            if not visual_object_side:
                visual_object_side = str(item.get("visual_object_side", "") or "")
            if not area_profile_state:
                area_profile_state = str(item.get("area_profile_state", "") or "")
            if (
                visual_sight_label and visual_form_family and visual_cortex_label
                and dominant_visual_object and visual_relation_label
                and visual_lifecycle_label and visual_object_side
                and area_profile_state
            ):
                break
        visual_score = self._clip01(
            (self._clip01(structure_quality) * 0.38)
            + (self._clip01(visual_grounding) * 0.24)
            + (self._clip01(visual_binding) * 0.18)
            + ((1.0 - self._clip01(visual_gap)) * 0.10)
            + ((1.0 - self._clip01(visual_blind_load)) * 0.10)
        )

        hearing_loudness = self._mean_recent(recent, "market_loudness", last_outcome.get("market_loudness", 0.0))
        hearing_compression = self._mean_recent(recent, "market_hearing_compression", last_outcome.get("market_hearing_compression", 0.0))
        hearing_frequency = self._last_recent(recent, "market_frequency_hz", last_outcome.get("market_frequency_hz", 0.0))
        hearing_overstim = self._clip01((max(0.0, hearing_loudness - 0.85) * 0.55) + (hearing_compression * 0.45))
        hearing_score = self._clip01(1.0 - (hearing_overstim * 0.72))

        contact_carry = self._mean_recent(recent, "contact_carrying_quality", last_outcome.get("contact_carrying_quality", 0.0))
        outer_inner = self._mean_recent(recent, "outer_inner_coherence", last_outcome.get("outer_inner_coherence", 0.0))
        felt_pressure = self._mean_recent(recent, "pressure_to_capacity", last_outcome.get("pressure_to_capacity", 0.0))
        contact_over = self._mean_recent(recent, "contact_overcoupling_risk", last_outcome.get("contact_overcoupling_risk", 0.0))
        mcm_axis_displacement = self._last_recent(recent, "mcm_axis_displacement", last_outcome.get("mcm_axis_displacement", 0.0))
        mcm_axis_field_position = self._last_recent(recent, "mcm_axis_field_position", last_outcome.get("mcm_axis_field_position", 0.0))
        mcm_axis_tension = self._last_recent(recent, "mcm_axis_tension", last_outcome.get("mcm_axis_tension", 0.0))
        mcm_axis_state = "0"
        for item in reversed(list(recent or [])):
            if not isinstance(item, dict):
                continue
            state = str(item.get("mcm_axis_state", "") or "").strip()
            if state:
                mcm_axis_state = state
                break
        felt_score = self._clip01(
            (self._clip01(contact_carry) * 0.36)
            + (self._clip01(outer_inner) * 0.26)
            + ((1.0 - self._clip01(felt_pressure)) * 0.20)
            + ((1.0 - self._clip01(contact_over)) * 0.18)
        )

        thought_enabled = bool(getattr(Config, "MCM_HYPOTHESIS_LEARNING_ENABLED", False)) or bool(getattr(Config, "MCM_THOUGHT_MEMORY_ENABLED", False))
        thought_confirm = self._mean_recent(recent, "thought_confirmation_bearing", proof.get("hypothesis_confirmation_without_action", 0.0))
        thought_trust = self._mean_recent(recent, "thought_trust_bearing", proof.get("hypothesis_trust_score", 0.0))
        thought_reject = self._mean_recent(recent, "thought_rejection_pressure", proof.get("hypothesis_rejection_without_action", 0.0))
        thought_contradiction = self._mean_recent(recent, "thought_contradiction_pressure", last_outcome.get("thought_contradiction_pressure", 0.0))
        thought_score = (
            self._clip01(
                (self._clip01(thought_confirm) * 0.32)
                + (self._clip01(thought_trust) * 0.28)
                + ((1.0 - self._clip01(thought_reject)) * 0.20)
                + ((1.0 - self._clip01(thought_contradiction)) * 0.20)
            )
            if thought_enabled
            else 1.0
        )

        inner_consent = self._mean_recent(recent, "inner_action_consent", last_outcome.get("inner_action_consent", 0.0))
        action_support = self._mean_recent(recent, "inner_action_support", last_outcome.get("inner_action_support", 0.0))
        action_no = self._mean_recent(recent, "inner_action_no", last_outcome.get("inner_action_no", 0.0))
        action_inhibition = self._clip01(proof.get("action_inhibition", 0.0))
        execution_quality = self._clip01(last_outcome.get("execution_quality", 0.0))
        plan_quality = self._clip01(last_outcome.get("plan_quality", 0.0))
        risk_fit = self._clip01(last_outcome.get("risk_fit_quality", 0.0))
        action_score = self._clip01(
            (self._clip01(inner_consent) * 0.26)
            + (self._clip01(action_support) * 0.18)
            + ((1.0 - self._clip01(action_no)) * 0.16)
            + ((1.0 - action_inhibition) * 0.12)
            + (plan_quality * 0.10)
            + (execution_quality * 0.10)
            + (risk_fit * 0.08)
        )

        integration_score = self._clip01(
            (visual_score * 0.22)
            + (hearing_score * 0.14)
            + (felt_score * 0.24)
            + ((thought_score if thought_enabled else felt_score) * 0.18)
            + (action_score * 0.22)
        )

        if visual_score < 0.38:
            break_layer = "sehen"
        elif hearing_overstim > 0.58 and (thought_score < 0.48 if thought_enabled else action_score < 0.48):
            break_layer = "hoeren_reizueberhang"
        elif felt_score < 0.38:
            break_layer = "fuehlen"
        elif thought_enabled and thought_score < 0.38:
            break_layer = "denken"
        elif action_score < 0.38:
            break_layer = "handlung"
        else:
            break_layer = "keine_klare_bruchstelle"

        if break_layer == "handlung":
            interpretation = "Sinneslagen tragen eher als die Handlungsnaehe; Bruch liegt zwischen Wahrnehmung, MCM-Kontakt und Entry."
        elif break_layer == "denken":
            interpretation = "Sehen/Fuehlen liefern Reiz, aber die Verdichtung zur tragenden Hypothese bleibt schwach."
        elif break_layer == "hoeren_reizueberhang":
            interpretation = "Hoerreiz wirkt stark; DIO braucht mehr Abstand zwischen Marktspannung und Denken."
        elif break_layer == "sehen":
            interpretation = "Formwahrnehmung ist unscharf; DIO fuehlt mehr als er strukturell sieht."
        elif break_layer == "fuehlen":
            interpretation = "Form kann sichtbar sein, aber das MCM-Feld traegt den Kontakt nicht stabil."
        else:
            interpretation = "Sehen, Hoeren, Fuehlen, Denken und Handlung sind ohne klare Einzelbruchstelle gekoppelt."

        return {
            "state": "sensory_balance_observed",
            "integration_score": float(integration_score),
            "break_layer": str(break_layer),
            "interpretation": str(interpretation),
            "sehen": {
                "state": self._sensory_state_label(visual_score, "clear_form", "partial_form", "blurred_form"),
                "score": float(visual_score),
                "structure_quality": float(structure_quality),
                "visual_grounding_strength": float(visual_grounding),
                "visual_object_binding": float(visual_binding),
                "visual_grounding_gap": float(visual_gap),
                "visual_blind_action_load": float(visual_blind_load),
                "visual_sight_label": str(visual_sight_label),
                "visual_form_family": str(visual_form_family),
                "visual_contact_candidate": float(visual_contact_candidate),
                "visual_background_load": float(visual_background_load),
                "visual_depth": float(visual_depth),
                "visual_cortex_label": str(visual_cortex_label),
                "dominant_visual_object": str(dominant_visual_object),
                "visual_object_presence": float(visual_object_presence),
                "visual_object_clarity": float(visual_object_clarity),
                "visual_relation_coherence": float(visual_relation_coherence),
                "visual_readiness": float(visual_readiness),
                "visual_relation_label": str(visual_relation_label),
                "visual_lifecycle_label": str(visual_lifecycle_label),
                "visual_object_side": str(visual_object_side),
                "visual_object_distance": float(visual_object_distance),
                "visual_contact_nearness": float(visual_contact_nearness),
                "visual_lifecycle_stability": float(visual_lifecycle_stability),
                "visual_lifecycle_rejection": float(visual_lifecycle_rejection),
                "visual_lifecycle_dissolution": float(visual_lifecycle_dissolution),
                "visual_object_binding_quality": float(visual_object_binding_quality),
                "visual_cortex_grounding": float(visual_cortex_grounding),
            },
            "bereich": {
                "state": str(area_profile_state or "background_area_perception"),
                "multisensory_coherence": float(area_multisensory_coherence),
                "attention_need": float(area_attention_need),
                "felt_depth": float(area_felt_depth),
                "overcoupling_risk": float(area_overcoupling_risk),
                "role": "perception_only",
            },
            "hoeren": {
                "state": "overstimulated_hearing" if hearing_overstim >= 0.58 else self._sensory_state_label(hearing_score, "calm_hearing", "active_hearing", "noisy_hearing"),
                "score": float(hearing_score),
                "loudness": float(hearing_loudness),
                "compression": float(hearing_compression),
                "frequency_hz": float(hearing_frequency),
                "overstimulation": float(hearing_overstim),
            },
            "fuehlen": {
                "state": self._sensory_state_label(felt_score, "carrying_field", "mixed_field", "burdened_field"),
                "score": float(felt_score),
                "mcm_axis_displacement": float(mcm_axis_displacement),
                "mcm_axis_field_position": float(mcm_axis_field_position),
                "mcm_axis_tension": float(mcm_axis_tension),
                "mcm_axis_state": str(mcm_axis_state),
                "contact_carrying_quality": float(contact_carry),
                "outer_inner_coherence": float(outer_inner),
                "pressure_to_capacity": float(felt_pressure),
                "contact_overcoupling_risk": float(contact_over),
            },
            "denken": {
                "state": "thought_disabled" if not thought_enabled else self._sensory_state_label(thought_score, "coherent_thought", "learning_thought", "unclear_thought"),
                "score": float(thought_score),
                "enabled": bool(thought_enabled),
                "confirmation_bearing": float(thought_confirm),
                "trust_bearing": float(thought_trust),
                "rejection_pressure": float(thought_reject),
                "contradiction_pressure": float(thought_contradiction),
            },
            "handlung": {
                "state": self._sensory_state_label(action_score, "action_coupled", "action_fragile", "action_break"),
                "score": float(action_score),
                "inner_action_consent": float(inner_consent),
                "inner_action_support": float(action_support),
                "inner_action_no": float(action_no),
                "action_inhibition": float(action_inhibition),
                "plan_quality": float(plan_quality),
                "execution_quality": float(execution_quality),
                "risk_fit_quality": float(risk_fit),
            },
            "sample": {
                "recent_attempts": int(len(recent)),
                "trades": int(self.data.get("trades", 0) or 0),
                "attempts": int(self.data.get("attempts", 0) or 0),
                "pnl_netto": float(self.data.get("pnl_netto", 0.0) or 0.0),
            },
        }

    def _write_sensory_balance_protocol(self):
        if not bool(getattr(Config, "MCM_SENSORY_BALANCE_PROTOCOL_DEBUG", False)):
            return
        payload = dict(self.data.get("sensory_balance", {}) or {})
        if not payload:
            return
        try:
            path = dbr_resolve_path("debug/mcm_sensory_balance_protocol.json")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except Exception:
            pass

    def _remember_outcome_record(self, record: dict):
        try:
            cache = list(getattr(self, "_outcome_records_cache", []) or [])
            cache.append(dict(record or {}))
            self._outcome_records_cache = cache[-2000:]
        except Exception:
            pass

    def _pick_fields(self, payload: dict, keys: list[str]) -> dict:
        source = dict(payload or {})
        result = {}

        for key in list(keys or []):
            if key not in source:
                continue

            value = source.get(key)
            if value is None:
                continue

            result[str(key)] = value

        return result

    # ─────────────────────────────────────────────
    def _net_pnl_at_price(self, *, side: str, entry: float, exit_price: float, amount: float) -> float:
        side_key = str(side or "").upper().strip()
        if side_key == "LONG":
            gross = (float(exit_price) - float(entry)) * float(amount)
        elif side_key == "SHORT":
            gross = (float(entry) - float(exit_price)) * float(amount)
        else:
            return 0.0

        fee_rate = getattr(Config, "FEE_RATE", 0.0) or 0.0
        fees = (
            (float(entry) * float(amount) * fee_rate) +
            (float(exit_price) * float(amount) * fee_rate) +
            (Config.FEE_PER_TRADE or 0.0)
        )
        return float(gross - fees)

    # ─────────────────────────────────────────────
    def _record_exit_candidate_replay(self, *, entry: float, side: str, amount: float, actual_reason: str, actual_exit_price: float, actual_pnl: float, context: dict):
        replay_state = dict((context or {}).get("exit_candidate_replay_state", {}) or {})
        if not bool(replay_state.get("exit_candidate", False)):
            return None

        try:
            candidate_price = float(replay_state.get("candidate_price", replay_state.get("close", 0.0)) or 0.0)
        except Exception:
            candidate_price = 0.0
        if candidate_price <= 0.0:
            return None

        hypothetical_pnl = self._net_pnl_at_price(
            side=str(side),
            entry=float(entry),
            exit_price=float(candidate_price),
            amount=float(amount),
        )
        delta_pnl = float(hypothetical_pnl) - float(actual_pnl)
        actual_reason_key = str(actual_reason or "").strip().lower()

        self.data["exit_candidate_replay_count"] = int(self.data.get("exit_candidate_replay_count", 0) or 0) + 1
        self.data["exit_candidate_replay_actual_pnl"] = float(self.data.get("exit_candidate_replay_actual_pnl", 0.0) or 0.0) + float(actual_pnl)
        self.data["exit_candidate_replay_hypothetical_pnl"] = float(self.data.get("exit_candidate_replay_hypothetical_pnl", 0.0) or 0.0) + float(hypothetical_pnl)
        self.data["exit_candidate_replay_delta_pnl"] = float(self.data.get("exit_candidate_replay_delta_pnl", 0.0) or 0.0) + float(delta_pnl)

        if delta_pnl > 0.0 and actual_pnl < 0.0:
            self.data["exit_candidate_replay_saved_loss_count"] = int(self.data.get("exit_candidate_replay_saved_loss_count", 0) or 0) + 1
        elif delta_pnl > 0.0:
            self.data["exit_candidate_replay_saved_giveback_count"] = int(self.data.get("exit_candidate_replay_saved_giveback_count", 0) or 0) + 1
        elif delta_pnl < 0.0:
            self.data["exit_candidate_replay_harmed_count"] = int(self.data.get("exit_candidate_replay_harmed_count", 0) or 0) + 1

        if actual_reason_key == "tp_hit" and delta_pnl < 0.0:
            self.data["exit_candidate_replay_tp_cut_count"] = int(self.data.get("exit_candidate_replay_tp_cut_count", 0) or 0) + 1

        replay_csv = {
            "timestamp": self.data.get("current_timestamp"),
            "candidate_timestamp": replay_state.get("candidate_timestamp"),
            "candidate_bars_open": replay_state.get("candidate_bars_open"),
            "side": str(side or "").upper().strip(),
            "entry": float(entry),
            "candidate_price": float(candidate_price),
            "actual_exit_price": float(actual_exit_price),
            "actual_reason": str(actual_reason_key),
            "actual_pnl": float(actual_pnl),
            "hypothetical_pnl": float(hypothetical_pnl),
            "delta_pnl": float(delta_pnl),
            "confirmation_score": float(replay_state.get("confirmation_score", 0.0) or 0.0),
            "exit_decision_pressure": float(replay_state.get("exit_decision_pressure", 0.0) or 0.0),
            "plan_trust": float(replay_state.get("plan_trust", 0.0) or 0.0),
            "holding_stability": float(replay_state.get("holding_stability", 0.0) or 0.0),
            "intervention_fitness": float(replay_state.get("intervention_fitness", 0.0) or 0.0),
            "intervention_unfit_state": float(replay_state.get("intervention_unfit_state", 0.0) or 0.0),
            "exit_evidence": float(replay_state.get("exit_evidence", 0.0) or 0.0),
            "current_r": float(replay_state.get("current_r", 0.0) or 0.0),
            "candidate_mfe_r": float(replay_state.get("candidate_mfe_r", 0.0) or 0.0),
            "candidate_mae_r": float(replay_state.get("candidate_mae_r", 0.0) or 0.0),
            "target_expectation_context": str(replay_state.get("target_expectation_context", "") or ""),
            "tp_reachability": float(replay_state.get("tp_reachability", 0.0) or 0.0),
            "target_path_integrity": float(replay_state.get("target_path_integrity", 0.0) or 0.0),
            "expectation_deviation": float(replay_state.get("expectation_deviation", 0.0) or 0.0),
            "expectation_break_pressure": float(replay_state.get("expectation_break_pressure", 0.0) or 0.0),
            "expectation_hold_support": float(replay_state.get("expectation_hold_support", 0.0) or 0.0),
            "target_recovery_potential": float(replay_state.get("target_recovery_potential", 0.0) or 0.0),
            "target_recovery_momentum": float(replay_state.get("target_recovery_momentum", 0.0) or 0.0),
            "target_recovery_confirmation": float(replay_state.get("target_recovery_confirmation", 0.0) or 0.0),
            "break_to_recovery_delta": float(replay_state.get("break_to_recovery_delta", 0.0) or 0.0),
            "prior_target_hold_support": float(replay_state.get("prior_target_hold_support", 0.0) or 0.0),
            "prior_tp_reachability": float(replay_state.get("prior_tp_reachability", 0.0) or 0.0),
            "expectation_break_persistence": float(replay_state.get("expectation_break_persistence", 0.0) or 0.0),
            "deep_retrace_recovery_watch": int(bool(replay_state.get("deep_retrace_recovery_watch", False))),
            "recovery_after_break_watch": int(bool(replay_state.get("recovery_after_break_watch", False))),
            "entry_route_familiarity": float(replay_state.get("entry_route_familiarity", 0.0) or 0.0),
            "entry_transfer_bearing": float(replay_state.get("entry_transfer_bearing", 0.0) or 0.0),
            "current_route_familiarity": float(replay_state.get("current_route_familiarity", 0.0) or 0.0),
            "current_semantic_shift_pressure": float(replay_state.get("current_semantic_shift_pressure", 0.0) or 0.0),
            "current_transfer_bearing": float(replay_state.get("current_transfer_bearing", 0.0) or 0.0),
            "current_interpretation_quality": float(replay_state.get("current_interpretation_quality", 0.0) or 0.0),
            "current_adaptation_phase": str(replay_state.get("current_adaptation_phase", "") or ""),
            "route_familiarity_delta": float(replay_state.get("route_familiarity_delta", 0.0) or 0.0),
            "transfer_bearing_delta": float(replay_state.get("transfer_bearing_delta", 0.0) or 0.0),
            "semantic_transfer_stress": float(replay_state.get("semantic_transfer_stress", 0.0) or 0.0),
        }
        self._append_exit_candidate_replay_csv(replay_csv)

        dbr_debug(
            "EXIT_CANDIDATE_REPLAY "
            f"ts={self.data.get('current_timestamp')} "
            f"candidate_ts={replay_state.get('candidate_timestamp')} "
            f"side={str(side or '').upper().strip()} "
            f"entry={float(entry):.4f} candidate_price={candidate_price:.4f} "
            f"actual_exit_price={float(actual_exit_price):.4f} actual_reason={actual_reason_key} "
            f"actual_pnl={float(actual_pnl):.6f} hypothetical_pnl={float(hypothetical_pnl):.6f} "
            f"delta_pnl={float(delta_pnl):.6f} "
            f"score={float(replay_state.get('confirmation_score', 0.0) or 0.0):.4f} "
            f"pressure={float(replay_state.get('exit_decision_pressure', 0.0) or 0.0):.4f} "
            f"plan_trust={float(replay_state.get('plan_trust', 0.0) or 0.0):.4f} "
            f"fitness={float(replay_state.get('intervention_fitness', 0.0) or 0.0):.4f}",
            "mcm_exit_candidate_replay_debug.log",
        )

        return {
            "candidate_price": float(candidate_price),
            "hypothetical_pnl": float(hypothetical_pnl),
            "delta_pnl": float(delta_pnl),
        }

    # ─────────────────────────────────────────────
    def _append_exit_candidate_replay_csv(self, record: dict):
        try:
            path = str(self.exit_candidate_replay_path)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            keys = [
                "timestamp",
                "candidate_timestamp",
                "candidate_bars_open",
                "side",
                "entry",
                "candidate_price",
                "actual_exit_price",
                "actual_reason",
                "actual_pnl",
                "hypothetical_pnl",
                "delta_pnl",
                "confirmation_score",
                "exit_decision_pressure",
                "plan_trust",
                "holding_stability",
                "intervention_fitness",
                "intervention_unfit_state",
                "exit_evidence",
                "current_r",
                "candidate_mfe_r",
                "candidate_mae_r",
                "target_expectation_context",
                "tp_reachability",
                "target_path_integrity",
                "expectation_deviation",
                "expectation_break_pressure",
                "expectation_hold_support",
                "target_recovery_potential",
                "target_recovery_momentum",
                "target_recovery_confirmation",
                "break_to_recovery_delta",
                "prior_target_hold_support",
                "prior_tp_reachability",
                "expectation_break_persistence",
                "deep_retrace_recovery_watch",
                "recovery_after_break_watch",
                "entry_route_familiarity",
                "entry_transfer_bearing",
                "current_route_familiarity",
                "current_semantic_shift_pressure",
                "current_transfer_bearing",
                "current_interpretation_quality",
                "current_adaptation_phase",
                "route_familiarity_delta",
                "transfer_bearing_delta",
                "semantic_transfer_stress",
            ]
            header_key = f"_csv_header_written::{path}"
            write_header = (not os.path.exists(path)) and not bool(getattr(self, header_key, False))
            payload = ""
            if write_header:
                payload += ",".join(keys) + "\n"
                setattr(self, header_key, True)
            payload += ",".join(str((record or {}).get(key, "")) for key in keys) + "\n"
            dbr_append_text(
                path,
                payload,
                operation="exit_candidate_replay_csv_append",
            )
        except Exception:
            pass

    # ─────────────────────────────────────────────
    def _compact_context(self, context: dict) -> dict:
        normalized_context = self._normalize_record_value(context or {})
        compact_attempt = bool(getattr(Config, "TRADE_STATS_ATTEMPT_RECORD_COMPACT", True))

        def _compact_snapshot(value):
            item = self._normalize_record_value(value or {})
            if not isinstance(item, dict):
                return {}
            return {
                "tension": self._pick_fields(item.get("tension", {}), [
                    "stability",
                    "clarity",
                    "pressure",
                    "conflict",
                    "recovery_balance",
                ]),
                "field": self._pick_fields(item.get("field", {}), [
                    "pressure_to_capacity",
                    "regulatory_load",
                    "action_capacity",
                    "recovery_need",
                    "survival_pressure",
                    "capacity_reserve",
                    "recovery_balance",
                    "field_perception_label",
                    "field_perception_clarity",
                    "field_perception_fragmentation",
                    "field_perception_strain",
                ]),
                "experience": self._pick_fields(item.get("experience", {}), [
                    "pressure_release",
                    "load_bearing_capacity",
                    "process_quality",
                    "carrying_capacity_delta",
                    "self_confidence_delta",
                ]),
            }

        trade_plan_source = dict(normalized_context.get("trade_plan", {}) or {})
        action_intent_source = dict(normalized_context.get("action_intent_state", {}) or {})
        meta_source = dict(normalized_context.get("meta_regulation_state", {}) or {})
        possibility_source = dict(
            normalized_context.get(
                "possibility_field_state",
                meta_source.get("mcm_possibility_field_state", {}),
            )
            or {}
        )
        rejection_reason = str(
            normalized_context.get(
                "rejection_reason",
                trade_plan_source.get(
                    "rejection_reason",
                    meta_source.get("rejection_reason", action_intent_source.get("intent_state", "")),
                ),
            )
            or ""
        )
        inner_action_consent_state = str(
            normalized_context.get(
                "inner_action_consent_state",
                trade_plan_source.get(
                    "inner_action_consent_state",
                    meta_source.get("inner_action_consent_state", rejection_reason),
                ),
            )
            or ""
        )
        compact = {
            "decision_tendency": str(normalized_context.get("decision_tendency", "") or ""),
            "proposed_decision": str(normalized_context.get("proposed_decision", "") or ""),
            "rejection_reason": rejection_reason,
            "inner_action_consent": float(normalized_context.get("inner_action_consent", trade_plan_source.get("inner_action_consent", meta_source.get("inner_action_consent", 0.0))) or 0.0),
            "inner_action_support": float(normalized_context.get("inner_action_support", trade_plan_source.get("inner_action_support", meta_source.get("inner_action_support", 0.0))) or 0.0),
            "inner_action_no": float(normalized_context.get("inner_action_no", trade_plan_source.get("inner_action_no", meta_source.get("inner_action_no", 0.0))) or 0.0),
            "inner_action_consent_state": inner_action_consent_state,
            "strategy_confirmation": float(normalized_context.get("strategy_confirmation", trade_plan_source.get("strategy_confirmation", meta_source.get("strategy_confirmation", 0.0))) or 0.0),
            "strategy_rejection": float(normalized_context.get("strategy_rejection", trade_plan_source.get("strategy_rejection", meta_source.get("strategy_rejection", 0.0))) or 0.0),
            "strategy_trust_bearing": float(normalized_context.get("strategy_trust_bearing", trade_plan_source.get("strategy_trust_bearing", meta_source.get("strategy_trust_bearing", 0.0))) or 0.0),
            "strategy_context_bearing": float(normalized_context.get("strategy_context_bearing", trade_plan_source.get("strategy_context_bearing", meta_source.get("strategy_context_bearing", 0.0))) or 0.0),
            "raw_strategy_contradiction_pressure": float(normalized_context.get("raw_strategy_contradiction_pressure", trade_plan_source.get("raw_strategy_contradiction_pressure", meta_source.get("raw_strategy_contradiction_pressure", 0.0))) or 0.0),
            "strategy_contradiction_pressure": float(normalized_context.get("strategy_contradiction_pressure", trade_plan_source.get("strategy_contradiction_pressure", meta_source.get("strategy_contradiction_pressure", 0.0))) or 0.0),
            "thought_confirmation_bearing": float(normalized_context.get("thought_confirmation_bearing", trade_plan_source.get("thought_confirmation_bearing", meta_source.get("thought_confirmation_bearing", normalized_context.get("strategy_confirmation", trade_plan_source.get("strategy_confirmation", meta_source.get("strategy_confirmation", 0.0)))))) or 0.0),
            "thought_rejection_pressure": float(normalized_context.get("thought_rejection_pressure", trade_plan_source.get("thought_rejection_pressure", meta_source.get("thought_rejection_pressure", normalized_context.get("strategy_rejection", trade_plan_source.get("strategy_rejection", meta_source.get("strategy_rejection", 0.0)))))) or 0.0),
            "thought_trust_bearing": float(normalized_context.get("thought_trust_bearing", trade_plan_source.get("thought_trust_bearing", meta_source.get("thought_trust_bearing", normalized_context.get("strategy_trust_bearing", trade_plan_source.get("strategy_trust_bearing", meta_source.get("strategy_trust_bearing", 0.0)))))) or 0.0),
            "contact_context_bearing": float(normalized_context.get("contact_context_bearing", trade_plan_source.get("contact_context_bearing", meta_source.get("contact_context_bearing", normalized_context.get("strategy_context_bearing", trade_plan_source.get("strategy_context_bearing", meta_source.get("strategy_context_bearing", 0.0)))))) or 0.0),
            "real_area_contact_bearing": float(normalized_context.get("real_area_contact_bearing", trade_plan_source.get("real_area_contact_bearing", meta_source.get("real_area_contact_bearing", 0.0))) or 0.0),
            "visual_reality_bearing": float(normalized_context.get("visual_reality_bearing", trade_plan_source.get("visual_reality_bearing", meta_source.get("visual_reality_bearing", 0.0))) or 0.0),
            "felt_reality_bearing": float(normalized_context.get("felt_reality_bearing", trade_plan_source.get("felt_reality_bearing", meta_source.get("felt_reality_bearing", meta_source.get("contact_carrying_quality", 0.0)))) or 0.0),
            "form_mcm_reality_fit": float(normalized_context.get("form_mcm_reality_fit", trade_plan_source.get("form_mcm_reality_fit", meta_source.get("form_mcm_reality_fit", meta_source.get("outer_inner_coherence", 0.0)))) or 0.0),
            "receptive_contact_offer_pressure": float(normalized_context.get("receptive_contact_offer_pressure", trade_plan_source.get("receptive_contact_offer_pressure", meta_source.get("receptive_contact_offer_pressure", 0.0))) or 0.0),
            "receptive_contact_maturity": float(normalized_context.get("receptive_contact_maturity", trade_plan_source.get("receptive_contact_maturity", meta_source.get("receptive_contact_maturity", 0.0))) or 0.0),
            "receptive_contact_immaturity_pressure": float(normalized_context.get("receptive_contact_immaturity_pressure", trade_plan_source.get("receptive_contact_immaturity_pressure", meta_source.get("receptive_contact_immaturity_pressure", 0.0))) or 0.0),
            "receptive_contact_restraint": float(normalized_context.get("receptive_contact_restraint", trade_plan_source.get("receptive_contact_restraint", meta_source.get("receptive_contact_restraint", 0.0))) or 0.0),
            "raw_thought_contradiction_pressure": float(normalized_context.get("raw_thought_contradiction_pressure", trade_plan_source.get("raw_thought_contradiction_pressure", meta_source.get("raw_thought_contradiction_pressure", normalized_context.get("raw_strategy_contradiction_pressure", trade_plan_source.get("raw_strategy_contradiction_pressure", meta_source.get("raw_strategy_contradiction_pressure", 0.0)))))) or 0.0),
            "thought_contradiction_pressure": float(normalized_context.get("thought_contradiction_pressure", trade_plan_source.get("thought_contradiction_pressure", meta_source.get("thought_contradiction_pressure", normalized_context.get("strategy_contradiction_pressure", trade_plan_source.get("strategy_contradiction_pressure", meta_source.get("strategy_contradiction_pressure", 0.0)))))) or 0.0),
            "open_hypothesis_reality_permission": float(normalized_context.get("open_hypothesis_reality_permission", trade_plan_source.get("open_hypothesis_reality_permission", meta_source.get("open_hypothesis_reality_permission", normalized_context.get("open_hypothesis_action_permission", trade_plan_source.get("open_hypothesis_action_permission", meta_source.get("open_hypothesis_action_permission", 0.0)))))) or 0.0),
            "possibility_contact_bearing": float(normalized_context.get("possibility_contact_bearing", trade_plan_source.get("possibility_contact_bearing", meta_source.get("possibility_contact_bearing", normalized_context.get("possibility_action_support", trade_plan_source.get("possibility_action_support", meta_source.get("possibility_action_support", 0.0)))))) or 0.0),
            "dominant_hypothesis_reality_bearing": float(normalized_context.get("dominant_hypothesis_reality_bearing", trade_plan_source.get("dominant_hypothesis_reality_bearing", meta_source.get("dominant_hypothesis_reality_bearing", normalized_context.get("dominant_hypothesis_action_readiness", trade_plan_source.get("dominant_hypothesis_action_readiness", meta_source.get("dominant_hypothesis_action_readiness", 0.0)))))) or 0.0),
            "current_hypothesis_reality_bearing": float(normalized_context.get("current_hypothesis_reality_bearing", trade_plan_source.get("current_hypothesis_reality_bearing", meta_source.get("current_hypothesis_reality_bearing", normalized_context.get("current_hypothesis_action_support", trade_plan_source.get("current_hypothesis_action_support", meta_source.get("current_hypothesis_action_support", 0.0)))))) or 0.0),
            "hypothesis_reality_bearing": float(normalized_context.get("hypothesis_reality_bearing", trade_plan_source.get("hypothesis_reality_bearing", meta_source.get("hypothesis_reality_bearing", normalized_context.get("hypothesis_action_support", trade_plan_source.get("hypothesis_action_support", meta_source.get("hypothesis_action_support", 0.0)))))) or 0.0),
            "order_geometry_source": str(normalized_context.get("order_geometry_source", trade_plan_source.get("order_geometry_source", "")) or ""),
            "impulse_role": str(normalized_context.get("impulse_role", trade_plan_source.get("impulse_role", "")) or ""),
            "entry_mode": str(normalized_context.get("entry_mode", "") or ""),
            "contact_entry_mode": str(normalized_context.get("contact_entry_mode", trade_plan_source.get("contact_entry_mode", normalized_context.get("entry_mode", ""))) or ""),
            "entry_contact_state": str(normalized_context.get("entry_contact_state", trade_plan_source.get("entry_contact_state", normalized_context.get("entry_choice_state", ""))) or ""),
            "entry_choice_state": str(normalized_context.get("entry_choice_state", "") or ""),
            "area_contact_fit": float(normalized_context.get("area_contact_fit", trade_plan_source.get("area_contact_fit", normalized_context.get("strategic_entry_fit", 0.0))) or 0.0),
            "strategic_entry_fit": float(normalized_context.get("strategic_entry_fit", 0.0) or 0.0),
            "area_bearing_quality": float(normalized_context.get("area_bearing_quality", trade_plan_source.get("area_bearing_quality", meta_source.get("area_bearing_quality", 0.0))) or 0.0),
            "area_contact_timing_fit": float(normalized_context.get("area_contact_timing_fit", trade_plan_source.get("area_contact_timing_fit", meta_source.get("area_contact_timing_fit", meta_source.get("area_action_timing_fit", 0.0)))) or 0.0),
            "area_spacetime_fit": float(normalized_context.get("area_spacetime_fit", trade_plan_source.get("area_spacetime_fit", meta_source.get("area_spacetime_fit", 0.0))) or 0.0),
            "area_present_contact": float(normalized_context.get("area_present_contact", trade_plan_source.get("area_present_contact", meta_source.get("area_present_contact", 0.0))) or 0.0),
            "area_invalidity_pressure": float(normalized_context.get("area_invalidity_pressure", trade_plan_source.get("area_invalidity_pressure", meta_source.get("area_invalidity_pressure", 0.0))) or 0.0),
            "area_afterimage": float(normalized_context.get("area_afterimage", trade_plan_source.get("area_afterimage", meta_source.get("area_afterimage", 0.0))) or 0.0),
            "area_contact_readiness": float(normalized_context.get("area_contact_readiness", trade_plan_source.get("area_contact_readiness", normalized_context.get("area_direct_readiness", 0.0))) or 0.0),
            "area_direct_readiness": float(normalized_context.get("area_direct_readiness", 0.0) or 0.0),
            "market_loudness": float(normalized_context.get("market_loudness", 0.0) or 0.0),
            "market_frequency_hz": float(normalized_context.get("market_frequency_hz", 0.0) or 0.0),
            "market_hearing_compression": float(normalized_context.get("market_hearing_compression", 0.0) or 0.0),
            "energy_coherence_bearing": float(normalized_context.get("energy_coherence_bearing", trade_plan_source.get("energy_coherence_bearing", meta_source.get("energy_coherence_bearing", 0.0))) or 0.0),
            "market_tone": str(normalized_context.get("market_tone", "") or ""),
            "state": self._pick_fields(normalized_context.get("state", {}), [
                "energy",
                "market_loudness",
                "market_frequency_hz",
                "market_hearing_compression",
                "market_tone",
                "coherence",
                "asymmetry",
                "coh_zone",
                "self_state",
                "attractor",
            ]),
            "focus": self._pick_fields(normalized_context.get("focus", {}), [
                "focus_point",
                "focus_confidence",
                "target_lock",
                "target_drift",
            ]),
            "experience": self._pick_fields(normalized_context.get("experience", {}), [
                "entry_expectation",
                "target_expectation",
                "approach_pressure",
                "pressure_release",
                "experience_regulation",
                "reflection_maturity",
                "load_bearing_capacity",
                "protective_width_regulation",
                "protective_courage",
                "carrying_balance",
                "bearing_pressure_gap",
            ]),
            "field_state": self._pick_fields(normalized_context.get("field_state", {}), [
                "field_stimulus_density",
                "field_density",
                "field_stability",
                "regulatory_load",
                "action_capacity",
                "recovery_need",
                "survival_pressure",
                "pressure_to_capacity",
                "capacity_reserve",
                "recovery_balance",
            ]),
            "bearing_context": self._pick_fields(normalized_context.get("bearing_context", {}), [
                "structure_quality",
                "bearing_pressure",
                "load_bearing_capacity",
                "regulation_cost",
                "relief_quality",
            ]),
            "position_watch_state": self._pick_fields(normalized_context.get("position_watch_state", {}), [
                "mfe",
                "mae",
                "risk",
                "mfe_r",
                "mae_r",
                "fill_ratio",
                "bars_open",
            ]),
            "position_intervention_state": self._pick_fields(normalized_context.get("position_intervention_state", {}), [
                "position_cognitive_load",
                "exit_decision_pressure",
                "holding_stability",
                "plan_trust",
                "intervention_fatigue",
                "inner_noise",
                "intervention_fitness",
                "intervention_unfit_state",
                "exit_evidence",
                "sustained_exit_pressure",
                "current_r",
                "giveback_r",
                "mfe_r",
                "mae_r",
                "pressure_to_capacity",
                "structure_quality",
                "structure_stability",
                "context_confidence",
                "bars_open",
                "intervention_label",
                "position_inconsistency_stress",
                "position_mcm_field_strain",
                "position_self_trust_gap",
                "position_cortisol_load",
                "position_noradrenaline_arousal",
                "position_protective_distance",
                "position_held_risk_discomfort",
                "position_process_quality",
                "position_experience_label",
            ]),
            "target_expectation_state": self._pick_fields(normalized_context.get("target_expectation_state", {}), [
                "target_expectation_context",
                "tp_reachability",
                "target_path_integrity",
                "expectation_deviation",
                "expectation_break_pressure",
                "expectation_hold_support",
                "target_room_pressure",
                "target_semantic_confidence",
                "target_progress",
                "target_remaining_r",
                "target_total_r",
                "target_recovery_potential",
                "target_recovery_momentum",
                "target_recovery_confirmation",
                "break_to_recovery_delta",
                "recovery_after_break_watch",
                "prior_target_hold_support",
                "prior_tp_reachability",
                "prior_target_path_integrity",
                "expectation_break_persistence",
                "expectation_break_count",
                "deep_retrace_recovery_watch",
                "base_entry_expectation",
                "base_target_expectation",
                "entry_route_familiarity",
                "entry_transfer_bearing",
                "current_route_familiarity",
                "current_semantic_shift_pressure",
                "current_transfer_bearing",
                "current_interpretation_quality",
                "current_adaptation_phase",
                "route_familiarity_delta",
                "transfer_bearing_delta",
                "semantic_transfer_stress",
            ]),
            "matured_exit_state": self._pick_fields(normalized_context.get("matured_exit_state", {}), [
                "mode",
                "exit_price",
                "maturity_pressure",
                "mfe_r",
                "mae_r",
                "current_r",
                "giveback_r",
                "structure_quality",
                "pressure_to_capacity",
                "recovery_balance",
                "bars_open",
            ]),
            "possibility_field_state": self._pick_fields(possibility_source, [
                "possibility_field_state",
                "possibility_observer_state",
                "possibility_variant_count",
                "possibility_dominant_variant_id",
                "possibility_dominant_kind",
                "possibility_dominant_direction",
                "possibility_dominant_support",
                "possibility_second_support",
                "possibility_spread",
                "possibility_openness",
                "possibility_collapse_pressure",
                "possibility_reflection_pull",
                "possibility_observation_pull",
                "possibility_action_support",
                "possibility_doppler_energy",
                "possibility_future_variant_pressure",
                "possibility_form_mcm_fit",
                "possibility_memory_fit",
                "possibility_caution",
                "possibility_observation_depth",
                "possibility_reality_contact",
                "possibility_variant_maturity",
                "possibility_variant_trust",
                "possibility_variant_caution",
                "possibility_collapse_reason",
                "possibility_collapse_reversibility",
                "possibility_memory_return",
            ]),
            "exit_candidate_observe_state": self._pick_fields(normalized_context.get("exit_candidate_observe_state", {}), [
                "exit_candidate",
                "candidate_label",
                "confirmation_score",
                "exit_decision_pressure",
                "plan_trust",
                "holding_stability",
                "intervention_fitness",
                "intervention_unfit_state",
                "exit_evidence",
                "current_r",
                "adverse_depth_ok",
                "sustained_exit_pressure",
                "target_expectation_context",
                "tp_reachability",
                "target_path_integrity",
                "expectation_deviation",
                "expectation_break_pressure",
                "expectation_hold_support",
                "target_recovery_potential",
                "target_recovery_momentum",
                "target_recovery_confirmation",
                "break_to_recovery_delta",
                "prior_target_hold_support",
                "prior_tp_reachability",
                "expectation_break_persistence",
                "deep_retrace_recovery_watch",
                "recovery_after_break_watch",
                "entry_route_familiarity",
                "entry_transfer_bearing",
                "current_route_familiarity",
                "current_semantic_shift_pressure",
                "current_transfer_bearing",
                "current_interpretation_quality",
                "current_adaptation_phase",
                "route_familiarity_delta",
                "transfer_bearing_delta",
                "semantic_transfer_stress",
            ]),
            "exit_candidate_replay_state": self._pick_fields(normalized_context.get("exit_candidate_replay_state", {}), [
                "exit_candidate",
                "candidate_label",
                "confirmation_score",
                "exit_decision_pressure",
                "plan_trust",
                "holding_stability",
                "intervention_fitness",
                "intervention_unfit_state",
                "exit_evidence",
                "current_r",
                "adverse_depth_ok",
                "sustained_exit_pressure",
                "candidate_timestamp",
                "candidate_bars_open",
                "candidate_price",
                "candidate_mfe_r",
                "candidate_mae_r",
                "target_expectation_context",
                "tp_reachability",
                "target_path_integrity",
                "expectation_deviation",
                "expectation_break_pressure",
                "expectation_hold_support",
                "target_recovery_potential",
                "target_recovery_momentum",
                "target_recovery_confirmation",
                "break_to_recovery_delta",
                "prior_target_hold_support",
                "prior_tp_reachability",
                "expectation_break_persistence",
                "deep_retrace_recovery_watch",
                "recovery_after_break_watch",
                "entry_route_familiarity",
                "entry_transfer_bearing",
                "current_route_familiarity",
                "current_semantic_shift_pressure",
                "current_transfer_bearing",
                "current_interpretation_quality",
                "current_adaptation_phase",
                "route_familiarity_delta",
                "transfer_bearing_delta",
                "semantic_transfer_stress",
            ]),
            "thought_seed_state": self._pick_fields(normalized_context.get("thought_seed_state", {}), [
                "thought_seed_id",
                "thought_seed_label",
                "thought_trace_strength",
                "thought_recall_potential",
                "thought_maturity",
                "reality_binding_score",
                "thought_confirmation_score",
                "consequence_echo",
                "reorganization_echo",
                "thought_consequence_alignment",
                "thought_consequence_balance",
                "thought_reality_lag",
                "thought_structural_grounding",
                "thought_open_hypothesis_pressure",
                "thought_replay_maturation_pull",
                "thought_distance_maturation_pull",
                "thought_reinterpretation_pull",
                "thought_digestive_replay_pull",
                "thought_digestive_distance_pull",
                "thought_digestive_integration_pull",
                "thought_digestive_returned_trust",
                "trust_return_readiness",
                "thought_digest_state",
                "thought_reifung_direction",
                "semantic_origin_state",
                "borrowed_open_hypothesis_pressure",
                "own_field_binding_pull",
                "own_vs_foreign_margin",
                "borrowed_vs_own_margin",
                "boundary_support_margin",
                "previous_open_hypothesis_learning_state",
                "previous_open_hypothesis_reorganization_posture",
                "hallucination_drift_risk",
                "overthinking_risk",
                "seed_metaregulator_state",
                "emergent_memory_trace",
                "emergent_structure_state",
                "emergent_structure_reading",
                "form_symbol_anchor",
                "mcm_field_anchor",
                "experience_memory_anchor",
                "outcome_anchor",
                "decision",
                "phase",
                "reason",
                "rr_value",
            ]),
            "regulation_snapshot": _compact_snapshot(normalized_context.get("regulation_snapshot", {})) if compact_attempt else self._normalize_record_value(normalized_context.get("regulation_snapshot", {})),
            "state_before": _compact_snapshot(normalized_context.get("state_before", {})) if compact_attempt else self._normalize_record_value(normalized_context.get("state_before", {})),
            "state_after": _compact_snapshot(normalized_context.get("state_after", {})) if compact_attempt else self._normalize_record_value(normalized_context.get("state_after", {})),
            "state_delta": _compact_snapshot(normalized_context.get("state_delta", {})) if compact_attempt else self._normalize_record_value(normalized_context.get("state_delta", {})),
            "world_state": self._pick_fields(normalized_context.get("world_state", {}), [
                "current_price",
                "close",
                "last_price",
                "price",
                "candle_state",
            ]),
            "felt_state": self._pick_fields(normalized_context.get("felt_state", {}), [
                "confidence",
                "urgency",
                "pressure",
                "hesitation",
                "protective_tension",
                "courage_tension",
                "relief_need",
                "regulated_confidence",
            ]),
            "meta_regulation_state": self._pick_fields(normalized_context.get("meta_regulation_state", {}), [
                "decision",
                "observation_priority",
                "uncertainty_load",
                "regulatory_balance",
                "neurochemical_state_label",
                "neurochemical_dominant_tone",
                "dopamine_tone",
                "gaba_inhibition",
                "noradrenaline_arousal",
                "acetylcholine_focus",
                "serotonin_stability",
                "cortisol_load",
                "endorphin_relief",
                "glutamate_activation",
                "neurochemical_load",
                "neurochemical_support",
                "neurochemical_balance",
                "reward_stability_echo",
                "world_shift_evidence",
                "serotonin_carryover_risk",
                "emotional_decoupling",
                "reactive_nervous_drive",
                "nervous_system_overload",
                "escape_action_drive",
                "shock_response_risk",
                "nervous_overload_reflection_need",
                "previous_digest_state",
                "previous_trust_return_readiness",
                "previous_digestive_returned_trust",
                "previous_emergent_structure_state",
                "previous_confirmed_structure_protection",
                "trust_return_open_hypothesis_load",
                "trust_return_context_instability",
                "trust_return_motor_contact_strength",
                "trust_return_act_bridge",
                "trust_return_motor_heat",
                "trust_return_stabilization_need",
                "trust_return_focus_pull",
                "trust_return_motor_mode",
                "active_context_self_certainty",
                "nervous_context_overcoupling",
                "own_field_identity_strength",
                "foreign_semantic_pressure",
                "adopted_language_pressure",
                "self_foreign_boundary_clarity",
                "semantic_origin_conflict",
                "own_vs_foreign_margin",
                "borrowed_vs_own_margin",
                "boundary_support_margin",
                "semantic_origin_state",
                "conscious_perception_state",
                "inner_posture_state",
                "arousal_load",
                "curiosity_tone",
                "fatigue_tone",
                "calm_tone",
                "stimulus_field_effect",
                "inner_impact_trace",
                "perceived_field_change",
                "felt_afterimage",
                "object_release_state",
                "inner_outer_reflection",
                "perceptual_distance",
                "object_contact_depth",
                "field_attachment",
                "release_capacity",
                "selective_attention",
                "background_containment",
                "reflective_distance",
                "inner_outer_alignment",
                "engaged_effort",
                "effort_state",
                "effort_learning_pull",
                "effort_reorganization_pressure",
                "pre_action_reorganization_pressure",
                "pre_action_context_selectivity",
                "strategic_window_state",
                "strategic_pressure_interpretation",
                "strategic_patience",
                "lookback_bearing_capacity",
                "area_bearing_quality",
                "area_order_intention",
                "active_mcm_contact_state",
                "contact_posture",
                "contact_interest",
                "contact_focus_pull",
                "contact_resonance_probe",
                "outer_inner_resonance",
                "outer_inner_coherence",
                "inner_change_from_contact",
                "contact_carrying_quality",
                "contact_overcoupling_risk",
                "contact_release_readiness",
                "contact_deepen_pull",
                "contact_replay_pull",
                "contact_curiosity",
                "contact_felt_shift",
                "contact_selected_depth",
                "contact_salience",
                "overcoupled_touch_score",
                "release_contact_score",
                "deepening_contact_score",
                "resonant_contact_score",
                "reflective_contact_score",
                "curious_touch_score",
                "contact_action_maturity",
                "contact_bearing_gap",
                "contact_impulse_vs_bearing",
                "contact_learning_need",
                "contact_reality_check",
                "contact_regime_mismatch",
                "contact_stability_carryover",
                "contact_context_maturity",
                "contact_context_reframe_need",
                "previous_packet_label",
                "previous_packet_process_reward",
                "previous_packet_reorganization_need",
                "diffuse_open_development_pressure",
                "posture_development_hint",
                "regulated_courage",
                "courage_gap",
                "action_inhibition",
                "action_clearance",
                "pre_action_phase",
                "dominant_tension_cause",
                "known_form_support",
                "route_familiarity",
                "semantic_shift_pressure",
                "transfer_bearing",
                "interpretation_quality",
                "adaptation_phase",
                "trust_transfer_base",
                "trust_transfer_support",
                "transfer_maturity_gap",
                "trust_transfer_mode",
                "transfer_break_fatigue",
                "transfer_recovery_need",
                "transfer_break_trigger",
                "transfer_break_ready",
                "visual_blind_action_load",
                "visual_action_uncertainty",
                "visual_object_binding",
                "visual_grounding_strength",
                "visual_resonance_unbound",
                "visual_grounding_gap",
                "visual_grounding_need",
                "visual_rational_observation_support",
                "visual_grounding_state",
                "uncertain_form_family_state",
                "uncertain_form_exposure",
                "uncertainty_familiarity",
                "variant_similarity",
                "variant_spread",
                "variant_learning_pressure",
                "variant_bearing_memory",
                "form_symbol_semantic_density",
                "form_symbol_semantic_compression",
                "form_symbol_semantic_coherence",
                "form_symbol_semantic_learning_need",
                "form_symbol_semantic_action_nearness",
                "form_symbol_semantic_primary_layer",
                "form_symbol_semantic_layer_count",
                "form_symbol_semantic_packet_state",
                "form_symbol_semantic_profile",
                "hypothesis_observed_outcome",
                "hypothesis_confirmation_without_action",
                "hypothesis_rejection_without_action",
                "hypothesis_neutral_without_action",
                "hypothesis_observation_maturity",
                "possibility_maturity",
                "possibility_caution",
                "possibility_action_support",
                "possibility_reality_check_need",
                "mcm_possibility_field_state",
                "possibility_field_state",
                "possibility_observer_state",
                "possibility_dominant_variant_id",
                "possibility_dominant_kind",
                "possibility_dominant_direction",
                "possibility_dominant_support",
                "possibility_openness",
                "possibility_collapse_pressure",
                "possibility_reflection_pull",
                "possibility_observation_pull",
                "possibility_doppler_energy",
                "possibility_future_variant_pressure",
                "possibility_form_mcm_fit",
                "possibility_memory_fit",
                "possibility_observation_depth",
                "possibility_reality_contact",
                "possibility_variant_maturity",
                "possibility_variant_trust",
                "possibility_variant_caution",
                "possibility_collapse_reason",
                "possibility_collapse_reversibility",
                "possibility_memory_return",
                "hypothesis_trust_score",
                "hypothesis_trust_priority",
                "hypothesis_frustration_risk",
                "hypothesis_distance_risk",
                "hypothesis_trust_state",
                "dominant_hypothesis_trust_key",
                "dominant_hypothesis_trust_score",
            ]),            
            "strategic_window_state": self._pick_fields(normalized_context.get("strategic_window_state", {}), [
                "strategic_window_state",
                "lookback_window_size",
                "lookback_load",
                "lookback_relevance",
                "lookback_bearing_capacity",
                "replay_budget",
                "zoom_budget",
                "old_structure_carryover_risk",
                "strategic_pressure_interpretation",
                "strategic_patience",
                "area_candidate_count",
                "area_focus_id",
                "area_price_low",
                "area_price_high",
                "area_distance_from_price",
                "area_structural_density",
                "area_energy_compression",
                "area_mcm_resonance",
                "area_memory_pull",
                "area_bearing_quality",
                "area_zoom_need",
                "area_zoom_clarity",
                "area_replay_fit",
                "area_patience_quality",
                "area_order_intention",
                "area_invalidity_pressure",
            ]),
            "active_mcm_contact_state": self._pick_fields(
                normalized_context.get("active_mcm_contact_state", normalized_context.get("meta_regulation_state", {}).get("active_mcm_contact", {})),
                [
                    "active_mcm_contact_state",
                    "contact_posture",
                    "contact_interest",
                    "contact_focus_pull",
                    "contact_resonance_probe",
                    "outer_inner_resonance",
                    "outer_inner_coherence",
                    "inner_change_from_contact",
                    "contact_carrying_quality",
                    "contact_overcoupling_risk",
                    "contact_release_readiness",
                    "contact_deepen_pull",
                    "contact_replay_pull",
                    "contact_curiosity",
                    "contact_felt_shift",
                    "contact_selected_depth",
                    "contact_salience",
                    "overcoupled_touch_score",
                    "release_contact_score",
                    "deepening_contact_score",
                    "resonant_contact_score",
                    "reflective_contact_score",
                    "curious_touch_score",
                    "contact_action_maturity",
                    "contact_bearing_gap",
                    "contact_impulse_vs_bearing",
                    "contact_learning_need",
                    "contact_reality_check",
                    "contact_regime_mismatch",
                    "contact_stability_carryover",
                    "contact_context_maturity",
                    "contact_context_reframe_need",
                ],
            ),
            "expectation_state": self._pick_fields(normalized_context.get("expectation_state", {}), [
                "entry_expectation",
                "target_expectation",
                "approach_pressure",
                "pressure_release",
                "experience_regulation",
                "reflection_maturity",
                "load_bearing_capacity",
            ]),
            "neurochemical_state": self._pick_fields(
                normalized_context.get("neurochemical_state", normalized_context.get("meta_regulation_state", {}).get("neurochemical_state", {})),
                [
                    "neurochemical_state_label",
                    "neurochemical_dominant_tone",
                    "dopamine_tone",
                    "gaba_inhibition",
                    "noradrenaline_arousal",
                    "acetylcholine_focus",
                    "serotonin_stability",
                    "cortisol_load",
                    "endorphin_relief",
                    "glutamate_activation",
                    "neurochemical_load",
                    "neurochemical_support",
                    "neurochemical_balance",
                    "reward_stability_echo",
                    "world_shift_evidence",
                    "serotonin_carryover_risk",
                    "emotional_decoupling",
                    "reactive_nervous_drive",
                ],
            ),
            "form_symbol_state": self._pick_fields(normalized_context.get("form_symbol_state", {}), [
                "form_symbol_id",
                "form_symbol_scope",
                "form_symbol_development_quality",
                "form_symbol_action_affinity",
                "form_symbol_action_binding",
                "form_symbol_observation_affinity",
                "form_symbol_observation_binding",
                "form_symbol_reframe_binding",
                "form_symbol_learning_trust",
                "form_symbol_action_trust",
                "form_symbol_caution_trust",
                "form_symbol_contact_maturity",
                "form_symbol_contact_utility",
                "form_symbol_contact_pain_memory",
                "form_symbol_contact_carefulness",
                "form_symbol_contact_burden_evidence",
                "form_symbol_contact_utility_evidence",
                "form_symbol_contact_learning_state",
                "form_symbol_compound_id",
                "form_symbol_compound_development_quality",
                "form_symbol_compound_action_affinity",
                "form_symbol_compound_observation_affinity",
                "form_symbol_compound_reframe_potential",
                "form_symbol_compound_learning_trust",
                "form_symbol_compound_action_trust",
                "form_symbol_compound_caution_trust",
                "uncertain_form_family_state",
                "uncertain_form_exposure",
                "uncertainty_familiarity",
                "variant_similarity",
                "variant_spread",
                "variant_learning_pressure",
                "variant_bearing_memory",
                "form_symbol_semantic_density",
                "form_symbol_semantic_compression",
                "form_symbol_semantic_coherence",
                "form_symbol_semantic_learning_need",
                "form_symbol_semantic_action_nearness",
                "form_symbol_semantic_primary_layer",
                "form_symbol_semantic_layer_count",
                "form_symbol_semantic_packet_state",
                "form_symbol_semantic_profile",
            ]),
            "trade_plan": self._pick_fields(normalized_context.get("trade_plan", {}), [
                "decision",
                "entry_price",
                "sl_price",
                "tp_price",
                "rr_value",
                "risk_model_score",
                "reward_model_score",
                "entry_mode",
                "contact_entry_mode",
                "impulse_entry_price",
                "contact_entry_price",
                "strategic_entry_price",
                "area_contact_weight",
                "area_contact_fit",
                "area_contact_intention",
                "contact_entry_weight",
                "contact_entry_fit",
                "strategic_entry_weight",
                "strategic_entry_fit",
                "area_contact_distance_fit",
                "area_motor_intention",
                "area_motor_distance_fit",
                "impulse_perception_pressure",
                "impulse_entry_intention",
                "area_order_geometry_intention",
                "area_entry_intention",
                "entry_contact_pressure",
                "entry_choice_pressure",
                "entry_choice_conflict",
                "entry_contact_bearing",
                "entry_choice_bearing",
                "area_bearing_quality",
                "area_contact_timing_fit",
                "area_spacetime_fit",
                "area_present_contact",
                "area_invalidity_pressure",
                "area_afterimage",
                "area_contact_readiness",
                "area_direct_readiness",
                "area_contact_restraint",
                "area_motor_restraint",
                "entry_geometry_bearing",
                "entry_geometry_state",
                "pre_geometry_thought_bearing",
                "pre_geometry_felt_bearing",
                "pre_geometry_reality_bearing",
                "pre_geometry_preference_bearing",
                "organic_contact_bearing",
                "entry_contact_state",
                "entry_choice_state",
                "entry_preference_state",
                "entry_choice_basis",
                "entry_contact_option_count",
                "selected_entry_offer_score",
                "selected_entry_learned_fit",
                "selected_entry_preference_key",
                "selected_entry_preference_trust",
                "selected_entry_preference_caution",
                "selected_entry_preference_maturity",
                "selected_entry_preference_utility",
                "selected_entry_property_profile_id",
                "selected_entry_property_profile_similarity",
                "selected_entry_property_profile_trust",
                "selected_entry_property_profile_caution",
                "selected_entry_property_profile_maturity",
                "selected_entry_property_profile_utility",
                "selected_memory_caution_pressure",
                "selected_memory_bearing_pressure",
                "mature_careful_contact_pressure",
                "entry_contact_options",
                "contact_learning_state",
                "learned_contact_fit",
                "entry_choice_sync",
                "inner_action_consent",
                "inner_action_support",
                "inner_action_no",
                "inner_action_consent_state",
                "strategy_confirmation",
                "strategy_rejection",
                "strategy_trust_bearing",
                "strategy_context_bearing",
                "raw_strategy_contradiction_pressure",
                "strategy_contradiction_pressure",
                "thought_confirmation_bearing",
                "thought_rejection_pressure",
                "thought_trust_bearing",
                "contact_context_bearing",
                "real_area_contact_bearing",
                "visual_reality_bearing",
                "felt_reality_bearing",
                "form_mcm_reality_fit",
                "raw_thought_contradiction_pressure",
                "thought_contradiction_pressure",
                "open_hypothesis_reality_permission",
                "possibility_contact_bearing",
                "dominant_hypothesis_reality_bearing",
                "current_hypothesis_reality_bearing",
                "hypothesis_reality_bearing",
                "open_hypothesis_reality_bearing",
                "open_hypothesis_reality_fit",
                "order_geometry_source",
                "impulse_role",
                "strategic_area_focus_id",
                "strategic_area_price_low",
                "strategic_area_price_high",
                "strategic_entry_location",
                "entry_validity_band",
            ]),
            "structure_perception_state": self._pick_fields(normalized_context.get("structure_perception_state", {}), [
                "structure_seen",
                "swing_high_strength",
                "swing_low_strength",
                "zone_proximity",
                "structure_stability",
                "structure_quality",
                "stress_relief_potential",
                "context_confidence",
            ]),
            "signal": self._pick_fields(normalized_context.get("signal", {}), [
                "signature_bias",
                "signature_block",
                "signature_quality",
                "signature_distance",
                "context_cluster_id",
                "context_cluster_bias",
                "context_cluster_quality",
                "context_cluster_distance",
                "context_cluster_block",
                "inhibition_level",
                "habituation_level",
                "competition_bias",
                "observation_mode",
                "long_score",
                "short_score",
            ]),
            "market_hearing_state": self._pick_fields(normalized_context.get("market_hearing_state", {}), [
                "loudness",
                "frequency_hz",
                "compression",
                "tone",
            ]),
            "area_perception_profile": self._pick_fields(normalized_context.get("area_perception_profile", {}), [
                "area_profile_id",
                "area_price_low",
                "area_price_high",
                "area_price_mid",
                "area_attention_need",
                "area_felt_depth",
                "area_multisensory_coherence",
                "area_overcoupling_risk",
                "area_profile_state",
                "area_profile_role",
            ]),
        }
        return {key: value for key, value in compact.items() if value}
    # ─────────────────────────────────────────────
    def _save(self, force: bool = False):
        try:
            if not bool(force):
                every_n = max(1, int(getattr(Config, "TRADE_STATS_JSON_SAVE_EVERY_N", 1) or 1))
                self._json_save_seq = int(getattr(self, "_json_save_seq", 0) or 0) + 1
                if every_n > 1 and (self._json_save_seq % every_n) != 0:
                    return

            if not bool(getattr(self, "_kpi_rebuild_before_save", False)):
                self._kpi_rebuild_before_save = True
                try:
                    self._rebuild_kpi_summary()
                finally:
                    self._kpi_rebuild_before_save = False

            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            write_start = time.perf_counter()
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
            self._write_sensory_balance_protocol()
            elapsed_ms = (time.perf_counter() - write_start) * 1000.0
            try:
                bytes_written = int(os.path.getsize(self.path))
            except Exception:
                bytes_written = 0
            dbr_file_write_profile(
                self.path,
                elapsed_ms,
                bytes_written=bytes_written,
                operation="trade_stats_json_dump",
                extra=f"force={bool(force)}|trades={int(self.data.get('trades', 0) or 0)}|attempts={int(self.data.get('attempts', 0) or 0)}",
            )
        except Exception:
            pass

    # ─────────────────────────────────────────────
    def _extract_structure_quality(self, context: dict) -> float:
        ctx = dict(context or {})
        world_state = dict(ctx.get("world_state", {}) or {})
        structure = dict(ctx.get("structure_perception_state", {}) or {})
        bearing_context = dict(ctx.get("bearing_context", {}) or {})

        if not structure and isinstance(world_state.get("structure_perception_state"), dict):
            structure = dict(world_state.get("structure_perception_state", {}) or {})

        if not structure and isinstance(ctx.get("outer_visual_perception_state"), dict):
            structure = dict(ctx.get("outer_visual_perception_state", {}) or {})

        if not structure and isinstance(ctx.get("context"), dict):
            nested_context = dict(ctx.get("context", {}) or {})
            structure = dict(nested_context.get("structure_perception_state", {}) or {})
            if not structure:
                bearing_context = dict(nested_context.get("bearing_context", {}) or {})

        try:
            if "structure_quality" in structure:
                return float(structure.get("structure_quality", 0.0) or 0.0)
        except Exception:
            pass

        try:
            return float(bearing_context.get("structure_quality", 0.0) or 0.0)
        except Exception:
            return 0.0

    # ─────────────────────────────────────────────
    def _extract_attempt_side_fast(self, context: dict) -> str:
        ctx = dict(context or {})
        nested = dict(ctx.get("context", {}) or {}) if isinstance(ctx.get("context", {}), dict) else {}
        for source in (
            ctx.get("trade_plan", {}),
            nested.get("trade_plan", {}),
            ctx.get("meta_regulation_state", {}),
            nested.get("meta_regulation_state", {}),
        ):
            if not isinstance(source, dict):
                continue
            side = str(source.get("decision", source.get("proposed_decision", "")) or "").strip().upper()
            if side in ("LONG", "SHORT"):
                return side
        return "-"

    def _attempt_value_fast(self, context: dict, key: str, default=0.0):
        ctx = dict(context or {})
        nested = dict(ctx.get("context", {}) or {}) if isinstance(ctx.get("context", {}), dict) else {}
        sources = (
            ctx,
            nested,
            ctx.get("field_state", {}) if isinstance(ctx.get("field_state", {}), dict) else {},
            nested.get("field_state", {}) if isinstance(nested.get("field_state", {}), dict) else {},
            ctx.get("meta_regulation_state", {}) if isinstance(ctx.get("meta_regulation_state", {}), dict) else {},
            nested.get("meta_regulation_state", {}) if isinstance(nested.get("meta_regulation_state", {}), dict) else {},
            ctx.get("trade_plan", {}) if isinstance(ctx.get("trade_plan", {}), dict) else {},
            nested.get("trade_plan", {}) if isinstance(nested.get("trade_plan", {}), dict) else {},
            ctx.get("active_mcm_contact_state", {}) if isinstance(ctx.get("active_mcm_contact_state", {}), dict) else {},
            nested.get("active_mcm_contact_state", {}) if isinstance(nested.get("active_mcm_contact_state", {}), dict) else {},
            ctx.get("market_hearing_state", {}) if isinstance(ctx.get("market_hearing_state", {}), dict) else {},
            nested.get("market_hearing_state", {}) if isinstance(nested.get("market_hearing_state", {}), dict) else {},
            ctx.get("visual_sight_state", {}) if isinstance(ctx.get("visual_sight_state", {}), dict) else {},
            nested.get("visual_sight_state", {}) if isinstance(nested.get("visual_sight_state", {}), dict) else {},
            ctx.get("visual_cortex_state", {}) if isinstance(ctx.get("visual_cortex_state", {}), dict) else {},
            nested.get("visual_cortex_state", {}) if isinstance(nested.get("visual_cortex_state", {}), dict) else {},
            ctx.get("area_perception_profile", {}) if isinstance(ctx.get("area_perception_profile", {}), dict) else {},
            nested.get("area_perception_profile", {}) if isinstance(nested.get("area_perception_profile", {}), dict) else {},
            (ctx.get("perception_state", {}) or {}).get("area_perception_profile", {}) if isinstance(ctx.get("perception_state", {}), dict) else {},
            (nested.get("perception_state", {}) or {}).get("area_perception_profile", {}) if isinstance(nested.get("perception_state", {}), dict) else {},
            ctx.get("outer_visual_perception_state", {}) if isinstance(ctx.get("outer_visual_perception_state", {}), dict) else {},
            nested.get("outer_visual_perception_state", {}) if isinstance(nested.get("outer_visual_perception_state", {}), dict) else {},
            ctx.get("experience", {}) if isinstance(ctx.get("experience", {}), dict) else {},
            nested.get("experience", {}) if isinstance(nested.get("experience", {}), dict) else {},
        )
        for source in sources:
            if not isinstance(source, dict) or key not in source:
                continue
            try:
                return float(source.get(key, default) or default)
            except Exception:
                return default
        return default

    def _on_attempt_fast_path(self, status_key: str, context: dict = None) -> bool:
        if not bool(getattr(Config, "TRADE_STATS_FAST_ATTEMPT_PATH", False)):
            return False
        if self._should_write_attempt_record(status_key):
            return False

        ctx = dict(context or {})
        nested = dict(ctx.get("context", {}) or {}) if isinstance(ctx.get("context", {}), dict) else {}
        side = self._extract_attempt_side_fast(ctx)
        self.data["attempts"] = int(self.data.get("attempts", 0) or 0) + 1
        if side == "LONG":
            self.data["attempts_long"] = int(self.data.get("attempts_long", 0) or 0) + 1
        elif side == "SHORT":
            self.data["attempts_short"] = int(self.data.get("attempts_short", 0) or 0) + 1

        if status_key == "submitted":
            self.data["attempts_submitted"] = int(self.data.get("attempts_submitted", 0) or 0) + 1
            if side == "LONG":
                self.data["attempts_submitted_long"] = int(self.data.get("attempts_submitted_long", 0) or 0) + 1
            elif side == "SHORT":
                self.data["attempts_submitted_short"] = int(self.data.get("attempts_submitted_short", 0) or 0) + 1
        elif status_key == "filled":
            self.data["attempts_filled"] = int(self.data.get("attempts_filled", 0) or 0) + 1
            if side == "LONG":
                self.data["attempts_filled_long"] = int(self.data.get("attempts_filled_long", 0) or 0) + 1
            elif side == "SHORT":
                self.data["attempts_filled_short"] = int(self.data.get("attempts_filled_short", 0) or 0) + 1
        elif status_key == "cancelled":
            self.data["attempts_cancelled"] = int(self.data.get("attempts_cancelled", 0) or 0) + 1
        elif status_key == "timeout":
            self.data["attempts_timeout"] = int(self.data.get("attempts_timeout", 0) or 0) + 1
        elif status_key in ("blocked", "blocked_value_gate"):
            self.data["attempts_blocked"] = int(self.data.get("attempts_blocked", 0) or 0) + 1
        elif status_key == "skipped":
            self.data["attempts_skipped"] = int(self.data.get("attempts_skipped", 0) or 0) + 1
        elif status_key == "observed_only":
            self.data["attempts_observed"] = int(self.data.get("attempts_observed", 0) or 0) + 1
        elif status_key == "replanned":
            self.data["attempts_replanned"] = int(self.data.get("attempts_replanned", 0) or 0) + 1
        elif status_key == "withheld":
            self.data["attempts_withheld"] = int(self.data.get("attempts_withheld", 0) or 0) + 1

        structure_quality = self._extract_structure_quality(ctx)
        if structure_quality >= 0.55:
            self.data["attempt_structure_zone"] = int(self.data.get("attempt_structure_zone", 0) or 0) + 1
            structure_bucket = "zone"
        else:
            self.data["attempt_non_structure_zone"] = int(self.data.get("attempt_non_structure_zone", 0) or 0) + 1
            structure_bucket = "non_zone"

        if status_key in ("observed_only", "replanned", "withheld", "skipped"):
            self._register_observation_learning(
                status_key,
                ctx,
                structure_quality,
                structure_bucket,
            )

        meta = ctx.get("meta_regulation_state", {}) if isinstance(ctx.get("meta_regulation_state", {}), dict) else {}
        visual_sight_state = {}
        for source in (
            ctx.get("visual_sight_state", {}),
            nested.get("visual_sight_state", {}),
            (ctx.get("outer_visual_perception_state", {}) or {}).get("visual_sight_state", {}) if isinstance(ctx.get("outer_visual_perception_state", {}), dict) else {},
            (nested.get("outer_visual_perception_state", {}) or {}).get("visual_sight_state", {}) if isinstance(nested.get("outer_visual_perception_state", {}), dict) else {},
            (ctx.get("visual_market_state", {}) or {}).get("visual_sight_state", {}) if isinstance(ctx.get("visual_market_state", {}), dict) else {},
            (nested.get("visual_market_state", {}) or {}).get("visual_sight_state", {}) if isinstance(nested.get("visual_market_state", {}), dict) else {},
        ):
            if isinstance(source, dict) and source:
                visual_sight_state = dict(source)
                break
        visual_cortex_state = {}
        for source in (
            ctx.get("visual_cortex_state", {}),
            nested.get("visual_cortex_state", {}),
            (ctx.get("outer_visual_perception_state", {}) or {}).get("visual_cortex_state", {}) if isinstance(ctx.get("outer_visual_perception_state", {}), dict) else {},
            (nested.get("outer_visual_perception_state", {}) or {}).get("visual_cortex_state", {}) if isinstance(nested.get("outer_visual_perception_state", {}), dict) else {},
            (ctx.get("visual_market_state", {}) or {}).get("visual_cortex_state", {}) if isinstance(ctx.get("visual_market_state", {}), dict) else {},
            (nested.get("visual_market_state", {}) or {}).get("visual_cortex_state", {}) if isinstance(nested.get("visual_market_state", {}), dict) else {},
        ):
            if isinstance(source, dict) and source:
                visual_cortex_state = dict(source)
                break
        area_perception_profile = {}
        for source in (
            ctx.get("area_perception_profile", {}),
            nested.get("area_perception_profile", {}),
            (ctx.get("perception_state", {}) or {}).get("area_perception_profile", {}) if isinstance(ctx.get("perception_state", {}), dict) else {},
            (nested.get("perception_state", {}) or {}).get("area_perception_profile", {}) if isinstance(nested.get("perception_state", {}), dict) else {},
        ):
            if isinstance(source, dict) and source:
                area_perception_profile = dict(source)
                break
        recent = list(self.data.get("recent_attempts", []) or [])
        recent.append({
            "status": status_key or "unknown",
            "side": str(side),
            "structure_quality": float(structure_quality),
            "structure_bucket": structure_bucket,
            "pressure_to_capacity": float(self._attempt_value_fast(ctx, "pressure_to_capacity", 0.0)),
            "field_stimulus_density": float(self._attempt_value_fast(ctx, "field_stimulus_density", 0.0)),
            "regulatory_load": float(self._attempt_value_fast(ctx, "regulatory_load", 0.0)),
            "action_capacity": float(self._attempt_value_fast(ctx, "action_capacity", 0.0)),
            "recovery_need": float(self._attempt_value_fast(ctx, "recovery_need", 0.0)),
            "survival_pressure": float(self._attempt_value_fast(ctx, "survival_pressure", 0.0)),
            "pressure_release": float(self._attempt_value_fast(ctx, "pressure_release", 0.0)),
            "load_bearing_capacity": float(self._attempt_value_fast(ctx, "load_bearing_capacity", 0.0)),
            "state_stability": float(self._attempt_value_fast(ctx, "state_stability", 0.0)),
            "capacity_reserve": float(self._attempt_value_fast(ctx, "capacity_reserve", 0.0)),
            "recovery_balance": float(self._attempt_value_fast(ctx, "recovery_balance", 0.0)),
            "visual_blind_action_load": float(self._attempt_value_fast(ctx, "visual_blind_action_load", 0.0)),
            "visual_object_binding": float(self._attempt_value_fast(ctx, "visual_object_binding", 0.0)),
            "visual_grounding_strength": float(self._attempt_value_fast(ctx, "visual_grounding_strength", 0.0)),
            "visual_grounding_gap": float(self._attempt_value_fast(ctx, "visual_grounding_gap", 0.0)),
            "visual_sight_label": str(visual_sight_state.get("sight_label", "") or ""),
            "visual_form_family": str(visual_sight_state.get("form_family", "") or ""),
            "visual_contact_candidate": float(visual_sight_state.get("contact_candidate", 0.0) or 0.0),
            "visual_background_load": float(visual_sight_state.get("background_load", 0.0) or 0.0),
            "visual_depth": float(visual_sight_state.get("depth", 0.0) or 0.0),
            "visual_cortex_label": str(visual_cortex_state.get("visual_cortex_label", "") or ""),
            "dominant_visual_object": str(visual_cortex_state.get("dominant_visual_object", "") or ""),
            "visual_object_presence": float(visual_cortex_state.get("object_presence", 0.0) or 0.0),
            "visual_object_clarity": float(visual_cortex_state.get("object_clarity", 0.0) or 0.0),
            "visual_relation_coherence": float(visual_cortex_state.get("relation_coherence", 0.0) or 0.0),
            "visual_readiness": float(visual_cortex_state.get("visual_readiness", 0.0) or 0.0),
            "visual_relation_label": str(visual_cortex_state.get("visual_relation_label", "") or ""),
            "visual_lifecycle_label": str(visual_cortex_state.get("visual_lifecycle_label", "") or ""),
            "visual_object_side": str(visual_cortex_state.get("visual_object_side", "") or ""),
            "visual_object_distance": float(visual_cortex_state.get("visual_object_distance", 0.0) or 0.0),
            "visual_contact_nearness": float(visual_cortex_state.get("visual_contact_nearness", 0.0) or 0.0),
            "visual_lifecycle_stability": float(visual_cortex_state.get("visual_lifecycle_stability", 0.0) or 0.0),
            "visual_lifecycle_rejection": float(visual_cortex_state.get("visual_lifecycle_rejection", 0.0) or 0.0),
            "visual_lifecycle_dissolution": float(visual_cortex_state.get("visual_lifecycle_dissolution", 0.0) or 0.0),
            "visual_object_binding_quality": float(visual_cortex_state.get("visual_object_binding_quality", 0.0) or 0.0),
            "visual_cortex_grounding": float(self._attempt_value_fast(ctx, "visual_cortex_grounding", 0.0)),
            "area_profile_state": str(area_perception_profile.get("area_profile_state", "") or ""),
            "area_multisensory_coherence": float(area_perception_profile.get("area_multisensory_coherence", 0.0) or 0.0),
            "area_attention_need": float(area_perception_profile.get("area_attention_need", 0.0) or 0.0),
            "area_felt_depth": float(area_perception_profile.get("area_felt_depth", 0.0) or 0.0),
            "area_overcoupling_risk": float(area_perception_profile.get("area_overcoupling_risk", 0.0) or 0.0),
            "outer_inner_coherence": float(self._attempt_value_fast(ctx, "outer_inner_coherence", 0.0)),
            "contact_carrying_quality": float(self._attempt_value_fast(ctx, "contact_carrying_quality", 0.0)),
            "contact_overcoupling_risk": float(self._attempt_value_fast(ctx, "contact_overcoupling_risk", 0.0)),
            "market_loudness": float(max(
                self._attempt_value_fast(ctx, "market_loudness", 0.0),
                self._attempt_value_fast(ctx, "loudness", 0.0),
            )),
            "market_frequency_hz": float(max(
                self._attempt_value_fast(ctx, "market_frequency_hz", 0.0),
                self._attempt_value_fast(ctx, "frequency_hz", 0.0),
            )),
            "market_hearing_compression": float(max(
                self._attempt_value_fast(ctx, "market_hearing_compression", 0.0),
                self._attempt_value_fast(ctx, "compression", 0.0),
            )),
            "energy_coherence_bearing": float(self._attempt_value_fast(ctx, "energy_coherence_bearing", 0.0)),
            "mcm_axis_displacement": float(self._attempt_value_fast(ctx, "mcm_axis_displacement", 0.0)),
            "mcm_axis_field_position": float(self._attempt_value_fast(ctx, "mcm_axis_field_position", 0.0)),
            "mcm_axis_tension": float(self._attempt_value_fast(ctx, "mcm_axis_tension", 0.0)),
            "mcm_axis_state": str(meta.get("mcm_axis_state", "0") or "0"),
            "thought_confirmation_bearing": float(self._attempt_value_fast(ctx, "thought_confirmation_bearing", 0.0)),
            "thought_rejection_pressure": float(self._attempt_value_fast(ctx, "thought_rejection_pressure", 0.0)),
            "thought_trust_bearing": float(self._attempt_value_fast(ctx, "thought_trust_bearing", 0.0)),
            "thought_contradiction_pressure": float(self._attempt_value_fast(ctx, "thought_contradiction_pressure", 0.0)),
            "inner_action_consent": float(self._attempt_value_fast(ctx, "inner_action_consent", 0.0)),
            "inner_action_support": float(self._attempt_value_fast(ctx, "inner_action_support", 0.0)),
            "inner_action_no": float(self._attempt_value_fast(ctx, "inner_action_no", 0.0)),
            "regulated_courage": float(self._attempt_value_fast(ctx, "regulated_courage", 0.0)),
            "courage_gap": float(self._attempt_value_fast(ctx, "courage_gap", 0.0)),
            "action_inhibition": float(self._attempt_value_fast(ctx, "action_inhibition", 0.0)),
            "action_clearance": float(self._attempt_value_fast(ctx, "action_clearance", 0.0)),
            "pre_action_phase": str(meta.get("pre_action_phase", "") or ""),
        })
        self.data["recent_attempts"] = recent[-80:]
        self._save(force=False)
        return True

    def _extract_observation_price(self, context: dict) -> float:
        ctx = dict(context or {})
        trade_plan = dict(ctx.get("trade_plan", {}) or {})
        nested = dict(ctx.get("context", {}) or {}) if isinstance(ctx.get("context", {}), dict) else {}
        compact_trade_plan = dict(nested.get("trade_plan", {}) or {})

        # Observation learning resolves old hypotheses against the real
        # current market, not against the newly imagined entry geometry.
        for source in (ctx.get("world_state", {}), nested.get("world_state", {})):
            world = dict(source or {}) if isinstance(source, dict) else {}
            candle = dict(world.get("candle_state", {}) or {}) if isinstance(world.get("candle_state", {}), dict) else {}
            for key in ("current_price", "close", "last_price", "price"):
                try:
                    price = float(world.get(key, 0.0) or candle.get(key, 0.0) or 0.0)
                    if price > 0.0:
                        return float(price)
                except Exception:
                    pass
        for source in (trade_plan, compact_trade_plan):
            try:
                price = float(source.get("entry_price", 0.0) or 0.0)
                if price > 0.0:
                    return float(price)
            except Exception:
                pass
        return 0.0

    def _infer_observation_trade_plan(self, context: dict, current_price: float) -> dict:
        ctx = dict(context or {})
        price = float(current_price or 0.0)
        if price <= 0.0:
            return {}

        meta = dict(ctx.get("meta_regulation_state", {}) or {})
        signal = dict(ctx.get("signal", {}) or {})

        side = str(meta.get("decision", "") or "").strip().upper()
        if side not in ("LONG", "SHORT"):
            try:
                long_score = float(signal.get("long_score", 0.0) or 0.0)
                short_score = float(signal.get("short_score", 0.0) or 0.0)
            except Exception:
                long_score = 0.0
                short_score = 0.0
            if max(abs(long_score), abs(short_score)) < 0.08 and abs(long_score - short_score) < 0.04:
                return {}
            side = "LONG" if long_score >= short_score else "SHORT"

        risk_pct = max(0.0015, min(0.012, float(getattr(Config, "BASE_RISK_PCT", 0.0045) or 0.0045)))
        min_rr_floor = max(0.0, float(getattr(Config, "MIN_RR", 1.0) or 1.0))
        target_expectation = float((ctx.get("experience", {}) or {}).get("target_expectation", 0.0) or 0.0)
        load_bearing_capacity = float((ctx.get("experience", {}) or {}).get("load_bearing_capacity", 0.0) or 0.0)
        focus_confidence = float((ctx.get("focus", {}) or {}).get("focus_confidence", 0.0) or 0.0)
        target_lock = float((ctx.get("focus", {}) or {}).get("target_lock", 0.0) or 0.0)
        rr_value = min_rr_floor + max(
            0.0,
            (target_expectation * 0.22)
            + (load_bearing_capacity * 0.16)
            + (focus_confidence * 0.14)
            + (target_lock * 0.12),
        )
        risk_distance = max(price * risk_pct, price * 0.0015)
        reward_distance = risk_distance * rr_value

        if side == "LONG":
            sl_price = price - risk_distance
            tp_price = price + reward_distance
        else:
            sl_price = price + risk_distance
            tp_price = price - reward_distance

        return {
            "decision": str(side),
            "entry_price": float(price),
            "sl_price": float(sl_price),
            "tp_price": float(tp_price),
            "rr_value": float(rr_value),
            "entry_mode": str((ctx.get("trade_plan", {}) or {}).get("entry_mode", ctx.get("entry_mode", "")) or "no_mature_entry_thesis"),
            "contact_entry_mode": str((ctx.get("trade_plan", {}) or {}).get("contact_entry_mode", ctx.get("contact_entry_mode", (ctx.get("trade_plan", {}) or {}).get("entry_mode", ctx.get("entry_mode", "")))) or "no_mature_entry_thesis"),
            "entry_contact_state": str((ctx.get("trade_plan", {}) or {}).get("entry_contact_state", ctx.get("entry_contact_state", (ctx.get("trade_plan", {}) or {}).get("entry_choice_state", ctx.get("entry_choice_state", "")))) or "no_entry_choice"),
            "entry_choice_state": str((ctx.get("trade_plan", {}) or {}).get("entry_choice_state", ctx.get("entry_choice_state", "")) or "no_entry_choice"),
            "area_contact_focus_id": str((ctx.get("trade_plan", {}) or {}).get("area_contact_focus_id", ctx.get("area_contact_focus_id", (ctx.get("trade_plan", {}) or {}).get("strategic_area_focus_id", ctx.get("strategic_area_focus_id", "")))) or ""),
            "strategic_area_focus_id": str((ctx.get("trade_plan", {}) or {}).get("strategic_area_focus_id", ctx.get("strategic_area_focus_id", "")) or ""),
            "area_contact_location": str((ctx.get("trade_plan", {}) or {}).get("area_contact_location", ctx.get("area_contact_location", (ctx.get("trade_plan", {}) or {}).get("strategic_entry_location", ctx.get("strategic_entry_location", "")))) or ""),
            "strategic_entry_location": str((ctx.get("trade_plan", {}) or {}).get("strategic_entry_location", ctx.get("strategic_entry_location", "")) or ""),
            "inferred_observation_plan": True,
        }

    def _refresh_observation_learning_summary(self):
        learning = refresh_observation_learning_summary(
            self.data.get("observation_learning", {}) or {},
            self.data.get("pending_observations", []) or [],
        )
        self.data["observation_learning"] = dict(learning)
        return dict(learning)

    def _resolve_pending_observations(self, current_price: float):
        result = resolve_pending_observations(
            pending_observations=self.data.get("pending_observations", []) or [],
            learning=self.data.get("observation_learning", {}) or {},
            recent_observation_learning=self.data.get("recent_observation_learning", []) or [],
            current_price=float(current_price or 0.0),
            now_attempt=int(self.data.get("attempts", 0) or 0),
            horizon=max(3, int(getattr(Config, "OBSERVATION_LEARNING_HORIZON_ATTEMPTS", 24) or 24)),
        )
        self.data["pending_observations"] = list(result.get("pending_observations", []) or [])
        self.data["recent_observation_learning"] = list(result.get("recent_observation_learning", []) or [])
        self.data["observation_learning"] = dict(result.get("observation_learning", {}) or {})

    def _register_observation_learning(self, status_key: str, context: dict, structure_quality: float, structure_bucket: str):
        compact_context = self._compact_context(context or {})
        current_price = self._extract_observation_price(compact_context)
        self._resolve_pending_observations(current_price)

        status = str(status_key or "").strip().lower()
        if status not in ("observed_only", "replanned", "withheld", "skipped"):
            return

        learning = dict(self.data.get("observation_learning", {}) or {})
        if str(structure_bucket or "").strip().lower() != "non_zone":
            learning["zone_observations"] = int(learning.get("zone_observations", 0) or 0) + 1

        trade_plan = dict(compact_context.get("trade_plan", {}) or {})
        side = str(trade_plan.get("decision", "") or "").strip().upper()
        entry_price = float(trade_plan.get("entry_price", 0.0) or 0.0)
        tp_price = float(trade_plan.get("tp_price", 0.0) or 0.0)
        sl_price = float(trade_plan.get("sl_price", 0.0) or 0.0)
        rr_value = float(trade_plan.get("rr_value", 0.0) or 0.0)
        if side not in ("LONG", "SHORT") or entry_price <= 0.0 or tp_price <= 0.0 or sl_price <= 0.0:
            # A held/observed posture is not automatically a concrete trade
            # hypothesis. Only real entry geometry may mature as "would have
            # carried / would have hurt"; otherwise generic observation floods
            # the thought memory with artificial trades.
            return
        if rr_value <= 0.0:
            rr_value = abs(tp_price - entry_price) / max(abs(entry_price - sl_price), 1e-9)

        form_state = dict(compact_context.get("form_symbol_state", {}) or {})
        meta_state = dict(compact_context.get("meta_regulation_state", {}) or {})
        possibility_state = dict(
            compact_context.get(
                "possibility_field_state",
                meta_state.get("mcm_possibility_field_state", {}),
            )
            or {}
        )
        thought_seed = dict(compact_context.get("thought_seed_state", {}) or {})
        possibility_direction = str(
            possibility_state.get(
                "possibility_dominant_direction",
                meta_state.get("possibility_dominant_direction", side),
            )
            or side
        ).strip().upper()
        possibility_variant_id = str(
            possibility_state.get(
                "possibility_dominant_variant_id",
                meta_state.get("possibility_dominant_variant_id", ""),
            )
            or ""
        ).strip()
        possibility_reason = str(
            possibility_state.get(
                "possibility_collapse_reason",
                meta_state.get("possibility_collapse_reason", ""),
            )
            or ""
        ).strip()
        possibility_family_key = (
            f"{possibility_direction}:{possibility_variant_id}:{possibility_reason}"
            if possibility_variant_id
            else ""
        )
        pending = list(self.data.get("pending_observations", []) or [])
        pending.append({
            "attempt_index": int(self.data.get("attempts", 0) or 0),
            "timestamp": self.data.get("current_timestamp"),
            "status": str(status),
            "rejection_reason": str(compact_context.get("rejection_reason", meta_state.get("rejection_reason", "")) or ""),
            "inner_action_consent_state": str(compact_context.get("inner_action_consent_state", meta_state.get("inner_action_consent_state", "")) or ""),
            "inner_action_consent": float(compact_context.get("inner_action_consent", meta_state.get("inner_action_consent", 0.0)) or 0.0),
            "inner_action_support": float(compact_context.get("inner_action_support", meta_state.get("inner_action_support", 0.0)) or 0.0),
            "inner_action_no": float(compact_context.get("inner_action_no", meta_state.get("inner_action_no", 0.0)) or 0.0),
            "strategy_confirmation": float(compact_context.get("strategy_confirmation", meta_state.get("strategy_confirmation", 0.0)) or 0.0),
            "strategy_rejection": float(compact_context.get("strategy_rejection", meta_state.get("strategy_rejection", 0.0)) or 0.0),
            "strategy_trust_bearing": float(compact_context.get("strategy_trust_bearing", meta_state.get("strategy_trust_bearing", 0.0)) or 0.0),
            "strategy_context_bearing": float(compact_context.get("strategy_context_bearing", meta_state.get("strategy_context_bearing", 0.0)) or 0.0),
            "strategy_contradiction_pressure": float(compact_context.get("strategy_contradiction_pressure", meta_state.get("strategy_contradiction_pressure", 0.0)) or 0.0),
            "thought_confirmation_bearing": float(compact_context.get("thought_confirmation_bearing", meta_state.get("thought_confirmation_bearing", compact_context.get("strategy_confirmation", meta_state.get("strategy_confirmation", 0.0)))) or 0.0),
            "thought_rejection_pressure": float(compact_context.get("thought_rejection_pressure", meta_state.get("thought_rejection_pressure", compact_context.get("strategy_rejection", meta_state.get("strategy_rejection", 0.0)))) or 0.0),
            "thought_trust_bearing": float(compact_context.get("thought_trust_bearing", meta_state.get("thought_trust_bearing", compact_context.get("strategy_trust_bearing", meta_state.get("strategy_trust_bearing", 0.0)))) or 0.0),
            "contact_context_bearing": float(compact_context.get("contact_context_bearing", meta_state.get("contact_context_bearing", compact_context.get("strategy_context_bearing", meta_state.get("strategy_context_bearing", 0.0)))) or 0.0),
            "real_area_contact_bearing": float(compact_context.get("real_area_contact_bearing", meta_state.get("real_area_contact_bearing", 0.0)) or 0.0),
            "visual_reality_bearing": float(compact_context.get("visual_reality_bearing", meta_state.get("visual_reality_bearing", 0.0)) or 0.0),
            "felt_reality_bearing": float(compact_context.get("felt_reality_bearing", meta_state.get("felt_reality_bearing", meta_state.get("contact_carrying_quality", 0.0))) or 0.0),
            "form_mcm_reality_fit": float(compact_context.get("form_mcm_reality_fit", meta_state.get("form_mcm_reality_fit", meta_state.get("outer_inner_coherence", 0.0))) or 0.0),
            "receptive_contact_offer_pressure": float(compact_context.get("receptive_contact_offer_pressure", meta_state.get("receptive_contact_offer_pressure", 0.0)) or 0.0),
            "receptive_contact_maturity": float(compact_context.get("receptive_contact_maturity", meta_state.get("receptive_contact_maturity", 0.0)) or 0.0),
            "receptive_contact_immaturity_pressure": float(compact_context.get("receptive_contact_immaturity_pressure", meta_state.get("receptive_contact_immaturity_pressure", 0.0)) or 0.0),
            "receptive_contact_restraint": float(compact_context.get("receptive_contact_restraint", meta_state.get("receptive_contact_restraint", 0.0)) or 0.0),
            "thought_contradiction_pressure": float(compact_context.get("thought_contradiction_pressure", meta_state.get("thought_contradiction_pressure", compact_context.get("strategy_contradiction_pressure", meta_state.get("strategy_contradiction_pressure", 0.0)))) or 0.0),
            "open_hypothesis_reality_permission": float(compact_context.get("open_hypothesis_reality_permission", meta_state.get("open_hypothesis_reality_permission", compact_context.get("open_hypothesis_action_permission", meta_state.get("open_hypothesis_action_permission", 0.0)))) or 0.0),
            "possibility_contact_bearing": float(compact_context.get("possibility_contact_bearing", meta_state.get("possibility_contact_bearing", compact_context.get("possibility_action_support", meta_state.get("possibility_action_support", 0.0)))) or 0.0),
            "dominant_hypothesis_reality_bearing": float(compact_context.get("dominant_hypothesis_reality_bearing", meta_state.get("dominant_hypothesis_reality_bearing", compact_context.get("dominant_hypothesis_action_readiness", meta_state.get("dominant_hypothesis_action_readiness", 0.0)))) or 0.0),
            "current_hypothesis_reality_bearing": float(compact_context.get("current_hypothesis_reality_bearing", meta_state.get("current_hypothesis_reality_bearing", compact_context.get("current_hypothesis_action_support", meta_state.get("current_hypothesis_action_support", 0.0)))) or 0.0),
            "side": str(side),
            "entry_price": float(entry_price),
            "tp_price": float(tp_price),
            "sl_price": float(sl_price),
            "rr_value": float(rr_value),
            "entry_mode": str(trade_plan.get("entry_mode", "") or ""),
            "contact_entry_mode": str(trade_plan.get("contact_entry_mode", trade_plan.get("entry_mode", "")) or ""),
            "entry_contact_state": str(trade_plan.get("entry_contact_state", trade_plan.get("entry_choice_state", "")) or ""),
            "entry_choice_state": str(trade_plan.get("entry_choice_state", "") or ""),
            "entry_preference_state": str(trade_plan.get("entry_preference_state", "") or ""),
            "entry_choice_basis": str(trade_plan.get("entry_choice_basis", "") or ""),
            "entry_contact_option_count": int(trade_plan.get("entry_contact_option_count", 0) or 0),
            "selected_entry_offer_score": float(trade_plan.get("selected_entry_offer_score", 0.0) or 0.0),
            "selected_entry_learned_fit": float(trade_plan.get("selected_entry_learned_fit", 0.0) or 0.0),
            "selected_entry_preference_key": str(trade_plan.get("selected_entry_preference_key", "-") or "-"),
            "selected_entry_preference_trust": float(trade_plan.get("selected_entry_preference_trust", 0.0) or 0.0),
            "selected_entry_preference_caution": float(trade_plan.get("selected_entry_preference_caution", 0.0) or 0.0),
            "selected_entry_preference_maturity": float(trade_plan.get("selected_entry_preference_maturity", 0.0) or 0.0),
            "selected_entry_preference_utility": float(trade_plan.get("selected_entry_preference_utility", 0.0) or 0.0),
            "selected_entry_property_profile_id": str(trade_plan.get("selected_entry_property_profile_id", "-") or "-"),
            "selected_entry_property_profile_similarity": float(trade_plan.get("selected_entry_property_profile_similarity", 0.0) or 0.0),
            "selected_entry_property_profile_trust": float(trade_plan.get("selected_entry_property_profile_trust", 0.0) or 0.0),
            "selected_entry_property_profile_caution": float(trade_plan.get("selected_entry_property_profile_caution", 0.0) or 0.0),
            "selected_entry_property_profile_maturity": float(trade_plan.get("selected_entry_property_profile_maturity", 0.0) or 0.0),
            "selected_entry_property_profile_utility": float(trade_plan.get("selected_entry_property_profile_utility", 0.0) or 0.0),
            "selected_memory_caution_pressure": float(trade_plan.get("selected_memory_caution_pressure", 0.0) or 0.0),
            "selected_memory_bearing_pressure": float(trade_plan.get("selected_memory_bearing_pressure", 0.0) or 0.0),
            "mature_careful_contact_pressure": float(trade_plan.get("mature_careful_contact_pressure", 0.0) or 0.0),
            "contact_learning_state": str(trade_plan.get("contact_learning_state", "") or ""),
            "learned_contact_fit": float(trade_plan.get("learned_contact_fit", 0.0) or 0.0),
            "area_contact_focus_id": str(trade_plan.get("area_contact_focus_id", trade_plan.get("strategic_area_focus_id", "")) or ""),
            "strategic_area_focus_id": str(trade_plan.get("strategic_area_focus_id", "") or ""),
            "area_contact_location": str(trade_plan.get("area_contact_location", trade_plan.get("strategic_entry_location", "")) or ""),
            "strategic_entry_location": str(trade_plan.get("strategic_entry_location", "") or ""),
            "contact_entry_fit": float(trade_plan.get("contact_entry_fit", trade_plan.get("strategic_entry_fit", 0.0)) or 0.0),
            "strategic_entry_fit": float(trade_plan.get("strategic_entry_fit", trade_plan.get("contact_entry_fit", 0.0)) or 0.0),
            "area_contact_readiness": float(trade_plan.get("area_contact_readiness", trade_plan.get("area_direct_readiness", 0.0)) or 0.0),
            "area_direct_readiness": float(trade_plan.get("area_direct_readiness", trade_plan.get("area_contact_readiness", 0.0)) or 0.0),
            "entry_geometry_bearing": float(trade_plan.get("entry_geometry_bearing", 0.0) or 0.0),
            "entry_geometry_state": str(trade_plan.get("entry_geometry_state", "contact_offer_only") or "contact_offer_only"),
            "pre_geometry_thought_bearing": float(trade_plan.get("pre_geometry_thought_bearing", 0.0) or 0.0),
            "pre_geometry_felt_bearing": float(trade_plan.get("pre_geometry_felt_bearing", 0.0) or 0.0),
            "pre_geometry_reality_bearing": float(trade_plan.get("pre_geometry_reality_bearing", 0.0) or 0.0),
            "pre_geometry_preference_bearing": float(trade_plan.get("pre_geometry_preference_bearing", 0.0) or 0.0),
            "organic_contact_bearing": float(trade_plan.get("organic_contact_bearing", 0.0) or 0.0),
            "structure_quality": float(structure_quality),
            "structure_bucket": str(structure_bucket),
            "form_symbol_id": str(form_state.get("form_symbol_id", "") or ""),
            "form_symbol_compound_id": str(form_state.get("form_symbol_compound_id", "") or ""),
            "form_symbol_semantic_profile": str(form_state.get("form_symbol_semantic_profile", "") or ""),
            "hypothesis_confirmation": float(thought_seed.get("thought_confirmation_score", meta_state.get("hypothesis_confirmation_without_action", 0.0)) or 0.0),
            "reality_binding": float(thought_seed.get("reality_binding_score", meta_state.get("inner_outer_alignment", 0.0)) or 0.0),
            "structural_grounding": float(thought_seed.get("thought_structural_grounding", structure_quality) or 0.0),
            "future_variant_pressure": float(meta_state.get("future_variant_pressure", 0.0) or 0.0),
            "afterimage_action_maturity": float(meta_state.get("afterimage_action_maturity", 0.0) or 0.0),
            "possibility_field_state": str(possibility_state.get("possibility_field_state", meta_state.get("possibility_field_state", "")) or ""),
            "possibility_observer_state": str(possibility_state.get("possibility_observer_state", meta_state.get("possibility_observer_state", "")) or ""),
            "possibility_dominant_variant_id": str(possibility_variant_id),
            "possibility_dominant_kind": str(possibility_state.get("possibility_dominant_kind", meta_state.get("possibility_dominant_kind", "")) or ""),
            "possibility_dominant_direction": str(possibility_direction),
            "possibility_family_key": str(possibility_family_key),
            "possibility_observation_depth": float(possibility_state.get("possibility_observation_depth", meta_state.get("possibility_observation_depth", 0.0)) or 0.0),
            "possibility_reality_contact": float(possibility_state.get("possibility_reality_contact", meta_state.get("possibility_reality_contact", 0.0)) or 0.0),
            "possibility_variant_maturity": float(possibility_state.get("possibility_variant_maturity", meta_state.get("possibility_variant_maturity", 0.0)) or 0.0),
            "possibility_variant_trust": float(possibility_state.get("possibility_variant_trust", meta_state.get("possibility_variant_trust", 0.0)) or 0.0),
            "possibility_variant_caution": float(possibility_state.get("possibility_variant_caution", meta_state.get("possibility_variant_caution", 0.0)) or 0.0),
            "possibility_collapse_reason": str(possibility_reason),
            "possibility_collapse_reversibility": float(possibility_state.get("possibility_collapse_reversibility", meta_state.get("possibility_collapse_reversibility", 0.0)) or 0.0),
            "possibility_memory_return": float(possibility_state.get("possibility_memory_return", meta_state.get("possibility_memory_return", 0.0)) or 0.0),
        })
        self.data["pending_observations"] = pending[-120:]
        if str(structure_bucket or "").strip().lower() == "non_zone":
            learning["low_observations"] = int(learning.get("low_observations", 0) or 0) + 1
        else:
            learning["structured_observations"] = int(learning.get("structured_observations", 0) or 0) + 1
        self.data["observation_learning"] = dict(learning)
        self._refresh_observation_learning_summary()

    def _build_attempt_record(self, status_key: str, context: dict, structure_quality: float, structure_bucket: str) -> dict:
        compact_context = self._compact_context(context or {})
        trade_plan = dict(compact_context.get("trade_plan", {}) or {})
        side = str(trade_plan.get("decision", "") or "").strip().upper()
        if side not in ("LONG", "SHORT"):
            side = "-"

        return {
            "event": "attempt",
            "status": str(status_key or "unknown"),
            "timestamp": self.data.get("current_timestamp"),
            "side": str(side),
            "structure_quality": float(structure_quality),
            "structure_bucket": str(structure_bucket),
            "context": compact_context,
        }

    # ─────────────────────────────────────────────
    def _should_write_attempt_record(self, status_key: str) -> bool:
        if bool(getattr(self, "_attempt_record_path_explicit", False)):
            return True

        if not bool(getattr(Config, "TRADE_STATS_ATTEMPT_RECORD_DEBUG", True)):
            return False

        status = str(status_key or "").strip().lower()
        if status in ("submitted", "filled", "cancelled", "timeout", "blocked_value_gate"):
            return True

        every_n = max(1, int(getattr(Config, "TRADE_STATS_ATTEMPT_RECORD_EVERY_N", 1) or 1))
        if every_n <= 1:
            return True

        return (int(self.data.get("attempts", 0) or 0) % every_n) == 0

    def _should_write_outcome_record(self) -> bool:
        return bool(getattr(Config, "MCM_OUTCOME_DEBUG", False))

    # ─────────────────────────────────────────────
    def get_attempt_feedback(self, window: int = 24) -> dict:
        recent_attempts = list(self.data.get("recent_attempts", []) or [])
        items = recent_attempts[-max(1, int(window or 1)):]

        if not items:
            return {
                "recent_attempt_count": 0,
                "attempt_density": 0.0,
                "fill_ratio": 0.0,
                "blocked_ratio": 0.0,
                "cancel_ratio": 0.0,
                "timeout_ratio": 0.0,
                "zone_ratio": 0.0,
                "mean_structure_quality": 0.0,
                "context_quality": 0.0,
                "overtrade_pressure": 0.0,
                "observe_share": 0.0,
                "replan_share": 0.0,
                "withheld_share": 0.0,
                "pressure_to_capacity": 0.0,
                "field_stimulus_density": 0.0,
                "regulatory_load": 0.0,
                "action_capacity": 0.0,
                "recovery_need": 0.0,
                "survival_pressure": 0.0,
                "pressure_release": 0.0,
                "load_bearing_capacity": 0.0,
                "state_stability": 0.0,
                "capacity_reserve": 0.0,
                "recovery_balance": 0.0,
                "regulated_courage": 0.0,
                "courage_gap": 0.0,
                "action_inhibition": 0.0,
                "action_clearance": 0.0,
                "regulation_before_action": 0.0,
                "observation_learning_open": 0,
                "observation_learning_resolved": 0,
                "observation_saved_loss": 0,
                "observation_missed_gain": 0,
                "observation_neutral": 0,
                "observation_low_count": 0,
                "observation_maturity_trust": 0.0,
                "observation_action_pressure": 0.0,
                "hypothesis_observed_outcome": "hypothesis_observed_open",
                "hypothesis_confirmation_without_action": 0.0,
                "hypothesis_rejection_without_action": 0.0,
                "hypothesis_neutral_without_action": 0.0,
                "hypothesis_observation_maturity": 0.0,
                "possibility_maturity": 0.0,
                "possibility_caution": 0.0,
                "hypothesis_observed_stability": 0.0,
                "hypothesis_trust_score": 0.0,
                "hypothesis_trust_priority": 0.0,
                "hypothesis_frustration_risk": 0.0,
                "hypothesis_distance_risk": 0.0,
                "hypothesis_trust_state": "hypothesis_trust_unformed",
                "dominant_hypothesis_trust_key": "-",
                "dominant_hypothesis_trust_score": 0.0,
                "dominant_hypothesis_action_readiness": 0.0,
                "dominant_hypothesis_trust_evidence": 0,
                "dominant_possibility_variant_key": "-",
                "dominant_possibility_variant_trust": 0.0,
                "dominant_possibility_variant_caution": 0.0,
                "dominant_possibility_variant_maturity": 0.0,
                "dominant_possibility_variant_evidence": 0,
                "hypothesis_trust_family_count": 0,
                "declined_hypothesis_resolved": 0,
                "declined_hypothesis_saved_loss": 0,
                "declined_hypothesis_missed_gain": 0,
                "declined_hypothesis_confirmation_without_action": 0.0,
                "declined_hypothesis_rejection_without_action": 0.0,
                "declined_hypothesis_maturity": 0.0,
                "declined_long_hypothesis_count": 0,
                "declined_long_hypothesis_confirmation": 0.0,
                "declined_long_hypothesis_rejection": 0.0,
                "declined_long_hypothesis_maturity": 0.0,
                "declined_short_hypothesis_count": 0,
                "declined_short_hypothesis_confirmation": 0.0,
                "declined_short_hypothesis_rejection": 0.0,
                "declined_short_hypothesis_maturity": 0.0,
            }

        total = float(len(items))
        filled = 0.0
        blocked = 0.0
        cancelled = 0.0
        timeout = 0.0
        observed = 0.0
        replanned = 0.0
        withheld = 0.0
        zone = 0.0
        structure_sum = 0.0
        pressure_sum = 0.0
        field_stimulus_density_sum = 0.0
        regulatory_load_sum = 0.0
        action_capacity_sum = 0.0
        recovery_sum = 0.0
        survival_pressure_sum = 0.0
        pressure_release_sum = 0.0
        load_bearing_sum = 0.0
        state_stability_sum = 0.0
        capacity_reserve_sum = 0.0
        recovery_balance_sum = 0.0
        regulated_courage_sum = 0.0
        courage_gap_sum = 0.0
        action_inhibition_sum = 0.0
        action_clearance_sum = 0.0
        regulation_before_action_sum = 0.0

        for item in items:
            status = str((item or {}).get("status", "") or "").strip().lower()
            structure_quality = float((item or {}).get("structure_quality", 0.0) or 0.0)
            structure_bucket = str((item or {}).get("structure_bucket", "") or "").strip().lower()
            pressure_to_capacity = float((item or {}).get("pressure_to_capacity", 0.0) or 0.0)
            field_stimulus_density = float((item or {}).get("field_stimulus_density", 0.0) or 0.0)
            regulatory_load = float((item or {}).get("regulatory_load", 0.0) or 0.0)
            action_capacity = float((item or {}).get("action_capacity", 0.0) or 0.0)
            recovery_need = float((item or {}).get("recovery_need", 0.0) or 0.0)
            survival_pressure = float((item or {}).get("survival_pressure", 0.0) or 0.0)
            pressure_release = float((item or {}).get("pressure_release", 0.0) or 0.0)
            load_bearing_capacity = float((item or {}).get("load_bearing_capacity", 0.0) or 0.0)
            state_stability = float((item or {}).get("state_stability", 0.0) or 0.0)
            capacity_reserve = float((item or {}).get("capacity_reserve", 0.0) or 0.0)
            recovery_balance = float((item or {}).get("recovery_balance", 0.0) or 0.0)
            regulated_courage = float((item or {}).get("regulated_courage", 0.0) or 0.0)
            courage_gap = float((item or {}).get("courage_gap", 0.0) or 0.0)
            action_inhibition = float((item or {}).get("action_inhibition", 0.0) or 0.0)
            action_clearance = float((item or {}).get("action_clearance", 0.0) or 0.0)
            pre_action_phase = str((item or {}).get("pre_action_phase", "") or "").strip().lower()

            structure_sum += structure_quality
            pressure_sum += pressure_to_capacity
            field_stimulus_density_sum += field_stimulus_density
            regulatory_load_sum += regulatory_load
            action_capacity_sum += action_capacity
            recovery_sum += recovery_need
            survival_pressure_sum += survival_pressure
            pressure_release_sum += pressure_release
            load_bearing_sum += load_bearing_capacity
            state_stability_sum += state_stability
            capacity_reserve_sum += capacity_reserve
            recovery_balance_sum += recovery_balance
            regulated_courage_sum += regulated_courage
            courage_gap_sum += courage_gap
            action_inhibition_sum += action_inhibition
            action_clearance_sum += action_clearance

            if status == "filled":
                filled += 1.0
            elif status in ("blocked", "blocked_value_gate"):
                blocked += 1.0
            elif status == "cancelled":
                cancelled += 1.0
            elif status == "timeout":
                timeout += 1.0
            elif status == "observed_only":
                observed += 1.0
            elif status == "replanned":
                replanned += 1.0
            elif status == "withheld":
                withheld += 1.0

            if structure_bucket == "zone":
                zone += 1.0

            if pre_action_phase in ("regulated", "ready", "stable", "aligned"):
                regulation_before_action_sum += 1.0

        attempt_density = max(0.0, min(1.0, total / max(8.0, float(window) * 0.50)))
        fill_ratio = filled / total
        blocked_ratio = blocked / total
        cancel_ratio = cancelled / total
        timeout_ratio = timeout / total
        observe_share = observed / total
        replan_share = replanned / total
        withheld_share = withheld / total
        zone_ratio = zone / total
        mean_structure_quality = structure_sum / total
        avg_pressure_to_capacity = pressure_sum / total
        avg_field_stimulus_density = field_stimulus_density_sum / total
        avg_regulatory_load = regulatory_load_sum / total
        avg_action_capacity = action_capacity_sum / total
        avg_recovery_need = recovery_sum / total
        avg_survival_pressure = survival_pressure_sum / total
        avg_pressure_release = pressure_release_sum / total
        avg_load_bearing_capacity = load_bearing_sum / total
        avg_state_stability = state_stability_sum / total
        avg_capacity_reserve = capacity_reserve_sum / total
        avg_recovery_balance = recovery_balance_sum / total
        avg_regulated_courage = regulated_courage_sum / total
        avg_courage_gap = courage_gap_sum / total
        avg_action_inhibition = action_inhibition_sum / total
        avg_action_clearance = action_clearance_sum / total
        regulation_before_action = regulation_before_action_sum / total
        observation_learning = self._refresh_observation_learning_summary()
        observation_open = int(observation_learning.get("open", 0) or 0)
        observation_resolved = int(observation_learning.get("resolved", 0) or 0)
        observation_saved_loss = int(observation_learning.get("saved_loss", 0) or 0)
        observation_missed_gain = int(observation_learning.get("missed_gain", 0) or 0)
        observation_neutral = int(observation_learning.get("neutral", 0) or 0)
        observation_low_count = int(observation_learning.get("low_observations", 0) or 0)
        observation_maturity_trust = float(observation_learning.get("maturity_trust", 0.0) or 0.0)
        observation_action_pressure = float(observation_learning.get("action_pressure", 0.0) or 0.0)
        hypothesis_observed_outcome = str(observation_learning.get("hypothesis_observed_outcome", "hypothesis_observed_open") or "hypothesis_observed_open")
        hypothesis_confirmation_without_action = float(observation_learning.get("hypothesis_confirmation_without_action", 0.0) or 0.0)
        hypothesis_rejection_without_action = float(observation_learning.get("hypothesis_rejection_without_action", 0.0) or 0.0)
        hypothesis_neutral_without_action = float(observation_learning.get("hypothesis_neutral_without_action", 0.0) or 0.0)
        hypothesis_observation_maturity = float(observation_learning.get("hypothesis_observation_maturity", 0.0) or 0.0)
        possibility_maturity = float(observation_learning.get("possibility_maturity", 0.0) or 0.0)
        possibility_caution = float(observation_learning.get("possibility_caution", 0.0) or 0.0)
        hypothesis_observed_stability = float(observation_learning.get("hypothesis_observed_stability", 0.0) or 0.0)
        hypothesis_trust_score = float(observation_learning.get("hypothesis_trust_score", 0.0) or 0.0)
        hypothesis_trust_priority = float(observation_learning.get("hypothesis_trust_priority", 0.0) or 0.0)
        hypothesis_frustration_risk = float(observation_learning.get("hypothesis_frustration_risk", 0.0) or 0.0)
        hypothesis_distance_risk = float(observation_learning.get("hypothesis_distance_risk", 0.0) or 0.0)
        hypothesis_trust_state = str(observation_learning.get("hypothesis_trust_state", "hypothesis_trust_unformed") or "hypothesis_trust_unformed")
        dominant_hypothesis_trust_key = str(observation_learning.get("dominant_hypothesis_trust_key", "-") or "-")
        dominant_hypothesis_trust_score = float(observation_learning.get("dominant_hypothesis_trust_score", 0.0) or 0.0)
        dominant_hypothesis_action_readiness = float(observation_learning.get("dominant_hypothesis_action_readiness", 0.0) or 0.0)
        dominant_hypothesis_trust_evidence = int(observation_learning.get("dominant_hypothesis_trust_evidence", 0) or 0)
        dominant_possibility_variant_key = str(observation_learning.get("dominant_possibility_variant_key", "-") or "-")
        dominant_possibility_variant_trust = float(observation_learning.get("dominant_possibility_variant_trust", 0.0) or 0.0)
        dominant_possibility_variant_caution = float(observation_learning.get("dominant_possibility_variant_caution", 0.0) or 0.0)
        dominant_possibility_variant_maturity = float(observation_learning.get("dominant_possibility_variant_maturity", 0.0) or 0.0)
        dominant_possibility_variant_evidence = int(observation_learning.get("dominant_possibility_variant_evidence", 0) or 0)
        hypothesis_trust_family_count = int(observation_learning.get("hypothesis_trust_family_count", 0) or 0)
        declined_hypothesis_resolved = int(observation_learning.get("declined_hypothesis_resolved", 0) or 0)
        declined_hypothesis_saved_loss = int(observation_learning.get("declined_hypothesis_saved_loss", 0) or 0)
        declined_hypothesis_missed_gain = int(observation_learning.get("declined_hypothesis_missed_gain", 0) or 0)
        declined_hypothesis_confirmation_without_action = float(observation_learning.get("declined_hypothesis_confirmation_without_action", 0.0) or 0.0)
        declined_hypothesis_rejection_without_action = float(observation_learning.get("declined_hypothesis_rejection_without_action", 0.0) or 0.0)
        declined_hypothesis_maturity = float(observation_learning.get("declined_hypothesis_maturity", 0.0) or 0.0)
        declined_long_hypothesis_count = int(observation_learning.get("declined_long_hypothesis_count", 0) or 0)
        declined_long_hypothesis_confirmation = float(observation_learning.get("declined_long_hypothesis_confirmation", 0.0) or 0.0)
        declined_long_hypothesis_rejection = float(observation_learning.get("declined_long_hypothesis_rejection", 0.0) or 0.0)
        declined_long_hypothesis_maturity = float(observation_learning.get("declined_long_hypothesis_maturity", 0.0) or 0.0)
        declined_short_hypothesis_count = int(observation_learning.get("declined_short_hypothesis_count", 0) or 0)
        declined_short_hypothesis_confirmation = float(observation_learning.get("declined_short_hypothesis_confirmation", 0.0) or 0.0)
        declined_short_hypothesis_rejection = float(observation_learning.get("declined_short_hypothesis_rejection", 0.0) or 0.0)
        declined_short_hypothesis_maturity = float(observation_learning.get("declined_short_hypothesis_maturity", 0.0) or 0.0)

        context_quality = max(
            0.0,
            min(
                1.0,
                (mean_structure_quality * 0.28)
                + (zone_ratio * 0.12)
                + (fill_ratio * 0.08)
                + (avg_regulated_courage * 0.08)
                + (avg_action_clearance * 0.08)
                + (regulation_before_action * 0.08)
                + (observe_share * 0.03)
                + (replan_share * 0.03)
                + (avg_load_bearing_capacity * 0.08)
                + (avg_pressure_release * 0.05)
                + (avg_state_stability * 0.04)
                + (avg_capacity_reserve * 0.03)
                + (avg_recovery_balance * 0.03)
                - (min(1.0, avg_pressure_to_capacity / 2.0) * 0.06)
                - (avg_regulatory_load * 0.05)
                - (avg_recovery_need * 0.04)
                - (avg_survival_pressure * 0.04)
                - (avg_courage_gap * 0.04)
                - (avg_action_inhibition * 0.04)
                - (cancel_ratio * 0.03)
                - (timeout_ratio * 0.04)
            ),
        )

        overtrade_pressure = max(
            0.0,
            min(
                1.0,
                (attempt_density * 0.26)
                + ((1.0 - context_quality) * 0.18)
                + (blocked_ratio * 0.08)
                + (cancel_ratio * 0.06)
                + (timeout_ratio * 0.08)
                + (min(1.0, avg_pressure_to_capacity / 2.0) * 0.08)
                + (avg_regulatory_load * 0.08)
                + (avg_recovery_need * 0.05)
                + (avg_survival_pressure * 0.05)
                + (avg_action_inhibition * 0.04)
            ),
        )

        return {
            "recent_attempt_count": int(total),
            "attempt_density": float(attempt_density),
            "fill_ratio": float(fill_ratio),
            "blocked_ratio": float(blocked_ratio),
            "cancel_ratio": float(cancel_ratio),
            "timeout_ratio": float(timeout_ratio),
            "zone_ratio": float(zone_ratio),
            "mean_structure_quality": float(mean_structure_quality),
            "context_quality": float(context_quality),
            "overtrade_pressure": float(overtrade_pressure),
            "observe_share": float(observe_share),
            "replan_share": float(replan_share),
            "withheld_share": float(withheld_share),
            "pressure_to_capacity": float(avg_pressure_to_capacity),
            "field_stimulus_density": float(avg_field_stimulus_density),
            "regulatory_load": float(avg_regulatory_load),
            "action_capacity": float(avg_action_capacity),
            "recovery_need": float(avg_recovery_need),
            "survival_pressure": float(avg_survival_pressure),
            "pressure_release": float(avg_pressure_release),
            "load_bearing_capacity": float(avg_load_bearing_capacity),
            "state_stability": float(avg_state_stability),
            "capacity_reserve": float(avg_capacity_reserve),
            "recovery_balance": float(avg_recovery_balance),
            "regulated_courage": float(avg_regulated_courage),
            "courage_gap": float(avg_courage_gap),
            "action_inhibition": float(avg_action_inhibition),
            "action_clearance": float(avg_action_clearance),
            "regulation_before_action": float(regulation_before_action),
            "observation_learning_open": int(observation_open),
            "observation_learning_resolved": int(observation_resolved),
            "observation_saved_loss": int(observation_saved_loss),
            "observation_missed_gain": int(observation_missed_gain),
            "observation_neutral": int(observation_neutral),
            "observation_low_count": int(observation_low_count),
            "observation_maturity_trust": float(observation_maturity_trust),
            "observation_action_pressure": float(observation_action_pressure),
            "hypothesis_observed_outcome": str(hypothesis_observed_outcome),
            "hypothesis_confirmation_without_action": float(hypothesis_confirmation_without_action),
            "hypothesis_rejection_without_action": float(hypothesis_rejection_without_action),
            "hypothesis_neutral_without_action": float(hypothesis_neutral_without_action),
            "hypothesis_observation_maturity": float(hypothesis_observation_maturity),
            "possibility_maturity": float(possibility_maturity),
            "possibility_caution": float(possibility_caution),
            "hypothesis_observed_stability": float(hypothesis_observed_stability),
            "hypothesis_trust_score": float(hypothesis_trust_score),
            "hypothesis_trust_priority": float(hypothesis_trust_priority),
            "hypothesis_frustration_risk": float(hypothesis_frustration_risk),
            "hypothesis_distance_risk": float(hypothesis_distance_risk),
            "hypothesis_trust_state": str(hypothesis_trust_state),
            "dominant_hypothesis_trust_key": str(dominant_hypothesis_trust_key),
            "dominant_hypothesis_trust_score": float(dominant_hypothesis_trust_score),
            "dominant_hypothesis_action_readiness": float(dominant_hypothesis_action_readiness),
            "dominant_hypothesis_trust_evidence": int(dominant_hypothesis_trust_evidence),
            "dominant_possibility_variant_key": str(dominant_possibility_variant_key),
            "dominant_possibility_variant_trust": float(dominant_possibility_variant_trust),
            "dominant_possibility_variant_caution": float(dominant_possibility_variant_caution),
            "dominant_possibility_variant_maturity": float(dominant_possibility_variant_maturity),
            "dominant_possibility_variant_evidence": int(dominant_possibility_variant_evidence),
            "hypothesis_trust_family_count": int(hypothesis_trust_family_count),
            "declined_hypothesis_resolved": int(declined_hypothesis_resolved),
            "declined_hypothesis_saved_loss": int(declined_hypothesis_saved_loss),
            "declined_hypothesis_missed_gain": int(declined_hypothesis_missed_gain),
            "declined_hypothesis_confirmation_without_action": float(declined_hypothesis_confirmation_without_action),
            "declined_hypothesis_rejection_without_action": float(declined_hypothesis_rejection_without_action),
            "declined_hypothesis_maturity": float(declined_hypothesis_maturity),
            "declined_long_hypothesis_count": int(declined_long_hypothesis_count),
            "declined_long_hypothesis_confirmation": float(declined_long_hypothesis_confirmation),
            "declined_long_hypothesis_rejection": float(declined_long_hypothesis_rejection),
            "declined_long_hypothesis_maturity": float(declined_long_hypothesis_maturity),
            "declined_short_hypothesis_count": int(declined_short_hypothesis_count),
            "declined_short_hypothesis_confirmation": float(declined_short_hypothesis_confirmation),
            "declined_short_hypothesis_rejection": float(declined_short_hypothesis_rejection),
            "declined_short_hypothesis_maturity": float(declined_short_hypothesis_maturity),
        }

    # ─────────────────────────────────────────────
    def on_attempt(self, *, status: str, context: dict = None):
        status_key = str(status or "").strip().lower()
        if self._on_attempt_fast_path(status_key, context=context):
            return

        normalized_context = self._normalize_record_value(context or {})
        compact_context = self._compact_context(normalized_context)
        trade_plan = dict(compact_context.get("trade_plan", {}) or {})
        side = str(trade_plan.get("decision", "") or "").strip().upper()
        if side not in ("LONG", "SHORT"):
            side = "-"

        self.data["attempts"] = int(self.data.get("attempts", 0) or 0) + 1
        if side == "LONG":
            self.data["attempts_long"] = int(self.data.get("attempts_long", 0) or 0) + 1
        elif side == "SHORT":
            self.data["attempts_short"] = int(self.data.get("attempts_short", 0) or 0) + 1

        if status_key == "submitted":
            self.data["attempts_submitted"] = int(self.data.get("attempts_submitted", 0) or 0) + 1
            if side == "LONG":
                self.data["attempts_submitted_long"] = int(self.data.get("attempts_submitted_long", 0) or 0) + 1
            elif side == "SHORT":
                self.data["attempts_submitted_short"] = int(self.data.get("attempts_submitted_short", 0) or 0) + 1
        elif status_key == "filled":
            self.data["attempts_filled"] = int(self.data.get("attempts_filled", 0) or 0) + 1
            if side == "LONG":
                self.data["attempts_filled_long"] = int(self.data.get("attempts_filled_long", 0) or 0) + 1
            elif side == "SHORT":
                self.data["attempts_filled_short"] = int(self.data.get("attempts_filled_short", 0) or 0) + 1
        elif status_key == "cancelled":
            self.data["attempts_cancelled"] = int(self.data.get("attempts_cancelled", 0) or 0) + 1
        elif status_key == "timeout":
            self.data["attempts_timeout"] = int(self.data.get("attempts_timeout", 0) or 0) + 1
        elif status_key in ("blocked", "blocked_value_gate"):
            self.data["attempts_blocked"] = int(self.data.get("attempts_blocked", 0) or 0) + 1
        elif status_key == "skipped":
            self.data["attempts_skipped"] = int(self.data.get("attempts_skipped", 0) or 0) + 1
        elif status_key == "observed_only":
            self.data["attempts_observed"] = int(self.data.get("attempts_observed", 0) or 0) + 1
        elif status_key == "replanned":
            self.data["attempts_replanned"] = int(self.data.get("attempts_replanned", 0) or 0) + 1
        elif status_key == "withheld":
            self.data["attempts_withheld"] = int(self.data.get("attempts_withheld", 0) or 0) + 1

        structure_quality = self._extract_structure_quality(normalized_context)
        if structure_quality >= 0.55:
            self.data["attempt_structure_zone"] = int(self.data.get("attempt_structure_zone", 0) or 0) + 1
            structure_bucket = "zone"
        else:
            self.data["attempt_non_structure_zone"] = int(self.data.get("attempt_non_structure_zone", 0) or 0) + 1
            structure_bucket = "non_zone"

        self._register_observation_learning(
            status_key,
            normalized_context,
            structure_quality,
            structure_bucket,
        )

        attempt_record = self._build_attempt_record(
            status_key,
            normalized_context,
            structure_quality,
            structure_bucket,
        )

        field_state = dict(compact_context.get("field_state", {}) or {})
        experience_state = dict(compact_context.get("experience", {}) or {})
        meta_regulation_state = dict(compact_context.get("meta_regulation_state", {}) or {})
        active_mcm_contact_state = dict(compact_context.get("active_mcm_contact_state", {}) or {})
        trade_plan_state = dict(compact_context.get("trade_plan", {}) or {})
        regulation_snapshot = dict(compact_context.get("regulation_snapshot", {}) or {})
        state_after = dict(compact_context.get("state_after", {}) or {})

        snapshot_tension = dict(regulation_snapshot.get("tension", {}) or state_after.get("tension", {}) or {})
        snapshot_field = dict(regulation_snapshot.get("field", {}) or state_after.get("field", {}) or {})
        snapshot_experience = dict(regulation_snapshot.get("experience", {}) or state_after.get("experience", {}) or {})

        recent = list(self.data.get("recent_attempts", []) or [])
        recent.append(
            {
                "status": status_key or "unknown",
                "side": str(side),
                "decision_tendency": str(compact_context.get("decision_tendency", meta_regulation_state.get("pre_action_phase", "")) or ""),
                "rejection_reason": str(compact_context.get("rejection_reason", meta_regulation_state.get("rejection_reason", "")) or ""),
                "structure_quality": float(structure_quality),
                "structure_bucket": structure_bucket,
                "entry_mode": str(trade_plan_state.get("entry_mode", compact_context.get("entry_mode", "")) or ""),
                "contact_entry_mode": str(trade_plan_state.get("contact_entry_mode", compact_context.get("contact_entry_mode", trade_plan_state.get("entry_mode", compact_context.get("entry_mode", "")))) or ""),
                "entry_contact_state": str(trade_plan_state.get("entry_contact_state", compact_context.get("entry_contact_state", trade_plan_state.get("entry_choice_state", compact_context.get("entry_choice_state", "")))) or ""),
                "entry_choice_state": str(trade_plan_state.get("entry_choice_state", compact_context.get("entry_choice_state", "")) or ""),
                "contact_entry_fit": float(trade_plan_state.get("contact_entry_fit", compact_context.get("contact_entry_fit", trade_plan_state.get("strategic_entry_fit", compact_context.get("strategic_entry_fit", 0.0)))) or 0.0),
                "strategic_entry_fit": float(trade_plan_state.get("strategic_entry_fit", compact_context.get("strategic_entry_fit", trade_plan_state.get("contact_entry_fit", compact_context.get("contact_entry_fit", 0.0)))) or 0.0),
                "area_contact_readiness": float(trade_plan_state.get("area_contact_readiness", compact_context.get("area_contact_readiness", trade_plan_state.get("area_direct_readiness", compact_context.get("area_direct_readiness", 0.0)))) or 0.0),
                "area_direct_readiness": float(trade_plan_state.get("area_direct_readiness", compact_context.get("area_direct_readiness", trade_plan_state.get("area_contact_readiness", compact_context.get("area_contact_readiness", 0.0)))) or 0.0),
                "market_loudness": float(compact_context.get("market_loudness", 0.0) or 0.0),
                "market_frequency_hz": float(compact_context.get("market_frequency_hz", 0.0) or 0.0),
                "market_hearing_compression": float(compact_context.get("market_hearing_compression", 0.0) or 0.0),
                "energy_coherence_bearing": float(compact_context.get("energy_coherence_bearing", trade_plan_state.get("energy_coherence_bearing", meta_regulation_state.get("energy_coherence_bearing", 0.0))) or 0.0),
                "market_tone": str(compact_context.get("market_tone", "") or ""),
                "visual_blind_action_load": float(meta_regulation_state.get("visual_blind_action_load", 0.0) or 0.0),
                "visual_object_binding": float(meta_regulation_state.get("visual_object_binding", 0.0) or 0.0),
                "visual_grounding_strength": float(meta_regulation_state.get("visual_grounding_strength", 0.0) or 0.0),
                "visual_grounding_gap": float(meta_regulation_state.get("visual_grounding_gap", 0.0) or 0.0),
                "outer_inner_coherence": float(active_mcm_contact_state.get("outer_inner_coherence", meta_regulation_state.get("outer_inner_coherence", 0.0)) or 0.0),
                "contact_carrying_quality": float(active_mcm_contact_state.get("contact_carrying_quality", meta_regulation_state.get("contact_carrying_quality", 0.0)) or 0.0),
                "contact_overcoupling_risk": float(active_mcm_contact_state.get("contact_overcoupling_risk", meta_regulation_state.get("contact_overcoupling_risk", 0.0)) or 0.0),
                "inner_action_consent": float(compact_context.get("inner_action_consent", trade_plan_state.get("inner_action_consent", meta_regulation_state.get("inner_action_consent", 0.0))) or 0.0),
                "inner_action_support": float(compact_context.get("inner_action_support", trade_plan_state.get("inner_action_support", meta_regulation_state.get("inner_action_support", 0.0))) or 0.0),
                "inner_action_no": float(compact_context.get("inner_action_no", trade_plan_state.get("inner_action_no", meta_regulation_state.get("inner_action_no", 0.0))) or 0.0),
                "inner_action_consent_state": str(compact_context.get("inner_action_consent_state", trade_plan_state.get("inner_action_consent_state", meta_regulation_state.get("inner_action_consent_state", ""))) or ""),
                "strategy_confirmation": float(compact_context.get("strategy_confirmation", trade_plan_state.get("strategy_confirmation", meta_regulation_state.get("strategy_confirmation", 0.0))) or 0.0),
                "strategy_rejection": float(compact_context.get("strategy_rejection", trade_plan_state.get("strategy_rejection", meta_regulation_state.get("strategy_rejection", 0.0))) or 0.0),
                "strategy_trust_bearing": float(compact_context.get("strategy_trust_bearing", trade_plan_state.get("strategy_trust_bearing", meta_regulation_state.get("strategy_trust_bearing", 0.0))) or 0.0),
                "strategy_context_bearing": float(compact_context.get("strategy_context_bearing", trade_plan_state.get("strategy_context_bearing", meta_regulation_state.get("strategy_context_bearing", 0.0))) or 0.0),
                "raw_strategy_contradiction_pressure": float(compact_context.get("raw_strategy_contradiction_pressure", trade_plan_state.get("raw_strategy_contradiction_pressure", meta_regulation_state.get("raw_strategy_contradiction_pressure", 0.0))) or 0.0),
                "strategy_contradiction_pressure": float(compact_context.get("strategy_contradiction_pressure", trade_plan_state.get("strategy_contradiction_pressure", meta_regulation_state.get("strategy_contradiction_pressure", 0.0))) or 0.0),
                "thought_confirmation_bearing": float(compact_context.get("thought_confirmation_bearing", trade_plan_state.get("thought_confirmation_bearing", meta_regulation_state.get("thought_confirmation_bearing", compact_context.get("strategy_confirmation", trade_plan_state.get("strategy_confirmation", meta_regulation_state.get("strategy_confirmation", 0.0)))))) or 0.0),
                "thought_rejection_pressure": float(compact_context.get("thought_rejection_pressure", trade_plan_state.get("thought_rejection_pressure", meta_regulation_state.get("thought_rejection_pressure", compact_context.get("strategy_rejection", trade_plan_state.get("strategy_rejection", meta_regulation_state.get("strategy_rejection", 0.0)))))) or 0.0),
                "thought_trust_bearing": float(compact_context.get("thought_trust_bearing", trade_plan_state.get("thought_trust_bearing", meta_regulation_state.get("thought_trust_bearing", compact_context.get("strategy_trust_bearing", trade_plan_state.get("strategy_trust_bearing", meta_regulation_state.get("strategy_trust_bearing", 0.0)))))) or 0.0),
                "contact_context_bearing": float(compact_context.get("contact_context_bearing", trade_plan_state.get("contact_context_bearing", meta_regulation_state.get("contact_context_bearing", compact_context.get("strategy_context_bearing", trade_plan_state.get("strategy_context_bearing", meta_regulation_state.get("strategy_context_bearing", 0.0)))))) or 0.0),
                "real_area_contact_bearing": float(compact_context.get("real_area_contact_bearing", trade_plan_state.get("real_area_contact_bearing", meta_regulation_state.get("real_area_contact_bearing", 0.0))) or 0.0),
                "visual_reality_bearing": float(compact_context.get("visual_reality_bearing", trade_plan_state.get("visual_reality_bearing", meta_regulation_state.get("visual_reality_bearing", 0.0))) or 0.0),
                "felt_reality_bearing": float(compact_context.get("felt_reality_bearing", trade_plan_state.get("felt_reality_bearing", meta_regulation_state.get("felt_reality_bearing", meta_regulation_state.get("contact_carrying_quality", 0.0)))) or 0.0),
                "form_mcm_reality_fit": float(compact_context.get("form_mcm_reality_fit", trade_plan_state.get("form_mcm_reality_fit", meta_regulation_state.get("form_mcm_reality_fit", meta_regulation_state.get("outer_inner_coherence", 0.0)))) or 0.0),
                "receptive_contact_offer_pressure": float(compact_context.get("receptive_contact_offer_pressure", trade_plan_state.get("receptive_contact_offer_pressure", meta_regulation_state.get("receptive_contact_offer_pressure", 0.0))) or 0.0),
                "receptive_contact_maturity": float(compact_context.get("receptive_contact_maturity", trade_plan_state.get("receptive_contact_maturity", meta_regulation_state.get("receptive_contact_maturity", 0.0))) or 0.0),
                "receptive_contact_immaturity_pressure": float(compact_context.get("receptive_contact_immaturity_pressure", trade_plan_state.get("receptive_contact_immaturity_pressure", meta_regulation_state.get("receptive_contact_immaturity_pressure", 0.0))) or 0.0),
                "receptive_contact_restraint": float(compact_context.get("receptive_contact_restraint", trade_plan_state.get("receptive_contact_restraint", meta_regulation_state.get("receptive_contact_restraint", 0.0))) or 0.0),
                "raw_thought_contradiction_pressure": float(compact_context.get("raw_thought_contradiction_pressure", trade_plan_state.get("raw_thought_contradiction_pressure", meta_regulation_state.get("raw_thought_contradiction_pressure", compact_context.get("raw_strategy_contradiction_pressure", trade_plan_state.get("raw_strategy_contradiction_pressure", meta_regulation_state.get("raw_strategy_contradiction_pressure", 0.0)))))) or 0.0),
                "thought_contradiction_pressure": float(compact_context.get("thought_contradiction_pressure", trade_plan_state.get("thought_contradiction_pressure", meta_regulation_state.get("thought_contradiction_pressure", compact_context.get("strategy_contradiction_pressure", trade_plan_state.get("strategy_contradiction_pressure", meta_regulation_state.get("strategy_contradiction_pressure", 0.0)))))) or 0.0),
                "open_hypothesis_reality_permission": float(compact_context.get("open_hypothesis_reality_permission", trade_plan_state.get("open_hypothesis_reality_permission", meta_regulation_state.get("open_hypothesis_reality_permission", compact_context.get("open_hypothesis_action_permission", trade_plan_state.get("open_hypothesis_action_permission", meta_regulation_state.get("open_hypothesis_action_permission", 0.0)))))) or 0.0),
                "possibility_contact_bearing": float(compact_context.get("possibility_contact_bearing", trade_plan_state.get("possibility_contact_bearing", meta_regulation_state.get("possibility_contact_bearing", compact_context.get("possibility_action_support", trade_plan_state.get("possibility_action_support", meta_regulation_state.get("possibility_action_support", 0.0)))))) or 0.0),
                "dominant_hypothesis_reality_bearing": float(compact_context.get("dominant_hypothesis_reality_bearing", trade_plan_state.get("dominant_hypothesis_reality_bearing", meta_regulation_state.get("dominant_hypothesis_reality_bearing", compact_context.get("dominant_hypothesis_action_readiness", trade_plan_state.get("dominant_hypothesis_action_readiness", meta_regulation_state.get("dominant_hypothesis_action_readiness", 0.0)))))) or 0.0),
                "current_hypothesis_reality_bearing": float(compact_context.get("current_hypothesis_reality_bearing", trade_plan_state.get("current_hypothesis_reality_bearing", meta_regulation_state.get("current_hypothesis_reality_bearing", compact_context.get("current_hypothesis_action_support", trade_plan_state.get("current_hypothesis_action_support", meta_regulation_state.get("current_hypothesis_action_support", 0.0)))))) or 0.0),
                "pressure_to_capacity": float(field_state.get("pressure_to_capacity", snapshot_field.get("pressure_to_capacity", 0.0)) or 0.0),
                "field_stimulus_density": float(field_state.get("field_stimulus_density", snapshot_field.get("field_stimulus_density", 0.0)) or 0.0),
                "regulatory_load": float(field_state.get("regulatory_load", snapshot_field.get("regulatory_load", 0.0)) or 0.0),
                "action_capacity": float(field_state.get("action_capacity", snapshot_field.get("action_capacity", 0.0)) or 0.0),
                "recovery_need": float(field_state.get("recovery_need", snapshot_field.get("recovery_need", 0.0)) or 0.0),
                "survival_pressure": float(field_state.get("survival_pressure", snapshot_field.get("survival_pressure", 0.0)) or 0.0),
                "pressure_release": float(experience_state.get("pressure_release", snapshot_experience.get("pressure_release", 0.0)) or 0.0),
                "load_bearing_capacity": float(experience_state.get("load_bearing_capacity", snapshot_experience.get("load_bearing_capacity", 0.0)) or 0.0),
                "state_stability": float(snapshot_tension.get("stability", 0.0) or 0.0),
                "capacity_reserve": float(field_state.get("capacity_reserve", snapshot_field.get("capacity_reserve", 0.0)) or 0.0),
                "recovery_balance": float(field_state.get("recovery_balance", snapshot_field.get("recovery_balance", 0.0)) or 0.0),
                "regulated_courage": float(meta_regulation_state.get("regulated_courage", 0.0) or 0.0),
                "courage_gap": float(meta_regulation_state.get("courage_gap", 0.0) or 0.0),
                "action_inhibition": float(meta_regulation_state.get("action_inhibition", 0.0) or 0.0),
                "action_clearance": float(meta_regulation_state.get("action_clearance", 0.0) or 0.0),
                "pre_action_phase": str(meta_regulation_state.get("pre_action_phase", "") or ""),
            }
        )
        self.data["recent_attempts"] = recent[-80:]
        if self._should_write_attempt_record(status_key):
            self._append_record_file(self.attempt_path, attempt_record)
        self._rebuild_kpi_summary()
        self._save(force=bool(getattr(self, "_attempt_record_path_explicit", False)))

    # ─────────────────────────────────────────────
    def on_exit(
        self,
        *,
        entry: float,
        tp: float,
        sl: float,
        reason: str,
        side: str = None,
        amount: float = 1.0,
        exit_price: float = None,
        exploration_trade: bool = False,
        outcome_decomposition: dict = None,
        context: dict = None,
    ):
        pnl = 0.0

        side = str(side).upper().strip() if side is not None else "LONG"

        if reason == "tp_hit":
            if side == "LONG":
                pnl = (tp - entry) * float(amount)
            elif side == "SHORT":
                pnl = (entry - tp) * float(amount)
            else:
                return
            self.data["tp"] += 1

            if exploration_trade:
                self.data["exploration_tp"] = int(self.data.get("exploration_tp", 0) or 0) + 1

        elif reason == "sl_hit":
            if side == "LONG":
                pnl = (sl - entry) * float(amount)
            elif side == "SHORT":
                pnl = (entry - sl) * float(amount)
            else:
                return
            self.data["sl"] += 1

            if exploration_trade:
                self.data["exploration_sl"] = int(self.data.get("exploration_sl", 0) or 0) + 1

        elif reason == "matured_exit":
            try:
                resolved_exit_price = float(exit_price)
            except Exception:
                return
            if resolved_exit_price <= 0.0:
                return
            if side == "LONG":
                pnl = (resolved_exit_price - entry) * float(amount)
            elif side == "SHORT":
                pnl = (entry - resolved_exit_price) * float(amount)
            else:
                return
            self.data["matured_exits"] = int(self.data.get("matured_exits", 0) or 0) + 1
            if pnl >= 0:
                self.data["tp"] += 1
                if exploration_trade:
                    self.data["exploration_tp"] = int(self.data.get("exploration_tp", 0) or 0) + 1
            else:
                self.data["sl"] += 1
                if exploration_trade:
                    self.data["exploration_sl"] = int(self.data.get("exploration_sl", 0) or 0) + 1

        else:
            return

        exit_price = float(exit_price) if reason == "matured_exit" else (tp if reason == "tp_hit" else sl)
        fee_rate = getattr(Config, "FEE_RATE", 0.0) or 0.0
        fees = (
            (entry * float(amount) * fee_rate) +
            (exit_price * float(amount) * fee_rate) +
            (Config.FEE_PER_TRADE or 0.0)
        )
        pnl = pnl - fees

        normalized_context = self._normalize_record_value(context or {})
        compact_context = self._compact_context(normalized_context)
        normalized_decomposition = self._normalize_record_value(outcome_decomposition or {})
        raw_outcome_decomposition = dict(normalized_decomposition or {})

        def _context_section(name: str) -> dict:
            for source in (
                normalized_context,
                compact_context,
                dict(normalized_context.get("context", {}) or {}),
                dict(compact_context.get("context", {}) or {}),
            ):
                value = source.get(name, {}) if isinstance(source, dict) else {}
                if isinstance(value, dict) and value:
                    return dict(value)
            return {}

        exit_candidate_replay = self._record_exit_candidate_replay(
            entry=float(entry),
            side=str(side),
            amount=float(amount),
            actual_reason=str(reason or ""),
            actual_exit_price=float(exit_price),
            actual_pnl=float(pnl),
            context=normalized_context,
        )

        self.data["trades"] += 1
        self.data["last_outcome_decomposition"] = dict(raw_outcome_decomposition or {})
        if side == "LONG":
            self.data["long_trades"] = int(self.data.get("long_trades", 0) or 0) + 1
            self.data["long_pnl"] = float(self.data.get("long_pnl", 0.0) or 0.0) + float(pnl)
            if reason == "tp_hit" or (reason == "matured_exit" and pnl >= 0.0):
                self.data["long_tp"] = int(self.data.get("long_tp", 0) or 0) + 1
            elif reason == "sl_hit" or (reason == "matured_exit" and pnl < 0.0):
                self.data["long_sl"] = int(self.data.get("long_sl", 0) or 0) + 1
        elif side == "SHORT":
            self.data["short_trades"] = int(self.data.get("short_trades", 0) or 0) + 1
            self.data["short_pnl"] = float(self.data.get("short_pnl", 0.0) or 0.0) + float(pnl)
            if reason == "tp_hit" or (reason == "matured_exit" and pnl >= 0.0):
                self.data["short_tp"] = int(self.data.get("short_tp", 0) or 0) + 1
            elif reason == "sl_hit" or (reason == "matured_exit" and pnl < 0.0):
                self.data["short_sl"] = int(self.data.get("short_sl", 0) or 0) + 1

        if exploration_trade:
            self.data["exploration_trades"] = int(self.data.get("exploration_trades", 0) or 0) + 1
            self.data["exploration_pnl"] = float(self.data.get("exploration_pnl", 0.0) or 0.0) + float(pnl)

        self.data["pnl_netto"] = float(self.data.get("pnl_netto", 0.0) or 0.0) + float(pnl)
        self.data["current_equity"] = float(self.data.get("start_equity", 0.0) or 0.0) + float(self.data.get("pnl_netto", 0.0) or 0.0)
        self._sync_live_account_equity(reason="trade_exit")

        if pnl > 0:
            self.data["pnl_tp"] += pnl

        if pnl < 0:
            self.data["pnl_sl"] += pnl

        if reason == "matured_exit":
            self.data["matured_exit_pnl"] = float(self.data.get("matured_exit_pnl", 0.0) or 0.0) + float(pnl)

        structure_quality = self._extract_structure_quality(normalized_context)
        structure_bucket = "zone" if structure_quality >= 0.55 else "non_zone"
        form_symbol_state = _context_section("form_symbol_state")
        meta_regulation_state = _context_section("meta_regulation_state")
        neurochemical_state = _context_section("neurochemical_state") or dict(meta_regulation_state.get("neurochemical_state", {}) or {})
        active_mcm_contact_state = _context_section("active_mcm_contact_state") or dict(meta_regulation_state.get("active_mcm_contact", {}) or {})
        strategic_window_state = _context_section("strategic_window_state")
        trade_plan_state = _context_section("trade_plan")
        target_expectation_state = _context_section("target_expectation_state")
        thought_seed_state = _context_section("thought_seed_state")
        experience_state = _context_section("experience")
        experience_packet_feedback = dict(normalized_decomposition.get("experience_packet_feedback", {}) or {})

        def _f(*values, default=0.0):
            for value in values:
                try:
                    if value is None:
                        continue
                    return float(value)
                except Exception:
                    continue
            return float(default)

        def _clip(value):
            value = _f(value)
            if value != value:
                value = 0.0
            return max(0.0, min(1.0, float(value)))

        def _entry_contact_learning_source() -> dict:
            source = dict(trade_plan_state or {})
            fallback_keys = (
                "area_bearing_quality",
                "area_contact_timing_fit",
                "area_action_timing_fit",
                "area_spacetime_fit",
                "area_present_contact",
                "area_invalidity_pressure",
                "area_afterimage",
                "area_contact_distance_fit",
                "contact_entry_fit",
                "strategic_entry_fit",
                "entry_contact_bearing",
                "area_contact_readiness",
                "receptive_contact_maturity",
                "receptive_contact_immaturity_pressure",
                "real_area_contact_bearing",
                "felt_reality_bearing",
                "form_mcm_reality_fit",
                "energy_coherence_bearing",
            )
            for fallback in (strategic_window_state, meta_regulation_state, active_mcm_contact_state, compact_context):
                if not isinstance(fallback, dict):
                    continue
                for key in fallback_keys:
                    if key in source and source.get(key) not in (None, "", 0, 0.0):
                        continue
                    if key in fallback:
                        source[key] = fallback.get(key)
            return source

        rr_value = _f(trade_plan_state.get("rr_value"), default=0.0)
        structural_run_room = _clip((rr_value - 1.6) / 3.2)
        target_expectation_value = _clip(
            target_expectation_state.get(
                "tp_reachability",
                target_expectation_state.get(
                    "base_target_expectation",
                    experience_state.get("target_expectation", 0.0),
                ),
            )
        )
        emergent_structure_reading = _clip(
            (structural_run_room * 0.24)
            + (_clip(meta_regulation_state.get("future_projection_depth", 0.0)) * 0.16)
            + (_clip(meta_regulation_state.get("mcm_spacetime_depth", 0.0)) * 0.14)
            + (_clip(strategic_window_state.get("area_bearing_quality", meta_regulation_state.get("area_bearing_quality", 0.0))) * 0.14)
            + (_clip(trade_plan_state.get("entry_contact_bearing", trade_plan_state.get("entry_choice_bearing", 0.0))) * 0.12)
            + (_clip(active_mcm_contact_state.get("contact_action_maturity", meta_regulation_state.get("contact_action_maturity", 0.0))) * 0.10)
            + (target_expectation_value * 0.10)
            - (_clip(meta_regulation_state.get("spacetime_unlocated_pressure", 0.0)) * 0.10)
            - (_clip(meta_regulation_state.get("contact_regime_mismatch", 0.0)) * 0.08)
        )
        emergent_structure_confirmation = _clip(
            (emergent_structure_reading * 0.42)
            + (_clip(normalized_decomposition.get("plan_quality", 0.0)) * 0.16)
            + (_clip(normalized_decomposition.get("execution_quality", 0.0)) * 0.14)
            + (_clip(normalized_decomposition.get("risk_fit_quality", 0.0)) * 0.12)
            + (_clip(normalized_decomposition.get("position_constructive_bearing", 0.0)) * 0.10)
            + (0.12 if reason == "tp_hit" and rr_value >= 2.4 else 0.0)
            - (0.10 if reason == "sl_hit" and rr_value >= 2.4 else 0.0)
        )
        if emergent_structure_reading >= 0.52 and emergent_structure_confirmation >= 0.50:
            emergent_structure_state = "confirmed_structure_contact"
        elif emergent_structure_reading >= 0.44 and rr_value >= 2.4:
            emergent_structure_state = "open_structure_contact"
        elif rr_value >= 2.4 and emergent_structure_reading < 0.34:
            emergent_structure_state = "wide_range_without_structure"
        else:
            emergent_structure_state = "ordinary_structure_contact"
        open_hypothesis_learning = self._derive_open_hypothesis_learning(
            {
                "reason": str(reason or "").strip().lower(),
                "pnl": float(pnl),
                "rr_value": float(rr_value),
                "emergent_structure_reading": float(emergent_structure_reading),
                "emergent_structure_confirmation": float(emergent_structure_confirmation),
                "emergent_structure_state": str(emergent_structure_state),
                "thought_seed_structural_grounding": float(thought_seed_state.get("thought_structural_grounding", 0.0) or 0.0),
                "thought_seed_open_hypothesis_pressure": float(thought_seed_state.get("thought_open_hypothesis_pressure", 0.0) or 0.0),
                "thought_seed_reality_lag": float(thought_seed_state.get("thought_reality_lag", 0.0) or 0.0),
                "thought_seed_consequence_balance": float(thought_seed_state.get("thought_consequence_balance", 0.0) or 0.0),
            },
            emergent_state=str(emergent_structure_state),
        )
        normalized_decomposition.update({
            "emergent_structure_reading": float(emergent_structure_reading),
            "emergent_structure_confirmation": float(emergent_structure_confirmation),
            "emergent_structure_state": str(emergent_structure_state),
            "open_hypothesis_learning_state": str(open_hypothesis_learning.get("open_hypothesis_learning_state", "-") or "-"),
            "open_hypothesis_consequence_score": float(open_hypothesis_learning.get("open_hypothesis_consequence_score", 0.0) or 0.0),
            "open_hypothesis_burden_score": float(open_hypothesis_learning.get("open_hypothesis_burden_score", 0.0) or 0.0),
            "open_hypothesis_reorganization_score": float(open_hypothesis_learning.get("open_hypothesis_reorganization_score", 0.0) or 0.0),
            "open_hypothesis_replay_need": float(open_hypothesis_learning.get("open_hypothesis_replay_need", 0.0) or 0.0),
            "open_hypothesis_distance_need": float(open_hypothesis_learning.get("open_hypothesis_distance_need", 0.0) or 0.0),
            "open_hypothesis_reinterpretation_need": float(open_hypothesis_learning.get("open_hypothesis_reinterpretation_need", 0.0) or 0.0),
            "open_hypothesis_reorganization_posture": str(open_hypothesis_learning.get("open_hypothesis_reorganization_posture", "-") or "-"),
        })
        entry_contact_preference_feedback = self._update_entry_contact_learning(
            side=str(side),
            reason=str(reason or "").strip().lower(),
            pnl=float(pnl),
            trade_plan_state=_entry_contact_learning_source(),
            outcome_decomposition=normalized_decomposition,
        )
        if entry_contact_preference_feedback:
            normalized_decomposition.update(
                {
                    "entry_contact_preference_key": str(entry_contact_preference_feedback.get("key", "-") or "-"),
                    "entry_contact_preference_state": str(entry_contact_preference_feedback.get("last_state", "-") or "-"),
                    "entry_contact_preference_trust": float(entry_contact_preference_feedback.get("trust", 0.0) or 0.0),
                    "entry_contact_preference_caution": float(entry_contact_preference_feedback.get("caution", 0.0) or 0.0),
                    "entry_contact_preference_maturity": float(entry_contact_preference_feedback.get("maturity", 0.0) or 0.0),
                    "entry_contact_preference_utility": float(entry_contact_preference_feedback.get("utility", 0.0) or 0.0),
                    "entry_property_profile_id": str(entry_contact_preference_feedback.get("property_profile_id", "-") or "-"),
                    "entry_property_profile_state": str(entry_contact_preference_feedback.get("property_profile_state", "-") or "-"),
                    "entry_property_profile_similarity": float(entry_contact_preference_feedback.get("property_profile_similarity", 0.0) or 0.0),
                    "entry_property_profile_trust": float(entry_contact_preference_feedback.get("property_profile_trust", 0.0) or 0.0),
                    "entry_property_profile_caution": float(entry_contact_preference_feedback.get("property_profile_caution", 0.0) or 0.0),
                    "entry_property_profile_maturity": float(entry_contact_preference_feedback.get("property_profile_maturity", 0.0) or 0.0),
                    "entry_property_profile_utility": float(entry_contact_preference_feedback.get("property_profile_utility", 0.0) or 0.0),
                }
            )
        self.data["last_outcome_decomposition"] = dict(raw_outcome_decomposition or {})
        self.data["last_outcome_decomposition_enriched"] = dict(normalized_decomposition or {})

        outcome_record = {
            "event": "trade_exit",
            "reason": str(reason or "").strip().lower(),
            "timestamp": self.data.get("current_timestamp"),
            "side": side,
            "entry": float(entry),
            "tp": float(tp),
            "sl": float(sl),
            "exit_price": float(exit_price),
            "amount": float(amount),
            "pnl": float(pnl),
            "rr_value": float(rr_value),
            "structural_run_room": float(structural_run_room),
            "emergent_structure_reading": float(emergent_structure_reading),
            "emergent_structure_confirmation": float(emergent_structure_confirmation),
            "emergent_structure_state": str(emergent_structure_state),
            "open_hypothesis_learning_state": str(open_hypothesis_learning.get("open_hypothesis_learning_state", "-") or "-"),
            "open_hypothesis_consequence_score": float(open_hypothesis_learning.get("open_hypothesis_consequence_score", 0.0) or 0.0),
            "open_hypothesis_burden_score": float(open_hypothesis_learning.get("open_hypothesis_burden_score", 0.0) or 0.0),
            "open_hypothesis_reorganization_score": float(open_hypothesis_learning.get("open_hypothesis_reorganization_score", 0.0) or 0.0),
            "open_hypothesis_replay_need": float(open_hypothesis_learning.get("open_hypothesis_replay_need", 0.0) or 0.0),
            "open_hypothesis_distance_need": float(open_hypothesis_learning.get("open_hypothesis_distance_need", 0.0) or 0.0),
            "open_hypothesis_reinterpretation_need": float(open_hypothesis_learning.get("open_hypothesis_reinterpretation_need", 0.0) or 0.0),
            "open_hypothesis_reorganization_posture": str(open_hypothesis_learning.get("open_hypothesis_reorganization_posture", "-") or "-"),
            "entry_contact_preference_key": str(entry_contact_preference_feedback.get("key", "-") or "-"),
            "entry_contact_preference_state": str(entry_contact_preference_feedback.get("last_state", "-") or "-"),
            "entry_contact_preference_trust": float(entry_contact_preference_feedback.get("trust", 0.0) or 0.0),
            "entry_contact_preference_caution": float(entry_contact_preference_feedback.get("caution", 0.0) or 0.0),
            "entry_contact_preference_maturity": float(entry_contact_preference_feedback.get("maturity", 0.0) or 0.0),
            "entry_contact_preference_utility": float(entry_contact_preference_feedback.get("utility", 0.0) or 0.0),
            "entry_property_profile_id": str(entry_contact_preference_feedback.get("property_profile_id", "-") or "-"),
            "entry_property_profile_state": str(entry_contact_preference_feedback.get("property_profile_state", "-") or "-"),
            "entry_property_profile_similarity": float(entry_contact_preference_feedback.get("property_profile_similarity", 0.0) or 0.0),
            "entry_property_profile_trust": float(entry_contact_preference_feedback.get("property_profile_trust", 0.0) or 0.0),
            "entry_property_profile_caution": float(entry_contact_preference_feedback.get("property_profile_caution", 0.0) or 0.0),
            "entry_property_profile_maturity": float(entry_contact_preference_feedback.get("property_profile_maturity", 0.0) or 0.0),
            "entry_property_profile_utility": float(entry_contact_preference_feedback.get("property_profile_utility", 0.0) or 0.0),
            "thought_seed_id": str(thought_seed_state.get("thought_seed_id", "") or ""),
            "thought_seed_label": str(thought_seed_state.get("thought_seed_label", "") or ""),
            "thought_seed_metaregulator_state": str(thought_seed_state.get("seed_metaregulator_state", "") or ""),
            "thought_seed_emergent_state": str(thought_seed_state.get("emergent_structure_state", "") or ""),
            "thought_seed_trace_strength": float(thought_seed_state.get("thought_trace_strength", 0.0) or 0.0),
            "thought_seed_maturity": float(thought_seed_state.get("thought_maturity", 0.0) or 0.0),
            "thought_seed_reality_binding": float(thought_seed_state.get("reality_binding_score", 0.0) or 0.0),
            "thought_seed_confirmation": float(thought_seed_state.get("thought_confirmation_score", 0.0) or 0.0),
            "thought_seed_consequence_echo": float(thought_seed_state.get("consequence_echo", 0.0) or 0.0),
            "thought_seed_reorganization_echo": float(thought_seed_state.get("reorganization_echo", 0.0) or 0.0),
            "thought_seed_consequence_alignment": float(thought_seed_state.get("thought_consequence_alignment", 0.0) or 0.0),
            "thought_seed_consequence_balance": float(thought_seed_state.get("thought_consequence_balance", 0.0) or 0.0),
            "thought_seed_reality_lag": float(thought_seed_state.get("thought_reality_lag", 0.0) or 0.0),
            "thought_seed_structural_grounding": float(thought_seed_state.get("thought_structural_grounding", 0.0) or 0.0),
            "thought_seed_open_hypothesis_pressure": float(thought_seed_state.get("thought_open_hypothesis_pressure", 0.0) or 0.0),
            "thought_seed_replay_maturation_pull": float(thought_seed_state.get("thought_replay_maturation_pull", 0.0) or 0.0),
            "thought_seed_distance_maturation_pull": float(thought_seed_state.get("thought_distance_maturation_pull", 0.0) or 0.0),
            "thought_seed_reinterpretation_pull": float(thought_seed_state.get("thought_reinterpretation_pull", 0.0) or 0.0),
            "thought_seed_digestive_replay_pull": float(thought_seed_state.get("thought_digestive_replay_pull", 0.0) or 0.0),
            "thought_seed_digestive_distance_pull": float(thought_seed_state.get("thought_digestive_distance_pull", 0.0) or 0.0),
            "thought_seed_digestive_integration_pull": float(thought_seed_state.get("thought_digestive_integration_pull", 0.0) or 0.0),
            "thought_seed_digestive_returned_trust": float(thought_seed_state.get("thought_digestive_returned_trust", 0.0) or 0.0),
            "thought_seed_trust_return_readiness": float(thought_seed_state.get("trust_return_readiness", 0.0) or 0.0),
            "thought_seed_digest_state": str(thought_seed_state.get("thought_digest_state", "") or ""),
            "thought_seed_reifung_direction": str(thought_seed_state.get("thought_reifung_direction", "") or ""),
            "thought_seed_semantic_origin_state": str(thought_seed_state.get("semantic_origin_state", "") or ""),
            "thought_seed_borrowed_open_hypothesis_pressure": float(thought_seed_state.get("borrowed_open_hypothesis_pressure", 0.0) or 0.0),
            "thought_seed_own_field_binding_pull": float(thought_seed_state.get("own_field_binding_pull", 0.0) or 0.0),
            "semantic_origin_state": str(meta_regulation_state.get("semantic_origin_state", "") or ""),
            "own_field_identity_strength": float(meta_regulation_state.get("own_field_identity_strength", 0.0) or 0.0),
            "foreign_semantic_pressure": float(meta_regulation_state.get("foreign_semantic_pressure", 0.0) or 0.0),
            "adopted_language_pressure": float(meta_regulation_state.get("adopted_language_pressure", 0.0) or 0.0),
            "self_foreign_boundary_clarity": float(meta_regulation_state.get("self_foreign_boundary_clarity", 0.0) or 0.0),
            "semantic_origin_conflict": float(meta_regulation_state.get("semantic_origin_conflict", 0.0) or 0.0),
            "own_vs_foreign_margin": float(meta_regulation_state.get("own_vs_foreign_margin", 0.0) or 0.0),
            "borrowed_vs_own_margin": float(meta_regulation_state.get("borrowed_vs_own_margin", 0.0) or 0.0),
            "boundary_support_margin": float(meta_regulation_state.get("boundary_support_margin", 0.0) or 0.0),
            "thought_seed_drift_risk": float(thought_seed_state.get("hallucination_drift_risk", 0.0) or 0.0),
            "thought_seed_overthinking_risk": float(thought_seed_state.get("overthinking_risk", 0.0) or 0.0),
            "target_expectation_value": float(target_expectation_value),
            "structure_quality": float(structure_quality),
            "structure_bucket": structure_bucket,
            "form_symbol_id": str(form_symbol_state.get("form_symbol_id", "") or ""),
            "form_symbol_development_quality": float(form_symbol_state.get("form_symbol_development_quality", 0.0) or 0.0),
            "form_symbol_action_binding": float(form_symbol_state.get("form_symbol_action_binding", 0.0) or 0.0),
            "form_symbol_observation_binding": float(form_symbol_state.get("form_symbol_observation_binding", 0.0) or 0.0),
            "form_symbol_reframe_binding": float(form_symbol_state.get("form_symbol_reframe_binding", 0.0) or 0.0),
            "form_symbol_learning_trust": float(form_symbol_state.get("form_symbol_learning_trust", 0.0) or 0.0),
            "form_symbol_action_trust": float(form_symbol_state.get("form_symbol_action_trust", 0.0) or 0.0),
            "form_symbol_caution_trust": float(form_symbol_state.get("form_symbol_caution_trust", 0.0) or 0.0),
            "form_symbol_contact_maturity": float(form_symbol_state.get("form_symbol_contact_maturity", meta_regulation_state.get("form_symbol_contact_maturity", 0.0)) or 0.0),
            "form_symbol_contact_utility": float(form_symbol_state.get("form_symbol_contact_utility", meta_regulation_state.get("form_symbol_contact_utility", 0.0)) or 0.0),
            "form_symbol_contact_pain_memory": float(form_symbol_state.get("form_symbol_contact_pain_memory", meta_regulation_state.get("form_symbol_contact_pain_memory", 0.0)) or 0.0),
            "form_symbol_contact_carefulness": float(form_symbol_state.get("form_symbol_contact_carefulness", meta_regulation_state.get("form_symbol_contact_carefulness", 0.0)) or 0.0),
            "form_symbol_contact_burden_evidence": float(form_symbol_state.get("form_symbol_contact_burden_evidence", meta_regulation_state.get("form_symbol_contact_burden_evidence", 0.0)) or 0.0),
            "form_symbol_contact_utility_evidence": float(form_symbol_state.get("form_symbol_contact_utility_evidence", meta_regulation_state.get("form_symbol_contact_utility_evidence", 0.0)) or 0.0),
            "form_symbol_contact_learning_state": str(form_symbol_state.get("form_symbol_contact_learning_state", meta_regulation_state.get("form_symbol_contact_learning_state", "")) or ""),
            "form_contact_maturity_sample": float(normalized_decomposition.get("contact_maturity_sample", 0.0) or 0.0),
            "form_contact_utility_sample": float(normalized_decomposition.get("contact_utility_sample", 0.0) or 0.0),
            "form_contact_pain_sample": float(normalized_decomposition.get("contact_pain_sample", 0.0) or 0.0),
            "form_contact_carefulness_sample": float(normalized_decomposition.get("contact_carefulness_sample", 0.0) or 0.0),
            "form_contact_learning_state": str(normalized_decomposition.get("contact_learning_state", "") or ""),
            "position_consequence_burden": float(normalized_decomposition.get("position_consequence_burden", 0.0) or 0.0),
            "position_consequence_residual_for_care": float(normalized_decomposition.get("position_consequence_residual_for_care", 0.0) or 0.0),
            "position_consequence_residual_for_memory": float(normalized_decomposition.get("position_consequence_residual_for_memory", 0.0) or 0.0),
            "position_constructive_bearing": float(normalized_decomposition.get("position_constructive_bearing", 0.0) or 0.0),
            "transitional_contact_band": float(normalized_decomposition.get("transitional_contact_band", 0.0) or 0.0),
            "transitional_contact_maturation": float(normalized_decomposition.get("transitional_contact_maturation", 0.0) or 0.0),
            "position_feedback_label": str(normalized_decomposition.get("position_feedback_label", "") or ""),
            "position_process_quality_feedback": float(normalized_decomposition.get("position_process_quality", 0.0) or 0.0),
            "position_held_risk_discomfort_feedback": float(normalized_decomposition.get("position_held_risk_discomfort", 0.0) or 0.0),
            "position_cortisol_load_feedback": float(normalized_decomposition.get("position_cortisol_load", 0.0) or 0.0),
            "position_noradrenaline_arousal_feedback": float(normalized_decomposition.get("position_noradrenaline_arousal", 0.0) or 0.0),
            "form_symbol_compound_id": str(form_symbol_state.get("form_symbol_compound_id", "") or ""),
            "form_symbol_compound_development_quality": float(form_symbol_state.get("form_symbol_compound_development_quality", 0.0) or 0.0),
            "uncertain_form_family_state": str(form_symbol_state.get("uncertain_form_family_state", meta_regulation_state.get("uncertain_form_family_state", "")) or ""),
            "uncertain_form_exposure": float(form_symbol_state.get("uncertain_form_exposure", meta_regulation_state.get("uncertain_form_exposure", 0.0)) or 0.0),
            "uncertainty_familiarity": float(form_symbol_state.get("uncertainty_familiarity", meta_regulation_state.get("uncertainty_familiarity", 0.0)) or 0.0),
            "variant_similarity": float(form_symbol_state.get("variant_similarity", meta_regulation_state.get("variant_similarity", 0.0)) or 0.0),
            "variant_spread": float(form_symbol_state.get("variant_spread", meta_regulation_state.get("variant_spread", 0.0)) or 0.0),
            "variant_learning_pressure": float(form_symbol_state.get("variant_learning_pressure", meta_regulation_state.get("variant_learning_pressure", 0.0)) or 0.0),
            "variant_bearing_memory": float(form_symbol_state.get("variant_bearing_memory", meta_regulation_state.get("variant_bearing_memory", 0.0)) or 0.0),
            "form_symbol_semantic_density": float(form_symbol_state.get("form_symbol_semantic_density", 0.0) or 0.0),
            "form_symbol_semantic_compression": float(form_symbol_state.get("form_symbol_semantic_compression", 0.0) or 0.0),
            "form_symbol_semantic_coherence": float(form_symbol_state.get("form_symbol_semantic_coherence", 0.0) or 0.0),
            "form_symbol_semantic_learning_need": float(form_symbol_state.get("form_symbol_semantic_learning_need", 0.0) or 0.0),
            "form_symbol_semantic_action_nearness": float(form_symbol_state.get("form_symbol_semantic_action_nearness", 0.0) or 0.0),
            "form_symbol_semantic_primary_layer": str(form_symbol_state.get("form_symbol_semantic_primary_layer", "") or ""),
            "form_symbol_semantic_layer_count": int(form_symbol_state.get("form_symbol_semantic_layer_count", 0) or 0),
            "form_symbol_semantic_packet_state": str(form_symbol_state.get("form_symbol_semantic_packet_state", "") or ""),
            "form_symbol_semantic_profile": str(form_symbol_state.get("form_symbol_semantic_profile", "") or ""),
            "visual_blind_action_load": float(meta_regulation_state.get("visual_blind_action_load", 0.0) or 0.0),
            "visual_action_uncertainty": float(meta_regulation_state.get("visual_action_uncertainty", 0.0) or 0.0),
            "visual_object_binding": float(meta_regulation_state.get("visual_object_binding", 0.0) or 0.0),
            "visual_grounding_strength": float(meta_regulation_state.get("visual_grounding_strength", 0.0) or 0.0),
            "visual_resonance_unbound": float(meta_regulation_state.get("visual_resonance_unbound", 0.0) or 0.0),
            "visual_grounding_gap": float(meta_regulation_state.get("visual_grounding_gap", 0.0) or 0.0),
            "visual_grounding_need": float(meta_regulation_state.get("visual_grounding_need", 0.0) or 0.0),
            "visual_rational_observation_support": float(meta_regulation_state.get("visual_rational_observation_support", 0.0) or 0.0),
            "visual_grounding_state": str(meta_regulation_state.get("visual_grounding_state", "") or ""),
            "neurochemical_state_label": str(neurochemical_state.get("neurochemical_state_label", meta_regulation_state.get("neurochemical_state_label", "")) or ""),
            "neurochemical_dominant_tone": str(neurochemical_state.get("neurochemical_dominant_tone", meta_regulation_state.get("neurochemical_dominant_tone", "")) or ""),
            "dopamine_tone": float(neurochemical_state.get("dopamine_tone", meta_regulation_state.get("dopamine_tone", 0.0)) or 0.0),
            "gaba_inhibition": float(neurochemical_state.get("gaba_inhibition", meta_regulation_state.get("gaba_inhibition", 0.0)) or 0.0),
            "noradrenaline_arousal": float(neurochemical_state.get("noradrenaline_arousal", meta_regulation_state.get("noradrenaline_arousal", 0.0)) or 0.0),
            "acetylcholine_focus": float(neurochemical_state.get("acetylcholine_focus", meta_regulation_state.get("acetylcholine_focus", 0.0)) or 0.0),
            "serotonin_stability": float(neurochemical_state.get("serotonin_stability", meta_regulation_state.get("serotonin_stability", 0.0)) or 0.0),
            "cortisol_load": float(neurochemical_state.get("cortisol_load", meta_regulation_state.get("cortisol_load", 0.0)) or 0.0),
            "endorphin_relief": float(neurochemical_state.get("endorphin_relief", meta_regulation_state.get("endorphin_relief", 0.0)) or 0.0),
            "glutamate_activation": float(neurochemical_state.get("glutamate_activation", meta_regulation_state.get("glutamate_activation", 0.0)) or 0.0),
            "neurochemical_load": float(neurochemical_state.get("neurochemical_load", meta_regulation_state.get("neurochemical_load", 0.0)) or 0.0),
            "neurochemical_support": float(neurochemical_state.get("neurochemical_support", meta_regulation_state.get("neurochemical_support", 0.0)) or 0.0),
            "neurochemical_balance": float(neurochemical_state.get("neurochemical_balance", meta_regulation_state.get("neurochemical_balance", 0.0)) or 0.0),
            "reward_stability_echo": float(neurochemical_state.get("reward_stability_echo", meta_regulation_state.get("reward_stability_echo", 0.0)) or 0.0),
            "world_shift_evidence": float(neurochemical_state.get("world_shift_evidence", meta_regulation_state.get("world_shift_evidence", 0.0)) or 0.0),
            "serotonin_carryover_risk": float(neurochemical_state.get("serotonin_carryover_risk", meta_regulation_state.get("serotonin_carryover_risk", 0.0)) or 0.0),
            "emotional_decoupling": float(neurochemical_state.get("emotional_decoupling", meta_regulation_state.get("emotional_decoupling", 0.0)) or 0.0),
            "reactive_nervous_drive": float(neurochemical_state.get("reactive_nervous_drive", meta_regulation_state.get("reactive_nervous_drive", 0.0)) or 0.0),
            "active_mcm_contact_state": str(active_mcm_contact_state.get("active_mcm_contact_state", meta_regulation_state.get("active_mcm_contact_state", "")) or ""),
            "contact_posture": str(active_mcm_contact_state.get("contact_posture", meta_regulation_state.get("contact_posture", "")) or ""),
            "contact_interest": float(active_mcm_contact_state.get("contact_interest", meta_regulation_state.get("contact_interest", 0.0)) or 0.0),
            "contact_focus_pull": float(active_mcm_contact_state.get("contact_focus_pull", meta_regulation_state.get("contact_focus_pull", 0.0)) or 0.0),
            "contact_resonance_probe": float(active_mcm_contact_state.get("contact_resonance_probe", meta_regulation_state.get("contact_resonance_probe", 0.0)) or 0.0),
            "outer_inner_resonance": float(active_mcm_contact_state.get("outer_inner_resonance", meta_regulation_state.get("outer_inner_resonance", 0.0)) or 0.0),
            "outer_inner_coherence": float(active_mcm_contact_state.get("outer_inner_coherence", meta_regulation_state.get("outer_inner_coherence", 0.0)) or 0.0),
            "inner_change_from_contact": float(active_mcm_contact_state.get("inner_change_from_contact", meta_regulation_state.get("inner_change_from_contact", 0.0)) or 0.0),
            "contact_carrying_quality": float(active_mcm_contact_state.get("contact_carrying_quality", meta_regulation_state.get("contact_carrying_quality", 0.0)) or 0.0),
            "contact_overcoupling_risk": float(active_mcm_contact_state.get("contact_overcoupling_risk", meta_regulation_state.get("contact_overcoupling_risk", 0.0)) or 0.0),
            "contact_release_readiness": float(active_mcm_contact_state.get("contact_release_readiness", meta_regulation_state.get("contact_release_readiness", 0.0)) or 0.0),
            "contact_deepen_pull": float(active_mcm_contact_state.get("contact_deepen_pull", meta_regulation_state.get("contact_deepen_pull", 0.0)) or 0.0),
            "contact_replay_pull": float(active_mcm_contact_state.get("contact_replay_pull", meta_regulation_state.get("contact_replay_pull", 0.0)) or 0.0),
            "contact_curiosity": float(active_mcm_contact_state.get("contact_curiosity", meta_regulation_state.get("contact_curiosity", 0.0)) or 0.0),
            "contact_felt_shift": float(active_mcm_contact_state.get("contact_felt_shift", meta_regulation_state.get("contact_felt_shift", 0.0)) or 0.0),
            "contact_selected_depth": float(active_mcm_contact_state.get("contact_selected_depth", meta_regulation_state.get("contact_selected_depth", 0.0)) or 0.0),
            "contact_salience": float(active_mcm_contact_state.get("contact_salience", meta_regulation_state.get("contact_salience", 0.0)) or 0.0),
            "overcoupled_touch_score": float(active_mcm_contact_state.get("overcoupled_touch_score", meta_regulation_state.get("overcoupled_touch_score", 0.0)) or 0.0),
            "release_contact_score": float(active_mcm_contact_state.get("release_contact_score", meta_regulation_state.get("release_contact_score", 0.0)) or 0.0),
            "deepening_contact_score": float(active_mcm_contact_state.get("deepening_contact_score", meta_regulation_state.get("deepening_contact_score", 0.0)) or 0.0),
            "resonant_contact_score": float(active_mcm_contact_state.get("resonant_contact_score", meta_regulation_state.get("resonant_contact_score", 0.0)) or 0.0),
            "reflective_contact_score": float(active_mcm_contact_state.get("reflective_contact_score", meta_regulation_state.get("reflective_contact_score", 0.0)) or 0.0),
            "curious_touch_score": float(active_mcm_contact_state.get("curious_touch_score", meta_regulation_state.get("curious_touch_score", 0.0)) or 0.0),
            "contact_action_maturity": float(active_mcm_contact_state.get("contact_action_maturity", meta_regulation_state.get("contact_action_maturity", 0.0)) or 0.0),
            "contact_bearing_gap": float(active_mcm_contact_state.get("contact_bearing_gap", meta_regulation_state.get("contact_bearing_gap", 0.0)) or 0.0),
            "contact_impulse_vs_bearing": float(active_mcm_contact_state.get("contact_impulse_vs_bearing", meta_regulation_state.get("contact_impulse_vs_bearing", 0.0)) or 0.0),
            "contact_learning_need": float(active_mcm_contact_state.get("contact_learning_need", meta_regulation_state.get("contact_learning_need", 0.0)) or 0.0),
            "contact_reality_check": float(active_mcm_contact_state.get("contact_reality_check", meta_regulation_state.get("contact_reality_check", 0.0)) or 0.0),
            "contact_regime_mismatch": float(active_mcm_contact_state.get("contact_regime_mismatch", meta_regulation_state.get("contact_regime_mismatch", 0.0)) or 0.0),
            "contact_stability_carryover": float(active_mcm_contact_state.get("contact_stability_carryover", meta_regulation_state.get("contact_stability_carryover", 0.0)) or 0.0),
            "contact_context_maturity": float(active_mcm_contact_state.get("contact_context_maturity", meta_regulation_state.get("contact_context_maturity", 0.0)) or 0.0),
            "contact_context_reframe_need": float(active_mcm_contact_state.get("contact_context_reframe_need", meta_regulation_state.get("contact_context_reframe_need", 0.0)) or 0.0),
            "conscious_perception_state": str(meta_regulation_state.get("conscious_perception_state", "") or ""),
            "inner_posture_state": str(meta_regulation_state.get("inner_posture_state", "") or ""),
            "arousal_load": float(meta_regulation_state.get("arousal_load", 0.0) or 0.0),
            "curiosity_tone": float(meta_regulation_state.get("curiosity_tone", 0.0) or 0.0),
            "fatigue_tone": float(meta_regulation_state.get("fatigue_tone", 0.0) or 0.0),
            "calm_tone": float(meta_regulation_state.get("calm_tone", 0.0) or 0.0),
            "stimulus_field_effect": float(meta_regulation_state.get("stimulus_field_effect", 0.0) or 0.0),
            "inner_impact_trace": float(meta_regulation_state.get("inner_impact_trace", 0.0) or 0.0),
            "perceived_field_change": float(meta_regulation_state.get("perceived_field_change", 0.0) or 0.0),
            "felt_afterimage": float(meta_regulation_state.get("felt_afterimage", 0.0) or 0.0),
            "object_release_state": str(meta_regulation_state.get("object_release_state", "") or ""),
            "inner_outer_reflection": float(meta_regulation_state.get("inner_outer_reflection", 0.0) or 0.0),
            "perceptual_distance": float(meta_regulation_state.get("perceptual_distance", 0.0) or 0.0),
            "object_contact_depth": float(meta_regulation_state.get("object_contact_depth", 0.0) or 0.0),
            "field_attachment": float(meta_regulation_state.get("field_attachment", 0.0) or 0.0),
            "release_capacity": float(meta_regulation_state.get("release_capacity", 0.0) or 0.0),
            "selective_attention": float(meta_regulation_state.get("selective_attention", 0.0) or 0.0),
            "background_containment": float(meta_regulation_state.get("background_containment", 0.0) or 0.0),
            "reflective_distance": float(meta_regulation_state.get("reflective_distance", 0.0) or 0.0),
            "inner_outer_alignment": float(meta_regulation_state.get("inner_outer_alignment", 0.0) or 0.0),
            "engaged_effort": float(meta_regulation_state.get("engaged_effort", 0.0) or 0.0),
            "effort_state": str(meta_regulation_state.get("effort_state", "") or ""),
            "effort_learning_pull": float(meta_regulation_state.get("effort_learning_pull", 0.0) or 0.0),
            "effort_reorganization_pressure": float(meta_regulation_state.get("effort_reorganization_pressure", 0.0) or 0.0),
            "pre_action_reorganization_pressure": float(meta_regulation_state.get("pre_action_reorganization_pressure", 0.0) or 0.0),
            "pre_action_context_selectivity": float(meta_regulation_state.get("pre_action_context_selectivity", 0.0) or 0.0),
            "previous_packet_label": str(meta_regulation_state.get("previous_packet_label", "") or ""),
            "previous_packet_process_reward": float(meta_regulation_state.get("previous_packet_process_reward", 0.0) or 0.0),
            "previous_packet_reorganization_need": float(meta_regulation_state.get("previous_packet_reorganization_need", 0.0) or 0.0),
            "diffuse_open_development_pressure": float(meta_regulation_state.get("diffuse_open_development_pressure", 0.0) or 0.0),
            "posture_development_hint": str(meta_regulation_state.get("posture_development_hint", "") or ""),
            "metaregulator_state": str(meta_regulation_state.get("metaregulator_state", "") or ""),
            "metaregulator_balance": float(meta_regulation_state.get("metaregulator_balance", 0.0) or 0.0),
            "regulatory_second_order_load": float(meta_regulation_state.get("regulatory_second_order_load", 0.0) or 0.0),
            "subconscious_field_pressure": float(meta_regulation_state.get("subconscious_field_pressure", 0.0) or 0.0),
            "subconscious_habituation": float(meta_regulation_state.get("subconscious_habituation", 0.0) or 0.0),
            "subconscious_filter_strength": float(meta_regulation_state.get("subconscious_filter_strength", 0.0) or 0.0),
            "subconscious_buffering": float(meta_regulation_state.get("subconscious_buffering", 0.0) or 0.0),
            "subconscious_leakage": float(meta_regulation_state.get("subconscious_leakage", 0.0) or 0.0),
            "subconscious_afterimage_depth": float(meta_regulation_state.get("subconscious_afterimage_depth", 0.0) or 0.0),
            "subconscious_afterimage_pressure": float(meta_regulation_state.get("subconscious_afterimage_pressure", 0.0) or 0.0),
            "subconscious_afterimage_bearing": float(meta_regulation_state.get("subconscious_afterimage_bearing", 0.0) or 0.0),
            "subconscious_afterimage_clarity": float(meta_regulation_state.get("subconscious_afterimage_clarity", 0.0) or 0.0),
            "subconscious_afterimage_release": float(meta_regulation_state.get("subconscious_afterimage_release", 0.0) or 0.0),
            "subconscious_afterimage_reflection_pull": float(meta_regulation_state.get("subconscious_afterimage_reflection_pull", 0.0) or 0.0),
            "conscious_selection_pressure": float(meta_regulation_state.get("conscious_selection_pressure", 0.0) or 0.0),
            "conscious_workspace_focus": float(meta_regulation_state.get("conscious_workspace_focus", 0.0) or 0.0),
            "conscious_workspace_load": float(meta_regulation_state.get("conscious_workspace_load", 0.0) or 0.0),
            "conscious_gate_balance": float(meta_regulation_state.get("conscious_gate_balance", 0.0) or 0.0),
            "integration_strain_value": float(meta_regulation_state.get("integration_strain_value", 0.0) or 0.0),
            "integration_sorting_need": float(meta_regulation_state.get("integration_sorting_need", 0.0) or 0.0),
            "integration_reframe_pull": float(meta_regulation_state.get("integration_reframe_pull", 0.0) or 0.0),
            "integration_memory_recall": float(meta_regulation_state.get("integration_memory_recall", 0.0) or 0.0),
            "integration_contact_deepening": float(meta_regulation_state.get("integration_contact_deepening", 0.0) or 0.0),
            "integration_response_strength": float(meta_regulation_state.get("integration_response_strength", 0.0) or 0.0),
            "integration_response_state": str(meta_regulation_state.get("integration_response_state", "") or ""),
            "cautious_hypothesis_strength": float(meta_regulation_state.get("cautious_hypothesis_strength", 0.0) or 0.0),
            "cautious_hypothesis_clarity": float(meta_regulation_state.get("cautious_hypothesis_clarity", 0.0) or 0.0),
            "cautious_hypothesis_patience": float(meta_regulation_state.get("cautious_hypothesis_patience", 0.0) or 0.0),
            "cautious_hypothesis_state": str(meta_regulation_state.get("cautious_hypothesis_state", "") or ""),
            "temporal_binding_state": str(meta_regulation_state.get("temporal_binding_state", "") or ""),
            "temporal_continuity": float(meta_regulation_state.get("temporal_continuity", 0.0) or 0.0),
            "temporal_source_binding": float(meta_regulation_state.get("temporal_source_binding", 0.0) or 0.0),
            "temporal_recurrence": float(meta_regulation_state.get("temporal_recurrence", 0.0) or 0.0),
            "temporal_novelty": float(meta_regulation_state.get("temporal_novelty", 0.0) or 0.0),
            "temporal_afterimage": float(meta_regulation_state.get("temporal_afterimage", 0.0) or 0.0),
            "temporal_decay": float(meta_regulation_state.get("temporal_decay", 0.0) or 0.0),
            "temporal_context_depth": float(meta_regulation_state.get("temporal_context_depth", 0.0) or 0.0),
            "mcm_spacetime_depth": float(meta_regulation_state.get("mcm_spacetime_depth", 0.0) or 0.0),
            "memory_experience_depth": float(meta_regulation_state.get("memory_experience_depth", 0.0) or 0.0),
            "future_projection_depth": float(meta_regulation_state.get("future_projection_depth", 0.0) or 0.0),
            "temporal_self_location": float(meta_regulation_state.get("temporal_self_location", 0.0) or 0.0),
            "temporal_self_location_state": str(meta_regulation_state.get("temporal_self_location_state", "") or ""),
            "spacetime_unlocated_pressure": float(meta_regulation_state.get("spacetime_unlocated_pressure", 0.0) or 0.0),
            "spacetime_memory_bearing": float(meta_regulation_state.get("spacetime_memory_bearing", 0.0) or 0.0),
            "spacetime_future_bearing": float(meta_regulation_state.get("spacetime_future_bearing", 0.0) or 0.0),
            "spacetime_reflection_need": float(meta_regulation_state.get("spacetime_reflection_need", 0.0) or 0.0),
            "spacetime_regulation_support": float(meta_regulation_state.get("spacetime_regulation_support", 0.0) or 0.0),
            "spacetime_regulation_state": str(meta_regulation_state.get("spacetime_regulation_state", "") or ""),
            "temporal_self_consistency": float(meta_regulation_state.get("temporal_self_consistency", 0.0) or 0.0),
            "perception_sequence_coherence": float(meta_regulation_state.get("perception_sequence_coherence", 0.0) or 0.0),
            "memory_time_distance": float(meta_regulation_state.get("memory_time_distance", 1.0) or 1.0),
            "return_strength": float(meta_regulation_state.get("return_strength", 0.0) or 0.0),
            "integration_capacity": float(meta_regulation_state.get("integration_capacity", 0.0) or 0.0),
            "variance_regulation": float(meta_regulation_state.get("variance_regulation", 0.0) or 0.0),
            "load_tolerance": float(meta_regulation_state.get("load_tolerance", 0.0) or 0.0),
            "impulse_control": float(meta_regulation_state.get("impulse_control", 0.0) or 0.0),
            "frustration_tolerance": float(meta_regulation_state.get("frustration_tolerance", 0.0) or 0.0),
            "protective_distance_regulation": float(meta_regulation_state.get("protective_distance_regulation", 0.0) or 0.0),
            "self_reflection_regulator": float(meta_regulation_state.get("self_reflection_regulator", 0.0) or 0.0),
            "distance_regulation": float(meta_regulation_state.get("distance_regulation", 0.0) or 0.0),
            "experience_packet_label": str(experience_packet_feedback.get("experience_packet_label", normalized_decomposition.get("experience_packet_label", "")) or ""),
            "packet_bearing_quality": float(experience_packet_feedback.get("packet_bearing_quality", normalized_decomposition.get("packet_bearing_quality", 0.0)) or 0.0),
            "packet_inner_outer_fit": float(experience_packet_feedback.get("packet_inner_outer_fit", normalized_decomposition.get("packet_inner_outer_fit", 0.0)) or 0.0),
            "packet_confidence_integrity": float(experience_packet_feedback.get("packet_confidence_integrity", normalized_decomposition.get("packet_confidence_integrity", 0.0)) or 0.0),
            "packet_repetition_potential": float(experience_packet_feedback.get("packet_repetition_potential", normalized_decomposition.get("packet_repetition_potential", 0.0)) or 0.0),
            "packet_curiosity_pull": float(experience_packet_feedback.get("packet_curiosity_pull", normalized_decomposition.get("packet_curiosity_pull", 0.0)) or 0.0),
            "packet_process_reward": float(experience_packet_feedback.get("packet_process_reward", normalized_decomposition.get("packet_process_reward", 0.0)) or 0.0),
            "packet_reorganization_need": float(experience_packet_feedback.get("packet_reorganization_need", normalized_decomposition.get("packet_reorganization_need", 0.0)) or 0.0),
            "constructive_stimulation": float(experience_packet_feedback.get("constructive_stimulation", normalized_decomposition.get("constructive_stimulation", 0.0)) or 0.0),
            "constructive_dopamine": float(experience_packet_feedback.get("constructive_dopamine", normalized_decomposition.get("constructive_dopamine", 0.0)) or 0.0),
            "stabilizing_serotonin": float(experience_packet_feedback.get("stabilizing_serotonin", normalized_decomposition.get("stabilizing_serotonin", 0.0)) or 0.0),
            "relief_endorphin": float(experience_packet_feedback.get("relief_endorphin", normalized_decomposition.get("relief_endorphin", 0.0)) or 0.0),
            "focused_acetylcholine": float(experience_packet_feedback.get("focused_acetylcholine", normalized_decomposition.get("focused_acetylcholine", 0.0)) or 0.0),
            "exit_candidate_replay": self._normalize_record_value(exit_candidate_replay or {}),
            "outcome_decomposition": raw_outcome_decomposition,
            "outcome_decomposition_enriched": normalized_decomposition,
            "context": compact_context,
        }

        if self._should_write_outcome_record():
            self._append_record_file(self.outcome_path, outcome_record)
        else:
            self._remember_outcome_record(outcome_record)

        current_equity = float(self.data.get("current_equity", self.data.get("start_equity", 0.0)) or 0.0)
        equity_peak = max(
            float(self.data.get("equity_peak", self.data.get("start_equity", 0.0)) or self.data.get("start_equity", 0.0)),
            float(current_equity),
        )
        self.data["equity_peak"] = float(equity_peak)

        drawdown_abs = max(0.0, equity_peak - float(current_equity))
        drawdown_pct = (drawdown_abs / equity_peak) if equity_peak > 0.0 else 0.0

        self.data["max_drawdown_abs"] = float(max(float(self.data.get("max_drawdown_abs", 0.0) or 0.0), drawdown_abs))
        self.data["max_drawdown_pct"] = float(max(float(self.data.get("max_drawdown_pct", 0.0) or 0.0), drawdown_pct))

        self._rebuild_kpi_summary()
        self._save(force=True)

        try:
            os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

            header_key = f"_csv_header_written::{self.csv_path}"
            write_header = (not os.path.exists(self.csv_path)) and not bool(getattr(self, header_key, False))
            payload = ""
            if write_header:
                payload += "trade,current_equity,pnl_netto,pnl_tp,pnl_sl\n"
                setattr(self, header_key, True)
            payload += (
                f"{self.data['trades']},"
                f"{self.data.get('current_equity', self.data.get('start_equity', 0.0))},"
                f"{self.data['pnl_netto']},"
                f"{self.data['pnl_tp']},"
                f"{self.data['pnl_sl']}\n"
            )
            dbr_append_text(self.csv_path, payload, operation="trade_equity_csv_append")
        except Exception:
            pass

    # ─────────────────────────────────────────────
    # Snapshot mit zusätzlichen Kennzahlen
    # ─────────────────────────────────────────────
    def snapshot(self) -> dict:
        """
        Aktuellen Stand zurückgeben (read-only Kopie)
        """
        data = dict(self.data)

        trades = data.get("trades", 0)
        pnl_tp = data.get("pnl_tp", 0.0)
        pnl_sl = data.get("pnl_sl", 0.0)

        avg_win = (pnl_tp / data.get("tp", 1)) if data.get("tp", 0) > 0 else 0.0
        avg_loss = (pnl_sl / data.get("sl", 1)) if data.get("sl", 0) > 0 else 0.0

        profit_factor = (
            abs(pnl_tp / pnl_sl)
            if pnl_sl != 0
            else 0.0
        )

        expectancy = (
            (data.get("pnl_netto", 0.0) / trades)
            if trades > 0
            else 0.0
        )

        exploration_trades = int(data.get("exploration_trades", 0) or 0)
        exploration_tp = int(data.get("exploration_tp", 0) or 0)
        exploration_sl = int(data.get("exploration_sl", 0) or 0)
        exploration_pnl = float(data.get("exploration_pnl", 0.0) or 0.0)

        exploration_avg = (
            exploration_pnl / exploration_trades
            if exploration_trades > 0
            else 0.0
        )

        self._rebuild_kpi_summary()
        kpi_summary = dict(self.data.get("kpi_summary", {}) or {})
        proof = dict(kpi_summary.get("proof", {}) or {})

        data.pop("attempt_records", None)
        data.pop("outcome_records", None)

        data.update({
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "profit_factor": profit_factor,
            "expectancy": expectancy,
            "exploration_avg": exploration_avg,
            "normal_trades": max(0, trades - exploration_trades),
            "normal_tp": max(0, int(data.get("tp", 0) or 0) - exploration_tp),
            "normal_sl": max(0, int(data.get("sl", 0) or 0) - exploration_sl),
            "normal_cancels": max(0, int(data.get("cancels", 0) or 0) - int(data.get("exploration_cancels", 0) or 0)),
            "attempts_per_trade": (
                float(data.get("attempts", 0) or 0) / max(1, int(trades))
            ),
            "attempt_zone_share": (
                float(data.get("attempt_structure_zone", 0) or 0) / max(1, int(data.get("attempts", 0) or 0))
            ),
            "attempt_fill_rate": (
                float(data.get("attempts_filled", 0) or 0) / max(1, int(data.get("attempts", 0) or 0))
            ),
            "attempt_density": float(proof.get("attempt_density", 0.0) or 0.0),
            "context_quality": float(proof.get("context_quality", 0.0) or 0.0),
            "overtrade_pressure": float(proof.get("overtrade_pressure", 0.0) or 0.0),
            "observe_share": float(proof.get("observe_share", 0.0) or 0.0),
            "replan_share": float(proof.get("replan_share", 0.0) or 0.0),
            "withheld_share": float(proof.get("withheld_share", 0.0) or 0.0),
            "pressure_to_capacity": float(proof.get("pressure_to_capacity", 0.0) or 0.0),
            "recovery_need": float(proof.get("recovery_need", 0.0) or 0.0),
            "regulated_courage": float(proof.get("regulated_courage", 0.0) or 0.0),
            "courage_gap": float(proof.get("courage_gap", 0.0) or 0.0),
            "action_inhibition": float(proof.get("action_inhibition", 0.0) or 0.0),
            "action_clearance": float(proof.get("action_clearance", 0.0) or 0.0),
            "regulation_before_action": float(proof.get("regulation_before_action", 0.0) or 0.0),
            "max_drawdown_abs": float(proof.get("max_drawdown_abs", 0.0) or 0.0),
            "max_drawdown_pct": float(proof.get("max_drawdown_pct", 0.0) or 0.0),
            "kpi_summary": kpi_summary,
        })

        return data
    
    # ───────────────────────────────────────────── 
    def on_cancel(self, *, order_id=None, cause: str = None, exploration_trade: bool = False, outcome_decomposition: dict = None, context: dict = None):
        """
        Order wurde gecancelt bevor ein Trade/Exit stattgefunden hat.
        Keine PnL-Änderung – nur Zählung.
        """
        try:
            normalized_context = self._normalize_record_value(context or {})
            normalized_decomposition = self._normalize_record_value(outcome_decomposition or {})
            raw_outcome_decomposition = dict(normalized_decomposition or {})
            structure_quality = self._extract_structure_quality(normalized_context)
            structure_bucket = "zone" if structure_quality >= 0.55 else "non_zone"

            self.data["cancels"] = int(self.data.get("cancels", 0) or 0) + 1
            self.data["last_outcome_decomposition"] = dict(raw_outcome_decomposition or {})
            if exploration_trade:
                self.data["exploration_cancels"] = int(self.data.get("exploration_cancels", 0) or 0) + 1

            compact_context = self._compact_context(normalized_context)
            trade_plan_state = dict(compact_context.get("trade_plan", {}) or {})
            meta_regulation_state = dict(compact_context.get("meta_regulation_state", {}) or {})
            active_mcm_contact_state = dict(compact_context.get("active_mcm_contact_state", meta_regulation_state.get("active_mcm_contact", {}) or {}) or {})
            target_expectation_state = dict(compact_context.get("target_expectation_state", {}) or {})
            thought_seed_state = dict(compact_context.get("thought_seed_state", {}) or {})

            def _f(*values, default=0.0):
                for value in values:
                    try:
                        if value is None:
                            continue
                        return float(value)
                    except Exception:
                        continue
                return float(default)

            def _clip(value):
                value = _f(value)
                if value != value:
                    value = 0.0
                return max(0.0, min(1.0, float(value)))

            def _entry_contact_learning_source() -> dict:
                source = dict(trade_plan_state or {})
                fallback_keys = (
                    "area_bearing_quality",
                    "area_contact_timing_fit",
                    "area_action_timing_fit",
                    "area_spacetime_fit",
                    "area_present_contact",
                    "area_invalidity_pressure",
                    "area_afterimage",
                    "area_contact_distance_fit",
                    "contact_entry_fit",
                    "strategic_entry_fit",
                    "entry_contact_bearing",
                    "area_contact_readiness",
                    "receptive_contact_maturity",
                    "receptive_contact_immaturity_pressure",
                    "real_area_contact_bearing",
                    "felt_reality_bearing",
                    "form_mcm_reality_fit",
                    "energy_coherence_bearing",
                )
                for fallback in (meta_regulation_state, active_mcm_contact_state, compact_context):
                    if not isinstance(fallback, dict):
                        continue
                    for key in fallback_keys:
                        if key in source and source.get(key) not in (None, "", 0, 0.0):
                            continue
                        if key in fallback:
                            source[key] = fallback.get(key)
                return source

            rr_value = _f(trade_plan_state.get("rr_value"), default=0.0)
            structural_run_room = _clip((rr_value - 1.6) / 3.2)
            target_expectation_value = _clip(
                target_expectation_state.get(
                    "tp_reachability",
                    target_expectation_state.get("base_target_expectation", 0.0),
                )
            )
            emergent_structure_reading = _clip(
                (structural_run_room * 0.24)
                + (_clip(meta_regulation_state.get("future_projection_depth", 0.0)) * 0.16)
                + (_clip(meta_regulation_state.get("mcm_spacetime_depth", 0.0)) * 0.14)
                + (_clip(meta_regulation_state.get("area_bearing_quality", 0.0)) * 0.14)
                + (_clip(trade_plan_state.get("entry_contact_bearing", trade_plan_state.get("entry_choice_bearing", 0.0))) * 0.12)
                + (_clip(active_mcm_contact_state.get("contact_action_maturity", meta_regulation_state.get("contact_action_maturity", 0.0))) * 0.10)
                + (target_expectation_value * 0.10)
                - (_clip(meta_regulation_state.get("spacetime_unlocated_pressure", 0.0)) * 0.10)
                - (_clip(meta_regulation_state.get("contact_regime_mismatch", 0.0)) * 0.08)
            )
            emergent_structure_confirmation = _clip(
                (emergent_structure_reading * 0.42)
                + (_clip(normalized_decomposition.get("plan_quality", 0.0)) * 0.16)
                + (_clip(normalized_decomposition.get("execution_quality", 0.0)) * 0.14)
                + (_clip(normalized_decomposition.get("risk_fit_quality", 0.0)) * 0.12)
                + (_clip(normalized_decomposition.get("position_constructive_bearing", 0.0)) * 0.10)
            )
            if emergent_structure_reading >= 0.52 and emergent_structure_confirmation >= 0.50:
                emergent_structure_state = "confirmed_structure_contact"
            elif emergent_structure_reading >= 0.44 and rr_value >= 2.4:
                emergent_structure_state = "open_structure_contact"
            elif rr_value >= 2.4 and emergent_structure_reading < 0.34:
                emergent_structure_state = "wide_range_without_structure"
            else:
                emergent_structure_state = "ordinary_structure_contact"
            open_hypothesis_learning = self._derive_open_hypothesis_learning(
                {
                    "reason": "cancel",
                    "pnl": 0.0,
                    "rr_value": float(rr_value),
                    "emergent_structure_reading": float(emergent_structure_reading),
                    "emergent_structure_confirmation": float(emergent_structure_confirmation),
                    "emergent_structure_state": str(emergent_structure_state),
                    "thought_seed_structural_grounding": float(thought_seed_state.get("thought_structural_grounding", 0.0) or 0.0),
                    "thought_seed_open_hypothesis_pressure": float(thought_seed_state.get("thought_open_hypothesis_pressure", 0.0) or 0.0),
                    "thought_seed_reality_lag": float(thought_seed_state.get("thought_reality_lag", 0.0) or 0.0),
                    "thought_seed_consequence_balance": float(thought_seed_state.get("thought_consequence_balance", 0.0) or 0.0),
                },
                emergent_state=str(emergent_structure_state),
            )
            normalized_decomposition.update({
                "emergent_structure_reading": float(emergent_structure_reading),
                "emergent_structure_confirmation": float(emergent_structure_confirmation),
                "emergent_structure_state": str(emergent_structure_state),
                "open_hypothesis_learning_state": str(open_hypothesis_learning.get("open_hypothesis_learning_state", "-") or "-"),
                "open_hypothesis_consequence_score": float(open_hypothesis_learning.get("open_hypothesis_consequence_score", 0.0) or 0.0),
                "open_hypothesis_burden_score": float(open_hypothesis_learning.get("open_hypothesis_burden_score", 0.0) or 0.0),
                "open_hypothesis_reorganization_score": float(open_hypothesis_learning.get("open_hypothesis_reorganization_score", 0.0) or 0.0),
                "open_hypothesis_replay_need": float(open_hypothesis_learning.get("open_hypothesis_replay_need", 0.0) or 0.0),
                "open_hypothesis_distance_need": float(open_hypothesis_learning.get("open_hypothesis_distance_need", 0.0) or 0.0),
                "open_hypothesis_reinterpretation_need": float(open_hypothesis_learning.get("open_hypothesis_reinterpretation_need", 0.0) or 0.0),
                "open_hypothesis_reorganization_posture": str(open_hypothesis_learning.get("open_hypothesis_reorganization_posture", "-") or "-"),
            })
            entry_contact_preference_feedback = self._update_entry_contact_learning(
                side=str(trade_plan_state.get("side", trade_plan_state.get("decision", "-")) or "-"),
                reason="cancel",
                pnl=0.0,
                trade_plan_state=_entry_contact_learning_source(),
                outcome_decomposition=normalized_decomposition,
            )
            if entry_contact_preference_feedback:
                normalized_decomposition.update(
                    {
                        "entry_contact_preference_key": str(entry_contact_preference_feedback.get("key", "-") or "-"),
                        "entry_contact_preference_state": str(entry_contact_preference_feedback.get("last_state", "-") or "-"),
                        "entry_contact_preference_trust": float(entry_contact_preference_feedback.get("trust", 0.0) or 0.0),
                        "entry_contact_preference_caution": float(entry_contact_preference_feedback.get("caution", 0.0) or 0.0),
                        "entry_contact_preference_maturity": float(entry_contact_preference_feedback.get("maturity", 0.0) or 0.0),
                        "entry_contact_preference_utility": float(entry_contact_preference_feedback.get("utility", 0.0) or 0.0),
                        "entry_property_profile_id": str(entry_contact_preference_feedback.get("property_profile_id", "-") or "-"),
                        "entry_property_profile_state": str(entry_contact_preference_feedback.get("property_profile_state", "-") or "-"),
                        "entry_property_profile_similarity": float(entry_contact_preference_feedback.get("property_profile_similarity", 0.0) or 0.0),
                        "entry_property_profile_trust": float(entry_contact_preference_feedback.get("property_profile_trust", 0.0) or 0.0),
                        "entry_property_profile_caution": float(entry_contact_preference_feedback.get("property_profile_caution", 0.0) or 0.0),
                        "entry_property_profile_maturity": float(entry_contact_preference_feedback.get("property_profile_maturity", 0.0) or 0.0),
                        "entry_property_profile_utility": float(entry_contact_preference_feedback.get("property_profile_utility", 0.0) or 0.0),
                    }
                )
            self.data["last_outcome_decomposition"] = dict(raw_outcome_decomposition or {})
            self.data["last_outcome_decomposition_enriched"] = dict(normalized_decomposition or {})

            outcome_record = {
                    "event": "cancel",
                    "reason": "cancel",
                    "timestamp": self.data.get("current_timestamp"),
                    "order_id": None if order_id is None else str(order_id),
                    "cause": None if cause is None else str(cause),
                    "rr_value": float(rr_value),
                    "structural_run_room": float(structural_run_room),
                    "emergent_structure_reading": float(emergent_structure_reading),
                    "emergent_structure_confirmation": float(emergent_structure_confirmation),
                    "emergent_structure_state": str(emergent_structure_state),
                    "open_hypothesis_learning_state": str(open_hypothesis_learning.get("open_hypothesis_learning_state", "-") or "-"),
                    "open_hypothesis_consequence_score": float(open_hypothesis_learning.get("open_hypothesis_consequence_score", 0.0) or 0.0),
                    "open_hypothesis_burden_score": float(open_hypothesis_learning.get("open_hypothesis_burden_score", 0.0) or 0.0),
                    "open_hypothesis_reorganization_score": float(open_hypothesis_learning.get("open_hypothesis_reorganization_score", 0.0) or 0.0),
                    "open_hypothesis_replay_need": float(open_hypothesis_learning.get("open_hypothesis_replay_need", 0.0) or 0.0),
                    "open_hypothesis_distance_need": float(open_hypothesis_learning.get("open_hypothesis_distance_need", 0.0) or 0.0),
                    "open_hypothesis_reinterpretation_need": float(open_hypothesis_learning.get("open_hypothesis_reinterpretation_need", 0.0) or 0.0),
                    "open_hypothesis_reorganization_posture": str(open_hypothesis_learning.get("open_hypothesis_reorganization_posture", "-") or "-"),
                    "entry_contact_preference_key": str(entry_contact_preference_feedback.get("key", "-") or "-"),
                    "entry_contact_preference_state": str(entry_contact_preference_feedback.get("last_state", "-") or "-"),
                    "entry_contact_preference_trust": float(entry_contact_preference_feedback.get("trust", 0.0) or 0.0),
                    "entry_contact_preference_caution": float(entry_contact_preference_feedback.get("caution", 0.0) or 0.0),
                    "entry_contact_preference_maturity": float(entry_contact_preference_feedback.get("maturity", 0.0) or 0.0),
                    "entry_contact_preference_utility": float(entry_contact_preference_feedback.get("utility", 0.0) or 0.0),
                    "entry_property_profile_id": str(entry_contact_preference_feedback.get("property_profile_id", "-") or "-"),
                    "entry_property_profile_state": str(entry_contact_preference_feedback.get("property_profile_state", "-") or "-"),
                    "entry_property_profile_similarity": float(entry_contact_preference_feedback.get("property_profile_similarity", 0.0) or 0.0),
                    "entry_property_profile_trust": float(entry_contact_preference_feedback.get("property_profile_trust", 0.0) or 0.0),
                    "entry_property_profile_caution": float(entry_contact_preference_feedback.get("property_profile_caution", 0.0) or 0.0),
                    "entry_property_profile_maturity": float(entry_contact_preference_feedback.get("property_profile_maturity", 0.0) or 0.0),
                    "entry_property_profile_utility": float(entry_contact_preference_feedback.get("property_profile_utility", 0.0) or 0.0),
                    "thought_seed_id": str(thought_seed_state.get("thought_seed_id", "") or ""),
                    "thought_seed_label": str(thought_seed_state.get("thought_seed_label", "") or ""),
                    "thought_seed_metaregulator_state": str(thought_seed_state.get("seed_metaregulator_state", "") or ""),
                    "thought_seed_emergent_state": str(thought_seed_state.get("emergent_structure_state", "") or ""),
                    "thought_seed_trace_strength": float(thought_seed_state.get("thought_trace_strength", 0.0) or 0.0),
                    "thought_seed_maturity": float(thought_seed_state.get("thought_maturity", 0.0) or 0.0),
                    "thought_seed_reality_binding": float(thought_seed_state.get("reality_binding_score", 0.0) or 0.0),
                    "thought_seed_confirmation": float(thought_seed_state.get("thought_confirmation_score", 0.0) or 0.0),
                    "thought_seed_consequence_echo": float(thought_seed_state.get("consequence_echo", 0.0) or 0.0),
                    "thought_seed_reorganization_echo": float(thought_seed_state.get("reorganization_echo", 0.0) or 0.0),
                    "thought_seed_consequence_alignment": float(thought_seed_state.get("thought_consequence_alignment", 0.0) or 0.0),
                    "thought_seed_consequence_balance": float(thought_seed_state.get("thought_consequence_balance", 0.0) or 0.0),
                    "thought_seed_reality_lag": float(thought_seed_state.get("thought_reality_lag", 0.0) or 0.0),
                    "thought_seed_structural_grounding": float(thought_seed_state.get("thought_structural_grounding", 0.0) or 0.0),
                    "thought_seed_open_hypothesis_pressure": float(thought_seed_state.get("thought_open_hypothesis_pressure", 0.0) or 0.0),
                    "thought_seed_replay_maturation_pull": float(thought_seed_state.get("thought_replay_maturation_pull", 0.0) or 0.0),
                    "thought_seed_distance_maturation_pull": float(thought_seed_state.get("thought_distance_maturation_pull", 0.0) or 0.0),
                    "thought_seed_reinterpretation_pull": float(thought_seed_state.get("thought_reinterpretation_pull", 0.0) or 0.0),
                    "thought_seed_digestive_replay_pull": float(thought_seed_state.get("thought_digestive_replay_pull", 0.0) or 0.0),
                    "thought_seed_digestive_distance_pull": float(thought_seed_state.get("thought_digestive_distance_pull", 0.0) or 0.0),
                    "thought_seed_digestive_integration_pull": float(thought_seed_state.get("thought_digestive_integration_pull", 0.0) or 0.0),
                    "thought_seed_digestive_returned_trust": float(thought_seed_state.get("thought_digestive_returned_trust", 0.0) or 0.0),
                    "thought_seed_trust_return_readiness": float(thought_seed_state.get("trust_return_readiness", 0.0) or 0.0),
                    "thought_seed_digest_state": str(thought_seed_state.get("thought_digest_state", "") or ""),
                    "thought_seed_reifung_direction": str(thought_seed_state.get("thought_reifung_direction", "") or ""),
                    "thought_seed_semantic_origin_state": str(thought_seed_state.get("semantic_origin_state", "") or ""),
                    "thought_seed_borrowed_open_hypothesis_pressure": float(thought_seed_state.get("borrowed_open_hypothesis_pressure", 0.0) or 0.0),
                    "thought_seed_own_field_binding_pull": float(thought_seed_state.get("own_field_binding_pull", 0.0) or 0.0),
                    "semantic_origin_state": str(meta_regulation_state.get("semantic_origin_state", "") or ""),
                    "own_field_identity_strength": float(meta_regulation_state.get("own_field_identity_strength", 0.0) or 0.0),
                    "foreign_semantic_pressure": float(meta_regulation_state.get("foreign_semantic_pressure", 0.0) or 0.0),
                    "adopted_language_pressure": float(meta_regulation_state.get("adopted_language_pressure", 0.0) or 0.0),
                    "self_foreign_boundary_clarity": float(meta_regulation_state.get("self_foreign_boundary_clarity", 0.0) or 0.0),
                    "semantic_origin_conflict": float(meta_regulation_state.get("semantic_origin_conflict", 0.0) or 0.0),
                    "own_vs_foreign_margin": float(meta_regulation_state.get("own_vs_foreign_margin", 0.0) or 0.0),
                    "borrowed_vs_own_margin": float(meta_regulation_state.get("borrowed_vs_own_margin", 0.0) or 0.0),
                    "boundary_support_margin": float(meta_regulation_state.get("boundary_support_margin", 0.0) or 0.0),
                    "thought_seed_drift_risk": float(thought_seed_state.get("hallucination_drift_risk", 0.0) or 0.0),
                    "thought_seed_overthinking_risk": float(thought_seed_state.get("overthinking_risk", 0.0) or 0.0),
                    "target_expectation_value": float(target_expectation_value),
                    "structure_quality": float(structure_quality),
                    "structure_bucket": structure_bucket,
                    "outcome_decomposition": raw_outcome_decomposition,
                    "outcome_decomposition_enriched": normalized_decomposition,
                    "context": compact_context,
                }

            if self._should_write_outcome_record():
                self._append_record_file(self.outcome_path, outcome_record)
            else:
                self._remember_outcome_record(outcome_record)
            self._rebuild_kpi_summary()
            self._save(force=True)
        except Exception:
            pass
