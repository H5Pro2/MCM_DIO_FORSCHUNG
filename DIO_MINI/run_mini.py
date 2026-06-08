"""Run the isolated mini DIO episodic core."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from config import Config
from DIO_MINI.mcm_neuron import ACTION_NAMES, MiniMCMField
from DIO_MINI.mini_world import best_future_action, build_senses, evaluate_future, evaluate_trade_event, load_candles
from DIO_MINI.neuro_state import build_mini_neuro_state
from DIO_MINI.semantic_memory import SemanticMemory, make_syntax_symbol, make_syntax_vector
from DIO_MINI.temporal_memory import MiniTemporalTracker


def _clip(value: float, lo: float = -1.0, hi: float = 1.0) -> float:
    try:
        value = float(value)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return max(lo, min(hi, value))


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def load_passive_world_carrying_state(memory_path: Path | None, world_label: str) -> dict:
    """Load passive world-reife diagnostics for debug output only."""

    if memory_path is None or not world_label or not memory_path.exists():
        return {}
    try:
        payload = json.loads(memory_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    worlds = dict(payload.get("worlds", {}) or {})
    return dict(worlds.get(world_label, {}) or {})


def load_passive_inner_awareness_state(memory_path: Path | None) -> dict:
    """Load passive inner-awareness entries for debug output only."""

    if memory_path is None or not memory_path.exists():
        return {}
    try:
        payload = json.loads(memory_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    boundary = dict(payload.get("boundary", {}) or {})
    if not bool(boundary.get("passive_only", False)):
        return {}
    if bool(boundary.get("influences_action", True)):
        return {}
    if bool(boundary.get("is_gate", True)) or bool(boundary.get("is_motoric", True)):
        return {}
    by_family = {}
    for entry in payload.get("entries", []) or []:
        family = str(entry.get("symbol_family", "") or "")
        if family:
            by_family[family] = dict(entry)
    return by_family


def passive_world_debug_fields(world_label: str, world_state: dict) -> dict:
    """Return per-episode passive world fields without action coupling."""

    last = dict(world_state.get("last", {}) or {})
    return {
        "passive_world_label": world_label or "-",
        "passive_world_observations": int(world_state.get("observations", 0) or 0),
        "passive_world_mean_avg_carry": f"{_safe_float(world_state.get('mean_avg_carry')):.6f}",
        "passive_world_mean_avg_carried_cos": f"{_safe_float(world_state.get('mean_avg_carried_cos')):.6f}",
        "passive_world_best_max_carry": f"{_safe_float(world_state.get('best_max_carry')):.6f}",
        "passive_world_best_max_carried_cos": f"{_safe_float(world_state.get('best_max_carried_cos')):.6f}",
        "passive_world_positive_carried_cos_count": int(last.get("positive_carried_cos_family_count", 0) or 0),
        "passive_world_avg_readiness": f"{_safe_float(last.get('avg_readiness')):.6f}",
        "passive_world_passive_only": 1 if world_state else 0,
    }


def passive_inner_awareness_debug_fields(symbol_family: str, inner_state: dict) -> dict:
    """Return passive inner-awareness fields without action coupling."""

    state = dict(inner_state or {})
    return {
        "passive_inner_awareness_loaded": 1 if state else 0,
        "passive_inner_awareness_state": str(state.get("inner_awareness_state", "-") or "-"),
        "passive_inner_awareness_direction": str(state.get("dominant_direction", "NONE") or "NONE"),
        "passive_inner_awareness_observations": int(state.get("observation_count", 0) or 0),
        "passive_inner_awareness_afterlook": f"{_safe_float(state.get('avg_afterlook_best_reward')):.6f}",
        "passive_inner_awareness_carry": f"{_safe_float(state.get('avg_reflection_carry')):.6f}",
        "passive_inner_awareness_world_carry": f"{_safe_float(state.get('avg_world_carry')):.6f}",
        "passive_inner_awareness_passive_only": 1 if bool(state.get("passive_only", False)) else 0,
        "passive_inner_awareness_is_gate": 1 if bool(state.get("is_gate", False)) else 0,
        "passive_inner_awareness_is_motoric": 1 if bool(state.get("is_motoric", False)) else 0,
        "passive_inner_awareness_influences_action": 1 if bool(state.get("influences_action", False)) else 0,
        "passive_inner_awareness_symbol_family": symbol_family or "-",
    }


def build_reflection_context_state(
    passive_world_state: dict,
    trade_readiness: float,
    observation_learning_pressure: float,
    neuro_state: dict,
) -> dict:
    """Compress passive world context and current inner state for debug only."""

    world_carry = _clip(_safe_float(passive_world_state.get("mean_avg_carry")), 0.0, 1.0)
    world_cos = _clip(_safe_float(passive_world_state.get("mean_avg_carried_cos")), -1.0, 1.0)
    positive_world_cos = max(0.0, world_cos)
    negative_world_cos = max(0.0, -world_cos)
    neuro_balance = _clip(_safe_float(neuro_state.get("mini_neuro_balance")), 0.0, 1.0)
    neuro_support = _clip(_safe_float(neuro_state.get("mini_neuro_support")), 0.0, 1.0)
    neuro_load = _clip(_safe_float(neuro_state.get("mini_neuro_load")), 0.0, 1.0)
    readiness = _clip(_safe_float(trade_readiness), 0.0, 1.0)
    observation_pressure = _clip(_safe_float(observation_learning_pressure), 0.0, 1.0)
    world_support = _clip((world_carry * 0.45) + (positive_world_cos * 0.35) + (neuro_balance * 0.20), 0.0, 1.0)
    current_support = _clip((readiness * 0.40) + (observation_pressure * 0.30) + (neuro_support * 0.30), 0.0, 1.0)
    reflection_carry = _clip((world_support * 0.55) + (current_support * 0.45), 0.0, 1.0)
    reflection_strain = _clip(
        (negative_world_cos * 0.42)
        + (neuro_load * 0.34)
        + ((1.0 - world_support) * 0.14)
        + ((1.0 - current_support) * 0.10),
        0.0,
        1.0,
    )
    reflection_alignment = _clip(1.0 - abs(world_support - current_support), 0.0, 1.0)
    if not passive_world_state:
        tone = "reflection_context_unloaded"
    elif reflection_carry >= reflection_strain:
        tone = "reflection_context_carried"
    else:
        tone = "reflection_context_cautious"
    return {
        "reflection_context_state": tone,
        "reflection_context_carry": reflection_carry,
        "reflection_context_strain": reflection_strain,
        "reflection_context_alignment": reflection_alignment,
        "reflection_world_support": world_support,
        "reflection_current_support": current_support,
    }


def entry_improvement_room(action: str, entry_price: float, better_entry: float) -> float:
    if entry_price <= 0.0:
        return 0.0
    if action == "LONG":
        return max(0.0, entry_price - better_entry) / entry_price
    if action == "SHORT":
        return max(0.0, better_entry - entry_price) / entry_price
    return 0.0


def _positive_band(value: float) -> float:
    """Map an internal -1..1 state to a soft 0..1 support band."""

    return _clip((float(value or 0.0) + 1.0) * 0.5, 0.0, 1.0)


def _organic_action_pressure(action: str, base: float, bias: float, readiness: dict) -> dict:
    """Return soft action pressure without fixed accept/reject thresholds.

    The active core still needs numerical coupling, but this avoids "below X
    means blocked" logic. Low support becomes a continuous pressure instead of
    a hard rule.
    """

    raw_trade_signal = abs(float(base or 0.0) + float(bias or 0.0))
    best_trade_readiness = max(float(readiness["LONG"]), float(readiness["SHORT"]))
    trade_support = _positive_band(best_trade_readiness)
    wait_bias = 0.0
    trade_caution = 0.0
    memory_support_pressure = 0.0
    signal_diffusion_pressure = 0.0
    if action == "WAIT":
        wait_bias = (1.0 - trade_support) * 0.045
    elif action in ("LONG", "SHORT"):
        action_support = _positive_band(float(readiness[action]))
        signal_support = _clip(raw_trade_signal / (raw_trade_signal + 0.12), 0.0, 1.0)
        memory_support_pressure = (1.0 - action_support) * 0.040
        signal_diffusion_pressure = (1.0 - signal_support) * 0.030
        trade_caution = memory_support_pressure + signal_diffusion_pressure
    return {
        "raw_trade_signal": raw_trade_signal,
        "wait_bias": wait_bias,
        "trade_caution": trade_caution,
        "memory_support_pressure": memory_support_pressure,
        "signal_diffusion_pressure": signal_diffusion_pressure,
    }


def _observation_recognition_pressure(senses: dict, associative_trade: float, maturity_gap: float) -> float:
    """Soft recognition strength for seen-but-unacted learning.

    This does not make a trade and does not increase direct action trust. It
    only gives memory.learn_observation a continuous sense of how clearly the
    current sehen/fuehlen state was noticed.
    """

    sehen = dict(senses.get("sehen", {}) or {})
    fuehlen = dict(senses.get("fuehlen", {}) or {})
    flow_presence = abs(float(sehen.get("form_flow", 0.0) or 0.0))
    form_stability = _positive_band(float(sehen.get("form_stability", 0.0) or 0.0))
    coherence = _positive_band(float(fuehlen.get("mcm_coherence", 0.0) or 0.0))
    tension_room = 1.0 - _clip(float(fuehlen.get("mcm_tension", 0.0) or 0.0), 0.0, 1.0)
    sensory_presence = _clip(
        (flow_presence * 0.25)
        + (form_stability * 0.25)
        + (coherence * 0.30)
        + (tension_room * 0.20),
        0.0,
        1.0,
    )
    memory_presence = _clip(
        (max(0.0, float(associative_trade or 0.0)) * 0.40)
        + (max(0.0, float(maturity_gap or 0.0)) * 0.60),
        0.0,
        1.0,
    )
    return _clip((sensory_presence * 0.72) + (memory_presence * 0.28), 0.0, 1.0)


def choose_action(action_scores: dict, memory: SemanticMemory, symbol: str, vector: list[float]) -> tuple[str, dict, dict]:
    scores = {}
    diagnostics = {
        action: memory.action_diagnostics(symbol, action, vector=vector)
        for action in ACTION_NAMES
    }
    readiness = {
        action: float(diagnostics[action].get("readiness", 0.0) or 0.0)
        for action in ACTION_NAMES
    }
    for action in ACTION_NAMES:
        base = float(action_scores.get(action, 0.0) or 0.0)
        bias = float(diagnostics[action].get("action_bias", 0.0) or 0.0)
        pressure = _organic_action_pressure(action, base, bias, readiness)
        wait_bias = float(pressure["wait_bias"])
        raw_trade_signal = float(pressure["raw_trade_signal"])
        trade_caution = float(pressure["trade_caution"])
        scores[action] = base + bias + wait_bias - trade_caution
        diagnostics[action]["base_score"] = base
        diagnostics[action]["wait_bias"] = wait_bias
        diagnostics[action]["raw_trade_signal"] = raw_trade_signal
        diagnostics[action]["immature_memory_pressure"] = float(pressure["memory_support_pressure"])
        diagnostics[action]["weak_signal_pressure"] = float(pressure["signal_diffusion_pressure"])
        diagnostics[action]["memory_support_pressure"] = float(pressure["memory_support_pressure"])
        diagnostics[action]["signal_diffusion_pressure"] = float(pressure["signal_diffusion_pressure"])
        diagnostics[action]["trade_caution"] = trade_caution
        diagnostics[action]["final_score"] = scores[action]
    action = max(scores, key=scores.get)
    return action, scores, diagnostics


def sensory_distance(left: dict, right: dict) -> float:
    if not left or not right:
        return 1.0
    keys = [
        ("sehen", "form_flow"),
        ("sehen", "form_stability"),
        ("sehen", "form_change"),
        ("hoeren", "energy_tone"),
        ("hoeren", "energy_shift"),
        ("fuehlen", "mcm_coherence"),
        ("fuehlen", "mcm_tension"),
        ("fuehlen", "mcm_asymmetry"),
    ]
    distance = 0.0
    for root, key in keys:
        distance += abs(
            float(dict(left.get(root, {}) or {}).get(key, 0.0) or 0.0)
            - float(dict(right.get(root, {}) or {}).get(key, 0.0) or 0.0)
        )
    return distance / max(1, len(keys))


def episode_binding_state(active_phase: dict, action: str, senses: dict, scores: dict, index: int, horizon: int) -> dict:
    active_action = str(active_phase.get("action", "WAIT") or "WAIT").upper()
    action = str(action or "WAIT").upper()
    phase_distance = sensory_distance(senses, dict(active_phase.get("senses", {}) or {}))
    started_at = int(active_phase.get("started_at", -1) or -1)
    phase_age = index - started_at if started_at >= 0 else 9999
    phase_window = max(1, int(horizon) + 2)
    same_action = active_action in ("LONG", "SHORT") and action == active_action
    in_afterimage = phase_age <= phase_window
    coherence = abs(float(dict(senses.get("fuehlen", {}) or {}).get("mcm_coherence", 0.0) or 0.0))
    tension = float(dict(senses.get("fuehlen", {}) or {}).get("mcm_tension", 0.0) or 0.0)
    trade_score = float(scores.get(action, 0.0) or 0.0)
    wait_score = float(scores.get("WAIT", 0.0) or 0.0)
    score_gap = max(0.0, trade_score - wait_score)
    time_residue = max(0.0, 1.0 - (phase_age / phase_window)) if in_afterimage else 0.0
    binding_pressure = 0.0
    release_pressure = 1.0
    relation = "none"
    if same_action and in_afterimage:
        binding_pressure = _clip(
            ((1.0 - phase_distance) * 0.46)
            + (time_residue * 0.24)
            + (coherence * 0.18)
            + ((1.0 - min(1.0, tension)) * 0.12),
            0.0,
            1.0,
        )
        release_pressure = _clip((phase_distance * 0.30) + (score_gap * 0.70), 0.0, 1.0)
        relation = "same_episode" if binding_pressure > release_pressure else "new_contact"
    elif active_action in ("LONG", "SHORT") and in_afterimage:
        relation = "different_contact"
        release_pressure = 1.0
    return {
        "phase_distance": phase_distance,
        "phase_age": phase_age,
        "episode_binding_pressure": binding_pressure,
        "episode_release_pressure": release_pressure,
        "episode_relation": relation,
        "phase_active": same_action and in_afterimage and binding_pressure > release_pressure,
    }


def run_once(
    data_path: Path,
    memory: SemanticMemory,
    run_index: int,
    debug_root: Path,
    passive_world_label: str = "",
    passive_world_state: dict | None = None,
    passive_inner_awareness_by_family: dict | None = None,
) -> dict:
    candles = load_candles(data_path)
    field = MiniMCMField(neuron_count=getattr(Config, "DIO_MINI_MCM_NEURON_COUNT", 12))
    debug_dir = debug_root / f"dio_mini_lauf_{run_index}"
    debug_dir.mkdir(parents=True, exist_ok=True)
    episode_path = debug_dir / "episodes.csv"
    passive_world_state = dict(passive_world_state or {})
    passive_inner_awareness_by_family = dict(passive_inner_awareness_by_family or {})
    passive_world_fields = passive_world_debug_fields(passive_world_label, passive_world_state)

    rows = []
    trades = 0
    long_trades = 0
    short_trades = 0
    total_reward = 0.0
    correct_direction = 0
    actionable_seen = 0
    outcome_event_counter = {}
    trade_readiness_values = []
    associative_trade_values = []
    maturity_gap_values = []
    mature_transfer_values = []
    temporal_afterimage_values = []
    temporal_trust_values = []
    temporal_caution_values = []
    neuro_balance_values = []
    neuro_load_values = []
    neuro_support_values = []
    neuro_tone_counter = {}
    reflection_carry_values = []
    reflection_strain_values = []
    reflection_alignment_values = []
    reflection_context_counter = {}
    passive_inner_awareness_counter = {}
    observation_learning_values = []
    observation_signal_values = []
    observation_readiness_values = []
    observation_learning_events = 0
    symbol_counter = {}
    active_phase = {
        "action": "WAIT",
        "symbol_family": "-",
        "started_at": -1,
        "senses": {},
        "cooldown": 0,
    }

    index = 1
    horizon = 5
    temporal_tracker = MiniTemporalTracker()
    while index < max(1, len(candles) - horizon):
        senses = build_senses(candles, index)
        field_state = field.step(senses)
        syntax_vector = make_syntax_vector(senses, field_state["signature"])
        symbol = make_syntax_symbol(senses, field_state["signature"])
        action, scores, diagnostics = choose_action(field_state["action_scores"], memory, symbol, syntax_vector)
        record = memory.symbol_record(symbol)
        symbol_family = str(record.get("syntax_family", symbol[:8]) or symbol[:8])
        passive_inner_awareness_state = dict(passive_inner_awareness_by_family.get(symbol_family, {}) or {})
        passive_inner_state_name = str(passive_inner_awareness_state.get("inner_awareness_state", "unloaded") or "unloaded")
        passive_inner_awareness_counter[passive_inner_state_name] = (
            int(passive_inner_awareness_counter.get(passive_inner_state_name, 0) or 0) + 1
        )
        temporal_state = temporal_tracker.step(symbol_family, index, syntax_vector)
        memory.store_temporal_family(symbol_family, temporal_state)
        temporal_afterimage_values.append(float(temporal_state["mini_afterimage"]))
        temporal_trust_values.append(float(temporal_state["mini_temporal_trust_support"]))
        temporal_caution_values.append(float(temporal_state["mini_temporal_caution_support"]))
        raw_action = action
        trade_readiness = max(
            float(diagnostics["LONG"].get("readiness", 0.0) or 0.0),
            float(diagnostics["SHORT"].get("readiness", 0.0) or 0.0),
        )
        associative_trade = max(
            float(diagnostics["LONG"].get("associative_raw", 0.0) or 0.0),
            float(diagnostics["SHORT"].get("associative_raw", 0.0) or 0.0),
        )
        observation_trade_signal = max(
            float(diagnostics["LONG"].get("observation_signal", 0.0) or 0.0),
            float(diagnostics["SHORT"].get("observation_signal", 0.0) or 0.0),
        )
        observation_trade_readiness = max(
            float(diagnostics["LONG"].get("observation_readiness", 0.0) or 0.0),
            float(diagnostics["SHORT"].get("observation_readiness", 0.0) or 0.0),
        )
        maturity_gap = max(0.0, associative_trade - trade_readiness)
        mature_transfer = min(max(0.0, associative_trade), max(0.0, trade_readiness))
        trade_readiness_values.append(trade_readiness)
        associative_trade_values.append(associative_trade)
        maturity_gap_values.append(maturity_gap)
        mature_transfer_values.append(mature_transfer)
        observation_signal_values.append(observation_trade_signal)
        observation_readiness_values.append(observation_trade_readiness)
        binding_state = episode_binding_state(active_phase, action, senses, scores, index, horizon)
        phase_distance = float(binding_state["phase_distance"])
        phase_active = bool(binding_state["phase_active"])
        if phase_active:
            action = "WAIT"
        best_action, best_reward = best_future_action(candles, index)
        outcome = evaluate_future(candles, index, action)
        trade_event = evaluate_trade_event(candles, index, action, horizon=horizon)
        reward = float(trade_event["event_reward"]) if action in ("LONG", "SHORT") else float(outcome["reward"])
        entry_price = float(candles[index]["close"])
        timing_improvement = entry_improvement_room(action, entry_price, float(outcome["better_entry"]))
        outcome_event = str(trade_event.get("outcome_event", "NO_TRADE") or "NO_TRADE")
        outcome_event_counter[outcome_event] = int(outcome_event_counter.get(outcome_event, 0) or 0) + 1
        neuro_state = build_mini_neuro_state(
            senses=senses,
            diagnostics=diagnostics,
            temporal_state=temporal_state,
            action=action,
            reward=reward,
            outcome_event=outcome_event,
        )
        neuro_balance_values.append(float(neuro_state["mini_neuro_balance"]))
        neuro_load_values.append(float(neuro_state["mini_neuro_load"]))
        neuro_support_values.append(float(neuro_state["mini_neuro_support"]))
        neuro_tone = str(neuro_state["mini_neuro_dominant_tone"])
        neuro_tone_counter[neuro_tone] = int(neuro_tone_counter.get(neuro_tone, 0) or 0) + 1

        if best_action != "WAIT":
            actionable_seen += 1
        if action in ("LONG", "SHORT"):
            trades += 1
            long_trades += 1 if action == "LONG" else 0
            short_trades += 1 if action == "SHORT" else 0
        if action == best_action and best_action != "WAIT":
            correct_direction += 1

        total_reward += reward
        memory.learn(symbol, action, reward, vector=syntax_vector, timing_improvement=timing_improvement)
        observation_learning_pressure = 0.0
        observation_learning_action = "-"
        if action == "WAIT" and best_action in ("LONG", "SHORT") and best_reward > 0.0:
            observation_learning_pressure = _observation_recognition_pressure(
                senses,
                associative_trade,
                maturity_gap,
            )
            if observation_learning_pressure > 0.0:
                observation_learning_action = best_action
                observation_learning_events += 1
                observation_learning_values.append(observation_learning_pressure)
                memory.learn_observation(
                    symbol,
                    best_action,
                    best_reward,
                    observation_learning_pressure,
                    vector=syntax_vector,
                )
        field.learn(field_state["flat"], action, reward)
        reflection_context = build_reflection_context_state(
            passive_world_state,
            trade_readiness,
            observation_learning_pressure,
            neuro_state,
        )
        reflection_state = str(reflection_context["reflection_context_state"])
        reflection_context_counter[reflection_state] = int(reflection_context_counter.get(reflection_state, 0) or 0) + 1
        reflection_carry_values.append(float(reflection_context["reflection_context_carry"]))
        reflection_strain_values.append(float(reflection_context["reflection_context_strain"]))
        reflection_alignment_values.append(float(reflection_context["reflection_context_alignment"]))

        symbol_counter[symbol] = symbol_counter.get(symbol, 0) + 1
        rows.append(
            {
                "tick": index,
                "timestamp_ms": candles[index]["timestamp_ms"],
                "symbol": symbol,
                "symbol_family": symbol_family,
                **passive_world_fields,
                **passive_inner_awareness_debug_fields(symbol_family, passive_inner_awareness_state),
                "reflection_context_state": reflection_context["reflection_context_state"],
                "reflection_context_carry": f"{float(reflection_context['reflection_context_carry']):.6f}",
                "reflection_context_strain": f"{float(reflection_context['reflection_context_strain']):.6f}",
                "reflection_context_alignment": f"{float(reflection_context['reflection_context_alignment']):.6f}",
                "reflection_world_support": f"{float(reflection_context['reflection_world_support']):.6f}",
                "reflection_current_support": f"{float(reflection_context['reflection_current_support']):.6f}",
                "action": action,
                "raw_action": raw_action,
                "phase_active": int(phase_active),
                "phase_distance": f"{phase_distance:.6f}",
                "phase_age": binding_state["phase_age"],
                "episode_binding_pressure": f"{float(binding_state['episode_binding_pressure']):.6f}",
                "episode_release_pressure": f"{float(binding_state['episode_release_pressure']):.6f}",
                "episode_relation": binding_state["episode_relation"],
                "mini_temporal_state": temporal_state["mini_temporal_state"],
                "mini_family_age": int(temporal_state["mini_family_age"]),
                "mini_ticks_since_family_seen": int(temporal_state["mini_ticks_since_family_seen"]),
                "mini_recurrence_strength": f"{float(temporal_state['mini_recurrence_strength']):.6f}",
                "mini_afterimage": f"{float(temporal_state['mini_afterimage']):.6f}",
                "mini_time_distance": f"{float(temporal_state['mini_time_distance']):.6f}",
                "mini_temporal_form_distance": f"{float(temporal_state['mini_temporal_form_distance']):.6f}",
                "mini_temporal_trust_support": f"{float(temporal_state['mini_temporal_trust_support']):.6f}",
                "mini_temporal_caution_support": f"{float(temporal_state['mini_temporal_caution_support']):.6f}",
                "mini_neuro_dominant_tone": neuro_state["mini_neuro_dominant_tone"],
                "mini_focus_tone": f"{float(neuro_state['mini_focus_tone']):.6f}",
                "mini_trust_tone": f"{float(neuro_state['mini_trust_tone']):.6f}",
                "mini_caution_tone": f"{float(neuro_state['mini_caution_tone']):.6f}",
                "mini_strain_tone": f"{float(neuro_state['mini_strain_tone']):.6f}",
                "mini_relief_tone": f"{float(neuro_state['mini_relief_tone']):.6f}",
                "mini_observation_tone": f"{float(neuro_state['mini_observation_tone']):.6f}",
                "mini_neuro_support": f"{float(neuro_state['mini_neuro_support']):.6f}",
                "mini_neuro_load": f"{float(neuro_state['mini_neuro_load']):.6f}",
                "mini_neuro_balance": f"{float(neuro_state['mini_neuro_balance']):.6f}",
                "best_action_training": best_action,
                "reward": f"{reward:.6f}",
                "close_reward": f"{float(outcome['reward']):.6f}",
                "best_reward_training": f"{best_reward:.6f}",
                "outcome_event": outcome_event,
                "event_reward": f"{float(trade_event.get('event_reward', 0.0) or 0.0):.6f}",
                "event_raw_return": f"{float(trade_event.get('event_raw_return', 0.0) or 0.0):.6f}",
                "entry_price": f"{entry_price:.8f}",
                "tp_price": f"{float(trade_event.get('tp_price', entry_price) or entry_price):.8f}",
                "sl_price": f"{float(trade_event.get('sl_price', entry_price) or entry_price):.8f}",
                "exit_price": f"{float(trade_event.get('exit_price', entry_price) or entry_price):.8f}",
                "bars_held": int(trade_event.get("bars_held", 0) or 0),
                "better_entry_training": f"{float(outcome['better_entry']):.8f}",
                "entry_improvement_room": f"{timing_improvement:.6f}",
                "score_wait": f"{scores['WAIT']:.6f}",
                "score_long": f"{scores['LONG']:.6f}",
                "score_short": f"{scores['SHORT']:.6f}",
                "base_score_wait": f"{float(diagnostics['WAIT'].get('base_score', 0.0) or 0.0):.6f}",
                "base_score_long": f"{float(diagnostics['LONG'].get('base_score', 0.0) or 0.0):.6f}",
                "base_score_short": f"{float(diagnostics['SHORT'].get('base_score', 0.0) or 0.0):.6f}",
                "wait_bias": f"{float(diagnostics['WAIT'].get('wait_bias', 0.0) or 0.0):.6f}",
                "trade_caution_long": f"{float(diagnostics['LONG'].get('trade_caution', 0.0) or 0.0):.6f}",
                "trade_caution_short": f"{float(diagnostics['SHORT'].get('trade_caution', 0.0) or 0.0):.6f}",
                "immature_memory_pressure_long": f"{float(diagnostics['LONG'].get('immature_memory_pressure', 0.0) or 0.0):.6f}",
                "immature_memory_pressure_short": f"{float(diagnostics['SHORT'].get('immature_memory_pressure', 0.0) or 0.0):.6f}",
                "weak_signal_pressure_long": f"{float(diagnostics['LONG'].get('weak_signal_pressure', 0.0) or 0.0):.6f}",
                "weak_signal_pressure_short": f"{float(diagnostics['SHORT'].get('weak_signal_pressure', 0.0) or 0.0):.6f}",
                "readiness_wait": f"{float(diagnostics['WAIT'].get('readiness', 0.0) or 0.0):.6f}",
                "readiness_long": f"{float(diagnostics['LONG'].get('readiness', 0.0) or 0.0):.6f}",
                "readiness_short": f"{float(diagnostics['SHORT'].get('readiness', 0.0) or 0.0):.6f}",
                "memory_bias_wait": f"{float(diagnostics['WAIT'].get('action_bias', 0.0) or 0.0):.6f}",
                "memory_bias_long": f"{float(diagnostics['LONG'].get('action_bias', 0.0) or 0.0):.6f}",
                "memory_bias_short": f"{float(diagnostics['SHORT'].get('action_bias', 0.0) or 0.0):.6f}",
                "associative_wait": f"{float(diagnostics['WAIT'].get('associative_raw', 0.0) or 0.0):.6f}",
                "associative_long": f"{float(diagnostics['LONG'].get('associative_raw', 0.0) or 0.0):.6f}",
                "associative_short": f"{float(diagnostics['SHORT'].get('associative_raw', 0.0) or 0.0):.6f}",
                "observation_wait": f"{float(diagnostics['WAIT'].get('observation_signal', 0.0) or 0.0):.6f}",
                "observation_long": f"{float(diagnostics['LONG'].get('observation_signal', 0.0) or 0.0):.6f}",
                "observation_short": f"{float(diagnostics['SHORT'].get('observation_signal', 0.0) or 0.0):.6f}",
                "observation_readiness_wait": f"{float(diagnostics['WAIT'].get('observation_readiness', 0.0) or 0.0):.6f}",
                "observation_readiness_long": f"{float(diagnostics['LONG'].get('observation_readiness', 0.0) or 0.0):.6f}",
                "observation_readiness_short": f"{float(diagnostics['SHORT'].get('observation_readiness', 0.0) or 0.0):.6f}",
                "trade_readiness": f"{trade_readiness:.6f}",
                "associative_trade": f"{associative_trade:.6f}",
                "observation_trade_signal": f"{observation_trade_signal:.6f}",
                "observation_trade_readiness": f"{observation_trade_readiness:.6f}",
                "maturity_gap": f"{maturity_gap:.6f}",
                "mature_transfer": f"{mature_transfer:.6f}",
                "observation_learning_action": observation_learning_action,
                "observation_learning_pressure": f"{observation_learning_pressure:.6f}",
                "sehen_form_flow": f"{senses['sehen']['form_flow']:.6f}",
                "sehen_form_stability": f"{senses['sehen']['form_stability']:.6f}",
                "sehen_form_change": f"{senses['sehen']['form_change']:.6f}",
                "hoeren_energy_tone": f"{senses['hoeren']['energy_tone']:.6f}",
                "hoeren_energy_shift": f"{senses['hoeren']['energy_shift']:.6f}",
                "fuehlen_mcm_coherence": f"{senses['fuehlen']['mcm_coherence']:.6f}",
                "fuehlen_mcm_tension": f"{senses['fuehlen']['mcm_tension']:.6f}",
                "fuehlen_mcm_asymmetry": f"{senses['fuehlen']['mcm_asymmetry']:.6f}",
            }
        )
        if action in ("LONG", "SHORT"):
            active_phase = {
                "action": action,
                "symbol_family": symbol_family,
                "started_at": index,
                "senses": senses,
                "cooldown": horizon + 2,
            }
            index += horizon
        else:
            if int(active_phase.get("cooldown", 0) or 0) > 0:
                active_phase["cooldown"] = int(active_phase.get("cooldown", 0) or 0) - 1
            index += 1

    with episode_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)

    report = {
        "run": run_index,
        "data_path": str(data_path),
        "passive_world_label": passive_world_label or "",
        "passive_world_memory_loaded": bool(passive_world_state),
        "passive_inner_awareness_memory_loaded": bool(passive_inner_awareness_by_family),
        "passive_inner_awareness_contexts": dict(sorted(passive_inner_awareness_counter.items())),
        "passive_world_mean_avg_carry": _safe_float(passive_world_state.get("mean_avg_carry")),
        "passive_world_mean_avg_carried_cos": _safe_float(passive_world_state.get("mean_avg_carried_cos")),
        "reflection_contexts": dict(sorted(reflection_context_counter.items())),
        "avg_reflection_context_carry": sum(reflection_carry_values) / max(1, len(reflection_carry_values)),
        "max_reflection_context_carry": max(reflection_carry_values) if reflection_carry_values else 0.0,
        "avg_reflection_context_strain": sum(reflection_strain_values) / max(1, len(reflection_strain_values)),
        "max_reflection_context_strain": max(reflection_strain_values) if reflection_strain_values else 0.0,
        "avg_reflection_context_alignment": sum(reflection_alignment_values) / max(1, len(reflection_alignment_values)),
        "max_reflection_context_alignment": max(reflection_alignment_values) if reflection_alignment_values else 0.0,
        "candles": len(candles),
        "episodes": len(rows),
        "trades": trades,
        "long_trades": long_trades,
        "short_trades": short_trades,
        "waits": len(rows) - trades,
        "total_reward": total_reward,
        "avg_reward": total_reward / max(1, len(rows)),
        "actionable_seen": actionable_seen,
        "correct_action_when_actionable": correct_direction,
        "outcome_events": dict(sorted(outcome_event_counter.items())),
        "tp_hits": int(outcome_event_counter.get("TP", 0) or 0),
        "sl_hits": int(outcome_event_counter.get("SL", 0) or 0),
        "timeout_trades": int(outcome_event_counter.get("TIMEOUT", 0) or 0),
        "both_touched_trades": int(outcome_event_counter.get("BOTH_TOUCHED", 0) or 0),
        "unique_symbols": len(symbol_counter),
        "avg_trade_readiness": sum(trade_readiness_values) / max(1, len(trade_readiness_values)),
        "max_trade_readiness": max(trade_readiness_values) if trade_readiness_values else 0.0,
        "avg_associative_trade": sum(associative_trade_values) / max(1, len(associative_trade_values)),
        "max_associative_trade": max(associative_trade_values) if associative_trade_values else 0.0,
        "avg_maturity_gap": sum(maturity_gap_values) / max(1, len(maturity_gap_values)),
        "max_maturity_gap": max(maturity_gap_values) if maturity_gap_values else 0.0,
        "avg_mature_transfer": sum(mature_transfer_values) / max(1, len(mature_transfer_values)),
        "max_mature_transfer": max(mature_transfer_values) if mature_transfer_values else 0.0,
        "avg_mini_afterimage": sum(temporal_afterimage_values) / max(1, len(temporal_afterimage_values)),
        "max_mini_afterimage": max(temporal_afterimage_values) if temporal_afterimage_values else 0.0,
        "avg_mini_temporal_trust_support": sum(temporal_trust_values) / max(1, len(temporal_trust_values)),
        "max_mini_temporal_trust_support": max(temporal_trust_values) if temporal_trust_values else 0.0,
        "avg_mini_temporal_caution_support": sum(temporal_caution_values) / max(1, len(temporal_caution_values)),
        "max_mini_temporal_caution_support": max(temporal_caution_values) if temporal_caution_values else 0.0,
        "avg_mini_neuro_support": sum(neuro_support_values) / max(1, len(neuro_support_values)),
        "max_mini_neuro_support": max(neuro_support_values) if neuro_support_values else 0.0,
        "avg_mini_neuro_load": sum(neuro_load_values) / max(1, len(neuro_load_values)),
        "max_mini_neuro_load": max(neuro_load_values) if neuro_load_values else 0.0,
        "avg_mini_neuro_balance": sum(neuro_balance_values) / max(1, len(neuro_balance_values)),
        "max_mini_neuro_balance": max(neuro_balance_values) if neuro_balance_values else 0.0,
        "mini_neuro_tones": dict(sorted(neuro_tone_counter.items())),
        "avg_observation_trade_signal": sum(observation_signal_values) / max(1, len(observation_signal_values)),
        "max_observation_trade_signal": max(observation_signal_values) if observation_signal_values else 0.0,
        "avg_observation_trade_readiness": sum(observation_readiness_values) / max(1, len(observation_readiness_values)),
        "max_observation_trade_readiness": max(observation_readiness_values) if observation_readiness_values else 0.0,
        "observation_learning_events": observation_learning_events,
        "avg_observation_learning_pressure": sum(observation_learning_values) / max(1, len(observation_learning_values)),
        "max_observation_learning_pressure": max(observation_learning_values) if observation_learning_values else 0.0,
        "top_symbols": [
            {"symbol": symbol, "count": count}
            for symbol, count in sorted(symbol_counter.items(), key=lambda item: item[1], reverse=True)[:8]
        ],
        "memory_top": memory.compact_top(limit=8),
        "family_top": memory.compact_top_families(limit=8),
    }
    (debug_dir / "mini_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="DIO mini episodic learner")
    parser.add_argument("--data", default=getattr(Config, "DIO_MINI_CONTROLLED_WORLD_PATH", "data/kontrolliert_long_short_5m_SOLUSDT.csv"))
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--reset-memory", action="store_true")
    parser.add_argument("--memory", default=getattr(Config, "DIO_MINI_EPISODIC_MEMORY_PATH", "bot_memory/dio_mini_episodic_memory.json"))
    parser.add_argument("--debug-root", default="debug")
    parser.add_argument("--world-carrying-memory", default="")
    parser.add_argument("--inner-awareness-memory", default="")
    parser.add_argument("--world-label", default="")
    args = parser.parse_args()

    data_path = Path(args.data)
    memory_path = Path(args.memory)
    if args.reset_memory and memory_path.exists():
        memory_path.unlink()

    memory = SemanticMemory(memory_path, max_symbols=getattr(Config, "DIO_MINI_MAX_EPISODES", 2048))
    memory.load()
    passive_world_memory_path = Path(args.world_carrying_memory) if args.world_carrying_memory else None
    passive_world_state = load_passive_world_carrying_state(passive_world_memory_path, str(args.world_label or ""))
    passive_inner_awareness_memory_path = Path(args.inner_awareness_memory) if args.inner_awareness_memory else None
    passive_inner_awareness_by_family = load_passive_inner_awareness_state(passive_inner_awareness_memory_path)
    debug_root = Path(args.debug_root)
    reports = []
    for _ in range(max(1, int(args.runs))):
        memory.mark_run()
        run_index = int(memory.data.get("runs", 1) or 1)
        report = run_once(
            data_path,
            memory,
            run_index,
            debug_root,
            passive_world_label=str(args.world_label or ""),
            passive_world_state=passive_world_state,
            passive_inner_awareness_by_family=passive_inner_awareness_by_family,
        )
        reports.append(report)
        memory.save()
        print(
            f"DIO_MINI RUN {run_index} | trades={report['trades']} "
            f"reward={report['total_reward']:.4f} avg={report['avg_reward']:.4f} "
            f"symbols={report['unique_symbols']}"
        )
    print(json.dumps(reports[-1], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
