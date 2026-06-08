"""Report whether a raw passive neighbor becomes mature or stays an echo.

The report compares a mature reference family with a raw neighbor family using
meaning-space and neighbor CSV files. It is diagnostic only.
"""

from __future__ import annotations

import argparse
import csv
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


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def _family(rows: list[dict], family: str) -> dict:
    for row in rows:
        if str(row.get("symbol_family", "") or "") == family:
            return dict(row)
    return {}


def _neighbor(rows: list[dict], left: str, right: str) -> dict:
    for row in rows:
        if {str(row.get("left_family", "") or ""), str(row.get("right_family", "") or "")} == {left, right}:
            return dict(row)
    return {}


def _development_state(reference: dict, raw: dict, neighbor: dict) -> str:
    if not raw:
        return "raw_neighbor_not_seen"
    raw_reife = str(raw.get("candidate_passive_reife_state", "") or "")
    raw_episodes = _safe_int(raw.get("episode_count"))
    meaning_similarity = _safe_float(neighbor.get("meaning_similarity"))
    if raw_reife:
        return "raw_neighbor_became_candidate"
    if meaning_similarity >= 0.96 and raw_episodes >= 2:
        return "raw_neighbor_stable_echo"
    if meaning_similarity >= 0.90:
        return "raw_neighbor_near_but_unmatured"
    return "raw_neighbor_distant"


def build_report(meaning_rows: list[dict], neighbor_rows: list[dict], reference_family: str, raw_family: str) -> tuple[list[dict], list[dict]]:
    reference = _family(meaning_rows, reference_family)
    raw = _family(meaning_rows, raw_family)
    neighbor = _neighbor(neighbor_rows, reference_family, raw_family)
    state = _development_state(reference, raw, neighbor)
    overview = [
        {
            "reference_family": reference_family,
            "raw_family": raw_family,
            "development_state": state,
            "reference_seen": bool(reference),
            "raw_seen": bool(raw),
            "reference_reife_state": str(reference.get("candidate_passive_reife_state", "") or ""),
            "raw_reife_state": str(raw.get("candidate_passive_reife_state", "") or ""),
            "reference_episode_count": _safe_int(reference.get("episode_count")),
            "raw_episode_count": _safe_int(raw.get("episode_count")),
            "reference_sources": str(reference.get("sources", "") or ""),
            "raw_sources": str(raw.get("sources", "") or ""),
            "neighbor_state": str(neighbor.get("neighbor_state", "") or ""),
            "meaning_similarity": neighbor.get("meaning_similarity", ""),
            "sense_similarity": neighbor.get("sense_similarity", ""),
            "mcm_similarity": neighbor.get("mcm_similarity", ""),
            "hearing_similarity": neighbor.get("hearing_similarity", ""),
            "temporal_similarity": neighbor.get("temporal_similarity", ""),
            "neuro_similarity": neighbor.get("neuro_similarity", ""),
            "reife_similarity": neighbor.get("reife_similarity", ""),
            "reading": _reading(reference_family, raw_family, state, neighbor),
            **BOUNDARY,
        }
    ]
    detail = []
    for label, row in [("reference", reference), ("raw_neighbor", raw)]:
        if not row:
            continue
        detail.append(
            {
                "role": label,
                "symbol_family": row.get("symbol_family", ""),
                "episode_count": row.get("episode_count", ""),
                "sources": row.get("sources", ""),
                "candidate_passive_reife_state": row.get("candidate_passive_reife_state", ""),
                "candidate_meaning_preservation_rate": row.get("candidate_meaning_preservation_rate", ""),
                "candidate_stable_recurrence_rate": row.get("candidate_stable_recurrence_rate", ""),
                "dominant_neuro_tone": row.get("dominant_neuro_tone", ""),
                "avg_sehen_form_stability": row.get("avg_sehen_form_stability", ""),
                "avg_hoeren_energy_shift": row.get("avg_hoeren_energy_shift", ""),
                "avg_fuehlen_mcm_coherence": row.get("avg_fuehlen_mcm_coherence", ""),
                "avg_observation_learning_pressure": row.get("avg_observation_learning_pressure", ""),
                **BOUNDARY,
            }
        )
    return overview, detail


def _reading(reference_family: str, raw_family: str, state: str, neighbor: dict) -> str:
    if state == "raw_neighbor_became_candidate":
        return f"{raw_family} hat eigene Reife ausgebildet und ist nicht nur Echo von {reference_family}."
    if state == "raw_neighbor_stable_echo":
        return f"{raw_family} ist eine stabile rohe Nachbarspur von {reference_family}; gleiche Inselnaehe, aber noch ohne eigene Reife."
    if state == "raw_neighbor_near_but_unmatured":
        return f"{raw_family} liegt nahe bei {reference_family}, ist aber noch nicht stabil genug als Echo."
    if state == "raw_neighbor_not_seen":
        return f"{raw_family} wurde in dieser Karte nicht gesehen."
    return f"{raw_family} ist von {reference_family} getrennt oder nur schwach verwandt."


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(overview: list[dict], detail: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    overview_path = output_dir / "passive_raw_neighbor_development_overview.csv"
    detail_path = output_dir / "passive_raw_neighbor_development_detail.csv"
    json_path = output_dir / "passive_raw_neighbor_development.json"
    md_path = output_dir / "README.md"
    _write_csv(overview_path, overview, ["reference_family", "raw_family"])
    _write_csv(detail_path, detail, ["role", "symbol_family"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_raw_neighbor_development.v1",
                "boundary": BOUNDARY,
                "overview": overview,
                "detail": detail,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Mini-DIO passive rohe Nachbarspur",
        "",
        "Ziel: pruefen, ob eine rohe Nachbarspur eigene Reife bekommt oder Echo bleibt.",
        "",
        "## Grenze",
        "- Nur Bericht.",
        "- Keine Runtime-Rueckfuehrung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Trainingsmemory.",
        "",
        "## Befund",
    ]
    if overview:
        row = overview[0]
        lines.append(f"- state: {row['development_state']}")
        lines.append(f"- {row['reading']}")
        lines.append(f"- meaning_similarity: {row.get('meaning_similarity', '')}")
        lines.append(f"- mcm_similarity: {row.get('mcm_similarity', '')}")
        lines.append(f"- reife_similarity: {row.get('reife_similarity', '')}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive raw neighbor development")
    parser.add_argument("--meaning-space", required=True, type=Path)
    parser.add_argument("--neighbors", required=True, type=Path)
    parser.add_argument("--reference-family", required=True)
    parser.add_argument("--raw-family", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    overview, detail = build_report(
        _read_csv(args.meaning_space),
        _read_csv(args.neighbors),
        args.reference_family,
        args.raw_family,
    )
    write_outputs(overview, detail, args.output_dir)
    print(
        json.dumps(
            {
                "overview_rows": len(overview),
                "detail_rows": len(detail),
                "output_dir": str(args.output_dir),
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
