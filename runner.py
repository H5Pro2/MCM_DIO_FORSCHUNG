# ==================================================
# runner.py
# ==================================================
import argparse
import csv
import time
from workspace import append_workspace_live, init_workspace_live
from datetime import datetime
from config import Config
from bot import Bot
from trading.exchange_data import (
    create_exchange,
    get_sufficient_balance,
    get_account_value,
    fetch_ohlcv,
    resolve_exchange_symbol,
)

from trading.order_logic import _SYMBOL, set_context, place_order, ensure_order_monitor_started
from memory.memory_state import save_memory_state
from debug_tools.audio_debug import flush_market_melody_wav


def _count_backtest_rows(filepath):
    try:
        with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return sum(1 for _ in reader)
    except Exception:
        return 0


def _update_backtest_progress_stats(bot, filepath, processed_windows, total_windows, complete=False, stop_reason="running"):
    total = max(0, int(total_windows or 0))
    processed = max(0, int(processed_windows or 0))
    progress = 0.0 if total <= 0 else max(0.0, min(1.0, processed / float(total)))
    bot.stats.data["backtest_filepath"] = str(filepath or "")
    bot.stats.data["backtest_processed_windows"] = processed
    bot.stats.data["backtest_total_windows"] = total
    bot.stats.data["backtest_progress"] = float(progress)
    bot.stats.data["backtest_complete"] = bool(complete)
    bot.stats.data["backtest_stop_reason"] = str(stop_reason or "running")


# --------------------------------------------------
# BACKTEST RANGE PRINT
# --------------------------------------------------
def _print_backtest_range_legacy(path):
    first_ts = None
    last_ts = None

    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                ts = row.get("timestamp_ms")
                if ts is None:
                    continue

                ts = int(float(ts))

                if first_ts is None:
                    first_ts = ts

                last_ts = ts

        if first_ts and last_ts:

            # Mikrosekunden → Millisekunden
            if first_ts > 10_000_000_000_000:
                first_ts = first_ts / 1000

            if last_ts > 10_000_000_000_000:
                last_ts = last_ts / 1000

            first_dt = datetime.fromtimestamp(first_ts / 1000).strftime("%d.%m.%Y")
            last_dt = datetime.fromtimestamp(last_ts / 1000).strftime("%d.%m.%Y")
            print(f"BACKTEST RANGE: {first_dt} → {last_dt}")

    except Exception:
        print("BACKTEST RANGE: -")

# --------------------------------------------------
# BACKTEST MODE
# --------------------------------------------------
def _print_backtest_range(path):
    first_ts = None
    last_ts = None

    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = row.get("timestamp_ms")
                if ts is None:
                    continue
                ts = int(float(ts))
                if first_ts is None:
                    first_ts = ts
                last_ts = ts

        if first_ts and last_ts:
            if first_ts > 10_000_000_000_000:
                first_ts = first_ts / 1000
            if last_ts > 10_000_000_000_000:
                last_ts = last_ts / 1000

            first_dt = datetime.fromtimestamp(first_ts / 1000).strftime("%d.%m.%Y")
            last_dt = datetime.fromtimestamp(last_ts / 1000).strftime("%d.%m.%Y")
            print(f"BACKTEST RANGE: {first_dt} -> {last_dt}")
            return

    except Exception as exc:
        print(f"BACKTEST RANGE: - ({type(exc).__name__})")
        return

    print("BACKTEST RANGE: -")


def _run_backtest_mode(filepath=None, max_windows=None, save_memory=True):

    filepath = filepath or Config.BACKTEST_FILEPATH

    bot = Bot(filepath)
    total_rows = _count_backtest_rows(filepath)
    total_windows = max(0, int(total_rows) - int(Config.WINDOW_SIZE) + 1)
    if max_windows is not None:
        total_windows = min(total_windows, max(1, int(max_windows or 1)))
    _update_backtest_progress_stats(bot, filepath, 0, total_windows, complete=False, stop_reason="running")
    synchronous_runtime = bool(
        getattr(Config, "BACKTEST_SYNCHRONOUS_RUNTIME", True)
        and getattr(Config, "BACKTEST_WAIT_FOR_RUNTIME_IDLE", True)
    )
    if not synchronous_runtime:
        bot.start_runtime_thread()

    buffer = []
    bot.processed = 0
    world_time_seconds = max(
        0.0,
        float(getattr(Config, "WORLD_TIME_SECONDS", 0.0) or 0.0),
    )

    processed_windows = 0
    stop_reason = "feed_exhausted"
    try:
        # Die CSV liefert die fachliche Marktzeit. Fuer saubere Lern- und
        # Vergleichslaeufe muss DIO jede Kerze verarbeiten. Der asynchrone
        # Stress-Test bleibt ueber BACKTEST_WAIT_FOR_RUNTIME_IDLE=False moeglich.
        for row in bot.feed.rows(delay_seconds=0.0):
            buffer.append(row)

            if len(buffer) < Config.WINDOW_SIZE:
                continue

            if len(buffer) > Config.WINDOW_SIZE:
                buffer.pop(0)

            if synchronous_runtime:
                bot._process_market_window_and_followup(buffer)
            else:
                bot.publish_market_window(buffer)
            processed_windows += 1

            if (not synchronous_runtime) and bool(getattr(Config, "BACKTEST_WAIT_FOR_RUNTIME_IDLE", True)):
                bot.wait_until_runtime_idle()

            if max_windows is not None and processed_windows >= int(max_windows):
                stop_reason = "max_windows"
                break

            _update_backtest_progress_stats(bot, filepath, processed_windows, total_windows, complete=False, stop_reason="running")
            if processed_windows == 1 or (processed_windows % 50) == 0:
                try:
                    bot.stats._save(force=True)
                except Exception:
                    pass

            if bool(getattr(Config, "BACKTEST_REPLAY_SLEEP_ENABLED", False)) and world_time_seconds > 0.0:
                time.sleep(world_time_seconds)
    except Exception as exc:
        stop_reason = f"error:{type(exc).__name__}"
        raise
    finally:
        complete = bool(total_windows > 0 and processed_windows >= total_windows)
        if complete and stop_reason == "feed_exhausted":
            stop_reason = "complete"
        _update_backtest_progress_stats(bot, filepath, processed_windows, total_windows, complete=complete, stop_reason=stop_reason)
        try:
            bot.stats._save(force=True)
        except Exception:
            pass
        if synchronous_runtime:
            bot._flush_runtime_followup()
            flush_market_melody_wav(force=True)
            if save_memory:
                bot._save_memory_state(force=True)
        else:
            bot.wait_until_runtime_idle()
            flush_market_melody_wav(force=True)
            bot.stop_runtime_thread(save_memory=save_memory)

    if save_memory and not synchronous_runtime:
        save_memory_state(bot)
    return filepath, bot, bot.stats.snapshot()


def _run_smoke_mode(filepath=None, max_windows=3):
    filepath, bot, stats = _run_backtest_mode(
        filepath=filepath,
        max_windows=max(1, int(max_windows or 1)),
        save_memory=False,
    )
    print(
        f"SMOKE OK | "
        f"FILE: {filepath} | "
        f"WINDOWS: {max(1, int(max_windows or 1))} | "
        f"TRADES: {stats.get('trades', 0)} | "
        f"PNL_NETTO: {float(stats.get('pnl_netto', 0.0) or 0.0):.4f}"
    )
    return filepath, bot, stats

# --------------------------------------------------
# TIMEFRAME RESOLUTION
# --------------------------------------------------
def _resolve_timeframe_seconds(timeframe: str) -> int:

    tf = timeframe.lower().strip()

    if tf.endswith("m"):
        return int(tf[:-1]) * 60
    elif tf.endswith("h"):
        return int(tf[:-1]) * 3600

    return 60

# --------------------------------------------------
# LIVE MODE (SEQUENZIELL · BACKEND-IDENTISCH)
# --------------------------------------------------
def _run_live_mode():

    timeframe = Config.TIMEFRAME
    symbol = Config.SYMBOL
    exchange_symbol = resolve_exchange_symbol(symbol)

    world_time_seconds = max(1.0, float(_resolve_timeframe_seconds(timeframe) or 1.0))

    exchange = create_exchange()

    set_context(
        exchange=exchange,
        symbol=exchange_symbol,
        timeframe=timeframe,
        get_sufficient_balance=get_sufficient_balance,
        get_account_value=get_account_value,
    )
    ensure_order_monitor_started()

    bot = Bot(None)
    bot.start_runtime_thread()

    last_processed_ts = None
    buffer = []

    while True:

        raw = fetch_ohlcv(exchange, exchange_symbol, timeframe)

        if raw is None or not isinstance(raw, list):
            continue

        if len(raw) < Config.WINDOW_SIZE + 1:
            continue

        # --------------------------------------------------
        # Letzte Kerze nur entfernen wenn sie noch läuft
        # --------------------------------------------------
        tf_seconds = _resolve_timeframe_seconds(timeframe)

        now_ts = int(time.time())
        last_candle_ts = int(raw[-1][0]) // 1000

        # Wenn letzte Kerze noch nicht geschlossen ist → entfernen
        if now_ts < (last_candle_ts + tf_seconds):
            raw = raw[:-1]

        # --------------------------------------------------
        # INITIALISIERUNG (einmalig)
        # --------------------------------------------------
        if last_processed_ts is None:

            init_slice = raw[-Config.WINDOW_SIZE:]
            init_workspace_live(symbol, timeframe, init_slice)

            buffer = [
                {
                    "timestamp": int(ts),
                    "open": float(o),
                    "high": float(h),
                    "low": float(l),
                    "close": float(c),
                    "volume": float(v),
                }
                for ts, o, h, l, c, v in init_slice
            ]

            bot.publish_market_window(buffer)
            last_processed_ts = buffer[-1]["timestamp"]
            time.sleep(world_time_seconds)
            continue

        # --------------------------------------------------
        # NEUE KERZEN ERMITTELN
        # --------------------------------------------------
        new_candles = [
            c for c in raw
            if int(c[0]) > last_processed_ts
        ]

        if not new_candles:
            time.sleep(world_time_seconds)
            continue

        # --------------------------------------------------
        # SEQUENZIELLE VERARBEITUNG
        # --------------------------------------------------
        for ts, o, h, l, c, v in new_candles:

            # Workspace append
            append_workspace_live(symbol, timeframe, (ts, o, h, l, c, v))

            row = {
                "timestamp": int(ts),
                "open": float(o),
                "high": float(h),
                "low": float(l),
                "close": float(c),
                "volume": float(v),
            }

            buffer.append(row)

            if len(buffer) > Config.WINDOW_SIZE:
                buffer.pop(0)

            bot.publish_market_window(buffer)

            last_processed_ts = int(ts)

        time.sleep(world_time_seconds)

# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DIO Runner")
    parser.add_argument("--smoke", action="store_true", help="Kurzer Startcheck ohne Memory-Save.")
    parser.add_argument("--backtest-file", default=None, help="Optionaler CSV-Pfad fuer Backtest/Smoke.")
    parser.add_argument("--max-windows", type=int, default=None, help="Optionale Begrenzung der verarbeiteten Backtest-Fenster.")
    args = parser.parse_args()

    print("-------------------------------------------------------")
    print("WORKSPACE")
    print(f"  WINDOW_SIZE: {Config.WINDOW_SIZE}")

    print("-------------------------------------------------------")
    print("RISK MANAGEMENT")
    print(f"  MIN_RR: {Config.MIN_RR}")
    print(f"  BASE_RISK_PCT: {Config.BASE_RISK_PCT}")
    print(f"  MAX_SL_DISTANCE: {Config.MAX_SL_DISTANCE}")
    print(f"  MIN_TP_DISTANCE: {Config.MIN_TP_DISTANCE}")
    print(f"  RR_EXECUTION_MIN: {Config.RR_EXECUTION_MIN}")
    print(f"  PENDING_ENTRY_MAX_WAIT_BARS: {Config.PENDING_ENTRY_MAX_WAIT_BARS}")

    print("-------------------------------------------------------")
    print("MCM")
    print(f"  MCM_ENABLED: {Config.MCM_ENABLED}")
    print(f"  MCM_INTERNAL_CYCLES: {Config.MCM_INTERNAL_CYCLES}")
    print(f"  MCM_REPLAY_SCALE: {Config.MCM_REPLAY_SCALE}")
    print(f"  MCM_COUPLING: {Config.MCM_COUPLING}")
    print(f"  MCM_NOISE: {Config.MCM_NOISE}")
    print(f"  MCM_PRESSURE_WEIGHT: {Config.MCM_PRESSURE_WEIGHT}")
    print(f"  MCM_MEMORY_WEIGHT: {Config.MCM_MEMORY_WEIGHT}")
    print(f"  MCM_REGULATION_WEIGHT: {Config.MCM_REGULATION_WEIGHT}")

    print("-------------------------------------------------------")
    print("COSTS")
    print(f"  FEE_RATE: {Config.FEE_RATE}")
    print(f"  FEE_PER_TRADE: {Config.FEE_PER_TRADE}")

    print("-------------------------------------------------------")
    print("SYSTEM")
    print(f"  AKTIV_ORDER: {Config.AKTIV_ORDER}")
    # --------------------------------------------------
    # BACKTEST MODE
    # --------------------------------------------------
    if args.smoke:
        filepath, bot, stats = _run_smoke_mode(
            filepath=args.backtest_file,
            max_windows=args.max_windows or 3,
        )
        _print_backtest_range(filepath)

    elif Config.MODE == "BACKTEST":

        filepath, bot, stats = _run_backtest_mode(
            filepath=args.backtest_file,
            max_windows=args.max_windows,
            save_memory=True,
        )

        _print_backtest_range(filepath)

        '''
        print(
            f"BACKTEST EXPLORATION | "
            f"TRADES: {stats.get('exploration_trades', 0)} | "
            f"TP: {stats.get('exploration_tp', 0)} | "
            f"SL: {stats.get('exploration_sl', 0)} | "
            f"CANCELS: {stats.get('exploration_cancels', 0)} | "
            f"PNL: {stats.get('exploration_pnl', 0.0):.4f}"
        )
        '''
        print(
            f"BACKTEST GESAMT | "
            f"TRADES: {stats.get('trades', 0)} | "
            f"TP: {stats.get('tp', 0)} | "
            f"SL: {stats.get('sl', 0)} | "
            f"CANCELS: {stats.get('cancels', 0)} | "
            f"PNL_NETTO: {stats.get('pnl_netto', 0.0):.4f}"
        )

        proof = dict((stats.get("kpi_summary", {}) or {}).get("proof", {}) or {})
        structure_bands = dict((stats.get("kpi_summary", {}) or {}).get("structure_bands", {}) or {})

        print(
            f"KPI NACHWEIS | "
            f"EXPECTANCY: {float(proof.get('expectancy', 0.0) or 0.0):.4f} | "
            f"PF: {float(proof.get('profit_factor', 0.0) or 0.0):.3f} | "
            f"ATTEMPT_DENSITY: {float(proof.get('attempt_density', 0.0) or 0.0):.3f} | "
            f"CONTEXT_QUALITY: {float(proof.get('context_quality', 0.0) or 0.0):.3f} | "
            f"OVERTRADE_PRESSURE: {float(proof.get('overtrade_pressure', 0.0) or 0.0):.3f} | "
            f"MAX_DD_PCT: {float(proof.get('max_drawdown_pct', 0.0) or 0.0) * 100.0:.2f}%"
        )

        print(
            f"MCM RAUM | "
            f"FIELD_DENSITY: {float(getattr(bot, 'field_density', 0.0) or 0.0):.3f} | "
            f"FIELD_STABILITY: {float(getattr(bot, 'field_stability', 0.0) or 0.0):.3f} | "
            f"REGULATORY_LOAD: {float(getattr(bot, 'regulatory_load', 0.0) or 0.0):.3f} | "
            f"ACTION_CAPACITY: {float(getattr(bot, 'action_capacity', 0.0) or 0.0):.3f} | "
            f"RECOVERY_NEED: {float(getattr(bot, 'recovery_need', 0.0) or 0.0):.3f} | "
            f"SURVIVAL_PRESSURE: {float(getattr(bot, 'survival_pressure', 0.0) or 0.0):.3f}"
        )

        print(
            f"STRUKTURBÄNDER | "
            f"HIGH: win={float(((structure_bands.get('high', {}) or {}).get('winrate', 0.0) or 0.0) * 100.0):.2f}% pnl={float((structure_bands.get('high', {}) or {}).get('avg_pnl', 0.0) or 0.0):.4f} | "
            f"MID: win={float(((structure_bands.get('mid', {}) or {}).get('winrate', 0.0) or 0.0) * 100.0):.2f}% pnl={float((structure_bands.get('mid', {}) or {}).get('avg_pnl', 0.0) or 0.0):.4f} | "
            f"LOW: win={float(((structure_bands.get('low', {}) or {}).get('winrate', 0.0) or 0.0) * 100.0):.2f}% pnl={float((structure_bands.get('low', {}) or {}).get('avg_pnl', 0.0) or 0.0):.4f}"
        )

    # --------------------------------------------------
    # LIVE MODE (SEQUENZIELL · BACKEND-IDENTISCH)
    # --------------------------------------------------
    elif Config.MODE == "LIVE":

        _run_live_mode()
