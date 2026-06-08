"""Passive temporal perception for Mini-DIO.

The layer tracks family recurrence, distance and afterimage. It is deliberately
passive: it does not choose actions and it does not change action scores.
"""

from __future__ import annotations


def _clip(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        value = float(value)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return max(lo, min(hi, value))


def _signed_clip(value: float) -> float:
    return max(-1.0, min(1.0, float(value or 0.0)))


def _vector_distance(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 1.0
    size = min(len(left), len(right))
    if size <= 0:
        return 1.0
    return _clip(sum(abs(_signed_clip(left[i]) - _signed_clip(right[i])) for i in range(size)) / size)


class MiniTemporalTracker:
    """In-run temporal trace for DIO-owned symbol families."""

    def __init__(self, *, afterimage_decay: float = 0.86):
        self.afterimage_decay = _clip(afterimage_decay, 0.0, 0.99)
        self.families: dict[str, dict] = {}

    def step(self, family: str, tick: int, vector: list[float]) -> dict:
        family = str(family or "-") or "-"
        tick = int(tick)
        previous = dict(self.families.get(family, {}) or {})
        seen_before = int(previous.get("seen_count", 0) or 0)
        first_seen_tick = int(previous.get("first_seen_tick", tick) or tick)
        previous_seen_tick = int(previous.get("last_seen_tick", tick) or tick)
        ticks_since_seen = tick - previous_seen_tick if seen_before > 0 else -1
        family_age = max(0, tick - first_seen_tick)
        previous_vector = list(previous.get("vector", []) or [])
        form_distance = _vector_distance(vector, previous_vector) if seen_before > 0 else 1.0
        temporal_distance = _clip((ticks_since_seen if ticks_since_seen >= 0 else 999.0) / 24.0)
        recurrence_strength = _clip(seen_before / (seen_before + 5.0)) if seen_before > 0 else 0.0
        if ticks_since_seen < 0:
            contact_state = "temporal_first_contact"
            contact_pressure = 0.0
        elif ticks_since_seen <= 1:
            contact_state = "temporal_immediate_afterimage"
            contact_pressure = 0.90
        elif ticks_since_seen <= 8:
            contact_state = "temporal_near_return"
            contact_pressure = _clip(1.0 - (ticks_since_seen / 10.0))
        else:
            contact_state = "temporal_far_return"
            contact_pressure = _clip(1.0 / (1.0 + ticks_since_seen / 8.0))
        previous_afterimage = float(previous.get("afterimage", 0.0) or 0.0)
        afterimage = _clip((previous_afterimage * self.afterimage_decay) + (contact_pressure * (1.0 - self.afterimage_decay)))
        temporal_fit = _clip((1.0 - form_distance) * 0.58 + afterimage * 0.24 + recurrence_strength * 0.18)
        temporal_caution = _clip(form_distance * 0.42 + temporal_distance * 0.18 + max(0.0, 0.30 - temporal_fit) * 0.40)

        self.families[family] = {
            "family": family,
            "first_seen_tick": first_seen_tick,
            "last_seen_tick": tick,
            "seen_count": seen_before + 1,
            "family_age": family_age,
            "ticks_since_seen": ticks_since_seen,
            "afterimage": afterimage,
            "vector": list(vector or []),
        }
        return {
            "mini_temporal_identity": family,
            "mini_temporal_state": contact_state,
            "mini_family_age": family_age,
            "mini_ticks_since_family_seen": ticks_since_seen,
            "mini_recurrence_strength": recurrence_strength,
            "mini_afterimage": afterimage,
            "mini_time_distance": temporal_distance,
            "mini_temporal_form_distance": form_distance,
            "mini_temporal_trust_support": temporal_fit,
            "mini_temporal_caution_support": temporal_caution,
            "passive_only": 1,
        }


__all__ = ["MiniTemporalTracker"]
