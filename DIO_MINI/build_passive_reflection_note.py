"""Build a passive reflection note from a sense-separation report.

The note is a documentation and later-review artifact. It is not read by the
Mini-DIO runtime and does not influence action.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _read_one(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return dict(rows[0]) if rows else {}


def _read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _truthy(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes"}


def build_note(overall_path: Path, fields_path: Path) -> dict:
    overall = _read_one(overall_path)
    fields = _read_rows(fields_path)
    family = str(overall.get("symbol_family", "") or "-")
    best_actions = str(overall.get("best_actions", "") or "")
    stable_fields = str(overall.get("stable_fields", "") or "")
    variant_fields = str(overall.get("variant_fields", "") or "")
    interpretation = str(overall.get("interpretation", "") or "")
    direction_stable = _truthy(overall.get("direction_stable"))
    inner_stable = _truthy(overall.get("inner_stable"))

    if inner_stable and not direction_stable:
        note_state = "passive_reflection_note_stable_field_unstable_direction"
        note_text = (
            "Ich sehe/fuehle diese Lage stabil, aber meine Deutung der Richtung ist nicht stabil. "
            "Meine Vorsicht ist hier wiederkehrend, darf aber noch nicht motorisch geloest werden."
        )
    elif inner_stable and direction_stable:
        note_state = "passive_reflection_note_stable_field_and_direction"
        note_text = (
            "Ich sehe/fuehle diese Lage stabil und die Nachblick-Richtung ist einheitlich. "
            "Das bleibt trotzdem eine Reflexionsnotiz, kein Entry."
        )
    else:
        note_state = "passive_reflection_note_unstable_inner_context"
        note_text = (
            "Diese Lage ist noch nicht stabil genug fuer eine Reflexionsspeicher-Reifung."
        )

    return {
        "symbol_family": family,
        "passive_reflection_note_state": note_state,
        "note_text": note_text,
        "interpretation": interpretation,
        "best_actions": best_actions,
        "stable_fields": stable_fields,
        "variant_fields": variant_fields,
        "inner_states": str(overall.get("inner_states", "") or ""),
        "reflection_states": str(overall.get("reflection_states", "") or ""),
        "debug_root_count": str(overall.get("debug_root_count", "0") or "0"),
        "count": str(overall.get("count", "0") or "0"),
        "field_summary": fields,
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
    }


def write_outputs(note: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    family = str(note.get("symbol_family", "candidate") or "candidate")
    json_path = output_dir / f"{family}_passive_reflection_note.json"
    md_path = output_dir / f"{family}_passive_reflection_note.md"
    csv_path = output_dir / f"{family}_passive_reflection_note.csv"

    json_path.write_text(json.dumps(note, indent=2, sort_keys=True), encoding="utf-8")
    flat = {
        key: value
        for key, value in note.items()
        if key not in {"field_summary", "boundary"}
    }
    flat.update({f"boundary_{key}": value for key, value in dict(note.get("boundary", {})).items()})
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat.keys()))
        writer.writeheader()
        writer.writerow(flat)

    lines = [
        f"# Passive Reflection Note: {family}",
        "",
        "## Grenze",
        "- passive Notiz",
        "- kein Runtime-Speicher",
        "- kein Entry",
        "- kein Gate",
        "- keine Richtung",
        "",
        "## Notiz",
        note.get("note_text", ""),
        "",
        "## Befund",
        f"- state={note.get('passive_reflection_note_state', '-')}",
        f"- interpretation={note.get('interpretation', '-')}",
        f"- best_actions={note.get('best_actions', '-')}",
        f"- stable_fields={note.get('stable_fields', '-')}",
        f"- variant_fields={note.get('variant_fields', '-')}",
        f"- inner_states={note.get('inner_states', '-')}",
        f"- reflection_states={note.get('reflection_states', '-')}",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive reflection note")
    parser.add_argument("--overall", required=True)
    parser.add_argument("--fields", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    note = build_note(Path(args.overall), Path(args.fields))
    write_outputs(note, Path(args.output_dir))
    print(f"family={note.get('symbol_family', '-')} state={note.get('passive_reflection_note_state', '-')}")


if __name__ == "__main__":
    main()
