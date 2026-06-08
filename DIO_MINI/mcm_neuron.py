"""Small MCM-neuron structure for isolated episodic learning."""

from __future__ import annotations

import math


FEATURES = (
    "sehen.form_flow",
    "sehen.form_stability",
    "sehen.form_change",
    "hoeren.energy_tone",
    "hoeren.energy_shift",
    "fuehlen.mcm_coherence",
    "fuehlen.mcm_tension",
    "fuehlen.mcm_asymmetry",
)

ACTION_NAMES = ("WAIT", "LONG", "SHORT")


def _clip(value: float, lo: float = -1.0, hi: float = 1.0) -> float:
    try:
        value = float(value)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return max(lo, min(hi, value))


def flatten_senses(senses: dict) -> dict:
    flat = {}
    for path in FEATURES:
        root, key = path.split(".", 1)
        flat[path] = _clip(dict(senses.get(root, {}) or {}).get(key, 0.0))
    return flat


class MCMNeuron:
    def __init__(self, index: int):
        self.index = int(index)
        self.activation = 0.0
        self.afterimage = 0.0
        self.weights = {}
        for i, name in enumerate(FEATURES):
            phase = (self.index + 1) * (i + 3)
            self.weights[name] = math.sin(phase * 0.73) * 0.22
        self.action_weights = {
            "WAIT": math.sin((self.index + 2) * 0.39) * 0.08,
            "LONG": math.sin((self.index + 3) * 0.61) * 0.08,
            "SHORT": math.sin((self.index + 5) * 0.47) * 0.08,
        }

    def step(self, flat: dict, neighbor_signal: float) -> float:
        raw = sum(float(flat.get(name, 0.0) or 0.0) * weight for name, weight in self.weights.items())
        raw += neighbor_signal * 0.12
        self.activation = math.tanh(raw + self.afterimage * 0.32)
        self.afterimage = (self.afterimage * 0.82) + (self.activation * 0.18)
        return self.activation

    def score_action(self, action: str) -> float:
        return self.activation * float(self.action_weights.get(action, 0.0) or 0.0)

    def learn(self, flat: dict, action: str, reward: float, rate: float = 0.035) -> None:
        reward = _clip(reward, -1.0, 1.0)
        direction = 1.0 if action == "LONG" else -1.0 if action == "SHORT" else 0.0
        if action == "WAIT":
            direction = -0.25 if reward < 0.0 else 0.10
        for name, value in flat.items():
            self.weights[name] = _clip(
                self.weights.get(name, 0.0) + rate * reward * value * max(0.15, abs(self.activation)),
                -1.0,
                1.0,
            )
        self.action_weights[action] = _clip(
            self.action_weights.get(action, 0.0) + rate * reward * max(0.20, abs(self.activation)),
            -1.0,
            1.0,
        )
        if action in ("LONG", "SHORT"):
            opposite = "SHORT" if action == "LONG" else "LONG"
            self.action_weights[opposite] = _clip(
                self.action_weights.get(opposite, 0.0) - rate * reward * 0.35 * direction,
                -1.0,
                1.0,
            )


class MiniMCMField:
    def __init__(self, neuron_count: int = 9):
        self.neurons = [MCMNeuron(index) for index in range(int(neuron_count))]
        self.last_signature = 0.0

    def step(self, senses: dict) -> dict:
        flat = flatten_senses(senses)
        previous = 0.0
        activations = []
        for neuron in self.neurons:
            activation = neuron.step(flat, previous)
            activations.append(activation)
            previous = activation
        signature = sum(activations) / max(1, len(activations))
        self.last_signature = signature
        action_scores = {
            action: sum(neuron.score_action(action) for neuron in self.neurons) / max(1, len(self.neurons))
            for action in ACTION_NAMES
        }
        return {
            "flat": flat,
            "signature": signature,
            "activations": activations,
            "action_scores": action_scores,
        }

    def learn(self, flat: dict, action: str, reward: float) -> None:
        for neuron in self.neurons:
            neuron.learn(flat, action, reward)

