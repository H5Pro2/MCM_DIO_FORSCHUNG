def finalize_pending_fill_handoff(bot, side, entry_price, tp_price, sl_price, entry_ts, order_id, position_meta, reason, *, episode_marker):
    fill_state_before = bot._build_regulation_state_snapshot()
    fill_risk = abs(float(entry_price) - float(sl_price))

    position_context = dict(position_meta or {})
    position_context["handoff_reason"] = str(reason or "pending_fill_handoff")
    position_context["felt_bearing_score"] = float(position_context.get("felt_bearing_score", 0.0) or 0.0)
    position_context["felt_profile_label"] = str(position_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear")
    position_context["bearing_context"] = dict(position_context.get("bearing_context", {}) or {})

    bot.execution_state = {
        **dict(bot.execution_state or {}),
        "execution_phase": "position_active",
        "execution_ready": True,
        "execution_blocked": False,
    }

    bot.position = {
        "side": str(side),
        "entry": float(entry_price),
        "tp": float(tp_price),
        "sl": float(sl_price),
        "mfe": 0.0,
        "mae": 0.0,
        "risk": float(fill_risk),
        "order_id": order_id,
        "entry_ts": entry_ts,
        "entry_index": bot.processed,
        "last_checked_ts": entry_ts,
        "meta": dict(position_context or {}),
    }

    fill_state_after = bot._build_regulation_state_snapshot()
    fill_state_delta = bot._build_regulation_state_delta(
        fill_state_before,
        fill_state_after,
    )

    bot.pending_entry = None
    bot.stats.on_attempt(
        status="filled",
        context=position_context,
    )
    episode_marker(
        bot,
        "filled",
        {
            "position": dict(bot.position or {}),
            "reason": str(reason or "pending_fill_handoff"),
            "bearing_context": dict((position_context.get("bearing_context", {}) or {})),
            "felt_bearing_score": float(position_context.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(position_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "state_before": dict(fill_state_before or {}),
            "state_after": dict(fill_state_after or {}),
            "state_delta": dict(fill_state_delta or {}),
        },
    )
    bot._mark_memory_state_dirty()
    bot._commit_regulation_state_snapshot(fill_state_after)
    return True


def handle_decision_tendency(bot, entry_result, *, episode_marker):
    result = dict(entry_result or {})
    decision_tendency = str(result.get("decision_tendency", "") or "").strip().lower()

    bot.action_intent_state = dict(result.get("action_intent_state", {}) or {})
    bot.execution_state = dict(result.get("execution_state", {}) or {})

    if decision_tendency == "act":
        return False

    if decision_tendency == "observe":
        event_name = "observed_only"
    elif decision_tendency == "replan":
        event_name = "replanned"
    else:
        event_name = "withheld"

    state_before, state_after, state_delta = bot._capture_regulation_transition()

    non_action_context = bot._build_entry_attempt_context(
        result,
        state_before=state_before,
        state_after=state_after,
        state_delta=state_delta,
    )
    bot.stats.on_attempt(
        status=event_name,
        context=non_action_context,
    )

    episode_marker(
        bot,
        event_name,
        {
            "decision_tendency": str(decision_tendency or "hold"),
            "proposed_decision": str(result.get("proposed_decision", "WAIT") or "WAIT"),
            "reason": str(result.get("rejection_reason", "runtime_non_action") or "runtime_non_action"),
            "meta_regulation_state": dict(result.get("meta_regulation_state", {}) or {}),
            "expectation_state": dict(result.get("expectation_state", {}) or {}),
            "bearing_context": dict((non_action_context.get("bearing_context", {}) or {})),
            "felt_bearing_score": float(non_action_context.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(non_action_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "state_before": dict(state_before or {}),
            "state_after": dict(state_after or {}),
            "state_delta": dict(state_delta or {}),
        },
    )
    bot._commit_regulation_state_snapshot(state_after)
    return True


def finalize_active_position_cancel(bot, resolved_position, exit_context, order_id, cancel_cause, *, outcome_stimulus, episode_marker):
    cancel_state_before = bot._build_regulation_state_snapshot()
    position_meta = dict((resolved_position or {}).get("meta", {}) or {})
    cancel_context = {
        **dict(exit_context or {}),
        **position_meta,
    }
    position_for_outcome = dict(bot.position or {})
    position_for_outcome["meta"] = {
        **dict(position_for_outcome.get("meta", {}) or {}),
        **dict(cancel_context or {}),
    }
    outcome_stimulus(bot, "cancel", position_for_outcome)
    cancel_state_after = bot._build_regulation_state_snapshot()
    cancel_state_delta = bot._build_regulation_state_delta(
        cancel_state_before,
        cancel_state_after,
    )
    bot.stats.on_attempt(
        status="cancelled",
        context=cancel_context,
    )
    episode_marker(
        bot,
        "cancelled",
        {
            "position": dict(resolved_position or {}),
            "reason": str(cancel_cause or "exchange_cancel"),
            "bearing_context": dict((cancel_context.get("bearing_context", {}) or {})),
            "felt_bearing_score": float(cancel_context.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(cancel_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "state_before": dict(cancel_state_before or {}),
            "state_after": dict(cancel_state_after or {}),
            "state_delta": dict(cancel_state_delta or {}),
        },
    )
    bot.stats.on_cancel(
        order_id=order_id,
        cause=str(cancel_cause or "exchange_cancel"),
        exploration_trade=False,
        outcome_decomposition=dict(getattr(bot, "last_outcome_decomposition", {}) or {}),
        context=cancel_context,
    )
    bot._sync_last_outcome_decomposition_from_stats()
    bot._mark_memory_state_dirty()
    bot._commit_regulation_state_snapshot(cancel_state_after)
    bot.position = None
    return True


def finalize_active_position_resolution(bot, resolved_position, exit_context, reason, live_mode, *, config, outcome_stimulus, episode_marker):
    state_before = bot._build_regulation_state_snapshot()
    position_for_outcome = dict(bot.position or {})
    position_for_outcome["meta"] = {
        **dict(position_for_outcome.get("meta", {}) or {}),
        **dict(exit_context or {}),
    }
    outcome_stimulus(bot, reason, position_for_outcome)
    state_after = bot._build_regulation_state_snapshot()
    state_delta = bot._build_regulation_state_delta(
        state_before,
        state_after,
    )
    bot._mark_memory_state_dirty()

    if str(reason).lower() == "sl_hit":
        bot.mcm_pause_left = int(getattr(config, "MCM_SL_PAUSE_STEPS", 3) or 3)

    bot.stats.on_exit(
        entry=bot.position.get("entry"),
        tp=bot.position.get("tp"),
        sl=bot.position.get("sl"),
        reason=reason,
        side=bot.position.get("side"),
        amount=config.ORDER_SIZE if live_mode else 1.0,
        exit_price=float(resolved_position.get("matured_exit_price", 0.0) or 0.0) if str(reason).lower() == "matured_exit" else None,
        exploration_trade=False,
        outcome_decomposition=dict(getattr(bot, "last_outcome_decomposition", {}) or {}),
        context=exit_context,
    )
    bot._sync_last_outcome_decomposition_from_stats()
    episode_marker(
        bot,
        "resolved",
        {
            "position": dict(resolved_position or {}),
            "reason": str(reason or "-"),
            "bearing_context": dict((exit_context.get("bearing_context", {}) or {})),
            "felt_bearing_score": float(exit_context.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(exit_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "state_before": dict(state_before or {}),
            "state_after": dict(state_after or {}),
            "state_delta": dict(state_delta or {}),
        },
    )

    bot._commit_regulation_state_snapshot(state_after)
    bot.position = None
    return True


def finalize_entry_attempt_abandoned(bot, entry_result, reason, state_before, state_after, state_delta, *, episode_marker):
    abandoned_context = bot._build_entry_attempt_context(
        entry_result,
        state_before=state_before,
        state_after=state_after,
        state_delta=state_delta,
    )
    bot.stats.on_attempt(
        status="skipped",
        context=abandoned_context,
    )
    episode_marker(
        bot,
        "abandoned",
        {
            "trade_plan": dict((abandoned_context.get("trade_plan", {}) or {})),
            "reason": str(reason or "entry_abandoned"),
            "bearing_context": dict((abandoned_context.get("bearing_context", {}) or {})),
            "felt_bearing_score": float(abandoned_context.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(abandoned_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "state_before": dict((abandoned_context.get("state_before", {}) or {})),
            "state_after": dict((abandoned_context.get("state_after", {}) or {})),
            "state_delta": dict((abandoned_context.get("state_delta", {}) or {})),
        },
    )
    bot._commit_regulation_state_snapshot(state_after)
    return True


def finalize_entry_attempt_submission(bot, entry_result, side, entry_price, tp_price, sl_price, risk, order_id, state_before, state_after, state_delta, *, config, episode_marker):
    attempt_meta = bot._build_entry_attempt_context(
        entry_result,
        state_before=state_before,
        state_after=state_after,
        state_delta=state_delta,
    )

    bot.execution_state = {
        **dict(bot.execution_state or {}),
        "execution_phase": "pending_submitted",
        "execution_ready": True,
        "execution_blocked": False,
    }

    bot.pending_entry = {
        "side": side,
        "entry": entry_price,
        "tp": tp_price,
        "sl": sl_price,
        "risk": float(risk),
        "order_id": order_id,
        "created_index": bot.processed,
        "max_wait_bars": int(getattr(config, "PENDING_ENTRY_MAX_WAIT_BARS", 20) or 20),
        "meta": {
            **dict(attempt_meta or {}),
            "felt_bearing_score": float(entry_result.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(entry_result.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "episode_felt_summary": dict(entry_result.get("episode_felt_summary", {}) or {}),
            "bearing_context": dict((attempt_meta.get("bearing_context", {}) or {})),
        },
    }
    bot.stats.on_attempt(
        status="submitted",
        context=dict(bot.pending_entry.get("meta", {}) or {}),
    )
    episode_marker(
        bot,
        "submitted",
        {
            "trade_plan": dict((attempt_meta.get("trade_plan", {}) or {})),
            "reason": str(side or "-").lower(),
            "bearing_context": dict((attempt_meta.get("bearing_context", {}) or {})),
            "felt_bearing_score": float(attempt_meta.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(attempt_meta.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
        },
    )

    bot._mark_memory_state_dirty()
    bot._commit_regulation_state_snapshot(state_after)
    return True
