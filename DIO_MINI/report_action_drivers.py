"""Report active action drivers from DIO_MINI episode debug files."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ACTIONS = ("WAIT", "LONG", "SHORT")


def _float(row: dict, key: str) -> float:
    try:
        return float(row.get(key, 0.0) or 0.0)
    except Exception:
        return 0.0


def _iter_episode_rows(debug_root: Path) -> list[dict]:
    rows = []
    for path in sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv")):
        run_id = path.parent.name.replace("dio_mini_lauf_", "")
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["run"] = run_id
                rows.append(item)
    return rows


def _dominant_driver(row: dict, action: str) -> str:
    action = str(action or "WAIT").upper()
    raw_action = str(row.get("raw_action", action) or action).upper()
    phase_active = str(row.get("phase_active", "0") or "0") in ("1", "true", "True")
    if action == "WAIT" and raw_action in ("LONG", "SHORT") and phase_active:
        return "episode_binding_hold"
    if action == "WAIT":
        wait_bias = abs(_float(row, "wait_bias"))
        wait_base = abs(_float(row, "base_score_wait"))
        wait_memory = abs(_float(row, "memory_bias_wait"))
        if wait_bias >= wait_base and wait_bias >= wait_memory:
            return "wait_regulation"
        if wait_memory >= wait_base:
            return "memory_bias"
        return "field_base"

    base = abs(_float(row, f"base_score_{action.lower()}"))
    memory = abs(_float(row, f"memory_bias_{action.lower()}"))
    caution = abs(_float(row, f"trade_caution_{action.lower()}"))
    associative = abs(_float(row, f"associative_{action.lower()}"))
    observation = abs(_float(row, f"observation_{action.lower()}"))
    values = {
        "field_base": base,
        "memory_bias": memory,
        "trade_caution": caution,
        "associative_near": associative,
        "observation_signal": observation,
    }
    return max(values, key=values.get)


def _summaries(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    detail = []
    overview: dict[str, dict] = {}
    for row in rows:
        action = str(row.get("action", "WAIT") or "WAIT").upper()
        driver = _dominant_driver(row, action)
        item = {
            "run": row.get("run", ""),
            "tick": row.get("tick", ""),
            "symbol_family": row.get("symbol_family", ""),
            "action": action,
            "raw_action": str(row.get("raw_action", action) or action).upper(),
            "phase_active": int(str(row.get("phase_active", "0") or "0") in ("1", "true", "True")),
            "episode_relation": row.get("episode_relation", ""),
            "best_action_training": row.get("best_action_training", ""),
            "reward": _float(row, "reward"),
            "driver": driver,
            "score_wait": _float(row, "score_wait"),
            "score_long": _float(row, "score_long"),
            "score_short": _float(row, "score_short"),
            "base_score_wait": _float(row, "base_score_wait"),
            "base_score_long": _float(row, "base_score_long"),
            "base_score_short": _float(row, "base_score_short"),
            "memory_bias_wait": _float(row, "memory_bias_wait"),
            "memory_bias_long": _float(row, "memory_bias_long"),
            "memory_bias_short": _float(row, "memory_bias_short"),
            "trade_caution_long": _float(row, "trade_caution_long"),
            "trade_caution_short": _float(row, "trade_caution_short"),
            "wait_bias": _float(row, "wait_bias"),
            "trade_readiness": _float(row, "trade_readiness"),
            "associative_trade": _float(row, "associative_trade"),
            "observation_trade_signal": _float(row, "observation_trade_signal"),
        }
        detail.append(item)
        key = f"{action}:{driver}"
        state = overview.setdefault(
            key,
            {
                "action": action,
                "driver": driver,
                "count": 0,
                "reward_sum": 0.0,
                "positive_count": 0,
                "negative_count": 0,
            },
        )
        state["count"] += 1
        state["reward_sum"] += float(item["reward"])
        if float(item["reward"]) > 0.0:
            state["positive_count"] += 1
        if float(item["reward"]) < 0.0:
            state["negative_count"] += 1
    overview_rows = []
    for item in overview.values():
        count = int(item["count"] or 0)
        overview_rows.append(
            {
                "action": item["action"],
                "driver": item["driver"],
                "count": count,
                "reward_sum": round(float(item["reward_sum"]), 6),
                "avg_reward": round(float(item["reward_sum"]) / max(1, count), 6),
                "positive_count": int(item["positive_count"]),
                "negative_count": int(item["negative_count"]),
            }
        )
    overview_rows.sort(key=lambda item: (-int(item["count"]), item["action"], item["driver"]))
    return detail, overview_rows


def _write(detail: list[dict], overview: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_action_driver_detail.csv"
    overview_csv = output_dir / "dio_mini_action_driver_overview.csv"
    json_path = output_dir / "dio_mini_action_driver_overview.json"
    md_path = output_dir / "dio_mini_action_driver_overview.md"

    detail_fields = list(detail[0].keys()) if detail else [
        "run",
        "tick",
        "symbol_family",
        "action",
        "best_action_training",
        "reward",
        "driver",
    ]
    with detail_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    overview_fields = [
        "action",
        "driver",
        "count",
        "reward_sum",
        "avg_reward",
        "positive_count",
        "negative_count",
    ]
    with overview_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=overview_fields)
        writer.writeheader()
        writer.writerows(overview)
    json_path.write_text(json.dumps(overview, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Action Driver Overview", ""]
    if not overview:
        lines.append("Keine Episoden gefunden.")
    for row in overview:
        lines.extend(
            [
                f"## {row['action']} / {row['driver']}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- avg_reward: {float(row['avg_reward']):.6f}",
                f"- positive_count: {row['positive_count']}",
                f"- negative_count: {row['negative_count']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rows = _iter_episode_rows(Path(args.debug_root))
    detail, overview = _summaries(rows)
    _write(detail, overview, Path(args.output_dir))
    print(f"episodes={len(detail)} groups={len(overview)}")
    for row in overview[:12]:
        print(
            f"{row['action']} {row['driver']} count={row['count']} "
            f"reward={row['reward_sum']} avg={row['avg_reward']}"
        )


if __name__ == "__main__":
    main()
