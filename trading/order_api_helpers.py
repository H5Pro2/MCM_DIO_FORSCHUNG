import api
import threading
import time
from config import Config
from trading import exchange_data as ph_ohlcv
import debug_tools.writers as dbr
# --------------------------------------------------
_ACTIVE_ORDER_ID = None
_ACTIVE_SIDE = None
_ACTIVE_TP = None
_POSITION_OPEN = False
_LAST_SYNC_TS = None
_CONNECTION_OK = False
_BOOTSTRAPPED = False
_BOOTSTRAP_LOCK = threading.Lock()
_EXCHANGE = None
_SYMBOL = None
_ENTRY_REFERENCE = None
_ENTRY_DISTANCE = None
_RISK_REFERENCE = None
_ENTRY_VALIDITY_CENTER = None
_ENTRY_VALIDITY_LOWER = None
_ENTRY_VALIDITY_UPPER = None
# --------------------------------------------------
# CANCEL TRACKING
# --------------------------------------------------
_CANCEL_COUNT = 0
_CANCELLED_ORDER_IDS = set()
_CANCELLED_ORDER_CAUSES = {}
# --------------------------------------------------
# DEBUGGING
# --------------------------------------------------
def gate_debug(msg):
    dbr.dbr_debug(msg, "order_debug.csv")
# --------------------------------------------------
# ACTIVE CHECK - wird in rl_structure_bot.py genutz
# --------------------------------------------------
def is_order_active():
    global _ACTIVE_ORDER_ID, _POSITION_OPEN
    return (_ACTIVE_ORDER_ID is not None) or (_POSITION_OPEN is True)
# --------------------------------------------------
# EXCHANGE INIT / SAFE FETCH
# --------------------------------------------------
def _ensure_exchange():
    global _EXCHANGE, _SYMBOL

    if _SYMBOL is None:
        _SYMBOL = ph_ohlcv.resolve_exchange_symbol(Config.SYMBOL)

    if _EXCHANGE is None:
        _EXCHANGE = ph_ohlcv.create_exchange(api.API_KEY, api.API_SECRET)

    return _EXCHANGE
# --------------------------------------------------
def _safe_fetch_open_orders(exchange):
    try:
        return exchange.fetch_open_orders(_SYMBOL)
    except Exception as e:
        gate_debug(f"❌ fetch_open_orders Fehler: {e}")
        return None
# --------------------------------------------------
def _safe_fetch_positions(exchange):
    # ccxt: nicht jede Börse unterstützt positions() gleich
    try:
        if hasattr(exchange, "fetch_positions"):
            return exchange.fetch_positions([_SYMBOL])
    except Exception as e:
        gate_debug(f"❌ fetch_positions Fehler: {e}")
        return None
    return None
# --------------------------------------------------
def _detect_open_position(positions):
    """
    Phemex Futures:
    Nur wenn contracts > 0 gilt Position als offen.
    Alles andere ignorieren.
    """
    if not positions:
        return False

    try:
        for p in positions:
            if not isinstance(p, dict):
                continue

            contracts = p.get("contracts")

            if contracts is None:
                continue

            try:
                if abs(float(contracts)) > 0.0:
                    return True
            except Exception:
                continue

    except Exception:
        return False

    return False
# --------------------------------------------------
def _sync_with_exchange(reason="startup"):
    global _ACTIVE_ORDER_ID, _ACTIVE_TP, _ACTIVE_SIDE, _POSITION_OPEN, _LAST_SYNC_TS, _CONNECTION_OK, _ENTRY_REFERENCE, _RISK_REFERENCE

    def _read_order_float(order_payload, info_payload, keys):
        for source in (dict(order_payload or {}), dict(info_payload or {})):
            for key in list(keys or []):
                value = source.get(key)
                if value is None:
                    continue

                try:
                    number = float(value)
                except Exception:
                    continue

                if number > 0.0:
                    return float(number)

        return None

    exchange = _ensure_exchange()

    #gate_debug("---------------------------------------")
    #gate_debug(f"🔄 SYNC START | reason={reason}")

    # 1) Positions prüfen (fail-safe)
    positions = _safe_fetch_positions(exchange)
    pos_open = _detect_open_position(positions)

    # POSITION_OPEN immer hart neu setzen (kein Sticky-Block mehr)
    if pos_open:
        _POSITION_OPEN = True
        gate_debug("⚠️ Sync: POSITION OFFEN erkannt → neue Orders gesperrt (failsafe)")
    else:
        if _POSITION_OPEN:
            gate_debug("🟢 Sync: vorher offene Position jetzt geschlossen → Freigabe")
        _POSITION_OPEN = False

    # 2) Open Orders prüfen
    open_orders = _safe_fetch_open_orders(exchange)
    if open_orders is None:
        _CONNECTION_OK = False
        gate_debug("❌ SYNC: open_orders nicht abrufbar → Verbindung OK? = False")
        gate_debug("---------------------------------------")
        return False

    _CONNECTION_OK = True

    # Wenn aktive Order-ID schon gesetzt ist, nur validieren
    if _ACTIVE_ORDER_ID is not None:
        exists = ph_ohlcv.check_order_id_exist(exchange, _SYMBOL, _ACTIVE_ORDER_ID)
        if exists:
            confirmed_order = None

            for order_item in list(open_orders or []):
                if str((order_item or {}).get("id")) == str(_ACTIVE_ORDER_ID):
                    confirmed_order = dict(order_item or {})
                    break

            if confirmed_order:
                info = dict(confirmed_order.get("info", {}) or {})
                side = str(confirmed_order.get("side") or "").lower() or None
                entry = _read_order_float(confirmed_order, info, ("price", "entryPrice", "avgPrice", "average"))
                tp = _read_order_float(confirmed_order, info, ("takeProfitPrice", "takeProfitRp", "takeProfit", "tp"))
                sl = _read_order_float(confirmed_order, info, ("stopLossPrice", "stopLossRp", "stopLoss", "sl"))

                if _ACTIVE_SIDE is None and side is not None:
                    _ACTIVE_SIDE = side

                if _ACTIVE_TP is None and tp is not None:
                    _ACTIVE_TP = float(tp)

                if _ENTRY_REFERENCE is None and entry is not None:
                    _ENTRY_REFERENCE = float(entry)

                try:
                    risk_missing = _RISK_REFERENCE is None or float(_RISK_REFERENCE) <= 0.0
                except Exception:
                    risk_missing = True

                if risk_missing and entry is not None and sl is not None:
                    _RISK_REFERENCE = abs(float(entry) - float(sl))

            gate_debug(f"🟡 SYNC: aktive Order bestätigt | id={_ACTIVE_ORDER_ID}")
            _LAST_SYNC_TS = time.time()
            gate_debug("---------------------------------------")
            return True
        else:
            gate_debug(f"🟢 SYNC: aktive Order existiert nicht mehr → Freigabe | id={_ACTIVE_ORDER_ID}")
            _ACTIVE_ORDER_ID = None
            _ACTIVE_TP = None
            _ACTIVE_SIDE = None

    # Keine aktive Order: ggf. offene Orders übernehmen (defensiv: nur wenn eindeutig)
    if open_orders:
        if len(open_orders) == 1:
            o = open_orders[0]
            info = dict((o or {}).get("info", {}) or {})
            oid = o.get("id")
            side = str(o.get("side") or "").lower() or None
            entry = _read_order_float(o, info, ("price", "entryPrice", "avgPrice", "average"))
            tp = _read_order_float(o, info, ("takeProfitPrice", "takeProfitRp", "takeProfit", "tp"))
            sl = _read_order_float(o, info, ("stopLossPrice", "stopLossRp", "stopLoss", "sl"))

            _ACTIVE_ORDER_ID = oid
            _ACTIVE_SIDE = side
            _ACTIVE_TP = float(tp) if tp is not None else None

            if entry is not None:
                _ENTRY_REFERENCE = float(entry)

            if entry is not None and sl is not None:
                _RISK_REFERENCE = abs(float(entry) - float(sl))

            gate_debug(f"🟡 SYNC: 1 offene Order übernommen | id={_ACTIVE_ORDER_ID} | side={_ACTIVE_SIDE}")
        else:
            gate_debug(f"⚠️ SYNC: {len(open_orders)} offene Orders gefunden → keine automatische Übernahme")
            # failsafe: wenn mehrere offene Orders existieren, blockieren wir neue Orders über _ACTIVE_ORDER_ID-Sentinel
            _ACTIVE_ORDER_ID = "MULTI_OPEN_ORDERS"
            _ACTIVE_SIDE = None
            _ACTIVE_TP = None
    #else:
        #gate_debug("🟢 SYNC: keine offenen Orders")

    _LAST_SYNC_TS = time.time()
    #gate_debug("---------------------------------------")
    return True
# --------------------------------------------------
def _bootstrap_once():
    global _BOOTSTRAPPED

    if _BOOTSTRAPPED:
        return

    with _BOOTSTRAP_LOCK:
        if _BOOTSTRAPPED:
            return
        try:
            _ensure_exchange()
            _sync_with_exchange(reason="bootstrap")
        except Exception as e:
            gate_debug(f"❌ BOOTSTRAP Fehler: {e}")
        _BOOTSTRAPPED = True
# --------------------------------------------------
def _extract_position_context_from_positions(positions):
    if not positions:
        return None

    def _read_float(payload, keys):
        for key in list(keys or []):
            try:
                value = payload.get(key)
            except Exception:
                value = None

            if value is None:
                continue

            try:
                number = float(value)
            except Exception:
                continue

            if number > 0.0:
                return float(number)

        return None

    for position in list(positions or []):
        if not isinstance(position, dict):
            continue

        contracts = position.get("contracts")
        try:
            if contracts is None or abs(float(contracts)) <= 0.0:
                continue
        except Exception:
            continue

        info = dict(position.get("info", {}) or {})

        side_raw = str(
            position.get(
                "side",
                info.get("side", info.get("posSide", info.get("positionSide", ""))),
            )
            or ""
        ).strip().lower()

        if side_raw in ("long", "buy"):
            side = "LONG"
        elif side_raw in ("short", "sell"):
            side = "SHORT"
        else:
            continue

        entry = _read_float(
            position,
            ("entryPrice", "entry_price", "avgPrice", "average", "avgEntryPrice"),
        )
        if entry is None:
            entry = _read_float(
                info,
                ("entryPrice", "avgEntryPrice", "avgEntryPx", "avgEntryPriceRp", "avgPx"),
            )

        tp = _read_float(
            position,
            ("takeProfitPrice", "takeProfit", "tp", "takeProfitRp"),
        )
        if tp is None:
            tp = _read_float(
                info,
                ("takeProfitPrice", "takeProfit", "takeProfitPx", "takeProfitRp", "tp"),
            )

        sl = _read_float(
            position,
            ("stopLossPrice", "stopLoss", "sl", "stopLossRp"),
        )
        if sl is None:
            sl = _read_float(
                info,
                ("stopLossPrice", "stopLoss", "stopLossPx", "stopLossRp", "sl"),
            )

        if entry is None or tp is None or sl is None:
            continue

        entry_ts = position.get("timestamp", info.get("timestamp", None))

        try:
            entry_ts = int(float(entry_ts)) if entry_ts is not None else None
        except Exception:
            entry_ts = None

        return {
            "id": position.get("id", info.get("orderID", info.get("orderId", None))),
            "source": "position_context",
            "side": str(side),
            "entry": float(entry),
            "tp": float(tp),
            "sl": float(sl),
            "entry_ts": entry_ts,
        }

    return None
# --------------------------------------------------
# get_active_order_snapshot - wird in rl_structure_bot.py genutz
# - prüft, ob aktuell eine Order offen ist (über _ACTIVE_ORDER_ID oder _POSITION_OPEN) 
# # --------------------------------------------------       
def get_active_order_snapshot():
    global _ACTIVE_ORDER_ID, _ACTIVE_SIDE, _ACTIVE_TP, _POSITION_OPEN, _ENTRY_REFERENCE, _RISK_REFERENCE

    def _read_order_float(order_payload, info_payload, keys):
        for source in (dict(order_payload or {}), dict(info_payload or {})):
            for key in list(keys or []):
                value = source.get(key)
                if value is None:
                    continue

                try:
                    number = float(value)
                except Exception:
                    continue

                if number > 0.0:
                    return float(number)

        return None

    exchange = _ensure_exchange()
    _bootstrap_once()
    open_orders = _safe_fetch_open_orders(exchange)

    if open_orders and len(open_orders) == 1:
        o = open_orders[0]
        info = o.get("info", {})

        try:
            # --------------------------------------------------
            # Exchange Timestamp (ms)
            # --------------------------------------------------
            order_ts_raw = o.get("timestamp")

            try:
                order_ts = int(float(order_ts_raw)) if order_ts_raw is not None else None
            except Exception:
                order_ts = None

            # --------------------------------------------------
            # Timeframe → ms berechnen
            # --------------------------------------------------
            tf = str(Config.TIMEFRAME).lower().strip()

            if tf.endswith("m"):
                tf_minutes = int(tf[:-1])
                timeframe_ms = tf_minutes * 60 * 1000
            elif tf.endswith("h"):
                tf_hours = int(tf[:-1])
                timeframe_ms = tf_hours * 60 * 60 * 1000
            else:
                timeframe_ms = 5 * 60 * 1000  # fallback 5m

            # --------------------------------------------------
            # Floor auf Candle-Open
            # --------------------------------------------------
            entry_ts = None
            if order_ts is not None:
                entry_ts = (order_ts // timeframe_ms) * timeframe_ms

            order_side = str(o.get("side") or "").strip().lower()
            side = "LONG"
            if order_side == "sell":
                side = "SHORT"

            return {
                "id": o.get("id"),
                "source": "open_order",
                "side": str(side),
                "entry": float(o.get("price")),
                "tp": _read_order_float(o, info, ("takeProfitPrice", "takeProfitRp", "takeProfit", "tp")),
                "sl": _read_order_float(o, info, ("stopLossPrice", "stopLossRp", "stopLoss", "sl")),
                "entry_ts": entry_ts,
            }

        except Exception:
            return None

    if isinstance(open_orders, list) and (not open_orders) and _ACTIVE_ORDER_ID is not None and str(_ACTIVE_ORDER_ID) != "MULTI_OPEN_ORDERS":
        vanished_order_id = _ACTIVE_ORDER_ID
        vanished_side = _ACTIVE_SIDE
        vanished_tp = _ACTIVE_TP

        _sync_with_exchange(reason="snapshot_order_missing_sync")

        if _POSITION_OPEN is True:
            if vanished_side is not None and _ACTIVE_SIDE is None:
                _ACTIVE_SIDE = vanished_side

            if vanished_tp is not None and _ACTIVE_TP is None:
                _ACTIVE_TP = vanished_tp

            gate_debug("🟢 Snapshot: LIVE FILL erkannt → Positionskontext für Bot-Handoff bereit")
        elif vanished_order_id is not None:
            mark_order_cancelled(vanished_order_id, cause="exchange_disappeared")
            return None

    if isinstance(open_orders, list) and (not open_orders) and bool(_POSITION_OPEN):
        positions = _safe_fetch_positions(exchange)
        position_snapshot = _extract_position_context_from_positions(positions)

        if isinstance(position_snapshot, dict):
            try:
                _ACTIVE_SIDE = "buy" if str(position_snapshot.get("side", "")).upper() == "LONG" else "sell"
                _ACTIVE_TP = float(position_snapshot.get("tp"))
                _ENTRY_REFERENCE = float(position_snapshot.get("entry"))
                _RISK_REFERENCE = abs(float(position_snapshot.get("entry")) - float(position_snapshot.get("sl")))
            except Exception:
                pass

            return dict(position_snapshot or {})

        try:
            side = str(_ACTIVE_SIDE or "").strip().lower()
            entry = float(_ENTRY_REFERENCE) if _ENTRY_REFERENCE is not None else None
            tp = float(_ACTIVE_TP) if _ACTIVE_TP is not None else None
            risk = float(_RISK_REFERENCE) if _RISK_REFERENCE is not None else None

            if side not in ("buy", "sell"):
                return None

            if entry is None or tp is None or risk is None or risk <= 0.0:
                return None

            if side == "buy":
                position_side = "LONG"
                sl = float(entry - risk)
            else:
                position_side = "SHORT"
                sl = float(entry + risk)

            return {
                "id": vanished_order_id if "vanished_order_id" in locals() else None,
                "source": "position_context",
                "side": str(position_side),
                "entry": float(entry),
                "tp": float(tp),
                "sl": float(sl),
                "entry_ts": None,
            }
        except Exception:
            return None

    return None
# --------------------------------------------------
def mark_order_cancelled(order_id, cause: str = None):
    global _CANCEL_COUNT, _CANCELLED_ORDER_IDS, _CANCELLED_ORDER_CAUSES

    if order_id is None:
        return

    oid = str(order_id)
    _CANCEL_COUNT += 1
    _CANCELLED_ORDER_IDS.add(oid)
    _CANCELLED_ORDER_CAUSES[oid] = str(cause or "exchange_cancel")

    if cause:
        try:
            gate_debug(f"🟠 CANCEL_TRACK | id={order_id} | cause={cause}")
            gate_debug("---------------------------------------")
        except Exception:
            pass
# --------------------------------------------------
def consume_cancelled(order_id) -> bool:
    return consume_cancelled_cause(order_id) is not None
# --------------------------------------------------
def consume_cancelled_cause(order_id):
    global _CANCELLED_ORDER_IDS, _CANCELLED_ORDER_CAUSES

    if order_id is None:
        return None

    oid = str(order_id)
    if oid in _CANCELLED_ORDER_IDS:
        try:
            _CANCELLED_ORDER_IDS.remove(oid)
        except Exception:
            pass

        try:
            return _CANCELLED_ORDER_CAUSES.pop(oid, None)
        except Exception:
            return None

    return None
# --------------------------------------------------
def get_cancel_count() -> int:
    return int(_CANCEL_COUNT or 0)
# --------------------------------------------------
