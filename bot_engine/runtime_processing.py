def compose_runtime_perception_packet(bot, perception_packet, *, candle_state=None, visual_market_state=None, structure_perception_state=None):
    return bot._build_runtime_market_packet(
        perception_packet,
        candle_state=candle_state,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
    )


def advance_runtime_from_resolved_packet(bot, resolved_packet, *, runtime_stepper):
    item = dict(resolved_packet or {})
    local_window = [dict(entry or {}) for entry in list(item.get("window", []) or []) if isinstance(entry, dict)]
    if not local_window:
        return None

    resolved_candle_state = dict(item.get("candle_state", {}) or {})
    resolved_tension_state = dict(item.get("tension_state", {}) or {})
    resolved_visual_market_state = dict(item.get("visual_market_state", {}) or {})
    resolved_structure_perception_state = dict(item.get("structure_perception_state", {}) or {})
    resolved_temporal_perception_state = dict(item.get("temporal_perception_state", {}) or {})

    return runtime_stepper(
        local_window,
        dict(resolved_candle_state or {}),
        bot=bot,
        tension_state=dict(resolved_tension_state or {}),
        visual_market_state=dict(resolved_visual_market_state or {}),
        structure_perception_state=dict(resolved_structure_perception_state or {}),
        temporal_perception_state=dict(resolved_temporal_perception_state or {}),
    )


def run_runtime_packet_action_cycle(bot, resolved_packet, seed_runtime=False):
    item = dict(resolved_packet or {})
    local_window = [dict(entry or {}) for entry in list(item.get("window", []) or []) if isinstance(entry, dict)]
    if not local_window:
        return None

    resolved_candle_state = dict(item.get("candle_state", {}) or {})

    if seed_runtime:
        bot._ensure_memory_state_loaded()

    bot._apply_market_perception_state(item)

    runtime_result = bot._advance_runtime_from_resolved_packet(
        item,
    )

    if seed_runtime:
        bot._runtime_seeded = True

    action_result = bot._run_runtime_action_cycle(
        local_window,
        dict(resolved_candle_state or {}),
    )
    if action_result is None:
        return runtime_result

    return action_result


def seed_runtime_window(bot, resolved_packet):
    return run_runtime_packet_action_cycle(
        bot,
        resolved_packet,
        seed_runtime=True,
    )


def build_prepared_runtime_action_context(bot, window):
    action_context = bot._build_runtime_action_context(window)
    if action_context is None:
        return None

    return bot._prepare_runtime_action_context(
        action_context,
    )


def process_market_packet(bot, packet):
    resolved_packet = bot._resolve_market_packet_payload(packet)
    if resolved_packet is None:
        return None

    window = [dict(entry or {}) for entry in list(resolved_packet.get("window", []) or []) if isinstance(entry, dict)]
    candle_state = dict(resolved_packet.get("candle_state", {}) or {})
    visual_market_state = dict(resolved_packet.get("visual_market_state", {}) or {})
    structure_perception_state = dict(resolved_packet.get("structure_perception_state", {}) or {})

    if not bot._runtime_seeded:
        result = bot._seed_runtime_window(
            resolved_packet,
        )
    else:
        result = bot._process_runtime_packet(
            window,
            candle_state,
            visual_market_state=visual_market_state,
            structure_perception_state=structure_perception_state,
        )

    bot._finalize_market_packet_processing(resolved_packet)
    return result


def process_runtime_packet(bot, window, candle_state, *, visual_market_state=None, structure_perception_state=None):
    runtime_packet = bot._build_current_runtime_packet(
        window,
        candle_state,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
    )
    if runtime_packet is None:
        return None

    return run_runtime_packet_action_cycle(
        bot,
        runtime_packet,
        seed_runtime=False,
    )


def finalize_market_packet_processing(bot, resolved_packet):
    item = dict(resolved_packet or {})
    window = [dict(entry or {}) for entry in list(item.get("window", []) or []) if isinstance(entry, dict)]
    if not window:
        return None

    candle_state = dict(item.get("candle_state", {}) or {})

    bot._write_visualization_snapshots(
        window,
        candle_state,
    )

    bot.processed += 1
    return True
