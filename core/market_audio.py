"""Market audio sense.

This module translates candle energy into a compact hearing state. It is a
perception adapter only: no entry logic, no strategy, no order permission.
"""

from __future__ import annotations

from config import Config


def _clip(value: float, low: float, high: float) -> float:
    try:
        value = float(value)
    except Exception:
        value = 0.0
    return max(float(low), min(float(high), float(value)))


def limit_energy_amplitude(raw_energy: float) -> dict:
    """Normalize raw candle energy into a bounded auditory amplitude."""

    raw = float(raw_energy or 0.0)
    raw_abs = abs(raw)

    if not bool(getattr(Config, "MCM_ENERGY_LIMITER_ENABLED", True)):
        limited_abs = raw_abs
    else:
        threshold = max(0.0, float(getattr(Config, "MCM_ENERGY_LIMITER_THRESHOLD", 0.85) or 0.85))
        ratio = _clip(float(getattr(Config, "MCM_ENERGY_LIMITER_RATIO", 0.35) or 0.35), 0.0, 1.0)
        ceiling = max(threshold, float(getattr(Config, "MCM_ENERGY_LIMITER_CEILING", 1.20) or 1.20))

        if raw_abs <= threshold:
            limited_abs = raw_abs
        else:
            limited_abs = threshold + ((raw_abs - threshold) * ratio)
        limited_abs = min(limited_abs, ceiling)

    sign = -1.0 if raw < 0.0 else 1.0
    limited = sign * limited_abs
    gain = limited_abs / raw_abs if raw_abs > 1e-9 else 1.0
    overdrive = max(0.0, raw_abs - limited_abs)

    return {
        "energy_raw_amplitude": float(raw_abs),
        "energy_limited_amplitude": float(limited_abs),
        "energy_limiter_gain": float(gain),
        "energy_overdrive": float(overdrive),
        "energy_limited": float(limited),
    }


def _trimmed_mean(values: list[float]) -> float:
    clean = sorted(max(0.0, float(value or 0.0)) for value in values if value is not None)
    if not clean:
        return 0.0
    trim = int(len(clean) * 0.10)
    if trim > 0 and len(clean) > trim * 2:
        clean = clean[trim:-trim]
    return sum(clean) / max(1, len(clean))


def _candle_energy(candle: dict) -> float:
    open_price = float((candle or {}).get("open", 0.0) or 0.0)
    high = float((candle or {}).get("high", open_price) or open_price)
    low = float((candle or {}).get("low", open_price) or open_price)
    close = float((candle or {}).get("close", open_price) or open_price)
    volume = float((candle or {}).get("volume", 0.0) or 0.0)

    span = max(high - low, 1e-9)
    body = close - open_price
    body_ratio = _clip(abs(body) / span, 0.0, 1.0)
    close_position = _clip((((close - low) / span) * 2.0) - 1.0, -1.0, 1.0)
    upper_wick = max(0.0, high - max(open_price, close))
    lower_wick = max(0.0, min(open_price, close) - low)
    wick_imbalance = _clip((lower_wick - upper_wick) / span, -1.0, 1.0)

    midpoint = (high + low) / 2.0
    center_deviation = (
        abs(open_price - midpoint)
        + abs(close - midpoint)
        + abs(high - midpoint)
        + abs(low - midpoint)
    ) / (span * 2.0)
    range_pressure = _clip((span / max(abs(close), 1e-9)) * 120.0, 0.0, 1.0)

    volume_factor = 1.0
    try:
        import math

        volume_factor += min(0.22, math.log1p(max(float(volume), 0.0)) / 18.0)
    except Exception:
        volume_factor = 1.0

    return float(
        (
            (center_deviation * 0.46)
            + (body_ratio * 0.34)
            + (abs(close_position) * 0.14)
            + (abs(wick_imbalance) * 0.06)
            + (range_pressure * 0.18)
        )
        * volume_factor
    )


def market_energy_baseline(candles: list[dict] | None, fallback: float) -> float:
    """Estimate the market's local normal loudness from recent candles."""

    if not candles:
        return max(abs(float(fallback or 0.0)), 1e-6)

    baseline_window = max(8, int(getattr(Config, "MCM_MARKET_HEARING_BASELINE_WINDOW", 96) or 96))
    energies: list[float] = []
    for candle in list(candles or [])[-baseline_window:]:
        if not isinstance(candle, dict):
            continue
        try:
            energies.append(abs(_candle_energy(candle)))
        except Exception:
            continue

    baseline = _trimmed_mean(energies)
    return max(baseline, abs(float(fallback or 0.0)) * 0.20, 1e-6)


def tone_from_loudness(loudness: float, compression: float) -> str:
    loudness = max(0.0, float(loudness or 0.0))
    compression = max(0.0, float(compression or 0.0))
    if loudness < 0.08:
        return "silent_tone"
    if compression > 0.34:
        return "compressed_loud_tone"
    if loudness < 0.55:
        return "low_tone"
    if loudness < 1.10:
        return "clear_tone"
    if loudness < 1.65:
        return "bright_tone"
    return "overdriven_tone"


def build_market_hearing_state(
    *,
    raw_energy: float,
    limited_abs: float,
    limiter_gain: float,
    overdrive: float,
    candles: list[dict] | None = None,
) -> dict:
    """Build DIO's compact market hearing state."""

    raw_abs = abs(float(raw_energy or 0.0))
    limited_abs = max(0.0, float(limited_abs or 0.0))
    baseline = market_energy_baseline(candles, fallback=max(raw_abs, limited_abs))
    normalized_raw = raw_abs / max(baseline, 1e-6)

    threshold = 1.0
    ratio = _clip(float(getattr(Config, "MCM_ENERGY_LIMITER_RATIO", 0.35) or 0.35), 0.0, 1.0)
    if normalized_raw <= threshold:
        loudness = normalized_raw
    else:
        loudness = threshold + ((normalized_raw - threshold) * ratio)
    loudness = _clip(loudness, 0.0, 2.5)

    reference_loudness = max(0.1, float(getattr(Config, "MCM_MARKET_HEARING_REFERENCE_LOUDNESS", 2.0) or 2.0))
    frequency_curve = max(0.25, float(getattr(Config, "MCM_MARKET_HEARING_FREQUENCY_CURVE", 1.60) or 1.60))
    frequency_norm = _clip(loudness / reference_loudness, 0.0, 1.0) ** frequency_curve
    min_hz = max(0.0, float(getattr(Config, "MCM_MARKET_HEARING_MIN_HZ", 20.0) or 20.0))
    max_hz = max(min_hz, float(getattr(Config, "MCM_MARKET_HEARING_MAX_HZ", 17000.0) or 17000.0))
    frequency_hz = 0.0 if loudness < 0.02 else min_hz + (frequency_norm * (max_hz - min_hz))

    normalized_compression = _clip(max(0.0, normalized_raw - loudness) / max(normalized_raw, 1e-6), 0.0, 1.0)
    limiter_compression = _clip(1.0 - float(limiter_gain or 1.0), 0.0, 1.0)
    compression = max(normalized_compression, limiter_compression)

    return {
        "sense": "hearing",
        "channel": "market_audio",
        "loudness": float(loudness),
        "frequency_hz": float(frequency_hz),
        "compression": float(compression),
        "tone": tone_from_loudness(loudness, compression),
        "baseline": float(baseline),
        "normalized_raw_loudness": float(normalized_raw),
        "frequency_curve": float(frequency_curve),
        "raw_amplitude": float(raw_abs),
        "limited_amplitude": float(limited_abs),
        "overdrive": float(max(0.0, float(overdrive or 0.0))),
        "action_permission": 0.0,
    }


def build_silent_market_hearing_state() -> dict:
    return build_market_hearing_state(
        raw_energy=0.0,
        limited_abs=0.0,
        limiter_gain=1.0,
        overdrive=0.0,
    )


__all__ = [
    "build_market_hearing_state",
    "build_silent_market_hearing_state",
    "limit_energy_amplitude",
    "market_energy_baseline",
    "tone_from_loudness",
]
