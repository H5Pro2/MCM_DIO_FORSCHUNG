"""Compare passive maturity consequence landscapes across worlds.

This is a diagnostic-only comparison. It does not feed Mini-DIO runtime.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


PASSIVE_BOUNDARY = {
    "passive_only": True,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_future_teacher": False,
}


def _f(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _world_state_class(state: str) -> str:
    if state == "action_carried":
        return "acted_carried"
    if state in {"action_not_carried", "action_unclear"}:
        return "acted_unstable"
    if state == "withheld_carried_context_later_carried":
        return "overcautious_carried_context"
    if state == "withheld_cautious_context_later_carried":
        return "cautious_potential"
    if state == "withheld_open_context_later_carried":
        return "open_potential"
    if state == "withheld_not_carried":
        return "withheld_not_carried"
    return "unknown"


def _family_stability(classes: list[str]) -> str:
    counts = Counter(classes)
    if not classes:
        return "family_unknown"
    if counts["acted_carried"] and len(counts) == 1:
        return "family_stably_acted_carried"
    if counts["overcautious_carried_context"] and len(counts) == 1:
        return "family_stably_overcautious_carried"
    if counts["cautious_potential"] and len(counts) == 1:
        return "family_stably_cautious_potential"
    if counts["open_potential"] and len(counts) == 1:
        return "family_stably_open_potential"
    if counts["acted_carried"] and (
        counts["overcautious_carried_context"] or counts["cautious_potential"] or counts["open_potential"]
    ):
        return "family_context_switches_action_and_withholding"
    if counts["overcautious_carried_context"] and (counts["cautious_potential"] or counts["open_potential"]):
        return "family_context_dependent_withholding"
    if len(counts) > 1:
        return "family_mixed_context"
    return f"family_{classes[0]}"


def build_report(landscapes: dict[str, Path]) -> dict[str, Any]:
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for label, path in landscapes.items():
        for row in _read_csv(path):
            family = str(row.get("symbol_family", "") or "").strip()
            if not family:
                continue
            state = str(row.get("maturity_consequence_state", "") or "").strip()
            by_family[family].append(
                {
                    "landscape_label": label,
                    "world_label": row.get("world_label", ""),
                    "symbol_family": family,
                    "maturity_consequence_state": state,
                    "world_state_class": _world_state_class(state),
                    "afterlook_direction_hint": row.get("afterlook_direction_hint", "NONE"),
                    "afterlook_avg_best_reward": _f(row.get("afterlook_avg_best_reward")),
                    "avg_reflection_carry": _f(row.get("avg_reflection_carry")),
                    "world_carry": _f(row.get("world_carry")),
                    **PASSIVE_BOUNDARY,
                }
            )

    entries: list[dict[str, Any]] = []
    for family, observations in sorted(by_family.items()):
        classes = [str(obs["world_state_class"]) for obs in observations]
        directions = [str(obs.get("afterlook_direction_hint", "NONE")) for obs in observations]
        class_counts = Counter(classes)
        direction_counts = Counter(directions)
        entries.append(
            {
                "symbol_family": family,
                "observation_count": len(observations),
                "family_stability_state": _family_stability(classes),
                "class_counts": dict(class_counts),
                "direction_counts": dict(direction_counts),
                "dominant_direction": direction_counts.most_common(1)[0][0] if direction_counts else "NONE",
                "avg_afterlook_best_reward": mean([obs["afterlook_avg_best_reward"] for obs in observations] or [0.0]),
                "avg_reflection_carry": mean([obs["avg_reflection_carry"] for obs in observations] or [0.0]),
                "avg_world_carry": mean([obs["world_carry"] for obs in observations] or [0.0]),
                "observations": observations,
                **PASSIVE_BOUNDARY,
            }
        )

    stability_counts = Counter(entry["family_stability_state"] for entry in entries)
    return {
        "boundary": dict(PASSIVE_BOUNDARY),
        "landscapes": {k: str(v) for k, v in landscapes.items()},
        "summary": {
            "families": len(entries),
            "stability_counts": dict(stability_counts),
            "avg_afterlook_best_reward": mean([e["avg_afterlook_best_reward"] for e in entries] or [0.0]),
            "avg_reflection_carry": mean([e["avg_reflection_carry"] for e in entries] or [0.0]),
            "avg_world_carry": mean([e["avg_world_carry"] for e in entries] or [0.0]),
        },
        "entries": entries,
    }


def _write_outputs(report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "passive_maturity_consequence_landscape_compare.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    csv_path = output_dir / "passive_maturity_consequence_landscape_compare.csv"
    rows = []
    for entry in report.get("entries", []):
        flat = dict(entry)
        flat["class_counts"] = json.dumps(flat.get("class_counts", {}), sort_keys=True)
        flat["direction_counts"] = json.dumps(flat.get("direction_counts", {}), sort_keys=True)
        flat.pop("observations", None)
        rows.append(flat)
    if rows:
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    else:
        csv_path.write_text("symbol_family,family_stability_state\n", encoding="utf-8")

    summary = report.get("summary", {})
    ranked = sorted(
        report.get("entries", []),
        key=lambda e: (e.get("observation_count", 0), e.get("avg_afterlook_best_reward", 0.0)),
        reverse=True,
    )
    lines = [
        "# Mini-DIO Passive Maturity Consequence Landscape Compare",
        "",
        "- boundary: passive only; not read by Mini-DIO; no action; no gate",
        "",
        "## Summary",
        f"- families: {summary.get('families', 0)}",
        f"- stability_counts: {summary.get('stability_counts', {})}",
        f"- avg_afterlook_best_reward: {summary.get('avg_afterlook_best_reward', 0.0):.9f}",
        f"- avg_reflection_carry: {summary.get('avg_reflection_carry', 0.0):.9f}",
        f"- avg_world_carry: {summary.get('avg_world_carry', 0.0):.9f}",
        "",
        "## Repeated Families",
    ]
    for entry in [e for e in ranked if e.get("observation_count", 0) > 1][:25]:
        lines.append(
            "- "
            f"{entry['symbol_family']}: {entry['family_stability_state']}; "
            f"obs={entry['observation_count']}; "
            f"direction={entry['dominant_direction']}; "
            f"reward={entry['avg_afterlook_best_reward']:.6f}; "
            f"classes={entry['class_counts']}."
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- keine Regelbildung",
            "- keine Runtime-Rueckfuehrung",
            "- nur Vergleich, ob Reife familien- oder kontextgetragen wirkt",
        ]
    )
    (output_dir / "passive_maturity_consequence_landscape_compare.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--landscape",
        action="append",
        default=[],
        help="Landscape binding as label=csv_path.",
    )
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    landscapes: dict[str, Path] = {}
    for item in args.landscape:
        if "=" not in item:
            raise SystemExit(f"Invalid --landscape value: {item!r}; expected label=path")
        label, path = item.split("=", 1)
        landscapes[label] = Path(path)
    report = build_report(landscapes)
    _write_outputs(report, Path(args.output_dir))
    print(json.dumps(report["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
