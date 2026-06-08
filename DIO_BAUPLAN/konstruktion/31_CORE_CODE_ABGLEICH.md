# 31 Core-Code-Abgleich

Diese Datei ist die technische Prüflandkarte für den bestehenden Code.

Ziel: Den aktuellen Code zurück auf den Bauplan führen, ohne alte
Strategie-, Motorik- oder Gate-Logik wieder als aktive Architektur zu
übernehmen.

## Prüfregel

Jede Funktion wird einer Bauplan-Schicht zugeordnet:

```text
Welt
Sinneswahrnehmung
MCM-Feld
Memory
Thought
Realitätsprüfung
Handlung
Konsequenz
Regulation
Debug
```

## Ergaenzung Hypothese / Handlung

Eine Hypothese darf auch nicht sagen: Ich handle.

```text
Hypothese -> Realitaetskontakt -> Reife / Distanz / Naehe
Reale Form + MCM-Wirkung + Erfahrung + innere Zustimmung -> Handlungsnaehe
Handlungsnaehe + Value-Gate -> Order
```

Im Code werden alte Namen mit `*_action_*` nur noch als
Kompatibilitaetsalias behandelt. Fachlich bevorzugt sind:

```text
open_hypothesis_reality_probe
dominant_hypothesis_reality_support
current_hypothesis_reality_support
hypothesis_role = thought_reality_probe
```

Wenn eine Funktion mehrere Schichten gleichzeitig steuert, ist sie
prüfpflichtig.

## Begriffliche Risikowörter

Diese Wörter sind im aktuellen Code nicht automatisch falsch. Sie zeigen aber
alte Kopplungen an:

| Wortfeld | Risiko |
| --- | --- |
| `strategy_*` | Hypothese oder Kontakt wird wieder als Strategie behandelt |
| `motor_*` | Handlung entsteht zu früh aus Wahrnehmung oder Druck |
| `action_*` | innere Lage wird zu nah an Handlung gekoppelt |
| `permission` | innere Zustände werden wie Freigaben gelesen |
| `gate` | innere Zustände werden als Sperren behandelt |
| `block` | Distanz oder Vorsicht wird als harte Blockade gelesen |
| `impulse` | Reizdruck wird Entry-Anker |
| `hypothesis` | Gedanke wird mit Realität vermischt |
| `entry` | Handlung liegt zu früh in Core-Schichten |

## Aktueller Hotspot-Befund

Gezählt wurden Treffer in `core`, `trading`, `bot_gates` und `bot_engine`.
Die Zahlen sind nur technische Hinweise, keine Qualitätsbewertung.

| Datei | Risiko-Befund | Einschätzung |
| --- | --- | --- |
| `core/decision_regulation.py` | sehr viele `action_`, `hypothesis`, `permission`, `block` | größter Entflechtungsbereich |
| `trading/trade_stats.py` | viele alte Strategie-/Action-/Hypothesenfelder | Debug/Stats trägt alte Sprache weiter |
| `bot_gates/entry_decision.py` | `strategy_*`, `motor_*`, `permission`, `impulse`, `entry` | Entry-Brücke vermischt Zustimmung, Thought und Ordernähe |
| `core/runtime_entry.py` | Entry-Orchestrierung mit Hypothese, Kontakt und alten Fallbacks | Übergabeschicht muss sauber bleiben |
| `trading/trade_plan.py` | Entry-Geometrie plus Hypothesen-/Impuls-Modulation | Handlungsadapter ist noch zu kognitiv |
| `bot_engine/entry_attempt_context.py` | alte Strategie-/Motorikfelder im Kontext | Übergabekompatibilität prüfen |
| `core/review_feedback.py` | Hypothesenvertrauen | fachlich wertvoll, aber Thought/Memory sauber trennen |
| `core/hypothesis_learning.py` | Hypothesenlernen | fachlich wertvoll, darf nicht direkt Handlung treiben |
| `core/strategic_window.py` | alter Name, Bereichswahrnehmung eigentlich wertvoll | umbenennen oder strikt als Wahrnehmungsfenster behandeln |

## Funktionale Einordnung

### Behalten

Diese Bereiche passen grundsätzlich zum Bauplan:

- `core/visual_perception.py` als Sinneswahrnehmung
- `core/perception.py` als Wahrnehmungsverdichtung
- `core/temporal_perception.py` als Zeit-/Nachhall-Wahrnehmung
- `core/mcm_field.py` als Feld / Neuronensystem
- `core/neurochemistry.py` als Modulation
- `core/felt_state.py` als gefühlte Lage
- `core/form_language.py` als Formsprache
- `core/form_symbol_orchestration.py` als Form-/Syntax-Orchestrierung
- `core/thought_memory.py` als Thought-Memory
- `core/runtime.py` und `core/runtime_bridge.py` als technische Runtime

### Behalten, aber begrenzen

- `core/hypothesis_learning.py` bleibt Thought-Lernen.
- `core/review_feedback.py` bleibt Beobachtungs-/Hypothesenbewertung.
- `core/possibility_field.py` bleibt Variantenraum.
- `core/strategic_window.py` bleibt nur als Bereichs-/Rückblickwahrnehmung.

Diese Bereiche dürfen keine direkte Entry-Motorik erzeugen.

### Entflechten

- `core/decision_regulation.py`
- `core/runtime_entry.py`
- `bot_gates/entry_decision.py`
- `trading/trade_plan.py`
- `trading/trade_stats.py`

Hier sitzt aktuell die Gefahr, dass DIO wieder mechanisch wird:

```text
Hypothese -> Permission -> Entry
Reizdruck -> Impuls -> Entry
Vorsicht -> Block
Kontakt -> Motorik
```

Der Bauplan verlangt stattdessen:

```text
Hypothese -> Realitätsprüfung -> Reife / Abstand / Nähe
Reizdruck -> Wahrnehmungsdruck -> Feldwirkung / Fokus
Vorsicht -> Regulation / Distanz
Kontakt -> tragende Nähe -> Handlungsadapter
```

## Erster Rückbau-Fokus

### 1. `core/decision_regulation.py`

Aktuelle Rolle:

- Innenlage
- offene Hypothesen
- Reife
- Vorsicht
- Handlungsspannung
- Block-/Gate-Übergänge
- Trust-Return
- Thought-Last

Zielrolle:

```text
Regulation erzeugt keine Freigabe.
Regulation beschreibt Umgang mit Innenlage.
```

Rückbau:

- `open_hypothesis_action_permission` vollständig als Alt-Alias behandeln.
- `open_hypothesis_reality_permission` fachlich umbenennen zu
  `open_hypothesis_reality_fit` oder `open_hypothesis_reality_bearing`.
- `open_hypothesis_motor_tension` fachlich trennen:
  `thought_action_tension` oder `hypothesis_contact_tension`.
- `allow_block` nicht mehr als fachliches Ergebnis führen.
- `*_block`-Gründe zu Distanz-/Beobachtungs-/Reorganisationszuständen
  übersetzen.

### 2. `bot_gates/entry_decision.py`

Aktuelle Rolle:

- wertet innere Zustimmung
- prüft Entry-Geometrie
- schreibt Debug
- führt alte `strategy_*`-Kompatibilität
- kann innere Ablehnung in Nicht-Handlung übersetzen

Zielrolle:

```text
Entry-Brücke liest tragende Nähe.
Value-Gate prüft Order-Geometrie.
Innere Zustände modulieren, aber sperren nicht hart.
```

Rückbau:

- Begriff `gate` fachlich nur für Value-Gate.
- `inner_action_consent` in `inner_contact_consent` oder
  `bearing_to_action` überführen.
- `strategy_*` nur noch als Ausgabe-Fallback, später entfernen.
- `impulse_only` bleibt Nicht-Handlung / Beobachtung, nicht Entry-Pfad.

### 3. `trading/trade_plan.py`

Aktuelle Rolle:

- berechnet Entry, SL, TP, RR
- liest Bereichskontakt
- liest Hypothesenlage
- hält Impuls- und Kontaktpreise als Übergang

Zielrolle:

```text
Trade-Plan ist Handlungsadapter.
Er denkt nicht.
Er übersetzt tragende Nähe in Order-Geometrie.
```

Rückbau:

- Hypothesen-Modulation aus Preisbildung entfernen oder vorgelagert als
  Realitätsprüfung liefern.
- Impuls nur noch als Wahrnehmungsdruck protokollieren.
- Entry-Preis aus Bereichs-/Kontakt-/MCM-Nähe bilden.
- Falls keine tragende Nähe vorhanden ist: kein Plan, aber Beobachtung kann
  gespeichert werden.

### 4. `trading/trade_stats.py`

Aktuelle Rolle:

- Stats
- Debug
- GUI-Daten
- alte Kompatibilitätsfelder
- teilweise Lern-/Beobachtungsspur

Zielrolle:

```text
Stats beobachtet nur.
Stats steuert nicht.
Stats trennt GUI, Outcome, Thought, Feld und Entry.
```

Rückbau:

- alte `strategy_*`-Felder nicht weiter als führende Debugsprache nutzen.
- GUI-relevante PnL/Equity getrennt halten.
- Thought-Landkarte und Feldtopologie getrennt schreiben.
- keine doppelten Deutungen in einer Zeile erzwingen.

## Konkrete nächste technische Reihenfolge

1. `core/decision_regulation.py` Rückgabe-Felder entschärfen:
   `permission`, `block`, `motor` nur noch Alias oder umbenannt.
2. `bot_gates/entry_decision.py` auf neue Namen umstellen.
3. `trading/trade_plan.py` als reinen Handlungsadapter begrenzen.
4. `trading/trade_stats.py` Debug in Beobachtungsschichten trennen.
5. Erst danach wieder Laufvergleich gegen alte Referenz.

## Umgesetzter erster Code-Schritt

Datei:

- `core/decision_regulation.py`

Änderung:

- `open_hypothesis_reality_bearing` ergänzt.
- `open_hypothesis_reality_fit` ergänzt.
- `open_hypothesis_action_tension` ergänzt.
- `inner_distance_state` ergänzt.
- `former_block_reason` ergänzt.

Die alten Felder bleiben als technische Kompatibilität erhalten:

- `open_hypothesis_reality_permission`
- `open_hypothesis_action_permission`
- `open_hypothesis_motor_tension`
- `allow_block`

Fachliche Bedeutung:

```text
permission -> Reality-Bearing / Reality-Fit
motor_tension -> Action-Tension
block -> Distanz-/Hold-/Beobachtungszustand
```

Das ist noch keine vollständige Entflechtung. Es ist der erste sichere
Adapter-Schritt, damit nachgelagerte Dateien auf neue Namen umgestellt werden
können, ohne bestehende Übergaben sofort zu brechen.

Prüfung:

```text
python -m py_compile core/decision_regulation.py
```

erfolgreich.

## Umgesetzter zweiter Code-Schritt

Datei:

- `bot_gates/entry_decision.py`

Änderung:

- Entry-Brücke liest `open_hypothesis_reality_bearing` bevorzugt.
- Danach folgt `open_hypothesis_reality_fit`.
- Alte Felder bleiben Fallback:
  `open_hypothesis_reality_permission`,
  `open_hypothesis_action_permission`.
- Consent-Trace und Entry-Result schreiben die neuen Felder mit.

Fachliche Bedeutung:

```text
Die Brücke liest Hypothesenreife als Realitätsbezug,
nicht als innere Handlungserlaubnis.
```

Prüfung:

```text
python -m py_compile bot_gates/entry_decision.py
python -m py_compile core/decision_regulation.py bot_gates/entry_decision.py
```

erfolgreich.

## Umgesetzter dritter Code-Schritt

Datei:

- `trading/trade_plan.py`

Änderung:

- Hypothesen-Beobachtungsdruck verändert die Order-Geometrie nicht mehr
  direkt.
- Impulsdruck verändert die Kontakt-Bereitschaft nicht mehr direkt.
- `entry_contact_pressure` bleibt als Diagnosewert erhalten.
- `impulse_perception_pressure` bleibt als Wahrnehmungsdruck erhalten.
- Neue Rückgabefelder:
  - `open_hypothesis_reality_bearing`
  - `open_hypothesis_reality_fit`
  - `order_geometry_source = area_contact_adapter`
  - `impulse_role = perception_pressure_only`

Fachliche Bedeutung:

```text
Der Trade-Plan denkt nicht.
Der Trade-Plan baut nur Order-Geometrie aus tragender Kontakt-/Bereichsnähe.
Hypothese und Impuls bleiben Kontext, nicht Entry-Anker.
```

Prüfung:

```text
python -m py_compile trading/trade_plan.py core/decision_regulation.py bot_gates/entry_decision.py
```

erfolgreich.

## Umgesetzter vierter Code-Schritt

Dateien:

- `core/runtime_entry.py`
- `bot_gates/entry_decision.py`
- `trading/trade_stats.py`

Änderung:

- `order_geometry_source` und `impulse_role` werden durch Runtime, Entry-Brücke
  und Stats weitergereicht.
- `open_hypothesis_reality_bearing` und `open_hypothesis_reality_fit` werden
  in Runtime-/Stats-Kontexten sichtbar.

Fachliche Bedeutung:

```text
Im Debug kann geprüft werden:
Kommt die Order-Geometrie aus Kontaktadapter?
Bleibt Impuls nur Wahrnehmungsdruck?
Wird Hypothese als Realitätsbezug statt Handlungserlaubnis geführt?
```

Prüfung:

```text
python -m py_compile trading/trade_stats.py core/runtime_entry.py bot_gates/entry_decision.py trading/trade_plan.py core/decision_regulation.py
```

erfolgreich.

## Umgesetzter fünfter Code-Schritt

Dateien:

- `trading/trade_plan.py`
- `core/possibility_field.py`
- `core/decision_regulation.py`

Änderung:

- Alte Entry-Druckfelder aus dem Trade-Plan werden neutral gehalten.
- `entry_contact_pressure`, `entry_choice_pressure` und
  `entry_choice_conflict` sind keine heimlichen Motorikwerte mehr.
- Der Möglichkeitspfad schreibt primär `open_hypothesis_reality_bearing` und
  `open_hypothesis_reality_fit`.
- Die Regulation liest offene Hypothesen primär als Realitätsbezug und
  Handlungsspannung, nicht als Erlaubnis oder Motorik.

Fachliche Bedeutung:

```text
Eine Hypothese darf sagen: Das könnte zur Realität passen.
Sie darf nicht sagen: Handle deshalb automatisch.

Ein Impuls darf sagen: Hier ist Reizdruck.
Er darf nicht sagen: Setze hier den Entry.
```

Prüfung:

```text
python -m py_compile core/decision_regulation.py core/possibility_field.py trading/trade_plan.py core/runtime_entry.py bot_gates/entry_decision.py trading/trade_stats.py
```

erfolgreich.

## Prüfsatz

Ein Lauf ist erst wieder sinnvoll, wenn im Code gilt:

```text
Core sieht und fühlt.
Thought denkt.
Regulation ordnet Innenlage.
Trade-Plan baut nur die Order-Geometrie.
Value-Gate prüft nur ökonomische Gültigkeit.
```
