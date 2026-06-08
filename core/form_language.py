"""DIO form-language construction.

This module builds DIO's compact internal sentence layer from form symbols,
MCM-field anchors, thought seeds, memory anchors, and action posture. It is a
translation layer, not a trading rule layer.
"""

import hashlib

from memory.thought_memory_store import _thought_memory_family_key


def _build_dio_form_language_state(seed_state, form_state=None, meta_regulation_state=None, runtime_result=None):
    seed = dict(seed_state or {})
    form = dict(form_state or {})
    meta = dict(meta_regulation_state or {})
    result = dict(runtime_result or {})

    def _clean(value):
        text = str(value or "-").replace("\n", " ").replace(";", "|").strip()
        return text or "-"

    def _clip(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(0.0, min(1.0, float(value)))

    def _signed_clip(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(-1.0, min(1.0, float(value)))

    def _bucket(value, step=0.10):
        value = _clip(value)
        step = max(0.01, float(step or 0.10))
        return f"{round(round(value / step) * step, 2):.2f}"

    form_word = _clean(form.get("form_symbol_id", seed.get("form_symbol_anchor", "-")))
    compound_word = _clean(form.get("form_symbol_compound_id", "-"))
    form_layer_word = _clean(form.get("form_symbol_semantic_primary_layer", "-"))
    form_family_word = _clean(form.get("uncertain_form_family_state", "-"))
    field_word = _clean(seed.get("mcm_field_anchor", meta.get("field_perception_label", "-")))
    thought_word = _clean(seed.get("thought_seed_id", "-"))
    structure_word = _clean(seed.get("emergent_structure_state", "-"))
    origin_word = _clean(seed.get("semantic_origin_state", meta.get("semantic_origin_state", "-")))
    reifung_word = _clean(seed.get("thought_reifung_direction", "-"))
    posture_word = _clean(seed.get("seed_metaregulator_state", "-"))
    action_word = _clean(seed.get("decision", result.get("decision", "WAIT")))
    phase_word = _clean(seed.get("phase", meta.get("pre_action_phase", "hold")))
    context_word = _clean(seed.get("experience_memory_anchor", result.get("context_cluster_id", "-")))
    thought_family_word, thought_family_key = _thought_memory_family_key(seed)
    world_experience_anchor = _clean(context_word)
    thought_experience_anchor = _clean(thought_family_word)

    form_density = _clip(form.get("form_symbol_semantic_density", 0.0))
    form_compression = _clip(form.get("form_symbol_semantic_compression", 0.0))
    form_coherence = _clip(form.get("form_symbol_semantic_coherence", 0.0))
    form_stability = _clip(form.get("form_symbol_stability", 0.0))
    thought_trace = _clip(seed.get("thought_trace_strength", 0.0))
    thought_recall_potential = _clip(seed.get("thought_recall_potential", 0.0))
    thought_maturity = _clip(seed.get("thought_maturity", 0.0))
    reality_binding = _clip(seed.get("reality_binding_score", 0.0))
    own_binding = _clip(seed.get("own_field_binding_pull", 0.0))
    borrowed_pressure = _clip(seed.get("borrowed_open_hypothesis_pressure", 0.0))
    drift_risk = _clip(seed.get("hallucination_drift_risk", 0.0))
    open_pressure = _clip(seed.get("thought_open_hypothesis_pressure", 0.0))
    thought_confirmation = _clip(seed.get("thought_confirmation_score", 0.0))
    structural_grounding = _clip(seed.get("thought_structural_grounding", 0.0))
    consequence_balance = _signed_clip(seed.get("thought_consequence_balance", 0.0))

    structure_quality = _clip(meta.get("structure_quality", result.get("structure_quality", 0.0)))
    context_confidence = _clip(meta.get("context_confidence", result.get("context_confidence", 0.0)))
    visual_clarity = _clip(meta.get("visual_clarity", result.get("visual_clarity", 0.0)))
    visual_stability = _clip(meta.get("visual_object_stability", result.get("visual_object_stability", 0.0)))
    area_bearing = _clip(meta.get("area_bearing_quality", result.get("entry_choice_bearing", 0.0)))
    structure_bearing = _clip(meta.get("structure_action_bearing", 0.0))
    inner_outer_alignment = _clip(meta.get("inner_outer_alignment", 0.0))
    contact_carrying = _clip(meta.get("contact_carrying_quality", 0.0))
    field_bearing_support = _clip(meta.get("field_bearing_support", meta.get("field_action_support", 0.0)))
    contact_overcoupling = _clip(meta.get("contact_overcoupling_risk", 0.0))
    field_observation_need = _clip(meta.get("field_observation_need", 0.0))
    felt_afterimage = _clip(meta.get("felt_afterimage", 0.0))

    form_to_mcm_recall = _clip(
        (form_density * 0.18)
        + (form_coherence * 0.16)
        + (form_stability * 0.14)
        + (thought_trace * 0.16)
        + (thought_recall_potential * 0.16)
        + (own_binding * 0.10)
        + (max(0.0, consequence_balance) * 0.06)
    )
    visual_mcm_context_fit = _clip(
        (structure_quality * 0.16)
        + (context_confidence * 0.10)
        + (visual_clarity * 0.10)
        + (visual_stability * 0.10)
        + (area_bearing * 0.10)
        + (structure_bearing * 0.08)
        + (inner_outer_alignment * 0.14)
        + (contact_carrying * 0.10)
        + (field_bearing_support * 0.08)
        + ((1.0 - contact_overcoupling) * 0.07)
        + ((1.0 - field_observation_need) * 0.04)
        + (felt_afterimage * 0.03)
    )
    mcm_to_form_confirmation = _clip(
        (inner_outer_alignment * 0.20)
        + (contact_carrying * 0.16)
        + (field_bearing_support * 0.12)
        + (thought_confirmation * 0.14)
        + (reality_binding * 0.14)
        + (structural_grounding * 0.12)
        + (form_coherence * 0.08)
        - (contact_overcoupling * 0.08)
        - (drift_risk * 0.06)
    )
    hypothesis_reality_binding = _clip(
        (reality_binding * 0.28)
        + (thought_confirmation * 0.20)
        + (structural_grounding * 0.18)
        + (visual_mcm_context_fit * 0.16)
        + (max(0.0, consequence_balance) * 0.08)
        + (own_binding * 0.06)
        - (open_pressure * 0.06)
        - (borrowed_pressure * 0.04)
    )
    visual_mcm_mismatch = _clip(
        abs(form_to_mcm_recall - mcm_to_form_confirmation)
        + abs(visual_mcm_context_fit - hypothesis_reality_binding) * 0.45
        + max(0.0, open_pressure - thought_confirmation) * 0.25
        + (borrowed_pressure * 0.10)
    )

    form_mcm_syntax_density = _clip(
        (form_to_mcm_recall * 0.28)
        + (mcm_to_form_confirmation * 0.24)
        + (visual_mcm_context_fit * 0.18)
        + (hypothesis_reality_binding * 0.18)
        + (max(0.0, consequence_balance) * 0.06)
        + (own_binding * 0.06)
    )
    form_mcm_syntax_pressures = {
        "form_field_mismatch_watch": _clip(
            (visual_mcm_mismatch * 0.34)
            + ((1.0 - hypothesis_reality_binding) * 0.18)
            + (open_pressure * 0.10)
        ),
        "bound_form_field_memory": _clip(
            (form_mcm_syntax_density * 0.30)
            + (hypothesis_reality_binding * 0.26)
            + (visual_mcm_context_fit * 0.12)
        ),
        "emerging_form_field_recall": _clip(
            (form_to_mcm_recall * 0.28)
            + (mcm_to_form_confirmation * 0.24)
            + (thought_confirmation * 0.08)
        ),
        "partial_form_field_contact": _clip(
            (max(form_to_mcm_recall, mcm_to_form_confirmation) * 0.28)
            + (visual_mcm_context_fit * 0.08)
        ),
        "unbound_form_field_syntax": _clip(
            ((1.0 - max(form_to_mcm_recall, mcm_to_form_confirmation, hypothesis_reality_binding)) * 0.24)
            + (visual_mcm_mismatch * 0.08)
        ),
    }
    form_mcm_syntax_state = max(form_mcm_syntax_pressures, key=form_mcm_syntax_pressures.get)

    syntax_density = _clip(
        (form_density * 0.26)
        + (thought_trace * 0.22)
        + (form_coherence * 0.16)
        + (thought_maturity * 0.16)
        + (reality_binding * 0.12)
        + (own_binding * 0.08)
    )
    syntax_compression = _clip(
        (form_compression * 0.34)
        + (form_coherence * 0.18)
        + (reality_binding * 0.16)
        + (thought_maturity * 0.14)
        + (own_binding * 0.10)
        - (open_pressure * 0.08)
        - (drift_risk * 0.06)
    )
    syntax_coherence = _clip(
        (syntax_density * 0.22)
        + (syntax_compression * 0.22)
        + (reality_binding * 0.22)
        + (thought_maturity * 0.18)
        + (own_binding * 0.12)
        - (borrowed_pressure * 0.10)
        - (drift_risk * 0.10)
    )

    syntax_origin_pressures = {
        "own_form_language": _clip((own_binding * 0.34) + (syntax_coherence * 0.24) + ((1.0 - borrowed_pressure) * 0.10)),
        "borrowed_translation_bridge": _clip((borrowed_pressure * 0.34) + ((1.0 - own_binding) * 0.14)),
        "mixed_form_translation": _clip((syntax_coherence * 0.24) + (borrowed_pressure * 0.18) + (own_binding * 0.10)),
        "emerging_form_language": _clip((syntax_density * 0.28) + (syntax_compression * 0.10)),
        "unlocated_syntax": _clip((1.0 - max(own_binding, borrowed_pressure, syntax_coherence, syntax_density)) * 0.24),
    }
    syntax_origin = max(syntax_origin_pressures, key=syntax_origin_pressures.get)

    syntax_state_pressures = {
        "condensed_sentence": _clip((syntax_coherence * 0.32) + (syntax_compression * 0.26) + (reality_binding * 0.08)),
        "formed_sentence": _clip((syntax_density * 0.28) + (syntax_coherence * 0.22) + (thought_maturity * 0.08)),
        "open_thought_sentence": _clip(
            (open_pressure * 0.26)
            + ((1.0 if reifung_word in ("replay_maturation", "reinterpretation_maturation", "distance_maturation") else 0.0) * 0.12)
            + (thought_trace * 0.08)
        ),
        "ungrounded_sentence_watch": _clip((drift_risk * 0.34) + ((1.0 - reality_binding) * 0.10)),
        "thin_syntax": _clip((1.0 - max(syntax_coherence, syntax_compression, syntax_density)) * 0.24),
    }
    syntax_state = max(syntax_state_pressures, key=syntax_state_pressures.get)

    syntax_parts = [
        f"fs:{form_word}",
        f"fc:{compound_word}",
        f"field:{field_word}",
        f"ts:{thought_word}",
        f"tf:{thought_family_word}",
        f"struct:{structure_word}",
        f"origin:{origin_word}",
        f"ripe:{reifung_word}",
        f"posture:{posture_word}",
        f"act:{action_word}",
        f"phase:{phase_word}",
        f"world:{world_experience_anchor}",
        f"thought:{thought_experience_anchor}",
        f"fm:{form_mcm_syntax_state}",
    ]
    syntax_sentence = "|".join(syntax_parts)
    dialogue_bridge_sentence = "|".join(
        [
            f"feel:{form_word}",
            f"world_memory:{world_experience_anchor}",
            f"thought_memory:{thought_experience_anchor}",
            f"hypothesis:{structure_word}",
            f"variant:{reifung_word}",
            f"bearing:{posture_word}",
            f"action:{action_word}",
            f"form_mcm:{form_mcm_syntax_state}",
        ]
    )
    form_mcm_basis = "|".join(
        [
            form_word,
            compound_word,
            field_word,
            structure_word,
            origin_word,
            reifung_word,
            f"{round(form_to_mcm_recall, 2):.2f}",
            f"{round(mcm_to_form_confirmation, 2):.2f}",
            f"{round(visual_mcm_context_fit, 2):.2f}",
            f"{round(hypothesis_reality_binding, 2):.2f}",
            form_mcm_syntax_state,
        ]
    )
    form_mcm_token = "fm_" + hashlib.sha1(form_mcm_basis.encode("utf-8", errors="ignore")).hexdigest()[:10]
    form_mcm_family_basis = "|".join(
        [
            form_layer_word,
            form_family_word,
            field_word,
            structure_word,
            origin_word,
            reifung_word,
            form_mcm_syntax_state,
            _bucket(form_to_mcm_recall, 0.10),
            _bucket(mcm_to_form_confirmation, 0.10),
            _bucket(visual_mcm_context_fit, 0.10),
            _bucket(hypothesis_reality_binding, 0.10),
            _bucket(visual_mcm_mismatch, 0.10),
        ]
    )
    form_mcm_family_token = "fmf_" + hashlib.sha1(form_mcm_family_basis.encode("utf-8", errors="ignore")).hexdigest()[:10]
    form_mcm_sentence = "|".join(
        [
            f"token:{form_mcm_token}",
            f"family:{form_mcm_family_token}",
            f"form:{form_word}",
            f"field:{field_word}",
            f"recall:{form_to_mcm_recall:.2f}",
            f"confirm:{mcm_to_form_confirmation:.2f}",
            f"fit:{visual_mcm_context_fit:.2f}",
            f"bind:{hypothesis_reality_binding:.2f}",
            f"mismatch:{visual_mcm_mismatch:.2f}",
            f"state:{form_mcm_syntax_state}",
        ]
    )
    signature_basis = "|".join([form_word, compound_word, field_word, structure_word, origin_word, reifung_word, posture_word, action_word, phase_word])
    syntax_signature = "ds_" + hashlib.sha1(signature_basis.encode("utf-8", errors="ignore")).hexdigest()[:10]

    return {
        "dio_syntax_signature": str(syntax_signature),
        "dio_form_mcm_token": str(form_mcm_token),
        "dio_form_mcm_family_token": str(form_mcm_family_token),
        "dio_form_mcm_sentence": str(form_mcm_sentence),
        "dio_form_mcm_syntax_state": str(form_mcm_syntax_state),
        "dio_form_mcm_syntax_pressures": dict(form_mcm_syntax_pressures),
        "form_to_mcm_recall": float(form_to_mcm_recall),
        "mcm_to_form_confirmation": float(mcm_to_form_confirmation),
        "visual_mcm_context_fit": float(visual_mcm_context_fit),
        "visual_mcm_mismatch": float(visual_mcm_mismatch),
        "hypothesis_reality_binding": float(hypothesis_reality_binding),
        "form_mcm_syntax_density": float(form_mcm_syntax_density),
        "dio_language_sentence": str(syntax_sentence),
        "dio_dialogue_bridge_sentence": str(dialogue_bridge_sentence),
        "dio_language_state": str(syntax_state),
        "dio_syntax_origin": str(syntax_origin),
        "dio_syntax_state_pressures": dict(syntax_state_pressures),
        "dio_syntax_origin_pressures": dict(syntax_origin_pressures),
        "dio_syntax_density": float(syntax_density),
        "dio_syntax_compression": float(syntax_compression),
        "dio_syntax_coherence": float(syntax_coherence),
        "dio_form_word": str(form_word),
        "dio_compound_word": str(compound_word),
        "dio_field_word": str(field_word),
        "dio_thought_word": str(thought_word),
        "dio_thought_family_word": str(thought_family_word),
        "dio_thought_family_key": str(thought_family_key),
        "dio_structure_word": str(structure_word),
        "dio_origin_word": str(origin_word),
        "dio_reifung_word": str(reifung_word),
        "dio_posture_word": str(posture_word),
        "dio_action_word": str(action_word),
        "dio_phase_word": str(phase_word),
        "dio_world_experience_anchor": str(world_experience_anchor),
        "dio_thought_experience_anchor": str(thought_experience_anchor),
        "dio_context_word": str(context_word),
    }


__all__ = [
    "_build_dio_form_language_state",
    "_quantize_form_axis",
    "_extract_outcome_form_symbol_state",
    "_build_form_symbol_base_quality_state",
    "_build_form_symbol_identity_state",
    "_build_form_symbol_object_state",
    "_build_form_symbol_compound_item",
    "_update_form_symbol_item_memory_stats",
    "_build_form_symbol_variant_family_state",
    "_build_form_symbol_semantic_state",
    "_learn_form_symbol_development_item",
]


def _quantize_form_axis(value, step=0.20, min_value=-2.0, max_value=2.0):

    try:
        raw = float(value or 0.0)
    except Exception:
        raw = 0.0

    step_value = max(0.01, float(step or 0.20))
    bounded = max(float(min_value), min(float(max_value), raw))
    return round(round(bounded / step_value) * step_value, 4)


def _extract_outcome_form_symbol_state(bot, position=None):

    position_state = dict(position or {}) if isinstance(position, dict) else {}
    meta = dict(position_state.get("meta", {}) or {}) if isinstance(position_state.get("meta", {}), dict) else {}

    for candidate in (
        meta.get("form_symbol_state", {}),
        (meta.get("runtime_result", {}) or {}).get("form_symbol_state", {}) if isinstance(meta.get("runtime_result", {}), dict) else {},
        (meta.get("brain_snapshot", {}) or {}).get("form_symbol_state", {}) if isinstance(meta.get("brain_snapshot", {}), dict) else {},
        getattr(bot, "form_symbol_state", {}) if bot is not None else {},
    ):
        if not isinstance(candidate, dict):
            continue
        symbol_id = str(candidate.get("form_symbol_id", "") or "").strip()
        if symbol_id and symbol_id != "-":
            return dict(candidate or {})

    return {}


def _build_form_symbol_base_quality_state(context=None):

    ctx = dict(context or {})

    def _b01(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(0.0, min(1.0, float(value)))

    directional_bias = float(ctx.get("directional_bias", 0.0) or 0.0)
    breakout_tension = _b01(ctx.get("breakout_tension", 0.0))
    range_position = float(ctx.get("range_position", 0.0) or 0.0)
    body_pressure = _b01(ctx.get("body_pressure", 0.0))
    wick_pressure = _b01(ctx.get("wick_pressure", 0.0))
    field_pressure = _b01(ctx.get("field_pressure", 0.0))
    field_fragmentation = _b01(ctx.get("field_fragmentation", 0.0))
    market_balance = _b01(ctx.get("market_balance", 0.0))
    visual_coherence = _b01(ctx.get("visual_coherence", 0.0))
    structure_quality = _b01(ctx.get("structure_quality", 0.0))
    context_confidence = _b01(ctx.get("context_confidence", 0.0))
    stress_relief_potential = _b01(ctx.get("stress_relief_potential", 0.0))
    field_clarity = _b01(ctx.get("field_clarity", 0.0))
    stability = _b01(ctx.get("stability", 0.0))
    maturity = _b01(ctx.get("maturity", 0.0))
    distance = _b01(ctx.get("distance", 0.0))
    novelty = _b01(ctx.get("novelty", 0.0))
    form_resolution_quality = _b01(ctx.get("form_resolution_quality", 0.0))
    form_detail_pressure = _b01(ctx.get("form_detail_pressure", 0.0))

    relevance = _b01(
        (abs(directional_bias) * 0.16)
        + (breakout_tension * 0.16)
        + (abs(range_position) * 0.10)
        + (body_pressure * 0.12)
        + (wick_pressure * 0.12)
        + (field_pressure * 0.12)
        + (field_fragmentation * 0.10)
        + (max(0.0, 1.0 - market_balance) * 0.06)
        + (max(0.0, 1.0 - visual_coherence) * 0.06)
    )
    bearing = _b01(
        (structure_quality * 0.24)
        + (context_confidence * 0.18)
        + (visual_coherence * 0.16)
        + (market_balance * 0.12)
        + (stress_relief_potential * 0.10)
        + (field_clarity * 0.10)
        + (stability * 0.10)
    )
    fragility = _b01(
        (wick_pressure * 0.22)
        + (field_fragmentation * 0.20)
        + (field_pressure * 0.16)
        + (max(0.0, 1.0 - context_confidence) * 0.14)
        + (max(0.0, 1.0 - visual_coherence) * 0.12)
        + (max(0.0, 1.0 - stability) * 0.16)
    )
    resonance = _b01(maturity * stability * (1.0 - min(1.0, distance)))
    zoom_need = _b01(
        (relevance * 0.30)
        + (novelty * 0.22)
        + (fragility * 0.20)
        + (max(0.0, 0.42 - bearing) * 0.18)
        + (max(0.0, distance) * 0.10)
        + ((1.0 - form_resolution_quality) * form_detail_pressure * 0.08)
    )
    load_reduction = _b01(resonance * (1.0 - zoom_need) * (0.60 + stability * 0.40))

    return {
        "relevance": float(relevance),
        "bearing": float(bearing),
        "fragility": float(fragility),
        "resonance": float(resonance),
        "zoom_need": float(zoom_need),
        "load_reduction": float(load_reduction),
    }


def _build_form_symbol_identity_state(context=None):

    ctx = dict(context or {})

    def _value(name, default=0.0):
        try:
            value = float(ctx.get(name, default) or default)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return float(value)

    spatial_bias = _value("spatial_bias")
    directional_bias = _value("directional_bias")
    range_position = _value("range_position")
    short_impulse = _value("short_impulse")
    mid_impulse = _value("mid_impulse")
    compression = _value("compression")
    expansion = _value("expansion")
    body_pressure = _value("body_pressure")
    wick_pressure = _value("wick_pressure")
    market_balance = _value("market_balance")
    breakout_tension = _value("breakout_tension")
    visual_coherence = _value("visual_coherence")
    structure_quality = _value("structure_quality")
    zone_proximity = _value("zone_proximity")
    context_confidence = _value("context_confidence")
    stress_relief_potential = _value("stress_relief_potential")
    field_clarity = _value("field_clarity")
    field_pressure = _value("field_pressure")
    field_fragmentation = _value("field_fragmentation")

    form_vector = [
        _quantize_form_axis(spatial_bias),
        _quantize_form_axis(directional_bias),
        _quantize_form_axis(range_position),
        _quantize_form_axis(short_impulse),
        _quantize_form_axis(mid_impulse),
        _quantize_form_axis(compression),
        _quantize_form_axis(expansion),
        _quantize_form_axis(body_pressure),
        _quantize_form_axis(wick_pressure),
        _quantize_form_axis(market_balance),
        _quantize_form_axis(breakout_tension),
        _quantize_form_axis(visual_coherence),
        _quantize_form_axis(structure_quality),
        _quantize_form_axis(zone_proximity),
        _quantize_form_axis(context_confidence),
        _quantize_form_axis(stress_relief_potential),
        _quantize_form_axis(field_clarity),
        _quantize_form_axis(field_pressure),
        _quantize_form_axis(field_fragmentation),
    ]
    form_key = "|".join(f"{float(item):.2f}" for item in form_vector)

    form_resolution_quality = max(
        0.0,
        min(
            1.0,
            (visual_coherence * 0.20)
            + (structure_quality * 0.24)
            + (context_confidence * 0.22)
            + (field_clarity * 0.16)
            + (market_balance * 0.10)
            + (stress_relief_potential * 0.08)
            - (field_fragmentation * 0.18)
            - (field_pressure * 0.06),
        ),
    )
    form_detail_pressure = max(
        0.0,
        min(
            1.0,
            (abs(directional_bias) * 0.18)
            + (abs(range_position) * 0.12)
            + (abs(short_impulse - mid_impulse) * 0.12)
            + (breakout_tension * 0.18)
            + (((body_pressure + wick_pressure) * 0.50) * 0.16)
            + (field_pressure * 0.14)
            + (field_fragmentation * 0.10),
        ),
    )

    form_symbol_scope_pressures = {
        "wide_trace": max(0.0, min(1.0, ((1.0 - form_resolution_quality) * 0.30) + (field_fragmentation * 0.10))),
        "wide_form": max(0.0, min(1.0, (form_resolution_quality * 0.18) + ((1.0 - abs(form_resolution_quality - 0.48)) * 0.18) + (form_detail_pressure * 0.06))),
        "structured_form": max(0.0, min(1.0, (form_resolution_quality * 0.34) + (visual_coherence * 0.10) + (structure_quality * 0.08))),
    }
    form_symbol_scope = max(form_symbol_scope_pressures, key=form_symbol_scope_pressures.get)
    form_symbol_abstraction_level = {"wide_trace": 0, "wide_form": 1, "structured_form": 2}.get(form_symbol_scope, 1)
    if form_symbol_scope == "wide_trace":
        family_vector = [
            _quantize_form_axis((directional_bias + spatial_bias) * 0.50, step=0.75),
            _quantize_form_axis((short_impulse + mid_impulse) * 0.50, step=0.75),
            _quantize_form_axis((structure_quality + context_confidence) * 0.50, step=0.50, min_value=0.0, max_value=1.0),
            _quantize_form_axis((field_pressure + breakout_tension) * 0.50, step=0.50, min_value=0.0, max_value=1.0),
        ]
    elif form_symbol_scope == "wide_form":
        family_vector = [
            _quantize_form_axis(directional_bias, step=0.55),
            _quantize_form_axis(range_position, step=0.55),
            _quantize_form_axis((short_impulse + mid_impulse) * 0.50, step=0.55),
            _quantize_form_axis(compression - expansion, step=0.55),
            _quantize_form_axis((body_pressure + wick_pressure) * 0.50, step=0.50),
            _quantize_form_axis((structure_quality + context_confidence + zone_proximity) / 3.0, step=0.50, min_value=0.0, max_value=1.0),
            _quantize_form_axis(field_clarity - ((field_pressure + field_fragmentation) * 0.50), step=0.50, min_value=-1.0, max_value=1.0),
        ]
    else:
        family_vector = [
            _quantize_form_axis(directional_bias, step=0.40),
            _quantize_form_axis(range_position, step=0.40),
            _quantize_form_axis((short_impulse + mid_impulse) * 0.50, step=0.40),
            _quantize_form_axis(compression - expansion, step=0.40),
            _quantize_form_axis((body_pressure + wick_pressure) * 0.50, step=0.40),
            _quantize_form_axis((structure_quality + context_confidence + zone_proximity) / 3.0, step=0.35, min_value=0.0, max_value=1.0),
            _quantize_form_axis((market_balance + visual_coherence - breakout_tension) / 2.0, step=0.35, min_value=-1.0, max_value=1.0),
            _quantize_form_axis(field_clarity - ((field_pressure + field_fragmentation) * 0.50), step=0.35, min_value=-1.0, max_value=1.0),
        ]

    family_key = str(form_symbol_abstraction_level) + "|" + "|".join(f"{float(item):.2f}" for item in family_vector)
    digest = hashlib.sha1(str(family_key).encode("utf-8")).hexdigest()[:10]
    symbol_id = f"fs_{digest}"

    return {
        "form_vector": [float(item) for item in form_vector],
        "form_key": str(form_key),
        "form_resolution_quality": float(form_resolution_quality),
        "form_detail_pressure": float(form_detail_pressure),
        "form_symbol_scope": str(form_symbol_scope),
        "form_symbol_scope_pressures": dict(form_symbol_scope_pressures),
        "form_symbol_abstraction_level": int(form_symbol_abstraction_level),
        "family_vector": [float(item) for item in family_vector],
        "family_key": str(family_key),
        "symbol_id": str(symbol_id),
    }


def _build_form_symbol_object_state(context=None):

    ctx = dict(context or {})

    def _b01(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(0.0, min(1.0, float(value)))

    maturity = _b01(ctx.get("maturity", 0.0))
    stability = _b01(ctx.get("stability", 0.0))
    resonance = _b01(ctx.get("resonance", 0.0))
    bearing = _b01(ctx.get("bearing", 0.0))
    fragility = _b01(ctx.get("fragility", 0.0))
    form_resolution_quality = _b01(ctx.get("form_resolution_quality", 0.0))
    load_reduction = _b01(ctx.get("load_reduction", 0.0))
    zoom_need = _b01(ctx.get("zoom_need", 0.0))
    form_detail_pressure = _b01(ctx.get("form_detail_pressure", 0.0))
    variance = _b01(ctx.get("variance", 0.0))
    novelty = _b01(ctx.get("novelty", 0.0))
    visual_blindness = _b01(ctx.get("visual_blindness", 0.0))
    visual_clarity = _b01(ctx.get("visual_clarity", 0.0))
    visual_object_stability = _b01(ctx.get("visual_object_stability", 0.0))
    visual_shape_fragility = _b01(ctx.get("visual_shape_fragility", 0.0))
    visual_form_pressure = _b01(ctx.get("visual_form_pressure", 0.0))
    visual_form_novelty = _b01(ctx.get("visual_form_novelty", 0.0))
    visual_shape_resonance = _b01(ctx.get("visual_shape_resonance", 0.0))

    symbolic_object_distance = _b01(
        maturity
        * stability
        * (0.45 + resonance * 0.55)
        * (0.45 + bearing * 0.55)
        * (1.0 - min(0.90, fragility * 0.72))
        * (0.65 + form_resolution_quality * 0.35)
    )
    symbolic_containment = _b01(
        (symbolic_object_distance * 0.58)
        + (load_reduction * 0.24)
        + (max(0.0, 1.0 - zoom_need) * 0.10)
        + (max(0.0, 1.0 - form_detail_pressure) * 0.08)
    )
    symbolic_field_decoupling = _b01(
        symbolic_containment
        * (0.40 + maturity * 0.28 + resonance * 0.20 + stability * 0.12)
        * (1.0 - min(0.78, fragility * 0.42))
    )
    split_pressure = _b01((variance * 0.52) + (novelty * 0.24) + (fragility * 0.18) - (stability * 0.10))
    merge_pressure = _b01((stability * 0.36) + (maturity * 0.30) + (resonance * 0.24) - (novelty * 0.18))
    uncertain_form_exposure = _b01(
        (visual_blindness * 0.26)
        + (max(0.0, 0.42 - visual_clarity) * 0.18)
        + (max(0.0, 0.44 - visual_object_stability) * 0.16)
        + (visual_shape_fragility * 0.12)
        + (visual_form_pressure * 0.10)
        + (fragility * 0.10)
        + (max(0.0, 0.46 - bearing) * 0.14)
        + (visual_form_novelty * 0.06)
        - (visual_shape_resonance * 0.10)
        - (resonance * 0.06)
    )

    return {
        "symbolic_object_distance": float(symbolic_object_distance),
        "symbolic_containment": float(symbolic_containment),
        "symbolic_field_decoupling": float(symbolic_field_decoupling),
        "split_pressure": float(split_pressure),
        "merge_pressure": float(merge_pressure),
        "uncertain_form_exposure": float(uncertain_form_exposure),
    }


def _build_form_symbol_compound_item(
    previous_symbol_id,
    symbol_id,
    previous_state=None,
    current_metrics=None,
    compound_item=None,
    timestamp=None,
):

    previous_symbol_id = str(previous_symbol_id or "").strip()
    symbol_id = str(symbol_id or "").strip()
    previous = dict(previous_state or {})
    current = dict(current_metrics or {})
    item = dict(compound_item or {})

    default_state = {
        "compound_id": "-",
        "compound_key": "-",
        "compound_scope": "single",
        "compound_seen": 0,
        "compound_maturity": 0.0,
        "compound_stability": 0.0,
        "compound_resonance": 0.0,
        "compound_bearing": 0.0,
        "compound_load_reduction": 0.0,
        "compound_novelty": 1.0,
        "compound_development_quality": 0.0,
        "compound_action_affinity": 0.50,
        "compound_observation_affinity": 0.0,
        "compound_reframe_potential": 0.0,
        "compound_learning_trust": 0.0,
        "compound_action_trust": 0.0,
        "compound_caution_trust": 0.0,
        "compound_contact_maturity": 0.0,
        "compound_contact_utility": 0.0,
        "compound_contact_pain_memory": 0.0,
        "compound_contact_carefulness": 0.0,
        "compound_contact_burden_evidence": 0.0,
        "compound_contact_utility_evidence": 0.0,
        "compound_contact_state": "unformed_contact",
        "compound_item": {},
        "has_compound": False,
    }

    if not previous_symbol_id or previous_symbol_id == "-" or previous_symbol_id == symbol_id:
        return dict(default_state)

    def _b01(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(0.0, min(1.0, float(value)))

    def _bs(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(-1.0, min(1.0, float(value)))

    compound_key = f"{previous_symbol_id}>{symbol_id}"
    compound_digest = hashlib.sha1(str(compound_key).encode("utf-8")).hexdigest()[:10]
    compound_id = f"fc_{compound_digest}"
    compound_seen = int(item.get("seen", 0) or 0) + 1
    compound_maturity = _b01(compound_seen / float(compound_seen + 13))

    bearing = _b01(current.get("bearing", 0.0))
    stability = _b01(current.get("stability", 0.0))
    resonance = _b01(current.get("resonance", 0.0))
    form_resolution_quality = _b01(current.get("form_resolution_quality", 0.0))

    previous_stability = _b01(previous.get("form_symbol_stability", 0.0))
    previous_resonance = _b01(previous.get("form_symbol_resonance", 0.0))
    previous_bearing = _b01(previous.get("form_symbol_bearing", 0.0))
    previous_resolution = _b01(previous.get("form_symbol_resolution_quality", 0.0))
    pair_balance = 1.0 - min(1.0, abs(previous_bearing - bearing))
    prior_compound_stability = _b01(item.get("stability", 0.0))

    compound_stability = _b01(
        (prior_compound_stability * 0.70)
        + (((previous_stability + stability) * 0.50) * 0.20)
        + (pair_balance * 0.10)
    )
    compound_resonance = _b01(
        compound_maturity
        * compound_stability
        * (0.45 + ((previous_resonance + resonance) * 0.50) * 0.55)
    )
    compound_bearing = _b01(
        ((previous_bearing + bearing) * 0.50 * 0.54)
        + (compound_stability * 0.24)
        + (compound_resonance * 0.14)
        + (min(form_resolution_quality, previous_resolution) * 0.08)
    )
    compound_novelty = _b01(1.0 - compound_maturity + (1.0 - pair_balance) * 0.20)
    compound_load_reduction = _b01(
        compound_resonance
        * (0.54 + compound_stability * 0.30 + compound_bearing * 0.16)
        * (1.0 - min(0.80, compound_novelty * 0.35))
    )

    compound_development_quality = _bs(item.get("development_quality", 0.0))
    compound_action_affinity = _b01(item.get("action_affinity", 0.50), default=0.50)
    compound_observation_affinity = _b01(item.get("observation_affinity", 0.0))
    compound_reframe_potential = _b01(item.get("context_reframe_potential", 0.0))
    compound_learning_trust = _b01(item.get("learning_trust", 0.0))
    compound_action_trust = _b01(item.get("action_trust", 0.0))
    compound_caution_trust = _b01(item.get("caution_trust", 0.0))
    compound_contact_maturity = _b01(item.get("contact_maturity", 0.0))
    compound_contact_utility = _b01(item.get("contact_utility", 0.0))
    compound_contact_pain_memory = _b01(item.get("contact_pain_memory", 0.0))
    compound_contact_carefulness = _b01(item.get("contact_carefulness", 0.0))
    compound_contact_burden_evidence = _b01(item.get("contact_burden_evidence", 0.0))
    compound_contact_utility_evidence = _b01(item.get("contact_utility_evidence", 0.0))
    compound_contact_state = str(item.get("contact_learning_state", "unformed_contact") or "unformed_contact")

    item.update({
        "compound_id": str(compound_id),
        "compound_key": str(compound_key),
        "left_symbol_id": str(previous_symbol_id),
        "right_symbol_id": str(symbol_id),
        "scope": "compound_form",
        "seen": int(compound_seen),
        "maturity": float(compound_maturity),
        "stability": float(compound_stability),
        "resonance": float(compound_resonance),
        "bearing": float(compound_bearing),
        "load_reduction": float(compound_load_reduction),
        "novelty": float(compound_novelty),
        "development_quality": float(compound_development_quality),
        "action_affinity": float(compound_action_affinity),
        "observation_affinity": float(compound_observation_affinity),
        "context_reframe_potential": float(compound_reframe_potential),
        "learning_trust": float(compound_learning_trust),
        "action_trust": float(compound_action_trust),
        "caution_trust": float(compound_caution_trust),
        "contact_maturity": float(compound_contact_maturity),
        "contact_utility": float(compound_contact_utility),
        "contact_pain_memory": float(compound_contact_pain_memory),
        "contact_carefulness": float(compound_contact_carefulness),
        "contact_burden_evidence": float(compound_contact_burden_evidence),
        "contact_utility_evidence": float(compound_contact_utility_evidence),
        "contact_learning_state": str(compound_contact_state),
        "first_seen_ts": item.get("first_seen_ts", timestamp),
        "last_seen_ts": timestamp,
    })

    return {
        "compound_id": str(compound_id),
        "compound_key": str(compound_key),
        "compound_scope": "compound_form",
        "compound_seen": int(compound_seen),
        "compound_maturity": float(compound_maturity),
        "compound_stability": float(compound_stability),
        "compound_resonance": float(compound_resonance),
        "compound_bearing": float(compound_bearing),
        "compound_load_reduction": float(compound_load_reduction),
        "compound_novelty": float(compound_novelty),
        "compound_development_quality": float(compound_development_quality),
        "compound_action_affinity": float(compound_action_affinity),
        "compound_observation_affinity": float(compound_observation_affinity),
        "compound_reframe_potential": float(compound_reframe_potential),
        "compound_learning_trust": float(compound_learning_trust),
        "compound_action_trust": float(compound_action_trust),
        "compound_caution_trust": float(compound_caution_trust),
        "compound_contact_maturity": float(compound_contact_maturity),
        "compound_contact_utility": float(compound_contact_utility),
        "compound_contact_pain_memory": float(compound_contact_pain_memory),
        "compound_contact_carefulness": float(compound_contact_carefulness),
        "compound_contact_burden_evidence": float(compound_contact_burden_evidence),
        "compound_contact_utility_evidence": float(compound_contact_utility_evidence),
        "compound_contact_state": str(compound_contact_state),
        "compound_item": dict(item),
        "has_compound": True,
    }


def _update_form_symbol_item_memory_stats(item, form_vector):

    item = dict(item or {})
    vector = [float(value) for value in list(form_vector or [])]
    seen_before = int(item.get("seen", 0) or 0)
    avg_vector = list(item.get("avg_vector", vector) or vector)
    if len(avg_vector) != len(vector):
        avg_vector = list(vector)
    avg_vector = [float(value) for value in avg_vector]

    if vector:
        squared_distance = sum((float(current) - float(prior)) ** 2 for current, prior in zip(vector, avg_vector))
        distance = float((squared_distance ** 0.5) / max(1.0, len(vector) ** 0.5))
    else:
        distance = 0.0

    seen = int(seen_before + 1)
    alpha = min(0.35, 1.0 / max(1, seen))
    new_avg = [
        (float(prior) * (1.0 - alpha)) + (float(current) * alpha)
        for current, prior in zip(vector, avg_vector)
    ]
    prior_variance = float(item.get("variance", 0.0) or 0.0)
    variance = max(0.0, min(1.0, (prior_variance * 0.92) + (distance * 0.08)))

    maturity = max(0.0, min(1.0, seen / float(seen + 8)))
    stability = max(0.0, min(1.0, 1.0 - (variance * 2.4)))
    novelty = max(0.0, min(1.0, 1.0 - maturity + min(1.0, distance)))
    resonance = max(0.0, min(1.0, maturity * stability * (1.0 - min(1.0, distance))))

    def _b01(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(0.0, min(1.0, float(value)))

    def _bs(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(-1.0, min(1.0, float(value)))

    return {
        "seen_before": int(seen_before),
        "seen": int(seen),
        "avg_vector": [float(value) for value in new_avg],
        "distance": float(distance),
        "variance": float(variance),
        "maturity": float(maturity),
        "stability": float(stability),
        "novelty": float(novelty),
        "resonance": float(resonance),
        "learned_development_quality": float(_bs(item.get("development_quality", 0.0))),
        "learned_action_affinity": float(_b01(item.get("action_affinity", 0.50), default=0.50)),
        "learned_observation_affinity": float(_b01(item.get("observation_affinity", 0.0))),
        "learned_reframe_potential": float(_b01(item.get("context_reframe_potential", 0.0))),
        "learned_learning_trust": float(_b01(item.get("learning_trust", 0.0))),
        "learned_action_trust": float(_b01(item.get("action_trust", 0.0))),
        "learned_caution_trust": float(_b01(item.get("caution_trust", 0.0))),
        "learned_contact_maturity": float(_b01(item.get("contact_maturity", 0.0))),
        "learned_contact_utility": float(_b01(item.get("contact_utility", 0.0))),
        "learned_contact_pain_memory": float(_b01(item.get("contact_pain_memory", 0.0))),
        "learned_contact_carefulness": float(_b01(item.get("contact_carefulness", 0.0))),
        "learned_contact_burden_evidence": float(_b01(item.get("contact_burden_evidence", 0.0))),
        "learned_contact_utility_evidence": float(_b01(item.get("contact_utility_evidence", 0.0))),
        "learned_contact_state": str(item.get("contact_learning_state", "unformed_contact") or "unformed_contact"),
    }


def _build_form_symbol_variant_family_state(variants=None, context=None):

    variant_map = dict(variants or {})
    ctx = dict(context or {})

    def _b01(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(0.0, min(1.0, float(value)))

    variant_count = int(len(variant_map))
    variant_seen_total = sum(
        int((variant or {}).get("seen", 0) or 0)
        for variant in variant_map.values()
        if isinstance(variant, dict)
    )
    variant_exposure_mean = 0.0
    variant_bearing_mean = 0.0
    if variant_count > 0:
        variant_exposure_mean = sum(
            float((variant or {}).get("uncertain_exposure", 0.0) or 0.0)
            for variant in variant_map.values()
            if isinstance(variant, dict)
        ) / float(max(1, variant_count))
        variant_bearing_mean = sum(
            float((variant or {}).get("bearing", 0.0) or 0.0)
            for variant in variant_map.values()
            if isinstance(variant, dict)
        ) / float(max(1, variant_count))

    distance = _b01(ctx.get("distance", 0.0))
    stability = _b01(ctx.get("stability", 0.0))
    resonance = _b01(ctx.get("resonance", 0.0))
    variance = _b01(ctx.get("variance", 0.0))
    max_variants = max(1, int(ctx.get("max_variants", 12) or 12))
    novelty = _b01(ctx.get("novelty", 0.0))
    visual_form_novelty = _b01(ctx.get("visual_form_novelty", 0.0))
    maturity = _b01(ctx.get("maturity", 0.0))
    learned_learning_trust = _b01(ctx.get("learned_learning_trust", 0.0))
    bearing = _b01(ctx.get("bearing", 0.0))
    learned_development_quality = max(-1.0, min(1.0, float(ctx.get("learned_development_quality", 0.0) or 0.0)))
    learned_action_trust = _b01(ctx.get("learned_action_trust", 0.0))
    visual_shape_resonance = _b01(ctx.get("visual_shape_resonance", 0.0))
    uncertain_form_exposure = _b01(ctx.get("uncertain_form_exposure", 0.0))
    learned_observation_affinity = _b01(ctx.get("learned_observation_affinity", 0.0))
    learned_reframe_potential = _b01(ctx.get("learned_reframe_potential", 0.0))

    variant_similarity = _b01((1.0 - min(1.0, distance)) * 0.58 + stability * 0.28 + resonance * 0.14)
    variant_spread = _b01(
        (variance * 0.52)
        + (min(1.0, float(variant_count) / float(max(1, max_variants))) * 0.26)
        + (novelty * 0.12)
        + (visual_form_novelty * 0.10)
    )
    uncertainty_familiarity = _b01(
        (maturity * 0.34)
        + (min(1.0, float(variant_seen_total) / 24.0) * 0.24)
        + (variant_similarity * 0.18)
        + (learned_learning_trust * 0.14)
        + (variant_exposure_mean * 0.10)
    )
    variant_bearing_memory = _b01(
        (variant_bearing_mean * 0.32)
        + (bearing * 0.22)
        + (max(0.0, learned_development_quality) * 0.16)
        + (learned_action_trust * 0.14)
        + (resonance * 0.10)
        + (visual_shape_resonance * 0.06)
    )
    variant_learning_pressure = _b01(
        (uncertain_form_exposure * 0.32)
        + (variant_spread * 0.20)
        + (max(0.0, 0.52 - uncertainty_familiarity) * 0.20)
        + (max(0.0, 0.48 - variant_bearing_memory) * 0.16)
        + (learned_observation_affinity * 0.08)
        + (learned_reframe_potential * 0.04)
    )

    uncertain_form_family_pressures = {
        "unfamiliar_uncertain_family": _b01(
            (uncertain_form_exposure * 0.32)
            + ((1.0 - uncertainty_familiarity) * 0.18)
            + (variant_spread * 0.08)
        ),
        "recurring_uncertain_variants": _b01(
            (uncertain_form_exposure * 0.26)
            + (variant_spread * 0.28)
            + (variant_similarity * 0.08)
        ),
        "familiar_uncertainty_watch": _b01(
            (uncertain_form_exposure * 0.24)
            + (uncertainty_familiarity * 0.22)
            + ((1.0 - variant_bearing_memory) * 0.12)
        ),
        "bearing_uncertainty_family": _b01(
            (uncertain_form_exposure * 0.22)
            + (variant_bearing_memory * 0.26)
            + (learned_action_trust * 0.08)
        ),
        "quiet_form_family": _b01(
            ((1.0 - uncertain_form_exposure) * 0.28)
            + (uncertainty_familiarity * 0.10)
            + ((1.0 - variant_spread) * 0.08)
        ),
    }
    uncertain_form_family_state = max(uncertain_form_family_pressures, key=uncertain_form_family_pressures.get)

    return {
        "variant_count": int(variant_count),
        "variant_seen_total": int(variant_seen_total),
        "variant_exposure_mean": float(variant_exposure_mean),
        "variant_bearing_mean": float(variant_bearing_mean),
        "variant_similarity": float(variant_similarity),
        "variant_spread": float(variant_spread),
        "uncertainty_familiarity": float(uncertainty_familiarity),
        "variant_bearing_memory": float(variant_bearing_memory),
        "variant_learning_pressure": float(variant_learning_pressure),
        "uncertain_form_family_state": str(uncertain_form_family_state),
        "uncertain_form_family_pressures": dict(uncertain_form_family_pressures),
    }


def _build_form_symbol_semantic_state(context=None):

    ctx = dict(context or {})

    def _b01(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(0.0, min(1.0, float(value)))

    form_resolution_quality = _b01(ctx.get("form_resolution_quality", 0.0))
    maturity = _b01(ctx.get("maturity", 0.0))
    stability = _b01(ctx.get("stability", 0.0))
    resonance = _b01(ctx.get("resonance", 0.0))
    bearing = _b01(ctx.get("bearing", 0.0))
    symbolic_containment = _b01(ctx.get("symbolic_containment", 0.0))
    uncertainty_familiarity = _b01(ctx.get("uncertainty_familiarity", 0.0))
    variant_similarity = _b01(ctx.get("variant_similarity", 0.0))
    fragility = _b01(ctx.get("fragility", 0.0))
    variant_spread = _b01(ctx.get("variant_spread", 0.0))
    load_reduction = _b01(ctx.get("load_reduction", 0.0))
    symbolic_object_distance = _b01(ctx.get("symbolic_object_distance", 0.0))
    symbolic_field_decoupling = _b01(ctx.get("symbolic_field_decoupling", 0.0))
    compound_load_reduction = _b01(ctx.get("compound_load_reduction", 0.0))
    merge_pressure = _b01(ctx.get("merge_pressure", 0.0))
    zoom_need = _b01(ctx.get("zoom_need", 0.0))
    split_pressure = _b01(ctx.get("split_pressure", 0.0))
    context_confidence = _b01(ctx.get("context_confidence", 0.0))
    visual_coherence = _b01(ctx.get("visual_coherence", 0.0))
    field_clarity = _b01(ctx.get("field_clarity", 0.0))
    field_fragmentation = _b01(ctx.get("field_fragmentation", 0.0))
    variant_learning_pressure = _b01(ctx.get("variant_learning_pressure", 0.0))
    novelty = _b01(ctx.get("novelty", 0.0))
    uncertain_form_exposure = _b01(ctx.get("uncertain_form_exposure", 0.0))
    learned_action_binding = _b01(ctx.get("learned_action_binding", 0.0))
    variant_bearing_memory = _b01(ctx.get("variant_bearing_memory", 0.0))
    compound_bearing = _b01(ctx.get("compound_bearing", 0.0))
    learned_action_trust = _b01(ctx.get("learned_action_trust", 0.0))
    learned_caution_trust = _b01(ctx.get("learned_caution_trust", 0.0))
    learned_observation_binding = _b01(ctx.get("learned_observation_binding", 0.0))
    learned_reframe_binding = _b01(ctx.get("learned_reframe_binding", 0.0))
    compound_maturity = _b01(ctx.get("compound_maturity", 0.0))
    compound_resonance = _b01(ctx.get("compound_resonance", 0.0))
    form_symbol_scope = str(ctx.get("form_symbol_scope", "wide_trace") or "wide_trace")
    uncertain_form_family_state = str(ctx.get("uncertain_form_family_state", "quiet_form_family") or "quiet_form_family")
    compound_scope = str(ctx.get("compound_scope", "single") or "single")

    semantic_density = _b01(
        (form_resolution_quality * 0.22)
        + (maturity * 0.16)
        + (stability * 0.14)
        + (resonance * 0.12)
        + (bearing * 0.14)
        + (symbolic_containment * 0.10)
        + (uncertainty_familiarity * 0.06)
        + (variant_similarity * 0.06)
        - (fragility * 0.08)
        - (variant_spread * 0.04)
    )
    semantic_compression = _b01(
        (load_reduction * 0.28)
        + (symbolic_object_distance * 0.22)
        + (symbolic_field_decoupling * 0.18)
        + (compound_load_reduction * 0.12)
        + (merge_pressure * 0.10)
        + (semantic_density * 0.10)
        - (zoom_need * 0.10)
        - (split_pressure * 0.06)
    )
    semantic_coherence = _b01(
        (semantic_density * 0.28)
        + (semantic_compression * 0.20)
        + (bearing * 0.16)
        + (stability * 0.14)
        + (context_confidence * 0.10)
        + (visual_coherence * 0.08)
        + (field_clarity * 0.04)
        - (field_fragmentation * 0.10)
        - (fragility * 0.08)
    )
    semantic_learning_need = _b01(
        (variant_learning_pressure * 0.26)
        + (zoom_need * 0.20)
        + (novelty * 0.16)
        + (uncertain_form_exposure * 0.14)
        + (split_pressure * 0.10)
        + (max(0.0, 0.48 - semantic_coherence) * 0.10)
        + (max(0.0, 0.44 - semantic_compression) * 0.04)
    )
    semantic_action_nearness = _b01(
        (learned_action_binding * 0.26)
        + (variant_bearing_memory * 0.18)
        + (bearing * 0.16)
        + (semantic_coherence * 0.14)
        + (compound_bearing * 0.10)
        + (symbolic_field_decoupling * 0.08)
        + (learned_action_trust * 0.08)
        - (learned_caution_trust * 0.10)
        - (semantic_learning_need * 0.08)
    )

    semantic_primary_layer_pressures = {
        "action_near_layer": _b01((semantic_action_nearness * 0.34) + (semantic_coherence * 0.22) + (learned_action_trust * 0.08)),
        "learning_layer": _b01((semantic_learning_need * 0.34) + ((1.0 - uncertainty_familiarity) * 0.14) + (variant_learning_pressure * 0.08)),
        "observation_layer": _b01((learned_observation_binding * 0.34) + ((1.0 - learned_action_binding) * 0.08) + (semantic_density * 0.06)),
        "reflective_layer": _b01((learned_reframe_binding * 0.26) + (symbolic_field_decoupling * 0.22) + (semantic_compression * 0.06)),
        "object_layer": _b01((symbolic_object_distance * 0.28) + (semantic_density * 0.22) + (semantic_compression * 0.06)),
        "structured_form_layer": _b01((semantic_density * 0.14) + (0.18 if form_symbol_scope == "structured_form" else 0.0)),
        "wide_form_layer": _b01((uncertain_form_exposure * 0.08) + (0.18 if form_symbol_scope == "wide_form" else 0.0)),
        "trace_layer": _b01((1.0 - max(semantic_density, semantic_coherence, semantic_action_nearness, semantic_learning_need)) * 0.24),
    }
    semantic_primary_layer = max(semantic_primary_layer_pressures, key=semantic_primary_layer_pressures.get)

    semantic_layer_pressure = 1.0
    for layer_value in (
        semantic_density,
        semantic_compression,
        symbolic_object_distance,
        learned_observation_binding,
        learned_reframe_binding,
        semantic_action_nearness,
        compound_maturity,
        uncertainty_familiarity,
    ):
        semantic_layer_pressure += _b01(float(layer_value) / 0.68)
    semantic_layer_count = int(max(1, min(8, round(semantic_layer_pressure))))

    semantic_packet_pressures = {
        "action_bearing_packet": _b01((semantic_action_nearness * 0.34) + (semantic_coherence * 0.24)),
        "condensed_object_packet": _b01((semantic_compression * 0.32) + (semantic_coherence * 0.22) + (symbolic_object_distance * 0.08)),
        "open_learning_packet": _b01((semantic_learning_need * 0.36) + (variant_learning_pressure * 0.10)),
        "watching_packet": _b01((learned_observation_binding * 0.34) + (semantic_density * 0.08)),
        "reflective_packet": _b01((learned_reframe_binding * 0.26) + (symbolic_field_decoupling * 0.24)),
        "compound_packet": _b01((compound_maturity * 0.26) + (compound_resonance * 0.22)),
        "named_form_packet": _b01((semantic_density * 0.30) + (semantic_coherence * 0.08)),
        "thin_trace": _b01((1.0 - max(semantic_density, semantic_compression, semantic_action_nearness, semantic_learning_need)) * 0.26),
    }
    semantic_packet_state = max(semantic_packet_pressures, key=semantic_packet_pressures.get)

    semantic_profile = "|".join(
        [
            str(form_symbol_scope),
            str(semantic_primary_layer),
            str(uncertain_form_family_state),
            str(compound_scope),
            str(semantic_packet_state),
        ]
    )

    return {
        "semantic_density": float(semantic_density),
        "semantic_compression": float(semantic_compression),
        "semantic_coherence": float(semantic_coherence),
        "semantic_learning_need": float(semantic_learning_need),
        "semantic_action_nearness": float(semantic_action_nearness),
        "semantic_primary_layer": str(semantic_primary_layer),
        "semantic_primary_layer_pressures": dict(semantic_primary_layer_pressures),
        "semantic_layer_count": int(semantic_layer_count),
        "semantic_layer_pressure": float(semantic_layer_pressure),
        "semantic_packet_state": str(semantic_packet_state),
        "semantic_packet_pressures": dict(semantic_packet_pressures),
        "semantic_profile": str(semantic_profile),
    }


def _learn_form_symbol_development_item(item, context=None, weight=1.0):

    ctx = dict(context or {})

    def _b01(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(0.0, min(1.0, float(value)))

    def _bs(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return max(-1.0, min(1.0, float(value)))

    development_sample = _bs(ctx.get("development_sample", 0.0))
    contact_maturity_sample = _b01(ctx.get("contact_maturity_sample", 0.0))
    contact_utility_sample = _b01(ctx.get("contact_utility_sample", 0.0))
    contact_pain_sample = _b01(ctx.get("contact_pain_sample", 0.0))
    contact_carefulness_sample = _b01(ctx.get("contact_carefulness_sample", 0.0))
    risk_width_pressure = _b01(ctx.get("risk_width_pressure", 0.0))
    reason = str(ctx.get("reason", "-") or "-")
    position_consequence_residual_for_memory = _b01(ctx.get("position_consequence_residual_for_memory", 0.0))
    structural_support = _b01(ctx.get("structural_support", 0.0))
    position_constructive_bearing = _b01(ctx.get("position_constructive_bearing", 0.0))
    position_consequence_burden = _b01(ctx.get("position_consequence_burden", 0.0))
    observation_sample = _b01(ctx.get("observation_sample", 0.0))
    reframe_sample = _b01(ctx.get("reframe_sample", 0.0))
    contact_learning_state = str(ctx.get("contact_learning_state", "neutral_contact") or "neutral_contact")
    timestamp = ctx.get("timestamp", None)

    learned = dict(item or {})
    prior_quality = _bs(learned.get("development_quality", 0.0))
    prior_action = _b01(learned.get("action_affinity", 0.50), default=0.50)
    prior_observe = _b01(learned.get("observation_affinity", 0.0))
    prior_reframe = _b01(learned.get("context_reframe_potential", 0.0))
    prior_contact_maturity = _b01(learned.get("contact_maturity", 0.0))
    prior_contact_utility = _b01(learned.get("contact_utility", 0.0))
    prior_contact_pain = _b01(learned.get("contact_pain_memory", 0.0))
    prior_contact_carefulness = _b01(learned.get("contact_carefulness", 0.0))
    prior_contact_burden_evidence = _b01(learned.get("contact_burden_evidence", 0.0))
    prior_contact_utility_evidence = _b01(learned.get("contact_utility_evidence", 0.0))
    sample = _bs(development_sample * float(weight))
    quality_alpha = 0.12 + (min(1.0, abs(sample) / 0.18) * 0.05)
    next_quality = _bs((prior_quality * (1.0 - quality_alpha)) + (sample * quality_alpha))
    contact_alpha = 0.12 + (contact_pain_sample * 0.06)
    next_contact_maturity = _b01((prior_contact_maturity * (1.0 - contact_alpha)) + (contact_maturity_sample * contact_alpha))
    next_contact_utility = _b01((prior_contact_utility * 0.86) + (contact_utility_sample * 0.14))
    next_contact_pain = _b01((prior_contact_pain * (1.0 - contact_alpha)) + (contact_pain_sample * contact_alpha))
    next_contact_carefulness = _b01((prior_contact_carefulness * 0.82) + (contact_carefulness_sample * 0.18))
    contact_burden_signal = _b01(
        (contact_pain_sample * 0.46)
        + (contact_carefulness_sample * 0.28)
        + (risk_width_pressure * 0.12 if reason == "sl_hit" else 0.0)
        + (max(0.0, -development_sample) * 0.14)
        + (position_consequence_residual_for_memory * 0.14)
    )
    contact_utility_signal = _b01(
        (contact_utility_sample * 0.42)
        + (contact_maturity_sample * 0.26)
        + (max(0.0, development_sample) * 0.18)
        + (structural_support * 0.14)
        + (position_constructive_bearing * 0.08)
        - (position_consequence_burden * 0.06)
    )
    burden_alpha = 0.14 + (_b01(max(0.0, -development_sample) + (0.35 if reason == "sl_hit" else 0.0)) * 0.10)
    utility_alpha = 0.12 + (_b01(max(0.0, development_sample)) * 0.08)
    next_contact_burden_evidence = _b01((prior_contact_burden_evidence * (1.0 - burden_alpha)) + (contact_burden_signal * burden_alpha))
    next_contact_utility_evidence = _b01((prior_contact_utility_evidence * (1.0 - utility_alpha)) + (contact_utility_signal * utility_alpha))
    action_target = _b01(
        0.47
        + (next_quality * 0.50)
        + ((structural_support - 0.50) * 0.26)
        + (next_contact_maturity * 0.15)
        + (next_contact_utility * 0.10)
        + (next_contact_utility_evidence * 0.05)
        - (observation_sample * 0.10)
        - (next_contact_pain * 0.14)
        - (next_contact_carefulness * 0.07)
        - (next_contact_burden_evidence * 0.06)
        - (risk_width_pressure * 0.12 if reason == "sl_hit" else 0.0),
        default=0.50,
    )
    observe_target = _b01(
        (observation_sample * 0.64)
        + (max(0.0, -next_quality) * 0.28)
        + (risk_width_pressure * 0.12 if reason == "sl_hit" else 0.0)
        + (next_contact_carefulness * 0.14)
        + (next_contact_burden_evidence * 0.08)
    )
    reframe_target = _b01((reframe_sample * 0.62) + (prior_reframe * 0.22) + (next_contact_carefulness * 0.10) + (next_contact_burden_evidence * 0.06))
    constructive_seen = int(learned.get("constructive_seen", 0) or 0)
    unconstructive_seen = int(learned.get("unconstructive_seen", 0) or 0)
    evidence_count = constructive_seen + unconstructive_seen + 1
    evidence_trust = _b01(evidence_count / float(evidence_count + 10))
    consistency_trust = _b01(abs(next_quality) * 1.45)
    caution_evidence_bias = _b01((unconstructive_seen + (1 if development_sample < 0.0 else 0)) / float(evidence_count + 2))
    action_evidence_bias = _b01((constructive_seen + (1 if development_sample >= 0.0 else 0)) / float(evidence_count + 2))
    learning_target = _b01((evidence_trust * 0.58) + (consistency_trust * 0.42))
    learned["development_quality"] = float(next_quality)
    plasticity = 0.13 + (_b01(max(0.0, -development_sample)) * 0.05)
    learned["action_affinity"] = float(_b01((prior_action * (1.0 - plasticity)) + (action_target * plasticity), default=0.50))
    learned["observation_affinity"] = float(_b01((prior_observe * 0.80) + (observe_target * 0.20)))
    learned["context_reframe_potential"] = float(_b01((prior_reframe * 0.84) + (reframe_target * 0.16)))
    learned["contact_maturity"] = float(next_contact_maturity)
    learned["contact_utility"] = float(next_contact_utility)
    learned["contact_pain_memory"] = float(next_contact_pain)
    learned["contact_carefulness"] = float(next_contact_carefulness)
    learned["contact_burden_evidence"] = float(next_contact_burden_evidence)
    learned["contact_utility_evidence"] = float(next_contact_utility_evidence)
    contact_state_pressures = {
        "protective_reorganization_contact": _b01(
            (0.24 if contact_learning_state == "protective_reorganization_contact" else 0.0)
            + ((1.0 - next_contact_maturity) * 0.16)
            + (position_consequence_burden * 0.14)
            + (reframe_sample * 0.08)
        ),
        "careful_contact": _b01(
            (next_contact_burden_evidence * 0.30)
            + (next_contact_carefulness * 0.24)
            + ((1.0 - next_contact_maturity) * 0.12)
        ),
        "burdened_contact": _b01(
            (next_contact_pain * 0.30)
            + ((1.0 - next_contact_maturity) * 0.12)
            + (max(0.0, -next_quality) * 0.22)
        ),
        "constructive_contact": _b01(
            (next_contact_utility_evidence * 0.28)
            + (next_contact_utility * 0.22)
            + (next_contact_maturity * 0.18)
            + (max(0.0, next_quality) * 0.10)
            - (next_contact_pain * 0.10)
        ),
        "learning_contact": _b01(
            (next_contact_burden_evidence * 0.16)
            + (next_contact_carefulness * 0.14)
            + (observation_sample * 0.10)
            + (reframe_sample * 0.08)
        ),
        "maturing_contact": _b01(
            (next_contact_maturity * 0.26)
            + (next_contact_utility * 0.10)
            + (next_contact_utility_evidence * 0.08)
        ),
        "neutral_contact": _b01(
            (1.0 - max(next_contact_maturity, next_contact_pain, next_contact_utility_evidence, next_contact_burden_evidence)) * 0.20
        ),
    }
    stored_contact_state = max(contact_state_pressures, key=contact_state_pressures.get)
    learned["contact_learning_state"] = str(stored_contact_state)
    learned["contact_state_pressures"] = dict(contact_state_pressures)
    if development_sample >= 0.0:
        learned["constructive_seen"] = int(learned.get("constructive_seen", 0) or 0) + 1
    else:
        learned["unconstructive_seen"] = int(learned.get("unconstructive_seen", 0) or 0) + 1
    prior_learning_trust = _b01(learned.get("learning_trust", 0.0))
    prior_action_trust = _b01(learned.get("action_trust", 0.0))
    prior_caution_trust = _b01(learned.get("caution_trust", 0.0))
    action_trust_target = _b01(
        (
            (max(0.0, next_quality) * 0.72)
            + (action_evidence_bias * max(0.0, structural_support - 0.45) * 0.28)
        )
        * learning_target
        * (0.55 + structural_support * 0.45)
    )
    caution_trust_target = _b01(
        (
            (max(0.0, -next_quality) * 0.56)
            + (caution_evidence_bias * 0.30)
            + (risk_width_pressure * 0.14 if reason == "sl_hit" else 0.0)
            + (next_contact_pain * 0.16)
            + (next_contact_carefulness * 0.10)
            + (next_contact_burden_evidence * 0.08)
        )
        * learning_target
        * (0.62 + observation_sample * 0.38)
    )
    learned["learning_trust"] = float(_b01((prior_learning_trust * 0.82) + (learning_target * 0.18)))
    learned["action_trust"] = float(_b01((prior_action_trust * 0.84) + (action_trust_target * 0.16)))
    caution_alpha = 0.22 + (_b01(max(0.0, -development_sample)) * 0.08)
    learned["caution_trust"] = float(_b01((prior_caution_trust * (1.0 - caution_alpha)) + (caution_trust_target * caution_alpha)))
    learned["last_development_reason"] = str(reason or "-")
    learned["last_development_sample"] = float(development_sample)
    learned["last_contact_maturity_sample"] = float(contact_maturity_sample)
    learned["last_contact_utility_sample"] = float(contact_utility_sample)
    learned["last_contact_pain_sample"] = float(contact_pain_sample)
    learned["last_contact_carefulness_sample"] = float(contact_carefulness_sample)
    learned["last_development_ts"] = timestamp
    return learned
