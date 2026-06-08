"""Form-symbol memory storage and normalization.

This module owns persistent form-symbol memory mechanics: load, normalize,
write and flush. It has no dependency on the Brain module.
"""

import json
import os
import time

from config import Config
from debug_tools.writers import dbr_debug, dbr_file_write_profile


def _form_symbol_memory_path(path=None):

    if path is not None:
        return str(path)

    configured = getattr(Config, "MCM_FORM_SYMBOL_MEMORY_PATH", "bot_memory/form_symbol_memory.json")
    return str(configured or "bot_memory/form_symbol_memory.json")

def _normalize_form_symbol_memory_symbols(symbols):

    if not isinstance(symbols, dict):
        return {}

    normalized = {}
    max_symbols = max(32, int(getattr(Config, "MCM_FORM_SYMBOL_MEMORY_MAX_SYMBOLS", 1024) or 1024))
    max_variants = max(1, int(getattr(Config, "MCM_FORM_SYMBOL_MEMORY_MAX_VARIANTS", 12) or 12))

    def _num(item, key, default=0.0):
        try:
            return float((item or {}).get(key, default) or default)
        except Exception:
            return float(default)

    candidates = []
    for symbol_id, raw_item in dict(symbols or {}).items():
        if not isinstance(raw_item, dict):
            continue

        symbol_key = str(symbol_id or raw_item.get("symbol_id", "") or "").strip()
        if not symbol_key:
            continue

        item = dict(raw_item or {})
        seen = max(0, int(_num(item, "seen", 0)))
        variants = dict(item.get("variants", {}) or {})
        cleaned_variants = {}
        for variant_key, variant_item in sorted(
            variants.items(),
            key=lambda kv: int((kv[1] or {}).get("seen", 0) or 0) if isinstance(kv[1], dict) else 0,
            reverse=True,
        )[:max_variants]:
            if not isinstance(variant_item, dict):
                continue
            cleaned_variants[str(variant_key)] = {
                "seen": max(0, int(_num(variant_item, "seen", 0))),
                "distance": max(0.0, min(1.0, _num(variant_item, "distance", 0.0))),
                "bearing": max(0.0, min(1.0, _num(variant_item, "bearing", 0.0))),
                "fragility": max(0.0, min(1.0, _num(variant_item, "fragility", 0.0))),
                "visual_blindness": max(0.0, min(1.0, _num(variant_item, "visual_blindness", 0.0))),
                "visual_clarity": max(0.0, min(1.0, _num(variant_item, "visual_clarity", 0.0))),
                "object_stability": max(0.0, min(1.0, _num(variant_item, "object_stability", 0.0))),
                "uncertain_exposure": max(0.0, min(1.0, _num(variant_item, "uncertain_exposure", 0.0))),
                "last_seen_ts": variant_item.get("last_seen_ts", None),
            }

        avg_vector = []
        for value in list(item.get("avg_vector", []) or [])[:32]:
            try:
                avg_vector.append(float(value))
            except Exception:
                continue

        cleaned = {
            "symbol_id": str(symbol_key),
            "form_key": str(item.get("form_key", item.get("family_key", "")) or ""),
            "family_key": str(item.get("family_key", item.get("form_key", "")) or ""),
            "scope": str(item.get("scope", "") or ""),
            "abstraction_level": max(0, int(_num(item, "abstraction_level", 0))),
            "seen": int(seen),
            "avg_vector": list(avg_vector or []),
            "variance": max(0.0, min(1.0, _num(item, "variance", 0.0))),
            "maturity": max(0.0, min(1.0, _num(item, "maturity", 0.0))),
            "stability": max(0.0, min(1.0, _num(item, "stability", 0.0))),
            "resonance": max(0.0, min(1.0, _num(item, "resonance", 0.0))),
            "bearing": max(0.0, min(1.0, _num(item, "bearing", 0.0))),
            "fragility": max(0.0, min(1.0, _num(item, "fragility", 0.0))),
            "resolution_quality": max(0.0, min(1.0, _num(item, "resolution_quality", 0.0))),
            "detail_pressure": max(0.0, min(1.0, _num(item, "detail_pressure", 0.0))),
            "symbolic_object_distance": max(0.0, min(1.0, _num(item, "symbolic_object_distance", 0.0))),
            "symbolic_containment": max(0.0, min(1.0, _num(item, "symbolic_containment", 0.0))),
            "symbolic_field_decoupling": max(0.0, min(1.0, _num(item, "symbolic_field_decoupling", 0.0))),
            "development_quality": max(-1.0, min(1.0, _num(item, "development_quality", 0.0))),
            "action_affinity": max(0.0, min(1.0, _num(item, "action_affinity", 0.50))),
            "observation_affinity": max(0.0, min(1.0, _num(item, "observation_affinity", 0.0))),
            "context_reframe_potential": max(0.0, min(1.0, _num(item, "context_reframe_potential", 0.0))),
            "learning_trust": max(0.0, min(1.0, _num(item, "learning_trust", 0.0))),
            "action_trust": max(0.0, min(1.0, _num(item, "action_trust", 0.0))),
            "caution_trust": max(0.0, min(1.0, _num(item, "caution_trust", 0.0))),
            "contact_maturity": max(0.0, min(1.0, _num(item, "contact_maturity", 0.0))),
            "contact_utility": max(0.0, min(1.0, _num(item, "contact_utility", 0.0))),
            "contact_pain_memory": max(0.0, min(1.0, _num(item, "contact_pain_memory", 0.0))),
            "contact_carefulness": max(0.0, min(1.0, _num(item, "contact_carefulness", 0.0))),
            "contact_burden_evidence": max(0.0, min(1.0, _num(item, "contact_burden_evidence", 0.0))),
            "contact_utility_evidence": max(0.0, min(1.0, _num(item, "contact_utility_evidence", 0.0))),
            "contact_learning_state": str(item.get("contact_learning_state", "unformed_contact") or "unformed_contact"),
            "constructive_seen": max(0, int(_num(item, "constructive_seen", 0))),
            "unconstructive_seen": max(0, int(_num(item, "unconstructive_seen", 0))),
            "last_zoom_need": max(0.0, min(1.0, _num(item, "last_zoom_need", 0.0))),
            "last_load_reduction": max(0.0, min(1.0, _num(item, "last_load_reduction", 0.0))),
            "uncertain_form_exposure": max(0.0, min(1.0, _num(item, "uncertain_form_exposure", 0.0))),
            "uncertainty_familiarity": max(0.0, min(1.0, _num(item, "uncertainty_familiarity", 0.0))),
            "variant_similarity": max(0.0, min(1.0, _num(item, "variant_similarity", 0.0))),
            "variant_spread": max(0.0, min(1.0, _num(item, "variant_spread", 0.0))),
            "variant_learning_pressure": max(0.0, min(1.0, _num(item, "variant_learning_pressure", 0.0))),
            "variant_bearing_memory": max(0.0, min(1.0, _num(item, "variant_bearing_memory", 0.0))),
            "uncertain_form_family_state": str(item.get("uncertain_form_family_state", "quiet_form_family") or "quiet_form_family"),
            "first_seen_ts": item.get("first_seen_ts", None),
            "last_seen_ts": item.get("last_seen_ts", None),
            "variants": dict(cleaned_variants or {}),
        }
        score = (float(cleaned.get("seen", 0) or 0) * 1.0) + (float(cleaned.get("resonance", 0.0) or 0.0) * 32.0)
        candidates.append((score, symbol_key, cleaned))

    for _, symbol_key, cleaned in sorted(candidates, reverse=True)[:max_symbols]:
        normalized[str(symbol_key)] = dict(cleaned or {})

    return normalized

def _normalize_form_symbol_memory_compounds(compounds):

    if not isinstance(compounds, dict):
        return {}

    normalized = {}
    max_compounds = max(16, int(getattr(Config, "MCM_FORM_SYMBOL_MEMORY_MAX_COMPOUNDS", 768) or 768))

    def _num(item, key, default=0.0):
        try:
            return float((item or {}).get(key, default) or default)
        except Exception:
            return float(default)

    candidates = []
    for compound_id, raw_item in dict(compounds or {}).items():
        if not isinstance(raw_item, dict):
            continue

        compound_key = str(compound_id or raw_item.get("compound_id", "") or "").strip()
        if not compound_key:
            continue

        item = dict(raw_item or {})
        seen = max(0, int(_num(item, "seen", 0)))
        cleaned = {
            "compound_id": str(compound_key),
            "compound_key": str(item.get("compound_key", "") or ""),
            "left_symbol_id": str(item.get("left_symbol_id", "") or ""),
            "right_symbol_id": str(item.get("right_symbol_id", "") or ""),
            "scope": str(item.get("scope", "") or ""),
            "seen": int(seen),
            "maturity": max(0.0, min(1.0, _num(item, "maturity", 0.0))),
            "stability": max(0.0, min(1.0, _num(item, "stability", 0.0))),
            "resonance": max(0.0, min(1.0, _num(item, "resonance", 0.0))),
            "bearing": max(0.0, min(1.0, _num(item, "bearing", 0.0))),
            "load_reduction": max(0.0, min(1.0, _num(item, "load_reduction", 0.0))),
            "novelty": max(0.0, min(1.0, _num(item, "novelty", 0.0))),
            "development_quality": max(-1.0, min(1.0, _num(item, "development_quality", 0.0))),
            "action_affinity": max(0.0, min(1.0, _num(item, "action_affinity", 0.50))),
            "observation_affinity": max(0.0, min(1.0, _num(item, "observation_affinity", 0.0))),
            "context_reframe_potential": max(0.0, min(1.0, _num(item, "context_reframe_potential", 0.0))),
            "learning_trust": max(0.0, min(1.0, _num(item, "learning_trust", 0.0))),
            "action_trust": max(0.0, min(1.0, _num(item, "action_trust", 0.0))),
            "caution_trust": max(0.0, min(1.0, _num(item, "caution_trust", 0.0))),
            "contact_maturity": max(0.0, min(1.0, _num(item, "contact_maturity", 0.0))),
            "contact_utility": max(0.0, min(1.0, _num(item, "contact_utility", 0.0))),
            "contact_pain_memory": max(0.0, min(1.0, _num(item, "contact_pain_memory", 0.0))),
            "contact_carefulness": max(0.0, min(1.0, _num(item, "contact_carefulness", 0.0))),
            "contact_burden_evidence": max(0.0, min(1.0, _num(item, "contact_burden_evidence", 0.0))),
            "contact_utility_evidence": max(0.0, min(1.0, _num(item, "contact_utility_evidence", 0.0))),
            "contact_learning_state": str(item.get("contact_learning_state", "unformed_contact") or "unformed_contact"),
            "constructive_seen": max(0, int(_num(item, "constructive_seen", 0))),
            "unconstructive_seen": max(0, int(_num(item, "unconstructive_seen", 0))),
            "first_seen_ts": item.get("first_seen_ts", None),
            "last_seen_ts": item.get("last_seen_ts", None),
        }
        score = (float(seen) * 1.0) + (float(cleaned.get("resonance", 0.0) or 0.0) * 28.0)
        candidates.append((score, compound_key, cleaned))

    for _, compound_key, cleaned in sorted(candidates, reverse=True)[:max_compounds]:
        normalized[str(compound_key)] = dict(cleaned or {})

    return normalized

def _read_form_symbol_memory(path=None):

    filepath = _form_symbol_memory_path(path)
    default_payload = {
        "version": 1,
        "symbols": {},
        "compounds": {},
        "summary": {
            "symbol_count": 0,
            "compound_count": 0,
            "total_seen": 0,
            "compound_total_seen": 0,
        },
    }

    if not bool(getattr(Config, "MCM_FORM_SYMBOL_MEMORY_ENABLED", True)):
        return dict(default_payload)

    if not os.path.exists(filepath):
        return dict(default_payload)

    try:
        with open(filepath, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except Exception:
        return dict(default_payload)

    symbols = _normalize_form_symbol_memory_symbols((raw or {}).get("symbols", {}))
    compounds = _normalize_form_symbol_memory_compounds((raw or {}).get("compounds", {}))
    total_seen = sum(int((item or {}).get("seen", 0) or 0) for item in symbols.values())
    compound_total_seen = sum(int((item or {}).get("seen", 0) or 0) for item in compounds.values())
    return {
        "version": 1,
        "symbols": dict(symbols or {}),
        "compounds": dict(compounds or {}),
        "summary": {
            "symbol_count": int(len(symbols or {})),
            "compound_count": int(len(compounds or {})),
            "total_seen": int(total_seen),
            "compound_total_seen": int(compound_total_seen),
            "loaded_from": str(filepath),
            "last_saved_ts": (raw or {}).get("summary", {}).get("last_saved_ts", None) if isinstance((raw or {}).get("summary", {}), dict) else None,
        },
    }

def _ensure_form_symbol_memory_loaded(bot):

    if bot is None:
        return {}

    if bool(getattr(bot, "_form_symbol_memory_loaded", False)):
        return dict(getattr(bot, "form_symbol_space", {}) or {})

    payload = _read_form_symbol_memory()
    symbols = dict(payload.get("symbols", {}) or {})
    compounds = dict(payload.get("compounds", {}) or {})
    current = dict(getattr(bot, "form_symbol_space", {}) or {})
    current.update(symbols)
    bot.form_symbol_space = dict(current or {})
    compound_current = dict(getattr(bot, "form_symbol_compound_space", {}) or {})
    compound_current.update(compounds)
    bot.form_symbol_compound_space = dict(compound_current or {})
    bot._form_symbol_memory_loaded = True
    bot._form_symbol_memory_dirty = False
    bot._form_symbol_memory_updates = 0
    bot._form_symbol_memory_last_save_ts = float(time.time())
    bot.form_symbol_memory_summary = dict(payload.get("summary", {}) or {})
    return dict(bot.form_symbol_space or {})

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

def _write_form_symbol_memory(bot, force=False):

    if bot is None or not bool(getattr(Config, "MCM_FORM_SYMBOL_MEMORY_ENABLED", True)):
        return None

    if not bool(force) and not bool(getattr(bot, "_form_symbol_memory_dirty", False)):
        return None

    symbols = _normalize_form_symbol_memory_symbols(getattr(bot, "form_symbol_space", {}) or {})
    compounds = _normalize_form_symbol_memory_compounds(getattr(bot, "form_symbol_compound_space", {}) or {})
    total_seen = sum(int((item or {}).get("seen", 0) or 0) for item in symbols.values())
    compound_total_seen = sum(int((item or {}).get("seen", 0) or 0) for item in compounds.values())
    filepath = _form_symbol_memory_path()
    payload = {
        "version": 1,
        "summary": {
            "symbol_count": int(len(symbols or {})),
            "compound_count": int(len(compounds or {})),
            "total_seen": int(total_seen),
            "compound_total_seen": int(compound_total_seen),
            "last_saved_ts": float(time.time()),
        },
        "symbols": dict(symbols or {}),
        "compounds": dict(compounds or {}),
    }

    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    written = _write_text_atomic_with_retry(
        filepath,
        text,
        operation="form_symbol_memory_write",
        extra=f"symbols={int(len(symbols or {}))}|total_seen={int(total_seen)}",
    )
    if not written:
        bot._form_symbol_memory_dirty = True
        return None

    bot.form_symbol_space = dict(symbols or {})
    bot.form_symbol_compound_space = dict(compounds or {})
    bot.form_symbol_memory_summary = dict(payload.get("summary", {}) or {})
    bot._form_symbol_memory_dirty = False
    bot._form_symbol_memory_last_save_ts = float(time.time())
    return dict(payload or {})

def _flush_form_symbol_memory_if_due(bot, force=False):

    if bot is None or not bool(getattr(Config, "MCM_FORM_SYMBOL_MEMORY_ENABLED", True)):
        return None

    if not bool(force) and not bool(getattr(bot, "_form_symbol_memory_dirty", False)):
        return None

    updates = int(getattr(bot, "_form_symbol_memory_updates", 0) or 0)
    every_n = max(1, int(getattr(Config, "MCM_FORM_SYMBOL_MEMORY_SAVE_EVERY_N", 64) or 64))
    if not bool(force) and updates % every_n != 0:
        return None
    if not bool(force):
        cooldown = max(0.0, float(getattr(Config, "MCM_MEMORY_SAVE_COOLDOWN_SECONDS", 0.0) or 0.0))
        last_save_ts = float(getattr(bot, "_form_symbol_memory_last_save_ts", 0.0) or 0.0)
        if cooldown > 0.0 and (time.time() - last_save_ts) < cooldown:
            return None

    return _write_form_symbol_memory(bot, force=True)


__all__ = [
    "_ensure_form_symbol_memory_loaded",
    "_flush_form_symbol_memory_if_due",
    "_form_symbol_memory_path",
    "_normalize_form_symbol_memory_compounds",
    "_normalize_form_symbol_memory_symbols",
    "_read_form_symbol_memory",
    "_write_form_symbol_memory",
    "_write_text_atomic_with_retry",
]
