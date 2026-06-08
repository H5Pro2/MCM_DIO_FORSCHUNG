"""Report passive family maturation paths across DIO_MINI debug roots.

This reader combines family contrast states from multiple debug worlds. It
shows whether a family moves, for example, from conflict to observed to carried.
It is diagnostic only and does not write memory or influence action.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.report_family_contrast import build_family_rows


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _state_rank(state: str) -> int:
    return {
        "conflict": -2,
        "quiet": -1,
        "held": 0,
        "observed": 1,
        "carried": 2,
    }.get(str(state or ""), 0)


def _path_sentence(family: str, states: list[str], rewards: list[float]) -> str:
    path = " -> ".join(states)
    if "conflict" in states and states[-1] == "carried":
        return f"{family}: Konflikt wurde ueber Beobachtung/Erfahrung in Tragnaehe ueberfuehrt ({path})."
    if "conflict" in states and states[-1] == "observed":
        return f"{family}: Konflikt wurde in Beobachtung/Vorsicht ueberfuehrt ({path})."
    if states[0] == "observed" and states[-1] == "carried":
        return f"{family}: beobachtetes Potenzial wurde spaeter getragen ({path})."
    if all(state == "carried" for state in states):
        return f"{family}: bleibt ueber alle gelesenen Welten getragen ({path})."
    if len(set(states)) == 1:
        return f"{family}: bleibt stabil bei {states[0]} ({path})."
    return f"{family}: zeigt einen offenen Reifeverlauf ({path}), reward_sum={sum(rewards):.6f}."


def _read_roots(inputs: list[tuple[str, Path]], selected_families: set[str] | None) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    grouped: dict[str, list[dict]] = {}
    for label, root in inputs:
        for row in build_family_rows(root, selected_families=selected_families):
            item = {
                "label": label,
                "debug_root": str(root),
                "family": str(row.get("family", "") or ""),
                "family_state": str(row.get("family_state", "") or ""),
                "dominant_action": str(row.get("dominant_action", "") or ""),
                "episode_count": int(row.get("episode_count", 0) or 0),
                "executed_count": int(row.get("executed_count", 0) or 0),
                "reward_sum": float(row.get("reward_sum", 0.0) or 0.0),
                "states": str(row.get("states", "") or "-"),
                "actions": str(row.get("actions", "") or "-"),
                "passive_sentence": str(row.get("passive_sentence", "") or ""),
            }
            detail.append(item)
            if item["family"]:
                grouped.setdefault(item["family"], []).append(item)

    summary: list[dict] = []
    order = {label: index for index, (label, _root) in enumerate(inputs)}
    for family, items in sorted(grouped.items()):
        items = sorted(items, key=lambda item: order.get(str(item.get("label", "")), 9999))
        states = [str(item.get("family_state", "") or "") for item in items]
        rewards = [_safe_float(item.get("reward_sum", 0.0)) for item in items]
        ranks = [_state_rank(state) for state in states]
        trend = "flat"
        if len(ranks) >= 2 and ranks[-1] > ranks[0]:
            trend = "maturing"
        elif len(ranks) >= 2 and ranks[-1] < ranks[0]:
            trend = "cooling"
        if "conflict" in states and states[-1] in ("observed", "held"):
            trend = "conflict_to_caution"
        if "conflict" in states and states[-1] == "carried":
            trend = "conflict_to_carried"
        if states[0] == "observed" and states[-1] == "carried":
            trend = "observed_to_carried"
        summary.append(
            {
                "family": family,
                "step_count": len(items),
                "path": " -> ".join(f"{item['label']}:{item['family_state']}" for item in items),
                "state_path": " -> ".join(states),
                "action_path": " -> ".join(f"{item['label']}:{item['dominant_action']}" for item in items),
                "reward_sum": round(sum(rewards), 6),
                "trend": trend,
                "passive_sentence": _path_sentence(family, states, rewards),
            }
        )
    summary.sort(
        key=lambda item: (
            str(item.get("trend", "")) not in ("conflict_to_carried", "observed_to_carried", "maturing"),
            -_safe_float(item.get("reward_sum", 0.0)),
            str(item.get("family", "")),
        )
    )
    return detail, summary


def _write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_family_maturation_path_detail.csv"
    summary_csv = output_dir / "dio_mini_family_maturation_path.csv"
    json_path = output_dir / "dio_mini_family_maturation_path.json"
    md_path = output_dir / "dio_mini_family_maturation_path.md"

    detail_fields = [
        "label",
        "debug_root",
        "family",
        "family_state",
        "dominant_action",
        "episode_count",
        "executed_count",
        "reward_sum",
        "states",
        "actions",
        "passive_sentence",
    ]
    with detail_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = [
        "family",
        "step_count",
        "trend",
        "reward_sum",
        "state_path",
        "action_path",
        "path",
        "passive_sentence",
    ]
    with summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)
    json_path.write_text(json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Family Maturation Path", ""]
    if not summary:
        lines.append("Keine Familienpfade gefunden.")
    for row in summary:
        lines.extend(
            [
                f"## {row['family']}",
                f"- trend: {row['trend']}",
                f"- state_path: {row['state_path']}",
                f"- action_path: {row['action_path']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- passive_sentence: {row['passive_sentence']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive DIO_MINI family maturation path report")
    parser.add_argument("--debug-root", action="append", required=True, help="label=path/to/debug/root")
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    inputs: list[tuple[str, Path]] = []
    for raw in args.debug_root:
        if "=" not in raw:
            raise SystemExit(f"--debug-root must be label=path, got: {raw}")
        label, path = raw.split("=", 1)
        inputs.append((label.strip(), Path(path.strip())))
    selected = {str(item).strip() for item in args.family if str(item).strip()} or None
    detail, summary = _read_roots(inputs, selected)
    _write_outputs(detail, summary, Path(args.output_dir))
    print(f"families={len(summary)} detail_rows={len(detail)}")
    for row in summary[:25]:
        print(f"{row['family']} trend={row['trend']} states={row['state_path']} reward={row['reward_sum']}")


if __name__ == "__main__":
    main()
