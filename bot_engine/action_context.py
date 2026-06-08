def resolve_runtime_action_window_state(action_context):
    context = dict(action_context or {})
    window = [dict(item or {}) for item in list(context.get("window", []) or []) if isinstance(item, dict)]

    if not window:
        return None

    timestamp = context.get("timestamp", window[-1].get("timestamp"))
    last = dict(context.get("last", window[-1]) or window[-1])

    return {
        "context": dict(context or {}),
        "window": list(window or []),
        "timestamp": timestamp,
        "last": dict(last or {}),
    }


def build_runtime_action_context_flags(bot, *, config, is_order_active_func, debug_enabled, dbr_debug_func):
    live_mode = str(getattr(config, "MODE", "LIVE")).upper() == "LIVE"
    external_order_active = False

    if live_mode and bot.position is None and is_order_active_func():
        external_order_active = True
        if debug_enabled:
            dbr_debug_func("RUNTIME: ORDER_ACTIVE_WATCH", "live_backtest_debug.csv")

    return {
        "live_mode": bool(live_mode),
        "external_order_active": bool(external_order_active),
        "outer_market_state": dict(getattr(bot, "outer_market_state", {}) or {}),
    }


def resolve_runtime_action_context_state(action_context, *, window_state_resolver):
    resolved_state = window_state_resolver(action_context)
    if resolved_state is None:
        return None

    context = dict(resolved_state.get("context", {}) or {})
    return {
        "context": dict(context or {}),
        "window": list(resolved_state.get("window", []) or []),
        "last": dict(resolved_state.get("last", {}) or {}),
        "timestamp": resolved_state.get("timestamp", None),
        "live_mode": bool(context.get("live_mode", False)),
        "external_order_active": bool(context.get("external_order_active", False)),
        "outer_market_state": dict(context.get("outer_market_state", {}) or {}),
    }


def build_runtime_action_payload_state(action_context, *, candle_state=None, allow_empty=False, context_state_resolver):
    resolved_context = context_state_resolver(action_context)
    if resolved_context is None:
        if not bool(allow_empty):
            return None

        return {
            "window": [],
            "last": {},
            "timestamp": None,
            "live_mode": False,
            "external_order_active": False,
            "outer_market_state": {},
            "candle_state": dict(candle_state or {}),
        }

    return {
        "window": list(resolved_context.get("window", []) or []),
        "last": dict(resolved_context.get("last", {}) or {}),
        "timestamp": resolved_context.get("timestamp", None),
        "live_mode": bool(resolved_context.get("live_mode", False)),
        "external_order_active": bool(resolved_context.get("external_order_active", False)),
        "outer_market_state": dict(resolved_context.get("outer_market_state", {}) or {}),
        "candle_state": dict(candle_state or {}),
    }


def build_runtime_action_context(window, *, flags_builder):
    if not window:
        return None

    local_window = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
    if not local_window:
        return None

    last = local_window[-1]
    timestamp = last.get("timestamp")
    context_flags = flags_builder()

    return {
        "window": local_window,
        "last": last,
        "timestamp": timestamp,
        "live_mode": bool(context_flags.get("live_mode", False)),
        "external_order_active": bool(context_flags.get("external_order_active", False)),
        "outer_market_state": dict(context_flags.get("outer_market_state", {}) or {}),
    }


def normalize_runtime_action_context(action_context, *, payload_state_builder):
    payload_state = payload_state_builder(
        action_context,
        allow_empty=False,
    )
    if payload_state is None:
        return None

    return {
        "window": list(payload_state.get("window", []) or []),
        "last": dict(payload_state.get("last", {}) or {}),
        "timestamp": payload_state.get("timestamp", None),
        "live_mode": bool(payload_state.get("live_mode", False)),
        "external_order_active": bool(payload_state.get("external_order_active", False)),
        "outer_market_state": dict(payload_state.get("outer_market_state", {}) or {}),
    }


def apply_runtime_action_state(bot, action_context, *, window_state_resolver):
    resolved_state = window_state_resolver(action_context)
    if resolved_state is None:
        return None

    context = dict(resolved_state.get("context", {}) or {})
    timestamp = resolved_state.get("timestamp", None)

    if bot.position and bot.position.get("entry_ts") is None:
        bot.position["entry_ts"] = timestamp
        bot.position["last_checked_ts"] = timestamp

    bot.current_timestamp = timestamp
    bot.stats.data["current_timestamp"] = bot.current_timestamp
    return dict(context or {})


def build_runtime_execution_payload(bot, action_context, *, candle_state=None):
    payload_state = bot._build_runtime_action_payload_state(
        action_context,
        candle_state=candle_state,
        allow_empty=True,
    )

    return {
        "window": list(payload_state.get("window", []) or []),
        "last": dict(payload_state.get("last", {}) or {}),
        "live_mode": bool(payload_state.get("live_mode", False)),
        "external_order_active": bool(payload_state.get("external_order_active", False)),
        "candle_state": dict(payload_state.get("candle_state", {}) or {}),
    }


def prepare_runtime_action_context(bot, action_context):
    normalized_context = bot._normalize_runtime_action_context(
        action_context,
    )
    if normalized_context is None:
        return None

    return bot._apply_runtime_action_state(
        normalized_context,
    )


def run_runtime_action_cycle(bot, window, candle_state):
    bot._ensure_memory_state_loaded()

    prepared_context = bot._build_prepared_runtime_action_context(window)
    if prepared_context is None:
        return None

    return bot._run_runtime_execution_paths(
        prepared_context,
        candle_state,
    )
