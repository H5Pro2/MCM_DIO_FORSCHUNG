"""Field, topology, and neuron snapshot helpers.

These functions prepare read-only debug/visualization views of the MCM field.
They do not mutate the brain or change decision mechanics.
"""

from __future__ import annotations

import numpy as np

from config import Config


def _clip01(value):
    return max(0.0, min(1.0, float(value or 0.0)))


def _vector_norm(values):
    array = np.asarray(values, dtype=float).ravel()
    if array.size <= 0:
        return 0.0
    return float(float(np.dot(array, array)) ** 0.5)


def _snapshot_field_topology_layout(field, limit=96, field_snapshot=None):

    layout_state = {
        "topology_rows": 0,
        "topology_cols": 0,
        "topology_position_count": 0,
        "topology_neighbor_link_count": 0,
        "topology_neighbor_count_mean": 0.0,
        "topology_neighbor_count_max": 0,
        "topology_positions": [],
        "topology_links": [],
    }

    field_snapshot = dict(field_snapshot or {}) if isinstance(field_snapshot, dict) else {}

    if field_snapshot:
        positions = np.asarray(field_snapshot.get("topology_positions", []), dtype=float)
        neighbor_map = dict(field_snapshot.get("topology_neighbor_indices", {}) or {})
        topology_rows = int(field_snapshot.get("topology_rows", 0) or 0)
        topology_cols = int(field_snapshot.get("topology_cols", 0) or 0)
    elif field is not None:
        positions = np.asarray(getattr(field, "topology_positions", []), dtype=float)
        neighbor_map = dict(getattr(field, "topology_neighbor_indices", {}) or {})
        topology_rows = int(getattr(field, "topology_rows", 0) or 0)
        topology_cols = int(getattr(field, "topology_cols", 0) or 0)
    else:
        return dict(layout_state or {})

    if positions.ndim != 2 or len(positions) <= 0:
        return dict(layout_state or {})

    position_count = int(len(positions))
    sample_limit = max(1, int(getattr(Config, "MCM_SNAPSHOT_TOPOLOGY_LIMIT", limit) or limit))

    if position_count <= sample_limit:
        indices = list(range(position_count))
    else:
        indices = []
        for value in np.linspace(0, position_count - 1, num=sample_limit):
            index = int(round(float(value)))
            if index not in indices:
                indices.append(index)

    index_set = set(int(item) for item in list(indices or []))
    topology_positions = []
    topology_links = []
    neighbor_counts = []

    for index in range(position_count):
        raw_neighbors = []

        for neighbor_index in list(neighbor_map.get(int(index), neighbor_map.get(str(index), [])) or []):
            try:
                resolved_neighbor = int(neighbor_index)
            except Exception:
                continue

            if resolved_neighbor < 0 or resolved_neighbor >= position_count:
                continue

            if resolved_neighbor == int(index):
                continue

            raw_neighbors.append(int(resolved_neighbor))

        neighbor_counts.append(int(len(raw_neighbors)))

        if int(index) not in index_set:
            continue

        topology_positions.append(
            {
                "agent_index": int(index),
                "field_position": _snapshot_float_vector(positions[int(index)]),
                "topology_neighbors": [int(item) for item in list(raw_neighbors or [])],
            }
        )

        for neighbor_index in list(raw_neighbors or []):
            if int(neighbor_index) not in index_set:
                continue

            if int(index) >= int(neighbor_index):
                continue

            topology_links.append(
                {
                    "source": int(index),
                    "target": int(neighbor_index),
                    "distance": _vector_norm(positions[int(index)] - positions[int(neighbor_index)]),
                }
            )

    layout_state = {
        "topology_rows": int(topology_rows),
        "topology_cols": int(topology_cols),
        "topology_position_count": int(position_count),
        "topology_neighbor_link_count": int(sum(neighbor_counts)),
        "topology_neighbor_count_mean": float(np.mean(neighbor_counts)) if neighbor_counts else 0.0,
        "topology_neighbor_count_max": int(max(neighbor_counts)) if neighbor_counts else 0,
        "topology_positions": list(topology_positions or []),
        "topology_links": list(topology_links or []),
    }

    return dict(layout_state or {})


def _build_field_topology_state(snapshot):

    snap = dict(snapshot or {})
    cluster_links = [dict(item or {}) for item in list(snap.get("field_cluster_links", []) or []) if isinstance(item, dict)]
    areal_links = [dict(item or {}) for item in list(snap.get("field_areal_links", []) or []) if isinstance(item, dict)]

    cluster_count = max(0, int(snap.get("cluster_count", snap.get("field_cluster_count", 0)) or 0))
    areal_count = max(0, int(snap.get("field_areal_count", 0) or 0))

    cluster_link_count = int(len(cluster_links))
    areal_link_count = int(len(areal_links))

    cluster_possible = float(cluster_count * max(0, cluster_count - 1) / 2.0)
    areal_possible = float(areal_count * max(0, areal_count - 1) / 2.0)

    cluster_link_density = float(cluster_link_count / cluster_possible) if cluster_possible > 0.0 else 0.0
    areal_link_density = float(areal_link_count / areal_possible) if areal_possible > 0.0 else 0.0

    cluster_distances = [float(item.get("distance", 0.0) or 0.0) for item in list(cluster_links or [])]
    areal_distances = [float(item.get("distance", 0.0) or 0.0) for item in list(areal_links or [])]
    all_distances = list(cluster_distances or []) + list(areal_distances or [])

    cluster_distance_mean = float(np.mean(cluster_distances)) if cluster_distances else 0.0
    areal_distance_mean = float(np.mean(areal_distances)) if areal_distances else 0.0
    topology_distance_mean = float(np.mean(all_distances)) if all_distances else 0.0

    areal_fragmentation = max(0.0, min(1.0, float(snap.get("field_areal_fragmentation", 0.0) or 0.0)))
    areal_coherence = max(0.0, float(snap.get("field_areal_coherence_mean", 0.0) or 0.0))
    areal_conflict = max(0.0, float(snap.get("field_areal_conflict_mean", 0.0) or 0.0))
    link_density = max(0.0, min(1.0, (cluster_link_density * 0.44) + (areal_link_density * 0.56)))

    topology_coherence = max(
        0.0,
        min(
            1.0,
            (link_density * 0.30)
            + (areal_coherence * 0.42)
            - (areal_fragmentation * 0.28)
            - (areal_conflict * 0.20),
        ),
    )
    topology_tension = max(
        0.0,
        min(
            1.0,
            (areal_fragmentation * 0.38)
            + (areal_conflict * 0.34)
            + (max(0.0, 1.0 - link_density) * 0.18),
        ),
    )

    if topology_tension >= 0.62:
        topology_state_label = "fragmented_topology"
    elif topology_coherence >= 0.54 and link_density >= 0.08:
        topology_state_label = "coherent_topology"
    elif cluster_link_count > 0 or areal_link_count > 0:
        topology_state_label = "linked_topology"
    else:
        topology_state_label = "sparse_topology"

    return {
        "cluster_link_count": int(cluster_link_count),
        "areal_link_count": int(areal_link_count),
        "cluster_link_density": float(cluster_link_density),
        "areal_link_density": float(areal_link_density),
        "link_density": float(link_density),
        "cluster_distance_mean": float(cluster_distance_mean),
        "areal_distance_mean": float(areal_distance_mean),
        "topology_distance_mean": float(topology_distance_mean),
        "topology_coherence": float(topology_coherence),
        "topology_tension": float(topology_tension),
        "topology_state_label": str(topology_state_label),
    }


def _build_neural_felt_state(inner_field_state):

    field_state = dict(inner_field_state or {})
    topology_state = dict(field_state.get("field_topology_state", {}) or {})

    neural_felt_activation = _clip01(field_state.get("field_neuron_activation_mean", 0.0) or 0.0)
    neural_felt_stability = _clip01(field_state.get("field_neuron_stability_mean", 0.0) or 0.0)
    neural_regulation_pressure = _clip01(field_state.get("field_neuron_regulation_pressure_mean", 0.0) or 0.0)
    neural_memory_resonance = _clip01(max(
        float(field_state.get("field_neuron_memory_norm_mean", 0.0) or 0.0),
        float(field_state.get("field_neuron_memory_resonance_mean", 0.0) or 0.0),
    ))
    neural_context_reactivation = _clip01(max(
        float(field_state.get("field_neuron_context_memory_impulse_norm_mean", 0.0) or 0.0),
        float(field_state.get("field_neuron_context_reactivation_mean", 0.0) or 0.0),
    ))
    neural_overload = _clip01(field_state.get("field_neuron_overload_mean", 0.0) or 0.0)
    neural_recovery_tendency = _clip01(field_state.get("field_neuron_recovery_tendency_mean", 0.0) or 0.0)
    neural_coupling_resonance = _clip01(field_state.get("field_neuron_coupling_resonance_mean", 0.0) or 0.0)
    neural_receptivity = _clip01(field_state.get("field_neuron_receptivity_mean", 0.0) or 0.0)
    areal_pressure = _clip01(field_state.get("field_areal_pressure_mean", 0.0) or 0.0)
    areal_coherence = _clip01(field_state.get("field_areal_coherence_mean", 0.0) or 0.0)
    areal_conflict = _clip01(field_state.get("field_areal_conflict_mean", 0.0) or 0.0)
    topology_coherence = _clip01(field_state.get("field_topology_coherence", topology_state.get("topology_coherence", 0.0)) or 0.0)
    topology_tension = _clip01(field_state.get("field_topology_tension", topology_state.get("topology_tension", 0.0)) or 0.0)

    neural_felt_pressure = _clip01(
        (neural_regulation_pressure * 0.34)
        + (areal_pressure * 0.24)
        + (areal_conflict * 0.18)
        + (topology_tension * 0.16)
        + (neural_overload * 0.14)
        + (max(0.0, 1.0 - neural_felt_stability) * 0.08)
    )

    neural_felt_bearing = _clip01(
        (neural_felt_stability * 0.28)
        + (areal_coherence * 0.18)
        + (topology_coherence * 0.18)
        + (neural_memory_resonance * 0.10)
        + (neural_recovery_tendency * 0.10)
        + (neural_coupling_resonance * 0.05)
        + (neural_context_reactivation * 0.08)
        + (max(0.0, 1.0 - neural_felt_pressure) * 0.13)
    )

    if neural_overload >= 0.62 and neural_felt_bearing < 0.48:
        neural_felt_label = "overloaded_neural_felt"
    elif neural_felt_pressure >= 0.62 and neural_felt_bearing < 0.42:
        neural_felt_label = "strained_neural_felt"
    elif neural_context_reactivation >= max(0.035, neural_memory_resonance * 0.35):
        neural_felt_label = "memory_reactivated_neural_felt"
    elif neural_recovery_tendency >= 0.52 and neural_felt_pressure <= 0.50:
        neural_felt_label = "recovering_neural_felt"
    elif neural_coupling_resonance >= 0.42 and areal_coherence >= 0.36:
        neural_felt_label = "coupled_neural_felt"
    elif neural_felt_bearing >= 0.58 and neural_felt_pressure <= 0.42:
        neural_felt_label = "bearing_neural_felt"
    elif topology_tension >= 0.58 or areal_conflict >= 0.58:
        neural_felt_label = "tense_neural_felt"
    elif neural_felt_activation >= 0.58:
        neural_felt_label = "activated_neural_felt"
    else:
        neural_felt_label = "quiet_neural_felt"

    return {
        "neural_felt_activation": float(neural_felt_activation),
        "neural_felt_stability": float(neural_felt_stability),
        "neural_felt_pressure": float(neural_felt_pressure),
        "neural_felt_memory_resonance": float(neural_memory_resonance),
        "neural_felt_context_reactivation": float(neural_context_reactivation),
        "neural_felt_overload": float(neural_overload),
        "neural_felt_recovery_tendency": float(neural_recovery_tendency),
        "neural_felt_coupling_resonance": float(neural_coupling_resonance),
        "neural_felt_receptivity": float(neural_receptivity),
        "neural_felt_topology_coherence": float(topology_coherence),
        "neural_felt_topology_tension": float(topology_tension),
        "neural_felt_bearing": float(neural_felt_bearing),
        "neural_felt_label": str(neural_felt_label),
    }


def _snapshot_float_vector(values, digits=4):

    vector = []

    for value in list(np.asarray(values, dtype=float).tolist() if values is not None else []):
        try:
            vector.append(float(round(float(value), digits)))
        except Exception:
            vector.append(0.0)

    return vector


def _neuron_snapshot_from_object(neuron, index=0):
    if neuron is None:
        return {}

    return {
        "agent_index": int(index),
        "field_position": getattr(neuron, "field_position", []),
        "topology_neighbors": list(getattr(neuron, "topology_neighbors", []) or []),
        "state": getattr(neuron, "state", []),
        "velocity": getattr(neuron, "velocity", []),
        "memory_trace": getattr(neuron, "memory_trace", []),
        "activation": float(getattr(neuron, "activation", 0.0) or 0.0),
        "stability": float(getattr(neuron, "stability", 0.0) or 0.0),
        "regulation_pressure": float(getattr(neuron, "regulation_pressure", 0.0) or 0.0),
        "receptivity": float(getattr(neuron, "receptivity", 1.0) or 1.0),
        "overload": float(getattr(neuron, "overload", 0.0) or 0.0),
        "recovery_tendency": float(getattr(neuron, "recovery_tendency", 0.0) or 0.0),
        "memory_resonance": float(getattr(neuron, "memory_resonance", 0.0) or 0.0),
        "auditory_resonance": float(getattr(neuron, "auditory_resonance", 0.0) or 0.0),
        "auditory_frequency_norm": float(getattr(neuron, "auditory_frequency_norm", 0.0) or 0.0),
        "visual_resonance": float(getattr(neuron, "visual_resonance", 0.0) or 0.0),
        "context_reactivation": float(getattr(neuron, "context_reactivation", 0.0) or 0.0),
        "coupling_resonance": float(getattr(neuron, "coupling_resonance", 0.0) or 0.0),
        "field_perception_weight": float(getattr(neuron, "field_perception_weight", 0.0) or 0.0),
        "activity_label": str(getattr(neuron, "activity_label", "quiet") or "quiet"),
        "activation_components": dict(getattr(neuron, "activation_components", {}) or {}),
        "external_impulse": getattr(neuron, "last_external_impulse", []),
        "auditory_impulse": getattr(neuron, "last_auditory_impulse", []),
        "auditory_aftertone": getattr(neuron, "auditory_aftertone", []),
        "visual_impulse": getattr(neuron, "last_visual_impulse", []),
        "visual_afterimage": getattr(neuron, "visual_afterimage", []),
        "context_memory_impulse": getattr(neuron, "last_context_memory_impulse", []),
        "coupling_force": getattr(neuron, "last_coupling_force", []),
        "regulation_force": getattr(neuron, "last_regulation_force", []),
    }


def _snapshot_agent_field_points(field, limit=48, field_snapshot=None):

    points = []

    if field is None:
        return points

    energy = np.asarray(getattr(field, "energy", []), dtype=float)
    velocity = np.asarray(getattr(field, "velocity", []), dtype=float)

    if len(energy) == 0:
        return points

    neuron_map = {}
    areal_membership = {}
    areal_label_map = {}

    field_snapshot = dict(field_snapshot or {}) if isinstance(field_snapshot, dict) else {}

    for neuron_item in list(field_snapshot.get("neurons", []) or []):
        if not isinstance(neuron_item, dict):
            continue

        try:
            neuron_index = int(neuron_item.get("agent_index", len(neuron_map)))
        except Exception:
            neuron_index = len(neuron_map)

        neuron_map[int(neuron_index)] = dict(neuron_item or {})

    raw_areal_states = list(field_snapshot.get("areal_states", []) or [])
    if not raw_areal_states:
        raw_areal_states = list((getattr(field, "areal_state", {}) or {}).get("areal_states", []) or [])

    for areal_item in list(raw_areal_states or []):
        if not isinstance(areal_item, dict):
            continue

        areal_id = str(areal_item.get("areal_id", "") or "")
        state_label = str(areal_item.get("state_label", "adaptive_areal") or "adaptive_areal")

        for member_index in list(areal_item.get("member_indices", []) or []):
            try:
                resolved_index = int(member_index)
            except Exception:
                continue

            areal_membership[int(resolved_index)] = str(areal_id)
            areal_label_map[int(resolved_index)] = str(state_label)

    sample_limit = max(1, int(getattr(Config, "MCM_SNAPSHOT_AGENT_LIMIT", limit) or limit))

    if len(energy) <= sample_limit:
        indices = list(range(len(energy)))
    else:
        indices = []
        for value in np.linspace(0, len(energy) - 1, num=sample_limit):
            index = int(round(float(value)))
            if index not in indices:
                indices.append(index)

    for index in indices:
        velocity_item = velocity[index] if len(velocity) > index else np.zeros(energy.shape[1], dtype=float)
        neuron_item = dict(neuron_map.get(int(index), {}) or {})
        if not neuron_item:
            neurons = list(getattr(field, "neurons", []) or [])
            if int(index) < len(neurons):
                neuron_item = _neuron_snapshot_from_object(neurons[int(index)], index=int(index))
        memory_trace = np.asarray(neuron_item.get("memory_trace", []), dtype=float)
        coupling_force = np.asarray(neuron_item.get("coupling_force", []), dtype=float)
        regulation_force = np.asarray(neuron_item.get("regulation_force", []), dtype=float)
        external_impulse = np.asarray(neuron_item.get("external_impulse", []), dtype=float)
        auditory_impulse = np.asarray(neuron_item.get("auditory_impulse", []), dtype=float)
        auditory_aftertone = np.asarray(neuron_item.get("auditory_aftertone", []), dtype=float)
        visual_impulse = np.asarray(neuron_item.get("visual_impulse", []), dtype=float)
        visual_afterimage = np.asarray(neuron_item.get("visual_afterimage", []), dtype=float)
        context_memory_impulse = np.asarray(neuron_item.get("context_memory_impulse", []), dtype=float)

        points.append({
            "agent_index": int(index),
            "field_position": _snapshot_float_vector(neuron_item.get("field_position", [])),
            "topology_neighbors": [int(item) for item in list(neuron_item.get("topology_neighbors", []) or [])],
            "position": _snapshot_float_vector(energy[index]),
            "velocity": _snapshot_float_vector(velocity_item),
            "activation": float(neuron_item.get("activation", 0.0) or 0.0),
            "stability": float(neuron_item.get("stability", 0.0) or 0.0),
            "regulation_pressure": float(neuron_item.get("regulation_pressure", 0.0) or 0.0),
            "memory_norm": _vector_norm(memory_trace) if memory_trace.size > 0 else 0.0,
            "coupling_norm": _vector_norm(coupling_force) if coupling_force.size > 0 else 0.0,
            "regulation_force_norm": _vector_norm(regulation_force) if regulation_force.size > 0 else 0.0,
            "external_impulse_norm": _vector_norm(external_impulse) if external_impulse.size > 0 else 0.0,
            "auditory_impulse_norm": _vector_norm(auditory_impulse) if auditory_impulse.size > 0 else 0.0,
            "auditory_resonance": float(neuron_item.get("auditory_resonance", 0.0) or 0.0),
            "auditory_aftertone_norm": _vector_norm(auditory_aftertone) if auditory_aftertone.size > 0 else 0.0,
            "visual_impulse_norm": _vector_norm(visual_impulse) if visual_impulse.size > 0 else 0.0,
            "visual_resonance": float(neuron_item.get("visual_resonance", 0.0) or 0.0),
            "visual_afterimage_norm": _vector_norm(visual_afterimage) if visual_afterimage.size > 0 else 0.0,
            "context_memory_impulse_norm": _vector_norm(context_memory_impulse) if context_memory_impulse.size > 0 else 0.0,
            "areal_id": str(areal_membership.get(int(index), "") or ""),
            "areal_state_label": str(areal_label_map.get(int(index), "") or ""),
        })

    return points


def _snapshot_neuron_population(field, limit=24, field_snapshot=None):

    summary = {
        "neuron_count": 0,
        "neuron_activation_mean": 0.0,
        "neuron_activation_max": 0.0,
        "neuron_stability_mean": 0.0,
        "neuron_regulation_pressure_mean": 0.0,
        "neuron_memory_norm_mean": 0.0,
        "neuron_coupling_norm_mean": 0.0,
        "neuron_regulation_force_norm_mean": 0.0,
        "neuron_external_impulse_norm_mean": 0.0,
        "neuron_auditory_impulse_norm_mean": 0.0,
        "neuron_auditory_resonance_mean": 0.0,
        "neuron_auditory_aftertone_norm_mean": 0.0,
        "neuron_visual_impulse_norm_mean": 0.0,
        "neuron_visual_resonance_mean": 0.0,
        "neuron_visual_afterimage_norm_mean": 0.0,
        "neuron_context_memory_impulse_norm_mean": 0.0,
    }
    population = []

    field_snapshot = dict(field_snapshot or {}) if isinstance(field_snapshot, dict) else {}

    neurons = [dict(item or {}) for item in list(field_snapshot.get("neurons", []) or []) if isinstance(item, dict)]
    if not neurons and field is not None:
        neurons = [
            _neuron_snapshot_from_object(neuron, index=index)
            for index, neuron in enumerate(list(getattr(field, "neurons", []) or []))
        ]
    if not neurons:
        return summary, population

    activation_values = []
    stability_values = []
    regulation_pressure_values = []
    memory_norm_values = []
    coupling_norm_values = []
    regulation_force_norm_values = []
    external_impulse_norm_values = []
    auditory_impulse_norm_values = []
    auditory_resonance_values = []
    auditory_aftertone_norm_values = []
    visual_impulse_norm_values = []
    visual_resonance_values = []
    visual_afterimage_norm_values = []
    context_memory_impulse_norm_values = []
    overload_values = []
    recovery_tendency_values = []
    memory_resonance_values = []
    context_reactivation_values = []
    coupling_resonance_values = []
    receptivity_values = []

    for neuron_index, neuron_item in enumerate(list(neurons or [])):
        memory_trace = np.asarray(neuron_item.get("memory_trace", []), dtype=float)
        coupling_force = np.asarray(neuron_item.get("coupling_force", []), dtype=float)
        regulation_force = np.asarray(neuron_item.get("regulation_force", []), dtype=float)
        external_impulse = np.asarray(neuron_item.get("external_impulse", []), dtype=float)
        auditory_impulse = np.asarray(neuron_item.get("auditory_impulse", []), dtype=float)
        auditory_aftertone = np.asarray(neuron_item.get("auditory_aftertone", []), dtype=float)
        visual_impulse = np.asarray(neuron_item.get("visual_impulse", []), dtype=float)
        visual_afterimage = np.asarray(neuron_item.get("visual_afterimage", []), dtype=float)
        context_memory_impulse = np.asarray(neuron_item.get("context_memory_impulse", []), dtype=float)

        activation_values.append(float(neuron_item.get("activation", 0.0) or 0.0))
        stability_values.append(float(neuron_item.get("stability", 0.0) or 0.0))
        regulation_pressure_values.append(float(neuron_item.get("regulation_pressure", 0.0) or 0.0))
        memory_norm_values.append(_vector_norm(memory_trace) if memory_trace.size > 0 else 0.0)
        coupling_norm_values.append(_vector_norm(coupling_force) if coupling_force.size > 0 else 0.0)
        regulation_force_norm_values.append(_vector_norm(regulation_force) if regulation_force.size > 0 else 0.0)
        external_impulse_norm_values.append(_vector_norm(external_impulse) if external_impulse.size > 0 else 0.0)
        auditory_impulse_norm_values.append(_vector_norm(auditory_impulse) if auditory_impulse.size > 0 else 0.0)
        auditory_resonance_values.append(float(neuron_item.get("auditory_resonance", 0.0) or 0.0))
        auditory_aftertone_norm_values.append(_vector_norm(auditory_aftertone) if auditory_aftertone.size > 0 else 0.0)
        visual_impulse_norm_values.append(_vector_norm(visual_impulse) if visual_impulse.size > 0 else 0.0)
        visual_resonance_values.append(float(neuron_item.get("visual_resonance", 0.0) or 0.0))
        visual_afterimage_norm_values.append(_vector_norm(visual_afterimage) if visual_afterimage.size > 0 else 0.0)
        context_memory_impulse_norm_values.append(_vector_norm(context_memory_impulse) if context_memory_impulse.size > 0 else 0.0)
        overload_values.append(float(neuron_item.get("overload", 0.0) or 0.0))
        recovery_tendency_values.append(float(neuron_item.get("recovery_tendency", 0.0) or 0.0))
        memory_resonance_values.append(float(neuron_item.get("memory_resonance", 0.0) or 0.0))
        context_reactivation_values.append(float(neuron_item.get("context_reactivation", 0.0) or 0.0))
        coupling_resonance_values.append(float(neuron_item.get("coupling_resonance", 0.0) or 0.0))
        receptivity_values.append(float(neuron_item.get("receptivity", 1.0) or 1.0))

    summary = {
        "neuron_count": int(len(neurons)),
        "neuron_activation_mean": float(np.mean(activation_values)) if activation_values else 0.0,
        "neuron_activation_max": float(np.max(activation_values)) if activation_values else 0.0,
        "neuron_stability_mean": float(np.mean(stability_values)) if stability_values else 0.0,
        "neuron_regulation_pressure_mean": float(np.mean(regulation_pressure_values)) if regulation_pressure_values else 0.0,
        "neuron_memory_norm_mean": float(np.mean(memory_norm_values)) if memory_norm_values else 0.0,
        "neuron_coupling_norm_mean": float(np.mean(coupling_norm_values)) if coupling_norm_values else 0.0,
        "neuron_regulation_force_norm_mean": float(np.mean(regulation_force_norm_values)) if regulation_force_norm_values else 0.0,
        "neuron_external_impulse_norm_mean": float(np.mean(external_impulse_norm_values)) if external_impulse_norm_values else 0.0,
        "neuron_auditory_impulse_norm_mean": float(np.mean(auditory_impulse_norm_values)) if auditory_impulse_norm_values else 0.0,
        "neuron_auditory_resonance_mean": float(np.mean(auditory_resonance_values)) if auditory_resonance_values else 0.0,
        "neuron_auditory_aftertone_norm_mean": float(np.mean(auditory_aftertone_norm_values)) if auditory_aftertone_norm_values else 0.0,
        "neuron_visual_impulse_norm_mean": float(np.mean(visual_impulse_norm_values)) if visual_impulse_norm_values else 0.0,
        "neuron_visual_resonance_mean": float(np.mean(visual_resonance_values)) if visual_resonance_values else 0.0,
        "neuron_visual_afterimage_norm_mean": float(np.mean(visual_afterimage_norm_values)) if visual_afterimage_norm_values else 0.0,
        "neuron_context_memory_impulse_norm_mean": float(np.mean(context_memory_impulse_norm_values)) if context_memory_impulse_norm_values else 0.0,
        "neuron_overload_mean": float(np.mean(overload_values)) if overload_values else 0.0,
        "neuron_recovery_tendency_mean": float(np.mean(recovery_tendency_values)) if recovery_tendency_values else 0.0,
        "neuron_memory_resonance_mean": float(np.mean(memory_resonance_values)) if memory_resonance_values else 0.0,
        "neuron_context_reactivation_mean": float(np.mean(context_reactivation_values)) if context_reactivation_values else 0.0,
        "neuron_coupling_resonance_mean": float(np.mean(coupling_resonance_values)) if coupling_resonance_values else 0.0,
        "neuron_receptivity_mean": float(np.mean(receptivity_values)) if receptivity_values else 0.0,
    }

    sample_limit = max(1, int(getattr(Config, "MCM_SNAPSHOT_NEURON_LIMIT", limit) or limit))

    if len(neurons) <= sample_limit:
        indices = list(range(len(neurons)))
    else:
        indices = []
        for value in np.linspace(0, len(neurons) - 1, num=sample_limit):
            index = int(round(float(value)))
            if index not in indices:
                indices.append(index)

    for index in indices:
        neuron_item = dict(neurons[index] or {})
        memory_trace = np.asarray(neuron_item.get("memory_trace", []), dtype=float)
        coupling_force = np.asarray(neuron_item.get("coupling_force", []), dtype=float)
        regulation_force = np.asarray(neuron_item.get("regulation_force", []), dtype=float)
        external_impulse = np.asarray(neuron_item.get("external_impulse", []), dtype=float)
        auditory_impulse = np.asarray(neuron_item.get("auditory_impulse", []), dtype=float)
        auditory_aftertone = np.asarray(neuron_item.get("auditory_aftertone", []), dtype=float)
        visual_impulse = np.asarray(neuron_item.get("visual_impulse", []), dtype=float)
        visual_afterimage = np.asarray(neuron_item.get("visual_afterimage", []), dtype=float)
        context_memory_impulse = np.asarray(neuron_item.get("context_memory_impulse", []), dtype=float)

        population.append({
            "agent_index": int(neuron_item.get("agent_index", index) or index),
            "field_position": _snapshot_float_vector(neuron_item.get("field_position", [])),
            "topology_neighbors": [int(item) for item in list(neuron_item.get("topology_neighbors", []) or [])],
            "activation": float(neuron_item.get("activation", 0.0) or 0.0),
            "stability": float(neuron_item.get("stability", 0.0) or 0.0),
            "regulation_pressure": float(neuron_item.get("regulation_pressure", 0.0) or 0.0),
            "memory_norm": _vector_norm(memory_trace) if memory_trace.size > 0 else 0.0,
            "coupling_norm": _vector_norm(coupling_force) if coupling_force.size > 0 else 0.0,
            "regulation_force_norm": _vector_norm(regulation_force) if regulation_force.size > 0 else 0.0,
            "external_impulse_norm": _vector_norm(external_impulse) if external_impulse.size > 0 else 0.0,
            "auditory_impulse_norm": _vector_norm(auditory_impulse) if auditory_impulse.size > 0 else 0.0,
            "auditory_resonance": float(neuron_item.get("auditory_resonance", 0.0) or 0.0),
            "auditory_aftertone_norm": _vector_norm(auditory_aftertone) if auditory_aftertone.size > 0 else 0.0,
            "visual_impulse_norm": _vector_norm(visual_impulse) if visual_impulse.size > 0 else 0.0,
            "visual_resonance": float(neuron_item.get("visual_resonance", 0.0) or 0.0),
            "visual_afterimage_norm": _vector_norm(visual_afterimage) if visual_afterimage.size > 0 else 0.0,
            "context_memory_impulse_norm": _vector_norm(context_memory_impulse) if context_memory_impulse.size > 0 else 0.0,
            "overload": float(neuron_item.get("overload", 0.0) or 0.0),
            "recovery_tendency": float(neuron_item.get("recovery_tendency", 0.0) or 0.0),
            "memory_resonance": float(neuron_item.get("memory_resonance", 0.0) or 0.0),
            "context_reactivation": float(neuron_item.get("context_reactivation", 0.0) or 0.0),
            "coupling_resonance": float(neuron_item.get("coupling_resonance", 0.0) or 0.0),
            "receptivity": float(neuron_item.get("receptivity", 1.0) or 1.0),
            "activity_label": str(neuron_item.get("activity_label", "quiet") or "quiet"),
            "activation_components": dict(neuron_item.get("activation_components", {}) or {}),
            "state": _snapshot_float_vector(neuron_item.get("state", [])),
            "velocity": _snapshot_float_vector(neuron_item.get("velocity", [])),
        })

    return summary, population


def _snapshot_areal_population(field, limit=16, field_snapshot=None):

    summary = {
        "areal_count": 0,
        "areal_activation_mean": 0.0,
        "areal_stability_mean": 0.0,
        "areal_pressure_mean": 0.0,
        "areal_drift": 0.0,
        "areal_dominance": 0.0,
        "areal_fragmentation": 0.0,
        "areal_coherence_mean": 0.0,
        "areal_conflict_mean": 0.0,
    }
    areal_states = []
    areal_links = []

    field_snapshot = dict(field_snapshot or {}) if isinstance(field_snapshot, dict) else {}

    if field_snapshot:
        areal_state = dict(field_snapshot.get("areal_state", {}) or {})
    else:
        areal_state = dict(getattr(field, "areal_state", {}) or {}) if field is not None else {}
    raw_areal_states = [dict(item or {}) for item in list(field_snapshot.get("areal_states", []) or []) if isinstance(item, dict)]
    raw_areal_links = [dict(item or {}) for item in list(field_snapshot.get("areal_links", []) or []) if isinstance(item, dict)]
    if not raw_areal_states:
        raw_areal_states = [dict(item or {}) for item in list(areal_state.get("areal_states", []) or []) if isinstance(item, dict)]
    if not raw_areal_links:
        raw_areal_links = [dict(item or {}) for item in list(areal_state.get("areal_links", []) or []) if isinstance(item, dict)]

    summary = {
        "areal_count": int(areal_state.get("areal_count", 0) or 0),
        "areal_activation_mean": float(areal_state.get("areal_activation_mean", 0.0) or 0.0),
        "areal_stability_mean": float(areal_state.get("areal_stability_mean", 0.0) or 0.0),
        "areal_pressure_mean": float(areal_state.get("areal_pressure_mean", 0.0) or 0.0),
        "areal_drift": float(areal_state.get("areal_drift", 0.0) or 0.0),
        "areal_dominance": float(areal_state.get("areal_dominance", 0.0) or 0.0),
        "areal_fragmentation": float(areal_state.get("areal_fragmentation", 0.0) or 0.0),
        "areal_coherence_mean": float(areal_state.get("areal_coherence_mean", 0.0) or 0.0),
        "areal_conflict_mean": float(areal_state.get("areal_conflict_mean", 0.0) or 0.0),
        "areal_topology_density_mean": float(areal_state.get("areal_topology_density_mean", 0.0) or 0.0),
        "areal_topology_span_mean": float(areal_state.get("areal_topology_span_mean", 0.0) or 0.0),
        "areal_topology_boundary_mean": float(areal_state.get("areal_topology_boundary_mean", 0.0) or 0.0),
    }

    sample_limit = max(1, int(getattr(Config, "MCM_SNAPSHOT_AREAL_LIMIT", limit) or limit))

    if len(raw_areal_states) <= sample_limit:
        indices = list(range(len(raw_areal_states)))
    else:
        indices = []
        for value in np.linspace(0, len(raw_areal_states) - 1, num=sample_limit):
            index = int(round(float(value)))
            if index not in indices:
                indices.append(index)

    for index in indices:
        areal_item = dict(raw_areal_states[index] or {})
        areal_states.append({
            "areal_id": str(areal_item.get("areal_id", f"areal_{index}") or f"areal_{index}"),
            "member_indices": [int(item) for item in list(areal_item.get("member_indices", []) or [])],
            "center": _snapshot_float_vector(areal_item.get("center", [])),
            "mean_velocity_vector": _snapshot_float_vector(areal_item.get("mean_velocity_vector", [])),
            "bounds_min": _snapshot_float_vector(areal_item.get("bounds_min", [])),
            "bounds_max": _snapshot_float_vector(areal_item.get("bounds_max", [])),
            "topology_center": _snapshot_float_vector(areal_item.get("topology_center", [])),
            "topology_bounds_min": _snapshot_float_vector(areal_item.get("topology_bounds_min", [])),
            "topology_bounds_max": _snapshot_float_vector(areal_item.get("topology_bounds_max", [])),
            "topology_span": float(areal_item.get("topology_span", 0.0) or 0.0),
            "topology_density": float(areal_item.get("topology_density", 0.0) or 0.0),
            "topology_internal_link_count": int(areal_item.get("topology_internal_link_count", 0) or 0),
            "topology_boundary_link_count": int(areal_item.get("topology_boundary_link_count", 0) or 0),
            "mass": int(areal_item.get("mass", 0) or 0),
            "density": float(areal_item.get("density", 0.0) or 0.0),
            "activation_mean": float(areal_item.get("activation_mean", 0.0) or 0.0),
            "stability_mean": float(areal_item.get("stability_mean", 0.0) or 0.0),
            "pressure_mean": float(areal_item.get("pressure_mean", 0.0) or 0.0),
            "memory_norm_mean": float(areal_item.get("memory_norm_mean", 0.0) or 0.0),
            "coupling_norm_mean": float(areal_item.get("coupling_norm_mean", 0.0) or 0.0),
            "regulation_force_norm_mean": float(areal_item.get("regulation_force_norm_mean", 0.0) or 0.0),
            "external_impulse_norm_mean": float(areal_item.get("external_impulse_norm_mean", 0.0) or 0.0),
            "velocity_mean": float(areal_item.get("velocity_mean", 0.0) or 0.0),
            "coherence": float(areal_item.get("coherence", 0.0) or 0.0),
            "conflict": float(areal_item.get("conflict", 0.0) or 0.0),
            "state_label": str(areal_item.get("state_label", "adaptive_areal") or "adaptive_areal"),
        })

    areal_links = [
        {
            "source_areal_id": str(item.get("source_areal_id", "") or ""),
            "target_areal_id": str(item.get("target_areal_id", "") or ""),
            "distance": float(item.get("distance", 0.0) or 0.0),
            "relation_label": str(item.get("relation_label", "bridged") or "bridged"),
        }
        for item in list(raw_areal_links or [])
    ]

    return summary, areal_states, areal_links


def _snapshot_field_perception_state(field, field_snapshot=None):

    field_snapshot = dict(field_snapshot or {}) if isinstance(field_snapshot, dict) else {}
    if field_snapshot:
        state = dict(field_snapshot.get("field_perception_state", {}) or {})
    else:
        state = dict(getattr(field, "field_perception_state", {}) or {}) if field is not None else {}
    islands = [dict(item or {}) for item in list(field_snapshot.get("activity_islands", state.get("activity_islands", [])) or []) if isinstance(item, dict)]

    return {
        "activity_island_count": int(state.get("activity_island_count", len(islands)) or 0),
        "activity_island_mass_mean": float(state.get("activity_island_mass_mean", 0.0) or 0.0),
        "activity_island_mass_max": float(state.get("activity_island_mass_max", 0.0) or 0.0),
        "activity_island_activation_mean": float(state.get("activity_island_activation_mean", 0.0) or 0.0),
        "activity_island_pressure_mean": float(state.get("activity_island_pressure_mean", 0.0) or 0.0),
        "activity_island_coherence_mean": float(state.get("activity_island_coherence_mean", 0.0) or 0.0),
        "activity_island_context_reactivation_mean": float(state.get("activity_island_context_reactivation_mean", 0.0) or 0.0),
        "activity_island_spread": float(state.get("activity_island_spread", 0.0) or 0.0),
        "field_perception_focus": float(state.get("field_perception_focus", 0.0) or 0.0),
        "field_perception_clarity": float(state.get("field_perception_clarity", state.get("activity_island_coherence_mean", 0.0)) or 0.0),
        "field_perception_stability": float(state.get("field_perception_stability", state.get("activity_island_coherence_mean", 0.0)) or 0.0),
        "field_perception_fragmentation": float(state.get("field_perception_fragmentation", 0.0) or 0.0),
        "field_perception_strain": float(state.get("field_perception_strain", state.get("activity_island_pressure_mean", 0.0)) or 0.0),
        "dominant_activity_island_id": str(state.get("dominant_activity_island_id", "-") or "-"),
        "field_perception_label": str(state.get("field_perception_label", "quiet_field") or "quiet_field"),
        "activity_islands": list(islands or []),
    }


def _snapshot_cluster_centers(clusters):

    payload = []
    center_vectors = []

    for cluster_index, item in enumerate(list(clusters or [])):
        cluster_array = np.asarray(item, dtype=float)

        if len(cluster_array) == 0:
            continue

        center = np.mean(cluster_array, axis=0)
        distances = [
            float(np.linalg.norm(np.asarray(point, dtype=float) - np.asarray(center, dtype=float)))
            for point in cluster_array
        ]
        mean_radius = float(np.mean(distances)) if distances else 0.0
        max_radius = float(max(distances)) if distances else 0.0

        center_vectors.append(np.asarray(center, dtype=float))
        payload.append({
            "cluster_index": int(cluster_index),
            "size": int(len(cluster_array)),
            "center": _snapshot_float_vector(center),
            "mean_radius": float(round(mean_radius, 4)),
            "max_radius": float(round(max_radius, 4)),
        })

    return payload, center_vectors


def _snapshot_cluster_links(center_vectors, limit=12):

    links = []
    if len(list(center_vectors or [])) < 2:
        return links

    candidates = []

    for i in range(len(center_vectors)):
        for j in range(i + 1, len(center_vectors)):
            distance = float(
                np.linalg.norm(
                    np.asarray(center_vectors[i], dtype=float)
                    - np.asarray(center_vectors[j], dtype=float)
                )
            )
            candidates.append((distance, i, j))

    candidates.sort(key=lambda item: float(item[0]))
    link_limit = max(1, int(getattr(Config, "MCM_SNAPSHOT_CLUSTER_LINK_LIMIT", limit) or limit))

    for distance, source_index, target_index in candidates[:link_limit]:
        links.append({
            "source_index": int(source_index),
            "target_index": int(target_index),
            "distance": float(round(distance, 4)),
        })

    return links

