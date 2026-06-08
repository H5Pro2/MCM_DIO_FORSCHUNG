"""Felt-state construction for the MCM runtime.

This module owns the current felt-state computation. It receives the
expectation and neural-felt builders from the bridge layer so the calculation
can stay free of MCM_Brain_Modell.py imports.
"""

from core.mcm_preregulator import build_mcm_preregulator_state


def _clip01(value):
    try:
        value = float(value)
    except Exception:
        return 0.0
    return max(0.0, min(1.0, value))


def _collect_felt_input_axes(bot, stimulus, snapshot, perception_state, processing_state, expectation_state, inner_field_perception_state, neural_felt_builder):
    filtered_vision = dict((stimulus or {}).get("filtered_vision", {}) or {})
    perception = dict(perception_state or {})
    processing = dict(processing_state or {})
    snap = dict(snapshot or {})
    inner_field_state = dict(inner_field_perception_state or (getattr(bot, "inner_field_perception_state", {}) if bot is not None else {}) or {})
    neural_felt_state = dict(inner_field_state.get("neural_felt_state", {}) or {})
    if not neural_felt_state and inner_field_state:
        neural_felt_state = neural_felt_builder(inner_field_state)
    neural_felt_bearing = float(neural_felt_state.get("neural_felt_bearing", inner_field_state.get("neural_felt_bearing", 0.0)) or 0.0)
    neural_felt_pressure = float(neural_felt_state.get("neural_felt_pressure", inner_field_state.get("neural_felt_pressure", 0.0)) or 0.0)
    neural_felt_memory_resonance = float(neural_felt_state.get("neural_felt_memory_resonance", 0.0) or 0.0)
    neural_felt_context_reactivation = float(neural_felt_state.get("neural_felt_context_reactivation", 0.0) or 0.0)
    neural_felt_label = str(neural_felt_state.get("neural_felt_label", inner_field_state.get("neural_felt_label", "quiet_neural_felt")) or "quiet_neural_felt")
    competition_abs = abs(float(getattr(bot, "competition_bias", 0.0) or 0.0)) if bot is not None else 0.0
    habituation_level = float(getattr(bot, "habituation_level", 0.0) or 0.0) if bot is not None else 0.0
    
    structure_quality = float(perception.get("structure_quality", 0.0) or 0.0)
    stress_relief_potential = float(perception.get("stress_relief_potential", 0.0) or 0.0)
    context_confidence = float(perception.get("context_confidence", 0.0) or 0.0)
    market_balance = float(perception.get("market_balance", 0.0) or 0.0)
    breakout_tension = float(perception.get("breakout_tension", 0.0) or 0.0)
    visual_coherence = float(perception.get("visual_coherence", 0.0) or 0.0)
    visual_clarity = float(processing.get("visual_clarity", perception.get("visual_clarity", 0.0)) or 0.0)
    visual_object_stability = float(processing.get("visual_object_stability", perception.get("visual_object_stability", 0.0)) or 0.0)
    visual_form_novelty = float(processing.get("visual_form_novelty", perception.get("visual_form_novelty", 0.0)) or 0.0)
    visual_blindness = float(processing.get("visual_blindness", perception.get("visual_blindness", 0.0)) or 0.0)
    raw_visual_form_pressure = float(processing.get("visual_form_pressure", perception.get("visual_form_pressure", 0.0)) or 0.0)
    raw_visual_shape_resonance = float(processing.get("visual_shape_resonance", perception.get("visual_shape_resonance", 0.0)) or 0.0)
    visual_shape_fragility = float(processing.get("visual_shape_fragility", perception.get("visual_shape_fragility", 0.0)) or 0.0)
    visual_attention_state = dict(processing.get("visual_attention_state", perception.get("visual_attention_state", {})) or {})
    visual_attention_label = str(visual_attention_state.get("visual_attention_label", "background_form") or "background_form")
    visual_form_contact = float(visual_attention_state.get("visual_form_contact", processing.get("visual_form_contact", perception.get("visual_form_contact", 0.0))) or 0.0)
    visual_inspection_pull = float(visual_attention_state.get("visual_inspection_pull", processing.get("visual_inspection_pull", perception.get("visual_inspection_pull", 0.0))) or 0.0)
    visual_attention_depth = float(visual_attention_state.get("visual_attention_depth", processing.get("visual_attention_depth", perception.get("visual_attention_depth", 0.0))) or 0.0)
    visual_background_filter = float(visual_attention_state.get("visual_background_filter", processing.get("visual_background_filter", perception.get("visual_background_filter", 0.0))) or 0.0)
    visual_mcm_contact_weight = max(
        0.0,
        min(
            1.0,
            float(
                visual_attention_state.get(
                    "visual_mcm_contact_weight",
                    processing.get("visual_mcm_contact_weight", perception.get("visual_mcm_contact_weight", 0.35)),
                )
                or 0.0
            ),
        ),
    )
    memory_complexity_state = dict(getattr(bot, "memory_complexity_state", {}) or {}) if bot is not None else {}
    if bot is not None and not memory_complexity_state:
        runtime_state = dict(getattr(bot, "mcm_runtime_decision_state", {}) or {})
        memory_complexity_state = dict(runtime_state.get("memory_complexity_state", {}) or {})
    form_symbol_state = dict(getattr(bot, "form_symbol_state", {}) or {}) if bot is not None else {}
    previous_thought_state = dict(getattr(bot, "thought_state", {}) or {}) if bot is not None else {}
    outcome_state = dict(getattr(bot, "last_outcome_decomposition", {}) or {}) if bot is not None else {}
    if bot is not None:
        packet_feedback = dict(getattr(bot, "last_experience_packet_feedback", {}) or {})
        if packet_feedback:
            outcome_state = {**outcome_state, **packet_feedback}

    mcm_preregulator_state = build_mcm_preregulator_state(
        perception_state=perception,
        processing_state=processing,
        stimulus=stimulus,
        memory_state=memory_complexity_state,
        form_symbol_state=form_symbol_state,
        thought_state=previous_thought_state,
        outcome_state=outcome_state,
    )
    visual_mcm_contact_weight = float(mcm_preregulator_state.get("visual_mcm_contact_weight", visual_mcm_contact_weight) or 0.0)
    felt_visual_weight = max(0.0, min(1.0, 0.25 + (visual_mcm_contact_weight * 0.75)))
    visual_reflective_contact_weight = visual_mcm_contact_weight
    visual_reflective_coherence = float(mcm_preregulator_state.get("visual_reflective_coherence", visual_coherence) or 0.0)
    visual_form_pressure = float(mcm_preregulator_state.get("visual_form_pressure", raw_visual_form_pressure * felt_visual_weight) or 0.0)
    visual_shape_resonance = float(mcm_preregulator_state.get("visual_shape_resonance", raw_visual_shape_resonance * max(0.0, min(1.0, 0.35 + (visual_mcm_contact_weight * 0.65)))) or 0.0)
    spatial_bias = float(perception.get("spatial_bias", 0.0) or 0.0)
    directional_bias = float(perception.get("directional_bias", 0.0) or 0.0)
    signal_quality = float(perception.get("signal_quality", 0.0) or 0.0)
    uncertainty_score = float(perception.get("uncertainty_score", 0.0) or 0.0)
    processing_load = float(processing.get("processing_load", 0.0) or 0.0)
    processing_stability = float(processing.get("processing_stability", 0.0) or 0.0)
    processing_alignment = float(processing.get("processing_alignment", 0.0) or 0.0)
    processing_tension = float(processing.get("processing_tension", 0.0) or 0.0)
    processing_areal_tension = float(processing.get("processing_areal_tension", 0.0) or 0.0)
    processing_areal_support = float(processing.get("processing_areal_support", 0.0) or 0.0)
    field_perception_pressure = float(processing.get("field_perception_pressure", 0.0) or 0.0)
    field_perception_support = float(processing.get("field_perception_support", 0.0) or 0.0)
    field_perception_clarity = float(processing.get("field_perception_clarity", 0.0) or 0.0)
    field_perception_focus = float(processing.get("field_perception_focus", snap.get("field_perception_focus", 0.0)) or 0.0)
    field_perception_stability = float(processing.get("field_perception_stability", snap.get("field_perception_stability", 0.0)) or 0.0)
    field_perception_fragmentation = float(processing.get("field_perception_fragmentation", snap.get("field_perception_fragmentation", 0.0)) or 0.0)
    field_perception_strain = float(processing.get("field_perception_strain", snap.get("field_perception_strain", 0.0)) or 0.0)
    dominant_activity_island_id = str(processing.get("dominant_activity_island_id", snap.get("dominant_activity_island_id", "-")) or "-")
    field_perception_label = str(processing.get("field_perception_label", inner_field_state.get("field_perception_label", "quiet_field")) or "quiet_field").strip().lower()
    field_areal_count = int(snap.get("field_areal_count", processing.get("field_areal_count", 0)) or 0)
    field_areal_stability_mean = float(snap.get("field_areal_stability_mean", processing.get("field_areal_stability_mean", 0.0)) or 0.0)
    field_areal_pressure_mean = float(snap.get("field_areal_pressure_mean", processing.get("field_areal_pressure_mean", 0.0)) or 0.0)
    field_areal_drift = float(snap.get("field_areal_drift", processing.get("field_areal_drift", 0.0)) or 0.0)
    field_areal_dominance = float(snap.get("field_areal_dominance", processing.get("field_areal_dominance", 0.0)) or 0.0)
    field_areal_fragmentation = float(snap.get("field_areal_fragmentation", processing.get("field_areal_fragmentation", 0.0)) or 0.0)
    field_areal_coherence_mean = float(snap.get("field_areal_coherence_mean", processing.get("field_areal_coherence_mean", 0.0)) or 0.0)
    field_areal_conflict_mean = float(snap.get("field_areal_conflict_mean", processing.get("field_areal_conflict_mean", 0.0)) or 0.0)
    field_activity_island_count = int(snap.get("field_activity_island_count", processing.get("field_activity_island_count", 0)) or 0)
    field_activity_island_activation_mean = float(snap.get("field_activity_island_activation_mean", processing.get("field_activity_island_activation_mean", 0.0)) or 0.0)
    field_activity_island_pressure_mean = float(snap.get("field_activity_island_pressure_mean", processing.get("field_activity_island_pressure_mean", 0.0)) or 0.0)
    field_activity_island_coherence_mean = float(snap.get("field_activity_island_coherence_mean", processing.get("field_activity_island_coherence_mean", 0.0)) or 0.0)
    field_activity_island_context_reactivation_mean = float(snap.get("field_activity_island_context_reactivation_mean", processing.get("field_activity_island_context_reactivation_mean", 0.0)) or 0.0)
    field_activity_island_spread = float(snap.get("field_activity_island_spread", processing.get("field_activity_island_spread", 0.0)) or 0.0)
    
    entry_expectation = float((expectation_state or {}).get("entry_expectation", 0.0) or 0.0)
    target_expectation = float((expectation_state or {}).get("target_expectation", 0.0) or 0.0)
    approach_pressure = float((expectation_state or {}).get("approach_pressure", 0.0) or 0.0)
    pressure_release = float((expectation_state or {}).get("pressure_release", 0.0) or 0.0)
    experience_regulation = float((expectation_state or {}).get("experience_regulation", 0.0) or 0.0)
    reflection_maturity = float((expectation_state or {}).get("reflection_maturity", 0.0) or 0.0)
    load_bearing_capacity = float((expectation_state or {}).get("load_bearing_capacity", 0.0) or 0.0)
    protective_width_regulation = float((expectation_state or {}).get("protective_width_regulation", 0.0) or 0.0)
    protective_courage = float((expectation_state or {}).get("protective_courage", 0.0) or 0.0)

    return {
        "filtered_vision": filtered_vision,
        "perception": perception,
        "processing": processing,
        "snap": snap,
        "inner_field_state": inner_field_state,
        "neural_felt_state": neural_felt_state,
        "neural_felt_bearing": neural_felt_bearing,
        "neural_felt_pressure": neural_felt_pressure,
        "neural_felt_memory_resonance": neural_felt_memory_resonance,
        "neural_felt_context_reactivation": neural_felt_context_reactivation,
        "neural_felt_label": neural_felt_label,
        "competition_abs": competition_abs,
        "habituation_level": habituation_level,
        "structure_quality": structure_quality,
        "stress_relief_potential": stress_relief_potential,
        "context_confidence": context_confidence,
        "market_balance": market_balance,
        "breakout_tension": breakout_tension,
        "visual_coherence": visual_coherence,
        "visual_reflective_coherence": visual_reflective_coherence,
        "visual_clarity": visual_clarity,
        "visual_object_stability": visual_object_stability,
        "visual_form_novelty": visual_form_novelty,
        "visual_blindness": visual_blindness,
        "visual_form_pressure": visual_form_pressure,
        "raw_visual_form_pressure": raw_visual_form_pressure,
        "visual_shape_resonance": visual_shape_resonance,
        "raw_visual_shape_resonance": raw_visual_shape_resonance,
        "visual_shape_fragility": visual_shape_fragility,
        "visual_attention_state": visual_attention_state,
        "visual_attention_label": visual_attention_label,
        "visual_form_contact": visual_form_contact,
        "visual_inspection_pull": visual_inspection_pull,
        "visual_attention_depth": visual_attention_depth,
        "visual_background_filter": visual_background_filter,
        "visual_mcm_contact_weight": visual_mcm_contact_weight,
        "visual_reflective_contact_weight": visual_reflective_contact_weight,
        "felt_visual_weight": felt_visual_weight,
        "spatial_bias": spatial_bias,
        "directional_bias": directional_bias,
        "signal_quality": signal_quality,
        "uncertainty_score": uncertainty_score,
        "processing_load": processing_load,
        "processing_stability": processing_stability,
        "processing_alignment": processing_alignment,
        "processing_tension": processing_tension,
        "processing_areal_tension": processing_areal_tension,
        "processing_areal_support": processing_areal_support,
        "field_perception_pressure": field_perception_pressure,
        "field_perception_support": field_perception_support,
        "field_perception_clarity": field_perception_clarity,
        "field_perception_focus": field_perception_focus,
        "field_perception_stability": field_perception_stability,
        "field_perception_fragmentation": field_perception_fragmentation,
        "field_perception_strain": field_perception_strain,
        "dominant_activity_island_id": dominant_activity_island_id,
        "field_perception_label": field_perception_label,
        "field_areal_count": field_areal_count,
        "field_areal_stability_mean": field_areal_stability_mean,
        "field_areal_pressure_mean": field_areal_pressure_mean,
        "field_areal_drift": field_areal_drift,
        "field_areal_dominance": field_areal_dominance,
        "field_areal_fragmentation": field_areal_fragmentation,
        "field_areal_coherence_mean": field_areal_coherence_mean,
        "field_areal_conflict_mean": field_areal_conflict_mean,
        "field_activity_island_count": field_activity_island_count,
        "field_activity_island_activation_mean": field_activity_island_activation_mean,
        "field_activity_island_pressure_mean": field_activity_island_pressure_mean,
        "field_activity_island_coherence_mean": field_activity_island_coherence_mean,
        "field_activity_island_context_reactivation_mean": field_activity_island_context_reactivation_mean,
        "field_activity_island_spread": field_activity_island_spread,
        "entry_expectation": entry_expectation,
        "target_expectation": target_expectation,
        "approach_pressure": approach_pressure,
        "pressure_release": pressure_release,
        "experience_regulation": experience_regulation,
        "reflection_maturity": reflection_maturity,
        "load_bearing_capacity": load_bearing_capacity,
        "protective_width_regulation": protective_width_regulation,
        "protective_courage": protective_courage,
        "mcm_preregulator_state": dict(mcm_preregulator_state or {}),
        "mcm_reflective_bearing": float(mcm_preregulator_state.get("mcm_reflective_bearing", 0.0) or 0.0),
        "mcm_reflective_pressure": float(mcm_preregulator_state.get("mcm_reflective_pressure", 0.0) or 0.0),
        "mcm_reflective_coupling_load": float(mcm_preregulator_state.get("mcm_reflective_coupling_load", 0.0) or 0.0),
        "mcm_reflective_displacement": float(mcm_preregulator_state.get("mcm_reflective_displacement", 0.0) or 0.0),
        "mcm_reflective_field_position": float(mcm_preregulator_state.get("mcm_reflective_field_position", 0.0) or 0.0),
        "mcm_reflective_tension": float(mcm_preregulator_state.get("mcm_reflective_tension", 0.0) or 0.0),
        "mcm_reflective_state": str(mcm_preregulator_state.get("mcm_reflective_state", "0") or "0"),
    }


def _compute_felt_areal_axes(axes):
    field_areal_count = axes["field_areal_count"]
    field_areal_stability_mean = axes["field_areal_stability_mean"]
    field_areal_pressure_mean = axes["field_areal_pressure_mean"]
    field_areal_drift = axes["field_areal_drift"]
    field_areal_dominance = axes["field_areal_dominance"]
    field_areal_fragmentation = axes["field_areal_fragmentation"]
    field_areal_coherence_mean = axes["field_areal_coherence_mean"]
    field_areal_conflict_mean = axes["field_areal_conflict_mean"]
    processing_areal_support = axes["processing_areal_support"]
    processing_areal_tension = axes["processing_areal_tension"]
    field_perception_support = axes["field_perception_support"]
    field_perception_stability = axes["field_perception_stability"]
    field_perception_focus = axes["field_perception_focus"]
    field_perception_pressure = axes["field_perception_pressure"]
    field_perception_fragmentation = axes["field_perception_fragmentation"]
    field_perception_strain = axes["field_perception_strain"]
    neural_felt_bearing = axes["neural_felt_bearing"]
    neural_felt_pressure = axes["neural_felt_pressure"]
    mcm_reflective_bearing = axes["mcm_reflective_bearing"]
    mcm_reflective_pressure = axes["mcm_reflective_pressure"]
    mcm_reflective_coupling_load = axes["mcm_reflective_coupling_load"]

    areal_presence = max(0.0, min(1.0, float(field_areal_count) / 4.0))
    areal_support = max(
        0.0,
        min(
            1.0,
            (field_areal_stability_mean * 0.28)
            + (field_areal_coherence_mean * 0.24)
            + (field_areal_dominance * 0.12)
            + (processing_areal_support * 0.18)
            + (field_perception_support * 0.12)
            + (field_perception_stability * 0.08)
            + (field_perception_focus * 0.04)
            + (max(0.0, 1.0 - field_areal_fragmentation) * 0.10)
            + (max(0.0, 1.0 - field_areal_conflict_mean) * 0.08)
            + (neural_felt_bearing * 0.08)
            + (mcm_reflective_bearing * 0.10)
            + (max(0.0, 1.0 - mcm_reflective_coupling_load) * 0.04),
        ),
    )

    areal_conflict_pressure = max(
        0.0,
        min(
            1.0,
            (field_areal_conflict_mean * 0.32)
            + (field_areal_fragmentation * 0.22)
            + (field_areal_pressure_mean * 0.18)
            + (processing_areal_tension * 0.14)
            + (field_perception_pressure * 0.12)
            + (field_perception_fragmentation * 0.10)
            + (field_perception_strain * 0.08)
            + (min(1.0, field_areal_drift) * 0.08)
            + (areal_presence * 0.06)
            + (neural_felt_pressure * 0.08)
            + (mcm_reflective_pressure * 0.12)
            + (mcm_reflective_coupling_load * max(0.0, 0.34 - mcm_reflective_bearing) * 0.10),
        ),
    )

    return {
        "areal_presence": areal_presence,
        "areal_support": areal_support,
        "areal_conflict_pressure": areal_conflict_pressure,
    }


def _compute_felt_valence_axes(axes, areal_axes):
    filtered_vision = axes["filtered_vision"]
    perception = axes["perception"]
    structure_quality = axes["structure_quality"]
    stress_relief_potential = axes["stress_relief_potential"]
    market_balance = axes["market_balance"]
    breakout_tension = axes["breakout_tension"]
    visual_coherence = axes["visual_coherence"]
    visual_reflective_coherence = axes.get("visual_reflective_coherence", visual_coherence)
    spatial_bias = axes["spatial_bias"]
    directional_bias = axes["directional_bias"]
    signal_quality = axes["signal_quality"]
    uncertainty_score = axes["uncertainty_score"]
    processing_alignment = axes["processing_alignment"]
    processing_tension = axes["processing_tension"]
    field_perception_pressure = axes["field_perception_pressure"]
    field_perception_support = axes["field_perception_support"]
    field_perception_clarity = axes["field_perception_clarity"]
    field_perception_focus = axes["field_perception_focus"]
    field_perception_fragmentation = axes["field_perception_fragmentation"]
    field_perception_strain = axes["field_perception_strain"]
    competition_abs = axes["competition_abs"]
    areal_support = areal_axes["areal_support"]
    areal_conflict_pressure = areal_axes["areal_conflict_pressure"]
    mcm_reflective_bearing = axes["mcm_reflective_bearing"]
    mcm_reflective_pressure = axes["mcm_reflective_pressure"]
    hearing_reflective_pressure = float(axes["mcm_preregulator_state"].get("hearing_reflective_pressure", 0.0) or 0.0)

    felt_risk = max(
        0.0,
        min(
            1.0,
            (float(filtered_vision.get("threat_map", 0.0) or 0.0) * 0.22)
            + (uncertainty_score * 0.16)
            + (float(perception.get("noise_damp", 0.0) or 0.0) * 0.10)
            + (breakout_tension * 0.16)
            + (max(0.0, 1.0 - market_balance) * 0.10)
            + (max(0.0, 1.0 - visual_reflective_coherence) * 0.06)
            + (processing_tension * 0.06)
            + (areal_conflict_pressure * 0.12)
            + (field_perception_pressure * 0.08)
            + (field_perception_strain * 0.06)
            + (field_perception_fragmentation * 0.04)
            + (mcm_reflective_pressure * 0.10)
            + (hearing_reflective_pressure * 0.04)
            - (stress_relief_potential * 0.08)
            - (areal_support * 0.10)
            - (mcm_reflective_bearing * 0.06),
        ),
    )

    felt_opportunity = max(
        0.0,
        min(
            1.0,
            (float(filtered_vision.get("target_map", 0.0) or 0.0) * 0.22)
            + (signal_quality * 0.16)
            + (float(perception.get("target_lock", 0.0) or 0.0) * 0.10)
            + (structure_quality * 0.08)
            + (market_balance * 0.12)
            + (visual_reflective_coherence * 0.10)
            + (processing_alignment * 0.12)
            + (areal_support * 0.14)
            + (field_perception_support * 0.08)
            + (field_perception_clarity * 0.05)
            + (field_perception_focus * 0.04)
            + (mcm_reflective_bearing * 0.10)
            - (processing_tension * 0.04)
            - (areal_conflict_pressure * 0.08),
        ),
    )

    felt_conflict = max(
        0.0,
        min(
            1.0,
            (abs(felt_opportunity - felt_risk) * 0.14)
            + (min(felt_opportunity, felt_risk) * 0.46)
            + (competition_abs * 0.08)
            + (abs(spatial_bias - directional_bias) * 0.08)
            + (max(0.0, processing_tension - processing_alignment) * 0.10)
            + (areal_conflict_pressure * 0.14)
            + (field_perception_pressure * 0.08)
            + (field_perception_fragmentation * 0.06),
        ),
    )

    return {
        "felt_risk": felt_risk,
        "felt_opportunity": felt_opportunity,
        "felt_conflict": felt_conflict,
    }


def _compute_felt_core_regulation_axes(axes, areal_axes, valence_axes):
    stress_relief_potential = axes["stress_relief_potential"]
    context_confidence = axes["context_confidence"]
    market_balance = axes["market_balance"]
    breakout_tension = axes["breakout_tension"]
    visual_coherence = axes["visual_coherence"]
    visual_reflective_coherence = axes.get("visual_reflective_coherence", visual_coherence)
    uncertainty_score = axes["uncertainty_score"]
    processing_load = axes["processing_load"]
    processing_stability = axes["processing_stability"]
    processing_alignment = axes["processing_alignment"]
    processing_tension = axes["processing_tension"]
    field_perception_pressure = axes["field_perception_pressure"]
    field_perception_clarity = axes["field_perception_clarity"]
    entry_expectation = axes["entry_expectation"]
    approach_pressure = axes["approach_pressure"]
    pressure_release = axes["pressure_release"]
    experience_regulation = axes["experience_regulation"]
    neural_felt_bearing = axes["neural_felt_bearing"]
    neural_felt_pressure = axes["neural_felt_pressure"]
    neural_felt_context_reactivation = axes["neural_felt_context_reactivation"]
    mcm_reflective_bearing = axes["mcm_reflective_bearing"]
    mcm_reflective_pressure = axes["mcm_reflective_pressure"]
    mcm_reflective_coupling_load = axes["mcm_reflective_coupling_load"]
    areal_support = areal_axes["areal_support"]
    areal_conflict_pressure = areal_axes["areal_conflict_pressure"]
    felt_risk = valence_axes["felt_risk"]
    felt_opportunity = valence_axes["felt_opportunity"]
    felt_conflict = valence_axes["felt_conflict"]

    felt_pressure = max(
        0.0,
        min(
            1.0,
            (approach_pressure * 0.26)
            + (entry_expectation * 0.10)
            + (felt_opportunity * 0.08)
            + (felt_risk * 0.08)
            + (breakout_tension * 0.14)
            + (processing_load * 0.10)
            + (processing_tension * 0.08)
            + (areal_conflict_pressure * 0.12)
            + (neural_felt_pressure * 0.06)
            + (neural_felt_context_reactivation * 0.02)
            + (field_perception_pressure * 0.08)
            + (mcm_reflective_pressure * 0.10)
            + (mcm_reflective_coupling_load * max(0.0, 0.30 - mcm_reflective_bearing) * 0.08)
            - (stress_relief_potential * 0.06)
            - (market_balance * 0.04)
            - (areal_support * 0.06)
            - (mcm_reflective_bearing * 0.04),
        ),
    )

    felt_stability = max(
        0.0,
        min(
            1.0,
            1.0
            - (uncertainty_score * 0.18)
            - (felt_conflict * 0.16)
            - (pressure_release * 0.06)
            - (felt_pressure * 0.08)
            - (areal_conflict_pressure * 0.10)
            + (experience_regulation * 0.10)
            + (context_confidence * 0.08)
            + (market_balance * 0.10)
            + (visual_reflective_coherence * 0.10)
            + (processing_stability * 0.12)
            + (areal_support * 0.14)
            + (field_perception_clarity * 0.08)
            + (neural_felt_bearing * 0.06)
            + (mcm_reflective_bearing * 0.08)
            - (neural_felt_pressure * 0.04)
            - (mcm_reflective_pressure * 0.04),
        ),
    )

    felt_alignment = max(
        0.0,
        min(
            1.0,
            (processing_alignment * 0.30)
            + (market_balance * 0.14)
            + (visual_reflective_coherence * 0.14)
            + (context_confidence * 0.10)
            + (axes["structure_quality"] * 0.08)
            + (max(0.0, 1.0 - felt_conflict) * 0.08)
            + (areal_support * 0.16)
            + (field_perception_clarity * 0.08)
            + (neural_felt_bearing * 0.05)
            + (mcm_reflective_bearing * 0.08)
            - (neural_felt_pressure * 0.03)
            - (areal_conflict_pressure * 0.10)
            - (mcm_reflective_pressure * 0.04),
        ),
    )

    return {
        "felt_pressure": felt_pressure,
        "felt_stability": felt_stability,
        "felt_alignment": felt_alignment,
    }


def _compute_felt_tension_cause_axes(axes, areal_axes, valence_axes, core_regulation_axes):
    filtered_vision = axes["filtered_vision"]
    context_confidence = axes["context_confidence"]
    market_balance = axes["market_balance"]
    breakout_tension = axes["breakout_tension"]
    visual_coherence = axes["visual_coherence"]
    visual_reflective_coherence = axes.get("visual_reflective_coherence", visual_coherence)
    spatial_bias = axes["spatial_bias"]
    directional_bias = axes["directional_bias"]
    signal_quality = axes["signal_quality"]
    uncertainty_score = axes["uncertainty_score"]
    processing_load = axes["processing_load"]
    processing_stability = axes["processing_stability"]
    processing_alignment = axes["processing_alignment"]
    processing_tension = axes["processing_tension"]
    processing_areal_tension = axes["processing_areal_tension"]
    field_perception_pressure = axes["field_perception_pressure"]
    field_perception_support = axes["field_perception_support"]
    field_perception_clarity = axes["field_perception_clarity"]
    competition_abs = axes["competition_abs"]
    habituation_level = axes["habituation_level"]
    entry_expectation = axes["entry_expectation"]
    target_expectation = axes["target_expectation"]
    approach_pressure = axes["approach_pressure"]
    pressure_release = axes["pressure_release"]
    experience_regulation = axes["experience_regulation"]
    reflection_maturity = axes["reflection_maturity"]
    load_bearing_capacity = axes["load_bearing_capacity"]
    protective_width_regulation = axes["protective_width_regulation"]
    protective_courage = axes["protective_courage"]
    areal_support = areal_axes["areal_support"]
    areal_conflict_pressure = areal_axes["areal_conflict_pressure"]
    felt_risk = valence_axes["felt_risk"]
    felt_conflict = valence_axes["felt_conflict"]
    felt_pressure = core_regulation_axes["felt_pressure"]
    felt_alignment = core_regulation_axes["felt_alignment"]

    external_pressure = max(
        0.0,
        min(
            1.0,
            (breakout_tension * 0.26)
            + (max(0.0, 1.0 - market_balance) * 0.16)
            + (max(0.0, 1.0 - visual_reflective_coherence) * 0.12)
            + (uncertainty_score * 0.10)
            + (processing_tension * 0.10)
            + (float(filtered_vision.get("threat_map", 0.0) or 0.0) * 0.12)
            + (max(0.0, 1.0 - context_confidence) * 0.06),
        ),
    )

    inner_conflict_pressure = max(
        0.0,
        min(
            1.0,
            (felt_conflict * 0.38)
            + (competition_abs * 0.12)
            + (abs(spatial_bias - directional_bias) * 0.10)
            + (max(0.0, processing_tension - processing_alignment) * 0.14)
            + (max(0.0, 1.0 - felt_alignment) * 0.08)
            + (max(0.0, 1.0 - processing_stability) * 0.06)
            + (areal_conflict_pressure * 0.12)
            + (field_perception_pressure * 0.08),
        ),
    )

    repetition_pressure = max(
        0.0,
        min(
            1.0,
            (habituation_level * 0.28)
            + (approach_pressure * 0.18)
            + (entry_expectation * 0.16)
            + (competition_abs * 0.08)
            + (max(0.0, 1.0 - experience_regulation) * 0.12)
            + (max(0.0, 1.0 - reflection_maturity) * 0.08)
            + (pressure_release * 0.10),
        ),
    )

    expectation_pressure = max(
        0.0,
        min(
            1.0,
            (approach_pressure * 0.40)
            + (entry_expectation * 0.18)
            + (target_expectation * 0.12)
            + (felt_pressure * 0.10)
            + (max(0.0, 1.0 - protective_width_regulation) * 0.06)
            + (max(0.0, 1.0 - load_bearing_capacity) * 0.08)
            + (areal_conflict_pressure * 0.06)
            + (field_perception_pressure * 0.06),
        ),
    )

    uncertainty_pressure = max(
        0.0,
        min(
            1.0,
            (uncertainty_score * 0.34)
            + (processing_load * 0.14)
            + (processing_tension * 0.10)
            + (max(0.0, 1.0 - context_confidence) * 0.10)
            + (max(0.0, 1.0 - signal_quality) * 0.08)
            + (max(0.0, 1.0 - visual_reflective_coherence) * 0.08)
            + (processing_areal_tension * 0.08)
            + (field_perception_pressure * 0.08),
        ),
    )

    aftereffect_pressure = max(
        0.0,
        min(
            1.0,
            (pressure_release * 0.28)
            + (max(0.0, 1.0 - experience_regulation) * 0.20)
            + (max(0.0, 1.0 - reflection_maturity) * 0.16)
            + (max(0.0, 1.0 - load_bearing_capacity) * 0.12)
            + (felt_risk * 0.08)
            + (max(0.0, 1.0 - protective_courage) * 0.10)
            + (max(0.0, 1.0 - areal_support) * 0.06)
            + (max(0.0, 1.0 - field_perception_support) * 0.05),
        ),
    )

    tension_cause_map = {
        "external_pressure": float(external_pressure),
        "inner_conflict_pressure": float(inner_conflict_pressure),
        "repetition_pressure": float(repetition_pressure),
        "expectation_pressure": float(expectation_pressure),
        "uncertainty_pressure": float(uncertainty_pressure),
        "aftereffect_pressure": float(aftereffect_pressure),
        "areal_conflict_pressure": float(areal_conflict_pressure),
        "field_perception_pressure": float(field_perception_pressure),
    }
    dominant_tension_cause = max(tension_cause_map, key=tension_cause_map.get)
    dominant_tension_value = float(tension_cause_map.get(dominant_tension_cause, 0.0) or 0.0)

    return {
        "external_pressure": external_pressure,
        "inner_conflict_pressure": inner_conflict_pressure,
        "repetition_pressure": repetition_pressure,
        "expectation_pressure": expectation_pressure,
        "uncertainty_pressure": uncertainty_pressure,
        "aftereffect_pressure": aftereffect_pressure,
        "dominant_tension_cause": dominant_tension_cause,
        "dominant_tension_value": dominant_tension_value,
    }


def _compute_felt_observation_need(axes, areal_axes, core_regulation_axes, tension_axes):
    context_confidence = axes["context_confidence"]
    signal_quality = axes["signal_quality"]
    processing_load = axes["processing_load"]
    areal_conflict_pressure = areal_axes["areal_conflict_pressure"]
    felt_pressure = core_regulation_axes["felt_pressure"]
    felt_stability = core_regulation_axes["felt_stability"]
    external_pressure = tension_axes["external_pressure"]
    uncertainty_pressure = tension_axes["uncertainty_pressure"]
    aftereffect_pressure = tension_axes["aftereffect_pressure"]

    return max(
        0.0,
        min(
            1.0,
            (external_pressure * 0.18)
            + (uncertainty_pressure * 0.18)
            + (aftereffect_pressure * 0.14)
            + (felt_pressure * 0.08)
            + (processing_load * 0.08)
            + (areal_conflict_pressure * 0.18)
            + (max(0.0, 1.0 - felt_stability) * 0.08)
            + (max(0.0, 1.0 - context_confidence) * 0.04)
            + (max(0.0, 1.0 - signal_quality) * 0.04),
        ),
    )


def _compute_felt_regulation_axes(axes, areal_axes, valence_axes):
    core_regulation_axes = _compute_felt_core_regulation_axes(axes, areal_axes, valence_axes)
    tension_axes = _compute_felt_tension_cause_axes(axes, areal_axes, valence_axes, core_regulation_axes)
    pre_action_observation_need = _compute_felt_observation_need(
        axes,
        areal_axes,
        core_regulation_axes,
        tension_axes,
    )

    return {
        **core_regulation_axes,
        **tension_axes,
        "pre_action_observation_need": pre_action_observation_need,
    }


def _resolve_market_feel_state(axes, areal_axes, valence_axes, regulation_axes):
    field_perception_label = axes["field_perception_label"]
    field_perception_pressure = axes["field_perception_pressure"]
    field_perception_clarity = axes["field_perception_clarity"]
    breakout_tension = axes["breakout_tension"]
    areal_conflict_pressure = areal_axes["areal_conflict_pressure"]
    felt_risk = valence_axes["felt_risk"]
    felt_opportunity = valence_axes["felt_opportunity"]
    felt_conflict = valence_axes["felt_conflict"]
    felt_pressure = regulation_axes["felt_pressure"]
    felt_stability = regulation_axes["felt_stability"]

    market_feel_pressures = {
        "threatened": _clip01((felt_risk * 0.42) + ((felt_risk - felt_opportunity) * 0.24) + (felt_pressure * 0.10)),
        "drawn": _clip01((felt_opportunity * 0.42) + ((felt_opportunity - felt_risk) * 0.24) + (field_perception_clarity * 0.08)),
        "fragmented": _clip01((areal_conflict_pressure * 0.40) + (felt_conflict * 0.18)),
        "field_fragmented": _clip01((field_perception_pressure * 0.30) + (areal_conflict_pressure * 0.12) + (0.18 if field_perception_label == "fragmented_perception_field" else 0.0)),
        "field_coherent": _clip01((field_perception_clarity * 0.34) + (felt_stability * 0.14) + (0.18 if field_perception_label == "coherent_perception_field" else 0.0)),
        "conflicted": _clip01((felt_conflict * 0.36) + (areal_conflict_pressure * 0.16)),
        "tense": _clip01((felt_pressure * 0.30) + (breakout_tension * 0.26) + ((1.0 - felt_stability) * 0.08)),
        "unstable": _clip01(((1.0 - felt_stability) * 0.38) + (felt_conflict * 0.10)),
        "balanced": _clip01((felt_stability * 0.30) + ((1.0 - felt_conflict) * 0.14) + ((1.0 - areal_conflict_pressure) * 0.10)),
    }
    market_feel_state = max(market_feel_pressures, key=market_feel_pressures.get)

    return market_feel_state


def _build_felt_state_payload(axes, areal_axes, valence_axes, regulation_axes, market_feel_state):
    return {
        "market_feel_state": str(market_feel_state),
        "felt_risk": float(valence_axes["felt_risk"]),
        "felt_opportunity": float(valence_axes["felt_opportunity"]),
        "felt_conflict": float(valence_axes["felt_conflict"]),
        "felt_pressure": float(regulation_axes["felt_pressure"]),
        "felt_stability": float(regulation_axes["felt_stability"]),
        "felt_alignment": float(regulation_axes["felt_alignment"]),
        "structure_quality": float(axes["structure_quality"]),
        "stress_relief_potential": float(axes["stress_relief_potential"]),
        "context_confidence": float(axes["context_confidence"]),
        "market_balance": float(axes["market_balance"]),
        "breakout_tension": float(axes["breakout_tension"]),
        "visual_coherence": float(axes["visual_coherence"]),
        "visual_reflective_coherence": float(axes["visual_reflective_coherence"]),
        "visual_clarity": float(axes["visual_clarity"]),
        "visual_object_stability": float(axes["visual_object_stability"]),
        "visual_form_novelty": float(axes["visual_form_novelty"]),
        "visual_blindness": float(axes["visual_blindness"]),
        "visual_form_pressure": float(axes["visual_form_pressure"]),
        "raw_visual_form_pressure": float(axes["raw_visual_form_pressure"]),
        "visual_shape_resonance": float(axes["visual_shape_resonance"]),
        "raw_visual_shape_resonance": float(axes["raw_visual_shape_resonance"]),
        "visual_shape_fragility": float(axes["visual_shape_fragility"]),
        "visual_attention_state": dict(axes["visual_attention_state"] or {}),
        "visual_attention_label": str(axes["visual_attention_label"]),
        "visual_form_contact": float(axes["visual_form_contact"]),
        "visual_inspection_pull": float(axes["visual_inspection_pull"]),
        "visual_attention_depth": float(axes["visual_attention_depth"]),
        "visual_background_filter": float(axes["visual_background_filter"]),
        "visual_mcm_contact_weight": float(axes["visual_mcm_contact_weight"]),
        "visual_reflective_contact_weight": float(axes["visual_reflective_contact_weight"]),
        "felt_visual_weight": float(axes["felt_visual_weight"]),
        "mcm_preregulator_state": dict(axes["mcm_preregulator_state"] or {}),
        "mcm_reflective_bearing": float(axes["mcm_reflective_bearing"]),
        "mcm_reflective_pressure": float(axes["mcm_reflective_pressure"]),
        "mcm_reflective_coupling_load": float(axes["mcm_reflective_coupling_load"]),
        "mcm_reflective_displacement": float(axes["mcm_reflective_displacement"]),
        "mcm_reflective_field_position": float(axes["mcm_reflective_field_position"]),
        "mcm_reflective_tension": float(axes["mcm_reflective_tension"]),
        "mcm_reflective_state": str(axes["mcm_reflective_state"]),
        "entry_expectation": float(axes["entry_expectation"]),
        "target_expectation": float(axes["target_expectation"]),
        "approach_pressure": float(axes["approach_pressure"]),
        "pressure_release": float(axes["pressure_release"]),
        "experience_regulation": float(axes["experience_regulation"]),
        "reflection_maturity": float(axes["reflection_maturity"]),
        "load_bearing_capacity": float(axes["load_bearing_capacity"]),
        "protective_width_regulation": float(axes["protective_width_regulation"]),
        "protective_courage": float(axes["protective_courage"]),
        "field_areal_count": int(axes["field_areal_count"]),
        "field_areal_stability_mean": float(axes["field_areal_stability_mean"]),
        "field_areal_pressure_mean": float(axes["field_areal_pressure_mean"]),
        "field_areal_drift": float(axes["field_areal_drift"]),
        "field_areal_dominance": float(axes["field_areal_dominance"]),
        "field_areal_fragmentation": float(axes["field_areal_fragmentation"]),
        "field_areal_coherence_mean": float(axes["field_areal_coherence_mean"]),
        "field_areal_conflict_mean": float(axes["field_areal_conflict_mean"]),
        "field_perception_pressure": float(axes["field_perception_pressure"]),
        "field_perception_support": float(axes["field_perception_support"]),
        "field_perception_clarity": float(axes["field_perception_clarity"]),
        "field_perception_focus": float(axes["field_perception_focus"]),
        "field_perception_stability": float(axes["field_perception_stability"]),
        "field_perception_fragmentation": float(axes["field_perception_fragmentation"]),
        "field_perception_strain": float(axes["field_perception_strain"]),
        "dominant_activity_island_id": str(axes["dominant_activity_island_id"]),
        "field_perception_label": str(axes["field_perception_label"]),
        "field_activity_island_count": int(axes["field_activity_island_count"]),
        "field_activity_island_activation_mean": float(axes["field_activity_island_activation_mean"]),
        "field_activity_island_pressure_mean": float(axes["field_activity_island_pressure_mean"]),
        "field_activity_island_coherence_mean": float(axes["field_activity_island_coherence_mean"]),
        "field_activity_island_context_reactivation_mean": float(axes["field_activity_island_context_reactivation_mean"]),
        "field_activity_island_spread": float(axes["field_activity_island_spread"]),
        "areal_support": float(areal_axes["areal_support"]),
        "areal_conflict_pressure": float(areal_axes["areal_conflict_pressure"]),
        "external_pressure": float(regulation_axes["external_pressure"]),
        "inner_conflict_pressure": float(regulation_axes["inner_conflict_pressure"]),
        "repetition_pressure": float(regulation_axes["repetition_pressure"]),
        "expectation_pressure": float(regulation_axes["expectation_pressure"]),
        "uncertainty_pressure": float(regulation_axes["uncertainty_pressure"]),
        "aftereffect_pressure": float(regulation_axes["aftereffect_pressure"]),
        "dominant_tension_cause": str(regulation_axes["dominant_tension_cause"]),
        "dominant_tension_value": float(regulation_axes["dominant_tension_value"]),
        "pre_action_observation_need": float(regulation_axes["pre_action_observation_need"]),
        "neural_felt_state": dict(axes["neural_felt_state"] or {}),
        "neural_felt_bearing": float(axes["neural_felt_bearing"]),
        "neural_felt_pressure": float(axes["neural_felt_pressure"]),
        "neural_felt_memory_resonance": float(axes["neural_felt_memory_resonance"]),
        "neural_felt_context_reactivation": float(axes["neural_felt_context_reactivation"]),
        "neural_felt_label": str(axes["neural_felt_label"]),
    }


def resolve_felt_state(bot, candle_state, stimulus, snapshot, perception_state, decision="WAIT", processing_state=None, expectation_state=None, inner_field_perception_state=None, *, expectation_builder, neural_felt_builder):

    if expectation_state is None:
        expectation_state = expectation_builder(
            bot,
            candle_state,
            stimulus,
            snapshot,
            decision=decision,
            visual_market_state=dict(getattr(bot, "visual_market_state", {}) or {}) if bot is not None else {},
        )
    axes = _collect_felt_input_axes(
        bot,
        stimulus,
        snapshot,
        perception_state,
        processing_state,
        expectation_state,
        inner_field_perception_state,
        neural_felt_builder,
    )
    areal_axes = _compute_felt_areal_axes(axes)
    valence_axes = _compute_felt_valence_axes(axes, areal_axes)
    regulation_axes = _compute_felt_regulation_axes(axes, areal_axes, valence_axes)
    market_feel_state = _resolve_market_feel_state(axes, areal_axes, valence_axes, regulation_axes)
    return _build_felt_state_payload(axes, areal_axes, valence_axes, regulation_axes, market_feel_state)
