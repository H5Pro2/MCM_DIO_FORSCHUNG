"""Build a passive detail lupe for one Mini-DIO reflection candidate family."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _read_rows(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item.setdefault("source_file", str(path))
                rows.append(item)
    return rows


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def build_lupe(family: str, trace_paths: list[Path]) -> tuple[list[dict], dict]:
    detail: list[dict] = []
    for row in _read_rows(trace_paths):
        if str(row.get("symbol_family", "") or "") != family:
            continue
        item = {
            "symbol_family": family,
            "run": str(row.get("run", "") or ""),
            "tick": str(row.get("tick", "") or ""),
            "debug_root": str(row.get("debug_root", "") or ""),
            "passive_inner_awareness_state": str(row.get("passive_inner_awareness_state", "") or "-"),
            "reflection_context_state": str(row.get("reflection_context_state", "") or "-"),
            "action": str(row.get("action", "") or "WAIT"),
            "raw_action": str(row.get("raw_action", "") or "WAIT"),
            "best_action_training": str(row.get("best_action_training", "") or "WAIT"),
            "outcome_event": str(row.get("outcome_event", "") or "NO_TRADE"),
            "reward": round(_safe_float(row.get("reward")), 6),
            "best_reward_training": round(_safe_float(row.get("best_reward_training")), 6),
            "withheld_best_trade": _safe_int(row.get("withheld_best_trade")),
            "passive_inner_awareness_afterlook": round(_safe_float(row.get("passive_inner_awareness_afterlook")), 6),
            "passive_inner_awareness_carry": round(_safe_float(row.get("passive_inner_awareness_carry")), 6),
            "passive_inner_awareness_world_carry": round(_safe_float(row.get("passive_inner_awareness_world_carry")), 6),
            "reflection_context_carry": round(_safe_float(row.get("reflection_context_carry")), 6),
            "reflection_context_strain": round(_safe_float(row.get("reflection_context_strain")), 6),
            "reflection_context_alignment": round(_safe_float(row.get("reflection_context_alignment")), 6),
            "sehen_form_stability": round(_safe_float(row.get("sehen_form_stability")), 6),
            "hoeren_energy_tone": round(_safe_float(row.get("hoeren_energy_tone")), 6),
            "fuehlen_mcm_coherence": round(_safe_float(row.get("fuehlen_mcm_coherence")), 6),
            "fuehlen_mcm_tension": round(_safe_float(row.get("fuehlen_mcm_tension")), 6),
            "source_file": str(row.get("source_file", "") or ""),
            "passive_only": True,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
        }
        detail.append(item)

    roots = {row["debug_root"] for row in detail if row.get("debug_root")}
    best_actions = {row["best_action_training"] for row in detail if row.get("best_action_training")}
    inner_states = {row["passive_inner_awareness_state"] for row in detail if row.get("passive_inner_awareness_state")}
    reflection_states = {row["reflection_context_state"] for row in detail if row.get("reflection_context_state")}
    count = len(detail)
    summary = {
        "symbol_family": family,
        "count": count,
        "debug_root_count": len(roots),
        "debug_roots": "|".join(sorted(roots)),
        "best_actions": "|".join(sorted(best_actions)),
        "inner_states": "|".join(sorted(inner_states)),
        "reflection_states": "|".join(sorted(reflection_states)),
        "wait_count": sum(1 for row in detail if str(row.get("action", "")).upper() == "WAIT"),
        "trade_count": sum(1 for row in detail if str(row.get("action", "")).upper() in {"LONG", "SHORT"}),
        "withheld_best_trade_count": sum(_safe_int(row.get("withheld_best_trade")) for row in detail),
        "avg_best_reward": round(sum(_safe_float(row.get("best_reward_training")) for row in detail) / count, 6)
        if count
        else 0.0,
        "avg_reflection_carry": round(sum(_safe_float(row.get("reflection_context_carry")) for row in detail) / count, 6)
        if count
        else 0.0,
        "avg_reflection_strain": round(sum(_safe_float(row.get("reflection_context_strain")) for row in detail) / count, 6)
        if count
        else 0.0,
        "passive_only": True,
        "influences_action": False,
    }
    return detail, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(family: str, detail: list[dict], summary: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / f"{family}_passive_reflection_candidate_lupe.csv"
    summary_path = output_dir / f"{family}_passive_reflection_candidate_lupe_summary.csv"
    json_path = output_dir / f"{family}_passive_reflection_candidate_lupe.json"
    md_path = output_dir / f"{family}_passive_reflection_candidate_lupe.md"

    _write_csv(detail_path, detail, ["symbol_family", "debug_root", "passive_inner_awareness_state"])
    _write_csv(summary_path, [summary], list(summary.keys()) if summary else ["symbol_family"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": {
                    "passive_only": True,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "writes_runtime_memory": False,
                },
                "summary": summary,
                "detail": detail,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        f"# Passive Reflection Candidate Lupe: {family}",
        "",
        "## Grenze",
        "- reine Lupe",
        "- keine Handlung",
        "- keine Memory-Wirkung",
        "- kein Gate",
        "",
        "## Summary",
        f"- count={summary.get('count', 0)}",
        f"- debug_root_count={summary.get('debug_root_count', 0)}",
        f"- best_actions={summary.get('best_actions', '-')}",
        f"- inner_states={summary.get('inner_states', '-')}",
        f"- reflection_states={summary.get('reflection_states', '-')}",
        f"- wait_count={summary.get('wait_count', 0)}",
        f"- trade_count={summary.get('trade_count', 0)}",
        f"- withheld_best_trade_count={summary.get('withheld_best_trade_count', 0)}",
        f"- avg_best_reward={summary.get('avg_best_reward', 0.0)}",
        f"- avg_reflection_carry={summary.get('avg_reflection_carry', 0.0)}",
        f"- avg_reflection_strain={summary.get('avg_reflection_strain', 0.0)}",
        "",
        "## Timeline",
    ]
    for row in detail:
        lines.append(
            f"- {row['debug_root']} run={row['run']} tick={row['tick']} "
            f"inner={row['passive_inner_awareness_state']} "
            f"reflection={row['reflection_context_state']} "
            f"action={row['action']} best={row['best_action_training']} "
            f"best_reward={row['best_reward_training']}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive detail lupe for one reflection candidate")
    parser.add_argument("--family", required=True)
    parser.add_argument("--trace", required=True, nargs="+")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    detail, summary = build_lupe(args.family, [Path(item) for item in args.trace])
    write_outputs(args.family, detail, summary, Path(args.output_dir))
    print(f"family={args.family} detail_rows={len(detail)}")


if __name__ == "__main__":
    main()
