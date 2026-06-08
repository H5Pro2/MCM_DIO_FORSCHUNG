"""Build a passive multisensory inner map for Mini-DIO.

The map joins sight, hearing, feeling, and stored consequence inner state per
tick. It creates readable diagnostics only and must not influence action.
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


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _read_protocol(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _sight_state(flow: float, stability: float) -> str:
    if abs(stability) >= 0.75 and abs(flow) >= 0.35:
        return "sehen_geformte_bewegung"
    if abs(stability) >= 0.75:
        return "sehen_stabile_form"
    if abs(flow) >= 0.45:
        return "sehen_bewegte_form"
    if abs(stability) <= 0.15 and abs(flow) <= 0.15:
        return "sehen_offen"
    return "sehen_teilform"


def _hearing_state(tone: float) -> str:
    if tone >= 0.12:
        return "hoeren_helle_spannung"
    if tone <= -0.12:
        return "hoeren_dunkle_spannung"
    if abs(tone) <= 0.035:
        return "hoeren_leise"
    return "hoeren_mittlere_spannung"


def _feeling_state(coherence: float, tension: float) -> str:
    if coherence >= 0.75 and tension <= 0.18:
        return "fuehlen_koharent_ruhig"
    if coherence >= 0.65:
        return "fuehlen_koharent_gespannt"
    if coherence <= -0.20:
        return "fuehlen_inkoharent"
    if tension >= 0.32:
        return "fuehlen_hohe_spannung"
    return "fuehlen_offen"


def _binding_state(sight: str, hearing: str, feeling: str, inner: str, contact: str) -> str:
    if inner == "inner_consequence_carried" and contact == "real_contact_carried":
        return "multisensory_carried_contact"
    if inner == "inner_consequence_conflicted" and contact == "real_contact_burdened":
        return "multisensory_conflicted_burden"
    if inner == "inner_consequence_burdened":
        return "multisensory_burdened_memory"
    if inner == "inner_consequence_quiet" and contact.startswith("held_"):
        return "multisensory_quiet_hold"
    if inner == "inner_consequence_quiet":
        return "multisensory_quiet_observation"
    if "inkoharent" in feeling:
        return "multisensory_field_mismatch"
    if "geformte" in sight and "koharent" in feeling:
        return "multisensory_form_field_contact"
    if "spannung" in hearing and "teilform" in sight:
        return "multisensory_tone_over_partial_form"
    return "multisensory_open"


def _sentence(row: dict, sight: str, hearing: str, feeling: str, binding: str) -> str:
    family = str(row.get("symbol_family", "") or "-")
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    inner = str(row.get("inner_state", "inner_consequence_unknown") or "inner_consequence_unknown")
    contact = str(row.get("contact_state", "") or "-")
    return (
        f"{family}: {sight}, {hearing}, {feeling}; "
        f"Innenlage={inner}, Kontakt={contact}, Aktion={action}; Bindung={binding}."
    )


def build_rows(protocol_csv: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    for row in _read_protocol(protocol_csv):
        flow = _safe_float(row.get("sehen_form_flow", 0.0))
        stability = _safe_float(row.get("sehen_form_stability", 0.0))
        tone = _safe_float(row.get("hoeren_energy_tone", 0.0))
        coherence = _safe_float(row.get("fuehlen_mcm_coherence", 0.0))
        tension = _safe_float(row.get("fuehlen_mcm_tension", 0.0))
        sight = _sight_state(flow, stability)
        hearing = _hearing_state(tone)
        feeling = _feeling_state(coherence, tension)
        inner = str(row.get("inner_state", "") or "")
        contact = str(row.get("contact_state", "") or "")
        binding = _binding_state(sight, hearing, feeling, inner, contact)
        detail.append(
            {
                "run": str(row.get("run", "") or ""),
                "tick": str(row.get("tick", "") or ""),
                "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
                "symbol_family": str(row.get("symbol_family", "") or "-"),
                "action": str(row.get("action", "WAIT") or "WAIT").upper(),
                "outcome_event": str(row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper(),
                "contact_state": contact,
                "inner_state": inner,
                "sight_state": sight,
                "hearing_state": hearing,
                "feeling_state": feeling,
                "binding_state": binding,
                "sehen_form_flow": round(flow, 6),
                "sehen_form_stability": round(stability, 6),
                "hoeren_energy_tone": round(tone, 6),
                "fuehlen_mcm_coherence": round(coherence, 6),
                "fuehlen_mcm_tension": round(tension, 6),
                "reward": round(_safe_float(row.get("reward", 0.0)), 6),
                "event_reward": round(_safe_float(row.get("event_reward", 0.0)), 6),
                "inner_sentence": _sentence(row, sight, hearing, feeling, binding),
                "passive_only": 1,
            }
        )

    groups: dict[tuple[str, str, str, str], dict] = {}
    for row in detail:
        key = (
            str(row.get("binding_state", "")),
            str(row.get("inner_state", "")),
            str(row.get("contact_state", "")),
            str(row.get("action", "")),
        )
        group = groups.setdefault(
            key,
            {
                "binding_state": key[0],
                "inner_state": key[1],
                "contact_state": key[2],
                "action": key[3],
                "count": 0,
                "reward_sum": 0.0,
                "event_reward_sum": 0.0,
                "families": set(),
                "sight_states": set(),
                "hearing_states": set(),
                "feeling_states": set(),
            },
        )
        group["count"] += 1
        group["reward_sum"] += _safe_float(row.get("reward", 0.0))
        group["event_reward_sum"] += _safe_float(row.get("event_reward", 0.0))
        group["families"].add(str(row.get("symbol_family", "") or ""))
        group["sight_states"].add(str(row.get("sight_state", "") or ""))
        group["hearing_states"].add(str(row.get("hearing_state", "") or ""))
        group["feeling_states"].add(str(row.get("feeling_state", "") or ""))

    summary: list[dict] = []
    for group in groups.values():
        count = int(group["count"])
        summary.append(
            {
                "binding_state": group["binding_state"],
                "inner_state": group["inner_state"],
                "contact_state": group["contact_state"],
                "action": group["action"],
                "count": count,
                "reward_sum": round(float(group["reward_sum"]), 6),
                "event_reward_sum": round(float(group["event_reward_sum"]), 6),
                "avg_reward": round(float(group["reward_sum"]) / max(1, count), 6),
                "families": ",".join(sorted(name for name in group["families"] if name)),
                "sight_states": ",".join(sorted(name for name in group["sight_states"] if name)),
                "hearing_states": ",".join(sorted(name for name in group["hearing_states"] if name)),
                "feeling_states": ",".join(sorted(name for name in group["feeling_states"] if name)),
            }
        )

    summary.sort(
        key=lambda item: (
            str(item.get("binding_state", "")),
            str(item.get("inner_state", "")),
            str(item.get("action", "")),
        )
    )
    detail.sort(key=lambda item: (str(item.get("run", "")), _safe_int(item.get("tick", 0))))
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, protocol_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_multisensory_inner_map.csv"
    summary_path = output_dir / "dio_mini_multisensory_inner_map_summary.csv"
    json_path = output_dir / "dio_mini_multisensory_inner_map.json"
    md_path = output_dir / "dio_mini_multisensory_inner_map.md"

    detail_fields = list(detail[0].keys()) if detail else [
        "run",
        "tick",
        "symbol_family",
        "action",
        "inner_state",
        "sight_state",
        "hearing_state",
        "feeling_state",
        "binding_state",
        "inner_sentence",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else [
        "binding_state",
        "inner_state",
        "contact_state",
        "action",
        "count",
        "reward_sum",
        "event_reward_sum",
        "avg_reward",
        "families",
        "sight_states",
        "hearing_states",
        "feeling_states",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "protocol_csv": str(protocol_csv),
                "detail": detail,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Multisensory Inner Map",
        "",
        "## Grenze",
        "- liest nur das passive Konsequenz-Innenlagen-Protokoll",
        "- schreibt kein Memory",
        "- beeinflusst keine Handlung",
        "- kein Gate",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine multisensorische Innenkarte gefunden")
    else:
        for row in summary:
            lines.append(
                f"- {row.get('binding_state', '-')}: count={row.get('count', 0)} "
                f"reward_sum={row.get('reward_sum', 0.0)} "
                f"inner={row.get('inner_state', '-')} contact={row.get('contact_state', '-')} "
                f"families={row.get('families', '-') or '-'}"
            )
    lines.extend(["", "## Erste Tick-Lesung"])
    for row in detail[:80]:
        lines.append(f"- run {row.get('run', '-')} tick {row.get('tick', '-')}: {row.get('inner_sentence', '-')}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive multisensory inner map for Mini-DIO")
    parser.add_argument("--protocol-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    protocol_csv = Path(args.protocol_csv)
    detail, summary = build_rows(protocol_csv)
    write_outputs(detail, summary, Path(args.output_dir), protocol_csv)
    print(f"multisensory_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary[:20]:
        print(
            f"{row['binding_state']} count={row['count']} "
            f"reward={row['reward_sum']} families={row['families']}"
        )


if __name__ == "__main__":
    main()
