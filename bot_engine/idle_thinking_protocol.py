import os

from config import Config


def clip01(value):
    try:
        return float(max(0.0, min(1.0, float(value or 0.0))))
    except Exception:
        return 0.0


def resolve_idle_phase_from_state(
    reflection_need,
    replay_need,
    hypothesis_need,
    pause_maturity,
    depth_efficiency,
    decision_tendency,
    pre_action_phase="hold",
    plan_pressure=0.0,
    act_watch_readiness=0.0,
):
    if not bool(getattr(Config, "MCM_HYPOTHESIS_LEARNING_ENABLED", False)):
        hypothesis_need = 0.0

    phase = str(pre_action_phase or "").strip().lower()
    pressure = clip01(plan_pressure)
    readiness = clip01(act_watch_readiness)
    tendency = str(decision_tendency or "").lower()
    act_tendency = 1.0 if tendency == "act" else 0.0
    quiet_tendency = 1.0 if tendency in ("hold", "observe") else 0.0
    phase_trace = {
        "act_watch": clip01((readiness * 0.34) + (pressure * 0.28) + ((1.0 if phase == "act_watch" else 0.0) * 0.22) + (act_tendency * 0.12)),
        "plan_pressure": clip01((pressure * 0.46) + (act_tendency * 0.22) + (readiness * 0.12)),
        "pause": clip01((pause_maturity * 0.44) + (max(reflection_need, replay_need, hypothesis_need) * 0.12) + ((1.0 - depth_efficiency) * 0.10)),
        "replay": clip01((replay_need * 0.46) + (reflection_need * 0.12) + (hypothesis_need * 0.10)),
        "hypothesize": 0.0 if not bool(getattr(Config, "MCM_HYPOTHESIS_LEARNING_ENABLED", False)) else clip01((hypothesis_need * 0.48) + (reflection_need * 0.10) + (pressure * 0.08)),
        "reflect": clip01((reflection_need * 0.48) + (pause_maturity * 0.10) + ((1.0 - readiness) * 0.08)),
        "stabilize": clip01((depth_efficiency * 0.44) + (quiet_tendency * 0.18) + (pause_maturity * 0.08)),
        "hold": clip01(0.10 + ((1.0 - max(reflection_need, replay_need, hypothesis_need, pressure)) * 0.22) + (quiet_tendency * 0.10)),
    }
    return max(phase_trace, key=phase_trace.get)


def _num(source, key, default=0.0):
    try:
        return float((source or {}).get(key, default) or default)
    except Exception:
        return float(default)


def write_idle_thinking_protocol(
    bot,
    runtime_result,
    *,
    config,
    debug_enabled,
    dbr_path_func,
    dbr_append_text_func,
    dbr_debug_func,
):
    if not bool(getattr(config, "MCM_IDLE_THINKING_PROTOCOL_DEBUG", False)):
        return False

    result = dict(runtime_result or {})
    if not result:
        return False

    runtime_snapshot = dict(getattr(bot, "mcm_runtime_snapshot", {}) or {})
    timestamp = result.get("timestamp", runtime_snapshot.get("timestamp", getattr(bot, "current_timestamp", None)))
    runtime_tick_seq = int(result.get("runtime_tick_seq", runtime_snapshot.get("runtime_tick_seq", 0)) or 0)
    market_ticks = int(result.get("market_ticks", runtime_snapshot.get("market_ticks", getattr(bot, "mcm_runtime_market_ticks", 0))) or 0)
    decision_tendency = str(result.get("decision_tendency", runtime_snapshot.get("decision_tendency", "hold")) or "hold").lower()
    proposed_decision = str(result.get("proposed_decision", runtime_snapshot.get("proposed_decision", "WAIT")) or "WAIT").upper()

    thought_state = dict(result.get("thought_state", getattr(bot, "thought_state", {}) or {}) or {})
    meta_state = dict(result.get("meta_regulation_state", {}) or {})
    perception_state = dict(result.get("perception_state", {}) or {})
    form_symbol_state = dict(result.get("form_symbol_state", getattr(bot, "form_symbol_state", {}) or {}) or {})
    memory_state = dict(result.get("memory_complexity_state", {}) or {})
    if not memory_state:
        memory_state = dict((meta_state.get("memory_complexity_state", {}) or {}) or {})
    if not memory_state:
        memory_state = dict(getattr(bot, "last_memory_complexity_state", {}) or {})

    regulatory_load = clip01(result.get("regulatory_load", getattr(bot, "regulatory_load", 0.0)))
    action_capacity = clip01(result.get("action_capacity", getattr(bot, "action_capacity", 0.0)))
    recovery_need = clip01(result.get("recovery_need", getattr(bot, "recovery_need", 0.0)))
    survival_pressure = clip01(result.get("survival_pressure", getattr(bot, "survival_pressure", 0.0)))
    rumination_depth = clip01(_num(thought_state, "rumination_depth", 0.0))
    decision_conflict = clip01(_num(thought_state, "decision_conflict", 0.0))
    state_maturity = clip01(_num(thought_state, "state_maturity", 0.0))
    decision_readiness = clip01(_num(thought_state, "decision_readiness", 0.0))
    observe_priority = clip01(_num(perception_state, "observe_priority", 0.0))
    uncertainty_score = clip01(_num(perception_state, "uncertainty_score", 0.0))
    signal_quality = clip01(_num(perception_state, "signal_quality", 0.0))

    memory_compare_load = clip01(_num(memory_state, "memory_compare_load", 0.0))
    memory_support = clip01(_num(memory_state, "memory_support", 0.0))
    memory_inhibition = clip01(_num(memory_state, "memory_inhibition", 0.0))
    memory_conflict = clip01(_num(memory_state, "memory_conflict", 0.0))
    thinking_complexity = clip01(_num(memory_state, "thinking_complexity", 0.0))
    cognitive_load = clip01(_num(memory_state, "cognitive_load", 0.0))
    decision_energy_cost = clip01(_num(memory_state, "decision_energy_cost", 0.0))

    form_symbol_maturity = clip01(_num(form_symbol_state, "form_symbol_maturity", 0.0))
    form_symbol_zoom_need = clip01(_num(form_symbol_state, "form_symbol_zoom_need", 0.0))
    form_symbol_detail_pressure = clip01(_num(form_symbol_state, "form_symbol_detail_pressure", 0.0))
    form_symbol_containment = clip01(_num(form_symbol_state, "form_symbol_containment", 0.0))
    form_symbol_field_decoupling = clip01(_num(form_symbol_state, "form_symbol_field_decoupling", 0.0))
    pre_action_phase = str(meta_state.get("pre_action_phase", "hold") or "hold").strip().lower()
    plan_pressure = clip01(_num(meta_state, "plan_pressure", 0.0))
    act_watch_readiness = clip01(_num(meta_state, "act_watch_readiness", 0.0))
    structure_carrying_need = clip01(_num(meta_state, "structure_carrying_need", 0.0))

    load_gap = clip01(regulatory_load - action_capacity)
    reflection_need = clip01((decision_conflict * 0.30) + (cognitive_load * 0.24) + (load_gap * 0.22) + (rumination_depth * 0.16) + (uncertainty_score * 0.08))
    replay_need = clip01((memory_compare_load * 0.28) + (memory_conflict * 0.24) + (memory_support * 0.18) + (thinking_complexity * 0.16) + (max(0.0, 1.0 - form_symbol_maturity) * 0.08))
    hypothesis_need = clip01((form_symbol_zoom_need * 0.30) + (form_symbol_detail_pressure * 0.22) + (uncertainty_score * 0.18) + (observe_priority * 0.14) + (max(0.0, 1.0 - signal_quality) * 0.10))
    if not bool(getattr(config, "MCM_HYPOTHESIS_LEARNING_ENABLED", False)):
        hypothesis_need = 0.0
    pause_maturity = clip01((load_gap * 0.34) + (observe_priority * 0.24) + (recovery_need * 0.18) + (survival_pressure * 0.14) + (decision_conflict * 0.10) - (decision_readiness * 0.10))
    action_load_capacity = clip01(action_capacity - (regulatory_load * 0.48) - (decision_energy_cost * 0.22) + (state_maturity * 0.18))
    regulatory_self_control = clip01((pause_maturity * 0.32) + (reflection_need * 0.24) + (form_symbol_containment * 0.18) + (form_symbol_field_decoupling * 0.16) + (max(0.0, memory_inhibition - memory_support) * 0.10))
    parameter_dependency = clip01((max(0.0, 1.0 - form_symbol_maturity) * 0.26) + (decision_energy_cost * 0.20) + (cognitive_load * 0.18) + (uncertainty_score * 0.16) + (memory_inhibition * 0.12) - (form_symbol_containment * 0.10))
    self_regulation_maturity = clip01((state_maturity * 0.24) + (action_load_capacity * 0.22) + (form_symbol_containment * 0.18) + (form_symbol_field_decoupling * 0.14) + (memory_support * 0.12) - (load_gap * 0.14))
    depth_efficiency = clip01((state_maturity * 0.24) + (memory_support * 0.18) + (form_symbol_containment * 0.16) + (form_symbol_field_decoupling * 0.16) + (signal_quality * 0.14) - (cognitive_load * 0.18) - (memory_conflict * 0.10))
    cognitive_overcontrol = clip01((cognitive_load * 0.30) + (rumination_depth * 0.24) + (decision_energy_cost * 0.20) + (memory_compare_load * 0.14) - (depth_efficiency * 0.18))
    thinking_depth = clip01(max(rumination_depth, thinking_complexity, reflection_need, replay_need, hypothesis_need))
    action_depth = clip01((decision_energy_cost * 0.26) + (regulatory_load * 0.24) + (decision_conflict * 0.18) + ((1.0 if proposed_decision in ("LONG", "SHORT") else 0.0) * 0.16) + (max(0.0, 1.0 - action_capacity) * 0.16))
    adaptive_depth_shift = clip01(abs(thinking_depth - float(getattr(bot, "_idle_thinking_last_depth", 0.0) or 0.0)))
    bot._idle_thinking_last_depth = float(thinking_depth)

    idle_phase = resolve_idle_phase_from_state(
        reflection_need,
        replay_need,
        hypothesis_need,
        pause_maturity,
        depth_efficiency,
        decision_tendency,
        pre_action_phase=pre_action_phase,
        plan_pressure=plan_pressure,
        act_watch_readiness=act_watch_readiness,
    )
    state_key = (
        timestamp,
        idle_phase,
        round(thinking_depth, 2),
        round(regulatory_self_control, 2),
        round(parameter_dependency, 2),
        round(depth_efficiency, 2),
        round(plan_pressure, 2),
        round(act_watch_readiness, 2),
        pre_action_phase,
        decision_tendency,
        proposed_decision,
    )
    state_changed = state_key != bot._idle_thinking_last_state_key
    bot._idle_thinking_protocol_seq = int(getattr(bot, "_idle_thinking_protocol_seq", 0) or 0) + 1
    every_n = max(1, int(getattr(config, "MCM_IDLE_THINKING_PROTOCOL_EVERY_N", 5) or 5))
    if not state_changed and (bot._idle_thinking_protocol_seq % every_n) != 0:
        return False
    bot._idle_thinking_last_state_key = state_key

    path = dbr_path_func("mcm_idle_thinking_protocol.csv")
    try:
        header_key = "_idle_thinking_protocol_header_written"
        write_header = (not os.path.exists(path)) and not bool(getattr(bot, header_key, False))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        payload = ""
        if write_header:
            payload += (
                "timestamp;market_ticks;runtime_tick_sequence;idle_phase;state_changed;"
                "decision_tendency;proposed_decision;pre_action_phase;thinking_depth;action_depth;"
                "reflection_need;replay_need;hypothesis_need;pause_maturity;"
                "regulatory_self_control;parameter_dependency;self_regulation_maturity;"
                "cognitive_overcontrol;adaptive_depth_shift;action_load_capacity;"
                "depth_efficiency;plan_pressure;act_watch_readiness;structure_carrying_need;"
                "thinking_complexity;memory_compare_load;memory_support;"
                "memory_inhibition;memory_conflict;cognitive_load;decision_energy_cost;"
                "regulatory_load;action_capacity;recovery_need;survival_pressure;"
                "rumination_depth;decision_conflict;state_maturity;decision_readiness;"
                "observe_priority;uncertainty_score;signal_quality;form_symbol_id;"
                "form_symbol_maturity;form_symbol_zoom_need;form_symbol_containment;"
                "form_symbol_field_decoupling\n"
            )
            setattr(bot, header_key, True)

        form_symbol_id = str(form_symbol_state.get("form_symbol_id", "-") or "-").replace(";", "|")
        values = [
            timestamp,
            market_ticks,
            runtime_tick_seq,
            idle_phase,
            int(bool(state_changed)),
            decision_tendency,
            proposed_decision,
            pre_action_phase,
            thinking_depth,
            action_depth,
            reflection_need,
            replay_need,
            hypothesis_need,
            pause_maturity,
            regulatory_self_control,
            parameter_dependency,
            self_regulation_maturity,
            cognitive_overcontrol,
            adaptive_depth_shift,
            action_load_capacity,
            depth_efficiency,
            plan_pressure,
            act_watch_readiness,
            structure_carrying_need,
            thinking_complexity,
            memory_compare_load,
            memory_support,
            memory_inhibition,
            memory_conflict,
            cognitive_load,
            decision_energy_cost,
            regulatory_load,
            action_capacity,
            recovery_need,
            survival_pressure,
            rumination_depth,
            decision_conflict,
            state_maturity,
            decision_readiness,
            observe_priority,
            uncertainty_score,
            signal_quality,
            form_symbol_id,
            form_symbol_maturity,
            form_symbol_zoom_need,
            form_symbol_containment,
            form_symbol_field_decoupling,
        ]
        line = ";".join(
            f"{item:.4f}" if isinstance(item, float) else str(item)
            for item in values
        )
        payload += line + "\n"
        dbr_append_text_func(path, payload, operation="idle_thinking_protocol_append")
        return True
    except Exception as exc:
        if debug_enabled:
            dbr_debug_func(
                f"IDLE_THINKING_PROTOCOL_ERROR | {type(exc).__name__}:{str(exc).replace(';', '|')}",
                "mcm_idle_thinking_protocol_error.csv",
            )
        return False
