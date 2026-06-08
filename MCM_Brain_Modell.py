# ==================================================
# MCM_Brain_Modell.py
# Brain + MCM Bridge
# ==================================================
import time

from config import Config
from debug_tools.writers import dbr_append_text, dbr_debug, dbr_path, dbr_profile
from bot_engine.mcm_core_engine import build_tension_state_from_window
from core.visual_perception import build_visual_market_state
from core.active_context import (
    _apply_nervous_context_modulation as _apply_nervous_context_modulation_impl,
    _build_active_context_trace_from_inner_cluster as _build_active_context_trace_from_inner_cluster_impl,
    _build_active_context_trace_from_temporal_state as _build_active_context_trace_from_temporal_state_impl,
    _decay_active_context_trace as _decay_active_context_trace_impl,
    _refresh_active_context_trace as _refresh_active_context_trace_impl,
    _resolve_active_context_replay_impulse as _resolve_active_context_replay_impulse_impl,
    _resolve_context_modulation_source as _resolve_context_modulation_source_impl,
)
from core.brain_factory import create_mcm_brain as _create_mcm_brain_impl
from core.inner_pattern import (
    _build_inner_pattern_identity as _build_inner_pattern_identity_impl,
    _build_inner_pattern_identity_stability as _build_inner_pattern_identity_stability_impl,
    _build_inner_pattern_recognition_state as _build_inner_pattern_recognition_state_impl,
    _derive_inner_pattern_label as _derive_inner_pattern_label_impl,
)
from core.inner_context import (
    _build_inner_context_cluster_state as _build_inner_context_cluster_state_impl,
    _update_inner_context_cluster_memory as _update_inner_context_cluster_memory_impl,
)
from core.experience_space import (
    _append_experience_episode as _append_experience_episode_impl,
    _build_affective_structure_profile as _build_affective_structure_profile_impl,
    _build_episode_felt_summary as _build_episode_felt_summary_impl,
    _complete_experience_episode_summary as _complete_experience_episode_summary_impl,
    _build_episode_review_notes_from_context as _build_episode_review_notes_from_context_impl,
    _build_experience_similarity_axes as _build_experience_similarity_axes_impl,
    _compact_in_trade_update_payload,
    _derive_felt_label as _derive_felt_label_impl,
    _experience_bearing_delta as _experience_bearing_delta_impl,
    _experience_reward_delta as _experience_reward_delta_impl,
    _update_experience_link_bucket as _update_experience_link_bucket_impl,
    _summarize_in_trade_updates,
    _update_field_decision_outcome_protocol as _update_field_decision_outcome_protocol_impl,
    build_experience_neurochemical_effect as build_experience_neurochemical_effect_impl,
)
from core.form_language import _extract_outcome_form_symbol_state as _extract_outcome_form_symbol_state_impl, _quantize_form_axis as _quantize_form_axis_impl
from core.felt_state import resolve_felt_state
from core.form_symbol_orchestration import (
    build_form_symbol_state as _build_form_symbol_state_impl,
    update_form_symbol_development_from_outcome as _update_form_symbol_development_from_outcome_impl,
)
from core.mcm_field import MCMField, ClusterDetector, Memory, SelfModel, AttractorSystem, RegulationLayer
from core.runtime import MCMBrainRuntime as _MCMBrainRuntimeImpl
from core.runtime_bridge import create_mcm_runtime as _create_mcm_runtime_impl, step_mcm_runtime as _step_mcm_runtime_impl, step_mcm_runtime_idle as _step_mcm_runtime_idle_impl
from core.runtime_entry import (
    build_runtime_entry_trade_result,
    build_runtime_field_metrics,
    build_runtime_entry_state_stack,
    build_runtime_no_plan_result,
    build_virtual_observation_plan,
    record_runtime_entry_rejection_protocol,
    record_runtime_entry_result_protocol,
    synchronize_entry_choice_result,
    synchronize_entry_choice_prices,
)
from core.review_feedback import resolve_review_decision_feedback
from core.runtime_field_state import _derive_runtime_field_state
from core.strategic_window import build_strategic_window_state
from debug_tools.field_snapshots import (
    _build_field_topology_state as _build_field_topology_state_impl,
    _build_neural_felt_state as _build_neural_felt_state_impl,
    _snapshot_agent_field_points as _snapshot_agent_field_points_impl,
    _snapshot_areal_population as _snapshot_areal_population_impl,
    _snapshot_cluster_centers as _snapshot_cluster_centers_impl,
    _snapshot_cluster_links as _snapshot_cluster_links_impl,
    _snapshot_field_perception_state as _snapshot_field_perception_state_impl,
    _snapshot_field_topology_layout as _snapshot_field_topology_layout_impl,
    _snapshot_float_vector as _snapshot_float_vector_impl,
    _snapshot_neuron_population as _snapshot_neuron_population_impl,
)
from bot_engine.strukture_engine import StructureEngine
import numpy as np

STRUCTURE_ENGINE = StructureEngine()

# --------------------------------------------------
class MCMBrainRuntime(_MCMBrainRuntimeImpl):
    def __init__(self, bot=None):
        super().__init__(
            bot=bot,
            normalize_active_context_trace=_normalize_active_context_trace,
            decay_active_context_trace=_decay_active_context_trace,
            compute_runtime_result=_compute_runtime_result,
            apply_runtime_result=_apply_runtime_result,
            record_neuro_transition_protocol=_record_neuro_transition_protocol,
        )

# --------------------------------------------------
def _resolve_active_context_replay_impulse(trace):
    return _resolve_active_context_replay_impulse_impl(trace)

# --------------------------------------------------
from core.mcm_field import _extract_neurochemical_profile, _normalize_active_context_trace

def _resolve_context_modulation_source(bot=None, runtime_result=None):
    return _resolve_context_modulation_source_impl(bot=bot, runtime_result=runtime_result)

# --------------------------------------------------
def _apply_nervous_context_modulation(trace, bot=None, runtime_result=None):
    return _apply_nervous_context_modulation_impl(trace, bot=bot, runtime_result=runtime_result)

# --------------------------------------------------
def _snapshot_field_topology_layout(field, limit=96, field_snapshot=None):
    return _snapshot_field_topology_layout_impl(field, limit=limit, field_snapshot=field_snapshot)

# --------------------------------------------------
def _decay_active_context_trace(trace, market_tick_advanced=True):
    return _decay_active_context_trace_impl(trace, market_tick_advanced=market_tick_advanced)

# --------------------------------------------------
def _build_active_context_trace_from_inner_cluster(bot=None):
    return _build_active_context_trace_from_inner_cluster_impl(bot=bot)

# --------------------------------------------------
def _build_active_context_trace_from_temporal_state(bot=None, runtime_result=None):
    return _build_active_context_trace_from_temporal_state_impl(bot=bot, runtime_result=runtime_result)

# --------------------------------------------------
def _refresh_active_context_trace(trace, bot=None, runtime_result=None, market_tick_advanced=True):
    return _refresh_active_context_trace_impl(trace, bot=bot, runtime_result=runtime_result, market_tick_advanced=market_tick_advanced)

# --------------------------------------------------
def step_mcm_runtime_idle(bot=None, cycles=1):
    return _step_mcm_runtime_idle_impl(bot=bot, cycles=cycles)

# --------------------------------------------------
def create_mcm_runtime(bot=None):
    return _create_mcm_runtime_impl(bot=bot, runtime_cls=MCMBrainRuntime)

# --------------------------------------------------
# RUNTIME HELPERS
# --------------------------------------------------

# --------------------------------------------------
def _build_inner_pattern_recognition_state(identity_state):
    return _build_inner_pattern_recognition_state_impl(identity_state)

# --------------------------------------------------
def _build_inner_pattern_identity_stability(bot, identity_state):
    return _build_inner_pattern_identity_stability_impl(bot, identity_state)

# --------------------------------------------------
def _build_inner_pattern_identity(inner_field_state, summary_item, state_payload=None):
    return _build_inner_pattern_identity_impl(inner_field_state, summary_item, state_payload=state_payload)

# --------------------------------------------------
def _build_runtime_hold_decision(bot, candle_state=None, tension_state=None, decision_tendency="hold", reason="runtime_hold"):

    candle = dict(candle_state or {})
    tension = dict(tension_state or {})
    snapshot = dict(getattr(bot, "mcm_snapshot", {}) or {}) if bot is not None else {}
    expectation_state = dict(getattr(bot, "expectation_state", {}) or {}) if bot is not None else {}
    visual_market_state = dict(getattr(bot, "visual_market_state", {}) or {}) if bot is not None else {}
    structure_perception_state = dict(getattr(bot, "structure_perception_state", {}) or {}) if bot is not None else {}
    temporal_perception_state = dict(getattr(bot, "temporal_perception_state", {}) or {}) if bot is not None else {}
    outer_visual_perception_state = dict(getattr(bot, "outer_visual_perception_state", {}) or {}) if bot is not None else {}
    inner_field_perception_state = dict(getattr(bot, "inner_field_perception_state", {}) or {}) if bot is not None else {}
    processing_state = dict(getattr(bot, "processing_state", {}) or {}) if bot is not None else {}
    perception_state = dict(getattr(bot, "perception_state", {}) or {}) if bot is not None else {}
    felt_state = dict(getattr(bot, "felt_state", {}) or {}) if bot is not None else {}
    thought_state = dict(getattr(bot, "thought_state", {}) or {}) if bot is not None else {}
    meta_regulation_state = dict(getattr(bot, "meta_regulation_state", {}) or {}) if bot is not None else {}
    form_symbol_state = dict(getattr(bot, "form_symbol_state", {}) or {}) if bot is not None else {}
    state_signature = dict(getattr(bot, "last_signature_context", {}) or {}) if bot is not None else {}
    market_hearing_state = dict(tension.get("market_hearing_state", {}) or {})
    market_loudness = float(market_hearing_state.get("loudness", tension.get("market_loudness", tension.get("energy_amplitude_stimulus", 0.0))) or 0.0)
    market_frequency_hz = float(market_hearing_state.get("frequency_hz", tension.get("market_frequency_hz", 0.0)) or 0.0)
    market_hearing_compression = float(market_hearing_state.get("compression", tension.get("market_hearing_compression", 0.0)) or 0.0)
    market_tone = str(market_hearing_state.get("tone", tension.get("market_tone", "silent_tone")) or "silent_tone")

    strongest_memory = dict(snapshot.get("strongest_memory", {}) or {})
    proposed_decision = str(meta_regulation_state.get("decision", "WAIT") or "WAIT").upper().strip()
    field_state = _derive_runtime_field_state(
        bot=bot,
        tension_state=tension,
        snapshot=snapshot,
    )

    return {
        "decision": "WAIT",
        "entry_price": 0.0,
        "sl_price": 0.0,
        "tp_price": 0.0,
        "rr_value": 0.0,
        "entry_validity_band": {},
        "target_conviction": 0.0,
        "risk_model_score": 0.0,
        "reward_model_score": 0.0,
        "energy": float(tension.get("energy", 0.0) or 0.0),
        "market_hearing_state": dict(market_hearing_state or {}),
        "market_loudness": float(market_loudness),
        "market_frequency_hz": float(market_frequency_hz),
        "market_hearing_compression": float(market_hearing_compression),
        "market_tone": str(market_tone),
        "coherence": float(tension.get("coherence", 0.0) or 0.0),
        "asymmetry": int(tension.get("asymmetry", 0) or 0),
        "coh_zone": float(tension.get("coh_zone", 0.0) or 0.0),
        "self_state": str(snapshot.get("self_state", getattr(bot, "mcm_last_action", "stable") if bot is not None else "stable") or "stable"),
        "attractor": str(snapshot.get("attractor", getattr(bot, "mcm_last_attractor", "neutral") if bot is not None else "neutral") or "neutral"),
        "memory_center": float(strongest_memory.get("center", 0.0) or 0.0),
        "memory_strength": int(strongest_memory.get("strength", 0) or 0),
        "vision": {},
        "filtered_vision": {},
        "focus": {
            "focus_direction": float(getattr(bot, "focus_point", 0.0) or 0.0) if bot is not None else 0.0,
            "focus_strength": 0.0,
            "focus_confidence": float(getattr(bot, "focus_confidence", 0.0) or 0.0) if bot is not None else 0.0,
            "target_lock": float(getattr(bot, "target_lock", 0.0) or 0.0) if bot is not None else 0.0,
            "noise_damp": 0.0,
            "signal_relevance": float(getattr(bot, "last_signal_relevance", 0.0) or 0.0) if bot is not None else 0.0,
        },
        "world_state": {
            "candle_state": dict(candle or {}),
            "tension_state": dict(tension or {}),
            "visual_market_state": dict(visual_market_state or {}),
            "structure_perception_state": dict(structure_perception_state or {}),
            "temporal_perception_state": dict(temporal_perception_state or {}),
        },
        "structure_perception_state": dict(structure_perception_state or {}),
        "temporal_perception_state": dict(temporal_perception_state or {}),
        "outer_visual_perception_state": dict(outer_visual_perception_state or {}),
        "inner_field_perception_state": dict(inner_field_perception_state or {}),
        "processing_state": dict(processing_state or {}),
        "perception_state": dict(perception_state or {}),
        "felt_state": dict(felt_state or {}),
        "thought_state": dict(thought_state or {}),
        "meta_regulation_state": dict(meta_regulation_state or {}),
        "expectation_state": dict(expectation_state or {}),
        "form_symbol_state": dict(form_symbol_state or {}),
        "state_signature": dict(state_signature or {}),
        "signature_bias": 0.0,
        "signature_block": False,
        "signature_caution_modulation": False,
        "signature_quality": 0.0,
        "signature_distance": 0.0,
        "context_cluster_id": "-",
        "context_cluster_bias": 0.0,
        "context_cluster_quality": 0.0,
        "context_cluster_distance": 0.0,
        "context_cluster_block": False,
        "context_cluster_caution_modulation": False,
        "inhibition_level": float(getattr(bot, "inhibition_level", 0.0) or 0.0) if bot is not None else 0.0,
        "habituation_level": float(getattr(bot, "habituation_level", 0.0) or 0.0) if bot is not None else 0.0,
        "competition_bias": float(getattr(bot, "competition_bias", 0.0) or 0.0) if bot is not None else 0.0,
        "observation_mode": bool(getattr(bot, "observation_mode", False)) if bot is not None else False,
        "long_score": 0.0,
        "short_score": 0.0,
        "field_stimulus_density": float(field_state.get("field_stimulus_density", 0.0) or 0.0),
        "field_density": float(field_state.get("field_density", 0.0) or 0.0),
        "field_stability": float(field_state.get("field_stability", 0.0) or 0.0),
        "regulatory_load": float(field_state.get("regulatory_load", 0.0) or 0.0),
        "action_capacity": float(field_state.get("action_capacity", 0.0) or 0.0),
        "recovery_need": float(field_state.get("recovery_need", 0.0) or 0.0),
        "survival_pressure": float(field_state.get("survival_pressure", 0.0) or 0.0),
        "decision_tendency": str(decision_tendency or "hold"),
        "proposed_decision": str(proposed_decision or "WAIT"),
        "rejection_reason": str(reason or "runtime_hold"),
    }

# --------------------------------------------------
def step_mcm_runtime(window, candle_state, bot=None, tension_state=None, visual_market_state=None, structure_perception_state=None, temporal_perception_state=None):
    return _step_mcm_runtime_impl(
        window,
        candle_state,
        bot=bot,
        tension_state=tension_state,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        temporal_perception_state=temporal_perception_state,
        compute_runtime_result=_compute_runtime_result,
        apply_runtime_result=_apply_runtime_result,
    )

# --------------------------------------------------
def _experience_bearing_delta(summary):
    return _experience_bearing_delta_impl(summary)

# --------------------------------------------------
def build_experience_neurochemical_effect(summary):
    return build_experience_neurochemical_effect_impl(summary)

# --------------------------------------------------
def _experience_reward_delta(summary):
    return _experience_reward_delta_impl(summary)

# --------------------------------------------------
def _build_experience_similarity_axes(summary):
    return _build_experience_similarity_axes_impl(summary)

# --------------------------------------------------
def _derive_inner_pattern_label(inner_field_state, summary_item):
    return _derive_inner_pattern_label_impl(inner_field_state, summary_item)

# --------------------------------------------------
def _build_inner_context_cluster_state(inner_field_state, summary_item, bot=None):
    return _build_inner_context_cluster_state_impl(inner_field_state, summary_item, bot=bot)

# --------------------------------------------------
def _update_inner_context_cluster_memory(bot, summary):
    return _update_inner_context_cluster_memory_impl(bot, summary, reward_delta_builder=_experience_reward_delta)

# --------------------------------------------------
def _refresh_experience_space(bot, timestamp=None, decision_tendency=None, event_name=None):

    if bot is None:
        return None

    experience_space = dict(getattr(bot, "mcm_experience_space", {}) or {})
    summary = _build_experience_episode_summary(
        bot,
        timestamp=timestamp,
        decision_tendency=decision_tendency,
        event_name=event_name,
    )

    inner_context_result = _update_inner_context_cluster_memory(
        bot,
        summary,
    )

    if isinstance(inner_context_result, dict):
        summary["inner_context_cluster_id"] = str(inner_context_result.get("cluster_id", "-") or "-")
        summary["inner_context_cluster_distance"] = float(inner_context_result.get("distance", 0.0) or 0.0)
        summary["inner_context_cluster_score"] = float(inner_context_result.get("score", 0.0) or 0.0)
        summary["inner_context_cluster_trust"] = float(inner_context_result.get("trust", 0.0) or 0.0)
        summary["inner_context_cluster_mass_mean"] = float(inner_context_result.get("field_cluster_mass_mean", 0.0) or 0.0)
        summary["inner_context_cluster_mass_max"] = float(inner_context_result.get("field_cluster_mass_max", 0.0) or 0.0)
        summary["inner_context_cluster_center_spread"] = float(inner_context_result.get("field_cluster_center_spread", 0.0) or 0.0)
        summary["inner_context_cluster_separation"] = float(inner_context_result.get("field_cluster_separation", 0.0) or 0.0)
        summary["inner_context_cluster_center_drift"] = float(inner_context_result.get("field_cluster_center_drift", 0.0) or 0.0)
        summary["inner_context_cluster_count_drift"] = float(inner_context_result.get("field_cluster_count_drift", 0.0) or 0.0)
        summary["inner_context_cluster_velocity_trend"] = float(inner_context_result.get("field_velocity_trend", 0.0) or 0.0)
        summary["inner_context_cluster_reorganization_direction"] = str(inner_context_result.get("field_reorganization_direction", "stable") or "stable")
        summary["inner_context_cluster_mean_velocity"] = float(inner_context_result.get("field_mean_velocity", 0.0) or 0.0)
        summary["inner_context_cluster_regulation_pressure"] = float(inner_context_result.get("field_regulation_pressure", 0.0) or 0.0)
        summary["inner_context_cluster_neuron_count"] = int(inner_context_result.get("field_neuron_count", 0) or 0)
        summary["inner_context_cluster_neuron_activation_mean"] = float(inner_context_result.get("field_neuron_activation_mean", 0.0) or 0.0)
        summary["inner_context_cluster_neuron_activation_max"] = float(inner_context_result.get("field_neuron_activation_max", 0.0) or 0.0)
        summary["inner_context_cluster_neuron_stability_mean"] = float(inner_context_result.get("field_neuron_stability_mean", 0.0) or 0.0)
        summary["inner_context_cluster_neuron_regulation_pressure_mean"] = float(inner_context_result.get("field_neuron_regulation_pressure_mean", 0.0) or 0.0)
        summary["inner_context_cluster_neuron_memory_norm_mean"] = float(inner_context_result.get("field_neuron_memory_norm_mean", 0.0) or 0.0)
        summary["inner_context_cluster_neuron_coupling_norm_mean"] = float(inner_context_result.get("field_neuron_coupling_norm_mean", 0.0) or 0.0)
        summary["inner_context_cluster_neuron_regulation_force_norm_mean"] = float(inner_context_result.get("field_neuron_regulation_force_norm_mean", 0.0) or 0.0)
        summary["inner_context_cluster_neuron_external_impulse_norm_mean"] = float(inner_context_result.get("field_neuron_external_impulse_norm_mean", 0.0) or 0.0)
        summary["inner_context_cluster_neuron_context_memory_impulse_norm_mean"] = float(inner_context_result.get("field_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0)
        summary["inner_context_cluster_areal_count"] = int(inner_context_result.get("field_areal_count", 0) or 0)
        summary["inner_context_cluster_areal_activation_mean"] = float(inner_context_result.get("field_areal_activation_mean", 0.0) or 0.0)
        summary["inner_context_cluster_areal_stability_mean"] = float(inner_context_result.get("field_areal_stability_mean", 0.0) or 0.0)
        summary["inner_context_cluster_areal_pressure_mean"] = float(inner_context_result.get("field_areal_pressure_mean", 0.0) or 0.0)
        summary["inner_context_cluster_areal_drift"] = float(inner_context_result.get("field_areal_drift", 0.0) or 0.0)
        summary["inner_context_cluster_areal_dominance"] = float(inner_context_result.get("field_areal_dominance", 0.0) or 0.0)
        summary["inner_context_cluster_areal_fragmentation"] = float(inner_context_result.get("field_areal_fragmentation", 0.0) or 0.0)
        summary["inner_context_cluster_areal_coherence_mean"] = float(inner_context_result.get("field_areal_coherence_mean", 0.0) or 0.0)
        summary["inner_context_cluster_areal_conflict_mean"] = float(inner_context_result.get("field_areal_conflict_mean", 0.0) or 0.0)
        summary["inner_context_cluster_areal_topology_density_mean"] = float(inner_context_result.get("field_areal_topology_density_mean", 0.0) or 0.0)
        summary["inner_context_cluster_areal_topology_span_mean"] = float(inner_context_result.get("field_areal_topology_span_mean", 0.0) or 0.0)
        summary["inner_context_cluster_areal_topology_boundary_mean"] = float(inner_context_result.get("field_areal_topology_boundary_mean", 0.0) or 0.0)
        summary["inner_context_cluster_topology_rows"] = int(inner_context_result.get("field_topology_rows", 0) or 0)
        summary["inner_context_cluster_topology_cols"] = int(inner_context_result.get("field_topology_cols", 0) or 0)
        summary["inner_context_cluster_topology_position_count"] = int(inner_context_result.get("field_topology_position_count", 0) or 0)
        summary["inner_context_cluster_topology_neighbor_link_count"] = int(inner_context_result.get("field_topology_neighbor_link_count", 0) or 0)
        summary["inner_context_cluster_topology_neighbor_count_mean"] = float(inner_context_result.get("field_topology_neighbor_count_mean", 0.0) or 0.0)
        summary["inner_context_cluster_topology_neighbor_count_max"] = int(inner_context_result.get("field_topology_neighbor_count_max", 0) or 0)
        summary["inner_context_cluster_topology_cluster_link_count"] = int(inner_context_result.get("field_topology_cluster_link_count", 0) or 0)
        summary["inner_context_cluster_topology_areal_link_count"] = int(inner_context_result.get("field_topology_areal_link_count", 0) or 0)
        summary["inner_context_cluster_topology_link_density"] = float(inner_context_result.get("field_topology_link_density", 0.0) or 0.0)
        summary["inner_context_cluster_topology_distance_mean"] = float(inner_context_result.get("field_topology_distance_mean", 0.0) or 0.0)
        summary["inner_context_cluster_topology_coherence"] = float(inner_context_result.get("field_topology_coherence", 0.0) or 0.0)
        summary["inner_context_cluster_topology_tension"] = float(inner_context_result.get("field_topology_tension", 0.0) or 0.0)
        summary["inner_context_cluster_topology_state_label"] = str(inner_context_result.get("field_topology_state_label", "sparse_topology") or "sparse_topology")
        summary["inner_context_cluster_field_perception_state"] = dict(inner_context_result.get("field_perception_state", {}) or {})
        summary["inner_context_cluster_activity_island_count"] = int(inner_context_result.get("field_activity_island_count", 0) or 0)
        summary["inner_context_cluster_activity_island_mass_mean"] = float(inner_context_result.get("field_activity_island_mass_mean", 0.0) or 0.0)
        summary["inner_context_cluster_activity_island_mass_max"] = float(inner_context_result.get("field_activity_island_mass_max", 0.0) or 0.0)
        summary["inner_context_cluster_activity_island_activation_mean"] = float(inner_context_result.get("field_activity_island_activation_mean", 0.0) or 0.0)
        summary["inner_context_cluster_activity_island_pressure_mean"] = float(inner_context_result.get("field_activity_island_pressure_mean", 0.0) or 0.0)
        summary["inner_context_cluster_activity_island_coherence_mean"] = float(inner_context_result.get("field_activity_island_coherence_mean", 0.0) or 0.0)
        summary["inner_context_cluster_activity_island_context_reactivation_mean"] = float(inner_context_result.get("field_activity_island_context_reactivation_mean", 0.0) or 0.0)
        summary["inner_context_cluster_activity_island_spread"] = float(inner_context_result.get("field_activity_island_spread", 0.0) or 0.0)
        summary["inner_context_cluster_field_perception_label"] = str(inner_context_result.get("field_perception_label", "quiet_field") or "quiet_field")
        summary["inner_context_cluster_neural_felt_bearing"] = float(inner_context_result.get("neural_felt_bearing", 0.0) or 0.0)
        summary["inner_context_cluster_neural_felt_pressure"] = float(inner_context_result.get("neural_felt_pressure", 0.0) or 0.0)
        summary["inner_context_cluster_neural_felt_memory_resonance"] = float(inner_context_result.get("neural_felt_memory_resonance", 0.0) or 0.0)
        summary["inner_context_cluster_neural_felt_context_reactivation"] = float(inner_context_result.get("neural_felt_context_reactivation", 0.0) or 0.0)
        summary["inner_context_cluster_neural_felt_label"] = str(inner_context_result.get("neural_felt_label", "quiet_neural_felt") or "quiet_neural_felt")
        summary["inner_context_cluster_history_length"] = int(inner_context_result.get("inner_field_history_length", 0) or 0)
        summary["inner_context_cluster_pressure_trend"] = float(inner_context_result.get("inner_field_pressure_trend", 0.0) or 0.0)
        summary["inner_context_cluster_bearing_trend"] = float(inner_context_result.get("inner_field_bearing_trend", 0.0) or 0.0)
        summary["inner_context_cluster_topology_tension_trend"] = float(inner_context_result.get("inner_field_topology_tension_trend", 0.0) or 0.0)
        summary["inner_context_cluster_memory_resonance_trend"] = float(inner_context_result.get("inner_field_memory_resonance_trend", 0.0) or 0.0)
        summary["inner_context_cluster_history_label"] = str(inner_context_result.get("inner_field_history_label", "stable_field_trace") or "stable_field_trace")
        summary["inner_context_cluster_pattern_label"] = str(inner_context_result.get("inner_pattern_label", "") or "")
        summary["inner_context_cluster_pattern_support"] = float(inner_context_result.get("inner_pattern_support", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_conflict"] = float(inner_context_result.get("inner_pattern_conflict", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_fragility"] = float(inner_context_result.get("inner_pattern_fragility", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_bearing"] = float(inner_context_result.get("inner_pattern_bearing", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_state"] = str(inner_context_result.get("inner_pattern_state", "bearing") or "bearing")
        summary["inner_context_cluster_field_pattern_signature"] = dict(inner_context_result.get("field_pattern_signature", {}) or {})
        summary["inner_context_cluster_field_pattern_signature_key"] = str(inner_context_result.get("field_pattern_signature_key", "") or "")
        summary["inner_context_cluster_field_pattern_vector"] = [float(value) for value in list(inner_context_result.get("field_pattern_vector", []) or [])]
        summary["inner_context_cluster_pattern_identity"] = str(inner_context_result.get("inner_pattern_identity", "") or "")
        summary["inner_context_cluster_pattern_identity_label"] = str(inner_context_result.get("inner_pattern_identity_label", "") or "")
        summary["inner_context_cluster_pattern_identity_confidence"] = float(inner_context_result.get("inner_pattern_identity_confidence", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_identity_streak"] = int(inner_context_result.get("inner_pattern_identity_streak", 0) or 0)
        summary["inner_context_cluster_pattern_identity_stability"] = float(inner_context_result.get("inner_pattern_identity_stability", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_identity_recurrent"] = bool(inner_context_result.get("inner_pattern_identity_recurrent", False))
        summary["inner_context_cluster_pattern_identity_changed"] = bool(inner_context_result.get("inner_pattern_identity_changed", False))
        summary["inner_context_cluster_pattern_identity_last_seen_tick"] = int(inner_context_result.get("inner_pattern_identity_last_seen_tick", 0) or 0)
        summary["inner_context_cluster_pattern_recognition_state"] = dict(inner_context_result.get("inner_pattern_recognition_state", {}) or {})
        summary["inner_context_cluster_pattern_recognition_label"] = str(inner_context_result.get("inner_pattern_recognition_label", "unsettled_inner_pattern") or "unsettled_inner_pattern")
        summary["inner_context_cluster_pattern_recognition_strength"] = float(inner_context_result.get("inner_pattern_recognition_strength", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_recognition_recurrent"] = bool(inner_context_result.get("inner_pattern_recognition_recurrent", False))
        summary["inner_context_cluster_pattern_recognition_changed"] = bool(inner_context_result.get("inner_pattern_recognition_changed", False))
        summary["inner_context_cluster_pattern_support_score"] = float(inner_context_result.get("pattern_support_score", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_conflict_score"] = float(inner_context_result.get("pattern_conflict_score", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_fragility_score"] = float(inner_context_result.get("pattern_fragility_score", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_bearing_score"] = float(inner_context_result.get("pattern_bearing_score", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_reinforcement"] = float(inner_context_result.get("pattern_reinforcement", 0.0) or 0.0)
        summary["inner_context_cluster_pattern_attenuation"] = float(inner_context_result.get("pattern_attenuation", 0.0) or 0.0)
        summary["inner_context_cluster_self_state"] = str(inner_context_result.get("inner_self_state", "stable") or "stable")
        summary["inner_context_cluster_attractor"] = str(inner_context_result.get("inner_attractor", "neutral") or "neutral")

        experience_space["last_inner_context_cluster_id"] = str(inner_context_result.get("cluster_id", "-") or "-")
        experience_space["last_inner_context_cluster_key"] = str(getattr(bot, "last_inner_context_cluster_key", None) or "")
        experience_space["last_inner_context_cluster_distance"] = float(inner_context_result.get("distance", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_score"] = float(inner_context_result.get("score", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_trust"] = float(inner_context_result.get("trust", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_mass_mean"] = float(inner_context_result.get("field_cluster_mass_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_mass_max"] = float(inner_context_result.get("field_cluster_mass_max", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_center_spread"] = float(inner_context_result.get("field_cluster_center_spread", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_separation"] = float(inner_context_result.get("field_cluster_separation", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_center_drift"] = float(inner_context_result.get("field_cluster_center_drift", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_count_drift"] = float(inner_context_result.get("field_cluster_count_drift", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_velocity_trend"] = float(inner_context_result.get("field_velocity_trend", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_reorganization_direction"] = str(inner_context_result.get("field_reorganization_direction", "stable") or "stable")
        experience_space["last_inner_context_cluster_mean_velocity"] = float(inner_context_result.get("field_mean_velocity", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_regulation_pressure"] = float(inner_context_result.get("field_regulation_pressure", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neuron_count"] = int(inner_context_result.get("field_neuron_count", 0) or 0)
        experience_space["last_inner_context_cluster_neuron_activation_mean"] = float(inner_context_result.get("field_neuron_activation_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neuron_activation_max"] = float(inner_context_result.get("field_neuron_activation_max", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neuron_stability_mean"] = float(inner_context_result.get("field_neuron_stability_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neuron_regulation_pressure_mean"] = float(inner_context_result.get("field_neuron_regulation_pressure_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neuron_memory_norm_mean"] = float(inner_context_result.get("field_neuron_memory_norm_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neuron_coupling_norm_mean"] = float(inner_context_result.get("field_neuron_coupling_norm_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neuron_regulation_force_norm_mean"] = float(inner_context_result.get("field_neuron_regulation_force_norm_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neuron_external_impulse_norm_mean"] = float(inner_context_result.get("field_neuron_external_impulse_norm_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neuron_context_memory_impulse_norm_mean"] = float(inner_context_result.get("field_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_count"] = int(inner_context_result.get("field_areal_count", 0) or 0)
        experience_space["last_inner_context_cluster_areal_activation_mean"] = float(inner_context_result.get("field_areal_activation_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_stability_mean"] = float(inner_context_result.get("field_areal_stability_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_pressure_mean"] = float(inner_context_result.get("field_areal_pressure_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_drift"] = float(inner_context_result.get("field_areal_drift", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_dominance"] = float(inner_context_result.get("field_areal_dominance", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_fragmentation"] = float(inner_context_result.get("field_areal_fragmentation", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_coherence_mean"] = float(inner_context_result.get("field_areal_coherence_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_conflict_mean"] = float(inner_context_result.get("field_areal_conflict_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_topology_density_mean"] = float(inner_context_result.get("field_areal_topology_density_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_topology_span_mean"] = float(inner_context_result.get("field_areal_topology_span_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_areal_topology_boundary_mean"] = float(inner_context_result.get("field_areal_topology_boundary_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_topology_cluster_link_count"] = int(inner_context_result.get("field_topology_cluster_link_count", 0) or 0)
        experience_space["last_inner_context_cluster_topology_areal_link_count"] = int(inner_context_result.get("field_topology_areal_link_count", 0) or 0)
        experience_space["last_inner_context_cluster_topology_link_density"] = float(inner_context_result.get("field_topology_link_density", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_topology_distance_mean"] = float(inner_context_result.get("field_topology_distance_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_topology_coherence"] = float(inner_context_result.get("field_topology_coherence", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_topology_tension"] = float(inner_context_result.get("field_topology_tension", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_topology_state_label"] = str(inner_context_result.get("field_topology_state_label", "sparse_topology") or "sparse_topology")
        experience_space["last_inner_context_cluster_field_perception_state"] = dict(inner_context_result.get("field_perception_state", {}) or {})
        experience_space["last_inner_context_cluster_activity_island_count"] = int(inner_context_result.get("field_activity_island_count", 0) or 0)
        experience_space["last_inner_context_cluster_activity_island_mass_mean"] = float(inner_context_result.get("field_activity_island_mass_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_activity_island_mass_max"] = float(inner_context_result.get("field_activity_island_mass_max", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_activity_island_activation_mean"] = float(inner_context_result.get("field_activity_island_activation_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_activity_island_pressure_mean"] = float(inner_context_result.get("field_activity_island_pressure_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_activity_island_coherence_mean"] = float(inner_context_result.get("field_activity_island_coherence_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_activity_island_context_reactivation_mean"] = float(inner_context_result.get("field_activity_island_context_reactivation_mean", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_activity_island_spread"] = float(inner_context_result.get("field_activity_island_spread", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_field_perception_label"] = str(inner_context_result.get("field_perception_label", "quiet_field") or "quiet_field")
        experience_space["last_inner_context_cluster_neural_felt_bearing"] = float(inner_context_result.get("neural_felt_bearing", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neural_felt_pressure"] = float(inner_context_result.get("neural_felt_pressure", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neural_felt_memory_resonance"] = float(inner_context_result.get("neural_felt_memory_resonance", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neural_felt_context_reactivation"] = float(inner_context_result.get("neural_felt_context_reactivation", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_neural_felt_label"] = str(inner_context_result.get("neural_felt_label", "quiet_neural_felt") or "quiet_neural_felt")
        experience_space["last_inner_context_cluster_pattern_label"] = str(inner_context_result.get("inner_pattern_label", "") or "")
        experience_space["last_inner_context_cluster_pattern_support"] = float(inner_context_result.get("inner_pattern_support", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_conflict"] = float(inner_context_result.get("inner_pattern_conflict", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_fragility"] = float(inner_context_result.get("inner_pattern_fragility", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_bearing"] = float(inner_context_result.get("inner_pattern_bearing", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_state"] = str(inner_context_result.get("inner_pattern_state", "bearing") or "bearing")
        experience_space["last_inner_context_cluster_field_pattern_signature"] = dict(inner_context_result.get("field_pattern_signature", {}) or {})
        experience_space["last_inner_context_cluster_field_pattern_signature_key"] = str(inner_context_result.get("field_pattern_signature_key", "") or "")
        experience_space["last_inner_context_cluster_field_pattern_vector"] = [float(value) for value in list(inner_context_result.get("field_pattern_vector", []) or [])]
        experience_space["last_inner_context_cluster_pattern_identity"] = str(inner_context_result.get("inner_pattern_identity", "") or "")
        experience_space["last_inner_context_cluster_pattern_identity_label"] = str(inner_context_result.get("inner_pattern_identity_label", "") or "")
        experience_space["last_inner_context_cluster_pattern_identity_confidence"] = float(inner_context_result.get("inner_pattern_identity_confidence", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_identity_streak"] = int(inner_context_result.get("inner_pattern_identity_streak", 0) or 0)
        experience_space["last_inner_context_cluster_pattern_identity_stability"] = float(inner_context_result.get("inner_pattern_identity_stability", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_identity_recurrent"] = bool(inner_context_result.get("inner_pattern_identity_recurrent", False))
        experience_space["last_inner_context_cluster_pattern_identity_changed"] = bool(inner_context_result.get("inner_pattern_identity_changed", False))
        experience_space["last_inner_context_cluster_pattern_identity_last_seen_tick"] = int(inner_context_result.get("inner_pattern_identity_last_seen_tick", 0) or 0)
        experience_space["last_inner_context_cluster_pattern_recognition_state"] = dict(inner_context_result.get("inner_pattern_recognition_state", {}) or {})
        experience_space["last_inner_context_cluster_pattern_recognition_label"] = str(inner_context_result.get("inner_pattern_recognition_label", "unsettled_inner_pattern") or "unsettled_inner_pattern")
        experience_space["last_inner_context_cluster_pattern_recognition_strength"] = float(inner_context_result.get("inner_pattern_recognition_strength", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_recognition_recurrent"] = bool(inner_context_result.get("inner_pattern_recognition_recurrent", False))
        experience_space["last_inner_context_cluster_pattern_recognition_changed"] = bool(inner_context_result.get("inner_pattern_recognition_changed", False))
        experience_space["last_inner_context_cluster_pattern_support_score"] = float(inner_context_result.get("pattern_support_score", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_conflict_score"] = float(inner_context_result.get("pattern_conflict_score", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_fragility_score"] = float(inner_context_result.get("pattern_fragility_score", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_bearing_score"] = float(inner_context_result.get("pattern_bearing_score", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_reinforcement"] = float(inner_context_result.get("pattern_reinforcement", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_pattern_attenuation"] = float(inner_context_result.get("pattern_attenuation", 0.0) or 0.0)
        experience_space["last_inner_context_cluster_self_state"] = str(inner_context_result.get("inner_self_state", "stable") or "stable")
        experience_space["last_inner_context_cluster_attractor"] = str(inner_context_result.get("inner_attractor", "neutral") or "neutral")
    else:
        summary["inner_context_cluster_id"] = str(getattr(bot, "last_inner_context_cluster_id", None) or "-")
        summary["inner_context_cluster_distance"] = 0.0
        summary["inner_context_cluster_score"] = 0.0
        summary["inner_context_cluster_trust"] = 0.0
        summary["inner_context_cluster_mass_mean"] = 0.0
        summary["inner_context_cluster_mass_max"] = 0.0
        summary["inner_context_cluster_center_spread"] = 0.0
        summary["inner_context_cluster_separation"] = 0.0
        summary["inner_context_cluster_center_drift"] = 0.0
        summary["inner_context_cluster_count_drift"] = 0.0
        summary["inner_context_cluster_velocity_trend"] = 0.0
        summary["inner_context_cluster_reorganization_direction"] = "stable"
        summary["inner_context_cluster_mean_velocity"] = 0.0
        summary["inner_context_cluster_regulation_pressure"] = 0.0
        summary["inner_context_cluster_neuron_count"] = 0
        summary["inner_context_cluster_neuron_activation_mean"] = 0.0
        summary["inner_context_cluster_neuron_activation_max"] = 0.0
        summary["inner_context_cluster_neuron_stability_mean"] = 0.0
        summary["inner_context_cluster_neuron_regulation_pressure_mean"] = 0.0
        summary["inner_context_cluster_neuron_memory_norm_mean"] = 0.0
        summary["inner_context_cluster_neuron_coupling_norm_mean"] = 0.0
        summary["inner_context_cluster_neuron_regulation_force_norm_mean"] = 0.0
        summary["inner_context_cluster_neuron_external_impulse_norm_mean"] = 0.0
        summary["inner_context_cluster_neuron_context_memory_impulse_norm_mean"] = 0.0
        summary["inner_context_cluster_areal_count"] = 0
        summary["inner_context_cluster_areal_activation_mean"] = 0.0
        summary["inner_context_cluster_areal_stability_mean"] = 0.0
        summary["inner_context_cluster_areal_pressure_mean"] = 0.0
        summary["inner_context_cluster_areal_drift"] = 0.0
        summary["inner_context_cluster_areal_dominance"] = 0.0
        summary["inner_context_cluster_areal_fragmentation"] = 0.0
        summary["inner_context_cluster_areal_coherence_mean"] = 0.0
        summary["inner_context_cluster_areal_conflict_mean"] = 0.0
        summary["inner_context_cluster_areal_topology_density_mean"] = 0.0
        summary["inner_context_cluster_areal_topology_span_mean"] = 0.0
        summary["inner_context_cluster_areal_topology_boundary_mean"] = 0.0
        summary["inner_context_cluster_topology_cluster_link_count"] = 0
        summary["inner_context_cluster_topology_areal_link_count"] = 0
        summary["inner_context_cluster_topology_link_density"] = 0.0
        summary["inner_context_cluster_topology_distance_mean"] = 0.0
        summary["inner_context_cluster_topology_coherence"] = 0.0
        summary["inner_context_cluster_topology_tension"] = 0.0
        summary["inner_context_cluster_topology_state_label"] = "sparse_topology"
        summary["inner_context_cluster_field_perception_state"] = {}
        summary["inner_context_cluster_activity_island_count"] = 0
        summary["inner_context_cluster_activity_island_mass_mean"] = 0.0
        summary["inner_context_cluster_activity_island_mass_max"] = 0.0
        summary["inner_context_cluster_activity_island_activation_mean"] = 0.0
        summary["inner_context_cluster_activity_island_pressure_mean"] = 0.0
        summary["inner_context_cluster_activity_island_coherence_mean"] = 0.0
        summary["inner_context_cluster_activity_island_context_reactivation_mean"] = 0.0
        summary["inner_context_cluster_activity_island_spread"] = 0.0
        summary["inner_context_cluster_field_perception_label"] = "quiet_field"
        summary["inner_context_cluster_neural_felt_bearing"] = 0.0
        summary["inner_context_cluster_neural_felt_pressure"] = 0.0
        summary["inner_context_cluster_neural_felt_memory_resonance"] = 0.0
        summary["inner_context_cluster_neural_felt_context_reactivation"] = 0.0
        summary["inner_context_cluster_neural_felt_label"] = "quiet_neural_felt"
        summary["inner_context_cluster_pattern_label"] = ""
        summary["inner_context_cluster_field_pattern_signature"] = {}
        summary["inner_context_cluster_field_pattern_signature_key"] = ""
        summary["inner_context_cluster_field_pattern_vector"] = []
        summary["inner_context_cluster_pattern_identity"] = ""
        summary["inner_context_cluster_pattern_identity_label"] = ""
        summary["inner_context_cluster_pattern_identity_confidence"] = 0.0
        summary["inner_context_cluster_pattern_identity_streak"] = 0
        summary["inner_context_cluster_pattern_identity_stability"] = 0.0
        summary["inner_context_cluster_pattern_identity_recurrent"] = False
        summary["inner_context_cluster_pattern_identity_changed"] = False
        summary["inner_context_cluster_pattern_identity_last_seen_tick"] = 0
        summary["inner_context_cluster_pattern_recognition_state"] = {}
        summary["inner_context_cluster_pattern_recognition_label"] = "unsettled_inner_pattern"
        summary["inner_context_cluster_pattern_recognition_strength"] = 0.0
        summary["inner_context_cluster_pattern_recognition_recurrent"] = False
        summary["inner_context_cluster_pattern_recognition_changed"] = False
        summary["inner_context_cluster_self_state"] = "stable"
        summary["inner_context_cluster_attractor"] = "neutral"

    experience_space["market_ticks"] = int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0)
    experience_space["runtime_tick_seq"] = int(((getattr(bot, "mcm_runtime_snapshot", {}) or {}).get("runtime_tick_seq", 0)) or 0)
    experience_space["last_timestamp"] = summary.get("timestamp", None)
    experience_space["last_episode_id"] = str(summary.get("episode_id", "") or "")
    experience_space["last_proposed_decision"] = str(summary.get("proposed_decision", "WAIT") or "WAIT")
    experience_space["last_self_state"] = str(summary.get("self_state", "stable") or "stable")
    experience_space["last_attractor"] = str(summary.get("attractor", "neutral") or "neutral")
    experience_space["last_in_trade_avg_regulatory_load"] = float(summary.get("in_trade_avg_regulatory_load", 0.0) or 0.0)
    experience_space["last_in_trade_avg_action_capacity"] = float(summary.get("in_trade_avg_action_capacity", 0.0) or 0.0)
    experience_space["last_in_trade_avg_recovery_need"] = float(summary.get("in_trade_avg_recovery_need", 0.0) or 0.0)
    experience_space["last_in_trade_avg_survival_pressure"] = float(summary.get("in_trade_avg_survival_pressure", 0.0) or 0.0)
    experience_space["last_in_trade_avg_pressure_to_capacity"] = float(summary.get("in_trade_avg_pressure_to_capacity", 0.0) or 0.0)
    experience_space["last_in_trade_avg_pressure_release"] = float(summary.get("in_trade_avg_pressure_release", 0.0) or 0.0)
    experience_space["last_in_trade_avg_load_bearing_capacity"] = float(summary.get("in_trade_avg_load_bearing_capacity", 0.0) or 0.0)
    experience_space["last_in_trade_avg_state_stability"] = float(summary.get("in_trade_avg_state_stability", 0.0) or 0.0)
    experience_space["last_in_trade_avg_capacity_reserve"] = float(summary.get("in_trade_avg_capacity_reserve", 0.0) or 0.0)
    experience_space["last_in_trade_avg_recovery_balance"] = float(summary.get("in_trade_avg_recovery_balance", 0.0) or 0.0)
    experience_space["last_in_trade_avg_regulated_courage"] = float(summary.get("in_trade_avg_regulated_courage", 0.0) or 0.0)
    experience_space["last_in_trade_avg_courage_gap"] = float(summary.get("in_trade_avg_courage_gap", 0.0) or 0.0)
    experience_space["last_experience_effect_score"] = float(summary.get("experience_effect_score", 0.0) or 0.0)
    experience_space["last_profit_reward"] = float(summary.get("profit_reward", 0.0) or 0.0)
    experience_space["last_relief_signal"] = float(summary.get("relief_signal", 0.0) or 0.0)
    experience_space["last_stability_signal"] = float(summary.get("stability_signal", 0.0) or 0.0)
    experience_space["last_discipline_signal"] = float(summary.get("discipline_signal", 0.0) or 0.0)
    experience_space["last_confidence_signal"] = float(summary.get("confidence_signal", 0.0) or 0.0)
    experience_space["last_overactivation_signal"] = float(summary.get("overactivation_signal", 0.0) or 0.0)
    experience_space["last_chaos_penalty"] = float(summary.get("chaos_penalty", 0.0) or 0.0)
    experience_space["last_variance_penalty"] = float(summary.get("variance_penalty", 0.0) or 0.0)
    experience_space["last_overstrain_penalty"] = float(summary.get("overstrain_penalty", 0.0) or 0.0)
    experience_space["last_carrying_capacity_delta"] = float(summary.get("carrying_capacity_delta", 0.0) or 0.0)
    experience_space["last_self_confidence_delta"] = float(summary.get("self_confidence_delta", 0.0) or 0.0)
    experience_space["last_process_quality"] = float(summary.get("process_quality", 0.0) or 0.0)
    experience_space["last_in_trade_pre_action_phase"] = str(summary.get("in_trade_last_pre_action_phase", "-") or "-")
    experience_space["last_in_trade_dominant_tension_cause"] = str(summary.get("in_trade_last_dominant_tension_cause", "-") or "-")

    if decision_tendency is not None:
        tendency_key = str(decision_tendency or "hold").strip().lower() or "hold"
        experience_space["runtime_internal_ticks"] = int(experience_space.get("runtime_internal_ticks", 0) or 0) + 1
        experience_space[f"tendency_{tendency_key}"] = int(experience_space.get(f"tendency_{tendency_key}", 0) or 0) + 1

    if event_name is not None:
        normalized_event = str(event_name or "runtime_event").strip().lower() or "runtime_event"
        experience_space[f"event_{normalized_event}"] = int(experience_space.get(f"event_{normalized_event}", 0) or 0) + 1
        experience_space["last_event"] = str(normalized_event)
        experience_space["last_event_timestamp"] = summary.get("timestamp", None)

    if summary.get("non_action_type"):
        experience_space["last_non_action_type"] = str(summary.get("non_action_type") or "")

    if str(summary.get("outcome_reason", "-") or "-") != "-":
        experience_space["last_outcome_reason"] = str(summary.get("outcome_reason", "-") or "-")

    summary["experience_reward_delta"] = float(_experience_reward_delta(summary) or 0.0)
    summary["experience_similarity_axes"] = dict(_build_experience_similarity_axes(summary) or {})

    experience_space = _append_experience_episode(experience_space, summary)
    experience_space = _update_experience_link_bucket(experience_space, "signature_links", summary.get("signature_key"), summary)
    experience_space = _update_experience_link_bucket(experience_space, "context_links", summary.get("context_cluster_id"), summary)

    if str(summary.get("inner_context_cluster_id", "-") or "-") != "-":
        experience_space = _update_experience_link_bucket(
            experience_space,
            "inner_context_links",
            summary.get("inner_context_cluster_id"),
            summary,
        )

    experience_space = _update_experience_link_bucket(
        experience_space,
        "decision_links",
        f"{str(summary.get('decision_tendency', 'hold') or 'hold')}::{str(summary.get('proposed_decision', 'WAIT') or 'WAIT')}",
        summary,
    )

    non_action_type = summary.get("non_action_type", None)
    if non_action_type:
        experience_space = _update_experience_link_bucket(experience_space, "non_action_links", non_action_type, summary)

    bot.mcm_experience_space = dict(experience_space)
    return dict(experience_space)

# --------------------------------------------------
def _update_experience_link_bucket(space, bucket_name, link_key, summary):
    return _update_experience_link_bucket_impl(space, bucket_name, link_key, summary)

# --------------------------------------------------
def _update_field_decision_outcome_protocol(space, summary):
    return _update_field_decision_outcome_protocol_impl(space, summary)

# --------------------------------------------------
def _append_experience_episode(space, summary):
    return _append_experience_episode_impl(space, summary)

# --------------------------------------------------
def _read_experience_episode_context(bot, timestamp=None, decision_tendency=None, event_name=None):
    episode = dict(getattr(bot, "mcm_decision_episode", {}) or {}) if bot is not None else {}
    episode_internal = dict(getattr(bot, "mcm_decision_episode_internal", {}) or {}) if bot is not None else {}
    outcome_decomposition = dict(getattr(bot, "last_outcome_decomposition", {}) or {}) if bot is not None else {}
    runtime_state = dict(getattr(bot, "mcm_runtime_decision_state", {}) or {}) if bot is not None else {}
    review_notes = dict(episode_internal.get("review_notes", {}) or {})
    in_trade_updates = list(episode_internal.get("in_trade_updates", []) or [])
    in_trade_summary = _summarize_in_trade_updates(in_trade_updates)

    signal = dict(episode_internal.get("signal", {}) or {})
    inner_field = dict(episode_internal.get("inner_field_perception_state", {}) or {})
    focus = dict(episode_internal.get("focus", {}) or {})
    felt_state = dict(episode_internal.get("felt_state", getattr(bot, "felt_state", {}) if bot is not None else {}) or {})
    processing_state = dict(episode_internal.get("processing_state", getattr(bot, "processing_state", {}) if bot is not None else {}) or {})
    thought_state = dict(episode_internal.get("thought_state", getattr(bot, "thought_state", {}) if bot is not None else {}) or {})
    state_signature = dict(episode.get("state_signature", {}) or {})
    last_payload = dict(episode_internal.get("last_payload", episode.get("last_payload", {})) or {})
    state_before = dict(last_payload.get("state_before", {}) or {})
    state_after = dict(last_payload.get("state_after", {}) or {})
    state_delta = dict(last_payload.get("state_delta", {}) or {})
    neural_felt_state = dict(inner_field.get("neural_felt_state", felt_state.get("neural_felt_state", {})) or {})
    neural_felt_bearing = float(inner_field.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", felt_state.get("neural_felt_bearing", 0.0))) or 0.0)
    neural_felt_pressure = float(inner_field.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", felt_state.get("neural_felt_pressure", 0.0))) or 0.0)
    neural_felt_memory_resonance = float(neural_felt_state.get("neural_felt_memory_resonance", felt_state.get("neural_felt_memory_resonance", 0.0)) or 0.0)
    neural_felt_context_reactivation = float(neural_felt_state.get("neural_felt_context_reactivation", felt_state.get("neural_felt_context_reactivation", 0.0)) or 0.0)
    neural_felt_label = str(inner_field.get("neural_felt_label", neural_felt_state.get("neural_felt_label", felt_state.get("neural_felt_label", "quiet_neural_felt"))) or "quiet_neural_felt")

    summary_timestamp = timestamp
    if summary_timestamp is None:
        summary_timestamp = episode.get("timestamp", episode_internal.get("timestamp", None))

    summary_event_name = str(event_name or episode_internal.get("last_event", episode.get("last_event", "-")) or "-").strip().lower() or "-"
    summary_decision_tendency = str(decision_tendency or episode.get("decision_tendency", (getattr(bot, "mcm_runtime_decision_state", {}) or {}).get("decision_tendency", "hold")) or "hold").strip().lower()
    summary_outcome_reason = str(outcome_decomposition.get("reason", last_payload.get("reason", "-")) or "-").strip().lower() or "-"

    if summary_outcome_reason == "blocked_value_gate":
        summary_outcome_reason = str(last_payload.get("reason", "blocked_value_gate") or "blocked_value_gate").strip().lower()

    return {
        "episode": dict(episode or {}),
        "episode_internal": dict(episode_internal or {}),
        "outcome_decomposition": dict(outcome_decomposition or {}),
        "runtime_state": dict(runtime_state or {}),
        "review_notes": dict(review_notes or {}),
        "in_trade_summary": dict(in_trade_summary or {}),
        "signal": dict(signal or {}),
        "inner_field": dict(inner_field or {}),
        "focus": dict(focus or {}),
        "felt_state": dict(felt_state or {}),
        "processing_state": dict(processing_state or {}),
        "thought_state": dict(thought_state or {}),
        "state_signature": dict(state_signature or {}),
        "last_payload": dict(last_payload or {}),
        "state_before": dict(state_before or {}),
        "state_after": dict(state_after or {}),
        "state_delta": dict(state_delta or {}),
        "neural_felt_state": dict(neural_felt_state or {}),
        "neural_felt_bearing": float(neural_felt_bearing),
        "neural_felt_pressure": float(neural_felt_pressure),
        "neural_felt_memory_resonance": float(neural_felt_memory_resonance),
        "neural_felt_context_reactivation": float(neural_felt_context_reactivation),
        "neural_felt_label": str(neural_felt_label),
        "summary_timestamp": summary_timestamp,
        "summary_event_name": str(summary_event_name),
        "summary_decision_tendency": str(summary_decision_tendency),
        "summary_outcome_reason": str(summary_outcome_reason),
    }

# --------------------------------------------------
def _build_experience_base_summary(bot, context):

    context = dict(context or {})
    episode = dict(context.get("episode", {}) or {})
    episode_internal = dict(context.get("episode_internal", {}) or {})
    outcome_decomposition = dict(context.get("outcome_decomposition", {}) or {})
    runtime_state = dict(context.get("runtime_state", {}) or {})
    review_notes = dict(context.get("review_notes", {}) or {})
    in_trade_summary = dict(context.get("in_trade_summary", {}) or {})
    signal = dict(context.get("signal", {}) or {})
    inner_field = dict(context.get("inner_field", {}) or {})
    focus = dict(context.get("focus", {}) or {})
    felt_state = dict(context.get("felt_state", {}) or {})
    processing_state = dict(context.get("processing_state", {}) or {})
    thought_state = dict(context.get("thought_state", {}) or {})
    state_signature = dict(context.get("state_signature", {}) or {})
    state_before = dict(context.get("state_before", {}) or {})
    state_after = dict(context.get("state_after", {}) or {})
    state_delta = dict(context.get("state_delta", {}) or {})
    neural_felt_state = dict(context.get("neural_felt_state", {}) or {})
    neural_felt_bearing = float(context.get("neural_felt_bearing", 0.0) or 0.0)
    neural_felt_pressure = float(context.get("neural_felt_pressure", 0.0) or 0.0)
    neural_felt_memory_resonance = float(context.get("neural_felt_memory_resonance", 0.0) or 0.0)
    neural_felt_context_reactivation = float(context.get("neural_felt_context_reactivation", 0.0) or 0.0)
    neural_felt_label = str(context.get("neural_felt_label", "quiet_neural_felt") or "quiet_neural_felt")
    summary_timestamp = context.get("summary_timestamp", None)
    summary_event_name = str(context.get("summary_event_name", "-") or "-")
    summary_decision_tendency = str(context.get("summary_decision_tendency", "hold") or "hold")
    summary_outcome_reason = str(context.get("summary_outcome_reason", "-") or "-")

    summary = {
        "episode_id": str(episode.get("episode_id", "") or ""),
        "visible_episode_id": str(episode_internal.get("visible_episode_id", episode.get("episode_id", "")) or ""),
        "timestamp": summary_timestamp,
        "event_name": str(summary_event_name),
        "decision_tendency": str(summary_decision_tendency),
        "proposed_decision": str(episode.get("proposed_decision", runtime_state.get("proposed_decision", "WAIT")) or "WAIT"),
        "signature_key": str(state_signature.get("signature_key", getattr(bot, "last_signature_key", None) if bot is not None else None) or "-"),
        "context_cluster_id": str(signal.get("context_cluster_id", getattr(bot, "last_context_cluster_id", None) if bot is not None else None) or "-"),
        "self_state": str(inner_field.get("self_state", getattr(bot, "mcm_last_action", "stable") if bot is not None else "stable") or "stable"),
        "attractor": str(inner_field.get("attractor", getattr(bot, "mcm_last_attractor", "neutral") if bot is not None else "neutral") or "neutral"),
        "focus_confidence": float(focus.get("focus_confidence", getattr(bot, "focus_confidence", 0.0) if bot is not None else 0.0) or 0.0),
        "competition_bias": float(signal.get("competition_bias", getattr(bot, "competition_bias", 0.0) if bot is not None else 0.0) or 0.0),
        "non_action_type": str(episode_internal.get("non_action_type", "") or "").strip().lower() or None,
        "outcome_reason": str(summary_outcome_reason),
        "perception_quality": float(outcome_decomposition.get("perception_quality", 0.0) or 0.0),
        "felt_quality": float(outcome_decomposition.get("felt_quality", 0.0) or 0.0),
        "thought_quality": float(outcome_decomposition.get("thought_quality", 0.0) or 0.0),
        "plan_quality": float(outcome_decomposition.get("plan_quality", 0.0) or 0.0),
        "execution_quality": float(outcome_decomposition.get("execution_quality", 0.0) or 0.0),
        "risk_fit_quality": float(outcome_decomposition.get("risk_fit_quality", 0.0) or 0.0),
        "experience_packet_label": str(outcome_decomposition.get("experience_packet_label", "-") or "-"),
        "packet_bearing_quality": float(outcome_decomposition.get("packet_bearing_quality", 0.0) or 0.0),
        "packet_inner_outer_fit": float(outcome_decomposition.get("packet_inner_outer_fit", 0.0) or 0.0),
        "packet_confidence_integrity": float(outcome_decomposition.get("packet_confidence_integrity", 0.0) or 0.0),
        "packet_repetition_potential": float(outcome_decomposition.get("packet_repetition_potential", 0.0) or 0.0),
        "packet_curiosity_pull": float(outcome_decomposition.get("packet_curiosity_pull", 0.0) or 0.0),
        "packet_process_reward": float(outcome_decomposition.get("packet_process_reward", 0.0) or 0.0),
        "packet_reorganization_need": float(outcome_decomposition.get("packet_reorganization_need", 0.0) or 0.0),
        "constructive_stimulation": float(outcome_decomposition.get("constructive_stimulation", 0.0) or 0.0),
        "constructive_dopamine": float(outcome_decomposition.get("constructive_dopamine", 0.0) or 0.0),
        "stabilizing_serotonin": float(outcome_decomposition.get("stabilizing_serotonin", 0.0) or 0.0),
        "relief_endorphin": float(outcome_decomposition.get("relief_endorphin", 0.0) or 0.0),
        "focused_acetylcholine": float(outcome_decomposition.get("focused_acetylcholine", 0.0) or 0.0),
        "review_label": str(review_notes.get("review_label", "-") or "-"),
        "review_score": float(review_notes.get("review_score", 0.0) or 0.0),
        "decision_path_quality": float(review_notes.get("decision_path_quality", 0.0) or 0.0),
        "uncertainty_recognition_quality": float(review_notes.get("uncertainty_recognition_quality", 0.0) or 0.0),
        "observation_quality": float(review_notes.get("observation_quality", 0.0) or 0.0),
        "correction_timing_quality": float(review_notes.get("correction_timing_quality", 0.0) or 0.0),
        "structural_bearing_quality": float(review_notes.get("structural_bearing_quality", 0.0) or 0.0),
        "bearing_regulation_cost": float(review_notes.get("bearing_regulation_cost", 0.0) or 0.0),
        "relief_quality": float(review_notes.get("relief_quality", 0.0) or 0.0),
        "carrying_room": float(review_notes.get("carrying_room", 0.0) or 0.0),
        "action_inhibition": float(review_notes.get("action_inhibition", 0.0) or 0.0),
        "action_clearance": float(review_notes.get("action_clearance", 0.0) or 0.0),
        "field_areal_count": int(inner_field.get("field_areal_count", 0) or 0),
        "field_areal_activation_mean": float(inner_field.get("field_areal_activation_mean", 0.0) or 0.0),
        "field_areal_stability_mean": float(inner_field.get("field_areal_stability_mean", 0.0) or 0.0),
        "field_areal_pressure_mean": float(inner_field.get("field_areal_pressure_mean", 0.0) or 0.0),
        "field_areal_drift": float(inner_field.get("field_areal_drift", 0.0) or 0.0),
        "field_areal_dominance": float(inner_field.get("field_areal_dominance", 0.0) or 0.0),
        "field_areal_fragmentation": float(inner_field.get("field_areal_fragmentation", 0.0) or 0.0),
        "field_areal_coherence_mean": float(inner_field.get("field_areal_coherence_mean", 0.0) or 0.0),
        "field_areal_conflict_mean": float(inner_field.get("field_areal_conflict_mean", 0.0) or 0.0),
        "neural_felt_state": dict(neural_felt_state or {}),
        "neural_felt_bearing": float(neural_felt_bearing),
        "neural_felt_pressure": float(neural_felt_pressure),
        "neural_felt_memory_resonance": float(neural_felt_memory_resonance),
        "neural_felt_context_reactivation": float(neural_felt_context_reactivation),
        "neural_felt_label": str(neural_felt_label),
        "processing_areal_tension": float(processing_state.get("processing_areal_tension", 0.0) or 0.0),
        "processing_areal_support": float(processing_state.get("processing_areal_support", 0.0) or 0.0),
        "thought_decision_conflict": float(thought_state.get("decision_conflict", 0.0) or 0.0),
        "thought_state_maturity": float(thought_state.get("state_maturity", 0.0) or 0.0),
        "thought_rumination_depth": float(thought_state.get("rumination_depth", 0.0) or 0.0),
        "thought_inner_time_scale": float(thought_state.get("inner_time_scale", 0.0) or 0.0),
        "thought_decision_readiness": float(thought_state.get("decision_readiness", 0.0) or 0.0),
        "thought_alignment": float(thought_state.get("thought_alignment", 0.0) or 0.0),
        "thought_decision_pressure": float(thought_state.get("decision_pressure", 0.0) or 0.0),
        "thought_inertia": float(thought_state.get("thought_inertia", 0.0) or 0.0),
        "thought_settlement": float(thought_state.get("thought_settlement", 0.0) or 0.0),
        "thought_drift": float(thought_state.get("thought_drift", 0.0) or 0.0),
        "thought_areal_pressure": float(thought_state.get("thought_areal_pressure", 0.0) or 0.0),
        "thought_areal_support": float(thought_state.get("thought_areal_support", 0.0) or 0.0),
        "in_trade_update_count": int(in_trade_summary.get("in_trade_update_count", 0) or 0),
        "in_trade_max_mfe": float(in_trade_summary.get("in_trade_max_mfe", 0.0) or 0.0),
        "in_trade_max_mae": float(in_trade_summary.get("in_trade_max_mae", 0.0) or 0.0),
        "in_trade_last_bars_open": int(in_trade_summary.get("in_trade_last_bars_open", 0) or 0),
        "in_trade_avg_fill_ratio": float(in_trade_summary.get("in_trade_avg_fill_ratio", 0.0) or 0.0),
        "in_trade_direction_stability": float(in_trade_summary.get("in_trade_direction_stability", 0.0) or 0.0),
        "in_trade_avg_regulatory_load": float(in_trade_summary.get("in_trade_avg_regulatory_load", 0.0) or 0.0),
        "in_trade_avg_action_capacity": float(in_trade_summary.get("in_trade_avg_action_capacity", 0.0) or 0.0),
        "in_trade_avg_recovery_need": float(in_trade_summary.get("in_trade_avg_recovery_need", 0.0) or 0.0),
        "in_trade_avg_survival_pressure": float(in_trade_summary.get("in_trade_avg_survival_pressure", 0.0) or 0.0),
        "in_trade_avg_pressure_to_capacity": float(in_trade_summary.get("in_trade_avg_pressure_to_capacity", 0.0) or 0.0),
        "in_trade_avg_pressure_release": float(in_trade_summary.get("in_trade_avg_pressure_release", 0.0) or 0.0),
        "in_trade_avg_load_bearing_capacity": float(in_trade_summary.get("in_trade_avg_load_bearing_capacity", 0.0) or 0.0),
        "in_trade_avg_state_stability": float(in_trade_summary.get("in_trade_avg_state_stability", 0.0) or 0.0),
        "in_trade_avg_capacity_reserve": float(in_trade_summary.get("in_trade_avg_capacity_reserve", 0.0) or 0.0),
        "in_trade_avg_recovery_balance": float(in_trade_summary.get("in_trade_avg_recovery_balance", 0.0) or 0.0),
        "in_trade_avg_regulated_courage": float(in_trade_summary.get("in_trade_avg_regulated_courage", 0.0) or 0.0),
        "in_trade_avg_courage_gap": float(in_trade_summary.get("in_trade_avg_courage_gap", 0.0) or 0.0),
        "in_trade_avg_field_areal_count": float(in_trade_summary.get("in_trade_avg_field_areal_count", 0.0) or 0.0),
        "in_trade_avg_field_areal_activation_mean": float(in_trade_summary.get("in_trade_avg_field_areal_activation_mean", 0.0) or 0.0),
        "in_trade_avg_field_areal_stability_mean": float(in_trade_summary.get("in_trade_avg_field_areal_stability_mean", 0.0) or 0.0),
        "in_trade_avg_field_areal_pressure_mean": float(in_trade_summary.get("in_trade_avg_field_areal_pressure_mean", 0.0) or 0.0),
        "in_trade_avg_field_areal_drift": float(in_trade_summary.get("in_trade_avg_field_areal_drift", 0.0) or 0.0),
        "in_trade_avg_field_areal_dominance": float(in_trade_summary.get("in_trade_avg_field_areal_dominance", 0.0) or 0.0),
        "in_trade_avg_field_areal_fragmentation": float(in_trade_summary.get("in_trade_avg_field_areal_fragmentation", 0.0) or 0.0),
        "in_trade_avg_field_areal_coherence_mean": float(in_trade_summary.get("in_trade_avg_field_areal_coherence_mean", 0.0) or 0.0),
        "in_trade_avg_field_areal_conflict_mean": float(in_trade_summary.get("in_trade_avg_field_areal_conflict_mean", 0.0) or 0.0),
        "in_trade_last_pre_action_phase": str(in_trade_summary.get("in_trade_last_pre_action_phase", "-") or "-"),
        "in_trade_last_dominant_tension_cause": str(in_trade_summary.get("in_trade_last_dominant_tension_cause", "-") or "-"),
        "felt_state": dict(felt_state or {}),
        "state_before": dict(state_before or {}),
        "state_after": dict(state_after or {}),
        "state_delta": dict(state_delta or {}),
    }

    return dict(summary or {})

# --------------------------------------------------
def _build_experience_episode_summary(bot, timestamp=None, decision_tendency=None, event_name=None):

    context = _read_experience_episode_context(
        bot,
        timestamp=timestamp,
        decision_tendency=decision_tendency,
        event_name=event_name,
    )
    summary = _build_experience_base_summary(bot, context)

    return _complete_experience_episode_summary(summary)

# --------------------------------------------------
def mark_runtime_episode_event(bot, event_name, payload=None):

    if bot is None:
        return None

    event_key = str(event_name or "").strip().lower() or "runtime_event"
    payload_dict = dict(payload or {})
    timestamp = getattr(bot, "current_timestamp", None)

    episode = dict(getattr(bot, "mcm_decision_episode", {}) or {})
    episode_internal = dict(getattr(bot, "mcm_decision_episode_internal", {}) or {})

    if not episode:
        bot.mcm_episode_seq = int(getattr(bot, "mcm_episode_seq", 0) or 0) + 1
        episode = {
            "episode_id": f"ep_{int(getattr(bot, 'mcm_episode_seq', 0) or 0)}",
            "timestamp": timestamp,
            "lifecycle_state": "event_only",
            "action_status": "open",
            "decision_tendency": str(((getattr(bot, "mcm_runtime_decision_state", {}) or {}).get("decision_tendency", "hold") or "hold")),
            "proposed_decision": str(((getattr(bot, "mcm_runtime_decision_state", {}) or {}).get("proposed_decision", "WAIT") or "WAIT")),
            "events": [],
        }

    if not episode_internal:
        episode_internal = {
            "episode_id": str(episode.get("episode_id", "") or ""),
            "visible_episode_id": str(episode.get("episode_id", "") or ""),
            "timestamp": timestamp,
            "learning_state": "open",
            "internal_events": [],
            "in_trade_updates": [],
            "review_notes": {},
        }

    status_map = {
        "submitted": ("submitted", "submitted"),
        "blocked_value_gate": ("blocked", "blocked_value_gate"),
        "observed_only": ("observed_only", "observed_only"),
        "withheld": ("withheld", "withheld"),
        "replanned": ("replanned", "replanned"),
        "abandoned": ("abandoned", "abandoned"),
        "cancelled": ("cancelled", "cancelled"),
        "filled": ("filled", "filled"),
        "pending_update": ("tracking", "in_trade_updates"),
        "position_update": ("tracking", "in_trade_updates"),
        "in_trade_update": ("tracking", "in_trade_updates"),
        "monitor_update": ("tracking", "in_trade_updates"),
        "timeout": ("timeout", "timeout"),
        "resolved": ("resolved", "resolved"),
        "reviewed": ("reviewed", "reviewed"),
    }

    action_status, lifecycle_state = status_map.get(event_key, (event_key, event_key))

    events = list(episode.get("events", []) or [])
    events.append({
        "event": str(event_key),
        "timestamp": timestamp,
        "payload": dict(payload_dict or {}),
    })

    internal_events = list(episode_internal.get("internal_events", []) or [])
    internal_events.append({
        "event": str(event_key),
        "timestamp": timestamp,
        "payload": dict(payload_dict or {}),
    })

    in_trade_updates = list(episode_internal.get("in_trade_updates", []) or [])
    if event_key in ("pending_update", "position_update", "in_trade_update", "monitor_update"):
        in_trade_updates.append({
            "event": str(event_key),
            "timestamp": timestamp,
            "payload": _compact_in_trade_update_payload(payload_dict),
        })

    episode["timestamp"] = timestamp
    episode["action_status"] = str(action_status)
    episode["lifecycle_state"] = str(lifecycle_state)
    episode["last_event"] = str(event_key)
    episode["last_payload"] = dict(payload_dict or {})
    episode["events"] = list(events[-24:])
    episode[f"{event_key}_at"] = timestamp

    episode_internal["episode_id"] = str(episode.get("episode_id", "") or "")
    episode_internal["visible_episode_id"] = str(episode.get("episode_id", "") or "")
    episode_internal["timestamp"] = timestamp
    episode_internal["learning_state"] = "ready_for_review" if event_key in ("resolved", "cancelled", "timeout", "blocked_value_gate", "observed_only", "withheld", "replanned", "abandoned") else ("tracking" if event_key in ("pending_update", "position_update", "in_trade_update", "monitor_update") else str(episode_internal.get("learning_state", "open") or "open"))
    episode_internal["last_event"] = str(event_key)
    episode_internal["last_payload"] = dict(payload_dict or {})
    episode_internal["internal_events"] = list(internal_events[-24:])
    episode_internal["in_trade_updates"] = list(in_trade_updates[-24:])
    episode_internal[f"{event_key}_at"] = timestamp

    if event_key in ("observed_only", "withheld", "replanned", "abandoned"):
        episode_internal["non_action_type"] = str(event_key)

    if event_key in ("blocked_value_gate", "observed_only", "withheld", "replanned", "abandoned", "cancelled", "timeout", "resolved", "reviewed", "pending_update", "position_update", "in_trade_update", "monitor_update"):
        episode_internal["review_notes"] = _build_episode_review_notes(
            bot,
            episode=episode,
            episode_internal=episode_internal,
            event_name=event_key,
            timestamp=timestamp,
        )

    bot.mcm_decision_episode = dict(episode)
    bot.mcm_decision_episode_internal = dict(episode_internal)

    tracking_events = {"pending_update", "position_update", "in_trade_update", "monitor_update"}
    if event_key not in tracking_events or bool(getattr(Config, "MCM_EXPERIENCE_REFRESH_TRACKING_EVENTS", True)):
        _refresh_experience_space(
            bot,
            timestamp=timestamp,
            event_name=event_key,
        )

    return dict(episode)

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
    return _derive_felt_label_impl(
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

# --------------------------------------------------
def _build_episode_felt_summary(summary):
    return _build_episode_felt_summary_impl(summary)

# --------------------------------------------------
def _complete_experience_episode_summary(summary):
    return _complete_experience_episode_summary_impl(summary)

# --------------------------------------------------
def _build_affective_structure_profile(episodes):
    return _build_affective_structure_profile_impl(episodes)

# --------------------------------------------------
from core.mcm_field import _resolve_affective_context_modulation

def build_runtime_pipeline_snapshot(bot=None):
    return _build_runtime_pipeline_snapshot_impl(
        bot=bot,
        profile_start=_mcm_profile_start,
        profile_debug=_mcm_profile_debug,
    )

# --------------------------------------------------
# DEBUG
# --------------------------------------------------
def _mcm_state_debug(msg):
    if bool(getattr(Config, "MCM_DEBUG", False)):
        dbr_debug(msg, "mcm_state_debug.csv")

def _mcm_decision_debug(msg):
    if bool(getattr(Config, "MCM_DEBUG", False)):
        dbr_debug(msg, "mcm_decision_debug.csv")

def _mcm_outcome_debug(msg):
    if bool(getattr(Config, "MCM_OUTCOME_DEBUG", False)):
        dbr_debug(msg, "mcm_outcome_debug.csv")

def _mcm_profile_start():
    if not bool(getattr(Config, "MCM_RUNTIME_PROFILE_DEBUG", False)):
        return 0.0

    try:
        return float(time.perf_counter())
    except Exception:
        return 0.0

def _mcm_profile_debug(section, start_time, extra=None):
    try:
        started = float(start_time or 0.0)
    except Exception:
        started = 0.0

    if started <= 0.0:
        return

    try:
        elapsed_ms = (float(time.perf_counter()) - started) * 1000.0
        dbr_profile(section, elapsed_ms, extra=extra)
    except Exception:
        pass

from debug_tools.protocols import (
    _record_active_mcm_contact_protocol,
    _record_field_decision_protocol,
    _record_memory_thinking_protocol,
    _record_neuro_transition_protocol,
    _record_strategic_window_protocol,
)
from debug_tools.visualization import (
    build_visualization_snapshot_bundle as _build_visualization_snapshot_bundle_impl,
    capture_runtime_regulation_transition as _capture_runtime_regulation_transition_impl,
    commit_runtime_regulation_snapshot as _commit_runtime_regulation_snapshot_impl,
    prepare_visualization_snapshot_state as _prepare_visualization_snapshot_state_impl,
    write_visualization_snapshot_bundle as _write_visualization_snapshot_bundle_impl,
)

def create_mcm_brain():
    return _create_mcm_brain_impl(
        Config,
        field_cls=MCMField,
        cluster_detector_cls=ClusterDetector,
        memory_cls=Memory,
        self_model_cls=SelfModel,
        attractor_system_cls=AttractorSystem,
        regulation_layer_cls=RegulationLayer,
    )

# --------------------------------------------------
# FIELD TOPOLOGY ANALYSIS
# --------------------------------------------------
def _build_field_topology_state(snapshot):
    return _build_field_topology_state_impl(snapshot)

# --------------------------------------------------
# Build Neural Felt State
# --------------------------------------------------
def _build_neural_felt_state(inner_field_state):
    return _build_neural_felt_state_impl(inner_field_state)

# --------------------------------------------------
# STIMULUS
# --------------------------------------------------
def build_market_vision(candle_state, tension_state):

    energy = float(tension_state.get("energy", 0.0) or 0.0)
    energy_raw_amplitude = float(tension_state.get("energy_raw_amplitude", abs(energy)) or 0.0)
    energy_limited_amplitude = float(tension_state.get("energy_limited_amplitude", abs(energy)) or 0.0)
    energy_amplitude_stimulus = float(tension_state.get("energy_amplitude_stimulus", energy_limited_amplitude) or 0.0)
    energy_limiter_gain = float(tension_state.get("energy_limiter_gain", 1.0) or 1.0)
    energy_overdrive = float(tension_state.get("energy_overdrive", 0.0) or 0.0)
    market_hearing_state = dict(tension_state.get("market_hearing_state", {}) or {})
    market_loudness = float(market_hearing_state.get("loudness", tension_state.get("market_loudness", energy_amplitude_stimulus)) or 0.0)
    market_frequency_hz = float(market_hearing_state.get("frequency_hz", tension_state.get("market_frequency_hz", 0.0)) or 0.0)
    market_hearing_compression = float(market_hearing_state.get("compression", tension_state.get("market_hearing_compression", 0.0)) or 0.0)
    market_tone = str(market_hearing_state.get("tone", tension_state.get("market_tone", "silent_tone")) or "silent_tone")
    coherence = float(tension_state.get("coherence", 0.0) or 0.0)
    asymmetry = float(tension_state.get("asymmetry", 0.0) or 0.0)
    coh_zone = float(tension_state.get("coh_zone", 0.0) or 0.0)
    relative_range = float(tension_state.get("relative_range", 0.0) or 0.0)
    momentum = float(tension_state.get("momentum", 0.0) or 0.0)
    stability = float(tension_state.get("stability", 0.0) or 0.0)
    perceived_pressure = float(tension_state.get("perceived_pressure", 0.0) or 0.0)
    volume_pressure = float(tension_state.get("volume_pressure", 0.0) or 0.0)

    close_position = float(candle_state.get("close_position", 0.0) or 0.0)
    wick_bias = float(candle_state.get("wick_bias", 0.0) or 0.0)
    return_intensity = float(candle_state.get("return_intensity", 0.0) or 0.0)

    left_eye_flow = (coherence * 0.84) + (coh_zone * 0.22) + (momentum * 0.18)
    right_eye_flow = (close_position * 0.78) + (return_intensity * 0.44) + (volume_pressure * 0.12)
    optic_flow = (left_eye_flow * 0.52) + (right_eye_flow * 0.42) + (asymmetry * 0.10) + (momentum * 0.12)
    auditory_stimulus = max(0.0, min(2.5, market_loudness if market_hearing_state else energy_amplitude_stimulus))
    threat_map = (abs(wick_bias) * 0.48) + abs(min(0.0, coherence)) * 0.22 + (perceived_pressure * 0.32) + (max(0.0, 1.0 - stability) * 0.16)
    target_map = (max(0.0, coherence) * 0.34) + (max(0.0, close_position) * 0.28) + (max(0.0, return_intensity) * 0.14) + (max(0.0, momentum) * 0.16) + (max(0.0, stability - 0.50) * 0.18)
    orientation_drive = optic_flow * 0.68 + (momentum * 0.24) - (threat_map * 0.12) + (relative_range * 0.10)
    vision_contrast = abs(coherence - close_position) + abs(wick_bias) * 0.26 + abs(momentum) * 0.10 + max(0.0, relative_range - 0.55) * 0.18 + (1.0 - stability) * 0.12

    return {
        "left_eye_field": float(max(-2.5, min(2.5, left_eye_flow))),
        "right_eye_field": float(max(-2.5, min(2.5, right_eye_flow))),
        "optic_flow": float(max(-2.5, min(2.5, optic_flow))),
        "energy_raw_amplitude": float(energy_raw_amplitude),
        "energy_limited_amplitude": float(energy_limited_amplitude),
        "energy_amplitude_stimulus": float(auditory_stimulus),
        "energy_limiter_gain": float(energy_limiter_gain),
        "energy_overdrive": float(energy_overdrive),
        "energy_frequency_stimulus": float(auditory_stimulus),
        "auditory_stimulus": float(auditory_stimulus),
        "market_hearing_state": dict(market_hearing_state or {
            "loudness": float(auditory_stimulus),
            "frequency_hz": float(market_frequency_hz),
            "compression": float(market_hearing_compression),
            "tone": str(market_tone),
        }),
        "market_loudness": float(auditory_stimulus),
        "market_frequency_hz": float(market_frequency_hz),
        "market_hearing_compression": float(market_hearing_compression),
        "market_tone": str(market_tone),
        "threat_map": float(max(0.0, min(2.5, threat_map))),
        "target_map": float(max(0.0, min(2.5, target_map))),
        "orientation_drive": float(max(-2.5, min(2.5, orientation_drive))),
        "vision_contrast": float(max(0.0, min(2.5, vision_contrast))),
    }

def build_focus_projection(candle_state, tension_state, vision, pause_mode=False, bot=None):

    coherence = float(tension_state.get("coherence", 0.0) or 0.0)
    energy = float(tension_state.get("energy", 0.0) or 0.0)
    close_position = float(candle_state.get("close_position", 0.0) or 0.0)
    return_intensity = float(candle_state.get("return_intensity", 0.0) or 0.0)

    optic_flow = float(vision.get("optic_flow", 0.0) or 0.0)
    threat_map = float(vision.get("threat_map", 0.0) or 0.0)
    target_map = float(vision.get("target_map", 0.0) or 0.0)
    orientation_drive = float(vision.get("orientation_drive", 0.0) or 0.0)
    vision_contrast = float(vision.get("vision_contrast", 0.0) or 0.0)

    prev_focus_point = 0.0
    prev_focus_confidence = 0.0
    prev_target_lock = 0.0
    prev_target_drift = 0.0

    if bot is not None:
        prev_focus_point = float(getattr(bot, "focus_point", 0.0) or 0.0)
        prev_focus_confidence = float(getattr(bot, "focus_confidence", 0.0) or 0.0)
        prev_target_lock = float(getattr(bot, "target_lock", 0.0) or 0.0)
        prev_target_drift = float(getattr(bot, "target_drift", 0.0) or 0.0)

    focus_direction = (
        orientation_drive * 0.38
        + coherence * 0.20
        + close_position * 0.18
        + return_intensity * 0.10
        + prev_focus_point * 0.14
    )

    raw_focus_strength = (
        target_map * float(getattr(Config, "MCM_FOCUS_TARGET_WEIGHT", 0.72) or 0.72)
        + max(0.0, optic_flow) * float(getattr(Config, "MCM_FOCUS_FLOW_WEIGHT", 0.18) or 0.18)
        + max(0.0, coherence) * 0.08
        + prev_target_lock * 0.12
    )

    noise_damp = (
        vision_contrast * float(getattr(Config, "MCM_FOCUS_NOISE_WEIGHT", 0.34) or 0.34)
        + threat_map * float(getattr(Config, "MCM_FOCUS_THREAT_NOISE_WEIGHT", 0.18) or 0.18)
        + max(0.0, abs(energy) - 1.25) * 0.10
        + max(0.0, abs(prev_target_drift) - 0.20) * 0.18
    )

    if bool(pause_mode):
        noise_damp += float(getattr(Config, "MCM_FOCUS_PAUSE_NOISE_ADD", 0.22) or 0.22)

    focus_strength = max(0.0, raw_focus_strength - noise_damp)

    target_lock = max(
        0.0,
        min(
            1.0,
            (focus_strength * 0.52)
            + (max(0.0, coherence) * 0.12)
            + (prev_target_lock * 0.20)
            + (prev_focus_confidence * 0.10),
        ),
    )

    focus_confidence = max(
        0.0,
        min(
            1.0,
            (target_map * 0.28)
            + (max(0.0, coherence) * 0.22)
            + (max(0.0, return_intensity) * 0.16)
            + (prev_focus_confidence * 0.18)
            - (vision_contrast * 0.18)
            - (threat_map * 0.12),
        ),
    )

    signal_relevance = max(
        0.0,
        min(
            1.0,
            (target_lock * 0.38)
            + (focus_confidence * 0.32)
            + (max(0.0, abs(focus_direction)) * 0.10)
            - (noise_damp * 0.10),
        ),
    )

    return {
        "focus_direction": float(max(-2.5, min(2.5, focus_direction))),
        "focus_strength": float(max(0.0, min(2.5, focus_strength))),
        "focus_confidence": float(max(0.0, min(1.0, focus_confidence))),
        "target_lock": float(max(0.0, min(1.0, target_lock))),
        "noise_damp": float(max(0.0, min(2.5, noise_damp))),
        "signal_relevance": float(max(0.0, min(1.0, signal_relevance))),
    }

def apply_focus_filter(candle_state, tension_state, vision, focus, pause_mode=False):

    left_eye_field = float(vision.get("left_eye_field", 0.0) or 0.0)
    right_eye_field = float(vision.get("right_eye_field", 0.0) or 0.0)
    optic_flow = float(vision.get("optic_flow", 0.0) or 0.0)
    threat_map = float(vision.get("threat_map", 0.0) or 0.0)
    target_map = float(vision.get("target_map", 0.0) or 0.0)
    orientation_drive = float(vision.get("orientation_drive", 0.0) or 0.0)
    vision_contrast = float(vision.get("vision_contrast", 0.0) or 0.0)

    focus_direction = float(focus.get("focus_direction", 0.0) or 0.0)
    focus_strength = float(focus.get("focus_strength", 0.0) or 0.0)
    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)
    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)

    focus_gain = 1.0 + (focus_strength * float(getattr(Config, "MCM_FOCUS_GAIN_WEIGHT", 0.30) or 0.30))
    target_gain = 1.0 + (target_lock * float(getattr(Config, "MCM_TARGET_LOCK_GAIN", 0.42) or 0.42))
    threat_gate = 1.0 - (focus_confidence * float(getattr(Config, "MCM_THREAT_FOCUS_DAMP", 0.22) or 0.22))
    noise_gate = max(0.35, 1.0 - (noise_damp * float(getattr(Config, "MCM_NOISE_DAMP_WEIGHT", 0.24) or 0.24)))

    filtered_target_map = target_map * target_gain * noise_gate
    filtered_optic_flow = optic_flow * focus_gain * noise_gate
    filtered_orientation_drive = orientation_drive + (focus_direction * 0.26)
    filtered_threat_map = threat_map * max(0.35, threat_gate)
    filtered_contrast = vision_contrast * max(0.25, 1.0 - (signal_relevance * 0.45))

    impulse = filtered_orientation_drive + (filtered_optic_flow * 0.35) - (filtered_contrast * 0.08)
    motivation_impulse = (filtered_target_map * 0.48) + (right_eye_field * 0.22) - (filtered_threat_map * 0.14)
    threat_excess = max(0.0, filtered_threat_map - 0.22)
    contrast_excess = max(0.0, filtered_contrast - 0.18)
    sensory_safety = max(0.0, signal_relevance - filtered_threat_map)
    risk_impulse = (
        -(threat_excess * 0.28)
        - (contrast_excess * 0.06)
        + min(0.0, left_eye_field) * 0.08
        + (sensory_safety * 0.035)
    )
    opportunity_bias = (filtered_target_map * 0.62) + max(0.0, filtered_optic_flow) * 0.22 + (signal_relevance * 0.10)

    if bool(pause_mode):
        impulse *= float(getattr(Config, "MCM_PAUSE_ORIENTATION_GAIN", 1.35) or 1.35)
        motivation_impulse *= float(getattr(Config, "MCM_PAUSE_MOTIVATION_DAMP", 0.55) or 0.55)
        risk_impulse *= float(getattr(Config, "MCM_PAUSE_RISK_GAIN", 1.20) or 1.20)
        opportunity_bias *= 0.50

    return {
        "vision": vision,
        "filtered_vision": {
            "left_eye_field": float(max(-2.5, min(2.5, left_eye_field))),
            "right_eye_field": float(max(-2.5, min(2.5, right_eye_field))),
            "optic_flow": float(max(-2.5, min(2.5, filtered_optic_flow))),
            "threat_map": float(max(0.0, min(2.5, filtered_threat_map))),
            "target_map": float(max(0.0, min(2.5, filtered_target_map))),
            "orientation_drive": float(max(-2.5, min(2.5, filtered_orientation_drive))),
            "vision_contrast": float(max(0.0, min(2.5, filtered_contrast))),
        },
        "focus": {
            "focus_direction": float(max(-2.5, min(2.5, focus_direction))),
            "focus_strength": float(max(0.0, min(2.5, focus_strength))),
            "focus_confidence": float(max(0.0, min(1.0, focus_confidence))),
            "target_lock": float(max(0.0, min(1.0, target_lock))),
            "noise_damp": float(max(0.0, min(2.5, noise_damp))),
            "signal_relevance": float(max(0.0, min(1.0, signal_relevance))),
        },
        "impulse": float(max(-2.5, min(2.5, impulse))),
        "motivation_impulse": float(max(-2.5, min(2.5, motivation_impulse))),
        "risk_impulse": float(max(-2.5, min(2.5, risk_impulse))),
        "opportunity_bias": float(max(-2.5, min(2.5, opportunity_bias))),
    }

def build_mcm_stimulus(candle_state, tension_state, pause_mode=False, bot=None, visual_market_state=None):

    vision = build_market_vision(candle_state, tension_state)
    visual_market_state = dict(visual_market_state or getattr(bot, "visual_market_state", {}) or {})
    market_hearing_state = dict(vision.get("market_hearing_state", {}) or {})
    market_hearing_state["action_permission"] = 0.0
    focus = build_focus_projection(
        candle_state,
        tension_state,
        vision,
        pause_mode=pause_mode,
        bot=bot,
    )
    filtered = apply_focus_filter(candle_state, tension_state, vision, focus, pause_mode=pause_mode)
    active_context_trace = _normalize_active_context_trace(getattr(bot, "active_context_trace", {}) or {})
    active_context_replay_impulse = _resolve_active_context_replay_impulse(active_context_trace)

    return {
        "mode": "market",
        "pause_mode": bool(pause_mode),
        "vision": dict(filtered.get("vision", {}) or {}),
        "visual_market_state": dict(visual_market_state or {}),
        "filtered_vision": dict(filtered.get("filtered_vision", {}) or {}),
        "market_hearing_state": dict(market_hearing_state or {}),
        "focus": dict(filtered.get("focus", {}) or {}),
        "impulse": float(filtered.get("impulse", 0.0) or 0.0),
        "motivation_impulse": float(filtered.get("motivation_impulse", 0.0) or 0.0),
        "risk_impulse": float(filtered.get("risk_impulse", 0.0) or 0.0),
        "opportunity_bias": float(filtered.get("opportunity_bias", 0.0) or 0.0),
        "active_context_trace": dict(active_context_trace or {}),
        "active_context_replay_impulse": float(active_context_replay_impulse),
    }

def build_neural_modulation(bot, stimulus):

    if bot is None:
        return {
            "inhibition_level": 0.0,
            "habituation_level": 0.0,
            "competition_bias": 0.0,
            "observation_mode": False,
            "signal_relevance": 0.0,
        }

    focus = dict((stimulus or {}).get("focus", {}) or {})
    filtered_vision = dict((stimulus or {}).get("filtered_vision", {}) or {})

    focus_direction = float(focus.get("focus_direction", 0.0) or 0.0)
    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    target_map = float(filtered_vision.get("target_map", 0.0) or 0.0)
    threat_map = float(filtered_vision.get("threat_map", 0.0) or 0.0)
    optic_flow = float(filtered_vision.get("optic_flow", 0.0) or 0.0)

    prev_inhibition = float(getattr(bot, "inhibition_level", 0.0) or 0.0)
    prev_habituation = float(getattr(bot, "habituation_level", 0.0) or 0.0)
    prev_competition = float(getattr(bot, "competition_bias", 0.0) or 0.0)
    prev_signal_relevance = float(getattr(bot, "last_signal_relevance", 0.0) or 0.0)

    repeated_signal = max(0.0, min(1.0, min(signal_relevance, prev_signal_relevance)))
    settling_bias = max(
        0.0,
        min(
            1.0,
            (focus_confidence * 0.26)
            + (signal_relevance * 0.24)
            + (target_lock * 0.14),
        ),
    )

    inhibition_raw = (noise_damp * 0.48) + (threat_map * 0.26) + max(0.0, abs(focus_direction) - focus_confidence) * 0.14
    habituation_raw = (repeated_signal * 0.58) + (target_lock * 0.16) + (max(0.0, target_map - abs(optic_flow)) * 0.10)
    competition_raw = (focus_direction * 0.62) + ((target_map - threat_map) * 0.18) + (optic_flow * 0.10)

    inhibition_level = max(0.0, min(1.0, (prev_inhibition * 0.68) + (inhibition_raw * float(getattr(Config, "MCM_INHIBITION_GAIN", 0.26) or 0.26))))
    habituation_level = max(0.0, min(1.0, (prev_habituation * 0.72) + (habituation_raw * float(getattr(Config, "MCM_HABITUATION_GAIN", 0.18) or 0.18))))
    competition_bias = max(-1.0, min(1.0, (prev_competition * 0.44) + (competition_raw * float(getattr(Config, "MCM_COMPETITION_GAIN", 0.22) or 0.22))))

    observation_pressure = max(
        0.0,
        (inhibition_level * 0.56)
        + (habituation_level * 0.44)
        - (settling_bias * 0.42),
    )
    observation_mode = bool(
        observation_pressure >= float(getattr(Config, "MCM_OBSERVE_THRESHOLD", 0.66) or 0.66)
        and focus_confidence < 0.70
        and signal_relevance < 0.76
    )

    bot.inhibition_level = float(inhibition_level)
    bot.habituation_level = float(habituation_level)
    bot.competition_bias = float(competition_bias)
    bot.observation_mode = bool(observation_mode)
    bot.last_signal_relevance = float(signal_relevance)

    return {
        "inhibition_level": float(inhibition_level),
        "habituation_level": float(habituation_level),
        "competition_bias": float(competition_bias),
        "observation_mode": bool(observation_mode),
        "signal_relevance": float(signal_relevance),
    }

def build_outcome_stimulus(outcome_reason, position=None):

    reason = str(outcome_reason or "").strip().lower()

    reward = 0.0
    motivation_impulse = 0.0
    risk_impulse = 0.0
    memory_boost = 0.0
    outcome_label = "neutral"

    if reason == "tp_hit":
        reward = float(getattr(Config, "MCM_TP_REWARD", 0.75) or 0.75)
        motivation_impulse = reward * 0.40
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.18) or 0.18)
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 1.0) or 1.0)
        outcome_label = "reward"
    elif reason == "sl_hit":
        reward = -float(getattr(Config, "MCM_SL_PENALTY", 0.85) or 0.85)
        motivation_impulse = reward * 0.28
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.18) or 0.18)
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 1.0) or 1.0)
        outcome_label = "aversive"
    elif reason == "cancel":
        reward = -float(getattr(Config, "MCM_CANCEL_PENALTY", 0.35) or 0.35)
        motivation_impulse = reward * 0.30
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.30) or 0.30) * 0.45
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 2.0) or 2.0) * 0.50
        outcome_label = "cancel"
    elif reason == "timeout":
        reward = -float(getattr(Config, "MCM_TIMEOUT_PENALTY", 0.45) or 0.45)
        motivation_impulse = reward * 0.35
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.30) or 0.30) * 0.60
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 2.0) or 2.0) * 0.60
        outcome_label = "timeout"
    elif reason == "reward_too_small":
        reward = -float(getattr(Config, "MCM_CANCEL_PENALTY", 0.35) or 0.35) * 0.85
        motivation_impulse = reward * 0.32
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.30) or 0.30) * 0.42
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 2.0) or 2.0) * 0.45
        outcome_label = "gate_reward"
    elif reason == "sl_distance_too_high":
        reward = -float(getattr(Config, "MCM_SL_PENALTY", 0.85) or 0.85) * 0.72
        motivation_impulse = reward * 0.26
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.30) or 0.30) * 0.70
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 2.0) or 2.0) * 0.55
        outcome_label = "gate_risk"
    elif reason == "rr_too_low":
        reward = -float(getattr(Config, "MCM_CANCEL_PENALTY", 0.35) or 0.35) * 1.05
        motivation_impulse = reward * 0.34
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.30) or 0.30) * 0.58
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 2.0) or 2.0) * 0.50
        outcome_label = "gate_rr"

    return {
        "mode": "outcome",
        "impulse": float(max(-2.5, min(2.5, reward))),
        "motivation_impulse": float(max(-2.5, min(2.5, motivation_impulse))),
        "risk_impulse": float(max(-2.5, min(2.5, risk_impulse))),
        "memory_boost": float(max(0.0, min(8.0, memory_boost))),
        "outcome_label": outcome_label,
    }

# --------------------------------------------------
def _snapshot_float_vector(values, digits=4):
    return _snapshot_float_vector_impl(values, digits=digits)

# --------------------------------------------------
def _snapshot_agent_field_points(field, limit=48, field_snapshot=None):
    return _snapshot_agent_field_points_impl(field, limit=limit, field_snapshot=field_snapshot)

#  --------------------------------------------------
def _snapshot_neuron_population(field, limit=24, field_snapshot=None):
    return _snapshot_neuron_population_impl(field, limit=limit, field_snapshot=field_snapshot)

# --------------------------------------------------
def _snapshot_areal_population(field, limit=16, field_snapshot=None):
    return _snapshot_areal_population_impl(field, limit=limit, field_snapshot=field_snapshot)

# --------------------------------------------------
def _snapshot_field_perception_state(field, field_snapshot=None):
    return _snapshot_field_perception_state_impl(field, field_snapshot=field_snapshot)

# --------------------------------------------------
def _snapshot_cluster_centers(clusters):
    return _snapshot_cluster_centers_impl(clusters)

# --------------------------------------------------
def _snapshot_cluster_links(center_vectors, limit=12):
    return _snapshot_cluster_links_impl(center_vectors, limit=limit)
# --------------------------------------------------
# MCM STEP
# --------------------------------------------------
def step_mcm_brain(brain, stimulus, mode="market"):

    profile_total_start = _mcm_profile_start()
    field = brain["field"]
    memory = brain["memory"]
    cluster = brain["cluster"]
    self_model = brain["self_model"]
    attractor = brain["attractor"]
    regulation = brain["regulation"]

    replay_scale = float(getattr(Config, "MCM_REPLAY_SCALE", 0.05) or 0.05)
    internal_cycles = int(getattr(Config, "MCM_INTERNAL_CYCLES", 3) or 3)

    profile_section_start = _mcm_profile_start()
    memory_replay_impulse = float(memory.replay_impulse(replay_scale=replay_scale) or 0.0)
    _mcm_profile_debug(
        "step_mcm_brain.memory_replay",
        profile_section_start,
        extra=f"agents={int(getattr(field, 'N', 0) or 0)}",
    )

    mode_value = str(mode or stimulus.get("mode", "market") or "market").strip().lower()
    is_outcome_mode = bool(mode_value == "outcome")
    active_context_trace = _normalize_active_context_trace(stimulus.get("active_context_trace", {}) or {})
    active_context_replay_impulse = float(
        stimulus.get(
            "active_context_replay_impulse",
            _resolve_active_context_replay_impulse(active_context_trace),
        ) or 0.0
    )
    replay_impulse = float(max(-0.35, min(0.35, memory_replay_impulse + active_context_replay_impulse)))

    raw_impulse = float(stimulus.get("impulse", 0.0) or 0.0)
    motivation_impulse = float(stimulus.get("motivation_impulse", 0.0) or 0.0)
    risk_impulse = float(stimulus.get("risk_impulse", 0.0) or 0.0)
    opportunity_bias = float(stimulus.get("opportunity_bias", 0.0) or 0.0)
    memory_boost = float(stimulus.get("memory_boost", 0.0) or 0.0)
    outcome_label = str(stimulus.get("outcome_label", "-") or "-")
    market_hearing_state = dict(stimulus.get("market_hearing_state", {}) or {})
    visual_market_state = dict(stimulus.get("visual_market_state", {}) or {})

    if is_outcome_mode:
        total_energy_impulse = (raw_impulse * 1.10) + (replay_impulse * 0.18)
        motivation_impulse = (motivation_impulse * 0.95)
        risk_impulse = (risk_impulse * 0.95) - (max(0.0, abs(raw_impulse) - 0.5) * 0.15)
    else:
        total_energy_impulse = (raw_impulse * 0.72) + (replay_impulse * 0.45)
        motivation_impulse = (motivation_impulse * 0.55) - (abs(replay_impulse) * 0.08)
        risk_impulse = (risk_impulse * 0.72) - (max(0.0, abs(raw_impulse) - 1.18) * 0.045)

    replay_cycles = max(0, internal_cycles - 1)
    profile_section_start = _mcm_profile_start()
    for _ in range(replay_cycles):
        field.step(replay_impulse * 0.35)
    _mcm_profile_debug(
        "step_mcm_brain.replay_field_step",
        profile_section_start,
        extra=f"cycles={int(replay_cycles)}|agents={int(getattr(field, 'N', 0) or 0)}",
    )

    field.energy *= 0.94
    field.velocity *= 0.88

    field.energy[:, 0] += total_energy_impulse
    if is_outcome_mode:
        field.energy[:, 1] += motivation_impulse
        field.energy[:, 2] += risk_impulse
    else:
        field.energy[:, 1] += motivation_impulse - (opportunity_bias * 0.06)
        field.energy[:, 2] += risk_impulse - (max(0.0, opportunity_bias - 0.62) * 0.025)

    field.energy = np.clip(field.energy, -2.2, 2.2)

    profile_section_start = _mcm_profile_start()
    field.step(
        total_energy_impulse * 0.55,
        context_trace=active_context_trace,
        market_hearing_state=market_hearing_state,
        visual_market_state=visual_market_state,
        return_snapshot=False,
    )
    _mcm_profile_debug(
        "step_mcm_brain.primary_field_step",
        profile_section_start,
        extra=f"agents={int(getattr(field, 'N', 0) or 0)}|dims={int(getattr(field, 'D', 0) or 0)}",
    )

    field_velocity_values = np.sqrt(np.einsum("ij,ij->i", field.velocity, field.velocity)) if len(field.velocity) > 0 else np.asarray([], dtype=float)
    field_mean_velocity_for_cluster = float(np.mean(field_velocity_values)) if len(field_velocity_values) > 0 else 0.0

    profile_section_start = _mcm_profile_start()
    clusters = cluster.detect(
        field.energy,
        force=is_outcome_mode,
        mean_velocity=field_mean_velocity_for_cluster,
    )
    _mcm_profile_debug(
        "step_mcm_brain.cluster_detect_pre_memory",
        profile_section_start,
        extra=f"clusters={int(len(clusters or []))}|agents={int(getattr(field, 'N', 0) or 0)}",
    )

    memory_store_clusters = []
    for item in clusters:
        strength = int(len(item))
        if mode_value == "outcome":
            strength += int(round(memory_boost))
        if strength >= 3:
            memory_store_clusters.append(item[:12])

    profile_section_start = _mcm_profile_start()
    memory.store(memory_store_clusters)
    _mcm_profile_debug(
        "step_mcm_brain.memory_store",
        profile_section_start,
        extra=f"clusters={int(len(memory_store_clusters or []))}",
    )

    profile_section_start = _mcm_profile_start()
    self_state = self_model.evaluate(field.energy)
    regulation.regulate(field)
    self_state = self_model.evaluate(field.energy)
    _mcm_profile_debug(
        "step_mcm_brain.self_regulation",
        profile_section_start,
        extra=f"self_state={self_state}|agents={int(getattr(field, 'N', 0) or 0)}",
    )

    mean_energy = float(np.mean(field.energy[:, 0]))
    mean_motivation = float(np.mean(field.energy[:, 1]))
    mean_risk = float(np.mean(field.energy[:, 2]))

    if self_state == "excited" and mean_energy > 1.35:
        field.energy[:, 0] *= 0.90
        field.energy[:, 1] *= 0.92

    if self_state == "stressed" and mean_risk < -0.85:
        field.energy[:, 0] *= 0.88
        field.energy[:, 1] *= 0.84

    strongest_memory = memory.strongest()
    selected_attractor = attractor.choose(strongest_memory, self_state)

    mean_energy = float(np.mean(field.energy[:, 0]))
    mean_motivation = float(np.mean(field.energy[:, 1]))
    mean_risk = float(np.mean(field.energy[:, 2]))
    field_velocity_values = np.sqrt(np.einsum("ij,ij->i", field.velocity, field.velocity)) if len(field.velocity) > 0 else np.asarray([], dtype=float)
    mean_velocity = float(np.mean(field_velocity_values)) if len(field_velocity_values) > 0 else 0.0

    profile_section_start = _mcm_profile_start()
    clusters = cluster.detect(
        field.energy,
        force=is_outcome_mode,
        mean_velocity=mean_velocity,
        advance_tick=False,
    )
    _mcm_profile_debug(
        "step_mcm_brain.cluster_detect_snapshot",
        profile_section_start,
        extra=f"clusters={int(len(clusters or []))}|agents={int(getattr(field, 'N', 0) or 0)}",
    )

    cluster_sizes = [int(len(cluster)) for cluster in list(clusters or []) if len(cluster) > 0]
    cluster_center_payload, cluster_center_vectors = _snapshot_cluster_centers(clusters)
    cluster_centers = [np.asarray(item, dtype=float) for item in list(cluster_center_vectors or [])]
    cluster_links = _snapshot_cluster_links(cluster_center_vectors)
    field_center = np.mean(field.energy, axis=0) if len(field.energy) > 0 else np.zeros(field.D, dtype=float)
    field_energy = np.asarray(getattr(field, "energy", []), dtype=float)

    cluster_mass_mean = 0.0
    cluster_mass_max = 0.0
    cluster_center_spread = 0.0
    cluster_separation = 0.0

    if cluster_sizes:
        cluster_mass_mean = float(np.mean(cluster_sizes) / max(1, int(field.N or 1)))
        cluster_mass_max = float(max(cluster_sizes) / max(1, int(field.N or 1)))

    if cluster_centers:
        cluster_center_spread = float(
            np.mean(
                [
                    np.linalg.norm(
                        np.asarray(center, dtype=float) - np.asarray(field_center, dtype=float)
                    )
                    for center in cluster_centers
                ]
            )
        )

    if len(cluster_centers) > 1:
        separation_values = []

        for i in range(len(cluster_centers)):
            for j in range(i + 1, len(cluster_centers)):
                separation_values.append(
                    float(
                        np.linalg.norm(
                            np.asarray(cluster_centers[i], dtype=float)
                            - np.asarray(cluster_centers[j], dtype=float)
                        )
                    )
                )

        if separation_values:
            cluster_separation = float(np.mean(separation_values))

    field_bounds = {
        "energy": {
            "min": float(round(float(np.min(field_energy[:, 0])) if len(field_energy) > 0 else 0.0, 4)),
            "max": float(round(float(np.max(field_energy[:, 0])) if len(field_energy) > 0 else 0.0, 4)),
        },
        "motivation": {
            "min": float(round(float(np.min(field_energy[:, 1])) if len(field_energy) > 1 else 0.0, 4)),
            "max": float(round(float(np.max(field_energy[:, 1])) if len(field_energy) > 1 else 0.0, 4)),
        },
        "risk": {
            "min": float(round(float(np.min(field_energy[:, 2])) if len(field_energy) > 2 else 0.0, 4)),
            "max": float(round(float(np.max(field_energy[:, 2])) if len(field_energy) > 2 else 0.0, 4)),
        },
    }
    profile_section_start = _mcm_profile_start()
    field_topology_layout_state = _snapshot_field_topology_layout(field, field_snapshot=None)
    field_agent_points = _snapshot_agent_field_points(field, field_snapshot=None)
    neuron_population_summary, neuron_population = _snapshot_neuron_population(field, field_snapshot=None)
    areal_population_summary, areal_population, areal_links = _snapshot_areal_population(field, field_snapshot=None)
    field_perception_state = _snapshot_field_perception_state(field, field_snapshot=None)
    auditory_neural_state = dict(getattr(field, "auditory_neural_state", {}) or {})
    visual_neural_state = dict(getattr(field, "visual_neural_state", {}) or {})
    field_topology_state = _build_field_topology_state({
        "cluster_count": int(len(clusters)),
        "field_cluster_links": list(cluster_links or []),
        "field_areal_count": int(areal_population_summary.get("areal_count", 0) or 0),
        "field_areal_links": list(areal_links or []),
        "field_areal_fragmentation": float(areal_population_summary.get("areal_fragmentation", 0.0) or 0.0),
        "field_areal_coherence_mean": float(areal_population_summary.get("areal_coherence_mean", 0.0) or 0.0),
        "field_areal_conflict_mean": float(areal_population_summary.get("areal_conflict_mean", 0.0) or 0.0),
    })
    _mcm_profile_debug(
        "step_mcm_brain.snapshot_field_read",
        profile_section_start,
        extra=f"neurons={int(neuron_population_summary.get('neuron_count', 0) or 0)}|areals={int(areal_population_summary.get('areal_count', 0) or 0)}",
    )

    cluster_topology = dict(getattr(cluster, "last_topology", {}) or {})
    cluster_center_drift = float(cluster_topology.get("cluster_center_drift", 0.0) or 0.0)
    cluster_count_drift = float(cluster_topology.get("cluster_count_drift", 0.0) or 0.0)
    field_velocity_trend = float(cluster_topology.get("field_velocity_trend", 0.0) or 0.0)
    reorganization_direction = str(cluster_topology.get("reorganization_direction", "stable") or "stable")

    snapshot = {
        "mode": mode_value,
        "outcome_label": outcome_label,
        "replay_impulse": float(replay_impulse),
        "memory_replay_impulse": float(memory_replay_impulse),
        "active_context_replay_impulse": float(active_context_replay_impulse),
        "active_context_trace": dict(active_context_trace or {}),
        "self_state": str(self_state),
        "attractor": str(selected_attractor),
        "strongest_memory": strongest_memory,
        "mean_energy": float(mean_energy),
        "mean_motivation": float(mean_motivation),
        "mean_risk": float(mean_risk),
        "mean_velocity": float(mean_velocity),
        "cluster_count": int(len(clusters)),
        "cluster_mass_mean": float(cluster_mass_mean),
        "cluster_mass_max": float(cluster_mass_max),
        "cluster_center_spread": float(cluster_center_spread),
        "cluster_separation": float(cluster_separation),
        "cluster_center_drift": float(cluster_center_drift),
        "cluster_count_drift": float(cluster_count_drift),
        "field_velocity_trend": float(field_velocity_trend),
        "reorganization_direction": str(reorganization_direction),
        "regulation_pressure": float(abs(mean_energy) * 0.85 + abs(mean_risk) * 0.95 + mean_velocity * 0.35),
        "field_center_vector": _snapshot_float_vector(field_center),
        "field_agent_points": list(field_agent_points or []),
        "field_cluster_centers": list(cluster_center_payload or []),
        "field_cluster_links": list(cluster_links or []),
        "field_projection_axes": ["energy", "motivation", "risk"],
        "field_projection_bounds": dict(field_bounds or {}),
        "field_topology_layout_state": dict(field_topology_layout_state or {}),
        "field_topology_rows": int(field_topology_layout_state.get("topology_rows", 0) or 0),
        "field_topology_cols": int(field_topology_layout_state.get("topology_cols", 0) or 0),
        "field_topology_position_count": int(field_topology_layout_state.get("topology_position_count", 0) or 0),
        "field_topology_neighbor_link_count": int(field_topology_layout_state.get("topology_neighbor_link_count", 0) or 0),
        "field_topology_neighbor_count_mean": float(field_topology_layout_state.get("topology_neighbor_count_mean", 0.0) or 0.0),
        "field_topology_neighbor_count_max": int(field_topology_layout_state.get("topology_neighbor_count_max", 0) or 0),
        "field_topology_positions": list(field_topology_layout_state.get("topology_positions", []) or []),
        "field_topology_links": list(field_topology_layout_state.get("topology_links", []) or []),
        "field_neuron_count": int(neuron_population_summary.get("neuron_count", 0) or 0),
        "field_neuron_activation_mean": float(neuron_population_summary.get("neuron_activation_mean", 0.0) or 0.0),
        "field_neuron_activation_max": float(neuron_population_summary.get("neuron_activation_max", 0.0) or 0.0),
        "field_neuron_stability_mean": float(neuron_population_summary.get("neuron_stability_mean", 0.0) or 0.0),
        "field_neuron_regulation_pressure_mean": float(neuron_population_summary.get("neuron_regulation_pressure_mean", 0.0) or 0.0),
        "field_neuron_memory_norm_mean": float(neuron_population_summary.get("neuron_memory_norm_mean", 0.0) or 0.0),
        "field_neuron_coupling_norm_mean": float(neuron_population_summary.get("neuron_coupling_norm_mean", 0.0) or 0.0),
        "field_neuron_regulation_force_norm_mean": float(neuron_population_summary.get("neuron_regulation_force_norm_mean", 0.0) or 0.0),
        "field_neuron_external_impulse_norm_mean": float(neuron_population_summary.get("neuron_external_impulse_norm_mean", 0.0) or 0.0),
        "field_neuron_auditory_impulse_norm_mean": float(neuron_population_summary.get("neuron_auditory_impulse_norm_mean", 0.0) or 0.0),
        "field_neuron_auditory_resonance_mean": float(neuron_population_summary.get("neuron_auditory_resonance_mean", 0.0) or 0.0),
        "field_neuron_auditory_aftertone_norm_mean": float(neuron_population_summary.get("neuron_auditory_aftertone_norm_mean", 0.0) or 0.0),
        "field_neuron_visual_impulse_norm_mean": float(neuron_population_summary.get("neuron_visual_impulse_norm_mean", 0.0) or 0.0),
        "field_neuron_visual_resonance_mean": float(neuron_population_summary.get("neuron_visual_resonance_mean", 0.0) or 0.0),
        "field_neuron_visual_afterimage_norm_mean": float(neuron_population_summary.get("neuron_visual_afterimage_norm_mean", 0.0) or 0.0),
        "field_neuron_context_memory_impulse_norm_mean": float(neuron_population_summary.get("neuron_context_memory_impulse_norm_mean", 0.0) or 0.0),
        "field_neuron_overload_mean": float(neuron_population_summary.get("neuron_overload_mean", 0.0) or 0.0),
        "field_neuron_recovery_tendency_mean": float(neuron_population_summary.get("neuron_recovery_tendency_mean", 0.0) or 0.0),
        "field_neuron_memory_resonance_mean": float(neuron_population_summary.get("neuron_memory_resonance_mean", 0.0) or 0.0),
        "field_neuron_context_reactivation_mean": float(neuron_population_summary.get("neuron_context_reactivation_mean", 0.0) or 0.0),
        "field_neuron_coupling_resonance_mean": float(neuron_population_summary.get("neuron_coupling_resonance_mean", 0.0) or 0.0),
        "field_neuron_receptivity_mean": float(neuron_population_summary.get("neuron_receptivity_mean", 0.0) or 0.0),
        "field_neuron_population": list(neuron_population or []),
        "field_areal_count": int(areal_population_summary.get("areal_count", 0) or 0),
        "field_areal_activation_mean": float(areal_population_summary.get("areal_activation_mean", 0.0) or 0.0),
        "field_areal_stability_mean": float(areal_population_summary.get("areal_stability_mean", 0.0) or 0.0),
        "field_areal_pressure_mean": float(areal_population_summary.get("areal_pressure_mean", 0.0) or 0.0),
        "field_areal_drift": float(areal_population_summary.get("areal_drift", 0.0) or 0.0),
        "field_areal_dominance": float(areal_population_summary.get("areal_dominance", 0.0) or 0.0),
        "field_areal_fragmentation": float(areal_population_summary.get("areal_fragmentation", 0.0) or 0.0),
        "field_areal_coherence_mean": float(areal_population_summary.get("areal_coherence_mean", 0.0) or 0.0),
        "field_areal_conflict_mean": float(areal_population_summary.get("areal_conflict_mean", 0.0) or 0.0),
        "field_areal_topology_density_mean": float(areal_population_summary.get("areal_topology_density_mean", 0.0) or 0.0),
        "field_areal_topology_span_mean": float(areal_population_summary.get("areal_topology_span_mean", 0.0) or 0.0),
        "field_areal_topology_boundary_mean": float(areal_population_summary.get("areal_topology_boundary_mean", 0.0) or 0.0),
        "field_areal_states": list(areal_population or []),
        "field_areal_links": list(areal_links or []),
        "field_perception_state": dict(field_perception_state or {}),
        "field_activity_island_count": int(field_perception_state.get("activity_island_count", 0) or 0),
        "field_activity_island_mass_mean": float(field_perception_state.get("activity_island_mass_mean", 0.0) or 0.0),
        "field_activity_island_mass_max": float(field_perception_state.get("activity_island_mass_max", 0.0) or 0.0),
        "field_activity_island_activation_mean": float(field_perception_state.get("activity_island_activation_mean", 0.0) or 0.0),
        "field_activity_island_pressure_mean": float(field_perception_state.get("activity_island_pressure_mean", 0.0) or 0.0),
        "field_activity_island_coherence_mean": float(field_perception_state.get("activity_island_coherence_mean", 0.0) or 0.0),
        "field_activity_island_context_reactivation_mean": float(field_perception_state.get("activity_island_context_reactivation_mean", 0.0) or 0.0),
        "field_activity_island_spread": float(field_perception_state.get("activity_island_spread", 0.0) or 0.0),
        "field_perception_focus": float(field_perception_state.get("field_perception_focus", 0.0) or 0.0),
        "field_perception_clarity": float(field_perception_state.get("field_perception_clarity", 0.0) or 0.0),
        "field_perception_stability": float(field_perception_state.get("field_perception_stability", 0.0) or 0.0),
        "field_perception_fragmentation": float(field_perception_state.get("field_perception_fragmentation", 0.0) or 0.0),
        "field_perception_strain": float(field_perception_state.get("field_perception_strain", 0.0) or 0.0),
        "dominant_activity_island_id": str(field_perception_state.get("dominant_activity_island_id", "-") or "-"),
        "field_perception_label": str(field_perception_state.get("field_perception_label", "quiet_field") or "quiet_field"),
        "field_activity_islands": list(field_perception_state.get("activity_islands", []) or []),
        "auditory_neural_state": dict(auditory_neural_state or {}),
        "auditory_neural_resonance_mean": float(auditory_neural_state.get("resonance_mean", 0.0) or 0.0),
        "auditory_neural_aftertone_mean": float(auditory_neural_state.get("aftertone_mean", 0.0) or 0.0),
        "auditory_neural_action_permission": 0.0,
        "visual_neural_state": dict(visual_neural_state or {}),
        "visual_neural_resonance_mean": float(visual_neural_state.get("resonance_mean", 0.0) or 0.0),
        "visual_neural_afterimage_mean": float(visual_neural_state.get("afterimage_mean", 0.0) or 0.0),
        "visual_neural_action_permission": 0.0,
        "field_topology_state": dict(field_topology_state or {}),
    }

    _mcm_state_debug(
        "MCM_STATE | "
        f"mode={mode_value} "
        f"impulse={total_energy_impulse:.4f} "
        f"motivation={motivation_impulse:.4f} "
        f"risk={risk_impulse:.4f} "
        f"replay={replay_impulse:.4f} "
        f"self_state={self_state} "
        f"attractor={selected_attractor} "
        f"mean_energy={mean_energy:.4f} "
        f"mean_motivation={mean_motivation:.4f} "
        f"mean_risk={mean_risk:.4f} "
        f"mean_velocity={mean_velocity:.4f} "
        f"clusters={len(clusters)} "
        f"memory_center={float(strongest_memory.get('center', 0.0)) if strongest_memory else 0.0:.4f} "
        f"memory_strength={int(strongest_memory.get('strength', 0)) if strongest_memory else 0}"
    )

    _mcm_profile_debug(
        "step_mcm_brain.total",
        profile_total_start,
        extra=f"mode={mode_value}|clusters={int(len(clusters or []))}|agents={int(getattr(field, 'N', 0) or 0)}",
    )

    return snapshot

# --------------------------------------------------
# OUTCOME API
# --------------------------------------------------
def apply_outcome_stimulus(bot, outcome_reason, position=None):

    if bot is None:
        return None

    if not bool(getattr(Config, "MCM_ENABLED", True)):
        return None

    if getattr(bot, "mcm_brain", None) is None:
        bot.mcm_brain = create_mcm_brain()

    before_snapshot = dict(getattr(bot, "mcm_snapshot", {}) or {})
    before_memory = before_snapshot.get("strongest_memory") or {}

    stimulus = build_outcome_stimulus(outcome_reason, position)
    snapshot = step_mcm_brain(bot.mcm_brain, stimulus, mode="outcome")

    bot.mcm_last_state = dict(snapshot)
    bot.mcm_last_action = str(snapshot.get("self_state", "stable"))
    bot.mcm_last_attractor = str(snapshot.get("attractor", "neutral"))
    bot.mcm_snapshot = dict(snapshot)

    reason = str(outcome_reason or "").strip().lower()

    if reason == "tp_hit":
        bot.focus_confidence = float(min(1.0, (float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.55) + 0.35))
        bot.target_lock = float(min(1.0, (float(getattr(bot, "target_lock", 0.0) or 0.0) * 0.60) + 0.30))
        bot.target_drift = float((float(getattr(bot, "target_drift", 0.0) or 0.0)) * 0.45)

    elif reason == "sl_hit":
        bot.focus_confidence = float(max(0.0, float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.55))
        bot.target_lock = float(max(0.0, float(getattr(bot, "target_lock", 0.0) or 0.0) * 0.45))
        bot.target_drift = float((float(getattr(bot, "target_drift", 0.0) or 0.0)) * 1.15)

    elif reason in ("cancel", "timeout"):
        bot.focus_confidence = float(max(0.0, float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.72))
        bot.target_lock = float(max(0.0, float(getattr(bot, "target_lock", 0.0) or 0.0) * 0.68))

    elif reason in ("reward_too_small", "rr_too_low", "sl_distance_too_high"):
        bot.focus_confidence = float(max(0.0, float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.64))
        bot.target_lock = float(max(0.0, float(getattr(bot, "target_lock", 0.0) or 0.0) * 0.58))
        bot.target_drift = float((float(getattr(bot, "target_drift", 0.0) or 0.0)) * 1.08)

    experience_state = update_experience_state(bot, reason)
    outcome_decomposition = build_outcome_decomposition(bot, reason, position, experience_state)
    form_development_state = _update_form_symbol_development_from_outcome(
        bot,
        reason,
        position=position,
        outcome_decomposition=outcome_decomposition,
    )
    outcome_decomposition = dict(outcome_decomposition or {})
    for key, value in dict(form_development_state or {}).items():
        outcome_decomposition[key] = value
    bot.last_form_symbol_development_state = dict(form_development_state or {})
    experience_packet_feedback = build_experience_packet_feedback(
        bot,
        reason,
        position=position,
        outcome_decomposition=outcome_decomposition,
        experience_state=experience_state,
        form_development_state=form_development_state,
    )
    bot.last_experience_packet_feedback = dict(experience_packet_feedback or {})
    outcome_decomposition["experience_packet_feedback"] = dict(experience_packet_feedback or {})
    for key, value in dict(experience_packet_feedback or {}).items():
        outcome_decomposition[key] = value
    bot.last_outcome_decomposition = dict(outcome_decomposition or {})

    commit_pending_learning_context(
        bot,
        outcome=reason,
    )

    signature_key = str(getattr(bot, "last_signature_key", "") or "").strip()

    after_memory = snapshot.get("strongest_memory") or {}

    signature_score = 0.0
    if signature_key and isinstance(getattr(bot, "signature_memory", None), dict):
        signature_score = float((bot.signature_memory.get(signature_key) or {}).get("score", 0.0) or 0.0)

    _mcm_outcome_debug(
        "MCM_OUTCOME | "
        f"reason={str(outcome_reason or '-')} "
        f"reward_impulse={float(stimulus.get('impulse', 0.0) or 0.0):.4f} "
        f"motivation_impulse={float(stimulus.get('motivation_impulse', 0.0) or 0.0):.4f} "
        f"risk_impulse={float(stimulus.get('risk_impulse', 0.0) or 0.0):.4f} "
        f"self_state_before={str(before_snapshot.get('self_state', '-'))} "
        f"self_state_after={str(snapshot.get('self_state', '-'))} "
        f"attractor_before={str(before_snapshot.get('attractor', '-'))} "
        f"attractor_after={str(snapshot.get('attractor', '-'))} "
        f"memory_center_before={float(before_memory.get('center', 0.0) or 0.0):.4f} "
        f"memory_center_after={float(after_memory.get('center', 0.0) or 0.0):.4f} "
        f"memory_strength_before={int(before_memory.get('strength', 0) or 0)} "
        f"memory_strength_after={int(after_memory.get('strength', 0) or 0)} "
        f"focus_confidence={float(getattr(bot, 'focus_confidence', 0.0) or 0.0):.4f} "
        f"target_lock={float(getattr(bot, 'target_lock', 0.0) or 0.0):.4f} "
        f"target_drift={float(getattr(bot, 'target_drift', 0.0) or 0.0):.4f} "
        f"entry_expectation={float((experience_state or {}).get('entry_expectation', 0.0) or 0.0):.4f} "
        f"target_expectation={float((experience_state or {}).get('target_expectation', 0.0) or 0.0):.4f} "
        f"approach_pressure={float((experience_state or {}).get('approach_pressure', 0.0) or 0.0):.4f} "
        f"pressure_release={float((experience_state or {}).get('pressure_release', 0.0) or 0.0):.4f} "
        f"experience_regulation={float((experience_state or {}).get('experience_regulation', 0.0) or 0.0):.4f} "
        f"reflection_maturity={float((experience_state or {}).get('reflection_maturity', 0.0) or 0.0):.4f} "
        f"signature_key={signature_key or '-'} "
        f"signature_score={signature_score:.4f} "
        f"outcome_decomposition={dict(outcome_decomposition or {})} "
        f"form_development={dict(form_development_state or {})} "
        f"experience_packet_feedback={dict(experience_packet_feedback or {})}"
    )

    return snapshot

from core.perception import (
    build_conscious_perception_state,
    build_outer_visual_perception_state,
    build_perception_state,
    build_processing_state,
    build_world_state,
)

def build_inner_field_perception_state(snapshot, bot=None):
    snap = dict(snapshot or {})
    prior_regulation = float(getattr(bot, "experience_regulation", 0.0) or 0.0) if bot is not None else 0.0
    field_topology_state = _build_field_topology_state(snap)
    inner_field_state = {
        "field_mean_energy": float(snap.get("mean_energy", 0.0) or 0.0),
        "field_mean_motivation": float(snap.get("mean_motivation", 0.0) or 0.0),
        "field_mean_risk": float(snap.get("mean_risk", 0.0) or 0.0),
        "field_mean_velocity": float(snap.get("mean_velocity", 0.0) or 0.0),
        "field_cluster_count": int(snap.get("cluster_count", 0) or 0),
        "field_cluster_mass_mean": float(snap.get("cluster_mass_mean", 0.0) or 0.0),
        "field_cluster_mass_max": float(snap.get("cluster_mass_max", 0.0) or 0.0),
        "field_cluster_center_spread": float(snap.get("cluster_center_spread", 0.0) or 0.0),
        "field_cluster_separation": float(snap.get("cluster_separation", 0.0) or 0.0),
        "field_cluster_center_drift": float(snap.get("cluster_center_drift", 0.0) or 0.0),
        "field_cluster_count_drift": float(snap.get("cluster_count_drift", 0.0) or 0.0),
        "field_velocity_trend": float(snap.get("field_velocity_trend", 0.0) or 0.0),
        "field_reorganization_direction": str(snap.get("reorganization_direction", "stable") or "stable"),
        "field_regulation_pressure": float(snap.get("regulation_pressure", 0.0) or 0.0),
        "field_center_vector": list(snap.get("field_center_vector", []) or []),
        "field_agent_points": [dict(item or {}) for item in list(snap.get("field_agent_points", []) or []) if isinstance(item, dict)],
        "field_cluster_centers": [dict(item or {}) for item in list(snap.get("field_cluster_centers", []) or []) if isinstance(item, dict)],
        "field_cluster_links": [dict(item or {}) for item in list(snap.get("field_cluster_links", []) or []) if isinstance(item, dict)],
        "field_projection_axes": list(snap.get("field_projection_axes", []) or []),
        "field_projection_bounds": dict(snap.get("field_projection_bounds", {}) or {}),
        "field_topology_layout_state": dict(snap.get("field_topology_layout_state", {}) or {}),
        "field_topology_rows": int(snap.get("field_topology_rows", 0) or 0),
        "field_topology_cols": int(snap.get("field_topology_cols", 0) or 0),
        "field_topology_position_count": int(snap.get("field_topology_position_count", 0) or 0),
        "field_topology_neighbor_link_count": int(snap.get("field_topology_neighbor_link_count", 0) or 0),
        "field_topology_neighbor_count_mean": float(snap.get("field_topology_neighbor_count_mean", 0.0) or 0.0),
        "field_topology_neighbor_count_max": int(snap.get("field_topology_neighbor_count_max", 0) or 0),
        "field_topology_positions": [dict(item or {}) for item in list(snap.get("field_topology_positions", []) or []) if isinstance(item, dict)],
        "field_topology_links": [dict(item or {}) for item in list(snap.get("field_topology_links", []) or []) if isinstance(item, dict)],
        "field_neuron_count": int(snap.get("field_neuron_count", 0) or 0),
        "field_neuron_activation_mean": float(snap.get("field_neuron_activation_mean", 0.0) or 0.0),
        "field_neuron_activation_max": float(snap.get("field_neuron_activation_max", 0.0) or 0.0),
        "field_neuron_stability_mean": float(snap.get("field_neuron_stability_mean", 0.0) or 0.0),
        "field_neuron_regulation_pressure_mean": float(snap.get("field_neuron_regulation_pressure_mean", 0.0) or 0.0),
        "field_neuron_memory_norm_mean": float(snap.get("field_neuron_memory_norm_mean", 0.0) or 0.0),
        "field_neuron_coupling_norm_mean": float(snap.get("field_neuron_coupling_norm_mean", 0.0) or 0.0),
        "field_neuron_regulation_force_norm_mean": float(snap.get("field_neuron_regulation_force_norm_mean", 0.0) or 0.0),
        "field_neuron_external_impulse_norm_mean": float(snap.get("field_neuron_external_impulse_norm_mean", 0.0) or 0.0),
        "field_neuron_auditory_impulse_norm_mean": float(snap.get("field_neuron_auditory_impulse_norm_mean", 0.0) or 0.0),
        "field_neuron_auditory_resonance_mean": float(snap.get("field_neuron_auditory_resonance_mean", 0.0) or 0.0),
        "field_neuron_auditory_aftertone_norm_mean": float(snap.get("field_neuron_auditory_aftertone_norm_mean", 0.0) or 0.0),
        "field_neuron_visual_impulse_norm_mean": float(snap.get("field_neuron_visual_impulse_norm_mean", 0.0) or 0.0),
        "field_neuron_visual_resonance_mean": float(snap.get("field_neuron_visual_resonance_mean", 0.0) or 0.0),
        "field_neuron_visual_afterimage_norm_mean": float(snap.get("field_neuron_visual_afterimage_norm_mean", 0.0) or 0.0),
        "field_neuron_context_memory_impulse_norm_mean": float(snap.get("field_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0),
        "field_neuron_overload_mean": float(snap.get("field_neuron_overload_mean", 0.0) or 0.0),
        "field_neuron_recovery_tendency_mean": float(snap.get("field_neuron_recovery_tendency_mean", 0.0) or 0.0),
        "field_neuron_memory_resonance_mean": float(snap.get("field_neuron_memory_resonance_mean", 0.0) or 0.0),
        "field_neuron_context_reactivation_mean": float(snap.get("field_neuron_context_reactivation_mean", 0.0) or 0.0),
        "field_neuron_coupling_resonance_mean": float(snap.get("field_neuron_coupling_resonance_mean", 0.0) or 0.0),
        "field_neuron_receptivity_mean": float(snap.get("field_neuron_receptivity_mean", 0.0) or 0.0),
        "field_neuron_population": [dict(item or {}) for item in list(snap.get("field_neuron_population", []) or []) if isinstance(item, dict)],
        "field_areal_count": int(snap.get("field_areal_count", 0) or 0),
        "field_areal_activation_mean": float(snap.get("field_areal_activation_mean", 0.0) or 0.0),
        "field_areal_stability_mean": float(snap.get("field_areal_stability_mean", 0.0) or 0.0),
        "field_areal_pressure_mean": float(snap.get("field_areal_pressure_mean", 0.0) or 0.0),
        "field_areal_drift": float(snap.get("field_areal_drift", 0.0) or 0.0),
        "field_areal_dominance": float(snap.get("field_areal_dominance", 0.0) or 0.0),
        "field_areal_fragmentation": float(snap.get("field_areal_fragmentation", 0.0) or 0.0),
        "field_areal_coherence_mean": float(snap.get("field_areal_coherence_mean", 0.0) or 0.0),
        "field_areal_conflict_mean": float(snap.get("field_areal_conflict_mean", 0.0) or 0.0),
        "field_areal_topology_density_mean": float(snap.get("field_areal_topology_density_mean", 0.0) or 0.0),
        "field_areal_topology_span_mean": float(snap.get("field_areal_topology_span_mean", 0.0) or 0.0),
        "field_areal_topology_boundary_mean": float(snap.get("field_areal_topology_boundary_mean", 0.0) or 0.0),
        "field_areal_states": [dict(item or {}) for item in list(snap.get("field_areal_states", []) or []) if isinstance(item, dict)],
        "field_areal_links": [dict(item or {}) for item in list(snap.get("field_areal_links", []) or []) if isinstance(item, dict)],
        "field_perception_state": dict(snap.get("field_perception_state", {}) or {}),
        "field_activity_island_count": int(snap.get("field_activity_island_count", 0) or 0),
        "field_activity_island_mass_mean": float(snap.get("field_activity_island_mass_mean", 0.0) or 0.0),
        "field_activity_island_mass_max": float(snap.get("field_activity_island_mass_max", 0.0) or 0.0),
        "field_activity_island_activation_mean": float(snap.get("field_activity_island_activation_mean", 0.0) or 0.0),
        "field_activity_island_pressure_mean": float(snap.get("field_activity_island_pressure_mean", 0.0) or 0.0),
        "field_activity_island_coherence_mean": float(snap.get("field_activity_island_coherence_mean", 0.0) or 0.0),
        "field_activity_island_context_reactivation_mean": float(snap.get("field_activity_island_context_reactivation_mean", 0.0) or 0.0),
        "field_activity_island_spread": float(snap.get("field_activity_island_spread", 0.0) or 0.0),
        "field_perception_label": str(snap.get("field_perception_label", "quiet_field") or "quiet_field"),
        "field_activity_islands": [dict(item or {}) for item in list(snap.get("field_activity_islands", []) or []) if isinstance(item, dict)],
        "field_topology_state": dict(field_topology_state or {}),
        "field_topology_cluster_link_count": int(field_topology_state.get("cluster_link_count", 0) or 0),
        "field_topology_areal_link_count": int(field_topology_state.get("areal_link_count", 0) or 0),
        "field_topology_link_density": float(field_topology_state.get("link_density", 0.0) or 0.0),
        "field_topology_distance_mean": float(field_topology_state.get("topology_distance_mean", 0.0) or 0.0),
        "field_topology_coherence": float(field_topology_state.get("topology_coherence", 0.0) or 0.0),
        "field_topology_tension": float(field_topology_state.get("topology_tension", 0.0) or 0.0),
        "field_topology_state_label": str(field_topology_state.get("topology_state_label", "sparse_topology") or "sparse_topology"),
        "self_state": str(snap.get("self_state", "stable") or "stable"),
        "attractor": str(snap.get("attractor", "neutral") or "neutral"),
        "prior_experience_regulation": float(prior_regulation),
    }

    neural_felt_state = _build_neural_felt_state(inner_field_state)
    inner_field_state["neural_felt_state"] = dict(neural_felt_state or {})
    inner_field_state["neural_felt_bearing"] = float(neural_felt_state.get("neural_felt_bearing", 0.0) or 0.0)
    inner_field_state["neural_felt_pressure"] = float(neural_felt_state.get("neural_felt_pressure", 0.0) or 0.0)
    inner_field_state["neural_felt_memory_resonance"] = float(neural_felt_state.get("neural_felt_memory_resonance", 0.0) or 0.0)
    inner_field_state["neural_felt_context_reactivation"] = float(neural_felt_state.get("neural_felt_context_reactivation", 0.0) or 0.0)
    inner_field_state["neural_felt_overload"] = float(neural_felt_state.get("neural_felt_overload", 0.0) or 0.0)
    inner_field_state["neural_felt_recovery_tendency"] = float(neural_felt_state.get("neural_felt_recovery_tendency", 0.0) or 0.0)
    inner_field_state["neural_felt_coupling_resonance"] = float(neural_felt_state.get("neural_felt_coupling_resonance", 0.0) or 0.0)
    inner_field_state["neural_felt_receptivity"] = float(neural_felt_state.get("neural_felt_receptivity", 0.0) or 0.0)
    inner_field_state["neural_felt_label"] = str(neural_felt_state.get("neural_felt_label", "quiet_neural_felt") or "quiet_neural_felt")

    inner_field_history_state = _update_inner_field_history(inner_field_state, bot=bot)
    inner_field_state["inner_field_history_state"] = dict(inner_field_history_state or {})
    inner_field_state["inner_field_history_length"] = int(inner_field_history_state.get("inner_field_history_length", 0) or 0)
    inner_field_state["inner_field_pressure_trend"] = float(inner_field_history_state.get("inner_field_pressure_trend", 0.0) or 0.0)
    inner_field_state["inner_field_bearing_trend"] = float(inner_field_history_state.get("inner_field_bearing_trend", 0.0) or 0.0)
    inner_field_state["inner_field_topology_tension_trend"] = float(inner_field_history_state.get("inner_field_topology_tension_trend", 0.0) or 0.0)
    inner_field_state["inner_field_memory_resonance_trend"] = float(inner_field_history_state.get("inner_field_memory_resonance_trend", 0.0) or 0.0)
    inner_field_state["inner_field_history_label"] = str(inner_field_history_state.get("inner_field_history_label", "stable_field_trace") or "stable_field_trace")
    return dict(inner_field_state or {})

def build_outcome_decomposition(bot, outcome_reason, position=None, experience_state=None):
    reason = str(outcome_reason or "").strip().lower()
    state = dict(experience_state or {})

    perception_quality = float(max(0.0, min(
        1.0,
        0.52
        + (float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.22)
        - (float(getattr(bot, "last_signal_relevance", 0.0) or 0.0) * 0.10),
    )))
    felt_quality = float(max(0.0, min(
        1.0,
        0.50
        + (float(state.get("experience_regulation", 0.0) or 0.0) * 0.20)
        + (float(state.get("reflection_maturity", 0.0) or 0.0) * 0.12),
    )))
    thought_quality = float(max(0.0, min(
        1.0,
        0.50
        + (float(state.get("reflection_maturity", 0.0) or 0.0) * 0.22)
        + (float(state.get("load_bearing_capacity", 0.0) or 0.0) * 0.12),
    )))

    plan_quality = 0.50
    execution_quality = 0.50
    risk_fit_quality = 0.50

    if reason == "tp_hit":
        plan_quality += 0.18
        execution_quality += 0.18
        risk_fit_quality += 0.12
    elif reason == "sl_hit":
        plan_quality -= 0.16
        execution_quality -= 0.12
        risk_fit_quality -= 0.18
    elif reason in ("cancel", "timeout"):
        execution_quality -= 0.15
        plan_quality -= 0.08
    elif reason == "reward_too_small":
        plan_quality -= 0.18
    elif reason == "rr_too_low":
        plan_quality -= 0.16
        risk_fit_quality -= 0.12
    elif reason == "sl_distance_too_high":
        risk_fit_quality -= 0.20
        plan_quality -= 0.10

    if isinstance(position, dict):
        entry_price = abs(float(position.get("entry", 0.0) or 0.0))
        risk = abs(float(position.get("entry", 0.0) or 0.0) - float(position.get("sl", 0.0) or 0.0))
        if risk > 0.0:
            risk_fit_quality = float(max(0.0, min(1.0, risk_fit_quality - min(0.18, risk * 2.5))))
        risk_width_pressure = float(max(0.0, min(1.0, (risk / max(entry_price, 1e-9)) * 82.0))) if entry_price > 0.0 else 0.0
        if reason == "sl_hit" and risk_width_pressure > 0.0:
            plan_quality = float(max(0.0, min(1.0, plan_quality - (risk_width_pressure * 0.09))))
            execution_quality = float(max(0.0, min(1.0, execution_quality - (risk_width_pressure * 0.05))))
            risk_fit_quality = float(max(0.0, min(1.0, risk_fit_quality - (risk_width_pressure * 0.10))))
    else:
        risk_width_pressure = 0.0

    attempt_density = float(state.get("attempt_density", 0.0) or 0.0)
    overtrade_pressure = float(state.get("overtrade_pressure", 0.0) or 0.0)
    context_quality = float(state.get("context_quality", 0.0) or 0.0)

    plan_quality = float(max(0.0, min(1.0, plan_quality - (overtrade_pressure * 0.10) + (context_quality * 0.08))))
    execution_quality = float(max(0.0, min(1.0, execution_quality - (attempt_density * 0.08) - (overtrade_pressure * 0.10) + (context_quality * 0.10))))
    felt_quality = float(max(0.0, min(1.0, felt_quality - (overtrade_pressure * 0.12) + (context_quality * 0.10))))
    thought_quality = float(max(0.0, min(1.0, thought_quality - (attempt_density * 0.06) + (context_quality * 0.08))))

    return {
        "perception_quality": float(max(0.0, min(1.0, perception_quality))),
        "felt_quality": float(max(0.0, min(1.0, felt_quality))),
        "thought_quality": float(max(0.0, min(1.0, thought_quality))),
        "plan_quality": float(max(0.0, min(1.0, plan_quality))),
        "execution_quality": float(max(0.0, min(1.0, execution_quality))),
        "risk_fit_quality": float(max(0.0, min(1.0, risk_fit_quality))),
        "attempt_density": float(attempt_density),
        "overtrade_pressure": float(overtrade_pressure),
        "context_quality": float(context_quality),
        "risk_width_pressure": float(risk_width_pressure),
        "reason": str(reason or "-"),
    }

def build_experience_packet_feedback(
    bot,
    outcome_reason,
    position=None,
    outcome_decomposition=None,
    experience_state=None,
    form_development_state=None,
):
    reason = str(outcome_reason or "").strip().lower()
    outcome = dict(outcome_decomposition or {})
    experience = dict(experience_state or {})
    form_development = dict(form_development_state or {})
    position_state = dict(position or {}) if isinstance(position, dict) else {}
    meta = dict(position_state.get("meta", {}) or {}) if isinstance(position_state.get("meta", {}), dict) else {}
    meta_regulation = dict(meta.get("meta_regulation_state", {}) or {}) if isinstance(meta.get("meta_regulation_state", {}), dict) else {}
    if not meta_regulation and bot is not None:
        meta_regulation = dict(getattr(bot, "meta_regulation_state", {}) or {})
    neurochemical = dict(meta_regulation.get("neurochemical_state", {}) or {}) if isinstance(meta_regulation.get("neurochemical_state", {}), dict) else {}
    if not neurochemical and bot is not None:
        neurochemical = dict(getattr(bot, "neurochemical_state", {}) or {})
    bearing_context = dict(meta.get("bearing_context", {}) or {}) if isinstance(meta.get("bearing_context", {}), dict) else {}
    form_state = _extract_outcome_form_symbol_state(bot, position=position)

    def _b01(value, default=0.0):
        try:
            return _clip01(value)
        except Exception:
            return float(default)

    perception_quality = _b01(outcome.get("perception_quality", 0.50), default=0.50)
    felt_quality = _b01(outcome.get("felt_quality", 0.50), default=0.50)
    thought_quality = _b01(outcome.get("thought_quality", 0.50), default=0.50)
    plan_quality = _b01(outcome.get("plan_quality", 0.50), default=0.50)
    execution_quality = _b01(outcome.get("execution_quality", 0.50), default=0.50)
    risk_fit_quality = _b01(outcome.get("risk_fit_quality", 0.50), default=0.50)
    context_quality = _b01(outcome.get("context_quality", 0.0))
    attempt_density = _b01(outcome.get("attempt_density", 0.0))
    overtrade_pressure = _b01(outcome.get("overtrade_pressure", 0.0))
    risk_width_pressure = _b01(outcome.get("risk_width_pressure", 0.0))

    structure_quality = _b01(bearing_context.get("structure_quality", form_state.get("form_symbol_bearing", 0.0)))
    transfer_bearing = _b01(meta_regulation.get("transfer_bearing", 0.0))
    structure_action_bearing = _b01(meta_regulation.get("structure_action_bearing", 0.0))
    field_bearing_support = _b01(meta_regulation.get("field_bearing_support", meta_regulation.get("field_action_support", 0.0)))
    interpretation_quality = _b01(meta_regulation.get("interpretation_quality", perception_quality), default=perception_quality)
    load_bearing_capacity = _b01(experience.get("load_bearing_capacity", meta_regulation.get("load_bearing_capacity", 0.0)))
    reflection_maturity = _b01(experience.get("reflection_maturity", 0.0))
    experience_regulation = _b01(experience.get("experience_regulation", 0.0))

    perceptual_distance = _b01(meta_regulation.get("perceptual_distance", 0.0))
    object_contact_depth = _b01(meta_regulation.get("object_contact_depth", 0.0))
    field_attachment = _b01(meta_regulation.get("field_attachment", 0.0))
    release_capacity = _b01(meta_regulation.get("release_capacity", 0.0))
    inner_outer_alignment = _b01(meta_regulation.get("inner_outer_alignment", 0.0))
    selective_attention = _b01(meta_regulation.get("selective_attention", 0.0))
    diffuse_open_development_pressure = _b01(meta_regulation.get("diffuse_open_development_pressure", 0.0))
    action_clearance = _b01(meta_regulation.get("action_clearance", 0.0))
    action_inhibition = _b01(meta_regulation.get("action_inhibition", 0.0))
    regulated_courage = _b01(meta_regulation.get("regulated_courage", 0.0))
    curiosity_tone = _b01(meta_regulation.get("curiosity_tone", 0.0))
    fatigue_tone = _b01(meta_regulation.get("fatigue_tone", 0.0))
    pressure_release = _b01(experience.get("pressure_release", 0.0))
    emotional_decoupling = _b01(neurochemical.get("emotional_decoupling", meta_regulation.get("emotional_decoupling", 0.0)))

    form_process_quality = _b01(form_development.get("process_quality", 0.0))
    form_structural_support = _b01(form_development.get("structural_support", 0.0))
    form_action_affinity = _b01(form_development.get("symbol_action_affinity", form_state.get("form_symbol_action_trust", 0.0)))
    form_learning_trust = _b01(form_state.get("form_symbol_learning_trust", 0.0))
    form_novelty = _b01(form_state.get("form_symbol_novelty", 0.0))

    process_core = _b01(
        (perception_quality * 0.16)
        + (felt_quality * 0.14)
        + (thought_quality * 0.16)
        + (plan_quality * 0.22)
        + (execution_quality * 0.17)
        + (risk_fit_quality * 0.15),
        default=0.50,
    )
    packet_bearing_quality = _b01(
        (structure_quality * 0.24)
        + (structure_action_bearing * 0.16)
        + (field_bearing_support * 0.14)
        + (transfer_bearing * 0.12)
        + (interpretation_quality * 0.12)
        + (context_quality * 0.10)
        + (load_bearing_capacity * 0.08)
        + (form_structural_support * 0.04)
    )
    packet_inner_outer_fit = _b01(
        (inner_outer_alignment * 0.26)
        + (perceptual_distance * 0.14)
        + (release_capacity * 0.12)
        + ((1.0 - field_attachment) * 0.12)
        + (emotional_decoupling * 0.10)
        + (felt_quality * 0.10)
        + (thought_quality * 0.08)
        + (experience_regulation * 0.05)
        + ((1.0 - diffuse_open_development_pressure) * 0.03)
    )
    packet_confidence_integrity = _b01(
        (action_clearance * 0.19)
        + (regulated_courage * 0.18)
        + (plan_quality * 0.18)
        + (risk_fit_quality * 0.16)
        + (packet_bearing_quality * 0.15)
        + (execution_quality * 0.10)
        - (max(0.0, action_clearance - packet_bearing_quality) * 0.12)
        - (action_inhibition * 0.06)
    )
    packet_repetition_potential = _b01(
        (process_core * 0.20)
        + (packet_bearing_quality * 0.20)
        + (form_process_quality * 0.14)
        + (form_action_affinity * 0.12)
        + (form_learning_trust * 0.10)
        + (context_quality * 0.10)
        + (packet_confidence_integrity * 0.08)
        - (risk_width_pressure * 0.08)
        - (overtrade_pressure * 0.06)
    )
    packet_curiosity_pull = _b01(
        (curiosity_tone * 0.22)
        + (object_contact_depth * 0.18)
        + (selective_attention * 0.16)
        + (form_novelty * 0.14)
        + (packet_repetition_potential * 0.12)
        + (max(0.0, 0.62 - packet_bearing_quality) * 0.08)
        - (fatigue_tone * 0.10)
    )

    outcome_confirmation = 0.0
    if reason == "tp_hit":
        outcome_confirmation = 0.10
    elif reason == "sl_hit":
        outcome_confirmation = -0.07
    elif reason in ("cancel", "timeout"):
        outcome_confirmation = -0.03
    elif reason in ("reward_too_small", "rr_too_low", "sl_distance_too_high"):
        outcome_confirmation = -0.05

    packet_process_reward = _b01(
        (process_core * 0.34)
        + (packet_bearing_quality * 0.22)
        + (packet_inner_outer_fit * 0.18)
        + (packet_confidence_integrity * 0.12)
        + (packet_repetition_potential * 0.10)
        + outcome_confirmation
        - (overtrade_pressure * 0.07)
        - (risk_width_pressure * 0.06)
    )
    packet_reorganization_need = _b01(
        ((1.0 - process_core) * 0.22)
        + ((1.0 - packet_bearing_quality) * 0.20)
        + ((1.0 - packet_inner_outer_fit) * 0.16)
        + (risk_width_pressure * 0.12)
        + (overtrade_pressure * 0.10)
        + (diffuse_open_development_pressure * 0.10)
        + (attempt_density * 0.06)
        + (0.06 if reason == "sl_hit" else 0.0)
        - (packet_process_reward * 0.16)
    )
    constructive_stimulation = _b01(
        (packet_process_reward * 0.42)
        + (packet_repetition_potential * 0.20)
        + (packet_inner_outer_fit * 0.16)
        + (packet_curiosity_pull * 0.12)
        + (max(0.0, outcome_confirmation) * 0.10)
        - (packet_reorganization_need * 0.10)
    )
    constructive_dopamine = _b01(
        (packet_process_reward * 0.34)
        + (packet_repetition_potential * 0.28)
        + (packet_curiosity_pull * 0.22)
        + (max(0.0, outcome_confirmation) * 0.08)
    )
    stabilizing_serotonin = _b01(
        (packet_inner_outer_fit * 0.30)
        + (packet_bearing_quality * 0.26)
        + (packet_confidence_integrity * 0.16)
        + (release_capacity * 0.12)
        + (reflection_maturity * 0.08)
        - (packet_reorganization_need * 0.10)
    )
    relief_endorphin = _b01(
        (packet_process_reward * 0.24)
        + (pressure_release * 0.24)
        + (release_capacity * 0.18)
        + ((1.0 - risk_width_pressure) * 0.10)
        + (packet_inner_outer_fit * 0.08)
        - (fatigue_tone * 0.08)
    )
    focused_acetylcholine = _b01(
        (perception_quality * 0.20)
        + (object_contact_depth * 0.18)
        + (selective_attention * 0.16)
        + (packet_curiosity_pull * 0.16)
        + (packet_repetition_potential * 0.14)
        + ((1.0 - diffuse_open_development_pressure) * 0.08)
    )

    if (
        (packet_process_reward >= 0.52 and packet_reorganization_need < 0.36)
        or (
            packet_process_reward >= 0.46
            and packet_bearing_quality >= 0.42
            and packet_inner_outer_fit >= 0.38
            and packet_reorganization_need < 0.42
        )
    ):
        packet_label = "constructive_packet"
    elif packet_reorganization_need >= 0.58 or (packet_process_reward < 0.34 and packet_reorganization_need >= 0.43):
        packet_label = "reorganize_packet"
    elif (
        packet_bearing_quality >= 0.50
        and packet_process_reward >= 0.38
        and packet_reorganization_need < 0.48
    ) or (
        packet_bearing_quality >= 0.46
        and packet_process_reward >= 0.40
        and packet_reorganization_need < 0.44
    ):
        packet_label = "bearing_packet"
    elif packet_curiosity_pull >= 0.46:
        packet_label = "curiosity_packet"
    elif packet_reorganization_need >= 0.50 and packet_process_reward < 0.34:
        packet_label = "reorganize_packet"
    else:
        packet_label = "mixed_packet"

    return {
        "experience_packet_label": str(packet_label),
        "packet_bearing_quality": float(packet_bearing_quality),
        "packet_inner_outer_fit": float(packet_inner_outer_fit),
        "packet_confidence_integrity": float(packet_confidence_integrity),
        "packet_repetition_potential": float(packet_repetition_potential),
        "packet_curiosity_pull": float(packet_curiosity_pull),
        "packet_process_reward": float(packet_process_reward),
        "packet_reorganization_need": float(packet_reorganization_need),
        "constructive_stimulation": float(constructive_stimulation),
        "constructive_dopamine": float(constructive_dopamine),
        "stabilizing_serotonin": float(stabilizing_serotonin),
        "relief_endorphin": float(relief_endorphin),
        "focused_acetylcholine": float(focused_acetylcholine),
    }

# --------------------------------------------------
from core.temporal_perception import (
    _advance_temporal_perception_state,
    _resolve_temporal_decision_modulation,
    build_temporal_coherence_state,
)

def _advance_felt_state(felt_state=None, bot=None, decision_tendency="hold", market_tick_advanced=True):

    state = dict(felt_state or {})
    if not state:
        return {}

    previous_state = dict(getattr(bot, "felt_state", {}) or {}) if bot is not None else {}

    felt_pressure = float(state.get("felt_pressure", 0.0) or 0.0)
    felt_stability = float(state.get("felt_stability", 0.0) or 0.0)
    felt_alignment = float(state.get("felt_alignment", 0.0) or 0.0)
    felt_conflict = float(state.get("felt_conflict", 0.0) or 0.0)
    felt_risk = float(state.get("felt_risk", 0.0) or 0.0)
    felt_opportunity = float(state.get("felt_opportunity", 0.0) or 0.0)

    previous_pressure = float(previous_state.get("felt_pressure", felt_pressure) or felt_pressure)
    previous_stability = float(previous_state.get("felt_stability", felt_stability) or felt_stability)
    previous_alignment = float(previous_state.get("felt_alignment", felt_alignment) or felt_alignment)
    previous_conflict = float(previous_state.get("felt_conflict", felt_conflict) or felt_conflict)
    previous_risk = float(previous_state.get("felt_risk", felt_risk) or felt_risk)
    previous_opportunity = float(previous_state.get("felt_opportunity", felt_opportunity) or felt_opportunity)
    previous_carry = float(previous_state.get("felt_carry", 0.0) or 0.0)
    previous_residue = float(previous_state.get("felt_residue", 0.0) or 0.0)
    previous_settlement = float(previous_state.get("felt_settlement", 0.0) or 0.0)
    previous_drift = float(previous_state.get("felt_drift", 0.0) or 0.0)

    regulatory_load = float(getattr(bot, "regulatory_load", 0.0) or 0.0) if bot is not None else 0.0
    action_capacity = float(getattr(bot, "action_capacity", 0.0) or 0.0) if bot is not None else 0.0
    recovery_need = float(getattr(bot, "recovery_need", 0.0) or 0.0) if bot is not None else 0.0
    competition_bias = abs(float(getattr(bot, "competition_bias", 0.0) or 0.0)) if bot is not None else 0.0

    felt_pressure = float(min(1.0, max(0.0, (previous_pressure * 0.28) + (felt_pressure * 0.72))))
    felt_stability = float(min(1.0, max(0.0, (previous_stability * 0.26) + (felt_stability * 0.74))))
    felt_alignment = float(min(1.0, max(0.0, (previous_alignment * 0.30) + (felt_alignment * 0.70))))
    felt_conflict = float(min(1.0, max(0.0, (previous_conflict * 0.34) + (felt_conflict * 0.66))))
    felt_risk = float(min(1.0, max(0.0, (previous_risk * 0.30) + (felt_risk * 0.70))))
    felt_opportunity = float(min(1.0, max(0.0, (previous_opportunity * 0.30) + (felt_opportunity * 0.70))))

    felt_drift = float(min(1.0, max(0.0, (abs(felt_pressure - previous_pressure) * 0.34) + (abs(felt_conflict - previous_conflict) * 0.26) + (abs(felt_alignment - previous_alignment) * 0.18) + (competition_bias * 0.12) + (max(0.0, regulatory_load - action_capacity) * 0.10))))
    felt_carry = float(min(1.0, max(0.0, (previous_carry * 0.62) + (felt_pressure * 0.18) + (felt_conflict * 0.14) + (felt_risk * 0.10) - (felt_stability * 0.10) - (felt_alignment * 0.08))))
    felt_residue = float(min(1.0, max(0.0, (previous_residue * 0.66) + (max(0.0, regulatory_load - action_capacity) * 0.16) + (recovery_need * 0.12) + (felt_carry * 0.10) - (max(0.0, action_capacity - regulatory_load) * 0.08))))
    felt_settlement = float(previous_settlement)

    if bool(market_tick_advanced):
        felt_settlement = float(min(1.0, max(0.0, (previous_settlement * 0.54) + (felt_stability * 0.18) + (felt_alignment * 0.14) - (felt_pressure * 0.10) - (felt_conflict * 0.08))))
    else:
        felt_pressure = float(min(1.0, max(0.0, (felt_pressure * 0.94) + (felt_carry * 0.05) - (felt_settlement * 0.04))))
        felt_conflict = float(min(1.0, max(0.0, (felt_conflict * 0.94) + (felt_residue * 0.04) - (felt_settlement * 0.03))))
        felt_stability = float(min(1.0, max(0.0, (felt_stability * 0.96) + (felt_settlement * 0.04) - (felt_residue * 0.03))))
        felt_alignment = float(min(1.0, max(0.0, (felt_alignment * 0.96) + (felt_settlement * 0.04) - (felt_drift * 0.03))))
        felt_settlement = float(min(1.0, max(0.0, (previous_settlement * 0.72) + (felt_stability * 0.10) + (felt_alignment * 0.08) - (felt_residue * 0.06))))

    tendency = str(decision_tendency or "hold").strip().lower()
    if tendency in ("observe", "hold"):
        felt_pressure = float(max(0.0, felt_pressure - 0.03))
        felt_conflict = float(max(0.0, felt_conflict - 0.02))
        felt_settlement = float(min(1.0, felt_settlement + 0.04))
    elif tendency == "replan":
        felt_drift = float(min(1.0, felt_drift + 0.04))
        felt_conflict = float(min(1.0, felt_conflict + 0.02))
    elif tendency == "act":
        felt_pressure = float(min(1.0, felt_pressure + 0.02))
        felt_carry = float(min(1.0, felt_carry + 0.02))

    state["felt_pressure"] = float(felt_pressure)
    state["felt_stability"] = float(felt_stability)
    state["felt_alignment"] = float(felt_alignment)
    state["felt_conflict"] = float(felt_conflict)
    state["felt_risk"] = float(felt_risk)
    state["felt_opportunity"] = float(felt_opportunity)
    state["felt_carry"] = float(felt_carry)
    state["felt_residue"] = float(felt_residue)
    state["felt_settlement"] = float(felt_settlement)
    state["felt_drift"] = float(felt_drift)
    return dict(state)

# --------------------------------------------------
def _advance_thought_state(thought_state=None, felt_state=None, temporal_perception_state=None, bot=None, decision_tendency="hold", market_tick_advanced=True):

    state = dict(thought_state or {})
    if not state:
        return {}

    previous_state = dict(getattr(bot, "thought_state", {}) or {}) if bot is not None else {}
    felt = dict(felt_state or {})
    temporal_state = dict(temporal_perception_state or {})

    decision_conflict = float(state.get("decision_conflict", 0.0) or 0.0)
    state_maturity = float(state.get("state_maturity", 0.0) or 0.0)
    rumination_depth = float(state.get("rumination_depth", 0.0) or 0.0)
    inner_time_scale = float(state.get("inner_time_scale", 0.0) or 0.0)
    decision_readiness = float(state.get("decision_readiness", 0.0) or 0.0)
    thought_alignment = float(state.get("thought_alignment", 0.0) or 0.0)
    decision_pressure = float(state.get("decision_pressure", 0.0) or 0.0)

    previous_conflict = float(previous_state.get("decision_conflict", decision_conflict) or decision_conflict)
    previous_maturity = float(previous_state.get("state_maturity", state_maturity) or state_maturity)
    previous_rumination = float(previous_state.get("rumination_depth", rumination_depth) or rumination_depth)
    previous_time_scale = float(previous_state.get("inner_time_scale", inner_time_scale) or inner_time_scale)
    previous_readiness = float(previous_state.get("decision_readiness", decision_readiness) or decision_readiness)
    previous_alignment = float(previous_state.get("thought_alignment", thought_alignment) or thought_alignment)
    previous_pressure = float(previous_state.get("decision_pressure", decision_pressure) or decision_pressure)
    previous_inertia = float(previous_state.get("thought_inertia", 0.0) or 0.0)
    previous_settlement = float(previous_state.get("thought_settlement", 0.0) or 0.0)
    previous_drift = float(previous_state.get("thought_drift", 0.0) or 0.0)

    felt_pressure = float(felt.get("felt_pressure", 0.0) or 0.0)
    felt_conflict = float(felt.get("felt_conflict", 0.0) or 0.0)
    felt_alignment = float(felt.get("felt_alignment", 0.0) or 0.0)
    felt_stability = float(felt.get("felt_stability", 0.0) or 0.0)
    temporal_transition_pressure = float(temporal_state.get("transition_pressure", 0.0) or 0.0)
    temporal_continuation_readiness = float(temporal_state.get("continuation_readiness", 0.0) or 0.0)
    temporal_exhaustion = float(temporal_state.get("temporal_exhaustion", 0.0) or 0.0)
    temporal_coherence = float(temporal_state.get("temporal_coherence", 0.0) or 0.0)

    decision_conflict = float(min(1.0, max(0.0, (previous_conflict * 0.30) + (decision_conflict * 0.70))))
    state_maturity = float(min(1.0, max(0.0, (previous_maturity * 0.34) + (state_maturity * 0.66))))
    rumination_depth = float(min(1.0, max(0.0, (previous_rumination * 0.32) + (rumination_depth * 0.68))))
    inner_time_scale = float(min(1.0, max(0.0, (previous_time_scale * 0.38) + (inner_time_scale * 0.62))))
    decision_readiness = float(min(1.0, max(0.0, (previous_readiness * 0.30) + (decision_readiness * 0.70))))
    thought_alignment = float(min(1.0, max(0.0, (previous_alignment * 0.32) + (thought_alignment * 0.68))))
    decision_pressure = float(min(1.0, max(0.0, (previous_pressure * 0.28) + (decision_pressure * 0.72))))

    thought_drift = float(min(1.0, max(0.0, (abs(decision_conflict - previous_conflict) * 0.32) + (abs(decision_readiness - previous_readiness) * 0.24) + (temporal_transition_pressure * 0.18) + (felt_conflict * 0.16) + (max(0.0, 1.0 - thought_alignment) * 0.10))))
    thought_inertia = float(min(1.0, max(0.0, (previous_inertia * 0.64) + (rumination_depth * 0.20) + (decision_pressure * 0.12) + (felt_pressure * 0.08) - (state_maturity * 0.08) - (temporal_coherence * 0.06))))
    thought_settlement = float(previous_settlement)

    if bool(market_tick_advanced):
        thought_settlement = float(min(1.0, max(0.0, (previous_settlement * 0.56) + (state_maturity * 0.16) + (thought_alignment * 0.16) + (temporal_coherence * 0.10) - (decision_conflict * 0.08) - (rumination_depth * 0.06))))
    else:
        rumination_depth = float(min(1.0, max(0.0, (rumination_depth * 0.95) + (thought_inertia * 0.05) - (thought_settlement * 0.04))))
        decision_pressure = float(min(1.0, max(0.0, (decision_pressure * 0.94) + (felt_pressure * 0.04) + (temporal_exhaustion * 0.03) - (thought_settlement * 0.04))))
        decision_readiness = float(min(1.0, max(0.0, (decision_readiness * 0.96) + (temporal_continuation_readiness * 0.04) - (thought_inertia * 0.04))))
        thought_alignment = float(min(1.0, max(0.0, (thought_alignment * 0.96) + (felt_alignment * 0.04) - (thought_drift * 0.03))))
        state_maturity = float(min(1.0, max(0.0, (state_maturity * 0.96) + (felt_stability * 0.04) - (temporal_exhaustion * 0.03))))
        thought_settlement = float(min(1.0, max(0.0, (previous_settlement * 0.74) + (state_maturity * 0.10) + (thought_alignment * 0.08) - (thought_inertia * 0.06))))

    tendency = str(decision_tendency or "hold").strip().lower()
    if tendency in ("observe", "hold"):
        rumination_depth = float(max(0.0, rumination_depth - 0.03))
        decision_pressure = float(max(0.0, decision_pressure - 0.02))
        thought_settlement = float(min(1.0, thought_settlement + 0.04))
    elif tendency == "replan":
        rumination_depth = float(min(1.0, rumination_depth + 0.04))
        thought_drift = float(min(1.0, thought_drift + 0.04))
    elif tendency == "act":
        decision_readiness = float(min(1.0, decision_readiness + 0.03))
        thought_inertia = float(max(0.0, thought_inertia - 0.02))

    state["decision_conflict"] = float(decision_conflict)
    state["state_maturity"] = float(state_maturity)
    state["rumination_depth"] = float(rumination_depth)
    state["inner_time_scale"] = float(inner_time_scale)
    state["decision_readiness"] = float(decision_readiness)
    state["thought_alignment"] = float(thought_alignment)
    state["decision_pressure"] = float(decision_pressure)
    state["thought_inertia"] = float(thought_inertia)
    state["thought_settlement"] = float(thought_settlement)
    state["thought_drift"] = float(thought_drift)
    state["maturity"] = float(state_maturity)
    state["readiness"] = float(decision_readiness)
    state["conflict"] = float(decision_conflict)
    return dict(state)
# --------------------------------------------------
# PRICE BUILD
# --------------------------------------------------
from trading.trade_plan import derive_trade_plan_from_brain

def resolve_fused_decision(candle_state, tension_state, mcm_snapshot, bot=None, temporal_perception_state=None):

    coherence = float(tension_state.get("coherence", 0.0) or 0.0)
    close_position = float(candle_state.get("close_position", 0.0) or 0.0)
    wick_bias = float(candle_state.get("wick_bias", 0.0) or 0.0)
    return_intensity = float(candle_state.get("return_intensity", 0.0) or 0.0)

    long_score = (coherence * 0.95) + (close_position * 0.75) + (wick_bias * 0.35) + (return_intensity * 0.45)
    short_score = (-coherence * 0.95) + (-close_position * 0.75) + (-wick_bias * 0.35) + (-return_intensity * 0.45)

    memory = mcm_snapshot.get("strongest_memory") or {}
    memory_center = float(memory.get("center", 0.0) or 0.0)
    memory_strength = float(memory.get("strength", 0.0) or 0.0)

    focus_point = 0.0
    focus_confidence = 0.0
    target_lock = 0.0
    target_drift = 0.0
    inhibition_level = 0.0
    habituation_level = 0.0
    competition_bias = 0.0
    observation_mode = False
    temporal_state = dict(temporal_perception_state or {})

    if bot is not None:
        focus_point = float(getattr(bot, "focus_point", 0.0) or 0.0)
        focus_confidence = float(getattr(bot, "focus_confidence", 0.0) or 0.0)
        target_lock = float(getattr(bot, "target_lock", 0.0) or 0.0)
        target_drift = float(getattr(bot, "target_drift", 0.0) or 0.0)
        inhibition_level = float(getattr(bot, "inhibition_level", 0.0) or 0.0)
        habituation_level = float(getattr(bot, "habituation_level", 0.0) or 0.0)
        competition_bias = float(getattr(bot, "competition_bias", 0.0) or 0.0)
        observation_mode = bool(getattr(bot, "observation_mode", False))
        if not temporal_state:
            temporal_state = dict(getattr(bot, "temporal_perception_state", {}) or {})

    affective = _resolve_affective_context_modulation(
        bot=bot,
        fused_state={
            "context_cluster_id": getattr(bot, "last_context_cluster_id", "-") if bot is not None else "-",
        },
    )
    temporal_modulation = _resolve_temporal_decision_modulation(temporal_state)

    long_score += float(temporal_modulation.get("long_bias", 0.0) or 0.0)
    short_score += float(temporal_modulation.get("short_bias", 0.0) or 0.0)
    felt_bearing_score = float(affective.get("felt_bearing_score", 0.0) or 0.0)
    felt_profile_label = str(affective.get("felt_profile_label", "mixed_unclear") or "mixed_unclear")
    decision_bias = float(affective.get("decision_bias", 0.0) or 0.0)
    conviction_boost = float(affective.get("conviction_boost", 0.0) or 0.0)
    caution_penalty = float(affective.get("caution_penalty", 0.0) or 0.0)
    volatility_penalty = float(affective.get("volatility_penalty", 0.0) or 0.0)
    risk_shift = float(affective.get("risk_shift", 0.0) or 0.0)
    rr_shift = float(affective.get("rr_shift", 0.0) or 0.0)

    pressure_weight = float(getattr(Config, "MCM_PRESSURE_WEIGHT", 0.35) or 0.35)
    memory_weight = float(getattr(Config, "MCM_MEMORY_WEIGHT", 0.20) or 0.20)
    regulation_weight = float(getattr(Config, "MCM_REGULATION_WEIGHT", 0.25) or 0.25)

    mcm_direction = (
        float(mcm_snapshot.get("mean_energy", 0.0) or 0.0) * pressure_weight
        + float(mcm_snapshot.get("mean_motivation", 0.0) or 0.0) * 0.10
        + memory_center * memory_weight
    )

    regulation_pressure = float(mcm_snapshot.get("regulation_pressure", 0.0) or 0.0)
    memory_penalty = min(0.42, max(0.0, memory_strength - 12.0) * 0.012)
    regulation_penalty = min(
        0.52,
        max(0.0, regulation_pressure - 0.85) * (regulation_weight * 0.34),
    )

    focus_long_bias = max(0.0, focus_point) * (0.20 + target_lock * 0.14 + focus_confidence * 0.10)
    focus_short_bias = max(0.0, -focus_point) * (0.20 + target_lock * 0.14 + focus_confidence * 0.10)
    drift_penalty = max(0.0, abs(target_drift) - 0.28) * 0.12
    inhibition_penalty = inhibition_level * 0.18
    habituation_penalty = habituation_level * 0.12
    competition_long_bias = max(0.0, competition_bias) * 0.28
    competition_short_bias = max(0.0, -competition_bias) * 0.28
    affective_long_bias = decision_bias + (conviction_boost * 0.42) - caution_penalty - volatility_penalty
    affective_short_bias = decision_bias + (conviction_boost * 0.42) - caution_penalty - volatility_penalty

    long_score = long_score + mcm_direction - regulation_penalty - memory_penalty + focus_long_bias + competition_long_bias - drift_penalty - inhibition_penalty - habituation_penalty + affective_long_bias
    short_score = short_score - mcm_direction - regulation_penalty - memory_penalty + focus_short_bias + competition_short_bias - drift_penalty - inhibition_penalty - habituation_penalty + affective_short_bias

    selected_attractor = str(mcm_snapshot.get("attractor", "neutral") or "neutral")
    self_state = str(mcm_snapshot.get("self_state", "stable") or "stable")

    long_allowed = True
    short_allowed = True
    reject_reason = None

    if selected_attractor == "defense":
        long_score -= 0.10
        short_score -= 0.10
        if abs(coherence) < 0.10 and abs(return_intensity) < 0.06:
            long_score -= 0.08
            short_score -= 0.08
            reject_reason = "defense_modulation"
    elif selected_attractor == "explore":
        long_score -= 0.03
        short_score -= 0.03
    elif selected_attractor == "analysis":
        long_score -= 0.08
        short_score -= 0.08
    elif selected_attractor == "cooperate":
        if abs(coherence) < 0.10:
            long_score -= 0.04
            short_score -= 0.04

    if self_state == "stressed":
        long_score -= 0.14
        short_score -= 0.14
        if abs(coherence) < 0.12 and abs(return_intensity) < 0.08:
            long_score -= 0.10
            short_score -= 0.10
            reject_reason = "stressed_modulation"

    elif self_state == "excited":
        long_score -= 0.03
        short_score -= 0.03

    if abs(return_intensity) < 0.05:
        long_score -= 0.03
        short_score -= 0.03

    if observation_mode:
        long_score -= 0.10
        short_score -= 0.10
        if reject_reason is None and max(long_score, short_score) < 0.34:
            long_score -= 0.05
            short_score -= 0.05
            reject_reason = "observation_modulation"

    if bool(getattr(Config, "MCM_ATTRACTOR_LONG_ALLOW", True)) is False:
        long_score -= 0.20
        if reject_reason is None:
            reject_reason = "long_attractor_config_modulation"

    if bool(getattr(Config, "MCM_ATTRACTOR_SHORT_ALLOW", True)) is False:
        short_score -= 0.20
        if reject_reason is None:
            reject_reason = "short_attractor_config_modulation"

    min_score = 0.18 + max(0.0, caution_penalty * 0.18) + max(0.0, volatility_penalty * 0.12)
    min_edge = 0.08 + max(0.0, caution_penalty * 0.10)

    side = "WAIT"
    best_score = 0.0

    if long_allowed and long_score > min_score and (long_score - short_score) > min_edge:
        side = "LONG"
        best_score = long_score
    elif short_allowed and short_score > min_score and (short_score - long_score) > min_edge:
        side = "SHORT"
        best_score = short_score
    elif reject_reason is None:
        reject_reason = "fused_score_too_low"

    min_rr_floor = max(0.0, float(getattr(Config, "MIN_RR", 1.0) or 1.0))
    endogenous_rr_lift = max(
        0.0,
        (abs(best_score) * 0.18)
        + (focus_confidence * 0.14)
        + (target_lock * 0.12)
        + (conviction_boost * 0.16)
        + (felt_bearing_score * 0.10)
        - (caution_penalty * 0.12)
        - (volatility_penalty * 0.10)
    )
    rr_value = min_rr_floor + endogenous_rr_lift
    risk_pct = float(getattr(Config, "BASE_RISK_PCT", 0.01) or 0.01)

    if self_state == "stressed":
        risk_pct *= float(getattr(Config, "MCM_STRESS_RISK_FACTOR", 0.75) or 0.75)
        rr_value = max(min_rr_floor, rr_value * 0.92)
    elif self_state == "excited":
        rr_value *= 1.0 + min(0.10, endogenous_rr_lift * 0.16)

    risk_pct = max(0.0005, risk_pct * (1.0 + risk_shift))
    rr_value = max(min_rr_floor, rr_value * (1.0 + rr_shift))

    _mcm_decision_debug(
        "MCM_DECISION | "
        f"long_score={long_score:.4f} "
        f"short_score={short_score:.4f} "
        f"memory_center={memory_center:.4f} "
        f"memory_strength={memory_strength:.0f} "
        f"self_state={self_state} "
        f"attractor={selected_attractor} "
        f"felt_bearing_score={felt_bearing_score:.4f} "
        f"felt_profile_label={felt_profile_label} "
        f"best_score={best_score:.4f} "
        f"reject_reason={reject_reason or '-'}"
    )

    return {
        "decision": side,
        "rr_value": float(rr_value),
        "risk_pct": float(risk_pct),
        "long_score": float(long_score),
        "short_score": float(short_score),
        "self_state": self_state,
        "attractor": selected_attractor,
        "reject_reason": reject_reason,
        "inhibition_level": float(inhibition_level),
        "habituation_level": float(habituation_level),
        "competition_bias": float(competition_bias),
        "observation_mode": bool(observation_mode),
        "felt_bearing_score": float(felt_bearing_score),
        "felt_profile_label": str(felt_profile_label),
    }

# --------------------------------------------------
# update target model
# --------------------------------------------------
def update_target_model(bot, candle_state, focus):

    if bot is None:
        return None

    focus_point = float(focus.get("focus_direction", 0.0) or 0.0)
    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    return_intensity = float(candle_state.get("return_intensity", 0.0) or 0.0)

    previous_focus_point = float(getattr(bot, "focus_point", 0.0) or 0.0)

    bot.focus_point = float((previous_focus_point * 0.55) + (focus_point * 0.45))
    bot.focus_confidence = float((float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.45) + (focus_confidence * 0.55))
    bot.target_lock = float((float(getattr(bot, "target_lock", 0.0) or 0.0) * 0.40) + (target_lock * 0.60))
    bot.target_drift = float(return_intensity - bot.focus_point)

    return {
        "focus_point": float(bot.focus_point),
        "focus_confidence": float(bot.focus_confidence),
        "target_lock": float(bot.target_lock),
        "target_drift": float(bot.target_drift),
    }

# --------------------------------------------------
def update_expectation_pressure_state(bot, candle_state, stimulus, snapshot, decision="WAIT", visual_market_state=None):

    if bot is None:
        return None

    focus = dict((stimulus or {}).get("focus", {}) or {})
    filtered_vision = dict((stimulus or {}).get("filtered_vision", {}) or {})
    snapshot_state = dict(snapshot or {})
    candle = dict(candle_state or {})
    visual = dict(visual_market_state or {})

    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)
    filtered_target_map = float(filtered_vision.get("target_map", 0.0) or 0.0)
    filtered_threat_map = float(filtered_vision.get("threat_map", 0.0) or 0.0)
    filtered_optic_flow = float(filtered_vision.get("optic_flow", 0.0) or 0.0)
    return_intensity = float(candle.get("return_intensity", 0.0) or 0.0)
    close_position = float(candle.get("close_position", 0.0) or 0.0)
    directional_bias = float(visual.get("directional_bias", 0.0) or 0.0)
    range_position = float(visual.get("range_position", 0.0) or 0.0)
    market_balance = float(visual.get("market_balance", 0.0) or 0.0)
    breakout_tension = float(visual.get("breakout_tension", 0.0) or 0.0)
    visual_coherence = float(visual.get("visual_coherence", 0.0) or 0.0)

    prior_entry_expectation = float(getattr(bot, "entry_expectation", 0.0) or 0.0)
    prior_target_expectation = float(getattr(bot, "target_expectation", 0.0) or 0.0)
    prior_approach_pressure = float(getattr(bot, "approach_pressure", 0.0) or 0.0)
    prior_pressure_release = float(getattr(bot, "pressure_release", 0.0) or 0.0)
    experience_regulation = float(getattr(bot, "experience_regulation", 0.0) or 0.0)
    reflection_maturity = float(getattr(bot, "reflection_maturity", 0.0) or 0.0)
    load_bearing_capacity = float(getattr(bot, "load_bearing_capacity", 0.0) or 0.0)
    protective_width_regulation = float(getattr(bot, "protective_width_regulation", 0.0) or 0.0)
    protective_courage = float(getattr(bot, "protective_courage", 0.0) or 0.0)
    inhibition_level = float(getattr(bot, "inhibition_level", 0.0) or 0.0)
    observation_mode = bool(getattr(bot, "observation_mode", False))
    stress_pressure = max(
        0.0,
        min(
            1.0,
            max(0.0, float(snapshot_state.get("regulation_pressure", 0.0) or 0.0) / 2.2),
        ),
    )

    decision_value = str(decision or "WAIT").upper().strip()
    has_position = isinstance(getattr(bot, "position", None), dict)
    has_pending_entry = isinstance(getattr(bot, "pending_entry", None), dict)

    if decision_value == "LONG":
        directional_entry_bias = max(0.0, directional_bias)
    elif decision_value == "SHORT":
        directional_entry_bias = max(0.0, -directional_bias)
    else:
        directional_entry_bias = max(0.0, abs(directional_bias) - 0.12)

    range_drive = max(0.0, abs(range_position) - 0.15)

    entry_anchor = max(
        0.0,
        min(
            1.0,
            (target_lock * 0.26)
            + (focus_confidence * 0.22)
            + (signal_relevance * 0.16)
            + (max(0.0, filtered_target_map) * 0.08)
            + (max(0.0, filtered_optic_flow) * 0.04)
            + (directional_entry_bias * 0.10)
            + (market_balance * 0.08)
            + (visual_coherence * 0.08)
            - (noise_damp * 0.06)
            - (filtered_threat_map * 0.04)
            - (breakout_tension * 0.02),
        ),
    )

    target_anchor = max(
        0.0,
        min(
            1.0,
            (target_lock * 0.28)
            + (focus_confidence * 0.14)
            + (signal_relevance * 0.12)
            + (max(0.0, filtered_target_map) * 0.10)
            + (max(0.0, abs(close_position)) * 0.04)
            + (directional_entry_bias * 0.08)
            + (range_drive * 0.08)
            + (market_balance * 0.08)
            + (visual_coherence * 0.08)
            - (noise_damp * 0.04)
            - (breakout_tension * 0.02),
        ),
    )

    if has_position:
        entry_expectation_target = 0.0
        target_expectation_target = min(1.0, target_anchor + 0.18)
    elif has_pending_entry or decision_value in ("LONG", "SHORT"):
        entry_expectation_target = min(1.0, entry_anchor + 0.16)
        target_expectation_target = target_anchor * 0.35
    else:
        entry_expectation_target = entry_anchor
        target_expectation_target = 0.0

    if observation_mode:
        entry_expectation_target *= 0.82
        target_expectation_target *= 0.86

    expectation_bias = max(entry_expectation_target, target_expectation_target)
    approach_gain = max(
        0.0,
        (expectation_bias * 0.24)
        + (max(0.0, 0.45 - abs(float(getattr(bot, "target_drift", 0.0) or 0.0))) * 0.28)
        + (max(0.0, abs(return_intensity)) * 0.08)
        + (directional_entry_bias * 0.10)
        + (market_balance * 0.08)
        + (visual_coherence * 0.06)
        + (breakout_tension * 0.08)
        - (inhibition_level * 0.10)
        - (experience_regulation * 0.06),
    )

    missed_release = 0.0
    if decision_value == "WAIT" and prior_entry_expectation > 0.34 and prior_approach_pressure > 0.24:
        missed_release = min(1.0, (prior_entry_expectation * 0.42) + (prior_approach_pressure * 0.58))
    elif has_position is False and has_pending_entry is False and prior_target_expectation > 0.30 and prior_approach_pressure > 0.20:
        missed_release = min(1.0, (prior_target_expectation * 0.36) + (prior_approach_pressure * 0.52))

    release_decay = max(0.0, prior_pressure_release * 0.62)
    bot.entry_expectation = float(max(0.0, min(1.0, (prior_entry_expectation * 0.52) + (entry_expectation_target * 0.48))))
    bot.target_expectation = float(max(0.0, min(1.0, (prior_target_expectation * 0.54) + (target_expectation_target * 0.46))))
    bot.approach_pressure = float(max(0.0, min(1.0, (prior_approach_pressure * 0.58) + approach_gain - (missed_release * 0.44))))
    bot.pressure_release = float(max(0.0, min(1.0, release_decay + missed_release)))
    bot.experience_regulation = float(max(0.0, min(1.0, (experience_regulation * 0.985) + (reflection_maturity * 0.010))))
    bot.reflection_maturity = float(max(0.0, min(1.0, (reflection_maturity * 0.996) + (abs(snapshot_state.get("mean_velocity", 0.0) or 0.0) * 0.002))))
    bot.load_bearing_capacity = float(max(0.0, min(1.0, (load_bearing_capacity * 0.82) + (bot.experience_regulation * 0.11) + (bot.reflection_maturity * 0.08) - (bot.pressure_release * 0.03))))
    bot.protective_width_regulation = float(max(0.0, min(
        1.0,
        (protective_width_regulation * 0.66)
        + (bot.approach_pressure * 0.18)
        + (bot.pressure_release * 0.26)
        + (bot.experience_regulation * 0.22)
        + (bot.reflection_maturity * 0.12)
        + (stress_pressure * 0.10)
        + (breakout_tension * 0.16)
        + (max(0.0, 1.0 - market_balance) * 0.10)
        - (visual_coherence * 0.06)
        - (inhibition_level * 0.06),
    )))
    bot.protective_courage = float(max(0.0, min(
        0.86,
        (protective_courage * 0.70)
        + (bot.load_bearing_capacity * 0.18)
        + (bot.reflection_maturity * 0.10)
        + (max(0.0, 1.0 - noise_damp) * 0.05)
        + (market_balance * 0.06)
        + (visual_coherence * 0.08)
        - (bot.pressure_release * 0.12)
        - (filtered_threat_map * 0.08)
        - (breakout_tension * 0.08),
    )))

    return {
        "entry_expectation": float(bot.entry_expectation),
        "target_expectation": float(bot.target_expectation),
        "approach_pressure": float(bot.approach_pressure),
        "pressure_release": float(bot.pressure_release),
        "experience_regulation": float(bot.experience_regulation),
        "reflection_maturity": float(bot.reflection_maturity),
        "load_bearing_capacity": float(bot.load_bearing_capacity),
        "protective_width_regulation": float(bot.protective_width_regulation),
        "protective_courage": float(bot.protective_courage),
    }

# --------------------------------------------------
def update_experience_state(bot, outcome_reason):

    if bot is None:
        return None

    reason = str(outcome_reason or "").strip().lower()

    prior_release = float(getattr(bot, "pressure_release", 0.0) or 0.0)
    prior_regulation = float(getattr(bot, "experience_regulation", 0.0) or 0.0)
    prior_maturity = float(getattr(bot, "reflection_maturity", 0.0) or 0.0)
    prior_entry_expectation = float(getattr(bot, "entry_expectation", 0.0) or 0.0)
    prior_target_expectation = float(getattr(bot, "target_expectation", 0.0) or 0.0)
    prior_pressure = float(getattr(bot, "approach_pressure", 0.0) or 0.0)
    prior_load_bearing_capacity = float(getattr(bot, "load_bearing_capacity", 0.0) or 0.0)
    prior_protective_width_regulation = float(getattr(bot, "protective_width_regulation", 0.0) or 0.0)
    prior_protective_courage = float(getattr(bot, "protective_courage", 0.0) or 0.0)

    attempt_feedback = {}
    stats = getattr(bot, "stats", None)
    if stats is not None and hasattr(stats, "get_attempt_feedback"):
        try:
            attempt_feedback = dict(stats.get_attempt_feedback() or {})
        except Exception:
            attempt_feedback = {}

    attempt_density = float(attempt_feedback.get("attempt_density", 0.0) or 0.0)
    overtrade_pressure = float(attempt_feedback.get("overtrade_pressure", 0.0) or 0.0)
    context_quality = float(attempt_feedback.get("context_quality", 0.0) or 0.0)
    blocked_ratio = float(attempt_feedback.get("blocked_ratio", 0.0) or 0.0)
    timeout_ratio = float(attempt_feedback.get("timeout_ratio", 0.0) or 0.0)
    fill_ratio = float(attempt_feedback.get("fill_ratio", 0.0) or 0.0)

    release_gain = 0.0
    regulation_gain = 0.0
    maturity_gain = 0.0

    if reason == "tp_hit":
        release_gain = 0.72 + (prior_pressure * 0.18)
        regulation_gain = 0.08 + (prior_target_expectation * 0.06)
        maturity_gain = 0.04
    elif reason == "sl_hit":
        release_gain = 0.82 + (prior_pressure * 0.22)
        regulation_gain = 0.05 + (prior_regulation * 0.02)
        maturity_gain = 0.06
    elif reason in ("cancel", "timeout"):
        release_gain = 0.58 + (prior_entry_expectation * 0.18)
        regulation_gain = 0.04
        maturity_gain = 0.05
    elif reason in ("reward_too_small", "rr_too_low", "sl_distance_too_high"):
        release_gain = 0.46 + (prior_entry_expectation * 0.16)
        regulation_gain = 0.03
        maturity_gain = 0.04

    release_gain += (attempt_density * 0.08) + (overtrade_pressure * 0.12)
    regulation_gain += (context_quality * 0.10) + (fill_ratio * 0.06) - (overtrade_pressure * 0.10) - (timeout_ratio * 0.06)
    maturity_gain += (context_quality * 0.08) + (fill_ratio * 0.04) + (blocked_ratio * 0.02) - (overtrade_pressure * 0.06)

    bot.pressure_release = float(max(0.0, min(1.0, (prior_release * 0.30) + release_gain)))
    bot.approach_pressure = float(max(0.0, min(1.0, (prior_pressure * 0.36) + (attempt_density * 0.18) + (overtrade_pressure * 0.26) - (context_quality * 0.14))))
    bot.entry_expectation = float(max(0.0, min(1.0, (prior_entry_expectation * 0.42) - (overtrade_pressure * 0.10) + (context_quality * 0.04))))
    bot.target_expectation = float(max(0.0, min(1.0, (prior_target_expectation * 0.34) - (overtrade_pressure * 0.08) + (fill_ratio * 0.06))))
    bot.experience_regulation = float(max(0.0, min(1.0, (prior_regulation * 0.82) + regulation_gain + (prior_maturity * 0.04))))
    bot.reflection_maturity = float(max(0.0, min(1.0, (prior_maturity * 0.96) + maturity_gain + (abs(release_gain - regulation_gain) * 0.04))))
    bot.load_bearing_capacity = float(max(0.0, min(
        1.0,
        (prior_load_bearing_capacity * 0.76)
        + (bot.experience_regulation * 0.22)
        + (bot.reflection_maturity * 0.16)
        - (bot.pressure_release * 0.10)
        - (overtrade_pressure * 0.08),
    )))
    bot.protective_width_regulation = float(max(0.0, min(
        1.0,
        (prior_protective_width_regulation * 0.58)
        + (bot.pressure_release * 0.36)
        + (bot.experience_regulation * 0.28)
        + (bot.reflection_maturity * 0.18)
        + (prior_pressure * 0.14)
        + (overtrade_pressure * 0.12),
    )))
    bot.protective_courage = float(max(0.0, min(
        0.86,
        (prior_protective_courage * 0.62)
        + (bot.load_bearing_capacity * 0.16)
        + (bot.reflection_maturity * 0.10)
        - (bot.pressure_release * 0.16)
        - (overtrade_pressure * 0.12)
        + (context_quality * 0.08),
    )))

    return {
        "entry_expectation": float(bot.entry_expectation),
        "target_expectation": float(bot.target_expectation),
        "approach_pressure": float(bot.approach_pressure),
        "pressure_release": float(bot.pressure_release),
        "experience_regulation": float(bot.experience_regulation),
        "reflection_maturity": float(bot.reflection_maturity),
        "load_bearing_capacity": float(bot.load_bearing_capacity),
        "protective_width_regulation": float(bot.protective_width_regulation),
        "protective_courage": float(bot.protective_courage),
        "attempt_density": float(attempt_density),
        "overtrade_pressure": float(overtrade_pressure),
        "context_quality": float(context_quality),
        "fill_ratio": float(fill_ratio),
        "blocked_ratio": float(blocked_ratio),
        "timeout_ratio": float(timeout_ratio),
    }

# --------------------------------------------------
def build_state_signature(candle_state, tension_state, snapshot, stimulus, bot=None):

    focus = dict(stimulus.get("focus", {}) or {})
    filtered_vision = dict(stimulus.get("filtered_vision", {}) or {})
    strongest_memory = dict((snapshot.get("strongest_memory") or {}) or {})

    focus_point = float(getattr(bot, "focus_point", 0.0) or 0.0) if bot is not None else 0.0
    focus_confidence = float(getattr(bot, "focus_confidence", 0.0) or 0.0) if bot is not None else 0.0
    target_lock = float(getattr(bot, "target_lock", 0.0) or 0.0) if bot is not None else 0.0
    target_drift = float(getattr(bot, "target_drift", 0.0) or 0.0) if bot is not None else 0.0
    entry_expectation = float(getattr(bot, "entry_expectation", 0.0) or 0.0) if bot is not None else 0.0
    target_expectation = float(getattr(bot, "target_expectation", 0.0) or 0.0) if bot is not None else 0.0
    approach_pressure = float(getattr(bot, "approach_pressure", 0.0) or 0.0) if bot is not None else 0.0
    pressure_release = float(getattr(bot, "pressure_release", 0.0) or 0.0) if bot is not None else 0.0
    experience_regulation = float(getattr(bot, "experience_regulation", 0.0) or 0.0) if bot is not None else 0.0
    reflection_maturity = float(getattr(bot, "reflection_maturity", 0.0) or 0.0) if bot is not None else 0.0
    load_bearing_capacity = float(getattr(bot, "load_bearing_capacity", 0.0) or 0.0) if bot is not None else 0.0
    protective_width_regulation = float(getattr(bot, "protective_width_regulation", 0.0) or 0.0) if bot is not None else 0.0
    protective_courage = float(getattr(bot, "protective_courage", 0.0) or 0.0) if bot is not None else 0.0

    coherence = float(tension_state.get("coherence", 0.0) or 0.0)
    energy = float(tension_state.get("energy", 0.0) or 0.0)
    asymmetry = int(tension_state.get("asymmetry", 0) or 0)
    return_intensity = float(candle_state.get("return_intensity", 0.0) or 0.0)
    close_position = float(candle_state.get("close_position", 0.0) or 0.0)

    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)
    filtered_target_map = float(filtered_vision.get("target_map", 0.0) or 0.0)
    filtered_threat_map = float(filtered_vision.get("threat_map", 0.0) or 0.0)

    memory_center = float(strongest_memory.get("center", 0.0) or 0.0)
    memory_strength = int(strongest_memory.get("strength", 0) or 0)

    attractor = str(snapshot.get("attractor", "neutral") or "neutral")
    self_state = str(snapshot.get("self_state", "stable") or "stable")

    attractor_code = {
        "defense": -2,
        "analysis": -1,
        "neutral": 0,
        "cooperate": 1,
        "explore": 2,
    }.get(attractor, 0)

    self_state_code = {
        "stressed": -1,
        "stable": 0,
        "active": 1,
        "excited": 2,
    }.get(self_state, 0)

    signature_vector = [
        round(float(energy), 2),
        round(float(coherence), 2),
        int(asymmetry),
        round(float(close_position), 2),
        round(float(return_intensity), 2),
        round(float(focus_point), 2),
        round(float(focus_confidence), 2),
        round(float(target_lock), 2),
        round(float(target_drift), 2),
        round(float(entry_expectation), 2),
        round(float(target_expectation), 2),
        round(float(approach_pressure), 2),
        round(float(pressure_release), 2),
        round(float(experience_regulation), 2),
        round(float(reflection_maturity), 2),
        round(float(load_bearing_capacity), 2),
        round(float(protective_width_regulation), 2),
        round(float(protective_courage), 2),
        round(float(signal_relevance), 2),
        round(float(noise_damp), 2),
        round(float(filtered_target_map), 2),
        round(float(filtered_threat_map), 2),
        round(float(memory_center), 2),
        int(memory_strength),
        int(attractor_code),
        int(self_state_code),
    ]

    signature_key = "|".join(
        [
            f"e:{round(float(energy) / 0.25) * 0.25:.2f}",
            f"c:{round(float(coherence) / 0.20) * 0.20:.2f}",
            f"a:{int(asymmetry)}",
            f"cp:{round(float(close_position) / 0.25) * 0.25:.2f}",
            f"ri:{round(float(return_intensity) / 0.20) * 0.20:.2f}",
            f"fp:{round(float(focus_point) / 0.20) * 0.20:.2f}",
            f"fc:{round(float(focus_confidence) / 0.20) * 0.20:.2f}",
            f"tl:{round(float(target_lock) / 0.20) * 0.20:.2f}",
            f"td:{round(float(target_drift) / 0.20) * 0.20:.2f}",
            f"ee:{round(float(entry_expectation) / 0.20) * 0.20:.2f}",
            f"te:{round(float(target_expectation) / 0.20) * 0.20:.2f}",
            f"ap:{round(float(approach_pressure) / 0.20) * 0.20:.2f}",
            f"pr:{round(float(pressure_release) / 0.20) * 0.20:.2f}",
            f"er:{round(float(experience_regulation) / 0.20) * 0.20:.2f}",
            f"rm:{round(float(reflection_maturity) / 0.20) * 0.20:.2f}",
            f"lb:{round(float(load_bearing_capacity) / 0.20) * 0.20:.2f}",
            f"pw:{round(float(protective_width_regulation) / 0.20) * 0.20:.2f}",
            f"pc:{round(float(protective_courage) / 0.20) * 0.20:.2f}",
            f"sr:{round(float(signal_relevance) / 0.20) * 0.20:.2f}",
            f"nd:{round(float(noise_damp) / 0.20) * 0.20:.2f}",
            f"tm:{round(float(filtered_target_map) / 0.25) * 0.25:.2f}",
            f"th:{round(float(filtered_threat_map) / 0.25) * 0.25:.2f}",
            f"mc:{round(float(memory_center) / 0.25) * 0.25:.2f}",
            f"ms:{int(min(12, max(0, memory_strength)))}",
            f"at:{int(attractor_code)}",
            f"ss:{int(self_state_code)}",
        ]
    )

    return {
        "signature_key": str(signature_key),
        "signature_vector": list(signature_vector),
        "attractor_code": int(attractor_code),
        "self_state_code": int(self_state_code),
    }

# --------------------------------------------------
# internal form symbols
# --------------------------------------------------
def _quantize_form_axis(value, step=0.20, min_value=-2.0, max_value=2.0):
    return _quantize_form_axis_impl(value, step=step, min_value=min_value, max_value=max_value)

from memory.form_symbol_memory import _flush_form_symbol_memory_if_due

def _extract_outcome_form_symbol_state(bot, position=None):
    return _extract_outcome_form_symbol_state_impl(bot, position=position)

def _update_form_symbol_development_from_outcome(bot, outcome_reason, position=None, outcome_decomposition=None):

    return _update_form_symbol_development_from_outcome_impl(
        bot,
        outcome_reason,
        position=position,
        outcome_decomposition=outcome_decomposition,
    )


def build_form_symbol_state(bot, visual_market_state=None, structure_perception_state=None, perception_state=None, felt_state=None, snapshot=None):

    return _build_form_symbol_state_impl(
        bot,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        perception_state=perception_state,
        felt_state=felt_state,
        snapshot=snapshot,
    )

# --------------------------------------------------
# context cluster
# --------------------------------------------------
def decay_weak_cluster(bot):

    if bot is None:
        return None

    cluster_map = getattr(bot, "context_clusters", None)
    if not isinstance(cluster_map, dict):
        bot.context_clusters = {}
        return None

    decay_score = float(getattr(Config, "MCM_CONTEXT_DECAY", 0.992) or 0.992)
    max_age = int(getattr(Config, "MCM_CONTEXT_MAX_AGE", 320) or 320)
    min_trust = float(getattr(Config, "MCM_CONTEXT_MIN_TRUST", 0.06) or 0.06)

    updated_clusters = {}

    for cluster_id, item in cluster_map.items():
        if not isinstance(item, dict):
            continue

        aged_item = dict(item)
        aged_item["age"] = int(aged_item.get("age", 0) or 0) + 1
        aged_item["score"] = float(aged_item.get("score", 0.0) or 0.0) * decay_score
        aged_item["trust"] = float(aged_item.get("trust", 0.0) or 0.0) * 0.998

        if int(aged_item["age"]) > max_age and abs(float(aged_item["score"])) < 0.18 and float(aged_item["trust"]) < min_trust:
            continue

        updated_clusters[str(cluster_id)] = aged_item

    bot.context_clusters = updated_clusters
    return updated_clusters

# --------------------------------------------------
def classify_state_cluster(bot, state_signature):

    if bot is None:
        return None

    signature = dict(state_signature or {})
    signature_key = str(signature.get("signature_key", "") or "").strip()
    signature_vector = list(signature.get("signature_vector", []) or [])

    if not signature_key or not signature_vector:
        return None

    if not isinstance(getattr(bot, "context_clusters", None), dict):
        bot.context_clusters = {}

    decay_weak_cluster(bot)

    cluster_threshold = float(getattr(Config, "MCM_CONTEXT_MATCH_THRESHOLD", 0.28) or 0.28)
    current_vector = np.asarray(signature_vector, dtype=float)

    nearest_cluster_id = None
    nearest_cluster = None
    nearest_distance = None

    for cluster_id, item in bot.context_clusters.items():
        if not isinstance(item, dict):
            continue

        center_vector = list(item.get("center_vector", []) or [])
        if len(center_vector) != len(signature_vector):
            continue

        center_array = np.asarray(center_vector, dtype=float)
        distance = float(np.mean(np.abs(current_vector - center_array)))

        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_cluster_id = str(cluster_id)
            nearest_cluster = item

    if nearest_cluster is None or nearest_distance is None or nearest_distance > cluster_threshold:
        bot.context_cluster_seq = int(getattr(bot, "context_cluster_seq", 0) or 0) + 1
        nearest_cluster_id = f"ctx_{int(bot.context_cluster_seq)}"
        nearest_cluster = {
            "cluster_id": str(nearest_cluster_id),
            "center_vector": list(signature_vector),
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
            "signature_keys": [str(signature_key)],
            "last_signature_key": str(signature_key),
            "last_outcome": None,
            "last_distance": 0.0,
        }
        bot.context_clusters[str(nearest_cluster_id)] = nearest_cluster
        nearest_distance = 0.0

    seen_before = int(nearest_cluster.get("seen", 0) or 0)
    learn_rate = 1.0 / float(max(1, min(24, seen_before + 1)))
    center_array = np.asarray(list(nearest_cluster.get("center_vector", []) or signature_vector), dtype=float)
    new_center = center_array + ((current_vector - center_array) * learn_rate)
    distance_now = float(np.mean(np.abs(current_vector - new_center)))

    nearest_cluster["center_vector"] = [float(round(value, 4)) for value in new_center.tolist()]
    nearest_cluster["seen"] = seen_before + 1
    nearest_cluster["age"] = 0
    nearest_cluster["radius"] = float((float(nearest_cluster.get("radius", 0.0) or 0.0) * 0.72) + (distance_now * 0.28))
    nearest_cluster["variance"] = float((float(nearest_cluster.get("variance", 0.0) or 0.0) * 0.70) + ((distance_now ** 2) * 0.30))
    nearest_cluster["trust"] = float(min(1.0, (float(nearest_cluster.get("trust", 0.0) or 0.0) * 0.82) + 0.10))
    nearest_cluster["last_signature_key"] = str(signature_key)
    nearest_cluster["last_distance"] = float(nearest_distance)

    signature_keys = list(nearest_cluster.get("signature_keys", []) or [])
    if signature_key not in signature_keys:
        signature_keys.append(str(signature_key))
    nearest_cluster["signature_keys"] = signature_keys[-24:]

    bot.context_clusters[str(nearest_cluster_id)] = nearest_cluster
    bot.last_context_cluster_id = str(nearest_cluster_id)
    bot.last_context_cluster_key = str(signature_key)

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
        "last_outcome": nearest_cluster.get("last_outcome"),
    }

# --------------------------------------------------
def merge_similar_signatures(bot):

    if bot is None:
        return None

    cluster_map = getattr(bot, "context_clusters", None)
    if not isinstance(cluster_map, dict) or len(cluster_map) < 2:
        return cluster_map

    merge_threshold = float(getattr(Config, "MCM_CONTEXT_MERGE_THRESHOLD", 0.16) or 0.16)
    cluster_ids = list(cluster_map.keys())
    consumed_ids = set()
    merged_clusters = {}

    for idx, cluster_id in enumerate(cluster_ids):
        if cluster_id in consumed_ids:
            continue

        base_item = dict(cluster_map.get(cluster_id) or {})
        base_vector = list(base_item.get("center_vector", []) or [])
        if not base_vector:
            merged_clusters[str(cluster_id)] = base_item
            continue

        base_array = np.asarray(base_vector, dtype=float)

        for other_id in cluster_ids[idx + 1:]:
            if other_id in consumed_ids:
                continue

            other_item = dict(cluster_map.get(other_id) or {})
            other_vector = list(other_item.get("center_vector", []) or [])
            if len(other_vector) != len(base_vector):
                continue

            other_array = np.asarray(other_vector, dtype=float)
            distance = float(np.mean(np.abs(base_array - other_array)))

            if distance > merge_threshold:
                continue

            base_seen = int(base_item.get("seen", 0) or 0)
            other_seen = int(other_item.get("seen", 0) or 0)
            total_seen = max(1, base_seen + other_seen)

            merged_center = ((base_array * base_seen) + (other_array * other_seen)) / float(total_seen)
            base_item["center_vector"] = [float(round(value, 4)) for value in merged_center.tolist()]
            base_array = np.asarray(base_item["center_vector"], dtype=float)
            base_item["seen"] = int(total_seen)
            base_item["tp"] = int(base_item.get("tp", 0) or 0) + int(other_item.get("tp", 0) or 0)
            base_item["sl"] = int(base_item.get("sl", 0) or 0) + int(other_item.get("sl", 0) or 0)
            base_item["cancel"] = int(base_item.get("cancel", 0) or 0) + int(other_item.get("cancel", 0) or 0)
            base_item["timeout"] = int(base_item.get("timeout", 0) or 0) + int(other_item.get("timeout", 0) or 0)
            base_item["score"] = float(base_item.get("score", 0.0) or 0.0) + float(other_item.get("score", 0.0) or 0.0)
            base_item["trust"] = float(min(1.0, max(float(base_item.get("trust", 0.0) or 0.0), float(other_item.get("trust", 0.0) or 0.0)) + 0.06))
            base_item["variance"] = float((float(base_item.get("variance", 0.0) or 0.0) + float(other_item.get("variance", 0.0) or 0.0) + (distance ** 2)) / 3.0)
            base_item["radius"] = float(max(float(base_item.get("radius", 0.0) or 0.0), float(other_item.get("radius", 0.0) or 0.0), distance))
            base_item["age"] = int(min(int(base_item.get("age", 0) or 0), int(other_item.get("age", 0) or 0)))

            merged_keys = list(base_item.get("signature_keys", []) or [])
            merged_keys.extend(list(other_item.get("signature_keys", []) or []))
            unique_keys = []
            for key in merged_keys:
                key_value = str(key)
                if key_value not in unique_keys:
                    unique_keys.append(key_value)
            base_item["signature_keys"] = unique_keys[-32:]
            base_item["last_signature_key"] = str(base_item.get("last_signature_key") or other_item.get("last_signature_key") or "")
            base_item["last_outcome"] = other_item.get("last_outcome") or base_item.get("last_outcome")
            base_item["last_distance"] = float(min(float(base_item.get("last_distance", 0.0) or 0.0), float(other_item.get("last_distance", 0.0) or 0.0), distance))

            consumed_ids.add(str(other_id))

            if str(getattr(bot, "last_context_cluster_id", "") or "") == str(other_id):
                bot.last_context_cluster_id = str(cluster_id)

        merged_clusters[str(cluster_id)] = base_item

    bot.context_clusters = merged_clusters
    return merged_clusters

# --------------------------------------------------
def split_unstable_cluster(bot):

    if bot is None:
        return None

    cluster_map = getattr(bot, "context_clusters", None)
    if not isinstance(cluster_map, dict) or not cluster_map:
        return cluster_map

    split_variance = float(getattr(Config, "MCM_CONTEXT_SPLIT_VARIANCE", 0.085) or 0.085)
    split_radius = float(getattr(Config, "MCM_CONTEXT_SPLIT_RADIUS", 0.24) or 0.24)
    updated_clusters = {}

    for cluster_id, item in cluster_map.items():
        cluster_item = dict(item or {})
        seen = int(cluster_item.get("seen", 0) or 0)
        variance = float(cluster_item.get("variance", 0.0) or 0.0)
        radius = float(cluster_item.get("radius", 0.0) or 0.0)
        center_vector = list(cluster_item.get("center_vector", []) or [])

        if seen < 8 or not center_vector or (variance <= split_variance and radius <= split_radius):
            updated_clusters[str(cluster_id)] = cluster_item
            continue

        bot.context_cluster_seq = int(getattr(bot, "context_cluster_seq", 0) or 0) + 1
        child_cluster_id = f"ctx_{int(bot.context_cluster_seq)}"

        split_axis = int(np.argmax(np.abs(np.asarray(center_vector, dtype=float)))) if center_vector else 0
        offset_size = max(0.04, min(0.18, radius * 0.50 + (variance * 0.35)))

        parent_center = list(center_vector)
        child_center = list(center_vector)

        parent_center[split_axis] = float(round(parent_center[split_axis] - offset_size, 4))
        child_center[split_axis] = float(round(child_center[split_axis] + offset_size, 4))

        parent_tp = int(cluster_item.get("tp", 0) or 0)
        parent_sl = int(cluster_item.get("sl", 0) or 0)
        parent_cancel = int(cluster_item.get("cancel", 0) or 0)
        parent_timeout = int(cluster_item.get("timeout", 0) or 0)

        child_item = dict(cluster_item)
        child_item["cluster_id"] = str(child_cluster_id)
        child_item["center_vector"] = child_center
        child_item["seen"] = max(1, seen // 2)
        child_item["tp"] = max(0, parent_tp // 2)
        child_item["sl"] = max(0, parent_sl // 2)
        child_item["cancel"] = max(0, parent_cancel // 2)
        child_item["timeout"] = max(0, parent_timeout // 2)
        child_item["score"] = float(float(cluster_item.get("score", 0.0) or 0.0) * 0.46)
        child_item["trust"] = float(max(0.08, float(cluster_item.get("trust", 0.0) or 0.0) * 0.72))
        child_item["variance"] = float(max(0.0, variance * 0.58))
        child_item["radius"] = float(max(0.0, radius * 0.62))
        child_item["age"] = 0
        child_item["signature_keys"] = list((list(cluster_item.get("signature_keys", []) or []))[-12:])
        child_item["last_distance"] = float(radius * 0.50)

        cluster_item["center_vector"] = parent_center
        cluster_item["seen"] = max(1, seen - int(child_item["seen"]))
        cluster_item["tp"] = max(0, parent_tp - int(child_item["tp"]))
        cluster_item["sl"] = max(0, parent_sl - int(child_item["sl"]))
        cluster_item["cancel"] = max(0, parent_cancel - int(child_item["cancel"]))
        cluster_item["timeout"] = max(0, parent_timeout - int(child_item["timeout"]))
        cluster_item["score"] = float(float(cluster_item.get("score", 0.0) or 0.0) * 0.54)
        cluster_item["trust"] = float(max(0.08, float(cluster_item.get("trust", 0.0) or 0.0) * 0.76))
        cluster_item["variance"] = float(max(0.0, variance * 0.54))
        cluster_item["radius"] = float(max(0.0, radius * 0.58))
        cluster_item["age"] = 0
        cluster_item["last_distance"] = float(radius * 0.50)

        updated_clusters[str(cluster_id)] = cluster_item
        updated_clusters[str(child_cluster_id)] = child_item

    bot.context_clusters = updated_clusters
    return updated_clusters

# --------------------------------------------------
def update_context_cluster_outcome(bot, cluster_id, outcome=None):

    if bot is None:
        return None

    cluster_map = getattr(bot, "context_clusters", None)
    if not isinstance(cluster_map, dict):
        return None

    cluster_key = str(cluster_id or "").strip()
    if not cluster_key:
        return None

    cluster = cluster_map.get(cluster_key)
    if not isinstance(cluster, dict):
        return None

    reason = str(outcome or "").strip().lower()

    if reason == "tp_hit":
        cluster["tp"] = int(cluster.get("tp", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) + 1.00
        cluster["trust"] = float(min(1.0, float(cluster.get("trust", 0.0) or 0.0) + 0.08))
        cluster["last_outcome"] = "tp_hit"
    elif reason == "sl_hit":
        cluster["sl"] = int(cluster.get("sl", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 1.10
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.10))
        cluster["last_outcome"] = "sl_hit"
    elif reason == "cancel":
        cluster["cancel"] = int(cluster.get("cancel", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 0.35
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.04))
        cluster["last_outcome"] = "cancel"
    elif reason == "timeout":
        cluster["timeout"] = int(cluster.get("timeout", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 0.28
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.03))
        cluster["last_outcome"] = "timeout"
    elif reason == "reward_too_small":
        cluster["cancel"] = int(cluster.get("cancel", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 0.40
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.05))
        cluster["last_outcome"] = "reward_too_small"
    elif reason == "sl_distance_too_high":
        cluster["sl"] = int(cluster.get("sl", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 0.62
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.07))
        cluster["last_outcome"] = "sl_distance_too_high"
    elif reason == "rr_too_low":
        cluster["timeout"] = int(cluster.get("timeout", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 0.48
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.05))
        cluster["last_outcome"] = "rr_too_low"

    cluster["score"] = float(max(-8.0, min(8.0, float(cluster.get("score", 0.0) or 0.0))))
    cluster["age"] = 0
    cluster_map[cluster_key] = cluster
    bot.context_clusters = cluster_map

    return {
        "cluster_id": str(cluster_key),
        "seen": int(cluster.get("seen", 0) or 0),
        "tp": int(cluster.get("tp", 0) or 0),
        "sl": int(cluster.get("sl", 0) or 0),
        "cancel": int(cluster.get("cancel", 0) or 0),
        "timeout": int(cluster.get("timeout", 0) or 0),
        "score": float(cluster.get("score", 0.0) or 0.0),
        "trust": float(cluster.get("trust", 0.0) or 0.0),
        "variance": float(cluster.get("variance", 0.0) or 0.0),
        "radius": float(cluster.get("radius", 0.0) or 0.0),
        "last_outcome": cluster.get("last_outcome"),
    }


# --------------------------------------------------
def lookup_context_cluster(bot, state_signature):

    if bot is None:
        return None

    cluster_map = getattr(bot, "context_clusters", None)
    if not isinstance(cluster_map, dict) or not cluster_map:
        return None

    signature_vector = list((state_signature or {}).get("signature_vector", []) or [])
    if not signature_vector:
        return None

    current_vector = np.asarray(signature_vector, dtype=float)
    lookup_threshold = float(getattr(Config, "MCM_CONTEXT_LOOKUP_THRESHOLD", 0.30) or 0.30)

    nearest_cluster_id = None
    nearest_cluster = None
    nearest_distance = None

    for cluster_id, item in cluster_map.items():
        if not isinstance(item, dict):
            continue

        center_vector = list(item.get("center_vector", []) or [])
        if len(center_vector) != len(signature_vector):
            continue

        center_array = np.asarray(center_vector, dtype=float)
        distance = float(np.mean(np.abs(current_vector - center_array)))

        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_cluster_id = str(cluster_id)
            nearest_cluster = item

    if nearest_cluster is None or nearest_distance is None or nearest_distance > lookup_threshold:
        return None

    return {
        "cluster_id": str(nearest_cluster_id),
        "distance": float(nearest_distance),
        "seen": int(nearest_cluster.get("seen", 0) or 0),
        "tp": int(nearest_cluster.get("tp", 0) or 0),
        "sl": int(nearest_cluster.get("sl", 0) or 0),
        "cancel": int(nearest_cluster.get("cancel", 0) or 0),
        "timeout": int(nearest_cluster.get("timeout", 0) or 0),
        "score": float(nearest_cluster.get("score", 0.0) or 0.0),
        "trust": float(nearest_cluster.get("trust", 0.0) or 0.0),
        "variance": float(nearest_cluster.get("variance", 0.0) or 0.0),
        "radius": float(nearest_cluster.get("radius", 0.0) or 0.0),
        "age": int(nearest_cluster.get("age", 0) or 0),
        "last_outcome": nearest_cluster.get("last_outcome"),
    }

# --------------------------------------------------
# Update Inner Field History
# --------------------------------------------------
def _update_inner_field_history(inner_field_state, bot=None):

    field_state = dict(inner_field_state or {})

    if not field_state:
        return {
            "inner_field_history": [],
            "inner_field_history_length": 0,
            "inner_field_pressure_trend": 0.0,
            "inner_field_bearing_trend": 0.0,
            "inner_field_topology_tension_trend": 0.0,
            "inner_field_memory_resonance_trend": 0.0,
            "inner_field_history_label": "empty_field_history",
        }

    if bot is not None:
        prior_history = [
            dict(item or {})
            for item in list(getattr(bot, "inner_field_history", []) or [])
            if isinstance(item, dict)
        ]
    else:
        prior_history = [
            dict(item or {})
            for item in list(field_state.get("inner_field_history", []) or [])
            if isinstance(item, dict)
        ]

    limit = max(
        4,
        min(
            256,
            int(getattr(Config, "MCM_INNER_FIELD_HISTORY_LIMIT", 48) or 48),
        ),
    )
    runtime_snapshot = dict(getattr(bot, "mcm_runtime_snapshot", {}) or {}) if bot is not None else {}
    neural_felt_state = dict(field_state.get("neural_felt_state", {}) or {})

    entry = {
        "timestamp": field_state.get("timestamp", runtime_snapshot.get("timestamp", getattr(bot, "current_timestamp", None) if bot is not None else None)),
        "runtime_tick_seq": int(runtime_snapshot.get("runtime_tick_seq", getattr(bot, "mcm_runtime_market_ticks", 0) if bot is not None else 0) or 0),
        "field_mean_energy": float(field_state.get("field_mean_energy", 0.0) or 0.0),
        "field_mean_velocity": float(field_state.get("field_mean_velocity", 0.0) or 0.0),
        "field_pressure": float(field_state.get("field_regulation_pressure", 0.0) or 0.0),
        "field_cluster_count": int(field_state.get("field_cluster_count", 0) or 0),
        "field_areal_count": int(field_state.get("field_areal_count", 0) or 0),
        "field_areal_pressure_mean": float(field_state.get("field_areal_pressure_mean", 0.0) or 0.0),
        "field_areal_coherence_mean": float(field_state.get("field_areal_coherence_mean", 0.0) or 0.0),
        "field_areal_conflict_mean": float(field_state.get("field_areal_conflict_mean", 0.0) or 0.0),
        "field_topology_coherence": float(field_state.get("field_topology_coherence", 0.0) or 0.0),
        "field_topology_tension": float(field_state.get("field_topology_tension", 0.0) or 0.0),
        "neural_felt_bearing": float(field_state.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", 0.0)) or 0.0),
        "neural_felt_pressure": float(field_state.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", 0.0)) or 0.0),
        "neural_felt_memory_resonance": float(neural_felt_state.get("neural_felt_memory_resonance", 0.0) or 0.0),
        "neural_felt_context_reactivation": float(neural_felt_state.get("neural_felt_context_reactivation", 0.0) or 0.0),
        "neural_felt_label": str(field_state.get("neural_felt_label", neural_felt_state.get("neural_felt_label", "quiet_neural_felt")) or "quiet_neural_felt"),
    }

    prior_entry = dict(prior_history[-1] or {}) if prior_history else {}
    entry["delta_field_pressure"] = float(entry.get("field_pressure", 0.0) - float(prior_entry.get("field_pressure", entry.get("field_pressure", 0.0)) or 0.0))
    entry["delta_neural_felt_bearing"] = float(entry.get("neural_felt_bearing", 0.0) - float(prior_entry.get("neural_felt_bearing", entry.get("neural_felt_bearing", 0.0)) or 0.0))
    entry["delta_topology_tension"] = float(entry.get("field_topology_tension", 0.0) - float(prior_entry.get("field_topology_tension", entry.get("field_topology_tension", 0.0)) or 0.0))
    entry["delta_memory_resonance"] = float(entry.get("neural_felt_memory_resonance", 0.0) - float(prior_entry.get("neural_felt_memory_resonance", entry.get("neural_felt_memory_resonance", 0.0)) or 0.0))

    history = list((prior_history + [dict(entry or {})])[-limit:])

    def _history_trend(key):
        if len(history) < 2:
            return 0.0

        start_value = float((history[0] or {}).get(key, 0.0) or 0.0)
        end_value = float((history[-1] or {}).get(key, 0.0) or 0.0)
        return float(max(-1.0, min(1.0, end_value - start_value)))

    pressure_trend = _history_trend("field_pressure")
    bearing_trend = _history_trend("neural_felt_bearing")
    topology_tension_trend = _history_trend("field_topology_tension")
    memory_resonance_trend = _history_trend("neural_felt_memory_resonance")

    if pressure_trend >= 0.08 and topology_tension_trend >= 0.05:
        history_label = "rising_field_tension"
    elif bearing_trend >= 0.08 and pressure_trend <= 0.04:
        history_label = "recovering_field_bearing"
    elif abs(pressure_trend) <= 0.03 and abs(bearing_trend) <= 0.03 and abs(topology_tension_trend) <= 0.03:
        history_label = "stable_field_trace"
    else:
        history_label = "moving_field_trace"

    history_state = {
        "inner_field_history": [dict(item or {}) for item in list(history or []) if isinstance(item, dict)],
        "inner_field_history_length": int(len(history)),
        "inner_field_pressure_trend": float(pressure_trend),
        "inner_field_bearing_trend": float(bearing_trend),
        "inner_field_topology_tension_trend": float(topology_tension_trend),
        "inner_field_memory_resonance_trend": float(memory_resonance_trend),
        "inner_field_history_label": str(history_label),
    }

    if bot is not None:
        bot.inner_field_history = list(history_state.get("inner_field_history", []) or [])
        bot.inner_field_history_state = dict(history_state or {})

    return dict(history_state or {})

# --------------------------------------------------
# update signature memory
# --------------------------------------------------
def update_signature_memory(bot, state_signature, outcome=None):

    if bot is None:
        return None

    signature = dict(state_signature or {})
    signature_key = str(signature.get("signature_key", "") or "").strip()
    signature_vector = list(signature.get("signature_vector", []) or [])

    if not signature_key:
        return None

    if not isinstance(getattr(bot, "signature_memory", None), dict):
        bot.signature_memory = {}

    updated_memory = {}

    for key, item in dict(getattr(bot, "signature_memory", {}) or {}).items():
        if not isinstance(item, dict):
            continue

        aged_item = {
            "seen": int(item.get("seen", 0) or 0),
            "tp": int(item.get("tp", 0) or 0),
            "sl": int(item.get("sl", 0) or 0),
            "cancel": int(item.get("cancel", 0) or 0),
            "timeout": int(item.get("timeout", 0) or 0),
            "score": float(item.get("score", 0.0) or 0.0) * 0.995,
            "last_outcome": item.get("last_outcome"),
            "age": int(item.get("age", 0) or 0) + 1,
            "signature_vector": list(item.get("signature_vector", []) or []),
        }

        if aged_item["age"] <= 250 or abs(float(aged_item["score"])) >= 0.18:
            updated_memory[str(key)] = aged_item

    bot.signature_memory = updated_memory

    memory = bot.signature_memory.get(signature_key)
    if not isinstance(memory, dict):
        memory = {
            "seen": 0,
            "tp": 0,
            "sl": 0,
            "cancel": 0,
            "timeout": 0,
            "score": 0.0,
            "last_outcome": None,
            "age": 0,
            "signature_vector": list(signature_vector),
        }

    memory["seen"] = int(memory.get("seen", 0) or 0) + 1
    memory["age"] = 0

    if signature_vector:
        memory["signature_vector"] = list(signature_vector)

    reason = str(outcome or "").strip().lower()

    if reason == "tp_hit":
        memory["tp"] = int(memory.get("tp", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) + 1.00
        memory["last_outcome"] = "tp_hit"

    elif reason == "sl_hit":
        memory["sl"] = int(memory.get("sl", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 1.10
        memory["last_outcome"] = "sl_hit"

    elif reason == "cancel":
        memory["cancel"] = int(memory.get("cancel", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 0.35
        memory["last_outcome"] = "cancel"

    elif reason == "timeout":
        memory["timeout"] = int(memory.get("timeout", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 0.28
        memory["last_outcome"] = "timeout"

    elif reason == "reward_too_small":
        memory["cancel"] = int(memory.get("cancel", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 0.40
        memory["last_outcome"] = "reward_too_small"

    elif reason == "sl_distance_too_high":
        memory["sl"] = int(memory.get("sl", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 0.62
        memory["last_outcome"] = "sl_distance_too_high"

    elif reason == "rr_too_low":
        memory["timeout"] = int(memory.get("timeout", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 0.48
        memory["last_outcome"] = "rr_too_low"

    memory["score"] = float(max(-6.0, min(6.0, memory["score"])))

    bot.signature_memory[signature_key] = memory
    bot.last_signature_key = signature_key

    if reason:
        bot.last_signature_outcome = reason

    if len(bot.signature_memory) > 180:
        sorted_items = sorted(
            bot.signature_memory.items(),
            key=lambda item: (
                abs(float((item[1] or {}).get("score", 0.0) or 0.0)),
                -int((item[1] or {}).get("age", 0) or 0),
                int((item[1] or {}).get("seen", 0) or 0),
            ),
            reverse=True,
        )[:180]
        bot.signature_memory = dict(sorted_items)

    return {
        "signature_key": signature_key,
        "seen": int(memory.get("seen", 0) or 0),
        "tp": int(memory.get("tp", 0) or 0),
        "sl": int(memory.get("sl", 0) or 0),
        "cancel": int(memory.get("cancel", 0) or 0),
        "timeout": int(memory.get("timeout", 0) or 0),
        "score": float(memory.get("score", 0.0) or 0.0),
        "age": int(memory.get("age", 0) or 0),
        "last_outcome": memory.get("last_outcome"),
        "signature_vector": list(memory.get("signature_vector", []) or []),
    }

# --------------------------------------------------
# lookup signature context
# --------------------------------------------------
def lookup_signature_context(bot, state_signature):

    if bot is None:
        return None

    signature_key = str((state_signature or {}).get("signature_key", "") or "").strip()
    signature_vector = list((state_signature or {}).get("signature_vector", []) or [])

    if not signature_key or not signature_vector:
        return None

    signature_memory = getattr(bot, "signature_memory", None)
    if not isinstance(signature_memory, dict) or not signature_memory:
        return None

    nearest_key = None
    nearest_item = None
    nearest_distance = None

    current_vector = np.asarray(signature_vector, dtype=float)

    for key, item in signature_memory.items():
        if not isinstance(item, dict):
            continue

        candidate_vector = list(item.get("signature_vector", []) or [])
        if not candidate_vector:
            continue

        if len(candidate_vector) != len(signature_vector):
            continue

        candidate_array = np.asarray(candidate_vector, dtype=float)
        distance = float(np.mean(np.abs(current_vector - candidate_array)))

        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_key = str(key)
            nearest_item = item

    if nearest_item is None or nearest_distance is None:
        return None

    if nearest_distance > 0.34:
        return None

    return {
        "signature_key": str(nearest_key),
        "distance": float(nearest_distance),
        "seen": int(nearest_item.get("seen", 0) or 0),
        "tp": int(nearest_item.get("tp", 0) or 0),
        "sl": int(nearest_item.get("sl", 0) or 0),
        "cancel": int(nearest_item.get("cancel", 0) or 0),
        "timeout": int(nearest_item.get("timeout", 0) or 0),
        "score": float(nearest_item.get("score", 0.0) or 0.0),
        "age": int(nearest_item.get("age", 0) or 0),
        "last_outcome": nearest_item.get("last_outcome"),
    }

# --------------------------------------------------
# ENTRY API
# --------------------------------------------------
def reinterpret_focus_by_signature(bot, fused, state_signature):

    if bot is None:
        return dict(fused or {})

    result = dict(fused or {})
    signature_context = lookup_signature_context(bot, state_signature)
    cluster_context = lookup_context_cluster(bot, state_signature)

    result["signature_bias"] = 0.0
    result["signature_block"] = False
    result["signature_caution_modulation"] = False
    result["signature_key"] = "-"
    result["signature_quality"] = 0.0
    result["signature_distance"] = 0.0
    result["context_cluster_id"] = "-"
    result["context_cluster_bias"] = 0.0
    result["context_cluster_quality"] = 0.0
    result["context_cluster_distance"] = 0.0
    result["context_cluster_block"] = False
    result["context_cluster_caution_modulation"] = False
    result["experience_attention_bias"] = 0.0
    result["experience_caution_bias"] = 0.0
    result["experience_conviction_bias"] = 0.0
    memory_complexity_state = {
        "memory_compare_load": 0.0,
        "memory_match_count": 0,
        "memory_support": 0.0,
        "memory_inhibition": 0.0,
        "memory_conflict": 0.0,
        "thinking_complexity": 0.0,
        "cognitive_load": 0.0,
        "decision_energy_cost": 0.0,
        "memory_effect_on_phase": "neutral",
        "context_cluster_negative_source": "-",
        "context_cluster_id": "-",
        "context_cluster_seen": 0,
        "context_cluster_score": 0.0,
        "context_cluster_hit_ratio": 0.0,
        "context_cluster_loss_ratio": 0.0,
        "context_cluster_cancel_timeout_ratio": 0.0,
        "context_cluster_negative_evidence": "-",
        "context_cluster_quality": 0.0,
        "context_cluster_distance": 0.0,
        "context_cluster_trust": 0.0,
        "context_cluster_variance": 0.0,
        "signature_key": "-",
        "signature_seen": 0,
        "signature_score": 0.0,
        "signature_hit_ratio": 0.0,
        "signature_quality": 0.0,
        "signature_distance": 0.0,
    }

    long_score = float(result.get("long_score", 0.0) or 0.0)
    short_score = float(result.get("short_score", 0.0) or 0.0)

    if isinstance(signature_context, dict):
        memory_complexity_state["memory_match_count"] = int(memory_complexity_state.get("memory_match_count", 0) or 0) + 1
        score = float(signature_context.get("score", 0.0) or 0.0)
        seen = int(signature_context.get("seen", 0) or 0)
        tp_hits = int(signature_context.get("tp", 0) or 0)
        sl_hits = int(signature_context.get("sl", 0) or 0)
        cancel_hits = int(signature_context.get("cancel", 0) or 0)
        timeout_hits = int(signature_context.get("timeout", 0) or 0)
        distance = float(signature_context.get("distance", 0.0) or 0.0)
        resolved = max(1, tp_hits + sl_hits + cancel_hits + timeout_hits)
        hit_ratio = tp_hits / float(resolved)
        memory_complexity_state.update({
            "signature_key": str(signature_context.get("signature_key", "-") or "-"),
            "signature_seen": int(seen),
            "signature_score": float(score),
            "signature_hit_ratio": float(hit_ratio),
            "signature_distance": float(distance),
        })

        if seen >= 3:
            quality = (
                score * 0.10
                + (hit_ratio - 0.50) * 0.35
                - (max(0, sl_hits - tp_hits) * 0.04)
                - (distance * 0.30)
            )
            bias = max(-0.28, min(0.28, quality))
            result["experience_attention_bias"] += float(max(0.0, quality) * 0.36)
            result["experience_caution_bias"] += float(max(0.0, -quality) * 0.42)
            result["experience_conviction_bias"] += float(bias * 0.55)
            memory_complexity_state["signature_quality"] = float(quality)
            memory_complexity_state["memory_support"] = float(memory_complexity_state.get("memory_support", 0.0) or 0.0) + max(0.0, quality) * 0.36
            memory_complexity_state["memory_inhibition"] = float(memory_complexity_state.get("memory_inhibition", 0.0) or 0.0) + max(0.0, -quality) * 0.42

            if float(getattr(bot, "focus_point", 0.0) or 0.0) >= 0.0:
                long_score += bias
                short_score -= max(0.0, bias * 0.45)
            else:
                short_score += bias
                long_score -= max(0.0, bias * 0.45)

            result["signature_bias"] = float(bias)
            result["signature_quality"] = float(quality)

            if score <= -2.20 or (seen >= 5 and hit_ratio <= 0.18):
                result["reject_reason"] = "signature_negative_modulation"
                result["signature_block"] = False
                result["signature_caution_modulation"] = True
                result["experience_caution_bias"] += 0.18
                memory_complexity_state["memory_inhibition"] = float(memory_complexity_state.get("memory_inhibition", 0.0) or 0.0) + 0.18

            bot.last_signature_context = {
                "signature_key": str(signature_context.get("signature_key", "-") or "-"),
                "distance": float(distance),
                "quality": float(quality),
                "score": float(score),
            }

        result["signature_key"] = str(signature_context.get("signature_key", "-") or "-")
        result["signature_distance"] = float(distance)

    if isinstance(cluster_context, dict):
        memory_complexity_state["memory_match_count"] = int(memory_complexity_state.get("memory_match_count", 0) or 0) + 1
        cluster_score = float(cluster_context.get("score", 0.0) or 0.0)
        cluster_seen = int(cluster_context.get("seen", 0) or 0)
        cluster_tp = int(cluster_context.get("tp", 0) or 0)
        cluster_sl = int(cluster_context.get("sl", 0) or 0)
        cluster_cancel = int(cluster_context.get("cancel", 0) or 0)
        cluster_timeout = int(cluster_context.get("timeout", 0) or 0)
        cluster_distance = float(cluster_context.get("distance", 0.0) or 0.0)
        cluster_trust = float(cluster_context.get("trust", 0.0) or 0.0)
        cluster_variance = float(cluster_context.get("variance", 0.0) or 0.0)
        cluster_resolved = max(1, cluster_tp + cluster_sl + cluster_cancel + cluster_timeout)
        cluster_hit_ratio = cluster_tp / float(cluster_resolved)
        cluster_trade_resolved = max(1, cluster_tp + cluster_sl)
        cluster_loss_ratio = cluster_sl / float(cluster_trade_resolved)
        cluster_cancel_timeout_ratio = (cluster_cancel + cluster_timeout) / float(cluster_resolved)
        memory_complexity_state.update({
            "context_cluster_id": str(cluster_context.get("cluster_id", "-") or "-"),
            "context_cluster_seen": int(cluster_seen),
            "context_cluster_score": float(cluster_score),
            "context_cluster_hit_ratio": float(cluster_hit_ratio),
            "context_cluster_loss_ratio": float(cluster_loss_ratio),
            "context_cluster_cancel_timeout_ratio": float(cluster_cancel_timeout_ratio),
            "context_cluster_distance": float(cluster_distance),
            "context_cluster_trust": float(cluster_trust),
            "context_cluster_variance": float(cluster_variance),
        })

        cluster_quality = (
            (cluster_score * 0.08)
            + ((cluster_trust - 0.50) * 0.34)
            - (cluster_distance * 0.24)
            - (cluster_variance * 0.18)
        )

        result["experience_attention_bias"] += float(max(0.0, cluster_quality) * 0.28)
        result["experience_caution_bias"] += float(max(0.0, -cluster_quality) * 0.30)
        result["experience_conviction_bias"] += float(max(-0.22, min(0.22, cluster_quality * 0.45)))
        memory_complexity_state["memory_support"] = float(memory_complexity_state.get("memory_support", 0.0) or 0.0) + max(0.0, cluster_quality) * 0.28
        memory_complexity_state["memory_inhibition"] = float(memory_complexity_state.get("memory_inhibition", 0.0) or 0.0) + max(0.0, -cluster_quality) * 0.30

        if cluster_seen >= 3:
            cluster_quality = (
                cluster_score * 0.08
                + (cluster_hit_ratio - 0.50) * 0.42
                + (cluster_trust * 0.18)
                - (cluster_distance * 0.34)
                - (cluster_variance * 0.08)
            )
            cluster_bias = max(-0.24, min(0.24, cluster_quality))

            if float(getattr(bot, "focus_point", 0.0) or 0.0) >= 0.0:
                long_score += cluster_bias
                short_score -= max(0.0, cluster_bias * 0.40)
            else:
                short_score += cluster_bias
                long_score -= max(0.0, cluster_bias * 0.40)

            result["context_cluster_bias"] = float(cluster_bias)
            result["context_cluster_quality"] = float(cluster_quality)
            memory_complexity_state["context_cluster_quality"] = float(cluster_quality)

            score_confirms_negative = cluster_score <= -2.60
            loss_confirms_negative = (
                cluster_seen >= 6
                and cluster_hit_ratio <= 0.16
                and cluster_sl >= 3
                and cluster_loss_ratio >= 0.68
                and cluster_score <= -1.20
            )
            if score_confirms_negative:
                memory_complexity_state["context_cluster_negative_evidence"] = "score_confirms"
            elif loss_confirms_negative:
                memory_complexity_state["context_cluster_negative_evidence"] = "loss_confirms"
            elif cluster_seen >= 6 and cluster_hit_ratio <= 0.16:
                memory_complexity_state["context_cluster_negative_evidence"] = "low_hit_caution"

            if score_confirms_negative or loss_confirms_negative:
                result["reject_reason"] = "context_cluster_negative_modulation"
                result["context_cluster_block"] = False
                result["context_cluster_caution_modulation"] = True
                result["experience_caution_bias"] += 0.20
                memory_complexity_state["memory_inhibition"] = float(memory_complexity_state.get("memory_inhibition", 0.0) or 0.0) + 0.20
                if score_confirms_negative and loss_confirms_negative:
                    memory_complexity_state["context_cluster_negative_source"] = "mixed"
                elif score_confirms_negative:
                    memory_complexity_state["context_cluster_negative_source"] = "cluster_score"
                elif loss_confirms_negative:
                    memory_complexity_state["context_cluster_negative_source"] = "low_hit_ratio"

        result["context_cluster_id"] = str(cluster_context.get("cluster_id", "-") or "-")
        result["context_cluster_distance"] = float(cluster_distance)

    memory_support = max(0.0, min(1.0, float(memory_complexity_state.get("memory_support", 0.0) or 0.0)))
    memory_inhibition = max(0.0, min(1.0, float(memory_complexity_state.get("memory_inhibition", 0.0) or 0.0)))
    memory_conflict = max(0.0, min(1.0, min(memory_support, memory_inhibition) * 1.6))
    match_count = int(memory_complexity_state.get("memory_match_count", 0) or 0)
    compare_load = max(0.0, min(1.0, match_count / 2.0))
    thinking_complexity = max(0.0, min(1.0, (compare_load * 0.34) + (memory_conflict * 0.28) + (memory_inhibition * 0.22) + (abs(float(result.get("experience_conviction_bias", 0.0) or 0.0)) * 0.16)))
    cognitive_load = max(0.0, min(1.0, (thinking_complexity * 0.55) + (memory_inhibition * 0.28) + (memory_conflict * 0.17)))
    decision_energy_cost = max(0.0, min(1.0, (cognitive_load * 0.50) + (compare_load * 0.22) + (float(getattr(bot, "experience_regulation", 0.0) or 0.0) * 0.14) + (float(getattr(bot, "reflection_maturity", 0.0) or 0.0) * 0.14)))
    if bool(result.get("context_cluster_caution_modulation", False)) or bool(result.get("signature_caution_modulation", False)):
        memory_effect = "caution_modulation"
    elif memory_conflict >= 0.18:
        memory_effect = "conflict"
    elif memory_inhibition > memory_support + 0.04:
        memory_effect = "inhibit"
    elif memory_support > memory_inhibition + 0.04:
        memory_effect = "support"
    elif match_count > 0:
        memory_effect = "neutral_match"
    else:
        memory_effect = "no_match"
    memory_complexity_state.update({
        "memory_support": float(memory_support),
        "memory_inhibition": float(memory_inhibition),
        "memory_conflict": float(memory_conflict),
        "memory_compare_load": float(compare_load),
        "thinking_complexity": float(thinking_complexity),
        "cognitive_load": float(cognitive_load),
        "decision_energy_cost": float(decision_energy_cost),
        "memory_effect_on_phase": str(memory_effect),
    })
    result["memory_complexity_state"] = dict(memory_complexity_state or {})
    setattr(bot, "last_memory_complexity_state", dict(memory_complexity_state or {}))

    result["long_score"] = float(long_score)
    result["short_score"] = float(short_score)
    return result

# --------------------------------------------------
# felt_state
# --------------------------------------------------
def build_felt_state(bot, candle_state, stimulus, snapshot, perception_state, decision="WAIT", processing_state=None, expectation_state=None, inner_field_perception_state=None):

    return resolve_felt_state(
        bot,
        candle_state,
        stimulus,
        snapshot,
        perception_state,
        decision=decision,
        processing_state=processing_state,
        expectation_state=expectation_state,
        inner_field_perception_state=inner_field_perception_state,
        expectation_builder=update_expectation_pressure_state,
        neural_felt_builder=_build_neural_felt_state,
    )

# --------------------------------------------------
# meta_regulation_state
# --------------------------------------------------
from core.neurochemistry import build_neurochemical_state

from core.mcm_field import build_active_mcm_contact_state

from core.decision_regulation import build_meta_regulation_state, build_thought_state
from core.runtime_tendency import build_runtime_decision_tendency_view, build_runtime_entry_decision_view
from core.runtime_snapshot import build_runtime_decision_state, build_runtime_pipeline_snapshot as _build_runtime_pipeline_snapshot_impl, build_runtime_snapshot_state, merge_active_context_signal
from core.runtime_commit import advance_runtime_perception_layers, build_internal_episode_state, build_visible_episode_state, commit_runtime_episode_state, commit_runtime_snapshot_state, refresh_runtime_context_state

def register_pending_learning_context(bot, state_signature):

    if bot is None:
        return None

    signature = dict(state_signature or {})
    signature_key = str(signature.get("signature_key", "") or "").strip()

    if not signature_key:
        return None

    bot.last_signature_key = signature_key
    bot.last_signature_context = dict(signature)
    bot.last_signature_outcome = None

    cluster_context = lookup_context_cluster(bot, signature)
    cluster_id = None

    if isinstance(cluster_context, dict):
        cluster_id = str(cluster_context.get("cluster_id", "") or "").strip()

    bot.last_context_cluster_id = cluster_id or None
    bot.last_context_cluster_key = str(signature_key)

    return {
        "signature_key": str(signature_key),
        "context_cluster_id": cluster_id or None,
    }

# --------------------------------------------------
# commit pending learning context
# --------------------------------------------------
def commit_pending_learning_context(bot, outcome=None):

    if bot is None:
        return None

    signature_context = dict(getattr(bot, "last_signature_context", {}) or {})
    signature_key = str(getattr(bot, "last_signature_key", "") or "").strip()

    if not signature_context and signature_key:
        signature_context = {
            "signature_key": str(signature_key),
        }

    if not signature_context:
        return None

    signature_result = update_signature_memory(
        bot,
        signature_context,
        outcome=outcome,
    )

    cluster_result = classify_state_cluster(
        bot,
        signature_context,
    )

    if isinstance(cluster_result, dict):
        cluster_id = str(cluster_result.get("cluster_id", "") or "").strip()

        if cluster_id:
            update_context_cluster_outcome(
                bot,
                cluster_id,
                outcome=outcome,
            )

    merge_similar_signatures(bot)
    split_unstable_cluster(bot)

    return {
        "signature_key": str(getattr(bot, "last_signature_key", "") or "").strip() or None,
        "context_cluster_id": str(getattr(bot, "last_context_cluster_id", "") or "").strip() or None,
        "signature_result": dict(signature_result or {}),
        "cluster_result": dict(cluster_result or {}),
    }

# --------------------------------------------------
# ENTRY API
# --------------------------------------------------
def _compute_runtime_entry_result(window, candle_state, bot=None, visual_market_state=None, structure_perception_state=None, temporal_perception_state=None):

    if not window:
        return None

    tension_state = build_tension_state_from_window(window)
    visual_market_state = dict(visual_market_state or {})
    structure_perception_state = dict(structure_perception_state or {})
    temporal_perception_state = dict(temporal_perception_state or {})

    energy = float(tension_state.get("energy", 0.0) or 0.0)
    coherence = float(tension_state.get("coherence", 0.0) or 0.0)
    asymmetry = int(tension_state.get("asymmetry", 0) or 0)
    coh_zone = float(tension_state.get("coh_zone", 0.0) or 0.0)

    if not bool(getattr(Config, "MCM_ENABLED", True)):
        return None

    if bot is None:
        return None

    if getattr(bot, "mcm_brain", None) is None:
        bot.mcm_brain = create_mcm_brain()

    pause_left = int(getattr(bot, "mcm_pause_left", 0) or 0)
    pause_mode = pause_left > 0

    stimulus = build_mcm_stimulus(
        candle_state,
        tension_state,
        pause_mode=pause_mode,
        bot=bot,
        visual_market_state=visual_market_state,
    )
    snapshot = step_mcm_brain(bot.mcm_brain, stimulus, mode="market")

    bot.mcm_last_state = dict(snapshot)
    bot.mcm_last_action = str(snapshot.get("self_state", "stable"))
    bot.mcm_last_attractor = str(snapshot.get("attractor", "neutral"))
    bot.mcm_snapshot = dict(snapshot)
    field_state = _derive_runtime_field_state(
        bot=bot,
        tension_state=tension_state,
        snapshot=snapshot,
    )

    update_target_model(
        bot,
        candle_state,
        dict(stimulus.get("focus", {}) or {}),
    )

    neural_state = build_neural_modulation(
        bot,
        stimulus,
    )

    fused_preview = resolve_fused_decision(
        candle_state,
        tension_state,
        snapshot,
        bot=bot,
        temporal_perception_state=temporal_perception_state,
    )

    entry_state_stack = build_runtime_entry_state_stack(
        bot=bot,
        window=window,
        candle_state=candle_state,
        tension_state=tension_state,
        stimulus=stimulus,
        snapshot=snapshot,
        fused_preview=fused_preview,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        temporal_perception_state=temporal_perception_state,
        pause_mode=pause_mode,
        visual_builder=build_visual_market_state,
        structure_engine=STRUCTURE_ENGINE,
        world_state_builder=build_world_state,
        outer_visual_builder=build_outer_visual_perception_state,
        inner_field_builder=build_inner_field_perception_state,
        perception_builder=build_perception_state,
        processing_builder=build_processing_state,
        expectation_builder=update_expectation_pressure_state,
        felt_builder=build_felt_state,
        form_symbol_builder=build_form_symbol_state,
        state_signature_builder=build_state_signature,
        temporal_builder=build_temporal_coherence_state,
        active_context_refresher=_refresh_active_context_trace,
        pending_learning_register=register_pending_learning_context,
        signature_reinterpreter=reinterpret_focus_by_signature,
        thought_builder=build_thought_state,
        meta_regulation_builder=build_meta_regulation_state,
        review_feedback_resolver=_resolve_review_decision_feedback,
        strategic_window_builder=build_strategic_window_state,
        active_contact_builder=build_active_mcm_contact_state,
    )
    visual_market_state = entry_state_stack["visual_market_state"]
    structure_perception_state = entry_state_stack["structure_perception_state"]
    temporal_perception_state = entry_state_stack["temporal_perception_state"]
    world_state = entry_state_stack["world_state"]
    outer_visual_perception_state = entry_state_stack["outer_visual_perception_state"]
    inner_field_perception_state = entry_state_stack["inner_field_perception_state"]
    perception_state = entry_state_stack["perception_state"]
    processing_state = entry_state_stack["processing_state"]
    expectation_state = entry_state_stack["expectation_state"]
    felt_state = entry_state_stack["felt_state"]
    form_symbol_state = entry_state_stack["form_symbol_state"]
    state_signature = entry_state_stack["state_signature"]
    early_active_context_trace = entry_state_stack["early_active_context_trace"]
    fused = entry_state_stack["fused"]
    thought_state = entry_state_stack["thought_state"]
    meta_regulation_state = entry_state_stack["meta_regulation_state"]
    review_feedback_state = entry_state_stack["review_feedback_state"]
    strategic_window_state = entry_state_stack["strategic_window_state"]
    area_perception_profile = entry_state_stack.get("area_perception_profile", {}) or {}
    active_mcm_contact_state = entry_state_stack["active_mcm_contact_state"]

    decision = str(meta_regulation_state.get("decision", fused.get("decision", "WAIT")) or "WAIT")

    field_metrics = build_runtime_field_metrics(field_state)
    virtual_observation_plan = build_virtual_observation_plan(
        decision=decision,
        candle_state=candle_state,
        fused=fused,
        stimulus=stimulus,
        snapshot=snapshot,
        bot=bot,
        strategic_window_state=strategic_window_state,
        form_symbol_state=form_symbol_state,
        thought_state=thought_state,
        derive_trade_plan_from_brain=derive_trade_plan_from_brain,
    )

    if not bool(meta_regulation_state.get("allow_plan", False)):
        result = build_runtime_no_plan_result(
            decision=decision,
            virtual_observation_plan=virtual_observation_plan,
            energy=energy,
            coherence=coherence,
            asymmetry=asymmetry,
            coh_zone=coh_zone,
            snapshot=snapshot,
            stimulus=stimulus,
            world_state=world_state,
            structure_perception_state=structure_perception_state,
            temporal_perception_state=temporal_perception_state,
            outer_visual_perception_state=outer_visual_perception_state,
            inner_field_perception_state=inner_field_perception_state,
            processing_state=processing_state,
            perception_state=perception_state,
            felt_state=felt_state,
            thought_state=thought_state,
            meta_regulation_state=meta_regulation_state,
            expectation_state=expectation_state,
            form_symbol_state=form_symbol_state,
            strategic_window_state=strategic_window_state,
            area_perception_profile=area_perception_profile,
            active_mcm_contact_state=active_mcm_contact_state,
            early_active_context_trace=early_active_context_trace,
            state_signature=state_signature,
            fused=fused,
            neural_state=neural_state,
            review_feedback_state=review_feedback_state,
        )
        record_runtime_entry_result_protocol(
            bot,
            result,
            meta_regulation_state=meta_regulation_state,
            processing_state=processing_state,
            felt_state=felt_state,
            thought_state=thought_state,
            record_field_decision_protocol=_record_field_decision_protocol,
            record_strategic_window_protocol=_record_strategic_window_protocol,
            record_active_mcm_contact_protocol=_record_active_mcm_contact_protocol,
        )
        return result

    if decision not in ("LONG", "SHORT"):
        record_runtime_entry_rejection_protocol(
            bot,
            decision=decision,
            rejection_reason="decision_not_tradeable",
            meta_regulation_state=meta_regulation_state,
            processing_state=processing_state,
            felt_state=felt_state,
            thought_state=thought_state,
            fused=fused,
            form_symbol_state=form_symbol_state,
            strategic_window_state=strategic_window_state,
            area_perception_profile=area_perception_profile,
            active_mcm_contact_state=active_mcm_contact_state,
            early_active_context_trace=early_active_context_trace,
            record_field_decision_protocol=_record_field_decision_protocol,
            record_strategic_window_protocol=_record_strategic_window_protocol,
            record_active_mcm_contact_protocol=_record_active_mcm_contact_protocol,
        )
        return None

    prices = derive_trade_plan_from_brain(
        decision,
        candle_state,
        fused,
        stimulus,
        snapshot,
        bot=bot,
        strategic_window_state=strategic_window_state,
        form_symbol_state=form_symbol_state,
        thought_state=thought_state,
    )

    if prices is None:
        record_runtime_entry_rejection_protocol(
            bot,
            decision=decision,
            rejection_reason="trade_plan_missing",
            meta_regulation_state=meta_regulation_state,
            processing_state=processing_state,
            felt_state=felt_state,
            thought_state=thought_state,
            fused=fused,
            form_symbol_state=form_symbol_state,
            strategic_window_state=strategic_window_state,
            area_perception_profile=area_perception_profile,
            active_mcm_contact_state=active_mcm_contact_state,
            early_active_context_trace=early_active_context_trace,
            record_field_decision_protocol=_record_field_decision_protocol,
            record_strategic_window_protocol=_record_strategic_window_protocol,
            record_active_mcm_contact_protocol=_record_active_mcm_contact_protocol,
        )
        return None

    prices = synchronize_entry_choice_prices(
        prices,
        decision=decision,
        candle_state=candle_state,
        fused=fused,
        stimulus=stimulus,
        snapshot=snapshot,
        bot=bot,
        strategic_window_state=strategic_window_state,
        form_symbol_state=form_symbol_state,
        derive_trade_plan_from_brain=derive_trade_plan_from_brain,
    )

    hypothesis_reality_state = str(prices.get("hypothesis_reality_state", "") or "")
    hypothesis_binding_state = str(prices.get("hypothesis_reality_binding_state", "") or "")
    try:
        hypothesis_observation_pressure = float(prices.get("hypothesis_observation_pressure", 0.0) or 0.0)
    except Exception:
        hypothesis_observation_pressure = 0.0
    try:
        hypothesis_reality_bearing = float(prices.get("hypothesis_reality_bearing", 0.0) or 0.0)
    except Exception:
        hypothesis_reality_bearing = 0.0
    observation_dominates_hypothesis = False
    if observation_dominates_hypothesis:
        observation_meta = {
            **dict(meta_regulation_state or {}),
            "rejection_reason": "hypothesis_requires_reality_observation",
        }
        result = build_runtime_no_plan_result(
            decision=decision,
            virtual_observation_plan=prices,
            energy=energy,
            coherence=coherence,
            asymmetry=asymmetry,
            coh_zone=coh_zone,
            snapshot=snapshot,
            stimulus=stimulus,
            world_state=world_state,
            structure_perception_state=structure_perception_state,
            temporal_perception_state=temporal_perception_state,
            outer_visual_perception_state=outer_visual_perception_state,
            inner_field_perception_state=inner_field_perception_state,
            processing_state=processing_state,
            perception_state=perception_state,
            felt_state=felt_state,
            thought_state=thought_state,
            meta_regulation_state=observation_meta,
            expectation_state=expectation_state,
            form_symbol_state=form_symbol_state,
            strategic_window_state=strategic_window_state,
            area_perception_profile=area_perception_profile,
            active_mcm_contact_state=active_mcm_contact_state,
            early_active_context_trace=early_active_context_trace,
            state_signature=state_signature,
            fused=fused,
            neural_state=neural_state,
            review_feedback_state=review_feedback_state,
        )
        result.update(
            {
                "decision_tendency": "observe",
                "hypothesis_role": "thought_reality_probe",
                "hypothesis_reality_state": str(hypothesis_reality_state),
                "hypothesis_reality_binding_state": str(hypothesis_binding_state),
                "hypothesis_observation_pressure": float(hypothesis_observation_pressure),
                "hypothesis_reality_bearing": float(hypothesis_reality_bearing),
                "hypothesis_action_support": float(hypothesis_reality_bearing),
                "hypothesis_observation_reason": "open_structure_needs_mcm_feeling",
                "entry_mode": str(prices.get("entry_mode", result.get("entry_mode", "area_contact_entry")) or "area_contact_entry"),
                "entry_contact_state": str(prices.get("entry_contact_state", prices.get("entry_choice_state", "area_contact_preferred")) or "area_contact_preferred"),
                "entry_geometry_state": str(prices.get("entry_geometry_state", "entry_geometry_observed") or "entry_geometry_observed"),
                "pre_entry_emergent_structure_state": str(prices.get("pre_entry_emergent_structure_state", "") or ""),
                "pre_entry_emergent_structure_reading": float(prices.get("pre_entry_emergent_structure_reading", 0.0) or 0.0),
                "pre_entry_emergent_structure_confirmation": float(prices.get("pre_entry_emergent_structure_confirmation", 0.0) or 0.0),
                "visual_reality_bearing": float(prices.get("visual_reality_bearing", 0.0) or 0.0),
                "felt_reality_bearing": float(prices.get("felt_reality_bearing", 0.0) or 0.0),
                "thought_reality_bearing": float(prices.get("thought_reality_bearing", 0.0) or 0.0),
                "form_mcm_reality_fit": float(prices.get("form_mcm_reality_fit", 0.0) or 0.0),
                "uncoupled_area_contact_pressure": float(prices.get("uncoupled_area_contact_pressure", 0.0) or 0.0),
            }
        )
        record_runtime_entry_result_protocol(
            bot,
            result,
            meta_regulation_state=observation_meta,
            processing_state=processing_state,
            felt_state=felt_state,
            thought_state=thought_state,
            record_field_decision_protocol=_record_field_decision_protocol,
            record_strategic_window_protocol=_record_strategic_window_protocol,
            record_active_mcm_contact_protocol=_record_active_mcm_contact_protocol,
        )
        return result

    result = build_runtime_entry_trade_result(
        decision=decision,
        prices=prices,
        energy=energy,
        coherence=coherence,
        asymmetry=asymmetry,
        coh_zone=coh_zone,
        snapshot=snapshot,
        stimulus=stimulus,
        world_state=world_state,
        structure_perception_state=structure_perception_state,
        temporal_perception_state=temporal_perception_state,
        outer_visual_perception_state=outer_visual_perception_state,
        inner_field_perception_state=inner_field_perception_state,
        processing_state=processing_state,
        perception_state=perception_state,
        felt_state=felt_state,
        thought_state=thought_state,
        meta_regulation_state=meta_regulation_state,
        expectation_state=expectation_state,
        form_symbol_state=form_symbol_state,
        strategic_window_state=strategic_window_state,
        area_perception_profile=area_perception_profile,
        active_mcm_contact_state=active_mcm_contact_state,
        early_active_context_trace=early_active_context_trace,
        state_signature=state_signature,
        fused=fused,
        neural_state=neural_state,
        review_feedback_state=review_feedback_state,
        field_stimulus_density=field_metrics["field_stimulus_density"],
        field_density=field_metrics["field_density"],
        field_stability=field_metrics["field_stability"],
        regulatory_load=field_metrics["regulatory_load"],
        action_capacity=field_metrics["action_capacity"],
        recovery_need=field_metrics["recovery_need"],
        survival_pressure=field_metrics["survival_pressure"],
    )

    result = synchronize_entry_choice_result(
        result,
        decision=decision,
        candle_state=candle_state,
        fused=fused,
        stimulus=stimulus,
        snapshot=snapshot,
        bot=bot,
        strategic_window_state=strategic_window_state,
        form_symbol_state=form_symbol_state,
        derive_trade_plan_from_brain=derive_trade_plan_from_brain,
    )

    record_runtime_entry_result_protocol(
        bot,
        result,
        meta_regulation_state=meta_regulation_state,
        processing_state=processing_state,
        felt_state=felt_state,
        thought_state=thought_state,
        record_field_decision_protocol=_record_field_decision_protocol,
        record_strategic_window_protocol=_record_strategic_window_protocol,
        record_active_mcm_contact_protocol=_record_active_mcm_contact_protocol,
    )
    return result

# --------------------------------------------------

def decide_mcm_brain_entry(window, candle_state, bot=None):

    if bot is None or not window:
        return None

    timestamp = (window[-1] or {}).get("timestamp")
    decision_state = dict(getattr(bot, "mcm_runtime_decision_state", {}) or {})

    if decision_state.get("timestamp") != timestamp:
        return None

    entry_result = dict(decision_state.get("entry_result", {}) or {})

    if not entry_result:
        return None

    decision = str(entry_result.get("decision", "WAIT") or "WAIT").upper().strip()

    if decision not in ("LONG", "SHORT"):
        return dict(entry_result)

    return dict(entry_result)

# --------------------------------------------------
def build_runtime_decision_tendency(window, candle_state, bot=None):

    return build_runtime_decision_tendency_view(
        window,
        candle_state,
        bot=bot,
        tension_builder=build_tension_state_from_window,
        hold_decision_builder=_build_runtime_hold_decision,
    )

def build_runtime_entry_decision(window, candle_state, bot=None):
    """Backward-compatible runtime entry view used by older gates/tests."""

    return build_runtime_entry_decision_view(
        window,
        candle_state,
        bot=bot,
        tension_builder=build_tension_state_from_window,
        hold_decision_builder=_build_runtime_hold_decision,
    )

# --------------------------------------------------
def _build_runtime_brain_snapshot(bot, runtime_result, decision_tendency, timestamp, runtime_tick_seq=0):

    result = dict(runtime_result or {})
    meta_regulation_state = dict(result.get("meta_regulation_state", {}) or {})
    review_feedback_state = dict(meta_regulation_state.get("review_feedback_state", result.get("review_feedback_state", {}) or {}) or {})
    form_symbol_state = dict(result.get("form_symbol_state", getattr(bot, "form_symbol_state", {}) if bot is not None else {}) or {})
    strategic_window_state = dict(result.get("strategic_window_state", getattr(bot, "strategic_window_state", {}) if bot is not None else {}) or {})
    active_mcm_contact_state = dict(result.get("active_mcm_contact_state", getattr(bot, "active_mcm_contact_state", {}) if bot is not None else {}) or {})
    inner_field_state = dict(result.get("inner_field_perception_state", {}) or {})
    felt_state = dict(result.get("felt_state", {}) or {})
    neural_felt_state = dict(inner_field_state.get("neural_felt_state", felt_state.get("neural_felt_state", {})) or {})
    neural_felt_bearing = float(inner_field_state.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", felt_state.get("neural_felt_bearing", 0.0))) or 0.0)
    neural_felt_pressure = float(inner_field_state.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", felt_state.get("neural_felt_pressure", 0.0))) or 0.0)
    neural_felt_memory_resonance = float(neural_felt_state.get("neural_felt_memory_resonance", felt_state.get("neural_felt_memory_resonance", 0.0)) or 0.0)
    neural_felt_context_reactivation = float(neural_felt_state.get("neural_felt_context_reactivation", felt_state.get("neural_felt_context_reactivation", 0.0)) or 0.0)
    neural_felt_label = str(inner_field_state.get("neural_felt_label", neural_felt_state.get("neural_felt_label", felt_state.get("neural_felt_label", "quiet_neural_felt"))) or "quiet_neural_felt")
    inner_field_history_state = dict(inner_field_state.get("inner_field_history_state", {}) or {})
    inner_field_history_length = int(inner_field_history_state.get("inner_field_history_length", inner_field_state.get("inner_field_history_length", 0)) or 0)
    inner_field_pressure_trend = float(inner_field_history_state.get("inner_field_pressure_trend", inner_field_state.get("inner_field_pressure_trend", 0.0)) or 0.0)
    inner_field_bearing_trend = float(inner_field_history_state.get("inner_field_bearing_trend", inner_field_state.get("inner_field_bearing_trend", 0.0)) or 0.0)
    inner_field_topology_tension_trend = float(inner_field_history_state.get("inner_field_topology_tension_trend", inner_field_state.get("inner_field_topology_tension_trend", 0.0)) or 0.0)
    inner_field_memory_resonance_trend = float(inner_field_history_state.get("inner_field_memory_resonance_trend", inner_field_state.get("inner_field_memory_resonance_trend", 0.0)) or 0.0)
    inner_field_history_label = str(inner_field_history_state.get("inner_field_history_label", inner_field_state.get("inner_field_history_label", "stable_field_trace")) or "stable_field_trace")

    return {
        "timestamp": timestamp,
        "runtime_tick_seq": int(runtime_tick_seq or 0),
        "decision_tendency": str(decision_tendency or "hold"),
        "proposed_decision": str(result.get("proposed_decision", result.get("decision", "WAIT")) or "WAIT"),
        "self_state": str(result.get("self_state", getattr(bot, "mcm_last_action", "stable") if bot is not None else "stable") or "stable"),
        "attractor": str(result.get("attractor", getattr(bot, "mcm_last_attractor", "neutral") if bot is not None else "neutral") or "neutral"),
        "world_state": dict(result.get("world_state", {}) or {}),
        "structure_perception_state": dict(result.get("structure_perception_state", {}) or {}),
        "outer_visual_perception_state": dict(result.get("outer_visual_perception_state", {}) or {}),
        "inner_field_perception_state": dict(inner_field_state or {}),
        "processing_state": dict(result.get("processing_state", {}) or {}),
        "perception_state": dict(result.get("perception_state", {}) or {}),
        "felt_state": dict(felt_state or {}),
        "thought_state": dict(result.get("thought_state", {}) or {}),
        "meta_regulation_state": dict(result.get("meta_regulation_state", {}) or {}),
        "expectation_state": dict(result.get("expectation_state", {}) or {}),
        "form_symbol_state": dict(form_symbol_state or {}),
        "strategic_window_state": dict(strategic_window_state or {}),
        "active_mcm_contact_state": dict(active_mcm_contact_state or {}),
        "state_signature": dict(result.get("state_signature", {}) or {}),
        "focus": dict(result.get("focus", {}) or {}),
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
        "signal": {
            "signature_bias": float(result.get("signature_bias", 0.0) or 0.0),
            "signature_block": bool(result.get("signature_block", False)),
            "signature_caution_modulation": bool(result.get("signature_caution_modulation", False)),
            "signature_quality": float(result.get("signature_quality", 0.0) or 0.0),
            "signature_distance": float(result.get("signature_distance", 0.0) or 0.0),
            "context_cluster_id": str(result.get("context_cluster_id", "-") or "-"),
            "context_cluster_bias": float(result.get("context_cluster_bias", 0.0) or 0.0),
            "context_cluster_quality": float(result.get("context_cluster_quality", 0.0) or 0.0),
            "context_cluster_distance": float(result.get("context_cluster_distance", 0.0) or 0.0),
            "context_cluster_block": bool(result.get("context_cluster_block", False)),
            "context_cluster_caution_modulation": bool(result.get("context_cluster_caution_modulation", False)),
            "inhibition_level": float(result.get("inhibition_level", 0.0) or 0.0),
            "habituation_level": float(result.get("habituation_level", 0.0) or 0.0),
            "competition_bias": float(result.get("competition_bias", 0.0) or 0.0),
            "observation_mode": bool(result.get("observation_mode", False)),
            "long_score": float(result.get("long_score", 0.0) or 0.0),
            "short_score": float(result.get("short_score", 0.0) or 0.0),
            "field_stimulus_density": float(result.get("field_stimulus_density", 0.0) or 0.0),
            "field_density": float(result.get("field_density", 0.0) or 0.0),
            "field_stability": float(result.get("field_stability", 0.0) or 0.0),
            "regulatory_load": float(result.get("regulatory_load", 0.0) or 0.0),
            "action_capacity": float(result.get("action_capacity", 0.0) or 0.0),
            "recovery_need": float(result.get("recovery_need", 0.0) or 0.0),
            "survival_pressure": float(result.get("survival_pressure", 0.0) or 0.0),
            "inner_pattern_support": float(meta_regulation_state.get("inner_pattern_support", review_feedback_state.get("inner_pattern_support", 0.0)) or 0.0),
            "inner_pattern_conflict": float(meta_regulation_state.get("inner_pattern_conflict", review_feedback_state.get("inner_pattern_conflict", 0.0)) or 0.0),
            "inner_pattern_fragility": float(meta_regulation_state.get("inner_pattern_fragility", review_feedback_state.get("inner_pattern_fragility", 0.0)) or 0.0),
            "inner_pattern_bearing": float(meta_regulation_state.get("inner_pattern_bearing", review_feedback_state.get("inner_pattern_bearing", 0.0)) or 0.0),
            "inner_pattern_state": str(meta_regulation_state.get("inner_pattern_state", review_feedback_state.get("inner_pattern_state", "bearing")) or "bearing"),
            "pattern_action_support": float(meta_regulation_state.get("pattern_action_support", review_feedback_state.get("pattern_action_support", 0.0)) or 0.0),
            "pattern_observe_pressure": float(meta_regulation_state.get("pattern_observe_pressure", review_feedback_state.get("pattern_observe_pressure", 0.0)) or 0.0),
            "pattern_replan_pressure": float(meta_regulation_state.get("pattern_replan_pressure", review_feedback_state.get("pattern_replan_pressure", 0.0)) or 0.0),
            "form_symbol_id": str(form_symbol_state.get("form_symbol_id", "") or ""),
            "form_symbol_seen": int(form_symbol_state.get("form_symbol_seen", 0) or 0),
            "form_symbol_maturity": float(form_symbol_state.get("form_symbol_maturity", 0.0) or 0.0),
            "form_symbol_stability": float(form_symbol_state.get("form_symbol_stability", 0.0) or 0.0),
            "form_symbol_resonance": float(form_symbol_state.get("form_symbol_resonance", 0.0) or 0.0),
            "form_symbol_load_reduction": float(form_symbol_state.get("form_symbol_load_reduction", 0.0) or 0.0),
            "form_symbol_zoom_need": float(form_symbol_state.get("form_symbol_zoom_need", 0.0) or 0.0),
            "form_symbol_bearing": float(form_symbol_state.get("form_symbol_bearing", 0.0) or 0.0),
            "form_symbol_fragility": float(form_symbol_state.get("form_symbol_fragility", 0.0) or 0.0),
            "strategic_window_state": str(strategic_window_state.get("strategic_window_state", "no_area_focus") or "no_area_focus"),
            "lookback_window_size": int(strategic_window_state.get("lookback_window_size", 0) or 0),
            "lookback_bearing_capacity": float(strategic_window_state.get("lookback_bearing_capacity", 0.0) or 0.0),
            "strategic_pressure_interpretation": float(strategic_window_state.get("strategic_pressure_interpretation", 0.0) or 0.0),
            "strategic_patience": float(strategic_window_state.get("strategic_patience", 0.0) or 0.0),
            "area_bearing_quality": float(strategic_window_state.get("area_bearing_quality", 0.0) or 0.0),
            "area_order_intention": float(strategic_window_state.get("area_order_intention", 0.0) or 0.0),
            "area_invalidity_pressure": float(strategic_window_state.get("area_invalidity_pressure", 0.0) or 0.0),
            "active_mcm_contact_state": str(active_mcm_contact_state.get("active_mcm_contact_state", active_mcm_contact_state.get("contact_posture", "background_scan")) or "background_scan"),
            "contact_posture": str(active_mcm_contact_state.get("contact_posture", "background_scan") or "background_scan"),
            "contact_interest": float(active_mcm_contact_state.get("contact_interest", 0.0) or 0.0),
            "contact_focus_pull": float(active_mcm_contact_state.get("contact_focus_pull", 0.0) or 0.0),
            "contact_resonance_probe": float(active_mcm_contact_state.get("contact_resonance_probe", 0.0) or 0.0),
            "outer_inner_resonance": float(active_mcm_contact_state.get("outer_inner_resonance", 0.0) or 0.0),
            "outer_inner_coherence": float(active_mcm_contact_state.get("outer_inner_coherence", 0.0) or 0.0),
            "inner_change_from_contact": float(active_mcm_contact_state.get("inner_change_from_contact", 0.0) or 0.0),
            "contact_carrying_quality": float(active_mcm_contact_state.get("contact_carrying_quality", 0.0) or 0.0),
            "contact_overcoupling_risk": float(active_mcm_contact_state.get("contact_overcoupling_risk", 0.0) or 0.0),
            "contact_release_readiness": float(active_mcm_contact_state.get("contact_release_readiness", 0.0) or 0.0),
            "contact_deepen_pull": float(active_mcm_contact_state.get("contact_deepen_pull", 0.0) or 0.0),
            "contact_replay_pull": float(active_mcm_contact_state.get("contact_replay_pull", 0.0) or 0.0),
            "contact_curiosity": float(active_mcm_contact_state.get("contact_curiosity", 0.0) or 0.0),
            "contact_felt_shift": float(active_mcm_contact_state.get("contact_felt_shift", 0.0) or 0.0),
            "contact_selected_depth": float(active_mcm_contact_state.get("contact_selected_depth", 0.0) or 0.0),
            "contact_salience": float(active_mcm_contact_state.get("contact_salience", 0.0) or 0.0),
            "overcoupled_touch_score": float(active_mcm_contact_state.get("overcoupled_touch_score", 0.0) or 0.0),
            "release_contact_score": float(active_mcm_contact_state.get("release_contact_score", 0.0) or 0.0),
            "deepening_contact_score": float(active_mcm_contact_state.get("deepening_contact_score", 0.0) or 0.0),
            "resonant_contact_score": float(active_mcm_contact_state.get("resonant_contact_score", 0.0) or 0.0),
            "reflective_contact_score": float(active_mcm_contact_state.get("reflective_contact_score", 0.0) or 0.0),
            "curious_touch_score": float(active_mcm_contact_state.get("curious_touch_score", 0.0) or 0.0),
            "contact_action_maturity": float(active_mcm_contact_state.get("contact_action_maturity", 0.0) or 0.0),
            "contact_bearing_gap": float(active_mcm_contact_state.get("contact_bearing_gap", 0.0) or 0.0),
            "contact_impulse_vs_bearing": float(active_mcm_contact_state.get("contact_impulse_vs_bearing", 0.0) or 0.0),
            "contact_learning_need": float(active_mcm_contact_state.get("contact_learning_need", 0.0) or 0.0),
            "contact_reality_check": float(active_mcm_contact_state.get("contact_reality_check", 0.0) or 0.0),
            "contact_regime_mismatch": float(active_mcm_contact_state.get("contact_regime_mismatch", 0.0) or 0.0),
            "contact_stability_carryover": float(active_mcm_contact_state.get("contact_stability_carryover", 0.0) or 0.0),
            "contact_context_maturity": float(active_mcm_contact_state.get("contact_context_maturity", 0.0) or 0.0),
            "contact_context_reframe_need": float(active_mcm_contact_state.get("contact_context_reframe_need", 0.0) or 0.0),
            "neural_felt_bearing": float(neural_felt_bearing),
            "neural_felt_pressure": float(neural_felt_pressure),
            "neural_felt_memory_resonance": float(neural_felt_memory_resonance),
            "neural_felt_context_reactivation": float(neural_felt_context_reactivation),
            "neural_felt_label": str(neural_felt_label),
            "inner_field_history_length": int(inner_field_history_length),
            "inner_field_pressure_trend": float(inner_field_pressure_trend),
            "inner_field_bearing_trend": float(inner_field_bearing_trend),
            "inner_field_topology_tension_trend": float(inner_field_topology_tension_trend),
            "inner_field_memory_resonance_trend": float(inner_field_memory_resonance_trend),
            "inner_field_history_label": str(inner_field_history_label),
        },
    }

# --------------------------------------------------
def _resolve_review_decision_feedback(bot=None, runtime_result=None):

    return resolve_review_decision_feedback(
        bot=bot,
        runtime_result=runtime_result,
    )

# --------------------------------------------------
def _compute_runtime_result(window, candle_state, bot=None, tension_state=None, visual_market_state=None, structure_perception_state=None, temporal_perception_state=None):

    profile_start = _mcm_profile_start()

    if bot is None or not window:
        return None, None, None

    timestamp = (window[-1] or {}).get("timestamp")
    tension_state = dict(tension_state or {})
    if not tension_state:
        tension_state = build_tension_state_from_window(window)
    visual_market_state = dict(visual_market_state or {})
    structure_perception_state = dict(structure_perception_state or {})
    temporal_perception_state = dict(temporal_perception_state or {})
    if not temporal_perception_state:
        temporal_perception_state = dict(getattr(bot, "temporal_perception_state", {}) or {})
    temporal_modulation = _resolve_temporal_decision_modulation(temporal_perception_state)
    active_position = bool(getattr(bot, "position", None))
    active_pending = bool(getattr(bot, "pending_entry", None))

    runtime_result = None
    decision_tendency = "hold"

    if active_position or active_pending:
        if bool(getattr(bot, "observation_mode", False)):
            decision_tendency = "observe"
        runtime_result = _build_runtime_hold_decision(
            bot,
            candle_state=candle_state,
            tension_state=tension_state,
            decision_tendency=decision_tendency,
            reason="runtime_active_trade",
        )
    else:
        runtime_result = _compute_runtime_entry_result(
            window=window,
            candle_state=candle_state,
            bot=bot,
            visual_market_state=visual_market_state,
            structure_perception_state=structure_perception_state,
            temporal_perception_state=temporal_perception_state,
        )

        if runtime_result is None:
            if bool(getattr(bot, "observation_mode", False)):
                decision_tendency = "observe"
            runtime_result = _build_runtime_hold_decision(
                bot,
                candle_state=candle_state,
                tension_state=tension_state,
                decision_tendency=decision_tendency,
                reason="runtime_no_plan",
            )
        else:
            proposed_decision = str(runtime_result.get("proposed_decision", runtime_result.get("decision", "WAIT")) or "WAIT").upper().strip()
            meta_regulation_state = dict(runtime_result.get("meta_regulation_state", {}) or {})
            pre_action_phase = str(meta_regulation_state.get("pre_action_phase", "hold") or "hold").strip().lower()
            review_feedback_state = dict(runtime_result.get("review_feedback_state", {}) or {})
            tendency_hint = str(review_feedback_state.get("tendency_hint", "hold") or "hold").strip().lower()
            act_push = float(review_feedback_state.get("act_push", 0.0) or 0.0)
            observe_pull = float(review_feedback_state.get("observe_pull", 0.0) or 0.0)
            replan_pull = float(review_feedback_state.get("replan_pull", 0.0) or 0.0)
            hold_pull = float(review_feedback_state.get("hold_pull", 0.0) or 0.0)

            temporal_observe_pull = float(temporal_modulation.get("observe_pull", 0.0) or 0.0)
            temporal_replan_pull = float(temporal_modulation.get("replan_pull", 0.0) or 0.0)
            temporal_exhaustion_risk = float(temporal_modulation.get("exhaustion_risk", 0.0) or 0.0)
            temporal_conviction_boost = float(temporal_modulation.get("conviction_boost", 0.0) or 0.0)

            act_push = max(0.0, act_push + (temporal_conviction_boost * 0.42) - (temporal_exhaustion_risk * 0.34))
            observe_pull = max(observe_pull, observe_pull + temporal_observe_pull)
            replan_pull = max(replan_pull, replan_pull + temporal_replan_pull)
            hold_pull = max(hold_pull, hold_pull + (temporal_observe_pull * 0.42) + (temporal_exhaustion_risk * 0.24))

            if not bool(meta_regulation_state.get("allow_plan", False)):
                if pre_action_phase == "replan" or bool(meta_regulation_state.get("allow_ruminate", False)):
                    decision_tendency = "replan"
                elif pre_action_phase == "observe" or bool(meta_regulation_state.get("allow_observe", False)):
                    decision_tendency = "observe"
                else:
                    decision_tendency = "hold"
            elif proposed_decision in ("LONG", "SHORT"):
                if temporal_exhaustion_risk >= 0.18 and act_push < max(0.20, observe_pull):
                    decision_tendency = "observe"
                elif tendency_hint == "replan" and replan_pull >= max(0.34, act_push + 0.02):
                    decision_tendency = "replan"
                elif tendency_hint == "observe" and observe_pull >= max(0.32, act_push + 0.02):
                    decision_tendency = "observe"
                elif hold_pull >= 0.34 and act_push < 0.18:
                    decision_tendency = "hold"
                else:
                    decision_tendency = "act"
            elif pre_action_phase == "observe" or bool(meta_regulation_state.get("allow_observe", False)):
                decision_tendency = "observe"
            elif pre_action_phase == "replan" or bool(meta_regulation_state.get("allow_ruminate", False)):
                decision_tendency = "replan"
            elif tendency_hint == "replan" and replan_pull >= 0.34:
                decision_tendency = "replan"
            elif tendency_hint == "observe" and observe_pull >= 0.32:
                decision_tendency = "observe"
            elif bool(runtime_result.get("observation_mode", False)):
                decision_tendency = "observe"
            else:
                decision_tendency = "hold"

            runtime_result["decision_tendency"] = str(decision_tendency)
            runtime_result["proposed_decision"] = str(proposed_decision or "WAIT")

    _mcm_profile_debug(
        "compute_runtime_result.total",
        profile_start,
        extra=f"decision_tendency={decision_tendency}|active_trade={bool(active_position or active_pending)}",
    )
    return runtime_result, decision_tendency, timestamp

# --------------------------------------------------
def _apply_runtime_result(bot, runtime_result, decision_tendency, timestamp, runtime_tick_seq=0, market_tick_advanced=True):

    profile_start = _mcm_profile_start()
    runtime_payload = advance_runtime_perception_layers(
        runtime_result,
        bot=bot,
        decision_tendency=decision_tendency,
        market_tick_advanced=market_tick_advanced,
        temporal_advance=_advance_temporal_perception_state,
        felt_advance=_advance_felt_state,
        thought_advance=_advance_thought_state,
    )

    _flush_form_symbol_memory_if_due(bot, force=False)

    brain_snapshot = _build_runtime_brain_snapshot(
        bot,
        runtime_payload,
        decision_tendency,
        timestamp,
        runtime_tick_seq=runtime_tick_seq,
    )
    snapshot = build_runtime_snapshot_state(
        runtime_payload,
        bot=bot,
        brain_snapshot=brain_snapshot,
        decision_tendency=decision_tendency,
        timestamp=timestamp,
        runtime_tick_seq=runtime_tick_seq,
        market_tick_advanced=market_tick_advanced,
    )
    decision_state = build_runtime_decision_state(
        runtime_payload,
        timestamp=timestamp,
        decision_tendency=decision_tendency,
        runtime_tick_seq=runtime_tick_seq,
        form_symbol_state=runtime_payload.get("form_symbol_state", getattr(bot, "form_symbol_state", {}) or {}),
    )

    commit_runtime_snapshot_state(
        bot,
        snapshot=snapshot,
        decision_state=decision_state,
        brain_snapshot=brain_snapshot,
        decision_tendency=decision_tendency,
        timestamp=timestamp,
    )

    previous_episode = dict(getattr(bot, "mcm_decision_episode", {}) or {})
    if previous_episode.get("timestamp") != timestamp:
        bot.mcm_episode_seq = int(getattr(bot, "mcm_episode_seq", 0) or 0) + 1
    episode = build_visible_episode_state(
        runtime_result,
        previous_episode=previous_episode,
        episode_seq=int(getattr(bot, "mcm_episode_seq", 0) or 0),
        decision_state=decision_state,
        decision_tendency=decision_tendency,
        timestamp=timestamp,
        runtime_tick_seq=runtime_tick_seq,
    )

    previous_episode_internal = dict(getattr(bot, "mcm_decision_episode_internal", {}) or {})
    episode_internal = build_internal_episode_state(
        runtime_result,
        previous_internal=previous_episode_internal,
        visible_episode_id=str(episode.get("episode_id", "") or ""),
        decision_tendency=decision_tendency,
        timestamp=timestamp,
        runtime_tick_seq=runtime_tick_seq,
    )
    episode_internal["episode_id"] = str(episode.get("episode_id", "") or "")
    episode_internal["visible_episode_id"] = str(episode.get("episode_id", "") or "")
    episode_internal["learning_state"] = str((episode_internal.get("learning_state", "open") or "open"))
    episode_internal["internal_events"] = list((previous_episode_internal.get("internal_events", []) or [])[-24:])

    commit_runtime_episode_state(
        bot,
        episode=episode,
        episode_internal=episode_internal,
    )

    profile_section_start = _mcm_profile_start()
    context_refresh_state = refresh_runtime_context_state(
        bot,
        runtime_result=runtime_payload,
        decision_tendency=decision_tendency,
        timestamp=timestamp,
        market_tick_advanced=market_tick_advanced,
        experience_refresher=_refresh_experience_space,
        active_context_refresher=_refresh_active_context_trace,
        active_context_signal_merger=merge_active_context_signal,
    )
    active_context_trace = dict((context_refresh_state or {}).get("active_context_trace", {}) or {})
    _mcm_profile_debug(
        "apply_runtime_result.refresh_runtime_context_state",
        profile_section_start,
        extra=f"decision_tendency={decision_tendency}|active={float(active_context_trace.get('activation', 0.0) or 0.0):.4f}",
    )

    _mcm_profile_debug(
        "apply_runtime_result.total",
        profile_start,
        extra=f"decision_tendency={decision_tendency}|runtime_tick_seq={int(runtime_tick_seq or 0)}",
    )
    return dict(runtime_result or {})

# --------------------------------------------------
def _build_episode_review_notes(bot, episode=None, episode_internal=None, event_name=None, timestamp=None):

    visible_episode = dict(episode or {})
    internal_episode = dict(episode_internal or {})
    outcome_decomposition = dict(getattr(bot, "last_outcome_decomposition", {}) or {}) if bot is not None else {}
    in_trade_summary = _summarize_in_trade_updates(internal_episode.get("in_trade_updates", []))
    return _build_episode_review_notes_from_context_impl(
        visible_episode=visible_episode,
        internal_episode=internal_episode,
        outcome_decomposition=outcome_decomposition,
        in_trade_summary=in_trade_summary,
        event_name=event_name,
        timestamp=timestamp,
    )

def _clip01(value):

    try:
        value = float(value)
    except Exception:
        value = 0.0

    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)

def write_visualization_snapshot_bundle(snapshot_bundle):
    return _write_visualization_snapshot_bundle_impl(
        snapshot_bundle,
        profile_start=_mcm_profile_start,
        profile_debug=_mcm_profile_debug,
    )

# --------------------------------------------------
def build_visualization_snapshot_bundle(bot=None, window=None, candle_state=None):
    return _build_visualization_snapshot_bundle_impl(
        bot=bot,
        window=window,
        candle_state=candle_state,
        pipeline_snapshot_builder=build_runtime_pipeline_snapshot,
    )

# --------------------------------------------------
def prepare_visualization_snapshot_state(bot=None, window=None, candle_state=None):
    return _prepare_visualization_snapshot_state_impl(
        bot=bot,
        window=window,
        candle_state=candle_state,
        pipeline_snapshot_builder=build_runtime_pipeline_snapshot,
    )

# --------------------------------------------------
def capture_runtime_regulation_transition(bot=None, state_before: dict | None = None, state_after: dict | None = None) -> tuple[dict, dict, dict]:
    return _capture_runtime_regulation_transition_impl(
        bot=bot,
        state_before=state_before,
        state_after=state_after,
    )

# --------------------------------------------------
def commit_runtime_regulation_snapshot(bot=None, state_after: dict | None = None) -> dict:
    return _commit_runtime_regulation_snapshot_impl(
        bot=bot,
        state_after=state_after,
    )


