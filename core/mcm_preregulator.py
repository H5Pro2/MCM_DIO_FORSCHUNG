"""Pre-regulation for inputs that may touch the MCM field.

The MCM field is treated as an organ-like felt space. Raw sensory values,
memory values, thought values and outcome values must not be written into the
field directly. This module converts those sources into normalized reflective
effects: bearing, pressure, coupling, displacement and tension.
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
    return value


def _clip11(value):
    try:
        value = float(value)
    except Exception:
        return 0.0
    if value < -1.0:
        return -1.0
    if value > 1.0:
        return 1.0
    return value


def _v(*sources, key, default=0.0):
    for source in sources:
        if not isinstance(source, dict):
            continue
        if key not in source:
            continue
        try:
            return float(source.get(key, default) or default)
        except Exception:
            return float(default or 0.0)
    return float(default or 0.0)


def _nested(source, key):
    if not isinstance(source, dict):
        return {}
    value = source.get(key, {})
    return dict(value or {}) if isinstance(value, dict) else {}


def _build_visual_channel(perception, processing):
    attention = _nested(processing, "visual_attention_state") or _nested(perception, "visual_attention_state")
    cortex = _nested(perception, "visual_cortex_state")
    coherence = _clip11(_v(perception, processing, key="visual_coherence"))
    clarity = _clip01(_v(processing, perception, key="visual_clarity"))
    stability = _clip01(_v(processing, perception, key="visual_object_stability"))
    contact = _clip01(_v(attention, processing, perception, key="visual_form_contact"))
    inspection = _clip01(_v(attention, processing, perception, key="visual_inspection_pull"))
    depth = _clip01(_v(attention, processing, perception, key="visual_attention_depth"))
    background_filter = _clip01(_v(attention, processing, perception, key="visual_background_filter"))
    relation = _clip01(_v(cortex, key="relation_coherence"))
    object_binding = _clip01(_v(cortex, key="visual_object_binding_quality"))
    raw_contact_weight = _clip01(_v(attention, processing, perception, key="visual_mcm_contact_weight", default=0.35))
    contact_weight = _clip01(
        (raw_contact_weight * 0.45)
        + (contact * 0.22)
        + (inspection * 0.12)
        + (depth * 0.10)
        + (clarity * 0.06)
        + (object_binding * 0.05)
        - (background_filter * 0.10)
    )
    coupling = _clip01(0.18 + (contact_weight * 0.62) + (relation * 0.10) + (stability * 0.10))
    bearing = _clip01((clarity * 0.22) + (stability * 0.20) + (relation * 0.16) + (object_binding * 0.14) + (contact_weight * 0.18) + (max(0.0, 1.0 - abs(coherence)) * 0.10))
    pressure = _clip01((_v(processing, perception, key="visual_form_pressure") * 0.22) + (_v(processing, perception, key="visual_shape_fragility") * 0.18) + (max(0.0, 1.0 - clarity) * 0.16) + (max(0.0, 1.0 - stability) * 0.12) + (contact_weight * max(0.0, 1.0 - relation) * 0.20) + (_v(processing, perception, key="visual_blindness") * 0.12))
    displacement = _clip11(coherence * coupling * max(0.15, contact_weight))
    tension = _clip01(max(abs(displacement), pressure * 0.72, contact_weight * 0.38))
    return {
        "bearing": float(bearing),
        "pressure": float(pressure),
        "coupling": float(coupling),
        "contact_weight": float(contact_weight),
        "displacement": float(displacement),
        "tension": float(tension),
        "reflective_coherence": float(_clip11(coherence * (0.45 + (coupling * 0.55)))),
        "form_pressure": float(_v(processing, perception, key="visual_form_pressure") * (0.20 + (coupling * 0.80))),
        "shape_resonance": float(_v(processing, perception, key="visual_shape_resonance") * (0.25 + (coupling * 0.75))),
    }


def _build_hearing_channel(perception, processing, stimulus):
    hearing = _nested(processing, "market_hearing_state") or _nested(perception, "market_hearing_state") or _nested(stimulus, "market_hearing_state")
    loudness = _clip01(_v(hearing, processing, perception, stimulus, key="loudness", default=_v(processing, perception, stimulus, key="market_loudness")))
    compression = _clip01(_v(hearing, processing, perception, stimulus, key="compression", default=_v(processing, perception, stimulus, key="market_hearing_compression")))
    overstimulation = _clip01(_v(hearing, processing, perception, key="overstimulation"))
    frequency_hz = max(0.0, _v(hearing, processing, perception, stimulus, key="frequency_hz", default=_v(processing, perception, stimulus, key="market_frequency_hz")))
    # Hearing is stimulus intensity, not directional truth.
    frequency_presence = _clip01(frequency_hz / 17000.0)
    coupling = _clip01(0.12 + (loudness * 0.34) + (compression * 0.18) + (frequency_presence * 0.10) - (overstimulation * 0.12))
    pressure = _clip01((loudness * 0.32) + (compression * 0.22) + (overstimulation * 0.24) + (frequency_presence * 0.08))
    bearing = _clip01((max(0.0, 1.0 - compression) * 0.20) + (max(0.0, 1.0 - overstimulation) * 0.22) + (loudness * 0.10))
    tension = _clip01((pressure * 0.72) + (coupling * 0.18))
    return {
        "bearing": float(bearing),
        "pressure": float(pressure),
        "coupling": float(coupling),
        "displacement": 0.0,
        "tension": float(tension),
        "loudness": float(loudness),
        "compression": float(compression),
        "frequency_presence": float(frequency_presence),
    }


def _build_memory_channel(memory, form):
    support = _clip01(_v(memory, form, key="memory_support", default=_v(form, key="form_symbol_learning_trust")))
    inhibition = _clip01(_v(memory, form, key="memory_inhibition", default=_v(form, key="form_symbol_caution_trust")))
    conflict = _clip01(_v(memory, form, key="memory_conflict"))
    orientation = _clip01(_v(memory, form, key="memory_orientation", default=_v(form, key="known_form_support")))
    compare_load = _clip01(_v(memory, key="memory_compare_load"))
    action_trust = _clip01(_v(form, key="form_symbol_action_trust"))
    maturity = _clip01(_v(form, key="form_symbol_contact_maturity", default=_v(form, key="form_mcm_family_maturity")))
    bearing = _clip01((support * 0.26) + (orientation * 0.18) + (action_trust * 0.18) + (maturity * 0.16) - (conflict * 0.12) - (compare_load * 0.08))
    pressure = _clip01((inhibition * 0.24) + (conflict * 0.24) + (compare_load * 0.20) + (max(0.0, 0.28 - orientation) * 0.16))
    coupling = _clip01(0.10 + (orientation * 0.26) + (maturity * 0.22) + (support * 0.14) + (max(0.0, 1.0 - conflict) * 0.08))
    displacement = _clip11((bearing - pressure) * coupling)
    tension = _clip01(max(abs(displacement), pressure * 0.76, bearing * 0.42))
    return {
        "bearing": float(bearing),
        "pressure": float(pressure),
        "coupling": float(coupling),
        "displacement": float(displacement),
        "tension": float(tension),
    }


def _build_thought_channel(thought):
    readiness = _clip01(_v(thought, key="decision_readiness"))
    alignment = _clip01(_v(thought, key="thought_alignment"))
    maturity = _clip01(_v(thought, key="state_maturity"))
    trust = _clip01(_v(thought, key="thought_trust_bearing", default=_v(thought, key="hypothesis_trust_score")))
    confirmation = _clip01(_v(thought, key="thought_confirmation_bearing", default=_v(thought, key="thought_confirmation_score")))
    rejection = _clip01(_v(thought, key="thought_rejection_pressure"))
    load = _clip01(_v(thought, key="thought_load_pressure", default=_v(thought, key="cognitive_load")))
    contradiction = _clip01(_v(thought, key="thought_contradiction_pressure"))
    bearing = _clip01((readiness * 0.18) + (alignment * 0.18) + (maturity * 0.16) + (trust * 0.18) + (confirmation * 0.16) - (rejection * 0.08) - (contradiction * 0.08))
    pressure = _clip01((rejection * 0.24) + (load * 0.22) + (contradiction * 0.22) + (max(0.0, 0.32 - maturity) * 0.14) + (max(0.0, 0.28 - alignment) * 0.10))
    coupling = _clip01(0.08 + (maturity * 0.22) + (alignment * 0.18) + (confirmation * 0.16) + (trust * 0.14))
    displacement = _clip11((bearing - pressure) * coupling)
    tension = _clip01(max(abs(displacement), pressure * 0.78, bearing * 0.38))
    return {
        "bearing": float(bearing),
        "pressure": float(pressure),
        "coupling": float(coupling),
        "displacement": float(displacement),
        "tension": float(tension),
    }


def _build_outcome_channel(outcome):
    process_reward = _clip01(_v(outcome, key="packet_process_reward"))
    bearing_quality = _clip01(_v(outcome, key="packet_bearing_quality"))
    constructive = _clip01(_v(outcome, key="constructive_stimulation", default=_v(outcome, key="position_constructive_bearing")))
    reorg = _clip01(_v(outcome, key="packet_reorganization_need"))
    burden = _clip01(_v(outcome, key="position_consequence_burden"))
    pain = _clip01(_v(outcome, key="contact_pain_sample"))
    utility = _clip01(_v(outcome, key="contact_utility_sample"))
    bearing = _clip01((process_reward * 0.24) + (bearing_quality * 0.20) + (constructive * 0.18) + (utility * 0.14) - (burden * 0.10) - (pain * 0.08))
    pressure = _clip01((reorg * 0.24) + (burden * 0.24) + (pain * 0.20) + (max(0.0, 0.24 - bearing_quality) * 0.12))
    coupling = _clip01(0.10 + (process_reward * 0.20) + (bearing_quality * 0.16) + (reorg * 0.12) + (burden * 0.10) + (utility * 0.10))
    displacement = _clip11((bearing - pressure) * coupling)
    tension = _clip01(max(abs(displacement), pressure * 0.80, bearing * 0.42))
    return {
        "bearing": float(bearing),
        "pressure": float(pressure),
        "coupling": float(coupling),
        "displacement": float(displacement),
        "tension": float(tension),
    }


def build_mcm_preregulator_state(
    *,
    perception_state=None,
    processing_state=None,
    stimulus=None,
    memory_state=None,
    form_symbol_state=None,
    thought_state=None,
    outcome_state=None,
):
    perception = dict(perception_state or {})
    processing = dict(processing_state or {})
    stimulus = dict(stimulus or {})
    memory = dict(memory_state or {})
    form = dict(form_symbol_state or {})
    thought = dict(thought_state or {})
    outcome = dict(outcome_state or {})

    visual = _build_visual_channel(perception, processing)
    hearing = _build_hearing_channel(perception, processing, stimulus)
    memory_channel = _build_memory_channel(memory, form)
    thought_channel = _build_thought_channel(thought)
    outcome_channel = _build_outcome_channel(outcome)

    channels = {
        "seeing": visual,
        "hearing": hearing,
        "memory": memory_channel,
        "thought": thought_channel,
        "outcome": outcome_channel,
    }
    displacement = _clip11(
        (visual["displacement"] * 0.30)
        + (memory_channel["displacement"] * 0.20)
        + (thought_channel["displacement"] * 0.18)
        + (outcome_channel["displacement"] * 0.18)
    )
    pressure = _clip01(
        (visual["pressure"] * 0.18)
        + (hearing["pressure"] * 0.14)
        + (memory_channel["pressure"] * 0.18)
        + (thought_channel["pressure"] * 0.22)
        + (outcome_channel["pressure"] * 0.16)
    )
    bearing = _clip01(
        (visual["bearing"] * 0.18)
        + (hearing["bearing"] * 0.08)
        + (memory_channel["bearing"] * 0.22)
        + (thought_channel["bearing"] * 0.20)
        + (outcome_channel["bearing"] * 0.18)
    )
    coupling_load = _clip01(
        (visual["coupling"] * 0.22)
        + (hearing["coupling"] * 0.14)
        + (memory_channel["coupling"] * 0.18)
        + (thought_channel["coupling"] * 0.20)
        + (outcome_channel["coupling"] * 0.14)
    )
    tension = _clip01(max(abs(displacement), pressure * 0.86, coupling_load * 0.42))
    field_position = _clip11(displacement) * 3.0
    if displacement >= 0.45:
        state = "++"
    elif displacement >= 0.18:
        state = "+"
    elif displacement <= -0.45:
        state = "--"
    elif displacement <= -0.18:
        state = "-"
    else:
        state = "0"

    return {
        "mcm_preregulator_channels": channels,
        "mcm_reflective_bearing": float(bearing),
        "mcm_reflective_pressure": float(pressure),
        "mcm_reflective_coupling_load": float(coupling_load),
        "mcm_reflective_displacement": float(displacement),
        "mcm_reflective_field_position": float(field_position),
        "mcm_reflective_tension": float(tension),
        "mcm_reflective_state": str(state),
        "visual_reflective_coherence": float(visual["reflective_coherence"]),
        "visual_mcm_contact_weight": float(visual["contact_weight"]),
        "visual_form_pressure": float(visual["form_pressure"]),
        "visual_shape_resonance": float(visual["shape_resonance"]),
        "hearing_reflective_pressure": float(hearing["pressure"]),
        "memory_reflective_bearing": float(memory_channel["bearing"]),
        "memory_reflective_pressure": float(memory_channel["pressure"]),
        "thought_reflective_bearing": float(thought_channel["bearing"]),
        "thought_reflective_pressure": float(thought_channel["pressure"]),
        "outcome_reflective_bearing": float(outcome_channel["bearing"]),
        "outcome_reflective_pressure": float(outcome_channel["pressure"]),
    }


__all__ = ["build_mcm_preregulator_state"]
