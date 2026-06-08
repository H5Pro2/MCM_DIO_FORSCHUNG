def recover_live_state_on_boot(bot, *, config, active_order_snapshot_getter):
    live_mode = str(getattr(config, "MODE", "LIVE")).upper() == "LIVE"
    snapshot = None

    if live_mode and bool(getattr(config, "AKTIV_ORDER", False)):
        snapshot = active_order_snapshot_getter()

    if snapshot:
        recovered = bot._apply_restart_recovery_snapshot(
            snapshot,
        )

        if recovered:
            bot._save_memory_state(force=True)

        return bool(recovered)

    return False
