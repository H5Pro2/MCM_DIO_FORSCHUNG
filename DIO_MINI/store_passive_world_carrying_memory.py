"""Store passive Mini-DIO world carrying observations in a separate memory.

This store is intentionally separate from action memory. It records world-level
diagnostics from ``report_passive_world_carrying_map`` and does not influence
Mini-DIO's runtime.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path


def _float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _int(value: object, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}.{int(time.time() * 1000)}")
    temp_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temp_path, path)


def update_running_average(previous_average: float, previous_count: int, new_value: float) -> float:
    count = max(0, int(previous_count))
    return ((float(previous_average) * count) + float(new_value)) / (count + 1)


def update_world_record(current: dict, observation: dict) -> dict:
    count = _int(current.get("observations"))
    updated = dict(current)
    updated["observations"] = count + 1
    updated["last"] = dict(observation)
    for field in (
        "avg_carry",
        "max_carry",
        "avg_carried_cos",
        "max_carried_cos",
        "avg_readiness",
        "avg_inner_balance",
        "avg_temporal_trust",
        "avg_temporal_caution",
    ):
        updated[f"mean_{field}"] = update_running_average(
            _float(current.get(f"mean_{field}")),
            count,
            _float(observation.get(field)),
        )
    updated["best_max_carry"] = max(_float(current.get("best_max_carry")), _float(observation.get("max_carry")))
    updated["best_max_carried_cos"] = max(
        _float(current.get("best_max_carried_cos")),
        _float(observation.get("max_carried_cos")),
    )
    updated["last_updated_utc_ms"] = int(time.time() * 1000)
    return updated


def build_observation(row: dict) -> dict:
    keep = [
        "world",
        "families",
        "carry_signal_family_count",
        "positive_carried_cos_family_count",
        "avg_carry",
        "max_carry",
        "avg_carried_cos",
        "max_carried_cos",
        "avg_readiness",
        "avg_inner_balance",
        "avg_temporal_trust",
        "avg_temporal_caution",
    ]
    observation = {key: row.get(key) for key in keep}
    observation["strongest_families"] = list(row.get("strongest_families", []) or [])[:5]
    return observation


def store_world_map(report_path: Path, memory_path: Path, source_label: str) -> dict:
    report = load_json(report_path)
    memory = load_json(memory_path)
    memory.setdefault("schema", "dio_mini_passive_world_carrying_memory.v1")
    memory.setdefault("source_reports", [])
    memory.setdefault("worlds", {})
    source_entry = {
        "source_label": source_label,
        "source_report": str(report_path),
        "stored_utc_ms": int(time.time() * 1000),
    }
    memory["source_reports"].append(source_entry)
    memory["source_reports"] = memory["source_reports"][-32:]

    for row in report.get("worlds", []) or []:
        observation = build_observation(dict(row))
        world = str(observation.get("world", "") or "world")
        current = dict(memory["worlds"].get(world, {}) or {})
        memory["worlds"][world] = update_world_record(current, observation)

    atomic_write_json(memory_path, memory)
    return memory


def main() -> None:
    parser = argparse.ArgumentParser(description="Store passive Mini-DIO world carrying memory")
    parser.add_argument("--report", required=True, help="passive_world_carrying_map.json")
    parser.add_argument("--memory", default="bot_memory/dio_mini_world_carrying_memory.json")
    parser.add_argument("--source-label", default="")
    args = parser.parse_args()

    memory = store_world_map(Path(args.report), Path(args.memory), args.source_label)
    print(
        json.dumps(
            {
                "worlds": len(memory.get("worlds", {}) or {}),
                "memory": str(Path(args.memory)),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
