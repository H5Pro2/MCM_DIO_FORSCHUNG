"""Run the passive DIO_MINI cortex diagnosis bundle.

The bundle creates:
- family file from semantic memory,
- reflection timeline from semantic memory,
- one passive cortex view per probe/debug world,
- cross-probe cortex comparison,
- passive family maturation path across probe/debug worlds.
- passive family maturation reflection from that path.
- passive inner-awareness map from maturation reflection.
- passive per-probe inner-state protocol from episodes.
- passive per-probe inner-state timeline from the protocol.
- passive per-probe inner-state stability from the timeline.
- passive per-probe inner coherence map from the timeline.

It is diagnosis only. It does not write memory and it is not imported by the
mini motor path.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from DIO_MINI.report_family_file import build_rows as build_family_rows
from DIO_MINI.report_family_file import write_outputs as write_family_outputs
from DIO_MINI.report_family_reflection_timeline import build_rows as build_timeline_rows
from DIO_MINI.report_family_reflection_timeline import write_outputs as write_timeline_outputs
from DIO_MINI.report_family_maturation_path import _read_roots as build_maturation_rows
from DIO_MINI.report_family_maturation_path import _write_outputs as write_maturation_outputs
from DIO_MINI.report_family_maturation_reflection import build_rows as build_maturation_reflection_rows
from DIO_MINI.report_family_maturation_reflection import write_outputs as write_maturation_reflection_outputs
from DIO_MINI.report_passive_inner_awareness import build_rows as build_inner_awareness_rows
from DIO_MINI.report_passive_inner_awareness import write_outputs as write_inner_awareness_outputs
from DIO_MINI.report_passive_inner_state_protocol import build_rows as build_inner_state_protocol_rows
from DIO_MINI.report_passive_inner_state_protocol import write_outputs as write_inner_state_protocol_outputs
from DIO_MINI.report_passive_inner_state_timeline import build_rows as build_inner_state_timeline_rows
from DIO_MINI.report_passive_inner_state_timeline import write_outputs as write_inner_state_timeline_outputs
from DIO_MINI.report_passive_inner_stability import build_rows as build_inner_stability_rows
from DIO_MINI.report_passive_inner_stability import write_outputs as write_inner_stability_outputs
from DIO_MINI.report_passive_inner_coherence_map import build_rows as build_inner_coherence_rows
from DIO_MINI.report_passive_inner_coherence_map import write_outputs as write_inner_coherence_outputs
from DIO_MINI.report_passive_cortex_comparison import build_rows as build_comparison_rows
from DIO_MINI.report_passive_cortex_comparison import write_outputs as write_comparison_outputs
from DIO_MINI.report_passive_cortex_view import build_rows as build_view_rows
from DIO_MINI.report_passive_cortex_view import write_outputs as write_view_outputs
from DIO_MINI.report_passive_recognition_boundary import build_rows as build_recognition_boundary_rows
from DIO_MINI.report_passive_recognition_boundary import write_outputs as write_recognition_boundary_outputs
from DIO_MINI.semantic_memory import SemanticMemory


def _write_bundle_summary(
    *,
    output_dir: Path,
    family_rows: int,
    timeline_rows: int,
    comparison_rows: int,
    maturation_rows: int,
    probes: list[str],
    view_dirs: dict[str, str],
    maturation_summary: list[dict],
    maturation_reflection_rows: list[dict],
    inner_awareness_rows: list[dict],
    inner_awareness_summary: list[dict],
    recognition_boundary_rows: int,
    recognition_boundary_summary_rows: int,
    inner_protocol_rows: int,
    inner_timeline_rows: int,
    inner_stability_rows: int,
    inner_coherence_rows: int,
) -> None:
    summary = {
        "family_rows": family_rows,
        "timeline_rows": timeline_rows,
        "comparison_rows": comparison_rows,
        "maturation_rows": maturation_rows,
        "maturation_reflection_rows": len(maturation_reflection_rows),
        "inner_awareness_rows": len(inner_awareness_rows),
        "inner_awareness_summary_rows": len(inner_awareness_summary),
        "recognition_boundary_rows": recognition_boundary_rows,
        "recognition_boundary_summary_rows": recognition_boundary_summary_rows,
        "inner_protocol_rows": inner_protocol_rows,
        "inner_timeline_rows": inner_timeline_rows,
        "inner_stability_rows": inner_stability_rows,
        "inner_coherence_rows": inner_coherence_rows,
        "probes": probes,
        "view_dirs": view_dirs,
        "outputs": {
            "family_file": "family_file",
            "family_reflection_timeline": "family_reflection_timeline",
            "passive_cortex_comparison": "passive_cortex_comparison",
            "family_maturation_path": "family_maturation_path" if maturation_rows else "",
            "family_maturation_reflection": "family_maturation_reflection" if maturation_reflection_rows else "",
            "passive_recognition_boundary": "passive_recognition_boundary" if recognition_boundary_rows else "",
            "passive_inner_awareness": "passive_inner_awareness" if inner_awareness_rows else "",
            "passive_inner_state_protocol": "passive_inner_state_<probe>" if inner_protocol_rows else "",
            "passive_inner_state_timeline": "passive_inner_timeline_<probe>" if inner_timeline_rows else "",
            "passive_inner_stability": "passive_inner_stability_<probe>" if inner_stability_rows else "",
            "passive_inner_coherence_map": "passive_inner_coherence_<probe>" if inner_coherence_rows else "",
        },
        "boundary": {
            "writes_memory": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
        },
    }
    (output_dir / "dio_mini_passive_cortex_diagnostics_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Cortex Diagnostics",
        "",
        "## Umfang",
        f"- family_rows: {family_rows}",
        f"- timeline_rows: {timeline_rows}",
        f"- comparison_rows: {comparison_rows}",
        f"- maturation_rows: {maturation_rows}",
        f"- maturation_reflection_rows: {len(maturation_reflection_rows)}",
        f"- inner_awareness_rows: {len(inner_awareness_rows)}",
        f"- recognition_boundary_rows: {recognition_boundary_rows}",
        f"- recognition_boundary_summary_rows: {recognition_boundary_summary_rows}",
        f"- inner_protocol_rows: {inner_protocol_rows}",
        f"- inner_timeline_rows: {inner_timeline_rows}",
        f"- inner_stability_rows: {inner_stability_rows}",
        f"- inner_coherence_rows: {inner_coherence_rows}",
        "",
        "## Proben",
    ]
    for probe in probes:
        lines.append(f"- {probe}: {view_dirs.get(probe, '-')}")
    lines.extend(
        [
            "",
            "## Reifeverlauf",
        ]
    )
    if not maturation_summary:
        lines.append("- nicht erzeugt, weil weniger als zwei Proben uebergeben wurden")
    else:
        for row in maturation_summary[:20]:
            lines.append(
                f"- {row.get('family', '-')}: {row.get('trend', '-')} | "
                f"{row.get('state_path', '-')} | reward_sum={row.get('reward_sum', 0.0)}"
            )
    lines.extend(
        [
            "",
            "## Reflexionshaltung",
        ]
    )
    if not maturation_reflection_rows:
        lines.append("- nicht erzeugt")
    else:
        for row in maturation_reflection_rows[:20]:
            lines.append(
                f"- {row.get('family', '-')}: {row.get('reflection_posture', '-')} | "
                f"{row.get('state_path', '-')} | reward_sum={row.get('reward_sum', 0.0)}"
            )
    lines.extend(["", "## Innenwahrnehmung"])
    if not inner_awareness_summary:
        lines.append("- nicht erzeugt")
    else:
        for row in inner_awareness_summary:
            lines.append(
                f"- {row.get('inner_state', '-')}: count={row.get('count', 0)} | "
                f"reward_sum={row.get('reward_sum', 0.0)} | families={row.get('families', '-') or '-'}"
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
    (output_dir / "dio_mini_passive_cortex_diagnostics_summary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def _parse_probe(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise SystemExit(f"--probe must be name=debug_root, got: {raw}")
    name, path = raw.split("=", 1)
    name = name.strip()
    if not name:
        raise SystemExit(f"Probe name is empty in: {raw}")
    return name, Path(path.strip())


def _probe_output_name(name: str) -> str:
    safe = "".join(char if char.isalnum() or char in ("-", "_") else "_" for char in name.strip())
    return safe or "probe"


def run_bundle(
    *,
    memory_path: Path,
    probes: list[tuple[str, Path]],
    output_dir: Path,
    selected_families: set[str] | None = None,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    memory = SemanticMemory(memory_path)
    memory.load()

    family_dir = output_dir / "family_file"
    family_rows = build_family_rows(memory, selected_families=selected_families)
    write_family_outputs(family_rows, family_dir)
    family_file = family_dir / "dio_mini_family_file.csv"

    timeline_dir = output_dir / "family_reflection_timeline"
    family_timeline_rows = build_timeline_rows(memory, selected_families=selected_families)
    write_timeline_outputs(family_timeline_rows, timeline_dir)
    timeline_file = timeline_dir / "dio_mini_family_reflection_timeline.csv"

    view_inputs = []
    view_dirs = {}
    inner_protocol_dirs = {}
    for probe_name, debug_root in probes:
        view_dir = output_dir / f"passive_cortex_{_probe_output_name(probe_name)}"
        view_rows = build_view_rows(
            family_file,
            timeline_file,
            debug_root,
            selected_families=selected_families,
        )
        write_view_outputs(view_rows, view_dir)
        view_csv = view_dir / "dio_mini_passive_cortex_view.csv"
        view_inputs.append((probe_name, view_csv))
        view_dirs[probe_name] = str(view_dir)

    comparison_dir = output_dir / "passive_cortex_comparison"
    comparison_detail, comparison_summary = build_comparison_rows(view_inputs)
    write_comparison_outputs(comparison_detail, comparison_summary, comparison_dir)

    maturation_dir = output_dir / "family_maturation_path"
    maturation_detail = []
    maturation_summary = []
    if len(probes) > 1:
        maturation_detail, maturation_summary = build_maturation_rows(probes, selected_families)
        write_maturation_outputs(maturation_detail, maturation_summary, maturation_dir)

    maturation_reflection_rows = []
    recognition_boundary_detail = []
    recognition_boundary_summary = []
    if maturation_summary:
        maturation_csv = maturation_dir / "dio_mini_family_maturation_path.csv"
        maturation_reflection_dir = output_dir / "family_maturation_reflection"
        maturation_reflection_rows = build_maturation_reflection_rows(maturation_csv, selected_families)
        write_maturation_reflection_outputs(maturation_reflection_rows, maturation_reflection_dir)
        maturation_reflection_csv = maturation_reflection_dir / "dio_mini_family_maturation_reflection.csv"
        recognition_boundary_dir = output_dir / "passive_recognition_boundary"
        recognition_boundary_detail, recognition_boundary_summary = build_recognition_boundary_rows(
            maturation_reflection_csv
        )
        write_recognition_boundary_outputs(
            recognition_boundary_detail,
            recognition_boundary_summary,
            recognition_boundary_dir,
        )

    inner_awareness_rows = []
    inner_awareness_summary = []
    if maturation_reflection_rows:
        reflection_csv = output_dir / "family_maturation_reflection" / "dio_mini_family_maturation_reflection.csv"
        inner_awareness_dir = output_dir / "passive_inner_awareness"
        inner_awareness_rows, inner_awareness_summary = build_inner_awareness_rows(reflection_csv, selected_families)
        write_inner_awareness_outputs(inner_awareness_rows, inner_awareness_summary, inner_awareness_dir)

    inner_protocol_rows = 0
    inner_timeline_rows = 0
    inner_stability_rows = 0
    inner_coherence_rows = 0
    if inner_awareness_rows:
        inner_awareness_csv = output_dir / "passive_inner_awareness" / "dio_mini_passive_inner_awareness.csv"
        for probe_name, debug_root in probes:
            protocol_dir = output_dir / f"passive_inner_state_{_probe_output_name(probe_name)}"
            protocol_detail, protocol_summary = build_inner_state_protocol_rows(debug_root, inner_awareness_csv)
            write_inner_state_protocol_outputs(protocol_detail, protocol_summary, protocol_dir)
            inner_protocol_rows += len(protocol_detail)
            inner_protocol_dirs[probe_name] = str(protocol_dir)
            protocol_csv = protocol_dir / "dio_mini_passive_inner_state_protocol.csv"
            inner_timeline_dir = output_dir / f"passive_inner_timeline_{_probe_output_name(probe_name)}"
            inner_timeline_detail, inner_timeline_summary = build_inner_state_timeline_rows(protocol_csv)
            write_inner_state_timeline_outputs(inner_timeline_detail, inner_timeline_summary, inner_timeline_dir)
            inner_timeline_rows += len(inner_timeline_detail)
            timeline_csv = inner_timeline_dir / "dio_mini_passive_inner_state_timeline.csv"
            stability_dir = output_dir / f"passive_inner_stability_{_probe_output_name(probe_name)}"
            stability_detail, stability_overview, stability_transitions = build_inner_stability_rows(timeline_csv)
            write_inner_stability_outputs(stability_detail, stability_overview, stability_transitions, stability_dir)
            inner_stability_rows += len(stability_detail)
            coherence_dir = output_dir / f"passive_inner_coherence_{_probe_output_name(probe_name)}"
            coherence_detail, coherence_summary = build_inner_coherence_rows(timeline_csv)
            write_inner_coherence_outputs(coherence_detail, coherence_summary, coherence_dir)
            inner_coherence_rows += len(coherence_detail)

    _write_bundle_summary(
        output_dir=output_dir,
        family_rows=len(family_rows),
        timeline_rows=len(family_timeline_rows),
        comparison_rows=len(comparison_summary),
        maturation_rows=len(maturation_summary),
        probes=[name for name, _ in probes],
        view_dirs=view_dirs,
        maturation_summary=maturation_summary,
        maturation_reflection_rows=maturation_reflection_rows,
        inner_awareness_rows=inner_awareness_rows,
        inner_awareness_summary=inner_awareness_summary,
        recognition_boundary_rows=len(recognition_boundary_detail),
        recognition_boundary_summary_rows=len(recognition_boundary_summary),
        inner_protocol_rows=inner_protocol_rows,
        inner_timeline_rows=inner_timeline_rows,
        inner_stability_rows=inner_stability_rows,
        inner_coherence_rows=inner_coherence_rows,
    )

    return {
        "family_rows": len(family_rows),
        "timeline_rows": len(family_timeline_rows),
        "probes": [name for name, _ in probes],
        "view_dirs": view_dirs,
        "comparison_rows": len(comparison_summary),
        "maturation_rows": len(maturation_summary),
        "maturation_reflection_rows": len(maturation_reflection_rows),
        "recognition_boundary_rows": len(recognition_boundary_detail),
        "recognition_boundary_summary_rows": len(recognition_boundary_summary),
        "inner_awareness_rows": len(inner_awareness_rows),
        "inner_protocol_rows": inner_protocol_rows,
        "inner_timeline_rows": inner_timeline_rows,
        "inner_stability_rows": inner_stability_rows,
        "inner_coherence_rows": inner_coherence_rows,
        "inner_protocol_dirs": inner_protocol_dirs,
        "output_dir": str(output_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run passive DIO_MINI cortex diagnosis bundle")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--probe", action="append", required=True, help="name=debug_root")
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    selected = {str(item).strip() for item in args.family if str(item).strip()}
    summary = run_bundle(
        memory_path=Path(args.memory),
        probes=[_parse_probe(item) for item in args.probe],
        output_dir=Path(args.output_dir),
        selected_families=selected or None,
    )
    print(
        f"family_rows={summary['family_rows']} "
        f"timeline_rows={summary['timeline_rows']} "
        f"comparison_rows={summary['comparison_rows']} "
        f"maturation_rows={summary['maturation_rows']} "
        f"maturation_reflection_rows={summary['maturation_reflection_rows']} "
        f"recognition_boundary_rows={summary['recognition_boundary_rows']} "
        f"inner_awareness_rows={summary['inner_awareness_rows']} "
        f"inner_protocol_rows={summary['inner_protocol_rows']} "
        f"inner_timeline_rows={summary['inner_timeline_rows']} "
        f"inner_stability_rows={summary['inner_stability_rows']} "
        f"inner_coherence_rows={summary['inner_coherence_rows']}"
    )
    for probe_name, view_dir in summary["view_dirs"].items():
        print(f"{probe_name}: {view_dir}")


if __name__ == "__main__":
    main()
