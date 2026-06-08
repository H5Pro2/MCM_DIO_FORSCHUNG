"""Rate passive open maturity candidates without changing Mini-DIO behavior.

The report combines:
- open maturity candidates,
- raw Mini-DIO episode traces,
- multisensory stability,
- consequence and temporal contact.

It is a passive diagnostic. It writes no memory and is not imported by the
action core.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SENSE_FIELDS = (
    "sehen_form_flow",
    "sehen_form_stability",
    "sehen_form_change",
    "hoeren_energy_tone",
    "hoeren_energy_shift",
    "fuehlen_mcm_coherence",
    "fuehlen_mcm_tension",
    "fuehlen_mcm_asymmetry",
)


def _safe_float(value: object) -> float:
    try:
        value = float(value or 0.0)
    except Exception:
        value = 0.0
    if value != value:
        return 0.0
    return value


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    if rows:
        ordered = list(fields)
        for row in rows:
            for key in row.keys():
                if key not in ordered:
                    ordered.append(key)
        fields = ordered
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _episode_files(root: Path) -> list[Path]:
    if root.is_file() and root.name == "episodes.csv":
        return [root]
    return sorted(root.glob("**/episodes.csv"))


def _mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _stability(values: list[float], scale: float = 2.0) -> float:
    if len(values) <= 1:
        return 1.0 if values else 0.0
    avg = _mean(values)
    variance = _mean([(value - avg) ** 2 for value in values])
    spread = variance ** 0.5
    return max(0.0, min(1.0, 1.0 - (spread / max(1e-9, scale))))


def _candidate_rows(path: Path) -> list[dict]:
    return [
        row
        for row in _read_csv(path)
        if str(row.get("open_reife_candidate_state", "") or "") == "open_inner_reife_candidate"
    ]


def _load_episode_rows(sources: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for root in sources:
        for episode_path in _episode_files(root):
            source_label = root.name
            run_label = episode_path.parent.name
            for row in _read_csv(episode_path):
                item = dict(row)
                item["_source_root"] = source_label
                item["_run_label"] = run_label
                rows.append(item)
    return rows


def _rating_state(score: float, consequence: float, multisensory: float, recurrence: float) -> str:
    """Return a descriptive state, not an action boundary.

    The numeric score remains continuous. The state only says whether the
    trace was carried, burdened, or still open; it is not a maturity gate.
    """

    if consequence <= 0.0:
        return "passive_reife_burden_or_open_candidate"
    return "passive_reife_carried_candidate"


def _note(row: dict) -> str:
    family_action = str(row.get("family_action", "") or "-")
    state = str(row.get("passive_reife_rating_state", "") or "-")
    if state == "passive_reife_carried_candidate":
        return (
            f"{family_action}: wiederkehrend getragen und multisensorisch ausreichend stabil. "
            "Passiv als innere Reife-Kandidatur lesbar; der Score bleibt kontinuierlich."
        )
    return f"{family_action}: keine getragene Reife-Kandidatur oder noch offene Konsequenz."


def build_rating(candidate_path: Path, episode_sources: list[Path]) -> tuple[list[dict], list[dict]]:
    candidates = _candidate_rows(candidate_path)
    episodes = _load_episode_rows(episode_sources)
    detail: list[dict] = []

    for candidate in candidates:
        family_action = str(candidate.get("family_action", "") or "")
        symbol_family = str(candidate.get("symbol_family", "") or "")
        action = str(candidate.get("action", "") or "")
        matches = [
            row for row in episodes
            if str(row.get("symbol_family", "") or "") == symbol_family and str(row.get("action", "") or "") == action
        ]
        rewards = [_safe_float(row.get("event_reward")) for row in matches]
        tp_count = sum(1 for row in matches if str(row.get("outcome_event", "") or "") == "TP")
        sl_count = sum(1 for row in matches if str(row.get("outcome_event", "") or "") == "SL")
        trade_count = sum(1 for row in matches if str(row.get("action", "") or "") in ("LONG", "SHORT"))
        run_labels = sorted({str(row.get("_run_label", "") or "") for row in matches if str(row.get("_run_label", "") or "")})
        source_roots = sorted({str(row.get("_source_root", "") or "") for row in matches if str(row.get("_source_root", "") or "")})
        sense_stabilities = {
            f"{field}_stability": round(_stability([_safe_float(row.get(field)) for row in matches]), 6)
            for field in SENSE_FIELDS
        }
        visual_stability = _mean([sense_stabilities[f"{field}_stability"] for field in SENSE_FIELDS[:3]])
        auditory_stability = _mean([sense_stabilities[f"{field}_stability"] for field in SENSE_FIELDS[3:5]])
        mcm_stability = _mean([sense_stabilities[f"{field}_stability"] for field in SENSE_FIELDS[5:]])
        multisensory_stability = _mean([visual_stability, auditory_stability, mcm_stability])
        consequence_support = max(0.0, _mean(rewards)) if rewards else 0.0
        recurrence_support = min(1.0, len(run_labels) / 6.0)
        source_support = min(1.0, len(source_roots) / max(1, len(episode_sources)))
        temporal_contact = max(0.0, 1.0 - min(1.0, _mean([_safe_float(row.get("phase_distance")) for row in matches]) if matches else 1.0))
        maturity_score = (
            consequence_support * 0.34
            + multisensory_stability * 0.24
            + recurrence_support * 0.18
            + source_support * 0.10
            + temporal_contact * 0.14
        )
        row = {
            "family_action": family_action,
            "symbol_family": symbol_family,
            "action": action,
            "passive_reife_rating_state": _rating_state(maturity_score, consequence_support, multisensory_stability, recurrence_support),
            "passive_reife_score": round(maturity_score, 6),
            "consequence_support": round(consequence_support, 6),
            "multisensory_stability": round(multisensory_stability, 6),
            "visual_stability": round(visual_stability, 6),
            "auditory_stability": round(auditory_stability, 6),
            "mcm_stability": round(mcm_stability, 6),
            "recurrence_support": round(recurrence_support, 6),
            "source_support": round(source_support, 6),
            "temporal_contact": round(temporal_contact, 6),
            "episode_count": len(matches),
            "trade_count": trade_count,
            "tp_count": tp_count,
            "sl_count": sl_count,
            "event_reward_sum": round(sum(rewards), 6),
            "run_labels": ",".join(run_labels),
            "source_roots": ",".join(source_roots),
            "passive_only": 1,
            "writes_memory": 0,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
        row.update(sense_stabilities)
        row["passive_reife_note"] = _note(row)
        detail.append(row)

    summary_by_state: dict[str, dict] = {}
    for row in detail:
        state = str(row.get("passive_reife_rating_state", "") or "unknown")
        bucket = summary_by_state.setdefault(
            state,
            {
                "passive_reife_rating_state": state,
                "count": 0,
                "family_actions": set(),
                "event_reward_sum": 0.0,
                "avg_passive_reife_score": 0.0,
                "avg_multisensory_stability": 0.0,
            },
        )
        bucket["count"] += 1
        bucket["family_actions"].add(str(row.get("family_action", "") or ""))
        bucket["event_reward_sum"] += _safe_float(row.get("event_reward_sum"))
        bucket["avg_passive_reife_score"] += _safe_float(row.get("passive_reife_score"))
        bucket["avg_multisensory_stability"] += _safe_float(row.get("multisensory_stability"))

    summary: list[dict] = []
    for bucket in summary_by_state.values():
        count = max(1, _safe_int(bucket["count"]))
        summary.append(
            {
                "passive_reife_rating_state": str(bucket["passive_reife_rating_state"]),
                "count": _safe_int(bucket["count"]),
                "event_reward_sum": round(_safe_float(bucket["event_reward_sum"]), 6),
                "avg_passive_reife_score": round(_safe_float(bucket["avg_passive_reife_score"]) / count, 6),
                "avg_multisensory_stability": round(_safe_float(bucket["avg_multisensory_stability"]) / count, 6),
                "family_actions": ",".join(sorted(item for item in bucket["family_actions"] if item)),
            }
        )
    detail.sort(key=lambda row: (-_safe_float(row.get("passive_reife_score")), str(row.get("family_action", ""))))
    summary.sort(key=lambda row: (-_safe_float(row.get("avg_passive_reife_score")), str(row.get("passive_reife_rating_state", ""))))
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, candidate_path: Path, episode_sources: list[Path]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_open_reife_rating.csv"
    summary_path = output_dir / "dio_mini_passive_open_reife_rating_summary.csv"
    json_path = output_dir / "dio_mini_passive_open_reife_rating.json"
    md_path = output_dir / "dio_mini_passive_open_reife_rating.md"
    txt_path = output_dir / "dio_mini_passive_open_reife_rating.txt"
    _write_csv(detail_path, detail, ["family_action", "passive_reife_rating_state", "passive_reife_score"])
    _write_csv(summary_path, summary, ["passive_reife_rating_state", "count", "family_actions"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_open_reife_rating.v1",
                "candidate_path": str(candidate_path),
                "episode_sources": [str(path) for path in episode_sources],
                "detail": detail,
                "summary": summary,
                "passive_only": True,
                "writes_memory": False,
                "influences_action": False,
                "is_gate": False,
                "is_motoric": False,
            },
            indent=2,
            ensure_ascii=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Mini-DIO passive offene Reife-Bewertung",
        "",
        "Grenze:",
        "",
        "- Diagnose nur passiv.",
        "- Kein Memory-Schreiben.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Keine Motorik.",
        "",
        "Zusammenfassung:",
        "",
    ]
    for row in summary:
        lines.append(
            f"- {row['passive_reife_rating_state']}: count={row['count']} "
            f"score={row['avg_passive_reife_score']} reward={row['event_reward_sum']} "
            f"families={row['family_actions']}"
        )
    lines.extend(["", "Details:", ""])
    for row in detail:
        lines.append(
            f"- `{row['family_action']}`: state={row['passive_reife_rating_state']} "
            f"score={row['passive_reife_score']} reward={row['event_reward_sum']} "
            f"multi={row['multisensory_stability']} visual={row['visual_stability']} "
            f"audio={row['auditory_stability']} mcm={row['mcm_stability']}"
        )
        lines.append(f"  {row['passive_reife_note']}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    txt_path.write_text(
        "\n".join(
            [
                f"passive_open_reife_rating_rows={len(detail)}",
                f"summary={len(summary)}",
                "",
                *[
                    f"{row['family_action']} {row['passive_reife_rating_state']} score={row['passive_reife_score']} reward={row['event_reward_sum']}"
                    for row in detail
                ],
                "",
                "passive_only=1",
                "writes_memory=0",
                "influences_action=0",
                "is_gate=0",
                "is_motoric=0",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--episode-source", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    detail, summary = build_rating(args.candidates, list(args.episode_source or []))
    write_outputs(detail, summary, args.output_dir, args.candidates, list(args.episode_source or []))
    print(f"passive_open_reife_rating_rows={len(detail)}")
    print(f"summary={len(summary)}")
    print(args.output_dir)


if __name__ == "__main__":
    main()
