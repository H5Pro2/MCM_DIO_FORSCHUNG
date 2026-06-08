def build_market_component_bundle(bot, window, base_packet=None):
    local_window = bot._normalize_market_window(window)
    if not local_window:
        return None

    item = dict(base_packet or {})
    timestamp = local_window[-1].get("timestamp")

    candle_state = dict(item.get("candle_state", {}) or {})
    tension_state = dict(item.get("tension_state", {}) or {})
    visual_market_state = dict(item.get("visual_market_state", {}) or {})
    structure_perception_state = dict(item.get("structure_perception_state", {}) or {})
    temporal_perception_state = dict(item.get("temporal_perception_state", {}) or {})
    world_motion_afterimage_state = dict(item.get("world_motion_afterimage_state", {}) or getattr(bot, "world_motion_afterimage_state", {}) or {})

    if not candle_state:
        candle_state = bot._build_candle_state_packet(local_window)

    if not tension_state:
        tension_state = bot._build_tension_state_packet(local_window)

    if not visual_market_state:
        visual_market_state = bot._build_visual_market_state_packet(local_window)

    if not structure_perception_state:
        structure_perception_state = bot._build_structure_perception_packet(local_window)

    if not temporal_perception_state:
        temporal_perception_state = dict(bot._build_temporal_perception_state(local_window) or {})

    if world_motion_afterimage_state:
        temporal_perception_state["world_motion_afterimage_state"] = dict(world_motion_afterimage_state)
        temporal_perception_state["world_motion_afterimage_strength"] = float(world_motion_afterimage_state.get("world_motion_afterimage_strength", 0.0) or 0.0)
        temporal_perception_state["world_motion_afterimage_pressure"] = float(world_motion_afterimage_state.get("world_motion_afterimage_pressure", 0.0) or 0.0)
        temporal_perception_state["world_motion_afterimage_direction"] = float(world_motion_afterimage_state.get("world_motion_afterimage_direction", 0.0) or 0.0)
        temporal_perception_state["motion_approach_pressure"] = float(world_motion_afterimage_state.get("motion_approach_pressure", 0.0) or 0.0)
        temporal_perception_state["motion_recession_pressure"] = float(world_motion_afterimage_state.get("motion_recession_pressure", 0.0) or 0.0)
        temporal_perception_state["contact_frequency_shift"] = float(world_motion_afterimage_state.get("contact_frequency_shift", 0.0) or 0.0)
        temporal_perception_state["afterimage_doppler_bias"] = float(world_motion_afterimage_state.get("afterimage_doppler_bias", 0.0) or 0.0)
        temporal_perception_state["future_variant_pressure"] = float(world_motion_afterimage_state.get("future_variant_pressure", 0.0) or 0.0)
        temporal_perception_state["afterimage_action_maturity"] = float(world_motion_afterimage_state.get("afterimage_action_maturity", 0.0) or 0.0)
        temporal_perception_state["afterimage_doppler_label"] = str(world_motion_afterimage_state.get("afterimage_doppler_label", "doppler_clear") or "doppler_clear")

    outer_market_state = bot._build_outer_market_state_packet(
        timestamp,
        candle_state=candle_state,
        tension_state=tension_state,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        temporal_perception_state=temporal_perception_state,
        world_motion_afterimage_state=world_motion_afterimage_state,
        base_state=dict(item.get("outer_market_state", {}) or {}),
    )

    return {
        "timestamp": timestamp,
        "window": list(local_window or []),
        "candle_state": dict(candle_state or {}),
        "tension_state": dict(tension_state or {}),
        "visual_market_state": dict(visual_market_state or {}),
        "structure_perception_state": dict(structure_perception_state or {}),
        "temporal_perception_state": dict(temporal_perception_state or {}),
        "world_motion_afterimage_state": dict(world_motion_afterimage_state or {}),
        "outer_market_state": dict(outer_market_state or {}),
    }


def build_market_perception_packet(bot, window):
    return bot._build_market_component_bundle(window)


def resolve_market_packet_payload(bot, packet):
    item = dict(packet or {})
    window = [dict(entry or {}) for entry in list(item.get("window", []) or []) if isinstance(entry, dict)]

    return bot._build_market_component_bundle(
        window,
        base_packet=item,
    )


def build_candle_state_packet(bot, window, *, candle_state_builder):
    local_window = bot._normalize_market_window(window)
    if not local_window:
        return {}

    last = local_window[-1]
    prev_close = local_window[-2].get("close") if len(local_window) > 1 else None
    return dict(candle_state_builder(last, prev_close=prev_close) or {})


def build_tension_state_packet(bot, window, *, tension_state_builder):
    local_window = bot._normalize_market_window(window)
    if not local_window:
        return {}

    return dict(tension_state_builder(local_window) or {})


def build_structure_perception_packet(bot, window, *, structure_engine):
    local_window = bot._normalize_market_window(window)
    if not local_window:
        return {}

    return dict(structure_engine.build_structure_perception_state(local_window) or {})


def build_visual_market_state_packet(bot, window, *, visual_market_state_builder):
    local_window = bot._normalize_market_window(window)
    if not local_window:
        return {}

    visual_state = dict(visual_market_state_builder(local_window) or {})
    bot._record_visual_cortex_protocol(local_window, visual_state)
    return dict(visual_state or {})


def build_temporal_perception_state(bot, window):
    previous_state = dict(getattr(bot, "temporal_perception_state", {}) or {})
    candles = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
    if len(candles) < 3:
        return {
            "flow_direction": float(previous_state.get("flow_direction", 0.0) or 0.0),
            "flow_strength": float(previous_state.get("flow_strength", 0.0) or 0.0),
            "flow_stability": float(previous_state.get("flow_stability", 0.0) or 0.0),
            "acceleration": 0.0,
            "swing_pressure": float(previous_state.get("swing_pressure", 0.0) or 0.0),
            "sequence_bias": str(previous_state.get("sequence_bias", "neutral") or "neutral"),
            "flow_memory": float(previous_state.get("flow_memory", 0.0) or 0.0),
            "transition_pressure": float(previous_state.get("transition_pressure", 0.0) or 0.0),
            "continuation_readiness": float(previous_state.get("continuation_readiness", 0.0) or 0.0),
            "temporal_exhaustion": float(previous_state.get("temporal_exhaustion", 0.0) or 0.0),
            "temporal_coherence": float(previous_state.get("temporal_coherence", 0.0) or 0.0),
            "state_drift": 0.0,
        }

    tail = candles[-12:]
    closes = [float(item.get("close", 0.0) or 0.0) for item in tail]
    highs = [float(item.get("high", 0.0) or 0.0) for item in tail]
    lows = [float(item.get("low", 0.0) or 0.0) for item in tail]

    deltas = []
    for index in range(1, len(closes)):
        deltas.append(float(closes[index] - closes[index - 1]))

    move_sum = sum(deltas)
    abs_sum = sum(abs(value) for value in deltas)
    raw_flow_direction = float(move_sum / max(abs_sum, 1e-9))
    raw_flow_strength = float(min(1.0, abs_sum / max(abs(closes[-1]) * 0.02, 1e-9)))

    direction_hits = 0
    for value in deltas:
        if move_sum >= 0.0 and value >= 0.0:
            direction_hits += 1
        elif move_sum < 0.0 and value <= 0.0:
            direction_hits += 1

    raw_flow_stability = float(direction_hits / max(1, len(deltas)))

    raw_acceleration = 0.0
    if len(deltas) >= 2:
        raw_acceleration = float(deltas[-1] - deltas[-2])

    range_span = max(max(highs) - min(lows), 1e-9)
    raw_swing_pressure = float(min(1.0, abs(raw_acceleration) / range_span))

    previous_direction = float(previous_state.get("flow_direction", 0.0) or 0.0)
    previous_strength = float(previous_state.get("flow_strength", 0.0) or 0.0)
    previous_stability = float(previous_state.get("flow_stability", 0.0) or 0.0)
    previous_swing_pressure = float(previous_state.get("swing_pressure", 0.0) or 0.0)
    previous_flow_memory = float(previous_state.get("flow_memory", 0.0) or 0.0)
    previous_transition_pressure = float(previous_state.get("transition_pressure", 0.0) or 0.0)
    previous_continuation_readiness = float(previous_state.get("continuation_readiness", 0.0) or 0.0)
    previous_temporal_exhaustion = float(previous_state.get("temporal_exhaustion", 0.0) or 0.0)
    previous_temporal_coherence = float(previous_state.get("temporal_coherence", 0.0) or 0.0)

    flow_direction = float((previous_direction * 0.34) + (raw_flow_direction * 0.66))
    flow_strength = float(min(1.0, max(0.0, (previous_strength * 0.26) + (raw_flow_strength * 0.74))))
    flow_stability = float(min(1.0, max(0.0, (previous_stability * 0.30) + (raw_flow_stability * 0.70))))
    swing_pressure = float(min(1.0, max(0.0, (previous_swing_pressure * 0.28) + (raw_swing_pressure * 0.72))))
    acceleration = float(raw_acceleration)

    state_drift = float(abs(flow_direction - previous_direction))
    direction_alignment = 1.0 - min(1.0, abs(flow_direction - previous_direction) / 2.0)
    flow_memory = float(max(-1.0, min(1.0, (previous_flow_memory * 0.58) + (flow_direction * 0.42))))
    transition_pressure = float(min(1.0, max(0.0, (previous_transition_pressure * 0.52) + (state_drift * 0.34) + (swing_pressure * 0.24) + (max(0.0, 1.0 - flow_stability) * 0.12))))
    continuation_readiness = float(min(1.0, max(0.0, (previous_continuation_readiness * 0.48) + (flow_strength * 0.24) + (flow_stability * 0.24) + (max(0.0, direction_alignment) * 0.16) - (transition_pressure * 0.18))))
    temporal_exhaustion = float(min(1.0, max(0.0, (previous_temporal_exhaustion * 0.62) + (swing_pressure * 0.20) + (max(0.0, abs(acceleration) / range_span) * 0.18) - (flow_stability * 0.10))))
    temporal_coherence = float(min(1.0, max(0.0, (previous_temporal_coherence * 0.34) + (flow_stability * 0.30) + (max(0.0, 1.0 - transition_pressure) * 0.22) + (max(0.0, 1.0 - temporal_exhaustion) * 0.14))))

    sequence_bias_pressures = {
        "up": float(max(0.0, flow_direction)),
        "down": float(max(0.0, -flow_direction)),
        "neutral": float(max(0.0, 1.0 - abs(flow_direction))),
    }
    sequence_bias = max(sequence_bias_pressures, key=sequence_bias_pressures.get)

    return {
        "flow_direction": float(flow_direction),
        "flow_strength": float(flow_strength),
        "flow_stability": float(flow_stability),
        "acceleration": float(acceleration),
        "swing_pressure": float(swing_pressure),
        "sequence_bias": str(sequence_bias),
        "sequence_bias_pressures": dict(sequence_bias_pressures),
        "flow_memory": float(flow_memory),
        "transition_pressure": float(transition_pressure),
        "continuation_readiness": float(continuation_readiness),
        "temporal_exhaustion": float(temporal_exhaustion),
        "temporal_coherence": float(temporal_coherence),
        "state_drift": float(state_drift),
    }


def apply_market_perception_state(bot, resolved_packet):
    item = dict(resolved_packet or {})
    if not item:
        return None

    bot.current_timestamp = item.get("timestamp", None)
    bot.tension_state = dict(item.get("tension_state", {}) or {})
    bot.visual_market_state = dict(item.get("visual_market_state", {}) or {})
    bot.structure_perception_state = dict(item.get("structure_perception_state", {}) or {})
    bot.temporal_perception_state = dict(item.get("temporal_perception_state", {}) or {})
    bot.world_motion_afterimage_state = dict(item.get("world_motion_afterimage_state", {}) or getattr(bot, "world_motion_afterimage_state", {}) or {})
    bot.outer_market_state = dict(item.get("outer_market_state", {}) or {})
    return dict(item)
