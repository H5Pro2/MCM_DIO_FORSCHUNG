"""Runtime snapshot builders.

These helpers shape runtime result data into persistent snapshot dictionaries.
They avoid mutating the bot directly; `MCM_Brain_Modell.py` still owns the
commit into bot state.
"""


def extract_neural_felt_summary(runtime_result):
    result = dict(runtime_result or {})
    inner_field_state = dict(result.get("inner_field_perception_state", {}) or {})
    felt_state = dict(result.get("felt_state", {}) or {})
    neural_felt_state = dict(inner_field_state.get("neural_felt_state", felt_state.get("neural_felt_state", {})) or {})
    inner_field_history_state = dict(inner_field_state.get("inner_field_history_state", {}) or {})

    return {
        "neural_felt_state": dict(neural_felt_state or {}),
        "neural_felt_bearing": float(inner_field_state.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", felt_state.get("neural_felt_bearing", 0.0))) or 0.0),
        "neural_felt_pressure": float(inner_field_state.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", felt_state.get("neural_felt_pressure", 0.0))) or 0.0),
        "neural_felt_memory_resonance": float(neural_felt_state.get("neural_felt_memory_resonance", felt_state.get("neural_felt_memory_resonance", 0.0)) or 0.0),
        "neural_felt_context_reactivation": float(neural_felt_state.get("neural_felt_context_reactivation", felt_state.get("neural_felt_context_reactivation", 0.0)) or 0.0),
        "neural_felt_label": str(inner_field_state.get("neural_felt_label", neural_felt_state.get("neural_felt_label", felt_state.get("neural_felt_label", "quiet_neural_felt"))) or "quiet_neural_felt"),
        "inner_field_history_state": dict(inner_field_history_state or {}),
        "inner_field_history_length": int(inner_field_history_state.get("inner_field_history_length", inner_field_state.get("inner_field_history_length", 0)) or 0),
        "inner_field_pressure_trend": float(inner_field_history_state.get("inner_field_pressure_trend", inner_field_state.get("inner_field_pressure_trend", 0.0)) or 0.0),
        "inner_field_bearing_trend": float(inner_field_history_state.get("inner_field_bearing_trend", inner_field_state.get("inner_field_bearing_trend", 0.0)) or 0.0),
        "inner_field_topology_tension_trend": float(inner_field_history_state.get("inner_field_topology_tension_trend", inner_field_state.get("inner_field_topology_tension_trend", 0.0)) or 0.0),
        "inner_field_memory_resonance_trend": float(inner_field_history_state.get("inner_field_memory_resonance_trend", inner_field_state.get("inner_field_memory_resonance_trend", 0.0)) or 0.0),
        "inner_field_history_label": str(inner_field_history_state.get("inner_field_history_label", inner_field_state.get("inner_field_history_label", "stable_field_trace")) or "stable_field_trace"),
    }


def build_runtime_snapshot_state(
    runtime_result,
    *,
    bot=None,
    brain_snapshot=None,
    decision_tendency="hold",
    timestamp=None,
    runtime_tick_seq=0,
    market_tick_advanced=True,
):
    result = dict(runtime_result or {})
    brain_snapshot = dict(brain_snapshot or {})
    neural = extract_neural_felt_summary(result)

    market_ticks_before = int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0) if bot is not None else 0
    focus = dict(result.get("focus", {}) or {})
    meta = dict(result.get("meta_regulation_state", {}) or {})

    snapshot = {
        "timestamp": timestamp,
        "market_ticks": int(market_ticks_before + (1 if bool(market_tick_advanced) else 0)),
        "runtime_tick_seq": int(runtime_tick_seq or 0),
        "market_tick_advanced": bool(market_tick_advanced),
        "decision_tendency": str(decision_tendency or "hold"),
        "proposed_decision": str(result.get("proposed_decision", result.get("decision", "WAIT")) or "WAIT"),
        "self_state": str(result.get("self_state", getattr(bot, "mcm_last_action", "stable") if bot is not None else "stable") or "stable"),
        "attractor": str(result.get("attractor", getattr(bot, "mcm_last_attractor", "neutral") if bot is not None else "neutral") or "neutral"),
        "focus_confidence": float(focus.get("focus_confidence", getattr(bot, "focus_confidence", 0.0) if bot is not None else 0.0) or 0.0),
        "observation_mode": bool(result.get("observation_mode", False)),
        "allow_plan": bool(meta.get("allow_plan", False)),
        "field_stimulus_density": float(result.get("field_stimulus_density", 0.0) or 0.0),
        "field_density": float(result.get("field_density", 0.0) or 0.0),
        "field_stability": float(result.get("field_stability", 0.0) or 0.0),
        "regulatory_load": float(result.get("regulatory_load", 0.0) or 0.0),
        "action_capacity": float(result.get("action_capacity", 0.0) or 0.0),
        "recovery_need": float(result.get("recovery_need", 0.0) or 0.0),
        "survival_pressure": float(result.get("survival_pressure", 0.0) or 0.0),
        "brain_snapshot_ready": bool(brain_snapshot),
    }
    snapshot.update(neural)
    return snapshot


def build_runtime_decision_state(
    runtime_result,
    *,
    timestamp=None,
    decision_tendency="hold",
    runtime_tick_seq=0,
    form_symbol_state=None,
):
    result = dict(runtime_result or {})
    neural = extract_neural_felt_summary(result)

    decision_state = {
        "timestamp": timestamp,
        "runtime_tick_seq": int(runtime_tick_seq or 0),
        "decision_tendency": str(decision_tendency or "hold"),
        "proposed_decision": str(result.get("proposed_decision", result.get("decision", "WAIT")) or "WAIT"),
        "allow_plan": bool((result.get("meta_regulation_state", {}) or {}).get("allow_plan", False)),
        "entry_price": float(result.get("entry_price", 0.0) or 0.0),
        "tp_price": float(result.get("tp_price", 0.0) or 0.0),
        "sl_price": float(result.get("sl_price", 0.0) or 0.0),
        "rr_value": float(result.get("rr_value", 0.0) or 0.0),
        "entry_validity_band": dict(result.get("entry_validity_band", {}) or {}),
        "form_symbol_state": dict(form_symbol_state or result.get("form_symbol_state", {}) or {}),
        "entry_result": dict(result or {}),
    }
    decision_state.update(neural)
    return decision_state


def build_active_context_signal_state(active_context_trace):
    trace = dict(active_context_trace or {})
    return {
        "active_context_activation": float(trace.get("activation", 0.0) or 0.0),
        "active_context_support": float(trace.get("support", 0.0) or 0.0),
        "active_context_conflict": float(trace.get("conflict", 0.0) or 0.0),
        "active_context_bearing": float(trace.get("bearing", 0.0) or 0.0),
        "active_context_neural_felt_bearing": float(trace.get("neural_felt_bearing", 0.0) or 0.0),
        "active_context_neural_felt_pressure": float(trace.get("neural_felt_pressure", 0.0) or 0.0),
        "active_context_neural_felt_memory_resonance": float(trace.get("neural_felt_memory_resonance", 0.0) or 0.0),
        "active_context_neural_felt_context_reactivation": float(trace.get("neural_felt_context_reactivation", 0.0) or 0.0),
        "active_context_neural_felt_label": str(trace.get("neural_felt_label", "quiet_neural_felt") or "quiet_neural_felt"),
        "active_context_history_length": int(trace.get("inner_field_history_length", 0) or 0),
        "active_context_pressure_trend": float(trace.get("inner_field_pressure_trend", 0.0) or 0.0),
        "active_context_bearing_trend": float(trace.get("inner_field_bearing_trend", 0.0) or 0.0),
        "active_context_topology_tension_trend": float(trace.get("inner_field_topology_tension_trend", 0.0) or 0.0),
        "active_context_memory_resonance_trend": float(trace.get("inner_field_memory_resonance_trend", 0.0) or 0.0),
        "active_context_history_label": str(trace.get("inner_field_history_label", "stable_field_trace") or "stable_field_trace"),
        "active_context_topology_rows": int(trace.get("field_topology_rows", 0) or 0),
        "active_context_topology_cols": int(trace.get("field_topology_cols", 0) or 0),
        "active_context_topology_position_count": int(trace.get("field_topology_position_count", 0) or 0),
        "active_context_topology_neighbor_link_count": int(trace.get("field_topology_neighbor_link_count", 0) or 0),
        "active_context_topology_neighbor_count_mean": float(trace.get("field_topology_neighbor_count_mean", 0.0) or 0.0),
        "active_context_topology_neighbor_count_max": int(trace.get("field_topology_neighbor_count_max", 0) or 0),
        "active_context_areal_topology_density_mean": float(trace.get("field_areal_topology_density_mean", 0.0) or 0.0),
        "active_context_areal_topology_span_mean": float(trace.get("field_areal_topology_span_mean", 0.0) or 0.0),
        "active_context_areal_topology_boundary_mean": float(trace.get("field_areal_topology_boundary_mean", 0.0) or 0.0),
        "active_context_field_pattern_signature_key": str(trace.get("field_pattern_signature_key", "") or ""),
        "active_context_inner_pattern_identity": str(trace.get("inner_pattern_identity", "") or ""),
        "active_context_inner_pattern_identity_label": str(trace.get("inner_pattern_identity_label", "") or ""),
        "active_context_inner_pattern_identity_confidence": float(trace.get("inner_pattern_identity_confidence", 0.0) or 0.0),
        "active_context_inner_pattern_identity_streak": int(trace.get("inner_pattern_identity_streak", 0) or 0),
        "active_context_inner_pattern_identity_stability": float(trace.get("inner_pattern_identity_stability", 0.0) or 0.0),
        "active_context_inner_pattern_identity_recurrent": bool(trace.get("inner_pattern_identity_recurrent", False)),
        "active_context_inner_pattern_identity_changed": bool(trace.get("inner_pattern_identity_changed", False)),
        "active_context_inner_pattern_identity_last_seen_tick": int(trace.get("inner_pattern_identity_last_seen_tick", 0) or 0),
        "active_context_inner_pattern_recognition_label": str(trace.get("inner_pattern_recognition_label", "unsettled_inner_pattern") or "unsettled_inner_pattern"),
        "active_context_inner_pattern_recognition_strength": float(trace.get("inner_pattern_recognition_strength", 0.0) or 0.0),
        "active_context_inner_pattern_recognition_recurrent": bool(trace.get("inner_pattern_recognition_recurrent", False)),
        "active_context_inner_pattern_recognition_changed": bool(trace.get("inner_pattern_recognition_changed", False)),
    }


def merge_active_context_signal(signal_state, active_context_trace):
    merged = dict(signal_state or {})
    merged.update(build_active_context_signal_state(active_context_trace))
    return merged


# Runtime pipeline snapshot -------------------------------------------------
def build_runtime_pipeline_snapshot(bot=None, *, profile_start=None, profile_debug=None):

    section_start = profile_start() if profile_start is not None else None

    if bot is None:
        return {
            "outer_visual_perception_state": {},
            "inner_field_perception_state": {},
            "temporal_perception_state": {},
            "perception_state": {},
            "processing_state": {},
            "felt_state": {},
            "thought_state": {},
            "meta_regulation_state": {},
            "review_feedback_state": {},
            "review_carry_capacity": 0.0,
            "review_caution_load": 0.0,
            "review_tendency_hint": "hold",
            "inner_pattern_support": 0.0,
            "inner_pattern_conflict": 0.0,
            "inner_pattern_fragility": 0.0,
            "inner_pattern_bearing": 0.0,
            "inner_pattern_state": "bearing",
            "pattern_action_support": 0.0,
            "pattern_observe_pressure": 0.0,
            "pattern_replan_pressure": 0.0,
            "form_symbol_state": {},
            "neural_felt_state": {},
            "neural_felt_bearing": 0.0,
            "neural_felt_pressure": 0.0,
            "neural_felt_memory_resonance": 0.0,
            "neural_felt_context_reactivation": 0.0,
            "neural_felt_label": "quiet_neural_felt",
            "active_context_trace": {},
            "inner_field_history_state": {},
            "inner_field_history_length": 0,
            "inner_field_pressure_trend": 0.0,
            "inner_field_bearing_trend": 0.0,
            "inner_field_topology_tension_trend": 0.0,
            "inner_field_memory_resonance_trend": 0.0,
            "inner_field_history_label": "empty_field_history",
            "expectation_state": {},
            "action_intent_state": {},
            "execution_state": {},
            "field_state": {
                "field_stimulus_density": 0.0,
                "field_density": 0.0,
                "field_stability": 0.0,
                "regulatory_load": 0.0,
                "action_capacity": 0.0,
                "recovery_need": 0.0,
                "survival_pressure": 0.0,
            },
            "runtime_state": {
                "decision_tendency": "hold",
                "proposed_decision": "WAIT",
                "self_state": "stable",
                "attractor": "neutral",
                "observation_mode": False,
            },
        }

    meta_regulation_state = dict(getattr(bot, "meta_regulation_state", {}) or {})
    review_feedback_state = dict(meta_regulation_state.get("review_feedback_state", {}) or {})
    runtime_state = dict(getattr(bot, "mcm_runtime_decision_state", {}) or {})
    inner_field_state = dict(getattr(bot, "inner_field_perception_state", {}) or {})
    felt_state = dict(getattr(bot, "felt_state", {}) or {})
    neural_felt_state = dict(inner_field_state.get("neural_felt_state", felt_state.get("neural_felt_state", {})) or {})
    inner_field_history_state = dict(inner_field_state.get("inner_field_history_state", getattr(bot, "inner_field_history_state", {})) or {})

    payload = {
        "outer_visual_perception_state": dict(getattr(bot, "outer_visual_perception_state", {}) or {}),
        "inner_field_perception_state": dict(inner_field_state or {}),
        "temporal_perception_state": dict(getattr(bot, "temporal_perception_state", {}) or {}),
        "perception_state": dict(getattr(bot, "perception_state", {}) or {}),
        "processing_state": dict(getattr(bot, "processing_state", {}) or {}),
        "felt_state": dict(felt_state or {}),
        "thought_state": dict(getattr(bot, "thought_state", {}) or {}),
        "meta_regulation_state": dict(meta_regulation_state or {}),
        "review_feedback_state": dict(review_feedback_state or {}),
        "review_carry_capacity": float(meta_regulation_state.get("review_carry_capacity", review_feedback_state.get("carry_capacity", 0.0)) or 0.0),
        "review_caution_load": float(meta_regulation_state.get("review_caution_load", review_feedback_state.get("caution_load", 0.0)) or 0.0),
        "review_tendency_hint": str(meta_regulation_state.get("review_tendency_hint", review_feedback_state.get("tendency_hint", "hold")) or "hold"),
        "inner_pattern_support": float(meta_regulation_state.get("inner_pattern_support", review_feedback_state.get("inner_pattern_support", 0.0)) or 0.0),
        "inner_pattern_conflict": float(meta_regulation_state.get("inner_pattern_conflict", review_feedback_state.get("inner_pattern_conflict", 0.0)) or 0.0),
        "inner_pattern_fragility": float(meta_regulation_state.get("inner_pattern_fragility", review_feedback_state.get("inner_pattern_fragility", 0.0)) or 0.0),
        "inner_pattern_bearing": float(meta_regulation_state.get("inner_pattern_bearing", review_feedback_state.get("inner_pattern_bearing", 0.0)) or 0.0),
        "inner_pattern_state": str(meta_regulation_state.get("inner_pattern_state", review_feedback_state.get("inner_pattern_state", "bearing")) or "bearing"),
        "pattern_action_support": float(meta_regulation_state.get("pattern_action_support", review_feedback_state.get("pattern_action_support", 0.0)) or 0.0),
        "pattern_observe_pressure": float(meta_regulation_state.get("pattern_observe_pressure", review_feedback_state.get("pattern_observe_pressure", 0.0)) or 0.0),
        "pattern_replan_pressure": float(meta_regulation_state.get("pattern_replan_pressure", review_feedback_state.get("pattern_replan_pressure", 0.0)) or 0.0),
        "form_symbol_state": dict(getattr(bot, "form_symbol_state", {}) or {}),
        "neural_felt_state": dict(neural_felt_state or {}),
        "neural_felt_bearing": float(inner_field_state.get("neural_felt_bearing", neural_felt_state.get("neural_felt_bearing", felt_state.get("neural_felt_bearing", 0.0))) or 0.0),
        "neural_felt_pressure": float(inner_field_state.get("neural_felt_pressure", neural_felt_state.get("neural_felt_pressure", felt_state.get("neural_felt_pressure", 0.0))) or 0.0),
        "neural_felt_memory_resonance": float(neural_felt_state.get("neural_felt_memory_resonance", felt_state.get("neural_felt_memory_resonance", 0.0)) or 0.0),
        "neural_felt_context_reactivation": float(neural_felt_state.get("neural_felt_context_reactivation", felt_state.get("neural_felt_context_reactivation", 0.0)) or 0.0),
        "neural_felt_label": str(inner_field_state.get("neural_felt_label", neural_felt_state.get("neural_felt_label", felt_state.get("neural_felt_label", "quiet_neural_felt"))) or "quiet_neural_felt"),
        "active_context_trace": dict(getattr(bot, "active_context_trace", {}) or {}),
        "inner_field_history_state": dict(inner_field_history_state or {}),
        "inner_field_history_length": int(inner_field_history_state.get("inner_field_history_length", inner_field_state.get("inner_field_history_length", 0)) or 0),
        "inner_field_pressure_trend": float(inner_field_history_state.get("inner_field_pressure_trend", inner_field_state.get("inner_field_pressure_trend", 0.0)) or 0.0),
        "inner_field_bearing_trend": float(inner_field_history_state.get("inner_field_bearing_trend", inner_field_state.get("inner_field_bearing_trend", 0.0)) or 0.0),
        "inner_field_topology_tension_trend": float(inner_field_history_state.get("inner_field_topology_tension_trend", inner_field_state.get("inner_field_topology_tension_trend", 0.0)) or 0.0),
        "inner_field_memory_resonance_trend": float(inner_field_history_state.get("inner_field_memory_resonance_trend", inner_field_state.get("inner_field_memory_resonance_trend", 0.0)) or 0.0),
        "inner_field_history_label": str(inner_field_history_state.get("inner_field_history_label", inner_field_state.get("inner_field_history_label", "stable_field_trace")) or "stable_field_trace"),
        "expectation_state": dict(getattr(bot, "expectation_state", {}) or {}),
        "action_intent_state": dict(getattr(bot, "action_intent_state", {}) or {}),
        "execution_state": dict(getattr(bot, "execution_state", {}) or {}),
        "field_state": {
            "field_stimulus_density": float(getattr(bot, "field_stimulus_density", 0.0) or 0.0),
            "field_density": float(getattr(bot, "field_density", 0.0) or 0.0),
            "field_stability": float(getattr(bot, "field_stability", 0.0) or 0.0),
            "regulatory_load": float(getattr(bot, "regulatory_load", 0.0) or 0.0),
            "action_capacity": float(getattr(bot, "action_capacity", 0.0) or 0.0),
            "recovery_need": float(getattr(bot, "recovery_need", 0.0) or 0.0),
            "survival_pressure": float(getattr(bot, "survival_pressure", 0.0) or 0.0),
        },
        "runtime_state": {
            "decision_tendency": str(runtime_state.get("decision_tendency", "hold") or "hold"),
            "proposed_decision": str(runtime_state.get("proposed_decision", "WAIT") or "WAIT"),
            "self_state": str(runtime_state.get("self_state", "stable") or "stable"),
            "attractor": str(runtime_state.get("attractor", "neutral") or "neutral"),
            "observation_mode": bool(getattr(bot, "observation_mode", False)),
        },
    }

    if profile_debug is not None:
        profile_debug(
            "build_runtime_pipeline_snapshot.total",
            section_start,
            extra=f"keys={int(len(payload or {}))}",
        )
    return dict(payload or {})

