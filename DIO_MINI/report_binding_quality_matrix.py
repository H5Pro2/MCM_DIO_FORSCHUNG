"""Compare DIO_MINI episode binding quality across debug roots."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.report_episode_binding import _summaries, _iter_rows


def _root_name(path: Path) -> str:
    return path.name or str(path)


def _collect(debug_roots: list[Path]) -> tuple[list[dict], list[dict]]:
    detail_rows: list[dict] = []
    root_rows: list[dict] = []
    for root in debug_roots:
        rows = _iter_rows(root)
        detail, overview = _summaries(rows)
        root = root.resolve()
        by_state = {str(item["binding_state"]): item for item in overview}
        executed = float(by_state.get("executed_aligned", {}).get("reward_sum", 0.0) or 0.0)
        overheld = float(by_state.get("held_useful_impulse", {}).get("held_impulse_potential_sum", 0.0) or 0.0)
        observed = float(by_state.get("observed_not_bound", {}).get("unrealized_best_reward_sum", 0.0) or 0.0)
        total_episodes = len(detail)
        root_rows.append(
            {
                "debug_root": str(root),
                "root_name": _root_name(root),
                "episodes": total_episodes,
                "executed_confirmed_count": int(by_state.get("executed_aligned", {}).get("count", 0) or 0),
                "executed_confirmed_reward": round(executed, 6),
                "overheld_count": int(by_state.get("held_useful_impulse", {}).get("count", 0) or 0),
                "overheld_potential": round(overheld, 6),
                "observed_potential_count": int(by_state.get("observed_not_bound", {}).get("count", 0) or 0),
                "observed_potential": round(observed, 6),
                "quiet_count": int(by_state.get("quiet", {}).get("count", 0) or 0),
                "binding_balance_note": _balance_note(executed, overheld, observed),
            }
        )
        for item in detail:
            item = dict(item)
            item["debug_root"] = str(root)
            item["root_name"] = _root_name(root)
            detail_rows.append(item)
    return detail_rows, root_rows


def _balance_note(executed_reward: float, overheld_potential: float, observed_potential: float) -> str:
    if executed_reward <= 0.0 and (overheld_potential > 0.0 or observed_potential > 0.0):
        return "binding_or_observation_dominates"
    if overheld_potential > executed_reward:
        return "overholding_larger_than_execution"
    if observed_potential > executed_reward * 2.0 and observed_potential > 0.0:
        return "large_observation_potential"
    if executed_reward > 0.0 and overheld_potential == 0.0:
        return "execution_without_overholding"
    return "mixed"


def _write(detail: list[dict], roots: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_binding_quality_matrix_detail.csv"
    root_path = output_dir / "dio_mini_binding_quality_matrix.csv"
    json_path = output_dir / "dio_mini_binding_quality_matrix.json"
    md_path = output_dir / "dio_mini_binding_quality_matrix.md"

    if detail:
        fields = ["debug_root", "root_name"] + [key for key in detail[0].keys() if key not in ("debug_root", "root_name")]
        with detail_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(detail)
    else:
        detail_path.write_text("", encoding="utf-8")

    fields = [
        "debug_root",
        "root_name",
        "episodes",
        "executed_confirmed_count",
        "executed_confirmed_reward",
        "overheld_count",
        "overheld_potential",
        "observed_potential_count",
        "observed_potential",
        "quiet_count",
        "binding_balance_note",
    ]
    with root_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(roots)
    json_path.write_text(json.dumps(roots, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Binding Quality Matrix", ""]
    if not roots:
        lines.append("Keine Debug-Wurzeln gefunden.")
    for row in roots:
        lines.extend(
            [
                f"## {row['root_name']}",
                f"- episodes: {row['episodes']}",
                f"- executed_confirmed: {row['executed_confirmed_count']} / {float(row['executed_confirmed_reward']):.6f}",
                f"- overheld: {row['overheld_count']} / {float(row['overheld_potential']):.6f}",
                f"- observed_potential: {row['observed_potential_count']} / {float(row['observed_potential']):.6f}",
                f"- quiet: {row['quiet_count']}",
                f"- note: {row['binding_balance_note']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug-root", action="append", default=[])
    parser.add_argument("--debug-glob")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    roots = [Path(item) for item in args.debug_root]
    if args.debug_glob:
        roots.extend(sorted(Path().glob(args.debug_glob)))
    roots = [root for root in roots if root.exists()]
    detail, root_rows = _collect(roots)
    _write(detail, root_rows, Path(args.output_dir))
    print(f"debug_roots={len(root_rows)} episodes={len(detail)}")
    for row in root_rows:
        print(
            f"{row['root_name']} episodes={row['episodes']} "
            f"executed={row['executed_confirmed_count']}/{row['executed_confirmed_reward']} "
            f"overheld={row['overheld_count']}/{row['overheld_potential']} "
            f"observed={row['observed_potential_count']}/{row['observed_potential']} "
            f"note={row['binding_balance_note']}"
        )


if __name__ == "__main__":
    main()
