"""Report recurring passive fragments across fragment-island diagnostics.

This is a passive cross-pair diagnosis. It asks whether the same fragment
appears in several passive island contexts. It does not write runtime memory
and does not influence Mini-DIO behavior.
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


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


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
    name = name.replace("dio_mini_passive_fragment_islands_", "")
    return name or path.stem


def _split(value: object) -> list[str]:
    return sorted({item.strip() for item in str(value or "").split("|") if item.strip()})


def _state_for(fragment_group: str, source_count: int) -> str:
    if fragment_group == "persistent_shared_core" and source_count > 1:
        return "recurring_passive_shared_core_fragment"
    if fragment_group == "target_only_new_fragments" and source_count > 1:
        return "recurring_passive_target_expansion_fragment"
    if fragment_group == "gained_shared_fragments" and source_count > 1:
        return "recurring_passive_new_shared_fragment"
    if source_count > 1:
        return "recurring_passive_fragment_trace"
    return "single_passive_fragment_trace"


def build_fragment_recurrence(paths: list[Path]) -> tuple[list[dict], list[dict]]:
    grouped: dict[tuple[str, str], dict] = {}
    for path in paths:
        source = _source_label(path)
        for row in _read_csv(path):
            target = str(row.get("target_family", "") or "")
            related = str(row.get("related_family", "") or "")
            fragment_group = str(row.get("fragment_group", "") or "")
            island_state = str(row.get("fragment_island_state", "") or "")
            island_symbol = str(row.get("passive_fragment_island_symbol", "") or "")
            if not target or not fragment_group:
                continue
            for fragment in _split(row.get("fragments")):
                key = (fragment_group, fragment)
                item = grouped.setdefault(
                    key,
                    {
                        "fragment_group": fragment_group,
                        "fragment": fragment,
                        "sources": set(),
                        "target_families": set(),
                        "related_families": set(),
                        "island_states": set(),
                        "island_symbols": set(),
                    },
                )
                item["sources"].add(source)
                item["target_families"].add(target)
                if related:
                    item["related_families"].add(related)
                if island_state:
                    item["island_states"].add(island_state)
                if island_symbol:
                    item["island_symbols"].add(island_symbol)

    rows: list[dict] = []
    summary_groups: dict[str, dict] = {}
    for item in grouped.values():
        source_count = len(item["sources"])
        state = _state_for(str(item["fragment_group"]), source_count)
        row = {
            "fragment_recurrence_state": state,
            "fragment_group": item["fragment_group"],
            "fragment": item["fragment"],
            "source_count": source_count,
            "sources": "|".join(sorted(item["sources"])),
            "target_families": "|".join(sorted(item["target_families"])),
            "related_families": "|".join(sorted(item["related_families"])),
            "island_states": "|".join(sorted(item["island_states"])),
            "island_symbols": "|".join(sorted(item["island_symbols"])),
            **BOUNDARY,
        }
        rows.append(row)
        summary = summary_groups.setdefault(
            state,
            {
                "fragment_recurrence_state": state,
                "fragment_count": 0,
                "fragments": [],
            },
        )
        summary["fragment_count"] += 1
        summary["fragments"].append(f"{item['fragment_group']}:{item['fragment']}")

    rows.sort(
        key=lambda row: (
            row["fragment_recurrence_state"].startswith("single"),
            -int(row["source_count"]),
            str(row["fragment_group"]),
            str(row["fragment"]),
        )
    )
    summary_rows = [
        {
            "fragment_recurrence_state": item["fragment_recurrence_state"],
            "fragment_count": int(item["fragment_count"]),
            "fragments": "|".join(sorted(item["fragments"])),
            **BOUNDARY,
        }
        for item in summary_groups.values()
    ]
    summary_rows.sort(key=lambda row: (-int(row["fragment_count"]), str(row["fragment_recurrence_state"])))
    return rows, summary_rows


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_fragment_recurrence.csv"
    summary_path = output_dir / "passive_fragment_recurrence_summary.csv"
    json_path = output_dir / "passive_fragment_recurrence.json"
    md_path = output_dir / "passive_fragment_recurrence.md"
    _write_csv(detail_path, rows, ["fragment_recurrence_state", "fragment_group", "fragment"])
    _write_csv(summary_path, summary, ["fragment_recurrence_state", "fragment_count"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": BOUNDARY,
                "fragments": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Fragment Recurrence",
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
        lines.append(f"- {row['fragment_recurrence_state']}: {row['fragment_count']}")
    lines.extend(["", "## Details"])
    for row in rows[:30]:
        lines.append(
            f"- {row['fragment_recurrence_state']}: {row['fragment_group']} "
            f"{row['fragment']} sources={row['source_count']}"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fragment-islands", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    paths = _expand_patterns(args.fragment_islands)
    rows, summary = build_fragment_recurrence(paths)
    write_outputs(rows, summary, Path(args.output_dir))
    print(f"island_sources={len(paths)} fragments={len(rows)} summary_rows={len(summary)}")
    for row in summary:
        print(f"{row['fragment_recurrence_state']}={row['fragment_count']}")


if __name__ == "__main__":
    main()
