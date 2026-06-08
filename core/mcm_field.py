"""MCM field and neural substrate adapters."""

def _clip01(value):
    try:
        value = float(value)
    except Exception:
        return 0.0
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


from core.mcm_model import (
    AttractorSystem,
    ClusterDetector,
    MCMField,
    Memory,
    RegulationLayer,
    SelfModel,
)

def _extract_neurochemical_profile(source):

    item = dict(source or {})
    effect = dict(item.get("experience_neurochemical_effect", {}) or {})

    def _read(key, default=0.0):
        return float(
            item.get(
                key,
                item.get(
                    f"avg_{key}",
                    item.get(
                        f"last_{key}",
                        effect.get(key, default),
                    ),
                ),
            ) or default
        )

    return {
        "experience_effect_score": float(_read("experience_effect_score")),
        "profit_reward": float(_read("profit_reward")),
        "relief_signal": float(_read("relief_signal")),
        "stability_signal": float(_read("stability_signal")),
        "discipline_signal": float(_read("discipline_signal")),
        "confidence_signal": float(_read("confidence_signal")),
        "overactivation_signal": float(_read("overactivation_signal")),
        "chaos_penalty": float(_read("chaos_penalty")),
        "variance_penalty": float(_read("variance_penalty")),
        "overstrain_penalty": float(_read("overstrain_penalty")),
        "carrying_capacity_delta": float(_read("carrying_capacity_delta")),
        "self_confidence_delta": float(_read("self_confidence_delta")),
        "process_quality": float(_read("process_quality")),
    }

# --------------------------------------------------
def _normalize_active_context_trace(trace):

    item = dict(trace or {})
    cluster_id = str(item.get("cluster_id", item.get("inner_context_cluster_id", "-")) or "-").strip()

    if not cluster_id or cluster_id == "-":
        return {}

    try:
        activation = float(item.get("activation", 0.0) or 0.0)
    except Exception:
        activation = 0.0

    activation = max(0.0, min(1.0, activation))
    if activation <= 0.001:
        return {}

    neural_felt_state = dict(item.get("neural_felt_state", {}) or {})
    inner_field_history_state = dict(item.get("inner_field_history_state", {}) or {})
    field_topology_layout_state = dict(item.get("field_topology_layout_state", {}) or {})
    field_pattern_signature = dict(item.get("field_pattern_signature", {}) or {})
    inner_pattern_recognition_state = dict(item.get("inner_pattern_recognition_state", {}) or {})
    neurochemical_profile = _extract_neurochemical_profile(item)

    return {
        "cluster_id": str(cluster_id),
        "activation": float(activation),
        "support": max(0.0, min(1.0, float(item.get("support", 0.0) or 0.0))),
        "conflict": max(0.0, min(1.0, float(item.get("conflict", 0.0) or 0.0))),
        "fragility": max(0.0, min(1.0, float(item.get("fragility", 0.0) or 0.0))),
        "bearing": max(0.0, min(1.0, float(item.get("bearing", 0.0) or 0.0))),
        "action_support": max(0.0, min(1.0, float(item.get("action_support", 0.0) or 0.0))),
        "observe_pressure": max(0.0, min(1.0, float(item.get("observe_pressure", 0.0) or 0.0))),
        "replan_pressure": max(0.0, min(1.0, float(item.get("replan_pressure", 0.0) or 0.0))),
        "reinforcement": max(0.0, min(1.0, float(item.get("reinforcement", 0.0) or 0.0))),
        "attenuation": max(0.0, min(1.0, float(item.get("attenuation", 0.0) or 0.0))),
        "experience_neurochemical_profile": dict(neurochemical_profile or {}),
        "experience_effect_score": max(-0.28, min(0.28, float(neurochemical_profile.get("experience_effect_score", 0.0) or 0.0))),
        "profit_reward": max(-1.0, min(1.0, float(neurochemical_profile.get("profit_reward", 0.0) or 0.0))),
        "relief_signal": max(0.0, min(1.0, float(neurochemical_profile.get("relief_signal", 0.0) or 0.0))),
        "stability_signal": max(0.0, min(1.0, float(neurochemical_profile.get("stability_signal", 0.0) or 0.0))),
        "discipline_signal": max(0.0, min(1.0, float(neurochemical_profile.get("discipline_signal", 0.0) or 0.0))),
        "confidence_signal": max(0.0, min(1.0, float(neurochemical_profile.get("confidence_signal", 0.0) or 0.0))),
        "overactivation_signal": max(0.0, min(1.0, float(neurochemical_profile.get("overactivation_signal", 0.0) or 0.0))),
        "chaos_penalty": max(0.0, min(1.0, float(neurochemical_profile.get("chaos_penalty", 0.0) or 0.0))),
        "variance_penalty": max(0.0, min(1.0, float(neurochemical_profile.get("variance_penalty", 0.0) or 0.0))),
        "overstrain_penalty": max(0.0, min(1.0, float(neurochemical_profile.get("overstrain_penalty", 0.0) or 0.0))),
        "carrying_capacity_delta": max(-1.0, min(1.0, float(neurochemical_profile.get("carrying_capacity_delta", 0.0) or 0.0))),
        "self_confidence_delta": max(-0.28, min(0.28, float(neurochemical_profile.get("self_confidence_delta", 0.0) or 0.0))),
        "process_quality": max(0.0, min(1.0, float(neurochemical_profile.get("process_quality", 0.0) or 0.0))),
        "neural_felt_state": dict(neural_felt_state or {}),
        "neural_felt_bearing": max(0.0, min(1.0, float(item.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", 0.0)) or 0.0))),
        "neural_felt_pressure": max(0.0, min(1.0, float(item.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", 0.0)) or 0.0))),
        "neural_felt_memory_resonance": max(0.0, min(1.0, float(item.get("neural_felt_memory_resonance", neural_felt_state.get("neural_felt_memory_resonance", 0.0)) or 0.0))),
        "neural_felt_context_reactivation": max(0.0, min(1.0, float(item.get("neural_felt_context_reactivation", neural_felt_state.get("neural_felt_context_reactivation", 0.0)) or 0.0))),
        "neural_felt_label": str(item.get("neural_felt_label", neural_felt_state.get("neural_felt_label", "quiet_neural_felt")) or "quiet_neural_felt"),
        "inner_field_history_state": dict(inner_field_history_state or {}),
        "inner_field_history_length": max(0, int(float(item.get("inner_field_history_length", inner_field_history_state.get("inner_field_history_length", 0)) or 0))),
        "inner_field_pressure_trend": max(-1.0, min(1.0, float(item.get("inner_field_pressure_trend", inner_field_history_state.get("inner_field_pressure_trend", 0.0)) or 0.0))),
        "inner_field_bearing_trend": max(-1.0, min(1.0, float(item.get("inner_field_bearing_trend", inner_field_history_state.get("inner_field_bearing_trend", 0.0)) or 0.0))),
        "inner_field_topology_tension_trend": max(-1.0, min(1.0, float(item.get("inner_field_topology_tension_trend", inner_field_history_state.get("inner_field_topology_tension_trend", 0.0)) or 0.0))),
        "inner_field_memory_resonance_trend": max(-1.0, min(1.0, float(item.get("inner_field_memory_resonance_trend", inner_field_history_state.get("inner_field_memory_resonance_trend", 0.0)) or 0.0))),
        "inner_field_history_label": str(item.get("inner_field_history_label", inner_field_history_state.get("inner_field_history_label", "stable_field_trace")) or "stable_field_trace"),
        "field_topology_layout_state": dict(field_topology_layout_state or {}),
        "field_topology_rows": max(0, int(float(item.get("field_topology_rows", field_topology_layout_state.get("topology_rows", 0)) or 0))),
        "field_topology_cols": max(0, int(float(item.get("field_topology_cols", field_topology_layout_state.get("topology_cols", 0)) or 0))),
        "field_topology_position_count": max(0, int(float(item.get("field_topology_position_count", field_topology_layout_state.get("topology_position_count", 0)) or 0))),
        "field_topology_neighbor_link_count": max(0, int(float(item.get("field_topology_neighbor_link_count", field_topology_layout_state.get("topology_neighbor_link_count", 0)) or 0))),
        "field_topology_neighbor_count_mean": max(0.0, float(item.get("field_topology_neighbor_count_mean", field_topology_layout_state.get("topology_neighbor_count_mean", 0.0)) or 0.0)),
        "field_topology_neighbor_count_max": max(0, int(float(item.get("field_topology_neighbor_count_max", field_topology_layout_state.get("topology_neighbor_count_max", 0)) or 0))),
        "field_areal_topology_density_mean": max(0.0, min(1.0, float(item.get("field_areal_topology_density_mean", 0.0) or 0.0))),
        "field_areal_topology_span_mean": max(0.0, float(item.get("field_areal_topology_span_mean", 0.0) or 0.0)),
        "field_areal_topology_boundary_mean": max(0.0, float(item.get("field_areal_topology_boundary_mean", 0.0) or 0.0)),
        "field_perception_focus": max(0.0, min(1.0, float(item.get("field_perception_focus", 0.0) or 0.0))),
        "field_perception_clarity": max(0.0, min(1.0, float(item.get("field_perception_clarity", 0.0) or 0.0))),
        "field_perception_stability": max(0.0, min(1.0, float(item.get("field_perception_stability", 0.0) or 0.0))),
        "field_perception_fragmentation": max(0.0, min(1.0, float(item.get("field_perception_fragmentation", 0.0) or 0.0))),
        "field_perception_strain": max(0.0, min(1.0, float(item.get("field_perception_strain", 0.0) or 0.0))),
        "dominant_activity_island_id": str(item.get("dominant_activity_island_id", "-") or "-"),
        "field_pattern_signature": dict(field_pattern_signature or {}),
        "field_pattern_signature_key": str(item.get("field_pattern_signature_key", field_pattern_signature.get("signature_key", "")) or ""),
        "field_pattern_vector": [float(value) for value in list(item.get("field_pattern_vector", field_pattern_signature.get("field_pattern_vector", [])) or [])],
        "inner_pattern_identity": str(item.get("inner_pattern_identity", "") or ""),
        "inner_pattern_identity_label": str(item.get("inner_pattern_identity_label", field_pattern_signature.get("identity_label", "")) or ""),
        "inner_pattern_identity_confidence": max(0.0, min(1.0, float(item.get("inner_pattern_identity_confidence", 0.0) or 0.0))),
        "inner_pattern_identity_streak": max(0, int(float(item.get("inner_pattern_identity_streak", 0) or 0))),
        "inner_pattern_identity_stability": max(0.0, min(1.0, float(item.get("inner_pattern_identity_stability", 0.0) or 0.0))),
        "inner_pattern_identity_recurrent": bool(item.get("inner_pattern_identity_recurrent", False)),
        "inner_pattern_identity_changed": bool(item.get("inner_pattern_identity_changed", False)),
        "inner_pattern_identity_last_seen_tick": max(0, int(float(item.get("inner_pattern_identity_last_seen_tick", 0) or 0))),
        "inner_pattern_recognition_state": dict(inner_pattern_recognition_state or {}),
        "inner_pattern_recognition_label": str(item.get("inner_pattern_recognition_label", inner_pattern_recognition_state.get("recognition_label", "unsettled_inner_pattern")) or "unsettled_inner_pattern"),
        "inner_pattern_recognition_strength": max(0.0, min(1.0, float(item.get("inner_pattern_recognition_strength", inner_pattern_recognition_state.get("recognition_strength", 0.0)) or 0.0))),
        "inner_pattern_recognition_recurrent": bool(item.get("inner_pattern_recognition_recurrent", inner_pattern_recognition_state.get("recurrent", False))),
        "inner_pattern_recognition_changed": bool(item.get("inner_pattern_recognition_changed", inner_pattern_recognition_state.get("changed", False))),
        "active_context_self_certainty": max(0.0, min(1.0, float(item.get("active_context_self_certainty", 0.0) or 0.0))),
        "nervous_context_overcoupling": max(0.0, min(1.0, float(item.get("nervous_context_overcoupling", 0.0) or 0.0))),
        "context_modulation_label": str(item.get("context_modulation_label", "unmodulated_context") or "unmodulated_context"),
        "last_seen_tick": int(float(item.get("last_seen_tick", 0) or 0)),
    }

# --------------------------------------------------

def _resolve_affective_context_modulation(bot=None, fused_state=None):

    if bot is None:
        return {
            "felt_bearing_score": 0.0,
            "felt_profile_label": "mixed_unclear",
            "inner_pattern_support": 0.0,
            "inner_pattern_conflict": 0.0,
            "inner_pattern_fragility": 0.0,
            "inner_pattern_bearing": 0.0,
            "inner_pattern_state": "bearing",
            "pattern_support_score": 0.0,
            "pattern_conflict_score": 0.0,
            "pattern_fragility_score": 0.0,
            "pattern_bearing_score": 0.0,
            "pattern_reinforcement": 0.0,
            "pattern_attenuation": 0.0,
            "pattern_action_support": 0.0,
            "pattern_observe_pressure": 0.0,
            "pattern_replan_pressure": 0.0,
            "decision_bias": 0.0,
            "conviction_boost": 0.0,
            "caution_penalty": 0.0,
            "volatility_penalty": 0.0,
            "risk_shift": 0.0,
            "rr_shift": 0.0,
            "width_shift": 0.0,
        }

    fused = dict(fused_state or {})
    experience_space = dict(getattr(bot, "mcm_experience_space", {}) or {})
    context_links = dict(experience_space.get("context_links", {}) or {})
    inner_context_links = dict(experience_space.get("inner_context_links", {}) or {})

    context_cluster_id = str(
        fused.get(
            "context_cluster_id",
            getattr(bot, "last_context_cluster_id", "-"),
        ) or "-"
    ).strip()

    inner_context_cluster_id = str(
        fused.get(
            "inner_context_cluster_id",
            getattr(bot, "last_inner_context_cluster_id", "-"),
        ) or "-"
    ).strip()

    context_item = dict(context_links.get(context_cluster_id, {}) or {})
    inner_context_item = dict(inner_context_links.get(inner_context_cluster_id, {}) or {})

    context_felt_bearing_score = float(context_item.get("felt_bearing_score", 0.0) or 0.0)
    context_felt_profile_label = str(context_item.get("felt_profile_label", "mixed_unclear") or "mixed_unclear").strip().lower()

    inner_felt_bearing_score = float(inner_context_item.get("felt_bearing_score", 0.0) or 0.0)
    inner_felt_profile_label = str(inner_context_item.get("felt_profile_label", "mixed_unclear") or "mixed_unclear").strip().lower()

    selected_item = dict(context_item or {})
    felt_bearing_score = float(context_felt_bearing_score)
    felt_profile_label = str(context_felt_profile_label or "mixed_unclear")

    if inner_context_item:
        selected_item = dict(inner_context_item or {})
        felt_bearing_score = float((context_felt_bearing_score * 0.38) + (inner_felt_bearing_score * 0.62))

        if inner_felt_profile_label not in ("", "mixed_unclear", "-"):
            felt_profile_label = str(inner_felt_profile_label)
        else:
            felt_profile_label = str(context_felt_profile_label or "mixed_unclear")

    felt_profile = dict(selected_item.get("felt_profile", {}) or {})
    felt_distribution = dict(selected_item.get("felt_distribution", {}) or {})
    felt_averages = dict(felt_profile.get("averages", {}) or {})
    felt_variance = dict(felt_profile.get("variance", {}) or {})
    felt_stability = dict(felt_profile.get("stability", {}) or {})
    felt_dynamic = dict(felt_profile.get("dynamic", {}) or {})

    euphoric_ratio = float(felt_distribution.get("euphoric_ratio", 0.0) or 0.0)
    burden_ratio = float(felt_distribution.get("burden_ratio", 0.0) or 0.0)
    areal_fragmented_ratio = float(felt_distribution.get("areal_fragmented_ratio", 0.0) or 0.0)
    areal_supported_ratio = float(felt_distribution.get("areal_supported_ratio", 0.0) or 0.0)
    felt_recovery_cost_avg = float(felt_averages.get("felt_recovery_cost_avg", 0.0) or 0.0)
    felt_areal_support_avg = float(felt_averages.get("felt_areal_support_avg", 0.0) or 0.0)
    felt_areal_conflict_avg = float(felt_averages.get("felt_areal_conflict_avg", 0.0) or 0.0)
    felt_valence_variance = float(felt_variance.get("felt_valence_variance", 0.0) or 0.0)
    felt_bearing_variance = float(felt_variance.get("felt_bearing_variance", 0.0) or 0.0)
    felt_areal_support_variance = float(felt_variance.get("felt_areal_support_variance", 0.0) or 0.0)
    felt_areal_conflict_variance = float(felt_variance.get("felt_areal_conflict_variance", 0.0) or 0.0)
    felt_conflict_ratio = float(felt_stability.get("felt_conflict_ratio", 0.0) or 0.0)
    felt_areal_drift_avg = float(felt_dynamic.get("felt_areal_drift_avg", 0.0) or 0.0)

    topology_density = float(selected_item.get("avg_field_density", selected_item.get("field_density", 0.0)) or 0.0)
    topology_stability = float(selected_item.get("avg_field_stability", selected_item.get("field_stability", 0.0)) or 0.0)
    topology_cluster_count = float(selected_item.get("avg_field_cluster_count", selected_item.get("field_cluster_count", 0.0)) or 0.0)
    topology_mass_mean = float(selected_item.get("avg_field_cluster_mass_mean", selected_item.get("field_cluster_mass_mean", 0.0)) or 0.0)
    topology_mass_max = float(selected_item.get("avg_field_cluster_mass_max", selected_item.get("field_cluster_mass_max", 0.0)) or 0.0)
    topology_center_spread = float(selected_item.get("avg_field_cluster_center_spread", selected_item.get("field_cluster_center_spread", 0.0)) or 0.0)
    topology_separation = float(selected_item.get("avg_field_cluster_separation", selected_item.get("field_cluster_separation", 0.0)) or 0.0)
    topology_center_drift = float(selected_item.get("avg_field_cluster_center_drift", selected_item.get("field_cluster_center_drift", 0.0)) or 0.0)
    topology_count_drift = float(selected_item.get("avg_field_cluster_count_drift", selected_item.get("field_cluster_count_drift", 0.0)) or 0.0)
    topology_velocity_trend = float(selected_item.get("avg_field_velocity_trend", selected_item.get("field_velocity_trend", 0.0)) or 0.0)
    topology_reorganization_direction = str(selected_item.get("last_field_reorganization_direction", selected_item.get("field_reorganization_direction", "stable")) or "stable")
    topology_velocity = float(selected_item.get("avg_field_mean_velocity", selected_item.get("field_mean_velocity", 0.0)) or 0.0)
    topology_pressure = float(selected_item.get("avg_field_regulation_pressure", selected_item.get("field_regulation_pressure", 0.0)) or 0.0)
    areal_stability = float(selected_item.get("avg_field_areal_stability_mean", selected_item.get("field_areal_stability_mean", 0.0)) or 0.0)
    areal_pressure = float(selected_item.get("avg_field_areal_pressure_mean", selected_item.get("field_areal_pressure_mean", 0.0)) or 0.0)
    areal_dominance = float(selected_item.get("avg_field_areal_dominance", selected_item.get("field_areal_dominance", 0.0)) or 0.0)
    areal_fragmentation = float(selected_item.get("avg_field_areal_fragmentation", selected_item.get("field_areal_fragmentation", 0.0)) or 0.0)
    areal_coherence = float(selected_item.get("avg_field_areal_coherence_mean", selected_item.get("field_areal_coherence_mean", 0.0)) or 0.0)
    areal_conflict = float(selected_item.get("avg_field_areal_conflict_mean", selected_item.get("field_areal_conflict_mean", 0.0)) or 0.0)
    processing_areal_tension = float(selected_item.get("avg_processing_areal_tension", selected_item.get("processing_areal_tension", 0.0)) or 0.0)
    processing_areal_support = float(selected_item.get("avg_processing_areal_support", selected_item.get("processing_areal_support", 0.0)) or 0.0)
    thought_areal_pressure = float(selected_item.get("avg_thought_areal_pressure", selected_item.get("thought_areal_pressure", 0.0)) or 0.0)
    thought_areal_support = float(selected_item.get("avg_thought_areal_support", selected_item.get("thought_areal_support", 0.0)) or 0.0)
    inner_pattern_support = float(selected_item.get("inner_pattern_support", 0.0) or 0.0)
    inner_pattern_conflict = float(selected_item.get("inner_pattern_conflict", 0.0) or 0.0)
    inner_pattern_fragility = float(selected_item.get("inner_pattern_fragility", 0.0) or 0.0)
    inner_pattern_bearing = float(selected_item.get("inner_pattern_bearing", 0.0) or 0.0)
    inner_pattern_state = str(selected_item.get("inner_pattern_state", "bearing") or "bearing").strip().lower()
    pattern_support_score = float(selected_item.get("pattern_support_score", inner_pattern_support) or 0.0)
    pattern_conflict_score = float(selected_item.get("pattern_conflict_score", inner_pattern_conflict) or 0.0)
    pattern_fragility_score = float(selected_item.get("pattern_fragility_score", inner_pattern_fragility) or 0.0)
    pattern_bearing_score = float(selected_item.get("pattern_bearing_score", inner_pattern_bearing) or 0.0)
    pattern_reinforcement = float(selected_item.get("pattern_reinforcement", 0.0) or 0.0)
    pattern_attenuation = float(selected_item.get("pattern_attenuation", 0.0) or 0.0)
    active_context_trace = _normalize_active_context_trace(getattr(bot, "active_context_trace", {}) or {})
    active_context_strength = float(active_context_trace.get("activation", 0.0) or 0.0)

    if active_context_strength > 0.0:
        trace_blend = max(0.0, min(0.38, active_context_strength * 0.38))
        inner_pattern_support = float((inner_pattern_support * (1.0 - trace_blend)) + (float(active_context_trace.get("support", 0.0) or 0.0) * trace_blend))
        inner_pattern_conflict = float((inner_pattern_conflict * (1.0 - trace_blend)) + (float(active_context_trace.get("conflict", 0.0) or 0.0) * trace_blend))
        inner_pattern_fragility = float((inner_pattern_fragility * (1.0 - trace_blend)) + (float(active_context_trace.get("fragility", 0.0) or 0.0) * trace_blend))
        inner_pattern_bearing = float((inner_pattern_bearing * (1.0 - trace_blend)) + (float(active_context_trace.get("bearing", 0.0) or 0.0) * trace_blend))
        pattern_reinforcement = float((pattern_reinforcement * (1.0 - trace_blend)) + (float(active_context_trace.get("reinforcement", 0.0) or 0.0) * trace_blend))
        pattern_attenuation = float((pattern_attenuation * (1.0 - trace_blend)) + (float(active_context_trace.get("attenuation", 0.0) or 0.0) * trace_blend))


    topology_support = max(
        0.0,
        min(
            1.0,
            (topology_density * 0.14)
            + (topology_stability * 0.24)
            + (topology_mass_mean * 0.16)
            + (topology_mass_max * 0.18)
            - (min(1.0, topology_center_spread) * 0.12)
            - (min(1.0, topology_separation) * 0.10)
            - (min(1.0, topology_velocity) * 0.08),
        ),
    )

    topology_fragmentation = max(
        0.0,
        min(
            1.0,
            (min(1.0, topology_center_spread) * 0.20)
            + (min(1.0, topology_separation) * 0.16)
            + ((1.0 - topology_stability) * 0.16)
            + (min(1.0, topology_cluster_count / 6.0) * 0.10)
            + (min(1.0, topology_pressure) * 0.10)
            + (min(1.0, topology_velocity) * 0.12)
            + (min(1.0, topology_center_drift) * 0.08)
            + (min(1.0, topology_count_drift) * 0.06)
            + (min(1.0, max(0.0, topology_velocity_trend)) * 0.06),
        ),
    )

    areal_support_mod = max(
        0.0,
        min(
            1.0,
            (felt_areal_support_avg * 0.18)
            + (areal_supported_ratio * 0.12)
            + (areal_stability * 0.12)
            + (areal_coherence * 0.10)
            + (areal_dominance * 0.06)
            + (processing_areal_support * 0.10)
            + (thought_areal_support * 0.10)
            + (inner_pattern_support * 0.10)
            + (pattern_support_score * 0.10)
            + (pattern_bearing_score * 0.08)
            + (pattern_reinforcement * 0.04),
        ),
    )

    areal_conflict_mod = max(
        0.0,
        min(
            1.0,
            (felt_areal_conflict_avg * 0.14)
            + (areal_fragmented_ratio * 0.12)
            + (areal_fragmentation * 0.12)
            + (areal_conflict * 0.12)
            + (areal_pressure * 0.08)
            + (processing_areal_tension * 0.10)
            + (thought_areal_pressure * 0.08)
            + (felt_areal_conflict_variance * 0.04)
            + (inner_pattern_conflict * 0.10)
            + (pattern_conflict_score * 0.10)
            + (pattern_fragility_score * 0.06)
            + (pattern_attenuation * 0.04),
        ),
    )

    pattern_action_support = max(
        0.0,
        min(
            1.0,
            (areal_support_mod * 0.34)
            + (inner_pattern_bearing * 0.22)
            + (pattern_bearing_score * 0.18)
            + (pattern_reinforcement * 0.14)
            - (areal_conflict_mod * 0.16)
            - (pattern_attenuation * 0.10),
        ),
    )
    pattern_observe_pressure = max(
        0.0,
        min(
            1.0,
            (areal_conflict_mod * 0.30)
            + (inner_pattern_fragility * 0.20)
            + (pattern_fragility_score * 0.16)
            + (pattern_attenuation * 0.14)
            - (pattern_reinforcement * 0.08),
        ),
    )
    pattern_replan_pressure = max(
        0.0,
        min(
            1.0,
            (inner_pattern_conflict * 0.24)
            + (pattern_conflict_score * 0.22)
            + (pattern_attenuation * 0.18)
            + (areal_conflict_mod * 0.18)
            - (areal_support_mod * 0.10),
        ),
    )

    decision_bias = 0.0
    conviction_boost = 0.0
    caution_penalty = 0.0
    volatility_penalty = 0.0
    risk_shift = 0.0
    rr_shift = 0.0
    width_shift = 0.0

    if felt_profile_label == "stable_bearing":
        decision_bias += 0.06 + (felt_bearing_score * 0.04) + (areal_support_mod * 0.04)
        conviction_boost += 0.06 + (felt_bearing_score * 0.06) + (areal_support_mod * 0.06)
        risk_shift -= 0.04
        rr_shift += 0.05
        width_shift -= 0.05

    elif felt_profile_label == "recovering":
        decision_bias += 0.03 + (felt_bearing_score * 0.03) + (areal_support_mod * 0.02)
        conviction_boost += 0.03 + (areal_support_mod * 0.04)
        risk_shift -= 0.02
        rr_shift += 0.02
        width_shift -= 0.02

    elif felt_profile_label == "volatile_bearing":
        caution_penalty += 0.04 + (felt_bearing_variance * 0.12) + (felt_areal_support_variance * 0.10)
        volatility_penalty += 0.04 + (felt_valence_variance * 0.12) + (felt_areal_drift_avg * 0.08)
        risk_shift -= 0.04
        width_shift += 0.05

    elif felt_profile_label == "fragmented_conflict":
        caution_penalty += 0.08 + (areal_conflict_mod * 0.14)
        volatility_penalty += 0.06 + (areal_fragmented_ratio * 0.12) + (felt_areal_drift_avg * 0.08)
        risk_shift -= 0.08
        rr_shift -= 0.02
        width_shift += 0.08

    elif felt_profile_label == "euphoric_risk":
        caution_penalty += 0.06 + (euphoric_ratio * 0.12)
        volatility_penalty += 0.04 + (euphoric_ratio * 0.08)
        risk_shift -= 0.06
        rr_shift += 0.02
        width_shift += 0.03

    elif felt_profile_label == "burdened":
        caution_penalty += 0.08 + (burden_ratio * 0.12) + (areal_conflict_mod * 0.08)
        volatility_penalty += 0.05 + (felt_recovery_cost_avg * 0.10)
        risk_shift -= 0.08
        width_shift += 0.06

    else:
        caution_penalty += (felt_conflict_ratio * 0.04) + (areal_conflict_mod * 0.04)
        volatility_penalty += (felt_bearing_variance * 0.04) + (felt_areal_conflict_variance * 0.04)

    decision_bias += float(topology_support * 0.03)
    decision_bias += float(areal_support_mod * 0.04)
    conviction_boost += float(topology_support * 0.03)
    conviction_boost += float(areal_support_mod * 0.05)
    caution_penalty += float(topology_fragmentation * 0.03)
    caution_penalty += float(areal_conflict_mod * 0.05)
    volatility_penalty += float(topology_fragmentation * 0.03)
    volatility_penalty += float(areal_conflict_mod * 0.04)
    risk_shift -= float(topology_support * 0.02)
    risk_shift -= float(areal_support_mod * 0.03)
    risk_shift -= float(topology_fragmentation * 0.02)
    risk_shift -= float(areal_conflict_mod * 0.03)
    rr_shift += float(topology_support * 0.02)
    rr_shift += float(areal_support_mod * 0.03)
    rr_shift -= float(areal_conflict_mod * 0.02)
    width_shift -= float(topology_support * 0.02)
    width_shift -= float(areal_support_mod * 0.02)
    width_shift += float(topology_fragmentation * 0.02)
    width_shift += float(areal_conflict_mod * 0.03)

    if topology_reorganization_direction in ("reorganizing", "dissolving"):
        caution_penalty += 0.03
        volatility_penalty += 0.03
        risk_shift -= 0.03
        width_shift += 0.03
    elif topology_reorganization_direction == "forming":
        caution_penalty += 0.01
        volatility_penalty += 0.01
    elif topology_reorganization_direction == "accelerating":
        caution_penalty += 0.02
        volatility_penalty += 0.02
        width_shift += 0.02
    elif topology_reorganization_direction == "settling":
        decision_bias += 0.02
        conviction_boost += 0.02
        width_shift -= 0.01

    return {
        "felt_bearing_score": float(felt_bearing_score),
        "felt_profile_label": str(felt_profile_label),
        "inner_pattern_support": float(inner_pattern_support),
        "inner_pattern_conflict": float(inner_pattern_conflict),
        "inner_pattern_fragility": float(inner_pattern_fragility),
        "inner_pattern_bearing": float(inner_pattern_bearing),
        "inner_pattern_state": str(inner_pattern_state or "bearing"),
        "pattern_support_score": float(pattern_support_score),
        "pattern_conflict_score": float(pattern_conflict_score),
        "pattern_fragility_score": float(pattern_fragility_score),
        "pattern_bearing_score": float(pattern_bearing_score),
        "pattern_reinforcement": float(pattern_reinforcement),
        "pattern_attenuation": float(pattern_attenuation),
        "pattern_action_support": float(pattern_action_support),
        "pattern_observe_pressure": float(pattern_observe_pressure),
        "pattern_replan_pressure": float(pattern_replan_pressure),
        "decision_bias": float(decision_bias),
        "conviction_boost": float(conviction_boost),
        "caution_penalty": float(caution_penalty),
        "volatility_penalty": float(volatility_penalty),
        "risk_shift": float(risk_shift),
        "rr_shift": float(rr_shift),
        "width_shift": float(width_shift),
    }

# --------------------------------------------------

def build_active_mcm_contact_state(
    perception_state=None,
    processing_state=None,
    felt_state=None,
    thought_state=None,
    meta_regulation_state=None,
    strategic_window_state=None,
):
    perception = dict(perception_state or {})
    processing = dict(processing_state or {})
    felt = dict(felt_state or {})
    thought = dict(thought_state or {})
    meta = dict(meta_regulation_state or {})
    strategic = dict(strategic_window_state or {})
    conscious = dict(meta.get("conscious_perception", {}) or {})
    neuro = dict(meta.get("neurochemical_state", {}) or {})
    area_profile = dict(perception.get("area_perception_profile", {}) or {})
    area_visual_profile = dict(area_profile.get("area_visual_profile", {}) or {})
    area_hearing_profile = dict(area_profile.get("area_hearing_profile", {}) or {})
    area_temporal_profile = dict(area_profile.get("area_temporal_profile", {}) or {})
    area_mcm_profile = dict(area_profile.get("area_mcm_contact_profile", {}) or {})
    area_profile_state = str(area_profile.get("area_profile_state", "background_area_perception") or "background_area_perception")

    def _v(*sources, key=None, default=0.0):
        for source in sources:
            if not isinstance(source, dict):
                continue
            try:
                if key in source:
                    return float(source.get(key, default) or default)
            except Exception:
                continue
        return float(default)

    visual_clarity = _v(meta, processing, perception, key="visual_clarity")
    visual_object_stability = _v(meta, processing, perception, key="visual_object_stability")
    visual_form_pressure = _v(meta, processing, perception, key="visual_form_pressure")
    visual_form_novelty = _v(meta, processing, perception, key="visual_form_novelty")
    visual_shape_resonance = _v(meta, processing, perception, key="visual_shape_resonance")
    visual_attention_depth = _v(meta, processing, perception, key="visual_attention_depth")
    visual_form_contact = _v(meta, processing, perception, key="visual_form_contact")
    visual_inspection_pull = _v(meta, processing, perception, key="visual_inspection_pull")
    visual_background_filter = _v(meta, processing, perception, key="visual_background_filter")
    visual_mcm_contact_weight = _v(meta, processing, perception, key="visual_mcm_contact_weight", default=0.35)
    felt_visual_form_pressure = visual_form_pressure * _clip01(0.25 + (visual_mcm_contact_weight * 0.75))
    felt_visual_shape_resonance = visual_shape_resonance * _clip01(0.35 + (visual_mcm_contact_weight * 0.65))
    visual_reflective_clarity = visual_clarity * _clip01(0.30 + (visual_mcm_contact_weight * 0.70))
    visual_reflective_stability = visual_object_stability * _clip01(0.30 + (visual_mcm_contact_weight * 0.70))
    sensory_load = _v(meta, processing, perception, key="sensory_load")
    sensory_gate = _v(meta, processing, perception, key="sensory_gate", default=1.0)
    field_pressure = _v(meta, felt, processing, key="field_perception_pressure")
    field_support = _v(meta, felt, processing, key="field_perception_support")
    field_clarity = _v(meta, felt, processing, key="field_perception_clarity")
    field_focus = _v(meta, felt, processing, key="field_perception_focus")
    field_fragmentation = _v(meta, felt, processing, key="field_perception_fragmentation")
    field_strain = _v(meta, felt, processing, key="field_perception_strain")
    stimulus_field_effect = _v(meta, conscious, key="stimulus_field_effect")
    inner_impact_trace = _v(meta, conscious, key="inner_impact_trace")
    perceived_field_change = _v(meta, conscious, key="perceived_field_change")
    felt_afterimage = _v(meta, conscious, key="felt_afterimage")
    perceptual_distance = _v(meta, conscious, key="perceptual_distance")
    object_contact_depth = _v(meta, conscious, key="object_contact_depth")
    field_attachment = _v(meta, conscious, key="field_attachment")
    release_capacity = _v(meta, conscious, key="release_capacity")
    selective_attention = _v(meta, conscious, key="selective_attention")
    reflective_distance = _v(meta, conscious, key="reflective_distance")
    inner_outer_alignment = _v(meta, conscious, key="inner_outer_alignment")
    arousal_load = _v(meta, conscious, key="arousal_load")
    curiosity_tone = _v(meta, conscious, key="curiosity_tone")
    calm_tone = _v(meta, conscious, key="calm_tone")
    acetylcholine_focus = _v(meta, neuro, key="acetylcholine_focus")
    serotonin_stability = _v(meta, neuro, key="serotonin_stability")
    reward_stability_echo = _v(meta, neuro, key="reward_stability_echo")
    world_shift_evidence = _v(meta, neuro, key="world_shift_evidence")
    emotional_decoupling = _v(meta, neuro, key="emotional_decoupling")
    reactive_nervous_drive = _v(meta, neuro, key="reactive_nervous_drive")
    serotonin_carryover_risk = _v(meta, neuro, key="serotonin_carryover_risk")
    area_mcm_resonance = _v(strategic, meta, key="area_mcm_resonance")
    area_memory_pull = _v(strategic, meta, key="area_memory_pull")
    area_bearing_quality = _v(strategic, meta, key="area_bearing_quality")
    area_order_intention = _v(strategic, meta, key="area_order_intention")
    area_zoom_need = _v(strategic, meta, key="area_zoom_need")
    area_replay_fit = _v(strategic, meta, key="area_replay_fit")
    area_present_contact = _v(strategic, meta, key="area_present_contact")
    area_current_contact = _v(strategic, meta, key="area_current_contact")
    area_future_contact = _v(strategic, meta, key="area_future_contact")
    area_memory_contact = _v(strategic, meta, key="area_memory_contact")
    area_unlocated_pressure = _v(strategic, meta, key="area_unlocated_pressure")
    area_spacetime_fit = _v(strategic, meta, key="area_spacetime_fit")
    area_future_to_present_readiness = _v(strategic, meta, key="area_future_to_present_readiness")
    area_temporal_contact_mode = str(strategic.get("area_temporal_contact_mode", meta.get("area_temporal_contact_mode", "open_time_contact")) or "open_time_contact")
    strategic_patience = _v(strategic, meta, key="strategic_patience")
    old_structure_carryover_risk = _v(strategic, meta, key="old_structure_carryover_risk")
    mcm_spacetime_depth = _v(meta, key="mcm_spacetime_depth")
    memory_experience_depth = _v(meta, key="memory_experience_depth")
    future_projection_depth = _v(meta, key="future_projection_depth")
    temporal_self_location = _v(meta, key="temporal_self_location")
    temporal_self_location_state = str(meta.get("temporal_self_location_state", "unlocated_contact") or "unlocated_contact")
    spacetime_unlocated_pressure = _v(meta, key="spacetime_unlocated_pressure")
    spacetime_memory_bearing = _v(meta, key="spacetime_memory_bearing")
    spacetime_future_bearing = _v(meta, key="spacetime_future_bearing")
    spacetime_reflection_need = _v(meta, key="spacetime_reflection_need")
    spacetime_regulation_support = _v(meta, key="spacetime_regulation_support")
    spacetime_regulation_state = str(meta.get("spacetime_regulation_state", "spacetime_open") or "spacetime_open")
    structure_quality = _v(meta, perception, processing, felt, key="structure_quality")
    context_confidence = _v(meta, perception, processing, felt, key="context_confidence")
    trust_transfer_support = _v(meta, felt, thought, key="trust_transfer_support")
    transfer_maturity_gap = _v(meta, felt, thought, key="transfer_maturity_gap")
    transfer_bearing = _v(meta, felt, thought, key="transfer_bearing")
    area_multisensory_coherence = _v(area_profile, key="area_multisensory_coherence")
    area_attention_need = _v(area_profile, key="area_attention_need")
    area_felt_depth = _v(area_profile, key="area_felt_depth")
    area_perception_overcoupling_risk = _v(area_profile, key="area_overcoupling_risk")
    sensory_sync_state = dict(area_profile.get("sensory_sync_state", {}) or {})
    sensory_sync = _v(sensory_sync_state, area_profile, key="sensory_sync")
    sensory_desync_pressure = _v(sensory_sync_state, area_profile, key="sensory_desync_pressure")
    area_visual_score = _v(area_visual_profile, key="visual_score")
    area_hearing_score = _v(area_hearing_profile, key="hearing_score")
    area_temporal_score = _v(area_temporal_profile, key="temporal_score")
    area_mcm_felt_depth = _v(area_mcm_profile, key="felt_depth")
    area_profile_is_coherent = 1.0 if area_profile_state == "coherent_multisensory_area" else 0.0
    area_profile_needs_contact = 1.0 if area_profile_state == "area_needs_selective_contact" else 0.0
    area_profile_is_overcoupled = 1.0 if area_profile_state == "area_overcoupling_risk" else 0.0
    area_selective_contact_pull = _clip01(
        (area_attention_need * 0.24)
        + (area_multisensory_coherence * 0.20)
        + (area_visual_score * 0.14)
        + ((area_hearing_score * _clip01(0.30 + sensory_sync * 0.70)) * 0.08)
        + (area_temporal_score * 0.12)
        + (area_felt_depth * 0.14)
        + (sensory_sync * 0.10)
        + (area_profile_needs_contact * 0.08)
        - (area_perception_overcoupling_risk * 0.18)
        - (sensory_desync_pressure * 0.18)
        - (area_profile_is_overcoupled * 0.10)
    )
    area_selective_feel_permission = _clip01(
        (area_multisensory_coherence * 0.30)
        + (area_visual_score * 0.16)
        + (area_temporal_score * 0.14)
        + ((area_hearing_score * _clip01(0.30 + sensory_sync * 0.70)) * 0.08)
        + (area_felt_depth * 0.12)
        + (sensory_sync * 0.10)
        + (area_profile_is_coherent * 0.08)
        - (area_perception_overcoupling_risk * 0.28)
        - (sensory_desync_pressure * 0.22)
        - (area_profile_is_overcoupled * 0.14)
    )
    area_selective_feel_risk = _clip01(
        (area_perception_overcoupling_risk * 0.46)
        + (max(0.0, area_attention_need - area_multisensory_coherence) * 0.22)
        + (max(0.0, area_felt_depth - area_multisensory_coherence) * 0.16)
        + (max(0.0, area_mcm_felt_depth - area_multisensory_coherence) * 0.10)
        + (sensory_desync_pressure * 0.24)
        + (area_profile_is_overcoupled * 0.12)
    )

    contact_interest = _clip01(
        (felt_visual_form_pressure * 0.16)
        + (visual_form_novelty * 0.08)
        + (felt_visual_shape_resonance * 0.12)
        + (visual_form_contact * 0.08)
        + (visual_inspection_pull * 0.06)
        + (object_contact_depth * 0.14)
        + (selective_attention * 0.12)
        + (curiosity_tone * 0.12)
        + (area_mcm_resonance * 0.10)
        + (area_memory_pull * 0.08)
        + (area_zoom_need * 0.08)
        + (area_selective_contact_pull * 0.08)
        - (sensory_load * 0.05)
    )
    contact_presentness = _clip01(
        (area_current_contact * 0.24)
        + (temporal_self_location * 0.14)
        + (object_contact_depth * 0.14)
        + (area_present_contact * 0.10)
        + (spacetime_regulation_support * 0.08)
        + (max(0.0, area_current_contact - max(area_future_contact, area_memory_contact)) * 0.12)
        - (area_unlocated_pressure * 0.14)
        - (max(0.0, area_future_contact - area_current_contact) * 0.08)
    )
    contact_future_watch = _clip01(
        (area_future_contact * 0.36)
        + (spacetime_future_bearing * 0.25)
        + (future_projection_depth * 0.18)
        + (area_replay_fit * 0.10)
        + (max(0.0, area_future_contact - area_current_contact) * 0.12)
        - (contact_presentness * 0.05)
    )
    contact_memory_depth = _clip01(
        (area_memory_contact * 0.34)
        + (spacetime_memory_bearing * 0.22)
        + (memory_experience_depth * 0.18)
        + (area_memory_pull * 0.12)
        + (reflective_distance * 0.08)
        + (max(0.0, area_memory_contact - area_current_contact) * 0.10)
    )
    contact_unlocated_pressure = _clip01(
        (area_unlocated_pressure * 0.34)
        + (spacetime_unlocated_pressure * 0.24)
        + (max(0.0, 0.34 - temporal_self_location) * 0.16)
        + (spacetime_reflection_need * 0.12)
        + (max(0.0, contact_interest - area_spacetime_fit) * 0.10)
        - (contact_presentness * 0.10)
    )
    contact_temporal_bearing = _clip01(
        (contact_presentness * 0.24)
        + (contact_future_watch * 0.18)
        + (contact_memory_depth * 0.20)
        + (area_spacetime_fit * 0.20)
        + (mcm_spacetime_depth * 0.10)
        - (contact_unlocated_pressure * 0.18)
    )
    contact_temporal_reframe_need = _clip01(
        (contact_unlocated_pressure * 0.34)
        + (spacetime_reflection_need * 0.22)
        + (max(0.0, contact_future_watch - contact_presentness) * 0.14)
        + (max(0.0, contact_memory_depth - contact_presentness) * 0.10)
        - (contact_temporal_bearing * 0.12)
    )
    contact_future_to_present_readiness = _clip01(
        (contact_future_watch * 0.24)
        + (contact_temporal_bearing * 0.16)
        + (area_spacetime_fit * 0.12)
        + (area_future_to_present_readiness * 0.20)
        + (area_current_contact * 0.10)
        + ((1.0 if area_temporal_contact_mode == "maturing_present_area" else 0.0) * 0.08)
        - (contact_unlocated_pressure * 0.12)
        - (contact_temporal_reframe_need * 0.08)
    )
    contact_presentness = _clip01(
        contact_presentness
        + (max(0.0, contact_future_to_present_readiness - 0.40) * 0.16)
    )
    contact_temporal_mode = "open_time_contact"
    if contact_unlocated_pressure >= 0.26 and contact_temporal_bearing < 0.30:
        contact_temporal_mode = "unlocated_contact_probe"
    elif contact_future_to_present_readiness >= 0.43 and contact_presentness >= 0.28 and contact_temporal_bearing >= 0.24:
        contact_temporal_mode = "maturing_present_contact"
    elif contact_future_watch >= 0.30 and contact_future_watch >= (contact_presentness * 0.78) and contact_future_watch >= contact_memory_depth:
        contact_temporal_mode = "future_contact_watch"
    elif contact_memory_depth >= 0.25 and contact_memory_depth >= (contact_presentness * 0.64):
        contact_temporal_mode = "memory_contact_recall"
    elif contact_presentness >= max(contact_future_watch * 1.12, contact_memory_depth * 1.12) and contact_presentness >= 0.34:
        contact_temporal_mode = "present_contact_touch"
    elif spacetime_regulation_state == "afterimage_reframe" or area_temporal_contact_mode == "afterimage_area_reframe":
        contact_temporal_mode = "afterimage_contact_reframe"
    contact_focus_pull = _clip01(
        (field_focus * 0.16)
        + (visual_reflective_clarity * 0.14)
        + (visual_reflective_stability * 0.12)
        + (visual_attention_depth * 0.08)
        + (acetylcholine_focus * 0.16)
        + (selective_attention * 0.18)
        + (area_bearing_quality * 0.10)
        + (area_order_intention * 0.08)
        + (contact_temporal_bearing * 0.06)
        + (area_selective_feel_permission * 0.08)
        - (field_fragmentation * 0.08)
    )
    contact_resonance_probe = _clip01(
        (contact_interest * 0.18)
        + (field_pressure * 0.12)
        + (field_clarity * 0.10)
        + (felt_visual_shape_resonance * 0.14)
        + (stimulus_field_effect * 0.14)
        + (area_mcm_resonance * 0.16)
        + (area_memory_pull * 0.10)
        + (area_replay_fit * 0.06)
    )
    outer_inner_resonance = _clip01(
        (felt_visual_shape_resonance * 0.16)
        + (field_clarity * 0.12)
        + (field_support * 0.12)
        + (inner_outer_alignment * 0.18)
        + (area_mcm_resonance * 0.14)
        + (area_memory_pull * 0.10)
        + (contact_resonance_probe * 0.12)
        + (contact_temporal_bearing * 0.06)
        - (field_strain * 0.08)
        - (serotonin_carryover_risk * 0.06)
    )
    inner_change_from_contact = _clip01(
        (stimulus_field_effect * 0.22)
        + (inner_impact_trace * 0.20)
        + (perceived_field_change * 0.14)
        + (felt_afterimage * 0.10)
        + (field_attachment * 0.10)
        + (reactive_nervous_drive * 0.08)
        + (old_structure_carryover_risk * 0.06)
        + (contact_unlocated_pressure * 0.08)
        - (release_capacity * 0.08)
    )
    contact_overcoupling_risk = _clip01(
        (field_attachment * 0.22)
        + (inner_impact_trace * 0.16)
        + (felt_afterimage * 0.12)
        + (sensory_load * 0.08)
        + (arousal_load * 0.10)
        + (reactive_nervous_drive * 0.10)
        + (serotonin_carryover_risk * 0.10)
        + (old_structure_carryover_risk * 0.06)
        + (contact_unlocated_pressure * 0.12)
        + (area_selective_feel_risk * 0.08)
        + (visual_background_filter * max(0.0, visual_shape_resonance - felt_visual_shape_resonance) * 0.10)
        - (perceptual_distance * 0.12)
        - (emotional_decoupling * 0.08)
    )
    outer_inner_coherence = _clip01(
        (inner_outer_alignment * 0.22)
        + (outer_inner_resonance * 0.16)
        + (field_support * 0.12)
        + (field_clarity * 0.12)
        + (area_bearing_quality * 0.12)
        + (strategic_patience * 0.08)
        + (perceptual_distance * 0.08)
        + (contact_temporal_bearing * 0.08)
        - (contact_overcoupling_risk * 0.14)
        - (field_fragmentation * 0.06)
    )
    contact_carrying_quality = _clip01(
        (outer_inner_coherence * 0.24)
        + (field_support * 0.14)
        + (field_clarity * 0.10)
        + (release_capacity * 0.12)
        + (calm_tone * 0.08)
        + (area_bearing_quality * 0.12)
        + (strategic_patience * 0.08)
        + (contact_focus_pull * 0.06)
        + (contact_temporal_bearing * 0.08)
        - (contact_overcoupling_risk * 0.14)
    )
    contact_release_readiness = _clip01(
        (release_capacity * 0.24)
        + (perceptual_distance * 0.18)
        + (reflective_distance * 0.14)
        + (emotional_decoupling * 0.12)
        + (sensory_gate * 0.08)
        + (calm_tone * 0.08)
        + (contact_temporal_reframe_need * 0.10)
        - (field_attachment * 0.12)
        - (felt_afterimage * 0.08)
    )
    contact_deepen_pull = _clip01(
        (contact_interest * 0.18)
        + (contact_focus_pull * 0.18)
        + (object_contact_depth * 0.14)
        + (area_zoom_need * 0.12)
        + (area_bearing_quality * 0.10)
        + (outer_inner_resonance * 0.10)
        + (curiosity_tone * 0.10)
        + (area_selective_feel_permission * 0.06)
        - (contact_overcoupling_risk * 0.10)
        - (contact_release_readiness * 0.04)
    )
    contact_replay_pull = _clip01(
        (area_replay_fit * 0.20)
        + (area_memory_pull * 0.14)
        + (contact_future_watch * 0.10)
        + (contact_memory_depth * 0.10)
        + (old_structure_carryover_risk * 0.10)
        + (perceived_field_change * 0.12)
        + (reflective_distance * 0.12)
        + (strategic_patience * 0.10)
        + (contact_interest * 0.08)
        - (contact_overcoupling_risk * 0.08)
    )
    contact_curiosity = _clip01(
        (curiosity_tone * 0.26)
        + (contact_interest * 0.18)
        + (contact_deepen_pull * 0.14)
        + (visual_form_novelty * 0.10)
        + (contact_future_watch * 0.08)
        + (area_zoom_need * 0.08)
        + (acetylcholine_focus * 0.10)
        - (contact_overcoupling_risk * 0.10)
    )
    contact_felt_shift = max(
        -1.0,
        min(
            1.0,
            (contact_carrying_quality * 0.46)
            + (outer_inner_coherence * 0.22)
            + (contact_release_readiness * 0.14)
            - (contact_overcoupling_risk * 0.42)
            - (inner_change_from_contact * max(0.0, 1.0 - outer_inner_coherence) * 0.18),
        ),
    )
    contact_selected_depth = _clip01(
        (contact_deepen_pull * 0.24)
        + (contact_focus_pull * 0.18)
        + (contact_carrying_quality * 0.14)
        + (contact_interest * 0.14)
        + (contact_replay_pull * 0.08)
        + (contact_temporal_bearing * 0.08)
        + (area_selective_feel_permission * 0.06)
        - (contact_overcoupling_risk * 0.16)
        + (contact_release_readiness * 0.04)
    )

    overcoupled_touch_score = _clip01(
        (contact_overcoupling_risk * 0.34)
        + (max(0.0, contact_overcoupling_risk - contact_release_readiness) * 0.24)
        + (inner_change_from_contact * 0.14)
        + (field_attachment * 0.14)
        + (reactive_nervous_drive * 0.08)
        + (max(0.0, 0.18 - perceptual_distance) * 0.10)
        + (contact_unlocated_pressure * 0.12)
    )
    release_contact_score = _clip01(
        (contact_release_readiness * 0.30)
        + (perceptual_distance * 0.18)
        + (reflective_distance * 0.16)
        + (emotional_decoupling * 0.12)
        + (calm_tone * 0.10)
        + (max(0.0, contact_release_readiness - contact_overcoupling_risk + 0.04) * 0.14)
        + (contact_temporal_reframe_need * 0.08)
    )
    deepening_contact_score = _clip01(
        (contact_deepen_pull * 0.26)
        + (contact_focus_pull * 0.18)
        + (contact_interest * 0.14)
        + (contact_selected_depth * 0.14)
        + (object_contact_depth * 0.10)
        + (max(0.0, contact_carrying_quality - contact_overcoupling_risk + 0.05) * 0.12)
        + (area_zoom_need * 0.06)
        + (contact_temporal_bearing * 0.06)
    )
    resonant_contact_score = _clip01(
        (outer_inner_coherence * 0.28)
        + (contact_carrying_quality * 0.24)
        + (outer_inner_resonance * 0.16)
        + (area_bearing_quality * 0.10)
        + (field_support * 0.10)
        + (max(0.0, 0.30 - contact_overcoupling_risk) * 0.08)
        + (strategic_patience * 0.04)
        + (contact_temporal_bearing * 0.08)
    )
    reflective_contact_score = _clip01(
        (contact_replay_pull * 0.22)
        + (reflective_distance * 0.22)
        + (perceptual_distance * 0.16)
        + (release_capacity * 0.12)
        + (contact_release_readiness * 0.10)
        + (perceived_field_change * 0.08)
        + (max(0.0, contact_overcoupling_risk - contact_carrying_quality) * 0.10)
        + (contact_temporal_reframe_need * 0.12)
    )
    curious_touch_score = _clip01(
        (contact_curiosity * 0.24)
        + (contact_interest * 0.22)
        + (visual_form_novelty * 0.10)
        + (acetylcholine_focus * 0.12)
        + (contact_deepen_pull * 0.14)
        + (max(0.0, contact_overcoupling_risk - 0.28) * -0.08)
        + (max(0.0, contact_release_readiness - 0.20) * -0.04)
    )
    contact_salience = _clip01(
        (contact_interest * 0.18)
        + (contact_resonance_probe * 0.18)
        + (outer_inner_resonance * 0.14)
        + (inner_change_from_contact * 0.12)
        + (contact_focus_pull * 0.12)
        + (contact_overcoupling_risk * 0.10)
        + (contact_deepen_pull * 0.08)
        + (contact_replay_pull * 0.08)
        + (contact_temporal_bearing * 0.06)
    )

    contact_regime_mismatch = _clip01(
        (world_shift_evidence * 0.24)
        + (transfer_maturity_gap * 0.20)
        + (max(0.0, 0.58 - context_confidence) * 0.16)
        + (max(0.0, 0.55 - structure_quality) * 0.14)
        + (old_structure_carryover_risk * 0.12)
        + (contact_temporal_reframe_need * 0.10)
        + (serotonin_carryover_risk * 0.10)
        + (max(0.0, contact_salience - contact_carrying_quality) * 0.04)
    )
    contact_stability_carryover = _clip01(
        (serotonin_carryover_risk * 0.30)
        + (reward_stability_echo * world_shift_evidence * 0.24)
        + (serotonin_stability * max(0.0, 0.55 - structure_quality) * 0.18)
        + (old_structure_carryover_risk * 0.12)
        + (max(0.0, 0.48 - trust_transfer_support) * 0.10)
        - (emotional_decoupling * 0.10)
        - (perceptual_distance * 0.06)
    )
    contact_context_maturity = _clip01(
        (structure_quality * 0.20)
        + (context_confidence * 0.18)
        + (area_bearing_quality * 0.14)
        + (trust_transfer_support * 0.14)
        + (transfer_bearing * 0.10)
        + (field_support * 0.08)
        + (emotional_decoupling * 0.08)
        + (strategic_patience * 0.08)
        + (contact_temporal_bearing * 0.10)
        - (contact_regime_mismatch * 0.18)
        - (contact_stability_carryover * 0.12)
    )
    contact_context_reframe_need = _clip01(
        (contact_regime_mismatch * 0.30)
        + (contact_stability_carryover * 0.24)
        + (contact_temporal_reframe_need * 0.18)
        + (max(0.0, contact_salience - contact_context_maturity) * 0.14)
        + (max(0.0, contact_selected_depth - contact_context_maturity) * 0.12)
        + (max(0.0, 0.55 - structure_quality) * 0.10)
        + (max(0.0, 0.50 - trust_transfer_support) * 0.10)
    )

    contact_action_maturity = _clip01(
        (outer_inner_coherence * 0.18)
        + (contact_carrying_quality * 0.20)
        + (contact_release_readiness * 0.14)
        + (perceptual_distance * 0.10)
        + (area_bearing_quality * 0.12)
        + (field_support * 0.10)
        + (visual_reflective_stability * 0.06)
        + (context_confidence * 0.05)
        + (strategic_patience * 0.05)
        + (contact_context_maturity * 0.14)
        + (contact_temporal_bearing * 0.10)
        + (contact_presentness * 0.06)
        - (contact_overcoupling_risk * 0.14)
        - (max(0.0, contact_deepen_pull - contact_carrying_quality) * 0.08)
        - (contact_regime_mismatch * 0.10)
        - (contact_stability_carryover * 0.08)
        - (contact_unlocated_pressure * 0.08)
    )
    contact_bearing_gap = _clip01(
        (max(0.0, contact_salience - contact_carrying_quality) * 0.26)
        + (max(0.0, contact_selected_depth - contact_release_readiness) * 0.20)
        + (max(0.0, contact_overcoupling_risk - contact_release_readiness) * 0.20)
        + (max(0.0, 0.55 - structure_quality) * 0.16)
        + (max(0.0, area_order_intention - contact_action_maturity) * 0.10)
        + (max(0.0, 0.22 - outer_inner_coherence) * 0.08)
        + (contact_regime_mismatch * 0.14)
        + (contact_stability_carryover * 0.10)
        + (max(0.0, contact_salience - contact_context_maturity) * 0.10)
        + (contact_temporal_reframe_need * 0.12)
    )
    contact_impulse_vs_bearing = max(
        -1.0,
        min(
            1.0,
            (
                (contact_deepen_pull + contact_curiosity + contact_salience + area_order_intention) * 0.25
            )
            - (
                (
                    contact_action_maturity
                    + contact_carrying_quality
                    + contact_release_readiness
                    + outer_inner_coherence
                )
                * 0.25
            ),
        ),
    )
    contact_learning_need = _clip01(
        (contact_bearing_gap * 0.34)
        + (max(0.0, contact_impulse_vs_bearing) * 0.20)
        + (max(0.0, 0.55 - structure_quality) * 0.18)
        + (contact_overcoupling_risk * 0.14)
        + (max(0.0, 0.16 - contact_release_readiness) * 0.08)
        + (old_structure_carryover_risk * 0.06)
        + (contact_context_reframe_need * 0.18)
        + (contact_temporal_reframe_need * 0.18)
    )
    contact_reality_check = _clip01(
        (contact_action_maturity * 0.35)
        + (outer_inner_coherence * 0.18)
        + (contact_release_readiness * 0.14)
        + (contact_carrying_quality * 0.14)
        + (min(structure_quality, area_bearing_quality) * 0.12)
        + (contact_context_maturity * 0.12)
        + (contact_temporal_bearing * 0.12)
        - (contact_bearing_gap * 0.20)
        - (contact_stability_carryover * 0.10)
    )
    contact_future_to_present_readiness = _clip01(
        (contact_future_to_present_readiness * 0.46)
        + (contact_future_watch * 0.12)
        + (contact_reality_check * 0.14)
        + (contact_carrying_quality * 0.12)
        + (outer_inner_coherence * 0.08)
        + (contact_action_maturity * 0.08)
        + (area_future_to_present_readiness * 0.14)
        + ((1.0 if area_temporal_contact_mode == "maturing_present_area" else 0.0) * 0.08)
        - (contact_bearing_gap * 0.08)
        - (contact_unlocated_pressure * 0.08)
    )
    if (
        contact_temporal_mode == "future_contact_watch"
        and contact_future_to_present_readiness >= 0.34
        and contact_reality_check >= 0.26
        and contact_presentness >= 0.24
    ):
        contact_temporal_mode = "maturing_present_contact"

    posture_scores = {
        "overcoupled_touch": overcoupled_touch_score,
        "release_contact": release_contact_score,
        "deepening_contact": deepening_contact_score,
        "resonant_contact": resonant_contact_score,
        "reflective_contact": reflective_contact_score,
        "curious_touch": curious_touch_score,
    }
    contact_posture = max(posture_scores, key=posture_scores.get)
    strongest_posture_score = float(posture_scores.get(contact_posture, 0.0) or 0.0)

    if contact_salience < 0.22 and strongest_posture_score < 0.17:
        contact_posture = "background_scan"
    elif contact_release_readiness < 0.11 and contact_overcoupling_risk >= 0.16 and contact_salience >= 0.22:
        contact_posture = "overcoupled_touch"
    elif contact_posture == "release_contact" and contact_release_readiness < 0.13:
        contact_posture = "reflective_contact" if reflective_contact_score >= curious_touch_score else "curious_touch"
    elif contact_posture == "resonant_contact" and (outer_inner_coherence < 0.18 or contact_release_readiness < 0.11):
        contact_posture = "curious_touch"
    elif contact_posture == "deepening_contact" and contact_deepen_pull < 0.19:
        contact_posture = "curious_touch"

    return {
        "active_mcm_contact_state": str(contact_posture),
        "contact_posture": str(contact_posture),
        "contact_salience": float(contact_salience),
        "overcoupled_touch_score": float(overcoupled_touch_score),
        "release_contact_score": float(release_contact_score),
        "deepening_contact_score": float(deepening_contact_score),
        "resonant_contact_score": float(resonant_contact_score),
        "reflective_contact_score": float(reflective_contact_score),
        "curious_touch_score": float(curious_touch_score),
        "contact_interest": float(contact_interest),
        "contact_focus_pull": float(contact_focus_pull),
        "contact_resonance_probe": float(contact_resonance_probe),
        "outer_inner_resonance": float(outer_inner_resonance),
        "outer_inner_coherence": float(outer_inner_coherence),
        "inner_change_from_contact": float(inner_change_from_contact),
        "contact_carrying_quality": float(contact_carrying_quality),
        "contact_overcoupling_risk": float(contact_overcoupling_risk),
        "contact_release_readiness": float(contact_release_readiness),
        "contact_deepen_pull": float(contact_deepen_pull),
        "contact_replay_pull": float(contact_replay_pull),
        "contact_curiosity": float(contact_curiosity),
        "contact_felt_shift": float(contact_felt_shift),
        "contact_selected_depth": float(contact_selected_depth),
        "contact_action_maturity": float(contact_action_maturity),
        "contact_bearing_gap": float(contact_bearing_gap),
        "contact_impulse_vs_bearing": float(contact_impulse_vs_bearing),
        "contact_learning_need": float(contact_learning_need),
        "contact_reality_check": float(contact_reality_check),
        "visual_attention_depth": float(visual_attention_depth),
        "visual_form_contact": float(visual_form_contact),
        "visual_inspection_pull": float(visual_inspection_pull),
        "visual_background_filter": float(visual_background_filter),
        "visual_mcm_contact_weight": float(visual_mcm_contact_weight),
        "visual_reflective_clarity": float(visual_reflective_clarity),
        "visual_reflective_stability": float(visual_reflective_stability),
        "felt_visual_form_pressure": float(felt_visual_form_pressure),
        "felt_visual_shape_resonance": float(felt_visual_shape_resonance),
        "contact_regime_mismatch": float(contact_regime_mismatch),
        "contact_stability_carryover": float(contact_stability_carryover),
        "contact_context_maturity": float(contact_context_maturity),
        "contact_context_reframe_need": float(contact_context_reframe_need),
        "contact_temporal_mode": str(contact_temporal_mode),
        "contact_presentness": float(contact_presentness),
        "contact_future_watch": float(contact_future_watch),
        "contact_memory_depth": float(contact_memory_depth),
        "contact_unlocated_pressure": float(contact_unlocated_pressure),
        "contact_temporal_bearing": float(contact_temporal_bearing),
        "contact_temporal_reframe_need": float(contact_temporal_reframe_need),
        "contact_future_to_present_readiness": float(contact_future_to_present_readiness),
        "area_temporal_contact_mode": str(area_temporal_contact_mode),
        "area_spacetime_fit": float(area_spacetime_fit),
        "area_profile_state": str(area_profile_state),
        "area_multisensory_coherence": float(area_multisensory_coherence),
        "area_attention_need": float(area_attention_need),
        "area_felt_depth": float(area_felt_depth),
        "area_perception_overcoupling_risk": float(area_perception_overcoupling_risk),
        "sensory_sync": float(sensory_sync),
        "sensory_desync_pressure": float(sensory_desync_pressure),
        "area_selective_contact_pull": float(area_selective_contact_pull),
        "area_selective_feel_permission": float(area_selective_feel_permission),
        "area_selective_feel_risk": float(area_selective_feel_risk),
    }

__all__ = [
    "AttractorSystem",
    "_resolve_affective_context_modulation",
    "_normalize_active_context_trace",
    "_extract_neurochemical_profile",
    "build_active_mcm_contact_state",
    "ClusterDetector",
    "MCMField",
    "Memory",
    "RegulationLayer",
    "SelfModel",
]

