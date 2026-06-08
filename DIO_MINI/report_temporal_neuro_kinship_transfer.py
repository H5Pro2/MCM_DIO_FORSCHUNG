"""Compare Mini-DIO families by passive sensory/MCM kinship across worlds.

This is a diagnostic report. It does not require identical family names.
Instead it compares averaged sehen/hoeren/fuehlen traces and shows which
source-world family is nearest to each target-world family.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


VECTOR_FIELDS = [
    "sehen_form_flow",
    "sehen_form_stability",
    "sehen_form_change",
    "hoeren_energy_tone",
    "hoeren_energy_shift",
    "fuehlen_mcm_coherence",
    "fuehlen_mcm_tension",
    "fuehlen_mcm_asymmetry",
]


def _float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _int(value: object, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def _run_number(path: Path) -> int:
    try:
        return int(path.name.rsplit("_", 1)[-1])
    except Exception:
        return 0


def load_episode_rows(debug_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv"), key=lambda p: _run_number(p.parent)):
        run = _run_number(path.parent)
        with path.open("r", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["run"] = run
                rows.append(item)
    return rows


def aggregate(rows: list[dict]) -> dict[str, dict]:
    families: dict[str, dict] = {}
    for row in rows:
        family = str(row.get("symbol_family", "-") or "-")
        item = families.setdefault(
            family,
            {
                "family": family,
                "rows": 0,
                "trades": 0,
                "tp": 0,
                "sl": 0,
                "reward_sum": 0.0,
                "vector_sums": {field: 0.0 for field in VECTOR_FIELDS},
                "neuro_balance_sum": 0.0,
                "max_trade_readiness": 0.0,
                "max_temporal_trust_support": 0.0,
                "max_temporal_caution_support": 0.0,
                "tone_counts": {},
            },
        )
        item["rows"] += 1
        action = str(row.get("action", "") or "").upper()
        if action in ("LONG", "SHORT"):
            item["trades"] += 1
        outcome = str(row.get("outcome_event", "") or "")
        item["tp"] += 1 if outcome == "TP" else 0
        item["sl"] += 1 if outcome == "SL" else 0
        item["reward_sum"] += _float(row.get("reward"))
        for field in VECTOR_FIELDS:
            item["vector_sums"][field] += _float(row.get(field))
        item["neuro_balance_sum"] += _float(row.get("mini_neuro_balance"))
        item["max_trade_readiness"] = max(float(item["max_trade_readiness"]), _float(row.get("trade_readiness")))
        item["max_temporal_trust_support"] = max(
            float(item["max_temporal_trust_support"]),
            _float(row.get("mini_temporal_trust_support")),
        )
        item["max_temporal_caution_support"] = max(
            float(item["max_temporal_caution_support"]),
            _float(row.get("mini_temporal_caution_support")),
        )
        tone = str(row.get("mini_neuro_dominant_tone", "-") or "-")
        item["tone_counts"][tone] = _int(item["tone_counts"].get(tone)) + 1

    for item in families.values():
        count = max(1, int(item["rows"]))
        item["vector"] = [float(item["vector_sums"][field]) / count for field in VECTOR_FIELDS]
        item["vector_map"] = {
            field: float(item["vector_sums"][field]) / count
            for field in VECTOR_FIELDS
        }
        item["avg_neuro_balance"] = float(item["neuro_balance_sum"]) / count
    return families


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm <= 0.0 or right_norm <= 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def euclidean_distance(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) * (a - b) for a, b in zip(left, right)))


def nearest_source_family(target: dict, sources: dict[str, dict], *, require_consequence: bool = False) -> dict:
    best: dict | None = None
    for source in sources.values():
        if require_consequence and _int(source.get("trades")) <= 0 and _float(source.get("reward_sum")) <= 0.0:
            continue
        cosine = cosine_similarity(target["vector"], source["vector"])
        distance = euclidean_distance(target["vector"], source["vector"])
        candidate = {
            "source_family": source["family"],
            "kinship_cosine": round(float(cosine), 6),
            "kinship_distance": round(float(distance), 6),
            "source_rows": int(source["rows"]),
            "source_trades": int(source["trades"]),
            "source_tp": int(source["tp"]),
            "source_sl": int(source["sl"]),
            "source_reward_sum": round(float(source["reward_sum"]), 6),
            "source_avg_neuro_balance": round(float(source["avg_neuro_balance"]), 6),
            "source_max_trade_readiness": round(float(source["max_trade_readiness"]), 6),
            "source_max_temporal_trust_support": round(float(source["max_temporal_trust_support"]), 6),
            "source_tones": dict(source["tone_counts"]),
            "source_vector": dict(source["vector_map"]),
        }
        if best is None:
            best = candidate
            continue
        if (candidate["kinship_cosine"], -candidate["kinship_distance"], candidate["source_rows"]) > (
            best["kinship_cosine"],
            -best["kinship_distance"],
            best["source_rows"],
        ):
            best = candidate
    return best or {}


def passive_carrying_nearness(target: dict, nearest: dict) -> dict:
    """Read passive carrying proximity without making it actionable.

    The value is a diagnostic compression of:
    - sensory/MCM kinship
    - real source-world consequence
    - target inner balance

    It is intentionally not used by Mini-DIO's action selection.
    """

    source_trades = max(0, _int(nearest.get("source_trades")))
    source_tp = max(0, _int(nearest.get("source_tp")))
    source_sl = max(0, _int(nearest.get("source_sl")))
    source_reward = _float(nearest.get("source_reward_sum"))
    kinship = max(0.0, min(1.0, (_float(nearest.get("kinship_cosine")) + 1.0) * 0.5))
    experience_weight = source_trades / (source_trades + 3.0) if source_trades > 0 else 0.0
    positive_rate = source_tp / source_trades if source_trades > 0 else 0.0
    negative_rate = source_sl / source_trades if source_trades > 0 else 0.0
    reward_support = max(0.0, source_reward) / (abs(source_reward) + 1.0) if source_reward != 0.0 else 0.0
    consequence_support = max(0.0, ((positive_rate * 0.65) + (reward_support * 0.35)) - (negative_rate * 0.45))
    target_balance = max(0.0, min(1.0, (_float(target.get("avg_neuro_balance")) + 1.0) * 0.5))
    carrying = kinship * consequence_support * experience_weight * (0.55 + (target_balance * 0.45))
    return {
        "source_experience_weight": round(float(experience_weight), 6),
        "source_consequence_support": round(float(consequence_support), 6),
        "target_inner_balance_support": round(float(target_balance), 6),
        "passive_carrying_nearness": round(float(carrying), 6),
    }


def build_report(source_rows: list[dict], target_rows: list[dict]) -> dict:
    sources = aggregate(source_rows)
    targets = aggregate(target_rows)
    rows = []
    for target in targets.values():
        nearest = nearest_source_family(target, sources)
        nearest_carried = nearest_source_family(target, sources, require_consequence=True)
        carrying = passive_carrying_nearness(target, nearest_carried)
        rows.append(
            {
                "target_family": target["family"],
                "target_rows": int(target["rows"]),
                "target_trades": int(target["trades"]),
                "target_tp": int(target["tp"]),
                "target_sl": int(target["sl"]),
                "target_reward_sum": round(float(target["reward_sum"]), 6),
                "target_avg_neuro_balance": round(float(target["avg_neuro_balance"]), 6),
                "target_max_trade_readiness": round(float(target["max_trade_readiness"]), 6),
                "target_max_temporal_trust_support": round(float(target["max_temporal_trust_support"]), 6),
                "target_max_temporal_caution_support": round(float(target["max_temporal_caution_support"]), 6),
                "target_tones": dict(target["tone_counts"]),
                "target_vector": dict(target["vector_map"]),
                **nearest,
                "carried_source_family": nearest_carried.get("source_family", ""),
                "carried_kinship_cosine": nearest_carried.get("kinship_cosine", 0.0),
                "carried_kinship_distance": nearest_carried.get("kinship_distance", 0.0),
                "carried_source_rows": nearest_carried.get("source_rows", 0),
                "carried_source_trades": nearest_carried.get("source_trades", 0),
                "carried_source_tp": nearest_carried.get("source_tp", 0),
                "carried_source_sl": nearest_carried.get("source_sl", 0),
                "carried_source_reward_sum": nearest_carried.get("source_reward_sum", 0.0),
                "carried_source_max_trade_readiness": nearest_carried.get("source_max_trade_readiness", 0.0),
                "carried_source_max_temporal_trust_support": nearest_carried.get(
                    "source_max_temporal_trust_support",
                    0.0,
                ),
                **carrying,
            }
        )
    rows.sort(
        key=lambda item: (
            item.get("kinship_cosine", 0.0),
            item.get("carried_kinship_cosine", 0.0),
            item.get("passive_carrying_nearness", 0.0),
            -item.get("kinship_distance", 999.0),
            item.get("source_reward_sum", 0.0),
            item.get("target_rows", 0),
        ),
        reverse=True,
    )
    return {
        "source_rows_scanned": len(source_rows),
        "target_rows_scanned": len(target_rows),
        "source_families": len(sources),
        "target_families": len(targets),
        "vector_fields": VECTOR_FIELDS,
        "families": rows,
        "top_families": rows[:20],
    }


def write_outputs(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "temporal_neuro_kinship_transfer_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    rows = list(report.get("families", []) or [])
    if rows:
        csv_rows = []
        for row in rows:
            csv_row = dict(row)
            csv_row["target_tones"] = json.dumps(csv_row.get("target_tones", {}), sort_keys=True)
            csv_row["source_tones"] = json.dumps(csv_row.get("source_tones", {}), sort_keys=True)
            csv_row["target_vector"] = json.dumps(csv_row.get("target_vector", {}), sort_keys=True)
            csv_row["source_vector"] = json.dumps(csv_row.get("source_vector", {}), sort_keys=True)
            csv_rows.append(csv_row)
        with (output_dir / "temporal_neuro_kinship_transfer.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(csv_rows)
    lines = [
        "MINI DIO TEMPORAL/NEURO KINSHIP TRANSFER",
        f"source_rows={report.get('source_rows_scanned', 0)} target_rows={report.get('target_rows_scanned', 0)}",
        f"source_families={report.get('source_families', 0)} target_families={report.get('target_families', 0)}",
        f"vector_fields={','.join(report.get('vector_fields', []))}",
        "",
        "TOP TARGET FAMILIES BY NEAREST SOURCE KINSHIP",
    ]
    for row in report.get("top_families", []) or []:
        lines.append(
            f"{row['target_family']} -> {row.get('source_family', '-')}: "
            f"cos={row.get('kinship_cosine', 0.0):.6f} dist={row.get('kinship_distance', 0.0):.6f} "
            f"target_rows={row['target_rows']} target_trades={row['target_trades']} "
            f"target_readiness={row['target_max_trade_readiness']:.6f} "
            f"source_trades={row.get('source_trades', 0)} source_tp={row.get('source_tp', 0)} "
            f"source_reward={row.get('source_reward_sum', 0.0):.6f} "
            f"carried={row.get('carried_source_family', '-')}:"
            f"{row.get('carried_kinship_cosine', 0.0):.6f} "
            f"carrying_near={row.get('passive_carrying_nearness', 0.0):.6f}"
        )
    (output_dir / "temporal_neuro_kinship_transfer_summary.txt").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini-DIO passive kinship transfer report")
    parser.add_argument("--source-debug-root", required=True)
    parser.add_argument("--target-debug-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report(
        load_episode_rows(Path(args.source_debug_root)),
        load_episode_rows(Path(args.target_debug_root)),
    )
    write_outputs(report, Path(args.output))
    print(
        json.dumps(
            {
                "source_rows_scanned": report["source_rows_scanned"],
                "target_rows_scanned": report["target_rows_scanned"],
                "source_families": report["source_families"],
                "target_families": report["target_families"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
