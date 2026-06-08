# ==================================================
# bot_engine/regulation_snapshot.py
# Bot regulation state snapshots and deltas
# ==================================================

def build_regulation_state_snapshot(bot) -> dict:

    if bot is None:
        return {
            "tension": {
                "energy": 0.0,
                "coherence": 0.0,
                "stability": 0.0,
                "momentum": 0.0,
                "perceived_pressure": 0.0,
                "volume_pressure": 0.0,
            },
            "field": {
                "regulatory_load": 0.0,
                "action_capacity": 0.0,
                "recovery_need": 0.0,
                "survival_pressure": 0.0,
                "pressure_to_capacity": 0.0,
                "capacity_reserve": 0.0,
                "recovery_balance": 0.0,
                "field_areal_count": 0.0,
                "field_areal_activation_mean": 0.0,
                "field_areal_stability_mean": 0.0,
                "field_areal_pressure_mean": 0.0,
                "field_areal_drift": 0.0,
                "field_areal_dominance": 0.0,
                "field_areal_fragmentation": 0.0,
                "field_areal_coherence_mean": 0.0,
                "field_areal_conflict_mean": 0.0,
            },
            "experience": {
                "approach_pressure": 0.0,
                "pressure_release": 0.0,
                "experience_regulation": 0.0,
                "reflection_maturity": 0.0,
                "load_bearing_capacity": 0.0,
                "protective_width_regulation": 0.0,
                "protective_courage": 0.0,
                "carrying_balance": 0.0,
                "bearing_pressure_gap": 0.0,
            },
        }

    tension_state = dict(getattr(bot, "tension_state", {}) or {})
    inner_field_state = dict(getattr(bot, "inner_field_perception_state", {}) or {})
    regulatory_load = float(getattr(bot, "regulatory_load", 0.0) or 0.0)
    action_capacity = float(getattr(bot, "action_capacity", 0.0) or 0.0)
    recovery_need = float(getattr(bot, "recovery_need", 0.0) or 0.0)
    survival_pressure = float(getattr(bot, "survival_pressure", 0.0) or 0.0)
    pressure_release = float(getattr(bot, "pressure_release", 0.0) or 0.0)
    experience_regulation = float(getattr(bot, "experience_regulation", 0.0) or 0.0)
    reflection_maturity = float(getattr(bot, "reflection_maturity", 0.0) or 0.0)
    load_bearing_capacity = float(getattr(bot, "load_bearing_capacity", 0.0) or 0.0)
    protective_width_regulation = float(getattr(bot, "protective_width_regulation", 0.0) or 0.0)
    protective_courage = float(getattr(bot, "protective_courage", 0.0) or 0.0)

    pressure_to_capacity = 0.0
    if action_capacity > 0.0:
        pressure_to_capacity = regulatory_load / max(0.05, action_capacity)

    capacity_reserve = float(max(0.0, action_capacity - regulatory_load))
    recovery_balance = float(max(-1.0, min(1.0, pressure_release - recovery_need)))
    carrying_balance = float(
        max(
            -1.0,
            min(
                1.0,
                (load_bearing_capacity + action_capacity + protective_courage)
                - (regulatory_load + recovery_need + survival_pressure),
            ),
        )
    )
    bearing_pressure_gap = float(
        max(
            -1.0,
            min(
                1.0,
                (load_bearing_capacity + protective_width_regulation + protective_courage)
                - (pressure_to_capacity + survival_pressure),
            ),
        )
    )

    return {
        "tension": {
            "energy": float(tension_state.get("energy", 0.0) or 0.0),
            "coherence": float(tension_state.get("coherence", 0.0) or 0.0),
            "stability": float(tension_state.get("stability", 0.0) or 0.0),
            "momentum": float(tension_state.get("momentum", 0.0) or 0.0),
            "perceived_pressure": float(tension_state.get("perceived_pressure", 0.0) or 0.0),
            "volume_pressure": float(tension_state.get("volume_pressure", 0.0) or 0.0),
        },
        "field": {
            "regulatory_load": float(regulatory_load),
            "action_capacity": float(action_capacity),
            "recovery_need": float(recovery_need),
            "survival_pressure": float(survival_pressure),
            "pressure_to_capacity": float(pressure_to_capacity),
            "capacity_reserve": float(capacity_reserve),
            "recovery_balance": float(recovery_balance),
            "field_areal_count": float(inner_field_state.get("field_areal_count", 0.0) or 0.0),
            "field_areal_activation_mean": float(inner_field_state.get("field_areal_activation_mean", 0.0) or 0.0),
            "field_areal_stability_mean": float(inner_field_state.get("field_areal_stability_mean", 0.0) or 0.0),
            "field_areal_pressure_mean": float(inner_field_state.get("field_areal_pressure_mean", 0.0) or 0.0),
            "field_areal_drift": float(inner_field_state.get("field_areal_drift", 0.0) or 0.0),
            "field_areal_dominance": float(inner_field_state.get("field_areal_dominance", 0.0) or 0.0),
            "field_areal_fragmentation": float(inner_field_state.get("field_areal_fragmentation", 0.0) or 0.0),
            "field_areal_coherence_mean": float(inner_field_state.get("field_areal_coherence_mean", 0.0) or 0.0),
            "field_areal_conflict_mean": float(inner_field_state.get("field_areal_conflict_mean", 0.0) or 0.0),
        },
        "experience": {
            "approach_pressure": float(getattr(bot, "approach_pressure", 0.0) or 0.0),
            "pressure_release": float(pressure_release),
            "experience_regulation": float(experience_regulation),
            "reflection_maturity": float(reflection_maturity),
            "load_bearing_capacity": float(load_bearing_capacity),
            "protective_width_regulation": float(protective_width_regulation),
            "protective_courage": float(protective_courage),
            "carrying_balance": float(carrying_balance),
            "bearing_pressure_gap": float(bearing_pressure_gap),
        },
    }    
# --------------------------------------------------
def build_regulation_state_delta(state_before: dict, state_after: dict) -> dict:

    before = dict(state_before or {})
    after = dict(state_after or {})

    return {
        "tension": {
            "energy": float(after.get("tension", {}).get("energy", 0.0) - before.get("tension", {}).get("energy", 0.0)),
            "coherence": float(after.get("tension", {}).get("coherence", 0.0) - before.get("tension", {}).get("coherence", 0.0)),
            "stability": float(after.get("tension", {}).get("stability", 0.0) - before.get("tension", {}).get("stability", 0.0)),
            "momentum": float(after.get("tension", {}).get("momentum", 0.0) - before.get("tension", {}).get("momentum", 0.0)),
            "perceived_pressure": float(after.get("tension", {}).get("perceived_pressure", 0.0) - before.get("tension", {}).get("perceived_pressure", 0.0)),
            "volume_pressure": float(after.get("tension", {}).get("volume_pressure", 0.0) - before.get("tension", {}).get("volume_pressure", 0.0)),
        },
        "field": {
            "regulatory_load": float(after.get("field", {}).get("regulatory_load", 0.0) - before.get("field", {}).get("regulatory_load", 0.0)),
            "action_capacity": float(after.get("field", {}).get("action_capacity", 0.0) - before.get("field", {}).get("action_capacity", 0.0)),
            "recovery_need": float(after.get("field", {}).get("recovery_need", 0.0) - before.get("field", {}).get("recovery_need", 0.0)),
            "survival_pressure": float(after.get("field", {}).get("survival_pressure", 0.0) - before.get("field", {}).get("survival_pressure", 0.0)),
            "pressure_to_capacity": float(after.get("field", {}).get("pressure_to_capacity", 0.0) - before.get("field", {}).get("pressure_to_capacity", 0.0)),
            "capacity_reserve": float(after.get("field", {}).get("capacity_reserve", 0.0) - before.get("field", {}).get("capacity_reserve", 0.0)),
            "recovery_balance": float(after.get("field", {}).get("recovery_balance", 0.0) - before.get("field", {}).get("recovery_balance", 0.0)),
            "field_areal_count": float(after.get("field", {}).get("field_areal_count", 0.0) - before.get("field", {}).get("field_areal_count", 0.0)),
            "field_areal_activation_mean": float(after.get("field", {}).get("field_areal_activation_mean", 0.0) - before.get("field", {}).get("field_areal_activation_mean", 0.0)),
            "field_areal_stability_mean": float(after.get("field", {}).get("field_areal_stability_mean", 0.0) - before.get("field", {}).get("field_areal_stability_mean", 0.0)),
            "field_areal_pressure_mean": float(after.get("field", {}).get("field_areal_pressure_mean", 0.0) - before.get("field", {}).get("field_areal_pressure_mean", 0.0)),
            "field_areal_drift": float(after.get("field", {}).get("field_areal_drift", 0.0) - before.get("field", {}).get("field_areal_drift", 0.0)),
            "field_areal_dominance": float(after.get("field", {}).get("field_areal_dominance", 0.0) - before.get("field", {}).get("field_areal_dominance", 0.0)),
            "field_areal_fragmentation": float(after.get("field", {}).get("field_areal_fragmentation", 0.0) - before.get("field", {}).get("field_areal_fragmentation", 0.0)),
            "field_areal_coherence_mean": float(after.get("field", {}).get("field_areal_coherence_mean", 0.0) - before.get("field", {}).get("field_areal_coherence_mean", 0.0)),
            "field_areal_conflict_mean": float(after.get("field", {}).get("field_areal_conflict_mean", 0.0) - before.get("field", {}).get("field_areal_conflict_mean", 0.0)),
        },
        "experience": {
            "approach_pressure": float(after.get("experience", {}).get("approach_pressure", 0.0) - before.get("experience", {}).get("approach_pressure", 0.0)),
            "pressure_release": float(after.get("experience", {}).get("pressure_release", 0.0) - before.get("experience", {}).get("pressure_release", 0.0)),
            "experience_regulation": float(after.get("experience", {}).get("experience_regulation", 0.0) - before.get("experience", {}).get("experience_regulation", 0.0)),
            "reflection_maturity": float(after.get("experience", {}).get("reflection_maturity", 0.0) - before.get("experience", {}).get("reflection_maturity", 0.0)),
            "load_bearing_capacity": float(after.get("experience", {}).get("load_bearing_capacity", 0.0) - before.get("experience", {}).get("load_bearing_capacity", 0.0)),
            "protective_width_regulation": float(after.get("experience", {}).get("protective_width_regulation", 0.0) - before.get("experience", {}).get("protective_width_regulation", 0.0)),
            "protective_courage": float(after.get("experience", {}).get("protective_courage", 0.0) - before.get("experience", {}).get("protective_courage", 0.0)),
            "carrying_balance": float(after.get("experience", {}).get("carrying_balance", 0.0) - before.get("experience", {}).get("carrying_balance", 0.0)),
            "bearing_pressure_gap": float(after.get("experience", {}).get("bearing_pressure_gap", 0.0) - before.get("experience", {}).get("bearing_pressure_gap", 0.0)),
        },
    }
