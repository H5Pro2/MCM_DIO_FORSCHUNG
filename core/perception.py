"""DIO perception construction.

This module owns the outer/world perception parts that are independent from the
live MCM field object: world state, outer visual perception, processing state,
and high-level perception state.
"""

from core.visual_attention import build_visual_attention_state
from core.area_perception import build_area_perception_profile
from core.visual_cortex import build_visual_cortex_state

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


def _as_dict(value):
    return dict(value or {}) if isinstance(value, dict) else {}


def _float_from(*sources, key, default=0.0):
    for source in sources:
        if isinstance(source, dict) and key in source:
            try:
                return float(source.get(key, default) or default)
            except Exception:
                return float(default)
    return float(default)


def _int_from(*sources, key, default=0):
    for source in sources:
        if isinstance(source, dict) and key in source:
            try:
                return int(source.get(key, default) or default)
            except Exception:
                return int(default)
    return int(default)


def _str_from(*sources, key, default=""):
    for source in sources:
        if isinstance(source, dict) and key in source:
            return str(source.get(key, default) or default)
    return str(default)



def build_world_state(candle_state, tension_state, stimulus, visual_market_state=None, structure_perception_state=None, temporal_perception_state=None):
    temporal_state = dict(temporal_perception_state or {})
    world_motion_afterimage_state = dict(temporal_state.get("world_motion_afterimage_state", {}) or {})
    return {
        "candle_state": dict(candle_state or {}),
        "tension_state": dict(tension_state or {}),
        "vision": dict((stimulus or {}).get("vision", {}) or {}),
        "filtered_vision": dict((stimulus or {}).get("filtered_vision", {}) or {}),
        "focus": dict((stimulus or {}).get("focus", {}) or {}),
        "visual_market_state": dict(visual_market_state or {}),
        "structure_perception_state": dict(structure_perception_state or {}),
        "temporal_perception_state": dict(temporal_state or {}),
        "world_motion_afterimage_state": dict(world_motion_afterimage_state or {}),
    }

def build_outer_visual_perception_state(world_state):
    world = dict(world_state or {})
    focus = dict(world.get("focus", {}) or {})
    filtered_vision = dict(world.get("filtered_vision", {}) or {})
    vision = dict(world.get("vision", {}) or {})
    visual_market_state = dict(world.get("visual_market_state", {}) or {})
    structure_perception_state = dict(world.get("structure_perception_state", {}) or {})
    temporal_perception_state = dict(world.get("temporal_perception_state", {}) or {})
    core_visual_trace_state = _as_dict(visual_market_state.get("core_visual_trace_state"))
    core_visual_interpretation_state = _as_dict(visual_market_state.get("core_visual_interpretation_state"))
    trace_form_axes = _as_dict(core_visual_trace_state.get("form_axes"))
    world_motion_afterimage_state = dict(world.get("world_motion_afterimage_state", {}) or {})

    spatial_bias = _float_from(core_visual_interpretation_state, visual_market_state, key="spatial_bias")
    directional_bias = _float_from(core_visual_interpretation_state, visual_market_state, key="directional_bias")
    range_position = _float_from(core_visual_trace_state, visual_market_state, key="range_position")
    range_width = _float_from(core_visual_trace_state, visual_market_state, key="range_width")
    short_impulse = _float_from(core_visual_interpretation_state, visual_market_state, key="short_impulse")
    mid_impulse = _float_from(core_visual_interpretation_state, visual_market_state, key="mid_impulse")
    compression = _float_from(core_visual_trace_state, visual_market_state, key="compression")
    expansion = _float_from(core_visual_trace_state, visual_market_state, key="expansion")
    body_pressure = _float_from(core_visual_interpretation_state, visual_market_state, key="body_pressure")
    wick_pressure = _float_from(core_visual_interpretation_state, visual_market_state, key="wick_pressure")
    volume_bias = _float_from(core_visual_interpretation_state, visual_market_state, key="volume_bias")
    market_balance = _float_from(core_visual_interpretation_state, visual_market_state, key="market_balance")
    breakout_tension = _float_from(core_visual_interpretation_state, visual_market_state, key="breakout_tension")
    visual_coherence = _float_from(core_visual_trace_state, visual_market_state, key="visual_coherence")
    visual_sight_state = dict(visual_market_state.get("visual_sight_state", {}) or {})
    if not visual_sight_state:
        for source in (core_visual_trace_state, core_visual_interpretation_state):
            candidate = source.get("visual_sight_state") if isinstance(source, dict) else None
            if isinstance(candidate, dict) and candidate:
                visual_sight_state = dict(candidate)
                break
    visual_cortex_state = dict(visual_market_state.get("visual_cortex_state", {}) or {})
    if not visual_cortex_state:
        for source in (core_visual_trace_state, core_visual_interpretation_state):
            candidate = source.get("visual_cortex_state") if isinstance(source, dict) else None
            if isinstance(candidate, dict) and candidate:
                visual_cortex_state = dict(candidate)
                break
    visual_cortex_state = build_visual_cortex_state(
        visual_sight_state,
        visual_market_state,
        structure_perception_state,
        temporal_perception_state,
    )
    visual_form_state = dict(visual_market_state.get("visual_form_state", {}) or {})
    visual_clarity = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_clarity")
    visual_object_stability = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_object_stability")
    visual_form_novelty = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_form_novelty")
    visual_blindness = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_blindness")
    visual_form_pressure = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_form_pressure")
    visual_shape_resonance = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_shape_resonance")
    visual_shape_fragility = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_shape_fragility")
    visual_attention_state = dict(visual_market_state.get("visual_attention_state", {}) or {})
    if not visual_attention_state:
        visual_attention_state = build_visual_attention_state(
            {
                "visual_clarity": visual_clarity,
                "visual_object_stability": visual_object_stability,
                "visual_form_novelty": visual_form_novelty,
                "visual_blindness": visual_blindness,
                "visual_form_pressure": visual_form_pressure,
                "visual_shape_resonance": visual_shape_resonance,
                "visual_shape_fragility": visual_shape_fragility,
                "visual_coherence": visual_coherence,
                "market_balance": market_balance,
            },
            focus,
        )
    sensory_state = _as_dict(core_visual_interpretation_state.get("sensory_reality"))
    sensory_reality_pressure = _float_from(sensory_state, core_visual_interpretation_state, visual_market_state, key="sensory_reality_pressure")
    sensory_load = _float_from(sensory_state, core_visual_interpretation_state, visual_market_state, key="sensory_load")
    sensory_redundancy = _float_from(sensory_state, visual_market_state, key="sensory_redundancy")
    sensory_habituation = _float_from(sensory_state, visual_market_state, key="sensory_habituation")
    sensory_gate = _float_from(sensory_state, core_visual_interpretation_state, visual_market_state, key="sensory_gate", default=1.0)
    sensory_active_axis_count = _int_from(sensory_state, visual_market_state, key="sensory_active_axis_count")
    sensory_primary_pressure = _float_from(sensory_state, visual_market_state, key="sensory_primary_pressure")
    sensory_reality_label = _str_from(sensory_state, core_visual_interpretation_state, visual_market_state, key="sensory_reality_label", default="quiet_outer_reality")
    visual_attention_state = dict(visual_market_state.get("visual_attention_state", {}) or {})
    if not visual_attention_state:
        visual_attention_state = build_visual_attention_state(
            {
                "visual_clarity": visual_clarity,
                "visual_object_stability": visual_object_stability,
                "visual_form_novelty": visual_form_novelty,
                "visual_blindness": visual_blindness,
                "visual_form_pressure": visual_form_pressure,
                "visual_shape_resonance": visual_shape_resonance,
                "visual_shape_fragility": visual_shape_fragility,
                "visual_coherence": visual_coherence,
                "market_balance": market_balance,
                "sensory_load": sensory_load,
                "sensory_habituation": sensory_habituation,
                "sensory_primary_pressure": sensory_primary_pressure,
            },
            focus,
        )
    world_motion_afterimage_strength = _clip01(world_motion_afterimage_state.get("world_motion_afterimage_strength", 0.0))
    world_motion_afterimage_pressure = _clip01(world_motion_afterimage_state.get("world_motion_afterimage_pressure", 0.0))
    world_motion_afterimage_direction = max(-1.0, min(1.0, float(world_motion_afterimage_state.get("world_motion_afterimage_direction", 0.0) or 0.0)))
    world_motion_afterimage_volatility = _clip01(world_motion_afterimage_state.get("world_motion_afterimage_volatility", 0.0))
    world_motion_afterimage_acceleration = max(-1.0, min(1.0, float(world_motion_afterimage_state.get("world_motion_afterimage_acceleration", 0.0) or 0.0)))
    world_motion_afterimage_label = str(world_motion_afterimage_state.get("world_motion_afterimage_label", "motion_afterimage_clear") or "motion_afterimage_clear")
    motion_approach_pressure = _clip01(world_motion_afterimage_state.get("motion_approach_pressure", 0.0))
    motion_recession_pressure = _clip01(world_motion_afterimage_state.get("motion_recession_pressure", 0.0))
    contact_frequency_shift = _clip01(world_motion_afterimage_state.get("contact_frequency_shift", 0.0))
    afterimage_doppler_bias = max(-1.0, min(1.0, float(world_motion_afterimage_state.get("afterimage_doppler_bias", 0.0) or 0.0)))
    future_variant_pressure = _clip01(world_motion_afterimage_state.get("future_variant_pressure", 0.0))
    afterimage_action_maturity = _clip01(world_motion_afterimage_state.get("afterimage_action_maturity", 0.0))
    afterimage_doppler_label = str(world_motion_afterimage_state.get("afterimage_doppler_label", "doppler_clear") or "doppler_clear")
    signal_relevance = max(
        0.0,
        min(
            1.0,
            (float(focus.get("signal_relevance", 0.0) or 0.0) * 0.42)
            + (visual_coherence * 0.20)
            + (market_balance * 0.16)
            + (max(0.0, 1.0 - wick_pressure) * 0.10)
            + (max(0.0, 1.0 - min(1.0, abs(volume_bias))) * 0.12),
        ),
    )

    visual_contrast = max(
        0.0,
        min(
            1.0,
            (abs(spatial_bias - directional_bias) * 0.24)
            + (abs(range_position) * 0.18)
            + (expansion * 0.18)
            + (wick_pressure * 0.12)
            + (abs(volume_bias) * 0.10)
            + (world_motion_afterimage_pressure * 0.10)
            + (world_motion_afterimage_volatility * 0.08)
            + (float(vision.get("vision_contrast", 0.0) or 0.0) * 0.12),
        ),
    )
    visual_attention_state = build_visual_attention_state(
        {
            "visual_clarity": visual_clarity,
            "visual_object_stability": visual_object_stability,
            "visual_form_novelty": visual_form_novelty,
            "visual_blindness": visual_blindness,
            "visual_form_pressure": visual_form_pressure,
            "visual_shape_resonance": visual_shape_resonance,
            "visual_shape_fragility": visual_shape_fragility,
            "visual_coherence": visual_coherence,
            "market_balance": market_balance,
            "visual_contrast": visual_contrast,
            "sensory_load": sensory_load,
            "sensory_habituation": sensory_habituation,
            "sensory_primary_pressure": sensory_primary_pressure,
        },
        focus,
    )

    return {
        "focus_direction": float(focus.get("focus_direction", 0.0) or 0.0),
        "focus_strength": float(focus.get("focus_strength", 0.0) or 0.0),
        "focus_confidence": float(focus.get("focus_confidence", 0.0) or 0.0),
        "target_lock": float(focus.get("target_lock", 0.0) or 0.0),
        "noise_damp": float(focus.get("noise_damp", 0.0) or 0.0),
        "signal_relevance": float(signal_relevance),
        "visual_target_map": float(filtered_vision.get("target_map", 0.0) or 0.0),
        "visual_threat_map": float(filtered_vision.get("threat_map", 0.0) or 0.0),
        "visual_optic_flow": float(filtered_vision.get("optic_flow", 0.0) or 0.0),
        "visual_contrast": float(visual_contrast),
        "spatial_bias": float(spatial_bias),
        "directional_bias": float(directional_bias),
        "range_position": float(range_position),
        "range_width": float(range_width),
        "short_impulse": float(short_impulse),
        "mid_impulse": float(mid_impulse),
        "compression": float(compression),
        "expansion": float(expansion),
        "body_pressure": float(body_pressure),
        "wick_pressure": float(wick_pressure),
        "volume_bias": float(volume_bias),
        "market_balance": float(market_balance),
        "breakout_tension": float(breakout_tension),
        "visual_coherence": float(visual_coherence),
        "visual_sight_state": dict(visual_sight_state),
        "visual_cortex_state": dict(visual_cortex_state),
        "visual_form_state": dict(visual_form_state or {}),
        "core_visual_trace_state": dict(core_visual_trace_state),
        "core_visual_interpretation_state": dict(core_visual_interpretation_state),
        "visual_trace_form_axes": dict(trace_form_axes),
        "visual_clarity": float(visual_clarity),
        "visual_object_stability": float(visual_object_stability),
        "visual_form_novelty": float(visual_form_novelty),
        "visual_blindness": float(visual_blindness),
        "visual_form_pressure": float(visual_form_pressure),
        "visual_shape_resonance": float(visual_shape_resonance),
        "visual_shape_fragility": float(visual_shape_fragility),
        "visual_attention_state": dict(visual_attention_state),
        "visual_attention_label": str(visual_attention_state.get("visual_attention_label", "background_form")),
        "visual_form_contact": float(visual_attention_state.get("visual_form_contact", 0.0) or 0.0),
        "visual_inspection_pull": float(visual_attention_state.get("visual_inspection_pull", 0.0) or 0.0),
        "visual_attention_depth": float(visual_attention_state.get("visual_attention_depth", 0.0) or 0.0),
        "visual_background_filter": float(visual_attention_state.get("visual_background_filter", 0.0) or 0.0),
        "visual_mcm_contact_weight": float(visual_attention_state.get("visual_mcm_contact_weight", 0.0) or 0.0),
        "sensory_reality_pressure": float(sensory_reality_pressure),
        "sensory_load": float(sensory_load),
        "sensory_redundancy": float(sensory_redundancy),
        "sensory_habituation": float(sensory_habituation),
        "sensory_gate": float(sensory_gate),
        "sensory_active_axis_count": int(sensory_active_axis_count),
        "sensory_primary_pressure": float(sensory_primary_pressure),
        "sensory_reality_label": str(sensory_reality_label),
        "world_motion_afterimage_strength": float(world_motion_afterimage_strength),
        "world_motion_afterimage_pressure": float(world_motion_afterimage_pressure),
        "world_motion_afterimage_direction": float(world_motion_afterimage_direction),
        "world_motion_afterimage_volatility": float(world_motion_afterimage_volatility),
        "world_motion_afterimage_acceleration": float(world_motion_afterimage_acceleration),
        "world_motion_afterimage_label": str(world_motion_afterimage_label),
        "motion_approach_pressure": float(motion_approach_pressure),
        "motion_recession_pressure": float(motion_recession_pressure),
        "contact_frequency_shift": float(contact_frequency_shift),
        "afterimage_doppler_bias": float(afterimage_doppler_bias),
        "future_variant_pressure": float(future_variant_pressure),
        "afterimage_action_maturity": float(afterimage_action_maturity),
        "afterimage_doppler_label": str(afterimage_doppler_label),
    }

def build_processing_state(outer_visual_perception_state, inner_field_perception_state, perception_state):
    outer = dict(outer_visual_perception_state or {})
    inner = dict(inner_field_perception_state or {})
    perception = dict(perception_state or {})

    signal_relevance = float(outer.get("signal_relevance", 0.0) or 0.0)
    visual_contrast = float(outer.get("visual_contrast", 0.0) or 0.0)
    visual_coherence = float(outer.get("visual_coherence", perception.get("visual_coherence", 0.0)) or 0.0)
    visual_clarity = float(outer.get("visual_clarity", perception.get("visual_clarity", 0.0)) or 0.0)
    visual_object_stability = float(outer.get("visual_object_stability", perception.get("visual_object_stability", 0.0)) or 0.0)
    visual_form_novelty = float(outer.get("visual_form_novelty", perception.get("visual_form_novelty", 0.0)) or 0.0)
    visual_blindness = float(outer.get("visual_blindness", perception.get("visual_blindness", 0.0)) or 0.0)
    visual_form_pressure = float(outer.get("visual_form_pressure", perception.get("visual_form_pressure", 0.0)) or 0.0)
    visual_shape_resonance = float(outer.get("visual_shape_resonance", perception.get("visual_shape_resonance", 0.0)) or 0.0)
    visual_shape_fragility = float(outer.get("visual_shape_fragility", perception.get("visual_shape_fragility", 0.0)) or 0.0)
    market_balance = float(outer.get("market_balance", perception.get("market_balance", 0.0)) or 0.0)
    visual_attention_state = dict(outer.get("visual_attention_state", perception.get("visual_attention_state", {})) or {})
    if not visual_attention_state:
        visual_attention_state = build_visual_attention_state(
            {
                "visual_clarity": visual_clarity,
                "visual_object_stability": visual_object_stability,
                "visual_form_novelty": visual_form_novelty,
                "visual_blindness": visual_blindness,
                "visual_form_pressure": visual_form_pressure,
                "visual_shape_resonance": visual_shape_resonance,
                "visual_shape_fragility": visual_shape_fragility,
                "visual_coherence": visual_coherence,
                "market_balance": market_balance,
                "visual_contrast": visual_contrast,
            }
        )
    visual_attention_label = str(visual_attention_state.get("visual_attention_label", "background_form") or "background_form")
    visual_form_contact = float(visual_attention_state.get("visual_form_contact", 0.0) or 0.0)
    visual_inspection_pull = float(visual_attention_state.get("visual_inspection_pull", 0.0) or 0.0)
    visual_attention_depth = float(visual_attention_state.get("visual_attention_depth", 0.0) or 0.0)
    visual_background_filter = float(visual_attention_state.get("visual_background_filter", 0.0) or 0.0)
    visual_mcm_contact_weight = float(visual_attention_state.get("visual_mcm_contact_weight", 0.0) or 0.0)
    breakout_tension = float(outer.get("breakout_tension", perception.get("breakout_tension", 0.0)) or 0.0)
    spatial_bias = float(outer.get("spatial_bias", perception.get("spatial_bias", 0.0)) or 0.0)
    directional_bias = float(outer.get("directional_bias", perception.get("directional_bias", 0.0)) or 0.0)
    world_motion_afterimage_strength = float(outer.get("world_motion_afterimage_strength", perception.get("world_motion_afterimage_strength", 0.0)) or 0.0)
    world_motion_afterimage_pressure = float(outer.get("world_motion_afterimage_pressure", perception.get("world_motion_afterimage_pressure", 0.0)) or 0.0)
    world_motion_afterimage_volatility = float(outer.get("world_motion_afterimage_volatility", perception.get("world_motion_afterimage_volatility", 0.0)) or 0.0)
    world_motion_afterimage_direction = float(outer.get("world_motion_afterimage_direction", perception.get("world_motion_afterimage_direction", 0.0)) or 0.0)
    world_motion_afterimage_acceleration = float(outer.get("world_motion_afterimage_acceleration", perception.get("world_motion_afterimage_acceleration", 0.0)) or 0.0)
    world_motion_afterimage_label = str(outer.get("world_motion_afterimage_label", perception.get("world_motion_afterimage_label", "motion_afterimage_clear")) or "motion_afterimage_clear")
    motion_approach_pressure = float(outer.get("motion_approach_pressure", perception.get("motion_approach_pressure", 0.0)) or 0.0)
    motion_recession_pressure = float(outer.get("motion_recession_pressure", perception.get("motion_recession_pressure", 0.0)) or 0.0)
    contact_frequency_shift = float(outer.get("contact_frequency_shift", perception.get("contact_frequency_shift", 0.0)) or 0.0)
    afterimage_doppler_bias = float(outer.get("afterimage_doppler_bias", perception.get("afterimage_doppler_bias", 0.0)) or 0.0)
    future_variant_pressure = float(outer.get("future_variant_pressure", perception.get("future_variant_pressure", 0.0)) or 0.0)
    afterimage_action_maturity = float(outer.get("afterimage_action_maturity", perception.get("afterimage_action_maturity", 0.0)) or 0.0)
    afterimage_doppler_label = str(outer.get("afterimage_doppler_label", perception.get("afterimage_doppler_label", "doppler_clear")) or "doppler_clear")
    zone_proximity = float(perception.get("zone_proximity", 0.0) or 0.0)
    field_risk = abs(float(inner.get("field_mean_risk", 0.0) or 0.0))
    field_pressure = float(inner.get("field_regulation_pressure", 0.0) or 0.0)
    field_areal_count = int(inner.get("field_areal_count", 0) or 0)
    field_areal_stability_mean = float(inner.get("field_areal_stability_mean", 0.0) or 0.0)
    field_areal_pressure_mean = float(inner.get("field_areal_pressure_mean", 0.0) or 0.0)
    field_areal_drift = float(inner.get("field_areal_drift", 0.0) or 0.0)
    field_areal_dominance = float(inner.get("field_areal_dominance", 0.0) or 0.0)
    field_areal_fragmentation = float(inner.get("field_areal_fragmentation", 0.0) or 0.0)
    field_areal_coherence_mean = float(inner.get("field_areal_coherence_mean", 0.0) or 0.0)
    field_areal_conflict_mean = float(inner.get("field_areal_conflict_mean", 0.0) or 0.0)
    field_activity_island_count = int(inner.get("field_activity_island_count", 0) or 0)
    field_activity_island_mass_mean = float(inner.get("field_activity_island_mass_mean", 0.0) or 0.0)
    field_activity_island_mass_max = float(inner.get("field_activity_island_mass_max", 0.0) or 0.0)
    field_activity_island_activation_mean = float(inner.get("field_activity_island_activation_mean", 0.0) or 0.0)
    field_activity_island_pressure_mean = float(inner.get("field_activity_island_pressure_mean", 0.0) or 0.0)
    field_activity_island_coherence_mean = float(inner.get("field_activity_island_coherence_mean", 0.0) or 0.0)
    field_activity_island_context_reactivation_mean = float(inner.get("field_activity_island_context_reactivation_mean", 0.0) or 0.0)
    field_activity_island_spread = float(inner.get("field_activity_island_spread", 0.0) or 0.0)
    field_neuron_activation_mean = float(inner.get("field_neuron_activation_mean", 0.0) or 0.0)
    field_neuron_stability_mean = float(inner.get("field_neuron_stability_mean", 0.0) or 0.0)
    field_neuron_memory_resonance_mean = float(inner.get("field_neuron_memory_resonance_mean", 0.0) or 0.0)
    raw_field_perception_focus = float(inner.get("field_perception_focus", 0.0) or 0.0)
    raw_field_perception_clarity = float(inner.get("field_perception_clarity", 0.0) or 0.0)
    raw_field_perception_stability = float(inner.get("field_perception_stability", 0.0) or 0.0)
    raw_field_perception_fragmentation = float(inner.get("field_perception_fragmentation", 0.0) or 0.0)
    raw_field_perception_strain = float(inner.get("field_perception_strain", 0.0) or 0.0)
    dominant_activity_island_id = str(inner.get("dominant_activity_island_id", "-") or "-")
    field_perception_label = str(inner.get("field_perception_label", "quiet_field") or "quiet_field").strip().lower()
    uncertainty = float(perception.get("uncertainty_score", 0.0) or 0.0)
    novelty = float(perception.get("novelty_score", 0.0) or 0.0)
    structure_quality = float(perception.get("structure_quality", 0.0) or 0.0)
    structure_stability = float(perception.get("structure_stability", 0.0) or 0.0)

    visual_alignment = max(0.0, min(1.0, 1.0 - abs(spatial_bias - directional_bias)))
    areal_presence = max(0.0, min(1.0, float(field_areal_count) / 4.0))
    activity_island_presence = max(0.0, min(1.0, float(field_activity_island_count) / 4.0))
    coherent_field_bonus = 0.10 if field_perception_label == "coherent_perception_field" else 0.0
    active_field_bonus = 0.06 if field_perception_label == "active_perception_field" else 0.0
    memory_field_bonus = 0.05 if field_perception_label == "memory_reactivated_field" else 0.0
    strained_field_bonus = 0.10 if field_perception_label == "strained_field" else 0.0
    fragmented_field_bonus = 0.14 if field_perception_label == "fragmented_perception_field" else 0.0

    field_perception_pressure = max(
        0.0,
        min(
            1.0,
            (field_activity_island_pressure_mean * 0.24)
            + (raw_field_perception_strain * 0.22)
            + (raw_field_perception_fragmentation * 0.14)
            + (field_activity_island_activation_mean * 0.12)
            + (field_activity_island_spread * 0.08)
            + (activity_island_presence * 0.08)
            + (field_activity_island_context_reactivation_mean * 0.08)
            + strained_field_bonus
            + fragmented_field_bonus
            - (field_activity_island_coherence_mean * 0.08)
            - (raw_field_perception_clarity * 0.08),
        ),
    )

    field_perception_support = max(
        0.0,
        min(
            1.0,
            (field_activity_island_coherence_mean * 0.22)
            + (raw_field_perception_stability * 0.22)
            + (raw_field_perception_focus * 0.14)
            + (field_activity_island_mass_max * 0.10)
            + (field_activity_island_mass_mean * 0.08)
            + (field_activity_island_activation_mean * 0.10)
            + (field_activity_island_context_reactivation_mean * 0.08)
            + coherent_field_bonus
            + active_field_bonus
            + memory_field_bonus
            - (field_activity_island_pressure_mean * 0.12)
            - (raw_field_perception_fragmentation * 0.12)
            - (fragmented_field_bonus * 0.70),
        ),
    )

    field_perception_clarity = max(
        0.0,
        min(
            1.0,
            (field_perception_support * 0.38)
            + (raw_field_perception_clarity * 0.26)
            + (raw_field_perception_focus * 0.14)
            + (field_activity_island_coherence_mean * 0.12)
            + (max(0.0, 1.0 - field_perception_pressure) * 0.10),
        ),
    )

    field_perception_focus = max(
        raw_field_perception_focus,
        max(
            0.0,
            min(
                1.0,
                (visual_mcm_contact_weight * 0.24)
                + (activity_island_presence * 0.20)
                + (field_neuron_activation_mean * 0.18)
                + (field_areal_dominance * 0.14)
                + (field_activity_island_mass_max * 0.12)
                + (field_neuron_memory_resonance_mean * 0.08)
                - (field_perception_pressure * 0.08),
            ),
        ),
    )

    processing_areal_tension = max(
        0.0,
        min(
            1.0,
            (field_areal_pressure_mean * 0.26)
            + (field_areal_conflict_mean * 0.24)
            + (field_areal_fragmentation * 0.22)
            + (field_perception_pressure * 0.10)
            + (min(1.0, field_areal_drift) * 0.12)
            + (areal_presence * 0.08)
            - (field_areal_coherence_mean * 0.10)
            - (field_areal_stability_mean * 0.08),
        ),
    )

    processing_areal_support = max(
        0.0,
        min(
            1.0,
            (field_areal_stability_mean * 0.28)
            + (field_areal_coherence_mean * 0.24)
            + (field_perception_support * 0.12)
            + (field_areal_dominance * 0.12)
            + (max(0.0, 1.0 - field_areal_fragmentation) * 0.16)
            + (max(0.0, 1.0 - min(1.0, field_areal_drift)) * 0.10)
            + (max(0.0, 1.0 - field_areal_conflict_mean) * 0.10),
        ),
    )

    field_perception_stability = max(
        raw_field_perception_stability,
        max(
            0.0,
            min(
                1.0,
                (field_perception_support * 0.30)
                + (field_areal_stability_mean * 0.22)
                + (field_neuron_stability_mean * 0.20)
                + (processing_areal_support * 0.12)
                + (max(0.0, 1.0 - field_perception_pressure) * 0.10)
                + (max(0.0, 1.0 - processing_areal_tension) * 0.08)
                - (field_areal_fragmentation * 0.08),
            ),
        ),
    )

    processing_tension = max(
        0.0,
        min(
            1.0,
            (breakout_tension * 0.30)
            + (visual_contrast * 0.16)
            + (uncertainty * 0.14)
            + (world_motion_afterimage_pressure * 0.08)
            + (world_motion_afterimage_volatility * 0.05)
            + (future_variant_pressure * 0.05)
            + (contact_frequency_shift * 0.04)
            + (field_pressure * 0.12)
            + (processing_areal_tension * 0.14)
            + (field_perception_pressure * 0.08)
            + (max(0.0, abs(spatial_bias) - market_balance) * 0.08)
            - (visual_coherence * 0.08)
            - (processing_areal_support * 0.06),
        ),
    )

    processing_load = max(
        0.0,
        min(
            1.0,
            (uncertainty * 0.22)
            + (novelty * 0.12)
            + (field_pressure * 0.14)
            + (field_risk * 0.08)
            + (visual_contrast * 0.06)
            + (world_motion_afterimage_pressure * 0.08)
            + (world_motion_afterimage_strength * 0.04)
            + (future_variant_pressure * 0.04)
            + (contact_frequency_shift * 0.03)
            + (breakout_tension * 0.12)
            + (processing_areal_tension * 0.16)
            + (field_perception_pressure * 0.10)
            + (max(0.0, 1.0 - visual_alignment) * 0.06)
            - (structure_stability * 0.04)
            - (market_balance * 0.06)
            - (visual_coherence * 0.08)
            - (processing_areal_support * 0.08),
        ),
    )

    processing_alignment = max(
        0.0,
        min(
            1.0,
            (visual_alignment * 0.28)
            + (market_balance * 0.18)
            + (visual_coherence * 0.14)
            + (signal_relevance * 0.08)
            + (zone_proximity * 0.06)
            + (structure_quality * 0.08)
            + (processing_areal_support * 0.14)
            + (field_perception_clarity * 0.08)
            - (processing_areal_tension * 0.10),
        ),
    )

    processing_stability = max(
        0.0,
        min(
            1.0,
            (signal_relevance * 0.18)
            + (max(0.0, 1.0 - uncertainty) * 0.14)
            + (max(0.0, 1.0 - min(1.0, field_risk)) * 0.10)
            + (structure_quality * 0.08)
            + (structure_stability * 0.08)
            + (market_balance * 0.12)
            + (visual_coherence * 0.10)
            + (processing_alignment * 0.10)
            + (processing_areal_support * 0.16)
            + (field_perception_clarity * 0.08)
            - (processing_tension * 0.10)
            - (processing_areal_tension * 0.10),
        ),
    )

    processing_readiness = max(
        0.0,
        min(
            1.0,
            (processing_stability * 0.44)
            + (max(0.0, 1.0 - processing_load) * 0.24)
            + (processing_alignment * 0.16)
            + (processing_areal_support * 0.16)
            + (field_perception_clarity * 0.08)
            - (field_perception_pressure * 0.06),
        ),
    )

    return {
        "processing_load": float(processing_load),
        "processing_stability": float(processing_stability),
        "processing_readiness": float(processing_readiness),
        "processing_alignment": float(processing_alignment),
        "processing_tension": float(processing_tension),
        "processing_areal_tension": float(processing_areal_tension),
        "processing_areal_support": float(processing_areal_support),
        "visual_clarity": float(visual_clarity),
        "visual_object_stability": float(visual_object_stability),
        "visual_form_novelty": float(visual_form_novelty),
        "visual_blindness": float(visual_blindness),
        "visual_form_pressure": float(visual_form_pressure),
        "visual_shape_resonance": float(visual_shape_resonance),
        "visual_shape_fragility": float(visual_shape_fragility),
        "visual_attention_state": dict(visual_attention_state),
        "visual_attention_label": str(visual_attention_label),
        "visual_form_contact": float(visual_form_contact),
        "visual_inspection_pull": float(visual_inspection_pull),
        "visual_attention_depth": float(visual_attention_depth),
        "visual_background_filter": float(visual_background_filter),
        "visual_mcm_contact_weight": float(visual_mcm_contact_weight),
        "world_motion_afterimage_strength": float(world_motion_afterimage_strength),
        "world_motion_afterimage_pressure": float(world_motion_afterimage_pressure),
        "world_motion_afterimage_volatility": float(world_motion_afterimage_volatility),
        "world_motion_afterimage_direction": float(world_motion_afterimage_direction),
        "world_motion_afterimage_acceleration": float(world_motion_afterimage_acceleration),
        "world_motion_afterimage_label": str(world_motion_afterimage_label),
        "motion_approach_pressure": float(motion_approach_pressure),
        "motion_recession_pressure": float(motion_recession_pressure),
        "contact_frequency_shift": float(contact_frequency_shift),
        "afterimage_doppler_bias": float(afterimage_doppler_bias),
        "future_variant_pressure": float(future_variant_pressure),
        "afterimage_action_maturity": float(afterimage_action_maturity),
        "afterimage_doppler_label": str(afterimage_doppler_label),
        "field_perception_pressure": float(field_perception_pressure),
        "field_perception_support": float(field_perception_support),
        "field_perception_clarity": float(field_perception_clarity),
        "field_perception_focus": float(field_perception_focus),
        "field_perception_stability": float(field_perception_stability),
        "field_perception_fragmentation": float(raw_field_perception_fragmentation),
        "field_perception_strain": float(raw_field_perception_strain),
        "dominant_activity_island_id": str(dominant_activity_island_id),
        "field_perception_label": str(field_perception_label),
        "field_activity_island_count": int(field_activity_island_count),
        "field_activity_island_mass_mean": float(field_activity_island_mass_mean),
        "field_activity_island_mass_max": float(field_activity_island_mass_max),
        "field_activity_island_activation_mean": float(field_activity_island_activation_mean),
        "field_activity_island_pressure_mean": float(field_activity_island_pressure_mean),
        "field_activity_island_coherence_mean": float(field_activity_island_coherence_mean),
        "field_activity_island_context_reactivation_mean": float(field_activity_island_context_reactivation_mean),
        "field_activity_island_spread": float(field_activity_island_spread),
        "field_areal_count": int(field_areal_count),
        "field_areal_stability_mean": float(field_areal_stability_mean),
        "field_areal_pressure_mean": float(field_areal_pressure_mean),
        "field_areal_drift": float(field_areal_drift),
        "field_areal_dominance": float(field_areal_dominance),
        "field_areal_fragmentation": float(field_areal_fragmentation),
        "field_areal_coherence_mean": float(field_areal_coherence_mean),
        "field_areal_conflict_mean": float(field_areal_conflict_mean),
    }

def build_perception_state(world_state, bot=None):

    world = dict(world_state or {})
    candle_state = dict(world.get("candle_state", {}) or {})
    tension_state = dict(world.get("tension_state", {}) or {})
    core_trace_state = _as_dict(tension_state.get("core_trace_state"))
    core_interpretation_state = _as_dict(tension_state.get("core_interpretation_state"))
    focus = dict(world.get("focus", {}) or {})
    filtered_vision = dict(world.get("filtered_vision", {}) or {})
    visual_market_state = dict(world.get("visual_market_state", {}) or {})
    temporal_perception_state = dict(world.get("temporal_perception_state", {}) or {})
    core_visual_trace_state = _as_dict(visual_market_state.get("core_visual_trace_state"))
    core_visual_interpretation_state = _as_dict(visual_market_state.get("core_visual_interpretation_state"))
    trace_form_axes = _as_dict(core_visual_trace_state.get("form_axes"))
    structure_perception_state = dict(world.get("structure_perception_state", {}) or {})
    world_motion_afterimage_state = dict(world.get("world_motion_afterimage_state", {}) or {})

    focus_direction = float(focus.get("focus_direction", 0.0) or 0.0)
    focus_strength = float(focus.get("focus_strength", 0.0) or 0.0)
    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)
    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)
    filtered_target_map = float(filtered_vision.get("target_map", 0.0) or 0.0)
    filtered_threat_map = float(filtered_vision.get("threat_map", 0.0) or 0.0)
    filtered_optic_flow = float(filtered_vision.get("optic_flow", 0.0) or 0.0)
    spatial_bias = _float_from(core_visual_interpretation_state, visual_market_state, key="spatial_bias")
    directional_bias = _float_from(core_visual_interpretation_state, visual_market_state, key="directional_bias")
    range_position = _float_from(core_visual_trace_state, visual_market_state, key="range_position")
    short_impulse = _float_from(core_visual_interpretation_state, visual_market_state, key="short_impulse")
    mid_impulse = _float_from(core_visual_interpretation_state, visual_market_state, key="mid_impulse")
    market_balance = _float_from(core_visual_interpretation_state, visual_market_state, key="market_balance")
    breakout_tension = _float_from(core_visual_interpretation_state, visual_market_state, key="breakout_tension")
    visual_coherence = _float_from(core_visual_trace_state, visual_market_state, key="visual_coherence")
    visual_sight_state = dict(visual_market_state.get("visual_sight_state", {}) or {})
    if not visual_sight_state:
        for source in (core_visual_trace_state, core_visual_interpretation_state):
            candidate = source.get("visual_sight_state") if isinstance(source, dict) else None
            if isinstance(candidate, dict) and candidate:
                visual_sight_state = dict(candidate)
                break
    visual_cortex_state = dict(visual_market_state.get("visual_cortex_state", {}) or {})
    if not visual_cortex_state:
        for source in (core_visual_trace_state, core_visual_interpretation_state):
            candidate = source.get("visual_cortex_state") if isinstance(source, dict) else None
            if isinstance(candidate, dict) and candidate:
                visual_cortex_state = dict(candidate)
                break
    visual_cortex_state = build_visual_cortex_state(
        visual_sight_state,
        visual_market_state,
        dict(world.get("structure_perception_state", {}) or {}),
        temporal_perception_state,
    )
    visual_form_state = dict(visual_market_state.get("visual_form_state", {}) or {})
    visual_clarity = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_clarity")
    visual_object_stability = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_object_stability")
    visual_form_novelty = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_form_novelty")
    visual_blindness = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_blindness")
    visual_form_pressure = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_form_pressure")
    visual_shape_resonance = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_shape_resonance")
    visual_shape_fragility = _float_from(core_visual_interpretation_state, visual_market_state, key="visual_shape_fragility")
    sensory_state = _as_dict(core_visual_interpretation_state.get("sensory_reality"))
    sensory_reality_pressure = _float_from(sensory_state, core_visual_interpretation_state, visual_market_state, key="sensory_reality_pressure")
    sensory_load = _float_from(sensory_state, core_visual_interpretation_state, visual_market_state, key="sensory_load")
    sensory_redundancy = _float_from(sensory_state, visual_market_state, key="sensory_redundancy")
    sensory_habituation = _float_from(sensory_state, visual_market_state, key="sensory_habituation")
    sensory_gate = _float_from(sensory_state, core_visual_interpretation_state, visual_market_state, key="sensory_gate", default=1.0)
    sensory_active_axis_count = _int_from(sensory_state, visual_market_state, key="sensory_active_axis_count")
    sensory_primary_pressure = _float_from(sensory_state, visual_market_state, key="sensory_primary_pressure")
    sensory_reality_label = _str_from(sensory_state, core_visual_interpretation_state, visual_market_state, key="sensory_reality_label", default="quiet_outer_reality")
    visual_attention_state = dict(visual_market_state.get("visual_attention_state", {}) or {})
    if not visual_attention_state:
        visual_attention_state = build_visual_attention_state(
            {
                "visual_clarity": visual_clarity,
                "visual_object_stability": visual_object_stability,
                "visual_form_novelty": visual_form_novelty,
                "visual_blindness": visual_blindness,
                "visual_form_pressure": visual_form_pressure,
                "visual_shape_resonance": visual_shape_resonance,
                "visual_shape_fragility": visual_shape_fragility,
                "visual_coherence": visual_coherence,
                "market_balance": market_balance,
                "sensory_load": sensory_load,
                "sensory_habituation": sensory_habituation,
                "sensory_primary_pressure": sensory_primary_pressure,
            },
            {
                "focus_strength": focus_strength,
                "focus_confidence": focus_confidence,
                "target_lock": target_lock,
                "signal_relevance": signal_relevance,
            },
        )
    world_motion_afterimage_strength = _clip01(world_motion_afterimage_state.get("world_motion_afterimage_strength", 0.0))
    world_motion_afterimage_pressure = _clip01(world_motion_afterimage_state.get("world_motion_afterimage_pressure", 0.0))
    world_motion_afterimage_direction = max(-1.0, min(1.0, float(world_motion_afterimage_state.get("world_motion_afterimage_direction", 0.0) or 0.0)))
    world_motion_afterimage_volatility = _clip01(world_motion_afterimage_state.get("world_motion_afterimage_volatility", 0.0))
    world_motion_afterimage_acceleration = max(-1.0, min(1.0, float(world_motion_afterimage_state.get("world_motion_afterimage_acceleration", 0.0) or 0.0)))
    world_motion_afterimage_label = str(world_motion_afterimage_state.get("world_motion_afterimage_label", "motion_afterimage_clear") or "motion_afterimage_clear")
    motion_approach_pressure = _clip01(world_motion_afterimage_state.get("motion_approach_pressure", 0.0))
    motion_recession_pressure = _clip01(world_motion_afterimage_state.get("motion_recession_pressure", 0.0))
    contact_frequency_shift = _clip01(world_motion_afterimage_state.get("contact_frequency_shift", 0.0))
    afterimage_doppler_bias = max(-1.0, min(1.0, float(world_motion_afterimage_state.get("afterimage_doppler_bias", 0.0) or 0.0)))
    future_variant_pressure = _clip01(world_motion_afterimage_state.get("future_variant_pressure", 0.0))
    afterimage_action_maturity = _clip01(world_motion_afterimage_state.get("afterimage_action_maturity", 0.0))
    afterimage_doppler_label = str(world_motion_afterimage_state.get("afterimage_doppler_label", "doppler_clear") or "doppler_clear")

    coherence = _float_from(core_trace_state, tension_state, key="coherence")
    energy = _float_from(core_trace_state, tension_state, key="energy")
    energy_amplitude_stimulus = _float_from(
        core_trace_state,
        tension_state,
        key="energy_amplitude_stimulus",
        default=-1.0,
    )
    if energy_amplitude_stimulus < 0.0:
        energy_amplitude_stimulus = _float_from(
            core_trace_state,
            tension_state,
            key="energy_limited_amplitude",
            default=-1.0,
        )
    if energy_amplitude_stimulus < 0.0:
        energy_amplitude_stimulus = _float_from(
            core_trace_state,
            tension_state,
            key="energy_frequency_stimulus",
            default=abs(float(energy or 0.0)),
        )
    energy_raw_amplitude = _float_from(
        core_trace_state,
        tension_state,
        key="energy_raw_amplitude",
        default=abs(float(energy or 0.0)),
    )
    energy_limiter_gain = _float_from(
        core_trace_state,
        tension_state,
        key="energy_limiter_gain",
        default=1.0,
    )
    energy_overdrive = _float_from(
        core_trace_state,
        tension_state,
        key="energy_overdrive",
        default=0.0,
    )
    market_hearing_state = {}
    for source in (core_trace_state, tension_state, visual_market_state):
        candidate = (source or {}).get("market_hearing_state") if isinstance(source, dict) else None
        if isinstance(candidate, dict) and candidate:
            market_hearing_state = dict(candidate)
            break
    if not market_hearing_state:
        market_hearing_state = {
            "loudness": float(energy_amplitude_stimulus),
            "frequency_hz": _float_from(core_trace_state, tension_state, visual_market_state, key="market_frequency_hz", default=0.0),
            "compression": _float_from(core_trace_state, tension_state, visual_market_state, key="market_hearing_compression", default=0.0),
            "tone": _str_from(core_trace_state, tension_state, visual_market_state, key="market_tone", default="silent_tone"),
        }
    return_intensity = float((candle_state or {}).get("return_intensity", 0.0) or 0.0)
    close_position = float((candle_state or {}).get("close_position", 0.0) or 0.0)

    prev_signal_relevance = float(getattr(bot, "last_signal_relevance", 0.0) or 0.0) if bot is not None else 0.0
    prev_focus_confidence = float(getattr(bot, "focus_confidence", 0.0) or 0.0) if bot is not None else 0.0
    observation_mode = bool(getattr(bot, "observation_mode", False)) if bot is not None else False

    perception_settle = max(
        0.0,
        min(
            1.0,
            (prev_signal_relevance * 0.22)
            + (prev_focus_confidence * 0.20)
            + (focus_confidence * 0.14),
        ),
    )

    trace_mismatch = _clip01(max(0.0, abs(coherence - close_position)))
    trace_motion_change = _clip01(
        (abs(return_intensity) * 0.22)
        + (abs(filtered_optic_flow) * 0.18)
        + (energy_amplitude_stimulus * 0.10)
        + (abs(range_position) * 0.12)
        + (world_motion_afterimage_strength * 0.16)
        + (abs(world_motion_afterimage_acceleration) * 0.10)
        + (contact_frequency_shift * 0.10)
    )
    trace_support = _clip01(
        (signal_relevance * 0.22)
        + (focus_confidence * 0.18)
        + (target_lock * 0.12)
        + (focus_strength * 0.08)
        + (max(0.0, filtered_target_map) * 0.08)
        + (visual_coherence * 0.16)
        + (market_balance * 0.10)
        + (perception_settle * 0.14)
    )
    trace_strain = _clip01(
        (noise_damp * 0.18)
        + (filtered_threat_map * 0.14)
        + (max(0.0, abs(focus_direction) - focus_confidence) * 0.16)
        + (max(0.0, 1.0 - signal_relevance) * 0.14)
        + (trace_mismatch * 0.12)
        + (world_motion_afterimage_pressure * 0.10)
        + (world_motion_afterimage_volatility * 0.08)
        + (future_variant_pressure * 0.08)
        - (perception_settle * 0.14)
    )

    interpretation_uncertainty = _clip01(
        (breakout_tension * 0.08)
        + (sensory_load * 0.08)
        + (abs(spatial_bias - directional_bias) * 0.10)
        - (sensory_habituation * 0.08)
        - (market_balance * 0.10)
    )
    interpretation_novelty = _clip01(
        (abs(short_impulse - mid_impulse) * 0.13)
        + (sensory_reality_pressure * 0.06)
        - (sensory_habituation * 0.10)
    )
    interpretation_quality = _clip01(
        (market_balance * 0.10)
        + (afterimage_action_maturity * 0.05)
        + (max(0.0, 1.0 - breakout_tension) * 0.06)
    )

    uncertainty_score = _clip01((trace_strain * 0.74) + (interpretation_uncertainty * 0.26))
    novelty_score = _clip01((trace_motion_change * 0.78) + (interpretation_novelty * 0.22) - (perception_settle * 0.08))
    signal_quality = _clip01((trace_support * 0.82) + (interpretation_quality * 0.18) - (uncertainty_score * 0.12))
    observe_priority = _clip01(
        (trace_strain * 0.34)
        + (trace_motion_change * 0.18)
        + (max(0.0, 1.0 - trace_support) * 0.20)
        + (uncertainty_score * 0.16)
        + (0.10 if observation_mode else 0.0)
        - (perception_settle * 0.18)
    )

    perception_trace_metrics = {
        "trace_mismatch": float(trace_mismatch),
        "trace_motion_change": float(trace_motion_change),
        "energy_raw_amplitude": float(energy_raw_amplitude),
        "energy_limited_amplitude": float(energy_amplitude_stimulus),
        "energy_amplitude_stimulus": float(energy_amplitude_stimulus),
        "energy_limiter_gain": float(energy_limiter_gain),
        "energy_overdrive": float(energy_overdrive),
        "energy_frequency_stimulus": float(energy_amplitude_stimulus),
        "market_hearing_state": dict(market_hearing_state),
        "market_loudness": float(market_hearing_state.get("loudness", energy_amplitude_stimulus) or 0.0),
        "market_frequency_hz": float(market_hearing_state.get("frequency_hz", 0.0) or 0.0),
        "market_hearing_compression": float(market_hearing_state.get("compression", 0.0) or 0.0),
        "market_tone": str(market_hearing_state.get("tone", "silent_tone") or "silent_tone"),
        "trace_support": float(trace_support),
        "trace_strain": float(trace_strain),
    }
    perception_interpretation_metrics = {
        "interpretation_uncertainty": float(interpretation_uncertainty),
        "interpretation_novelty": float(interpretation_novelty),
        "interpretation_quality": float(interpretation_quality),
    }
    area_perception_profile = build_area_perception_profile(
        candle_state=candle_state,
        visual_cortex_state=visual_cortex_state,
        market_hearing_state=market_hearing_state,
        temporal_perception_state=temporal_perception_state,
        visual_attention_state=visual_attention_state,
        structure_perception_state=structure_perception_state,
    )

    return {
        "focus_direction": float(focus_direction),
        "focus_strength": float(focus_strength),
        "focus_confidence": float(focus_confidence),
        "target_lock": float(target_lock),
        "noise_damp": float(noise_damp),
        "signal_relevance": float(signal_relevance),
        "uncertainty_score": float(uncertainty_score),
        "novelty_score": float(novelty_score),
        "signal_quality": float(signal_quality),
        "observe_priority": float(observe_priority),
        "perception_trace_metrics": dict(perception_trace_metrics),
        "perception_interpretation_metrics": dict(perception_interpretation_metrics),
        "area_perception_profile": dict(area_perception_profile),
        "area_attention_need": float(area_perception_profile.get("area_attention_need", 0.0) or 0.0),
        "area_felt_depth": float(area_perception_profile.get("area_felt_depth", 0.0) or 0.0),
        "area_multisensory_coherence": float(area_perception_profile.get("area_multisensory_coherence", 0.0) or 0.0),
        "area_overcoupling_risk": float(area_perception_profile.get("area_overcoupling_risk", 0.0) or 0.0),
        "area_profile_state": str(area_perception_profile.get("area_profile_state", "background_area_perception") or "background_area_perception"),
        "sensory_sync_state": dict(area_perception_profile.get("sensory_sync_state", {}) or {}),
        "sensory_sync": float(area_perception_profile.get("sensory_sync", 0.0) or 0.0),
        "sensory_desync_pressure": float(area_perception_profile.get("sensory_desync_pressure", 0.0) or 0.0),
        "visual_hearing_fit": float(area_perception_profile.get("visual_hearing_fit", 0.0) or 0.0),
        "visual_felt_fit": float(area_perception_profile.get("visual_felt_fit", 0.0) or 0.0),
        "hearing_felt_fit": float(area_perception_profile.get("hearing_felt_fit", 0.0) or 0.0),
        "temporal_visual_fit": float(area_perception_profile.get("temporal_visual_fit", 0.0) or 0.0),
        "multisensory_binding_state": str(area_perception_profile.get("multisensory_binding_state", "loose_sensory_area") or "loose_sensory_area"),
        "spatial_bias": float(spatial_bias),
        "directional_bias": float(directional_bias),
        "range_position": float(range_position),
        "short_impulse": float(short_impulse),
        "mid_impulse": float(mid_impulse),
        "market_balance": float(market_balance),
        "breakout_tension": float(breakout_tension),
        "visual_coherence": float(visual_coherence),
        "visual_sight_state": dict(visual_sight_state),
        "visual_cortex_state": dict(visual_cortex_state),
        "visual_form_state": dict(visual_form_state or {}),
        "core_trace_state": dict(core_trace_state),
        "core_interpretation_state": dict(core_interpretation_state),
        "core_visual_trace_state": dict(core_visual_trace_state),
        "core_visual_interpretation_state": dict(core_visual_interpretation_state),
        "visual_trace_form_axes": dict(trace_form_axes),
        "visual_clarity": float(visual_clarity),
        "visual_object_stability": float(visual_object_stability),
        "visual_form_novelty": float(visual_form_novelty),
        "visual_blindness": float(visual_blindness),
        "visual_form_pressure": float(visual_form_pressure),
        "visual_shape_resonance": float(visual_shape_resonance),
        "visual_shape_fragility": float(visual_shape_fragility),
        "visual_attention_state": dict(visual_attention_state),
        "visual_attention_label": str(visual_attention_state.get("visual_attention_label", "background_form")),
        "visual_form_contact": float(visual_attention_state.get("visual_form_contact", 0.0) or 0.0),
        "visual_inspection_pull": float(visual_attention_state.get("visual_inspection_pull", 0.0) or 0.0),
        "visual_attention_depth": float(visual_attention_state.get("visual_attention_depth", 0.0) or 0.0),
        "visual_background_filter": float(visual_attention_state.get("visual_background_filter", 0.0) or 0.0),
        "visual_mcm_contact_weight": float(visual_attention_state.get("visual_mcm_contact_weight", 0.0) or 0.0),
        "sensory_reality_pressure": float(sensory_reality_pressure),
        "sensory_load": float(sensory_load),
        "sensory_redundancy": float(sensory_redundancy),
        "sensory_habituation": float(sensory_habituation),
        "sensory_gate": float(sensory_gate),
        "sensory_active_axis_count": int(sensory_active_axis_count),
        "sensory_primary_pressure": float(sensory_primary_pressure),
        "sensory_reality_label": str(sensory_reality_label),
        "world_motion_afterimage_state": dict(world_motion_afterimage_state or {}),
        "world_motion_afterimage_strength": float(world_motion_afterimage_strength),
        "world_motion_afterimage_pressure": float(world_motion_afterimage_pressure),
        "world_motion_afterimage_direction": float(world_motion_afterimage_direction),
        "world_motion_afterimage_volatility": float(world_motion_afterimage_volatility),
        "world_motion_afterimage_acceleration": float(world_motion_afterimage_acceleration),
        "world_motion_afterimage_label": str(world_motion_afterimage_label),
        "motion_approach_pressure": float(motion_approach_pressure),
        "motion_recession_pressure": float(motion_recession_pressure),
        "contact_frequency_shift": float(contact_frequency_shift),
        "afterimage_doppler_bias": float(afterimage_doppler_bias),
        "future_variant_pressure": float(future_variant_pressure),
        "afterimage_action_maturity": float(afterimage_action_maturity),
        "afterimage_doppler_label": str(afterimage_doppler_label),
        "structure_seen": float(structure_perception_state.get("structure_seen", 0.0) or 0.0),
        "structure_high": float(structure_perception_state.get("structure_high", 0.0) or 0.0),
        "structure_low": float(structure_perception_state.get("structure_low", 0.0) or 0.0),
        "structure_range": float(structure_perception_state.get("structure_range", 0.0) or 0.0),
        "swing_high_strength": float(structure_perception_state.get("swing_high_strength", 0.0) or 0.0),
        "swing_low_strength": float(structure_perception_state.get("swing_low_strength", 0.0) or 0.0),
        "zone_proximity": float(structure_perception_state.get("zone_proximity", 0.0) or 0.0),
        "structure_stability": float(structure_perception_state.get("structure_stability", 0.0) or 0.0),
        "structure_quality": float(structure_perception_state.get("structure_quality", 0.0) or 0.0),
        "stress_relief_potential": float(structure_perception_state.get("stress_relief_potential", 0.0) or 0.0),
        "context_confidence": float(structure_perception_state.get("context_confidence", 0.0) or 0.0),
    }


__all__ = [
    "build_world_state",
    "build_outer_visual_perception_state",
    "build_processing_state",
    "build_perception_state",
]

def build_conscious_perception_state(perception_state=None, processing_state=None, felt_state=None, thought_state=None, fused=None, neurochemical_state=None, meta_axes=None):
    perception = dict(perception_state or {})
    processing = dict(processing_state or {})
    felt = dict(felt_state or {})
    thought = dict(thought_state or {})
    fused_state = dict(fused or {})
    neuro = dict(neurochemical_state or {})
    axes = dict(meta_axes or {})

    def _v(source, key, default=0.0):
        try:
            return float(source.get(key, default) or default)
        except Exception:
            return float(default)

    sensory_load = _v(perception, "sensory_load", _v(processing, "sensory_load"))
    sensory_redundancy = _v(perception, "sensory_redundancy", _v(processing, "sensory_redundancy"))
    sensory_habituation = _v(perception, "sensory_habituation", _v(processing, "sensory_habituation"))
    sensory_gate = _v(perception, "sensory_gate", _v(processing, "sensory_gate", 1.0))
    sensory_pressure = _v(perception, "sensory_reality_pressure", _v(processing, "sensory_reality_pressure"))
    world_motion_afterimage_strength = _v(perception, "world_motion_afterimage_strength", _v(processing, "world_motion_afterimage_strength"))
    world_motion_afterimage_pressure = _v(perception, "world_motion_afterimage_pressure", _v(processing, "world_motion_afterimage_pressure"))
    world_motion_afterimage_volatility = _v(perception, "world_motion_afterimage_volatility", _v(processing, "world_motion_afterimage_volatility"))
    motion_approach_pressure = _v(perception, "motion_approach_pressure", _v(processing, "motion_approach_pressure"))
    motion_recession_pressure = _v(perception, "motion_recession_pressure", _v(processing, "motion_recession_pressure"))
    contact_frequency_shift = _v(perception, "contact_frequency_shift", _v(processing, "contact_frequency_shift"))
    future_variant_pressure = _v(perception, "future_variant_pressure", _v(processing, "future_variant_pressure"))
    afterimage_action_maturity = _v(perception, "afterimage_action_maturity", _v(processing, "afterimage_action_maturity"))
    visual_form_pressure = _v(axes, "visual_form_pressure", _v(processing, "visual_form_pressure", _v(perception, "visual_form_pressure")))
    visual_form_novelty = _v(axes, "visual_form_novelty", _v(processing, "visual_form_novelty", _v(perception, "visual_form_novelty")))
    visual_clarity = _v(axes, "visual_clarity", _v(processing, "visual_clarity", _v(perception, "visual_clarity")))
    visual_object_stability = _v(axes, "visual_object_stability", _v(processing, "visual_object_stability", _v(perception, "visual_object_stability")))
    visual_blindness = _v(axes, "visual_blindness", _v(processing, "visual_blindness", _v(perception, "visual_blindness")))
    visual_action_uncertainty = _v(axes, "visual_action_uncertainty")

    field_pressure = _v(axes, "field_perception_pressure", _v(felt, "field_perception_pressure", _v(processing, "field_perception_pressure")))
    field_support = _v(axes, "field_perception_support", _v(felt, "field_perception_support", _v(processing, "field_perception_support")))
    field_clarity = _v(axes, "field_perception_clarity", _v(felt, "field_perception_clarity", _v(processing, "field_perception_clarity")))
    field_focus = _v(axes, "field_perception_focus", _v(felt, "field_perception_focus", _v(processing, "field_perception_focus")))
    field_stability = _v(axes, "field_perception_stability", _v(felt, "field_perception_stability", _v(processing, "field_perception_stability")))
    field_fragmentation = _v(axes, "field_perception_fragmentation", _v(felt, "field_perception_fragmentation", _v(processing, "field_perception_fragmentation")))
    field_strain = _v(axes, "field_perception_strain", _v(felt, "field_perception_strain", _v(processing, "field_perception_strain")))
    field_observation_need = _v(axes, "field_observation_need")
    field_replan_pressure = _v(axes, "field_replan_pressure")
    field_bearing_support = _v(axes, "field_bearing_support", _v(axes, "field_action_support"))
    action_readiness_from_field = _v(axes, "action_readiness_from_field", _v(axes, "field_action_support", field_bearing_support))
    field_action_support = action_readiness_from_field

    felt_pressure = _v(axes, "felt_pressure", _v(felt, "felt_pressure"))
    felt_stability = _v(axes, "felt_stability", _v(felt, "felt_stability"))
    felt_alignment = _v(axes, "felt_alignment", _v(felt, "felt_alignment"))
    pressure_release = _v(axes, "pressure_release", _v(felt, "pressure_release"))
    experience_regulation = _v(axes, "experience_regulation", _v(felt, "experience_regulation"))
    load_bearing_capacity = _v(axes, "load_bearing_capacity", _v(felt, "load_bearing_capacity"))

    memory_orientation = _v(axes, "memory_orientation")
    memory_support = _v(axes, "memory_support")
    memory_compare_load = _v(axes, "memory_compare_load")
    cognitive_load = _v(axes, "cognitive_load")
    orientation_gap = _v(axes, "orientation_gap")
    blind_thinking_load = _v(axes, "blind_thinking_load")
    structure_action_uncertainty = _v(axes, "structure_action_uncertainty")
    semantic_shift_pressure = _v(axes, "semantic_shift_pressure")
    transfer_bearing = _v(axes, "transfer_bearing")
    interpretation_quality = _v(axes, "interpretation_quality")
    action_clearance = _v(axes, "action_clearance")
    action_inhibition = _v(axes, "action_inhibition")
    symbolic_regulation = _v(axes, "symbolic_regulation")
    symbolic_object_distance = _v(axes, "symbolic_object_distance")
    symbolic_containment = _v(axes, "symbolic_containment")
    symbolic_field_decoupling = _v(axes, "symbolic_field_decoupling")
    form_symbol_observation_binding = _v(axes, "form_symbol_observation_binding")
    form_symbol_reframe_binding = _v(axes, "form_symbol_reframe_binding")
    variant_learning_pressure = _v(axes, "variant_learning_pressure")
    uncertainty_familiarity = _v(axes, "uncertainty_familiarity")

    serotonin_carryover_risk = _v(neuro, "serotonin_carryover_risk")
    emotional_decoupling = _v(neuro, "emotional_decoupling")
    reactive_nervous_drive = _v(neuro, "reactive_nervous_drive")
    world_shift_evidence = _v(neuro, "world_shift_evidence")
    acetylcholine_focus = _v(neuro, "acetylcholine_focus")
    gaba_inhibition = _v(neuro, "gaba_inhibition")
    cortisol_load = _v(neuro, "cortisol_load")

    stimulus_field_effect = _clip01(
        (sensory_pressure * 0.18)
        + (sensory_load * 0.12)
        + (world_motion_afterimage_pressure * 0.10)
        + (future_variant_pressure * 0.06)
        + (visual_form_pressure * 0.16)
        + (visual_form_novelty * 0.08)
        + (field_pressure * 0.20)
        + (felt_pressure * 0.14)
        + (semantic_shift_pressure * 0.08)
        + (world_shift_evidence * 0.08)
        - (sensory_habituation * 0.06)
        - (field_support * 0.06)
    )
    perceived_field_change = _clip01(
        (world_shift_evidence * 0.22)
        + (world_motion_afterimage_strength * 0.10)
        + (world_motion_afterimage_volatility * 0.06)
        + (contact_frequency_shift * 0.06)
        + (future_variant_pressure * 0.05)
        + (semantic_shift_pressure * 0.18)
        + (visual_form_novelty * 0.14)
        + (structure_action_uncertainty * 0.12)
        + (field_fragmentation * 0.10)
        + (field_strain * 0.08)
        + (max(0.0, 1.0 - transfer_bearing) * 0.10)
        - (interpretation_quality * 0.08)
    )
    inner_impact_trace = _clip01(
        (stimulus_field_effect * 0.28)
        + (felt_pressure * 0.16)
        + (field_pressure * 0.14)
        + (world_motion_afterimage_pressure * 0.08)
        + (max(motion_approach_pressure, motion_recession_pressure) * 0.05)
        + (reactive_nervous_drive * 0.12)
        + (serotonin_carryover_risk * 0.10)
        + (cortisol_load * 0.08)
        + (orientation_gap * 0.08)
        + (blind_thinking_load * 0.06)
        - (emotional_decoupling * 0.10)
        - (pressure_release * 0.05)
    )
    felt_afterimage = _clip01(
        (serotonin_carryover_risk * 0.24)
        + (reactive_nervous_drive * 0.14)
        + (aftereffect_pressure := _v(axes, "aftereffect_pressure", _v(felt, "aftereffect_pressure"))) * 0.16
        + (inner_impact_trace * 0.16)
        + (memory_compare_load * 0.08)
        + (max(0.0, 1.0 - emotional_decoupling) * 0.08)
        - (pressure_release * 0.10)
        - (symbolic_containment * 0.06)
    )
    field_attachment = _clip01(
        (inner_impact_trace * 0.24)
        + (felt_afterimage * 0.18)
        + (field_pressure * 0.14)
        + (reactive_nervous_drive * 0.12)
        + (max(0.0, action_clearance - action_inhibition) * 0.10)
        + (visual_action_uncertainty * 0.08)
        - (symbolic_object_distance * 0.12)
        - (emotional_decoupling * 0.10)
        - (pressure_release * 0.06)
    )
    object_contact_depth = _clip01(
        (visual_object_stability * 0.20)
        + (visual_clarity * 0.16)
        + (field_focus * 0.14)
        + (acetylcholine_focus * 0.12)
        + (form_symbol_observation_binding * 0.10)
        + (uncertainty_familiarity * 0.06)
        + (perceived_field_change * 0.08)
        + (afterimage_action_maturity * 0.06)
        - (visual_blindness * 0.12)
        - (field_fragmentation * 0.08)
    )
    background_containment = _clip01(
        (sensory_habituation * 0.18)
        + (sensory_redundancy * 0.12)
        + (symbolic_containment * 0.18)
        + (symbolic_regulation * 0.14)
        + (field_stability * 0.12)
        + (field_support * 0.10)
        + (gaba_inhibition * 0.08)
        + (experience_regulation * 0.08)
        - (stimulus_field_effect * 0.08)
    )
    selective_attention = _clip01(
        (object_contact_depth * 0.22)
        + (acetylcholine_focus * 0.16)
        + (visual_clarity * 0.12)
        + (field_focus * 0.12)
        + (form_symbol_reframe_binding * 0.10)
        + (field_observation_need * 0.08)
        - (sensory_load * 0.06)
        - (field_fragmentation * 0.08)
    )
    reflective_distance = _clip01(
        (emotional_decoupling * 0.22)
        + (symbolic_field_decoupling * 0.18)
        + (symbolic_object_distance * 0.14)
        + (background_containment * 0.12)
        + (pressure_release * 0.10)
        + (experience_regulation * 0.08)
        + (field_replan_pressure * 0.06)
        + (form_symbol_reframe_binding * 0.06)
        - (field_attachment * 0.12)
        - (reactive_nervous_drive * 0.06)
    )
    release_capacity = _clip01(
        (pressure_release * 0.18)
        + (reflective_distance * 0.16)
        + (background_containment * 0.14)
        + (emotional_decoupling * 0.12)
        + (load_bearing_capacity * 0.10)
        + (field_stability * 0.08)
        + (symbolic_regulation * 0.08)
        + (memory_orientation * 0.06)
        - (felt_afterimage * 0.10)
        - (cognitive_load * 0.06)
    )
    perceptual_distance = _clip01(
        (reflective_distance * 0.24)
        + (object_contact_depth * 0.10)
        + (background_containment * 0.14)
        + (symbolic_object_distance * 0.16)
        + (release_capacity * 0.12)
        + (sensory_gate * 0.08)
        - (field_attachment * 0.12)
        - (inner_impact_trace * 0.06)
    )
    inner_outer_alignment = _clip01(
        (field_support * 0.16)
        + (field_clarity * 0.14)
        + (felt_alignment * 0.12)
        + (visual_clarity * 0.10)
        + (interpretation_quality * 0.12)
        + (transfer_bearing * 0.10)
        + (memory_support * 0.08)
        + (max(0.0, 1.0 - perceived_field_change) * 0.08)
        - (serotonin_carryover_risk * 0.10)
        - (orientation_gap * 0.06)
    )

    arousal_load = _clip01(
        (reactive_nervous_drive * 0.24)
        + (cortisol_load * 0.16)
        + (stimulus_field_effect * 0.16)
        + (inner_impact_trace * 0.14)
        + (sensory_load * 0.08)
        + (field_attachment * 0.10)
        - (background_containment * 0.08)
    )
    curiosity_tone = _clip01(
        (object_contact_depth * 0.24)
        + (selective_attention * 0.22)
        + (acetylcholine_focus * 0.14)
        + (perceived_field_change * 0.10)
        + (form_symbol_observation_binding * 0.08)
        - (felt_afterimage * 0.08)
    )
    fatigue_tone = _clip01(
        (orientation_gap * 0.18)
        + (blind_thinking_load * 0.16)
        + (cognitive_load * 0.14)
        + (memory_compare_load * 0.10)
        + (max(0.0, 0.22 - release_capacity) * 0.16)
        + (max(0.0, 0.18 - perceptual_distance) * 0.10)
        - (acetylcholine_focus * 0.08)
    )
    calm_tone = _clip01(
        (background_containment * 0.22)
        + (release_capacity * 0.18)
        + (reflective_distance * 0.16)
        + (field_stability * 0.12)
        + (emotional_decoupling * 0.12)
        + (gaba_inhibition * 0.08)
        - (arousal_load * 0.10)
    )

    conscious_perception_pressures = {
        "overcoupled_field": _clip01(
            (field_attachment * 0.30)
            + ((1.0 - reflective_distance) * 0.18)
            + (inner_impact_trace * 0.24)
            + (stimulus_field_effect * 0.10)
        ),
        "reflective_check": _clip01(
            (reflective_distance * 0.28)
            + ((1.0 - inner_outer_alignment) * 0.18)
            + (perceived_field_change * 0.22)
            + (emotional_decoupling * 0.08)
        ),
        "release_ready": _clip01(
            (release_capacity * 0.30)
            + ((1.0 - field_attachment) * 0.16)
            + ((1.0 - felt_afterimage) * 0.14)
            + (background_containment * 0.08)
        ),
        "object_contact": _clip01(
            (object_contact_depth * 0.30)
            + (selective_attention * 0.24)
            + (curiosity_tone * 0.10)
        ),
        "background_held": _clip01(
            (background_containment * 0.30)
            + ((1.0 - stimulus_field_effect) * 0.14)
            + (calm_tone * 0.10)
        ),
        "world_shift_contact": _clip01(
            (perceived_field_change * 0.24)
            + (variant_learning_pressure * 0.18)
            + (world_shift_evidence * 0.24)
            + (future_variant_pressure * 0.08)
        ),
        "open_perception": _clip01(
            ((1.0 - max(field_attachment, object_contact_depth, perceived_field_change)) * 0.22)
            + (background_containment * 0.08)
            + ((1.0 - felt_afterimage) * 0.08)
        ),
    }
    state_label = max(conscious_perception_pressures, key=conscious_perception_pressures.get)

    object_release_pressures = {
        "can_release": _clip01(
            (release_capacity * 0.34)
            + ((1.0 - felt_afterimage) * 0.18)
            + ((1.0 - field_attachment) * 0.16)
        ),
        "attached": _clip01(
            (field_attachment * 0.34)
            + ((1.0 - release_capacity) * 0.18)
            + (felt_afterimage * 0.10)
        ),
        "reflective_hold": _clip01(
            (reflective_distance * 0.28)
            + (release_capacity * 0.18)
            + (inner_outer_alignment * 0.08)
        ),
        "holding": _clip01(
            ((1.0 - release_capacity) * 0.18)
            + (field_attachment * 0.12)
            + (felt_afterimage * 0.10)
        ),
    }
    release_state = max(object_release_pressures, key=object_release_pressures.get)

    inner_posture_pressures = {
        "overstimulated": _clip01((arousal_load * 0.32) + (field_attachment * 0.18) + (reactive_nervous_drive * 0.08)),
        "tired": _clip01((fatigue_tone * 0.34) + ((1.0 - release_capacity) * 0.14) + (cognitive_load * 0.08)),
        "curious": _clip01((curiosity_tone * 0.32) + (object_contact_depth * 0.20) + (selective_attention * 0.10)),
        "excited": _clip01((arousal_load * 0.26) + (reactive_nervous_drive * 0.24) + (perceived_field_change * 0.08)),
        "calm": _clip01((calm_tone * 0.32) + (release_capacity * 0.16) + (background_containment * 0.10)),
        "reflective": _clip01((reflective_distance * 0.28) + ((1.0 - inner_outer_alignment) * 0.16) + (emotional_decoupling * 0.08)),
        "uncertain_open": _clip01(
            ((1.0 - max(calm_tone, curiosity_tone, arousal_load, fatigue_tone)) * 0.22)
            + ((1.0 - inner_outer_alignment) * 0.08)
        ),
    }
    inner_posture_state = max(inner_posture_pressures, key=inner_posture_pressures.get)

    return {
        "conscious_perception_state": str(state_label),
        "inner_posture_state": str(inner_posture_state),
        "conscious_perception_pressures": dict(conscious_perception_pressures),
        "object_release_pressures": dict(object_release_pressures),
        "inner_posture_pressures": dict(inner_posture_pressures),
        "arousal_load": float(arousal_load),
        "curiosity_tone": float(curiosity_tone),
        "fatigue_tone": float(fatigue_tone),
        "calm_tone": float(calm_tone),
        "stimulus_field_effect": float(stimulus_field_effect),
        "inner_impact_trace": float(inner_impact_trace),
        "perceived_field_change": float(perceived_field_change),
        "felt_afterimage": float(felt_afterimage),
        "object_release_state": str(release_state),
        "inner_outer_reflection": float(reflective_distance),
        "perceptual_distance": float(perceptual_distance),
        "object_contact_depth": float(object_contact_depth),
        "field_attachment": float(field_attachment),
        "release_capacity": float(release_capacity),
        "selective_attention": float(selective_attention),
        "background_containment": float(background_containment),
        "reflective_distance": float(reflective_distance),
        "inner_outer_alignment": float(inner_outer_alignment),
        "motion_approach_pressure": float(motion_approach_pressure),
        "motion_recession_pressure": float(motion_recession_pressure),
        "contact_frequency_shift": float(contact_frequency_shift),
        "future_variant_pressure": float(future_variant_pressure),
        "afterimage_action_maturity": float(afterimage_action_maturity),
    }
