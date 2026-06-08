"""Decision and meta-regulation construction for DIO.

This module owns the meta-regulatory bridge between perception, felt state,
thought state, memory/form context, neurochemistry and pre-action phases.
It computes regulation state only; it does not place orders.
"""

from config import Config
from core.mcm_field import _normalize_active_context_trace
from core.neurochemistry import build_neurochemical_state
from core.perception import build_conscious_perception_state


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


def _build_field_regulation_state(context=None):

    ctx = dict(context or {})

    def _value(name, default=0.0):
        try:
            value = float(ctx.get(name, default) or default)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return value

    field_perception_label = str(ctx.get("field_perception_label", "quiet_field") or "quiet_field").strip().lower()
    field_activity_island_count = int(ctx.get("field_activity_island_count", 0) or 0)
    field_perception_pressure = _value("field_perception_pressure")
    field_perception_strain = _value("field_perception_strain")
    field_perception_fragmentation = _value("field_perception_fragmentation")
    field_activity_island_pressure_mean = _value("field_activity_island_pressure_mean")
    field_perception_clarity = _value("field_perception_clarity")
    field_perception_support = _value("field_perception_support")
    field_perception_stability = _value("field_perception_stability")
    field_activity_island_context_reactivation_mean = _value("field_activity_island_context_reactivation_mean")
    field_perception_focus = _value("field_perception_focus")
    field_activity_island_coherence_mean = _value("field_activity_island_coherence_mean")
    symbolic_regulation = _clip01(ctx.get("symbolic_regulation", 0.0))
    symbolic_action_regulation = _clip01(ctx.get("symbolic_action_regulation", 0.0))

    field_fragmentation_bias = 1.0 if field_perception_label == "fragmented_perception_field" else 0.0
    field_strain_bias = 1.0 if field_perception_label == "strained_field" else 0.0
    field_coherence_bias = 1.0 if field_perception_label == "coherent_perception_field" else 0.0
    field_memory_bias = 1.0 if field_perception_label == "memory_reactivated_field" else 0.0
    field_activity_presence = _clip01(float(field_activity_island_count) / 4.0)

    field_perception_instability = _clip01(
        (field_perception_pressure * 0.42)
        + (field_perception_strain * 0.20)
        + (field_perception_fragmentation * 0.16)
        + (field_activity_island_pressure_mean * 0.18)
        + (field_activity_presence * 0.08)
        + (field_fragmentation_bias * 0.16)
        + (field_strain_bias * 0.12)
        - (field_perception_clarity * 0.18)
        - (field_perception_support * 0.10)
        - (field_perception_stability * 0.10)
    )
    field_observation_need = _clip01(
        (field_perception_instability * 0.42)
        + (field_perception_pressure * 0.24)
        + (field_perception_fragmentation * 0.16)
        + (field_perception_strain * 0.10)
        + (max(0.0, 1.0 - field_perception_clarity) * 0.14)
        + (field_activity_island_context_reactivation_mean * 0.08)
        + (field_fragmentation_bias * 0.08)
        + (field_strain_bias * 0.04)
        - (field_perception_focus * 0.06)
    )
    field_replan_pressure = _clip01(
        (field_perception_instability * 0.36)
        + (field_perception_pressure * 0.22)
        + (field_perception_fragmentation * 0.18)
        + (field_perception_strain * 0.12)
        + (max(0.0, 1.0 - field_perception_support) * 0.16)
        + (field_activity_island_context_reactivation_mean * 0.08)
        + (field_fragmentation_bias * 0.12)
        + (field_strain_bias * 0.06)
        - (field_perception_stability * 0.06)
    )
    field_bearing_support = _clip01(
        (field_perception_support * 0.34)
        + (field_perception_clarity * 0.28)
        + (field_perception_focus * 0.16)
        + (field_perception_stability * 0.14)
        + (field_activity_island_coherence_mean * 0.14)
        + (field_coherence_bias * 0.10)
        + (field_memory_bias * 0.04)
        - (field_perception_pressure * 0.18)
        - (field_perception_fragmentation * 0.14)
        - (field_perception_strain * 0.10)
        - (field_fragmentation_bias * 0.10)
    )
    action_readiness_from_field = field_bearing_support
    if symbolic_regulation > 0.0:
        field_observation_need = _clip01(field_observation_need * (1.0 - symbolic_regulation * 0.10))
        field_replan_pressure = _clip01(field_replan_pressure * (1.0 - symbolic_regulation * 0.08))
        action_readiness_from_field = _clip01(action_readiness_from_field + symbolic_action_regulation)

    return {
        "field_fragmentation_bias": float(field_fragmentation_bias),
        "field_strain_bias": float(field_strain_bias),
        "field_coherence_bias": float(field_coherence_bias),
        "field_memory_bias": float(field_memory_bias),
        "field_activity_presence": float(field_activity_presence),
        "field_perception_instability": float(field_perception_instability),
        "field_observation_need": float(field_observation_need),
        "field_replan_pressure": float(field_replan_pressure),
        "field_bearing_support": float(field_bearing_support),
        "action_readiness_from_field": float(action_readiness_from_field),
        "field_action_support": float(action_readiness_from_field),
    }


def _apply_form_symbol_learning_regulation(field_state=None, form_state=None):

    field = dict(field_state or {})
    form = dict(form_state or {})

    field_observation_need = _clip01(field.get("field_observation_need", 0.0))
    field_replan_pressure = _clip01(field.get("field_replan_pressure", 0.0))
    field_bearing_support = _clip01(field.get("field_bearing_support", field.get("field_action_support", 0.0)))
    field_action_support = _clip01(field.get("action_readiness_from_field", field.get("field_action_support", field_bearing_support)))

    form_symbol_action_binding = _clip01(form.get("form_symbol_action_binding", 0.50))
    form_symbol_observation_binding = _clip01(form.get("form_symbol_observation_binding", 0.0))
    form_symbol_reframe_binding = _clip01(form.get("form_symbol_reframe_binding", 0.0))
    form_symbol_development_quality = max(-1.0, min(1.0, float(form.get("form_symbol_development_quality", 0.0) or 0.0)))
    form_symbol_caution_trust = _clip01(form.get("form_symbol_caution_trust", 0.0))
    form_symbol_contact_pain_memory = _clip01(form.get("form_symbol_contact_pain_memory", 0.0))
    form_symbol_contact_carefulness = _clip01(form.get("form_symbol_contact_carefulness", 0.0))
    form_symbol_contact_burden_evidence = _clip01(form.get("form_symbol_contact_burden_evidence", 0.0))
    form_symbol_contact_maturity = _clip01(form.get("form_symbol_contact_maturity", 0.0))
    form_symbol_contact_utility = _clip01(form.get("form_symbol_contact_utility", 0.0))
    form_symbol_contact_utility_evidence = _clip01(form.get("form_symbol_contact_utility_evidence", 0.0))
    form_symbol_action_trust = _clip01(form.get("form_symbol_action_trust", 0.0))
    form_symbol_contact_learning_state = str(form.get("form_symbol_contact_learning_state", "unformed_contact") or "unformed_contact")
    variant_learning_pressure = _clip01(form.get("variant_learning_pressure", 0.0))

    learned_development_uncertainty = _clip01(
        (max(0.0, 0.46 - form_symbol_action_binding) * 0.74)
        + (form_symbol_observation_binding * 0.22)
        + (form_symbol_reframe_binding * 0.18)
        + (max(0.0, -form_symbol_development_quality) * 0.26)
        + (form_symbol_caution_trust * 0.44)
        + (form_symbol_contact_pain_memory * 0.18)
        + (form_symbol_contact_carefulness * 0.12)
        + (form_symbol_contact_burden_evidence * 0.16)
        + (variant_learning_pressure * 0.12)
        - (form_symbol_contact_maturity * 0.08)
        - (form_symbol_contact_utility * 0.05)
        - (form_symbol_contact_utility_evidence * 0.05)
        - (form_symbol_action_trust * 0.10)
    )

    if learned_development_uncertainty > 0.0:
        field_observation_need = _clip01(field_observation_need + (learned_development_uncertainty * 0.08))
        field_replan_pressure = _clip01(field_replan_pressure + (form_symbol_reframe_binding * 0.06) + (learned_development_uncertainty * 0.035))
        field_action_support = _clip01(field_action_support - (learned_development_uncertainty * 0.060))

    contact_state_observe_bias = 0.0
    contact_state_replan_bias = 0.0
    contact_state_action_bias = 0.0
    if form_symbol_contact_learning_state == "burdened_contact":
        contact_state_observe_bias = 0.035
        contact_state_replan_bias = 0.020
        contact_state_action_bias = -0.030
    elif form_symbol_contact_learning_state == "careful_contact":
        contact_state_observe_bias = 0.026
        contact_state_replan_bias = 0.014
        contact_state_action_bias = -0.018
    elif form_symbol_contact_learning_state == "learning_contact":
        contact_state_observe_bias = 0.014
        contact_state_replan_bias = 0.010
        contact_state_action_bias = -0.006
    elif form_symbol_contact_learning_state in ("maturing_contact", "constructive_contact"):
        contact_state_action_bias = min(0.026, (form_symbol_contact_maturity * form_symbol_contact_utility) + (form_symbol_contact_utility_evidence * 0.04))

    if form_symbol_contact_maturity > 0.0 or form_symbol_contact_pain_memory > 0.0 or form_symbol_contact_burden_evidence > 0.0:
        field_observation_need = _clip01(
            field_observation_need
            + (form_symbol_contact_carefulness * 0.055)
            + (form_symbol_contact_pain_memory * 0.040)
            + (form_symbol_contact_burden_evidence * 0.045)
            + contact_state_observe_bias
        )
        field_replan_pressure = _clip01(
            field_replan_pressure
            + (form_symbol_contact_carefulness * 0.040)
            + (form_symbol_contact_burden_evidence * 0.025)
            + contact_state_replan_bias
        )
        field_action_support = _clip01(
            field_action_support
            + (form_symbol_contact_maturity * form_symbol_contact_utility * 0.055)
            + (form_symbol_contact_utility_evidence * 0.018)
            - (form_symbol_contact_pain_memory * 0.035)
            - (form_symbol_contact_burden_evidence * 0.035)
            + contact_state_action_bias
        )

    if variant_learning_pressure > 0.0:
        field_observation_need = _clip01(field_observation_need + (variant_learning_pressure * 0.070))
        field_replan_pressure = _clip01(field_replan_pressure + (variant_learning_pressure * 0.040))
        field_action_support = _clip01(field_action_support - (variant_learning_pressure * 0.025))

    return {
        "field_observation_need": float(field_observation_need),
        "field_replan_pressure": float(field_replan_pressure),
        "field_bearing_support": float(field_bearing_support),
        "action_readiness_from_field": float(field_action_support),
        "field_action_support": float(field_action_support),
        "learned_development_uncertainty": float(learned_development_uncertainty),
        "contact_state_observe_bias": float(contact_state_observe_bias),
        "contact_state_replan_bias": float(contact_state_replan_bias),
        "contact_state_action_bias": float(contact_state_action_bias),
    }


def _build_orientation_state(context=None):

    ctx = dict(context or {})

    memory_support = _clip01(ctx.get("memory_support", 0.0))
    field_perception_clarity = _clip01(ctx.get("field_perception_clarity", 0.0))
    field_perception_support = _clip01(ctx.get("field_perception_support", 0.0))
    field_bearing_support = _clip01(ctx.get("field_bearing_support", ctx.get("field_action_support", 0.0)))
    action_readiness_from_field = _clip01(ctx.get("action_readiness_from_field", ctx.get("field_action_support", field_bearing_support)))
    field_action_support = action_readiness_from_field
    processing_alignment = _clip01(ctx.get("processing_alignment", 0.0))
    signal_quality = _clip01(ctx.get("signal_quality", 0.0))
    memory_inhibition = _clip01(ctx.get("memory_inhibition", 0.0))
    memory_conflict = _clip01(ctx.get("memory_conflict", 0.0))
    thinking_complexity = _clip01(ctx.get("thinking_complexity", 0.0))
    memory_compare_load = _clip01(ctx.get("memory_compare_load", 0.0))
    decision_energy_cost = _clip01(ctx.get("decision_energy_cost", 0.0))
    processing_load = _clip01(ctx.get("processing_load", 0.0))
    field_observation_need = _clip01(ctx.get("field_observation_need", 0.0))
    cognitive_load = _clip01(ctx.get("cognitive_load", 0.0))
    structure_quality = _clip01(ctx.get("structure_quality", 0.0))
    context_confidence = _clip01(ctx.get("context_confidence", 0.0))

    memory_orientation = _clip01(
        (memory_support * 0.30)
        + (field_perception_clarity * 0.20)
        + (field_perception_support * 0.16)
        + (field_bearing_support * 0.14)
        + (processing_alignment * 0.10)
        + (signal_quality * 0.10)
        - (memory_inhibition * 0.16)
        - (memory_conflict * 0.10)
    )
    orientation_gap = _clip01(
        (thinking_complexity * 0.30)
        + (memory_compare_load * 0.20)
        + (decision_energy_cost * 0.20)
        + (processing_load * 0.14)
        + (field_observation_need * 0.10)
        - (memory_orientation * 0.34)
        - (field_perception_clarity * 0.10)
    )
    blind_thinking_load = _clip01(
        (thinking_complexity * 0.32)
        + (memory_compare_load * 0.18)
        + (memory_inhibition * 0.16)
        + (decision_energy_cost * 0.16)
        + (cognitive_load * 0.12)
        + (max(0.0, 0.12 - memory_support) * 0.28)
        + (max(0.0, 0.30 - field_perception_clarity) * 0.12)
    )
    structure_orientation = _clip01(
        (structure_quality * 0.34)
        + (context_confidence * 0.22)
        + (field_bearing_support * 0.14)
        + (field_perception_clarity * 0.10)
        + (processing_alignment * 0.08)
        + (memory_orientation * 0.08)
        + (memory_support * 0.10)
        - (memory_inhibition * 0.08)
    )
    structure_orientation_gap = _clip01(
        (max(0.0, 0.56 - structure_quality) * 0.46)
        + (max(0.0, 0.54 - context_confidence) * 0.26)
        + (max(0.0, 0.22 - memory_orientation) * 0.16)
        + (max(0.0, 0.10 - memory_support) * 0.12)
    )

    return {
        "memory_orientation": float(memory_orientation),
        "orientation_gap": float(orientation_gap),
        "blind_thinking_load": float(blind_thinking_load),
        "structure_orientation": float(structure_orientation),
        "structure_orientation_gap": float(structure_orientation_gap),
    }


def _build_structure_action_state(context=None):

    ctx = dict(context or {})

    structure_quality = _clip01(ctx.get("structure_quality", 0.0))
    context_confidence = _clip01(ctx.get("context_confidence", 0.0))
    field_bearing_support = _clip01(ctx.get("field_bearing_support", ctx.get("field_action_support", 0.0)))
    action_readiness_from_field = _clip01(ctx.get("action_readiness_from_field", ctx.get("field_action_support", field_bearing_support)))
    field_action_support = action_readiness_from_field
    field_observation_need = _clip01(ctx.get("field_observation_need", 0.0))
    field_replan_pressure = _clip01(ctx.get("field_replan_pressure", 0.0))
    memory_support = _clip01(ctx.get("memory_support", 0.0))
    memory_orientation = _clip01(ctx.get("memory_orientation", 0.0))
    symbolic_action_regulation = _clip01(ctx.get("symbolic_action_regulation", 0.0))
    form_symbol_action_binding = _clip01(ctx.get("form_symbol_action_binding", 0.0))
    variant_bearing_memory = _clip01(ctx.get("variant_bearing_memory", 0.0))
    uncertainty_familiarity = _clip01(ctx.get("uncertainty_familiarity", 0.0))
    memory_inhibition = _clip01(ctx.get("memory_inhibition", 0.0))
    action_structure_min = _clip01(ctx.get("action_structure_min", 0.70))
    mid_support_min = max(0.0, float(ctx.get("mid_support_min", 0.045) or 0.045))
    learned_development_uncertainty = _clip01(ctx.get("learned_development_uncertainty", 0.0))
    variant_learning_pressure = _clip01(ctx.get("variant_learning_pressure", 0.0))
    uncertain_form_exposure = _clip01(ctx.get("uncertain_form_exposure", 0.0))

    structure_action_bearing = _clip01(
        (structure_quality * 0.42)
        + (context_confidence * 0.22)
        + (action_readiness_from_field * 0.12)
        + (memory_support * 0.12)
        + (memory_orientation * 0.08)
        + (symbolic_action_regulation * 0.04)
        + (form_symbol_action_binding * 0.08)
        + (variant_bearing_memory * 0.06)
        + (uncertainty_familiarity * max(0.0, variant_bearing_memory - 0.36) * 0.04)
        - (memory_inhibition * 0.08)
    )
    structure_action_gap = _clip01(
        max(0.0, action_structure_min - structure_quality)
        + max(0.0, mid_support_min - max(memory_support, action_readiness_from_field * 0.18))
        + max(0.0, 0.40 - context_confidence) * 0.40
    )
    structure_action_uncertainty = _clip01(
        (structure_action_gap * 0.58)
        + (max(0.0, 0.55 - structure_quality) * 0.42)
        + (learned_development_uncertainty * 0.35)
        + (variant_learning_pressure * 0.18)
        + (max(0.0, uncertain_form_exposure - variant_bearing_memory) * 0.14)
        + (max(0.0, mid_support_min - memory_support) * 1.25)
    )
    structure_carrying_need = _clip01(
        (structure_action_uncertainty * 0.34)
        + (max(0.0, 0.58 - structure_quality) * 0.24)
        + (max(0.0, 0.46 - context_confidence) * 0.16)
        + (max(0.0, 0.20 - memory_orientation) * 0.12)
        + (max(0.0, 0.22 - action_readiness_from_field) * 0.14)
        + (variant_learning_pressure * 0.08)
        - (variant_bearing_memory * 0.04)
    )
    if structure_action_uncertainty > 0.0:
        field_observation_need = _clip01(field_observation_need + (structure_action_uncertainty * 0.10))
        field_replan_pressure = _clip01(field_replan_pressure + (structure_action_uncertainty * 0.055))
        action_readiness_from_field = _clip01(action_readiness_from_field - (structure_action_uncertainty * 0.055))
        field_action_support = action_readiness_from_field

    return {
        "structure_action_bearing": float(structure_action_bearing),
        "structure_action_gap": float(structure_action_gap),
        "structure_action_uncertainty": float(structure_action_uncertainty),
        "structure_carrying_need": float(structure_carrying_need),
        "field_observation_need": float(field_observation_need),
        "field_replan_pressure": float(field_replan_pressure),
        "field_bearing_support": float(field_bearing_support),
        "action_readiness_from_field": float(action_readiness_from_field),
        "field_action_support": float(field_action_support),
    }


def _build_visual_action_grounding_state(field_state=None, visual_state=None):
    field = dict(field_state or {})
    visual = dict(visual_state or {})

    field_observation_need = float(field.get("field_observation_need", 0.0) or 0.0)
    field_replan_pressure = float(field.get("field_replan_pressure", 0.0) or 0.0)
    field_bearing_support = float(field.get("field_bearing_support", field.get("field_action_support", 0.0)) or 0.0)
    action_readiness_from_field = float(field.get("action_readiness_from_field", field.get("field_action_support", field_bearing_support)) or 0.0)
    field_action_support = action_readiness_from_field
    structure_action_uncertainty = float(field.get("structure_action_uncertainty", 0.0) or 0.0)
    structure_carrying_need = float(field.get("structure_carrying_need", 0.0) or 0.0)

    visual_blindness = float(visual.get("visual_blindness", 0.0) or 0.0)
    visual_clarity = float(visual.get("visual_clarity", 0.0) or 0.0)
    visual_object_stability = float(visual.get("visual_object_stability", 0.0) or 0.0)
    visual_shape_fragility = float(visual.get("visual_shape_fragility", 0.0) or 0.0)
    visual_form_pressure = float(visual.get("visual_form_pressure", 0.0) or 0.0)
    structure_quality = float(visual.get("structure_quality", 0.0) or 0.0)
    visual_shape_resonance = float(visual.get("visual_shape_resonance", 0.0) or 0.0)
    structure_action_bearing = float(visual.get("structure_action_bearing", 0.0) or 0.0)
    field_perception_clarity = float(visual.get("field_perception_clarity", 0.0) or 0.0)
    visual_form_novelty = float(visual.get("visual_form_novelty", 0.0) or 0.0)
    memory_orientation = float(visual.get("memory_orientation", 0.0) or 0.0)
    visual_coherence = float(visual.get("visual_coherence", 0.0) or 0.0)
    visual_reflective_coherence = float(visual.get("visual_reflective_coherence", visual_coherence) or 0.0)
    context_confidence = float(visual.get("context_confidence", 0.0) or 0.0)
    market_balance = float(visual.get("market_balance", 0.0) or 0.0)
    form_symbol_containment = float(visual.get("form_symbol_containment", 0.0) or 0.0)
    form_symbol_object_distance = float(visual.get("form_symbol_object_distance", 0.0) or 0.0)
    visual_cortex_presence = float(visual.get("visual_cortex_presence", visual.get("object_presence", 0.0)) or 0.0)
    visual_cortex_clarity = float(visual.get("visual_cortex_clarity", visual.get("object_clarity", 0.0)) or 0.0)
    visual_cortex_relation_coherence = float(visual.get("visual_cortex_relation_coherence", visual.get("relation_coherence", 0.0)) or 0.0)
    visual_cortex_readiness = float(visual.get("visual_cortex_readiness", visual.get("visual_readiness", 0.0)) or 0.0)
    visual_object_binding_quality = float(visual.get("visual_object_binding_quality", 0.0) or 0.0)
    visual_contact_nearness = float(visual.get("visual_contact_nearness", 0.0) or 0.0)
    visual_lifecycle_stability = float(visual.get("visual_lifecycle_stability", 0.0) or 0.0)
    visual_lifecycle_rejection = float(visual.get("visual_lifecycle_rejection", 0.0) or 0.0)
    visual_lifecycle_dissolution = float(visual.get("visual_lifecycle_dissolution", 0.0) or 0.0)
    visual_cortex_grounding = max(
        0.0,
        min(
            1.0,
            (visual_object_binding_quality * 0.24)
            + (visual_cortex_relation_coherence * 0.20)
            + (visual_cortex_clarity * 0.16)
            + (visual_cortex_readiness * 0.14)
            + (visual_lifecycle_stability * 0.12)
            + (visual_contact_nearness * 0.08)
            + (visual_cortex_presence * 0.06)
            - (visual_lifecycle_rejection * 0.10)
            - (visual_lifecycle_dissolution * 0.08),
        ),
    )

    visual_blind_action_load = max(
        0.0,
        min(
            1.0,
            (visual_blindness * 0.30)
            + (max(0.0, 0.38 - visual_clarity) * 0.22)
            + (max(0.0, 0.42 - visual_object_stability) * 0.18)
            + (visual_shape_fragility * 0.12)
            + (visual_form_pressure * 0.10)
            + (max(0.0, 0.58 - structure_quality) * 0.12)
            - (visual_shape_resonance * 0.10)
            - (structure_action_bearing * 0.08),
        ),
    )
    visual_action_uncertainty = max(
        0.0,
        min(
            1.0,
            (visual_blind_action_load * 0.44)
            + (structure_action_uncertainty * 0.24)
            + (max(0.0, 0.46 - field_perception_clarity) * 0.14)
            + (max(0.0, 0.28 - action_readiness_from_field) * 0.12)
            + (visual_form_novelty * 0.06)
            - (memory_orientation * 0.08),
        ),
    )
    visual_object_binding = max(
        0.0,
        min(
            1.0,
            (visual_object_stability * 0.24)
            + (visual_clarity * 0.20)
            + (visual_reflective_coherence * 0.14)
            + (structure_quality * 0.14)
            + (context_confidence * 0.10)
            + (market_balance * 0.08)
            + (min(visual_shape_resonance, visual_object_stability) * 0.10)
            + (visual_cortex_grounding * 0.14)
            - (visual_blindness * 0.12)
            - (visual_shape_fragility * 0.08),
        ),
    )
    visual_grounding_strength = max(
        0.0,
        min(
            1.0,
            (visual_object_binding * 0.38)
            + (structure_action_bearing * 0.20)
            + (field_perception_clarity * 0.12)
            + (memory_orientation * 0.10)
            + (form_symbol_containment * 0.08)
            + (form_symbol_object_distance * 0.06)
            + (context_confidence * 0.06)
            + (visual_cortex_grounding * 0.12)
            - (max(0.0, visual_shape_resonance - visual_object_binding) * 0.16),
        ),
    )
    visual_resonance_unbound = max(
        0.0,
        min(
            1.0,
            (max(0.0, visual_shape_resonance - visual_object_binding) * 0.46)
            + (visual_form_pressure * 0.14)
            + (visual_blindness * 0.14)
            + (visual_shape_fragility * 0.12)
            + (max(0.0, 0.50 - context_confidence) * 0.08)
            + (max(0.0, 0.52 - structure_quality) * 0.06)
            - (visual_cortex_grounding * 0.08),
        ),
    )
    visual_grounding_gap = max(
        0.0,
        min(
            1.0,
            (max(0.0, 0.56 - visual_object_binding) * 0.30)
            + (visual_resonance_unbound * 0.28)
            + (max(0.0, 0.50 - visual_grounding_strength) * 0.24)
            + (visual_blind_action_load * 0.12)
            + (structure_action_uncertainty * 0.06)
            - (visual_cortex_grounding * 0.08),
        ),
    )
    visual_grounding_need = max(
        0.0,
        min(
            1.0,
            (visual_grounding_gap * 0.36)
            + (visual_resonance_unbound * 0.26)
            + (visual_action_uncertainty * 0.18)
            + (max(0.0, 0.44 - visual_clarity) * 0.10)
            + (max(0.0, 0.46 - visual_object_stability) * 0.10),
        ),
    )
    visual_rational_observation_support = max(
        0.0,
        min(
            1.0,
            (visual_grounding_need * 0.28)
            + (max(0.0, visual_shape_resonance - visual_object_binding) * 0.18)
            + (form_symbol_object_distance * 0.12)
            + (field_perception_clarity * 0.08)
            - (visual_grounding_strength * 0.08),
        ),
    )
    visual_grounding_pressures = {
        "unbound_resonance": _clip01((visual_resonance_unbound * 0.62) + ((1.0 - visual_grounding_strength) * 0.38)),
        "needs_visual_grounding": _clip01(visual_grounding_need),
        "shape_without_object": _clip01((visual_shape_resonance * 0.56) + ((1.0 - visual_object_binding) * 0.44)),
        "cortex_grounded_object": _clip01((visual_cortex_grounding * 0.52) + (visual_object_binding * 0.48)),
        "grounded_object": _clip01((visual_grounding_strength * 0.54) + (visual_object_binding * 0.46)),
    }
    visual_grounding_state = max(visual_grounding_pressures, key=visual_grounding_pressures.get)

    if visual_grounding_need > 0.0:
        field_observation_need = max(
            0.0,
            min(1.0, field_observation_need + (visual_grounding_need * 0.070)),
        )
        field_replan_pressure = max(
            0.0,
            min(1.0, field_replan_pressure + (max(0.0, visual_grounding_need - 0.22) * 0.045)),
        )
        action_readiness_from_field = max(
            0.0,
            min(1.0, action_readiness_from_field - (visual_grounding_gap * 0.035)),
        )
        field_action_support = action_readiness_from_field
        visual_action_uncertainty = max(
            0.0,
            min(1.0, visual_action_uncertainty + (visual_grounding_gap * 0.075)),
        )
    if visual_action_uncertainty > 0.0:
        field_observation_need = max(
            0.0,
            min(1.0, field_observation_need + (visual_action_uncertainty * 0.075)),
        )
        field_replan_pressure = max(
            0.0,
            min(1.0, field_replan_pressure + (visual_action_uncertainty * 0.040)),
        )
        action_readiness_from_field = max(
            0.0,
            min(1.0, action_readiness_from_field - (visual_action_uncertainty * 0.035)),
        )
        field_action_support = action_readiness_from_field
        structure_action_uncertainty = max(
            0.0,
            min(1.0, structure_action_uncertainty + (visual_action_uncertainty * 0.085)),
        )
        structure_carrying_need = max(
            0.0,
            min(1.0, structure_carrying_need + (visual_action_uncertainty * 0.095)),
        )

    return {
        "visual_blind_action_load": float(visual_blind_action_load),
        "visual_action_uncertainty": float(visual_action_uncertainty),
        "visual_object_binding": float(visual_object_binding),
        "visual_cortex_grounding": float(visual_cortex_grounding),
        "visual_grounding_strength": float(visual_grounding_strength),
        "visual_resonance_unbound": float(visual_resonance_unbound),
        "visual_grounding_gap": float(visual_grounding_gap),
        "visual_grounding_need": float(visual_grounding_need),
        "visual_rational_observation_support": float(visual_rational_observation_support),
        "visual_grounding_state": str(visual_grounding_state),
        "field_observation_need": float(field_observation_need),
        "field_replan_pressure": float(field_replan_pressure),
        "field_bearing_support": float(field_bearing_support),
        "action_readiness_from_field": float(action_readiness_from_field),
        "field_action_support": float(field_action_support),
        "structure_action_uncertainty": float(structure_action_uncertainty),
        "structure_carrying_need": float(structure_carrying_need),
    }


def _build_semantic_transfer_state(field_state=None, semantic_state=None):
    field = dict(field_state or {})
    semantic = dict(semantic_state or {})

    field_observation_need = float(field.get("field_observation_need", 0.0) or 0.0)
    field_replan_pressure = float(field.get("field_replan_pressure", 0.0) or 0.0)
    field_bearing_support = float(field.get("field_bearing_support", field.get("field_action_support", 0.0)) or 0.0)
    action_readiness_from_field = float(field.get("action_readiness_from_field", field.get("field_action_support", field_bearing_support)) or 0.0)
    field_action_support = action_readiness_from_field

    form_symbol_maturity = float(semantic.get("form_symbol_maturity", 0.0) or 0.0)
    form_symbol_stability = float(semantic.get("form_symbol_stability", 0.0) or 0.0)
    form_symbol_learning_trust = float(semantic.get("form_symbol_learning_trust", 0.0) or 0.0)
    form_symbol_action_trust = float(semantic.get("form_symbol_action_trust", 0.0) or 0.0)
    form_symbol_development_quality = float(semantic.get("form_symbol_development_quality", 0.0) or 0.0)
    form_symbol_compound_bearing = float(semantic.get("form_symbol_compound_bearing", 0.0) or 0.0)
    active_context_support = float(semantic.get("active_context_support", 0.0) or 0.0)
    memory_orientation = float(semantic.get("memory_orientation", 0.0) or 0.0)
    memory_support = float(semantic.get("memory_support", 0.0) or 0.0)
    context_confidence = float(semantic.get("context_confidence", 0.0) or 0.0)
    structure_orientation = float(semantic.get("structure_orientation", 0.0) or 0.0)
    field_perception_clarity = float(semantic.get("field_perception_clarity", 0.0) or 0.0)
    active_context_bearing = float(semantic.get("active_context_bearing", 0.0) or 0.0)
    memory_conflict = float(semantic.get("memory_conflict", 0.0) or 0.0)
    active_context_conflict = float(semantic.get("active_context_conflict", 0.0) or 0.0)
    form_symbol_novelty = float(semantic.get("form_symbol_novelty", 0.0) or 0.0)
    form_symbol_compound_novelty = float(semantic.get("form_symbol_compound_novelty", 0.0) or 0.0)
    form_symbol_distance = float(semantic.get("form_symbol_distance", 0.0) or 0.0)
    form_symbol_zoom_need = float(semantic.get("form_symbol_zoom_need", 0.0) or 0.0)
    form_symbol_detail_pressure = float(semantic.get("form_symbol_detail_pressure", 0.0) or 0.0)
    learned_development_uncertainty = float(semantic.get("learned_development_uncertainty", 0.0) or 0.0)
    structure_action_uncertainty = float(semantic.get("structure_action_uncertainty", 0.0) or 0.0)
    variant_learning_pressure = float(semantic.get("variant_learning_pressure", 0.0) or 0.0)
    variant_spread = float(semantic.get("variant_spread", 0.0) or 0.0)
    uncertain_form_exposure = float(semantic.get("uncertain_form_exposure", 0.0) or 0.0)
    orientation_gap = float(semantic.get("orientation_gap", 0.0) or 0.0)
    blind_thinking_load = float(semantic.get("blind_thinking_load", 0.0) or 0.0)
    structure_action_bearing = float(semantic.get("structure_action_bearing", 0.0) or 0.0)
    form_symbol_action_binding = float(semantic.get("form_symbol_action_binding", 0.0) or 0.0)
    variant_bearing_memory = float(semantic.get("variant_bearing_memory", 0.0) or 0.0)
    form_symbol_caution_trust = float(semantic.get("form_symbol_caution_trust", 0.0) or 0.0)
    expectation_pressure = float(semantic.get("expectation_pressure", 0.0) or 0.0)
    aftereffect_pressure = float(semantic.get("aftereffect_pressure", 0.0) or 0.0)

    known_form_support = max(
        0.0,
        min(
            1.0,
            (form_symbol_maturity * 0.18)
            + (form_symbol_stability * 0.16)
            + (form_symbol_learning_trust * 0.18)
            + (form_symbol_action_trust * 0.12)
            + (max(0.0, form_symbol_development_quality) * 0.12)
            + (form_symbol_compound_bearing * 0.12)
            + (active_context_support * 0.12),
        ),
    )
    route_familiarity = max(
        0.0,
        min(
            1.0,
            (known_form_support * 0.30)
            + (memory_orientation * 0.20)
            + (memory_support * 0.16)
            + (context_confidence * 0.12)
            + (structure_orientation * 0.10)
            + (field_perception_clarity * 0.08)
            + (active_context_bearing * 0.04)
            - (memory_conflict * 0.08)
            - (active_context_conflict * 0.08),
        ),
    )
    semantic_shift_pressure = max(
        0.0,
        min(
            1.0,
            (form_symbol_novelty * 0.18)
            + (form_symbol_compound_novelty * 0.12)
            + (form_symbol_distance * 0.10)
            + (form_symbol_zoom_need * 0.10)
            + (form_symbol_detail_pressure * 0.08)
            + (learned_development_uncertainty * 0.14)
            + (structure_action_uncertainty * 0.12)
            + (variant_learning_pressure * 0.10)
            + (variant_spread * uncertain_form_exposure * 0.08)
            + (orientation_gap * 0.10)
            + (blind_thinking_load * 0.08)
            + (memory_conflict * 0.05)
            + (active_context_conflict * 0.05)
            - (route_familiarity * 0.20)
            - (known_form_support * 0.06),
        ),
    )
    transfer_bearing = max(
        0.0,
        min(
            1.0,
            (route_familiarity * 0.26)
            + (structure_action_bearing * 0.18)
            + (memory_orientation * 0.16)
            + (known_form_support * 0.14)
            + (context_confidence * 0.10)
            + (field_bearing_support * 0.08)
            + (form_symbol_action_binding * 0.08)
            + (variant_bearing_memory * 0.06)
            - (semantic_shift_pressure * 0.16)
            - (learned_development_uncertainty * 0.08),
        ),
    )
    trust_transfer_base = max(
        0.0,
        min(
            1.0,
            (form_symbol_learning_trust * 0.24)
            + (form_symbol_action_trust * 0.18)
            + ((1.0 - form_symbol_caution_trust) * 0.14)
            + (max(0.0, form_symbol_development_quality) * 0.14)
            + (memory_orientation * 0.12)
            + (active_context_support * 0.08)
            + (structure_action_bearing * 0.10),
        ),
    )
    trust_transfer_support = max(
        0.0,
        min(
            1.0,
            (trust_transfer_base * 0.34)
            + (route_familiarity * 0.24)
            + (transfer_bearing * 0.20)
            + (structure_orientation * 0.12)
            + (context_confidence * 0.10)
            - (semantic_shift_pressure * 0.14)
            - (structure_action_uncertainty * 0.10),
        ),
    )
    transfer_maturity_gap = max(
        0.0,
        min(
            1.0,
            ((1.0 - trust_transfer_support) * 0.28)
            + ((1.0 - transfer_bearing) * 0.22)
            + ((1.0 - route_familiarity) * 0.16)
            + (semantic_shift_pressure * 0.14)
            + (structure_action_uncertainty * 0.12)
            + (learned_development_uncertainty * 0.10)
            + (form_symbol_caution_trust * 0.06)
            + (variant_learning_pressure * 0.08)
            - (form_symbol_action_trust * 0.06),
        ),
    )
    trust_transfer_mode_pressures = {
        "immature_transfer_watch": _clip01((transfer_maturity_gap * 0.58) + ((1.0 - trust_transfer_support) * 0.42)),
        "partial_transfer": _clip01((transfer_maturity_gap * 0.44) + (transfer_bearing * 0.20) + (route_familiarity * 0.16)),
        "bearing_transfer": _clip01((trust_transfer_support * 0.46) + (transfer_bearing * 0.38) + (route_familiarity * 0.16)),
        "trusted_transfer": _clip01((trust_transfer_support * 0.50) + (route_familiarity * 0.26) + (context_confidence * 0.24)),
    }
    trust_transfer_mode = max(trust_transfer_mode_pressures, key=trust_transfer_mode_pressures.get)
    interpretation_quality = max(
        0.0,
        min(
            1.0,
            (route_familiarity * 0.30)
            + (transfer_bearing * 0.24)
            + (memory_orientation * 0.16)
            + (field_perception_clarity * 0.12)
            + (structure_orientation * 0.10)
            + ((1.0 - orientation_gap) * 0.08)
            - (semantic_shift_pressure * 0.12),
        ),
    )
    transfer_break_fatigue = max(
        0.0,
        min(
            1.0,
            (transfer_maturity_gap * 0.26)
            + (expectation_pressure * 0.18)
            + (aftereffect_pressure * 0.14)
            + (learned_development_uncertainty * 0.14)
            + (structure_action_uncertainty * 0.12)
            + (max(0.0, 0.46 - trust_transfer_support) * 0.20)
            + (max(0.0, 0.42 - transfer_bearing) * 0.14)
            + (field_replan_pressure * 0.08)
            - (form_symbol_action_trust * 0.08)
            - (max(0.0, trust_transfer_support - 0.48) * 0.10),
        ),
    )
    transfer_recovery_need = max(
        0.0,
        min(
            1.0,
            (transfer_break_fatigue * 0.38)
            + (orientation_gap * 0.18)
            + (blind_thinking_load * 0.14)
            + (field_observation_need * 0.12)
            + (max(0.0, 0.50 - interpretation_quality) * 0.18),
        ),
    )
    transfer_break_trigger = max(
        0.0,
        min(
            1.0,
            (transfer_break_fatigue * 0.32)
            + (transfer_maturity_gap * 0.20)
            + (structure_action_uncertainty * 0.16)
            + (max(0.0, 0.42 - transfer_bearing) * 0.14)
            + (max(0.0, 0.42 - trust_transfer_support) * 0.12)
            + (expectation_pressure * 0.10)
            + (aftereffect_pressure * 0.08)
            - (structure_action_bearing * 0.10)
            - (form_symbol_action_trust * 0.06),
        ),
    )
    transfer_break_pressure = _clip01(
        (transfer_break_trigger * 0.34)
        + (transfer_maturity_gap * 0.24)
        + ((1.0 - trust_transfer_support) * 0.16)
        + ((1.0 - transfer_bearing) * 0.14)
        + ((1.0 - structure_action_bearing) * 0.12)
    )
    transfer_break_ready = bool(transfer_break_pressure > trust_transfer_support)
    adaptation_phase_pressures = {
        "transfer_break_fatigue": _clip01((transfer_break_pressure * 0.56) + (transfer_break_fatigue * 0.44)),
        "immature_transfer_watch": _clip01((transfer_maturity_gap * 0.56) + ((1.0 - trust_transfer_support) * 0.44)),
        "new_market_grammar_watch": _clip01((semantic_shift_pressure * 0.58) + ((1.0 - route_familiarity) * 0.42)),
        "transfer_observe": _clip01(((1.0 - transfer_bearing) * 0.52) + (semantic_shift_pressure * 0.30)),
        "familiar_route": _clip01((route_familiarity * 0.54) + (transfer_bearing * 0.46)),
        "interpretation_watch": _clip01((interpretation_quality * 0.36) + (field_observation_need * 0.22) + (orientation_gap * 0.16)),
    }
    adaptation_phase = max(adaptation_phase_pressures, key=adaptation_phase_pressures.get)
    transfer_gap = max(0.0, 1.0 - transfer_bearing)
    if semantic_shift_pressure > 0.0:
        field_observation_need = max(
            0.0,
            min(1.0, field_observation_need + (semantic_shift_pressure * transfer_gap * 0.075)),
        )
        field_replan_pressure = max(
            0.0,
            min(1.0, field_replan_pressure + (semantic_shift_pressure * transfer_gap * 0.045)),
        )
        action_readiness_from_field = max(
            0.0,
            min(1.0, action_readiness_from_field - (semantic_shift_pressure * transfer_gap * 0.040)),
        )
        field_action_support = action_readiness_from_field
    if transfer_maturity_gap > 0.0:
        field_observation_need = max(
            0.0,
            min(1.0, field_observation_need + (transfer_maturity_gap * 0.065)),
        )
        field_replan_pressure = max(
            0.0,
            min(1.0, field_replan_pressure + (max(0.0, transfer_maturity_gap - 0.38) * 0.070)),
        )
        action_readiness_from_field = max(
            0.0,
            min(1.0, action_readiness_from_field - (transfer_maturity_gap * 0.045)),
        )
        field_action_support = action_readiness_from_field
    fatigue_excess = max(0.0, transfer_break_fatigue - 0.34)
    if fatigue_excess > 0.0:
        field_observation_need = max(
            0.0,
            min(1.0, field_observation_need + (fatigue_excess * 0.045)),
        )
        field_replan_pressure = max(
            0.0,
            min(1.0, field_replan_pressure + (max(0.0, transfer_recovery_need - 0.34) * 0.055)),
        )
        action_readiness_from_field = max(
            0.0,
            min(1.0, action_readiness_from_field - (fatigue_excess * 0.022)),
        )
        field_action_support = action_readiness_from_field

    return {
        "known_form_support": float(known_form_support),
        "route_familiarity": float(route_familiarity),
        "semantic_shift_pressure": float(semantic_shift_pressure),
        "transfer_bearing": float(transfer_bearing),
        "trust_transfer_base": float(trust_transfer_base),
        "trust_transfer_support": float(trust_transfer_support),
        "transfer_maturity_gap": float(transfer_maturity_gap),
        "trust_transfer_mode": str(trust_transfer_mode),
        "interpretation_quality": float(interpretation_quality),
        "transfer_break_fatigue": float(transfer_break_fatigue),
        "transfer_recovery_need": float(transfer_recovery_need),
        "transfer_break_trigger": float(transfer_break_trigger),
        "transfer_break_ready": bool(transfer_break_ready),
        "adaptation_phase": str(adaptation_phase),
        "transfer_gap": float(transfer_gap),
        "fatigue_excess": float(fatigue_excess),
        "field_observation_need": float(field_observation_need),
        "field_replan_pressure": float(field_replan_pressure),
        "field_bearing_support": float(field_bearing_support),
        "action_readiness_from_field": float(action_readiness_from_field),
        "field_action_support": float(field_action_support),
    }


def _build_action_activation_state(context=None):
    ctx = dict(context or {})

    protective_courage = float(ctx.get("protective_courage", 0.0) or 0.0)
    load_bearing_capacity = float(ctx.get("load_bearing_capacity", 0.0) or 0.0)
    state_maturity = float(ctx.get("state_maturity", 0.0) or 0.0)
    decision_readiness = float(ctx.get("decision_readiness", 0.0) or 0.0)
    felt_alignment = float(ctx.get("felt_alignment", 0.0) or 0.0)
    experience_regulation = float(ctx.get("experience_regulation", 0.0) or 0.0)
    areal_support = float(ctx.get("areal_support", 0.0) or 0.0)
    processing_areal_support = float(ctx.get("processing_areal_support", 0.0) or 0.0)
    field_bearing_support = float(ctx.get("field_bearing_support", ctx.get("field_action_support", 0.0)) or 0.0)
    action_readiness_from_field = float(ctx.get("action_readiness_from_field", ctx.get("field_action_support", field_bearing_support)) or 0.0)
    field_action_support = action_readiness_from_field
    field_perception_instability = float(ctx.get("field_perception_instability", 0.0) or 0.0)
    expectation_pressure = float(ctx.get("expectation_pressure", 0.0) or 0.0)
    felt_pressure = float(ctx.get("felt_pressure", 0.0) or 0.0)
    decision_conflict = float(ctx.get("decision_conflict", 0.0) or 0.0)
    processing_tension = float(ctx.get("processing_tension", 0.0) or 0.0)
    uncertainty_pressure = float(ctx.get("uncertainty_pressure", 0.0) or 0.0)
    aftereffect_pressure = float(ctx.get("aftereffect_pressure", 0.0) or 0.0)
    areal_conflict_pressure = float(ctx.get("areal_conflict_pressure", 0.0) or 0.0)
    processing_areal_tension = float(ctx.get("processing_areal_tension", 0.0) or 0.0)
    field_observation_need = float(ctx.get("field_observation_need", 0.0) or 0.0)
    field_replan_pressure = float(ctx.get("field_replan_pressure", 0.0) or 0.0)
    protective_width_regulation = float(ctx.get("protective_width_regulation", 0.0) or 0.0)
    symbolic_regulation = float(ctx.get("symbolic_regulation", 0.0) or 0.0)
    symbolic_action_regulation = float(ctx.get("symbolic_action_regulation", 0.0) or 0.0)
    structure_action_uncertainty = float(ctx.get("structure_action_uncertainty", 0.0) or 0.0)
    learned_development_uncertainty = float(ctx.get("learned_development_uncertainty", 0.0) or 0.0)
    semantic_shift_pressure = float(ctx.get("semantic_shift_pressure", 0.0) or 0.0)
    transfer_bearing = float(ctx.get("transfer_bearing", 0.0) or 0.0)
    transfer_maturity_gap = float(ctx.get("transfer_maturity_gap", 0.0) or 0.0)
    fatigue_excess = float(ctx.get("fatigue_excess", 0.0) or 0.0)
    visual_action_uncertainty = float(ctx.get("visual_action_uncertainty", 0.0) or 0.0)
    variant_learning_pressure = float(ctx.get("variant_learning_pressure", 0.0) or 0.0)
    signal_quality = float(ctx.get("signal_quality", 0.0) or 0.0)
    processing_alignment = float(ctx.get("processing_alignment", 0.0) or 0.0)
    variant_bearing_memory = float(ctx.get("variant_bearing_memory", 0.0) or 0.0)
    decision_strength = float(ctx.get("decision_strength", 0.0) or 0.0)
    structure_quality = float(ctx.get("structure_quality", 0.0) or 0.0)
    structure_carrying_need = float(ctx.get("structure_carrying_need", 0.0) or 0.0)

    regulated_courage = max(
        0.0,
        min(
            1.0,
            (protective_courage * 0.30)
            + (load_bearing_capacity * 0.20)
            + (state_maturity * 0.12)
            + (decision_readiness * 0.10)
            + (felt_alignment * 0.08)
            + (experience_regulation * 0.08)
            + (areal_support * 0.08)
            + (processing_areal_support * 0.04)
            + (field_action_support * 0.08)
            - (field_perception_instability * 0.06),
        ),
    )

    courage_gap = max(
        0.0,
        min(
            1.0,
            max(0.0, expectation_pressure - regulated_courage),
        ),
    )

    action_inhibition = max(
        0.0,
        min(
            1.0,
            (felt_pressure * 0.16)
            + (decision_conflict * 0.12)
            + (processing_tension * 0.10)
            + (uncertainty_pressure * 0.10)
            + (aftereffect_pressure * 0.08)
            + (areal_conflict_pressure * 0.12)
            + (processing_areal_tension * 0.06)
            + (field_observation_need * 0.10)
            + (field_replan_pressure * 0.08)
            + (courage_gap * 0.18)
            + (max(0.0, 1.0 - protective_width_regulation) * 0.06)
            + (max(0.0, 1.0 - load_bearing_capacity) * 0.04),
        ),
    )
    if symbolic_regulation > 0.0:
        action_inhibition = max(0.0, min(1.0, action_inhibition - symbolic_action_regulation))
    if structure_action_uncertainty > 0.0:
        action_inhibition = max(
            0.0,
            min(1.0, action_inhibition + (structure_action_uncertainty * 0.16)),
        )
    if learned_development_uncertainty > 0.0:
        action_inhibition = max(
            0.0,
            min(1.0, action_inhibition + (learned_development_uncertainty * 0.14)),
        )
    if semantic_shift_pressure > 0.0:
        transfer_gap = max(0.0, 1.0 - transfer_bearing)
        action_inhibition = max(
            0.0,
            min(1.0, action_inhibition + (semantic_shift_pressure * transfer_gap * 0.11)),
        )
    if transfer_maturity_gap > 0.0:
        action_inhibition = max(
            0.0,
            min(1.0, action_inhibition + (transfer_maturity_gap * 0.090)),
        )
    if fatigue_excess > 0.0:
        action_inhibition = max(
            0.0,
            min(1.0, action_inhibition + (fatigue_excess * 0.045)),
        )
    if visual_action_uncertainty > 0.0:
        action_inhibition = max(
            0.0,
            min(1.0, action_inhibition + (visual_action_uncertainty * 0.090)),
        )
    if variant_learning_pressure > 0.0:
        action_inhibition = max(
            0.0,
            min(1.0, action_inhibition + (variant_learning_pressure * 0.075)),
        )

    action_clearance = max(
        0.0,
        min(
            1.0,
            (regulated_courage * 0.30)
            + (decision_readiness * 0.16)
            + (state_maturity * 0.14)
            + (signal_quality * 0.10)
            + (processing_alignment * 0.10)
            + (areal_support * 0.10)
            + (processing_areal_support * 0.10)
            + (field_action_support * 0.10)
            - (field_perception_instability * 0.08),
        ),
    )
    if structure_action_uncertainty > 0.0:
        action_clearance = max(
            0.0,
            min(1.0, action_clearance - (structure_action_uncertainty * 0.10)),
        )
    if learned_development_uncertainty > 0.0:
        action_clearance = max(
            0.0,
            min(1.0, action_clearance - (learned_development_uncertainty * 0.095)),
        )
    if semantic_shift_pressure > 0.0:
        transfer_gap = max(0.0, 1.0 - transfer_bearing)
        action_clearance = max(
            0.0,
            min(1.0, action_clearance - (semantic_shift_pressure * transfer_gap * 0.075)),
        )
    if transfer_maturity_gap > 0.0:
        action_clearance = max(
            0.0,
            min(1.0, action_clearance - (transfer_maturity_gap * 0.065)),
        )
    if fatigue_excess > 0.0:
        action_clearance = max(
            0.0,
            min(1.0, action_clearance - (fatigue_excess * 0.035)),
        )
    if visual_action_uncertainty > 0.0:
        action_clearance = max(
            0.0,
            min(1.0, action_clearance - (visual_action_uncertainty * 0.055)),
        )
    if variant_learning_pressure > 0.0:
        action_clearance = max(
            0.0,
            min(1.0, action_clearance - (variant_learning_pressure * 0.040) + (variant_bearing_memory * 0.020)),
        )
    plan_pressure = max(
        0.0,
        min(
            1.0,
            (decision_strength * 0.26)
            + (regulated_courage * 0.18)
            + (action_clearance * 0.10)
            + (max(0.0, structure_quality - 0.40) * 0.16)
            + (signal_quality * 0.10)
            + (decision_readiness * 0.10)
            + (state_maturity * 0.10),
        ),
    )
    act_watch_readiness = max(
        0.0,
        min(
            1.0,
            (plan_pressure * 0.32)
            + (structure_carrying_need * 0.26)
            + (learned_development_uncertainty * 0.14)
            + (semantic_shift_pressure * 0.10)
            + (transfer_maturity_gap * 0.10)
            + (visual_action_uncertainty * 0.12)
            + (variant_learning_pressure * 0.10)
            + (max(0.0, action_inhibition - action_clearance) * 0.08),
        ),
    )

    return {
        "regulated_courage": float(regulated_courage),
        "courage_gap": float(courage_gap),
        "action_inhibition": float(action_inhibition),
        "action_clearance": float(action_clearance),
        "plan_pressure": float(plan_pressure),
        "act_watch_readiness": float(act_watch_readiness),
    }


def _build_mcm_axis_state(context=None):
    ctx = dict(context or {})

    field_perception_clarity = float(ctx.get("field_perception_clarity", 0.0) or 0.0)
    interpretation_quality = float(ctx.get("interpretation_quality", 0.0) or 0.0)
    memory_orientation = float(ctx.get("memory_orientation", 0.0) or 0.0)
    processing_alignment = float(ctx.get("processing_alignment", 0.0) or 0.0)
    known_form_support = float(ctx.get("known_form_support", 0.0) or 0.0)
    route_familiarity = float(ctx.get("route_familiarity", 0.0) or 0.0)
    orientation_gap = float(ctx.get("orientation_gap", 0.0) or 0.0)
    plan_pressure = float(ctx.get("plan_pressure", 0.0) or 0.0)
    action_clearance = float(ctx.get("action_clearance", 0.0) or 0.0)
    action_inhibition = float(ctx.get("action_inhibition", 0.0) or 0.0)
    form_symbol_action_trust = float(ctx.get("form_symbol_action_trust", 0.0) or 0.0)
    trust_transfer_support = float(ctx.get("trust_transfer_support", 0.0) or 0.0)
    previous_constructive_stimulation = float(ctx.get("previous_constructive_stimulation", 0.0) or 0.0)
    previous_packet_process_reward = float(ctx.get("previous_packet_process_reward", 0.0) or 0.0)
    decision_strength = float(ctx.get("decision_strength", 0.0) or 0.0)
    field_bearing_support = float(ctx.get("field_bearing_support", ctx.get("field_action_support", 0.0)) or 0.0)
    action_readiness_from_field = float(ctx.get("action_readiness_from_field", ctx.get("field_action_support", field_bearing_support)) or 0.0)
    field_action_support = action_readiness_from_field
    field_perception_pressure = float(ctx.get("field_perception_pressure", 0.0) or 0.0)
    field_perception_strain = float(ctx.get("field_perception_strain", 0.0) or 0.0)
    mcm_reflective_bearing = float(ctx.get("mcm_reflective_bearing", 0.0) or 0.0)
    mcm_reflective_pressure = float(ctx.get("mcm_reflective_pressure", 0.0) or 0.0)
    mcm_reflective_coupling_load = float(ctx.get("mcm_reflective_coupling_load", 0.0) or 0.0)
    mcm_reflective_tension = float(ctx.get("mcm_reflective_tension", 0.0) or 0.0)
    processing_load = float(ctx.get("processing_load", 0.0) or 0.0)
    visual_blind_action_load = float(ctx.get("visual_blind_action_load", 0.0) or 0.0)
    structure_action_uncertainty = float(ctx.get("structure_action_uncertainty", 0.0) or 0.0)
    regulated_courage = float(ctx.get("regulated_courage", 0.0) or 0.0)
    structure_action_bearing = float(ctx.get("structure_action_bearing", 0.0) or 0.0)
    field_observation_need = float(ctx.get("field_observation_need", 0.0) or 0.0)
    act_watch_readiness = float(ctx.get("act_watch_readiness", 0.0) or 0.0)

    pre_conscious_inner_outer_alignment = _clip01(
        (field_perception_clarity * 0.24)
        + (interpretation_quality * 0.22)
        + (memory_orientation * 0.16)
        + (processing_alignment * 0.14)
        + (known_form_support * 0.10)
        + (route_familiarity * 0.08)
        + (max(0.0, 1.0 - orientation_gap) * 0.06)
    )
    positive_expansion_pressure = _clip01(
        (plan_pressure * 0.22)
        + (max(0.0, action_clearance - action_inhibition) * 0.16)
        + (form_symbol_action_trust * 0.12)
        + (trust_transfer_support * 0.10)
        + (previous_constructive_stimulation * 0.10)
        + (previous_packet_process_reward * 0.08)
        + (max(0.0, decision_strength - 1.0) * 0.10)
        + (field_action_support * 0.08)
        + (mcm_reflective_bearing * 0.08)
    )
    negative_contraction_pressure = _clip01(
        (field_perception_pressure * 0.18)
        + (field_perception_strain * 0.16)
        + (mcm_reflective_pressure * 0.10)
        + (action_inhibition * 0.15)
        + (orientation_gap * 0.13)
        + (processing_load * 0.12)
        + (visual_blind_action_load * 0.10)
        + (structure_action_uncertainty * 0.10)
        + (mcm_reflective_coupling_load * max(0.0, 0.34 - mcm_reflective_bearing) * 0.08)
        + (max(0.0, 0.42 - regulated_courage) * 0.06)
    )
    positive_overextension = _clip01(
        positive_expansion_pressure
        * (
            0.22
            + (max(0.0, 0.48 - field_action_support) * 0.24)
            + (max(0.0, 0.48 - structure_action_bearing) * 0.20)
            + (max(0.0, 0.38 - mcm_reflective_bearing) * 0.12)
            + (max(0.0, 0.42 - pre_conscious_inner_outer_alignment) * 0.16)
            + (max(0.0, action_clearance - action_inhibition) * 0.12)
        )
    )
    positive_return_pressure = _clip01(
        (positive_overextension * 0.46)
        + (positive_expansion_pressure * max(0.0, 0.44 - field_action_support) * 0.20)
        + (positive_expansion_pressure * max(0.0, 0.42 - structure_action_bearing) * 0.16)
        + (positive_expansion_pressure * max(0.0, 0.34 - mcm_reflective_bearing) * 0.10)
        + (mcm_reflective_tension * max(0.0, 0.30 - mcm_reflective_bearing) * 0.08)
        + (positive_expansion_pressure * max(0.0, 0.36 - pre_conscious_inner_outer_alignment) * 0.12)
    )
    mcm_axis_displacement = max(-1.0, min(1.0, positive_expansion_pressure - negative_contraction_pressure))
    mcm_axis_field_position = max(-3.0, min(3.0, mcm_axis_displacement * 3.0))
    mcm_axis_tension = _clip01(max(positive_expansion_pressure, negative_contraction_pressure))
    mcm_axis_label_pressures = {
        "++": _clip01(max(0.0, mcm_axis_displacement) * positive_expansion_pressure),
        "+": _clip01(max(0.0, mcm_axis_displacement) * (1.0 - abs(mcm_axis_displacement - 0.32))),
        "0": _clip01(1.0 - abs(mcm_axis_displacement) - (mcm_axis_tension * 0.18)),
        "-": _clip01(max(0.0, -mcm_axis_displacement) * (1.0 - abs(mcm_axis_displacement + 0.32))),
        "--": _clip01(max(0.0, -mcm_axis_displacement) * negative_contraction_pressure),
    }
    mcm_axis_state = max(mcm_axis_label_pressures, key=mcm_axis_label_pressures.get)
    if positive_return_pressure > 0.0:
        field_observation_need = _clip01(field_observation_need + (positive_return_pressure * 0.055))
        act_watch_readiness = _clip01(act_watch_readiness + (positive_return_pressure * 0.050))
        action_inhibition = _clip01(action_inhibition + (positive_return_pressure * 0.040))
        action_clearance = _clip01(action_clearance - (positive_return_pressure * 0.030))

    return {
        "pre_conscious_inner_outer_alignment": float(pre_conscious_inner_outer_alignment),
        "positive_expansion_pressure": float(positive_expansion_pressure),
        "negative_contraction_pressure": float(negative_contraction_pressure),
        "positive_overextension": float(positive_overextension),
        "positive_return_pressure": float(positive_return_pressure),
        "mcm_axis_displacement": float(mcm_axis_displacement),
        "mcm_axis_field_position": float(mcm_axis_field_position),
        "mcm_axis_tension": float(mcm_axis_tension),
        "mcm_axis_state": str(mcm_axis_state),
        "mcm_reflective_bearing": float(mcm_reflective_bearing),
        "mcm_reflective_pressure": float(mcm_reflective_pressure),
        "mcm_reflective_coupling_load": float(mcm_reflective_coupling_load),
        "mcm_reflective_tension": float(mcm_reflective_tension),
        "field_observation_need": float(field_observation_need),
        "act_watch_readiness": float(act_watch_readiness),
        "action_inhibition": float(action_inhibition),
        "action_clearance": float(action_clearance),
    }


def _build_zero_point_orientation_state(context=None):
    ctx = dict(context or {})

    orientation_gap = float(ctx.get("orientation_gap", 0.0) or 0.0)
    action_inhibition = float(ctx.get("action_inhibition", 0.0) or 0.0)
    action_clearance = float(ctx.get("action_clearance", 0.0) or 0.0)
    symbolic_regulation = float(ctx.get("symbolic_regulation", 0.0) or 0.0)
    symbolic_inner_regulation = float(ctx.get("symbolic_inner_regulation", 0.0) or 0.0)
    blind_thinking_load = float(ctx.get("blind_thinking_load", 0.0) or 0.0)
    processing_load = float(ctx.get("processing_load", 0.0) or 0.0)
    memory_orientation = float(ctx.get("memory_orientation", 0.0) or 0.0)
    memory_support = float(ctx.get("memory_support", 0.0) or 0.0)
    decision_strength = float(ctx.get("decision_strength", 0.0) or 0.0)
    positive_return_pressure = float(ctx.get("positive_return_pressure", 0.0) or 0.0)
    field_bearing_support = float(ctx.get("field_bearing_support", ctx.get("field_action_support", 0.0)) or 0.0)
    action_readiness_from_field = float(ctx.get("action_readiness_from_field", ctx.get("field_action_support", field_bearing_support)) or 0.0)
    field_action_support = action_readiness_from_field
    structure_action_bearing = float(ctx.get("structure_action_bearing", 0.0) or 0.0)
    structure_orientation_gap = float(ctx.get("structure_orientation_gap", 0.0) or 0.0)
    structure_quality = float(ctx.get("structure_quality", 0.0) or 0.0)
    context_confidence = float(ctx.get("context_confidence", 0.0) or 0.0)
    memory_effect_on_phase = str(ctx.get("memory_effect_on_phase", "neutral_match") or "neutral_match")
    context_cluster_negative_evidence = str(ctx.get("context_cluster_negative_evidence", "-") or "-")

    orientation_gap = max(
        0.0,
        min(
            1.0,
            orientation_gap
            + (action_inhibition * 0.12)
            + (max(0.0, 0.44 - action_clearance) * 0.10)
            - (max(0.0, action_clearance - action_inhibition) * 0.06),
        ),
    )
    if symbolic_regulation > 0.0:
        orientation_gap = max(0.0, min(1.0, orientation_gap - (symbolic_inner_regulation * 0.055)))
    blind_thinking_load = max(
        0.0,
        min(
            1.0,
            blind_thinking_load
            + (action_inhibition * 0.10)
            + (max(0.0, processing_load - 0.48) * 0.12)
            - (memory_orientation * 0.08),
        ),
    )
    if symbolic_regulation > 0.0:
        blind_thinking_load = max(0.0, min(1.0, blind_thinking_load - (symbolic_inner_regulation * 0.075)))
    memory_continuity_pressure = _clip01(
        (memory_support * 0.24)
        + (memory_orientation * 0.20)
        + (decision_strength * 0.16)
        + (structure_quality * 0.14)
        + (context_confidence * 0.12)
        + (field_action_support * 0.08)
        + (structure_action_bearing * 0.06)
    )
    zero_point_pressure = _clip01(
        (blind_thinking_load * 0.28)
        + (orientation_gap * 0.24)
        + ((1.0 - memory_support) * 0.12)
        + ((1.0 - memory_orientation) * 0.12)
        + ((1.0 - min(1.0, decision_strength)) * 0.08)
    )
    positive_zero_point_pressure = _clip01(
        (positive_return_pressure * 0.24)
        + ((1.0 - field_action_support) * 0.14)
        + ((1.0 - structure_action_bearing) * 0.12)
        + ((1.0 - min(1.0, decision_strength)) * 0.08)
    )
    structure_orientation_pressure = _clip01(
        (structure_orientation_gap * 0.24)
        + ((1.0 - structure_quality) * 0.14)
        + ((1.0 - context_confidence) * 0.12)
        + ((1.0 - memory_support) * 0.10)
        + ((1.0 - memory_orientation) * 0.10)
        + ((1.0 - min(1.0, decision_strength)) * 0.06)
        + ((1.0 if memory_effect_on_phase in ("inhibit", "neutral_match", "no_match") else 0.0) * 0.08)
    )
    zero_point_regulation = bool(zero_point_pressure > memory_continuity_pressure)
    positive_zero_point_regulation = bool(positive_zero_point_pressure > memory_continuity_pressure)
    structure_orientation_guard = bool(structure_orientation_pressure > memory_continuity_pressure)
    if context_cluster_negative_evidence == "low_hit_caution":
        caution_orientation_pressure = _clip01(
            (structure_orientation_pressure * 0.70)
            + ((1.0 - structure_quality) * 0.12)
            + ((1.0 - memory_support) * 0.10)
            + ((1.0 - min(1.0, decision_strength)) * 0.08)
        )
        structure_orientation_guard = bool(max(structure_orientation_pressure, caution_orientation_pressure) > memory_continuity_pressure)

    return {
        "orientation_gap": float(orientation_gap),
        "blind_thinking_load": float(blind_thinking_load),
        "memory_continuity_pressure": float(memory_continuity_pressure),
        "zero_point_pressure": float(zero_point_pressure),
        "positive_zero_point_pressure": float(positive_zero_point_pressure),
        "structure_orientation_pressure": float(structure_orientation_pressure),
        "zero_point_regulation": bool(zero_point_regulation),
        "positive_zero_point_regulation": bool(positive_zero_point_regulation),
        "structure_orientation_guard": bool(structure_orientation_guard),
    }


def _build_open_hypothesis_feedback_state(context=None):
    ctx = dict(context or {})
    outcome_decomposition = dict(ctx.get("outcome_decomposition", {}) or {})
    outcome_trace_coupling = _clip01(ctx.get("outcome_trace_coupling", 0.38))

    def _outcome_clip(key, default=0.0):
        try:
            value = float(outcome_decomposition.get(key, default) or default)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(0.0, min(1.0, float(value))) * outcome_trace_coupling

    field_bearing_support = float(ctx.get("field_bearing_support", ctx.get("field_action_support", 0.0)) or 0.0)
    action_readiness_from_field = float(ctx.get("action_readiness_from_field", ctx.get("field_action_support", field_bearing_support)) or 0.0)
    field_action_support = action_readiness_from_field
    structure_action_bearing = float(ctx.get("structure_action_bearing", 0.0) or 0.0)
    field_perception_clarity = float(ctx.get("field_perception_clarity", 0.0) or 0.0)
    decision_readiness = float(ctx.get("decision_readiness", 0.0) or 0.0)
    form_symbol_action_trust = float(ctx.get("form_symbol_action_trust", 0.0) or 0.0)
    structure_action_uncertainty = float(ctx.get("structure_action_uncertainty", 0.0) or 0.0)
    state_maturity = float(ctx.get("state_maturity", 0.0) or 0.0)
    memory_orientation = float(ctx.get("memory_orientation", 0.0) or 0.0)
    action_inhibition = float(ctx.get("action_inhibition", 0.0) or 0.0)
    experience_regulation = float(ctx.get("experience_regulation", 0.0) or 0.0)
    decision_strength = float(ctx.get("decision_strength", 0.0) or 0.0)
    bot = ctx.get("bot")
    previous_seed = dict(getattr(bot, "mcm_thought_seed_state", {}) or {}) if bot is not None else {}
    attempt_feedback = {}
    stats_obj = getattr(bot, "stats", None) if bot is not None else None
    if stats_obj is not None and hasattr(stats_obj, "get_attempt_feedback"):
        try:
            attempt_feedback = dict(stats_obj.get_attempt_feedback() or {})
        except Exception:
            attempt_feedback = {}
    declined_hypothesis_confirmation_without_action = _clip01(
        attempt_feedback.get("declined_hypothesis_confirmation_without_action", 0.0)
    )
    declined_hypothesis_rejection_without_action = _clip01(
        attempt_feedback.get("declined_hypothesis_rejection_without_action", 0.0)
    )
    declined_hypothesis_maturity = _clip01(
        attempt_feedback.get("declined_hypothesis_maturity", 0.0)
    )
    declined_hypothesis_balance_gap = abs(
        declined_hypothesis_confirmation_without_action
        - declined_hypothesis_rejection_without_action
    )
    declined_hypothesis_protective_trace = _clip01(
        declined_hypothesis_rejection_without_action
        * declined_hypothesis_maturity
    )
    declined_hypothesis_missed_trace = _clip01(
        declined_hypothesis_confirmation_without_action
        * declined_hypothesis_maturity
    )
    declined_hypothesis_mixed_trace = _clip01(
        min(declined_hypothesis_confirmation_without_action, declined_hypothesis_rejection_without_action)
        * declined_hypothesis_maturity
        * (1.0 - declined_hypothesis_balance_gap)
    )
    declined_hypothesis_protective_edge = _clip01(
        max(
            0.0,
            declined_hypothesis_rejection_without_action
            - declined_hypothesis_confirmation_without_action,
        )
        * declined_hypothesis_maturity
    )
    declined_hypothesis_missed_edge = _clip01(
        max(
            0.0,
            declined_hypothesis_confirmation_without_action
            - declined_hypothesis_rejection_without_action,
        )
        * declined_hypothesis_maturity
    )
    decision_key = str(ctx.get("decision", ctx.get("proposed_decision", "WAIT")) or "WAIT").upper().strip()
    directional_hypothesis_confirmation = 0.0
    directional_hypothesis_rejection = 0.0
    directional_hypothesis_maturity = 0.0
    if decision_key in ("LONG", "SHORT"):
        side_key = decision_key.lower()
        directional_hypothesis_confirmation = _clip01(
            attempt_feedback.get(f"declined_{side_key}_hypothesis_confirmation", 0.0)
        )
        directional_hypothesis_rejection = _clip01(
            attempt_feedback.get(f"declined_{side_key}_hypothesis_rejection", 0.0)
        )
        directional_hypothesis_maturity = _clip01(
            attempt_feedback.get(f"declined_{side_key}_hypothesis_maturity", 0.0)
        )
    directional_hypothesis_missed_edge = _clip01(
        max(0.0, directional_hypothesis_confirmation - directional_hypothesis_rejection)
        * directional_hypothesis_maturity
    )
    directional_hypothesis_protective_edge = _clip01(
        max(0.0, directional_hypothesis_rejection - directional_hypothesis_confirmation)
        * directional_hypothesis_maturity
    )

    def _seed_or_ctx(key, default=0.0):
        if key in ctx:
            return _clip01(ctx.get(key, default))
        return _clip01(previous_seed.get(key, default))

    form_mcm_family_recurrence = _seed_or_ctx("form_mcm_family_recurrence")
    form_mcm_family_maturity = _seed_or_ctx("form_mcm_family_maturity")
    form_mcm_family_trust = _seed_or_ctx("form_mcm_family_trust")
    form_mcm_family_caution = _seed_or_ctx("form_mcm_family_caution")
    form_mcm_family_reorganization_need = _seed_or_ctx("form_mcm_family_reorganization_need")

    previous_open_hypothesis_learning_state = str(outcome_decomposition.get("open_hypothesis_learning_state", "-") or "-").strip().lower() or "-"
    previous_open_hypothesis_reorganization_posture = str(outcome_decomposition.get("open_hypothesis_reorganization_posture", "-") or "-").strip().lower() or "-"
    carried_trace = outcome_trace_coupling if previous_open_hypothesis_learning_state == "open_hypothesis_carried" else 0.0
    burdened_trace = outcome_trace_coupling if previous_open_hypothesis_learning_state == "open_hypothesis_burdened" else 0.0
    reorganizing_trace = outcome_trace_coupling if previous_open_hypothesis_learning_state == "open_hypothesis_reorganizing" else 0.0
    previous_open_hypothesis_consequence_score = _outcome_clip("open_hypothesis_consequence_score")
    previous_open_hypothesis_burden_score = _outcome_clip("open_hypothesis_burden_score")
    previous_open_hypothesis_reorganization_score = _outcome_clip("open_hypothesis_reorganization_score")
    previous_open_hypothesis_replay_need = _outcome_clip("open_hypothesis_replay_need")
    previous_open_hypothesis_distance_need = _outcome_clip("open_hypothesis_distance_need")
    previous_open_hypothesis_reinterpretation_need = _outcome_clip("open_hypothesis_reinterpretation_need")
    open_hypothesis_has_trace = bool(
        previous_open_hypothesis_learning_state
        in ("open_hypothesis_carried", "open_hypothesis_burdened", "open_hypothesis_reorganizing")
        or max(
            previous_open_hypothesis_consequence_score,
            previous_open_hypothesis_burden_score,
            previous_open_hypothesis_reorganization_score,
            previous_open_hypothesis_replay_need,
            previous_open_hypothesis_distance_need,
            previous_open_hypothesis_reinterpretation_need,
        )
        > 0.01
    )
    open_hypothesis_trace_strength = _clip01(
        ((0.24 * outcome_trace_coupling) if open_hypothesis_has_trace else 0.0)
        + (previous_open_hypothesis_consequence_score * 0.26)
        + (previous_open_hypothesis_burden_score * 0.20)
        + (previous_open_hypothesis_reorganization_score * 0.18)
        + (previous_open_hypothesis_replay_need * 0.06)
        + (previous_open_hypothesis_distance_need * 0.05)
        + (previous_open_hypothesis_reinterpretation_need * 0.05)
    )
    open_hypothesis_bearing_echo = _clip01(
        open_hypothesis_trace_strength
        * (
            (carried_trace * 0.32)
            + (previous_open_hypothesis_consequence_score * 0.38)
            + (max(0.0, 1.0 - previous_open_hypothesis_burden_score) * 0.10)
            + (max(0.0, 1.0 - previous_open_hypothesis_reorganization_score) * 0.08)
        )
    )
    hypothesis_trust = _clip01(
        (open_hypothesis_bearing_echo * 0.45)
        + (previous_open_hypothesis_consequence_score * 0.36)
        + (carried_trace * 0.20)
        + (form_mcm_family_trust * 0.10)
        + (form_mcm_family_maturity * 0.05)
        + (declined_hypothesis_missed_trace * 0.06)
        + (declined_hypothesis_missed_edge * 0.08)
        + (directional_hypothesis_missed_edge * 0.10)
        - (previous_open_hypothesis_burden_score * 0.14)
        - (previous_open_hypothesis_reorganization_score * 0.10)
        - (form_mcm_family_caution * 0.05)
        - (declined_hypothesis_protective_edge * 0.04)
        - (directional_hypothesis_protective_edge * 0.06)
    )
    hypothesis_caution = _clip01(
        open_hypothesis_trace_strength
        * (
            (burdened_trace * 0.24)
            + (previous_open_hypothesis_burden_score * 0.36)
            + (previous_open_hypothesis_distance_need * 0.16)
            + (max(0.0, previous_open_hypothesis_burden_score - previous_open_hypothesis_consequence_score) * 0.18)
        )
        + (form_mcm_family_caution * 0.10)
        + (form_mcm_family_reorganization_need * 0.04)
        + (declined_hypothesis_protective_trace * 0.08)
        + (declined_hypothesis_protective_edge * 0.10)
        + (directional_hypothesis_protective_edge * 0.12)
        - (form_mcm_family_trust * 0.04)
        - (declined_hypothesis_missed_edge * 0.04)
        - (directional_hypothesis_missed_edge * 0.05)
    )
    hypothesis_reorganization_weight = _clip01(
        open_hypothesis_trace_strength
        * (
            (reorganizing_trace * 0.26)
            + (previous_open_hypothesis_reorganization_score * 0.34)
            + (previous_open_hypothesis_replay_need * 0.16)
            + (previous_open_hypothesis_reinterpretation_need * 0.16)
            + (max(0.0, previous_open_hypothesis_burden_score - previous_open_hypothesis_consequence_score) * 0.10)
        )
        + (form_mcm_family_reorganization_need * 0.08)
        + (form_mcm_family_caution * 0.04)
        + (declined_hypothesis_mixed_trace * 0.08)
        + ((declined_hypothesis_protective_trace + declined_hypothesis_missed_trace) * 0.025)
        + ((directional_hypothesis_protective_edge + directional_hypothesis_missed_edge) * 0.05)
    )
    open_hypothesis_confirmation_weight = _clip01(
        (hypothesis_trust * 0.32)
        + (open_hypothesis_bearing_echo * 0.24)
        + (previous_open_hypothesis_consequence_score * 0.20)
        + (carried_trace * 0.12)
        + (form_mcm_family_trust * 0.06)
        + (form_mcm_family_recurrence * form_mcm_family_maturity * 0.04)
        + (declined_hypothesis_missed_trace * 0.05)
        + (declined_hypothesis_missed_edge * 0.08)
        + (directional_hypothesis_missed_edge * 0.10)
        + (max(0.0, previous_open_hypothesis_replay_need - previous_open_hypothesis_distance_need) * 0.06)
        - (previous_open_hypothesis_burden_score * 0.08)
        - (previous_open_hypothesis_reorganization_score * 0.06)
        - (form_mcm_family_caution * 0.03)
        - (declined_hypothesis_protective_edge * 0.04)
        - (directional_hypothesis_protective_edge * 0.05)
    )
    open_hypothesis_learning_charge = _clip01(
        (hypothesis_reorganization_weight * 0.30)
        + (previous_open_hypothesis_reorganization_score * 0.24)
        + (previous_open_hypothesis_reinterpretation_need * 0.18)
        + (previous_open_hypothesis_distance_need * 0.12)
        + (max(0.0, previous_open_hypothesis_burden_score - previous_open_hypothesis_consequence_score) * 0.12)
        + (reorganizing_trace * 0.08)
        + (form_mcm_family_reorganization_need * 0.06)
        + (form_mcm_family_caution * 0.035)
        + (declined_hypothesis_mixed_trace * 0.08)
        + (declined_hypothesis_protective_edge * 0.04)
        + (declined_hypothesis_missed_edge * 0.04)
        + ((directional_hypothesis_protective_edge + directional_hypothesis_missed_edge) * 0.05)
        - (open_hypothesis_confirmation_weight * 0.10)
        - (form_mcm_family_trust * 0.025)
    )
    open_hypothesis_reality_bearing = _clip01(
        (open_hypothesis_confirmation_weight * 0.34)
        + (field_bearing_support * 0.10)
        + (action_readiness_from_field * 0.08)
        + (structure_action_bearing * 0.18)
        + (field_perception_clarity * 0.12)
        + (decision_readiness * 0.10)
        + (form_mcm_family_trust * 0.04)
        + (declined_hypothesis_missed_edge * 0.055)
        + (directional_hypothesis_missed_edge * 0.065)
        - (hypothesis_caution * 0.12)
        - (open_hypothesis_learning_charge * 0.14)
        - (previous_open_hypothesis_burden_score * 0.08)
        - (form_mcm_family_caution * 0.035)
        - (form_mcm_family_reorganization_need * 0.025)
        - (declined_hypothesis_protective_edge * 0.060)
        - (directional_hypothesis_protective_edge * 0.075)
    )
    open_hypothesis_reality_fit = float(open_hypothesis_reality_bearing)
    open_hypothesis_reality_permission = float(open_hypothesis_reality_bearing)
    open_hypothesis_action_permission = float(open_hypothesis_reality_bearing)
    open_hypothesis_reality_check_need = _clip01(
        (open_hypothesis_learning_charge * 0.34)
        + (hypothesis_caution * 0.22)
        + (max(0.0, previous_open_hypothesis_reorganization_score - previous_open_hypothesis_consequence_score) * 0.18)
        + (max(0.0, 0.42 - field_perception_clarity) * 0.10)
        + (max(0.0, 0.36 - memory_orientation) * 0.08)
        + (max(0.0, 0.40 - open_hypothesis_reality_bearing) * 0.08)
        + (declined_hypothesis_mixed_trace * 0.06)
        + (declined_hypothesis_missed_edge * 0.06)
        + (declined_hypothesis_protective_edge * 0.04)
        + (directional_hypothesis_missed_edge * 0.06)
        + (directional_hypothesis_protective_edge * 0.04)
    )
    hypothesis_weight = _clip01(
        0.50
        + (hypothesis_trust * 0.24)
        + (open_hypothesis_confirmation_weight * 0.12)
        - (hypothesis_caution * 0.18)
        - (open_hypothesis_learning_charge * 0.12)
    )
    action_weight = _clip01(
        0.50
        + (hypothesis_trust * 0.12)
        + (open_hypothesis_reality_bearing * 0.16)
        + (form_symbol_action_trust * 0.08)
        + (action_readiness_from_field * 0.08)
        + (structure_action_bearing * 0.06)
        - (hypothesis_caution * 0.16)
        - (open_hypothesis_learning_charge * 0.12)
        - (structure_action_uncertainty * 0.06)
    )
    decision_weight = _clip01(
        0.42
        + (action_weight * 0.24)
        + (decision_readiness * 0.16)
        + (state_maturity * 0.12)
        + (memory_orientation * 0.08)
        + (field_perception_clarity * 0.08)
        - (action_inhibition * 0.08)
    )
    open_hypothesis_reifung_pressure = _clip01(
        (hypothesis_caution * 0.24)
        + (open_hypothesis_learning_charge * 0.30)
        + (previous_open_hypothesis_replay_need * 0.05)
        + (previous_open_hypothesis_distance_need * 0.05)
        + (previous_open_hypothesis_reinterpretation_need * 0.05)
        + (declined_hypothesis_mixed_trace * 0.06)
        + (declined_hypothesis_protective_edge * 0.04)
        + ((directional_hypothesis_protective_edge + directional_hypothesis_missed_edge) * 0.04)
        - (open_hypothesis_confirmation_weight * 0.18)
    )
    open_hypothesis_reflection_pull = _clip01(
        (open_hypothesis_reifung_pressure * 0.26)
        + (open_hypothesis_learning_charge * 0.28)
        + (previous_open_hypothesis_replay_need * 0.20)
        + (previous_open_hypothesis_distance_need * 0.18)
        + (previous_open_hypothesis_reinterpretation_need * 0.16)
        + (declined_hypothesis_mixed_trace * 0.06)
        + (declined_hypothesis_missed_edge * 0.04)
        + ((directional_hypothesis_protective_edge + directional_hypothesis_missed_edge) * 0.04)
        + (max(0.0, 0.42 - field_perception_clarity) * 0.06)
        + (max(0.0, 0.34 - memory_orientation) * 0.06)
        + (max(0.0, 0.40 - experience_regulation) * 0.05)
    )
    open_hypothesis_motor_tension = _clip01(
        (hypothesis_caution * 0.22)
        + (open_hypothesis_reifung_pressure * 0.12)
        + (structure_action_uncertainty * 0.18)
        + (max(0.0, decision_strength - 1.0) * 0.10)
        + (max(0.0, 0.46 - action_readiness_from_field) * 0.12)
        + (declined_hypothesis_protective_edge * 0.05)
        + (directional_hypothesis_protective_edge * 0.06)
        - (open_hypothesis_confirmation_weight * 0.18)
        - (open_hypothesis_learning_charge * 0.08)
        - (declined_hypothesis_missed_edge * 0.025)
        - (directional_hypothesis_missed_edge * 0.030)
    )
    open_hypothesis_action_tension = float(open_hypothesis_motor_tension)
    open_hypothesis_reifung_pressures = {
        "open_hypothesis_carried_memory": _clip01((open_hypothesis_confirmation_weight * 0.54) + (hypothesis_trust * 0.24) + (open_hypothesis_learning_charge * 0.10)),
        "open_hypothesis_burden_memory": _clip01((hypothesis_caution * 0.54) + ((1.0 - hypothesis_trust) * 0.24) + (open_hypothesis_motor_tension * 0.12)),
        "open_hypothesis_reorganizing_memory": _clip01((open_hypothesis_learning_charge * 0.46) + (previous_open_hypothesis_reinterpretation_need * 0.22) + (open_hypothesis_reifung_pressure * 0.16)),
        "open_hypothesis_neutral_memory": _clip01((1.0 - max(open_hypothesis_confirmation_weight, hypothesis_caution, open_hypothesis_learning_charge)) * 0.40),
    }
    open_hypothesis_reifung_state = max(open_hypothesis_reifung_pressures, key=open_hypothesis_reifung_pressures.get)

    return {
        "previous_open_hypothesis_learning_state": str(previous_open_hypothesis_learning_state),
        "previous_open_hypothesis_reorganization_posture": str(previous_open_hypothesis_reorganization_posture),
        "previous_open_hypothesis_consequence_score": float(previous_open_hypothesis_consequence_score),
        "previous_open_hypothesis_burden_score": float(previous_open_hypothesis_burden_score),
        "previous_open_hypothesis_reorganization_score": float(previous_open_hypothesis_reorganization_score),
        "previous_open_hypothesis_replay_need": float(previous_open_hypothesis_replay_need),
        "previous_open_hypothesis_distance_need": float(previous_open_hypothesis_distance_need),
        "previous_open_hypothesis_reinterpretation_need": float(previous_open_hypothesis_reinterpretation_need),
        "outcome_trace_coupling": float(outcome_trace_coupling),
        "form_mcm_family_recurrence": float(form_mcm_family_recurrence),
        "form_mcm_family_maturity": float(form_mcm_family_maturity),
        "form_mcm_family_trust": float(form_mcm_family_trust),
        "form_mcm_family_caution": float(form_mcm_family_caution),
        "form_mcm_family_reorganization_need": float(form_mcm_family_reorganization_need),
        "declined_hypothesis_confirmation_without_action": float(declined_hypothesis_confirmation_without_action),
        "declined_hypothesis_rejection_without_action": float(declined_hypothesis_rejection_without_action),
        "declined_hypothesis_maturity": float(declined_hypothesis_maturity),
        "declined_hypothesis_protective_trace": float(declined_hypothesis_protective_trace),
        "declined_hypothesis_missed_trace": float(declined_hypothesis_missed_trace),
        "declined_hypothesis_mixed_trace": float(declined_hypothesis_mixed_trace),
        "declined_hypothesis_protective_edge": float(declined_hypothesis_protective_edge),
        "declined_hypothesis_missed_edge": float(declined_hypothesis_missed_edge),
        "directional_hypothesis_decision": str(decision_key),
        "directional_hypothesis_confirmation": float(directional_hypothesis_confirmation),
        "directional_hypothesis_rejection": float(directional_hypothesis_rejection),
        "directional_hypothesis_maturity": float(directional_hypothesis_maturity),
        "directional_hypothesis_protective_edge": float(directional_hypothesis_protective_edge),
        "directional_hypothesis_missed_edge": float(directional_hypothesis_missed_edge),
        "open_hypothesis_has_trace": bool(open_hypothesis_has_trace),
        "open_hypothesis_trace_strength": float(open_hypothesis_trace_strength),
        "open_hypothesis_bearing_echo": float(open_hypothesis_bearing_echo),
        "hypothesis_trust": float(hypothesis_trust),
        "hypothesis_caution": float(hypothesis_caution),
        "hypothesis_reorganization_weight": float(hypothesis_reorganization_weight),
        "open_hypothesis_confirmation_weight": float(open_hypothesis_confirmation_weight),
        "open_hypothesis_learning_charge": float(open_hypothesis_learning_charge),
        "open_hypothesis_reality_bearing": float(open_hypothesis_reality_bearing),
        "open_hypothesis_reality_fit": float(open_hypothesis_reality_fit),
        "open_hypothesis_reality_permission": float(open_hypothesis_reality_permission),
        "open_hypothesis_action_permission": float(open_hypothesis_action_permission),
        "open_hypothesis_reality_check_need": float(open_hypothesis_reality_check_need),
        "hypothesis_weight": float(hypothesis_weight),
        "action_weight": float(action_weight),
        "decision_weight": float(decision_weight),
        "open_hypothesis_reifung_pressure": float(open_hypothesis_reifung_pressure),
        "open_hypothesis_reflection_pull": float(open_hypothesis_reflection_pull),
        "open_hypothesis_action_tension": float(open_hypothesis_action_tension),
        "open_hypothesis_motor_tension": float(open_hypothesis_motor_tension),
        "open_hypothesis_reifung_state": str(open_hypothesis_reifung_state),
    }


def _build_pre_action_decision_state(context=None, config=None):
    ctx = dict(context or {})
    cfg = config

    pause_mode = bool(ctx.get("pause_mode", False))
    decision = str(ctx.get("decision", "WAIT") or "WAIT")
    reject_reason_default = str(ctx.get("reject_reason_default", "decision_wait") or "decision_wait")
    observation_mode = bool(ctx.get("observation_mode", False))
    decision_strength = float(ctx.get("decision_strength", 0.0) or 0.0)
    dominant_tension_cause = str(ctx.get("dominant_tension_cause", "-") or "-")
    dominant_tension_value = float(ctx.get("dominant_tension_value", 0.0) or 0.0)
    pre_action_observation_need = float(ctx.get("pre_action_observation_need", 0.0) or 0.0)
    observe_priority_threshold = float(ctx.get("observe_priority_threshold", 0.0) or 0.0)
    observe_priority = float(ctx.get("observe_priority", 0.0) or 0.0)
    uncertainty_score = float(ctx.get("uncertainty_score", 0.0) or 0.0)
    uncertainty_threshold = float(ctx.get("uncertainty_threshold", 0.0) or 0.0)
    processing_load = float(ctx.get("processing_load", 0.0) or 0.0)
    breakout_tension = float(ctx.get("breakout_tension", 0.0) or 0.0)
    processing_alignment = float(ctx.get("processing_alignment", 0.0) or 0.0)
    processing_areal_tension = float(ctx.get("processing_areal_tension", 0.0) or 0.0)
    processing_areal_support = float(ctx.get("processing_areal_support", 0.0) or 0.0)
    field_perception_label = str(ctx.get("field_perception_label", "-") or "-")
    field_observation_need = float(ctx.get("field_observation_need", 0.0) or 0.0)
    field_perception_fragmentation = float(ctx.get("field_perception_fragmentation", 0.0) or 0.0)
    field_perception_focus = float(ctx.get("field_perception_focus", 0.0) or 0.0)
    field_perception_pressure = float(ctx.get("field_perception_pressure", 0.0) or 0.0)
    field_perception_clarity = float(ctx.get("field_perception_clarity", 0.0) or 0.0)
    field_perception_strain = float(ctx.get("field_perception_strain", 0.0) or 0.0)
    field_perception_stability = float(ctx.get("field_perception_stability", 0.0) or 0.0)
    expectation_pressure = float(ctx.get("expectation_pressure", 0.0) or 0.0)
    courage_gap = float(ctx.get("courage_gap", 0.0) or 0.0)
    repetition_pressure = float(ctx.get("repetition_pressure", 0.0) or 0.0)
    action_inhibition = float(ctx.get("action_inhibition", 0.0) or 0.0)
    action_clearance = float(ctx.get("action_clearance", 0.0) or 0.0)
    regulated_courage = float(ctx.get("regulated_courage", 0.0) or 0.0)
    field_replan_pressure = float(ctx.get("field_replan_pressure", 0.0) or 0.0)
    field_bearing_support = float(ctx.get("field_bearing_support", ctx.get("field_action_support", 0.0)) or 0.0)
    action_readiness_from_field = float(ctx.get("action_readiness_from_field", ctx.get("field_action_support", field_bearing_support)) or 0.0)
    field_action_support = action_readiness_from_field
    open_hypothesis_reifung_state = str(ctx.get("open_hypothesis_reifung_state", "open_hypothesis_neutral_memory") or "open_hypothesis_neutral_memory")
    open_hypothesis_reality_check_need = float(ctx.get("open_hypothesis_reality_check_need", 0.0) or 0.0)
    open_hypothesis_reality_bearing = float(
        ctx.get(
            "open_hypothesis_reality_bearing",
            ctx.get("open_hypothesis_reality_fit", ctx.get("open_hypothesis_reality_permission", ctx.get("open_hypothesis_action_permission", 0.0))),
        )
        or 0.0
    )
    open_hypothesis_reality_fit = float(open_hypothesis_reality_bearing)
    open_hypothesis_reality_permission = float(open_hypothesis_reality_bearing)
    open_hypothesis_action_permission = float(open_hypothesis_reality_bearing)
    open_hypothesis_action_tension = float(ctx.get("open_hypothesis_action_tension", ctx.get("open_hypothesis_motor_tension", 0.0)) or 0.0)
    open_hypothesis_motor_tension = float(open_hypothesis_action_tension)
    action_weight = float(ctx.get("action_weight", 0.0) or 0.0)
    positive_zero_point_regulation = bool(ctx.get("positive_zero_point_regulation", False))
    positive_overextension = float(ctx.get("positive_overextension", 0.0) or 0.0)
    positive_return_pressure = float(ctx.get("positive_return_pressure", 0.0) or 0.0)
    areal_conflict_pressure = float(ctx.get("areal_conflict_pressure", 0.0) or 0.0)
    areal_support = float(ctx.get("areal_support", 0.0) or 0.0)
    decision_conflict = float(ctx.get("decision_conflict", 0.0) or 0.0)
    conflict_threshold = float(ctx.get("conflict_threshold", 0.0) or 0.0)
    rumination_depth = float(ctx.get("rumination_depth", 0.0) or 0.0)
    rumination_threshold = float(ctx.get("rumination_threshold", 0.0) or 0.0)
    felt_pressure = float(ctx.get("felt_pressure", 0.0) or 0.0)
    felt_conflict = float(ctx.get("felt_conflict", 0.0) or 0.0)
    state_maturity = float(ctx.get("state_maturity", 0.0) or 0.0)
    maturity_min = float(ctx.get("maturity_min", 0.0) or 0.0)
    decision_readiness = float(ctx.get("decision_readiness", 0.0) or 0.0)
    readiness_min = float(ctx.get("readiness_min", 0.0) or 0.0)
    signal_quality = float(ctx.get("signal_quality", 0.0) or 0.0)
    signal_quality_min = float(ctx.get("signal_quality_min", 0.0) or 0.0)
    processing_tension = float(ctx.get("processing_tension", 0.0) or 0.0)
    field_perception_instability = float(ctx.get("field_perception_instability", 0.0) or 0.0)
    market_balance = float(ctx.get("market_balance", 0.0) or 0.0)
    visual_coherence = float(ctx.get("visual_coherence", 0.0) or 0.0)
    visual_reflective_coherence = float(ctx.get("visual_reflective_coherence", visual_coherence) or 0.0)
    structure_quality = float(ctx.get("structure_quality", 0.0) or 0.0)
    plan_pressure = float(ctx.get("plan_pressure", 0.0) or 0.0)
    act_watch_readiness = float(ctx.get("act_watch_readiness", 0.0) or 0.0)
    structure_carrying_need = float(ctx.get("structure_carrying_need", 0.0) or 0.0)
    structure_action_uncertainty = float(ctx.get("structure_action_uncertainty", 0.0) or 0.0)
    learned_development_uncertainty = float(ctx.get("learned_development_uncertainty", 0.0) or 0.0)
    visual_action_uncertainty = float(ctx.get("visual_action_uncertainty", 0.0) or 0.0)
    variant_learning_pressure = float(ctx.get("variant_learning_pressure", 0.0) or 0.0)
    transfer_maturity_gap = float(ctx.get("transfer_maturity_gap", 0.0) or 0.0)
    form_symbol_reframe_binding = float(ctx.get("form_symbol_reframe_binding", 0.0) or 0.0)
    zero_point_regulation = bool(ctx.get("zero_point_regulation", False))
    structure_orientation_guard = bool(ctx.get("structure_orientation_guard", False))
    action_structure_min = float(ctx.get("action_structure_min", 0.0) or 0.0)
    memory_support = float(ctx.get("memory_support", 0.0) or 0.0)
    mid_support_min = float(ctx.get("mid_support_min", 0.0) or 0.0)
    low_strength_min = float(ctx.get("low_strength_min", 0.0) or 0.0)
    mid_strength_min = float(ctx.get("mid_strength_min", 0.0) or 0.0)
    structure_action_bearing = float(ctx.get("structure_action_bearing", 0.0) or 0.0)
    semantic_shift_pressure = float(ctx.get("semantic_shift_pressure", 0.0) or 0.0)
    transfer_bearing = float(ctx.get("transfer_bearing", 0.0) or 0.0)
    trust_transfer_support = float(ctx.get("trust_transfer_support", 0.0) or 0.0)
    form_symbol_action_trust = float(ctx.get("form_symbol_action_trust", 0.0) or 0.0)
    transfer_break_ready = bool(ctx.get("transfer_break_ready", False))
    transfer_recovery_need = float(ctx.get("transfer_recovery_need", 0.0) or 0.0)

    allow_observe = False
    allow_ruminate = False
    allow_plan = False
    allow_block = False
    rejection_reason = None
    pre_action_phase = "hold"
    pre_action_pressure_trace = {
        "observe_pressure": 0.0,
        "replan_pressure": 0.0,
        "hold_pressure": 0.0,
        "act_pressure": 0.0,
    }

    if bool(pause_mode):
        allow_block = True
        rejection_reason = "pause_mode"
        pre_action_phase = "hold"
    elif decision not in ("LONG", "SHORT"):
        allow_block = True
        rejection_reason = reject_reason_default
        pre_action_phase = "hold"
    else:
        external_tension_pressure = dominant_tension_value if dominant_tension_cause in (
            "external_pressure",
            "uncertainty_pressure",
            "aftereffect_pressure",
            "areal_conflict_pressure",
        ) else 0.0
        internal_tension_pressure = dominant_tension_value if dominant_tension_cause in (
            "inner_conflict_pressure",
            "repetition_pressure",
            "expectation_pressure",
        ) else 0.0
        field_fragmentation_pressure = _clip01(
            (field_perception_fragmentation * 0.46)
            + ((1.0 - field_perception_focus) * 0.24)
            + (field_observation_need * 0.30)
        )
        field_strain_pressure = _clip01(
            (field_perception_strain * 0.42)
            + ((1.0 - field_perception_stability) * 0.24)
            + (field_replan_pressure * 0.34)
        )
        processing_observe_pressure = _clip01(
            (processing_load * 0.34)
            + (breakout_tension * 0.22)
            + ((1.0 - processing_alignment) * 0.18)
            + (processing_areal_tension * 0.16)
            + ((1.0 - processing_areal_support) * 0.10)
        )
        low_courage_pressure = _clip01(
            ((1.0 - regulated_courage) * 0.24)
            + ((1.0 - state_maturity) * 0.18)
            + ((1.0 - decision_readiness) * 0.18)
            + ((1.0 - structure_quality) * 0.14)
            + ((1.0 - structure_action_bearing) * 0.12)
            + ((1.0 - action_clearance) * 0.14)
        )
        open_hypothesis_reality_pressure = _clip01(
            (open_hypothesis_reality_check_need * 0.34)
            + ((1.0 - open_hypothesis_reality_permission) * 0.22)
            + (open_hypothesis_motor_tension * 0.18)
            + ((1.0 - action_weight) * 0.12)
        )
        positive_return_need = _clip01(
            positive_overextension + positive_return_pressure + (1.0 if positive_zero_point_regulation else 0.0) * 0.20
        )
        maturity_gap_pressure = _clip01(
            ((1.0 - state_maturity) * 0.20)
            + ((1.0 - decision_readiness) * 0.18)
            + ((1.0 - signal_quality) * 0.18)
            + ((1.0 - action_readiness_from_field) * 0.16)
            + ((1.0 - action_clearance) * 0.14)
        )
        observe_pressure = _clip01(
            ((1.0 if observation_mode else 0.0) * 0.18)
            + (external_tension_pressure * 0.12)
            + (pre_action_observation_need * 0.14)
            + (observe_priority * 0.10)
            + (uncertainty_score * 0.10)
            + (processing_observe_pressure * 0.12)
            + (field_fragmentation_pressure * 0.12)
            + (action_inhibition * 0.08)
            + (positive_return_need * 0.06)
        )
        replan_pressure = _clip01(
            (field_strain_pressure * 0.16)
            + (expectation_pressure * 0.08)
            + (repetition_pressure * 0.08)
            + (courage_gap * 0.08)
            + (internal_tension_pressure * 0.12)
            + (field_replan_pressure * 0.14)
            + (open_hypothesis_reality_pressure * 0.12)
            + (decision_conflict * 0.10)
            + (rumination_depth * 0.06)
            + (felt_conflict * 0.06)
        )
        hold_pressure = _clip01(
            (low_courage_pressure * 0.18)
            + (maturity_gap_pressure * 0.16)
            + (action_inhibition * 0.12)
            + ((1.0 - action_clearance) * 0.10)
            + (processing_load * processing_tension * 0.12)
            + (processing_areal_tension * (1.0 - areal_support) * 0.10)
            + (field_perception_instability * (1.0 - action_readiness_from_field) * 0.10)
            + (felt_pressure * (1.0 - state_maturity) * 0.08)
            + ((1.0 - market_balance) * (1.0 - visual_reflective_coherence) * breakout_tension * 0.06)
        )
        act_pressure = _clip01(
            (decision_strength * 0.18)
            + (field_perception_clarity * 0.12)
            + (field_perception_stability * 0.12)
            + (action_readiness_from_field * 0.14)
            + (action_clearance * 0.14)
            + (regulated_courage * 0.10)
            + (state_maturity * 0.08)
            + (decision_readiness * 0.08)
            + (structure_action_bearing * 0.04)
            - (observe_pressure * 0.12)
            - (replan_pressure * 0.12)
            - (hold_pressure * 0.14)
        )
        pre_action_pressure_trace = {
            "observe_pressure": float(observe_pressure),
            "replan_pressure": float(replan_pressure),
            "hold_pressure": float(hold_pressure),
            "act_pressure": float(act_pressure),
            "low_courage_pressure": float(low_courage_pressure),
            "maturity_gap_pressure": float(maturity_gap_pressure),
            "open_hypothesis_reality_pressure": float(open_hypothesis_reality_pressure),
            "field_fragmentation_pressure": float(field_fragmentation_pressure),
            "field_strain_pressure": float(field_strain_pressure),
        }
        pressure_choice = max(
            {
                "observe": observe_pressure,
                "replan": replan_pressure,
                "hold": hold_pressure,
                "act": act_pressure,
            },
            key={
                "observe": observe_pressure,
                "replan": replan_pressure,
                "hold": hold_pressure,
                "act": act_pressure,
            }.get,
        )
        allow_observe = pressure_choice == "observe"
        allow_ruminate = pressure_choice == "replan"
        allow_block = pressure_choice == "hold"
        allow_plan = pressure_choice == "act"
        pre_action_phase = pressure_choice
        rejection_reason = {
            "observe": "pre_action_observe_pressure",
            "replan": "pre_action_replan_pressure",
            "hold": "pre_action_hold_pressure",
            "act": "plan_allowed",
        }.get(pressure_choice, "pre_action_pressure_selection")

    act_watch_enabled = bool(getattr(cfg, "MCM_ACT_WATCH_ENABLED", True)) if cfg is not None else True
    act_watch_structure_max = float(getattr(cfg, "MCM_ACT_WATCH_STRUCTURE_MAX", 0.58) or 0.58) if cfg is not None else 0.58
    act_watch_plan_pressure_min = float(getattr(cfg, "MCM_ACT_WATCH_PLAN_PRESSURE_MIN", 0.44) or 0.44) if cfg is not None else 0.44
    act_watch_maturity_min = float(getattr(cfg, "MCM_ACT_WATCH_MATURITY_MIN", 0.38) or 0.38) if cfg is not None else 0.38
    act_watch_trace = {}
    if bool(allow_plan) and decision in ("LONG", "SHORT"):
        uncertainty_components = {
            "structure_carrying": structure_carrying_need,
            "structure_action": structure_action_uncertainty,
            "learned_development": learned_development_uncertainty,
            "visual_action": visual_action_uncertainty,
            "variant_learning": variant_learning_pressure,
            "transfer_maturity": transfer_maturity_gap,
        }
        dominant_uncertainty_reason = max(uncertainty_components, key=uncertainty_components.get)
        dominant_uncertainty_pressure = uncertainty_components.get(dominant_uncertainty_reason, 0.0)
        act_watch_pressure = _clip01(
            ((1.0 if act_watch_enabled else 0.0) * 0.08)
            + (max(0.0, act_watch_structure_max - structure_quality) * 0.16)
            + (max(0.0, plan_pressure - act_watch_plan_pressure_min) * 0.14)
            + (max(0.0, act_watch_readiness - act_watch_maturity_min) * 0.10)
            + (dominant_uncertainty_pressure * 0.18)
            + (field_replan_pressure * 0.08)
            + (form_symbol_reframe_binding * 0.06)
        )
        development_reframe_pressure = _clip01(
            (learned_development_uncertainty * 0.26)
            + (form_symbol_reframe_binding * 0.14)
            + (max(0.0, (1.06 + form_symbol_reframe_binding * 0.30 + learned_development_uncertainty * 0.42) - decision_strength) * 0.10)
        )
        structure_orientation_pressure = _clip01(
            ((1.0 if structure_orientation_guard else 0.0) * 0.26)
            + (max(0.0, action_structure_min - structure_quality) * 0.16)
            + (max(0.0, mid_support_min - memory_support) * 0.12)
            + (max(0.0, 1.0 - structure_action_bearing) * 0.08)
        )
        semantic_transfer_pressure = _clip01(
            (semantic_shift_pressure * 0.18)
            + (max(0.0, 1.0 - transfer_bearing) * 0.10)
            + (transfer_maturity_gap * 0.18)
            + (max(0.0, 1.0 - trust_transfer_support) * 0.10)
            + ((1.0 if transfer_break_ready else 0.0) * transfer_recovery_need * 0.12)
        )
        plan_continuity_pressure = _clip01(
            (decision_strength * 0.20)
            + (structure_quality * 0.14)
            + (memory_support * 0.12)
            + (structure_action_bearing * 0.12)
            + (trust_transfer_support * 0.10)
            + (form_symbol_action_trust * 0.08)
        )
        act_watch_trace = {
            "act_watch_pressure": float(act_watch_pressure),
            "development_reframe_pressure": float(development_reframe_pressure),
            "structure_orientation_pressure": float(structure_orientation_pressure),
            "semantic_transfer_pressure": float(semantic_transfer_pressure),
            "plan_continuity_pressure": float(plan_continuity_pressure),
            "dominant_uncertainty_reason": str(dominant_uncertainty_reason),
            "dominant_uncertainty_pressure": float(dominant_uncertainty_pressure),
        }
        posture_pressures = {
            "act_watch": act_watch_pressure,
            "development_reframe": development_reframe_pressure,
            "structure_orientation": structure_orientation_pressure,
            "semantic_transfer": semantic_transfer_pressure,
        }
        posture_reason = max(posture_pressures, key=posture_pressures.get)
        posture_pressure = posture_pressures.get(posture_reason, 0.0)
        if posture_pressure > plan_continuity_pressure:
            allow_plan = False
            allow_observe = True
            allow_ruminate = bool(
                (field_replan_pressure + form_symbol_reframe_binding + transfer_recovery_need + semantic_shift_pressure)
                > (field_observation_need + act_watch_readiness + memory_support)
            )
            allow_block = False
            if posture_reason == "act_watch":
                rejection_reason = f"{dominant_uncertainty_reason}_act_watch"
                pre_action_phase = "act_watch"
            else:
                rejection_reason = f"{posture_reason}_replan" if allow_ruminate else f"{posture_reason}_observe"
                pre_action_phase = "replan" if allow_ruminate else "observe"

    if bool(zero_point_regulation) and not bool(allow_plan):
        allow_observe = True
        allow_ruminate = False
        allow_block = False
        rejection_reason = "zero_point_regulation"
        pre_action_phase = "observe"

    former_allow_block = bool(allow_block)
    if former_allow_block:
        allow_block = False
        if pre_action_phase == "hold" and decision in ("LONG", "SHORT"):
            allow_observe = True
        if isinstance(rejection_reason, str) and rejection_reason.endswith("_block"):
            rejection_reason = rejection_reason[:-6] + "_hold"

    # Non-economic regulation must describe inner posture, not prevent the
    # later inner-action consent bridge from doing its work. The economic
    # value gate remains the only hard execution gate.
    if decision in ("LONG", "SHORT") and not bool(pause_mode):
        allow_plan = True

    return {
        "allow_observe": bool(allow_observe),
        "allow_ruminate": bool(allow_ruminate),
        "allow_plan": bool(allow_plan),
        "allow_block": bool(allow_block),
        "former_allow_block": bool(former_allow_block),
        "inner_distance_state": str(rejection_reason or "-"),
        "former_block_reason": str(rejection_reason or "-") if former_allow_block else "-",
        "non_economic_gate_policy": "field_modulation_only",
        "rejection_reason": str(rejection_reason or "-"),
        "pre_action_phase": str(pre_action_phase),
        "pre_action_pressure_trace": dict(pre_action_pressure_trace),
        "act_watch_trace": dict(act_watch_trace),
    }


def _build_neurochemical_meta_axes(context=None, felt_state=None):
    ctx = dict(context or {})
    felt = dict(felt_state or {})
    return {
        "signal_quality": ctx.get("signal_quality", 0.0),
        "decision_strength": ctx.get("decision_strength", 0.0),
        "decision_readiness": ctx.get("decision_readiness", 0.0),
        "state_maturity": ctx.get("state_maturity", 0.0),
        "processing_load": ctx.get("processing_load", 0.0),
        "processing_tension": ctx.get("processing_tension", 0.0),
        "processing_alignment": ctx.get("processing_alignment", 0.0),
        "field_perception_pressure": ctx.get("field_perception_pressure", 0.0),
        "field_perception_support": ctx.get("field_perception_support", 0.0),
        "field_perception_clarity": ctx.get("field_perception_clarity", 0.0),
        "field_perception_focus": ctx.get("field_perception_focus", 0.0),
        "field_perception_stability": ctx.get("field_perception_stability", 0.0),
        "field_perception_fragmentation": ctx.get("field_perception_fragmentation", 0.0),
        "field_perception_strain": ctx.get("field_perception_strain", 0.0),
        "field_activity_island_activation_mean": ctx.get("field_activity_island_activation_mean", 0.0),
        "field_activity_island_pressure_mean": ctx.get("field_activity_island_pressure_mean", 0.0),
        "field_activity_island_context_reactivation_mean": ctx.get("field_activity_island_context_reactivation_mean", 0.0),
        "visual_clarity": ctx.get("visual_clarity", 0.0),
        "visual_object_stability": ctx.get("visual_object_stability", 0.0),
        "visual_blindness": ctx.get("visual_blindness", 0.0),
        "visual_form_pressure": ctx.get("visual_form_pressure", 0.0),
        "visual_shape_resonance": ctx.get("visual_shape_resonance", 0.0),
        "visual_shape_fragility": ctx.get("visual_shape_fragility", 0.0),
        "visual_blind_action_load": ctx.get("visual_blind_action_load", 0.0),
        "visual_action_uncertainty": ctx.get("visual_action_uncertainty", 0.0),
        "felt_pressure": ctx.get("felt_pressure", 0.0),
        "felt_stability": float(felt.get("felt_stability", 0.0) or 0.0),
        "felt_alignment": ctx.get("felt_alignment", 0.0),
        "pressure_release": float(felt.get("pressure_release", 0.0) or 0.0),
        "experience_regulation": ctx.get("experience_regulation", 0.0),
        "load_bearing_capacity": ctx.get("load_bearing_capacity", 0.0),
        "stress_relief_potential": float(felt.get("stress_relief_potential", 0.0) or 0.0),
        "protective_courage": ctx.get("protective_courage", 0.0),
        "memory_support": ctx.get("memory_support", 0.0),
        "memory_inhibition": ctx.get("memory_inhibition", 0.0),
        "memory_compare_load": ctx.get("memory_compare_load", 0.0),
        "memory_conflict": ctx.get("memory_conflict", 0.0),
        "cognitive_load": ctx.get("cognitive_load", 0.0),
        "decision_energy_cost": ctx.get("decision_energy_cost", 0.0),
        "thinking_complexity": ctx.get("thinking_complexity", 0.0),
        "memory_orientation": ctx.get("memory_orientation", 0.0),
        "orientation_gap": ctx.get("orientation_gap", 0.0),
        "blind_thinking_load": ctx.get("blind_thinking_load", 0.0),
        "action_inhibition": ctx.get("action_inhibition", 0.0),
        "action_clearance": ctx.get("action_clearance", 0.0),
        "regulated_courage": ctx.get("regulated_courage", 0.0),
        "plan_pressure": ctx.get("plan_pressure", 0.0),
        "act_watch_readiness": ctx.get("act_watch_readiness", 0.0),
        "structure_action_uncertainty": ctx.get("structure_action_uncertainty", 0.0),
        "structure_carrying_need": ctx.get("structure_carrying_need", 0.0),
        "field_observation_need": ctx.get("field_observation_need", 0.0),
        "field_replan_pressure": ctx.get("field_replan_pressure", 0.0),
        "field_bearing_support": ctx.get("field_bearing_support", ctx.get("field_action_support", 0.0)),
        "action_readiness_from_field": ctx.get("action_readiness_from_field", ctx.get("field_action_support", 0.0)),
        "field_action_support": ctx.get("field_action_support", 0.0),
        "semantic_shift_pressure": ctx.get("semantic_shift_pressure", 0.0),
        "transfer_bearing": ctx.get("transfer_bearing", 0.0),
        "trust_transfer_support": ctx.get("trust_transfer_support", 0.0),
        "transfer_maturity_gap": ctx.get("transfer_maturity_gap", 0.0),
        "transfer_break_fatigue": ctx.get("transfer_break_fatigue", 0.0),
        "interpretation_quality": ctx.get("interpretation_quality", 0.0),
        "route_familiarity": ctx.get("route_familiarity", 0.0),
        "learned_development_uncertainty": ctx.get("learned_development_uncertainty", 0.0),
        "variant_learning_pressure": ctx.get("variant_learning_pressure", 0.0),
        "variant_bearing_memory": ctx.get("variant_bearing_memory", 0.0),
        "uncertainty_familiarity": ctx.get("uncertainty_familiarity", 0.0),
        "form_symbol_development_quality": ctx.get("form_symbol_development_quality", 0.0),
        "form_symbol_learning_trust": ctx.get("form_symbol_learning_trust", 0.0),
        "form_symbol_action_trust": ctx.get("form_symbol_action_trust", 0.0),
        "form_symbol_caution_trust": ctx.get("form_symbol_caution_trust", 0.0),
    }


def _build_conscious_perception_meta_axes(context=None, felt_state=None):
    ctx = dict(context or {})
    felt = dict(felt_state or {})
    return {
        "field_perception_pressure": ctx.get("field_perception_pressure", 0.0),
        "field_perception_support": ctx.get("field_perception_support", 0.0),
        "field_perception_clarity": ctx.get("field_perception_clarity", 0.0),
        "field_perception_focus": ctx.get("field_perception_focus", 0.0),
        "field_perception_stability": ctx.get("field_perception_stability", 0.0),
        "field_perception_fragmentation": ctx.get("field_perception_fragmentation", 0.0),
        "field_perception_strain": ctx.get("field_perception_strain", 0.0),
        "field_observation_need": ctx.get("field_observation_need", 0.0),
        "field_replan_pressure": ctx.get("field_replan_pressure", 0.0),
        "field_bearing_support": ctx.get("field_bearing_support", ctx.get("field_action_support", 0.0)),
        "action_readiness_from_field": ctx.get("action_readiness_from_field", ctx.get("field_action_support", 0.0)),
        "field_action_support": ctx.get("field_action_support", 0.0),
        "visual_clarity": ctx.get("visual_clarity", 0.0),
        "visual_object_stability": ctx.get("visual_object_stability", 0.0),
        "visual_blindness": ctx.get("visual_blindness", 0.0),
        "visual_form_pressure": ctx.get("visual_form_pressure", 0.0),
        "visual_form_novelty": ctx.get("visual_form_novelty", 0.0),
        "visual_action_uncertainty": ctx.get("visual_action_uncertainty", 0.0),
        "felt_pressure": ctx.get("felt_pressure", 0.0),
        "felt_stability": float(felt.get("felt_stability", 0.0) or 0.0),
        "felt_alignment": ctx.get("felt_alignment", 0.0),
        "aftereffect_pressure": ctx.get("aftereffect_pressure", 0.0),
        "pressure_release": float(felt.get("pressure_release", 0.0) or 0.0),
        "experience_regulation": ctx.get("experience_regulation", 0.0),
        "load_bearing_capacity": ctx.get("load_bearing_capacity", 0.0),
        "memory_support": ctx.get("memory_support", 0.0),
        "memory_compare_load": ctx.get("memory_compare_load", 0.0),
        "cognitive_load": ctx.get("cognitive_load", 0.0),
        "memory_orientation": ctx.get("memory_orientation", 0.0),
        "orientation_gap": ctx.get("orientation_gap", 0.0),
        "blind_thinking_load": ctx.get("blind_thinking_load", 0.0),
        "structure_action_uncertainty": ctx.get("structure_action_uncertainty", 0.0),
        "semantic_shift_pressure": ctx.get("semantic_shift_pressure", 0.0),
        "transfer_bearing": ctx.get("transfer_bearing", 0.0),
        "interpretation_quality": ctx.get("interpretation_quality", 0.0),
        "action_clearance": ctx.get("action_clearance", 0.0),
        "action_inhibition": ctx.get("action_inhibition", 0.0),
        "symbolic_regulation": ctx.get("symbolic_regulation", 0.0),
        "symbolic_object_distance": ctx.get("form_symbol_object_distance", 0.0),
        "symbolic_containment": ctx.get("form_symbol_containment", 0.0),
        "symbolic_field_decoupling": ctx.get("form_symbol_field_decoupling", 0.0),
        "form_symbol_observation_binding": ctx.get("form_symbol_observation_binding", 0.0),
        "form_symbol_reframe_binding": ctx.get("form_symbol_reframe_binding", 0.0),
        "variant_learning_pressure": ctx.get("variant_learning_pressure", 0.0),
        "uncertainty_familiarity": ctx.get("uncertainty_familiarity", 0.0),
    }


def _read_conscious_perception_values(conscious_perception_state=None):
    state = dict(conscious_perception_state or {})
    return {
        "conscious_label": str(state.get("conscious_perception_state", "open_perception") or "open_perception"),
        "inner_posture_label": str(state.get("inner_posture_state", "uncertain_open") or "uncertain_open"),
        "perceptual_distance": float(state.get("perceptual_distance", 0.0) or 0.0),
        "object_contact_depth": float(state.get("object_contact_depth", 0.0) or 0.0),
        "field_attachment": float(state.get("field_attachment", 0.0) or 0.0),
        "release_capacity": float(state.get("release_capacity", 0.0) or 0.0),
        "inner_outer_alignment": float(state.get("inner_outer_alignment", 0.0) or 0.0),
        "selective_attention": float(state.get("selective_attention", 0.0) or 0.0),
        "curiosity_tone": float(state.get("curiosity_tone", 0.0) or 0.0),
        "fatigue_tone": float(state.get("fatigue_tone", 0.0) or 0.0),
        "calm_tone": float(state.get("calm_tone", 0.0) or 0.0),
        "arousal_load": float(state.get("arousal_load", 0.0) or 0.0),
        "stimulus_field_effect": float(state.get("stimulus_field_effect", 0.0) or 0.0),
        "inner_impact_trace": float(state.get("inner_impact_trace", 0.0) or 0.0),
        "perceived_field_change": float(state.get("perceived_field_change", 0.0) or 0.0),
        "felt_afterimage": float(state.get("felt_afterimage", 0.0) or 0.0),
        "inner_outer_reflection": float(state.get("inner_outer_reflection", 0.0) or 0.0),
        "background_containment": float(state.get("background_containment", 0.0) or 0.0),
        "reflective_distance": float(state.get("reflective_distance", 0.0) or 0.0),
    }


def _build_spacetime_regulation_state(temporal_state=None, strategic_state=None, context=None):
    temporal = dict(temporal_state or {})
    strategic = dict(strategic_state or {})
    ctx = dict(context or {})

    temporal_continuity = float(temporal.get("temporal_continuity", 0.0) or 0.0)
    temporal_source_binding = float(temporal.get("temporal_source_binding", 0.0) or 0.0)
    temporal_recurrence = float(temporal.get("temporal_recurrence", 0.0) or 0.0)
    temporal_novelty = float(temporal.get("temporal_novelty", 0.0) or 0.0)
    temporal_afterimage = float(temporal.get("temporal_afterimage", 0.0) or 0.0)
    temporal_decay = float(temporal.get("temporal_decay", 0.0) or 0.0)
    temporal_context_depth = float(temporal.get("temporal_context_depth", 0.0) or 0.0)
    mcm_spacetime_depth = float(temporal.get("mcm_spacetime_depth", 0.0) or 0.0)
    memory_experience_depth = float(temporal.get("memory_experience_depth", 0.0) or 0.0)
    future_projection_depth = float(temporal.get("future_projection_depth", 0.0) or 0.0)
    temporal_self_location = float(temporal.get("temporal_self_location", 0.0) or 0.0)
    temporal_self_location_state = str(temporal.get("temporal_self_location_state", "unlocated_contact") or "unlocated_contact")
    temporal_self_consistency = float(temporal.get("temporal_self_consistency", 0.0) or 0.0)
    perception_sequence_coherence = float(temporal.get("perception_sequence_coherence", 0.0) or 0.0)
    memory_time_distance = float(temporal.get("memory_time_distance", 1.0) or 1.0)
    temporal_binding_state = str(temporal.get("temporal_binding_state", "unbound_moment") or "unbound_moment")
    area_afterimage = float(strategic.get("area_afterimage", 0.0) or 0.0)
    structure_action_bearing = float(ctx.get("structure_action_bearing", 0.0) or 0.0)
    interpretation_quality = float(ctx.get("interpretation_quality", 0.0) or 0.0)

    spacetime_unlocated_pressure = _clip01(
        (max(0.0, 0.34 - temporal_self_location) * 0.56)
        + (max(0.0, 0.30 - mcm_spacetime_depth) * 0.34)
        + ((1.0 if temporal_self_location_state == "unlocated_contact" else 0.0) * 0.16)
        + ((1.0 if temporal_binding_state == "unbound_moment" else 0.0) * 0.10)
        + (temporal_novelty * 0.08)
        - (temporal_source_binding * 0.10)
    )
    spacetime_memory_bearing = _clip01(
        (memory_experience_depth * 0.30)
        + (temporal_recurrence * 0.16)
        + (temporal_context_depth * 0.16)
        + (temporal_self_location * 0.14)
        + (perception_sequence_coherence * 0.12)
        + (max(0.0, 1.0 - memory_time_distance) * 0.12)
    )
    spacetime_future_bearing = _clip01(
        (future_projection_depth * 0.32)
        + (mcm_spacetime_depth * 0.18)
        + (temporal_self_location * 0.14)
        + (perception_sequence_coherence * 0.12)
        + (structure_action_bearing * 0.12)
        + (interpretation_quality * 0.12)
    )
    spacetime_regulation_support = _clip01(
        (spacetime_memory_bearing * 0.30)
        + (spacetime_future_bearing * 0.30)
        + (temporal_self_location * 0.18)
        + (mcm_spacetime_depth * 0.14)
        + (temporal_source_binding * 0.08)
        - (spacetime_unlocated_pressure * 0.18)
    )
    spacetime_reflection_need = _clip01(
        (spacetime_unlocated_pressure * 0.36)
        + (max(0.0, future_projection_depth - temporal_self_location) * 0.16)
        + (max(0.0, mcm_spacetime_depth - memory_experience_depth) * 0.10)
        + ((1.0 if temporal_self_location_state == "future_possibility" else 0.0) * 0.06)
        + ((1.0 if temporal_self_location_state == "afterimage_trace" else 0.0) * 0.10)
        - (spacetime_memory_bearing * 0.10)
    )
    spacetime_regulation_pressures = {
        "spacetime_unlocated_reflection": _clip01((spacetime_unlocated_pressure * 0.58) + ((1.0 - spacetime_regulation_support) * 0.42)),
        "afterimage_reframe": _clip01(((1.0 if temporal_self_location_state == "afterimage_trace" else 0.0) * 0.36) + (spacetime_reflection_need * 0.64)),
        "memory_depth_bearing": _clip01(((1.0 if temporal_self_location_state == "remembered_experience" else 0.0) * 0.30) + (spacetime_memory_bearing * 0.70)),
        "future_depth_watch": _clip01(((1.0 if temporal_self_location_state == "future_possibility" else 0.0) * 0.30) + (spacetime_future_bearing * 0.70)),
        "present_depth_bearing": _clip01(((1.0 if temporal_self_location_state == "present_contact" else 0.0) * 0.30) + (spacetime_regulation_support * 0.70)),
        "spacetime_open": _clip01((temporal_self_location * 0.34) + (spacetime_regulation_support * 0.26) + ((1.0 - spacetime_unlocated_pressure) * 0.22)),
    }
    spacetime_regulation_state = max(spacetime_regulation_pressures, key=spacetime_regulation_pressures.get)

    return {
        "temporal_continuity": float(temporal_continuity),
        "temporal_source_binding": float(temporal_source_binding),
        "temporal_recurrence": float(temporal_recurrence),
        "temporal_novelty": float(temporal_novelty),
        "temporal_afterimage": float(temporal_afterimage),
        "temporal_decay": float(temporal_decay),
        "temporal_context_depth": float(temporal_context_depth),
        "mcm_spacetime_depth": float(mcm_spacetime_depth),
        "memory_experience_depth": float(memory_experience_depth),
        "future_projection_depth": float(future_projection_depth),
        "temporal_self_location": float(temporal_self_location),
        "temporal_self_location_state": str(temporal_self_location_state),
        "temporal_self_consistency": float(temporal_self_consistency),
        "perception_sequence_coherence": float(perception_sequence_coherence),
        "memory_time_distance": float(memory_time_distance),
        "temporal_binding_state": str(temporal_binding_state),
        "area_afterimage": float(area_afterimage),
        "spacetime_unlocated_pressure": float(spacetime_unlocated_pressure),
        "spacetime_memory_bearing": float(spacetime_memory_bearing),
        "spacetime_future_bearing": float(spacetime_future_bearing),
        "spacetime_regulation_support": float(spacetime_regulation_support),
        "spacetime_reflection_need": float(spacetime_reflection_need),
        "spacetime_regulation_state": str(spacetime_regulation_state),
    }


def _build_experience_effort_feedback_state(packet_feedback=None, context=None):
    feedback = dict(packet_feedback or {})
    ctx = dict(context or {})

    previous_packet_process_reward = _clip01(float(feedback.get("packet_process_reward", 0.0) or 0.0))
    previous_packet_bearing_quality = _clip01(float(feedback.get("packet_bearing_quality", 0.0) or 0.0))
    previous_packet_inner_outer_fit = _clip01(float(feedback.get("packet_inner_outer_fit", 0.0) or 0.0))
    previous_packet_repetition_potential = _clip01(float(feedback.get("packet_repetition_potential", 0.0) or 0.0))
    previous_packet_curiosity_pull = _clip01(float(feedback.get("packet_curiosity_pull", 0.0) or 0.0))
    previous_packet_reorganization_need = _clip01(float(feedback.get("packet_reorganization_need", 0.0) or 0.0))
    previous_constructive_stimulation = _clip01(float(feedback.get("constructive_stimulation", 0.0) or 0.0))
    previous_constructive_dopamine = _clip01(float(feedback.get("constructive_dopamine", 0.0) or 0.0))
    previous_stabilizing_serotonin = _clip01(float(feedback.get("stabilizing_serotonin", 0.0) or 0.0))
    previous_packet_label = str(feedback.get("experience_packet_label", "-") or "-").strip().lower() or "-"

    structure_action_bearing = float(ctx.get("structure_action_bearing", 0.0) or 0.0)
    field_bearing_support = float(ctx.get("field_bearing_support", ctx.get("field_action_support", 0.0)) or 0.0)
    action_readiness_from_field = float(ctx.get("action_readiness_from_field", ctx.get("field_action_support", field_bearing_support)) or 0.0)
    field_action_support = action_readiness_from_field
    inner_outer_alignment = float(ctx.get("inner_outer_alignment", 0.0) or 0.0)
    regulated_courage = float(ctx.get("regulated_courage", 0.0) or 0.0)
    curiosity_tone = float(ctx.get("curiosity_tone", 0.0) or 0.0)
    structure_action_uncertainty = float(ctx.get("structure_action_uncertainty", 0.0) or 0.0)
    fatigue_tone = float(ctx.get("fatigue_tone", 0.0) or 0.0)
    structure_quality = float(ctx.get("structure_quality", 0.0) or 0.0)
    context_confidence = float(ctx.get("context_confidence", 0.0) or 0.0)
    interpretation_quality = float(ctx.get("interpretation_quality", 0.0) or 0.0)
    open_hypothesis_reifung_pressure = float(ctx.get("open_hypothesis_reifung_pressure", 0.0) or 0.0)
    open_hypothesis_reality_check_need = float(ctx.get("open_hypothesis_reality_check_need", 0.0) or 0.0)
    open_hypothesis_action_tension = float(ctx.get("open_hypothesis_action_tension", ctx.get("open_hypothesis_motor_tension", 0.0)) or 0.0)
    open_hypothesis_motor_tension = float(open_hypothesis_action_tension)
    open_hypothesis_bearing_echo = float(ctx.get("open_hypothesis_bearing_echo", 0.0) or 0.0)
    open_hypothesis_reality_bearing = float(
        ctx.get(
            "open_hypothesis_reality_bearing",
            ctx.get("open_hypothesis_reality_fit", ctx.get("open_hypothesis_reality_permission", ctx.get("open_hypothesis_action_permission", 0.0))),
        )
        or 0.0
    )
    open_hypothesis_reality_fit = float(open_hypothesis_reality_bearing)
    open_hypothesis_reality_permission = float(open_hypothesis_reality_bearing)
    open_hypothesis_action_permission = float(open_hypothesis_reality_bearing)
    object_contact_depth = float(ctx.get("object_contact_depth", 0.0) or 0.0)
    selective_attention = float(ctx.get("selective_attention", 0.0) or 0.0)
    action_clearance = float(ctx.get("action_clearance", 0.0) or 0.0)
    act_watch_readiness = float(ctx.get("act_watch_readiness", 0.0) or 0.0)
    field_observation_need = float(ctx.get("field_observation_need", 0.0) or 0.0)
    field_replan_pressure = float(ctx.get("field_replan_pressure", 0.0) or 0.0)
    action_inhibition = float(ctx.get("action_inhibition", 0.0) or 0.0)

    engaged_effort = max(
        0.0,
        min(
            1.0,
            (previous_packet_process_reward * 0.15)
            + (previous_constructive_stimulation * 0.13)
            + (previous_packet_bearing_quality * 0.10)
            + (previous_packet_inner_outer_fit * 0.08)
            + (previous_constructive_dopamine * 0.06)
            + (previous_stabilizing_serotonin * 0.05)
            + (structure_action_bearing * 0.15)
            + (action_readiness_from_field * 0.10)
            + (inner_outer_alignment * 0.08)
            + (regulated_courage * 0.08)
            + (curiosity_tone * 0.05)
            + (previous_packet_repetition_potential * 0.05)
            - (previous_packet_reorganization_need * 0.08)
            - (structure_action_uncertainty * 0.08)
            - (fatigue_tone * 0.05),
        ),
    )
    effort_reorganization_pressure = max(
        0.0,
        min(
            1.0,
            (previous_packet_reorganization_need * 0.28)
            + (structure_action_uncertainty * 0.30)
            + (max(0.0, 0.52 - structure_action_bearing) * 0.18)
            + (max(0.0, 0.46 - action_readiness_from_field) * 0.12)
            + (max(0.0, 0.46 - engaged_effort) * 0.22)
            + (fatigue_tone * 0.08)
            - (previous_packet_process_reward * 0.08)
            - (curiosity_tone * 0.04),
        ),
    )
    pre_action_reorganization_pressure = max(
        0.0,
        min(
            1.0,
            (previous_packet_reorganization_need * 0.20)
            + (max(0.0, 0.42 - previous_packet_process_reward) * 0.18)
            + ((1.0 if previous_packet_label == "reorganize_packet" else 0.0) * 0.08)
            + (structure_action_uncertainty * 0.22)
            + (max(0.0, 0.58 - structure_quality) * 0.20)
            + (max(0.0, 0.46 - context_confidence) * 0.14)
            + (max(0.0, 0.54 - structure_action_bearing) * 0.20)
            + (max(0.0, 0.48 - action_readiness_from_field) * 0.14)
            + (max(0.0, 0.46 - interpretation_quality) * 0.08)
            + (max(0.0, 0.42 - inner_outer_alignment) * 0.06)
            + (open_hypothesis_reifung_pressure * 0.10)
            + (open_hypothesis_reality_check_need * 0.14)
            + (open_hypothesis_motor_tension * 0.06)
            - (previous_constructive_stimulation * 0.08)
            - (open_hypothesis_bearing_echo * 0.06)
            - (open_hypothesis_reality_permission * 0.10)
            - (max(0.0, structure_quality - 0.62) * 0.18)
            - (max(0.0, context_confidence - 0.52) * 0.10)
            - (max(0.0, structure_action_bearing - 0.54) * 0.10)
            - (max(0.0, action_readiness_from_field - 0.50) * 0.06),
        ),
    )
    pre_action_context_selectivity = max(
        0.0,
        min(
            1.0,
            (structure_action_bearing * 0.24)
            + (structure_quality * 0.22)
            + (context_confidence * 0.12)
            + (action_readiness_from_field * 0.18)
            + (interpretation_quality * 0.16)
            + (inner_outer_alignment * 0.12)
            + (engaged_effort * 0.12)
            + (open_hypothesis_bearing_echo * 0.10)
            + (open_hypothesis_reality_permission * 0.08)
            + (previous_packet_process_reward * 0.10)
            + (previous_constructive_stimulation * 0.08)
            - (open_hypothesis_reifung_pressure * 0.12)
            - (open_hypothesis_reality_check_need * 0.08)
            - (pre_action_reorganization_pressure * 0.18),
        ),
    )
    effort_learning_pull = max(
        0.0,
        min(
            1.0,
            (previous_packet_curiosity_pull * 0.20)
            + (previous_packet_repetition_potential * 0.18)
            + (previous_constructive_stimulation * 0.16)
            + (object_contact_depth * 0.12)
            + (selective_attention * 0.10)
            + (curiosity_tone * 0.10)
            + (max(0.0, 0.50 - previous_packet_bearing_quality) * 0.08)
            - (fatigue_tone * 0.08),
        ),
    )
    effort_state_pressures = {
        "underengaged_reorganize": _clip01((max(effort_reorganization_pressure, pre_action_reorganization_pressure) * 0.56) + ((1.0 - engaged_effort) * 0.44)),
        "engaged_bearing": _clip01((engaged_effort * 0.50) + ((1.0 - effort_reorganization_pressure) * 0.24) + ((1.0 - pre_action_reorganization_pressure) * 0.20)),
        "curious_effort": _clip01((effort_learning_pull * 0.58) + (engaged_effort * 0.42)),
        "constructive_echo": _clip01(((1.0 if previous_packet_label == "constructive_packet" else 0.0) * 0.42) + (engaged_effort * 0.58)),
        "settled_effort": _clip01((1.0 - max(effort_reorganization_pressure, pre_action_reorganization_pressure, effort_learning_pull)) * 0.36 + engaged_effort * 0.20),
    }
    effort_state = max(effort_state_pressures, key=effort_state_pressures.get)
    if effort_state in ("engaged_bearing", "constructive_echo", "curious_effort"):
        effort_boost = max(0.0, engaged_effort - 0.40)
        action_readiness_from_field = max(0.0, min(1.0, action_readiness_from_field + (effort_boost * 0.045)))
        field_action_support = action_readiness_from_field
        action_clearance = max(0.0, min(1.0, action_clearance + (effort_boost * 0.040)))
        act_watch_readiness = max(0.0, min(1.0, act_watch_readiness + (effort_learning_pull * 0.040)))
    elif effort_state == "underengaged_reorganize":
        reorganization_signal = max(effort_reorganization_pressure, pre_action_reorganization_pressure)
        field_observation_need = max(0.0, min(1.0, field_observation_need + (reorganization_signal * 0.085)))
        field_replan_pressure = max(0.0, min(1.0, field_replan_pressure + (max(0.0, reorganization_signal - 0.24) * 0.075)))
        action_inhibition = max(0.0, min(1.0, action_inhibition + (reorganization_signal * 0.050)))
        action_clearance = max(0.0, min(1.0, action_clearance - (reorganization_signal * 0.045)))
        act_watch_readiness = max(0.0, min(1.0, act_watch_readiness + (effort_learning_pull * 0.060) + (reorganization_signal * 0.055)))

    return {
        "previous_packet_process_reward": float(previous_packet_process_reward),
        "previous_packet_bearing_quality": float(previous_packet_bearing_quality),
        "previous_packet_inner_outer_fit": float(previous_packet_inner_outer_fit),
        "previous_packet_repetition_potential": float(previous_packet_repetition_potential),
        "previous_packet_curiosity_pull": float(previous_packet_curiosity_pull),
        "previous_packet_reorganization_need": float(previous_packet_reorganization_need),
        "previous_constructive_stimulation": float(previous_constructive_stimulation),
        "previous_constructive_dopamine": float(previous_constructive_dopamine),
        "previous_stabilizing_serotonin": float(previous_stabilizing_serotonin),
        "previous_packet_label": str(previous_packet_label),
        "engaged_effort": float(engaged_effort),
        "effort_reorganization_pressure": float(effort_reorganization_pressure),
        "pre_action_reorganization_pressure": float(pre_action_reorganization_pressure),
        "pre_action_context_selectivity": float(pre_action_context_selectivity),
        "effort_learning_pull": float(effort_learning_pull),
        "effort_state": str(effort_state),
        "field_bearing_support": float(field_bearing_support),
        "action_readiness_from_field": float(action_readiness_from_field),
        "field_action_support": float(field_action_support),
        "action_clearance": float(action_clearance),
        "act_watch_readiness": float(act_watch_readiness),
        "field_observation_need": float(field_observation_need),
        "field_replan_pressure": float(field_replan_pressure),
        "action_inhibition": float(action_inhibition),
    }


def _build_diffuse_open_development_state(context=None):
    context = dict(context or {})
    inner_posture_label = str(context.get("inner_posture_label", "") or "")
    conscious_label = str(context.get("conscious_label", "") or "")
    object_contact_depth = _clip01(context.get("object_contact_depth", 0.0))
    perceptual_distance = _clip01(context.get("perceptual_distance", 0.0))
    release_capacity = _clip01(context.get("release_capacity", 0.0))
    inner_outer_alignment = _clip01(context.get("inner_outer_alignment", 0.0))
    curiosity_tone = _clip01(context.get("curiosity_tone", 0.0))
    calm_tone = _clip01(context.get("calm_tone", 0.0))
    field_attachment = _clip01(context.get("field_attachment", 0.0))
    field_observation_need = _clip01(context.get("field_observation_need", 0.0))
    field_replan_pressure = _clip01(context.get("field_replan_pressure", 0.0))
    action_inhibition = _clip01(context.get("action_inhibition", 0.0))
    action_clearance = _clip01(context.get("action_clearance", 0.0))
    act_watch_readiness = _clip01(context.get("act_watch_readiness", 0.0))

    diffuse_open_development_pressure = _clip01(
        ((1.0 if inner_posture_label == "uncertain_open" else 0.0) * 0.24)
        + ((1.0 if conscious_label == "open_perception" else 0.0) * 0.12)
        + (max(0.0, 0.22 - object_contact_depth) * 0.70)
        + (max(0.0, 0.20 - perceptual_distance) * 0.55)
        + (max(0.0, 0.20 - release_capacity) * 0.50)
        + (max(0.0, 0.26 - inner_outer_alignment) * 0.42)
        + (max(0.0, 0.16 - curiosity_tone) * 0.26)
        - (calm_tone * 0.08)
        - (field_attachment * 0.06)
    )

    posture_development_pressures = {
        "develop_object_contact": _clip01(diffuse_open_development_pressure * ((1.0 - object_contact_depth) * 0.56 + (1.0 - curiosity_tone) * 0.44)),
        "develop_reflective_distance": _clip01(diffuse_open_development_pressure * ((1.0 - perceptual_distance) * 0.50 + (1.0 - inner_outer_alignment) * 0.50)),
        "develop_release_capacity": _clip01(diffuse_open_development_pressure * (1.0 - release_capacity)),
        "develop_observation": _clip01(diffuse_open_development_pressure * (field_observation_need * 0.34 + curiosity_tone * 0.24 + calm_tone * 0.16)),
        "stable_posture": _clip01((1.0 - diffuse_open_development_pressure) * 0.40 + calm_tone * 0.20),
    }
    posture_development_hint = max(posture_development_pressures, key=posture_development_pressures.get)
    field_observation_need = _clip01(field_observation_need + (diffuse_open_development_pressure * 0.055))
    field_replan_pressure = _clip01(field_replan_pressure + (diffuse_open_development_pressure * 0.030))
    action_inhibition = _clip01(action_inhibition + (diffuse_open_development_pressure * 0.060))
    action_clearance = _clip01(action_clearance - (diffuse_open_development_pressure * 0.040))
    act_watch_readiness = _clip01(act_watch_readiness + (diffuse_open_development_pressure * 0.080))

    return {
        "diffuse_open_development_pressure": float(diffuse_open_development_pressure),
        "posture_development_hint": posture_development_hint,
        "field_observation_need": float(field_observation_need),
        "field_replan_pressure": float(field_replan_pressure),
        "action_inhibition": float(action_inhibition),
        "action_clearance": float(action_clearance),
        "act_watch_readiness": float(act_watch_readiness),
    }


def _apply_open_hypothesis_mutation_state(context=None):
    context = dict(context or {})
    field_observation_need = _clip01(context.get("field_observation_need", 0.0))
    field_replan_pressure = _clip01(context.get("field_replan_pressure", 0.0))
    action_inhibition = _clip01(context.get("action_inhibition", 0.0))
    action_clearance = _clip01(context.get("action_clearance", 0.0))
    regulated_courage = _clip01(context.get("regulated_courage", 0.0))
    act_watch_readiness = _clip01(context.get("act_watch_readiness", 0.0))
    field_bearing_support = _clip01(context.get("field_bearing_support", context.get("field_action_support", 0.0)))
    action_readiness_from_field = _clip01(context.get("action_readiness_from_field", context.get("field_action_support", field_bearing_support)))
    field_action_support = action_readiness_from_field
    reifung = _clip01(context.get("open_hypothesis_reifung_pressure", 0.0))
    reflection = _clip01(context.get("open_hypothesis_reflection_pull", 0.0))
    reality = _clip01(context.get("open_hypothesis_reality_check_need", 0.0))
    action_tension = _clip01(context.get("open_hypothesis_action_tension", context.get("open_hypothesis_motor_tension", 0.0)))
    confirm = _clip01(context.get("open_hypothesis_confirmation_weight", 0.0))
    learning = _clip01(context.get("open_hypothesis_learning_charge", 0.0))
    reality_bearing = _clip01(
        context.get(
            "open_hypothesis_reality_bearing",
            context.get("open_hypothesis_reality_fit", context.get("open_hypothesis_reality_permission", context.get("open_hypothesis_action_permission", 0.0))),
        )
    )
    echo = _clip01(context.get("open_hypothesis_bearing_echo", 0.0))
    caution = _clip01(context.get("hypothesis_caution", 0.0))
    if reifung > 0.0:
        field_observation_need = _clip01(field_observation_need + reflection * 0.050 + reality * 0.030 + action_tension * 0.014 - confirm * 0.020)
        field_replan_pressure = _clip01(field_replan_pressure + reflection * 0.050 + learning * 0.034 + reality * 0.024 - confirm * 0.018)
        action_inhibition = _clip01(action_inhibition + action_tension * 0.024 + caution * 0.020 + reality * 0.012 - confirm * 0.014)
        action_clearance = _clip01(action_clearance - action_tension * 0.018 - reifung * 0.012 - reality * 0.010 + reality_bearing * 0.026)
        regulated_courage = _clip01(regulated_courage - reifung * 0.014 + confirm * 0.018 + reality_bearing * 0.012)
        act_watch_readiness = _clip01(act_watch_readiness + reflection * 0.052 + learning * 0.040 + reality * 0.030 - confirm * 0.016)
    if echo > 0.0:
        action_readiness_from_field = _clip01(action_readiness_from_field + confirm * 0.032 + reality_bearing * 0.022 - reality * 0.012)
        field_action_support = action_readiness_from_field
        action_clearance = _clip01(action_clearance + reality_bearing * 0.026)
        regulated_courage = _clip01(regulated_courage + confirm * 0.024)
    return {
        "field_observation_need": float(field_observation_need),
        "field_replan_pressure": float(field_replan_pressure),
        "action_inhibition": float(action_inhibition),
        "action_clearance": float(action_clearance),
        "regulated_courage": float(regulated_courage),
        "act_watch_readiness": float(act_watch_readiness),
        "field_bearing_support": float(field_bearing_support),
        "action_readiness_from_field": float(action_readiness_from_field),
        "field_action_support": float(field_action_support),
    }


def _build_trust_return_state(context=None):
    ctx = dict(context or {})
    bot = ctx.get("bot")
    previous_thought_seed_state = dict(getattr(bot, "mcm_thought_seed_state", {}) or {}) if bot is not None else {}

    def _seed_float(key, default=0.0):
        try:
            value = float(previous_thought_seed_state.get(key, default) or default)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(0.0, min(1.0, float(value)))

    previous_digest_state = str(previous_thought_seed_state.get("thought_digest_state", "") or "")
    previous_trust_return_readiness = _seed_float("trust_return_readiness")
    previous_digestive_returned_trust = _seed_float("thought_digestive_returned_trust")
    previous_digestive_replay_pull = _seed_float("thought_digestive_replay_pull")
    previous_digestive_distance_pull = _seed_float("thought_digestive_distance_pull")
    previous_digest_action_permission = _seed_float("open_hypothesis_reality_permission", _seed_float("open_hypothesis_action_permission"))
    previous_emergent_structure_state = str(previous_thought_seed_state.get("emergent_structure_state", "") or "")
    previous_thought_confirmation_score = _seed_float("thought_confirmation_score")
    previous_reality_binding_score = _seed_float("reality_binding_score")
    previous_thought_maturity = _seed_float("thought_maturity")
    previous_form_mcm_family_recurrence = _seed_float("form_mcm_family_recurrence")
    previous_form_mcm_family_maturity = _seed_float("form_mcm_family_maturity")
    previous_form_mcm_family_trust = _seed_float("form_mcm_family_trust")
    previous_form_mcm_family_caution = _seed_float("form_mcm_family_caution")
    previous_form_mcm_family_reorganization_need = _seed_float("form_mcm_family_reorganization_need")
    open_hypothesis_confirmation_weight = _clip01(ctx.get("open_hypothesis_confirmation_weight", 0.0))
    open_hypothesis_reifung_state = str(ctx.get("open_hypothesis_reifung_state", "open_hypothesis_neutral_memory") or "open_hypothesis_neutral_memory")
    open_hypothesis_learning_charge = _clip01(ctx.get("open_hypothesis_learning_charge", 0.0))
    open_hypothesis_reality_check_need = _clip01(ctx.get("open_hypothesis_reality_check_need", 0.0))
    inner_outer_alignment = _clip01(ctx.get("inner_outer_alignment", 0.0))
    perceptual_distance = _clip01(ctx.get("perceptual_distance", 0.0))
    cortisol_load = _clip01(ctx.get("cortisol_load", 0.0))
    nervous_system_overload = _clip01(ctx.get("nervous_system_overload", 0.0))
    field_perception_strain = _clip01(ctx.get("field_perception_strain", 0.0))
    emotional_decoupling = _clip01(ctx.get("emotional_decoupling", 0.0))
    acetylcholine_focus = _clip01(ctx.get("acetylcholine_focus", 0.0))
    serotonin_stability = _clip01(ctx.get("serotonin_stability", 0.0))

    previous_confirmed_structure_protection = _clip01(
        ((1.0 if previous_emergent_structure_state in ("confirmed_structure_contact", "confirmed_structural_interpretation") else 0.0) * 0.34)
        + (previous_thought_confirmation_score * 0.24)
        + (previous_reality_binding_score * 0.20)
        + (previous_thought_maturity * 0.14)
        + (previous_form_mcm_family_trust * 0.10)
        + (previous_form_mcm_family_maturity * 0.05)
        + (open_hypothesis_confirmation_weight * 0.08)
        - (previous_form_mcm_family_caution * 0.04)
    )
    trust_return_open_hypothesis_load = _clip01(
        (0.28 if open_hypothesis_reifung_state == "open_hypothesis_reorganizing_memory" else 0.0)
        + (0.20 if open_hypothesis_reifung_state == "open_hypothesis_burden_memory" else 0.0)
        + (0.10 if open_hypothesis_reifung_state == "open_hypothesis_neutral_memory" else 0.0)
        + (open_hypothesis_learning_charge * 0.20)
        + (open_hypothesis_reality_check_need * 0.18)
        + (max(0.0, open_hypothesis_confirmation_weight - 0.42) * 0.10)
        + (previous_form_mcm_family_reorganization_need * 0.08)
        + (previous_form_mcm_family_caution * 0.04)
        - (previous_form_mcm_family_trust * 0.03)
    )
    trust_return_context_instability = _clip01(
        (max(0.0, 0.42 - inner_outer_alignment) * 0.34)
        + (max(0.0, 0.30 - perceptual_distance) * 0.18)
        + (max(0.0, cortisol_load - 0.32) * 0.22)
        + (max(0.0, nervous_system_overload - 0.28) * 0.16)
        + (field_perception_strain * 0.10)
    )
    trust_return_motor_contact_strength = _clip01(
        ((1.0 if previous_digest_state in ("digestive_trust_emergence", "digestive_trust_return") else 0.0) * 0.22)
        + (previous_trust_return_readiness * 0.22)
        + (previous_digestive_returned_trust * 0.16)
        + (trust_return_open_hypothesis_load * 0.18)
        + (trust_return_context_instability * 0.12)
        + (max(previous_digestive_replay_pull, previous_digestive_distance_pull) * 0.10)
        + (previous_form_mcm_family_recurrence * previous_form_mcm_family_trust * 0.05)
        - (previous_confirmed_structure_protection * 0.10)
    )
    trust_return_motor_heat = _clip01(
        (previous_trust_return_readiness * 0.28)
        + (previous_digestive_returned_trust * 0.24)
        + (max(0.0, cortisol_load - 0.30) * 0.22)
        + (max(0.0, previous_digest_action_permission - 0.28) * 0.16)
        + (max(previous_digestive_replay_pull, previous_digestive_distance_pull) * 0.10)
        + (trust_return_open_hypothesis_load * 0.12)
        + (trust_return_context_instability * 0.10)
    )
    trust_return_stabilization_need = _clip01(
        ((1.0 if previous_digest_state in ("digestive_trust_emergence", "digestive_trust_return") else 0.0) * 0.18)
        + (trust_return_motor_heat * 0.34)
        + (trust_return_motor_contact_strength * 0.18)
        + (max(0.0, cortisol_load - 0.34) * 0.24)
        + (max(0.0, previous_digest_action_permission - 0.32) * 0.14)
        + (max(0.0, 0.40 - emotional_decoupling) * 0.10)
        + (trust_return_open_hypothesis_load * 0.18)
        + (trust_return_context_instability * 0.16)
        + (max(0.0, 0.40 - inner_outer_alignment) * 0.10)
    )
    trust_return_focus_pull = _clip01(
        (previous_trust_return_readiness * 0.24)
        + (previous_digestive_returned_trust * 0.18)
        + (acetylcholine_focus * 0.14)
        + (serotonin_stability * 0.12)
        + (max(0.0, 1.0 - cortisol_load) * 0.10)
        + (inner_outer_alignment * 0.12)
        + (perceptual_distance * 0.10)
        + (previous_form_mcm_family_maturity * 0.04)
        + (previous_form_mcm_family_trust * 0.03)
        + (trust_return_context_instability * 0.08)
    )
    trust_return_contact_pressure = _clip01(
        ((1.0 if previous_digest_state in ("digestive_trust_emergence", "digestive_trust_return") else 0.0) * 0.38)
        + (trust_return_motor_contact_strength * 0.62)
    )
    trust_return_motor_contact = bool(trust_return_contact_pressure > 0.0)
    trust_return_motor_mode_pressures = {
        "trust_stabilize_before_act": _clip01((trust_return_stabilization_need * 0.54) + (cortisol_load * 0.30) + (trust_return_contact_pressure * 0.16)),
        "trust_focused_ready": _clip01((trust_return_focus_pull * 0.58) + (trust_return_contact_pressure * 0.22) + (previous_digestive_returned_trust * 0.12)),
        "trust_emerging": _clip01((trust_return_contact_pressure * 0.46) + (previous_trust_return_readiness * 0.24) + (previous_form_mcm_family_trust * 0.10)),
        "trust_quiet": _clip01((1.0 - trust_return_contact_pressure) * 0.42 + (1.0 - trust_return_stabilization_need) * 0.16),
    }
    trust_return_motor_mode = max(trust_return_motor_mode_pressures, key=trust_return_motor_mode_pressures.get)

    trust_return_act_bridge = _clip01(
        (trust_return_stabilization_need * 0.36)
        + (trust_return_motor_contact_strength * 0.28)
        + (trust_return_open_hypothesis_load * 0.18)
        + (trust_return_context_instability * 0.12)
        + (previous_form_mcm_family_trust * 0.04)
        - (previous_confirmed_structure_protection * 0.16)
        - (previous_form_mcm_family_caution * 0.04)
        - (previous_form_mcm_family_reorganization_need * 0.03)
    )

    return {
        "previous_digest_state": str(previous_digest_state),
        "previous_trust_return_readiness": float(previous_trust_return_readiness),
        "previous_digestive_returned_trust": float(previous_digestive_returned_trust),
        "previous_digestive_replay_pull": float(previous_digestive_replay_pull),
        "previous_digestive_distance_pull": float(previous_digestive_distance_pull),
        "previous_digest_action_permission": float(previous_digest_action_permission),
        "previous_emergent_structure_state": str(previous_emergent_structure_state),
        "previous_form_mcm_family_recurrence": float(previous_form_mcm_family_recurrence),
        "previous_form_mcm_family_maturity": float(previous_form_mcm_family_maturity),
        "previous_form_mcm_family_trust": float(previous_form_mcm_family_trust),
        "previous_form_mcm_family_caution": float(previous_form_mcm_family_caution),
        "previous_form_mcm_family_reorganization_need": float(previous_form_mcm_family_reorganization_need),
        "previous_confirmed_structure_protection": float(previous_confirmed_structure_protection),
        "trust_return_open_hypothesis_load": float(trust_return_open_hypothesis_load),
        "trust_return_context_instability": float(trust_return_context_instability),
        "trust_return_motor_contact_strength": float(trust_return_motor_contact_strength),
        "trust_return_motor_heat": float(trust_return_motor_heat),
        "trust_return_stabilization_need": float(trust_return_stabilization_need),
        "trust_return_focus_pull": float(trust_return_focus_pull),
        "trust_return_motor_mode": str(trust_return_motor_mode),
        "trust_return_act_bridge": float(trust_return_act_bridge),
    }


def build_meta_regulation_state(perception_state, processing_state, felt_state, thought_state, fused, pause_mode=False, bot=None):

    perception = dict(perception_state or {})
    processing = dict(processing_state or {})
    felt = dict(felt_state or {})
    thought = dict(thought_state or {})
    fused_state = dict(fused or {})

    def _num(*sources, key=None, default=0.0):
        for source in sources:
            if isinstance(source, dict) and key in source:
                try:
                    return float(source.get(key, default) or default)
                except Exception:
                    return float(default)
        return float(default)

    outcome_decomposition = dict(getattr(bot, "last_outcome_decomposition", {}) or {}) if bot is not None else {}
    outcome_trace_coupling = 0.38

    action_weight = active_context_activation = active_context_bearing = active_context_conflict = active_context_support = 0.0
    aftereffect_pressure = area_afterimage = areal_conflict_pressure = areal_support = arousal_load = 0.0
    background_containment = blind_thinking_load = breakout_tension = calm_tone = cognitive_load = 0.0
    contact_state_observe_bias = context_confidence = courage_gap = curiosity_tone = decision_conflict = 0.0
    decision_readiness = decision_strength = decision_weight = diffuse_open_development_pressure = dominant_tension_value = 0.0
    effort_learning_pull = effort_reorganization_pressure = engaged_effort = expectation_pressure = experience_regulation = 0.0
    external_pressure = fatigue_tone = felt_afterimage = felt_conflict = felt_pressure = 0.0
    field_activity_island_count = field_attachment = field_perception_clarity = field_perception_focus = field_perception_fragmentation = 0.0
    field_perception_instability = field_perception_pressure = field_perception_stability = field_perception_strain = field_perception_support = 0.0
    form_symbol_action_binding = form_symbol_action_trust = form_symbol_caution_trust = form_symbol_compound_bearing = form_symbol_compound_load_reduction = 0.0
    form_symbol_compound_novelty = form_symbol_contact_burden_evidence = form_symbol_contact_carefulness = form_symbol_contact_maturity = form_symbol_contact_pain_memory = 0.0
    form_symbol_contact_utility = form_symbol_contact_utility_evidence = form_symbol_containment = form_symbol_development_quality = form_symbol_field_decoupling = 0.0
    form_symbol_learning_trust = form_symbol_object_distance = form_symbol_observation_binding = form_symbol_reframe_binding = future_projection_depth = 0.0
    hypothesis_reorganization_weight = hypothesis_trust = hypothesis_weight = inner_conflict_pressure = inner_impact_trace = 0.0
    inner_outer_alignment = interpretation_quality = known_form_support = learned_development_uncertainty = load_bearing_capacity = 0.0
    market_balance = mcm_spacetime_depth = memory_conflict = memory_experience_depth = memory_orientation = 0.0
    memory_time_distance = object_contact_depth = observe_priority = open_hypothesis_trace_strength = orientation_gap = 0.0
    perceived_field_change = perception_sequence_coherence = plan_pressure = posture_development_hint = pre_action_context_selectivity = 0.0
    pre_action_observation_need = pre_action_reorganization_pressure = previous_constructive_stimulation = previous_open_hypothesis_burden_score = previous_open_hypothesis_consequence_score = 0.0
    previous_open_hypothesis_distance_need = previous_open_hypothesis_reinterpretation_need = previous_open_hypothesis_reorganization_score = previous_open_hypothesis_replay_need = previous_packet_bearing_quality = 0.0
    previous_packet_process_reward = previous_packet_reorganization_need = processing_alignment = processing_areal_support = processing_areal_tension = 0.0
    processing_load = processing_tension = protective_courage = protective_width_regulation = release_capacity = 0.0
    repetition_pressure = route_familiarity = rumination_depth = selective_attention = semantic_shift_pressure = 0.0
    signal_quality = spacetime_future_bearing = spacetime_memory_bearing = spacetime_reflection_need = spacetime_regulation_support = 0.0
    spacetime_unlocated_pressure = state_maturity = stimulus_field_effect = structure_action_bearing = structure_action_gap = 0.0
    structure_action_uncertainty = structure_carrying_need = structure_orientation = structure_orientation_gap = structure_orientation_guard = 0.0
    structure_quality = symbolic_action_regulation = symbolic_inner_regulation = symbolic_regulation = temporal_afterimage = 0.0
    temporal_context_depth = temporal_continuity = temporal_decay = temporal_novelty = temporal_recurrence = 0.0
    temporal_self_consistency = temporal_self_location = temporal_source_binding = transfer_bearing = transfer_maturity_gap = 0.0
    transfer_recovery_need = trust_transfer_base = trust_transfer_support = uncertain_form_exposure = uncertainty_familiarity = 0.0
    uncertainty_pressure = uncertainty_score = variant_bearing_memory = variant_learning_pressure = variant_similarity = 0.0
    thought_alignment = thought_load_pressure = thought_overprocessing_signal = thought_economy_need = thought_release_pressure = thought_efficiency_support = 0.0
    perception_event_strength = 0.0
    variant_spread = visual_action_uncertainty = visual_blind_action_load = visual_blindness = visual_clarity = 0.0
    visual_coherence = visual_reflective_coherence = visual_form_novelty = visual_form_pressure = visual_grounding_gap = visual_grounding_need = 0.0
    visual_grounding_strength = visual_object_binding = visual_object_stability = visual_rational_observation_support = visual_resonance_unbound = 0.0
    visual_cortex_grounding = visual_cortex_presence = visual_cortex_clarity = visual_cortex_relation_coherence = visual_cortex_readiness = 0.0
    visual_object_binding_quality = visual_contact_nearness = visual_lifecycle_stability = visual_lifecycle_rejection = visual_lifecycle_dissolution = 0.0
    visual_shape_fragility = visual_shape_resonance = 0.0
    mcm_reflective_bearing = mcm_reflective_pressure = mcm_reflective_coupling_load = mcm_reflective_displacement = 0.0
    mcm_reflective_field_position = mcm_reflective_tension = 0.0
    adaptation_phase = "-"
    conscious_label = "open_perception"
    conscious_perception_state = "-"
    decision = "WAIT"
    dominant_activity_island_id = "-"
    dominant_tension_cause = "-"
    effort_state = "-"
    field_perception_label = "quiet_field"
    form_symbol_contact_learning_state = "-"
    inner_posture_label = "uncertain_open"
    neurochemical_state = "-"
    open_hypothesis_reifung_state = "-"
    previous_open_hypothesis_learning_state = "-"
    previous_open_hypothesis_reorganization_posture = "-"
    previous_packet_label = "-"
    spacetime_regulation_state = "-"
    temporal_binding_state = "-"
    temporal_self_location_state = "-"
    trust_transfer_mode = "-"
    uncertain_form_family_state = "-"
    visual_grounding_state = "-"
    transfer_break_fatigue = False
    transfer_break_ready = False
    transfer_break_trigger = False
    zero_point_regulation = False
    decision = str(fused_state.get("decision", fused_state.get("proposed_decision", "WAIT")) or "WAIT").upper()
    uncertainty_score = _clip01(_num(perception, thought, fused_state, key="uncertainty_score"))
    observe_priority = _clip01(_num(perception, thought, fused_state, key="observe_priority"))
    signal_quality = _clip01(_num(perception, processing, felt, fused_state, key="signal_quality"))
    long_hypothesis = _num(thought, key="long_hypothesis")
    short_hypothesis = _num(thought, key="short_hypothesis")
    decision_strength = max(long_hypothesis, short_hypothesis)
    decision_readiness = _clip01(_num(thought, felt, processing, fused_state, key="decision_readiness"))
    decision_conflict = _clip01(_num(thought, felt, processing, fused_state, key="decision_conflict"))
    state_maturity = _clip01(_num(thought, felt, processing, key="state_maturity"))
    processing_load = _clip01(_num(processing, thought, key="processing_load"))
    processing_alignment = _clip01(_num(processing, thought, key="processing_alignment"))
    processing_tension = _clip01(_num(processing, thought, key="processing_tension"))
    felt_pressure = _clip01(_num(felt, thought, processing, key="felt_pressure"))
    felt_conflict = _clip01(_num(felt, thought, processing, key="felt_conflict"))
    market_balance = _num(felt, perception, key="market_balance")
    breakout_tension = _clip01(_num(felt, perception, key="breakout_tension"))
    visual_coherence = _clip01(_num(felt, perception, processing, key="visual_coherence"))
    visual_reflective_coherence = _clip01(_num(felt, processing, perception, key="visual_reflective_coherence", default=visual_coherence))
    field_perception_pressure = _clip01(_num(processing, felt, key="field_perception_pressure"))
    field_perception_support = _clip01(_num(processing, felt, key="field_perception_support"))
    field_perception_clarity = _clip01(_num(processing, felt, key="field_perception_clarity"))
    field_perception_focus = _clip01(_num(processing, felt, key="field_perception_focus"))
    field_perception_stability = _clip01(_num(processing, felt, key="field_perception_stability"))
    field_perception_fragmentation = _clip01(_num(processing, felt, key="field_perception_fragmentation"))
    field_perception_strain = _clip01(_num(processing, felt, key="field_perception_strain"))
    visual_clarity = _clip01(_num(perception, processing, felt, key="visual_clarity"))
    visual_object_stability = _clip01(_num(perception, processing, felt, key="visual_object_stability"))
    visual_blindness = _clip01(_num(perception, processing, felt, key="visual_blindness"))
    visual_form_pressure = _clip01(_num(perception, processing, felt, key="visual_form_pressure"))
    visual_form_novelty = _clip01(_num(perception, processing, felt, key="visual_form_novelty"))
    visual_shape_resonance = _clip01(_num(perception, processing, felt, key="visual_shape_resonance"))
    visual_shape_fragility = _clip01(_num(perception, processing, felt, key="visual_shape_fragility"))
    visual_cortex_state = dict(perception.get("visual_cortex_state", {}) or {})
    visual_cortex_presence = _clip01(visual_cortex_state.get("object_presence", 0.0))
    visual_cortex_clarity = _clip01(visual_cortex_state.get("object_clarity", 0.0))
    visual_cortex_relation_coherence = _clip01(visual_cortex_state.get("relation_coherence", 0.0))
    visual_cortex_readiness = _clip01(visual_cortex_state.get("visual_readiness", 0.0))
    visual_object_binding_quality = _clip01(visual_cortex_state.get("visual_object_binding_quality", 0.0))
    visual_contact_nearness = _clip01(visual_cortex_state.get("visual_contact_nearness", 0.0))
    visual_lifecycle_stability = _clip01(visual_cortex_state.get("visual_lifecycle_stability", 0.0))
    visual_lifecycle_rejection = _clip01(visual_cortex_state.get("visual_lifecycle_rejection", 0.0))
    visual_lifecycle_dissolution = _clip01(visual_cortex_state.get("visual_lifecycle_dissolution", 0.0))
    visual_attention_label = str(processing.get("visual_attention_label", perception.get("visual_attention_label", felt.get("visual_attention_label", "background_form"))) or "background_form")
    visual_form_contact = _clip01(_num(processing, perception, felt, key="visual_form_contact"))
    visual_inspection_pull = _clip01(_num(processing, perception, felt, key="visual_inspection_pull"))
    visual_attention_depth = _clip01(_num(processing, perception, felt, key="visual_attention_depth"))
    visual_background_filter = _clip01(_num(processing, perception, felt, key="visual_background_filter"))
    visual_mcm_contact_weight = _clip01(_num(processing, perception, felt, key="visual_mcm_contact_weight"))
    mcm_preregulator_state = dict(felt.get("mcm_preregulator_state", {}) or {})
    mcm_reflective_bearing = _clip01(_num(felt, processing, thought, mcm_preregulator_state, key="mcm_reflective_bearing"))
    mcm_reflective_pressure = _clip01(_num(felt, processing, thought, mcm_preregulator_state, key="mcm_reflective_pressure"))
    mcm_reflective_coupling_load = _clip01(_num(felt, processing, thought, mcm_preregulator_state, key="mcm_reflective_coupling_load"))
    mcm_reflective_displacement = max(-1.0, min(1.0, _num(felt, processing, thought, mcm_preregulator_state, key="mcm_reflective_displacement")))
    mcm_reflective_field_position = max(-3.0, min(3.0, _num(felt, processing, thought, mcm_preregulator_state, key="mcm_reflective_field_position")))
    mcm_reflective_tension = _clip01(_num(felt, processing, thought, mcm_preregulator_state, key="mcm_reflective_tension"))
    external_pressure = _clip01(_num(felt, processing, thought, key="external_pressure"))
    inner_conflict_pressure = _clip01(_num(felt, processing, thought, key="inner_conflict_pressure"))
    repetition_pressure = _clip01(_num(felt, processing, thought, key="repetition_pressure"))
    expectation_pressure = _clip01(_num(felt, processing, thought, key="expectation_pressure"))
    uncertainty_pressure = _clip01(_num(felt, processing, thought, key="uncertainty_pressure"))
    aftereffect_pressure = _clip01(_num(felt, processing, thought, key="aftereffect_pressure"))
    areal_support = _clip01(_num(felt, processing, thought, key="areal_support"))
    areal_conflict_pressure = _clip01(_num(felt, processing, thought, key="areal_conflict_pressure"))
    dominant_tension_cause = str(felt.get("dominant_tension_cause", "-") or "-")
    dominant_tension_value = _clip01(felt.get("dominant_tension_value", 0.0))
    pre_action_observation_need = _clip01(felt.get("pre_action_observation_need", 0.0))
    observation_mode = bool(fused_state.get("observation_mode", False))
    reject_reason_default = "decision_wait"
    observe_priority_threshold = float(getattr(Config, "MCM_META_OBSERVE_PRIORITY_ALLOW", 0.66) or 0.66)
    uncertainty_threshold = float(getattr(Config, "MCM_META_UNCERTAINTY_ALLOW", 0.72) or 0.72)
    conflict_threshold = float(getattr(Config, "MCM_META_CONFLICT_ALLOW", 0.60) or 0.60)
    rumination_threshold = float(getattr(Config, "MCM_META_RUMINATION_ALLOW", 0.64) or 0.64)
    maturity_min = float(getattr(Config, "MCM_META_MATURITY_MIN", 0.34) or 0.34)
    readiness_min = float(getattr(Config, "MCM_META_READINESS_MIN", 0.38) or 0.38)
    signal_quality_min = float(getattr(Config, "MCM_META_SIGNAL_QUALITY_MIN", 0.24) or 0.24)
    action_structure_min = float(getattr(Config, "MCM_STRUCTURE_ACTION_MIN_QUALITY", 0.70) or 0.70)
    mid_support_min = float(getattr(Config, "MCM_STRUCTURE_ACTION_MID_SUPPORT_MIN", 0.045) or 0.045)
    mid_strength_min = float(getattr(Config, "MCM_STRUCTURE_ACTION_MID_STRENGTH_MIN", 1.36) or 1.36)
    low_strength_min = float(getattr(Config, "MCM_STRUCTURE_ACTION_LOW_STRENGTH_MIN", 1.52) or 1.52)
    form_symbol_state = dict(getattr(bot, "form_symbol_state", {}) or {}) if bot is not None else {}
    active_context_trace = _normalize_active_context_trace(getattr(bot, "active_context_trace", {}) or {}) if bot is not None else {}
    active_context_activation = _clip01(active_context_trace.get("activation", 0.0))
    active_context_support = _clip01(active_context_trace.get("support", 0.0))
    active_context_conflict = _clip01(active_context_trace.get("conflict", 0.0))
    active_context_bearing = _clip01(active_context_trace.get("bearing", 0.0))
    field_state = _build_field_regulation_state({**processing, **felt, **thought, **form_symbol_state})
    field_perception_instability = float(field_state.get("field_perception_instability", 0.0) or 0.0)
    field_observation_need = float(field_state.get("field_observation_need", 0.0) or 0.0)
    field_replan_pressure = float(field_state.get("field_replan_pressure", 0.0) or 0.0)
    field_action_support = float(field_state.get("field_action_support", 0.0) or 0.0)
    field_bearing_support = float(field_state.get("field_bearing_support", field_action_support) or 0.0)
    action_readiness_from_field = float(field_state.get("action_readiness_from_field", field_action_support) or 0.0)
    structure_quality = _clip01(_num(perception, processing, felt, form_symbol_state, key="structure_quality"))
    context_confidence = _clip01(_num(perception, processing, felt, form_symbol_state, key="context_confidence"))
    memory_support = _clip01(_num(thought, processing, felt, key="memory_support"))
    memory_conflict = _clip01(_num(thought, processing, felt, key="memory_conflict"))
    memory_inhibition = _clip01(_num(thought, processing, felt, key="memory_inhibition"))
    cognitive_load = _clip01(_num(thought, processing, felt, key="cognitive_load"))
    thinking_complexity = _clip01(_num(thought, processing, felt, key="thinking_complexity"))
    memory_compare_load = _clip01(_num(thought, processing, felt, key="memory_compare_load"))
    orientation_state = _build_orientation_state(locals())
    memory_orientation = float(orientation_state.get("memory_orientation", 0.0) or 0.0)
    orientation_gap = float(orientation_state.get("orientation_gap", 0.0) or 0.0)
    blind_thinking_load = float(orientation_state.get("blind_thinking_load", 0.0) or 0.0)
    thought_alignment = _clip01(_num(thought, processing, felt, key="thought_alignment"))
    structure_orientation = float(orientation_state.get("structure_orientation", 0.0) or 0.0)
    structure_orientation_gap = float(orientation_state.get("structure_orientation_gap", 0.0) or 0.0)
    zero_point_regulation = bool(orientation_state.get("zero_point_regulation", False))
    positive_zero_point_regulation = bool(orientation_state.get("positive_zero_point_regulation", False))
    structure_orientation_guard = bool(orientation_state.get("structure_orientation_guard", False))
    structure_action_state = _build_structure_action_state(locals())
    structure_action_bearing = float(structure_action_state.get("structure_action_bearing", 0.0) or 0.0)
    structure_action_gap = float(structure_action_state.get("structure_action_gap", 0.0) or 0.0)
    structure_action_uncertainty = float(structure_action_state.get("structure_action_uncertainty", 0.0) or 0.0)
    structure_carrying_need = float(structure_action_state.get("structure_carrying_need", 0.0) or 0.0)
    visual_action_grounding_state = _build_visual_action_grounding_state(
        field_state={**field_state, **structure_action_state},
        visual_state={
            **perception,
            **processing,
            **felt,
            **form_symbol_state,
            **structure_action_state,
            "visual_clarity": visual_clarity,
            "visual_object_stability": visual_object_stability,
            "visual_blindness": visual_blindness,
            "visual_form_pressure": visual_form_pressure,
            "visual_form_novelty": visual_form_novelty,
            "visual_shape_resonance": visual_shape_resonance,
            "visual_shape_fragility": visual_shape_fragility,
            "visual_attention_label": visual_attention_label,
            "visual_form_contact": visual_form_contact,
            "visual_inspection_pull": visual_inspection_pull,
            "visual_attention_depth": visual_attention_depth,
            "visual_background_filter": visual_background_filter,
            "visual_mcm_contact_weight": visual_mcm_contact_weight,
            "visual_cortex_presence": visual_cortex_presence,
            "visual_cortex_clarity": visual_cortex_clarity,
            "visual_cortex_relation_coherence": visual_cortex_relation_coherence,
            "visual_cortex_readiness": visual_cortex_readiness,
            "visual_object_binding_quality": visual_object_binding_quality,
            "visual_contact_nearness": visual_contact_nearness,
            "visual_lifecycle_stability": visual_lifecycle_stability,
            "visual_lifecycle_rejection": visual_lifecycle_rejection,
            "visual_lifecycle_dissolution": visual_lifecycle_dissolution,
            "visual_coherence": visual_coherence,
            "visual_reflective_coherence": visual_reflective_coherence,
            "structure_quality": structure_quality,
            "context_confidence": context_confidence,
            "field_perception_clarity": field_perception_clarity,
            "memory_orientation": memory_orientation,
        },
    )
    visual_blind_action_load = float(visual_action_grounding_state.get("visual_blind_action_load", 0.0) or 0.0)
    visual_action_uncertainty = float(visual_action_grounding_state.get("visual_action_uncertainty", 0.0) or 0.0)
    visual_object_binding = float(visual_action_grounding_state.get("visual_object_binding", 0.0) or 0.0)
    visual_cortex_grounding = float(visual_action_grounding_state.get("visual_cortex_grounding", 0.0) or 0.0)
    visual_grounding_strength = float(visual_action_grounding_state.get("visual_grounding_strength", 0.0) or 0.0)
    visual_resonance_unbound = float(visual_action_grounding_state.get("visual_resonance_unbound", 0.0) or 0.0)
    visual_grounding_gap = float(visual_action_grounding_state.get("visual_grounding_gap", 0.0) or 0.0)
    visual_grounding_need = float(visual_action_grounding_state.get("visual_grounding_need", 0.0) or 0.0)
    visual_rational_observation_support = float(visual_action_grounding_state.get("visual_rational_observation_support", 0.0) or 0.0)
    visual_grounding_state = str(visual_action_grounding_state.get("visual_grounding_state", "-") or "-")
    field_observation_need = float(visual_action_grounding_state.get("field_observation_need", field_observation_need) or 0.0)
    field_replan_pressure = float(visual_action_grounding_state.get("field_replan_pressure", field_replan_pressure) or 0.0)
    field_bearing_support = float(visual_action_grounding_state.get("field_bearing_support", field_bearing_support) or 0.0)
    action_readiness_from_field = float(visual_action_grounding_state.get("action_readiness_from_field", visual_action_grounding_state.get("field_action_support", action_readiness_from_field)) or 0.0)
    field_action_support = action_readiness_from_field
    structure_action_uncertainty = float(visual_action_grounding_state.get("structure_action_uncertainty", structure_action_uncertainty) or 0.0)
    structure_carrying_need = float(visual_action_grounding_state.get("structure_carrying_need", structure_carrying_need) or 0.0)
    action_state = _build_action_activation_state(locals())
    regulated_courage = float(action_state.get("regulated_courage", 0.0) or 0.0)
    courage_gap = float(action_state.get("courage_gap", 0.0) or 0.0)
    action_inhibition = float(action_state.get("action_inhibition", 0.0) or 0.0)
    action_clearance = float(action_state.get("action_clearance", 0.0) or 0.0)
    plan_pressure = float(action_state.get("plan_pressure", 0.0) or 0.0)
    act_watch_readiness = float(action_state.get("act_watch_readiness", 0.0) or 0.0)
    meta_axes = _build_neurochemical_meta_axes(locals(), felt)
    neurochemical_state = build_neurochemical_state(perception, processing, felt, thought, fused_state, meta_axes=meta_axes)
    conscious_meta_axes = _build_conscious_perception_meta_axes({**locals(), **meta_axes}, felt)
    conscious_perception_state = build_conscious_perception_state(perception, processing, felt, thought, fused_state, neurochemical_state=neurochemical_state, meta_axes=conscious_meta_axes)
    conscious_values = _read_conscious_perception_values(conscious_perception_state)
    conscious_label = str(conscious_values.get("conscious_label", "open_perception") or "open_perception")
    inner_posture_label = str(conscious_values.get("inner_posture_label", "uncertain_open") or "uncertain_open")
    perceptual_distance = float(conscious_values.get("perceptual_distance", 0.0) or 0.0)
    object_contact_depth = float(conscious_values.get("object_contact_depth", 0.0) or 0.0)
    field_attachment = float(conscious_values.get("field_attachment", 0.0) or 0.0)
    release_capacity = float(conscious_values.get("release_capacity", 0.0) or 0.0)
    inner_outer_alignment = float(conscious_values.get("inner_outer_alignment", 0.0) or 0.0)
    selective_attention = float(conscious_values.get("selective_attention", 0.0) or 0.0)
    curiosity_tone = float(conscious_values.get("curiosity_tone", 0.0) or 0.0)
    fatigue_tone = float(conscious_values.get("fatigue_tone", 0.0) or 0.0)
    calm_tone = float(conscious_values.get("calm_tone", 0.0) or 0.0)
    arousal_load = float(conscious_values.get("arousal_load", 0.0) or 0.0)
    stimulus_field_effect = float(conscious_values.get("stimulus_field_effect", 0.0) or 0.0)
    inner_impact_trace = float(conscious_values.get("inner_impact_trace", 0.0) or 0.0)
    perceived_field_change = float(conscious_values.get("perceived_field_change", 0.0) or 0.0)
    felt_afterimage = float(conscious_values.get("felt_afterimage", 0.0) or 0.0)
    inner_outer_reflection = float(conscious_values.get("inner_outer_reflection", 0.0) or 0.0)
    background_containment = float(conscious_values.get("background_containment", 0.0) or 0.0)
    reflective_distance = float(conscious_values.get("reflective_distance", 0.0) or 0.0)
    hypothesis_state = _build_open_hypothesis_feedback_state(locals())
    previous_open_hypothesis_learning_state = str(hypothesis_state.get("previous_open_hypothesis_learning_state", "new_hypothesis") or "new_hypothesis")
    previous_open_hypothesis_reorganization_posture = str(hypothesis_state.get("previous_open_hypothesis_reorganization_posture", "neutral") or "neutral")
    previous_open_hypothesis_consequence_score = float(hypothesis_state.get("previous_open_hypothesis_consequence_score", 0.0) or 0.0)
    previous_open_hypothesis_burden_score = float(hypothesis_state.get("previous_open_hypothesis_burden_score", 0.0) or 0.0)
    previous_open_hypothesis_reorganization_score = float(hypothesis_state.get("previous_open_hypothesis_reorganization_score", 0.0) or 0.0)
    previous_open_hypothesis_replay_need = float(hypothesis_state.get("previous_open_hypothesis_replay_need", 0.0) or 0.0)
    previous_open_hypothesis_distance_need = float(hypothesis_state.get("previous_open_hypothesis_distance_need", 0.0) or 0.0)
    previous_open_hypothesis_reinterpretation_need = float(hypothesis_state.get("previous_open_hypothesis_reinterpretation_need", 0.0) or 0.0)
    open_hypothesis_trace_strength = float(hypothesis_state.get("open_hypothesis_trace_strength", 0.0) or 0.0)
    open_hypothesis_bearing_echo = float(hypothesis_state.get("open_hypothesis_bearing_echo", 0.0) or 0.0)
    hypothesis_trust = float(hypothesis_state.get("hypothesis_trust", 0.0) or 0.0)
    hypothesis_caution = float(hypothesis_state.get("hypothesis_caution", 0.0) or 0.0)
    hypothesis_reorganization_weight = float(hypothesis_state.get("hypothesis_reorganization_weight", 0.0) or 0.0)
    open_hypothesis_confirmation_weight = float(hypothesis_state.get("open_hypothesis_confirmation_weight", 0.0) or 0.0)
    open_hypothesis_learning_charge = float(hypothesis_state.get("open_hypothesis_learning_charge", 0.0) or 0.0)
    open_hypothesis_reality_permission = float(
        hypothesis_state.get(
            "open_hypothesis_reality_bearing",
            hypothesis_state.get("open_hypothesis_reality_fit", hypothesis_state.get("open_hypothesis_reality_permission", hypothesis_state.get("open_hypothesis_action_permission", 0.0))),
        )
        or 0.0
    )
    open_hypothesis_action_permission = float(open_hypothesis_reality_permission)
    open_hypothesis_reality_check_need = float(hypothesis_state.get("open_hypothesis_reality_check_need", 0.0) or 0.0)
    hypothesis_weight = float(hypothesis_state.get("hypothesis_weight", 0.0) or 0.0)
    action_weight = float(hypothesis_state.get("action_weight", 0.0) or 0.0)
    decision_weight = float(hypothesis_state.get("decision_weight", 0.0) or 0.0)
    open_hypothesis_reifung_pressure = float(hypothesis_state.get("open_hypothesis_reifung_pressure", 0.0) or 0.0)
    open_hypothesis_reflection_pull = float(hypothesis_state.get("open_hypothesis_reflection_pull", 0.0) or 0.0)
    open_hypothesis_motor_tension = float(hypothesis_state.get("open_hypothesis_action_tension", hypothesis_state.get("open_hypothesis_motor_tension", 0.0)) or 0.0)
    open_hypothesis_reifung_state = str(hypothesis_state.get("open_hypothesis_reifung_state", "open_hypothesis_unformed") or "open_hypothesis_unformed")
    form_mcm_family_recurrence = float(hypothesis_state.get("form_mcm_family_recurrence", 0.0) or 0.0)
    form_mcm_family_maturity = float(hypothesis_state.get("form_mcm_family_maturity", 0.0) or 0.0)
    form_mcm_family_trust = float(hypothesis_state.get("form_mcm_family_trust", 0.0) or 0.0)
    form_mcm_family_caution = float(hypothesis_state.get("form_mcm_family_caution", 0.0) or 0.0)
    form_mcm_family_reorganization_need = float(hypothesis_state.get("form_mcm_family_reorganization_need", 0.0) or 0.0)
    declined_hypothesis_confirmation_without_action = float(hypothesis_state.get("declined_hypothesis_confirmation_without_action", 0.0) or 0.0)
    declined_hypothesis_rejection_without_action = float(hypothesis_state.get("declined_hypothesis_rejection_without_action", 0.0) or 0.0)
    declined_hypothesis_maturity = float(hypothesis_state.get("declined_hypothesis_maturity", 0.0) or 0.0)
    declined_hypothesis_protective_trace = float(hypothesis_state.get("declined_hypothesis_protective_trace", 0.0) or 0.0)
    declined_hypothesis_missed_trace = float(hypothesis_state.get("declined_hypothesis_missed_trace", 0.0) or 0.0)
    declined_hypothesis_mixed_trace = float(hypothesis_state.get("declined_hypothesis_mixed_trace", 0.0) or 0.0)
    declined_hypothesis_protective_edge = float(hypothesis_state.get("declined_hypothesis_protective_edge", 0.0) or 0.0)
    declined_hypothesis_missed_edge = float(hypothesis_state.get("declined_hypothesis_missed_edge", 0.0) or 0.0)
    directional_hypothesis_decision = str(hypothesis_state.get("directional_hypothesis_decision", "WAIT") or "WAIT")
    directional_hypothesis_confirmation = float(hypothesis_state.get("directional_hypothesis_confirmation", 0.0) or 0.0)
    directional_hypothesis_rejection = float(hypothesis_state.get("directional_hypothesis_rejection", 0.0) or 0.0)
    directional_hypothesis_maturity = float(hypothesis_state.get("directional_hypothesis_maturity", 0.0) or 0.0)
    directional_hypothesis_protective_edge = float(hypothesis_state.get("directional_hypothesis_protective_edge", 0.0) or 0.0)
    directional_hypothesis_missed_edge = float(hypothesis_state.get("directional_hypothesis_missed_edge", 0.0) or 0.0)
    spacetime_state = _build_spacetime_regulation_state(dict(getattr(bot, "temporal_perception_state", {}) or {}) if bot is not None else {}, dict(getattr(bot, "strategic_window_state", {}) or {}) if bot is not None else {}, locals())
    temporal_continuity = float(spacetime_state.get("temporal_continuity", 0.0) or 0.0)
    temporal_source_binding = float(spacetime_state.get("temporal_source_binding", 0.0) or 0.0)
    temporal_recurrence = float(spacetime_state.get("temporal_recurrence", 0.0) or 0.0)
    temporal_novelty = float(spacetime_state.get("temporal_novelty", 0.0) or 0.0)
    temporal_afterimage = float(spacetime_state.get("temporal_afterimage", 0.0) or 0.0)
    temporal_decay = float(spacetime_state.get("temporal_decay", 0.0) or 0.0)
    temporal_context_depth = float(spacetime_state.get("temporal_context_depth", 0.0) or 0.0)
    mcm_spacetime_depth = float(spacetime_state.get("mcm_spacetime_depth", 0.0) or 0.0)
    memory_experience_depth = float(spacetime_state.get("memory_experience_depth", 0.0) or 0.0)
    future_projection_depth = float(spacetime_state.get("future_projection_depth", 0.0) or 0.0)
    temporal_self_location = float(spacetime_state.get("temporal_self_location", 0.0) or 0.0)
    temporal_self_consistency = float(spacetime_state.get("temporal_self_consistency", 0.0) or 0.0)
    perception_sequence_coherence = float(spacetime_state.get("perception_sequence_coherence", 0.0) or 0.0)
    memory_time_distance = float(spacetime_state.get("memory_time_distance", 1.0) or 1.0)
    area_afterimage = float(spacetime_state.get("area_afterimage", 0.0) or 0.0)
    spacetime_unlocated_pressure = float(spacetime_state.get("spacetime_unlocated_pressure", 0.0) or 0.0)
    spacetime_memory_bearing = float(spacetime_state.get("spacetime_memory_bearing", 0.0) or 0.0)
    spacetime_future_bearing = float(spacetime_state.get("spacetime_future_bearing", 0.0) or 0.0)
    spacetime_regulation_support = float(spacetime_state.get("spacetime_regulation_support", 0.0) or 0.0)
    spacetime_reflection_need = float(spacetime_state.get("spacetime_reflection_need", 0.0) or 0.0)
    temporal_self_location_state = str(spacetime_state.get("temporal_self_location_state", "unlocated_contact") or "unlocated_contact")
    temporal_binding_state = str(spacetime_state.get("temporal_binding_state", "unbound_moment") or "unbound_moment")
    spacetime_regulation_state = str(spacetime_state.get("spacetime_regulation_state", "spacetime_open") or "spacetime_open")
    experience_effort_state = _build_experience_effort_feedback_state(dict(getattr(bot, "last_experience_packet_feedback", {}) or {}) if bot is not None else {}, locals())
    previous_packet_process_reward = float(experience_effort_state.get("previous_packet_process_reward", 0.0) or 0.0)
    previous_packet_bearing_quality = float(experience_effort_state.get("previous_packet_bearing_quality", 0.0) or 0.0)
    previous_packet_inner_outer_fit = float(experience_effort_state.get("previous_packet_inner_outer_fit", 0.0) or 0.0)
    previous_packet_repetition_potential = float(experience_effort_state.get("previous_packet_repetition_potential", 0.0) or 0.0)
    previous_packet_curiosity_pull = float(experience_effort_state.get("previous_packet_curiosity_pull", 0.0) or 0.0)
    previous_packet_reorganization_need = float(experience_effort_state.get("previous_packet_reorganization_need", 0.0) or 0.0)
    previous_constructive_stimulation = float(experience_effort_state.get("previous_constructive_stimulation", 0.0) or 0.0)
    previous_constructive_dopamine = float(experience_effort_state.get("previous_constructive_dopamine", 0.0) or 0.0)
    previous_stabilizing_serotonin = float(experience_effort_state.get("previous_stabilizing_serotonin", 0.0) or 0.0)
    engaged_effort = float(experience_effort_state.get("engaged_effort", 0.0) or 0.0)
    effort_reorganization_pressure = float(experience_effort_state.get("effort_reorganization_pressure", 0.0) or 0.0)
    pre_action_reorganization_pressure = float(experience_effort_state.get("pre_action_reorganization_pressure", 0.0) or 0.0)
    pre_action_context_selectivity = float(experience_effort_state.get("pre_action_context_selectivity", 0.0) or 0.0)
    effort_learning_pull = float(experience_effort_state.get("effort_learning_pull", 0.0) or 0.0)
    previous_packet_label = str(experience_effort_state.get("previous_packet_label", "-") or "-")
    effort_state = str(experience_effort_state.get("effort_state", "settled_effort") or "settled_effort")
    field_bearing_support = float(experience_effort_state.get("field_bearing_support", field_bearing_support) or 0.0)
    action_readiness_from_field = float(experience_effort_state.get("action_readiness_from_field", experience_effort_state.get("field_action_support", action_readiness_from_field)) or 0.0)
    field_action_support = action_readiness_from_field
    action_clearance = float(experience_effort_state.get("action_clearance", action_clearance) or 0.0)
    act_watch_readiness = float(experience_effort_state.get("act_watch_readiness", act_watch_readiness) or 0.0)
    field_observation_need = float(experience_effort_state.get("field_observation_need", field_observation_need) or 0.0)
    field_replan_pressure = float(experience_effort_state.get("field_replan_pressure", field_replan_pressure) or 0.0)
    action_inhibition = float(experience_effort_state.get("action_inhibition", action_inhibition) or 0.0)
    diffuse_open_state = _build_diffuse_open_development_state(locals())
    diffuse_open_development_pressure = float(diffuse_open_state.get("diffuse_open_development_pressure", 0.0) or 0.0)
    posture_development_hint = str(diffuse_open_state.get("posture_development_hint", "stable_posture") or "stable_posture")
    field_observation_need = float(diffuse_open_state.get("field_observation_need", field_observation_need) or 0.0)
    field_replan_pressure = float(diffuse_open_state.get("field_replan_pressure", field_replan_pressure) or 0.0)
    action_inhibition = float(diffuse_open_state.get("action_inhibition", action_inhibition) or 0.0)
    action_clearance = float(diffuse_open_state.get("action_clearance", action_clearance) or 0.0)
    act_watch_readiness = float(diffuse_open_state.get("act_watch_readiness", act_watch_readiness) or 0.0)
    open_hypothesis_mutation_state = _apply_open_hypothesis_mutation_state(locals())
    field_observation_need = float(open_hypothesis_mutation_state.get("field_observation_need", field_observation_need) or 0.0)
    field_replan_pressure = float(open_hypothesis_mutation_state.get("field_replan_pressure", field_replan_pressure) or 0.0)
    action_inhibition = float(open_hypothesis_mutation_state.get("action_inhibition", action_inhibition) or 0.0)
    action_clearance = float(open_hypothesis_mutation_state.get("action_clearance", action_clearance) or 0.0)
    regulated_courage = float(open_hypothesis_mutation_state.get("regulated_courage", regulated_courage) or 0.0)
    act_watch_readiness = float(open_hypothesis_mutation_state.get("act_watch_readiness", act_watch_readiness) or 0.0)
    field_bearing_support = float(open_hypothesis_mutation_state.get("field_bearing_support", field_bearing_support) or 0.0)
    action_readiness_from_field = float(open_hypothesis_mutation_state.get("action_readiness_from_field", open_hypothesis_mutation_state.get("field_action_support", action_readiness_from_field)) or 0.0)
    field_action_support = action_readiness_from_field
    positive_expansion_pressure = _clip01(_num(felt, thought, processing, key="positive_expansion_pressure"))
    negative_contraction_pressure = _clip01(_num(felt, thought, processing, key="negative_contraction_pressure"))
    positive_overextension = _clip01(_num(felt, thought, processing, key="positive_overextension"))
    positive_return_pressure = _clip01(_num(felt, thought, processing, key="positive_return_pressure"))
    positive_zero_point_signal = _clip01(_num(felt, thought, processing, key="positive_zero_point_regulation"))
    pre_action_state = _build_pre_action_decision_state(
        {
            **locals(),
            "positive_zero_point_regulation": bool(positive_zero_point_regulation or positive_zero_point_signal >= 0.50),
        },
        config=Config,
    )
    positive_zero_point_regulation = bool(positive_zero_point_regulation or positive_zero_point_signal >= 0.50)
    allow_observe = bool(pre_action_state.get("allow_observe", False))
    allow_ruminate = bool(pre_action_state.get("allow_ruminate", False))
    allow_plan = bool(pre_action_state.get("allow_plan", False))
    allow_block = bool(pre_action_state.get("allow_block", False))
    pre_action_phase = str(pre_action_state.get("pre_action_phase", "hold") or "hold")
    rejection_reason = str(pre_action_state.get("rejection_reason", "-") or "-")
    pre_action_pressure_trace = dict(pre_action_state.get("pre_action_pressure_trace", {}) or {})
    dopamine_tone = float(neurochemical_state.get("dopamine_tone", 0.0) or 0.0)
    gaba_inhibition = float(neurochemical_state.get("gaba_inhibition", 0.0) or 0.0)
    acetylcholine_focus = float(neurochemical_state.get("acetylcholine_focus", 0.0) or 0.0)
    serotonin_stability = float(neurochemical_state.get("serotonin_stability", 0.0) or 0.0)
    cortisol_load = float(neurochemical_state.get("cortisol_load", 0.0) or 0.0)
    endorphin_relief = float(neurochemical_state.get("endorphin_relief", 0.0) or 0.0)
    world_shift_evidence = float(neurochemical_state.get("world_shift_evidence", 0.0) or 0.0)
    serotonin_carryover_risk = float(neurochemical_state.get("serotonin_carryover_risk", 0.0) or 0.0)
    emotional_decoupling = float(neurochemical_state.get("emotional_decoupling", 0.0) or 0.0)
    reactive_nervous_drive = float(neurochemical_state.get("reactive_nervous_drive", 0.0) or 0.0)
    nervous_system_overload = float(neurochemical_state.get("nervous_system_overload", 0.0) or 0.0)
    escape_action_drive = float(neurochemical_state.get("escape_action_drive", 0.0) or 0.0)
    shock_response_risk = float(neurochemical_state.get("shock_response_risk", 0.0) or 0.0)
    mcm_reflective_bearing = float(neurochemical_state.get("mcm_reflective_bearing", mcm_reflective_bearing) or 0.0)
    mcm_reflective_pressure = float(neurochemical_state.get("mcm_reflective_pressure", mcm_reflective_pressure) or 0.0)
    mcm_reflective_coupling_load = float(neurochemical_state.get("mcm_reflective_coupling_load", mcm_reflective_coupling_load) or 0.0)
    mcm_reflective_tension = float(neurochemical_state.get("mcm_reflective_tension", mcm_reflective_tension) or 0.0)
    positive_expansion_pressure = max(
        float(positive_expansion_pressure),
        float(neurochemical_state.get("positive_expansion_pressure", 0.0) or 0.0),
    )
    negative_contraction_pressure = max(
        float(negative_contraction_pressure),
        float(neurochemical_state.get("negative_contraction_pressure", 0.0) or 0.0),
    )
    positive_overextension = max(
        float(positive_overextension),
        float(neurochemical_state.get("positive_overextension", 0.0) or 0.0),
    )
    positive_return_pressure = max(
        float(positive_return_pressure),
        float(neurochemical_state.get("positive_return_pressure", 0.0) or 0.0),
    )
    mcm_axis_displacement = max(-1.0, min(1.0, float(positive_expansion_pressure - negative_contraction_pressure)))
    mcm_axis_field_position = max(-3.0, min(3.0, mcm_axis_displacement * 3.0))
    mcm_axis_tension = _clip01(max(positive_expansion_pressure, negative_contraction_pressure))
    mcm_axis_label_pressures = {
        "++": _clip01(max(0.0, mcm_axis_displacement) * positive_expansion_pressure),
        "+": _clip01(max(0.0, mcm_axis_displacement) * (1.0 - abs(mcm_axis_displacement - 0.32))),
        "0": _clip01(1.0 - abs(mcm_axis_displacement) - (mcm_axis_tension * 0.18)),
        "-": _clip01(max(0.0, -mcm_axis_displacement) * (1.0 - abs(mcm_axis_displacement + 0.32))),
        "--": _clip01(max(0.0, -mcm_axis_displacement) * negative_contraction_pressure),
    }
    mcm_axis_state = max(mcm_axis_label_pressures, key=mcm_axis_label_pressures.get)
    if positive_return_pressure > 0.0:
        field_observation_need = _clip01(field_observation_need + (positive_return_pressure * 0.030))
        act_watch_readiness = _clip01(act_watch_readiness + (positive_return_pressure * 0.025))
        action_inhibition = _clip01(action_inhibition + (positive_return_pressure * 0.025))
        action_clearance = _clip01(action_clearance - (positive_return_pressure * 0.018))
        regulated_courage = _clip01(regulated_courage - (positive_overextension * 0.018))
        inner_outer_reflection = _clip01(inner_outer_reflection + (positive_return_pressure * 0.025))
        perceptual_distance = _clip01(perceptual_distance + (positive_return_pressure * 0.020))
        conscious_perception_state["inner_outer_reflection"] = float(inner_outer_reflection)
        conscious_perception_state["perceptual_distance"] = float(perceptual_distance)

    field_overcoupling = max(field_attachment, field_perception_strain, felt_afterimage)
    nervous_overload_reflection_need = max(
        0.0,
        min(
            1.0,
            (shock_response_risk * 0.38)
            + (nervous_system_overload * 0.24)
            + (escape_action_drive * 0.18)
            + (max(0.0, 0.34 - emotional_decoupling) * 0.16)
            + (field_overcoupling * 0.10),
        ),
    )
    active_context_self_certainty = _clip01(
        active_context_activation
        * ((active_context_support + active_context_bearing) * 0.5)
        * max(0.0, 1.0 - active_context_conflict)
    )
    nervous_context_overcoupling = _clip01(
        active_context_self_certainty
        * (
            (nervous_system_overload * 0.34)
            + (escape_action_drive * 0.28)
            + (shock_response_risk * 0.26)
            + (max(0.0, 0.24 - emotional_decoupling) * 0.20)
        )
    )
    own_field_identity_strength = _clip01(
        (inner_outer_alignment * 0.20)
        + (perceptual_distance * 0.14)
        + (reflective_distance * 0.10)
        + (active_context_self_certainty * 0.16)
        + (form_symbol_learning_trust * 0.10)
        + (form_symbol_development_quality * 0.08)
        + (temporal_self_consistency * 0.10)
        + (memory_orientation * 0.08)
        + (emotional_decoupling * 0.08)
        - (semantic_shift_pressure * 0.10)
        - (visual_resonance_unbound * 0.06)
        - (nervous_context_overcoupling * 0.06)
    )
    foreign_semantic_pressure = _clip01(
        (semantic_shift_pressure * 0.24)
        + (visual_resonance_unbound * 0.14)
        + (world_shift_evidence * 0.12)
        + (orientation_gap * 0.12)
        + (blind_thinking_load * 0.10)
        + (field_perception_strain * 0.10)
        + (nervous_context_overcoupling * 0.10)
        + (max(0.0, 0.34 - known_form_support) * 0.10)
        - (form_symbol_containment * 0.08)
        - (memory_orientation * 0.06)
    )
    adopted_language_pressure = _clip01(
        (foreign_semantic_pressure * 0.32)
        + (active_context_activation * 0.14)
        + (max(0.0, 0.40 - form_symbol_development_quality) * 0.18)
        + (max(0.0, 0.38 - form_symbol_learning_trust) * 0.14)
        + (semantic_shift_pressure * 0.12)
        - (own_field_identity_strength * 0.10)
    )
    self_foreign_boundary_clarity = _clip01(
        (inner_outer_alignment * 0.22)
        + (perceptual_distance * 0.18)
        + (temporal_source_binding * 0.14)
        + (emotional_decoupling * 0.12)
        + (form_symbol_object_distance * 0.10)
        + (background_containment * 0.10)
        + (reflective_distance * 0.10)
        - (nervous_context_overcoupling * 0.10)
        - (field_attachment * 0.08)
        - (adopted_language_pressure * 0.06)
    )
    semantic_origin_conflict = _clip01(
        (foreign_semantic_pressure * 0.30)
        + (adopted_language_pressure * 0.24)
        + (max(0.0, 0.42 - self_foreign_boundary_clarity) * 0.24)
        + (max(0.0, active_context_self_certainty - own_field_identity_strength) * 0.14)
        - (own_field_identity_strength * 0.08)
    )
    own_vs_foreign_margin = max(-1.0, min(1.0, float(own_field_identity_strength - foreign_semantic_pressure)))
    borrowed_vs_own_margin = max(-1.0, min(1.0, float(adopted_language_pressure - own_field_identity_strength)))
    boundary_support_margin = max(-1.0, min(1.0, float(self_foreign_boundary_clarity - semantic_origin_conflict)))
    semantic_origin_pressures = {
        "own_field_origin": _clip01((own_field_identity_strength * 0.50) + (max(0.0, own_vs_foreign_margin) * 0.26) + ((1.0 - semantic_origin_conflict) * 0.24)),
        "borrowed_analogy_watch": _clip01((borrowed_vs_own_margin * 0.42) + ((1.0 - self_foreign_boundary_clarity) * 0.38) + (adopted_language_pressure * 0.20)),
        "mixed_translation_zone": _clip01((min(own_field_identity_strength, foreign_semantic_pressure) * 0.46) + ((1.0 - abs(own_vs_foreign_margin)) * 0.34)),
        "differentiated_contact": _clip01((self_foreign_boundary_clarity * 0.50) + ((boundary_support_margin + 1.0) * 0.25)),
        "unlocated_semantic_contact": _clip01((semantic_origin_conflict * 0.34) + (foreign_semantic_pressure * 0.22) + ((1.0 - self_foreign_boundary_clarity) * 0.20)),
    }
    semantic_origin_state = max(semantic_origin_pressures, key=semantic_origin_pressures.get)

    if nervous_context_overcoupling > 0.0:
        nervous_overload_reflection_need = _clip01(
            nervous_overload_reflection_need
            + (nervous_context_overcoupling * 0.18)
        )
        field_observation_need = _clip01(
            field_observation_need
            + (nervous_context_overcoupling * 0.060)
        )
        act_watch_readiness = _clip01(
            act_watch_readiness
            + (nervous_context_overcoupling * 0.050)
        )
        action_inhibition = _clip01(
            action_inhibition
            + (nervous_context_overcoupling * 0.070)
        )
        action_clearance = _clip01(
            action_clearance
            - (nervous_context_overcoupling * 0.050)
        )
        regulated_courage = _clip01(
            regulated_courage
            - (nervous_context_overcoupling * 0.050)
        )
        perceptual_distance = _clip01(
            perceptual_distance
            + (nervous_context_overcoupling * 0.060)
        )
        reflective_distance = _clip01(
            reflective_distance
            + (nervous_context_overcoupling * 0.055)
        )
        inner_outer_reflection = _clip01(
            inner_outer_reflection
            + (nervous_context_overcoupling * 0.050)
        )
        conscious_perception_state["perceptual_distance"] = float(perceptual_distance)
        conscious_perception_state["reflective_distance"] = float(reflective_distance)
        conscious_perception_state["inner_outer_reflection"] = float(inner_outer_reflection)
    if semantic_origin_conflict > 0.0:
        field_observation_need = _clip01(field_observation_need + (semantic_origin_conflict * 0.035))
        act_watch_readiness = _clip01(act_watch_readiness + (semantic_origin_conflict * 0.030))
        self_reflection_boost = semantic_origin_conflict * 0.035
    else:
        self_reflection_boost = 0.0
    positive_zero_point_regulation = bool(
        positive_zero_point_regulation
        or (
            positive_return_pressure >= 0.30
            and field_action_support < 0.46
            and structure_action_bearing < 0.50
            and decision_strength < 1.28
        )
    )
    zero_point_value = 1.0 if bool(zero_point_regulation or positive_zero_point_regulation) else 0.0
    reflective_posture_value = 1.0 if inner_posture_label == "reflective" else 0.0
    reflective_perception_value = 1.0 if conscious_label == "reflective_check" else 0.0
    subconscious_field_pressure = max(
        0.0,
        min(
            1.0,
            (field_perception_pressure * 0.20)
            + (field_perception_strain * 0.14)
            + (stimulus_field_effect * 0.14)
            + (inner_impact_trace * 0.12)
            + (perceived_field_change * 0.12)
            + (world_shift_evidence * 0.10)
            + (visual_resonance_unbound * 0.08)
            + (reactive_nervous_drive * 0.10),
        ),
    )
    subconscious_habituation = max(
        0.0,
        min(
            1.0,
            (uncertainty_familiarity * 0.18)
            + (variant_bearing_memory * 0.16)
            + (known_form_support * 0.16)
            + (route_familiarity * 0.14)
            + (form_symbol_containment * 0.14)
            + (form_symbol_field_decoupling * 0.12)
            + (gaba_inhibition * 0.10),
        ),
    )
    subconscious_filter_strength = max(
        0.0,
        min(
            1.0,
            (background_containment * 0.18)
            + (symbolic_regulation * 0.16)
            + (subconscious_habituation * 0.16)
            + (form_symbol_object_distance * 0.12)
            + (form_symbol_field_decoupling * 0.12)
            + (emotional_decoupling * 0.10)
            + (serotonin_stability * 0.08)
            + (gaba_inhibition * 0.08),
        ),
    )
    subconscious_buffering = max(
        0.0,
        min(
            1.0,
            subconscious_field_pressure
            * (0.34 + subconscious_filter_strength * 0.54 + subconscious_habituation * 0.20)
            * max(0.15, 1.0 - field_attachment * 0.34),
        ),
    )
    conscious_selection_pressure = max(
        0.0,
        min(
            1.0,
            (object_contact_depth * 0.17)
            + (selective_attention * 0.15)
            + (visual_grounding_need * 0.13)
            + (visual_action_uncertainty * 0.11)
            + (semantic_shift_pressure * 0.10)
            + (transfer_maturity_gap * 0.10)
            + (field_observation_need * 0.10)
            + (curiosity_tone * 0.07)
            + (felt_afterimage * 0.07),
        ),
    )
    conscious_workspace_focus = max(
        0.0,
        min(
            1.0,
            (selective_attention * 0.16)
            + (inner_outer_reflection * 0.15)
            + (perceptual_distance * 0.14)
            + (visual_grounding_strength * 0.14)
            + (interpretation_quality * 0.14)
            + (memory_orientation * 0.10)
            + (perception_sequence_coherence * 0.08)
            + (acetylcholine_focus * 0.09)
            + (release_capacity * 0.08),
        ),
    )
    conscious_workspace_load = max(
        0.0,
        min(
            1.0,
            (conscious_selection_pressure * 0.24)
            + (processing_load * 0.15)
            + (cognitive_load * 0.14)
            + (orientation_gap * 0.12)
            + (temporal_novelty * 0.08)
            + (temporal_decay * 0.06)
            + (field_attachment * 0.10)
            + (arousal_load * 0.10)
            + (blind_thinking_load * 0.09)
            + (max(0.0, subconscious_field_pressure - subconscious_buffering) * 0.06),
        ),
    )
    conscious_gate_balance = max(
        0.0,
        min(
            1.0,
            (conscious_workspace_focus * 0.36)
            + (subconscious_filter_strength * 0.22)
            + (temporal_source_binding * 0.10)
            + (temporal_self_consistency * 0.08)
            + (release_capacity * 0.14)
            + (inner_outer_alignment * 0.12)
            + (emotional_decoupling * 0.10)
            + (subconscious_buffering * 0.06)
            - (conscious_workspace_load * 0.20),
        ),
    )
    subconscious_leakage = max(
        0.0,
        min(
            1.0,
            (subconscious_field_pressure * 0.38)
            + (conscious_selection_pressure * 0.20)
            + (field_overcoupling * 0.16)
            + (reactive_nervous_drive * 0.14)
            + (felt_afterimage * 0.12)
            - (subconscious_filter_strength * 0.24)
            - (subconscious_buffering * 0.16)
            - (conscious_workspace_focus * 0.10),
        ),
    )
    subconscious_afterimage_depth = _clip01(
        (felt_afterimage * 0.26)
        + (temporal_afterimage * 0.26)
        + (area_afterimage * 0.18)
        + (max(0.0, temporal_decay - temporal_source_binding) * 0.12)
        + ((1.0 if temporal_self_location_state == "afterimage_trace" else 0.0) * 0.08)
        + ((1.0 if temporal_binding_state == "afterimage_contact" else 0.0) * 0.06)
        + (subconscious_field_pressure * 0.08)
    )
    compressed_afterimage_depth = _clip01(subconscious_afterimage_depth ** 0.72)
    subconscious_afterimage_pressure = _clip01(
        compressed_afterimage_depth
        * (
            0.28
            + (subconscious_leakage * 0.26)
            + (spacetime_reflection_need * 0.18)
            + (max(0.0, 0.42 - temporal_source_binding) * 0.16)
            + (max(0.0, 0.34 - subconscious_filter_strength) * 0.12)
        )
    )
    subconscious_afterimage_bearing = _clip01(
        (subconscious_buffering * 0.22)
        + (subconscious_filter_strength * 0.16)
        + (temporal_context_depth * 0.16)
        + (spacetime_memory_bearing * 0.14)
        + (perception_sequence_coherence * 0.12)
        + (release_capacity * 0.10)
        + (emotional_decoupling * 0.08)
        - (subconscious_afterimage_pressure * 0.16)
    )
    subconscious_afterimage_clarity = _clip01(
        (temporal_source_binding * 0.24)
        + (perception_sequence_coherence * 0.18)
        + (conscious_gate_balance * 0.16)
        + (reflective_distance * 0.12)
        + (inner_outer_alignment * 0.10)
        + (emotional_decoupling * 0.10)
        - (spacetime_unlocated_pressure * 0.14)
    )
    subconscious_afterimage_release = _clip01(
        (release_capacity * 0.24)
        + (subconscious_filter_strength * 0.20)
        + (subconscious_buffering * 0.16)
        + (emotional_decoupling * 0.14)
        + (subconscious_afterimage_clarity * 0.14)
        - (subconscious_afterimage_pressure * 0.22)
    )
    subconscious_afterimage_reflection_pull = _clip01(
        subconscious_afterimage_pressure
        * max(0.0, 1.0 - subconscious_afterimage_clarity)
        * max(0.0, 1.0 - subconscious_afterimage_release)
    )
    if subconscious_afterimage_reflection_pull > 0.0:
        field_observation_need = _clip01(field_observation_need + (subconscious_afterimage_reflection_pull * 0.045))
        act_watch_readiness = _clip01(act_watch_readiness + (subconscious_afterimage_reflection_pull * 0.035))
        action_clearance = _clip01(action_clearance - (subconscious_afterimage_reflection_pull * 0.025))

    return_strength = max(
        0.0,
        min(
            1.0,
            (field_perception_stability * 0.16)
            + (field_perception_support * 0.14)
            + (release_capacity * 0.15)
            + (calm_tone * 0.12)
            + (experience_regulation * 0.11)
            + (action_clearance * 0.10)
            + (serotonin_stability * 0.10)
            + (endorphin_relief * 0.06)
            + (subconscious_buffering * 0.08)
            + (zero_point_value * 0.08)
            - (field_perception_instability * 0.08)
            - (orientation_gap * 0.06)
            - (reactive_nervous_drive * 0.06),
        ),
    )
    integration_capacity = max(
        0.0,
        min(
            1.0,
            (interpretation_quality * 0.18)
            + (memory_orientation * 0.14)
            + (route_familiarity * 0.11)
            + (temporal_context_depth * 0.10)
            + (mcm_spacetime_depth * 0.06)
            + (memory_experience_depth * 0.04)
            + (future_projection_depth * 0.04)
            + (perception_sequence_coherence * 0.08)
            + (inner_outer_alignment * 0.14)
            + (previous_packet_process_reward * 0.10)
            + (previous_packet_bearing_quality * 0.09)
            + (form_symbol_contact_maturity * 0.10)
            + (known_form_support * 0.08)
            + (selective_attention * 0.06)
            + (conscious_gate_balance * 0.08)
            - (previous_packet_reorganization_need * 0.08)
            - (semantic_shift_pressure * 0.05)
            - (transfer_maturity_gap * 0.05),
        ),
    )
    variance_regulation = max(
        0.0,
        min(
            1.0,
            (variant_learning_pressure * 0.10)
            + (variant_bearing_memory * 0.12)
            + (interpretation_quality * 0.12)
            + (temporal_continuity * 0.08)
            + (temporal_recurrence * 0.07)
            + (field_perception_stability * 0.12)
            + (action_inhibition * 0.12)
            + (release_capacity * 0.12)
            + (inner_outer_alignment * 0.10)
            + (gaba_inhibition * 0.10)
            + (emotional_decoupling * 0.10)
            + (subconscious_filter_strength * 0.10)
            - (field_perception_fragmentation * 0.10)
            - (arousal_load * 0.08)
            - (blind_thinking_load * 0.06),
        ),
    )
    load_tolerance = max(
        0.0,
        min(
            1.0,
            (load_bearing_capacity * 0.18)
            + (field_perception_support * 0.12)
            + (serotonin_stability * 0.12)
            + (gaba_inhibition * 0.10)
            + (action_inhibition * 0.10)
            + (calm_tone * 0.12)
            + (protective_courage * 0.08)
            + (return_strength * 0.10)
            + (subconscious_buffering * 0.08)
            - (cortisol_load * 0.10)
            - (processing_load * 0.08)
            - (cognitive_load * 0.08)
            - (fatigue_tone * 0.08),
        ),
    )
    impulse_control = max(
        0.0,
        min(
            1.0,
            (action_inhibition * 0.18)
            + (release_capacity * 0.14)
            + (perceptual_distance * 0.13)
            + (regulated_courage * 0.10)
            + (gaba_inhibition * 0.12)
            + (reflective_distance * 0.12)
            + (pre_action_context_selectivity * 0.09)
            + (emotional_decoupling * 0.08)
            + (conscious_gate_balance * 0.08)
            - (plan_pressure * 0.10)
            - (reactive_nervous_drive * 0.10)
            - (field_perception_pressure * 0.06),
        ),
    )
    frustration_tolerance = max(
        0.0,
        min(
            1.0,
            (return_strength * 0.16)
            + (integration_capacity * 0.15)
            + (effort_learning_pull * 0.12)
            + (pre_action_reorganization_pressure * 0.08)
            + (calm_tone * 0.10)
            + (serotonin_stability * 0.10)
            + (endorphin_relief * 0.08)
            + (previous_packet_process_reward * 0.08)
            - (fatigue_tone * 0.10)
            - (cortisol_load * 0.10)
            - (reactive_nervous_drive * 0.08)
            - (blind_thinking_load * 0.06),
        ),
    )
    protective_distance_regulation = max(
        0.0,
        min(
            1.0,
            (protective_width_regulation * 0.15)
            + (perceptual_distance * 0.16)
            + (release_capacity * 0.15)
            + (max(0.0, 1.0 - temporal_decay) * 0.08)
            + (emotional_decoupling * 0.13)
            + (visual_rational_observation_support * 0.10)
            + (background_containment * 0.09)
            + (form_symbol_field_decoupling * 0.09)
            + (reflective_distance * 0.10)
            + (subconscious_filter_strength * 0.08)
            - (field_attachment * 0.12)
            - (max(0.0, object_contact_depth - 0.62) * 0.08)
            - (field_overcoupling * 0.06),
        ),
    )
    self_reflection_regulator = max(
        0.0,
        min(
            1.0,
            (inner_outer_alignment * 0.16)
            + (inner_outer_reflection * 0.14)
            + (reflective_distance * 0.14)
            + (perceptual_distance * 0.10)
            + (interpretation_quality * 0.12)
            + (selective_attention * 0.10)
            + (reflective_posture_value * 0.10)
            + (reflective_perception_value * 0.08)
            + (acetylcholine_focus * 0.06)
            + (conscious_workspace_focus * 0.08)
            + (nervous_overload_reflection_need * 0.08)
            + (self_reflection_boost * 0.80)
            - (arousal_load * 0.08)
            - (blind_thinking_load * 0.06),
        ),
    )
    if spacetime_reflection_need > 0.0:
        field_observation_need = _clip01(field_observation_need + (spacetime_reflection_need * 0.055))
        field_replan_pressure = _clip01(field_replan_pressure + (spacetime_reflection_need * 0.035))
        act_watch_readiness = _clip01(act_watch_readiness + (spacetime_reflection_need * 0.050))
        perceptual_distance = _clip01(perceptual_distance + (spacetime_reflection_need * 0.035))
        reflective_distance = _clip01(reflective_distance + (spacetime_reflection_need * 0.040))
        self_reflection_regulator = _clip01(self_reflection_regulator + (spacetime_reflection_need * 0.045))
        action_inhibition = _clip01(action_inhibition + (spacetime_unlocated_pressure * 0.030))
        action_clearance = _clip01(action_clearance - (spacetime_unlocated_pressure * 0.020))
        conscious_perception_state["perceptual_distance"] = float(perceptual_distance)
        conscious_perception_state["reflective_distance"] = float(reflective_distance)
    if spacetime_regulation_support > 0.0:
        integration_capacity = _clip01(integration_capacity + (spacetime_regulation_support * 0.035))
        variance_regulation = _clip01(variance_regulation + (spacetime_regulation_support * 0.025))
        load_tolerance = _clip01(load_tolerance + (spacetime_regulation_support * 0.020))
        if spacetime_regulation_state in ("memory_depth_bearing", "present_depth_bearing"):
            action_clearance = _clip01(action_clearance + (spacetime_regulation_support * 0.025))
            action_readiness_from_field = _clip01(action_readiness_from_field + (spacetime_regulation_support * 0.020))
            field_action_support = action_readiness_from_field
    distance_regulation = max(
        0.0,
        min(
            1.0,
            (perceptual_distance * 0.17)
            + (release_capacity * 0.16)
            + (background_containment * 0.12)
            + (reflective_distance * 0.14)
            + (emotional_decoupling * 0.12)
            + (form_symbol_field_decoupling * 0.10)
            + (protective_distance_regulation * 0.11)
            + (subconscious_buffering * 0.08)
            - (field_attachment * 0.12)
            - (felt_afterimage * 0.08)
            - (serotonin_carryover_risk * 0.08),
        ),
    )
    metaregulator_balance = max(
        0.0,
        min(
            1.0,
            (
                return_strength
                + integration_capacity
                + variance_regulation
                + load_tolerance
                + impulse_control
                + frustration_tolerance
                + protective_distance_regulation
                + self_reflection_regulator
                + distance_regulation
            )
            / 9.0,
        ),
    )
    regulatory_second_order_load = max(
        0.0,
        min(
            1.0,
            ((1.0 - metaregulator_balance) * 0.42)
            + (effort_reorganization_pressure * 0.14)
            + (pre_action_reorganization_pressure * 0.14)
            + (field_perception_strain * 0.10)
            + (arousal_load * 0.08)
            + (fatigue_tone * 0.08)
            + (field_overcoupling * 0.04),
        ),
    )
    regulatory_second_order_load = max(
        0.0,
        min(
            1.0,
            regulatory_second_order_load
            - (subconscious_buffering * 0.12)
            - (conscious_gate_balance * 0.08)
            + (subconscious_leakage * 0.10)
            + (conscious_workspace_load * 0.05),
        ),
    )
    regulatory_second_order_load = max(
        0.0,
        min(
            1.0,
            regulatory_second_order_load
            + (nervous_overload_reflection_need * 0.08)
            + (shock_response_risk * 0.05)
            + (nervous_context_overcoupling * 0.06),
        ),
    )
    regulatory_second_order_load = _clip01(
        regulatory_second_order_load
        + (spacetime_unlocated_pressure * 0.035)
        + (spacetime_reflection_need * 0.030)
        - (spacetime_regulation_support * 0.035)
    )
    perception_event_strength = _clip01(
        (structure_quality * 0.18)
        + (context_confidence * 0.12)
        + (visual_clarity * 0.12)
        + (visual_reflective_coherence * 0.10)
        + (field_perception_clarity * 0.12)
        + (field_perception_focus * 0.08)
        + (form_symbol_containment * 0.10)
        + (form_symbol_development_quality * 0.08)
        + (open_hypothesis_confirmation_weight * 0.06)
        + (form_mcm_family_maturity * 0.04)
        - (visual_blindness * 0.08)
        - (field_perception_fragmentation * 0.06)
    )
    thought_load_pressure = _clip01(
        (cognitive_load * 0.18)
        + (blind_thinking_load * 0.22)
        + (rumination_depth * 0.18)
        + (open_hypothesis_reifung_pressure * 0.12)
        + (open_hypothesis_learning_charge * 0.10)
        + (open_hypothesis_reality_check_need * 0.10)
        + (regulatory_second_order_load * 0.10)
    )
    thought_efficiency_support = _clip01(
        (perception_event_strength * 0.26)
        + (open_hypothesis_confirmation_weight * 0.16)
        + (thought_alignment * 0.14)
        + (memory_orientation * 0.12)
        + (form_symbol_containment * 0.10)
        + (spacetime_regulation_support * 0.08)
        + (inner_outer_alignment * 0.08)
        + (form_mcm_family_trust * 0.06)
    )
    thought_overprocessing_signal = _clip01(
        (thought_load_pressure * 0.48)
        + (max(0.0, 0.34 - perception_event_strength) * 0.22)
        + (max(0.0, open_hypothesis_reifung_pressure - open_hypothesis_confirmation_weight) * 0.18)
        + (max(0.0, blind_thinking_load - memory_orientation) * 0.12)
        - (thought_efficiency_support * 0.22)
    )
    thought_economy_need = _clip01(
        (thought_overprocessing_signal * 0.42)
        + (max(0.0, thought_load_pressure - thought_efficiency_support) * 0.30)
        + (max(0.0, 0.40 - perception_event_strength) * 0.16)
        + (field_perception_strain * 0.08)
        + (fatigue_tone * 0.04)
    )
    thought_release_pressure = _clip01(
        (thought_overprocessing_signal * 0.32)
        + (max(0.0, open_hypothesis_reality_check_need - open_hypothesis_confirmation_weight) * 0.22)
        + (max(0.0, open_hypothesis_learning_charge - hypothesis_trust) * 0.18)
        + (max(0.0, 0.36 - perception_event_strength) * 0.14)
        - (form_mcm_family_trust * 0.08)
        - (thought_efficiency_support * 0.06)
    )
    if thought_economy_need > 0.0:
        regulatory_second_order_load = _clip01(regulatory_second_order_load + (thought_overprocessing_signal * 0.070))
        field_observation_need = _clip01(field_observation_need + (thought_economy_need * 0.060) + (thought_release_pressure * 0.035))
        field_replan_pressure = _clip01(field_replan_pressure + (thought_release_pressure * 0.045))
        action_inhibition = _clip01(action_inhibition + (thought_overprocessing_signal * 0.035))
        action_clearance = _clip01(action_clearance - (thought_overprocessing_signal * 0.028))
        act_watch_readiness = _clip01(act_watch_readiness + (thought_economy_need * 0.040))
        perceptual_distance = _clip01(perceptual_distance + (thought_economy_need * 0.035))
        inner_outer_reflection = _clip01(inner_outer_reflection + (thought_release_pressure * 0.030))
        conscious_perception_state["perceptual_distance"] = float(perceptual_distance)
        conscious_perception_state["inner_outer_reflection"] = float(inner_outer_reflection)
    metaregulator_state_pressures = {
        "regulated_field": _clip01((metaregulator_balance * 0.44) + ((1.0 - regulatory_second_order_load) * 0.30) + ((1.0 - subconscious_leakage) * 0.26)),
        "positive_expansion_return": _clip01((positive_return_pressure * 0.54) + (positive_overextension * 0.46)),
        "spacetime_reflection": _clip01((spacetime_reflection_need * 0.58) + ((1.0 - spacetime_regulation_support) * 0.42)),
        "nervous_overload_reflection": _clip01((shock_response_risk * 0.42) + (nervous_overload_reflection_need * 0.58)),
        "context_overcoupling_reflection": _clip01((nervous_context_overcoupling * 0.46) + (nervous_overload_reflection_need * 0.54)),
        "subconscious_leakage": _clip01((subconscious_leakage * 0.56) + ((1.0 - protective_distance_regulation) * 0.44)),
        "low_distance_processing": _clip01((conscious_workspace_load * 0.48) + ((1.0 - distance_regulation) * 0.52)),
        "integration_strain": _clip01(((1.0 - integration_capacity) * 0.48) + (previous_packet_reorganization_need * 0.52)),
        "impulse_pressure": _clip01(((1.0 - impulse_control) * 0.54) + (plan_pressure * 0.46)),
        "tired_stabilization": _clip01((fatigue_tone * 0.36) + (serotonin_stability * 0.34) + (load_tolerance * 0.30)),
        "reflective_recovery": _clip01((reflective_perception_value * 0.52) + (self_reflection_regulator * 0.48)),
        "overcoupled_protection": _clip01(((1.0 - protective_distance_regulation) * 0.48) + (field_attachment * 0.52)),
        "thought_load_distance": _clip01((thought_overprocessing_signal * 0.58) + ((1.0 - thought_efficiency_support) * 0.42)),
        "regulatory_overload": _clip01(((1.0 - load_tolerance) * 0.34) + ((1.0 - variance_regulation) * 0.28) + (regulatory_second_order_load * 0.38)),
        "adaptive_watch": _clip01((field_observation_need * 0.22) + (act_watch_readiness * 0.18) + (conscious_gate_balance * 0.16)),
    }
    metaregulator_state = max(metaregulator_state_pressures, key=metaregulator_state_pressures.get)

    integration_strain_value = max(
        0.0,
        min(
            1.0,
            (max(0.0, 0.34 - integration_capacity) * 0.64)
            + (previous_packet_reorganization_need * 0.18)
            + (semantic_shift_pressure * 0.14)
            + (transfer_maturity_gap * 0.12)
            + (max(0.0, temporal_novelty - temporal_continuity) * 0.10)
            + (temporal_decay * 0.08)
            + (conscious_workspace_load * 0.10)
            + (max(0.0, subconscious_leakage - subconscious_buffering) * 0.10),
        ),
    )
    integration_sorting_need = max(
        0.0,
        min(
            1.0,
            (integration_strain_value * 0.28)
            + (orientation_gap * 0.18)
            + (blind_thinking_load * 0.14)
            + (conscious_selection_pressure * 0.12)
            + (field_observation_need * 0.10)
            + (max(0.0, 0.30 - conscious_workspace_focus) * 0.12)
            + (max(0.0, 0.24 - distance_regulation) * 0.06),
        ),
    )
    integration_reframe_pull = max(
        0.0,
        min(
            1.0,
            (integration_strain_value * 0.24)
            + (form_symbol_reframe_binding * 0.18)
            + (effort_learning_pull * 0.14)
            + (previous_packet_reorganization_need * 0.14)
            + (semantic_shift_pressure * 0.12)
            + (transfer_recovery_need * 0.10)
            + (reflective_distance * 0.08),
        ),
    )
    integration_memory_recall = max(
        0.0,
        min(
            1.0,
            (memory_orientation * 0.20)
            + (route_familiarity * 0.16)
            + (temporal_context_depth * 0.12)
            + (temporal_recurrence * 0.08)
            + (known_form_support * 0.14)
            + (variant_bearing_memory * 0.12)
            + (uncertainty_familiarity * 0.10)
            + (form_symbol_learning_trust * 0.10)
            + (subconscious_habituation * 0.10)
            - (memory_conflict * 0.10)
            - (orientation_gap * 0.06),
        ),
    )
    integration_contact_deepening = max(
        0.0,
        min(
            1.0,
            (integration_strain_value * 0.16)
            + (object_contact_depth * 0.16)
            + (contact_state_observe_bias * 2.0)
            + (form_symbol_contact_carefulness * 0.12)
            + (form_symbol_contact_maturity * 0.10)
            + (conscious_selection_pressure * 0.12)
            + (curiosity_tone * 0.10)
            + (integration_memory_recall * 0.10)
            - (subconscious_leakage * 0.08),
        ),
    )
    integration_response_strength = max(
        0.0,
        min(
            1.0,
            (integration_sorting_need * 0.28)
            + (integration_reframe_pull * 0.24)
            + (integration_memory_recall * 0.18)
            + (integration_contact_deepening * 0.18)
            + (conscious_gate_balance * 0.08)
            + (return_strength * 0.04),
        ),
    )
    integration_response_pressures = {
        "reframe_integration": _clip01((integration_response_strength * 0.52) + (integration_reframe_pull * 0.48)),
        "memory_sorting": _clip01((integration_sorting_need * 0.56) + (integration_memory_recall * 0.44)),
        "contact_deepening": _clip01(integration_contact_deepening),
        "workspace_sorting": _clip01((integration_strain_value * 0.50) + (conscious_workspace_load * 0.50)),
        "quiet_integration": _clip01(integration_response_strength * 0.74),
        "integration_background": _clip01((1.0 - integration_response_strength) * 0.40 + integration_capacity * 0.20),
    }
    integration_response_state = max(integration_response_pressures, key=integration_response_pressures.get)

    if integration_response_strength > 0.0:
        integration_relief = min(0.11, integration_response_strength * 0.075)
        field_observation_need = max(
            0.0,
            min(1.0, field_observation_need + (integration_sorting_need * 0.045) + (integration_contact_deepening * 0.030)),
        )
        field_replan_pressure = max(
            0.0,
            min(1.0, field_replan_pressure + (integration_reframe_pull * 0.050)),
        )
        act_watch_readiness = max(
            0.0,
            min(1.0, act_watch_readiness + (integration_memory_recall * 0.035) + (integration_contact_deepening * 0.030)),
        )
        action_inhibition = max(
            0.0,
            min(1.0, action_inhibition + (integration_sorting_need * 0.030) + (integration_reframe_pull * 0.020)),
        )
        action_clearance = max(
            0.0,
            min(1.0, action_clearance - (max(0.0, integration_sorting_need - integration_memory_recall) * 0.030)),
        )
        regulatory_second_order_load = max(
            0.0,
            min(1.0, regulatory_second_order_load - integration_relief + (max(0.0, integration_strain_value - integration_response_strength) * 0.035)),
        )
        integration_capacity = max(
            0.0,
            min(1.0, integration_capacity + (integration_response_strength * 0.045) + (integration_memory_recall * 0.020)),
        )
        metaregulator_balance = max(
            0.0,
            min(1.0, metaregulator_balance + (integration_response_strength * 0.025)),
        )
        integration_state_takeover_pressure = _clip01(
            ((1.0 if metaregulator_state == "integration_strain" else 0.0) * 0.42)
            + (integration_response_strength * 0.58)
        )
        if integration_state_takeover_pressure > metaregulator_state_pressures.get(str(metaregulator_state), 0.0):
            metaregulator_state = str(integration_response_state)

    cautious_hypothesis_strength = max(
        0.0,
        min(
            1.0,
            (integration_memory_recall * 0.22)
            + (integration_reframe_pull * 0.18)
            + (integration_contact_deepening * 0.14)
            + (conscious_gate_balance * 0.12)
            + (interpretation_quality * 0.12)
            + (transfer_bearing * 0.10)
            + (temporal_source_binding * 0.08)
            + (perception_sequence_coherence * 0.08)
            + (field_bearing_support * 0.08)
            + (form_symbol_action_binding * 0.06)
            - (integration_sorting_need * 0.08)
            - (subconscious_leakage * 0.06),
        ),
    )
    cautious_hypothesis_clarity = max(
        0.0,
        min(
            1.0,
            (cautious_hypothesis_strength * 0.28)
            + (memory_orientation * 0.20)
            + (route_familiarity * 0.15)
            + (temporal_context_depth * 0.12)
            + (temporal_self_consistency * 0.10)
            + (visual_grounding_strength * 0.12)
            + (structure_action_bearing * 0.12)
            + (inner_outer_alignment * 0.08)
            + (selective_attention * 0.05),
        ),
    )
    cautious_hypothesis_patience = max(
        0.0,
        min(
            1.0,
            (protective_distance_regulation * 0.20)
            + (distance_regulation * 0.18)
            + (integration_sorting_need * 0.16)
            + (max(0.0, 1.0 - temporal_source_binding) * 0.08)
            + (temporal_afterimage * 0.06)
            + (action_inhibition * 0.14)
            + (subconscious_buffering * 0.12)
            + (serotonin_stability * 0.10)
            + (gaba_inhibition * 0.10)
            - (plan_pressure * 0.08),
        ),
    )
    cautious_hypothesis_pressures = {
        "cautious_plan_seed": _clip01((cautious_hypothesis_strength * 0.54) + (cautious_hypothesis_clarity * 0.46)),
        "memory_reframe_seed": _clip01((integration_memory_recall * 0.52) + (integration_reframe_pull * 0.48)),
        "observe_until_clear": _clip01((integration_sorting_need * 0.48) + (cautious_hypothesis_patience * 0.52)),
        "deepen_contact_first": _clip01(integration_contact_deepening),
        "weak_hypothesis_seed": _clip01(cautious_hypothesis_strength * 0.74),
        "no_cautious_hypothesis": _clip01((1.0 - cautious_hypothesis_strength) * 0.38 + (1.0 - integration_response_strength) * 0.22),
    }
    cautious_hypothesis_state = max(cautious_hypothesis_pressures, key=cautious_hypothesis_pressures.get)

    if cautious_hypothesis_state != "no_cautious_hypothesis":
        act_watch_readiness = max(
            0.0,
            min(1.0, act_watch_readiness + (cautious_hypothesis_strength * 0.040) + (cautious_hypothesis_clarity * 0.025)),
        )
        field_replan_pressure = max(
            0.0,
            min(1.0, field_replan_pressure + (max(0.0, cautious_hypothesis_strength - cautious_hypothesis_clarity) * 0.030)),
        )
        action_readiness_from_field = max(
            0.0,
            min(1.0, action_readiness_from_field + (cautious_hypothesis_clarity * 0.030) - (cautious_hypothesis_patience * 0.010)),
        )
        field_action_support = action_readiness_from_field
        action_inhibition = max(
            0.0,
            min(1.0, action_inhibition + (cautious_hypothesis_patience * 0.018)),
        )
        action_clearance = max(
            0.0,
            min(1.0, action_clearance + (cautious_hypothesis_clarity * 0.018) - (max(0.0, cautious_hypothesis_patience - cautious_hypothesis_clarity) * 0.014)),
        )

    non_economic_plan_modulation_reasons = []

    trust_return_state = _build_trust_return_state(locals())
    previous_digest_state = str(trust_return_state.get("previous_digest_state", "") or "")
    previous_trust_return_readiness = float(trust_return_state.get("previous_trust_return_readiness", 0.0) or 0.0)
    previous_digestive_returned_trust = float(trust_return_state.get("previous_digestive_returned_trust", 0.0) or 0.0)
    previous_digestive_distance_pull = float(trust_return_state.get("previous_digestive_distance_pull", 0.0) or 0.0)
    previous_emergent_structure_state = str(trust_return_state.get("previous_emergent_structure_state", "") or "")
    previous_form_mcm_family_recurrence = float(trust_return_state.get("previous_form_mcm_family_recurrence", 0.0) or 0.0)
    previous_form_mcm_family_maturity = float(trust_return_state.get("previous_form_mcm_family_maturity", 0.0) or 0.0)
    previous_form_mcm_family_trust = float(trust_return_state.get("previous_form_mcm_family_trust", 0.0) or 0.0)
    previous_form_mcm_family_caution = float(trust_return_state.get("previous_form_mcm_family_caution", 0.0) or 0.0)
    previous_form_mcm_family_reorganization_need = float(trust_return_state.get("previous_form_mcm_family_reorganization_need", 0.0) or 0.0)
    previous_confirmed_structure_protection = float(trust_return_state.get("previous_confirmed_structure_protection", 0.0) or 0.0)
    trust_return_open_hypothesis_load = float(trust_return_state.get("trust_return_open_hypothesis_load", 0.0) or 0.0)
    trust_return_context_instability = float(trust_return_state.get("trust_return_context_instability", 0.0) or 0.0)
    trust_return_motor_contact_strength = float(trust_return_state.get("trust_return_motor_contact_strength", 0.0) or 0.0)
    trust_return_act_bridge = float(trust_return_state.get("trust_return_act_bridge", 0.0) or 0.0)
    trust_return_motor_heat = float(trust_return_state.get("trust_return_motor_heat", 0.0) or 0.0)
    trust_return_stabilization_need = float(trust_return_state.get("trust_return_stabilization_need", 0.0) or 0.0)
    trust_return_focus_pull = float(trust_return_state.get("trust_return_focus_pull", 0.0) or 0.0)
    trust_return_motor_mode = str(trust_return_state.get("trust_return_motor_mode", "trust_quiet") or "trust_quiet")
    metaregulator_reflection_pressure = _clip01(
        (regulatory_second_order_load * 0.22)
        + (nervous_overload_reflection_need * 0.20)
        + (nervous_context_overcoupling * 0.18)
        + (max(0.0, 0.30 - inner_outer_alignment) * 0.16)
        + (max(0.0, 0.24 - field_action_support) * 0.14)
        + (max(0.0, 0.34 - perceptual_distance) * 0.10)
    )

    plan_modulation_trace = {}
    if bool(allow_plan) and decision in ("LONG", "SHORT"):
        effort_reorganization_modulation = _clip01(
            ((1.0 if effort_state == "underengaged_reorganize" else 0.0) * 0.24)
            + (pre_action_reorganization_pressure * 0.22)
            + ((1.0 - pre_action_context_selectivity) * 0.14)
            + (effort_learning_pull * 0.12)
            + (max(0.0, (1.24 + effort_learning_pull * 0.34) - decision_strength) * 0.10)
        )
        diffuse_open_modulation = _clip01(
            (diffuse_open_development_pressure * 0.34)
            + (curiosity_tone * 0.12)
            + (calm_tone * 0.08)
            + ((1.0 if posture_development_hint in ("develop_reflective_distance", "develop_release_capacity") else 0.0) * 0.14)
            + (max(0.0, (1.16 + max(0.0, curiosity_tone - 0.12) * 0.60 + max(0.0, calm_tone - 0.10) * 0.40) - decision_strength) * 0.10)
        )
        integration_reframe_modulation = _clip01(
            (integration_response_strength * 0.20)
            + (max(0.0, integration_sorting_need - integration_memory_recall) * 0.20)
            + (integration_reframe_pull * 0.18)
            + (field_replan_pressure * 0.10)
            + (max(0.0, (1.18 + integration_memory_recall * 0.32 + conscious_gate_balance * 0.18) - decision_strength) * 0.08)
        )
        cautious_hypothesis_modulation = _clip01(
            (cautious_hypothesis_patience * 0.22)
            + (max(0.0, cautious_hypothesis_strength - cautious_hypothesis_clarity) * 0.20)
            + (integration_reframe_pull * 0.10)
            + ((1.0 if cautious_hypothesis_state in ("observe_until_clear", "deepen_contact_first") else 0.0) * 0.12)
            + (max(0.0, (1.14 + cautious_hypothesis_strength * 0.24) - decision_strength) * 0.08)
        )
        trust_return_modulation = _clip01(
            ((1.0 if trust_return_motor_mode == "trust_stabilize_before_act" else 0.0) * 0.20)
            + (trust_return_act_bridge * 0.16)
            + (trust_return_stabilization_need * 0.20)
            + (previous_digestive_distance_pull * 0.12)
            + (trust_return_context_instability * 0.12)
            + (max(0.0, (1.32 + trust_return_focus_pull * 0.26 + trust_return_act_bridge * 0.16) - decision_strength) * 0.08)
        )
        metaregulator_reflection_modulation = _clip01(
            (metaregulator_reflection_pressure * 0.24)
            + ((1.0 if metaregulator_state in (
                "context_overcoupling_reflection",
                "nervous_overload_reflection",
                "low_distance_processing",
                "overcoupled_protection",
                "spacetime_reflection",
                "regulatory_overload",
                "impulse_pressure",
            ) else 0.0) * 0.18)
            + ((1.0 - field_action_support) * 0.10)
            + ((1.0 - inner_outer_alignment) * 0.10)
            + ((1.0 - perceptual_distance) * 0.08)
            + ((1.0 - action_clearance) * 0.08)
            + (regulatory_second_order_load * 0.06)
            + (spacetime_reflection_need * 0.06)
        )
        act_continuity_pressure = _clip01(
            (decision_strength * 0.18)
            + (action_clearance * 0.18)
            + (field_action_support * 0.16)
            + (inner_outer_alignment * 0.14)
            + (perceptual_distance * 0.10)
            + (conscious_gate_balance * 0.10)
            + (trust_return_act_bridge * 0.06)
        )
        plan_modulation_trace = {
            "effort_reorganization_modulation": float(effort_reorganization_modulation),
            "diffuse_open_modulation": float(diffuse_open_modulation),
            "integration_reframe_modulation": float(integration_reframe_modulation),
            "cautious_hypothesis_modulation": float(cautious_hypothesis_modulation),
            "trust_return_modulation": float(trust_return_modulation),
            "metaregulator_reflection_modulation": float(metaregulator_reflection_modulation),
            "act_continuity_pressure": float(act_continuity_pressure),
        }
        modulation_pressures = {
            "pre_action_reorganization": effort_reorganization_modulation,
            "diffuse_open": diffuse_open_modulation,
            "integration_reframe": integration_reframe_modulation,
            "cautious_hypothesis": cautious_hypothesis_modulation,
            "trust_return": trust_return_modulation,
            "metaregulator_reflection": metaregulator_reflection_modulation,
        }
        dominant_modulation_reason = max(modulation_pressures, key=modulation_pressures.get)
        dominant_modulation_pressure = modulation_pressures.get(dominant_modulation_reason, 0.0)
        if dominant_modulation_pressure > act_continuity_pressure:
            non_economic_plan_modulation_reasons.append(str(dominant_modulation_reason))
            allow_observe = True
            replan_pull = _clip01(
                (field_replan_pressure * 0.18)
                + (integration_reframe_pull * 0.16)
                + (regulatory_second_order_load * 0.12)
                + (pre_action_reorganization_pressure * 0.12)
                + (trust_return_stabilization_need * 0.10)
                + (spacetime_reflection_need * 0.08)
            )
            observe_pull = _clip01(
                (field_observation_need * 0.18)
                + (diffuse_open_development_pressure * 0.14)
                + (cautious_hypothesis_patience * 0.12)
                + (metaregulator_reflection_pressure * 0.10)
                + (trust_return_focus_pull * 0.08)
            )
            allow_ruminate = bool(replan_pull > observe_pull)
            allow_block = False
            rejection_reason = f"{dominant_modulation_reason}_replan" if allow_ruminate else f"{dominant_modulation_reason}_observe"
            pre_action_phase = "replan" if allow_ruminate else "observe"
        field_observation_need = _clip01(field_observation_need + (metaregulator_reflection_pressure * 0.030) + (trust_return_stabilization_need * 0.026))
        field_replan_pressure = _clip01(field_replan_pressure + (metaregulator_reflection_pressure * 0.025) + (integration_reframe_pull * 0.028))
        action_inhibition = _clip01(action_inhibition + (metaregulator_reflection_pressure * 0.020) + (trust_return_stabilization_need * 0.024))
        action_clearance = _clip01(action_clearance - (metaregulator_reflection_pressure * 0.014) - (trust_return_stabilization_need * 0.018))
        perceptual_distance = _clip01(perceptual_distance + (metaregulator_reflection_pressure * 0.018) + (trust_return_stabilization_need * 0.024))
        inner_outer_reflection = _clip01(inner_outer_reflection + (metaregulator_reflection_pressure * 0.016) + (trust_return_stabilization_need * 0.022))

    non_economic_plan_modulated = bool(non_economic_plan_modulation_reasons)
    if non_economic_plan_modulated and decision in ("LONG", "SHORT"):
        allow_plan = True
        allow_block = False

    return {
        "allow_observe": bool(allow_observe),
        "allow_ruminate": bool(allow_ruminate),
        "allow_plan": bool(allow_plan),
        "allow_block": bool(allow_block),
        "non_economic_plan_modulated": bool(non_economic_plan_modulated),
        "non_economic_plan_modulation_reasons": list(non_economic_plan_modulation_reasons),
        "plan_modulation_trace": dict(plan_modulation_trace),
        "non_economic_gate_policy": "field_modulation_only",
        "pre_action_phase": str(pre_action_phase),
        "pre_action_pressure_trace": dict(pre_action_pressure_trace),
        "rejection_reason": str(rejection_reason or "-"),
        "decision": str(decision),
        "uncertainty_score": float(uncertainty_score),
        "observe_priority": float(observe_priority),
        "felt_conflict": float(felt_conflict),
        "felt_pressure": float(felt_pressure),
        "decision_conflict": float(decision_conflict),
        "state_maturity": float(state_maturity),
        "rumination_depth": float(rumination_depth),
        "decision_readiness": float(decision_readiness),
        "signal_quality": float(signal_quality),
        "decision_strength": float(decision_strength),
        "processing_load": float(processing_load),
        "processing_alignment": float(processing_alignment),
        "processing_tension": float(processing_tension),
        "processing_areal_tension": float(processing_areal_tension),
        "processing_areal_support": float(processing_areal_support),
        "field_perception_pressure": float(field_perception_pressure),
        "field_perception_support": float(field_perception_support),
        "field_perception_clarity": float(field_perception_clarity),
        "field_perception_focus": float(field_perception_focus),
        "field_perception_stability": float(field_perception_stability),
        "field_perception_fragmentation": float(field_perception_fragmentation),
        "field_perception_strain": float(field_perception_strain),
        "dominant_activity_island_id": str(dominant_activity_island_id),
        "field_perception_label": str(field_perception_label),
        "field_activity_island_count": int(field_activity_island_count),
        "field_perception_instability": float(field_perception_instability),
        "field_observation_need": float(field_observation_need),
        "field_replan_pressure": float(field_replan_pressure),
        "field_bearing_support": float(field_bearing_support),
        "action_readiness_from_field": float(action_readiness_from_field),
        "field_action_support": float(field_action_support),
        "market_balance": float(market_balance),
        "breakout_tension": float(breakout_tension),
        "visual_coherence": float(visual_coherence),
        "visual_reflective_coherence": float(visual_reflective_coherence),
        "visual_clarity": float(visual_clarity),
        "visual_object_stability": float(visual_object_stability),
        "visual_form_novelty": float(visual_form_novelty),
        "visual_blindness": float(visual_blindness),
        "visual_form_pressure": float(visual_form_pressure),
        "visual_shape_resonance": float(visual_shape_resonance),
        "visual_shape_fragility": float(visual_shape_fragility),
        "visual_attention_label": str(visual_attention_label),
        "visual_form_contact": float(visual_form_contact),
        "visual_inspection_pull": float(visual_inspection_pull),
        "visual_attention_depth": float(visual_attention_depth),
        "visual_background_filter": float(visual_background_filter),
        "visual_mcm_contact_weight": float(visual_mcm_contact_weight),
        "visual_blind_action_load": float(visual_blind_action_load),
        "visual_action_uncertainty": float(visual_action_uncertainty),
        "visual_object_binding": float(visual_object_binding),
        "visual_cortex_grounding": float(visual_cortex_grounding),
        "visual_object_binding_quality": float(visual_object_binding_quality),
        "visual_contact_nearness": float(visual_contact_nearness),
        "visual_lifecycle_stability": float(visual_lifecycle_stability),
        "visual_lifecycle_rejection": float(visual_lifecycle_rejection),
        "visual_lifecycle_dissolution": float(visual_lifecycle_dissolution),
        "visual_grounding_strength": float(visual_grounding_strength),
        "visual_resonance_unbound": float(visual_resonance_unbound),
        "visual_grounding_gap": float(visual_grounding_gap),
        "visual_grounding_need": float(visual_grounding_need),
        "visual_rational_observation_support": float(visual_rational_observation_support),
        "visual_grounding_state": str(visual_grounding_state),
        "external_pressure": float(external_pressure),
        "inner_conflict_pressure": float(inner_conflict_pressure),
        "repetition_pressure": float(repetition_pressure),
        "expectation_pressure": float(expectation_pressure),
        "uncertainty_pressure": float(uncertainty_pressure),
        "aftereffect_pressure": float(aftereffect_pressure),
        "areal_support": float(areal_support),
        "areal_conflict_pressure": float(areal_conflict_pressure),
        "dominant_tension_cause": str(dominant_tension_cause),
        "dominant_tension_value": float(dominant_tension_value),
        "observation_need": float(pre_action_observation_need),
        "regulated_courage": float(regulated_courage),
        "courage_gap": float(courage_gap),
        "action_inhibition": float(action_inhibition),
        "action_clearance": float(action_clearance),
        "engaged_effort": float(engaged_effort),
        "effort_state": str(effort_state),
        "effort_learning_pull": float(effort_learning_pull),
        "effort_reorganization_pressure": float(effort_reorganization_pressure),
        "pre_action_reorganization_pressure": float(pre_action_reorganization_pressure),
        "pre_action_context_selectivity": float(pre_action_context_selectivity),
        "previous_packet_label": str(previous_packet_label),
        "previous_packet_process_reward": float(previous_packet_process_reward),
        "previous_packet_reorganization_need": float(previous_packet_reorganization_need),
        "previous_constructive_stimulation": float(previous_constructive_stimulation),
        "previous_open_hypothesis_learning_state": str(previous_open_hypothesis_learning_state),
        "previous_open_hypothesis_reorganization_posture": str(previous_open_hypothesis_reorganization_posture),
        "previous_open_hypothesis_consequence_score": float(previous_open_hypothesis_consequence_score),
        "previous_open_hypothesis_burden_score": float(previous_open_hypothesis_burden_score),
        "previous_open_hypothesis_reorganization_score": float(previous_open_hypothesis_reorganization_score),
        "previous_open_hypothesis_replay_need": float(previous_open_hypothesis_replay_need),
        "previous_open_hypothesis_distance_need": float(previous_open_hypothesis_distance_need),
        "previous_open_hypothesis_reinterpretation_need": float(previous_open_hypothesis_reinterpretation_need),
        "open_hypothesis_trace_strength": float(open_hypothesis_trace_strength),
        "hypothesis_weight": float(hypothesis_weight),
        "hypothesis_trust": float(hypothesis_trust),
        "hypothesis_caution": float(hypothesis_caution),
        "hypothesis_reorganization_weight": float(hypothesis_reorganization_weight),
        "action_weight": float(action_weight),
        "decision_weight": float(decision_weight),
        "open_hypothesis_reifung_state": str(open_hypothesis_reifung_state),
        "open_hypothesis_bearing_echo": float(open_hypothesis_bearing_echo),
        "open_hypothesis_reifung_pressure": float(open_hypothesis_reifung_pressure),
        "open_hypothesis_reflection_pull": float(open_hypothesis_reflection_pull),
        "open_hypothesis_action_tension": float(open_hypothesis_motor_tension),
        "open_hypothesis_motor_tension": float(open_hypothesis_motor_tension),
        "open_hypothesis_confirmation_weight": float(open_hypothesis_confirmation_weight),
        "open_hypothesis_learning_charge": float(open_hypothesis_learning_charge),
        "open_hypothesis_reality_bearing": float(open_hypothesis_reality_permission),
        "open_hypothesis_reality_fit": float(open_hypothesis_reality_permission),
        "open_hypothesis_reality_permission": float(open_hypothesis_reality_permission),
        "open_hypothesis_action_permission": float(open_hypothesis_action_permission),
        "open_hypothesis_reality_check_need": float(open_hypothesis_reality_check_need),
        "declined_hypothesis_confirmation_without_action": float(declined_hypothesis_confirmation_without_action),
        "declined_hypothesis_rejection_without_action": float(declined_hypothesis_rejection_without_action),
        "declined_hypothesis_maturity": float(declined_hypothesis_maturity),
        "declined_hypothesis_protective_trace": float(declined_hypothesis_protective_trace),
        "declined_hypothesis_missed_trace": float(declined_hypothesis_missed_trace),
        "declined_hypothesis_mixed_trace": float(declined_hypothesis_mixed_trace),
        "declined_hypothesis_protective_edge": float(declined_hypothesis_protective_edge),
        "declined_hypothesis_missed_edge": float(declined_hypothesis_missed_edge),
        "directional_hypothesis_decision": str(directional_hypothesis_decision),
        "directional_hypothesis_confirmation": float(directional_hypothesis_confirmation),
        "directional_hypothesis_rejection": float(directional_hypothesis_rejection),
        "directional_hypothesis_maturity": float(directional_hypothesis_maturity),
        "directional_hypothesis_protective_edge": float(directional_hypothesis_protective_edge),
        "directional_hypothesis_missed_edge": float(directional_hypothesis_missed_edge),
        "previous_digest_state": str(previous_digest_state),
        "previous_trust_return_readiness": float(previous_trust_return_readiness),
        "previous_digestive_returned_trust": float(previous_digestive_returned_trust),
        "previous_emergent_structure_state": str(previous_emergent_structure_state),
        "previous_confirmed_structure_protection": float(previous_confirmed_structure_protection),
        "trust_return_open_hypothesis_load": float(trust_return_open_hypothesis_load),
        "trust_return_context_instability": float(trust_return_context_instability),
        "trust_return_motor_contact_strength": float(trust_return_motor_contact_strength),
        "trust_return_act_bridge": float(trust_return_act_bridge),
        "trust_return_motor_heat": float(trust_return_motor_heat),
        "trust_return_stabilization_need": float(trust_return_stabilization_need),
        "trust_return_focus_pull": float(trust_return_focus_pull),
        "trust_return_motor_mode": str(trust_return_motor_mode),
        "metaregulator_reflection_pressure": float(metaregulator_reflection_pressure),
        "diffuse_open_development_pressure": float(diffuse_open_development_pressure),
        "posture_development_hint": str(posture_development_hint),
        "metaregulator_state": str(metaregulator_state),
        "metaregulator_balance": float(metaregulator_balance),
        "regulatory_second_order_load": float(regulatory_second_order_load),
        "subconscious_field_pressure": float(subconscious_field_pressure),
        "subconscious_habituation": float(subconscious_habituation),
        "subconscious_filter_strength": float(subconscious_filter_strength),
        "subconscious_buffering": float(subconscious_buffering),
        "subconscious_leakage": float(subconscious_leakage),
        "subconscious_afterimage_depth": float(subconscious_afterimage_depth),
        "subconscious_afterimage_pressure": float(subconscious_afterimage_pressure),
        "subconscious_afterimage_bearing": float(subconscious_afterimage_bearing),
        "subconscious_afterimage_clarity": float(subconscious_afterimage_clarity),
        "subconscious_afterimage_release": float(subconscious_afterimage_release),
        "subconscious_afterimage_reflection_pull": float(subconscious_afterimage_reflection_pull),
        "conscious_selection_pressure": float(conscious_selection_pressure),
        "conscious_workspace_focus": float(conscious_workspace_focus),
        "conscious_workspace_load": float(conscious_workspace_load),
        "conscious_gate_balance": float(conscious_gate_balance),
        "integration_strain_value": float(integration_strain_value),
        "integration_sorting_need": float(integration_sorting_need),
        "integration_reframe_pull": float(integration_reframe_pull),
        "integration_memory_recall": float(integration_memory_recall),
        "integration_contact_deepening": float(integration_contact_deepening),
        "integration_response_strength": float(integration_response_strength),
        "integration_response_state": str(integration_response_state),
        "cautious_hypothesis_strength": float(cautious_hypothesis_strength),
        "cautious_hypothesis_clarity": float(cautious_hypothesis_clarity),
        "cautious_hypothesis_patience": float(cautious_hypothesis_patience),
        "cautious_hypothesis_state": str(cautious_hypothesis_state),
        "temporal_binding_state": str(temporal_binding_state),
        "temporal_continuity": float(temporal_continuity),
        "temporal_source_binding": float(temporal_source_binding),
        "temporal_recurrence": float(temporal_recurrence),
        "temporal_novelty": float(temporal_novelty),
        "temporal_afterimage": float(temporal_afterimage),
        "temporal_decay": float(temporal_decay),
        "temporal_context_depth": float(temporal_context_depth),
        "mcm_spacetime_depth": float(mcm_spacetime_depth),
        "memory_experience_depth": float(memory_experience_depth),
        "future_projection_depth": float(future_projection_depth),
        "temporal_self_location": float(temporal_self_location),
        "temporal_self_location_state": str(temporal_self_location_state),
        "temporal_self_consistency": float(temporal_self_consistency),
        "perception_sequence_coherence": float(perception_sequence_coherence),
        "memory_time_distance": float(memory_time_distance),
        "spacetime_unlocated_pressure": float(spacetime_unlocated_pressure),
        "spacetime_memory_bearing": float(spacetime_memory_bearing),
        "spacetime_future_bearing": float(spacetime_future_bearing),
        "spacetime_reflection_need": float(spacetime_reflection_need),
        "spacetime_regulation_support": float(spacetime_regulation_support),
        "spacetime_regulation_state": str(spacetime_regulation_state),
        "return_strength": float(return_strength),
        "integration_capacity": float(integration_capacity),
        "variance_regulation": float(variance_regulation),
        "load_tolerance": float(load_tolerance),
        "impulse_control": float(impulse_control),
        "frustration_tolerance": float(frustration_tolerance),
        "protective_distance_regulation": float(protective_distance_regulation),
        "self_reflection_regulator": float(self_reflection_regulator),
        "distance_regulation": float(distance_regulation),
        "memory_orientation": float(memory_orientation),
        "orientation_gap": float(orientation_gap),
        "blind_thinking_load": float(blind_thinking_load),
        "perception_event_strength": float(perception_event_strength),
        "thought_load_pressure": float(thought_load_pressure),
        "thought_overprocessing_signal": float(thought_overprocessing_signal),
        "thought_economy_need": float(thought_economy_need),
        "thought_release_pressure": float(thought_release_pressure),
        "thought_efficiency_support": float(thought_efficiency_support),
        "symbolic_object_distance": float(form_symbol_object_distance),
        "symbolic_containment": float(form_symbol_containment),
        "symbolic_field_decoupling": float(form_symbol_field_decoupling),
        "symbolic_regulation": float(symbolic_regulation),
        "symbolic_inner_regulation": float(symbolic_inner_regulation),
        "symbolic_action_regulation": float(symbolic_action_regulation),
        "symbolic_compound_load_reduction": float(form_symbol_compound_load_reduction),
        "symbolic_compound_bearing": float(form_symbol_compound_bearing),
        "symbolic_compound_novelty": float(form_symbol_compound_novelty),
        "form_symbol_development_quality": float(form_symbol_development_quality),
        "form_symbol_action_binding": float(form_symbol_action_binding),
        "form_symbol_observation_binding": float(form_symbol_observation_binding),
        "form_symbol_reframe_binding": float(form_symbol_reframe_binding),
        "form_symbol_learning_trust": float(form_symbol_learning_trust),
        "form_symbol_action_trust": float(form_symbol_action_trust),
        "form_symbol_caution_trust": float(form_symbol_caution_trust),
        "form_symbol_contact_maturity": float(form_symbol_contact_maturity),
        "form_symbol_contact_utility": float(form_symbol_contact_utility),
        "form_symbol_contact_pain_memory": float(form_symbol_contact_pain_memory),
        "form_symbol_contact_carefulness": float(form_symbol_contact_carefulness),
        "form_symbol_contact_burden_evidence": float(form_symbol_contact_burden_evidence),
        "form_symbol_contact_utility_evidence": float(form_symbol_contact_utility_evidence),
        "form_symbol_contact_learning_state": str(form_symbol_contact_learning_state),
        "uncertain_form_family_state": str(uncertain_form_family_state),
        "uncertain_form_exposure": float(uncertain_form_exposure),
        "uncertainty_familiarity": float(uncertainty_familiarity),
        "variant_similarity": float(variant_similarity),
        "variant_spread": float(variant_spread),
        "variant_learning_pressure": float(variant_learning_pressure),
        "variant_bearing_memory": float(variant_bearing_memory),
        "learned_development_uncertainty": float(learned_development_uncertainty),
        "zero_point_regulation": bool(zero_point_regulation),
        "zero_point_hint": "finde_wieder_zu_dir_selbst" if bool(zero_point_regulation) else "-",
        "structure_quality": float(structure_quality),
        "context_confidence": float(context_confidence),
        "structure_orientation": float(structure_orientation),
        "structure_orientation_gap": float(structure_orientation_gap),
        "structure_action_bearing": float(structure_action_bearing),
        "structure_action_gap": float(structure_action_gap),
        "structure_action_uncertainty": float(structure_action_uncertainty),
        "structure_carrying_need": float(structure_carrying_need),
        "plan_pressure": float(plan_pressure),
        "act_watch_readiness": float(act_watch_readiness),
        "structure_orientation_guard": bool(structure_orientation_guard),
        "known_form_support": float(known_form_support),
        "route_familiarity": float(route_familiarity),
        "semantic_shift_pressure": float(semantic_shift_pressure),
        "transfer_bearing": float(transfer_bearing),
        "interpretation_quality": float(interpretation_quality),
        "adaptation_phase": str(adaptation_phase),
        "trust_transfer_base": float(trust_transfer_base),
        "trust_transfer_support": float(trust_transfer_support),
        "transfer_maturity_gap": float(transfer_maturity_gap),
        "trust_transfer_mode": str(trust_transfer_mode),
        "transfer_break_fatigue": float(transfer_break_fatigue),
        "transfer_recovery_need": float(transfer_recovery_need),
        "transfer_break_trigger": float(transfer_break_trigger),
        "transfer_break_ready": bool(transfer_break_ready),
        "neurochemical_state": dict(neurochemical_state or {}),
        "neurochemical_state_label": str(neurochemical_state.get("neurochemical_state_label", "mixed_neurochemistry") or "mixed_neurochemistry"),
        "neurochemical_dominant_tone": str(neurochemical_state.get("neurochemical_dominant_tone", "-") or "-"),
        "dopamine_tone": float(neurochemical_state.get("dopamine_tone", 0.0) or 0.0),
        "gaba_inhibition": float(neurochemical_state.get("gaba_inhibition", 0.0) or 0.0),
        "noradrenaline_arousal": float(neurochemical_state.get("noradrenaline_arousal", 0.0) or 0.0),
        "acetylcholine_focus": float(neurochemical_state.get("acetylcholine_focus", 0.0) or 0.0),
        "serotonin_stability": float(neurochemical_state.get("serotonin_stability", 0.0) or 0.0),
        "cortisol_load": float(neurochemical_state.get("cortisol_load", 0.0) or 0.0),
        "endorphin_relief": float(neurochemical_state.get("endorphin_relief", 0.0) or 0.0),
        "glutamate_activation": float(neurochemical_state.get("glutamate_activation", 0.0) or 0.0),
        "neurochemical_load": float(neurochemical_state.get("neurochemical_load", 0.0) or 0.0),
        "neurochemical_support": float(neurochemical_state.get("neurochemical_support", 0.0) or 0.0),
        "neurochemical_balance": float(neurochemical_state.get("neurochemical_balance", 0.0) or 0.0),
        "reward_stability_echo": float(neurochemical_state.get("reward_stability_echo", 0.0) or 0.0),
        "positive_expansion_pressure": float(positive_expansion_pressure),
        "negative_contraction_pressure": float(negative_contraction_pressure),
        "positive_overextension": float(positive_overextension),
        "positive_return_pressure": float(positive_return_pressure),
        "mcm_axis_displacement": float(mcm_axis_displacement),
        "mcm_axis_field_position": float(mcm_axis_field_position),
        "mcm_axis_tension": float(mcm_axis_tension),
        "mcm_axis_state": str(mcm_axis_state),
        "mcm_preregulator_state": dict(mcm_preregulator_state or {}),
        "mcm_reflective_bearing": float(mcm_reflective_bearing),
        "mcm_reflective_pressure": float(mcm_reflective_pressure),
        "mcm_reflective_coupling_load": float(mcm_reflective_coupling_load),
        "mcm_reflective_displacement": float(mcm_reflective_displacement),
        "mcm_reflective_field_position": float(mcm_reflective_field_position),
        "mcm_reflective_tension": float(mcm_reflective_tension),
        "positive_zero_point_regulation": bool(positive_zero_point_regulation),
        "world_shift_evidence": float(neurochemical_state.get("world_shift_evidence", 0.0) or 0.0),
        "serotonin_carryover_risk": float(neurochemical_state.get("serotonin_carryover_risk", 0.0) or 0.0),
        "emotional_decoupling": float(neurochemical_state.get("emotional_decoupling", 0.0) or 0.0),
        "reactive_nervous_drive": float(neurochemical_state.get("reactive_nervous_drive", 0.0) or 0.0),
        "nervous_system_overload": float(neurochemical_state.get("nervous_system_overload", 0.0) or 0.0),
        "escape_action_drive": float(neurochemical_state.get("escape_action_drive", 0.0) or 0.0),
        "shock_response_risk": float(neurochemical_state.get("shock_response_risk", 0.0) or 0.0),
        "nervous_overload_reflection_need": float(nervous_overload_reflection_need),
        "active_context_self_certainty": float(active_context_self_certainty),
        "nervous_context_overcoupling": float(nervous_context_overcoupling),
        "own_field_identity_strength": float(own_field_identity_strength),
        "foreign_semantic_pressure": float(foreign_semantic_pressure),
        "adopted_language_pressure": float(adopted_language_pressure),
        "self_foreign_boundary_clarity": float(self_foreign_boundary_clarity),
        "semantic_origin_conflict": float(semantic_origin_conflict),
        "own_vs_foreign_margin": float(own_vs_foreign_margin),
        "borrowed_vs_own_margin": float(borrowed_vs_own_margin),
        "boundary_support_margin": float(boundary_support_margin),
        "semantic_origin_state": str(semantic_origin_state),
        "conscious_perception": dict(conscious_perception_state or {}),
        "conscious_perception_state": str(conscious_perception_state.get("conscious_perception_state", "open_perception") or "open_perception"),
        "inner_posture_state": str(conscious_perception_state.get("inner_posture_state", "uncertain_open") or "uncertain_open"),
        "arousal_load": float(conscious_perception_state.get("arousal_load", 0.0) or 0.0),
        "curiosity_tone": float(conscious_perception_state.get("curiosity_tone", 0.0) or 0.0),
        "fatigue_tone": float(conscious_perception_state.get("fatigue_tone", 0.0) or 0.0),
        "calm_tone": float(conscious_perception_state.get("calm_tone", 0.0) or 0.0),
        "stimulus_field_effect": float(conscious_perception_state.get("stimulus_field_effect", 0.0) or 0.0),
        "inner_impact_trace": float(conscious_perception_state.get("inner_impact_trace", 0.0) or 0.0),
        "perceived_field_change": float(conscious_perception_state.get("perceived_field_change", 0.0) or 0.0),
        "felt_afterimage": float(conscious_perception_state.get("felt_afterimage", 0.0) or 0.0),
        "object_release_state": str(conscious_perception_state.get("object_release_state", "holding") or "holding"),
        "inner_outer_reflection": float(conscious_perception_state.get("inner_outer_reflection", 0.0) or 0.0),
        "perceptual_distance": float(conscious_perception_state.get("perceptual_distance", 0.0) or 0.0),
        "object_contact_depth": float(conscious_perception_state.get("object_contact_depth", 0.0) or 0.0),
        "field_attachment": float(conscious_perception_state.get("field_attachment", 0.0) or 0.0),
        "release_capacity": float(conscious_perception_state.get("release_capacity", 0.0) or 0.0),
        "selective_attention": float(conscious_perception_state.get("selective_attention", 0.0) or 0.0),
        "background_containment": float(conscious_perception_state.get("background_containment", 0.0) or 0.0),
        "reflective_distance": float(conscious_perception_state.get("reflective_distance", 0.0) or 0.0),
        "inner_outer_alignment": float(conscious_perception_state.get("inner_outer_alignment", 0.0) or 0.0),
        "readiness": float(decision_readiness),
        "maturity": float(state_maturity),
        "uncertainty": float(uncertainty_score),
        "conflict": float(decision_conflict),
    }

# --------------------------------------------------
# pthought_state
# --------------------------------------------------

def build_thought_state(candle_state, tension_state, fused, perception_state, felt_state, snapshot, processing_state=None, bot=None):

    fused_state = dict(fused or {})
    perception = dict(perception_state or {})
    felt = dict(felt_state or {})
    processing = dict(processing_state or {})
    snap = dict(snapshot or {})

    long_score = float(fused_state.get("long_score", 0.0) or 0.0)
    short_score = float(fused_state.get("short_score", 0.0) or 0.0)
    decision = str(fused_state.get("decision", "WAIT") or "WAIT")
    market_balance = float(felt.get("market_balance", perception.get("market_balance", 0.0)) or 0.0)
    breakout_tension = float(felt.get("breakout_tension", perception.get("breakout_tension", 0.0)) or 0.0)
    visual_coherence = float(felt.get("visual_coherence", perception.get("visual_coherence", 0.0)) or 0.0)
    visual_reflective_coherence = float(felt.get("visual_reflective_coherence", processing.get("visual_reflective_coherence", visual_coherence)) or 0.0)
    felt_alignment = float(felt.get("felt_alignment", 0.0) or 0.0)
    processing_load = float(processing.get("processing_load", 0.0) or 0.0)
    processing_stability = float(processing.get("processing_stability", 0.0) or 0.0)
    processing_readiness = float(processing.get("processing_readiness", 0.0) or 0.0)
    processing_alignment = float(processing.get("processing_alignment", 0.0) or 0.0)
    processing_tension = float(processing.get("processing_tension", 0.0) or 0.0)
    processing_areal_tension = float(processing.get("processing_areal_tension", 0.0) or 0.0)
    processing_areal_support = float(processing.get("processing_areal_support", 0.0) or 0.0)
    field_perception_pressure = float(felt.get("field_perception_pressure", processing.get("field_perception_pressure", 0.0)) or 0.0)
    field_perception_support = float(felt.get("field_perception_support", processing.get("field_perception_support", 0.0)) or 0.0)
    field_perception_clarity = float(felt.get("field_perception_clarity", processing.get("field_perception_clarity", 0.0)) or 0.0)
    field_perception_focus = float(felt.get("field_perception_focus", processing.get("field_perception_focus", snap.get("field_perception_focus", 0.0))) or 0.0)
    field_perception_stability = float(felt.get("field_perception_stability", processing.get("field_perception_stability", snap.get("field_perception_stability", 0.0))) or 0.0)
    field_perception_fragmentation = float(felt.get("field_perception_fragmentation", processing.get("field_perception_fragmentation", snap.get("field_perception_fragmentation", 0.0))) or 0.0)
    field_perception_strain = float(felt.get("field_perception_strain", processing.get("field_perception_strain", snap.get("field_perception_strain", 0.0))) or 0.0)
    dominant_activity_island_id = str(felt.get("dominant_activity_island_id", processing.get("dominant_activity_island_id", snap.get("dominant_activity_island_id", "-"))) or "-")
    field_perception_label = str(felt.get("field_perception_label", processing.get("field_perception_label", snap.get("field_perception_label", "quiet_field"))) or "quiet_field").strip().lower()
    areal_support = float(felt.get("areal_support", 0.0) or 0.0)
    areal_conflict_pressure = float(felt.get("areal_conflict_pressure", 0.0) or 0.0)
    field_areal_count = int(snap.get("field_areal_count", processing.get("field_areal_count", 0)) or 0)
    field_areal_dominance = float(snap.get("field_areal_dominance", processing.get("field_areal_dominance", 0.0)) or 0.0)
    field_areal_fragmentation = float(snap.get("field_areal_fragmentation", processing.get("field_areal_fragmentation", 0.0)) or 0.0)
    field_areal_conflict_mean = float(snap.get("field_areal_conflict_mean", processing.get("field_areal_conflict_mean", 0.0)) or 0.0)
    field_areal_stability_mean = float(snap.get("field_areal_stability_mean", processing.get("field_areal_stability_mean", 0.0)) or 0.0)
    field_areal_coherence_mean = float(snap.get("field_areal_coherence_mean", processing.get("field_areal_coherence_mean", 0.0)) or 0.0)
    field_activity_island_count = int(snap.get("field_activity_island_count", processing.get("field_activity_island_count", felt.get("field_activity_island_count", 0))) or 0)
    field_activity_island_activation_mean = float(snap.get("field_activity_island_activation_mean", processing.get("field_activity_island_activation_mean", felt.get("field_activity_island_activation_mean", 0.0))) or 0.0)
    field_activity_island_pressure_mean = float(snap.get("field_activity_island_pressure_mean", processing.get("field_activity_island_pressure_mean", felt.get("field_activity_island_pressure_mean", 0.0))) or 0.0)
    field_activity_island_coherence_mean = float(snap.get("field_activity_island_coherence_mean", processing.get("field_activity_island_coherence_mean", felt.get("field_activity_island_coherence_mean", 0.0))) or 0.0)
    field_activity_island_context_reactivation_mean = float(snap.get("field_activity_island_context_reactivation_mean", processing.get("field_activity_island_context_reactivation_mean", felt.get("field_activity_island_context_reactivation_mean", 0.0))) or 0.0)
    field_activity_island_spread = float(snap.get("field_activity_island_spread", processing.get("field_activity_island_spread", felt.get("field_activity_island_spread", 0.0))) or 0.0)
    uncertainty_score = float(perception.get("uncertainty_score", 0.0) or 0.0)

    thought_areal_pressure = max(
        0.0,
        min(
            1.0,
            (areal_conflict_pressure * 0.34)
            + (processing_areal_tension * 0.24)
            + (field_areal_conflict_mean * 0.18)
            + (field_areal_fragmentation * 0.14)
            + (field_perception_pressure * 0.12)
            + (field_perception_fragmentation * 0.10)
            + (field_perception_strain * 0.08)
            + (min(1.0, float(field_areal_count) / 4.0) * 0.10),
        ),
    )

    thought_areal_support = max(
        0.0,
        min(
            1.0,
            (areal_support * 0.34)
            + (processing_areal_support * 0.24)
            + (field_areal_stability_mean * 0.18)
            + (field_areal_coherence_mean * 0.14)
            + (field_perception_support * 0.12)
            + (field_perception_clarity * 0.08)
            + (field_perception_stability * 0.08)
            + (field_perception_focus * 0.04)
            + (field_areal_dominance * 0.10)
            - (field_areal_fragmentation * 0.12),
        ),
    )

    decision_conflict = max(
        0.0,
        min(
            1.0,
            1.0
            - min(1.0, abs(long_score - short_score) / 1.2)
            + (float(felt.get("felt_conflict", 0.0) or 0.0) * 0.16)
            + (processing_tension * 0.10)
            + (max(0.0, 1.0 - processing_alignment) * 0.08)
            + (thought_areal_pressure * 0.12)
            + (field_perception_pressure * 0.06)
            + (field_perception_fragmentation * 0.06)
            - (thought_areal_support * 0.08),
        ),
    )

    state_maturity = max(
        0.0,
        min(
            1.0,
            (float(felt.get("reflection_maturity", 0.0) or 0.0) * 0.18)
            + (float(felt.get("experience_regulation", 0.0) or 0.0) * 0.14)
            + (float(felt.get("felt_stability", 0.0) or 0.0) * 0.10)
            + (float(perception.get("signal_quality", 0.0) or 0.0) * 0.10)
            + (max(0.0, 1.0 - uncertainty_score) * 0.08)
            + (processing_stability * 0.10)
            + (processing_alignment * 0.08)
            + (felt_alignment * 0.08)
            + (market_balance * 0.06)
            + (visual_reflective_coherence * 0.06)
            + (thought_areal_support * 0.16)
            + (field_perception_clarity * 0.08)
            + (field_perception_stability * 0.06)
            - (decision_conflict * 0.14)
            - (thought_areal_pressure * 0.10),
        ),
    )

    rumination_depth = max(
        0.0,
        min(
            1.0,
            (decision_conflict * 0.28)
            + (float(perception.get("observe_priority", 0.0) or 0.0) * 0.16)
            + (float(felt.get("felt_pressure", 0.0) or 0.0) * 0.10)
            + (processing_load * 0.12)
            + (processing_tension * 0.08)
            + (breakout_tension * 0.06)
            + (thought_areal_pressure * 0.14)
            + (field_perception_pressure * 0.08)
            + (field_perception_strain * 0.06)
            - (thought_areal_support * 0.08)
            + (0.10 if bool(fused_state.get("observation_mode", False)) else 0.0),
        ),
    )

    inner_time_scale = max(
        0.0,
        min(
            1.0,
            (state_maturity * 0.22)
            + (float(felt.get("load_bearing_capacity", 0.0) or 0.0) * 0.10)
            + (max(0.0, 1.0 - float(perception.get("novelty_score", 0.0) or 0.0)) * 0.08)
            + (processing_alignment * 0.14)
            + (processing_stability * 0.12)
            + (visual_reflective_coherence * 0.08)
            + (market_balance * 0.06)
            + (thought_areal_support * 0.12)
            + (field_perception_clarity * 0.08)
            + (field_perception_focus * 0.05)
            - (processing_tension * 0.08)
            - (thought_areal_pressure * 0.08)
            + max(0.0, 1.0 - (abs(float((tension_state or {}).get("coherence", 0.0) or 0.0)) * 0.18)),
        ),
    )

    decision_pressure = max(
        0.0,
        min(
            1.0,
            (float(felt.get("felt_pressure", 0.0) or 0.0) * 0.24)
            + (breakout_tension * 0.16)
            + (processing_tension * 0.14)
            + (max(0.0, abs(long_score - short_score)) * 0.08)
            + (thought_areal_pressure * 0.16)
            + (field_perception_pressure * 0.08)
            + (field_perception_strain * 0.05)
            - (market_balance * 0.08)
            - (visual_reflective_coherence * 0.06)
            - (thought_areal_support * 0.08),
        ),
    )

    decision_readiness = max(
        0.0,
        min(
            1.0,
            (state_maturity * 0.24)
            + (max(0.0, 1.0 - decision_conflict) * 0.14)
            + (float(perception.get("signal_quality", 0.0) or 0.0) * 0.10)
            + (float(felt.get("felt_stability", 0.0) or 0.0) * 0.08)
            + (processing_readiness * 0.20)
            + (felt_alignment * 0.08)
            + (thought_areal_support * 0.14)
            + (field_perception_clarity * 0.08)
            + (field_perception_stability * 0.06)
            - (rumination_depth * 0.08)
            - (decision_pressure * 0.06)
            - (thought_areal_pressure * 0.10),
        ),
    )

    thought_alignment = max(
        0.0,
        min(
            1.0,
            (processing_alignment * 0.28)
            + (felt_alignment * 0.20)
            + (market_balance * 0.12)
            + (visual_reflective_coherence * 0.10)
            + (max(0.0, 1.0 - decision_conflict) * 0.12)
            + (thought_areal_support * 0.18)
            + (field_perception_clarity * 0.08)
            + (field_perception_focus * 0.04)
            - (thought_areal_pressure * 0.10),
        ),
    )

    return {
        "long_hypothesis": float(long_score),
        "short_hypothesis": float(short_score),
        "wait_hypothesis": float(max(0.0, 1.0 - max(long_score, short_score))),
        "decision": str(decision),
        "decision_conflict": float(decision_conflict),
        "state_maturity": float(state_maturity),
        "rumination_depth": float(rumination_depth),
        "inner_time_scale": float(inner_time_scale),
        "decision_readiness": float(decision_readiness),
        "thought_alignment": float(thought_alignment),
        "decision_pressure": float(decision_pressure),
        "thought_areal_pressure": float(thought_areal_pressure),
        "thought_areal_support": float(thought_areal_support),
        "field_perception_pressure": float(field_perception_pressure),
        "field_perception_support": float(field_perception_support),
        "field_perception_clarity": float(field_perception_clarity),
        "field_perception_focus": float(field_perception_focus),
        "field_perception_stability": float(field_perception_stability),
        "field_perception_fragmentation": float(field_perception_fragmentation),
        "field_perception_strain": float(field_perception_strain),
        "dominant_activity_island_id": str(dominant_activity_island_id),
        "field_perception_label": str(field_perception_label),
        "field_activity_island_count": int(field_activity_island_count),
        "field_activity_island_activation_mean": float(field_activity_island_activation_mean),
        "field_activity_island_pressure_mean": float(field_activity_island_pressure_mean),
        "field_activity_island_coherence_mean": float(field_activity_island_coherence_mean),
        "field_activity_island_context_reactivation_mean": float(field_activity_island_context_reactivation_mean),
        "field_activity_island_spread": float(field_activity_island_spread),
        "field_areal_count": int(field_areal_count),
        "field_areal_dominance": float(field_areal_dominance),
        "field_areal_fragmentation": float(field_areal_fragmentation),
        "field_areal_conflict_mean": float(field_areal_conflict_mean),
        "visual_coherence": float(visual_coherence),
        "visual_reflective_coherence": float(visual_reflective_coherence),
        "uncertainty": float(uncertainty_score),
        "conflict": float(decision_conflict),
        "maturity": float(state_maturity),
        "readiness": float(decision_readiness),
        "dominant_tension_cause": str(felt.get("dominant_tension_cause", "-") or "-"),
    }

# --------------------------------------------------
# perception_stat
# --------------------------------------------------
# --------------------------------------------------
# register pending learning context
# --------------------------------------------------


__all__ = ["build_meta_regulation_state", "build_thought_state"]
