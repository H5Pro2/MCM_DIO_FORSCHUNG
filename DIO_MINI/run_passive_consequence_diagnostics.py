"""Run the passive Mini-DIO consequence diagnosis pipeline.

The pipeline chains the passive consequence reports:

trade events -> memory consequence effect -> consequence inner awareness ->
consequence inner state protocol -> multisensory inner map ->
multisensory stability -> multisensory maturation map ->
multisensory maturation timeline -> passive development diagnosis ->
passive development reflection -> passive inner-state map.

It is diagnosis only. It writes no memory and it must not influence action.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from DIO_MINI.report_memory_consequence_effect import build_rows as build_memory_effect_rows
from DIO_MINI.report_memory_consequence_effect import write_outputs as write_memory_effect_outputs
from DIO_MINI.report_multisensory_inner_map import build_rows as build_multisensory_rows
from DIO_MINI.report_multisensory_inner_map import write_outputs as write_multisensory_outputs
from DIO_MINI.report_multisensory_maturation_map import build_rows as build_maturation_rows
from DIO_MINI.report_multisensory_maturation_map import write_outputs as write_maturation_outputs
from DIO_MINI.report_multisensory_maturation_timeline import build_rows as build_timeline_rows
from DIO_MINI.report_multisensory_maturation_timeline import write_outputs as write_timeline_outputs
from DIO_MINI.report_multisensory_stability import build_rows as build_stability_rows
from DIO_MINI.report_multisensory_stability import write_outputs as write_stability_outputs
from DIO_MINI.report_passive_consequence_inner_awareness import build_rows as build_inner_awareness_rows
from DIO_MINI.report_passive_consequence_inner_awareness import write_outputs as write_inner_awareness_outputs
from DIO_MINI.report_passive_consequence_inner_state_protocol import build_rows as build_inner_protocol_rows
from DIO_MINI.report_passive_consequence_inner_state_protocol import write_outputs as write_inner_protocol_outputs
from DIO_MINI.report_passive_development_diagnosis import build_rows as build_development_rows
from DIO_MINI.report_passive_development_diagnosis import write_outputs as write_development_outputs
from DIO_MINI.report_passive_development_reflection import build_rows as build_reflection_rows
from DIO_MINI.report_passive_development_reflection import write_outputs as write_reflection_outputs
from DIO_MINI.report_passive_inner_state_landkarte import build_rows as build_landkarte_rows
from DIO_MINI.report_passive_inner_state_landkarte import write_outputs as write_landkarte_outputs
from DIO_MINI.report_trade_events import build_rows as build_trade_event_rows
from DIO_MINI.report_trade_events import write_outputs as write_trade_event_outputs


def _write_pipeline_summary(
    *,
    output_dir: Path,
    label: str,
    memory_path: Path,
    debug_root: Path,
    rows: dict[str, int],
    outputs: dict[str, str],
    development_summary: list[dict],
) -> None:
    summary = {
        "label": label,
        "memory_path": str(memory_path),
        "debug_root": str(debug_root),
        "rows": rows,
        "outputs": outputs,
        "development_summary": development_summary,
        "boundary": {
            "writes_memory": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
        },
    }
    (output_dir / "dio_mini_passive_consequence_diagnostics_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Consequence Diagnostics",
        "",
        f"- label: {label}",
        f"- memory: {memory_path}",
        f"- debug_root: {debug_root}",
        "",
        "## Umfang",
    ]
    for key, value in rows.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Entwicklungsdiagnose"])
    if not development_summary:
        lines.append("- keine Entwicklungsdaten")
    else:
        for row in development_summary:
            lines.append(
                f"- {row.get('development_state', '-')}: "
                f"families={row.get('family_count', 0)} "
                f"rows={row.get('row_count', 0)} "
                f"reward_sum={row.get('reward_sum', 0.0)} "
                f"families_list={row.get('families', '-') or '-'}"
            )
    lines.extend(["", "## Ausgaben"])
    for key, value in outputs.items():
        lines.append(f"- {key}: {value}")
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
    (output_dir / "dio_mini_passive_consequence_diagnostics_summary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def run_pipeline(*, label: str, memory_path: Path, debug_root: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    trade_events_dir = output_dir / "01_trade_events"
    trade_detail, trade_summary = build_trade_event_rows(debug_root)
    write_trade_event_outputs(trade_detail, trade_summary, trade_events_dir)
    trade_summary_csv = trade_events_dir / "dio_mini_trade_events_summary.csv"

    memory_effect_dir = output_dir / "02_memory_consequence_effect"
    memory_effect_rows = build_memory_effect_rows(memory_path, trade_summary_csv)
    write_memory_effect_outputs(memory_effect_rows, memory_effect_dir, memory_path, trade_summary_csv)
    memory_effect_csv = memory_effect_dir / "dio_mini_memory_consequence_effect.csv"

    inner_awareness_dir = output_dir / "03_consequence_inner_awareness"
    inner_awareness_detail, inner_awareness_summary = build_inner_awareness_rows(memory_effect_csv)
    write_inner_awareness_outputs(inner_awareness_detail, inner_awareness_summary, inner_awareness_dir, memory_effect_csv)
    inner_awareness_csv = inner_awareness_dir / "dio_mini_passive_consequence_inner_awareness.csv"

    inner_protocol_dir = output_dir / "04_consequence_inner_state_protocol"
    inner_protocol_detail, inner_protocol_summary = build_inner_protocol_rows(debug_root, inner_awareness_csv)
    write_inner_protocol_outputs(inner_protocol_detail, inner_protocol_summary, inner_protocol_dir, inner_awareness_csv)
    inner_protocol_csv = inner_protocol_dir / "dio_mini_passive_consequence_inner_state_protocol.csv"

    multisensory_dir = output_dir / "05_multisensory_inner_map"
    multisensory_detail, multisensory_summary = build_multisensory_rows(inner_protocol_csv)
    write_multisensory_outputs(multisensory_detail, multisensory_summary, multisensory_dir, inner_protocol_csv)
    multisensory_csv = multisensory_dir / "dio_mini_multisensory_inner_map.csv"

    stability_dir = output_dir / "06_multisensory_stability"
    stability_detail, stability_summary = build_stability_rows(multisensory_csv)
    write_stability_outputs(stability_detail, stability_summary, stability_dir, multisensory_csv)
    stability_csv = stability_dir / "dio_mini_multisensory_stability.csv"

    maturation_dir = output_dir / "07_multisensory_maturation_map"
    maturation_detail, maturation_summary = build_maturation_rows(stability_csv)
    write_maturation_outputs(maturation_detail, maturation_summary, maturation_dir, stability_csv)
    maturation_csv = maturation_dir / "dio_mini_multisensory_maturation_map.csv"

    timeline_dir = output_dir / "08_multisensory_maturation_timeline"
    timeline_detail, timeline_summary = build_timeline_rows(multisensory_csv, maturation_csv)
    write_timeline_outputs(timeline_detail, timeline_summary, timeline_dir, multisensory_csv, maturation_csv)
    timeline_csv = timeline_dir / "dio_mini_multisensory_maturation_timeline.csv"
    timeline_summary_csv = timeline_dir / "dio_mini_multisensory_maturation_timeline_summary.csv"

    development_dir = output_dir / "09_passive_development_diagnosis"
    development_detail, development_summary = build_development_rows(timeline_summary_csv)
    write_development_outputs(development_detail, development_summary, development_dir, timeline_summary_csv)
    development_csv = development_dir / "dio_mini_passive_development_diagnosis.csv"

    reflection_dir = output_dir / "10_passive_development_reflection"
    reflection_detail, reflection_summary = build_reflection_rows(development_csv)
    write_reflection_outputs(reflection_detail, reflection_summary, reflection_dir, development_csv)
    reflection_csv = reflection_dir / "dio_mini_passive_development_reflection.csv"

    landkarte_dir = output_dir / "11_passive_inner_state_landkarte"
    landkarte_detail, landkarte_summary = build_landkarte_rows(timeline_csv, reflection_csv)
    write_landkarte_outputs(landkarte_detail, landkarte_summary, landkarte_dir, timeline_csv, reflection_csv)

    rows = {
        "trade_events_detail": len(trade_detail),
        "trade_events_summary": len(trade_summary),
        "memory_effect": len(memory_effect_rows),
        "inner_awareness_detail": len(inner_awareness_detail),
        "inner_awareness_summary": len(inner_awareness_summary),
        "inner_protocol_detail": len(inner_protocol_detail),
        "inner_protocol_summary": len(inner_protocol_summary),
        "multisensory_detail": len(multisensory_detail),
        "multisensory_summary": len(multisensory_summary),
        "stability_detail": len(stability_detail),
        "stability_summary": len(stability_summary),
        "maturation_detail": len(maturation_detail),
        "maturation_summary": len(maturation_summary),
        "timeline_detail": len(timeline_detail),
        "timeline_summary": len(timeline_summary),
        "development_detail": len(development_detail),
        "development_summary": len(development_summary),
        "development_reflection_detail": len(reflection_detail),
        "development_reflection_summary": len(reflection_summary),
        "inner_state_landkarte_detail": len(landkarte_detail),
        "inner_state_landkarte_summary": len(landkarte_summary),
    }
    outputs = {
        "trade_events": str(trade_events_dir),
        "memory_consequence_effect": str(memory_effect_dir),
        "consequence_inner_awareness": str(inner_awareness_dir),
        "consequence_inner_state_protocol": str(inner_protocol_dir),
        "multisensory_inner_map": str(multisensory_dir),
        "multisensory_stability": str(stability_dir),
        "multisensory_maturation_map": str(maturation_dir),
        "multisensory_maturation_timeline": str(timeline_dir),
        "passive_development_diagnosis": str(development_dir),
        "passive_development_reflection": str(reflection_dir),
        "passive_inner_state_landkarte": str(landkarte_dir),
    }
    _write_pipeline_summary(
        output_dir=output_dir,
        label=label,
        memory_path=memory_path,
        debug_root=debug_root,
        rows=rows,
        outputs=outputs,
        development_summary=development_summary,
    )
    return {
        "label": label,
        "rows": rows,
        "outputs": outputs,
        "development_summary": development_summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run passive Mini-DIO consequence diagnosis pipeline")
    parser.add_argument("--label", default="consequence_current")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    summary = run_pipeline(
        label=str(args.label or "consequence_current"),
        memory_path=Path(args.memory),
        debug_root=Path(args.debug_root),
        output_dir=Path(args.output_dir),
    )
    rows = summary["rows"]
    print(
        "passive_consequence_pipeline_complete "
        f"label={summary['label']} "
        f"events={rows['trade_events_detail']} "
        f"development={rows['development_detail']}"
    )
    for row in summary["development_summary"]:
        print(
            f"{row['development_state']} families={row['family_count']} "
            f"rows={row['row_count']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
