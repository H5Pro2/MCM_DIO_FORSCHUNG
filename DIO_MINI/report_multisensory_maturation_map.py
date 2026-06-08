"""Build a passive maturation map from multisensory stability.

The map separates stable positive recurrence, stable negative recurrence,
quiet observation, and mixed recurrence. It is diagnostic only.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _maturation_state(row: dict) -> str:
    reward = _safe_float(row.get("reward_sum", 0.0))
    avg_reward = _safe_float(row.get("avg_reward", 0.0))
    binding = str(row.get("dominant_binding_state", "") or "")
    inner = str(row.get("dominant_inner_state", "") or "")
    outcome = str(row.get("dominant_outcome_event", "") or "")
    stability = str(row.get("stability_label", "") or "")
    if "mixed" in stability:
        return "maturation_mixed_recurrence"
    if binding == "multisensory_carried_contact" and outcome == "TP" and reward > 0.0:
        return "maturation_stable_carried"
    if binding == "multisensory_conflicted_burden" and outcome == "SL" and reward < 0.0:
        return "maturation_stable_conflicted_burden"
    if inner == "inner_consequence_quiet" and outcome == "NO_TRADE":
        return "maturation_quiet_observation"
    if reward > 0.0 and avg_reward > 0.0:
        return "maturation_positive_open"
    if reward < 0.0 and avg_reward < 0.0:
        return "maturation_negative_open"
    return "maturation_open"


def _sentence(row: dict, state: str) -> str:
    family = str(row.get("symbol_family", "") or "-")
    binding = str(row.get("dominant_binding_state", "") or "-")
    sight = str(row.get("dominant_sight_state", "") or "-")
    hearing = str(row.get("dominant_hearing_state", "") or "-")
    feeling = str(row.get("dominant_feeling_state", "") or "-")
    reward = _safe_float(row.get("reward_sum", 0.0))
    runs = str(row.get("runs", "") or "-")
    if state == "maturation_stable_carried":
        return (
            f"{family}: stabile tragende Wiederkehr; {binding}; "
            f"Sehen={sight}, Hoeren={hearing}, Fuehlen={feeling}; reward_sum={reward:.6f}; Runs={runs}."
        )
    if state == "maturation_stable_conflicted_burden":
        return (
            f"{family}: stabile widerspruechlich-belastende Wiederkehr; {binding}; "
            f"Sehen={sight}, Hoeren={hearing}, Fuehlen={feeling}; reward_sum={reward:.6f}; Runs={runs}."
        )
    if state == "maturation_quiet_observation":
        return (
            f"{family}: stabile ruhige Beobachtung; {binding}; "
            f"Sehen={sight}, Hoeren={hearing}, Fuehlen={feeling}; Runs={runs}."
        )
    if state == "maturation_mixed_recurrence":
        return (
            f"{family}: gemischte Wiederkehr; {binding}; "
            f"Sehen={sight}, Hoeren={hearing}, Fuehlen={feeling}; reward_sum={reward:.6f}; Runs={runs}."
        )
    if state == "maturation_positive_open":
        return f"{family}: positive offene Reifespur; {binding}; reward_sum={reward:.6f}; Runs={runs}."
    if state == "maturation_negative_open":
        return f"{family}: negative offene Reifespur; {binding}; reward_sum={reward:.6f}; Runs={runs}."
    return f"{family}: offene Reifespur; {binding}; reward_sum={reward:.6f}; Runs={runs}."


def build_rows(stability_csv: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    for row in _read_csv(stability_csv):
        state = _maturation_state(row)
        item = {
            "symbol_family": str(row.get("symbol_family", "") or "-"),
            "maturation_state": state,
            "stability_label": str(row.get("stability_label", "") or ""),
            "count": int(float(row.get("count", 0) or 0)),
            "run_count": int(float(row.get("run_count", 0) or 0)),
            "runs": str(row.get("runs", "") or ""),
            "reward_sum": round(_safe_float(row.get("reward_sum", 0.0)), 6),
            "event_reward_sum": round(_safe_float(row.get("event_reward_sum", 0.0)), 6),
            "avg_reward": round(_safe_float(row.get("avg_reward", 0.0)), 6),
            "avg_dominant_share": round(_safe_float(row.get("avg_dominant_share", 0.0)), 6),
            "dominant_binding_state": str(row.get("dominant_binding_state", "") or ""),
            "dominant_inner_state": str(row.get("dominant_inner_state", "") or ""),
            "dominant_contact_state": str(row.get("dominant_contact_state", "") or ""),
            "dominant_action": str(row.get("dominant_action", "") or ""),
            "dominant_outcome_event": str(row.get("dominant_outcome_event", "") or ""),
            "dominant_sight_state": str(row.get("dominant_sight_state", "") or ""),
            "dominant_hearing_state": str(row.get("dominant_hearing_state", "") or ""),
            "dominant_feeling_state": str(row.get("dominant_feeling_state", "") or ""),
            "maturation_sentence": "",
            "passive_only": 1,
        }
        item["maturation_sentence"] = _sentence(row, state)
        detail.append(item)

    groups: dict[str, dict] = {}
    for row in detail:
        state = str(row.get("maturation_state", "") or "")
        group = groups.setdefault(
            state,
            {
                "maturation_state": state,
                "family_count": 0,
                "row_count": 0,
                "reward_sum": 0.0,
                "event_reward_sum": 0.0,
                "families": set(),
                "bindings": set(),
                "outcomes": set(),
            },
        )
        group["family_count"] += 1
        group["row_count"] += int(row.get("count", 0) or 0)
        group["reward_sum"] += _safe_float(row.get("reward_sum", 0.0))
        group["event_reward_sum"] += _safe_float(row.get("event_reward_sum", 0.0))
        group["families"].add(str(row.get("symbol_family", "") or ""))
        group["bindings"].add(str(row.get("dominant_binding_state", "") or ""))
        group["outcomes"].add(str(row.get("dominant_outcome_event", "") or ""))

    summary: list[dict] = []
    for group in groups.values():
        summary.append(
            {
                "maturation_state": group["maturation_state"],
                "family_count": int(group["family_count"]),
                "row_count": int(group["row_count"]),
                "reward_sum": round(float(group["reward_sum"]), 6),
                "event_reward_sum": round(float(group["event_reward_sum"]), 6),
                "families": ",".join(sorted(name for name in group["families"] if name)),
                "bindings": ",".join(sorted(name for name in group["bindings"] if name)),
                "outcomes": ",".join(sorted(name for name in group["outcomes"] if name)),
            }
        )

    order = {
        "maturation_stable_carried": 0,
        "maturation_positive_open": 1,
        "maturation_mixed_recurrence": 2,
        "maturation_quiet_observation": 3,
        "maturation_stable_conflicted_burden": 4,
        "maturation_negative_open": 5,
        "maturation_open": 6,
    }
    detail.sort(key=lambda item: (order.get(str(item.get("maturation_state", "")), 99), str(item.get("symbol_family", ""))))
    summary.sort(key=lambda item: order.get(str(item.get("maturation_state", "")), 99))
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, stability_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_multisensory_maturation_map.csv"
    summary_path = output_dir / "dio_mini_multisensory_maturation_map_summary.csv"
    json_path = output_dir / "dio_mini_multisensory_maturation_map.json"
    md_path = output_dir / "dio_mini_multisensory_maturation_map.md"

    detail_fields = list(detail[0].keys()) if detail else [
        "symbol_family",
        "maturation_state",
        "stability_label",
        "count",
        "run_count",
        "reward_sum",
        "dominant_binding_state",
        "dominant_outcome_event",
        "maturation_sentence",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else [
        "maturation_state",
        "family_count",
        "row_count",
        "reward_sum",
        "event_reward_sum",
        "families",
        "bindings",
        "outcomes",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "stability_csv": str(stability_csv),
                "detail": detail,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Multisensory Maturation Map",
        "",
        "## Grenze",
        "- liest nur die passive multisensorische Stabilitaet",
        "- schreibt kein Memory",
        "- beeinflusst keine Handlung",
        "- kein Gate",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Reifungsdaten")
    else:
        for row in summary:
            lines.append(
                f"- {row.get('maturation_state', '-')}: families={row.get('family_count', 0)} "
                f"rows={row.get('row_count', 0)} reward_sum={row.get('reward_sum', 0.0)} "
                f"bindings={row.get('bindings', '-') or '-'}"
            )
    lines.extend(["", "## Familien"])
    for row in detail:
        lines.append(f"- {row.get('maturation_sentence', '-')}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO multisensory maturation map")
    parser.add_argument("--stability-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    stability_csv = Path(args.stability_csv)
    detail, summary = build_rows(stability_csv)
    write_outputs(detail, summary, Path(args.output_dir), stability_csv)
    print(f"multisensory_maturation_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary:
        print(
            f"{row['maturation_state']} families={row['family_count']} "
            f"rows={row['row_count']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
