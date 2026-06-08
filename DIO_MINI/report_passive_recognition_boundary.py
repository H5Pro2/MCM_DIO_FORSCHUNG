"""Report passive recognition boundaries for DIO_MINI.

The report separates stable recognition from reflection-worthy difference.
It is diagnostic only: no memory writes, no motor influence, no gates.
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


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _boundary_state(row: dict) -> str:
    posture = str(row.get("reflection_posture", "") or "")
    trend = str(row.get("trend", "") or "")
    reward = _safe_float(row.get("reward_sum", 0.0))
    state_path = str(row.get("state_path", "") or "")

    has_change = "->" in state_path and len({part.strip() for part in state_path.split("->")}) > 1
    has_conflict_word = any(word in posture or word in state_path for word in ("conflict", "negative", "cautious"))

    if posture == "passive_reflection_stable_carry" and trend == "flat" and reward > 0.0:
        return "stable_recognition_not_memory"
    if posture == "passive_reflection_open_observation" and trend == "flat":
        return "open_observation_not_memory"
    if posture == "passive_reflection_held_unfinished" and trend == "flat":
        return "unfinished_trace_not_memory"
    if has_change or has_conflict_word:
        return "reflection_worthy_difference"
    return "undecided_passive_boundary"


def _boundary_sentence(row: dict, boundary: str) -> str:
    family = str(row.get("family", "") or "-")
    state_path = str(row.get("state_path", "") or "-")
    reward = _safe_float(row.get("reward_sum", 0.0))
    if boundary == "stable_recognition_not_memory":
        return (
            f"{family}: stabile Wiedererkennung ({state_path}), reward={reward:.6f}; "
            "kein neuer Reflexionsspeicher noetig."
        )
    if boundary == "open_observation_not_memory":
        return f"{family}: offene Beobachtung ({state_path}); weiter lesbar, aber nicht speicherpflichtig."
    if boundary == "unfinished_trace_not_memory":
        return f"{family}: unfertige/gehaltene Spur ({state_path}); beobachten, nicht als Reife speichern."
    if boundary == "reflection_worthy_difference":
        return f"{family}: relevante Differenz ({state_path}); passiv reflexionswuerdig."
    return f"{family}: Grenze passiv unentschieden ({state_path})."


def build_rows(maturation_reflection_csv: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    for row in _read_csv(maturation_reflection_csv):
        boundary = _boundary_state(row)
        item = {
            "family": str(row.get("family", "") or ""),
            "boundary_state": boundary,
            "reflection_posture": str(row.get("reflection_posture", "") or ""),
            "trend": str(row.get("trend", "") or ""),
            "reward_sum": round(_safe_float(row.get("reward_sum", 0.0)), 6),
            "state_path": str(row.get("state_path", "") or ""),
            "action_path": str(row.get("action_path", "") or ""),
            "boundary_sentence": _boundary_sentence(row, boundary),
            "writes_memory": 0,
            "influences_action": 0,
            "is_gate": 0,
            "passive_only": 1,
        }
        detail.append(item)

    groups: dict[str, dict] = {}
    for row in detail:
        key = str(row.get("boundary_state", "") or "")
        item = groups.setdefault(
            key,
            {
                "boundary_state": key,
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
                "boundary_state": item["boundary_state"],
                "count": int(item["count"]),
                "reward_sum": round(float(item["reward_sum"]), 6),
                "families": ",".join(sorted(name for name in item["families"] if name)),
                "writes_memory": 0,
                "influences_action": 0,
                "is_gate": 0,
                "passive_only": 1,
            }
        )
    summary.sort(key=lambda item: (str(item.get("boundary_state", "")), str(item.get("families", ""))))
    detail.sort(key=lambda item: (str(item.get("boundary_state", "")), str(item.get("family", ""))))
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_recognition_boundary.csv"
    summary_path = output_dir / "dio_mini_passive_recognition_boundary_summary.csv"
    json_path = output_dir / "dio_mini_passive_recognition_boundary.json"
    md_path = output_dir / "dio_mini_passive_recognition_boundary.md"

    detail_fields = list(detail[0].keys()) if detail else [
        "family",
        "boundary_state",
        "reflection_posture",
        "trend",
        "reward_sum",
        "state_path",
        "action_path",
        "boundary_sentence",
        "writes_memory",
        "influences_action",
        "is_gate",
        "passive_only",
    ]
    summary_fields = list(summary[0].keys()) if summary else [
        "boundary_state",
        "count",
        "reward_sum",
        "families",
        "writes_memory",
        "influences_action",
        "is_gate",
        "passive_only",
    ]

    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)
    json_path.write_text(
        json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Recognition Boundary",
        "",
        "## Grenze",
        "- kein Memory-Schreiben",
        "- keine Motorik",
        "- kein Gate",
        "- keine harte Regel",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Zeilen")
    else:
        for row in summary:
            lines.append(
                f"- {row.get('boundary_state', '-')}: count={row.get('count', 0)} | "
                f"reward_sum={row.get('reward_sum', 0.0)} | families={row.get('families', '-') or '-'}"
            )
    lines.extend(["", "## Detail"])
    for row in detail:
        lines.append(f"- {row.get('boundary_sentence', '')}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive DIO_MINI recognition boundaries")
    parser.add_argument("--maturation-reflection", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    detail, summary = build_rows(Path(args.maturation_reflection))
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"detail_rows={len(detail)} summary_rows={len(summary)}")


if __name__ == "__main__":
    main()
