"""Compare passive Mini-DIO inner maturity maps.

This report checks whether passive inner seeds repeat across map generations.
It does not train memory, influence action, or create gates.
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


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _parse_source(spec: str) -> tuple[str, Path]:
    if "=" in spec:
        label, path = spec.split("=", 1)
        return label.strip() or Path(path).parent.name, Path(path)
    path = Path(spec)
    return path.parent.name, path


def _transition_state(seeds: set[str], source_count: int) -> str:
    if source_count >= 2 and len(seeds) == 1:
        return "inner_seed_repeats_stably"
    if source_count >= 2 and len(seeds) > 1:
        return "inner_seed_reorganizes"
    return "inner_seed_local"


def build_report(sources: list[tuple[str, Path]]) -> tuple[list[dict], list[dict], list[dict]]:
    detail: list[dict] = []
    by_family: dict[str, dict] = {}
    by_seed: dict[str, dict] = {}

    for label, path in sources:
        for row in _read_csv(path):
            family = str(row.get("passive_family_action", "") or "-")
            seed = str(row.get("inner_maturity_seed", "") or "inner_unknown_seed")
            item = {
                "map_label": label,
                "source_label": str(row.get("source_label", "") or ""),
                "passive_family_action": family,
                "action": str(row.get("action", "") or ""),
                "inner_maturity_seed": seed,
                "passive_maturity_state": str(row.get("passive_maturity_state", "") or ""),
                "best_similarity": round(_safe_float(row.get("best_similarity")), 9),
                "best_mcm_similarity": round(_safe_float(row.get("best_mcm_similarity")), 9),
                "best_real_family_action": str(row.get("best_real_family_action", "") or ""),
                "best_real_reward_sum": round(_safe_float(row.get("best_real_reward_sum")), 9),
                "inner_sentence": str(row.get("inner_sentence", "") or ""),
                "passive_only": 1,
            }
            detail.append(item)

            family_bucket = by_family.setdefault(
                family,
                {
                    "passive_family_action": family,
                    "map_labels": set(),
                    "source_labels": set(),
                    "seeds": set(),
                    "actions": set(),
                    "best_similarity_sum": 0.0,
                    "best_mcm_similarity_sum": 0.0,
                    "real_reward_sum": 0.0,
                    "trace_count": 0,
                },
            )
            family_bucket["map_labels"].add(label)
            family_bucket["source_labels"].add(item["source_label"])
            family_bucket["seeds"].add(seed)
            family_bucket["actions"].add(item["action"])
            family_bucket["best_similarity_sum"] += item["best_similarity"]
            family_bucket["best_mcm_similarity_sum"] += item["best_mcm_similarity"]
            family_bucket["real_reward_sum"] += item["best_real_reward_sum"]
            family_bucket["trace_count"] += 1

            seed_bucket = by_seed.setdefault(
                seed,
                {
                    "inner_maturity_seed": seed,
                    "map_labels": set(),
                    "source_labels": set(),
                    "families": set(),
                    "actions": set(),
                    "best_similarity_sum": 0.0,
                    "best_mcm_similarity_sum": 0.0,
                    "real_reward_sum": 0.0,
                    "trace_count": 0,
                },
            )
            seed_bucket["map_labels"].add(label)
            seed_bucket["source_labels"].add(item["source_label"])
            seed_bucket["families"].add(family)
            seed_bucket["actions"].add(item["action"])
            seed_bucket["best_similarity_sum"] += item["best_similarity"]
            seed_bucket["best_mcm_similarity_sum"] += item["best_mcm_similarity"]
            seed_bucket["real_reward_sum"] += item["best_real_reward_sum"]
            seed_bucket["trace_count"] += 1

    family_summary: list[dict] = []
    for bucket in by_family.values():
        count = max(1, int(bucket["trace_count"]))
        maps = set(bucket["map_labels"])
        seeds = set(bucket["seeds"])
        family_summary.append(
            {
                "passive_family_action": bucket["passive_family_action"],
                "map_count": len(maps),
                "map_labels": ",".join(sorted(maps)),
                "source_labels": ",".join(sorted(bucket["source_labels"])),
                "seeds": ",".join(sorted(seeds)),
                "actions": ",".join(sorted(bucket["actions"])),
                "trace_count": count,
                "avg_similarity": round(float(bucket["best_similarity_sum"]) / count, 9),
                "avg_mcm_similarity": round(float(bucket["best_mcm_similarity_sum"]) / count, 9),
                "real_reward_sum": round(float(bucket["real_reward_sum"]), 9),
                "transition_state": _transition_state(seeds, len(maps)),
                "passive_only": 1,
            }
        )

    seed_summary: list[dict] = []
    for bucket in by_seed.values():
        count = max(1, int(bucket["trace_count"]))
        maps = set(bucket["map_labels"])
        seed_summary.append(
            {
                "inner_maturity_seed": bucket["inner_maturity_seed"],
                "map_count": len(maps),
                "map_labels": ",".join(sorted(maps)),
                "source_labels": ",".join(sorted(bucket["source_labels"])),
                "family_count": len(bucket["families"]),
                "families": ",".join(sorted(bucket["families"])),
                "actions": ",".join(sorted(bucket["actions"])),
                "trace_count": count,
                "avg_similarity": round(float(bucket["best_similarity_sum"]) / count, 9),
                "avg_mcm_similarity": round(float(bucket["best_mcm_similarity_sum"]) / count, 9),
                "real_reward_sum": round(float(bucket["real_reward_sum"]), 9),
                "seed_stability": "seed_repeats_across_maps" if len(maps) >= 2 else "seed_local_to_one_map",
                "passive_only": 1,
            }
        )

    detail.sort(key=lambda item: (str(item["map_label"]), str(item["inner_maturity_seed"]), str(item["passive_family_action"])))
    family_summary.sort(key=lambda item: (-int(item["map_count"]), str(item["passive_family_action"])))
    seed_summary.sort(key=lambda item: (-int(item["map_count"]), -int(item["trace_count"]), str(item["inner_maturity_seed"])))
    return detail, family_summary, seed_summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    detail: list[dict],
    family_summary: list[dict],
    seed_summary: list[dict],
    sources: list[tuple[str, Path]],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_inner_maturity_stability.csv"
    family_csv = output_dir / "dio_mini_passive_inner_maturity_stability_by_family.csv"
    seed_csv = output_dir / "dio_mini_passive_inner_maturity_stability_by_seed.csv"
    json_path = output_dir / "dio_mini_passive_inner_maturity_stability.json"
    md_path = output_dir / "dio_mini_passive_inner_maturity_stability.md"

    _write_csv(detail_csv, detail, ["map_label", "passive_family_action", "inner_maturity_seed"])
    _write_csv(family_csv, family_summary, ["passive_family_action", "map_count", "seeds"])
    _write_csv(seed_csv, seed_summary, ["inner_maturity_seed", "map_count", "trace_count"])
    json_path.write_text(
        json.dumps(
            {
                "sources": [{"label": label, "path": str(path)} for label, path in sources],
                "detail": detail,
                "family_summary": family_summary,
                "seed_summary": seed_summary,
                "boundary": {
                    "writes_training_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_future_teacher": False,
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Inner Maturity Stability", ""]
    lines.append("## Quellen")
    for label, path in sources:
        lines.append(f"- {label}: {path}")
    lines.extend(["", "## Keim-Stabilitaet"])
    if not seed_summary:
        lines.append("- keine Keime")
    for row in seed_summary:
        lines.append(
            f"- {row['inner_maturity_seed']}: maps={row['map_count']} traces={row['trace_count']} "
            f"families={row['family_count']} actions={row['actions']} state={row['seed_stability']}"
        )
    lines.extend(["", "## Familien-Stabilitaet"])
    repeated = [row for row in family_summary if int(row["map_count"]) >= 2]
    if not repeated:
        lines.append("- keine identische passive Familie ueber mehrere Landkarten")
    for row in repeated:
        lines.append(
            f"- {row['passive_family_action']}: maps={row['map_count']} seeds={row['seeds']} "
            f"transition={row['transition_state']}"
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Stabilitaetsdiagnose",
            "- keine Handlung",
            "- kein Trainingsmemory",
            "- kein Gate",
            "- kein Zukunftslehrer",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive Mini-DIO inner maturity maps")
    parser.add_argument("--source", action="append", required=True, help="label=map.csv or map.csv; can be repeated")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    sources = [_parse_source(spec) for spec in args.source]
    detail, family_summary, seed_summary = build_report(sources)
    write_outputs(detail, family_summary, seed_summary, sources, Path(args.output_dir))
    print(
        f"passive_inner_maturity_stability_rows={len(detail)} "
        f"families={len(family_summary)} seeds={len(seed_summary)}"
    )
    for row in seed_summary:
        print(
            f"{row['inner_maturity_seed']} maps={row['map_count']} "
            f"traces={row['trace_count']} state={row['seed_stability']}"
        )


if __name__ == "__main__":
    main()
