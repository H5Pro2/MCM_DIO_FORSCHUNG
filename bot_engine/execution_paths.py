def run_runtime_execution_paths(bot, prepared_context, candle_state):
    if bot._run_existing_trade_execution_paths(prepared_context):
        return True

    if bot._run_entry_execution_path(prepared_context, candle_state):
        return True

    return True


def run_existing_trade_execution_paths(bot, prepared_context):
    if bot._run_position_execution_path(prepared_context):
        return True

    if bot._run_pending_execution_path(prepared_context):
        return True

    return False


def run_entry_execution_path(bot, prepared_context, candle_state):
    return bot._run_decision_execution_path(
        prepared_context,
        candle_state,
    )


def run_position_execution_path(bot, action_context):
    payload = bot._build_runtime_execution_payload(
        action_context,
    )
    return bot._handle_active_position(
        payload.get("window", []),
        payload.get("last", {}),
        bool(payload.get("live_mode", False)),
    )


def run_pending_execution_path(bot, action_context):
    payload = bot._build_runtime_execution_payload(
        action_context,
    )
    return bot._handle_pending_entry(
        payload.get("window", []),
        payload.get("last", {}),
        bool(payload.get("live_mode", False)),
    )


def run_decision_execution_path(bot, action_context, candle_state):
    payload = bot._build_runtime_execution_payload(
        action_context,
        candle_state=candle_state,
    )
    return bot._handle_entry_attempt(
        payload.get("window", []),
        dict(payload.get("candle_state", {}) or {}),
        payload.get("last", {}),
        bool(payload.get("live_mode", False)),
        bool(payload.get("external_order_active", False)),
    )
