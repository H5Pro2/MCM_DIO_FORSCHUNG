"""Passive inner-awareness sentences for DIO_MINI conflict traces.

The report translates conflict trace rows into readable inner-state statements.
It keeps a strict boundary: no memory write, no action influence, no gate.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _family_sentence(row: dict) -> str:
    family = str(row.get("symbol_family", "") or "-")
    state = str(row.get("passive_conflict_state", "") or "-")
    conflict = _safe_float(row.get("conflict_reward_sum"))
    positive = _safe_float(row.get("positive_reward_sum"))
    observed = _safe_float(row.get("observed_best_reward_sum"))
    if state == "conflict_reorganized_to_carried":
        return (
            f"{family}: Diese Familie hatte Konflikt, wurde spaeter aber getragen; "
            f"Konflikt={conflict:.6f}, getragen={positive:.6f}."
        )
    if state == "conflict_to_observation":
        return (
            f"{family}: Diese Familie blieb nach Konflikt vorsichtig/beobachtend; "
            f"Konflikt={conflict:.6f}, beobachtetes Potenzial={observed:.6f}."
        )
    if state == "mixed_conflict_with_carried_trace":
        return (
            f"{family}: Diese Familie bleibt gemischt; Konflikt und getragene Spur existieren parallel."
        )
    return f"{family}: Diese Familie hat eine offene Konfliktspur."


def _world_sentence(row: dict) -> str:
    family = str(row.get("symbol_family", "") or "-")
    world = str(row.get("world", "") or "-")
    inner = str(row.get("inner_state", "") or "-")
    role = str(row.get("trace_role", "") or "-")
    contact = str(row.get("contact_quality", "") or "-")
    reward = _safe_float(row.get("reward_sum"))
    if role == "conflict":
        return (
            f"{world}: {family} fuehlt sich als {inner} an, hatte aber realen Konflikt "
            f"({contact}, reward={reward:.6f})."
        )
    if role == "carried_positive":
        return (
            f"{world}: {family} fuehlt sich als {inner} an und wurde real getragen "
            f"({contact}, reward={reward:.6f})."
        )
    if role == "observed_potential":
        best = _safe_float(row.get("best_reward_sum"))
        return (
            f"{world}: {family} bleibt in {inner} beobachtet; Potenzial wurde gesehen "
            f"({contact}, best={best:.6f}), aber nicht als reale Handlung fixiert."
        )
    return f"{world}: {family} bleibt passiv lesbar ({inner}/{contact})."


def build_rows(summary_rows: list[dict], detail_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    summary_by_family = {
        str(row.get("symbol_family", "") or ""): row
        for row in summary_rows
        if str(row.get("symbol_family", "") or "")
    }

    family_output: list[dict] = []
    for family in sorted(summary_by_family):
        source = summary_by_family[family]
        family_output.append(
            {
                "symbol_family": family,
                "passive_conflict_state": str(source.get("passive_conflict_state", "") or ""),
                "conflict_reward_sum": round(_safe_float(source.get("conflict_reward_sum")), 6),
                "positive_reward_sum": round(_safe_float(source.get("positive_reward_sum")), 6),
                "observed_best_reward_sum": round(_safe_float(source.get("observed_best_reward_sum")), 6),
                "inner_conflict_sentence": _family_sentence(source),
                "world_path": str(source.get("world_path", "") or ""),
                "passive_only": 1,
            }
        )

    detail_output: list[dict] = []
    for source in detail_rows:
        family = str(source.get("symbol_family", "") or "")
        if family not in summary_by_family:
            continue
        detail_output.append(
            {
                "symbol_family": family,
                "world": str(source.get("world", "") or ""),
                "inner_state": str(source.get("inner_state", "") or ""),
                "contact_quality": str(source.get("contact_quality", "") or ""),
                "trace_role": str(source.get("trace_role", "") or ""),
                "reward_sum": round(_safe_float(source.get("reward_sum")), 6),
                "best_reward_sum": round(_safe_float(source.get("best_reward_sum")), 6),
                "world_inner_sentence": _world_sentence(source),
                "passive_conflict_state": str(source.get("passive_conflict_state", "") or ""),
                "passive_only": 1,
            }
        )
    return family_output, detail_output


def write_outputs(family_rows: list[dict], detail_rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    family_path = output_dir / "dio_mini_passive_conflict_inner_awareness_family.csv"
    detail_path = output_dir / "dio_mini_passive_conflict_inner_awareness_detail.csv"
    json_path = output_dir / "dio_mini_passive_conflict_inner_awareness.json"
    md_path = output_dir / "dio_mini_passive_conflict_inner_awareness.md"

    family_fields = list(family_rows[0].keys()) if family_rows else ["symbol_family", "inner_conflict_sentence"]
    with family_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=family_fields)
        writer.writeheader()
        writer.writerows(family_rows)

    detail_fields = list(detail_rows[0].keys()) if detail_rows else ["symbol_family", "world_inner_sentence"]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail_rows)

    json_path.write_text(
        json.dumps({"family": family_rows, "detail": detail_rows}, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Conflict Inner Awareness", ""]
    if not family_rows:
        lines.append("Keine passiven Konflikt-Innensaetze gefunden.")
    for row in family_rows:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- state: {row['passive_conflict_state']}",
                f"- sentence: {row['inner_conflict_sentence']}",
                f"- world_path: {row['world_path']}",
                "",
            ]
        )
        for item in [item for item in detail_rows if item["symbol_family"] == row["symbol_family"]]:
            lines.append(f"  - {item['world_inner_sentence']}")
        lines.append("")
    lines.extend(
        [
            "## Grenze",
            "- passiver Leser",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive conflict inner-awareness sentences")
    parser.add_argument("--conflict-summary", required=True)
    parser.add_argument("--conflict-detail", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    family_rows, detail_rows = build_rows(_read_csv(Path(args.conflict_summary)), _read_csv(Path(args.conflict_detail)))
    write_outputs(family_rows, detail_rows, Path(args.output_dir))
    print(f"family_rows={len(family_rows)} detail_rows={len(detail_rows)}")
    for row in family_rows:
        print(row["inner_conflict_sentence"])


if __name__ == "__main__":
    main()
