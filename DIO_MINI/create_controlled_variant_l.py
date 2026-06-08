"""Create controlled Mini-DIO probe variant L.

Variant L is a deterministic follow-up after K. It keeps the controlled probe
structure and adds another world-contact movement to test whether the
multi-center field around dio_10qz/dio_1ytc stabilizes, falls back to one
center, or forms another group zone.

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
    """Return a deterministic fourth-contact continuation of variant K."""

    if not rows:
        return []
    timestamp_shift = 3_100_000_000_000 + (probe * 29_000_000)
    probe_phase = ((probe % 11) - 5) / 5.0
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

        local_phase = ((index % 29) - 14) / 14.0
        slow_wave = ((index // 8) % 9 - 4) / 4.0
        pulse = ((index % 12) - 5.5) / 5.5

        center_shift = (slow_wave * 0.0039) + (pulse * 0.0028) - (probe_phase * 0.0017)
        body_scale = max(0.55, 1.0 + (local_phase * 0.022) - (slow_wave * 0.016))
        upper_scale = max(0.55, 1.0 + (pulse * 0.020) + (abs(local_phase) * 0.012))
        lower_scale = max(0.55, 1.0 - (pulse * 0.021) + (abs(slow_wave) * 0.014))
        volume_scale = max(0.78, min(1.22, 1.0 + (abs(local_phase) * 0.018) + (abs(slow_wave) * 0.021)))

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


def create_variant_l(data_dir: Path) -> list[Path]:
    written: list[Path] = []
    for probe, label in PROBES.items():
        source = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteK_folgekontakt2_5m_SOLUSDT.csv"
        target = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteL_folgekontakt3_5m_SOLUSDT.csv"
        rows = _read_rows(source)
        if not rows:
            continue
        _write_rows(target, mutate_rows(rows, probe), list(rows[0].keys()))
        written.append(target)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Create controlled Mini-DIO variant L CSVs.")
    parser.add_argument("--data-dir", default="data")
    args = parser.parse_args()
    for path in create_variant_l(Path(args.data_dir)):
        print(path)


if __name__ == "__main__":
    main()
