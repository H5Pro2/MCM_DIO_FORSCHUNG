"""Debug protocol writers for DIO runtime traces.

This module owns CSV/debug protocol emission. It reads runtime state and writes
protocol rows only; it does not change DIO decision mechanics.
"""

import hashlib
import json
import os
import time

from config import Config
from debug_tools.writers import dbr_append_text, dbr_file_write_profile, dbr_path
from core.form_language import _build_dio_form_language_state
from core.mcm_field import _normalize_active_context_trace
from memory.thought_memory_store import _update_thought_memory

_FIELD_DECISION_PROTOCOL_HEADER_DONE = set()
_MEMORY_THINKING_PROTOCOL_HEADER_DONE = set()
_FORM_SYMBOL_PROTOCOL_HEADER_DONE = set()
_NEUROCHEMICAL_PROTOCOL_HEADER_DONE = set()
_NEURO_TRANSITION_PROTOCOL_HEADER_DONE = set()
_STRATEGIC_WINDOW_PROTOCOL_HEADER_DONE = set()
_ACTIVE_CONTACT_PROTOCOL_HEADER_DONE = set()
_THOUGHT_SEED_PROTOCOL_HEADER_DONE = set()
_THOUGHT_DIGEST_PROTOCOL_HEADER_DONE = set()
_THOUGHT_LANDKARTE_HEADER_DONE = set()


def _clip01(value):
    try:
        value = float(value)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return max(0.0, min(1.0, value))


def _landkarte_quality_label(value):
    value = _clip01(value)
    if value >= 0.66:
        return "tragend"
    if value >= 0.42:
        return "teilweise passend"
    if value >= 0.22:
        return "offen"
    return "schwach"


def _record_thought_landkarte_protocol(
    bot,
    runtime_result,
    meta_regulation_state=None,
    processing_state=None,
    felt_state=None,
    thought_state=None,
):
    """Write a readable thought map from existing perception/regulation state.

    This is debug output only. It describes how form, MCM recall, and hypothesis
    currently relate; it does not affect decisions.
    """
    if bot is None:
        return None

    if not bool(getattr(Config, "MCM_THOUGHT_LANDKARTE_DEBUG", True)):
        return None

    result = dict(runtime_result or {})
    meta = dict(meta_regulation_state or result.get("meta_regulation_state", {}) or {})
    processing = dict(processing_state or result.get("processing_state", {}) or {})
    felt = dict(felt_state or result.get("felt_state", {}) or {})
    thought = dict(thought_state or result.get("thought_state", {}) or {})
    form = dict(result.get("form_symbol_state", {}) or {})
    seed = dict(result.get("thought_seed_state", {}) or {})
    structure = dict(result.get("structure_perception_state", {}) or {})
    contact = dict(result.get("active_mcm_contact_state", {}) or {})

    phase = str(meta.get("pre_action_phase", result.get("decision_tendency", "hold")) or "hold").strip().lower()
    reason = str(meta.get("rejection_reason", result.get("rejection_reason", "-")) or "-").strip()
    decision = str(meta.get("decision", result.get("decision", "WAIT")) or "WAIT").strip().upper()
    timestamp = result.get("timestamp", getattr(bot, "current_timestamp", None))
    runtime_tick = int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0)

    protocol = dict(getattr(bot, "mcm_thought_landkarte_protocol", {}) or {})
    sequence = int(protocol.get("sequence", 0) or 0) + 1

    form_symbol_id = str(form.get("form_symbol_id", result.get("form_symbol_id", "-")) or "-").strip()
    compound_id = str(form.get("form_symbol_compound_id", form.get("compound_id", "-")) or "-").strip()
    form_layer = str(form.get("form_symbol_semantic_primary_layer", "-") or "-").strip()
    form_family = str(form.get("uncertain_form_family_state", "quiet_form_family") or "quiet_form_family").strip()
    form_profile = str(form.get("form_symbol_semantic_profile", "-") or "-").strip()

    field_label = str(meta.get("field_perception_label", processing.get("field_perception_label", "quiet_field")) or "quiet_field").strip()
    contact_state = str(
        contact.get("active_mcm_contact_state", meta.get("active_mcm_contact_state", "-")) or "-"
    ).strip()
    posture = str(contact.get("contact_posture", meta.get("contact_posture", "-")) or "-").strip()
    previous_hypothesis = str(meta.get("previous_open_hypothesis_learning_state", "-") or "-").strip()

    emergent_state = str(seed.get("emergent_structure_state", "ordinary_structure_reading") or "ordinary_structure_reading").strip()
    seed_label = str(seed.get("thought_seed_label", "-") or "-").strip()
    seed_mode = str(seed.get("seed_metaregulator_state", "-") or "-").strip()
    dio_form_mcm_token = str(seed.get("dio_form_mcm_token", "-") or "-").strip()
    dio_form_mcm_family_token = str(seed.get("dio_form_mcm_family_token", "-") or "-").strip()
    dio_form_mcm_state = str(seed.get("dio_form_mcm_syntax_state", "-") or "-").strip()

    structure_quality = _clip01(structure.get("structure_quality", meta.get("structure_quality", 0.0)))
    context_confidence = _clip01(structure.get("context_confidence", 0.0))
    visual_clarity = _clip01(meta.get("visual_clarity", processing.get("visual_clarity", felt.get("visual_clarity", 0.0))))
    visual_stability = _clip01(
        meta.get(
            "visual_object_stability",
            processing.get("visual_object_stability", felt.get("visual_object_stability", 0.0)),
        )
    )
    area_bearing = _clip01(meta.get("area_bearing_quality", result.get("entry_choice_bearing", 0.0)))
    structure_bearing = _clip01(meta.get("structure_action_bearing", 0.0))
    visual_form_fit = _clip01(
        (structure_quality * 0.30)
        + (context_confidence * 0.16)
        + (visual_clarity * 0.16)
        + (visual_stability * 0.14)
        + (area_bearing * 0.14)
        + (structure_bearing * 0.10)
    )

    inner_outer_alignment = _clip01(meta.get("inner_outer_alignment", 0.0))
    contact_carrying = _clip01(meta.get("contact_carrying_quality", contact.get("contact_carrying_quality", 0.0)))
    contact_overcoupling = _clip01(meta.get("contact_overcoupling_risk", contact.get("contact_overcoupling_risk", 0.0)))
    field_action_support = _clip01(meta.get("field_action_support", 0.0))
    field_observation_need = _clip01(meta.get("field_observation_need", 0.0))
    felt_afterimage = _clip01(meta.get("felt_afterimage", 0.0))
    mcm_context_fit = _clip01(
        (inner_outer_alignment * 0.24)
        + (contact_carrying * 0.22)
        + (field_action_support * 0.18)
        + ((1.0 - contact_overcoupling) * 0.14)
        + ((1.0 - field_observation_need) * 0.12)
        + (felt_afterimage * 0.10)
    )

    thought_confirmation = _clip01(seed.get("thought_confirmation_score", thought.get("thought_confirmation_score", 0.0)))
    reality_binding = _clip01(seed.get("reality_binding_score", 0.0))
    structural_grounding = _clip01(seed.get("thought_structural_grounding", 0.0))
    open_pressure = _clip01(seed.get("thought_open_hypothesis_pressure", 0.0))
    hypothesis_fit = _clip01(
        (thought_confirmation * 0.34)
        + (reality_binding * 0.26)
        + (structural_grounding * 0.20)
        + ((1.0 - open_pressure) * 0.10)
        + (mcm_context_fit * 0.10)
    )

    mismatch = _clip01(abs(visual_form_fit - mcm_context_fit) + max(0.0, open_pressure - thought_confirmation) * 0.30)
    thought_overprocessing = _clip01(meta.get("thought_overprocessing_signal", 0.0))
    thought_economy_need = _clip01(meta.get("thought_economy_need", 0.0))
    thought_efficiency = _clip01(meta.get("thought_efficiency_support", 0.0))
    perception_event_strength = _clip01(meta.get("perception_event_strength", 0.0))
    fundamental_shift = _clip01(
        (mismatch * 0.24)
        + (hypothesis_fit * 0.20)
        + (perception_event_strength * 0.18)
        + (thought_overprocessing * 0.14)
        + (thought_economy_need * 0.12)
        + (max(0.0, thought_efficiency - 0.34) * 0.12)
    )
    event_strength = max(
        mismatch,
        hypothesis_fit,
        thought_overprocessing,
        thought_economy_need,
        perception_event_strength,
        fundamental_shift,
    )
    if mismatch >= 0.46:
        reaction = "ich halte Abstand und pruefe weiter"
    elif phase == "act":
        reaction = "ich lasse Handlung zu"
    elif phase == "replan":
        reaction = "ich ordne die Hypothese neu"
    elif phase == "observe":
        reaction = "ich beobachte die Form weiter"
    else:
        reaction = "ich halte den Kontakt noch zurueck"

    visual_label = _landkarte_quality_label(visual_form_fit)
    mcm_label = _landkarte_quality_label(mcm_context_fit)
    hypothesis_label = _landkarte_quality_label(hypothesis_fit)
    thought_label = _landkarte_quality_label(thought_efficiency)
    key = (
        f"{phase}|{reason}|{decision}|{field_label}|{contact_state}|"
        f"{emergent_state}|{dio_form_mcm_family_token}|{visual_label}|{mcm_label}|{hypothesis_label}|{reaction}"
    )
    prior_key = str(protocol.get("last_key", "") or "")
    changed = bool(not prior_key or prior_key != key)
    suppressed_count = int(protocol.get("suppressed_count", 0) or 0)
    landkarte_every_n = max(1, int(getattr(Config, "MCM_THOUGHT_LANDKARTE_EVERY_N", 25) or 25))
    min_event = _clip01(getattr(Config, "MCM_THOUGHT_LANDKARTE_MIN_EVENT", 0.52) or 0.52)
    important_event = bool(
        fundamental_shift >= min_event
        or mismatch >= 0.52
        or hypothesis_fit >= 0.62
        or perception_event_strength >= 0.62
        or thought_overprocessing >= 0.52
        or thought_economy_need >= 0.52
        or (phase == "act" and hypothesis_fit >= 0.50 and perception_event_strength >= 0.48)
        or (phase == "replan" and mismatch >= 0.38 and thought_economy_need >= 0.24)
    )
    write_due_to_summary = bool(changed and suppressed_count >= landkarte_every_n)
    should_write = bool(changed and (important_event or write_due_to_summary))
    if changed and not should_write:
        suppressed_count += 1
    elif should_write:
        suppressed_count = 0
    protocol.update(
        {
            "sequence": int(sequence),
            "last_key": str(key),
            "last_timestamp": timestamp,
            "last_runtime_tick": int(runtime_tick),
            "last_visual_form_fit": float(visual_form_fit),
            "last_mcm_context_fit": float(mcm_context_fit),
            "last_hypothesis_fit": float(hypothesis_fit),
            "last_mismatch": float(mismatch),
            "last_event_strength": float(event_strength),
            "last_fundamental_shift": float(fundamental_shift),
            "suppressed_count": int(suppressed_count),
        }
    )
    setattr(bot, "mcm_thought_landkarte_protocol", dict(protocol))

    if not should_write:
        return dict(protocol)

    path = dbr_path("mcm_thought_landkarte.txt")
    if path not in _THOUGHT_LANDKARTE_HEADER_DONE:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header = (
            "# MCM Thought Landkarte\n"
            "# Lesbares Debug-Protokoll: Formseite + MCM-Wirkseite + Hypothesenpruefung.\n"
            "# Es beschreibt vorhandene Zustaende und veraendert keine Entscheidung.\n\n"
        )
        start = time.perf_counter()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header)
        dbr_file_write_profile(
            path,
            (time.perf_counter() - start) * 1000.0,
            bytes_written=len(header.encode("utf-8")),
            operation="thought_landkarte_header",
        )
        _THOUGHT_LANDKARTE_HEADER_DONE.add(path)

    summary_note = ""
    if write_due_to_summary:
        summary_note = f" | verdichtet={landkarte_every_n}+ aehnliche/offene Denkwechsel"
    block = (
        f"[{sequence}] t={timestamp} tick={runtime_tick} phase={phase} reason={reason} decision={decision}{summary_note}\n"
        f"Form/MCM: form={form_symbol_id}/{compound_id} family={dio_form_mcm_family_token} feld={field_label} kontakt={contact_state}/{posture}\n"
        f"Pruefung: form={visual_label}({visual_form_fit:.3f}) mcm={mcm_label}({mcm_context_fit:.3f}) "
        f"hypothese={hypothesis_label}({hypothesis_fit:.3f}) mismatch={mismatch:.3f}\n"
        f"Denkonomie: fundamental={fundamental_shift:.3f} ereignis={perception_event_strength:.3f} last={thought_overprocessing:.3f} "
        f"sparbedarf={thought_economy_need:.3f} effizienz={thought_label}({thought_efficiency:.3f}) -> {reaction}\n\n"
    )
    dbr_append_text(
        path,
        block,
        operation="thought_landkarte_append",
        extra=f"phase={phase}|reason={reason}|decision={decision}",
    )
    return dict(protocol)


def _record_memory_thinking_protocol(bot, runtime_result, meta_regulation_state=None, processing_state=None, felt_state=None, thought_state=None):

    if bot is None:
        return None

    if not bool(getattr(Config, "MCM_MEMORY_THINKING_PROTOCOL_DEBUG", True)):
        return None

    result = dict(runtime_result or {})
    meta = dict(meta_regulation_state or result.get("meta_regulation_state", {}) or {})
    processing = dict(processing_state or result.get("processing_state", {}) or {})
    felt = dict(felt_state or result.get("felt_state", {}) or {})
    thought = dict(thought_state or result.get("thought_state", {}) or {})
    memory_state = dict(result.get("memory_complexity_state", getattr(bot, "last_memory_complexity_state", {}) or {}) or {})
    active_context_trace = _normalize_active_context_trace(
        result.get("active_context_trace", getattr(bot, "active_context_trace", {}) or {}) or {}
    )

    phase = str(meta.get("pre_action_phase", "hold") or "hold").strip().lower()
    reason = str(meta.get("rejection_reason", result.get("rejection_reason", "-")) or "-").strip()
    proposed_decision = str(meta.get("decision", result.get("decision", "WAIT")) or "WAIT").strip().upper()
    runtime_tick = int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0)
    timestamp = result.get("timestamp", getattr(bot, "current_timestamp", None))

    protocol = dict(getattr(bot, "mcm_memory_thinking_protocol", {}) or {})
    prior_key = str(protocol.get("last_key", "") or "")
    key = f"{phase}|{reason}|{memory_state.get('context_cluster_negative_source', '-')}"
    first_event = not bool(prior_key)
    changed = bool(first_event or prior_key != key)
    every_n = max(1, int(getattr(Config, "MCM_MEMORY_THINKING_PROTOCOL_EVERY_N", 5) or 5))
    sequence = int(protocol.get("sequence", 0) or 0) + 1

    protocol.update({
        "sequence": int(sequence),
        "last_key": str(key),
        "last_phase": str(phase),
        "last_reason": str(reason),
        "last_timestamp": timestamp,
        "last_runtime_tick": int(runtime_tick),
    })
    setattr(bot, "mcm_memory_thinking_protocol", dict(protocol))

    if not changed and (sequence % every_n) != 0:
        return dict(protocol)

    path = dbr_path("mcm_memory_thinking_protocol.csv")
    if path not in _MEMORY_THINKING_PROTOCOL_HEADER_DONE:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header_text = (
            "timestamp;runtime_tick;sequence;phase;reason;decision;"
            "neurochemical_state_label;neurochemical_dominant_tone;dopamine_tone;gaba_inhibition;"
            "noradrenaline_arousal;acetylcholine_focus;serotonin_stability;cortisol_load;"
            "endorphin_relief;glutamate_activation;neurochemical_load;neurochemical_support;neurochemical_balance;"
            "reward_stability_echo;positive_expansion_pressure;negative_contraction_pressure;positive_overextension;"
            "positive_return_pressure;mcm_axis_displacement;mcm_axis_field_position;mcm_axis_tension;mcm_axis_state;positive_zero_point_regulation;"
            "world_shift_evidence;serotonin_carryover_risk;emotional_decoupling;reactive_nervous_drive;"
            "nervous_system_overload;escape_action_drive;shock_response_risk;nervous_overload_reflection_need;"
            "active_context_self_certainty;nervous_context_overcoupling;"
            "own_field_identity_strength;foreign_semantic_pressure;adopted_language_pressure;"
            "self_foreign_boundary_clarity;semantic_origin_conflict;"
            "own_vs_foreign_margin;borrowed_vs_own_margin;boundary_support_margin;semantic_origin_state;"
            "conscious_perception_state;inner_posture_state;arousal_load;curiosity_tone;fatigue_tone;calm_tone;"
            "stimulus_field_effect;inner_impact_trace;perceived_field_change;felt_afterimage;"
            "object_release_state;inner_outer_reflection;perceptual_distance;object_contact_depth;field_attachment;"
            "release_capacity;selective_attention;background_containment;reflective_distance;inner_outer_alignment;"
            "engaged_effort;effort_state;effort_learning_pull;effort_reorganization_pressure;"
            "pre_action_reorganization_pressure;pre_action_context_selectivity;"
            "previous_packet_label;previous_packet_process_reward;previous_packet_reorganization_need;"
            "previous_open_hypothesis_learning_state;open_hypothesis_trace_strength;"
            "hypothesis_weight;hypothesis_trust;hypothesis_caution;hypothesis_reorganization_weight;"
            "action_weight;decision_weight;open_hypothesis_reifung_state;"
            "open_hypothesis_bearing_echo;open_hypothesis_reifung_pressure;"
            "open_hypothesis_reflection_pull;open_hypothesis_motor_tension;"
            "open_hypothesis_confirmation_weight;open_hypothesis_learning_charge;"
            "open_hypothesis_action_permission;open_hypothesis_reality_check_need;"
            "diffuse_open_development_pressure;posture_development_hint;"
            "metaregulator_state;metaregulator_balance;regulatory_second_order_load;"
            "subconscious_field_pressure;subconscious_habituation;subconscious_filter_strength;"
            "subconscious_buffering;subconscious_leakage;subconscious_afterimage_depth;"
            "subconscious_afterimage_pressure;subconscious_afterimage_bearing;subconscious_afterimage_clarity;"
            "subconscious_afterimage_release;subconscious_afterimage_reflection_pull;conscious_selection_pressure;"
            "conscious_workspace_focus;conscious_workspace_load;conscious_gate_balance;"
            "integration_strain_value;integration_sorting_need;integration_reframe_pull;"
            "integration_memory_recall;integration_contact_deepening;integration_response_strength;integration_response_state;"
            "cautious_hypothesis_strength;cautious_hypothesis_clarity;cautious_hypothesis_patience;cautious_hypothesis_state;"
            "temporal_binding_state;temporal_continuity;temporal_source_binding;temporal_recurrence;"
            "temporal_novelty;temporal_afterimage;temporal_decay;temporal_context_depth;"
            "mcm_spacetime_depth;memory_experience_depth;future_projection_depth;temporal_self_location;temporal_self_location_state;"
            "spacetime_unlocated_pressure;spacetime_memory_bearing;spacetime_future_bearing;spacetime_reflection_need;spacetime_regulation_support;spacetime_regulation_state;"
            "temporal_self_consistency;perception_sequence_coherence;memory_time_distance;"
            "return_strength;integration_capacity;variance_regulation;load_tolerance;impulse_control;"
            "frustration_tolerance;protective_distance_regulation;self_reflection_regulator;distance_regulation;"
            "thinking_complexity;memory_compare_load;memory_match_count;memory_support;memory_inhibition;"
            "memory_conflict;cognitive_load;decision_energy_cost;memory_effect_on_phase;"
            "memory_orientation;orientation_gap;blind_thinking_load;perception_event_strength;"
            "thought_load_pressure;thought_overprocessing_signal;thought_economy_need;"
            "thought_release_pressure;thought_efficiency_support;zero_point_regulation;"
            "symbolic_object_distance;symbolic_containment;symbolic_field_decoupling;symbolic_regulation;"
            "symbolic_inner_regulation;symbolic_action_regulation;"
            "form_symbol_development_quality;form_symbol_action_binding;form_symbol_observation_binding;"
            "form_symbol_reframe_binding;form_symbol_learning_trust;form_symbol_action_trust;"
            "form_symbol_caution_trust;learned_development_uncertainty;"
            "observation_maturity_trust;observation_action_pressure;observation_maturity_balance;"
            "observation_maturity_scope;observation_scoped_balance;observation_low_count;"
            "hypothesis_observed_outcome;hypothesis_confirmation_without_action;hypothesis_rejection_without_action;"
            "hypothesis_neutral_without_action;hypothesis_observation_maturity;possibility_maturity;"
            "possibility_caution;possibility_action_support;possibility_reality_check_need;"
            "hypothesis_observed_stability;hypothesis_trust_score;hypothesis_trust_priority;"
            "hypothesis_frustration_risk;hypothesis_distance_risk;hypothesis_trust_state;"
            "dominant_hypothesis_trust_key;dominant_hypothesis_trust_score;"
            "structure_quality;context_confidence;structure_orientation;structure_orientation_gap;"
            "structure_action_bearing;structure_action_gap;structure_action_uncertainty;"
            "known_form_support;route_familiarity;semantic_shift_pressure;transfer_bearing;interpretation_quality;adaptation_phase;"
            "trust_transfer_base;trust_transfer_support;transfer_maturity_gap;trust_transfer_mode;"
            "transfer_break_fatigue;transfer_recovery_need;transfer_break_trigger;transfer_break_ready;"
            "context_cluster_negative_source;context_cluster_id;context_cluster_seen;context_cluster_score;"
            "context_cluster_hit_ratio;context_cluster_loss_ratio;context_cluster_cancel_timeout_ratio;"
            "context_cluster_negative_evidence;context_cluster_quality;context_cluster_distance;context_cluster_trust;context_cluster_variance;"
            "signature_key;signature_seen;signature_score;signature_hit_ratio;signature_quality;signature_distance;"
            "active_context_activation;active_context_support;active_context_conflict;active_context_bearing;active_context_modulation_label;"
            "action_clearance;action_inhibition;decision_readiness;processing_load;thought_pressure;field_clarity\n"
        )
        write_start = time.perf_counter()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header_text)
        dbr_file_write_profile(
            path,
            (time.perf_counter() - write_start) * 1000.0,
            bytes_written=len(header_text.encode("utf-8")),
            operation="memory_thinking_protocol_header",
        )
        _MEMORY_THINKING_PROTOCOL_HEADER_DONE.add(path)

    def _clean(value):
        return str(value).replace("\n", " ").replace(";", "|")

    def _num(key, default=0.0):
        try:
            return float(memory_state.get(key, default) or default)
        except Exception:
            return float(default)

    row = [
        _clean(timestamp),
        int(runtime_tick),
        int(sequence),
        _clean(phase),
        _clean(reason),
        _clean(proposed_decision),
        _clean(meta.get("neurochemical_state_label", "mixed_neurochemistry")),
        _clean(meta.get("neurochemical_dominant_tone", "-")),
        f"{float(meta.get('dopamine_tone', 0.0) or 0.0):.4f}",
        f"{float(meta.get('gaba_inhibition', 0.0) or 0.0):.4f}",
        f"{float(meta.get('noradrenaline_arousal', 0.0) or 0.0):.4f}",
        f"{float(meta.get('acetylcholine_focus', 0.0) or 0.0):.4f}",
        f"{float(meta.get('serotonin_stability', 0.0) or 0.0):.4f}",
        f"{float(meta.get('cortisol_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('endorphin_relief', 0.0) or 0.0):.4f}",
        f"{float(meta.get('glutamate_activation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('neurochemical_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('neurochemical_support', 0.0) or 0.0):.4f}",
        f"{float(meta.get('neurochemical_balance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('reward_stability_echo', 0.0) or 0.0):.4f}",
        f"{float(meta.get('positive_expansion_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('negative_contraction_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('positive_overextension', 0.0) or 0.0):.4f}",
        f"{float(meta.get('positive_return_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('mcm_axis_displacement', 0.0) or 0.0):.4f}",
        f"{float(meta.get('mcm_axis_field_position', 0.0) or 0.0):.4f}",
        f"{float(meta.get('mcm_axis_tension', 0.0) or 0.0):.4f}",
        _clean(meta.get("mcm_axis_state", "0")),
        int(bool(meta.get("positive_zero_point_regulation", False))),
        f"{float(meta.get('world_shift_evidence', 0.0) or 0.0):.4f}",
        f"{float(meta.get('serotonin_carryover_risk', 0.0) or 0.0):.4f}",
        f"{float(meta.get('emotional_decoupling', 0.0) or 0.0):.4f}",
        f"{float(meta.get('reactive_nervous_drive', 0.0) or 0.0):.4f}",
        f"{float(meta.get('nervous_system_overload', 0.0) or 0.0):.4f}",
        f"{float(meta.get('escape_action_drive', 0.0) or 0.0):.4f}",
        f"{float(meta.get('shock_response_risk', 0.0) or 0.0):.4f}",
        f"{float(meta.get('nervous_overload_reflection_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('active_context_self_certainty', 0.0) or 0.0):.4f}",
        f"{float(meta.get('nervous_context_overcoupling', 0.0) or 0.0):.4f}",
        f"{float(meta.get('own_field_identity_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('foreign_semantic_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('adopted_language_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('self_foreign_boundary_clarity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('semantic_origin_conflict', 0.0) or 0.0):.4f}",
        f"{float(meta.get('own_vs_foreign_margin', 0.0) or 0.0):.4f}",
        f"{float(meta.get('borrowed_vs_own_margin', 0.0) or 0.0):.4f}",
        f"{float(meta.get('boundary_support_margin', 0.0) or 0.0):.4f}",
        _clean(meta.get("semantic_origin_state", "unlocated_semantic_contact")),
        _clean(meta.get("conscious_perception_state", "open_perception")),
        _clean(meta.get("inner_posture_state", "uncertain_open")),
        f"{float(meta.get('arousal_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('curiosity_tone', 0.0) or 0.0):.4f}",
        f"{float(meta.get('fatigue_tone', 0.0) or 0.0):.4f}",
        f"{float(meta.get('calm_tone', 0.0) or 0.0):.4f}",
        f"{float(meta.get('stimulus_field_effect', 0.0) or 0.0):.4f}",
        f"{float(meta.get('inner_impact_trace', 0.0) or 0.0):.4f}",
        f"{float(meta.get('perceived_field_change', 0.0) or 0.0):.4f}",
        f"{float(meta.get('felt_afterimage', 0.0) or 0.0):.4f}",
        _clean(meta.get("object_release_state", "holding")),
        f"{float(meta.get('inner_outer_reflection', 0.0) or 0.0):.4f}",
        f"{float(meta.get('perceptual_distance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('object_contact_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('field_attachment', 0.0) or 0.0):.4f}",
        f"{float(meta.get('release_capacity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('selective_attention', 0.0) or 0.0):.4f}",
        f"{float(meta.get('background_containment', 0.0) or 0.0):.4f}",
        f"{float(meta.get('reflective_distance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('inner_outer_alignment', 0.0) or 0.0):.4f}",
        f"{float(meta.get('engaged_effort', 0.0) or 0.0):.4f}",
        _clean(meta.get("effort_state", "settled_effort")),
        f"{float(meta.get('effort_learning_pull', 0.0) or 0.0):.4f}",
        f"{float(meta.get('effort_reorganization_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('pre_action_reorganization_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('pre_action_context_selectivity', 0.0) or 0.0):.4f}",
        _clean(meta.get("previous_packet_label", "-")),
        f"{float(meta.get('previous_packet_process_reward', 0.0) or 0.0):.4f}",
        f"{float(meta.get('previous_packet_reorganization_need', 0.0) or 0.0):.4f}",
        _clean(meta.get("previous_open_hypothesis_learning_state", "-")),
        f"{float(meta.get('open_hypothesis_trace_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_weight', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_trust', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_caution', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_reorganization_weight', 0.0) or 0.0):.4f}",
        f"{float(meta.get('action_weight', 0.0) or 0.0):.4f}",
        f"{float(meta.get('decision_weight', 0.0) or 0.0):.4f}",
        _clean(meta.get("open_hypothesis_reifung_state", "open_hypothesis_neutral_memory")),
        f"{float(meta.get('open_hypothesis_bearing_echo', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_reifung_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_reflection_pull', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_motor_tension', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_confirmation_weight', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_learning_charge', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_action_permission', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_reality_check_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('diffuse_open_development_pressure', 0.0) or 0.0):.4f}",
        _clean(meta.get("posture_development_hint", "stable_posture")),
        _clean(meta.get("metaregulator_state", "adaptive_watch")),
        f"{float(meta.get('metaregulator_balance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('regulatory_second_order_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_field_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_habituation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_filter_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_buffering', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_leakage', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_bearing', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_clarity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_release', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_reflection_pull', 0.0) or 0.0):.4f}",
        f"{float(meta.get('conscious_selection_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('conscious_workspace_focus', 0.0) or 0.0):.4f}",
        f"{float(meta.get('conscious_workspace_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('conscious_gate_balance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_strain_value', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_sorting_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_reframe_pull', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_memory_recall', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_contact_deepening', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_response_strength', 0.0) or 0.0):.4f}",
        _clean(meta.get("integration_response_state", "integration_background")),
        f"{float(meta.get('cautious_hypothesis_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('cautious_hypothesis_clarity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('cautious_hypothesis_patience', 0.0) or 0.0):.4f}",
        _clean(meta.get("cautious_hypothesis_state", "no_cautious_hypothesis")),
        _clean(meta.get("temporal_binding_state", "unbound_moment")),
        f"{float(meta.get('temporal_continuity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_source_binding', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_recurrence', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_novelty', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_afterimage', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_decay', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_context_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('mcm_spacetime_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('memory_experience_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('future_projection_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_self_location', 0.0) or 0.0):.4f}",
        _clean(meta.get("temporal_self_location_state", "unlocated_contact")),
        f"{float(meta.get('spacetime_unlocated_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('spacetime_memory_bearing', 0.0) or 0.0):.4f}",
        f"{float(meta.get('spacetime_future_bearing', 0.0) or 0.0):.4f}",
        f"{float(meta.get('spacetime_reflection_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('spacetime_regulation_support', 0.0) or 0.0):.4f}",
        _clean(meta.get("spacetime_regulation_state", "spacetime_open")),
        f"{float(meta.get('temporal_self_consistency', 0.0) or 0.0):.4f}",
        f"{float(meta.get('perception_sequence_coherence', 0.0) or 0.0):.4f}",
        f"{float(meta.get('memory_time_distance', 1.0) or 1.0):.4f}",
        f"{float(meta.get('return_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_capacity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('variance_regulation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('load_tolerance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('impulse_control', 0.0) or 0.0):.4f}",
        f"{float(meta.get('frustration_tolerance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('protective_distance_regulation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('self_reflection_regulator', 0.0) or 0.0):.4f}",
        f"{float(meta.get('distance_regulation', 0.0) or 0.0):.4f}",
        f"{_num('thinking_complexity'):.4f}",
        f"{_num('memory_compare_load'):.4f}",
        int(_num("memory_match_count")),
        f"{_num('memory_support'):.4f}",
        f"{_num('memory_inhibition'):.4f}",
        f"{_num('memory_conflict'):.4f}",
        f"{_num('cognitive_load'):.4f}",
        f"{_num('decision_energy_cost'):.4f}",
        _clean(memory_state.get("memory_effect_on_phase", "neutral")),
        f"{float(meta.get('memory_orientation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('orientation_gap', 0.0) or 0.0):.4f}",
        f"{float(meta.get('blind_thinking_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('perception_event_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('thought_load_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('thought_overprocessing_signal', 0.0) or 0.0):.4f}",
        f"{float(meta.get('thought_economy_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('thought_release_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('thought_efficiency_support', 0.0) or 0.0):.4f}",
        int(bool(meta.get("zero_point_regulation", False))),
        f"{float(meta.get('symbolic_object_distance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('symbolic_containment', 0.0) or 0.0):.4f}",
        f"{float(meta.get('symbolic_field_decoupling', 0.0) or 0.0):.4f}",
        f"{float(meta.get('symbolic_regulation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('symbolic_inner_regulation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('symbolic_action_regulation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('form_symbol_development_quality', 0.0) or 0.0):.4f}",
        f"{float(meta.get('form_symbol_action_binding', 0.0) or 0.0):.4f}",
        f"{float(meta.get('form_symbol_observation_binding', 0.0) or 0.0):.4f}",
        f"{float(meta.get('form_symbol_reframe_binding', 0.0) or 0.0):.4f}",
        f"{float(meta.get('form_symbol_learning_trust', 0.0) or 0.0):.4f}",
        f"{float(meta.get('form_symbol_action_trust', 0.0) or 0.0):.4f}",
        f"{float(meta.get('form_symbol_caution_trust', 0.0) or 0.0):.4f}",
        f"{float(meta.get('learned_development_uncertainty', 0.0) or 0.0):.4f}",
        f"{float(meta.get('observation_maturity_trust', 0.0) or 0.0):.4f}",
        f"{float(meta.get('observation_action_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('observation_maturity_balance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('observation_maturity_scope', 0.0) or 0.0):.4f}",
        f"{float(meta.get('observation_scoped_balance', 0.0) or 0.0):.4f}",
        int(float(meta.get("observation_low_count", 0) or 0)),
        _clean(meta.get("hypothesis_observed_outcome", "hypothesis_observed_open")),
        f"{float(meta.get('hypothesis_confirmation_without_action', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_rejection_without_action', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_neutral_without_action', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_observation_maturity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('possibility_maturity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('possibility_caution', 0.0) or 0.0):.4f}",
        f"{float(meta.get('possibility_action_support', 0.0) or 0.0):.4f}",
        f"{float(meta.get('possibility_reality_check_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_observed_stability', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_trust_score', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_trust_priority', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_frustration_risk', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_distance_risk', 0.0) or 0.0):.4f}",
        _clean(meta.get("hypothesis_trust_state", "hypothesis_trust_unformed")),
        _clean(meta.get("dominant_hypothesis_trust_key", "-")),
        f"{float(meta.get('dominant_hypothesis_trust_score', 0.0) or 0.0):.4f}",
        f"{float(meta.get('structure_quality', felt.get('structure_quality', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('context_confidence', felt.get('context_confidence', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('structure_orientation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('structure_orientation_gap', 0.0) or 0.0):.4f}",
        f"{float(meta.get('structure_action_bearing', 0.0) or 0.0):.4f}",
        f"{float(meta.get('structure_action_gap', 0.0) or 0.0):.4f}",
        f"{float(meta.get('structure_action_uncertainty', 0.0) or 0.0):.4f}",
        f"{float(meta.get('known_form_support', 0.0) or 0.0):.4f}",
        f"{float(meta.get('route_familiarity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('semantic_shift_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('transfer_bearing', 0.0) or 0.0):.4f}",
        f"{float(meta.get('interpretation_quality', 0.0) or 0.0):.4f}",
        _clean(meta.get("adaptation_phase", "-")),
        f"{float(meta.get('trust_transfer_base', 0.0) or 0.0):.4f}",
        f"{float(meta.get('trust_transfer_support', 0.0) or 0.0):.4f}",
        f"{float(meta.get('transfer_maturity_gap', 0.0) or 0.0):.4f}",
        _clean(meta.get("trust_transfer_mode", "-")),
        f"{float(meta.get('transfer_break_fatigue', 0.0) or 0.0):.4f}",
        f"{float(meta.get('transfer_recovery_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('transfer_break_trigger', 0.0) or 0.0):.4f}",
        int(bool(meta.get("transfer_break_ready", False))),
        _clean(memory_state.get("context_cluster_negative_source", "-")),
        _clean(memory_state.get("context_cluster_id", result.get("context_cluster_id", "-"))),
        int(_num("context_cluster_seen")),
        f"{_num('context_cluster_score'):.4f}",
        f"{_num('context_cluster_hit_ratio'):.4f}",
        f"{_num('context_cluster_loss_ratio'):.4f}",
        f"{_num('context_cluster_cancel_timeout_ratio'):.4f}",
        _clean(memory_state.get("context_cluster_negative_evidence", "-")),
        f"{_num('context_cluster_quality', default=float(result.get('context_cluster_quality', 0.0) or 0.0)):.4f}",
        f"{_num('context_cluster_distance', default=float(result.get('context_cluster_distance', 0.0) or 0.0)):.4f}",
        f"{_num('context_cluster_trust'):.4f}",
        f"{_num('context_cluster_variance'):.4f}",
        _clean(memory_state.get("signature_key", result.get("signature_key", "-"))),
        int(_num("signature_seen")),
        f"{_num('signature_score'):.4f}",
        f"{_num('signature_hit_ratio'):.4f}",
        f"{_num('signature_quality', default=float(result.get('signature_quality', 0.0) or 0.0)):.4f}",
        f"{_num('signature_distance', default=float(result.get('signature_distance', 0.0) or 0.0)):.4f}",
        f"{float(active_context_trace.get('activation', 0.0) or 0.0):.4f}",
        f"{float(active_context_trace.get('support', 0.0) or 0.0):.4f}",
        f"{float(active_context_trace.get('conflict', 0.0) or 0.0):.4f}",
        f"{float(active_context_trace.get('bearing', 0.0) or 0.0):.4f}",
        _clean(active_context_trace.get("context_modulation_label", "unmodulated_context")),
        f"{float(meta.get('action_clearance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('action_inhibition', 0.0) or 0.0):.4f}",
        f"{float(meta.get('decision_readiness', thought.get('decision_readiness', 0.0)) or 0.0):.4f}",
        f"{float(processing.get('processing_load', 0.0) or 0.0):.4f}",
        f"{float(thought.get('thought_areal_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('field_perception_clarity', processing.get('field_perception_clarity', 0.0)) or 0.0):.4f}",
    ]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    line = ";".join(str(item) for item in row) + "\n"
    dbr_append_text(
        path,
        line,
        operation="memory_thinking_protocol_append",
        extra=f"phase={phase}|reason={reason}|effect={memory_state.get('memory_effect_on_phase', 'neutral')}",
    )
    return dict(protocol)

def _record_form_symbol_protocol(bot, runtime_result, meta_regulation_state=None, processing_state=None, felt_state=None):

    if bot is None:
        return None

    if not bool(getattr(Config, "MCM_FORM_SYMBOL_PROTOCOL_DEBUG", True)):
        return None

    result = dict(runtime_result or {})
    meta = dict(meta_regulation_state or result.get("meta_regulation_state", {}) or {})
    processing = dict(processing_state or result.get("processing_state", {}) or {})
    felt = dict(felt_state or result.get("felt_state", {}) or {})
    form_state = dict(result.get("form_symbol_state", getattr(bot, "form_symbol_state", {}) or {}) or {})

    symbol_id = str(form_state.get("form_symbol_id", "-") or "-").strip()
    if not symbol_id or symbol_id == "-":
        return None

    phase = str(meta.get("pre_action_phase", "hold") or "hold").strip().lower()
    reason = str(meta.get("rejection_reason", result.get("rejection_reason", "-")) or "-").strip()
    proposed_decision = str(meta.get("decision", result.get("decision", "WAIT")) or "WAIT").strip().upper()
    runtime_tick = int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0)
    timestamp = result.get("timestamp", getattr(bot, "current_timestamp", None))

    zoom_need = float(form_state.get("form_symbol_zoom_need", 0.0) or 0.0)
    zoom_bucket = int(max(0, min(10, round(zoom_need * 10.0))))
    protocol = dict(getattr(bot, "mcm_form_symbol_protocol", {}) or {})
    prior_key = str(protocol.get("last_key", "") or "")
    key = f"{symbol_id}|{phase}|{reason}|z{zoom_bucket}"
    first_event = not bool(prior_key)
    changed = bool(first_event or prior_key != key)
    every_n = max(1, int(getattr(Config, "MCM_FORM_SYMBOL_PROTOCOL_EVERY_N", 5) or 5))
    sequence = int(protocol.get("sequence", 0) or 0) + 1

    protocol.update({
        "sequence": int(sequence),
        "last_key": str(key),
        "last_symbol_id": str(symbol_id),
        "last_phase": str(phase),
        "last_reason": str(reason),
        "last_zoom_bucket": int(zoom_bucket),
        "last_timestamp": timestamp,
        "last_runtime_tick": int(runtime_tick),
    })
    setattr(bot, "mcm_form_symbol_protocol", dict(protocol))

    if not changed and (sequence % every_n) != 0:
        return dict(protocol)

    path = dbr_path("mcm_form_symbol_protocol.csv")
    if path not in _FORM_SYMBOL_PROTOCOL_HEADER_DONE:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header_text = (
            "timestamp;runtime_tick;sequence;phase;reason;decision;"
            "form_symbol_id;form_symbol_family_key;form_symbol_variant_key;"
            "form_symbol_scope;form_symbol_abstraction_level;form_symbol_resolution_quality;form_symbol_detail_pressure;"
            "form_symbol_object_distance;form_symbol_containment;form_symbol_field_decoupling;"
            "form_symbol_development_quality;form_symbol_action_affinity;form_symbol_observation_affinity;"
            "form_symbol_reframe_potential;form_symbol_action_binding;form_symbol_observation_binding;form_symbol_reframe_binding;"
            "form_symbol_learning_trust;form_symbol_action_trust;form_symbol_caution_trust;"
            "form_symbol_contact_maturity;form_symbol_contact_utility;form_symbol_contact_pain_memory;"
            "form_symbol_contact_carefulness;form_symbol_contact_burden_evidence;"
            "form_symbol_contact_utility_evidence;form_symbol_contact_learning_state;"
            "form_symbol_memory_loaded;form_symbol_memory_symbol_count;"
            "form_symbol_seen;form_symbol_maturity;form_symbol_stability;"
            "form_symbol_resonance;form_symbol_load_reduction;form_symbol_zoom_need;"
            "form_symbol_split_pressure;form_symbol_merge_pressure;form_symbol_bearing;"
            "form_symbol_fragility;form_symbol_relevance;form_symbol_novelty;form_symbol_distance;"
            "uncertain_form_family_state;uncertain_form_exposure;uncertainty_familiarity;"
            "variant_similarity;variant_spread;variant_learning_pressure;variant_bearing_memory;"
            "form_symbol_semantic_density;form_symbol_semantic_compression;form_symbol_semantic_coherence;"
            "form_symbol_semantic_learning_need;form_symbol_semantic_action_nearness;"
            "form_symbol_semantic_primary_layer;form_symbol_semantic_layer_count;"
            "form_symbol_semantic_packet_state;form_symbol_semantic_profile;"
            "form_symbol_compound_id;form_symbol_compound_scope;form_symbol_compound_seen;"
            "form_symbol_compound_maturity;form_symbol_compound_stability;form_symbol_compound_resonance;"
            "form_symbol_compound_bearing;form_symbol_compound_load_reduction;form_symbol_compound_novelty;"
            "form_symbol_compound_development_quality;form_symbol_compound_action_affinity;"
            "form_symbol_compound_observation_affinity;form_symbol_compound_reframe_potential;"
            "form_symbol_compound_learning_trust;form_symbol_compound_action_trust;form_symbol_compound_caution_trust;"
            "form_symbol_compound_contact_maturity;form_symbol_compound_contact_utility;"
            "form_symbol_compound_contact_pain_memory;form_symbol_compound_contact_carefulness;"
            "form_symbol_compound_contact_burden_evidence;form_symbol_compound_contact_utility_evidence;"
            "form_symbol_compound_contact_learning_state;"
            "form_symbol_memory_compound_count;"
            "structure_quality;context_confidence;field_clarity;field_pressure;field_fragmentation\n"
        )
        write_start = time.perf_counter()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header_text)
        dbr_file_write_profile(
            path,
            (time.perf_counter() - write_start) * 1000.0,
            bytes_written=len(header_text.encode("utf-8")),
            operation="form_symbol_protocol_header",
        )
        _FORM_SYMBOL_PROTOCOL_HEADER_DONE.add(path)

    def _clean(value):
        return str(value).replace("\n", " ").replace(";", "|")

    def _num(key, default=0.0):
        try:
            return float(form_state.get(key, default) or default)
        except Exception:
            return float(default)

    row = [
        _clean(timestamp),
        int(runtime_tick),
        int(sequence),
        _clean(phase),
        _clean(reason),
        _clean(proposed_decision),
        _clean(symbol_id),
        _clean(form_state.get("form_symbol_family_key", form_state.get("form_symbol_key", ""))),
        _clean(form_state.get("form_symbol_variant_key", "")),
        _clean(form_state.get("form_symbol_scope", "")),
        int(_num("form_symbol_abstraction_level")),
        f"{_num('form_symbol_resolution_quality'):.4f}",
        f"{_num('form_symbol_detail_pressure'):.4f}",
        f"{_num('form_symbol_object_distance'):.4f}",
        f"{_num('form_symbol_containment'):.4f}",
        f"{_num('form_symbol_field_decoupling'):.4f}",
        f"{_num('form_symbol_development_quality'):.4f}",
        f"{_num('form_symbol_action_affinity', 0.50):.4f}",
        f"{_num('form_symbol_observation_affinity'):.4f}",
        f"{_num('form_symbol_reframe_potential'):.4f}",
        f"{_num('form_symbol_action_binding', 0.50):.4f}",
        f"{_num('form_symbol_observation_binding'):.4f}",
        f"{_num('form_symbol_reframe_binding'):.4f}",
        f"{_num('form_symbol_learning_trust'):.4f}",
        f"{_num('form_symbol_action_trust'):.4f}",
        f"{_num('form_symbol_caution_trust'):.4f}",
        f"{_num('form_symbol_contact_maturity'):.4f}",
        f"{_num('form_symbol_contact_utility'):.4f}",
        f"{_num('form_symbol_contact_pain_memory'):.4f}",
        f"{_num('form_symbol_contact_carefulness'):.4f}",
        f"{_num('form_symbol_contact_burden_evidence'):.4f}",
        f"{_num('form_symbol_contact_utility_evidence'):.4f}",
        _clean(form_state.get("form_symbol_contact_learning_state", "unformed_contact")),
        int(bool(form_state.get("form_symbol_memory_loaded", False))),
        int(_num("form_symbol_memory_symbol_count")),
        int(_num("form_symbol_seen")),
        f"{_num('form_symbol_maturity'):.4f}",
        f"{_num('form_symbol_stability'):.4f}",
        f"{_num('form_symbol_resonance'):.4f}",
        f"{_num('form_symbol_load_reduction'):.4f}",
        f"{_num('form_symbol_zoom_need'):.4f}",
        f"{_num('form_symbol_split_pressure'):.4f}",
        f"{_num('form_symbol_merge_pressure'):.4f}",
        f"{_num('form_symbol_bearing'):.4f}",
        f"{_num('form_symbol_fragility'):.4f}",
        f"{_num('form_symbol_relevance'):.4f}",
        f"{_num('form_symbol_novelty'):.4f}",
        f"{_num('form_symbol_distance'):.4f}",
        _clean(form_state.get("uncertain_form_family_state", "quiet_form_family")),
        f"{_num('uncertain_form_exposure'):.4f}",
        f"{_num('uncertainty_familiarity'):.4f}",
        f"{_num('variant_similarity'):.4f}",
        f"{_num('variant_spread'):.4f}",
        f"{_num('variant_learning_pressure'):.4f}",
        f"{_num('variant_bearing_memory'):.4f}",
        f"{_num('form_symbol_semantic_density'):.4f}",
        f"{_num('form_symbol_semantic_compression'):.4f}",
        f"{_num('form_symbol_semantic_coherence'):.4f}",
        f"{_num('form_symbol_semantic_learning_need'):.4f}",
        f"{_num('form_symbol_semantic_action_nearness'):.4f}",
        _clean(form_state.get("form_symbol_semantic_primary_layer", "")),
        int(_num("form_symbol_semantic_layer_count")),
        _clean(form_state.get("form_symbol_semantic_packet_state", "")),
        _clean(form_state.get("form_symbol_semantic_profile", "")),
        _clean(form_state.get("form_symbol_compound_id", "-")),
        _clean(form_state.get("form_symbol_compound_scope", "single")),
        int(_num("form_symbol_compound_seen")),
        f"{_num('form_symbol_compound_maturity'):.4f}",
        f"{_num('form_symbol_compound_stability'):.4f}",
        f"{_num('form_symbol_compound_resonance'):.4f}",
        f"{_num('form_symbol_compound_bearing'):.4f}",
        f"{_num('form_symbol_compound_load_reduction'):.4f}",
        f"{_num('form_symbol_compound_novelty'):.4f}",
        f"{_num('form_symbol_compound_development_quality'):.4f}",
        f"{_num('form_symbol_compound_action_affinity', 0.50):.4f}",
        f"{_num('form_symbol_compound_observation_affinity'):.4f}",
        f"{_num('form_symbol_compound_reframe_potential'):.4f}",
        f"{_num('form_symbol_compound_learning_trust'):.4f}",
        f"{_num('form_symbol_compound_action_trust'):.4f}",
        f"{_num('form_symbol_compound_caution_trust'):.4f}",
        f"{_num('form_symbol_compound_contact_maturity'):.4f}",
        f"{_num('form_symbol_compound_contact_utility'):.4f}",
        f"{_num('form_symbol_compound_contact_pain_memory'):.4f}",
        f"{_num('form_symbol_compound_contact_carefulness'):.4f}",
        f"{_num('form_symbol_compound_contact_burden_evidence'):.4f}",
        f"{_num('form_symbol_compound_contact_utility_evidence'):.4f}",
        _clean(form_state.get("form_symbol_compound_contact_learning_state", "unformed_contact")),
        int(_num("form_symbol_memory_compound_count")),
        f"{float(meta.get('structure_quality', felt.get('structure_quality', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('context_confidence', felt.get('context_confidence', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('field_perception_clarity', processing.get('field_perception_clarity', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('field_perception_pressure', processing.get('field_perception_pressure', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('field_perception_fragmentation', processing.get('field_perception_fragmentation', 0.0)) or 0.0):.4f}",
    ]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    line = ";".join(str(item) for item in row) + "\n"
    dbr_append_text(
        path,
        line,
        operation="form_symbol_protocol_append",
        extra=f"symbol={symbol_id}|phase={phase}|zoom={zoom_bucket}",
    )
    return dict(protocol)

from core.form_language import _build_dio_form_language_state

def _build_thought_seed_state(runtime_result, meta_regulation_state=None, processing_state=None, felt_state=None, thought_state=None):
    result = dict(runtime_result or {})
    meta = dict(meta_regulation_state or result.get("meta_regulation_state", {}) or {})
    processing = dict(processing_state or result.get("processing_state", {}) or {})
    felt = dict(felt_state or result.get("felt_state", {}) or {})
    thought = dict(thought_state or result.get("thought_state", {}) or {})
    form_state = dict(result.get("form_symbol_state", meta.get("form_symbol_state", {}) or {}) or {})
    strategic = dict(result.get("strategic_window_state", meta.get("strategic_window_state", {}) or {}) or {})
    active_contact = dict(result.get("active_mcm_contact_state", meta.get("active_mcm_contact", {}) or {}) or {})

    def _clip(value, lo=0.0, hi=1.0):
        try:
            value = float(value)
        except Exception:
            value = 0.0
        if value != value:
            value = 0.0
        return max(float(lo), min(float(hi), float(value)))

    def _clean(value):
        return str(value).replace("\n", " ").replace(";", "|").strip()

    def _field(*keys, default=0.0):
        for source in (meta, active_contact, strategic, form_state, thought, felt, processing, result):
            for key in keys:
                if isinstance(source, dict) and key in source:
                    return _clip(source.get(key, default))
        return _clip(default)

    decision = _clean(result.get("proposed_decision", result.get("decision", meta.get("decision", "WAIT")) or "WAIT")).upper()
    phase = _clean(meta.get("pre_action_phase", result.get("decision_tendency", "hold")) or "hold").lower()
    reason = _clean(meta.get("rejection_reason", result.get("rejection_reason", "-")) or "-")
    rr_value = max(0.0, float(result.get("rr_value", 0.0) or 0.0))
    rr_norm = _clip(rr_value / 4.0)

    structure_quality = _field("structure_quality")
    context_confidence = _field("context_confidence")
    field_action_support = _field("field_action_support")
    field_observation_need = _field("field_observation_need")
    field_replan_pressure = _field("field_replan_pressure")
    action_clearance = _field("action_clearance")
    action_inhibition = _field("action_inhibition")
    decision_readiness = _field("decision_readiness")
    decision_strength = _field("decision_strength")
    future_projection_depth = _field("future_projection_depth")
    mcm_spacetime_depth = _field("mcm_spacetime_depth")
    spacetime_unlocated_pressure = _field("spacetime_unlocated_pressure")
    area_bearing_quality = _field("area_bearing_quality")
    area_spacetime_fit = _field("area_spacetime_fit")
    contact_reality_check = _field("contact_reality_check")
    contact_temporal_bearing = _field("contact_temporal_bearing")
    contact_regime_mismatch = _field("contact_regime_mismatch")
    emotional_decoupling = _field("emotional_decoupling")
    regulation_load = _field("regulatory_second_order_load", "neurochemical_load", "processing_load")
    rumination_depth = _field("rumination_depth")
    field_pressure = _field("field_perception_pressure", "felt_pressure")
    field_clarity = _field("field_perception_clarity")
    form_maturity = _field("form_symbol_maturity")
    form_stability = _field("form_symbol_stability")
    form_novelty = _field("form_symbol_novelty", default=1.0)
    form_action_binding = _field("form_symbol_action_binding", "form_symbol_action_affinity")
    form_learning_trust = _field("form_symbol_learning_trust")
    form_contact_utility = _field("form_symbol_contact_utility")
    form_contact_utility_evidence = _field("form_symbol_contact_utility_evidence")
    form_contact_pain_memory = _field("form_symbol_contact_pain_memory")
    form_contact_burden_evidence = _field("form_symbol_contact_burden_evidence")
    memory_support = _field("memory_support")
    memory_conflict = _field("memory_conflict")
    entry_choice_bearing = _field("entry_choice_bearing")
    target_conviction = _field("target_conviction")
    target_recovery_confirmation = _field("target_recovery_confirmation")
    previous_packet_process_reward = _field("previous_packet_process_reward")
    previous_packet_reorganization_need = _field("previous_packet_reorganization_need")
    previous_constructive_stimulation = _field("previous_constructive_stimulation")
    previous_open_hypothesis_learning_state = _clean(meta.get("previous_open_hypothesis_learning_state", "-") or "-")
    previous_open_hypothesis_reorganization_posture = _clean(meta.get("previous_open_hypothesis_reorganization_posture", "-") or "-")
    previous_open_hypothesis_replay_need = _field("previous_open_hypothesis_replay_need")
    previous_open_hypothesis_distance_need = _field("previous_open_hypothesis_distance_need")
    previous_open_hypothesis_reinterpretation_need = _field("previous_open_hypothesis_reinterpretation_need")
    previous_open_hypothesis_consequence_score = _field("previous_open_hypothesis_consequence_score")
    previous_open_hypothesis_burden_score = _field("previous_open_hypothesis_burden_score")
    previous_open_hypothesis_reorganization_score = _field("previous_open_hypothesis_reorganization_score")
    semantic_origin_state = _clean(meta.get("semantic_origin_state", "unlocated_semantic_contact") or "unlocated_semantic_contact")
    own_field_identity_strength = _field("own_field_identity_strength")
    foreign_semantic_pressure = _field("foreign_semantic_pressure")
    adopted_language_pressure = _field("adopted_language_pressure")
    self_foreign_boundary_clarity = _field("self_foreign_boundary_clarity")
    semantic_origin_conflict = _field("semantic_origin_conflict")
    own_vs_foreign_margin = max(-1.0, min(1.0, float(meta.get("own_vs_foreign_margin", own_field_identity_strength - foreign_semantic_pressure) or 0.0)))
    borrowed_vs_own_margin = max(-1.0, min(1.0, float(meta.get("borrowed_vs_own_margin", adopted_language_pressure - own_field_identity_strength) or 0.0)))
    boundary_support_margin = max(-1.0, min(1.0, float(meta.get("boundary_support_margin", self_foreign_boundary_clarity - semantic_origin_conflict) or 0.0)))
    consequence_echo = _clip(
        (previous_packet_process_reward * 0.34)
        + (previous_constructive_stimulation * 0.24)
        + (form_contact_utility_evidence * 0.14)
        + (form_contact_utility * 0.10)
        + (memory_support * 0.08)
        + (target_recovery_confirmation * 0.08)
        - (previous_packet_reorganization_need * 0.18)
        - (form_contact_burden_evidence * 0.08)
    )
    reorganization_echo = _clip(
        (previous_packet_reorganization_need * 0.36)
        + (form_contact_pain_memory * 0.18)
        + (form_contact_burden_evidence * 0.16)
        + (memory_conflict * 0.12)
        + (contact_regime_mismatch * 0.10)
        + (spacetime_unlocated_pressure * 0.08)
        - (previous_packet_process_reward * 0.12)
    )

    structure_reading = _clip(
        (_clip((rr_value - 1.6) / 3.2) * 0.18)
        + (area_bearing_quality * 0.16)
        + (future_projection_depth * 0.15)
        + (mcm_spacetime_depth * 0.13)
        + (structure_quality * 0.12)
        + (context_confidence * 0.09)
        + (entry_choice_bearing * 0.10)
        + (contact_temporal_bearing * 0.09)
        + (contact_reality_check * 0.08)
        + (form_maturity * 0.04)
        - (spacetime_unlocated_pressure * 0.10)
        - (contact_regime_mismatch * 0.08)
    )
    thought_confirmation_score = _clip(
        (structure_reading * 0.34)
        + (area_spacetime_fit * 0.12)
        + (entry_choice_bearing * 0.11)
        + (target_conviction * 0.09)
        + (target_recovery_confirmation * 0.07)
        + (field_action_support * 0.07)
        + (contact_reality_check * 0.06)
        + (form_action_binding * 0.05)
        + (form_learning_trust * 0.04)
        + (form_contact_utility * 0.04)
        + (form_contact_utility_evidence * 0.04)
        + (consequence_echo * 0.08)
        - (form_contact_pain_memory * 0.05)
        - (form_contact_burden_evidence * 0.05)
        - (contact_regime_mismatch * 0.04)
        - (reorganization_echo * 0.05)
    )
    reality_binding_score = _clip(
        (thought_confirmation_score * 0.22)
        + (contact_reality_check * 0.18)
        + (area_spacetime_fit * 0.15)
        + (context_confidence * 0.12)
        + (field_clarity * 0.09)
        + (form_stability * 0.08)
        + (memory_support * 0.07)
        + (emotional_decoupling * 0.05)
        + (action_clearance * 0.04)
        + (consequence_echo * 0.05)
        - (memory_conflict * 0.08)
        - (spacetime_unlocated_pressure * 0.07)
        - (reorganization_echo * 0.04)
    )
    thought_trace_strength = _clip(
        (structure_reading * 0.42)
        + (decision_strength * 0.14)
        + (future_projection_depth * 0.12)
        + (field_pressure * 0.10)
        + (rr_norm * 0.09)
        + (form_novelty * 0.05)
        + (field_observation_need * 0.05)
        + (field_replan_pressure * 0.03)
    )
    thought_maturity = _clip(
        (reality_binding_score * 0.36)
        + (structure_reading * 0.22)
        + (field_action_support * 0.12)
        + (decision_readiness * 0.10)
        + (form_maturity * 0.10)
        + (contact_temporal_bearing * 0.10)
        + (consequence_echo * 0.07)
        - (action_inhibition * 0.10)
        - (reorganization_echo * 0.05)
    )
    thought_consequence_alignment = _clip(
        (thought_confirmation_score * 0.26)
        + (reality_binding_score * 0.22)
        + (thought_maturity * 0.18)
        + (consequence_echo * 0.18)
        + (structure_reading * 0.12)
        - (reorganization_echo * 0.12)
    )
    thought_consequence_balance = max(-1.0, min(1.0, float(consequence_echo - reorganization_echo)))
    thought_reality_lag = _clip(
        (max(0.0, structure_reading - thought_confirmation_score) * 0.46)
        + (max(0.0, thought_maturity - reality_binding_score) * 0.20)
        + (max(0.0, reorganization_echo - consequence_echo) * 0.18)
        + (max(0.0, field_pressure - field_clarity) * 0.10)
        + (memory_conflict * 0.06)
    )
    thought_structural_grounding = _clip(
        (area_spacetime_fit * 0.18)
        + (contact_reality_check * 0.16)
        + (entry_choice_bearing * 0.14)
        + (target_recovery_confirmation * 0.12)
        + (form_stability * 0.10)
        + (memory_support * 0.08)
        + (emotional_decoupling * 0.08)
        + (field_clarity * 0.06)
        + (consequence_echo * 0.06)
        - (spacetime_unlocated_pressure * 0.10)
        - (contact_regime_mismatch * 0.10)
        - (reorganization_echo * 0.08)
        - (memory_conflict * 0.06)
    )
    thought_open_hypothesis_pressure = _clip(
        (rr_norm * 0.20)
        + (structure_reading * 0.18)
        + (max(0.0, 0.48 - thought_structural_grounding) * 0.22)
        + (max(0.0, reorganization_echo - consequence_echo) * 0.16)
        + (thought_reality_lag * 0.14)
        + (action_inhibition * 0.10)
    )
    borrowed_open_hypothesis_pressure = _clip(
        ((1.0 if semantic_origin_state == "borrowed_analogy_watch" else 0.0) * 0.34)
        + (max(0.0, borrowed_vs_own_margin) * 0.28)
        + (adopted_language_pressure * 0.18)
        + (semantic_origin_conflict * 0.14)
        + (max(0.0, 0.0 - boundary_support_margin) * 0.12)
        + (thought_open_hypothesis_pressure * 0.10)
        - (own_field_identity_strength * 0.08)
        - (self_foreign_boundary_clarity * 0.06)
    )
    own_field_binding_pull = _clip(
        (own_field_identity_strength * 0.30)
        + (self_foreign_boundary_clarity * 0.22)
        + (max(0.0, own_vs_foreign_margin) * 0.18)
        + (form_learning_trust * 0.10)
        + (memory_support * 0.08)
        + (emotional_decoupling * 0.06)
        - (adopted_language_pressure * 0.10)
        - (semantic_origin_conflict * 0.08)
    )
    thought_recall_potential = _clip(
        (thought_trace_strength * 0.36)
        + (form_stability * 0.17)
        + (memory_support * 0.14)
        + (mcm_spacetime_depth * 0.13)
        + (contact_temporal_bearing * 0.10)
        + (field_clarity * 0.10)
    )
    hallucination_drift_risk = _clip(
        (thought_trace_strength * 0.24)
        + (spacetime_unlocated_pressure * 0.22)
        + (form_novelty * 0.12)
        + (memory_conflict * 0.12)
        + (max(0.0, 0.42 - reality_binding_score) * 0.36)
        - (contact_reality_check * 0.10)
        - (emotional_decoupling * 0.08)
    )
    overthinking_risk = _clip(
        (rumination_depth * 0.28)
        + (regulation_load * 0.20)
        + (field_replan_pressure * 0.16)
        + (field_observation_need * 0.12)
        + (action_inhibition * 0.12)
        + (max(0.0, thought_trace_strength - thought_maturity) * 0.12)
    )
    thought_replay_maturation_pull = _clip(
        previous_open_hypothesis_replay_need
        + (0.18 if previous_open_hypothesis_reorganization_posture == "replay_dominant" else 0.0)
        + (0.10 if previous_open_hypothesis_learning_state == "open_hypothesis_carried" else 0.0)
        + (previous_open_hypothesis_consequence_score * 0.08)
        - (previous_open_hypothesis_burden_score * 0.06)
    )
    thought_distance_maturation_pull = _clip(
        previous_open_hypothesis_distance_need
        + (0.14 if previous_open_hypothesis_reorganization_posture == "distance_dominant" else 0.0)
        + (0.10 if previous_open_hypothesis_learning_state in ("open_hypothesis_burdened", "open_hypothesis_reorganizing") else 0.0)
        + (previous_open_hypothesis_burden_score * 0.08)
        + (borrowed_open_hypothesis_pressure * 0.08)
    )
    thought_reinterpretation_pull = _clip(
        previous_open_hypothesis_reinterpretation_need
        + (0.18 if previous_open_hypothesis_reorganization_posture == "reinterpretation_dominant" else 0.0)
        + (previous_open_hypothesis_reorganization_score * 0.12)
        + (max(0.0, previous_open_hypothesis_burden_score - previous_open_hypothesis_consequence_score) * 0.08)
        + (borrowed_open_hypothesis_pressure * 0.12)
        - (own_field_binding_pull * 0.04)
    )
    thought_digestive_replay_pull = _clip(
        (previous_open_hypothesis_replay_need * 0.24)
        + (previous_open_hypothesis_reinterpretation_need * 0.18)
        + (previous_open_hypothesis_reorganization_score * 0.18)
        + (thought_open_hypothesis_pressure * 0.12)
        + (max(0.0, reorganization_echo - consequence_echo) * 0.12)
        + (thought_reality_lag * 0.10)
        - (thought_confirmation_score * 0.08)
    )
    thought_digestive_distance_pull = _clip(
        (previous_open_hypothesis_distance_need * 0.26)
        + (previous_open_hypothesis_burden_score * 0.18)
        + (max(0.0, previous_open_hypothesis_burden_score - previous_open_hypothesis_consequence_score) * 0.16)
        + (borrowed_open_hypothesis_pressure * 0.10)
        + (hallucination_drift_risk * 0.08)
        - (reality_binding_score * 0.08)
    )
    thought_digestive_integration_pull = _clip(
        (thought_digestive_replay_pull * 0.24)
        + (thought_digestive_distance_pull * 0.16)
        + (thought_reinterpretation_pull * 0.16)
        + (thought_structural_grounding * 0.14)
        + (reality_binding_score * 0.12)
        + (own_field_binding_pull * 0.08)
        - (hallucination_drift_risk * 0.08)
        - (overthinking_risk * 0.06)
    )
    thought_digestive_returned_trust = _clip(
        (previous_open_hypothesis_consequence_score * 0.20)
        + (thought_confirmation_score * 0.18)
        + (thought_digestive_integration_pull * 0.14)
        + (reality_binding_score * 0.14)
        + (thought_structural_grounding * 0.12)
        + (max(0.0, previous_open_hypothesis_replay_need - previous_open_hypothesis_distance_need) * 0.08)
        - (previous_open_hypothesis_burden_score * 0.10)
        - (previous_open_hypothesis_reorganization_score * 0.08)
    )
    trust_return_readiness = _clip(
        (thought_digestive_returned_trust * 0.34)
        + (thought_confirmation_score * 0.20)
        + (reality_binding_score * 0.16)
        + (thought_digestive_integration_pull * 0.12)
        + (thought_structural_grounding * 0.10)
        - (thought_digestive_distance_pull * 0.05)
        - (previous_open_hypothesis_burden_score * 0.05)
    )
    if (
        thought_digestive_returned_trust >= 0.25
        and trust_return_readiness >= 0.28
        and reality_binding_score >= 0.30
        and thought_confirmation_score >= 0.22
        and previous_open_hypothesis_burden_score < 0.46
    ):
        thought_digest_state = "digestive_trust_return"
    elif (
        thought_digestive_returned_trust >= 0.21
        and trust_return_readiness >= 0.24
        and reality_binding_score >= 0.28
        and thought_confirmation_score >= 0.18
    ):
        thought_digest_state = "digestive_trust_emergence"
    elif thought_digestive_integration_pull >= 0.34 and thought_digestive_integration_pull >= max(thought_digestive_replay_pull, thought_digestive_distance_pull):
        thought_digest_state = "digestive_integration"
    elif thought_digestive_distance_pull >= 0.32 and thought_digestive_distance_pull >= thought_digestive_replay_pull:
        thought_digest_state = "digestive_distance"
    elif thought_digestive_replay_pull >= 0.30:
        thought_digest_state = "digestive_replay"
    else:
        thought_digest_state = "digestive_quiet"
    if max(thought_replay_maturation_pull, thought_distance_maturation_pull, thought_reinterpretation_pull) < 0.22:
        thought_reifung_direction = "no_previous_open_hypothesis_trace"
    elif thought_reinterpretation_pull >= thought_replay_maturation_pull and thought_reinterpretation_pull >= thought_distance_maturation_pull:
        thought_reifung_direction = "reinterpretation_maturation"
    elif thought_replay_maturation_pull >= thought_distance_maturation_pull:
        thought_reifung_direction = "replay_maturation"
    else:
        thought_reifung_direction = "distance_maturation"

    if (
        thought_confirmation_score >= 0.52
        and thought_maturity >= 0.44
        and reality_binding_score >= 0.40
    ) or (
        thought_consequence_alignment >= 0.46
        and thought_maturity >= 0.44
        and reality_binding_score >= 0.39
        and reorganization_echo < 0.42
    ):
        seed_metaregulator_state = "seed_action_ready"
    elif hallucination_drift_risk >= 0.58 and reality_binding_score < 0.44:
        seed_metaregulator_state = "seed_drift_watch"
    elif overthinking_risk >= 0.58 and thought_maturity < 0.50:
        seed_metaregulator_state = "seed_overthinking_watch"
    elif thought_digestive_integration_pull >= 0.38 and thought_digestive_returned_trust < 0.28:
        seed_metaregulator_state = "seed_digest"
    elif field_replan_pressure >= 0.48 or phase == "replan":
        seed_metaregulator_state = "seed_replay"
    elif borrowed_open_hypothesis_pressure >= 0.42 and thought_open_hypothesis_pressure >= 0.34:
        seed_metaregulator_state = "seed_reinterpret"
    elif thought_reinterpretation_pull >= 0.46:
        seed_metaregulator_state = "seed_reinterpret"
    elif thought_replay_maturation_pull >= 0.44:
        seed_metaregulator_state = "seed_replay"
    elif thought_maturity >= 0.44 and reality_binding_score >= 0.38:
        seed_metaregulator_state = "seed_mature"
    elif thought_trace_strength >= 0.44 and field_observation_need >= 0.36:
        seed_metaregulator_state = "seed_focus"
    elif thought_trace_strength >= 0.34:
        seed_metaregulator_state = "seed_store"
    else:
        seed_metaregulator_state = "seed_release"

    emergent_structure_state = "ordinary_structure_reading"
    if (
        structure_reading >= 0.52
        and thought_confirmation_score >= 0.50
        and reality_binding_score >= 0.38
    ) or (
        structure_reading >= 0.50
        and thought_consequence_alignment >= 0.46
        and reality_binding_score >= 0.38
        and reorganization_echo < 0.42
    ):
        emergent_structure_state = "confirmed_structural_interpretation"
    elif structure_reading >= 0.44 and rr_value >= 2.4:
        emergent_structure_state = "open_structural_hypothesis"
    elif rr_value >= 2.4 and structure_reading < 0.34:
        emergent_structure_state = "wide_target_without_structure"

    basis = "|".join(
        [
            _clean(decision),
            _clean(phase),
            _clean(emergent_structure_state),
            _clean(form_state.get("form_symbol_id", result.get("form_symbol_id", "-")) or "-"),
            _clean(result.get("context_cluster_id", "-") or "-"),
            f"{round(structure_reading, 2):.2f}",
            f"{round(reality_binding_score, 2):.2f}",
        ]
    )
    thought_seed_id = "ts_" + hashlib.sha1(basis.encode("utf-8", errors="ignore")).hexdigest()[:10]
    thought_seed_label = "_".join(
        item
        for item in (
            "seed",
            emergent_structure_state.replace("_structural_", "_").replace("_interpretation", ""),
            seed_metaregulator_state.replace("seed_", ""),
        )
        if item
    )

    seed_state = {
        "thought_seed_id": str(thought_seed_id),
        "thought_seed_label": str(thought_seed_label),
        "thought_trace_strength": float(thought_trace_strength),
        "thought_recall_potential": float(thought_recall_potential),
        "thought_maturity": float(thought_maturity),
        "reality_binding_score": float(reality_binding_score),
        "thought_confirmation_score": float(thought_confirmation_score),
        "consequence_echo": float(consequence_echo),
        "reorganization_echo": float(reorganization_echo),
        "thought_consequence_alignment": float(thought_consequence_alignment),
        "thought_consequence_balance": float(thought_consequence_balance),
        "thought_reality_lag": float(thought_reality_lag),
        "thought_structural_grounding": float(thought_structural_grounding),
        "thought_open_hypothesis_pressure": float(thought_open_hypothesis_pressure),
        "thought_replay_maturation_pull": float(thought_replay_maturation_pull),
        "thought_distance_maturation_pull": float(thought_distance_maturation_pull),
        "thought_reinterpretation_pull": float(thought_reinterpretation_pull),
        "thought_digestive_replay_pull": float(thought_digestive_replay_pull),
        "thought_digestive_distance_pull": float(thought_digestive_distance_pull),
        "thought_digestive_integration_pull": float(thought_digestive_integration_pull),
        "thought_digestive_returned_trust": float(thought_digestive_returned_trust),
        "trust_return_readiness": float(trust_return_readiness),
        "thought_digest_state": str(thought_digest_state),
        "thought_reifung_direction": str(thought_reifung_direction),
        "semantic_origin_state": str(semantic_origin_state),
        "borrowed_open_hypothesis_pressure": float(borrowed_open_hypothesis_pressure),
        "own_field_binding_pull": float(own_field_binding_pull),
        "own_vs_foreign_margin": float(own_vs_foreign_margin),
        "borrowed_vs_own_margin": float(borrowed_vs_own_margin),
        "boundary_support_margin": float(boundary_support_margin),
        "previous_open_hypothesis_learning_state": str(previous_open_hypothesis_learning_state),
        "previous_open_hypothesis_reorganization_posture": str(previous_open_hypothesis_reorganization_posture),
        "hallucination_drift_risk": float(hallucination_drift_risk),
        "overthinking_risk": float(overthinking_risk),
        "seed_metaregulator_state": str(seed_metaregulator_state),
        "emergent_memory_trace": bool(thought_trace_strength >= 0.34 or emergent_structure_state == "open_structural_hypothesis"),
        "emergent_structure_state": str(emergent_structure_state),
        "emergent_structure_reading": float(structure_reading),
        "form_symbol_anchor": str(form_state.get("form_symbol_id", result.get("form_symbol_id", "-")) or "-"),
        "mcm_field_anchor": str(meta.get("field_perception_label", felt.get("field_perception_label", "-")) or "-"),
        "experience_memory_anchor": str(result.get("context_cluster_id", meta.get("inner_context_cluster_id", "-")) or "-"),
        "outcome_anchor": "pending",
        "decision": str(decision),
        "phase": str(phase),
        "reason": str(reason),
        "rr_value": float(rr_value),
    }
    seed_state.update(_build_dio_form_language_state(
        seed_state,
        form_state=form_state,
        meta_regulation_state=meta,
        runtime_result=result,
    ))
    return dict(seed_state)

from memory.thought_memory_store import (
    _empty_thought_memory_payload,
    _ensure_thought_memory_loaded,
    _flush_thought_memory_if_due,
    _normalize_thought_memory,
    _normalize_thought_memory_families,
    _read_thought_memory,
    _thought_memory_development_state,
    _thought_memory_family_key,
    _thought_memory_path,
    _thought_memory_sentence_state,
    _update_thought_memory,
    _write_thought_memory,
)

def _record_thought_digest_protocol(bot, seed_state, meta_regulation_state=None, timestamp=None, runtime_tick=0):

    if bot is None or not bool(getattr(Config, "MCM_THOUGHT_DIGEST_PROTOCOL_DEBUG", True)):
        return None

    seed = dict(seed_state or {})
    meta = dict(meta_regulation_state or {})
    protocol = dict(getattr(bot, "mcm_thought_digest_protocol", {}) or {})
    sequence = int(protocol.get("sequence", 0) or 0) + 1
    def _quality_bucket(value, step=0.12):
        try:
            value = float(value or 0.0)
        except Exception:
            value = 0.0
        value = max(0.0, min(1.0, value))
        step = max(0.01, float(step or 0.12))
        return f"{round(value / step) * step:.2f}"

    key = "|".join(
        [
            str(seed.get("dio_form_mcm_family_token", "-")),
            str(seed.get("thought_digest_state", "-")),
            str(seed.get("thought_reifung_direction", "-")),
            str(meta.get("open_hypothesis_reifung_state", "-")),
            str(seed.get("phase", "-")),
            _quality_bucket(seed.get("thought_confirmation_score", 0.0)),
            _quality_bucket(seed.get("hypothesis_reality_binding", 0.0)),
            _quality_bucket(meta.get("open_hypothesis_action_permission", 0.0)),
        ]
    )
    prior_key = str(protocol.get("last_key", "") or "")
    changed = bool(key != prior_key)
    every_n = max(1, int(getattr(Config, "MCM_THOUGHT_DIGEST_PROTOCOL_EVERY_N", 5) or 5))
    change_burst = bool(getattr(Config, "MCM_PROTOCOL_CHANGE_BURST_DEBUG", True))
    protocol.update({
        "sequence": int(sequence),
        "last_key": str(key),
        "last_timestamp": timestamp,
        "last_runtime_tick": int(runtime_tick),
        "last_digest_state": str(seed.get("thought_digest_state", "-") or "-"),
    })
    setattr(bot, "mcm_thought_digest_protocol", dict(protocol))

    if (not change_burst or not changed) and (sequence % every_n) != 0:
        return dict(protocol)

    path = dbr_path("mcm_thought_digest_protocol.csv")
    if path not in _THOUGHT_DIGEST_PROTOCOL_HEADER_DONE:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header_text = (
            "timestamp;runtime_tick;sequence;decision;phase;reason;"
            "thought_seed_id;thought_seed_label;seed_metaregulator_state;emergent_structure_state;"
            "thought_digest_state;thought_reifung_direction;"
            "thought_digestive_replay_pull;thought_digestive_distance_pull;"
            "thought_digestive_integration_pull;thought_digestive_returned_trust;"
            "trust_return_readiness;"
            "thought_confirmation_score;thought_open_hypothesis_pressure;thought_reality_lag;"
            "previous_open_hypothesis_learning_state;previous_open_hypothesis_reorganization_posture;"
            "semantic_origin_state;dio_syntax_signature;"
            "dio_form_mcm_token;dio_form_mcm_family_token;dio_form_mcm_syntax_state;form_to_mcm_recall;mcm_to_form_confirmation;"
            "visual_mcm_context_fit;visual_mcm_mismatch;hypothesis_reality_binding;form_mcm_syntax_density;"
            "form_mcm_family_recurrence;form_mcm_family_maturity;form_mcm_family_trust;"
            "form_mcm_family_caution;form_mcm_family_reorganization_need;"
            "open_hypothesis_reifung_state;open_hypothesis_confirmation_weight;"
            "open_hypothesis_learning_charge;open_hypothesis_action_permission;"
            "open_hypothesis_reality_check_need;inner_outer_alignment;"
            "previous_digest_state;previous_trust_return_readiness;previous_digestive_returned_trust;"
            "trust_return_open_hypothesis_load;trust_return_context_instability;"
            "trust_return_motor_contact_strength;trust_return_act_bridge;"
            "trust_return_motor_heat;trust_return_stabilization_need;trust_return_focus_pull;trust_return_motor_mode;"
            "cortisol_load;serotonin_stability;dopamine_drive;mcm_axis_state;mcm_axis_tension;"
            "field_perception_label;form_symbol_anchor;mcm_field_anchor;experience_memory_anchor\n"
        )
        write_start = time.perf_counter()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header_text)
        dbr_file_write_profile(
            path,
            (time.perf_counter() - write_start) * 1000.0,
            bytes_written=len(header_text.encode("utf-8")),
            operation="thought_digest_protocol_header",
        )
        _THOUGHT_DIGEST_PROTOCOL_HEADER_DONE.add(path)

    def _clean(value):
        return str(value).replace("\n", " ").replace(";", "|")

    row = [
        _clean(timestamp),
        int(runtime_tick),
        int(sequence),
        _clean(seed.get("decision", "WAIT")),
        _clean(seed.get("phase", "hold")),
        _clean(seed.get("reason", "-")),
        _clean(seed.get("thought_seed_id", "-")),
        _clean(seed.get("thought_seed_label", "-")),
        _clean(seed.get("seed_metaregulator_state", "seed_release")),
        _clean(seed.get("emergent_structure_state", "ordinary_structure_reading")),
        _clean(seed.get("thought_digest_state", "digestive_quiet")),
        _clean(seed.get("thought_reifung_direction", "no_previous_open_hypothesis_trace")),
        f"{float(seed.get('thought_digestive_replay_pull', 0.0) or 0.0):.4f}",
        f"{float(seed.get('thought_digestive_distance_pull', 0.0) or 0.0):.4f}",
        f"{float(seed.get('thought_digestive_integration_pull', 0.0) or 0.0):.4f}",
        f"{float(seed.get('thought_digestive_returned_trust', 0.0) or 0.0):.4f}",
        f"{float(seed.get('trust_return_readiness', 0.0) or 0.0):.4f}",
        f"{float(seed.get('thought_confirmation_score', 0.0) or 0.0):.4f}",
        f"{float(seed.get('thought_open_hypothesis_pressure', 0.0) or 0.0):.4f}",
        f"{float(seed.get('thought_reality_lag', 0.0) or 0.0):.4f}",
        _clean(seed.get("previous_open_hypothesis_learning_state", "-")),
        _clean(seed.get("previous_open_hypothesis_reorganization_posture", "-")),
        _clean(seed.get("semantic_origin_state", "unlocated_semantic_contact")),
        _clean(seed.get("dio_syntax_signature", "-")),
        _clean(seed.get("dio_form_mcm_token", "-")),
        _clean(seed.get("dio_form_mcm_family_token", "-")),
        _clean(seed.get("dio_form_mcm_syntax_state", "-")),
        f"{float(seed.get('form_to_mcm_recall', 0.0) or 0.0):.4f}",
        f"{float(seed.get('mcm_to_form_confirmation', 0.0) or 0.0):.4f}",
        f"{float(seed.get('visual_mcm_context_fit', 0.0) or 0.0):.4f}",
        f"{float(seed.get('visual_mcm_mismatch', 0.0) or 0.0):.4f}",
        f"{float(seed.get('hypothesis_reality_binding', 0.0) or 0.0):.4f}",
        f"{float(seed.get('form_mcm_syntax_density', 0.0) or 0.0):.4f}",
        f"{float(seed.get('form_mcm_family_recurrence', 0.0) or 0.0):.4f}",
        f"{float(seed.get('form_mcm_family_maturity', 0.0) or 0.0):.4f}",
        f"{float(seed.get('form_mcm_family_trust', 0.0) or 0.0):.4f}",
        f"{float(seed.get('form_mcm_family_caution', 0.0) or 0.0):.4f}",
        f"{float(seed.get('form_mcm_family_reorganization_need', 0.0) or 0.0):.4f}",
        _clean(meta.get("open_hypothesis_reifung_state", "open_hypothesis_neutral_memory")),
        f"{float(meta.get('open_hypothesis_confirmation_weight', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_learning_charge', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_action_permission', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_reality_check_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('inner_outer_alignment', 0.0) or 0.0):.4f}",
        _clean(meta.get("previous_digest_state", "-")),
        f"{float(meta.get('previous_trust_return_readiness', 0.0) or 0.0):.4f}",
        f"{float(meta.get('previous_digestive_returned_trust', 0.0) or 0.0):.4f}",
        f"{float(meta.get('trust_return_open_hypothesis_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('trust_return_context_instability', 0.0) or 0.0):.4f}",
        f"{float(meta.get('trust_return_motor_contact_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('trust_return_act_bridge', 0.0) or 0.0):.4f}",
        f"{float(meta.get('trust_return_motor_heat', 0.0) or 0.0):.4f}",
        f"{float(meta.get('trust_return_stabilization_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('trust_return_focus_pull', 0.0) or 0.0):.4f}",
        _clean(meta.get("trust_return_motor_mode", "trust_quiet")),
        f"{float(meta.get('cortisol_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('serotonin_stability', 0.0) or 0.0):.4f}",
        f"{float(meta.get('dopamine_drive', 0.0) or 0.0):.4f}",
        _clean(meta.get("mcm_axis_state", "0")),
        f"{float(meta.get('mcm_axis_tension', 0.0) or 0.0):.4f}",
        _clean(meta.get("field_perception_label", seed.get("mcm_field_anchor", "-"))),
        _clean(seed.get("form_symbol_anchor", "-")),
        _clean(seed.get("mcm_field_anchor", "-")),
        _clean(seed.get("experience_memory_anchor", "-")),
    ]
    dbr_append_text(
        path,
        ";".join(str(item) for item in row) + "\n",
        operation="thought_digest_protocol_append",
        extra=f"digest={seed.get('thought_digest_state', '-')}",
    )
    return dict(protocol)

def _record_thought_seed_protocol(bot, runtime_result, meta_regulation_state=None, processing_state=None, felt_state=None, thought_state=None):
    if bot is None:
        return None

    result = dict(runtime_result or {})
    meta = dict(meta_regulation_state or result.get("meta_regulation_state", {}) or {})
    seed_state = _build_thought_seed_state(
        result,
        meta_regulation_state=meta,
        processing_state=processing_state,
        felt_state=felt_state,
        thought_state=thought_state,
    )
    protocol = dict(getattr(bot, "mcm_thought_seed_protocol", {}) or {})
    sequence = int(protocol.get("sequence", 0) or 0) + 1
    timestamp = result.get("timestamp", getattr(bot, "current_timestamp", None))
    runtime_tick = int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0)

    def _clip01(value):
        try:
            value = float(value)
        except Exception:
            value = 0.0
        if value != value:
            value = 0.0
        return max(0.0, min(1.0, float(value)))

    def _resolve_thought_memory_budget():
        if not bool(getattr(Config, "MCM_WORLD_THOUGHT_DECOUPLING_ENABLED", True)):
            return True, {
                "thought_memory_budget_state": "coupled_update",
                "thought_memory_budget_score": 1.0,
                "thought_memory_deferred_count": 0,
                "thought_memory_tick_gap": 999,
            }

        budget = dict(getattr(bot, "mcm_thought_memory_budget_state", {}) or {})
        last_update_tick = int(budget.get("last_update_tick", -999999) or -999999)
        tick_gap = max(0, int(runtime_tick) - int(last_update_tick))
        min_gap = max(1, int(getattr(Config, "MCM_THOUGHT_MEMORY_UPDATE_MIN_TICK_GAP", 8) or 8))
        world_tick_seconds = max(1e-9, float(getattr(Config, "WORLD_TIME_SECONDS", 1.0) or 1.0))
        cognitive_budget_seconds = max(1e-9, float(getattr(Config, "GLOBAL_COGNITIVE_REACTION_SECONDS", 0.001) or 0.001))
        cognitive_world_ratio = max(0.0, min(1.0, float(cognitive_budget_seconds) / float(world_tick_seconds)))
        fundamental_min = max(0.0, min(1.0, float(getattr(Config, "MCM_THOUGHT_MEMORY_FUNDAMENTAL_MIN", 0.42) or 0.42)))
        phase = str(seed_state.get("phase", result.get("phase", "")) or "")
        reason = str(seed_state.get("reason", result.get("reason", "")) or "")
        decision = str(seed_state.get("decision", result.get("decision", "")) or "")
        meta_state = str(meta.get("metaregulator_state", "") or "")
        digest_state = str(seed_state.get("thought_digest_state", "") or "")

        immediate_pressure = 0.0
        if phase in ("act", "replan"):
            immediate_pressure = max(immediate_pressure, 0.58)
        if reason in ("plan_allowed", "metaregulator_reflection_replan", "structure_development_observe"):
            immediate_pressure = max(immediate_pressure, 0.46)
        if decision in ("LONG", "SHORT") and phase in ("act", "replan", "observe"):
            immediate_pressure = max(immediate_pressure, 0.38)
        if meta_state in ("thought_load_distance", "integration_strain", "regulatory_overload"):
            immediate_pressure = max(immediate_pressure, 0.34)
        if digest_state in ("digestive_replay", "digestive_integration"):
            immediate_pressure = max(immediate_pressure, 0.34)

        fundamental_score = _clip01(
            (_clip01(seed_state.get("thought_confirmation_score", 0.0)) * 0.18)
            + (_clip01(seed_state.get("reality_binding_score", 0.0)) * 0.18)
            + (_clip01(seed_state.get("thought_structural_grounding", 0.0)) * 0.16)
            + (_clip01(seed_state.get("thought_trace_strength", 0.0)) * 0.12)
            + (_clip01(seed_state.get("thought_recall_potential", 0.0)) * 0.10)
            + (_clip01(seed_state.get("trust_return_readiness", 0.0)) * 0.10)
            + (max(0.0, float(seed_state.get("thought_consequence_balance", 0.0) or 0.0)) * 0.08)
            + (immediate_pressure * 0.18)
        )
        first_update = bool(last_update_tick < 0)
        enough_world_time = bool(tick_gap >= min_gap)
        allow = bool(first_update or (enough_world_time and fundamental_score >= fundamental_min))

        deferred_count = max(0, int(budget.get("deferred_count", 0) or 0))
        if allow:
            budget.update({
                "last_update_tick": int(runtime_tick),
                "last_update_sequence": int(sequence),
                "last_budget_score": float(fundamental_score),
                "deferred_count": 0,
                "last_state": "thought_memory_update",
            })
        else:
            deferred_count += 1
            budget.update({
                "deferred_count": int(deferred_count),
                "last_deferred_tick": int(runtime_tick),
                "last_deferred_sequence": int(sequence),
                "last_budget_score": float(fundamental_score),
                "last_state": "thought_memory_deferred",
            })
        setattr(bot, "mcm_thought_memory_budget_state", dict(budget or {}))
        return allow, {
            "thought_memory_budget_state": str(budget.get("last_state", "")),
            "thought_memory_budget_score": float(fundamental_score),
            "thought_memory_deferred_count": int(budget.get("deferred_count", 0) or 0),
            "thought_memory_tick_gap": int(tick_gap),
            "thought_memory_min_tick_gap": int(min_gap),
            "thought_memory_budget_fundamental_min": float(fundamental_min),
            "world_tick_seconds": float(world_tick_seconds),
            "cognitive_budget_seconds": float(cognitive_budget_seconds),
            "cognitive_world_ratio": float(cognitive_world_ratio),
        }

    allow_memory_update, budget_state = _resolve_thought_memory_budget()
    seed_state.update(dict(budget_state or {}))
    memory_item = {}
    if allow_memory_update:
        memory_item = _update_thought_memory(bot, seed_state, timestamp=timestamp, runtime_tick=runtime_tick)
    if isinstance(memory_item, dict):
        for key in (
            "form_mcm_family_recurrence",
            "form_mcm_family_maturity",
            "form_mcm_family_trust",
            "form_mcm_family_caution",
            "form_mcm_family_reorganization_need",
        ):
            if key in memory_item:
                seed_state[key] = memory_item.get(key)
    setattr(bot, "mcm_thought_seed_state", dict(seed_state or {}))
    if isinstance(runtime_result, dict):
        runtime_result["thought_seed_state"] = dict(seed_state or {})
    _record_thought_digest_protocol(
        bot,
        seed_state,
        meta_regulation_state=meta,
        timestamp=timestamp,
        runtime_tick=runtime_tick,
    )

    if not bool(getattr(Config, "MCM_THOUGHT_SEED_PROTOCOL_DEBUG", True)):
        return dict(getattr(bot, "mcm_thought_seed_protocol", {}) or {})

    key = "|".join(
        [
            str(seed_state.get("thought_seed_id", "-")),
            str(seed_state.get("seed_metaregulator_state", "-")),
            str(seed_state.get("emergent_structure_state", "-")),
            str(seed_state.get("phase", "-")),
        ]
    )
    prior_key = str(protocol.get("last_key", "") or "")
    changed = bool(key != prior_key)
    every_n = max(1, int(getattr(Config, "MCM_THOUGHT_SEED_PROTOCOL_EVERY_N", 5) or 5))
    protocol.update({
        "sequence": int(sequence),
        "last_key": str(key),
        "last_timestamp": timestamp,
        "last_runtime_tick": int(runtime_tick),
        "last_seed_state": dict(seed_state or {}),
    })
    setattr(bot, "mcm_thought_seed_protocol", dict(protocol))

    if not changed and (sequence % every_n) != 0:
        return dict(protocol)

    path = dbr_path("mcm_thought_seed_protocol.csv")
    if path not in _THOUGHT_SEED_PROTOCOL_HEADER_DONE:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header_text = (
            "timestamp;runtime_tick;sequence;thought_seed_id;thought_seed_label;decision;phase;reason;"
            "seed_metaregulator_state;emergent_memory_trace;emergent_structure_state;"
            "thought_trace_strength;thought_recall_potential;thought_maturity;reality_binding_score;"
            "thought_confirmation_score;consequence_echo;reorganization_echo;thought_consequence_alignment;"
            "thought_consequence_balance;thought_reality_lag;"
            "thought_structural_grounding;thought_open_hypothesis_pressure;"
            "thought_replay_maturation_pull;thought_distance_maturation_pull;thought_reinterpretation_pull;"
            "thought_digestive_replay_pull;thought_digestive_distance_pull;thought_digestive_integration_pull;"
            "thought_digestive_returned_trust;trust_return_readiness;thought_digest_state;"
            "thought_reifung_direction;previous_open_hypothesis_learning_state;previous_open_hypothesis_reorganization_posture;"
            "semantic_origin_state;borrowed_open_hypothesis_pressure;own_field_binding_pull;"
            "own_vs_foreign_margin;borrowed_vs_own_margin;boundary_support_margin;"
            "dio_syntax_signature;dio_language_state;dio_syntax_origin;"
            "dio_syntax_density;dio_syntax_compression;dio_syntax_coherence;"
            "dio_form_mcm_token;dio_form_mcm_family_token;dio_form_mcm_syntax_state;form_to_mcm_recall;mcm_to_form_confirmation;"
            "visual_mcm_context_fit;visual_mcm_mismatch;hypothesis_reality_binding;form_mcm_syntax_density;"
            "form_mcm_family_recurrence;form_mcm_family_maturity;form_mcm_family_trust;"
            "form_mcm_family_caution;form_mcm_family_reorganization_need;"
            "dio_world_experience_anchor;dio_thought_experience_anchor;"
            "dio_language_sentence;dio_dialogue_bridge_sentence;"
            "hallucination_drift_risk;overthinking_risk;emergent_structure_reading;rr_value;"
            "form_symbol_anchor;mcm_field_anchor;experience_memory_anchor;outcome_anchor\n"
        )
        write_start = time.perf_counter()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header_text)
        dbr_file_write_profile(
            path,
            (time.perf_counter() - write_start) * 1000.0,
            bytes_written=len(header_text.encode("utf-8")),
            operation="thought_seed_protocol_header",
        )
        _THOUGHT_SEED_PROTOCOL_HEADER_DONE.add(path)

    def _clean(value):
        return str(value).replace("\n", " ").replace(";", "|")

    row = [
        _clean(timestamp),
        int(runtime_tick),
        int(sequence),
        _clean(seed_state.get("thought_seed_id", "-")),
        _clean(seed_state.get("thought_seed_label", "-")),
        _clean(seed_state.get("decision", "WAIT")),
        _clean(seed_state.get("phase", "hold")),
        _clean(seed_state.get("reason", "-")),
        _clean(seed_state.get("seed_metaregulator_state", "seed_release")),
        int(bool(seed_state.get("emergent_memory_trace", False))),
        _clean(seed_state.get("emergent_structure_state", "ordinary_structure_reading")),
        f"{float(seed_state.get('thought_trace_strength', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_recall_potential', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_maturity', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('reality_binding_score', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_confirmation_score', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('consequence_echo', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('reorganization_echo', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_consequence_alignment', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_consequence_balance', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_reality_lag', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_structural_grounding', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_open_hypothesis_pressure', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_replay_maturation_pull', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_distance_maturation_pull', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_reinterpretation_pull', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_digestive_replay_pull', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_digestive_distance_pull', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_digestive_integration_pull', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('thought_digestive_returned_trust', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('trust_return_readiness', 0.0) or 0.0):.4f}",
        _clean(seed_state.get("thought_digest_state", "digestive_quiet")),
        _clean(seed_state.get("thought_reifung_direction", "no_previous_open_hypothesis_trace")),
        _clean(seed_state.get("previous_open_hypothesis_learning_state", "-")),
        _clean(seed_state.get("previous_open_hypothesis_reorganization_posture", "-")),
        _clean(seed_state.get("semantic_origin_state", "unlocated_semantic_contact")),
        f"{float(seed_state.get('borrowed_open_hypothesis_pressure', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('own_field_binding_pull', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('own_vs_foreign_margin', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('borrowed_vs_own_margin', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('boundary_support_margin', 0.0) or 0.0):.4f}",
        _clean(seed_state.get("dio_syntax_signature", "-")),
        _clean(seed_state.get("dio_language_state", "-")),
        _clean(seed_state.get("dio_syntax_origin", "-")),
        f"{float(seed_state.get('dio_syntax_density', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('dio_syntax_compression', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('dio_syntax_coherence', 0.0) or 0.0):.4f}",
        _clean(seed_state.get("dio_form_mcm_token", "-")),
        _clean(seed_state.get("dio_form_mcm_family_token", "-")),
        _clean(seed_state.get("dio_form_mcm_syntax_state", "-")),
        f"{float(seed_state.get('form_to_mcm_recall', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('mcm_to_form_confirmation', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('visual_mcm_context_fit', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('visual_mcm_mismatch', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('hypothesis_reality_binding', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('form_mcm_syntax_density', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('form_mcm_family_recurrence', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('form_mcm_family_maturity', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('form_mcm_family_trust', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('form_mcm_family_caution', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('form_mcm_family_reorganization_need', 0.0) or 0.0):.4f}",
        _clean(seed_state.get("dio_world_experience_anchor", "-")),
        _clean(seed_state.get("dio_thought_experience_anchor", "-")),
        _clean(seed_state.get("dio_language_sentence", "-")),
        _clean(seed_state.get("dio_dialogue_bridge_sentence", "-")),
        f"{float(seed_state.get('hallucination_drift_risk', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('overthinking_risk', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('emergent_structure_reading', 0.0) or 0.0):.4f}",
        f"{float(seed_state.get('rr_value', 0.0) or 0.0):.4f}",
        _clean(seed_state.get("form_symbol_anchor", "-")),
        _clean(seed_state.get("mcm_field_anchor", "-")),
        _clean(seed_state.get("experience_memory_anchor", "-")),
        _clean(seed_state.get("outcome_anchor", "pending")),
    ]
    line = ";".join(str(item) for item in row) + "\n"
    dbr_append_text(
        path,
        line,
        operation="thought_seed_protocol_append",
        extra=f"seed={seed_state.get('thought_seed_id', '-')}|state={seed_state.get('seed_metaregulator_state', '-')}",
    )
    return dict(protocol)

def _record_field_decision_protocol(bot, runtime_result, meta_regulation_state=None, processing_state=None, felt_state=None, thought_state=None):

    if bot is None:
        return None

    _record_form_symbol_protocol(
        bot,
        runtime_result,
        meta_regulation_state=meta_regulation_state,
        processing_state=processing_state,
        felt_state=felt_state,
    )

    _record_memory_thinking_protocol(
        bot,
        runtime_result,
        meta_regulation_state=meta_regulation_state,
        processing_state=processing_state,
        felt_state=felt_state,
        thought_state=thought_state,
    )

    _record_thought_seed_protocol(
        bot,
        runtime_result,
        meta_regulation_state=meta_regulation_state,
        processing_state=processing_state,
        felt_state=felt_state,
        thought_state=thought_state,
    )

    _record_thought_landkarte_protocol(
        bot,
        runtime_result,
        meta_regulation_state=meta_regulation_state,
        processing_state=processing_state,
        felt_state=felt_state,
        thought_state=thought_state,
    )

    if not bool(getattr(Config, "MCM_FIELD_DECISION_PROTOCOL_DEBUG", True)):
        return None

    result = dict(runtime_result or {})
    meta = dict(meta_regulation_state or result.get("meta_regulation_state", {}) or {})
    processing = dict(processing_state or result.get("processing_state", {}) or {})
    felt = dict(felt_state or result.get("felt_state", {}) or {})
    thought = dict(thought_state or result.get("thought_state", {}) or {})

    phase = str(meta.get("pre_action_phase", "hold") or "hold").strip().lower()
    reason = str(meta.get("rejection_reason", result.get("rejection_reason", "-")) or "-").strip()
    proposed_decision = str(meta.get("decision", result.get("decision", "WAIT")) or "WAIT").strip().upper()
    field_label = str(meta.get("field_perception_label", processing.get("field_perception_label", felt.get("field_perception_label", "quiet_field"))) or "quiet_field").strip()
    runtime_tick = int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0)
    lag_state = dict(getattr(bot, "last_cognitive_lag_state", {}) or {})
    timestamp = result.get("timestamp", getattr(bot, "current_timestamp", None))

    protocol = dict(getattr(bot, "mcm_field_decision_protocol", {}) or {})
    counts = dict(protocol.get("phase_counts", {}) or {})
    reason_counts = dict(protocol.get("reason_counts", {}) or {})
    field_label_counts = dict(protocol.get("field_label_counts", {}) or {})

    counts[phase] = int(counts.get(phase, 0) or 0) + 1
    reason_counts[reason] = int(reason_counts.get(reason, 0) or 0) + 1
    field_label_counts[field_label] = int(field_label_counts.get(field_label, 0) or 0) + 1

    prior_key = str(protocol.get("last_phase_key", "") or "")
    phase_key = f"{phase}|{reason}|{field_label}"
    first_event = not bool(prior_key)
    phase_changed = bool(first_event or prior_key != phase_key)
    every_n = max(1, int(getattr(Config, "MCM_FIELD_DECISION_PROTOCOL_EVERY_N", 5) or 5))
    change_burst = bool(getattr(Config, "MCM_PROTOCOL_CHANGE_BURST_DEBUG", True))
    sequence = int(protocol.get("sequence", 0) or 0) + 1

    protocol.update({
        "sequence": int(sequence),
        "last_phase": str(phase),
        "last_reason": str(reason),
        "last_field_label": str(field_label),
        "last_phase_key": str(phase_key),
        "last_timestamp": timestamp,
        "last_runtime_tick": int(runtime_tick),
        "phase_counts": dict(counts),
        "reason_counts": dict(reason_counts),
        "field_label_counts": dict(field_label_counts),
    })
    setattr(bot, "mcm_field_decision_protocol", dict(protocol))

    if (not change_burst or not phase_changed) and (sequence % every_n) != 0:
        return dict(protocol)

    path = dbr_path("mcm_field_decision_protocol.csv")
    if path not in _FIELD_DECISION_PROTOCOL_HEADER_DONE:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header_text = (
            "timestamp;runtime_tick;sequence;world_published_ticks;world_missed_ticks;dropped_world_ticks;"
            "runtime_queue_size;cognitive_lag_pressure;world_motion_afterimage_strength;"
            "world_motion_afterimage_pressure;world_motion_afterimage_direction;"
            "world_motion_afterimage_label;motion_approach_pressure;motion_recession_pressure;"
            "contact_frequency_shift;afterimage_doppler_bias;future_variant_pressure;"
            "afterimage_action_maturity;afterimage_doppler_label;phase;reason;decision;field_label;"
            "neurochemical_state_label;neurochemical_dominant_tone;dopamine_tone;gaba_inhibition;"
            "noradrenaline_arousal;acetylcholine_focus;serotonin_stability;cortisol_load;"
            "endorphin_relief;glutamate_activation;neurochemical_load;neurochemical_support;neurochemical_balance;"
            "reward_stability_echo;positive_expansion_pressure;negative_contraction_pressure;positive_overextension;"
            "positive_return_pressure;mcm_axis_displacement;mcm_axis_field_position;mcm_axis_tension;mcm_axis_state;positive_zero_point_regulation;"
            "world_shift_evidence;serotonin_carryover_risk;emotional_decoupling;reactive_nervous_drive;"
            "nervous_system_overload;escape_action_drive;shock_response_risk;nervous_overload_reflection_need;"
            "active_context_self_certainty;nervous_context_overcoupling;"
            "own_field_identity_strength;foreign_semantic_pressure;adopted_language_pressure;"
            "self_foreign_boundary_clarity;semantic_origin_conflict;"
            "own_vs_foreign_margin;borrowed_vs_own_margin;boundary_support_margin;semantic_origin_state;"
            "conscious_perception_state;inner_posture_state;arousal_load;curiosity_tone;fatigue_tone;calm_tone;"
            "stimulus_field_effect;inner_impact_trace;perceived_field_change;felt_afterimage;"
            "object_release_state;inner_outer_reflection;perceptual_distance;object_contact_depth;field_attachment;"
            "release_capacity;selective_attention;background_containment;reflective_distance;inner_outer_alignment;"
            "engaged_effort;effort_state;effort_learning_pull;effort_reorganization_pressure;"
            "pre_action_reorganization_pressure;pre_action_context_selectivity;"
            "previous_packet_label;previous_packet_process_reward;previous_packet_reorganization_need;"
            "previous_open_hypothesis_learning_state;open_hypothesis_trace_strength;"
            "hypothesis_weight;hypothesis_trust;hypothesis_caution;hypothesis_reorganization_weight;"
            "action_weight;decision_weight;open_hypothesis_reifung_state;"
            "open_hypothesis_bearing_echo;open_hypothesis_reifung_pressure;"
            "open_hypothesis_reflection_pull;open_hypothesis_motor_tension;"
            "open_hypothesis_confirmation_weight;open_hypothesis_learning_charge;"
            "open_hypothesis_action_permission;open_hypothesis_reality_check_need;"
            "diffuse_open_development_pressure;posture_development_hint;"
            "metaregulator_state;metaregulator_balance;regulatory_second_order_load;"
            "subconscious_field_pressure;subconscious_habituation;subconscious_filter_strength;"
            "subconscious_buffering;subconscious_leakage;subconscious_afterimage_depth;"
            "subconscious_afterimage_pressure;subconscious_afterimage_bearing;subconscious_afterimage_clarity;"
            "subconscious_afterimage_release;subconscious_afterimage_reflection_pull;conscious_selection_pressure;"
            "conscious_workspace_focus;conscious_workspace_load;conscious_gate_balance;"
            "integration_strain_value;integration_sorting_need;integration_reframe_pull;"
            "integration_memory_recall;integration_contact_deepening;integration_response_strength;integration_response_state;"
            "cautious_hypothesis_strength;cautious_hypothesis_clarity;cautious_hypothesis_patience;cautious_hypothesis_state;"
            "temporal_binding_state;temporal_continuity;temporal_source_binding;temporal_recurrence;"
            "temporal_novelty;temporal_afterimage;temporal_decay;temporal_context_depth;"
            "mcm_spacetime_depth;memory_experience_depth;future_projection_depth;temporal_self_location;temporal_self_location_state;"
            "spacetime_unlocated_pressure;spacetime_memory_bearing;spacetime_future_bearing;spacetime_reflection_need;spacetime_regulation_support;spacetime_regulation_state;"
            "temporal_self_consistency;perception_sequence_coherence;memory_time_distance;"
            "return_strength;integration_capacity;variance_regulation;load_tolerance;impulse_control;"
            "frustration_tolerance;protective_distance_regulation;self_reflection_regulator;distance_regulation;"
            "field_focus;field_clarity;field_stability;field_fragmentation;field_strain;"
            "field_pressure;field_support;field_observation_need;field_replan_pressure;field_action_support;"
            "action_clearance;action_inhibition;regulated_courage;decision_strength;state_maturity;decision_readiness;"
            "plan_pressure;act_watch_readiness;structure_carrying_need;structure_action_uncertainty;"
            "visual_blind_action_load;visual_action_uncertainty;visual_clarity;visual_object_stability;"
            "visual_object_binding;visual_grounding_strength;visual_resonance_unbound;visual_grounding_gap;"
            "visual_grounding_need;visual_rational_observation_support;visual_grounding_state;"
            "visual_blindness;visual_form_pressure;visual_shape_resonance;visual_shape_fragility;"
            "uncertain_form_family_state;uncertain_form_exposure;uncertainty_familiarity;"
            "variant_spread;variant_learning_pressure;variant_bearing_memory;"
            "processing_load;processing_tension;felt_pressure;felt_stability;thought_pressure;thought_support;"
            "context_cluster_id;inner_context_cluster_id\n"
        )
        write_start = time.perf_counter()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header_text)
        dbr_file_write_profile(
            path,
            (time.perf_counter() - write_start) * 1000.0,
            bytes_written=len(header_text.encode("utf-8")),
            operation="field_decision_protocol_header",
        )
        _FIELD_DECISION_PROTOCOL_HEADER_DONE.add(path)

    def _clean(value):
        return str(value).replace("\n", " ").replace(";", "|")

    row = [
        _clean(timestamp),
        int(runtime_tick),
        int(sequence),
        int(getattr(bot, "world_published_ticks", 0) or 0),
        int(getattr(bot, "world_missed_ticks", 0) or 0),
        int(lag_state.get("dropped_world_ticks", 0) or 0),
        int(lag_state.get("queue_size", 0) or 0),
        f"{float(getattr(bot, 'cognitive_lag_pressure', 0.0) or 0.0):.4f}",
        f"{float((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get('world_motion_afterimage_strength', 0.0) or 0.0):.4f}",
        f"{float((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get('world_motion_afterimage_pressure', 0.0) or 0.0):.4f}",
        f"{float((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get('world_motion_afterimage_direction', 0.0) or 0.0):.4f}",
        _clean((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get("world_motion_afterimage_label", "motion_afterimage_clear")),
        f"{float((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get('motion_approach_pressure', 0.0) or 0.0):.4f}",
        f"{float((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get('motion_recession_pressure', 0.0) or 0.0):.4f}",
        f"{float((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get('contact_frequency_shift', 0.0) or 0.0):.4f}",
        f"{float((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get('afterimage_doppler_bias', 0.0) or 0.0):.4f}",
        f"{float((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get('future_variant_pressure', 0.0) or 0.0):.4f}",
        f"{float((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get('afterimage_action_maturity', 0.0) or 0.0):.4f}",
        _clean((getattr(bot, 'world_motion_afterimage_state', {}) or {}).get("afterimage_doppler_label", "doppler_clear")),
        _clean(phase),
        _clean(reason),
        _clean(proposed_decision),
        _clean(field_label),
        _clean(meta.get("neurochemical_state_label", "mixed_neurochemistry")),
        _clean(meta.get("neurochemical_dominant_tone", "-")),
        f"{float(meta.get('dopamine_tone', 0.0) or 0.0):.4f}",
        f"{float(meta.get('gaba_inhibition', 0.0) or 0.0):.4f}",
        f"{float(meta.get('noradrenaline_arousal', 0.0) or 0.0):.4f}",
        f"{float(meta.get('acetylcholine_focus', 0.0) or 0.0):.4f}",
        f"{float(meta.get('serotonin_stability', 0.0) or 0.0):.4f}",
        f"{float(meta.get('cortisol_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('endorphin_relief', 0.0) or 0.0):.4f}",
        f"{float(meta.get('glutamate_activation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('neurochemical_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('neurochemical_support', 0.0) or 0.0):.4f}",
        f"{float(meta.get('neurochemical_balance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('reward_stability_echo', 0.0) or 0.0):.4f}",
        f"{float(meta.get('positive_expansion_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('negative_contraction_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('positive_overextension', 0.0) or 0.0):.4f}",
        f"{float(meta.get('positive_return_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('mcm_axis_displacement', 0.0) or 0.0):.4f}",
        f"{float(meta.get('mcm_axis_field_position', 0.0) or 0.0):.4f}",
        f"{float(meta.get('mcm_axis_tension', 0.0) or 0.0):.4f}",
        _clean(meta.get("mcm_axis_state", "0")),
        int(bool(meta.get("positive_zero_point_regulation", False))),
        f"{float(meta.get('world_shift_evidence', 0.0) or 0.0):.4f}",
        f"{float(meta.get('serotonin_carryover_risk', 0.0) or 0.0):.4f}",
        f"{float(meta.get('emotional_decoupling', 0.0) or 0.0):.4f}",
        f"{float(meta.get('reactive_nervous_drive', 0.0) or 0.0):.4f}",
        f"{float(meta.get('nervous_system_overload', 0.0) or 0.0):.4f}",
        f"{float(meta.get('escape_action_drive', 0.0) or 0.0):.4f}",
        f"{float(meta.get('shock_response_risk', 0.0) or 0.0):.4f}",
        f"{float(meta.get('nervous_overload_reflection_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('active_context_self_certainty', 0.0) or 0.0):.4f}",
        f"{float(meta.get('nervous_context_overcoupling', 0.0) or 0.0):.4f}",
        f"{float(meta.get('own_field_identity_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('foreign_semantic_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('adopted_language_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('self_foreign_boundary_clarity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('semantic_origin_conflict', 0.0) or 0.0):.4f}",
        f"{float(meta.get('own_vs_foreign_margin', 0.0) or 0.0):.4f}",
        f"{float(meta.get('borrowed_vs_own_margin', 0.0) or 0.0):.4f}",
        f"{float(meta.get('boundary_support_margin', 0.0) or 0.0):.4f}",
        _clean(meta.get("semantic_origin_state", "unlocated_semantic_contact")),
        _clean(meta.get("conscious_perception_state", "open_perception")),
        _clean(meta.get("inner_posture_state", "uncertain_open")),
        f"{float(meta.get('arousal_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('curiosity_tone', 0.0) or 0.0):.4f}",
        f"{float(meta.get('fatigue_tone', 0.0) or 0.0):.4f}",
        f"{float(meta.get('calm_tone', 0.0) or 0.0):.4f}",
        f"{float(meta.get('stimulus_field_effect', 0.0) or 0.0):.4f}",
        f"{float(meta.get('inner_impact_trace', 0.0) or 0.0):.4f}",
        f"{float(meta.get('perceived_field_change', 0.0) or 0.0):.4f}",
        f"{float(meta.get('felt_afterimage', 0.0) or 0.0):.4f}",
        _clean(meta.get("object_release_state", "holding")),
        f"{float(meta.get('inner_outer_reflection', 0.0) or 0.0):.4f}",
        f"{float(meta.get('perceptual_distance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('object_contact_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('field_attachment', 0.0) or 0.0):.4f}",
        f"{float(meta.get('release_capacity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('selective_attention', 0.0) or 0.0):.4f}",
        f"{float(meta.get('background_containment', 0.0) or 0.0):.4f}",
        f"{float(meta.get('reflective_distance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('inner_outer_alignment', 0.0) or 0.0):.4f}",
        f"{float(meta.get('engaged_effort', 0.0) or 0.0):.4f}",
        _clean(meta.get("effort_state", "settled_effort")),
        f"{float(meta.get('effort_learning_pull', 0.0) or 0.0):.4f}",
        f"{float(meta.get('effort_reorganization_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('pre_action_reorganization_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('pre_action_context_selectivity', 0.0) or 0.0):.4f}",
        _clean(meta.get("previous_packet_label", "-")),
        f"{float(meta.get('previous_packet_process_reward', 0.0) or 0.0):.4f}",
        f"{float(meta.get('previous_packet_reorganization_need', 0.0) or 0.0):.4f}",
        _clean(meta.get("previous_open_hypothesis_learning_state", "-")),
        f"{float(meta.get('open_hypothesis_trace_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_weight', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_trust', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_caution', 0.0) or 0.0):.4f}",
        f"{float(meta.get('hypothesis_reorganization_weight', 0.0) or 0.0):.4f}",
        f"{float(meta.get('action_weight', 0.0) or 0.0):.4f}",
        f"{float(meta.get('decision_weight', 0.0) or 0.0):.4f}",
        _clean(meta.get("open_hypothesis_reifung_state", "open_hypothesis_neutral_memory")),
        f"{float(meta.get('open_hypothesis_bearing_echo', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_reifung_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_reflection_pull', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_motor_tension', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_confirmation_weight', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_learning_charge', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_action_permission', 0.0) or 0.0):.4f}",
        f"{float(meta.get('open_hypothesis_reality_check_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('diffuse_open_development_pressure', 0.0) or 0.0):.4f}",
        _clean(meta.get("posture_development_hint", "stable_posture")),
        _clean(meta.get("metaregulator_state", "adaptive_watch")),
        f"{float(meta.get('metaregulator_balance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('regulatory_second_order_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_field_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_habituation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_filter_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_buffering', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_leakage', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_bearing', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_clarity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_release', 0.0) or 0.0):.4f}",
        f"{float(meta.get('subconscious_afterimage_reflection_pull', 0.0) or 0.0):.4f}",
        f"{float(meta.get('conscious_selection_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('conscious_workspace_focus', 0.0) or 0.0):.4f}",
        f"{float(meta.get('conscious_workspace_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('conscious_gate_balance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_strain_value', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_sorting_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_reframe_pull', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_memory_recall', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_contact_deepening', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_response_strength', 0.0) or 0.0):.4f}",
        _clean(meta.get("integration_response_state", "integration_background")),
        f"{float(meta.get('cautious_hypothesis_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('cautious_hypothesis_clarity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('cautious_hypothesis_patience', 0.0) or 0.0):.4f}",
        _clean(meta.get("cautious_hypothesis_state", "no_cautious_hypothesis")),
        _clean(meta.get("temporal_binding_state", "unbound_moment")),
        f"{float(meta.get('temporal_continuity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_source_binding', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_recurrence', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_novelty', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_afterimage', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_decay', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_context_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('mcm_spacetime_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('memory_experience_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('future_projection_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('temporal_self_location', 0.0) or 0.0):.4f}",
        _clean(meta.get("temporal_self_location_state", "unlocated_contact")),
        f"{float(meta.get('spacetime_unlocated_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('spacetime_memory_bearing', 0.0) or 0.0):.4f}",
        f"{float(meta.get('spacetime_future_bearing', 0.0) or 0.0):.4f}",
        f"{float(meta.get('spacetime_reflection_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('spacetime_regulation_support', 0.0) or 0.0):.4f}",
        _clean(meta.get("spacetime_regulation_state", "spacetime_open")),
        f"{float(meta.get('temporal_self_consistency', 0.0) or 0.0):.4f}",
        f"{float(meta.get('perception_sequence_coherence', 0.0) or 0.0):.4f}",
        f"{float(meta.get('memory_time_distance', 1.0) or 1.0):.4f}",
        f"{float(meta.get('return_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('integration_capacity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('variance_regulation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('load_tolerance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('impulse_control', 0.0) or 0.0):.4f}",
        f"{float(meta.get('frustration_tolerance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('protective_distance_regulation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('self_reflection_regulator', 0.0) or 0.0):.4f}",
        f"{float(meta.get('distance_regulation', 0.0) or 0.0):.4f}",
        f"{float(meta.get('field_perception_focus', processing.get('field_perception_focus', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('field_perception_clarity', processing.get('field_perception_clarity', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('field_perception_stability', processing.get('field_perception_stability', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('field_perception_fragmentation', processing.get('field_perception_fragmentation', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('field_perception_strain', processing.get('field_perception_strain', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('field_perception_pressure', processing.get('field_perception_pressure', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('field_perception_support', processing.get('field_perception_support', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('field_observation_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('field_replan_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('field_action_support', 0.0) or 0.0):.4f}",
        f"{float(meta.get('action_clearance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('action_inhibition', 0.0) or 0.0):.4f}",
        f"{float(meta.get('regulated_courage', 0.0) or 0.0):.4f}",
        f"{float(meta.get('decision_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('state_maturity', thought.get('state_maturity', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('decision_readiness', thought.get('decision_readiness', 0.0)) or 0.0):.4f}",
        f"{float(meta.get('plan_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('act_watch_readiness', 0.0) or 0.0):.4f}",
        f"{float(meta.get('structure_carrying_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('structure_action_uncertainty', 0.0) or 0.0):.4f}",
        f"{float(meta.get('visual_blind_action_load', 0.0) or 0.0):.4f}",
        f"{float(meta.get('visual_action_uncertainty', 0.0) or 0.0):.4f}",
        f"{float(meta.get('visual_clarity', felt.get('visual_clarity', processing.get('visual_clarity', 0.0))) or 0.0):.4f}",
        f"{float(meta.get('visual_object_stability', felt.get('visual_object_stability', processing.get('visual_object_stability', 0.0))) or 0.0):.4f}",
        f"{float(meta.get('visual_object_binding', 0.0) or 0.0):.4f}",
        f"{float(meta.get('visual_grounding_strength', 0.0) or 0.0):.4f}",
        f"{float(meta.get('visual_resonance_unbound', 0.0) or 0.0):.4f}",
        f"{float(meta.get('visual_grounding_gap', 0.0) or 0.0):.4f}",
        f"{float(meta.get('visual_grounding_need', 0.0) or 0.0):.4f}",
        f"{float(meta.get('visual_rational_observation_support', 0.0) or 0.0):.4f}",
        _clean(meta.get("visual_grounding_state", "-")),
        f"{float(meta.get('visual_blindness', felt.get('visual_blindness', processing.get('visual_blindness', 0.0))) or 0.0):.4f}",
        f"{float(meta.get('visual_form_pressure', felt.get('visual_form_pressure', processing.get('visual_form_pressure', 0.0))) or 0.0):.4f}",
        f"{float(meta.get('visual_shape_resonance', felt.get('visual_shape_resonance', processing.get('visual_shape_resonance', 0.0))) or 0.0):.4f}",
        f"{float(meta.get('visual_shape_fragility', felt.get('visual_shape_fragility', processing.get('visual_shape_fragility', 0.0))) or 0.0):.4f}",
        _clean(meta.get('uncertain_form_family_state', 'quiet_form_family')),
        f"{float(meta.get('uncertain_form_exposure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('uncertainty_familiarity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('variant_spread', 0.0) or 0.0):.4f}",
        f"{float(meta.get('variant_learning_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('variant_bearing_memory', 0.0) or 0.0):.4f}",
        f"{float(processing.get('processing_load', 0.0) or 0.0):.4f}",
        f"{float(processing.get('processing_tension', 0.0) or 0.0):.4f}",
        f"{float(felt.get('felt_pressure', 0.0) or 0.0):.4f}",
        f"{float(felt.get('felt_stability', 0.0) or 0.0):.4f}",
        f"{float(thought.get('thought_areal_pressure', 0.0) or 0.0):.4f}",
        f"{float(thought.get('thought_areal_support', 0.0) or 0.0):.4f}",
        _clean(result.get("context_cluster_id", "-")),
        _clean(getattr(bot, "last_inner_context_cluster_id", "-")),
    ]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    line = ";".join(str(item) for item in row) + "\n"
    dbr_append_text(
        path,
        line,
        operation="field_decision_protocol_append",
        extra=f"phase={phase}|reason={reason}|field={field_label}",
    )
    return dict(protocol)

def build_strategic_window_state(
    window,
    candle_state=None,
    visual_market_state=None,
    structure_perception_state=None,
    form_symbol_state=None,
    meta_regulation_state=None,
    bot=None,
):
    candles = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
    if not candles:
        return {
            "strategic_window_state": "no_window",
            "lookback_window_size": 0,
            "area_candidate_count": 0,
            "area_focus_candidates": [],
        }

    candle_state = dict(candle_state or {})
    visual_market_state = dict(visual_market_state or {})
    structure_perception_state = dict(structure_perception_state or {})
    form_symbol_state = dict(form_symbol_state or {})
    meta = dict(meta_regulation_state or {})

    def _clip(value, lo=0.0, hi=1.0):
        try:
            value = float(value)
        except Exception:
            value = 0.0
        if value != value:
            value = 0.0
        return max(float(lo), min(float(hi), float(value)))

    def _float(value, default=0.0):
        try:
            value = float(value)
        except Exception:
            value = float(default)
        if value != value:
            value = float(default)
        return float(value)

    def _price(candle, key, fallback=0.0):
        item = dict(candle or {})
        return _float(item.get(key, item.get(key.capitalize(), fallback)), fallback)

    current = dict(candles[-1] or {})
    current_price = _float(
        candle_state.get(
            "close",
            candle_state.get("price", current.get("close", current.get("Close", 0.0))),
        ),
        0.0,
    )
    if current_price <= 0.0:
        current_price = _price(current, "close", _price(current, "Close", 0.0))

    neurochemical_load = _clip(meta.get("neurochemical_load", 0.0))
    processing_load = _clip(meta.get("processing_load", meta.get("field_perception_pressure", 0.0)))
    memory_compare_load = _clip(meta.get("memory_compare_load", 0.0))
    fatigue_tone = _clip(meta.get("fatigue_tone", 0.0))
    reorg_pressure = _clip(meta.get("effort_reorganization_pressure", meta.get("pre_action_reorganization_pressure", 0.0)))
    focus_support = _clip(meta.get("acetylcholine_focus", meta.get("selective_attention", 0.0)))
    serotonin_stability = _clip(meta.get("serotonin_stability", 0.0))
    dopamine_tone = _clip(meta.get("dopamine_tone", 0.0))
    gaba_inhibition = _clip(meta.get("gaba_inhibition", 0.0))

    lookback_load = _clip(
        (neurochemical_load * 0.26)
        + (processing_load * 0.22)
        + (memory_compare_load * 0.18)
        + (fatigue_tone * 0.18)
        + (reorg_pressure * 0.16)
    )
    max_lookback = int(getattr(Config, "MCM_STRATEGIC_LOOKBACK_MAX", 96) or 96)
    min_lookback = int(getattr(Config, "MCM_STRATEGIC_LOOKBACK_MIN", 24) or 24)
    max_lookback = max(12, min(240, max_lookback))
    min_lookback = max(6, min(max_lookback, min_lookback))
    adaptive_size = int(round(max_lookback - ((max_lookback - min_lookback) * lookback_load)))
    lookback_window_size = max(min_lookback, min(max_lookback, adaptive_size, len(candles)))
    tail = candles[-lookback_window_size:]

    highs = [_price(item, "high", _price(item, "close", 0.0)) for item in tail]
    lows = [_price(item, "low", _price(item, "close", 0.0)) for item in tail]
    closes = [_price(item, "close", 0.0) for item in tail]
    volumes = [_price(item, "volume", 0.0) for item in tail]
    valid_prices = [value for value in highs + lows + closes if value > 0.0]
    if not valid_prices:
        return {
            "strategic_window_state": "no_price_form",
            "lookback_window_size": int(lookback_window_size),
            "area_candidate_count": 0,
            "area_focus_candidates": [],
        }

    window_high = max(highs) if highs else max(valid_prices)
    window_low = min(lows) if lows else min(valid_prices)
    window_span = max(1e-9, float(window_high - window_low))
    candle_spans = [max(0.0, high - low) for high, low in zip(highs, lows)]
    avg_span = float(np.mean(candle_spans)) if candle_spans else 0.0
    avg_volume = float(np.mean(volumes)) if volumes else 0.0
    close_delta = abs(closes[-1] - closes[0]) if len(closes) > 1 else 0.0
    drift_pressure = _clip(close_delta / max(window_span, 1e-9))

    structural_quality = _clip(structure_perception_state.get("structure_quality", meta.get("structure_quality", 0.0)))
    context_confidence = _clip(structure_perception_state.get("context_confidence", meta.get("context_confidence", 0.0)))
    visual_clarity = _clip(visual_market_state.get("visual_clarity", meta.get("visual_clarity", 0.0)))
    visual_stability = _clip(visual_market_state.get("visual_object_stability", meta.get("visual_object_stability", 0.0)))
    form_resonance = _clip(form_symbol_state.get("form_symbol_resonance", 0.0))
    form_learning_trust = _clip(form_symbol_state.get("form_symbol_learning_trust", 0.0))
    variant_bearing_memory = _clip(form_symbol_state.get("variant_bearing_memory", meta.get("variant_bearing_memory", 0.0)))
    packet_reward = _clip(meta.get("previous_packet_process_reward", 0.0))
    packet_reorg = _clip(meta.get("previous_packet_reorganization_need", 0.0))
    memory_orientation = _clip(meta.get("inner_pattern_bearing", 0.0))
    memory_conflict = _clip(meta.get("inner_pattern_conflict", 0.0))
    mcm_spacetime_depth = _clip(meta.get("mcm_spacetime_depth", 0.0))
    memory_experience_depth = _clip(meta.get("memory_experience_depth", 0.0))
    future_projection_depth = _clip(meta.get("future_projection_depth", 0.0))
    temporal_self_location = _clip(meta.get("temporal_self_location", 0.0))
    temporal_self_location_state = str(meta.get("temporal_self_location_state", "unlocated_contact") or "unlocated_contact")
    spacetime_unlocated_pressure = _clip(meta.get("spacetime_unlocated_pressure", 0.0))
    spacetime_memory_bearing = _clip(meta.get("spacetime_memory_bearing", 0.0))
    spacetime_future_bearing = _clip(meta.get("spacetime_future_bearing", 0.0))
    spacetime_reflection_need = _clip(meta.get("spacetime_reflection_need", 0.0))
    spacetime_regulation_support = _clip(meta.get("spacetime_regulation_support", 0.0))
    spacetime_regulation_state = str(meta.get("spacetime_regulation_state", "spacetime_open") or "spacetime_open")

    replay_budget = _clip((focus_support * 0.28) + (serotonin_stability * 0.22) + (context_confidence * 0.18) + (gaba_inhibition * 0.12) - (lookback_load * 0.20) + 0.28)
    zoom_budget = _clip((visual_clarity * 0.28) + (focus_support * 0.24) + (structural_quality * 0.18) + (dopamine_tone * 0.10) - (fatigue_tone * 0.14) + 0.26)
    lookback_relevance = _clip((visual_stability * 0.22) + (structural_quality * 0.24) + (context_confidence * 0.20) + (form_resonance * 0.14) - (drift_pressure * 0.10) + 0.20)
    lookback_bearing_capacity = _clip((lookback_relevance * 0.36) + (replay_budget * 0.22) + (zoom_budget * 0.18) + (memory_orientation * 0.12) - (lookback_load * 0.18) + 0.16)
    old_structure_carryover_risk = _clip((drift_pressure * 0.30) + (packet_reorg * 0.22) + (memory_conflict * 0.20) + (lookback_load * 0.12) - (visual_stability * 0.10))

    segment_len = max(6, min(18, int(round(lookback_window_size / 6.0))))
    stride = max(3, int(round(segment_len / 2.0)))
    candidates = []
    for start in range(0, max(1, len(tail) - segment_len + 1), stride):
        segment = tail[start:start + segment_len]
        if len(segment) < 4:
            continue
        seg_highs = [_price(item, "high", _price(item, "close", 0.0)) for item in segment]
        seg_lows = [_price(item, "low", _price(item, "close", 0.0)) for item in segment]
        seg_closes = [_price(item, "close", 0.0) for item in segment]
        seg_volumes = [_price(item, "volume", 0.0) for item in segment]
        area_high = max(seg_highs)
        area_low = min(seg_lows)
        area_mid = (area_high + area_low) / 2.0
        area_span = max(1e-9, area_high - area_low)
        area_distance = _clip(abs(current_price - area_mid) / max(window_span, 1e-9))
        area_center_index = float(start + (len(segment) - 1) * 0.50)
        area_temporal_distance = _clip((len(tail) - 1 - area_center_index) / max(1.0, len(tail) - 1))
        area_recency = _clip(1.0 - area_temporal_distance)
        area_decay = _clip(area_temporal_distance * (0.58 + drift_pressure * 0.24 + old_structure_carryover_risk * 0.18))
        touch_band = max(avg_span * 0.80, window_span * 0.018, 1e-9)
        touches = sum(1 for value in seg_closes if abs(value - area_mid) <= touch_band)
        touch_density = _clip(touches / max(1, len(seg_closes)))
        compression = _clip(1.0 - (area_span / max(window_span, 1e-9)))
        close_std = float(np.std(seg_closes)) if len(seg_closes) > 1 else 0.0
        close_compression = _clip(1.0 - (close_std / max(window_span, 1e-9)))
        volume_pressure = _clip((float(np.mean(seg_volumes)) / max(avg_volume, 1e-9)) - 0.72) if avg_volume > 0.0 else 0.0

        area_structural_density = _clip((touch_density * 0.30) + (compression * 0.25) + (close_compression * 0.20) + (structural_quality * 0.15) + (volume_pressure * 0.10))
        field_pressure = _clip(meta.get("field_perception_pressure", 0.0))
        field_action_support = _clip(meta.get("field_action_support", 0.0))
        field_focus = _clip(meta.get("field_perception_focus", 0.0))
        field_fragmentation = _clip(meta.get("field_perception_fragmentation", 0.0))
        area_energy_compression = _clip((compression * 0.32) + (volume_pressure * 0.22) + (touch_density * 0.18) + (field_pressure * 0.10) + (1.0 - area_distance) * 0.10)
        area_mcm_resonance = _clip((area_energy_compression * 0.25) + (area_structural_density * 0.24) + (field_action_support * 0.12) + (field_focus * 0.10) + (form_resonance * 0.12) - (field_fragmentation * 0.12))
        area_memory_pull = _clip((form_learning_trust * 0.24) + (variant_bearing_memory * 0.20) + (memory_orientation * 0.18) + (packet_reward * 0.14) - (packet_reorg * 0.14) - (memory_conflict * 0.10) + 0.10)
        area_bearing_quality = _clip((area_structural_density * 0.26) + (area_mcm_resonance * 0.25) + (area_memory_pull * 0.20) + (lookback_bearing_capacity * 0.16) - (old_structure_carryover_risk * 0.18) + 0.10)
        area_afterimage = _clip((area_memory_pull * 0.26) + (area_mcm_resonance * 0.20) + (area_bearing_quality * 0.18) + (area_temporal_distance * 0.20) - (area_recency * 0.10))
        area_zoom_need = _clip((area_energy_compression * 0.25) + ((1.0 - visual_clarity) * 0.18) + ((1.0 - area_bearing_quality) * 0.16) + (area_distance * 0.12) + (memory_conflict * 0.10))
        area_zoom_clarity = _clip((zoom_budget * 0.30) + (visual_clarity * 0.22) + (area_structural_density * 0.18) + (area_mcm_resonance * 0.12) - (area_zoom_need * 0.10) + 0.18)
        area_replay_fit = _clip((replay_budget * 0.28) + (lookback_relevance * 0.20) + (area_memory_pull * 0.18) + (area_bearing_quality * 0.18) - (area_distance * 0.10))
        area_temporal_relevance = _clip((area_recency * 0.34) + (area_bearing_quality * 0.20) + (area_replay_fit * 0.16) + (1.0 - area_distance) * 0.14 - (area_decay * 0.22) - (area_afterimage * 0.08))
        area_present_contact = _clip((area_temporal_relevance * 0.42) + ((1.0 - area_distance) * 0.24) + (area_mcm_resonance * 0.18) + (area_structural_density * 0.12) - (area_afterimage * 0.16))
        area_current_contact = _clip(
            (area_present_contact * 0.24)
            + (area_recency * 0.15)
            + ((1.0 - area_distance) * 0.14)
            + (temporal_self_location * 0.10)
            + (spacetime_regulation_support * 0.08)
            - (area_afterimage * 0.14)
            - (area_decay * 0.08)
        )
        area_future_contact = _clip(
            (future_projection_depth * 0.26)
            + (spacetime_future_bearing * 0.24)
            + (area_bearing_quality * 0.16)
            + (area_replay_fit * 0.12)
            + (area_temporal_relevance * 0.10)
            + (max(0.0, 0.46 - area_current_contact) * 0.08)
            - (area_decay * 0.12)
        )
        area_memory_contact = _clip(
            (memory_experience_depth * 0.28)
            + (spacetime_memory_bearing * 0.24)
            + (area_memory_pull * 0.18)
            + (area_afterimage * 0.12)
            + (area_replay_fit * 0.10)
            + (max(0.0, area_afterimage - area_recency) * 0.08)
            - (old_structure_carryover_risk * 0.12)
        )
        area_future_to_present_readiness = _clip(
            (area_future_contact * 0.24)
            + ((1.0 - area_distance) * 0.18)
            + (area_bearing_quality * 0.16)
            + (area_action_timing_fit if "area_action_timing_fit" in locals() else 0.0) * 0.10
            + (area_temporal_relevance * 0.12)
            + (spacetime_regulation_support * 0.10)
            + (area_mcm_resonance * 0.08)
            - (area_unlocated_pressure if "area_unlocated_pressure" in locals() else 0.0) * 0.10
            - (old_structure_carryover_risk * 0.08)
        )
        area_current_contact = _clip(
            area_current_contact
            + (max(0.0, area_future_to_present_readiness - 0.42) * 0.18)
        )
        area_unlocated_pressure = _clip(
            (spacetime_unlocated_pressure * 0.30)
            + (max(0.0, 0.34 - temporal_self_location) * 0.18)
            + (area_distance * 0.16)
            + (area_decay * 0.12)
            + (memory_conflict * 0.10)
            - (area_current_contact * 0.14)
        )
        area_spacetime_fit = _clip(
            (area_current_contact * 0.24)
            + (area_future_contact * 0.22)
            + (area_memory_contact * 0.18)
            + (spacetime_regulation_support * 0.18)
            + (mcm_spacetime_depth * 0.12)
            - (area_unlocated_pressure * 0.18)
            - (spacetime_reflection_need * 0.08)
        )
        area_temporal_contact_mode = "open_time_contact"
        if area_unlocated_pressure >= 0.30 and area_spacetime_fit < 0.30:
            area_temporal_contact_mode = "unlocated_area_probe"
        elif area_future_to_present_readiness >= 0.46 and area_current_contact >= 0.36 and area_spacetime_fit >= 0.28:
            area_temporal_contact_mode = "maturing_present_area"
        elif area_future_contact >= 0.34 and area_future_contact >= (area_current_contact * 0.72) and area_future_contact >= area_memory_contact:
            area_temporal_contact_mode = "future_area_watch"
        elif area_memory_contact >= 0.28 and area_memory_contact >= (area_current_contact * 0.58):
            area_temporal_contact_mode = "memory_area_recall"
        elif area_current_contact >= max(area_future_contact * 1.10, area_memory_contact * 1.12) and area_current_contact >= 0.42:
            area_temporal_contact_mode = "present_area_contact"
        elif spacetime_regulation_state == "afterimage_reframe":
            area_temporal_contact_mode = "afterimage_area_reframe"
        area_patience_quality = _clip((serotonin_stability * 0.20) + (gaba_inhibition * 0.18) + (area_replay_fit * 0.22) + (area_zoom_clarity * 0.16) - (neurochemical_load * 0.12) + 0.18)
        area_action_timing_fit = _clip((area_present_contact * 0.30) + (area_patience_quality * 0.16) + (area_replay_fit * 0.16) + (area_recency * 0.12) + (area_spacetime_fit * 0.14) - (area_decay * 0.18) - (area_afterimage * 0.08) - (area_unlocated_pressure * 0.08))
        area_order_intention = _clip((area_bearing_quality * 0.25) + (area_mcm_resonance * 0.17) + (area_replay_fit * 0.14) + (area_action_timing_fit * 0.16) + (area_spacetime_fit * 0.12) - (area_zoom_need * 0.10) - (old_structure_carryover_risk * 0.10) - (area_afterimage * 0.08) - (area_unlocated_pressure * 0.06))
        area_invalidity_pressure = _clip((old_structure_carryover_risk * 0.24) + (memory_conflict * 0.20) + (packet_reorg * 0.18) + (area_zoom_need * 0.12) + (area_unlocated_pressure * 0.12) - (area_bearing_quality * 0.14) - (area_spacetime_fit * 0.08))

        area_key = "|".join([
            f"{area_mid:.6f}",
            f"{area_span:.6f}",
            f"{start}",
            str(segment[0].get("timestamp", segment[0].get("open_time", ""))),
        ])
        focus_id = "sa_" + hashlib.sha1(area_key.encode("utf-8")).hexdigest()[:10]
        candidates.append({
            "area_focus_id": focus_id,
            "area_start_index": int(max(0, len(candles) - lookback_window_size + start)),
            "area_end_index": int(max(0, len(candles) - lookback_window_size + start + len(segment) - 1)),
            "area_price_low": float(area_low),
            "area_price_high": float(area_high),
            "area_price_mid": float(area_mid),
            "area_distance_from_price": float(area_distance),
            "area_temporal_distance": float(area_temporal_distance),
            "area_temporal_relevance": float(area_temporal_relevance),
            "area_recency": float(area_recency),
            "area_decay": float(area_decay),
            "area_afterimage": float(area_afterimage),
            "area_present_contact": float(area_present_contact),
            "area_current_contact": float(area_current_contact),
            "area_future_contact": float(area_future_contact),
            "area_memory_contact": float(area_memory_contact),
            "area_unlocated_pressure": float(area_unlocated_pressure),
            "area_spacetime_fit": float(area_spacetime_fit),
            "area_future_to_present_readiness": float(area_future_to_present_readiness),
            "area_temporal_contact_mode": str(area_temporal_contact_mode),
            "area_action_timing_fit": float(area_action_timing_fit),
            "area_structural_density": float(area_structural_density),
            "area_energy_compression": float(area_energy_compression),
            "area_mcm_resonance": float(area_mcm_resonance),
            "area_memory_pull": float(area_memory_pull),
            "area_bearing_quality": float(area_bearing_quality),
            "area_zoom_need": float(area_zoom_need),
            "area_zoom_clarity": float(area_zoom_clarity),
            "area_replay_fit": float(area_replay_fit),
            "area_patience_quality": float(area_patience_quality),
            "area_order_intention": float(area_order_intention),
            "area_invalidity_pressure": float(area_invalidity_pressure),
        })

    candidates = sorted(
        candidates,
        key=lambda item: (
            float(item.get("area_bearing_quality", 0.0) or 0.0)
            + float(item.get("area_replay_fit", 0.0) or 0.0) * 0.46
            + float(item.get("area_zoom_clarity", 0.0) or 0.0) * 0.28
            + float(item.get("area_action_timing_fit", 0.0) or 0.0) * 0.44
            + float(item.get("area_present_contact", 0.0) or 0.0) * 0.22
            + float(item.get("area_spacetime_fit", 0.0) or 0.0) * 0.32
            - float(item.get("area_invalidity_pressure", 0.0) or 0.0) * 0.70
            - float(item.get("area_afterimage", 0.0) or 0.0) * 0.34
        ),
        reverse=True,
    )[:3]
    focus = dict(candidates[0] if candidates else {})

    if not focus:
        state_label = "no_area_focus"
    elif float(focus.get("area_invalidity_pressure", 0.0) or 0.0) >= 0.52:
        state_label = "area_releasing"
    elif float(focus.get("area_zoom_need", 0.0) or 0.0) >= 0.48 and float(focus.get("area_zoom_clarity", 0.0) or 0.0) < 0.44:
        state_label = "area_needs_zoom"
    elif float(focus.get("area_bearing_quality", 0.0) or 0.0) >= 0.46 and float(focus.get("area_replay_fit", 0.0) or 0.0) >= 0.38:
        state_label = "bearing_area_hypothesis"
    elif float(focus.get("area_energy_compression", 0.0) or 0.0) >= 0.52:
        state_label = "compressed_area_attention"
    else:
        state_label = "area_observation"

    pressure_interpretation = _clip(
        (float(focus.get("area_energy_compression", 0.0) or 0.0) * 0.28)
        + (float(focus.get("area_mcm_resonance", 0.0) or 0.0) * 0.22)
        + (lookback_load * 0.12)
        - (float(focus.get("area_patience_quality", 0.0) or 0.0) * 0.16)
    )
    strategic_patience = _clip(
        (float(focus.get("area_patience_quality", 0.0) or 0.0) * 0.34)
        + (replay_budget * 0.22)
        + (gaba_inhibition * 0.16)
        + (serotonin_stability * 0.16)
        - (pressure_interpretation * 0.16)
    )

    return {
        "strategic_window_state": str(state_label),
        "lookback_window_size": int(lookback_window_size),
        "lookback_load": float(lookback_load),
        "lookback_relevance": float(lookback_relevance),
        "lookback_bearing_capacity": float(lookback_bearing_capacity),
        "replay_budget": float(replay_budget),
        "zoom_budget": float(zoom_budget),
        "old_structure_carryover_risk": float(old_structure_carryover_risk),
        "strategic_pressure_interpretation": float(pressure_interpretation),
        "strategic_patience": float(strategic_patience),
        "area_candidate_count": int(len(candidates)),
        "area_focus_candidates": [dict(item) for item in candidates],
        "area_focus_id": str(focus.get("area_focus_id", "-") or "-"),
        "area_price_low": float(focus.get("area_price_low", 0.0) or 0.0),
        "area_price_high": float(focus.get("area_price_high", 0.0) or 0.0),
        "area_price_mid": float(focus.get("area_price_mid", 0.0) or 0.0),
        "area_distance_from_price": float(focus.get("area_distance_from_price", 0.0) or 0.0),
        "area_temporal_distance": float(focus.get("area_temporal_distance", 0.0) or 0.0),
        "area_temporal_relevance": float(focus.get("area_temporal_relevance", 0.0) or 0.0),
        "area_recency": float(focus.get("area_recency", 0.0) or 0.0),
        "area_decay": float(focus.get("area_decay", 0.0) or 0.0),
        "area_afterimage": float(focus.get("area_afterimage", 0.0) or 0.0),
        "area_present_contact": float(focus.get("area_present_contact", 0.0) or 0.0),
        "area_current_contact": float(focus.get("area_current_contact", 0.0) or 0.0),
        "area_future_contact": float(focus.get("area_future_contact", 0.0) or 0.0),
        "area_memory_contact": float(focus.get("area_memory_contact", 0.0) or 0.0),
        "area_unlocated_pressure": float(focus.get("area_unlocated_pressure", 0.0) or 0.0),
        "area_spacetime_fit": float(focus.get("area_spacetime_fit", 0.0) or 0.0),
        "area_future_to_present_readiness": float(focus.get("area_future_to_present_readiness", 0.0) or 0.0),
        "area_temporal_contact_mode": str(focus.get("area_temporal_contact_mode", "open_time_contact") or "open_time_contact"),
        "area_action_timing_fit": float(focus.get("area_action_timing_fit", 0.0) or 0.0),
        "area_structural_density": float(focus.get("area_structural_density", 0.0) or 0.0),
        "area_energy_compression": float(focus.get("area_energy_compression", 0.0) or 0.0),
        "area_mcm_resonance": float(focus.get("area_mcm_resonance", 0.0) or 0.0),
        "area_memory_pull": float(focus.get("area_memory_pull", 0.0) or 0.0),
        "area_bearing_quality": float(focus.get("area_bearing_quality", 0.0) or 0.0),
        "area_zoom_need": float(focus.get("area_zoom_need", 0.0) or 0.0),
        "area_zoom_clarity": float(focus.get("area_zoom_clarity", 0.0) or 0.0),
        "area_replay_fit": float(focus.get("area_replay_fit", 0.0) or 0.0),
        "area_patience_quality": float(focus.get("area_patience_quality", 0.0) or 0.0),
        "area_order_intention": float(focus.get("area_order_intention", 0.0) or 0.0),
        "area_invalidity_pressure": float(focus.get("area_invalidity_pressure", 0.0) or 0.0),
    }

def _record_strategic_window_protocol(bot, runtime_result):

    if bot is None:
        return None

    if not bool(getattr(Config, "MCM_STRATEGIC_WINDOW_PROTOCOL_DEBUG", True)):
        return None

    result = dict(runtime_result or {})
    state = dict(result.get("strategic_window_state", getattr(bot, "strategic_window_state", {}) or {}) or {})
    if not state:
        return None

    meta = dict(result.get("meta_regulation_state", getattr(bot, "meta_regulation_state", {}) or {}) or {})
    timestamp = result.get("timestamp", getattr(bot, "current_timestamp", None))
    sequence = int(getattr(bot, "mcm_strategic_window_protocol_sequence", 0) or 0) + 1
    setattr(bot, "mcm_strategic_window_protocol_sequence", int(sequence))

    path = dbr_path("mcm_strategic_window_protocol.csv")
    if path not in _STRATEGIC_WINDOW_PROTOCOL_HEADER_DONE:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header_text = (
            "timestamp;sequence;decision;phase;reason;strategic_window_state;lookback_window_size;"
            "lookback_load;lookback_relevance;lookback_bearing_capacity;replay_budget;zoom_budget;"
            "old_structure_carryover_risk;strategic_pressure_interpretation;strategic_patience;"
            "area_candidate_count;area_focus_id;area_price_low;area_price_high;area_distance_from_price;"
            "area_temporal_distance;area_temporal_relevance;area_recency;area_decay;area_afterimage;"
            "area_present_contact;area_current_contact;area_future_contact;area_memory_contact;"
            "area_unlocated_pressure;area_spacetime_fit;area_future_to_present_readiness;"
            "area_temporal_contact_mode;area_action_timing_fit;"
            "area_structural_density;area_energy_compression;area_mcm_resonance;area_memory_pull;"
            "area_bearing_quality;area_zoom_need;area_zoom_clarity;area_replay_fit;area_patience_quality;"
            "area_order_intention;area_invalidity_pressure;pre_action_reorganization_pressure;"
            "pre_action_context_selectivity;effort_state;previous_packet_label;candidates_json\n"
        )
        write_start = time.perf_counter()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header_text)
        dbr_file_write_profile(
            path,
            (time.perf_counter() - write_start) * 1000.0,
            bytes_written=len(header_text.encode("utf-8")),
            operation="strategic_window_protocol_header",
        )
        _STRATEGIC_WINDOW_PROTOCOL_HEADER_DONE.add(path)

    def _clean(value):
        return str(value).replace("\n", " ").replace(";", "|")

    def _num(key, default=0.0):
        try:
            return float(state.get(key, default) or default)
        except Exception:
            return float(default)

    candidates_json = json.dumps(state.get("area_focus_candidates", []) or [], ensure_ascii=False, separators=(",", ":"))
    row = [
        _clean(timestamp),
        int(sequence),
        _clean(result.get("decision", result.get("proposed_decision", "WAIT"))),
        _clean(meta.get("pre_action_phase", "hold")),
        _clean(meta.get("rejection_reason", result.get("rejection_reason", "-"))),
        _clean(state.get("strategic_window_state", "no_area_focus")),
        int(_num("lookback_window_size", 0.0)),
        f"{_num('lookback_load'):.4f}",
        f"{_num('lookback_relevance'):.4f}",
        f"{_num('lookback_bearing_capacity'):.4f}",
        f"{_num('replay_budget'):.4f}",
        f"{_num('zoom_budget'):.4f}",
        f"{_num('old_structure_carryover_risk'):.4f}",
        f"{_num('strategic_pressure_interpretation'):.4f}",
        f"{_num('strategic_patience'):.4f}",
        int(_num("area_candidate_count", 0.0)),
        _clean(state.get("area_focus_id", "-")),
        f"{_num('area_price_low'):.8f}",
        f"{_num('area_price_high'):.8f}",
        f"{_num('area_distance_from_price'):.4f}",
        f"{_num('area_temporal_distance'):.4f}",
        f"{_num('area_temporal_relevance'):.4f}",
        f"{_num('area_recency'):.4f}",
        f"{_num('area_decay'):.4f}",
        f"{_num('area_afterimage'):.4f}",
        f"{_num('area_present_contact'):.4f}",
        f"{_num('area_current_contact'):.4f}",
        f"{_num('area_future_contact'):.4f}",
        f"{_num('area_memory_contact'):.4f}",
        f"{_num('area_unlocated_pressure'):.4f}",
        f"{_num('area_spacetime_fit'):.4f}",
        f"{_num('area_future_to_present_readiness'):.4f}",
        _clean(state.get("area_temporal_contact_mode", "open_time_contact")),
        f"{_num('area_action_timing_fit'):.4f}",
        f"{_num('area_structural_density'):.4f}",
        f"{_num('area_energy_compression'):.4f}",
        f"{_num('area_mcm_resonance'):.4f}",
        f"{_num('area_memory_pull'):.4f}",
        f"{_num('area_bearing_quality'):.4f}",
        f"{_num('area_zoom_need'):.4f}",
        f"{_num('area_zoom_clarity'):.4f}",
        f"{_num('area_replay_fit'):.4f}",
        f"{_num('area_patience_quality'):.4f}",
        f"{_num('area_order_intention'):.4f}",
        f"{_num('area_invalidity_pressure'):.4f}",
        f"{float(meta.get('pre_action_reorganization_pressure', 0.0) or 0.0):.4f}",
        f"{float(meta.get('pre_action_context_selectivity', 0.0) or 0.0):.4f}",
        _clean(meta.get("effort_state", "settled_effort")),
        _clean(meta.get("previous_packet_label", "-")),
        _clean(candidates_json),
    ]
    line = ";".join(str(item) for item in row) + "\n"
    dbr_append_text(
        path,
        line,
        operation="strategic_window_protocol_append",
        extra=f"state={state.get('strategic_window_state', 'no_area_focus')}|focus={state.get('area_focus_id', '-')}",
    )
    return dict(state)

def _record_active_mcm_contact_protocol(bot, runtime_result):

    if bot is None:
        return None

    if not bool(getattr(Config, "MCM_ACTIVE_CONTACT_PROTOCOL_DEBUG", True)):
        return None

    result = dict(runtime_result or {})
    meta = dict(result.get("meta_regulation_state", getattr(bot, "meta_regulation_state", {}) or {}) or {})
    state = dict(result.get("active_mcm_contact_state", getattr(bot, "active_mcm_contact_state", {}) or {}) or {})
    if not state:
        state = dict(meta.get("active_mcm_contact", {}) or {})
    if not state:
        return None

    timestamp = result.get("timestamp", getattr(bot, "current_timestamp", None))
    sequence = int(getattr(bot, "mcm_active_contact_protocol_sequence", 0) or 0) + 1
    setattr(bot, "mcm_active_contact_protocol_sequence", int(sequence))

    path = dbr_path("mcm_active_contact_protocol.csv")
    if path not in _ACTIVE_CONTACT_PROTOCOL_HEADER_DONE:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header_text = (
            "timestamp;sequence;decision;phase;reason;contact_posture;contact_interest;"
            "contact_focus_pull;contact_resonance_probe;outer_inner_resonance;outer_inner_coherence;"
            "inner_change_from_contact;contact_carrying_quality;contact_overcoupling_risk;"
            "contact_release_readiness;contact_deepen_pull;contact_replay_pull;contact_curiosity;"
            "contact_felt_shift;contact_selected_depth;contact_salience;overcoupled_touch_score;"
            "release_contact_score;deepening_contact_score;resonant_contact_score;reflective_contact_score;"
            "curious_touch_score;contact_action_maturity;contact_bearing_gap;contact_impulse_vs_bearing;"
            "contact_learning_need;contact_reality_check;contact_regime_mismatch;contact_stability_carryover;"
            "contact_context_maturity;contact_context_reframe_need;conscious_perception_state;inner_posture_state;"
            "contact_temporal_mode;contact_presentness;contact_future_watch;contact_memory_depth;"
            "contact_unlocated_pressure;contact_temporal_bearing;contact_temporal_reframe_need;"
            "contact_future_to_present_readiness;"
            "strategic_window_state;area_temporal_contact_mode;area_spacetime_fit;"
            "area_profile_state;area_multisensory_coherence;area_attention_need;area_felt_depth;"
            "area_perception_overcoupling_risk;area_selective_contact_pull;"
            "area_selective_feel_permission;area_selective_feel_risk;"
            "area_bearing_quality;area_order_intention;perceptual_distance;"
            "object_contact_depth;field_attachment;release_capacity;inner_outer_alignment\n"
        )
        write_start = time.perf_counter()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header_text)
        dbr_file_write_profile(
            path,
            (time.perf_counter() - write_start) * 1000.0,
            bytes_written=len(header_text.encode("utf-8")),
            operation="active_contact_protocol_header",
        )
        _ACTIVE_CONTACT_PROTOCOL_HEADER_DONE.add(path)

    def _clean(value):
        return str(value).replace("\n", " ").replace(";", "|")

    def _num(key, default=0.0):
        try:
            return float(state.get(key, meta.get(key, default)) or default)
        except Exception:
            return float(default)

    row = [
        _clean(timestamp),
        int(sequence),
        _clean(result.get("decision", result.get("proposed_decision", meta.get("decision", "WAIT")))),
        _clean(meta.get("pre_action_phase", "hold")),
        _clean(meta.get("rejection_reason", result.get("rejection_reason", "-"))),
        _clean(state.get("contact_posture", "background_scan")),
        f"{_num('contact_interest'):.4f}",
        f"{_num('contact_focus_pull'):.4f}",
        f"{_num('contact_resonance_probe'):.4f}",
        f"{_num('outer_inner_resonance'):.4f}",
        f"{_num('outer_inner_coherence'):.4f}",
        f"{_num('inner_change_from_contact'):.4f}",
        f"{_num('contact_carrying_quality'):.4f}",
        f"{_num('contact_overcoupling_risk'):.4f}",
        f"{_num('contact_release_readiness'):.4f}",
        f"{_num('contact_deepen_pull'):.4f}",
        f"{_num('contact_replay_pull'):.4f}",
        f"{_num('contact_curiosity'):.4f}",
        f"{_num('contact_felt_shift'):.4f}",
        f"{_num('contact_selected_depth'):.4f}",
        f"{_num('contact_salience'):.4f}",
        f"{_num('overcoupled_touch_score'):.4f}",
        f"{_num('release_contact_score'):.4f}",
        f"{_num('deepening_contact_score'):.4f}",
        f"{_num('resonant_contact_score'):.4f}",
        f"{_num('reflective_contact_score'):.4f}",
        f"{_num('curious_touch_score'):.4f}",
        f"{_num('contact_action_maturity'):.4f}",
        f"{_num('contact_bearing_gap'):.4f}",
        f"{_num('contact_impulse_vs_bearing'):.4f}",
        f"{_num('contact_learning_need'):.4f}",
        f"{_num('contact_reality_check'):.4f}",
        f"{_num('contact_regime_mismatch'):.4f}",
        f"{_num('contact_stability_carryover'):.4f}",
        f"{_num('contact_context_maturity'):.4f}",
        f"{_num('contact_context_reframe_need'):.4f}",
        _clean(meta.get("conscious_perception_state", "-")),
        _clean(meta.get("inner_posture_state", "-")),
        _clean(state.get("contact_temporal_mode", "open_time_contact")),
        f"{_num('contact_presentness'):.4f}",
        f"{_num('contact_future_watch'):.4f}",
        f"{_num('contact_memory_depth'):.4f}",
        f"{_num('contact_unlocated_pressure'):.4f}",
        f"{_num('contact_temporal_bearing'):.4f}",
        f"{_num('contact_temporal_reframe_need'):.4f}",
        f"{_num('contact_future_to_present_readiness'):.4f}",
        _clean(meta.get("strategic_window_state", "-")),
        _clean(state.get("area_temporal_contact_mode", meta.get("area_temporal_contact_mode", "open_time_contact"))),
        f"{_num('area_spacetime_fit'):.4f}",
        _clean(state.get("area_profile_state", meta.get("area_profile_state", "background_area_perception"))),
        f"{_num('area_multisensory_coherence'):.4f}",
        f"{_num('area_attention_need'):.4f}",
        f"{_num('area_felt_depth'):.4f}",
        f"{_num('area_perception_overcoupling_risk'):.4f}",
        f"{_num('area_selective_contact_pull'):.4f}",
        f"{_num('area_selective_feel_permission'):.4f}",
        f"{_num('area_selective_feel_risk'):.4f}",
        f"{float(meta.get('area_bearing_quality', 0.0) or 0.0):.4f}",
        f"{float(meta.get('area_order_intention', 0.0) or 0.0):.4f}",
        f"{float(meta.get('perceptual_distance', 0.0) or 0.0):.4f}",
        f"{float(meta.get('object_contact_depth', 0.0) or 0.0):.4f}",
        f"{float(meta.get('field_attachment', 0.0) or 0.0):.4f}",
        f"{float(meta.get('release_capacity', 0.0) or 0.0):.4f}",
        f"{float(meta.get('inner_outer_alignment', 0.0) or 0.0):.4f}",
    ]
    line = ";".join(str(item) for item in row) + "\n"
    dbr_append_text(
        path,
        line,
        operation="active_contact_protocol_append",
        extra=f"posture={state.get('contact_posture', 'background_scan')}",
    )
    return dict(state)

def _record_neuro_transition_protocol(bot, runtime_result, current_window=None):

    if bot is None:
        return None

    if not bool(getattr(Config, "MCM_NEURO_TRANSITION_PROTOCOL_DEBUG", True)):
        return None

    result = dict(runtime_result or {})
    meta = dict(result.get("meta_regulation_state", {}) or getattr(bot, "meta_regulation_state", {}) or {})
    if not meta:
        decision_state = dict(getattr(bot, "mcm_runtime_decision_state", {}) or {})
        entry_result = dict(decision_state.get("entry_result", {}) or {})
        meta = dict(entry_result.get("meta_regulation_state", {}) or {})
        result = dict(entry_result or result)

    tone = str(meta.get("neurochemical_dominant_tone", "-") or "-").strip()
    timestamp = result.get("timestamp", getattr(bot, "current_timestamp", None))
    if not tone or tone == "-" or timestamp is None:
        return None

    window = [dict(item or {}) for item in list(current_window or []) if isinstance(item, dict)]
    if not window:
        world_state = dict(result.get("world_state", {}) or {})
        window = [dict(item or {}) for item in list(world_state.get("window", []) or []) if isinstance(item, dict)]

    protocol = dict(getattr(bot, "mcm_neuro_transition_protocol", {}) or {})
    pending = [dict(item or {}) for item in list(protocol.get("pending", []) or []) if isinstance(item, dict)]
    context = max(1, int(getattr(Config, "MCM_NEURO_TRANSITION_PROTOCOL_CONTEXT", 2) or 2))

    def _clean(value):
        return str(value).replace("\n", " ").replace(";", "|")

    def _float(value, default=0.0):
        try:
            return float(value)
        except Exception:
            return float(default)

    def _candle_timestamp(candle):
        item = dict(candle or {})
        value = item.get("timestamp", item.get("timestamp_ms", item.get("time", item.get("open_time", None))))
        if value is None:
            return None
        return str(value)

    def _candle_float(candle, key):
        item = dict(candle or {})
        return _float(item.get(key, item.get(key.capitalize(), 0.0)), 0.0)

    def _find_index_by_timestamp(items, ts):
        target = str(ts)
        for idx, candle in enumerate(list(items or [])):
            if _candle_timestamp(candle) == target:
                return idx
        return -1

    def _avg(values):
        clean_values = [_float(value, 0.0) for value in list(values or [])]
        clean_values = [value for value in clean_values if value == value]
        if not clean_values:
            return 0.0
        return float(sum(clean_values) / len(clean_values))

    def _row_for_event(event, candles, idx):
        transition_candle = dict(candles[idx] or {})
        pre2 = dict(candles[idx - 2] or {}) if idx >= 2 else {}
        pre1 = dict(candles[idx - 1] or {}) if idx >= 1 else {}
        post1 = dict(candles[idx + 1] or {}) if (idx + 1) < len(candles) else {}
        post2 = dict(candles[idx + 2] or {}) if (idx + 2) < len(candles) else {}
        before = list(candles[max(0, idx - 48):idx])

        close = _candle_float(transition_candle, "close")
        open_price = _candle_float(transition_candle, "open")
        high = _candle_float(transition_candle, "high")
        low = _candle_float(transition_candle, "low")
        volume = _candle_float(transition_candle, "volume")
        pre2_close = _candle_float(pre2, "close")
        pre1_close = _candle_float(pre1, "close")
        post1_close = _candle_float(post1, "close")
        post2_close = _candle_float(post2, "close")

        base_price = abs(close) if abs(close) > 1e-12 else 1.0
        pre_ret = (close - pre2_close) / (abs(pre2_close) if abs(pre2_close) > 1e-12 else base_price) if pre2_close else 0.0
        post_ret = (post2_close - close) / base_price if post2_close else 0.0
        window_ret = (post2_close - pre2_close) / (abs(pre2_close) if abs(pre2_close) > 1e-12 else base_price) if pre2_close and post2_close else 0.0
        body_pct = (close - open_price) / base_price if open_price else 0.0
        range_pct = (high - low) / base_price if high or low else 0.0
        volume_baseline = _avg([_candle_float(item, "volume") for item in before]) or volume or 1.0
        range_baseline = _avg([
            (_candle_float(item, "high") - _candle_float(item, "low")) / (abs(_candle_float(item, "close")) if abs(_candle_float(item, "close")) > 1e-12 else 1.0)
            for item in before
        ]) or range_pct or 1.0
        volume_ratio = volume / volume_baseline if volume_baseline else 0.0
        range_ratio = range_pct / range_baseline if range_baseline else 0.0
        direction_flip = 1 if (pre_ret > 0.0 > post_ret) or (pre_ret < 0.0 < post_ret) else 0

        before_meta = dict(event.get("from_meta", {}) or {})
        after_meta = dict(event.get("to_meta", {}) or {})

        def _delta(key):
            return _float(after_meta.get(key, 0.0), 0.0) - _float(before_meta.get(key, 0.0), 0.0)

        row = [
            _clean(event.get("timestamp", "")),
            int(event.get("runtime_tick", 0) or 0),
            int(event.get("sequence", 0) or 0),
            _clean(event.get("from_tone", "-")),
            _clean(event.get("to_tone", "-")),
            _clean(event.get("transition_key", "-")),
            _clean(event.get("phase", "hold")),
            _clean(event.get("reason", "-")),
            _clean(event.get("decision", "WAIT")),
            f"{open_price:.6f}",
            f"{high:.6f}",
            f"{low:.6f}",
            f"{close:.6f}",
            f"{volume:.6f}",
            f"{pre2_close:.6f}",
            f"{pre1_close:.6f}",
            f"{post1_close:.6f}",
            f"{post2_close:.6f}",
            f"{pre_ret:.6f}",
            f"{post_ret:.6f}",
            f"{window_ret:.6f}",
            f"{abs(window_ret):.6f}",
            int(direction_flip),
            f"{volume_ratio:.4f}",
            f"{range_pct:.6f}",
            f"{range_ratio:.4f}",
            f"{body_pct:.6f}",
            f"{_delta('serotonin_stability'):.4f}",
            f"{_delta('glutamate_activation'):.4f}",
            f"{_delta('cortisol_load'):.4f}",
            f"{_delta('gaba_inhibition'):.4f}",
            f"{_delta('dopamine_tone'):.4f}",
            f"{_delta('acetylcholine_focus'):.4f}",
            f"{_delta('noradrenaline_arousal'):.4f}",
            f"{_delta('endorphin_relief'):.4f}",
            f"{_delta('neurochemical_load'):.4f}",
            f"{_delta('neurochemical_support'):.4f}",
            f"{_delta('neurochemical_balance'):.4f}",
            f"{_delta('serotonin_carryover_risk'):.4f}",
            f"{_delta('emotional_decoupling'):.4f}",
            f"{_delta('reactive_nervous_drive'):.4f}",
            f"{_delta('field_perception_pressure'):.4f}",
            f"{_delta('field_perception_clarity'):.4f}",
            f"{_delta('field_observation_need'):.4f}",
            f"{_delta('field_replan_pressure'):.4f}",
            f"{_delta('field_action_support'):.4f}",
            f"{_delta('action_inhibition'):.4f}",
            f"{_delta('action_clearance'):.4f}",
            f"{_float(after_meta.get('serotonin_stability', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('glutamate_activation', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('cortisol_load', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('neurochemical_balance', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('serotonin_carryover_risk', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('emotional_decoupling', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('reactive_nervous_drive', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('field_perception_pressure', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('field_perception_clarity', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('action_inhibition', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('action_clearance', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('visual_action_uncertainty', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('variant_learning_pressure', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('structure_quality', 0.0), 0.0):.4f}",
            f"{_float(after_meta.get('context_confidence', 0.0), 0.0):.4f}",
        ]
        return row

    path = dbr_path("mcm_neuro_transition_protocol.csv")
    if path not in _NEURO_TRANSITION_PROTOCOL_HEADER_DONE:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header_text = (
            "timestamp;runtime_tick;sequence;from_tone;to_tone;transition_key;phase;reason;decision;"
            "open;high;low;close;volume;pre2_close;pre1_close;post1_close;post2_close;"
            "pre_ret;post_ret;window_ret;abs_window_ret;direction_flip;volume_ratio;range_pct;range_ratio;body_pct;"
            "serotonin_delta;glutamate_delta;cortisol_delta;gaba_delta;dopamine_delta;acetylcholine_delta;"
            "noradrenaline_delta;endorphin_delta;neurochemical_load_delta;neurochemical_support_delta;neurochemical_balance_delta;"
            "serotonin_carryover_risk_delta;emotional_decoupling_delta;reactive_nervous_drive_delta;"
            "field_pressure_delta;field_clarity_delta;field_observation_need_delta;field_replan_pressure_delta;"
            "field_action_support_delta;action_inhibition_delta;action_clearance_delta;"
            "serotonin_stability;glutamate_activation;cortisol_load;neurochemical_balance;"
            "serotonin_carryover_risk;emotional_decoupling;reactive_nervous_drive;"
            "field_pressure;field_clarity;action_inhibition;action_clearance;visual_action_uncertainty;"
            "variant_learning_pressure;structure_quality;context_confidence\n"
        )
        write_start = time.perf_counter()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header_text)
        dbr_file_write_profile(
            path,
            (time.perf_counter() - write_start) * 1000.0,
            bytes_written=len(header_text.encode("utf-8")),
            operation="neuro_transition_protocol_header",
        )
        _NEURO_TRANSITION_PROTOCOL_HEADER_DONE.add(path)

    flushed = []
    remaining = []
    for event in pending:
        idx = _find_index_by_timestamp(window, event.get("timestamp", None))
        if idx >= context and (idx + context) < len(window):
            flushed.append(_row_for_event(event, window, idx))
        else:
            remaining.append(dict(event))

    if flushed:
        payload = "".join(";".join(str(item) for item in row) + "\n" for row in flushed)
        dbr_append_text(
            path,
            payload,
            operation="neuro_transition_protocol_append",
            extra=f"flushed={len(flushed)}",
        )

    last_tone = str(protocol.get("last_tone", "") or "")
    last_timestamp = protocol.get("last_timestamp", None)
    last_meta = dict(protocol.get("last_meta", {}) or {})
    timestamp_changed = bool(str(last_timestamp) != str(timestamp))
    tone_changed = bool(last_tone and last_tone != tone and timestamp_changed)

    if tone_changed:
        sequence = int(protocol.get("sequence", 0) or 0) + 1
        event = {
            "timestamp": timestamp,
            "runtime_tick": int(getattr(bot, "mcm_runtime_market_ticks", 0) or 0),
            "sequence": int(sequence),
            "from_tone": str(last_tone),
            "to_tone": str(tone),
            "transition_key": f"{last_tone}->{tone}",
            "phase": str(meta.get("pre_action_phase", result.get("decision_tendency", "hold")) or "hold"),
            "reason": str(meta.get("rejection_reason", result.get("rejection_reason", "-")) or "-"),
            "decision": str(meta.get("decision", result.get("proposed_decision", result.get("decision", "WAIT"))) or "WAIT"),
            "from_meta": dict(last_meta or {}),
            "to_meta": dict(meta or {}),
        }
        idx = _find_index_by_timestamp(window, timestamp)
        if idx >= context and (idx + context) < len(window):
            row = _row_for_event(event, window, idx)
            dbr_append_text(
                path,
                ";".join(str(item) for item in row) + "\n",
                operation="neuro_transition_protocol_append",
                extra=f"transition={event['transition_key']}",
            )
        else:
            remaining.append(dict(event))
        protocol["sequence"] = int(sequence)

    protocol.update({
        "last_tone": str(tone),
        "last_timestamp": timestamp,
        "last_meta": dict(meta or {}),
        "pending": list(remaining[-128:]),
        "last_pending_count": int(len(remaining[-128:])),
    })
    setattr(bot, "mcm_neuro_transition_protocol", dict(protocol))
    return dict(protocol)

__all__ = [
    "_record_active_mcm_contact_protocol",
    "_record_field_decision_protocol",
    "_record_form_symbol_protocol",
    "_record_memory_thinking_protocol",
    "_record_neuro_transition_protocol",
    "_record_strategic_window_protocol",
    "_record_thought_digest_protocol",
    "_record_thought_landkarte_protocol",
    "_record_thought_seed_protocol",
]
