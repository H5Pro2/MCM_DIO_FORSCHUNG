"""MCM possibility field.

This layer keeps several possible continuations open without turning them into
hard trading rules. It translates visual form, MCM field reaction, time-depth
and Doppler afterimage into a small variant cloud that can feed reflection,
trust, caution and observation pressure.
"""

import hashlib

from config import Config


def _clip(value, lo=0.0, hi=1.0):
    try:
        value = float(value)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return max(float(lo), min(float(hi), float(value)))


def _signed(value):
    return _clip(value, -1.0, 1.0)


def _state(value, default="-"):
    text = str(value or default).replace("\n", " ").replace(";", "|").strip()
    return text or str(default)


def _variant_token(parts):
    basis = "|".join(_state(part) for part in parts)
    return "pv_" + hashlib.sha1(basis.encode("utf-8", errors="ignore")).hexdigest()[:10]


def _hypothesis_learning_enabled():
    return bool(getattr(Config, "MCM_HYPOTHESIS_LEARNING_ENABLED", False))


def _empty_possibility_field():
    return {
        "possibility_field_state": "possibility_disabled",
        "possibility_observer_state": "observer_disabled",
        "possibility_variants": [],
        "possibility_variant_count": 0,
        "possibility_dominant_variant_id": "-",
        "possibility_dominant_kind": "-",
        "possibility_dominant_direction": "-",
        "possibility_dominant_support": 0.0,
        "possibility_second_support": 0.0,
        "possibility_spread": 0.0,
        "possibility_openness": 0.0,
        "possibility_collapse_pressure": 0.0,
        "possibility_reflection_pull": 0.0,
        "possibility_observation_pull": 0.0,
        "possibility_contact_bearing": 0.0,
        "possibility_action_support": 0.0,
        "possibility_doppler_energy": 0.0,
        "possibility_future_variant_pressure": 0.0,
        "possibility_form_mcm_fit": 0.0,
        "possibility_memory_fit": 0.0,
        "possibility_caution": 0.0,
        "possibility_observation_depth": 0.0,
        "possibility_reality_contact": 0.0,
        "possibility_variant_maturity": 0.0,
        "possibility_variant_trust": 0.0,
        "possibility_variant_caution": 0.0,
        "possibility_collapse_reason": "hypothesis_disabled",
        "possibility_collapse_reason_pressures": {},
        "possibility_state_pressures": {},
        "possibility_observer_state_pressures": {},
        "possibility_collapse_reversibility": 0.0,
        "possibility_memory_return": 0.0,
    }


def _variant(kind, *, direction, visual_fit, mcm_resonance, temporal_fit, doppler_fit, memory_fit, caution, source):
    visual_fit = _clip(visual_fit)
    mcm_resonance = _clip(mcm_resonance)
    temporal_fit = _clip(temporal_fit)
    doppler_fit = _clip(doppler_fit)
    memory_fit = _clip(memory_fit)
    caution = _clip(caution)
    support = _clip(
        (visual_fit * 0.24)
        + (mcm_resonance * 0.24)
        + (temporal_fit * 0.18)
        + (doppler_fit * 0.16)
        + (memory_fit * 0.14)
        - (caution * 0.18)
    )
    uncertainty = _clip(
        (abs(visual_fit - mcm_resonance) * 0.28)
        + (abs(temporal_fit - doppler_fit) * 0.22)
        + (caution * 0.24)
        + (max(0.0, 0.36 - memory_fit) * 0.16)
        + (max(0.0, 0.34 - visual_fit) * 0.10)
    )
    return {
        "variant_id": _variant_token((kind, direction, source, round(visual_fit, 2), round(mcm_resonance, 2), round(temporal_fit, 2), round(doppler_fit, 2))),
        "variant_kind": str(kind),
        "variant_direction": str(direction),
        "variant_source": str(source),
        "variant_visual_fit": float(visual_fit),
        "variant_mcm_resonance": float(mcm_resonance),
        "variant_temporal_fit": float(temporal_fit),
        "variant_doppler_fit": float(doppler_fit),
        "variant_memory_fit": float(memory_fit),
        "variant_caution": float(caution),
        "variant_support": float(support),
        "variant_uncertainty": float(uncertainty),
    }


def build_mcm_possibility_field(
    *,
    temporal_perception_state=None,
    form_symbol_state=None,
    meta_regulation_state=None,
    perception_state=None,
    thought_state=None,
    review_feedback_state=None,
    strategic_window_state=None,
    active_mcm_contact_state=None,
):
    if not _hypothesis_learning_enabled():
        return _empty_possibility_field()

    temporal = dict(temporal_perception_state or {})
    form = dict(form_symbol_state or {})
    meta = dict(meta_regulation_state or {})
    perception = dict(perception_state or {})
    thought = dict(thought_state or {})
    review = dict(review_feedback_state or {})
    strategic = dict(strategic_window_state or {})
    contact = dict(active_mcm_contact_state or {})

    visual_clarity = _clip(meta.get("visual_clarity", perception.get("visual_clarity", 0.0)))
    visual_stability = _clip(meta.get("visual_object_stability", perception.get("visual_object_stability", 0.0)))
    visual_fit = _clip(
        (visual_clarity * 0.26)
        + (visual_stability * 0.22)
        + (_clip(form.get("form_symbol_stability", 0.0)) * 0.16)
        + (_clip(form.get("form_symbol_semantic_coherence", 0.0)) * 0.16)
        + (_clip(meta.get("structure_quality", 0.0)) * 0.12)
        + (_clip(meta.get("context_confidence", 0.0)) * 0.08)
    )
    visual_fragility = _clip(
        (_clip(form.get("form_symbol_fragility", form.get("visual_shape_fragility", 0.0))) * 0.24)
        + (max(0.0, 0.42 - visual_clarity) * 0.24)
        + (_clip(meta.get("structure_action_uncertainty", 0.0)) * 0.20)
        + (_clip(meta.get("visual_action_uncertainty", 0.0)) * 0.18)
    )

    inner_alignment = _clip(meta.get("inner_outer_alignment", 0.0))
    field_support = _clip(meta.get("field_bearing_support", meta.get("field_action_support", 0.0)))
    carrying = _clip(meta.get("contact_carrying_quality", 0.0))
    overcoupling = _clip(meta.get("contact_overcoupling_risk", meta.get("field_overcoupling", 0.0)))
    mcm_resonance = _clip((inner_alignment * 0.28) + (field_support * 0.22) + (carrying * 0.22) + (_clip(meta.get("field_perception_clarity", 0.0)) * 0.16) - (overcoupling * 0.14))

    memory_bearing = _clip(temporal.get("spacetime_memory_bearing", 0.0))
    future_bearing = _clip(temporal.get("spacetime_future_bearing", 0.0))
    context_depth = _clip(temporal.get("temporal_context_depth", 0.0))
    afterimage = _clip(temporal.get("temporal_afterimage", 0.0))
    temporal_fit = _clip((memory_bearing * 0.26) + (future_bearing * 0.24) + (context_depth * 0.22) + (_clip(temporal.get("temporal_self_location", 0.0)) * 0.18) - (_clip(temporal.get("spacetime_unlocated_pressure", 0.0)) * 0.14))

    doppler_bias = _signed(temporal.get("afterimage_doppler_bias", 0.0))
    approach = _clip(temporal.get("motion_approach_pressure", 0.0))
    recession = _clip(temporal.get("motion_recession_pressure", 0.0))
    frequency_shift = _clip(temporal.get("contact_frequency_shift", 0.0))
    future_variant_pressure = _clip(temporal.get("future_variant_pressure", 0.0))
    doppler_energy = _clip((future_variant_pressure * 0.30) + (frequency_shift * 0.24) + (approach * 0.18) + (recession * 0.10) + (abs(doppler_bias) * 0.18))

    thought_recall = _clip(thought.get("thought_recall_potential", meta.get("thought_recall_potential", 0.0)))
    thought_maturity = _clip(thought.get("thought_maturity", meta.get("thought_maturity", 0.0)))
    hypothesis_trust = _clip(meta.get("hypothesis_trust", review.get("hypothesis_trust_score", 0.0)))
    form_trust = _clip(form.get("form_symbol_action_trust", meta.get("form_symbol_action_trust", 0.0)))
    family_trust = _clip(meta.get("form_mcm_family_trust", 0.0))
    memory_fit = _clip((thought_recall * 0.20) + (thought_maturity * 0.20) + (hypothesis_trust * 0.22) + (form_trust * 0.18) + (family_trust * 0.20))

    area_bearing = _clip(strategic.get("area_bearing_quality", meta.get("area_bearing_quality", 0.0)))
    contact_future = _clip(contact.get("contact_future_watch", meta.get("contact_future_watch", 0.0)))
    contact_release = _clip(contact.get("contact_release_readiness", meta.get("contact_release_readiness", 0.0)))
    contact_reality_check = _clip(contact.get("contact_reality_check", meta.get("contact_reality_check", 0.0)))
    base_caution = _clip(
        (visual_fragility * 0.22)
        + (_clip(meta.get("hypothesis_caution", 0.0)) * 0.22)
        + (_clip(meta.get("open_hypothesis_reality_check_need", 0.0)) * 0.20)
        + (overcoupling * 0.18)
        + (contact_reality_check * 0.12)
        - (contact_release * 0.08)
    )

    long_bias = _clip(max(0.0, doppler_bias) + (approach * 0.18) + (_clip(meta.get("long_score", 0.0)) * 0.12))
    short_bias = _clip(max(0.0, -doppler_bias) + (approach * 0.18) + (_clip(meta.get("short_score", 0.0)) * 0.12))
    hold_bias = _clip(base_caution + (_clip(meta.get("field_observation_need", 0.0)) * 0.18) + (frequency_shift * 0.10))
    replan_bias = _clip(_clip(meta.get("open_hypothesis_learning_charge", 0.0)) + (_clip(meta.get("field_replan_pressure", 0.0)) * 0.18) + (future_variant_pressure * 0.12))

    variants = [
        _variant(
            "directional_continuation",
            direction="LONG",
            visual_fit=visual_fit,
            mcm_resonance=mcm_resonance,
            temporal_fit=temporal_fit,
            doppler_fit=long_bias,
            memory_fit=memory_fit,
            caution=base_caution,
            source="doppler_form_mcm",
        ),
        _variant(
            "directional_continuation",
            direction="SHORT",
            visual_fit=visual_fit,
            mcm_resonance=mcm_resonance,
            temporal_fit=temporal_fit,
            doppler_fit=short_bias,
            memory_fit=memory_fit,
            caution=base_caution,
            source="doppler_form_mcm",
        ),
        _variant(
            "observational_hold",
            direction="WAIT",
            visual_fit=max(visual_fit, visual_fragility),
            mcm_resonance=max(mcm_resonance, base_caution),
            temporal_fit=max(afterimage, temporal_fit * 0.70),
            doppler_fit=hold_bias,
            memory_fit=max(memory_fit, memory_bearing),
            caution=max(base_caution, hold_bias),
            source="field_distance",
        ),
        _variant(
            "reorganization_replay",
            direction="REPLAN",
            visual_fit=max(visual_fit * 0.72, visual_fragility),
            mcm_resonance=max(mcm_resonance * 0.74, replan_bias),
            temporal_fit=max(future_bearing, afterimage, context_depth * 0.74),
            doppler_fit=max(future_variant_pressure, frequency_shift),
            memory_fit=max(memory_fit, family_trust),
            caution=max(base_caution, replan_bias),
            source="unclosed_variant",
        ),
    ]

    ranked = sorted(variants, key=lambda item: float(item.get("variant_support", 0.0)), reverse=True)
    dominant = dict(ranked[0] if ranked else {})
    second = dict(ranked[1] if len(ranked) > 1 else {})
    dominant_support = _clip(dominant.get("variant_support", 0.0))
    second_support = _clip(second.get("variant_support", 0.0))
    spread = _clip(dominant_support - second_support)
    openness = _clip(
        (sum(float(item.get("variant_uncertainty", 0.0)) for item in ranked) / float(max(1, len(ranked))) * 0.42)
        + ((1.0 - spread) * 0.30)
        + (future_variant_pressure * 0.16)
        + (frequency_shift * 0.12)
    )
    collapse_pressure = _clip(
        (spread * 0.34)
        + (dominant_support * 0.24)
        + (_clip(dominant.get("variant_memory_fit", 0.0)) * 0.16)
        + (_clip(dominant.get("variant_mcm_resonance", 0.0)) * 0.14)
        - (openness * 0.18)
    )
    reflection_pull = _clip((openness * 0.28) + (base_caution * 0.22) + (future_variant_pressure * 0.18) + (visual_fragility * 0.16) + (max(0.0, 0.34 - memory_fit) * 0.12))
    action_support = _clip((collapse_pressure * 0.26) + (dominant_support * 0.26) + (memory_fit * 0.16) + (mcm_resonance * 0.14) + (area_bearing * 0.10) - (reflection_pull * 0.18))
    possibility_contact_bearing = float(action_support)
    observation_pull = _clip((openness * 0.32) + (reflection_pull * 0.24) + (base_caution * 0.18) + (frequency_shift * 0.12) - (collapse_pressure * 0.10))
    observation_depth = _clip((openness * 0.34) + (observation_pull * 0.26) + (reflection_pull * 0.18) + (future_variant_pressure * 0.12) + (afterimage * 0.10))
    reality_contact = _clip((visual_fit * 0.26) + (mcm_resonance * 0.24) + (temporal_fit * 0.18) + (area_bearing * 0.14) + (contact_release * 0.10) - (base_caution * 0.12))
    variant_maturity = _clip((reality_contact * 0.30) + (memory_fit * 0.24) + (dominant_support * 0.18) + (collapse_pressure * 0.12) + (observation_depth * 0.08) - (openness * 0.10))
    variant_trust = _clip((variant_maturity * 0.34) + (form_mcm_fit := _clip((visual_fit * 0.34) + (mcm_resonance * 0.34) + (memory_fit * 0.18) - (base_caution * 0.12))) * 0.24 + (memory_fit * 0.18) + (reality_contact * 0.16) - (base_caution * 0.16))
    variant_caution = _clip((base_caution * 0.34) + (openness * 0.22) + (reflection_pull * 0.18) + (max(0.0, 0.42 - reality_contact) * 0.16) - (variant_trust * 0.12))

    collapse_reason_pressures = {
        "reality_contact": _clip((collapse_pressure * 0.24) + (reality_contact * 0.42) + (form_mcm_fit * 0.12)),
        "memory_return": _clip((collapse_pressure * 0.20) + (memory_fit * 0.42) + (memory_return if "memory_return" in locals() else 0.0) * 0.08),
        "doppler_vorhall": _clip((collapse_pressure * 0.18) + (doppler_energy * 0.42) + (future_variant_pressure * 0.12)),
        "reflection_pressure": _clip((collapse_pressure * 0.18) + (reflection_pull * 0.42) + (base_caution * 0.12)),
        "observer_holds_open": _clip((observation_pull * 0.42) + (openness * 0.22)),
        "replan_needed": _clip((reflection_pull * 0.44) + (variant_caution * 0.16)),
        "open_variant": _clip((openness * 0.42) + ((1.0 - collapse_pressure) * 0.20)),
    }
    collapse_reason = max(collapse_reason_pressures, key=collapse_reason_pressures.get)
    collapse_reversibility = _clip((openness * 0.42) + (variant_caution * 0.22) + (reflection_pull * 0.18) + (max(0.0, second_support - dominant_support + 0.20) * 0.18))
    memory_return = _clip((memory_fit * 0.46) + (family_trust * 0.22) + (thought_recall * 0.18) + (memory_bearing * 0.14))

    direction_present = 1.0 if dominant.get("variant_direction") in ("LONG", "SHORT") else 0.0
    possibility_state_pressures = {
        "possibility_soft_collapse": _clip((collapse_pressure * 0.34) + (action_support * 0.28) + (direction_present * 0.12)),
        "possibility_reflection_field": _clip((reflection_pull * 0.42) + (variant_caution * 0.12)),
        "possibility_observation_field": _clip((observation_pull * 0.42) + (observation_depth * 0.18)),
        "possibility_variant_cloud": _clip((openness * 0.44) + (future_variant_pressure * 0.14)),
        "possibility_field_open": _clip((openness * 0.28) + ((1.0 - collapse_pressure) * 0.24)),
    }
    state = max(possibility_state_pressures, key=possibility_state_pressures.get)

    observer_state_pressures = {
        "observer_soft_collapse": _clip(possibility_state_pressures["possibility_soft_collapse"] * 0.52 + action_support * 0.16),
        "observer_reflecting": _clip(reflection_pull * 0.46 + variant_caution * 0.14),
        "observer_holding_variant": _clip(observation_depth * 0.44 + openness * 0.16),
        "observer_reality_contact": _clip(reality_contact * 0.46 + form_mcm_fit * 0.14),
        "observer_open": _clip(openness * 0.34 + (1.0 - max(collapse_pressure, reflection_pull)) * 0.16),
    }
    observer_state = max(observer_state_pressures, key=observer_state_pressures.get)

    return {
        "possibility_field_state": str(state),
        "possibility_observer_state": str(observer_state),
        "possibility_variants": [dict(item) for item in ranked],
        "possibility_variant_count": int(len(ranked)),
        "possibility_dominant_variant_id": str(dominant.get("variant_id", "-") or "-"),
        "possibility_dominant_kind": str(dominant.get("variant_kind", "-") or "-"),
        "possibility_dominant_direction": str(dominant.get("variant_direction", "-") or "-"),
        "possibility_dominant_support": float(dominant_support),
        "possibility_second_support": float(second_support),
        "possibility_spread": float(spread),
        "possibility_openness": float(openness),
        "possibility_collapse_pressure": float(collapse_pressure),
        "possibility_reflection_pull": float(reflection_pull),
        "possibility_observation_pull": float(observation_pull),
        "possibility_contact_bearing": float(possibility_contact_bearing),
        "possibility_action_support": float(action_support),
        "possibility_doppler_energy": float(doppler_energy),
        "possibility_future_variant_pressure": float(future_variant_pressure),
        "possibility_form_mcm_fit": float(form_mcm_fit),
        "possibility_memory_fit": float(memory_fit),
        "possibility_caution": float(base_caution),
        "possibility_observation_depth": float(observation_depth),
        "possibility_reality_contact": float(reality_contact),
        "possibility_variant_maturity": float(variant_maturity),
        "possibility_variant_trust": float(variant_trust),
        "possibility_variant_caution": float(variant_caution),
        "possibility_collapse_reason": str(collapse_reason),
        "possibility_collapse_reason_pressures": dict(collapse_reason_pressures),
        "possibility_state_pressures": dict(possibility_state_pressures),
        "possibility_observer_state_pressures": dict(observer_state_pressures),
        "possibility_collapse_reversibility": float(collapse_reversibility),
        "possibility_memory_return": float(memory_return),
    }


def apply_possibility_field_to_meta(meta_regulation_state=None, possibility_field_state=None):
    meta = dict(meta_regulation_state or {})
    field = dict(possibility_field_state or {})

    if not _hypothesis_learning_enabled():
        neutral = _empty_possibility_field()
        meta["mcm_possibility_field_state"] = dict(neutral)
        meta["possibility_field_state"] = "possibility_disabled"
        meta["possibility_dominant_direction"] = "-"
        meta["possibility_dominant_support"] = 0.0
        meta["possibility_openness"] = 0.0
        meta["possibility_collapse_pressure"] = 0.0
        meta["possibility_reflection_pull"] = 0.0
        meta["possibility_observation_pull"] = 0.0
        meta["possibility_contact_bearing"] = 0.0
        meta["possibility_action_support"] = 0.0
        meta["possibility_form_mcm_fit"] = 0.0
        meta["possibility_observer_state"] = "observer_disabled"
        meta["possibility_observation_depth"] = 0.0
        meta["possibility_reality_contact"] = 0.0
        meta["possibility_variant_maturity"] = 0.0
        meta["possibility_variant_trust"] = 0.0
        meta["possibility_variant_caution"] = 0.0
        meta["possibility_collapse_reason"] = "hypothesis_disabled"
        meta["possibility_collapse_reversibility"] = 0.0
        meta["possibility_memory_return"] = 0.0
        meta["open_hypothesis_reality_check_need"] = 0.0
        meta["open_hypothesis_reality_bearing"] = 0.0
        meta["open_hypothesis_reality_fit"] = 0.0
        meta["open_hypothesis_reality_permission"] = 0.0
        meta["open_hypothesis_action_permission"] = 0.0
        meta["hypothesis_trust"] = 0.0
        meta["hypothesis_caution"] = 0.0
        meta["possibility_direction_mismatch"] = False
        return dict(meta or {})

    contact_bearing = _clip(field.get("possibility_contact_bearing", field.get("possibility_action_support", 0.0)))
    action_support = float(contact_bearing)
    observation_pull = _clip(field.get("possibility_observation_pull", 0.0))
    reflection_pull = _clip(field.get("possibility_reflection_pull", 0.0))
    collapse_pressure = _clip(field.get("possibility_collapse_pressure", 0.0))
    openness = _clip(field.get("possibility_openness", 0.0))
    form_mcm_fit = _clip(field.get("possibility_form_mcm_fit", 0.0))
    caution = _clip(field.get("possibility_caution", 0.0))
    dominant_direction = _state(field.get("possibility_dominant_direction", "-"))

    meta["mcm_possibility_field_state"] = dict(field or {})
    meta["possibility_field_state"] = str(field.get("possibility_field_state", "possibility_field_open") or "possibility_field_open")
    meta["possibility_dominant_direction"] = str(dominant_direction)
    meta["possibility_dominant_support"] = float(field.get("possibility_dominant_support", 0.0) or 0.0)
    meta["possibility_openness"] = float(openness)
    meta["possibility_collapse_pressure"] = float(collapse_pressure)
    meta["possibility_reflection_pull"] = float(reflection_pull)
    meta["possibility_observation_pull"] = float(observation_pull)
    meta["possibility_contact_bearing"] = float(contact_bearing)
    meta["possibility_action_support"] = float(action_support)
    meta["possibility_form_mcm_fit"] = float(form_mcm_fit)
    meta["possibility_observer_state"] = str(field.get("possibility_observer_state", "observer_open") or "observer_open")
    meta["possibility_observation_depth"] = float(field.get("possibility_observation_depth", 0.0) or 0.0)
    meta["possibility_reality_contact"] = float(field.get("possibility_reality_contact", 0.0) or 0.0)
    meta["possibility_variant_maturity"] = float(field.get("possibility_variant_maturity", 0.0) or 0.0)
    meta["possibility_variant_trust"] = float(field.get("possibility_variant_trust", 0.0) or 0.0)
    meta["possibility_variant_caution"] = float(field.get("possibility_variant_caution", 0.0) or 0.0)
    meta["possibility_collapse_reason"] = str(field.get("possibility_collapse_reason", "open_variant") or "open_variant")
    meta["possibility_collapse_reversibility"] = float(field.get("possibility_collapse_reversibility", 0.0) or 0.0)
    meta["possibility_memory_return"] = float(field.get("possibility_memory_return", 0.0) or 0.0)

    meta["field_observation_need"] = _clip(float(meta.get("field_observation_need", 0.0) or 0.0) + (observation_pull * 0.045) + (openness * 0.030))
    meta["field_replan_pressure"] = _clip(float(meta.get("field_replan_pressure", 0.0) or 0.0) + (reflection_pull * 0.045))
    meta["open_hypothesis_reality_check_need"] = _clip(float(meta.get("open_hypothesis_reality_check_need", 0.0) or 0.0) + (reflection_pull * 0.055) + (openness * 0.025))
    open_hypothesis_reality_bearing = _clip(
        float(
            meta.get(
                "open_hypothesis_reality_bearing",
                meta.get("open_hypothesis_reality_fit", meta.get("open_hypothesis_reality_permission", meta.get("open_hypothesis_action_permission", 0.0))),
            )
            or 0.0
        )
        + (contact_bearing * 0.045)
        + (collapse_pressure * 0.025)
        - (caution * 0.035)
    )
    meta["open_hypothesis_reality_bearing"] = float(open_hypothesis_reality_bearing)
    meta["open_hypothesis_reality_fit"] = float(open_hypothesis_reality_bearing)
    meta["open_hypothesis_reality_permission"] = float(open_hypothesis_reality_bearing)
    meta["open_hypothesis_action_permission"] = float(open_hypothesis_reality_bearing)
    meta["hypothesis_trust"] = _clip(float(meta.get("hypothesis_trust", 0.0) or 0.0) + (form_mcm_fit * action_support * 0.035))
    meta["hypothesis_caution"] = _clip(float(meta.get("hypothesis_caution", 0.0) or 0.0) + (caution * 0.035) + (openness * 0.020))

    decision = _state(meta.get("decision", meta.get("proposed_decision", "WAIT"))).upper()
    if decision in ("LONG", "SHORT") and dominant_direction in ("LONG", "SHORT") and dominant_direction != decision:
        meta["open_hypothesis_reality_check_need"] = _clip(float(meta.get("open_hypothesis_reality_check_need", 0.0) or 0.0) + 0.035 + (collapse_pressure * 0.030))
        open_hypothesis_reality_bearing = _clip(
            float(meta.get("open_hypothesis_reality_bearing", meta.get("open_hypothesis_reality_fit", meta.get("open_hypothesis_reality_permission", meta.get("open_hypothesis_action_permission", 0.0)))) or 0.0)
            - 0.035
        )
        meta["open_hypothesis_reality_bearing"] = float(open_hypothesis_reality_bearing)
        meta["open_hypothesis_reality_fit"] = float(open_hypothesis_reality_bearing)
        meta["open_hypothesis_reality_permission"] = float(open_hypothesis_reality_bearing)
        meta["open_hypothesis_action_permission"] = float(open_hypothesis_reality_bearing)
        meta["possibility_direction_mismatch"] = True
    else:
        meta["possibility_direction_mismatch"] = False

    return dict(meta or {})


__all__ = [
    "build_mcm_possibility_field",
    "apply_possibility_field_to_meta",
]
