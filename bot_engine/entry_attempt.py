def handle_entry_attempt(
    bot,
    window,
    candle_state,
    last,
    live_mode: bool,
    external_order_active: bool,
    *,
    config,
    debug_enabled,
    debug_writer,
    entry_decision_evaluator,
    order_placer,
    outcome_stimulus,
    episode_marker,
):
    if bot.position is not None or bot.pending_entry is not None:
        return False

    if external_order_active:
        skip_state_before, skip_state_after, skip_state_delta = bot._capture_regulation_transition()
        return bot._finalize_entry_attempt_abandoned(
            {
                "decision_tendency": "hold",
                "proposed_decision": "WAIT",
                "rejection_reason": "external_order_active",
            },
            reason="external_order_active",
            state_before=skip_state_before,
            state_after=skip_state_after,
            state_delta=skip_state_delta,
        )

    if int(getattr(bot, "mcm_pause_left", 0) or 0) > 0:
        bot.mcm_pause_left -= 1

    entry_result = entry_decision_evaluator(
        bot,
        window,
        candle_state,
    )

    if entry_result is None:
        skip_state_before, skip_state_after, skip_state_delta = bot._capture_regulation_transition()
        return bot._finalize_entry_attempt_abandoned(
            {
                "decision_tendency": "hold",
                "proposed_decision": "WAIT",
                "rejection_reason": "entry_result_missing",
            },
            reason="entry_result_missing",
            state_before=skip_state_before,
            state_after=skip_state_after,
            state_delta=skip_state_delta,
        )

    entry_world_state = dict(entry_result.get("world_state", {}) or {})
    entry_world_state["candle_state"] = dict(candle_state or {})
    try:
        entry_world_state["current_price"] = float(candle_state.get("close", last.get("close", 0.0)) or 0.0)
    except Exception:
        entry_world_state["current_price"] = 0.0
    entry_result["world_state"] = dict(entry_world_state)

    bot.action_intent_state = dict(entry_result.get("action_intent_state", {}) or {})
    bot.execution_state = dict(entry_result.get("execution_state", {}) or {})

    if bot._handle_decision_tendency(entry_result):
        return True

    bot.execution_state = {
        **dict(bot.execution_state or {}),
        "execution_phase": "value_check",
        "execution_ready": True,
        "execution_blocked": False,
    }

    value_check = bot.value_gate.evaluate(entry_result)

    if debug_enabled:
        debug_writer(f"VALUE_GATE: {value_check}", "value_check_debug.csv")

    if not value_check.get("trade_allowed", False):
        bot.execution_state = {
            **dict(bot.execution_state or {}),
            "execution_phase": "blocked_value_gate",
            "execution_ready": False,
            "execution_blocked": True,
        }
        blocked_state_before = bot._build_regulation_state_snapshot()
        outcome_stimulus(
            bot,
            value_check.get("reason"),
            entry_result,
        )
        blocked_state_after = bot._build_regulation_state_snapshot()
        blocked_state_delta = bot._build_regulation_state_delta(
            blocked_state_before,
            blocked_state_after,
        )
        blocked_context = bot._build_entry_attempt_context(
            entry_result,
            state_before=blocked_state_before,
            state_after=blocked_state_after,
            state_delta=blocked_state_delta,
        )

        bot.stats.on_attempt(
            status="blocked_value_gate",
            context=blocked_context,
        )
        episode_marker(
            bot,
            "blocked_value_gate",
            {
                "trade_plan": dict((blocked_context.get("trade_plan", {}) or {})),
                "reason": str(value_check.get("reason") or "blocked_value_gate"),
                "bearing_context": dict((blocked_context.get("bearing_context", {}) or {})),
                "felt_bearing_score": float(blocked_context.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(blocked_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "state_before": dict(blocked_state_before or {}),
                "state_after": dict(blocked_state_after or {}),
                "state_delta": dict(blocked_state_delta or {}),
            },
        )
        bot._mark_memory_state_dirty()
        bot._commit_regulation_state_snapshot(blocked_state_after)
        return True

    side = str(entry_result.get("decision", "")).upper().strip()
    entry_price = float(entry_result.get("entry_price", 0.0) or 0.0)
    tp_price = float(entry_result.get("tp_price", 0.0) or 0.0)
    sl_price = float(entry_result.get("sl_price", 0.0) or 0.0)
    risk = abs(entry_price - sl_price)

    if side not in ("LONG", "SHORT"):
        invalid_state_before, invalid_state_after, invalid_state_delta = bot._capture_regulation_transition()
        return bot._finalize_entry_attempt_abandoned(
            {
                **dict(entry_result or {}),
                "rejection_reason": "invalid_trade_direction",
            },
            reason="invalid_trade_direction",
            state_before=invalid_state_before,
            state_after=invalid_state_after,
            state_delta=invalid_state_delta,
        )

    if entry_price <= 0.0 or tp_price <= 0.0 or sl_price <= 0.0 or risk <= 0.0:
        invalid_state_before, invalid_state_after, invalid_state_delta = bot._capture_regulation_transition()
        return bot._finalize_entry_attempt_abandoned(
            {
                **dict(entry_result or {}),
                "rejection_reason": "invalid_trade_geometry",
            },
            reason="invalid_trade_geometry",
            state_before=invalid_state_before,
            state_after=invalid_state_after,
            state_delta=invalid_state_delta,
        )

    order_side = "sell" if side == "SHORT" else "buy"

    order_id = None
    is_memory_trade = False
    rr_exec_min = float(getattr(config, "RR_EXECUTION_MIN", 1.2) or 1.2)

    bot.execution_state = {
        **dict(bot.execution_state or {}),
        "execution_phase": "execution_prepare",
        "execution_ready": True,
        "execution_blocked": False,
    }

    if live_mode and config.AKTIV_ORDER and float(entry_result.get("rr_value", 0.0) or 0.0) < rr_exec_min:
        is_memory_trade = True

    if live_mode and config.AKTIV_ORDER and not is_memory_trade:
        order_id = order_placer(
            order_type=order_side,
            price=entry_price,
            amount=config.ORDER_SIZE,
            open_orders=None,
            tp=tp_price,
            sl=sl_price,
            params={
                "_entry_reference": entry_price,
                "_entry_distance": abs(entry_price - float(last.get("close", entry_price) or entry_price)),
                "_risk_reference": risk,
                "_entry_validity_band": dict(entry_result.get("entry_validity_band", {}) or {}),
            },
        )

        if order_id is None:
            failed_state_before, failed_state_after, failed_state_delta = bot._capture_regulation_transition()
            return bot._finalize_entry_attempt_abandoned(
                {
                    **dict(entry_result or {}),
                    "rejection_reason": "order_submit_failed",
                },
                reason="order_submit_failed",
                state_before=failed_state_before,
                state_after=failed_state_after,
                state_delta=failed_state_delta,
            )

    submitted_state_before, submitted_state_after, submitted_state_delta = bot._capture_regulation_transition()
    return bot._finalize_entry_attempt_submission(
        entry_result=dict(entry_result or {}),
        side=side,
        entry_price=entry_price,
        tp_price=tp_price,
        sl_price=sl_price,
        risk=float(risk),
        order_id=order_id,
        state_before=submitted_state_before,
        state_after=submitted_state_after,
        state_delta=submitted_state_delta,
    )
