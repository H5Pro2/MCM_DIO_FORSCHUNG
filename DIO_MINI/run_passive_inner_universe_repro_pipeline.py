"""Run passive Mini-DIO inner-universe reproduction diagnostics.

This module is a diagnostic helper. It executes controlled Mini-DIO runs and
builds passive meaning-space, semantic-matrix, text-island, and lineage
reports. The generated memory is diagnostic only and must not be read by
Mini-DIO for action, gates, entries, or direction.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROBES = tuple(range(20, 27))


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _run(command: list[str], cwd: Path, dry_run: bool = False) -> None:
    printable = " ".join(command)
    print(printable)
    if dry_run:
        return
    subprocess.run(command, cwd=str(cwd), check=True)


def _probe_data_path(data_dir: Path, probe: int, variant: str) -> Path:
    pattern = f"kontrolliert_sensor_relation_probe{probe}_*_6episoden_variante{variant}_*_5m_SOLUSDT.csv"
    matches = sorted(data_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No data file for probe{probe}, variant {variant}: {pattern}")
    if len(matches) > 1:
        names = ", ".join(path.name for path in matches)
        raise RuntimeError(f"Ambiguous data file for probe{probe}, variant {variant}: {names}")
    return matches[0]


def _resolve_path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


def _debug_root(debug_dir: Path, variant: str, tag: str, probe: int) -> Path:
    return debug_dir / f"dio_mini_repro_semantic_matrix_6episoden_variante{variant}_{tag}_probe{probe}"


def _run_probe_set(args: argparse.Namespace, root: Path, probe_dirs: list[Path]) -> None:
    data_dir = root / args.data_dir
    debug_dir = root / args.debug_dir
    memory_path = root / args.memory

    for index, probe in enumerate(args.probes):
        data_path = _probe_data_path(data_dir, probe, args.variant)
        probe_debug = _debug_root(debug_dir, args.variant, args.tag, probe)
        probe_dirs.append(probe_debug)
        if args.skip_runs:
            continue
        command = [
            sys.executable,
            "-m",
            "DIO_MINI.run_mini",
            "--data",
            str(data_path),
            "--runs",
            str(args.runs),
            "--memory",
            str(memory_path),
            "--debug-root",
            str(probe_debug),
            "--world-label",
            f"variante{args.variant}_{args.tag}_probe{probe}",
        ]
        if args.reset_memory and index == 0:
            command.append("--reset-memory")
        _run(command, root, dry_run=args.dry_run)


def _build_passive_reports(args: argparse.Namespace, root: Path, probe_dirs: list[Path]) -> dict[str, Path]:
    debug_dir = root / args.debug_dir
    base = f"6episoden_variante{args.variant}_{args.tag}_{args.date_tag}"
    meaning_dir = debug_dir / f"dio_mini_passive_cluster_meaning_space_{base}"
    neighbors_dir = debug_dir / f"dio_mini_passive_cluster_neighbors_{base}"
    matrix_dir = debug_dir / f"dio_mini_passive_semantic_matrix_{base}"
    density_dir = debug_dir / f"dio_mini_passive_semantic_density_{base}"
    memory_out_dir = debug_dir / f"dio_mini_semantic_matrix_memory_variante{args.variant}_{args.tag}_{args.date_tag}"
    maturity_dir = debug_dir / f"dio_mini_passive_text_island_maturity_variante{args.variant}_{args.tag}_{args.date_tag}"
    inner_map_dir = debug_dir / f"dio_mini_passive_text_island_inner_map_variante{args.variant}_{args.tag}_{args.date_tag}"
    memory_path = root / args.semantic_matrix_memory
    meaning_csv = meaning_dir / "passive_cluster_meaning_space.csv"
    neighbors_csv = neighbors_dir / "passive_cluster_neighbors.csv"
    maturity_csv = maturity_dir / "passive_text_island_maturity.csv"

    _run(
        [
            sys.executable,
            "-m",
            "DIO_MINI.report_passive_cluster_meaning_space",
            "--debug-root",
            *[str(path) for path in probe_dirs],
            "--output-dir",
            str(meaning_dir),
        ],
        root,
        dry_run=args.dry_run,
    )
    _run(
        [
            sys.executable,
            "-m",
            "DIO_MINI.report_passive_cluster_neighbors",
            "--meaning-space",
            str(meaning_csv),
            "--topn",
            str(args.neighbor_topn),
            "--output-dir",
            str(neighbors_dir),
        ],
        root,
        dry_run=args.dry_run,
    )
    _run(
        [
            sys.executable,
            "-m",
            "DIO_MINI.report_passive_semantic_matrix",
            "--meaning-space",
            str(meaning_csv),
            "--neighbors",
            str(neighbors_csv),
            "--min-similarity",
            str(args.min_similarity),
            "--output-dir",
            str(matrix_dir),
        ],
        root,
        dry_run=args.dry_run,
    )
    _run(
        [
            sys.executable,
            "-m",
            "DIO_MINI.report_passive_semantic_density",
            "--matrix-dir",
            str(matrix_dir),
            "--output-dir",
            str(density_dir),
        ],
        root,
        dry_run=args.dry_run,
    )
    _run(
        [
            sys.executable,
            "-m",
            "DIO_MINI.store_passive_semantic_matrix_memory",
            "--matrix-dir",
            str(matrix_dir),
            "--density-dir",
            str(density_dir),
            "--memory",
            str(memory_path),
            "--output-dir",
            str(memory_out_dir),
            "--source-label",
            f"variante{args.variant}_{args.tag}",
        ],
        root,
        dry_run=args.dry_run,
    )
    _run(
        [
            sys.executable,
            "-m",
            "DIO_MINI.report_passive_text_island_maturity",
            "--memory",
            str(memory_path),
            "--output-dir",
            str(maturity_dir),
        ],
        root,
        dry_run=args.dry_run,
    )
    _run(
        [
            sys.executable,
            "-m",
            "DIO_MINI.report_passive_text_island_inner_map",
            "--maturity",
            str(maturity_csv),
            "--output-dir",
            str(inner_map_dir),
        ],
        root,
        dry_run=args.dry_run,
    )
    return {
        "meaning": meaning_dir,
        "neighbors": neighbors_dir,
        "matrix": matrix_dir,
        "density": density_dir,
        "memory": memory_out_dir,
        "maturity": maturity_dir,
        "inner_map": inner_map_dir,
    }


def _optional_comparisons(args: argparse.Namespace, root: Path, outputs: dict[str, Path]) -> None:
    debug_dir = root / args.debug_dir
    shift_dir = None
    alignment_dir = None
    if args.compare_matrix:
        compare_dir = debug_dir / f"dio_mini_passive_semantic_matrix_compare_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"
        _run(
            [
                sys.executable,
                "-m",
                "DIO_MINI.compare_passive_semantic_matrices",
                "--reference",
                str(root / args.compare_matrix),
                "--candidate",
                str(outputs["matrix"]),
                "--output-dir",
                str(compare_dir),
            ],
            root,
            dry_run=args.dry_run,
        )
    if args.compare_inner_map:
        compare_dir = debug_dir / f"dio_mini_passive_text_island_inner_map_compare_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"
        _run(
            [
                sys.executable,
                "-m",
                "DIO_MINI.compare_passive_text_island_inner_maps",
                "--left",
                str(root / args.compare_inner_map),
                "--right",
                str(outputs["inner_map"] / "passive_text_island_inner_map.csv"),
                "--output-dir",
                str(compare_dir),
            ],
            root,
            dry_run=args.dry_run,
        )
        shift_dir = debug_dir / f"dio_mini_passive_syntax_maturity_shift_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"
        _run(
            [
                sys.executable,
                "-m",
                "DIO_MINI.report_passive_syntax_maturity_shift",
                "--left",
                str(root / args.compare_inner_map),
                "--right",
                str(outputs["inner_map"] / "passive_text_island_inner_map.csv"),
                "--left-label",
                str(args.compare_label),
                "--right-label",
                f"VARIANTE_{args.variant}_{args.tag}",
                "--output-dir",
                str(shift_dir),
            ],
            root,
            dry_run=args.dry_run,
        )
        if args.compare_meaning_space:
            alignment_dir = debug_dir / f"dio_mini_passive_shift_sensory_field_alignment_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"
            _run(
                [
                    sys.executable,
                    "-m",
                    "DIO_MINI.report_passive_shift_sensory_field_alignment",
                    "--shift",
                    str(shift_dir / "passive_syntax_maturity_shift.csv"),
                    "--left-meaning-space",
                    str(root / args.compare_meaning_space),
                    "--right-meaning-space",
                    str(outputs["meaning"] / "passive_cluster_meaning_space.csv"),
                    "--left-label",
                    str(args.compare_label),
                    "--right-label",
                    f"VARIANTE_{args.variant}_{args.tag}",
                    "--output-dir",
                    str(alignment_dir),
                ],
                root,
                dry_run=args.dry_run,
            )
    direction_path = _resolve_path(root, args.temporal_kipp_direction) if args.temporal_kipp_direction else None
    temporal_root_args = []
    if args.temporal_left_debug_root and args.temporal_right_debug_root:
        for value in args.temporal_left_debug_root:
            temporal_root_args.extend(["--left-debug-root", str(_resolve_path(root, value))])
        for value in args.temporal_right_debug_root:
            temporal_root_args.extend(["--right-debug-root", str(_resolve_path(root, value))])
    if args.build_direction_support_shift and alignment_dir is not None and temporal_root_args:
        direction_dir = debug_dir / f"dio_mini_passive_direction_support_shift_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"
        _run(
            [
                sys.executable,
                "-m",
                "DIO_MINI.report_passive_direction_support_shift",
                "--alignment",
                str(alignment_dir / "passive_shift_sensory_field_alignment.csv"),
                *temporal_root_args,
                "--output-dir",
                str(direction_dir),
            ],
            root,
            dry_run=args.dry_run,
        )
        direction_path = direction_dir / "passive_direction_support_shift.csv"
    if direction_path is not None and temporal_root_args:
        temporal_dir = debug_dir / f"dio_mini_passive_temporal_kipp_points_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"
        _run(
            [
                sys.executable,
                "-m",
                "DIO_MINI.report_passive_temporal_kipp_points",
                "--direction",
                str(direction_path),
                *temporal_root_args,
                "--output-dir",
                str(temporal_dir),
            ],
            root,
            dry_run=args.dry_run,
        )
        if args.build_trace_carry_curve:
            carry_curve_dir = debug_dir / f"dio_mini_passive_trace_carry_curve_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"
            _run(
                [
                    sys.executable,
                    "-m",
                    "DIO_MINI.report_passive_trace_carry_curve",
                    "--temporal-detail",
                    str(temporal_dir / "passive_temporal_kipp_points_detail.csv"),
                    "--temporal-families",
                    str(temporal_dir / "passive_temporal_kipp_points_families.csv"),
                    "--output-dir",
                    str(carry_curve_dir),
                ],
                root,
                dry_run=args.dry_run,
            )
            if args.build_carry_contrast and alignment_dir is not None:
                contrast_dir = debug_dir / f"dio_mini_passive_carry_contrast_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"
                followup_result_csv = None
                _run(
                    [
                        sys.executable,
                        "-m",
                        "DIO_MINI.report_passive_carry_contrast",
                        "--carry-families",
                        str(carry_curve_dir / "passive_trace_carry_curve_families.csv"),
                        "--alignment",
                        str(alignment_dir / "passive_shift_sensory_field_alignment.csv"),
                        "--direction",
                        str(direction_path),
                        "--temporal-detail",
                        str(temporal_dir / "passive_temporal_kipp_points_detail.csv"),
                        "--output-dir",
                        str(contrast_dir),
                    ],
                    root,
                    dry_run=args.dry_run,
                )
                if args.carry_followup_candidates:
                    followup_result_dir = debug_dir / f"dio_mini_passive_carry_followup_result_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"
                    followup_result_csv = followup_result_dir / "passive_carry_followup_result.csv"
                    _run(
                        [
                            sys.executable,
                            "-m",
                            "DIO_MINI.report_passive_carry_followup_result",
                            "--candidates",
                            str(_resolve_path(root, args.carry_followup_candidates)),
                            "--new-carry-contrast",
                            str(contrast_dir / "passive_carry_contrast_families.csv"),
                            "--output-dir",
                            str(followup_result_dir),
                        ],
                        root,
                        dry_run=args.dry_run,
                    )
                    if args.build_carry_separator:
                        _run(
                            [
                                sys.executable,
                                "-m",
                                "DIO_MINI.report_passive_carry_separator",
                                "--carry-contrast",
                                str(contrast_dir / "passive_carry_contrast_families.csv"),
                                "--followup-result",
                                str(followup_result_csv),
                                "--reference-family",
                                str(args.carry_separator_reference or args.carry_profile_family or "dio_11vr"),
                                "--output-dir",
                                str(debug_dir / f"dio_mini_passive_carry_separator_{args.carry_separator_reference or args.carry_profile_family or 'dio_11vr'}_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"),
                            ],
                            root,
                            dry_run=args.dry_run,
                        )
                if args.carry_profile_family:
                    profile_dir = debug_dir / f"dio_mini_passive_carry_profile_{args.carry_profile_family}_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"
                    _run(
                        [
                            sys.executable,
                            "-m",
                            "DIO_MINI.report_passive_carry_profile",
                            "--carry-contrast",
                            str(contrast_dir / "passive_carry_contrast_families.csv"),
                            "--family",
                            str(args.carry_profile_family),
                            "--topn",
                            str(args.carry_profile_topn),
                            "--output-dir",
                            str(profile_dir),
                        ],
                        root,
                        dry_run=args.dry_run,
                    )
                    if args.build_carry_followup_candidates:
                        _run(
                            [
                                sys.executable,
                                "-m",
                                "DIO_MINI.report_passive_carry_followup_candidates",
                                "--carry-profile-contrast",
                                str(profile_dir / "passive_carry_profile_contrast.csv"),
                                "--limit",
                                str(args.carry_followup_limit),
                                "--output-dir",
                                str(debug_dir / f"dio_mini_passive_carry_followup_candidates_{args.carry_profile_family}_{args.compare_label}_vs_variante{args.variant}_{args.tag}_{args.date_tag}"),
                            ],
                            root,
                            dry_run=args.dry_run,
                        )
    if args.family:
        lineage_dir = debug_dir / f"dio_mini_passive_family_bridge_lineage_variante{args.variant}_{args.tag}_{args.date_tag}"
        stage_args = []
        if args.compare_inner_map:
            stage_args.extend(["--stage", f"{args.compare_label}={root / args.compare_inner_map}"])
        stage_args.extend(["--stage", f"VARIANTE_{args.variant}_{args.tag}={outputs['inner_map'] / 'passive_text_island_inner_map.csv'}"])
        family_args = []
        for family in args.family:
            family_args.extend(["--family", family])
        _run(
            [
                sys.executable,
                "-m",
                "DIO_MINI.report_passive_family_bridge_lineage",
                *family_args,
                *stage_args,
                "--output-dir",
                str(lineage_dir),
            ],
            root,
            dry_run=args.dry_run,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run passive Mini-DIO inner-universe reproduction pipeline")
    parser.add_argument("--variant", required=True, help="Controlled variant letter, e.g. F, G, or H")
    parser.add_argument("--tag", required=True, help="Short run tag, e.g. repro2")
    parser.add_argument("--date-tag", default="20260607")
    parser.add_argument("--runs", type=int, default=2)
    parser.add_argument("--probes", type=int, nargs="+", default=list(PROBES))
    parser.add_argument("--reset-memory", action="store_true")
    parser.add_argument("--skip-runs", action="store_true", help="Reuse existing probe debug folders and only rebuild passive reports")
    parser.add_argument("--memory", default="bot_memory/dio_mini_repro_pipeline_runtime_memory.json")
    parser.add_argument("--semantic-matrix-memory", default="bot_memory/dio_mini_passive_repro_pipeline_semantic_matrix_memory.json")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--debug-dir", default="debug")
    parser.add_argument("--neighbor-topn", type=int, default=12)
    parser.add_argument("--min-similarity", type=float, default=0.92)
    parser.add_argument("--compare-matrix", default="")
    parser.add_argument("--compare-inner-map", default="")
    parser.add_argument("--compare-meaning-space", default="")
    parser.add_argument("--compare-label", default="REFERENCE")
    parser.add_argument("--temporal-kipp-direction", default="", help="Existing passive_direction_support_shift.csv for optional temporal kipp analysis")
    parser.add_argument("--temporal-left-debug-root", action="append", default=[], help="Existing left debug root for optional temporal kipp analysis; repeat for multiple probes")
    parser.add_argument("--temporal-right-debug-root", action="append", default=[], help="Existing right debug root for optional temporal kipp analysis; repeat for multiple probes")
    parser.add_argument("--build-direction-support-shift", action="store_true", help="Build passive direction support shift from alignment and debug roots")
    parser.add_argument("--build-trace-carry-curve", action="store_true", help="Build passive trace carry curve after temporal kipp analysis")
    parser.add_argument("--build-carry-contrast", action="store_true", help="Build passive carry contrast after trace carry curve and alignment analysis")
    parser.add_argument("--carry-profile-family", default="", help="Optional family for passive carry profile after carry contrast, e.g. dio_11vr")
    parser.add_argument("--carry-profile-topn", type=int, default=20)
    parser.add_argument("--build-carry-followup-candidates", action="store_true", help="Build passive follow-up candidates after carry profile")
    parser.add_argument("--carry-followup-limit", type=int, default=20)
    parser.add_argument("--carry-followup-candidates", default="", help="Existing passive_carry_followup_candidates.csv to evaluate against new carry contrast")
    parser.add_argument("--build-carry-separator", action="store_true", help="Build passive stable-vs-keim separator after follow-up result")
    parser.add_argument("--carry-separator-reference", default="", help="Reference family for passive carry separator; defaults to carry-profile-family or dio_11vr")
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = _repo_root()
    probe_dirs: list[Path] = []
    _run_probe_set(args, root, probe_dirs)
    outputs = _build_passive_reports(args, root, probe_dirs)
    _optional_comparisons(args, root, outputs)
    print("passive_inner_universe_repro_pipeline complete")
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
