"""Inner-context cluster memory helpers.

This module carries DIO's inner context cluster formation and update logic.
Reward-delta calculation is injected to avoid coupling this module back into
the broader experience-space implementation.
"""

from __future__ import annotations

import numpy as np

from config import Config
from core.inner_pattern import (
    _build_inner_pattern_identity,
    _build_inner_pattern_identity_stability,
    _build_inner_pattern_recognition_state,
    _derive_inner_pattern_label,
)
from core.mcm_field import _extract_neurochemical_profile


def _build_inner_context_cluster_state(inner_field_state, summary_item, bot=None):

    field_state = dict(inner_field_state or {})
    summary = dict(summary_item or {})

    field_density = float(getattr(bot, "field_density", 0.0) or 0.0) if bot is not None else 0.0
    field_stability = float(getattr(bot, "field_stability", 0.0) or 0.0) if bot is not None else 0.0
    areal_stability_mean = float(field_state.get("field_areal_stability_mean", 0.0) or 0.0)
    areal_pressure_mean = float(field_state.get("field_areal_pressure_mean", 0.0) or 0.0)
    areal_dominance = float(field_state.get("field_areal_dominance", 0.0) or 0.0)
    areal_fragmentation = float(field_state.get("field_areal_fragmentation", 0.0) or 0.0)
    areal_coherence_mean = float(field_state.get("field_areal_coherence_mean", 0.0) or 0.0)
    areal_conflict_mean = float(field_state.get("field_areal_conflict_mean", 0.0) or 0.0)
    areal_topology_density_mean = float(field_state.get("field_areal_topology_density_mean", 0.0) or 0.0)
    areal_topology_span_mean = float(field_state.get("field_areal_topology_span_mean", 0.0) or 0.0)
    areal_topology_boundary_mean = float(field_state.get("field_areal_topology_boundary_mean", 0.0) or 0.0)
    processing_areal_tension = float(summary.get("processing_areal_tension", 0.0) or 0.0)
    processing_areal_support = float(summary.get("processing_areal_support", 0.0) or 0.0)
    thought_areal_pressure = float(summary.get("thought_areal_pressure", 0.0) or 0.0)
    thought_areal_support = float(summary.get("thought_areal_support", 0.0) or 0.0)
    felt_bearing_score = float(summary.get("felt_bearing_score", 0.0) or 0.0)
    felt_recovery_cost = float(summary.get("felt_recovery_cost", 0.0) or 0.0)
    field_topology_state = dict(field_state.get("field_topology_state", {}) or {})
    field_topology_layout_state = dict(field_state.get("field_topology_layout_state", {}) or {})
    field_topology_rows = int(field_state.get("field_topology_rows", field_topology_layout_state.get("topology_rows", 0)) or 0)
    field_topology_cols = int(field_state.get("field_topology_cols", field_topology_layout_state.get("topology_cols", 0)) or 0)
    field_topology_position_count = int(field_state.get("field_topology_position_count", field_topology_layout_state.get("topology_position_count", 0)) or 0)
    field_topology_neighbor_link_count = int(field_state.get("field_topology_neighbor_link_count", field_topology_layout_state.get("topology_neighbor_link_count", 0)) or 0)
    field_topology_neighbor_count_mean = float(field_state.get("field_topology_neighbor_count_mean", field_topology_layout_state.get("topology_neighbor_count_mean", 0.0)) or 0.0)
    field_topology_neighbor_count_max = int(field_state.get("field_topology_neighbor_count_max", field_topology_layout_state.get("topology_neighbor_count_max", 0)) or 0)
    field_topology_link_density = float(field_state.get("field_topology_link_density", field_topology_state.get("link_density", 0.0)) or 0.0)
    field_topology_distance_mean = float(field_state.get("field_topology_distance_mean", field_topology_state.get("topology_distance_mean", 0.0)) or 0.0)
    field_topology_coherence = float(field_state.get("field_topology_coherence", field_topology_state.get("topology_coherence", 0.0)) or 0.0)
    field_topology_tension = float(field_state.get("field_topology_tension", field_topology_state.get("topology_tension", 0.0)) or 0.0)
    field_perception_state = dict(field_state.get("field_perception_state", {}) or {})
    field_activity_island_count = int(field_state.get("field_activity_island_count", field_perception_state.get("activity_island_count", 0)) or 0)
    field_activity_island_mass_mean = float(field_state.get("field_activity_island_mass_mean", field_perception_state.get("activity_island_mass_mean", 0.0)) or 0.0)
    field_activity_island_mass_max = float(field_state.get("field_activity_island_mass_max", field_perception_state.get("activity_island_mass_max", 0.0)) or 0.0)
    field_activity_island_activation_mean = float(field_state.get("field_activity_island_activation_mean", field_perception_state.get("activity_island_activation_mean", 0.0)) or 0.0)
    field_activity_island_pressure_mean = float(field_state.get("field_activity_island_pressure_mean", field_perception_state.get("activity_island_pressure_mean", 0.0)) or 0.0)
    field_activity_island_coherence_mean = float(field_state.get("field_activity_island_coherence_mean", field_perception_state.get("activity_island_coherence_mean", 0.0)) or 0.0)
    field_activity_island_context_reactivation_mean = float(field_state.get("field_activity_island_context_reactivation_mean", field_perception_state.get("activity_island_context_reactivation_mean", 0.0)) or 0.0)
    field_activity_island_spread = float(field_state.get("field_activity_island_spread", field_perception_state.get("activity_island_spread", 0.0)) or 0.0)
    field_perception_focus = float(field_state.get("field_perception_focus", field_perception_state.get("field_perception_focus", 0.0)) or 0.0)
    field_perception_clarity = float(field_state.get("field_perception_clarity", field_perception_state.get("field_perception_clarity", field_activity_island_coherence_mean)) or 0.0)
    field_perception_stability = float(field_state.get("field_perception_stability", field_perception_state.get("field_perception_stability", field_activity_island_coherence_mean)) or 0.0)
    field_perception_fragmentation = float(field_state.get("field_perception_fragmentation", field_perception_state.get("field_perception_fragmentation", 0.0)) or 0.0)
    field_perception_strain = float(field_state.get("field_perception_strain", field_perception_state.get("field_perception_strain", field_activity_island_pressure_mean)) or 0.0)
    dominant_activity_island_id = str(field_state.get("dominant_activity_island_id", field_perception_state.get("dominant_activity_island_id", "-")) or "-")
    field_perception_label = str(field_state.get("field_perception_label", field_perception_state.get("field_perception_label", "quiet_field")) or "quiet_field")
    field_activity_islands = [
        dict(item or {})
        for item in list(field_state.get("field_activity_islands", field_perception_state.get("activity_islands", [])) or [])
        if isinstance(item, dict)
    ]
    neural_felt_state = dict(field_state.get("neural_felt_state", {}) or {})
    neural_felt_bearing = float(field_state.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", 0.0)) or 0.0)
    neural_felt_pressure = float(field_state.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", 0.0)) or 0.0)
    neural_felt_memory_resonance = float(neural_felt_state.get("neural_felt_memory_resonance", 0.0) or 0.0)
    neural_felt_context_reactivation = float(neural_felt_state.get("neural_felt_context_reactivation", 0.0) or 0.0)
    neural_felt_label = str(field_state.get("neural_felt_label", neural_felt_state.get("neural_felt_label", "quiet_neural_felt")) or "quiet_neural_felt")
    inner_field_history_state = dict(field_state.get("inner_field_history_state", {}) or {})
    inner_field_history_length = int(inner_field_history_state.get("inner_field_history_length", field_state.get("inner_field_history_length", 0)) or 0)
    inner_field_pressure_trend = float(inner_field_history_state.get("inner_field_pressure_trend", field_state.get("inner_field_pressure_trend", 0.0)) or 0.0)
    inner_field_bearing_trend = float(inner_field_history_state.get("inner_field_bearing_trend", field_state.get("inner_field_bearing_trend", 0.0)) or 0.0)
    inner_field_topology_tension_trend = float(inner_field_history_state.get("inner_field_topology_tension_trend", field_state.get("inner_field_topology_tension_trend", 0.0)) or 0.0)
    inner_field_memory_resonance_trend = float(inner_field_history_state.get("inner_field_memory_resonance_trend", field_state.get("inner_field_memory_resonance_trend", 0.0)) or 0.0)
    inner_field_history_label = str(inner_field_history_state.get("inner_field_history_label", field_state.get("inner_field_history_label", "stable_field_trace")) or "stable_field_trace")

    inner_pattern_support = max(
        0.0,
        min(
            1.0,
            (field_stability * 0.12)
            + (areal_stability_mean * 0.18)
            + (areal_coherence_mean * 0.16)
            + (areal_dominance * 0.08)
            + (field_perception_stability * 0.10)
            + (field_perception_focus * 0.06)
            + (processing_areal_support * 0.16)
            + (thought_areal_support * 0.14)
            + (felt_bearing_score * 0.16),
        ),
    )
    inner_pattern_conflict = max(
        0.0,
        min(
            1.0,
            (areal_pressure_mean * 0.16)
            + (areal_fragmentation * 0.18)
            + (areal_conflict_mean * 0.22)
            + (field_perception_fragmentation * 0.12)
            + (field_perception_strain * 0.10)
            + (processing_areal_tension * 0.16)
            + (thought_areal_pressure * 0.16)
            + (felt_recovery_cost * 0.12),
        ),
    )
    inner_pattern_fragility = max(0.0, min(1.0, inner_pattern_conflict - (inner_pattern_support * 0.42)))
    inner_pattern_bearing = max(0.0, min(1.0, inner_pattern_support - (inner_pattern_conflict * 0.46)))
    inner_pattern_state_pressures = {
        "conflicted": max(0.0, min(1.0, (inner_pattern_conflict * 0.34) + ((1.0 - inner_pattern_support) * 0.14))),
        "fragile": max(0.0, min(1.0, (inner_pattern_fragility * 0.36) + (inner_pattern_conflict * 0.08))),
        "supported": max(0.0, min(1.0, (inner_pattern_support * 0.34) + ((1.0 - inner_pattern_conflict) * 0.12))),
        "bearing": max(0.0, min(1.0, (inner_pattern_bearing * 0.30) + (inner_pattern_support * 0.12))),
    }
    inner_pattern_state = max(inner_pattern_state_pressures, key=inner_pattern_state_pressures.get)

    inner_pattern_label = _derive_inner_pattern_label(field_state, summary)

    state_payload = {
        "field_density": float(field_density),
        "field_stability": float(field_stability),
        "field_cluster_count": int(field_state.get("field_cluster_count", 0) or 0),
        "field_cluster_mass_mean": float(field_state.get("field_cluster_mass_mean", 0.0) or 0.0),
        "field_cluster_mass_max": float(field_state.get("field_cluster_mass_max", 0.0) or 0.0),
        "field_cluster_center_spread": float(field_state.get("field_cluster_center_spread", 0.0) or 0.0),
        "field_cluster_separation": float(field_state.get("field_cluster_separation", 0.0) or 0.0),
        "field_cluster_center_drift": float(field_state.get("field_cluster_center_drift", 0.0) or 0.0),
        "field_cluster_count_drift": float(field_state.get("field_cluster_count_drift", 0.0) or 0.0),
        "field_velocity_trend": float(field_state.get("field_velocity_trend", 0.0) or 0.0),
        "field_reorganization_direction": str(field_state.get("field_reorganization_direction", "stable") or "stable"),
        "field_mean_velocity": float(field_state.get("field_mean_velocity", 0.0) or 0.0),
        "field_regulation_pressure": float(field_state.get("field_regulation_pressure", 0.0) or 0.0),
        "field_neuron_count": int(field_state.get("field_neuron_count", 0) or 0),
        "field_neuron_activation_mean": float(field_state.get("field_neuron_activation_mean", 0.0) or 0.0),
        "field_neuron_activation_max": float(field_state.get("field_neuron_activation_max", 0.0) or 0.0),
        "field_neuron_stability_mean": float(field_state.get("field_neuron_stability_mean", 0.0) or 0.0),
        "field_neuron_regulation_pressure_mean": float(field_state.get("field_neuron_regulation_pressure_mean", 0.0) or 0.0),
        "field_neuron_memory_norm_mean": float(field_state.get("field_neuron_memory_norm_mean", 0.0) or 0.0),
        "field_neuron_coupling_norm_mean": float(field_state.get("field_neuron_coupling_norm_mean", 0.0) or 0.0),
        "field_neuron_regulation_force_norm_mean": float(field_state.get("field_neuron_regulation_force_norm_mean", 0.0) or 0.0),
        "field_neuron_external_impulse_norm_mean": float(field_state.get("field_neuron_external_impulse_norm_mean", 0.0) or 0.0),
        "field_neuron_context_memory_impulse_norm_mean": float(field_state.get("field_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0),
        "field_areal_count": int(field_state.get("field_areal_count", 0) or 0),
        "field_areal_activation_mean": float(field_state.get("field_areal_activation_mean", 0.0) or 0.0),
        "field_areal_stability_mean": float(field_state.get("field_areal_stability_mean", 0.0) or 0.0),
        "field_areal_pressure_mean": float(field_state.get("field_areal_pressure_mean", 0.0) or 0.0),
        "field_areal_drift": float(field_state.get("field_areal_drift", 0.0) or 0.0),
        "field_areal_dominance": float(field_state.get("field_areal_dominance", 0.0) or 0.0),
        "field_areal_fragmentation": float(field_state.get("field_areal_fragmentation", 0.0) or 0.0),
        "field_areal_coherence_mean": float(field_state.get("field_areal_coherence_mean", 0.0) or 0.0),
        "field_areal_conflict_mean": float(field_state.get("field_areal_conflict_mean", 0.0) or 0.0),
        "field_areal_topology_density_mean": float(areal_topology_density_mean),
        "field_areal_topology_span_mean": float(areal_topology_span_mean),
        "field_areal_topology_boundary_mean": float(areal_topology_boundary_mean),
        "field_topology_state": dict(field_topology_state or {}),
        "field_topology_layout_state": dict(field_topology_layout_state or {}),
        "field_topology_rows": int(field_topology_rows),
        "field_topology_cols": int(field_topology_cols),
        "field_topology_position_count": int(field_topology_position_count),
        "field_topology_neighbor_link_count": int(field_topology_neighbor_link_count),
        "field_topology_neighbor_count_mean": float(field_topology_neighbor_count_mean),
        "field_topology_neighbor_count_max": int(field_topology_neighbor_count_max),
        "field_topology_cluster_link_count": int(field_state.get("field_topology_cluster_link_count", field_topology_state.get("cluster_link_count", 0)) or 0),
        "field_topology_areal_link_count": int(field_state.get("field_topology_areal_link_count", field_topology_state.get("areal_link_count", 0)) or 0),
        "field_topology_link_density": float(field_topology_link_density),
        "field_topology_distance_mean": float(field_topology_distance_mean),
        "field_topology_coherence": float(field_topology_coherence),
        "field_topology_tension": float(field_topology_tension),
        "field_topology_state_label": str(field_state.get("field_topology_state_label", field_topology_state.get("topology_state_label", "sparse_topology")) or "sparse_topology"),
        "field_perception_state": dict(field_perception_state or {}),
        "field_activity_island_count": int(field_activity_island_count),
        "field_activity_island_mass_mean": float(field_activity_island_mass_mean),
        "field_activity_island_mass_max": float(field_activity_island_mass_max),
        "field_activity_island_activation_mean": float(field_activity_island_activation_mean),
        "field_activity_island_pressure_mean": float(field_activity_island_pressure_mean),
        "field_activity_island_coherence_mean": float(field_activity_island_coherence_mean),
        "field_activity_island_context_reactivation_mean": float(field_activity_island_context_reactivation_mean),
        "field_activity_island_spread": float(field_activity_island_spread),
        "field_perception_focus": float(field_perception_focus),
        "field_perception_clarity": float(field_perception_clarity),
        "field_perception_stability": float(field_perception_stability),
        "field_perception_fragmentation": float(field_perception_fragmentation),
        "field_perception_strain": float(field_perception_strain),
        "dominant_activity_island_id": str(dominant_activity_island_id),
        "field_perception_label": str(field_perception_label),
        "field_activity_islands": list(field_activity_islands or []),
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
        "inner_pattern_support": float(inner_pattern_support),
        "inner_pattern_conflict": float(inner_pattern_conflict),
        "inner_pattern_fragility": float(inner_pattern_fragility),
        "inner_pattern_bearing": float(inner_pattern_bearing),
        "inner_pattern_state": str(inner_pattern_state),
        "inner_pattern_state_pressures": dict(inner_pattern_state_pressures),
        "inner_pattern_label": str(inner_pattern_label),
        "inner_self_state": str(field_state.get("self_state", summary.get("self_state", "stable")) or "stable"),
        "inner_attractor": str(field_state.get("attractor", summary.get("attractor", "neutral")) or "neutral"),
    }

    inner_pattern_identity_state = _build_inner_pattern_identity(
        field_state,
        summary,
        state_payload=state_payload,
    )
    state_payload.update(dict(inner_pattern_identity_state or {}))
    inner_pattern_identity_stability_state = _build_inner_pattern_identity_stability(
        bot,
        inner_pattern_identity_state,
    )
    state_payload.update(dict(inner_pattern_identity_stability_state or {}))
    state_payload.update(
        _build_inner_pattern_recognition_state(
            state_payload,
        )
    )

    current_vector = [
        float(summary.get("in_trade_avg_regulatory_load", 0.0) or 0.0),
        float(summary.get("in_trade_avg_action_capacity", 0.0) or 0.0),
        float(summary.get("in_trade_avg_recovery_need", 0.0) or 0.0),
        float(summary.get("in_trade_avg_survival_pressure", 0.0) or 0.0),
        float(summary.get("in_trade_avg_pressure_to_capacity", 0.0) or 0.0),
        float(summary.get("in_trade_avg_pressure_release", 0.0) or 0.0),
        float(summary.get("in_trade_avg_load_bearing_capacity", 0.0) or 0.0),
        float(summary.get("in_trade_avg_state_stability", 0.0) or 0.0),
        float(summary.get("in_trade_avg_capacity_reserve", 0.0) or 0.0),
        float(summary.get("in_trade_avg_recovery_balance", 0.0) or 0.0),
        float(summary.get("in_trade_avg_regulated_courage", 0.0) or 0.0),
        float(summary.get("in_trade_avg_courage_gap", 0.0) or 0.0),
        float(summary.get("felt_bearing_score", 0.0) or 0.0),
        float(summary.get("focus_confidence", 0.0) or 0.0),
        float(summary.get("competition_bias", 0.0) or 0.0),
        float(state_payload.get("field_density", 0.0) or 0.0),
        float(state_payload.get("field_stability", 0.0) or 0.0),
        float(state_payload.get("field_cluster_count", 0.0) or 0.0),
        float(state_payload.get("field_cluster_mass_mean", 0.0) or 0.0),
        float(state_payload.get("field_cluster_mass_max", 0.0) or 0.0),
        float(state_payload.get("field_cluster_center_spread", 0.0) or 0.0),
        float(state_payload.get("field_cluster_separation", 0.0) or 0.0),
        float(state_payload.get("field_mean_velocity", 0.0) or 0.0),
        float(state_payload.get("field_regulation_pressure", 0.0) or 0.0),
        float(state_payload.get("field_neuron_count", 0.0) or 0.0),
        float(state_payload.get("field_neuron_activation_mean", 0.0) or 0.0),
        float(state_payload.get("field_neuron_activation_max", 0.0) or 0.0),
        float(state_payload.get("field_neuron_stability_mean", 0.0) or 0.0),
        float(state_payload.get("field_neuron_regulation_pressure_mean", 0.0) or 0.0),
        float(state_payload.get("field_neuron_memory_norm_mean", 0.0) or 0.0),
        float(state_payload.get("field_neuron_coupling_norm_mean", 0.0) or 0.0),
        float(state_payload.get("field_neuron_regulation_force_norm_mean", 0.0) or 0.0),
        float(state_payload.get("field_neuron_external_impulse_norm_mean", 0.0) or 0.0),
        float(state_payload.get("field_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0),
        float(state_payload.get("field_areal_count", 0.0) or 0.0),
        float(state_payload.get("field_areal_activation_mean", 0.0) or 0.0),
        float(state_payload.get("field_areal_stability_mean", 0.0) or 0.0),
        float(state_payload.get("field_areal_pressure_mean", 0.0) or 0.0),
        float(state_payload.get("field_areal_drift", 0.0) or 0.0),
        float(state_payload.get("field_areal_dominance", 0.0) or 0.0),
        float(state_payload.get("field_areal_fragmentation", 0.0) or 0.0),
        float(state_payload.get("field_areal_coherence_mean", 0.0) or 0.0),
        float(state_payload.get("field_areal_conflict_mean", 0.0) or 0.0),
        float(state_payload.get("field_areal_topology_density_mean", 0.0) or 0.0),
        float(state_payload.get("field_areal_topology_span_mean", 0.0) or 0.0),
        float(state_payload.get("field_areal_topology_boundary_mean", 0.0) or 0.0),
        float(state_payload.get("field_topology_rows", 0.0) or 0.0),
        float(state_payload.get("field_topology_cols", 0.0) or 0.0),
        float(state_payload.get("field_topology_position_count", 0.0) or 0.0),
        float(state_payload.get("field_topology_neighbor_link_count", 0.0) or 0.0),
        float(state_payload.get("field_topology_neighbor_count_mean", 0.0) or 0.0),
        float(state_payload.get("field_topology_neighbor_count_max", 0.0) or 0.0),
        float(state_payload.get("field_topology_cluster_link_count", 0.0) or 0.0),
        float(state_payload.get("field_topology_areal_link_count", 0.0) or 0.0),
        float(state_payload.get("field_topology_link_density", 0.0) or 0.0),
        float(state_payload.get("field_topology_distance_mean", 0.0) or 0.0),
        float(state_payload.get("field_topology_coherence", 0.0) or 0.0),
        float(state_payload.get("field_topology_tension", 0.0) or 0.0),
        float(state_payload.get("field_activity_island_count", 0.0) or 0.0),
        float(state_payload.get("field_activity_island_mass_mean", 0.0) or 0.0),
        float(state_payload.get("field_activity_island_mass_max", 0.0) or 0.0),
        float(state_payload.get("field_activity_island_activation_mean", 0.0) or 0.0),
        float(state_payload.get("field_activity_island_pressure_mean", 0.0) or 0.0),
        float(state_payload.get("field_activity_island_coherence_mean", 0.0) or 0.0),
        float(state_payload.get("field_activity_island_context_reactivation_mean", 0.0) or 0.0),
        float(state_payload.get("field_activity_island_spread", 0.0) or 0.0),
        float(state_payload.get("field_perception_focus", 0.0) or 0.0),
        float(state_payload.get("field_perception_clarity", 0.0) or 0.0),
        float(state_payload.get("field_perception_stability", 0.0) or 0.0),
        float(state_payload.get("field_perception_fragmentation", 0.0) or 0.0),
        float(state_payload.get("field_perception_strain", 0.0) or 0.0),
        float(state_payload.get("neural_felt_bearing", 0.0) or 0.0),
        float(state_payload.get("neural_felt_pressure", 0.0) or 0.0),
        float(state_payload.get("neural_felt_memory_resonance", 0.0) or 0.0),
        float(state_payload.get("neural_felt_context_reactivation", 0.0) or 0.0),
        float(state_payload.get("inner_field_pressure_trend", 0.0) or 0.0),
        float(state_payload.get("inner_field_bearing_trend", 0.0) or 0.0),
        float(state_payload.get("inner_field_topology_tension_trend", 0.0) or 0.0),
        float(state_payload.get("inner_field_memory_resonance_trend", 0.0) or 0.0),
        float(state_payload.get("inner_pattern_support", 0.0) or 0.0),
        float(state_payload.get("inner_pattern_conflict", 0.0) or 0.0),
        float(state_payload.get("inner_pattern_fragility", 0.0) or 0.0),
        float(state_payload.get("inner_pattern_bearing", 0.0) or 0.0),
        float(state_payload.get("inner_pattern_identity_confidence", 0.0) or 0.0),
        float(state_payload.get("inner_pattern_identity_stability", 0.0) or 0.0),
        float(max(0.0, min(1.0, float(state_payload.get("inner_pattern_identity_streak", 0.0) or 0.0) / max(2.0, float(getattr(Config, "MCM_INNER_PATTERN_IDENTITY_STABILITY_TICKS", 5) or 5))))),
        float(state_payload.get("inner_pattern_recognition_strength", 0.0) or 0.0),
        1.0 if bool(state_payload.get("inner_pattern_recognition_recurrent", False)) else 0.0,
        1.0 if bool(state_payload.get("inner_pattern_recognition_changed", False)) else 0.0,
    ]

    current_vector.extend(
        [
            float(value)
            for value in list(state_payload.get("field_pattern_vector", []) or [])
        ]
    )

    return {
        "state_payload": dict(state_payload or {}),
        "current_vector": list(current_vector or []),
    }


def _update_inner_context_cluster_memory(bot, summary, *, reward_delta_builder=None):

    if bot is None:
        return None

    summary_item = dict(summary or {})
    inner_context_clusters = dict(getattr(bot, "inner_context_clusters", {}) or {})
    inner_field_state = dict(getattr(bot, "inner_field_perception_state", {}) or {})
    signature_key = str(summary_item.get("signature_key", "") or "").strip()
    outcome_reason = str(summary_item.get("outcome_reason", "-") or "-").strip().lower()
    outcome_delta = float(reward_delta_builder(summary_item) if reward_delta_builder is not None else 0.0)
    neurochemical_profile = _extract_neurochemical_profile(summary_item)
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

    cluster_state = _build_inner_context_cluster_state(
        inner_field_state,
        summary_item,
        bot=bot,
    )
    state_payload = dict(cluster_state.get("state_payload", {}) or {})
    current_vector = list(cluster_state.get("current_vector", []) or [])
    current_array = np.asarray(current_vector, dtype=float)
    inner_pattern_support = float(state_payload.get("inner_pattern_support", 0.0) or 0.0)
    inner_pattern_conflict = float(state_payload.get("inner_pattern_conflict", 0.0) or 0.0)
    inner_pattern_fragility = float(state_payload.get("inner_pattern_fragility", 0.0) or 0.0)
    inner_pattern_bearing = float(state_payload.get("inner_pattern_bearing", 0.0) or 0.0)
    inner_pattern_state = str(state_payload.get("inner_pattern_state", "bearing") or "bearing")
    neural_felt_state = dict(state_payload.get("neural_felt_state", {}) or {})
    neural_felt_bearing = float(state_payload.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", 0.0)) or 0.0)
    neural_felt_pressure = float(state_payload.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", 0.0)) or 0.0)
    neural_felt_memory_resonance = float(state_payload.get("neural_felt_memory_resonance", neural_felt_state.get("neural_felt_memory_resonance", 0.0)) or 0.0)
    neural_felt_context_reactivation = float(state_payload.get("neural_felt_context_reactivation", neural_felt_state.get("neural_felt_context_reactivation", 0.0)) or 0.0)
    neural_felt_label = str(state_payload.get("neural_felt_label", neural_felt_state.get("neural_felt_label", "quiet_neural_felt")) or "quiet_neural_felt")
    inner_field_history_state = dict(state_payload.get("inner_field_history_state", {}) or {})
    inner_field_history_length = int(state_payload.get("inner_field_history_length", inner_field_history_state.get("inner_field_history_length", 0)) or 0)
    inner_field_pressure_trend = float(state_payload.get("inner_field_pressure_trend", inner_field_history_state.get("inner_field_pressure_trend", 0.0)) or 0.0)
    inner_field_bearing_trend = float(state_payload.get("inner_field_bearing_trend", inner_field_history_state.get("inner_field_bearing_trend", 0.0)) or 0.0)
    inner_field_topology_tension_trend = float(state_payload.get("inner_field_topology_tension_trend", inner_field_history_state.get("inner_field_topology_tension_trend", 0.0)) or 0.0)
    inner_field_memory_resonance_trend = float(state_payload.get("inner_field_memory_resonance_trend", inner_field_history_state.get("inner_field_memory_resonance_trend", 0.0)) or 0.0)
    inner_field_history_label = str(state_payload.get("inner_field_history_label", inner_field_history_state.get("inner_field_history_label", "stable_field_trace")) or "stable_field_trace")
    pattern_reinforcement = max(
        0.0,
        min(
            1.0,
            inner_pattern_support
            + max(0.0, outcome_delta)
            + (neuro_support * 0.14)
            - (inner_pattern_conflict * 0.52)
            - (neuro_strain * 0.10),
        ),
    )
    pattern_attenuation = max(
        0.0,
        min(
            1.0,
            inner_pattern_conflict
            + max(0.0, -outcome_delta)
            + (neuro_strain * 0.16)
            - (inner_pattern_support * 0.42)
            - (neuro_support * 0.06),
        ),
    )

    nearest_cluster_id = None
    nearest_cluster = None
    nearest_distance = None

    for cluster_id, item in inner_context_clusters.items():
        if not isinstance(item, dict):
            continue

        candidate_vector = list(item.get("center_vector", []) or [])
        if len(candidate_vector) != len(current_vector):
            continue

        candidate_array = np.asarray(candidate_vector, dtype=float)
        distance = float(np.mean(np.abs(current_array - candidate_array)))

        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_cluster_id = str(cluster_id)
            nearest_cluster = dict(item or {})

    match_threshold = float(getattr(Config, "MCM_INNER_CONTEXT_MATCH_THRESHOLD", 0.18) or 0.18)

    if nearest_cluster is None or nearest_distance is None or nearest_distance > match_threshold:
        bot.inner_context_cluster_seq = max(0, int(getattr(bot, "inner_context_cluster_seq", 0) or 0)) + 1
        nearest_cluster_id = f"inner_ctx_{int(bot.inner_context_cluster_seq)}"
        nearest_distance = 0.0
        nearest_cluster = {
            "cluster_id": str(nearest_cluster_id),
            "center_vector": [float(round(value, 4)) for value in current_array.tolist()],
            "variance": 0.0,
            "radius": 0.0,
            "seen": 0,
            "tp": 0,
            "sl": 0,
            "cancel": 0,
            "timeout": 0,
            "score": 0.0,
            "trust": 0.12,
            "age": 0,
            "signature_keys": [],
            "last_signature_key": None,
            "last_outcome": None,
            "last_distance": 0.0,
            "pattern_support_score": float(inner_pattern_support),
            "pattern_conflict_score": float(inner_pattern_conflict),
            "pattern_fragility_score": float(inner_pattern_fragility),
            "pattern_bearing_score": float(inner_pattern_bearing),
            "pattern_reinforcement": 0.0,
            "pattern_attenuation": 0.0,
            "experience_neurochemical_profile": dict(neurochemical_profile or {}),
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
            **dict(state_payload or {}),
        }
    else:
        seen = max(0, int(nearest_cluster.get("seen", 0) or 0))
        prior_vector = list(nearest_cluster.get("center_vector", []) or [])
        prior_array = np.asarray(prior_vector, dtype=float)

        alpha = max(0.10, min(0.28, 1.0 / max(1.0, float(seen + 1))))
        merged_center = (prior_array * (1.0 - alpha)) + (current_array * alpha)

        updated_distance = float(np.mean(np.abs(current_array - prior_array)))

        nearest_cluster["center_vector"] = [float(round(value, 4)) for value in merged_center.tolist()]
        nearest_cluster["variance"] = float(
            (float(nearest_cluster.get("variance", 0.0) or 0.0) * 0.78)
            + ((updated_distance ** 2) * 0.22)
        )
        nearest_cluster["radius"] = float(
            max(
                float(nearest_cluster.get("radius", 0.0) or 0.0) * 0.88,
                updated_distance,
            )
        )
        nearest_distance = float(updated_distance)

    nearest_cluster["seen"] = int(nearest_cluster.get("seen", 0) or 0) + 1
    nearest_cluster["score"] = float(
        max(
            -12.0,
            min(
                12.0,
                (float(nearest_cluster.get("score", 0.0) or 0.0) * 0.82) + outcome_delta,
            ),
        )
    )

    nearest_cluster["pattern_support_score"] = float(
        (float(nearest_cluster.get("pattern_support_score", 0.0) or 0.0) * 0.74)
        + (inner_pattern_support * 0.26)
    )
    nearest_cluster["pattern_conflict_score"] = float(
        (float(nearest_cluster.get("pattern_conflict_score", 0.0) or 0.0) * 0.74)
        + (inner_pattern_conflict * 0.26)
    )
    nearest_cluster["pattern_fragility_score"] = float(
        (float(nearest_cluster.get("pattern_fragility_score", 0.0) or 0.0) * 0.74)
        + (inner_pattern_fragility * 0.26)
    )
    nearest_cluster["pattern_bearing_score"] = float(
        (float(nearest_cluster.get("pattern_bearing_score", 0.0) or 0.0) * 0.74)
        + (inner_pattern_bearing * 0.26)
    )
    nearest_cluster["pattern_reinforcement"] = float(
        (float(nearest_cluster.get("pattern_reinforcement", 0.0) or 0.0) * 0.78)
        + (pattern_reinforcement * 0.22)
    )
    nearest_cluster["pattern_attenuation"] = float(
        (float(nearest_cluster.get("pattern_attenuation", 0.0) or 0.0) * 0.78)
        + (pattern_attenuation * 0.22)
    )
    for neuro_key, neuro_value in dict(neurochemical_profile or {}).items():
        value = float(neuro_value or 0.0)
        nearest_cluster[f"avg_{neuro_key}"] = float(
            (float(nearest_cluster.get(f"avg_{neuro_key}", 0.0) or 0.0) * 0.76)
            + (value * 0.24)
        )
        nearest_cluster[f"last_{neuro_key}"] = float(value)
    nearest_cluster["experience_neurochemical_profile"] = dict(neurochemical_profile or {})
    nearest_cluster["neurochemical_support"] = float(
        (float(nearest_cluster.get("neurochemical_support", 0.0) or 0.0) * 0.76)
        + (neuro_support * 0.24)
    )
    nearest_cluster["neurochemical_strain"] = float(
        (float(nearest_cluster.get("neurochemical_strain", 0.0) or 0.0) * 0.76)
        + (neuro_strain * 0.24)
    )

    prior_neural_felt_bearing = float(nearest_cluster.get("neural_felt_bearing", neural_felt_bearing) or 0.0)
    prior_neural_felt_pressure = float(nearest_cluster.get("neural_felt_pressure", neural_felt_pressure) or 0.0)
    prior_neural_felt_memory_resonance = float(nearest_cluster.get("neural_felt_memory_resonance", neural_felt_memory_resonance) or 0.0)
    prior_neural_felt_context_reactivation = float(nearest_cluster.get("neural_felt_context_reactivation", neural_felt_context_reactivation) or 0.0)

    trust_base = float(nearest_cluster.get("trust", 0.0) or 0.0)
    trust_shift = (
        (0.04 if outcome_delta >= 0.0 else -0.03)
        + (inner_pattern_support * 0.05)
        + (inner_pattern_bearing * 0.04)
        + (neuro_support * 0.025)
        - (inner_pattern_conflict * 0.06)
        - (inner_pattern_fragility * 0.04)
        - (neuro_strain * 0.035)
    )
    nearest_cluster["trust"] = float(
        min(
            1.0,
            max(
                0.0,
                (trust_base * 0.84) + 0.08 + trust_shift,
            ),
        )
    )
    nearest_cluster["age"] = 0
    nearest_cluster["last_signature_key"] = str(signature_key or nearest_cluster.get("last_signature_key") or "") or None
    nearest_cluster["last_outcome"] = str(outcome_reason or nearest_cluster.get("last_outcome") or "-") or None
    nearest_cluster["last_distance"] = float(nearest_distance)

    for key, value in dict(state_payload or {}).items():
        nearest_cluster[str(key)] = value

    nearest_cluster["neural_felt_state"] = dict(neural_felt_state or {})
    nearest_cluster["neural_felt_bearing"] = float((prior_neural_felt_bearing * 0.74) + (neural_felt_bearing * 0.26))
    nearest_cluster["neural_felt_pressure"] = float((prior_neural_felt_pressure * 0.74) + (neural_felt_pressure * 0.26))
    nearest_cluster["neural_felt_memory_resonance"] = float((prior_neural_felt_memory_resonance * 0.74) + (neural_felt_memory_resonance * 0.26))
    nearest_cluster["neural_felt_context_reactivation"] = float((prior_neural_felt_context_reactivation * 0.74) + (neural_felt_context_reactivation * 0.26))
    nearest_cluster["neural_felt_label"] = str(neural_felt_label)

    signature_keys = list(nearest_cluster.get("signature_keys", []) or [])
    if signature_key and signature_key not in signature_keys:
        signature_keys.append(str(signature_key))
    nearest_cluster["signature_keys"] = signature_keys[-24:]

    if outcome_reason == "tp_hit":
        nearest_cluster["tp"] = int(nearest_cluster.get("tp", 0) or 0) + 1
    elif outcome_reason == "sl_hit":
        nearest_cluster["sl"] = int(nearest_cluster.get("sl", 0) or 0) + 1
    elif "timeout" in outcome_reason:
        nearest_cluster["timeout"] = int(nearest_cluster.get("timeout", 0) or 0) + 1
    elif "cancel" in outcome_reason:
        nearest_cluster["cancel"] = int(nearest_cluster.get("cancel", 0) or 0) + 1

    inner_context_clusters[str(nearest_cluster_id)] = dict(nearest_cluster)
    bot.inner_context_clusters = dict(inner_context_clusters)
    bot.last_inner_context_cluster_id = str(nearest_cluster_id)
    bot.last_inner_context_cluster_key = str(signature_key or nearest_cluster_id)

    return {
        "cluster_id": str(nearest_cluster_id),
        "distance": float(nearest_distance),
        "seen": int(nearest_cluster.get("seen", 0) or 0),
        "score": float(nearest_cluster.get("score", 0.0) or 0.0),
        "trust": float(nearest_cluster.get("trust", 0.0) or 0.0),
        "variance": float(nearest_cluster.get("variance", 0.0) or 0.0),
        "radius": float(nearest_cluster.get("radius", 0.0) or 0.0),
        "tp": int(nearest_cluster.get("tp", 0) or 0),
        "sl": int(nearest_cluster.get("sl", 0) or 0),
        "cancel": int(nearest_cluster.get("cancel", 0) or 0),
        "timeout": int(nearest_cluster.get("timeout", 0) or 0),
        "field_density": float(nearest_cluster.get("field_density", 0.0) or 0.0),
        "field_stability": float(nearest_cluster.get("field_stability", 0.0) or 0.0),
        "field_cluster_count": int(nearest_cluster.get("field_cluster_count", 0) or 0),
        "field_cluster_mass_mean": float(nearest_cluster.get("field_cluster_mass_mean", 0.0) or 0.0),
        "field_cluster_mass_max": float(nearest_cluster.get("field_cluster_mass_max", 0.0) or 0.0),
        "field_cluster_center_spread": float(nearest_cluster.get("field_cluster_center_spread", 0.0) or 0.0),
        "field_cluster_separation": float(nearest_cluster.get("field_cluster_separation", 0.0) or 0.0),
        "field_cluster_center_drift": float(nearest_cluster.get("field_cluster_center_drift", 0.0) or 0.0),
        "field_cluster_count_drift": float(nearest_cluster.get("field_cluster_count_drift", 0.0) or 0.0),
        "field_velocity_trend": float(nearest_cluster.get("field_velocity_trend", 0.0) or 0.0),
        "field_reorganization_direction": str(nearest_cluster.get("field_reorganization_direction", "stable") or "stable"),
        "field_mean_velocity": float(nearest_cluster.get("field_mean_velocity", 0.0) or 0.0),
        "field_regulation_pressure": float(nearest_cluster.get("field_regulation_pressure", 0.0) or 0.0),
        "field_neuron_count": int(nearest_cluster.get("field_neuron_count", 0) or 0),
        "field_neuron_activation_mean": float(nearest_cluster.get("field_neuron_activation_mean", 0.0) or 0.0),
        "field_neuron_activation_max": float(nearest_cluster.get("field_neuron_activation_max", 0.0) or 0.0),
        "field_neuron_stability_mean": float(nearest_cluster.get("field_neuron_stability_mean", 0.0) or 0.0),
        "field_neuron_regulation_pressure_mean": float(nearest_cluster.get("field_neuron_regulation_pressure_mean", 0.0) or 0.0),
        "field_neuron_memory_norm_mean": float(nearest_cluster.get("field_neuron_memory_norm_mean", 0.0) or 0.0),
        "field_neuron_coupling_norm_mean": float(nearest_cluster.get("field_neuron_coupling_norm_mean", 0.0) or 0.0),
        "field_neuron_regulation_force_norm_mean": float(nearest_cluster.get("field_neuron_regulation_force_norm_mean", 0.0) or 0.0),
        "field_neuron_external_impulse_norm_mean": float(nearest_cluster.get("field_neuron_external_impulse_norm_mean", 0.0) or 0.0),
        "field_neuron_context_memory_impulse_norm_mean": float(nearest_cluster.get("field_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0),
        "field_areal_count": int(nearest_cluster.get("field_areal_count", 0) or 0),
        "field_areal_activation_mean": float(nearest_cluster.get("field_areal_activation_mean", 0.0) or 0.0),
        "field_areal_stability_mean": float(nearest_cluster.get("field_areal_stability_mean", 0.0) or 0.0),
        "field_areal_pressure_mean": float(nearest_cluster.get("field_areal_pressure_mean", 0.0) or 0.0),
        "field_areal_drift": float(nearest_cluster.get("field_areal_drift", 0.0) or 0.0),
        "field_areal_dominance": float(nearest_cluster.get("field_areal_dominance", 0.0) or 0.0),
        "field_areal_fragmentation": float(nearest_cluster.get("field_areal_fragmentation", 0.0) or 0.0),
        "field_areal_coherence_mean": float(nearest_cluster.get("field_areal_coherence_mean", 0.0) or 0.0),
        "field_areal_conflict_mean": float(nearest_cluster.get("field_areal_conflict_mean", 0.0) or 0.0),
        "field_areal_topology_density_mean": float(nearest_cluster.get("field_areal_topology_density_mean", 0.0) or 0.0),
        "field_areal_topology_span_mean": float(nearest_cluster.get("field_areal_topology_span_mean", 0.0) or 0.0),
        "field_areal_topology_boundary_mean": float(nearest_cluster.get("field_areal_topology_boundary_mean", 0.0) or 0.0),
        "field_topology_layout_state": dict(nearest_cluster.get("field_topology_layout_state", {}) or {}),
        "field_topology_rows": int(nearest_cluster.get("field_topology_rows", 0) or 0),
        "field_topology_cols": int(nearest_cluster.get("field_topology_cols", 0) or 0),
        "field_topology_position_count": int(nearest_cluster.get("field_topology_position_count", 0) or 0),
        "field_topology_neighbor_link_count": int(nearest_cluster.get("field_topology_neighbor_link_count", 0) or 0),
        "field_topology_neighbor_count_mean": float(nearest_cluster.get("field_topology_neighbor_count_mean", 0.0) or 0.0),
        "field_topology_neighbor_count_max": int(nearest_cluster.get("field_topology_neighbor_count_max", 0) or 0),
        "field_topology_cluster_link_count": int(nearest_cluster.get("field_topology_cluster_link_count", 0) or 0),
        "field_topology_areal_link_count": int(nearest_cluster.get("field_topology_areal_link_count", 0) or 0),
        "field_topology_link_density": float(nearest_cluster.get("field_topology_link_density", 0.0) or 0.0),
        "field_topology_distance_mean": float(nearest_cluster.get("field_topology_distance_mean", 0.0) or 0.0),
        "field_topology_coherence": float(nearest_cluster.get("field_topology_coherence", 0.0) or 0.0),
        "field_topology_tension": float(nearest_cluster.get("field_topology_tension", 0.0) or 0.0),
        "field_topology_state_label": str(nearest_cluster.get("field_topology_state_label", "sparse_topology") or "sparse_topology"),
        "field_perception_state": dict(nearest_cluster.get("field_perception_state", {}) or {}),
        "field_activity_island_count": int(nearest_cluster.get("field_activity_island_count", 0) or 0),
        "field_activity_island_mass_mean": float(nearest_cluster.get("field_activity_island_mass_mean", 0.0) or 0.0),
        "field_activity_island_mass_max": float(nearest_cluster.get("field_activity_island_mass_max", 0.0) or 0.0),
        "field_activity_island_activation_mean": float(nearest_cluster.get("field_activity_island_activation_mean", 0.0) or 0.0),
        "field_activity_island_pressure_mean": float(nearest_cluster.get("field_activity_island_pressure_mean", 0.0) or 0.0),
        "field_activity_island_coherence_mean": float(nearest_cluster.get("field_activity_island_coherence_mean", 0.0) or 0.0),
        "field_activity_island_context_reactivation_mean": float(nearest_cluster.get("field_activity_island_context_reactivation_mean", 0.0) or 0.0),
        "field_activity_island_spread": float(nearest_cluster.get("field_activity_island_spread", 0.0) or 0.0),
        "field_perception_focus": float(nearest_cluster.get("field_perception_focus", 0.0) or 0.0),
        "field_perception_clarity": float(nearest_cluster.get("field_perception_clarity", 0.0) or 0.0),
        "field_perception_stability": float(nearest_cluster.get("field_perception_stability", 0.0) or 0.0),
        "field_perception_fragmentation": float(nearest_cluster.get("field_perception_fragmentation", 0.0) or 0.0),
        "field_perception_strain": float(nearest_cluster.get("field_perception_strain", 0.0) or 0.0),
        "dominant_activity_island_id": str(nearest_cluster.get("dominant_activity_island_id", "-") or "-"),
        "field_perception_label": str(nearest_cluster.get("field_perception_label", "quiet_field") or "quiet_field"),
        "field_activity_islands": [dict(item or {}) for item in list(nearest_cluster.get("field_activity_islands", []) or []) if isinstance(item, dict)],
        "neural_felt_state": dict(nearest_cluster.get("neural_felt_state", {}) or {}),
        "neural_felt_bearing": float(nearest_cluster.get("neural_felt_bearing", 0.0) or 0.0),
        "neural_felt_pressure": float(nearest_cluster.get("neural_felt_pressure", 0.0) or 0.0),
        "neural_felt_memory_resonance": float(nearest_cluster.get("neural_felt_memory_resonance", 0.0) or 0.0),
        "neural_felt_context_reactivation": float(nearest_cluster.get("neural_felt_context_reactivation", 0.0) or 0.0),
        "neural_felt_label": str(nearest_cluster.get("neural_felt_label", "quiet_neural_felt") or "quiet_neural_felt"),
        "inner_field_history_state": dict(nearest_cluster.get("inner_field_history_state", {}) or {}),
        "inner_field_history_length": int(nearest_cluster.get("inner_field_history_length", 0) or 0),
        "inner_field_pressure_trend": float(nearest_cluster.get("inner_field_pressure_trend", 0.0) or 0.0),
        "inner_field_bearing_trend": float(nearest_cluster.get("inner_field_bearing_trend", 0.0) or 0.0),
        "inner_field_topology_tension_trend": float(nearest_cluster.get("inner_field_topology_tension_trend", 0.0) or 0.0),
        "inner_field_memory_resonance_trend": float(nearest_cluster.get("inner_field_memory_resonance_trend", 0.0) or 0.0),
        "inner_field_history_label": str(nearest_cluster.get("inner_field_history_label", "stable_field_trace") or "stable_field_trace"),
        "inner_pattern_support": float(nearest_cluster.get("inner_pattern_support", 0.0) or 0.0),
        "inner_pattern_conflict": float(nearest_cluster.get("inner_pattern_conflict", 0.0) or 0.0),
        "inner_pattern_fragility": float(nearest_cluster.get("inner_pattern_fragility", 0.0) or 0.0),
        "inner_pattern_bearing": float(nearest_cluster.get("inner_pattern_bearing", 0.0) or 0.0),
        "inner_pattern_state": str(nearest_cluster.get("inner_pattern_state", "bearing") or "bearing"),
        "pattern_support_score": float(nearest_cluster.get("pattern_support_score", 0.0) or 0.0),
        "pattern_conflict_score": float(nearest_cluster.get("pattern_conflict_score", 0.0) or 0.0),
        "pattern_fragility_score": float(nearest_cluster.get("pattern_fragility_score", 0.0) or 0.0),
        "pattern_bearing_score": float(nearest_cluster.get("pattern_bearing_score", 0.0) or 0.0),
        "pattern_reinforcement": float(nearest_cluster.get("pattern_reinforcement", 0.0) or 0.0),
        "pattern_attenuation": float(nearest_cluster.get("pattern_attenuation", 0.0) or 0.0),
        "experience_neurochemical_profile": dict(nearest_cluster.get("experience_neurochemical_profile", {}) or {}),
        "neurochemical_support": float(nearest_cluster.get("neurochemical_support", 0.0) or 0.0),
        "neurochemical_strain": float(nearest_cluster.get("neurochemical_strain", 0.0) or 0.0),
        "avg_experience_effect_score": float(nearest_cluster.get("avg_experience_effect_score", 0.0) or 0.0),
        "avg_confidence_signal": float(nearest_cluster.get("avg_confidence_signal", 0.0) or 0.0),
        "avg_stability_signal": float(nearest_cluster.get("avg_stability_signal", 0.0) or 0.0),
        "avg_discipline_signal": float(nearest_cluster.get("avg_discipline_signal", 0.0) or 0.0),
        "avg_chaos_penalty": float(nearest_cluster.get("avg_chaos_penalty", 0.0) or 0.0),
        "avg_variance_penalty": float(nearest_cluster.get("avg_variance_penalty", 0.0) or 0.0),
        "avg_overactivation_signal": float(nearest_cluster.get("avg_overactivation_signal", 0.0) or 0.0),
        "avg_overstrain_penalty": float(nearest_cluster.get("avg_overstrain_penalty", 0.0) or 0.0),
        "avg_carrying_capacity_delta": float(nearest_cluster.get("avg_carrying_capacity_delta", 0.0) or 0.0),
        "inner_pattern_label": str(nearest_cluster.get("inner_pattern_label", "") or ""),
        "field_pattern_signature": dict(nearest_cluster.get("field_pattern_signature", {}) or {}),
        "field_pattern_signature_key": str(nearest_cluster.get("field_pattern_signature_key", "") or ""),
        "field_pattern_vector": [float(value) for value in list(nearest_cluster.get("field_pattern_vector", []) or [])],
        "inner_pattern_identity": str(nearest_cluster.get("inner_pattern_identity", "") or ""),
        "inner_pattern_identity_label": str(nearest_cluster.get("inner_pattern_identity_label", "") or ""),
        "inner_pattern_identity_confidence": float(nearest_cluster.get("inner_pattern_identity_confidence", 0.0) or 0.0),
        "inner_pattern_identity_streak": int(nearest_cluster.get("inner_pattern_identity_streak", 0) or 0),
        "inner_pattern_identity_stability": float(nearest_cluster.get("inner_pattern_identity_stability", 0.0) or 0.0),
        "inner_pattern_identity_recurrent": bool(nearest_cluster.get("inner_pattern_identity_recurrent", False)),
        "inner_pattern_identity_changed": bool(nearest_cluster.get("inner_pattern_identity_changed", False)),
        "inner_pattern_identity_last_seen_tick": int(nearest_cluster.get("inner_pattern_identity_last_seen_tick", 0) or 0),
        "inner_pattern_recognition_state": dict(nearest_cluster.get("inner_pattern_recognition_state", {}) or {}),
        "inner_pattern_recognition_label": str(nearest_cluster.get("inner_pattern_recognition_label", "unsettled_inner_pattern") or "unsettled_inner_pattern"),
        "inner_pattern_recognition_strength": float(nearest_cluster.get("inner_pattern_recognition_strength", 0.0) or 0.0),
        "inner_pattern_recognition_recurrent": bool(nearest_cluster.get("inner_pattern_recognition_recurrent", False)),
        "inner_pattern_recognition_changed": bool(nearest_cluster.get("inner_pattern_recognition_changed", False)),
        "inner_self_state": str(nearest_cluster.get("inner_self_state", "stable") or "stable"),
        "inner_attractor": str(nearest_cluster.get("inner_attractor", "neutral") or "neutral"),
        "last_outcome": nearest_cluster.get("last_outcome"),
    }

