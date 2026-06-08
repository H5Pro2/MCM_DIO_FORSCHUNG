"""Create controlled Mini-DIO probe variant J.

Variant J is a deterministic follow-up after I. It keeps the same controlled
probe structure, but adds a second world-contact movement. The goal is to test
whether passive emergent density centers remain stable, drift, or reorganize.

This changes only OHLCV input data. It does not change Mini-DIO logic, memory,
gates, entries, direction, or runtime behavior.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


PROBES = {
    20: "emergenz_richtungsvarianz",
    21: "emergenz_hoervarianz",
    22: "emergenz_skalenvarianz",
    23: "emergenz_temporalvarianz",
    24: "emergenz_minimalsensorik",
    25: "emergenz_kontrastvarianz",
    26: "emergenz_signaturdrift",
}


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_rows(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _fmt_price(value: float) -> str:
    return f"{value:.2f}"


def _fmt_volume(value: float) -> str:
    return f"{value:.1f}"


def mutate_rows(rows: list[dict], probe: int) -> list[dict]:
    """Return a deterministic second-contact continuation of variant I."""

    if not rows:
        return []
    timestamp_shift = 2_400_000_000_000 + (probe * 19_000_000)
    probe_phase = ((probe % 7) - 3) / 3.0
    mutated: list[dict] = []

    for index, row in enumerate(rows):
        open_price = _safe_float(row.get("open"), 100.0)
        high_price = _safe_float(row.get("high"), open_price)
        low_price = _safe_float(row.get("low"), open_price)
        close_price = _safe_float(row.get("close"), open_price)
        volume = _safe_float(row.get("volume"), 0.0)

        center = (open_price + close_price) / 2.0
        body = close_price - open_price
        upper_wick = max(0.0, high_price - max(open_price, close_price))
        lower_wick = max(0.0, min(open_price, close_price) - low_price)

        local_phase = ((index % 19) - 9) / 9.0
        slow_drift = ((index // 9) % 5 - 2) / 2.0
        pulse = ((index % 8) - 3.5) / 3.5

        center_shift = (local_phase * 0.0048) + (slow_drift * 0.0062) + (probe_phase * 0.0024)
        body_scale = max(0.58, 1.0 + (pulse * 0.038) + (slow_drift * 0.022))
        upper_scale = max(0.58, 1.0 + (local_phase * 0.028) + (abs(pulse) * 0.014))
        lower_scale = max(0.58, 1.0 - (local_phase * 0.026) + (abs(slow_drift) * 0.016))
        volume_scale = max(0.80, min(1.20, 1.0 + (abs(pulse) * 0.024) + (abs(local_phase) * 0.026)))

        new_center = center + center_shift
        new_body = body * body_scale
        new_open = new_center - (new_body / 2.0)
        new_close = new_center + (new_body / 2.0)
        new_high = max(new_open, new_close) + max(0.02, upper_wick * upper_scale)
        new_low = min(new_open, new_close) - max(0.02, lower_wick * lower_scale)
        new_volume = max(1.0, volume * volume_scale)

        new_row = dict(row)
        try:
            new_row["timestamp_ms"] = str(int(float(row.get("timestamp_ms", 0))) + timestamp_shift)
        except Exception:
            new_row["timestamp_ms"] = str(timestamp_shift + index * 300_000)
        new_row["open"] = _fmt_price(new_open)
        new_row["high"] = _fmt_price(new_high)
        new_row["low"] = _fmt_price(new_low)
        new_row["close"] = _fmt_price(new_close)
        new_row["volume"] = _fmt_volume(new_volume)
        mutated.append(new_row)

    return mutated


def create_variant_j(data_dir: Path) -> list[Path]:
    written: list[Path] = []
    for probe, label in PROBES.items():
        source = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteI_weltkontakt_5m_SOLUSDT.csv"
        target = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteJ_folgekontakt_5m_SOLUSDT.csv"
        rows = _read_rows(source)
        if not rows:
            continue
        _write_rows(target, mutate_rows(rows, probe), list(rows[0].keys()))
        written.append(target)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Create controlled Mini-DIO variant J CSVs.")
    parser.add_argument("--data-dir", default="data")
    args = parser.parse_args()
    for path in create_variant_j(Path(args.data_dir)):
        print(path)


if __name__ == "__main__":
    main()
