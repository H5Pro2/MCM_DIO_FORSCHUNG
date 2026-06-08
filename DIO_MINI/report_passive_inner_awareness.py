"""Build a passive inner-awareness map from family maturation reflection.

This report translates passive reflection postures into an internal state view:
what feels carried, cautious, open, unfinished, or cooling. It does not write
memory and it must not influence action.
"""

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


def _inner_state(posture: str) -> str:
    posture = str(posture or "")
    if posture in ("passive_reflection_stable_carry", "passive_reflection_carried_maturation"):
        return "inner_carried"
    if posture == "passive_reflection_caution_after_conflict":
        return "inner_cautious"
    if posture == "passive_reflection_open_observation":
        return "inner_open_observation"
    if posture == "passive_reflection_held_unfinished":
        return "inner_unfinished"
    if posture == "passive_reflection_cooling":
        return "inner_cooling"
    return "inner_open"


def _inner_sentence(row: dict, inner_state: str) -> str:
    family = str(row.get("family", "") or "-")
    state_path = str(row.get("state_path", "") or "-")
    reward = _safe_float(row.get("reward_sum", 0.0))
    if inner_state == "inner_carried":
        return f"{family}: Diese Spur fuehlt sich innen getragen an ({state_path}); reward_sum={reward:.6f}."
    if inner_state == "inner_cautious":
        return f"{family}: Diese Spur fuehlt sich innen vorsichtig an ({state_path}); Konflikt wurde nicht fortgesetzt."
    if inner_state == "inner_open_observation":
        return f"{family}: Diese Spur bleibt innen beobachtend offen ({state_path})."
    if inner_state == "inner_unfinished":
        return f"{family}: Diese Spur fuehlt sich innen unfertig/gehalten an ({state_path})."
    if inner_state == "inner_cooling":
        return f"{family}: Diese Spur kuehlt innen ab ({state_path})."
    return f"{family}: Diese Spur bleibt innen offen ({state_path})."


def build_rows(reflection_csv: Path, selected_families: set[str] | None = None) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    with reflection_csv.open(newline="", encoding="utf-8") as handle:
        for source in csv.DictReader(handle):
            family = str(source.get("family", "") or "")
            if selected_families and family not in selected_families:
                continue
            state = _inner_state(str(source.get("reflection_posture", "") or ""))
            reward = round(_safe_float(source.get("reward_sum", 0.0)), 6)
            detail.append(
                {
                    "family": family,
                    "inner_state": state,
                    "reflection_posture": str(source.get("reflection_posture", "") or ""),
                    "trend": str(source.get("trend", "") or ""),
                    "reward_sum": reward,
                    "state_path": str(source.get("state_path", "") or ""),
                    "action_path": str(source.get("action_path", "") or ""),
                    "inner_sentence": _inner_sentence(source, state),
                    "passive_only": 1,
                }
            )

    groups: dict[str, dict] = {}
    for row in detail:
        state = str(row["inner_state"])
        item = groups.setdefault(
            state,
            {
                "inner_state": state,
                "count": 0,
                "reward_sum": 0.0,
                "families": set(),
            },
        )
        item["count"] += 1
        item["reward_sum"] += _safe_float(row.get("reward_sum", 0.0))
        item["families"].add(str(row.get("family", "") or ""))

    summary: list[dict] = []
    for item in groups.values():
        summary.append(
            {
                "inner_state": item["inner_state"],
                "count": int(item["count"]),
                "reward_sum": round(float(item["reward_sum"]), 6),
                "families": ",".join(sorted(name for name in item["families"] if name)),
            }
        )
    summary.sort(
        key=lambda item: (
            str(item.get("inner_state", "")) != "inner_carried",
            -_safe_float(item.get("reward_sum", 0.0)),
            str(item.get("inner_state", "")),
        )
    )
    detail.sort(
        key=lambda item: (
            str(item.get("inner_state", "")) != "inner_carried",
            -_safe_float(item.get("reward_sum", 0.0)),
            str(item.get("family", "")),
        )
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_inner_awareness.csv"
    summary_path = output_dir / "dio_mini_passive_inner_awareness_summary.csv"
    json_path = output_dir / "dio_mini_passive_inner_awareness.json"
    md_path = output_dir / "dio_mini_passive_inner_awareness.md"
    detail_fields = [
        "family",
        "inner_state",
        "reflection_posture",
        "trend",
        "reward_sum",
        "state_path",
        "action_path",
        "inner_sentence",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = ["inner_state", "count", "reward_sum", "families"]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Inner Awareness", ""]
    if not summary:
        lines.append("Keine Innenwahrnehmung gefunden.")
    for item in summary:
        lines.extend(
            [
                f"## {item['inner_state']}",
                f"- count: {item['count']}",
                f"- reward_sum: {float(item['reward_sum']):.6f}",
                f"- families: {item['families'] or '-'}",
                "",
            ]
        )
    lines.extend(["# Detail", ""])
    for row in detail:
        lines.extend(
            [
                f"## {row['family']}",
                f"- inner_state: {row['inner_state']}",
                f"- reflection_posture: {row['reflection_posture']}",
                f"- state_path: {row['state_path']}",
                f"- action_path: {row['action_path']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- inner_sentence: {row['inner_sentence']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Grenze",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive inner awareness from maturation reflection")
    parser.add_argument("--reflection-csv", required=True)
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    selected = {str(item).strip() for item in args.family if str(item).strip()} or None
    detail, summary = build_rows(Path(args.reflection_csv), selected_families=selected)
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"inner_awareness_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary:
        print(
            f"{row['inner_state']} count={row['count']} "
            f"reward_sum={row['reward_sum']} families={row['families']}"
        )


if __name__ == "__main__":
    main()
