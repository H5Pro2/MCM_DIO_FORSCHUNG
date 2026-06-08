"""Report passive fragment islands from cluster-drift lupe output.

Fragment islands are diagnostic only. They describe whether a drifting passive
cluster contains a stable shared core or asymmetric extension fragments. The
report does not write runtime memory and does not influence Mini-DIO action.
"""

from __future__ import annotations

import argparse
import csv
import glob
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


def _base36(number: int) -> str:
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    number = abs(int(number))
    if number == 0:
        return "0"
    chars: list[str] = []
    while number:
        number, rem = divmod(number, 36)
        chars.append(alphabet[rem])
    return "".join(reversed(chars))


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


def _split(value: object) -> list[str]:
    return sorted({item.strip() for item in str(value or "").split("|") if item.strip()})


def _join(values: list[str] | set[str]) -> str:
    return "|".join(sorted(values))


def _make_island_symbol(payload: dict) -> str:
    identity = "|".join(
        [
            str(payload.get("target_family", "") or ""),
            str(payload.get("related_family", "") or ""),
            str(payload.get("fragment_island_state", "") or ""),
            str(payload.get("fragment_group", "") or ""),
            str(payload.get("fragments", "") or ""),
        ]
    )
    hash_value = 2166136261
    for char in identity:
        hash_value ^= ord(char) + 101
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    return f"dio_fragment_island_{_base36(hash_value).rjust(7, '0')}"


def _island_state(fragment_group: str, fragment_count: int, source_count: int) -> str:
    if fragment_group == "persistent_shared_core" and fragment_count >= 2 and source_count >= 2:
        return "passive_fragment_island_shared_core"
    if fragment_group == "target_only_new_fragments" and fragment_count >= 2:
        return "passive_fragment_island_target_expansion"
    if fragment_group == "related_only_new_fragments" and fragment_count >= 2:
        return "passive_fragment_island_related_expansion"
    if fragment_count > 0:
        return "passive_fragment_trace"
    return "empty_fragment_trace"


def _island_sentence(row: dict) -> str:
    state = str(row.get("fragment_island_state", "") or "")
    target = str(row.get("target_family", "") or "")
    related = str(row.get("related_family", "") or "")
    fragments = str(row.get("fragments", "") or "")
    if state == "passive_fragment_island_shared_core":
        return (
            f"{target}+{related}: Diese Fragmente bilden einen stabilen gemeinsamen "
            f"Kern ({fragments}). Ich halte das nur als passive Innenkarte."
        )
    if state == "passive_fragment_island_target_expansion":
        return (
            f"{target}: Diese Fragmente erweitern die Zielsignatur ({fragments}). "
            "Das ist Eigenverdichtung, keine Handlung."
        )
    if state == "passive_fragment_island_related_expansion":
        return (
            f"{related}: Diese Fragmente erweitern die Nachbarsignatur ({fragments}). "
            "Das ist Eigenverdichtung, keine Handlung."
        )
    if state == "passive_fragment_trace":
        return f"{target}+{related}: Diese Fragmente sind sichtbar, aber noch keine Insel."
    return f"{target}+{related}: Keine Fragmentinsel sichtbar."


def _load_lupe(path: Path) -> tuple[list[dict], list[dict], list[dict]]:
    if path.suffix.lower() == ".json":
        payload = _read_json(path)
        return (
            list(payload.get("timeline", []) or []),
            list(payload.get("fragments", []) or []),
            list(payload.get("summary", []) or []),
        )
    if path.name.endswith("_fragments.csv"):
        fragments = _read_csv(path)
        summary_path = path.with_name("passive_cluster_drift_lupe_summary.csv")
        timeline_path = path.with_name("passive_cluster_drift_lupe_timeline.csv")
        return _read_csv(timeline_path), fragments, _read_csv(summary_path)
    if path.name.endswith("_summary.csv"):
        summary = _read_csv(path)
        fragments_path = path.with_name("passive_cluster_drift_lupe_fragments.csv")
        timeline_path = path.with_name("passive_cluster_drift_lupe_timeline.csv")
        return _read_csv(timeline_path), _read_csv(fragments_path), summary
    return [], [], []


def build_fragment_islands(paths: list[Path]) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    groups: dict[str, dict] = {}

    for path in paths:
        timeline, fragments, summary_rows = _load_lupe(path)
        if not summary_rows:
            continue
        summary = dict(summary_rows[0])
        target = str(summary.get("target_family", "") or "")
        related = str(summary.get("related_family", "") or "")
        source_count = _safe_int(summary.get("source_count"))
        latest_cluster_symbol = str(summary.get("latest_cluster_symbol", "") or "")
        drift_reading = str(summary.get("cluster_drift_reading", "") or "")
        latest_timeline = dict(timeline[-1]) if timeline else {}
        persistent_shared = ""
        for fragment in fragments:
            if str(fragment.get("fragment_group", "") or "") == "persistent_shared_core":
                persistent_shared = _join(_split(fragment.get("fragments")))
                break

        for fragment in fragments:
            fragment_group = str(fragment.get("fragment_group", "") or "")
            fragment_list = _split(fragment.get("fragments"))
            fragment_count = len(fragment_list)
            if fragment_group == "all_shared_fragments" and _join(fragment_list) == persistent_shared:
                continue
            state = _island_state(fragment_group, fragment_count, source_count)
            if state == "empty_fragment_trace":
                continue
            payload = {
                "target_family": target,
                "related_family": related,
                "latest_cluster_symbol": latest_cluster_symbol,
                "cluster_drift_reading": drift_reading,
                "fragment_group": fragment_group,
                "fragment_island_state": state,
                "fragments": _join(fragment_list),
                "fragment_count": fragment_count,
                "source_count": source_count,
                "latest_field_overlap": round(_safe_float(latest_timeline.get("avg_field_overlap")), 6),
                "latest_relation_score": round(_safe_float(latest_timeline.get("avg_relation_score")), 6),
                "latest_target_sign_symbol": str(latest_timeline.get("target_sign_symbol", "") or ""),
                "latest_related_sign_symbol": str(latest_timeline.get("related_sign_symbol", "") or ""),
                **BOUNDARY,
            }
            payload["passive_fragment_island_symbol"] = _make_island_symbol(payload)
            payload["dio_sentence"] = _island_sentence(payload)
            rows.append(payload)

            group = groups.setdefault(
                state,
                {
                    "fragment_island_state": state,
                    "island_count": 0,
                    "fragment_groups": [],
                    "island_symbols": [],
                },
            )
            group["island_count"] += 1
            group["fragment_groups"].append(fragment_group)
            group["island_symbols"].append(payload["passive_fragment_island_symbol"])

    rows.sort(
        key=lambda row: (
            row["fragment_island_state"] != "passive_fragment_island_shared_core",
            row["fragment_island_state"] != "passive_fragment_island_target_expansion",
            -int(row["fragment_count"]),
            str(row["target_family"]),
            str(row["related_family"]),
            str(row["fragment_group"]),
        )
    )
    summary = [
        {
            "fragment_island_state": group["fragment_island_state"],
            "island_count": int(group["island_count"]),
            "fragment_groups": "|".join(sorted(set(group["fragment_groups"]))),
            "island_symbols": "|".join(sorted(set(group["island_symbols"]))),
            **BOUNDARY,
        }
        for group in groups.values()
    ]
    summary.sort(key=lambda row: (-int(row["island_count"]), str(row["fragment_island_state"])))
    return rows, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_fragment_islands.csv"
    summary_path = output_dir / "passive_fragment_islands_summary.csv"
    json_path = output_dir / "passive_fragment_islands.json"
    md_path = output_dir / "passive_fragment_islands.md"

    _write_csv(detail_path, rows, ["target_family", "related_family", "fragment_island_state"])
    _write_csv(summary_path, summary, ["fragment_island_state", "island_count"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": BOUNDARY,
                "rows": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Passive Fragment Islands",
        "",
        "## Grenze",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- keine Richtung",
        "",
        "## Islands",
    ]
    for row in rows:
        lines.append(
            f"- {row['passive_fragment_island_symbol']}: "
            f"{row['fragment_island_state']} fragments={row['fragments']}"
        )
    lines.extend(["", "## Summary"])
    for row in summary:
        lines.append(f"- {row['fragment_island_state']}: {row['island_count']}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lupe", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    paths = _expand_patterns(args.lupe)
    rows, summary = build_fragment_islands(paths)
    write_outputs(rows, summary, Path(args.output_dir))
    print(f"sources={len(paths)} fragment_islands={len(rows)} states={len(summary)}")
    for row in summary:
        print(f"{row['fragment_island_state']}={row['island_count']}")


if __name__ == "__main__":
    main()
