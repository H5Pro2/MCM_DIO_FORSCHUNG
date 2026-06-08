# ENTMECHANISIERUNG_ABGLEICH

Ziel:
Konkreter Ist-Abgleich zum Rueckbauplan. Diese Datei listet die Stellen, an
denen der aktuelle Code eher mechanisch wirkt, und ordnet sie nach
Rueckbauprioritaet.

Referenz:
`docs/07_konstruktion/ENTMECHANISIERUNG_PLAN.md`

---

# 1. Kurzbefund

Der aktuelle Funktionssplit ist strukturell brauchbar, aber einige Pfade sind
zu stark vorgedeutet:

- Die Core-/Perception-Schicht erzeugt bereits viele Druck-, Qualitaets-,
  Risiko- und Labelwerte.
- Das Entry-Gate arbeitet mit expliziten `allowed`, `reject`, `decline`,
  `allow_plan`, `decision_tendency` und `reason`-Ketten.
- Der Trade-Planer bildet weiterhin eine fertige Entry-These ueber gewichtete
  Bedingungen.
- Observation-Learning speichert korrekt realitaetsgetrennt, bekommt aber noch
  zu oft Restzustaende wie `no_mature_entry_thesis`.

Die Hauptgefahr:
DIO sieht nicht nur eine energetische Spur, sondern bekommt bereits
vorgedeutete Bedeutung. Dadurch entsteht indirekte Wenn-Dann-Logik.

---

# 2. Core- und Wahrnehmungsschichten

## 2.1 `bot_engine/mcm_core_engine.py`

Status:
Strukturell bereinigt. Die Datei wurde auf den energetischen Kern reduziert.
Sie enthaelt jetzt:

- OHLCV-Hilfsfunktionen.
- `compute_tension_from_ohlc()`.
- `build_tension_state_from_window()`.
- `core_trace_state`.
- `core_interpretation_state`.
- Kompatibilitaets-Export fuer `build_visual_market_state`.

Ausgelagert:

- `core/visual_perception.py`: visuelle Formspur, Formachsen,
  `visual_form_id`, Visual-Kompatibilitaetswerte.
- `core/sensory_reality.py`: Reizlast, Habituation, sensory gate und
  sensory reality label.

Der Core liefert weiterhin getrennte Zustandsraeume:

- `core_trace_state`: reine energetische Kernspur aus OHLCV.
- `core_interpretation_state`: abgeleitete Druck-/Stabilitaetsdeutung.
- `core_visual_trace_state`: sichtbare Formspur ohne direkte Handlungsaussage.
- `core_visual_interpretation_state`: kompatible Altdeutung fuer bestehende Module.

Die alten Visual-Top-Level-Felder bleiben im Visual-Modul vorerst erhalten,
damit nachgelagerte Module nicht brechen. Der naechste Rueckbauschritt ist,
Perception und Gates schrittweise auf die Trace-Zustaende zu fuehren und
direkte Deutungswerte nur noch als Feldreizung oder Diagnose zu behandeln.

Positiv:

- `compute_tension_from_ohlc()` liefert bereits den gewuenschten Kern:
  - `energy`
  - `coherence`
  - `asymmetry`
  - `coh_zone`

Restproblem:

- `core/visual_perception.py` fuehrt weiterhin viele Zusatzdeutungen:
  - `short_impulse`
  - `mid_impulse`
  - `body_pressure`
  - `wick_pressure`
  - `breakout_tension`
  - `visual_form_pressure`
  - `visual_shape_resonance`
  - `visual_shape_fragility`
  - `sensory_reality_pressure`
  - `sensory_load`
  - `sensory_gate`
  - `sensory_reality_label`

Rueckbauziel:

- Core darf OHLCV in energetische Spur uebersetzen.
- Visual-/Sensory-Labels duerfen nicht als fertige Bedeutung in Gates wirken.
- Sekundaere Werte entweder entfernen oder als rein interne MCM-Reizung
  markieren.

Prioritaet:
Hoch.

## 2.2 `bot_engine/strukture_engine.py`

Status:
Fachlich weicher als andere Stellen, aber zu nah an fertiger Strukturwertung.

Werte:

- `structure_quality`
- `context_confidence`
- `stress_relief_potential`
- `zone_proximity`

Risiko:
Diese Werte koennen als direkte Entry-Nahe gelesen werden. Das widerspricht
dem Ziel, dass DIO selbst Form/MCM-Wiederkehr bildet.

Rueckbauziel:

- Swing-/Zone-Erkennung darf als sensorische Formnaehe bleiben.
- `structure_quality`, `context_confidence`, `stress_relief_potential` sollten
  nicht direkt Gate-Entscheidungen treiben.
- Besser: als leichte Feldstimulation an MCM/Formbildung weitergeben.

Prioritaet:
Mittel bis hoch.

## 2.3 `core/perception.py`

Status:
Stark ueberladen, aber erster Rueckbauschritt umgesetzt.

Aktuell geaendert:

- `build_outer_visual_perception_state()` liest zuerst
  `core_visual_trace_state` und erst danach kompatible Altwerte.
- `build_perception_state()` liest zuerst `core_trace_state` und
  `core_visual_trace_state`.
- Abgeleitete Visual-/Sensory-Werte bleiben ueber
  `core_visual_interpretation_state` verfuegbar, sind aber strukturell als
  Interpretation getrennt.
- Die Trace-Zustaende werden in den Perception-Outputs mitgefuehrt.
- `uncertainty_score`, `novelty_score`, `signal_quality` und
  `observe_priority` sind intern in zwei Gruppen zerlegt:
  - `perception_trace_metrics`: reine Spurwerte wie Mismatch, Bewegung,
    Support und Strain.
  - `perception_interpretation_metrics`: kompatible Restdeutung aus
    Visual-/Sensory-Werten.
  Die alten Output-Namen bleiben erhalten, damit Regulation und Felt-State
  nicht brechen.

Problematische Verdichtung:

- `uncertainty_score`
- `novelty_score`
- `signal_quality`
- `observe_priority`
- `visual_form_pressure`
- `sensory_reality_pressure`
- `field_perception_pressure`
- viele bewusste Labels:
  - `overcoupled_field`
  - `reflective_check`
  - `release_ready`
  - `object_contact`
  - `world_shift_contact`

Risiko:
Die Wahrnehmung wird bereits psychologisch und handlungsnah etikettiert. Das
ist als Diagnose lesbar, wirkt aber schnell wie ein innerer Zustandsautomat.

Rueckbauziel:

- Bewusste Labels nicht als Gate-Bedingung verwenden.
- Druck-/Qualitaetswerte auf wenige Rezeptorfamilien reduzieren.
- Wahrnehmung soll Feldlage beschreiben, nicht Handlung vorbereiten.
- Als naechstes pruefen, welche downstream Module noch die alten Score-Namen
  als harte Handlungsnaehe lesen. Dort muessen sie schrittweise als
  Wahrnehmungslage statt als Entscheidungsvorbereitung behandelt werden.

Prioritaet:
Sehr hoch.

## 2.4 `core/temporal_perception.py`

Status:
Konzeptionell wichtig, aber zu viele direkte Modulatoren.

Werte:

- `transition_pressure`
- `continuation_readiness`
- `temporal_exhaustion`
- `spacetime_regulation_state`
- `conviction_boost`
- `observe_pull`
- `replan_pull`

Risiko:
Zeitwahrnehmung wird nicht nur Tiefe, sondern direkte Steuerkraft.

Rueckbauziel:

- Zeitachse als Tiefen-/Nachhall-/Vorhall-Wahrnehmung erhalten.
- Direkte `act/observe/replan`-Modulation entschärfen.
- Keine harte Uebersetzung aus Zeitwerten in Handlung.

Prioritaet:
Mittel.

## 2.5 `core/strategic_window.py`

Status:
Mechanisch kritisch.

Werte:

- `area_bearing_quality`
- `area_invalidity_pressure`
- `strategic_pressure_interpretation`
- `area_action_timing_fit`
- `strategic_window_state`

Risiko:
Diese Schicht kann aus "ich sehe Bereich" zu schnell "dort ist Entry" machen.

Rueckbauziel:

- Bereichswahrnehmung darf bleiben.
- Bereich darf MCM-Feld und Formgedaechtnis reizen.
- Bereich darf nicht selbst strategische Handlung erzeugen.

Prioritaet:
Sehr hoch.

---

# 3. Gate- und Handlungslogik

## 3.1 `bot_gates/entry_decision.py`

Status:
Hauptstelle fuer mechanisches Verhalten, erster Gate-Rueckbau umgesetzt.

Mechanische Elemente:

- `allowed`
- `inner_action_declined`
- `inner_state_declines_motor_action`
- `open_hypothesis_needs_reality_contact`
- `runtime_allow_plan_false`
- `decision_plan_missing`
- `signature_block`
- `context_cluster_block`
- `impulse_only`

Beispielhafte harte Muster:

- `if decision_tendency != "act": ...`
- `if not consent_state["allowed"]: ...`
- `if impulse_only: allowed = False`
- `if explicit_allow_plan is False: ...`

Sicherheitsinvarianten, die bleiben duerfen:

- kein Trade ohne valide `entry_price`, `sl_price`, `tp_price`
- kein Trade bei ungueltiger Risk-Geometrie
- kein Trade ohne reale Orderfaehigkeit im Livebetrieb

Aktuell geaendert:

- `_resolve_inner_action_consent()` blockiert nicht mehr hart.
- Innere Zustandskonflikte liefern weiter Diagnose:
  - `inner_action_consent`
  - `inner_action_support`
  - `inner_action_no`
  - `strategy_confirmation`
  - `strategy_rejection`
  - `inner_action_would_have_declined`
  - `non_economic_gate_policy = field_modulation_only`
- `runtime_allow_plan_false` wird nicht mehr als harter Non-Action-Return
  behandelt, sondern als Meta-Diagnose weitergegeben.

Damit bleibt die Value-/Geometriepruefung hart, aber innere Regulation wird
nicht mehr als Gate verwendet.

## 3.2 `core/decision_regulation.py`

Architekturregel umgesetzt:

- Innere Zustaende duerfen kein hartes Gate sein.
- Das einzige echte Gate bleibt das oekonomische Value-Gate:
  valide Preis-/Risiko-/Order-Geometrie.
- `_build_pre_action_decision_state()` fuehrt alte innere Block-Pfade jetzt
  auf Feldmodulation zurueck:
  - `allow_block` wird fuer innere Zustaende auf `False` gesetzt.
  - `former_allow_block` bleibt als Diagnose sichtbar.
  - `non_economic_gate_policy = field_modulation_only`.
  - `*_block`-Gruende werden als `*_hold` lesbar, sofern sie aus innerer
    Regulation stammen.

Damit bleiben Ueberlastung, Reife, Unsicherheit, Druck und Vorsicht im System
wirksam, aber nicht als harte Handlungssperre.

Alles andere ist zu pruefen:

- Innere Zustimmung soll Feldtendenz sein, nicht Freigabeschalter.
- Hypothesenreife soll Vertrauen/Vorsicht modulieren, nicht direkt sperren.
- `decision_tendency` soll Ergebnis der Feldlage sein, nicht Gate-Vorstufe.

Prioritaet:
Sehr hoch.

## 3.2 `core/runtime_tendency.py`

Status:
Zu stark als Uebersetzungsbruecke in konkrete Tendenzen.

Risiko:
`allow_plan`, `decision_tendency`, `signature_block` und
`context_cluster_block` werden als fertige Steuerwerte transportiert.

Rueckbauziel:

- Diese Werte entweder als Diagnose behalten oder in weiche Meta-Achsen
  uebersetzen.
- Keine direkte act/hold/replan-Entscheidung aus einzelnen Flags.

Prioritaet:
Hoch.

## 3.3 `core/runtime_entry.py`

Status:
Orchestrierung ist noetig, aber Review-/Strategie-Anwendungen setzen
teilweise direkt `allow_plan = False`, `pre_action_phase = replan/observe`.

Kritische Stellen:

- `apply_review_feedback_to_meta()`
- `apply_strategic_window_to_meta()`
- `apply_active_mcm_contact_to_meta()`
- `build_runtime_no_plan_result()`
- `synchronize_entry_choice_prices()`

Rueckbauziel:

- Keine direkte harte Ueberschreibung von `allow_plan`, ausser Sicherheit.
- Review/Strategie/Kontakt sollen Feldachsen modulieren.
- `no_plan` soll nicht zum dominanten Restzustand werden.

Prioritaet:
Hoch.

## 3.4 `trading/trade_plan.py`

Status:
Funktional wichtig, aber aktuell zu mechanisch.

Problem:
`thesis_ready` wird ueber explizite Bedingungen gebildet:

- `strategic_anchor > 0`
- `side_fit > ...`
- `strategic_entry_fit > ...`
- `area_motor_intention > ...`
- `entry_choice_state in (...)`

Das ist verstaendlich, aber wirkt wie ein klassischer Strategiefilter.

Rueckbauziel:

- Trade-Planer soll nur Geometrie erzeugen, wenn DIO bereits eine organische
  Handlungsnaehe traegt.
- Der Planer soll keine Reife entscheiden.
- Entry-Naehe soll aus MCM-Feld-/Form-/Thought-Lage kommen, nicht aus
  Trade-Plan-Bedingungen.

Prioritaet:
Sehr hoch.

---

# 4. Speicher- und Lernpfade

## 4.1 `core/hypothesis_learning.py`

Status:
Nach letzter Korrektur besser.

Positiv:

- keine `thesis:*`-Familien als Realitaetsanker
- Hypothese wird als `thought_trace` an reale Form gebunden

Weiter pruefen:

- ob `no_mature_entry_thesis` zu oft als Restzustand gespeichert wird
- ob reale Formanker genug Wiederkehr bekommen
- ob `thought_trace_counts` spaeter sinnvoll auf Vertrauen/Vorsicht wirkt

Prioritaet:
Mittel.

## 4.2 `trading/trade_stats.py`

Status:
Funktional, aber Debug-/Learning-Bruecke kann falsche Restzustaende erzeugen.

Risiko:
Wenn Entry-Metadaten fehlen, wird eine Beobachtung zwar nicht mehr als
`impulse_contact`, aber weiterhin als `no_mature_entry_thesis` gespeichert.
Das ist korrekt als Fallback, darf aber nicht dominieren, wenn Entry-Bridge
eigentlich `hypothesis_area_entry` gesehen hat.

Rueckbauziel:

- Beobachtete These muss aus der realen Entscheidungsspur kommen.
- Fallback nur verwenden, wenn wirklich keine These gesehen wurde.
- Nicht jede Nicht-Handlung ist "keine reife These"; manchmal ist es eine
  gesehene These mit innerer Distanz.

Prioritaet:
Hoch.

---

# 5. Rueckbau-Reihenfolge

## Phase A: Keine Code-Feature-Erweiterung

Status:
Ab sofort keine neuen Organe, keine neuen Diagnosewerte, keine neuen Gates.

Ziel:
System stabilisieren und mechanische Stellen reduzieren.

## Phase B: Core-Basisspur festlegen

Konkreter Zielkern:

- `energy`
- `coherence`
- `asymmetry`
- `coh_zone` / `regime`
- optional: einfache Range-/Volatilitaetsnaehe

Alles andere wird markiert als:

- interne DIO-Deutung
- Debug
- Rueckbaukandidat

## Phase C: Gate-Rueckbau

Zuerst:

1. `bot_gates/entry_decision.py`
2. `trading/trade_plan.py`
3. `core/runtime_entry.py`
4. `core/runtime_tendency.py`

Regel:
Nur Sicherheitsinvarianten bleiben hart.

## Phase D: Perception entkoppeln

Zuerst:

1. `core/perception.py`
2. `core/strategic_window.py`
3. `bot_engine/mcm_core_engine.py`
4. `bot_engine/strukture_engine.py`

Regel:
Perception beschreibt Reiz/Feld, nicht Handlung.

---

# 6. Konkrete erste Umbaustelle

Empfohlener erster Code-Schritt:

`bot_gates/entry_decision.py`

Ziel:
`_resolve_inner_action_consent()` darf nicht mehr als harte Freigabeinstanz
arbeiten, ausser bei Sicherheitsinvarianten.

Umbauidee:

- Ausgabe nicht mehr `allowed True/False` als primärer Sinn.
- Ausgabe stattdessen:
  - `motor_readiness`
  - `motor_resistance`
  - `reflection_pull`
  - `field_consent_tone`
  - `safety_block`
- Nur `safety_block` darf hart verhindern.
- Alles andere moduliert `decision_tendency`.

Erwarteter Effekt:
DIO wird weniger durch starre innere Zustimmung blockiert und mehr durch
Feldspannung/Tragfaehigkeit moduliert.

---

# 7. Kontrollfragen fuer jede Aenderung

Vor jedem Umbau pruefen:

1. Ist das eine echte Sicherheit oder ein verstecktes Tradingurteil?
2. Beschreibt der Wert Wahrnehmung oder entscheidet er schon?
3. Wird eine Hypothese als Gedanke oder als Realitaet behandelt?
4. Wird DIO handlungsnaeher durch Feldlage oder durch ein Label?
5. Gibt es dieselbe Druckwirkung bereits an anderer Stelle?

Wenn eine Stelle diese Fragen nicht sauber besteht, ist sie Rueckbaukandidat.

---

# 8. Umgesetzter Gate-Rueckbau

Aktueller Stand:

- Harte innere Gates wurden in den ersten relevanten Pfaden zurueckgebaut.
- `allow_block` wird bereits auf Diagnose-/Hold-Semantik reduziert.
- Nachgelagerte innere Plan-Sperren wurden in
  `non_economic_plan_modulation_reasons` ueberfuehrt.
- Review-/Pattern-Druck in `runtime_entry.py` darf den Plan nicht mehr hart
  ausschalten.
- Nicht-Handeln wird nicht mehr als technische Blockade beschrieben, sondern
  als organischer Zustand: `observe`, `replan`, `hold`, `inner_processing`.

Verbindliche Regel:

Das einzige echte Gate ist das oekonomische Value-/Ausfuehrungs-Gate:

- gueltige Richtung
- gueltige Entry-/SL-/TP-Geometrie
- gueltiges Risiko
- gueltige Order-/API-Ausfuehrung

Alle MCM-, neurochemischen, hypothetischen, visuellen, semantischen und
regulatorischen Signale sind keine Gates. Sie modulieren Feld, Reife,
Vorsicht, These, Fokus, Distanz und Handlungstendenz.

Offen:

- `signature_block`
- `context_cluster_block`

Diese Begriffe muessen im naechsten Schritt fachlich geprueft werden. Wenn sie
nur Diagnose sind, werden sie umbenannt. Wenn sie noch Verhalten hart sperren,
werden sie wie oben auf Feldmodulation zurueckgebaut.

## 8.1 Signatur-/Cluster-Erfahrung

Gepruefte Altlogik:

Im Kompatibilitaetskern wurde negative Erfahrung aus Signatur oder Kontext-
Cluster direkt in `decision = WAIT` umgeschrieben. Das war nicht organisch,
sondern eine versteckte starre Regel.

Rueckbau:

- Negative Signaturerfahrung bleibt erhalten, aber als
  `signature_caution_modulation`.
- Negative Clustererfahrung bleibt erhalten, aber als
  `context_cluster_caution_modulation`.
- Beide erhoehen Vorsicht und Memory-Inhibition.
- Beide duerfen die Entscheidung nicht allein auf `WAIT` setzen.

Fachliche Einordnung:

Erfahrung darf DIO nicht mechanisch stoppen. Erfahrung muss Feldspannung,
Vorsicht, Reife, Vertrauen und Distanz veraendern. Die Handlung entsteht aus
dem Gesamtzustand, nicht aus einem einzelnen Vergangenheitsurteil.

## 8.2 Attractor, Stress und Observation

Rueckbau:

- `defense_block` und `stressed_block` wurden entfernt.
- Attractor- oder Stresslage senkt Handlungsscores und erhoeht Vorsicht, aber
  deaktiviert Long/Short nicht hart.
- `observation_mode` ist kein Gate. Er moduliert die Bereitschaft und kann zu
  `WAIT` fuehren, wenn kein tragender Score entsteht.
- Konfigurationswerte fuer Long-/Short-Attractor wirken nur noch als
  Modulation, nicht als harte Richtungssperre.

Damit bleibt DIO organisch: innere Lage beeinflusst Handlung, aber ersetzt
nicht die Gesamtentscheidung.
