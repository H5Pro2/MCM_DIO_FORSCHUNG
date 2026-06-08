"""Select passive follow-up candidates for weakly carried Mini-DIO traces.

This report extracts traces that look close to a stable carried reference but
were only carried once. It prepares a passive candidate list for another
controlled world-contact run. The output is diagnostic only and must not be
read by Mini-DIO for runtime, action, gates, entries, or direction.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


PASSIVE_FLAGS = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}


FIELDS = [
    "reference_family",
    "candidate_family",
    "candidate_state",
    "test_priority",
    "profile_distance",
    "carry_ratio_gap",
    "sensory_distance_gap",
    "mcm_coherence_gap",
    "mcm_tension_gap",
    "mcm_asymmetry_gap",
    "lived_support_drop_gap",
    "neuro_tone_reorganizes_gap",
    "text_island_same",
    "followup_question",
]


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except (TypeError, ValueError):
        return default
    if result != result:
        return default
    return result


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = list(fields)
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in ordered})


def _priority(row: dict[str, str]) -> str:
    distance = _safe_float(row.get("profile_distance"))
    text_same = str(row.get("text_island_same", "")).lower() == "true"
    sensory_gap = abs(_safe_float(row.get("sensory_distance_gap")))
    if text_same and distance <= 0.01 and sensory_gap <= 0.006:
        return "high"
    if text_same and distance <= 0.025:
        return "medium"
    return "low"


def _followup_question(priority: str) -> str:
    if priority == "high":
        return "Wird diese nahe Spur bei mehr Weltkontakt zu einer Mehr-Proben-Tragung?"
    if priority == "medium":
        return "Bleibt diese Spur stabil genug, oder kippt sie bei weiterer Variation?"
    return "Ist diese Spur nur ein kurzer situativer Kontakt oder eine entfernte Verwandtschaft?"


def build_candidates(rows: list[dict[str, str]], limit: int) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for row in rows:
        if row.get("contrast_reading") != "weak_carried_like_reference_needs_more_world_contact":
            continue
        priority = _priority(row)
        selected.append(
            {
                "reference_family": row.get("reference_family", ""),
                "candidate_family": row.get("family", ""),
                "candidate_state": row.get("contrast_reading", ""),
                "test_priority": priority,
                "profile_distance": row.get("profile_distance", ""),
                "carry_ratio_gap": row.get("carry_ratio_gap", ""),
                "sensory_distance_gap": row.get("sensory_distance_gap", ""),
                "mcm_coherence_gap": row.get("mcm_coherence_gap", ""),
                "mcm_tension_gap": row.get("mcm_tension_gap", ""),
                "mcm_asymmetry_gap": row.get("mcm_asymmetry_gap", ""),
                "lived_support_drop_gap": row.get("lived_support_drop_gap", ""),
                "neuro_tone_reorganizes_gap": row.get("neuro_tone_reorganizes_gap", ""),
                "text_island_same": row.get("text_island_same", ""),
                "followup_question": _followup_question(priority),
                **PASSIVE_FLAGS,
            }
        )
    selected.sort(
        key=lambda row: (
            {"high": 0, "medium": 1, "low": 2}.get(str(row["test_priority"]), 9),
            _safe_float(row["profile_distance"]),
            str(row["candidate_family"]),
        )
    )
    return selected[: max(1, limit)]


def write_report(output_dir: Path, rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_carry_followup_candidates.csv", rows, FIELDS + list(PASSIVE_FLAGS))
    priority_counts: dict[str, int] = {}
    for row in rows:
        key = str(row.get("test_priority", "unknown"))
        priority_counts[key] = priority_counts.get(key, 0) + 1
    summary = {
        "candidate_count": len(rows),
        "priority_counts": priority_counts,
        "top_candidate": rows[0]["candidate_family"] if rows else "-",
        **PASSIVE_FLAGS,
    }
    (output_dir / "passive_carry_followup_candidates.json").write_text(
        json.dumps({"summary": summary, "candidates": rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        "# Passive Carry Follow-Up Candidates",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry-Signal, kein Richtungssignal.",
        "",
        f"- Kandidaten: {summary['candidate_count']}",
        f"- Prioritäten: {summary['priority_counts']}",
        f"- Top-Kandidat: {summary['top_candidate']}",
        "",
        "## Kandidaten",
        "",
    ]
    for row in rows:
        lines.append(
            "- {family}: priority={priority}; distance={distance}; text_same={text_same}; frage={question}".format(
                family=row["candidate_family"],
                priority=row["test_priority"],
                distance=row["profile_distance"],
                text_same=row["text_island_same"],
                question=row["followup_question"],
            )
        )
    text = "\n".join(lines) + "\n"
    (output_dir / "passive_carry_followup_candidates.md").write_text(text, encoding="utf-8")
    (output_dir / "passive_carry_followup_candidates.txt").write_text(
        "\n".join(f"{row['candidate_family']}: {row['test_priority']} {row['profile_distance']}" for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive carry follow-up candidates")
    parser.add_argument("--carry-profile-contrast", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = _read_csv(args.carry_profile_contrast)
    candidates = build_candidates(rows, args.limit)
    write_report(args.output_dir, candidates)
    print(
        json.dumps(
            {
                "candidate_count": len(candidates),
                "top_candidate": candidates[0]["candidate_family"] if candidates else "-",
                "passive_only": True,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
