"""Visual attention layer.

This layer keeps seeing separate from immediate MCM feeling. Raw visual
perception can notice many forms, but only attended form contact should receive
stronger felt/MCM coupling.
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


def _v(source, key, default=0.0):
    try:
        return float((source or {}).get(key, default) or default)
    except Exception:
        return float(default)


def build_visual_attention_state(visual_state=None, focus_state=None):
    visual = dict(visual_state or {})
    focus = dict(focus_state or {})

    visual_clarity = _v(visual, "visual_clarity")
    visual_object_stability = _v(visual, "visual_object_stability")
    visual_form_pressure = _v(visual, "visual_form_pressure")
    visual_form_novelty = _v(visual, "visual_form_novelty")
    visual_blindness = _v(visual, "visual_blindness")
    visual_shape_resonance = _v(visual, "visual_shape_resonance")
    visual_shape_fragility = _v(visual, "visual_shape_fragility")
    visual_coherence = _v(visual, "visual_coherence")
    market_balance = _v(visual, "market_balance")
    visual_contrast = _v(visual, "visual_contrast")
    sensory_load = _v(visual, "sensory_load")
    sensory_habituation = _v(visual, "sensory_habituation")
    sensory_primary_pressure = _v(visual, "sensory_primary_pressure")

    focus_confidence = _v(focus, "focus_confidence")
    focus_strength = _v(focus, "focus_strength")
    target_lock = _v(focus, "target_lock")
    signal_relevance = _v(focus, "signal_relevance")

    form_contact = _clip01(
        (visual_shape_resonance * 0.24)
        + (visual_form_pressure * 0.18)
        + (visual_clarity * 0.16)
        + (visual_object_stability * 0.14)
        + (visual_coherence * 0.12)
        + (market_balance * 0.06)
        + (visual_contrast * 0.06)
        - (visual_blindness * 0.14)
        - (visual_shape_fragility * 0.06)
    )
    inspection_pull = _clip01(
        (form_contact * 0.26)
        + (visual_form_novelty * 0.16)
        + (sensory_primary_pressure * 0.12)
        + (visual_form_pressure * 0.12)
        + (visual_shape_resonance * 0.12)
        + (signal_relevance * 0.10)
        + (visual_contrast * 0.08)
        - (sensory_habituation * 0.08)
        - (sensory_load * 0.04)
    )
    attention_depth = _clip01(
        (form_contact * 0.42)
        + (inspection_pull * 0.28)
        + (focus_confidence * 0.10)
        + (focus_strength * 0.08)
        + (target_lock * 0.08)
        + (signal_relevance * 0.08)
        - (visual_blindness * 0.08)
        - (sensory_load * 0.04)
    )
    background_filter = _clip01(
        1.0
        - (form_contact * 0.46)
        - (attention_depth * 0.34)
        + (sensory_habituation * 0.12)
        + (max(0.0, 0.42 - visual_clarity) * 0.10)
    )
    mcm_contact_weight = _clip01(
        0.18
        + (attention_depth * 0.50)
        + (form_contact * 0.22)
        + (target_lock * 0.06)
        - (background_filter * 0.10)
    )

    visual_attention_pressures = {
        "focused_form_contact": _clip01((attention_depth * 0.34) + (form_contact * 0.28) + (target_lock * 0.08)),
        "form_contact": _clip01((form_contact * 0.28) + (inspection_pull * 0.24) + (visual_shape_resonance * 0.08)),
        "background_perception": _clip01((background_filter * 0.34) + (sensory_habituation * 0.08)),
        "background_form": _clip01(((1.0 - max(attention_depth, form_contact, inspection_pull)) * 0.24) + (visual_clarity * 0.04)),
    }
    attention_label = max(visual_attention_pressures, key=visual_attention_pressures.get)

    return {
        "visual_attention_label": str(attention_label),
        "visual_form_contact": float(form_contact),
        "visual_inspection_pull": float(inspection_pull),
        "visual_attention_depth": float(attention_depth),
        "visual_background_filter": float(background_filter),
        "visual_mcm_contact_weight": float(mcm_contact_weight),
        "visual_attention_pressures": dict(visual_attention_pressures),
    }
