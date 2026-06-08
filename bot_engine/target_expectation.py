def build_target_expectation_state(
    bot,
    *,
    position_intervention_state: dict,
    side: str,
    entry_price: float,
    close_price: float,
    tp_price: float,
    risk_value: float,
    bars_open: int,
    config,
    debug_writer,
) -> dict:
    state = dict(position_intervention_state or {})
    if not state or risk_value <= 0.0:
        return {}

    def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
        try:
            return max(lo, min(hi, float(value)))
        except Exception:
            return lo

    def _val(key: str) -> float:
        try:
            return float(state.get(key, 0.0) or 0.0)
        except Exception:
            return 0.0

    side = str(side or "").upper().strip()
    if side == "LONG":
        current_r = (float(close_price) - float(entry_price)) / max(float(risk_value), 1e-9)
        target_total_r = max(0.0, (float(tp_price) - float(entry_price)) / max(float(risk_value), 1e-9))
    elif side == "SHORT":
        current_r = (float(entry_price) - float(close_price)) / max(float(risk_value), 1e-9)
        target_total_r = max(0.0, (float(entry_price) - float(tp_price)) / max(float(risk_value), 1e-9))
    else:
        current_r = _val("current_r")
        target_total_r = 0.0

    target_total_r = max(float(target_total_r), 0.01)
    target_progress = _clamp(float(current_r) / target_total_r)
    target_remaining_r = max(0.0, target_total_r - float(current_r))
    target_remaining_pressure = _clamp(target_remaining_r / max(target_total_r, 0.01))

    plan_trust = _val("plan_trust")
    holding_stability = _val("holding_stability")
    exit_decision_pressure = _val("exit_decision_pressure")
    exit_evidence = _val("exit_evidence")
    structure_quality = _val("structure_quality")
    structure_stability = _val("structure_stability")
    context_confidence = _val("context_confidence")
    giveback_r = _val("giveback_r")
    mfe_r = _val("mfe_r")
    mae_r = _val("mae_r")
    position_cognitive_load = _val("position_cognitive_load")
    intervention_unfit_state = _val("intervention_unfit_state")

    position_meta = dict((bot.position or {}).get("meta", {}) or {})
    expectation_state = dict(position_meta.get("expectation_state", {}) or {})
    experience_state = dict(position_meta.get("experience", {}) or {})
    entry_meta_regulation_state = dict(position_meta.get("meta_regulation_state", {}) or {})
    current_meta_regulation_state = dict(getattr(bot, "meta_regulation_state", {}) or {})
    base_entry_expectation = float(
        expectation_state.get(
            "entry_expectation",
            experience_state.get("entry_expectation", 0.0),
        ) or 0.0
    )
    base_target_expectation = float(
        expectation_state.get(
            "target_expectation",
            experience_state.get("target_expectation", 0.0),
        ) or 0.0
    )
    base_expectation_support = _clamp((base_entry_expectation * 0.62) + (base_target_expectation * 0.38))

    giveback_load = _clamp(giveback_r / 2.50)
    adverse_load = _clamp(mae_r / 1.20)
    negative_current_load = _clamp((-float(current_r)) / 0.90)
    path_retrace_load = _clamp(giveback_r / max(float(mfe_r), 0.25))
    time_pressure = _clamp(float(bars_open) / 96.0)

    tp_reachability = _clamp(
        (plan_trust * 0.26)
        + (holding_stability * 0.20)
        + (structure_quality * 0.16)
        + (context_confidence * 0.12)
        + (target_progress * 0.10)
        + ((1.0 - giveback_load) * 0.07)
        + ((1.0 - negative_current_load) * 0.05)
        + (base_expectation_support * 0.04)
    )
    target_path_integrity = _clamp(
        (structure_stability * 0.24)
        + (plan_trust * 0.22)
        + (holding_stability * 0.18)
        + (context_confidence * 0.12)
        + ((1.0 - path_retrace_load) * 0.10)
        + ((1.0 - adverse_load) * 0.08)
        + (base_expectation_support * 0.06)
    )
    expectation_deviation = _clamp(
        ((1.0 - target_path_integrity) * 0.28)
        + (exit_decision_pressure * 0.22)
        + (negative_current_load * 0.18)
        + (giveback_load * 0.14)
        + ((1.0 - plan_trust) * 0.10)
        + (position_cognitive_load * 0.08)
    )
    expectation_break_pressure = _clamp(
        (expectation_deviation * 0.38)
        + (exit_evidence * 0.22)
        + ((1.0 - tp_reachability) * 0.18)
        + (negative_current_load * 0.12)
        + (intervention_unfit_state * 0.10)
    )
    expectation_hold_support = _clamp(
        (tp_reachability * 0.38)
        + (target_path_integrity * 0.28)
        + (plan_trust * 0.16)
        + (holding_stability * 0.12)
        + ((1.0 - expectation_break_pressure) * 0.06)
    )
    target_room_pressure = _clamp(
        (target_remaining_pressure * 0.34)
        + (exit_decision_pressure * 0.22)
        + (time_pressure * 0.14)
        + (path_retrace_load * 0.14)
        + (position_cognitive_load * 0.10)
        + ((1.0 - base_expectation_support) * 0.06)
    )
    target_semantic_confidence = _clamp(
        (context_confidence * 0.30)
        + (structure_quality * 0.22)
        + (structure_stability * 0.18)
        + (base_expectation_support * 0.16)
        + ((1.0 - position_cognitive_load) * 0.08)
        + ((1.0 - target_room_pressure) * 0.06)
    )
    entry_route_familiarity = _clamp(entry_meta_regulation_state.get("route_familiarity", 0.0))
    entry_transfer_bearing = _clamp(entry_meta_regulation_state.get("transfer_bearing", 0.0))
    current_route_familiarity = _clamp(current_meta_regulation_state.get("route_familiarity", entry_route_familiarity))
    current_semantic_shift_pressure = _clamp(current_meta_regulation_state.get("semantic_shift_pressure", 0.0))
    current_transfer_bearing = _clamp(current_meta_regulation_state.get("transfer_bearing", entry_transfer_bearing))
    current_interpretation_quality = _clamp(current_meta_regulation_state.get("interpretation_quality", 0.0))
    current_adaptation_phase = str(current_meta_regulation_state.get("adaptation_phase", "-") or "-")
    route_familiarity_delta = max(-1.0, min(1.0, current_route_familiarity - entry_route_familiarity))
    transfer_bearing_delta = max(-1.0, min(1.0, current_transfer_bearing - entry_transfer_bearing))
    semantic_transfer_stress = _clamp(
        (current_semantic_shift_pressure * 0.42)
        + ((1.0 - current_transfer_bearing) * 0.24)
        + ((1.0 - current_route_familiarity) * 0.16)
        + (max(0.0, -route_familiarity_delta) * 0.10)
        + (max(0.0, -transfer_bearing_delta) * 0.08)
    )

    prior_target_hold_support = 0.0
    prior_tp_reachability = 0.0
    prior_target_path_integrity = 0.0
    previous_tp_reachability = tp_reachability
    previous_target_path_integrity = target_path_integrity
    previous_expectation_hold_support = expectation_hold_support
    previous_expectation_break_pressure = expectation_break_pressure
    previous_current_r = current_r
    previous_target_progress = target_progress
    prior_break_count = 0
    if bot.position is not None:
        prior_target_hold_support = float(bot.position.get("target_hold_support_peak", 0.0) or 0.0)
        prior_tp_reachability = float(bot.position.get("tp_reachability_peak", 0.0) or 0.0)
        prior_target_path_integrity = float(bot.position.get("target_path_integrity_peak", 0.0) or 0.0)
        previous_tp_reachability = float(bot.position.get("last_tp_reachability", tp_reachability) or 0.0)
        previous_target_path_integrity = float(bot.position.get("last_target_path_integrity", target_path_integrity) or 0.0)
        previous_expectation_hold_support = float(bot.position.get("last_expectation_hold_support", expectation_hold_support) or 0.0)
        previous_expectation_break_pressure = float(bot.position.get("last_expectation_break_pressure", expectation_break_pressure) or 0.0)
        previous_current_r = float(bot.position.get("last_current_r", current_r) or 0.0)
        previous_target_progress = float(bot.position.get("last_target_progress", target_progress) or 0.0)
        prior_break_count = int(bot.position.get("expectation_break_count", 0) or 0)

    break_active_pressure = _clamp((expectation_break_pressure * 0.34) + ((1.0 - expectation_hold_support) * 0.18) + (expectation_deviation * 0.10))
    hold_active_pressure = _clamp((expectation_hold_support * 0.34) + (target_path_integrity * 0.14) + (tp_reachability * 0.10))
    break_active = bool(break_active_pressure > hold_active_pressure)
    if break_active:
        expectation_break_count = prior_break_count + 1
    else:
        expectation_break_count = max(0, prior_break_count - 1)

    expectation_break_persistence = _clamp(
        (_clamp(expectation_break_count / 4.0) * 0.42)
        + (expectation_break_pressure * 0.24)
        + ((1.0 - expectation_hold_support) * 0.16)
        + (expectation_deviation * 0.12)
        + (target_room_pressure * 0.06)
    )
    target_recovery_potential = _clamp(
        (prior_target_hold_support * 0.24)
        + (prior_tp_reachability * 0.18)
        + (prior_target_path_integrity * 0.12)
        + (structure_stability * 0.14)
        + (context_confidence * 0.10)
        + (_clamp(mfe_r / 2.0) * 0.10)
        + ((1.0 - negative_current_load) * 0.06)
        + ((1.0 - path_retrace_load) * 0.04)
        + (base_expectation_support * 0.02)
    )
    target_recovery_momentum = _clamp(
        (_clamp((tp_reachability - previous_tp_reachability) / 0.18) * 0.24)
        + (_clamp((target_path_integrity - previous_target_path_integrity) / 0.18) * 0.20)
        + (_clamp((expectation_hold_support - previous_expectation_hold_support) / 0.18) * 0.20)
        + (_clamp((previous_expectation_break_pressure - expectation_break_pressure) / 0.20) * 0.16)
        + (_clamp((current_r - previous_current_r) / 0.45) * 0.12)
        + (_clamp((target_progress - previous_target_progress) / 0.20) * 0.08)
    )
    break_to_recovery_delta = _clamp(
        (target_recovery_momentum * 0.40)
        + (expectation_hold_support * 0.20)
        + (target_path_integrity * 0.18)
        + ((1.0 - expectation_break_pressure) * 0.14)
        + (target_semantic_confidence * 0.08)
    )
    target_recovery_confirmation = _clamp(
        (target_recovery_momentum * 0.34)
        + (break_to_recovery_delta * 0.26)
        + (target_recovery_potential * 0.18)
        + ((1.0 - expectation_break_persistence) * 0.12)
        + (target_semantic_confidence * 0.10)
    )
    recovery_after_break_pressure = _clamp(
        ((1.0 if prior_break_count > 0 else 0.0) * 0.12)
        + ((1.0 - break_active_pressure) * 0.10)
        + (target_recovery_momentum * 0.22)
        + (target_recovery_confirmation * 0.30)
        + ((1.0 - expectation_break_pressure) * 0.10)
    )
    deep_retrace_recovery_pressure = _clamp(
        (break_active_pressure * 0.16)
        + (target_recovery_potential * 0.26)
        + (target_recovery_momentum * 0.18)
        + (target_recovery_confirmation * 0.24)
        + ((1.0 - expectation_break_persistence) * 0.10)
    )
    recovery_after_break_watch = bool(recovery_after_break_pressure > break_active_pressure and prior_break_count > 0)
    deep_retrace_recovery_watch = bool(deep_retrace_recovery_pressure > hold_active_pressure and break_active)

    if bot.position is not None:
        bot.position["target_hold_support_peak"] = float(max(prior_target_hold_support * 0.92, expectation_hold_support))
        bot.position["tp_reachability_peak"] = float(max(prior_tp_reachability * 0.92, tp_reachability))
        bot.position["target_path_integrity_peak"] = float(max(prior_target_path_integrity * 0.92, target_path_integrity))
        bot.position["expectation_break_count"] = int(expectation_break_count)
        bot.position["last_tp_reachability"] = float(tp_reachability)
        bot.position["last_target_path_integrity"] = float(target_path_integrity)
        bot.position["last_expectation_hold_support"] = float(expectation_hold_support)
        bot.position["last_expectation_break_pressure"] = float(expectation_break_pressure)
        bot.position["last_current_r"] = float(current_r)
        bot.position["last_target_progress"] = float(target_progress)

    expectation_label_pressures = {
        "recovery_after_break_watch": recovery_after_break_pressure,
        "deep_retrace_recovery_watch": deep_retrace_recovery_pressure,
        "expectation_break_observe": break_active_pressure,
        "target_expectation_holds": hold_active_pressure,
        "target_retrace_observe": _clamp((path_retrace_load * 0.28) + (tp_reachability * 0.24)),
        "target_unclear_observe": _clamp(((1.0 - target_semantic_confidence) * 0.22) + (expectation_deviation * 0.26)),
        "target_watch": _clamp((1.0 - max(break_active_pressure, hold_active_pressure, recovery_after_break_pressure, deep_retrace_recovery_pressure)) * 0.24),
    }
    expectation_label = max(expectation_label_pressures, key=expectation_label_pressures.get)

    result = {
        "target_expectation_context": str(expectation_label),
        "tp_reachability": float(tp_reachability),
        "target_path_integrity": float(target_path_integrity),
        "expectation_deviation": float(expectation_deviation),
        "expectation_break_pressure": float(expectation_break_pressure),
        "expectation_break_active_pressure": float(break_active_pressure),
        "expectation_hold_active_pressure": float(hold_active_pressure),
        "expectation_hold_support": float(expectation_hold_support),
        "target_room_pressure": float(target_room_pressure),
        "target_semantic_confidence": float(target_semantic_confidence),
        "target_progress": float(target_progress),
        "target_remaining_r": float(target_remaining_r),
        "target_total_r": float(target_total_r),
        "target_recovery_potential": float(target_recovery_potential),
        "target_recovery_momentum": float(target_recovery_momentum),
        "target_recovery_confirmation": float(target_recovery_confirmation),
        "recovery_after_break_pressure": float(recovery_after_break_pressure),
        "deep_retrace_recovery_pressure": float(deep_retrace_recovery_pressure),
        "break_to_recovery_delta": float(break_to_recovery_delta),
        "recovery_after_break_watch": bool(recovery_after_break_watch),
        "prior_target_hold_support": float(prior_target_hold_support),
        "prior_tp_reachability": float(prior_tp_reachability),
        "prior_target_path_integrity": float(prior_target_path_integrity),
        "expectation_break_persistence": float(expectation_break_persistence),
        "expectation_break_count": int(expectation_break_count),
        "deep_retrace_recovery_watch": bool(deep_retrace_recovery_watch),
        "target_expectation_label_pressures": dict(expectation_label_pressures),
        "base_entry_expectation": float(base_entry_expectation),
        "base_target_expectation": float(base_target_expectation),
        "entry_route_familiarity": float(entry_route_familiarity),
        "entry_transfer_bearing": float(entry_transfer_bearing),
        "current_route_familiarity": float(current_route_familiarity),
        "current_semantic_shift_pressure": float(current_semantic_shift_pressure),
        "current_transfer_bearing": float(current_transfer_bearing),
        "current_interpretation_quality": float(current_interpretation_quality),
        "current_adaptation_phase": str(current_adaptation_phase),
        "route_familiarity_delta": float(route_familiarity_delta),
        "transfer_bearing_delta": float(transfer_bearing_delta),
        "semantic_transfer_stress": float(semantic_transfer_stress),
    }

    if bool(getattr(config, "MCM_TARGET_EXPECTATION_PROTOCOL_DEBUG", True)):
        every_n = max(1, int(getattr(config, "MCM_TARGET_EXPECTATION_PROTOCOL_EVERY_N", 5) or 5))
        should_write = (
            (int(getattr(bot, "processed", 0) or 0) % every_n == 0)
            or break_active_pressure > hold_active_pressure
            or expectation_label != "target_watch"
        )
        if should_write:
            debug_writer(
                "TARGET_EXPECTATION "
                f"ts={int(getattr(bot, 'current_timestamp', 0) or 0)} "
                f"label={expectation_label} side={side} "
                f"entry={float(entry_price):.4f} close={float(close_price):.4f} tp={float(tp_price):.4f} "
                f"tp_reachability={tp_reachability:.4f} target_path_integrity={target_path_integrity:.4f} "
                f"expectation_deviation={expectation_deviation:.4f} "
                f"expectation_break_pressure={expectation_break_pressure:.4f} "
                f"expectation_hold_support={expectation_hold_support:.4f} "
                f"target_room_pressure={target_room_pressure:.4f} "
                f"target_semantic_confidence={target_semantic_confidence:.4f} "
                f"target_progress={target_progress:.4f} target_remaining_r={target_remaining_r:.4f} "
                f"target_recovery_potential={target_recovery_potential:.4f} "
                f"target_recovery_momentum={target_recovery_momentum:.4f} "
                f"target_recovery_confirmation={target_recovery_confirmation:.4f} "
                f"break_to_recovery_delta={break_to_recovery_delta:.4f} "
                f"current_route_familiarity={current_route_familiarity:.4f} "
                f"current_semantic_shift_pressure={current_semantic_shift_pressure:.4f} "
                f"current_transfer_bearing={current_transfer_bearing:.4f} "
                f"semantic_transfer_stress={semantic_transfer_stress:.4f} "
                f"current_adaptation_phase={current_adaptation_phase} "
                f"prior_target_hold_support={prior_target_hold_support:.4f} "
                f"expectation_break_persistence={expectation_break_persistence:.4f} "
                f"deep_retrace_recovery_watch={int(deep_retrace_recovery_watch)} "
                f"recovery_after_break_watch={int(recovery_after_break_watch)}",
                "mcm_target_expectation_protocol.csv",
            )

    return result
