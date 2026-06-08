"""Visualization snapshot helpers.

The helpers in this module prepare and write GUI/runtime snapshot payloads.
Brain-specific builders are injected by the caller to avoid coupling debug
output back into the MCM mechanics.
"""

from __future__ import annotations

import json
import os
import time

from config import Config
from debug_tools.writers import dbr_file_write_profile, dbr_resolve_path


def snapshot_write_path(snapshot_kind):
    snapshot_key = str(snapshot_kind or "visual").strip().lower()

    if snapshot_key == "inner":
        configured = str(getattr(Config, "MCM_INNER_SNAPSHOT_PATH", "debug/bot_inner_snapshot.json") or "debug/bot_inner_snapshot.json")
    else:
        configured = str(getattr(Config, "MCM_VISUAL_SNAPSHOT_PATH", "debug/bot_visual_snapshot.json") or "debug/bot_visual_snapshot.json")

    return dbr_resolve_path(configured)


def write_runtime_snapshot_payload(
    snapshot_kind,
    payload,
    *,
    profile_start=None,
    profile_debug=None,
):
    path = snapshot_write_path(snapshot_kind)
    section_start = profile_start() if profile_start is not None else None

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        write_start = time.perf_counter()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dict(payload or {}), f, indent=2)
        elapsed_ms = (time.perf_counter() - write_start) * 1000.0
        try:
            bytes_written = int(os.path.getsize(path))
        except Exception:
            bytes_written = 0
        dbr_file_write_profile(
            path,
            elapsed_ms,
            bytes_written=bytes_written,
            operation="runtime_snapshot_json_dump",
            extra=f"kind={snapshot_kind}|keys={int(len(dict(payload or {})))}",
        )
    except Exception:
        return None

    if profile_debug is not None:
        profile_debug(
            "write_runtime_snapshot_payload.total",
            section_start,
            extra=f"kind={snapshot_kind}|keys={int(len(dict(payload or {})))}|path={path}",
        )
    return path


def write_visualization_snapshot_bundle(
    snapshot_bundle,
    *,
    profile_start=None,
    profile_debug=None,
):
    section_start = profile_start() if profile_start is not None else None
    bundle = dict(snapshot_bundle or {})
    if not bundle:
        return None

    visual_payload = dict(bundle.get("visual", {}) or {})
    inner_payload = dict(bundle.get("inner", {}) or {})

    write_runtime_snapshot_payload(
        "visual",
        visual_payload,
        profile_start=profile_start,
        profile_debug=profile_debug,
    )
    write_runtime_snapshot_payload(
        "inner",
        inner_payload,
        profile_start=profile_start,
        profile_debug=profile_debug,
    )

    if profile_debug is not None:
        profile_debug(
            "write_visualization_snapshot_bundle.total",
            section_start,
            extra=f"visual_keys={int(len(visual_payload or {}))}|inner_keys={int(len(inner_payload or {}))}",
        )
    return dict(bundle or {})


def build_visual_chart_snapshot(window):
    local_window = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
    if not local_window:
        return {
            "visible_window_size": 0,
            "price_bounds": {
                "low": 0.0,
                "high": 0.0,
                "span": 0.0,
            },
            "candles": [],
            "close_trace": [],
        }

    visible_window_size = min(120, len(local_window))
    visible_window = local_window[-visible_window_size:]

    lows = []
    highs = []
    candles = []
    close_trace = []

    for index, candle in enumerate(visible_window):
        open_price = float(candle.get("open", 0.0) or 0.0)
        high_price = float(candle.get("high", open_price) or open_price)
        low_price = float(candle.get("low", open_price) or open_price)
        close_price = float(candle.get("close", open_price) or open_price)
        volume_value = float(candle.get("volume", 0.0) or 0.0)
        timestamp = candle.get("timestamp")

        lows.append(low_price)
        highs.append(high_price)
        close_trace.append(close_price)
        candles.append({
            "index": int(index),
            "timestamp": timestamp,
            "open": float(open_price),
            "high": float(high_price),
            "low": float(low_price),
            "close": float(close_price),
            "volume": float(volume_value),
            "direction": "up" if close_price >= open_price else "down",
            "body": float(close_price - open_price),
            "range": float(high_price - low_price),
        })

    price_low = min(lows) if lows else 0.0
    price_high = max(highs) if highs else 0.0
    price_span = max(price_high - price_low, 1e-9)

    normalized_close_trace = []
    for close_price in close_trace:
        normalized_close_trace.append(float((close_price - price_low) / price_span))

    return {
        "visible_window_size": int(visible_window_size),
        "price_bounds": {
            "low": float(price_low),
            "high": float(price_high),
            "span": float(price_high - price_low),
        },
        "candles": list(candles or []),
        "close_trace": list(close_trace or []),
        "normalized_close_trace": list(normalized_close_trace or []),
    }


def build_visualization_snapshot_bundle(
    bot=None,
    window=None,
    candle_state=None,
    *,
    pipeline_snapshot_builder=None,
):
    local_window = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
    timestamp = local_window[-1].get("timestamp") if local_window else None
    chart_snapshot = build_visual_chart_snapshot(local_window)
    inner_pipeline_snapshot = pipeline_snapshot_builder(bot) if pipeline_snapshot_builder is not None else {}

    visual_payload = {
        "timestamp": timestamp,
        "window": list(local_window or []),
        "candle_state": dict(candle_state or {}),
        "tension_state": dict(getattr(bot, "tension_state", {}) or {}) if bot is not None else {},
        "visual_market_state": dict(getattr(bot, "visual_market_state", {}) or {}) if bot is not None else {},
        "structure_perception_state": dict(getattr(bot, "structure_perception_state", {}) or {}) if bot is not None else {},
        "chart_snapshot": dict(chart_snapshot or {}),
    }

    inner_payload = {
        "timestamp": timestamp,
        **dict(inner_pipeline_snapshot or {}),
    }

    return {
        "visual": dict(visual_payload or {}),
        "inner": dict(inner_payload or {}),
    }


def prepare_visualization_snapshot_state(
    bot=None,
    window=None,
    candle_state=None,
    *,
    pipeline_snapshot_builder=None,
):
    snapshot_bundle = build_visualization_snapshot_bundle(
        bot=bot,
        window=window,
        candle_state=candle_state,
        pipeline_snapshot_builder=pipeline_snapshot_builder,
    )
    if snapshot_bundle is None:
        return {
            "snapshot_bundle": {},
            "snapshot_dirty": False,
        }

    return {
        "snapshot_bundle": dict(snapshot_bundle or {}),
        "snapshot_dirty": True,
    }


def capture_runtime_regulation_transition(bot=None, state_before=None, state_after=None):
    if bot is None:
        current_state = dict(state_after or {})
        previous_state = dict(state_before or {})

        if not previous_state:
            previous_state = dict(current_state or {})

        return previous_state, current_state, {}

    current_state = dict(state_after or {}) if state_after is not None else bot._build_regulation_state_snapshot()
    previous_state = dict(state_before or {}) if state_before is not None else dict(getattr(bot, "_last_regulation_state_snapshot", {}) or {})

    if not previous_state:
        previous_state = dict(current_state or {})

    state_delta = bot._build_regulation_state_delta(
        previous_state,
        current_state,
    )

    return previous_state, current_state, state_delta


def commit_runtime_regulation_snapshot(bot=None, state_after=None):
    if bot is None:
        return dict(state_after or {})

    committed_state = dict(state_after or {}) if state_after is not None else bot._build_regulation_state_snapshot()
    bot._last_regulation_state_snapshot = dict(committed_state or {})
    return dict(committed_state or {})
