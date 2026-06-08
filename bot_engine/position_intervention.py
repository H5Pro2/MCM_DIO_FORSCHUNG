def build_position_intervention_state(
    bot,
    *,
    close_price: float,
    entry_price: float,
    side: str,
    risk_value: float,
    mfe_r: float,
    mae_r: float,
    fill_ratio: float,
    pressure_to_capacity: float,
    bars_open: int,
    config,
    debug_writer,
) -> dict:
    def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
        try:
            return max(lo, min(hi, float(value)))
        except Exception:
            return lo

    if risk_value <= 0.0:
        return {}

    side = str(side or "").upper().strip()
    if side == "LONG":
        current_r = (float(close_price) - float(entry_price)) / max(risk_value, 1e-9)
    elif side == "SHORT":
        current_r = (float(entry_price) - float(close_price)) / max(risk_value, 1e-9)
    else:
        current_r = 0.0

    giveback_r = max(0.0, float(mfe_r) - float(current_r))
    structure_quality = float((bot.structure_perception_state or {}).get("structure_quality", 0.0) or 0.0)
    structure_stability = float((bot.structure_perception_state or {}).get("structure_stability", structure_quality) or 0.0)
    context_confidence = float((bot.structure_perception_state or {}).get("context_confidence", structure_quality) or 0.0)
    regulatory_load = float(getattr(bot, "regulatory_load", 0.0) or 0.0)
    action_capacity = float(getattr(bot, "action_capacity", 0.0) or 0.0)
    recovery_need = float(getattr(bot, "recovery_need", 0.0) or 0.0)
    recovery_balance = float(getattr(bot, "recovery_balance", 0.0) or 0.0)
    survival_pressure = float(getattr(bot, "survival_pressure", 0.0) or 0.0)
    if pressure_to_capacity <= 0.0 and action_capacity > 0.0:
        pressure_to_capacity = regulatory_load / max(0.05, action_capacity)

    pressure_load = _clamp(float(pressure_to_capacity) / 2.25)
    giveback_load = _clamp(giveback_r / 2.50)
    adverse_load = _clamp(float(mae_r) / 1.20)
    recovery_load = _clamp(float(recovery_need) + max(0.0, -float(recovery_balance)))
    structure_loss = _clamp((0.62 - structure_quality) / 0.35)
    confidence_loss = _clamp((0.58 - context_confidence) / 0.35)
    negative_current_load = _clamp((-current_r) / 0.90)

    exit_decision_pressure = _clamp(
        (giveback_load * 0.30)
        + (structure_loss * 0.24)
        + (pressure_load * 0.20)
        + (negative_current_load * 0.16)
        + (adverse_load * 0.10)
    )
    position_cognitive_load = _clamp(
        (pressure_load * 0.24)
        + (regulatory_load * 0.20)
        + (recovery_load * 0.18)
        + (exit_decision_pressure * 0.18)
        + (survival_pressure * 0.10)
        + (_clamp(float(bars_open) / 64.0) * 0.10)
    )
    plan_trust = _clamp(
        (structure_quality * 0.26)
        + (structure_stability * 0.18)
        + (context_confidence * 0.16)
        + (_clamp(current_r / 1.40) * 0.14)
        + ((1.0 - pressure_load) * 0.12)
        + ((1.0 - giveback_load) * 0.10)
        + ((1.0 - recovery_load) * 0.04)
    )
    holding_stability = _clamp(
        (plan_trust * 0.46)
        + ((1.0 - exit_decision_pressure) * 0.24)
        + (_clamp(current_r / 1.75) * 0.16)
        + ((1.0 - position_cognitive_load) * 0.14)
    )
    inner_noise = _clamp(
        (position_cognitive_load * 0.32)
        + (exit_decision_pressure * 0.28)
        + (abs(plan_trust - exit_decision_pressure) * 0.14)
        + (confidence_loss * 0.14)
        + (_clamp(giveback_r / max(float(mfe_r), 0.25)) * 0.12)
    )

    contact_state = dict(getattr(bot, "active_mcm_contact_state", {}) or {})
    temporal_state = dict(getattr(bot, "temporal_perception_state", {}) or {})
    meta_state = dict(getattr(bot, "meta_regulation_state", {}) or {})
    contact_reality_check = _clamp(contact_state.get("contact_reality_check", 0.0))
    contact_temporal_bearing = _clamp(contact_state.get("contact_temporal_bearing", 0.0))
    contact_bearing_gap = _clamp(contact_state.get("contact_bearing_gap", 0.0))
    contact_action_maturity = _clamp(contact_state.get("contact_action_maturity", 0.0))
    contact_learning_need = _clamp(contact_state.get("contact_learning_need", 0.0))
    contact_overcoupling_risk = _clamp(contact_state.get("contact_overcoupling_risk", 0.0))
    temporal_self_location = _clamp(temporal_state.get("temporal_self_location", 0.0))
    spacetime_reflection_need = _clamp(meta_state.get("spacetime_reflection_need", 0.0))
    structure_action_uncertainty = _clamp(meta_state.get("structure_action_uncertainty", 0.0))

    position_self_trust_gap = _clamp(
        ((1.0 - plan_trust) * 0.22)
        + (contact_bearing_gap * 0.18)
        + ((1.0 - contact_reality_check) * 0.14)
        + ((1.0 - contact_temporal_bearing) * 0.12)
        + (structure_action_uncertainty * 0.12)
        + (negative_current_load * 0.10)
        + (giveback_load * 0.08)
        + ((1.0 - temporal_self_location) * 0.04)
    )
    position_inconsistency_stress = _clamp(
        (position_self_trust_gap * 0.26)
        + (position_cognitive_load * 0.20)
        + (exit_decision_pressure * 0.16)
        + (inner_noise * 0.14)
        + (adverse_load * 0.10)
        + (contact_learning_need * 0.08)
        + (spacetime_reflection_need * 0.06)
    )
    position_noradrenaline_arousal = _clamp(
        (exit_decision_pressure * 0.28)
        + (negative_current_load * 0.20)
        + (giveback_load * 0.18)
        + (contact_overcoupling_risk * 0.14)
        + (structure_action_uncertainty * 0.12)
        + (_clamp(float(bars_open) / 40.0) * 0.08)
    )
    prior_count = int(bot.position.get("intervention_pressure_count", 0) or 0) if bot.position else 0
    prior_sum = float(bot.position.get("intervention_pressure_sum", 0.0) or 0.0) if bot.position else 0.0
    pressure_count = prior_count + 1
    pressure_sum = prior_sum + float(exit_decision_pressure)
    sustained_exit_pressure = _clamp(pressure_sum / max(1, pressure_count))

    position_cortisol_load = _clamp(
        (position_inconsistency_stress * 0.32)
        + (position_cognitive_load * 0.22)
        + (sustained_exit_pressure * 0.18)
        + (recovery_load * 0.12)
        + (adverse_load * 0.08)
        + (spacetime_reflection_need * 0.08)
    )
    position_mcm_field_strain = _clamp(
        (position_cortisol_load * 0.26)
        + (position_noradrenaline_arousal * 0.22)
        + (contact_overcoupling_risk * 0.18)
        + (position_self_trust_gap * 0.16)
        + ((1.0 - holding_stability) * 0.10)
        + ((1.0 - temporal_self_location) * 0.08)
    )
    position_protective_distance = _clamp(
        (position_mcm_field_strain * 0.28)
        + (position_self_trust_gap * 0.22)
        + (position_cortisol_load * 0.18)
        + (spacetime_reflection_need * 0.14)
        + ((1.0 - contact_action_maturity) * 0.10)
        + ((1.0 - holding_stability) * 0.08)
    )
    position_held_risk_discomfort = _clamp(
        (adverse_load * 0.22)
        + (negative_current_load * 0.20)
        + (position_self_trust_gap * 0.18)
        + (position_noradrenaline_arousal * 0.16)
        + (position_cortisol_load * 0.14)
        + (giveback_load * 0.10)
    )
    position_process_quality = _clamp(
        (plan_trust * 0.22)
        + (holding_stability * 0.18)
        + (contact_reality_check * 0.14)
        + (contact_temporal_bearing * 0.12)
        + (contact_action_maturity * 0.10)
        + ((1.0 - position_inconsistency_stress) * 0.10)
        + ((1.0 - position_mcm_field_strain) * 0.08)
        + ((1.0 - position_held_risk_discomfort) * 0.06)
    )

    intervention_fatigue = _clamp(
        (sustained_exit_pressure * 0.48)
        + (_clamp(pressure_count / 48.0) * 0.20)
        + (position_cognitive_load * 0.20)
        + (inner_noise * 0.12)
    )
    intervention_unfit_state = _clamp(
        (position_cognitive_load * 0.34)
        + (inner_noise * 0.24)
        + ((1.0 - plan_trust) * 0.20)
        + (intervention_fatigue * 0.14)
        + ((1.0 - holding_stability) * 0.08)
    )
    exit_evidence = _clamp(
        (structure_loss * 0.30)
        + (giveback_load * 0.26)
        + (negative_current_load * 0.20)
        + (pressure_load * 0.16)
        + (adverse_load * 0.08)
    )
    intervention_fitness = _clamp(exit_evidence * (1.0 - (intervention_unfit_state * 0.65)))

    if bot.position is not None:
        bot.position["intervention_pressure_count"] = int(pressure_count)
        bot.position["intervention_pressure_sum"] = float(pressure_sum)

    intervention_label_pressures = {
        "confirmed_exit_candidate": _clamp((intervention_fitness * 0.34) + (exit_decision_pressure * 0.26)),
        "intervention_unfit_state": _clamp((intervention_unfit_state * 0.34) + (exit_decision_pressure * 0.14)),
        "plan_holding_trust": _clamp((plan_trust * 0.30) + (holding_stability * 0.24)),
        "exit_nervousness_observe": _clamp((exit_decision_pressure * 0.30) + (position_cognitive_load * 0.08)),
        "quiet_position_watch": _clamp((1.0 - max(exit_decision_pressure, intervention_fitness, intervention_unfit_state)) * 0.24),
    }
    intervention_label = max(intervention_label_pressures, key=intervention_label_pressures.get)

    position_experience_pressures = {
        "carried_position_contact": _clamp((position_process_quality * 0.34) + ((1.0 - position_mcm_field_strain) * 0.14)),
        "unearned_relief_watch": _clamp((max(0.0, current_r) * 0.20) + ((1.0 - position_process_quality) * 0.18)),
        "protective_stress_contact": _clamp((position_cortisol_load * 0.26) + (position_held_risk_discomfort * 0.26)),
        "self_trust_gap_contact": _clamp(position_self_trust_gap * 0.34),
        "protective_distance_watch": _clamp(position_protective_distance * 0.34),
        "open_position_feel": _clamp((1.0 - max(position_process_quality, position_cortisol_load, position_held_risk_discomfort, position_self_trust_gap)) * 0.22),
    }
    position_experience_label = max(position_experience_pressures, key=position_experience_pressures.get)

    position_experience_state = {
        "position_inconsistency_stress": float(position_inconsistency_stress),
        "position_mcm_field_strain": float(position_mcm_field_strain),
        "position_self_trust_gap": float(position_self_trust_gap),
        "position_cortisol_load": float(position_cortisol_load),
        "position_noradrenaline_arousal": float(position_noradrenaline_arousal),
        "position_protective_distance": float(position_protective_distance),
        "position_held_risk_discomfort": float(position_held_risk_discomfort),
        "position_process_quality": float(position_process_quality),
        "position_experience_label": str(position_experience_label),
        "position_experience_pressures": dict(position_experience_pressures),
    }

    state = {
        "position_cognitive_load": float(position_cognitive_load),
        "exit_decision_pressure": float(exit_decision_pressure),
        "holding_stability": float(holding_stability),
        "plan_trust": float(plan_trust),
        "intervention_fatigue": float(intervention_fatigue),
        "inner_noise": float(inner_noise),
        "intervention_fitness": float(intervention_fitness),
        "intervention_unfit_state": float(intervention_unfit_state),
        "exit_evidence": float(exit_evidence),
        "intervention_label_pressures": dict(intervention_label_pressures),
        "sustained_exit_pressure": float(sustained_exit_pressure),
        "current_r": float(current_r),
        "giveback_r": float(giveback_r),
        "mfe_r": float(mfe_r),
        "mae_r": float(mae_r),
        "pressure_to_capacity": float(pressure_to_capacity),
        "structure_quality": float(structure_quality),
        "structure_stability": float(structure_stability),
        "context_confidence": float(context_confidence),
        "bars_open": int(bars_open),
        "intervention_label": str(intervention_label),
        "position_inconsistency_stress": float(position_inconsistency_stress),
        "position_mcm_field_strain": float(position_mcm_field_strain),
        "position_self_trust_gap": float(position_self_trust_gap),
        "position_cortisol_load": float(position_cortisol_load),
        "position_noradrenaline_arousal": float(position_noradrenaline_arousal),
        "position_protective_distance": float(position_protective_distance),
        "position_held_risk_discomfort": float(position_held_risk_discomfort),
        "position_process_quality": float(position_process_quality),
        "position_experience_label": str(position_experience_label),
        "position_experience_state": dict(position_experience_state),
    }

    if bool(getattr(config, "MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG", True)):
        every_n = max(1, int(getattr(config, "MCM_POSITION_INTERVENTION_PROTOCOL_EVERY_N", 5) or 5))
        should_write = (int(getattr(bot, "processed", 0) or 0) % every_n == 0) or intervention_label != "quiet_position_watch"
        if should_write:
            debug_writer(
                "POSITION_INTERVENTION "
                f"ts={int(getattr(bot, 'current_timestamp', 0) or 0)} side={side} "
                f"entry={float(entry_price):.4f} close={float(close_price):.4f} "
                f"current_r={current_r:.4f} mfe_r={float(mfe_r):.4f} mae_r={float(mae_r):.4f} "
                f"giveback_r={giveback_r:.4f} position_cognitive_load={position_cognitive_load:.4f} "
                f"exit_decision_pressure={exit_decision_pressure:.4f} plan_trust={plan_trust:.4f} "
                f"holding_stability={holding_stability:.4f} intervention_fatigue={intervention_fatigue:.4f} "
                f"inner_noise={inner_noise:.4f} intervention_unfit_state={intervention_unfit_state:.4f} "
                f"intervention_fitness={intervention_fitness:.4f} label={intervention_label} "
                f"position_inconsistency_stress={position_inconsistency_stress:.4f} "
                f"position_mcm_field_strain={position_mcm_field_strain:.4f} "
                f"position_self_trust_gap={position_self_trust_gap:.4f} "
                f"position_cortisol_load={position_cortisol_load:.4f} "
                f"position_noradrenaline_arousal={position_noradrenaline_arousal:.4f} "
                f"position_protective_distance={position_protective_distance:.4f} "
                f"position_held_risk_discomfort={position_held_risk_discomfort:.4f} "
                f"position_process_quality={position_process_quality:.4f} "
                f"position_experience_label={position_experience_label}",
                "mcm_position_intervention_protocol.csv",
            )

    return state
