def resolve_matured_exit_signal(
    bot,
    last: dict,
    exit_context: dict,
    fill_ratio: float,
    pressure_to_capacity: float,
    risk_value: float,
    bars_open: int,
    live_mode: bool = False,
    *,
    config,
    debug_enabled,
    debug_writer,
    episode_marker,
):
    mode = str(getattr(config, "MCM_MATURED_EXIT_MODE", "fixed") or "fixed").strip().lower()
    if mode not in ("observe", "active"):
        return None

    if not bot.position or risk_value <= 0.0:
        return None

    side = str(bot.position.get("side", "") or "").upper().strip()
    if side not in ("LONG", "SHORT"):
        return None

    try:
        close_price = float(last.get("close", 0.0) or 0.0)
    except Exception:
        close_price = 0.0
    if close_price <= 0.0:
        return None

    mfe_r = float(bot.position.get("mfe", 0.0) or 0.0) / max(risk_value, 1e-9)
    mae_r = float(bot.position.get("mae", 0.0) or 0.0) / max(risk_value, 1e-9)
    if side == "LONG":
        current_r = (close_price - float(bot.position.get("entry", 0.0) or 0.0)) / max(risk_value, 1e-9)
    else:
        current_r = (float(bot.position.get("entry", 0.0) or 0.0) - close_price) / max(risk_value, 1e-9)

    giveback_r = max(0.0, mfe_r - current_r)
    structure_quality = float((bot.structure_perception_state or {}).get("structure_quality", 0.0) or 0.0)
    recovery_balance = float(getattr(bot, "recovery_balance", 0.0) or 0.0)
    action_capacity = float(getattr(bot, "action_capacity", 0.0) or 0.0)
    regulatory_load = float(getattr(bot, "regulatory_load", 0.0) or 0.0)
    if pressure_to_capacity <= 0.0 and action_capacity > 0.0:
        pressure_to_capacity = regulatory_load / max(0.05, action_capacity)

    min_mfe = float(getattr(config, "MCM_MATURED_EXIT_MIN_MFE_R", 1.0) or 1.0)
    min_giveback = float(getattr(config, "MCM_MATURED_EXIT_GIVEBACK_R", 0.35) or 0.35)
    max_structure = float(getattr(config, "MCM_MATURED_EXIT_STRUCTURE_MAX", 0.50) or 0.50)
    min_pressure = float(getattr(config, "MCM_MATURED_EXIT_PRESSURE_MIN", 1.15) or 1.15)

    def _clip01(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    structure_loss = _clip01((max_structure - structure_quality) / 0.18)
    pressure_load = _clip01((pressure_to_capacity - min_pressure) / 0.70)
    giveback_load = _clip01((giveback_r - min_giveback) / 0.80)
    recovery_loss = _clip01((-recovery_balance - 0.20) / 0.55)
    mfe_support = _clip01(mfe_r / max(min_mfe, 1e-9))
    giveback_support = _clip01(giveback_r / max(min_giveback, 1e-9))
    maturity_pressure = (
        (structure_loss * 0.34)
        + (giveback_load * 0.30)
        + (pressure_load * 0.22)
        + (recovery_loss * 0.14)
    )
    matured_exit_pressure = _clip01(
        (maturity_pressure * 0.48)
        + (giveback_support * 0.18)
        + (mfe_support * 0.12)
        + (pressure_load * 0.12)
        + (recovery_loss * 0.10)
    )
    continue_position_pressure = _clip01(
        ((1.0 - structure_loss) * 0.26)
        + ((1.0 - giveback_load) * 0.20)
        + ((1.0 - pressure_load) * 0.18)
        + (max(0.0, recovery_balance) * 0.16)
        + ((1.0 - mfe_support) * 0.12)
        + ((1.0 - giveback_support) * 0.08)
    )
    matured_exit_pressures = {
        "matured_exit": float(matured_exit_pressure),
        "continue_position": float(continue_position_pressure),
    }
    matured_exit_label = max(matured_exit_pressures, key=matured_exit_pressures.get)

    if matured_exit_label != "matured_exit":
        return None

    signal = {
        "reason": "matured_exit",
        "matured_exit_label": str(matured_exit_label),
        "mode": str(mode),
        "timestamp": int(getattr(bot, "current_timestamp", 0) or 0),
        "entry": float(bot.position.get("entry", 0.0) or 0.0),
        "tp": float(bot.position.get("tp", 0.0) or 0.0),
        "sl": float(bot.position.get("sl", 0.0) or 0.0),
        "risk": float(risk_value),
        "exit_price": float(close_price),
        "maturity_pressure": float(maturity_pressure),
        "matured_exit_pressure": float(matured_exit_pressure),
        "continue_position_pressure": float(continue_position_pressure),
        "matured_exit_pressures": dict(matured_exit_pressures),
        "mfe_support": float(mfe_support),
        "giveback_support": float(giveback_support),
        "mfe_r": float(mfe_r),
        "mae_r": float(mae_r),
        "current_r": float(current_r),
        "giveback_r": float(giveback_r),
        "structure_quality": float(structure_quality),
        "pressure_to_capacity": float(pressure_to_capacity),
        "recovery_balance": float(recovery_balance),
        "bars_open": int(bars_open),
    }
    position_intervention_state = dict((exit_context or {}).get("position_intervention_state", {}) or {})
    if position_intervention_state:
        signal["position_intervention_state"] = dict(position_intervention_state)
    exit_candidate_observe_state = dict((exit_context or {}).get("exit_candidate_observe_state", {}) or {})
    if exit_candidate_observe_state:
        signal["exit_candidate_observe_state"] = dict(exit_candidate_observe_state)

    if debug_enabled:
        debug_writer(
            "MATURED_EXIT "
            f"mode={mode} ts={int(getattr(bot, 'current_timestamp', 0) or 0)} "
            f"side={side} entry={float(bot.position.get('entry', 0.0) or 0.0):.4f} "
            f"tp={float(bot.position.get('tp', 0.0) or 0.0):.4f} "
            f"sl={float(bot.position.get('sl', 0.0) or 0.0):.4f} "
            f"risk={risk_value:.4f} exit_price={close_price:.4f} "
            f"maturity_pressure={maturity_pressure:.4f} "
            f"matured_exit_pressure={matured_exit_pressure:.4f} "
            f"continue_position_pressure={continue_position_pressure:.4f} "
            f"mfe_r={mfe_r:.4f} mae_r={mae_r:.4f} current_r={current_r:.4f} "
            f"giveback_r={giveback_r:.4f} structure_quality={structure_quality:.4f} "
            f"pressure_to_capacity={pressure_to_capacity:.4f} recovery_balance={recovery_balance:.4f} "
            f"bars_open={int(bars_open)} "
            f"position_cognitive_load={float(position_intervention_state.get('position_cognitive_load', 0.0) or 0.0):.4f} "
            f"exit_decision_pressure={float(position_intervention_state.get('exit_decision_pressure', 0.0) or 0.0):.4f} "
            f"plan_trust={float(position_intervention_state.get('plan_trust', 0.0) or 0.0):.4f} "
            f"intervention_fitness={float(position_intervention_state.get('intervention_fitness', 0.0) or 0.0):.4f} "
            f"intervention_label={str(position_intervention_state.get('intervention_label', '-') or '-')} "
            f"exit_candidate={int(bool(exit_candidate_observe_state.get('exit_candidate', False)))} "
            f"candidate_label={str(exit_candidate_observe_state.get('candidate_label', '-') or '-')}",
            "matured_exit_debug.csv",
        )

    episode_marker(
        bot,
        "matured_exit_observe" if mode == "observe" else "matured_exit_active",
        {
            **dict(signal),
            "position": dict(bot.position or {}),
            "bearing_context": dict((exit_context or {}).get("bearing_context", {}) or {}),
            "position_intervention_state": dict(position_intervention_state),
            "exit_candidate_observe_state": dict(exit_candidate_observe_state),
        },
    )

    if mode == "observe" or bool(live_mode):
        return None
    return dict(signal)
