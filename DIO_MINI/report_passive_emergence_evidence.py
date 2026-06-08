"""Build a passive emergence evidence report for Mini-DIO families.

This is diagnostic only. It reads validation/pipeline CSV files and writes an
evidence map. It does not write runtime memory and does not influence action.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def _truthy(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes"}


def _source_label(path: Path) -> str:
    text = str(path.parent.name or path.stem)
    text = text.replace("dio_mini_passive_reflection_candidate_validation_", "")
    text = text.replace("dio_mini_passive_reflection_note_pipeline_validated_", "")
    return text or path.stem


def build_evidence(validation_paths: list[Path], pipeline_overview_paths: list[Path]) -> tuple[list[dict], list[dict]]:
    families: dict[str, dict] = {}

    for path in validation_paths:
        source = _source_label(path)
        for row in _read_csv(path):
            family = str(row.get("symbol_family", "") or "-")
            if family == "-":
                continue
            item = families.setdefault(
                family,
                {
                    "symbol_family": family,
                    "candidate_only": False,
                    "validation_sources_seen": set(),
                    "validation_sources_withheld": set(),
                    "validation_observation_count": 0,
                    "validation_withheld_best_trade_count": 0,
                    "validation_best_actions": set(),
                    "emergence_readings": set(),
                    "note_states": set(),
                    "stable_fields": set(),
                },
            )
            if _truthy(row.get("candidate_only")):
                item["candidate_only"] = True
            if _truthy(row.get("validation_seen")):
                item["validation_sources_seen"].add(source)
            withheld = _safe_int(row.get("validation_withheld_best_trade_count"))
            if withheld > 0:
                item["validation_sources_withheld"].add(source)
            item["validation_observation_count"] += _safe_int(row.get("validation_observation_count"))
            item["validation_withheld_best_trade_count"] += withheld
            for part in str(row.get("validation_best_actions", "") or "").split("|"):
                part = part.strip()
                if part:
                    item["validation_best_actions"].add(part)

    for path in pipeline_overview_paths:
        for row in _read_csv(path):
            family = str(row.get("symbol_family", "") or "-")
            if family == "-":
                continue
            item = families.setdefault(
                family,
                {
                    "symbol_family": family,
                    "candidate_only": False,
                    "validation_sources_seen": set(),
                    "validation_sources_withheld": set(),
                    "validation_observation_count": 0,
                    "validation_withheld_best_trade_count": 0,
                    "validation_best_actions": set(),
                    "emergence_readings": set(),
                    "note_states": set(),
                    "stable_fields": set(),
                },
            )
            reading = str(row.get("emergence_reading", "") or "").strip()
            if reading:
                item["emergence_readings"].add(reading)
            note_state = str(row.get("note_state", "") or "").strip()
            if note_state:
                item["note_states"].add(note_state)
            for part in str(row.get("stable_fields", "") or "").split("|"):
                part = part.strip()
                if part:
                    item["stable_fields"].add(part)

    detail: list[dict] = []
    summary_groups: dict[str, dict] = {}
    for item in families.values():
        readings = sorted(item["emergence_readings"])
        best_actions = sorted(item["validation_best_actions"])
        sources_seen = sorted(item["validation_sources_seen"])
        source_count = len(sources_seen)
        has_emergence_without_direction = "emergence_candidate_form_field_without_direction" in item["emergence_readings"]
        has_direction_candidate = "stable_form_field_direction_candidate" in item["emergence_readings"]
        if has_emergence_without_direction and source_count >= 3:
            evidence_state = "repeated_passive_emergence_candidate"
        elif has_emergence_without_direction:
            evidence_state = "passive_emergence_candidate"
        elif has_direction_candidate:
            evidence_state = "passive_stable_direction_candidate"
        elif source_count > 0:
            evidence_state = "passive_validation_seen"
        else:
            evidence_state = "not_seen_in_validation"

        row = {
            "symbol_family": item["symbol_family"],
            "evidence_state": evidence_state,
            "candidate_only": bool(item["candidate_only"]),
            "validation_source_count": source_count,
            "validation_sources_seen": "|".join(sources_seen),
            "validation_sources_withheld": "|".join(sorted(item["validation_sources_withheld"])),
            "validation_observation_count": int(item["validation_observation_count"]),
            "validation_withheld_best_trade_count": int(item["validation_withheld_best_trade_count"]),
            "validation_best_actions": "|".join(best_actions),
            "emergence_readings": "|".join(readings),
            "note_states": "|".join(sorted(item["note_states"])),
            "stable_fields": "|".join(sorted(item["stable_fields"])),
            "passive_only": True,
            "writes_runtime_memory": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "is_direction_signal": False,
        }
        detail.append(row)
        group = summary_groups.setdefault(
            evidence_state,
            {
                "evidence_state": evidence_state,
                "family_count": 0,
                "families": [],
                "validation_source_count_sum": 0,
                "withheld_best_trade_sum": 0,
            },
        )
        group["family_count"] += 1
        group["families"].append(item["symbol_family"])
        group["validation_source_count_sum"] += source_count
        group["withheld_best_trade_sum"] += int(item["validation_withheld_best_trade_count"])

    detail.sort(
        key=lambda row: (
            0 if row["evidence_state"] == "repeated_passive_emergence_candidate" else 1,
            -int(row["validation_source_count"]),
            str(row["symbol_family"]),
        )
    )
    summary = [
        {
            "evidence_state": group["evidence_state"],
            "family_count": int(group["family_count"]),
            "families": "|".join(sorted(group["families"])),
            "validation_source_count_sum": int(group["validation_source_count_sum"]),
            "withheld_best_trade_sum": int(group["withheld_best_trade_sum"]),
            "passive_only": True,
            "influences_action": False,
        }
        for group in summary_groups.values()
    ]
    summary.sort(key=lambda row: (-int(row["family_count"]), str(row["evidence_state"])))
    return detail, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_emergence_evidence.csv"
    summary_path = output_dir / "passive_emergence_evidence_summary.csv"
    json_path = output_dir / "passive_emergence_evidence.json"
    md_path = output_dir / "passive_emergence_evidence.md"

    _write_csv(detail_path, detail, ["symbol_family", "evidence_state"])
    _write_csv(summary_path, summary, ["evidence_state", "family_count"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": {
                    "passive_only": True,
                    "writes_runtime_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_entry_signal": False,
                    "is_direction_signal": False,
                },
                "detail": detail,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Passive Emergence Evidence",
        "",
        "## Grenze",
        "- passiv",
        "- kein Runtime-Speicher",
        "- keine Handlung",
        "- keine Richtung",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(
            f"- {row['evidence_state']}: families={row['family_count']} "
            f"sources={row['validation_source_count_sum']} withheld={row['withheld_best_trade_sum']} "
            f"{row['families']}"
        )
    lines.extend(["", "## Staerkste Familien"])
    for row in detail[:12]:
        lines.append(
            f"- {row['symbol_family']}: {row['evidence_state']} "
            f"sources={row['validation_source_count']} seen={row['validation_sources_seen']} "
            f"best={row['validation_best_actions']} readings={row['emergence_readings']}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO emergence evidence report")
    parser.add_argument("--validation", required=True, nargs="+")
    parser.add_argument("--pipeline-overview", required=True, nargs="+")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    detail, summary = build_evidence(
        [Path(item) for item in args.validation],
        [Path(item) for item in args.pipeline_overview],
    )
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"detail_rows={len(detail)} summary_rows={len(summary)}")


if __name__ == "__main__":
    main()
