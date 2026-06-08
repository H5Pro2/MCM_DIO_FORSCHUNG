"""Summarize passive DIO_MINI reflection-map validation runs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def _load_map(path: Path, label: str) -> list[dict]:
    rows = []
    if not path.exists():
        return rows
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            item = dict(row)
            item["probe"] = label
            rows.append(item)
    return rows


def _build(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    detail = []
    by_state: dict[str, dict] = {}
    for row in rows:
        state = str(row.get("reflection_map_state", "") or "")
        family = str(row.get("symbol_family", "") or "")
        reward = _safe_float(row.get("reward_sum"))
        item = {
            "probe": str(row.get("probe", "") or ""),
            "symbol_family": family,
            "reflection_symbol": str(row.get("reflection_symbol", "") or ""),
            "reflection_map_state": state,
            "reward_sum": round(reward, 6),
            "seen_count": row.get("seen_count", ""),
            "executed_count": row.get("executed_count", ""),
            "observed_count": row.get("observed_count", ""),
            "dio_sentence": row.get("dio_sentence", ""),
        }
        detail.append(item)
        summary = by_state.setdefault(
            state,
            {
                "reflection_map_state": state,
                "count": 0,
                "reward_sum": 0.0,
                "probes": set(),
                "families": set(),
            },
        )
        summary["count"] += 1
        summary["reward_sum"] += reward
        summary["probes"].add(item["probe"])
        summary["families"].add(family)
    summary_rows = []
    for item in by_state.values():
        summary_rows.append(
            {
                "reflection_map_state": item["reflection_map_state"],
                "count": int(item["count"]),
                "reward_sum": round(float(item["reward_sum"]), 6),
                "probes": ",".join(sorted(name for name in item["probes"] if name)),
                "families": ",".join(sorted(name for name in item["families"] if name)),
            }
        )
    summary_rows.sort(key=lambda item: item["reflection_map_state"])
    detail.sort(key=lambda item: (item["symbol_family"], item["probe"]))
    return detail, summary_rows


def _write(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_reflection_validation.csv"
    summary_path = output_dir / "dio_mini_reflection_validation_summary.csv"
    json_path = output_dir / "dio_mini_reflection_validation.json"
    md_path = output_dir / "dio_mini_reflection_validation.md"

    detail_fields = [
        "probe",
        "symbol_family",
        "reflection_symbol",
        "reflection_map_state",
        "reward_sum",
        "seen_count",
        "executed_count",
        "observed_count",
        "dio_sentence",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["reflection_map_state", "count", "reward_sum", "probes", "families"])
        writer.writeheader()
        writer.writerows(summary)
    json_path.write_text(json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Reflection Validation", ""]
    for row in summary:
        lines.extend(
            [
                f"## {row['reflection_map_state']}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- probes: {row['probes'] or '-'}",
                f"- families: {row['families'] or '-'}",
                "",
            ]
        )
    lines.append("# Detail")
    lines.append("")
    for row in detail:
        lines.extend(
            [
                f"## {row['probe']} / {row['symbol_family']}",
                f"- state: {row['reflection_map_state']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- seen/executed/observed: {row['seen_count']} / {row['executed_count']} / {row['observed_count']}",
                f"- DIO: {row['dio_sentence']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", action="append", default=[], help="LABEL=path/to/dio_mini_reflection_map.csv")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = []
    for item in args.map:
        if "=" not in item:
            raise SystemExit(f"Invalid --map value, expected LABEL=PATH: {item}")
        label, path = item.split("=", 1)
        rows.extend(_load_map(Path(path), label))
    detail, summary = _build(rows)
    _write(detail, summary, Path(args.output_dir))
    print(f"reflection_validation={len(detail)}")
    for row in summary:
        print(
            f"{row['reflection_map_state']} count={row['count']} "
            f"reward={row['reward_sum']} probes={row['probes']}"
        )


if __name__ == "__main__":
    main()
