"""Report passive emergent island lifecycle across Mini-DIO stages.

The report separates reality-bound recurring order from emergent movement:
popup, recurrence with variation, drift, coupling, split/merge hints, and
manifestation pressure.

Passive only. No runtime reads, no memory writes, no action, no gate, no entry,
no direction signal.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
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


VECTOR_FIELDS = [
    "avg_sehen_form_flow",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
    "avg_mini_recurrence_strength",
    "avg_mini_afterimage",
    "avg_mini_temporal_trust_support",
    "avg_mini_temporal_caution_support",
    "avg_mini_focus_tone",
    "avg_mini_trust_tone",
    "avg_mini_caution_tone",
    "avg_mini_strain_tone",
    "avg_mini_neuro_balance",
]


FIELDS = [
    "symbol_family",
    "lifecycle_state",
    "lifecycle_reading",
    "stage_count",
    "stage_trace",
    "first_stage",
    "last_stage",
    "missing_stage_count",
    "avg_episode_count",
    "max_episode_count",
    "avg_source_count",
    "max_source_count",
    "avg_vector_drift",
    "max_vector_drift",
    "variation_pressure",
    "reality_order_pressure",
    "island_presence_count",
    "island_presence_rate",
    "island_contact_count",
    "island_contact_rate",
    "island_partner_count",
    "island_partner_trace",
    "island_membership_trace",
    "merge_pressure",
    "split_pressure",
    "manifestation_pressure",
    "dominant_neuro_tone_trace",
    "dominant_temporal_state_trace",
    "dominant_action_trace",
    "dio_lifecycle_sentence",
]


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


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except (TypeError, ValueError):
        return default
    if result != result:
        return default
    return result


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value if value not in (None, "") else default))
    except (TypeError, ValueError):
        return default


def _parse_stage(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise ValueError(f"Stage must be LABEL=path: {value}")
    label, raw_path = value.split("=", 1)
    label = label.strip()
    if not label:
        raise ValueError(f"Stage label is empty: {value}")
    return label, Path(raw_path.strip())


def _split_pipe(value: Any) -> list[str]:
    return sorted({item.strip() for item in str(value or "").split("|") if item.strip() and item.strip() != "-"})


def _vector(row: dict[str, str]) -> list[float]:
    return [_safe_float(row.get(field)) for field in VECTOR_FIELDS]


def _distance(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    total = 0.0
    for a, b in zip(left, right):
        total += (a - b) * (a - b)
    return math.sqrt(total / max(1, min(len(left), len(right))))


def _mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _island_membership(island_rows: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    membership: dict[str, dict[str, Any]] = {}
    for row in island_rows:
        island_id = str(row.get("island_id", "") or "")
        families = _split_pipe(row.get("families"))
        if not island_id or not families:
            continue
        for family in families:
            item = membership.setdefault(
                family,
                {
                    "islands": [],
                    "partners": set(),
                    "max_family_count": 0,
                    "contact_count": 0,
                },
            )
            item["islands"].append(island_id)
            item["partners"].update(other for other in families if other != family)
            item["max_family_count"] = max(int(item["max_family_count"]), _safe_int(row.get("family_count"), len(families)))
            item["contact_count"] = int(item["contact_count"]) + 1
    return membership


def _lifecycle_state(
    *,
    stage_count: int,
    total_stages: int,
    variation_pressure: float,
    reality_order_pressure: float,
    island_presence_rate: float,
    island_contact_rate: float,
    merge_pressure: float,
    split_pressure: float,
    manifestation_pressure: float,
) -> str:
    if stage_count <= 1:
        return "sporadic_popup"
    if manifestation_pressure >= 0.68 and variation_pressure <= 0.20:
        return "reality_bound_manifestation_candidate"
    if manifestation_pressure >= 0.68 and island_contact_rate > 0.0:
        return "emergent_manifestation_candidate"
    if manifestation_pressure >= 0.68 and island_presence_rate > 0.0:
        return "isolated_emergent_variation_candidate"
    if merge_pressure > 0.0 and split_pressure > 0.0:
        return "emergent_reorganization_trace"
    if merge_pressure > 0.0:
        return "emergent_merge_contact_trace"
    if split_pressure > 0.0:
        return "emergent_split_drift_trace"
    if stage_count >= max(2, total_stages - 1) and reality_order_pressure >= 0.66:
        return "reality_order_trace"
    if variation_pressure > 0.20 and island_contact_rate > 0.0:
        return "recurring_emergent_variation_trace"
    if variation_pressure > 0.20 and island_presence_rate > 0.0:
        return "isolated_emergent_variation_trace"
    if variation_pressure > 0.20:
        return "recurring_drift_trace"
    return "recurring_soft_order_trace"


def _reading(state: str) -> str:
    return {
        "sporadic_popup": "taucht auf, aber noch ohne Wiederkehr",
        "reality_bound_manifestation_candidate": "stabile Ordnung mit Manifestationsdruck",
        "emergent_manifestation_candidate": "wiederkehrende Variation verdichtet sich Richtung Manifestation",
        "isolated_emergent_variation_candidate": "isolierte Variation baut Manifestationsdruck auf, aber noch ohne Kopplung",
        "emergent_reorganization_trace": "Kopplung und Teilung wirken gleichzeitig",
        "emergent_merge_contact_trace": "Insel findet Kopplung zu anderen Inseln",
        "emergent_split_drift_trace": "Insel verliert oder wechselt Kopplungsnaehe",
        "reality_order_trace": "wiederkehrende Ordnung, eher Realitaetsbezug als eigentliche Emergenz",
        "recurring_emergent_variation_trace": "Wiederkehr mit Variation und Inselkontakt",
        "isolated_emergent_variation_trace": "Wiederkehr mit Variation, aber noch ohne Kopplung",
        "recurring_drift_trace": "Wiederkehr mit innerer Drift",
        "recurring_soft_order_trace": "weiche Wiederkehr ohne starken Emergenzdruck",
    }.get(state, "passiv uneindeutig")


def _sentence(row: dict[str, Any]) -> str:
    family = row["symbol_family"]
    state = row["lifecycle_state"]
    if state == "reality_order_trace":
        return f"{family}: Wiederkehr wirkt wie realitaetsbezogene Ordnung; noch nicht der eigentliche Emergenzprozess."
    if state == "recurring_emergent_variation_trace":
        return f"{family}: Die Spur kehrt wieder, variiert und koppelt an Inseln; passiver Emergenzkeim."
    if state == "emergent_manifestation_candidate":
        return f"{family}: Variation und Wiederkehr bauen Manifestationsdruck auf; weiter passiv pruefen."
    if state == "isolated_emergent_variation_candidate":
        return f"{family}: Variation verdichtet sich isoliert; noch keine Verschmelzung mit anderen Inseln."
    if state == "reality_bound_manifestation_candidate":
        return f"{family}: Stabile Weltordnung wird mehrfach getragen; Manifestationskandidat ohne Handlungsfreigabe."
    if state == "sporadic_popup":
        return f"{family}: Aufploppen ohne ausreichende Wiederkehr."
    return f"{family}: {row['lifecycle_reading']}."


def build_report(stages: list[tuple[str, list[dict[str, str]]]], island_stages: dict[str, list[dict[str, str]]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    total_stages = len(stages)
    stage_index = {label: index for index, (label, _) in enumerate(stages)}
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    island_by_stage = {label: _island_membership(rows) for label, rows in island_stages.items()}

    for label, rows in stages:
        for row in rows:
            family = str(row.get("symbol_family", "") or "")
            if not family:
                continue
            membership = island_by_stage.get(label, {}).get(family, {})
            by_family[family].append(
                {
                    "stage": label,
                    "stage_index": stage_index[label],
                    "row": row,
                    "vector": _vector(row),
                    "membership": membership,
                }
            )

    output_rows: list[dict[str, Any]] = []
    for family, items in sorted(by_family.items()):
        items.sort(key=lambda item: int(item["stage_index"]))
        stage_labels = [str(item["stage"]) for item in items]
        episode_counts = [_safe_float(item["row"].get("episode_count")) for item in items]
        source_counts = [_safe_float(item["row"].get("source_count")) for item in items]
        distances = [_distance(left["vector"], right["vector"]) for left, right in zip(items, items[1:])]
        avg_drift = _mean(distances)
        max_drift = max(distances) if distances else 0.0
        stage_count = len(items)
        first_index = int(items[0]["stage_index"])
        last_index = int(items[-1]["stage_index"])
        missing_stage_count = max(0, (last_index - first_index + 1) - stage_count)

        partner_sets = [set(item["membership"].get("partners", set()) or set()) for item in items]
        all_partners = set().union(*partner_sets) if partner_sets else set()
        island_presence_count = sum(1 for item in items if item["membership"])
        island_presence_rate = island_presence_count / max(1, stage_count)
        island_contact_count = sum(1 for partners in partner_sets if partners)
        island_contact_rate = island_contact_count / max(1, stage_count)
        island_trace_parts: list[str] = []
        for item in items:
            islands = item["membership"].get("islands", []) if item["membership"] else []
            island_trace_parts.append(f"{item['stage']}:{'|'.join(islands) if islands else '-'}")
        partner_trace_parts: list[str] = []
        for item, partners in zip(items, partner_sets):
            partner_trace_parts.append(f"{item['stage']}:{'|'.join(sorted(partners)) if partners else '-'}")

        partner_counts = [len(partners) for partners in partner_sets]
        merge_pressure = max(0.0, (max(partner_counts) - partner_counts[0]) / max(1, max(partner_counts))) if partner_counts else 0.0
        split_pressure = 0.0
        if len(partner_sets) >= 2:
            first = partner_sets[0]
            latest = partner_sets[-1]
            lost = len(first - latest)
            gained = len(latest - first)
            split_pressure = min(1.0, (lost + gained) / max(1, len(first | latest)))

        # Variation is normalized softly by observed vector distance. This is
        # diagnostic scale only, not a runtime threshold.
        variation_pressure = min(1.0, avg_drift / 0.35)
        reality_order_pressure = max(0.0, 1.0 - variation_pressure) * (stage_count / max(1, total_stages))
        manifestation_pressure = min(
            1.0,
            (stage_count / max(1, total_stages)) * 0.35
            + min(1.0, _mean(episode_counts) / 12.0) * 0.25
            + island_presence_rate * 0.20
            + max(0.0, 1.0 - min(1.0, avg_drift / 0.35)) * 0.20,
        )

        state = _lifecycle_state(
            stage_count=stage_count,
            total_stages=total_stages,
            variation_pressure=variation_pressure,
            reality_order_pressure=reality_order_pressure,
            island_presence_rate=island_presence_rate,
            island_contact_rate=island_contact_rate,
            merge_pressure=merge_pressure,
            split_pressure=split_pressure,
            manifestation_pressure=manifestation_pressure,
        )
        row = {
            "symbol_family": family,
            "lifecycle_state": state,
            "lifecycle_reading": _reading(state),
            "stage_count": stage_count,
            "stage_trace": "|".join(stage_labels),
            "first_stage": stage_labels[0],
            "last_stage": stage_labels[-1],
            "missing_stage_count": missing_stage_count,
            "avg_episode_count": round(_mean(episode_counts), 6),
            "max_episode_count": round(max(episode_counts) if episode_counts else 0.0, 6),
            "avg_source_count": round(_mean(source_counts), 6),
            "max_source_count": round(max(source_counts) if source_counts else 0.0, 6),
            "avg_vector_drift": round(avg_drift, 9),
            "max_vector_drift": round(max_drift, 9),
            "variation_pressure": round(variation_pressure, 9),
            "reality_order_pressure": round(reality_order_pressure, 9),
            "island_presence_count": island_presence_count,
            "island_presence_rate": round(island_presence_rate, 9),
            "island_contact_count": island_contact_count,
            "island_contact_rate": round(island_contact_rate, 9),
            "island_partner_count": len(all_partners),
            "island_partner_trace": ";".join(partner_trace_parts),
            "island_membership_trace": ";".join(island_trace_parts),
            "merge_pressure": round(merge_pressure, 9),
            "split_pressure": round(split_pressure, 9),
            "manifestation_pressure": round(manifestation_pressure, 9),
            "dominant_neuro_tone_trace": "|".join(str(item["row"].get("dominant_neuro_tone", "") or "-") for item in items),
            "dominant_temporal_state_trace": "|".join(str(item["row"].get("dominant_temporal_state", "") or "-") for item in items),
            "dominant_action_trace": "|".join(str(item["row"].get("dominant_action", "") or "-") for item in items),
            **PASSIVE_FLAGS,
        }
        row["dio_lifecycle_sentence"] = _sentence(row)
        output_rows.append(row)

    counts: dict[str, int] = {}
    for row in output_rows:
        counts[str(row["lifecycle_state"])] = counts.get(str(row["lifecycle_state"]), 0) + 1
    summary = {
        "stage_count": total_stages,
        "stages": [label for label, _ in stages],
        "family_count": len(output_rows),
        "lifecycle_state_counts": counts,
        "top_manifestation_candidates": [
            row["symbol_family"]
            for row in sorted(output_rows, key=lambda item: -float(item["manifestation_pressure"]))[:20]
        ],
        "top_emergent_variation": [
            row["symbol_family"]
            for row in sorted(output_rows, key=lambda item: -float(item["variation_pressure"]))[:20]
        ],
        **PASSIVE_FLAGS,
    }
    output_rows.sort(
        key=lambda row: (
            -float(row["manifestation_pressure"]),
            -float(row["variation_pressure"]),
            str(row["symbol_family"]),
        )
    )
    return summary, output_rows


def write_report(output_dir: Path, summary: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_emergent_lifecycle.csv", rows, FIELDS + list(PASSIVE_FLAGS))
    (output_dir / "passive_emergent_lifecycle.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        "# Passive Emergent Lifecycle",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Leittrennung",
        "",
        "```text",
        "Realitaetsbezogene Ordnung:",
        "  wiederholte aehnliche Weltlage erzeugt wiederholte innere Ordnung.",
        "",
        "Eigentliche Emergenz:",
        "  Aufploppen, Drift, Variation, Kopplung, Teilung, Verdichtung.",
        "",
        "Manifestation:",
        "  emergente Bewegung wird ueber Weltkontakt stabil genug getragen.",
        "```",
        "",
        "## Zusammenfassung",
        "",
        f"- Stages: {' | '.join(summary['stages'])}",
        f"- Familien: {summary['family_count']}",
        "",
        "## Zustaende",
        "",
    ]
    for key, value in sorted(summary["lifecycle_state_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Top Manifestationsdruck", ""])
    for row in rows[:20]:
        lines.append(
            "- {family}: {state}; manifestation={manifest}; variation={variation}; "
            "presence={presence}; coupling={coupling}; stages={stages}".format(
                family=row["symbol_family"],
                state=row["lifecycle_state"],
                manifest=row["manifestation_pressure"],
                variation=row["variation_pressure"],
                presence=row["island_presence_rate"],
                coupling=row["island_contact_rate"],
                stages=row["stage_trace"],
            )
        )
    (output_dir / "passive_emergent_lifecycle.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", action="append", required=True, help="LABEL=passive_cluster_meaning_space.csv")
    parser.add_argument("--island-stage", action="append", default=[], help="LABEL=passive_semantic_matrix_islands.csv")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    stages = [(label, _read_csv(path)) for label, path in (_parse_stage(value) for value in args.stage)]
    island_stages = {label: _read_csv(path) for label, path in (_parse_stage(value) for value in args.island_stage)}
    summary, rows = build_report(stages, island_stages)
    write_report(args.output_dir, summary, rows)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
