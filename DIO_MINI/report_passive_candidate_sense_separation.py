"""Separate senses, inner state, and afterlook for one passive candidate.

The report is diagnostic only. It reads a candidate lupe CSV and checks whether
the family is stable in seeing, hearing, feeling, inner state, or only afterlook.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SENSE_FIELDS = [
    "sehen_form_stability",
    "hoeren_energy_tone",
    "fuehlen_mcm_coherence",
    "fuehlen_mcm_tension",
    "reflection_context_carry",
    "reflection_context_strain",
    "reflection_context_alignment",
]


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _stats(values: list[float]) -> dict:
    if not values:
        return {"count": 0, "min": 0.0, "max": 0.0, "range": 0.0, "avg": 0.0}
    lo = min(values)
    hi = max(values)
    return {
        "count": len(values),
        "min": round(lo, 6),
        "max": round(hi, 6),
        "range": round(hi - lo, 6),
        "avg": round(sum(values) / len(values), 6),
    }


def _stability_label(range_value: float) -> str:
    if range_value <= 0.02:
        return "stable"
    if range_value <= 0.08:
        return "soft_variant"
    return "variant"


def build_report(lupe_path: Path) -> tuple[list[dict], list[dict], dict]:
    rows = _read_csv(lupe_path)
    if not rows:
        return [], [], {"count": 0}

    family = str(rows[0].get("symbol_family", "") or "-")
    roots = sorted({str(row.get("debug_root", "") or "") for row in rows if row.get("debug_root")})
    best_actions = sorted({str(row.get("best_action_training", "") or "") for row in rows if row.get("best_action_training")})
    inner_states = sorted({str(row.get("passive_inner_awareness_state", "") or "") for row in rows})
    reflection_states = sorted({str(row.get("reflection_context_state", "") or "") for row in rows})

    field_summary: list[dict] = []
    for field in SENSE_FIELDS:
        stats = _stats([_safe_float(row.get(field)) for row in rows])
        field_summary.append(
            {
                "symbol_family": family,
                "field": field,
                "count": stats["count"],
                "min": stats["min"],
                "max": stats["max"],
                "range": stats["range"],
                "avg": stats["avg"],
                "stability": _stability_label(float(stats["range"])),
                "passive_only": True,
                "influences_action": False,
            }
        )

    group_summary: list[dict] = []
    for key_name in ["best_action_training", "debug_root", "reflection_context_state"]:
        for key_value in sorted({str(row.get(key_name, "") or "-") for row in rows}):
            group_rows = [row for row in rows if str(row.get(key_name, "") or "-") == key_value]
            item = {
                "symbol_family": family,
                "group_by": key_name,
                "group_value": key_value,
                "count": len(group_rows),
                "best_actions": "|".join(sorted({str(row.get("best_action_training", "") or "") for row in group_rows})),
                "inner_states": "|".join(sorted({str(row.get("passive_inner_awareness_state", "") or "") for row in group_rows})),
                "reflection_states": "|".join(sorted({str(row.get("reflection_context_state", "") or "") for row in group_rows})),
                "passive_only": True,
                "influences_action": False,
            }
            for field in SENSE_FIELDS:
                stats = _stats([_safe_float(row.get(field)) for row in group_rows])
                item[f"{field}_avg"] = stats["avg"]
                item[f"{field}_range"] = stats["range"]
            group_summary.append(item)

    stable_fields = [row["field"] for row in field_summary if row["stability"] == "stable"]
    variant_fields = [row["field"] for row in field_summary if row["stability"] == "variant"]
    direction_stable = len(best_actions) == 1
    inner_stable = len(inner_states) == 1
    reflection_stable = len(reflection_states) == 1
    if inner_stable and not direction_stable:
        interpretation = "stable_inner_state_with_direction_variance"
    elif inner_stable and direction_stable:
        interpretation = "stable_inner_state_and_direction"
    elif not inner_stable and direction_stable:
        interpretation = "direction_stable_inner_variant"
    else:
        interpretation = "inner_and_direction_variant"

    overall = {
        "symbol_family": family,
        "count": len(rows),
        "debug_root_count": len(roots),
        "debug_roots": "|".join(roots),
        "best_actions": "|".join(best_actions),
        "inner_states": "|".join(inner_states),
        "reflection_states": "|".join(reflection_states),
        "stable_fields": "|".join(stable_fields),
        "variant_fields": "|".join(variant_fields),
        "direction_stable": direction_stable,
        "inner_stable": inner_stable,
        "reflection_stable": reflection_stable,
        "interpretation": interpretation,
        "passive_only": True,
        "influences_action": False,
        "is_gate": False,
        "is_motoric": False,
        "is_entry_signal": False,
    }
    return field_summary, group_summary, overall


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(field_summary: list[dict], group_summary: list[dict], overall: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    family = str(overall.get("symbol_family", "candidate") or "candidate")
    field_path = output_dir / f"{family}_sense_separation_fields.csv"
    group_path = output_dir / f"{family}_sense_separation_groups.csv"
    overall_path = output_dir / f"{family}_sense_separation_overall.csv"
    json_path = output_dir / f"{family}_sense_separation.json"
    md_path = output_dir / f"{family}_sense_separation.md"

    _write_csv(field_path, field_summary, ["symbol_family", "field", "stability"])
    _write_csv(group_path, group_summary, ["symbol_family", "group_by", "group_value"])
    _write_csv(overall_path, [overall], list(overall.keys()) if overall else ["symbol_family"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": {
                    "passive_only": True,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_entry_signal": False,
                },
                "overall": overall,
                "field_summary": field_summary,
                "group_summary": group_summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        f"# Passive Candidate Sense Separation: {family}",
        "",
        "## Grenze",
        "- liest nur Lupe",
        "- keine Handlung",
        "- kein Entry",
        "- kein Gate",
        "",
        "## Gesamt",
        f"- count={overall.get('count', 0)}",
        f"- debug_root_count={overall.get('debug_root_count', 0)}",
        f"- best_actions={overall.get('best_actions', '-')}",
        f"- inner_states={overall.get('inner_states', '-')}",
        f"- reflection_states={overall.get('reflection_states', '-')}",
        f"- interpretation={overall.get('interpretation', '-')}",
        "",
        "## Felder",
    ]
    for row in field_summary:
        lines.append(
            f"- {row['field']}: avg={row['avg']} range={row['range']} stability={row['stability']}"
        )
    lines.extend(["", "## Lesung"])
    if overall.get("interpretation") == "stable_inner_state_with_direction_variance":
        lines.append(
            "- Die Innenlage ist stabil, aber die Nachblick-Richtung variiert. "
            "Das ist keine Richtung, sondern eine wiederkehrende Innen-/Feldlage."
        )
    else:
        lines.append("- Die Lupe muss weiter gegen zusaetzliche Welten gelesen werden.")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Separate senses for a passive candidate lupe")
    parser.add_argument("--lupe", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    field_summary, group_summary, overall = build_report(Path(args.lupe))
    write_outputs(field_summary, group_summary, overall, Path(args.output_dir))
    print(
        f"family={overall.get('symbol_family', '-')} "
        f"fields={len(field_summary)} groups={len(group_summary)} interpretation={overall.get('interpretation', '-')}"
    )


if __name__ == "__main__":
    main()
