"""Runtime tendency view for entry gates.

This module reads the latest runtime snapshot and converts it into the compact
decision-tendency shape consumed by gate code. It does not mutate DIO state.
"""


def build_runtime_decision_tendency_view(
    window,
    candle_state,
    bot=None,
    *,
    tension_builder=None,
    hold_decision_builder=None,
):
    if bot is None or not window:
        return None

    timestamp = (window[-1] or {}).get("timestamp")
    decision_state = dict(getattr(bot, "mcm_runtime_decision_state", {}) or {})
    brain_snapshot = dict(getattr(bot, "mcm_runtime_brain_snapshot", {}) or {})

    if decision_state.get("timestamp") != timestamp:
        if tension_builder is None or hold_decision_builder is None:
            return None

        tension_state = tension_builder(window)
        hold_result = hold_decision_builder(
            bot,
            candle_state=candle_state,
            tension_state=tension_state,
            decision_tendency="hold",
            reason="runtime_timestamp_miss",
        )

        return {
            "timestamp": timestamp,
            "runtime_tick_seq": int(decision_state.get("runtime_tick_seq", 0) or 0),
            "decision_tendency": str(hold_result.get("decision_tendency", "hold") or "hold"),
            "proposed_decision": str(hold_result.get("proposed_decision", "WAIT") or "WAIT"),
            "allow_plan": bool((hold_result.get("meta_regulation_state", {}) or {}).get("allow_plan", False)),
            "observation_mode": bool(hold_result.get("observation_mode", False)),
            "self_state": str(hold_result.get("self_state", "stable") or "stable"),
            "attractor": str(hold_result.get("attractor", "neutral") or "neutral"),
            "focus": dict(hold_result.get("focus", {}) or {}),
            "world_state": dict(hold_result.get("world_state", {}) or {}),
            "structure_perception_state": dict(hold_result.get("structure_perception_state", {}) or {}),
            "outer_visual_perception_state": dict(hold_result.get("outer_visual_perception_state", {}) or {}),
            "inner_field_perception_state": dict(hold_result.get("inner_field_perception_state", {}) or {}),
            "perception_state": dict(hold_result.get("perception_state", {}) or {}),
            "processing_state": dict(hold_result.get("processing_state", {}) or {}),
            "felt_state": dict(hold_result.get("felt_state", {}) or {}),
            "thought_state": dict(hold_result.get("thought_state", {}) or {}),
            "meta_regulation_state": dict(hold_result.get("meta_regulation_state", {}) or {}),
            "expectation_state": dict(hold_result.get("expectation_state", {}) or {}),
            "form_symbol_state": dict(hold_result.get("form_symbol_state", {}) or {}),
            "strategic_window_state": dict(hold_result.get("strategic_window_state", {}) or {}),
            "active_mcm_contact_state": dict(hold_result.get("active_mcm_contact_state", {}) or {}),
            "state_signature": dict(hold_result.get("state_signature", {}) or {}),
            "signature_bias": float(hold_result.get("signature_bias", 0.0) or 0.0),
            "signature_block": bool(hold_result.get("signature_block", False)),
            "signature_quality": float(hold_result.get("signature_quality", 0.0) or 0.0),
            "signature_distance": float(hold_result.get("signature_distance", 0.0) or 0.0),
            "context_cluster_id": str(hold_result.get("context_cluster_id", "-") or "-"),
            "context_cluster_bias": float(hold_result.get("context_cluster_bias", 0.0) or 0.0),
            "context_cluster_quality": float(hold_result.get("context_cluster_quality", 0.0) or 0.0),
            "context_cluster_distance": float(hold_result.get("context_cluster_distance", 0.0) or 0.0),
            "context_cluster_block": bool(hold_result.get("context_cluster_block", False)),
            "inhibition_level": float(hold_result.get("inhibition_level", 0.0) or 0.0),
            "habituation_level": float(hold_result.get("habituation_level", 0.0) or 0.0),
            "competition_bias": float(hold_result.get("competition_bias", 0.0) or 0.0),
            "long_score": float(hold_result.get("long_score", 0.0) or 0.0),
            "short_score": float(hold_result.get("short_score", 0.0) or 0.0),
            "field_density": float(hold_result.get("field_density", 0.0) or 0.0),
            "field_stability": float(hold_result.get("field_stability", 0.0) or 0.0),
            "regulatory_load": float(hold_result.get("regulatory_load", 0.0) or 0.0),
            "action_capacity": float(hold_result.get("action_capacity", 0.0) or 0.0),
            "recovery_need": float(hold_result.get("recovery_need", 0.0) or 0.0),
            "survival_pressure": float(hold_result.get("survival_pressure", 0.0) or 0.0),
            "felt_bearing_score": float(hold_result.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(hold_result.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "rejection_reason": str(hold_result.get("rejection_reason", "runtime_timestamp_miss") or "runtime_timestamp_miss"),
        }

    entry_result = dict(decision_state.get("entry_result", {}) or {})
    signal_state = dict(brain_snapshot.get("signal", {}) or {})
    focus_state = dict(brain_snapshot.get("focus", {}) or {})
    world_state = dict(brain_snapshot.get("world_state", {}) or {})

    return {
        "timestamp": timestamp,
        "runtime_tick_seq": int(decision_state.get("runtime_tick_seq", 0) or 0),
        "decision_tendency": str(decision_state.get("decision_tendency", entry_result.get("decision_tendency", "hold")) or "hold"),
        "proposed_decision": str(decision_state.get("proposed_decision", entry_result.get("proposed_decision", entry_result.get("decision", "WAIT"))) or "WAIT"),
        "allow_plan": bool(decision_state.get("allow_plan", False)),
        "observation_mode": bool(signal_state.get("observation_mode", entry_result.get("observation_mode", False))),
        "self_state": str(brain_snapshot.get("self_state", entry_result.get("self_state", "stable")) or "stable"),
        "attractor": str(brain_snapshot.get("attractor", entry_result.get("attractor", "neutral")) or "neutral"),
        "focus": dict(focus_state or {}),
        "world_state": dict(world_state or entry_result.get("world_state", {}) or {}),
        "structure_perception_state": dict(brain_snapshot.get("structure_perception_state", entry_result.get("structure_perception_state", {})) or {}),
        "temporal_perception_state": dict((world_state or entry_result.get("world_state", {}) or {}).get("temporal_perception_state", entry_result.get("temporal_perception_state", {})) or {}),
        "temporal_decision_state": dict(entry_result.get("temporal_decision_state", {}) or {}),
        "outer_visual_perception_state": dict(brain_snapshot.get("outer_visual_perception_state", entry_result.get("outer_visual_perception_state", {})) or {}),
        "inner_field_perception_state": dict(brain_snapshot.get("inner_field_perception_state", entry_result.get("inner_field_perception_state", {})) or {}),
        "perception_state": dict(brain_snapshot.get("perception_state", entry_result.get("perception_state", {})) or {}),
        "processing_state": dict(brain_snapshot.get("processing_state", entry_result.get("processing_state", {})) or {}),
        "felt_state": dict(brain_snapshot.get("felt_state", entry_result.get("felt_state", {})) or {}),
        "thought_state": dict(brain_snapshot.get("thought_state", entry_result.get("thought_state", {})) or {}),
        "meta_regulation_state": dict(brain_snapshot.get("meta_regulation_state", entry_result.get("meta_regulation_state", {})) or {}),
        "expectation_state": dict(brain_snapshot.get("expectation_state", entry_result.get("expectation_state", {})) or {}),
        "form_symbol_state": dict(brain_snapshot.get("form_symbol_state", entry_result.get("form_symbol_state", {})) or {}),
        "strategic_window_state": dict(brain_snapshot.get("strategic_window_state", entry_result.get("strategic_window_state", {})) or {}),
        "active_mcm_contact_state": dict(brain_snapshot.get("active_mcm_contact_state", entry_result.get("active_mcm_contact_state", {})) or {}),
        "state_signature": dict(brain_snapshot.get("state_signature", entry_result.get("state_signature", {})) or {}),
        "signature_bias": float(signal_state.get("signature_bias", entry_result.get("signature_bias", 0.0)) or 0.0),
        "signature_block": bool(signal_state.get("signature_block", entry_result.get("signature_block", False))),
        "signature_quality": float(signal_state.get("signature_quality", entry_result.get("signature_quality", 0.0)) or 0.0),
        "signature_distance": float(signal_state.get("signature_distance", entry_result.get("signature_distance", 0.0)) or 0.0),
        "context_cluster_id": str(signal_state.get("context_cluster_id", entry_result.get("context_cluster_id", "-")) or "-"),
        "context_cluster_bias": float(signal_state.get("context_cluster_bias", entry_result.get("context_cluster_bias", 0.0)) or 0.0),
        "context_cluster_quality": float(signal_state.get("context_cluster_quality", entry_result.get("context_cluster_quality", 0.0)) or 0.0),
        "context_cluster_distance": float(signal_state.get("context_cluster_distance", entry_result.get("context_cluster_distance", 0.0)) or 0.0),
        "context_cluster_block": bool(signal_state.get("context_cluster_block", entry_result.get("context_cluster_block", False))),
        "inhibition_level": float(signal_state.get("inhibition_level", entry_result.get("inhibition_level", 0.0)) or 0.0),
        "habituation_level": float(signal_state.get("habituation_level", entry_result.get("habituation_level", 0.0)) or 0.0),
        "competition_bias": float(signal_state.get("competition_bias", entry_result.get("competition_bias", 0.0)) or 0.0),
        "long_score": float(signal_state.get("long_score", entry_result.get("long_score", 0.0)) or 0.0),
        "short_score": float(signal_state.get("short_score", entry_result.get("short_score", 0.0)) or 0.0),
        "field_density": float(signal_state.get("field_density", entry_result.get("field_density", 0.0)) or 0.0),
        "field_stability": float(signal_state.get("field_stability", entry_result.get("field_stability", 0.0)) or 0.0),
        "regulatory_load": float(signal_state.get("regulatory_load", entry_result.get("regulatory_load", 0.0)) or 0.0),
        "action_capacity": float(signal_state.get("action_capacity", entry_result.get("action_capacity", 0.0)) or 0.0),
        "recovery_need": float(signal_state.get("recovery_need", entry_result.get("recovery_need", 0.0)) or 0.0),
        "survival_pressure": float(signal_state.get("survival_pressure", entry_result.get("survival_pressure", 0.0)) or 0.0),
        "felt_bearing_score": float(entry_result.get("felt_bearing_score", 0.0) or 0.0),
        "felt_profile_label": str(entry_result.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
        "rejection_reason": str(entry_result.get("rejection_reason", "runtime_tendency_only") or "runtime_tendency_only"),
    }


def build_runtime_entry_decision_view(
    window,
    candle_state,
    bot=None,
    *,
    tension_builder=None,
    hold_decision_builder=None,
):
    state = build_runtime_decision_tendency_view(
        window,
        candle_state,
        bot=bot,
        tension_builder=tension_builder,
        hold_decision_builder=hold_decision_builder,
    )
    if isinstance(state, dict) and "decision" not in state:
        state = dict(state)
        state["decision"] = str(state.get("proposed_decision", "WAIT") or "WAIT")
    return state
