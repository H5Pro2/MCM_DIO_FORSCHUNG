"""Compare passive DIO_MINI cortex views across probe worlds."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _safe_int(value: object) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0


def _probe_order(probe: str) -> tuple:
    text = str(probe or "")
    digits = "".join(char for char in text if char.isdigit())
    return (_safe_int(digits), text)


def _read_view(path: Path, probe: str) -> list[dict]:
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            item = dict(row)
            item["probe"] = probe
            rows.append(item)
    return rows


def _probe_state(row: dict) -> str:
    seen = _safe_int(row.get("current_seen_count", 0))
    reward = _safe_float(row.get("current_reward_sum", 0.0))
    states = str(row.get("current_states", "") or "")
    timeline_state = str(row.get("timeline_state", "") or "")
    if seen <= 0:
        return "not_seen"
    if "executed_misaligned" in states and reward < 0.0:
        return "seen_conflict"
    if reward > 0.0:
        return "seen_carried"
    if "conflict" in timeline_state:
        return "seen_old_conflict_trace"
    return "seen_unclear"


def _family_sentence(family: str, states: list[str], rewards: list[float]) -> str:
    if "seen_conflict" in states and "seen_carried" in states:
        return f"{family}: wird in manchen Welten getragen und in anderen konflikthaft."
    if states.count("seen_carried") >= 2:
        return f"{family}: wird ueber mehrere Welten getragen gelesen."
    if "seen_conflict" in states:
        return f"{family}: zeigt mindestens eine konflikthafte Weltbegegnung."
    if all(state == "not_seen" for state in states):
        return f"{family}: bleibt in den gelesenen Welten still."
    return f"{family}: bleibt gemischt/offen, reward_sum={sum(rewards):.6f}."


def build_rows(inputs: list[tuple[str, Path]]) -> tuple[list[dict], list[dict]]:
    detail = []
    grouped: dict[str, list[dict]] = {}
    for probe, path in sorted(inputs, key=lambda item: _probe_order(item[0])):
        for row in _read_view(path, probe):
            state = _probe_state(row)
            item = {
                "probe": probe,
                "family": str(row.get("family", "") or ""),
                "probe_state": state,
                "timeline_state": str(row.get("timeline_state", "") or ""),
                "strongest_action_trace": str(row.get("strongest_action_trace", "") or ""),
                "current_seen_count": _safe_int(row.get("current_seen_count", 0)),
                "current_executed_count": _safe_int(row.get("current_executed_count", 0)),
                "current_reward_sum": round(_safe_float(row.get("current_reward_sum", 0.0)), 6),
                "current_actions": str(row.get("current_actions", "") or "-"),
                "current_states": str(row.get("current_states", "") or "-"),
                "cortex_sentence": str(row.get("cortex_sentence", "") or ""),
            }
            detail.append(item)
            if item["family"]:
                grouped.setdefault(item["family"], []).append(item)

    summary = []
    for family, items in sorted(grouped.items()):
        items = sorted(items, key=lambda item: _probe_order(str(item.get("probe", "") or "")))
        states = [str(item.get("probe_state", "") or "") for item in items]
        rewards = [_safe_float(item.get("current_reward_sum", 0.0)) for item in items]
        summary.append(
            {
                "family": family,
                "probe_count": len(items),
                "seen_count": sum(1 for item in items if _safe_int(item.get("current_seen_count", 0)) > 0),
                "executed_count": sum(_safe_int(item.get("current_executed_count", 0)) for item in items),
                "reward_sum": round(sum(rewards), 6),
                "probe_states": " -> ".join(f"{item['probe']}:{item['probe_state']}" for item in items),
                "timeline_states": "|".join(sorted({str(item.get("timeline_state", "") or "-") for item in items})),
                "strongest_action_traces": "|".join(
                    sorted({str(item.get("strongest_action_trace", "") or "-") for item in items})
                ),
                "passive_sentence": _family_sentence(family, states, rewards),
            }
        )
    summary.sort(
        key=lambda item: (
            "seen_conflict" not in item["probe_states"],
            -_safe_float(item.get("reward_sum", 0.0)),
            str(item.get("family", "")),
        )
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_cortex_comparison_detail.csv"
    summary_csv = output_dir / "dio_mini_passive_cortex_comparison_summary.csv"
    json_path = output_dir / "dio_mini_passive_cortex_comparison_summary.json"
    md_path = output_dir / "dio_mini_passive_cortex_comparison_summary.md"

    detail_fields = [
        "probe",
        "family",
        "probe_state",
        "timeline_state",
        "strongest_action_trace",
        "current_seen_count",
        "current_executed_count",
        "current_reward_sum",
        "current_actions",
        "current_states",
        "cortex_sentence",
    ]
    with detail_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = [
        "family",
        "probe_count",
        "seen_count",
        "executed_count",
        "reward_sum",
        "probe_states",
        "timeline_states",
        "strongest_action_traces",
        "passive_sentence",
    ]
    with summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Cortex Comparison", ""]
    if not summary:
        lines.append("Keine Kortexansichten gefunden.")
    for row in summary:
        lines.extend(
            [
                f"## {row['family']}",
                f"- passive_sentence: {row['passive_sentence']}",
                f"- probe_states: {row['probe_states']}",
                f"- seen / executed: {row['seen_count']} / {row['executed_count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- timeline_states: {row['timeline_states']}",
                f"- strongest_action_traces: {row['strongest_action_traces']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive DIO_MINI cortex views")
    parser.add_argument(
        "--view",
        action="append",
        required=True,
        help="probe_name=path/to/dio_mini_passive_cortex_view.csv",
    )
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    inputs = []
    for raw in args.view:
        if "=" not in raw:
            raise SystemExit(f"--view must be probe=path, got: {raw}")
        probe, path = raw.split("=", 1)
        inputs.append((probe.strip(), Path(path.strip())))
    detail, summary = build_rows(inputs)
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"families={len(summary)} detail_rows={len(detail)}")
    for row in summary:
        print(f"{row['family']} states={row['probe_states']} reward={row['reward_sum']}")


if __name__ == "__main__":
    main()
