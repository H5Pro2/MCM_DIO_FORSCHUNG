"""Inspect why a passive sign cluster drifts.

The lupe separates whole-cluster nearness from fragment-level nearness. It is
diagnostic only: no runtime memory, no action influence, no direction signal.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
from pathlib import Path


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


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


def _split(value: object) -> set[str]:
    return {item.strip() for item in str(value or "").split("|") if item.strip()}


def _join(values: set[str] | list[str]) -> str:
    return "|".join(sorted(values))


def _expand_patterns(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            paths.extend(Path(match) for match in matches)
        else:
            paths.append(Path(pattern))
    unique = {str(path.resolve()): path for path in paths}
    return [unique[key] for key in sorted(unique)]


def _source_label(path: Path) -> str:
    name = path.parent.name or path.stem
    name = name.replace("dio_mini_passive_sign_cluster_candidates_", "")
    name = name.replace("dio_0x52_", "")
    return name or path.stem


def _select_rows(paths: list[Path], target: str, related: str) -> list[dict]:
    selected: list[dict] = []
    for path in paths:
        source = _source_label(path)
        for row in _read_csv(path):
            if str(row.get("target_family", "") or "") != target:
                continue
            if str(row.get("related_family", "") or "") != related:
                continue
            item = dict(row)
            item["_source"] = source
            selected.append(item)
    return selected


def _drift_cause(first: dict, latest: dict) -> str:
    first_shared = _split(first.get("shared_field_trace"))
    latest_shared = _split(latest.get("shared_field_trace"))
    first_target = _split(first.get("target_stable_fields"))
    latest_target = _split(latest.get("target_stable_fields"))
    first_related = _split(first.get("related_stable_fields"))
    latest_related = _split(latest.get("related_stable_fields"))
    lost_shared = first_shared - latest_shared
    gained_shared = latest_shared - first_shared
    target_gains = latest_target - first_target
    related_gains = latest_related - first_related
    target_only_gains = target_gains - latest_related
    related_only_gains = related_gains - latest_target
    field_delta = _safe_float(latest.get("avg_field_overlap")) - _safe_float(first.get("avg_field_overlap"))
    relation_delta = _safe_float(latest.get("avg_relation_score")) - _safe_float(first.get("avg_relation_score"))

    if lost_shared:
        return "shared_core_fragment_loss"
    if gained_shared and not target_only_gains and not related_only_gains:
        return "new_shared_fragment_integration"
    if target_only_gains and not related_only_gains and field_delta < 0:
        return "target_sign_expanded_beyond_shared_core"
    if related_only_gains and not target_only_gains and field_delta < 0:
        return "related_sign_expanded_beyond_shared_core"
    if target_only_gains or related_only_gains:
        return "asymmetric_fragment_expansion"
    if relation_delta < 0:
        return "whole_relation_weakened_without_fragment_change"
    return "no_clear_fragment_drift"


def build_lupe(rows: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    timeline: list[dict] = []
    for index, row in enumerate(rows):
        target_fields = _split(row.get("target_stable_fields"))
        related_fields = _split(row.get("related_stable_fields"))
        shared_fields = _split(row.get("shared_field_trace"))
        target_only = target_fields - related_fields
        related_only = related_fields - target_fields
        timeline.append(
            {
                "source": str(row.get("_source", "") or f"source_{index + 1}"),
                "target_family": str(row.get("target_family", "") or ""),
                "related_family": str(row.get("related_family", "") or ""),
                "cluster_symbol": str(row.get("passive_cluster_symbol", "") or ""),
                "cluster_candidate_state": str(row.get("cluster_candidate_state", "") or ""),
                "relation_stability_state": str(row.get("relation_stability_state", "") or ""),
                "relation_source_count": _safe_int(row.get("relation_source_count")),
                "avg_relation_score": round(_safe_float(row.get("avg_relation_score")), 6),
                "avg_field_overlap": round(_safe_float(row.get("avg_field_overlap")), 6),
                "avg_afterlook_overlap": round(_safe_float(row.get("avg_afterlook_overlap")), 6),
                "target_sign_symbol": str(row.get("target_sign_symbol", "") or ""),
                "related_sign_symbol": str(row.get("related_sign_symbol", "") or ""),
                "shared_field_trace": _join(shared_fields),
                "target_only_fragments": _join(target_only),
                "related_only_fragments": _join(related_only),
                "target_fragment_count": len(target_fields),
                "related_fragment_count": len(related_fields),
                "shared_fragment_count": len(shared_fields),
                "passive_only": True,
                "writes_runtime_memory": False,
                "read_by_mini_dio": False,
                "influences_action": False,
                "is_gate": False,
                "is_motoric": False,
                "is_entry_signal": False,
                "is_direction_signal": False,
            }
        )

    if not rows:
        return [], [], []

    first = rows[0]
    latest = rows[-1]
    shared_sets = [_split(row.get("shared_field_trace")) for row in rows]
    target_sets = [_split(row.get("target_stable_fields")) for row in rows]
    related_sets = [_split(row.get("related_stable_fields")) for row in rows]
    persistent_shared = set.intersection(*shared_sets) if shared_sets else set()
    all_shared = set.union(*shared_sets) if shared_sets else set()
    first_shared = shared_sets[0] if shared_sets else set()
    latest_shared = shared_sets[-1] if shared_sets else set()
    first_target = target_sets[0] if target_sets else set()
    latest_target = target_sets[-1] if target_sets else set()
    first_related = related_sets[0] if related_sets else set()
    latest_related = related_sets[-1] if related_sets else set()

    fragment_rows = [
        {
            "fragment_group": "persistent_shared_core",
            "fragments": _join(persistent_shared),
            "fragment_count": len(persistent_shared),
            "reading": "Ganzheitsnaehe besitzt einen stabilen gemeinsamen Kern.",
            "passive_only": True,
            "influences_action": False,
        },
        {
            "fragment_group": "all_shared_fragments",
            "fragments": _join(all_shared),
            "fragment_count": len(all_shared),
            "reading": "Alle je geteilten Fragmente ueber die Clusterstaende.",
            "passive_only": True,
            "influences_action": False,
        },
        {
            "fragment_group": "lost_shared_fragments",
            "fragments": _join(first_shared - latest_shared),
            "fragment_count": len(first_shared - latest_shared),
            "reading": "Fragmente, die aus der gemeinsamen Naehe gefallen sind.",
            "passive_only": True,
            "influences_action": False,
        },
        {
            "fragment_group": "gained_shared_fragments",
            "fragments": _join(latest_shared - first_shared),
            "fragment_count": len(latest_shared - first_shared),
            "reading": "Fragmente, die neu gemeinsam wurden.",
            "passive_only": True,
            "influences_action": False,
        },
        {
            "fragment_group": "target_only_new_fragments",
            "fragments": _join((latest_target - first_target) - latest_related),
            "fragment_count": len((latest_target - first_target) - latest_related),
            "reading": "Neue Fragmente nur auf der Zielzeichen-Seite.",
            "passive_only": True,
            "influences_action": False,
        },
        {
            "fragment_group": "related_only_new_fragments",
            "fragments": _join((latest_related - first_related) - latest_target),
            "fragment_count": len((latest_related - first_related) - latest_target),
            "reading": "Neue Fragmente nur auf der Nachbarzeichen-Seite.",
            "passive_only": True,
            "influences_action": False,
        },
    ]

    summary = [
        {
            "target_family": str(latest.get("target_family", "") or ""),
            "related_family": str(latest.get("related_family", "") or ""),
            "cluster_drift_reading": _drift_cause(first, latest),
            "source_count": len(rows),
            "first_cluster_state": str(first.get("cluster_candidate_state", "") or ""),
            "latest_cluster_state": str(latest.get("cluster_candidate_state", "") or ""),
            "first_cluster_symbol": str(first.get("passive_cluster_symbol", "") or ""),
            "latest_cluster_symbol": str(latest.get("passive_cluster_symbol", "") or ""),
            "relation_score_delta": round(
                _safe_float(latest.get("avg_relation_score")) - _safe_float(first.get("avg_relation_score")),
                6,
            ),
            "field_overlap_delta": round(
                _safe_float(latest.get("avg_field_overlap")) - _safe_float(first.get("avg_field_overlap")),
                6,
            ),
            "persistent_shared_core": _join(persistent_shared),
            "latest_target_only_fragments": _join(latest_target - latest_related),
            "latest_related_only_fragments": _join(latest_related - latest_target),
            "whole_nearness_vs_fragment_reading": (
                "Ganzheitsnaehe bleibt lesbar, aber Detailnaehe ist fragmentiert."
                if persistent_shared and ((latest_target - latest_related) or (latest_related - latest_target))
                else "Keine klare Trennung zwischen Ganzheit und Fragmenten."
            ),
            "passive_only": True,
            "writes_runtime_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "is_direction_signal": False,
        }
    ]
    return timeline, fragment_rows, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(timeline: list[dict], fragments: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    timeline_path = output_dir / "passive_cluster_drift_lupe_timeline.csv"
    fragments_path = output_dir / "passive_cluster_drift_lupe_fragments.csv"
    summary_path = output_dir / "passive_cluster_drift_lupe_summary.csv"
    json_path = output_dir / "passive_cluster_drift_lupe.json"
    md_path = output_dir / "passive_cluster_drift_lupe.md"
    _write_csv(timeline_path, timeline, ["source", "target_family", "related_family"])
    _write_csv(fragments_path, fragments, ["fragment_group", "fragments"])
    _write_csv(summary_path, summary, ["target_family", "related_family", "cluster_drift_reading"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": {
                    "passive_only": True,
                    "writes_runtime_memory": False,
                    "read_by_mini_dio": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_entry_signal": False,
                    "is_direction_signal": False,
                },
                "timeline": timeline,
                "fragments": fragments,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Cluster Drift Lupe",
        "",
        "## Grenze",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- keine Richtung",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(f"- reading: {row['cluster_drift_reading']}")
        lines.append(f"- whole/detail: {row['whole_nearness_vs_fragment_reading']}")
        lines.append(f"- shared core: {row['persistent_shared_core']}")
        lines.append(f"- target only: {row['latest_target_only_fragments']}")
        lines.append(f"- related only: {row['latest_related_only_fragments']}")
    lines.extend(["", "## Timeline"])
    for row in timeline:
        lines.append(
            f"- {row['source']}: {row['cluster_candidate_state']} "
            f"field={row['avg_field_overlap']} score={row['avg_relation_score']} "
            f"shared={row['shared_field_trace']}"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cluster-candidates", nargs="+", required=True)
    parser.add_argument("--target-family", required=True)
    parser.add_argument("--related-family", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    paths = _expand_patterns(args.cluster_candidates)
    rows = _select_rows(paths, args.target_family, args.related_family)
    timeline, fragments, summary = build_lupe(rows)
    write_outputs(timeline, fragments, summary, Path(args.output_dir))
    reading = summary[0]["cluster_drift_reading"] if summary else "not_seen"
    print(f"sources={len(paths)} selected={len(rows)} reading={reading}")
    for row in summary:
        print(row["whole_nearness_vs_fragment_reading"])


if __name__ == "__main__":
    main()
