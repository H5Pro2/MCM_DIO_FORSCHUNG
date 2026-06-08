"""Build passive transfer maturity from Mini-DIO family vector kinship.

The report reads the best passive kinship pairs and separates:

- sensory/MCM similarity
- action continuity
- consequence continuity
- reward alignment

It is diagnostic only. It writes no memory, does not influence action, and is
not a gate.
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


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _reward_relation(left_reward: float, right_reward: float) -> str:
    if left_reward > 0.0 and right_reward > 0.0:
        return "positive_to_positive"
    if left_reward < 0.0 and right_reward < 0.0:
        return "negative_to_negative"
    if left_reward == 0.0 and right_reward == 0.0:
        return "neutral_to_neutral"
    if left_reward > 0.0 and right_reward == 0.0:
        return "positive_to_neutral"
    if left_reward == 0.0 and right_reward > 0.0:
        return "neutral_to_positive"
    if left_reward < 0.0 and right_reward == 0.0:
        return "negative_to_neutral"
    if left_reward == 0.0 and right_reward < 0.0:
        return "neutral_to_negative"
    if left_reward > 0.0 and right_reward < 0.0:
        return "positive_to_negative"
    if left_reward < 0.0 and right_reward > 0.0:
        return "negative_to_positive"
    return "mixed"


def _reward_alignment(left_reward: float, right_reward: float) -> float:
    if left_reward == 0.0 and right_reward == 0.0:
        return 0.5
    if left_reward == 0.0 or right_reward == 0.0:
        return 0.35
    if (left_reward > 0.0 and right_reward > 0.0) or (left_reward < 0.0 and right_reward < 0.0):
        scale = max(abs(left_reward), abs(right_reward), 1.0)
        return _clip01(1.0 - (abs(abs(left_reward) - abs(right_reward)) / scale))
    return 0.0


def _transfer_state(row: dict, event_relation: str, potential_relation: str) -> str:
    same_action = _safe_int(row.get("same_action")) == 1
    same_outcome = _safe_int(row.get("same_outcome")) == 1
    left_class = str(row.get("left_state_class", "") or "")
    right_class = str(row.get("right_state_class", "") or "")
    left_outcome = str(row.get("left_outcome", "") or "").upper()
    right_outcome = str(row.get("right_outcome", "") or "").upper()
    if same_action and same_outcome and left_outcome == right_outcome == "NO_TRADE" and event_relation == "positive_to_positive":
        return "transfer_reife_family_carried_observation_dominant"
    if same_action and same_outcome and event_relation == "positive_to_positive":
        if left_class == right_class == "trust":
            return "transfer_reife_carried_same_trust"
        return "transfer_reife_carried_same_consequence"
    if same_action and same_outcome and event_relation == "negative_to_negative":
        return "transfer_reife_burden_same_consequence"
    if same_action and same_outcome and event_relation == "neutral_to_neutral" and potential_relation == "positive_to_positive":
        return "transfer_reife_observed_potential_same_consequence"
    if same_action and same_outcome and event_relation == "neutral_to_neutral":
        return "transfer_reife_quiet_same_consequence"
    if same_action and not same_outcome:
        return "transfer_reife_action_same_consequence_changed"
    if not same_action and same_outcome:
        return "transfer_reife_consequence_same_action_changed"
    if left_class == "trust" and right_class in {"quiet", "single"}:
        return "transfer_reife_form_near_trust_not_carried"
    if left_class == "variant" and right_class == "variant":
        return "transfer_reife_variant_continues"
    return "transfer_reife_open"


def _transfer_score(
    similarity: float,
    same_action: int,
    same_outcome: int,
    event_alignment: float,
    potential_alignment: float,
    same_state_class: int,
) -> float:
    return round(
        _clip01(
            (similarity * 0.38)
            + (float(same_action) * 0.18)
            + (float(same_outcome) * 0.20)
            + (event_alignment * 0.14)
            + (potential_alignment * 0.04)
            + (float(same_state_class) * 0.06)
        ),
        9,
    )


def _sentence(row: dict) -> str:
    return (
        f"{row['left_family']} -> {row['right_family']}: transfer_reife={float(row['transfer_reife']):.6f}; "
        f"sinnesnaehe={float(row['sensory_mcm_similarity']):.6f}; "
        f"aktion={row['left_action']}->{row['right_action']}; "
        f"konsequenz={row['left_outcome']}->{row['right_outcome']}; "
        f"event_reward={float(row['left_event_reward_sum']):.6f}->{float(row['right_event_reward_sum']):.6f}; "
        f"potential_reward={float(row['left_reward_sum']):.6f}->{float(row['right_reward_sum']):.6f}."
    )


def build_rows(kinship_best_csv: Path) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    summary_bucket: dict[str, dict] = {}
    for source in _read_csv(kinship_best_csv):
        left_reward = _safe_float(source.get("left_reward_sum"))
        right_reward = _safe_float(source.get("right_reward_sum"))
        left_event_reward = _safe_float(source.get("left_event_reward_sum"))
        right_event_reward = _safe_float(source.get("right_event_reward_sum"))
        potential_relation = _reward_relation(left_reward, right_reward)
        event_relation = _reward_relation(left_event_reward, right_event_reward)
        potential_alignment = _reward_alignment(left_reward, right_reward)
        event_alignment = _reward_alignment(left_event_reward, right_event_reward)
        same_action = _safe_int(source.get("same_action"))
        same_outcome = _safe_int(source.get("same_outcome"))
        same_state_class = _safe_int(source.get("same_state_class"))
        similarity = _safe_float(source.get("similarity"))
        state = _transfer_state(source, event_relation, potential_relation)
        item = {
            "left_family": str(source.get("left_family", "") or ""),
            "right_family": str(source.get("right_family", "") or ""),
            "transfer_reife_state": state,
            "transfer_reife": _transfer_score(
                similarity,
                same_action,
                same_outcome,
                event_alignment,
                potential_alignment,
                same_state_class,
            ),
            "sensory_mcm_similarity": round(similarity, 9),
            "distance": round(_safe_float(source.get("distance")), 9),
            "same_action": same_action,
            "same_outcome": same_outcome,
            "same_state_class": same_state_class,
            "event_reward_relation": event_relation,
            "event_reward_alignment": round(event_alignment, 9),
            "potential_reward_relation": potential_relation,
            "potential_reward_alignment": round(potential_alignment, 9),
            "left_state_class": str(source.get("left_state_class", "") or ""),
            "right_state_class": str(source.get("right_state_class", "") or ""),
            "left_landkarte_state": str(source.get("left_landkarte_state", "") or ""),
            "right_landkarte_state": str(source.get("right_landkarte_state", "") or ""),
            "left_reflection_state": str(source.get("left_reflection_state", "") or ""),
            "right_reflection_state": str(source.get("right_reflection_state", "") or ""),
            "left_action": str(source.get("left_action", "") or ""),
            "right_action": str(source.get("right_action", "") or ""),
            "left_outcome": str(source.get("left_outcome", "") or ""),
            "right_outcome": str(source.get("right_outcome", "") or ""),
            "left_reward_sum": round(left_reward, 6),
            "right_reward_sum": round(right_reward, 6),
            "left_event_reward_sum": round(left_event_reward, 6),
            "right_event_reward_sum": round(right_event_reward, 6),
            "passive_only": 1,
        }
        item["transfer_sentence"] = _sentence(item)
        rows.append(item)
        bucket = summary_bucket.setdefault(
            state,
            {
                "transfer_reife_state": state,
                "family_count": 0,
                "avg_transfer_reife": 0.0,
                "avg_similarity": 0.0,
                "same_action_count": 0,
                "same_outcome_count": 0,
                "families": [],
            },
        )
        bucket["family_count"] += 1
        bucket["avg_transfer_reife"] += float(item["transfer_reife"])
        bucket["avg_similarity"] += similarity
        bucket["same_action_count"] += same_action
        bucket["same_outcome_count"] += same_outcome
        bucket["families"].append(f"{item['left_family']}->{item['right_family']}")

    rows.sort(key=lambda item: (-float(item["transfer_reife"]), str(item["transfer_reife_state"]), str(item["left_family"])))
    summary: list[dict] = []
    for item in summary_bucket.values():
        count = max(1, int(item["family_count"]))
        item["avg_transfer_reife"] = round(float(item["avg_transfer_reife"]) / count, 9)
        item["avg_similarity"] = round(float(item["avg_similarity"]) / count, 9)
        item["families"] = ",".join(sorted(item["families"]))
        summary.append(item)
    summary.sort(key=lambda item: (-float(item["avg_transfer_reife"]), str(item["transfer_reife_state"])))
    return rows, summary


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path, kinship_best_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_transfer_reife.csv"
    summary_csv = output_dir / "dio_mini_passive_transfer_reife_summary.csv"
    json_path = output_dir / "dio_mini_passive_transfer_reife.json"
    md_path = output_dir / "dio_mini_passive_transfer_reife.md"

    detail_fields = list(rows[0].keys()) if rows else ["left_family", "right_family", "transfer_reife_state"]
    with detail_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(rows)

    summary_fields = list(summary[0].keys()) if summary else ["transfer_reife_state", "family_count"]
    with summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "source": str(kinship_best_csv),
                "detail": rows,
                "summary": summary,
                "boundary": {
                    "writes_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "uses_hard_threshold": False,
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Transfer Reife", "", f"- source: {kinship_best_csv}", ""]
    lines.append("## Zusammenfassung")
    if not summary:
        lines.append("- keine Transferdaten")
    for row in summary:
        lines.append(
            f"- {row['transfer_reife_state']}: families={row['family_count']} "
            f"avg_transfer_reife={row['avg_transfer_reife']} avg_similarity={row['avg_similarity']} "
            f"same_action={row['same_action_count']} same_outcome={row['same_outcome_count']} "
            f"pairs={row['families'] or '-'}"
        )
    lines.extend(["", "## Paare"])
    for row in rows:
        lines.append(
            f"- {row['left_family']} -> {row['right_family']}: {row['transfer_reife_state']}; "
            f"transfer_reife={float(row['transfer_reife']):.6f}; "
            f"similarity={float(row['sensory_mcm_similarity']):.6f}; "
            f"event_relation={row['event_reward_relation']}; "
            f"potential_relation={row['potential_reward_relation']}"
        )
        lines.append(f"  {row['transfer_sentence']}")
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Transferreife",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
            "- Sinnesnaehe und Handlungsreife bleiben getrennt",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO transfer maturity")
    parser.add_argument("--kinship-best-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rows, summary = build_rows(Path(args.kinship_best_csv))
    write_outputs(rows, summary, Path(args.output_dir), Path(args.kinship_best_csv))
    print(f"passive_transfer_reife_rows={len(rows)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['transfer_reife_state']} families={row['family_count']} "
            f"avg_transfer_reife={row['avg_transfer_reife']}"
        )


if __name__ == "__main__":
    main()
