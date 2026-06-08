import os


def _clean(value):
    return str(value).replace("\n", " ").replace(";", "|")


def _num(source, key_name, default=0.0):
    try:
        return float((source or {}).get(key_name, default) or default)
    except Exception:
        return float(default)


def record_visual_cortex_protocol(
    bot,
    window,
    visual_market_state,
    *,
    config,
    dbr_path_func,
    dbr_append_text_func,
    normalize_market_window_func,
):
    if not bool(getattr(config, "MCM_VISUAL_CORTEX_PROTOCOL_DEBUG", True)):
        return False

    visual = dict(visual_market_state or {})
    form_state = dict(visual.get("visual_form_state", {}) or {})
    axes = dict(form_state.get("axes", {}) or {})
    if not visual:
        return False

    local_window = normalize_market_window_func(window)
    timestamp = local_window[-1].get("timestamp") if local_window else getattr(bot, "current_timestamp", None)
    visual_form_id = str(form_state.get("visual_form_id", "-") or "-")
    clarity_bucket = int(round(float(visual.get("visual_clarity", 0.0) or 0.0) * 10.0))
    blindness_bucket = int(round(float(visual.get("visual_blindness", 0.0) or 0.0) * 10.0))
    pressure_bucket = int(round(float(visual.get("visual_form_pressure", 0.0) or 0.0) * 10.0))

    protocol = dict(getattr(bot, "mcm_visual_cortex_protocol", {}) or {})
    sequence = int(protocol.get("sequence", 0) or 0) + 1
    key = f"{visual_form_id}|c{clarity_bucket}|b{blindness_bucket}|p{pressure_bucket}"
    changed = bool(str(protocol.get("last_key", "") or "") != key)
    every_n = max(1, int(getattr(config, "MCM_VISUAL_CORTEX_PROTOCOL_EVERY_N", 5) or 5))

    protocol.update({
        "sequence": int(sequence),
        "last_key": str(key),
        "last_visual_form_id": str(visual_form_id),
        "last_timestamp": timestamp,
    })
    setattr(bot, "mcm_visual_cortex_protocol", dict(protocol))

    if not changed and (sequence % every_n) != 0:
        return False

    path = dbr_path_func("mcm_visual_cortex_protocol.csv")
    header_key = "_visual_cortex_protocol_header_written"
    write_header = (not os.path.exists(path)) and not bool(getattr(bot, header_key, False))

    payload = ""
    if write_header:
        payload += (
            "timestamp;sequence;visual_form_id;visual_clarity;visual_object_stability;"
            "visual_form_novelty;visual_blindness;visual_form_pressure;visual_shape_resonance;"
            "visual_shape_fragility;edge_strength;curvature;density;fracture;flow;void;"
            "range_rhythm;direction_consistency;spatial_bias;directional_bias;range_position;"
            "short_impulse;mid_impulse;compression;expansion;body_pressure;wick_pressure;"
            "volume_bias;market_balance;breakout_tension;visual_coherence;"
            "sensory_reality_pressure;sensory_load;sensory_redundancy;sensory_habituation;"
            "sensory_gate;sensory_active_axis_count;sensory_primary_pressure;sensory_reality_label\n"
        )
        setattr(bot, header_key, True)

    row = [
        _clean(timestamp),
        int(sequence),
        _clean(visual_form_id),
        f"{_num(visual, 'visual_clarity'):.4f}",
        f"{_num(visual, 'visual_object_stability'):.4f}",
        f"{_num(visual, 'visual_form_novelty'):.4f}",
        f"{_num(visual, 'visual_blindness'):.4f}",
        f"{_num(visual, 'visual_form_pressure'):.4f}",
        f"{_num(visual, 'visual_shape_resonance'):.4f}",
        f"{_num(visual, 'visual_shape_fragility'):.4f}",
        f"{_num(axes, 'edge_strength'):.4f}",
        f"{_num(axes, 'curvature'):.4f}",
        f"{_num(axes, 'density'):.4f}",
        f"{_num(axes, 'fracture'):.4f}",
        f"{_num(axes, 'flow'):.4f}",
        f"{_num(axes, 'void'):.4f}",
        f"{_num(axes, 'range_rhythm'):.4f}",
        f"{_num(axes, 'direction_consistency'):.4f}",
        f"{_num(visual, 'spatial_bias'):.4f}",
        f"{_num(visual, 'directional_bias'):.4f}",
        f"{_num(visual, 'range_position'):.4f}",
        f"{_num(visual, 'short_impulse'):.4f}",
        f"{_num(visual, 'mid_impulse'):.4f}",
        f"{_num(visual, 'compression'):.4f}",
        f"{_num(visual, 'expansion'):.4f}",
        f"{_num(visual, 'body_pressure'):.4f}",
        f"{_num(visual, 'wick_pressure'):.4f}",
        f"{_num(visual, 'volume_bias'):.4f}",
        f"{_num(visual, 'market_balance'):.4f}",
        f"{_num(visual, 'breakout_tension'):.4f}",
        f"{_num(visual, 'visual_coherence'):.4f}",
        f"{_num(visual, 'sensory_reality_pressure'):.4f}",
        f"{_num(visual, 'sensory_load'):.4f}",
        f"{_num(visual, 'sensory_redundancy'):.4f}",
        f"{_num(visual, 'sensory_habituation'):.4f}",
        f"{_num(visual, 'sensory_gate', 1.0):.4f}",
        int(_num(visual, 'sensory_active_axis_count')),
        f"{_num(visual, 'sensory_primary_pressure'):.4f}",
        _clean(visual.get("sensory_reality_label", "quiet_outer_reality")),
    ]
    payload += ";".join(str(item) for item in row) + "\n"
    dbr_append_text_func(path, payload, operation="visual_cortex_protocol_append")
    return True
