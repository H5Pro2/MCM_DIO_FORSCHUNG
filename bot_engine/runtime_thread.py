import queue
import threading
import time


def initialize_runtime_thread_state(bot):
    bot._runtime_thread = None
    bot._runtime_thread_lock = threading.Lock()
    bot._runtime_stop_event = threading.Event()
    bot._market_packet_queue = queue.Queue()
    bot._runtime_seeded = bool(bot.mcm_runtime is not None and bot.mcm_runtime.has_impulse())
    bot._last_regulation_state_snapshot = bot._build_regulation_state_snapshot()
    bot._memory_state_dirty = False
    bot._memory_state_last_save_ts = float(time.time())
    bot._snapshot_bundle = {}
    bot._snapshot_dirty = False
    bot._snapshot_write_seq = 0
    bot._snapshot_last_write_ts = 0.0
    bot._snapshot_last_state_key = None
    bot._last_live_market_packet_key = None
    bot._live_duplicate_market_packet_skips = 0
    bot._idle_thinking_protocol_seq = 0
    bot._idle_thinking_last_state_key = None
    bot._idle_thinking_last_depth = 0.0
    return True


def start_runtime_thread(bot):
    if bot._runtime_thread is not None and bot._runtime_thread.is_alive():
        return bot._runtime_thread

    with bot._runtime_thread_lock:
        if bot._runtime_thread is not None and bot._runtime_thread.is_alive():
            return bot._runtime_thread

        bot._runtime_stop_event.clear()
        bot._runtime_thread = threading.Thread(
            target=bot._runtime_loop,
            daemon=True,
        )
        bot._runtime_thread.start()

    return bot._runtime_thread


def stop_runtime_thread(bot, *, config, debug_enabled, debug_writer, save_memory=True):
    bot._runtime_stop_event.set()

    thread = bot._runtime_thread
    if thread is not None and thread.is_alive():
        timeout = max(0.1, float(getattr(config, "MCM_RUNTIME_THREAD_STOP_TIMEOUT_SECONDS", 5.0) or 5.0))
        thread.join(timeout=timeout)

        if thread.is_alive():
            if debug_enabled:
                debug_writer(
                    f"RUNTIME_THREAD_STOP_TIMEOUT | timeout={timeout:.2f}",
                    "runtime_thread_watchdog.csv",
                )
            return thread

    if bool(save_memory):
        bot._save_memory_state(force=True)
    return thread


def wait_until_runtime_idle(bot, *, config, debug_enabled, debug_writer):
    timeout = max(0.1, float(getattr(config, "MCM_RUNTIME_QUEUE_IDLE_TIMEOUT_SECONDS", 30.0) or 30.0))
    poll_seconds = max(
        0.0,
        float(getattr(config, "GLOBAL_COGNITIVE_REACTION_SECONDS", 0.001) or 0.001),
    )
    deadline = time.time() + timeout

    while int(bot._market_packet_queue.unfinished_tasks or 0) > 0:
        if time.time() >= deadline:
            if debug_enabled:
                debug_writer(
                    f"RUNTIME_QUEUE_IDLE_TIMEOUT | unfinished={int(bot._market_packet_queue.unfinished_tasks or 0)} | timeout={timeout:.2f}",
                    "runtime_thread_watchdog.csv",
                )
            return False
        time.sleep(poll_seconds)

    return True


def get_queue_empty_exception():
    return queue.Empty
