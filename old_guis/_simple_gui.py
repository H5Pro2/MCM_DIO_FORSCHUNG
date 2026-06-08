from __future__ import annotations

import argparse
import csv
import json
import tkinter as tk
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

PATH = "debug_lauf_32"

# ==================================================
# CONFIG
# ==================================================
REFRESH_MS = 250
MAX_CANDLES = 80

C = {
    "bg_root": "#000000",
    "bg_panel": "#13161c",
    "bg_card": "#181c24",
    "bg_chart": "#0f1319",
    "border": "#252a36",
    "border_hi": "#2e3548",
    "text_hi": "#e8eaf0",
    "text_med": "#8b92a8",
    "text_lo": "#4a5168",
    "text_label": "#4e5f87",
    "green": "#4caf78",
    "red": "#c05050",
    "blue": "#5b8dd9",
    "orange": "#d4894a",
}

matplotlib.rcParams.update(
    {
        "figure.facecolor": C["bg_card"],
        "axes.facecolor": C["bg_chart"],
        "axes.edgecolor": C["border"],
        "axes.labelcolor": C["text_med"],
        "axes.titlecolor": C["text_label"],
        "xtick.color": C["text_lo"],
        "ytick.color": C["text_lo"],
        "grid.color": "#1a1f2b",
        "grid.linewidth": 0.5,
        "text.color": C["text_med"],
        "font.family": "monospace",
        "font.size": 8,
    }
)


# ==================================================
# HELPERS
# ==================================================
def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


# --------------------------------------------------
def safe_int(value, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return int(default)


# --------------------------------------------------
def safe_load_json(path: Path) -> dict:
    try:
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


# --------------------------------------------------
def fmt_num(value, digits: int = 2) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "–"


# --------------------------------------------------
def fmt_pct(value, digits: int = 2) -> str:
    try:
        return f"{float(value) * 100.0:.{digits}f}%"
    except Exception:
        return "–"


# --------------------------------------------------
def fmt_ts(value) -> str:
    try:
        if value is None:
            return "–"

        ts = int(float(value))
        if ts > 10_000_000_000_000:
            ts = ts // 1000

        if ts > 10_000_000_000:
            dt = datetime.fromtimestamp(ts / 1000)
        else:
            dt = datetime.fromtimestamp(ts)

        return dt.strftime("%d.%m.%Y %H:%M:%S")
    except Exception:
        return "–"


# --------------------------------------------------
def read_equity_curve(path: Path) -> list[float]:
    values: list[float] = []

    try:
        if not path.exists():
            return values

        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                values.append(safe_float(row.get("current_equity"), 0.0))
    except Exception:
        return []

    return values


# ==================================================
# UI BLOCKS
# ==================================================
class CardFrame(tk.Frame):

    # --------------------------------------------------
    def __init__(self, parent, title: str = "", width: int | None = None, height: int | None = None):
        super().__init__(
            parent,
            bg=C["bg_card"],
            highlightbackground=C["border"],
            highlightthickness=1,
            width=width,
            height=height,
        )
        self.body = tk.Frame(self, bg=C["bg_card"])

        if width is not None or height is not None:
            self.pack_propagate(False)
            self.grid_propagate(False)

        if title:
            tk.Label(
                self,
                text=str(title).upper(),
                bg=C["bg_card"],
                fg=C["text_label"],
                font=("Courier New", 8, "bold"),
                anchor="w",
                padx=8,
                pady=5,
            ).pack(fill="x")
            tk.Frame(self, bg=C["border"], height=1).pack(fill="x")

        self.body.pack(fill="both", expand=True)


# ==================================================
# SIMPLE GUI
# ==================================================
class SimpleGUI:

    # --------------------------------------------------
    def __init__(self, root: tk.Tk, base_dir: Path):
        self.root = root
        self.base_dir = Path(base_dir)
        self.visual_path = self.base_dir / "debug" / PATH / "bot_visual_snapshot.json"
        self.stats_path = self.base_dir / "debug" / PATH / "trade_stats.json"
        self.equity_path = self.base_dir / "debug" / PATH / "trade_equity.csv"
        self._after_id = None

        self.root.title("MCM Simple GUI")
        self.root.configure(bg=C["bg_root"])
        self.root.geometry("1600x900")
        self.root.minsize(1200, 720)

        self._build_layout()
        self._refresh()

    # --------------------------------------------------
    def _build_layout(self):
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=1)

        self.card_market = CardFrame(self.root, "MARKTÜBERBLICK", width=790, height=410)
        self.card_market.grid(row=0, column=0, sticky="nw", padx=(10, 0), pady=(10, 0))

        self.card_stats = CardFrame(self.root, "TRADE STATS & KPI", width=670, height=395)
        self.card_stats.grid(row=0, column=1, sticky="nw", padx=(10, 0), pady=(10, 0))

        self.card_candle = CardFrame(self.root, "CANDLE STATE", width=790, height=220)
        self.card_candle.grid(row=1, column=0, sticky="nw", padx=(10, 0), pady=(8, 0))

        self.card_backtest = CardFrame(self.root, "BACKTEST %", width=380, height=165)
        self.card_backtest.grid(row=1, column=1, sticky="nw", padx=(10, 0), pady=(44, 0))

        self.card_equity = CardFrame(self.root, "EQUITY-KURVE", width=1130, height=295)
        self.card_equity.grid(row=2, column=0, columnspan=2, sticky="nw", padx=(10, 0), pady=(10, 0))

        self.fig_market = Figure(figsize=(7.8, 3.45), dpi=100)
        self.fig_market.subplots_adjust(left=0.09, right=0.985, top=0.965, bottom=0.115)
        self.ax_market = self.fig_market.add_subplot(111)
        self.canvas_market = FigureCanvasTkAgg(self.fig_market, master=self.card_market.body)
        self.canvas_market.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)

        self.fig_equity = Figure(figsize=(11.15, 2.35), dpi=100)
        self.fig_equity.subplots_adjust(left=0.05, right=0.99, top=0.95, bottom=0.16)
        self.ax_equity = self.fig_equity.add_subplot(111)
        self.canvas_equity = FigureCanvasTkAgg(self.fig_equity, master=self.card_equity.body)
        self.canvas_equity.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)

        self.candle_labels = {}
        self._build_value_rows(
            self.card_candle.body,
            [
                ("Open", "open"),
                ("High", "high"),
                ("Low", "low"),
                ("Close", "close"),
                ("Volume", "volume"),
            ],
            self.candle_labels,
        )

        self.stats_labels = {}
        self._build_value_rows(
            self.card_stats.body,
            [
                ("PnL Netto", "pnl_netto"),
                ("Wins / Loss", "wins_loss"),
                ("Trades", "trades"),
                ("Cancels", "cancels"),
                ("Attempts", "attempts"),
                ("Observed", "attempts_observed"),
                ("Replanned", "attempts_replanned"),
                ("Withheld", "attempts_withheld"),
                ("Max DD", "max_drawdown_pct"),
                ("Eq. Peak", "equity_peak"),
            ],
            self.stats_labels,
        )

        self.backtest_label = tk.Label(
            self.card_backtest.body,
            text="–",
            bg=C["bg_card"],
            fg=C["orange"],
            font=("Courier New", 22, "bold"),
            anchor="center",
        )
        self.backtest_label.pack(fill="both", expand=True)

    # --------------------------------------------------
    def _build_value_rows(self, parent: tk.Frame, rows: list[tuple[str, str]], target: dict):
        for row_index, (label_text, key) in enumerate(rows):
            parent.grid_columnconfigure(0, weight=1)
            parent.grid_columnconfigure(1, weight=0)

            tk.Label(
                parent,
                text=label_text,
                bg=C["bg_card"],
                fg=C["text_label"],
                font=("Courier New", 10, "bold"),
                anchor="w",
            ).grid(row=row_index, column=0, sticky="ew", padx=(16, 8), pady=4)

            value_label = tk.Label(
                parent,
                text="–",
                bg=C["bg_card"],
                fg=C["text_hi"],
                font=("Courier New", 10, "bold"),
                anchor="e",
                width=18,
            )
            value_label.grid(row=row_index, column=1, sticky="e", padx=(8, 16), pady=4)
            target[key] = value_label

    # --------------------------------------------------
    def _refresh(self):
        visual = safe_load_json(self.visual_path)
        stats = safe_load_json(self.stats_path)
        equity = read_equity_curve(self.equity_path)

        self._draw_market_chart(visual)
        self._draw_equity_chart(equity, stats)
        self._update_candle_state(visual)
        self._update_trade_stats(stats)
        self._update_backtest_progress(visual, stats)

        self._after_id = self.root.after(REFRESH_MS, self._refresh)

    # --------------------------------------------------
    def _resolve_window(self, visual: dict) -> list[dict]:
        chart_snapshot = dict(visual.get("chart_snapshot", {}) or {})
        candles = chart_snapshot.get("candles", [])

        if isinstance(candles, list) and candles:
            return [dict(item or {}) for item in candles if isinstance(item, dict)][-MAX_CANDLES:]

        window = visual.get("window", [])
        if isinstance(window, list):
            return [dict(item or {}) for item in window if isinstance(item, dict)][-MAX_CANDLES:]

        return []

    # --------------------------------------------------
    def _draw_market_chart(self, visual: dict):
        self.ax_market.clear()
        self.ax_market.set_facecolor(C["bg_chart"])
        self.ax_market.grid(True, alpha=0.55)

        candles = self._resolve_window(visual)

        if not candles:
            self.ax_market.text(
                0.5,
                0.5,
                "NO MARKET DATA",
                ha="center",
                va="center",
                color=C["text_lo"],
                transform=self.ax_market.transAxes,
            )
            self.canvas_market.draw_idle()
            return

        lows = []
        highs = []

        for index, candle in enumerate(candles):
            open_price = safe_float(candle.get("open"), 0.0)
            high_price = safe_float(candle.get("high"), open_price)
            low_price = safe_float(candle.get("low"), open_price)
            close_price = safe_float(candle.get("close"), open_price)

            lows.append(low_price)
            highs.append(high_price)

            color = C["green"] if close_price >= open_price else C["red"]
            self.ax_market.vlines(index, low_price, high_price, color="#31394d", linewidth=1.2)

            body_low = min(open_price, close_price)
            body_height = max(abs(close_price - open_price), 1e-9)
            self.ax_market.add_patch(
                matplotlib.patches.Rectangle(
                    (index - 0.31, body_low),
                    0.62,
                    body_height,
                    facecolor=color,
                    edgecolor=color,
                    linewidth=0.8,
                    alpha=0.72,
                )
            )

        price_low = min(lows)
        price_high = max(highs)
        price_span = max(price_high - price_low, 1e-9)
        self.ax_market.set_xlim(-1, len(candles))
        self.ax_market.set_ylim(price_low - price_span * 0.06, price_high + price_span * 0.06)
        self.ax_market.tick_params(labelsize=8)
        self.canvas_market.draw_idle()

    # --------------------------------------------------
    def _draw_equity_chart(self, equity: list[float], stats: dict):
        self.ax_equity.clear()
        self.ax_equity.set_facecolor(C["bg_chart"])
        self.ax_equity.grid(True, alpha=0.55)

        values = [float(item) for item in list(equity or []) if float(item) != 0.0]

        if not values:
            start_equity = safe_float(stats.get("start_equity"), 100.0)
            current_equity = safe_float(stats.get("current_equity"), start_equity)
            values = [start_equity, current_equity]

        x_values = list(range(len(values)))
        self.ax_equity.plot(x_values, values, linewidth=2.0, color=C["blue"])
        self.ax_equity.fill_between(x_values, values, min(values), alpha=0.14, color=C["blue"])
        self.ax_equity.tick_params(labelsize=8)
        self.canvas_equity.draw_idle()

    # --------------------------------------------------
    def _update_candle_state(self, visual: dict):
        candle_state = dict(visual.get("candle_state", {}) or {})
        candles = self._resolve_window(visual)
        last_candle = dict(candles[-1] if candles else {})

        source = dict(last_candle or candle_state or {})

        values = {
            "open": fmt_num(source.get("open"), 2),
            "high": fmt_num(source.get("high"), 2),
            "low": fmt_num(source.get("low"), 2),
            "close": fmt_num(source.get("close"), 2),
            "volume": fmt_num(source.get("volume"), 2) if source.get("volume") is not None else "–",
        }

        for key, value in values.items():
            label = self.candle_labels.get(key)
            if label is not None:
                label.configure(text=value)

        if self.candle_labels.get("high") is not None:
            self.candle_labels["high"].configure(fg=C["green"])
        if self.candle_labels.get("low") is not None:
            self.candle_labels["low"].configure(fg=C["red"])

    # --------------------------------------------------
    def _update_trade_stats(self, stats: dict):
        tp = safe_int(stats.get("tp"), 0)
        sl = safe_int(stats.get("sl"), 0)
        pnl = safe_float(stats.get("pnl_netto"), 0.0)

        values = {
            "pnl_netto": fmt_num(pnl, 2),
            "wins_loss": f"{tp} / {sl}",
            "trades": str(safe_int(stats.get("trades"), 0)),
            "cancels": str(safe_int(stats.get("cancels"), 0)),
            "attempts": str(safe_int(stats.get("attempts"), 0)),
            "attempts_observed": str(safe_int(stats.get("attempts_observed"), 0)),
            "attempts_replanned": str(safe_int(stats.get("attempts_replanned"), 0)),
            "attempts_withheld": str(safe_int(stats.get("attempts_withheld"), 0)),
            "max_drawdown_pct": fmt_pct(stats.get("max_drawdown_pct"), 2),
            "equity_peak": fmt_num(stats.get("equity_peak"), 12),
        }

        for key, value in values.items():
            label = self.stats_labels.get(key)
            if label is not None:
                label.configure(text=value)

        if self.stats_labels.get("pnl_netto") is not None:
            self.stats_labels["pnl_netto"].configure(fg=C["green"] if pnl >= 0 else C["red"])

    # --------------------------------------------------
    def _update_backtest_progress(self, visual: dict, stats: dict):
        current_ts = stats.get("current_timestamp", visual.get("timestamp"))
        progress = stats.get("backtest_progress")

        if progress is None:
            progress = stats.get("progress")

        if progress is not None:
            progress_text = fmt_pct(progress, 0)
        elif current_ts is not None:
            progress_text = fmt_ts(current_ts)
        else:
            progress_text = "–"

        self.backtest_label.configure(text=str(progress_text))

    # --------------------------------------------------
    def close(self):
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        self.root.destroy()


# ==================================================
# MAIN
# ==================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default=".")
    args = parser.parse_args()

    root = tk.Tk()
    app = SimpleGUI(root, Path(args.base_dir))
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


# --------------------------------------------------
if __name__ == "__main__":
    main()
