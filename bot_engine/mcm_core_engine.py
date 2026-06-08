import math

from core.market_audio import build_market_hearing_state, limit_energy_amplitude


def _clip(value: float, low: float, high: float) -> float:
    return max(float(low), min(float(high), float(value)))


def _coh_zone_from_value(coherence: float) -> float:
    return _clip(float(coherence) * 2.0, -2.0, 2.0)


def _candle_span(candle: dict) -> float:
    high = float((candle or {}).get("high", 0.0) or 0.0)
    low = float((candle or {}).get("low", high) or high)
    return max(high - low, 1e-9)


def _candle_coherence(candle: dict) -> float:
    open_price = float((candle or {}).get("open", 0.0) or 0.0)
    close_price = float((candle or {}).get("close", open_price) or open_price)
    span = _candle_span(candle)
    return _clip((close_price - open_price) / span, -1.0, 1.0)


def _limit_energy_amplitude(raw_energy: float) -> dict:
    return limit_energy_amplitude(raw_energy)


def _build_core_trace_state(
    *,
    energy: float,
    coherence: float,
    asymmetry: int,
    coh_zone: float,
    relative_range: float = 0.0,
    momentum: float = 0.0,
    volume_pressure: float = 0.0,
    energy_raw_amplitude: float | None = None,
    energy_limited_amplitude: float | None = None,
    energy_limiter_gain: float | None = None,
    energy_overdrive: float | None = None,
    market_hearing_state: dict | None = None,
    origin: str = "ohlcv_energy_trace",
) -> dict:
    """Pure Kernspur: keine Handlungsdeutung, keine Entscheidungsvorgabe."""

    if energy_raw_amplitude is None or energy_limited_amplitude is None:
        limiter_state = _limit_energy_amplitude(float(energy))
        energy_raw_amplitude = limiter_state["energy_raw_amplitude"]
        energy_limited_amplitude = limiter_state["energy_limited_amplitude"]
        energy_limiter_gain = limiter_state["energy_limiter_gain"]
        energy_overdrive = limiter_state["energy_overdrive"]

    energy_amplitude_stimulus = _clip(float(energy_limited_amplitude or 0.0), 0.0, 2.5)
    if not isinstance(market_hearing_state, dict):
        market_hearing_state = _build_market_hearing_state(
            raw_energy=float(energy),
            limited_abs=float(energy_limited_amplitude or 0.0),
            limiter_gain=float(energy_limiter_gain if energy_limiter_gain is not None else 1.0),
            overdrive=float(energy_overdrive or 0.0),
        )
    return {
        "energy": float(energy),
        "energy_raw_amplitude": float(energy_raw_amplitude or 0.0),
        "energy_limited_amplitude": float(energy_limited_amplitude or 0.0),
        "energy_amplitude_stimulus": float(energy_amplitude_stimulus),
        "energy_limiter_gain": float(energy_limiter_gain if energy_limiter_gain is not None else 1.0),
        "energy_overdrive": float(energy_overdrive or 0.0),
        "energy_frequency_stimulus": float(energy_amplitude_stimulus),
        "energy_stimulus_channel": "market_hearing_normalized",
        "market_hearing_state": dict(market_hearing_state),
        "market_loudness": float(market_hearing_state.get("loudness", energy_amplitude_stimulus) or 0.0),
        "market_frequency_hz": float(market_hearing_state.get("frequency_hz", 0.0) or 0.0),
        "market_hearing_compression": float(market_hearing_state.get("compression", 0.0) or 0.0),
        "market_tone": str(market_hearing_state.get("tone", "silent_tone") or "silent_tone"),
        "coherence": float(coherence),
        "asymmetry": int(asymmetry),
        "coh_zone": float(coh_zone),
        "relative_range": float(relative_range),
        "momentum": float(momentum),
        "volume_pressure": float(volume_pressure),
        "origin": str(origin),
    }


def _build_core_interpretation_state(
    *,
    stability: float = 0.0,
    perceived_pressure: float = 0.0,
    origin: str = "derived_compatibility_interpretation",
) -> dict:
    """Abgeleitete Deutung: bleibt kompatibel, ist aber vom Kern getrennt."""

    return {
        "stability": float(stability),
        "perceived_pressure": float(perceived_pressure),
        "origin": str(origin),
    }


def compute_tension_from_ohlc(
    o_: float,
    h_: float,
    l_: float,
    c_: float,
    v_: float | None = None,
):
    """
    returns:
        energy (float)
        coherence (float)
        asymmetry (int)
        coh_zone (float)
    """

    span = max(h_ - l_, 1e-9)
    body = c_ - o_
    body_ratio = _clip(abs(body) / span, 0.0, 1.0)
    close_position = _clip((((c_ - l_) / span) * 2.0) - 1.0, -1.0, 1.0)
    upper_wick = max(0.0, h_ - max(o_, c_))
    lower_wick = max(0.0, min(o_, c_) - l_)
    wick_imbalance = _clip((lower_wick - upper_wick) / span, -1.0, 1.0)

    coherence = _clip(((body / span) * 0.72) + (close_position * 0.28), -1.0, 1.0)

    midpoint = (h_ + l_) / 2.0
    center_deviation = (
        abs(o_ - midpoint)
        + abs(c_ - midpoint)
        + abs(h_ - midpoint)
        + abs(l_ - midpoint)
    ) / (span * 2.0)
    range_pressure = _clip((span / max(abs(c_), 1e-9)) * 120.0, 0.0, 1.0)

    volume_factor = 1.0
    if v_ is not None:
        try:
            volume_factor += min(0.22, math.log1p(max(float(v_), 0.0)) / 18.0)
        except Exception:
            volume_factor = 1.0

    energy = (
        (center_deviation * 0.46)
        + (body_ratio * 0.34)
        + (abs(close_position) * 0.14)
        + (abs(wick_imbalance) * 0.06)
        + (range_pressure * 0.18)
    ) * volume_factor

    if coherence > 0:
        asymmetry = 1
    elif coherence < 0:
        asymmetry = -1
    else:
        asymmetry = 0

    coh_zone = _coh_zone_from_value(coherence)
    return float(energy), float(coherence), int(asymmetry), float(coh_zone)


def _build_market_hearing_state(
    *,
    raw_energy: float,
    limited_abs: float,
    limiter_gain: float,
    overdrive: float,
    candles: list[dict] | None = None,
) -> dict:
    return build_market_hearing_state(
        raw_energy=raw_energy,
        limited_abs=limited_abs,
        limiter_gain=limiter_gain,
        overdrive=overdrive,
        candles=candles,
    )


def _empty_tension_state(origin: str) -> dict:
    market_hearing_state = _build_market_hearing_state(
        raw_energy=0.0,
        limited_abs=0.0,
        limiter_gain=1.0,
        overdrive=0.0,
    )
    core_trace_state = _build_core_trace_state(
        energy=0.0,
        coherence=0.0,
        asymmetry=0,
        coh_zone=0.0,
        market_hearing_state=market_hearing_state,
        origin=origin,
    )
    core_interpretation_state = _build_core_interpretation_state(origin=origin)
    return {
        "energy": 0.0,
        "energy_raw_amplitude": 0.0,
        "energy_limited_amplitude": 0.0,
        "energy_amplitude_stimulus": 0.0,
        "energy_limiter_gain": 1.0,
        "energy_overdrive": 0.0,
        "energy_frequency_stimulus": 0.0,
        "energy_stimulus_channel": "market_hearing_normalized",
        "market_hearing_state": dict(market_hearing_state),
        "market_loudness": 0.0,
        "market_frequency_hz": 0.0,
        "market_hearing_compression": 0.0,
        "market_tone": "silent_tone",
        "coherence": 0.0,
        "asymmetry": 0,
        "coh_zone": 0.0,
        "relative_range": 0.0,
        "momentum": 0.0,
        "stability": 0.0,
        "perceived_pressure": 0.0,
        "volume_pressure": 0.0,
        "core_trace_state": dict(core_trace_state),
        "core_interpretation_state": dict(core_interpretation_state),
    }


def build_tension_state_from_window(window: list[dict]) -> dict:
    if not window:
        return _empty_tension_state("empty_window")

    candles = [dict(c or {}) for c in list(window or []) if isinstance(c, dict)]
    if not candles:
        return _empty_tension_state("empty_candles")

    tail = candles[-8:]
    last = tail[-1]
    prev = tail[-2] if len(tail) > 1 else tail[-1]

    last_open = float(last.get("open", 0.0) or 0.0)
    last_high = float(last.get("high", last_open) or last_open)
    last_low = float(last.get("low", last_open) or last_open)
    last_close = float(last.get("close", last_open) or last_open)
    last_volume = float(last.get("volume", 0.0) or 0.0)
    prev_close = float(prev.get("close", last_close) or last_close)

    raw_energy, coherence, asymmetry, coh_zone = compute_tension_from_ohlc(
        last_open,
        last_high,
        last_low,
        last_close,
        last_volume,
    )
    energy_limiter_state = _limit_energy_amplitude(raw_energy)
    energy = float(energy_limiter_state["energy_limited"])
    energy_raw_amplitude = float(energy_limiter_state["energy_raw_amplitude"])
    energy_limited_amplitude = float(energy_limiter_state["energy_limited_amplitude"])
    market_hearing_state = _build_market_hearing_state(
        raw_energy=raw_energy,
        limited_abs=energy_limited_amplitude,
        limiter_gain=float(energy_limiter_state["energy_limiter_gain"]),
        overdrive=float(energy_limiter_state["energy_overdrive"]),
        candles=candles,
    )
    energy_amplitude_stimulus = _clip(float(market_hearing_state.get("loudness", energy_limited_amplitude) or 0.0), 0.0, 2.5)

    spans = [_candle_span(candle) for candle in tail]
    span_mean = sum(spans) / max(1, len(spans))
    last_span = spans[-1]

    relative_range_raw = last_span / max(span_mean, 1e-9)
    relative_range = _clip(relative_range_raw / 2.0, 0.0, 1.5)

    momentum_denominator = max(span_mean, last_close * 0.0012, 1e-9)
    momentum = _clip((last_close - prev_close) / momentum_denominator, -1.0, 1.0)

    coherences = [_candle_coherence(candle) for candle in tail]
    coherence_mean = sum(coherences) / max(1, len(coherences))
    coherence_dispersion = sum(abs(value - coherence_mean) for value in coherences) / max(1, len(coherences))
    range_dispersion = sum(abs((span / max(span_mean, 1e-9)) - 1.0) for span in spans) / max(1, len(spans))
    stability = _clip(1.0 - (coherence_dispersion * 0.62) - (range_dispersion * 0.28), 0.0, 1.0)

    volumes = [max(0.0, float((candle or {}).get("volume", 0.0) or 0.0)) for candle in tail]
    volume_mean = sum(volumes) / max(1, len(volumes))
    volume_pressure = _clip((last_volume / max(volume_mean, 1e-9)) - 1.0, -1.0, 1.0)

    perceived_pressure = _clip(
        (abs(momentum) * 0.34)
        + (max(0.0, relative_range_raw - 1.0) * 0.24)
        + (max(0.0, energy_amplitude_stimulus - 1.0) * 0.10)
        + (abs(volume_pressure) * 0.14)
        + ((1.0 - stability) * 0.18),
        0.0,
        1.0,
    )
    core_trace_state = _build_core_trace_state(
        energy=energy,
        coherence=coherence,
        asymmetry=asymmetry,
        coh_zone=coh_zone,
        relative_range=relative_range,
        momentum=momentum,
        volume_pressure=volume_pressure,
        energy_raw_amplitude=energy_raw_amplitude,
        energy_limited_amplitude=energy_limited_amplitude,
        energy_limiter_gain=float(energy_limiter_state["energy_limiter_gain"]),
        energy_overdrive=float(energy_limiter_state["energy_overdrive"]),
        market_hearing_state=market_hearing_state,
    )
    core_interpretation_state = _build_core_interpretation_state(
        stability=stability,
        perceived_pressure=perceived_pressure,
    )

    return {
        "energy": float(energy),
        "energy_raw_amplitude": float(energy_raw_amplitude),
        "energy_limited_amplitude": float(energy_limited_amplitude),
        "energy_amplitude_stimulus": float(energy_amplitude_stimulus),
        "energy_limiter_gain": float(energy_limiter_state["energy_limiter_gain"]),
        "energy_overdrive": float(energy_limiter_state["energy_overdrive"]),
        "energy_frequency_stimulus": float(energy_amplitude_stimulus),
        "energy_stimulus_channel": "market_hearing_normalized",
        "market_hearing_state": dict(market_hearing_state),
        "market_loudness": float(market_hearing_state.get("loudness", energy_amplitude_stimulus) or 0.0),
        "market_frequency_hz": float(market_hearing_state.get("frequency_hz", 0.0) or 0.0),
        "market_hearing_compression": float(market_hearing_state.get("compression", 0.0) or 0.0),
        "market_tone": str(market_hearing_state.get("tone", "silent_tone") or "silent_tone"),
        "coherence": float(coherence),
        "asymmetry": int(asymmetry),
        "coh_zone": float(coh_zone),
        "relative_range": float(relative_range),
        "momentum": float(momentum),
        "stability": float(stability),
        "perceived_pressure": float(perceived_pressure),
        "volume_pressure": float(volume_pressure),
        "core_trace_state": dict(core_trace_state),
        "core_interpretation_state": dict(core_interpretation_state),
    }
