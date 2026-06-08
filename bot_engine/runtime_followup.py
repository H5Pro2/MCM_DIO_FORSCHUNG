def step_runtime_idle(bot, *, cycles=None, idle_cycle_resolver, idle_stepper, memory_loader):
    memory_loader()

    idle_cycles = cycles
    if idle_cycles is None:
        idle_cycles = idle_cycle_resolver()

    return idle_stepper(
        bot=bot,
        cycles=max(1, int(idle_cycles or 1)),
    )


def flush_runtime_followup(bot, *, visualization_flusher, memory_flusher):
    visualization_flusher()
    memory_flusher()
    return True


def run_runtime_idle_followup(
    bot,
    *,
    idle_cycle_resolver,
    idle_stepper,
    memory_loader,
    idle_protocol_writer,
    followup_flusher,
):
    idle_result = None
    if bot._runtime_seeded:
        idle_result = step_runtime_idle(
            bot,
            cycles=idle_cycle_resolver(),
            idle_cycle_resolver=idle_cycle_resolver,
            idle_stepper=idle_stepper,
            memory_loader=memory_loader,
        )
        idle_protocol_writer(idle_result)

    return followup_flusher()


def run_runtime_market_followup(
    bot,
    *,
    market_cycle_resolver,
    idle_step_func,
    followup_flusher,
):
    market_cycles = market_cycle_resolver()
    if bot._runtime_seeded and market_cycles > 0:
        idle_step_func(
            cycles=market_cycles,
        )

    return followup_flusher()
