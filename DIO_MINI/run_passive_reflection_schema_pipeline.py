"""Run the passive DIO_MINI reflection-schema pipeline.

The pipeline chains existing passive reports:

inner coherence transfer -> conflict trace -> inner awareness ->
reflection candidates -> candidate timeline -> reflection maturity ->
schema check -> optional schema stability comparison.

It is diagnosis only. It does not write memory and it does not influence action.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from DIO_MINI.report_passive_conflict_inner_awareness import build_rows as build_conflict_awareness_rows
from DIO_MINI.report_passive_conflict_inner_awareness import write_outputs as write_conflict_awareness_outputs
from DIO_MINI.report_passive_conflict_trace_lupe import build_rows as build_conflict_rows
from DIO_MINI.report_passive_conflict_trace_lupe import write_outputs as write_conflict_outputs
from DIO_MINI.report_passive_inner_coherence_transfer import build_rows as build_transfer_rows
from DIO_MINI.report_passive_inner_coherence_transfer import write_outputs as write_transfer_outputs
from DIO_MINI.report_passive_reflection_candidate_timeline import build_rows as build_candidate_timeline_rows
from DIO_MINI.report_passive_reflection_candidate_timeline import write_outputs as write_candidate_timeline_outputs
from DIO_MINI.report_passive_reflection_candidates import build_rows as build_candidate_rows
from DIO_MINI.report_passive_reflection_candidates import write_outputs as write_candidate_outputs
from DIO_MINI.report_passive_reflection_maturity import build_rows as build_maturity_rows
from DIO_MINI.report_passive_reflection_maturity import write_outputs as write_maturity_outputs
from DIO_MINI.report_passive_reflection_memory_schema_check import build_rows as build_schema_rows
from DIO_MINI.report_passive_reflection_memory_schema_check import write_outputs as write_schema_outputs
from DIO_MINI.report_passive_reflection_schema_stability import build_rows as build_stability_rows
from DIO_MINI.report_passive_reflection_schema_stability import write_outputs as write_stability_outputs


def _parse_input(raw: str, flag: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise SystemExit(f"{flag} must be label=csv_path, got: {raw}")
    label, path = raw.split("=", 1)
    label = label.strip()
    if not label:
        raise SystemExit(f"Empty label in {flag}: {raw}")
    return label, Path(path.strip())


def _read_csv(path: Path) -> list[dict]:
    import csv

    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def run_pipeline(
    *,
    label: str,
    coherence_inputs: list[tuple[str, Path]],
    protocol_inputs: list[tuple[str, Path]],
    stability_inputs: list[tuple[str, Path]],
    output_dir: Path,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    transfer_dir = output_dir / "01_inner_coherence_transfer"
    transfer_detail, transfer_world, transfer_summary = build_transfer_rows(coherence_inputs)
    write_transfer_outputs(transfer_detail, transfer_world, transfer_summary, transfer_dir)

    conflict_dir = output_dir / "02_conflict_trace_lupe"
    conflict_detail, conflict_summary = build_conflict_rows(transfer_detail)
    write_conflict_outputs(conflict_detail, conflict_summary, conflict_dir)

    awareness_dir = output_dir / "03_conflict_inner_awareness"
    awareness_family, awareness_detail = build_conflict_awareness_rows(conflict_summary, conflict_detail)
    write_conflict_awareness_outputs(awareness_family, awareness_detail, awareness_dir)

    candidates_dir = output_dir / "04_reflection_candidates"
    candidates, candidate_detail = build_candidate_rows(awareness_family, awareness_detail)
    write_candidate_outputs(candidates, candidate_detail, candidates_dir)

    timeline_dir = output_dir / "05_reflection_candidate_timeline"
    timeline_detail, timeline_summary = build_candidate_timeline_rows(
        {str(row.get("symbol_family", "") or ""): row for row in candidates if str(row.get("symbol_family", "") or "")},
        protocol_inputs,
    )
    write_candidate_timeline_outputs(timeline_detail, timeline_summary, timeline_dir)

    maturity_dir = output_dir / "06_reflection_maturity"
    maturity_rows = build_maturity_rows(timeline_summary)
    write_maturity_outputs(maturity_rows, maturity_dir)

    schema_dir = output_dir / "07_reflection_memory_schema_check"
    schema_detail, schema_summary = build_schema_rows(maturity_rows)
    write_schema_outputs(schema_detail, schema_summary, schema_dir)

    stability_dir = output_dir / "08_reflection_schema_stability"
    schema_csv = schema_dir / "dio_mini_passive_reflection_memory_schema_check.csv"
    stability_sources = list(stability_inputs) + [(label, schema_csv)]
    stability_detail, stability_summary = build_stability_rows(stability_sources)
    write_stability_outputs(stability_detail, stability_summary, stability_dir)

    summary = {
        "label": label,
        "coherence_inputs": [name for name, _path in coherence_inputs],
        "protocol_inputs": [name for name, _path in protocol_inputs],
        "stability_inputs": [name for name, _path in stability_sources],
        "rows": {
            "transfer_detail": len(transfer_detail),
            "transfer_summary": len(transfer_summary),
            "conflict_detail": len(conflict_detail),
            "conflict_summary": len(conflict_summary),
            "awareness_family": len(awareness_family),
            "awareness_detail": len(awareness_detail),
            "reflection_candidates": len(candidates),
            "candidate_timeline_detail": len(timeline_detail),
            "candidate_timeline_summary": len(timeline_summary),
            "reflection_maturity": len(maturity_rows),
            "schema_detail": len(schema_detail),
            "schema_summary": len(schema_summary),
            "stability_detail": len(stability_detail),
            "stability_summary": len(stability_summary),
        },
        "outputs": {
            "transfer": str(transfer_dir),
            "conflict": str(conflict_dir),
            "awareness": str(awareness_dir),
            "candidates": str(candidates_dir),
            "timeline": str(timeline_dir),
            "maturity": str(maturity_dir),
            "schema": str(schema_dir),
            "stability": str(stability_dir),
        },
        "boundary": {
            "writes_memory": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
        },
    }
    (output_dir / "dio_mini_passive_reflection_schema_pipeline_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Reflection Schema Pipeline",
        "",
        f"- label: {label}",
        f"- coherence_inputs: {', '.join(summary['coherence_inputs']) or '-'}",
        f"- protocol_inputs: {', '.join(summary['protocol_inputs']) or '-'}",
        f"- stability_inputs: {', '.join(summary['stability_inputs']) or '-'}",
        "",
        "## Rows",
    ]
    for key, value in summary["rows"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Stability"])
    if not stability_summary:
        lines.append("- keine Stabilitaetsdaten")
    for row in stability_summary:
        lines.append(
            f"- {row.get('symbol_family', '-')}: {row.get('stability_state', '-')} "
            f"({row.get('source_labels', '-')})"
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    (output_dir / "dio_mini_passive_reflection_schema_pipeline_summary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run passive DIO_MINI reflection schema pipeline")
    parser.add_argument("--label", default="pipeline_current")
    parser.add_argument("--coherence", action="append", required=True, help="label=inner_coherence_detail_csv")
    parser.add_argument("--protocol", action="append", required=True, help="label=inner_state_protocol_csv")
    parser.add_argument("--stability-source", action="append", default=[], help="label=schema_check_csv")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    summary = run_pipeline(
        label=str(args.label or "pipeline_current"),
        coherence_inputs=[_parse_input(item, "--coherence") for item in args.coherence],
        protocol_inputs=[_parse_input(item, "--protocol") for item in args.protocol],
        stability_inputs=[_parse_input(item, "--stability-source") for item in args.stability_source],
        output_dir=Path(args.output_dir),
    )
    rows = summary["rows"]
    print(
        "pipeline_complete "
        f"label={summary['label']} "
        f"schema_rows={rows['schema_detail']} "
        f"stability_rows={rows['stability_summary']}"
    )


if __name__ == "__main__":
    main()
