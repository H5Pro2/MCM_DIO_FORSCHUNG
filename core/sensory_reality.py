def _clip(value: float, low: float, high: float) -> float:
    return max(float(low), min(float(high), float(value)))


def build_sensory_reality_state(
    expansion: float,
    body_pressure: float,
    wick_pressure: float,
    volume_bias: float,
    range_position: float,
    short_impulse: float,
    mid_impulse: float,
    breakout_tension: float,
    edge_strength: float,
    fracture: float,
    visual_form_novelty: float,
) -> dict:
    """Verdichtet verwandte Aussenreize zu einer gemeinsamen Realitaetslage."""

    raw_values = [
        max(0.0, float(expansion or 0.0)),
        max(0.0, float(body_pressure or 0.0)),
        abs(float(volume_bias or 0.0)),
        abs(float(range_position or 0.0)),
        max(0.0, float(breakout_tension or 0.0)),
        max(0.0, float(edge_strength or 0.0)),
        max(0.0, float(fracture or 0.0)),
        max(0.0, float(visual_form_novelty or 0.0)),
    ]
    active_pressure_values = [_clip((value - 0.18) / 0.82, 0.0, 1.0) for value in raw_values]
    active_count_pressure = sum(active_pressure_values)
    active_count = int(round(active_count_pressure))
    active_mean = sum(value * pressure for value, pressure in zip(raw_values, active_pressure_values)) / max(1e-9, active_count_pressure)
    primary_pressure = max(raw_values) if raw_values else 0.0

    sensory_redundancy = _clip(
        (max(0, active_count - 1) / 6.0) * active_mean,
        0.0,
        1.0,
    )
    sensory_gate = _clip(1.0 - (sensory_redundancy * 0.34), 0.58, 1.0)
    sensory_load = _clip(
        (primary_pressure * 0.50)
        + (active_mean * 0.22)
        + (abs(float(short_impulse or 0.0) - float(mid_impulse or 0.0)) * 0.10)
        + (max(0.0, float(wick_pressure or 0.0) - 0.50) * 0.08)
        - (sensory_redundancy * 0.14),
        0.0,
        1.0,
    )
    sensory_habituation = _clip(
        (sensory_redundancy * 0.56)
        + (active_mean * 0.18)
        + (max(0.0, primary_pressure - sensory_load) * 0.18),
        0.0,
        1.0,
    )
    sensory_reality_pressure = _clip(
        (primary_pressure * 0.62)
        + (sensory_load * 0.30)
        - (sensory_redundancy * 0.18),
        0.0,
        1.0,
    )

    sensory_reality_pressures = {
        "redundant_outer_reality": _clip((sensory_redundancy * 0.42) + (active_count_pressure / 8.0 * 0.18), 0.0, 1.0),
        "intense_outer_reality": _clip((sensory_reality_pressure * 0.42) + (primary_pressure * 0.18), 0.0, 1.0),
        "quiet_outer_reality": _clip(((1.0 - sensory_load) * 0.34) + ((1.0 - primary_pressure) * 0.16), 0.0, 1.0),
        "clear_outer_reality": _clip((sensory_gate * 0.24) + ((1.0 - sensory_redundancy) * 0.16) + (sensory_reality_pressure * 0.10), 0.0, 1.0),
    }
    label = max(sensory_reality_pressures, key=sensory_reality_pressures.get)

    return {
        "sensory_reality_pressure": float(sensory_reality_pressure),
        "sensory_load": float(sensory_load),
        "sensory_redundancy": float(sensory_redundancy),
        "sensory_habituation": float(sensory_habituation),
        "sensory_gate": float(sensory_gate),
        "sensory_active_axis_count": int(active_count),
        "sensory_active_axis_pressure": float(active_count_pressure),
        "sensory_primary_pressure": float(primary_pressure),
        "sensory_reality_label": str(label),
        "sensory_reality_pressures": dict(sensory_reality_pressures),
    }
