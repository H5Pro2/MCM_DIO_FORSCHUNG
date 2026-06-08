"""Visual cortex object layer.

This layer turns raw sight into visual objects and relationships. It does not
decide entries and it does not write into the MCM field directly.
"""


def _clip01(value):
    try:
        value = float(value)
    except Exception:
        return 0.0
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)


def _clip_signed(value):
    try:
        value = float(value)
    except Exception:
        return 0.0
    if value < -1.0:
        return -1.0
    if value > 1.0:
        return 1.0
    return float(value)


def _v(source, key, default=0.0):
    try:
        return float((source or {}).get(key, default) or default)
    except Exception:
        return float(default)


def _s(source, key, default=""):
    return str((source or {}).get(key, default) or default)


def _object_label(strength, high, mid, low):
    strength = _clip01(strength)
    pressures = {
        high: _clip01(strength * 0.44),
        mid: _clip01(strength * 0.28 + (1.0 - abs(strength - 0.50)) * 0.12),
        low: _clip01((1.0 - strength) * 0.34),
    }
    return max(pressures, key=pressures.get)


def _side_label(range_position):
    pos = _clip_signed(range_position)
    pressures = {
        "upper_area": _clip01(max(0.0, pos) * 0.44),
        "lower_area": _clip01(max(0.0, -pos) * 0.44),
        "center_area": _clip01((1.0 - abs(pos)) * 0.34),
    }
    return max(pressures, key=pressures.get)


def _relation_label(contact_nearness, object_distance, edge_contact, swing_contact, object_presence):
    pressures = {
        "visual_background_relation": _clip01((1.0 - object_presence) * 0.38),
        "near_contact_object": _clip01((contact_nearness * 0.30) + (edge_contact * 0.24) + (object_presence * 0.08)),
        "swing_related_object": _clip01((swing_contact * 0.34) + (object_presence * 0.08)),
        "distant_visual_object": _clip01((object_distance * 0.34) + ((1.0 - contact_nearness) * 0.08)),
        "located_visual_object": _clip01((object_presence * 0.22) + ((1.0 - object_distance) * 0.10) + (contact_nearness * 0.08)),
    }
    return max(pressures, key=pressures.get)


def _lifecycle_label(emergence, stability, contact, rejection, dissolution):
    pressures = {
        "emerging_object": emergence,
        "stable_object": stability,
        "contacting_object": contact,
        "rejecting_object": rejection,
        "dissolving_object": dissolution,
        "background_lifecycle": _clip01((1.0 - max(emergence, stability, contact, rejection, dissolution)) * 0.30),
    }
    return max(pressures, key=pressures.get)


def build_visual_cortex_state(visual_sight_state=None, visual_market_state=None, structure_perception_state=None, temporal_perception_state=None):
    sight = dict(visual_sight_state or {})
    visual = dict(visual_market_state or {})
    structure = dict(structure_perception_state or {})
    temporal = dict(temporal_perception_state or {})
    form_state = dict(visual.get("visual_form_state", {}) or {})
    axes = dict(form_state.get("axes", {}) or visual.get("visual_trace_form_axes", {}) or {})

    clarity = _clip01(_v(sight, "clarity", visual.get("visual_clarity", 0.0)))
    object_stability = _clip01(_v(sight, "object_stability", visual.get("visual_object_stability", 0.0)))
    coherence = _clip01(_v(sight, "coherence", visual.get("visual_coherence", 0.0)))
    direction_bias = _clip_signed(_v(sight, "direction_bias", visual.get("directional_bias", 0.0)))
    range_position = _clip_signed(_v(sight, "range_position", visual.get("range_position", 0.0)))
    pressure = _clip01(_v(sight, "form_pressure", visual.get("visual_form_pressure", 0.0)))
    resonance = _clip01(_v(sight, "form_resonance", visual.get("visual_shape_resonance", 0.0)))
    fragility = _clip01(_v(sight, "form_fragility", visual.get("visual_shape_fragility", 0.0)))
    depth = _clip01(_v(sight, "depth", 0.0))
    contact_candidate = _clip01(_v(sight, "contact_candidate", 0.0))
    background_load = _clip01(_v(sight, "background_load", 0.0))

    flow = _clip01(_v(axes, "flow", 0.0))
    fracture = _clip01(_v(axes, "fracture", 0.0))
    density = _clip01(_v(axes, "density", 0.0))
    edge_strength = _clip01(_v(axes, "edge_strength", 0.0))
    void = _clip01(_v(axes, "void", 0.0))
    range_rhythm = _clip01(_v(axes, "range_rhythm", 0.0))
    direction_consistency = _clip01(_v(axes, "direction_consistency", 0.0))

    swing_high_strength = _clip01(_v(structure, "swing_high_strength", 0.0))
    swing_low_strength = _clip01(_v(structure, "swing_low_strength", 0.0))
    zone_proximity = _clip01(_v(structure, "zone_proximity", 0.0))
    structure_stability = _clip01(_v(structure, "structure_stability", 0.0))
    temporal_coherence = _clip01(_v(temporal, "temporal_coherence", 0.0))
    flow_stability = _clip01(_v(temporal, "flow_stability", 0.0))

    trend_object_strength = _clip01(
        (flow * 0.26)
        + (direction_consistency * 0.22)
        + (abs(direction_bias) * 0.18)
        + (object_stability * 0.16)
        + (flow_stability * 0.12)
        - (fracture * 0.14)
    )
    range_object_strength = _clip01(
        (range_rhythm * 0.24)
        + (void * 0.18)
        + (coherence * 0.18)
        + (object_stability * 0.16)
        + ((1.0 - abs(range_position)) * 0.14)
        - (pressure * 0.10)
    )
    contact_object_strength = _clip01(
        (contact_candidate * 0.26)
        + (zone_proximity * 0.22)
        + (edge_strength * 0.16)
        + (max(swing_high_strength, swing_low_strength) * 0.14)
        + (depth * 0.12)
        - (background_load * 0.10)
    )
    compression_object_strength = _clip01(
        (density * 0.24)
        + (void * 0.18)
        + (range_rhythm * 0.16)
        + (coherence * 0.16)
        + ((1.0 - fragility) * 0.12)
        - (fracture * 0.10)
    )
    break_object_strength = _clip01(
        (fracture * 0.30)
        + (pressure * 0.20)
        + (fragility * 0.18)
        + (edge_strength * 0.14)
        + (background_load * 0.08)
        - (object_stability * 0.10)
    )

    object_presence = _clip01(
        max(
            trend_object_strength,
            range_object_strength,
            contact_object_strength,
            compression_object_strength,
            break_object_strength,
        )
    )
    object_clarity = _clip01(
        (clarity * 0.30)
        + (object_stability * 0.22)
        + (resonance * 0.18)
        + (object_presence * 0.16)
        - (background_load * 0.14)
        - (fragility * 0.08)
    )
    relation_coherence = _clip01(
        (coherence * 0.24)
        + (temporal_coherence * 0.18)
        + (structure_stability * 0.18)
        + (range_rhythm * 0.14)
        + (direction_consistency * 0.14)
        - (break_object_strength * 0.10)
    )

    strengths = {
        "trend_object": trend_object_strength,
        "range_object": range_object_strength,
        "contact_object": contact_object_strength,
        "compression_object": compression_object_strength,
        "break_object": break_object_strength,
        "background": _clip01((1.0 - object_presence) * 0.30 + background_load * 0.12),
    }
    dominant_object = max(strengths, key=strengths.get)

    visual_readiness = _clip01(
        (object_clarity * 0.34)
        + (relation_coherence * 0.24)
        + (contact_object_strength * 0.16)
        + (depth * 0.12)
        - (background_load * 0.10)
        - (break_object_strength * 0.08)
    )

    cortex_label = _object_label(
        visual_readiness,
        "structured_visual_object",
        "forming_visual_object",
        "unformed_visual_background",
    )

    object_distance = _clip01(abs(range_position))
    contact_nearness = _clip01(max(contact_candidate, zone_proximity, contact_object_strength * 0.82))
    edge_contact = _clip01((edge_strength * 0.52) + (zone_proximity * 0.30) + (contact_candidate * 0.18))
    swing_contact = _clip01(max(swing_high_strength, swing_low_strength))
    object_side = _side_label(range_position)
    relation_label = _relation_label(
        contact_nearness,
        object_distance,
        edge_contact,
        swing_contact,
        object_presence,
    )

    emergence_strength = _clip01(
        (object_presence * 0.30)
        + (resonance * 0.20)
        + (density * 0.16)
        + (max(0.0, 1.0 - object_stability) * 0.14)
        - (background_load * 0.10)
    )
    stability_strength = _clip01(
        (object_stability * 0.30)
        + (relation_coherence * 0.22)
        + (structure_stability * 0.18)
        + (temporal_coherence * 0.14)
        - (fragility * 0.12)
    )
    contact_strength = _clip01(
        (contact_nearness * 0.34)
        + (edge_contact * 0.22)
        + (swing_contact * 0.18)
        + (depth * 0.12)
        - (background_load * 0.08)
    )
    rejection_strength = _clip01(
        (break_object_strength * 0.28)
        + (fracture * 0.22)
        + (pressure * 0.18)
        + (fragility * 0.16)
        - (object_stability * 0.12)
    )
    dissolution_strength = _clip01(
        (background_load * 0.24)
        + (void * 0.18)
        + ((1.0 - object_presence) * 0.18)
        + (fragility * 0.14)
        - (resonance * 0.10)
    )
    lifecycle_label = _lifecycle_label(
        emergence_strength,
        stability_strength,
        contact_strength,
        rejection_strength,
        dissolution_strength,
    )

    object_binding_quality = _clip01(
        (object_presence * 0.22)
        + (object_clarity * 0.24)
        + (relation_coherence * 0.20)
        + (stability_strength * 0.14)
        + (contact_nearness * 0.10)
        - (background_load * 0.08)
        - (dissolution_strength * 0.06)
    )

    visual_object_relation_state = {
        "relation_label": str(relation_label),
        "object_side": str(object_side),
        "object_distance": float(object_distance),
        "contact_nearness": float(contact_nearness),
        "edge_contact": float(edge_contact),
        "swing_contact": float(swing_contact),
    }
    visual_object_lifecycle_state = {
        "lifecycle_label": str(lifecycle_label),
        "emergence_strength": float(emergence_strength),
        "stability_strength": float(stability_strength),
        "contact_strength": float(contact_strength),
        "rejection_strength": float(rejection_strength),
        "dissolution_strength": float(dissolution_strength),
    }

    return {
        "visual_cortex_label": str(cortex_label),
        "dominant_visual_object": str(dominant_object),
        "object_presence": float(object_presence),
        "object_clarity": float(object_clarity),
        "relation_coherence": float(relation_coherence),
        "visual_readiness": float(visual_readiness),
        "trend_object_strength": float(trend_object_strength),
        "range_object_strength": float(range_object_strength),
        "contact_object_strength": float(contact_object_strength),
        "compression_object_strength": float(compression_object_strength),
        "break_object_strength": float(break_object_strength),
        "visual_object_relation_state": dict(visual_object_relation_state),
        "visual_object_lifecycle_state": dict(visual_object_lifecycle_state),
        "visual_relation_label": str(relation_label),
        "visual_lifecycle_label": str(lifecycle_label),
        "visual_object_side": str(object_side),
        "visual_object_distance": float(object_distance),
        "visual_contact_nearness": float(contact_nearness),
        "visual_edge_contact": float(edge_contact),
        "visual_swing_contact": float(swing_contact),
        "visual_lifecycle_emergence": float(emergence_strength),
        "visual_lifecycle_stability": float(stability_strength),
        "visual_lifecycle_contact": float(contact_strength),
        "visual_lifecycle_rejection": float(rejection_strength),
        "visual_lifecycle_dissolution": float(dissolution_strength),
        "visual_object_binding_quality": float(object_binding_quality),
        "form_id": _s(sight, "form_id", "-"),
        "form_family": _s(sight, "form_family", "mixed_form"),
        "sight_label": _s(sight, "sight_label", "background_sight"),
    }


__all__ = ["build_visual_cortex_state"]
