# ==================================================
# core/experience_space.py
# Experience-Space helpers for DIO's MCM memory organization.
# ==================================================

import numpy as np

from config import Config
from core.mcm_field import _normalize_active_context_trace


def _clip01(value):
    try:
        value = float(value)
    except Exception:
        return 0.0
    return max(0.0, min(1.0, value))


def _experience_bearing_delta(summary):

    item = dict(summary or {})
    state_delta = dict(item.get("state_delta", {}) or {})
    field_delta = dict(state_delta.get("field", {}) or {})
    experience_delta = dict(state_delta.get("experience", {}) or {})

    delta_pressure = float(field_delta.get("regulatory_load", 0.0) or 0.0)
    delta_capacity = float(field_delta.get("action_capacity", 0.0) or 0.0)
    delta_recovery = float(field_delta.get("recovery_need", 0.0) or 0.0)
    delta_survival = float(field_delta.get("survival_pressure", 0.0) or 0.0)
    delta_release = float(experience_delta.get("pressure_release", 0.0) or 0.0)
    delta_bearing = float(experience_delta.get("load_bearing_capacity", 0.0) or 0.0)

    return float(
        (delta_capacity * 0.34)
        + (delta_release * 0.24)
        + (delta_bearing * 0.28)
        - (delta_pressure * 0.30)
        - (delta_recovery * 0.24)
        - (delta_survival * 0.26)
    )

# --------------------------------------------------
def build_experience_neurochemical_effect(summary):

    item = dict(summary or {})
    event_name = str(item.get("event_name", "") or "").strip().lower()
    outcome_reason = str(item.get("outcome_reason", "") or "").strip().lower()
    decision_tendency = str(item.get("decision_tendency", "hold") or "hold").strip().lower()
    plan_quality = float(item.get("plan_quality", 0.0) or 0.0)
    execution_quality = float(item.get("execution_quality", 0.0) or 0.0)
    risk_fit_quality = float(item.get("risk_fit_quality", 0.0) or 0.0)
    observation_quality = float(item.get("observation_quality", 0.0) or 0.0)
    correction_timing_quality = float(item.get("correction_timing_quality", 0.0) or 0.0)
    structural_bearing_quality = float(item.get("structural_bearing_quality", 0.0) or 0.0)
    review_score = float(item.get("review_score", 0.0) or 0.0)
    bearing_regulation_cost = float(item.get("bearing_regulation_cost", 0.0) or 0.0)
    relief_quality = float(item.get("relief_quality", 0.0) or 0.0)
    carrying_room = float(item.get("carrying_room", 0.0) or 0.0)
    felt_bearing = float(item.get("felt_bearing", 0.0) or 0.0)
    felt_regulation_quality = float(item.get("felt_regulation_quality", 0.0) or 0.0)
    felt_recovery_cost = float(item.get("felt_recovery_cost", 0.0) or 0.0)
    felt_burden = float(item.get("felt_burden", 0.0) or 0.0)
    felt_overactivation = float(item.get("felt_overactivation", 0.0) or 0.0)
    felt_confidence = float(item.get("felt_confidence", 0.0) or 0.0)
    felt_stability = float(item.get("felt_stability", 0.0) or 0.0)
    experience_friction_cost = float(item.get("experience_friction_cost", 0.0) or 0.0)
    experience_energy_cost = float(item.get("experience_energy_cost", 0.0) or 0.0)
    experience_bearing_room = float(item.get("experience_bearing_room", 0.0) or 0.0)
    in_trade_direction_stability = float(item.get("in_trade_direction_stability", 0.0) or 0.0)
    in_trade_avg_state_stability = float(item.get("in_trade_avg_state_stability", 0.0) or 0.0)
    in_trade_avg_action_capacity = float(item.get("in_trade_avg_action_capacity", 0.0) or 0.0)
    in_trade_avg_recovery_need = float(item.get("in_trade_avg_recovery_need", 0.0) or 0.0)
    in_trade_avg_survival_pressure = float(item.get("in_trade_avg_survival_pressure", 0.0) or 0.0)
    in_trade_avg_pressure_to_capacity = float(item.get("in_trade_avg_pressure_to_capacity", 0.0) or 0.0)
    in_trade_avg_load_bearing_capacity = float(item.get("in_trade_avg_load_bearing_capacity", 0.0) or 0.0)
    in_trade_max_mfe = float(item.get("in_trade_max_mfe", 0.0) or 0.0)
    in_trade_max_mae = float(item.get("in_trade_max_mae", 0.0) or 0.0)
    field_areal_stability_mean = float(item.get("field_areal_stability_mean", 0.0) or 0.0)
    field_areal_pressure_mean = float(item.get("field_areal_pressure_mean", 0.0) or 0.0)
    field_areal_dominance = float(item.get("field_areal_dominance", 0.0) or 0.0)
    field_areal_fragmentation = float(item.get("field_areal_fragmentation", 0.0) or 0.0)
    field_areal_coherence_mean = float(item.get("field_areal_coherence_mean", 0.0) or 0.0)
    field_areal_conflict_mean = float(item.get("field_areal_conflict_mean", 0.0) or 0.0)
    field_areal_drift = float(item.get("field_areal_drift", 0.0) or 0.0)
    field_neuron_context_memory_impulse_norm_mean = float(item.get("field_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0)
    processing_areal_tension = float(item.get("processing_areal_tension", 0.0) or 0.0)
    processing_areal_support = float(item.get("processing_areal_support", 0.0) or 0.0)
    thought_areal_pressure = float(item.get("thought_areal_pressure", 0.0) or 0.0)
    thought_areal_support = float(item.get("thought_areal_support", 0.0) or 0.0)
    field_perception_pressure = float(item.get("field_perception_pressure", item.get("inner_context_cluster_activity_island_pressure_mean", 0.0)) or 0.0)
    field_perception_support = float(item.get("field_perception_support", item.get("inner_context_cluster_activity_island_coherence_mean", 0.0)) or 0.0)
    field_perception_clarity = float(item.get("field_perception_clarity", item.get("inner_context_cluster_activity_island_coherence_mean", 0.0)) or 0.0)
    field_activity_island_spread = float(item.get("field_activity_island_spread", item.get("inner_context_cluster_activity_island_spread", 0.0)) or 0.0)
    field_perception_label = str(item.get("field_perception_label", item.get("inner_context_cluster_field_perception_label", "quiet_field")) or "quiet_field").strip().lower()
    active_context_trace = _normalize_active_context_trace(item.get("active_context_trace", {}) or {})
    active_context_activation = float(active_context_trace.get("activation", 0.0) or 0.0)
    active_context_support = float(active_context_trace.get("support", 0.0) or 0.0)
    active_context_conflict = float(active_context_trace.get("conflict", 0.0) or 0.0)
    active_context_bearing = float(active_context_trace.get("bearing", 0.0) or 0.0)
    active_context_reinforcement = float(active_context_trace.get("reinforcement", 0.0) or 0.0)
    active_context_attenuation = float(active_context_trace.get("attenuation", 0.0) or 0.0)
    active_context_balance = max(
        -1.0,
        min(
            1.0,
            (
                active_context_support
                + active_context_bearing
                + active_context_reinforcement
                - active_context_conflict
                - active_context_attenuation
            ) / 3.0,
        ),
    )
    active_context_support_effect = max(0.0, active_context_balance) * active_context_activation
    active_context_strain_effect = max(0.0, -active_context_balance) * active_context_activation
    episode_felt_summary = dict(item.get("episode_felt_summary", {}) or {})
    felt_areal_support = float(episode_felt_summary.get("areal_support", 0.0) or 0.0)
    felt_areal_conflict = float(episode_felt_summary.get("areal_conflict_pressure", 0.0) or 0.0)
    bearing_delta = float(_experience_bearing_delta(item) or 0.0)

    state_support = float(
        (bearing_delta * 0.24)
        + (structural_bearing_quality * 0.12)
        + (relief_quality * 0.10)
        + (carrying_room * 0.08)
        + (felt_bearing * 0.08)
        + (felt_regulation_quality * 0.08)
        + (review_score * 0.04)
        + (field_areal_stability_mean * 0.08)
        + (field_areal_coherence_mean * 0.06)
        + (field_areal_dominance * 0.04)
        + (felt_areal_support * 0.08)
        + (processing_areal_support * 0.06)
        + (thought_areal_support * 0.04)
        + (field_neuron_context_memory_impulse_norm_mean * active_context_support_effect * 0.10)
    )

    state_strain = float(
        (bearing_regulation_cost * 0.10)
        + (experience_friction_cost * 0.10)
        + (experience_energy_cost * 0.08)
        + (felt_recovery_cost * 0.08)
        + (felt_burden * 0.08)
        + (field_areal_pressure_mean * 0.06)
        + (field_areal_fragmentation * 0.06)
        + (field_areal_conflict_mean * 0.08)
        + (felt_areal_conflict * 0.08)
        + (processing_areal_tension * 0.06)
        + (thought_areal_pressure * 0.04)
        + (field_neuron_context_memory_impulse_norm_mean * active_context_strain_effect * 0.10)
    )

    state_effect_delta = float(state_support - state_strain)
    base_delta = float((state_support * 0.66) - (state_strain * 0.60))
    event_context_delta = 0.0
    process_quality = max(
        0.0,
        min(
            1.0,
            (plan_quality * 0.22)
            + (execution_quality * 0.18)
            + (risk_fit_quality * 0.18)
            + (structural_bearing_quality * 0.14)
            + (review_score * 0.10)
            + (correction_timing_quality * 0.08)
            + (observation_quality * 0.06)
            + (felt_regulation_quality * 0.04),
        ),
    )
    carrying_capacity_delta = float(
        (bearing_delta * 0.38)
        + (carrying_room * 0.18)
        + (experience_bearing_room * 0.14)
        + (in_trade_avg_load_bearing_capacity * 0.10)
        + (in_trade_avg_action_capacity * 0.10)
        - (in_trade_avg_recovery_need * 0.12)
        - (in_trade_avg_survival_pressure * 0.10)
    )
    relief_signal = max(
        0.0,
        min(
            1.0,
            (relief_quality * 0.30)
            + (max(0.0, bearing_delta) * 0.18)
            + (max(0.0, state_effect_delta) * 0.18)
            + (max(0.0, 1.0 - felt_burden) * 0.12)
            + (max(0.0, 1.0 - in_trade_avg_pressure_to_capacity / 2.0) * 0.10)
            + (field_perception_clarity * 0.12),
        ),
    )
    stability_signal = max(
        0.0,
        min(
            1.0,
            (field_areal_stability_mean * 0.20)
            + (field_areal_coherence_mean * 0.16)
            + (felt_stability * 0.14)
            + (in_trade_avg_state_stability * 0.12)
            + (in_trade_direction_stability * 0.10)
            + (processing_areal_support * 0.10)
            + (thought_areal_support * 0.08)
            + (field_perception_clarity * 0.10),
        ),
    )
    discipline_signal = max(
        0.0,
        min(
            1.0,
            (process_quality * 0.36)
            + (correction_timing_quality * 0.16)
            + (risk_fit_quality * 0.14)
            + (observation_quality * 0.10)
            + (max(0.0, 1.0 - bearing_regulation_cost) * 0.10)
            + (max(0.0, 1.0 - experience_friction_cost) * 0.08)
            + (0.06 if decision_tendency in ("observe", "replan", "hold") and event_name in ("observed_only", "withheld", "replanned", "abandoned") else 0.0),
        ),
    )
    chaos_penalty = max(
        0.0,
        min(
            1.0,
            (experience_friction_cost * 0.20)
            + (experience_energy_cost * 0.16)
            + (field_areal_fragmentation * 0.14)
            + (field_areal_conflict_mean * 0.12)
            + (field_activity_island_spread * 0.08)
            + (field_perception_pressure * 0.12)
            + (processing_areal_tension * 0.08)
            + (thought_areal_pressure * 0.06)
            + (0.04 if field_perception_label in ("fragmented_perception_field", "strained_field") else 0.0),
        ),
    )
    variance_penalty = max(
        0.0,
        min(
            1.0,
            (max(0.0, 1.0 - in_trade_direction_stability) * 0.20)
            + (max(0.0, 1.0 - field_areal_stability_mean) * 0.14)
            + (field_areal_drift * 0.12)
            + (field_areal_fragmentation * 0.14)
            + (abs(in_trade_max_mfe - in_trade_max_mae) * 0.08)
            + (field_activity_island_spread * 0.12)
            + (active_context_strain_effect * 0.10),
        ),
    )
    overstrain_penalty = max(
        0.0,
        min(
            1.0,
            (felt_recovery_cost * 0.18)
            + (felt_burden * 0.14)
            + (bearing_regulation_cost * 0.12)
            + (in_trade_avg_recovery_need * 0.14)
            + (in_trade_avg_survival_pressure * 0.10)
            + (min(1.0, in_trade_avg_pressure_to_capacity / 2.0) * 0.10)
            + (field_areal_pressure_mean * 0.10)
            + (field_perception_pressure * 0.12),
        ),
    )
    overactivation_signal = max(
        0.0,
        min(
            1.0,
            (felt_overactivation * 0.28)
            + (max(0.0, in_trade_max_mfe - in_trade_max_mae) * 0.08)
            + (max(0.0, 1.0 - process_quality) * 0.12)
            + (chaos_penalty * 0.18)
            + ((0.18 if outcome_reason == "tp_hit" else 0.0) * max(0.0, 1.0 - (process_quality / 0.42)))
            + ((0.10 if outcome_reason == "tp_hit" else 0.0) * min(1.0, variance_penalty / 0.46)),
        ),
    )
    profit_reward = 0.0
    if outcome_reason == "tp_hit":
        profit_reward = max(
            0.0,
            min(
                1.0,
                0.18
                + (process_quality * 0.24)
                + (risk_fit_quality * 0.16)
                + (stability_signal * 0.14)
                + (relief_signal * 0.10)
                - (chaos_penalty * 0.16)
                - (overactivation_signal * 0.10),
            ),
        )
    elif outcome_reason == "sl_hit":
        profit_reward = -max(
            0.0,
            min(
                1.0,
                0.16
                + ((1.0 - risk_fit_quality) * 0.18)
                + (overstrain_penalty * 0.12)
                + (chaos_penalty * 0.10)
                - (process_quality * 0.16)
                - (discipline_signal * 0.10),
            ),
        )
    elif outcome_reason in ("cancel", "timeout", "reward_too_small", "rr_too_low", "sl_distance_too_high"):
        profit_reward = max(-0.12, min(0.12, (discipline_signal * 0.10) + (relief_signal * 0.06) - (overstrain_penalty * 0.08)))

    confidence_signal = max(
        0.0,
        min(
            1.0,
            (discipline_signal * 0.22)
            + (stability_signal * 0.20)
            + (max(0.0, profit_reward) * 0.16)
            + (felt_confidence * 0.12)
            + (max(0.0, carrying_capacity_delta) * 0.12)
            + (field_perception_support * 0.08)
            - (variance_penalty * 0.14)
            - (chaos_penalty * 0.12),
        ),
    )
    self_confidence_delta = float(
        (confidence_signal * 0.16)
        + (discipline_signal * 0.08)
        + (max(0.0, profit_reward) * 0.06)
        - (variance_penalty * 0.10)
        - (overactivation_signal * 0.08)
        - (max(0.0, -profit_reward) * 0.06)
    )

    if event_name in ("observed_only", "withheld", "replanned", "abandoned"):
        event_context_delta += (observation_quality * 0.04) + (correction_timing_quality * 0.03)
        if decision_tendency in ("observe", "replan", "hold"):
            event_context_delta += max(0.0, state_effect_delta) * 0.025

    elif event_name == "submitted":
        event_context_delta += (plan_quality * 0.015) + max(0.0, state_effect_delta) * 0.015

    elif event_name == "filled":
        event_context_delta += (execution_quality * 0.015) + max(0.0, state_effect_delta) * 0.015

    elif event_name in ("pending_update", "position_update", "in_trade_update", "monitor_update"):
        event_context_delta += (execution_quality * 0.015) + (risk_fit_quality * 0.015)
        event_context_delta += max(-0.015, min(0.015, state_effect_delta * 0.025))

    if outcome_reason == "tp_hit":
        event_context_delta += max(0.0, state_effect_delta) * 0.045
        event_context_delta += (plan_quality * 0.01) + (execution_quality * 0.01)

    elif outcome_reason == "sl_hit":
        event_context_delta -= max(0.0, -state_effect_delta) * 0.045
        event_context_delta -= ((1.0 - risk_fit_quality) * 0.012) + (bearing_regulation_cost * 0.010)

    elif outcome_reason in ("cancel", "timeout", "reward_too_small", "rr_too_low", "sl_distance_too_high"):
        event_context_delta += (correction_timing_quality * 0.025) + (observation_quality * 0.020)
        event_context_delta += max(-0.018, min(0.018, state_effect_delta * 0.030))

    effect_upper_bound = 0.28
    effect_lower_bound = -0.28

    if outcome_reason == "sl_hit":
        effect_upper_bound = max(
            -0.02,
            min(
                0.16,
                0.04
                + (discipline_signal * 0.06)
                + (stability_signal * 0.05)
                + (risk_fit_quality * 0.03)
                - (chaos_penalty * 0.05)
                - (overstrain_penalty * 0.04),
            ),
        )
    elif outcome_reason in ("cancel", "timeout", "reward_too_small", "rr_too_low", "sl_distance_too_high"):
        effect_upper_bound = max(
            0.02,
            min(
                0.18,
                0.05
                + (discipline_signal * 0.06)
                + (observation_quality * 0.04)
                + (relief_signal * 0.03)
                - (chaos_penalty * 0.04),
            ),
        )

    experience_effect_score = float(
        max(
            effect_lower_bound,
            min(
                effect_upper_bound,
                (base_delta * 0.46)
                + (profit_reward * 0.16)
                + (relief_signal * 0.06)
                + (stability_signal * 0.06)
                + (discipline_signal * 0.07)
                + (confidence_signal * 0.05)
                + (carrying_capacity_delta * 0.12)
                + (self_confidence_delta * 0.06)
                + event_context_delta
                - (chaos_penalty * 0.08)
                - (variance_penalty * 0.06)
                - (overstrain_penalty * 0.08)
                - (overactivation_signal * 0.05),
            ),
        )
    )

    return {
        "profit_reward": float(profit_reward),
        "relief_signal": float(relief_signal),
        "stability_signal": float(stability_signal),
        "discipline_signal": float(discipline_signal),
        "confidence_signal": float(confidence_signal),
        "overactivation_signal": float(overactivation_signal),
        "chaos_penalty": float(chaos_penalty),
        "variance_penalty": float(variance_penalty),
        "overstrain_penalty": float(overstrain_penalty),
        "carrying_capacity_delta": float(carrying_capacity_delta),
        "self_confidence_delta": float(max(-0.28, min(0.28, self_confidence_delta))),
        "process_quality": float(process_quality),
        "state_support": float(state_support),
        "state_strain": float(state_strain),
        "state_effect_delta": float(state_effect_delta),
        "event_context_delta": float(event_context_delta),
        "effect_upper_bound": float(effect_upper_bound),
        "effect_lower_bound": float(effect_lower_bound),
        "experience_effect_score": float(experience_effect_score),
    }

# --------------------------------------------------
def _experience_reward_delta(summary):

    effect = build_experience_neurochemical_effect(summary)
    return float(dict(effect or {}).get("experience_effect_score", 0.0) or 0.0)

# --------------------------------------------------
def _build_experience_similarity_axes(summary):

    item = dict(summary or {})
    decision_tendency = str(item.get("decision_tendency", "hold") or "hold").strip().lower()
    proposed_decision = str(item.get("proposed_decision", "WAIT") or "WAIT").strip().upper()
    state_delta = dict(item.get("state_delta", {}) or {})
    tension_delta = dict(state_delta.get("tension", {}) or {})
    field_delta = dict(state_delta.get("field", {}) or {})
    experience_delta = dict(state_delta.get("experience", {}) or {})

    direction_value = 0.0
    if proposed_decision == "LONG":
        direction_value = 1.0
    elif proposed_decision == "SHORT":
        direction_value = -1.0

    tendency_value = {
        "act": 1.0,
        "replan": 0.35,
        "observe": -0.35,
        "hold": -0.15,
    }.get(decision_tendency, 0.0)

    pressure_delta = float(field_delta.get("regulatory_load", 0.0) or 0.0)
    capacity_delta = float(field_delta.get("action_capacity", 0.0) or 0.0)
    recovery_delta = float(field_delta.get("recovery_need", 0.0) or 0.0)
    survival_delta = float(field_delta.get("survival_pressure", 0.0) or 0.0)
    areal_pressure_delta = float(field_delta.get("field_areal_pressure_mean", 0.0) or 0.0)
    areal_stability_delta = float(field_delta.get("field_areal_stability_mean", 0.0) or 0.0)
    areal_drift_delta = float(field_delta.get("field_areal_drift", 0.0) or 0.0)
    areal_dominance_delta = float(field_delta.get("field_areal_dominance", 0.0) or 0.0)
    areal_fragmentation_delta = float(field_delta.get("field_areal_fragmentation", 0.0) or 0.0)
    areal_conflict_delta = float(field_delta.get("field_areal_conflict_mean", 0.0) or 0.0)
    release_delta = float(experience_delta.get("pressure_release", 0.0) or 0.0)
    bearing_delta = float(experience_delta.get("load_bearing_capacity", 0.0) or 0.0)
    bearing_effect = float(_experience_bearing_delta(item) or 0.0)
    packet_bearing_quality = float(item.get("packet_bearing_quality", 0.0) or 0.0)
    packet_inner_outer_fit = float(item.get("packet_inner_outer_fit", 0.0) or 0.0)
    packet_confidence_integrity = float(item.get("packet_confidence_integrity", 0.0) or 0.0)
    packet_repetition_potential = float(item.get("packet_repetition_potential", 0.0) or 0.0)
    packet_curiosity_pull = float(item.get("packet_curiosity_pull", 0.0) or 0.0)
    packet_process_reward = float(item.get("packet_process_reward", 0.0) or 0.0)
    packet_reorganization_need = float(item.get("packet_reorganization_need", 0.0) or 0.0)
    constructive_stimulation = float(item.get("constructive_stimulation", 0.0) or 0.0)

    field_areal_fragmentation = float(item.get("field_areal_fragmentation", 0.0) or 0.0)
    field_areal_conflict_mean = float(item.get("field_areal_conflict_mean", 0.0) or 0.0)
    field_areal_dominance = float(item.get("field_areal_dominance", 0.0) or 0.0)
    field_areal_stability_mean = float(item.get("field_areal_stability_mean", 0.0) or 0.0)
    field_areal_coherence_mean = float(item.get("field_areal_coherence_mean", 0.0) or 0.0)
    processing_areal_tension = float(item.get("processing_areal_tension", 0.0) or 0.0)
    processing_areal_support = float(item.get("processing_areal_support", 0.0) or 0.0)
    thought_areal_pressure = float(item.get("thought_areal_pressure", 0.0) or 0.0)
    thought_areal_support = float(item.get("thought_areal_support", 0.0) or 0.0)
    field_neuron_context_memory_impulse_norm_mean = float(item.get("field_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0)
    neural_felt_state = dict(item.get("neural_felt_state", {}) or {})
    neural_felt_bearing = float(item.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", 0.0)) or 0.0)
    neural_felt_pressure = float(item.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", 0.0)) or 0.0)
    neural_felt_memory_resonance = float(item.get("neural_felt_memory_resonance", neural_felt_state.get("neural_felt_memory_resonance", 0.0)) or 0.0)
    neural_felt_context_reactivation = float(item.get("neural_felt_context_reactivation", neural_felt_state.get("neural_felt_context_reactivation", 0.0)) or 0.0)
    active_context_trace = _normalize_active_context_trace(item.get("active_context_trace", {}) or {})
    active_context_activation = float(active_context_trace.get("activation", 0.0) or 0.0)
    active_context_balance = float(
        active_context_trace.get("support", 0.0)
        + active_context_trace.get("bearing", 0.0)
        + active_context_trace.get("reinforcement", 0.0)
        - active_context_trace.get("conflict", 0.0)
        - active_context_trace.get("attenuation", 0.0)
    )
    inner_field_history_state = dict(item.get("inner_field_history_state", {}) or {})
    inner_field_pressure_trend = float(item.get("inner_field_pressure_trend", item.get("inner_context_cluster_pressure_trend", inner_field_history_state.get("inner_field_pressure_trend", 0.0))) or 0.0)
    inner_field_bearing_trend = float(item.get("inner_field_bearing_trend", item.get("inner_context_cluster_bearing_trend", inner_field_history_state.get("inner_field_bearing_trend", 0.0))) or 0.0)
    inner_field_topology_tension_trend = float(item.get("inner_field_topology_tension_trend", item.get("inner_context_cluster_topology_tension_trend", inner_field_history_state.get("inner_field_topology_tension_trend", 0.0))) or 0.0)
    inner_field_memory_resonance_trend = float(item.get("inner_field_memory_resonance_trend", item.get("inner_context_cluster_memory_resonance_trend", inner_field_history_state.get("inner_field_memory_resonance_trend", 0.0))) or 0.0)
    active_context_pressure_trend = float(active_context_trace.get("inner_field_pressure_trend", 0.0) or 0.0)
    active_context_bearing_trend = float(active_context_trace.get("inner_field_bearing_trend", 0.0) or 0.0)
    active_context_topology_tension_trend = float(active_context_trace.get("inner_field_topology_tension_trend", 0.0) or 0.0)
    active_context_memory_resonance_trend = float(active_context_trace.get("inner_field_memory_resonance_trend", 0.0) or 0.0)
    field_topology_layout_state = dict(item.get("field_topology_layout_state", {}) or {})
    field_topology_rows = float(item.get("field_topology_rows", item.get("inner_context_cluster_topology_rows", field_topology_layout_state.get("topology_rows", 0.0))) or 0.0)
    field_topology_cols = float(item.get("field_topology_cols", item.get("inner_context_cluster_topology_cols", field_topology_layout_state.get("topology_cols", 0.0))) or 0.0)
    field_topology_position_count = float(item.get("field_topology_position_count", item.get("inner_context_cluster_topology_position_count", field_topology_layout_state.get("topology_position_count", 0.0))) or 0.0)
    field_topology_neighbor_link_count = float(item.get("field_topology_neighbor_link_count", item.get("inner_context_cluster_topology_neighbor_link_count", field_topology_layout_state.get("topology_neighbor_link_count", 0.0))) or 0.0)
    field_topology_neighbor_count_mean = float(item.get("field_topology_neighbor_count_mean", item.get("inner_context_cluster_topology_neighbor_count_mean", field_topology_layout_state.get("topology_neighbor_count_mean", 0.0))) or 0.0)
    field_topology_neighbor_count_max = float(item.get("field_topology_neighbor_count_max", item.get("inner_context_cluster_topology_neighbor_count_max", field_topology_layout_state.get("topology_neighbor_count_max", 0.0))) or 0.0)
    active_context_topology_rows = float(active_context_trace.get("field_topology_rows", 0.0) or 0.0)
    active_context_topology_cols = float(active_context_trace.get("field_topology_cols", 0.0) or 0.0)
    active_context_topology_position_count = float(active_context_trace.get("field_topology_position_count", 0.0) or 0.0)
    active_context_topology_neighbor_link_count = float(active_context_trace.get("field_topology_neighbor_link_count", 0.0) or 0.0)
    active_context_topology_neighbor_count_mean = float(active_context_trace.get("field_topology_neighbor_count_mean", 0.0) or 0.0)
    active_context_topology_neighbor_count_max = float(active_context_trace.get("field_topology_neighbor_count_max", 0.0) or 0.0)
    field_areal_topology_density_mean = float(item.get("field_areal_topology_density_mean", item.get("inner_context_cluster_areal_topology_density_mean", 0.0)) or 0.0)
    field_areal_topology_span_mean = float(item.get("field_areal_topology_span_mean", item.get("inner_context_cluster_areal_topology_span_mean", 0.0)) or 0.0)
    field_areal_topology_boundary_mean = float(item.get("field_areal_topology_boundary_mean", item.get("inner_context_cluster_areal_topology_boundary_mean", 0.0)) or 0.0)
    active_context_areal_topology_density_mean = float(active_context_trace.get("field_areal_topology_density_mean", 0.0) or 0.0)
    active_context_areal_topology_span_mean = float(active_context_trace.get("field_areal_topology_span_mean", 0.0) or 0.0)
    active_context_areal_topology_boundary_mean = float(active_context_trace.get("field_areal_topology_boundary_mean", 0.0) or 0.0)
    field_pattern_signature = dict(item.get("field_pattern_signature", {}) or {})
    field_pattern_signature_key = str(item.get("field_pattern_signature_key", item.get("inner_context_cluster_field_pattern_signature_key", field_pattern_signature.get("signature_key", ""))) or "")
    field_pattern_vector = [float(value) for value in list(item.get("field_pattern_vector", item.get("inner_context_cluster_field_pattern_vector", field_pattern_signature.get("field_pattern_vector", []))) or [])]
    inner_pattern_identity = str(item.get("inner_pattern_identity", item.get("inner_context_cluster_pattern_identity", "")) or "")
    inner_pattern_identity_confidence = float(item.get("inner_pattern_identity_confidence", item.get("inner_context_cluster_pattern_identity_confidence", 0.0)) or 0.0)
    inner_pattern_identity_stability = float(item.get("inner_pattern_identity_stability", item.get("inner_context_cluster_pattern_identity_stability", 0.0)) or 0.0)
    inner_pattern_identity_streak = float(item.get("inner_pattern_identity_streak", item.get("inner_context_cluster_pattern_identity_streak", 0.0)) or 0.0)
    inner_pattern_recognition_state = dict(item.get("inner_pattern_recognition_state", item.get("inner_context_cluster_pattern_recognition_state", {})) or {})
    inner_pattern_recognition_strength = float(item.get("inner_pattern_recognition_strength", item.get("inner_context_cluster_pattern_recognition_strength", inner_pattern_recognition_state.get("recognition_strength", 0.0))) or 0.0)
    inner_pattern_recognition_recurrent = bool(item.get("inner_pattern_recognition_recurrent", item.get("inner_context_cluster_pattern_recognition_recurrent", inner_pattern_recognition_state.get("recurrent", False))))
    inner_pattern_recognition_changed = bool(item.get("inner_pattern_recognition_changed", item.get("inner_context_cluster_pattern_recognition_changed", inner_pattern_recognition_state.get("changed", False))))
    active_context_field_pattern_signature_key = str(active_context_trace.get("field_pattern_signature_key", "") or "")
    active_context_field_pattern_vector = [float(value) for value in list(active_context_trace.get("field_pattern_vector", []) or [])]
    active_context_inner_pattern_identity = str(active_context_trace.get("inner_pattern_identity", "") or "")
    active_context_inner_pattern_identity_confidence = float(active_context_trace.get("inner_pattern_identity_confidence", 0.0) or 0.0)
    active_context_inner_pattern_identity_stability = float(active_context_trace.get("inner_pattern_identity_stability", 0.0) or 0.0)
    active_context_inner_pattern_identity_streak = float(active_context_trace.get("inner_pattern_identity_streak", 0.0) or 0.0)
    active_context_inner_pattern_recognition_strength = float(active_context_trace.get("inner_pattern_recognition_strength", 0.0) or 0.0)
    active_context_inner_pattern_recognition_recurrent = bool(active_context_trace.get("inner_pattern_recognition_recurrent", False))
    active_context_inner_pattern_recognition_changed = bool(active_context_trace.get("inner_pattern_recognition_changed", False))
    topology_agent_scale = max(1.0, float(getattr(Config, "MCM_FIELD_NEURON", field_topology_position_count or 1.0) or 1.0))
    topology_neighbor_scale = max(1.0, float(getattr(Config, "MCM_FIELD_LOCAL_NEIGHBORS", field_topology_neighbor_count_max or 1.0) or 1.0))
    topology_grid_capacity = max(1.0, field_topology_rows * field_topology_cols)
    active_context_topology_grid_capacity = max(1.0, active_context_topology_rows * active_context_topology_cols)
    field_topology_shape_balance = float((min(field_topology_rows, field_topology_cols) / max(1.0, max(field_topology_rows, field_topology_cols))) if max(field_topology_rows, field_topology_cols) > 0.0 else 0.0)
    field_topology_position_scale = float(max(0.0, min(1.0, field_topology_position_count / topology_agent_scale)))
    field_topology_grid_fill = float(max(0.0, min(1.0, field_topology_position_count / topology_grid_capacity)))
    field_topology_neighbor_density = float(max(0.0, min(1.0, field_topology_neighbor_count_mean / topology_neighbor_scale)))
    field_topology_link_density_axis = float(max(0.0, min(1.0, field_topology_neighbor_link_count / max(1.0, field_topology_position_count * topology_neighbor_scale))))
    active_context_topology_shape_balance = float((min(active_context_topology_rows, active_context_topology_cols) / max(1.0, max(active_context_topology_rows, active_context_topology_cols))) if max(active_context_topology_rows, active_context_topology_cols) > 0.0 else 0.0)
    active_context_topology_position_scale = float(max(0.0, min(1.0, active_context_topology_position_count / topology_agent_scale)))
    active_context_topology_grid_fill = float(max(0.0, min(1.0, active_context_topology_position_count / active_context_topology_grid_capacity)))
    active_context_topology_neighbor_density = float(max(0.0, min(1.0, active_context_topology_neighbor_count_mean / topology_neighbor_scale)))
    active_context_topology_link_density_axis = float(max(0.0, min(1.0, active_context_topology_neighbor_link_count / max(1.0, active_context_topology_position_count * topology_neighbor_scale))))
    topology_span_scale = max(1.0, float(np.sqrt(8.0)))
    field_areal_topology_density_axis = float(max(0.0, min(1.0, field_areal_topology_density_mean)))
    field_areal_topology_span_axis = float(max(0.0, min(1.0, field_areal_topology_span_mean / topology_span_scale)))
    field_areal_topology_boundary_axis = float(max(0.0, min(1.0, field_areal_topology_boundary_mean / topology_neighbor_scale)))
    field_areal_topology_integrity_axis = float(field_areal_topology_density_axis - field_areal_topology_boundary_axis)
    active_context_areal_topology_density_axis = float(max(0.0, min(1.0, active_context_areal_topology_density_mean)))
    active_context_areal_topology_span_axis = float(max(0.0, min(1.0, active_context_areal_topology_span_mean / topology_span_scale)))
    active_context_areal_topology_boundary_axis = float(max(0.0, min(1.0, active_context_areal_topology_boundary_mean / topology_neighbor_scale)))
    active_context_areal_topology_integrity_axis = float(active_context_areal_topology_density_axis - active_context_areal_topology_boundary_axis)
    field_pattern_vector_length_axis = float(max(0.0, min(1.0, len(field_pattern_vector) / 32.0)))
    field_pattern_vector_mean_axis = float(max(-1.0, min(1.0, float(np.mean(field_pattern_vector)) if field_pattern_vector else 0.0)))
    field_pattern_vector_max_axis = float(max(0.0, min(1.0, float(np.max(np.abs(field_pattern_vector))) if field_pattern_vector else 0.0)))
    field_pattern_vector_spread_axis = float(max(0.0, min(1.0, float(np.std(field_pattern_vector)) if field_pattern_vector else 0.0)))
    active_context_pattern_vector_length_axis = float(max(0.0, min(1.0, len(active_context_field_pattern_vector) / 32.0)))
    active_context_pattern_vector_mean_axis = float(max(-1.0, min(1.0, float(np.mean(active_context_field_pattern_vector)) if active_context_field_pattern_vector else 0.0)))
    active_context_pattern_vector_max_axis = float(max(0.0, min(1.0, float(np.max(np.abs(active_context_field_pattern_vector))) if active_context_field_pattern_vector else 0.0)))
    active_context_pattern_vector_spread_axis = float(max(0.0, min(1.0, float(np.std(active_context_field_pattern_vector)) if active_context_field_pattern_vector else 0.0)))
    inner_pattern_identity_confidence_axis = float(max(0.0, min(1.0, inner_pattern_identity_confidence)))
    active_context_inner_pattern_identity_confidence_axis = float(max(0.0, min(1.0, active_context_inner_pattern_identity_confidence)))
    stability_tick_scale = max(2.0, float(getattr(Config, "MCM_INNER_PATTERN_IDENTITY_STABILITY_TICKS", 5) or 5))
    inner_pattern_identity_stability_axis = float(max(0.0, min(1.0, inner_pattern_identity_stability)))
    active_context_inner_pattern_identity_stability_axis = float(max(0.0, min(1.0, active_context_inner_pattern_identity_stability)))
    inner_pattern_identity_streak_axis = float(max(0.0, min(1.0, inner_pattern_identity_streak / stability_tick_scale)))
    active_context_inner_pattern_identity_streak_axis = float(max(0.0, min(1.0, active_context_inner_pattern_identity_streak / stability_tick_scale)))
    inner_pattern_identity_match_axis = float(
        1.0
        if field_pattern_signature_key
        and active_context_field_pattern_signature_key
        and field_pattern_signature_key == active_context_field_pattern_signature_key
        else 0.0
    )
    inner_pattern_identity_reactivation_axis = float(active_context_activation * active_context_inner_pattern_identity_confidence_axis)
    inner_pattern_identity_presence_axis = float(1.0 if inner_pattern_identity or field_pattern_signature_key else 0.0)
    active_context_inner_pattern_identity_presence_axis = float(1.0 if active_context_inner_pattern_identity or active_context_field_pattern_signature_key else 0.0)
    inner_pattern_recognition_strength_axis = float(max(0.0, min(1.0, inner_pattern_recognition_strength)))
    active_context_inner_pattern_recognition_strength_axis = float(max(0.0, min(1.0, active_context_inner_pattern_recognition_strength)))
    inner_pattern_recognition_recurrent_axis = float(1.0 if inner_pattern_recognition_recurrent else 0.0)
    active_context_inner_pattern_recognition_recurrent_axis = float(1.0 if active_context_inner_pattern_recognition_recurrent else 0.0)
    inner_pattern_recognition_changed_axis = float(1.0 if inner_pattern_recognition_changed else 0.0)
    active_context_inner_pattern_recognition_changed_axis = float(1.0 if active_context_inner_pattern_recognition_changed else 0.0)
    inner_pattern_recognition_alignment_axis = float(inner_pattern_recognition_strength_axis * active_context_inner_pattern_recognition_strength_axis)
    inner_pattern_recognition_instability_axis = float(max(inner_pattern_recognition_changed_axis, active_context_inner_pattern_recognition_changed_axis))

    return {
        "direction_axis": float(direction_value),
        "tendency_axis": float(tendency_value),
        "confidence_axis": float(item.get("focus_confidence", 0.0) or 0.0),
        "observation_axis": float(item.get("observation_quality", 0.0) or 0.0),
        "uncertainty_axis": float(item.get("uncertainty_recognition_quality", 0.0) or 0.0),
        "correction_axis": float(item.get("correction_timing_quality", 0.0) or 0.0),
        "bearing_axis": float(item.get("structural_bearing_quality", 0.0) or 0.0),
        "path_axis": float(item.get("decision_path_quality", 0.0) or 0.0),
        "reward_axis": float(_experience_reward_delta(item) or 0.0),
        "profit_reward_axis": float(item.get("profit_reward", 0.0) or 0.0),
        "relief_signal_axis": float(item.get("relief_signal", 0.0) or 0.0),
        "stability_signal_axis": float(item.get("stability_signal", 0.0) or 0.0),
        "discipline_signal_axis": float(item.get("discipline_signal", 0.0) or 0.0),
        "neurochemical_confidence_axis": float(item.get("confidence_signal", 0.0) or 0.0),
        "overactivation_axis": float(item.get("overactivation_signal", 0.0) or 0.0),
        "chaos_penalty_axis": float(item.get("chaos_penalty", 0.0) or 0.0),
        "variance_penalty_axis": float(item.get("variance_penalty", 0.0) or 0.0),
        "overstrain_penalty_axis": float(item.get("overstrain_penalty", 0.0) or 0.0),
        "carrying_capacity_axis": float(item.get("carrying_capacity_delta", 0.0) or 0.0),
        "self_confidence_axis": float(item.get("self_confidence_delta", 0.0) or 0.0),
        "process_quality_axis": float(item.get("process_quality", 0.0) or 0.0),
        "bearing_effect_axis": float(bearing_effect),
        "packet_bearing_quality_axis": float(packet_bearing_quality),
        "packet_inner_outer_fit_axis": float(packet_inner_outer_fit),
        "packet_confidence_integrity_axis": float(packet_confidence_integrity),
        "packet_repetition_potential_axis": float(packet_repetition_potential),
        "packet_curiosity_pull_axis": float(packet_curiosity_pull),
        "packet_process_reward_axis": float(packet_process_reward),
        "packet_reorganization_need_axis": float(packet_reorganization_need),
        "constructive_stimulation_axis": float(constructive_stimulation),
        "strain_axis": float(pressure_delta + recovery_delta + survival_delta),
        "relief_axis": float(release_delta + bearing_delta),
        "capacity_balance_axis": float(capacity_delta - pressure_delta),
        "areal_pressure_axis": float(
            field_areal_conflict_mean
            + field_areal_fragmentation
            + processing_areal_tension
            + thought_areal_pressure
        ),
        "areal_support_axis": float(
            field_areal_stability_mean
            + field_areal_coherence_mean
            + field_areal_dominance
            + processing_areal_support
            + thought_areal_support
        ),
        "context_memory_impulse_axis": float(field_neuron_context_memory_impulse_norm_mean),
        "active_context_activation_axis": float(active_context_activation),
        "active_context_balance_axis": float(active_context_balance),
        "context_memory_reactivation_axis": float(field_neuron_context_memory_impulse_norm_mean * active_context_activation),
        "neural_felt_bearing_axis": float(neural_felt_bearing),
        "neural_felt_pressure_axis": float(neural_felt_pressure),
        "neural_felt_memory_resonance_axis": float(neural_felt_memory_resonance),
        "neural_felt_context_reactivation_axis": float(neural_felt_context_reactivation),
        "neural_felt_resonance_balance_axis": float(neural_felt_memory_resonance + neural_felt_context_reactivation - neural_felt_pressure),
        "inner_field_pressure_trend_axis": float(inner_field_pressure_trend),
        "inner_field_bearing_trend_axis": float(inner_field_bearing_trend),
        "inner_field_topology_tension_trend_axis": float(inner_field_topology_tension_trend),
        "inner_field_memory_resonance_trend_axis": float(inner_field_memory_resonance_trend),
        "inner_field_history_balance_axis": float(inner_field_bearing_trend + inner_field_memory_resonance_trend - inner_field_pressure_trend - inner_field_topology_tension_trend),
        "active_context_pressure_trend_axis": float(active_context_pressure_trend),
        "active_context_bearing_trend_axis": float(active_context_bearing_trend),
        "active_context_topology_tension_trend_axis": float(active_context_topology_tension_trend),
        "active_context_memory_resonance_trend_axis": float(active_context_memory_resonance_trend),
        "active_context_history_balance_axis": float(active_context_bearing_trend + active_context_memory_resonance_trend - active_context_pressure_trend - active_context_topology_tension_trend),
        "field_topology_shape_balance_axis": float(field_topology_shape_balance),
        "field_topology_position_scale_axis": float(field_topology_position_scale),
        "field_topology_grid_fill_axis": float(field_topology_grid_fill),
        "field_topology_neighbor_density_axis": float(field_topology_neighbor_density),
        "field_topology_link_density_axis": float(field_topology_link_density_axis),
        "active_context_topology_shape_balance_axis": float(active_context_topology_shape_balance),
        "active_context_topology_position_scale_axis": float(active_context_topology_position_scale),
        "active_context_topology_grid_fill_axis": float(active_context_topology_grid_fill),
        "active_context_topology_neighbor_density_axis": float(active_context_topology_neighbor_density),
        "active_context_topology_link_density_axis": float(active_context_topology_link_density_axis),
        "field_areal_topology_density_axis": float(field_areal_topology_density_axis),
        "field_areal_topology_span_axis": float(field_areal_topology_span_axis),
        "field_areal_topology_boundary_axis": float(field_areal_topology_boundary_axis),
        "field_areal_topology_integrity_axis": float(field_areal_topology_integrity_axis),
        "active_context_areal_topology_density_axis": float(active_context_areal_topology_density_axis),
        "active_context_areal_topology_span_axis": float(active_context_areal_topology_span_axis),
        "active_context_areal_topology_boundary_axis": float(active_context_areal_topology_boundary_axis),
        "active_context_areal_topology_integrity_axis": float(active_context_areal_topology_integrity_axis),
        "field_pattern_vector_length_axis": float(field_pattern_vector_length_axis),
        "field_pattern_vector_mean_axis": float(field_pattern_vector_mean_axis),
        "field_pattern_vector_max_axis": float(field_pattern_vector_max_axis),
        "field_pattern_vector_spread_axis": float(field_pattern_vector_spread_axis),
        "active_context_pattern_vector_length_axis": float(active_context_pattern_vector_length_axis),
        "active_context_pattern_vector_mean_axis": float(active_context_pattern_vector_mean_axis),
        "active_context_pattern_vector_max_axis": float(active_context_pattern_vector_max_axis),
        "active_context_pattern_vector_spread_axis": float(active_context_pattern_vector_spread_axis),
        "inner_pattern_identity_confidence_axis": float(inner_pattern_identity_confidence_axis),
        "active_context_inner_pattern_identity_confidence_axis": float(active_context_inner_pattern_identity_confidence_axis),
        "inner_pattern_identity_stability_axis": float(inner_pattern_identity_stability_axis),
        "active_context_inner_pattern_identity_stability_axis": float(active_context_inner_pattern_identity_stability_axis),
        "inner_pattern_identity_streak_axis": float(inner_pattern_identity_streak_axis),
        "active_context_inner_pattern_identity_streak_axis": float(active_context_inner_pattern_identity_streak_axis),
        "inner_pattern_identity_match_axis": float(inner_pattern_identity_match_axis),
        "inner_pattern_identity_reactivation_axis": float(inner_pattern_identity_reactivation_axis),
        "inner_pattern_identity_presence_axis": float(inner_pattern_identity_presence_axis),
        "active_context_inner_pattern_identity_presence_axis": float(active_context_inner_pattern_identity_presence_axis),
        "inner_pattern_recognition_strength_axis": float(inner_pattern_recognition_strength_axis),
        "active_context_inner_pattern_recognition_strength_axis": float(active_context_inner_pattern_recognition_strength_axis),
        "inner_pattern_recognition_recurrent_axis": float(inner_pattern_recognition_recurrent_axis),
        "active_context_inner_pattern_recognition_recurrent_axis": float(active_context_inner_pattern_recognition_recurrent_axis),
        "inner_pattern_recognition_changed_axis": float(inner_pattern_recognition_changed_axis),
        "active_context_inner_pattern_recognition_changed_axis": float(active_context_inner_pattern_recognition_changed_axis),
        "inner_pattern_recognition_alignment_axis": float(inner_pattern_recognition_alignment_axis),
        "inner_pattern_recognition_instability_axis": float(inner_pattern_recognition_instability_axis),
        "thought_conflict_axis": float(item.get("thought_decision_conflict", 0.0) or 0.0),
        "thought_maturity_axis": float(item.get("thought_state_maturity", 0.0) or 0.0),
        "delta_energy_axis": float(tension_delta.get("energy", 0.0) or 0.0),
        "delta_stability_axis": float(tension_delta.get("stability", 0.0) or 0.0),
        "delta_pressure_axis": float(pressure_delta),
        "delta_capacity_axis": float(capacity_delta),
        "delta_recovery_axis": float(recovery_delta),
        "delta_survival_axis": float(survival_delta),
        "delta_release_axis": float(release_delta),
        "delta_bearing_axis": float(bearing_delta),
        "delta_areal_pressure_axis": float(areal_pressure_delta),
        "delta_areal_stability_axis": float(areal_stability_delta),
        "delta_areal_drift_axis": float(areal_drift_delta),
        "delta_areal_dominance_axis": float(areal_dominance_delta),
        "delta_areal_fragmentation_axis": float(areal_fragmentation_delta),
        "delta_areal_conflict_axis": float(areal_conflict_delta),
    }

# --------------------------------------------------
def _update_experience_link_bucket(space, bucket_name, link_key, summary):

    experience_space = space if isinstance(space, dict) else {}
    normalized_key = str(link_key or "").strip()

    if not normalized_key or normalized_key == "-":
        return experience_space

    bucket = experience_space.get(bucket_name, {})
    if not isinstance(bucket, dict):
        bucket = {}
    item = dict(bucket.get(normalized_key, {}) or {})
    summary_item = summary if isinstance(summary, dict) else {}
    delta = float(summary_item.get("experience_reward_delta", _experience_reward_delta(summary_item)) or 0.0)

    previous_context = str(item.get("last_context_cluster_id", "-") or "-")
    current_context = str(summary_item.get("context_cluster_id", "-") or "-")
    previous_self_state = str(item.get("last_self_state", "-") or "-")
    current_self_state = str(summary_item.get("self_state", "stable") or "stable")

    relocation_count = int(item.get("relocation_count", 0) or 0)

    if previous_context not in ("", "-") and current_context not in ("", "-") and previous_context != current_context:
        relocation_count += 1

    if previous_self_state not in ("", "-") and current_self_state not in ("", "-") and previous_self_state != current_self_state:
        relocation_count += 1

    similarity_axes = dict(summary_item.get("experience_similarity_axes", {}) or {})
    if not similarity_axes:
        similarity_axes = _build_experience_similarity_axes(summary_item)
    previous_similarity_axes = dict(item.get("similarity_axes", {}) or {})

    drift_value = float(item.get("drift", 0.0) or 0.0)
    drift_input = abs(float(summary_item.get("competition_bias", 0.0) or 0.0))

    if summary_item.get("non_action_type"):
        drift_input += 0.12

    axis_shift = 0.0
    for axis_name, axis_value in similarity_axes.items():
        axis_shift += abs(float(axis_value or 0.0) - float(previous_similarity_axes.get(axis_name, 0.0) or 0.0))

    drift_input += min(0.45, axis_shift * 0.08)
    drift_value = float((drift_value * 0.74) + drift_input)

    reinforcement = float(item.get("reinforcement", 0.0) or 0.0)
    attenuation = float(item.get("attenuation", 0.0) or 0.0)

    if delta >= 0.0:
        reinforcement = float((reinforcement * 0.88) + delta)
        attenuation = float(attenuation * 0.94)
    else:
        reinforcement = float(reinforcement * 0.94)
        attenuation = float((attenuation * 0.82) + abs(delta))

    episodes = list(item.get("episodes", []) or [])
    episodes.append({
        "episode_id": str(summary_item.get("episode_id", "") or ""),
        "timestamp": summary_item.get("timestamp", None),
        "event_name": str(summary_item.get("event_name", "-") or "-"),
        "decision_tendency": str(summary_item.get("decision_tendency", "hold") or "hold"),
        "outcome_reason": str(summary_item.get("outcome_reason", "-") or "-"),
        "non_action_type": summary_item.get("non_action_type", None),
        "review_label": str(summary_item.get("review_label", "-") or "-"),
        "review_score": float(summary_item.get("review_score", 0.0) or 0.0),
        "experience_effect_score": float(summary_item.get("experience_effect_score", summary_item.get("experience_reward_delta", _experience_reward_delta(summary_item))) or 0.0),
        "profit_reward": float(summary_item.get("profit_reward", 0.0) or 0.0),
        "relief_signal": float(summary_item.get("relief_signal", 0.0) or 0.0),
        "stability_signal": float(summary_item.get("stability_signal", 0.0) or 0.0),
        "discipline_signal": float(summary_item.get("discipline_signal", 0.0) or 0.0),
        "confidence_signal": float(summary_item.get("confidence_signal", 0.0) or 0.0),
        "overactivation_signal": float(summary_item.get("overactivation_signal", 0.0) or 0.0),
        "chaos_penalty": float(summary_item.get("chaos_penalty", 0.0) or 0.0),
        "variance_penalty": float(summary_item.get("variance_penalty", 0.0) or 0.0),
        "overstrain_penalty": float(summary_item.get("overstrain_penalty", 0.0) or 0.0),
        "carrying_capacity_delta": float(summary_item.get("carrying_capacity_delta", 0.0) or 0.0),
        "self_confidence_delta": float(summary_item.get("self_confidence_delta", 0.0) or 0.0),
        "process_quality": float(summary_item.get("process_quality", 0.0) or 0.0),
        "decision_path_quality": float(summary_item.get("decision_path_quality", 0.0) or 0.0),
        "uncertainty_recognition_quality": float(summary_item.get("uncertainty_recognition_quality", 0.0) or 0.0),
        "observation_quality": float(summary_item.get("observation_quality", 0.0) or 0.0),
        "correction_timing_quality": float(summary_item.get("correction_timing_quality", 0.0) or 0.0),
        "structural_bearing_quality": float(summary_item.get("structural_bearing_quality", 0.0) or 0.0),
        "in_trade_update_count": int(summary_item.get("in_trade_update_count", 0) or 0),
        "in_trade_max_mfe": float(summary_item.get("in_trade_max_mfe", 0.0) or 0.0),
        "in_trade_max_mae": float(summary_item.get("in_trade_max_mae", 0.0) or 0.0),
        "in_trade_last_bars_open": int(summary_item.get("in_trade_last_bars_open", 0) or 0),
        "in_trade_avg_fill_ratio": float(summary_item.get("in_trade_avg_fill_ratio", 0.0) or 0.0),
        "in_trade_direction_stability": float(summary_item.get("in_trade_direction_stability", 0.0) or 0.0),
        "in_trade_avg_regulatory_load": float(summary_item.get("in_trade_avg_regulatory_load", 0.0) or 0.0),
        "in_trade_avg_action_capacity": float(summary_item.get("in_trade_avg_action_capacity", 0.0) or 0.0),
        "in_trade_avg_recovery_need": float(summary_item.get("in_trade_avg_recovery_need", 0.0) or 0.0),
        "in_trade_avg_survival_pressure": float(summary_item.get("in_trade_avg_survival_pressure", 0.0) or 0.0),
        "in_trade_avg_pressure_to_capacity": float(summary_item.get("in_trade_avg_pressure_to_capacity", 0.0) or 0.0),
        "in_trade_avg_pressure_release": float(summary_item.get("in_trade_avg_pressure_release", 0.0) or 0.0),
        "in_trade_avg_load_bearing_capacity": float(summary_item.get("in_trade_avg_load_bearing_capacity", 0.0) or 0.0),
        "in_trade_avg_state_stability": float(summary_item.get("in_trade_avg_state_stability", 0.0) or 0.0),
        "in_trade_avg_capacity_reserve": float(summary_item.get("in_trade_avg_capacity_reserve", 0.0) or 0.0),
        "in_trade_avg_recovery_balance": float(summary_item.get("in_trade_avg_recovery_balance", 0.0) or 0.0),
        "in_trade_avg_regulated_courage": float(summary_item.get("in_trade_avg_regulated_courage", 0.0) or 0.0),
        "in_trade_avg_courage_gap": float(summary_item.get("in_trade_avg_courage_gap", 0.0) or 0.0),
        "in_trade_last_pre_action_phase": str(summary_item.get("in_trade_last_pre_action_phase", "-") or "-"),
        "in_trade_last_dominant_tension_cause": str(summary_item.get("in_trade_last_dominant_tension_cause", "-") or "-"),
        "field_density": float(summary_item.get("field_density", 0.0) or 0.0),
        "field_stability": float(summary_item.get("field_stability", 0.0) or 0.0),
        "field_cluster_count": int(summary_item.get("field_cluster_count", 0) or 0),
        "field_areal_count": int(summary_item.get("field_areal_count", 0) or 0),
        "field_areal_activation_mean": float(summary_item.get("field_areal_activation_mean", 0.0) or 0.0),
        "field_areal_stability_mean": float(summary_item.get("field_areal_stability_mean", 0.0) or 0.0),
        "field_areal_pressure_mean": float(summary_item.get("field_areal_pressure_mean", 0.0) or 0.0),
        "field_areal_drift": float(summary_item.get("field_areal_drift", 0.0) or 0.0),
        "field_areal_dominance": float(summary_item.get("field_areal_dominance", 0.0) or 0.0),
        "field_areal_fragmentation": float(summary_item.get("field_areal_fragmentation", 0.0) or 0.0),
        "field_areal_coherence_mean": float(summary_item.get("field_areal_coherence_mean", 0.0) or 0.0),
        "field_areal_conflict_mean": float(summary_item.get("field_areal_conflict_mean", 0.0) or 0.0),
        "processing_areal_tension": float(summary_item.get("processing_areal_tension", 0.0) or 0.0),
        "processing_areal_support": float(summary_item.get("processing_areal_support", 0.0) or 0.0),
        "thought_areal_pressure": float(summary_item.get("thought_areal_pressure", 0.0) or 0.0),
        "thought_areal_support": float(summary_item.get("thought_areal_support", 0.0) or 0.0),
        "inner_context_cluster_mass_mean": float(summary_item.get("inner_context_cluster_mass_mean", 0.0) or 0.0),
        "inner_context_cluster_mass_max": float(summary_item.get("inner_context_cluster_mass_max", 0.0) or 0.0),
        "inner_context_cluster_center_spread": float(summary_item.get("inner_context_cluster_center_spread", 0.0) or 0.0),
        "inner_context_cluster_separation": float(summary_item.get("inner_context_cluster_separation", 0.0) or 0.0),
        "inner_context_cluster_center_drift": float(summary_item.get("inner_context_cluster_center_drift", 0.0) or 0.0),
        "inner_context_cluster_count_drift": float(summary_item.get("inner_context_cluster_count_drift", 0.0) or 0.0),
        "inner_context_cluster_velocity_trend": float(summary_item.get("inner_context_cluster_velocity_trend", 0.0) or 0.0),
        "inner_context_cluster_reorganization_direction": str(summary_item.get("inner_context_cluster_reorganization_direction", "stable") or "stable"),
        "inner_context_cluster_mean_velocity": float(summary_item.get("inner_context_cluster_mean_velocity", 0.0) or 0.0),
        "inner_context_cluster_regulation_pressure": float(summary_item.get("inner_context_cluster_regulation_pressure", 0.0) or 0.0),
        "inner_context_cluster_neuron_context_memory_impulse_norm_mean": float(summary_item.get("inner_context_cluster_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0),
        "inner_context_cluster_topology_link_density": float(summary_item.get("inner_context_cluster_topology_link_density", 0.0) or 0.0),
        "inner_context_cluster_topology_coherence": float(summary_item.get("inner_context_cluster_topology_coherence", 0.0) or 0.0),
        "inner_context_cluster_topology_tension": float(summary_item.get("inner_context_cluster_topology_tension", 0.0) or 0.0),
        "inner_context_cluster_topology_state_label": str(summary_item.get("inner_context_cluster_topology_state_label", "sparse_topology") or "sparse_topology"),
        "episode_felt_summary": dict(summary_item.get("episode_felt_summary", {}) or {}),
        "felt_label": str(summary_item.get("felt_label", "mixed") or "mixed"),
        "axis_shift": float(axis_shift),
        "drift": float(drift_value),
    })

    affective_profile = _build_affective_structure_profile(episodes[-24:])

    item["link_key"] = str(normalized_key)
    item["seen"] = int(item.get("seen", 0) or 0) + 1
    item["last_episode_id"] = str(summary_item.get("episode_id", "") or "")
    item["last_timestamp"] = summary_item.get("timestamp", None)
    item["last_event"] = str(summary_item.get("event_name", "-") or "-")
    item["last_decision_tendency"] = str(summary_item.get("decision_tendency", "hold") or "hold")
    item["last_outcome_reason"] = str(summary_item.get("outcome_reason", "-") or "-")
    item["last_context_cluster_id"] = str(current_context)
    item["last_self_state"] = str(current_self_state)
    item["last_attractor"] = str(summary_item.get("attractor", "neutral") or "neutral")
    item["last_review_label"] = str(summary_item.get("review_label", "-") or "-")
    item["last_review_score"] = float(summary_item.get("review_score", 0.0) or 0.0)
    item["last_in_trade_pre_action_phase"] = str(summary_item.get("in_trade_last_pre_action_phase", "-") or "-")
    item["last_in_trade_dominant_tension_cause"] = str(summary_item.get("in_trade_last_dominant_tension_cause", "-") or "-")
    item["decision_path_quality"] = float((float(item.get("decision_path_quality", 0.0) or 0.0) * 0.72) + (float(summary_item.get("decision_path_quality", 0.0) or 0.0) * 0.28))
    item["uncertainty_recognition_quality"] = float((float(item.get("uncertainty_recognition_quality", 0.0) or 0.0) * 0.72) + (float(summary_item.get("uncertainty_recognition_quality", 0.0) or 0.0) * 0.28))
    item["observation_quality"] = float((float(item.get("observation_quality", 0.0) or 0.0) * 0.72) + (float(summary_item.get("observation_quality", 0.0) or 0.0) * 0.28))
    item["correction_timing_quality"] = float((float(item.get("correction_timing_quality", 0.0) or 0.0) * 0.72) + (float(summary_item.get("correction_timing_quality", 0.0) or 0.0) * 0.28))
    item["structural_bearing_quality"] = float((float(item.get("structural_bearing_quality", 0.0) or 0.0) * 0.72) + (float(summary_item.get("structural_bearing_quality", 0.0) or 0.0) * 0.28))
    for neuro_key in (
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
    ):
        value = float(summary_item.get(neuro_key, 0.0) or 0.0)
        item[f"avg_{neuro_key}"] = float((float(item.get(f"avg_{neuro_key}", 0.0) or 0.0) * 0.72) + (value * 0.28))
        item[f"last_{neuro_key}"] = float(value)
    item["avg_regulatory_load"] = float((float(item.get("avg_regulatory_load", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_regulatory_load", 0.0) or 0.0) * 0.32))
    item["avg_action_capacity"] = float((float(item.get("avg_action_capacity", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_action_capacity", 0.0) or 0.0) * 0.32))
    item["avg_recovery_need"] = float((float(item.get("avg_recovery_need", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_recovery_need", 0.0) or 0.0) * 0.32))
    item["avg_survival_pressure"] = float((float(item.get("avg_survival_pressure", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_survival_pressure", 0.0) or 0.0) * 0.32))
    item["avg_pressure_to_capacity"] = float((float(item.get("avg_pressure_to_capacity", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_pressure_to_capacity", 0.0) or 0.0) * 0.32))
    item["avg_pressure_release"] = float((float(item.get("avg_pressure_release", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_pressure_release", 0.0) or 0.0) * 0.32))
    item["avg_load_bearing_capacity"] = float((float(item.get("avg_load_bearing_capacity", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_load_bearing_capacity", 0.0) or 0.0) * 0.32))
    item["avg_state_stability"] = float((float(item.get("avg_state_stability", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_state_stability", 0.0) or 0.0) * 0.32))
    item["avg_capacity_reserve"] = float((float(item.get("avg_capacity_reserve", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_capacity_reserve", 0.0) or 0.0) * 0.32))
    item["avg_recovery_balance"] = float((float(item.get("avg_recovery_balance", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_recovery_balance", 0.0) or 0.0) * 0.32))
    item["avg_regulated_courage"] = float((float(item.get("avg_regulated_courage", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_regulated_courage", 0.0) or 0.0) * 0.32))
    item["avg_courage_gap"] = float((float(item.get("avg_courage_gap", 0.0) or 0.0) * 0.68) + (float(summary_item.get("in_trade_avg_courage_gap", 0.0) or 0.0) * 0.32))
    item["avg_field_density"] = float((float(item.get("avg_field_density", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_density", 0.0) or 0.0) * 0.32))
    item["avg_field_stability"] = float((float(item.get("avg_field_stability", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_stability", 0.0) or 0.0) * 0.32))
    item["avg_field_cluster_count"] = float((float(item.get("avg_field_cluster_count", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_cluster_count", 0.0) or 0.0) * 0.32))
    item["avg_field_cluster_mass_mean"] = float((float(item.get("avg_field_cluster_mass_mean", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_mass_mean", 0.0) or 0.0) * 0.32))
    item["avg_field_cluster_mass_max"] = float((float(item.get("avg_field_cluster_mass_max", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_mass_max", 0.0) or 0.0) * 0.32))
    item["avg_field_cluster_center_spread"] = float((float(item.get("avg_field_cluster_center_spread", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_center_spread", 0.0) or 0.0) * 0.32))
    item["avg_field_cluster_separation"] = float((float(item.get("avg_field_cluster_separation", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_separation", 0.0) or 0.0) * 0.32))
    item["avg_field_cluster_center_drift"] = float((float(item.get("avg_field_cluster_center_drift", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_center_drift", 0.0) or 0.0) * 0.32))
    item["avg_field_cluster_count_drift"] = float((float(item.get("avg_field_cluster_count_drift", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_count_drift", 0.0) or 0.0) * 0.32))
    item["avg_field_velocity_trend"] = float((float(item.get("avg_field_velocity_trend", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_velocity_trend", 0.0) or 0.0) * 0.32))
    item["last_field_reorganization_direction"] = str(summary_item.get("inner_context_cluster_reorganization_direction", item.get("last_field_reorganization_direction", "stable")) or "stable")
    item["avg_field_mean_velocity"] = float((float(item.get("avg_field_mean_velocity", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_mean_velocity", 0.0) or 0.0) * 0.32))
    item["avg_field_regulation_pressure"] = float((float(item.get("avg_field_regulation_pressure", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_regulation_pressure", 0.0) or 0.0) * 0.32))
    item["avg_context_memory_impulse"] = float((float(item.get("avg_context_memory_impulse", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0) * 0.32))
    item["avg_field_topology_link_density"] = float((float(item.get("avg_field_topology_link_density", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_topology_link_density", 0.0) or 0.0) * 0.32))
    item["avg_field_topology_coherence"] = float((float(item.get("avg_field_topology_coherence", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_topology_coherence", 0.0) or 0.0) * 0.32))
    item["avg_field_topology_tension"] = float((float(item.get("avg_field_topology_tension", 0.0) or 0.0) * 0.68) + (float(summary_item.get("inner_context_cluster_topology_tension", 0.0) or 0.0) * 0.32))
    item["last_field_topology_state_label"] = str(summary_item.get("inner_context_cluster_topology_state_label", item.get("last_field_topology_state_label", "sparse_topology")) or "sparse_topology")
    item["avg_field_areal_count"] = float((float(item.get("avg_field_areal_count", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_areal_count", 0.0) or 0.0) * 0.32))
    item["avg_field_areal_activation_mean"] = float((float(item.get("avg_field_areal_activation_mean", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_areal_activation_mean", 0.0) or 0.0) * 0.32))
    item["avg_field_areal_stability_mean"] = float((float(item.get("avg_field_areal_stability_mean", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_areal_stability_mean", 0.0) or 0.0) * 0.32))
    item["avg_field_areal_pressure_mean"] = float((float(item.get("avg_field_areal_pressure_mean", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_areal_pressure_mean", 0.0) or 0.0) * 0.32))
    item["avg_field_areal_drift"] = float((float(item.get("avg_field_areal_drift", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_areal_drift", 0.0) or 0.0) * 0.32))
    item["avg_field_areal_dominance"] = float((float(item.get("avg_field_areal_dominance", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_areal_dominance", 0.0) or 0.0) * 0.32))
    item["avg_field_areal_fragmentation"] = float((float(item.get("avg_field_areal_fragmentation", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_areal_fragmentation", 0.0) or 0.0) * 0.32))
    item["avg_field_areal_coherence_mean"] = float((float(item.get("avg_field_areal_coherence_mean", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_areal_coherence_mean", 0.0) or 0.0) * 0.32))
    item["avg_field_areal_conflict_mean"] = float((float(item.get("avg_field_areal_conflict_mean", 0.0) or 0.0) * 0.68) + (float(summary_item.get("field_areal_conflict_mean", 0.0) or 0.0) * 0.32))
    item["avg_processing_areal_tension"] = float((float(item.get("avg_processing_areal_tension", 0.0) or 0.0) * 0.68) + (float(summary_item.get("processing_areal_tension", 0.0) or 0.0) * 0.32))
    item["avg_processing_areal_support"] = float((float(item.get("avg_processing_areal_support", 0.0) or 0.0) * 0.68) + (float(summary_item.get("processing_areal_support", 0.0) or 0.0) * 0.32))
    item["avg_thought_areal_pressure"] = float((float(item.get("avg_thought_areal_pressure", 0.0) or 0.0) * 0.68) + (float(summary_item.get("thought_areal_pressure", 0.0) or 0.0) * 0.32))
    item["avg_thought_areal_support"] = float((float(item.get("avg_thought_areal_support", 0.0) or 0.0) * 0.68) + (float(summary_item.get("thought_areal_support", 0.0) or 0.0) * 0.32))
    item["bearing_effect"] = float((float(item.get("bearing_effect", 0.0) or 0.0) * 0.70) + (float(_experience_bearing_delta(summary_item) or 0.0) * 0.30))
    item["relief_score"] = float((float(item.get("relief_score", 0.0) or 0.0) * 0.70) + (max(0.0, float(summary_item.get("in_trade_avg_action_capacity", 0.0) or 0.0) + float(summary_item.get("in_trade_avg_pressure_release", 0.0) or 0.0) + float(summary_item.get("in_trade_avg_capacity_reserve", 0.0) or 0.0)) * 0.30))
    item["strain_score"] = float((float(item.get("strain_score", 0.0) or 0.0) * 0.70) + (max(0.0, float(summary_item.get("in_trade_avg_regulatory_load", 0.0) or 0.0) + float(summary_item.get("in_trade_avg_recovery_need", 0.0) or 0.0) + float(summary_item.get("in_trade_avg_survival_pressure", 0.0) or 0.0) + max(0.0, -float(summary_item.get("in_trade_avg_recovery_balance", 0.0) or 0.0))) * 0.30))
    item["areal_support_score"] = float((float(item.get("areal_support_score", 0.0) or 0.0) * 0.70) + (max(0.0, float(summary_item.get("field_areal_stability_mean", 0.0) or 0.0) + float(summary_item.get("field_areal_coherence_mean", 0.0) or 0.0) + float(summary_item.get("field_areal_dominance", 0.0) or 0.0) + float(summary_item.get("processing_areal_support", 0.0) or 0.0) + float(summary_item.get("thought_areal_support", 0.0) or 0.0)) * 0.24))
    item["areal_conflict_score"] = float((float(item.get("areal_conflict_score", 0.0) or 0.0) * 0.70) + (max(0.0, float(summary_item.get("field_areal_conflict_mean", 0.0) or 0.0) + float(summary_item.get("field_areal_fragmentation", 0.0) or 0.0) + float(summary_item.get("processing_areal_tension", 0.0) or 0.0) + float(summary_item.get("thought_areal_pressure", 0.0) or 0.0)) * 0.24))
    item["similarity_axes"] = dict(similarity_axes)
    item["axis_shift"] = float((float(item.get("axis_shift", 0.0) or 0.0) * 0.68) + (axis_shift * 0.32))
    item["drift"] = float(drift_value)
    item["reinforcement"] = float(reinforcement)
    item["attenuation"] = float(attenuation)
    item["relocation_count"] = int(relocation_count)
    item["episodes"] = list(episodes[-12:])
    item["felt_profile"] = {
        "distribution": dict(affective_profile.get("distribution", {}) or {}),
        "averages": dict(affective_profile.get("averages", {}) or {}),
        "variance": dict(affective_profile.get("variance", {}) or {}),
        "stability": dict(affective_profile.get("stability", {}) or {}),
        "dynamic": dict(affective_profile.get("dynamic", {}) or {}),
    }
    item["felt_bearing_score"] = float(affective_profile.get("felt_bearing_score", 0.0) or 0.0)
    item["felt_profile_label"] = str(affective_profile.get("felt_profile_label", "mixed_unclear") or "mixed_unclear")
    item["felt_distribution"] = dict(affective_profile.get("distribution", {}) or {})
    item["felt_history"] = list(affective_profile.get("felt_history", []) or [])

    outcome_reason = str(summary_item.get("outcome_reason", "-") or "-").strip().lower()

    if outcome_reason == "tp_hit":
        item["tp"] = int(item.get("tp", 0) or 0) + 1
    elif outcome_reason == "sl_hit":
        item["sl"] = int(item.get("sl", 0) or 0) + 1
    elif outcome_reason == "cancel":
        item["cancel"] = int(item.get("cancel", 0) or 0) + 1
    elif outcome_reason == "timeout":
        item["timeout"] = int(item.get("timeout", 0) or 0) + 1

    if summary_item.get("non_action_type"):
        item["non_action"] = int(item.get("non_action", 0) or 0) + 1

    phase_key = str(summary_item.get("in_trade_last_pre_action_phase", "-") or "-").strip().lower()
    tension_key = str(summary_item.get("in_trade_last_dominant_tension_cause", "-") or "-").strip().lower()

    if phase_key and phase_key != "-":
        item[f"phase_{phase_key}"] = int(item.get(f"phase_{phase_key}", 0) or 0) + 1

    if tension_key and tension_key != "-":
        item[f"tension_{tension_key}"] = int(item.get(f"tension_{tension_key}", 0) or 0) + 1

    bucket[str(normalized_key)] = dict(item)
    experience_space[str(bucket_name)] = bucket
    return experience_space

# --------------------------------------------------
def _update_field_decision_outcome_protocol(space, summary):

    experience_space = space if isinstance(space, dict) else {}
    item = summary if isinstance(summary, dict) else {}

    phase = str(item.get("in_trade_last_pre_action_phase", item.get("pre_action_phase", "-")) or "-").strip().lower()
    outcome_reason = str(item.get("outcome_reason", "-") or "-").strip().lower()
    field_label = str(item.get("inner_context_cluster_field_perception_label", item.get("field_perception_label", "-")) or "-").strip().lower()

    if not phase or phase == "-":
        return experience_space

    protocol = experience_space.get("field_decision_outcome_protocol", {})
    if not isinstance(protocol, dict):
        protocol = {}
    phase_stats = protocol.get("phase_stats", {})
    if not isinstance(phase_stats, dict):
        phase_stats = {}
    phase_item = dict(phase_stats.get(phase, {}) or {})

    count = int(phase_item.get("count", 0) or 0) + 1

    def _avg(existing, value):
        return float(((float(existing or 0.0) * float(count - 1)) + float(value or 0.0)) / max(1, count))

    phase_item.update({
        "count": int(count),
        "last_outcome_reason": str(outcome_reason or "-"),
        "last_field_label": str(field_label or "-"),
        "avg_experience_effect_score": _avg(phase_item.get("avg_experience_effect_score", 0.0), item.get("experience_effect_score", 0.0)),
        "avg_process_quality": _avg(phase_item.get("avg_process_quality", 0.0), item.get("process_quality", 0.0)),
        "avg_carrying_capacity_delta": _avg(phase_item.get("avg_carrying_capacity_delta", 0.0), item.get("carrying_capacity_delta", 0.0)),
        "avg_self_confidence_delta": _avg(phase_item.get("avg_self_confidence_delta", 0.0), item.get("self_confidence_delta", 0.0)),
        "avg_in_trade_state_stability": _avg(phase_item.get("avg_in_trade_state_stability", 0.0), item.get("in_trade_avg_state_stability", 0.0)),
        "avg_in_trade_regulatory_load": _avg(phase_item.get("avg_in_trade_regulatory_load", 0.0), item.get("in_trade_avg_regulatory_load", 0.0)),
        "avg_in_trade_action_capacity": _avg(phase_item.get("avg_in_trade_action_capacity", 0.0), item.get("in_trade_avg_action_capacity", 0.0)),
    })

    outcome_counts = dict(phase_item.get("outcome_counts", {}) or {})
    outcome_counts[outcome_reason or "-"] = int(outcome_counts.get(outcome_reason or "-", 0) or 0) + 1
    phase_item["outcome_counts"] = dict(outcome_counts)

    field_label_counts = dict(phase_item.get("field_label_counts", {}) or {})
    field_label_counts[field_label or "-"] = int(field_label_counts.get(field_label or "-", 0) or 0) + 1
    phase_item["field_label_counts"] = dict(field_label_counts)

    phase_stats[phase] = dict(phase_item)
    protocol.update({
        "last_phase": str(phase),
        "last_outcome_reason": str(outcome_reason or "-"),
        "last_field_label": str(field_label or "-"),
        "phase_stats": phase_stats,
    })
    experience_space["field_decision_outcome_protocol"] = protocol
    return experience_space

# --------------------------------------------------
def _append_experience_episode(space, summary):

    experience_space = space if isinstance(space, dict) else {}
    history = list(experience_space.get("episode_links", []) or [])
    history.append({
        "episode_id": str((summary or {}).get("episode_id", "") or ""),
        "timestamp": (summary or {}).get("timestamp", None),
        "event_name": str((summary or {}).get("event_name", "-") or "-"),
        "decision_tendency": str((summary or {}).get("decision_tendency", "hold") or "hold"),
        "proposed_decision": str((summary or {}).get("proposed_decision", "WAIT") or "WAIT"),
        "signature_key": str((summary or {}).get("signature_key", "-") or "-"),
        "context_cluster_id": str((summary or {}).get("context_cluster_id", "-") or "-"),
        "inner_context_cluster_id": str((summary or {}).get("inner_context_cluster_id", "-") or "-"),
        "inner_context_cluster_distance": float((summary or {}).get("inner_context_cluster_distance", 0.0) or 0.0),
        "inner_context_cluster_score": float((summary or {}).get("inner_context_cluster_score", 0.0) or 0.0),
        "inner_context_cluster_trust": float((summary or {}).get("inner_context_cluster_trust", 0.0) or 0.0),
        "inner_context_cluster_mass_mean": float((summary or {}).get("inner_context_cluster_mass_mean", 0.0) or 0.0),
        "inner_context_cluster_mass_max": float((summary or {}).get("inner_context_cluster_mass_max", 0.0) or 0.0),
        "inner_context_cluster_center_spread": float((summary or {}).get("inner_context_cluster_center_spread", 0.0) or 0.0),
        "inner_context_cluster_separation": float((summary or {}).get("inner_context_cluster_separation", 0.0) or 0.0),
        "inner_context_cluster_center_drift": float((summary or {}).get("inner_context_cluster_center_drift", 0.0) or 0.0),
        "inner_context_cluster_count_drift": float((summary or {}).get("inner_context_cluster_count_drift", 0.0) or 0.0),
        "inner_context_cluster_velocity_trend": float((summary or {}).get("inner_context_cluster_velocity_trend", 0.0) or 0.0),
        "inner_context_cluster_reorganization_direction": str((summary or {}).get("inner_context_cluster_reorganization_direction", "stable") or "stable"),
        "inner_context_cluster_mean_velocity": float((summary or {}).get("inner_context_cluster_mean_velocity", 0.0) or 0.0),
        "inner_context_cluster_regulation_pressure": float((summary or {}).get("inner_context_cluster_regulation_pressure", 0.0) or 0.0),
        "outcome_reason": str((summary or {}).get("outcome_reason", "-") or "-"),
        "non_action_type": (summary or {}).get("non_action_type", None),
        "review_label": str((summary or {}).get("review_label", "-") or "-"),
        "review_score": float((summary or {}).get("review_score", 0.0) or 0.0),
        "experience_effect_score": float((summary or {}).get("experience_effect_score", _experience_reward_delta(summary)) or 0.0),
        "profit_reward": float((summary or {}).get("profit_reward", 0.0) or 0.0),
        "relief_signal": float((summary or {}).get("relief_signal", 0.0) or 0.0),
        "stability_signal": float((summary or {}).get("stability_signal", 0.0) or 0.0),
        "discipline_signal": float((summary or {}).get("discipline_signal", 0.0) or 0.0),
        "confidence_signal": float((summary or {}).get("confidence_signal", 0.0) or 0.0),
        "overactivation_signal": float((summary or {}).get("overactivation_signal", 0.0) or 0.0),
        "chaos_penalty": float((summary or {}).get("chaos_penalty", 0.0) or 0.0),
        "variance_penalty": float((summary or {}).get("variance_penalty", 0.0) or 0.0),
        "overstrain_penalty": float((summary or {}).get("overstrain_penalty", 0.0) or 0.0),
        "carrying_capacity_delta": float((summary or {}).get("carrying_capacity_delta", 0.0) or 0.0),
        "self_confidence_delta": float((summary or {}).get("self_confidence_delta", 0.0) or 0.0),
        "process_quality": float((summary or {}).get("process_quality", 0.0) or 0.0),
        "decision_path_quality": float((summary or {}).get("decision_path_quality", 0.0) or 0.0),
        "uncertainty_recognition_quality": float((summary or {}).get("uncertainty_recognition_quality", 0.0) or 0.0),
        "observation_quality": float((summary or {}).get("observation_quality", 0.0) or 0.0),
        "correction_timing_quality": float((summary or {}).get("correction_timing_quality", 0.0) or 0.0),
        "structural_bearing_quality": float((summary or {}).get("structural_bearing_quality", 0.0) or 0.0),
        "in_trade_update_count": int((summary or {}).get("in_trade_update_count", 0) or 0),
        "in_trade_max_mfe": float((summary or {}).get("in_trade_max_mfe", 0.0) or 0.0),
        "in_trade_max_mae": float((summary or {}).get("in_trade_max_mae", 0.0) or 0.0),
        "in_trade_last_bars_open": int((summary or {}).get("in_trade_last_bars_open", 0) or 0),
        "in_trade_avg_fill_ratio": float((summary or {}).get("in_trade_avg_fill_ratio", 0.0) or 0.0),
        "in_trade_direction_stability": float((summary or {}).get("in_trade_direction_stability", 0.0) or 0.0),
        "in_trade_avg_regulatory_load": float((summary or {}).get("in_trade_avg_regulatory_load", 0.0) or 0.0),
        "in_trade_avg_action_capacity": float((summary or {}).get("in_trade_avg_action_capacity", 0.0) or 0.0),
        "in_trade_avg_recovery_need": float((summary or {}).get("in_trade_avg_recovery_need", 0.0) or 0.0),
        "in_trade_avg_survival_pressure": float((summary or {}).get("in_trade_avg_survival_pressure", 0.0) or 0.0),
        "in_trade_avg_pressure_to_capacity": float((summary or {}).get("in_trade_avg_pressure_to_capacity", 0.0) or 0.0),
        "in_trade_avg_pressure_release": float((summary or {}).get("in_trade_avg_pressure_release", 0.0) or 0.0),
        "in_trade_avg_load_bearing_capacity": float((summary or {}).get("in_trade_avg_load_bearing_capacity", 0.0) or 0.0),
        "in_trade_avg_state_stability": float((summary or {}).get("in_trade_avg_state_stability", 0.0) or 0.0),
        "in_trade_avg_capacity_reserve": float((summary or {}).get("in_trade_avg_capacity_reserve", 0.0) or 0.0),
        "in_trade_avg_recovery_balance": float((summary or {}).get("in_trade_avg_recovery_balance", 0.0) or 0.0),
        "in_trade_avg_regulated_courage": float((summary or {}).get("in_trade_avg_regulated_courage", 0.0) or 0.0),
        "in_trade_avg_courage_gap": float((summary or {}).get("in_trade_avg_courage_gap", 0.0) or 0.0),
        "in_trade_last_pre_action_phase": str((summary or {}).get("in_trade_last_pre_action_phase", "-") or "-"),
        "in_trade_last_dominant_tension_cause": str((summary or {}).get("in_trade_last_dominant_tension_cause", "-") or "-"),
        "state_before": dict((summary or {}).get("state_before", {}) or {}),
        "state_after": dict((summary or {}).get("state_after", {}) or {}),
        "state_delta": dict((summary or {}).get("state_delta", {}) or {}),
        "similarity_axes": dict((summary or {}).get("experience_similarity_axes", {}) or _build_experience_similarity_axes(summary)),
    })
    experience_space["episode_links"] = list(history[-32:])
    experience_space = _update_field_decision_outcome_protocol(experience_space, summary)
    return experience_space

# --------------------------------------------------
def _build_affective_structure_profile(episodes):

    items = [dict(item or {}) for item in list(episodes or []) if isinstance(item, dict)]

    if not items:
        return {
            "distribution": {
                "positive_ratio": 0.0,
                "negative_ratio": 0.0,
                "neutral_ratio": 0.0,
                "euphoric_ratio": 0.0,
                "burden_ratio": 0.0,
                "areal_fragmented_ratio": 0.0,
                "areal_supported_ratio": 0.0,
            },
            "averages": {
                "felt_valence_avg": 0.0,
                "felt_bearing_avg": 0.0,
                "felt_regulation_quality_avg": 0.0,
                "felt_recovery_cost_avg": 0.0,
                "felt_areal_support_avg": 0.0,
                "felt_areal_conflict_avg": 0.0,
            },
            "variance": {
                "felt_valence_variance": 0.0,
                "felt_bearing_variance": 0.0,
                "felt_areal_support_variance": 0.0,
                "felt_areal_conflict_variance": 0.0,
            },
            "stability": {
                "felt_stability": 0.0,
                "felt_coherence_avg": 0.0,
                "felt_conflict_ratio": 0.0,
                "felt_areal_support_avg": 0.0,
                "felt_areal_conflict_avg": 0.0,
            },
            "dynamic": {
                "felt_drift_avg": 0.0,
                "felt_trend": "flat",
                "felt_areal_drift_avg": 0.0,
            },
            "felt_bearing_score": 0.0,
            "felt_profile_label": "mixed_unclear",
            "felt_history": [],
        }

    felt_items = []
    for item in items:
        felt = dict(item.get("episode_felt_summary", {}) or {})
        felt_items.append({
            "timestamp": item.get("timestamp", None),
            "valence": float(felt.get("valence", 0.0) or 0.0),
            "bearing": float(felt.get("bearing", 0.0) or 0.0),
            "regulation_quality": float(felt.get("regulation_quality", 0.0) or 0.0),
            "burden": float(felt.get("burden", 0.0) or 0.0),
            "overactivation": float(felt.get("overactivation", 0.0) or 0.0),
            "stability": float(felt.get("stability", 0.0) or 0.0),
            "confidence": float(felt.get("confidence", 0.0) or 0.0),
            "conflict": float(felt.get("conflict", 0.0) or 0.0),
            "recovery_cost": float(felt.get("recovery_cost", 0.0) or 0.0),
            "areal_support": float(felt.get("areal_support", 0.0) or 0.0),
            "areal_conflict_pressure": float(felt.get("areal_conflict_pressure", 0.0) or 0.0),
            "field_areal_fragmentation": float(felt.get("field_areal_fragmentation", 0.0) or 0.0),
            "field_areal_conflict_mean": float(felt.get("field_areal_conflict_mean", 0.0) or 0.0),
            "processing_areal_tension": float(felt.get("processing_areal_tension", 0.0) or 0.0),
            "processing_areal_support": float(felt.get("processing_areal_support", 0.0) or 0.0),
            "thought_areal_pressure": float(felt.get("thought_areal_pressure", 0.0) or 0.0),
            "thought_areal_support": float(felt.get("thought_areal_support", 0.0) or 0.0),
            "label": str(felt.get("felt_label", "mixed") or "mixed"),
            "axis_shift": float(item.get("axis_shift", 0.0) or 0.0),
            "drift": float(item.get("drift", 0.0) or 0.0),
        })

    total = float(len(felt_items))
    valences = [float(item["valence"]) for item in felt_items]
    bearings = [float(item["bearing"]) for item in felt_items]
    regulation_values = [float(item["regulation_quality"]) for item in felt_items]
    recovery_values = [float(item["recovery_cost"]) for item in felt_items]
    stability_values = [float(item["stability"]) for item in felt_items]
    conflict_values = [float(item["conflict"]) for item in felt_items]
    areal_support_values = [float(item["areal_support"]) for item in felt_items]
    areal_conflict_values = [float(item["areal_conflict_pressure"]) for item in felt_items]
    fragmentation_values = [float(item["field_areal_fragmentation"]) for item in felt_items]
    areal_dynamic_values = [
        float(item["drift"])
        + float(item["axis_shift"])
        + (float(item["processing_areal_tension"]) * 0.35)
        + (float(item["thought_areal_pressure"]) * 0.25)
        for item in felt_items
    ]

    valence_avg = float(sum(valences) / total)
    bearing_avg = float(sum(bearings) / total)
    regulation_avg = float(sum(regulation_values) / total)
    recovery_avg = float(sum(recovery_values) / total)
    stability_avg = float(sum(stability_values) / total)
    conflict_avg = float(sum(conflict_values) / total)
    areal_support_avg = float(sum(areal_support_values) / total)
    areal_conflict_avg = float(sum(areal_conflict_values) / total)
    drift_avg = float(sum(areal_dynamic_values) / total)

    valence_variance = float(sum((value - valence_avg) ** 2 for value in valences) / total)
    bearing_variance = float(sum((value - bearing_avg) ** 2 for value in bearings) / total)
    areal_support_variance = float(sum((value - areal_support_avg) ** 2 for value in areal_support_values) / total)
    areal_conflict_variance = float(sum((value - areal_conflict_avg) ** 2 for value in areal_conflict_values) / total)

    positive_ratio = float(sum(_clip01(max(0.0, value) / 0.36) for value in valences) / total)
    negative_ratio = float(sum(_clip01(max(0.0, -value) / 0.36) for value in valences) / total)
    neutral_ratio = float(sum(_clip01(1.0 - (abs(value) / 0.24)) for value in valences) / total)
    euphoric_ratio = float(sum(1.0 for item in felt_items if item["label"] == "euphoric") / total)
    burden_ratio = float(sum(1.0 for item in felt_items if item["label"] == "burdened") / total)
    conflict_ratio = float(sum(_clip01(value / 0.55) for value in conflict_values) / total)
    areal_fragmented_ratio = float(sum(_clip01(value / 0.48) for value in fragmentation_values) / total)
    areal_supported_ratio = float(sum(_clip01(value / 0.58) for value in areal_support_values) / total)

    coherence_avg = float(max(0.0, min(1.0, 1.0 - ((valence_variance * 0.58) + (bearing_variance * 0.66) + (areal_support_variance * 0.46) + (areal_conflict_variance * 0.52) + (conflict_ratio * 0.40)))))
    felt_stability = float(max(0.0, min(1.0, (stability_avg * 0.28) + (coherence_avg * 0.22) + (bearing_avg * 0.16) + (areal_support_avg * 0.18) - (areal_conflict_avg * 0.12) - (drift_avg * 0.06))))

    if len(valences) >= 2:
        trend_value = float((valences[-1] + areal_support_values[-1] - areal_conflict_values[-1]) - (valences[0] + areal_support_values[0] - areal_conflict_values[0]))
    else:
        trend_value = 0.0

    felt_trend_pressures = {
        "up": _clip01(max(0.0, trend_value) / 0.28),
        "down": _clip01(max(0.0, -trend_value) / 0.28),
        "flat": _clip01(1.0 - (abs(trend_value) / 0.28)),
    }
    felt_trend = max(felt_trend_pressures, key=felt_trend_pressures.get)

    felt_bearing_score = float(max(
        0.0,
        min(
            1.0,
            (bearing_avg * 0.24)
            + (regulation_avg * 0.16)
            + (felt_stability * 0.16)
            + (coherence_avg * 0.10)
            + (max(0.0, valence_avg) * 0.08)
            + (areal_support_avg * 0.18)
            - (recovery_avg * 0.14)
            - (burden_ratio * 0.10)
            - (euphoric_ratio * 0.06)
            - (areal_conflict_avg * 0.12)
            - (areal_fragmented_ratio * 0.08),
        ),
    ))

    felt_profile_pressures = {
        "stable_bearing": _clip01(
            (felt_bearing_score * 0.26)
            + (felt_stability * 0.22)
            + (areal_supported_ratio * 0.18)
            + ((1.0 - areal_fragmented_ratio) * 0.10)
        ),
        "fragmented_conflict": _clip01((areal_fragmented_ratio * 0.34) + (areal_conflict_avg * 0.24)),
        "euphoric_risk": _clip01((euphoric_ratio * 0.32) + ((1.0 - bearing_avg) * 0.10)),
        "burdened": _clip01((burden_ratio * 0.30) + (recovery_avg * 0.22)),
        "recovering": _clip01(
            (felt_trend_pressures.get("up", 0.0) * 0.20)
            + ((1.0 - recovery_avg) * 0.14)
            + ((1.0 - burden_ratio) * 0.10)
            + ((1.0 - areal_conflict_avg) * 0.08)
        ),
        "volatile_bearing": _clip01((valence_variance * 2.0) + (bearing_variance * 2.4) + (areal_support_variance * 1.6)),
        "mixed_unclear": _clip01((1.0 - max(felt_bearing_score, felt_stability, areal_supported_ratio)) * 0.20),
    }
    felt_profile_label = max(felt_profile_pressures, key=felt_profile_pressures.get)

    felt_history = []
    for item in felt_items[-24:]:
        felt_history.append({
            "timestamp": item.get("timestamp", None),
            "valence": float(item.get("valence", 0.0) or 0.0),
            "bearing": float(item.get("bearing", 0.0) or 0.0),
            "regulation_quality": float(item.get("regulation_quality", 0.0) or 0.0),
            "burden": float(item.get("burden", 0.0) or 0.0),
            "overactivation": float(item.get("overactivation", 0.0) or 0.0),
            "areal_support": float(item.get("areal_support", 0.0) or 0.0),
            "areal_conflict_pressure": float(item.get("areal_conflict_pressure", 0.0) or 0.0),
            "field_areal_fragmentation": float(item.get("field_areal_fragmentation", 0.0) or 0.0),
            "label": str(item.get("label", "mixed") or "mixed"),
        })

    return {
        "distribution": {
            "positive_ratio": float(positive_ratio),
            "negative_ratio": float(negative_ratio),
            "neutral_ratio": float(neutral_ratio),
            "euphoric_ratio": float(euphoric_ratio),
            "burden_ratio": float(burden_ratio),
            "areal_fragmented_ratio": float(areal_fragmented_ratio),
            "areal_supported_ratio": float(areal_supported_ratio),
        },
        "averages": {
            "felt_valence_avg": float(valence_avg),
            "felt_bearing_avg": float(bearing_avg),
            "felt_regulation_quality_avg": float(regulation_avg),
            "felt_recovery_cost_avg": float(recovery_avg),
            "felt_areal_support_avg": float(areal_support_avg),
            "felt_areal_conflict_avg": float(areal_conflict_avg),
        },
        "variance": {
            "felt_valence_variance": float(valence_variance),
            "felt_bearing_variance": float(bearing_variance),
            "felt_areal_support_variance": float(areal_support_variance),
            "felt_areal_conflict_variance": float(areal_conflict_variance),
        },
        "stability": {
            "felt_stability": float(felt_stability),
            "felt_coherence_avg": float(coherence_avg),
            "felt_conflict_ratio": float(conflict_ratio),
            "felt_areal_support_avg": float(areal_support_avg),
            "felt_areal_conflict_avg": float(areal_conflict_avg),
        },
        "dynamic": {
            "felt_drift_avg": float(drift_avg),
            "felt_trend": str(felt_trend),
            "felt_trend_pressures": dict(felt_trend_pressures),
            "felt_areal_drift_avg": float(sum(areal_dynamic_values) / total),
        },
        "felt_bearing_score": float(felt_bearing_score),
        "felt_profile_label": str(felt_profile_label),
        "felt_profile_pressures": dict(felt_profile_pressures),
        "felt_history": list(felt_history),
    }

# --------------------------------------------------
def _derive_felt_label(
    valence,
    bearing,
    overactivation,
    burden,
    regulation_quality,
    conflict,
    recovery_cost,
    areal_support=0.0,
    areal_conflict_pressure=0.0,
    field_areal_fragmentation=0.0,
    processing_areal_tension=0.0,
    thought_areal_pressure=0.0,
):

    label_pressures = {
        "euphoric": _clip01((overactivation * 0.30) + (max(0.0, valence) * 0.20) + ((1.0 - areal_conflict_pressure) * 0.08)),
        "fragmented_conflict": _clip01(
            (areal_conflict_pressure * 0.24)
            + (field_areal_fragmentation * 0.22)
            + (processing_areal_tension * 0.16)
            + (thought_areal_pressure * 0.16)
        ),
        "burdened": _clip01((burden * 0.30) + (recovery_cost * 0.26)),
        "stable_bearing": _clip01(
            (bearing * 0.24)
            + (regulation_quality * 0.22)
            + ((1.0 - conflict) * 0.12)
            + (areal_support * 0.16)
            + ((1.0 - areal_conflict_pressure) * 0.08)
        ),
        "recovering": _clip01(
            (bearing * 0.20)
            + (areal_support * 0.18)
            + ((1.0 - recovery_cost) * 0.12)
            + ((1.0 - conflict) * 0.10)
        ),
        "conflicted": _clip01(conflict * 0.34),
        "neutral": _clip01(
            (1.0 - abs(valence)) * 0.10
            + (1.0 - abs(bearing)) * 0.10
            + ((1.0 - areal_support) * 0.06)
            + ((1.0 - areal_conflict_pressure) * 0.06)
        ),
        "volatile_bearing": _clip01((field_areal_fragmentation * 0.26) + (areal_conflict_pressure * 0.20)),
        "strained": _clip01(max(0.0, -valence) * 0.34 + burden * 0.08),
        "mixed": _clip01((1.0 - max(abs(valence), bearing, conflict, burden, areal_support)) * 0.20),
    }
    return max(label_pressures, key=label_pressures.get)

# --------------------------------------------------
def _build_episode_felt_summary(summary):

    item = dict(summary or {})
    felt_state = dict(item.get("felt_state", {}) or {})
    state_delta = dict(item.get("state_delta", {}) or {})
    field_delta = dict(state_delta.get("field", {}) or {})
    experience_delta = dict(state_delta.get("experience", {}) or {})

    perception_quality = float(item.get("perception_quality", 0.0) or 0.0)
    felt_quality = float(item.get("felt_quality", 0.0) or 0.0)
    thought_quality = float(item.get("thought_quality", 0.0) or 0.0)
    review_score = float(item.get("review_score", 0.0) or 0.0)
    decision_path_quality = float(item.get("decision_path_quality", 0.0) or 0.0)
    uncertainty_quality = float(item.get("uncertainty_recognition_quality", 0.0) or 0.0)
    observation_quality = float(item.get("observation_quality", 0.0) or 0.0)
    correction_quality = float(item.get("correction_timing_quality", 0.0) or 0.0)
    structural_bearing_quality = float(item.get("structural_bearing_quality", 0.0) or 0.0)

    confidence = float(item.get("focus_confidence", 0.0) or 0.0)
    competition_bias = abs(float(item.get("competition_bias", 0.0) or 0.0))
    pressure_delta = float(field_delta.get("regulatory_load", 0.0) or 0.0)
    capacity_delta = float(field_delta.get("action_capacity", 0.0) or 0.0)
    recovery_delta = float(field_delta.get("recovery_need", 0.0) or 0.0)
    survival_delta = float(field_delta.get("survival_pressure", 0.0) or 0.0)
    release_delta = float(experience_delta.get("pressure_release", 0.0) or 0.0)
    bearing_delta = float(experience_delta.get("load_bearing_capacity", 0.0) or 0.0)
    field_areal_pressure_mean = float(item.get("field_areal_pressure_mean", 0.0) or 0.0)
    field_areal_stability_mean = float(item.get("field_areal_stability_mean", 0.0) or 0.0)
    field_areal_dominance = float(item.get("field_areal_dominance", 0.0) or 0.0)
    field_areal_fragmentation = float(item.get("field_areal_fragmentation", 0.0) or 0.0)
    field_areal_coherence_mean = float(item.get("field_areal_coherence_mean", 0.0) or 0.0)
    field_areal_conflict_mean = float(item.get("field_areal_conflict_mean", 0.0) or 0.0)
    processing_areal_tension = float(item.get("processing_areal_tension", 0.0) or 0.0)
    processing_areal_support = float(item.get("processing_areal_support", 0.0) or 0.0)
    thought_areal_pressure = float(item.get("thought_areal_pressure", 0.0) or 0.0)
    thought_areal_support = float(item.get("thought_areal_support", 0.0) or 0.0)
    areal_support = float(felt_state.get("areal_support", 0.0) or 0.0)
    areal_conflict_pressure = float(felt_state.get("areal_conflict_pressure", 0.0) or 0.0)
    delta_areal_pressure = float(field_delta.get("field_areal_pressure_mean", 0.0) or 0.0)
    delta_areal_fragmentation = float(field_delta.get("field_areal_fragmentation", 0.0) or 0.0)
    delta_areal_conflict = float(field_delta.get("field_areal_conflict_mean", 0.0) or 0.0)
    neural_felt_state = dict(item.get("neural_felt_state", felt_state.get("neural_felt_state", {})) or {})
    neural_felt_bearing = float(item.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", felt_state.get("neural_felt_bearing", 0.0))) or 0.0)
    neural_felt_pressure = float(item.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", felt_state.get("neural_felt_pressure", 0.0))) or 0.0)
    neural_felt_memory_resonance = float(item.get("neural_felt_memory_resonance", neural_felt_state.get("neural_felt_memory_resonance", felt_state.get("neural_felt_memory_resonance", 0.0))) or 0.0)
    neural_felt_context_reactivation = float(item.get("neural_felt_context_reactivation", neural_felt_state.get("neural_felt_context_reactivation", felt_state.get("neural_felt_context_reactivation", 0.0))) or 0.0)
    neural_felt_label = str(item.get("neural_felt_label", neural_felt_state.get("neural_felt_label", felt_state.get("neural_felt_label", "quiet_neural_felt"))) or "quiet_neural_felt")

    raw_valence = (
        (felt_quality * 0.20)
        + (review_score * 0.14)
        + (thought_quality * 0.08)
        + (release_delta * 0.18)
        + (areal_support * 0.10)
        + (field_areal_stability_mean * 0.08)
        + (field_areal_coherence_mean * 0.06)
        + (processing_areal_support * 0.06)
        + (thought_areal_support * 0.06)
        - (pressure_delta * 0.18)
        - (survival_delta * 0.14)
        - (recovery_delta * 0.10)
        - (areal_conflict_pressure * 0.14)
        - (field_areal_pressure_mean * 0.08)
        - (field_areal_fragmentation * 0.06)
    )

    valence = float(max(-1.0, min(1.0, raw_valence)))
    bearing = float(max(
        0.0,
        min(
            1.0,
            (structural_bearing_quality * 0.18)
            + (decision_path_quality * 0.10)
            + (capacity_delta * 0.16)
            + (bearing_delta * 0.18)
            + (confidence * 0.08)
            + (areal_support * 0.14)
            + (field_areal_stability_mean * 0.10)
            + (field_areal_coherence_mean * 0.08)
            + (field_areal_dominance * 0.06)
            + (processing_areal_support * 0.08)
            + (thought_areal_support * 0.08)
            - (pressure_delta * 0.12)
            - (recovery_delta * 0.08)
            - (field_areal_fragmentation * 0.08)
            - (field_areal_conflict_mean * 0.10),
        ),
    ))
    overactivation = float(max(
        0.0,
        min(
            1.0,
            competition_bias
            + max(0.0, pressure_delta * 0.26)
            + max(0.0, survival_delta * 0.18)
            + (areal_conflict_pressure * 0.18)
            + (field_areal_pressure_mean * 0.14)
            + (processing_areal_tension * 0.12)
            - (release_delta * 0.12)
            - (processing_areal_support * 0.10),
        ),
    ))
    burden = float(max(
        0.0,
        min(
            1.0,
            (pressure_delta * 0.24)
            + (recovery_delta * 0.20)
            + (survival_delta * 0.18)
            + (areal_conflict_pressure * 0.16)
            + (field_areal_fragmentation * 0.12)
            + (field_areal_conflict_mean * 0.12)
            - (capacity_delta * 0.12)
            - (release_delta * 0.10)
            - (areal_support * 0.10),
        ),
    ))
    regulation_quality = float(max(
        0.0,
        min(
            1.0,
            (review_score * 0.14)
            + (observation_quality * 0.10)
            + (correction_quality * 0.14)
            + (uncertainty_quality * 0.12)
            + (release_delta * 0.12)
            + (bearing_delta * 0.08)
            + (areal_support * 0.12)
            + (processing_areal_support * 0.10)
            + (thought_areal_support * 0.08)
            - (competition_bias * 0.10)
            - (areal_conflict_pressure * 0.12)
            - (processing_areal_tension * 0.08)
            - (thought_areal_pressure * 0.08),
        ),
    ))
    stability = float(max(
        0.0,
        min(
            1.0,
            (bearing * 0.26)
            + (regulation_quality * 0.18)
            + (confidence * 0.12)
            + (areal_support * 0.16)
            + (processing_areal_support * 0.10)
            + (thought_areal_support * 0.08)
            - (overactivation * 0.14)
            - (burden * 0.12)
            - (areal_conflict_pressure * 0.10),
        ),
    ))
    conflict = float(max(
        0.0,
        min(
            1.0,
            (abs(valence) * 0.08)
            + (competition_bias * 0.20)
            + max(0.0, pressure_delta - capacity_delta) * 0.16
            + max(0.0, 0.5 - regulation_quality) * 0.12
            + (field_areal_conflict_mean * 0.16)
            + (field_areal_fragmentation * 0.12)
            + (areal_conflict_pressure * 0.12)
            + (thought_areal_pressure * 0.08),
        ),
    ))
    recovery_cost = float(max(
        0.0,
        min(
            1.0,
            (recovery_delta * 0.34)
            + (burden * 0.20)
            + (conflict * 0.14)
            + (areal_conflict_pressure * 0.12)
            + (max(0.0, delta_areal_fragmentation) * 0.08)
            + (max(0.0, delta_areal_conflict) * 0.08)
            + (max(0.0, delta_areal_pressure) * 0.08)
            - (release_delta * 0.14)
            - (areal_support * 0.10),
        ),
    ))

    felt_label = _derive_felt_label(
        valence,
        bearing,
        overactivation,
        burden,
        regulation_quality,
        conflict,
        recovery_cost,
        areal_support=areal_support,
        areal_conflict_pressure=areal_conflict_pressure,
        field_areal_fragmentation=field_areal_fragmentation,
        processing_areal_tension=processing_areal_tension,
        thought_areal_pressure=thought_areal_pressure,
    )

    return {
        "valence": float(valence),
        "bearing": float(bearing),
        "overactivation": float(overactivation),
        "burden": float(burden),
        "regulation_quality": float(regulation_quality),
        "stability": float(stability),
        "confidence": float(confidence),
        "conflict": float(conflict),
        "recovery_cost": float(recovery_cost),
        "areal_support": float(areal_support),
        "areal_conflict_pressure": float(areal_conflict_pressure),
        "neural_felt_state": dict(neural_felt_state or {}),
        "neural_felt_bearing": float(neural_felt_bearing),
        "neural_felt_pressure": float(neural_felt_pressure),
        "neural_felt_memory_resonance": float(neural_felt_memory_resonance),
        "neural_felt_context_reactivation": float(neural_felt_context_reactivation),
        "neural_felt_label": str(neural_felt_label),
        "field_areal_fragmentation": float(field_areal_fragmentation),
        "field_areal_conflict_mean": float(field_areal_conflict_mean),
        "processing_areal_tension": float(processing_areal_tension),
        "processing_areal_support": float(processing_areal_support),
        "thought_areal_pressure": float(thought_areal_pressure),
        "thought_areal_support": float(thought_areal_support),
        "felt_label": str(felt_label),
    }

# --------------------------------------------------
def _complete_experience_episode_summary(summary):

    item = dict(summary or {})
    episode_felt_summary = _build_episode_felt_summary(item)

    item["episode_felt_summary"] = dict(episode_felt_summary or {})
    item["felt_valence"] = float(episode_felt_summary.get("valence", 0.0) or 0.0)
    item["felt_bearing"] = float(episode_felt_summary.get("bearing", 0.0) or 0.0)
    item["felt_overactivation"] = float(episode_felt_summary.get("overactivation", 0.0) or 0.0)
    item["felt_burden"] = float(episode_felt_summary.get("burden", 0.0) or 0.0)
    item["felt_regulation_quality"] = float(episode_felt_summary.get("regulation_quality", 0.0) or 0.0)
    item["felt_stability"] = float(episode_felt_summary.get("stability", 0.0) or 0.0)
    item["felt_confidence"] = float(episode_felt_summary.get("confidence", 0.0) or 0.0)
    item["felt_conflict"] = float(episode_felt_summary.get("conflict", 0.0) or 0.0)
    item["felt_recovery_cost"] = float(episode_felt_summary.get("recovery_cost", 0.0) or 0.0)
    item["felt_label"] = str(episode_felt_summary.get("felt_label", "mixed") or "mixed")
    item["neural_felt_memory_resonance"] = float(episode_felt_summary.get("neural_felt_memory_resonance", item.get("neural_felt_memory_resonance", 0.0)) or 0.0)
    item["neural_felt_context_reactivation"] = float(episode_felt_summary.get("neural_felt_context_reactivation", item.get("neural_felt_context_reactivation", 0.0)) or 0.0)

    state_delta = dict(item.get("state_delta", {}) or {})
    field_delta = dict(state_delta.get("field", {}) or {})
    tension_delta = dict(state_delta.get("tension", {}) or {})

    pressure_cost = float(
        min(
            1.0,
            max(0.0, float(item.get("in_trade_avg_pressure_to_capacity", 0.0) or 0.0) / 2.0),
        )
    )
    destabilization_cost = float(max(0.0, -float(tension_delta.get("stability", 0.0) or 0.0)))
    energy_disturbance = float(min(1.0, abs(float(tension_delta.get("energy", 0.0) or 0.0))))
    delta_pressure_cost = float(min(1.0, max(0.0, float(field_delta.get("regulatory_load", 0.0) or 0.0))))
    areal_pressure_cost = float(min(1.0, max(0.0, float(item.get("in_trade_avg_field_areal_pressure_mean", item.get("field_areal_pressure_mean", 0.0)) or 0.0))))
    areal_fragmentation_cost = float(min(1.0, max(0.0, float(item.get("in_trade_avg_field_areal_fragmentation", item.get("field_areal_fragmentation", 0.0)) or 0.0))))
    delta_areal_pressure_cost = float(min(1.0, max(0.0, float(field_delta.get("field_areal_pressure_mean", 0.0) or 0.0))))
    delta_areal_fragmentation_cost = float(min(1.0, max(0.0, float(field_delta.get("field_areal_fragmentation", 0.0) or 0.0))))
    delta_areal_conflict_cost = float(min(1.0, max(0.0, float(field_delta.get("field_areal_conflict_mean", 0.0) or 0.0))))
    areal_support_room = float(
        max(
            0.0,
            min(
                1.0,
                (float(item.get("field_areal_stability_mean", 0.0) or 0.0) * 0.28)
                + (float(item.get("field_areal_coherence_mean", 0.0) or 0.0) * 0.24)
                + (float(item.get("field_areal_dominance", 0.0) or 0.0) * 0.14)
                + (float(item.get("processing_areal_support", 0.0) or 0.0) * 0.18)
                + (float(item.get("thought_areal_support", 0.0) or 0.0) * 0.16)
            ),
        )
    )

    item["experience_friction_cost"] = float(
        max(
            0.0,
            min(
                1.0,
                (pressure_cost * 0.26)
                + (destabilization_cost * 0.18)
                + (delta_pressure_cost * 0.08)
                + (areal_pressure_cost * 0.10)
                + (areal_fragmentation_cost * 0.08)
                + (delta_areal_pressure_cost * 0.04)
                + (delta_areal_fragmentation_cost * 0.02)
                + (delta_areal_conflict_cost * 0.02),
            ),
        )
    )

    item["experience_energy_cost"] = float(
        max(
            0.0,
            min(
                1.0,
                (energy_disturbance * 0.46)
                + (min(1.0, destabilization_cost) * 0.38)
                + (delta_areal_conflict_cost * 0.10)
                + (delta_areal_fragmentation_cost * 0.06),
            ),
        )
    )

    item["experience_bearing_room"] = float(
        max(
            0.0,
            min(
                1.0,
                (float(item.get("carrying_room", 0.0) or 0.0) * 0.34)
                + (float(item.get("felt_bearing", 0.0) or 0.0) * 0.22)
                + (float(item.get("relief_quality", 0.0) or 0.0) * 0.14)
                + (areal_support_room * 0.18)
                + (float(item.get("thought_areal_support", 0.0) or 0.0) * 0.12),
            ),
        )
    )

    neurochemical_effect = build_experience_neurochemical_effect(item)
    item["experience_neurochemical_effect"] = dict(neurochemical_effect or {})
    item["experience_effect_score"] = float(neurochemical_effect.get("experience_effect_score", 0.0) or 0.0)
    item["profit_reward"] = float(neurochemical_effect.get("profit_reward", 0.0) or 0.0)
    item["relief_signal"] = float(neurochemical_effect.get("relief_signal", 0.0) or 0.0)
    item["stability_signal"] = float(neurochemical_effect.get("stability_signal", 0.0) or 0.0)
    item["discipline_signal"] = float(neurochemical_effect.get("discipline_signal", 0.0) or 0.0)
    item["confidence_signal"] = float(neurochemical_effect.get("confidence_signal", 0.0) or 0.0)
    item["overactivation_signal"] = float(neurochemical_effect.get("overactivation_signal", 0.0) or 0.0)
    item["chaos_penalty"] = float(neurochemical_effect.get("chaos_penalty", 0.0) or 0.0)
    item["variance_penalty"] = float(neurochemical_effect.get("variance_penalty", 0.0) or 0.0)
    item["overstrain_penalty"] = float(neurochemical_effect.get("overstrain_penalty", 0.0) or 0.0)
    item["carrying_capacity_delta"] = float(neurochemical_effect.get("carrying_capacity_delta", 0.0) or 0.0)
    item["self_confidence_delta"] = float(neurochemical_effect.get("self_confidence_delta", 0.0) or 0.0)
    item["process_quality"] = float(neurochemical_effect.get("process_quality", 0.0) or 0.0)

    return dict(item)

# --------------------------------------------------
def _compact_in_trade_update_payload(payload):

    item = dict(payload or {})
    state_before = dict(item.get("state_before", {}) or {})
    state_after = dict(item.get("state_after", {}) or {})
    state_delta = dict(item.get("state_delta", {}) or {})
    field_after = dict(state_after.get("field", {}) or {})
    experience_after = dict(state_after.get("experience", {}) or {})
    tension_after = dict(state_after.get("tension", {}) or {})
    position_intervention = dict(item.get("position_intervention_state", {}) or {})

    compact = {
        "entry": float(item.get("entry", 0.0) or 0.0),
        "tp": float(item.get("tp", 0.0) or 0.0),
        "sl": float(item.get("sl", 0.0) or 0.0),
        "risk": float(item.get("risk", 0.0) or 0.0),
        "rr": float(item.get("rr", 0.0) or 0.0),
        "mfe": float(item.get("mfe", 0.0) or 0.0),
        "mae": float(item.get("mae", 0.0) or 0.0),
        "bars_open": int(item.get("bars_open", 0) or 0),
        "fill_ratio": float(item.get("fill_ratio", 0.0) or 0.0),
        "regulatory_load": float(item.get("regulatory_load", field_after.get("regulatory_load", 0.0)) or 0.0),
        "action_capacity": float(item.get("action_capacity", field_after.get("action_capacity", 0.0)) or 0.0),
        "recovery_need": float(item.get("recovery_need", field_after.get("recovery_need", 0.0)) or 0.0),
        "survival_pressure": float(item.get("survival_pressure", field_after.get("survival_pressure", 0.0)) or 0.0),
        "pressure_to_capacity": float(item.get("pressure_to_capacity", field_after.get("pressure_to_capacity", 0.0)) or 0.0),
        "pressure_release": float(item.get("pressure_release", experience_after.get("pressure_release", 0.0)) or 0.0),
        "load_bearing_capacity": float(item.get("load_bearing_capacity", experience_after.get("load_bearing_capacity", 0.0)) or 0.0),
        "state_stability": float(item.get("state_stability", tension_after.get("stability", 0.0)) or 0.0),
        "capacity_reserve": float(item.get("capacity_reserve", field_after.get("capacity_reserve", 0.0)) or 0.0),
        "recovery_balance": float(item.get("recovery_balance", field_after.get("recovery_balance", 0.0)) or 0.0),
        "regulated_courage": float(item.get("regulated_courage", 0.0) or 0.0),
        "courage_gap": float(item.get("courage_gap", 0.0) or 0.0),
        "position_inconsistency_stress": float(position_intervention.get("position_inconsistency_stress", 0.0) or 0.0),
        "position_mcm_field_strain": float(position_intervention.get("position_mcm_field_strain", 0.0) or 0.0),
        "position_self_trust_gap": float(position_intervention.get("position_self_trust_gap", 0.0) or 0.0),
        "position_cortisol_load": float(position_intervention.get("position_cortisol_load", 0.0) or 0.0),
        "position_noradrenaline_arousal": float(position_intervention.get("position_noradrenaline_arousal", 0.0) or 0.0),
        "position_protective_distance": float(position_intervention.get("position_protective_distance", 0.0) or 0.0),
        "position_held_risk_discomfort": float(position_intervention.get("position_held_risk_discomfort", 0.0) or 0.0),
        "position_process_quality": float(position_intervention.get("position_process_quality", 0.0) or 0.0),
        "position_experience_label": str(position_intervention.get("position_experience_label", "-") or "-"),
        "field_areal_count": int(item.get("field_areal_count", field_after.get("field_areal_count", 0)) or 0),
        "field_areal_activation_mean": float(item.get("field_areal_activation_mean", field_after.get("field_areal_activation_mean", 0.0)) or 0.0),
        "field_areal_stability_mean": float(item.get("field_areal_stability_mean", field_after.get("field_areal_stability_mean", 0.0)) or 0.0),
        "field_areal_pressure_mean": float(item.get("field_areal_pressure_mean", field_after.get("field_areal_pressure_mean", 0.0)) or 0.0),
        "field_areal_drift": float(item.get("field_areal_drift", field_after.get("field_areal_drift", 0.0)) or 0.0),
        "field_areal_dominance": float(item.get("field_areal_dominance", field_after.get("field_areal_dominance", 0.0)) or 0.0),
        "field_areal_fragmentation": float(item.get("field_areal_fragmentation", field_after.get("field_areal_fragmentation", 0.0)) or 0.0),
        "field_areal_coherence_mean": float(item.get("field_areal_coherence_mean", field_after.get("field_areal_coherence_mean", 0.0)) or 0.0),
        "field_areal_conflict_mean": float(item.get("field_areal_conflict_mean", field_after.get("field_areal_conflict_mean", 0.0)) or 0.0),
        "pre_action_phase": str(item.get("pre_action_phase", "hold") or "hold"),
        "dominant_tension_cause": str(item.get("dominant_tension_cause", "-") or "-"),
        "decision_tendency": str(item.get("decision_tendency", "hold") or "hold"),
        "proposed_decision": str(item.get("proposed_decision", "WAIT") or "WAIT"),
        "reason": str(item.get("reason", "-") or "-"),
        "state_before": dict(state_before or {}),
        "state_after": dict(state_after or {}),
        "state_delta": dict(state_delta or {}),
    }

    return dict(compact)

# --------------------------------------------------
def _summarize_in_trade_updates(in_trade_updates):

    updates = [dict(item or {}) for item in list(in_trade_updates or []) if isinstance(item, dict)]
    if not updates:
        return {
            "in_trade_update_count": 0,
            "in_trade_max_mfe": 0.0,
            "in_trade_max_mae": 0.0,
            "in_trade_last_bars_open": 0,
            "in_trade_avg_fill_ratio": 0.0,
            "in_trade_direction_stability": 0.0,
            "in_trade_avg_regulatory_load": 0.0,
            "in_trade_avg_action_capacity": 0.0,
            "in_trade_avg_recovery_need": 0.0,
            "in_trade_avg_survival_pressure": 0.0,
            "in_trade_avg_pressure_to_capacity": 0.0,
            "in_trade_avg_pressure_release": 0.0,
            "in_trade_avg_load_bearing_capacity": 0.0,
            "in_trade_avg_state_stability": 0.0,
            "in_trade_avg_capacity_reserve": 0.0,
            "in_trade_avg_recovery_balance": 0.0,
            "in_trade_avg_regulated_courage": 0.0,
            "in_trade_avg_courage_gap": 0.0,
            "in_trade_avg_position_inconsistency_stress": 0.0,
            "in_trade_avg_position_mcm_field_strain": 0.0,
            "in_trade_avg_position_self_trust_gap": 0.0,
            "in_trade_avg_position_cortisol_load": 0.0,
            "in_trade_avg_position_noradrenaline_arousal": 0.0,
            "in_trade_avg_position_protective_distance": 0.0,
            "in_trade_avg_position_held_risk_discomfort": 0.0,
            "in_trade_avg_position_process_quality": 0.0,
            "in_trade_last_position_experience_label": "-",
            "in_trade_avg_field_areal_count": 0.0,
            "in_trade_avg_field_areal_activation_mean": 0.0,
            "in_trade_avg_field_areal_stability_mean": 0.0,
            "in_trade_avg_field_areal_pressure_mean": 0.0,
            "in_trade_avg_field_areal_drift": 0.0,
            "in_trade_avg_field_areal_dominance": 0.0,
            "in_trade_avg_field_areal_fragmentation": 0.0,
            "in_trade_avg_field_areal_coherence_mean": 0.0,
            "in_trade_avg_field_areal_conflict_mean": 0.0,
            "in_trade_last_pre_action_phase": "-",
            "in_trade_last_dominant_tension_cause": "-",
            "in_trade_last_state_before": {},
            "in_trade_last_state_after": {},
            "in_trade_last_state_delta": {},
        }

    payloads = [dict(item.get("payload", {}) or {}) for item in updates]

    mfe_values = [float(item.get("mfe", 0.0) or 0.0) for item in payloads]
    mae_values = [float(item.get("mae", 0.0) or 0.0) for item in payloads]
    bars_open_values = [int(item.get("bars_open", 0) or 0) for item in payloads]
    fill_ratio_values = [float(item.get("fill_ratio", 0.0) or 0.0) for item in payloads]
    regulatory_load_values = [float(item.get("regulatory_load", 0.0) or 0.0) for item in payloads]
    action_capacity_values = [float(item.get("action_capacity", 0.0) or 0.0) for item in payloads]
    recovery_need_values = [float(item.get("recovery_need", 0.0) or 0.0) for item in payloads]
    survival_pressure_values = [float(item.get("survival_pressure", 0.0) or 0.0) for item in payloads]
    pressure_to_capacity_values = [float(item.get("pressure_to_capacity", 0.0) or 0.0) for item in payloads]
    pressure_release_values = [float(item.get("pressure_release", 0.0) or 0.0) for item in payloads]
    load_bearing_capacity_values = [float(item.get("load_bearing_capacity", 0.0) or 0.0) for item in payloads]
    state_stability_values = [float(item.get("state_stability", 0.0) or 0.0) for item in payloads]
    capacity_reserve_values = [float(item.get("capacity_reserve", 0.0) or 0.0) for item in payloads]
    recovery_balance_values = [float(item.get("recovery_balance", 0.0) or 0.0) for item in payloads]
    regulated_courage_values = [float(item.get("regulated_courage", 0.0) or 0.0) for item in payloads]
    courage_gap_values = [float(item.get("courage_gap", 0.0) or 0.0) for item in payloads]
    position_inconsistency_stress_values = [float(item.get("position_inconsistency_stress", 0.0) or 0.0) for item in payloads]
    position_mcm_field_strain_values = [float(item.get("position_mcm_field_strain", 0.0) or 0.0) for item in payloads]
    position_self_trust_gap_values = [float(item.get("position_self_trust_gap", 0.0) or 0.0) for item in payloads]
    position_cortisol_load_values = [float(item.get("position_cortisol_load", 0.0) or 0.0) for item in payloads]
    position_noradrenaline_arousal_values = [float(item.get("position_noradrenaline_arousal", 0.0) or 0.0) for item in payloads]
    position_protective_distance_values = [float(item.get("position_protective_distance", 0.0) or 0.0) for item in payloads]
    position_held_risk_discomfort_values = [float(item.get("position_held_risk_discomfort", 0.0) or 0.0) for item in payloads]
    position_process_quality_values = [float(item.get("position_process_quality", 0.0) or 0.0) for item in payloads]
    field_areal_count_values = [float(item.get("field_areal_count", 0.0) or 0.0) for item in payloads]
    field_areal_activation_values = [float(item.get("field_areal_activation_mean", 0.0) or 0.0) for item in payloads]
    field_areal_stability_values = [float(item.get("field_areal_stability_mean", 0.0) or 0.0) for item in payloads]
    field_areal_pressure_values = [float(item.get("field_areal_pressure_mean", 0.0) or 0.0) for item in payloads]
    field_areal_drift_values = [float(item.get("field_areal_drift", 0.0) or 0.0) for item in payloads]
    field_areal_dominance_values = [float(item.get("field_areal_dominance", 0.0) or 0.0) for item in payloads]
    field_areal_fragmentation_values = [float(item.get("field_areal_fragmentation", 0.0) or 0.0) for item in payloads]
    field_areal_coherence_values = [float(item.get("field_areal_coherence_mean", 0.0) or 0.0) for item in payloads]
    field_areal_conflict_values = [float(item.get("field_areal_conflict_mean", 0.0) or 0.0) for item in payloads]

    direction_values = []
    for item in payloads:
        proposed_decision = str(item.get("proposed_decision", "WAIT") or "WAIT").strip().upper()

        if proposed_decision == "LONG":
            direction_values.append(1.0)
        elif proposed_decision == "SHORT":
            direction_values.append(-1.0)
        else:
            direction_values.append(0.0)

    direction_stability = 0.0
    if direction_values:
        direction_stability = abs(sum(direction_values) / max(1, len(direction_values)))

    last_payload = dict(payloads[-1] or {}) if payloads else {}

    return {
        "in_trade_update_count": int(len(updates)),
        "in_trade_max_mfe": float(max(mfe_values) if mfe_values else 0.0),
        "in_trade_max_mae": float(max(mae_values) if mae_values else 0.0),
        "in_trade_last_bars_open": int(bars_open_values[-1] if bars_open_values else 0),
        "in_trade_avg_fill_ratio": float(sum(fill_ratio_values) / max(1, len(fill_ratio_values))),
        "in_trade_direction_stability": float(direction_stability),
        "in_trade_avg_regulatory_load": float(sum(regulatory_load_values) / max(1, len(regulatory_load_values))),
        "in_trade_avg_action_capacity": float(sum(action_capacity_values) / max(1, len(action_capacity_values))),
        "in_trade_avg_recovery_need": float(sum(recovery_need_values) / max(1, len(recovery_need_values))),
        "in_trade_avg_survival_pressure": float(sum(survival_pressure_values) / max(1, len(survival_pressure_values))),
        "in_trade_avg_pressure_to_capacity": float(sum(pressure_to_capacity_values) / max(1, len(pressure_to_capacity_values))),
        "in_trade_avg_pressure_release": float(sum(pressure_release_values) / max(1, len(pressure_release_values))),
        "in_trade_avg_load_bearing_capacity": float(sum(load_bearing_capacity_values) / max(1, len(load_bearing_capacity_values))),
        "in_trade_avg_state_stability": float(sum(state_stability_values) / max(1, len(state_stability_values))),
        "in_trade_avg_capacity_reserve": float(sum(capacity_reserve_values) / max(1, len(capacity_reserve_values))),
        "in_trade_avg_recovery_balance": float(sum(recovery_balance_values) / max(1, len(recovery_balance_values))),
        "in_trade_avg_regulated_courage": float(sum(regulated_courage_values) / max(1, len(regulated_courage_values))),
        "in_trade_avg_courage_gap": float(sum(courage_gap_values) / max(1, len(courage_gap_values))),
        "in_trade_avg_position_inconsistency_stress": float(sum(position_inconsistency_stress_values) / max(1, len(position_inconsistency_stress_values))),
        "in_trade_avg_position_mcm_field_strain": float(sum(position_mcm_field_strain_values) / max(1, len(position_mcm_field_strain_values))),
        "in_trade_avg_position_self_trust_gap": float(sum(position_self_trust_gap_values) / max(1, len(position_self_trust_gap_values))),
        "in_trade_avg_position_cortisol_load": float(sum(position_cortisol_load_values) / max(1, len(position_cortisol_load_values))),
        "in_trade_avg_position_noradrenaline_arousal": float(sum(position_noradrenaline_arousal_values) / max(1, len(position_noradrenaline_arousal_values))),
        "in_trade_avg_position_protective_distance": float(sum(position_protective_distance_values) / max(1, len(position_protective_distance_values))),
        "in_trade_avg_position_held_risk_discomfort": float(sum(position_held_risk_discomfort_values) / max(1, len(position_held_risk_discomfort_values))),
        "in_trade_avg_position_process_quality": float(sum(position_process_quality_values) / max(1, len(position_process_quality_values))),
        "in_trade_last_position_experience_label": str(last_payload.get("position_experience_label", "-") or "-"),
        "in_trade_avg_field_areal_count": float(sum(field_areal_count_values) / max(1, len(field_areal_count_values))),
        "in_trade_avg_field_areal_activation_mean": float(sum(field_areal_activation_values) / max(1, len(field_areal_activation_values))),
        "in_trade_avg_field_areal_stability_mean": float(sum(field_areal_stability_values) / max(1, len(field_areal_stability_values))),
        "in_trade_avg_field_areal_pressure_mean": float(sum(field_areal_pressure_values) / max(1, len(field_areal_pressure_values))),
        "in_trade_avg_field_areal_drift": float(sum(field_areal_drift_values) / max(1, len(field_areal_drift_values))),
        "in_trade_avg_field_areal_dominance": float(sum(field_areal_dominance_values) / max(1, len(field_areal_dominance_values))),
        "in_trade_avg_field_areal_fragmentation": float(sum(field_areal_fragmentation_values) / max(1, len(field_areal_fragmentation_values))),
        "in_trade_avg_field_areal_coherence_mean": float(sum(field_areal_coherence_values) / max(1, len(field_areal_coherence_values))),
        "in_trade_avg_field_areal_conflict_mean": float(sum(field_areal_conflict_values) / max(1, len(field_areal_conflict_values))),
        "in_trade_last_pre_action_phase": str(last_payload.get("pre_action_phase", "-") or "-"),
        "in_trade_last_dominant_tension_cause": str(last_payload.get("dominant_tension_cause", "-") or "-"),
        "in_trade_last_state_before": dict(last_payload.get("state_before", {}) or {}),
        "in_trade_last_state_after": dict(last_payload.get("state_after", {}) or {}),
        "in_trade_last_state_delta": dict(last_payload.get("state_delta", {}) or {}),
    }

# --------------------------------------------------
def _build_episode_review_notes_from_context(
    visible_episode=None,
    internal_episode=None,
    outcome_decomposition=None,
    in_trade_summary=None,
    event_name=None,
    timestamp=None,
):

    visible_episode = dict(visible_episode or {})
    internal_episode = dict(internal_episode or {})
    outcome_decomposition = dict(outcome_decomposition or {})
    in_trade_summary = dict(in_trade_summary or {})
    thought_state = dict(internal_episode.get("thought_state", visible_episode.get("thought_state", {})) or {})
    meta_regulation_state = dict(internal_episode.get("meta_regulation_state", visible_episode.get("meta_regulation_state", {})) or {})
    expectation_state = dict(internal_episode.get("expectation_state", visible_episode.get("expectation_state", {})) or {})
    signal = dict(internal_episode.get("signal", {}) or {})

    plan_quality = float(outcome_decomposition.get("plan_quality", 0.0) or 0.0)
    execution_quality = float(outcome_decomposition.get("execution_quality", 0.0) or 0.0)
    risk_fit_quality = float(outcome_decomposition.get("risk_fit_quality", 0.0) or 0.0)
    readiness = float(meta_regulation_state.get("readiness", 0.0) or 0.0)
    maturity = float(meta_regulation_state.get("maturity", thought_state.get("maturity", 0.0)) or 0.0)
    uncertainty = float(thought_state.get("uncertainty", 0.0) or 0.0)
    conflict = float(thought_state.get("conflict", 0.0) or 0.0)
    regulated_courage = float(meta_regulation_state.get("regulated_courage", 0.0) or 0.0)
    courage_gap = float(meta_regulation_state.get("courage_gap", 0.0) or 0.0)
    action_inhibition = float(meta_regulation_state.get("action_inhibition", 0.0) or 0.0)
    action_clearance = float(meta_regulation_state.get("action_clearance", 0.0) or 0.0)
    context_cluster_quality = float(signal.get("context_cluster_quality", 0.0) or 0.0)
    signature_quality = float(signal.get("signature_quality", 0.0) or 0.0)
    expectation_alignment = float(expectation_state.get("experience_regulation", 0.0) or 0.0)
    observation_mode = bool(signal.get("observation_mode", False))
    in_trade_update_count = int(in_trade_summary.get("in_trade_update_count", 0) or 0)
    in_trade_max_mfe = float(in_trade_summary.get("in_trade_max_mfe", 0.0) or 0.0)
    in_trade_max_mae = float(in_trade_summary.get("in_trade_max_mae", 0.0) or 0.0)
    in_trade_avg_fill_ratio = float(in_trade_summary.get("in_trade_avg_fill_ratio", 0.0) or 0.0)
    in_trade_direction_stability = float(in_trade_summary.get("in_trade_direction_stability", 0.0) or 0.0)
    in_trade_avg_regulatory_load = float(in_trade_summary.get("in_trade_avg_regulatory_load", 0.0) or 0.0)
    in_trade_avg_action_capacity = float(in_trade_summary.get("in_trade_avg_action_capacity", 0.0) or 0.0)
    in_trade_avg_recovery_need = float(in_trade_summary.get("in_trade_avg_recovery_need", 0.0) or 0.0)
    in_trade_avg_pressure_to_capacity = float(in_trade_summary.get("in_trade_avg_pressure_to_capacity", 0.0) or 0.0)
    in_trade_avg_regulated_courage = float(in_trade_summary.get("in_trade_avg_regulated_courage", 0.0) or 0.0)

    event_key = str(event_name or internal_episode.get("last_event", visible_episode.get("last_event", "-")) or "-").strip().lower()
    decision_tendency_value = str(visible_episode.get("decision_tendency", "hold") or "hold").strip().lower()

    uncertainty_recognition_quality = max(
        0.0,
        min(
            1.0,
            (1.0 - uncertainty) * 0.22
            + (1.0 - conflict) * 0.12
            + (readiness * 0.10)
            + (maturity * 0.12)
            + (context_cluster_quality * 0.10)
            + (signature_quality * 0.08)
            + (expectation_alignment * 0.08)
            + (regulated_courage * 0.08)
            + (action_clearance * 0.10),
        ),
    )

    observation_quality = max(
        0.0,
        min(
            1.0,
            (uncertainty_recognition_quality * 0.24)
            + (context_cluster_quality * 0.10)
            + (signature_quality * 0.08)
            + (expectation_alignment * 0.06)
            + (max(0.0, 1.0 - action_inhibition) * 0.08)
            + (regulated_courage * 0.08)
            + (0.12 if observation_mode else 0.0)
            + (0.08 if decision_tendency_value in ("observe", "hold") else 0.0)
            + (0.10 if event_key in ("observed_only", "withheld") else 0.0)
            + (max(0.0, 1.0 - (courage_gap / 0.08)) * 0.06),
        ),
    )

    correction_timing_quality = max(
        0.0,
        min(
            1.0,
            (plan_quality * 0.14)
            + (execution_quality * 0.10)
            + (readiness * 0.10)
            + (maturity * 0.12)
            + (context_cluster_quality * 0.08)
            + (expectation_alignment * 0.10)
            + (regulated_courage * 0.10)
            + (max(0.0, 1.0 - courage_gap) * 0.10)
            + (max(0.0, 1.0 - in_trade_avg_pressure_to_capacity) * 0.08)
            + (0.10 if event_key in ("replanned", "abandoned", "cancelled") else 0.0),
        ),
    )

    structural_bearing_quality = max(
        0.0,
        min(
            1.0,
            (plan_quality * 0.14)
            + (risk_fit_quality * 0.14)
            + (context_cluster_quality * 0.12)
            + (signature_quality * 0.10)
            + (in_trade_direction_stability * 0.08)
            + (in_trade_avg_fill_ratio * 0.06)
            + (max(0.0, 1.0 - in_trade_avg_regulatory_load) * 0.08)
            + (in_trade_avg_action_capacity * 0.10)
            + (max(0.0, 1.0 - in_trade_avg_recovery_need) * 0.08)
            + (in_trade_avg_regulated_courage * 0.10)
            + (max(0.0, in_trade_max_mfe - in_trade_max_mae) / max(1.0, abs(in_trade_max_mfe) + abs(in_trade_max_mae)) * 0.10),
        ),
    )

    bearing_regulation_cost = max(
        0.0,
        min(
            1.0,
            (in_trade_avg_regulatory_load * 0.22)
            + (in_trade_avg_recovery_need * 0.20)
            + (min(1.0, in_trade_avg_pressure_to_capacity / 2.0) * 0.18)
            + (max(0.0, 1.0 - in_trade_avg_action_capacity) * 0.14)
            + (action_inhibition * 0.14)
            + (courage_gap * 0.12),
        ),
    )

    relief_quality = max(
        0.0,
        min(
            1.0,
            (expectation_alignment * 0.12)
            + (structural_bearing_quality * 0.18)
            + (in_trade_avg_action_capacity * 0.16)
            + (max(0.0, 1.0 - in_trade_avg_regulatory_load) * 0.12)
            + (max(0.0, 1.0 - in_trade_avg_recovery_need) * 0.12)
            + (max(0.0, 1.0 - min(1.0, in_trade_avg_pressure_to_capacity / 2.0)) * 0.10)
            + (regulated_courage * 0.10)
            + (action_clearance * 0.10),
        ),
    )

    carrying_room = max(
        0.0,
        min(
            1.0,
            (plan_quality * 0.10)
            + (risk_fit_quality * 0.12)
            + (structural_bearing_quality * 0.22)
            + (readiness * 0.08)
            + (maturity * 0.08)
            + (relief_quality * 0.14)
            + (max(0.0, 1.0 - bearing_regulation_cost) * 0.14)
            + (in_trade_avg_regulated_courage * 0.12),
        ),
    )

    decision_path_quality = max(
        0.0,
        min(
            1.0,
            (plan_quality * 0.12)
            + (execution_quality * 0.10)
            + (risk_fit_quality * 0.08)
            + (observation_quality * 0.10)
            + (correction_timing_quality * 0.12)
            + (structural_bearing_quality * 0.10)
            + (expectation_alignment * 0.08)
            + (regulated_courage * 0.08)
            + (action_clearance * 0.08)
            + (max(0.0, 1.0 - courage_gap) * 0.06)
            + (relief_quality * 0.04)
            + (carrying_room * 0.04),
        ),
    )

    review_score = max(
        0.0,
        min(
            1.0,
            (decision_path_quality * 0.22)
            + (uncertainty_recognition_quality * 0.12)
            + (observation_quality * 0.12)
            + (correction_timing_quality * 0.12)
            + (structural_bearing_quality * 0.14)
            + (relief_quality * 0.10)
            + (carrying_room * 0.10)
            + (max(0.0, 1.0 - bearing_regulation_cost) * 0.08),
        ),
    )

    review_label_pressures = {
        "observe_was_correct": _clip01(
            (observation_quality * 0.34)
            + ((1.0 - bearing_regulation_cost) * 0.12)
            + (0.16 if event_key in ("observed_only", "withheld") else 0.0)
        ),
        "correction_was_correct": _clip01(
            (correction_timing_quality * 0.32)
            + (bearing_regulation_cost * 0.12)
            + (0.16 if event_key in ("replanned", "abandoned", "cancelled") else 0.0)
        ),
        "reinforce": _clip01(
            (carrying_room * 0.26)
            + (review_score * 0.24)
            + ((1.0 - bearing_regulation_cost) * 0.10)
        ),
        "deepen_reflection": _clip01(
            (bearing_regulation_cost * 0.30)
            + ((1.0 - review_score) * 0.18)
            + (uncertainty_recognition_quality * 0.08)
        ),
        "mixed": _clip01((1.0 - max(review_score, observation_quality, correction_timing_quality, carrying_room)) * 0.22),
    }
    review_label = max(review_label_pressures, key=review_label_pressures.get)

    return {
        "review_timestamp": timestamp,
        "review_label": str(review_label),
        "review_label_pressures": dict(review_label_pressures),
        "review_score": float(review_score),
        "decision_path_quality": float(decision_path_quality),
        "uncertainty_recognition_quality": float(uncertainty_recognition_quality),
        "observation_quality": float(observation_quality),
        "correction_timing_quality": float(correction_timing_quality),
        "structural_bearing_quality": float(structural_bearing_quality),
        "bearing_regulation_cost": float(bearing_regulation_cost),
        "relief_quality": float(relief_quality),
        "carrying_room": float(carrying_room),
        "action_inhibition": float(action_inhibition),
        "action_clearance": float(action_clearance),
        "in_trade_update_count": int(in_trade_update_count),
        "in_trade_max_mfe": float(in_trade_max_mfe),
        "in_trade_max_mae": float(in_trade_max_mae),
        "in_trade_avg_fill_ratio": float(in_trade_avg_fill_ratio),
        "in_trade_direction_stability": float(in_trade_direction_stability),
        "in_trade_avg_regulatory_load": float(in_trade_avg_regulatory_load),
        "in_trade_avg_action_capacity": float(in_trade_avg_action_capacity),
        "in_trade_avg_recovery_need": float(in_trade_avg_recovery_need),
        "in_trade_avg_pressure_to_capacity": float(in_trade_avg_pressure_to_capacity),
        "in_trade_avg_regulated_courage": float(in_trade_avg_regulated_courage),
    }
