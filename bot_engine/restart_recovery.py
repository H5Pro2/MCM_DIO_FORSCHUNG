import time


def apply_restart_recovery_snapshot(bot, snapshot, *, config, episode_marker, time_module=time):
    if bot is None or not isinstance(snapshot, dict):
        return False

    snapshot_source = str(snapshot.get("source", "") or "").strip().lower()
    entry_raw = snapshot.get("entry")
    tp_raw = snapshot.get("tp")
    sl_raw = snapshot.get("sl")

    try:
        entry = float(entry_raw)
    except Exception:
        entry = None

    try:
        tp_value = float(tp_raw) if tp_raw is not None else None
    except Exception:
        tp_value = None

    try:
        sl_value = float(sl_raw) if sl_raw is not None else None
    except Exception:
        sl_value = None

    if entry is None or tp_value is None or sl_value is None:
        return False

    restart_state_before = bot._build_regulation_state_snapshot()
    risk = abs(entry - sl_value)
    restart_entry_ts = snapshot.get("entry_ts")

    if restart_entry_ts is None:
        restart_entry_ts = getattr(bot, "current_timestamp", None)

    if restart_entry_ts is None:
        restart_entry_ts = int(time_module.time() * 1000)

    restart_meta = {
        "felt_bearing_score": 0.0,
        "felt_profile_label": "mixed_unclear",
        "episode_felt_summary": {},
        "bearing_context": {},
        "restart_recovery": True,
        "recovery_source": str(snapshot_source or "unknown"),
        "recovery_snapshot": dict(snapshot or {}),
    }

    if snapshot_source == "open_order":
        print("RESTART RECOVERY â†’ PENDING ORDER FOUND")

        bot.execution_state = {
            **dict(getattr(bot, "execution_state", {}) or {}),
            "execution_phase": "pending_recovered",
            "execution_ready": True,
            "execution_blocked": False,
        }
        bot.pending_entry = {
            "side": snapshot.get("side"),
            "entry": entry,
            "tp": tp_value,
            "sl": sl_value,
            "risk": risk,
            "order_id": snapshot.get("id"),
            "created_index": 0,
            "max_wait_bars": int(getattr(config, "PENDING_ENTRY_MAX_WAIT_BARS", 20) or 20),
            "meta": dict(restart_meta or {}),
        }
        restart_state_after = bot._build_regulation_state_snapshot()
        restart_state_delta = bot._build_regulation_state_delta(
            restart_state_before,
            restart_state_after,
        )
        episode_marker(
            bot,
            "pending_update",
            {
                "pending_entry": dict(bot.pending_entry or {}),
                "reason": "restart_pending_recovery",
                "recovery_source": str(snapshot_source or "open_order"),
                "recovery_snapshot": dict(snapshot or {}),
                "state_before": dict(restart_state_before or {}),
                "state_after": dict(restart_state_after or {}),
                "state_delta": dict(restart_state_delta or {}),
            },
        )
    else:
        print("RESTART RECOVERY â†’ ACTIVE POSITION FOUND")

        bot.execution_state = {
            **dict(getattr(bot, "execution_state", {}) or {}),
            "execution_phase": "position_recovered",
            "execution_ready": True,
            "execution_blocked": False,
        }
        bot.position = {
            "side": snapshot.get("side"),
            "entry": entry,
            "tp": tp_value,
            "sl": sl_value,
            "mfe": 0.0,
            "mae": 0.0,
            "risk": risk,
            "order_id": snapshot.get("id"),
            "entry_ts": restart_entry_ts,
            "entry_index": None,
            "last_checked_ts": restart_entry_ts,
            "meta": dict(restart_meta or {}),
        }
        restart_state_after = bot._build_regulation_state_snapshot()
        restart_state_delta = bot._build_regulation_state_delta(
            restart_state_before,
            restart_state_after,
        )
        episode_marker(
            bot,
            "position_update",
            {
                "position": dict(bot.position or {}),
                "reason": "restart_position_recovery",
                "recovery_source": str(snapshot_source or "position_context"),
                "recovery_snapshot": dict(snapshot or {}),
                "state_before": dict(restart_state_before or {}),
                "state_after": dict(restart_state_after or {}),
                "state_delta": dict(restart_state_delta or {}),
            },
        )

    bot._mark_memory_state_dirty()
    bot._commit_regulation_state_snapshot(restart_state_after)
    return True
