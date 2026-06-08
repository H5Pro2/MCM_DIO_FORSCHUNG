# AKTUELLER STAND

## Aktiver Bauplan

Die einzige aktive Bauanleitung für DIO liegt jetzt unter:

- `../../DIO_2/konstruktion/README.md`
- `../../DIO_2/konstruktion/00_BAUPLAN.md`
- `../../DIO_2/konstruktion/12_ARBEITSSPUR.md`
- `../../DIO_2/konstruktion/26_AUSRICHTUNG_GEFUEHLSWAHRNEHMUNG.md`
- `../../DIO_2/konstruktion/27_CODE_ABGLEICH_GEFUEHLSWAHRNEHMUNG.md`
- `../../DIO_2/konstruktion/28_UEBERTRAGUNGSMATRIX_CODE.md`

`docs` enthält dazu nur noch Begleitdokumente, Status und Verweise. Dort liegt
keine zweite Bauanleitung mehr.

Der alte `UMSETZUNGSPLAN.md`, die alte `FIX_LISTE.md` und das alte
`FIX_LISTE_ARCHIV.md` liegen jetzt unter `../99_temp_alt/` und bleiben nur als
historische Referenz erhalten. Neue Architektur wird dort nicht mehr erweitert.

## Aktive Zielordnung

`Welt -> Sehen -> MCM-Feld -> Memory -> Thought -> Realitätsprüfung -> Handlung -> Konsequenz`

Wichtig:

- DIO wird zuerst schriftlich als Schichtsystem aufgebaut.
- Hypothesen bleiben Gedanken, nicht Realität.
- Hypothesen sind Wahrnehmung des eigenen Denkens, keine Strategie.
- MCM-Feld wird als Gefühlswahrnehmung geführt.
- Strategie wird nicht erzwungen; sie darf nur als emergente, tragende
  Reaktion aus wiederkehrender Form, MCM-Wirkung, Erfahrung und Konsequenz
  entstehen.
- Entry-Anker sollen aus realer Form-, Bereichs- und MCM-Nähe entstehen.
- Innere Zustände modulieren Reife, Vorsicht, Fokus und Vertrauen.
- Harte innere Gates werden vermieden; hart bleibt nur die ökonomische Prüfung
  einer real ausführbaren Order.

## Letzter Code-Stand

Die Debug-Ausgabe wurde für normale Backtests verschlankt:

- `DEBUG_OUTPUT_PROFILE = "LEAN_BACKTEST"` ist Standard.
- GUI/KPI-relevante Daten bleiben aktiv.
- schwere Forschungsprotokolle laufen nur im Forschungsprofil.

Der Entry-Pfad wurde begonnen zurückzuführen:

- Hypothesen erhöhen keine Motorik/Entry-Reife mehr direkt.
- Hypothesen wirken nur noch als Deutung, Abstand oder Beobachtungsdruck.
- Code-Abgleich zeigt aber noch einen Bruch:
  `_resolve_inner_action_consent()` erkennt innere Nicht-Handlung als
  `would_have_declined=True`, gibt aktuell aber weiter `allowed=True` zurück.
  Dadurch kann DIOs innere Gefühlslage reale Handlung noch zu wenig in
  Beobachtung/Reifung umleiten.
- Dieser Bruch wurde im ersten Schritt korrigiert:
  innere Nicht-Handlungszustände geben jetzt `allowed=False` zurück und laufen
  über `_as_inner_non_action()` in observe/replan/hold statt in reale Order.
- Die alten `strategy_*`-Felder wurden im zweiten Schritt semantisch
  entkoppelt:
  sie bleiben als Kompatibilität erhalten, werden aber zusätzlich als
  `thought_confirmation_bearing`, `thought_rejection_pressure`,
  `thought_trust_bearing`, `contact_context_bearing` und
  `thought_contradiction_pressure` durchgereicht.
- Die Hypothesenwirkung im Entry-Consent wurde weiter entmotorisiert:
  Hypothesen liefern jetzt stärker Denkbestätigung, Realitätsbindung und
  Kontakttragfähigkeit und weniger direkte Handlungsunterstützung.
- Das Rückblickfenster wurde semantisch neutralisiert:
  `area_contact_pull`, `area_contact_timing_fit` und
  `area_future_present_coherence` werden als Wahrnehmungsfelder geführt; alte
  `area_order_intention`-/`area_action_timing_fit`-Felder bleiben nur für
  Kompatibilität erhalten.
- Eine Übertragungsmatrix wurde erstellt:
  bestehende Dateien sind den DIO-Schichten zugeordnet und je Bereich als
  behalten, umbauen oder später entfernen eingeordnet.
- `trading/trade_plan.py` wurde begonnen als Handlungsadapter zurückzuführen:
  neue Kontakt-/Realitätsfelder laufen parallel zu alten Kompatibilitätsfeldern,
  unter anderem `area_contact_weight`, `area_contact_fit`,
  `entry_contact_bearing`, `area_contact_readiness`,
  `impulse_perception_pressure` und `hypothesis_reality_bearing`.
- Nachgelagerte Pfade lesen diese Kontakt-/Realitätsfelder jetzt bevorzugt:
  `core/runtime_entry.py`, `bot_gates/entry_decision.py`,
  `trading/trade_stats.py` und `bot_engine/entry_attempt_context.py`.
- `possibility_field`, `review_feedback` und `decision_regulation` geben erste
  DIO-konforme Alias-Felder aus:
  `possibility_contact_bearing`, `open_hypothesis_reality_permission` und
  `dominant_hypothesis_reality_bearing`.
  Alte `action_*`-Namen bleiben vorerst als technische Kompatibilität erhalten.
- Im regulatorischen Pfad wird `open_hypothesis_reality_permission` jetzt
  bevorzugt gelesen; `open_hypothesis_action_permission` bleibt als alte Kopie.
- Im Entry-Adapter wurde die irreführende Restbenennung `impulse_preferred`
  entfernt. Schwacher Kontakt heißt dort jetzt `area_contact_weak`; die
  Synchronisierung spricht von `contact_context_integrated` oder
  `contact_context_unresolved`.
- `trading/trade_plan.py` arbeitet intern stärker mit Kontaktbegriffen:
  `contact_entry_price`, `contact_entry_weight`, `contact_entry_fit`,
  `area_contact_distance_fit` und `entry_contact_pressure`.
  Alte strategische/motorische Felder werden dort nur noch als
  Kompatibilitätsausgabe mitgeführt.
- Die Übergabepfade übernehmen diese neuen Kontaktfelder bevorzugt:
  `core/runtime_entry.py`, `bot_engine/entry_attempt_context.py`,
  `bot_gates/entry_decision.py` und `trading/trade_stats.py`.
- Ein Konsistenzfehler im Zustimmungs-/Regulationspfad wurde korrigiert:
  `bot_gates/entry_decision.py` nutzt für den inneren Zustimmungswert jetzt
  `contact_fit` statt des alten, nicht mehr geführten `strategic_fit`.
- Inferierte Beobachtungspläne in `trading/trade_stats.py` tragen jetzt auch
  die neuen Kontaktfelder (`contact_entry_mode`, `entry_contact_state`,
  `area_contact_focus_id`, `area_contact_location`).
- Der innere Zustimmungsregler in `bot_gates/entry_decision.py` bildet seine
  Werte intern jetzt als Gedanke-/Kontaktgrößen
  (`thought_confirmation_bearing`, `thought_rejection_pressure`,
  `thought_trust_bearing`, `contact_context_bearing`). Alte `strategy_*`-Felder
  bleiben nur als Kompatibilitätskopie.
- Die Entry-Bridge-Debugausgabe wurde auf die neue Fachsprache nachgezogen.
- Alle Python-Dateien kompilieren aktuell ohne Syntaxfehler.
- Neue Bauplan-Ergänzung:
  `coherence`, `asymmetry` und `energy` werden als getrennte Sinnesachsen
  geführt.
  - `coherence`: Fühlen / MCM-Lage
  - `asymmetry`: Wahrnehmen / gerichtete Prägung
  - `energy`: Hören / Frequenz, Kerzenspannung, Stimulus
- Daraus folgt für die nächste Codeprüfung: `energy` darf Außenreiz und
  neuronale Stimulation liefern, aber nicht direkt als innere Feldlage,
  Stressregel oder Entry-Anker wirken.
- Erste Umsetzung:
  `bot_engine/mcm_core_engine.py` erzeugt jetzt einen sensorischen
  Energie-Limiter mit `energy_raw_amplitude`, `energy_limited_amplitude`,
  `energy_amplitude_stimulus`, `energy_limiter_gain` und `energy_overdrive`.
  `core/perception.py` nutzt diesen Wert statt `abs(energy - coherence)`,
  und `MCM_Brain_Modell.py` führt den alten Vision-Pfad mit
  `auditory_stimulus` weiter.
- `energy_frequency_stimulus` bleibt vorerst nur als Kompatibilitätsalias.
  Fachlich ist der aktuelle Kanal kein echter Frequenzwert, sondern begrenzte
  wahrgenommene Lautstärke.
- Die Trennung ist jetzt bis in Feldzustand, Runtime-Snapshot und Stats
  sichtbar:
  `core/runtime_field_state.py` führt `field_stimulus_density` als
  Aktivitäts-/Reizdichte getrennt von `field_density` und `regulatory_load`.
  `core/runtime_entry.py`, `core/runtime_snapshot.py`, `MCM_Brain_Modell.py`
  und `trading/trade_stats.py` reichen diesen Wert weiter.
- Fachlich bedeutet das:
  Ein lautes Feld ist nicht automatisch ein überlastetes Feld. DIO kann jetzt
  unterscheiden, ob viel Außenreiz anliegt oder ob die innere Regulation
  wirklich belastet ist.
- Neue Zielstruktur für das Hören:
  Jeder Markt spielt seine eigene Melodie. Aus den technischen Energiewerten
  soll deshalb schrittweise ein kompaktes `market_hearing_state` entstehen:
  `loudness`, `frequency_hz`, `compression` und `tone`. Das ist noch nicht
  vollständig umgesetzt; bisher existiert der Limiter als erster Sinnesfilter.
- Erster Code-Schritt dazu ist jetzt umgesetzt:
  `bot_engine/mcm_core_engine.py` berechnet `market_hearing_state` über eine
  marktrelative Energie-Baseline. `energy_amplitude_stimulus` nutzt diese
  Lautstärke, `MCM_Brain_Modell.py` übernimmt sie als `auditory_stimulus`.
  Die Frequenz ist aktuell ein symbolischer Hörraum, keine Audio-Ausgabe.
- `core/runtime_entry.py` und `trading/trade_stats.py` reichen diese
  Hörwerte kompakt weiter, damit Läufe später nach `market_tone`,
  `market_loudness`, `market_frequency_hz` und Kompression auswertbar sind.
- Der erste Debug-Lauf danach zeigte einen Übergabebruch:
  Snapshots enthielten die Hörwerte, `trade_stats.json` schrieb sie in
  `recent_attempts` aber noch als `0.0`. `bot_engine/entry_attempt_context.py`
  übernimmt diese Werte jetzt explizit in den Attempt-Kontext.
- Nachprüfung am nächsten Lauf zeigte weiter leere Recent-Attempt-Werte,
  weil No-Plan-/Hold-Resultate die Hörwerte nicht direkt nach oben führten.
  `core/runtime_entry.py` und `_build_runtime_hold_decision()` geben diese
  Felder jetzt ebenfalls direkt aus.
- Weitere Prüfung gegen die neuen DIO-Schichten bleibt offen.
