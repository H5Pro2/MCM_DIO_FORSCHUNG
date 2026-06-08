# ==================================================
# bot_engine/market_packets.py
# Market/runtime packet shaping helpers
# ==================================================


def normalize_market_window(window):
    if not window:
        return []

    return [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]


def build_outer_market_state_packet(
    timestamp,
    candle_state=None,
    tension_state=None,
    visual_market_state=None,
    structure_perception_state=None,
    temporal_perception_state=None,
    world_motion_afterimage_state=None,
    base_state=None,
):
    return {
        **dict(base_state or {}),
        "timestamp": timestamp,
        "candle_state": dict(candle_state or {}),
        "tension_state": dict(tension_state or {}),
        "visual_market_state": dict(visual_market_state or {}),
        "structure_perception_state": dict(structure_perception_state or {}),
        "temporal_perception_state": dict(temporal_perception_state or {}),
        "world_motion_afterimage_state": dict(world_motion_afterimage_state or {}),
    }


def build_runtime_market_packet(
    packet,
    *,
    outer_market_state_builder,
    candle_state=None,
    visual_market_state=None,
    structure_perception_state=None,
    tension_state=None,
    temporal_perception_state=None,
):
    item = dict(packet or {})
    if not item:
        return None

    resolved_window = normalize_market_window(item.get("window", []) or [])
    if not resolved_window:
        return None

    resolved_timestamp = item.get("timestamp", None)
    resolved_candle_state = dict(item.get("candle_state", {}) or {})
    resolved_tension_state = dict(item.get("tension_state", {}) or {})
    resolved_visual_market_state = dict(item.get("visual_market_state", {}) or {})
    resolved_structure_perception_state = dict(item.get("structure_perception_state", {}) or {})
    resolved_temporal_perception_state = dict(item.get("temporal_perception_state", {}) or {})
    resolved_world_motion_afterimage_state = dict(item.get("world_motion_afterimage_state", {}) or {})

    if candle_state is not None:
        resolved_candle_state = dict(candle_state or {})

    if tension_state is not None:
        resolved_tension_state = dict(tension_state or {})

    if visual_market_state is not None:
        resolved_visual_market_state = dict(visual_market_state or {})

    if structure_perception_state is not None:
        resolved_structure_perception_state = dict(structure_perception_state or {})

    if temporal_perception_state is not None:
        resolved_temporal_perception_state = dict(temporal_perception_state or {})

    resolved_outer_market_state = outer_market_state_builder(
        resolved_timestamp,
        candle_state=resolved_candle_state,
        tension_state=resolved_tension_state,
        visual_market_state=resolved_visual_market_state,
        structure_perception_state=resolved_structure_perception_state,
        temporal_perception_state=resolved_temporal_perception_state,
        world_motion_afterimage_state=resolved_world_motion_afterimage_state,
        base_state=dict(item.get("outer_market_state", {}) or {}),
    )

    return {
        "timestamp": resolved_timestamp,
        "window": normalize_market_window(resolved_window),
        "candle_state": dict(resolved_candle_state or {}),
        "tension_state": dict(resolved_tension_state or {}),
        "visual_market_state": dict(resolved_visual_market_state or {}),
        "structure_perception_state": dict(resolved_structure_perception_state or {}),
        "temporal_perception_state": dict(resolved_temporal_perception_state or {}),
        "world_motion_afterimage_state": dict(resolved_world_motion_afterimage_state or {}),
        "outer_market_state": dict(resolved_outer_market_state or {}),
    }


def build_live_market_packet_key(packet):
    window = normalize_market_window((packet or {}).get("window", []) or [])
    if not window:
        return None

    first = dict(window[0] or {})
    last = dict(window[-1] or {})
    tail = []

    for item in window[-3:]:
        row = dict(item or {})
        tail.append(
            (
                int(float(row.get("timestamp", 0) or 0)),
                round(float(row.get("open", 0.0) or 0.0), 8),
                round(float(row.get("high", 0.0) or 0.0), 8),
                round(float(row.get("low", 0.0) or 0.0), 8),
                round(float(row.get("close", 0.0) or 0.0), 8),
                round(float(row.get("volume", 0.0) or 0.0), 8),
            )
        )

    return (
        int(float(last.get("timestamp", (packet or {}).get("timestamp", 0)) or 0)),
        int(float(first.get("timestamp", 0) or 0)),
        len(window),
        tuple(tail),
    )


def is_duplicate_live_market_packet(
    bot,
    packet,
    *,
    config,
    key_builder=build_live_market_packet_key,
    debug_writer=None,
):
    if str(getattr(config, "MODE", "LIVE")).upper() != "LIVE":
        return False

    if not bool(getattr(config, "LIVE_MARKET_PACKET_DEDUPE_ENABLED", True)):
        return False

    key = key_builder(packet)
    if key is None:
        return False

    if key != bot._last_live_market_packet_key:
        bot._last_live_market_packet_key = key
        bot._live_duplicate_market_packet_skips = 0
        return False

    bot._live_duplicate_market_packet_skips = int(getattr(bot, "_live_duplicate_market_packet_skips", 0) or 0) + 1
    every_n = max(1, int(getattr(config, "LIVE_MARKET_PACKET_DEDUPE_LOG_EVERY_N", 25) or 25))
    if debug_writer is not None and (
        bot._live_duplicate_market_packet_skips == 1
        or (bot._live_duplicate_market_packet_skips % every_n) == 0
    ):
        debug_writer(
            f"LIVE_MARKET_PACKET_DEDUPE | skipped={bot._live_duplicate_market_packet_skips} timestamp={key[0]} tail={key[1]}",
            "mcm_live_market_dedupe.csv",
        )
    return True
