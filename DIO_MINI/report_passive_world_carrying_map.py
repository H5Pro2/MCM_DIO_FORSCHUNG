"""Build a passive world-level carrying map from kinship transfer reports.

The report compares complete target worlds instead of single families. It is
diagnostic only and does not write memory or influence action.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


NUMERIC_FIELDS = [
    "passive_carrying_nearness",
    "carried_kinship_cosine",
    "target_max_trade_readiness",
    "target_avg_neuro_balance",
    "target_max_temporal_trust_support",
    "target_max_temporal_caution_support",
]


def _float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def parse_input(raw: str) -> tuple[str, Path]:
    if "=" not in str(raw):
        raise SystemExit(f"--world must be label=csv_path, got: {raw}")
    label, path = str(raw).split("=", 1)
    label = label.strip()
    if not label:
        raise SystemExit(f"Empty world label: {raw}")
    return label, Path(path.strip())


def read_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def summarize_world(label: str, path: Path) -> dict:
    rows = read_rows(path)
    numeric = {
        field: [_float(row.get(field)) for row in rows]
        for field in NUMERIC_FIELDS
    }
    carried_rows = [row for row in rows if _float(row.get("passive_carrying_nearness")) > 0.0]
    positive_carried_cos_rows = [row for row in rows if _float(row.get("carried_kinship_cosine")) > 0.0]
    strongest = sorted(
        rows,
        key=lambda row: (
            _float(row.get("passive_carrying_nearness")),
            _float(row.get("carried_kinship_cosine")),
            _float(row.get("target_max_trade_readiness")),
        ),
        reverse=True,
    )[:8]
    return {
        "world": label,
        "source_file": str(path),
        "families": len(rows),
        "carry_signal_family_count": len(carried_rows),
        "positive_carried_cos_family_count": len(positive_carried_cos_rows),
        "avg_carry": round(sum(numeric["passive_carrying_nearness"]) / max(1, len(rows)), 6),
        "max_carry": round(max(numeric["passive_carrying_nearness"] or [0.0]), 6),
        "avg_carried_cos": round(sum(numeric["carried_kinship_cosine"]) / max(1, len(rows)), 6),
        "max_carried_cos": round(max(numeric["carried_kinship_cosine"] or [0.0]), 6),
        "avg_readiness": round(sum(numeric["target_max_trade_readiness"]) / max(1, len(rows)), 6),
        "max_readiness": round(max(numeric["target_max_trade_readiness"] or [0.0]), 6),
        "avg_inner_balance": round(sum(numeric["target_avg_neuro_balance"]) / max(1, len(rows)), 6),
        "avg_temporal_trust": round(sum(numeric["target_max_temporal_trust_support"]) / max(1, len(rows)), 6),
        "avg_temporal_caution": round(sum(numeric["target_max_temporal_caution_support"]) / max(1, len(rows)), 6),
        "strongest_families": [
            {
                "target_family": row.get("target_family", ""),
                "nearest_source": row.get("source_family", ""),
                "carried_source": row.get("carried_source_family", ""),
                "carry": round(_float(row.get("passive_carrying_nearness")), 6),
                "carried_cos": round(_float(row.get("carried_kinship_cosine")), 6),
                "readiness": round(_float(row.get("target_max_trade_readiness")), 6),
            }
            for row in strongest
        ],
    }


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda row: (row["avg_carry"], row["avg_carried_cos"], row["max_carry"]), reverse=True)
    report = {"worlds": rows}
    (output_dir / "passive_world_carrying_map.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    csv_rows = [
        {key: value for key, value in row.items() if key != "strongest_families"}
        for row in rows
    ]
    if csv_rows:
        with (output_dir / "passive_world_carrying_map.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(csv_rows)

    lines = ["MINI DIO PASSIVE WORLD CARRYING MAP", ""]
    for row in rows:
        lines.extend(
            [
                f"{row['world']}: families={row['families']} "
                f"carry_signal={row['carry_signal_family_count']} "
                f"positive_carried_cos={row['positive_carried_cos_family_count']} "
                f"avg_carry={row['avg_carry']:.6f} max_carry={row['max_carry']:.6f} "
                f"avg_carried_cos={row['avg_carried_cos']:.6f} max_carried_cos={row['max_carried_cos']:.6f} "
                f"avg_readiness={row['avg_readiness']:.6f}",
                "  strongest:",
            ]
        )
        for family in row["strongest_families"][:5]:
            lines.append(
                f"    {family['target_family']} -> carried={family['carried_source']} "
                f"carry={family['carry']:.6f} cos={family['carried_cos']:.6f} readiness={family['readiness']:.6f}"
            )
        lines.append("")
    (output_dir / "passive_world_carrying_map_summary.txt").write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini-DIO passive world carrying map")
    parser.add_argument("--world", action="append", required=True, help="label=kinship_transfer_csv")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = [summarize_world(label, path) for label, path in (parse_input(item) for item in args.world)]
    write_outputs(rows, Path(args.output))
    print(json.dumps({"worlds": len(rows)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
