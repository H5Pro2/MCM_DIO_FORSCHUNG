"""Report passive recurrence maturity context for Mini-DIO episodes.

This diagnostic joins current Mini-DIO episode families with the separated
passive recurrence maturity candidates. It is read-only reporting:

- no training memory is written
- no runtime state is changed
- no action, gate, or motoric path is influenced
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = list(fields)
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        writer.writerows(rows)


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _episode_paths(debug_root: Path) -> list[Path]:
    return sorted(debug_root.glob("**/episodes.csv"))


def _context_state(candidate: dict | None) -> str:
    if not candidate:
        return "recurrence_context_unknown"
    state = str(candidate.get("passive_reife_state", "") or "")
    if state == "sinnnah_variantenfaehig":
        return "recurrence_context_meaning_near"
    if state == "zeitfragil_aber_richtungserhaltend":
        return "recurrence_context_time_fragile"
    if state == "instabil_neuordnend":
        return "recurrence_context_reorganizing"
    return "recurrence_context_open"


def _context_note(family: str, candidate: dict | None) -> str:
    if not candidate:
        return f"{family}: keine passive Wiederkehrspur gefunden; nur beobachten."
    return (
        f"{family}: {candidate.get('passive_reife_state')}; "
        f"Sinn-Erhalt={_safe_float(candidate.get('meaning_preservation_rate')):.6f}; "
        f"stabile Wiederkehr={_safe_float(candidate.get('stable_recurrence_rate')):.6f}; "
        f"Zeitfragilitaet={_safe_float(candidate.get('temporal_fragility')):.6f}; "
        "passive Kontextlesung, keine Handlung."
    )


def load_candidates(path: Path) -> dict[str, dict]:
    payload = _load_json(path)
    entries = payload.get("entries", []) or []
    result: dict[str, dict] = {}
    for item in entries:
        family = str(item.get("reference_family", "") or "")
        if family:
            result[family] = dict(item)
    return result


def build_rows(debug_root: Path, candidates_path: Path) -> tuple[list[dict], list[dict]]:
    candidates = load_candidates(candidates_path)
    detail: list[dict] = []
    family_groups: dict[str, dict] = {}

    for episode_path in _episode_paths(debug_root):
        run_name = episode_path.parent.name
        for row in _read_csv(episode_path):
            family = str(row.get("symbol_family", "") or row.get("symbol", "") or "-")
            candidate = candidates.get(family)
            context_state = _context_state(candidate)
            item = {
                "run": run_name,
                "tick": str(row.get("tick", "") or ""),
                "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
                "symbol": str(row.get("symbol", "") or ""),
                "symbol_family": family,
                "action": str(row.get("action", "") or ""),
                "best_action_training": str(row.get("best_action_training", "") or ""),
                "outcome_event": str(row.get("outcome_event", "") or ""),
                "recurrence_context_state": context_state,
                "recurrence_maturity_symbol": str((candidate or {}).get("recurrence_maturity_symbol", "-") or "-"),
                "candidate_passive_reife_state": str((candidate or {}).get("passive_reife_state", "-") or "-"),
                "candidate_meaning_preservation_rate": round(
                    _safe_float((candidate or {}).get("meaning_preservation_rate")), 9
                ),
                "candidate_stable_recurrence_rate": round(
                    _safe_float((candidate or {}).get("stable_recurrence_rate")), 9
                ),
                "candidate_variant_capacity_rate": round(
                    _safe_float((candidate or {}).get("variant_capacity_rate")), 9
                ),
                "candidate_temporal_fragility": round(_safe_float((candidate or {}).get("temporal_fragility")), 9),
                "candidate_conflict_or_new_rate": round(_safe_float((candidate or {}).get("conflict_or_new_rate")), 9),
                "current_observation_learning_pressure": round(_safe_float(row.get("observation_learning_pressure")), 9),
                "current_trade_readiness": round(_safe_float(row.get("trade_readiness")), 9),
                "current_reflection_alignment": round(_safe_float(row.get("reflection_context_alignment")), 9),
                "current_mcm_coherence": round(_safe_float(row.get("fuehlen_mcm_coherence")), 9),
                "current_mcm_tension": round(_safe_float(row.get("fuehlen_mcm_tension")), 9),
                "context_note": _context_note(family, candidate),
                "passive_only": 1,
                "writes_training_memory": 0,
                "read_by_mini_dio": 0,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
            detail.append(item)

            group = family_groups.setdefault(
                family,
                {
                    "symbol_family": family,
                    "episodes": 0,
                    "context_state_counts": {},
                    "runs": set(),
                    "sum_observation_learning_pressure": 0.0,
                    "sum_trade_readiness": 0.0,
                    "sum_reflection_alignment": 0.0,
                    "candidate": candidate or {},
                },
            )
            group["episodes"] += 1
            group["runs"].add(run_name)
            group["sum_observation_learning_pressure"] += float(item["current_observation_learning_pressure"])
            group["sum_trade_readiness"] += float(item["current_trade_readiness"])
            group["sum_reflection_alignment"] += float(item["current_reflection_alignment"])
            counts = group["context_state_counts"]
            counts[context_state] = counts.get(context_state, 0) + 1

    summary: list[dict] = []
    for group in family_groups.values():
        episodes = max(1, int(group["episodes"]))
        counts = dict(sorted(group["context_state_counts"].items()))
        candidate = dict(group.get("candidate", {}) or {})
        dominant_state = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]
        summary.append(
            {
                "symbol_family": group["symbol_family"],
                "episodes": int(group["episodes"]),
                "run_count": len(group["runs"]),
                "dominant_recurrence_context_state": dominant_state,
                "context_state_counts": ";".join(f"{key}:{value}" for key, value in counts.items()),
                "candidate_passive_reife_state": str(candidate.get("passive_reife_state", "-") or "-"),
                "candidate_meaning_preservation_rate": round(
                    _safe_float(candidate.get("meaning_preservation_rate")), 9
                ),
                "candidate_stable_recurrence_rate": round(_safe_float(candidate.get("stable_recurrence_rate")), 9),
                "candidate_temporal_fragility": round(_safe_float(candidate.get("temporal_fragility")), 9),
                "avg_observation_learning_pressure": round(
                    float(group["sum_observation_learning_pressure"]) / episodes, 9
                ),
                "avg_trade_readiness": round(float(group["sum_trade_readiness"]) / episodes, 9),
                "avg_reflection_alignment": round(float(group["sum_reflection_alignment"]) / episodes, 9),
                "passive_only": 1,
                "writes_training_memory": 0,
                "read_by_mini_dio": 0,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
        )
    summary.sort(
        key=lambda row: (
            -_safe_float(row.get("candidate_meaning_preservation_rate")),
            -_safe_float(row.get("candidate_stable_recurrence_rate")),
            str(row.get("symbol_family", "")),
        )
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, debug_root: Path, candidates_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_recurrence_maturity_context.csv"
    summary_csv = output_dir / "dio_mini_passive_recurrence_maturity_context_summary.csv"
    json_path = output_dir / "dio_mini_passive_recurrence_maturity_context.json"
    md_path = output_dir / "dio_mini_passive_recurrence_maturity_context.md"
    txt_path = output_dir / "dio_mini_passive_recurrence_maturity_context.txt"

    _write_csv(detail_csv, detail, ["run", "tick", "symbol_family", "recurrence_context_state"])
    _write_csv(summary_csv, summary, ["symbol_family", "dominant_recurrence_context_state", "episodes"])
    payload = {
        "schema": "dio_mini_passive_recurrence_maturity_context.v1",
        "debug_root": str(debug_root),
        "candidates_path": str(candidates_path),
        "boundary": {
            "passive_only": True,
            "writes_training_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
        },
        "detail": detail,
        "summary": summary,
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    state_counts: dict[str, int] = {}
    for row in detail:
        state = str(row.get("recurrence_context_state", "") or "-")
        state_counts[state] = state_counts.get(state, 0) + 1
    lines = [
        "# Mini-DIO Passive Recurrence Maturity Context",
        "",
        f"- debug_root: `{debug_root}`",
        f"- candidates_path: `{candidates_path}`",
        "",
        "## Summary",
        f"- detail_rows: {len(detail)}",
        f"- family_rows: {len(summary)}",
        f"- states: {dict(sorted(state_counts.items()))}",
        "",
        "## Familien",
    ]
    for row in summary:
        lines.append(
            f"- {row['symbol_family']}: {row['dominant_recurrence_context_state']}; "
            f"state={row['candidate_passive_reife_state']}; "
            f"Sinn-Erhalt={row['candidate_meaning_preservation_rate']}; "
            f"Zeitfragilitaet={row['candidate_temporal_fragility']}"
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- Nur Bericht.",
            "- Keine Runtime-Rueckfuehrung.",
            "- Keine Handlung.",
            "- Kein Gate.",
            "- Kein Trainingsmemory.",
        ]
    )
    text = "\n".join(lines) + "\n"
    md_path.write_text(text, encoding="utf-8")
    txt_path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive recurrence maturity context")
    parser.add_argument("--debug-root", required=True, type=Path)
    parser.add_argument(
        "--candidates",
        default=Path("bot_memory/dio_mini_passive_recurrence_maturity_candidates.json"),
        type=Path,
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    detail, summary = build_rows(args.debug_root, args.candidates)
    write_outputs(detail, summary, args.output_dir, args.debug_root, args.candidates)
    print(
        json.dumps(
            {
                "detail_rows": len(detail),
                "family_rows": len(summary),
                "output_dir": str(args.output_dir),
                "read_by_mini_dio": False,
                "influences_action": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
