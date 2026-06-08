"""Build a passive inner maturity map for Mini-DIO.

The map translates passive maturity-bridge diagnostics into inner reading
seeds. It is deliberately separated from action and memory training.
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


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _inner_seed(state: str) -> str:
    if state == "passive_observation_has_carried_neighbor":
        return "inner_trust_seed"
    if state == "passive_observation_has_burdened_neighbor":
        return "inner_carefulness_seed"
    if state == "passive_observation_has_mixed_neighbors":
        return "inner_reorganization_seed"
    return "inner_open_observation_seed"


def _inner_sentence(row: dict, seed: str) -> str:
    passive = str(row.get("passive_family_action", "") or "-")
    neighbor = str(row.get("best_real_family_action", "") or "-")
    similarity = _safe_float(row.get("best_similarity"))
    reward = _safe_float(row.get("best_real_reward_sum"))
    if seed == "inner_trust_seed":
        return (
            f"{passive}: Ich habe diese Form passiv gesehen. "
            f"Eine nahe reale Spur {neighbor} wurde getragen "
            f"(Naehe={similarity:.6f}, Konsequenz={reward:.6f})."
        )
    if seed == "inner_carefulness_seed":
        return (
            f"{passive}: Ich habe diese Form passiv gesehen. "
            f"Eine nahe reale Spur {neighbor} wurde belastet "
            f"(Naehe={similarity:.6f}, Konsequenz={reward:.6f})."
        )
    if seed == "inner_reorganization_seed":
        return (
            f"{passive}: Ich habe diese Form passiv gesehen. "
            f"Nahe reale Spuren waren gemischt. "
            f"Diese Familie braucht Reorganisation statt direkte Handlung."
        )
    return f"{passive}: Ich habe diese Form passiv gesehen. Die innere Bedeutung bleibt offen."


def build_map(source_path: Path) -> tuple[list[dict], list[dict]]:
    rows = _read_csv(source_path)
    detail: list[dict] = []
    by_seed: dict[str, dict] = {}

    for row in rows:
        state = str(row.get("passive_maturity_state", "") or "")
        seed = _inner_seed(state)
        item = {
            "source_label": str(row.get("source_label", "") or ""),
            "passive_family_action": str(row.get("passive_family_action", "") or ""),
            "action": str(row.get("action", "") or ""),
            "inner_maturity_seed": seed,
            "passive_maturity_state": state,
            "candidate_count": _safe_int(row.get("candidate_count")),
            "best_similarity": round(_safe_float(row.get("best_similarity")), 9),
            "best_sensory_similarity": round(_safe_float(row.get("best_sensory_similarity")), 9),
            "best_mcm_similarity": round(_safe_float(row.get("best_mcm_similarity")), 9),
            "best_real_family_action": str(row.get("best_real_family_action", "") or ""),
            "best_real_reward_sum": round(_safe_float(row.get("best_real_reward_sum")), 9),
            "best_real_tp_count": _safe_int(row.get("best_real_tp_count")),
            "best_real_sl_count": _safe_int(row.get("best_real_sl_count")),
            "carried_candidate_count": _safe_int(row.get("carried_candidate_count")),
            "burdened_candidate_count": _safe_int(row.get("burdened_candidate_count")),
            "mixed_candidate_count": _safe_int(row.get("mixed_candidate_count")),
            "inner_sentence": "",
            "passive_only": 1,
        }
        item["inner_sentence"] = _inner_sentence(item, seed)
        detail.append(item)

        bucket = by_seed.setdefault(
            seed,
            {
                "inner_maturity_seed": seed,
                "trace_count": 0,
                "source_count": 0,
                "sources": set(),
                "actions": set(),
                "families": set(),
                "avg_similarity_sum": 0.0,
                "avg_mcm_similarity_sum": 0.0,
                "real_reward_sum": 0.0,
            },
        )
        bucket["trace_count"] += 1
        bucket["sources"].add(item["source_label"])
        bucket["actions"].add(item["action"])
        bucket["families"].add(item["passive_family_action"])
        bucket["avg_similarity_sum"] += item["best_similarity"]
        bucket["avg_mcm_similarity_sum"] += item["best_mcm_similarity"]
        bucket["real_reward_sum"] += item["best_real_reward_sum"]

    summary: list[dict] = []
    for bucket in by_seed.values():
        count = max(1, int(bucket["trace_count"]))
        sources = set(bucket["sources"])
        item = {
            "inner_maturity_seed": bucket["inner_maturity_seed"],
            "trace_count": count,
            "source_count": len(sources),
            "sources": ",".join(sorted(sources)),
            "actions": ",".join(sorted(bucket["actions"])),
            "families": ",".join(sorted(bucket["families"])),
            "avg_similarity": round(float(bucket["avg_similarity_sum"]) / count, 9),
            "avg_mcm_similarity": round(float(bucket["avg_mcm_similarity_sum"]) / count, 9),
            "real_reward_sum": round(float(bucket["real_reward_sum"]), 9),
            "passive_only": 1,
        }
        summary.append(item)

    detail.sort(key=lambda item: (str(item["source_label"]), str(item["inner_maturity_seed"]), str(item["passive_family_action"])))
    summary.sort(key=lambda item: (-int(item["trace_count"]), str(item["inner_maturity_seed"])))
    return detail, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(detail: list[dict], summary: list[dict], source_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_inner_maturity_map.csv"
    summary_csv = output_dir / "dio_mini_passive_inner_maturity_map_summary.csv"
    json_path = output_dir / "dio_mini_passive_inner_maturity_map.json"
    md_path = output_dir / "dio_mini_passive_inner_maturity_map.md"
    txt_path = output_dir / "dio_mini_passive_inner_maturity_map.txt"

    _write_csv(detail_csv, detail, ["source_label", "passive_family_action", "inner_maturity_seed"])
    _write_csv(summary_csv, summary, ["inner_maturity_seed", "trace_count", "source_count"])
    json_path.write_text(
        json.dumps(
            {
                "source": str(source_path),
                "detail": detail,
                "summary": summary,
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

    lines = ["# DIO Mini Passive Inner Maturity Map", "", f"- source: {source_path}", ""]
    lines.append("## Keime")
    if not summary:
        lines.append("- keine passiven Reifekeime")
    for row in summary:
        lines.append(
            f"- {row['inner_maturity_seed']}: traces={row['trace_count']} "
            f"sources={row['source_count']} actions={row['actions']} "
            f"avg_similarity={row['avg_similarity']} avg_mcm={row['avg_mcm_similarity']} "
            f"reward_sum={row['real_reward_sum']}"
        )
    lines.extend(["", "## Innensaetze"])
    if not detail:
        lines.append("- keine Innensaetze")
    for row in detail:
        lines.append(f"- {row['inner_sentence']}")
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Innenzustands-Landkarte",
            "- keine Handlung",
            "- kein Trainingsmemory",
            "- kein Gate",
            "- kein Zukunftslehrer",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    txt_path.write_text("\n".join(row["inner_sentence"] for row in detail), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO inner maturity map")
    parser.add_argument("--maturity-summary", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    source_path = Path(args.maturity_summary)
    detail, summary = build_map(source_path)
    write_outputs(detail, summary, source_path, Path(args.output_dir))
    print(f"passive_inner_maturity_map_rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['inner_maturity_seed']} traces={row['trace_count']} "
            f"sources={row['source_count']} actions={row['actions']}"
        )


if __name__ == "__main__":
    main()
