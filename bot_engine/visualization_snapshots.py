# ==================================================
# bot_engine/visualization_snapshots.py
# Bot visualization snapshot write orchestration
# ==================================================


def resolve_visualization_snapshot_write_due(bot, window=None, candle_state=None, *, config, time_module):
    bot._snapshot_write_seq = int(getattr(bot, "_snapshot_write_seq", 0) or 0) + 1

    every_n = max(
        1,
        int(getattr(config, "MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N", 1) or 1),
    )
    min_interval = max(
        0.0,
        float(getattr(config, "MCM_VISUAL_SNAPSHOT_MIN_INTERVAL_SECONDS", 0.0) or 0.0),
    )
    force_on_state_change = bool(getattr(config, "MCM_VISUAL_SNAPSHOT_FORCE_ON_STATE_CHANGE", True))

    pending_state = dict(getattr(bot, "pending_entry", {}) or {})
    position_state = dict(getattr(bot, "position", {}) or {})

    state_key = (
        bool(position_state),
        str(position_state.get("side", "-") or "-"),
        str(position_state.get("entry_ts", position_state.get("entry", "-")) or "-"),
        bool(pending_state),
        str(pending_state.get("order_id", pending_state.get("id", "-")) or "-"),
    )

    if force_on_state_change and state_key != getattr(bot, "_snapshot_last_state_key", None):
        bot._snapshot_last_state_key = tuple(state_key)
        bot._snapshot_last_write_ts = float(time_module.time())
        return True

    if every_n <= 1:
        bot._snapshot_last_write_ts = float(time_module.time())
        return True

    if (int(bot._snapshot_write_seq) % every_n) == 0:
        bot._snapshot_last_write_ts = float(time_module.time())
        return True

    if min_interval > 0.0:
        now_ts = float(time_module.time())
        last_ts = float(getattr(bot, "_snapshot_last_write_ts", 0.0) or 0.0)
        if (now_ts - last_ts) >= min_interval:
            bot._snapshot_last_write_ts = float(now_ts)
            return True

    return False


def build_inner_pipeline_snapshot(bot, *, pipeline_snapshot_builder):
    return pipeline_snapshot_builder(bot)


def build_bot_visualization_snapshot_bundle(bot, window, candle_state, *, visualization_snapshot_builder):
    return visualization_snapshot_builder(
        bot=bot,
        window=window,
        candle_state=candle_state,
    )


def write_visualization_snapshots(bot, window, candle_state, *, write_due_resolver, snapshot_state_preparer, config, time_module):
    if not write_due_resolver(
        bot,
        window=window,
        candle_state=candle_state,
        config=config,
        time_module=time_module,
    ):
        return None

    snapshot_state = snapshot_state_preparer(
        bot=bot,
        window=window,
        candle_state=candle_state,
    )

    snapshot_bundle = dict(snapshot_state.get("snapshot_bundle", {}) or {})
    if not snapshot_bundle:
        return None

    bot._snapshot_bundle = dict(snapshot_bundle or {})
    bot._snapshot_dirty = bool(snapshot_state.get("snapshot_dirty", False))
    return dict(snapshot_bundle or {})


def flush_visualization_snapshots(bot, force: bool = False, *, snapshot_bundle_writer):
    if not bool(getattr(bot, "_snapshot_dirty", False)) and not bool(force):
        return None

    snapshot_bundle = dict(getattr(bot, "_snapshot_bundle", {}) or {})
    if not snapshot_bundle:
        return None

    written_bundle = snapshot_bundle_writer(snapshot_bundle)
    if written_bundle is None:
        return None

    bot._snapshot_dirty = False
    return dict(written_bundle or {})
