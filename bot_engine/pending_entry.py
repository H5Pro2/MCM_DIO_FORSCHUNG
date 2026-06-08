def handle_pending_entry(
    bot,
    window,
    last,
    live_mode: bool,
    *,
    outcome_stimulus,
    episode_marker,
    cancelled_cause_consumer,
    order_cancel_func,
    active_order_snapshot_getter,
):
    if bot.pending_entry is None or bot.position is not None:
        return False

    pending_meta = dict(bot.pending_entry.get("meta", {}) or {})
    side = bot.pending_entry["side"]
    entry_price = bot.pending_entry["entry"]
    tp_price = bot.pending_entry["tp"]
    sl_price = bot.pending_entry["sl"]
    created = bot.pending_entry["created_index"]
    max_wait = bot.pending_entry["max_wait_bars"]

    high = float(last["high"])
    low = float(last["low"])
    trade_plan = dict(pending_meta.get("trade_plan", {}) or {})
    entry_validity_band = dict(trade_plan.get("entry_validity_band", {}) or {})

    validity_lower = entry_validity_band.get("lower")
    validity_upper = entry_validity_band.get("upper")

    try:
        validity_lower = float(validity_lower) if validity_lower is not None else None
    except Exception:
        validity_lower = None

    try:
        validity_upper = float(validity_upper) if validity_upper is not None else None
    except Exception:
        validity_upper = None

    entry_touched = low <= entry_price <= high
    validity_touched = False

    if validity_lower is not None and validity_upper is not None:
        validity_touched = high >= validity_lower and low <= validity_upper

    bars_open = max(0, int(bot.processed) - int(created))
    pending_risk = abs(float(entry_price) - float(sl_price))
    rr_value = 0.0
    if pending_risk > 0.0:
        if side == "LONG":
            rr_value = max(
                0.0,
                float(tp_price) - float(entry_price),
            ) / pending_risk
        else:
            rr_value = max(
                0.0,
                float(entry_price) - float(tp_price),
            ) / pending_risk

    distance_to_entry = 0.0
    if low <= entry_price <= high:
        distance_to_entry = 0.0
    elif entry_price < low:
        distance_to_entry = low - entry_price
    elif entry_price > high:
        distance_to_entry = entry_price - high

    fill_ratio = 0.0
    if pending_risk > 0.0:
        fill_ratio = max(0.0, min(2.0, 1.0 - (distance_to_entry / max(pending_risk, 1e-9))))

    meta_regulation_state = dict(getattr(bot, "meta_regulation_state", {}) or {})
    runtime_state = dict(getattr(bot, "mcm_runtime_decision_state", {}) or {})
    pending_state_before, pending_state_after, pending_state_delta = bot._capture_regulation_transition()

    pressure_to_capacity = 0.0
    if float(getattr(bot, "action_capacity", 0.0) or 0.0) > 0.0:
        pressure_to_capacity = float(getattr(bot, "regulatory_load", 0.0) or 0.0) / max(0.05, float(getattr(bot, "action_capacity", 0.0) or 0.0))

    episode_marker(
        bot,
        "pending_update",
        {
            "pending_entry": dict(bot.pending_entry or {}),
            "entry": float(entry_price),
            "tp": float(tp_price),
            "sl": float(sl_price),
            "risk": float(pending_risk),
            "rr": float(rr_value),
            "mfe": 0.0,
            "mae": 0.0,
            "bars_open": int(bars_open),
            "fill_ratio": float(fill_ratio),
            "regulatory_load": float(getattr(bot, "regulatory_load", 0.0) or 0.0),
            "action_capacity": float(getattr(bot, "action_capacity", 0.0) or 0.0),
            "recovery_need": float(getattr(bot, "recovery_need", 0.0) or 0.0),
            "survival_pressure": float(getattr(bot, "survival_pressure", 0.0) or 0.0),
            "pressure_to_capacity": float(pressure_to_capacity),
            "regulated_courage": float(meta_regulation_state.get("regulated_courage", 0.0) or 0.0),
            "courage_gap": float(meta_regulation_state.get("courage_gap", 0.0) or 0.0),
            "decision_tendency": str(runtime_state.get("decision_tendency", "hold") or "hold"),
            "proposed_decision": str(runtime_state.get("proposed_decision", "WAIT") or "WAIT"),
            "pre_action_phase": str(meta_regulation_state.get("pre_action_phase", "hold") or "hold"),
            "dominant_tension_cause": str(meta_regulation_state.get("dominant_tension_cause", "-") or "-"),
            "bearing_context": dict((pending_meta.get("bearing_context", {}) or {})),
            "felt_bearing_score": float(pending_meta.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(pending_meta.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "reason": "pending_watch",
            "state_before": dict(pending_state_before or {}),
            "state_after": dict(pending_state_after or {}),
            "state_delta": dict(pending_state_delta or {}),
        },
    )
    bot._commit_regulation_state_snapshot(pending_state_after)

    pending_order_id = bot.pending_entry.get("order_id")

    if live_mode and pending_order_id is not None:
        cancel_cause = cancelled_cause_consumer(pending_order_id)
        if cancel_cause is not None:
            cancel_snapshot = dict(bot.pending_entry or {})
            cancel_state_before = bot._build_regulation_state_snapshot()
            outcome_stimulus(bot, "cancel", bot.pending_entry)
            cancel_state_after = bot._build_regulation_state_snapshot()
            cancel_state_delta = bot._build_regulation_state_delta(
                cancel_state_before,
                cancel_state_after,
            )
            bot.stats.on_attempt(
                status="cancelled",
                context=pending_meta,
            )
            episode_marker(
                bot,
                "cancelled",
                {
                    "pending_entry": dict(cancel_snapshot or {}),
                    "reason": str(cancel_cause or "exchange_cancel"),
                    "bearing_context": dict((pending_meta.get("bearing_context", {}) or {})),
                    "felt_bearing_score": float(pending_meta.get("felt_bearing_score", 0.0) or 0.0),
                    "felt_profile_label": str(pending_meta.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                    "state_before": dict(cancel_state_before or {}),
                    "state_after": dict(cancel_state_after or {}),
                    "state_delta": dict(cancel_state_delta or {}),
                },
            )
            bot.stats.on_cancel(
                order_id=pending_order_id,
                cause=str(cancel_cause or "exchange_cancel"),
                exploration_trade=False,
                outcome_decomposition=dict(getattr(bot, "last_outcome_decomposition", {}) or {}),
                context=pending_meta,
            )
            bot._sync_last_outcome_decomposition_from_stats()
            bot._mark_memory_state_dirty()
            bot._commit_regulation_state_snapshot(cancel_state_after)
            bot.pending_entry = None
            return True

        live_snapshot = active_order_snapshot_getter()
        live_source = ""

        if isinstance(live_snapshot, dict):
            live_source = str(live_snapshot.get("source", "") or "").strip().lower()

        if live_source == "position_context":
            live_entry_price = float(live_snapshot.get("entry", entry_price) or entry_price)
            live_tp_price = float(live_snapshot.get("tp", tp_price) or tp_price)
            live_sl_price = float(live_snapshot.get("sl", sl_price) or sl_price)
            live_entry_ts = live_snapshot.get("entry_ts")

            if live_entry_ts is None:
                live_entry_ts = last.get("timestamp")

            live_position_meta = dict(pending_meta or {})
            live_position_meta["live_handoff"] = {
                "source": str(live_source or "position_context"),
                "order_id": bot.pending_entry.get("order_id"),
                "pending_order_id": bot.pending_entry.get("order_id"),
                "snapshot_id": live_snapshot.get("id"),
                "pending_side": str(side),
                "snapshot_side": str(live_snapshot.get("side", side) or side),
                "entry": float(live_entry_price),
                "tp": float(live_tp_price),
                "sl": float(live_sl_price),
                "entry_ts": live_entry_ts,
            }
            live_position_meta["execution_source"] = "live_position_context"

            return bot._finalize_pending_fill_handoff(
                side=str(live_snapshot.get("side", side) or side),
                entry_price=float(live_entry_price),
                tp_price=float(live_tp_price),
                sl_price=float(live_sl_price),
                entry_ts=live_entry_ts,
                order_id=bot.pending_entry.get("order_id"),
                position_meta=dict(live_position_meta or {}),
                reason="live_fill_handoff",
            )

        if (bot.processed - created) > max_wait:
            timeout_snapshot = dict(bot.pending_entry or {})
            cancel_sent = order_cancel_func(pending_order_id, cause="pending_timeout")

            if not cancel_sent:
                return True

            cancelled_cause_consumer(pending_order_id)

            timeout_state_before = bot._build_regulation_state_snapshot()
            outcome_stimulus(bot, "timeout", bot.pending_entry)
            timeout_state_after = bot._build_regulation_state_snapshot()
            timeout_state_delta = bot._build_regulation_state_delta(
                timeout_state_before,
                timeout_state_after,
            )
            bot.stats.on_attempt(
                status="timeout",
                context=pending_meta,
            )
            episode_marker(
                bot,
                "timeout",
                {
                    "pending_entry": dict(timeout_snapshot or {}),
                    "reason": "live_timeout",
                    "bearing_context": dict((pending_meta.get("bearing_context", {}) or {})),
                    "felt_bearing_score": float(pending_meta.get("felt_bearing_score", 0.0) or 0.0),
                    "felt_profile_label": str(pending_meta.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                    "state_before": dict(timeout_state_before or {}),
                    "state_after": dict(timeout_state_after or {}),
                    "state_delta": dict(timeout_state_delta or {}),
                },
            )
            bot.stats.on_cancel(
                order_id=pending_order_id,
                cause="pending_timeout",
                exploration_trade=False,
                outcome_decomposition=dict(getattr(bot, "last_outcome_decomposition", {}) or {}),
                context=pending_meta,
            )
            bot._sync_last_outcome_decomposition_from_stats()
            bot._mark_memory_state_dirty()
            bot._commit_regulation_state_snapshot(timeout_state_after)
            bot.pending_entry = None
            return True

        return True

    fill_price = float(entry_price)

    if (not entry_touched) and validity_touched:
        fill_price = float(min(max(entry_price, low), high))

    if side in ("LONG", "SHORT") and (entry_touched or validity_touched):
        return bot._finalize_pending_fill_handoff(
            side=str(side),
            entry_price=float(fill_price),
            tp_price=float(tp_price),
            sl_price=float(sl_price),
            entry_ts=last.get("timestamp"),
            order_id=None,
            position_meta=dict(pending_meta or {}),
            reason="backtest_fill",
        )

    if (bot.processed - created) > max_wait:

        pending_snapshot = dict(bot.pending_entry or {})
        timeout_state_before = bot._build_regulation_state_snapshot()
        outcome_stimulus(bot, "timeout", bot.pending_entry)
        timeout_state_after = bot._build_regulation_state_snapshot()
        timeout_state_delta = bot._build_regulation_state_delta(
            timeout_state_before,
            timeout_state_after,
        )
        bot.stats.on_attempt(
            status="timeout",
            context=pending_meta,
        )
        episode_marker(
            bot,
            "timeout",
            {
                "pending_entry": dict(pending_snapshot or {}),
                "reason": "backtest_timeout",
                "bearing_context": dict((pending_meta.get("bearing_context", {}) or {})),
                "felt_bearing_score": float(pending_meta.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(pending_meta.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "state_before": dict(timeout_state_before or {}),
                "state_after": dict(timeout_state_after or {}),
                "state_delta": dict(timeout_state_delta or {}),
            },
        )
        bot.stats.on_cancel(
            order_id=None,
            cause="backtest_timeout",
            exploration_trade=False,
            outcome_decomposition=dict(getattr(bot, "last_outcome_decomposition", {}) or {}),
            context=pending_meta,
        )
        bot._sync_last_outcome_decomposition_from_stats()

        bot._mark_memory_state_dirty()
        bot._commit_regulation_state_snapshot(timeout_state_after)
        bot.pending_entry = None
        return True

    return True
