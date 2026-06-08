"""Build a passive semantic-candidate map from recurring fragments.

The map groups recurring passive fragments into descriptive semantic roles:
sensory core, affective field, auditory energy, reflective context, peripheral
trace, or noise. It is diagnostic only and has no runtime or action effect.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
from pathlib import Path


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


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _expand_patterns(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            paths.extend(Path(match) for match in matches)
        else:
            paths.append(Path(pattern))
    unique = {str(path.resolve()): path for path in paths}
    return [unique[key] for key in sorted(unique)]


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def _semantic_role(fragment: str, group: str, recurrence_state: str) -> str:
    if group == "persistent_shared_core" and fragment in {"sehen_form_stability", "fuehlen_mcm_coherence"}:
        return "sensorisch_affektiver_kern"
    if fragment.startswith("sehen_"):
        return "visueller_formanteil"
    if fragment.startswith("hoeren_"):
        return "auditive_energie"
    if fragment.startswith("fuehlen_"):
        return "affektive_feldwirkung"
    if fragment.startswith("reflection_"):
        return "reflektiver_kontextanteil"
    if recurrence_state.startswith("single_"):
        return "randspur_oder_rauschen"
    return "offener_semantikanteil"


def _candidate_state(recurrence_state: str, semantic_role: str) -> str:
    if recurrence_state == "recurring_passive_shared_core_fragment":
        return "passiver_semantischer_kernkandidat"
    if recurrence_state == "recurring_passive_target_expansion_fragment":
        if semantic_role == "reflektiver_kontextanteil":
            return "passiver_reflexions_semantikkandidat"
        return "passiver_erweiterungs_semantikkandidat"
    if recurrence_state == "recurring_passive_new_shared_fragment":
        return "passiver_neuer_geteilter_semantikkandidat"
    if recurrence_state == "recurring_passive_fragment_trace":
        return "passive_semantikspur"
    return "randspur_oder_rauschen"


def _sentence(row: dict) -> str:
    role = str(row.get("semantic_role", "") or "")
    fragment = str(row.get("fragment", "") or "")
    state = str(row.get("semantic_candidate_state", "") or "")
    if state == "passiver_semantischer_kernkandidat":
        return f"{fragment}: wiederkehrender Kernanteil der praebewussten Innenkarte."
    if state == "passiver_reflexions_semantikkandidat":
        return f"{fragment}: wiederkehrender Reflexionsanteil, noch ohne Handlung."
    if state == "passiver_erweiterungs_semantikkandidat":
        return f"{fragment}: wiederkehrende Eigenverdichtung im Rollenbereich {role}."
    if state == "passiver_neuer_geteilter_semantikkandidat":
        return f"{fragment}: neu geteilter Fragmentanteil, passiv weiter beobachten."
    if state == "passive_semantikspur":
        return f"{fragment}: passive Spur im Rollenbereich {role}, noch nicht stabil genug."
    return f"{fragment}: Randspur oder Rauschen, keine Semantik ableiten."


def build_semantic_map(recurrence_paths: list[Path]) -> tuple[list[dict], list[dict]]:
    grouped_rows: dict[tuple[str, str, str], dict] = {}
    groups: dict[str, dict] = {}

    for path in recurrence_paths:
        for item in _read_csv(path):
            fragment = str(item.get("fragment", "") or "")
            group = str(item.get("fragment_group", "") or "")
            recurrence_state = str(item.get("fragment_recurrence_state", "") or "")
            if not fragment:
                continue
            role = _semantic_role(fragment, group, recurrence_state)
            candidate_state = _candidate_state(recurrence_state, role)
            key = (candidate_state, role, fragment)
            row = grouped_rows.setdefault(
                key,
                {
                    "semantic_candidate_state": candidate_state,
                    "semantic_role": role,
                    "fragment_groups": set(),
                    "fragment": fragment,
                    "fragment_recurrence_states": set(),
                    "source_count": 0,
                    "sources": set(),
                    "target_families": set(),
                    "related_families": set(),
                    "island_states": set(),
                    "island_symbols": set(),
                    **BOUNDARY,
                },
            )
            row["fragment_groups"].add(group)
            row["fragment_recurrence_states"].add(recurrence_state)
            row["source_count"] = max(int(row["source_count"]), _safe_int(item.get("source_count")))
            row["sources"].update(value for value in str(item.get("sources", "") or "").split("|") if value)
            row["target_families"].update(value for value in str(item.get("target_families", "") or "").split("|") if value)
            row["related_families"].update(value for value in str(item.get("related_families", "") or "").split("|") if value)
            row["island_states"].update(value for value in str(item.get("island_states", "") or "").split("|") if value)
            row["island_symbols"].update(value for value in str(item.get("island_symbols", "") or "").split("|") if value)

    rows: list[dict] = []
    for raw in grouped_rows.values():
        row = {
            "semantic_candidate_state": str(raw["semantic_candidate_state"]),
            "semantic_role": str(raw["semantic_role"]),
            "fragment_groups": "|".join(sorted(raw["fragment_groups"])),
            "fragment": str(raw["fragment"]),
            "fragment_recurrence_states": "|".join(sorted(raw["fragment_recurrence_states"])),
            "source_count": int(raw["source_count"]),
            "sources": "|".join(sorted(raw["sources"])),
            "target_families": "|".join(sorted(raw["target_families"])),
            "related_families": "|".join(sorted(raw["related_families"])),
            "island_states": "|".join(sorted(raw["island_states"])),
            "island_symbols": "|".join(sorted(raw["island_symbols"])),
            **BOUNDARY,
        }
        candidate_state = str(row["semantic_candidate_state"])
        role = str(row["semantic_role"])
        fragment = str(row["fragment"])
        row["dio_sentence"] = _sentence(row)
        rows.append(row)

        summary = groups.setdefault(
            candidate_state,
            {
                "semantic_candidate_state": candidate_state,
                "candidate_count": 0,
                "semantic_roles": set(),
                "fragments": [],
            },
        )
        summary["candidate_count"] += 1
        summary["semantic_roles"].add(role)
        summary["fragments"].append(fragment)

    rows.sort(
        key=lambda row: (
            row["semantic_candidate_state"] != "passiver_semantischer_kernkandidat",
            row["semantic_candidate_state"] != "passiver_reflexions_semantikkandidat",
            row["semantic_candidate_state"] != "passiver_erweiterungs_semantikkandidat",
            row["semantic_candidate_state"] != "passiver_neuer_geteilter_semantikkandidat",
            -int(row["source_count"]),
            str(row["semantic_role"]),
            str(row["fragment"]),
        )
    )
    summary_rows = [
        {
            "semantic_candidate_state": item["semantic_candidate_state"],
            "candidate_count": int(item["candidate_count"]),
            "semantic_roles": "|".join(sorted(item["semantic_roles"])),
            "fragments": "|".join(sorted(set(item["fragments"]))),
            **BOUNDARY,
        }
        for item in groups.values()
    ]
    summary_rows.sort(key=lambda row: (-int(row["candidate_count"]), str(row["semantic_candidate_state"])))
    return rows, summary_rows


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_semantic_candidate_map.csv"
    summary_path = output_dir / "passive_semantic_candidate_map_summary.csv"
    json_path = output_dir / "passive_semantic_candidate_map.json"
    md_path = output_dir / "passive_semantic_candidate_map.md"
    _write_csv(detail_path, rows, ["semantic_candidate_state", "semantic_role", "fragment"])
    _write_csv(summary_path, summary, ["semantic_candidate_state", "candidate_count"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": BOUNDARY,
                "candidates": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Semantic Candidate Map",
        "",
        "## Grenze",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- keine Richtung",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(f"- {row['semantic_candidate_state']}: {row['candidate_count']}")
    lines.extend(["", "## Details"])
    for row in rows:
        lines.append(
            f"- {row['semantic_candidate_state']} / {row['semantic_role']}: "
            f"{row['fragment']} sources={row['source_count']}"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fragment-recurrence", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    paths = _expand_patterns(args.fragment_recurrence)
    rows, summary = build_semantic_map(paths)
    write_outputs(rows, summary, Path(args.output_dir))
    print(f"recurrence_sources={len(paths)} semantic_candidates={len(rows)} summary_rows={len(summary)}")
    for row in summary:
        print(f"{row['semantic_candidate_state']}={row['candidate_count']}")


if __name__ == "__main__":
    main()
