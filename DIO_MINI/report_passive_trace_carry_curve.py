"""Build passive carry curves for situational emergent traces.

This report reads passive temporal kipp points and describes how long a
syntax/family trace remains carried before it softens, loses lived support,
drifts, or reorganizes.

Passive only. It does not write runtime memory and is not read by Mini-DIO for
action, gates, entry, or direction.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PASSIVE_FLAGS = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}


CARRIED_STATE = "probe_no_visible_kipp"


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except (TypeError, ValueError):
        return default
    if result != result:
        return default
    return result


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = list(fields)
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in ordered})


def _probe_order(probe: str) -> int:
    match = re.search(r"(\d+)", str(probe or ""))
    return int(match.group(1)) if match else 999999


def _is_carried(state: str) -> bool:
    return str(state or "") == CARRIED_STATE


def _longest_run(states: list[str], *, carried: bool) -> int:
    longest = 0
    current = 0
    for state in states:
        matches = _is_carried(state) if carried else not _is_carried(state)
        if matches:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def _family_curve_state(states: list[str]) -> str:
    if not states:
        return "trace_absent"
    carried_count = sum(1 for state in states if _is_carried(state))
    kipp_count = len(states) - carried_count
    if kipp_count == 0:
        return "trace_fully_carried"
    if carried_count == 0:
        return "trace_immediate_or_continuous_kipp"
    if _is_carried(states[0]) and not _is_carried(states[-1]):
        return "trace_carries_then_kipps"
    if not _is_carried(states[0]) and _is_carried(states[-1]):
        return "trace_kipps_then_recarries"
    if carried_count >= kipp_count:
        return "trace_mixed_mostly_carried"
    return "trace_mixed_mostly_kipped"


def build_rows(
    *,
    detail_rows: list[dict[str, str]],
    family_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    family_meta = {str(row.get("symbol_family", "") or ""): row for row in family_rows}
    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_probe: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in detail_rows:
        family = str(row.get("symbol_family", "") or "")
        probe = str(row.get("probe", "") or "")
        if family:
            by_family[family].append(row)
        if probe:
            by_probe[probe].append(row)

    family_curve_rows: list[dict[str, Any]] = []
    for family, rows in sorted(by_family.items()):
        ordered = sorted(rows, key=lambda item: _probe_order(str(item.get("probe", ""))))
        states = [str(row.get("probe_kipp_state", "") or "") for row in ordered]
        probes = [str(row.get("probe", "") or "") for row in ordered]
        carried_count = sum(1 for state in states if _is_carried(state))
        kipp_count = len(states) - carried_count
        first_kipp_index = next((idx for idx, state in enumerate(states) if not _is_carried(state)), None)
        first_kipp_probe = probes[first_kipp_index] if first_kipp_index is not None else "-"
        first_kipp_state = states[first_kipp_index] if first_kipp_index is not None else CARRIED_STATE
        carried_before_first_kipp = first_kipp_index if first_kipp_index is not None else carried_count
        kipp_counter = Counter(state for state in states if not _is_carried(state))
        dominant_kipp_state = kipp_counter.most_common(1)[0][0] if kipp_counter else "-"
        meta = family_meta.get(family, {})
        family_curve_rows.append(
            {
                "symbol_family": family,
                "trace_carry_state": _family_curve_state(states),
                "visible_probe_count": len(states),
                "carried_probe_count": carried_count,
                "kipp_probe_count": kipp_count,
                "carry_ratio": round(carried_count / max(1, len(states)), 9),
                "first_probe": probes[0] if probes else "-",
                "last_probe": probes[-1] if probes else "-",
                "first_kipp_probe": first_kipp_probe,
                "first_kipp_state": first_kipp_state,
                "carried_before_first_kipp": carried_before_first_kipp,
                "longest_carried_run": _longest_run(states, carried=True),
                "longest_kipp_run": _longest_run(states, carried=False),
                "dominant_kipp_state": dominant_kipp_state,
                "probe_path": " -> ".join(probes),
                "kipp_state_path": " -> ".join(states),
                "family_temporal_kipp_state": meta.get("family_temporal_kipp_state", ""),
                "direction_support_state": meta.get("direction_support_state", ""),
                "alignment_state": meta.get("alignment_state", ""),
                "left_text_island_symbol": meta.get("left_text_island_symbol", ""),
                "right_text_island_symbol": meta.get("right_text_island_symbol", ""),
                "score_delta": meta.get("score_delta", ""),
                **PASSIVE_FLAGS,
            }
        )

    probe_curve_rows: list[dict[str, Any]] = []
    for probe, rows in sorted(by_probe.items(), key=lambda item: _probe_order(item[0])):
        states = [str(row.get("probe_kipp_state", "") or "") for row in rows]
        counter = Counter(states)
        carried_count = counter.get(CARRIED_STATE, 0)
        family_count = len(rows)
        probe_curve_rows.append(
            {
                "probe": probe,
                "family_count": family_count,
                "carried_count": carried_count,
                "kipp_count": family_count - carried_count,
                "carry_ratio": round(carried_count / max(1, family_count), 9),
                "lived_support_drop_count": counter.get("probe_lived_support_drop", 0),
                "direction_flip_count": counter.get("probe_direction_flip", 0),
                "observation_direction_flip_count": counter.get("probe_observation_direction_flip", 0),
                "best_reward_softens_count": counter.get("probe_best_reward_softens", 0),
                "trade_readiness_softens_count": counter.get("probe_trade_readiness_softens", 0),
                "neuro_tone_reorganizes_count": counter.get("probe_neuro_tone_reorganizes", 0),
                "temporal_state_reorganizes_count": counter.get("probe_temporal_state_reorganizes", 0),
                "avg_episode_count_delta": round(
                    sum(_safe_float(row.get("episode_count_delta")) for row in rows) / max(1, family_count), 9
                ),
                "avg_trade_readiness_delta": round(
                    sum(_safe_float(row.get("trade_readiness_delta")) for row in rows) / max(1, family_count), 9
                ),
                "avg_best_reward_training_delta": round(
                    sum(_safe_float(row.get("best_reward_training_delta")) for row in rows) / max(1, family_count),
                    9,
                ),
                "state_counts": "|".join(f"{key}:{value}" for key, value in sorted(counter.items())),
                **PASSIVE_FLAGS,
            }
        )

    summary_map: dict[str, dict[str, Any]] = {}
    for row in family_curve_rows:
        state = str(row["trace_carry_state"])
        bucket = summary_map.setdefault(
            state,
            {
                "trace_carry_state": state,
                "family_count": 0,
                "avg_carry_ratio": 0.0,
                "avg_carried_before_first_kipp": 0.0,
                "families": [],
                **PASSIVE_FLAGS,
            },
        )
        count = int(bucket["family_count"])
        bucket["family_count"] = count + 1
        bucket["families"].append(str(row["symbol_family"]))
        bucket["avg_carry_ratio"] = (
            (float(bucket["avg_carry_ratio"]) * count) + _safe_float(row.get("carry_ratio"))
        ) / max(1, count + 1)
        bucket["avg_carried_before_first_kipp"] = (
            (float(bucket["avg_carried_before_first_kipp"]) * count)
            + _safe_float(row.get("carried_before_first_kipp"))
        ) / max(1, count + 1)

    summary_rows: list[dict[str, Any]] = []
    for row in summary_map.values():
        row["avg_carry_ratio"] = round(float(row["avg_carry_ratio"]), 9)
        row["avg_carried_before_first_kipp"] = round(float(row["avg_carried_before_first_kipp"]), 9)
        row["families"] = "|".join(sorted(row["families"])[:40])
        summary_rows.append(row)

    family_curve_rows.sort(key=lambda row: (str(row["trace_carry_state"]), str(row["symbol_family"])))
    summary_rows.sort(key=lambda row: (-int(row["family_count"]), str(row["trace_carry_state"])))
    return family_curve_rows, probe_curve_rows, summary_rows


def _write_markdown(
    output_dir: Path,
    family_curve_rows: list[dict[str, Any]],
    probe_curve_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# Passive Trace Carry Curve",
        "",
        "Dieser Bericht beschreibt, wie lange situative emergente Spuren getragen bleiben.",
        "",
        "## Grenze",
        "",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- kein Gate",
        "- kein Entry",
        "- keine Richtung",
        "",
        "## Familien-Summary",
        "",
    ]
    for row in summary_rows:
        lines.append(
            "- {state}: families={count}, avg_carry_ratio={ratio}, "
            "avg_before_first_kipp={before}, examples={families}".format(
                state=row["trace_carry_state"],
                count=row["family_count"],
                ratio=row["avg_carry_ratio"],
                before=row["avg_carried_before_first_kipp"],
                families=row["families"] or "-",
            )
        )
    lines.extend(["", "## Probe-Kurve", ""])
    for row in probe_curve_rows:
        lines.append(
            "- {probe}: carry={carried}/{count} ratio={ratio}; support_drop={support}; "
            "direction_flip={flip}; neuro={neuro}; readiness={readiness}".format(
                probe=row["probe"],
                carried=row["carried_count"],
                count=row["family_count"],
                ratio=row["carry_ratio"],
                support=row["lived_support_drop_count"],
                flip=row["direction_flip_count"],
                neuro=row["neuro_tone_reorganizes_count"],
                readiness=row["trade_readiness_softens_count"],
            )
        )
    lines.extend(["", "## Familien", ""])
    for row in family_curve_rows[:100]:
        lines.append(
            "- {family}: {state}; carry={carried}/{visible}; first_kipp={probe}/{kipp}; "
            "path={path}".format(
                family=row["symbol_family"],
                state=row["trace_carry_state"],
                carried=row["carried_probe_count"],
                visible=row["visible_probe_count"],
                probe=row["first_kipp_probe"],
                kipp=row["first_kipp_state"],
                path=row["kipp_state_path"],
            )
        )
    (output_dir / "passive_trace_carry_curve.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(
    output_dir: Path,
    family_curve_rows: list[dict[str, Any]],
    probe_curve_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_trace_carry_curve_families.csv",
        family_curve_rows,
        [
            "symbol_family",
            "trace_carry_state",
            "visible_probe_count",
            "carried_probe_count",
            "kipp_probe_count",
            "carry_ratio",
            "first_probe",
            "last_probe",
            "first_kipp_probe",
            "first_kipp_state",
            "carried_before_first_kipp",
            "longest_carried_run",
            "longest_kipp_run",
            "dominant_kipp_state",
            "family_temporal_kipp_state",
            "direction_support_state",
            "alignment_state",
            "left_text_island_symbol",
            "right_text_island_symbol",
            "score_delta",
        ],
    )
    _write_csv(
        output_dir / "passive_trace_carry_curve_probes.csv",
        probe_curve_rows,
        [
            "probe",
            "family_count",
            "carried_count",
            "kipp_count",
            "carry_ratio",
            "lived_support_drop_count",
            "direction_flip_count",
            "observation_direction_flip_count",
            "best_reward_softens_count",
            "trade_readiness_softens_count",
            "neuro_tone_reorganizes_count",
            "temporal_state_reorganizes_count",
            "avg_episode_count_delta",
            "avg_trade_readiness_delta",
            "avg_best_reward_training_delta",
            "state_counts",
        ],
    )
    _write_csv(
        output_dir / "passive_trace_carry_curve_summary.csv",
        summary_rows,
        ["trace_carry_state", "family_count", "avg_carry_ratio", "avg_carried_before_first_kipp", "families"],
    )
    payload = {
        "families": family_curve_rows,
        "probes": probe_curve_rows,
        "summary": summary_rows,
        "boundary": PASSIVE_FLAGS,
    }
    (output_dir / "passive_trace_carry_curve.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, family_curve_rows, probe_curve_rows, summary_rows)
    (output_dir / "passive_trace_carry_curve.txt").write_text(
        "\n".join(
            f"{row['symbol_family']}: {row['trace_carry_state']} carry={row['carried_probe_count']}/{row['visible_probe_count']}"
            for row in family_curve_rows
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive trace carry curve")
    parser.add_argument("--temporal-detail", type=Path, required=True)
    parser.add_argument("--temporal-families", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    family_rows, probe_rows, summary_rows = build_rows(
        detail_rows=_read_csv(args.temporal_detail),
        family_rows=_read_csv(args.temporal_families),
    )
    write_outputs(args.output_dir, family_rows, probe_rows, summary_rows)
    print(
        json.dumps(
            {
                "families": len(family_rows),
                "probes": len(probe_rows),
                "summary": {row["trace_carry_state"]: row["family_count"] for row in summary_rows},
                **PASSIVE_FLAGS,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
