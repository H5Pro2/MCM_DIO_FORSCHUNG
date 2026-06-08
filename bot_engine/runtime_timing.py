def runtime_dynamic_load(bot):
    dynamic_load = max(
        float(getattr(bot, "focus_confidence", 0.0) or 0.0),
        float(getattr(bot, "target_lock", 0.0) or 0.0),
        float(getattr(bot, "last_signal_relevance", 0.0) or 0.0),
        abs(float(getattr(bot, "competition_bias", 0.0) or 0.0)),
    )

    if bot.position is not None:
        dynamic_load = max(dynamic_load, 1.0)
    elif bot.pending_entry is not None:
        dynamic_load = max(dynamic_load, 0.82)
    elif bool(getattr(bot, "observation_mode", False)):
        dynamic_load = max(dynamic_load, 0.68)

    return float(max(0.0, min(1.0, float(dynamic_load))))


def runtime_idle_sleep_seconds(bot, *, config, dynamic_load_func):
    cognitive_seconds = max(
        0.0,
        float(getattr(config, "GLOBAL_COGNITIVE_REACTION_SECONDS", 0.001) or 0.0),
    )
    world_seconds = max(
        cognitive_seconds,
        float(getattr(config, "WORLD_TIME_SECONDS", cognitive_seconds) or cognitive_seconds),
    )

    if str(getattr(config, "MODE", "") or "").strip().upper() == "BACKTEST":
        return float(cognitive_seconds)

    min_sleep = float(cognitive_seconds)
    max_sleep = max(min_sleep, min(float(world_seconds), float(cognitive_seconds) * 8.0))

    queue_depth = int(bot._market_packet_queue.qsize() or 0)
    if queue_depth > 0:
        return float(min_sleep)

    dynamic_load = dynamic_load_func()
    sleep_span = max_sleep - min_sleep
    return float(max_sleep - (sleep_span * dynamic_load))


def runtime_idle_cycles(bot, *, config, dynamic_load_func):
    base_cycles = max(
        1,
        int(
            getattr(
                config,
                "MCM_INNER_IDLE_BASE_TICKS",
                1,
            ) or 1
        ),
    )
    max_cycles = max(
        base_cycles,
        int(
            getattr(
                config,
                "MCM_INNER_IDLE_MAX_TICKS",
                base_cycles,
            ) or base_cycles
        ),
    )

    dynamic_load = dynamic_load_func()
    cycle_boost = 0

    if bot.position is not None:
        cycle_boost += 2
    elif bot.pending_entry is not None:
        cycle_boost += 1

    if bool(getattr(bot, "observation_mode", False)):
        cycle_boost += 1

    cycle_boost += int(round(dynamic_load * max(0, max_cycles - base_cycles)))
    return int(min(max_cycles, base_cycles + cycle_boost))


def runtime_market_followup_cycles(bot, *, config, dynamic_load_func):
    configured_cycles = max(
        1,
        int(
            getattr(
                config,
                "MCM_INNER_TICKS_PER_WORLD_TICK",
                1,
            ) or 1
        ),
    )

    followup_cycles = max(0, configured_cycles - 1)
    if followup_cycles <= 0:
        return 0

    dynamic_load = dynamic_load_func()
    scaled_cycles = int(round(dynamic_load * followup_cycles))
    return int(max(0, min(followup_cycles, scaled_cycles if followup_cycles > 1 else followup_cycles)))
