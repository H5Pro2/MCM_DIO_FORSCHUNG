"""Create controlled Mini-DIO probe variant H.

Variant H is intentionally more structurally different than G. It mutates only
OHLCV input data and leaves Mini-DIO logic, memory, gates, entries, direction,
and runtime behavior untouched.
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
    """Return a deterministic structural-contrast variant after G."""

    if not rows:
        return []
    timestamp_shift = 1_800_000_000_000 + (probe * 14_000_000)
    probe_bias = ((probe % 4) - 1.5) * 0.003
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

        phase = ((index % 13) - 6) / 6.0
        mirror = -1.0 if ((index // 6) % 2) else 1.0
        compression = ((index // 9) % 3 - 1) / 1.0
        local_shear = ((index % 4) - 1.5) / 1.5

        center_shift = (phase * 0.015 * mirror) + (compression * 0.010) + probe_bias
        body_scale = max(0.35, 0.92 + (local_shear * 0.12) - (compression * 0.06))
        if (index // 8) % 2:
            body_scale *= -0.55
        wick_asym = phase * mirror
        upper_scale = max(0.35, 1.0 + (wick_asym * 0.22) + (abs(compression) * 0.06))
        lower_scale = max(0.35, 1.0 - (wick_asym * 0.18) + (abs(local_shear) * 0.08))

        # Keep the energy channel present, but do not simply amplify it.
        volume_wave = 1.0 + (0.035 * compression) + (0.025 * abs(local_shear)) - (0.018 * abs(phase))
        volume_scale = max(0.72, min(1.28, volume_wave))

        new_center = center + center_shift
        new_body = body * body_scale
        new_open = new_center - (new_body / 2.0)
        new_close = new_center + (new_body / 2.0)
        new_high = max(new_open, new_close) + max(0.02, upper_wick * upper_scale + abs(center_shift) * 0.20)
        new_low = min(new_open, new_close) - max(0.02, lower_wick * lower_scale + abs(local_shear) * 0.012)
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


def create_variant_h(data_dir: Path) -> list[Path]:
    written: list[Path] = []
    for probe, label in PROBES.items():
        source = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteG_verwandt_5m_SOLUSDT.csv"
        target = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteH_strukturkontrast_5m_SOLUSDT.csv"
        rows = _read_rows(source)
        if not rows:
            continue
        _write_rows(target, mutate_rows(rows, probe), list(rows[0].keys()))
        written.append(target)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Create controlled Mini-DIO variant H CSVs.")
    parser.add_argument("--data-dir", default="data")
    args = parser.parse_args()
    for path in create_variant_h(Path(args.data_dir)):
        print(path)


if __name__ == "__main__":
    main()
