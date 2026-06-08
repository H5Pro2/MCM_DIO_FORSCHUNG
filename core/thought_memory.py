"""Persistent thought-memory store for DIO.

This module owns the separate mcm_thought_memory.json layer: emergent thought
seeds, thought families, syntax traces, and flush/load behavior. Function names
keep the legacy underscore API while MCM_Brain_Modell.py is refactored in phases.
"""

import hashlib
import json
import os
import time

from config import Config
from debug_tools.writers import dbr_append_text, dbr_file_write_profile, dbr_path


def _write_text_atomic_with_retry(filepath, text, operation="atomic_write", extra=None, attempts=6, sleep_seconds=0.08):
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)

    payload = str(text or "")
    encoded_len = len(payload.encode("utf-8"))
    last_error = None
    write_start = time.perf_counter()

    for attempt in range(max(1, int(attempts or 1))):
        temp_path = f"{filepath}.{os.getpid()}.{int(time.time() * 1000)}.{attempt}.tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, filepath)
            elapsed_ms = (time.perf_counter() - write_start) * 1000.0
            dbr_file_write_profile(
                filepath,
                elapsed_ms,
                bytes_written=encoded_len,
                operation=operation,
                extra=extra,
            )
            return True
        except PermissionError as exc:
            last_error = exc
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception:
                pass
            time.sleep(max(0.0, float(sleep_seconds or 0.0)) * float(attempt + 1))
        except Exception as exc:
            last_error = exc
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception:
                pass
            break

    try:
        dbr_append_text(
            dbr_path("memory_write_errors.log"),
            (
                f"{time.time():.6f};{operation};{str(filepath).replace(';', '|')};"
                f"{type(last_error).__name__ if last_error else 'UnknownError'};"
                f"{str(last_error).replace(';', '|') if last_error else ''}\n"
            ),
            operation="memory_write_error",
        )
    except Exception:
        pass
    return False


def _thought_memory_path(path=None):

    if path is not None:
        return str(path)

    configured = getattr(Config, "MCM_THOUGHT_MEMORY_PATH", "bot_memory/mcm_thought_memory.json")
    return str(configured or "bot_memory/mcm_thought_memory.json")

def _empty_thought_memory_payload():

    return {
        "version": 1,
        "summary": {
            "seed_count": 0,
            "family_count": 0,
            "form_mcm_family_count": 0,
            "total_seen": 0,
            "family_total_seen": 0,
            "last_saved_ts": None,
        },
        "seeds": {},
        "families": {},
        "form_mcm_families": {},
    }

def _thought_memory_family_key(seed_state):

    state = dict(seed_state or {})

    def _clean(value):
        text = str(value or "-").strip()
        text = text.replace("\n", " ").replace(";", "|")
        return text or "-"

    basis = "|".join(
        [
            _clean(state.get("emergent_structure_state", "-")),
            _clean(state.get("seed_metaregulator_state", "-")),
            _clean(state.get("thought_reifung_direction", "-")),
            _clean(state.get("semantic_origin_state", "-")),
            _clean(state.get("form_symbol_anchor", "-")),
            _clean(state.get("mcm_field_anchor", "-")),
            _clean(state.get("experience_memory_anchor", "-")),
        ]
    )
    family_id = "tf_" + hashlib.sha1(basis.encode("utf-8", errors="ignore")).hexdigest()[:10]
    return str(family_id), str(basis)

def _thought_memory_sentence_state(seed_state, development_state):

    state = dict(seed_state or {})
    emergent = str(state.get("emergent_structure_state", "-") or "-")
    semantic = str(state.get("semantic_origin_state", "-") or "-")
    reifung = str(state.get("thought_reifung_direction", "-") or "-")
    digest = str(state.get("thought_digest_state", "-") or "-")
    metaregulator = str(state.get("seed_metaregulator_state", "-") or "-")
    phase = str(state.get("phase", "-") or "-")
    decision = str(state.get("decision", "-") or "-")

    return "|".join(
        [
            f"form={state.get('form_symbol_anchor', '-')}",
            f"field={state.get('mcm_field_anchor', '-')}",
            f"structure={emergent}",
            f"origin={semantic}",
            f"reifung={reifung}",
            f"digest={digest}",
            f"seed={metaregulator}",
            f"dev={development_state}",
            f"phase={phase}",
            f"decision={decision}",
        ]
    )

def _normalize_thought_memory_families(families):

    if not isinstance(families, dict):
        return {}

    max_families = max(16, int(getattr(Config, "MCM_THOUGHT_MEMORY_MAX_FAMILIES", 768) or 768))

    def _num(item, key, default=0.0):
        try:
            value = float((item or {}).get(key, default) or default)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return value

    candidates = []
    for family_id, raw_item in dict(families or {}).items():
        if not isinstance(raw_item, dict):
            continue
        family_key = str(family_id or raw_item.get("thought_family_id", "") or "").strip()
        if not family_key:
            continue
        item = dict(raw_item or {})
        seen = max(0, int(_num(item, "seen", 0)))
        cleaned = {
            "thought_family_id": family_key,
            "family_key": str(item.get("family_key", "") or ""),
            "family_syntax": str(item.get("family_syntax", "") or ""),
            "last_dio_language_sentence": str(item.get("last_dio_language_sentence", "") or ""),
            "last_dio_dialogue_bridge_sentence": str(item.get("last_dio_dialogue_bridge_sentence", "") or ""),
            "last_dio_language_state": str(item.get("last_dio_language_state", "") or ""),
            "last_dio_syntax_origin": str(item.get("last_dio_syntax_origin", "") or ""),
            "last_dio_syntax_signature": str(item.get("last_dio_syntax_signature", "") or ""),
            "last_dio_form_mcm_token": str(item.get("last_dio_form_mcm_token", "") or ""),
            "last_dio_form_mcm_family_token": str(item.get("last_dio_form_mcm_family_token", "") or ""),
            "last_dio_form_mcm_sentence": str(item.get("last_dio_form_mcm_sentence", "") or ""),
            "last_dio_form_mcm_syntax_state": str(item.get("last_dio_form_mcm_syntax_state", "") or ""),
            "seen": int(seen),
            "unique_seed_count": max(0, int(_num(item, "unique_seed_count", 0))),
            "first_seen_ts": item.get("first_seen_ts", None),
            "last_seen_ts": item.get("last_seen_ts", None),
            "last_runtime_tick": max(0, int(_num(item, "last_runtime_tick", 0))),
            "last_development_state": str(item.get("last_development_state", "thought_seed_observed") or "thought_seed_observed"),
            "last_semantic_origin_state": str(item.get("last_semantic_origin_state", "") or ""),
            "last_emergent_structure_state": str(item.get("last_emergent_structure_state", "") or ""),
            "last_reifung_direction": str(item.get("last_reifung_direction", "") or ""),
            "last_digest_state": str(item.get("last_digest_state", "") or ""),
            "last_seed_metaregulator_state": str(item.get("last_seed_metaregulator_state", "") or ""),
            "last_sentence_state": str(item.get("last_sentence_state", "") or ""),
            "seed_ids": [str(value) for value in list(item.get("seed_ids", []) or [])[:32]],
            "semantic_origin_counts": dict(item.get("semantic_origin_counts", {}) or {}),
            "emergent_structure_counts": dict(item.get("emergent_structure_counts", {}) or {}),
            "reifung_direction_counts": dict(item.get("reifung_direction_counts", {}) or {}),
            "digest_state_counts": dict(item.get("digest_state_counts", {}) or {}),
            "metaregulator_counts": dict(item.get("metaregulator_counts", {}) or {}),
            "development_state_counts": dict(item.get("development_state_counts", {}) or {}),
            "avg_trace_strength": max(0.0, min(1.0, _num(item, "avg_trace_strength", 0.0))),
            "avg_recall_potential": max(0.0, min(1.0, _num(item, "avg_recall_potential", 0.0))),
            "avg_maturity": max(0.0, min(1.0, _num(item, "avg_maturity", 0.0))),
            "avg_reality_binding": max(0.0, min(1.0, _num(item, "avg_reality_binding", 0.0))),
            "avg_confirmation": max(0.0, min(1.0, _num(item, "avg_confirmation", 0.0))),
            "avg_open_hypothesis_pressure": max(0.0, min(1.0, _num(item, "avg_open_hypothesis_pressure", 0.0))),
            "avg_borrowed_open_hypothesis_pressure": max(0.0, min(1.0, _num(item, "avg_borrowed_open_hypothesis_pressure", 0.0))),
            "avg_own_field_binding_pull": max(0.0, min(1.0, _num(item, "avg_own_field_binding_pull", 0.0))),
            "avg_consequence_balance": max(-1.0, min(1.0, _num(item, "avg_consequence_balance", 0.0))),
            "avg_reality_lag": max(0.0, min(1.0, _num(item, "avg_reality_lag", 0.0))),
            "avg_structural_grounding": max(0.0, min(1.0, _num(item, "avg_structural_grounding", 0.0))),
            "avg_drift_risk": max(0.0, min(1.0, _num(item, "avg_drift_risk", 0.0))),
            "avg_overthinking_risk": max(0.0, min(1.0, _num(item, "avg_overthinking_risk", 0.0))),
            "avg_digestive_replay_pull": max(0.0, min(1.0, _num(item, "avg_digestive_replay_pull", 0.0))),
            "avg_digestive_distance_pull": max(0.0, min(1.0, _num(item, "avg_digestive_distance_pull", 0.0))),
            "avg_digestive_integration_pull": max(0.0, min(1.0, _num(item, "avg_digestive_integration_pull", 0.0))),
            "avg_digestive_returned_trust": max(0.0, min(1.0, _num(item, "avg_digestive_returned_trust", 0.0))),
            "avg_trust_return_readiness": max(0.0, min(1.0, _num(item, "avg_trust_return_readiness", 0.0))),
            "avg_dio_syntax_density": max(0.0, min(1.0, _num(item, "avg_dio_syntax_density", 0.0))),
            "avg_dio_syntax_compression": max(0.0, min(1.0, _num(item, "avg_dio_syntax_compression", 0.0))),
            "avg_dio_syntax_coherence": max(0.0, min(1.0, _num(item, "avg_dio_syntax_coherence", 0.0))),
            "avg_form_to_mcm_recall": max(0.0, min(1.0, _num(item, "avg_form_to_mcm_recall", 0.0))),
            "avg_mcm_to_form_confirmation": max(0.0, min(1.0, _num(item, "avg_mcm_to_form_confirmation", 0.0))),
            "avg_visual_mcm_context_fit": max(0.0, min(1.0, _num(item, "avg_visual_mcm_context_fit", 0.0))),
            "avg_visual_mcm_mismatch": max(0.0, min(1.0, _num(item, "avg_visual_mcm_mismatch", 0.0))),
            "avg_hypothesis_reality_binding": max(0.0, min(1.0, _num(item, "avg_hypothesis_reality_binding", 0.0))),
            "avg_form_mcm_syntax_density": max(0.0, min(1.0, _num(item, "avg_form_mcm_syntax_density", 0.0))),
        }
        score = (float(seen) * 1.0) + (float(cleaned.get("avg_maturity", 0.0) or 0.0) * 32.0) + (float(cleaned.get("unique_seed_count", 0) or 0) * 0.4)
        candidates.append((score, cleaned.get("last_runtime_tick", 0), family_key, cleaned))

    normalized = {}
    for _, _, family_key, cleaned in sorted(candidates, reverse=True)[:max_families]:
        normalized[str(family_key)] = dict(cleaned or {})

    return normalized

def _normalize_form_mcm_families(families):

    if not isinstance(families, dict):
        return {}

    max_families = max(16, int(getattr(Config, "MCM_FORM_MCM_MEMORY_MAX_FAMILIES", 768) or 768))

    def _num(item, key, default=0.0):
        try:
            value = float((item or {}).get(key, default) or default)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return value

    candidates = []
    for family_id, raw_item in dict(families or {}).items():
        if not isinstance(raw_item, dict):
            continue
        family_key = str(family_id or raw_item.get("dio_form_mcm_family_token", "") or "").strip()
        if not family_key:
            continue
        item = dict(raw_item or {})
        seen = max(0, int(_num(item, "seen", 0)))
        cleaned = {
            "dio_form_mcm_family_token": family_key,
            "last_dio_form_mcm_token": str(item.get("last_dio_form_mcm_token", "") or ""),
            "last_dio_form_mcm_syntax_state": str(item.get("last_dio_form_mcm_syntax_state", "") or ""),
            "last_dio_form_mcm_sentence": str(item.get("last_dio_form_mcm_sentence", "") or ""),
            "seen": int(seen),
            "first_seen_ts": item.get("first_seen_ts", None),
            "last_seen_ts": item.get("last_seen_ts", None),
            "last_runtime_tick": max(0, int(_num(item, "last_runtime_tick", 0))),
            "syntax_state_counts": dict(item.get("syntax_state_counts", {}) or {}),
            "phase_counts": dict(item.get("phase_counts", {}) or {}),
            "decision_counts": dict(item.get("decision_counts", {}) or {}),
            "emergent_structure_counts": dict(item.get("emergent_structure_counts", {}) or {}),
            "avg_form_to_mcm_recall": max(0.0, min(1.0, _num(item, "avg_form_to_mcm_recall", 0.0))),
            "avg_mcm_to_form_confirmation": max(0.0, min(1.0, _num(item, "avg_mcm_to_form_confirmation", 0.0))),
            "avg_visual_mcm_context_fit": max(0.0, min(1.0, _num(item, "avg_visual_mcm_context_fit", 0.0))),
            "avg_visual_mcm_mismatch": max(0.0, min(1.0, _num(item, "avg_visual_mcm_mismatch", 0.0))),
            "avg_hypothesis_reality_binding": max(0.0, min(1.0, _num(item, "avg_hypothesis_reality_binding", 0.0))),
            "avg_form_mcm_syntax_density": max(0.0, min(1.0, _num(item, "avg_form_mcm_syntax_density", 0.0))),
            "avg_thought_confirmation": max(0.0, min(1.0, _num(item, "avg_thought_confirmation", 0.0))),
            "avg_open_hypothesis_pressure": max(0.0, min(1.0, _num(item, "avg_open_hypothesis_pressure", 0.0))),
            "avg_consequence_balance": max(-1.0, min(1.0, _num(item, "avg_consequence_balance", 0.0))),
            "family_recurrence": max(0.0, min(1.0, _num(item, "family_recurrence", 0.0))),
            "family_maturity": max(0.0, min(1.0, _num(item, "family_maturity", 0.0))),
            "family_trust": max(0.0, min(1.0, _num(item, "family_trust", 0.0))),
            "family_caution": max(0.0, min(1.0, _num(item, "family_caution", 0.0))),
            "family_reorganization_need": max(0.0, min(1.0, _num(item, "family_reorganization_need", 0.0))),
        }
        score = (float(seen) * 1.0) + (float(cleaned.get("family_maturity", 0.0) or 0.0) * 32.0)
        candidates.append((score, cleaned.get("last_runtime_tick", 0), family_key, cleaned))

    normalized = {}
    for _, _, family_key, cleaned in sorted(candidates, reverse=True)[:max_families]:
        normalized[str(family_key)] = dict(cleaned or {})

    return normalized

def _normalize_thought_memory(memory):

    if not isinstance(memory, dict):
        return _empty_thought_memory_payload()

    raw_seeds = dict(memory.get("seeds", {}) or {})
    raw_families = dict(memory.get("families", {}) or {})
    raw_form_mcm_families = dict(memory.get("form_mcm_families", {}) or {})
    max_seeds = max(32, int(getattr(Config, "MCM_THOUGHT_MEMORY_MAX_SEEDS", 2048) or 2048))
    normalized = {}

    def _num(item, key, default=0.0):
        try:
            value = float((item or {}).get(key, default) or default)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return value

    candidates = []
    for seed_id, raw_item in raw_seeds.items():
        if not isinstance(raw_item, dict):
            continue
        seed_key = str(seed_id or raw_item.get("thought_seed_id", "") or "").strip()
        if not seed_key:
            continue
        item = dict(raw_item or {})
        seen = max(0, int(_num(item, "seen", 0)))
        cleaned = {
            "thought_seed_id": seed_key,
            "thought_family_id": str(item.get("thought_family_id", "") or ""),
            "family_key": str(item.get("family_key", "") or ""),
            "sentence_state": str(item.get("sentence_state", "") or ""),
            "dio_language_sentence": str(item.get("dio_language_sentence", "") or ""),
            "dio_dialogue_bridge_sentence": str(item.get("dio_dialogue_bridge_sentence", "") or ""),
            "dio_language_state": str(item.get("dio_language_state", "") or ""),
            "dio_syntax_origin": str(item.get("dio_syntax_origin", "") or ""),
            "dio_syntax_signature": str(item.get("dio_syntax_signature", "") or ""),
            "dio_form_mcm_token": str(item.get("dio_form_mcm_token", "") or ""),
            "dio_form_mcm_family_token": str(item.get("dio_form_mcm_family_token", "") or ""),
            "dio_form_mcm_sentence": str(item.get("dio_form_mcm_sentence", "") or ""),
            "dio_form_mcm_syntax_state": str(item.get("dio_form_mcm_syntax_state", "") or ""),
            "thought_seed_label": str(item.get("thought_seed_label", "") or ""),
            "seen": int(seen),
            "first_seen_ts": item.get("first_seen_ts", None),
            "last_seen_ts": item.get("last_seen_ts", None),
            "last_runtime_tick": max(0, int(_num(item, "last_runtime_tick", 0))),
            "last_development_state": str(item.get("last_development_state", "thought_seed_observed") or "thought_seed_observed"),
            "last_semantic_origin_state": str(item.get("last_semantic_origin_state", "") or ""),
            "last_emergent_structure_state": str(item.get("last_emergent_structure_state", "") or ""),
            "last_reifung_direction": str(item.get("last_reifung_direction", "") or ""),
            "last_digest_state": str(item.get("last_digest_state", "") or ""),
            "last_seed_metaregulator_state": str(item.get("last_seed_metaregulator_state", "") or ""),
            "semantic_origin_counts": dict(item.get("semantic_origin_counts", {}) or {}),
            "emergent_structure_counts": dict(item.get("emergent_structure_counts", {}) or {}),
            "reifung_direction_counts": dict(item.get("reifung_direction_counts", {}) or {}),
            "digest_state_counts": dict(item.get("digest_state_counts", {}) or {}),
            "metaregulator_counts": dict(item.get("metaregulator_counts", {}) or {}),
            "development_state_counts": dict(item.get("development_state_counts", {}) or {}),
            "avg_trace_strength": max(0.0, min(1.0, _num(item, "avg_trace_strength", 0.0))),
            "avg_recall_potential": max(0.0, min(1.0, _num(item, "avg_recall_potential", 0.0))),
            "avg_maturity": max(0.0, min(1.0, _num(item, "avg_maturity", 0.0))),
            "avg_reality_binding": max(0.0, min(1.0, _num(item, "avg_reality_binding", 0.0))),
            "avg_confirmation": max(0.0, min(1.0, _num(item, "avg_confirmation", 0.0))),
            "avg_open_hypothesis_pressure": max(0.0, min(1.0, _num(item, "avg_open_hypothesis_pressure", 0.0))),
            "avg_borrowed_open_hypothesis_pressure": max(0.0, min(1.0, _num(item, "avg_borrowed_open_hypothesis_pressure", 0.0))),
            "avg_own_field_binding_pull": max(0.0, min(1.0, _num(item, "avg_own_field_binding_pull", 0.0))),
            "avg_consequence_balance": max(-1.0, min(1.0, _num(item, "avg_consequence_balance", 0.0))),
            "avg_reality_lag": max(0.0, min(1.0, _num(item, "avg_reality_lag", 0.0))),
            "avg_structural_grounding": max(0.0, min(1.0, _num(item, "avg_structural_grounding", 0.0))),
            "avg_drift_risk": max(0.0, min(1.0, _num(item, "avg_drift_risk", 0.0))),
            "avg_overthinking_risk": max(0.0, min(1.0, _num(item, "avg_overthinking_risk", 0.0))),
            "avg_digestive_replay_pull": max(0.0, min(1.0, _num(item, "avg_digestive_replay_pull", 0.0))),
            "avg_digestive_distance_pull": max(0.0, min(1.0, _num(item, "avg_digestive_distance_pull", 0.0))),
            "avg_digestive_integration_pull": max(0.0, min(1.0, _num(item, "avg_digestive_integration_pull", 0.0))),
            "avg_digestive_returned_trust": max(0.0, min(1.0, _num(item, "avg_digestive_returned_trust", 0.0))),
            "avg_trust_return_readiness": max(0.0, min(1.0, _num(item, "avg_trust_return_readiness", 0.0))),
            "avg_dio_syntax_density": max(0.0, min(1.0, _num(item, "avg_dio_syntax_density", 0.0))),
            "avg_dio_syntax_compression": max(0.0, min(1.0, _num(item, "avg_dio_syntax_compression", 0.0))),
            "avg_dio_syntax_coherence": max(0.0, min(1.0, _num(item, "avg_dio_syntax_coherence", 0.0))),
            "avg_form_to_mcm_recall": max(0.0, min(1.0, _num(item, "avg_form_to_mcm_recall", 0.0))),
            "avg_mcm_to_form_confirmation": max(0.0, min(1.0, _num(item, "avg_mcm_to_form_confirmation", 0.0))),
            "avg_visual_mcm_context_fit": max(0.0, min(1.0, _num(item, "avg_visual_mcm_context_fit", 0.0))),
            "avg_visual_mcm_mismatch": max(0.0, min(1.0, _num(item, "avg_visual_mcm_mismatch", 0.0))),
            "avg_hypothesis_reality_binding": max(0.0, min(1.0, _num(item, "avg_hypothesis_reality_binding", 0.0))),
            "avg_form_mcm_syntax_density": max(0.0, min(1.0, _num(item, "avg_form_mcm_syntax_density", 0.0))),
        }
        score = (float(seen) * 1.0) + (float(cleaned.get("avg_maturity", 0.0) or 0.0) * 24.0)
        candidates.append((score, cleaned.get("last_runtime_tick", 0), seed_key, cleaned))

    for _, _, seed_key, cleaned in sorted(candidates, reverse=True)[:max_seeds]:
        normalized[str(seed_key)] = dict(cleaned or {})

    families = _normalize_thought_memory_families(raw_families)
    form_mcm_families = _normalize_form_mcm_families(raw_form_mcm_families)
    total_seen = sum(int((item or {}).get("seen", 0) or 0) for item in normalized.values())
    family_total_seen = sum(int((item or {}).get("seen", 0) or 0) for item in families.values())
    form_mcm_family_total_seen = sum(int((item or {}).get("seen", 0) or 0) for item in form_mcm_families.values())
    payload = {
        "version": 1,
        "summary": {
            "seed_count": int(len(normalized or {})),
            "family_count": int(len(families or {})),
            "form_mcm_family_count": int(len(form_mcm_families or {})),
            "total_seen": int(total_seen),
            "family_total_seen": int(family_total_seen),
            "form_mcm_family_total_seen": int(form_mcm_family_total_seen),
            "last_saved_ts": (memory.get("summary", {}) or {}).get("last_saved_ts", None) if isinstance(memory.get("summary", {}), dict) else None,
        },
        "seeds": dict(normalized or {}),
        "families": dict(families or {}),
        "form_mcm_families": dict(form_mcm_families or {}),
    }
    return payload

def _read_thought_memory(path=None):

    if not bool(getattr(Config, "MCM_THOUGHT_MEMORY_ENABLED", True)):
        return _empty_thought_memory_payload()

    filepath = _thought_memory_path(path)
    if not os.path.exists(filepath):
        return _empty_thought_memory_payload()

    try:
        with open(filepath, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except Exception:
        return _empty_thought_memory_payload()

    payload = _normalize_thought_memory(raw or {})
    payload.setdefault("summary", {})["loaded_from"] = str(filepath)
    return payload

def _ensure_thought_memory_loaded(bot):

    if bot is None:
        return {}

    if bool(getattr(bot, "_thought_memory_loaded", False)):
        return dict(getattr(bot, "mcm_thought_memory", {}) or {})

    payload = _read_thought_memory()
    bot.mcm_thought_memory = dict(payload.get("seeds", {}) or {})
    bot.mcm_thought_family_memory = dict(payload.get("families", {}) or {})
    bot.mcm_form_mcm_family_memory = dict(payload.get("form_mcm_families", {}) or {})
    bot.mcm_thought_memory_summary = dict(payload.get("summary", {}) or {})
    bot._thought_memory_loaded = True
    bot._thought_memory_dirty = False
    bot._thought_memory_updates = 0
    bot._thought_memory_last_save_ts = float(time.time())
    return dict(bot.mcm_thought_memory or {})

def _thought_memory_development_state(seed_state):

    state = dict(seed_state or {})
    semantic_origin = str(state.get("semantic_origin_state", "") or "")
    reifung_direction = str(state.get("thought_reifung_direction", "") or "")
    digest_state = str(state.get("thought_digest_state", "") or "")
    metaregulator_state = str(state.get("seed_metaregulator_state", "") or "")

    borrowed_pressure = max(0.0, min(1.0, float(state.get("borrowed_open_hypothesis_pressure", 0.0) or 0.0)))
    open_pressure = max(0.0, min(1.0, float(state.get("thought_open_hypothesis_pressure", 0.0) or 0.0)))
    own_binding = max(0.0, min(1.0, float(state.get("own_field_binding_pull", 0.0) or 0.0)))
    maturity = max(0.0, min(1.0, float(state.get("thought_maturity", 0.0) or 0.0)))
    reality_binding = max(0.0, min(1.0, float(state.get("reality_binding_score", 0.0) or 0.0)))
    digestive_integration = max(0.0, min(1.0, float(state.get("thought_digestive_integration_pull", 0.0) or 0.0)))
    digestive_returned_trust = max(0.0, min(1.0, float(state.get("thought_digestive_returned_trust", 0.0) or 0.0)))

    development_pressures = {
        "digested_trust_return": (0.34 if digest_state == "digestive_trust_return" else 0.0) + (digestive_returned_trust * 0.46),
        "trust_return_emergence_memory_trace": (0.28 if digest_state == "digestive_trust_emergence" else 0.0) + (digestive_returned_trust * 0.34),
        "borrowed_reinterpretation_needed": (0.26 if semantic_origin == "borrowed_analogy_watch" else 0.0) + (borrowed_pressure * 0.30) + (open_pressure * 0.22),
        "reorganizing_digest_memory_trace": (0.24 if digest_state in ("digestive_replay", "digestive_integration") else 0.0) + (digestive_integration * 0.42),
        "reinterpretation_memory_trace": (0.34 if metaregulator_state == "seed_reinterpret" else 0.0) + (0.30 if reifung_direction == "reinterpretation_maturation" else 0.0),
        "replay_memory_trace": (0.34 if metaregulator_state == "seed_replay" else 0.0) + (0.30 if reifung_direction == "replay_maturation" else 0.0),
        "distance_memory_trace": 0.40 if reifung_direction == "distance_maturation" else 0.0,
        "own_field_binding_developing": (own_binding * 0.30) + (maturity * 0.24) + (reality_binding * 0.24),
        "mixed_translation_learning": 0.38 if semantic_origin == "mixed_translation_zone" else 0.0,
        "thought_seed_observed": 0.18 + ((1.0 - max(maturity, reality_binding, digestive_returned_trust)) * 0.16),
    }
    return max(development_pressures, key=development_pressures.get)

def _update_thought_memory(bot, seed_state, timestamp=None, runtime_tick=0):

    if bot is None or not bool(getattr(Config, "MCM_THOUGHT_MEMORY_ENABLED", True)):
        return {}

    profile_start = time.perf_counter() if bool(getattr(Config, "MCM_RUNTIME_PROFILE_DEBUG", False)) else 0.0
    profile_stage = "start"

    state = dict(seed_state or {})
    seed_id = str(state.get("thought_seed_id", "") or "").strip()
    if not seed_id or seed_id == "-":
        return {}

    _ensure_thought_memory_loaded(bot)
    memory = getattr(bot, "mcm_thought_memory", {}) or {}
    if not isinstance(memory, dict):
        memory = {}
        bot.mcm_thought_memory = memory
    item = dict(memory.get(seed_id, {}) or {})
    prior_seen = max(0, int(item.get("seen", 0) or 0))
    seen = prior_seen + 1

    def _clip(value, lo=0.0, hi=1.0):
        try:
            value = float(value)
        except Exception:
            value = 0.0
        if value != value:
            value = 0.0
        return max(float(lo), min(float(hi), float(value)))

    def _mean(key, value, lo=0.0, hi=1.0):
        current = _clip(item.get(key, 0.0), lo=lo, hi=hi)
        next_value = _clip(value, lo=lo, hi=hi)
        item[key] = float(current + ((next_value - current) / float(seen)))

    def _count(bucket_key, value):
        bucket = dict(item.get(bucket_key, {}) or {})
        key = str(value or "-")
        bucket[key] = int(bucket.get(key, 0) or 0) + 1
        item[bucket_key] = dict(bucket)

    development_state = _thought_memory_development_state(state)
    family_id, family_key = _thought_memory_family_key(state)
    sentence_state = _thought_memory_sentence_state(state, development_state)
    dio_language_sentence = str(state.get("dio_language_sentence", "") or "")
    dio_dialogue_bridge_sentence = str(state.get("dio_dialogue_bridge_sentence", "") or "")
    dio_language_state = str(state.get("dio_language_state", "") or "")
    dio_syntax_origin = str(state.get("dio_syntax_origin", "") or "")
    dio_syntax_signature = str(state.get("dio_syntax_signature", "") or "")
    dio_form_mcm_token = str(state.get("dio_form_mcm_token", "") or "")
    dio_form_mcm_family_token = str(state.get("dio_form_mcm_family_token", "") or "")
    dio_form_mcm_sentence = str(state.get("dio_form_mcm_sentence", "") or "")
    dio_form_mcm_syntax_state = str(state.get("dio_form_mcm_syntax_state", "") or "")
    semantic_origin = str(state.get("semantic_origin_state", "") or "-")
    emergent_state = str(state.get("emergent_structure_state", "") or "-")
    reifung_direction = str(state.get("thought_reifung_direction", "") or "-")
    digest_state = str(state.get("thought_digest_state", "") or "-")
    metaregulator_state = str(state.get("seed_metaregulator_state", "") or "-")

    item.update({
        "thought_seed_id": str(seed_id),
        "thought_family_id": str(family_id),
        "family_key": str(family_key),
        "sentence_state": str(sentence_state),
        "dio_language_sentence": str(dio_language_sentence),
        "dio_dialogue_bridge_sentence": str(dio_dialogue_bridge_sentence),
        "dio_language_state": str(dio_language_state),
        "dio_syntax_origin": str(dio_syntax_origin),
        "dio_syntax_signature": str(dio_syntax_signature),
        "dio_form_mcm_token": str(dio_form_mcm_token),
        "dio_form_mcm_family_token": str(dio_form_mcm_family_token),
        "dio_form_mcm_sentence": str(dio_form_mcm_sentence),
        "dio_form_mcm_syntax_state": str(dio_form_mcm_syntax_state),
        "thought_seed_label": str(state.get("thought_seed_label", item.get("thought_seed_label", "")) or ""),
        "seen": int(seen),
        "first_seen_ts": item.get("first_seen_ts", timestamp),
        "last_seen_ts": timestamp,
        "last_runtime_tick": int(runtime_tick or 0),
        "last_development_state": str(development_state),
        "last_semantic_origin_state": str(semantic_origin),
        "last_emergent_structure_state": str(emergent_state),
        "last_reifung_direction": str(reifung_direction),
        "last_digest_state": str(digest_state),
        "last_seed_metaregulator_state": str(metaregulator_state),
    })
    _count("semantic_origin_counts", semantic_origin)
    _count("emergent_structure_counts", emergent_state)
    _count("reifung_direction_counts", reifung_direction)
    _count("digest_state_counts", digest_state)
    _count("metaregulator_counts", metaregulator_state)
    _count("development_state_counts", development_state)

    _mean("avg_trace_strength", state.get("thought_trace_strength", 0.0))
    _mean("avg_recall_potential", state.get("thought_recall_potential", 0.0))
    _mean("avg_maturity", state.get("thought_maturity", 0.0))
    _mean("avg_reality_binding", state.get("reality_binding_score", 0.0))
    _mean("avg_confirmation", state.get("thought_confirmation_score", 0.0))
    _mean("avg_open_hypothesis_pressure", state.get("thought_open_hypothesis_pressure", 0.0))
    _mean("avg_borrowed_open_hypothesis_pressure", state.get("borrowed_open_hypothesis_pressure", 0.0))
    _mean("avg_own_field_binding_pull", state.get("own_field_binding_pull", 0.0))
    _mean("avg_consequence_balance", state.get("thought_consequence_balance", 0.0), lo=-1.0, hi=1.0)
    _mean("avg_reality_lag", state.get("thought_reality_lag", 0.0))
    _mean("avg_structural_grounding", state.get("thought_structural_grounding", 0.0))
    _mean("avg_drift_risk", state.get("hallucination_drift_risk", 0.0))
    _mean("avg_overthinking_risk", state.get("overthinking_risk", 0.0))
    _mean("avg_digestive_replay_pull", state.get("thought_digestive_replay_pull", 0.0))
    _mean("avg_digestive_distance_pull", state.get("thought_digestive_distance_pull", 0.0))
    _mean("avg_digestive_integration_pull", state.get("thought_digestive_integration_pull", 0.0))
    _mean("avg_digestive_returned_trust", state.get("thought_digestive_returned_trust", 0.0))
    _mean("avg_trust_return_readiness", state.get("trust_return_readiness", 0.0))
    _mean("avg_dio_syntax_density", state.get("dio_syntax_density", 0.0))
    _mean("avg_dio_syntax_compression", state.get("dio_syntax_compression", 0.0))
    _mean("avg_dio_syntax_coherence", state.get("dio_syntax_coherence", 0.0))
    _mean("avg_form_to_mcm_recall", state.get("form_to_mcm_recall", 0.0))
    _mean("avg_mcm_to_form_confirmation", state.get("mcm_to_form_confirmation", 0.0))
    _mean("avg_visual_mcm_context_fit", state.get("visual_mcm_context_fit", 0.0))
    _mean("avg_visual_mcm_mismatch", state.get("visual_mcm_mismatch", 0.0))
    _mean("avg_hypothesis_reality_binding", state.get("hypothesis_reality_binding", 0.0))
    _mean("avg_form_mcm_syntax_density", state.get("form_mcm_syntax_density", 0.0))

    memory[seed_id] = dict(item or {})

    families = getattr(bot, "mcm_thought_family_memory", {}) or {}
    if not isinstance(families, dict):
        families = {}
        bot.mcm_thought_family_memory = families
    family = dict(families.get(family_id, {}) or {})
    family_seen = max(0, int(family.get("seen", 0) or 0)) + 1

    def _family_mean(key, value, lo=0.0, hi=1.0):
        current = _clip(family.get(key, 0.0), lo=lo, hi=hi)
        next_value = _clip(value, lo=lo, hi=hi)
        family[key] = float(current + ((next_value - current) / float(family_seen)))

    def _family_count(bucket_key, value):
        bucket = dict(family.get(bucket_key, {}) or {})
        key = str(value or "-")
        bucket[key] = int(bucket.get(key, 0) or 0) + 1
        family[bucket_key] = dict(bucket)

    seed_ids = [str(value) for value in list(family.get("seed_ids", []) or []) if str(value or "").strip()]
    if seed_id not in seed_ids:
        seed_ids.append(seed_id)
    seed_ids = seed_ids[-32:]
    family.update({
        "thought_family_id": str(family_id),
        "family_key": str(family_key),
        "family_syntax": str(family_key),
        "last_dio_language_sentence": str(dio_language_sentence),
        "last_dio_dialogue_bridge_sentence": str(dio_dialogue_bridge_sentence),
        "last_dio_language_state": str(dio_language_state),
        "last_dio_syntax_origin": str(dio_syntax_origin),
        "last_dio_syntax_signature": str(dio_syntax_signature),
        "last_dio_form_mcm_token": str(dio_form_mcm_token),
        "last_dio_form_mcm_family_token": str(dio_form_mcm_family_token),
        "last_dio_form_mcm_sentence": str(dio_form_mcm_sentence),
        "last_dio_form_mcm_syntax_state": str(dio_form_mcm_syntax_state),
        "seen": int(family_seen),
        "unique_seed_count": int(len(set(seed_ids))),
        "seed_ids": list(seed_ids),
        "first_seen_ts": family.get("first_seen_ts", timestamp),
        "last_seen_ts": timestamp,
        "last_runtime_tick": int(runtime_tick or 0),
        "last_development_state": str(development_state),
        "last_semantic_origin_state": str(semantic_origin),
        "last_emergent_structure_state": str(emergent_state),
        "last_reifung_direction": str(reifung_direction),
        "last_digest_state": str(digest_state),
        "last_seed_metaregulator_state": str(metaregulator_state),
        "last_sentence_state": str(sentence_state),
    })
    _family_count("semantic_origin_counts", semantic_origin)
    _family_count("emergent_structure_counts", emergent_state)
    _family_count("reifung_direction_counts", reifung_direction)
    _family_count("digest_state_counts", digest_state)
    _family_count("metaregulator_counts", metaregulator_state)
    _family_count("development_state_counts", development_state)
    _family_mean("avg_trace_strength", state.get("thought_trace_strength", 0.0))
    _family_mean("avg_recall_potential", state.get("thought_recall_potential", 0.0))
    _family_mean("avg_maturity", state.get("thought_maturity", 0.0))
    _family_mean("avg_reality_binding", state.get("reality_binding_score", 0.0))
    _family_mean("avg_confirmation", state.get("thought_confirmation_score", 0.0))
    _family_mean("avg_open_hypothesis_pressure", state.get("thought_open_hypothesis_pressure", 0.0))
    _family_mean("avg_borrowed_open_hypothesis_pressure", state.get("borrowed_open_hypothesis_pressure", 0.0))
    _family_mean("avg_own_field_binding_pull", state.get("own_field_binding_pull", 0.0))
    _family_mean("avg_consequence_balance", state.get("thought_consequence_balance", 0.0), lo=-1.0, hi=1.0)
    _family_mean("avg_reality_lag", state.get("thought_reality_lag", 0.0))
    _family_mean("avg_structural_grounding", state.get("thought_structural_grounding", 0.0))
    _family_mean("avg_drift_risk", state.get("hallucination_drift_risk", 0.0))
    _family_mean("avg_overthinking_risk", state.get("overthinking_risk", 0.0))
    _family_mean("avg_digestive_replay_pull", state.get("thought_digestive_replay_pull", 0.0))
    _family_mean("avg_digestive_distance_pull", state.get("thought_digestive_distance_pull", 0.0))
    _family_mean("avg_digestive_integration_pull", state.get("thought_digestive_integration_pull", 0.0))
    _family_mean("avg_digestive_returned_trust", state.get("thought_digestive_returned_trust", 0.0))
    _family_mean("avg_trust_return_readiness", state.get("trust_return_readiness", 0.0))
    _family_mean("avg_dio_syntax_density", state.get("dio_syntax_density", 0.0))
    _family_mean("avg_dio_syntax_compression", state.get("dio_syntax_compression", 0.0))
    _family_mean("avg_dio_syntax_coherence", state.get("dio_syntax_coherence", 0.0))
    _family_mean("avg_form_to_mcm_recall", state.get("form_to_mcm_recall", 0.0))
    _family_mean("avg_mcm_to_form_confirmation", state.get("mcm_to_form_confirmation", 0.0))
    _family_mean("avg_visual_mcm_context_fit", state.get("visual_mcm_context_fit", 0.0))
    _family_mean("avg_visual_mcm_mismatch", state.get("visual_mcm_mismatch", 0.0))
    _family_mean("avg_hypothesis_reality_binding", state.get("hypothesis_reality_binding", 0.0))
    _family_mean("avg_form_mcm_syntax_density", state.get("form_mcm_syntax_density", 0.0))
    families[family_id] = dict(family or {})

    form_mcm_families = getattr(bot, "mcm_form_mcm_family_memory", {}) or {}
    if not isinstance(form_mcm_families, dict):
        form_mcm_families = {}
        bot.mcm_form_mcm_family_memory = form_mcm_families
    form_mcm_family_token = str(dio_form_mcm_family_token or "").strip()
    form_mcm_feedback = {}
    form_mcm_family_seen_delta = 0
    if form_mcm_family_token and form_mcm_family_token != "-":
        form_mcm_family = dict(form_mcm_families.get(form_mcm_family_token, {}) or {})
        form_mcm_seen = max(0, int(form_mcm_family.get("seen", 0) or 0)) + 1
        form_mcm_family_seen_delta = 1

        def _fm_mean(key, value, lo=0.0, hi=1.0):
            current = _clip(form_mcm_family.get(key, 0.0), lo=lo, hi=hi)
            next_value = _clip(value, lo=lo, hi=hi)
            form_mcm_family[key] = float(current + ((next_value - current) / float(form_mcm_seen)))

        def _fm_count(bucket_key, value):
            bucket = dict(form_mcm_family.get(bucket_key, {}) or {})
            key = str(value or "-")
            bucket[key] = int(bucket.get(key, 0) or 0) + 1
            form_mcm_family[bucket_key] = dict(bucket)

        form_mcm_family.update({
            "dio_form_mcm_family_token": str(form_mcm_family_token),
            "last_dio_form_mcm_token": str(dio_form_mcm_token),
            "last_dio_form_mcm_syntax_state": str(dio_form_mcm_syntax_state),
            "last_dio_form_mcm_sentence": str(dio_form_mcm_sentence),
            "seen": int(form_mcm_seen),
            "first_seen_ts": form_mcm_family.get("first_seen_ts", timestamp),
            "last_seen_ts": timestamp,
            "last_runtime_tick": int(runtime_tick or 0),
        })
        _fm_count("syntax_state_counts", dio_form_mcm_syntax_state)
        _fm_count("phase_counts", state.get("phase", "-"))
        _fm_count("decision_counts", state.get("decision", "-"))
        _fm_count("emergent_structure_counts", emergent_state)
        _fm_mean("avg_form_to_mcm_recall", state.get("form_to_mcm_recall", 0.0))
        _fm_mean("avg_mcm_to_form_confirmation", state.get("mcm_to_form_confirmation", 0.0))
        _fm_mean("avg_visual_mcm_context_fit", state.get("visual_mcm_context_fit", 0.0))
        _fm_mean("avg_visual_mcm_mismatch", state.get("visual_mcm_mismatch", 0.0))
        _fm_mean("avg_hypothesis_reality_binding", state.get("hypothesis_reality_binding", 0.0))
        _fm_mean("avg_form_mcm_syntax_density", state.get("form_mcm_syntax_density", 0.0))
        _fm_mean("avg_thought_confirmation", state.get("thought_confirmation_score", 0.0))
        _fm_mean("avg_open_hypothesis_pressure", state.get("thought_open_hypothesis_pressure", 0.0))
        _fm_mean("avg_consequence_balance", state.get("thought_consequence_balance", 0.0), lo=-1.0, hi=1.0)

        recurrence = _clip(form_mcm_seen / 24.0)
        avg_binding = _clip(form_mcm_family.get("avg_hypothesis_reality_binding", 0.0))
        avg_confirmation = _clip(form_mcm_family.get("avg_thought_confirmation", 0.0))
        avg_density = _clip(form_mcm_family.get("avg_form_mcm_syntax_density", 0.0))
        avg_fit = _clip(form_mcm_family.get("avg_visual_mcm_context_fit", 0.0))
        avg_mismatch = _clip(form_mcm_family.get("avg_visual_mcm_mismatch", 0.0))
        avg_open_pressure = _clip(form_mcm_family.get("avg_open_hypothesis_pressure", 0.0))
        avg_balance = _clip(form_mcm_family.get("avg_consequence_balance", 0.0), lo=-1.0, hi=1.0)
        family_maturity = _clip(
            (recurrence * 0.26)
            + (avg_binding * 0.22)
            + (avg_confirmation * 0.16)
            + (avg_density * 0.16)
            + (avg_fit * 0.12)
            - (avg_mismatch * 0.12)
        )
        family_trust = _clip(
            (family_maturity * 0.30)
            + (avg_binding * 0.24)
            + (avg_confirmation * 0.20)
            + (max(0.0, avg_balance) * 0.14)
            + (recurrence * 0.08)
            - (avg_mismatch * 0.18)
            - (avg_open_pressure * 0.08)
        )
        family_caution = _clip(
            (avg_mismatch * 0.30)
            + (avg_open_pressure * 0.24)
            + (max(0.0, -avg_balance) * 0.16)
            + (max(0.0, 0.34 - avg_binding) * 0.18)
            + (recurrence * 0.04)
            - (family_trust * 0.10)
        )
        family_reorganization_need = _clip(
            (family_caution * 0.34)
            + (avg_mismatch * 0.24)
            + (max(0.0, avg_open_pressure - avg_confirmation) * 0.22)
            + (max(0.0, 0.30 - avg_density) * 0.12)
        )
        form_mcm_family.update({
            "family_recurrence": float(recurrence),
            "family_maturity": float(family_maturity),
            "family_trust": float(family_trust),
            "family_caution": float(family_caution),
            "family_reorganization_need": float(family_reorganization_need),
        })
        form_mcm_feedback = {
            "form_mcm_family_recurrence": float(recurrence),
            "form_mcm_family_maturity": float(family_maturity),
            "form_mcm_family_trust": float(family_trust),
            "form_mcm_family_caution": float(family_caution),
            "form_mcm_family_reorganization_need": float(family_reorganization_need),
        }
        item.update(form_mcm_feedback)
        form_mcm_families[form_mcm_family_token] = dict(form_mcm_family or {})

    max_seeds = max(32, int(getattr(Config, "MCM_THOUGHT_MEMORY_MAX_SEEDS", 2048) or 2048))
    max_families = max(16, int(getattr(Config, "MCM_THOUGHT_MEMORY_MAX_FAMILIES", 768) or 768))
    max_form_mcm_families = max(16, int(getattr(Config, "MCM_FORM_MCM_MEMORY_MAX_FAMILIES", 768) or 768))
    needs_trim = bool(
        len(memory or {}) > (max_seeds + 128)
        or len(families or {}) > (max_families + 64)
        or len(form_mcm_families or {}) > (max_form_mcm_families + 64)
    )
    if needs_trim:
        profile_stage = "normalize_trim"
        normalized = _normalize_thought_memory({
            "seeds": memory,
            "families": families,
            "form_mcm_families": form_mcm_families,
        })
        memory = dict(normalized.get("seeds", {}) or {})
        families = dict(normalized.get("families", {}) or {})
        form_mcm_families = dict(normalized.get("form_mcm_families", {}) or {})
        summary = dict(normalized.get("summary", {}) or {})
    else:
        prior_summary = dict(getattr(bot, "mcm_thought_memory_summary", {}) or {})

        def _summary_count(key, values):
            if key in prior_summary:
                try:
                    return max(0, int(prior_summary.get(key, 0) or 0))
                except Exception:
                    pass
            return int(sum(int((entry or {}).get("seen", 0) or 0) for entry in values))

        summary = {
            "seed_count": int(len(memory or {})),
            "family_count": int(len(families or {})),
            "form_mcm_family_count": int(len(form_mcm_families or {})),
            "total_seen": int(_summary_count("total_seen", memory.values()) + 1),
            "family_total_seen": int(_summary_count("family_total_seen", families.values()) + 1),
            "form_mcm_family_total_seen": int(
                _summary_count("form_mcm_family_total_seen", form_mcm_families.values())
                + int(form_mcm_family_seen_delta)
            ),
        }

    bot.mcm_thought_memory = memory
    bot.mcm_thought_family_memory = families
    bot.mcm_form_mcm_family_memory = form_mcm_families
    bot.mcm_thought_memory_summary = dict(summary or {})
    bot._thought_memory_dirty = True
    bot._thought_memory_updates = int(getattr(bot, "_thought_memory_updates", 0) or 0) + 1
    profile_stage = "flush_check"
    _flush_thought_memory_if_due(bot, force=False)
    if profile_start:
        try:
            dbr_file_write_profile(
                "thought_memory_update",
                (time.perf_counter() - float(profile_start)) * 1000.0,
                bytes_written=0,
                operation="thought_memory_update",
                extra=(
                    f"stage={profile_stage}"
                    f"|seeds={int(len(memory or {}))}"
                    f"|families={int(len(families or {}))}"
                    f"|form_mcm_families={int(len(form_mcm_families or {}))}"
                    f"|needs_trim={bool(needs_trim)}"
                    f"|updates={int(getattr(bot, '_thought_memory_updates', 0) or 0)}"
                ),
            )
        except Exception:
            pass
    return dict(item or {})

def _write_thought_memory(bot, force=False):

    if bot is None or not bool(getattr(Config, "MCM_THOUGHT_MEMORY_ENABLED", True)):
        return None

    if not bool(force) and not bool(getattr(bot, "_thought_memory_dirty", False)):
        return None

    payload = _normalize_thought_memory({
        "seeds": getattr(bot, "mcm_thought_memory", {}) or {},
        "families": getattr(bot, "mcm_thought_family_memory", {}) or {},
        "form_mcm_families": getattr(bot, "mcm_form_mcm_family_memory", {}) or {},
    })
    payload.setdefault("summary", {})["last_saved_ts"] = float(time.time())
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    filepath = _thought_memory_path()
    written = _write_text_atomic_with_retry(
        filepath,
        text,
        operation="thought_memory_write",
        extra=(
            f"seeds={int(payload.get('summary', {}).get('seed_count', 0) or 0)}"
            f"|families={int(payload.get('summary', {}).get('family_count', 0) or 0)}"
            f"|total_seen={int(payload.get('summary', {}).get('total_seen', 0) or 0)}"
            f"|family_total_seen={int(payload.get('summary', {}).get('family_total_seen', 0) or 0)}"
        ),
    )
    if not written:
        bot._thought_memory_dirty = True
        return None

    bot.mcm_thought_memory = dict(payload.get("seeds", {}) or {})
    bot.mcm_thought_family_memory = dict(payload.get("families", {}) or {})
    bot.mcm_form_mcm_family_memory = dict(payload.get("form_mcm_families", {}) or {})
    bot.mcm_thought_memory_summary = dict(payload.get("summary", {}) or {})
    bot._thought_memory_dirty = False
    bot._thought_memory_last_save_ts = float(time.time())
    return dict(payload or {})

def _flush_thought_memory_if_due(bot, force=False):

    if bot is None or not bool(getattr(Config, "MCM_THOUGHT_MEMORY_ENABLED", True)):
        return None

    if not bool(force) and not bool(getattr(bot, "_thought_memory_dirty", False)):
        return None

    updates = int(getattr(bot, "_thought_memory_updates", 0) or 0)
    every_n = max(1, int(getattr(Config, "MCM_THOUGHT_MEMORY_SAVE_EVERY_N", 64) or 64))
    if not bool(force) and updates % every_n != 0:
        return None
    if not bool(force):
        cooldown = max(0.0, float(getattr(Config, "MCM_MEMORY_SAVE_COOLDOWN_SECONDS", 0.0) or 0.0))
        last_save_ts = float(getattr(bot, "_thought_memory_last_save_ts", 0.0) or 0.0)
        if cooldown > 0.0 and (time.time() - last_save_ts) < cooldown:
            return None

    return _write_thought_memory(bot, force=True)


__all__ = [
    "_thought_memory_path",
    "_empty_thought_memory_payload",
    "_thought_memory_family_key",
    "_thought_memory_sentence_state",
    "_normalize_thought_memory_families",
    "_normalize_form_mcm_families",
    "_normalize_thought_memory",
    "_read_thought_memory",
    "_ensure_thought_memory_loaded",
    "_thought_memory_development_state",
    "_update_thought_memory",
    "_write_thought_memory",
    "_flush_thought_memory_if_due",
]
