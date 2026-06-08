"""Report passive open maturity transfer into a related variant world.

The report joins passive open maturity inner-awareness with a family-vector
kinship report. It answers whether a passively carried trace keeps its inner
reading only under identical repetition or also finds a sensory/MCM relative in
a variant world.

Diagnostic only:
- no memory writes
- no action influence
- no gate
- no motorics
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
        return 0.0
    return value


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _left_family_from_awareness(row: dict) -> str:
    family = str(row.get("symbol_family", "") or "")
    if family:
        return family
    family_action = str(row.get("family_action", "") or "")
    return family_action.split(":", 1)[0]


def _load_awareness(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for row in _read_csv(path):
        family = _left_family_from_awareness(row)
        if family:
            rows[family] = row
    return rows


def _load_kinship_best(path: Path) -> dict[str, dict]:
    return {
        str(row.get("left_family", "") or ""): row
        for row in _read_csv(path)
        if str(row.get("left_family", "") or "")
    }


def _transfer_state(awareness: dict, kinship: dict | None) -> str:
    if not kinship:
        return "no_variant_relative_seen"
    left_action = str(kinship.get("left_action", "") or "")
    right_action = str(kinship.get("right_action", "") or "")
    left_outcome = str(kinship.get("left_outcome", "") or "")
    right_outcome = str(kinship.get("right_outcome", "") or "")
    if left_action == right_action and left_outcome == right_outcome:
        return "variant_keeps_action_and_outcome"
    if left_action == right_action:
        return "variant_keeps_action_but_outcome_changes"
    if left_outcome == right_outcome:
        return "variant_changes_action_but_outcome_class_matches"
    if right_action == "WAIT":
        return "variant_relative_seen_as_observation"
    return "variant_relative_seen_with_changed_action"


def _sentence(row: dict) -> str:
    state = str(row.get("variant_transfer_state", "") or "")
    left = str(row.get("family_action", "") or row.get("left_family", "-") or "-")
    right = str(row.get("right_family", "-") or "-")
    similarity = _safe_float(row.get("similarity"))
    if state == "variant_relative_seen_as_observation":
        return (
            f"{left}: In der Variante wird eine nahe Sinnes-/MCM-Verwandtschaft zu {right} gesehen "
            f"(similarity={similarity:.6f}), aber sie bleibt Beobachtung statt Handlung."
        )
    if state == "variant_keeps_action_and_outcome":
        return (
            f"{left}: In der Variante bleibt die verwandte Spur auch in Aktion und Outcome gekoppelt "
            f"(similarity={similarity:.6f})."
        )
    if state == "no_variant_relative_seen":
        return f"{left}: In der Variante wurde keine verwandte Spur im Kinship-Bericht gefunden."
    return (
        f"{left}: In der Variante wird {right} als verwandte Spur gesehen "
        f"(similarity={similarity:.6f}), aber Aktion/Outcome verschieben sich."
    )


def build_rows(awareness_csv: Path, kinship_best_csv: Path) -> tuple[list[dict], list[dict]]:
    awareness = _load_awareness(awareness_csv)
    kinship = _load_kinship_best(kinship_best_csv)
    detail: list[dict] = []
    summary: dict[str, dict] = {}

    for left_family, awareness_row in sorted(awareness.items()):
        kinship_row = kinship.get(left_family)
        state = _transfer_state(awareness_row, kinship_row)
        row = {
            "family_action": str(awareness_row.get("family_action", "") or ""),
            "left_family": left_family,
            "inner_reife_awareness_state": str(awareness_row.get("inner_reife_awareness_state", "") or ""),
            "passive_reife_score": round(_safe_float(awareness_row.get("passive_reife_score")), 9),
            "left_event_reward_sum": round(_safe_float(awareness_row.get("event_reward_sum")), 9),
            "left_episode_count": str(awareness_row.get("episode_count", "") or ""),
            "right_family": str((kinship_row or {}).get("right_family", "") or ""),
            "similarity": round(_safe_float((kinship_row or {}).get("similarity")), 9),
            "distance": round(_safe_float((kinship_row or {}).get("distance")), 9),
            "left_action": str((kinship_row or {}).get("left_action", "") or ""),
            "right_action": str((kinship_row or {}).get("right_action", "") or ""),
            "left_outcome": str((kinship_row or {}).get("left_outcome", "") or ""),
            "right_outcome": str((kinship_row or {}).get("right_outcome", "") or ""),
            "right_reward_sum": round(_safe_float((kinship_row or {}).get("right_reward_sum")), 9),
            "right_event_reward_sum": round(_safe_float((kinship_row or {}).get("right_event_reward_sum")), 9),
            "same_action": int(str((kinship_row or {}).get("same_action", "0") or "0") == "1"),
            "same_outcome": int(str((kinship_row or {}).get("same_outcome", "0") or "0") == "1"),
            "variant_transfer_state": state,
            "passive_only": 1,
            "writes_training_memory": 0,
            "read_by_mini_dio": 0,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
        row["variant_transfer_sentence"] = _sentence(row)
        detail.append(row)
        bucket = summary.setdefault(
            state,
            {
                "variant_transfer_state": state,
                "count": 0,
                "avg_similarity_sum": 0.0,
                "right_event_reward_sum": 0.0,
                "families": [],
            },
        )
        bucket["count"] += 1
        bucket["avg_similarity_sum"] += _safe_float(row.get("similarity"))
        bucket["right_event_reward_sum"] += _safe_float(row.get("right_event_reward_sum"))
        bucket["families"].append(str(row.get("family_action", "") or left_family))

    summary_rows: list[dict] = []
    for row in summary.values():
        count = max(1, int(row["count"]))
        summary_rows.append(
            {
                "variant_transfer_state": row["variant_transfer_state"],
                "count": row["count"],
                "avg_similarity": round(float(row["avg_similarity_sum"]) / count, 9),
                "right_event_reward_sum": round(float(row["right_event_reward_sum"]), 9),
                "families": ",".join(sorted(row["families"])),
            }
        )
    summary_rows.sort(key=lambda item: (str(item["variant_transfer_state"]), str(item["families"])))
    detail.sort(key=lambda item: (str(item["variant_transfer_state"]), str(item["family_action"])))
    return detail, summary_rows


def _write_csv(path: Path, rows: list[dict], default_fields: list[str]) -> None:
    fields = list(default_fields)
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    output_dir: Path,
    awareness_csv: Path,
    kinship_best_csv: Path,
    detail: list[dict],
    summary: list[dict],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_open_reife_variant_transfer.csv"
    summary_csv = output_dir / "dio_mini_passive_open_reife_variant_transfer_summary.csv"
    json_path = output_dir / "dio_mini_passive_open_reife_variant_transfer.json"
    md_path = output_dir / "dio_mini_passive_open_reife_variant_transfer.md"

    _write_csv(detail_csv, detail, ["family_action", "variant_transfer_state", "similarity", "right_family"])
    _write_csv(summary_csv, summary, ["variant_transfer_state", "count", "avg_similarity"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_open_reife_variant_transfer.v1",
                "awareness_source": str(awareness_csv),
                "kinship_source": str(kinship_best_csv),
                "summary": summary,
                "detail": detail,
                "boundary": {
                    "passive_only": True,
                    "writes_training_memory": False,
                    "read_by_mini_dio": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Mini-DIO Passive Open Reife Variant Transfer",
        "",
        f"- awareness_source: `{awareness_csv}`",
        f"- kinship_source: `{kinship_best_csv}`",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine Transferdaten")
    for row in summary:
        lines.append(
            f"- {row['variant_transfer_state']}: count={row['count']} "
            f"avg_similarity={float(row['avg_similarity']):.6f} "
            f"right_reward={float(row['right_event_reward_sum']):.6f} "
            f"families={row['families'] or '-'}"
        )
    lines.extend(["", "## Detail"])
    for row in detail:
        lines.extend(
            [
                f"- {row['family_action']} -> {row['right_family'] or '-'}: {row['variant_transfer_state']}",
                f"  similarity={float(row['similarity']):.6f}; action={row['left_action']}->{row['right_action']}; outcome={row['left_outcome']}->{row['right_outcome']}; right_reward={float(row['right_event_reward_sum']):.6f}",
                f"  {row['variant_transfer_sentence']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Varianzdiagnose",
            "- keine Handlung",
            "- kein Gate",
            "- keine Motorik",
            "- kein Trainingsmemory",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--awareness", type=Path, required=True)
    parser.add_argument("--kinship-best", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    detail, summary = build_rows(args.awareness, args.kinship_best)
    write_outputs(args.output_dir, args.awareness, args.kinship_best, detail, summary)
    print(f"passive_open_reife_variant_transfer rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['variant_transfer_state']} count={row['count']} "
            f"avg_similarity={row['avg_similarity']} right_reward={row['right_event_reward_sum']}"
        )


if __name__ == "__main__":
    main()
