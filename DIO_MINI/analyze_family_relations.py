"""Analyze semantic family relations in DIO mini memory.

This is diagnostic only. It compares stored family vectors and consequence
traces to show which DIO-owned word families are related.
"""

from __future__ import annotations

import argparse
import csv
import json
from itertools import combinations
from pathlib import Path


TRADE_ACTIONS = ("LONG", "SHORT")


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _clip(value: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, _safe_float(value)))


def _vector_distance(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 1.0
    size = min(len(left), len(right))
    if size <= 0:
        return 1.0
    return sum(abs(_clip(left[i]) - _clip(right[i])) for i in range(size)) / size


def _similarity(distance: float) -> float:
    return 1.0 / (1.0 + (distance * distance * 12.0))


def _observation_pressure(record: dict, action: str) -> float:
    state = dict(dict(record.get("observations", {}) or {}).get(action, {}) or {})
    count = _safe_int(state.get("count", 0))
    if count <= 0:
        return 0.0
    recognition_avg = _safe_float(state.get("recognition_sum", 0.0)) / max(1, count)
    reward_avg = _safe_float(state.get("reward_sum", 0.0)) / max(1, count)
    return recognition_avg * reward_avg * min(1.0, count / 8.0)


def _action_pressure(record: dict, action: str) -> float:
    state = dict(dict(record.get("actions", {}) or {}).get(action, {}) or {})
    count = _safe_int(state.get("count", 0))
    trust = _safe_float(state.get("trust", 0.0))
    caution = _safe_float(state.get("caution", 0.0))
    familiarity = min(1.0, count / 6.0)
    return ((trust - caution) * familiarity) + (_observation_pressure(record, action) * 0.35)


def _dominant_action(record: dict) -> str:
    pressures = {action: _action_pressure(record, action) for action in TRADE_ACTIONS}
    best_action = max(pressures, key=pressures.get)
    if abs(pressures[best_action]) <= 1e-9:
        return "-"
    return best_action


def _family_summary(record: dict) -> dict:
    actions = dict(record.get("actions", {}) or {})
    observations = dict(record.get("observations", {}) or {})
    return {
        "family": str(record.get("family", "-") or "-"),
        "count": _safe_int(record.get("count", 0)),
        "dominant_action": _dominant_action(record),
        "long_pressure": _action_pressure(record, "LONG"),
        "short_pressure": _action_pressure(record, "SHORT"),
        "long_count": _safe_int(dict(actions.get("LONG", {}) or {}).get("count", 0)),
        "short_count": _safe_int(dict(actions.get("SHORT", {}) or {}).get("count", 0)),
        "long_trust": _safe_float(dict(actions.get("LONG", {}) or {}).get("trust", 0.0)),
        "short_trust": _safe_float(dict(actions.get("SHORT", {}) or {}).get("trust", 0.0)),
        "long_observations": _safe_int(dict(observations.get("LONG", {}) or {}).get("count", 0)),
        "short_observations": _safe_int(dict(observations.get("SHORT", {}) or {}).get("count", 0)),
    }


def load_families(memory_path: Path) -> list[dict]:
    data = json.loads(memory_path.read_text(encoding="utf-8"))
    families = []
    for record in dict(data.get("families", {}) or {}).values():
        if not isinstance(record, dict):
            continue
        vector = record.get("vector")
        if not isinstance(vector, list):
            continue
        family = dict(record)
        family["vector"] = [_clip(value) for value in vector]
        families.append(family)
    return families


def analyze(memory_path: Path) -> list[dict]:
    families = load_families(memory_path)
    rows = []
    for left, right in combinations(families, 2):
        left_summary = _family_summary(left)
        right_summary = _family_summary(right)
        distance = _vector_distance(left["vector"], right["vector"])
        similarity = _similarity(distance)
        long_alignment = left_summary["long_pressure"] * right_summary["long_pressure"]
        short_alignment = left_summary["short_pressure"] * right_summary["short_pressure"]
        cross_alignment = (
            left_summary["long_pressure"] * right_summary["short_pressure"]
            + left_summary["short_pressure"] * right_summary["long_pressure"]
        )
        same_action = (
            left_summary["dominant_action"] == right_summary["dominant_action"]
            and left_summary["dominant_action"] in TRADE_ACTIONS
        )
        rows.append(
            {
                "left_family": left_summary["family"],
                "right_family": right_summary["family"],
                "distance": round(distance, 6),
                "similarity": round(similarity, 6),
                "left_action": left_summary["dominant_action"],
                "right_action": right_summary["dominant_action"],
                "same_action": int(same_action),
                "long_alignment": round(long_alignment, 6),
                "short_alignment": round(short_alignment, 6),
                "cross_alignment": round(cross_alignment, 6),
                "left_count": left_summary["count"],
                "right_count": right_summary["count"],
                "left_long_trust": round(left_summary["long_trust"], 6),
                "right_long_trust": round(right_summary["long_trust"], 6),
                "left_short_trust": round(left_summary["short_trust"], 6),
                "right_short_trust": round(right_summary["short_trust"], 6),
                "left_long_observations": left_summary["long_observations"],
                "right_long_observations": right_summary["long_observations"],
                "left_short_observations": left_summary["short_observations"],
                "right_short_observations": right_summary["short_observations"],
            }
        )
    rows.sort(key=lambda item: (item["similarity"], item["same_action"], abs(item["long_alignment"]) + abs(item["short_alignment"])), reverse=True)
    return rows


def write_outputs(rows: list[dict], output_dir: Path, topn: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    selected = rows[: max(1, int(topn))]
    (output_dir / "dio_mini_family_relations.json").write_text(json.dumps(selected, indent=2, sort_keys=True), encoding="utf-8")
    if selected:
        with (output_dir / "dio_mini_family_relations.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(selected[0].keys()))
            writer.writeheader()
            writer.writerows(selected)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DIO mini family relations")
    parser.add_argument("--memory", default="bot_memory/dio_mini_sensor_transfer_memory.json")
    parser.add_argument("--output-dir", default="debug/dio_mini_family_relations")
    parser.add_argument("--topn", type=int, default=80)
    args = parser.parse_args()

    rows = analyze(Path(args.memory))
    write_outputs(rows, Path(args.output_dir), args.topn)
    for row in rows[:12]:
        print(
            f"{row['left_family']} <-> {row['right_family']} "
            f"sim={row['similarity']:.4f} actions=({row['left_action']},{row['right_action']}) "
            f"same={row['same_action']}"
        )


if __name__ == "__main__":
    main()
