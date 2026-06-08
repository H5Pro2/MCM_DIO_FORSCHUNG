"""Form-symbol orchestration for DIO.

This module builds and updates the active form-symbol state from visual,
structural, perceptual and felt state. It keeps the same mechanics that used
to live in MCM_Brain_Modell.py; the Brain now calls this as a bridge.
"""

import hashlib

from config import Config
from core.form_language import (
    _build_form_symbol_compound_item as _build_form_symbol_compound_item_impl,
    _build_form_symbol_base_quality_state as _build_form_symbol_base_quality_state_impl,
    _build_form_symbol_identity_state as _build_form_symbol_identity_state_impl,
    _build_form_symbol_object_state as _build_form_symbol_object_state_impl,
    _build_form_symbol_semantic_state as _build_form_symbol_semantic_state_impl,
    _build_form_symbol_variant_family_state as _build_form_symbol_variant_family_state_impl,
    _extract_outcome_form_symbol_state as _extract_outcome_form_symbol_state_impl,
    _learn_form_symbol_development_item as _learn_form_symbol_development_item_impl,
    _update_form_symbol_item_memory_stats as _update_form_symbol_item_memory_stats_impl,
)
from memory.form_symbol_memory import (
    _ensure_form_symbol_memory_loaded,
    _flush_form_symbol_memory_if_due,
)


def build_form_symbol_state(bot, visual_market_state=None, structure_perception_state=None, perception_state=None, felt_state=None, snapshot=None):

    visual = dict(visual_market_state or {})
    structure = dict(structure_perception_state or {})
    perception = dict(perception_state or {})
    felt = dict(felt_state or {})
    snap = dict(snapshot or {})

    if not isinstance(getattr(bot, "form_symbol_space", None), dict):
        if bot is not None:
            bot.form_symbol_space = {}
    if not isinstance(getattr(bot, "form_symbol_compound_space", None), dict):
        if bot is not None:
            bot.form_symbol_compound_space = {}

    if bot is not None:
        _ensure_form_symbol_memory_loaded(bot)

    spatial_bias = float(visual.get("spatial_bias", perception.get("spatial_bias", 0.0)) or 0.0)
    directional_bias = float(visual.get("directional_bias", perception.get("directional_bias", 0.0)) or 0.0)
    range_position = float(visual.get("range_position", perception.get("range_position", 0.0)) or 0.0)
    short_impulse = float(visual.get("short_impulse", 0.0) or 0.0)
    mid_impulse = float(visual.get("mid_impulse", 0.0) or 0.0)
    compression = float(visual.get("compression", 0.0) or 0.0)
    expansion = float(visual.get("expansion", 0.0) or 0.0)
    body_pressure = float(visual.get("body_pressure", 0.0) or 0.0)
    wick_pressure = float(visual.get("wick_pressure", 0.0) or 0.0)
    market_balance = float(visual.get("market_balance", perception.get("market_balance", 0.0)) or 0.0)
    breakout_tension = float(visual.get("breakout_tension", perception.get("breakout_tension", 0.0)) or 0.0)
    visual_coherence = float(visual.get("visual_coherence", perception.get("visual_coherence", 0.0)) or 0.0)
    visual_clarity = float(visual.get("visual_clarity", perception.get("visual_clarity", 0.0)) or 0.0)
    visual_object_stability = float(visual.get("visual_object_stability", perception.get("visual_object_stability", 0.0)) or 0.0)
    visual_form_novelty = float(visual.get("visual_form_novelty", perception.get("visual_form_novelty", 0.0)) or 0.0)
    visual_blindness = float(visual.get("visual_blindness", perception.get("visual_blindness", 0.0)) or 0.0)
    visual_form_pressure = float(visual.get("visual_form_pressure", perception.get("visual_form_pressure", 0.0)) or 0.0)
    visual_shape_resonance = float(visual.get("visual_shape_resonance", perception.get("visual_shape_resonance", 0.0)) or 0.0)
    visual_shape_fragility = float(visual.get("visual_shape_fragility", perception.get("visual_shape_fragility", 0.0)) or 0.0)
    structure_quality = float(structure.get("structure_quality", perception.get("structure_quality", felt.get("structure_quality", 0.0))) or 0.0)
    zone_proximity = float(structure.get("zone_proximity", perception.get("zone_proximity", 0.0)) or 0.0)
    context_confidence = float(structure.get("context_confidence", perception.get("context_confidence", felt.get("context_confidence", 0.0))) or 0.0)
    stress_relief_potential = float(structure.get("stress_relief_potential", perception.get("stress_relief_potential", felt.get("stress_relief_potential", 0.0))) or 0.0)
    field_clarity = float(felt.get("field_perception_clarity", snap.get("field_perception_clarity", 0.0)) or 0.0)
    field_pressure = float(felt.get("field_perception_pressure", snap.get("field_perception_pressure", 0.0)) or 0.0)
    field_fragmentation = float(felt.get("field_perception_fragmentation", snap.get("field_perception_fragmentation", 0.0)) or 0.0)

    identity_state = _build_form_symbol_identity_state_impl({
        "spatial_bias": float(spatial_bias),
        "directional_bias": float(directional_bias),
        "range_position": float(range_position),
        "short_impulse": float(short_impulse),
        "mid_impulse": float(mid_impulse),
        "compression": float(compression),
        "expansion": float(expansion),
        "body_pressure": float(body_pressure),
        "wick_pressure": float(wick_pressure),
        "market_balance": float(market_balance),
        "breakout_tension": float(breakout_tension),
        "visual_coherence": float(visual_coherence),
        "structure_quality": float(structure_quality),
        "zone_proximity": float(zone_proximity),
        "context_confidence": float(context_confidence),
        "stress_relief_potential": float(stress_relief_potential),
        "field_clarity": float(field_clarity),
        "field_pressure": float(field_pressure),
        "field_fragmentation": float(field_fragmentation),
    })
    form_vector = list(identity_state.get("form_vector", []) or [])
    form_key = str(identity_state.get("form_key", "-") or "-")
    form_resolution_quality = float(identity_state.get("form_resolution_quality", 0.0) or 0.0)
    form_detail_pressure = float(identity_state.get("form_detail_pressure", 0.0) or 0.0)
    form_symbol_scope = str(identity_state.get("form_symbol_scope", "wide_trace") or "wide_trace")
    form_symbol_abstraction_level = int(identity_state.get("form_symbol_abstraction_level", 0) or 0)
    family_vector = list(identity_state.get("family_vector", []) or [])
    family_key = str(identity_state.get("family_key", "-") or "-")
    symbol_id = str(identity_state.get("symbol_id", "-") or "-")

    symbol_space = dict(getattr(bot, "form_symbol_space", {}) or {}) if bot is not None else {}
    item = dict(symbol_space.get(symbol_id, {}) or {})
    symbol_memory_stats = _update_form_symbol_item_memory_stats_impl(item, form_vector)
    distance = float(symbol_memory_stats.get("distance", 0.0) or 0.0)
    seen = int(symbol_memory_stats.get("seen", 0) or 0)
    new_avg = list(symbol_memory_stats.get("avg_vector", form_vector) or form_vector)
    variance = float(symbol_memory_stats.get("variance", 0.0) or 0.0)
    maturity = float(symbol_memory_stats.get("maturity", 0.0) or 0.0)
    stability = float(symbol_memory_stats.get("stability", 0.0) or 0.0)
    novelty = float(symbol_memory_stats.get("novelty", 0.0) or 0.0)
    resonance = float(symbol_memory_stats.get("resonance", 0.0) or 0.0)
    learned_development_quality = float(symbol_memory_stats.get("learned_development_quality", 0.0) or 0.0)
    learned_action_affinity = float(symbol_memory_stats.get("learned_action_affinity", 0.50) or 0.50)
    learned_observation_affinity = float(symbol_memory_stats.get("learned_observation_affinity", 0.0) or 0.0)
    learned_reframe_potential = float(symbol_memory_stats.get("learned_reframe_potential", 0.0) or 0.0)
    learned_learning_trust = float(symbol_memory_stats.get("learned_learning_trust", 0.0) or 0.0)
    learned_action_trust = float(symbol_memory_stats.get("learned_action_trust", 0.0) or 0.0)
    learned_caution_trust = float(symbol_memory_stats.get("learned_caution_trust", 0.0) or 0.0)
    learned_contact_maturity = float(symbol_memory_stats.get("learned_contact_maturity", 0.0) or 0.0)
    learned_contact_utility = float(symbol_memory_stats.get("learned_contact_utility", 0.0) or 0.0)
    learned_contact_pain_memory = float(symbol_memory_stats.get("learned_contact_pain_memory", 0.0) or 0.0)
    learned_contact_carefulness = float(symbol_memory_stats.get("learned_contact_carefulness", 0.0) or 0.0)
    learned_contact_burden_evidence = float(symbol_memory_stats.get("learned_contact_burden_evidence", 0.0) or 0.0)
    learned_contact_utility_evidence = float(symbol_memory_stats.get("learned_contact_utility_evidence", 0.0) or 0.0)
    learned_contact_state = str(symbol_memory_stats.get("learned_contact_state", "unformed_contact") or "unformed_contact")

    base_quality_state = _build_form_symbol_base_quality_state_impl({
        "directional_bias": float(directional_bias),
        "breakout_tension": float(breakout_tension),
        "range_position": float(range_position),
        "body_pressure": float(body_pressure),
        "wick_pressure": float(wick_pressure),
        "field_pressure": float(field_pressure),
        "field_fragmentation": float(field_fragmentation),
        "market_balance": float(market_balance),
        "visual_coherence": float(visual_coherence),
        "structure_quality": float(structure_quality),
        "context_confidence": float(context_confidence),
        "stress_relief_potential": float(stress_relief_potential),
        "field_clarity": float(field_clarity),
        "stability": float(stability),
        "maturity": float(maturity),
        "distance": float(distance),
        "novelty": float(novelty),
        "form_resolution_quality": float(form_resolution_quality),
        "form_detail_pressure": float(form_detail_pressure),
    })
    relevance = float(base_quality_state.get("relevance", 0.0) or 0.0)
    bearing = float(base_quality_state.get("bearing", 0.0) or 0.0)
    fragility = float(base_quality_state.get("fragility", 0.0) or 0.0)
    resonance = float(base_quality_state.get("resonance", 0.0) or 0.0)
    zoom_need = float(base_quality_state.get("zoom_need", 0.0) or 0.0)
    load_reduction = float(base_quality_state.get("load_reduction", 0.0) or 0.0)
    learned_development_quality = max(-1.0, min(1.0, float(item.get("development_quality", 0.0) or 0.0)))
    learned_action_affinity = max(0.0, min(1.0, float(item.get("action_affinity", 0.50) or 0.50)))
    learned_observation_affinity = max(0.0, min(1.0, float(item.get("observation_affinity", 0.0) or 0.0)))
    learned_reframe_potential = max(0.0, min(1.0, float(item.get("context_reframe_potential", 0.0) or 0.0)))
    learned_learning_trust = max(0.0, min(1.0, float(item.get("learning_trust", 0.0) or 0.0)))
    learned_action_trust = max(0.0, min(1.0, float(item.get("action_trust", 0.0) or 0.0)))
    learned_caution_trust = max(0.0, min(1.0, float(item.get("caution_trust", 0.0) or 0.0)))
    learned_contact_maturity = max(0.0, min(1.0, float(item.get("contact_maturity", 0.0) or 0.0)))
    learned_contact_utility = max(0.0, min(1.0, float(item.get("contact_utility", 0.0) or 0.0)))
    learned_contact_pain_memory = max(0.0, min(1.0, float(item.get("contact_pain_memory", 0.0) or 0.0)))
    learned_contact_carefulness = max(0.0, min(1.0, float(item.get("contact_carefulness", 0.0) or 0.0)))
    learned_contact_burden_evidence = max(0.0, min(1.0, float(item.get("contact_burden_evidence", 0.0) or 0.0)))
    learned_contact_utility_evidence = max(0.0, min(1.0, float(item.get("contact_utility_evidence", 0.0) or 0.0)))
    learned_contact_state = str(item.get("contact_learning_state", "unformed_contact") or "unformed_contact")
    object_state = _build_form_symbol_object_state_impl({
        "maturity": float(maturity),
        "stability": float(stability),
        "resonance": float(resonance),
        "bearing": float(bearing),
        "fragility": float(fragility),
        "form_resolution_quality": float(form_resolution_quality),
        "load_reduction": float(load_reduction),
        "zoom_need": float(zoom_need),
        "form_detail_pressure": float(form_detail_pressure),
        "variance": float(variance),
        "novelty": float(novelty),
        "visual_blindness": float(visual_blindness),
        "visual_clarity": float(visual_clarity),
        "visual_object_stability": float(visual_object_stability),
        "visual_shape_fragility": float(visual_shape_fragility),
        "visual_form_pressure": float(visual_form_pressure),
        "visual_form_novelty": float(visual_form_novelty),
        "visual_shape_resonance": float(visual_shape_resonance),
    })
    symbolic_object_distance = float(object_state.get("symbolic_object_distance", 0.0) or 0.0)
    symbolic_containment = float(object_state.get("symbolic_containment", 0.0) or 0.0)
    symbolic_field_decoupling = float(object_state.get("symbolic_field_decoupling", 0.0) or 0.0)
    split_pressure = float(object_state.get("split_pressure", 0.0) or 0.0)
    merge_pressure = float(object_state.get("merge_pressure", 0.0) or 0.0)
    uncertain_form_exposure = float(object_state.get("uncertain_form_exposure", 0.0) or 0.0)

    previous_state = dict(getattr(bot, "_last_form_symbol_state", {}) or {}) if bot is not None else {}
    previous_symbol_id = str(previous_state.get("form_symbol_id", "") or "").strip()
    compound_space = dict(getattr(bot, "form_symbol_compound_space", {}) or {}) if bot is not None else {}
    compound_key_preview = f"{previous_symbol_id}>{symbol_id}" if previous_symbol_id and previous_symbol_id != "-" and previous_symbol_id != symbol_id else "-"
    compound_id_preview = "-"
    compound_item_source = {}
    if compound_key_preview != "-":
        compound_id_preview = "fc_" + hashlib.sha1(str(compound_key_preview).encode("utf-8")).hexdigest()[:10]
        compound_item_source = dict(compound_space.get(compound_id_preview, {}) or {})

    compound_state = _build_form_symbol_compound_item_impl(
        previous_symbol_id=previous_symbol_id,
        symbol_id=symbol_id,
        previous_state=previous_state,
        current_metrics={
            "bearing": float(bearing),
            "stability": float(stability),
            "resonance": float(resonance),
            "form_resolution_quality": float(form_resolution_quality),
        },
        compound_item=compound_item_source,
        timestamp=getattr(bot, "current_timestamp", None) if bot is not None else None,
    )
    compound_id = str(compound_state.get("compound_id", "-") or "-")
    compound_key = str(compound_state.get("compound_key", "-") or "-")
    compound_scope = str(compound_state.get("compound_scope", "single") or "single")
    compound_seen = int(compound_state.get("compound_seen", 0) or 0)
    compound_maturity = float(compound_state.get("compound_maturity", 0.0) or 0.0)
    compound_stability = float(compound_state.get("compound_stability", 0.0) or 0.0)
    compound_resonance = float(compound_state.get("compound_resonance", 0.0) or 0.0)
    compound_bearing = float(compound_state.get("compound_bearing", 0.0) or 0.0)
    compound_load_reduction = float(compound_state.get("compound_load_reduction", 0.0) or 0.0)
    compound_novelty = float(compound_state.get("compound_novelty", 1.0) or 1.0)
    compound_development_quality = float(compound_state.get("compound_development_quality", 0.0) or 0.0)
    compound_action_affinity = float(compound_state.get("compound_action_affinity", 0.50) or 0.50)
    compound_observation_affinity = float(compound_state.get("compound_observation_affinity", 0.0) or 0.0)
    compound_reframe_potential = float(compound_state.get("compound_reframe_potential", 0.0) or 0.0)
    compound_learning_trust = float(compound_state.get("compound_learning_trust", 0.0) or 0.0)
    compound_action_trust = float(compound_state.get("compound_action_trust", 0.0) or 0.0)
    compound_caution_trust = float(compound_state.get("compound_caution_trust", 0.0) or 0.0)
    compound_contact_maturity = float(compound_state.get("compound_contact_maturity", 0.0) or 0.0)
    compound_contact_utility = float(compound_state.get("compound_contact_utility", 0.0) or 0.0)
    compound_contact_pain_memory = float(compound_state.get("compound_contact_pain_memory", 0.0) or 0.0)
    compound_contact_carefulness = float(compound_state.get("compound_contact_carefulness", 0.0) or 0.0)
    compound_contact_burden_evidence = float(compound_state.get("compound_contact_burden_evidence", 0.0) or 0.0)
    compound_contact_utility_evidence = float(compound_state.get("compound_contact_utility_evidence", 0.0) or 0.0)
    compound_contact_state = str(compound_state.get("compound_contact_state", "unformed_contact") or "unformed_contact")
    if bool(compound_state.get("has_compound", False)) and bot is not None and compound_id != "-":
        compound_space[compound_id] = dict(compound_state.get("compound_item", {}) or {})
        bot.form_symbol_compound_space = dict(compound_space)

    learned_action_binding = max(
        0.0,
        min(
            1.0,
            (learned_action_affinity * 0.58)
            + (compound_action_affinity * 0.24 * max(0.0, min(1.0, compound_maturity)))
            + (bearing * 0.18)
            + (learned_action_trust * 0.08)
            - (learned_observation_affinity * 0.08)
            - (learned_reframe_potential * 0.05)
            - (learned_caution_trust * 0.18),
        ),
    )
    learned_observation_binding = max(
        0.0,
        min(
            1.0,
            (learned_observation_affinity * 0.62)
            + (compound_observation_affinity * 0.24 * max(0.0, min(1.0, compound_maturity)))
            + (fragility * 0.14),
        ),
    )
    learned_reframe_binding = max(
        0.0,
        min(
            1.0,
            (learned_reframe_potential * 0.60)
            + (compound_reframe_potential * 0.26 * max(0.0, min(1.0, compound_maturity)))
            + (max(0.0, 0.48 - bearing) * 0.14),
        ),
    )

    item.update({
        "symbol_id": str(symbol_id),
        "form_key": str(family_key),
        "family_key": str(family_key),
        "variant_key": str(form_key),
        "scope": str(form_symbol_scope),
        "abstraction_level": int(form_symbol_abstraction_level),
        "resolution_quality": float(form_resolution_quality),
        "detail_pressure": float(form_detail_pressure),
        "symbolic_object_distance": float(symbolic_object_distance),
        "symbolic_containment": float(symbolic_containment),
        "symbolic_field_decoupling": float(symbolic_field_decoupling),
        "development_quality": float(learned_development_quality),
        "action_affinity": float(learned_action_affinity),
        "observation_affinity": float(learned_observation_affinity),
        "context_reframe_potential": float(learned_reframe_potential),
        "learning_trust": float(learned_learning_trust),
        "action_trust": float(learned_action_trust),
        "caution_trust": float(learned_caution_trust),
        "seen": int(seen),
        "avg_vector": [float(v) for v in new_avg],
        "variance": float(variance),
        "maturity": float(maturity),
        "stability": float(stability),
        "resonance": float(resonance),
        "bearing": float(bearing),
        "fragility": float(fragility),
        "last_zoom_need": float(zoom_need),
        "last_load_reduction": float(load_reduction),
        "first_seen_ts": item.get("first_seen_ts", getattr(bot, "current_timestamp", None) if bot is not None else None),
        "last_seen_ts": getattr(bot, "current_timestamp", None) if bot is not None else None,
    })
    variants = dict(item.get("variants", {}) or {})
    variant_item = dict(variants.get(form_key, {}) or {})
    variant_item["seen"] = int(variant_item.get("seen", 0) or 0) + 1
    variant_item["distance"] = float(distance)
    variant_item["bearing"] = float(bearing)
    variant_item["fragility"] = float(fragility)
    variant_item["visual_blindness"] = float(visual_blindness)
    variant_item["visual_clarity"] = float(visual_clarity)
    variant_item["object_stability"] = float(visual_object_stability)
    variant_item["uncertain_exposure"] = float(uncertain_form_exposure)
    variant_item["last_seen_ts"] = getattr(bot, "current_timestamp", None) if bot is not None else None
    variants[str(form_key)] = dict(variant_item)
    max_variants = max(1, int(getattr(Config, "MCM_FORM_SYMBOL_MEMORY_MAX_VARIANTS", 12) or 12))
    item["variants"] = dict(
        sorted(
            variants.items(),
            key=lambda kv: int((kv[1] or {}).get("seen", 0) or 0) if isinstance(kv[1], dict) else 0,
            reverse=True,
        )[:max_variants]
    )
    variant_family_state = _build_form_symbol_variant_family_state_impl(
        item.get("variants", {}) or {},
        {
            "distance": float(distance),
            "stability": float(stability),
            "resonance": float(resonance),
            "variance": float(variance),
            "max_variants": int(max_variants),
            "novelty": float(novelty),
            "visual_form_novelty": float(visual_form_novelty),
            "maturity": float(maturity),
            "learned_learning_trust": float(learned_learning_trust),
            "bearing": float(bearing),
            "learned_development_quality": float(learned_development_quality),
            "learned_action_trust": float(learned_action_trust),
            "visual_shape_resonance": float(visual_shape_resonance),
            "uncertain_form_exposure": float(uncertain_form_exposure),
            "learned_observation_affinity": float(learned_observation_affinity),
            "learned_reframe_potential": float(learned_reframe_potential),
        },
    )
    variant_count = int(variant_family_state.get("variant_count", 0) or 0)
    variant_seen_total = int(variant_family_state.get("variant_seen_total", 0) or 0)
    variant_exposure_mean = float(variant_family_state.get("variant_exposure_mean", 0.0) or 0.0)
    variant_bearing_mean = float(variant_family_state.get("variant_bearing_mean", 0.0) or 0.0)
    variant_similarity = float(variant_family_state.get("variant_similarity", 0.0) or 0.0)
    variant_spread = float(variant_family_state.get("variant_spread", 0.0) or 0.0)
    uncertainty_familiarity = float(variant_family_state.get("uncertainty_familiarity", 0.0) or 0.0)
    variant_bearing_memory = float(variant_family_state.get("variant_bearing_memory", 0.0) or 0.0)
    variant_learning_pressure = float(variant_family_state.get("variant_learning_pressure", 0.0) or 0.0)
    uncertain_form_family_state = str(variant_family_state.get("uncertain_form_family_state", "quiet_form_family") or "quiet_form_family")

    semantic_state = _build_form_symbol_semantic_state_impl({
        "form_resolution_quality": float(form_resolution_quality),
        "maturity": float(maturity),
        "stability": float(stability),
        "resonance": float(resonance),
        "bearing": float(bearing),
        "symbolic_containment": float(symbolic_containment),
        "uncertainty_familiarity": float(uncertainty_familiarity),
        "variant_similarity": float(variant_similarity),
        "fragility": float(fragility),
        "variant_spread": float(variant_spread),
        "load_reduction": float(load_reduction),
        "symbolic_object_distance": float(symbolic_object_distance),
        "symbolic_field_decoupling": float(symbolic_field_decoupling),
        "compound_load_reduction": float(compound_load_reduction),
        "merge_pressure": float(merge_pressure),
        "zoom_need": float(zoom_need),
        "split_pressure": float(split_pressure),
        "context_confidence": float(context_confidence),
        "visual_coherence": float(visual_coherence),
        "field_clarity": float(field_clarity),
        "field_fragmentation": float(field_fragmentation),
        "variant_learning_pressure": float(variant_learning_pressure),
        "novelty": float(novelty),
        "uncertain_form_exposure": float(uncertain_form_exposure),
        "learned_action_binding": float(learned_action_binding),
        "variant_bearing_memory": float(variant_bearing_memory),
        "compound_bearing": float(compound_bearing),
        "learned_action_trust": float(learned_action_trust),
        "learned_caution_trust": float(learned_caution_trust),
        "learned_observation_binding": float(learned_observation_binding),
        "learned_reframe_binding": float(learned_reframe_binding),
        "compound_maturity": float(compound_maturity),
        "compound_resonance": float(compound_resonance),
        "form_symbol_scope": str(form_symbol_scope),
        "uncertain_form_family_state": str(uncertain_form_family_state),
        "compound_scope": str(compound_scope),
    })
    semantic_density = float(semantic_state.get("semantic_density", 0.0) or 0.0)
    semantic_compression = float(semantic_state.get("semantic_compression", 0.0) or 0.0)
    semantic_coherence = float(semantic_state.get("semantic_coherence", 0.0) or 0.0)
    semantic_learning_need = float(semantic_state.get("semantic_learning_need", 0.0) or 0.0)
    semantic_action_nearness = float(semantic_state.get("semantic_action_nearness", 0.0) or 0.0)
    semantic_primary_layer = str(semantic_state.get("semantic_primary_layer", "trace_layer") or "trace_layer")
    semantic_layer_count = int(semantic_state.get("semantic_layer_count", 1) or 1)
    semantic_packet_state = str(semantic_state.get("semantic_packet_state", "thin_trace") or "thin_trace")
    semantic_profile = str(semantic_state.get("semantic_profile", "-") or "-")

    item.update({
        "uncertain_form_exposure": float(uncertain_form_exposure),
        "uncertainty_familiarity": float(uncertainty_familiarity),
        "variant_similarity": float(variant_similarity),
        "variant_spread": float(variant_spread),
        "variant_learning_pressure": float(variant_learning_pressure),
        "variant_bearing_memory": float(variant_bearing_memory),
        "uncertain_form_family_state": str(uncertain_form_family_state),
        "semantic_density": float(semantic_density),
        "semantic_compression": float(semantic_compression),
        "semantic_coherence": float(semantic_coherence),
        "semantic_learning_need": float(semantic_learning_need),
        "semantic_action_nearness": float(semantic_action_nearness),
        "semantic_primary_layer": str(semantic_primary_layer),
        "semantic_layer_count": int(semantic_layer_count),
        "semantic_packet_state": str(semantic_packet_state),
        "semantic_profile": str(semantic_profile),
    })

    if bot is not None:
        symbol_space[symbol_id] = dict(item)
        bot.form_symbol_space = dict(symbol_space)
        bot._form_symbol_memory_dirty = True
        bot._form_symbol_memory_updates = int(getattr(bot, "_form_symbol_memory_updates", 0) or 0) + 1
        bot.form_symbol_state = {
            "form_symbol_id": str(symbol_id),
            "form_symbol_key": str(family_key),
            "form_symbol_family_key": str(family_key),
            "form_symbol_variant_key": str(form_key),
            "form_symbol_scope": str(form_symbol_scope),
            "form_symbol_abstraction_level": int(form_symbol_abstraction_level),
            "form_symbol_resolution_quality": float(form_resolution_quality),
            "form_symbol_detail_pressure": float(form_detail_pressure),
            "form_symbol_object_distance": float(symbolic_object_distance),
            "form_symbol_containment": float(symbolic_containment),
            "form_symbol_field_decoupling": float(symbolic_field_decoupling),
            "form_symbol_development_quality": float(learned_development_quality),
            "form_symbol_action_affinity": float(learned_action_affinity),
            "form_symbol_observation_affinity": float(learned_observation_affinity),
            "form_symbol_reframe_potential": float(learned_reframe_potential),
            "form_symbol_learning_trust": float(learned_learning_trust),
            "form_symbol_action_trust": float(learned_action_trust),
            "form_symbol_caution_trust": float(learned_caution_trust),
            "form_symbol_contact_maturity": float(learned_contact_maturity),
            "form_symbol_contact_utility": float(learned_contact_utility),
            "form_symbol_contact_pain_memory": float(learned_contact_pain_memory),
            "form_symbol_contact_carefulness": float(learned_contact_carefulness),
            "form_symbol_contact_burden_evidence": float(learned_contact_burden_evidence),
            "form_symbol_contact_utility_evidence": float(learned_contact_utility_evidence),
            "form_symbol_contact_learning_state": str(learned_contact_state),
            "form_symbol_action_binding": float(learned_action_binding),
            "form_symbol_observation_binding": float(learned_observation_binding),
            "form_symbol_reframe_binding": float(learned_reframe_binding),
            "form_symbol_seen": int(seen),
            "form_symbol_maturity": float(maturity),
            "form_symbol_stability": float(stability),
            "form_symbol_resonance": float(resonance),
            "form_symbol_load_reduction": float(load_reduction),
            "form_symbol_zoom_need": float(zoom_need),
            "form_symbol_split_pressure": float(split_pressure),
            "form_symbol_merge_pressure": float(merge_pressure),
            "form_symbol_bearing": float(bearing),
            "form_symbol_fragility": float(fragility),
            "form_symbol_relevance": float(relevance),
            "form_symbol_novelty": float(novelty),
            "form_symbol_distance": float(distance),
            "uncertain_form_family_state": str(uncertain_form_family_state),
            "uncertain_form_exposure": float(uncertain_form_exposure),
            "uncertainty_familiarity": float(uncertainty_familiarity),
            "variant_similarity": float(variant_similarity),
            "variant_spread": float(variant_spread),
            "variant_learning_pressure": float(variant_learning_pressure),
            "variant_bearing_memory": float(variant_bearing_memory),
            "form_symbol_semantic_density": float(semantic_density),
            "form_symbol_semantic_compression": float(semantic_compression),
            "form_symbol_semantic_coherence": float(semantic_coherence),
            "form_symbol_semantic_learning_need": float(semantic_learning_need),
            "form_symbol_semantic_action_nearness": float(semantic_action_nearness),
            "form_symbol_semantic_primary_layer": str(semantic_primary_layer),
            "form_symbol_semantic_layer_count": int(semantic_layer_count),
            "form_symbol_semantic_packet_state": str(semantic_packet_state),
            "form_symbol_semantic_profile": str(semantic_profile),
            "form_symbol_compound_id": str(compound_id),
            "form_symbol_compound_key": str(compound_key),
            "form_symbol_compound_scope": str(compound_scope),
            "form_symbol_compound_seen": int(compound_seen),
            "form_symbol_compound_maturity": float(compound_maturity),
            "form_symbol_compound_stability": float(compound_stability),
            "form_symbol_compound_resonance": float(compound_resonance),
            "form_symbol_compound_bearing": float(compound_bearing),
            "form_symbol_compound_load_reduction": float(compound_load_reduction),
            "form_symbol_compound_novelty": float(compound_novelty),
            "form_symbol_compound_development_quality": float(compound_development_quality),
            "form_symbol_compound_action_affinity": float(compound_action_affinity),
            "form_symbol_compound_observation_affinity": float(compound_observation_affinity),
            "form_symbol_compound_reframe_potential": float(compound_reframe_potential),
            "form_symbol_compound_learning_trust": float(compound_learning_trust),
            "form_symbol_compound_action_trust": float(compound_action_trust),
            "form_symbol_compound_caution_trust": float(compound_caution_trust),
            "form_symbol_compound_contact_maturity": float(compound_contact_maturity),
            "form_symbol_compound_contact_utility": float(compound_contact_utility),
            "form_symbol_compound_contact_pain_memory": float(compound_contact_pain_memory),
            "form_symbol_compound_contact_carefulness": float(compound_contact_carefulness),
            "form_symbol_compound_contact_burden_evidence": float(compound_contact_burden_evidence),
            "form_symbol_compound_contact_utility_evidence": float(compound_contact_utility_evidence),
            "form_symbol_compound_contact_learning_state": str(compound_contact_state),
            "form_symbol_memory_loaded": bool(getattr(bot, "_form_symbol_memory_loaded", False)),
            "form_symbol_memory_symbol_count": int(len(getattr(bot, "form_symbol_space", {}) or {})),
            "form_symbol_memory_compound_count": int(len(getattr(bot, "form_symbol_compound_space", {}) or {})),
        }
        bot._last_form_symbol_state = dict(bot.form_symbol_state)
        _flush_form_symbol_memory_if_due(bot, force=False)
        return dict(bot.form_symbol_state)

    return {
        "form_symbol_id": str(symbol_id),
        "form_symbol_key": str(family_key),
        "form_symbol_family_key": str(family_key),
        "form_symbol_variant_key": str(form_key),
        "form_symbol_scope": str(form_symbol_scope),
        "form_symbol_abstraction_level": int(form_symbol_abstraction_level),
        "form_symbol_resolution_quality": float(form_resolution_quality),
        "form_symbol_detail_pressure": float(form_detail_pressure),
        "form_symbol_object_distance": float(symbolic_object_distance),
        "form_symbol_containment": float(symbolic_containment),
        "form_symbol_field_decoupling": float(symbolic_field_decoupling),
        "form_symbol_development_quality": float(learned_development_quality),
        "form_symbol_action_affinity": float(learned_action_affinity),
        "form_symbol_observation_affinity": float(learned_observation_affinity),
        "form_symbol_reframe_potential": float(learned_reframe_potential),
        "form_symbol_learning_trust": float(learned_learning_trust),
        "form_symbol_action_trust": float(learned_action_trust),
        "form_symbol_caution_trust": float(learned_caution_trust),
        "form_symbol_contact_maturity": float(learned_contact_maturity),
        "form_symbol_contact_utility": float(learned_contact_utility),
        "form_symbol_contact_pain_memory": float(learned_contact_pain_memory),
        "form_symbol_contact_carefulness": float(learned_contact_carefulness),
        "form_symbol_contact_burden_evidence": float(learned_contact_burden_evidence),
        "form_symbol_contact_utility_evidence": float(learned_contact_utility_evidence),
        "form_symbol_contact_learning_state": str(learned_contact_state),
        "form_symbol_action_binding": float(learned_action_binding),
        "form_symbol_observation_binding": float(learned_observation_binding),
        "form_symbol_reframe_binding": float(learned_reframe_binding),
        "form_symbol_seen": int(seen),
        "form_symbol_maturity": float(maturity),
        "form_symbol_stability": float(stability),
        "form_symbol_resonance": float(resonance),
        "form_symbol_load_reduction": float(load_reduction),
        "form_symbol_zoom_need": float(zoom_need),
        "form_symbol_split_pressure": float(split_pressure),
        "form_symbol_merge_pressure": float(merge_pressure),
        "form_symbol_bearing": float(bearing),
        "form_symbol_fragility": float(fragility),
        "form_symbol_relevance": float(relevance),
        "form_symbol_novelty": float(novelty),
        "form_symbol_distance": float(distance),
        "uncertain_form_family_state": str(uncertain_form_family_state),
        "uncertain_form_exposure": float(uncertain_form_exposure),
        "uncertainty_familiarity": float(uncertainty_familiarity),
        "variant_similarity": float(variant_similarity),
        "variant_spread": float(variant_spread),
        "variant_learning_pressure": float(variant_learning_pressure),
        "variant_bearing_memory": float(variant_bearing_memory),
        "form_symbol_semantic_density": float(semantic_density),
        "form_symbol_semantic_compression": float(semantic_compression),
        "form_symbol_semantic_coherence": float(semantic_coherence),
        "form_symbol_semantic_learning_need": float(semantic_learning_need),
        "form_symbol_semantic_action_nearness": float(semantic_action_nearness),
        "form_symbol_semantic_primary_layer": str(semantic_primary_layer),
        "form_symbol_semantic_layer_count": int(semantic_layer_count),
        "form_symbol_semantic_packet_state": str(semantic_packet_state),
        "form_symbol_semantic_profile": str(semantic_profile),
        "form_symbol_compound_id": str(compound_id),
        "form_symbol_compound_key": str(compound_key),
        "form_symbol_compound_scope": str(compound_scope),
        "form_symbol_compound_seen": int(compound_seen),
        "form_symbol_compound_maturity": float(compound_maturity),
        "form_symbol_compound_stability": float(compound_stability),
        "form_symbol_compound_resonance": float(compound_resonance),
        "form_symbol_compound_bearing": float(compound_bearing),
        "form_symbol_compound_load_reduction": float(compound_load_reduction),
        "form_symbol_compound_novelty": float(compound_novelty),
        "form_symbol_compound_development_quality": float(compound_development_quality),
        "form_symbol_compound_action_affinity": float(compound_action_affinity),
        "form_symbol_compound_observation_affinity": float(compound_observation_affinity),
        "form_symbol_compound_reframe_potential": float(compound_reframe_potential),
        "form_symbol_compound_learning_trust": float(compound_learning_trust),
        "form_symbol_compound_action_trust": float(compound_action_trust),
        "form_symbol_compound_caution_trust": float(compound_caution_trust),
        "form_symbol_compound_contact_maturity": float(compound_contact_maturity),
        "form_symbol_compound_contact_utility": float(compound_contact_utility),
        "form_symbol_compound_contact_pain_memory": float(compound_contact_pain_memory),
        "form_symbol_compound_contact_carefulness": float(compound_contact_carefulness),
        "form_symbol_compound_contact_burden_evidence": float(compound_contact_burden_evidence),
        "form_symbol_compound_contact_utility_evidence": float(compound_contact_utility_evidence),
        "form_symbol_compound_contact_learning_state": str(compound_contact_state),
    }



def update_form_symbol_development_from_outcome(bot, outcome_reason, position=None, outcome_decomposition=None):

    if bot is None or not bool(getattr(Config, "MCM_FORM_SYMBOL_MEMORY_ENABLED", True)):
        return {}

    _ensure_form_symbol_memory_loaded(bot)

    form_state = _extract_outcome_form_symbol_state_impl(bot, position=position)
    symbol_id = str(form_state.get("form_symbol_id", "") or "").strip()
    if not symbol_id or symbol_id == "-":
        return {}

    outcome = dict(outcome_decomposition or {})
    reason = str(outcome_reason or outcome.get("reason", "") or "").strip().lower()

    def _b01(value, default=0.0):
        try:
            return max(0.0, min(1.0, float(value)))
        except Exception:
            return float(default)

    def _bs(value, default=0.0):
        try:
            return max(-1.0, min(1.0, float(value)))
        except Exception:
            return float(default)

    structure_quality = _b01(form_state.get("form_symbol_bearing", 0.0))
    meta = dict((position or {}).get("meta", {}) or {}) if isinstance(position, dict) else {}
    bearing_context = dict(meta.get("bearing_context", {}) or {}) if isinstance(meta.get("bearing_context", {}), dict) else {}
    if bearing_context:
        structure_quality = _b01(bearing_context.get("structure_quality", structure_quality))
    contact_state = dict(meta.get("active_mcm_contact_state", meta.get("active_mcm_contact", {})) or {}) if isinstance(meta, dict) else {}
    meta_regulation = dict(meta.get("meta_regulation_state", {}) or {}) if isinstance(meta.get("meta_regulation_state", {}), dict) else {}
    if not contact_state and meta_regulation:
        contact_state = dict(meta_regulation.get("active_mcm_contact", {}) or {})
    contact_action_maturity = _b01(contact_state.get("contact_action_maturity", 0.0))
    contact_carrying_quality = _b01(contact_state.get("contact_carrying_quality", 0.0))
    contact_reality_check = _b01(contact_state.get("contact_reality_check", 0.0))
    contact_temporal_bearing = _b01(contact_state.get("contact_temporal_bearing", meta_regulation.get("contact_temporal_bearing", 0.0)))
    contact_overcoupling_risk = _b01(contact_state.get("contact_overcoupling_risk", 0.0))
    contact_learning_need = _b01(contact_state.get("contact_learning_need", 0.0))
    contact_context_reframe_need = _b01(contact_state.get("contact_context_reframe_need", 0.0))
    contact_regime_mismatch = _b01(contact_state.get("contact_regime_mismatch", 0.0))
    area_bearing_quality = _b01(meta_regulation.get("area_bearing_quality", meta.get("area_bearing_quality", 0.0)) if isinstance(meta, dict) else 0.0)
    area_spacetime_fit = _b01(meta_regulation.get("area_spacetime_fit", meta.get("area_spacetime_fit", 0.0)) if isinstance(meta, dict) else 0.0)
    position_intervention_state = dict(meta.get("position_intervention_state", {}) or {}) if isinstance(meta, dict) else {}
    position_experience_state = dict(position_intervention_state.get("position_experience_state", {}) or {})
    position_experience_label = str(
        position_intervention_state.get(
            "position_experience_label",
            position_experience_state.get("position_experience_label", "-"),
        )
        or "-"
    ).strip().lower()
    position_inconsistency_stress = _b01(position_intervention_state.get("position_inconsistency_stress", position_experience_state.get("position_inconsistency_stress", 0.0)))
    position_mcm_field_strain = _b01(position_intervention_state.get("position_mcm_field_strain", position_experience_state.get("position_mcm_field_strain", 0.0)))
    position_self_trust_gap = _b01(position_intervention_state.get("position_self_trust_gap", position_experience_state.get("position_self_trust_gap", 0.0)))
    position_cortisol_load = _b01(position_intervention_state.get("position_cortisol_load", position_experience_state.get("position_cortisol_load", 0.0)))
    position_noradrenaline_arousal = _b01(position_intervention_state.get("position_noradrenaline_arousal", position_experience_state.get("position_noradrenaline_arousal", 0.0)))
    position_protective_distance = _b01(position_intervention_state.get("position_protective_distance", position_experience_state.get("position_protective_distance", 0.0)))
    position_held_risk_discomfort = _b01(position_intervention_state.get("position_held_risk_discomfort", position_experience_state.get("position_held_risk_discomfort", 0.0)))
    position_process_quality = _b01(position_intervention_state.get("position_process_quality", position_experience_state.get("position_process_quality", 0.50)), default=0.50)

    position_consequence_burden = _b01(
        (position_held_risk_discomfort * 0.26)
        + (position_inconsistency_stress * 0.22)
        + (position_cortisol_load * 0.18)
        + (position_self_trust_gap * 0.14)
        + (position_mcm_field_strain * 0.10)
        + (position_noradrenaline_arousal * 0.06)
        + ((1.0 - position_process_quality) * 0.04)
    )
    if position_experience_label == "protective_stress_contact":
        position_consequence_burden = _b01(position_consequence_burden + 0.10)
    elif position_experience_label == "self_trust_gap_contact":
        position_consequence_burden = _b01(position_consequence_burden + 0.06)
    elif position_experience_label == "unearned_relief_watch":
        position_consequence_burden = _b01(position_consequence_burden + 0.05)

    position_constructive_bearing = _b01(
        (position_process_quality * 0.34)
        + ((1.0 - position_inconsistency_stress) * 0.16)
        + ((1.0 - position_held_risk_discomfort) * 0.14)
        + ((1.0 - position_mcm_field_strain) * 0.12)
        + (max(0.0, 1.0 - position_self_trust_gap) * 0.10)
        + (contact_action_maturity * 0.08)
        + (contact_reality_check * 0.06)
    )
    if position_experience_label == "carried_position_contact":
        position_constructive_bearing = _b01(position_constructive_bearing + 0.10)

    emotional_decoupling = _b01(meta.get("emotional_decoupling", 0.0))
    if not emotional_decoupling and isinstance(meta.get("meta_regulation_state", {}), dict):
        emotional_decoupling = _b01((meta.get("meta_regulation_state", {}) or {}).get("emotional_decoupling", 0.0))

    process_quality = _b01(
        (
            _b01(outcome.get("perception_quality", 0.50)) * 0.18
            + _b01(outcome.get("felt_quality", 0.50)) * 0.16
            + _b01(outcome.get("thought_quality", 0.50)) * 0.18
            + _b01(outcome.get("plan_quality", 0.50)) * 0.22
            + _b01(outcome.get("execution_quality", 0.50)) * 0.14
            + _b01(outcome.get("risk_fit_quality", 0.50)) * 0.12
        ),
        default=0.50,
    )
    if position_intervention_state:
        process_quality = _b01(
            (process_quality * 0.74)
            + (position_process_quality * 0.20)
            + (position_constructive_bearing * 0.08)
            - (position_consequence_burden * 0.10),
            default=process_quality,
        )
    context_quality = _b01(outcome.get("context_quality", 0.0))
    risk_width_pressure = _b01(outcome.get("risk_width_pressure", 0.0))
    structural_support = _b01((structure_quality * 0.64) + (context_quality * 0.36))
    constructive_signal = _b01((process_quality * 0.62) + (structural_support * 0.38))
    outcome_contact_reward = 0.40
    result_bias = 0.0
    if reason == "tp_hit":
        result_bias = 0.18
        outcome_contact_reward = 0.72
    elif reason == "sl_hit":
        result_bias = -0.22 - (max(0.0, 0.56 - structure_quality) * 0.22) - (risk_width_pressure * 0.12)
        outcome_contact_reward = 0.18
    elif reason in ("cancel", "timeout"):
        result_bias = -0.08
        outcome_contact_reward = 0.34
    elif reason in ("reward_too_small", "rr_too_low", "sl_distance_too_high"):
        result_bias = -0.12
        outcome_contact_reward = 0.28

    development_sample = _bs(((constructive_signal - 0.50) * 1.40) + result_bias)
    transitional_contact_band = _b01(1.0 - min(1.0, abs(structure_quality - 0.54) / 0.24))
    transitional_contact_maturation = _b01(
        (transitional_contact_band * 0.18)
        + (contact_temporal_bearing * 0.18)
        + (area_bearing_quality * 0.16)
        + (area_spacetime_fit * 0.12)
        + (contact_reality_check * 0.16)
        + (position_constructive_bearing * 0.16)
        - (position_consequence_burden * 0.14)
        - (contact_overcoupling_risk * 0.08)
    )
    transitional_contact_maturation = max(0.0, transitional_contact_maturation - 0.30)
    contact_utility_sample = _b01(
        (process_quality * 0.26)
        + (structural_support * 0.20)
        + (outcome_contact_reward * 0.20)
        + (contact_carrying_quality * 0.12)
        + (contact_action_maturity * 0.10)
        + (contact_reality_check * 0.08)
        + (emotional_decoupling * 0.04)
        + (position_constructive_bearing * 0.08)
        + (transitional_contact_maturation * 0.08)
        - (contact_overcoupling_risk * 0.12)
        - (risk_width_pressure * 0.08)
        - (position_consequence_burden * 0.10)
    )
    contact_pain_sample = _b01(
        ((0.52 if reason == "sl_hit" else 0.08) * 0.34)
        + (risk_width_pressure * 0.18)
        + (contact_overcoupling_risk * 0.16)
        + (max(0.0, 0.48 - process_quality) * 0.16)
        + (max(0.0, 0.50 - structural_support) * 0.14)
        + (contact_regime_mismatch * 0.08)
        + (position_consequence_burden * 0.18)
        - (contact_reality_check * 0.08)
        - (emotional_decoupling * 0.06)
        - (position_constructive_bearing * 0.05)
    )
    position_consequence_residual_for_care = _b01(
        position_consequence_burden * (1.0 - min(0.72, contact_pain_sample * 1.35))
    )
    contact_maturity_sample = _b01(
        (contact_utility_sample * 0.36)
        + (contact_action_maturity * 0.18)
        + (contact_reality_check * 0.14)
        + (structural_support * 0.12)
        + (process_quality * 0.10)
        + (emotional_decoupling * 0.10)
        + (position_constructive_bearing * 0.08)
        + (transitional_contact_maturation * 0.10)
        - (contact_pain_sample * 0.20)
        - (position_consequence_burden * 0.06)
    )
    contact_carefulness_sample = _b01(
        (contact_pain_sample * 0.38)
        + (contact_learning_need * 0.20)
        + (contact_context_reframe_need * 0.16)
        + (contact_regime_mismatch * 0.12)
        + (max(0.0, 0.46 - contact_maturity_sample) * 0.14)
        + (position_consequence_residual_for_care * 0.16)
        + (position_protective_distance * 0.08)
    )
    position_consequence_residual_for_memory = _b01(
        position_consequence_burden
        * (1.0 - min(0.78, (contact_pain_sample * 0.95) + (contact_carefulness_sample * 0.65)))
    )
    contact_learning_pressures = {
        "protective_reorganization_contact": _b01(
            (position_consequence_burden * 0.34)
            + ((1.0 - contact_maturity_sample) * 0.16)
            + (contact_context_reframe_need * 0.10)
        ),
        "burdened_contact": _b01(
            (contact_pain_sample * 0.34)
            + ((1.0 - contact_maturity_sample) * 0.14)
            + (max(0.0, -development_sample) * 0.12)
        ),
        "careful_contact": _b01(
            (contact_carefulness_sample * 0.28)
            + (contact_pain_sample * 0.18)
            + ((1.0 - contact_maturity_sample) * 0.10)
            + (0.12 if position_experience_label == "unearned_relief_watch" else 0.0)
        ),
        "constructive_contact": _b01(
            (contact_utility_sample * 0.32)
            + (contact_maturity_sample * 0.24)
            + (position_constructive_bearing * 0.10)
            - (contact_pain_sample * 0.10)
        ),
        "learning_contact": _b01(
            (contact_learning_need * 0.26)
            + (contact_context_reframe_need * 0.24)
            + (observation_sample if "observation_sample" in locals() else 0.0) * 0.06
        ),
        "maturing_contact": _b01(
            (contact_maturity_sample * 0.30)
            + (contact_reality_check * 0.10)
            + (transitional_contact_maturation * 0.08)
        ),
        "unformed_contact": _b01(
            (1.0 - max(contact_pain_sample, contact_maturity_sample, contact_utility_sample, contact_learning_need)) * 0.22
        ),
    }
    contact_learning_state = max(contact_learning_pressures, key=contact_learning_pressures.get)
    observation_sample = _b01(
        max(0.0, -development_sample) * 0.54
        + max(0.0, 0.52 - structural_support) * 0.34
        + max(0.0, 0.46 - process_quality) * 0.20
        + (risk_width_pressure * 0.12 if reason == "sl_hit" else 0.0)
        + (contact_carefulness_sample * 0.10)
    )
    reframe_sample = _b01(
        observation_sample * 0.46
        + _b01(form_state.get("form_symbol_novelty", 0.0)) * 0.14
        + _b01(form_state.get("form_symbol_compound_novelty", 0.0)) * 0.12
        + max(0.0, 0.50 - structure_quality) * 0.28
        + (contact_context_reframe_need * 0.08)
    )

    learning_context = {
        "development_sample": float(development_sample),
        "contact_maturity_sample": float(contact_maturity_sample),
        "contact_utility_sample": float(contact_utility_sample),
        "contact_pain_sample": float(contact_pain_sample),
        "contact_carefulness_sample": float(contact_carefulness_sample),
        "risk_width_pressure": float(risk_width_pressure),
        "reason": str(reason or "-"),
        "position_consequence_residual_for_memory": float(position_consequence_residual_for_memory),
        "structural_support": float(structural_support),
        "position_constructive_bearing": float(position_constructive_bearing),
        "position_consequence_burden": float(position_consequence_burden),
        "observation_sample": float(observation_sample),
        "reframe_sample": float(reframe_sample),
        "contact_learning_state": str(contact_learning_state),
        "contact_learning_pressures": dict(contact_learning_pressures),
        "timestamp": getattr(bot, "current_timestamp", None),
    }

    def _learn_item(item, weight=1.0):
        return _learn_form_symbol_development_item_impl(item, learning_context, weight=weight)

    symbol_space = getattr(bot, "form_symbol_space", {})
    if not isinstance(symbol_space, dict):
        symbol_space = {}
    symbol_item = _learn_item(dict(symbol_space.get(symbol_id, {}) or {}), weight=1.0)
    symbol_space[str(symbol_id)] = dict(symbol_item)
    bot.form_symbol_space = symbol_space

    compound_id = str(form_state.get("form_symbol_compound_id", "") or "").strip()
    compound_item = {}
    if compound_id and compound_id != "-":
        compound_space = getattr(bot, "form_symbol_compound_space", {})
        if not isinstance(compound_space, dict):
            compound_space = {}
        compound_item = _learn_item(dict(compound_space.get(compound_id, {}) or {}), weight=0.86)
        compound_space[str(compound_id)] = dict(compound_item)
        bot.form_symbol_compound_space = compound_space

    bot._form_symbol_memory_dirty = True
    bot._form_symbol_memory_updates = int(getattr(bot, "_form_symbol_memory_updates", 0) or 0) + 1
    _flush_form_symbol_memory_if_due(bot, force=False)

    return {
        "symbol_id": str(symbol_id),
        "compound_id": str(compound_id or "-"),
        "development_sample": float(development_sample),
        "process_quality": float(process_quality),
        "structural_support": float(structural_support),
        "risk_width_pressure": float(risk_width_pressure),
        "symbol_development_quality": float(symbol_item.get("development_quality", 0.0) or 0.0),
        "symbol_action_affinity": float(symbol_item.get("action_affinity", 0.50) or 0.50),
        "symbol_observation_affinity": float(symbol_item.get("observation_affinity", 0.0) or 0.0),
        "symbol_reframe_potential": float(symbol_item.get("context_reframe_potential", 0.0) or 0.0),
        "symbol_contact_maturity": float(symbol_item.get("contact_maturity", 0.0) or 0.0),
        "symbol_contact_utility": float(symbol_item.get("contact_utility", 0.0) or 0.0),
        "symbol_contact_pain_memory": float(symbol_item.get("contact_pain_memory", 0.0) or 0.0),
        "symbol_contact_carefulness": float(symbol_item.get("contact_carefulness", 0.0) or 0.0),
        "symbol_contact_burden_evidence": float(symbol_item.get("contact_burden_evidence", 0.0) or 0.0),
        "symbol_contact_utility_evidence": float(symbol_item.get("contact_utility_evidence", 0.0) or 0.0),
        "symbol_contact_learning_state": str(symbol_item.get("contact_learning_state", contact_learning_state) or contact_learning_state),
        "contact_maturity_sample": float(contact_maturity_sample),
        "contact_utility_sample": float(contact_utility_sample),
        "contact_pain_sample": float(contact_pain_sample),
        "contact_carefulness_sample": float(contact_carefulness_sample),
        "contact_learning_state": str(contact_learning_state),
        "position_consequence_burden": float(position_consequence_burden),
        "position_consequence_residual_for_care": float(position_consequence_residual_for_care),
        "position_consequence_residual_for_memory": float(position_consequence_residual_for_memory),
        "position_constructive_bearing": float(position_constructive_bearing),
        "transitional_contact_band": float(transitional_contact_band),
        "transitional_contact_maturation": float(transitional_contact_maturation),
        "position_feedback_label": str(position_experience_label or "-"),
        "position_process_quality": float(position_process_quality),
        "position_held_risk_discomfort": float(position_held_risk_discomfort),
        "position_cortisol_load": float(position_cortisol_load),
        "position_noradrenaline_arousal": float(position_noradrenaline_arousal),
        "compound_development_quality": float(compound_item.get("development_quality", 0.0) or 0.0) if compound_item else 0.0,
        "compound_contact_maturity": float(compound_item.get("contact_maturity", 0.0) or 0.0) if compound_item else 0.0,
        "compound_contact_burden_evidence": float(compound_item.get("contact_burden_evidence", 0.0) or 0.0) if compound_item else 0.0,
        "compound_contact_utility_evidence": float(compound_item.get("contact_utility_evidence", 0.0) or 0.0) if compound_item else 0.0,
    }


__all__ = ["build_form_symbol_state", "update_form_symbol_development_from_outcome"]
