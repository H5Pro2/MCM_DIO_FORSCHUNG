"""Report passive growth of emergent semantic islands across Mini-DIO stages.

This diagnostic follows selected symbol families across multiple stages and
checks whether they remain isolated, disappear, or become part of a semantic
island with density and partners.

Diagnostic only: no runtime memory, no action, no entry, no gate.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


BOUNDARY = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value if value not in (None, "") else default))
    except Exception:
        return default


def _parse_stage_arg(raw: str, flag: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise SystemExit(f"{flag} must be label=path, got: {raw}")
    label, path = raw.split("=", 1)
    return label.strip(), Path(path.strip())


def _families(value: object) -> list[str]:
    text = str(value or "").strip()
    if not text or text == "-":
        return []
    return [part.strip() for part in text.split("|") if part.strip() and part.strip() != "-"]


def _family_row(rows: list[dict[str, str]], family: str) -> dict[str, str]:
    for row in rows:
        if str(row.get("symbol_family", "") or "") == family:
            return row
    return {}


def _island_for_family(rows: list[dict[str, str]], family: str) -> dict[str, str]:
    for row in rows:
        members = _families(row.get("families"))
        if family in members:
            return row
    return {}


def _density_for_island(rows: list[dict[str, str]], island_id: str) -> dict[str, str]:
    for row in rows:
        if str(row.get("island_id", "") or "") == island_id:
            return row
    return {}


def _stage_state(found: bool, members: list[str], density_state: str) -> str:
    if not found:
        return "not_visible"
    if len(members) <= 1:
        return "visible_isolated"
    if density_state == "passive_semantic_density_center":
        return "coupled_density_center"
    if density_state:
        return "coupled_semantic_island"
    return "coupled_raw_island"


def _growth_state(states: list[str]) -> str:
    if states and states[-1] == "not_visible" and any(state != "not_visible" for state in states[:-1]):
        if any(state == "coupled_density_center" for state in states[:-1]):
            return "density_center_lost_under_followup_contact"
        return "visible_trace_lost_under_followup_contact"
    visible = [state for state in states if state != "not_visible"]
    if not visible:
        return "not_visible_across_stages"
    if len(set(visible)) == 1:
        return f"stable_{visible[-1]}"
    if visible[0] == "visible_isolated" and visible[-1] == "coupled_density_center":
        return "isolated_trace_to_density_center"
    if visible[0] == "visible_isolated" and visible[-1].startswith("coupled"):
        return "isolated_trace_to_coupled_island"
    if visible[-1] == "not_visible":
        return "visible_trace_lost"
    return "mixed_island_reorganization"


def build_report(
    meaning_stages: list[tuple[str, Path]],
    island_stages: list[tuple[str, Path]],
    density_stages: list[tuple[str, Path]],
    candidates: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    meaning_by_label = {label: _read_csv(path) for label, path in meaning_stages}
    islands_by_label = {label: _read_csv(path) for label, path in island_stages}
    density_by_label = {label: _read_csv(path) for label, path in density_stages}
    labels = [label for label, _ in meaning_stages]

    detail: list[dict[str, Any]] = []
    for family in candidates:
        for label in labels:
            meaning_rows = meaning_by_label.get(label, [])
            island_rows = islands_by_label.get(label, [])
            density_rows = density_by_label.get(label, [])
            family_meta = _family_row(meaning_rows, family)
            island = _island_for_family(island_rows, family)
            island_id = str(island.get("island_id", "") or "")
            density = _density_for_island(density_rows, island_id) if island_id else {}
            members = _families(island.get("families"))
            partners = [item for item in members if item != family]
            found = bool(family_meta)
            density_state = str(density.get("density_state", "") or "")
            detail.append(
                {
                    "symbol_family": family,
                    "stage": label,
                    "family_found": found,
                    "stage_state": _stage_state(found, members, density_state),
                    "island_id": island_id or "-",
                    "island_members": "|".join(members) if members else "-",
                    "partners": "|".join(partners) if partners else "-",
                    "partner_count": len(partners),
                    "family_count": _safe_int(island.get("family_count"), len(members)),
                    "edge_count": _safe_int(island.get("edge_count")),
                    "avg_meaning_similarity": round(_safe_float(island.get("avg_meaning_similarity")), 9),
                    "semantic_density": round(_safe_float(density.get("semantic_density")), 9),
                    "variant_attraction": round(_safe_float(density.get("variant_attraction")), 9),
                    "island_growth": round(_safe_float(density.get("island_growth")), 9),
                    "island_fragmentation": round(_safe_float(density.get("island_fragmentation")), 9),
                    "semantic_vorticity": round(_safe_float(density.get("semantic_vorticity")), 9),
                    "density_state": density_state or "-",
                    "dominant_neuro_tone": str(family_meta.get("dominant_neuro_tone", "") or "-"),
                    "dominant_temporal_state": str(family_meta.get("dominant_temporal_state", "") or "-"),
                    **BOUNDARY,
                }
            )

    summary: list[dict[str, Any]] = []
    for family in candidates:
        rows = [row for row in detail if row["symbol_family"] == family]
        states = [str(row["stage_state"]) for row in rows]
        partner_sets = [set(_families(row.get("partners"))) for row in rows if row.get("partners") not in ("", "-")]
        all_partners = sorted(set().union(*partner_sets)) if partner_sets else []
        first_density = _safe_float(rows[0].get("semantic_density")) if rows else 0.0
        last_density = _safe_float(rows[-1].get("semantic_density")) if rows else 0.0
        first_growth = _safe_float(rows[0].get("island_growth")) if rows else 0.0
        last_growth = _safe_float(rows[-1].get("island_growth")) if rows else 0.0
        growth = _growth_state(states)
        if growth == "isolated_trace_to_density_center":
            reading = "vorher isolierte Spur; spaeter semantisches Dichtezentrum unter Weltkontakt"
        elif growth == "isolated_trace_to_coupled_island":
            reading = "vorher isolierte Spur; spaeter gekoppelte Bedeutungsinsel"
        elif growth == "density_center_lost_under_followup_contact":
            reading = "Dichtezentrum wird im Folgekontakt nicht mehr sichtbar"
        elif growth == "visible_trace_lost_under_followup_contact":
            reading = "sichtbare Spur wird im Folgekontakt nicht mehr sichtbar"
        elif growth.startswith("stable_"):
            reading = "stabile Stufe ohne sichtbare Reorganisation"
        else:
            reading = "gemischte passive Reorganisation"
        summary.append(
            {
                "symbol_family": family,
                "stage_path": " -> ".join(labels),
                "state_path": " -> ".join(states),
                "growth_state": growth,
                "partner_trace": "|".join(all_partners) if all_partners else "-",
                "first_semantic_density": round(first_density, 9),
                "last_semantic_density": round(last_density, 9),
                "semantic_density_delta": round(last_density - first_density, 9),
                "first_island_growth": round(first_growth, 9),
                "last_island_growth": round(last_growth, 9),
                "island_growth_delta": round(last_growth - first_growth, 9),
                "passive_growth_reading": reading,
                **BOUNDARY,
            }
        )
    return detail, summary


def _write_csv(path: Path, rows: list[dict[str, Any]], fallback_fields: list[str]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fields:
                fields.append(key)
    if not fields:
        fields = fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(detail: list[dict[str, Any]], summary: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_emergent_island_growth_lupe_detail.csv", detail, ["symbol_family", "stage"])
    _write_csv(output_dir / "passive_emergent_island_growth_lupe_summary.csv", summary, ["symbol_family"])
    (output_dir / "passive_emergent_island_growth_lupe.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_emergent_island_growth_lupe.v1",
                "boundary": BOUNDARY,
                "detail": detail,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Emergent Island Growth Lupe",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Zusammenfassung",
        "",
    ]
    for row in summary:
        lines.append(
            f"- {row['symbol_family']}: {row['growth_state']}; "
            f"partners={row['partner_trace']}; density_delta={row['semantic_density_delta']}; "
            f"{row['passive_growth_reading']}."
        )
    lines.extend(["", "## Details", ""])
    for row in detail:
        lines.append(
            f"- {row['symbol_family']} / {row['stage']}: {row['stage_state']}; "
            f"island={row['island_id']}; partners={row['partners']}; "
            f"density={row['semantic_density']}; growth={row['island_growth']}; "
            f"vorticity={row['semantic_vorticity']}"
        )
    (output_dir / "passive_emergent_island_growth_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive emergent island growth lupe")
    parser.add_argument("--stage", action="append", required=True, help="label=passive_cluster_meaning_space.csv")
    parser.add_argument("--island-stage", action="append", required=True, help="label=passive_semantic_matrix_islands.csv")
    parser.add_argument("--density-stage", action="append", required=True, help="label=passive_semantic_density.csv")
    parser.add_argument("--candidate", action="append", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    detail, summary = build_report(
        [_parse_stage_arg(item, "--stage") for item in args.stage],
        [_parse_stage_arg(item, "--island-stage") for item in args.island_stage],
        [_parse_stage_arg(item, "--density-stage") for item in args.density_stage],
        list(args.candidate),
    )
    write_outputs(detail, summary, args.output_dir)
    print(
        json.dumps(
            {
                "candidate_count": len(args.candidate),
                "detail_count": len(detail),
                "summary_count": len(summary),
                "candidates": list(args.candidate),
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
