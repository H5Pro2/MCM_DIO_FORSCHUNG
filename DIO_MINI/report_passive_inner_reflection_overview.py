"""Build a passive Mini-DIO inner reflection overview.

This report reads transfer-note stability and translates it into a compact
reflection map:

- stable quiet recognition
- stable carried recognition
- stable open transfer
- stable non-action maturity warning
- single variant burden

It is intentionally passive. It writes no training memory and must not be used
as an action gate.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        value = float(value or 0.0)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return value


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _reflection_state(kind: str, source_count: int, note_count: int) -> str:
    repeated = source_count >= 2
    if kind == "note_similar_and_carried":
        return "inner_reflection_carried_recognition_repeats" if repeated else "inner_reflection_carried_local"
    if kind == "note_similar_and_quiet":
        return "inner_reflection_quiet_recognition_repeats" if repeated else "inner_reflection_quiet_local"
    if kind == "note_similar_family_carried_but_observed":
        return "inner_reflection_carried_potential_observed_repeats" if repeated else "inner_reflection_carried_potential_local"
    if kind == "note_similar_but_not_action_mature":
        return "inner_reflection_near_but_not_action_mature_repeats" if repeated else "inner_reflection_near_but_not_action_mature_local"
    if kind == "note_similar_and_burdened":
        return "inner_reflection_burden_trace_repeats" if repeated else "inner_reflection_burden_trace_local"
    if kind == "note_transfer_open":
        return "inner_reflection_open_transfer_repeats" if repeated else "inner_reflection_open_transfer_local"
    return "inner_reflection_unclassified_repeat" if repeated else "inner_reflection_unclassified_local"


def _reflection_note(row: dict, state: str) -> str:
    kind = str(row.get("learning_note_kind", "") or "-")
    sources = str(row.get("sources", "") or "-")
    note_count = _safe_int(row.get("note_count"))
    avg_reife = _safe_float(row.get("avg_transfer_reife"))
    avg_similarity = _safe_float(row.get("avg_similarity"))
    if state == "inner_reflection_carried_recognition_repeats":
        return (
            f"{kind} kehrt ueber {sources} wieder: getragenes Erkennen bleibt ueber Varianten sichtbar "
            f"(notes={note_count}, reife={avg_reife:.6f}, naehe={avg_similarity:.6f})."
        )
    if state == "inner_reflection_quiet_recognition_repeats":
        return (
            f"{kind} kehrt ueber {sources} wieder: aehnliche Lage bleibt ruhig beobachtbar "
            f"(notes={note_count}, reife={avg_reife:.6f})."
        )
    if state == "inner_reflection_carried_potential_observed_repeats":
        return (
            f"{kind} kehrt ueber {sources} wieder: Potenzial ist da, aber bleibt beobachtend statt motorisch."
        )
    if state == "inner_reflection_near_but_not_action_mature_repeats":
        return (
            f"{kind} kehrt ueber {sources} wieder: Naehe reicht nicht fuer Handlungsreife. "
            "Das ist ein wichtiger Distanzmarker."
        )
    if state == "inner_reflection_open_transfer_repeats":
        return f"{kind} bleibt ueber {sources} offen: Verwandtschaft wird gesehen, aber noch nicht verdichtet."
    if state == "inner_reflection_burden_trace_local":
        return f"{kind} ist bisher lokal: belastende Spur sichtbar, aber noch nicht variantenstabil."
    return f"{kind}: passive Reflexionslage {state}."


def build_rows(stability_by_kind_csv: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    summary: dict[str, dict] = {}
    for row in _read_csv(stability_by_kind_csv):
        kind = str(row.get("learning_note_kind", "") or "note_unknown")
        source_count = _safe_int(row.get("source_count"))
        note_count = _safe_int(row.get("note_count"))
        state = _reflection_state(kind, source_count, note_count)
        item = {
            "learning_note_kind": kind,
            "inner_reflection_state": state,
            "source_count": source_count,
            "note_count": note_count,
            "avg_transfer_reife": round(_safe_float(row.get("avg_transfer_reife")), 9),
            "avg_similarity": round(_safe_float(row.get("avg_similarity")), 9),
            "sources": str(row.get("sources", "") or ""),
            "pairs": str(row.get("pairs", "") or ""),
            "inner_reflection_note": "",
            "passive_only": 1,
        }
        item["inner_reflection_note"] = _reflection_note(item, state)
        detail.append(item)
        bucket = summary.setdefault(
            state,
            {
                "inner_reflection_state": state,
                "kind_count": 0,
                "note_count": 0,
                "source_count_max": 0,
                "avg_transfer_reife": 0.0,
                "avg_similarity": 0.0,
                "kinds": [],
            },
        )
        bucket["kind_count"] += 1
        bucket["note_count"] += note_count
        bucket["source_count_max"] = max(int(bucket["source_count_max"]), source_count)
        bucket["avg_transfer_reife"] += item["avg_transfer_reife"]
        bucket["avg_similarity"] += item["avg_similarity"]
        bucket["kinds"].append(kind)

    summary_rows: list[dict] = []
    for bucket in summary.values():
        count = max(1, int(bucket["kind_count"]))
        summary_rows.append(
            {
                "inner_reflection_state": bucket["inner_reflection_state"],
                "kind_count": int(bucket["kind_count"]),
                "note_count": int(bucket["note_count"]),
                "source_count_max": int(bucket["source_count_max"]),
                "avg_transfer_reife": round(float(bucket["avg_transfer_reife"]) / count, 9),
                "avg_similarity": round(float(bucket["avg_similarity"]) / count, 9),
                "kinds": ",".join(sorted(set(bucket["kinds"]))),
                "passive_only": 1,
            }
        )
    detail.sort(key=lambda item: (-int(item["source_count"]), -float(item["avg_transfer_reife"]), str(item["learning_note_kind"])))
    summary_rows.sort(key=lambda item: (-int(item["source_count_max"]), -int(item["note_count"]), str(item["inner_reflection_state"])))
    return detail, summary_rows


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, source: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_inner_reflection_overview.csv"
    summary_csv = output_dir / "dio_mini_passive_inner_reflection_overview_summary.csv"
    json_path = output_dir / "dio_mini_passive_inner_reflection_overview.json"
    md_path = output_dir / "dio_mini_passive_inner_reflection_overview.md"

    _write_csv(detail_csv, detail, ["learning_note_kind", "inner_reflection_state"])
    _write_csv(summary_csv, summary, ["inner_reflection_state", "kind_count", "note_count"])
    json_path.write_text(
        json.dumps(
            {
                "source": str(source),
                "detail": detail,
                "summary": summary,
                "boundary": {
                    "writes_training_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_hard_rule": False,
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Inner Reflection Overview", "", f"- source: {source}", ""]
    lines.append("## Zusammenfassung")
    if not summary:
        lines.append("- keine Reflexionszustaende")
    for row in summary:
        lines.append(
            f"- {row['inner_reflection_state']}: kinds={row['kind_count']} notes={row['note_count']} "
            f"sources_max={row['source_count_max']} avg_transfer_reife={row['avg_transfer_reife']} "
            f"kinds_list={row['kinds']}"
        )
    lines.extend(["", "## Innere Notizen"])
    for row in detail:
        lines.append(f"- {row['learning_note_kind']} -> {row['inner_reflection_state']}")
        lines.append(f"  {row['inner_reflection_note']}")
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Reflexionsuebersicht",
            "- kein Trainingsmemory",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO inner reflection overview")
    parser.add_argument("--stability-by-kind-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    source = Path(args.stability_by_kind_csv)
    detail, summary = build_rows(source)
    write_outputs(detail, summary, Path(args.output_dir), source)
    print(f"passive_inner_reflection_overview_rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['inner_reflection_state']} kinds={row['kind_count']} "
            f"notes={row['note_count']} sources_max={row['source_count_max']}"
        )


if __name__ == "__main__":
    main()
