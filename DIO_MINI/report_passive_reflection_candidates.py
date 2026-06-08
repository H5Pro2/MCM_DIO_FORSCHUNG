"""Build passive reflection candidates from DIO_MINI conflict awareness.

Reflection candidates are not rules. They are readable markers for traces that
may deserve later reflection because conflict, observation, and carried contact
appeared in the same family history.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _candidate_kind(state: str) -> str:
    if state == "conflict_reorganized_to_carried":
        return "reflection_candidate_reorganized_trace"
    if state == "conflict_to_observation":
        return "reflection_candidate_cautious_trace"
    if state == "mixed_conflict_with_carried_trace":
        return "reflection_candidate_mixed_trace"
    return "reflection_candidate_open_trace"


def _reflection_question(row: dict) -> str:
    family = str(row.get("symbol_family", "") or "-")
    state = str(row.get("passive_conflict_state", "") or "")
    if state == "conflict_reorganized_to_carried":
        return (
            f"{family}: Was hat sich zwischen Konflikt und spaeterem Tragen geaendert?"
        )
    if state == "conflict_to_observation":
        return (
            f"{family}: Warum bleibt diese Spur nach Konflikt eher Beobachtung als getragener Kontakt?"
        )
    if state == "mixed_conflict_with_carried_trace":
        return f"{family}: Welche Anteile tragen, welche Anteile bleiben Konflikt?"
    return f"{family}: Welche reale Erfahrung fehlt, um diese Spur besser zu lesen?"


def _reflection_note(row: dict) -> str:
    state = str(row.get("passive_conflict_state", "") or "")
    conflict = _safe_float(row.get("conflict_reward_sum"))
    positive = _safe_float(row.get("positive_reward_sum"))
    observed = _safe_float(row.get("observed_best_reward_sum"))
    if state == "conflict_reorganized_to_carried":
        return (
            "Konflikt und spaeteres Tragen liegen in derselben Familie. "
            f"Das spricht passiv fuer Reorganisation: conflict={conflict:.6f}, carried={positive:.6f}."
        )
    if state == "conflict_to_observation":
        return (
            "Konflikt blieb eher vorsichtig/beobachtend. "
            f"Das spricht passiv fuer Schutzdistanz: conflict={conflict:.6f}, observed_best={observed:.6f}."
        )
    return "Offene Konfliktspur ohne aktive Bedeutung."


def build_rows(family_rows: list[dict], detail_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    details_by_family: dict[str, list[dict]] = defaultdict(list)
    for row in detail_rows:
        family = str(row.get("symbol_family", "") or "")
        if family:
            details_by_family[family].append(row)

    detail_out: list[dict] = []
    summary_out: list[dict] = []
    for row in family_rows:
        family = str(row.get("symbol_family", "") or "")
        if not family:
            continue
        kind = _candidate_kind(str(row.get("passive_conflict_state", "") or ""))
        contacts = details_by_family.get(family, [])
        conflict_contacts = [item for item in contacts if str(item.get("trace_role", "") or "") == "conflict"]
        observed_contacts = [item for item in contacts if str(item.get("trace_role", "") or "") == "observed_potential"]
        carried_contacts = [item for item in contacts if str(item.get("trace_role", "") or "") == "carried_positive"]

        summary_item = {
            "symbol_family": family,
            "reflection_candidate_kind": kind,
            "passive_conflict_state": str(row.get("passive_conflict_state", "") or ""),
            "conflict_contacts": len(conflict_contacts),
            "observed_contacts": len(observed_contacts),
            "carried_contacts": len(carried_contacts),
            "conflict_reward_sum": round(_safe_float(row.get("conflict_reward_sum")), 6),
            "positive_reward_sum": round(_safe_float(row.get("positive_reward_sum")), 6),
            "observed_best_reward_sum": round(_safe_float(row.get("observed_best_reward_sum")), 6),
            "reflection_question": _reflection_question(row),
            "reflection_note": _reflection_note(row),
            "source_sentence": str(row.get("inner_conflict_sentence", "") or ""),
            "passive_only": 1,
        }
        summary_out.append(summary_item)

        for item in contacts:
            detail_out.append(
                {
                    "symbol_family": family,
                    "world": str(item.get("world", "") or ""),
                    "reflection_candidate_kind": kind,
                    "trace_role": str(item.get("trace_role", "") or ""),
                    "inner_state": str(item.get("inner_state", "") or ""),
                    "contact_quality": str(item.get("contact_quality", "") or ""),
                    "reward_sum": round(_safe_float(item.get("reward_sum")), 6),
                    "best_reward_sum": round(_safe_float(item.get("best_reward_sum")), 6),
                    "world_inner_sentence": str(item.get("world_inner_sentence", "") or ""),
                    "passive_only": 1,
                }
            )

    summary_out.sort(
        key=lambda item: (
            str(item.get("reflection_candidate_kind", "")),
            str(item.get("symbol_family", "")),
        )
    )
    return summary_out, detail_out


def write_outputs(summary_rows: list[dict], detail_rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "dio_mini_passive_reflection_candidates.csv"
    detail_path = output_dir / "dio_mini_passive_reflection_candidates_detail.csv"
    json_path = output_dir / "dio_mini_passive_reflection_candidates.json"
    md_path = output_dir / "dio_mini_passive_reflection_candidates.md"

    summary_fields = list(summary_rows[0].keys()) if summary_rows else ["symbol_family", "reflection_candidate_kind"]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary_rows)

    detail_fields = list(detail_rows[0].keys()) if detail_rows else ["symbol_family", "world"]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail_rows)

    json_path.write_text(
        json.dumps({"summary": summary_rows, "detail": detail_rows}, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Reflection Candidates", ""]
    if not summary_rows:
        lines.append("Keine passiven Reflexionskandidaten gefunden.")
    for row in summary_rows:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- kind: {row['reflection_candidate_kind']}",
                f"- conflict_contacts: {row['conflict_contacts']}",
                f"- observed_contacts: {row['observed_contacts']}",
                f"- carried_contacts: {row['carried_contacts']}",
                f"- question: {row['reflection_question']}",
                f"- note: {row['reflection_note']}",
                f"- source: {row['source_sentence']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Grenze",
            "- passiver Reflexionskandidat",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive reflection candidates from conflict awareness")
    parser.add_argument("--awareness-family", required=True)
    parser.add_argument("--awareness-detail", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    summary_rows, detail_rows = build_rows(
        _read_csv(Path(args.awareness_family)),
        _read_csv(Path(args.awareness_detail)),
    )
    write_outputs(summary_rows, detail_rows, Path(args.output_dir))
    print(f"reflection_candidate_rows={len(summary_rows)} detail_rows={len(detail_rows)}")
    for row in summary_rows:
        print(f"{row['symbol_family']} {row['reflection_candidate_kind']} {row['reflection_question']}")


if __name__ == "__main__":
    main()
