import numpy as np
import random
import time
from config import Config
from debug_tools.writers import dbr_profile
# --------------------------------------------------
Default_N_AGENTS = 160
DIMS = 3
# --------------------------------------------------
# Wahrnehmung
# --------------------------------------------------

class Perception:

    def encode(self, stimulus):
        """Stimulus → Energieimpuls"""

        mapping = {
            "positive": +1.45,
            "negative": -0.65,
            "threat": -1.75,
            "reward": +1.55,
            "neutral": 0.0
        }

        return mapping.get(stimulus, 0.0)
    
# --------------------------------------------------
# MCM SelfModel
# --------------------------------------------------
class SelfModel:

    def evaluate(self, energy):

        mean_e = float(np.mean(energy[:,0]))
        motivation = float(np.mean(energy[:,1]))
        risk = float(np.mean(energy[:,2]))

        state_pressures = {
            "stressed": float(max(0.0, -risk) * 0.46 + max(0.0, abs(mean_e) - 0.20) * 0.08),
            "excited": float(max(0.0, motivation) * 0.42 + max(0.0, mean_e) * 0.10),
            "stable": float(max(0.0, 1.0 - abs(mean_e)) * 0.34 + max(0.0, 1.0 - abs(risk)) * 0.18),
            "active": float(abs(mean_e) * 0.24 + abs(motivation) * 0.16 + max(0.0, 1.0 - abs(risk)) * 0.08),
        }
        self.last_state_pressures = dict(state_pressures)
        return max(state_pressures, key=state_pressures.get)
    
# --------------------------------------------------
# MCM Feld
# --------------------------------------------------

class MCMField:

    def __init__(self, n_agents=Default_N_AGENTS, dims=DIMS):

        self.N = max(1, int(n_agents or Default_N_AGENTS))
        self.D = max(1, int(dims or DIMS))

        self.k_center = 0.0035
        self.coupling = 0.08
        self.noise = 0.18
        self.coupling_sigma = float(getattr(Config, "MCM_FIELD_COUPLING_SIGMA", 0.5) or 0.5)
        self.local_neighbor_count = max(1, int(getattr(Config, "MCM_FIELD_LOCAL_NEIGHBORS", 8) or 8))
        self.max_abs_state = 3.0
        self.areal_radius = float(getattr(Config, "MCM_FIELD_AREAL_RADIUS", 0.78) or 0.78)
        self.areal_min_size = max(2, int(getattr(Config, "MCM_FIELD_AREAL_MIN_SIZE", 3) or 3))
        self.topology_rows, self.topology_cols = self._resolve_fixed_topology_shape()
        self.topology_positions = self._build_fixed_topology_positions()
        self.topology_neighbor_indices = self._build_fixed_topology_neighbor_indices()
        self.topology_neighbor_array = self._build_fixed_topology_neighbor_array()
        self.field_step_seq = 0
        self._last_areal_refresh_seq = -1
        self._runtime_parameter_signature = None

        self.neurons = [MCMNeuron(dims=self.D) for _ in range(self.N)]
        self._assign_fixed_topology_to_neurons()
        self.energy = np.zeros((self.N, self.D), dtype=float)
        self.velocity = np.zeros((self.N, self.D), dtype=float)
        self.areal_state = {
            "areal_count": 0,
            "areal_activation_mean": 0.0,
            "areal_stability_mean": 0.0,
            "areal_pressure_mean": 0.0,
            "areal_drift": 0.0,
            "areal_dominance": 0.0,
            "areal_fragmentation": 0.0,
            "areal_coherence_mean": 0.0,
            "areal_conflict_mean": 0.0,
            "areal_states": [],
            "areal_links": [],
        }
        self.field_perception_state = {
            "activity_island_count": 0,
            "activity_island_mass_mean": 0.0,
            "activity_island_mass_max": 0.0,
            "activity_island_activation_mean": 0.0,
            "activity_island_pressure_mean": 0.0,
            "activity_island_coherence_mean": 0.0,
            "activity_island_context_reactivation_mean": 0.0,
            "activity_island_spread": 0.0,
            "field_perception_focus": 0.0,
            "field_perception_clarity": 0.0,
            "field_perception_stability": 0.0,
            "field_perception_fragmentation": 0.0,
            "field_perception_strain": 0.0,
            "dominant_activity_island_id": "-",
            "field_perception_label": "quiet_field",
            "activity_island_threshold_mode": "adaptive_relative",
            "activity_island_threshold": 0.0,
            "activity_score_mean": 0.0,
            "activity_score_max": 0.0,
            "activity_score_p90": 0.0,
            "activity_islands": [],
        }
        self._last_activity_island_threshold_state = {
            "activity_island_threshold_mode": "adaptive_relative",
            "activity_island_threshold": 0.0,
            "activity_score_mean": 0.0,
            "activity_score_max": 0.0,
            "activity_score_p90": 0.0,
        }
        self.auditory_neural_state = {
            "enabled": False,
            "sense": "hearing",
            "channel": "market_audio_to_neuron",
            "loudness": 0.0,
            "frequency_hz": 0.0,
            "frequency_norm": 0.0,
            "compression": 0.0,
            "overdrive": 0.0,
            "scale": 0.0,
            "resonance_mean": 0.0,
            "resonance_max": 0.0,
            "aftertone_mean": 0.0,
            "tone": "silent_tone",
            "action_permission": 0.0,
        }
        self.visual_neural_state = {
            "enabled": False,
            "sense": "seeing",
            "channel": "market_visual_to_neuron",
            "clarity": 0.0,
            "contact": 0.0,
            "coherence": 0.0,
            "pressure": 0.0,
            "scale": 0.0,
            "resonance_mean": 0.0,
            "resonance_max": 0.0,
            "afterimage_mean": 0.0,
            "form_family": "-",
            "sight_label": "blind_visual_trace",
            "action_permission": 0.0,
        }
        self._last_areal_centers = []
        self._refresh_arrays_from_neurons()
        self._refresh_areal_state(force=True)

    # --------------------------------------------------
    def _field_profile_start(self):
        return time.perf_counter() if bool(getattr(Config, "MCM_RUNTIME_PROFILE_DEBUG", False)) else 0.0

    # --------------------------------------------------
    def _field_profile_debug(self, section, start, extra=None):
        if not start:
            return
        try:
            dbr_profile(
                section,
                (time.perf_counter() - float(start)) * 1000.0,
                extra=extra,
            )
        except Exception:
            pass

    # --------------------------------------------------
    def _propagate_runtime_parameters(self):

        signature = (
            float(self.k_center),
            float(self.coupling),
            float(self.noise),
            float(self.coupling_sigma),
            float(self.max_abs_state),
        )
        if getattr(self, "_runtime_parameter_signature", None) == signature:
            return

        for neuron in list(self.neurons or []):
            neuron.center_force = float(self.k_center)
            neuron.coupling_strength = float(self.coupling)
            neuron.noise_strength = float(self.noise)
            neuron.coupling_sigma = float(self.coupling_sigma)
            neuron.max_abs_state = float(self.max_abs_state)
        self._runtime_parameter_signature = signature

    # --------------------------------------------------
    def _resolve_fixed_topology_shape(self):

        configured_rows = int(getattr(Config, "MCM_FIELD_TOPOLOGY_ROWS", 0) or 0)
        configured_cols = int(getattr(Config, "MCM_FIELD_TOPOLOGY_COLS", 0) or 0)

        if configured_rows > 0 and configured_cols > 0:
            rows = max(1, int(configured_rows))
            cols = max(1, int(configured_cols))
            if rows * cols < self.N:
                cols = int(np.ceil(float(self.N) / max(1.0, float(rows))))
            return int(rows), int(cols)

        cols = max(1, int(np.ceil(np.sqrt(float(self.N)))))
        rows = max(1, int(np.ceil(float(self.N) / max(1.0, float(cols)))))
        return int(rows), int(cols)

    # --------------------------------------------------
    def _build_fixed_topology_positions(self):

        positions = []
        rows = max(1, int(getattr(self, "topology_rows", 1) or 1))
        cols = max(1, int(getattr(self, "topology_cols", 1) or 1))

        for index in range(int(self.N)):
            row = int(index) // cols
            col = int(index) % cols

            if cols > 1:
                x_pos = (float(col) / float(cols - 1)) * 2.0 - 1.0
            else:
                x_pos = 0.0

            if rows > 1:
                y_pos = (float(row) / float(rows - 1)) * 2.0 - 1.0
            else:
                y_pos = 0.0

            positions.append([float(x_pos), float(y_pos)])

        return np.asarray(positions, dtype=float)

    # --------------------------------------------------
    def _build_fixed_topology_neighbor_indices(self):

        neighbor_map = {index: [] for index in range(int(self.N))}
        positions = np.asarray(getattr(self, "topology_positions", []), dtype=float)

        if positions.ndim != 2 or len(positions) <= 1:
            return neighbor_map

        agent_count = min(int(self.N), int(len(positions)))
        local_neighbors = max(1, min(agent_count - 1, int(self.local_neighbor_count or 1)))

        for index in range(agent_count):
            local_delta = positions[:agent_count] - positions[int(index)]
            local_distances = np.linalg.norm(local_delta, axis=1)
            local_distances[int(index)] = np.inf

            if len(local_distances) > local_neighbors + 1:
                order = np.argpartition(local_distances, local_neighbors)[:local_neighbors]
                order = order[np.argsort(local_distances[order])]
            else:
                order = np.argsort(local_distances)

            selected = []

            for neighbor_index in list(order):
                if len(selected) >= local_neighbors:
                    break

                if not np.isfinite(local_distances[int(neighbor_index)]):
                    continue

                selected.append(int(neighbor_index))

            neighbor_map[int(index)] = list(selected or [])

        return neighbor_map

    # --------------------------------------------------
    def _build_fixed_topology_neighbor_array(self):

        neighbor_map = dict(getattr(self, "topology_neighbor_indices", {}) or {})
        arrays = []

        for index in range(int(self.N)):
            cleaned = []
            for neighbor_index in list(neighbor_map.get(int(index), []) or []):
                try:
                    resolved = int(neighbor_index)
                except Exception:
                    continue

                if resolved == int(index):
                    continue
                if resolved < 0 or resolved >= int(self.N):
                    continue

                cleaned.append(int(resolved))

            arrays.append(np.asarray(cleaned, dtype=int))

        return list(arrays or [])

    # --------------------------------------------------
    def _assign_fixed_topology_to_neurons(self):

        positions = np.asarray(getattr(self, "topology_positions", []), dtype=float)
        neighbor_map = dict(getattr(self, "topology_neighbor_indices", {}) or {})

        for index, neuron in enumerate(list(self.neurons or [])):
            neuron.field_index = int(index)

            if positions.ndim == 2 and int(index) < len(positions):
                neuron.field_position = np.asarray(positions[int(index)], dtype=float).copy()
            else:
                neuron.field_position = np.zeros(2, dtype=float)

            neuron.topology_neighbors = [int(item) for item in list(neighbor_map.get(int(index), []) or [])]

    # --------------------------------------------------
    def _sync_neurons_from_arrays(self):

        energy = np.asarray(getattr(self, "energy", []), dtype=float)
        velocity = np.asarray(getattr(self, "velocity", []), dtype=float)

        if energy.shape != (self.N, self.D):
            repaired_energy = np.zeros((self.N, self.D), dtype=float)
            if energy.size > 0:
                rows = min(int(energy.shape[0]) if energy.ndim >= 1 else 0, self.N)
                cols = min(int(energy.shape[1]) if energy.ndim >= 2 else 0, self.D)
                if rows > 0 and cols > 0:
                    repaired_energy[:rows, :cols] = energy[:rows, :cols]
            energy = repaired_energy
            self.energy = np.asarray(energy, dtype=float)

        if velocity.shape != (self.N, self.D):
            repaired_velocity = np.zeros((self.N, self.D), dtype=float)
            if velocity.size > 0:
                rows = min(int(velocity.shape[0]) if velocity.ndim >= 1 else 0, self.N)
                cols = min(int(velocity.shape[1]) if velocity.ndim >= 2 else 0, self.D)
                if rows > 0 and cols > 0:
                    repaired_velocity[:rows, :cols] = velocity[:rows, :cols]
            velocity = repaired_velocity
            self.velocity = np.asarray(velocity, dtype=float)

        for index, neuron in enumerate(list(self.neurons or [])):
            neuron.state = np.asarray(energy[index], dtype=float).copy()
            neuron.velocity = np.asarray(velocity[index], dtype=float).copy()
            neuron._clip_state()

    # --------------------------------------------------
    def _refresh_arrays_from_neurons(self):

        if not self.neurons:
            self.energy = np.zeros((self.N, self.D), dtype=float)
            self.velocity = np.zeros((self.N, self.D), dtype=float)
            return

        self.energy = np.asarray([
            np.asarray(neuron.state, dtype=float).copy()
            for neuron in list(self.neurons or [])
        ], dtype=float)
        self.velocity = np.asarray([
            np.asarray(neuron.velocity, dtype=float).copy()
            for neuron in list(self.neurons or [])
        ], dtype=float)

    # --------------------------------------------------
    def _build_local_neighbor_state_map(self):

        energy = np.asarray(getattr(self, "energy", []), dtype=float)

        if energy.ndim != 2 or len(energy) <= 1:
            return [np.zeros((0, self.D), dtype=float) for _ in range(int(self.N))]

        agent_count = min(int(self.N), int(len(energy)))
        neighbor_arrays = list(getattr(self, "topology_neighbor_array", []) or [])
        if len(neighbor_arrays) < agent_count:
            self.topology_neighbor_array = self._build_fixed_topology_neighbor_array()
            neighbor_arrays = list(getattr(self, "topology_neighbor_array", []) or [])

        neighbor_state_map = []
        empty = np.zeros((0, self.D), dtype=float)

        for index in range(agent_count):
            neighbor_indices = np.asarray(neighbor_arrays[int(index)] if int(index) < len(neighbor_arrays) else [], dtype=int)
            if neighbor_indices.size <= 0:
                neighbor_state_map.append(empty)
                continue

            valid = neighbor_indices[(neighbor_indices >= 0) & (neighbor_indices < agent_count) & (neighbor_indices != int(index))]
            if valid.size <= 0:
                neighbor_state_map.append(empty)
                continue

            local_limit = max(1, int(self.local_neighbor_count or 1))
            neighbor_state_map.append(np.asarray(energy[valid[:local_limit]], dtype=float))

        if agent_count < int(self.N):
            neighbor_state_map.extend([empty for _ in range(int(self.N) - agent_count)])

        return list(neighbor_state_map or [])

    # --------------------------------------------------
    def _norm01_rows(self, values, scale=None):

        matrix = np.asarray(values, dtype=float)
        if matrix.ndim != 2 or matrix.size <= 0:
            return np.zeros((0,), dtype=float)

        resolved_scale = float(scale if scale is not None else max(float(self.max_abs_state or 3.0), 1e-9))
        denom = max(resolved_scale, 1e-9) * max(1.0, float(self.D) ** 0.5)
        return np.clip(np.sqrt(np.einsum("ij,ij->i", matrix, matrix)) / denom, 0.0, 1.0)

    # --------------------------------------------------
    def _alignment_rows(self, left, right):

        left_values = np.asarray(left, dtype=float)
        right_values = np.asarray(right, dtype=float)
        if left_values.ndim != 2 or right_values.ndim != 2 or left_values.shape != right_values.shape:
            return np.zeros((left_values.shape[0] if left_values.ndim == 2 else 0,), dtype=float)

        left_norm = np.sqrt(np.einsum("ij,ij->i", left_values, left_values))
        right_norm = np.sqrt(np.einsum("ij,ij->i", right_values, right_values))
        denom = left_norm * right_norm
        result = np.zeros_like(denom, dtype=float)
        mask = denom > 1e-9
        result[mask] = np.einsum("ij,ij->i", left_values[mask], right_values[mask]) / denom[mask]
        return np.clip(result, -1.0, 1.0)

    # --------------------------------------------------
    def _step_neurons_vectorized(
        self,
        external_step_vector,
        replay_step_vector,
        context_memory_matrix,
        auditory_neural_matrix,
        visual_neural_matrix,
        auditory_frequency_norm=0.0,
    ):

        neurons = list(self.neurons or [])
        neuron_count = int(len(neurons))
        if neuron_count <= 0:
            return

        states = np.asarray(getattr(self, "energy", []), dtype=float)
        velocities = np.asarray(getattr(self, "velocity", []), dtype=float)
        if states.ndim != 2 or len(states) < neuron_count:
            states = np.asarray([np.asarray(getattr(neuron, "state", np.zeros(self.D, dtype=float)), dtype=float) for neuron in neurons], dtype=float)
        if velocities.ndim != 2 or len(velocities) < neuron_count:
            velocities = np.asarray([np.asarray(getattr(neuron, "velocity", np.zeros(self.D, dtype=float)), dtype=float) for neuron in neurons], dtype=float)

        states = np.asarray(states[:neuron_count], dtype=float)
        velocities = np.asarray(velocities[:neuron_count], dtype=float)
        memories = np.asarray([np.asarray(getattr(neuron, "memory_trace", np.zeros(self.D, dtype=float)), dtype=float) for neuron in neurons], dtype=float)
        previous_regulation_pressures = np.asarray([float(getattr(neuron, "regulation_pressure", 0.0) or 0.0) for neuron in neurons], dtype=float)

        external_base = np.asarray(external_step_vector, dtype=float).reshape(1, -1)
        replay_base = np.asarray(replay_step_vector, dtype=float).reshape(1, -1)
        if external_base.shape[1] != self.D:
            repaired = np.zeros((1, self.D), dtype=float)
            repaired[:, : min(self.D, external_base.shape[1])] = external_base[:, : min(self.D, external_base.shape[1])]
            external_base = repaired
        if replay_base.shape[1] != self.D:
            repaired = np.zeros((1, self.D), dtype=float)
            repaired[:, : min(self.D, replay_base.shape[1])] = replay_base[:, : min(self.D, replay_base.shape[1])]
            replay_base = repaired

        context_matrix = np.asarray(context_memory_matrix, dtype=float)
        if context_matrix.ndim != 2 or len(context_matrix) < neuron_count or context_matrix.shape[1] != self.D:
            repaired = np.zeros((neuron_count, self.D), dtype=float)
            if context_matrix.ndim == 2:
                rows = min(neuron_count, context_matrix.shape[0])
                cols = min(self.D, context_matrix.shape[1])
                repaired[:rows, :cols] = context_matrix[:rows, :cols]
            context_matrix = repaired
        else:
            context_matrix = context_matrix[:neuron_count]

        auditory_matrix = np.asarray(auditory_neural_matrix, dtype=float)
        if auditory_matrix.ndim != 2 or len(auditory_matrix) < neuron_count or auditory_matrix.shape[1] != self.D:
            repaired = np.zeros((neuron_count, self.D), dtype=float)
            if auditory_matrix.ndim == 2:
                rows = min(neuron_count, auditory_matrix.shape[0])
                cols = min(self.D, auditory_matrix.shape[1])
                repaired[:rows, :cols] = auditory_matrix[:rows, :cols]
            auditory_matrix = repaired
        else:
            auditory_matrix = auditory_matrix[:neuron_count]

        visual_matrix = np.asarray(visual_neural_matrix, dtype=float)
        if visual_matrix.ndim != 2 or len(visual_matrix) < neuron_count or visual_matrix.shape[1] != self.D:
            repaired = np.zeros((neuron_count, self.D), dtype=float)
            if visual_matrix.ndim == 2:
                rows = min(neuron_count, visual_matrix.shape[0])
                cols = min(self.D, visual_matrix.shape[1])
                repaired[:rows, :cols] = visual_matrix[:rows, :cols]
            visual_matrix = repaired
        else:
            visual_matrix = visual_matrix[:neuron_count]

        decay = float(getattr(Config, "MCM_MARKET_AUDIO_AFTERTONE_DECAY", 0.88) or 0.88)
        decay = float(max(0.0, min(0.995, decay)))
        auditory_aftertones = np.asarray([np.asarray(getattr(neuron, "auditory_aftertone", np.zeros(self.D, dtype=float)), dtype=float) for neuron in neurons], dtype=float)
        auditory_aftertones = (auditory_aftertones * decay) + (auditory_matrix * (1.0 - decay))
        auditory_resonances = self._norm01_rows(auditory_matrix, scale=0.12)
        visual_decay = float(getattr(Config, "MCM_MARKET_VISUAL_AFTERIMAGE_DECAY", 0.90) or 0.90)
        visual_decay = float(max(0.0, min(0.995, visual_decay)))
        visual_afterimages = np.asarray([np.asarray(getattr(neuron, "visual_afterimage", np.zeros(self.D, dtype=float)), dtype=float) for neuron in neurons], dtype=float)
        visual_afterimages = (visual_afterimages * visual_decay) + (visual_matrix * (1.0 - visual_decay))
        visual_resonances = self._norm01_rows(visual_matrix, scale=0.10)

        external_matrix = np.repeat(external_base, neuron_count, axis=0)
        replay_matrix = np.repeat(replay_base, neuron_count, axis=0)

        state_activity = self._norm01_rows(states)
        memory_activity = self._norm01_rows(memories)
        regulation_pressure_scaled = np.clip(previous_regulation_pressures / 0.38, 0.0, 1.0)
        external_alignment = self._alignment_rows(states, external_matrix)
        memory_alignment = self._alignment_rows(memories, external_matrix + context_matrix)

        positions = np.asarray(getattr(self, "topology_positions", []), dtype=float)
        topology_bias = np.zeros((neuron_count,), dtype=float)
        if positions.ndim == 2 and len(positions) >= neuron_count and positions.shape[1] >= 2:
            topology_bias = (positions[:neuron_count, 0] * 0.025) + (positions[:neuron_count, 1] * 0.015)

        receptivities = (
            0.78
            + (np.maximum(0.0, external_alignment) * 0.22)
            + (np.maximum(0.0, memory_alignment) * 0.18)
            + (memory_activity * 0.12)
            + topology_bias
            - (state_activity * 0.10)
            - (regulation_pressure_scaled * 0.18)
        )
        receptivities = np.clip(receptivities, 0.35, 1.35)
        external_matrix = external_matrix * receptivities[:, None]

        neighbor_arrays = list(getattr(self, "topology_neighbor_array", []) or [])
        if len(neighbor_arrays) < neuron_count:
            self.topology_neighbor_array = self._build_fixed_topology_neighbor_array()
            neighbor_arrays = list(getattr(self, "topology_neighbor_array", []) or [])

        sigma = max(float(self.coupling_sigma or 0.5), 1e-9)
        coupling_forces = np.zeros((neuron_count, self.D), dtype=float)
        for index in range(neuron_count):
            neighbor_indices = np.asarray(neighbor_arrays[int(index)] if int(index) < len(neighbor_arrays) else [], dtype=int)
            if neighbor_indices.size <= 0:
                continue
            neighbor_indices = neighbor_indices[(neighbor_indices >= 0) & (neighbor_indices < neuron_count) & (neighbor_indices != int(index))]
            if neighbor_indices.size <= 0:
                continue
            local_limit = max(1, int(self.local_neighbor_count or 1))
            neighbor_indices = neighbor_indices[:local_limit]
            diffs = states[neighbor_indices] - states[int(index)]
            distance_sq = np.einsum("ij,ij->i", diffs, diffs)
            weights = np.exp(-(distance_sq / sigma))
            coupling_forces[int(index)] = np.sum(diffs * weights[:, None], axis=0) * float(self.coupling)

        center_force = -float(self.k_center) * states
        overload_axis = np.maximum(np.abs(states[:, 0]), np.abs(states[:, 2] if self.D > 2 else 0.0))
        regulation_scale = np.minimum(1.0, overload_axis / 2.2)
        regulation_forces = center_force + (-velocities * (0.24 * regulation_scale[:, None]))
        regulation_pressures = np.mean(np.abs(regulation_forces), axis=1)

        sensory_matrix = (auditory_matrix * 0.18) + (visual_matrix * 0.12)
        total_impulses = external_matrix + replay_matrix
        memories = (memories * 0.86) + ((total_impulses + context_matrix) * 0.18)
        memory_feedback = memories * 0.35
        noise = np.random.randn(neuron_count, self.D) * float(self.noise)
        velocities = (velocities * 0.92) + coupling_forces + regulation_forces + total_impulses + memory_feedback + noise
        velocities = velocities + sensory_matrix
        states = np.clip(states + velocities, -float(self.max_abs_state), float(self.max_abs_state))

        external_intensity = self._norm01_rows(external_matrix, scale=1.0)
        replay_intensity = self._norm01_rows(replay_matrix, scale=1.0)
        context_intensity = self._norm01_rows(context_matrix, scale=0.18)
        coupling_intensity = self._norm01_rows(coupling_forces, scale=0.45)
        regulation_intensity = self._norm01_rows(regulation_forces, scale=0.45)
        memory_feedback_intensity = self._norm01_rows(memory_feedback, scale=0.45)
        velocity_intensity = self._norm01_rows(velocities, scale=float(self.max_abs_state or 3.0))
        state_intensity = self._norm01_rows(states, scale=float(self.max_abs_state or 3.0))
        noise_intensity = self._norm01_rows(noise, scale=0.45)
        auditory_intensity = self._norm01_rows(auditory_matrix, scale=0.12)
        visual_intensity = self._norm01_rows(visual_matrix, scale=0.10)
        sensory_intensity = self._norm01_rows(sensory_matrix, scale=0.12)
        memory_resonance = self._norm01_rows(memories, scale=float(self.max_abs_state or 3.0))
        overloads = np.clip((state_intensity * 0.36) + (velocity_intensity * 0.24) + (regulation_intensity * 0.22) + (context_intensity * 0.12) + (sensory_intensity * 0.06), 0.0, 1.0)
        recoveries = np.clip((regulation_intensity * 0.36) + ((1.0 - overloads) * 0.26) + (np.maximum(0.0, 1.0 - velocity_intensity) * 0.18) + (memory_resonance * 0.10), 0.0, 1.0)
        activations = np.clip(
            (
                external_intensity * 0.26
                + replay_intensity * 0.10
                + context_intensity * 0.16
                + coupling_intensity * 0.18
                + regulation_intensity * 0.10
                + memory_feedback_intensity * 0.10
                + velocity_intensity * 0.12
                + auditory_intensity * 0.04
                + visual_intensity * 0.04
                + memory_resonance * 0.06
                + noise_intensity * 0.02
            )
            * 2.15,
            0.0,
            1.0,
        )
        stabilities = np.clip(
            1.0
            - (overloads * 0.46)
            - (velocity_intensity * 0.24)
            - (coupling_intensity * 0.10)
            + (recoveries * 0.18)
            + (memory_resonance * 0.06),
            0.0,
            1.0,
        )

        keep_components = bool(getattr(Config, "MCM_NEURON_ACTIVATION_COMPONENTS_ENABLED", True))
        for index, neuron in enumerate(neurons):
            neuron.state = np.asarray(states[int(index)], dtype=float)
            neuron.velocity = np.asarray(velocities[int(index)], dtype=float)
            neuron.memory_trace = np.asarray(memories[int(index)], dtype=float)
            neuron.last_external_impulse = np.asarray(external_matrix[int(index)], dtype=float)
            neuron.last_memory_impulse = np.asarray(replay_matrix[int(index)], dtype=float)
            neuron.last_context_memory_impulse = np.asarray(context_matrix[int(index)], dtype=float)
            neuron.last_coupling_force = np.asarray(coupling_forces[int(index)], dtype=float)
            neuron.last_regulation_force = np.asarray(regulation_forces[int(index)], dtype=float)
            neuron.last_total_impulse = np.asarray(total_impulses[int(index)], dtype=float)
            neuron.last_memory_feedback = np.asarray(memory_feedback[int(index)], dtype=float)
            neuron.last_noise = np.asarray(noise[int(index)], dtype=float)
            neuron.last_auditory_impulse = np.asarray(auditory_matrix[int(index)], dtype=float)
            neuron.auditory_aftertone = np.asarray(auditory_aftertones[int(index)], dtype=float)
            neuron.auditory_resonance = float(auditory_resonances[int(index)])
            neuron.auditory_frequency_norm = float(max(0.0, min(1.0, float(auditory_frequency_norm or 0.0))))
            neuron.last_visual_impulse = np.asarray(visual_matrix[int(index)], dtype=float)
            neuron.visual_afterimage = np.asarray(visual_afterimages[int(index)], dtype=float)
            neuron.visual_resonance = float(visual_resonances[int(index)])
            neuron.receptivity = float(receptivities[int(index)])
            neuron.regulation_pressure = float(regulation_pressures[int(index)])
            neuron.memory_resonance = float(memory_resonance[int(index)])
            neuron.context_reactivation = float(context_intensity[int(index)])
            neuron.coupling_resonance = float(coupling_intensity[int(index)])
            neuron.overload = float(overloads[int(index)])
            neuron.recovery_tendency = float(recoveries[int(index)])
            neuron.activation = float(activations[int(index)])
            neuron.stability = float(stabilities[int(index)])

            activity_label_pressures = {
                "overloaded": float((neuron.overload * 0.48) + (neuron.activation * 0.20) + ((1.0 - neuron.stability) * 0.12)),
                "memory_reactivated": float((neuron.context_reactivation * 0.44) + (neuron.memory_resonance * 0.32) + (neuron.activation * 0.10)),
                "locally_coupled": float((neuron.coupling_resonance * 0.44) + (neuron.activation * 0.24) + (neuron.stability * 0.08)),
                "recovering": float((neuron.recovery_tendency * 0.44) + ((1.0 - neuron.activation) * 0.24) + (neuron.stability * 0.10)),
                "active": float((neuron.activation * 0.48) + (neuron.receptivity * 0.12) + ((1.0 - neuron.overload) * 0.08)),
                "settled": float((neuron.stability * 0.46) + ((1.0 - neuron.activation) * 0.24) + ((1.0 - neuron.overload) * 0.10)),
                "quiet": float(((1.0 - neuron.activation) * 0.34) + ((1.0 - neuron.overload) * 0.20) + ((1.0 - neuron.context_reactivation) * 0.08)),
            }
            neuron.activity_label = max(activity_label_pressures, key=activity_label_pressures.get)

            if keep_components:
                neuron.activation_components = {
                    "external_intensity": float(round(float(external_intensity[int(index)]), 4)),
                    "replay_intensity": float(round(float(replay_intensity[int(index)]), 4)),
                    "context_intensity": float(round(float(context_intensity[int(index)]), 4)),
                    "coupling_intensity": float(round(float(coupling_intensity[int(index)]), 4)),
                    "regulation_intensity": float(round(float(regulation_intensity[int(index)]), 4)),
                    "memory_feedback_intensity": float(round(float(memory_feedback_intensity[int(index)]), 4)),
                    "velocity_intensity": float(round(float(velocity_intensity[int(index)]), 4)),
                    "state_intensity": float(round(float(state_intensity[int(index)]), 4)),
                    "noise_intensity": float(round(float(noise_intensity[int(index)]), 4)),
                    "auditory_intensity": float(round(float(auditory_intensity[int(index)]), 4)),
                    "visual_intensity": float(round(float(visual_intensity[int(index)]), 4)),
                    "sensory_intensity": float(round(float(sensory_intensity[int(index)]), 4)),
                    "auditory_action_permission": 0.0,
                    "visual_action_permission": 0.0,
                    "activity_label_pressures": dict(activity_label_pressures),
                }
            elif neuron.activation_components:
                neuron.activation_components = {}

    # --------------------------------------------------
    def _build_areal_components(self, energy):

        energy = np.asarray(energy, dtype=float)

        if energy.ndim != 2 or len(energy) <= 1:
            return []

        agent_count = min(int(self.N), int(len(energy)))
        radius = max(float(self.areal_radius or 0.78), 1e-9)
        expanded_radius = radius * 1.35
        neighbor_index_map = dict(getattr(self, "topology_neighbor_indices", {}) or {})
        adjacency = {index: set() for index in range(agent_count)}

        for index in range(agent_count):
            selected_neighbors = []

            for neighbor_index in list(neighbor_index_map.get(int(index), []) or []):
                try:
                    resolved_neighbor = int(neighbor_index)
                except Exception:
                    continue

                if resolved_neighbor == int(index):
                    continue

                if resolved_neighbor < 0 or resolved_neighbor >= agent_count:
                    continue

                distance = float(np.linalg.norm(energy[int(resolved_neighbor)] - energy[int(index)]))
                if not np.isfinite(distance):
                    continue

                if distance <= radius or distance <= expanded_radius:
                    selected_neighbors.append(int(resolved_neighbor))

            for neighbor_index in list(selected_neighbors or []):
                adjacency[int(index)].add(int(neighbor_index))
                adjacency[int(neighbor_index)].add(int(index))

        components = []
        visited = set()

        for start_index in range(agent_count):
            if start_index in visited:
                continue

            stack = [int(start_index)]
            component = []
            visited.add(int(start_index))

            while stack:
                current_index = int(stack.pop())
                component.append(int(current_index))

                for neighbor_index in list(adjacency.get(current_index, set()) or set()):
                    if int(neighbor_index) in visited:
                        continue

                    visited.add(int(neighbor_index))
                    stack.append(int(neighbor_index))

            if len(component) >= int(self.areal_min_size):
                components.append(sorted(int(item) for item in list(component or [])))

        return list(components or [])

    # --------------------------------------------------
    def _build_areal_state(self):

        energy = np.asarray(getattr(self, "energy", []), dtype=float)
        velocity = np.asarray(getattr(self, "velocity", []), dtype=float)

        if energy.ndim != 2 or len(energy) == 0:
            self.areal_state = {
                "areal_count": 0,
                "areal_activation_mean": 0.0,
                "areal_stability_mean": 0.0,
                "areal_pressure_mean": 0.0,
                "areal_drift": 0.0,
                "areal_dominance": 0.0,
                "areal_fragmentation": 0.0,
                "areal_coherence_mean": 0.0,
                "areal_conflict_mean": 0.0,
                "areal_states": [],
                "areal_links": [],
            }
            self._last_areal_centers = []
            return dict(self.areal_state or {})

        agent_count = int(len(energy))

        if velocity.ndim != 2 or len(velocity) < agent_count:
            repaired_velocity = np.zeros((agent_count, energy.shape[1]), dtype=float)
            if velocity.size > 0 and velocity.ndim == 2:
                rows = min(int(len(velocity)), agent_count)
                cols = min(int(velocity.shape[1]), int(energy.shape[1]))
                if rows > 0 and cols > 0:
                    repaired_velocity[:rows, :cols] = velocity[:rows, :cols]
            velocity = repaired_velocity

        components = self._build_areal_components(energy)
        areal_states = []
        current_centers = []

        for areal_index, component in enumerate(list(components or [])):
            component_indices = [int(item) for item in list(component or []) if 0 <= int(item) < agent_count]
            if len(component_indices) <= 0:
                continue

            component_energy = np.asarray(energy[component_indices], dtype=float)
            component_velocity = np.asarray(velocity[component_indices], dtype=float)
            topology_positions = np.asarray(getattr(self, "topology_positions", []), dtype=float)
            component_topology_positions = np.zeros((0, 2), dtype=float)

            if topology_positions.ndim == 2 and max(component_indices) < len(topology_positions):
                component_topology_positions = np.asarray(topology_positions[component_indices], dtype=float)

            activation_values = []
            stability_values = []
            pressure_values = []
            memory_norm_values = []
            coupling_norm_values = []
            regulation_norm_values = []
            external_norm_values = []
            overload_values = []
            recovery_tendency_values = []
            memory_resonance_values = []
            context_reactivation_values = []
            coupling_resonance_values = []
            receptivity_values = []

            for neuron_index in list(component_indices or []):
                neuron = self.neurons[int(neuron_index)]
                activation_values.append(float(getattr(neuron, "activation", 0.0) or 0.0))
                stability_values.append(float(getattr(neuron, "stability", 0.0) or 0.0))
                pressure_values.append(float(getattr(neuron, "regulation_pressure", 0.0) or 0.0))
                memory_norm_values.append(float(np.linalg.norm(np.asarray(getattr(neuron, "memory_trace", []), dtype=float))))
                coupling_norm_values.append(float(np.linalg.norm(np.asarray(getattr(neuron, "last_coupling_force", []), dtype=float))))
                regulation_norm_values.append(float(np.linalg.norm(np.asarray(getattr(neuron, "last_regulation_force", []), dtype=float))))
                external_norm_values.append(float(np.linalg.norm(np.asarray(getattr(neuron, "last_external_impulse", []), dtype=float))))
                overload_values.append(float(getattr(neuron, "overload", 0.0) or 0.0))
                recovery_tendency_values.append(float(getattr(neuron, "recovery_tendency", 0.0) or 0.0))
                memory_resonance_values.append(float(getattr(neuron, "memory_resonance", 0.0) or 0.0))
                context_reactivation_values.append(float(getattr(neuron, "context_reactivation", 0.0) or 0.0))
                coupling_resonance_values.append(float(getattr(neuron, "coupling_resonance", 0.0) or 0.0))
                receptivity_values.append(float(getattr(neuron, "receptivity", 1.0) or 1.0))

            center = np.mean(component_energy, axis=0)
            mean_velocity_vector = np.mean(component_velocity, axis=0)
            current_centers.append(np.asarray(center, dtype=float))

            mean_internal_distance = self._build_component_internal_distance_mean(component_energy)
            density = float(max(0.0, min(1.0, 1.0 - (mean_internal_distance / max(self.areal_radius * 1.35, 1e-9)))))
            activation_mean = float(np.mean(activation_values)) if activation_values else 0.0
            stability_mean = float(np.mean(stability_values)) if stability_values else 0.0
            pressure_mean = float(np.mean(pressure_values)) if pressure_values else 0.0
            velocity_mean = float(np.mean(np.linalg.norm(component_velocity, axis=1))) if len(component_velocity) > 0 else 0.0
            center_abs = np.abs(np.asarray(center, dtype=float))
            coherence = float(np.max(center_abs)) if center_abs.size > 0 else 0.0
            conflict = float(np.std(component_energy[:, 0])) if component_energy.shape[1] > 0 else 0.0

            topology_center = np.mean(component_topology_positions, axis=0) if len(component_topology_positions) > 0 else np.zeros(2, dtype=float)
            topology_bounds_min = np.min(component_topology_positions, axis=0) if len(component_topology_positions) > 0 else np.zeros(2, dtype=float)
            topology_bounds_max = np.max(component_topology_positions, axis=0) if len(component_topology_positions) > 0 else np.zeros(2, dtype=float)
            topology_span = float(np.linalg.norm(topology_bounds_max - topology_bounds_min)) if len(component_topology_positions) > 0 else 0.0
            component_set = set(int(item) for item in list(component_indices or []))
            internal_topology_link_count = 0
            boundary_topology_link_count = 0

            for member_index in list(component_indices or []):
                for neighbor_index in list((getattr(self, "topology_neighbor_indices", {}) or {}).get(int(member_index), []) or []):
                    if int(neighbor_index) in component_set:
                        if int(member_index) < int(neighbor_index):
                            internal_topology_link_count += 1
                    else:
                        boundary_topology_link_count += 1

            topology_density = float(
                max(
                    0.0,
                    min(
                        1.0,
                        internal_topology_link_count
                        / max(1.0, (len(component_indices) * max(1.0, float(self.local_neighbor_count or 1))) / 2.0),
                    ),
                )
            )

            areal_label_pressures = {
                "strain_areal": float((pressure_mean * 0.42) + ((1.0 - stability_mean) * 0.24) + (conflict * 0.10)),
                "active_areal": float((activation_mean * 0.42) + (velocity_mean * 0.24) + (density * 0.08)),
                "settled_areal": float((stability_mean * 0.42) + (density * 0.24) + ((1.0 - pressure_mean) * 0.10)),
                "conflict_areal": float((conflict * 0.48) + (pressure_mean * 0.12) + ((1.0 - density) * 0.08)),
                "adaptive_areal": float((density * 0.20) + (stability_mean * 0.16) + (activation_mean * 0.12) + ((1.0 - conflict) * 0.12)),
            }
            areal_label = max(areal_label_pressures, key=areal_label_pressures.get)

            bounds_min = np.min(component_energy, axis=0)
            bounds_max = np.max(component_energy, axis=0)

            areal_states.append({
                "areal_id": f"areal_{int(areal_index)}",
                "member_indices": [int(item) for item in list(component_indices or [])],
                "center": [float(round(value, 4)) for value in np.asarray(center, dtype=float).tolist()],
                "mean_velocity_vector": [float(round(value, 4)) for value in np.asarray(mean_velocity_vector, dtype=float).tolist()],
                "bounds_min": [float(round(value, 4)) for value in np.asarray(bounds_min, dtype=float).tolist()],
                "bounds_max": [float(round(value, 4)) for value in np.asarray(bounds_max, dtype=float).tolist()],
                "topology_center": [float(round(value, 4)) for value in np.asarray(topology_center, dtype=float).tolist()],
                "topology_bounds_min": [float(round(value, 4)) for value in np.asarray(topology_bounds_min, dtype=float).tolist()],
                "topology_bounds_max": [float(round(value, 4)) for value in np.asarray(topology_bounds_max, dtype=float).tolist()],
                "topology_span": float(round(topology_span, 4)),
                "topology_density": float(round(topology_density, 4)),
                "topology_internal_link_count": int(internal_topology_link_count),
                "topology_boundary_link_count": int(boundary_topology_link_count),
                "mass": int(len(component_indices)),
                "density": float(round(density, 4)),
                "activation_mean": float(round(activation_mean, 4)),
                "stability_mean": float(round(stability_mean, 4)),
                "pressure_mean": float(round(pressure_mean, 4)),
                "memory_norm_mean": float(round(float(np.mean(memory_norm_values)) if memory_norm_values else 0.0, 4)),
                "coupling_norm_mean": float(round(float(np.mean(coupling_norm_values)) if coupling_norm_values else 0.0, 4)),
                "regulation_force_norm_mean": float(round(float(np.mean(regulation_norm_values)) if regulation_norm_values else 0.0, 4)),
                "external_impulse_norm_mean": float(round(float(np.mean(external_norm_values)) if external_norm_values else 0.0, 4)),
                "overload_mean": float(round(float(np.mean(overload_values)) if overload_values else 0.0, 4)),
                "recovery_tendency_mean": float(round(float(np.mean(recovery_tendency_values)) if recovery_tendency_values else 0.0, 4)),
                "memory_resonance_mean": float(round(float(np.mean(memory_resonance_values)) if memory_resonance_values else 0.0, 4)),
                "context_reactivation_mean": float(round(float(np.mean(context_reactivation_values)) if context_reactivation_values else 0.0, 4)),
                "coupling_resonance_mean": float(round(float(np.mean(coupling_resonance_values)) if coupling_resonance_values else 0.0, 4)),
                "receptivity_mean": float(round(float(np.mean(receptivity_values)) if receptivity_values else 0.0, 4)),
                "velocity_mean": float(round(velocity_mean, 4)),
                "coherence": float(round(coherence, 4)),
                "conflict": float(round(conflict, 4)),
                "state_label": str(areal_label),
                "areal_label_pressures": dict(areal_label_pressures),
            })

        areal_links = []

        for left_index, left_state in enumerate(list(areal_states or [])):
            left_center = np.asarray(left_state.get("center", []), dtype=float)

            for right_index in range(left_index + 1, len(areal_states)):
                right_state = dict(areal_states[right_index] or {})
                right_center = np.asarray(right_state.get("center", []), dtype=float)
                if len(left_center) == 0 or len(right_center) == 0:
                    continue

                distance = float(np.linalg.norm(left_center - right_center))
                if distance > (self.areal_radius * 3.2):
                    continue

                relation_label = "bridged"
                if np.sign(left_center[0] if len(left_center) > 0 else 0.0) != np.sign(right_center[0] if len(right_center) > 0 else 0.0):
                    relation_label = "counter_tension"
                elif distance <= (self.areal_radius * 1.6):
                    relation_label = "coupled"

                areal_links.append({
                    "source_areal_id": str(left_state.get("areal_id", f"areal_{left_index}")),
                    "target_areal_id": str(right_state.get("areal_id", f"areal_{right_index}")),
                    "distance": float(round(distance, 4)),
                    "relation_label": str(relation_label),
                })

        areal_drift = 0.0
        previous_centers = [np.asarray(item, dtype=float) for item in list(self._last_areal_centers or [])]
        if current_centers and previous_centers:
            drift_values = []
            for center in list(current_centers or []):
                distances_to_previous = [
                    float(np.linalg.norm(np.asarray(center, dtype=float) - np.asarray(previous_center, dtype=float)))
                    for previous_center in list(previous_centers or [])
                ]
                if distances_to_previous:
                    drift_values.append(float(min(distances_to_previous)))
            if drift_values:
                areal_drift = float(np.mean(drift_values))

        areal_count = int(len(areal_states))
        dominance = float(max((float(item.get("mass", 0) or 0) / max(1, self.N)) for item in list(areal_states or []))) if areal_states else 0.0
        fragmentation = float(min(1.0, areal_count / max(1.0, float(self.N) / max(1.0, float(self.areal_min_size)))))
        areal_activation_mean = float(np.mean([float(item.get("activation_mean", 0.0) or 0.0) for item in list(areal_states or [])])) if areal_states else 0.0
        areal_stability_mean = float(np.mean([float(item.get("stability_mean", 0.0) or 0.0) for item in list(areal_states or [])])) if areal_states else 0.0
        areal_pressure_mean = float(np.mean([float(item.get("pressure_mean", 0.0) or 0.0) for item in list(areal_states or [])])) if areal_states else 0.0
        areal_coherence_mean = float(np.mean([float(item.get("coherence", 0.0) or 0.0) for item in list(areal_states or [])])) if areal_states else 0.0
        areal_conflict_mean = float(np.mean([float(item.get("conflict", 0.0) or 0.0) for item in list(areal_states or [])])) if areal_states else 0.0

        self.areal_state = {
            "areal_count": int(areal_count),
            "areal_activation_mean": float(round(areal_activation_mean, 4)),
            "areal_stability_mean": float(round(areal_stability_mean, 4)),
            "areal_pressure_mean": float(round(areal_pressure_mean, 4)),
            "areal_drift": float(round(areal_drift, 4)),
            "areal_dominance": float(round(dominance, 4)),
            "areal_fragmentation": float(round(fragmentation, 4)),
            "areal_coherence_mean": float(round(areal_coherence_mean, 4)),
            "areal_conflict_mean": float(round(areal_conflict_mean, 4)),
            "areal_states": list(areal_states or []),
            "areal_links": list(areal_links or []),
        }
        self._last_areal_centers = [np.asarray(item, dtype=float) for item in list(current_centers or [])]
        return dict(self.areal_state or {})

    # --------------------------------------------------
    def _refresh_areal_state(self, force=False):
        every_n = max(1, int(getattr(Config, "MCM_FIELD_AREAL_REFRESH_EVERY_N", 1) or 1))
        current_seq = int(getattr(self, "field_step_seq", 0) or 0)

        last_refresh_seq = getattr(self, "_last_areal_refresh_seq", -1)
        try:
            last_refresh_seq = int(last_refresh_seq)
        except Exception:
            last_refresh_seq = -1

        if (
            not bool(force)
            and every_n > 1
            and isinstance(getattr(self, "areal_state", None), dict)
            and int(last_refresh_seq) >= 0
            and (current_seq % every_n) != 0
        ):
            carried = dict(self.areal_state or {})
            carried["areal_refresh_skipped"] = True
            carried["areal_stale_ticks"] = max(0, current_seq - int(last_refresh_seq))
            self.areal_state = dict(carried or {})
            return dict(self.areal_state or {})

        result = self._build_areal_state()
        self._last_areal_refresh_seq = int(current_seq)
        if isinstance(self.areal_state, dict):
            self.areal_state["areal_refresh_skipped"] = False
            self.areal_state["areal_stale_ticks"] = 0
        return dict(result or {})

    # --------------------------------------------------
    def _clip01(self, value):
        try:
            value = float(value)
        except Exception:
            value = 0.0

        if value < 0.0:
            return 0.0
        if value > 1.0:
            return 1.0
        return float(value)

    # --------------------------------------------------
    def _apply_activity_diffusion(self):

        if not self.neurons:
            return

        neurons = list(self.neurons or [])
        neuron_count = int(len(neurons))
        if neuron_count <= 0:
            return

        states = np.asarray([
            np.asarray(getattr(neuron, "state", np.zeros(self.D, dtype=float)), dtype=float)
            for neuron in neurons
        ], dtype=float)
        activations = np.clip(
            np.asarray([float(getattr(neuron, "activation", 0.0) or 0.0) for neuron in neurons], dtype=float),
            0.0,
            1.0,
        )
        couplings = np.clip(
            np.asarray([float(getattr(neuron, "coupling_resonance", 0.0) or 0.0) for neuron in neurons], dtype=float),
            0.0,
            1.0,
        )
        contexts = np.clip(
            np.asarray([float(getattr(neuron, "context_reactivation", 0.0) or 0.0) for neuron in neurons], dtype=float),
            0.0,
            1.0,
        )
        overloads = np.clip(
            np.asarray([float(getattr(neuron, "overload", 0.0) or 0.0) for neuron in neurons], dtype=float),
            0.0,
            1.0,
        )
        recoveries = np.clip(
            np.asarray([float(getattr(neuron, "recovery_tendency", 0.0) or 0.0) for neuron in neurons], dtype=float),
            0.0,
            1.0,
        )
        receptivities = np.clip(
            np.asarray([float(getattr(neuron, "receptivity", 1.0) or 1.0) for neuron in neurons], dtype=float),
            0.35,
            1.35,
        )

        neighbor_arrays = list(getattr(self, "topology_neighbor_array", []) or [])
        if len(neighbor_arrays) < neuron_count:
            self.topology_neighbor_array = self._build_fixed_topology_neighbor_array()
            neighbor_arrays = list(getattr(self, "topology_neighbor_array", []) or [])

        if not neighbor_arrays:
            neighbor_index_map = dict(getattr(self, "topology_neighbor_indices", {}) or {})
            neighbor_arrays = [
                np.asarray(neighbor_index_map.get(int(index), []) or [], dtype=int)
                for index in range(neuron_count)
            ]

        scale = max(0.0, min(0.12, float(getattr(Config, "MCM_FIELD_ACTIVITY_DIFFUSION_SCALE", 0.055) or 0.055)))
        deltas = np.zeros((neuron_count, self.D), dtype=float)

        for index in range(neuron_count):
            neighbor_indices = np.asarray(
                neighbor_arrays[int(index)] if int(index) < len(neighbor_arrays) else [],
                dtype=int,
            )
            if neighbor_indices.size > 0:
                neighbor_indices = neighbor_indices[
                    (neighbor_indices >= 0)
                    & (neighbor_indices < neuron_count)
                    & (neighbor_indices != int(index))
                ]

            if neighbor_indices.size <= 0:
                continue

            neighbor_weights = (
                (activations[neighbor_indices] * 0.58)
                + (couplings[neighbor_indices] * 0.24)
                + (contexts[neighbor_indices] * 0.18)
            )
            active_mask = neighbor_weights > 0.001
            if not bool(np.any(active_mask)):
                continue

            active_indices = neighbor_indices[active_mask]
            active_weights = np.asarray(neighbor_weights[active_mask], dtype=float)
            local_state = np.asarray(states[int(index)], dtype=float)
            weighted_delta = np.sum(
                (states[active_indices] - local_state) * active_weights[:, None],
                axis=0,
            )
            total_weight = float(np.sum(active_weights))
            strongest_neighbor_activation = float(np.max(activations[active_indices])) if active_indices.size > 0 else 0.0

            if total_weight <= 1e-9:
                continue

            local_overload = float(overloads[int(index)])
            local_recovery = float(recoveries[int(index)])
            local_receptivity = float(receptivities[int(index)])
            pressure_gate = max(0.25, min(1.05, 1.0 - (local_overload * 0.34) + (local_recovery * 0.12)))
            local_gate = max(0.20, min(1.20, (local_receptivity * 0.72) + (strongest_neighbor_activation * 0.28)))

            delta = (weighted_delta / total_weight) * float(scale) * float(pressure_gate) * float(local_gate)
            deltas[int(index)] = np.asarray(delta, dtype=float)

        for index, neuron in enumerate(neurons):
            delta = np.asarray(deltas[int(index)], dtype=float)
            neuron.last_field_diffusion = np.asarray(delta, dtype=float)
            neuron.state = np.clip(
                np.asarray(getattr(neuron, "state", np.zeros(self.D, dtype=float)), dtype=float) + delta,
                -float(self.max_abs_state),
                float(self.max_abs_state),
            )
            neuron.velocity = np.asarray(getattr(neuron, "velocity", np.zeros(self.D, dtype=float)), dtype=float) + (delta * 0.35)

            neighbor_weight = self._clip01(float(float(np.dot(delta, delta)) ** 0.5) / max(float(self.max_abs_state or 3.0), 1e-9))
            neuron.field_perception_weight = self._clip01(
                (float(getattr(neuron, "activation", 0.0) or 0.0) * 0.38)
                + (float(getattr(neuron, "context_reactivation", 0.0) or 0.0) * 0.22)
                + (float(getattr(neuron, "coupling_resonance", 0.0) or 0.0) * 0.22)
                + (neighbor_weight * 0.18)
            )

    # --------------------------------------------------
    def _build_activity_island_components(self):

        if not self.neurons:
            self._last_activity_island_threshold_state = {
                "activity_island_threshold_mode": "adaptive_relative",
                "activity_island_threshold": 0.0,
                "activity_score_mean": 0.0,
                "activity_score_max": 0.0,
                "activity_score_p90": 0.0,
            }
            return []

        threshold_ceiling = max(0.02, min(0.95, float(getattr(Config, "MCM_FIELD_ACTIVITY_ISLAND_THRESHOLD", 0.26) or 0.26)))
        neighbor_index_map = dict(getattr(self, "topology_neighbor_indices", {}) or {})
        active_indices = set()
        activity_scores = []

        for index, neuron in enumerate(list(self.neurons or [])):
            activation = self._clip01(float(getattr(neuron, "activation", 0.0) or 0.0))
            context = self._clip01(float(getattr(neuron, "context_reactivation", 0.0) or 0.0))
            coupling = self._clip01(float(getattr(neuron, "coupling_resonance", 0.0) or 0.0))
            perception_weight = self._clip01(float(getattr(neuron, "field_perception_weight", 0.0) or 0.0))
            activity_score = max(activation, (activation * 0.55) + (context * 0.20) + (coupling * 0.15) + (perception_weight * 0.10))
            activity_scores.append(float(activity_score))

        score_values = np.asarray(activity_scores, dtype=float)
        score_mean = float(np.mean(score_values)) if score_values.size else 0.0
        score_std = float(np.std(score_values)) if score_values.size else 0.0
        score_max = float(np.max(score_values)) if score_values.size else 0.0
        score_p90 = float(np.percentile(score_values, 90)) if score_values.size else 0.0
        threshold_candidate = max(
            float(score_mean + (score_std * 0.50)),
            float(score_p90 * 0.86),
            float(score_max * 0.72),
        )
        threshold = max(0.035, min(float(threshold_ceiling), float(threshold_candidate)))
        self._last_activity_island_threshold_state = {
            "activity_island_threshold_mode": "adaptive_relative",
            "activity_island_threshold": float(round(threshold, 4)),
            "activity_score_mean": float(round(score_mean, 4)),
            "activity_score_max": float(round(score_max, 4)),
            "activity_score_p90": float(round(score_p90, 4)),
        }

        for index, activity_score in enumerate(list(activity_scores or [])):
            if activity_score >= threshold:
                active_indices.add(int(index))

        components = []
        visited = set()

        for start_index in sorted(active_indices):
            if int(start_index) in visited:
                continue

            stack = [int(start_index)]
            component = []
            visited.add(int(start_index))

            while stack:
                current = int(stack.pop())
                component.append(int(current))

                for neighbor_index in list(neighbor_index_map.get(int(current), []) or []):
                    neighbor_index = int(neighbor_index)
                    if neighbor_index not in active_indices or neighbor_index in visited:
                        continue

                    visited.add(int(neighbor_index))
                    stack.append(int(neighbor_index))

            if component:
                components.append(sorted(int(item) for item in list(component or [])))

        return list(components or [])

    # --------------------------------------------------
    def _build_field_perception_state(self):

        components = self._build_activity_island_components()
        threshold_state = dict(getattr(self, "_last_activity_island_threshold_state", {}) or {})
        positions = np.asarray(getattr(self, "topology_positions", []), dtype=float)
        islands = []

        for island_index, component in enumerate(list(components or [])):
            component_indices = [int(item) for item in list(component or []) if 0 <= int(item) < len(self.neurons)]
            if not component_indices:
                continue

            component_neurons = [self.neurons[int(index)] for index in list(component_indices or [])]
            activation_values = [float(getattr(neuron, "activation", 0.0) or 0.0) for neuron in component_neurons]
            overload_values = [float(getattr(neuron, "overload", 0.0) or 0.0) for neuron in component_neurons]
            recovery_values = [float(getattr(neuron, "recovery_tendency", 0.0) or 0.0) for neuron in component_neurons]
            context_values = [float(getattr(neuron, "context_reactivation", 0.0) or 0.0) for neuron in component_neurons]
            coupling_values = [float(getattr(neuron, "coupling_resonance", 0.0) or 0.0) for neuron in component_neurons]
            perception_values = [float(getattr(neuron, "field_perception_weight", 0.0) or 0.0) for neuron in component_neurons]
            stability_values = [float(getattr(neuron, "stability", 0.0) or 0.0) for neuron in component_neurons]

            island_positions = np.zeros((0, 2), dtype=float)
            if positions.ndim == 2 and len(positions) > 0 and max(component_indices) < len(positions):
                island_positions = np.asarray(positions[component_indices], dtype=float)

            center = np.mean(island_positions, axis=0) if len(island_positions) > 0 else np.zeros(2, dtype=float)
            span = 0.0
            if len(island_positions) > 1:
                bounds_min = np.min(island_positions, axis=0)
                bounds_max = np.max(island_positions, axis=0)
                span = float(np.linalg.norm(bounds_max - bounds_min))

            activation_mean = float(np.mean(activation_values)) if activation_values else 0.0
            pressure_mean = float(np.mean(overload_values)) if overload_values else 0.0
            recovery_mean = float(np.mean(recovery_values)) if recovery_values else 0.0
            context_mean = float(np.mean(context_values)) if context_values else 0.0
            coupling_mean = float(np.mean(coupling_values)) if coupling_values else 0.0
            perception_mean = float(np.mean(perception_values)) if perception_values else 0.0
            stability_mean = float(np.mean(stability_values)) if stability_values else 0.0
            coherence = self._clip01((stability_mean * 0.34) + (coupling_mean * 0.26) + (perception_mean * 0.22) + ((1.0 - pressure_mean) * 0.18))

            island_label_pressures = {
                "strained_island": float((pressure_mean * 0.46) + ((1.0 - coherence) * 0.24) + (activation_mean * 0.08)),
                "memory_reactivated_island": float((context_mean * 0.48) + (coupling_mean * 0.12) + (perception_mean * 0.08)),
                "recovering_island": float((recovery_mean * 0.46) + ((1.0 - pressure_mean) * 0.18) + (stability_mean * 0.10)),
                "coherent_island": float((coherence * 0.44) + (activation_mean * 0.20) + (stability_mean * 0.10)),
                "active_island": float((activation_mean * 0.38) + (perception_mean * 0.18) + (coupling_mean * 0.12)),
            }
            label = max(island_label_pressures, key=island_label_pressures.get)

            islands.append({
                "island_id": f"activity_island_{int(island_index)}",
                "member_indices": [int(item) for item in list(component_indices or [])],
                "mass": int(len(component_indices)),
                "mass_ratio": float(round(float(len(component_indices)) / max(1.0, float(self.N)), 4)),
                "topology_center": [float(round(value, 4)) for value in np.asarray(center, dtype=float).tolist()],
                "topology_span": float(round(span, 4)),
                "activation_mean": float(round(activation_mean, 4)),
                "pressure_mean": float(round(pressure_mean, 4)),
                "recovery_tendency_mean": float(round(recovery_mean, 4)),
                "context_reactivation_mean": float(round(context_mean, 4)),
                "coupling_resonance_mean": float(round(coupling_mean, 4)),
                "perception_weight_mean": float(round(perception_mean, 4)),
                "coherence": float(round(coherence, 4)),
                "state_label": str(label),
                "island_label_pressures": dict(island_label_pressures),
            })

        island_count = int(len(islands))
        mass_values = [float(item.get("mass_ratio", 0.0) or 0.0) for item in list(islands or [])]
        activation_values = [float(item.get("activation_mean", 0.0) or 0.0) for item in list(islands or [])]
        pressure_values = [float(item.get("pressure_mean", 0.0) or 0.0) for item in list(islands or [])]
        coherence_values = [float(item.get("coherence", 0.0) or 0.0) for item in list(islands or [])]
        context_values = [float(item.get("context_reactivation_mean", 0.0) or 0.0) for item in list(islands or [])]
        spread_values = [float(item.get("topology_span", 0.0) or 0.0) for item in list(islands or [])]

        mass_mean = float(np.mean(mass_values)) if mass_values else 0.0
        mass_max = float(np.max(mass_values)) if mass_values else 0.0
        activation_mean = float(np.mean(activation_values)) if activation_values else 0.0
        pressure_mean = float(np.mean(pressure_values)) if pressure_values else 0.0
        coherence_mean = float(np.mean(coherence_values)) if coherence_values else 0.0
        context_mean = float(np.mean(context_values)) if context_values else 0.0
        spread_mean = float(np.mean(spread_values)) if spread_values else 0.0
        dominant_island = {}
        if islands:
            dominant_island = max(
                list(islands or []),
                key=lambda item: (
                    float((item or {}).get("mass_ratio", 0.0) or 0.0)
                    * max(0.0, float((item or {}).get("activation_mean", 0.0) or 0.0))
                    * max(0.0, float((item or {}).get("coherence", 0.0) or 0.0))
                ),
            )
        dominant_mass = float(dominant_island.get("mass_ratio", 0.0) or 0.0) if dominant_island else 0.0
        dominant_activation = float(dominant_island.get("activation_mean", 0.0) or 0.0) if dominant_island else 0.0
        dominant_coherence = float(dominant_island.get("coherence", 0.0) or 0.0) if dominant_island else 0.0
        dominant_pressure = float(dominant_island.get("pressure_mean", 0.0) or 0.0) if dominant_island else 0.0
        island_count_pressure = self._clip01(max(0.0, float(island_count - 1)) / 5.0)
        spread_pressure = self._clip01(spread_mean / max(float(np.sqrt(8.0)), 1e-9))
        dominance_balance = self._clip01(dominant_mass / max(mass_mean * max(1.0, float(island_count)), 1e-9)) if island_count > 0 and mass_mean > 0.0 else 0.0
        field_focus = self._clip01(
            (dominant_mass * 0.34)
            + (dominant_activation * 0.20)
            + (dominant_coherence * 0.24)
            + (dominance_balance * 0.12)
            - (island_count_pressure * 0.06)
            - (spread_pressure * 0.04)
        )
        field_fragmentation = self._clip01(
            (island_count_pressure * 0.34)
            + (spread_pressure * 0.20)
            + (max(0.0, 1.0 - mass_max) * field_activity_presence if (field_activity_presence := self._clip01(float(island_count) / 4.0)) else 0.0) * 0.18
            + (max(0.0, 1.0 - coherence_mean) * 0.16)
            + (pressure_mean * 0.12)
        )
        field_strain = self._clip01(
            (pressure_mean * 0.40)
            + (dominant_pressure * 0.18)
            + (field_fragmentation * 0.18)
            + (max(0.0, 1.0 - coherence_mean) * 0.14)
            + (spread_pressure * 0.10)
        )
        field_stability = self._clip01(
            (coherence_mean * 0.34)
            + (field_focus * 0.22)
            + (dominant_coherence * 0.18)
            + ((1.0 - field_strain) * 0.16)
            + ((1.0 - field_fragmentation) * 0.10)
        )
        field_clarity = self._clip01(
            (field_focus * 0.34)
            + (coherence_mean * 0.24)
            + (dominant_activation * 0.14)
            + ((1.0 - field_fragmentation) * 0.16)
            + ((1.0 - field_strain) * 0.12)
        )

        field_label_pressures = {
            "quiet_field": float(((1.0 - field_activity_presence) * 0.42) + ((1.0 - activation_mean) * 0.20) + ((1.0 - field_strain) * 0.10)),
            "strained_field": float((field_strain * 0.44) + ((1.0 - field_clarity) * 0.24) + (pressure_mean * 0.10)),
            "memory_reactivated_field": float((context_mean * 0.48) + (dominant_coherence * 0.10) + (activation_mean * 0.08)),
            "fragmented_perception_field": float((field_fragmentation * 0.48) + (spread_pressure * 0.16) + (island_count_pressure * 0.12)),
            "coherent_perception_field": float((field_stability * 0.34) + (field_clarity * 0.30) + (activation_mean * 0.12)),
            "active_perception_field": float((activation_mean * 0.42) + (field_focus * 0.16) + (field_clarity * 0.10)),
        }
        label = max(field_label_pressures, key=field_label_pressures.get)

        self.field_perception_state = {
            "activity_island_count": int(island_count),
            "activity_island_mass_mean": float(round(mass_mean, 4)),
            "activity_island_mass_max": float(round(mass_max, 4)),
            "activity_island_activation_mean": float(round(activation_mean, 4)),
            "activity_island_pressure_mean": float(round(pressure_mean, 4)),
            "activity_island_coherence_mean": float(round(coherence_mean, 4)),
            "activity_island_context_reactivation_mean": float(round(context_mean, 4)),
            "activity_island_spread": float(round(spread_mean, 4)),
            "field_perception_focus": float(round(field_focus, 4)),
            "field_perception_clarity": float(round(field_clarity, 4)),
            "field_perception_stability": float(round(field_stability, 4)),
            "field_perception_fragmentation": float(round(field_fragmentation, 4)),
            "field_perception_strain": float(round(field_strain, 4)),
            "dominant_activity_island_id": str(dominant_island.get("island_id", "-") or "-"),
            "field_perception_label": str(label),
            "field_perception_label_pressures": dict(field_label_pressures),
            "activity_island_threshold_mode": str(threshold_state.get("activity_island_threshold_mode", "adaptive_relative") or "adaptive_relative"),
            "activity_island_threshold": float(threshold_state.get("activity_island_threshold", 0.0) or 0.0),
            "activity_score_mean": float(threshold_state.get("activity_score_mean", 0.0) or 0.0),
            "activity_score_max": float(threshold_state.get("activity_score_max", 0.0) or 0.0),
            "activity_score_p90": float(threshold_state.get("activity_score_p90", 0.0) or 0.0),
            "activity_islands": list(islands or []),
        }
        return dict(self.field_perception_state or {})

    # --------------------------------------------------
    def _build_context_memory_vector(self, context_trace):

        item = dict(context_trace or {})

        try:
            activation = float(item.get("activation", 0.0) or 0.0)
        except Exception:
            activation = 0.0

        activation = max(0.0, min(1.0, activation))
        if activation <= 0.001:
            return np.zeros(self.D, dtype=float)

        support = max(0.0, min(1.0, float(item.get("support", 0.0) or 0.0)))
        conflict = max(0.0, min(1.0, float(item.get("conflict", 0.0) or 0.0)))
        fragility = max(0.0, min(1.0, float(item.get("fragility", 0.0) or 0.0)))
        bearing = max(0.0, min(1.0, float(item.get("bearing", 0.0) or 0.0)))
        action_support = max(0.0, min(1.0, float(item.get("action_support", 0.0) or 0.0)))
        observe_pressure = max(0.0, min(1.0, float(item.get("observe_pressure", 0.0) or 0.0)))
        replan_pressure = max(0.0, min(1.0, float(item.get("replan_pressure", 0.0) or 0.0)))
        reinforcement = max(0.0, min(1.0, float(item.get("reinforcement", 0.0) or 0.0)))
        attenuation = max(0.0, min(1.0, float(item.get("attenuation", 0.0) or 0.0)))

        scale = max(0.0, min(0.08, float(getattr(Config, "MCM_NEURON_CONTEXT_MEMORY_SCALE", 0.035) or 0.035)))
        vector = np.zeros(self.D, dtype=float)

        if self.D > 0:
            vector[0] = (support + bearing + reinforcement - conflict - fragility - attenuation) * activation * scale

        if self.D > 1:
            vector[1] = (action_support + bearing + reinforcement - observe_pressure - replan_pressure) * activation * scale

        if self.D > 2:
            vector[2] = (conflict + fragility + attenuation - support - bearing) * activation * scale

        return np.asarray(vector, dtype=float)

    # --------------------------------------------------
    def _resolve_step_impulse_vector(self, impulse=None, motivation_impulse=0.0, risk_impulse=0.0):

        vector = np.zeros(int(self.D), dtype=float)

        if isinstance(impulse, (list, tuple, np.ndarray)):
            values = np.asarray(impulse, dtype=float).flatten()
            limit = min(len(values), int(self.D))
            if limit > 0:
                vector[:limit] = values[:limit]
        else:
            vector[0] = float(impulse or 0.0)

        if int(self.D) > 1:
            vector[1] += float(motivation_impulse or 0.0)

        if int(self.D) > 2:
            vector[2] += float(risk_impulse or 0.0)

        return np.asarray(vector, dtype=float)

    # --------------------------------------------------
    def _build_local_context_memory_impulse(self, context_trace, neuron, base_vector=None):

        if base_vector is None:
            base_vector = self._build_context_memory_vector(context_trace)
        else:
            base_vector = np.asarray(base_vector, dtype=float)

        if base_vector.size <= 0 or not np.any(base_vector):
            return np.zeros(self.D, dtype=float)

        local_state = np.asarray(getattr(neuron, "state", np.zeros(self.D, dtype=float)), dtype=float)
        local_memory = np.asarray(getattr(neuron, "memory_trace", np.zeros(self.D, dtype=float)), dtype=float)

        local_activity = float(np.mean(np.abs(local_state))) if local_state.size > 0 else 0.0
        local_trace = float(np.linalg.norm(local_memory)) if local_memory.size > 0 else 0.0
        local_activation = float(getattr(neuron, "activation", 0.0) or 0.0)
        local_pressure = float(getattr(neuron, "regulation_pressure", 0.0) or 0.0)

        resonance = (local_activation * 0.32) + (local_pressure * 0.24) + (local_activity * 0.28) + (local_trace * 0.16)
        resonance = max(0.12, min(1.0, float(resonance)))

        return np.asarray(base_vector, dtype=float) * float(resonance)

    # --------------------------------------------------
    def _build_local_context_memory_matrix(self, context_trace, base_vector=None):

        if base_vector is None:
            base_vector = self._build_context_memory_vector(context_trace)
        else:
            base_vector = np.asarray(base_vector, dtype=float)

        if base_vector.size <= 0 or not np.any(base_vector):
            return np.zeros((int(self.N), int(self.D)), dtype=float)

        energy = np.asarray(getattr(self, "energy", []), dtype=float)
        if energy.shape != (int(self.N), int(self.D)):
            energy = np.asarray([
                np.asarray(getattr(neuron, "state", np.zeros(self.D, dtype=float)), dtype=float)
                for neuron in list(self.neurons or [])
            ], dtype=float)

        if energy.shape != (int(self.N), int(self.D)):
            repaired = np.zeros((int(self.N), int(self.D)), dtype=float)
            rows = min(int(len(energy)) if getattr(energy, "ndim", 0) >= 1 else 0, int(self.N))
            cols = min(int(energy.shape[1]) if getattr(energy, "ndim", 0) >= 2 else 0, int(self.D))
            if rows > 0 and cols > 0:
                repaired[:rows, :cols] = energy[:rows, :cols]
            energy = repaired

        memory = np.asarray([
            np.asarray(getattr(neuron, "memory_trace", np.zeros(self.D, dtype=float)), dtype=float)
            for neuron in list(self.neurons or [])
        ], dtype=float)
        if memory.shape != (int(self.N), int(self.D)):
            repaired_memory = np.zeros((int(self.N), int(self.D)), dtype=float)
            rows = min(int(len(memory)) if getattr(memory, "ndim", 0) >= 1 else 0, int(self.N))
            cols = min(int(memory.shape[1]) if getattr(memory, "ndim", 0) >= 2 else 0, int(self.D))
            if rows > 0 and cols > 0:
                repaired_memory[:rows, :cols] = memory[:rows, :cols]
            memory = repaired_memory

        activations = np.asarray([
            float(getattr(neuron, "activation", 0.0) or 0.0)
            for neuron in list(self.neurons or [])
        ], dtype=float)
        pressures = np.asarray([
            float(getattr(neuron, "regulation_pressure", 0.0) or 0.0)
            for neuron in list(self.neurons or [])
        ], dtype=float)

        if activations.shape[0] != int(self.N):
            activations = np.resize(activations, int(self.N)) if activations.size > 0 else np.zeros(int(self.N), dtype=float)
        if pressures.shape[0] != int(self.N):
            pressures = np.resize(pressures, int(self.N)) if pressures.size > 0 else np.zeros(int(self.N), dtype=float)

        local_activity = np.mean(np.abs(energy), axis=1) if energy.size > 0 else np.zeros(int(self.N), dtype=float)
        local_trace = np.linalg.norm(memory, axis=1) if memory.size > 0 else np.zeros(int(self.N), dtype=float)
        resonance = (
            (activations * 0.32)
            + (pressures * 0.24)
            + (local_activity * 0.28)
            + (local_trace * 0.16)
        )
        resonance = np.clip(resonance, 0.12, 1.0)
        return np.asarray(base_vector, dtype=float)[None, :] * resonance[:, None]

    # --------------------------------------------------
    def _empty_auditory_neural_state(self):
        return {
            "enabled": False,
            "sense": "hearing",
            "channel": "market_audio_to_neuron",
            "loudness": 0.0,
            "frequency_hz": 0.0,
            "frequency_norm": 0.0,
            "compression": 0.0,
            "overdrive": 0.0,
            "scale": 0.0,
            "resonance_mean": 0.0,
            "resonance_max": 0.0,
            "aftertone_mean": 0.0,
            "tone": "silent_tone",
            "action_permission": 0.0,
        }

    # --------------------------------------------------
    def _empty_visual_neural_state(self):
        return {
            "enabled": False,
            "sense": "seeing",
            "channel": "market_visual_to_neuron",
            "clarity": 0.0,
            "contact": 0.0,
            "coherence": 0.0,
            "pressure": 0.0,
            "scale": 0.0,
            "resonance_mean": 0.0,
            "resonance_max": 0.0,
            "afterimage_mean": 0.0,
            "form_family": "-",
            "sight_label": "blind_visual_trace",
            "action_permission": 0.0,
        }

    # --------------------------------------------------
    def _build_visual_neural_matrix(self, visual_market_state=None):
        if not bool(getattr(Config, "MCM_MARKET_VISUAL_NEURAL_STIMULATION_ENABLED", True)):
            self.visual_neural_state = self._empty_visual_neural_state()
            return np.zeros((int(self.N), int(self.D)), dtype=float)

        visual = dict(visual_market_state or {})
        sight = dict(visual.get("visual_sight_state", {}) or {})
        cortex = dict(visual.get("visual_cortex_state", {}) or {})
        if not visual and not sight and not cortex:
            self.visual_neural_state = self._empty_visual_neural_state()
            return np.zeros((int(self.N), int(self.D)), dtype=float)

        def _f(*sources, key, default=0.0):
            for source in sources:
                if not isinstance(source, dict) or key not in source:
                    continue
                try:
                    return float(source.get(key, default) or default)
                except Exception:
                    return float(default or 0.0)
            return float(default or 0.0)

        clarity = max(0.0, min(1.0, _f(sight, visual, key="clarity", default=_f(visual, key="visual_clarity"))))
        stability = max(0.0, min(1.0, _f(sight, visual, key="object_stability", default=_f(visual, key="visual_object_stability"))))
        coherence = max(-1.0, min(1.0, _f(sight, visual, key="coherence", default=_f(visual, key="visual_coherence"))))
        contact = max(0.0, min(1.0, _f(sight, visual, key="contact_candidate")))
        pressure = max(0.0, min(1.0, _f(sight, visual, key="form_pressure", default=_f(visual, key="visual_form_pressure"))))
        resonance = max(0.0, min(1.0, _f(sight, visual, key="form_resonance", default=_f(visual, key="visual_shape_resonance"))))
        fragility = max(0.0, min(1.0, _f(sight, visual, key="form_fragility", default=_f(visual, key="visual_shape_fragility"))))
        direction = max(-1.0, min(1.0, _f(sight, visual, key="direction_bias", default=_f(visual, key="directional_bias"))))
        range_position = max(-1.0, min(1.0, _f(sight, visual, key="range_position")))
        background = max(0.0, min(1.0, _f(sight, visual, key="background_load", default=_f(visual, key="visual_background_load"))))
        scale = max(0.0, min(0.12, float(getattr(Config, "MCM_MARKET_VISUAL_NEURAL_STIMULATION_SCALE", 0.06) or 0.06)))

        form_presence = max(clarity, contact, resonance, pressure * 0.72, stability * 0.56)
        if form_presence <= 0.0 or scale <= 0.0:
            self.visual_neural_state = self._empty_visual_neural_state()
            return np.zeros((int(self.N), int(self.D)), dtype=float)

        positions = np.asarray(getattr(self, "topology_positions", []), dtype=float)
        if positions.shape != (int(self.N), 2):
            positions = np.zeros((int(self.N), 2), dtype=float)

        x_axis = positions[:, 0] if positions.ndim == 2 and positions.shape[1] >= 1 else np.zeros(int(self.N), dtype=float)
        y_axis = positions[:, 1] if positions.ndim == 2 and positions.shape[1] >= 2 else np.zeros(int(self.N), dtype=float)
        width = max(0.16, 0.44 - (clarity * 0.16) + (background * 0.18))
        local_focus = np.exp(-(((x_axis - range_position) ** 2) / max(width, 1e-9)))
        vertical_shape = 0.65 + (np.cos((y_axis + direction) * 3.141592653589793) * 0.35)
        spatial_trace = np.clip(local_focus * vertical_shape, 0.0, 1.0)
        amplitude = float(form_presence * scale)

        matrix = np.zeros((int(self.N), int(self.D)), dtype=float)
        if int(self.D) > 0:
            matrix[:, 0] = ((coherence * 0.58) + (direction * 0.42)) * spatial_trace * amplitude
        if int(self.D) > 1:
            matrix[:, 1] = ((contact * 0.44) + (resonance * 0.34) + (stability * 0.22)) * (0.35 + spatial_trace * 0.65) * amplitude
        if int(self.D) > 2:
            matrix[:, 2] = ((pressure * 0.44) + (fragility * 0.30) + (background * 0.26)) * (0.40 + spatial_trace * 0.60) * amplitude

        resonance_norm = np.linalg.norm(matrix, axis=1) if matrix.size > 0 else np.zeros(int(self.N), dtype=float)
        self.visual_neural_state = {
            "enabled": True,
            "sense": "seeing",
            "channel": "market_visual_to_neuron",
            "clarity": float(clarity),
            "contact": float(contact),
            "coherence": float(coherence),
            "pressure": float(pressure),
            "scale": float(scale),
            "resonance_mean": float(np.mean(resonance_norm)) if resonance_norm.size > 0 else 0.0,
            "resonance_max": float(np.max(resonance_norm)) if resonance_norm.size > 0 else 0.0,
            "afterimage_mean": 0.0,
            "form_family": str(sight.get("form_family", visual.get("visual_form_family", "-")) or "-"),
            "sight_label": str(sight.get("sight_label", visual.get("visual_sight_label", "visual_trace")) or "visual_trace"),
            "action_permission": 0.0,
        }
        return matrix

    # --------------------------------------------------
    def _build_auditory_neural_matrix(self, market_hearing_state=None):
        if not bool(getattr(Config, "MCM_MARKET_AUDIO_NEURAL_STIMULATION_ENABLED", True)):
            self.auditory_neural_state = self._empty_auditory_neural_state()
            return np.zeros((int(self.N), int(self.D)), dtype=float)

        hearing = dict(market_hearing_state or {})
        if not hearing:
            self.auditory_neural_state = self._empty_auditory_neural_state()
            return np.zeros((int(self.N), int(self.D)), dtype=float)

        try:
            loudness = float(hearing.get("loudness", 0.0) or 0.0)
        except Exception:
            loudness = 0.0

        try:
            frequency_hz = float(hearing.get("frequency_hz", 0.0) or 0.0)
        except Exception:
            frequency_hz = 0.0

        try:
            compression = float(hearing.get("compression", 0.0) or 0.0)
        except Exception:
            compression = 0.0

        try:
            overdrive = float(hearing.get("overdrive", 0.0) or 0.0)
        except Exception:
            overdrive = 0.0

        loudness = float(max(0.0, min(2.5, loudness)))
        frequency_hz = float(max(0.0, frequency_hz))
        max_hz = max(float(getattr(Config, "MCM_MARKET_HEARING_MAX_HZ", 17000.0) or 17000.0), 1.0)
        frequency_norm = float(max(0.0, min(1.0, frequency_hz / max_hz)))
        scale = float(max(0.0, getattr(Config, "MCM_MARKET_AUDIO_NEURAL_STIMULATION_SCALE", 0.08) or 0.08))

        if loudness <= 0.0 or scale <= 0.0:
            self.auditory_neural_state = self._empty_auditory_neural_state()
            return np.zeros((int(self.N), int(self.D)), dtype=float)

        positions = np.asarray(getattr(self, "topology_positions", []), dtype=float)
        if positions.shape != (int(self.N), 2):
            positions = np.zeros((int(self.N), 2), dtype=float)

        phase_seed = (float(getattr(self, "field_step_seq", 0) or 0) * 0.037) + (frequency_norm * 6.283185307179586)
        x_axis = positions[:, 0] if positions.ndim == 2 and positions.shape[1] >= 1 else np.zeros(int(self.N), dtype=float)
        y_axis = positions[:, 1] if positions.ndim == 2 and positions.shape[1] >= 2 else np.zeros(int(self.N), dtype=float)
        phase = (x_axis * (1.0 + frequency_norm * 5.0)) + (y_axis * 0.75) + phase_seed
        resonance = np.sin(phase * 3.141592653589793)
        carrier = np.cos((phase + frequency_norm) * 3.141592653589793)
        amplitude = float(min(1.0, loudness / 2.5) * scale)

        matrix = np.zeros((int(self.N), int(self.D)), dtype=float)
        if int(self.D) > 0:
            matrix[:, 0] = resonance * amplitude
        if int(self.D) > 1:
            matrix[:, 1] = carrier * amplitude * 0.55
        if int(self.D) > 2:
            matrix[:, 2] = np.clip((float(compression) + float(overdrive)) * scale * 0.35, 0.0, scale * 0.35)

        resonance_norm = np.linalg.norm(matrix, axis=1) if matrix.size > 0 else np.zeros(int(self.N), dtype=float)
        self.auditory_neural_state = {
            "enabled": True,
            "sense": "hearing",
            "channel": "market_audio_to_neuron",
            "loudness": float(loudness),
            "frequency_hz": float(frequency_hz),
            "frequency_norm": float(frequency_norm),
            "compression": float(compression),
            "overdrive": float(overdrive),
            "scale": float(scale),
            "resonance_mean": float(np.mean(resonance_norm)) if resonance_norm.size > 0 else 0.0,
            "resonance_max": float(np.max(resonance_norm)) if resonance_norm.size > 0 else 0.0,
            "aftertone_mean": 0.0,
            "tone": str(hearing.get("tone", "silent_tone") or "silent_tone"),
            "action_permission": 0.0,
        }
        return matrix

    # --------------------------------------------------
    def read_snapshot(self):

        neuron_payload = []

        for index, neuron in enumerate(list(self.neurons or [])):
            neuron_snapshot = dict(neuron.read_snapshot() or {})
            neuron_snapshot["agent_index"] = int(index)
            neuron_payload.append(neuron_snapshot)

        return {
            "energy": np.asarray(self.energy, dtype=float).copy(),
            "velocity": np.asarray(self.velocity, dtype=float).copy(),
            "neurons": list(neuron_payload or []),
            "topology_rows": int(getattr(self, "topology_rows", 0) or 0),
            "topology_cols": int(getattr(self, "topology_cols", 0) or 0),
            "topology_positions": np.asarray(getattr(self, "topology_positions", []), dtype=float).copy(),
            "topology_neighbor_indices": dict(getattr(self, "topology_neighbor_indices", {}) or {}),
            "areal_state": dict(self.areal_state or {}),
            "areal_states": [dict(item or {}) for item in list((self.areal_state or {}).get("areal_states", []) or []) if isinstance(item, dict)],
            "areal_links": [dict(item or {}) for item in list((self.areal_state or {}).get("areal_links", []) or []) if isinstance(item, dict)],
            "field_perception_state": dict(self.field_perception_state or {}),
            "activity_islands": [dict(item or {}) for item in list((self.field_perception_state or {}).get("activity_islands", []) or []) if isinstance(item, dict)],
            "auditory_neural_state": dict(self.auditory_neural_state or {}),
            "visual_neural_state": dict(self.visual_neural_state or {}),
        }

    # --------------------------------------------------
    def step(
        self,
        impulse,
        motivation_impulse=0.0,
        risk_impulse=0.0,
        replay_impulse=None,
        context_trace=None,
        market_hearing_state=None,
        visual_market_state=None,
        return_snapshot=True,
    ):

        self.field_step_seq = int(getattr(self, "field_step_seq", 0) or 0) + 1
        profile_total_start = self._field_profile_start()
        profile_section_start = self._field_profile_start()
        self._propagate_runtime_parameters()
        self._sync_neurons_from_arrays()
        self._field_profile_debug(
            "mcm_field.step.sync_neurons",
            profile_section_start,
            extra=f"agents={int(self.N)}|dims={int(self.D)}",
        )

        vectorized_step_enabled = bool(getattr(Config, "MCM_FIELD_VECTORIZED_STEP_ENABLED", True))
        neighbor_state_map = None
        if not vectorized_step_enabled:
            profile_section_start = self._field_profile_start()
            neighbor_state_map = self._build_local_neighbor_state_map()
            self._field_profile_debug(
                "mcm_field.step.build_neighbor_state_map",
                profile_section_start,
                extra=f"agents={int(self.N)}|neighbors={int(self.local_neighbor_count or 0)}",
            )

        profile_section_start = self._field_profile_start()
        context_memory_vector = self._build_context_memory_vector(context_trace)
        self._field_profile_debug(
            "mcm_field.step.context_memory_vector",
            profile_section_start,
            extra=f"active={bool(np.any(context_memory_vector))}",
        )

        profile_section_start = self._field_profile_start()
        context_memory_matrix = self._build_local_context_memory_matrix(
            context_trace,
            base_vector=context_memory_vector,
        )
        self._field_profile_debug(
            "mcm_field.step.context_memory_matrix",
            profile_section_start,
            extra=f"active={bool(np.any(context_memory_matrix))}|agents={int(self.N)}",
        )

        profile_section_start = self._field_profile_start()
        auditory_neural_matrix = self._build_auditory_neural_matrix(market_hearing_state)
        self._field_profile_debug(
            "mcm_field.step.auditory_neural_matrix",
            profile_section_start,
            extra=f"active={bool(np.any(auditory_neural_matrix))}|agents={int(self.N)}",
        )

        profile_section_start = self._field_profile_start()
        visual_neural_matrix = self._build_visual_neural_matrix(visual_market_state)
        self._field_profile_debug(
            "mcm_field.step.visual_neural_matrix",
            profile_section_start,
            extra=f"active={bool(np.any(visual_neural_matrix))}|agents={int(self.N)}",
        )

        profile_section_start = self._field_profile_start()
        external_step_vector = self._resolve_step_impulse_vector(
            impulse=impulse,
            motivation_impulse=motivation_impulse,
            risk_impulse=risk_impulse,
        )
        replay_step_vector = self._resolve_step_impulse_vector(
            impulse=replay_impulse,
            motivation_impulse=0.0,
            risk_impulse=0.0,
        )
        self._field_profile_debug(
            "mcm_field.step.prepare_impulse_vectors",
            profile_section_start,
            extra=f"dims={int(self.D)}",
        )

        profile_section_start = self._field_profile_start()
        neurons = list(self.neurons or [])
        if vectorized_step_enabled:
            self._step_neurons_vectorized(
                external_step_vector=external_step_vector,
                replay_step_vector=replay_step_vector,
                context_memory_matrix=context_memory_matrix,
                auditory_neural_matrix=auditory_neural_matrix,
                visual_neural_matrix=visual_neural_matrix,
                auditory_frequency_norm=float((self.auditory_neural_state or {}).get("frequency_norm", 0.0) or 0.0),
            )
        else:
            for index, neuron in enumerate(neurons):
                neuron.step(
                    neighbor_states=neighbor_state_map[int(index)] if int(index) < len(neighbor_state_map) else None,
                    prepared_external_vector=external_step_vector,
                    prepared_replay_vector=replay_step_vector,
                    prepared_context_memory_vector=context_memory_matrix[int(index)] if int(index) < len(context_memory_matrix) else None,
                    prepared_auditory_vector=auditory_neural_matrix[int(index)] if int(index) < len(auditory_neural_matrix) else None,
                    prepared_auditory_frequency_norm=float((self.auditory_neural_state or {}).get("frequency_norm", 0.0) or 0.0),
                    prepared_visual_vector=visual_neural_matrix[int(index)] if int(index) < len(visual_neural_matrix) else None,
                )
        if isinstance(getattr(self, "auditory_neural_state", None), dict) and neurons:
            aftertone_values = [
                float(np.linalg.norm(np.asarray(getattr(neuron, "auditory_aftertone", []), dtype=float)))
                for neuron in list(neurons or [])
            ]
            resonance_values = [
                float(getattr(neuron, "auditory_resonance", 0.0) or 0.0)
                for neuron in list(neurons or [])
            ]
            self.auditory_neural_state["aftertone_mean"] = float(np.mean(aftertone_values)) if aftertone_values else 0.0
            self.auditory_neural_state["resonance_mean"] = float(np.mean(resonance_values)) if resonance_values else float(self.auditory_neural_state.get("resonance_mean", 0.0) or 0.0)
            self.auditory_neural_state["resonance_max"] = float(np.max(resonance_values)) if resonance_values else float(self.auditory_neural_state.get("resonance_max", 0.0) or 0.0)
            self.auditory_neural_state["action_permission"] = 0.0
        if isinstance(getattr(self, "visual_neural_state", None), dict) and neurons:
            afterimage_values = [
                float(np.linalg.norm(np.asarray(getattr(neuron, "visual_afterimage", []), dtype=float)))
                for neuron in list(neurons or [])
            ]
            resonance_values = [
                float(getattr(neuron, "visual_resonance", 0.0) or 0.0)
                for neuron in list(neurons or [])
            ]
            self.visual_neural_state["afterimage_mean"] = float(np.mean(afterimage_values)) if afterimage_values else 0.0
            self.visual_neural_state["resonance_mean"] = float(np.mean(resonance_values)) if resonance_values else float(self.visual_neural_state.get("resonance_mean", 0.0) or 0.0)
            self.visual_neural_state["resonance_max"] = float(np.max(resonance_values)) if resonance_values else float(self.visual_neural_state.get("resonance_max", 0.0) or 0.0)
            self.visual_neural_state["action_permission"] = 0.0
        self._field_profile_debug(
            "mcm_field.step.neuron_loop",
            profile_section_start,
            extra=f"agents={int(self.N)}|neighbors={int(self.local_neighbor_count or 0)}",
        )

        profile_section_start = self._field_profile_start()
        self._apply_activity_diffusion()
        self._field_profile_debug(
            "mcm_field.step.activity_diffusion",
            profile_section_start,
            extra=f"agents={int(self.N)}|neighbors={int(self.local_neighbor_count or 0)}",
        )

        profile_section_start = self._field_profile_start()
        self._refresh_arrays_from_neurons()
        self._field_profile_debug(
            "mcm_field.step.refresh_arrays",
            profile_section_start,
            extra=f"agents={int(self.N)}|dims={int(self.D)}",
        )

        profile_section_start = self._field_profile_start()
        self._refresh_areal_state()
        areal_skipped = bool((self.areal_state or {}).get("areal_refresh_skipped", False))
        self._field_profile_debug(
            "mcm_field.step.refresh_areal_state_skipped" if areal_skipped else "mcm_field.step.refresh_areal_state",
            profile_section_start,
            extra=f"agents={int(self.N)}|every_n={int(getattr(Config, 'MCM_FIELD_AREAL_REFRESH_EVERY_N', 1) or 1)}",
        )

        profile_section_start = self._field_profile_start()
        self._build_field_perception_state()
        self._field_profile_debug(
            "mcm_field.step.field_perception_state",
            profile_section_start,
            extra=f"agents={int(self.N)}",
        )

        self._field_profile_debug(
            "mcm_field.step.total",
            profile_total_start,
            extra=f"agents={int(self.N)}|dims={int(self.D)}",
        )
        if not bool(return_snapshot):
            return None
        return self.read_snapshot()
    
    # --------------------------------------------------
    def _build_component_internal_distance_mean(self, component_energy):

        values = np.asarray(component_energy, dtype=float)

        if values.ndim != 2 or len(values) <= 1:
            return 0.0

        distances = []

        for index in range(len(values)):
            if int(index) + 1 >= len(values):
                continue

            local_delta = values[int(index) + 1:] - values[int(index)]
            if len(local_delta) <= 0:
                continue

            distances.extend(np.linalg.norm(local_delta, axis=1).tolist())

        return float(np.mean(distances)) if distances else 0.0
    
# --------------------------------------------------
# Clusterbildung
# --------------------------------------------------

class ClusterDetector:

    def __init__(self):

        self.tick_seq = 0
        self.last_clusters = []
        self.last_cluster_centers = []
        self.last_mean_velocity = 0.0
        self.last_topology = {
            "cluster_center_drift": 0.0,
            "cluster_count_drift": 0.0,
            "field_velocity_trend": 0.0,
            "reorganization_direction": "stable",
        }
        self.eps = float(getattr(Config, "MCM_CLUSTER_EPS", 0.4) or 0.4)
        self.min_samples = max(2, int(getattr(Config, "MCM_CLUSTER_MIN_SAMPLES", 4) or 4))
        self.detect_every_n = max(1, int(getattr(Config, "MCM_CLUSTER_EVERY_N_TICKS", 2) or 2))

    def _detect_labels_local(self, points):
        points = np.asarray(points, dtype=float)
        point_count = int(len(points))
        labels = np.full(point_count, -1, dtype=int)

        if point_count <= 0:
            return labels

        eps = max(1e-9, float(self.eps or 0.4))
        eps_sq = float(eps * eps)
        min_samples = max(1, int(self.min_samples or 1))

        delta = points[:, None, :] - points[None, :, :]
        distance_sq = np.einsum("ijk,ijk->ij", delta, delta)
        neighbors = distance_sq <= eps_sq
        core_mask = np.sum(neighbors, axis=1) >= min_samples

        visited = np.zeros(point_count, dtype=bool)
        cluster_id = 0

        for start_index in range(point_count):
            if visited[start_index] or not bool(core_mask[start_index]):
                continue

            stack = [int(start_index)]
            visited[start_index] = True
            labels[start_index] = int(cluster_id)

            while stack:
                current_index = int(stack.pop())
                current_neighbors = np.flatnonzero(neighbors[current_index])

                for neighbor_index in current_neighbors:
                    neighbor_index = int(neighbor_index)
                    if labels[neighbor_index] < 0:
                        labels[neighbor_index] = int(cluster_id)

                    if visited[neighbor_index] or not bool(core_mask[neighbor_index]):
                        continue

                    visited[neighbor_index] = True
                    stack.append(int(neighbor_index))

            cluster_id += 1

        return labels

    def detect(self, energy, force: bool = False, mean_velocity=None, advance_tick: bool = True):

        if bool(advance_tick):
            self.tick_seq = int(self.tick_seq or 0) + 1

        current_velocity = float(mean_velocity or 0.0) if mean_velocity is not None else float(self.last_mean_velocity or 0.0)
        previous_velocity = float(self.last_mean_velocity or 0.0)
        field_velocity_trend = float(current_velocity - previous_velocity)

        if (not bool(force)) and self.last_clusters and (self.tick_seq % self.detect_every_n) != 0:
            self.last_mean_velocity = float(current_velocity)
            self.last_topology["field_velocity_trend"] = float(field_velocity_trend)
            return [np.array(item, copy=True) for item in list(self.last_clusters or [])]

        points = np.asarray(energy, dtype=float)

        if len(points) < self.min_samples:
            previous_cluster_count = len(list(self.last_cluster_centers or []))

            self.last_clusters = []
            self.last_cluster_centers = []
            self.last_mean_velocity = float(current_velocity)
            self.last_topology = {
                "cluster_center_drift": 0.0,
                "cluster_count_drift": float(previous_cluster_count),
                "field_velocity_trend": float(field_velocity_trend),
                "reorganization_direction": "dissolving" if previous_cluster_count > 0 else "stable",
            }
            return []

        labels = self._detect_labels_local(points)

        clusters = []

        for c in set(labels):
            if c == -1:
                continue
            clusters.append(np.array(points[labels == c], copy=True))

        current_centers = [
            np.mean(item, axis=0)
            for item in list(clusters or [])
            if len(item) > 0
        ]
        previous_centers = [
            np.asarray(item, dtype=float)
            for item in list(self.last_cluster_centers or [])
        ]

        cluster_center_drift = 0.0
        if current_centers and previous_centers:
            drift_values = []

            for center in current_centers:
                distances = [
                    float(np.linalg.norm(np.asarray(center, dtype=float) - prev_center))
                    for prev_center in previous_centers
                ]
                if distances:
                    drift_values.append(float(min(distances)))

            if drift_values:
                cluster_center_drift = float(np.mean(drift_values))

        cluster_count_drift = float(
            abs(len(current_centers) - len(previous_centers))
            / max(1, max(len(current_centers), len(previous_centers)))
        )

        if not previous_centers and current_centers:
            reorganization_direction = "forming"
            reorganization_direction_pressures = {"forming": 1.0}
        elif previous_centers and not current_centers:
            reorganization_direction = "dissolving"
            reorganization_direction_pressures = {"dissolving": 1.0}
        else:
            reorganization_direction_pressures = {
                "reorganizing": float(min(1.0, (cluster_center_drift * 2.4) + (cluster_count_drift * 0.72))),
                "accelerating": float(min(1.0, max(0.0, field_velocity_trend) * 4.0)),
                "settling": float(min(1.0, max(0.0, -field_velocity_trend) * 4.0)),
                "stable": float(max(0.0, 1.0 - min(1.0, (cluster_center_drift * 2.2) + (cluster_count_drift * 0.62) + (abs(field_velocity_trend) * 3.0)))),
            }
            reorganization_direction = max(reorganization_direction_pressures, key=reorganization_direction_pressures.get)

        self.last_clusters = [np.array(item, copy=True) for item in list(clusters or [])]
        self.last_cluster_centers = [
            np.asarray(item, dtype=float)
            for item in list(current_centers or [])
        ]
        self.last_mean_velocity = float(current_velocity)
        self.last_topology = {
            "cluster_center_drift": float(cluster_center_drift),
            "cluster_count_drift": float(cluster_count_drift),
            "field_velocity_trend": float(field_velocity_trend),
            "reorganization_direction": str(reorganization_direction),
            "reorganization_direction_pressures": dict(reorganization_direction_pressures),
        }

        return [np.array(item, copy=True) for item in list(self.last_clusters or [])]


# --------------------------------------------------
# Gedächtnis
# --------------------------------------------------

class Memory:

    def __init__(self):
        self.memory = []
        self.decay = 0.85
        self.max_items = 12

    def store(self, clusters):

        updated_memory = []

        for item in self.memory:
            updated_memory.append({
                "center": float(item["center"]),
                "strength": max(1, int(round(item["strength"] * self.decay)))
            })

        for c in clusters:

            center = float(np.mean(c[:,0]))
            strength = int(len(c))
            merged = False

            for item in updated_memory:
                if abs(item["center"] - center) <= 0.35:
                    item["center"] = 0.5 * (item["center"] + center)
                    item["strength"] += strength
                    merged = True
                    break

            if not merged:
                updated_memory.append({
                    "center": center,
                    "strength": strength
                })

        updated_memory = sorted(
            updated_memory,
            key=lambda x: x["strength"],
            reverse=True
        )[:self.max_items]

        self.memory = updated_memory

    def strongest(self):

        if not self.memory:
            return None

        return max(self.memory, key=lambda x: x["strength"])

    def replay_impulse(self, replay_scale=0.08):

        if not self.memory:
            return 0.0

        item = random.choice(self.memory)

        return replay_scale * float(item["center"])


# --------------------------------------------------
# Attraktoren
# --------------------------------------------------

class AttractorSystem:

    def choose(self, memory, self_state):

        def _clip01(value):
            return max(0.0, min(1.0, float(value)))

        state = str(self_state or "").strip().lower()
        stressed = 1.0 if state == "stressed" else 0.0
        excited = 1.0 if state == "excited" else 0.0

        if memory is None:
            attractor_pressures = {
                "defense": 0.44 * stressed,
                "explore": 0.44 * excited,
                "neutral": 0.28 + ((1.0 - max(stressed, excited)) * 0.20),
            }
            self.last_attractor_pressures = dict(attractor_pressures)
            return max(attractor_pressures, key=attractor_pressures.get)

        e = memory["center"]
        attractor_pressures = {
            "defense": _clip01((max(0.0, -e) * 0.36) + (stressed * 0.28)),
            "analysis": _clip01((max(0.0, -e) * 0.16) + (max(0.0, 1.0 - abs(e)) * 0.18) + (stressed * 0.08)),
            "cooperate": _clip01((max(0.0, 1.0 - abs(e)) * 0.34) + (max(0.0, e) * 0.08)),
            "explore": _clip01((max(0.0, e) * 0.32) + (excited * 0.26)),
            "neutral": _clip01(0.18 + (max(0.0, 1.0 - abs(e)) * 0.12)),
        }
        self.last_attractor_pressures = dict(attractor_pressures)
        return max(attractor_pressures, key=attractor_pressures.get)

# --------------------------------------------------
# Handlungssystem
# --------------------------------------------------

class ActionSystem:

    def act(self, attractor):

        actions = {
            "defense": "block / withdraw",
            "analysis": "observe / process",
            "cooperate": "engage socially",
            "explore": "seek novelty",
            "neutral": "idle"
        }

        return actions.get(attractor, "idle")

# --------------------------------------------------
# MCM Neuron
# --------------------------------------------------
class MCMNeuron:

    def __init__(self, dims=DIMS):
        self.dims = max(1, int(dims or DIMS))
        self.field_index = -1
        self.field_position = np.zeros(2, dtype=float)
        self.topology_neighbors = []

        self.state = np.random.uniform(-0.3, 0.3, self.dims)
        self.velocity = np.zeros(self.dims, dtype=float)

        self.last_external_impulse = np.zeros(self.dims, dtype=float)
        self.last_memory_impulse = np.zeros(self.dims, dtype=float)
        self.last_context_memory_impulse = np.zeros(self.dims, dtype=float)
        self.last_coupling_force = np.zeros(self.dims, dtype=float)
        self.last_regulation_force = np.zeros(self.dims, dtype=float)
        self.last_total_impulse = np.zeros(self.dims, dtype=float)
        self.last_memory_feedback = np.zeros(self.dims, dtype=float)
        self.last_noise = np.zeros(self.dims, dtype=float)
        self.last_field_diffusion = np.zeros(self.dims, dtype=float)
        self.last_auditory_impulse = np.zeros(self.dims, dtype=float)
        self.last_visual_impulse = np.zeros(self.dims, dtype=float)

        self.memory_trace = np.zeros(self.dims, dtype=float)
        self.auditory_aftertone = np.zeros(self.dims, dtype=float)
        self.visual_afterimage = np.zeros(self.dims, dtype=float)
        self.activation = 0.0
        self.stability = 1.0
        self.regulation_pressure = 0.0
        self.receptivity = 1.0
        self.overload = 0.0
        self.recovery_tendency = 0.0
        self.memory_resonance = 0.0
        self.auditory_resonance = 0.0
        self.auditory_frequency_norm = 0.0
        self.visual_resonance = 0.0
        self.context_reactivation = 0.0
        self.coupling_resonance = 0.0
        self.field_perception_weight = 0.0
        self.activity_label = "quiet"
        self.activation_components = {}

        self.center_force = float(getattr(Config, "MCM_CENTER_FORCE", 0.0100) or 0.0100)
        self.coupling_strength = float(getattr(Config, "MCM_COUPLING", 0.045) or 0.045)
        self.noise_strength = float(getattr(Config, "MCM_NOISE", 0.08) or 0.08)
        self.coupling_sigma = float(getattr(Config, "MCM_FIELD_COUPLING_SIGMA", 0.5) or 0.5)

        self.inertia = 0.92
        self.memory_decay = 0.86
        self.memory_gain = 0.18
        self.regulation_gain = 0.24
        self.max_abs_state = 3.0

    # --------------------------------------------------
    def _clip01(self, value):
        try:
            value = float(value)
        except Exception:
            value = 0.0

        if value < 0.0:
            return 0.0
        if value > 1.0:
            return 1.0
        return float(value)

    # --------------------------------------------------
    def _vector_norm01(self, vector, scale=None):
        values = np.asarray(vector, dtype=float).ravel()
        if values.size <= 0:
            return 0.0

        resolved_scale = float(scale if scale is not None else max(float(self.max_abs_state or 3.0), 1e-9))
        resolved_scale = max(resolved_scale, 1e-9)
        norm = float(float(np.dot(values, values)) ** 0.5)
        return self._clip01(norm / (resolved_scale * max(1.0, float(self.dims) ** 0.5)))

    # --------------------------------------------------
    def _alignment(self, left, right):
        left_values = np.asarray(left, dtype=float).ravel()
        right_values = np.asarray(right, dtype=float).ravel()
        if left_values.size <= 0 or right_values.size <= 0 or left_values.size != right_values.size:
            return 0.0

        left_norm = float(float(np.dot(left_values, left_values)) ** 0.5)
        right_norm = float(float(np.dot(right_values, right_values)) ** 0.5)
        denom = float(left_norm * right_norm)
        if denom <= 1e-9:
            return 0.0

        return float(max(-1.0, min(1.0, float(np.dot(left_values, right_values)) / denom)))

    # --------------------------------------------------
    def _build_local_receptivity(self, external_vector, context_memory_vector):
        state_activity = self._vector_norm01(self.state)
        memory_activity = self._vector_norm01(self.memory_trace)
        regulation_pressure = self._clip01(float(getattr(self, "regulation_pressure", 0.0) or 0.0) / 0.38)

        external_alignment = self._alignment(self.state, external_vector)
        memory_alignment = self._alignment(self.memory_trace, external_vector + context_memory_vector)

        position = np.asarray(getattr(self, "field_position", np.zeros(2, dtype=float)), dtype=float).flatten()
        topology_bias = 0.0
        if position.size >= 2:
            topology_bias = float((position[0] * 0.025) + (position[1] * 0.015))

        receptivity = (
            0.78
            + (max(0.0, external_alignment) * 0.22)
            + (max(0.0, memory_alignment) * 0.18)
            + (memory_activity * 0.12)
            + topology_bias
            - (state_activity * 0.10)
            - (regulation_pressure * 0.18)
        )
        return float(max(0.35, min(1.35, receptivity)))

    # --------------------------------------------------
    def _clip_state(self):
        self.state = np.clip(self.state, -self.max_abs_state, self.max_abs_state)

    # --------------------------------------------------
    def _resolve_impulse_vector(self, impulse=None, motivation_impulse=0.0, risk_impulse=0.0):
        vector = np.zeros(self.dims, dtype=float)

        if isinstance(impulse, (list, tuple, np.ndarray)):
            values = np.asarray(impulse, dtype=float).flatten()
            limit = min(len(values), self.dims)
            if limit > 0:
                vector[:limit] = values[:limit]
        else:
            vector[0] = float(impulse or 0.0)

        if self.dims > 1:
            vector[1] += float(motivation_impulse or 0.0)

        if self.dims > 2:
            vector[2] += float(risk_impulse or 0.0)

        return vector

    # --------------------------------------------------
    def _build_coupling_force(self, neighbor_states):
        sigma = max(float(self.coupling_sigma or 0.5), 1e-9)

        if isinstance(neighbor_states, np.ndarray):
            states = np.asarray(neighbor_states, dtype=float)
            if states.ndim == 2 and states.shape[1] == self.dims and len(states) > 0:
                diffs = states - np.asarray(self.state, dtype=float)
                distance_sq = np.einsum("ij,ij->i", diffs, diffs)
                weights = np.exp(-(distance_sq / sigma))
                return np.sum(diffs * weights[:, None], axis=0) * float(self.coupling_strength)
            return np.zeros(self.dims, dtype=float)

        if not neighbor_states:
            return np.zeros(self.dims, dtype=float)

        force = np.zeros(self.dims, dtype=float)

        for neighbor in list(neighbor_states or []):
            neighbor_state = np.asarray(neighbor, dtype=float).flatten()
            if len(neighbor_state) != self.dims:
                continue

            diff = neighbor_state - self.state
            distance_sq = float(np.dot(diff, diff))
            weight = float(np.exp(-(distance_sq / sigma)))
            force += weight * diff

        return force * float(self.coupling_strength)

    # --------------------------------------------------
    def _build_regulation_force(self):
        center_pull = -float(self.center_force) * self.state

        overload = max(
            abs(float(self.state[0] if self.dims > 0 else 0.0)),
            abs(float(self.state[2] if self.dims > 2 else 0.0)),
        )

        regulation_scale = min(1.0, overload / 2.2)
        damping = -self.velocity * (self.regulation_gain * regulation_scale)

        regulation_force = center_pull + damping
        self.regulation_pressure = float(np.mean(np.abs(regulation_force)))
        return regulation_force

    # --------------------------------------------------
    def _update_memory_trace(self, total_impulse):
        self.memory_trace = (self.memory_trace * self.memory_decay) + (np.asarray(total_impulse, dtype=float) * self.memory_gain)
        return np.asarray(self.memory_trace, dtype=float)

    # --------------------------------------------------
    def _update_auditory_trace(self, auditory_vector, auditory_frequency_norm=0.0):
        values = np.asarray(auditory_vector, dtype=float).flatten()
        vector = np.zeros(self.dims, dtype=float)
        limit = min(int(values.size), int(self.dims))
        if limit > 0:
            vector[:limit] = values[:limit]

        decay = float(getattr(Config, "MCM_MARKET_AUDIO_AFTERTONE_DECAY", 0.88) or 0.88)
        decay = float(max(0.0, min(0.995, decay)))
        self.last_auditory_impulse = np.asarray(vector, dtype=float)
        self.auditory_aftertone = (np.asarray(self.auditory_aftertone, dtype=float) * decay) + (vector * (1.0 - decay))
        self.auditory_resonance = self._vector_norm01(vector, scale=0.12)
        self.auditory_frequency_norm = self._clip01(float(auditory_frequency_norm or 0.0))
        return np.asarray(vector, dtype=float)

    # --------------------------------------------------
    def _update_visual_trace(self, visual_vector):
        values = np.asarray(visual_vector, dtype=float).flatten()
        vector = np.zeros(self.dims, dtype=float)
        limit = min(int(values.size), int(self.dims))
        if limit > 0:
            vector[:limit] = values[:limit]

        decay = float(getattr(Config, "MCM_MARKET_VISUAL_AFTERIMAGE_DECAY", 0.90) or 0.90)
        decay = float(max(0.0, min(0.995, decay)))
        self.last_visual_impulse = np.asarray(vector, dtype=float)
        self.visual_afterimage = (np.asarray(self.visual_afterimage, dtype=float) * decay) + (vector * (1.0 - decay))
        self.visual_resonance = self._vector_norm01(vector, scale=0.10)
        return np.asarray(vector, dtype=float)

    # --------------------------------------------------
    def _update_activity_readout(
        self,
        external_vector,
        replay_vector,
        context_memory_vector,
        coupling_force,
        regulation_force,
        memory_feedback,
        noise,
        sensory_vector=None,
    ):
        external_intensity = self._vector_norm01(external_vector, scale=1.0)
        replay_intensity = self._vector_norm01(replay_vector, scale=1.0)
        context_intensity = self._vector_norm01(context_memory_vector, scale=0.18)
        coupling_intensity = self._vector_norm01(coupling_force, scale=0.45)
        regulation_intensity = self._vector_norm01(regulation_force, scale=0.45)
        memory_feedback_intensity = self._vector_norm01(memory_feedback, scale=0.45)
        velocity_intensity = self._vector_norm01(self.velocity, scale=float(self.max_abs_state or 3.0))
        state_intensity = self._vector_norm01(self.state, scale=float(self.max_abs_state or 3.0))
        noise_intensity = self._vector_norm01(noise, scale=0.45)
        auditory_intensity = self._vector_norm01(self.last_auditory_impulse, scale=0.12)
        visual_intensity = self._vector_norm01(self.last_visual_impulse, scale=0.10)
        sensory_intensity = self._vector_norm01(sensory_vector if sensory_vector is not None else np.zeros(self.dims, dtype=float), scale=0.12)

        self.memory_resonance = self._clip01(float(np.linalg.norm(np.asarray(self.memory_trace, dtype=float))) / (float(self.max_abs_state or 3.0) * max(1.0, np.sqrt(float(self.dims)))))
        self.context_reactivation = self._clip01(context_intensity)
        self.coupling_resonance = self._clip01(coupling_intensity)
        self.overload = self._clip01((state_intensity * 0.36) + (velocity_intensity * 0.24) + (regulation_intensity * 0.22) + (context_intensity * 0.12) + (sensory_intensity * 0.06))
        self.recovery_tendency = self._clip01((regulation_intensity * 0.36) + ((1.0 - self.overload) * 0.26) + (max(0.0, 1.0 - velocity_intensity) * 0.18) + (self.memory_resonance * 0.10))

        raw_activation = (
            external_intensity * 0.26
            + replay_intensity * 0.10
            + context_intensity * 0.16
            + coupling_intensity * 0.18
            + memory_feedback_intensity * 0.10
            + velocity_intensity * 0.12
            + auditory_intensity * 0.04
            + visual_intensity * 0.04
            + self.memory_resonance * 0.06
            + noise_intensity * 0.02
        )
        self.activation = self._clip01(raw_activation * 2.15)
        self.stability = self._clip01(
            1.0
            - (self.overload * 0.46)
            - (velocity_intensity * 0.24)
            - (coupling_intensity * 0.10)
            + (self.recovery_tendency * 0.18)
            + (self.memory_resonance * 0.06)
        )

        activity_label_pressures = {
            "overloaded": float((self.overload * 0.48) + (self.activation * 0.20) + ((1.0 - self.stability) * 0.12)),
            "memory_reactivated": float((self.context_reactivation * 0.44) + (self.memory_resonance * 0.32) + (self.activation * 0.10)),
            "locally_coupled": float((self.coupling_resonance * 0.44) + (self.activation * 0.24) + (self.stability * 0.08)),
            "recovering": float((self.recovery_tendency * 0.44) + ((1.0 - self.activation) * 0.24) + (self.stability * 0.10)),
            "active": float((self.activation * 0.48) + (self.receptivity * 0.12) + ((1.0 - self.overload) * 0.08)),
            "settled": float((self.stability * 0.46) + ((1.0 - self.activation) * 0.24) + ((1.0 - self.overload) * 0.10)),
            "quiet": float(((1.0 - self.activation) * 0.34) + ((1.0 - self.overload) * 0.20) + ((1.0 - self.context_reactivation) * 0.08)),
        }
        self.activity_label = max(activity_label_pressures, key=activity_label_pressures.get)

        if bool(getattr(Config, "MCM_NEURON_ACTIVATION_COMPONENTS_ENABLED", True)):
            self.activation_components = {
                "external_intensity": float(round(external_intensity, 4)),
                "replay_intensity": float(round(replay_intensity, 4)),
                "context_intensity": float(round(context_intensity, 4)),
                "coupling_intensity": float(round(coupling_intensity, 4)),
                "regulation_intensity": float(round(regulation_intensity, 4)),
                "memory_feedback_intensity": float(round(memory_feedback_intensity, 4)),
                "velocity_intensity": float(round(velocity_intensity, 4)),
                "state_intensity": float(round(state_intensity, 4)),
                "noise_intensity": float(round(noise_intensity, 4)),
                "auditory_intensity": float(round(auditory_intensity, 4)),
                "visual_intensity": float(round(visual_intensity, 4)),
                "sensory_intensity": float(round(sensory_intensity, 4)),
                "auditory_action_permission": 0.0,
                "visual_action_permission": 0.0,
                "activity_label_pressures": dict(activity_label_pressures),
            }
        elif self.activation_components:
            self.activation_components = {}

    # --------------------------------------------------
    def read_snapshot(self):
        return {
            "field_index": int(getattr(self, "field_index", -1)),
            "field_position": [float(round(v, 4)) for v in np.asarray(getattr(self, "field_position", np.zeros(2, dtype=float)), dtype=float).tolist()],
            "topology_neighbors": [int(item) for item in list(getattr(self, "topology_neighbors", []) or [])],
            "state": [float(round(v, 4)) for v in self.state.tolist()],
            "velocity": [float(round(v, 4)) for v in self.velocity.tolist()],
            "memory_trace": [float(round(v, 4)) for v in self.memory_trace.tolist()],
            "activation": float(round(self.activation, 4)),
            "stability": float(round(self.stability, 4)),
            "regulation_pressure": float(round(self.regulation_pressure, 4)),
            "receptivity": float(round(self.receptivity, 4)),
            "overload": float(round(self.overload, 4)),
            "recovery_tendency": float(round(self.recovery_tendency, 4)),
            "memory_resonance": float(round(self.memory_resonance, 4)),
            "auditory_resonance": float(round(self.auditory_resonance, 4)),
            "auditory_frequency_norm": float(round(self.auditory_frequency_norm, 4)),
            "visual_resonance": float(round(self.visual_resonance, 4)),
            "context_reactivation": float(round(self.context_reactivation, 4)),
            "coupling_resonance": float(round(self.coupling_resonance, 4)),
            "field_perception_weight": float(round(self.field_perception_weight, 4)),
            "activity_label": str(self.activity_label or "quiet"),
            "activation_components": dict(self.activation_components or {}),
            "external_impulse": [float(round(v, 4)) for v in self.last_external_impulse.tolist()],
            "auditory_impulse": [float(round(v, 4)) for v in self.last_auditory_impulse.tolist()],
            "auditory_aftertone": [float(round(v, 4)) for v in self.auditory_aftertone.tolist()],
            "visual_impulse": [float(round(v, 4)) for v in self.last_visual_impulse.tolist()],
            "visual_afterimage": [float(round(v, 4)) for v in self.visual_afterimage.tolist()],
            "memory_impulse": [float(round(v, 4)) for v in self.last_memory_impulse.tolist()],
            "context_memory_impulse": [float(round(v, 4)) for v in self.last_context_memory_impulse.tolist()],
            "total_impulse": [float(round(v, 4)) for v in self.last_total_impulse.tolist()],
            "memory_feedback": [float(round(v, 4)) for v in self.last_memory_feedback.tolist()],
            "noise": [float(round(v, 4)) for v in self.last_noise.tolist()],
            "field_diffusion": [float(round(v, 4)) for v in self.last_field_diffusion.tolist()],
            "coupling_force": [float(round(v, 4)) for v in self.last_coupling_force.tolist()],
            "regulation_force": [float(round(v, 4)) for v in self.last_regulation_force.tolist()],
        }

    # --------------------------------------------------
    def step(
        self,
        external_impulse=None,
        neighbor_states=None,
        replay_impulse=None,
        motivation_impulse=0.0,
        risk_impulse=0.0,
        context_memory_impulse=None,
        prepared_external_vector=None,
        prepared_replay_vector=None,
        prepared_context_memory_vector=None,
        prepared_auditory_vector=None,
        prepared_auditory_frequency_norm=0.0,
        prepared_visual_vector=None,
    ):
        if prepared_external_vector is None:
            external_vector = self._resolve_impulse_vector(
                impulse=external_impulse,
                motivation_impulse=motivation_impulse,
                risk_impulse=risk_impulse,
            )
        else:
            external_vector = np.asarray(prepared_external_vector, dtype=float)

        if prepared_replay_vector is None:
            replay_vector = self._resolve_impulse_vector(
                impulse=replay_impulse,
                motivation_impulse=0.0,
                risk_impulse=0.0,
            )
        else:
            replay_vector = np.asarray(prepared_replay_vector, dtype=float)

        if prepared_context_memory_vector is None:
            context_memory_vector = self._resolve_impulse_vector(
                impulse=context_memory_impulse,
                motivation_impulse=0.0,
                risk_impulse=0.0,
            )
        else:
            context_memory_vector = np.asarray(prepared_context_memory_vector, dtype=float)

        auditory_vector = np.asarray(prepared_auditory_vector, dtype=float) if prepared_auditory_vector is not None else np.zeros(self.dims, dtype=float)
        self._update_auditory_trace(auditory_vector, auditory_frequency_norm=prepared_auditory_frequency_norm)
        visual_vector = np.asarray(prepared_visual_vector, dtype=float) if prepared_visual_vector is not None else np.zeros(self.dims, dtype=float)
        self._update_visual_trace(visual_vector)

        self.receptivity = self._build_local_receptivity(external_vector, context_memory_vector)
        external_vector = np.asarray(external_vector, dtype=float) * float(self.receptivity)

        self.last_external_impulse = np.asarray(external_vector, dtype=float)
        self.last_memory_impulse = np.asarray(replay_vector, dtype=float)
        self.last_context_memory_impulse = np.asarray(context_memory_vector, dtype=float)

        coupling_force = self._build_coupling_force(neighbor_states)
        regulation_force = self._build_regulation_force()

        self.last_coupling_force = np.asarray(coupling_force, dtype=float)
        self.last_regulation_force = np.asarray(regulation_force, dtype=float)

        total_impulse = external_vector + replay_vector
        sensory_vector = (auditory_vector * 0.18) + (visual_vector * 0.24)
        memory_feedback = self._update_memory_trace(total_impulse + context_memory_vector) * 0.35
        noise = np.random.randn(self.dims) * float(self.noise_strength)
        self.last_total_impulse = np.asarray(total_impulse, dtype=float)
        self.last_memory_feedback = np.asarray(memory_feedback, dtype=float)
        self.last_noise = np.asarray(noise, dtype=float)

        self.velocity = (self.velocity * self.inertia) + coupling_force + regulation_force + total_impulse + memory_feedback + sensory_vector + noise
        self.state = self.state + self.velocity
        self._clip_state()
        self._update_activity_readout(
            external_vector=external_vector,
            replay_vector=replay_vector,
            context_memory_vector=context_memory_vector,
            coupling_force=coupling_force,
            regulation_force=regulation_force,
            memory_feedback=memory_feedback,
            noise=noise,
            sensory_vector=sensory_vector,
        )

        if bool(getattr(Config, "MCM_NEURON_STEP_RETURN_SNAPSHOT", False)):
            return self.read_snapshot()
        return None
    
# --------------------------------------------------
# KI Agent
# --------------------------------------------------

class MCM_AI:

    def __init__(self):

        self.perception = Perception()
        self.self_model = SelfModel()
        self.field = MCMField()
        self.cluster = ClusterDetector()
        self.memory = Memory()
        self.attractor = AttractorSystem()
        self.action = ActionSystem()
        self.regulation = RegulationLayer()


    def step(self, stimulus):

        # Wahrnehmung
        external_impulse = self.perception.encode(stimulus)

        # interner Replay-Impuls
        replay_impulse = self.memory.replay_impulse(replay_scale=0.05)
        total_impulse = external_impulse + replay_impulse

        # interne Gedankenzyklen
        internal_cycles = 3

        for _ in range(internal_cycles):
            self.field.step(replay_impulse)

        # Feld Dynamik mit externem Stimulus
        self.field.step(total_impulse)

        # Clusterbildung
        clusters = self.cluster.detect(self.field.energy)

        # Gedächtnis
        self.memory.store(clusters)

        # Selbstzustand
        self_state = self.self_model.evaluate(self.field.energy)

        # Regulation
        self.regulation.regulate(self.field)

        # Attraktor
        attractor = self.attractor.choose(self.memory.strongest(), self_state)

        # Handlung
        action = self.action.act(attractor)

        return action

# --------------------------------------------------
# Regulation / Homeostasis
# --------------------------------------------------

class RegulationLayer:

    def regulate(self, field):

        mean_energy = float(np.mean(field.energy[:,0]))
        mean_risk = float(np.mean(field.energy[:,2])) if getattr(field, "D", 0) > 2 else 0.0

        # Energie zu hoch → Exploration bremsen
        def _clip01(value):
            return max(0.0, min(1.0, float(value)))

        high_energy_pressure = _clip01(mean_energy / 3.0)
        low_energy_pressure = _clip01(-mean_energy / 3.0)
        balance_pressure = _clip01(1.0 - (abs(mean_energy) / 3.0))

        field.velocity *= max(
            0.35,
            1.0
            - (high_energy_pressure * 0.35)
            - (low_energy_pressure * 0.30)
            - (balance_pressure * 0.05),
        )
        field.energy[:,0] -= 0.25 * high_energy_pressure
        field.energy[:,0] += 0.15 * low_energy_pressure

        # Energie zu niedrig → Defense bremsen
        if getattr(field, "D", 0) > 2:
            negative_risk_pressure = _clip01(-mean_risk / 3.0)
            positive_risk_pressure = _clip01(mean_risk / 3.0)
            risk_relief_pressure = max(negative_risk_pressure, positive_risk_pressure)
            field.velocity[:,2] *= max(0.55, 1.0 - (risk_relief_pressure * 0.28))
            field.energy[:,2] += 0.18 * negative_risk_pressure
            field.energy[:,2] -= 0.18 * positive_risk_pressure

# --------------------------------------------------
# Beispiel
# --------------------------------------------------
if __name__ == "__main__":

    ai = MCM_AI()

    stimuli = ["neutral", "positive", "negative", "reward", "threat"]

    for t in range(200):

        stimulus = random.choice(stimuli)

        action = ai.step(stimulus)

        mean_energy = np.mean(ai.field.energy[:, 0])

        print(t, stimulus, "→", action, "| energy:", round(mean_energy, 3))
