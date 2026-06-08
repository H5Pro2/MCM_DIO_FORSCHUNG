"""Temporal and MCM spacetime perception.

This module owns DIO's time-depth perception: temporal identity, recurrence,
afterimage, memory/future bearing, spacetime pressure, and temporal modulation.
"""

import hashlib


def build_temporal_coherence_state(
    temporal_perception_state=None,
    bot=None,
    visual_market_state=None,
    structure_perception_state=None,
    form_symbol_state=None,
    state_signature=None,
    candle_state=None,
):

    previous = dict(temporal_perception_state or {})
    visual = dict(visual_market_state or {})
    structure = dict(structure_perception_state or {})
    symbol = dict(form_symbol_state or {})
    signature = dict(state_signature or {})
    candle = dict(candle_state or {})

    def _clip(value, lo=0.0, hi=1.0):
        try:
            value = float(value)
        except Exception:
            value = 0.0
        if value != value:
            value = 0.0
        return max(float(lo), min(float(hi), float(value)))

    def _flt(value, default=0.0):
        try:
            return float(value)
        except Exception:
            return float(default)

    runtime_tick = int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0) if bot is not None else 0
    timestamp = candle.get("timestamp", None)
    visual_form = dict(visual.get("visual_form_state", {}) or {})
    form_symbol_id = str(symbol.get("form_symbol_id", "") or "").strip()
    form_symbol_family_key = str(symbol.get("form_symbol_family_key", symbol.get("form_symbol_key", "")) or "").strip()
    form_symbol_variant_key = str(symbol.get("form_symbol_variant_key", "") or "").strip()
    compound_id = str(symbol.get("form_symbol_compound_id", "") or "").strip()
    compound_scope = str(symbol.get("form_symbol_compound_scope", "") or "").strip()
    uncertain_form_family_state = str(symbol.get("uncertain_form_family_state", "") or "").strip()
    visual_form_id = str(visual.get("visual_form_id", visual_form.get("visual_form_id", "")) or "").strip()
    signature_key = str(signature.get("signature_key", "") or "").strip()
    context_cluster_id = str(getattr(bot, "last_context_cluster_id", "") or "").strip() if bot is not None else ""
    inner_context_cluster_id = str(getattr(bot, "last_inner_context_cluster_id", "") or "").strip() if bot is not None else ""

    visual_bucket = "|".join(
        str(round(_flt(visual.get(key, 0.0)), 2))
        for key in ("visual_clarity", "visual_object_stability", "visual_shape_resonance", "visual_shape_fragility")
    )
    family_anchor = form_symbol_family_key or form_symbol_id or form_symbol_variant_key
    identity_parts = [
        item
        for item in (
            family_anchor,
            uncertain_form_family_state,
            compound_scope,
            context_cluster_id,
            inner_context_cluster_id,
            visual_bucket,
        )
        if item and item != "-"
    ]
    if identity_parts:
        raw_identity = "|".join(identity_parts[:5])
    else:
        raw_identity = visual_bucket
    source_identity_parts = [
        item
        for item in (
            form_symbol_id,
            compound_id,
            visual_form_id,
            context_cluster_id,
            inner_context_cluster_id,
            signature_key[:16] if signature_key else "",
        )
        if item and item != "-"
    ]
    raw_source_identity = "|".join(source_identity_parts[:6]) if source_identity_parts else raw_identity
    temporal_identity = hashlib.sha1(raw_identity.encode("utf-8", errors="ignore")).hexdigest()[:12] if raw_identity else "-"
    temporal_source_identity = hashlib.sha1(raw_source_identity.encode("utf-8", errors="ignore")).hexdigest()[:12] if raw_source_identity else temporal_identity

    previous_identity = str(previous.get("temporal_identity", "") or "").strip()
    identity_memory = dict(previous.get("temporal_identity_memory", {}) or {})
    remembered = dict(identity_memory.get(temporal_identity, {}) or {}) if temporal_identity and temporal_identity != "-" else {}
    last_seen_tick = int(remembered.get("last_seen_tick", previous.get("last_seen_tick", runtime_tick)) or runtime_tick)
    ticks_since_seen = max(0, int(runtime_tick) - int(last_seen_tick)) if remembered else 999
    previous_timestamp = previous.get("last_timestamp", None)
    same_identity = bool(temporal_identity and temporal_identity != "-" and temporal_identity == previous_identity)

    visual_clarity = _clip(visual.get("visual_clarity", 0.0))
    visual_object_stability = _clip(visual.get("visual_object_stability", 0.0))
    visual_grounding_strength = _clip(visual.get("visual_grounding_strength", visual.get("visual_object_binding", 0.0)))
    visual_form_novelty = _clip(visual.get("visual_form_novelty", 0.0))
    visual_shape_resonance = _clip(visual.get("visual_shape_resonance", 0.0))
    visual_shape_fragility = _clip(visual.get("visual_shape_fragility", 0.0))
    structure_quality = _clip(structure.get("structure_quality", 0.0))
    structure_stability = _clip(structure.get("structure_stability", 0.0))
    context_confidence = _clip(structure.get("context_confidence", 0.0))
    route_familiarity = _clip(previous.get("route_familiarity", 0.0))
    symbol_learning_trust = _clip(symbol.get("form_symbol_learning_trust", 0.0))
    symbol_action_trust = _clip(symbol.get("form_symbol_action_trust", 0.0))
    symbol_caution_trust = _clip(symbol.get("form_symbol_caution_trust", 0.0))

    previous_continuity = _clip(previous.get("temporal_continuity", 0.0))
    previous_afterimage = _clip(previous.get("temporal_afterimage", 0.0))
    previous_source_binding = _clip(previous.get("temporal_source_binding", 0.0))
    previous_self_consistency = _clip(previous.get("temporal_self_consistency", 0.0))

    recurrence_raw = 0.0
    if remembered:
        recurrence_raw = _clip((1.0 / (1.0 + (ticks_since_seen / 24.0))) + (_clip(remembered.get("seen_count", 0.0)) * 0.08))
    elif same_identity:
        recurrence_raw = 0.52

    source_binding = _clip(
        (visual_grounding_strength * 0.18)
        + (visual_object_stability * 0.14)
        + (visual_clarity * 0.12)
        + (structure_quality * 0.14)
        + (structure_stability * 0.12)
        + (context_confidence * 0.10)
        + (symbol_learning_trust * 0.08)
        + (max(symbol_action_trust, symbol_caution_trust) * 0.06)
        + (previous_source_binding * 0.06)
    )
    continuity = _clip(
        (previous_continuity * 0.20)
        + ((1.0 if same_identity else 0.0) * 0.22)
        + (recurrence_raw * 0.18)
        + (source_binding * 0.18)
        + (visual_object_stability * 0.10)
        + (structure_stability * 0.08)
        + (max(0.0, 1.0 - visual_form_novelty) * 0.04)
    )
    novelty = _clip(
        (visual_form_novelty * 0.24)
        + (visual_shape_fragility * 0.12)
        + ((0.0 if same_identity else 1.0) * 0.18)
        + (max(0.0, 0.48 - source_binding) * 0.18)
        + (max(0.0, 0.34 - recurrence_raw) * 0.12)
        - (continuity * 0.12)
    )
    afterimage = _clip(
        (previous_afterimage * 0.72)
        + (max(0.0, continuity - source_binding) * 0.12)
        + (visual_shape_resonance * 0.07)
        + (max(0.0, novelty - continuity) * 0.06)
        - (source_binding * 0.05)
    )
    memory_time_distance = _clip(1.0 if not remembered else ticks_since_seen / 96.0)
    temporal_decay = _clip((memory_time_distance * 0.58) + (afterimage * 0.18) + (max(0.0, 0.36 - continuity) * 0.16))
    temporal_context_depth = _clip(
        (continuity * 0.20)
        + (recurrence_raw * 0.16)
        + (source_binding * 0.16)
        + (structure_quality * 0.12)
        + (symbol_learning_trust * 0.10)
        + (visual_shape_resonance * 0.08)
        + (max(0.0, 1.0 - memory_time_distance) * 0.10)
        + (context_confidence * 0.08)
    )
    temporal_self_consistency = _clip(
        (previous_self_consistency * 0.18)
        + (continuity * 0.22)
        + (source_binding * 0.18)
        + (temporal_context_depth * 0.14)
        + (structure_stability * 0.10)
        + (visual_object_stability * 0.08)
        - (novelty * 0.08)
        - (temporal_decay * 0.06)
    )
    perception_sequence_coherence = _clip(
        (continuity * 0.24)
        + (temporal_self_consistency * 0.20)
        + (source_binding * 0.18)
        + (recurrence_raw * 0.12)
        + (max(0.0, 1.0 - temporal_decay) * 0.10)
        + (context_confidence * 0.08)
        - (novelty * 0.08)
    )
    memory_experience_depth = _clip(
        (max(0.0, 1.0 - memory_time_distance) * 0.30)
        + (recurrence_raw * 0.20)
        + (temporal_context_depth * 0.18)
        + (afterimage * 0.14)
        + (source_binding * 0.10)
        + (symbol_learning_trust * 0.08)
    )
    future_projection_depth = _clip(
        (temporal_context_depth * 0.22)
        + (perception_sequence_coherence * 0.18)
        + (structure_stability * 0.14)
        + (context_confidence * 0.12)
        + (max(symbol_action_trust, symbol_caution_trust) * 0.10)
        + (visual_shape_resonance * 0.10)
        + (max(0.0, 1.0 - temporal_decay) * 0.14)
    )
    mcm_spacetime_depth = _clip(
        (temporal_context_depth * 0.24)
        + (source_binding * 0.16)
        + (max(0.0, 1.0 - memory_time_distance) * 0.14)
        + (afterimage * 0.12)
        + (recurrence_raw * 0.12)
        + (visual_shape_resonance * 0.08)
        + (structure_quality * 0.08)
        + (context_confidence * 0.06)
    )
    temporal_self_location = _clip(
        (mcm_spacetime_depth * 0.22)
        + (source_binding * 0.18)
        + (continuity * 0.16)
        + (perception_sequence_coherence * 0.14)
        + (max(0.0, 1.0 - temporal_decay) * 0.12)
        + (max(0.0, 1.0 - novelty) * 0.08)
        + (previous_self_consistency * 0.10)
    )

    temporal_binding_pressures = {
        "new_contact": _clip((novelty * 0.34) + ((1.0 - continuity) * 0.16) + ((1.0 - source_binding) * 0.12)),
        "continued_contact": _clip((continuity * 0.32) + ((1.0 - memory_time_distance) * 0.16) + (source_binding * 0.10)),
        "recurrent_contact": _clip((recurrence_raw * 0.34) + (memory_time_distance * 0.12) + (temporal_context_depth * 0.10)),
        "afterimage_contact": _clip((afterimage * 0.30) + (temporal_decay * 0.16) + ((1.0 - source_binding) * 0.10)),
        "coherent_sequence": _clip((perception_sequence_coherence * 0.32) + (source_binding * 0.18) + (continuity * 0.10)),
        "aged_memory_contact": _clip((memory_time_distance * 0.30) + ((1.0 - continuity) * 0.14) + ((1.0 - source_binding) * 0.10)),
        "unbound_moment": _clip(((1.0 - max(continuity, recurrence_raw, source_binding, perception_sequence_coherence)) * 0.22) + (novelty * 0.08)),
    }
    temporal_binding_state = max(temporal_binding_pressures, key=temporal_binding_pressures.get)

    temporal_self_location_pressures = {
        "present_contact": _clip((temporal_self_location * 0.30) + (continuity * 0.16) + (perception_sequence_coherence * 0.12)),
        "afterimage_trace": _clip((afterimage * 0.30) + (temporal_decay * 0.18) + ((1.0 - temporal_self_location) * 0.08)),
        "remembered_experience": _clip((memory_experience_depth * 0.32) + (memory_time_distance * 0.12) + (recurrence_raw * 0.10)),
        "future_possibility": _clip((future_projection_depth * 0.34) + (temporal_context_depth * 0.16) + (mcm_spacetime_depth * 0.08)),
        "new_unmapped_contact": _clip((novelty * 0.30) + ((1.0 - source_binding) * 0.14) + ((1.0 - temporal_self_location) * 0.08)),
        "unlocated_contact": _clip(((1.0 - temporal_self_location) * 0.28) + ((1.0 - mcm_spacetime_depth) * 0.12)),
    }
    temporal_self_location_state = max(temporal_self_location_pressures, key=temporal_self_location_pressures.get)

    spacetime_unlocated_pressure = _clip(
        (max(0.0, 0.34 - temporal_self_location) * 0.56)
        + (max(0.0, 0.30 - mcm_spacetime_depth) * 0.34)
        + ((1.0 if temporal_self_location_state == "unlocated_contact" else 0.0) * 0.16)
        + ((1.0 if temporal_binding_state == "unbound_moment" else 0.0) * 0.10)
        + (novelty * 0.08)
        - (source_binding * 0.10)
    )
    spacetime_memory_bearing = _clip(
        (memory_experience_depth * 0.30)
        + (recurrence_raw * 0.16)
        + (temporal_context_depth * 0.16)
        + (temporal_self_location * 0.14)
        + (perception_sequence_coherence * 0.12)
        + (max(0.0, 1.0 - memory_time_distance) * 0.12)
    )
    spacetime_future_bearing = _clip(
        (future_projection_depth * 0.34)
        + (mcm_spacetime_depth * 0.20)
        + (temporal_self_location * 0.16)
        + (perception_sequence_coherence * 0.14)
        + (structure_quality * 0.08)
        + (context_confidence * 0.08)
    )
    spacetime_regulation_support = _clip(
        (spacetime_memory_bearing * 0.30)
        + (spacetime_future_bearing * 0.30)
        + (temporal_self_location * 0.18)
        + (mcm_spacetime_depth * 0.14)
        + (source_binding * 0.08)
        - (spacetime_unlocated_pressure * 0.18)
    )
    spacetime_reflection_need = _clip(
        (spacetime_unlocated_pressure * 0.36)
        + (max(0.0, future_projection_depth - temporal_self_location) * 0.16)
        + (max(0.0, mcm_spacetime_depth - memory_experience_depth) * 0.10)
        + ((1.0 if temporal_self_location_state == "future_possibility" else 0.0) * 0.06)
        + ((1.0 if temporal_self_location_state == "afterimage_trace" else 0.0) * 0.10)
        - (spacetime_memory_bearing * 0.10)
    )
    spacetime_regulation_pressures = {
        "spacetime_unlocated_reflection": _clip((spacetime_unlocated_pressure * 0.34) + ((1.0 - spacetime_regulation_support) * 0.14)),
        "afterimage_reframe": _clip((spacetime_reflection_need * 0.28) + (temporal_self_location_pressures.get("afterimage_trace", 0.0) * 0.18)),
        "memory_depth_bearing": _clip((spacetime_memory_bearing * 0.32) + (temporal_self_location_pressures.get("remembered_experience", 0.0) * 0.14)),
        "future_depth_watch": _clip((spacetime_future_bearing * 0.32) + (temporal_self_location_pressures.get("future_possibility", 0.0) * 0.14)),
        "present_depth_bearing": _clip((spacetime_regulation_support * 0.32) + (temporal_self_location_pressures.get("present_contact", 0.0) * 0.14)),
        "spacetime_open": _clip((mcm_spacetime_depth * 0.12) + ((1.0 - spacetime_unlocated_pressure) * 0.12)),
    }
    spacetime_regulation_state = max(spacetime_regulation_pressures, key=spacetime_regulation_pressures.get)

    identity_memory[temporal_identity] = {
        "last_seen_tick": int(runtime_tick),
        "last_timestamp": timestamp,
        "seen_count": int(remembered.get("seen_count", 0) or 0) + 1,
        "last_continuity": float(continuity),
        "last_source_binding": float(source_binding),
        "last_state": str(temporal_binding_state),
    }
    if len(identity_memory) > 96:
        sorted_items = sorted(
            identity_memory.items(),
            key=lambda kv: int(dict(kv[1] or {}).get("last_seen_tick", 0) or 0),
            reverse=True,
        )
        identity_memory = dict(sorted_items[:96])

    merged = dict(previous or {})
    merged.update({
        "temporal_identity": str(temporal_identity),
        "temporal_identity_source": str(raw_identity),
        "temporal_source_identity": str(temporal_source_identity),
        "temporal_source_identity_detail": str(raw_source_identity),
        "temporal_binding_state": str(temporal_binding_state),
        "temporal_binding_pressures": dict(temporal_binding_pressures),
        "temporal_continuity": float(continuity),
        "temporal_source_binding": float(source_binding),
        "temporal_recurrence": float(recurrence_raw),
        "temporal_novelty": float(novelty),
        "temporal_afterimage": float(afterimage),
        "temporal_decay": float(temporal_decay),
        "temporal_context_depth": float(temporal_context_depth),
        "mcm_spacetime_depth": float(mcm_spacetime_depth),
        "memory_experience_depth": float(memory_experience_depth),
        "future_projection_depth": float(future_projection_depth),
        "temporal_self_location": float(temporal_self_location),
        "temporal_self_location_state": str(temporal_self_location_state),
        "temporal_self_location_pressures": dict(temporal_self_location_pressures),
        "spacetime_unlocated_pressure": float(spacetime_unlocated_pressure),
        "spacetime_memory_bearing": float(spacetime_memory_bearing),
        "spacetime_future_bearing": float(spacetime_future_bearing),
        "spacetime_reflection_need": float(spacetime_reflection_need),
        "spacetime_regulation_support": float(spacetime_regulation_support),
        "spacetime_regulation_state": str(spacetime_regulation_state),
        "spacetime_regulation_pressures": dict(spacetime_regulation_pressures),
        "temporal_self_consistency": float(temporal_self_consistency),
        "perception_sequence_coherence": float(perception_sequence_coherence),
        "memory_time_distance": float(memory_time_distance),
        "temporal_structure_quality": float(structure_quality),
        "temporal_structure_stability": float(structure_stability),
        "temporal_context_confidence": float(context_confidence),
        "temporal_visual_grounding_strength": float(visual_grounding_strength),
        "temporal_ticks_since_seen": int(ticks_since_seen if remembered else 999),
        "temporal_same_identity": bool(same_identity),
        "last_seen_tick": int(runtime_tick),
        "last_timestamp": timestamp,
        "previous_timestamp": previous_timestamp,
        "temporal_identity_memory": dict(identity_memory or {}),
    })
    return dict(merged or {})

# --------------------------------------------------
def _resolve_temporal_decision_modulation(temporal_perception_state=None):

    temporal_state = dict(temporal_perception_state or {})
    flow_direction = float(temporal_state.get("flow_direction", 0.0) or 0.0)
    flow_strength = float(temporal_state.get("flow_strength", 0.0) or 0.0)
    flow_stability = float(temporal_state.get("flow_stability", 0.0) or 0.0)
    acceleration = float(temporal_state.get("acceleration", 0.0) or 0.0)
    swing_pressure = float(temporal_state.get("swing_pressure", 0.0) or 0.0)
    sequence_bias = str(temporal_state.get("sequence_bias", "neutral") or "neutral").strip().lower()
    flow_memory = float(temporal_state.get("flow_memory", 0.0) or 0.0)
    transition_pressure = float(temporal_state.get("transition_pressure", 0.0) or 0.0)
    continuation_readiness = float(temporal_state.get("continuation_readiness", 0.0) or 0.0)
    temporal_exhaustion = float(temporal_state.get("temporal_exhaustion", 0.0) or 0.0)
    temporal_coherence = float(temporal_state.get("temporal_coherence", 0.0) or 0.0)
    state_drift = float(temporal_state.get("state_drift", 0.0) or 0.0)

    directional_bias = float(((flow_direction * 0.16) + (flow_memory * 0.14)) * (1.0 + (flow_strength * 0.18) + (flow_stability * 0.12)))
    conviction_boost = float((max(0.0, flow_strength) * 0.08) + (max(0.0, flow_stability) * 0.06) + (continuation_readiness * 0.10) + (temporal_coherence * 0.08))
    caution_penalty = float((max(0.0, swing_pressure) * 0.08) + (max(0.0, 1.0 - flow_stability) * 0.05) + (transition_pressure * 0.10) + (temporal_exhaustion * 0.10))
    continuation_bias = float((max(0.0, flow_strength) * max(0.0, flow_stability) * 0.08) + (continuation_readiness * 0.12) + (max(0.0, temporal_coherence - transition_pressure) * 0.10))
    exhaustion_risk = float(min(0.28, (max(0.0, abs(acceleration)) * 0.12) + (max(0.0, swing_pressure - flow_stability) * 0.10) + (temporal_exhaustion * 0.14) + (state_drift * 0.10)))
    observe_pull = float((max(0.0, 1.0 - flow_stability) * 0.18) + (max(0.0, swing_pressure) * 0.12) + (transition_pressure * 0.18) + (temporal_exhaustion * 0.14))
    replan_pull = float((max(0.0, swing_pressure) * 0.16) + (max(0.0, abs(acceleration)) * 0.10) + (transition_pressure * 0.20) + (state_drift * 0.14))

    if sequence_bias == "up":
        long_bias = directional_bias + continuation_bias
        short_bias = -max(0.0, directional_bias * 0.42)
    elif sequence_bias == "down":
        long_bias = -max(0.0, (-directional_bias) * 0.42)
        short_bias = -directional_bias + continuation_bias
    else:
        long_bias = directional_bias * 0.42
        short_bias = -directional_bias * 0.42
        observe_pull += 0.06

    return {
        "flow_direction": float(flow_direction),
        "flow_strength": float(flow_strength),
        "flow_stability": float(flow_stability),
        "acceleration": float(acceleration),
        "swing_pressure": float(swing_pressure),
        "sequence_bias": str(sequence_bias),
        "flow_memory": float(flow_memory),
        "transition_pressure": float(transition_pressure),
        "continuation_readiness": float(continuation_readiness),
        "temporal_exhaustion": float(temporal_exhaustion),
        "temporal_coherence": float(temporal_coherence),
        "state_drift": float(state_drift),
        "long_bias": float(long_bias),
        "short_bias": float(short_bias),
        "conviction_boost": float(conviction_boost),
        "caution_penalty": float(caution_penalty),
        "continuation_bias": float(continuation_bias),
        "exhaustion_risk": float(exhaustion_risk),
        "observe_pull": float(observe_pull),
        "replan_pull": float(replan_pull),
    }

# --------------------------------------------------
def _advance_temporal_perception_state(temporal_perception_state=None, bot=None, decision_tendency="hold", market_tick_advanced=True):

    temporal_state = dict(temporal_perception_state or {})
    if not temporal_state:
        return {}

    flow_direction = float(temporal_state.get("flow_direction", 0.0) or 0.0)
    flow_strength = float(temporal_state.get("flow_strength", 0.0) or 0.0)
    flow_stability = float(temporal_state.get("flow_stability", 0.0) or 0.0)
    swing_pressure = float(temporal_state.get("swing_pressure", 0.0) or 0.0)
    flow_memory = float(temporal_state.get("flow_memory", flow_direction) or flow_direction)
    transition_pressure = float(temporal_state.get("transition_pressure", 0.0) or 0.0)
    continuation_readiness = float(temporal_state.get("continuation_readiness", 0.0) or 0.0)
    temporal_exhaustion = float(temporal_state.get("temporal_exhaustion", 0.0) or 0.0)
    temporal_coherence = float(temporal_state.get("temporal_coherence", 0.0) or 0.0)
    state_drift = float(temporal_state.get("state_drift", 0.0) or 0.0)

    inhibition_level = float(getattr(bot, "inhibition_level", 0.0) or 0.0) if bot is not None else 0.0
    competition_bias = abs(float(getattr(bot, "competition_bias", 0.0) or 0.0)) if bot is not None else 0.0
    action_capacity = float(getattr(bot, "action_capacity", 0.0) or 0.0) if bot is not None else 0.0
    regulatory_load = float(getattr(bot, "regulatory_load", 0.0) or 0.0) if bot is not None else 0.0
    recovery_need = float(getattr(bot, "recovery_need", 0.0) or 0.0) if bot is not None else 0.0

    if bool(market_tick_advanced):
        temporal_exhaustion = float(min(1.0, max(0.0, (temporal_exhaustion * 0.84) + (swing_pressure * 0.10) + (competition_bias * 0.06))))
        transition_pressure = float(min(1.0, max(0.0, (transition_pressure * 0.80) + (state_drift * 0.12) + (competition_bias * 0.08))))
    else:
        directional_decay = 0.96 if str(decision_tendency or "hold").strip().lower() == "act" else 0.92
        flow_direction = float(flow_direction * directional_decay)
        flow_strength = float(max(0.0, min(1.0, flow_strength * 0.94)))
        flow_memory = float(max(-1.0, min(1.0, (flow_memory * 0.90) + (flow_direction * 0.10))))
        transition_pressure = float(min(1.0, max(0.0, (transition_pressure * 0.92) + (competition_bias * 0.04) + (inhibition_level * 0.03))))
        temporal_exhaustion = float(min(1.0, max(0.0, (temporal_exhaustion * 0.94) + (max(0.0, regulatory_load - action_capacity) * 0.05) - (max(0.0, action_capacity - regulatory_load) * 0.03))))

    if str(decision_tendency or "hold").strip().lower() in ("observe", "hold"):
        transition_pressure = float(max(0.0, transition_pressure - 0.03))
        temporal_exhaustion = float(max(0.0, temporal_exhaustion - 0.02))
    elif str(decision_tendency or "hold").strip().lower() == "replan":
        transition_pressure = float(min(1.0, transition_pressure + 0.04))
        state_drift = float(min(1.0, state_drift + 0.03))

    continuation_readiness = float(min(1.0, max(0.0, (continuation_readiness * 0.76) + (flow_strength * 0.10) + (flow_stability * 0.08) + (max(0.0, action_capacity - regulatory_load) * 0.10) - (transition_pressure * 0.10) - (temporal_exhaustion * 0.08))))
    temporal_coherence = float(min(1.0, max(0.0, (temporal_coherence * 0.74) + (flow_stability * 0.12) + (continuation_readiness * 0.10) + (max(0.0, 1.0 - transition_pressure) * 0.08) - (recovery_need * 0.06))))

    temporal_state["flow_direction"] = float(flow_direction)
    temporal_state["flow_strength"] = float(flow_strength)
    temporal_state["flow_memory"] = float(flow_memory)
    temporal_state["transition_pressure"] = float(transition_pressure)
    temporal_state["continuation_readiness"] = float(continuation_readiness)
    temporal_state["temporal_exhaustion"] = float(temporal_exhaustion)
    temporal_state["temporal_coherence"] = float(temporal_coherence)
    temporal_state["state_drift"] = float(state_drift)
    return dict(temporal_state)

# --------------------------------------------------


__all__ = [
    "build_temporal_coherence_state",
    "_resolve_temporal_decision_modulation",
    "_advance_temporal_perception_state",
]
