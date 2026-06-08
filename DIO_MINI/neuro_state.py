"""Passive neurochemical mirror for Mini-DIO.

This layer names the inner condition from existing Mini-DIO signals. It is not
an entry system and it does not modify action scores.
"""

from __future__ import annotations


def _clip(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        value = float(value)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return max(lo, min(hi, value))


def _positive_band(value: float) -> float:
    try:
        value = float(value)
    except Exception:
        value = 0.0
    return _clip((value + 1.0) * 0.5)


def _diagnostic_max(diagnostics: dict, key: str) -> float:
    values = []
    for action in ("WAIT", "LONG", "SHORT"):
        state = dict(diagnostics.get(action, {}) or {})
        values.append(float(state.get(key, 0.0) or 0.0))
    return max(values) if values else 0.0


def build_mini_neuro_state(
    *,
    senses: dict,
    diagnostics: dict,
    temporal_state: dict,
    action: str,
    reward: float,
    outcome_event: str,
) -> dict:
    """Build passive inner-state tones from perception and consequence."""

    sehen = dict(senses.get("sehen", {}) or {})
    fuehlen = dict(senses.get("fuehlen", {}) or {})
    form_stability = _positive_band(sehen.get("form_stability", 0.0))
    coherence = _positive_band(fuehlen.get("mcm_coherence", 0.0))
    tension = _clip(fuehlen.get("mcm_tension", 0.0))
    temporal_trust = _clip(temporal_state.get("mini_temporal_trust_support", 0.0))
    temporal_caution = _clip(temporal_state.get("mini_temporal_caution_support", 0.0))
    afterimage = _clip(temporal_state.get("mini_afterimage", 0.0))
    max_readiness = _clip(max(0.0, _diagnostic_max(diagnostics, "readiness")))
    max_trade_caution = _clip(
        max(
            float(dict(diagnostics.get("LONG", {}) or {}).get("trade_caution", 0.0) or 0.0),
            float(dict(diagnostics.get("SHORT", {}) or {}).get("trade_caution", 0.0) or 0.0),
        )
    )
    reward = float(reward or 0.0)
    positive_consequence = _clip(max(0.0, reward))
    negative_consequence = _clip(max(0.0, -reward))
    action_taken = 1.0 if str(action or "").upper() in ("LONG", "SHORT") else 0.0
    event = str(outcome_event or "").upper()

    focus_tone = _clip((form_stability * 0.28) + (coherence * 0.28) + (temporal_trust * 0.24) + ((1.0 - tension) * 0.20))
    trust_tone = _clip((max_readiness * 0.34) + (temporal_trust * 0.24) + (positive_consequence * 0.30) + (afterimage * 0.12))
    caution_tone = _clip((max_trade_caution * 0.26) + (temporal_caution * 0.28) + (tension * 0.20) + (negative_consequence * 0.26))
    strain_tone = _clip((tension * 0.32) + (caution_tone * 0.34) + (max(0.0, 0.30 - max_readiness) * 0.18) + (action_taken * negative_consequence * 0.16))
    relief_tone = _clip((positive_consequence * 0.42) + ((1.0 - caution_tone) * 0.20) + (trust_tone * 0.20) + ((1.0 - tension) * 0.18))
    observation_tone = _clip(((1.0 - action_taken) * 0.30) + (afterimage * 0.22) + (temporal_trust * 0.18) + (max(0.0, 0.45 - max_readiness) * 0.30))

    tone_map = {
        "focus_tone": focus_tone,
        "trust_tone": trust_tone,
        "caution_tone": caution_tone,
        "strain_tone": strain_tone,
        "relief_tone": relief_tone,
        "observation_tone": observation_tone,
    }
    dominant_tone = max(tone_map, key=tone_map.get)
    neuro_support = _clip((focus_tone * 0.28) + (trust_tone * 0.30) + (relief_tone * 0.24) + (observation_tone * 0.18))
    neuro_load = _clip((caution_tone * 0.44) + (strain_tone * 0.42) + (negative_consequence * 0.14))
    neuro_balance = max(-1.0, min(1.0, neuro_support - neuro_load))

    return {
        "mini_neuro_dominant_tone": dominant_tone,
        "mini_focus_tone": focus_tone,
        "mini_trust_tone": trust_tone,
        "mini_caution_tone": caution_tone,
        "mini_strain_tone": strain_tone,
        "mini_relief_tone": relief_tone,
        "mini_observation_tone": observation_tone,
        "mini_neuro_support": neuro_support,
        "mini_neuro_load": neuro_load,
        "mini_neuro_balance": neuro_balance,
        "mini_neuro_event": event or "NO_EVENT",
        "passive_only": 1,
    }


__all__ = ["build_mini_neuro_state"]
