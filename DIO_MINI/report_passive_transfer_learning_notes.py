"""Build passive Mini-DIO transfer learning notes.

The notes translate transfer maturity into a compact inner reading:

- similar and carried
- similar and only observed
- similar but not action-mature
- similar and burdened

This is not memory for action. It writes only diagnostic note files.
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


def _note_kind(state: str) -> str:
    if state == "transfer_reife_carried_same_consequence":
        return "note_similar_and_carried"
    if state == "transfer_reife_carried_same_trust":
        return "note_similar_and_trust_carried"
    if state == "transfer_reife_family_carried_observation_dominant":
        return "note_similar_family_carried_but_observed"
    if state == "transfer_reife_burden_same_consequence":
        return "note_similar_and_burdened"
    if state == "transfer_reife_quiet_same_consequence":
        return "note_similar_and_quiet"
    if state == "transfer_reife_form_near_trust_not_carried":
        return "note_similar_but_not_action_mature"
    if state == "transfer_reife_variant_continues":
        return "note_variant_continues"
    return "note_transfer_open"


def _inner_note(row: dict, kind: str) -> str:
    left = str(row.get("left_family", "") or "-")
    right = str(row.get("right_family", "") or "-")
    similarity = _safe_float(row.get("sensory_mcm_similarity"))
    left_action = str(row.get("left_action", "") or "-")
    right_action = str(row.get("right_action", "") or "-")
    left_outcome = str(row.get("left_outcome", "") or "-")
    right_outcome = str(row.get("right_outcome", "") or "-")
    if kind == "note_similar_and_carried":
        return (
            f"{left} erinnert an {right}: aehnliche Sinnes-/MCM-Lage, "
            f"und die Konsequenz wurde wieder getragen ({left_action}/{left_outcome} -> {right_action}/{right_outcome})."
        )
    if kind == "note_similar_family_carried_but_observed":
        return (
            f"{left} erinnert an {right}: die Familie traegt Potenzial, "
            f"aber dominant wurde beobachtet. Noch keine saubere Handlungsreife."
        )
    if kind == "note_similar_and_burdened":
        return (
            f"{left} erinnert an {right}: aehnliche Lage und wieder belastende Konsequenz. "
            f"Diese Spur soll vorsichtig gelesen werden."
        )
    if kind == "note_similar_and_quiet":
        return f"{left} erinnert an {right}: aehnliche Lage bleibt ruhig beobachtend."
    if kind == "note_similar_but_not_action_mature":
        return (
            f"{left} erinnert stark an {right} (Naehe {similarity:.6f}), "
            f"aber Handlung und Konsequenz tragen nicht mit. Aehnlichkeit ist hier keine Handlungsreife."
        )
    if kind == "note_variant_continues":
        return f"{left} erinnert an {right}: Variantenwahrnehmung setzt sich fort."
    return f"{left} erinnert an {right}: Transfer bleibt passiv offen."


def build_rows(transfer_csv: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    summary: dict[str, dict] = {}
    for row in _read_csv(transfer_csv):
        state = str(row.get("transfer_reife_state", "") or "")
        kind = _note_kind(state)
        item = {
            "left_family": str(row.get("left_family", "") or ""),
            "right_family": str(row.get("right_family", "") or ""),
            "learning_note_kind": kind,
            "transfer_reife_state": state,
            "transfer_reife": round(_safe_float(row.get("transfer_reife")), 9),
            "sensory_mcm_similarity": round(_safe_float(row.get("sensory_mcm_similarity")), 9),
            "event_reward_relation": str(row.get("event_reward_relation", "") or ""),
            "potential_reward_relation": str(row.get("potential_reward_relation", "") or ""),
            "left_action": str(row.get("left_action", "") or ""),
            "right_action": str(row.get("right_action", "") or ""),
            "left_outcome": str(row.get("left_outcome", "") or ""),
            "right_outcome": str(row.get("right_outcome", "") or ""),
            "left_event_reward_sum": round(_safe_float(row.get("left_event_reward_sum")), 6),
            "right_event_reward_sum": round(_safe_float(row.get("right_event_reward_sum")), 6),
            "left_potential_reward_sum": round(_safe_float(row.get("left_reward_sum")), 6),
            "right_potential_reward_sum": round(_safe_float(row.get("right_reward_sum")), 6),
            "inner_learning_note": "",
            "passive_only": 1,
        }
        item["inner_learning_note"] = _inner_note(item, kind)
        detail.append(item)

        bucket = summary.setdefault(
            kind,
            {
                "learning_note_kind": kind,
                "note_count": 0,
                "avg_transfer_reife": 0.0,
                "avg_similarity": 0.0,
                "pairs": [],
            },
        )
        bucket["note_count"] += 1
        bucket["avg_transfer_reife"] += item["transfer_reife"]
        bucket["avg_similarity"] += item["sensory_mcm_similarity"]
        bucket["pairs"].append(f"{item['left_family']}->{item['right_family']}")

    detail.sort(key=lambda item: (-float(item["transfer_reife"]), str(item["learning_note_kind"]), str(item["left_family"])))
    summary_rows = []
    for row in summary.values():
        count = max(1, int(row["note_count"]))
        row["avg_transfer_reife"] = round(float(row["avg_transfer_reife"]) / count, 9)
        row["avg_similarity"] = round(float(row["avg_similarity"]) / count, 9)
        row["pairs"] = ",".join(sorted(row["pairs"]))
        summary_rows.append(row)
    summary_rows.sort(key=lambda item: (-float(item["avg_transfer_reife"]), str(item["learning_note_kind"])))
    return detail, summary_rows


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, transfer_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_transfer_learning_notes.csv"
    summary_csv = output_dir / "dio_mini_passive_transfer_learning_notes_summary.csv"
    json_path = output_dir / "dio_mini_passive_transfer_learning_notes.json"
    md_path = output_dir / "dio_mini_passive_transfer_learning_notes.md"
    txt_path = output_dir / "dio_mini_passive_transfer_learning_notes.txt"

    detail_fields = list(detail[0].keys()) if detail else ["left_family", "right_family", "learning_note_kind"]
    with detail_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else ["learning_note_kind", "note_count"]
    with summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "source": str(transfer_csv),
                "detail": detail,
                "summary": summary,
                "boundary": {
                    "writes_training_memory": False,
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

    lines = ["# DIO Mini Passive Transfer Learning Notes", "", f"- source: {transfer_csv}", ""]
    lines.append("## Zusammenfassung")
    if not summary:
        lines.append("- keine Lernnotizen")
    for row in summary:
        lines.append(
            f"- {row['learning_note_kind']}: notes={row['note_count']} "
            f"avg_transfer_reife={row['avg_transfer_reife']} avg_similarity={row['avg_similarity']} "
            f"pairs={row['pairs'] or '-'}"
        )
    lines.extend(["", "## Notizen"])
    txt_lines = []
    for row in detail:
        note = str(row["inner_learning_note"])
        lines.append(f"- {row['left_family']} -> {row['right_family']}: {row['learning_note_kind']}")
        lines.append(f"  {note}")
        txt_lines.append(note)
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Lernnotiz",
            "- kein Trainingsmemory",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    txt_path.write_text("\n".join(txt_lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO transfer learning notes")
    parser.add_argument("--transfer-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, summary = build_rows(Path(args.transfer_csv))
    write_outputs(detail, summary, Path(args.output_dir), Path(args.transfer_csv))
    print(f"passive_transfer_learning_notes={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['learning_note_kind']} notes={row['note_count']} "
            f"avg_transfer_reife={row['avg_transfer_reife']}"
        )


if __name__ == "__main__":
    main()
