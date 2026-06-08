"""Multisensory market-area perception.

This layer bundles how DIO perceives one market area through sight, hearing,
time and selective felt contact. It is not an entry signal, not a gate and not
strategy logic.
"""

import hashlib


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


def _profile_state(coherence, attention_need, overcoupling_risk, felt_depth):
    pressures = {
        "coherent_multisensory_area": _clip01((coherence * 0.34) + ((1.0 - overcoupling_risk) * 0.14)),
        "area_needs_selective_contact": _clip01((attention_need * 0.32) + ((1.0 - felt_depth) * 0.14)),
        "area_overcoupling_risk": _clip01((overcoupling_risk * 0.38) + (attention_need * 0.08)),
        "forming_multisensory_area": _clip01((coherence * 0.24) + (felt_depth * 0.10) + (attention_need * 0.06)),
        "background_area_perception": _clip01((1.0 - max(coherence, attention_need, overcoupling_risk, felt_depth)) * 0.24),
    }
    return max(pressures, key=pressures.get)


def _profile_pressures(coherence, attention_need, overcoupling_risk, felt_depth):
    return {
        "coherent_multisensory_area": _clip01((coherence * 0.34) + ((1.0 - overcoupling_risk) * 0.14)),
        "area_needs_selective_contact": _clip01((attention_need * 0.32) + ((1.0 - felt_depth) * 0.14)),
        "area_overcoupling_risk": _clip01((overcoupling_risk * 0.38) + (attention_need * 0.08)),
        "forming_multisensory_area": _clip01((coherence * 0.24) + (felt_depth * 0.10) + (attention_need * 0.06)),
        "background_area_perception": _clip01((1.0 - max(coherence, attention_need, overcoupling_risk, felt_depth)) * 0.24),
    }


def _fit(a, b):
    return _clip01(1.0 - abs(_clip01(a) - _clip01(b)))


def _binding_state(sync, desync):
    pressures = {
        "sensory_desync_area": _clip01(desync * 0.38),
        "bound_multisensory_area": _clip01(sync * 0.38 + (1.0 - desync) * 0.10),
        "forming_sensory_binding": _clip01(sync * 0.24 + (1.0 - abs(sync - desync)) * 0.08),
        "loose_sensory_area": _clip01((1.0 - max(sync, desync)) * 0.28),
    }
    return max(pressures, key=pressures.get)


def _binding_pressures(sync, desync):
    return {
        "sensory_desync_area": _clip01(desync * 0.38),
        "bound_multisensory_area": _clip01(sync * 0.38 + (1.0 - desync) * 0.10),
        "forming_sensory_binding": _clip01(sync * 0.24 + (1.0 - abs(sync - desync)) * 0.08),
        "loose_sensory_area": _clip01((1.0 - max(sync, desync)) * 0.28),
    }


def _area_id(area_mid, visual_label, tone, visual_side):
    raw = f"{area_mid:.5f}|{visual_label}|{tone}|{visual_side}".encode("utf-8", errors="ignore")
    return "ap_" + hashlib.sha1(raw).hexdigest()[:10]


def build_area_perception_profile(
    *,
    candle_state=None,
    visual_cortex_state=None,
    market_hearing_state=None,
    temporal_perception_state=None,
    visual_attention_state=None,
    structure_perception_state=None,
):
    candle = dict(candle_state or {})
    visual = dict(visual_cortex_state or {})
    hearing = dict(market_hearing_state or {})
    temporal = dict(temporal_perception_state or {})
    attention = dict(visual_attention_state or {})
    structure = dict(structure_perception_state or {})

    close_price = _v(candle, "close")
    high_price = _v(candle, "high", close_price)
    low_price = _v(candle, "low", close_price)
    span = max(0.0, high_price - low_price)
    area_mid = close_price if close_price else ((high_price + low_price) / 2.0)

    visual_presence = _clip01(_v(visual, "object_presence"))
    visual_clarity = _clip01(_v(visual, "object_clarity"))
    visual_relation = _clip01(_v(visual, "relation_coherence"))
    visual_readiness = _clip01(_v(visual, "visual_readiness"))
    visual_contact_nearness = _clip01(_v(visual, "visual_contact_nearness"))
    visual_binding = _clip01(_v(visual, "visual_object_binding_quality"))
    visual_rejection = _clip01(_v(visual, "visual_lifecycle_rejection"))
    visual_dissolution = _clip01(_v(visual, "visual_lifecycle_dissolution"))
    visual_side = _s(visual, "visual_object_side", "center_area")
    visual_label = _s(visual, "visual_cortex_label", "unformed_visual_background")

    loudness = _clip01(_v(hearing, "loudness"))
    hearing_compression = _clip01(_v(hearing, "compression"))
    frequency_hz = max(0.0, _v(hearing, "frequency_hz"))
    tone = _s(hearing, "tone", "silent_tone")
    hearing_presence = _clip01((loudness * 0.72) + (min(1.0, frequency_hz / 17000.0) * 0.18) + (hearing_compression * 0.10))

    temporal_coherence = _clip01(_v(temporal, "temporal_coherence"))
    temporal_depth = _clip01(_v(temporal, "time_depth", _v(temporal, "temporal_depth")))
    afterimage_strength = _clip01(_v(temporal, "world_motion_afterimage_strength"))
    afterimage_pressure = _clip01(_v(temporal, "world_motion_afterimage_pressure"))
    future_variant_pressure = _clip01(_v(temporal, "future_variant_pressure"))
    doppler_bias = _clip_signed(_v(temporal, "afterimage_doppler_bias"))
    temporal_presence = _clip01(
        (temporal_coherence * 0.32)
        + (temporal_depth * 0.18)
        + (afterimage_strength * 0.18)
        + (afterimage_pressure * 0.16)
        + (future_variant_pressure * 0.16)
    )

    visual_mcm_contact_weight = _clip01(_v(attention, "visual_mcm_contact_weight"))
    visual_form_contact = _clip01(_v(attention, "visual_form_contact"))
    visual_inspection_pull = _clip01(_v(attention, "visual_inspection_pull"))
    structure_seen = _clip01(_v(structure, "structure_seen"))
    structure_quality = _clip01(_v(structure, "structure_quality"))
    zone_proximity = _clip01(_v(structure, "zone_proximity"))

    area_visual_score = _clip01(
        (visual_presence * 0.22)
        + (visual_clarity * 0.18)
        + (visual_relation * 0.18)
        + (visual_readiness * 0.16)
        + (visual_contact_nearness * 0.14)
        + (visual_binding * 0.12)
    )
    area_hearing_score = _clip01((hearing_presence * 0.62) + ((1.0 - hearing_compression) * 0.18) + (loudness * 0.20))
    area_temporal_score = _clip01((temporal_presence * 0.70) + (max(0.0, 1.0 - abs(doppler_bias)) * 0.12) + (afterimage_strength * 0.18))
    area_felt_depth = _clip01(
        (visual_mcm_contact_weight * 0.30)
        + (visual_form_contact * 0.22)
        + (visual_contact_nearness * 0.18)
        + (zone_proximity * 0.14)
        + (structure_quality * 0.10)
        + (visual_inspection_pull * 0.06)
    )
    visual_hearing_fit = _fit(area_visual_score, area_hearing_score)
    visual_felt_fit = _fit(area_visual_score, area_felt_depth)
    hearing_felt_fit = _fit(area_hearing_score, area_felt_depth)
    temporal_visual_fit = _fit(area_temporal_score, area_visual_score)
    sensory_sync = _clip01(
        (visual_hearing_fit * 0.24)
        + (visual_felt_fit * 0.30)
        + (hearing_felt_fit * 0.18)
        + (temporal_visual_fit * 0.16)
        + (visual_relation * 0.12)
        - (visual_rejection * 0.08)
        - (visual_dissolution * 0.08)
    )
    sensory_desync_pressure = _clip01(
        ((1.0 - visual_hearing_fit) * 0.24)
        + ((1.0 - visual_felt_fit) * 0.30)
        + ((1.0 - hearing_felt_fit) * 0.18)
        + ((1.0 - temporal_visual_fit) * 0.12)
        + (hearing_compression * 0.10)
        + (visual_rejection * 0.08)
        + (visual_dissolution * 0.08)
    )
    multisensory_binding_state = _binding_state(sensory_sync, sensory_desync_pressure)
    multisensory_binding_pressures = _binding_pressures(sensory_sync, sensory_desync_pressure)
    bound_hearing_score = area_hearing_score * _clip01(0.25 + (sensory_sync * 0.75))
    bound_felt_depth = area_felt_depth * _clip01(0.35 + (sensory_sync * 0.65))
    bound_temporal_score = area_temporal_score * _clip01(0.35 + (sensory_sync * 0.65))

    area_multisensory_coherence = _clip01(
        (area_visual_score * 0.32)
        + (bound_hearing_score * 0.18)
        + (bound_temporal_score * 0.22)
        + (bound_felt_depth * 0.18)
        + (structure_seen * 0.10)
        + (sensory_sync * 0.10)
        - (visual_rejection * 0.10)
        - (visual_dissolution * 0.10)
        - (sensory_desync_pressure * 0.18)
    )
    area_attention_need = _clip01(
        (visual_presence * 0.20)
        + (visual_contact_nearness * 0.18)
        + (hearing_presence * 0.10)
        + (afterimage_pressure * 0.14)
        + (future_variant_pressure * 0.12)
        + (sensory_desync_pressure * 0.22)
        + (max(0.0, 0.46 - area_multisensory_coherence) * 0.20)
    )
    area_overcoupling_risk = _clip01(
        (area_felt_depth * 0.24)
        + (hearing_compression * 0.18)
        + (afterimage_pressure * 0.18)
        + (visual_rejection * 0.16)
        + (visual_dissolution * 0.12)
        + (sensory_desync_pressure * 0.24)
        + (max(0.0, area_attention_need - area_multisensory_coherence) * 0.18)
    )
    area_profile_state = _profile_state(
        area_multisensory_coherence,
        area_attention_need,
        area_overcoupling_risk,
        area_felt_depth,
    )
    area_profile_pressures = _profile_pressures(
        area_multisensory_coherence,
        area_attention_need,
        area_overcoupling_risk,
        area_felt_depth,
    )

    return {
        "area_profile_id": _area_id(area_mid, visual_label, tone, visual_side),
        "area_price_low": float(low_price),
        "area_price_high": float(high_price),
        "area_price_mid": float(area_mid),
        "area_price_span": float(span),
        "area_visual_profile": {
            "visual_cortex_label": visual_label,
            "dominant_visual_object": _s(visual, "dominant_visual_object", "background"),
            "visual_object_side": visual_side,
            "visual_lifecycle_label": _s(visual, "visual_lifecycle_label", "background_lifecycle"),
            "visual_relation_label": _s(visual, "visual_relation_label", "visual_background_relation"),
            "visual_score": float(area_visual_score),
            "visual_contact_nearness": float(visual_contact_nearness),
            "visual_object_binding_quality": float(visual_binding),
        },
        "area_hearing_profile": {
            "tone": tone,
            "loudness": float(loudness),
            "frequency_hz": float(frequency_hz),
            "compression": float(hearing_compression),
            "hearing_score": float(area_hearing_score),
            "bound_hearing_score": float(bound_hearing_score),
        },
        "area_temporal_profile": {
            "temporal_score": float(area_temporal_score),
            "bound_temporal_score": float(bound_temporal_score),
            "temporal_coherence": float(temporal_coherence),
            "afterimage_strength": float(afterimage_strength),
            "afterimage_pressure": float(afterimage_pressure),
            "future_variant_pressure": float(future_variant_pressure),
            "afterimage_doppler_bias": float(doppler_bias),
        },
        "area_mcm_contact_profile": {
            "felt_depth": float(area_felt_depth),
            "bound_felt_depth": float(bound_felt_depth),
            "visual_mcm_contact_weight": float(visual_mcm_contact_weight),
            "visual_form_contact": float(visual_form_contact),
            "inspection_pull": float(visual_inspection_pull),
            "structure_quality": float(structure_quality),
        },
        "sensory_sync_state": {
            "visual_hearing_fit": float(visual_hearing_fit),
            "visual_felt_fit": float(visual_felt_fit),
            "hearing_felt_fit": float(hearing_felt_fit),
            "temporal_visual_fit": float(temporal_visual_fit),
            "sensory_sync": float(sensory_sync),
            "sensory_desync_pressure": float(sensory_desync_pressure),
            "multisensory_binding_state": str(multisensory_binding_state),
            "multisensory_binding_pressures": dict(multisensory_binding_pressures),
        },
        "visual_hearing_fit": float(visual_hearing_fit),
        "visual_felt_fit": float(visual_felt_fit),
        "hearing_felt_fit": float(hearing_felt_fit),
        "temporal_visual_fit": float(temporal_visual_fit),
        "sensory_sync": float(sensory_sync),
        "sensory_desync_pressure": float(sensory_desync_pressure),
        "multisensory_binding_state": str(multisensory_binding_state),
        "multisensory_binding_pressures": dict(multisensory_binding_pressures),
        "area_attention_need": float(area_attention_need),
        "area_felt_depth": float(area_felt_depth),
        "area_multisensory_coherence": float(area_multisensory_coherence),
        "area_overcoupling_risk": float(area_overcoupling_risk),
        "area_profile_state": str(area_profile_state),
        "area_profile_pressures": dict(area_profile_pressures),
        "area_profile_role": "perception_only",
    }


__all__ = ["build_area_perception_profile"]
