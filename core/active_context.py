"""Active-context trace mechanics.

This module carries DIO's active-context replay, decay, temporal/context
selection, and nervous modulation logic. It preserves the formulas from the
Brain module and does not own runtime commit behavior.
"""

from __future__ import annotations

from config import Config
from core.mcm_field import _extract_neurochemical_profile, _normalize_active_context_trace


def _resolve_active_context_replay_impulse(trace):

    item = _normalize_active_context_trace(trace)
    if not item:
        return 0.0

    activation = float(item.get("activation", 0.0) or 0.0)
    support_pressure = (
        float(item.get("support", 0.0) or 0.0)
        + float(item.get("bearing", 0.0) or 0.0)
        + float(item.get("reinforcement", 0.0) or 0.0)
    )
    regulation_pressure = (
        float(item.get("conflict", 0.0) or 0.0)
        + float(item.get("fragility", 0.0) or 0.0)
        + float(item.get("attenuation", 0.0) or 0.0)
    )
    neuro_support = (
        max(0.0, float(item.get("experience_effect_score", 0.0) or 0.0)) * 2.0
        + float(item.get("confidence_signal", 0.0) or 0.0)
        + float(item.get("stability_signal", 0.0) or 0.0)
        + float(item.get("discipline_signal", 0.0) or 0.0)
        + max(0.0, float(item.get("carrying_capacity_delta", 0.0) or 0.0))
    )
    neuro_strain = (
        max(0.0, -float(item.get("experience_effect_score", 0.0) or 0.0)) * 2.0
        + float(item.get("chaos_penalty", 0.0) or 0.0)
        + float(item.get("variance_penalty", 0.0) or 0.0)
        + float(item.get("overactivation_signal", 0.0) or 0.0)
        + float(item.get("overstrain_penalty", 0.0) or 0.0)
    )
    support_pressure += max(0.0, min(1.0, neuro_support / 4.0)) * 0.18
    regulation_pressure += max(0.0, min(1.0, neuro_strain / 4.0)) * 0.22
    context_balance = max(-1.0, min(1.0, (support_pressure - regulation_pressure) / 3.0))
    replay_weight = max(0.0, min(0.18, float(getattr(Config, "MCM_ACTIVE_CONTEXT_REPLAY_WEIGHT", 0.06) or 0.06)))
    replay_weight = max(
        0.0,
        min(
            0.18,
            replay_weight
            * (1.0 + (max(0.0, min(1.0, neuro_support / 4.0)) * 0.08))
            * (1.0 - (max(0.0, min(1.0, neuro_strain / 4.0)) * 0.12)),
        ),
    )

    return float(max(-0.12, min(0.12, activation * context_balance * replay_weight)))


def _resolve_context_modulation_source(bot=None, runtime_result=None):

    runtime = dict(runtime_result or {})
    meta = dict(runtime.get("meta_regulation_state", {}) or {})

    if not meta and bot is not None:
        try:
            meta = dict(getattr(bot, "mcm_runtime_decision_state", {}).get("entry_result", {}).get("meta_regulation_state", {}) or {})
        except Exception:
            meta = {}

    if not meta and bot is not None:
        try:
            meta = dict(getattr(bot, "mcm_runtime_brain_snapshot", {}).get("meta_regulation_state", {}) or {})
        except Exception:
            meta = {}

    return dict(meta or {})


def _apply_nervous_context_modulation(trace, bot=None, runtime_result=None):

    item = _normalize_active_context_trace(trace)
    if not item:
        return {}

    meta = _resolve_context_modulation_source(bot=bot, runtime_result=runtime_result)

    def _read(key, default=0.0):
        try:
            return float(meta.get(key, item.get(key, default)) or default)
        except Exception:
            return float(default)

    nervous_context_overcoupling = max(0.0, min(1.0, _read("nervous_context_overcoupling", 0.0)))
    nervous_reflection_need = max(0.0, min(1.0, _read("nervous_overload_reflection_need", 0.0)))
    shock_response_risk = max(0.0, min(1.0, _read("shock_response_risk", 0.0)))

    context_self_certainty = max(
        0.0,
        min(
            1.0,
            float(item.get("activation", 0.0) or 0.0)
            * ((float(item.get("support", 0.0) or 0.0) + float(item.get("bearing", 0.0) or 0.0)) * 0.5)
            * max(0.0, 1.0 - float(item.get("conflict", 0.0) or 0.0)),
        ),
    )
    modulation = max(
        0.0,
        min(
            1.0,
            (nervous_context_overcoupling * 0.62)
            + (nervous_reflection_need * 0.22)
            + (shock_response_risk * 0.12),
        ),
    )

    if modulation <= 0.001:
        item["active_context_self_certainty"] = float(context_self_certainty)
        item["nervous_context_overcoupling"] = float(nervous_context_overcoupling)
        item["context_modulation_label"] = "unmodulated_context"
        return _normalize_active_context_trace(item)

    item["activation"] = max(0.0, min(1.0, float(item.get("activation", 0.0) or 0.0) - (modulation * 0.018)))
    item["support"] = max(0.0, min(1.0, float(item.get("support", 0.0) or 0.0) * (1.0 - modulation * 0.075)))
    item["bearing"] = max(0.0, min(1.0, float(item.get("bearing", 0.0) or 0.0) * (1.0 - modulation * 0.065)))
    item["action_support"] = max(0.0, min(1.0, float(item.get("action_support", 0.0) or 0.0) * (1.0 - modulation * 0.070)))
    item["conflict"] = max(0.0, min(1.0, float(item.get("conflict", 0.0) or 0.0) + (modulation * 0.080)))
    item["fragility"] = max(0.0, min(1.0, float(item.get("fragility", 0.0) or 0.0) + (modulation * 0.075)))
    item["attenuation"] = max(0.0, min(1.0, float(item.get("attenuation", 0.0) or 0.0) + (modulation * 0.090)))
    item["observe_pressure"] = max(0.0, min(1.0, float(item.get("observe_pressure", 0.0) or 0.0) + (modulation * 0.050)))
    item["replan_pressure"] = max(0.0, min(1.0, float(item.get("replan_pressure", 0.0) or 0.0) + (modulation * 0.035)))
    item["overtrust_pressure"] = max(0.0, min(1.0, float(item.get("overtrust_pressure", 0.0) or 0.0) + (modulation * 0.100)))
    item["active_context_self_certainty"] = float(context_self_certainty)
    item["nervous_context_overcoupling"] = float(nervous_context_overcoupling)
    item["context_modulation_label"] = "nervous_tinted_context" if modulation < 0.24 else "overcoupled_context"

    return _normalize_active_context_trace(item)


def _decay_active_context_trace(trace, market_tick_advanced=True):

    item = _normalize_active_context_trace(trace)
    if not item:
        return {}

    if market_tick_advanced:
        decay = float(getattr(Config, "MCM_ACTIVE_CONTEXT_TRACE_DECAY", 0.92) or 0.92)
    else:
        decay = float(getattr(Config, "MCM_ACTIVE_CONTEXT_TRACE_IDLE_DECAY", 0.975) or 0.975)

    item["activation"] = max(0.0, min(1.0, float(item.get("activation", 0.0) or 0.0) * max(0.0, min(1.0, decay))))

    if item["activation"] <= 0.01:
        return {}

    return dict(item)


def _build_active_context_trace_from_inner_cluster(bot=None):

    if bot is None:
        return {}

    cluster_id = str(getattr(bot, "last_inner_context_cluster_id", "-") or "-").strip()
    if not cluster_id or cluster_id == "-":
        return {}

    inner_context_clusters = dict(getattr(bot, "inner_context_clusters", {}) or {})
    experience_space = dict(getattr(bot, "mcm_experience_space", {}) or {})
    inner_context_links = dict(experience_space.get("inner_context_links", {}) or {})

    source = dict(inner_context_clusters.get(cluster_id, {}) or inner_context_links.get(cluster_id, {}) or {})
    if not source:
        return {}

    support = max(0.0, min(1.0, float(source.get("pattern_support_score", source.get("inner_pattern_support", 0.0)) or 0.0)))
    conflict = max(0.0, min(1.0, float(source.get("pattern_conflict_score", source.get("inner_pattern_conflict", 0.0)) or 0.0)))
    fragility = max(0.0, min(1.0, float(source.get("pattern_fragility_score", source.get("inner_pattern_fragility", 0.0)) or 0.0)))
    bearing = max(0.0, min(1.0, float(source.get("pattern_bearing_score", source.get("inner_pattern_bearing", 0.0)) or 0.0)))
    reinforcement = max(0.0, min(1.0, float(source.get("pattern_reinforcement", source.get("reinforcement", 0.0)) or 0.0)))
    attenuation = max(0.0, min(1.0, float(source.get("pattern_attenuation", source.get("attenuation", 0.0)) or 0.0)))
    neurochemical_profile = _extract_neurochemical_profile(source)
    neuro_support = max(
        0.0,
        min(
            1.0,
            (
                max(0.0, float(neurochemical_profile.get("experience_effect_score", 0.0) or 0.0)) * 2.0
                + float(neurochemical_profile.get("confidence_signal", 0.0) or 0.0)
                + float(neurochemical_profile.get("stability_signal", 0.0) or 0.0)
                + float(neurochemical_profile.get("discipline_signal", 0.0) or 0.0)
                + max(0.0, float(neurochemical_profile.get("carrying_capacity_delta", 0.0) or 0.0))
            ) / 4.0,
        ),
    )
    neuro_strain = max(
        0.0,
        min(
            1.0,
            (
                max(0.0, -float(neurochemical_profile.get("experience_effect_score", 0.0) or 0.0)) * 2.0
                + float(neurochemical_profile.get("chaos_penalty", 0.0) or 0.0)
                + float(neurochemical_profile.get("variance_penalty", 0.0) or 0.0)
                + float(neurochemical_profile.get("overactivation_signal", 0.0) or 0.0)
                + float(neurochemical_profile.get("overstrain_penalty", 0.0) or 0.0)
            ) / 4.0,
        ),
    )
    reinforcement = max(0.0, min(1.0, reinforcement + (neuro_support * 0.10) - (neuro_strain * 0.08)))
    attenuation = max(0.0, min(1.0, attenuation + (neuro_strain * 0.12) - (neuro_support * 0.06)))
    trust = max(0.0, min(1.0, float(source.get("trust", 0.0) or 0.0)))
    neural_felt_state = dict(source.get("neural_felt_state", {}) or {})
    neural_felt_bearing = max(0.0, min(1.0, float(source.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", 0.0)) or 0.0)))
    neural_felt_pressure = max(0.0, min(1.0, float(source.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", 0.0)) or 0.0)))
    neural_felt_memory_resonance = max(0.0, min(1.0, float(source.get("neural_felt_memory_resonance", neural_felt_state.get("neural_felt_memory_resonance", 0.0)) or 0.0)))
    neural_felt_context_reactivation = max(0.0, min(1.0, float(source.get("neural_felt_context_reactivation", neural_felt_state.get("neural_felt_context_reactivation", 0.0)) or 0.0)))
    neural_felt_label = str(source.get("neural_felt_label", neural_felt_state.get("neural_felt_label", "quiet_neural_felt")) or "quiet_neural_felt")
    inner_field_history_state = dict(source.get("inner_field_history_state", {}) or {})
    inner_field_history_length = max(0, int(float(source.get("inner_field_history_length", inner_field_history_state.get("inner_field_history_length", 0)) or 0)))
    inner_field_pressure_trend = max(-1.0, min(1.0, float(source.get("inner_field_pressure_trend", inner_field_history_state.get("inner_field_pressure_trend", 0.0)) or 0.0)))
    inner_field_bearing_trend = max(-1.0, min(1.0, float(source.get("inner_field_bearing_trend", inner_field_history_state.get("inner_field_bearing_trend", 0.0)) or 0.0)))
    inner_field_topology_tension_trend = max(-1.0, min(1.0, float(source.get("inner_field_topology_tension_trend", inner_field_history_state.get("inner_field_topology_tension_trend", 0.0)) or 0.0)))
    inner_field_memory_resonance_trend = max(-1.0, min(1.0, float(source.get("inner_field_memory_resonance_trend", inner_field_history_state.get("inner_field_memory_resonance_trend", 0.0)) or 0.0)))
    inner_field_history_label = str(source.get("inner_field_history_label", inner_field_history_state.get("inner_field_history_label", "stable_field_trace")) or "stable_field_trace")
    field_topology_layout_state = dict(source.get("field_topology_layout_state", {}) or {})
    field_topology_rows = max(0, int(float(source.get("field_topology_rows", field_topology_layout_state.get("topology_rows", 0)) or 0)))
    field_topology_cols = max(0, int(float(source.get("field_topology_cols", field_topology_layout_state.get("topology_cols", 0)) or 0)))
    field_topology_position_count = max(0, int(float(source.get("field_topology_position_count", field_topology_layout_state.get("topology_position_count", 0)) or 0)))
    field_topology_neighbor_link_count = max(0, int(float(source.get("field_topology_neighbor_link_count", field_topology_layout_state.get("topology_neighbor_link_count", 0)) or 0)))
    field_topology_neighbor_count_mean = max(0.0, float(source.get("field_topology_neighbor_count_mean", field_topology_layout_state.get("topology_neighbor_count_mean", 0.0)) or 0.0))
    field_topology_neighbor_count_max = max(0, int(float(source.get("field_topology_neighbor_count_max", field_topology_layout_state.get("topology_neighbor_count_max", 0)) or 0)))
    field_areal_topology_density_mean = max(0.0, min(1.0, float(source.get("field_areal_topology_density_mean", 0.0) or 0.0)))
    field_areal_topology_span_mean = max(0.0, float(source.get("field_areal_topology_span_mean", 0.0) or 0.0))
    field_areal_topology_boundary_mean = max(0.0, float(source.get("field_areal_topology_boundary_mean", 0.0) or 0.0))
    field_perception_focus = max(0.0, min(1.0, float(source.get("field_perception_focus", 0.0) or 0.0)))
    field_perception_clarity = max(0.0, min(1.0, float(source.get("field_perception_clarity", 0.0) or 0.0)))
    field_perception_stability = max(0.0, min(1.0, float(source.get("field_perception_stability", 0.0) or 0.0)))
    field_perception_fragmentation = max(0.0, min(1.0, float(source.get("field_perception_fragmentation", 0.0) or 0.0)))
    field_perception_strain = max(0.0, min(1.0, float(source.get("field_perception_strain", 0.0) or 0.0)))
    dominant_activity_island_id = str(source.get("dominant_activity_island_id", "-") or "-")
    field_pattern_signature = dict(source.get("field_pattern_signature", {}) or {})
    field_pattern_signature_key = str(source.get("field_pattern_signature_key", field_pattern_signature.get("signature_key", "")) or "")
    field_pattern_vector = [float(value) for value in list(source.get("field_pattern_vector", field_pattern_signature.get("field_pattern_vector", [])) or [])]
    inner_pattern_identity = str(source.get("inner_pattern_identity", "") or "")
    inner_pattern_identity_label = str(source.get("inner_pattern_identity_label", field_pattern_signature.get("identity_label", "")) or "")
    inner_pattern_identity_confidence = max(0.0, min(1.0, float(source.get("inner_pattern_identity_confidence", 0.0) or 0.0)))
    inner_pattern_identity_streak = max(0, int(float(source.get("inner_pattern_identity_streak", 0) or 0)))
    inner_pattern_identity_stability = max(0.0, min(1.0, float(source.get("inner_pattern_identity_stability", 0.0) or 0.0)))
    inner_pattern_identity_recurrent = bool(source.get("inner_pattern_identity_recurrent", False))
    inner_pattern_identity_changed = bool(source.get("inner_pattern_identity_changed", False))
    inner_pattern_identity_last_seen_tick = max(0, int(float(source.get("inner_pattern_identity_last_seen_tick", 0) or 0)))
    inner_pattern_recognition_state = dict(source.get("inner_pattern_recognition_state", {}) or {})
    inner_pattern_recognition_label = str(source.get("inner_pattern_recognition_label", inner_pattern_recognition_state.get("recognition_label", "unsettled_inner_pattern")) or "unsettled_inner_pattern")
    inner_pattern_recognition_strength = max(0.0, min(1.0, float(source.get("inner_pattern_recognition_strength", inner_pattern_recognition_state.get("recognition_strength", 0.0)) or 0.0)))
    inner_pattern_recognition_recurrent = bool(source.get("inner_pattern_recognition_recurrent", inner_pattern_recognition_state.get("recurrent", False)))
    inner_pattern_recognition_changed = bool(source.get("inner_pattern_recognition_changed", inner_pattern_recognition_state.get("changed", False)))

    activation = max(
        0.0,
        min(
            1.0,
            0.08
            + (trust * 0.30)
            + (support * 0.18)
            + (bearing * 0.18)
            + (reinforcement * 0.18)
            + (neuro_support * 0.08)
            - (conflict * 0.10)
            - (attenuation * 0.08)
            - (neuro_strain * 0.07),
        ),
    )

    action_support = max(0.0, min(1.0, (support * 0.28) + (bearing * 0.34) + (reinforcement * 0.24) + (neuro_support * 0.08) - (conflict * 0.14) - (neuro_strain * 0.06)))
    observe_pressure = max(0.0, min(1.0, (conflict * 0.30) + (fragility * 0.34) + (attenuation * 0.24) + (neuro_strain * 0.08) - (reinforcement * 0.08)))
    replan_pressure = max(0.0, min(1.0, (conflict * 0.34) + (attenuation * 0.28) + (fragility * 0.18) + (neuro_strain * 0.07) - (support * 0.10) - (neuro_support * 0.04)))

    return {
        "cluster_id": str(cluster_id),
        "activation": float(activation),
        "support": float(support),
        "conflict": float(conflict),
        "fragility": float(fragility),
        "bearing": float(bearing),
        "action_support": float(action_support),
        "observe_pressure": float(observe_pressure),
        "replan_pressure": float(replan_pressure),
        "reinforcement": float(reinforcement),
        "attenuation": float(attenuation),
        "experience_neurochemical_profile": dict(neurochemical_profile or {}),
        "experience_effect_score": float(neurochemical_profile.get("experience_effect_score", 0.0) or 0.0),
        "profit_reward": float(neurochemical_profile.get("profit_reward", 0.0) or 0.0),
        "relief_signal": float(neurochemical_profile.get("relief_signal", 0.0) or 0.0),
        "stability_signal": float(neurochemical_profile.get("stability_signal", 0.0) or 0.0),
        "discipline_signal": float(neurochemical_profile.get("discipline_signal", 0.0) or 0.0),
        "confidence_signal": float(neurochemical_profile.get("confidence_signal", 0.0) or 0.0),
        "overactivation_signal": float(neurochemical_profile.get("overactivation_signal", 0.0) or 0.0),
        "chaos_penalty": float(neurochemical_profile.get("chaos_penalty", 0.0) or 0.0),
        "variance_penalty": float(neurochemical_profile.get("variance_penalty", 0.0) or 0.0),
        "overstrain_penalty": float(neurochemical_profile.get("overstrain_penalty", 0.0) or 0.0),
        "carrying_capacity_delta": float(neurochemical_profile.get("carrying_capacity_delta", 0.0) or 0.0),
        "self_confidence_delta": float(neurochemical_profile.get("self_confidence_delta", 0.0) or 0.0),
        "process_quality": float(neurochemical_profile.get("process_quality", 0.0) or 0.0),
        "neurochemical_support": float(neuro_support),
        "neurochemical_strain": float(neuro_strain),
        "neural_felt_state": dict(neural_felt_state or {}),
        "neural_felt_bearing": float(neural_felt_bearing),
        "neural_felt_pressure": float(neural_felt_pressure),
        "neural_felt_memory_resonance": float(neural_felt_memory_resonance),
        "neural_felt_context_reactivation": float(neural_felt_context_reactivation),
        "neural_felt_label": str(neural_felt_label),
        "inner_field_history_state": dict(inner_field_history_state or {}),
        "inner_field_history_length": int(inner_field_history_length),
        "inner_field_pressure_trend": float(inner_field_pressure_trend),
        "inner_field_bearing_trend": float(inner_field_bearing_trend),
        "inner_field_topology_tension_trend": float(inner_field_topology_tension_trend),
        "inner_field_memory_resonance_trend": float(inner_field_memory_resonance_trend),
        "inner_field_history_label": str(inner_field_history_label),
        "field_topology_layout_state": dict(field_topology_layout_state or {}),
        "field_topology_rows": int(field_topology_rows),
        "field_topology_cols": int(field_topology_cols),
        "field_topology_position_count": int(field_topology_position_count),
        "field_topology_neighbor_link_count": int(field_topology_neighbor_link_count),
        "field_topology_neighbor_count_mean": float(field_topology_neighbor_count_mean),
        "field_topology_neighbor_count_max": int(field_topology_neighbor_count_max),
        "field_areal_topology_density_mean": float(field_areal_topology_density_mean),
        "field_areal_topology_span_mean": float(field_areal_topology_span_mean),
        "field_areal_topology_boundary_mean": float(field_areal_topology_boundary_mean),
        "field_perception_focus": float(field_perception_focus),
        "field_perception_clarity": float(field_perception_clarity),
        "field_perception_stability": float(field_perception_stability),
        "field_perception_fragmentation": float(field_perception_fragmentation),
        "field_perception_strain": float(field_perception_strain),
        "dominant_activity_island_id": str(dominant_activity_island_id),
        "field_pattern_signature": dict(field_pattern_signature or {}),
        "field_pattern_signature_key": str(field_pattern_signature_key),
        "field_pattern_vector": [float(value) for value in list(field_pattern_vector or [])],
        "inner_pattern_identity": str(inner_pattern_identity),
        "inner_pattern_identity_label": str(inner_pattern_identity_label),
        "inner_pattern_identity_confidence": float(inner_pattern_identity_confidence),
        "inner_pattern_identity_streak": int(inner_pattern_identity_streak),
        "inner_pattern_identity_stability": float(inner_pattern_identity_stability),
        "inner_pattern_identity_recurrent": bool(inner_pattern_identity_recurrent),
        "inner_pattern_identity_changed": bool(inner_pattern_identity_changed),
        "inner_pattern_identity_last_seen_tick": int(inner_pattern_identity_last_seen_tick),
        "inner_pattern_recognition_state": dict(inner_pattern_recognition_state or {}),
        "inner_pattern_recognition_label": str(inner_pattern_recognition_label),
        "inner_pattern_recognition_strength": float(inner_pattern_recognition_strength),
        "inner_pattern_recognition_recurrent": bool(inner_pattern_recognition_recurrent),
        "inner_pattern_recognition_changed": bool(inner_pattern_recognition_changed),
        "last_seen_tick": int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0),
    }


def _build_active_context_trace_from_temporal_state(bot=None, runtime_result=None):

    if bot is None:
        return {}

    result = dict(runtime_result or {})
    temporal_state = dict(
        result.get(
            "temporal_perception_state",
            getattr(bot, "temporal_perception_state", {}) or {},
        )
        or {}
    )
    if not temporal_state:
        return {}

    identity = str(temporal_state.get("temporal_identity", "") or "").strip()
    if not identity or identity == "-":
        return {}

    continuity = max(0.0, min(1.0, float(temporal_state.get("temporal_continuity", 0.0) or 0.0)))
    source_binding = max(0.0, min(1.0, float(temporal_state.get("temporal_source_binding", 0.0) or 0.0)))
    recurrence = max(0.0, min(1.0, float(temporal_state.get("temporal_recurrence", 0.0) or 0.0)))
    novelty = max(0.0, min(1.0, float(temporal_state.get("temporal_novelty", 0.0) or 0.0)))
    afterimage = max(0.0, min(1.0, float(temporal_state.get("temporal_afterimage", 0.0) or 0.0)))
    decay = max(0.0, min(1.0, float(temporal_state.get("temporal_decay", 0.0) or 0.0)))
    context_depth = max(0.0, min(1.0, float(temporal_state.get("temporal_context_depth", 0.0) or 0.0)))
    self_consistency = max(0.0, min(1.0, float(temporal_state.get("temporal_self_consistency", 0.0) or 0.0)))
    sequence_coherence = max(0.0, min(1.0, float(temporal_state.get("perception_sequence_coherence", 0.0) or 0.0)))
    memory_time_distance = max(0.0, min(1.0, float(temporal_state.get("memory_time_distance", 1.0) or 1.0)))
    structure_quality = max(0.0, min(1.0, float(temporal_state.get("temporal_structure_quality", 0.0) or 0.0)))
    structure_stability = max(0.0, min(1.0, float(temporal_state.get("temporal_structure_stability", 0.0) or 0.0)))
    context_confidence = max(0.0, min(1.0, float(temporal_state.get("temporal_context_confidence", 0.0) or 0.0)))
    visual_grounding_strength = max(0.0, min(1.0, float(temporal_state.get("temporal_visual_grounding_strength", 0.0) or 0.0)))
    binding_state = str(temporal_state.get("temporal_binding_state", "unbound_moment") or "unbound_moment")
    unbound_pressure = 1.0 if binding_state in ("unbound_moment", "aged_memory_contact", "afterimage_contact") else 0.0
    reality_anchor = max(
        0.0,
        min(
            1.0,
            (source_binding * 0.22)
            + (sequence_coherence * 0.18)
            + (structure_quality * 0.18)
            + (structure_stability * 0.12)
            + (context_confidence * 0.12)
            + (visual_grounding_strength * 0.12)
            + (continuity * 0.06),
        ),
    )
    overtrust_pressure = max(
        0.0,
        min(
            1.0,
            (unbound_pressure * 0.20)
            + (decay * 0.18)
            + (memory_time_distance * 0.14)
            + (novelty * 0.14)
            + (max(0.0, 0.52 - reality_anchor) * 0.34),
        ),
    )

    activation = max(
        0.0,
        min(
            1.0,
            0.03
            + (continuity * 0.20)
            + (source_binding * 0.18)
            + (sequence_coherence * 0.20)
            + (context_depth * 0.10)
            + (recurrence * 0.08)
            + (reality_anchor * 0.10)
            - (decay * 0.06)
            - (novelty * 0.04),
        ),
    )
    activation = max(0.0, min(1.0, activation * (0.54 + (reality_anchor * 0.34)) - (overtrust_pressure * 0.10)))
    if activation <= 0.01:
        return {}

    support = max(0.0, min(1.0, ((source_binding * 0.28) + (sequence_coherence * 0.24) + (continuity * 0.16) + (context_depth * 0.10) + (reality_anchor * 0.18)) * (0.60 + (reality_anchor * 0.32))))
    conflict = max(0.0, min(1.0, (novelty * 0.22) + (decay * 0.22) + (afterimage * 0.14) + (max(0.0, 0.42 - source_binding) * 0.16) + (overtrust_pressure * 0.30)))
    fragility = max(0.0, min(1.0, (decay * 0.24) + (novelty * 0.18) + (max(0.0, 0.42 - sequence_coherence) * 0.20) + (afterimage * 0.10) + (overtrust_pressure * 0.18)))
    bearing = max(0.0, min(1.0, ((self_consistency * 0.24) + (sequence_coherence * 0.24) + (context_depth * 0.16) + (source_binding * 0.12) + (reality_anchor * 0.18)) * (0.58 + (reality_anchor * 0.34))))
    reinforcement = max(0.0, min(1.0, (recurrence * 0.22) + (continuity * 0.24) + (bearing * 0.24) + (max(0.0, 1.0 - memory_time_distance) * 0.10)))
    attenuation = max(0.0, min(1.0, (decay * 0.28) + (memory_time_distance * 0.18) + (novelty * 0.16) + (max(0.0, 0.34 - continuity) * 0.14) + (overtrust_pressure * 0.24)))

    return {
        "cluster_id": f"temporal:{identity}",
        "activation": float(activation),
        "support": float(support),
        "conflict": float(conflict),
        "fragility": float(fragility),
        "bearing": float(bearing),
        "action_support": float(max(0.0, min(1.0, (bearing * 0.28) + (support * 0.20) - (conflict * 0.10)))),
        "observe_pressure": float(max(0.0, min(1.0, (conflict * 0.28) + (fragility * 0.24) + (novelty * 0.12)))),
        "replan_pressure": float(max(0.0, min(1.0, (decay * 0.24) + (afterimage * 0.20) + (max(0.0, novelty - continuity) * 0.18)))),
        "reinforcement": float(reinforcement),
        "attenuation": float(attenuation),
        "reality_anchor": float(reality_anchor),
        "overtrust_pressure": float(overtrust_pressure),
        "inner_field_history_length": int(max(0, int(float(temporal_state.get("temporal_ticks_since_seen", 0) or 0)))),
        "inner_field_history_label": str(temporal_state.get("temporal_binding_state", "unbound_moment") or "unbound_moment"),
        "inner_field_pressure_trend": float(max(-1.0, min(1.0, novelty + decay - continuity - source_binding))),
        "inner_field_bearing_trend": float(max(-1.0, min(1.0, bearing - conflict))),
        "inner_field_topology_tension_trend": float(max(-1.0, min(1.0, fragility - sequence_coherence))),
        "inner_field_memory_resonance_trend": float(max(-1.0, min(1.0, recurrence + continuity - memory_time_distance))),
        "inner_pattern_identity": str(identity),
        "inner_pattern_identity_label": str(temporal_state.get("temporal_binding_state", "unbound_moment") or "unbound_moment"),
        "inner_pattern_identity_confidence": float(source_binding),
        "inner_pattern_identity_stability": float(sequence_coherence),
        "inner_pattern_identity_streak": int(max(0, int(float(temporal_state.get("temporal_ticks_since_seen", 0) or 0)))),
        "inner_pattern_identity_recurrent": bool(recurrence >= 0.38),
        "inner_pattern_identity_changed": bool(novelty > continuity),
        "inner_pattern_recognition_label": str(temporal_state.get("temporal_binding_state", "unbound_moment") or "unbound_moment"),
        "inner_pattern_recognition_strength": float(sequence_coherence),
        "inner_pattern_recognition_recurrent": bool(recurrence >= 0.38),
        "inner_pattern_recognition_changed": bool(novelty > continuity),
        "last_seen_tick": int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0),
    }


def _refresh_active_context_trace(trace, bot=None, runtime_result=None, market_tick_advanced=True):

    current = _decay_active_context_trace(
        trace,
        market_tick_advanced=market_tick_advanced,
    )
    candidate = _build_active_context_trace_from_inner_cluster(bot=bot)
    if not candidate:
        candidate = _build_active_context_trace_from_temporal_state(
            bot=bot,
            runtime_result=runtime_result,
        )

    if not candidate:
        return _apply_nervous_context_modulation(
            current,
            bot=bot,
            runtime_result=runtime_result,
        )

    if not current:
        return _apply_nervous_context_modulation(
            candidate,
            bot=bot,
            runtime_result=runtime_result,
        )

    if str(current.get("cluster_id", "-") or "-") != str(candidate.get("cluster_id", "-") or "-"):
        if float(candidate.get("activation", 0.0) or 0.0) >= float(current.get("activation", 0.0) or 0.0) * 0.78:
            return _apply_nervous_context_modulation(
                candidate,
                bot=bot,
                runtime_result=runtime_result,
            )
        return _apply_nervous_context_modulation(
            current,
            bot=bot,
            runtime_result=runtime_result,
        )

    alpha = max(0.08, min(0.34, float(candidate.get("activation", 0.0) or 0.0)))
    merged = dict(current)
    merged["activation"] = float((float(current.get("activation", 0.0) or 0.0) * (1.0 - alpha)) + (float(candidate.get("activation", 0.0) or 0.0) * alpha))

    for key in (
        "support",
        "conflict",
        "fragility",
        "bearing",
        "action_support",
        "observe_pressure",
        "replan_pressure",
        "reinforcement",
        "attenuation",
        "experience_effect_score",
        "profit_reward",
        "relief_signal",
        "stability_signal",
        "discipline_signal",
        "confidence_signal",
        "overactivation_signal",
        "chaos_penalty",
        "variance_penalty",
        "overstrain_penalty",
        "carrying_capacity_delta",
        "self_confidence_delta",
        "process_quality",
        "neurochemical_support",
        "neurochemical_strain",
        "reality_anchor",
        "overtrust_pressure",
        "active_context_self_certainty",
        "nervous_context_overcoupling",
    ):
        merged[key] = float((float(current.get(key, 0.0) or 0.0) * (1.0 - alpha)) + (float(candidate.get(key, 0.0) or 0.0) * alpha))

    for key in (
        "neural_felt_bearing",
        "neural_felt_pressure",
        "neural_felt_memory_resonance",
        "neural_felt_context_reactivation",
    ):
        merged[key] = float((float(current.get(key, 0.0) or 0.0) * (1.0 - alpha)) + (float(candidate.get(key, 0.0) or 0.0) * alpha))

    for key in (
        "inner_field_pressure_trend",
        "inner_field_bearing_trend",
        "inner_field_topology_tension_trend",
        "inner_field_memory_resonance_trend",
    ):
        merged[key] = float((float(current.get(key, 0.0) or 0.0) * (1.0 - alpha)) + (float(candidate.get(key, 0.0) or 0.0) * alpha))

    merged["neural_felt_state"] = dict(candidate.get("neural_felt_state", current.get("neural_felt_state", {})) or {})
    merged["neural_felt_label"] = str(candidate.get("neural_felt_label", current.get("neural_felt_label", "quiet_neural_felt")) or "quiet_neural_felt")
    merged["inner_field_history_state"] = dict(candidate.get("inner_field_history_state", current.get("inner_field_history_state", {})) or {})
    merged["experience_neurochemical_profile"] = dict(candidate.get("experience_neurochemical_profile", current.get("experience_neurochemical_profile", {})) or {})
    merged["inner_field_history_length"] = int(candidate.get("inner_field_history_length", current.get("inner_field_history_length", 0)) or 0)
    merged["inner_field_history_label"] = str(candidate.get("inner_field_history_label", current.get("inner_field_history_label", "stable_field_trace")) or "stable_field_trace")
    merged["field_topology_layout_state"] = dict(candidate.get("field_topology_layout_state", current.get("field_topology_layout_state", {})) or {})
    merged["field_topology_rows"] = int(candidate.get("field_topology_rows", current.get("field_topology_rows", 0)) or 0)
    merged["field_topology_cols"] = int(candidate.get("field_topology_cols", current.get("field_topology_cols", 0)) or 0)
    merged["field_topology_position_count"] = int(candidate.get("field_topology_position_count", current.get("field_topology_position_count", 0)) or 0)
    merged["field_topology_neighbor_link_count"] = int(candidate.get("field_topology_neighbor_link_count", current.get("field_topology_neighbor_link_count", 0)) or 0)
    merged["field_topology_neighbor_count_mean"] = float(candidate.get("field_topology_neighbor_count_mean", current.get("field_topology_neighbor_count_mean", 0.0)) or 0.0)
    merged["field_topology_neighbor_count_max"] = int(candidate.get("field_topology_neighbor_count_max", current.get("field_topology_neighbor_count_max", 0)) or 0)
    merged["field_areal_topology_density_mean"] = float(candidate.get("field_areal_topology_density_mean", current.get("field_areal_topology_density_mean", 0.0)) or 0.0)
    merged["field_areal_topology_span_mean"] = float(candidate.get("field_areal_topology_span_mean", current.get("field_areal_topology_span_mean", 0.0)) or 0.0)
    merged["field_areal_topology_boundary_mean"] = float(candidate.get("field_areal_topology_boundary_mean", current.get("field_areal_topology_boundary_mean", 0.0)) or 0.0)
    for key in (
        "field_perception_focus",
        "field_perception_clarity",
        "field_perception_stability",
        "field_perception_fragmentation",
        "field_perception_strain",
    ):
        merged[key] = float((float(current.get(key, 0.0) or 0.0) * (1.0 - alpha)) + (float(candidate.get(key, 0.0) or 0.0) * alpha))
    merged["dominant_activity_island_id"] = str(candidate.get("dominant_activity_island_id", current.get("dominant_activity_island_id", "-")) or "-")
    merged["field_pattern_signature"] = dict(candidate.get("field_pattern_signature", current.get("field_pattern_signature", {})) or {})
    merged["field_pattern_signature_key"] = str(candidate.get("field_pattern_signature_key", current.get("field_pattern_signature_key", "")) or "")
    merged["field_pattern_vector"] = [float(value) for value in list(candidate.get("field_pattern_vector", current.get("field_pattern_vector", [])) or [])]
    merged["inner_pattern_identity"] = str(candidate.get("inner_pattern_identity", current.get("inner_pattern_identity", "")) or "")
    merged["inner_pattern_identity_label"] = str(candidate.get("inner_pattern_identity_label", current.get("inner_pattern_identity_label", "")) or "")
    merged["inner_pattern_identity_confidence"] = float(candidate.get("inner_pattern_identity_confidence", current.get("inner_pattern_identity_confidence", 0.0)) or 0.0)
    merged["inner_pattern_identity_streak"] = int(candidate.get("inner_pattern_identity_streak", current.get("inner_pattern_identity_streak", 0)) or 0)
    merged["inner_pattern_identity_stability"] = float(candidate.get("inner_pattern_identity_stability", current.get("inner_pattern_identity_stability", 0.0)) or 0.0)
    merged["inner_pattern_identity_recurrent"] = bool(candidate.get("inner_pattern_identity_recurrent", current.get("inner_pattern_identity_recurrent", False)))
    merged["inner_pattern_identity_changed"] = bool(candidate.get("inner_pattern_identity_changed", current.get("inner_pattern_identity_changed", False)))
    merged["inner_pattern_identity_last_seen_tick"] = int(candidate.get("inner_pattern_identity_last_seen_tick", current.get("inner_pattern_identity_last_seen_tick", 0)) or 0)
    merged["inner_pattern_recognition_state"] = dict(candidate.get("inner_pattern_recognition_state", current.get("inner_pattern_recognition_state", {})) or {})
    merged["inner_pattern_recognition_label"] = str(candidate.get("inner_pattern_recognition_label", current.get("inner_pattern_recognition_label", "unsettled_inner_pattern")) or "unsettled_inner_pattern")
    merged["inner_pattern_recognition_strength"] = float(candidate.get("inner_pattern_recognition_strength", current.get("inner_pattern_recognition_strength", 0.0)) or 0.0)
    merged["inner_pattern_recognition_recurrent"] = bool(candidate.get("inner_pattern_recognition_recurrent", current.get("inner_pattern_recognition_recurrent", False)))
    merged["inner_pattern_recognition_changed"] = bool(candidate.get("inner_pattern_recognition_changed", current.get("inner_pattern_recognition_changed", False)))
    merged["context_modulation_label"] = str(candidate.get("context_modulation_label", current.get("context_modulation_label", "unmodulated_context")) or "unmodulated_context")
    merged["last_seen_tick"] = int(candidate.get("last_seen_tick", current.get("last_seen_tick", 0)) or 0)
    return _apply_nervous_context_modulation(
        merged,
        bot=bot,
        runtime_result=runtime_result,
    )

