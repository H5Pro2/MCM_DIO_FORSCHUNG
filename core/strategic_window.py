# ==================================================
# core/strategic_window.py
# Strategic lookback / area perception
# ==================================================
import hashlib

import numpy as np

from config import Config

def build_strategic_window_state(
    window,
    candle_state=None,
    visual_market_state=None,
    structure_perception_state=None,
    form_symbol_state=None,
    meta_regulation_state=None,
    bot=None,
):
    """Build DIOs strategic lookback perception.

    This is a perception bridge, not an execution rule: it compresses recent
    market structure into a few candidate areas that the existing decision and
    trade-plan layers can inspect.
    """

    def _clip(value, lo=0.0, hi=1.0):
        try:
            value = float(value)
        except Exception:
            value = 0.0
        if value != value:
            value = 0.0
        return max(float(lo), min(float(hi), float(value)))

    def _value(row, key, default=0.0):
        if isinstance(row, dict):
            raw = row.get(key, default)
        else:
            raw = getattr(row, key, default)
        try:
            return float(raw)
        except Exception:
            return float(default)

    candles = list(window or [])
    candle = dict(candle_state or (candles[-1] if candles and isinstance(candles[-1], dict) else {}) or {})
    if not candles:
        return {
            "strategic_window_state": "no_area_focus",
            "area_focus_candidates": [],
            "lookback_window_size": 0,
            "lookback_bearing_capacity": 0.0,
            "strategic_pressure_interpretation": 0.0,
            "strategic_patience": 0.0,
            "area_bearing_quality": 0.0,
            "area_contact_pull": 0.0,
            "area_order_intention": 0.0,
            "area_invalidity_pressure": 0.0,
            "area_temporal_contact_mode": "open_time_contact",
            "area_future_present_coherence": 0.0,
            "area_contact_timing_fit": 0.0,
        }

    close_price = _value(candle, "close", _value(candles[-1], "close", 0.0))
    if close_price <= 0.0:
        close_price = _value(candles[-1], "close", 0.0)
    if close_price <= 0.0:
        close_price = 1.0

    meta = dict(meta_regulation_state or {})
    visual = dict(visual_market_state or {})
    structure = dict(structure_perception_state or {})
    form_symbol = dict(form_symbol_state or {})

    regulatory_load = _clip(
        (float(meta.get("regulatory_load", 0.0) or 0.0) * 0.30)
        + (float(meta.get("position_cognitive_load", 0.0) or 0.0) * 0.20)
        + (float(meta.get("field_overcoupling", 0.0) or 0.0) * 0.18)
        + (float(meta.get("sensory_load", 0.0) or 0.0) * 0.12)
        + (float(meta.get("open_hypothesis_pressure", 0.0) or 0.0) * 0.20)
    )
    visual_clarity = _clip(visual.get("visual_clarity", visual.get("form_clarity", 0.0)))
    structure_quality = _clip(structure.get("structure_quality", structure.get("visual_structure_quality", 0.0)))
    memory_resonance = _clip(
        (float(form_symbol.get("form_symbol_contact_utility", 0.0) or 0.0) * 0.32)
        + (float(form_symbol.get("form_symbol_contact_maturity", 0.0) or 0.0) * 0.26)
        + (float(form_symbol.get("form_symbol_memory_resonance", 0.0) or 0.0) * 0.22)
        + (float(meta.get("thought_hypothesis_trust", 0.0) or 0.0) * 0.20)
    )

    requested_lookback = int(getattr(Config, "MCM_STRATEGIC_LOOKBACK_WINDOW", 160) or 160)
    max_lookback = max(24, min(len(candles), requested_lookback))
    load_shrink = int(round(regulatory_load * max_lookback * 0.28))
    lookback_size = max(24, min(len(candles), max_lookback - load_shrink))
    tail = candles[-lookback_size:]

    closes = np.array([_value(row, "close", close_price) for row in tail], dtype=float)
    highs = np.array([_value(row, "high", _value(row, "close", close_price)) for row in tail], dtype=float)
    lows = np.array([_value(row, "low", _value(row, "close", close_price)) for row in tail], dtype=float)
    volumes = np.array([max(0.0, _value(row, "volume", 0.0)) for row in tail], dtype=float)
    if closes.size <= 0:
        closes = np.array([close_price], dtype=float)
        highs = np.array([close_price], dtype=float)
        lows = np.array([close_price], dtype=float)
        volumes = np.array([0.0], dtype=float)

    full_span = max(float(np.nanmax(highs) - np.nanmin(lows)), abs(close_price) * 0.002, 1e-9)
    avg_volume = max(float(np.nanmean(volumes)), 1e-9)
    segment_size = max(8, min(36, int(round(lookback_size / 4.0))))
    step = max(4, int(round(segment_size * 0.55)))

    candidates = []
    for start in range(0, max(1, lookback_size - segment_size + 1), step):
        end = min(lookback_size, start + segment_size)
        if end - start < 4:
            continue

        seg_closes = closes[start:end]
        seg_highs = highs[start:end]
        seg_lows = lows[start:end]
        seg_volumes = volumes[start:end]
        area_low = float(np.nanmin(seg_lows))
        area_high = float(np.nanmax(seg_highs))
        if area_low <= 0.0 or area_high <= 0.0 or area_high < area_low:
            continue

        area_mid = (area_low + area_high) * 0.50
        area_span = max(area_high - area_low, close_price * 0.0005, 1e-9)
        local_move = float(abs(seg_closes[-1] - seg_closes[0])) if seg_closes.size > 1 else 0.0
        body_sum = float(np.nansum(np.abs(np.diff(seg_closes)))) if seg_closes.size > 1 else 0.0
        compression = _clip(1.0 - (area_span / max(full_span, 1e-9)))
        density = _clip((body_sum / max(area_span, 1e-9)) / max(len(seg_closes), 1))
        impulse = _clip(local_move / max(area_span, 1e-9))
        volume_focus = _clip(float(np.nanmean(seg_volumes)) / max(avg_volume * 1.8, 1e-9))
        distance = abs(close_price - area_mid)
        distance_fit = _clip(1.0 - (distance / max(full_span * 0.72, area_span * 3.0, 1e-9)))
        present_contact = 1.0 if area_low <= close_price <= area_high else _clip(1.0 - (distance / max(area_span * 2.5, 1e-9)))
        recency = _clip((end / max(lookback_size, 1)) ** 0.75)
        temporal_depth = _clip(1.0 - recency)

        bearing = _clip(
            (compression * 0.18)
            + (density * 0.16)
            + (distance_fit * 0.16)
            + (present_contact * 0.12)
            + (volume_focus * 0.10)
            + (visual_clarity * 0.10)
            + (structure_quality * 0.10)
            + (memory_resonance * 0.12)
            - (regulatory_load * 0.12)
        )
        invalidity = _clip(
            (max(0.0, impulse - 0.72) * 0.28)
            + (max(0.0, regulatory_load - 0.62) * 0.28)
            + ((1.0 - distance_fit) * 0.16)
            + ((1.0 - max(visual_clarity, structure_quality)) * 0.10)
        )
        replay_fit = _clip(
            (memory_resonance * 0.28)
            + (temporal_depth * 0.18)
            + (compression * 0.18)
            + (density * 0.14)
            + (present_contact * 0.10)
            + (structure_quality * 0.12)
            - (invalidity * 0.16)
        )
        spacetime_fit = _clip(
            (distance_fit * 0.24)
            + (recency * 0.18)
            + (temporal_depth * 0.14)
            + (compression * 0.14)
            + (bearing * 0.18)
            + (replay_fit * 0.12)
        )
        order_intention = _clip(
            (bearing * 0.24)
            + (replay_fit * 0.18)
            + (spacetime_fit * 0.18)
            + (distance_fit * 0.16)
            + (present_contact * 0.10)
            + (memory_resonance * 0.10)
            - (invalidity * 0.22)
            - (regulatory_load * 0.08)
        )
        area_contact_pull = float(order_intention)
        patience = _clip(
            (bearing * 0.20)
            + (replay_fit * 0.18)
            + (temporal_depth * 0.16)
            + (compression * 0.14)
            + ((1.0 - regulatory_load) * 0.14)
            + (memory_resonance * 0.10)
            - (invalidity * 0.12)
        )
        score = _clip((bearing * 0.28) + (order_intention * 0.24) + (replay_fit * 0.18) + (spacetime_fit * 0.16) + (patience * 0.10) - (invalidity * 0.20))
        area_future_present_coherence = _clip((order_intention * 0.42) + (spacetime_fit * 0.32) + (present_contact * 0.18) - (invalidity * 0.18))
        area_contact_timing_fit = _clip((spacetime_fit * 0.38) + (distance_fit * 0.28) + (recency * 0.18) + (patience * 0.12) - (invalidity * 0.16))
        area_id_seed = f"{start}:{end}:{round(area_low, 5)}:{round(area_high, 5)}:{round(score, 4)}"

        candidates.append({
            "area_focus_id": "sa_" + hashlib.sha1(area_id_seed.encode("utf-8")).hexdigest()[:10],
            "area_index_start": int(start),
            "area_index_end": int(end),
            "area_price_low": float(area_low),
            "area_price_high": float(area_high),
            "area_price_mid": float(area_mid),
            "area_price_span": float(area_span),
            "area_distance_from_price": float(distance),
            "area_structural_density": float(density),
            "area_energy_compression": float(compression),
            "area_mcm_resonance": float(_clip((bearing * 0.46) + (memory_resonance * 0.34) + (present_contact * 0.20))),
            "area_memory_pull": float(memory_resonance),
            "area_bearing_quality": float(bearing),
            "area_zoom_need": float(_clip((1.0 - max(visual_clarity, structure_quality)) * 0.36 + invalidity * 0.28 + (1.0 - distance_fit) * 0.18)),
            "area_zoom_clarity": float(_clip((visual_clarity * 0.32) + (structure_quality * 0.30) + (bearing * 0.22) + (compression * 0.16))),
            "area_replay_fit": float(replay_fit),
            "area_patience_quality": float(patience),
            "area_contact_pull": float(area_contact_pull),
            "area_order_intention": float(order_intention),
            "area_invalidity_pressure": float(invalidity),
            "area_temporal_contact_mode": "present_contact" if present_contact >= 0.68 else ("recent_afterimage" if recency >= 0.62 else "deep_memory_contact"),
            "area_spacetime_fit": float(spacetime_fit),
            "area_future_present_coherence": float(area_future_present_coherence),
            "area_future_to_present_readiness": float(area_future_present_coherence),
            "area_contact_timing_fit": float(area_contact_timing_fit),
            "area_action_timing_fit": float(area_contact_timing_fit),
            "area_present_contact": float(present_contact),
            "area_afterimage": float(_clip(temporal_depth * (1.0 - present_contact) * (0.35 + compression * 0.35))),
            "area_temporal_relevance": float(_clip((recency * 0.34) + (temporal_depth * 0.22) + (spacetime_fit * 0.30) + (replay_fit * 0.14))),
            "area_score": float(score),
        })

    candidates.sort(key=lambda item: float(item.get("area_score", 0.0) or 0.0), reverse=True)
    candidates = candidates[:3]
    focus = dict(candidates[0]) if candidates else {}

    if not focus:
        return {
            "strategic_window_state": "no_area_focus",
            "area_focus_candidates": [],
            "lookback_window_size": int(lookback_size),
            "lookback_bearing_capacity": 0.0,
            "strategic_pressure_interpretation": float(regulatory_load),
            "strategic_patience": 0.0,
            "area_bearing_quality": 0.0,
            "area_contact_pull": 0.0,
            "area_order_intention": 0.0,
            "area_invalidity_pressure": float(regulatory_load),
            "area_temporal_contact_mode": "open_time_contact",
            "area_future_present_coherence": 0.0,
            "area_contact_timing_fit": 0.0,
        }

    lookback_bearing = _clip(sum(float(item.get("area_bearing_quality", 0.0) or 0.0) for item in candidates) / max(len(candidates), 1))
    strategic_pressure = _clip(
        (regulatory_load * 0.34)
        + (float(focus.get("area_invalidity_pressure", 0.0) or 0.0) * 0.30)
        + ((1.0 - lookback_bearing) * 0.18)
        + (float(focus.get("area_zoom_need", 0.0) or 0.0) * 0.18)
    )
    strategic_state = "area_focus"
    if float(focus.get("area_present_contact", 0.0) or 0.0) >= 0.68:
        strategic_state = "present_area_contact"
    elif float(focus.get("area_replay_fit", 0.0) or 0.0) >= 0.58:
        strategic_state = "replay_area_focus"
    elif strategic_pressure >= 0.66:
        strategic_state = "unclear_area_pressure"

    result = dict(focus)
    result.update({
        "strategic_window_state": strategic_state,
        "area_focus_candidates": list(candidates),
        "lookback_window_size": int(lookback_size),
        "lookback_bearing_capacity": float(lookback_bearing),
        "strategic_pressure_interpretation": float(strategic_pressure),
        "strategic_patience": float(focus.get("area_patience_quality", 0.0) or 0.0),
    })
    return result


