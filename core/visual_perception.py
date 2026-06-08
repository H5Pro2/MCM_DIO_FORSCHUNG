import hashlib

from core.sensory_reality import build_sensory_reality_state
from core.visual_cortex import build_visual_cortex_state


def _clip(value: float, low: float, high: float) -> float:
    return max(float(low), min(float(high), float(value)))


def _candle_span(candle: dict) -> float:
    high = float((candle or {}).get("high", 0.0) or 0.0)
    low = float((candle or {}).get("low", high) or high)
    return max(high - low, 1e-9)


def empty_visual_market_state() -> dict:
    visual_sight_state = {
        "form_id": "-",
        "form_family": "empty_form",
        "clarity": 0.0,
        "object_stability": 0.0,
        "coherence": 0.0,
        "direction_bias": 0.0,
        "range_position": 0.0,
        "form_pressure": 0.0,
        "form_resonance": 0.0,
        "form_fragility": 0.0,
        "depth": 0.0,
        "contact_candidate": 0.0,
        "background_load": 0.0,
        "sight_label": "empty_sight",
    }
    visual_cortex_state = build_visual_cortex_state(visual_sight_state)
    core_visual_trace_state = {
        "range_position": 0.0,
        "range_width": 0.0,
        "compression": 0.0,
        "expansion": 0.0,
        "visual_coherence": 0.0,
        "form_axes": {},
        "origin": "empty_visual_trace",
    }
    core_visual_interpretation_state = {
        "short_impulse": 0.0,
        "mid_impulse": 0.0,
        "body_pressure": 0.0,
        "wick_pressure": 0.0,
        "volume_bias": 0.0,
        "market_balance": 0.0,
        "breakout_tension": 0.0,
        "visual_form_pressure": 0.0,
        "visual_shape_resonance": 0.0,
        "visual_shape_fragility": 0.0,
        "sensory_reality_pressure": 0.0,
        "sensory_load": 0.0,
        "sensory_gate": 1.0,
        "sensory_reality_label": "quiet_outer_reality",
        "origin": "empty_visual_interpretation",
    }
    return {
        "spatial_bias": 0.0,
        "directional_bias": 0.0,
        "range_position": 0.0,
        "range_width": 0.0,
        "short_impulse": 0.0,
        "mid_impulse": 0.0,
        "compression": 0.0,
        "expansion": 0.0,
        "body_pressure": 0.0,
        "wick_pressure": 0.0,
        "volume_bias": 0.0,
        "market_balance": 0.0,
        "breakout_tension": 0.0,
        "visual_coherence": 0.0,
        "visual_sight_state": dict(visual_sight_state),
        "visual_cortex_state": dict(visual_cortex_state),
        "visual_form_state": {},
        "visual_clarity": 0.0,
        "visual_object_stability": 0.0,
        "visual_form_novelty": 0.0,
        "visual_blindness": 0.0,
        "visual_form_pressure": 0.0,
        "visual_shape_resonance": 0.0,
        "visual_shape_fragility": 0.0,
        "sensory_reality_pressure": 0.0,
        "sensory_load": 0.0,
        "sensory_redundancy": 0.0,
        "sensory_habituation": 0.0,
        "sensory_gate": 1.0,
        "sensory_active_axis_count": 0,
        "sensory_primary_pressure": 0.0,
        "sensory_reality_label": "quiet_outer_reality",
        "core_visual_trace_state": dict(core_visual_trace_state),
        "core_visual_interpretation_state": dict(core_visual_interpretation_state),
        "visual_sight_state": dict(visual_sight_state),
        "visual_cortex_state": dict(visual_cortex_state),
    }


def _quantize_visual_axis(value: float, step: float = 0.25, low: float = -1.0, high: float = 1.0) -> int:
    clipped = _clip(float(value or 0.0), low, high)
    return int(round(clipped / max(float(step), 1e-9)))


def _build_visual_form_id(*values) -> str:
    raw = "|".join(str(item) for item in values)
    return "vf_" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]


def _visual_form_family(form_axes: dict, visual_clarity: float, visual_form_pressure: float) -> str:
    axes = dict(form_axes or {})
    flow = float(axes.get("flow", 0.0) or 0.0)
    fracture = float(axes.get("fracture", 0.0) or 0.0)
    density = float(axes.get("density", 0.0) or 0.0)
    void = float(axes.get("void", 0.0) or 0.0)
    edge = float(axes.get("edge_strength", 0.0) or 0.0)

    form_family_pressures = {
        "flow_form": _clip((visual_clarity * 0.28) + (flow * 0.30) + ((1.0 - fracture) * 0.08), 0.0, 1.0),
        "broken_form": _clip((fracture * 0.42) + ((1.0 - visual_clarity) * 0.08), 0.0, 1.0),
        "dense_edge_form": _clip((density * 0.30) + (edge * 0.24) + (visual_form_pressure * 0.08), 0.0, 1.0),
        "quiet_void_form": _clip((void * 0.34) + ((1.0 - visual_form_pressure) * 0.16), 0.0, 1.0),
        "pressured_form": _clip((visual_form_pressure * 0.40) + (edge * 0.08) + (density * 0.06), 0.0, 1.0),
        "mixed_form": _clip((1.0 - max(flow, fracture, density, void, visual_form_pressure)) * 0.24 + (visual_clarity * 0.06), 0.0, 1.0),
    }
    return max(form_family_pressures, key=form_family_pressures.get)


def _visual_sight_label(clarity: float, pressure: float, fragility: float, contact_candidate: float) -> str:
    sight_pressures = {
        "clear_form_contact": _clip((clarity * 0.34) + (contact_candidate * 0.28), 0.0, 1.0),
        "pressured_unclear_form": _clip((pressure * 0.34) + ((1.0 - clarity) * 0.18), 0.0, 1.0),
        "fragile_form": _clip((fragility * 0.40) + (pressure * 0.08), 0.0, 1.0),
        "visible_form": _clip((clarity * 0.36) + ((1.0 - fragility) * 0.08), 0.0, 1.0),
        "background_sight": _clip(((1.0 - max(clarity, pressure, fragility, contact_candidate)) * 0.28), 0.0, 1.0),
    }
    return max(sight_pressures, key=sight_pressures.get)


def build_visual_market_state(window: list[dict]) -> dict:
    if not window:
        return empty_visual_market_state()

    candles = [dict(c or {}) for c in list(window or []) if isinstance(c, dict)]
    if not candles:
        return empty_visual_market_state()

    tail_short = candles[-8:]
    tail_mid = candles[-21:]
    last = tail_short[-1]
    prev = tail_short[-2] if len(tail_short) > 1 else tail_short[-1]

    last_open = float(last.get("open", 0.0) or 0.0)
    last_high = float(last.get("high", last_open) or last_open)
    last_low = float(last.get("low", last_open) or last_open)
    last_close = float(last.get("close", last_open) or last_open)
    last_volume = max(0.0, float(last.get("volume", 0.0) or 0.0))
    prev_close = float(prev.get("close", last_close) or last_close)

    short_spans = [_candle_span(candle) for candle in tail_short]
    mid_spans = [_candle_span(candle) for candle in tail_mid]
    short_span_mean = sum(short_spans) / max(1, len(short_spans))
    mid_span_mean = sum(mid_spans) / max(1, len(mid_spans))
    last_span = short_spans[-1]

    short_first_close = float((tail_short[0] or {}).get("close", last_close) or last_close)
    mid_first_close = float((tail_mid[0] or {}).get("close", last_close) or last_close)

    short_impulse = _clip(
        (last_close - short_first_close) / max(short_span_mean * 3.0, last_close * 0.0012, 1e-9),
        -1.0,
        1.0,
    )
    mid_impulse = _clip(
        (last_close - mid_first_close) / max(mid_span_mean * 8.0, last_close * 0.0020, 1e-9),
        -1.0,
        1.0,
    )

    mid_high = max(float((candle or {}).get("high", last_close) or last_close) for candle in tail_mid)
    mid_low = min(float((candle or {}).get("low", last_close) or last_close) for candle in tail_mid)
    mid_range = max(mid_high - mid_low, 1e-9)

    range_position = _clip((((last_close - mid_low) / mid_range) * 2.0) - 1.0, -1.0, 1.0)
    range_width = _clip(mid_range / max(last_close * 0.06, 1e-9), 0.0, 1.0)

    compression = _clip(1.0 - (last_span / max(short_span_mean, 1e-9)), 0.0, 1.0)
    expansion = _clip((last_span / max(short_span_mean, 1e-9)) - 1.0, 0.0, 1.0)

    body_pressure = _clip(abs(last_close - last_open) / max(last_span, 1e-9), 0.0, 1.0)
    upper_wick = max(0.0, last_high - max(last_open, last_close))
    lower_wick = max(0.0, min(last_open, last_close) - last_low)
    wick_pressure = _clip((upper_wick + lower_wick) / max(last_span, 1e-9), 0.0, 1.0)

    short_volumes = [max(0.0, float((candle or {}).get("volume", 0.0) or 0.0)) for candle in tail_short]
    short_volume_mean = sum(short_volumes) / max(1, len(short_volumes))
    volume_bias = _clip((last_volume / max(short_volume_mean, 1e-9)) - 1.0, -1.0, 1.0)

    directional_bias = _clip((short_impulse * 0.58) + (mid_impulse * 0.42), -1.0, 1.0)
    spatial_bias = _clip((range_position * 0.62) + (directional_bias * 0.38), -1.0, 1.0)
    breakout_tension = _clip(
        (expansion * 0.34)
        + (body_pressure * 0.22)
        + (abs(volume_bias) * 0.16)
        + (max(0.0, abs(range_position) - 0.55) * 0.22)
        + (abs(last_close - prev_close) / max(short_span_mean * 1.35, 1e-9) * 0.16),
        0.0,
        1.0,
    )
    market_balance = _clip(
        1.0
        - (abs(short_impulse - mid_impulse) * 0.46)
        - (expansion * 0.18)
        - (max(0.0, abs(range_position) - 0.35) * 0.24),
        0.0,
        1.0,
    )
    visual_coherence = _clip(
        (market_balance * 0.42)
        + ((1.0 - wick_pressure) * 0.18)
        + ((1.0 - min(1.0, abs(volume_bias))) * 0.12)
        + (max(0.0, 1.0 - abs(short_impulse - mid_impulse)) * 0.28),
        0.0,
        1.0,
    )

    closes = [float((candle or {}).get("close", last_close) or last_close) for candle in tail_mid]
    highs = [float((candle or {}).get("high", last_close) or last_close) for candle in tail_mid]
    lows = [float((candle or {}).get("low", last_close) or last_close) for candle in tail_mid]
    bodies = [
        abs(float((candle or {}).get("close", 0.0) or 0.0) - float((candle or {}).get("open", 0.0) or 0.0))
        for candle in tail_mid
    ]
    spans = [max(float(highs[index] - lows[index]), 1e-9) for index in range(len(tail_mid))]
    deltas = [closes[index] - closes[index - 1] for index in range(1, len(closes))]
    abs_delta_sum = sum(abs(value) for value in deltas)
    signed_delta_sum = sum(deltas)
    direction_consistency = _clip(abs(signed_delta_sum) / max(abs_delta_sum, 1e-9), 0.0, 1.0)

    second_deltas = [deltas[index] - deltas[index - 1] for index in range(1, len(deltas))]
    curvature_raw = (
        sum(abs(value) for value in second_deltas)
        / max(1, len(second_deltas))
        / max(mid_span_mean, last_close * 0.0012, 1e-9)
    )
    curvature = _clip(curvature_raw / 1.8, 0.0, 1.0)

    direction_flips = 0
    for index in range(1, len(deltas)):
        if (deltas[index] > 0 and deltas[index - 1] < 0) or (deltas[index] < 0 and deltas[index - 1] > 0):
            direction_flips += 1
    flip_pressure = _clip(direction_flips / max(1.0, float(len(deltas) - 1)), 0.0, 1.0)

    span_ratios = [span / max(mid_span_mean, 1e-9) for span in spans]
    range_rhythm = _clip(
        1.0 - (sum(abs(value - 1.0) for value in span_ratios) / max(1, len(span_ratios))),
        0.0,
        1.0,
    )
    body_mean = sum(bodies) / max(1, len(bodies))
    body_to_range = _clip(body_mean / max(mid_span_mean, 1e-9), 0.0, 1.0)

    edge_strength = _clip(
        (abs(range_position) * 0.22)
        + (abs(short_impulse - mid_impulse) * 0.22)
        + (breakout_tension * 0.26)
        + (expansion * 0.18)
        + (abs(volume_bias) * 0.12),
        0.0,
        1.0,
    )
    form_density = _clip(
        (body_to_range * 0.30)
        + (direction_consistency * 0.24)
        + (visual_coherence * 0.22)
        + ((1.0 - wick_pressure) * 0.14)
        + ((1.0 - compression) * 0.10),
        0.0,
        1.0,
    )
    fracture = _clip(
        (flip_pressure * 0.30)
        + (curvature * 0.24)
        + (wick_pressure * 0.18)
        + (expansion * 0.14)
        + (max(0.0, 1.0 - market_balance) * 0.14),
        0.0,
        1.0,
    )
    flow = _clip(
        (direction_consistency * 0.42)
        + (abs(directional_bias) * 0.26)
        + (market_balance * 0.18)
        + (max(0.0, 1.0 - curvature) * 0.14),
        0.0,
        1.0,
    )
    void = _clip(
        (compression * 0.26)
        + ((1.0 - body_to_range) * 0.24)
        + ((1.0 - abs(volume_bias)) * 0.14)
        + ((1.0 - abs(short_impulse)) * 0.16)
        + ((1.0 - abs(mid_impulse)) * 0.20),
        0.0,
        1.0,
    )
    visual_object_stability = _clip(
        (direction_consistency * 0.28)
        + (range_rhythm * 0.22)
        + (visual_coherence * 0.24)
        + (market_balance * 0.18)
        - (fracture * 0.22),
        0.0,
        1.0,
    )
    raw_visual_form_pressure = _clip(
        (breakout_tension * 0.28)
        + (edge_strength * 0.22)
        + (fracture * 0.18)
        + (abs(directional_bias) * 0.16)
        + (abs(volume_bias) * 0.10)
        + (max(0.0, 1.0 - visual_object_stability) * 0.06),
        0.0,
        1.0,
    )
    visual_clarity = _clip(
        (visual_object_stability * 0.30)
        + (flow * 0.22)
        + (form_density * 0.20)
        + (visual_coherence * 0.18)
        - (fracture * 0.18)
        - (void * 0.08),
        0.0,
        1.0,
    )
    raw_visual_form_novelty = _clip(
        (curvature * 0.22)
        + (edge_strength * 0.18)
        + (fracture * 0.22)
        + (abs(volume_bias) * 0.16)
        + (max(0.0, expansion - compression) * 0.12)
        + (max(0.0, 0.45 - visual_coherence) * 0.10),
        0.0,
        1.0,
    )

    sensory_reality_state = build_sensory_reality_state(
        expansion=expansion,
        body_pressure=body_pressure,
        wick_pressure=wick_pressure,
        volume_bias=volume_bias,
        range_position=range_position,
        short_impulse=short_impulse,
        mid_impulse=mid_impulse,
        breakout_tension=breakout_tension,
        edge_strength=edge_strength,
        fracture=fracture,
        visual_form_novelty=raw_visual_form_novelty,
    )
    sensory_gate = float(sensory_reality_state.get("sensory_gate", 1.0) or 1.0)
    sensory_habituation = float(sensory_reality_state.get("sensory_habituation", 0.0) or 0.0)
    sensory_reality_pressure = float(sensory_reality_state.get("sensory_reality_pressure", 0.0) or 0.0)

    visual_form_pressure = _clip(
        (raw_visual_form_pressure * sensory_gate)
        + (sensory_reality_pressure * 0.08),
        0.0,
        1.0,
    )
    visual_form_novelty = _clip(
        (raw_visual_form_novelty * (0.88 + sensory_gate * 0.12))
        - (sensory_habituation * 0.10),
        0.0,
        1.0,
    )
    visual_blindness = _clip(
        (visual_form_pressure * 0.42)
        + (max(0.0, 1.0 - visual_clarity) * 0.34)
        + (visual_form_novelty * 0.12)
        + (fracture * 0.12)
        - (visual_object_stability * 0.18),
        0.0,
        1.0,
    )
    visual_shape_resonance = _clip(
        (visual_coherence * 0.34)
        + (market_balance * 0.22)
        + (visual_object_stability * 0.24)
        + (form_density * 0.20),
        0.0,
        1.0,
    )
    visual_shape_fragility = _clip(
        (fracture * 0.34)
        + (visual_form_novelty * 0.20)
        + (wick_pressure * 0.16)
        + (curvature * 0.14)
        + (max(0.0, 1.0 - visual_object_stability) * 0.16),
        0.0,
        1.0,
    )

    form_axes = {
        "edge_strength": float(edge_strength),
        "curvature": float(curvature),
        "density": float(form_density),
        "fracture": float(fracture),
        "flow": float(flow),
        "void": float(void),
        "range_rhythm": float(range_rhythm),
        "direction_consistency": float(direction_consistency),
    }
    visual_form_id = _build_visual_form_id(
        _quantize_visual_axis(edge_strength, low=0.0, high=1.0),
        _quantize_visual_axis(curvature, low=0.0, high=1.0),
        _quantize_visual_axis(form_density, low=0.0, high=1.0),
        _quantize_visual_axis(fracture, low=0.0, high=1.0),
        _quantize_visual_axis(flow, low=0.0, high=1.0),
        _quantize_visual_axis(void, low=0.0, high=1.0),
        _quantize_visual_axis(visual_clarity, low=0.0, high=1.0),
        _quantize_visual_axis(visual_blindness, low=0.0, high=1.0),
    )
    visual_form_state = {
        "visual_form_id": str(visual_form_id),
        "axes": dict(form_axes),
        "clarity": float(visual_clarity),
        "object_stability": float(visual_object_stability),
        "novelty": float(visual_form_novelty),
        "blindness": float(visual_blindness),
        "pressure": float(visual_form_pressure),
        "resonance": float(visual_shape_resonance),
        "fragility": float(visual_shape_fragility),
        "sensory_reality": dict(sensory_reality_state),
    }
    visual_form_family = _visual_form_family(form_axes, visual_clarity, visual_form_pressure)
    visual_contact_candidate = _clip(
        (visual_clarity * 0.30)
        + (visual_object_stability * 0.24)
        + (visual_shape_resonance * 0.22)
        + (edge_strength * 0.12)
        - (visual_shape_fragility * 0.14)
        - (visual_blindness * 0.10),
        0.0,
        1.0,
    )
    visual_depth = _clip(
        (abs(range_position) * 0.18)
        + (range_width * 0.16)
        + (direction_consistency * 0.18)
        + (range_rhythm * 0.16)
        + (visual_object_stability * 0.18)
        + (visual_coherence * 0.14),
        0.0,
        1.0,
    )
    visual_background_load = _clip(
        (visual_blindness * 0.34)
        + (visual_shape_fragility * 0.24)
        + (raw_visual_form_novelty * 0.18)
        + (sensory_reality_pressure * 0.12)
        - (visual_clarity * 0.18)
        - (visual_contact_candidate * 0.12),
        0.0,
        1.0,
    )
    visual_sight_state = {
        "form_id": str(visual_form_id),
        "form_family": str(visual_form_family),
        "clarity": float(visual_clarity),
        "object_stability": float(visual_object_stability),
        "coherence": float(visual_coherence),
        "direction_bias": float(directional_bias),
        "range_position": float(range_position),
        "form_pressure": float(visual_form_pressure),
        "form_resonance": float(visual_shape_resonance),
        "form_fragility": float(visual_shape_fragility),
        "depth": float(visual_depth),
        "contact_candidate": float(visual_contact_candidate),
        "background_load": float(visual_background_load),
        "sight_label": _visual_sight_label(
            visual_clarity,
            visual_form_pressure,
            visual_shape_fragility,
            visual_contact_candidate,
        ),
    }
    core_visual_trace_state = {
        "range_position": float(range_position),
        "range_width": float(range_width),
        "compression": float(compression),
        "expansion": float(expansion),
        "visual_coherence": float(visual_coherence),
        "form_axes": dict(form_axes),
        "visual_form_id": str(visual_form_id),
        "visual_sight_state": dict(visual_sight_state),
        "origin": "visual_form_trace",
    }
    visual_cortex_state = build_visual_cortex_state(
        visual_sight_state,
        {
            "visual_form_state": dict(visual_form_state),
            "visual_trace_form_axes": dict(form_axes),
            "visual_clarity": float(visual_clarity),
            "visual_object_stability": float(visual_object_stability),
            "visual_coherence": float(visual_coherence),
            "visual_form_pressure": float(visual_form_pressure),
            "visual_shape_resonance": float(visual_shape_resonance),
            "visual_shape_fragility": float(visual_shape_fragility),
            "range_position": float(range_position),
            "directional_bias": float(directional_bias),
        },
    )
    core_visual_interpretation_state = {
        "spatial_bias": float(spatial_bias),
        "directional_bias": float(directional_bias),
        "short_impulse": float(short_impulse),
        "mid_impulse": float(mid_impulse),
        "body_pressure": float(body_pressure),
        "wick_pressure": float(wick_pressure),
        "volume_bias": float(volume_bias),
        "market_balance": float(market_balance),
        "breakout_tension": float(breakout_tension),
        "visual_clarity": float(visual_clarity),
        "visual_object_stability": float(visual_object_stability),
        "visual_form_novelty": float(visual_form_novelty),
        "visual_blindness": float(visual_blindness),
        "visual_form_pressure": float(visual_form_pressure),
        "visual_shape_resonance": float(visual_shape_resonance),
        "visual_shape_fragility": float(visual_shape_fragility),
        "visual_sight_state": dict(visual_sight_state),
        "visual_cortex_state": dict(visual_cortex_state),
        "sensory_reality": dict(sensory_reality_state),
        "origin": "derived_visual_interpretation",
    }

    return {
        "spatial_bias": float(spatial_bias),
        "directional_bias": float(directional_bias),
        "range_position": float(range_position),
        "range_width": float(range_width),
        "short_impulse": float(short_impulse),
        "mid_impulse": float(mid_impulse),
        "compression": float(compression),
        "expansion": float(expansion),
        "body_pressure": float(body_pressure),
        "wick_pressure": float(wick_pressure),
        "volume_bias": float(volume_bias),
        "market_balance": float(market_balance),
        "breakout_tension": float(breakout_tension),
        "visual_coherence": float(visual_coherence),
        "visual_sight_state": dict(visual_sight_state),
        "visual_cortex_state": dict(visual_cortex_state),
        "visual_form_state": dict(visual_form_state),
        "visual_clarity": float(visual_clarity),
        "visual_object_stability": float(visual_object_stability),
        "visual_form_novelty": float(visual_form_novelty),
        "visual_blindness": float(visual_blindness),
        "visual_form_pressure": float(visual_form_pressure),
        "visual_shape_resonance": float(visual_shape_resonance),
        "visual_shape_fragility": float(visual_shape_fragility),
        "sensory_reality_pressure": float(sensory_reality_state.get("sensory_reality_pressure", 0.0) or 0.0),
        "sensory_load": float(sensory_reality_state.get("sensory_load", 0.0) or 0.0),
        "sensory_redundancy": float(sensory_reality_state.get("sensory_redundancy", 0.0) or 0.0),
        "sensory_habituation": float(sensory_reality_state.get("sensory_habituation", 0.0) or 0.0),
        "sensory_gate": float(sensory_reality_state.get("sensory_gate", 1.0) or 1.0),
        "sensory_active_axis_count": int(sensory_reality_state.get("sensory_active_axis_count", 0) or 0),
        "sensory_primary_pressure": float(sensory_reality_state.get("sensory_primary_pressure", 0.0) or 0.0),
        "sensory_reality_label": str(sensory_reality_state.get("sensory_reality_label", "clear_outer_reality") or "clear_outer_reality"),
        "core_visual_trace_state": dict(core_visual_trace_state),
        "core_visual_interpretation_state": dict(core_visual_interpretation_state),
    }
