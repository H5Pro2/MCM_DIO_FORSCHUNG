"""Runtime bridge helpers.

These helpers connect the bot object to the runtime class without owning the
Brain formulas. Compute/apply functions are injected by `MCM_Brain_Modell.py`.
"""

from __future__ import annotations


def step_mcm_runtime_idle(bot=None, cycles=1):
    if bot is None:
        return None

    runtime = getattr(bot, "mcm_runtime", None)
    if runtime is None:
        return None

    return runtime.advance_idle(
        cycles=max(1, int(cycles or 1)),
    )


def create_mcm_runtime(bot=None, *, runtime_cls=None):
    if runtime_cls is None:
        return None

    runtime = runtime_cls(bot=bot)
    runtime.restore_from_bot()
    return runtime


def step_mcm_runtime(
    window,
    candle_state,
    *,
    bot=None,
    tension_state=None,
    visual_market_state=None,
    structure_perception_state=None,
    temporal_perception_state=None,
    compute_runtime_result=None,
    apply_runtime_result=None,
):
    if bot is None or not window:
        return None

    runtime = getattr(bot, "mcm_runtime", None)

    if runtime is None:
        if compute_runtime_result is None or apply_runtime_result is None:
            return None

        runtime_result, decision_tendency, timestamp = compute_runtime_result(
            window,
            candle_state,
            bot=bot,
            tension_state=dict(tension_state or {}),
            visual_market_state=dict(visual_market_state or {}),
            structure_perception_state=dict(structure_perception_state or {}),
            temporal_perception_state=dict(temporal_perception_state or {}),
        )

        if runtime_result is None:
            return None

        return apply_runtime_result(
            bot,
            runtime_result,
            decision_tendency,
            timestamp,
            runtime_tick_seq=int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0) + 1,
            market_tick_advanced=True,
        )

    runtime.ingest_market_impulse(
        window,
        candle_state,
        tension_state=dict(tension_state or {}),
        visual_market_state=dict(visual_market_state or {}),
        structure_perception_state=dict(structure_perception_state or {}),
        temporal_perception_state=dict(temporal_perception_state or {}),
    )
    return runtime.advance(1)
