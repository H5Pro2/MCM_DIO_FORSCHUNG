def build_exit_candidate_observe_state(
    bot,
    position_intervention_state: dict,
    side: str,
    entry_price: float,
    close_price: float,
    target_expectation_state: dict = None,
    *,
    config,
    debug_writer,
    episode_marker,
) -> dict:
    state = dict(position_intervention_state or {})
    if not state:
        return {}

    def _val(key: str) -> float:
        try:
            return float(state.get(key, 0.0) or 0.0)
        except Exception:
            return 0.0

    pressure_reference = max(0.05, float(getattr(config, "MCM_EXIT_CANDIDATE_MIN_PRESSURE", 0.58) or 0.58))
    fitness_reference = max(0.05, float(getattr(config, "MCM_EXIT_CANDIDATE_MIN_FITNESS", 0.40) or 0.40))
    evidence_reference = max(0.05, float(getattr(config, "MCM_EXIT_CANDIDATE_MIN_EVIDENCE", 0.54) or 0.54))
    adverse_reference = abs(float(getattr(config, "MCM_EXIT_CANDIDATE_MAX_CURRENT_R", -0.45) or -0.45)) or 0.45

    exit_decision_pressure = _val("exit_decision_pressure")
    plan_trust = _val("plan_trust")
    holding_stability = _val("holding_stability")
    intervention_fitness = _val("intervention_fitness")
    intervention_unfit_state = _val("intervention_unfit_state")
    exit_evidence = _val("exit_evidence")
    current_r = _val("current_r")
    sustained_exit_pressure = _val("sustained_exit_pressure")

    def _clip01(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    pressure_pull = _clip01(exit_decision_pressure / pressure_reference)
    fitness_pull = _clip01(intervention_fitness / fitness_reference)
    evidence_pull = _clip01(exit_evidence / evidence_reference)
    adverse_depth_pull = _clip01(max(0.0, -current_r) / adverse_reference)
    trust_hold_pull = _clip01(plan_trust)
    stability_hold_pull = _clip01(holding_stability)
    unfit_hold_pull = _clip01(intervention_unfit_state)

    confirmation_score = max(
        0.0,
        min(
            1.0,
            (exit_decision_pressure * 0.24)
            + ((1.0 - plan_trust) * 0.20)
            + ((1.0 - holding_stability) * 0.16)
            + (intervention_fitness * 0.18)
            + (exit_evidence * 0.14)
            + (sustained_exit_pressure * 0.08),
        ),
    )

    candidate_pressure = _clip01(
        (pressure_pull * 0.24)
        + (fitness_pull * 0.18)
        + (evidence_pull * 0.18)
        + (adverse_depth_pull * 0.16)
        + (sustained_exit_pressure * 0.12)
        + ((1.0 - trust_hold_pull) * 0.07)
        + ((1.0 - stability_hold_pull) * 0.05)
    )
    candidate_restraint_pressure = _clip01(
        (trust_hold_pull * 0.26)
        + (stability_hold_pull * 0.22)
        + (unfit_hold_pull * 0.18)
        + ((1.0 - fitness_pull) * 0.14)
        + ((1.0 - evidence_pull) * 0.12)
        + ((1.0 - adverse_depth_pull) * 0.08)
    )

    exit_candidate_pressures = {
        "exit_candidate_observe": float(candidate_pressure),
        "plan_trust_holds": float((trust_hold_pull * 0.44) + (stability_hold_pull * 0.28) + ((1.0 - pressure_pull) * 0.14)),
        "exit_pressure_unfit_observe": float((pressure_pull * 0.42) + ((1.0 - fitness_pull) * 0.34) + (unfit_hold_pull * 0.18)),
        "exit_retrace_observe": float((pressure_pull * 0.36) + ((1.0 - adverse_depth_pull) * 0.24) + (evidence_pull * 0.16)),
        "no_exit_candidate": float(candidate_restraint_pressure),
    }
    candidate_label = max(exit_candidate_pressures, key=exit_candidate_pressures.get)
    is_candidate = bool(candidate_label == "exit_candidate_observe")

    candidate = {
        "exit_candidate": bool(is_candidate),
        "candidate_label": str(candidate_label),
        "exit_candidate_pressure": float(candidate_pressure),
        "exit_candidate_restraint_pressure": float(candidate_restraint_pressure),
        "exit_candidate_pressures": dict(exit_candidate_pressures),
        "confirmation_score": float(confirmation_score),
        "exit_decision_pressure": float(exit_decision_pressure),
        "plan_trust": float(plan_trust),
        "holding_stability": float(holding_stability),
        "intervention_fitness": float(intervention_fitness),
        "intervention_unfit_state": float(intervention_unfit_state),
        "exit_evidence": float(exit_evidence),
        "current_r": float(current_r),
        "adverse_depth_pull": float(adverse_depth_pull),
        "sustained_exit_pressure": float(sustained_exit_pressure),
        "side": str(side or "").upper().strip(),
        "entry": float(entry_price),
        "close": float(close_price),
        **dict(target_expectation_state or {}),
    }

    if bool(getattr(config, "MCM_EXIT_CANDIDATE_OBSERVE_DEBUG", True)) and candidate_label != "no_exit_candidate":
        debug_writer(
            "EXIT_CANDIDATE "
            f"ts={int(getattr(bot, 'current_timestamp', 0) or 0)} "
            f"label={candidate_label} candidate={int(is_candidate)} side={candidate['side']} "
            f"entry={float(entry_price):.4f} close={float(close_price):.4f} "
            f"confirmation_score={confirmation_score:.4f} "
            f"exit_decision_pressure={exit_decision_pressure:.4f} plan_trust={plan_trust:.4f} "
            f"holding_stability={holding_stability:.4f} intervention_fitness={intervention_fitness:.4f} "
            f"intervention_unfit_state={intervention_unfit_state:.4f} exit_evidence={exit_evidence:.4f} "
            f"current_r={current_r:.4f} "
            f"target_expectation_context={str((target_expectation_state or {}).get('target_expectation_context', '-'))} "
            f"tp_reachability={float((target_expectation_state or {}).get('tp_reachability', 0.0) or 0.0):.4f} "
            f"expectation_break_pressure={float((target_expectation_state or {}).get('expectation_break_pressure', 0.0) or 0.0):.4f} "
            f"expectation_hold_support={float((target_expectation_state or {}).get('expectation_hold_support', 0.0) or 0.0):.4f} "
            f"target_recovery_potential={float((target_expectation_state or {}).get('target_recovery_potential', 0.0) or 0.0):.4f} "
            f"target_recovery_momentum={float((target_expectation_state or {}).get('target_recovery_momentum', 0.0) or 0.0):.4f} "
            f"target_recovery_confirmation={float((target_expectation_state or {}).get('target_recovery_confirmation', 0.0) or 0.0):.4f} "
            f"break_to_recovery_delta={float((target_expectation_state or {}).get('break_to_recovery_delta', 0.0) or 0.0):.4f} "
            f"expectation_break_persistence={float((target_expectation_state or {}).get('expectation_break_persistence', 0.0) or 0.0):.4f} "
            f"deep_retrace_recovery_watch={int(bool((target_expectation_state or {}).get('deep_retrace_recovery_watch', False)))} "
            f"recovery_after_break_watch={int(bool((target_expectation_state or {}).get('recovery_after_break_watch', False)))}",
            "mcm_exit_candidate_observe.csv",
        )

    if is_candidate:
        episode_marker(
            bot,
            "exit_candidate_observe",
            dict(candidate),
        )

    return candidate
