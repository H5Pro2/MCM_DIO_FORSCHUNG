# ==================================================
# memory_state.py
# Persistente Erfahrungsspeicherung
# - Signature Memory
# - Context Cluster
# - MCM Memory
# ==================================================
import json
import os
import time
from config import Config
from debug_tools.writers import dbr_file_write_profile, dbr_profile

# --------------------------------------------------
# PATH
# --------------------------------------------------
def _memory_state_path(path: str | None = None) -> str:

    if path is not None:
        return str(path)

    configured = getattr(Config, "MCM_MEMORY_STATE_PATH", "bot_memory/memory_state.json")
    configured = str(configured or "bot_memory/memory_state.json")
    return configured
# --------------------------------------------------
# FS
# --------------------------------------------------
def _ensure_dir(path: str):

    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
# --------------------------------------------------
# DIRTY
# --------------------------------------------------
def mark_memory_state_dirty(bot=None) -> bool:

    if bot is None:
        return False

    bot._memory_state_dirty = True
    return True
# --------------------------------------------------
# FLUSH IF DUE
# --------------------------------------------------
def flush_memory_state_if_due(bot=None, force: bool = False):

    if bot is None:
        return None

    if not bool(getattr(bot, "_memory_state_dirty", False)) and not bool(force):
        return None

    now_ts = float(time.time())
    cooldown = max(
        0.0,
        float(getattr(Config, "MCM_MEMORY_SAVE_COOLDOWN_SECONDS", 1.25) or 1.25),
    )

    if not force and (now_ts - float(getattr(bot, "_memory_state_last_save_ts", 0.0) or 0.0)) < cooldown:
        return None

    try:
        return bot._save_memory_state(force=True)
    except TypeError:
        return bot._save_memory_state()
# --------------------------------------------------
# FINALIZE SAVE
# --------------------------------------------------
def finalize_memory_state_save(bot=None, payload: dict | None = None):

    if bot is None or not isinstance(payload, dict):
        return None

    saved_payload = dict(payload or {})
    bot._memory_state_payload = dict(saved_payload or {})
    bot._memory_state_mcm_loaded = isinstance(getattr(bot, "mcm_brain", None), dict)
    bot._memory_state_dirty = False
    bot._memory_state_last_save_ts = float(time.time())
    return dict(saved_payload or {})
# --------------------------------------------------
# INITIALIZE BOOTSTRAP
# --------------------------------------------------
def initialize_memory_state_bootstrap(bot=None, payload: dict | None = None) -> dict:

    if bot is None:
        return {
            "payload": {},
            "loaded": False,
        }

    memory_payload = dict(payload or read_memory_state() or {})

    bot._memory_state_payload = dict(memory_payload or {})
    bot._memory_state_mcm_loaded = False

    apply_memory_state(
        bot,
        memory_payload,
    )

    bot._memory_state_mcm_loaded = isinstance(getattr(bot, "mcm_brain", None), dict)

    return {
        "payload": dict(memory_payload or {}),
        "loaded": bool(getattr(bot, "_memory_state_mcm_loaded", False)),
    }
# --------------------------------------------------
# CAST HELPERS
# --------------------------------------------------
def _to_int(value, default: int = 0) -> int:

    try:
        return int(value)
    except Exception:
        return int(default)
# --------------------------------------------------
def normalize_json_state(value):

    if isinstance(value, dict):
        normalized = {}

        for key, item in value.items():
            if key is None:
                continue

            normalized[str(key)] = normalize_json_state(item)

        return normalized

    if isinstance(value, list):
        return [normalize_json_state(item) for item in list(value or [])[:128]]

    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    return _to_str(value, None)
# --------------------------------------------------
def _to_float(value, default: float = 0.0) -> float:

    try:
        return float(value)
    except Exception:
        return float(default)
# --------------------------------------------------
def _to_str(value, default: str | None = None) -> str | None:

    if value is None:
        return default

    try:
        return str(value)
    except Exception:
        return default
# --------------------------------------------------
def _to_float_list(values) -> list[float]:

    cleaned = []

    for value in list(values or []):
        try:
            cleaned.append(float(value))
        except Exception:
            continue

    return cleaned
# --------------------------------------------------
def _to_str_list(values) -> list[str]:

    cleaned = []

    for value in list(values or []):
        if value is None:
            continue

        try:
            cleaned.append(str(value))
        except Exception:
            continue

    return cleaned
# --------------------------------------------------
def normalize_inner_field_history_state(history_state) -> dict:

    item = dict(history_state or {})
    raw_history = item.get("inner_field_history", [])

    if not isinstance(raw_history, list):
        raw_history = []

    limit = max(
        4,
        min(
            256,
            _to_int(getattr(Config, "MCM_INNER_FIELD_HISTORY_LIMIT", 48), 48),
        ),
    )

    normalized_history = []

    for raw_entry in list(raw_history or [])[-limit:]:
        if not isinstance(raw_entry, dict):
            continue

        entry = dict(raw_entry or {})
        normalized_history.append(
            {
                "timestamp": entry.get("timestamp", None),
                "runtime_tick_seq": max(0, _to_int(entry.get("runtime_tick_seq", 0), 0)),
                "field_mean_energy": _to_float(entry.get("field_mean_energy", 0.0), 0.0),
                "field_mean_velocity": _to_float(entry.get("field_mean_velocity", 0.0), 0.0),
                "field_pressure": max(0.0, _to_float(entry.get("field_pressure", 0.0), 0.0)),
                "field_cluster_count": max(0, _to_int(entry.get("field_cluster_count", 0), 0)),
                "field_areal_count": max(0, _to_int(entry.get("field_areal_count", 0), 0)),
                "field_areal_pressure_mean": max(0.0, _to_float(entry.get("field_areal_pressure_mean", 0.0), 0.0)),
                "field_areal_coherence_mean": max(0.0, _to_float(entry.get("field_areal_coherence_mean", 0.0), 0.0)),
                "field_areal_conflict_mean": max(0.0, _to_float(entry.get("field_areal_conflict_mean", 0.0), 0.0)),
                "field_topology_coherence": max(0.0, min(1.0, _to_float(entry.get("field_topology_coherence", 0.0), 0.0))),
                "field_topology_tension": max(0.0, min(1.0, _to_float(entry.get("field_topology_tension", 0.0), 0.0))),
                "neural_felt_bearing": max(0.0, min(1.0, _to_float(entry.get("neural_felt_bearing", 0.0), 0.0))),
                "neural_felt_pressure": max(0.0, min(1.0, _to_float(entry.get("neural_felt_pressure", 0.0), 0.0))),
                "neural_felt_memory_resonance": max(0.0, min(1.0, _to_float(entry.get("neural_felt_memory_resonance", 0.0), 0.0))),
                "neural_felt_context_reactivation": max(0.0, min(1.0, _to_float(entry.get("neural_felt_context_reactivation", 0.0), 0.0))),
                "neural_felt_label": _to_str(entry.get("neural_felt_label"), "quiet_neural_felt"),
                "delta_field_pressure": max(-1.0, min(1.0, _to_float(entry.get("delta_field_pressure", 0.0), 0.0))),
                "delta_neural_felt_bearing": max(-1.0, min(1.0, _to_float(entry.get("delta_neural_felt_bearing", 0.0), 0.0))),
                "delta_topology_tension": max(-1.0, min(1.0, _to_float(entry.get("delta_topology_tension", 0.0), 0.0))),
                "delta_memory_resonance": max(-1.0, min(1.0, _to_float(entry.get("delta_memory_resonance", 0.0), 0.0))),
            }
        )

    return {
        "inner_field_history": list(normalized_history or []),
        "inner_field_history_length": int(len(normalized_history)),
        "inner_field_pressure_trend": max(-1.0, min(1.0, _to_float(item.get("inner_field_pressure_trend", 0.0), 0.0))),
        "inner_field_bearing_trend": max(-1.0, min(1.0, _to_float(item.get("inner_field_bearing_trend", 0.0), 0.0))),
        "inner_field_topology_tension_trend": max(-1.0, min(1.0, _to_float(item.get("inner_field_topology_tension_trend", 0.0), 0.0))),
        "inner_field_memory_resonance_trend": max(-1.0, min(1.0, _to_float(item.get("inner_field_memory_resonance_trend", 0.0), 0.0))),
        "inner_field_history_label": _to_str(item.get("inner_field_history_label"), "empty_field_history" if not normalized_history else "stable_field_trace"),
    }
# --------------------------------------------------
# NORMALIZE SIGNATURE MEMORY
# --------------------------------------------------
def normalize_signature_memory(signature_memory) -> dict:

    normalized = {}

    if not isinstance(signature_memory, dict):
        return normalized

    for key, item in signature_memory.items():
        if key is None or not isinstance(item, dict):
            continue

        signature_key = str(key).strip()
        if not signature_key:
            continue

        normalized[signature_key] = {
            "seen": max(0, _to_int(item.get("seen", 0), 0)),
            "tp": max(0, _to_int(item.get("tp", 0), 0)),
            "sl": max(0, _to_int(item.get("sl", 0), 0)),
            "cancel": max(0, _to_int(item.get("cancel", 0), 0)),
            "timeout": max(0, _to_int(item.get("timeout", 0), 0)),
            "score": max(-6.0, min(6.0, _to_float(item.get("score", 0.0), 0.0))),
            "last_outcome": _to_str(item.get("last_outcome"), None),
            "age": max(0, _to_int(item.get("age", 0), 0)),
            "signature_vector": _to_float_list(item.get("signature_vector", [])),
        }

    if len(normalized) > 180:
        sorted_items = sorted(
            normalized.items(),
            key=lambda entry: (
                abs(_to_float((entry[1] or {}).get("score", 0.0), 0.0)),
                -max(0, _to_int((entry[1] or {}).get("age", 0), 0)),
                max(0, _to_int((entry[1] or {}).get("seen", 0), 0)),
            ),
            reverse=True,
        )[:180]
        normalized = dict(sorted_items)

    return normalized
# --------------------------------------------------
# NORMALIZE CONTEXT CLUSTERS
# --------------------------------------------------
def normalize_context_clusters(context_clusters) -> dict:

    normalized = {}

    if not isinstance(context_clusters, dict):
        return normalized

    for cluster_id, item in context_clusters.items():
        if cluster_id is None or not isinstance(item, dict):
            continue

        cluster_key = str(cluster_id).strip()
        if not cluster_key:
            continue

        normalized[cluster_key] = {
            "cluster_id": _to_str(item.get("cluster_id"), cluster_key),
            "center_vector": _to_float_list(item.get("center_vector", [])),
            "variance": max(0.0, _to_float(item.get("variance", 0.0), 0.0)),
            "radius": max(0.0, _to_float(item.get("radius", 0.0), 0.0)),
            "seen": max(0, _to_int(item.get("seen", 0), 0)),
            "tp": max(0, _to_int(item.get("tp", 0), 0)),
            "sl": max(0, _to_int(item.get("sl", 0), 0)),
            "cancel": max(0, _to_int(item.get("cancel", 0), 0)),
            "timeout": max(0, _to_int(item.get("timeout", 0), 0)),
            "score": max(-12.0, min(12.0, _to_float(item.get("score", 0.0), 0.0))),
            "trust": max(0.0, min(1.0, _to_float(item.get("trust", 0.0), 0.0))),
            "age": max(0, _to_int(item.get("age", 0), 0)),
            "signature_keys": _to_str_list(item.get("signature_keys", []))[-24:],
            "last_signature_key": _to_str(item.get("last_signature_key"), None),
            "last_outcome": _to_str(item.get("last_outcome"), None),
            "last_distance": max(0.0, _to_float(item.get("last_distance", 0.0), 0.0)),
        }

    return normalized
# --------------------------------------------------
def normalize_inner_context_clusters(inner_context_clusters) -> dict:

    normalized = {}

    if not isinstance(inner_context_clusters, dict):
        return normalized

    for cluster_id, item in inner_context_clusters.items():
        if cluster_id is None or not isinstance(item, dict):
            continue

        cluster_key = str(cluster_id).strip()
        if not cluster_key:
            continue

        normalized[cluster_key] = {
            "cluster_id": _to_str(item.get("cluster_id"), cluster_key),
            "center_vector": _to_float_list(item.get("center_vector", [])),
            "variance": max(0.0, _to_float(item.get("variance", 0.0), 0.0)),
            "radius": max(0.0, _to_float(item.get("radius", 0.0), 0.0)),
            "seen": max(0, _to_int(item.get("seen", 0), 0)),
            "tp": max(0, _to_int(item.get("tp", 0), 0)),
            "sl": max(0, _to_int(item.get("sl", 0), 0)),
            "cancel": max(0, _to_int(item.get("cancel", 0), 0)),
            "timeout": max(0, _to_int(item.get("timeout", 0), 0)),
            "score": max(-12.0, min(12.0, _to_float(item.get("score", 0.0), 0.0))),
            "trust": max(0.0, min(1.0, _to_float(item.get("trust", 0.0), 0.0))),
            "age": max(0, _to_int(item.get("age", 0), 0)),
            "signature_keys": _to_str_list(item.get("signature_keys", []))[-24:],
            "last_signature_key": _to_str(item.get("last_signature_key"), None),
            "last_outcome": _to_str(item.get("last_outcome"), None),
            "last_distance": max(0.0, _to_float(item.get("last_distance", 0.0), 0.0)),
            "field_density": max(0.0, min(1.0, _to_float(item.get("field_density", 0.0), 0.0))),
            "field_stability": max(0.0, min(1.0, _to_float(item.get("field_stability", 0.0), 0.0))),
            "field_cluster_count": max(0, _to_int(item.get("field_cluster_count", 0), 0)),
            "field_cluster_mass_mean": max(0.0, min(1.0, _to_float(item.get("field_cluster_mass_mean", 0.0), 0.0))),
            "field_cluster_mass_max": max(0.0, min(1.0, _to_float(item.get("field_cluster_mass_max", 0.0), 0.0))),
            "field_cluster_center_spread": max(0.0, _to_float(item.get("field_cluster_center_spread", 0.0), 0.0)),
            "field_cluster_separation": max(0.0, _to_float(item.get("field_cluster_separation", 0.0), 0.0)),
            "field_cluster_center_drift": max(0.0, _to_float(item.get("field_cluster_center_drift", 0.0), 0.0)),
            "field_cluster_count_drift": max(0.0, _to_float(item.get("field_cluster_count_drift", 0.0), 0.0)),
            "field_velocity_trend": _to_float(item.get("field_velocity_trend", 0.0), 0.0),
            "field_reorganization_direction": _to_str(item.get("field_reorganization_direction"), "stable"),
            "field_mean_velocity": max(0.0, _to_float(item.get("field_mean_velocity", 0.0), 0.0)),
            "field_regulation_pressure": max(0.0, _to_float(item.get("field_regulation_pressure", 0.0), 0.0)),
            "field_neuron_count": max(0, _to_int(item.get("field_neuron_count", 0), 0)),
            "field_neuron_activation_mean": max(0.0, _to_float(item.get("field_neuron_activation_mean", 0.0), 0.0)),
            "field_neuron_activation_max": max(0.0, _to_float(item.get("field_neuron_activation_max", 0.0), 0.0)),
            "field_neuron_stability_mean": max(0.0, _to_float(item.get("field_neuron_stability_mean", 0.0), 0.0)),
            "field_neuron_regulation_pressure_mean": max(0.0, _to_float(item.get("field_neuron_regulation_pressure_mean", 0.0), 0.0)),
            "field_neuron_memory_norm_mean": max(0.0, _to_float(item.get("field_neuron_memory_norm_mean", 0.0), 0.0)),
            "field_neuron_coupling_norm_mean": max(0.0, _to_float(item.get("field_neuron_coupling_norm_mean", 0.0), 0.0)),
            "field_neuron_regulation_force_norm_mean": max(0.0, _to_float(item.get("field_neuron_regulation_force_norm_mean", 0.0), 0.0)),
            "field_neuron_external_impulse_norm_mean": max(0.0, _to_float(item.get("field_neuron_external_impulse_norm_mean", 0.0), 0.0)),
            "field_neuron_context_memory_impulse_norm_mean": max(0.0, _to_float(item.get("field_neuron_context_memory_impulse_norm_mean", 0.0), 0.0)),
            "field_areal_count": max(0, _to_int(item.get("field_areal_count", 0), 0)),
            "field_areal_activation_mean": max(0.0, _to_float(item.get("field_areal_activation_mean", 0.0), 0.0)),
            "field_areal_stability_mean": max(0.0, _to_float(item.get("field_areal_stability_mean", 0.0), 0.0)),
            "field_areal_pressure_mean": max(0.0, _to_float(item.get("field_areal_pressure_mean", 0.0), 0.0)),
            "field_areal_drift": max(0.0, _to_float(item.get("field_areal_drift", 0.0), 0.0)),
            "field_areal_dominance": max(0.0, min(1.0, _to_float(item.get("field_areal_dominance", 0.0), 0.0))),
            "field_areal_fragmentation": max(0.0, min(1.0, _to_float(item.get("field_areal_fragmentation", 0.0), 0.0))),
            "field_areal_coherence_mean": max(0.0, _to_float(item.get("field_areal_coherence_mean", 0.0), 0.0)),
            "field_areal_conflict_mean": max(0.0, _to_float(item.get("field_areal_conflict_mean", 0.0), 0.0)),
            "field_areal_topology_density_mean": max(0.0, min(1.0, _to_float(item.get("field_areal_topology_density_mean", 0.0), 0.0))),
            "field_areal_topology_span_mean": max(0.0, _to_float(item.get("field_areal_topology_span_mean", 0.0), 0.0)),
            "field_areal_topology_boundary_mean": max(0.0, _to_float(item.get("field_areal_topology_boundary_mean", 0.0), 0.0)),
            "field_topology_state": normalize_json_state(item.get("field_topology_state", {}) or {}),
            "field_topology_layout_state": normalize_json_state(item.get("field_topology_layout_state", {}) or {}),
            "field_topology_rows": max(0, _to_int(item.get("field_topology_rows", 0), 0)),
            "field_topology_cols": max(0, _to_int(item.get("field_topology_cols", 0), 0)),
            "field_topology_position_count": max(0, _to_int(item.get("field_topology_position_count", 0), 0)),
            "field_topology_neighbor_link_count": max(0, _to_int(item.get("field_topology_neighbor_link_count", 0), 0)),
            "field_topology_neighbor_count_mean": max(0.0, _to_float(item.get("field_topology_neighbor_count_mean", 0.0), 0.0)),
            "field_topology_neighbor_count_max": max(0, _to_int(item.get("field_topology_neighbor_count_max", 0), 0)),
            "field_topology_cluster_link_count": max(0, _to_int(item.get("field_topology_cluster_link_count", 0), 0)),
            "field_topology_areal_link_count": max(0, _to_int(item.get("field_topology_areal_link_count", 0), 0)),
            "field_topology_link_density": max(0.0, min(1.0, _to_float(item.get("field_topology_link_density", 0.0), 0.0))),
            "field_topology_distance_mean": max(0.0, _to_float(item.get("field_topology_distance_mean", 0.0), 0.0)),
            "field_topology_coherence": max(0.0, min(1.0, _to_float(item.get("field_topology_coherence", 0.0), 0.0))),
            "field_topology_tension": max(0.0, min(1.0, _to_float(item.get("field_topology_tension", 0.0), 0.0))),
            "field_topology_state_label": _to_str(item.get("field_topology_state_label"), "sparse_topology"),
            "field_perception_state": normalize_json_state(item.get("field_perception_state", {}) or {}),
            "field_activity_island_count": max(0, _to_int(item.get("field_activity_island_count", 0), 0)),
            "field_activity_island_mass_mean": max(0.0, min(1.0, _to_float(item.get("field_activity_island_mass_mean", 0.0), 0.0))),
            "field_activity_island_mass_max": max(0.0, min(1.0, _to_float(item.get("field_activity_island_mass_max", 0.0), 0.0))),
            "field_activity_island_activation_mean": max(0.0, min(1.0, _to_float(item.get("field_activity_island_activation_mean", 0.0), 0.0))),
            "field_activity_island_pressure_mean": max(0.0, min(1.0, _to_float(item.get("field_activity_island_pressure_mean", 0.0), 0.0))),
            "field_activity_island_coherence_mean": max(0.0, min(1.0, _to_float(item.get("field_activity_island_coherence_mean", 0.0), 0.0))),
            "field_activity_island_context_reactivation_mean": max(0.0, min(1.0, _to_float(item.get("field_activity_island_context_reactivation_mean", 0.0), 0.0))),
            "field_activity_island_spread": max(0.0, min(1.0, _to_float(item.get("field_activity_island_spread", 0.0), 0.0))),
            "field_perception_focus": max(0.0, min(1.0, _to_float(item.get("field_perception_focus", 0.0), 0.0))),
            "field_perception_clarity": max(0.0, min(1.0, _to_float(item.get("field_perception_clarity", 0.0), 0.0))),
            "field_perception_stability": max(0.0, min(1.0, _to_float(item.get("field_perception_stability", 0.0), 0.0))),
            "field_perception_fragmentation": max(0.0, min(1.0, _to_float(item.get("field_perception_fragmentation", 0.0), 0.0))),
            "field_perception_strain": max(0.0, min(1.0, _to_float(item.get("field_perception_strain", 0.0), 0.0))),
            "dominant_activity_island_id": _to_str(item.get("dominant_activity_island_id"), "-"),
            "field_perception_label": _to_str(item.get("field_perception_label"), "quiet_field"),
            "field_activity_islands": normalize_json_state(item.get("field_activity_islands", []) or []),
            "neural_felt_state": normalize_json_state(item.get("neural_felt_state", {}) or {}),
            "neural_felt_bearing": max(0.0, min(1.0, _to_float(item.get("neural_felt_bearing", 0.0), 0.0))),
            "neural_felt_pressure": max(0.0, min(1.0, _to_float(item.get("neural_felt_pressure", 0.0), 0.0))),
            "neural_felt_memory_resonance": max(0.0, min(1.0, _to_float(item.get("neural_felt_memory_resonance", 0.0), 0.0))),
            "neural_felt_context_reactivation": max(0.0, min(1.0, _to_float(item.get("neural_felt_context_reactivation", 0.0), 0.0))),
            "neural_felt_label": _to_str(item.get("neural_felt_label"), "quiet_neural_felt"),
            "inner_field_history_state": normalize_json_state(item.get("inner_field_history_state", {}) or {}),
            "inner_field_history_length": max(0, _to_int(item.get("inner_field_history_length", 0), 0)),
            "inner_field_pressure_trend": max(-1.0, min(1.0, _to_float(item.get("inner_field_pressure_trend", 0.0), 0.0))),
            "inner_field_bearing_trend": max(-1.0, min(1.0, _to_float(item.get("inner_field_bearing_trend", 0.0), 0.0))),
            "inner_field_topology_tension_trend": max(-1.0, min(1.0, _to_float(item.get("inner_field_topology_tension_trend", 0.0), 0.0))),
            "inner_field_memory_resonance_trend": max(-1.0, min(1.0, _to_float(item.get("inner_field_memory_resonance_trend", 0.0), 0.0))),
            "inner_field_history_label": _to_str(item.get("inner_field_history_label"), "stable_field_trace"),
            "inner_pattern_support": max(0.0, min(1.0, _to_float(item.get("inner_pattern_support", 0.0), 0.0))),
            "inner_pattern_conflict": max(0.0, min(1.0, _to_float(item.get("inner_pattern_conflict", 0.0), 0.0))),
            "inner_pattern_fragility": max(0.0, min(1.0, _to_float(item.get("inner_pattern_fragility", 0.0), 0.0))),
            "inner_pattern_bearing": max(0.0, min(1.0, _to_float(item.get("inner_pattern_bearing", 0.0), 0.0))),
            "inner_pattern_state": _to_str(item.get("inner_pattern_state"), "bearing"),
            "pattern_support_score": max(0.0, min(1.0, _to_float(item.get("pattern_support_score", 0.0), 0.0))),
            "pattern_conflict_score": max(0.0, min(1.0, _to_float(item.get("pattern_conflict_score", 0.0), 0.0))),
            "pattern_fragility_score": max(0.0, min(1.0, _to_float(item.get("pattern_fragility_score", 0.0), 0.0))),
            "pattern_bearing_score": max(0.0, min(1.0, _to_float(item.get("pattern_bearing_score", 0.0), 0.0))),
            "pattern_reinforcement": max(0.0, min(1.0, _to_float(item.get("pattern_reinforcement", 0.0), 0.0))),
            "pattern_attenuation": max(0.0, min(1.0, _to_float(item.get("pattern_attenuation", 0.0), 0.0))),
            "experience_neurochemical_profile": normalize_json_state(item.get("experience_neurochemical_profile", {}) or {}),
            "neurochemical_support": max(0.0, min(1.0, _to_float(item.get("neurochemical_support", 0.0), 0.0))),
            "neurochemical_strain": max(0.0, min(1.0, _to_float(item.get("neurochemical_strain", 0.0), 0.0))),
            "avg_experience_effect_score": max(-0.28, min(0.28, _to_float(item.get("avg_experience_effect_score", 0.0), 0.0))),
            "avg_profit_reward": max(-1.0, min(1.0, _to_float(item.get("avg_profit_reward", 0.0), 0.0))),
            "avg_relief_signal": max(0.0, min(1.0, _to_float(item.get("avg_relief_signal", 0.0), 0.0))),
            "avg_stability_signal": max(0.0, min(1.0, _to_float(item.get("avg_stability_signal", 0.0), 0.0))),
            "avg_discipline_signal": max(0.0, min(1.0, _to_float(item.get("avg_discipline_signal", 0.0), 0.0))),
            "avg_confidence_signal": max(0.0, min(1.0, _to_float(item.get("avg_confidence_signal", 0.0), 0.0))),
            "avg_overactivation_signal": max(0.0, min(1.0, _to_float(item.get("avg_overactivation_signal", 0.0), 0.0))),
            "avg_chaos_penalty": max(0.0, min(1.0, _to_float(item.get("avg_chaos_penalty", 0.0), 0.0))),
            "avg_variance_penalty": max(0.0, min(1.0, _to_float(item.get("avg_variance_penalty", 0.0), 0.0))),
            "avg_overstrain_penalty": max(0.0, min(1.0, _to_float(item.get("avg_overstrain_penalty", 0.0), 0.0))),
            "avg_carrying_capacity_delta": max(-1.0, min(1.0, _to_float(item.get("avg_carrying_capacity_delta", 0.0), 0.0))),
            "avg_self_confidence_delta": max(-0.28, min(0.28, _to_float(item.get("avg_self_confidence_delta", 0.0), 0.0))),
            "avg_process_quality": max(0.0, min(1.0, _to_float(item.get("avg_process_quality", 0.0), 0.0))),
            "inner_pattern_label": _to_str(item.get("inner_pattern_label"), ""),
            "field_pattern_signature": normalize_json_state(item.get("field_pattern_signature", {}) or {}),
            "field_pattern_signature_key": _to_str(item.get("field_pattern_signature_key"), ""),
            "field_pattern_vector": _to_float_list(item.get("field_pattern_vector", [])),
            "inner_pattern_identity": _to_str(item.get("inner_pattern_identity"), ""),
            "inner_pattern_identity_label": _to_str(item.get("inner_pattern_identity_label"), ""),
            "inner_pattern_identity_confidence": max(0.0, min(1.0, _to_float(item.get("inner_pattern_identity_confidence", 0.0), 0.0))),
            "inner_pattern_identity_streak": max(0, _to_int(item.get("inner_pattern_identity_streak", 0), 0)),
            "inner_pattern_identity_stability": max(0.0, min(1.0, _to_float(item.get("inner_pattern_identity_stability", 0.0), 0.0))),
            "inner_pattern_identity_recurrent": bool(item.get("inner_pattern_identity_recurrent", False)),
            "inner_pattern_identity_changed": bool(item.get("inner_pattern_identity_changed", False)),
            "inner_pattern_identity_last_seen_tick": max(0, _to_int(item.get("inner_pattern_identity_last_seen_tick", 0), 0)),
            "inner_pattern_recognition_state": normalize_json_state(item.get("inner_pattern_recognition_state", {}) or {}),
            "inner_pattern_recognition_label": _to_str(item.get("inner_pattern_recognition_label"), "unsettled_inner_pattern"),
            "inner_pattern_recognition_strength": max(0.0, min(1.0, _to_float(item.get("inner_pattern_recognition_strength", 0.0), 0.0))),
            "inner_pattern_recognition_recurrent": bool(item.get("inner_pattern_recognition_recurrent", False)),
            "inner_pattern_recognition_changed": bool(item.get("inner_pattern_recognition_changed", False)),
            "inner_self_state": _to_str(item.get("inner_self_state"), "stable"),
            "inner_attractor": _to_str(item.get("inner_attractor"), "neutral"),
        }

    return normalized
# --------------------------------------------------
# NORMALIZE MCM MEMORY
# --------------------------------------------------
def normalize_mcm_memory(memory_items) -> list[dict]:

    normalized = []

    for item in list(memory_items or []):
        if not isinstance(item, dict):
            continue

        normalized.append(
            {
                "center": _to_float(item.get("center", 0.0), 0.0),
                "strength": max(1, _to_int(item.get("strength", 1), 1)),
            }
        )

    normalized = sorted(
        normalized,
        key=lambda item: max(1, _to_int(item.get("strength", 1), 1)),
        reverse=True,
    )[:24]

    return normalized
# --------------------------------------------------
# BUILD STATE
# --------------------------------------------------
def build_memory_state(bot, include_runtime_state: bool = True) -> dict:

    profile_start = time.perf_counter() if bool(getattr(Config, "MCM_RUNTIME_PROFILE_DEBUG", False)) else 0.0

    if bot is None:
        return {
            "signature_memory": {},
            "context_clusters": {},
            "context_cluster_seq": 0,
            "last_signature_key": None,
            "last_signature_outcome": None,
            "last_signature_context": None,
            "last_context_cluster_id": None,
            "last_context_cluster_key": None,
            "inner_context_clusters": {},
            "inner_context_cluster_seq": 0,
            "last_inner_context_cluster_id": None,
            "last_inner_context_cluster_key": None,
            "last_inner_pattern_identity": None,
            "inner_pattern_identity_streak": 0,
            "inner_pattern_identity_last_seen_tick": 0,
            "inner_pattern_identity_stability": 0.0,
            "inner_field_history_state": {},
            "inner_field_history": [],
            "mcm_runtime_snapshot": {},
            "mcm_runtime_decision_state": {},
            "mcm_runtime_brain_snapshot": {},
            "mcm_runtime_market_ticks": 0,
            "mcm_decision_episode": {},
            "mcm_experience_space": {},
            "entry_contact_preference_memory": {},
            "mcm_last_observe_timestamp": None,
            "mcm_memory": [],
            "mcm_last_attractor": None,
            "mcm_last_action": None,
        }

    mcm_memory = []
    mcm_brain = getattr(bot, "mcm_brain", None)

    if isinstance(mcm_brain, dict):
        memory_obj = mcm_brain.get("memory")
        memory_items = getattr(memory_obj, "memory", None)
        mcm_memory = normalize_mcm_memory(memory_items)

    payload = {
        "signature_memory": normalize_signature_memory(getattr(bot, "signature_memory", {})),
        "context_clusters": normalize_context_clusters(getattr(bot, "context_clusters", {})),
        "context_cluster_seq": max(0, _to_int(getattr(bot, "context_cluster_seq", 0), 0)),
        "last_signature_key": _to_str(getattr(bot, "last_signature_key", None), None),
        "last_signature_outcome": _to_str(getattr(bot, "last_signature_outcome", None), None),
        "last_signature_context": normalize_json_state(getattr(bot, "last_signature_context", None)),
        "last_context_cluster_id": _to_str(getattr(bot, "last_context_cluster_id", None), None),
        "last_context_cluster_key": _to_str(getattr(bot, "last_context_cluster_key", None), None),
        "inner_context_clusters": normalize_inner_context_clusters(getattr(bot, "inner_context_clusters", {})),
        "inner_context_cluster_seq": max(0, _to_int(getattr(bot, "inner_context_cluster_seq", 0), 0)),
        "last_inner_context_cluster_id": _to_str(getattr(bot, "last_inner_context_cluster_id", None), None),
        "last_inner_context_cluster_key": _to_str(getattr(bot, "last_inner_context_cluster_key", None), None),
        "last_inner_pattern_identity": _to_str(getattr(bot, "last_inner_pattern_identity", None), None),
        "inner_pattern_identity_streak": max(0, _to_int(getattr(bot, "inner_pattern_identity_streak", 0), 0)),
        "inner_pattern_identity_last_seen_tick": max(0, _to_int(getattr(bot, "inner_pattern_identity_last_seen_tick", 0), 0)),
        "inner_pattern_identity_stability": max(0.0, min(1.0, _to_float(getattr(bot, "inner_pattern_identity_stability", 0.0), 0.0))),
        "inner_field_history_state": normalize_inner_field_history_state(getattr(bot, "inner_field_history_state", {})),
        "inner_field_history": list(normalize_inner_field_history_state(getattr(bot, "inner_field_history_state", {})).get("inner_field_history", []) or []),
        "focus_point": _to_float(getattr(bot, "focus_point", 0.0), 0.0),
        "focus_confidence": _to_float(getattr(bot, "focus_confidence", 0.0), 0.0),
        "target_lock": _to_float(getattr(bot, "target_lock", 0.0), 0.0),
        "target_drift": _to_float(getattr(bot, "target_drift", 0.0), 0.0),
        "entry_expectation": _to_float(getattr(bot, "entry_expectation", 0.0), 0.0),
        "target_expectation": _to_float(getattr(bot, "target_expectation", 0.0), 0.0),
        "approach_pressure": _to_float(getattr(bot, "approach_pressure", 0.0), 0.0),
        "pressure_release": _to_float(getattr(bot, "pressure_release", 0.0), 0.0),
        "experience_regulation": _to_float(getattr(bot, "experience_regulation", 0.0), 0.0),
        "reflection_maturity": _to_float(getattr(bot, "reflection_maturity", 0.0), 0.0),
        "load_bearing_capacity": _to_float(getattr(bot, "load_bearing_capacity", 0.0), 0.0),
        "protective_width_regulation": _to_float(getattr(bot, "protective_width_regulation", 0.0), 0.0),
        "protective_courage": _to_float(getattr(bot, "protective_courage", 0.0), 0.0),
        "inhibition_level": _to_float(getattr(bot, "inhibition_level", 0.0), 0.0),
        "habituation_level": _to_float(getattr(bot, "habituation_level", 0.0), 0.0),
        "competition_bias": _to_float(getattr(bot, "competition_bias", 0.0), 0.0),
        "observation_mode": bool(getattr(bot, "observation_mode", False)),
        "last_signal_relevance": _to_float(getattr(bot, "last_signal_relevance", 0.0), 0.0),
        "structure_perception_state": normalize_json_state(getattr(bot, "structure_perception_state", {})),
        "perception_state": normalize_json_state(getattr(bot, "perception_state", {})),
        "outer_visual_perception_state": normalize_json_state(getattr(bot, "outer_visual_perception_state", {})),
        "inner_field_perception_state": normalize_json_state(getattr(bot, "inner_field_perception_state", {})),
        "processing_state": normalize_json_state(getattr(bot, "processing_state", {})),
        "expectation_state": normalize_json_state(getattr(bot, "expectation_state", {})),
        "felt_state": normalize_json_state(getattr(bot, "felt_state", {})),
        "thought_state": normalize_json_state(getattr(bot, "thought_state", {})),
        "meta_regulation_state": normalize_json_state(getattr(bot, "meta_regulation_state", {})),
        "last_outcome_decomposition": normalize_json_state(getattr(bot, "last_outcome_decomposition", {})),
        "entry_contact_preference_memory": normalize_json_state(getattr(bot, "entry_contact_preference_memory", {})),
        "mcm_memory": mcm_memory,
        "mcm_last_attractor": _to_str(getattr(bot, "mcm_last_attractor", None), None),
        "mcm_last_action": _to_str(getattr(bot, "mcm_last_action", None), None),
        "field_density": _to_float(getattr(bot, "field_density", 0.0), 0.0),
        "field_stability": _to_float(getattr(bot, "field_stability", 0.0), 0.0),
        "regulatory_load": _to_float(getattr(bot, "regulatory_load", 0.0), 0.0),
        "action_capacity": _to_float(getattr(bot, "action_capacity", 0.0), 0.0),
        "recovery_need": _to_float(getattr(bot, "recovery_need", 0.0), 0.0),
        "survival_pressure": _to_float(getattr(bot, "survival_pressure", 0.0), 0.0),
    }

    if bool(include_runtime_state):
        payload.update({
            "mcm_runtime_snapshot": normalize_json_state(getattr(bot, "mcm_runtime_snapshot", {})),
            "mcm_runtime_decision_state": normalize_json_state(getattr(bot, "mcm_runtime_decision_state", {})),
            "mcm_runtime_brain_snapshot": normalize_json_state(getattr(bot, "mcm_runtime_brain_snapshot", {})),
            "mcm_runtime_market_ticks": max(0, _to_int(getattr(bot, "mcm_runtime_market_ticks", 0), 0)),
            "mcm_decision_episode": normalize_json_state(getattr(bot, "mcm_decision_episode", {})),
            "mcm_decision_episode_internal": normalize_json_state(getattr(bot, "mcm_decision_episode_internal", {})),
            "mcm_experience_space": normalize_json_state(getattr(bot, "mcm_experience_space", {})),
            "mcm_last_observe_timestamp": getattr(bot, "mcm_last_observe_timestamp", None),
        })

    if profile_start:
        dbr_profile(
            "memory_state.build_memory_state",
            (time.perf_counter() - profile_start) * 1000.0,
            extra=f"keys={int(len(payload or {}))}|include_runtime_state={bool(include_runtime_state)}",
        )

    return payload
# --------------------------------------------------
# APPLY STATE
# --------------------------------------------------
def apply_memory_state(bot, state: dict | None) -> dict:

    payload = dict(state or {})

    if bot is None:
        return payload

    bot.signature_memory = normalize_signature_memory(payload.get("signature_memory", {}))
    bot.context_clusters = normalize_context_clusters(payload.get("context_clusters", {}))
    bot.context_cluster_seq = max(0, _to_int(payload.get("context_cluster_seq", 0), 0))
    bot.inner_context_clusters = normalize_inner_context_clusters(payload.get("inner_context_clusters", {}))
    bot.inner_context_cluster_seq = max(0, _to_int(payload.get("inner_context_cluster_seq", 0), 0))

    bot.last_signature_key = _to_str(payload.get("last_signature_key"), None)
    bot.last_signature_outcome = _to_str(payload.get("last_signature_outcome"), None)
    bot.last_signature_context = normalize_json_state(payload.get("last_signature_context"))
    bot.last_context_cluster_id = _to_str(payload.get("last_context_cluster_id"), None)
    bot.last_context_cluster_key = _to_str(payload.get("last_context_cluster_key"), None)
    bot.last_inner_context_cluster_id = _to_str(payload.get("last_inner_context_cluster_id"), None)
    bot.last_inner_context_cluster_key = _to_str(payload.get("last_inner_context_cluster_key"), None)
    bot.last_inner_pattern_identity = _to_str(payload.get("last_inner_pattern_identity"), None)
    bot.inner_pattern_identity_streak = max(0, _to_int(payload.get("inner_pattern_identity_streak", 0), 0))
    bot.inner_pattern_identity_last_seen_tick = max(0, _to_int(payload.get("inner_pattern_identity_last_seen_tick", 0), 0))
    bot.inner_pattern_identity_stability = max(0.0, min(1.0, _to_float(payload.get("inner_pattern_identity_stability", 0.0), 0.0)))
    inner_field_history_state = normalize_inner_field_history_state(
        payload.get(
            "inner_field_history_state",
            {"inner_field_history": payload.get("inner_field_history", [])},
        )
    )
    bot.inner_field_history_state = dict(inner_field_history_state or {})
    bot.inner_field_history = list(inner_field_history_state.get("inner_field_history", []) or [])
    bot.focus_point = _to_float(payload.get("focus_point", 0.0), 0.0)
    bot.focus_confidence = _to_float(payload.get("focus_confidence", 0.0), 0.0)
    bot.target_lock = _to_float(payload.get("target_lock", 0.0), 0.0)
    bot.target_drift = _to_float(payload.get("target_drift", 0.0), 0.0)
    bot.entry_expectation = _to_float(payload.get("entry_expectation", 0.0), 0.0)
    bot.target_expectation = _to_float(payload.get("target_expectation", 0.0), 0.0)
    bot.approach_pressure = _to_float(payload.get("approach_pressure", 0.0), 0.0)
    bot.pressure_release = _to_float(payload.get("pressure_release", 0.0), 0.0)
    bot.experience_regulation = _to_float(payload.get("experience_regulation", 0.0), 0.0)
    bot.reflection_maturity = _to_float(payload.get("reflection_maturity", 0.0), 0.0)
    bot.load_bearing_capacity = _to_float(payload.get("load_bearing_capacity", 0.0), 0.0)
    bot.protective_width_regulation = _to_float(payload.get("protective_width_regulation", 0.0), 0.0)
    bot.protective_courage = _to_float(payload.get("protective_courage", 0.0), 0.0)
    bot.inhibition_level = _to_float(payload.get("inhibition_level", 0.0), 0.0)
    bot.habituation_level = _to_float(payload.get("habituation_level", 0.0), 0.0)
    bot.competition_bias = _to_float(payload.get("competition_bias", 0.0), 0.0)
    bot.observation_mode = bool(payload.get("observation_mode", False))
    bot.last_signal_relevance = _to_float(payload.get("last_signal_relevance", 0.0), 0.0)
    bot.structure_perception_state = normalize_json_state(payload.get("structure_perception_state", {}))
    bot.perception_state = normalize_json_state(payload.get("perception_state", {}))
    bot.outer_visual_perception_state = normalize_json_state(payload.get("outer_visual_perception_state", {}))
    bot.inner_field_perception_state = normalize_json_state(payload.get("inner_field_perception_state", {}))
    bot.processing_state = normalize_json_state(payload.get("processing_state", {}))
    bot.expectation_state = normalize_json_state(payload.get("expectation_state", {}))
    bot.felt_state = normalize_json_state(payload.get("felt_state", {}))
    bot.thought_state = normalize_json_state(payload.get("thought_state", {}))
    bot.meta_regulation_state = normalize_json_state(payload.get("meta_regulation_state", {}))
    bot.last_outcome_decomposition = normalize_json_state(payload.get("last_outcome_decomposition", {}))
    bot.entry_contact_preference_memory = normalize_json_state(payload.get("entry_contact_preference_memory", {}))
    bot.mcm_runtime_snapshot = normalize_json_state(payload.get("mcm_runtime_snapshot", {}))
    bot.mcm_runtime_decision_state = normalize_json_state(payload.get("mcm_runtime_decision_state", {}))
    bot.mcm_runtime_brain_snapshot = normalize_json_state(payload.get("mcm_runtime_brain_snapshot", {}))
    bot.mcm_runtime_market_ticks = max(0, _to_int(payload.get("mcm_runtime_market_ticks", 0), 0))
    bot.mcm_decision_episode = normalize_json_state(payload.get("mcm_decision_episode", {}))
    bot.mcm_decision_episode_internal = normalize_json_state(payload.get("mcm_decision_episode_internal", {}))
    bot.mcm_experience_space = normalize_json_state(payload.get("mcm_experience_space", {}))
    bot.mcm_last_observe_timestamp = payload.get("mcm_last_observe_timestamp", None)
    bot.mcm_last_attractor = _to_str(payload.get("mcm_last_attractor"), None)
    bot.mcm_last_action = _to_str(payload.get("mcm_last_action"), None)
    bot.field_density = _to_float(payload.get("field_density", 0.0), 0.0)
    bot.field_stability = _to_float(payload.get("field_stability", 0.0), 0.0)
    bot.regulatory_load = _to_float(payload.get("regulatory_load", 0.0), 0.0)
    bot.action_capacity = _to_float(payload.get("action_capacity", 0.0), 0.0)
    bot.recovery_need = _to_float(payload.get("recovery_need", 0.0), 0.0)
    bot.survival_pressure = _to_float(payload.get("survival_pressure", 0.0), 0.0)

    mcm_brain = getattr(bot, "mcm_brain", None)
    if isinstance(mcm_brain, dict):
        memory_obj = mcm_brain.get("memory")
        if memory_obj is not None and hasattr(memory_obj, "memory"):
            memory_obj.memory = normalize_mcm_memory(payload.get("mcm_memory", []))

    return build_memory_state(bot)
# --------------------------------------------------
# READ
# --------------------------------------------------
def read_memory_state(path: str | None = None) -> dict:

    filepath = _memory_state_path(path)

    default_state = {
        "signature_memory": {},
        "context_clusters": {},
        "context_cluster_seq": 0,
        "last_signature_key": None,
        "last_signature_outcome": None,
        "last_signature_context": None,
        "last_context_cluster_id": None,
        "last_context_cluster_key": None,
        "inner_context_clusters": {},
        "inner_context_cluster_seq": 0,
        "last_inner_context_cluster_id": None,
        "last_inner_context_cluster_key": None,
        "last_inner_pattern_identity": None,
        "inner_pattern_identity_streak": 0,
        "inner_pattern_identity_last_seen_tick": 0,
        "inner_pattern_identity_stability": 0.0,
        "inner_field_history_state": {},
        "inner_field_history": [],
        "focus_point": 0.0,
        "focus_confidence": 0.0,
        "target_lock": 0.0,
        "target_drift": 0.0,
        "entry_expectation": 0.0,
        "target_expectation": 0.0,
        "approach_pressure": 0.0,
        "pressure_release": 0.0,
        "experience_regulation": 0.0,
        "reflection_maturity": 0.0,
        "load_bearing_capacity": 0.0,
        "protective_width_regulation": 0.0,
        "protective_courage": 0.0,
        "inhibition_level": 0.0,
        "habituation_level": 0.0,
        "competition_bias": 0.0,
        "observation_mode": False,
        "last_signal_relevance": 0.0,
        "structure_perception_state": {},
        "perception_state": {},
        "outer_visual_perception_state": {},
        "inner_field_perception_state": {},
        "processing_state": {},
        "expectation_state": {},
        "felt_state": {},
        "thought_state": {},
        "meta_regulation_state": {},
        "last_outcome_decomposition": {},
        "entry_contact_preference_memory": {},
        "mcm_runtime_snapshot": {},
        "mcm_runtime_decision_state": {},
        "mcm_runtime_brain_snapshot": {},
        "mcm_runtime_market_ticks": 0,
        "mcm_decision_episode": {},
        "mcm_decision_episode_internal": {},
        "mcm_experience_space": {},
        "mcm_last_observe_timestamp": None,
        "mcm_memory": [],
        "mcm_last_attractor": None,
        "mcm_last_action": None,
        "field_density": 0.0,
        "field_stability": 0.0,
        "regulatory_load": 0.0,
        "action_capacity": 0.0,
        "recovery_need": 0.0,
        "survival_pressure": 0.0,
    }

    if not os.path.exists(filepath):
        return dict(default_state)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return dict(default_state)

    return {
        "signature_memory": normalize_signature_memory((raw or {}).get("signature_memory", {})),
        "context_clusters": normalize_context_clusters((raw or {}).get("context_clusters", {})),
        "context_cluster_seq": max(0, _to_int((raw or {}).get("context_cluster_seq", 0), 0)),
        "last_signature_key": _to_str((raw or {}).get("last_signature_key"), None),
        "last_signature_outcome": _to_str((raw or {}).get("last_signature_outcome"), None),
        "last_signature_context": normalize_json_state((raw or {}).get("last_signature_context")),
        "last_context_cluster_id": _to_str((raw or {}).get("last_context_cluster_id"), None),
        "last_context_cluster_key": _to_str((raw or {}).get("last_context_cluster_key"), None),
        "inner_context_clusters": normalize_inner_context_clusters((raw or {}).get("inner_context_clusters", {})),
        "inner_context_cluster_seq": max(0, _to_int((raw or {}).get("inner_context_cluster_seq", 0), 0)),
        "last_inner_context_cluster_id": _to_str((raw or {}).get("last_inner_context_cluster_id"), None),
        "last_inner_context_cluster_key": _to_str((raw or {}).get("last_inner_context_cluster_key"), None),
        "last_inner_pattern_identity": _to_str((raw or {}).get("last_inner_pattern_identity"), None),
        "inner_pattern_identity_streak": max(0, _to_int((raw or {}).get("inner_pattern_identity_streak", 0), 0)),
        "inner_pattern_identity_last_seen_tick": max(0, _to_int((raw or {}).get("inner_pattern_identity_last_seen_tick", 0), 0)),
        "inner_pattern_identity_stability": max(0.0, min(1.0, _to_float((raw or {}).get("inner_pattern_identity_stability", 0.0), 0.0))),
        "inner_field_history_state": normalize_inner_field_history_state(
            (raw or {}).get(
                "inner_field_history_state",
                {"inner_field_history": (raw or {}).get("inner_field_history", [])},
            )
        ),
        "inner_field_history": list(
            normalize_inner_field_history_state(
                (raw or {}).get(
                    "inner_field_history_state",
                    {"inner_field_history": (raw or {}).get("inner_field_history", [])},
                )
            ).get("inner_field_history", []) or []
        ),
        "focus_point": _to_float((raw or {}).get("focus_point", 0.0), 0.0),
        "focus_confidence": _to_float((raw or {}).get("focus_confidence", 0.0), 0.0),
        "target_lock": _to_float((raw or {}).get("target_lock", 0.0), 0.0),
        "target_drift": _to_float((raw or {}).get("target_drift", 0.0), 0.0),
        "entry_expectation": _to_float((raw or {}).get("entry_expectation", 0.0), 0.0),
        "target_expectation": _to_float((raw or {}).get("target_expectation", 0.0), 0.0),
        "approach_pressure": _to_float((raw or {}).get("approach_pressure", 0.0), 0.0),
        "pressure_release": _to_float((raw or {}).get("pressure_release", 0.0), 0.0),
        "experience_regulation": _to_float((raw or {}).get("experience_regulation", 0.0), 0.0),
        "reflection_maturity": _to_float((raw or {}).get("reflection_maturity", 0.0), 0.0),
        "load_bearing_capacity": _to_float((raw or {}).get("load_bearing_capacity", 0.0), 0.0),
        "protective_width_regulation": _to_float((raw or {}).get("protective_width_regulation", 0.0), 0.0),
        "protective_courage": _to_float((raw or {}).get("protective_courage", 0.0), 0.0),
        "inhibition_level": _to_float((raw or {}).get("inhibition_level", 0.0), 0.0),
        "habituation_level": _to_float((raw or {}).get("habituation_level", 0.0), 0.0),
        "competition_bias": _to_float((raw or {}).get("competition_bias", 0.0), 0.0),
        "observation_mode": bool((raw or {}).get("observation_mode", False)),
        "last_signal_relevance": _to_float((raw or {}).get("last_signal_relevance", 0.0), 0.0),
        "structure_perception_state": normalize_json_state((raw or {}).get("structure_perception_state", {})),
        "perception_state": normalize_json_state((raw or {}).get("perception_state", {})),
        "outer_visual_perception_state": normalize_json_state((raw or {}).get("outer_visual_perception_state", {})),
        "inner_field_perception_state": normalize_json_state((raw or {}).get("inner_field_perception_state", {})),
        "processing_state": normalize_json_state((raw or {}).get("processing_state", {})),
        "expectation_state": normalize_json_state((raw or {}).get("expectation_state", {})),
        "felt_state": normalize_json_state((raw or {}).get("felt_state", {})),
        "thought_state": normalize_json_state((raw or {}).get("thought_state", {})),
        "meta_regulation_state": normalize_json_state((raw or {}).get("meta_regulation_state", {})),
        "last_outcome_decomposition": normalize_json_state((raw or {}).get("last_outcome_decomposition", {})),
        "entry_contact_preference_memory": normalize_json_state((raw or {}).get("entry_contact_preference_memory", {})),
        "mcm_runtime_snapshot": normalize_json_state((raw or {}).get("mcm_runtime_snapshot", {})),
        "mcm_runtime_decision_state": normalize_json_state((raw or {}).get("mcm_runtime_decision_state", {})),
        "mcm_runtime_brain_snapshot": normalize_json_state((raw or {}).get("mcm_runtime_brain_snapshot", {})),
        "mcm_runtime_market_ticks": max(0, _to_int((raw or {}).get("mcm_runtime_market_ticks", 0), 0)),
        "mcm_decision_episode": normalize_json_state((raw or {}).get("mcm_decision_episode", {})),
        "mcm_decision_episode_internal": normalize_json_state((raw or {}).get("mcm_decision_episode_internal", {})),
        "mcm_experience_space": normalize_json_state((raw or {}).get("mcm_experience_space", {})),
        "mcm_last_observe_timestamp": (raw or {}).get("mcm_last_observe_timestamp", None),
        "mcm_memory": normalize_mcm_memory((raw or {}).get("mcm_memory", [])),
        "mcm_last_attractor": _to_str((raw or {}).get("mcm_last_attractor"), None),
        "mcm_last_action": _to_str((raw or {}).get("mcm_last_action"), None),
        "field_density": _to_float((raw or {}).get("field_density", 0.0), 0.0),
        "field_stability": _to_float((raw or {}).get("field_stability", 0.0), 0.0),
        "regulatory_load": _to_float((raw or {}).get("regulatory_load", 0.0), 0.0),
        "action_capacity": _to_float((raw or {}).get("action_capacity", 0.0), 0.0),
        "recovery_need": _to_float((raw or {}).get("recovery_need", 0.0), 0.0),
        "survival_pressure": _to_float((raw or {}).get("survival_pressure", 0.0), 0.0),
    }
# --------------------------------------------------
# LOAD
# --------------------------------------------------
def load_memory_state(bot, path: str | None = None) -> dict:

    state = read_memory_state(path)
    return apply_memory_state(bot, state)
# --------------------------------------------------
# SAVE
# --------------------------------------------------
def save_memory_state(bot, path: str | None = None, include_runtime_state: bool | None = None) -> dict | None:

    payload = capture_memory_state(
        bot,
        include_runtime_state=include_runtime_state,
    )

    if payload is None:
        return None

    return write_memory_state_payload(
        payload,
        path=path,
    )
# --------------------------------------------------
# BOT SAVE WRAPPER
# --------------------------------------------------
def save_bot_memory_state(
    bot,
    *,
    force: bool = False,
    form_symbol_flusher=None,
    thought_memory_flusher=None,
) -> dict | None:

    if bot is None:
        return None

    if not bool(force) and not bool(getattr(bot, "_memory_state_dirty", False)):
        return None

    if form_symbol_flusher is not None:
        form_symbol_flusher(bot, force=bool(force))

    if thought_memory_flusher is not None:
        thought_memory_flusher(bot, force=bool(force))

    payload = capture_memory_state(
        bot,
        include_runtime_state=bool(getattr(Config, "MCM_SAVE_RUNTIME_STATE", False)),
    )

    if payload is None:
        return None

    saved_payload = write_memory_state_payload(payload)

    if saved_payload is None:
        return None

    return finalize_memory_state_save(
        bot,
        payload=saved_payload,
    )
# --------------------------------------------------
# CAPTURE
# --------------------------------------------------
def capture_memory_state(bot, include_runtime_state: bool | None = None) -> dict | None:

    if bot is None:
        return None

    if include_runtime_state is None:
        include_runtime_state = bool(getattr(Config, "MCM_SAVE_RUNTIME_STATE", True))

    return build_memory_state(
        bot,
        include_runtime_state=bool(include_runtime_state),
    )
# --------------------------------------------------
# WRITE
# --------------------------------------------------
def write_memory_state_payload(payload: dict | None, path: str | None = None) -> dict | None:

    if not isinstance(payload, dict):
        return None

    filepath = _memory_state_path(path)
    tmp_filepath = f"{filepath}.tmp"
    profile_start = time.perf_counter() if bool(getattr(Config, "MCM_RUNTIME_PROFILE_DEBUG", False)) else 0.0

    try:
        _ensure_dir(filepath)
        write_start = time.perf_counter()
        with open(tmp_filepath, "w", encoding="utf-8") as f:
            json.dump(dict(payload or {}), f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_filepath, filepath)
        elapsed_ms = (time.perf_counter() - write_start) * 1000.0
        try:
            bytes_written = int(os.path.getsize(filepath))
        except Exception:
            bytes_written = 0
        dbr_file_write_profile(
            filepath,
            elapsed_ms,
            bytes_written=bytes_written,
            operation="memory_state_json_dump_atomic",
            extra=f"keys={int(len(payload or {}))}",
        )
    except Exception:
        try:
            if os.path.exists(tmp_filepath):
                os.remove(tmp_filepath)
        except Exception:
            pass
        return None

    if profile_start:
        dbr_profile(
            "memory_state.write_payload",
            (time.perf_counter() - profile_start) * 1000.0,
            extra=f"path={filepath}|keys={int(len(payload or {}))}",
        )

    return dict(payload or {})
# --------------------------------------------------
# ENSURE LOADED
# --------------------------------------------------
def ensure_memory_state_loaded(bot, payload: dict | None = None) -> bool:

    if bot is None:
        return False

    if bool(getattr(bot, "_memory_state_mcm_loaded", False)):
        return True

    if not isinstance(getattr(bot, "mcm_brain", None), dict):
        return False

    memory_payload = dict(payload or getattr(bot, "_memory_state_payload", {}) or {})

    apply_memory_state(bot, memory_payload)

    runtime = getattr(bot, "mcm_runtime", None)
    if runtime is not None:
        runtime.restore_from_bot()

    bot._memory_state_payload = dict(memory_payload or {})
    bot._memory_state_mcm_loaded = True
    return True












