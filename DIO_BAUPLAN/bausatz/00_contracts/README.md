# 00 Contracts

Contracts definieren die Zustandsobjekte zwischen den Modulen.

Sie sind der wichtigste Teil des Baukastens.

## Zweck

Ein Modul darf intern frei gebaut werden, aber es muss seinen Vertrag einhalten:

- erwartete Eingaben
- erlaubte Ausgaben
- keine fremden Zuständigkeiten
- keine fertige Deutung aus einer späteren Schicht

## Kernzustände

```text
WorldState
VisualFormState
MarketHearingState
MCMFieldState
MemoryMatchState
ThoughtState
RealityCheckState
ActionState
ConsequenceState
RegulationState
NeuronState
NeurochemicalState
LanguageState
TimeSpaceState
```

## Regel

Contracts sind keine Strategie.

Sie beschreiben nur, wie Schichten miteinander sprechen.
