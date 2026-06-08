# 27 Code-Abgleich Gefühlswahrnehmung

## Zweck

Diese Datei hält den ersten Abgleich zwischen aktuellem Code und der neuen
DIO-Ausrichtung fest.

Leitlinie:

```text
MCM ist Gefühlswahrnehmung.
Hypothese ist Wahrnehmung des eigenen Denkens.
Strategie darf nur als freie tragende Reaktion entstehen.
Hart bleibt nur das Value-Gate.
```

## Sauber

### Value-Gate

`bot_gates/trade_value_gate.py` ist fachlich nah an der neuen Richtung.

Es prüft nur:

- gültige LONG/SHORT-Richtung
- Entry, SL, TP vorhanden
- Preisgeometrie
- Risiko
- Mindest-TP-Abstand
- Mindest-RR

Das ist die einzige harte Prüfung, die im Bauplan bleiben darf.

### Core-Kernspur

`bot_engine/mcm_core_engine.py` trennt bereits:

- reine Kernspur: Energie, Kohärenz, Asymmetrie, Zone
- abgeleitete Deutung: Stabilität, wahrgenommener Druck

Das passt zur Richtung, Core-Daten nicht direkt als Tradinglogik zu behandeln.

## Kritisch

### Inneres Nein wird aktuell nicht wirksam genug

In `bot_gates/entry_decision.py` erkennt `_resolve_inner_action_consent()`
mehrere innere Nicht-Handlungszustände:

- `impulse_needs_inner_processing`
- `inner_state_declines_motor_action`
- `open_hypothesis_needs_reality_contact`
- `ordinary_structure_needs_bearing`
- `inner_state_needs_positive_confirmation`

Diese Zustände setzen `would_have_declined=True`, geben aber trotzdem
`allowed=True` zurück.

Der spätere Pfad führt die Umwandlung in Nicht-Handlung nur aus, wenn
`allowed=False` ist.

Folge:

```text
DIO spürt inneres Nein.
Das Nein wird gespeichert/protokolliert.
Die reale Handlung kann trotzdem weiterlaufen.
```

Das widerspricht der neuen Zielrichtung. DIOs Gefühlswahrnehmung muss nicht
hart blockieren, aber sie muss eine reale Nicht-Handlung, Beobachtung oder
Reifung auslösen können.

### Hypothese wirkt noch zu handlungsnah

In mehreren Pfaden wirken Hypothesen noch direkt auf Handlungsnähe:

- `open_hypothesis_action_permission`
- `hypothesis_action_support`
- `dominant_hypothesis_action_readiness`
- `strategy_confirmation`
- `strategy_trust_bearing`
- `strategy_context_bearing`

Fachlich sollte das umbenannt und neu verdrahtet werden:

```text
Hypothese -> Denk-Wahrnehmung
Denk-Wahrnehmung -> Realität prüfen
Bestätigte reale Konsequenz -> Vertrauen/Reife
Vertrauen/Reife -> Handlung darf näherkommen
```

Nicht:

```text
Hypothese -> Action Support
```

### Strategie-Begriffe sind noch zu stark im Code

Der aktuelle Code verwendet noch viele `strategy_*`-Felder.

Teilweise meinen sie eigentlich:

- bestätigte Hypothesenfolge
- tragende Form-/MCM-Erfahrung
- Kontext-Passung
- innere Handlungsnähe

Diese Begriffe sollten im Bauplan ersetzt werden, damit Strategie nicht
als eingebaute Vorgabe wirkt.

### Strategic Window ist noch handlungsnah

`core/strategic_window.py` beschreibt sich zwar als Wahrnehmungsbrücke, bildet
aber bereits Werte wie:

- `area_order_intention`
- `area_action_timing_fit`
- `area_future_to_present_readiness`

Das ist nicht zwingend falsch, aber zu nah an Handlung.

Im neuen Aufbau sollte diese Schicht neutraler werden:

```text
Bereichswahrnehmung
Bereichsgefühl
Kontaktqualität
Zeitnähe
Nachhall
```

Die Handlung darf erst später entstehen.

## Nächster technischer Schritt

Zuerst den inneren Consent-Pfad korrigieren:

```text
would_have_declined=True
-> reale Nicht-Handlung / observe / replan / hold
-> keine Order
-> Hypothese und Gefühlslage als Erfahrung weiterführen
```

Das ist keine harte Sperre. Es ist die Umsetzung von:

```text
Ich spüre, dass diese Handlung innerlich nicht trägt.
Ich handle nicht blind.
Ich beobachte, reife oder prüfe weiter.
```

Danach sollten die `strategy_*`-Felder in DIO-Begriffe überführt werden.

## Umsetzung Schritt 1

`bot_gates/entry_decision.py` wurde korrigiert.

Alle inneren Nicht-Handlungszustände geben jetzt `allowed=False` zurück:

- `impulse_needs_inner_processing`
- `inner_state_declines_motor_action`
- `open_hypothesis_needs_reality_contact`
- `ordinary_structure_needs_bearing`
- `inner_state_needs_positive_confirmation`

Dadurch greift der vorhandene Pfad `_as_inner_non_action()`.

Fachliche Wirkung:

```text
DIO spürt ein inneres Nein.
DIO setzt keine reale Order.
DIO führt die Lage als observe/replan/hold weiter.
Die Richtung, der Grund und die Hypothesenlage bleiben als Lernspur erhalten.
```

Das ist keine zusätzliche harte Sperre. Es ist die Kopplung von
Gefühlswahrnehmung an reale Handlung.

## Umsetzung Schritt 2

Die alten `strategy_*`-Felder werden nicht mehr als Zielbegriff für DIO
weitergeführt.

Technisch bleiben sie vorerst als Kompatibilitätsfelder erhalten, damit Debug,
Stats und bestehende Speicherpfade nicht brechen. Parallel dazu werden neue
semantische Felder durchgereicht:

- `thought_confirmation_bearing`
- `thought_rejection_pressure`
- `thought_trust_bearing`
- `contact_context_bearing`
- `raw_thought_contradiction_pressure`
- `thought_contradiction_pressure`

Fachliche Bedeutung:

```text
DIO hat keine fest eingebaute Strategie.
DIO hat Denkbestätigung, Denkdruck, Vertrauensbildung und Kontakttragfähigkeit.
Eine Strategie darf später nur als wiederkehrend tragende Reaktion entstehen.
```

Geänderte Codebereiche:

- `bot_gates/entry_decision.py`
- `bot_engine/entry_attempt_context.py`
- `trading/trade_stats.py`

Prüfung:

```text
python -m py_compile bot_gates\entry_decision.py bot_engine\entry_attempt_context.py trading\trade_stats.py
```

Ergebnis: Syntaxprüfung erfolgreich.

## Umsetzung Schritt 3

Hypothesen wurden im Entry-Consent weiter von direkter Motorik gelöst.

Vorher wirkten mehrere Hypothesenfelder doppelt:

```text
Hypothese bestätigt sich etwas
-> erhöht Denkvertrauen
-> erhöht zusätzlich direkt Handlungsunterstützung
```

Das war zu nah an starrer Strategie.

Jetzt werden zusätzliche DIO-Begriffe geführt:

- `open_hypothesis_reality_permission`
- `possibility_contact_bearing`
- `dominant_hypothesis_reality_bearing`
- `current_hypothesis_reality_bearing`

Diese Werte dürfen weiter zur inneren Nähe beitragen, aber nur reduziert und
nicht als dominanter Motor. Die stärkere Wirkung läuft über:

```text
Denkbestätigung
Vertrauen
Kontakttragfähigkeit
Realitätsbindung
```

Fachlich:

```text
Eine Hypothese ist kein Entry-Befehl.
Eine Hypothese ist eine innere Deutung, die Kontakt zur Realität braucht.
Wenn sie wiederholt trägt, kann daraus später Handlungsnähe entstehen.
```

Prüfung:

```text
python -m py_compile bot_gates\entry_decision.py bot_engine\entry_attempt_context.py trading\trade_stats.py
```

Ergebnis: Syntaxprüfung erfolgreich.

## Umsetzung Schritt 4

`core/strategic_window.py` wurde semantisch neutralisiert.

Die alten handlungsnahen Felder bleiben als Kompatibilitätsausgabe erhalten,
bekommen aber Wahrnehmungsnamen:

- `area_order_intention` bleibt alt, neu dazu: `area_contact_pull`
- `area_action_timing_fit` bleibt alt, neu dazu: `area_contact_timing_fit`
- `area_future_to_present_readiness` bleibt alt, neu dazu:
  `area_future_present_coherence`

`trading/trade_plan.py` liest zuerst die neuen Wahrnehmungsnamen und fällt nur
bei Bedarf auf die alten Namen zurück.

Fachlich:

```text
Das Rückblickfenster erzeugt keine Strategie.
Es beschreibt Bereichskontakt, zeitliche Nähe und tragende Wahrnehmung.
Erst spätere Schichten dürfen daraus Handlungsnähe ableiten.
```

Prüfung:

```text
python -m py_compile core\strategic_window.py trading\trade_plan.py bot_gates\entry_decision.py bot_engine\entry_attempt_context.py trading\trade_stats.py
```

Ergebnis: Syntaxprüfung erfolgreich.

## Prüfpunkte im nächsten Lauf

- sinkt Übertrading deutlich?
- steigen observe/replan/withheld organisch?
- bleiben `inner_action_consent_state` und `inner_action_would_have_declined`
  in Stats/Debug sichtbar?
- werden abgelehnte Hypothesen später als `saved_loss`, `missed_gain` oder
  neutral ausgewertet?
- bleibt DIO handlungsfähig, wenn die innere Lage wirklich trägt?
