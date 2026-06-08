# 24 Code-Bausteine

Diese Datei ergänzt den schriftlichen DIO-Aufbau um technische Bausteine.

Wichtig:

Diese Bausteine sind keine fertige Implementierung. Sie sind eine
Konstruktionsvorlage, damit Code später gegen die DIO-Schichten gebaut oder
geprüft werden kann.

## Grundlauf

```python
def run_dio_tick(raw_world_packet, dio_state):
    world_state = build_world_state(raw_world_packet)
    visual_state = build_visual_form_state(world_state, dio_state.visual_window)
    hearing_state = build_market_hearing_state(world_state, dio_state.hearing_baseline)
    field_state = update_mcm_field_state(visual_state, hearing_state, dio_state.mcm_field)
    memory_state = query_memory_state(visual_state, field_state, dio_state.memory)
    thought_state = build_thought_state(visual_state, field_state, memory_state, dio_state.thought_memory)
    reality_state = check_reality_state(thought_state, visual_state, field_state, memory_state)
    action_state = derive_action_state(visual_state, field_state, memory_state, reality_state)
    consequence_state = observe_consequence_state(action_state, world_state, dio_state.active_position)
    regulation_state = update_regulation_state(
        visual_state,
        field_state,
        memory_state,
        thought_state,
        reality_state,
        action_state,
        consequence_state,
    )

    return DIOCycleState(
        world=world_state,
        visual=visual_state,
        hearing=hearing_state,
        field=field_state,
        memory=memory_state,
        thought=thought_state,
        reality=reality_state,
        action=action_state,
        consequence=consequence_state,
        regulation=regulation_state,
    )
```

## Zustandsobjekte

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class WorldState:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    time_delta: float
    world_index: int


@dataclass
class VisualFormState:
    form_id: str
    form_family: str
    direction_trace: float
    compression_trace: float
    area_trace: float
    recurrence_trace: float
    time_depth: float
    visual_uncertainty: float


@dataclass
class MarketHearingState:
    loudness: float
    frequency_hz: float
    compression: float
    tone: str


@dataclass
class MCMFieldState:
    field_tension: float
    field_coherence: float
    field_bearing: float
    field_afterimage: float
    field_distance: float
    field_overcoupling: float


@dataclass
class MemoryMatchState:
    known_form_family: str
    similarity_trace: float
    past_bearing: float
    past_risk: float
    past_context: str
    memory_confidence: float


@dataclass
class ThoughtState:
    thought_id: str
    thought_family: str
    hypothesis_direction: str
    hypothesis_area: Optional[float]
    hypothesis_reason: str
    thought_uncertainty: float
    thought_load: float


@dataclass
class RealityCheckState:
    inner_outer_fit: float
    hypothesis_reality_fit: float
    form_mcm_fit: float
    maturity: float
    trust: float
    carefulness: float
    reorganization_pressure: float


@dataclass
class ActionState:
    action_intention: str
    entry_area: Optional[float]
    entry_price: Optional[float]
    sl_price: Optional[float]
    tp_price: Optional[float]
    order_side: str
    value_gate_passed: bool
    action_distance: float


@dataclass
class ConsequenceState:
    outcome_type: str
    realized_pnl: float
    trade_duration: int
    hypothesis_confirmed: bool
    form_contact_confirmed: bool
    mcm_contact_confirmed: bool
    consequence_pressure: float


@dataclass
class RegulationState:
    focus_level: float
    distance_level: float
    cognitive_load: float
    nervous_system_load: float
    action_depth: float
    reflection_pull: float
    recovery_need: float


@dataclass
class DIOCycleState:
    world: WorldState
    visual: VisualFormState
    hearing: MarketHearingState
    field: MCMFieldState
    memory: MemoryMatchState
    thought: ThoughtState
    reality: RealityCheckState
    action: ActionState
    consequence: ConsequenceState
    regulation: RegulationState
```

## Welt-Baustein

```python
def build_world_state(raw_packet) -> WorldState:
    return WorldState(
        timestamp=int(raw_packet["timestamp"]),
        open=float(raw_packet["open"]),
        high=float(raw_packet["high"]),
        low=float(raw_packet["low"]),
        close=float(raw_packet["close"]),
        volume=float(raw_packet["volume"]),
        time_delta=float(raw_packet.get("time_delta", 0.0)),
        world_index=int(raw_packet.get("world_index", 0)),
    )
```

Regel:

`WorldState` deutet nicht. Er enthält nur reale Außenwelt.

## Sehen-Baustein

```python
def build_visual_form_state(world_state: WorldState, visual_window) -> VisualFormState:
    direction_trace = derive_direction_trace(visual_window)
    compression_trace = derive_compression_trace(visual_window)
    area_trace = derive_area_trace(visual_window)
    recurrence_trace = derive_recurrence_trace(visual_window)
    time_depth = derive_time_depth(visual_window, world_state.timestamp)

    return VisualFormState(
        form_id=make_form_id(direction_trace, compression_trace, area_trace),
        form_family=derive_form_family(direction_trace, compression_trace, recurrence_trace),
        direction_trace=direction_trace,
        compression_trace=compression_trace,
        area_trace=area_trace,
        recurrence_trace=recurrence_trace,
        time_depth=time_depth,
        visual_uncertainty=derive_visual_uncertainty(visual_window),
    )
```

Regel:

Sehen erkennt Form. Sehen erzeugt keinen Entry.

## Hören-Baustein

```python
def build_market_hearing_state(world_state: WorldState, hearing_baseline) -> MarketHearingState:
    raw_energy = derive_candle_energy(world_state)
    loudness = normalize_market_loudness(raw_energy, hearing_baseline)
    frequency_hz = map_loudness_to_frequency(loudness, min_hz=0.0, max_hz=17000.0)
    compression = derive_hearing_compression(raw_energy, loudness)

    return MarketHearingState(
        sense="hearing",
        channel="market_audio",
        loudness=loudness,
        frequency_hz=frequency_hz,
        compression=compression,
        tone=derive_hearing_tone(loudness, frequency_hz, compression),
        action_permission=0.0,
    )
```

Regel:

Hören übersetzt Energie in Marktmelodie. Hören erzeugt keinen Entry und keine
direkte innere Feldlage.

Aktueller Codeanker:

- `core/market_audio.py`
- `bot_engine/mcm_core_engine.py` nutzt diesen Adapter.
- `core/mcm_model.py` nimmt `market_hearing_state` als separate
  `auditory_*` Neuronenspur auf.

Wichtig:

```text
Hoeren -> auditive Neuronenspur
Hoeren -/-> Entry-Impuls
Hoeren -/-> Motivation/Risk-Impuls
Hoeren -/-> Trade-Plan
```

Die aktuelle auditive Spur darf Neuronen sichtbar stimulieren, aber noch keine
Handlung tragen. Sie ist Sensorik, nicht Motorik.

## MCM-Feld-Baustein

```python
def update_mcm_field_state(
    visual_state: VisualFormState,
    hearing_state: MarketHearingState,
    previous_field: MCMFieldState,
) -> MCMFieldState:
    field_tension = blend_tension(previous_field.field_tension, visual_state.compression_trace)
    field_coherence = derive_field_coherence(visual_state, hearing_state, previous_field)
    field_afterimage = decay_afterimage(previous_field.field_afterimage, visual_state.time_depth)
    field_distance = derive_field_distance(visual_state, field_coherence)
    field_overcoupling = derive_overcoupling(field_tension, field_distance, field_afterimage)

    return MCMFieldState(
        field_tension=field_tension,
        field_coherence=field_coherence,
        field_bearing=derive_field_bearing(field_coherence, field_tension),
        field_afterimage=field_afterimage,
        field_distance=field_distance,
        field_overcoupling=field_overcoupling,
    )
```

Regel:

Das MCM-Feld beschreibt Wirkung, nicht Entscheidung.

## Memory-Baustein

```python
def query_memory_state(visual_state: VisualFormState, field_state: MCMFieldState, memory_store) -> MemoryMatchState:
    match = memory_store.find_similar(
        form_family=visual_state.form_family,
        field_signature=field_state,
    )

    return MemoryMatchState(
        known_form_family=match.family if match else "unknown",
        similarity_trace=match.similarity if match else 0.0,
        past_bearing=match.bearing if match else 0.0,
        past_risk=match.risk if match else 0.0,
        past_context=match.context if match else "no_context",
        memory_confidence=match.confidence if match else 0.0,
    )
```

Regel:

Memory speichert reale Erfahrung. Thought-Memory bleibt getrennt.

## Thought-Baustein

```python
def build_thought_state(
    visual_state: VisualFormState,
    field_state: MCMFieldState,
    memory_state: MemoryMatchState,
    thought_memory,
) -> ThoughtState:
    seed = thought_memory.form_seed(
        visual_form=visual_state,
        field_state=field_state,
        memory_state=memory_state,
    )

    return ThoughtState(
        thought_id=seed.id,
        thought_family=seed.family,
        hypothesis_direction=seed.possible_direction,
        hypothesis_area=seed.possible_area,
        hypothesis_reason=seed.reason,
        thought_uncertainty=seed.uncertainty,
        thought_load=seed.load,
    )
```

Regel:

Thought erzeugt Möglichkeit. Thought erzeugt keine Realität.

Thought-Memory darf nur Gedanken mit Realitätsanker schreiben:

```text
thought + real_form + real_mcm_field + time_context
```

## Realitätsprüfungs-Baustein

```python
def check_reality_state(
    thought_state: ThoughtState,
    visual_state: VisualFormState,
    field_state: MCMFieldState,
    memory_state: MemoryMatchState,
) -> RealityCheckState:
    form_mcm_fit = fit_form_to_mcm(visual_state, field_state)
    hypothesis_reality_fit = fit_thought_to_reality(thought_state, visual_state, field_state)
    inner_outer_fit = combine_inner_outer_fit(form_mcm_fit, memory_state.memory_confidence)

    return RealityCheckState(
        inner_outer_fit=inner_outer_fit,
        hypothesis_reality_fit=hypothesis_reality_fit,
        form_mcm_fit=form_mcm_fit,
        maturity=derive_maturity(form_mcm_fit, memory_state, thought_state),
        trust=derive_trust(memory_state, hypothesis_reality_fit),
        carefulness=derive_carefulness(field_state, thought_state, memory_state),
        reorganization_pressure=derive_reorganization_pressure(thought_state, field_state),
    )
```

Regel:

Realitätsprüfung moduliert Reife, Vertrauen und Vorsicht. Sie ist kein hartes
Gate.

## Handlung-Baustein

```python
def derive_action_state(
    visual_state: VisualFormState,
    field_state: MCMFieldState,
    memory_state: MemoryMatchState,
    reality_state: RealityCheckState,
) -> ActionState:
    candidate = derive_entry_candidate_from_real_contact(
        visual_state=visual_state,
        field_state=field_state,
        memory_state=memory_state,
        reality_state=reality_state,
    )

    value_ok = value_gate(candidate)

    if not value_ok:
        return ActionState(
            action_intention="observe",
            entry_area=None,
            entry_price=None,
            sl_price=None,
            tp_price=None,
            order_side="WAIT",
            value_gate_passed=False,
            action_distance=1.0,
        )

    return ActionState(
        action_intention=candidate.intention,
        entry_area=candidate.area,
        entry_price=candidate.entry,
        sl_price=candidate.sl,
        tp_price=candidate.tp,
        order_side=candidate.side,
        value_gate_passed=True,
        action_distance=candidate.distance,
    )
```

Regel:

Das Value-Gate ist das einzige harte Gate. Alle inneren Zustände wirken weich
auf Nähe, Reife, Vorsicht und Handlungstiefe.

## Konsequenz-Baustein

```python
def observe_consequence_state(action_state: ActionState, world_state: WorldState, active_position) -> ConsequenceState:
    outcome = resolve_outcome(action_state, world_state, active_position)

    return ConsequenceState(
        outcome_type=outcome.kind,
        realized_pnl=outcome.pnl,
        trade_duration=outcome.duration,
        hypothesis_confirmed=outcome.hypothesis_confirmed,
        form_contact_confirmed=outcome.form_contact_confirmed,
        mcm_contact_confirmed=outcome.mcm_contact_confirmed,
        consequence_pressure=outcome.pressure,
    )
```

Regel:

Konsequenz bewertet nicht nur Gewinn oder Verlust. Sie bewertet Wahrnehmung,
Gedanke, Handlung, Nicht-Handlung und Feldwirkung.

Rückschreiben erfolgt getrennt:

```python
def commit_consequence(consequence_state, memory_store, thought_memory, field_state, regulation_state):
    memory_store.write_real_experience(consequence_state.real_experience)
    thought_memory.write_thought_feedback(consequence_state.thought_feedback)
    update_field_from_consequence(field_state, consequence_state.field_feedback)
    update_regulation_from_consequence(regulation_state, consequence_state.regulation_feedback)
```

Regel:

Ein Gedanke wird bewertet, aber nicht nachträglich zur Realität erklärt.

## Regulation-Baustein

```python
def update_regulation_state(
    visual_state: VisualFormState,
    field_state: MCMFieldState,
    memory_state: MemoryMatchState,
    thought_state: ThoughtState,
    reality_state: RealityCheckState,
    action_state: ActionState,
    consequence_state: ConsequenceState,
) -> RegulationState:
    cognitive_load = derive_cognitive_load(thought_state, reality_state)
    nervous_load = derive_nervous_system_load(field_state, consequence_state)
    distance_level = derive_distance_level(field_state, reality_state, nervous_load)

    return RegulationState(
        focus_level=derive_focus_level(visual_state, thought_state, reality_state),
        distance_level=distance_level,
        cognitive_load=cognitive_load,
        nervous_system_load=nervous_load,
        action_depth=derive_action_depth(action_state, reality_state),
        reflection_pull=derive_reflection_pull(cognitive_load, field_state, reality_state),
        recovery_need=derive_recovery_need(nervous_load, consequence_state),
    )
```

Regel:

Regulation verändert DIOs Haltung. Sie ersetzt nicht Welt, Sehen, Memory oder
Handlung.

## MCM-Neuron-Baustein

```python
@dataclass
class MCMNeuronState:
    activation: float = 0.0
    sensitivity: float = 1.0
    refractory_state: float = 0.0
    bearing_trace: float = 0.0
    stress_trace: float = 0.0
    trust_trace: float = 0.0
    afterimage: float = 0.0
    plasticity: float = 0.0


def update_mcm_neuron(
    neuron: MCMNeuronState,
    visual_input: float,
    field_input: float,
    memory_input: float,
    neurochemical_modulation,
) -> MCMNeuronState:
    activation_drive = (
        visual_input * neuron.sensitivity
        + field_input
        + memory_input
        - neuron.refractory_state
    )

    activation = modulate_activation(activation_drive, neurochemical_modulation)

    return MCMNeuronState(
        activation=activation,
        sensitivity=update_sensitivity(neuron, activation),
        refractory_state=update_refractory_state(neuron, activation),
        bearing_trace=update_bearing_trace(neuron, activation),
        stress_trace=update_stress_trace(neuron, neurochemical_modulation),
        trust_trace=update_trust_trace(neuron, neurochemical_modulation),
        afterimage=update_afterimage(neuron.afterimage, activation),
        plasticity=update_plasticity(neuron, activation, neurochemical_modulation),
    )
```

## Neurochemie-Baustein

```python
@dataclass
class NeurochemicalState:
    dopamine: float = 0.0
    serotonin: float = 0.0
    cortisol: float = 0.0
    adrenaline: float = 0.0
    glutamate: float = 0.0
    gaba: float = 0.0


def update_neurochemistry(field_state, consequence_state, regulation_state) -> NeurochemicalState:
    return NeurochemicalState(
        dopamine=derive_dopamine(consequence_state, regulation_state),
        serotonin=derive_serotonin(field_state, consequence_state),
        cortisol=derive_cortisol(field_state, regulation_state),
        adrenaline=derive_adrenaline(field_state, consequence_state),
        glutamate=derive_glutamate(field_state, regulation_state),
        gaba=derive_gaba(field_state, regulation_state),
    )
```

Regel:

Neurochemie ist Feldmodulation, kein Entry-Signal.

## Code-Prüfregel

Jede bestehende Funktion im Projekt soll später einer dieser Rollen zugeordnet
werden:

```text
Welt
Sehen
MCM-Feld
Memory
Thought
Realitätsprüfung
Handlung
Konsequenz
Regulation
Neuron
Neurochemie
Debug
```

Wenn eine Funktion mehrere Rollen gleichzeitig übernimmt, ist sie ein
Rückbaukandidat.
