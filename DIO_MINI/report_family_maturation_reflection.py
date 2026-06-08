"""Report passive reflection postures from DIO_MINI family maturation paths.

This reader consumes ``dio_mini_family_maturation_path.csv`` and translates a
family path into a readable passive posture. It is diagnosis only: no memory
write, no gate, no motor effect.
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


def _state_items(path: str) -> list[str]:
    return [item.strip() for item in str(path or "").split("->") if item.strip()]


def _posture(row: dict) -> str:
    trend = str(row.get("trend", "") or "")
    states = _state_items(str(row.get("state_path", "") or ""))
    reward = _safe_float(row.get("reward_sum", 0.0))
    if trend in ("conflict_to_carried", "observed_to_carried", "maturing") and reward > 0.0:
        return "passive_reflection_carried_maturation"
    if trend == "conflict_to_caution":
        return "passive_reflection_caution_after_conflict"
    if states and all(state == "carried" for state in states) and reward > 0.0:
        return "passive_reflection_stable_carry"
    if states and all(state == "observed" for state in states):
        return "passive_reflection_open_observation"
    if states and states[-1] == "held":
        return "passive_reflection_held_unfinished"
    if trend == "cooling":
        return "passive_reflection_cooling"
    return "passive_reflection_open_path"


def _sentence(row: dict, posture: str) -> str:
    family = str(row.get("family", "") or "-")
    state_path = str(row.get("state_path", "") or "-")
    action_path = str(row.get("action_path", "") or "-")
    reward = _safe_float(row.get("reward_sum", 0.0))
    if posture == "passive_reflection_carried_maturation":
        return (
            f"{family}: Die Familie wurde ueber wiederholten Kontakt tragender "
            f"({state_path}); Handlungspfad gelesen als {action_path}; reward_sum={reward:.6f}."
        )
    if posture == "passive_reflection_stable_carry":
        return (
            f"{family}: Die Familie blieb stabil getragen ({state_path}); "
            f"keine neue Anweisung, nur bestaetigte passive Reifespur."
        )
    if posture == "passive_reflection_caution_after_conflict":
        return (
            f"{family}: Konflikt wurde nicht fortgesetzt, sondern in Vorsicht/Beobachtung "
            f"ueberfuehrt ({state_path}); reward_sum={reward:.6f}."
        )
    if posture == "passive_reflection_open_observation":
        return f"{family}: Die Familie bleibt offen beobachtet ({state_path}); noch keine getragene Konsequenzspur."
    if posture == "passive_reflection_held_unfinished":
        return f"{family}: Die Familie endete gehalten/offen ({state_path}); Reifung ist nicht abgeschlossen."
    if posture == "passive_reflection_cooling":
        return f"{family}: Die Familie kuehlt im Verlauf ab ({state_path}); als passive Vorsicht lesen."
    return f"{family}: Offener Reifeverlauf ({state_path}); als passive Spur lesen."


def build_rows(maturation_csv: Path, selected_families: set[str] | None = None) -> list[dict]:
    rows: list[dict] = []
    with maturation_csv.open(newline="", encoding="utf-8") as handle:
        for source in csv.DictReader(handle):
            family = str(source.get("family", "") or "")
            if selected_families and family not in selected_families:
                continue
            posture = _posture(source)
            rows.append(
                {
                    "family": family,
                    "reflection_posture": posture,
                    "trend": str(source.get("trend", "") or ""),
                    "reward_sum": round(_safe_float(source.get("reward_sum", 0.0)), 6),
                    "state_path": str(source.get("state_path", "") or ""),
                    "action_path": str(source.get("action_path", "") or ""),
                    "passive_sentence": _sentence(source, posture),
                    "passive_only": 1,
                }
            )
    rows.sort(
        key=lambda item: (
            str(item.get("reflection_posture", "")) not in (
                "passive_reflection_carried_maturation",
                "passive_reflection_stable_carry",
            ),
            -_safe_float(item.get("reward_sum", 0.0)),
            str(item.get("family", "")),
        )
    )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_family_maturation_reflection.csv"
    json_path = output_dir / "dio_mini_family_maturation_reflection.json"
    md_path = output_dir / "dio_mini_family_maturation_reflection.md"
    fields = [
        "family",
        "reflection_posture",
        "trend",
        "reward_sum",
        "state_path",
        "action_path",
        "passive_sentence",
        "passive_only",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Family Maturation Reflection", ""]
    if not rows:
        lines.append("Keine Reifungsreflexion gefunden.")
    for row in rows:
        lines.extend(
            [
                f"## {row['family']}",
                f"- posture: {row['reflection_posture']}",
                f"- trend: {row['trend']}",
                f"- state_path: {row['state_path']}",
                f"- action_path: {row['action_path']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- passive_sentence: {row['passive_sentence']}",
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
    parser = argparse.ArgumentParser(description="Build passive family maturation reflection report")
    parser.add_argument("--maturation-csv", required=True)
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    selected = {str(item).strip() for item in args.family if str(item).strip()} or None
    rows = build_rows(Path(args.maturation_csv), selected_families=selected)
    write_outputs(rows, Path(args.output_dir))
    print(f"reflection_rows={len(rows)}")
    for row in rows[:25]:
        print(
            f"{row['family']} posture={row['reflection_posture']} "
            f"states={row['state_path']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
