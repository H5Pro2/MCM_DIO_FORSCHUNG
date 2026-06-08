"""Neurochemical state construction for DIO.

This module translates perception, processing, felt state, thought state,
memory/form context and meta axes into neurochemical MCM pressure/support
values. It intentionally contains no trading side effects.
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


def build_neurochemical_state(perception_state=None, processing_state=None, felt_state=None, thought_state=None, fused=None, meta_axes=None):

    perception = dict(perception_state or {})
    processing = dict(processing_state or {})
    felt = dict(felt_state or {})
    thought = dict(thought_state or {})
    fused_state = dict(fused or {})
    axes = dict(meta_axes or {})
    memory_state = dict(fused_state.get("memory_complexity_state", {}) or {})
    form_state = dict(fused_state.get("form_symbol_state", {}) or {})

    def _v(source, key, default=0.0):
        try:
            return float(source.get(key, default) or default)
        except Exception:
            return float(default)

    signal_quality = _v(axes, "signal_quality", _v(perception, "signal_quality"))
    decision_strength = _v(axes, "decision_strength", max(_v(thought, "long_hypothesis"), _v(thought, "short_hypothesis")))
    decision_readiness = _v(axes, "decision_readiness", _v(thought, "decision_readiness"))
    state_maturity = _v(axes, "state_maturity", _v(thought, "state_maturity"))
    processing_load = _v(axes, "processing_load", _v(processing, "processing_load"))
    processing_tension = _v(axes, "processing_tension", _v(processing, "processing_tension"))
    processing_alignment = _v(axes, "processing_alignment", _v(processing, "processing_alignment"))
    field_pressure = _v(axes, "field_perception_pressure", _v(processing, "field_perception_pressure"))
    field_support = _v(axes, "field_perception_support", _v(processing, "field_perception_support"))
    field_clarity = _v(axes, "field_perception_clarity", _v(processing, "field_perception_clarity"))
    field_focus = _v(axes, "field_perception_focus", _v(processing, "field_perception_focus"))
    field_stability = _v(axes, "field_perception_stability", _v(processing, "field_perception_stability"))
    field_fragmentation = _v(axes, "field_perception_fragmentation", _v(processing, "field_perception_fragmentation"))
    field_strain = _v(axes, "field_perception_strain", _v(processing, "field_perception_strain"))
    activity_activation = _v(axes, "field_activity_island_activation_mean", _v(processing, "field_activity_island_activation_mean"))
    activity_pressure = _v(axes, "field_activity_island_pressure_mean", _v(processing, "field_activity_island_pressure_mean"))
    activity_context = _v(axes, "field_activity_island_context_reactivation_mean", _v(processing, "field_activity_island_context_reactivation_mean"))
    mcm_reflective_bearing = _v(axes, "mcm_reflective_bearing", _v(felt, "mcm_reflective_bearing"))
    mcm_reflective_pressure = _v(axes, "mcm_reflective_pressure", _v(felt, "mcm_reflective_pressure"))
    mcm_reflective_coupling_load = _v(axes, "mcm_reflective_coupling_load", _v(felt, "mcm_reflective_coupling_load"))
    mcm_reflective_tension = _v(axes, "mcm_reflective_tension", _v(felt, "mcm_reflective_tension"))

    visual_clarity = _v(axes, "visual_clarity", _v(processing, "visual_clarity", _v(perception, "visual_clarity")))
    visual_object_stability = _v(axes, "visual_object_stability", _v(processing, "visual_object_stability", _v(perception, "visual_object_stability")))
    visual_blindness = _v(axes, "visual_blindness", _v(processing, "visual_blindness", _v(perception, "visual_blindness")))
    visual_form_pressure = _v(axes, "visual_form_pressure", _v(processing, "visual_form_pressure", _v(perception, "visual_form_pressure")))
    visual_shape_resonance = _v(axes, "visual_shape_resonance", _v(processing, "visual_shape_resonance", _v(perception, "visual_shape_resonance")))
    visual_shape_fragility = _v(axes, "visual_shape_fragility", _v(processing, "visual_shape_fragility", _v(perception, "visual_shape_fragility")))
    visual_mcm_contact_weight = _clip01(_v(axes, "visual_mcm_contact_weight", _v(processing, "visual_mcm_contact_weight", _v(perception, "visual_mcm_contact_weight", 0.35))))
    felt_visual_form_pressure = visual_form_pressure * _clip01(0.25 + (visual_mcm_contact_weight * 0.75))
    felt_visual_shape_resonance = visual_shape_resonance * _clip01(0.35 + (visual_mcm_contact_weight * 0.65))
    visual_action_uncertainty = _v(axes, "visual_action_uncertainty")
    visual_blind_action_load = _v(axes, "visual_blind_action_load")

    felt_pressure = _v(axes, "felt_pressure", _v(felt, "felt_pressure"))
    felt_stability = _v(axes, "felt_stability", _v(felt, "felt_stability"))
    felt_alignment = _v(axes, "felt_alignment", _v(felt, "felt_alignment"))
    pressure_release = _v(axes, "pressure_release", _v(felt, "pressure_release"))
    experience_regulation = _v(axes, "experience_regulation", _v(felt, "experience_regulation"))
    load_bearing_capacity = _v(axes, "load_bearing_capacity", _v(felt, "load_bearing_capacity"))
    stress_relief_potential = _v(axes, "stress_relief_potential", _v(felt, "stress_relief_potential"))
    protective_courage = _v(axes, "protective_courage", _v(felt, "protective_courage"))

    memory_support = _v(axes, "memory_support", _v(memory_state, "memory_support"))
    memory_inhibition = _v(axes, "memory_inhibition", _v(memory_state, "memory_inhibition"))
    memory_compare_load = _v(axes, "memory_compare_load", _v(memory_state, "memory_compare_load"))
    memory_conflict = _v(axes, "memory_conflict", _v(memory_state, "memory_conflict"))
    cognitive_load = _v(axes, "cognitive_load", _v(memory_state, "cognitive_load"))
    decision_energy_cost = _v(axes, "decision_energy_cost", _v(memory_state, "decision_energy_cost"))
    thinking_complexity = _v(axes, "thinking_complexity", _v(memory_state, "thinking_complexity"))
    memory_orientation = _v(axes, "memory_orientation")
    orientation_gap = _v(axes, "orientation_gap")
    blind_thinking_load = _v(axes, "blind_thinking_load")

    action_inhibition = _v(axes, "action_inhibition")
    action_clearance = _v(axes, "action_clearance")
    regulated_courage = _v(axes, "regulated_courage")
    plan_pressure = _v(axes, "plan_pressure")
    act_watch_readiness = _v(axes, "act_watch_readiness")
    structure_action_uncertainty = _v(axes, "structure_action_uncertainty")
    structure_carrying_need = _v(axes, "structure_carrying_need")
    field_observation_need = _v(axes, "field_observation_need")
    field_replan_pressure = _v(axes, "field_replan_pressure")
    field_bearing_support = _v(axes, "field_bearing_support", _v(axes, "field_action_support"))
    semantic_shift_pressure = _v(axes, "semantic_shift_pressure")
    transfer_bearing = _v(axes, "transfer_bearing")
    trust_transfer_support = _v(axes, "trust_transfer_support")
    transfer_maturity_gap = _v(axes, "transfer_maturity_gap")
    transfer_break_fatigue = _v(axes, "transfer_break_fatigue")
    interpretation_quality = _v(axes, "interpretation_quality")
    route_familiarity = _v(axes, "route_familiarity")
    learned_development_uncertainty = _v(axes, "learned_development_uncertainty")
    variant_learning_pressure = _v(axes, "variant_learning_pressure", _v(form_state, "variant_learning_pressure"))
    variant_bearing_memory = _v(axes, "variant_bearing_memory", _v(form_state, "variant_bearing_memory"))
    uncertainty_familiarity = _v(axes, "uncertainty_familiarity", _v(form_state, "uncertainty_familiarity"))
    form_symbol_development_quality = _v(axes, "form_symbol_development_quality", _v(form_state, "form_symbol_development_quality"))
    form_symbol_learning_trust = _v(axes, "form_symbol_learning_trust", _v(form_state, "form_symbol_learning_trust"))
    form_symbol_action_trust = _v(axes, "form_symbol_action_trust", _v(form_state, "form_symbol_action_trust"))
    form_symbol_caution_trust = _v(axes, "form_symbol_caution_trust", _v(form_state, "form_symbol_caution_trust"))

    dopamine_tone = _clip01(
        (max(0.0, form_symbol_development_quality) * 0.18)
        + (form_symbol_learning_trust * 0.14)
        + (form_symbol_action_trust * 0.10)
        + (trust_transfer_support * 0.12)
        + (memory_support * 0.12)
        + (plan_pressure * 0.10)
        + (action_clearance * 0.08)
        + (variant_bearing_memory * 0.08)
        + (signal_quality * 0.08)
        - (learned_development_uncertainty * 0.08)
        - (transfer_maturity_gap * 0.05)
    )
    gaba_inhibition = _clip01(
        (action_inhibition * 0.34)
        + (field_observation_need * 0.12)
        + (act_watch_readiness * 0.12)
        + (structure_action_uncertainty * 0.10)
        + (learned_development_uncertainty * 0.10)
        + (transfer_maturity_gap * 0.08)
        + (visual_action_uncertainty * 0.07)
        + (memory_inhibition * 0.07)
        - (action_clearance * 0.08)
    )
    noradrenaline_arousal = _clip01(
        (felt_pressure * 0.18)
        + (field_pressure * 0.16)
        + (mcm_reflective_pressure * 0.10)
        + (processing_tension * 0.12)
        + (felt_visual_form_pressure * 0.10)
        + (activity_pressure * 0.10)
        + (semantic_shift_pressure * 0.08)
        + (decision_strength * 0.08)
        + (plan_pressure * 0.08)
        + (visual_shape_fragility * 0.06)
        + (field_strain * 0.04)
    )
    acetylcholine_focus = _clip01(
        (visual_clarity * 0.22)
        + (visual_object_stability * 0.16)
        + (field_focus * 0.14)
        + (field_clarity * 0.14)
        + (mcm_reflective_bearing * 0.08)
        + (felt_visual_shape_resonance * 0.10)
        + (signal_quality * 0.08)
        + (processing_alignment * 0.08)
        + (max(0.0, 1.0 - visual_blindness) * 0.08)
    )
    serotonin_stability = _clip01(
        (felt_stability * 0.18)
        + (field_stability * 0.14)
        + (state_maturity * 0.12)
        + (load_bearing_capacity * 0.12)
        + (experience_regulation * 0.10)
        + (regulated_courage * 0.10)
        + (route_familiarity * 0.08)
        + (memory_orientation * 0.08)
        + (mcm_reflective_bearing * 0.08)
        + (max(0.0, 1.0 - transfer_break_fatigue) * 0.08)
    )
    cortisol_load = _clip01(
        (processing_load * 0.14)
        + (cognitive_load * 0.12)
        + (memory_compare_load * 0.10)
        + (blind_thinking_load * 0.12)
        + (orientation_gap * 0.10)
        + (decision_energy_cost * 0.08)
        + (field_strain * 0.08)
        + (mcm_reflective_pressure * 0.08)
        + (mcm_reflective_coupling_load * max(0.0, 0.30 - mcm_reflective_bearing) * 0.08)
        + (field_fragmentation * 0.07)
        + (transfer_break_fatigue * 0.07)
        + (visual_blind_action_load * 0.06)
        + (action_inhibition * 0.06)
    )
    endorphin_relief = _clip01(
        (pressure_release * 0.22)
        + (stress_relief_potential * 0.16)
        + (field_support * 0.12)
        + (mcm_reflective_bearing * 0.10)
        + (load_bearing_capacity * 0.12)
        + (experience_regulation * 0.10)
        + (action_clearance * 0.08)
        + (interpretation_quality * 0.08)
        + (trust_transfer_support * 0.06)
        + (max(0.0, 1.0 - cortisol_load) * 0.06)
    )
    glutamate_activation = _clip01(
        (activity_activation * 0.20)
        + (decision_strength * 0.16)
        + (processing_load * 0.12)
        + (field_pressure * 0.10)
        + (mcm_reflective_tension * 0.08)
        + (thinking_complexity * 0.10)
        + (decision_energy_cost * 0.08)
        + (activity_context * 0.08)
        + (plan_pressure * 0.08)
        + (felt_visual_form_pressure * 0.04)
        + (field_bearing_support * 0.04)
    )

    positive_expansion_pressure = _clip01(
        (dopamine_tone * 0.24)
        + (reward_stability_echo * 0.18 if "reward_stability_echo" in locals() else 0.0)
        + (glutamate_activation * 0.16)
        + (max(0.0, action_clearance - action_inhibition) * 0.12)
        + (plan_pressure * 0.10)
        + (form_symbol_action_trust * 0.08)
        + (trust_transfer_support * 0.06)
        + (mcm_reflective_bearing * 0.08)
        + (previous_constructive_stimulation * 0.06 if "previous_constructive_stimulation" in locals() else 0.0)
    )
    negative_contraction_pressure = _clip01(
        (cortisol_load * 0.26)
        + (noradrenaline_arousal * 0.22)
        + (gaba_inhibition * 0.16)
        + (field_strain * 0.12)
        + (mcm_reflective_pressure * 0.12)
        + (field_fragmentation * 0.10)
        + (orientation_gap * 0.08)
        + (visual_blind_action_load * 0.06)
    )
    positive_overextension = _clip01(
        positive_expansion_pressure
        * (
            0.24
            + (max(0.0, 0.48 - field_bearing_support) * 0.22)
            + (max(0.0, 0.34 - mcm_reflective_bearing) * 0.12)
            + (max(0.0, 0.46 - field_clarity) * 0.16)
            + (max(0.0, 0.44 - interpretation_quality) * 0.16)
            + (serotonin_carryover_risk * 0.14 if "serotonin_carryover_risk" in locals() else 0.0)
            + (max(0.0, action_clearance - action_inhibition) * 0.10)
        )
    )
    positive_return_pressure = _clip01(
        (positive_overextension * 0.44)
        + (positive_expansion_pressure * max(0.0, 0.42 - field_bearing_support) * 0.18)
        + (positive_expansion_pressure * max(0.0, 0.32 - mcm_reflective_bearing) * 0.10)
        + (positive_expansion_pressure * max(0.0, 0.38 - emotional_decoupling) * 0.12 if "emotional_decoupling" in locals() else 0.0)
        + (positive_expansion_pressure * max(0.0, 0.40 - interpretation_quality) * 0.12)
        + (serotonin_carryover_risk * 0.12 if "serotonin_carryover_risk" in locals() else 0.0)
    )
    mcm_axis_displacement = max(-1.0, min(1.0, positive_expansion_pressure - negative_contraction_pressure))
    mcm_axis_field_position = max(-3.0, min(3.0, mcm_axis_displacement * 3.0))
    mcm_axis_tension = _clip01(max(positive_expansion_pressure, negative_contraction_pressure))
    mcm_axis_state_pressures = {
        "++": _clip01(positive_expansion_pressure * 0.44 + max(0.0, mcm_axis_displacement) * 0.34),
        "+": _clip01(positive_expansion_pressure * 0.28 + max(0.0, mcm_axis_displacement) * 0.18 + (1.0 - mcm_axis_tension) * 0.08),
        "0": _clip01((1.0 - abs(mcm_axis_displacement)) * 0.34 + (1.0 - mcm_axis_tension) * 0.16),
        "-": _clip01(negative_contraction_pressure * 0.28 + max(0.0, -mcm_axis_displacement) * 0.18 + (1.0 - mcm_axis_tension) * 0.08),
        "--": _clip01(negative_contraction_pressure * 0.44 + max(0.0, -mcm_axis_displacement) * 0.34),
    }
    mcm_axis_state = max(mcm_axis_state_pressures, key=mcm_axis_state_pressures.get)

    neurochemical_load = _clip01((cortisol_load * 0.42) + (gaba_inhibition * 0.24) + (noradrenaline_arousal * 0.18) + (glutamate_activation * 0.16))
    neurochemical_load = _clip01(neurochemical_load + (positive_return_pressure * 0.10))
    neurochemical_support = _clip01((serotonin_stability * 0.30) + (endorphin_relief * 0.24) + (acetylcholine_focus * 0.18) + (dopamine_tone * 0.16) + (gaba_inhibition * 0.06) + (memory_orientation * 0.06) - (positive_overextension * 0.10))
    neurochemical_balance = max(-1.0, min(1.0, neurochemical_support - neurochemical_load))
    reward_stability_echo = _clip01(
        (serotonin_stability * 0.34)
        + (dopamine_tone * 0.22)
        + (endorphin_relief * 0.12)
        + (route_familiarity * 0.10)
        + (action_clearance * 0.10)
        + (max(0.0, 1.0 - transfer_break_fatigue) * 0.07)
        - (gaba_inhibition * 0.10)
        - (positive_overextension * 0.12)
    )
    world_shift_evidence = _clip01(
        (semantic_shift_pressure * 0.22)
        + (max(0.0, 1.0 - transfer_bearing) * 0.20)
        + (max(0.0, 1.0 - interpretation_quality) * 0.18)
        + (max(0.0, 1.0 - field_clarity) * 0.12)
        + (max(0.0, 1.0 - memory_support) * 0.10)
        + (visual_shape_fragility * 0.10)
        + (visual_action_uncertainty * 0.08)
    )
    serotonin_carryover_risk = _clip01(
        (reward_stability_echo * world_shift_evidence * 0.72)
        + (max(0.0, serotonin_stability - ((transfer_bearing + interpretation_quality) * 0.5)) * 0.28)
        + (max(0.0, action_clearance - action_inhibition) * max(0.0, 1.0 - interpretation_quality) * 0.14)
    )
    emotional_decoupling = _clip01(
        (gaba_inhibition * 0.20)
        + (acetylcholine_focus * 0.16)
        + (field_clarity * 0.14)
        + (interpretation_quality * 0.16)
        + (transfer_bearing * 0.14)
        + (memory_support * 0.10)
        + (form_symbol_caution_trust * 0.10)
        - (serotonin_carryover_risk * 0.24)
    )
    reactive_nervous_drive = _clip01(
        (dopamine_tone * 0.18)
        + (glutamate_activation * 0.20)
        + (noradrenaline_arousal * 0.16)
        + (action_clearance * 0.16)
        + (plan_pressure * 0.12)
        + (serotonin_carryover_risk * 0.14)
        + (positive_overextension * 0.14)
        - (emotional_decoupling * 0.16)
    )
    nervous_system_overload = _clip01(
        (cortisol_load * 0.24)
        + (noradrenaline_arousal * 0.20)
        + (glutamate_activation * 0.16)
        + (serotonin_carryover_risk * 0.16)
        + (reactive_nervous_drive * 0.14)
        + (positive_return_pressure * 0.10)
        + (max(0.0, -neurochemical_balance) * 0.14)
        - (emotional_decoupling * 0.18)
        - (gaba_inhibition * 0.05)
    )
    escape_action_drive = _clip01(
        (nervous_system_overload * 0.34)
        + (reactive_nervous_drive * 0.24)
        + (action_clearance * 0.14)
        + (plan_pressure * 0.12)
        + (world_shift_evidence * 0.10)
        - (emotional_decoupling * 0.22)
        - (acetylcholine_focus * 0.08)
    )
    shock_response_risk = _clip01(
        (nervous_system_overload * 0.36)
        + (escape_action_drive * 0.26)
        + (world_shift_evidence * 0.14)
        + (max(0.0, 0.34 - emotional_decoupling) * 0.18)
        + (serotonin_carryover_risk * 0.12)
        - (acetylcholine_focus * 0.06)
    )

    tone_map = {
        "cortisol_load": cortisol_load,
        "gaba_inhibition": gaba_inhibition,
        "noradrenaline_arousal": noradrenaline_arousal,
        "glutamate_activation": glutamate_activation,
        "serotonin_stability": serotonin_stability,
        "acetylcholine_focus": acetylcholine_focus,
        "endorphin_relief": endorphin_relief,
        "dopamine_tone": dopamine_tone,
    }
    dominant_tone = max(tone_map, key=tone_map.get)
    neurochemical_state_pressures = {
        "overloaded_neurochemistry": _clip01((shock_response_risk * 0.34) + (nervous_system_overload * 0.30) + (cortisol_load * 0.12)),
        "positive_overextension_neurochemistry": _clip01((positive_overextension * 0.36) + (positive_return_pressure * 0.28) + (serotonin_carryover_risk * 0.10)),
        "strained_neurochemistry": _clip01((max(0.0, -neurochemical_balance) * 0.32) + (cortisol_load * 0.26) + (neurochemical_load * 0.14)),
        "inhibited_neurochemistry": _clip01((gaba_inhibition * 0.34) + ((1.0 - action_clearance) * 0.18)),
        "focused_neurochemistry": _clip01((acetylcholine_focus * 0.36) + (field_clarity * 0.12) + ((1.0 - cortisol_load) * 0.10)),
        "carryover_neurochemistry": _clip01((serotonin_carryover_risk * 0.34) + (serotonin_stability * 0.18) + ((1.0 - transfer_bearing) * 0.12)),
        "stable_neurochemistry": _clip01((serotonin_stability * 0.32) + (neurochemical_support * 0.18) + ((1.0 - max(0.0, -neurochemical_balance)) * 0.10)),
        "activated_neurochemistry": _clip01((glutamate_activation * 0.32) + (noradrenaline_arousal * 0.24)),
        "relieved_neurochemistry": _clip01((endorphin_relief * 0.34) + ((1.0 - cortisol_load) * 0.12)),
        "mixed_neurochemistry": _clip01((1.0 - abs(neurochemical_balance)) * 0.16 + (1.0 - max(tone_map.values())) * 0.12),
    }
    state_label = max(neurochemical_state_pressures, key=neurochemical_state_pressures.get)

    return {
        "neurochemical_state_label": str(state_label),
        "neurochemical_dominant_tone": str(dominant_tone),
        "dopamine_tone": float(dopamine_tone),
        "gaba_inhibition": float(gaba_inhibition),
        "noradrenaline_arousal": float(noradrenaline_arousal),
        "acetylcholine_focus": float(acetylcholine_focus),
        "serotonin_stability": float(serotonin_stability),
        "cortisol_load": float(cortisol_load),
        "endorphin_relief": float(endorphin_relief),
        "glutamate_activation": float(glutamate_activation),
        "neurochemical_load": float(neurochemical_load),
        "neurochemical_support": float(neurochemical_support),
        "neurochemical_balance": float(neurochemical_balance),
        "reward_stability_echo": float(reward_stability_echo),
        "positive_expansion_pressure": float(positive_expansion_pressure),
        "negative_contraction_pressure": float(negative_contraction_pressure),
        "positive_overextension": float(positive_overextension),
        "positive_return_pressure": float(positive_return_pressure),
        "mcm_axis_displacement": float(mcm_axis_displacement),
        "mcm_axis_field_position": float(mcm_axis_field_position),
        "mcm_axis_tension": float(mcm_axis_tension),
        "mcm_axis_state": str(mcm_axis_state),
        "mcm_axis_state_pressures": dict(mcm_axis_state_pressures),
        "neurochemical_state_pressures": dict(neurochemical_state_pressures),
        "mcm_reflective_bearing": float(mcm_reflective_bearing),
        "mcm_reflective_pressure": float(mcm_reflective_pressure),
        "mcm_reflective_coupling_load": float(mcm_reflective_coupling_load),
        "mcm_reflective_tension": float(mcm_reflective_tension),
        "world_shift_evidence": float(world_shift_evidence),
        "serotonin_carryover_risk": float(serotonin_carryover_risk),
        "emotional_decoupling": float(emotional_decoupling),
        "reactive_nervous_drive": float(reactive_nervous_drive),
        "nervous_system_overload": float(nervous_system_overload),
        "escape_action_drive": float(escape_action_drive),
        "shock_response_risk": float(shock_response_risk),
    }


__all__ = ["build_neurochemical_state"]
