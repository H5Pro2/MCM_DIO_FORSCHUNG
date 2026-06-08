# ==================================================
# core/runtime_field_state.py
# Runtime field load / capacity state
# ==================================================
import numpy as np


def _clip01(value):
    try:
        value = float(value)
    except Exception:
        value = 0.0

    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)

def _derive_runtime_field_state(bot=None, tension_state=None, snapshot=None):

    tension = dict(tension_state or {})
    mcm_snapshot = dict(snapshot or {})

    if bot is None:
        return {
            "field_stimulus_density": 0.0,
            "field_density": 0.0,
            "field_stability": 0.0,
            "regulatory_load": 0.0,
            "action_capacity": 0.0,
            "recovery_need": 0.0,
            "survival_pressure": 0.0,
        }

    field = None
    mcm_brain = getattr(bot, "mcm_brain", None)
    if isinstance(mcm_brain, dict):
        field = mcm_brain.get("field")

    energy_mean_abs = 0.0
    velocity_mean_abs = 0.0
    energy_variance = 0.0

    if field is not None:
        try:
            energy_array = np.asarray(getattr(field, "energy", []), dtype=float)
            if energy_array.size > 0:
                energy_mean_abs = float(np.mean(np.abs(energy_array)))
                energy_variance = float(np.var(energy_array))
        except Exception:
            pass

        try:
            velocity_array = np.asarray(getattr(field, "velocity", []), dtype=float)
            if velocity_array.size > 0:
                velocity_mean_abs = float(np.mean(np.abs(velocity_array)))
        except Exception:
            pass

    strongest_memory = dict(mcm_snapshot.get("strongest_memory", {}) or {})
    memory_strength = float(strongest_memory.get("strength", 0.0) or 0.0)
    memory_pressure = _clip01(memory_strength / 14.0)

    tension_stability = _clip01(tension.get("stability", 0.0) or 0.0)
    coherence_balance = 1.0 - min(1.0, abs(float(tension.get("coherence", 0.0) or 0.0)))

    inhibition_level = _clip01(getattr(bot, "inhibition_level", 0.0) or 0.0)
    habituation_level = _clip01(getattr(bot, "habituation_level", 0.0) or 0.0)
    observation_mode = bool(getattr(bot, "observation_mode", False))
    pressure_release = _clip01(getattr(bot, "pressure_release", 0.0) or 0.0)
    experience_regulation = _clip01(getattr(bot, "experience_regulation", 0.0) or 0.0)
    load_bearing_capacity = _clip01(getattr(bot, "load_bearing_capacity", 0.0) or 0.0)

    attempt_feedback = {}
    stats_obj = getattr(bot, "stats", None)
    if stats_obj is not None:
        try:
            attempt_feedback = dict(stats_obj.get_attempt_feedback() or {})
        except Exception:
            attempt_feedback = {}

    attempt_density = _clip01(attempt_feedback.get("attempt_density", 0.0) or 0.0)
    overtrade_pressure = _clip01(attempt_feedback.get("overtrade_pressure", 0.0) or 0.0)
    context_quality = _clip01(attempt_feedback.get("context_quality", 0.0) or 0.0)

    pnl_netto = 0.0
    max_drawdown_pct = 0.0
    sl_count = 0.0
    trade_count = 0.0
    if stats_obj is not None:
        data = dict(getattr(stats_obj, "data", {}) or {})
        pnl_netto = float(data.get("pnl_netto", 0.0) or 0.0)
        max_drawdown_pct = max(0.0, float(data.get("max_drawdown_pct", 0.0) or 0.0))
        sl_count = float(data.get("sl", 0.0) or 0.0)
        trade_count = float(data.get("trades", 0.0) or 0.0)

    negative_pnl_pressure = _clip01(abs(min(0.0, pnl_netto)) / 100.0)
    drawdown_pressure = _clip01(max_drawdown_pct / 0.25)
    loss_pressure = _clip01(sl_count / max(1.0, trade_count + 1.0))

    field_stimulus_density = _clip01(
        (min(1.0, energy_mean_abs / 1.6) * 0.30)
        + (min(1.0, velocity_mean_abs / 0.45) * 0.22)
        + (min(1.0, energy_variance / 0.90) * 0.12)
    )

    field_density = _clip01(
        (field_stimulus_density * 0.28)
        + (memory_pressure * 0.08)
        + (attempt_density * 0.10)
        + (overtrade_pressure * 0.10)
        + (inhibition_level * 0.08)
        + ((1.0 - tension_stability) * 0.12)
    )

    field_stability = _clip01(
        (tension_stability * 0.38)
        + (coherence_balance * 0.12)
        + (pressure_release * 0.18)
        + (experience_regulation * 0.16)
        + (load_bearing_capacity * 0.16)
        - (min(1.0, velocity_mean_abs / 0.45) * 0.12)
    )

    survival_pressure = _clip01(
        (negative_pnl_pressure * 0.34)
        + (drawdown_pressure * 0.34)
        + (loss_pressure * 0.12)
        + (overtrade_pressure * 0.10)
        + ((1.0 - context_quality) * 0.10)
    )

    regulatory_load = _clip01(
        (field_density * 0.22)
        + (max(0.0, field_stimulus_density - field_stability) * 0.10)
        + ((1.0 - field_stability) * 0.18)
        + (survival_pressure * 0.22)
        + (inhibition_level * 0.10)
        + (habituation_level * 0.08)
        + (attempt_density * 0.08)
        + (0.06 if observation_mode else 0.0)
    )

    action_capacity = _clip01(
        (field_stability * 0.30)
        + (experience_regulation * 0.18)
        + (load_bearing_capacity * 0.16)
        + (pressure_release * 0.12)
        + (context_quality * 0.10)
        + ((1.0 - regulatory_load) * 0.22)
        - (survival_pressure * 0.18)
    )

    recovery_need = _clip01(
        (regulatory_load * 0.46)
        + (survival_pressure * 0.22)
        + ((1.0 - field_stability) * 0.14)
        + ((1.0 - action_capacity) * 0.14)
        + (0.08 if observation_mode else 0.0)
    )

    bot.field_stimulus_density = float(field_stimulus_density)
    bot.field_density = float(field_density)
    bot.field_stability = float(field_stability)
    bot.regulatory_load = float(regulatory_load)
    bot.action_capacity = float(action_capacity)
    bot.recovery_need = float(recovery_need)
    bot.survival_pressure = float(survival_pressure)

    return {
        "field_stimulus_density": float(field_stimulus_density),
        "field_density": float(field_density),
        "field_stability": float(field_stability),
        "regulatory_load": float(regulatory_load),
        "action_capacity": float(action_capacity),
        "recovery_need": float(recovery_need),
        "survival_pressure": float(survival_pressure),
    }

