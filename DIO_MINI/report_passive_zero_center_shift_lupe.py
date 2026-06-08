"""Track passive zero-topology center shifts across stages.

This diagnostic follows selected families through semantic islands and reports
whether a periphery member becomes center-near after follow-up contact.

Passive only. No runtime memory, no action, no gate, no entry, no direction.
Designed for controlled datasets first, not for long-run claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
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


def _parse_stage(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise ValueError(f"Stage must be LABEL=matrix_dir: {value}")
    label, path = value.split("=", 1)
    return label.strip(), Path(path.strip())


def _edge_key(left: str, right: str) -> str:
    return "|".join(sorted([left, right]))


def _find_island(islands: list[dict[str, str]], family: str) -> dict[str, str]:
    for island in islands:
        if family in _families(island.get("families")):
            return island
    return {}


def _degree_map(edges: list[dict[str, str]], members: list[str]) -> dict[str, int]:
    member_set = set(members)
    degrees = {member: 0 for member in members}
    for edge in edges:
        left = str(edge.get("left_family", "") or "")
        right = str(edge.get("right_family", "") or "")
        if left in member_set and right in member_set:
            degrees[left] += 1
            degrees[right] += 1
    return degrees


def _neighbors(edges: list[dict[str, str]], family: str, members: list[str]) -> list[str]:
    member_set = set(members)
    result: set[str] = set()
    for edge in edges:
        left = str(edge.get("left_family", "") or "")
        right = str(edge.get("right_family", "") or "")
        if left == family and right in member_set:
            result.add(right)
        if right == family and left in member_set:
            result.add(left)
    return sorted(result)


def _role_for(degree: int, max_degree: int, family_count: int) -> str:
    if family_count <= 1:
        return "single_trace"
    if degree <= 0:
        return "uncoupled_member"
    if degree == max_degree and max_degree > 0:
        return "center_candidate"
    if degree >= max(1, max_degree - 1):
        return "center_near_partner"
    return "periphery_member"


def build_report(stages: list[tuple[str, Path]], families: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for stage_index, (label, matrix_dir) in enumerate(stages, start=1):
        islands = _read_csv(matrix_dir / "passive_semantic_matrix_islands.csv")
        edges = _read_csv(matrix_dir / "passive_semantic_matrix_edges.csv")
        for family in families:
            island = _find_island(islands, family)
            members = _families(island.get("families")) if island else []
            degrees = _degree_map(edges, members)
            max_degree = max([degrees.get(member, 0) for member in members] or [0])
            degree = degrees.get(family, 0)
            family_count = len(members)
            possible_edges = max(0, family_count * (family_count - 1) // 2)
            edge_count = sum(degrees.values()) // 2
            role = _role_for(degree, max_degree, family_count)
            center_candidates = sorted(member for member in members if degrees.get(member, 0) == max_degree and max_degree > 0)
            row = {
                "stage_order": stage_index,
                "stage": label,
                "family": family,
                "found": bool(island),
                "island_id": str(island.get("island_id", "") or "-"),
                "island_members": "|".join(members) if members else "-",
                "family_count": family_count,
                "edge_count": edge_count,
                "possible_edge_count": possible_edges,
                "local_edge_density": round(edge_count / max(1, possible_edges), 6),
                "degree": degree,
                "max_degree": max_degree,
                "degree_share": round(degree / max(1, max_degree), 6),
                "role": role,
                "center_candidates": "|".join(center_candidates) if center_candidates else "-",
                "neighbors": "|".join(_neighbors(edges, family, members)) if members else "-",
                **BOUNDARY,
            }
            rows.append(row)
            by_family[family].append(row)

    summary: list[dict[str, Any]] = []
    for family, traces in by_family.items():
        first = traces[0] if traces else {}
        last = traces[-1] if traces else {}
        first_role = str(first.get("role", "-"))
        last_role = str(last.get("role", "-"))
        first_degree = _safe_float(first.get("degree"))
        last_degree = _safe_float(last.get("degree"))
        state = "role_stable"
        if first_role != last_role and last_role == "center_candidate":
            state = "shifted_into_center_candidate"
        elif first_role != last_role and last_role == "center_near_partner":
            state = "shifted_center_near"
        elif last_degree > first_degree:
            state = "degree_strengthened"
        elif last_degree < first_degree:
            state = "degree_weakened"
        summary.append(
            {
                "family": family,
                "first_role": first_role,
                "last_role": last_role,
                "first_degree": first_degree,
                "last_degree": last_degree,
                "first_center_candidates": str(first.get("center_candidates", "-")),
                "last_center_candidates": str(last.get("center_candidates", "-")),
                "center_shift_state": state,
                "center_shift_reading": _reading(state),
                **BOUNDARY,
            }
        )
    return rows, summary


def _reading(state: str) -> str:
    if state == "shifted_into_center_candidate":
        return "Rand- oder Partnerfamilie wird im letzten Kontakt selbst zentrumsnaher Pol."
    if state == "shifted_center_near":
        return "Familie bewegt sich in Richtung Zentrum, bleibt aber noch nicht Zentrumskandidat."
    if state == "degree_strengthened":
        return "Kopplungsgrad steigt; Rolle bleibt formal gleich."
    if state == "degree_weakened":
        return "Kopplungsgrad faellt; Rolle verliert Tragung."
    return "Rolle bleibt ueber die Stufen stabil."


def write_outputs(rows: list[dict[str, Any]], summary: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_zero_center_shift_trace.csv", rows, ["stage", "family", "role"])
    _write_csv(output_dir / "passive_zero_center_shift_summary.csv", summary, ["family", "center_shift_state"])
    (output_dir / "passive_zero_center_shift_lupe.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_zero_center_shift_lupe.v1",
                "boundary": BOUNDARY,
                "trace": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Zero Center Shift Lupe",
        "",
        "Passive Diagnose fuer kontrollierte Datensaetze. Keine Aussage ueber lange Laeufe.",
        "Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Summary",
        "",
    ]
    for row in summary:
        lines.append(
            f"- {row['family']}: {row['center_shift_state']}; "
            f"{row['first_role']} -> {row['last_role']}; "
            f"centers={row['first_center_candidates']} -> {row['last_center_candidates']}"
        )
    (output_dir / "passive_zero_center_shift_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive zero-center shift lupe")
    parser.add_argument("--stage", action="append", required=True, help="LABEL=matrix_dir")
    parser.add_argument("--family", action="append", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    rows, summary = build_report([_parse_stage(value) for value in args.stage], list(args.family))
    write_outputs(rows, summary, args.output_dir)
    print(
        json.dumps(
            {
                "trace_rows": len(rows),
                "summary": summary,
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
