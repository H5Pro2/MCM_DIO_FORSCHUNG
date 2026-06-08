"""Compare passive reflection-memory schema checks across runs/world groups.

The report is passive. It reads one or more schema-check CSV files and shows
whether a family keeps the same schema, maturity, contact path, and inner path
across inputs. It does not write reflection memory.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _parse_input(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise SystemExit(f"--schema-check must be label=csv_path, got: {raw}")
    label, path = raw.split("=", 1)
    label = label.strip()
    if not label:
        raise SystemExit(f"Empty label in --schema-check: {raw}")
    return label, Path(path.strip())


def _unique_values(rows: list[dict], field: str) -> list[str]:
    values = []
    for row in rows:
        value = str(row.get(field, "") or "")
        if value and value not in values:
            values.append(value)
    return values


def _stability_state(rows: list[dict]) -> str:
    if len(rows) <= 1:
        return "single_source_baseline"
    schema_states = _unique_values(rows, "schema_state")
    maturities = _unique_values(rows, "reflection_maturity")
    contact_paths = _unique_values(rows, "real_contact_path")
    inner_paths = _unique_values(rows, "inner_state_path")
    if len(schema_states) > 1:
        return "schema_state_changed"
    if len(maturities) > 1:
        return "reflection_maturity_changed"
    if len(contact_paths) > 1:
        return "real_contact_path_changed"
    if len(inner_paths) > 1:
        return "inner_state_path_changed"
    return "stable_passive_schema"


def _stability_note(family: str, state: str, rows: list[dict]) -> str:
    labels = ",".join(_unique_values(rows, "source_label")) or "-"
    if state == "single_source_baseline":
        return f"{family}: Nur eine passive Quelle vorhanden; dient als Baseline ({labels})."
    if state == "stable_passive_schema":
        return f"{family}: Passive Reflexionsschema-Lesung bleibt ueber Quellen stabil ({labels})."
    if state == "schema_state_changed":
        return f"{family}: Schema-Faehigkeit veraendert sich ueber Quellen ({labels})."
    if state == "reflection_maturity_changed":
        return f"{family}: Passive Reflexionsreife veraendert sich ueber Quellen ({labels})."
    if state == "real_contact_path_changed":
        return f"{family}: Reale Kontaktverdichtung veraendert sich ueber Quellen ({labels})."
    if state == "inner_state_path_changed":
        return f"{family}: Innenzustandsverdichtung veraendert sich ueber Quellen ({labels})."
    return f"{family}: Passive Schema-Stabilitaet offen ({labels})."


def build_rows(inputs: list[tuple[str, Path]]) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    by_family: dict[str, list[dict]] = defaultdict(list)

    for label, path in inputs:
        for row in _read_csv(path):
            family = str(row.get("symbol_family", "") or "")
            if not family:
                continue
            item = {
                "source_label": label,
                "source_file": str(path),
                "symbol_family": family,
                "schema_state": str(row.get("schema_state", "") or ""),
                "reflection_maturity": str(row.get("reflection_maturity", "") or ""),
                "real_contact_path": str(row.get("real_contact_path", "") or ""),
                "inner_state_path": str(row.get("inner_state_path", "") or ""),
                "worlds": str(row.get("worlds", "") or ""),
                "reward_sum": str(row.get("reward_sum", "") or ""),
                "best_reward_sum": str(row.get("best_reward_sum", "") or ""),
                "writes_memory": str(row.get("writes_memory", "") or "0"),
                "passive_only": 1,
            }
            detail.append(item)
            by_family[family].append(item)

    summary: list[dict] = []
    for family, rows in sorted(by_family.items()):
        state = _stability_state(rows)
        summary.append(
            {
                "symbol_family": family,
                "stability_state": state,
                "source_count": len(_unique_values(rows, "source_label")),
                "source_labels": ",".join(_unique_values(rows, "source_label")),
                "schema_states": " | ".join(_unique_values(rows, "schema_state")),
                "reflection_maturities": " | ".join(_unique_values(rows, "reflection_maturity")),
                "real_contact_paths": " | ".join(_unique_values(rows, "real_contact_path")),
                "inner_state_paths": " | ".join(_unique_values(rows, "inner_state_path")),
                "writes_memory_values": " | ".join(_unique_values(rows, "writes_memory")),
                "stability_note": _stability_note(family, state, rows),
                "passive_only": 1,
            }
        )

    summary.sort(
        key=lambda row: (
            str(row.get("stability_state", "")) != "stable_passive_schema",
            str(row.get("stability_state", "")) != "single_source_baseline",
            str(row.get("symbol_family", "")),
        )
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_reflection_schema_stability_detail.csv"
    summary_path = output_dir / "dio_mini_passive_reflection_schema_stability.csv"
    json_path = output_dir / "dio_mini_passive_reflection_schema_stability.json"
    md_path = output_dir / "dio_mini_passive_reflection_schema_stability.md"

    detail_fields = list(detail[0].keys()) if detail else ["source_label", "symbol_family"]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else ["symbol_family", "stability_state"]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Reflection Schema Stability", ""]
    if not summary:
        lines.append("Keine Schema-Stabilitaetsdaten gefunden.")
    for row in summary:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- stability_state: {row['stability_state']}",
                f"- source_labels: {row['source_labels'] or '-'}",
                f"- schema_states: {row['schema_states'] or '-'}",
                f"- reflection_maturities: {row['reflection_maturities'] or '-'}",
                f"- real_contact_paths: {row['real_contact_paths'] or '-'}",
                f"- inner_state_paths: {row['inner_state_paths'] or '-'}",
                f"- writes_memory_values: {row['writes_memory_values'] or '-'}",
                f"- note: {row['stability_note']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Grenze",
            "- passiver Stabilitaetsvergleich",
            "- kein Reflexionsspeicher-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive reflection schema checks")
    parser.add_argument("--schema-check", action="append", required=True, help="label=schema_check_csv")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, summary = build_rows([_parse_input(item) for item in args.schema_check])
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"schema_stability_rows={len(summary)} detail_rows={len(detail)}")
    for row in summary:
        print(f"{row['symbol_family']} {row['stability_state']} sources={row['source_labels']}")


if __name__ == "__main__":
    main()
