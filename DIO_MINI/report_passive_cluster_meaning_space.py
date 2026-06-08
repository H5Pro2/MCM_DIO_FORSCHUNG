"""Build a passive meaning-space lupe for Mini-DIO syntax clusters.

The report reads Mini-DIO episode CSV files and aggregates what a syntax
family carries: visual form, auditory energy, MCM feeling, temporal afterimage,
neuro tone, consequence, and action/observation traces.

It is diagnostic only. It does not write runtime memory and does not influence
Mini-DIO action.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


BOUNDARY = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}

SENSE_FIELDS = [
    "sehen_form_flow",
    "sehen_form_stability",
    "sehen_form_change",
    "hoeren_energy_tone",
    "hoeren_energy_shift",
    "fuehlen_mcm_coherence",
    "fuehlen_mcm_tension",
    "fuehlen_mcm_asymmetry",
]

TEMPORAL_FIELDS = [
    "mini_recurrence_strength",
    "mini_afterimage",
    "mini_time_distance",
    "mini_temporal_form_distance",
    "mini_temporal_trust_support",
    "mini_temporal_caution_support",
]

NEURO_FIELDS = [
    "mini_focus_tone",
    "mini_trust_tone",
    "mini_caution_tone",
    "mini_strain_tone",
    "mini_relief_tone",
    "mini_observation_tone",
    "mini_neuro_support",
    "mini_neuro_load",
    "mini_neuro_balance",
]

REFLECTION_FIELDS = [
    "reflection_context_carry",
    "reflection_context_strain",
    "reflection_context_alignment",
    "reflection_world_support",
    "reflection_current_support",
]


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


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


def _mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _span(values: list[float]) -> float:
    if not values:
        return 0.0
    return max(values) - min(values)


def _count(counter: dict[str, int], key: object) -> None:
    text = str(key or "-")
    counter[text] = int(counter.get(text, 0) or 0) + 1


def _counts_text(counter: dict[str, int]) -> str:
    return "|".join(f"{key}:{counter[key]}" for key in sorted(counter))


def _episode_paths(debug_roots: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for root in debug_roots:
        if root.is_file() and root.name == "episodes.csv":
            paths.append(root)
            continue
        if (root / "episodes.csv").exists():
            paths.append(root / "episodes.csv")
            continue
        paths.extend(sorted(root.glob("dio_mini_lauf_*/episodes.csv")))
    unique = {str(path.resolve()): path for path in paths}
    return [unique[key] for key in sorted(unique)]


def _source_label(path: Path) -> str:
    parent = path.parent.name
    grand = path.parent.parent.name if path.parent.parent else ""
    return f"{grand}/{parent}" if grand else parent


def _init_cluster(family: str) -> dict:
    return {
        "symbol_family": family,
        "sources": set(),
        "ticks": [],
        "timestamps": [],
        "symbols": set(),
        "actions": {},
        "raw_actions": {},
        "outcomes": {},
        "best_actions": {},
        "neuro_tones": {},
        "reflection_states": {},
        "temporal_states": {},
        "sense": {field: [] for field in SENSE_FIELDS},
        "temporal": {field: [] for field in TEMPORAL_FIELDS},
        "neuro": {field: [] for field in NEURO_FIELDS},
        "reflection": {field: [] for field in REFLECTION_FIELDS},
        "reward": [],
        "event_reward": [],
        "trade_readiness": [],
        "associative_trade": [],
        "observation_trade_signal": [],
        "observation_learning_pressure": [],
    }


def _candidate_index(path: Path | None) -> dict[str, dict]:
    if path is None:
        return {}
    payload = _read_json(path)
    entries = payload.get("entries", []) if isinstance(payload, dict) else []
    index: dict[str, dict] = {}
    for entry in entries or []:
        item = dict(entry or {})
        family = str(item.get("reference_family", "") or "")
        if family:
            index[family] = item
    return index


def _add_episode(cluster: dict, row: dict, source: str) -> None:
    cluster["sources"].add(source)
    cluster["ticks"].append(_safe_int(row.get("tick")))
    cluster["timestamps"].append(_safe_int(row.get("timestamp_ms")))
    symbol = str(row.get("symbol", "") or "")
    if symbol:
        cluster["symbols"].add(symbol)
    _count(cluster["actions"], row.get("action"))
    _count(cluster["raw_actions"], row.get("raw_action"))
    _count(cluster["outcomes"], row.get("outcome_event"))
    _count(cluster["best_actions"], row.get("best_action_training"))
    _count(cluster["neuro_tones"], row.get("mini_neuro_dominant_tone"))
    _count(cluster["reflection_states"], row.get("reflection_context_state"))
    _count(cluster["temporal_states"], row.get("mini_temporal_state"))
    for field in SENSE_FIELDS:
        cluster["sense"][field].append(_safe_float(row.get(field)))
    for field in TEMPORAL_FIELDS:
        cluster["temporal"][field].append(_safe_float(row.get(field)))
    for field in NEURO_FIELDS:
        cluster["neuro"][field].append(_safe_float(row.get(field)))
    for field in REFLECTION_FIELDS:
        cluster["reflection"][field].append(_safe_float(row.get(field)))
    cluster["reward"].append(_safe_float(row.get("reward")))
    cluster["event_reward"].append(_safe_float(row.get("event_reward")))
    cluster["trade_readiness"].append(_safe_float(row.get("trade_readiness")))
    cluster["associative_trade"].append(_safe_float(row.get("associative_trade")))
    cluster["observation_trade_signal"].append(_safe_float(row.get("observation_trade_signal")))
    cluster["observation_learning_pressure"].append(_safe_float(row.get("observation_learning_pressure")))


def _dominant(counter: dict[str, int]) -> str:
    if not counter:
        return "-"
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _field_summary(prefix: str, values_by_field: dict[str, list[float]]) -> dict:
    output: dict[str, float] = {}
    for field, values in values_by_field.items():
        key = field.replace(prefix, "") if field.startswith(prefix) else field
        output[f"avg_{key}"] = round(_mean(values), 6)
        output[f"span_{key}"] = round(_span(values), 6)
    return output


def _cluster_sentence(row: dict) -> str:
    family = str(row.get("symbol_family", "") or "")
    dominant_action = str(row.get("dominant_action", "") or "-")
    dominant_tone = str(row.get("dominant_neuro_tone", "") or "-")
    dominant_temporal = str(row.get("dominant_temporal_state", "") or "-")
    reward_sum = _safe_float(row.get("reward_sum"))
    if reward_sum > 0.0:
        consequence = "getragen"
    elif reward_sum < 0.0:
        consequence = "belastet"
    else:
        consequence = "neutral"
    return (
        f"{family}: wiederkehrende Syntaxspur; dominant {dominant_action}; "
        f"zeitlich {dominant_temporal}; neurochemisch {dominant_tone}; "
        f"Konsequenz {consequence}. Passive Lupe, keine Handlung."
    )


def build_meaning_space(
    debug_roots: list[Path],
    family_filter: set[str],
    candidates_path: Path | None = None,
) -> tuple[list[dict], list[dict]]:
    clusters: dict[str, dict] = {}
    detail: list[dict] = []
    candidates = _candidate_index(candidates_path)
    for path in _episode_paths(debug_roots):
        source = _source_label(path)
        for row in _read_csv(path):
            family = str(row.get("symbol_family", "") or "")
            if not family or (family_filter and family not in family_filter):
                continue
            cluster = clusters.setdefault(family, _init_cluster(family))
            _add_episode(cluster, row, source)
            detail.append(
                {
                    "source": source,
                    "tick": _safe_int(row.get("tick")),
                    "timestamp_ms": _safe_int(row.get("timestamp_ms")),
                    "symbol": str(row.get("symbol", "") or ""),
                    "symbol_family": family,
                    "action": str(row.get("action", "") or ""),
                    "raw_action": str(row.get("raw_action", "") or ""),
                    "outcome_event": str(row.get("outcome_event", "") or ""),
                    "best_action_training": str(row.get("best_action_training", "") or ""),
                    "mini_temporal_state": str(row.get("mini_temporal_state", "") or ""),
                    "mini_neuro_dominant_tone": str(row.get("mini_neuro_dominant_tone", "") or ""),
                    "reflection_context_state": str(row.get("reflection_context_state", "") or ""),
                    "reward": round(_safe_float(row.get("reward")), 6),
                    "observation_learning_pressure": round(_safe_float(row.get("observation_learning_pressure")), 6),
                    **{field: round(_safe_float(row.get(field)), 6) for field in SENSE_FIELDS},
                    **BOUNDARY,
                }
            )

    summary: list[dict] = []
    for cluster in clusters.values():
        ticks = cluster["ticks"]
        timestamps = cluster["timestamps"]
        candidate = dict(candidates.get(cluster["symbol_family"], {}) or {})
        row = {
            "symbol_family": cluster["symbol_family"],
            "source_count": len(cluster["sources"]),
            "sources": "|".join(sorted(cluster["sources"])),
            "episode_count": len(ticks),
            "symbol_count": len(cluster["symbols"]),
            "symbols": "|".join(sorted(cluster["symbols"])),
            "first_tick": min(ticks) if ticks else 0,
            "last_tick": max(ticks) if ticks else 0,
            "first_timestamp_ms": min(timestamps) if timestamps else 0,
            "last_timestamp_ms": max(timestamps) if timestamps else 0,
            "dominant_action": _dominant(cluster["actions"]),
            "action_counts": _counts_text(cluster["actions"]),
            "raw_action_counts": _counts_text(cluster["raw_actions"]),
            "outcome_counts": _counts_text(cluster["outcomes"]),
            "best_action_counts": _counts_text(cluster["best_actions"]),
            "dominant_neuro_tone": _dominant(cluster["neuro_tones"]),
            "neuro_tone_counts": _counts_text(cluster["neuro_tones"]),
            "dominant_temporal_state": _dominant(cluster["temporal_states"]),
            "temporal_state_counts": _counts_text(cluster["temporal_states"]),
            "dominant_reflection_state": _dominant(cluster["reflection_states"]),
            "reflection_state_counts": _counts_text(cluster["reflection_states"]),
            "reward_sum": round(sum(cluster["reward"]), 6),
            "avg_reward": round(_mean(cluster["reward"]), 6),
            "event_reward_sum": round(sum(cluster["event_reward"]), 6),
            "avg_trade_readiness": round(_mean(cluster["trade_readiness"]), 6),
            "avg_associative_trade": round(_mean(cluster["associative_trade"]), 6),
            "avg_observation_trade_signal": round(_mean(cluster["observation_trade_signal"]), 6),
            "avg_observation_learning_pressure": round(_mean(cluster["observation_learning_pressure"]), 6),
            "candidate_loaded": bool(candidate),
            "candidate_recurrence_maturity_symbol": str(candidate.get("recurrence_maturity_symbol", "") or ""),
            "candidate_passive_reife_state": str(candidate.get("passive_reife_state", "") or ""),
            "candidate_episodes": _safe_int(candidate.get("episodes")),
            "candidate_meaning_preservation_rate": round(_safe_float(candidate.get("meaning_preservation_rate")), 6),
            "candidate_stable_recurrence_rate": round(_safe_float(candidate.get("stable_recurrence_rate")), 6),
            "candidate_variant_capacity_rate": round(_safe_float(candidate.get("variant_capacity_rate")), 6),
            "candidate_temporal_fragility": round(_safe_float(candidate.get("temporal_fragility")), 6),
            "candidate_probe_trace": str(candidate.get("probe_trace", "") or ""),
            **_field_summary("", cluster["sense"]),
            **_field_summary("", cluster["temporal"]),
            **_field_summary("", cluster["neuro"]),
            **_field_summary("", cluster["reflection"]),
            **BOUNDARY,
        }
        row["dio_cluster_sentence"] = _cluster_sentence(row)
        summary.append(row)

    summary.sort(key=lambda row: (-int(row["episode_count"]), str(row["symbol_family"])))
    detail.sort(key=lambda row: (str(row["symbol_family"]), str(row["source"]), int(row["tick"])))
    return summary, detail


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(summary: list[dict], detail: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "passive_cluster_meaning_space.csv"
    detail_path = output_dir / "passive_cluster_meaning_space_episodes.csv"
    json_path = output_dir / "passive_cluster_meaning_space.json"
    md_path = output_dir / "README.md"

    _write_csv(summary_path, summary, ["symbol_family", "episode_count"])
    _write_csv(detail_path, detail, ["symbol_family", "tick"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_cluster_meaning_space.v1",
                "boundary": BOUNDARY,
                "clusters": summary,
                "episodes": detail,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Mini-DIO passive Cluster-Bedeutungsraum",
        "",
        "Ziel: einen emergenten Cluster isolieren und als getragenen Bedeutungsraum lesen.",
        "",
        "## Grenze",
        "- Nur Bericht.",
        "- Keine Runtime-Rueckfuehrung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Trainingsmemory.",
        "",
        "## Cluster",
    ]
    for row in summary[:40]:
        lines.append(f"- {row['dio_cluster_sentence']} episodes={row['episode_count']}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO cluster meaning-space lupe")
    parser.add_argument("--debug-root", nargs="+", required=True, type=Path)
    parser.add_argument("--family", nargs="*", default=[])
    parser.add_argument("--candidates", type=Path, default=None)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    summary, detail = build_meaning_space(args.debug_root, set(args.family or []), args.candidates)
    write_outputs(summary, detail, args.output_dir)
    print(
        json.dumps(
            {
                "clusters": len(summary),
                "episodes": len(detail),
                "output_dir": str(args.output_dir),
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
