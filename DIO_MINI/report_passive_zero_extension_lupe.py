"""Inspect how a passive zero-topology island expands.

The report isolates one or more extension families against a base island. It
answers whether an extension is only a visible name, attaches to the bridge
center, attaches to a periphery member, or shifts the island toward a
multi-center field.

Passive only. No runtime memory, no action, no gate, no entry, no direction.
Designed for controlled datasets first, not for long-run claims.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


BOUNDARY = {
    "passive_only": True,
    "controlled_dataset_scope": True,
    "long_run_claim": False,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}

SENSE_FIELDS = [
    "avg_sehen_form_flow",
    "avg_sehen_form_stability",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
]

MCM_FIELDS = [
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
]

NEURO_FIELDS = [
    "avg_mini_focus_tone",
    "avg_mini_trust_tone",
    "avg_mini_caution_tone",
    "avg_mini_strain_tone",
    "avg_mini_neuro_balance",
]


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict[str, Any]], fallback_fields: list[str]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    if not fields:
        fields = fallback_fields
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _families(value: object) -> list[str]:
    text = str(value or "").strip()
    if not text or text == "-":
        return []
    return [item.strip() for item in text.split("|") if item.strip() and item.strip() != "-"]


def _edge_key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted([left, right]))


def _edge_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    result: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        left = str(row.get("left_family", "") or "")
        right = str(row.get("right_family", "") or "")
        if left and right:
            result[_edge_key(left, right)] = row
    return result


def _meaning_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row.get("symbol_family", "") or ""): row for row in rows if row.get("symbol_family")}


def _distance(left: dict[str, str], right: dict[str, str], fields: list[str]) -> float:
    if not left or not right or not fields:
        return 0.0
    total = 0.0
    for field in fields:
        total += (_safe_float(left.get(field)) - _safe_float(right.get(field))) ** 2
    return math.sqrt(total / max(1, len(fields)))


def _find_container(islands: list[dict[str, str]], members: list[str]) -> dict[str, str]:
    target = set(members)
    candidates = []
    for island in islands:
        families = set(_families(island.get("families")))
        if target and target.issubset(families):
            candidates.append(island)
    if not candidates:
        return {}
    return sorted(candidates, key=lambda row: len(_families(row.get("families"))))[0]


def _degree_map(edges: list[dict[str, str]], members: list[str]) -> dict[str, int]:
    member_set = set(members)
    degrees = {member: 0 for member in members}
    for edge in edges:
        left = str(edge.get("left_family", "") or "")
        right = str(edge.get("right_family", "") or "")
        if left in member_set and right in member_set:
            degrees[left] = degrees.get(left, 0) + 1
            degrees[right] = degrees.get(right, 0) + 1
    return degrees


def _extension_state(
    extension: str,
    base_members: list[str],
    center_members: list[str],
    attached: list[str],
    degrees: dict[str, int],
    *,
    extension_found: bool = True,
) -> str:
    if not extension_found:
        return "extension_not_visible"
    center_attached = [member for member in attached if member in center_members]
    periphery_attached = [member for member in attached if member in base_members and member not in center_members]
    if not attached:
        return "visible_but_uncoupled_extension"
    if center_attached and periphery_attached:
        return "center_and_periphery_extension"
    if center_attached:
        return "center_attached_extension"
    if periphery_attached:
        if any(degrees.get(member, 0) >= max(degrees.get(center, 0) for center in center_members or [""]) for member in periphery_attached):
            return "periphery_extension_shifts_center_tension"
        return "periphery_attached_extension"
    return "foreign_extension_contact"


def _state_reading(state: str) -> str:
    if state == "extension_not_visible":
        return "Spur ist in dieser Folgewelt nicht sichtbar."
    if state == "periphery_extension_shifts_center_tension":
        return "Neue Spur koppelt an einen Randpartner und macht diesen zentrumsnaeher; offene 0-Form wird zum Multi-Center-Feld."
    if state == "periphery_attached_extension":
        return "Neue Spur koppelt an Peripherie; Randkontakt ohne direkte Zentrumskopplung."
    if state == "center_attached_extension":
        return "Neue Spur koppelt direkt an das Zentrum; moegliche Zentrumserweiterung."
    if state == "center_and_periphery_extension":
        return "Neue Spur koppelt Zentrum und Peripherie; Integrationskandidat."
    if state == "visible_but_uncoupled_extension":
        return "Spur ist sichtbar, aber ohne Kante zur Basisinsel."
    return "Spur koppelt ausserhalb der angegebenen Basis."


def build_report(
    *,
    meaning_space: Path,
    edges_csv: Path,
    islands_csv: Path,
    base_members: list[str],
    extension_members: list[str],
    base_centers: list[str] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    meaning = _meaning_lookup(_read_csv(meaning_space))
    edge_rows = _read_csv(edges_csv)
    edge_by_key = _edge_lookup(edge_rows)
    islands = _read_csv(islands_csv)

    all_members = sorted(set(base_members + extension_members))
    container = _find_container(islands, all_members)
    container_members = _families(container.get("families")) if container else all_members
    degrees = _degree_map(edge_rows, container_members)
    if base_centers:
        center_members = sorted(member for member in base_centers if member in base_members)
    else:
        max_degree = max([degrees.get(member, 0) for member in base_members] or [0])
        center_members = sorted(member for member in base_members if degrees.get(member, 0) == max_degree and max_degree > 0)

    pair_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    for extension in extension_members:
        attached: list[str] = []
        for base in base_members:
            edge = edge_by_key.get(_edge_key(extension, base), {})
            visible = bool(edge)
            if visible:
                attached.append(base)
            pair_rows.append(
                {
                    "extension_family": extension,
                    "base_family": base,
                    "edge_visible": visible,
                    "base_role": "center_candidate" if base in center_members else "base_periphery",
                    "meaning_similarity": round(_safe_float(edge.get("meaning_similarity")), 9) if visible else 0.0,
                    "sense_similarity": round(_safe_float(edge.get("sense_similarity")), 9) if visible else 0.0,
                    "mcm_similarity": round(_safe_float(edge.get("mcm_similarity")), 9) if visible else 0.0,
                    "hearing_similarity": round(_safe_float(edge.get("hearing_similarity")), 9) if visible else 0.0,
                    "temporal_similarity": round(_safe_float(edge.get("temporal_similarity")), 9) if visible else 0.0,
                    "neuro_similarity": round(_safe_float(edge.get("neuro_similarity")), 9) if visible else 0.0,
                    "sense_distance": round(_distance(meaning.get(extension, {}), meaning.get(base, {}), SENSE_FIELDS), 9),
                    "mcm_distance": round(_distance(meaning.get(extension, {}), meaning.get(base, {}), MCM_FIELDS), 9),
                    "neuro_distance": round(_distance(meaning.get(extension, {}), meaning.get(base, {}), NEURO_FIELDS), 9),
                    **BOUNDARY,
                }
            )

        extension_found = extension in meaning
        state = _extension_state(
            extension,
            base_members,
            center_members,
            attached,
            degrees,
            extension_found=extension_found,
        )
        summary_rows.append(
            {
                "extension_family": extension,
                "extension_found": extension_found,
                "container_island_id": str(container.get("island_id", "") or "-"),
                "container_members": "|".join(container_members) if container_members else "-",
                "base_members": "|".join(base_members),
                "center_members": "|".join(center_members) if center_members else "-",
                "attached_base_members": "|".join(sorted(attached)) if attached else "-",
                "extension_degree": degrees.get(extension, 0),
                "base_degree_map": "|".join(f"{member}:{degrees.get(member, 0)}" for member in base_members),
                "extension_state": state,
                "extension_reading": _state_reading(state),
                **BOUNDARY,
            }
        )
    return pair_rows, summary_rows


def write_outputs(pair_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_zero_extension_pairs.csv", pair_rows, ["extension_family", "base_family"])
    _write_csv(output_dir / "passive_zero_extension_summary.csv", summary_rows, ["extension_family", "extension_state"])
    (output_dir / "passive_zero_extension_lupe.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_zero_extension_lupe.v1",
                "boundary": BOUNDARY,
                "pairs": pair_rows,
                "summary": summary_rows,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Zero Extension Lupe",
        "",
        "Passive Diagnose fuer kontrollierte Datensaetze. Keine Aussage ueber lange Laeufe.",
        "Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Summary",
        "",
    ]
    for row in summary_rows:
        lines.append(
            f"- {row['extension_family']}: {row['extension_state']}; "
            f"attached={row['attached_base_members']}; centers={row['center_members']}"
        )
    lines.extend(["", "## Pairs", ""])
    for row in pair_rows:
        lines.append(
            f"- {row['extension_family']} <-> {row['base_family']}: edge={row['edge_visible']}; "
            f"role={row['base_role']}; meaning={row['meaning_similarity']}; mcm={row['mcm_similarity']}"
        )
    (output_dir / "passive_zero_extension_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive zero-extension lupe")
    parser.add_argument("--meaning-space", required=True, type=Path)
    parser.add_argument("--edges", required=True, type=Path)
    parser.add_argument("--islands", required=True, type=Path)
    parser.add_argument("--base-member", action="append", required=True)
    parser.add_argument("--base-center", action="append", default=[])
    parser.add_argument("--extension-member", action="append", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    pairs, summary = build_report(
        meaning_space=args.meaning_space,
        edges_csv=args.edges,
        islands_csv=args.islands,
        base_members=list(args.base_member),
        extension_members=list(args.extension_member),
        base_centers=list(args.base_center),
    )
    write_outputs(pairs, summary, args.output_dir)
    print(
        json.dumps(
            {
                "pairs": len(pairs),
                "summary": summary,
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
