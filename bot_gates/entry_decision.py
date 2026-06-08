# ==================================================
# bot_gate_funktions.py
# Entry / Gate / Strategie Mechanik außerhalb von bot.py
# ==================================================
from config import Config
from debug_tools.writers import dbr_append_text, dbr_debug, dbr_path
from MCM_Brain_Modell import build_runtime_decision_tendency, decide_mcm_brain_entry


DEBUG = True


def _entry_bridge_debug(line):
    try:
        dbr_append_text(dbr_path("entry_debug.csv"), str(line or "") + "\n", operation="entry_bridge_debug")
    except Exception:
        pass


def _clip01(value):
    try:
        value = float(value)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return max(0.0, min(1.0, value))


def _num(mapping, key, default=0.0):
    try:
        return float((mapping or {}).get(key, default) or default)
    except Exception:
        return float(default)


def _num_any(mapping, *keys, default=0.0):
    source = mapping or {}
    for key in keys:
        if key in source:
            try:
                return float(source.get(key, default) or default)
            except Exception:
                return float(default)
    return float(default)


def _first_signal_value(*values, default=0.0):
    for value in values:
        try:
            number = float(value or 0.0)
        except Exception:
            number = 0.0
        if number != 0.0:
            return number
    return float(default)


def _resolve_inner_action_consent(decision):
    decision_state = dict(decision or {})
    meta = dict(decision_state.get("meta_regulation_state", {}) or {})
    expectation = dict(decision_state.get("expectation_state", {}) or {})
    form = dict(decision_state.get("form_symbol_state", {}) or {})
    thought = dict(decision_state.get("thought_state", {}) or {})
    thought_seed = dict(decision_state.get("thought_seed_state", {}) or {})
    structure = dict(decision_state.get("structure_perception_state", {}) or {})
    pre_action_phase = str(meta.get("pre_action_phase", decision_state.get("decision_tendency", "hold")) or "hold").strip().lower()

    entry_mode = str(decision_state.get("entry_mode", "no_mature_entry_thesis") or "no_mature_entry_thesis")
    entry_contact_state = str(
        decision_state.get("entry_contact_state", decision_state.get("entry_choice_state", "no_entry_choice"))
        or "no_entry_choice"
    )
    entry_choice_state = str(decision_state.get("entry_choice_state", entry_contact_state) or entry_contact_state)
    impulse_only = entry_mode == "impulse_contact" or entry_choice_state in ("impulse_only", "impulse_preferred")

    inner_alignment = _clip01(meta.get("inner_outer_alignment", 0.0))
    regulated_courage = _clip01(meta.get("regulated_courage", 0.0))
    action_clearance = _clip01(meta.get("action_clearance", 0.0))
    action_inhibition = _clip01(meta.get("action_inhibition", 0.0))
    field_observation_need = _clip01(meta.get("field_observation_need", 0.0))
    pre_action_reorganization = _clip01(meta.get("pre_action_reorganization_pressure", 0.0))
    trust_return = _clip01(meta.get("trust_return_act_bridge", 0.0))
    open_hypothesis_reality_bearing = _clip01(
        meta.get(
            "open_hypothesis_reality_bearing",
            meta.get("open_hypothesis_reality_fit", meta.get("open_hypothesis_reality_permission", meta.get("open_hypothesis_action_permission", 0.0))),
        )
    )
    open_hypothesis_reality_fit = float(open_hypothesis_reality_bearing)
    # A hypothesis is a thought probe. It can describe reality contact, but it
    # must not become an action permission by itself. Older `*_action_*` names
    # are read only as compatibility aliases.
    open_hypothesis_reality_probe = float(open_hypothesis_reality_bearing)
    open_hypothesis_reality_permission = float(open_hypothesis_reality_bearing)
    nervous_reflection = _clip01(meta.get("nervous_overload_reflection_need", 0.0))
    possibility_contact_bearing = _clip01(meta.get("possibility_contact_bearing", meta.get("possibility_action_support", 0.0)))
    possibility_action_support = float(possibility_contact_bearing)
    possibility_reality_check_need = _clip01(meta.get("possibility_reality_check_need", 0.0))
    hypothesis_trust_score = _clip01(meta.get("hypothesis_trust_score", 0.0))
    hypothesis_trust_priority = _clip01(meta.get("hypothesis_trust_priority", 0.0))
    dominant_hypothesis_trust_score_raw = _clip01(meta.get("dominant_hypothesis_trust_score", 0.0))
    dominant_hypothesis_action_readiness_raw = _clip01(meta.get("dominant_hypothesis_reality_bearing", meta.get("dominant_hypothesis_action_readiness", 0.0)))
    dominant_hypothesis_trust_key = str(meta.get("dominant_hypothesis_trust_key", "-") or "-").strip()
    hypothesis_confirmation_without_action = _clip01(meta.get("hypothesis_confirmation_without_action", 0.0))
    hypothesis_rejection_without_action = _clip01(meta.get("hypothesis_rejection_without_action", 0.0))
    hypothesis_observation_maturity = _clip01(meta.get("hypothesis_observation_maturity", 0.0))
    hypothesis_observed_stability = _clip01(meta.get("hypothesis_observed_stability", 0.0))
    hypothesis_frustration_risk = _clip01(meta.get("hypothesis_frustration_risk", 0.0))
    hypothesis_distance_risk = _clip01(meta.get("hypothesis_distance_risk", 0.0))
    previous_open_hypothesis_learning_state = str(meta.get("previous_open_hypothesis_learning_state", "-") or "-").strip()
    open_hypothesis_reifung_state = str(meta.get("open_hypothesis_reifung_state", "-") or "-").strip()

    contact_carrying = _clip01(meta.get("contact_carrying_quality", 0.0))
    contact_maturity = _clip01(meta.get("contact_action_maturity", 0.0))
    contact_overcoupling = _clip01(meta.get("contact_overcoupling_risk", 0.0))
    contact_reality_check = _clip01(meta.get("contact_reality_check", 0.0))
    mcm_reflective_bearing = _clip01(meta.get("mcm_reflective_bearing", 0.0))
    mcm_reflective_pressure = _clip01(meta.get("mcm_reflective_pressure", 0.0))
    mcm_reflective_coupling_load = _clip01(meta.get("mcm_reflective_coupling_load", 0.0))
    market_hearing_state = dict(decision_state.get("market_hearing_state", meta.get("market_hearing_state", {})) or {})
    market_loudness = _clip01(
        _first_signal_value(
            decision_state.get("market_loudness", 0.0),
            meta.get("market_loudness", 0.0),
            market_hearing_state.get("loudness", 0.0),
        )
    )
    market_hearing_compression = _clip01(
        _first_signal_value(
            decision_state.get("market_hearing_compression", 0.0),
            meta.get("market_hearing_compression", 0.0),
            market_hearing_state.get("compression", 0.0),
        )
    )
    market_frequency_hz = max(
        0.0,
        _first_signal_value(
            decision_state.get("market_frequency_hz", 0.0),
            meta.get("market_frequency_hz", 0.0),
            market_hearing_state.get("frequency_hz", 0.0),
        ),
    )
    market_frequency_presence = _clip01(market_frequency_hz / 17000.0)
    energy_coherence_bearing = _clip01(
        (contact_carrying * 0.26)
        + (inner_alignment * 0.22)
        + (mcm_reflective_bearing * 0.16)
        + (market_loudness * 0.14)
        + (market_hearing_compression * 0.10)
        + (market_frequency_presence * 0.06)
        - (contact_overcoupling * 0.10)
        - (mcm_reflective_pressure * 0.08)
    )

    structure_quality = _clip01(structure.get("structure_quality", 0.0))
    context_confidence = _clip01(structure.get("context_confidence", 0.0))
    target_expectation = _clip01(expectation.get("target_expectation", decision_state.get("target_expectation", 0.0)))
    reflection_maturity = _clip01(expectation.get("reflection_maturity", 0.0))

    form_action_trust = _clip01(form.get("form_symbol_action_trust", 0.0))
    form_contact_maturity = _clip01(form.get("form_symbol_contact_maturity", 0.0))
    form_contact_utility = _clip01(form.get("form_symbol_contact_utility", 0.0))
    form_contact_pain_memory = _clip01(form.get("form_symbol_contact_pain_memory", 0.0))
    form_contact_carefulness = _clip01(form.get("form_symbol_contact_carefulness", 0.0))
    form_contact_burden_evidence = _clip01(form.get("form_symbol_contact_burden_evidence", 0.0))
    form_contact_utility_evidence = _clip01(form.get("form_symbol_contact_utility_evidence", 0.0))
    form_contact_burden = _clip01(
        (form_contact_pain_memory * 0.34)
        + (form_contact_carefulness * 0.24)
        + (form_contact_burden_evidence * 0.28)
        - (form_contact_utility * 0.14)
        - (form_contact_utility_evidence * 0.10)
    )
    form_contact_usefulness = _clip01(
        (form_contact_utility * 0.42)
        + (form_contact_utility_evidence * 0.28)
        + (form_contact_maturity * 0.18)
        - (form_contact_pain_memory * 0.18)
        - (form_contact_burden_evidence * 0.16)
    )
    form_symbol_id = str(form.get("form_symbol_id", decision_state.get("form_symbol_id", "-")) or "-").strip()
    side_key = str(
        decision_state.get("proposed_decision", decision_state.get("decision", "-")) or "-"
    ).strip().upper()
    area_contact_focus_id = str(
        decision_state.get("area_contact_focus_id", decision_state.get("strategic_area_focus_id", ""))
        or ""
    ).strip()
    area_contact_location = str(
        decision_state.get("area_contact_location", decision_state.get("strategic_entry_location", ""))
        or ""
    ).strip()
    strategic_area_focus_id = str(decision_state.get("strategic_area_focus_id", area_contact_focus_id) or "").strip()
    strategic_entry_location = str(decision_state.get("strategic_entry_location", area_contact_location) or "").strip()
    possibility_state = dict(meta.get("mcm_possibility_field_state", {}) or {})
    possibility_variant_id = str(
        possibility_state.get("possibility_dominant_variant_id", meta.get("possibility_dominant_variant_id", "")) or ""
    ).strip()
    form_hypothesis_keys = {
        key for key in (
            form_symbol_id,
            str(form.get("form_symbol_compound_id", "") or "").strip(),
            str(form.get("form_symbol_semantic_profile", "") or "").strip(),
        )
        if key and key != "-"
    }
    thought_confirmation = _clip01(thought.get("thought_confirmation_score", thought.get("trust_return_readiness", 0.0)))
    dominant_trust_matches_form = bool(
        dominant_hypothesis_trust_key
        and dominant_hypothesis_trust_key != "-"
        and dominant_hypothesis_trust_key in form_hypothesis_keys
    )
    dominant_hypothesis_trust_score = (
        dominant_hypothesis_trust_score_raw
        if dominant_trust_matches_form
        else dominant_hypothesis_trust_score_raw * 0.12
    )
    dominant_hypothesis_reality_support = (
        dominant_hypothesis_action_readiness_raw
        if dominant_trust_matches_form
        else dominant_hypothesis_action_readiness_raw * 0.12
    )
    dominant_hypothesis_reality_bearing = float(dominant_hypothesis_reality_support)
    borrowed_dominant_hypothesis_pressure = _clip01(
        dominant_hypothesis_trust_score_raw - dominant_hypothesis_trust_score
    )

    structure_aliases = {
        "confirmed_structural_interpretation": "confirmed_structure_contact",
        "open_structural_hypothesis": "open_structure_contact",
        "wide_target_without_structure": "wide_range_without_structure",
        "ordinary_structure_reading": "ordinary_structure_contact",
    }
    seed_emergent_structure_state = str(
        thought_seed.get("emergent_structure_state", "ordinary_structure_contact")
        or "ordinary_structure_contact"
    ).strip()
    seed_emergent_structure_state = structure_aliases.get(seed_emergent_structure_state, seed_emergent_structure_state)
    pre_entry_emergent_structure_state = str(
        decision_state.get("pre_entry_emergent_structure_state", "")
        or ""
    ).strip()
    pre_entry_emergent_structure_state = structure_aliases.get(pre_entry_emergent_structure_state, pre_entry_emergent_structure_state)
    emergent_structure_state = seed_emergent_structure_state
    if (
        emergent_structure_state in ("", "ordinary_structure_contact")
        and pre_entry_emergent_structure_state
        and pre_entry_emergent_structure_state != "ordinary_structure_contact"
    ):
        emergent_structure_state = pre_entry_emergent_structure_state
    seed_metaregulator_state = str(thought_seed.get("seed_metaregulator_state", "seed_release") or "seed_release").strip()
    seed_confirmation = _clip01(thought_seed.get("thought_confirmation_score", 0.0))
    seed_reality_binding = _clip01(thought_seed.get("reality_binding_score", 0.0))
    seed_grounding = _clip01(thought_seed.get("thought_structural_grounding", 0.0))
    seed_open_pressure = _clip01(thought_seed.get("thought_open_hypothesis_pressure", 0.0))
    seed_trust_return = _clip01(thought_seed.get("trust_return_readiness", 0.0))
    seed_returned_trust = _clip01(thought_seed.get("thought_digestive_returned_trust", 0.0))
    seed_integration_pull = _clip01(thought_seed.get("thought_digestive_integration_pull", 0.0))
    seed_reality_lag = _clip01(thought_seed.get("thought_reality_lag", 0.0))
    seed_reorganization_echo = _clip01(thought_seed.get("reorganization_echo", 0.0))
    seed_consequence_echo = _clip01(thought_seed.get("consequence_echo", 0.0))
    seed_borrowed_pressure = _clip01(thought_seed.get("borrowed_open_hypothesis_pressure", 0.0))
    carried_hypothesis_memory = (
        previous_open_hypothesis_learning_state == "open_hypothesis_carried"
        or open_hypothesis_reifung_state == "open_hypothesis_carried_memory"
    )
    burdened_hypothesis_memory = previous_open_hypothesis_learning_state in (
        "open_hypothesis_burdened",
        "open_hypothesis_reorganizing",
    ) or open_hypothesis_reifung_state == "open_hypothesis_reorganizing_memory"
    confirmed_current_hypothesis = emergent_structure_state == "confirmed_structure_contact"
    open_current_hypothesis = emergent_structure_state == "open_structure_contact"
    current_hypothesis_reality_support = _clip01(
        (0.28 if confirmed_current_hypothesis else 0.0)
        + (0.16 if seed_metaregulator_state in ("seed_action_ready", "seed_mature") else 0.0)
        + (0.14 if carried_hypothesis_memory else 0.0)
        + (seed_confirmation * 0.16)
        + (seed_reality_binding * 0.14)
        + (seed_grounding * 0.12)
        + (seed_trust_return * 0.10)
        + (seed_returned_trust * 0.08)
        + (seed_integration_pull * 0.06)
        - (0.12 if burdened_hypothesis_memory else 0.0)
    )
    current_hypothesis_reality_bearing = float(current_hypothesis_reality_support)
    current_hypothesis_reality_need = _clip01(
        (0.12 if open_current_hypothesis else 0.0)
        + (0.16 if seed_metaregulator_state in ("seed_reinterpret", "seed_drift_watch", "seed_overthinking_watch") else 0.0)
        + (0.10 if burdened_hypothesis_memory else 0.0)
        + (seed_open_pressure * 0.18)
        + (seed_reality_lag * 0.16)
        + (seed_borrowed_pressure * 0.12)
        + (max(0.0, 0.46 - seed_grounding) * 0.14)
        + (max(0.0, 0.48 - seed_confirmation) * 0.12)
        + (max(0.0, 0.42 - seed_reality_binding) * 0.10)
        + (max(0.0, seed_reorganization_echo - seed_consequence_echo) * 0.10)
        - (0.14 if confirmed_current_hypothesis else 0.0)
        - (0.10 if carried_hypothesis_memory else 0.0)
    )

    area_readiness = _clip01(decision_state.get("area_contact_readiness", decision_state.get("area_direct_readiness", 0.0)))
    area_bearing = _clip01(decision_state.get("entry_contact_bearing", decision_state.get("entry_choice_bearing", 0.0)))
    contact_fit = _clip01(decision_state.get("area_contact_fit", decision_state.get("contact_entry_fit", decision_state.get("strategic_entry_fit", 0.0))))
    motor_restraint = _clip01(decision_state.get("area_contact_restraint", decision_state.get("area_motor_restraint", 0.0)))
    entry_geometry_bearing = _clip01(decision_state.get("entry_geometry_bearing", 0.0))
    organic_contact_bearing = _clip01(decision_state.get("organic_contact_bearing", 0.0))
    visual_reality_bearing = _clip01(decision_state.get("visual_reality_bearing", 0.0))
    felt_reality_bearing = _clip01(decision_state.get("felt_reality_bearing", 0.0))
    form_mcm_reality_fit = _clip01(decision_state.get("form_mcm_reality_fit", 0.0))
    receptive_contact_offer_pressure = _clip01(decision_state.get("receptive_contact_offer_pressure", 0.0))
    receptive_contact_maturity = _clip01(decision_state.get("receptive_contact_maturity", 1.0))
    receptive_contact_immaturity_pressure = _clip01(decision_state.get("receptive_contact_immaturity_pressure", 0.0))
    receptive_contact_restraint = _clip01(decision_state.get("receptive_contact_restraint", 0.0))
    has_real_area_contact = bool(
        entry_mode.startswith("area_contact")
        or entry_contact_state in ("area_contact_preferred", "area_contact_available")
        or str(area_contact_location or "").strip() not in ("", "-", "no_mature_entry_thesis")
    )
    # Hypothesen sind vorerst keine Handlungsquelle. Diese Neutralisierung
    # betrifft nur Consent/Motorik; Debug- und Speicherfelder koennen weiter
    # existieren, ohne Entry-Druck zu erzeugen.
    open_hypothesis_reality_bearing = 0.0
    open_hypothesis_reality_fit = 0.0
    open_hypothesis_reality_probe = 0.0
    open_hypothesis_reality_permission = 0.0
    hypothesis_trust_score = 0.0
    hypothesis_trust_priority = 0.0
    dominant_hypothesis_trust_score = 0.0
    dominant_hypothesis_reality_support = 0.0
    dominant_hypothesis_reality_bearing = 0.0
    borrowed_dominant_hypothesis_pressure = 0.0
    hypothesis_confirmation_without_action = 0.0
    hypothesis_rejection_without_action = 0.0
    hypothesis_observation_maturity = 0.0
    hypothesis_observed_stability = 0.0
    hypothesis_frustration_risk = 0.0
    hypothesis_distance_risk = 0.0
    current_hypothesis_reality_bearing = 0.0
    current_hypothesis_reality_support = 0.0
    current_hypothesis_reality_need = 0.0
    seed_open_pressure = 0.0
    seed_reality_lag = 0.0
    seed_borrowed_pressure = 0.0
    thought_confirmation_bearing = _clip01(
        (hypothesis_confirmation_without_action * hypothesis_observation_maturity * 0.34)
        + (hypothesis_trust_priority * 0.24)
        + (hypothesis_trust_score * 0.18)
        + (dominant_hypothesis_trust_score * 0.16)
        + (dominant_hypothesis_reality_bearing * 0.10)
        + (hypothesis_observed_stability * 0.08)
        + (current_hypothesis_reality_bearing * 0.16)
    )
    thought_rejection_pressure = _clip01(
        (hypothesis_rejection_without_action * hypothesis_observation_maturity * 0.34)
        + (possibility_reality_check_need * 0.22)
        + (hypothesis_frustration_risk * 0.18)
        + (hypothesis_distance_risk * 0.14)
        + (max(0.0, 0.26 - hypothesis_observed_stability) * 0.08)
        + (current_hypothesis_reality_need * 0.18)
        + (borrowed_dominant_hypothesis_pressure * 0.10)
    )
    thought_trust_bearing = _clip01(
        (thought_confirmation_bearing * 0.42)
        + (possibility_contact_bearing * 0.24)
        + (form_action_trust * 0.12)
        + (open_hypothesis_reality_probe * 0.10)
        + (trust_return * 0.08)
        - (thought_rejection_pressure * 0.24)
    )
    contact_context_bearing = _clip01(
        (max(area_readiness, area_bearing, contact_fit) * 0.34)
        + (contact_carrying * 0.14)
        + (target_expectation * 0.12)
        + (mcm_reflective_bearing * 0.10)
        + (inner_alignment * 0.08)
    )
    thought_gap_pressure = _clip01(max(0.0, thought_rejection_pressure - thought_confirmation_bearing))
    thought_contact_consent = _clip01(
        (thought_trust_bearing * 0.44)
        + (thought_confirmation_bearing * 0.26)
        + (current_hypothesis_reality_bearing * 0.14)
        + (dominant_hypothesis_reality_bearing * 0.10)
        + (possibility_contact_bearing * 0.06)
        - (thought_rejection_pressure * 0.18)
    )
    untrusted_contact_pressure = _clip01(
        (contact_reality_check * 0.30)
        + (contact_overcoupling * 0.24)
        + (mcm_reflective_pressure * 0.18)
        + (mcm_reflective_coupling_load * 0.14)
        + (form_contact_burden * 0.14)
        + (receptive_contact_immaturity_pressure * 0.10)
    )
    thought_motor_bearing = 0.0
    thought_motor_pressure = 0.0
    thought_area_coupling = _clip01(
        (thought_contact_consent * 0.30)
        + (thought_confirmation_bearing * 0.22)
        + (thought_trust_bearing * 0.18)
        + (current_hypothesis_reality_bearing * 0.14)
        + (dominant_hypothesis_reality_bearing * 0.10)
        + (trust_return * 0.06)
    )
    felt_area_coupling = _clip01(
        (contact_context_bearing * 0.22)
        + (contact_carrying * 0.18)
        + (energy_coherence_bearing * 0.16)
        + (contact_maturity * 0.14)
        + (mcm_reflective_bearing * 0.12)
        + (form_contact_maturity * 0.12)
        + (form_contact_usefulness * 0.08)
        + (inner_alignment * 0.12)
        + (reflection_maturity * 0.08)
        + (target_expectation * 0.06)
        + (structure_quality * 0.05)
        - (form_contact_burden * 0.10)
        - (contact_overcoupling * 0.12)
        - (contact_reality_check * 0.08)
        - (mcm_reflective_pressure * 0.06)
    )
    sensory_area_coupling = _clip01(
        (felt_area_coupling * 0.78)
        + (mcm_reflective_bearing * 0.12)
        + (contact_context_bearing * 0.10)
    )
    raw_area_contact_bearing = _clip01(
        (
            (area_readiness * 0.30)
            + (area_bearing * 0.30)
            + (contact_fit * 0.22)
            + (contact_context_bearing * 0.18)
        )
        if has_real_area_contact
        else 0.0
    )
    uncoupled_area_contact_pressure = _clip01(
        (
            (raw_area_contact_bearing * max(0.0, 0.56 - sensory_area_coupling) * 0.58)
            + (mcm_reflective_pressure * 0.12)
            + (contact_reality_check * 0.10)
            - (felt_area_coupling * 0.08)
            - (contact_carrying * form_contact_maturity * 0.10)
        )
        if has_real_area_contact
        else 0.0
    )
    real_area_contact_bearing = _clip01(
        (
            raw_area_contact_bearing
            * (
                0.28
                + (sensory_area_coupling * 0.34)
                + (felt_area_coupling * 0.22)
                + (mcm_reflective_bearing * 0.12)
            )
            - (untrusted_contact_pressure * 0.10)
            - (uncoupled_area_contact_pressure * 0.12)
        )
        if has_real_area_contact
        else 0.0
    )
    contact_memory_evidence = _clip01(
        max(
            form_action_trust,
            form_contact_maturity,
            form_contact_usefulness,
            form_contact_burden,
            form_contact_utility_evidence,
            form_contact_burden_evidence,
        )
    )
    receptive_contact_memory_gap = _clip01(1.0 - contact_memory_evidence)
    receptive_exploration_bearing = _clip01(
        (
            (
                (raw_area_contact_bearing * 0.20)
                + (real_area_contact_bearing * 0.18)
                + (organic_contact_bearing * 0.16)
                + (entry_geometry_bearing * 0.12)
                + (energy_coherence_bearing * 0.18)
                + (visual_reality_bearing * 0.04)
                + (form_mcm_reality_fit * 0.10)
                + (felt_area_coupling * 0.08)
                + (felt_reality_bearing * 0.04)
            )
            * (0.18 + (receptive_contact_memory_gap * 0.32))
            - (untrusted_contact_pressure * 0.08)
            - (uncoupled_area_contact_pressure * 0.08)
            - (contact_overcoupling * 0.06)
        )
        if has_real_area_contact
        else 0.0
    )
    thought_reality_coupled_bearing = _clip01(
        thought_motor_bearing
    )
    receptive_contact_bearing = _clip01(
        (real_area_contact_bearing * 0.34)
        + (felt_area_coupling * 0.26)
        + (contact_context_bearing * 0.18)
        + (mcm_reflective_bearing * 0.12)
        + (contact_carrying * 0.10)
        + (receptive_exploration_bearing * 0.08)
    )
    raw_thought_contradiction_pressure = _clip01(
        (thought_gap_pressure * 0.52)
        + (max(0.0, 0.18 - thought_trust_bearing) * 0.18)
        + (max(0.0, possibility_reality_check_need - possibility_contact_bearing) * 0.16)
        + (untrusted_contact_pressure * 0.12)
    )
    thought_contradiction_pressure = _clip01(
        thought_motor_pressure
    )
    analytic_action_bearing = _clip01(
        thought_motor_bearing
    )
    intuitive_action_bearing = _clip01(
        (felt_area_coupling * 0.26)
        + (contact_context_bearing * 0.20)
        + (real_area_contact_bearing * 0.18)
        + (receptive_exploration_bearing * 0.16)
        + (contact_carrying * 0.12)
        + (inner_alignment * 0.10)
        + (target_expectation * 0.08)
        + (reflection_maturity * 0.06)
        - (contact_reality_check * 0.08)
        - (contact_overcoupling * 0.08)
    )
    conscious_action_bearing = _clip01(max(analytic_action_bearing, intuitive_action_bearing))
    thought_consent_trace = {
        "thought_confirmation_bearing": float(thought_confirmation_bearing),
        "thought_rejection_pressure": float(thought_rejection_pressure),
        "thought_trust_bearing": float(thought_trust_bearing),
        "contact_context_bearing": float(contact_context_bearing),
        "raw_thought_contradiction_pressure": float(raw_thought_contradiction_pressure),
        "thought_contradiction_pressure": float(thought_contradiction_pressure),
        "strategy_confirmation": 0.0,
        "strategy_rejection": 0.0,
        "strategy_trust_bearing": 0.0,
        "strategy_context_bearing": 0.0,
        "raw_strategy_contradiction_pressure": 0.0,
        "strategy_contradiction_pressure": 0.0,
        "strategy_alias_state": "deprecated_receptive_coupling_active",
        "open_hypothesis_reality_bearing": float(open_hypothesis_reality_bearing),
        "open_hypothesis_reality_fit": float(open_hypothesis_reality_fit),
        "open_hypothesis_reality_probe": float(open_hypothesis_reality_probe),
        "open_hypothesis_reality_permission": float(open_hypothesis_reality_permission),
        "possibility_contact_bearing": float(possibility_contact_bearing),
        "dominant_hypothesis_reality_bearing": float(dominant_hypothesis_reality_bearing),
        "dominant_hypothesis_reality_support": float(dominant_hypothesis_reality_support),
        "current_hypothesis_reality_bearing": float(current_hypothesis_reality_bearing),
        "current_hypothesis_reality_support": float(current_hypothesis_reality_support),
        "hypothesis_role": "thought_reality_probe",
        "thought_contact_consent": float(thought_contact_consent),
        "thought_area_coupling": float(thought_area_coupling),
        "felt_area_coupling": float(felt_area_coupling),
        "sensory_area_coupling": float(sensory_area_coupling),
        "thought_reality_coupled_bearing": float(thought_reality_coupled_bearing),
        "receptive_contact_bearing": float(receptive_contact_bearing),
        "analytic_action_bearing": float(analytic_action_bearing),
        "intuitive_action_bearing": float(intuitive_action_bearing),
        "conscious_action_bearing": float(conscious_action_bearing),
        "form_contact_usefulness": float(form_contact_usefulness),
        "form_contact_burden": float(form_contact_burden),
        "mcm_reflective_bearing": float(mcm_reflective_bearing),
        "mcm_reflective_pressure": float(mcm_reflective_pressure),
        "mcm_reflective_coupling_load": float(mcm_reflective_coupling_load),
        "market_loudness": float(market_loudness),
        "market_frequency_hz": float(market_frequency_hz),
        "market_hearing_compression": float(market_hearing_compression),
        "market_hearing_state": dict(market_hearing_state),
        "energy_coherence_bearing": float(energy_coherence_bearing),
        "untrusted_contact_pressure": float(untrusted_contact_pressure),
        "uncoupled_area_contact_pressure": float(uncoupled_area_contact_pressure),
        "raw_area_contact_bearing": float(raw_area_contact_bearing),
        "real_area_contact_bearing": float(real_area_contact_bearing),
        "contact_memory_evidence": float(contact_memory_evidence),
        "receptive_contact_memory_gap": float(receptive_contact_memory_gap),
        "receptive_contact_offer_pressure": float(receptive_contact_offer_pressure),
        "receptive_contact_maturity": float(receptive_contact_maturity),
        "receptive_contact_immaturity_pressure": float(receptive_contact_immaturity_pressure),
        "receptive_contact_restraint": float(receptive_contact_restraint),
        "receptive_exploration_bearing": float(receptive_exploration_bearing),
        "contact_continuation_support": float(contact_continuation_support) if "contact_continuation_support" in locals() else 0.0,
        "contact_continuation_pressure": float(contact_continuation_pressure) if "contact_continuation_pressure" in locals() else 0.0,
    }

    area_support_coupling = _clip01(0.06 + (felt_area_coupling * 0.58) + (mcm_reflective_bearing * 0.20) + (contact_context_bearing * 0.16))
    coupled_area_readiness = area_readiness * area_support_coupling
    coupled_area_bearing = area_bearing * area_support_coupling
    coupled_contact_fit = contact_fit * area_support_coupling

    inner_support = _clip01(
        (inner_alignment * 0.16)
        + (regulated_courage * 0.12)
        + (action_clearance * 0.12)
        + (contact_carrying * 0.10)
        + (contact_maturity * 0.10)
        + (structure_quality * 0.10)
        + (context_confidence * 0.07)
        + (target_expectation * 0.07)
        + (reflection_maturity * 0.06)
        + (form_action_trust * 0.05)
        + (form_contact_maturity * 0.05)
        + (form_contact_usefulness * 0.06)
        + (receptive_contact_bearing * 0.10)
        + (receptive_exploration_bearing * 0.10)
        + (coupled_area_readiness * 0.05)
        + (coupled_area_bearing * 0.05)
        + (coupled_contact_fit * 0.05)
        + (real_area_contact_bearing * 0.10)
        + (felt_area_coupling * 0.04)
        + (conscious_action_bearing * 0.09)
        + (raw_area_contact_bearing * contact_context_bearing * 0.04)
    )
    inner_no = _clip01(
        (action_inhibition * 0.14)
        + (field_observation_need * 0.13)
        + (pre_action_reorganization * 0.13)
        + (contact_overcoupling * 0.11)
        + (contact_reality_check * 0.10)
        + (nervous_reflection * 0.10)
        + (motor_restraint * 0.08)
        + (receptive_contact_restraint * 0.12)
        + (receptive_contact_immaturity_pressure * 0.10)
        + (max(0.0, 0.34 - inner_alignment) * 0.16)
        + (max(0.0, 0.30 - regulated_courage) * 0.12)
        + (max(0.0, 0.26 - target_expectation) * 0.08)
        + (thought_motor_pressure * 0.16)
        + (untrusted_contact_pressure * 0.18)
        + (uncoupled_area_contact_pressure * 0.30)
        + (form_contact_burden * 0.14)
        + (raw_area_contact_bearing * max(0.0, 0.30 - sensory_area_coupling) * 0.12)
        + (max(0.0, 0.26 - conscious_action_bearing) * 0.30)
        + (max(0.0, 0.14 - real_area_contact_bearing) * 0.08)
        + (form_contact_burden * max(0.0, 0.24 - conscious_action_bearing) * 0.22)
        - (felt_area_coupling * 0.04)
        - (mcm_reflective_bearing * 0.05)
        - (form_contact_usefulness * 0.04)
        - (receptive_exploration_bearing * 0.08)
    )
    contact_continuation_support = _clip01(
        (
            (real_area_contact_bearing * 0.22)
            + (felt_area_coupling * 0.18)
            + (contact_context_bearing * 0.14)
            + (conscious_action_bearing * 0.12)
            + (mcm_reflective_bearing * 0.08)
        )
        if has_real_area_contact
        else 0.0
    )
    contact_continuation_pressure = _clip01(
        (
            (uncoupled_area_contact_pressure * 0.22)
            + (untrusted_contact_pressure * 0.18)
            + (receptive_contact_immaturity_pressure * 0.16)
            + (receptive_contact_restraint * 0.12)
            + (mcm_reflective_pressure * 0.12)
            + (contact_overcoupling * 0.12)
        )
        if has_real_area_contact
        else 0.0
    )
    inner_support = _clip01(inner_support + (contact_continuation_support * 0.18))
    inner_no = _clip01(inner_no + (contact_continuation_pressure * 0.10) - (contact_continuation_support * 0.16))
    consent = _clip01((inner_support * 0.72) + (max(0.0, inner_support - inner_no) * 0.38))
    thought_consent_trace["contact_continuation_support"] = float(contact_continuation_support)
    thought_consent_trace["contact_continuation_pressure"] = float(contact_continuation_pressure)

    phase_hold_pressure = 1.0 if pre_action_phase in ("hold", "act_watch") else 0.0
    phase_replan_pressure = 1.0 if pre_action_phase == "replan" else 0.0
    impulse_processing_pressure = 1.0 if impulse_only else 0.0
    open_hypothesis_pressure = 0.0
    ordinary_structure_pressure = 1.0 if emergent_structure_state == "ordinary_structure_contact" and not carried_hypothesis_memory else 0.0
    thought_confirmation_gap = _clip01(max(0.0, thought_confirmation_bearing - thought_rejection_pressure))
    thought_rejection_gap = _clip01(max(0.0, thought_rejection_pressure - thought_confirmation_bearing))
    reality_contact_gap = 0.0
    contact_bearing_gap = _clip01(max(0.0, real_area_contact_bearing - uncoupled_area_contact_pressure))
    missing_bearing_pressure = _clip01(
        (1.0 - max(area_bearing, area_readiness, contact_carrying, target_expectation)) * ordinary_structure_pressure
    )
    weak_seed_pressure = 0.0

    act_pressure = _clip01(
        (consent * 0.32)
        + (inner_support * 0.24)
        + (contact_continuation_support * 0.14)
        + (contact_bearing_gap * 0.08)
        + (receptive_contact_bearing * 0.06)
        + (receptive_exploration_bearing * 0.08)
        + (mcm_reflective_bearing * 0.06)
        + (receptive_contact_maturity * 0.04)
        - (inner_no * 0.20)
        - (receptive_contact_restraint * 0.08)
        - (impulse_processing_pressure * 0.18)
    )
    observe_pressure = _clip01(
        ((1.0 - consent) * 0.18)
        + (field_observation_need * 0.16)
        + (inner_no * 0.12)
        + (contact_continuation_pressure * 0.12)
        + (uncoupled_area_contact_pressure * 0.10)
        + (receptive_contact_immaturity_pressure * 0.12)
        + (impulse_processing_pressure * 0.16)
        + (missing_bearing_pressure * 0.12)
        + (weak_seed_pressure * 0.10)
    )
    replan_pressure = _clip01(
        (pre_action_reorganization * 0.22)
        + (phase_replan_pressure * 0.12)
        + (weak_seed_pressure * 0.18)
        + (reality_contact_gap * open_hypothesis_pressure * 0.16)
        + (mcm_reflective_pressure * 0.08)
    )
    hold_pressure = _clip01(
        (action_inhibition * 0.18)
        + (phase_hold_pressure * 0.14)
        + (inner_no * 0.16)
        + (mcm_reflective_coupling_load * 0.10)
        + (mcm_reflective_pressure * 0.08)
        + (receptive_contact_restraint * 0.10)
        + (contact_overcoupling * 0.08)
        + (nervous_reflection * 0.06)
    )
    tendency_pressures = {
        "observe": observe_pressure,
        "replan": replan_pressure,
        "hold": hold_pressure,
        "act": act_pressure,
    }
    tendency = max(tendency_pressures, key=tendency_pressures.get)
    reason_by_tendency = {
        "act": "inner_state_carries_action",
        "observe": "inner_state_prefers_observation",
        "replan": "inner_state_reorganizes_action_thesis",
        "hold": "inner_state_holds_motor_action",
    }
    allowed = tendency == "act"

    return {
        "allowed": bool(allowed),
        "would_have_declined": not bool(allowed),
        "non_economic_gate_policy": "field_modulation_only",
        "tendency": tendency,
        "reason": reason_by_tendency.get(tendency, "inner_state_field_selection"),
        "inner_action_consent": float(consent),
        "inner_action_support": float(inner_support),
        "inner_action_no": float(inner_no),
        "act_pressure": float(act_pressure),
        "observe_pressure": float(observe_pressure),
        "replan_pressure": float(replan_pressure),
        "hold_pressure": float(hold_pressure),
        "weak_seed_pressure": float(weak_seed_pressure),
        "missing_bearing_pressure": float(missing_bearing_pressure),
        **thought_consent_trace,
        "contact_continuation_support": float(contact_continuation_support),
        "contact_continuation_pressure": float(contact_continuation_pressure),
        "dominant_hypothesis_reality_support": float(dominant_hypothesis_reality_support),
        "dominant_hypothesis_action_readiness": float(dominant_hypothesis_reality_support),
        "hypothesis_role": "thought_reality_probe",
        "impulse_only": bool(impulse_only),
    }


def _with_inner_action_consent(decision, consent_state):
    result = dict(decision or {})
    meta = dict(result.get("meta_regulation_state", {}) or {})
    meta.update(
        {
            "inner_action_consent": float(consent_state.get("inner_action_consent", 0.0) or 0.0),
            "inner_action_support": float(consent_state.get("inner_action_support", 0.0) or 0.0),
            "inner_action_no": float(consent_state.get("inner_action_no", 0.0) or 0.0),
            "strategy_confirmation": float(consent_state.get("strategy_confirmation", 0.0) or 0.0),
            "strategy_rejection": float(consent_state.get("strategy_rejection", 0.0) or 0.0),
            "strategy_trust_bearing": float(consent_state.get("strategy_trust_bearing", 0.0) or 0.0),
            "strategy_context_bearing": float(consent_state.get("strategy_context_bearing", 0.0) or 0.0),
            "raw_strategy_contradiction_pressure": float(consent_state.get("raw_strategy_contradiction_pressure", 0.0) or 0.0),
            "strategy_contradiction_pressure": float(consent_state.get("strategy_contradiction_pressure", 0.0) or 0.0),
            "strategy_alias_state": str(consent_state.get("strategy_alias_state", "deprecated_receptive_coupling_active") or "deprecated_receptive_coupling_active"),
            "thought_confirmation_bearing": _num_any(consent_state, "thought_confirmation_bearing", "strategy_confirmation"),
            "thought_rejection_pressure": _num_any(consent_state, "thought_rejection_pressure", "strategy_rejection"),
            "thought_trust_bearing": _num_any(consent_state, "thought_trust_bearing", "strategy_trust_bearing"),
            "contact_context_bearing": _num_any(consent_state, "contact_context_bearing", "strategy_context_bearing"),
            "raw_thought_contradiction_pressure": _num_any(consent_state, "raw_thought_contradiction_pressure", "raw_strategy_contradiction_pressure"),
            "thought_contradiction_pressure": _num_any(consent_state, "thought_contradiction_pressure", "strategy_contradiction_pressure"),
            "open_hypothesis_reality_bearing": _num_any(consent_state, "open_hypothesis_reality_bearing", "open_hypothesis_reality_permission", "open_hypothesis_action_permission"),
            "open_hypothesis_reality_fit": _num_any(consent_state, "open_hypothesis_reality_fit", "open_hypothesis_reality_bearing", "open_hypothesis_reality_permission"),
            "open_hypothesis_reality_probe": _num_any(consent_state, "open_hypothesis_reality_probe", "open_hypothesis_reality_bearing", "open_hypothesis_reality_permission"),
            "open_hypothesis_reality_permission": _num_any(consent_state, "open_hypothesis_reality_permission", "open_hypothesis_action_permission"),
            "possibility_contact_bearing": _num_any(consent_state, "possibility_contact_bearing", "possibility_action_support"),
            "dominant_hypothesis_reality_bearing": _num_any(consent_state, "dominant_hypothesis_reality_bearing", "dominant_hypothesis_action_readiness"),
            "dominant_hypothesis_reality_support": _num_any(consent_state, "dominant_hypothesis_reality_support", "dominant_hypothesis_reality_bearing", "dominant_hypothesis_action_readiness"),
            "current_hypothesis_reality_bearing": _num_any(consent_state, "current_hypothesis_reality_bearing", "current_hypothesis_action_support"),
            "current_hypothesis_reality_support": _num_any(consent_state, "current_hypothesis_reality_support", "current_hypothesis_reality_bearing", "current_hypothesis_action_support"),
            "hypothesis_role": str(consent_state.get("hypothesis_role", "thought_reality_probe") or "thought_reality_probe"),
            "thought_contact_consent": _num_any(consent_state, "thought_contact_consent"),
            "thought_area_coupling": _num_any(consent_state, "thought_area_coupling"),
            "felt_area_coupling": _num_any(consent_state, "felt_area_coupling"),
            "sensory_area_coupling": _num_any(consent_state, "sensory_area_coupling"),
            "thought_reality_coupled_bearing": _num_any(consent_state, "thought_reality_coupled_bearing"),
            "receptive_contact_bearing": _num_any(consent_state, "receptive_contact_bearing"),
            "analytic_action_bearing": _num_any(consent_state, "analytic_action_bearing"),
            "intuitive_action_bearing": _num_any(consent_state, "intuitive_action_bearing"),
            "conscious_action_bearing": _num_any(consent_state, "conscious_action_bearing"),
            "market_hearing_state": dict(consent_state.get("market_hearing_state", meta.get("market_hearing_state", {})) or {}),
            "market_loudness": _num_any(consent_state, "market_loudness"),
            "market_frequency_hz": _num_any(consent_state, "market_frequency_hz"),
            "market_hearing_compression": _num_any(consent_state, "market_hearing_compression"),
            "energy_coherence_bearing": _num_any(consent_state, "energy_coherence_bearing"),
            "untrusted_contact_pressure": _num_any(consent_state, "untrusted_contact_pressure"),
            "uncoupled_area_contact_pressure": _num_any(consent_state, "uncoupled_area_contact_pressure"),
            "raw_area_contact_bearing": _num_any(consent_state, "raw_area_contact_bearing"),
            "real_area_contact_bearing": _num_any(consent_state, "real_area_contact_bearing"),
            "contact_memory_evidence": _num_any(consent_state, "contact_memory_evidence"),
            "receptive_contact_memory_gap": _num_any(consent_state, "receptive_contact_memory_gap"),
            "receptive_contact_offer_pressure": _num_any(consent_state, "receptive_contact_offer_pressure"),
            "receptive_contact_maturity": _num_any(consent_state, "receptive_contact_maturity"),
            "receptive_contact_immaturity_pressure": _num_any(consent_state, "receptive_contact_immaturity_pressure"),
            "receptive_contact_restraint": _num_any(consent_state, "receptive_contact_restraint"),
            "receptive_exploration_bearing": _num_any(consent_state, "receptive_exploration_bearing"),
            "act_pressure": _num_any(consent_state, "act_pressure"),
            "observe_pressure": _num_any(consent_state, "observe_pressure"),
            "replan_pressure": _num_any(consent_state, "replan_pressure"),
            "hold_pressure": _num_any(consent_state, "hold_pressure"),
            "weak_seed_pressure": _num_any(consent_state, "weak_seed_pressure"),
            "missing_bearing_pressure": _num_any(consent_state, "missing_bearing_pressure"),
            "dominant_hypothesis_action_readiness": float(consent_state.get("dominant_hypothesis_action_readiness", meta.get("dominant_hypothesis_action_readiness", 0.0)) or 0.0),
            "inner_action_consent_state": str(consent_state.get("reason", "-") or "-"),
            "inner_action_would_have_declined": bool(consent_state.get("would_have_declined", False)),
            "non_economic_gate_policy": str(consent_state.get("non_economic_gate_policy", "field_modulation_only") or "field_modulation_only"),
        }
    )
    result["meta_regulation_state"] = meta
    result["inner_action_consent"] = float(consent_state.get("inner_action_consent", 0.0) or 0.0)
    result["inner_action_support"] = float(consent_state.get("inner_action_support", 0.0) or 0.0)
    result["inner_action_no"] = float(consent_state.get("inner_action_no", 0.0) or 0.0)
    result["strategy_confirmation"] = float(consent_state.get("strategy_confirmation", 0.0) or 0.0)
    result["strategy_rejection"] = float(consent_state.get("strategy_rejection", 0.0) or 0.0)
    result["strategy_trust_bearing"] = float(consent_state.get("strategy_trust_bearing", 0.0) or 0.0)
    result["strategy_context_bearing"] = float(consent_state.get("strategy_context_bearing", 0.0) or 0.0)
    result["raw_strategy_contradiction_pressure"] = float(consent_state.get("raw_strategy_contradiction_pressure", 0.0) or 0.0)
    result["strategy_contradiction_pressure"] = float(consent_state.get("strategy_contradiction_pressure", 0.0) or 0.0)
    result["strategy_alias_state"] = str(consent_state.get("strategy_alias_state", "deprecated_receptive_coupling_active") or "deprecated_receptive_coupling_active")
    result["thought_confirmation_bearing"] = _num_any(consent_state, "thought_confirmation_bearing", "strategy_confirmation")
    result["thought_rejection_pressure"] = _num_any(consent_state, "thought_rejection_pressure", "strategy_rejection")
    result["thought_trust_bearing"] = _num_any(consent_state, "thought_trust_bearing", "strategy_trust_bearing")
    result["contact_context_bearing"] = _num_any(consent_state, "contact_context_bearing", "strategy_context_bearing")
    result["raw_thought_contradiction_pressure"] = _num_any(consent_state, "raw_thought_contradiction_pressure", "raw_strategy_contradiction_pressure")
    result["thought_contradiction_pressure"] = _num_any(consent_state, "thought_contradiction_pressure", "strategy_contradiction_pressure")
    result["open_hypothesis_reality_bearing"] = _num_any(consent_state, "open_hypothesis_reality_bearing", "open_hypothesis_reality_permission", "open_hypothesis_action_permission")
    result["open_hypothesis_reality_fit"] = _num_any(consent_state, "open_hypothesis_reality_fit", "open_hypothesis_reality_bearing", "open_hypothesis_reality_permission")
    result["open_hypothesis_reality_probe"] = _num_any(consent_state, "open_hypothesis_reality_probe", "open_hypothesis_reality_bearing", "open_hypothesis_reality_permission")
    result["open_hypothesis_reality_permission"] = _num_any(consent_state, "open_hypothesis_reality_permission", "open_hypothesis_action_permission")
    result["possibility_contact_bearing"] = _num_any(consent_state, "possibility_contact_bearing", "possibility_action_support")
    result["dominant_hypothesis_reality_bearing"] = _num_any(consent_state, "dominant_hypothesis_reality_bearing", "dominant_hypothesis_action_readiness")
    result["dominant_hypothesis_reality_support"] = _num_any(consent_state, "dominant_hypothesis_reality_support", "dominant_hypothesis_reality_bearing", "dominant_hypothesis_action_readiness")
    result["current_hypothesis_reality_bearing"] = _num_any(consent_state, "current_hypothesis_reality_bearing", "current_hypothesis_action_support")
    result["current_hypothesis_reality_support"] = _num_any(consent_state, "current_hypothesis_reality_support", "current_hypothesis_reality_bearing", "current_hypothesis_action_support")
    result["hypothesis_role"] = str(consent_state.get("hypothesis_role", "thought_reality_probe") or "thought_reality_probe")
    result["thought_contact_consent"] = _num_any(consent_state, "thought_contact_consent")
    result["thought_area_coupling"] = _num_any(consent_state, "thought_area_coupling")
    result["felt_area_coupling"] = _num_any(consent_state, "felt_area_coupling")
    result["sensory_area_coupling"] = _num_any(consent_state, "sensory_area_coupling")
    result["thought_reality_coupled_bearing"] = _num_any(consent_state, "thought_reality_coupled_bearing")
    result["receptive_contact_bearing"] = _num_any(consent_state, "receptive_contact_bearing")
    result["analytic_action_bearing"] = _num_any(consent_state, "analytic_action_bearing")
    result["intuitive_action_bearing"] = _num_any(consent_state, "intuitive_action_bearing")
    result["conscious_action_bearing"] = _num_any(consent_state, "conscious_action_bearing")
    result["market_hearing_state"] = dict(consent_state.get("market_hearing_state", meta.get("market_hearing_state", result.get("market_hearing_state", {}))) or {})
    result["market_loudness"] = _num_any(consent_state, "market_loudness")
    result["market_frequency_hz"] = _num_any(consent_state, "market_frequency_hz")
    result["market_hearing_compression"] = _num_any(consent_state, "market_hearing_compression")
    result["energy_coherence_bearing"] = _num_any(consent_state, "energy_coherence_bearing")
    result["untrusted_contact_pressure"] = _num_any(consent_state, "untrusted_contact_pressure")
    result["uncoupled_area_contact_pressure"] = _num_any(consent_state, "uncoupled_area_contact_pressure")
    result["raw_area_contact_bearing"] = _num_any(consent_state, "raw_area_contact_bearing")
    result["real_area_contact_bearing"] = _num_any(consent_state, "real_area_contact_bearing")
    result["receptive_contact_offer_pressure"] = _num_any(consent_state, "receptive_contact_offer_pressure")
    result["receptive_contact_maturity"] = _num_any(consent_state, "receptive_contact_maturity")
    result["receptive_contact_immaturity_pressure"] = _num_any(consent_state, "receptive_contact_immaturity_pressure")
    result["receptive_contact_restraint"] = _num_any(consent_state, "receptive_contact_restraint")
    result["act_pressure"] = _num_any(consent_state, "act_pressure")
    result["observe_pressure"] = _num_any(consent_state, "observe_pressure")
    result["replan_pressure"] = _num_any(consent_state, "replan_pressure")
    result["hold_pressure"] = _num_any(consent_state, "hold_pressure")
    result["weak_seed_pressure"] = _num_any(consent_state, "weak_seed_pressure")
    result["missing_bearing_pressure"] = _num_any(consent_state, "missing_bearing_pressure")
    result["dominant_hypothesis_action_readiness"] = float(consent_state.get("dominant_hypothesis_action_readiness", meta.get("dominant_hypothesis_action_readiness", 0.0)) or 0.0)
    result["inner_action_consent_state"] = str(consent_state.get("reason", "-") or "-")
    result["inner_action_would_have_declined"] = bool(consent_state.get("would_have_declined", False))
    result["non_economic_gate_policy"] = str(consent_state.get("non_economic_gate_policy", "field_modulation_only") or "field_modulation_only")
    return result


def _as_inner_non_action(decision, consent_state):
    result = _with_inner_action_consent(decision, consent_state)
    proposed = str(result.get("decision", "WAIT") or "WAIT").upper().strip()
    result["decision_tendency"] = str(consent_state.get("tendency", "observe") or "observe")
    result["proposed_decision"] = proposed if proposed in ("LONG", "SHORT") else "WAIT"
    result["decision"] = "WAIT"
    result["rejection_reason"] = str(consent_state.get("reason", "inner_state_declines_motor_action") or "inner_state_declines_motor_action")
    result["action_intent_state"] = {
        "intent_state": "inner_processing",
        "intent_direction": str(result.get("proposed_decision", "WAIT") or "WAIT"),
        "intent_strength": float(consent_state.get("inner_action_support", 0.0) or 0.0),
        "intent_ready": False,
    }
    result["execution_state"] = {
        "execution_phase": "inner_processing",
        "execution_ready": False,
        "execution_blocked": False,
        "non_action_reason_type": "inner_processing",
    }
    return result


# --------------------------------------------------
def evaluate_entry_decision(bot, window, candle_state):

    tendency_state = build_runtime_decision_tendency(
        window=window,
        candle_state=candle_state,
        bot=bot,
    )

    if tendency_state is None:
        return None

    decision_tendency = str(tendency_state.get("decision_tendency", "hold") or "hold").strip().lower()
    meta_state = dict(tendency_state.get("meta_regulation_state", {}) or {})
    explicit_allow_plan = (
        tendency_state.get("allow_plan")
        if "allow_plan" in tendency_state
        else meta_state.get("allow_plan") if "allow_plan" in meta_state else None
    )

    if decision_tendency == "act" and explicit_allow_plan is False:
        meta_state["former_allow_plan_false"] = True
        meta_state["non_economic_gate_policy"] = "field_modulation_only"
        tendency_state["meta_regulation_state"] = dict(meta_state)

    if decision_tendency != "act":
        return {
            "decision_tendency": str(decision_tendency or "hold"),
            "action_intent_state": {
                "intent_state": "non_action",
                "intent_direction": str(tendency_state.get("proposed_decision", "WAIT") or "WAIT"),
                "intent_strength": float(tendency_state.get("focus", {}).get("focus_strength", 0.0) or 0.0),
                "intent_ready": False,
            },
            "execution_state": {
                "execution_phase": "idle",
                "execution_ready": False,
                "execution_blocked": False,
                "non_action_reason_type": "runtime_non_action_state",
            },
            "proposed_decision": str(tendency_state.get("proposed_decision", "WAIT") or "WAIT"),
            "self_state": str(tendency_state.get("self_state", "stable") or "stable"),
            "attractor": str(tendency_state.get("attractor", "neutral") or "neutral"),
            "focus": dict(tendency_state.get("focus", {}) or {}),
            "world_state": dict(tendency_state.get("world_state", {}) or {}),
            "structure_perception_state": dict(tendency_state.get("structure_perception_state", {}) or {}),
            "outer_visual_perception_state": dict(tendency_state.get("outer_visual_perception_state", {}) or {}),
            "inner_field_perception_state": dict(tendency_state.get("inner_field_perception_state", {}) or {}),
            "perception_state": dict(tendency_state.get("perception_state", {}) or {}),
            "processing_state": dict(tendency_state.get("processing_state", {}) or {}),
            "felt_state": dict(tendency_state.get("felt_state", {}) or {}),
            "thought_state": dict(tendency_state.get("thought_state", {}) or {}),
            "meta_regulation_state": dict(tendency_state.get("meta_regulation_state", {}) or {}),
            "expectation_state": dict(tendency_state.get("expectation_state", {}) or {}),
            "state_signature": dict(tendency_state.get("state_signature", {}) or {}),
            "signature_bias": float(tendency_state.get("signature_bias", 0.0) or 0.0),
            "signature_block": bool(tendency_state.get("signature_block", False)),
            "signature_quality": float(tendency_state.get("signature_quality", 0.0) or 0.0),
            "signature_distance": float(tendency_state.get("signature_distance", 0.0) or 0.0),
            "context_cluster_id": str(tendency_state.get("context_cluster_id", "-") or "-"),
            "context_cluster_bias": float(tendency_state.get("context_cluster_bias", 0.0) or 0.0),
            "context_cluster_quality": float(tendency_state.get("context_cluster_quality", 0.0) or 0.0),
            "context_cluster_distance": float(tendency_state.get("context_cluster_distance", 0.0) or 0.0),
            "context_cluster_block": bool(tendency_state.get("context_cluster_block", False)),
            "inhibition_level": float(tendency_state.get("inhibition_level", 0.0) or 0.0),
            "habituation_level": float(tendency_state.get("habituation_level", 0.0) or 0.0),
            "competition_bias": float(tendency_state.get("competition_bias", 0.0) or 0.0),
            "observation_mode": bool(tendency_state.get("observation_mode", False)),
            "long_score": float(tendency_state.get("long_score", 0.0) or 0.0),
            "short_score": float(tendency_state.get("short_score", 0.0) or 0.0),
            "field_density": float(tendency_state.get("field_density", 0.0) or 0.0),
            "field_stability": float(tendency_state.get("field_stability", 0.0) or 0.0),
            "regulatory_load": float(tendency_state.get("regulatory_load", 0.0) or 0.0),
            "action_capacity": float(tendency_state.get("action_capacity", 0.0) or 0.0),
            "recovery_need": float(tendency_state.get("recovery_need", 0.0) or 0.0),
            "survival_pressure": float(tendency_state.get("survival_pressure", 0.0) or 0.0),
            "felt_bearing_score": float(tendency_state.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(tendency_state.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "rejection_reason": str(tendency_state.get("rejection_reason", "runtime_non_action") or "runtime_non_action"),
        }

    decision = decide_mcm_brain_entry(
        window=window,
        candle_state=candle_state,
        bot=bot,
    )
    
    if decision is None:
        _entry_bridge_debug(
            "MCM_ENTRY_BRIDGE | state=decision_plan_missing "
            f"tendency={decision_tendency} proposed={str(tendency_state.get('proposed_decision', 'WAIT') or 'WAIT')} "
            f"allow_plan={bool(explicit_allow_plan)} "
            f"reason={str(tendency_state.get('rejection_reason', meta_state.get('rejection_reason', '-')) or '-')}"
        )
        return {
            "decision_tendency": "replan",
            "proposed_decision": str(tendency_state.get("proposed_decision", "WAIT") or "WAIT"),
            "self_state": str(tendency_state.get("self_state", "stable") or "stable"),
            "attractor": str(tendency_state.get("attractor", "neutral") or "neutral"),
            "focus": dict(tendency_state.get("focus", {}) or {}),
            "world_state": dict(tendency_state.get("world_state", {}) or {}),
            "structure_perception_state": dict(tendency_state.get("structure_perception_state", {}) or {}),
            "outer_visual_perception_state": dict(tendency_state.get("outer_visual_perception_state", {}) or {}),
            "inner_field_perception_state": dict(tendency_state.get("inner_field_perception_state", {}) or {}),
            "perception_state": dict(tendency_state.get("perception_state", {}) or {}),
            "processing_state": dict(tendency_state.get("processing_state", {}) or {}),
            "felt_state": dict(tendency_state.get("felt_state", {}) or {}),
            "thought_state": dict(tendency_state.get("thought_state", {}) or {}),
            "meta_regulation_state": dict(tendency_state.get("meta_regulation_state", {}) or {}),
            "expectation_state": dict(tendency_state.get("expectation_state", {}) or {}),
            "state_signature": dict(tendency_state.get("state_signature", {}) or {}),
            "signature_bias": float(tendency_state.get("signature_bias", 0.0) or 0.0),
            "signature_block": bool(tendency_state.get("signature_block", False)),
            "signature_quality": float(tendency_state.get("signature_quality", 0.0) or 0.0),
            "signature_distance": float(tendency_state.get("signature_distance", 0.0) or 0.0),
            "context_cluster_id": str(tendency_state.get("context_cluster_id", "-") or "-"),
            "context_cluster_bias": float(tendency_state.get("context_cluster_bias", 0.0) or 0.0),
            "context_cluster_quality": float(tendency_state.get("context_cluster_quality", 0.0) or 0.0),
            "context_cluster_distance": float(tendency_state.get("context_cluster_distance", 0.0) or 0.0),
            "context_cluster_block": bool(tendency_state.get("context_cluster_block", False)),
            "inhibition_level": float(tendency_state.get("inhibition_level", 0.0) or 0.0),
            "habituation_level": float(tendency_state.get("habituation_level", 0.0) or 0.0),
            "competition_bias": float(tendency_state.get("competition_bias", 0.0) or 0.0),
            "observation_mode": bool(tendency_state.get("observation_mode", False)),
            "long_score": float(tendency_state.get("long_score", 0.0) or 0.0),
            "short_score": float(tendency_state.get("short_score", 0.0) or 0.0),
            "field_density": float(tendency_state.get("field_density", 0.0) or 0.0),
            "field_stability": float(tendency_state.get("field_stability", 0.0) or 0.0),
            "regulatory_load": float(tendency_state.get("regulatory_load", 0.0) or 0.0),
            "action_capacity": float(tendency_state.get("action_capacity", 0.0) or 0.0),
            "recovery_need": float(tendency_state.get("recovery_need", 0.0) or 0.0),
            "survival_pressure": float(tendency_state.get("survival_pressure", 0.0) or 0.0),
            "felt_bearing_score": float(tendency_state.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(tendency_state.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "rejection_reason": "decision_plan_missing",
        }

    meta_regulation_state = dict(decision.get("meta_regulation_state", {}) or {})
    side_probe = str(decision.get("decision", "WAIT") or "WAIT").upper().strip()
    rejection_reason = str(
        decision.get("rejection_reason", meta_regulation_state.get("rejection_reason", "")) or ""
    ).strip()
    final_decision_tendency = str(decision.get("decision_tendency", decision_tendency) or decision_tendency).strip().lower()
    if side_probe not in ("LONG", "SHORT") and final_decision_tendency == "act":
        if rejection_reason == "hypothesis_requires_reality_observation":
            final_decision_tendency = "observe"
        else:
            final_decision_tendency = "hold"
    if final_decision_tendency != "act":
        focus_state = dict(decision.get("focus", {}) or {})
        decision["decision_tendency"] = str(final_decision_tendency or "hold")
        decision["action_intent_state"] = {
            "intent_state": "non_action",
            "intent_direction": str(decision.get("proposed_decision", decision.get("decision", "WAIT")) or "WAIT"),
            "intent_strength": float(focus_state.get("focus_strength", 0.0) or 0.0),
            "intent_ready": False,
        }
        decision["execution_state"] = {
            "execution_phase": "idle",
            "execution_ready": False,
            "execution_blocked": False,
            "non_action_reason_type": "runtime_non_action_state",
        }
        return decision

    focus_state = dict(decision.get("focus", {}) or {})
    decision["action_intent_state"] = {
        "intent_state": "prepare_action",
        "intent_direction": str(decision.get("decision", "WAIT") or "WAIT"),
        "intent_strength": float(focus_state.get("focus_strength", 0.0) or 0.0),
        "intent_ready": True,
    }
    decision["execution_state"] = {
        "execution_phase": "planned",
        "execution_ready": True,
        "execution_blocked": False,
    }

    side = str(decision.get("decision", "")).upper().strip()
    entry_price = float(decision.get("entry_price", 0.0) or 0.0)
    sl_price = float(decision.get("sl_price", 0.0) or 0.0)
    tp_price = float(decision.get("tp_price", 0.0) or 0.0)
    rr_value = float(decision.get("rr_value", 0.0) or 0.0)

    if side not in ("LONG", "SHORT"):
        _entry_bridge_debug(
            "MCM_ENTRY_BRIDGE | state=invalid_trade_direction "
            f"side={side} tendency={decision_tendency} "
            f"allow_plan={bool(explicit_allow_plan)} "
            f"reason={str(meta_regulation_state.get('rejection_reason', '-') or '-')}"
        )
        return None

    if entry_price <= 0.0 or sl_price <= 0.0 or tp_price <= 0.0:
        _entry_bridge_debug(
            "MCM_ENTRY_BRIDGE | state=invalid_trade_geometry "
            f"side={side} entry={entry_price:.8f} sl={sl_price:.8f} tp={tp_price:.8f} "
            f"allow_plan={bool(explicit_allow_plan)} "
            f"entry_mode={str(decision.get('entry_mode', 'no_mature_entry_thesis') or 'no_mature_entry_thesis')} "
            f"entry_contact_state={str(decision.get('entry_contact_state', decision.get('entry_choice_state', 'no_entry_choice')) or 'no_entry_choice')}"
        )
        return None

    risk = abs(entry_price - sl_price)
    if risk <= 0.0:
        _entry_bridge_debug(
            "MCM_ENTRY_BRIDGE | state=invalid_risk_geometry "
            f"side={side} entry={entry_price:.8f} sl={sl_price:.8f} tp={tp_price:.8f} "
            f"allow_plan={bool(explicit_allow_plan)}"
        )
        return None

    if rr_value <= 0.0:
        rr_value = abs(tp_price - entry_price) / risk

    focus = dict(decision.get("focus", {}) or {})
    filtered_vision = dict(decision.get("filtered_vision", {}) or {})
    raw_vision = dict(decision.get("vision", {}) or {})
    state_signature = dict(decision.get("state_signature", {}) or {})
    perception_state = dict(decision.get("perception_state", {}) or {})
    felt_state = dict(decision.get("felt_state", {}) or {})
    thought_state = dict(decision.get("thought_state", {}) or {})
    expectation_state = dict(decision.get("expectation_state", {}) or {})

    if DEBUG:
        dbr_debug(
            f"MCM_ENTRY | side={side} entry={entry_price:.6f} sl={sl_price:.6f} tp={tp_price:.6f} rr={rr_value:.4f} "
            f"self_state={decision.get('self_state', '-')} attractor={decision.get('attractor', '-')} "
            f"memory_center={float(decision.get('memory_center', 0.0) or 0.0):.4f} "
            f"memory_strength={int(decision.get('memory_strength', 0) or 0)} "
            f"focus_direction={float(focus.get('focus_direction', 0.0) or 0.0):.4f} "
            f"focus_strength={float(focus.get('focus_strength', 0.0) or 0.0):.4f} "
            f"focus_confidence={float(focus.get('focus_confidence', 0.0) or 0.0):.4f} "
            f"target_lock={float(focus.get('target_lock', 0.0) or 0.0):.4f} "
            f"noise_damp={float(focus.get('noise_damp', 0.0) or 0.0):.4f} "
            f"signal_relevance={float(focus.get('signal_relevance', 0.0) or 0.0):.4f} "
            f"entry_expectation={float(expectation_state.get('entry_expectation', 0.0) or 0.0):.4f} "
            f"target_expectation={float(expectation_state.get('target_expectation', 0.0) or 0.0):.4f} "
            f"approach_pressure={float(expectation_state.get('approach_pressure', 0.0) or 0.0):.4f} "
            f"pressure_release={float(expectation_state.get('pressure_release', 0.0) or 0.0):.4f} "
            f"experience_regulation={float(expectation_state.get('experience_regulation', 0.0) or 0.0):.4f} "
            f"reflection_maturity={float(expectation_state.get('reflection_maturity', 0.0) or 0.0):.4f} "
            f"signature_key={str(state_signature.get('signature_key', '-'))} "
            f"signature_bias={float(decision.get('signature_bias', 0.0) or 0.0):.4f} "
            f"signature_block={bool(decision.get('signature_block', False))} "
            f"signature_quality={float(decision.get('signature_quality', 0.0) or 0.0):.4f} "
            f"signature_distance={float(decision.get('signature_distance', 0.0) or 0.0):.4f} "
            f"context_cluster_id={str(decision.get('context_cluster_id', '-'))} "
            f"context_cluster_bias={float(decision.get('context_cluster_bias', 0.0) or 0.0):.4f} "
            f"context_cluster_quality={float(decision.get('context_cluster_quality', 0.0) or 0.0):.4f} "
            f"context_cluster_distance={float(decision.get('context_cluster_distance', 0.0) or 0.0):.4f} "
            f"context_cluster_block={bool(decision.get('context_cluster_block', False))} "
            f"inhibition_level={float(decision.get('inhibition_level', 0.0) or 0.0):.4f} "
            f"habituation_level={float(decision.get('habituation_level', 0.0) or 0.0):.4f} "
            f"competition_bias={float(decision.get('competition_bias', 0.0) or 0.0):.4f} "
            f"observation_mode={bool(decision.get('observation_mode', False))} "
            f"entry_mode={str(decision.get('entry_mode', 'no_mature_entry_thesis') or 'no_mature_entry_thesis')} "
            f"entry_contact_state={str(decision.get('entry_contact_state', decision.get('entry_choice_state', 'no_entry_choice')) or 'no_entry_choice')} "
            f"entry_choice_sync={str(decision.get('entry_choice_sync', '-') or '-')} "
            f"area_contact_intention={float(decision.get('area_contact_intention', decision.get('area_motor_intention', 0.0)) or 0.0):.4f} "
            f"entry_contact_bearing={float(decision.get('entry_contact_bearing', decision.get('entry_choice_bearing', 0.0)) or 0.0):.4f} "
            f"area_contact_readiness={float(decision.get('area_contact_readiness', decision.get('area_direct_readiness', 0.0)) or 0.0):.4f} "
            f"area_contact_restraint={float(decision.get('area_contact_restraint', decision.get('area_motor_restraint', 0.0)) or 0.0):.4f} "
            f"entry_geometry_state={str(decision.get('entry_geometry_state', 'contact_offer_only') or 'contact_offer_only')} "
            f"entry_geometry_bearing={float(decision.get('entry_geometry_bearing', 0.0) or 0.0):.4f} "
            f"organic_contact_bearing={float(decision.get('organic_contact_bearing', 0.0) or 0.0):.4f} "
            f"thought_seed_bearing={float(decision.get('thought_seed_bearing', 0.0) or 0.0):.4f} "
            f"thought_state_bearing={float(decision.get('thought_state_bearing', 0.0) or 0.0):.4f} "
            f"thought_state_carrier_factor={float(decision.get('thought_state_carrier_factor', 0.0) or 0.0):.4f} "
            f"thought_contact_bearing={float(decision.get('thought_contact_bearing', 0.0) or 0.0):.4f} "
            f"pre_geometry_thought_bearing={float(decision.get('pre_geometry_thought_bearing', 0.0) or 0.0):.4f} "
            f"pre_geometry_felt_bearing={float(decision.get('pre_geometry_felt_bearing', 0.0) or 0.0):.4f} "
            f"pre_geometry_reality_bearing={float(decision.get('pre_geometry_reality_bearing', 0.0) or 0.0):.4f} "
            f"pre_geometry_preference_bearing={float(decision.get('pre_geometry_preference_bearing', 0.0) or 0.0):.4f} "
            f"visual_reality_bearing={float(decision.get('visual_reality_bearing', 0.0) or 0.0):.4f} "
            f"felt_reality_bearing={float(decision.get('felt_reality_bearing', 0.0) or 0.0):.4f} "
            f"thought_reality_bearing={float(decision.get('thought_reality_bearing', 0.0) or 0.0):.4f} "
            f"form_mcm_reality_fit={float(decision.get('form_mcm_reality_fit', 0.0) or 0.0):.4f} "
            f"hypothesis_reality_binding={float(decision.get('hypothesis_reality_binding', 0.0) or 0.0):.4f} "
            f"hypothesis_reality_binding_gap={float(decision.get('hypothesis_reality_binding_gap', 0.0) or 0.0):.4f} "
            f"hypothesis_reality_binding_state={str(decision.get('hypothesis_reality_binding_state', 'hypothesis_reality_unread') or 'hypothesis_reality_unread')} "
            f"hypothesis_contact_restraint={float(decision.get('hypothesis_contact_restraint', 0.0) or 0.0):.4f} "
            f"receptive_contact_offer_pressure={float(decision.get('receptive_contact_offer_pressure', 0.0) or 0.0):.4f} "
            f"receptive_contact_maturity={float(decision.get('receptive_contact_maturity', 0.0) or 0.0):.4f} "
            f"receptive_contact_immaturity_pressure={float(decision.get('receptive_contact_immaturity_pressure', 0.0) or 0.0):.4f} "
            f"receptive_contact_restraint={float(decision.get('receptive_contact_restraint', 0.0) or 0.0):.4f} "
            f"hypothesis_reality_state={str(decision.get('hypothesis_reality_state', 'hypothesis_context_unread') or 'hypothesis_context_unread')} "
            f"pre_entry_emergent_structure_state={str(decision.get('pre_entry_emergent_structure_state', 'ordinary_structure_contact') or 'ordinary_structure_contact')} "
            f"pre_entry_emergent_structure_reading={float(decision.get('pre_entry_emergent_structure_reading', 0.0) or 0.0):.4f} "
            f"pre_entry_emergent_structure_confirmation={float(decision.get('pre_entry_emergent_structure_confirmation', 0.0) or 0.0):.4f} "
            f"hypothesis_role={str(decision.get('hypothesis_role', 'thought_reality_probe') or 'thought_reality_probe')} "
            f"hypothesis_reality_modulation={float(decision.get('hypothesis_reality_modulation', 0.0) or 0.0):.4f} "
            f"hypothesis_reality_bearing={float(decision.get('hypothesis_reality_bearing', decision.get('hypothesis_action_support', 0.0)) or 0.0):.4f} "
            f"hypothesis_observation_pressure={float(decision.get('hypothesis_observation_pressure', 0.0) or 0.0):.4f} "
            f"long_score={float(decision.get('long_score', 0.0) or 0.0):.4f} "
            f"short_score={float(decision.get('short_score', 0.0) or 0.0):.4f}",
            "entry_debug.csv",
        )

    consent_state = _resolve_inner_action_consent(decision)
    decision = _with_inner_action_consent(decision, consent_state)
    meta_regulation_state = dict(decision.get("meta_regulation_state", {}) or {})
    if not bool(consent_state.get("allowed", False)):
        _entry_bridge_debug(
            "MCM_ENTRY_BRIDGE | state=inner_action_reframed "
            f"proposed={side} tendency={consent_state.get('tendency')} "
            f"reason={consent_state.get('reason')} "
            f"consent={float(consent_state.get('inner_action_consent', 0.0) or 0.0):.4f} "
            f"support={float(consent_state.get('inner_action_support', 0.0) or 0.0):.4f} "
            f"inner_no={float(consent_state.get('inner_action_no', 0.0) or 0.0):.4f} "
            f"thought_confirmation_bearing={float(consent_state.get('thought_confirmation_bearing', consent_state.get('strategy_confirmation', 0.0)) or 0.0):.4f} "
            f"thought_rejection_pressure={float(consent_state.get('thought_rejection_pressure', consent_state.get('strategy_rejection', 0.0)) or 0.0):.4f} "
            f"thought_trust_bearing={float(consent_state.get('thought_trust_bearing', consent_state.get('strategy_trust_bearing', 0.0)) or 0.0):.4f} "
            f"contact_context_bearing={float(consent_state.get('contact_context_bearing', consent_state.get('strategy_context_bearing', 0.0)) or 0.0):.4f} "
            f"thought_contact_consent={float(consent_state.get('thought_contact_consent', 0.0) or 0.0):.4f} "
            f"thought_area_coupling={float(consent_state.get('thought_area_coupling', 0.0) or 0.0):.4f} "
            f"felt_area_coupling={float(consent_state.get('felt_area_coupling', 0.0) or 0.0):.4f} "
            f"sensory_area_coupling={float(consent_state.get('sensory_area_coupling', 0.0) or 0.0):.4f} "
            f"analytic_action_bearing={float(consent_state.get('analytic_action_bearing', 0.0) or 0.0):.4f} "
            f"intuitive_action_bearing={float(consent_state.get('intuitive_action_bearing', 0.0) or 0.0):.4f} "
            f"conscious_action_bearing={float(consent_state.get('conscious_action_bearing', 0.0) or 0.0):.4f} "
            f"form_contact_usefulness={float(consent_state.get('form_contact_usefulness', 0.0) or 0.0):.4f} "
            f"form_contact_burden={float(consent_state.get('form_contact_burden', 0.0) or 0.0):.4f} "
            f"untrusted_contact_pressure={float(consent_state.get('untrusted_contact_pressure', 0.0) or 0.0):.4f} "
            f"uncoupled_area_contact_pressure={float(consent_state.get('uncoupled_area_contact_pressure', 0.0) or 0.0):.4f} "
            f"raw_area_contact_bearing={float(consent_state.get('raw_area_contact_bearing', 0.0) or 0.0):.4f} "
            f"real_area_contact_bearing={float(consent_state.get('real_area_contact_bearing', 0.0) or 0.0):.4f} "
            f"receptive_contact_offer_pressure={float(consent_state.get('receptive_contact_offer_pressure', 0.0) or 0.0):.4f} "
            f"receptive_contact_maturity={float(consent_state.get('receptive_contact_maturity', 0.0) or 0.0):.4f} "
            f"receptive_contact_immaturity_pressure={float(consent_state.get('receptive_contact_immaturity_pressure', 0.0) or 0.0):.4f} "
            f"receptive_contact_restraint={float(consent_state.get('receptive_contact_restraint', 0.0) or 0.0):.4f} "
            f"contact_memory_evidence={float(consent_state.get('contact_memory_evidence', 0.0) or 0.0):.4f} "
            f"receptive_contact_memory_gap={float(consent_state.get('receptive_contact_memory_gap', 0.0) or 0.0):.4f} "
            f"receptive_exploration_bearing={float(consent_state.get('receptive_exploration_bearing', 0.0) or 0.0):.4f} "
            f"thought_contradiction_pressure={float(consent_state.get('thought_contradiction_pressure', consent_state.get('strategy_contradiction_pressure', 0.0)) or 0.0):.4f} "
            f"dominant_reality_bearing={float(consent_state.get('dominant_hypothesis_reality_bearing', consent_state.get('dominant_hypothesis_action_readiness', 0.0)) or 0.0):.4f} "
            f"hypothesis_role={str(consent_state.get('hypothesis_role', 'thought_reality_probe') or 'thought_reality_probe')} "
            f"entry_geometry_state={str(decision.get('entry_geometry_state', 'contact_offer_only') or 'contact_offer_only')} "
            f"entry_geometry_bearing={float(decision.get('entry_geometry_bearing', 0.0) or 0.0):.4f} "
            f"organic_contact_bearing={float(decision.get('organic_contact_bearing', 0.0) or 0.0):.4f} "
            f"thought_seed_bearing={float(decision.get('thought_seed_bearing', 0.0) or 0.0):.4f} "
            f"thought_state_bearing={float(decision.get('thought_state_bearing', 0.0) or 0.0):.4f} "
            f"thought_state_carrier_factor={float(decision.get('thought_state_carrier_factor', 0.0) or 0.0):.4f} "
            f"thought_contact_bearing={float(decision.get('thought_contact_bearing', 0.0) or 0.0):.4f} "
            f"pre_geometry_thought_bearing={float(decision.get('pre_geometry_thought_bearing', 0.0) or 0.0):.4f} "
            f"pre_geometry_felt_bearing={float(decision.get('pre_geometry_felt_bearing', 0.0) or 0.0):.4f} "
            f"pre_geometry_reality_bearing={float(decision.get('pre_geometry_reality_bearing', 0.0) or 0.0):.4f} "
            f"pre_geometry_preference_bearing={float(decision.get('pre_geometry_preference_bearing', 0.0) or 0.0):.4f} "
            f"visual_reality_bearing={float(decision.get('visual_reality_bearing', 0.0) or 0.0):.4f} "
            f"felt_reality_bearing={float(decision.get('felt_reality_bearing', 0.0) or 0.0):.4f} "
            f"thought_reality_bearing={float(decision.get('thought_reality_bearing', 0.0) or 0.0):.4f} "
            f"form_mcm_reality_fit={float(decision.get('form_mcm_reality_fit', 0.0) or 0.0):.4f} "
            f"hypothesis_reality_binding={float(decision.get('hypothesis_reality_binding', 0.0) or 0.0):.4f} "
            f"hypothesis_reality_binding_gap={float(decision.get('hypothesis_reality_binding_gap', 0.0) or 0.0):.4f} "
            f"hypothesis_reality_binding_state={str(decision.get('hypothesis_reality_binding_state', 'hypothesis_reality_unread') or 'hypothesis_reality_unread')} "
            f"hypothesis_contact_restraint={float(decision.get('hypothesis_contact_restraint', 0.0) or 0.0):.4f} "
            f"pre_entry_emergent_structure_state={str(decision.get('pre_entry_emergent_structure_state', 'ordinary_structure_contact') or 'ordinary_structure_contact')} "
            f"pre_entry_emergent_structure_reading={float(decision.get('pre_entry_emergent_structure_reading', 0.0) or 0.0):.4f} "
            f"pre_entry_emergent_structure_confirmation={float(decision.get('pre_entry_emergent_structure_confirmation', 0.0) or 0.0):.4f} "
            f"entry_mode={str(decision.get('entry_mode', 'no_mature_entry_thesis') or 'no_mature_entry_thesis')} "
            f"entry_contact_state={str(decision.get('entry_contact_state', decision.get('entry_choice_state', 'no_entry_choice')) or 'no_entry_choice')} "
            f"area_contact_location={str(decision.get('area_contact_location', decision.get('strategic_entry_location', '-')) or '-')}"
        )
        if DEBUG:
            dbr_debug(
                f"MCM_INNER_ACTION_CONSENT | proposed={side} tendency={consent_state.get('tendency')} "
                f"reason={consent_state.get('reason')} consent={float(consent_state.get('inner_action_consent', 0.0) or 0.0):.4f} "
                f"support={float(consent_state.get('inner_action_support', 0.0) or 0.0):.4f} "
                f"inner_no={float(consent_state.get('inner_action_no', 0.0) or 0.0):.4f} "
                f"thought_confirmation_bearing={float(consent_state.get('thought_confirmation_bearing', consent_state.get('strategy_confirmation', 0.0)) or 0.0):.4f} "
                f"thought_rejection_pressure={float(consent_state.get('thought_rejection_pressure', consent_state.get('strategy_rejection', 0.0)) or 0.0):.4f} "
                f"thought_trust_bearing={float(consent_state.get('thought_trust_bearing', consent_state.get('strategy_trust_bearing', 0.0)) or 0.0):.4f} "
                f"contact_context_bearing={float(consent_state.get('contact_context_bearing', consent_state.get('strategy_context_bearing', 0.0)) or 0.0):.4f} "
                f"thought_contact_consent={float(consent_state.get('thought_contact_consent', 0.0) or 0.0):.4f} "
                f"thought_area_coupling={float(consent_state.get('thought_area_coupling', 0.0) or 0.0):.4f} "
                f"felt_area_coupling={float(consent_state.get('felt_area_coupling', 0.0) or 0.0):.4f} "
                f"sensory_area_coupling={float(consent_state.get('sensory_area_coupling', 0.0) or 0.0):.4f} "
                f"analytic_action_bearing={float(consent_state.get('analytic_action_bearing', 0.0) or 0.0):.4f} "
                f"intuitive_action_bearing={float(consent_state.get('intuitive_action_bearing', 0.0) or 0.0):.4f} "
                f"conscious_action_bearing={float(consent_state.get('conscious_action_bearing', 0.0) or 0.0):.4f} "
                f"form_contact_usefulness={float(consent_state.get('form_contact_usefulness', 0.0) or 0.0):.4f} "
                f"form_contact_burden={float(consent_state.get('form_contact_burden', 0.0) or 0.0):.4f} "
                f"untrusted_contact_pressure={float(consent_state.get('untrusted_contact_pressure', 0.0) or 0.0):.4f} "
                f"uncoupled_area_contact_pressure={float(consent_state.get('uncoupled_area_contact_pressure', 0.0) or 0.0):.4f} "
                f"raw_area_contact_bearing={float(consent_state.get('raw_area_contact_bearing', 0.0) or 0.0):.4f} "
                f"real_area_contact_bearing={float(consent_state.get('real_area_contact_bearing', 0.0) or 0.0):.4f} "
                f"receptive_contact_offer_pressure={float(consent_state.get('receptive_contact_offer_pressure', 0.0) or 0.0):.4f} "
                f"receptive_contact_maturity={float(consent_state.get('receptive_contact_maturity', 0.0) or 0.0):.4f} "
                f"receptive_contact_immaturity_pressure={float(consent_state.get('receptive_contact_immaturity_pressure', 0.0) or 0.0):.4f} "
                f"receptive_contact_restraint={float(consent_state.get('receptive_contact_restraint', 0.0) or 0.0):.4f} "
                f"contact_memory_evidence={float(consent_state.get('contact_memory_evidence', 0.0) or 0.0):.4f} "
                f"receptive_contact_memory_gap={float(consent_state.get('receptive_contact_memory_gap', 0.0) or 0.0):.4f} "
                f"receptive_exploration_bearing={float(consent_state.get('receptive_exploration_bearing', 0.0) or 0.0):.4f} "
                f"thought_contradiction_pressure={float(consent_state.get('thought_contradiction_pressure', consent_state.get('strategy_contradiction_pressure', 0.0)) or 0.0):.4f} "
                f"entry_geometry_state={str(decision.get('entry_geometry_state', 'contact_offer_only') or 'contact_offer_only')} "
                f"entry_geometry_bearing={float(decision.get('entry_geometry_bearing', 0.0) or 0.0):.4f} "
                f"organic_contact_bearing={float(decision.get('organic_contact_bearing', 0.0) or 0.0):.4f} "
                f"thought_seed_bearing={float(decision.get('thought_seed_bearing', 0.0) or 0.0):.4f} "
                f"thought_state_bearing={float(decision.get('thought_state_bearing', 0.0) or 0.0):.4f} "
                f"thought_state_carrier_factor={float(decision.get('thought_state_carrier_factor', 0.0) or 0.0):.4f} "
                f"thought_contact_bearing={float(decision.get('thought_contact_bearing', 0.0) or 0.0):.4f} "
                f"pre_geometry_thought_bearing={float(decision.get('pre_geometry_thought_bearing', 0.0) or 0.0):.4f} "
                f"pre_geometry_felt_bearing={float(decision.get('pre_geometry_felt_bearing', 0.0) or 0.0):.4f} "
                f"pre_geometry_reality_bearing={float(decision.get('pre_geometry_reality_bearing', 0.0) or 0.0):.4f} "
                f"pre_geometry_preference_bearing={float(decision.get('pre_geometry_preference_bearing', 0.0) or 0.0):.4f} "
                f"visual_reality_bearing={float(decision.get('visual_reality_bearing', 0.0) or 0.0):.4f} "
                f"felt_reality_bearing={float(decision.get('felt_reality_bearing', 0.0) or 0.0):.4f} "
                f"thought_reality_bearing={float(decision.get('thought_reality_bearing', 0.0) or 0.0):.4f} "
                f"form_mcm_reality_fit={float(decision.get('form_mcm_reality_fit', 0.0) or 0.0):.4f} "
                f"hypothesis_reality_binding={float(decision.get('hypothesis_reality_binding', 0.0) or 0.0):.4f} "
                f"hypothesis_reality_binding_gap={float(decision.get('hypothesis_reality_binding_gap', 0.0) or 0.0):.4f} "
                f"hypothesis_reality_binding_state={str(decision.get('hypothesis_reality_binding_state', 'hypothesis_reality_unread') or 'hypothesis_reality_unread')} "
                f"hypothesis_contact_restraint={float(decision.get('hypothesis_contact_restraint', 0.0) or 0.0):.4f} "
                f"pre_entry_emergent_structure_state={str(decision.get('pre_entry_emergent_structure_state', 'ordinary_structure_contact') or 'ordinary_structure_contact')} "
                f"pre_entry_emergent_structure_reading={float(decision.get('pre_entry_emergent_structure_reading', 0.0) or 0.0):.4f} "
                f"pre_entry_emergent_structure_confirmation={float(decision.get('pre_entry_emergent_structure_confirmation', 0.0) or 0.0):.4f} "
                f"entry_mode={str(decision.get('entry_mode', 'no_mature_entry_thesis') or 'no_mature_entry_thesis')} "
                f"entry_contact_state={str(decision.get('entry_contact_state', decision.get('entry_choice_state', 'no_entry_choice')) or 'no_entry_choice')} "
                f"area_contact_location={str(decision.get('area_contact_location', decision.get('strategic_entry_location', '-')) or '-')}",
                "entry_debug.csv",
            )
        return _as_inner_non_action(decision, consent_state)

    _entry_bridge_debug(
        "MCM_ENTRY_BRIDGE | state=inner_action_accepted "
        f"side={side} entry={entry_price:.8f} sl={sl_price:.8f} tp={tp_price:.8f} rr={rr_value:.4f} "
        f"consent={float(consent_state.get('inner_action_consent', 0.0) or 0.0):.4f} "
        f"support={float(consent_state.get('inner_action_support', 0.0) or 0.0):.4f} "
        f"inner_no={float(consent_state.get('inner_action_no', 0.0) or 0.0):.4f} "
        f"thought_confirmation_bearing={float(consent_state.get('thought_confirmation_bearing', consent_state.get('strategy_confirmation', 0.0)) or 0.0):.4f} "
        f"thought_rejection_pressure={float(consent_state.get('thought_rejection_pressure', consent_state.get('strategy_rejection', 0.0)) or 0.0):.4f} "
        f"thought_trust_bearing={float(consent_state.get('thought_trust_bearing', consent_state.get('strategy_trust_bearing', 0.0)) or 0.0):.4f} "
        f"contact_context_bearing={float(consent_state.get('contact_context_bearing', consent_state.get('strategy_context_bearing', 0.0)) or 0.0):.4f} "
        f"thought_contact_consent={float(consent_state.get('thought_contact_consent', 0.0) or 0.0):.4f} "
        f"thought_area_coupling={float(consent_state.get('thought_area_coupling', 0.0) or 0.0):.4f} "
        f"felt_area_coupling={float(consent_state.get('felt_area_coupling', 0.0) or 0.0):.4f} "
        f"sensory_area_coupling={float(consent_state.get('sensory_area_coupling', 0.0) or 0.0):.4f} "
        f"analytic_action_bearing={float(consent_state.get('analytic_action_bearing', 0.0) or 0.0):.4f} "
        f"intuitive_action_bearing={float(consent_state.get('intuitive_action_bearing', 0.0) or 0.0):.4f} "
        f"conscious_action_bearing={float(consent_state.get('conscious_action_bearing', 0.0) or 0.0):.4f} "
        f"form_contact_usefulness={float(consent_state.get('form_contact_usefulness', 0.0) or 0.0):.4f} "
        f"form_contact_burden={float(consent_state.get('form_contact_burden', 0.0) or 0.0):.4f} "
        f"untrusted_contact_pressure={float(consent_state.get('untrusted_contact_pressure', 0.0) or 0.0):.4f} "
        f"uncoupled_area_contact_pressure={float(consent_state.get('uncoupled_area_contact_pressure', 0.0) or 0.0):.4f} "
        f"raw_area_contact_bearing={float(consent_state.get('raw_area_contact_bearing', 0.0) or 0.0):.4f} "
        f"real_area_contact_bearing={float(consent_state.get('real_area_contact_bearing', 0.0) or 0.0):.4f} "
        f"receptive_contact_offer_pressure={float(consent_state.get('receptive_contact_offer_pressure', 0.0) or 0.0):.4f} "
        f"receptive_contact_maturity={float(consent_state.get('receptive_contact_maturity', 0.0) or 0.0):.4f} "
        f"receptive_contact_immaturity_pressure={float(consent_state.get('receptive_contact_immaturity_pressure', 0.0) or 0.0):.4f} "
        f"receptive_contact_restraint={float(consent_state.get('receptive_contact_restraint', 0.0) or 0.0):.4f} "
        f"thought_contradiction_pressure={float(consent_state.get('thought_contradiction_pressure', consent_state.get('strategy_contradiction_pressure', 0.0)) or 0.0):.4f} "
        f"entry_geometry_state={str(decision.get('entry_geometry_state', 'contact_offer_only') or 'contact_offer_only')} "
        f"entry_geometry_bearing={float(decision.get('entry_geometry_bearing', 0.0) or 0.0):.4f} "
        f"organic_contact_bearing={float(decision.get('organic_contact_bearing', 0.0) or 0.0):.4f} "
        f"thought_seed_bearing={float(decision.get('thought_seed_bearing', 0.0) or 0.0):.4f} "
        f"thought_state_bearing={float(decision.get('thought_state_bearing', 0.0) or 0.0):.4f} "
        f"thought_state_carrier_factor={float(decision.get('thought_state_carrier_factor', 0.0) or 0.0):.4f} "
        f"thought_contact_bearing={float(decision.get('thought_contact_bearing', 0.0) or 0.0):.4f} "
        f"pre_geometry_thought_bearing={float(decision.get('pre_geometry_thought_bearing', 0.0) or 0.0):.4f} "
        f"pre_geometry_felt_bearing={float(decision.get('pre_geometry_felt_bearing', 0.0) or 0.0):.4f} "
        f"pre_geometry_reality_bearing={float(decision.get('pre_geometry_reality_bearing', 0.0) or 0.0):.4f} "
        f"pre_geometry_preference_bearing={float(decision.get('pre_geometry_preference_bearing', 0.0) or 0.0):.4f} "
        f"visual_reality_bearing={float(decision.get('visual_reality_bearing', 0.0) or 0.0):.4f} "
        f"felt_reality_bearing={float(decision.get('felt_reality_bearing', 0.0) or 0.0):.4f} "
        f"thought_reality_bearing={float(decision.get('thought_reality_bearing', 0.0) or 0.0):.4f} "
        f"form_mcm_reality_fit={float(decision.get('form_mcm_reality_fit', 0.0) or 0.0):.4f} "
        f"hypothesis_reality_binding={float(decision.get('hypothesis_reality_binding', 0.0) or 0.0):.4f} "
        f"hypothesis_reality_binding_gap={float(decision.get('hypothesis_reality_binding_gap', 0.0) or 0.0):.4f} "
        f"hypothesis_reality_binding_state={str(decision.get('hypothesis_reality_binding_state', 'hypothesis_reality_unread') or 'hypothesis_reality_unread')} "
        f"hypothesis_contact_restraint={float(decision.get('hypothesis_contact_restraint', 0.0) or 0.0):.4f} "
        f"pre_entry_emergent_structure_state={str(decision.get('pre_entry_emergent_structure_state', 'ordinary_structure_contact') or 'ordinary_structure_contact')} "
        f"pre_entry_emergent_structure_reading={float(decision.get('pre_entry_emergent_structure_reading', 0.0) or 0.0):.4f} "
        f"pre_entry_emergent_structure_confirmation={float(decision.get('pre_entry_emergent_structure_confirmation', 0.0) or 0.0):.4f} "
        f"entry_mode={str(decision.get('entry_mode', 'no_mature_entry_thesis') or 'no_mature_entry_thesis')} "
        f"entry_contact_state={str(decision.get('entry_contact_state', decision.get('entry_choice_state', 'no_entry_choice')) or 'no_entry_choice')} "
        f"area_contact_location={str(decision.get('area_contact_location', decision.get('strategic_entry_location', '-')) or '-')}"
    )

    return {
        "decision_tendency": "act",
        "decision": side,
        "entry_price": entry_price,
        "tp_price": tp_price,
        "sl_price": sl_price,
        "rr_value": rr_value,
        "energy": float(decision.get("energy", 0.0) or 0.0),
        "coherence": float(decision.get("coherence", 0.0) or 0.0),
        "asymmetry": int(decision.get("asymmetry", 0) or 0),
        "coh_zone": float(decision.get("coh_zone", 0.0) or 0.0),
        "self_state": str(decision.get("self_state", "stable")),
        "attractor": str(decision.get("attractor", "neutral")),
        "memory_center": float(decision.get("memory_center", 0.0) or 0.0),
        "memory_strength": int(decision.get("memory_strength", 0) or 0),
        "vision": raw_vision,
        "filtered_vision": filtered_vision,
        "focus": focus,
        "world_state": dict(decision.get("world_state", {}) or {}),
        "structure_perception_state": dict(decision.get("structure_perception_state", {}) or {}),
        "outer_visual_perception_state": dict(decision.get("outer_visual_perception_state", {}) or {}),
        "inner_field_perception_state": dict(decision.get("inner_field_perception_state", {}) or {}),
        "processing_state": dict(decision.get("processing_state", {}) or {}),
        "perception_state": perception_state,
        "felt_state": felt_state,
        "thought_state": thought_state,
        "meta_regulation_state": meta_regulation_state,
        "inner_action_consent": float(consent_state.get("inner_action_consent", 0.0) or 0.0),
        "inner_action_support": float(consent_state.get("inner_action_support", 0.0) or 0.0),
        "inner_action_no": float(consent_state.get("inner_action_no", 0.0) or 0.0),
        "strategy_confirmation": float(consent_state.get("strategy_confirmation", 0.0) or 0.0),
        "strategy_rejection": float(consent_state.get("strategy_rejection", 0.0) or 0.0),
        "strategy_trust_bearing": float(consent_state.get("strategy_trust_bearing", 0.0) or 0.0),
        "strategy_context_bearing": float(consent_state.get("strategy_context_bearing", 0.0) or 0.0),
        "raw_strategy_contradiction_pressure": float(consent_state.get("raw_strategy_contradiction_pressure", 0.0) or 0.0),
        "strategy_contradiction_pressure": float(consent_state.get("strategy_contradiction_pressure", 0.0) or 0.0),
        "thought_confirmation_bearing": _num_any(consent_state, "thought_confirmation_bearing", "strategy_confirmation"),
        "thought_rejection_pressure": _num_any(consent_state, "thought_rejection_pressure", "strategy_rejection"),
        "thought_trust_bearing": _num_any(consent_state, "thought_trust_bearing", "strategy_trust_bearing"),
        "contact_context_bearing": _num_any(consent_state, "contact_context_bearing", "strategy_context_bearing"),
        "raw_thought_contradiction_pressure": _num_any(consent_state, "raw_thought_contradiction_pressure", "raw_strategy_contradiction_pressure"),
        "thought_contradiction_pressure": _num_any(consent_state, "thought_contradiction_pressure", "strategy_contradiction_pressure"),
        "open_hypothesis_reality_bearing": _num_any(consent_state, "open_hypothesis_reality_bearing", "open_hypothesis_reality_permission", "open_hypothesis_action_permission"),
        "open_hypothesis_reality_fit": _num_any(consent_state, "open_hypothesis_reality_fit", "open_hypothesis_reality_bearing", "open_hypothesis_reality_permission"),
        "open_hypothesis_reality_probe": _num_any(consent_state, "open_hypothesis_reality_probe", "open_hypothesis_reality_bearing", "open_hypothesis_reality_permission"),
        "open_hypothesis_reality_permission": _num_any(consent_state, "open_hypothesis_reality_permission", "open_hypothesis_action_permission"),
        "possibility_contact_bearing": _num_any(consent_state, "possibility_contact_bearing", "possibility_action_support"),
        "dominant_hypothesis_reality_bearing": _num_any(consent_state, "dominant_hypothesis_reality_bearing", "dominant_hypothesis_action_readiness"),
        "dominant_hypothesis_reality_support": _num_any(consent_state, "dominant_hypothesis_reality_support", "dominant_hypothesis_reality_bearing", "dominant_hypothesis_action_readiness"),
        "current_hypothesis_reality_bearing": _num_any(consent_state, "current_hypothesis_reality_bearing", "current_hypothesis_action_support"),
        "current_hypothesis_reality_support": _num_any(consent_state, "current_hypothesis_reality_support", "current_hypothesis_reality_bearing", "current_hypothesis_action_support"),
        "hypothesis_role": str(consent_state.get("hypothesis_role", "thought_reality_probe") or "thought_reality_probe"),
        "thought_contact_consent": _num_any(consent_state, "thought_contact_consent"),
        "thought_area_coupling": _num_any(consent_state, "thought_area_coupling"),
        "felt_area_coupling": _num_any(consent_state, "felt_area_coupling"),
        "sensory_area_coupling": _num_any(consent_state, "sensory_area_coupling"),
        "analytic_action_bearing": _num_any(consent_state, "analytic_action_bearing"),
        "intuitive_action_bearing": _num_any(consent_state, "intuitive_action_bearing"),
        "conscious_action_bearing": _num_any(consent_state, "conscious_action_bearing"),
        "form_contact_usefulness": _num_any(consent_state, "form_contact_usefulness"),
        "form_contact_burden": _num_any(consent_state, "form_contact_burden"),
        "untrusted_contact_pressure": _num_any(consent_state, "untrusted_contact_pressure"),
        "uncoupled_area_contact_pressure": _num_any(consent_state, "uncoupled_area_contact_pressure"),
        "raw_area_contact_bearing": _num_any(consent_state, "raw_area_contact_bearing"),
        "real_area_contact_bearing": _num_any(consent_state, "real_area_contact_bearing"),
        "inner_action_consent_state": str(consent_state.get("reason", "-") or "-"),
        "expectation_state": expectation_state,
        "entry_expectation": float(expectation_state.get("entry_expectation", 0.0) or 0.0),
        "target_expectation": float(expectation_state.get("target_expectation", 0.0) or 0.0),
        "approach_pressure": float(expectation_state.get("approach_pressure", 0.0) or 0.0),
        "pressure_release": float(expectation_state.get("pressure_release", 0.0) or 0.0),
        "experience_regulation": float(expectation_state.get("experience_regulation", 0.0) or 0.0),
        "reflection_maturity": float(expectation_state.get("reflection_maturity", 0.0) or 0.0),
        "entry_validity_band": dict(decision.get("entry_validity_band", {}) or {}),
        "target_conviction": float(decision.get("target_conviction", 0.0) or 0.0),
        "risk_model_score": float(decision.get("risk_model_score", 0.0) or 0.0),
        "reward_model_score": float(decision.get("reward_model_score", 0.0) or 0.0),
        "entry_mode": str(decision.get("entry_mode", "no_mature_entry_thesis") or "no_mature_entry_thesis"),
        "contact_entry_mode": str(decision.get("contact_entry_mode", decision.get("entry_mode", "no_mature_entry_thesis")) or "no_mature_entry_thesis"),
        "impulse_entry_price": float(decision.get("impulse_entry_price", entry_price) or entry_price),
        "contact_entry_price": float(decision.get("contact_entry_price", decision.get("strategic_entry_price", entry_price)) or entry_price),
        "strategic_entry_price": float(decision.get("strategic_entry_price", decision.get("contact_entry_price", entry_price)) or entry_price),
        "area_contact_weight": float(decision.get("area_contact_weight", decision.get("strategic_entry_weight", 0.0)) or 0.0),
        "area_contact_fit": float(decision.get("area_contact_fit", decision.get("strategic_entry_fit", 0.0)) or 0.0),
        "area_contact_intention": float(decision.get("area_contact_intention", decision.get("area_motor_intention", 0.0)) or 0.0),
        "contact_entry_weight": float(decision.get("contact_entry_weight", decision.get("strategic_entry_weight", 0.0)) or 0.0),
        "contact_entry_fit": float(decision.get("contact_entry_fit", decision.get("strategic_entry_fit", 0.0)) or 0.0),
        "strategic_entry_weight": float(decision.get("strategic_entry_weight", decision.get("contact_entry_weight", 0.0)) or 0.0),
        "strategic_entry_fit": float(decision.get("strategic_entry_fit", decision.get("contact_entry_fit", 0.0)) or 0.0),
        "area_contact_distance_fit": float(decision.get("area_contact_distance_fit", decision.get("area_motor_distance_fit", 0.0)) or 0.0),
        "area_motor_intention": float(decision.get("area_motor_intention", 0.0) or 0.0),
        "area_motor_distance_fit": float(decision.get("area_motor_distance_fit", decision.get("area_contact_distance_fit", 0.0)) or 0.0),
        "impulse_perception_pressure": float(decision.get("impulse_perception_pressure", decision.get("impulse_entry_intention", 0.0)) or 0.0),
        "impulse_entry_intention": float(decision.get("impulse_entry_intention", 0.0) or 0.0),
        "area_order_geometry_intention": float(decision.get("area_order_geometry_intention", decision.get("area_entry_intention", 0.0)) or 0.0),
        "area_entry_intention": float(decision.get("area_entry_intention", 0.0) or 0.0),
        "entry_contact_pressure": float(decision.get("entry_contact_pressure", decision.get("entry_choice_pressure", decision.get("entry_choice_conflict", 0.0))) or 0.0),
        "entry_choice_pressure": float(decision.get("entry_choice_pressure", decision.get("entry_contact_pressure", decision.get("entry_choice_conflict", 0.0))) or 0.0),
        "entry_choice_conflict": float(decision.get("entry_choice_conflict", decision.get("entry_contact_pressure", 0.0)) or 0.0),
        "entry_contact_bearing": float(decision.get("entry_contact_bearing", decision.get("entry_choice_bearing", 0.0)) or 0.0),
        "entry_choice_bearing": float(decision.get("entry_choice_bearing", 0.0) or 0.0),
        "area_contact_readiness": float(decision.get("area_contact_readiness", decision.get("area_direct_readiness", 0.0)) or 0.0),
        "area_direct_readiness": float(decision.get("area_direct_readiness", 0.0) or 0.0),
        "area_contact_restraint": float(decision.get("area_contact_restraint", decision.get("area_motor_restraint", 0.0)) or 0.0),
        "area_motor_restraint": float(decision.get("area_motor_restraint", 0.0) or 0.0),
        "entry_geometry_bearing": float(decision.get("entry_geometry_bearing", 0.0) or 0.0),
        "entry_geometry_state": str(decision.get("entry_geometry_state", "contact_offer_only") or "contact_offer_only"),
        "pre_geometry_thought_bearing": float(decision.get("pre_geometry_thought_bearing", 0.0) or 0.0),
        "pre_geometry_felt_bearing": float(decision.get("pre_geometry_felt_bearing", 0.0) or 0.0),
        "pre_geometry_reality_bearing": float(decision.get("pre_geometry_reality_bearing", 0.0) or 0.0),
        "pre_geometry_preference_bearing": float(decision.get("pre_geometry_preference_bearing", 0.0) or 0.0),
        "visual_reality_bearing": float(decision.get("visual_reality_bearing", 0.0) or 0.0),
        "felt_reality_bearing": float(decision.get("felt_reality_bearing", 0.0) or 0.0),
        "thought_reality_bearing": float(decision.get("thought_reality_bearing", 0.0) or 0.0),
        "form_mcm_reality_fit": float(decision.get("form_mcm_reality_fit", 0.0) or 0.0),
        "hypothesis_reality_binding": float(decision.get("hypothesis_reality_binding", 0.0) or 0.0),
        "hypothesis_reality_binding_gap": float(decision.get("hypothesis_reality_binding_gap", 0.0) or 0.0),
        "hypothesis_reality_binding_state": str(decision.get("hypothesis_reality_binding_state", "hypothesis_reality_unread") or "hypothesis_reality_unread"),
        "hypothesis_reality_binding_pressures": dict(decision.get("hypothesis_reality_binding_pressures", {}) or {}),
        "organic_contact_bearing": float(decision.get("organic_contact_bearing", 0.0) or 0.0),
        "entry_contact_state": str(decision.get("entry_contact_state", decision.get("entry_choice_state", "no_entry_choice")) or "no_entry_choice"),
        "entry_choice_state": str(decision.get("entry_choice_state", "no_entry_choice") or "no_entry_choice"),
        "entry_preference_state": str(decision.get("entry_preference_state", "no_entry_preference") or "no_entry_preference"),
        "entry_choice_basis": str(decision.get("entry_choice_basis", "no_contact_offer") or "no_contact_offer"),
        "entry_contact_option_count": int(decision.get("entry_contact_option_count", 0) or 0),
        "selected_entry_offer_score": float(decision.get("selected_entry_offer_score", 0.0) or 0.0),
        "selected_entry_learned_fit": float(decision.get("selected_entry_learned_fit", 0.0) or 0.0),
        "selected_entry_preference_key": str(decision.get("selected_entry_preference_key", "-") or "-"),
        "selected_entry_preference_trust": float(decision.get("selected_entry_preference_trust", 0.0) or 0.0),
        "selected_entry_preference_caution": float(decision.get("selected_entry_preference_caution", 0.0) or 0.0),
        "selected_entry_preference_maturity": float(decision.get("selected_entry_preference_maturity", 0.0) or 0.0),
        "selected_entry_preference_utility": float(decision.get("selected_entry_preference_utility", 0.0) or 0.0),
        "entry_contact_options": list(decision.get("entry_contact_options", []) or []),
        "contact_learning_state": str(decision.get("contact_learning_state", "unformed_contact") or "unformed_contact"),
        "learned_contact_fit": float(decision.get("learned_contact_fit", 0.0) or 0.0),
        "entry_choice_sync": str(decision.get("entry_choice_sync", "-") or "-"),
        "hypothesis_reality_state": str(decision.get("hypothesis_reality_state", "hypothesis_context_unread") or "hypothesis_context_unread"),
        "hypothesis_reality_modulation": float(decision.get("hypothesis_reality_modulation", 0.0) or 0.0),
        "hypothesis_reality_bearing": float(decision.get("hypothesis_reality_bearing", decision.get("hypothesis_action_support", 0.0)) or 0.0),
        "hypothesis_role": str(decision.get("hypothesis_role", "thought_reality_probe") or "thought_reality_probe"),
        "hypothesis_action_support": float(decision.get("hypothesis_action_support", 0.0) or 0.0),
        "hypothesis_observation_pressure": float(decision.get("hypothesis_observation_pressure", 0.0) or 0.0),
        "order_geometry_source": str(decision.get("order_geometry_source", "area_contact_adapter") or "area_contact_adapter"),
        "impulse_role": str(decision.get("impulse_role", "perception_pressure_only") or "perception_pressure_only"),
        "strategic_area_focus_id": str(decision.get("strategic_area_focus_id", "-") or "-"),
        "strategic_area_price_low": float(decision.get("strategic_area_price_low", 0.0) or 0.0),
        "strategic_area_price_high": float(decision.get("strategic_area_price_high", 0.0) or 0.0),
        "strategic_entry_location": str(decision.get("strategic_entry_location", "-") or "-"),
        "state_signature": state_signature,
        "signature_bias": float(decision.get("signature_bias", 0.0) or 0.0),
        "signature_block": bool(decision.get("signature_block", False)),
        "signature_quality": float(decision.get("signature_quality", 0.0) or 0.0),
        "signature_distance": float(decision.get("signature_distance", 0.0) or 0.0),
        "context_cluster_id": str(decision.get("context_cluster_id", "-") or "-"),
        "context_cluster_bias": float(decision.get("context_cluster_bias", 0.0) or 0.0),
        "context_cluster_quality": float(decision.get("context_cluster_quality", 0.0) or 0.0),
        "context_cluster_distance": float(decision.get("context_cluster_distance", 0.0) or 0.0),
        "context_cluster_block": bool(decision.get("context_cluster_block", False)),
        "inhibition_level": float(decision.get("inhibition_level", 0.0) or 0.0),
        "habituation_level": float(decision.get("habituation_level", 0.0) or 0.0),
        "competition_bias": float(decision.get("competition_bias", 0.0) or 0.0),
        "observation_mode": bool(decision.get("observation_mode", False)),
        "long_score": float(decision.get("long_score", 0.0) or 0.0),
        "short_score": float(decision.get("short_score", 0.0) or 0.0),
        "felt_bearing_score": float(decision.get("felt_bearing_score", 0.0) or 0.0),
        "felt_profile_label": str(decision.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
    }
