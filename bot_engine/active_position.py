def handle_active_position(
    bot,
    window,
    last,
    live_mode: bool,
    *,
    config,
    debug_writer,
    episode_marker,
    cancelled_cause_consumer,
    cancelled_checker,
    active_order_snapshot_getter,
):
    if bot.position is None:
        return False

    entry_price = float(bot.position.get("entry", 0.0) or 0.0)
    side = str(bot.position.get("side", "")).upper().strip()
    risk_value = abs(float(bot.position.get("risk", 0.0) or 0.0))

    bot.current_timestamp = window[-1]["timestamp"]

    high = float(last["high"])
    low = float(last["low"])

    if side == "LONG":
        favorable = max(0.0, high - entry_price)
        adverse = max(0.0, entry_price - low)
    else:
        favorable = max(0.0, entry_price - low)
        adverse = max(0.0, high - entry_price)

    bot.position["mfe"] = max(float(bot.position.get("mfe", 0.0) or 0.0), favorable)
    bot.position["mae"] = max(float(bot.position.get("mae", 0.0) or 0.0), adverse)

    bars_open = 0
    entry_index = bot.position.get("entry_index")
    if isinstance(entry_index, int):
        bars_open = max(0, int(bot.processed) - int(entry_index))

    rr_value = 0.0
    if risk_value > 0.0:
        if side == "LONG":
            rr_value = max(
                0.0,
                float(bot.position.get("tp", 0.0) or 0.0) - entry_price,
            ) / risk_value
        else:
            rr_value = max(
                0.0,
                entry_price - float(bot.position.get("tp", 0.0) or 0.0),
            ) / risk_value

    fill_ratio = 0.0
    if risk_value > 0.0:
        fill_ratio = max(0.0, min(2.0, favorable / risk_value))

    try:
        close_price = float(last.get("close", 0.0) or 0.0)
    except Exception:
        close_price = 0.0
    mfe_r = float((float(bot.position.get("mfe", 0.0) or 0.0) / max(risk_value, 1e-9)) if risk_value > 0.0 else 0.0)
    mae_r = float((float(bot.position.get("mae", 0.0) or 0.0) / max(risk_value, 1e-9)) if risk_value > 0.0 else 0.0)

    meta_regulation_state = dict(getattr(bot, "meta_regulation_state", {}) or {})
    runtime_state = dict(getattr(bot, "mcm_runtime_decision_state", {}) or {})
    position_state_before, position_state_after, position_state_delta = bot._capture_regulation_transition()

    pressure_to_capacity = 0.0
    if float(getattr(bot, "action_capacity", 0.0) or 0.0) > 0.0:
        pressure_to_capacity = float(getattr(bot, "regulatory_load", 0.0) or 0.0) / max(0.05, float(getattr(bot, "action_capacity", 0.0) or 0.0))

    position_intervention_state = bot._build_position_intervention_state(
        close_price=float(close_price),
        entry_price=float(entry_price),
        side=str(side),
        risk_value=float(risk_value),
        mfe_r=float(mfe_r),
        mae_r=float(mae_r),
        fill_ratio=float(fill_ratio),
        pressure_to_capacity=float(pressure_to_capacity),
        bars_open=int(bars_open),
    )
    target_expectation_state = bot._build_target_expectation_state(
        position_intervention_state=dict(position_intervention_state or {}),
        side=str(side),
        entry_price=float(entry_price),
        close_price=float(close_price),
        tp_price=float(bot.position.get("tp", 0.0) or 0.0),
        risk_value=float(risk_value),
        bars_open=int(bars_open),
    )
    exit_candidate_observe_state = bot._build_exit_candidate_observe_state(
        dict(position_intervention_state or {}),
        side=str(side),
        entry_price=float(entry_price),
        close_price=float(close_price),
        target_expectation_state=dict(target_expectation_state or {}),
    )
    exit_candidate_replay_state = dict(bot.position.get("exit_candidate_replay_state", {}) or {})

    position_context = dict(bot.position.get("meta", {}) or {})
    exit_bearing_context = {
        **dict((position_context.get("bearing_context", {}) or {})),
        "structure_quality": float((bot.structure_perception_state or {}).get("structure_quality", 0.0) or 0.0),
        "stress_relief_potential": float((bot.structure_perception_state or {}).get("stress_relief_potential", 0.0) or 0.0),
        "context_confidence": float((bot.structure_perception_state or {}).get("context_confidence", 0.0) or 0.0),
        "pressure_to_capacity": float(pressure_to_capacity),
        "regulatory_load": float(getattr(bot, "regulatory_load", 0.0) or 0.0),
        "action_capacity": float(getattr(bot, "action_capacity", 0.0) or 0.0),
        "recovery_need": float(getattr(bot, "recovery_need", 0.0) or 0.0),
        "survival_pressure": float(getattr(bot, "survival_pressure", 0.0) or 0.0),
    }
    exit_context = {
        **dict(position_context or {}),
        "bearing_context": dict(exit_bearing_context or {}),
        "structure_perception_state": dict(bot.structure_perception_state or {}),
        "outer_visual_perception_state": dict(bot.outer_visual_perception_state or {}),
        "position_watch_state": {
            "mfe": float(bot.position.get("mfe", 0.0) or 0.0),
            "mae": float(bot.position.get("mae", 0.0) or 0.0),
            "risk": float(risk_value),
            "mfe_r": float(mfe_r),
            "mae_r": float(mae_r),
            "fill_ratio": float(fill_ratio),
            "bars_open": int(bars_open),
        },
        "position_intervention_state": dict(position_intervention_state or {}),
        "target_expectation_state": dict(target_expectation_state or {}),
        "exit_candidate_observe_state": dict(exit_candidate_observe_state or {}),
        "exit_candidate_replay_state": dict(exit_candidate_replay_state or {}),
        "world_state": {
            **dict((position_context.get("world_state", {}) or {})),
            "structure_perception_state": dict(bot.structure_perception_state or {}),
            "visual_market_state": dict(bot.visual_market_state or {}),
            "tension_state": dict(bot.tension_state or {}),
            "temporal_perception_state": dict(bot.temporal_perception_state or {}),
        },
    }

    episode_marker(
        bot,
        "position_update",
        {
            "position": dict(bot.position or {}),
            "entry": float(bot.position.get("entry", 0.0) or 0.0),
            "tp": float(bot.position.get("tp", 0.0) or 0.0),
            "sl": float(bot.position.get("sl", 0.0) or 0.0),
            "risk": float(risk_value),
            "rr": float(rr_value),
            "mfe": float(bot.position.get("mfe", 0.0) or 0.0),
            "mae": float(bot.position.get("mae", 0.0) or 0.0),
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
            "bearing_context": dict((exit_context.get("bearing_context", {}) or {})),
            "felt_bearing_score": float(exit_context.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(exit_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "position_intervention_state": dict(position_intervention_state or {}),
            "target_expectation_state": dict(target_expectation_state or {}),
            "exit_candidate_observe_state": dict(exit_candidate_observe_state or {}),
            "exit_candidate_replay_state": dict(exit_candidate_replay_state or {}),
            "reason": "position_watch",
            "state_before": dict(position_state_before or {}),
            "state_after": dict(position_state_after or {}),
            "state_delta": dict(position_state_delta or {}),
        },
    )
    bot._commit_regulation_state_snapshot(position_state_after)

    exit_signal = bot.exit_engine.process(
        window,
        bot.position,
        "exit_trading_debug.csv",
    )

    reason = None
    if exit_signal is not None:
        reason = exit_signal.get("reason")

    if reason is not None:
        resolved_position = dict(bot.position or {})

        if live_mode and config.AKTIV_ORDER:
            oid = bot.position.get("order_id")
            cancel_cause = cancelled_cause_consumer(oid)
            if oid is not None and cancel_cause is None and bool(cancelled_checker(oid)):
                cancel_cause = "exchange_cancel"
            if oid is not None and cancel_cause is not None:
                return bot._finalize_active_position_cancel(
                    resolved_position=dict(resolved_position or {}),
                    exit_context=dict(exit_context or {}),
                    order_id=oid,
                    cancel_cause=cancel_cause,
                )

            live_snapshot = active_order_snapshot_getter()
            if isinstance(live_snapshot, dict):
                exit_context = {
                    **dict(exit_context or {}),
                    "live_exit_confirmation": {
                        "confirmed_closed": False,
                        "reason": "exchange_position_or_order_still_active",
                        "snapshot": dict(live_snapshot or {}),
                        "local_exit_reason": str(reason or "-"),
                    },
                }
                debug_writer(
                    "LIVE_EXIT_WAIT "
                    f"local_reason={str(reason or '-')} "
                    f"source={str(live_snapshot.get('source', '-') or '-')} "
                    f"id={str(live_snapshot.get('id', '-') or '-')}",
                    "live_backtest_debug.csv",
                )
                return True

            exit_context = {
                **dict(exit_context or {}),
                "live_exit_confirmation": {
                    "confirmed_closed": True,
                    "reason": "exchange_no_active_position_snapshot",
                    "local_exit_reason": str(reason or "-"),
                },
            }

        return bot._finalize_active_position_resolution(
            resolved_position=dict(resolved_position or {}),
            exit_context=dict(exit_context or {}),
            reason=reason,
            live_mode=bool(live_mode),
        )

    if bool((exit_candidate_observe_state or {}).get("exit_candidate", False)) and not bot.position.get("exit_candidate_replay_state"):
        bot.position["exit_candidate_replay_state"] = {
            **dict(exit_candidate_observe_state or {}),
            "candidate_timestamp": int(getattr(bot, "current_timestamp", 0) or 0),
            "candidate_bars_open": int(bars_open),
            "candidate_price": float(close_price),
            "candidate_mfe_r": float(mfe_r),
            "candidate_mae_r": float(mae_r),
            "target_expectation_state": dict(target_expectation_state or {}),
        }
        exit_context["exit_candidate_replay_state"] = dict(bot.position.get("exit_candidate_replay_state", {}) or {})

    matured_signal = bot._resolve_matured_exit_signal(
        last=last,
        exit_context=dict(exit_context or {}),
        fill_ratio=float(fill_ratio),
        pressure_to_capacity=float(pressure_to_capacity),
        risk_value=float(risk_value),
        bars_open=int(bars_open),
        live_mode=bool(live_mode),
    )
    if matured_signal is not None:
        exit_context = {
            **dict(exit_context or {}),
            "matured_exit_state": dict(matured_signal or {}),
        }
        bot.position["matured_exit_price"] = float(matured_signal.get("exit_price", 0.0) or 0.0)
        return bot._finalize_active_position_resolution(
            resolved_position=dict(bot.position or {}),
            exit_context=dict(exit_context or {}),
            reason="matured_exit",
            live_mode=bool(live_mode),
        )
    return True
