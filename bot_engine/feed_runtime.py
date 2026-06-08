def run_runtime_loop(bot, *, queue_empty_exception):
    while True:
        if bot._runtime_stop_event.is_set() and bot._market_packet_queue.empty():
            break

        idle_sleep = bot._runtime_idle_sleep_seconds()

        try:
            packet = bot._market_packet_queue.get(timeout=idle_sleep)
        except queue_empty_exception:
            bot._run_runtime_idle_followup()
            continue

        try:
            bot._process_market_packet_and_followup(packet)
        finally:
            bot._market_packet_queue.task_done()


def consume_feed_windows(bot, windows):
    processed = 0

    for window in windows:
        bot._process_market_window_and_followup(window)
        processed += 1

    return processed


def iter_row_windows(bot, window_size=2, delay_seconds=0.0):
    buffer = []

    for row in bot.feed.rows(delay_seconds=delay_seconds):
        buffer.append(row)

        if len(buffer) < window_size:
            continue

        if len(buffer) > window_size:
            buffer.pop(0)

        yield list(buffer)


def process_market_packet_and_followup(bot, packet):
    result = bot._process_market_packet(packet)
    bot._run_runtime_market_followup()
    return result


def publish_market_window(bot, window):
    packet = bot._build_market_packet_from_window(window)
    if packet is None:
        return None

    return bot._publish_market_packet(packet)


def process_market_window_and_followup(bot, window):
    packet = bot._build_market_packet_from_window(window)
    if packet is None:
        return None

    return bot._process_market_packet_and_followup(packet)


def run_rows_buffer_loop(bot, *, window_size=2, delay_seconds=0.0):
    bot.processed = 0

    return bot._consume_feed_windows(
        bot._iter_row_windows(
            window_size=window_size,
            delay_seconds=delay_seconds,
        )
    )


def run_window_feed_loop(bot, *, size, delay_seconds=0.0):
    if not hasattr(bot, "processed"):
        bot.processed = 0

    return bot._consume_feed_windows(
        bot.feed.window(size, delay_seconds=delay_seconds)
    )
