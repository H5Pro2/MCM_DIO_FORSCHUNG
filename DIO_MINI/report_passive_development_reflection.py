"""Build passive reflection states from Mini-DIO development diagnosis.

This report is diagnostic only. It reads the passive development diagnosis and
translates it into a compact inner reflection view. It does not write memory,
does not influence action, and is not a gate.
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


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _reflection_state(development_state: str, reward_sum: float) -> str:
    if development_state == "development_stable_carried" and reward_sum > 0.0:
        return "reflection_trust_seed"
    if development_state == "development_observation_to_carried" and reward_sum > 0.0:
        return "reflection_confirmation_seed"
    if development_state == "development_repeated_burden":
        return "reflection_caution_seed"
    if development_state == "development_mixed_shift":
        return "reflection_reorganization_seed"
    if development_state == "development_quiet_observation":
        return "reflection_quiet_observation"
    if development_state == "development_positive_open":
        return "reflection_positive_open"
    if development_state == "development_negative_open":
        return "reflection_negative_open"
    return "reflection_open"


def _reflection_pressure(state: str, reward_sum: float, count: int) -> float:
    repeats = min(1.0, max(0.0, count / 3.0))
    reward = min(1.0, abs(reward_sum) / max(1.0, count))
    if state in {"reflection_trust_seed", "reflection_confirmation_seed"}:
        return round(0.45 + repeats * 0.30 + reward * 0.25, 6)
    if state == "reflection_caution_seed":
        return round(0.50 + repeats * 0.25 + reward * 0.25, 6)
    if state == "reflection_reorganization_seed":
        return round(0.35 + repeats * 0.25 + reward * 0.10, 6)
    if state == "reflection_quiet_observation":
        return round(0.20 + repeats * 0.20, 6)
    return round(0.10 + repeats * 0.15 + reward * 0.10, 6)


def _reflection_sentence(row: dict, state: str) -> str:
    family = str(row.get("symbol_family", "") or "-")
    action_path = str(row.get("action_path", "") or "-")
    moment_path = str(row.get("moment_path", "") or "-")
    if state == "reflection_trust_seed":
        return f"{family}: Wiederkehr wurde getragen; Innenlage darf Vertrauen erinnern. Aktionen={action_path}."
    if state == "reflection_confirmation_seed":
        return f"{family}: Beobachtung wurde spaeter getragen; Innenlage darf Bestaetigung erinnern. Momente={moment_path}."
    if state == "reflection_caution_seed":
        return f"{family}: Wiederkehr war belastend; Innenlage darf Vorsicht erinnern. Aktionen={action_path}."
    if state == "reflection_reorganization_seed":
        return f"{family}: Wiederkehr war gemischt; Innenlage darf Reorganisation erinnern. Momente={moment_path}."
    if state == "reflection_quiet_observation":
        return f"{family}: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen={action_path}."
    return f"{family}: Wiederkehr ist passiv noch offen; Innenlage bleibt lesend."


def build_rows(development_csv: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    summary: dict[str, dict] = {}
    for row in _read_rows(development_csv):
        development_state = str(row.get("development_state", "") or "")
        reward_sum = _safe_float(row.get("reward_sum"))
        count = _safe_int(row.get("count"))
        state = _reflection_state(development_state, reward_sum)
        pressure = _reflection_pressure(state, reward_sum, count)
        item = {
            "symbol_family": str(row.get("symbol_family", "") or ""),
            "passive_reflection_state": state,
            "development_state": development_state,
            "maturation_state": str(row.get("maturation_state", "") or ""),
            "count": count,
            "runs": str(row.get("runs", "") or ""),
            "first_moment_state": str(row.get("first_moment_state", "") or ""),
            "last_moment_state": str(row.get("last_moment_state", "") or ""),
            "moment_path": str(row.get("moment_path", "") or ""),
            "binding_path": str(row.get("binding_path", "") or ""),
            "action_path": str(row.get("action_path", "") or ""),
            "reward_sum": round(reward_sum, 6),
            "event_reward_sum": round(_safe_float(row.get("event_reward_sum")), 6),
            "reflection_pressure": pressure,
            "reflection_sentence": _reflection_sentence(row, state),
            "passive_only": 1,
        }
        detail.append(item)
        bucket = summary.setdefault(
            state,
            {
                "passive_reflection_state": state,
                "family_count": 0,
                "row_count": 0,
                "reward_sum": 0.0,
                "families": [],
                "max_reflection_pressure": 0.0,
            },
        )
        bucket["family_count"] += 1
        bucket["row_count"] += count
        bucket["reward_sum"] += reward_sum
        bucket["families"].append(item["symbol_family"])
        bucket["max_reflection_pressure"] = max(float(bucket["max_reflection_pressure"]), pressure)

    detail.sort(
        key=lambda item: (
            str(item.get("passive_reflection_state", "")),
            str(item.get("symbol_family", "")),
        )
    )
    summary_rows = []
    for item in summary.values():
        item["reward_sum"] = round(float(item["reward_sum"]), 6)
        item["max_reflection_pressure"] = round(float(item["max_reflection_pressure"]), 6)
        item["families"] = ",".join(sorted(str(family) for family in item["families"] if family))
        summary_rows.append(item)
    summary_rows.sort(
        key=lambda item: (
            str(item.get("passive_reflection_state", "")),
            str(item.get("families", "")),
        )
    )
    return detail, summary_rows


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, development_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_development_reflection.csv"
    summary_csv = output_dir / "dio_mini_passive_development_reflection_summary.csv"
    json_path = output_dir / "dio_mini_passive_development_reflection.json"
    md_path = output_dir / "dio_mini_passive_development_reflection.md"

    detail_fields = list(detail[0].keys()) if detail else ["symbol_family", "passive_reflection_state"]
    with detail_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else ["passive_reflection_state", "family_count"]
    with summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "source": str(development_csv),
                "detail": detail,
                "summary": summary,
                "boundary": {
                    "writes_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Development Reflection", "", f"- source: {development_csv}", ""]
    lines.append("## Zusammenfassung")
    if not summary:
        lines.append("- keine passiven Reflexionsdaten")
    for row in summary:
        lines.append(
            f"- {row['passive_reflection_state']}: "
            f"families={row['family_count']} rows={row['row_count']} "
            f"reward_sum={row['reward_sum']} pressure_max={row['max_reflection_pressure']} "
            f"families_list={row['families'] or '-'}"
        )
    lines.extend(["", "## Familien"])
    for row in detail:
        lines.extend(
            [
                f"- {row['symbol_family']}: {row['passive_reflection_state']}; "
                f"development={row['development_state']}; reward={float(row['reward_sum']):.6f}; "
                f"pressure={float(row['reflection_pressure']):.6f}",
                f"  {row['reflection_sentence']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Reflexionslesung",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive development reflection from Mini-DIO diagnosis")
    parser.add_argument("--development-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, summary = build_rows(Path(args.development_csv))
    write_outputs(detail, summary, Path(args.output_dir), Path(args.development_csv))
    print(f"passive_development_reflection_rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['passive_reflection_state']} families={row['family_count']} "
            f"rows={row['row_count']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
