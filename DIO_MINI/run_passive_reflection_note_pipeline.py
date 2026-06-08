"""Run passive lupe, sense separation, and reflection-note pipeline.

The pipeline is diagnostic only. It reads candidate validation rows and trace
CSVs, then creates per-family passive notes plus an overview.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.build_passive_reflection_note import build_note, write_outputs as write_note_outputs
from DIO_MINI.report_passive_candidate_sense_separation import build_report, write_outputs as write_sense_outputs
from DIO_MINI.report_passive_reflection_candidate_lupe import build_lupe, write_outputs as write_lupe_outputs


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _truthy(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes"}


def _select_families(validation_path: Path, only_validation_seen: bool) -> list[dict]:
    rows = _read_csv(validation_path)
    selected: list[dict] = []
    for row in rows:
        if not _truthy(row.get("candidate_only")):
            continue
        if only_validation_seen and not _truthy(row.get("validation_seen")):
            continue
        selected.append(row)
    selected.sort(key=lambda row: str(row.get("symbol_family", "") or ""))
    return selected


def _emergence_reading(note: dict) -> str:
    state = str(note.get("passive_reflection_note_state", "") or "")
    best_actions = str(note.get("best_actions", "") or "")
    stable_fields = str(note.get("stable_fields", "") or "")
    if state == "passive_reflection_note_stable_field_unstable_direction":
        return "emergence_candidate_form_field_without_direction"
    if state == "passive_reflection_note_stable_field_and_direction":
        return "stable_form_field_direction_candidate"
    if stable_fields and "|" in best_actions:
        return "possible_emergence_candidate_needs_more_worlds"
    return "not_emergence_candidate_yet"


def run_pipeline(
    validation_path: Path,
    trace_paths: list[Path],
    output_dir: Path,
    only_validation_seen: bool,
) -> tuple[list[dict], list[dict]]:
    selected = _select_families(validation_path, only_validation_seen=only_validation_seen)
    output_dir.mkdir(parents=True, exist_ok=True)
    overview: list[dict] = []

    for candidate in selected:
        family = str(candidate.get("symbol_family", "") or "")
        if not family:
            continue
        family_dir = output_dir / family
        lupe_dir = family_dir / "lupe"
        sense_dir = family_dir / "sense_separation"
        note_dir = family_dir / "reflection_note"

        detail, lupe_summary = build_lupe(family, trace_paths)
        write_lupe_outputs(family, detail, lupe_summary, lupe_dir)

        lupe_csv = lupe_dir / f"{family}_passive_reflection_candidate_lupe.csv"
        field_summary, group_summary, sense_overall = build_report(lupe_csv)
        write_sense_outputs(field_summary, group_summary, sense_overall, sense_dir)

        overall_csv = sense_dir / f"{family}_sense_separation_overall.csv"
        fields_csv = sense_dir / f"{family}_sense_separation_fields.csv"
        note = build_note(overall_csv, fields_csv)
        write_note_outputs(note, note_dir)

        overview.append(
            {
                "symbol_family": family,
                "validation_result_state": str(candidate.get("validation_result_state", "") or ""),
                "candidate_state": str(candidate.get("candidate_state", "") or ""),
                "validation_seen": _truthy(candidate.get("validation_seen")),
                "lupe_count": int(lupe_summary.get("count", 0) or 0),
                "lupe_world_count": int(lupe_summary.get("debug_root_count", 0) or 0),
                "best_actions": str(note.get("best_actions", "") or ""),
                "stable_fields": str(note.get("stable_fields", "") or ""),
                "variant_fields": str(note.get("variant_fields", "") or ""),
                "inner_states": str(note.get("inner_states", "") or ""),
                "reflection_states": str(note.get("reflection_states", "") or ""),
                "passive_reflection_note_state": str(note.get("passive_reflection_note_state", "") or ""),
                "emergence_reading": _emergence_reading(note),
                "passive_only": True,
                "writes_runtime_memory": False,
                "read_by_mini_dio": False,
                "influences_action": False,
                "is_gate": False,
                "is_motoric": False,
                "is_entry_signal": False,
                "is_direction_signal": False,
            }
        )

    groups: dict[str, dict] = {}
    for row in overview:
        key = str(row.get("emergence_reading", "") or "-")
        group = groups.setdefault(
            key,
            {
                "emergence_reading": key,
                "family_count": 0,
                "families": [],
                "passive_only": True,
                "influences_action": False,
            },
        )
        group["family_count"] += 1
        group["families"].append(str(row.get("symbol_family", "") or ""))

    summary = [
        {
            "emergence_reading": group["emergence_reading"],
            "family_count": int(group["family_count"]),
            "families": "|".join(sorted(group["families"])),
            "passive_only": True,
            "influences_action": False,
        }
        for group in groups.values()
    ]
    summary.sort(key=lambda row: (-int(row["family_count"]), str(row["emergence_reading"])))
    overview.sort(key=lambda row: str(row.get("symbol_family", "") or ""))
    return overview, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_pipeline_outputs(overview: list[dict], summary: list[dict], output_dir: Path) -> None:
    overview_path = output_dir / "passive_reflection_note_pipeline_overview.csv"
    summary_path = output_dir / "passive_reflection_note_pipeline_summary.csv"
    json_path = output_dir / "passive_reflection_note_pipeline.json"
    md_path = output_dir / "passive_reflection_note_pipeline.md"

    _write_csv(overview_path, overview, ["symbol_family", "emergence_reading"])
    _write_csv(summary_path, summary, ["emergence_reading", "family_count"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": {
                    "passive_only": True,
                    "writes_runtime_memory": False,
                    "read_by_mini_dio": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_entry_signal": False,
                    "is_direction_signal": False,
                },
                "overview": overview,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Passive Reflection Note Pipeline",
        "",
        "## Grenze",
        "- passiv",
        "- kein Runtime-Speicher",
        "- kein Entry",
        "- kein Gate",
        "- keine Richtung",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine Familien")
    else:
        for row in summary:
            lines.append(
                f"- {row['emergence_reading']}: families={row['family_count']} "
                f"{row['families']}"
            )
    lines.extend(["", "## Familien"])
    for row in overview:
        lines.append(
            f"- {row['symbol_family']}: {row['emergence_reading']} "
            f"note={row['passive_reflection_note_state']} "
            f"best={row['best_actions']} stable={row['stable_fields']}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run passive reflection note pipeline")
    parser.add_argument("--validation", required=True)
    parser.add_argument("--trace", required=True, nargs="+")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--all-candidates", action="store_true")
    args = parser.parse_args()

    overview, summary = run_pipeline(
        Path(args.validation),
        [Path(item) for item in args.trace],
        Path(args.output_dir),
        only_validation_seen=not bool(args.all_candidates),
    )
    write_pipeline_outputs(overview, summary, Path(args.output_dir))
    print(f"families={len(overview)} summary_rows={len(summary)}")


if __name__ == "__main__":
    main()
