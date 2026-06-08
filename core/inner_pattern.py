"""Inner-pattern identity helpers.

This module carries DIO's internal field-pattern naming, recognition, and
stability tracking. It preserves the formulas from the Brain module.
"""

from __future__ import annotations

from config import Config


def _build_inner_pattern_recognition_state(identity_state):

    item = dict(identity_state or {})
    identity = str(item.get("inner_pattern_identity", item.get("field_pattern_signature_key", "")) or "").strip()
    confidence = max(0.0, min(1.0, float(item.get("inner_pattern_identity_confidence", 0.0) or 0.0)))
    stability = max(0.0, min(1.0, float(item.get("inner_pattern_identity_stability", 0.0) or 0.0)))
    streak = max(0, int(float(item.get("inner_pattern_identity_streak", 0) or 0)))
    recurrent = bool(item.get("inner_pattern_identity_recurrent", False))
    changed = bool(item.get("inner_pattern_identity_changed", False))
    stability_ticks = max(2, int(getattr(Config, "MCM_INNER_PATTERN_IDENTITY_STABILITY_TICKS", 5) or 5))
    streak_axis = max(0.0, min(1.0, float(streak) / float(stability_ticks)))

    recognition_strength = max(
        0.0,
        min(
            1.0,
            (confidence * 0.30)
            + (stability * 0.38)
            + (streak_axis * 0.22)
            + (0.10 if recurrent else 0.0)
            - (0.18 if changed else 0.0),
        ),
    )

    recognition_label_pressures = {
        "no_inner_pattern_identity": 1.0 if not identity else 0.0,
        "identity_shift": (0.62 if changed else 0.0) + ((1.0 - stability) * 0.10),
        "recurrent_inner_pattern": (stability * 0.34) + (streak_axis * 0.30) + (confidence * 0.18) + (0.10 if recurrent else 0.0),
        "forming_inner_pattern": (stability * 0.34) + (confidence * 0.18) + ((1.0 - streak_axis) * 0.08),
        "weak_inner_pattern": (confidence * 0.34) + ((1.0 - stability) * 0.14),
        "unsettled_inner_pattern": ((1.0 - stability) * 0.30) + ((1.0 - confidence) * 0.22) + (0.12 if identity else 0.0),
    }
    recognition_label = max(recognition_label_pressures, key=recognition_label_pressures.get)

    return {
        "inner_pattern_recognition_state": {
            "identity": str(identity),
            "recognition_label": str(recognition_label),
            "recognition_strength": float(recognition_strength),
            "stability": float(stability),
            "confidence": float(confidence),
            "streak": int(streak),
            "recurrent": bool(recurrent),
            "changed": bool(changed),
            "recognition_label_pressures": dict(recognition_label_pressures),
        },
        "inner_pattern_recognition_label": str(recognition_label),
        "inner_pattern_recognition_strength": float(recognition_strength),
        "inner_pattern_recognition_recurrent": bool(recurrent),
        "inner_pattern_recognition_changed": bool(changed),
    }


def _build_inner_pattern_identity_stability(bot, identity_state):

    item = dict(identity_state or {})
    identity = str(item.get("inner_pattern_identity", item.get("field_pattern_signature_key", "")) or "").strip()
    confidence = max(0.0, min(1.0, float(item.get("inner_pattern_identity_confidence", 0.0) or 0.0)))

    if not identity:
        return {
            "inner_pattern_identity_streak": 0,
            "inner_pattern_identity_stability": 0.0,
            "inner_pattern_identity_recurrent": False,
            "inner_pattern_identity_changed": False,
            "inner_pattern_identity_last_seen_tick": 0,
        }

    current_tick = int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0) if bot is not None else 0
    last_identity = str(getattr(bot, "last_inner_pattern_identity", "") or "").strip() if bot is not None else ""
    previous_streak = max(0, int(getattr(bot, "inner_pattern_identity_streak", 0) or 0)) if bot is not None else 0
    identity_changed = bool(last_identity and identity != last_identity)

    if identity == last_identity:
        streak = previous_streak + 1
    else:
        streak = 1

    stability_ticks = max(2, int(getattr(Config, "MCM_INNER_PATTERN_IDENTITY_STABILITY_TICKS", 5) or 5))
    streak_ratio = max(0.0, min(1.0, float(streak) / float(stability_ticks)))
    stability = max(0.0, min(1.0, (streak_ratio * 0.68) + (confidence * 0.32)))
    recurrent_pressure = max(0.0, min(1.0, (streak_ratio * 0.64) + (confidence * 0.36)))
    transient_pressure = max(0.0, min(1.0, (1.0 - streak_ratio) * 0.56 + (1.0 - confidence) * 0.18))
    recurrent = bool(recurrent_pressure > transient_pressure)

    if bot is not None:
        setattr(bot, "last_inner_pattern_identity", str(identity))
        setattr(bot, "inner_pattern_identity_streak", int(streak))
        setattr(bot, "inner_pattern_identity_last_seen_tick", int(current_tick))
        setattr(bot, "inner_pattern_identity_stability", float(stability))

    return {
        "inner_pattern_identity_streak": int(streak),
        "inner_pattern_identity_stability": float(stability),
        "inner_pattern_identity_recurrent": bool(recurrent),
        "inner_pattern_identity_recurrent_pressure": float(recurrent_pressure),
        "inner_pattern_identity_transient_pressure": float(transient_pressure),
        "inner_pattern_identity_changed": bool(identity_changed),
        "inner_pattern_identity_last_seen_tick": int(current_tick),
    }


def _build_inner_pattern_identity(inner_field_state, summary_item, state_payload=None):

    field_state = dict(inner_field_state or {})
    summary = dict(summary_item or {})
    payload = dict(state_payload or {})

    def _band(value, low=0.33, high=0.66):
        number = max(0.0, min(1.0, float(value or 0.0)))

        mid_center = (float(low) + float(high)) / 2.0
        half_width = max(1e-9, float(high) - float(low))
        band_pressures = {
            "low": max(0.0, 1.0 - (number / max(float(high), 1e-9))),
            "mid": max(0.0, 1.0 - (abs(number - mid_center) / half_width)),
            "high": max(0.0, (number - float(low)) / max(1.0 - float(low), 1e-9)),
        }
        label = max(band_pressures, key=band_pressures.get)
        axis = (band_pressures["mid"] + (band_pressures["high"] * 2.0)) / max(
            1e-9,
            band_pressures["low"] + band_pressures["mid"] + band_pressures["high"],
        )
        return label, axis

    field_density = float(payload.get("field_density", field_state.get("field_density", 0.0)) or 0.0)
    field_stability = float(payload.get("field_stability", field_state.get("field_stability", 0.0)) or 0.0)
    field_regulation_pressure = float(payload.get("field_regulation_pressure", field_state.get("field_regulation_pressure", 0.0)) or 0.0)
    field_neuron_activation_mean = float(payload.get("field_neuron_activation_mean", field_state.get("field_neuron_activation_mean", 0.0)) or 0.0)
    field_neuron_memory_norm_mean = float(payload.get("field_neuron_memory_norm_mean", field_state.get("field_neuron_memory_norm_mean", 0.0)) or 0.0)
    field_neuron_context_memory_impulse_norm_mean = float(payload.get("field_neuron_context_memory_impulse_norm_mean", field_state.get("field_neuron_context_memory_impulse_norm_mean", 0.0)) or 0.0)
    field_areal_coherence_mean = float(payload.get("field_areal_coherence_mean", field_state.get("field_areal_coherence_mean", 0.0)) or 0.0)
    field_areal_conflict_mean = float(payload.get("field_areal_conflict_mean", field_state.get("field_areal_conflict_mean", 0.0)) or 0.0)
    field_areal_topology_density_mean = float(payload.get("field_areal_topology_density_mean", field_state.get("field_areal_topology_density_mean", 0.0)) or 0.0)
    field_areal_topology_boundary_mean = float(payload.get("field_areal_topology_boundary_mean", field_state.get("field_areal_topology_boundary_mean", 0.0)) or 0.0)
    field_topology_coherence = float(payload.get("field_topology_coherence", field_state.get("field_topology_coherence", 0.0)) or 0.0)
    field_topology_tension = float(payload.get("field_topology_tension", field_state.get("field_topology_tension", 0.0)) or 0.0)
    field_activity_island_count = int(payload.get("field_activity_island_count", field_state.get("field_activity_island_count", 0)) or 0)
    field_activity_island_mass_mean = float(payload.get("field_activity_island_mass_mean", field_state.get("field_activity_island_mass_mean", 0.0)) or 0.0)
    field_activity_island_mass_max = float(payload.get("field_activity_island_mass_max", field_state.get("field_activity_island_mass_max", 0.0)) or 0.0)
    field_activity_island_activation_mean = float(payload.get("field_activity_island_activation_mean", field_state.get("field_activity_island_activation_mean", 0.0)) or 0.0)
    field_activity_island_pressure_mean = float(payload.get("field_activity_island_pressure_mean", field_state.get("field_activity_island_pressure_mean", 0.0)) or 0.0)
    field_activity_island_coherence_mean = float(payload.get("field_activity_island_coherence_mean", field_state.get("field_activity_island_coherence_mean", 0.0)) or 0.0)
    field_activity_island_context_reactivation_mean = float(payload.get("field_activity_island_context_reactivation_mean", field_state.get("field_activity_island_context_reactivation_mean", 0.0)) or 0.0)
    field_activity_island_spread = float(payload.get("field_activity_island_spread", field_state.get("field_activity_island_spread", 0.0)) or 0.0)
    field_perception_label = str(payload.get("field_perception_label", field_state.get("field_perception_label", "quiet_field")) or "quiet_field").strip().lower()
    neural_felt_bearing = float(payload.get("neural_felt_bearing", field_state.get("neural_felt_bearing", 0.0)) or 0.0)
    neural_felt_pressure = float(payload.get("neural_felt_pressure", field_state.get("neural_felt_pressure", 0.0)) or 0.0)
    neural_felt_memory_resonance = float(payload.get("neural_felt_memory_resonance", field_state.get("neural_felt_memory_resonance", 0.0)) or 0.0)
    inner_field_bearing_trend = float(payload.get("inner_field_bearing_trend", field_state.get("inner_field_bearing_trend", 0.0)) or 0.0)
    inner_field_pressure_trend = float(payload.get("inner_field_pressure_trend", field_state.get("inner_field_pressure_trend", 0.0)) or 0.0)
    inner_pattern_support = float(payload.get("inner_pattern_support", 0.0) or 0.0)
    inner_pattern_conflict = float(payload.get("inner_pattern_conflict", 0.0) or 0.0)
    inner_pattern_bearing = float(payload.get("inner_pattern_bearing", 0.0) or 0.0)
    inner_pattern_fragility = float(payload.get("inner_pattern_fragility", 0.0) or 0.0)
    field_cluster_count = int(payload.get("field_cluster_count", field_state.get("field_cluster_count", 0)) or 0)
    field_areal_count = int(payload.get("field_areal_count", field_state.get("field_areal_count", 0)) or 0)
    field_topology_position_count = int(payload.get("field_topology_position_count", field_state.get("field_topology_position_count", 0)) or 0)
    field_reorganization_direction = str(payload.get("field_reorganization_direction", field_state.get("field_reorganization_direction", "stable")) or "stable").strip().lower()
    inner_pattern_state = str(payload.get("inner_pattern_state", "bearing") or "bearing").strip().lower()
    inner_pattern_label = str(payload.get("inner_pattern_label", _derive_inner_pattern_label(field_state, summary)) or "").strip().lower()
    neural_felt_label = str(payload.get("neural_felt_label", field_state.get("neural_felt_label", "quiet_neural_felt")) or "quiet_neural_felt").strip().lower()
    inner_field_history_label = str(payload.get("inner_field_history_label", field_state.get("inner_field_history_label", "stable_field_trace")) or "stable_field_trace").strip().lower()

    density_band, density_axis = _band(field_density)
    stability_band, stability_axis = _band(field_stability)
    regulation_band, regulation_axis = _band(field_regulation_pressure)
    activation_band, activation_axis = _band(field_neuron_activation_mean)
    memory_band, memory_axis = _band(max(field_neuron_memory_norm_mean, field_neuron_context_memory_impulse_norm_mean))
    areal_coherence_band, areal_coherence_axis = _band(field_areal_coherence_mean)
    areal_conflict_band, areal_conflict_axis = _band(field_areal_conflict_mean)
    areal_topology_band, areal_topology_axis = _band(field_areal_topology_density_mean)
    areal_boundary_band, areal_boundary_axis = _band(field_areal_topology_boundary_mean)
    topology_coherence_band, topology_coherence_axis = _band(field_topology_coherence)
    topology_tension_band, topology_tension_axis = _band(field_topology_tension)
    island_mass_band, island_mass_axis = _band(max(field_activity_island_mass_mean, field_activity_island_mass_max))
    island_activation_band, island_activation_axis = _band(field_activity_island_activation_mean)
    island_pressure_band, island_pressure_axis = _band(field_activity_island_pressure_mean)
    island_coherence_band, island_coherence_axis = _band(field_activity_island_coherence_mean)
    island_context_band, island_context_axis = _band(field_activity_island_context_reactivation_mean)
    island_spread_band, island_spread_axis = _band(field_activity_island_spread)
    neural_bearing_band, neural_bearing_axis = _band(neural_felt_bearing)
    neural_pressure_band, neural_pressure_axis = _band(neural_felt_pressure)
    neural_memory_band, neural_memory_axis = _band(neural_felt_memory_resonance)
    pattern_support_band, pattern_support_axis = _band(inner_pattern_support)
    pattern_conflict_band, pattern_conflict_axis = _band(inner_pattern_conflict)
    pattern_bearing_band, pattern_bearing_axis = _band(inner_pattern_bearing)
    pattern_fragility_band, pattern_fragility_axis = _band(inner_pattern_fragility)

    history_balance_axis = max(-1.0, min(1.0, inner_field_bearing_trend - inner_field_pressure_trend))
    cluster_axis = max(0.0, min(1.0, float(field_cluster_count) / 6.0))
    areal_axis = max(0.0, min(1.0, float(field_areal_count) / 6.0))
    topology_presence_axis = 1.0 if field_topology_position_count > 0 else 0.0
    island_count_axis = max(0.0, min(1.0, float(field_activity_island_count) / 6.0))

    field_pattern_vector = [
        float(density_axis / 2.0),
        float(stability_axis / 2.0),
        float(regulation_axis / 2.0),
        float(activation_axis / 2.0),
        float(memory_axis / 2.0),
        float(areal_coherence_axis / 2.0),
        float(areal_conflict_axis / 2.0),
        float(areal_topology_axis / 2.0),
        float(areal_boundary_axis / 2.0),
        float(topology_coherence_axis / 2.0),
        float(topology_tension_axis / 2.0),
        float(island_count_axis),
        float(island_mass_axis / 2.0),
        float(island_activation_axis / 2.0),
        float(island_pressure_axis / 2.0),
        float(island_coherence_axis / 2.0),
        float(island_context_axis / 2.0),
        float(island_spread_axis / 2.0),
        float(neural_bearing_axis / 2.0),
        float(neural_pressure_axis / 2.0),
        float(neural_memory_axis / 2.0),
        float(pattern_support_axis / 2.0),
        float(pattern_conflict_axis / 2.0),
        float(pattern_bearing_axis / 2.0),
        float(pattern_fragility_axis / 2.0),
        float(history_balance_axis),
        float(cluster_axis),
        float(areal_axis),
        float(topology_presence_axis),
    ]

    signature_parts = [
        f"fd_{density_band}",
        f"fs_{stability_band}",
        f"rp_{regulation_band}",
        f"na_{activation_band}",
        f"mem_{memory_band}",
        f"acoh_{areal_coherence_band}",
        f"acon_{areal_conflict_band}",
        f"atop_{areal_topology_band}",
        f"abnd_{areal_boundary_band}",
        f"tcoh_{topology_coherence_band}",
        f"tten_{topology_tension_band}",
        f"fp_{field_perception_label}",
        f"icnt_{field_activity_island_count}",
        f"imass_{island_mass_band}",
        f"iact_{island_activation_band}",
        f"iprs_{island_pressure_band}",
        f"icoh_{island_coherence_band}",
        f"ictx_{island_context_band}",
        f"ispd_{island_spread_band}",
        f"nb_{neural_bearing_band}",
        f"np_{neural_pressure_band}",
        f"nm_{neural_memory_band}",
        f"ps_{pattern_support_band}",
        f"pc_{pattern_conflict_band}",
        f"pb_{pattern_bearing_band}",
        f"pf_{pattern_fragility_band}",
        f"org_{field_reorganization_direction}",
        f"ips_{inner_pattern_state}",
    ]
    signature_key = "::".join(signature_parts)
    identity_label = f"{inner_pattern_state}::{field_perception_label}::{neural_felt_label}::{inner_field_history_label}"
    identity_confidence = max(
        0.0,
        min(
            1.0,
            (topology_presence_axis * 0.14)
            + (max(0.0, min(1.0, field_stability)) * 0.12)
            + (max(0.0, min(1.0, field_areal_coherence_mean)) * 0.10)
            + (max(0.0, min(1.0, inner_pattern_bearing)) * 0.14)
            + (max(0.0, min(1.0, neural_felt_memory_resonance)) * 0.10)
            + (max(0.0, min(1.0, field_areal_topology_density_mean)) * 0.08)
            + (max(0.0, min(1.0, 1.0 - field_areal_conflict_mean)) * 0.08)
            + (max(0.0, min(1.0, 1.0 - field_topology_tension)) * 0.06)
            + (max(0.0, min(1.0, field_activity_island_coherence_mean)) * 0.08)
            + (max(0.0, min(1.0, field_activity_island_activation_mean)) * 0.05)
            + (max(0.0, min(1.0, field_activity_island_mass_max)) * 0.03)
            + (max(0.0, min(1.0, 1.0 - field_activity_island_pressure_mean)) * 0.02),
        ),
    )

    return {
        "field_pattern_signature": {
            "signature_key": str(signature_key),
            "signature_parts": [str(item) for item in list(signature_parts or [])],
            "pattern_label": str(inner_pattern_label),
            "identity_label": str(identity_label),
            "field_perception_label": str(field_perception_label),
            "field_pattern_vector": [float(round(value, 4)) for value in list(field_pattern_vector or [])],
        },
        "field_pattern_signature_key": str(signature_key),
        "field_pattern_vector": [float(round(value, 4)) for value in list(field_pattern_vector or [])],
        "inner_pattern_identity": str(f"inner_identity::{signature_key}"),
        "inner_pattern_identity_label": str(identity_label),
        "inner_pattern_identity_confidence": float(identity_confidence),
    }


def _derive_inner_pattern_label(inner_field_state, summary_item):

    field_state = dict(inner_field_state or {})
    summary = dict(summary_item or {})

    regulation_pressure = float(field_state.get("field_regulation_pressure", 0.0) or 0.0)
    field_stability = float(field_state.get("field_stability", 0.0) or 0.0)
    field_cluster_count = int(field_state.get("field_cluster_count", 0) or 0)
    reorganization_direction = str(field_state.get("field_reorganization_direction", "stable") or "stable").strip().lower()
    neuron_activation_mean = float(field_state.get("field_neuron_activation_mean", 0.0) or 0.0)
    neuron_stability_mean = float(field_state.get("field_neuron_stability_mean", 0.0) or 0.0)
    neuron_coupling_norm_mean = float(field_state.get("field_neuron_coupling_norm_mean", 0.0) or 0.0)
    neuron_external_impulse_norm_mean = float(field_state.get("field_neuron_external_impulse_norm_mean", 0.0) or 0.0)
    neuron_context_memory_impulse_norm_mean = float(field_state.get("field_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0)
    areal_count = int(field_state.get("field_areal_count", 0) or 0)
    areal_stability_mean = float(field_state.get("field_areal_stability_mean", 0.0) or 0.0)
    areal_pressure_mean = float(field_state.get("field_areal_pressure_mean", 0.0) or 0.0)
    areal_dominance = float(field_state.get("field_areal_dominance", 0.0) or 0.0)
    areal_fragmentation = float(field_state.get("field_areal_fragmentation", 0.0) or 0.0)
    areal_coherence_mean = float(field_state.get("field_areal_coherence_mean", 0.0) or 0.0)
    areal_conflict_mean = float(field_state.get("field_areal_conflict_mean", 0.0) or 0.0)
    competition_bias = abs(float(summary.get("competition_bias", 0.0) or 0.0))
    felt_label = str(summary.get("felt_label", summary.get("felt_profile_label", "mixed")) or "mixed").strip().lower()
    felt_bearing_score = float(summary.get("felt_bearing_score", 0.0) or 0.0)
    thought_state_maturity = float(summary.get("thought_state_maturity", 0.0) or 0.0)
    thought_decision_readiness = float(summary.get("thought_decision_readiness", 0.0) or 0.0)
    thought_areal_pressure = float(summary.get("thought_areal_pressure", 0.0) or 0.0)
    thought_areal_support = float(summary.get("thought_areal_support", 0.0) or 0.0)
    processing_areal_tension = float(summary.get("processing_areal_tension", 0.0) or 0.0)
    processing_areal_support = float(summary.get("processing_areal_support", 0.0) or 0.0)

    areal_support = max(
        0.0,
        min(
            1.0,
            (areal_stability_mean * 0.24)
            + (areal_coherence_mean * 0.22)
            + (areal_dominance * 0.10)
            + (processing_areal_support * 0.16)
            + (thought_areal_support * 0.14)
            + (felt_bearing_score * 0.14),
        ),
    )
    areal_conflict = max(
        0.0,
        min(
            1.0,
            (areal_pressure_mean * 0.18)
            + (areal_conflict_mean * 0.24)
            + (areal_fragmentation * 0.20)
            + (processing_areal_tension * 0.14)
            + (thought_areal_pressure * 0.14)
            + (competition_bias * 0.10),
        ),
    )

    pressure_band_pressures = {
        "critical_load": max(regulation_pressure, areal_pressure_mean, areal_conflict) * 0.58 + max(0.0, areal_conflict - areal_support) * 0.18,
        "elevated_load": ((regulation_pressure + areal_pressure_mean + areal_conflict) / 3.0) * 0.46,
        "regulated_load": max(0.0, 1.0 - max(regulation_pressure, areal_pressure_mean, areal_conflict)) * 0.44 + areal_support * 0.10,
    }
    pressure_band = max(pressure_band_pressures, key=pressure_band_pressures.get)

    organization_band_pressures = {
        "fragmented_field": areal_fragmentation * 0.44 + min(1.0, float(max(areal_count, field_cluster_count)) / 4.0) * 0.20,
        "conflicted_areal": areal_conflict * 0.48 + areal_fragmentation * 0.10,
        "supported_areal": areal_support * 0.44 + areal_dominance * 0.18,
        "dominant_areal": areal_dominance * 0.42 + max(0.0, 1.0 - min(1.0, float(areal_count) / 4.0)) * 0.12,
        "multi_cluster": min(1.0, float(max(field_cluster_count, areal_count)) / 4.0) * 0.42,
        "coherent_field": max(0.0, 1.0 - areal_fragmentation) * 0.28 + max(0.0, 1.0 - areal_conflict) * 0.20 + areal_support * 0.08,
    }
    organization_band = max(organization_band_pressures, key=organization_band_pressures.get)

    neuron_band_pressures = {
        "contested_neurons": areal_conflict_mean * 0.32 + competition_bias * 0.26 + neuron_coupling_norm_mean * 0.18,
        "memory_reactivated_neurons": neuron_context_memory_impulse_norm_mean * 0.46 + max(0.0, neuron_context_memory_impulse_norm_mean - neuron_external_impulse_norm_mean) * 0.20,
        "settled_neurons": neuron_stability_mean * 0.34 + field_stability * 0.24 + areal_support * 0.14,
        "activated_neurons": neuron_activation_mean * 0.42 + neuron_external_impulse_norm_mean * 0.22,
        "adaptive_neurons": max(0.0, 1.0 - max(areal_conflict_mean, competition_bias, neuron_external_impulse_norm_mean)) * 0.34 + neuron_stability_mean * 0.08,
    }
    neuron_band = max(neuron_band_pressures, key=neuron_band_pressures.get)

    bearing_band_pressures = {
        "fragile_bearing": (0.30 if felt_label in ("fragmented_conflict", "burdened") else 0.0) + areal_conflict * 0.38 + max(0.0, 1.0 - areal_support) * 0.10,
        "mature_bearing": thought_state_maturity * 0.34 + thought_decision_readiness * 0.26 + areal_support * 0.18,
        "recovering_bearing": areal_support * 0.36 + max(0.0, 1.0 - areal_conflict) * 0.18,
        "unclear_bearing": max(0.0, 1.0 - max(areal_support, thought_state_maturity, thought_decision_readiness)) * 0.34 + areal_conflict * 0.08,
    }
    bearing_band = max(bearing_band_pressures, key=bearing_band_pressures.get)

    return f"{pressure_band}::{organization_band}::{neuron_band}::{bearing_band}::{reorganization_direction}"

