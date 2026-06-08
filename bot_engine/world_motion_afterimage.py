# ==================================================
# bot_engine/world_motion_afterimage.py
# Bewegte-Welt-Nachhall
# ==================================================


def _clip(value, lo=0.0, hi=1.0):
    try:
        value = float(value)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return max(float(lo), min(float(hi), float(value)))


def _as_float(value, default=0.0):
    try:
        value = float(value)
    except Exception:
        return float(default)
    if value != value:
        return float(default)
    return float(value)


def _packet_window(packet):
    return [dict(item or {}) for item in list((packet or {}).get("window", []) or []) if isinstance(item, dict)]


def _derive_doppler_axes(
    *,
    previous_strength,
    previous_pressure,
    previous_direction,
    previous_volatility,
    previous_acceleration,
    strength,
    pressure,
    direction,
    volatility,
    acceleration,
):
    strength_delta = _clip(strength - previous_strength, -1.0, 1.0)
    pressure_delta = _clip(pressure - previous_pressure, -1.0, 1.0)
    direction_delta = _clip(direction - previous_direction, -1.0, 1.0)
    volatility_delta = _clip(volatility - previous_volatility, -1.0, 1.0)
    acceleration_delta = _clip(acceleration - previous_acceleration, -1.0, 1.0)

    coherent_motion = _clip(1.0 - abs(direction_delta), 0.0, 1.0)
    motion_energy = _clip((pressure * 0.38) + (strength * 0.30) + (volatility * 0.18) + (abs(acceleration) * 0.14))
    motion_approach_pressure = _clip(
        (max(0.0, pressure_delta) * 0.34)
        + (max(0.0, strength_delta) * 0.26)
        + (max(0.0, abs(direction) - abs(previous_direction)) * 0.16)
        + (max(0.0, acceleration * direction) * 0.12)
        + (motion_energy * 0.12)
    )
    motion_recession_pressure = _clip(
        (max(0.0, -pressure_delta) * 0.34)
        + (max(0.0, -strength_delta) * 0.26)
        + (max(0.0, abs(previous_direction) - abs(direction)) * 0.14)
        + (max(0.0, -acceleration * direction) * 0.12)
        + ((1.0 - motion_energy) * 0.10)
    )
    contact_frequency_shift = _clip(
        (abs(pressure_delta) * 0.24)
        + (abs(strength_delta) * 0.20)
        + (abs(direction_delta) * 0.18)
        + (abs(volatility_delta) * 0.18)
        + (abs(acceleration_delta) * 0.20)
    )
    afterimage_doppler_bias = _clip(
        (direction * pressure * 0.54)
        + (acceleration * 0.24)
        + (direction_delta * 0.14)
        + ((motion_approach_pressure - motion_recession_pressure) * 0.22),
        -1.0,
        1.0,
    )
    future_variant_pressure = _clip(
        (motion_approach_pressure * 0.28)
        + (contact_frequency_shift * 0.24)
        + (volatility * 0.18)
        + (abs(afterimage_doppler_bias) * 0.16)
        + ((1.0 - coherent_motion) * 0.10)
        + (motion_recession_pressure * 0.04)
    )
    afterimage_action_maturity = _clip(
        (coherent_motion * 0.28)
        + ((1.0 - volatility) * 0.18)
        + ((1.0 - contact_frequency_shift) * 0.18)
        + (motion_approach_pressure * 0.12)
        + (motion_recession_pressure * 0.08)
        + (min(strength, pressure) * 0.16)
        - (future_variant_pressure * 0.10)
    )

    doppler_label_pressures = {
        "variant_pressure": float((future_variant_pressure * 0.46) + (contact_frequency_shift * 0.34) + (volatility * 0.10)),
        "approaching_motion": float((motion_approach_pressure * 0.56) + (max(0.0, afterimage_doppler_bias) * 0.22) + (coherent_motion * 0.12)),
        "receding_motion": float((motion_recession_pressure * 0.56) + (max(0.0, -afterimage_doppler_bias) * 0.22) + (coherent_motion * 0.12)),
        "directional_shift": float((abs(afterimage_doppler_bias) * 0.48) + (abs(direction_delta) * 0.28) + (contact_frequency_shift * 0.12)),
        "frequency_shift": float((contact_frequency_shift * 0.52) + (abs(volatility_delta) * 0.18) + (abs(acceleration_delta) * 0.16)),
        "doppler_clear": float((coherent_motion * 0.34) + ((1.0 - contact_frequency_shift) * 0.24) + ((1.0 - future_variant_pressure) * 0.18)),
    }
    label = max(doppler_label_pressures, key=doppler_label_pressures.get)

    return {
        "motion_approach_pressure": float(motion_approach_pressure),
        "motion_recession_pressure": float(motion_recession_pressure),
        "contact_frequency_shift": float(contact_frequency_shift),
        "afterimage_doppler_bias": float(afterimage_doppler_bias),
        "future_variant_pressure": float(future_variant_pressure),
        "afterimage_action_maturity": float(afterimage_action_maturity),
        "afterimage_doppler_label": str(label),
        "afterimage_doppler_label_pressures": dict(doppler_label_pressures),
    }


def _build_world_motion_state(previous_state=None, packet=None, *, motion_count=1, missed_count=0, observation_kind="missed"):
    previous = dict(previous_state or {})
    window = _packet_window(packet)
    motion_count = max(1, int(motion_count or 1))
    missed_count = max(0, int(missed_count or 0))

    previous_strength = _clip(previous.get("world_motion_afterimage_strength", 0.0))
    previous_pressure = _clip(previous.get("world_motion_afterimage_pressure", 0.0))
    previous_direction = _clip(previous.get("world_motion_afterimage_direction", 0.0), -1.0, 1.0)
    previous_volatility = _clip(previous.get("world_motion_afterimage_volatility", 0.0))
    previous_acceleration = _clip(previous.get("world_motion_afterimage_acceleration", 0.0), -1.0, 1.0)

    if len(window) < 2:
        missed_pressure = _clip(missed_count / 10.0)
        strength = _clip((previous_strength * 0.72) + min(1.0, motion_count / 12.0) * 0.06 + missed_pressure * 0.08)
        pressure = _clip((previous_pressure * 0.70) + min(1.0, motion_count / 10.0) * 0.04 + missed_pressure * 0.10)
        direction = previous_direction * 0.86
        volatility = previous_volatility * 0.82
        acceleration = previous_acceleration * 0.76
        doppler = _derive_doppler_axes(
            previous_strength=previous_strength,
            previous_pressure=previous_pressure,
            previous_direction=previous_direction,
            previous_volatility=previous_volatility,
            previous_acceleration=previous_acceleration,
            strength=strength,
            pressure=pressure,
            direction=direction,
            volatility=volatility,
            acceleration=acceleration,
        )
        return {
            "world_motion_afterimage_strength": float(strength),
            "world_motion_afterimage_pressure": float(pressure),
            "world_motion_afterimage_direction": float(direction),
            "world_motion_afterimage_volatility": float(volatility),
            "world_motion_afterimage_acceleration": float(acceleration),
            "world_motion_afterimage_count": int(previous.get("world_motion_afterimage_count", 0) or 0) + motion_count,
            "world_motion_seen_count": int(previous.get("world_motion_seen_count", 0) or 0) + motion_count,
            "world_motion_afterimage_missed_count": int(previous.get("world_motion_afterimage_missed_count", 0) or 0) + missed_count,
            "world_motion_observation_kind": str(observation_kind),
            "world_motion_afterimage_label": "motion_afterimage_fading",
            **doppler,
        }

    closes = [_as_float(item.get("close", 0.0)) for item in window[-8:]]
    highs = [_as_float(item.get("high", item.get("close", 0.0))) for item in window[-8:]]
    lows = [_as_float(item.get("low", item.get("close", 0.0))) for item in window[-8:]]
    base_close = max(abs(closes[-1]), 1e-9)

    deltas = [closes[index] - closes[index - 1] for index in range(1, len(closes))]
    move_sum = sum(deltas)
    abs_sum = sum(abs(value) for value in deltas)
    direction = _clip(move_sum / max(abs_sum, 1e-9), -1.0, 1.0)
    magnitude = _clip(abs_sum / max(base_close * 0.018, 1e-9))

    ranges = [max(0.0, high - low) for high, low in zip(highs, lows)]
    volatility = _clip((sum(ranges) / max(1, len(ranges))) / max(base_close * 0.012, 1e-9))
    acceleration = 0.0
    if len(deltas) >= 2:
        acceleration = _clip((deltas[-1] - deltas[-2]) / max(base_close * 0.006, 1e-9), -1.0, 1.0)

    missed_pressure = _clip(missed_count / 10.0)
    direction_blend = _clip((previous_direction * 0.42) + (direction * 0.58), -1.0, 1.0)
    acceleration_blend = _clip((previous_acceleration * 0.38) + (acceleration * 0.62), -1.0, 1.0)
    volatility_blend = _clip((previous_volatility * 0.48) + (volatility * 0.52))
    strength = _clip((previous_strength * 0.62) + (magnitude * 0.24) + (volatility * 0.10) + (missed_pressure * 0.12))
    pressure = _clip((previous_pressure * 0.58) + (magnitude * 0.20) + (volatility * 0.14) + (abs(acceleration) * 0.10) + (missed_pressure * 0.10))

    motion_label_pressures = {
        "motion_afterimage_forceful": float((pressure * 0.42) + (abs(direction_blend) * 0.26) + (strength * 0.18)),
        "motion_afterimage_unstable": float((volatility_blend * 0.48) + (abs(acceleration_blend) * 0.22) + ((1.0 - abs(direction_blend)) * 0.10)),
        "motion_afterimage_visible": float((strength * 0.48) + (pressure * 0.20) + ((1.0 - volatility_blend) * 0.12)),
        "motion_afterimage_faint": float(((1.0 - strength) * 0.22) + (strength * 0.20) + ((1.0 - pressure) * 0.16)),
        "motion_afterimage_neutral": float(((1.0 - pressure) * 0.24) + ((1.0 - volatility_blend) * 0.20) + ((1.0 - abs(direction_blend)) * 0.18)),
    }
    label = max(motion_label_pressures, key=motion_label_pressures.get)

    doppler = _derive_doppler_axes(
        previous_strength=previous_strength,
        previous_pressure=previous_pressure,
        previous_direction=previous_direction,
        previous_volatility=previous_volatility,
        previous_acceleration=previous_acceleration,
        strength=strength,
        pressure=pressure,
        direction=direction_blend,
        volatility=volatility_blend,
        acceleration=acceleration_blend,
    )

    return {
        "world_motion_afterimage_strength": float(strength),
        "world_motion_afterimage_pressure": float(pressure),
        "world_motion_afterimage_direction": float(direction_blend),
        "world_motion_afterimage_volatility": float(volatility_blend),
        "world_motion_afterimage_acceleration": float(acceleration_blend),
        "world_motion_afterimage_count": int(previous.get("world_motion_afterimage_count", 0) or 0) + motion_count,
        "world_motion_seen_count": int(previous.get("world_motion_seen_count", 0) or 0) + motion_count,
        "world_motion_afterimage_missed_count": int(previous.get("world_motion_afterimage_missed_count", 0) or 0) + missed_count,
        "world_motion_observation_kind": str(observation_kind),
        "world_motion_afterimage_label": str(label),
        "world_motion_afterimage_label_pressures": dict(motion_label_pressures),
        "world_motion_afterimage_last_timestamp": window[-1].get("timestamp"),
        **doppler,
    }


def build_world_motion_afterimage(previous_state=None, dropped_packet=None, *, dropped_count=1):
    return _build_world_motion_state(
        previous_state,
        dropped_packet,
        motion_count=max(1, int(dropped_count or 1)),
        missed_count=max(1, int(dropped_count or 1)),
        observation_kind="missed_world_tick",
    )


def build_world_motion_observation(previous_state=None, packet=None):
    return _build_world_motion_state(
        previous_state,
        packet,
        motion_count=1,
        missed_count=0,
        observation_kind="seen_world_tick",
    )
