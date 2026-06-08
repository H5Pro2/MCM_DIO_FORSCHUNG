# 12 Arbeitsspur

Diese Datei ersetzt die alte Denkweise einer Fix-Liste.

Es geht nicht um Fehlerjagd allein, sondern um die aktuelle Arbeitsrichtung.

## Aktueller Korrekturpunkt

Harte innere Schwellen werden zurueckgebaut.

Fachliche Regel:

- Value-/Oekonomie-Pruefung darf hart bleiben.
- Technische Gueltigkeit darf hart bleiben.
- Innere DIO-Zustaende duerfen nicht als starre Wenn-dann-Regeln wirken.
- Profit und Verlust sind Konsequenzsignale.
- Reife, Vertrauen, Vorsicht, Naehe und Handlungsneigung muessen aus
  kontinuierlicher Selbstregulation entstehen.

Erster Rueckbau:

- `bot_gates/entry_decision.py` nutzt kein hartes
  `felt_contact_can_continue` mehr.
- Stattdessen wirken `contact_continuation_support` und
  `contact_continuation_pressure` weich auf `inner_action_support`,
  `inner_action_no` und `inner_action_consent`.

## Aktuell

1. DIO textlich sauber aufbauen.
2. Alte Dokumentation nicht weiter aufblasen.
3. Entry-Pfad zurÃ¼ckfÃ¼hren:
   - reale Form/MCM/Bereich als Entry-Anker
   - Hypothese nur als Deutung/Abstand/BestÃ¤tigung
4. Core-Daten weiter reduzieren:
   - Welt
   - Sehen
   - MCM-Feld
   - keine fertige Trading-Deutung im Core
5. Regulatorschicht prÃ¼fen:
   - keine harten inneren Gates
   - nur Value-Gate bleibt hart
6. Schnittstellen, Neurochemie und MCM-Neuron als technische Baugrundlage
   verwenden.
7. Formsprache, Raumzeit/Variantenraum und Rezeptorik als fehlende alte
   Kernpunkte in den Bauplan Ã¼bernehmen.
8. Spannungsachse, Zero-Point-Regulation, Kontaktreife, Nicht-Handlung,
   Positions-Erleben und OrganÃ¼bersicht als zweite Abgleichrunde Ã¼bernehmen.
9. Code-Bausteine pro Schicht als ErgÃ¤nzung aufbauen und spÃ¤ter gegen den
   bestehenden Projektcode mappen.
10. Bausatzstruktur ohne Programmcode anlegen, damit DIO spÃ¤ter als Library
    sauber aus Modulen und Contracts entstehen kann.
11. Bauplan konsequent ausrichten:
    - MCM-Feld als GefÃ¼hlswahrnehmung
    - Hypothese als Wahrnehmung des eigenen Denkens
    - Strategie nicht erzwingen
    - Strategie nur als freie tragende Reaktion aus Erfahrung zulassen
12. Code-Abgleich gegen diese Richtung:
    - Value-Gate ist als einzige harte PrÃ¼fung passend.
    - Inneres Nein wurde an echte Nicht-Handlung gekoppelt.
    - `strategy_*`-Begriffe wurden als KompatibilitÃ¤tsfelder behalten und
      parallel in DIO-Begriffe Ã¼berfÃ¼hrt:
      `thought_confirmation_bearing`, `thought_rejection_pressure`,
      `thought_trust_bearing`, `contact_context_bearing`.
    - Hypothesen wirken im Entry-Consent weniger direkt motorisch und laufen
      zusÃ¤tzlich Ã¼ber `open_hypothesis_reality_permission`,
      `possibility_contact_bearing`,
      `dominant_hypothesis_reality_bearing` und
      `current_hypothesis_reality_bearing`.
    - `strategic_window` wurde semantisch neutralisiert:
      `area_contact_pull`, `area_contact_timing_fit` und
      `area_future_present_coherence` beschreiben WahrnehmungsnÃ¤he statt
      Strategie-Befehl.
13. Ãœbertragungsmatrix erstellt:
    - bestehende Dateien sind den DIO-Schichten zugeordnet.
    - pro Bereich steht, was behalten, umgebaut oder spÃ¤ter entfernt wird.
    - nÃ¤chste technische PrioritÃ¤t ist `trading/trade_plan.py` als
      Handlungsadapter statt Hypothesen-/Strategiekern.
14. `trading/trade_plan.py` begonnen zurÃ¼ckzufÃ¼hren:
    - neue Kontaktfelder ergÃ¤nzt:
      `area_contact_weight`, `area_contact_fit`, `area_contact_intention`,
      `entry_contact_bearing`, `area_contact_readiness`.
    - Ã¤uÃŸerer Reiz heiÃŸt zusÃ¤tzlich `impulse_perception_pressure`.
    - Hypothesen-TragfÃ¤higkeit heiÃŸt zusÃ¤tzlich `hypothesis_reality_bearing`.
    - alte Felder bleiben nur als KompatibilitÃ¤t bestehen.
15. Nachgelagerte Pfade auf neue Kontaktfelder umgestellt:
    - `core/runtime_entry.py`
    - `bot_gates/entry_decision.py`
    - `trading/trade_stats.py`
    - alte strategische/motorische Felder bleiben Fallback.
16. Erste Quellenfelder fachlich entkoppelt:
    - `core/possibility_field.py` liefert zusÃ¤tzlich
      `possibility_contact_bearing`.
    - `core/review_feedback.py` liefert zusÃ¤tzlich
      `dominant_hypothesis_reality_bearing`.
    - `core/decision_regulation.py` liefert zusÃ¤tzlich
      `open_hypothesis_reality_permission`.
    - alte `action_*`-Felder bleiben nur als Ãœbergangs-KompatibilitÃ¤t.
17. Regulatorischer Pfad nachgezogen:
    - `core/decision_regulation.py` liest
      `open_hypothesis_reality_permission` bevorzugt.
    - die alte `open_hypothesis_action_permission` bleibt nur als technische
      Kopie fÃ¼r alte Ãœbergabepfade.
18. ImpulswÃ¶rter im Entry-Adapter reduziert:
    - `trading/trade_plan.py` bezeichnet schwachen Kontakt nicht mehr als
      `impulse_preferred`, sondern als `area_contact_weak`.
    - `core/runtime_entry.py` synchronisiert fehlenden Bereichskontakt jetzt
      als `contact_context_integrated` oder `contact_context_unresolved`.
19. `trading/trade_plan.py` intern weiter auf Kontaktlogik umgestellt:
    - fÃ¼hrende interne Werte heiÃŸen jetzt `contact_entry_price`,
      `contact_entry_weight`, `contact_entry_fit`,
      `area_contact_distance_fit` und `entry_contact_pressure`.
    - alte Felder wie `strategic_entry_*`, `area_motor_*`,
      `area_direct_readiness` und `hypothesis_action_support` bleiben nur als
      RÃ¼ckgabe-KompatibilitÃ¤t fÃ¼r Runtime, Debug und Stats.
20. Ãœbergabepfade nachgezogen:
    - `core/runtime_entry.py`, `bot_engine/entry_attempt_context.py`,
      `bot_gates/entry_decision.py` und `trading/trade_stats.py` Ã¼bernehmen
      die neuen Kontaktfelder bevorzugt.
    - alte Felder werden weiter mitgeschrieben, aber nicht mehr als fÃ¼hrende
      Fachsprache behandelt.
21. Dokumentationsschnitt aktiviert:
    - alte Dokumentation liegt unter `DIO_BAUPLAN/temp_alt/docs_alt/`.
    - `DIO_BAUPLAN/konstruktion/` ist der aktive Bauplan.
    - es gibt keine zweite aktive Anleitung im alten `docs`-Baum.
22. Erste Konsistenzkorrektur im DIO-Bauplan:
    - `02_SEHEN` ist jetzt ausdrÃ¼cklich Sinneswahrnehmung.
    - sichtbare Form und hÃ¶rbare Marktmelodie laufen in derselben
      Wahrnehmungsschicht, nicht als zwei konkurrierende BauplÃ¤ne.
    - `MarketHearingState` wurde in Schnittstellen, Contracts und
      Code-Bausteine aufgenommen.
23. Grenze MCM-Feld / Regulation geschÃ¤rft:
    - MCM-Feld = gefÃ¼hlte Wirkung.
    - Neurochemie = Modulation dieser Wirkung.
    - Regulation = Umgang mit dieser Wirkung.
    - Feldwerte dÃ¼rfen keine Entry-/Blockade-Logik tragen.
24. Grenze Memory / Thought geschÃ¤rft:
    - Memory speichert reale Erfahrung.
    - Thought-Memory speichert Gedanken zu realer Erfahrung.
    - Konsequenz schreibt getrennt zurÃ¼ck:
      reale Erfahrung nach Memory, Gedankenbewertung nach Thought-Memory.
    - Hypothesen dÃ¼rfen nicht als RealitÃ¤t gespeichert werden.
25. Alte Variablenmechanik verdichtet Ã¼bernommen:
    - neue aktive Datei `29_VARIABLEN_UND_WIRKPFAD.md`.
    - Variablen werden nicht mehr als alte Einzelliste gefÃ¼hrt, sondern Ã¼ber
      Ebene, Rezeptorfamilie, Wirkung, Zielregler, Speicherpfad und
      verbotene Doppelwirkung.
26. Alte `WICHTIG_MECHANIKEN.md` als Quelle kontrolliert:
    - neue aktive Datei `30_MECHANIK_ABGLEICH_WICHTIG.md`.
    - übernommen wird nur, was in die neue Schichtung passt.
    - alte Strategie-, Motorik-, Block- und Permission-Begriffe bleiben
      Übergang oder Archiv, aber nicht aktive Fachsprache.
27. Core-Code-Abgleich begonnen:
    - neue aktive Datei `31_CORE_CODE_ABGLEICH.md`.
    - größte Entflechtungspunkte:
      `core/decision_regulation.py`, `core/runtime_entry.py`,
      `bot_gates/entry_decision.py`, `trading/trade_plan.py`,
      `trading/trade_stats.py`.
    - nächster Rückbau: Permission/Block/Motor-Begriffe in der Regulation
      fachlich entschärfen.
28. Erster Regulation-Adapter umgesetzt:
    - `core/decision_regulation.py` führt neue Bauplan-Aliasse:
      `open_hypothesis_reality_bearing`,
      `open_hypothesis_reality_fit`,
      `open_hypothesis_action_tension`,
      `inner_distance_state`,
      `former_block_reason`.
    - alte Felder bleiben Kompatibilität, aber nicht führende Fachsprache.
    - `python -m py_compile core/decision_regulation.py` erfolgreich.
29. Entry-Brücke auf Reality-Bearing vorbereitet:
    - `bot_gates/entry_decision.py` liest
      `open_hypothesis_reality_bearing` und
      `open_hypothesis_reality_fit` bevorzugt.
    - `permission` bleibt nur Fallback für alte Übergaben.
    - Consent-Trace und Entry-Result führen die neuen Felder mit.
    - `python -m py_compile core/decision_regulation.py bot_gates/entry_decision.py`
      erfolgreich.
30. Trade-Plan weiter zum Handlungsadapter reduziert:
    - `trading/trade_plan.py` nutzt Hypothesen-Beobachtungsdruck nicht mehr
      zur direkten Veränderung der Order-Geometrie.
    - Impulsdruck bleibt Wahrnehmungsdruck und macht keine
      Kontakt-Bereitschaft mehr.
    - neue Rückgabefelder:
      `order_geometry_source=area_contact_adapter` und
      `impulse_role=perception_pressure_only`.
    - `python -m py_compile trading/trade_plan.py core/decision_regulation.py bot_gates/entry_decision.py`
      erfolgreich.
31. Neue Trade-Plan-Diagnosefelder durchgereicht:
    - `core/runtime_entry.py`, `bot_gates/entry_decision.py` und
      `trading/trade_stats.py` führen `order_geometry_source`,
      `impulse_role`, `open_hypothesis_reality_bearing` und
      `open_hypothesis_reality_fit` mit.
    - Damit ist im Debug sichtbar, ob Entry-Geometrie wirklich aus Kontakt
      kommt und Impuls nur Wahrnehmungsdruck bleibt.
    - `python -m py_compile trading/trade_stats.py core/runtime_entry.py bot_gates/entry_decision.py trading/trade_plan.py core/decision_regulation.py`
      erfolgreich.
32. Konsistenzfehler im Zustimmungs-/Regulationspfad korrigiert:
    - `bot_gates/entry_decision.py` verwendete nach der Umbenennung noch
      `strategic_fit`, obwohl fachlich bereits `contact_fit` gefÃ¼hrt wird.
    - Der innere Zustimmungswert nutzt jetzt `contact_fit`.
    - `entry_contact_state`, `area_contact_focus_id` und
      `area_contact_location` werden bevorzugt gelesen; alte
      `entry_choice_*`-/`strategic_*`-Felder bleiben nur Fallback.
33. Beobachtungs-/Stats-Pfad ergÃ¤nzt:
    - inferierte BeobachtungsplÃ¤ne in `trading/trade_stats.py` fÃ¼hren jetzt
      ebenfalls `contact_entry_mode`, `entry_contact_state`,
      `area_contact_focus_id` und `area_contact_location`.
    - Dadurch bleibt die Debug-/Lernspur fachlich nÃ¤her an Kontakt,
      Wahrnehmung und RealitÃ¤t statt an Strategie-/Motorikbegriffen.
34. Innerer Zustimmungsregler fachlich umbenannt:
    - In `bot_gates/entry_decision.py` entstehen die tragenden Werte intern
      jetzt als `thought_confirmation_bearing`, `thought_rejection_pressure`,
      `thought_trust_bearing`, `contact_context_bearing` und
      `thought_contradiction_pressure`.
    - Die alten `strategy_*`-Felder werden nur noch als KompatibilitÃ¤tskopie
      ausgegeben.
    - Die Entry-Bridge-Debugausgabe spricht jetzt ebenfalls von
      `thought_*`, `contact_context_bearing`, `entry_contact_state` und
      `area_contact_location`.
    - Damit wird Hypothese nicht als fertige Strategie behandelt, sondern als
      Gedankenspur, die gegen Kontakt und RealitÃ¤t getragen werden muss.
35. Neue Kernwahrnehmungs-Trennung ergÃ¤nzt:
    - `coherence` wird als FÃ¼hlen / MCM-Lage gefÃ¼hrt.
    - `asymmetry` wird als Wahrnehmen / gerichtete PrÃ¤gung gefÃ¼hrt.
    - `energy` wird als HÃ¶ren / Kerzenspannung / Frequenzstimulus gefÃ¼hrt.
    - Hohe Energie darf nicht automatisch innere MCM-Unruhe bedeuten. Sie ist
      zuerst AuÃŸenreiz und wird erst durch MCM-Feld, Filterung, Nachhall und
      Regulation zur inneren Lage.
36. NÃ¤chste technische Klassifikation erweitert:
    - Alte `strategy_*`, `motor_*`, `action_*`-Felder werden nicht nur nach
      Namen geprÃ¼ft, sondern auch danach, ob sie SinneskanÃ¤le vermischen.
    - Besonders zu prÃ¼fen: Wo `energy` direkt wie Stress, Feldchaos oder
      Handlungstreiber wirkt, obwohl es nur Stimulus/Frequenz sein sollte.
37. Erste Code-Trennung fÃ¼r `energy` umgesetzt:
    - `bot_engine/mcm_core_engine.py` gibt zusÃ¤tzlich
      `energy_raw_amplitude`, `energy_limited_amplitude`,
      `energy_amplitude_stimulus`, `energy_limiter_gain`,
      `energy_overdrive` und `energy_stimulus_channel` aus.
    - Die Kerzenenergie lÃ¤uft durch einen weichen sensorischen Limiter.
      Zu laute Peaks werden komprimiert, statt DIO direkt zu Ã¼berreizen.
    - `core/perception.py` vergleicht `energy` nicht mehr direkt mit
      `coherence`; die BewegungsÃ¤nderung nutzt jetzt die begrenzte
      LautstÃ¤rke.
    - `MCM_Brain_Modell.py` fÃ¼hrt im alten Vision-Pfad
      `auditory_stimulus` / `energy_amplitude_stimulus`.
    - Hohe Energie trÃ¤gt dort nur noch reduziert zur `threat_map` bei und
      wirkt primÃ¤r als Wahrnehmungsreiz.
    - `energy_frequency_stimulus` bleibt nur als technischer Alias, bis alle
      nachgelagerten Pfade umbenannt sind.
38. FeldÃ¼berreizung fachlich getrennt:
    - `core/runtime_field_state.py` fÃ¼hrt `field_stimulus_density` ein.
    - `field_stimulus_density` beschreibt, wie laut/aktiv der Reizraum ist.
    - `field_density` und `regulatory_load` beschreiben weiter, wie stark das
      innere Feld und die Regulation tatsÃ¤chlich belastet werden.
    - Dieser Wert wird durch Runtime, Snapshot und Trade-Stats weitergereicht.
    - Ziel: DIO soll nicht jeden starken AuÃŸenreiz als innere Ãœberlastung
      behandeln.
39. HÃ¶ren als kompakte Marktmelodie festgehalten:
    - Jeder Markt spielt seine eigene Melodie. SOL, BTC oder andere MÃ¤rkte
      dÃ¼rfen nicht nur Ã¼ber rohe KerzengrÃ¶ÃŸe verglichen werden.
    - `energy` bleibt Rohmaterial fÃ¼r das HÃ¶ren, soll nach auÃŸen aber in einer
      kompakten Wahrnehmungsstruktur gefÃ¼hrt werden.
    - Zielstruktur: `market_hearing_state` mit `loudness`, `frequency_hz`,
      `compression` und `tone`.
    - Der sensorische Limiter ist nur der erste Schritt. Offen bleibt die
      marktrelative Normalisierung, damit verschiedene MÃ¤rkte in einem
      einheitlichen HÃ¶rraum wahrnehmbar bleiben, ohne ihre eigene Melodie zu
      verlieren.
40. Erster Code-Schritt zur Marktmelodie umgesetzt:
    - `bot_engine/mcm_core_engine.py` bildet jetzt ein `market_hearing_state`.
    - Die Kerzenenergie wird gegen eine marktrelative Baseline gelesen.
    - Daraus entstehen `loudness`, `frequency_hz`, `compression` und `tone`.
    - `energy_amplitude_stimulus` nutzt diese marktrelative LautstÃ¤rke.
    - Die Frequenz ist vorerst symbolischer HÃ¶rraum, keine echte
      Audio-Wiedergabe.
41. Marktmelodie kompakt in Entry-/Stats-Pfade durchgereicht:
    - `core/runtime_entry.py` gibt `market_hearing_state`,
      `market_loudness`, `market_frequency_hz`,
      `market_hearing_compression` und `market_tone` aus.
    - `trading/trade_stats.py` Ã¼bernimmt diese Felder kompakt in
      Attempt-/Recent-Spuren.
    - Damit ist sichtbar, ob DIO einen Markt gerade als leise, klar, hell,
      Ã¼bersteuert oder komprimiert wahrnimmt.
42. Ãœbergabebruch in Attempt-Kontext korrigiert:
    - Der erste Lauf nach der Marktmelodie zeigte:
      Snapshots enthielten `market_hearing_state`, aber `trade_stats.json`
      schrieb in `recent_attempts` noch Nullen.
    - Ursache: `bot_engine/entry_attempt_context.py` Ã¼bernahm die neuen
      HÃ¶rwerte nicht in den kompakten Attempt-Kontext.
    - Korrigiert: `market_hearing_state`, `market_loudness`,
      `market_frequency_hz`, `market_hearing_compression` und `market_tone`
      werden jetzt in Attempt-Kontexte Ã¼bernommen.
    - ZusÃ¤tzlich werden No-Plan- und Hold-Resultate direkt mit den
      HÃ¶rfeldern versehen, damit Beobachtung, Replan und Withheld nicht Ã¼ber
      leere Zwischenpfade laufen.

## NÃ¤chster PrÃ¼fpunkt

43. Trade-Plan auf Bauplan-Schnitt zurückgeführt:
    - `trading/trade_plan.py` ist fachlich nur noch ein Action-Adapter.
    - Entry-Geometrie entsteht aus realem Bereichs-/Kontaktfit.
    - Hypothesen liefern Realitätsbezug und Beobachtungsdruck, aber keinen
      direkten Entry-Anker.
    - Impuls bleibt `impulse_perception_pressure`: ein äußerer Reiz, keine
      Handelsmotorik.
    - Alte Felder wie `entry_contact_pressure`, `entry_choice_pressure` und
      `entry_choice_conflict` werden neutral gehalten, damit sie nicht wieder
      unbemerkt als Motor-Signal wirken.
44. Möglichkeitspfad sprachlich entkoppelt:
    - `core/possibility_field.py` schreibt primär
      `open_hypothesis_reality_bearing` und `open_hypothesis_reality_fit`.
    - Alte Permission-Felder bleiben nur als Übergabe-Alias erhalten.
    - Fachlich bedeutet das: DIO bekommt keine Erlaubnis durch eine These,
      sondern eine Einschätzung, wie gut Gedanke und Realität tragen.
45. Regulatorische Begriffe nachgezogen:
    - In `core/decision_regulation.py` wurden weitere aktive Lesepfade auf
      `reality_bearing` und `action_tension` umgestellt.
    - `permission` und `motor` sind damit keine fachlichen Leitbegriffe mehr,
      sondern nur noch Kompatibilitätsnamen an alten Schnittstellen.
46. Verifikation:
    - Kompiliert wurden `core/decision_regulation.py`,
      `core/possibility_field.py`, `trading/trade_plan.py`,
      `core/runtime_entry.py`, `bot_gates/entry_decision.py` und
      `trading/trade_stats.py`.
    - Ergebnis: keine Syntaxfehler.

47. Laufanalyse: zu wenige Trades durch Überhemmung:
    - Der Lauf erzeugte 5000 Attempts, aber nur 11 Submitted und 4 Filled.
    - Es fehlte nicht an Wahrnehmung: viele Versuche lagen in Structure-Zonen
      und `area_contact_entry` war vorhanden.
    - Die Engstelle lag in `bot_gates/entry_decision.py`:
      realer Bereichs-/MCM-Kontakt wurde von offener Hypothesenunsicherheit
      fast vollständig in Observe/Replan zurückgedrückt.
    - Korrigiert: `real_area_contact_bearing` entlastet jetzt die innere
      Brücke. Echter Kontakt kann Denkunsicherheit dämpfen, ohne dass Impuls
      wieder Entry-Anker wird.
    - Debug/Stats tragen `real_area_contact_bearing`, damit der nächste Lauf
      zeigt, ob Kontaktreife wirklich durchkommt.

48. Zweite Laufanalyse: ?ffnung war zu stark:
    - Nach der ersten Entlastung stieg der Lauf auf 166 Trades.
    - Ergebnis: 39 TP, 127 SL, Netto ungef?hr -22.
    - Ursache: `real_area_contact_bearing` lag im Entry-Debug zu hoch und
      d?mpfte die innere Ablehnung fast vollst?ndig.
    - Korrigiert: `real_area_contact_bearing` wird jetzt aus mehreren
      Kontaktqualit?ten gebildet, nicht mehr aus dem st?rksten Einzelwert.
    - Hohe Gedankenablehnung und sehr schwaches Gedankentragen reduzieren die
      Kontaktwirkung weich.
    - Die innere Br?cke bleibt offen, aber echter Kontakt muss jetzt wieder
      koh?renter tragen.

Nach dem Consent-Fix muss ein Lauf zeigen:

- weniger kopfloses Handeln
- keine RÃ¼ckkehr zu 0-Trades durch Ãœberhemmung
- klare Zunahme von Beobachtungslernen
- saubere Speicherung von `inner_action_consent_state`
- Hypothesen bleiben Denkspuren, keine Strategieanker

## Danach

49. Alte motorische/strategische Felder weiter aus der fachlichen Bewertung
   herauslÃ¶sen.
50. Ãœberladene Variablen gruppieren oder entfernen.
51. Alte PlÃ¤ne archivieren.
52. `BAUPLAN.md` als Hauptplan und spÃ¤teren Konstruktionsplan fÃ¼hren.

53. Sehen vom MCM-Feld sauberer getrennt:
    - `bot_engine/mcm_core_engine.py` erzeugt keine visuelle Wahrnehmung mehr.
      Der Core bleibt energetische Spur und Marktmelodie.
    - `core/visual_attention.py` fuehrt eine weiche Aufmerksamkeitsschicht ein.
    - `visual_form_state` bleibt rohes Sehen.
    - `visual_attention_state` entscheidet fachlich, ob eine Form nur
      Hintergrund bleibt oder als Kontakt naeher betrachtet wird.
    - Das MCM-Feld bekommt jetzt gewichtete visuelle Wirkung:
      `visual_mcm_contact_weight`, `visual_attention_depth` und
      `visual_background_filter`.
    - Ziel: weniger Reizflut, keine harte Sperre, klarere Trennung zwischen
      Aussenwahrnehmung und innerer Feldwirkung.

54. Naechster Lauf soll pruefen:
    - ob `visual_attention_label` zwischen Hintergrund und Formkontakt
      unterscheidet
    - ob `visual_mcm_contact_weight` nicht dauerhaft maximal ist
    - ob `field_action_support` und `inner_outer_alignment` steigen
    - ob `cognitive_lag_pressure` sinkt oder weiter auf Ueberdenken zeigt

55. Marktmelodie-Debug eingefuehrt:
    - `core/runtime_entry.py` schreibt jetzt ein kompaktes
      `mcm_market_melody_protocol.csv`.
    - Datei liegt bei gruppierten Debugs unter `debug/debug_lauf_x/perception/`.
    - Enthalten sind OHLC, `coherence`, `asymmetry`, `energy`,
      Roh-/Limiter-Energie, `market_loudness`, `market_frequency_hz`,
      `market_hearing_compression`, `market_tone` und die aktuelle visuelle
      Aufmerksamkeitskopplung.
    - Ziel: Hoeren des Marktes isoliert pruefen, ohne `trade_stats.json` zu
      ueberladen.

56. Marktmelodie-Frequenz mittiger kalibriert:
    - Der erste saubere Melodie-Lauf zeigte, dass normale Bewegung zu oft im
      oberen Hoerbereich lag.
    - `MCM_MARKET_HEARING_FREQUENCY_CURVE` wurde eingefuehrt.
    - Die Frequenz bleibt weiter aus `market_loudness` abgeleitet, wird aber
      psychoakustisch gekruemmt:
      normale Lautstaerke landet mittiger, echte Uebersteuerung kann weiter
      nach oben laufen.
    - Der Melodie-Debug schreibt jetzt pro Marktkerze und vermeidet doppelte
      Zeilen bei gleichem Timestamp/OHLC/Frequenz-Key.
    - Erwartung fuer den naechsten Lauf: weniger Dauerhelligkeit,
      differenziertere Tiefton-/Mittelton-/Klarbereich-Verteilung.

57. Lauf 10 geprueft und zwei Wahrnehmungs-/Regulationsfehler korrigiert:
    - `mcm_market_melody_protocol.csv` ist jetzt technisch sauber:
      Header vorhanden, jede Kerze eine Zeile, keine Tick-Luecken.
    - Frequenzbereich ist deutlich mittiger als im Lauf davor.
    - `cognitive_lag_pressure` klebte weiter dauerhaft auf `1.0`, weil
      Rueckstandsspannung nur aufgebaut, aber nicht abgebaut wurde.
      Korrigiert: natuerlicher Nachhall-Abbau pro Welt-Tick ohne Drop.
    - `field_perception_focus` und `field_perception_stability` kamen im
      Feldprotokoll dauerhaft als `0.0`, obwohl Neuron-/Arealzustand Daten
      liefert. Korrigiert: Processing leitet Fokus und Stabilitaet weich aus
      visueller MCM-Kontaktwirkung, Neuronenaktivitaet, Arealstabilitaet,
      Feldsupport und Druck ab.
    - Das ist keine Strategy-Aenderung. Es stellt nur sicher, dass DIO seine
      innere Feldlage nicht als blind/instabil liest, wenn das Feld ruhig oder
      schwach ausgepraegt ist.

58. Naechster Lauf:
    - `cognitive_lag_pressure` darf nicht mehr dauerhaft `1.0` sein.
    - `field_focus` und `field_stability` sollten im Feldprotokoll Werte ueber
      `0.0` zeigen.
    - Danach erst Tradingverhalten bewerten: Trades, TP/SL, Observe/Hold und
      PnL sind nur sinnvoll, wenn diese inneren Basiswerte stimmen.

59. Lauf 11 geprueft:
    - Feldfokus und Feldstabilitaet sind wieder lebendig:
      `field_focus` ca. 0.23 bis 0.47, `field_stability` ca. 0.64 bis 0.78.
    - `cognitive_lag_pressure` blieb trotzdem dauerhaft `1.0`.
    - Ursache ist nicht mehr der Abbauwert selbst, sondern der Backtest-Ablauf:
      Die Aussenwelt publizierte im Lauf bis ueber 33000 Weltfenster, davon
      wurden ueber 27000 verworfen. DIO verarbeitete also keinen sauberen
      Marktstrom, sondern einen massiven Wahrnehmungsverlust.
    - `BACKTEST_WAIT_FOR_RUNTIME_IDLE` wurde wieder wirksam gemacht:
      Der normale Backtest wartet jetzt nach jeder Kerze auf die Runtime.
      Damit verarbeitet DIO jede Kerze. Der asynchrone Stress-Test bleibt ueber
      `BACKTEST_WAIT_FOR_RUNTIME_IDLE=False` moeglich.
    - Das ist eine Runner-/Simulationskorrektur, keine DIO-Strategieaenderung.

60. Lauf 12 geprueft:
    - Die Runner-Korrektur wirkt: keine verpassten Welt-Ticks, keine Queue,
      `cognitive_lag_pressure` bleibt bei `0.0`.
    - Der Lauf ist damit technisch sauber, aber fachlich zu offen:
      494 Trades, 169 TP, 325 SL, Netto ca. -19.55.
    - Hauptschaden kommt von LONG: ca. -25.32, waehrend SHORT noch positiv
      blieb.
    - Ursache liegt in `bot_gates/entry_decision.py`: realer Bereichskontakt
      durfte die innere Bruecke zu stark tragen. Im Debug lag
      `thought_trust_bearing` bei akzeptierten Entries sehr niedrig, waehrend
      `real_area_contact_bearing` hoch blieb.
    - Korrigiert: Bereichskontakt bleibt Wahrnehmungs-/Kontaktnaehe, wird aber
      weicher an Gedankenbestaetigung, Vertrauen und Realitaetsbindung
      gekoppelt.
    - Neu sichtbar: `thought_contact_consent`, `untrusted_contact_pressure`
      und `raw_area_contact_bearing`. Damit kann der naechste Lauf zeigen, ob
      Kontaktreiz und innere Zustimmung wieder sauber getrennt sind.

61. Marktmelodie fuer Standardlaeufe abgeschaltet:
    - `mcm_market_melody_protocol.csv` war im letzten Lauf die groesste
      Debug-Datei und belastet normale Backtests unnoetig.
    - Standardprofile schreiben die Marktmelodie nicht mehr. `RESEARCH_DEBUG`
      kann sie weiterhin gezielt einschalten.
    - Fachliche Richtung: Marktmelodie soll spaeter als Audio-/Signaladapter
      verarbeitet werden, nicht als dauerhafte CSV-Mitschrift. Dann hoert DIO
      ein normalisiertes Frequenz-/Lautstaerke-Signal, statt Datenzeilen zu
      sammeln.

62. Verbindliche Sinnes- und Handlungstrennung festgehalten:
    - Bauplan-Kern:
      `Sehen = Form/Struktur`,
      `Fuehlen = MCM-Feldwirkung`,
      `Hoeren = Energie/Frequenz/Marktspannung`,
      `Denken = Hypothese/Verdichtung`,
      `Handeln = erst nach tragender Kopplung`.
    - Eingetragen in `00_BAUPLAN.md`, `02_SEHEN.md` und
      `23_ORGANUEBERSICHT.md`.
    - Das ist die Leitmechanik fuer den Rueckbau: Sinneskanal ist nicht
      Handlung, und Thought ist nicht Realitaet.

63. Markt-Hoeren als eigenes Core-Modul begonnen:
    - Neue Datei: `core/market_audio.py`.
    - Aufgabe: Kerzenenergie in einen kompakten Hoerzustand uebersetzen:
      `loudness`, `frequency_hz`, `compression`, `tone`.
    - `bot_engine/mcm_core_engine.py` nutzt diesen Adapter jetzt fuer
      Energie-Limiter und `market_hearing_state`.
    - Der Adapter setzt fachlich `sense=hearing`, `channel=market_audio` und
      `action_permission=0.0`. Damit ist technisch sichtbar: Hoeren ist
      Sinnesreiz, keine Entry-Erlaubnis.
    - Verifikation: `core/market_audio.py` und `bot_engine/mcm_core_engine.py`
      kompilieren fehlerfrei.
    - Sicherheitspruefung nachgezogen: alte ungenutzte Hoer-Hilfsfunktionen
      wurden aus `bot_engine/mcm_core_engine.py` entfernt. Die Hoerlogik liegt
      jetzt eindeutig in `core/market_audio.py`.

64. Hoeren als neuronale Stimulation ohne Entry-Wirkung:
    - `market_hearing_state` wird jetzt in `step_mcm_brain` bis zum
      `MCMField` durchgereicht.
    - Das Feld baut daraus eine separate auditive Neuronenspur:
      `auditory_impulse`, `auditory_aftertone`, `auditory_resonance` und
      `auditory_neural_state`.
    - Diese Spur stimuliert die Neuronen als Hoerreiz, wird aber nicht in
      `external_impulse`, `impulse`, `motivation_impulse`, `risk_impulse`,
      Entry oder Trade-Plan gemischt.
    - Alte direkte Kopplung entfernt: `auditory_stimulus` beeinflusst
      `threat_map` und `orientation_drive` nicht mehr.
    - Sicherheitspruefung: laute und stille Marktmelodie liefern identische
      Entry-Impulswerte; `auditory_neural_action_permission` bleibt `0.0`.
    - Verifikation: `config.py`, `core/mcm_model.py`,
      `debug_tools/field_snapshots.py` und `MCM_Brain_Modell.py`
      kompilieren fehlerfrei.

65. Backtest-Laufzeit entkoppelt und Schreiblast reduziert:
    - Befund: `WORLD_TIME_SECONDS=0.01` wurde im Backtest als echte
      `sleep()`-Pause pro Kerze verwendet. Bei mehrmonatigen 5m-Daten erzeugt
      das mehrere Minuten reine Wartezeit, ohne DIO fachlich klueger zu machen.
    - Neu: `BACKTEST_REPLAY_SLEEP_ENABLED=False` ist Standard. Die Marktzeit
      bleibt ueber Candle-Zeitstempel erhalten, aber der Backtest laeuft
      beschleunigt ohne kuenstliche Pause.
    - Runtime-Wartezeiten fuer Backtests wurden auf kurze Poll-Intervalle
      gestellt: `MCM_BACKTEST_RUNTIME_IDLE_SLEEP_SECONDS` und
      `MCM_RUNTIME_QUEUE_IDLE_POLL_SECONDS`.
    - Im `LEAN_BACKTEST` werden Memory-Dateien seltener persistiert:
      Form- und Thought-Memory lernen weiter im RAM, schreiben aber erst
      groesser gebuendelt auf Platte.
    - `TRADE_STATS_FAST_ATTEMPT_PATH` bleibt fuer Lean-Laeufe aktiv, damit
      Attempt-Zaehler und Feedbackachsen erhalten bleiben, ohne jeden Versuch
      vollstaendig als schweren Debug-Kontext zu normalisieren.
    - Verifikation: `config.py`, `runner.py`, `bot_engine/runtime_timing.py`
      und `bot_engine/runtime_thread.py` kompilieren fehlerfrei.

66. Schwere Cluster-Abhaengigkeit entfernt:
    - Befund: `sklearn.cluster.DBSCAN` zog beim Start grosse SciPy/Sklearn-
      Module nach. Das war fuer 120 MCM-Neuronen unverhaeltnismaessig.
    - `ClusterDetector` nutzt jetzt eine lokale, kleine DBSCAN-Variante:
      Distanzraum, Core-Punkte ab `min_samples`, zusammenhaengende
      Dichte-Inseln als Cluster.
    - Fachlich bleibt die Feld-Insel-Erkennung erhalten; technisch faellt
      der schwere Import weg.
    - Zusaetzlich beginnt der Memory-Save-Cooldown jetzt beim Runtime-Start,
      damit der erste Backtest-Flush nicht sofort auf Platte schreibt.
    - Messung: Smoke-Lauf mit 500 Fenstern fiel von ca. 4.8s auf ca. 2.2s
      nach der lokalen Clusterung und weiter auf ca. 1.9s nach der
      Persistenz-Startkorrektur.
    - Verifikation: `core/mcm_model.py` und `bot_engine/runtime_thread.py`
      kompilieren fehlerfrei.

67. Standard-Backtest ohne Queue-/Thread-Overhead:
    - Befund: Der normale Backtest publizierte jede Kerze in die Runtime-Queue
      und wartete danach sofort auf denselben Thread. Das war funktional
      korrekt, aber fuer deterministische Backtests unnoetig teuer.
    - Neu: `BACKTEST_SYNCHRONOUS_RUNTIME=True` verarbeitet Backtest-Kerzen
      direkt ueber denselben Runtime-/Action-Pfad, aber ohne Queue, Polling
      und Thread-Join.
    - LIVE und Stress-Test bleiben asynchron:
      `BACKTEST_WAIT_FOR_RUNTIME_IDLE=False` nutzt weiterhin den Queue-Pfad.
    - Memory wird im synchronen Backtest am Ende einmal gezielt gespeichert,
      im Smoke mit `save_memory=False` nicht.
    - Messung: Smoke-Lauf mit 500 Fenstern liegt danach bei ca. 1.6s.
    - Verifikation: `config.py`, `runner.py`, `bot.py` und
      `bot_engine/runtime_thread.py` kompilieren fehlerfrei.

68. Experience- und Symbolspeicher entlastet:
    - Befund auf realem 3-4-Datensatz: Form-Symbol-Outcomes erzwangen
      direkte Datei-Schreibvorgaenge; Tracking-Events verdichteten zu oft in
      den Experience-Space.
    - Form-Symbol-Outcome-Lernen bleibt im RAM aktiv, schreibt aber nicht mehr
      bei jedem Outcome erzwungen auf Platte. Persistenz laeuft periodisch bzw.
      am Laufende.
    - Experience-Space-Link-Buckets werden in-place aktualisiert, statt den
      gesamten Speicherbereich mehrfach pro Ereignis zu kopieren.
    - Im `LEAN_BACKTEST` verdichten Pending-/Positions-Tracking-Events nicht
      jedes Mal in Experience-Space. Die Episode selbst bleibt erhalten;
      relevante Ereignisse und Outcomes verdichten weiter.
    - Verifikation: `core/form_symbol_orchestration.py`,
      `core/experience_space.py`, `config.py` und `MCM_Brain_Modell.py`
      kompilieren fehlerfrei.

69. MCM-Feldlaufzeit reduziert:
    - Befund: Der Backtest war nicht mehr durch Datei-Debugging dominiert,
      sondern durch pro Tick erzeugte Voll-Snapshots und viele kleine
      Python-/NumPy-Aufrufe im Neuronenschritt.
    - Feld-Snapshots lesen jetzt direkt leichte Zustandswerte aus dem Feld,
      statt pro Tick `field.read_snapshot()` mit allen Neuronen-Dicts zu
      erzeugen.
    - Experience-Achsen und Reward-Delta werden pro Episode einmal berechnet
      und in den Link-Buckets wiederverwendet.
    - `MCM_FIELD_VECTORIZED_STEP_ENABLED=True` berechnet den neuronalen
      Feldschritt feldweise. Die MCM-Grundmechanik bleibt erhalten:
      Kopplung, Regulation, Memory-Trace, Audio-Nachhall, Aktivierung,
      Stabilitaet und Ueberlastung werden weiter gefuehrt.
    - `cluster.detect()` erhoeht seine interne Clusteruhr nur noch beim
      ersten Clusterzugriff eines Brain-Schritts. Der zweite Zugriff liest den
      Zustand fuer Snapshot/Topologie mit, ohne das Clusterintervall kuenstlich
      doppelt weiterzuschieben.
    - Im `LEAN_BACKTEST` werden detaillierte `activation_components` pro
      Neuron nicht mehr pro Tick aufgebaut; sie sind Analyse-/GUI-Ballast,
      keine Entscheidungsmechanik.
    - Messung auf `data/3-4_2026_5m_SOLUSDT.csv` mit 200 Fenstern:
      ca. 12.1s vor den letzten Entlastungen, danach ca. 7.9s.
    - Verifikation: `config.py`, `core/mcm_model.py`,
      `debug_tools/field_snapshots.py`, `core/experience_space.py` und
      `MCM_Brain_Modell.py` kompilieren fehlerfrei.

70. Bereichskontakt von Handlungskopplung getrennt:
    - Befund aus `debug_lauf_1`: DIO handelte zu oft aus
      `area_contact_entry`, obwohl `thought_confirmation_bearing` und
      `thought_contact_consent` fast null waren. Das war kein Value-Gate-
      Problem, sondern eine zu direkte Kopplung von Beruehrung und Motorik.
    - `bot_gates/entry_decision.py` fuehrt jetzt
      `thought_area_coupling` und `uncoupled_area_contact_pressure`.
    - Bereichskontakt bleibt damit ein Reiz. Erst wenn Form/MCM/Gedanke
      gemeinsam tragen, steigt die Handlungskopplung. Fehlt diese Kopplung,
      steigt organisch die innere Vorsicht und der Kontakt wird eher
      beobachtet oder neu gelesen.
    - Das ist keine harte Zusatzregel neben dem Value-Gate, sondern eine
      metaregulatorische Gewichtung im inneren Zustimmungsmodell.
    - Verifikation: `bot_gates/entry_decision.py` und
      `trading/trade_plan.py` kompilieren fehlerfrei.

71. Beobachtungslernen im schnellen Attempt-Pfad repariert:
    - Befund: Nach der Entlastung des Debug-/Stats-Pfades wurden
      `observed_only`, `withheld`, `replanned` und `skipped` im schnellen
      Attempt-Pfad zwar gezaehlt, aber nicht mehr in die
      Beobachtungs-/Hypothesenreife zurueckgefuehrt.
    - Wirkung: DIO sah viele Situationen, bildete aber keine reifenden
      Hypothesenfamilien. `hypothesis_trust_family_count` blieb 0,
      `recent_observation_learning` blieb leer und `thought_area_coupling`
      konnte kaum wachsen.
    - Korrektur: `trading/trade_stats.py` ruft im schnellen Attempt-Pfad
      wieder `_register_observation_learning(...)` fuer beobachtete,
      verhaltene, replante und uebersprungene Handlungsnaehen auf.
    - Fachlich: Das ist kein neues Gate. Es stellt nur den Lernkreis wieder
      her: Wahrnehmung -> nicht gehandelte Hypothese -> spaetere reale
      Bestaetigung oder Entlastung -> Reife/Vertrauen/Vorsicht.
    - Smoke-Befund auf 400 Fenstern `data/3-4_2026_5m_SOLUSDT.csv`:
      `observation_learning_resolved=237`, `hypothesis_trust_family_count=80`,
      dominante Familie `trust≈0.60`, `readiness≈0.57`.
    - Verifikation: `trading/trade_stats.py` kompiliert fehlerfrei.

73. Kuenstliche Beobachtungs-Trades entfernt:
    - Befund aus `debug_lauf_10`: DIO handelte wieder zu breit
      (`350` Trades, `PnL=-15.24`). Long war stark negativ, Short positiv.
      Die Ursache lag nicht im Value-Gate, sondern in der Beobachtungsreife:
      allgemeines Hold/Observe wurde bei fehlender Entry-Geometrie als
      hypothetischer Trade rekonstruiert.
    - Das war fachlich falsch: Beobachten ist nicht automatisch ein
      gedachter Trade. Eine Hypothese darf nur gegen die Realitaet reifen,
      wenn DIO tatsaechlich eine konkrete Entry-/SL-/TP-Geometrie im Feld
      hatte.
    - Korrektur: `_register_observation_learning(...)` erzeugt keine
      kuenstlichen Beobachtungs-Trades mehr aus allgemeinem Signalzustand.
      Ohne konkrete Trade-Geometrie wird keine `would_have_carried` /
      `would_have_hurt`-Reifung angelegt.
    - Fachlich: Das trennt Wahrnehmung, Gedanke und Realitaetsanker wieder
      sauberer. Nicht jede innere Regung wird als Strategie behandelt.
    - Kontrolllauf auf 500 Fenstern `data/3-4_2026_5m_SOLUSDT.csv`:
      `trades=1`, `attempts_submitted=4`,
      `observation_learning_resolved=97`,
      `hypothesis_trust_family_count=80`. Die Motorik ist deutlich ruhiger;
      naechster Schritt ist die Qualitaet der echten Entry-Geometrien zu
      pruefen.
    - Verifikation: `trading/trade_stats.py` kompiliert fehlerfrei.

74. Bereichskontakt stärker als nervliche Last moduliert:
    - Befund aus dem 2-Monats-Lauf `debug_lauf_12`: Trotz Entfernung
      kuenstlicher Beobachtungs-Trades handelte DIO wieder zu breit
      (`444` Trades, `PnL=-22.22`). Die akzeptierten Entries zeigten weiter
      `area_contact_entry` mit teilweise schwacher `thought_area_coupling`.
    - Ursache: Der Bereichskontakt trug noch zu stark in `inner_support`.
      Selbst schwach gekoppelte Form/MCM/Gedanken-Lagen konnten dadurch
      Handlung ausloesen.
    - Korrektur: In `bot_gates/entry_decision.py` wurde die Basistragung des
      Bereichskontakts reduziert. `uncoupled_area_contact_pressure` und
      `untrusted_contact_pressure` wirken staerker als innere Vorsicht.
    - Fachlich: Das ist weiterhin kein hartes Zusatz-Gate. Bereichskontakt
      bleibt Reiz, aber ohne Denk-/MCM-Kopplung fuehlt er sich weniger
      handlungsnah und mehr pruefbeduerftig an.
    - Kontrolllauf auf 500 Fenstern `data/1-2_2026_5m_SOLUSDT.csv`:
      `trades=7`, `attempts_submitted=13`, `PnL=-3.76`. Die Motorik ist
      deutlich ruhiger; die naechste Baustelle ist die Qualitaet der Entry-
      Geometrie, nicht mehr die reine Trade-Menge.
    - Verifikation: `bot_gates/entry_decision.py` kompiliert fehlerfrei.

72. Beobachtungslernen an reale Aussenwelt gebunden:
    - Befund aus `debug_lauf_8`: Nach Wiederaktivierung des
      Beobachtungslernens entstanden zu viele Trades (`289`) bei negativem
      Ergebnis. Ursache war keine Value-Gate-Entscheidung, sondern eine
      falsche Preisquelle in der Hypothesenaufloesung.
    - `_extract_observation_price(...)` las zuerst den gedachten
      `trade_plan.entry_price` und erst danach die reale Markt-/Kerzenlage.
      Dadurch wurden alte Beobachtungen gegen neu gedachte Entry-Geometrien
      statt gegen die Aussenwelt aufgeloest.
    - Korrektur: Beobachtungslernen nutzt jetzt zuerst
      `world_state.current_price` bzw. `candle_state.close`. Der gedachte
      Entry-Preis bleibt nur Fallback, wenn keine reale Preisquelle vorhanden
      ist.
    - Fachlich: Hypothese bleibt Hypothese. Reife entsteht erst durch Abgleich
      mit dem, was real vor DIO geschieht.
    - Kontrolllauf auf 500 Fenstern `data/3-4_2026_5m_SOLUSDT.csv`:
      `trades=3`, `attempts_submitted=7`,
      `observation_learning_resolved=408`,
      `hypothesis_trust_family_count=80`. Die Motorik ist wieder deutlich
      ruhiger; die Wirtschaftlichkeit muss im naechsten echten Lauf geprueft
      werden.
    - Verifikation: `trading/trade_stats.py` kompiliert fehlerfrei.

75. Markt-Hoeren als WAV-Debug ergaenzt:
    - DIO hatte bereits eine interne Hoerspur (`market_hearing_state`) mit
      `loudness`, `frequency_hz`, `compression` und `tone`. Bisher wurde
      diese Wahrnehmung aber nur intern bzw. optional als CSV-Protokoll
      sichtbar.
    - Ergaenzung: `debug_tools/audio_debug.py` sammelt die Hoerproben im RAM
      und schreibt am Laufende eine Mono-PCM-Datei
      `perception/market_melody.wav` plus `market_melody_meta.txt`.
    - Fachlich: Die WAV ist reine Diagnose. Sie erzeugt keinen Entry, keine
      Strategie, kein Gate und keine Rueckwirkung auf das MCM-Feld. DIO hoert
      weiterhin als neuronale Stimulation; die Datei macht diese Hoerspur fuer
      uns pruefbar.
    - Konfiguration: `MCM_MARKET_MELODY_WAV_DEBUG`,
      `MCM_MARKET_MELODY_WAV_MAX_SECONDS`,
      `MCM_MARKET_MELODY_WAV_SAMPLE_RATE`, `MCM_MARKET_MELODY_WAV_GAIN`.
    - Verifikation: `config.py`, `debug_tools/audio_debug.py`,
      `debug_tools/writers.py` und `core/runtime_entry.py` kompilieren
      fehlerfrei.

76. WAV-Hoerspur geglaettet:
    - Befund aus `debug_lauf_15`: Die WAV wurde korrekt erzeugt
      (`11625` Hoerproben, ca. `174s`, Frequenzbereich ca. `1061-7939 Hz`),
      klang aber bei stark komprimierter Backtest-Zeit fragmentiert.
    - Korrektur: Die WAV-Ausgabe interpoliert Frequenz und Lautstaerke jetzt
      weich zwischen zwei Marktproben (`MCM_MARKET_MELODY_WAV_GLIDE_ENABLED`).
    - Fachlich: Nur die Audio-Debug-Ausgabe wird lesbarer. DIOs Hoeren,
      Feldwahrnehmung, Entry-Logik und Regulation bleiben unveraendert.

77. Hypothese als Denkprobe, nicht als Handlungsgrund geschaerft:
    - Fachliche Korrektur: DIO soll nicht aus einer These handeln. Eine These
      ist ein innerer Denkentwurf: "Diese Form koennte so weiterwirken." Sie
      ist keine Realitaet und kein Muskelbefehl.
    - Handlung darf erst entstehen, wenn reale Form, MCM-Wirkung, Erfahrung,
      Realitaetskontakt, innere Zustimmung und oekonomisches Value-Gate
      zusammen tragen.
    - Code-Korrektur: In `bot_gates/entry_decision.py` wurden neue
      Reality-/Probe-Felder ergaenzt:
      `open_hypothesis_reality_probe`,
      `dominant_hypothesis_reality_support`,
      `current_hypothesis_reality_support`, `hypothesis_role`.
    - Alte Felder wie `dominant_hypothesis_action_readiness` und
      `hypothesis_action_support` bleiben nur als Kompatibilitaets-Aliase
      bestehen, damit bestehende Debug-/Stats-Pfade nicht brechen.
    - Debug-Korrektur: Die Entry-Bruecke schreibt jetzt
      `dominant_reality_bearing` und `hypothesis_role=thought_reality_probe`,
      damit die Ausgabe nicht suggeriert, dass eine Hypothese selbst handelt.

78. Backtest-Aussenwelt real getaktet:
    - Einstellung: `WORLD_TIME_SECONDS = 0.1` und
      `BACKTEST_REPLAY_SLEEP_ENABLED = True`.
    - Wirkung: Der Backtest laesst die Aussenwelt jetzt mit 0.1 Sekunden pro
      Marktschritt laufen, statt nur fachliche Candle-Zeitstempel zu nutzen
      und so schnell wie moeglich durchzulaufen.
    - Hinweis: Der Standard-Backtest bleibt synchron
      (`BACKTEST_SYNCHRONOUS_RUNTIME=True`,
      `BACKTEST_WAIT_FOR_RUNTIME_IDLE=True`). DIO verarbeitet also weiterhin
      jede Kerze sauber fertig; die Aussenwelt bekommt nur eine reale
      Abspielgeschwindigkeit.

79. WAV-Zeit an dominante Aussenweltzeit gekoppelt:
    - Befund: `WORLD_TIME_SECONDS` steuerte zwar den realen Backtest-Sleep,
      aber die WAV-Hoerspur nutzte weiter
      `MCM_MARKET_MELODY_WAV_SECONDS_PER_TICK=0.015`. Deshalb klang die
      Audioausgabe trotz langsamerer Aussenwelt fast gleich lang.
    - Korrektur: Die doppelte Einstellung wurde entfernt. Die WAV-Hoerspur
      nutzt jetzt direkt `WORLD_TIME_SECONDS`.
    - Wirkung: Jede gespeicherte Marktprobe wird in der WAV jetzt als
      Ton mit der aktuellen Aussenweltzeit ausgegeben. Bei
      `WORLD_TIME_SECONDS=1.0` wird jede Kerze auch als 1-Sekunden-Ton
      geschrieben; das erzeugt entsprechend grosse und lange WAV-Dateien.
    - Architekturregel: Fuer Sinneswahrnehmung ist `WORLD_TIME_SECONDS`
      dominant. Fuer Denken ist `GLOBAL_COGNITIVE_REACTION_SECONDS`
      dominant. Untergeordnete Module duerfen diese Zeiten lesen, aber keine
      zweite konkurrierende Zeitbasis einfuehren.

80. Zeitgeber bereinigt:
    - Korrektur: Alte aktive Sekundenregler fuer Runtime-Idle, Queue-Polling
      und WAV-Ticks wurden aus der aktiven Konfiguration entfernt.
    - Umsetzung: Technisches Warten in der Runtime nutzt jetzt die innere
      Reaktionszeit `GLOBAL_COGNITIVE_REACTION_SECONDS`; die Marktmelodie nutzt
      die Aussenzeit `WORLD_TIME_SECONDS`.
    - Ziel: Keine asynchrone Nebenrealitaet durch konkurrierende Zeitwerte.
      Sinneswahrnehmung folgt der Weltzeit, Denken folgt der Innenzeit.

81. WAV-Debug als gezielte Hoerprobe:
    - Befund Lauf 22: `samples=14581` bei `WORLD_TIME_SECONDS=0.1`
      ergab `duration_seconds=1458.1`, also ca. 24.3 Minuten. Die Laenge
      ist damit korrekt an die Aussenweltzeit gekoppelt.
    - Korrektur: `MCM_MARKET_MELODY_WAV_DEBUG` ist standardmaessig aus,
      damit normale Backtests keine grossen Audiodateien schreiben.
    - Nutzung: Fuer gezielte Hoerpruefung kann die WAV-Spur bewusst
      aktiviert werden. Sie bleibt Diagnose und hat keine Entry-Wirkung.

82. Sinnes-/Handlungsnaehe nach Lauf 22:
    - Befund: DIO sah sehr haeufig reale Bereichskontakte, aber die
      Handlungsnaehe wurde fast nur ueber Gedanken-/Hypothesen-Kopplung
      getragen. Dadurch wurde Sehen/Fuehlen zu stark von bewusster
      Bestaetigung abhaengig.
    - Korrektur: Die Entry-Bruecke unterscheidet jetzt `thought_area_coupling`,
      `felt_area_coupling` und `sensory_area_coupling`.
    - Bedeutung: Ein Bereich darf nicht nur handeln, weil er gesehen wird.
      Er darf aber auch nicht nur handeln, wenn ein fertiger Gedanke ihn
      bestaetigt. Tragender Form/MCM-Kontakt kann Handlungsnaehe mittragen;
      Denken bleibt bestaetigend oder bremsend.
    - Ziel: Rueckkehr zu einem fuehlenden DIO, ohne in Impuls- oder
      Strategieregel-Trading zurueckzufallen.

83. Lauf 24: Fuehlkopplung war zu direkt:
    - Befund: Nach der Oeffnung stieg die Entry-Annahme deutlich an
      (`inner_action_accepted` stark hoeher, Trades 329), das Ergebnis wurde
      negativ. Damit war Sehen/Fuehlen zwar tragender, aber noch nicht bewusst
      genug von Handlung getrennt.
    - Korrektur: Die Entry-Bruecke fuehrt jetzt zusaetzlich
      `analytic_action_bearing`, `intuitive_action_bearing` und
      `conscious_action_bearing`.
    - Bedeutung: Bauchgefuehl/Kohärenz ist ein eigener Handlungspfad, aber
      kein automatischer Entry. Analyse/Hypothese ist ein zweiter Pfad, aber
      ebenfalls keine Realitaet. Bewusste Handlung entsteht erst, wenn einer
      dieser Pfade tragend genug mit Form/MCM/Realitaetsbindung zusammenpasst.

84. Lauf 26: Konsequenzspur in die Handlungsnaehe zurueckgefuehrt:
    - Befund: Die Oeffnung aus Lauf 24 wurde beruhigt
      (`inner_action_accepted` 380, Trades 202), aber das Ergebnis blieb
      negativ (`pnl_netto=-4.49`). SHORT war positiv, LONG belastend.
    - Diagnose: Viele angenommene Entries hatten noch schwachen realen
      Bereichskontakt (`real_area_contact_bearing` im Mittel ca. 0.16).
      Die Form wurde gespuerter, aber ihre gelernte Konsequenz wirkte noch
      zu wenig auf die innere Zustimmung.
    - Korrektur: Die Entry-Bruecke nutzt jetzt die reale Formkontaktspur aus
      dem Memory: `form_contact_usefulness` und `form_contact_burden`.
    - Wirkung: Nutzbare, gereifte Formkontakte entlasten leicht. Schmerz,
      Burden und Carefulness erhoehen Vorsicht, besonders wenn die bewusste
      Handlungslage noch schwach ist.
    - Wichtig: Das ist kein neues Gate. Es ist eine MCM-Rueckkopplung:
      Konsequenz veraendert Naehe, Vorsicht und Tragfaehigkeit.

85. Sinnesbalance-Protokoll:
    - Ziel: Nach jedem Lauf soll lesbar sein, wie DIO die Sinnesaufteilung
      vertraegt: Sehen, Hoeren, Fuehlen, Denken, Handlung.
    - Umsetzung: `trading/trade_stats.py` schreibt `sensory_balance` in
      `trade_stats.json` und zusaetzlich ein kompaktes
      `mcm_sensory_balance_protocol.json` im Perception-Debugordner.
    - Bedeutung: Das Protokoll veraendert keine Entscheidung. Es zeigt nur,
      ob der Bruch eher bei unscharfer Form, ueberreiztem Hoeren, schwachem
      MCM-Fuehlen, unklarer Hypothese oder fehlender Handlungsnaehe liegt.
    - Fachliche Regel: Sehen, Hoeren und Fuehlen sind Sinnesorgane. Denken
      verdichtet. Handlung entsteht erst bei tragender Kopplung. Das Protokoll
      darf diese Reihenfolge sichtbar machen, aber nicht als Gate benutzen.

86. Prioritaet nach Lauf 33: Sehen, Hoeren, Fuehlen:
    - Befund: Lauf 33 wurde schlechter (`pnl_netto=-4.21`). Die Diagnose zeigt
      keinen Hoer-Ueberreiz, sondern schwache Feldtragfaehigkeit:
      `fuehlen=burdened_field`, `handlung=action_break`.
    - Sehen: Die Formwahrnehmung ist teilweise vorhanden. Das Problem ist
      nicht reine Blindheit, sondern die geringe Kopplung zwischen sichtbarem
      Bereich und realem MCM-Kontakt.
    - Hoeren: Die Marktmelodie bleibt ruhig. Die Fast-Path-Diagnose wurde
      korrigiert, damit `frequency_hz` aus `market_hearing_state` sauber in
      die Sinnesbalance fliesst.
    - Fuehlen: Naechster Arbeitsschwerpunkt ist nicht Entry-Optimierung,
      sondern die Frage, warum gesehene Bereiche innerlich nicht tragen:
      Kontaktkohaerenz, Kontakttragfaehigkeit, Druck-zu-Kapazitaet und
      Ueberkopplung.
    - Grenze: Keine neue Handlungssperre. Die Sinnesorgane sollen klarer
      werden; Handlung bleibt nachgelagert.

87. Reflektive MCM-Feldgrenze:
    - Entscheidung: Das MCM-Feld bleibt ein einfacher Spannungsraum um 0
      (`-3 / 0 / +3`). Es darf nicht mit Rohdaten, Formdaten, Frequenzen,
      Hypothesen oder Orderabsichten gefuellt werden.
    - Sehen bleibt Form/Struktur. Hoeren bleibt Energie/Frequenz/
      Marktspannung. Thought bleibt Hypothese. Handlung bleibt reale Aktion.
    - In das MCM-Feld darf nur die reflektierte Wirkung dieser Schichten:
      Spannung, Auslenkung, Naehe, Distanz, Tragfaehigkeit, Ueberkopplung,
      Nachhall und Rueckfuehrungsdruck.
    - Naechste Code-Pruefung: alle Stellen suchen, an denen `visual_*`,
      `market_hearing_*`, `thought_*`, `hypothesis_*`, `entry_*` oder
      `action_*` direkt als Feldlage, Tragfaehigkeit oder MCM-Kohärenz
      verwendet werden. Diese Stellen muessen in eine klare Uebergabe
      zerlegt werden: Sinneswert -> reflektive Wirkung -> MCM-Feld.

88. Erste Code-Trennung der reflektiven Feldgrenze:
    - Korrektur: `core/mcm_field.py` liest `field_perception_*` nicht mehr
      aus `thought_state`. Gedanken duerfen damit keine Feldwahrnehmung
      ueberschreiben.
    - Korrektur: Im aktiven MCM-Kontakt werden visuelle Klarheit und
      Objektstabilitaet nur noch als reflektierte Werte benutzt:
      `visual_reflective_clarity` und `visual_reflective_stability`.
    - Korrektur: `core/decision_regulation.py` zieht `field_perception_*`
      ebenfalls nicht mehr aus `thought_state`.
    - Befund: `field_action_support` ist weiterhin ein kritischer Altname,
      weil er Feld und Handlung sprachlich mischt. Der Wert darf fachlich nur
      eine gelesene Feldtragfaehigkeit fuer nachgelagerte Regulation sein,
      kein Handlungsbefehl. Spaeter sollte er sauberer getrennt werden, z.B.
      in `field_bearing_support` und `action_readiness`.

89. Feldtragfaehigkeit von Handlungsnaehe getrennt:
    - Umsetzung: `core/decision_regulation.py` erzeugt jetzt
      `field_bearing_support` als saubere MCM-Feldtragfaehigkeit und
      `action_readiness_from_field` als nachgelagerte Uebersetzung Richtung
      Handlung.
    - Kompatibilitaet: `field_action_support` bleibt vorerst als Alias
      bestehen, damit bestehende Pfade nicht abrupt brechen.
    - Anpassung: `core/form_language.py`, `core/possibility_field.py` und
      `core/neurochemistry.py` lesen bevorzugt `field_bearing_support`.
    - Ziel: Das MCM-Feld fuehlt und traegt. Regulation uebersetzt. Handlung
      handelt erst spaeter.

90. Restliche Uebergabeachsen nachgezogen:
    - Anpassung: `core/decision_regulation.py` gibt
      `field_bearing_support` und `action_readiness_from_field` jetzt auch in
      den neurochemischen und bewussten Perzeptionsachsen weiter.
    - Anpassung: Die visuelle Handlungs-Erdung reduziert nur noch
      `action_readiness_from_field`, nicht die eigentliche
      `field_bearing_support`.
    - Anpassung: `MCM_Brain_Modell.py` nutzt fuer
      `packet_bearing_quality` die Feldtragfaehigkeit, nicht den alten
      Handlungsalias.
    - Stand: Die alten Namen bleiben als Kompatibilitaet erhalten, aber die
      fachliche Richtung ist jetzt getrennt: Feldwirkung -> Uebersetzung ->
      Handlungsnaehe.

91. Semantik, Erfahrung und Hypothese entkoppelt:
    - Anpassung: Semantischer Transfer nutzt `field_bearing_support` fuer
      Tragfaehigkeit der Form-/MCM-Beziehung.
    - Anpassung: Unsicherheit, Transferluecken, Erfahrungsfeedback und offene
      Hypothesen modulieren nur `action_readiness_from_field`.
    - Grund: Gedanken, bekannte Formen und Hypothesen duerfen das MCM-Feld
      nicht als Realitaet ueberschreiben. Sie duerfen nur beeinflussen, wie nah
      eine Handlung innerlich kommt.
    - Pruefung: Betroffene Module kompilieren sauber.

92. Vorstufen-Regulator als Pflichtschicht:
    - Entscheidung: Sinneswerte duerfen nicht direkt MCM-Feldlage sein.
      `coherence` bleibt Sehen (`-1 .. +1`), `frequency_hz` bleibt Hoeren,
      Hypothese bleibt Thought.
    - Neue Bauplan-Datei:
      `32_VORSTUFEN_REGULATOR.md`.
    - Code-Pruefung: Direkte `coherence -> mcm_axis` oder
      `frequency_hz -> mcm_axis` Kopplungen wurden in den Kernpfaden nicht
      gefunden. Auffaellig bleiben alte Mischstellen, in denen visuelle
      Variablen in `felt_state`, `neurochemistry` oder
      `decision_regulation` eingehen. Diese sind nicht automatisch falsch,
      muessen aber in den naechsten Schritten als Vorstufen-Regulator oder
      reflektive Kopplung gekennzeichnet bzw. entmischt werden.
    - Wichtig: Das ist kein Gate. Es ist eine organische Reizuebersetzung
      zwischen Sinnesorgan und MCM-Feld.

93. Vorstufen-Regulator im Felt-Pfad begonnen:
    - Umsetzung: `core/felt_state.py` fuehrt `visual_reflective_coherence`
      ein.
    - Bedeutung: `visual_coherence` bleibt Roh-Sehen. Erst ueber
      `visual_mcm_contact_weight` entsteht die Felt-nahe, reflektive
      Kohaerenz.
    - Wirkung: Risiko, Gelegenheit, Stabilitaet, Alignment, aeusserer Druck
      und Unsicherheitsdruck lesen nicht mehr die rohe visuelle Kohaerenz,
      sondern die vorregulierte reflektive Kohaerenz.
    - Wichtig: Keine neue Sperre, kein neues Gate. Die Aenderung trennt nur
      Sinneswert und MCM/Felt-Wirkung sauberer.

94. Vorstufen-Regulator in Regulation und Thought nachgezogen:
    - Pruefung: `core/neurochemistry.py` nutzt visuelle Formdruck- und
      Resonanzwerte bereits ueber `visual_mcm_contact_weight`. Dort wurde
      keine direkte Hoerfrequenz- oder Roh-Kohaerenz-Kopplung auf die
      MCM-Achse gefunden.
    - Umsetzung: `core/decision_regulation.py` nutzt fuer
      visual object binding, Vor-Handlungsbeobachtung, Event-Staerke und
      Thought-Reife jetzt `visual_reflective_coherence`.
    - Bedeutung: DIO darf die sichtbare Form weiterhin sehen und denken, aber
      regulatorisch zaehlt die Form erst, wenn sie reflektiv an Felt/MCM
      gekoppelt ist.
    - Pruefung: `core/decision_regulation.py`, `core/felt_state.py`,
      `core/neurochemistry.py`, `core/perception.py` und
      `MCM_Brain_Modell.py` kompilieren sauber.

95. MCM-Achse auf Skalentrennung geprueft:
    - Befund: `mcm_axis_displacement` war technisch `-1 .. +1`, wurde aber
      sprachlich wie MCM-Feldlage gelesen. Das ist missverstaendlich.
    - Umsetzung: `core/neurochemistry.py` und `core/decision_regulation.py`
      geben jetzt zusaetzlich `mcm_axis_field_position` aus.
    - Bedeutung: `mcm_axis_displacement` bleibt normalisierter Rechenwert.
      `mcm_axis_field_position` ist die eigentliche MCM-Feldposition im Raum

33. Sehen als eigener Sinnesraum analog zum Hoeren.
    - Befund: Hoeren hatte mit `market_hearing_state` bereits eine kompakte
      Sinnesstruktur. Sehen war zwar vorhanden, aber noch zu stark ueber
      verstreute Form-/Corewerte lesbar.
    - Umsetzung: `core/visual_perception.py` gibt jetzt zusaetzlich
      `visual_sight_state` aus.
    - Inhalt: `form_id`, `form_family`, `clarity`, `object_stability`,
      `coherence`, `direction_bias`, `range_position`, `form_pressure`,
      `form_resonance`, `form_fragility`, `depth`, `contact_candidate`,
      `background_load`, `sight_label`.
    - `core/perception.py` reicht diesen Sehzustand weiter.
    - `trading/trade_stats.py` nimmt die wichtigsten Sehfelder in
      `recent_attempts` und `sensory_balance.sehen` auf.
    - Bedeutung: Sehen, Hoeren und Fuehlen sind damit klarer getrennt.
      `visual_sight_state` beschreibt sichtbare Form. Das MCM-Feld bleibt
      die gefuehlte/empfundene Wirkung und wird nicht durch Sehen ersetzt.

34. Visueller Kortex fuer echte Chartobjektbildung.
    - Befund: `visual_sight_state` macht Sehen sichtbar, erkennt aber noch
      keine stabilen Chartobjekte.
    - Umsetzung: neues Modul `core/visual_cortex.py`.
    - `visual_cortex_state` bildet aus Sehzustand, Formachsen und optionaler
      Struktur/Temporalinformation visuelle Objekte:
      `trend_object`, `range_object`, `contact_object`, `compression_object`,
      `break_object`.
    - `core/visual_perception.py` haengt den Kortex an den Sehpfad.
    - `core/perception.py` reicht `visual_cortex_state` weiter.
    - `trading/trade_stats.py` schreibt Kortexwerte in Lean-Stats:
      `visual_cortex_label`, `dominant_visual_object`,
      `visual_object_presence`, `visual_object_clarity`,
      `visual_relation_coherence`, `visual_readiness`.
    - Bedeutung: DIO kann damit nicht nur Form sehen, sondern erste visuelle
      Objekte lesen. Diese Schicht bleibt ausdruecklich keine Entry-Regel.
      `-3 .. 0 .. +3`.
    - Verhalten: Bestehende Regulation bleibt kompatibel, weil keine alte
      Schwelle entfernt wurde.

35. Visueller Kortex um Objektbeziehung und Objektverlauf erweitert.
    - Befund: DIO konnte bereits ein dominantes visuelles Objekt benennen,
      aber noch nicht sauber sagen, wo dieses Objekt liegt und ob es entsteht,
      stabilisiert, Kontakt bekommt, kippt oder sich aufloest.
    - Umsetzung: `core/visual_cortex.py` gibt jetzt
      `visual_object_relation_state` und `visual_object_lifecycle_state` aus.
    - Neue Lesespuren: `visual_relation_label`, `visual_lifecycle_label`,
      `visual_object_side`, `visual_object_distance`,
      `visual_contact_nearness`, `visual_lifecycle_stability`,
      `visual_lifecycle_rejection`, `visual_lifecycle_dissolution` und
      `visual_object_binding_quality`.
    - `core/perception.py` baut den visuellen Kortex jetzt mit Struktur- und
      Zeitinformationen nach, statt nur den fruehen Sehzustand zu uebernehmen.
    - Bedeutung: DIO bekommt mehr visuelle Tiefe, ohne dass daraus ein Gate,
      eine Strategie oder ein Entry-Anker entsteht.

36. Visueller Kortex in Wahrnehmungsbilanz eingebunden.
    - Befund: Die neuen Kortexwerte wurden geschrieben, aber die Regulation
      nutzte sie noch kaum. Dadurch blieb viel Sicht als
      `unformed_visual_background` haengen.
    - Umsetzung: `core/decision_regulation.py` bildet jetzt
      `visual_cortex_grounding` aus Objektbindung, Relation, Klarheit,
      Readiness, Kontaktnaehe und Lebenslauf. Zurueckweisung und Aufloesung
      wirken als Gegenlast.
    - Wirkung: `visual_cortex_grounding` staerkt `visual_object_binding` und
      `visual_grounding_strength`, ohne direkt Entry, MCM-Tragfaehigkeit oder
      Strategie zu erzeugen.
    - Debug: `trading/trade_stats.py` schreibt `visual_cortex_grounding` in
      `recent_attempts` und `sensory_balance.sehen`.

37. Multisensorische Bereichswahrnehmung als eigene Schicht angelegt.
    - Befund: Es gibt bereits `strategic_window_state`, `area_contact_*`,
      `sensory_area_coupling`, `felt_area_coupling` und
      `thought_area_coupling`. Diese Mechaniken beschreiben Bereichskontakt
      und Kopplung, liegen aber teils schon nahe an Entry oder Handlung.
    - Fehlstelle: Es gibt noch keinen sauberen vorgelagerten Zustand, in dem
      DIO einen Marktbereich als sichtbaren, hoerbaren, zeitlichen und gezielt
      gefuehlten Wahrnehmungsraum erlebt.
    - Umsetzung: neues Modul `core/area_perception.py`.
    - Zielzustand: `area_perception_profile` als eigene Schicht zwischen
      Sinneswahrnehmung und MCM-Kontakt.
    - Einbindung: `core/perception.py` reicht das Profil weiter;
      `trading/trade_stats.py` kann die kompakten Werte in Attempts/Stats
      sichtbar machen.
    - Bedeutung: DIO kann einen Bereich erst sehen und hoeren, dann bei
      Bedarf gezielt fuehlen. Das reduziert Dauerueberkopplung und haelt
      Sehen, Hoeren, Fuehlen, Denken und Handeln getrennt.

38. Multisensorische Bereichswahrnehmung kompakt debugbar gemacht.
    - Umsetzung: `core/runtime_entry.py` schreibt optional
      `mcm_area_perception_protocol.csv`.
    - Konfiguration:
      `MCM_AREA_PERCEPTION_PROTOCOL_DEBUG` und
      `MCM_AREA_PERCEPTION_PROTOCOL_EVERY_N`.
    - Debug-Gruppe: `debug_tools/writers.py` ordnet das Protokoll unter
      `perception` ein.
    - Sensory Balance: `trading/trade_stats.py` nimmt den Abschnitt
      `bereich` auf. Dort stehen `area_profile_state`,
      `area_multisensory_coherence`, `area_attention_need`,
      `area_felt_depth` und `area_overcoupling_risk`.
    - Bedeutung: Wir koennen jetzt lesen, ob DIO einen Marktbereich
      multisensorisch erlebt, ohne daraus direkt Entry oder Strategie zu
      machen.
    - Korrektur nach Lauf 12: Zustandswechsel im Area-Protokoll duerfen nicht
      an jede numerische Miniabweichung gekoppelt sein. Das Protokoll schreibt
      jetzt nur bei Profil-/Objekt-/Klangwechsel oder nach Sampling-Intervall.

96. Backtest-Abbruchdiagnose geschaerft:
    - Befund: Die letzten Debug-Laeufe enthielten gueltige Stats und keine
      Traceback-Spur. Das spricht nicht fuer einen klaren Python-Crash,
      sondern fuer fruehes Ende, Timeout, manuellen Abbruch oder unklare
      Fortschrittsanzeige.
    - Umsetzung: `runner.py` schreibt jetzt explizit
      `backtest_processed_windows`, `backtest_total_windows`,
      `backtest_progress`, `backtest_complete` und
      `backtest_stop_reason` in `trade_stats.json`.
    - Wirkung: Wenn DIO wieder scheinbar bei 20 bis 30 Prozent endet, ist
      direkt sichtbar, ob der Feed komplett war, ein Max-Window-Limit griff
      oder eine Exception den Lauf beendet hat.

97. Multisensorischer Bereich an selektiven MCM-Kontakt angeschlossen:
    - Umsetzung: `core/mcm_field.py` liest jetzt `area_perception_profile`
      in `build_active_mcm_contact_state`.
    - Neue Kontaktwerte:
      `area_selective_contact_pull`, `area_selective_feel_permission` und
      `area_selective_feel_risk`.
    - Bedeutung: Ein sichtbarer/hörbarer/zeitlich lokalisierter Bereich kann
      jetzt gezieltes Fühlen anfordern. Das ist keine Entry-Freigabe und kein
      Gate, sondern ein weicher Kontaktreiz für das MCM-Feld.
    - Weitergabe: `core/runtime_entry.py` übernimmt diese Werte in die
      Meta-Schicht, damit Debug und Regulation sehen können, ob ein Bereich
      nur gesehen oder wirklich selektiv gefühlt wurde.
    - Debug: `debug_tools/protocols.py` schreibt die neuen Werte im
      `mcm_active_contact_protocol.csv` mit.
    - Verifikation: `core/mcm_field.py`, `core/runtime_entry.py` und
      `debug_tools/protocols.py` kompilieren fehlerfrei; Smoke-Test erzeugt
      Kontaktzug ohne Handlung.

98. Entry-Plan von festem Bereichsanker auf Kontaktangebote umgestellt:
    - Umsetzung: `trading/trade_plan.py` erzeugt jetzt mehrere
      `entry_contact_options` aus vorhandenen Bereichskandidaten.
    - Auswahl: DIO wählt ein Angebot über gelernte Kontakttragfähigkeit,
      Bereichsfit, Zeitlage, Abstand, Wiederkehr und Belastung. Das ist keine
      starre Regel wie "Kohaerenz hoch = Trade".
    - Neue sichtbare Felder:
      `entry_preference_state`, `entry_choice_basis`,
      `entry_contact_option_count`, `selected_entry_offer_score`,
      `selected_entry_learned_fit`, `contact_learning_state` und
      `learned_contact_fit`.
    - Wichtig: `impulse_role` bleibt `perception_pressure_only`. Impuls darf
      Druck anzeigen, aber keinen Entry-Ort setzen.
    - Weitergabe: `core/runtime_entry.py`, `bot_gates/entry_decision.py` und
      `trading/trade_stats.py` reichen die neuen Felder durch.
    - Verifikation: `trading/trade_plan.py`, `core/runtime_entry.py`,
      `bot_gates/entry_decision.py` und `trading/trade_stats.py` kompilieren
      fehlerfrei; ein direkter Funktionscheck erzeugt mehrere Angebote und
      wählt eines als `learned_multisensory_contact_offer`.

99. Entry-Kontaktpraeferenz aus realer Konsequenz begonnen:
    - Umsetzung: `trading/trade_stats.py` fuehrt
      `entry_contact_learning` als kompakte Folgeerfahrung.
    - Gelernt wird pro Richtung und Kontaktlage, z.B.
      `LONG|long_return_area_upper_contact`.
    - Gespeicherte Werte: `trust`, `caution`, `maturity`, `utility`, Zaehler
      fuer TP/SL/Cancel und kumulative PnL.
    - Persistenz: `memory/memory_state.py` speichert die Spur als
      `entry_contact_preference_memory`; `bot.py` synchronisiert sie nach
      Outcomes aus `TradeStats`.
    - Rueckfuehrung: `trading/trade_plan.py` liest diese Spur und moduliert
      Kontaktangebote weich. Sie ist kein Gate und kein Befehl.
    - Neue sichtbare Felder: `selected_entry_preference_key`,
      `selected_entry_preference_trust`, `selected_entry_preference_caution`,
      `selected_entry_preference_maturity`,
      `selected_entry_preference_utility`.
    - Verifikation: Compile erfolgreich; Smoke-Test zeigt, dass eine
      gespeicherte Kontaktpraeferenz im naechsten Trade-Plan als
      `learned_contact_preference` sichtbar wird.

100. Klassische Ruecksetzer-Semantik aus aktiver Mechanik entfernt:
    - Entry-Kontaktlagen wurden auf neutrale Rueckkehrbegriffe umgestellt:
      `long_return_area_upper_contact` und
      `short_return_area_lower_contact`.
    - Exit-/Target-Begriffe wurden auf `retrace` statt Trading-Strategie-
      Sprache umgestellt.
    - Wichtig: Das ist keine Rueckkehr-Strategie. Es beschreibt nur eine
      raeumlich-zeitliche Kontaktlage.
    - Architekturregel festgehalten: DIO hat kein vorprogrammiertes
      Entry-System. Kontakt, Klang, Kohaerenz, Feldwirkung und Bereich sind
      Wahrnehmungen, keine Entry-Befehle.

101. Kontaktangebot von konkreter Entry-Geometrie getrennt:
    - Umsetzung: `trading/trade_plan.py` erzeugt weiter
      `entry_contact_options`, aber ein Kontaktangebot wird erst dann zu
      `entry_price`/SL/TP, wenn eine interne Geometrie-Kopplung entsteht.
    - Neue sichtbare Werte:
      `entry_geometry_state`, `entry_geometry_bearing`,
      `pre_geometry_thought_bearing`, `pre_geometry_felt_bearing`,
      `pre_geometry_reality_bearing` und
      `pre_geometry_preference_bearing`.
    - Fachlich: Bereichskontakt bleibt Wahrnehmung. Konkrete Order-Geometrie
      entsteht erst aus Kopplung von Denken, Fuehlen, Realitaetsbindung und
      gelernter Kontaktpraeferenz.
    - Wichtig: Das ist kein neues hartes Gate, sondern die Trennung zwischen
      "ich sehe eine Moeglichkeit" und "ich habe genug innere Tragnaehe fuer
      einen konkreten Entry-Ort".

102. Entry-Geometrie nach Null-Trade-Befund organischer geoeffnet:
    - Befund: Nach Punkt 101 entstanden bei ca. 70 Prozent Laufstand keine
      Trades. Die Trennung war fachlich richtig, aber zu eng: reifende
      Kontaktangebote wurden nicht mehr zu sichtbarer Handlung.
    - Korrektur: `trading/trade_plan.py` fuehrt
      `organic_contact_bearing`. Damit kann ein starker multisensorischer
      Kontakt auch ohne volle Thought-/Memory-Bestaetigung eine kleine
      Entry-Geometrie bilden.
    - Wichtig: Impuls bleibt weiter `perception_pressure_only`. Es wurde kein
      Impulstrading reaktiviert.

103. Sinneskanäle synchronisiert:
    - Befund: Sehen, Hoeren und Fuehlen konnten fachlich zu additiv wirken.
      Dadurch konnte ein lauter Klang oder starker Feldkontakt die
      Bereichskohaerenz erhoehen, obwohl die sichtbare Form nicht passend
      gebunden war.
    - Umsetzung: `core/area_perception.py` fuehrt eine
      `sensory_sync_state` mit `visual_hearing_fit`, `visual_felt_fit`,
      `hearing_felt_fit`, `temporal_visual_fit`, `sensory_sync`,
      `sensory_desync_pressure` und `multisensory_binding_state`.
    - Wirkung: Hoeren, Zeit und Fuehlen staerken die
      `area_multisensory_coherence` nur noch gebunden. Bei Desynchronisation
      steigt Aufmerksamkeit/Überkopplungsrisiko statt blinder Handlungsnaehe.
    - Weitergabe: `core/perception.py`, `core/mcm_field.py` und das
      `mcm_area_perception_protocol.csv` tragen die neuen Werte.

104. Entry-Bridge-Diagnose um Geometrie-Kopplung erweitert:
    - Befund nach zwei Läufen: Sinnesbindung ist stabil, aber die Bridge
      reframed sehr häufig mit `area_contact_needs_thought_coupling`.
    - Umsetzung: `bot_gates/entry_decision.py` schreibt jetzt in
      `entry_debug.csv` zusätzlich `entry_geometry_state`,
      `entry_geometry_bearing`, `organic_contact_bearing`,
      `pre_geometry_thought_bearing`, `pre_geometry_felt_bearing`,
      `pre_geometry_reality_bearing` und
      `pre_geometry_preference_bearing`.
    - Ziel: Im nächsten Lauf ist sichtbar, ob der Engpass vor der Bridge
      in der Geometriebildung liegt oder innerhalb der Thought-/Consent-
      Kopplung.

105. Thought-Seed an Entry-Geometrie angebunden:
    - Befund: `organic_contact_bearing` war vorhanden, aber
      `pre_geometry_thought_bearing` blieb praktisch leer. DIO konnte einen
      Bereichskontakt sehen/fuehlen, aber die eigene Denkspur trug diesen
      Kontakt vor der Entry-Geometrie nicht mit.
    - Umsetzung: `trading/trade_plan.py` liest jetzt den vorhandenen
      `mcm_thought_seed_state` direkt in die Vor-Geometrie.
    - Neue Debugspur: `thought_seed_bearing`.
    - Wichtig: Hypothese bleibt Deutung, nicht Realitaet. Die Korrektur
      stellt nur die fehlende Verbindung zwischen eigenem Gedankenkeim und
      realem Bereichskontakt her.
    - Verifikation: `python -m py_compile trading/trade_plan.py
      bot_gates/entry_decision.py` erfolgreich.

106. Diagnose nach Lauf `debug_lauf_22`:
    - Ergebnis: 39 Trades, 11 TP, 28 SL, PnL netto ca. -2.71.
    - Der Lauf zeigte noch keine `thought_seed_bearing`-Spur in
      `entry_debug.csv`; damit war die neue Diagnose im Lauf noch nicht
      eindeutig sichtbar.
    - Reframes: `area_contact_needs_thought_coupling` blieb dominant.
    - Nachgezogen: `bot_gates/entry_decision.py` schreibt die
      Geometrie-/Thought-Seed-Felder jetzt auch direkt in den
      `inner_action_reframed`-Bridge-Zweig.
    - Verifikation: `python -m py_compile trading/trade_plan.py
      bot_gates/entry_decision.py` erfolgreich.

107. Diagnose nach Lauf `debug_lauf_23`:
    - Ergebnis: 21 Trades, 5 TP, 16 SL, PnL netto ca. -2.73.
    - Reframes: `area_contact_needs_thought_coupling` blieb dominant.
    - `thought_seed_bearing` war jetzt sichtbar, blieb aber durchgehend 0.
    - `pre_geometry_thought_bearing` kam nur indirekt aus Meta-Werten.
    - Befund: Der Kontakt war organisch da, aber die aktuelle Denk- und
      Reifeschicht wurde nicht direkt in den Trade-Plan getragen.
108. Schnittstelle Thought -> Trade-Plan geschlossen:
    - `trading/trade_plan.py` nimmt jetzt optional `thought_state` entgegen.
    - `core/runtime_entry.py` und `MCM_Brain_Modell.py` uebergeben die
      aktuelle `thought_state` an den Trade-Plan.
    - `thought_seed_bearing` wird jetzt aus Thought-Seed oder aktueller
      Thought-Reife gebildet.
    - `core/runtime_entry.py` uebernimmt `thought_seed_bearing` in das
      Entry-Result.
    - Verifikation: `python -m py_compile trading/trade_plan.py
      core/runtime_entry.py MCM_Brain_Modell.py bot_gates/entry_decision.py`
      erfolgreich.

109. Diagnose nach Lauf `debug_lauf_24`:
    - Ergebnis: 35 Trades, 12 TP, 23 SL, PnL netto ca. +1.09.
    - Gegenueber Lauf 23 wurde die Thought-Kopplung sichtbar wirksam:
      `thought_seed_bearing`/`pre_geometry_thought_bearing` lagen im
      Entry-Pfad deutlich ueber 0.
    - Die Bridge blieb jedoch haeufig bei
      `area_contact_needs_thought_coupling`, also ist noch nicht jede
      gesehene Kontaktnaehe bewusst getragen.
    - Hochwertige Strukturkontakte trugen den Lauf:
      `confirmed_structural_interpretation` war positiv, offene Hypothesen
      blieben belastend.
110. Diagnosebenennung geschaerft:
    - `thought_seed_bearing` beschreibt wieder nur den eigentlichen
      Thought-Seed.
    - `thought_state_bearing` beschreibt aktuelle Denk-/Reifefaehigkeit.
    - `thought_contact_bearing` ist die wirksame Kopplung fuer die
      Vor-Geometrie.
    - Verhalten bleibt fachlich gleich, aber die Diagnose trennt echte
      Gedankenkeime von allgemeiner Denkfaehigkeit.
    - Verifikation: `python -m py_compile trading/trade_plan.py
      core/runtime_entry.py bot_gates/entry_decision.py MCM_Brain_Modell.py`
      erfolgreich.

111. Diagnose nach Lauf `debug_lauf_25`:
    - Ergebnis: 26 Trades, 6 TP, 20 SL, PnL netto ca. -4.37.
    - Die getrennte Diagnose zeigte:
      `thought_seed_bearing` blieb niedrig, waehrend
      `thought_state_bearing` hoch war.
    - Befund: DIO hatte situative Denk-/Reifefaehigkeit, aber zu wenig
      bestaetigte Gedanken-Erfahrung. Offene Hypothesen wurden dadurch zu
      stark von aktueller Denkfaehigkeit getragen.
112. Thought-State als Traeger, nicht als Ersatz fuer Erfahrung:
    - `thought_contact_bearing` wird nicht mehr als Maximum aus Seed und
      State gebildet.
    - Neue weiche Kopplung:
      `thought_state_carrier_factor` bestimmt, wie stark aktuelles Denken
      ohne echten Seed tragen darf.
    - Echte Seeds erhoehen diesen Traeger. Ohne Seed bleibt Denken eher
      Reifung/Beobachtung und ersetzt keine bestaetigte Erfahrung.
    - Verifikation: `python -m py_compile trading/trade_plan.py
      core/runtime_entry.py bot_gates/entry_decision.py MCM_Brain_Modell.py`
      erfolgreich.

113. Diagnose nach Lauf `debug_lauf_26`:
    - Ergebnis: 32 Trades, 12 TP, 20 SL, PnL netto ca. +3.78.
    - Die weiche Traeger-Kopplung stabilisierte den Lauf deutlich.
    - `thought_state_bearing` blieb hoch, aber `thought_contact_bearing`
      wurde durch `thought_state_carrier_factor` deutlich niedriger getragen.
    - Hochwertige Strukturkontakte waren stark positiv:
      `confirmed_structural_interpretation` 11 TP / 0 SL.
    - Offene Hypothesen blieben das Hauptproblem:
      `open_structural_hypothesis` 0 TP / 16 SL.
114. Offene Hypothesen bekommen Kontaktvorsicht:
    - Neue weiche Groesse: `hypothesis_contact_restraint`.
    - Sie senkt Entry-Geometrie und organische Kontaktnaehe, wenn eine
      offene Hypothese Beobachtungsdruck, wenig Seed oder belastete
      Hypothesenerfahrung traegt.
    - Das ist kein Gate. Offene Hypothesen werden nicht verboten, sondern
      brauchen mehr Reife/Bestätigung, um zu konkreter Entry-Geometrie zu
      werden.
    - Verifikation: `python -m py_compile trading/trade_plan.py
      core/runtime_entry.py bot_gates/entry_decision.py MCM_Brain_Modell.py`
      erfolgreich.
115. Diagnose nach aktuellem Lauf:
    - Im neuesten Debug-Lauf war die Entry-Bridge deutlich aktiver als zuvor:
      viele Kontakte wurden gesehen, aber meist als
      `area_contact_needs_thought_coupling` zurückgeführt.
    - Die angenommenen Entries hatten höhere Kopplung, höhere bewusste
      Zustimmung und stärkere reale Bereichsnähe als die zurückgeführten
      Kontakte.
    - Kernbefund: Die spätere Auswertung erkennt offene Hypothesen und
      bestätigte Struktur nach TP/SL, der Trade-Plan hatte diese
      Strukturdeutung vor dem Entry aber noch nicht ausreichend verfügbar.
116. Vor-Entry-Strukturdeutung ergänzt:
    - `trading/trade_plan.py` bildet jetzt vor dem Entry eine weiche
      Vorab-Deutung:
      `pre_entry_emergent_structure_reading`,
      `pre_entry_emergent_structure_confirmation`,
      `pre_entry_emergent_structure_state`.
    - Diese Vorab-Deutung nutzt reale Bereichs-/MCM-/Zeit-/Kontaktwerte und
      klassifiziert nur die Reife-Tendenz: bestätigte Struktur, offene
      Hypothese, normale Lesung oder nicht lokalisierte Weite.
    - Offene Hypothesen erzeugen dadurch vor der Handlung mehr
      `hypothesis_contact_restraint`; bestätigte Struktur bekommt mehr
      Realitätsbezug. Das bleibt eine weiche Regulation, kein Gate.
    - `bot_gates/entry_decision.py` nutzt diese Vorab-Deutung als
      Ergänzung, wenn der Thought-Seed selbst noch keine klare
      Strukturklasse trägt.
    - Verifikation: `python -m py_compile trading/trade_plan.py
      bot_gates/entry_decision.py` erfolgreich.
117. Diagnose nach Lauf `debug_lauf_28`:
    - Ergebnis: 18 Trades, PnL netto ca. -6.05.
    - Die neue Vor-Entry-Deutung war im Bridge-Debug sichtbar, aber
      `pre_entry_emergent_structure_reading` und
      `pre_entry_emergent_structure_confirmation` blieben bei 0.
    - Ursache: `trading/trade_plan.py` berechnete die Felder, aber
      `core/runtime_entry.py` übernahm sie nicht in den Decision-State.
      Die Entry-Bridge erhielt dadurch nur Defaultwerte.
118. Übergabe Vor-Entry-Deutung geschlossen:
    - `core/runtime_entry.py` übernimmt jetzt
      `pre_entry_emergent_structure_reading`,
      `pre_entry_emergent_structure_confirmation` und
      `pre_entry_emergent_structure_state` aus dem Trade-Plan.
    - Erwartung für den nächsten Lauf: Die Bridge kann offene/tragende
      Struktur vor dem Entry tatsächlich sehen; erst danach ist die Wirkung
      von `hypothesis_contact_restraint` sinnvoll bewertbar.
    - Verifikation: `python -m py_compile trading/trade_plan.py
      core/runtime_entry.py bot_gates/entry_decision.py MCM_Brain_Modell.py`
      erfolgreich.
119. Form-MCM-Gedanken-Kopplung als Realitaetsbindung ergaenzt:
    - `trading/trade_plan.py` berechnet jetzt weich:
      `visual_reality_bearing`, `felt_reality_bearing`,
      `thought_reality_bearing`, `form_mcm_reality_fit`,
      `hypothesis_reality_binding` und
      `hypothesis_reality_binding_gap`.
    - Zweck: Hypothesen werden nicht als Realitaet behandelt. Sie werden
      nur tragender, wenn sichtbare Form, MCM-Feldwirkung und Gedankenlage
      zusammenpassen.
    - `bot_gates/entry_decision.py` fuehrt diese Werte in Entry-Result und
      `entry_debug.csv`, damit sichtbar wird, ob DIO koppelt, beobachtet
      oder im Gedanken vorauslaeuft.
    - `DIO_BAUPLAN/konstruktion/06_REALITAETSPRUEFUNG.md` beschreibt diese
      Kopplung als Realitaetsbindung, nicht als Gate.
    - Verifikation: `python -m py_compile trading/trade_plan.py
      bot_gates/entry_decision.py MCM_Brain_Modell.py` und
      `python -m compileall -q .` erfolgreich.
120. Uebergabe der Realitaetsbindung geschlossen:
    - Diagnose aus `debug_lauf_37`: 0 Trades, viele Beobachtungen, aber
      `hypothesis_reality_binding`, `visual_reality_bearing`,
      `felt_reality_bearing`, `thought_reality_bearing` und
      `form_mcm_reality_fit` blieben im Entry-Debug bei 0.
    - Ursache: `trading/trade_plan.py` gab die Werte aus, aber
      `core/runtime_entry.py` uebernahm sie nicht in den Runtime-Entry-State.
    - Korrektur: `core/runtime_entry.py` uebernimmt und synchronisiert diese
      Felder jetzt. Damit kann das Entry-Gate die Kopplung tatsaechlich sehen.
    - Verifikation: `python -m py_compile core/runtime_entry.py
      trading/trade_plan.py bot_gates/entry_decision.py MCM_Brain_Modell.py`
      und `python -m compileall -q .` erfolgreich.
121. MCM-Aktivitaetsinseln relativ zur Feldpopulation kalibriert:
    - Diagnose aus `debug_lauf_38`: Die Sinne waren gebunden
      (`bound_multisensory_area`), aber das MCM-Feld blieb bei
      `quiet_field` mit 0 Aktivitaetsinseln.
    - Ursache: Die Insel-Erkennung nutzte einen absoluten Schwellwert
      von 0.26. Nach der Umstellung auf 120 Neuronen verteilte sich die
      Aktivierung sauberer; der maximale Neuronenwert lag darunter. Dadurch
      konnte trotz Struktur keine lokale Aktivitaetsinsel entstehen.
    - Korrektur: `core/mcm_model.py` nutzt jetzt eine adaptive, relative
      Insel-Erkennung. Das Feld vergleicht Neuronenaktivitaet gegen die
      aktuelle Feldpopulation statt nur gegen einen festen Absolutwert.
    - Neue Diagnosewerte:
      `activity_island_threshold_mode`, `activity_island_threshold`,
      `activity_score_mean`, `activity_score_max`, `activity_score_p90`.
    - Fachlich: Das ist keine neue Handlungssperre und kein Entry-Gate,
      sondern eine Wahrnehmungskalibrierung des MCM-Feldes.
122. Visuelle Formspur als echte neuronale Sinnesbahn ergaenzt:
    - Befund: Hoeren hatte bereits eine eigene neuronale Spur
      (`auditory_impulse`, `auditory_aftertone`, `auditory_resonance`).
      Sehen wirkte zwar ueber Vorregulator/Felt-State, aber noch nicht
      gleichwertig als Neuronenspur.
    - Korrektur: `core/mcm_model.py` fuehrt jetzt eine visuelle
      Neuronenspur:
      `visual_impulse`, `visual_afterimage`, `visual_resonance` und
      `visual_neural_state`.
    - `MCM_Brain_Modell.py` leitet die aktuelle `visual_market_state` in den
      MCM-Stimulus und an das Feld weiter.
    - `debug_tools/field_snapshots.py` protokolliert neue Mittelwerte:
      `neuron_visual_impulse_norm_mean`,
      `neuron_visual_resonance_mean`,
      `neuron_visual_afterimage_norm_mean`.
    - Fachlich: Sehen stimuliert nun wie Hoeren die MCM-Neuronen, erzeugt
      aber keine Handlungserlaubnis. `visual_neural_action_permission` bleibt
      bewusst 0.0. Handlung entsteht erst nach tragender Kopplung.
123. Visuelle Kopplung nach Laufbefund weicher gestellt:
    - Befund aus `debug_lauf_41`: Die visuelle Neuronenspur war messbar
      aktiv (`visual_impulse`, `visual_resonance`, `visual_afterimage`),
      aber die Feldspannung stieg deutlich. DIO sah mehr, das MCM-Feld
      trug den Kontakt jedoch nicht stabil genug.
    - Korrektur: Die visuelle Grundskala und die direkte Kopplung in die
      Feldbewegung wurden reduziert. Sehen bleibt Sinnesreiz und
      Nachbild, soll aber das Feld nicht ueberfahren.
    - Fachlich: Das ist keine Handelsregel. Es ist eine organischere
      Kopplung der Sinnesbahn: erst sehen, nachhallen lassen, dann ueber
      MCM-Fuehlen und Reife in Handlung naeher kommen.
124. Hypothese darf nicht als Realitaet handeln:
    - Befund aus `debug_lauf_42`: Der einzige echte Entry entstand, obwohl
      der Plan selbst `pre_entry_open_structure_observation` und
      `seen_form_needs_feeling` meldete. Die Hypothese wollte also
      Beobachtung, wurde aber trotzdem in eine Order ueberfuehrt.
    - Korrektur: `MCM_Brain_Modell.py` fuehrt solche offenen
      Strukturhypothesen jetzt als `WAIT/observe` zurueck. Der gedachte
      Entry bleibt als virtueller Beobachtungsplan erhalten, wird aber
      nicht als reale Handlung ausgefuehrt.
    - Fachlich: Das ist kein zusaetzliches Value-Gate. Es ist die
      Trennung von Gedanke und Realitaet: "Ich sehe etwas und denke eine
      Moeglichkeit" ist nicht automatisch "ich handle".
125. Beobachtung bleibt im Entry-Gate Beobachtung:
    - Befund aus `debug_lauf_45` auf kurzem Datensatz: 0 Trades, aber 641
      `MCM_ENTRY_BRIDGE`-Zeilen mit `side=WAIT`, `tendency=act` und
      `hypothesis_requires_reality_observation`.
    - Ursache: `MCM_Brain_Modell.py` gab offene Strukturhypothesen korrekt
      als `decision_tendency=observe` zurueck, aber
      `bot_gates/entry_decision.py` verwendete danach noch die alte
      Runtime-Tendenz `act` aus dem ersten Tendenzblick.
    - Korrektur: Das Entry-Gate liest nach `decide_mcm_brain_entry()` die
      finale Tendenz erneut. `observe`, `hold` und `replan` werden nun als
      Nicht-Handlung zurueckgegeben und laufen nicht mehr als ungueltiger
      `WAIT`-Entry durch die Orderlogik.
    - Fachlich: Die Trennung bleibt weich und organisch: DIO darf eine
      Handlung denken, aber wenn die Realitaetsbindung Beobachtung verlangt,
      bleibt es Beobachtung. Der Value-Gate-Bereich bleibt davon unberuehrt.
126. Rueckfuehrung vom Strategiepfad zur rezeptiven Kopplung:
    - Befund: Im Entry-Consent wirkten `hypothesis_trust_*` und alte
      `strategy_*`-Aliases wieder zu stark handlungsbildend. Dadurch konnte
      DIO vom rezeptiven Wahrnehmen in eine strategische Deutung kippen.
    - Korrektur: `bot_gates/entry_decision.py` fuehrt jetzt
      `thought_reality_coupled_bearing` und `receptive_contact_bearing`.
      Gedanken/Hypothesen koennen Handlung nur noch mittragen, wenn reale
      Kontaktnaehe, MCM-Fuehlen und Formbindung bereits gekoppelt sind.
    - Alte `strategy_*`-Felder werden im Consent neutral gehalten und als
      Debug-/Kompatibilitaetsalias markiert. Sie treiben die Handlung nicht
      mehr.
    - Fachlich: Das ist die Rueckkehr zur DIO-Basis: Sehen, Hoeren, Fuehlen
      und reale Kontaktnaehe kommen vor Denken-als-Handlung. Strategie darf
      nur als spaetere Folge gereifter Erfahrung sichtbar werden, nicht als
      eingebauter Motor.
127. WAIT bleibt Nicht-Handlung:
    - Befund aus `debug_lauf_46`: `WAIT` mit
      `hypothesis_requires_reality_observation` lief noch als `act` in die
      Entry-Bridge und endete als `invalid_trade_direction`.
    - Ursache: Die finale Entscheidung war bereits Beobachtung, aber der
      alte Tendenzpfad trug noch `act` aus dem vorherigen Laufweg.
    - Korrektur: `bot_gates/entry_decision.py` behandelt
      `WAIT + hypothesis_requires_reality_observation` jetzt explizit als
      `observe`. Andere `WAIT`-Rueckgaben werden als `hold` gefuehrt.
      Dadurch bleibt eine offene Hypothese im Beobachtungsraum und wird
      nicht als ungueltiger Entry verarbeitet.
    - Fachlich: Das ist kein Gate und keine Handelsregel, sondern saubere
      Realitaetstrennung: Gedachte Moeglichkeit bleibt Gedanke, bis reale
      Kontaktnaehe und MCM-Kopplung eine Handlung tragen.
128. Rueckschnitt des Denkens aus der Motorik:
    - Befund: Nach dem grossen Umbau hing Denken zu stark an Entry,
      Handlungsnaehe und Regulation. Dadurch kippte DIO zwischen
      Uebertrading und vollstaendiger Hemmung.
    - Korrektur: `trading/trade_plan.py` nutzt Thought/Hypothese nicht mehr
      als Entry-Geometrie-Treiber. `bot_gates/entry_decision.py` setzt
      `thought_motor_bearing` und `thought_motor_pressure` auf neutral.
      `MCM_Brain_Modell.py` fuehrt offene Hypothesen nicht mehr in einen
      eigenen No-Plan-Abzweig.
    - Fachlich: Denken bleibt Diagnose, Beobachtung, Nachhall und
      spaeterer Lernstoff. Handlung entsteht wieder aus rezeptiver Kopplung:
      Sehen, Hoeren, MCM-Fuehlen, reale Kontaktnaehe und Value-Gate.
    - Ziel des naechsten Laufs: pruefen, ob DIO wieder handlungsfaehiger wird
      und ob die Tradezahl ohne reflexives Uebertrading ansteigt.
129. Offene Strukturhypothese reift vor Handlung:
    - Befund aus `debug_lauf_49`: DIO war wieder handlungsfaehig, aber
      offene Strukturhypothesen erzeugten den Hauptverlust. Bestaetigte
      Strukturdeutung war dagegen stark tragend.
    - Korrektur: `trading/trade_plan.py` fuehrt
      `open_structure_contact_maturity`. Offene Hypothesen duerfen weiter als
      Kontaktangebot erscheinen, werden aber weich komprimiert, wenn
      sichtbare Form, MCM-Fuehlen, reale Kontaktnaehe und Erfahrung noch
      nicht gemeinsam tragen.
    - Fachlich: Das ist kein neues Gate und keine Strategie. Es trennt
      gedachte Moeglichkeit von gereiftem Kontakt. DIO darf eine Form sehen
      und eine Moeglichkeit spueren, aber Handlung entsteht erst, wenn der
      Kontakt im Feld reift.
    - Ziel des naechsten Laufs: weniger SL-lastige offene Hypothesentrades,
      ohne bestaetigte Strukturkontakte zu verlieren.
130. Hypothese vorerst aus Handlung entfernt:
    - Entscheidung: Die weiche Reifung reicht fuer den aktuellen Rueckbau
      nicht aus. Hypothese wird vorerst ganz aus Entry-Motorik und
      Entry-Consent genommen.
    - Korrektur: `trading/trade_plan.py` setzt Hypothesenfelder vor der
      Entry-Geometrie auf neutral. `bot_gates/entry_decision.py` neutralisiert
      Hypothesen im Consent, bevor Handlungsnaehe berechnet wird.
    - Fachlich: DIO handelt damit wieder aus rezeptiver Kopplung: Sehen,
      Hoeren, MCM-Fuehlen, reale Bereichsnaehe, Kontaktreife und Value-Gate.
      Thought/Hypothese bleibt Debug-, Erinnerungs- und Analyseebene, aber
      keine Handlungsquelle.
    - Ziel des naechsten Laufs: pruefen, ob DIO ohne Hypothesenmotorik wieder
      organischer handelt und ob die SL-lastigen offenen Gedankentrades
      verschwinden.
131. Hypothese als Beobachtungslernen:
    - Erkenntnis: Ein rein rezeptives System wird stabil, aber es verbessert
      sich nur begrenzt, wenn es keine Konsequenz aus Handlung oder
      beobachteter Fortsetzung erlebt.
    - Korrektur: Hypothese bleibt als beobachtende Fortsetzung erhalten:
      "Ich sehe diese Form; vielleicht laeuft sie so weiter." Die reale Welt
      bewertet diese Fortsetzung spaeter als getragen, verletzend, neutral
      oder reorganisierend.
    - Umsetzung: `Config.MCM_HYPOTHESIS_ACTION_INFLUENCE_ENABLED = False`.
      `core/review_feedback.py` berechnet Rohwerte wie
      `raw_possibility_action_support`, setzt daraus aber keine aktive
      `possibility_action_support` und keine `hypothesis_action_bearing`.
    - Fachlich: Das ist Lernen ohne Motorik. DIO sammelt hypothetische
      Erfahrung, aber Entry entsteht aktuell nur aus Sinnes-/MCM-Kopplung und
      Value-Gate. Eine spaetere Rueckfuehrung in Handlung muss explizit,
      kontrolliert und nach Reife erfolgen.
132. Rezeptiver Explorationskontakt nach frischem Memory:
    - Befund aus `debug_lauf_1`: Nach geloeschtem Memory sah DIO reale
      Bereichskontakte, aber setzte `0` Trades. Alle dokumentierten
      Entry-Kontakte wurden zu `observe` reframed.
    - Ursache: `form_contact_usefulness`, `form_contact_burden` und gelernte
      Kontaktpraeferenz waren leer. Ohne Hypothesenmotorik fehlte damit der
      koerperliche Erstkontakt, aus dem reale Konsequenz lernen kann.
    - Korrektur: `bot_gates/entry_decision.py` fuehrt
      `receptive_exploration_bearing`. Dieser Wert entsteht nur aus realem
      Bereichskontakt, organischem Kontakt, Form/MCM-Fit, visueller
      Realitaetsnaehe und gefuehlter Kopplung.
    - Fachlich: Das ist keine Strategie und kein Gate. Es ist eine weiche
      Lern-Startschicht, damit ein frisches Gedaechtnis vorsichtig reale
      Konsequenzen sammeln kann, ohne Thought/Hypothese als Motor zu nutzen.
133. Aktive Hypothesenbildung im fuehlenden Kern deaktiviert:
    - Entscheidung: Hypothesen werden vorerst nicht mehr gebildet, gereift,
      gespeichert oder als Moeglichkeitsfeld in Regulation und Entry
      zurueckgefuehrt.
    - Umsetzung:
      `MCM_THOUGHT_MEMORY_ENABLED = False`,
      `MCM_HYPOTHESIS_LEARNING_ENABLED = False`,
      `MCM_HYPOTHESIS_ACTION_INFLUENCE_ENABLED = False`.
    - Nachgezogene Pfade:
      `core/hypothesis_learning.py`,
      `core/possibility_field.py`,
      `core/runtime_entry.py`,
      `bot_engine/idle_thinking_protocol.py`.
    - Fachlich: DIO wird wieder als fuehlender, rezeptiver Organismus
      getestet. Handlung entsteht nicht aus Gedanken-Strategie, sondern aus
      Sinnes-/MCM-Kopplung, realer Kontaktnaehe, Erfahrung und Value-Gate.
    - Naechster Lauf: pruefen, ob DIO weniger Denklast zeigt und ob die
      Handlungsnaehe wieder aus Energie, Feld und Kontakt entsteht.
134. Mini-DIO: innere Semantikmatrix aus Emergenz:
    - Befund aus den passiven Cluster-Lupen: `dio_0x52` wirkt als gereifter
      Kern einer Bedeutungsinsel. `dio_1rv1` und `dio_1jgc` wirken nicht wie
      fertige Regeln, sondern wie rohe Varianten, Erweiterungen oder
      Satzfragmente im selben inneren Bedeutungsraum.
    - Grenze: Das ist keine Halluzination und kein selbststaendiges Denken im
      starken Sinn. Es ist Matrixbildung aus emergenten Mustern, die aus
      Erleben, Wiederkehr, Feldlage und Konsequenz entstehen.
    - Fachliche Verdichtung:
      getragener Zustand -> wiederkehrende Syntaxspur -> Bedeutungsinsel ->
      Satzbildung / Zusammenhang -> getragenes Erlebnis -> wachsende innere
      semantische Matrix.
    - Wirkung: Diese Matrix bleibt passiv. Sie schreibt keine aktive Runtime,
      erzeugt keine Handlung, kein Gate, keine Richtung und keinen Entry.
    - Ziel: Mini-DIO soll spaeter lernen koennen, innere Syntaxinseln zu
      festigen, zu kombinieren, zu erweitern, zu teilen und zu ordnen, ohne
      dass daraus mechanische Strategie entsteht.
135. Passive Semantikmatrix als Diagnosemodul:
    - Umsetzung: `DIO_MINI/report_passive_semantic_matrix.py` kombiniert
      Meaning-Space-Knoten und Neighbor-Kanten zu passiven Bedeutungsinseln.
    - Ergebnis aus `debug/dio_mini_passive_semantic_matrix_probe20_26_v1`:
      `dio_semantic_island_1` verbindet `dio_0x52` als gereiften Kern mit
      `dio_1rv1` und `dio_1jgc` als rohen Erweiterungen. Die
      durchschnittliche Bedeutungsnaehe liegt bei `0.989814`.
    - Grenze: Bericht bleibt passiv. Keine Runtime-Lesung, keine Handlung,
      kein Gate, kein Entry, keine Richtung.
136. Reproduktionspruefung der passiven Semantikmatrix:
    - Vorgehen: Probe20 bis Probe26 wurden mit frischem, getrenntem Memory
      erneut ausgefuehrt. Danach wurden Meaning-Space, Neighbor-Matrix und
      Semantikmatrix ohne Candidate-Reifeuebernahme neu erzeugt.
    - Ergebnis:
      Referenz-Knoten `78`, Repro-Knoten `78`, gemeinsame Knoten `78`.
      Referenz-Kanten `196`, Repro-Kanten `234`, gemeinsame Kanten `186`.
      Referenz-Inseln `13`, Repro-Inseln `11`.
    - Lesart: Die Syntaxstruktur reproduziert sich vollstaendig. Die
      Bedeutungsnaehen reproduzieren sich weitgehend und bilden im frischen
      Lauf eine dichtere Matrix mit weniger, groesseren Inseln.
    - Grenze: Der frische Lauf zeigt rohe Bedeutungsinseln, keine uebernommene
      Reife. Das ist gewollt, weil keine alte Candidate-Reife importiert wurde.
    - Debug:
      `debug/dio_mini_passive_semantic_matrix_compare_probe20_26_vs_repro_20260606_v1`.
137. Theorieanker fuer emergentes Gedaechtnis:
    - Abgleich mit MCM Pure Emergence, MCM Robustness und MCM 3D Emergence:
      Mini-DIOs reproduzierte Syntax- und Bedeutungsinseln passen zur
      MCM-Lesart, dass Ordnung aus lokaler Dynamik, Feldkopplung, Rauschen,
      Dichte und Wiederkehr entsteht.
    - Fachliche Uebertragung: `dio_*`-Spuren koennen als kondensierte
      Feldspuren gelesen werden. Bedeutungsinseln sind semantische
      Dichtezentren, nicht Regeln.
    - Wichtige Grenze: Das ist keine Halluzination und kein freies Denken.
      Es ist passive Matrixbildung aus wiederkehrendem Erleben.
    - Naechste passive Diagnoseachse:
      `semantic_density`, `variant_attraction`, `island_growth`,
      `island_fragmentation`, `density_reproduction`, `semantic_vorticity`.
    - Wirkung: weiterhin keine Runtime-Lesung, keine Handlung, kein Gate,
      kein Entry, keine Richtung.
138. Theorieanker als eigene Bauplan-Datei festgehalten:
    - Neue Datei: `DIO_BAUPLAN/konstruktion/43_MCM_THEORIEANKER_EMERGENZ.md`.
    - Inhalt: MCM Pure Emergence, MCM Robustness und MCM 3D Emergence wurden
      als fachliche Grundlage fuer Mini-DIOs emergentes Gedaechtnis und die
      wachsende innere Semantikmatrix zusammengefuehrt.
    - Bedeutung fuer Mini-DIO: reproduzierte `dio_*`-Syntaxfamilien und
      Bedeutungsinseln werden als passive Feldkondensation gelesen, nicht als
      Strategie.
    - Bedeutung fuer DIO allgemein: DIO soll nicht top-down Strategie
      erzwingen, sondern aus Sinnesraeumen, MCM-Feldwirkung, lokaler Kopplung,
      Wiederkehr, Konsequenz und Reifung innere Ordnung bilden.
139. Passive semantische Dichtekarte umgesetzt:
    - Neues Modul: `DIO_MINI/report_passive_semantic_density.py`.
    - Aufgabe: aus der passiven Semantikmatrix Dichtezentren,
      Variantenanziehung, Inselwachstum, Fragmentierung,
      Reproduktionsdichte und semantische Wirbelwirkung berechnen.
    - Referenzbefund:
      `max_semantic_density=0.816995`,
      `max_variant_attraction=0.997576`,
      `max_semantic_vorticity=0.624991`.
    - Repro-Befund:
      `max_semantic_density=0.809843`,
      `max_variant_attraction=0.99975`,
      `max_semantic_vorticity=0.669195`.
    - Lesart: Mini-DIO bildet reproduzierbare semantische Dichte. Der frische
      Lauf zeigt rohe Dichte und Wachstum, aber keine uebernommene Reife.
    - Grenze: Bericht bleibt passiv. Keine Runtime-Lesung, keine Handlung,
      kein Gate, kein Entry, keine Richtung.
140. Erweiterungspruefung der passiven Semantikmatrix mit sechs Episoden:
    - Vorgehen: Probe20 bis Probe26 wurden von zwei auf sechs kontrollierte
      Episoden erweitert. Jede Probe enthaelt 72 Kerzen. Mini-DIO wurde mit
      frischer, getrennter Memory ueber diese erweiterten Welten gelesen.
    - Ergebnis:
      Referenz-Knoten `78`, 6-Episoden-Knoten `169`, gemeinsame Knoten `48`,
      neue Knoten `121`.
      Referenz-Kanten `196`, 6-Episoden-Kanten `360`, gemeinsame Kanten `46`,
      neue Kanten `314`.
      Referenz-Inseln `13`, 6-Episoden-Inseln `30`.
    - Dichte:
      `max_semantic_density=0.748433`,
      `max_variant_attraction=0.99998`,
      `max_semantic_vorticity=0.650137`.
    - Lesart: Mini-DIO kopiert die alte Matrix nicht nur. Bei laengerem,
      kontrolliertem Erleben entstehen neue `dio_*`-Spuren, mehr Kanten und
      mehr Bedeutungsinseln. Das ist ein Hinweis auf Ausbau der passiven
      semantischen Matrix.
    - Grenze: Noch keine Handlung, kein Entry, keine Strategie. Es handelt
      sich um passive Rohinseln, deren Tragfaehigkeit spaeter getrennt ueber
      Konsequenz, Reife und Innenwahrnehmung geprueft werden muss.
    - Debug:
      `debug/dio_mini_passive_semantic_matrix_6episoden_20260606_v1`.
141. Zielbild fuer Matrixdynamik geschaerft:
    - Neue Lesart: Wir suchen nicht nur reproduzierte Labels, sondern
      emergente Cluster-Varianz.
    - Gewollte Dynamik:
      neue Inseln entstehen, Varianten lagern sich an, Naehe und Kohaerenz
      verdichten sich, nicht tragende Spuren driften ab, und Inseln koennen
      sich neu organisieren.
    - Begriff: Textinseln. Eine Textinsel ist ein passiver Bedeutungsraum aus
      mehreren `dio_*`-Spuren, die wiederkehrend Feldnaehe, Variante,
      Konsequenz oder semantische Nachbarschaft teilen.
    - Grenze: Textinseln sind keine Strategie, kein Entry, keine Richtung und
      kein Gate. Sie sind passive innere Struktur, aus der spaeter nur dann
      Reife entstehen darf, wenn reale Konsequenz und Innenwahrnehmung sie
      tragen.
142. Passiver semantischer Matrixspeicher umgesetzt:
    - Neues Modul: `DIO_MINI/store_passive_semantic_matrix_memory.py`.
    - Speicher: `bot_memory/dio_mini_semantic_matrix_memory.json`.
    - Aufgabe: Mini-DIOs semantische Entwicklung getrennt speichern, laden,
      erweitern, verbessern und verknuepfen.
    - Gespeichert werden `nodes`, `edges`, `text_islands` und eine
      Entwicklungshistorie je Textinsel.
    - Testlauf: Referenzmatrix Probe20-26 wurde geladen und danach die
      6-Episoden-Erweiterung nachgeladen.
    - Ergebnis nach Update:
      `text_islands=33`, `nodes=199`, `edges=510`.
    - Entwicklungszustaende der letzten Erweiterung:
      `reorganizing_text_island=6`,
      `emerging_text_island=20`,
      `expanding_text_island=1`,
      `drifting_text_island=3`.
    - Lesart: Der Speicher erkennt jetzt nicht nur neue Inseln, sondern auch
      Reorganisation, Drift und Erweiterung bestehender semantischer Raeume.
    - Grenze: Der Speicher bleibt passiv. Keine Runtime-Lesung, keine
      Handlung, kein Gate, kein Entry, keine Richtung.
143. Folgereproduktion der Textinseln geprueft:
    - Vorgehen: Die 6-Episoden-Welten wurden erneut mit frischer Mini-DIO-
      Memory gelesen. Danach wurden Meaning-Space, Nachbarschaften,
      Semantikmatrix und Dichtekarte neu erzeugt.
    - Reproduktion gegen die erste 6-Episoden-Matrix:
      Knoten `169/169`, Kanten `360/360`, Inseln `30/30`.
      `node_reproduction_rate=1.0`, `edge_reproduction_rate=1.0`,
      `density_reproduction=1.0`.
    - Nachladung in `bot_memory/dio_mini_semantic_matrix_memory.json`:
      Alle `30` aktiven Textinseln wurden als `densifying_text_island`
      erkannt.
    - Lesart: Die erste Erweiterung erzeugt neue Inseln, Reorganisation und
      Drift. Eine erneute gleiche Welt erzeugt keine weitere willkuerliche
      Vermehrung, sondern Verdichtung bestehender semantischer Raeume.
    - Grenze: Weiterhin passiv. Keine Runtime-Lesung, keine Handlung, kein
      Gate, kein Entry, keine Richtung.
144. Variationspruefung der Textinseln mit Variante A:
    - Vorgehen: Probe20 bis Probe26 wurden als 6-Episoden-Variante A erzeugt.
      Die Grundstruktur blieb gleich, Preis, Volumen, Wick und Timing wurden
      leicht deterministisch verschoben.
    - Matrixbefund gegen die stabile 6-Episoden-Matrix:
      Referenz-Knoten `169`, Variante-Knoten `178`, gemeinsame Knoten `111`.
      Referenz-Kanten `360`, Variante-Kanten `360`, gemeinsame Kanten `95`.
      Referenz-Inseln `30`, Variante-Inseln `39`.
      `node_reproduction_rate=0.656805`,
      `edge_reproduction_rate=0.263889`,
      `density_reproduction=0.440701`.
    - Nachladung in den semantischen Matrixspeicher:
      `reorganizing_text_island=14`,
      `emerging_text_island=17`,
      `expanding_text_island=1`,
      `drifting_text_island=4`,
      `densifying_text_island=3`.
    - Lesart: Die Variante wird nicht als identische Welt gelesen. Mini-DIO
      haelt einen Teil alter Bindungen, bildet neue Textinseln, reorganisiert
      bestehende Raeume und laesst einzelne Naehen driften. Das ist ein
      belastbarer Hinweis auf dynamische Matrixentwicklung statt blosser
      Kopie.
    - Grenze: Weiterhin passiv. Keine Runtime-Lesung, keine Handlung, kein
      Gate, kein Entry, keine Richtung.
145. Fremdpruefung der Textinseln mit Variante B:
    - Vorgehen: Probe20 bis Probe26 wurden als deutlich fremdere
      6-Episoden-Variante B erzeugt: Richtungs-/Impulsspiegelung,
      staerkere Wick- und Volumenstruktur, andere Schockverteilung.
    - Matrixbefund gegen die stabile 6-Episoden-Matrix:
      Referenz-Knoten `169`, Variante-B-Knoten `266`, gemeinsame Knoten `1`.
      Referenz-Kanten `360`, Variante-B-Kanten `360`, gemeinsame Kanten `0`.
      Referenz-Inseln `30`, Variante-B-Inseln `99`.
      `node_reproduction_rate=0.005917`,
      `edge_reproduction_rate=0.0`,
      `density_reproduction=0.002663`.
    - Nachladung in den semantischen Matrixspeicher:
      `emerging_text_island=99`.
    - Lesart: Mini-DIO presst die fremde Welt nicht in vorhandene Textinseln.
      Der Speicher trennt sauber und bildet eine neue Textinsel-Landschaft.
      Damit entsteht ein erster passiver Nachweis fuer semantische
      Trennfaehigkeit:
      identische Welt -> Verdichtung,
      verwandte Variation -> Reorganisation / Drift / Erweiterung,
      fremde Welt -> neue Inselbildung.
    - Grenze: Weiterhin passiv. Keine Runtime-Lesung, keine Handlung, kein
      Gate, kein Entry, keine Richtung.
146. Naechster Schritt festgelegt: passive Textinsel-Reife:
    - Ziel: Aus `bot_memory/dio_mini_semantic_matrix_memory.json` lesen,
      welche Textinseln bei gleicher Welt wiederkehren, bei verwandter
      Variation tragend reorganisieren und bei fremder Welt sauber getrennt
      bleiben.
    - Geplantes Modul:
      `DIO_MINI/report_passive_text_island_maturity.py`.
    - Geplante Reifezustaende:
      `stable_recurrent_text_island`,
      `variant_resilient_text_island`,
      `reorganizing_but_bearing_text_island`,
      `drifting_unstable_text_island`,
      `foreign_separated_text_island`,
      `new_unconfirmed_text_island`.
    - Geplante Diagnosewerte:
      `recurrence_count`, `density_stability`, `variation_tolerance`,
      `foreign_separation`, `reorganization_quality`, `drift_pressure`,
      `semantic_maturity_score`.
    - Grenze: Der naechste Schritt bleibt Analyse. Keine Runtime-Lesung,
      keine Handlung, kein Entry, kein Gate, keine Richtung.
147. Passiver Textinsel-Reifebericht umgesetzt:
    - Neues Modul: `DIO_MINI/report_passive_text_island_maturity.py`.
    - Input: `bot_memory/dio_mini_semantic_matrix_memory.json`.
    - Output:
      `debug/dio_mini_passive_text_island_maturity_20260606_v1`.
    - Ergebnis:
      `variant_resilient_text_island=21`,
      `stable_recurrent_text_island=9`,
      `new_unconfirmed_text_island=119`.
    - Lesart: 30 Textinseln zeigen passive Reifeansaetze. Der groesste Teil
      bleibt bewusst unbestaetigt. Das verhindert, dass neue Inseln zu frueh
      als tragende Struktur gelesen werden.
    - Naechster Schritt: zweite verwandte Variation pruefen. Wenn dieselben
      reifen Inseln auch dort stabil bleiben, kann spaeter eine passive
      Innenwahrnehmungs-Landkarte daraus entstehen.
    - Grenze: Weiterhin passiv. Keine Runtime-Lesung, keine Handlung, kein
      Entry, kein Gate, keine Richtung.
148. Zweite verwandte Variation C geprueft:
    - Vorgehen: Probe20 bis Probe26 wurden als 6-Episoden-Variante C erzeugt.
      Die Struktur blieb verwandt, aber Amplitude, Timingdruck,
      Wick-Spannung und Volumenwelle wurden anders moduliert als in Variante A.
    - Matrixbefund gegen die stabile 6-Episoden-Matrix:
      Referenz-Knoten `169`, Variante-C-Knoten `172`, gemeinsame Knoten `57`.
      Referenz-Kanten `360`, Variante-C-Kanten `360`, gemeinsame Kanten `34`.
      Referenz-Inseln `30`, Variante-C-Inseln `36`.
      `node_reproduction_rate=0.337278`,
      `edge_reproduction_rate=0.094444`,
      `density_reproduction=0.203719`.
    - Nachladung in den semantischen Matrixspeicher:
      `emerging_text_island=21`,
      `reorganizing_text_island=8`,
      `expanding_text_island=4`,
      `drifting_text_island=3`.
    - Reifebericht nach Variante C:
      `variant_resilient_text_island=26`,
      `stable_recurrent_text_island=6`,
      `drifting_unstable_text_island=1`,
      `new_unconfirmed_text_island=137`.
    - Lesart: Einige Textinseln bleiben ueber mehrere verwandte Welten
      tragend, vor allem `dio_text_hy2bya`, `dio_text_8a1lm4`,
      `dio_text_6z30px` und `dio_text_11zj9f0`.
    - Naechster Schritt: passive Innenwahrnehmungs-Landkarte aus reifen
      Textinseln bauen. Weiterhin ohne Runtime-Lesung, Handlung, Entry, Gate
      oder Richtung.
149. Passive Innenwahrnehmungs-Landkarte umgesetzt:
    - Neues Modul: `DIO_MINI/report_passive_text_island_inner_map.py`.
    - Input:
      `debug/dio_mini_passive_text_island_maturity_after_varianteC_20260606_v1`.
    - Output:
      `debug/dio_mini_passive_text_island_inner_map_after_varianteC_20260606_v1`.
    - Innere Zustandsraeume:
      `inner_variation_bearing_space`,
      `inner_stable_recurrence_space`,
      `inner_soft_variation_space`,
      `inner_foreign_boundary_space`,
      `inner_unconfirmed_raw_space`,
      `inner_drift_watch_space`.
    - Befund:
      `inner_foreign_boundary_space=99`,
      `inner_unconfirmed_raw_space=37`,
      `inner_variation_bearing_space=19`,
      `inner_soft_variation_space=7`,
      `inner_stable_recurrence_space=6`,
      `inner_drift_watch_space=2`.
    - Lesart: Mini-DIOs passive Innenkarte trennt fremde Grenzen, rohe
      unbestaetigte Raeume, stabile Wiederkehr, weiche Variation, tragende
      Variation und Drift-Beobachtung.
    - Naechster Schritt: Innenkarte mit einer weiteren verwandten Variante D
      pruefen. Dabei geht es nur um Stabilitaet der Innenraeume, weiterhin
      ohne Runtime-Lesung, Handlung, Entry, Gate oder Richtung.
150. Innenkarte mit Variante D stabilitaetsgeprueft:
    - Vorgehen: Probe20 bis Probe26 wurden als 6-Episoden-Variante D erzeugt.
      Die Struktur blieb verwandt, aber Phasenverschiebung, Volumenatmung,
      Koerperamplitude und Wick-Spannung wurden anders moduliert als in A/C.
    - Matrixbefund gegen die stabile 6-Episoden-Matrix:
      Referenz-Knoten `169`, Variante-D-Knoten `171`, gemeinsame Knoten `49`.
      Referenz-Kanten `360`, Variante-D-Kanten `360`, gemeinsame Kanten `24`.
      Referenz-Inseln `30`, Variante-D-Inseln `30`.
      `node_reproduction_rate=0.289941`,
      `edge_reproduction_rate=0.066667`,
      `density_reproduction=0.16714`.
    - Nachladung in den semantischen Matrixspeicher:
      `reorganizing_text_island=13`,
      `emerging_text_island=9`,
      `expanding_text_island=6`,
      `drifting_text_island=2`.
    - Reifebericht:
      `variant_resilient_text_island=37`,
      `stable_recurrent_text_island=5`,
      `drifting_unstable_text_island=1`,
      `new_unconfirmed_text_island=136`.
    - Innenkarte:
      `inner_variation_bearing_space=19`,
      `inner_soft_variation_space=18`,
      `inner_stable_recurrence_space=5`,
      `inner_foreign_boundary_space=99`,
      `inner_unconfirmed_raw_space=34`,
      `inner_drift_watch_space=4`.
    - Lesart: Die tragenden Variationsraeume bleiben stabil bei `19`, die
      Fremdgrenze bleibt stabil bei `99`, und weiche Variationsraeume werden
      feiner ausgebaut.
    - Naechster Schritt: passive Innenkarten-Stabilitaetsanalyse bauen, die
      C gegen D vergleicht. Weiterhin ohne Runtime-Lesung, Handlung, Entry,
      Gate oder Richtung.
151. Passive Innenkarten-Stabilitaetsanalyse C gegen D umgesetzt:
    - Neues Modul: `DIO_MINI/compare_passive_text_island_inner_maps.py`.
    - Vergleich:
      `debug/dio_mini_passive_text_island_inner_map_after_varianteC_20260606_v1`
      gegen
      `debug/dio_mini_passive_text_island_inner_map_after_varianteD_20260606_v1`.
    - Output:
      `debug/dio_mini_passive_text_island_inner_map_compare_C_vs_D_20260606_v1`.
    - Befund:
      `stable_foreign_boundary=99`,
      `stable_same_inner_state=32`,
      `stable_variation_bearing=19`,
      `inner_state_strengthened=11`,
      `new_in_right_inner_map=9`,
      `stable_recurrence=5`,
      `persistent_drift_watch=2`,
      `shifted_into_drift_watch=2`.
    - Lesart: Die Innenkarte bleibt zwischen C und D stabil. Tragende
      Variationsraeume bleiben bei `19`, Fremdgrenzen bleiben bei `99`, und
      `11` Raeume werden staerker.
    - Naechster Schritt: passive Kernliste aus stabilen Innenraeumen bilden.
      Diese Kernliste bleibt Diagnose und darf keine Handlung, Entry, Gate
      oder Richtung ausloesen.
152. Passive Kernliste und passiver Inner-Core-Speicher umgesetzt:
    - Neue Module:
      `DIO_MINI/report_passive_inner_core_list.py`,
      `DIO_MINI/store_passive_inner_core_memory.py`.
    - Input:
      `debug/dio_mini_passive_text_island_inner_map_compare_C_vs_D_20260606_v1`.
    - Outputs:
      `debug/dio_mini_passive_inner_core_list_C_vs_D_20260606_v1`,
      `debug/dio_mini_passive_inner_core_memory_C_vs_D_20260606_v1`,
      `bot_memory/dio_mini_passive_inner_core_memory.json`.
    - Befund:
      `passive_foreign_boundary_core=99`,
      `passive_variation_core=19`,
      `passive_recurrence_core=5`,
      gesamt `123` passive Kerne.
    - Lesart: Mini-DIO kann stabile Innenraeume jetzt getrennt festhalten:
      Fremdgrenzen, tragende Variation und stabile Wiederkehr. Das bleibt eine
      passive Ordnungsschicht und wird nicht von Mini-DIO fuer Handlung,
      Entry, Gate oder Richtung gelesen.
    - Naechster Schritt: diese passive Kernliste gegen eine neue verwandte
      Variante E pruefen. Relevant ist, ob Kernraeume stabil bleiben, sich
      erweitern, driften oder neu organisieren.
153. Variante E gegen passive Kernraeume geprueft:
    - Neue kontrollierte CSVs:
      `data/kontrolliert_sensor_relation_probe20_emergenz_richtungsvarianz_6episoden_varianteE_verwandt_5m_SOLUSDT.csv`
      bis
      `data/kontrolliert_sensor_relation_probe26_emergenz_signaturdrift_6episoden_varianteE_verwandt_5m_SOLUSDT.csv`.
    - Variante E bleibt verwandt, ist aber haerter moduliert:
      C/D-Gegenphase, kleine Wick- und Volumenatmung.
    - Matrixbefund gegen die stabile 6-Episoden-Matrix:
      Referenz-Knoten `169`, Variante-E-Knoten `237`, gemeinsame Knoten `67`.
      Referenz-Kanten `360`, Variante-E-Kanten `360`, gemeinsame Kanten `22`.
      Referenz-Inseln `30`, Variante-E-Inseln `90`.
      `node_reproduction_rate=0.39645`,
      `edge_reproduction_rate=0.061111`.
    - Nachladung in `bot_memory/dio_mini_semantic_matrix_memory.json`:
      Gesamtstand `233` Textinseln, `774` Knoten, `1986` Kanten.
    - Reifebericht nach Variante E:
      `variant_resilient_text_island=44`,
      `stable_recurrent_text_island=7`,
      `drifting_unstable_text_island=3`,
      `new_unconfirmed_text_island=179`.
    - Innenkarte nach Variante E:
      `inner_foreign_boundary_space=99`,
      `inner_unconfirmed_raw_space=77`,
      `inner_soft_variation_space=24`,
      `inner_variation_bearing_space=20`,
      `inner_stable_recurrence_space=7`,
      `inner_drift_watch_space=6`.
    - Vergleich D gegen E:
      `stable_foreign_boundary=99`,
      `stable_same_inner_state=36`,
      `stable_variation_bearing=17`,
      `inner_state_strengthened=15`,
      `stable_recurrence=5`,
      `persistent_drift_watch=3`,
      `shifted_into_drift_watch=3`,
      `inner_state_softened=1`,
      `new_in_right_inner_map=54`.
    - Passive Kernliste D gegen E:
      `passive_foreign_boundary_core=99`,
      `passive_variation_core=17`,
      `passive_recurrence_core=5`,
      gesamt `121`.
    - Lesart: Variante E fragmentiert staerker und erzeugt viele rohe neue
      Inseln. Trotzdem bleiben Fremdgrenzen und Wiederkehr stabil. Die
      Variationskerne sinken nur leicht von `19` auf `17`.
    - Naechster Schritt: Core-Stabilitaetslupe bauen. Sie soll konkret zeigen,
      welche Variationskerne von D nach E tragen und welche zwei Kerne
      weicher, driftend oder unbestaetigt wurden.
154. Core-Stabilitaetslupe umgesetzt:
    - Neues Modul: `DIO_MINI/report_passive_inner_core_stability_lupe.py`.
    - Vergleich:
      `debug/dio_mini_passive_inner_core_list_C_vs_D_20260606_v1`
      gegen
      `debug/dio_mini_passive_inner_core_list_D_vs_E_20260606_v1`.
    - Output:
      `debug/dio_mini_passive_inner_core_stability_lupe_CD_vs_DE_20260606_v1`.
    - Befund:
      `stable_passive_foreign_boundary_core=99`,
      `stable_passive_variation_core=17`,
      `stable_passive_recurrence_core=5`,
      `lost_passive_variation_core=2`.
    - Verlorene Variationskerne:
      `dio_text_1h5am86`,
      `dio_text_1nxyi3d`.
    - Lesart: Die Stabilitaet liegt in konkreten Textinsel-Symbolen, nicht
      nur in Summen. Fremdgrenzen und Wiederkehrkerne bleiben voll stabil.
      Nur zwei Variationskerne gehen bei der haerteren Variante E aus der
      Kernliste.
    - Naechster Schritt: Detail-Lupe auf die zwei verlorenen Variationskerne.
      Es soll geprueft werden, ob sie wirklich verschwinden, in weiche
      Variation wechseln oder in neue Inseln zerfallen.
155. Detail-Lupe verlorener Variationskerne umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_lost_core_reorganization_lupe.py`.
    - Output:
      `debug/dio_mini_passive_lost_core_reorganization_lupe_E_20260606_v1`.
    - Befund:
      Beide verlorenen Variationskerne sind nicht verschwunden, sondern als
      gleiche Textinsel-Symbole in `inner_drift_watch_space` gekippt.
    - Details:
      `dio_text_1h5am86`:
      vorher `passive_variation_core`,
      nachher `inner_drift_watch_space`,
      Familien-Ueberlappung `0.250`.
      `dio_text_1nxyi3d`:
      vorher `passive_variation_core`,
      nachher `inner_drift_watch_space`,
      Familien-Ueberlappung `0.200`.
    - Lesart: Mini-DIO verliert diese Kerne nicht blind. Der semantische Name
      bleibt, aber die tragende Familienbasis wird duenn und der Zustand wird
      als Drift-Beobachtung sichtbar. Das ist passive Reorganisation.
    - Naechster Schritt: Reorganisations-Historie fuer Textinseln bauen:
      Kern -> Variation -> Drift -> neue Stabilisierung oder Aufloesung.
      Weiterhin rein passiv.
156. Passive Textinsel-Reorganisationshistorie C/D/E umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_text_island_reorganization_history.py`.
    - Input:
      Innenkarten C, D und E.
    - Output:
      `debug/dio_mini_passive_text_island_reorganization_history_C_D_E_20260607_v1`.
    - Befund:
      `stable_foreign_boundary_history=99`,
      `persistent_raw_history=76`,
      `mixed_reorganization_history=17`,
      `stable_variation_history=17`,
      `stable_inner_soft_variation_space=6`,
      `reorganized_into_core=5`,
      `stable_recurrence_history=5`,
      `late_text_island_emergence=3`,
      `core_to_drift_reorganization=2`,
      `persistent_drift_history=2`,
      `core_to_soft_variation=1`.
    - Wichtige Einzelbewegungen:
      `dio_text_1h5am86` und `dio_text_1nxyi3d`
      bewegen sich von
      `inner_variation_bearing_space -> inner_variation_bearing_space -> inner_drift_watch_space`.
      Beide haben eine ausgeduennte Familienbasis.
      `dio_text_1ccct8g` bewegt sich von
      `inner_stable_recurrence_space -> inner_soft_variation_space -> inner_soft_variation_space`.
    - Lesart: Mini-DIO zeigt eine passive semantische Verlaufsordnung:
      stabile Insel, rohe Insel, driftende Insel, reorganisierte Insel.
      Das bleibt Diagnose und wirkt nicht auf Handlung, Entry, Gate oder
      Richtung.
    - Naechster Schritt: passive Reorganisations-Memory bauen. Sie speichert
      diese Verlaufszustaende je Textinsel als Historie, wird aber weiterhin
      nicht von Mini-DIO fuer Handlung gelesen.
157. Passive Textinsel-Reorganisationsmemory umgesetzt:
    - Neues Modul:
      `DIO_MINI/store_passive_text_island_reorganization_memory.py`.
    - Input:
      `debug/dio_mini_passive_text_island_reorganization_history_C_D_E_20260607_v1/passive_text_island_reorganization_history.csv`.
    - Memory:
      `bot_memory/dio_mini_passive_text_island_reorganization_memory.json`.
    - Output:
      `debug/dio_mini_passive_text_island_reorganization_memory_C_D_E_20260607_v1`.
    - Befund:
      `text_island_count=233`,
      `updates=233`,
      `avg_last_drift_pressure=0.030114449`.
    - Dominante Verlaufszustaende:
      `stable_foreign_boundary_history=99`,
      `persistent_raw_history=76`,
      `mixed_reorganization_history=17`,
      `stable_variation_history=17`,
      `stable_inner_soft_variation_space=6`,
      `reorganized_into_core=5`,
      `stable_recurrence_history=5`,
      `late_text_island_emergence=3`,
      `core_to_drift_reorganization=2`,
      `persistent_drift_history=2`,
      `core_to_soft_variation=1`.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Lesart: Die Textinseln haben jetzt eine getrennte passive
      Reorganisationsspur. Damit kann spaeter geprueft werden, ob eine Insel
      stabil bleibt, driftet, sich weich reorganisiert oder erneut Kernnaehe
      findet.
    - Naechster Schritt: gegen eine weitere Variante pruefen, ob Driftinseln
      wieder stabilisieren, weiter driften oder in rohe neue Textinseln
      zerfallen.
158. Variante F als weitere passive Testwelt umgesetzt und ausgewertet:
    - Neues Modul:
      `DIO_MINI/create_controlled_variant_f.py`.
    - Neue CSVs:
      `data/kontrolliert_sensor_relation_probe20_emergenz_richtungsvarianz_6episoden_varianteF_verwandt_5m_SOLUSDT.csv`
      bis
      `data/kontrolliert_sensor_relation_probe26_emergenz_signaturdrift_6episoden_varianteF_verwandt_5m_SOLUSDT.csv`.
    - Mini-DIO-Runs:
      `debug/dio_mini_repro_semantic_matrix_6episoden_varianteF_20260607_probe20`
      bis
      `debug/dio_mini_repro_semantic_matrix_6episoden_varianteF_20260607_probe26`.
    - Passive Matrix F:
      `clusters=253`,
      `episodes=924`,
      `nodes=253`,
      `edges=120`,
      `islands=161`.
    - Vergleich E gegen F:
      `node_count_reference=237`,
      `node_count_candidate=253`,
      `shared_node_count=177`,
      `node_reproduction_rate=0.746835`,
      `edge_count_reference=360`,
      `edge_count_candidate=120`,
      `shared_edge_count=48`,
      `edge_reproduction_rate=0.133333`,
      `island_count_reference=90`,
      `island_count_candidate=161`.
    - Passive Semantikmemory nach F:
      `text_islands=315`,
      `nodes=823`,
      `edges=2037`,
      `updated_islands=161`.
    - Maturity nach F:
      `variant_resilient_text_island=51`,
      `stable_recurrent_text_island=27`,
      `reorganizing_but_bearing_text_island=1`,
      `drifting_unstable_text_island=6`,
      `new_unconfirmed_text_island=230`.
    - Innenkarte nach F:
      `inner_foreign_boundary_space=99`,
      `inner_unconfirmed_raw_space=118`,
      `inner_soft_variation_space=31`,
      `inner_variation_bearing_space=20`,
      `inner_stable_recurrence_space=27`,
      `inner_drift_watch_space=20`.
    - Vergleich E gegen F:
      `stable_foreign_boundary=99`,
      `new_in_right_inner_map=82`,
      `stable_same_inner_state=50`,
      `inner_state_strengthened=39`,
      `stable_variation_bearing=16`,
      `shifted_into_drift_watch=15`,
      `persistent_drift_watch=5`,
      `stable_recurrence=5`,
      `inner_state_softened=4`.
    - Passive Kernliste E gegen F:
      `passive_foreign_boundary_core=99`,
      `passive_variation_core=16`,
      `passive_recurrence_core=5`,
      gesamt `120`.
    - D/E/F-Reorganisationshistorie:
      `persistent_raw_history=115`,
      `stable_foreign_boundary_history=99`,
      `reorganized_into_core=29`,
      `late_text_island_emergence=22`,
      `stable_variation_history=13`,
      `stable_inner_soft_variation_space=12`,
      `mixed_reorganization_history=10`,
      `core_to_drift_reorganization=5`,
      `stable_recurrence_history=5`,
      `core_to_soft_variation=3`,
      `persistent_drift_history=2`.
    - Memory-Updates:
      `bot_memory/dio_mini_semantic_matrix_memory.json`,
      `bot_memory/dio_mini_passive_text_island_reorganization_memory.json`,
      `bot_memory/dio_mini_passive_inner_core_memory.json`.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Lesart: Variante F zeigt keine blinde Wiederholung. Viele Namen bleiben
      erhalten, aber die Inselstruktur wird rauer und fragmentierter. Relevant
      ist der Gegenbefund: `reorganized_into_core=29` zeigt, dass einige
      vormals rohe oder weiche Inseln in Kernnaehe kommen.
    - Naechster Schritt: Lupe auf die `reorganized_into_core`-Textinseln.
      Wir pruefen, welche Inseln sich verdichtet haben und ob diese
      Verdichtung stabil oder nur variantenbedingt ist.
159. Lupe auf `reorganized_into_core` D/E/F umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_reorganized_core_lupe.py`.
    - Input:
      `debug/dio_mini_passive_text_island_reorganization_history_D_E_F_20260607_v1/passive_text_island_reorganization_history.csv`.
    - Output:
      `debug/dio_mini_passive_reorganized_core_lupe_D_E_F_20260607_v1`.
    - Befund:
      `reorganized_core_items=29`,
      `avg_score_delta=0.387771648`,
      `avg_family_overlap=0.789265189`.
    - Kernnaehe-Modi:
      `new_raw_to_stable_recurrence=19`,
      `soft_variation_to_variation_core=4`,
      `to_variation_core=3`,
      `to_stable_recurrence_core=2`,
      `drift_to_stable_recurrence=1`.
    - Familienbewegung:
      `family_basis_stable=20`,
      `family_basis_fragmented=6`,
      `family_basis_thinned=3`.
    - Lesart: Die wichtigste Bewegung ist passive semantische Verdichtung.
      19 vorher rohe Textinseln werden in F zu stabiler Wiederkehr. Die hohe
      durchschnittliche Familienueberlappung spricht dafuer, dass das keine
      reine Umbenennung ist, sondern haeufig auf erhaltener Familienbasis
      passiert.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt: die 19 `new_raw_to_stable_recurrence`-Textinseln
      gegen ihre konkreten Familien lesen. Ziel ist zu pruefen, ob sie aus
      einzelnen wiederkehrenden Familien bestehen oder ob mehrere nahe
      Familien zu einer neuen semantischen Insel verdichten.
160. Lupe `new_raw_to_stable_recurrence` gegen Familien umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_raw_to_recurrence_family_lupe.py`.
    - Input:
      `debug/dio_mini_passive_reorganized_core_lupe_D_E_F_20260607_v1/passive_reorganized_core_lupe.csv`
      und
      `debug/dio_mini_passive_cluster_meaning_space_6episoden_varianteF_20260607_v1/passive_cluster_meaning_space.csv`.
    - Output:
      `debug/dio_mini_passive_raw_to_recurrence_family_lupe_D_E_F_20260607_v1`.
    - Befund:
      `new_raw_to_stable_recurrence=19`,
      `single_family_stable_recurrence=18`,
      `multi_family_coherent_condensation=1`,
      `avg_episode_count_sum=5.894736842`,
      `avg_observation_learning_pressure=0.362646474`,
      `avg_trade_readiness=0.003255763`.
    - Mehrfamilien-Keim:
      `dio_text_1dg4vy8` mit den Familien `dio_0a6g` und `dio_1og2`.
    - Messbild:
      `avg_fuehlen_mcm_coherence=0.344496`,
      `span_fuehlen_mcm_coherence=0.00106`,
      `avg_hoeren_energy_tone=-0.1982285`,
      `span_hoeren_energy_tone=0.003787`,
      `avg_sehen_form_flow=0.506641`,
      `span_sehen_form_flow=0.032858`,
      `avg_mini_neuro_balance=0.0193425`,
      `span_mini_neuro_balance=0.003761`.
    - Lesart:
      18 Faelle sind einzelne stabile Wiederholungsfamilien. `dio_text_1dg4vy8`
      ist der relevante Sonderfall: zwei Familien liegen in Sehen, Hoeren,
      Fuehlen und Neurozustand so nah beieinander, dass eine passive
      Mehrfamilien-Verdichtung sichtbar wird.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt: `dio_text_1dg4vy8` ueber Varianten verfolgen. Ziel:
      pruefen, ob diese Verdichtung stabil bleibt, weitere Familien anzieht
      oder wieder in Einzelfamilien zerfaellt.
161. Lineage-Lupe fuer `dio_text_1dg4vy8` umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_text_island_lineage_lupe.py`.
    - Output:
      `debug/dio_mini_passive_text_island_lineage_lupe_dio_text_1dg4vy8_C_D_E_F_20260607_v1`.
    - Verlauf:
      `C=absent`,
      `D=absent`,
      `E=inner_unconfirmed_raw_space`,
      `F=inner_stable_recurrence_space`.
    - Score:
      `C=0.0`,
      `D=0.0`,
      `E=0.213333333`,
      `F=0.4776192`,
      `score_delta_first_last=0.4776192`.
    - Familien:
      `E=dio_0a6g|dio_1og2`,
      `F=dio_0a6g|dio_1og2`,
      `family_stability=1.0`.
    - E-F-Familiennaehe:
      In E und F liegen die beiden Familien eng zusammen in MCM-Kohaerenz,
      Hoerenergie, Sehfluss und neuronaler Balance. Die Familienbasis bleibt
      erhalten; die Textinsel wechselt von roh zu stabiler Wiederkehr.
    - Lesart:
      `dio_text_1dg4vy8` ist ein sauberer passiver Lineage-Fall:
      rohe Mehrfamiliennaehe wird in der naechsten verwandten Variante zur
      stabilen Wiederkehr, ohne Handlung, Gate, Entry oder Richtung.
    - Naechster Schritt:
      Entweder Variante F reproduzieren oder Variante G erzeugen. Ziel:
      pruefen, ob die Verdichtung stabil bleibt oder nur E/F-spezifisch ist.
162. Variante F reproduziert:
    - Repro-Runs:
      `debug/dio_mini_repro_semantic_matrix_6episoden_varianteF_repro_20260607_probe20`
      bis
      `debug/dio_mini_repro_semantic_matrix_6episoden_varianteF_repro_20260607_probe26`.
    - Passive Repro-Matrix:
      `debug/dio_mini_passive_semantic_matrix_6episoden_varianteF_repro_20260607_v1`.
    - Vergleich:
      `debug/dio_mini_passive_semantic_matrix_compare_varianteF_vs_F_repro_20260607_v1`.
    - Matrix-Reproduktion:
      `node_count_reference=253`,
      `node_count_candidate=253`,
      `shared_node_count=253`,
      `node_reproduction_rate=1.0`,
      `edge_count_reference=120`,
      `edge_count_candidate=120`,
      `shared_edge_count=120`,
      `edge_reproduction_rate=1.0`,
      `island_count_reference=161`,
      `island_count_candidate=161`.
    - Scratch-Reifecheck:
      `bot_memory/dio_mini_semantic_matrix_memory_F_repro_check_20260607.json`.
      Diese Memory ist nur fuer den Repro-Check und wird nicht von Mini-DIO
      gelesen.
    - Maturity-Repro-Befund:
      `stable_recurrent_text_island=161`.
    - `dio_text_1dg4vy8`:
      `F_original=inner_stable_recurrence_space`,
      `F_repro_scratch=inner_stable_recurrence_space`,
      `families=dio_0a6g|dio_1og2`,
      `family_stability=1.0`,
      `score_delta=0.0052938`.
    - Lesart:
      Variante F reproduziert exakt auf Matrixebene. Der Mehrfamilien-Keim
      `dio_text_1dg4vy8` bleibt in gleicher Familienbasis und gleicher
      innerer Kernnaehe. Damit ist diese Verdichtung kein einmaliger Zufall
      des ersten F-Laufs.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      nahe Variante G erzeugen. Ziel ist zu pruefen, ob `dio_text_1dg4vy8`
      bei verwandter neuer Welt weitertraegt, weitere Familien anzieht oder
      driftet.
163. Variante G erzeugt und gegen F geprueft:
    - Neues Modul:
      `DIO_MINI/create_controlled_variant_g.py`.
    - Neue CSVs:
      `data/kontrolliert_sensor_relation_probe20_emergenz_richtungsvarianz_6episoden_varianteG_verwandt_5m_SOLUSDT.csv`
      bis
      `data/kontrolliert_sensor_relation_probe26_emergenz_signaturdrift_6episoden_varianteG_verwandt_5m_SOLUSDT.csv`.
    - Runs:
      `debug/dio_mini_repro_semantic_matrix_6episoden_varianteG_20260607_probe20`
      bis
      `debug/dio_mini_repro_semantic_matrix_6episoden_varianteG_20260607_probe26`.
    - Matrix G:
      `nodes=266`,
      `edges=120`,
      `islands=170`.
    - Vergleich F gegen G:
      `shared_node_count=206`,
      `node_reproduction_rate=0.814229`,
      `shared_edge_count=53`,
      `edge_reproduction_rate=0.441667`,
      `island_count_reference=161`,
      `island_count_candidate=170`.
    - Scratch-Memory F -> G:
      `bot_memory/dio_mini_semantic_matrix_memory_F_G_check_20260607.json`.
    - Maturity F/G:
      `stable_recurrent_text_island=87`,
      `variant_resilient_text_island=26`,
      `new_unconfirmed_text_island=83`.
    - Innenkarte F/G:
      `inner_stable_recurrence_space=87`,
      `inner_soft_variation_space=26`,
      `inner_unconfirmed_raw_space=61`,
      `inner_drift_watch_space=22`.
    - `dio_text_1dg4vy8`:
      `F_original=inner_stable_recurrence_space`,
      `G_scratch=inner_soft_variation_space`,
      `score_delta=-0.002179733`,
      `family_stability=0.333333333`.
    - Familienbewegung:
      F: `dio_0a6g|dio_1og2`.
      G: `dio_14ls|dio_1og2`.
      `dio_1og2` bleibt Anker, `dio_0a6g` wird durch `dio_14ls` ersetzt.
    - Lesart:
      Die Textinsel zerfaellt nicht, wird aber weicher. Sie bleibt als
      variantenfaehige Bedeutungsnaehe erhalten: stabile Wiederkehr wird zu
      weicher Variation. Das ist passiv, keine Handlung.
    - Naechster Schritt:
      `dio_text_1dg4vy8` als passives Anker-/Austausch-Muster markieren und
      pruefen, ob solche Muster auch bei anderen Textinseln auftreten.
164. Anker-/Austausch-Lupe F -> G umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_anchor_exchange_lupe.py`.
    - Methodische Korrektur:
      Der Vergleich wurde sauber im Scratch-Kontext gemacht:
      links `F-only-Scratch-Inner-Map`,
      rechts `F->G-Scratch-Inner-Map`.
      Die globale F-Karte enthaelt aeltere C/D/E-Spuren und waere fuer diese
      Zaehllogik zu breit.
    - Output:
      `debug/dio_mini_passive_anchor_exchange_lupe_F_only_vs_G_check_20260607_v1`.
    - Befund:
      `same_family_basis=113`,
      `new_text_island=35`,
      `anchor_thinning=22`,
      `anchor_expansion=16`,
      `anchor_exchange=10`,
      `anchor_exchange_avg_family_stability=0.412263814`,
      `anchor_exchange_avg_score_delta=0.25851258`.
    - `dio_text_1dg4vy8`:
      `left_inner_state=inner_unconfirmed_raw_space`,
      `right_inner_state=inner_soft_variation_space`,
      `left_score=0.213333333`,
      `right_score=0.475439467`,
      `score_delta=0.262106134`,
      `family_stability=0.333333333`,
      `anchor=dio_1og2`,
      `added=dio_14ls`,
      `removed=dio_0a6g`.
    - Lesart:
      Bei gleicher Welt reproduziert `dio_text_1dg4vy8` stabil. Bei verwandter
      neuer Welt bleibt eine Ankerfamilie erhalten und eine nahe Familie wird
      ausgetauscht. Das ist passive semantische Reorganisation, nicht Zerfall.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Die 10 Anker-/Austausch-Faelle sensorisch clustern. Ziel ist zu pruefen,
      ob Ankerwechsel vor allem durch Sehen, Hoeren, Fuehlen oder Neurobalance
      getragen wird.
165. Sensor-Lupe fuer Anker-/Austausch-Faelle F -> G umgesetzt:
    - Modul:
      `DIO_MINI/report_passive_anchor_exchange_sensor_lupe.py`.
    - Output:
      `debug/dio_mini_passive_anchor_exchange_sensor_lupe_F_G_20260607_v1`.
    - Methodik:
      Die 10 Anker-/Austausch-Faelle werden mit dem Bedeutungsraum der
      Familien verbunden. Gemessen wird getrennt nach alter Austauschfamilie
      (`removed`), neuer Austauschfamilie (`added`) und stabiler Ankerfamilie.
      Der Austauschabstand wird zwischen `removed` und `added` gemessen; der
      Anker-Shift bleibt separate Stabilitaetsreferenz.
    - Befund:
      `anchor_exchange_items=10`,
      `hearing_dominant_delta=5`,
      `visual_dominant_delta=2`,
      `neuro_dominant_delta=1`,
      `mixed_sensor_delta=2`.
    - Durchschnittliche Austauschabstaende:
      `visual=0.019010237`,
      `hearing=0.01762365`,
      `feeling=0.007310162`,
      `neuro=0.009422163`.
    - `dio_text_1dg4vy8`:
      `state=mixed_sensor_delta`,
      `anchor=dio_1og2`,
      `removed=dio_0a6g`,
      `added=dio_14ls`,
      `visual_exchange_distance=0.007955667`,
      `hearing_exchange_distance=0.0077145`,
      `feeling_exchange_distance=0.003674667`,
      `neuro_exchange_distance=0.0015138`.
    - Lesart:
      Der Austausch wird in Variante G meistens ueber Hoeren/Energie und
      Sehen/Form getragen. Fuehlen/MCM wirkt eher als stabile Resonanz- und
      Kopplungsschicht, nicht als staerkster Austauschtreiber.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Dieselbe Sensor-Lupe auf weitere Varianten anwenden, um zu pruefen, ob
      Hoeren/Energie stabil der haeufigste Austauschtraeger bleibt oder nur in
      Variante G dominiert.
166. Sensor-Lupe auf D -> E und E -> F erweitert:
    - Outputs:
      `debug/dio_mini_passive_anchor_exchange_lupe_D_vs_E_20260607_v1`,
      `debug/dio_mini_passive_anchor_exchange_sensor_lupe_D_E_20260607_v1`,
      `debug/dio_mini_passive_anchor_exchange_lupe_E_vs_F_20260607_v1`,
      `debug/dio_mini_passive_anchor_exchange_sensor_lupe_E_F_20260607_v1`.
    - D -> E:
      `anchor_exchange=14`,
      `same_family_basis=147`,
      `new_text_island=54`,
      `hearing_dominant_delta=7`,
      `visual_dominant_delta=3`,
      `neuro_dominant_delta=3`,
      `no_clear_sensor_delta=1`.
    - E -> F:
      `anchor_exchange=13`,
      `same_family_basis=186`,
      `new_text_island=82`,
      `hearing_dominant_delta=8`,
      `visual_dominant_delta=2`,
      `neuro_dominant_delta=1`,
      `mixed_sensor_delta=2`.
    - Vergleich mit F -> G:
      Auch F -> G zeigt `hearing_dominant_delta=5` bei 10 Austauschfaellen.
      Damit ist Hoeren/Energie ueber mehrere Uebergaenge hinweg ein
      wiederkehrender Traeger von Anker-/Austauschbewegung.
    - Lesart:
      Mini-DIOs passive Textinseln verschieben sich multisensorisch. Sehen und
      Neurobalance beteiligen sich, aber die energetische Tonspur ist bisher
      der haeufigste Austauschtraeger. Fuehlen/MCM wirkt eher als Resonanz-
      und Kopplungsschicht.
    - Naechster Schritt:
      Eine kompakte Uebergangs-Matrix bauen:
      `transition`, `anchor_exchange_count`, `dominant_sensor_axis`,
      `avg_family_stability`, `avg_score_delta`, `avg_exchange_distances`.
167. Kompakte Anker-/Austausch-Uebergangs-Matrix gebaut:
    - Modul:
      `DIO_MINI/report_passive_anchor_exchange_transition_matrix.py`.
    - Output:
      `debug/dio_mini_passive_anchor_exchange_transition_matrix_D_E_F_G_20260607_v1`.
    - Matrix:
      `D_to_E`: `anchor_exchange_count=14`,
      `dominant_sensor_axis=hearing_dominant_delta`,
      `avg_family_stability=0.272610029`,
      `avg_score_delta=0.103308466`.
      `E_to_F`: `anchor_exchange_count=13`,
      `dominant_sensor_axis=hearing_dominant_delta`,
      `avg_family_stability=0.356762468`,
      `avg_score_delta=0.128988169`.
      `F_to_G`: `anchor_exchange_count=10`,
      `dominant_sensor_axis=hearing_dominant_delta`,
      `avg_family_stability=0.412263814`,
      `avg_score_delta=0.25851258`.
    - Lesart:
      Ueber drei Uebergaenge bleibt Hoeren/Energie die dominante
      Austauschachse. Gleichzeitig steigt die durchschnittliche
      Familien-Stabilitaet. Das ist ein passiver Hinweis auf reproduzierbare
      Syntaxentwicklung mit erhaltener Ankernaehe und variabler
      Austauschfamilie.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Eine neue kontrollierte Variante H oder einen bewusst andersartigen
      Datensatz erzeugen, um zu pruefen, ob die steigende Stabilitaet auch
      ausserhalb der verwandten Varianten erhalten bleibt.
168. Theorieabgleich mit ProtoMind-Abhandlung festgehalten:
    - Quelle:
      `ProtoMind, selbstaktive Feldkognition, akustische Reizmodulation und
      Schmerz-Gefahrenverarbeitung als integriertes Feldsystem`.
    - Methodisch wichtiger Punkt:
      Mini-DIO wurde nicht nach dieser Abhandlung gebaut. Die aktuellen
      Befunde entstanden zuerst aus kontrollierten Laeufen, Textinseln,
      Anker-/Austausch-Lupen und Sensor-Matrix-Auswertung. Erst danach wurde
      die Abhandlung gegengelesen.
    - Erkenntnis:
      Wir kamen zum Inhalt einer MCM-Abhandlung, ohne danach gearbeitet zu
      haben. Besonders passend ist der Befund, dass Hoeren/Energie in D->E,
      E->F und F->G die dominante Austauschachse war. Die Abhandlung beschreibt
      akustische Reizmodulation als Stimuluskanal, der Resonanzprozesse und
      interne Dynamiken beeinflussen kann.
    - Abgleich:
      `Textinsel = minimale kohaerente Organisationsstruktur`,
      `Ankerfamilie = stabiler Kern`,
      `Austauschfamilie = resonante Peripherie / Variantenraum`,
      `Hoeren/Energie = wiederkehrender Austauschtraeger`,
      `MCM/Fuehlen = Kopplungs- und Resonanzschicht`.
    - Lesart:
      Keine absolute Beweisbehauptung, aber ein relevanter
      Teil-Kohaerenzbefund zwischen MCM-Theorie und Mini-DIO-Messdaten.
    - Wirkungsgrenze:
      Dokumentation, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Mit Variante H oder einem deutlich anderen Datensatz pruefen, ob diese
      akustische Dominanz stabil bleibt oder weltspezifisch wechselt.
169. Variante H als Strukturkontrast umgesetzt und ausgewertet:
    - Neues Modul:
      `DIO_MINI/create_controlled_variant_h.py`.
    - Neue CSVs:
      `data/kontrolliert_sensor_relation_probe20_emergenz_richtungsvarianz_6episoden_varianteH_strukturkontrast_5m_SOLUSDT.csv`
      bis
      `data/kontrolliert_sensor_relation_probe26_emergenz_signaturdrift_6episoden_varianteH_strukturkontrast_5m_SOLUSDT.csv`.
    - Mini-DIO-Runs:
      `debug/dio_mini_repro_semantic_matrix_6episoden_varianteH_20260607_probe20`
      bis
      `debug/dio_mini_repro_semantic_matrix_6episoden_varianteH_20260607_probe26`.
    - Passive Matrix H:
      `clusters=303`,
      `episodes=462`,
      `nodes=303`,
      `edges=120`,
      `islands=197`.
    - Vergleich G -> H:
      `node_count_reference=266`,
      `node_count_candidate=303`,
      `shared_node_count=64`,
      `node_reproduction_rate=0.240602`,
      `edge_count_reference=120`,
      `edge_count_candidate=120`,
      `shared_edge_count=9`,
      `edge_reproduction_rate=0.075`,
      `island_count_reference=170`,
      `island_count_candidate=197`.
    - Scratch-Reife G -> H:
      `new_unconfirmed_text_island=298`,
      `stable_recurrent_text_island=19`,
      `variant_resilient_text_island=11`.
    - Anker-/Austausch G -> H:
      `new_text_island=158`,
      `same_family_basis=150`,
      `anchor_exchange=6`,
      `anchor_exchange_avg_family_stability=0.3`,
      `anchor_exchange_avg_score_delta=0.240592933`.
    - Sensor-Lupe G -> H:
      `hearing_dominant_delta=4`,
      `visual_dominant_delta=2`,
      `avg_exchange_distance.hearing=0.025480805`,
      `avg_exchange_distance.visual=0.022874574`,
      `avg_exchange_distance.feeling=0.017748769`,
      `avg_exchange_distance.neuro=0.005655133`.
    - Erweiterte Uebergangs-Matrix:
      `debug/dio_mini_passive_anchor_exchange_transition_matrix_D_E_F_G_H_20260607_v1`.
    - Lesart:
      H ist deutlich fremder als G: mehr neue Textinseln, geringere
      Node-/Edge-Reproduktion, weniger Anker-/Austauschfaelle. Trotzdem bleibt
      Hoeren/Energie die dominante Austauschachse. Das staerkt den Befund,
      dass die energetische Tonspur in Mini-DIO ein wiederkehrender
      semantischer Modulationstraeger ist.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Eine gezielte Hoer-Kontrastvariante bauen: sichtbare Form naeher halten,
      aber Energie-/Volumen-/Tonspur staerker verschieben. Damit laesst sich
      pruefen, ob Hoeren/Energie wirklich tragende Modulationsachse ist oder
      nur mit Formvarianz gemeinsam driftet.
170. Block E / E.1 wissenschaftlich fuer DIO festgehalten:
    - Quellen:
      `Abhandlung Block E - Die kosmische Matrix.pdf`
      und
      `Abhandlung Block E.1 - Die polare Entstehung des Universums.pdf`.
    - Kernaussage Block E:
      Zentrum, Abweichung, Expansion, lokale Verdichtung, Cluster-/
      Attraktorbildung und Rueckfuehrung bilden einen MCM-konformen
      Ordnungszyklus.
    - Kernaussage Block E.1:
      Polaritaet braucht Gegenbindung. Der Zero Point ist keine leere Mitte,
      sondern Referenz, Balancezone, Uebergang, Schnittstelle und moeglicher
      Wendepunkt. Zeit wird als Richtung wirkender oder gewirkter Energie
      gelesen.
    - Uebertragung auf Mini-DIO:
      `Textinseln = lokale semantische Kondensationen`,
      `dio_* Familien = Cluster / Attraktornaehe`,
      `Ankerfamilien = Rueckbindung / erhaltener Kern`,
      `Austauschfamilien = Expansion / Varianz`,
      `Hoeren/Energie = gerichtete Spannungsbewegung`,
      `MCM/Fuehlen = Gegenbindung / Resonanz / Rueckfuehrung`.
    - Wissenschaftliche Grenze:
      Das ist kein Beweis einer kosmologischen Theorie. Es ist ein
      struktureller Teil-Kohaerenzbefund zwischen MCM-Theorie und den
      kontrollierten Mini-DIO-Diagnosen.
    - Dokumentiert in:
      `DIO_BAUPLAN/konstruktion/43_MCM_THEORIEANKER_EMERGENZ.md`,
      `DIO_BAUPLAN/konstruktion/20_SPANNUNGSACHSE_ZERO_POINT.md`,
      `DIO_BAUPLAN/konstruktion/17_RAUMZEIT_VARIANTEN.md`.
    - Wirkungsgrenze:
      Dokumentation, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Die passive Vorbewusstseins-/Cluster-Reproduktion weiter pruefen:
      Welche Textinseln bleiben ueber kontrollierte Erweiterungen stabil,
      welche expandieren, welche driften, welche fuehren zu neuen semantischen
      Inseln?
171. Reproduzierbarkeit als Realitaetsbezug festgehalten:
    - Arbeitsdefinition:
      Reproduzierbarkeit bedeutet in Mini-DIO keine mechanische Kopie, sondern
      den direkten Bezug zur gelebten Realitaet der Daten und die beginnende
      Organisation im inneren MCM-System.
    - Lesart:
      Wenn gleiche oder aehnliche Gegebenheiten wieder aehnliche `dio_*`
      Syntax, Textinseln oder Cluster erzeugen, ist das eine
      strukturbedingte Konsequenz der Feldanordnung.
    - Grenze:
      Nicht exakt wie eine mathematische Konstante, keine absolute Wahrheit,
      kein Entry-Signal. Es ist ein Hinweis auf innere Ordnung aus erlebter
      Welt und MCM-Anordnung.
    - Dokumentiert in:
      `DIO_BAUPLAN/konstruktion/43_MCM_THEORIEANKER_EMERGENZ.md`.
    - Naechster Schritt:
      Reproduzierbarkeit weiter trennen in stabilen Kern, Variantenraum,
      Drift und neue semantische Inselbildung.
172. Begriff `inneres Universum` fuer DIO festgehalten:
    - Definition:
      Das innere Universum ist die selbst entstehende Ordnung aus erlebter
      Welt, MCM-Feldwirkung, Wiederkehr, Verdichtung, eigener Syntax und
      Konsequenz.
    - Grenze:
      Kein Fantasieraum und keine Halluzination. Das innere Universum bleibt
      an gelebte Realitaet, Weltspur und reale Konsequenz rueckgebunden.
    - Lesart:
      Memory ist nicht nur Datensammlung, sondern wachsender Innenraum aus
      wiederkehrender Feldwirkung, Textinseln, semantischer Dichte und Drift.
    - Dokumentiert in:
      `DIO_BAUPLAN/konstruktion/43_MCM_THEORIEANKER_EMERGENZ.md`.
    - Naechster Schritt:
      Im Mini-DIO weiter pruefen, wie dieses innere Universum passiv waechst:
      stabile Inseln, neue Inseln, Verdichtung, Drift, Rueckbindung.
173. Passive Diagnose `inneres Universum Wachstum` umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_inner_universe_growth.py`.
    - Zweck:
      Vorhandene Textinsel-Inner-Maps passiv auswerten und Wachstum trennen
      in stabilen Kern, rohen neuen Innenraum, weichen Variantenraum,
      Drift-Beobachtung und Rueckbindung durch Reproduktion.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Ausgaben:
      `passive_inner_universe_growth_stages.csv`,
      `passive_inner_universe_growth_transitions.csv`,
      `passive_inner_universe_growth_shared_details.csv`,
      `passive_inner_universe_growth.json`,
      `passive_inner_universe_growth.md`.
    - Messung C -> D -> E -> F:
      `debug/dio_mini_passive_inner_universe_growth_C_D_E_F_20260607_v1`.
      `C->D`: `shared=170`, `new=9`, `lost=0`.
      `D->E`: `shared=179`, `new=54`, `lost=0`.
      `E->F`: `shared=233`, `new=82`, `lost=0`.
    - Messung F-only -> F-G:
      `debug/dio_mini_passive_inner_universe_growth_F_only_to_F_G_20260607_v1`.
      `shared=161`, `new=35`, `lost=0`,
      `shared_delta_score=0.19114582`.
    - Messung G-only -> G-H:
      `debug/dio_mini_passive_inner_universe_growth_G_only_to_G_H_20260607_v1`.
      `shared=170`, `new=158`, `lost=0`,
      `shared_delta_score=0.048017436`.
    - Lesart:
      Die bisherigen Textinseln bleiben in diesen Messungen erhalten, waehrend
      neue Inseln hinzukommen. Das spricht fuer wachsende innere Organisation
      mit Realitaetsbindung, nicht fuer beliebige Erfindung.
    - Dokumentiert in:
      `DIO_BAUPLAN/konstruktion/42_DIO_MINI_DIAGNOSEMODULE.md`,
      `DIO_BAUPLAN/konstruktion/43_MCM_THEORIEANKER_EMERGENZ.md`.
    - Naechster Schritt:
      Entweder gezielte Hoer-Kontrastvariante bauen oder die vorhandenen
      Growth-Details mit der Lupe lesen: Welche stabilen Inseln tragen den
      Kern, welche neuen Inseln entstehen nur roh, welche driften?
174. Entwicklungslesart fuer nichtlineares Wachstum eingebaut:
    - Modul erweitert:
      `DIO_MINI/report_passive_inner_universe_growth.py`.
    - Neue passive Klassifikation:
      `plateau_stabilization`,
      `organic_expansion`,
      `jump_expansion_with_binding`,
      `reorganization_pressure`,
      `evolutionary_regression`,
      `open_evolutionary_motion`.
    - Neue Reports:
      `debug/dio_mini_passive_inner_universe_growth_C_D_E_F_20260607_v2`,
      `debug/dio_mini_passive_inner_universe_growth_F_only_to_F_G_20260607_v2`,
      `debug/dio_mini_passive_inner_universe_growth_G_only_to_G_H_20260607_v2`.
    - Befund:
      `C->D = plateau_stabilization`,
      `D->E = organic_expansion`,
      `E->F = organic_expansion`,
      `F_ONLY->F_G = reorganization_pressure`,
      `G_ONLY->G_H = jump_expansion_with_binding`.
    - Lesart:
      Nicht sauber exponentiell belegt, aber klar nicht linear ruhig.
      Besser: evolutionaere semantische Dynamik mit Plateau, Expansion,
      Sprung, Rueckbindung, Drift und moeglicher Reorganisation.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Growth-Details mit der Lupe lesen: Welche Textinseln bilden stabilen
      Kern, welche treiben Reorganisationsdruck, welche neuen Inseln sind nur
      rohe Erweiterung?
175. Passive Inner-Universe Lupe umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_inner_universe_lupe.py`.
    - Zweck:
      Konkrete Textinseln zweier Inner-Maps vergleichen und gruppieren:
      `stable_core`, `soft_variation_space`, `drift_watch`,
      `new_raw_extension`, `carried_raw_space`.
    - Neue Reports:
      `debug/dio_mini_passive_inner_universe_lupe_F_only_to_F_G_20260607_v1`,
      `debug/dio_mini_passive_inner_universe_lupe_G_only_to_G_H_20260607_v1`.
    - F-only -> F-G:
      `stable_core=87`,
      `new_raw_extension=35`,
      `carried_raw_space=26`,
      `soft_variation_space=26`,
      `drift_watch=22`.
    - G-only -> G-H:
      `new_raw_extension=158`,
      `carried_raw_space=133`,
      `stable_core=19`,
      `soft_variation_space=11`,
      `drift_watch=7`.
    - Lesart:
      F-G wirkt wie Reifung und Rueckbindung. G-H wirkt wie fremdere
      Weltvarianz mit starker roher Erweiterung, aber ohne Verlust der alten
      Textinseln.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Einzelne stabile Kerninseln und Drift-Inseln vergleichen: Welche
      dio_* Familien tauchen in beiden Uebergaengen wieder auf, und welche
      bleiben nur variantenspezifisch?
176. Passive Inner-Universe Cross-Lupe umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_inner_universe_cross_lupe.py`.
    - Zweck:
      Zwei Inner-Universe-Lupen auf dio_*-Familienebene vergleichen, damit
      sichtbar wird, welche Familien ueber unterschiedliche Weltvarianten
      wiederkehren und welche nur variantenspezifisch auftreten.
    - Report:
      `debug/dio_mini_passive_inner_universe_cross_lupe_FG_vs_GH_20260607_v1`.
    - Befund:
      `right_specific_family=239`,
      `recurrent_category_shift_family=170`,
      `recurrent_drift_family=47`,
      `left_specific_family=36`,
      `recurrent_stable_core_family=14`,
      `recurrent_variation_family=10`,
      `recurrent_carried_raw_family=8`.
    - Wiederkehrender stabiler Kern:
      `dio_06gy`, `dio_07t9`, `dio_0ft4`, `dio_0gmg`, `dio_0nrp`,
      `dio_0ocv`, `dio_0pni`, `dio_0t27`, `dio_17ny`, `dio_19bg`,
      `dio_1a1w`, `dio_1fck`, `dio_1jba`, `dio_1si6`.
    - Wiederkehrender Variantenraum:
      `dio_03yz`, `dio_095l`, `dio_0g9z`, `dio_0x52`, `dio_0xkp`,
      `dio_140n`, `dio_1ffn`, `dio_1i05`, `dio_1lg2`, `dio_1ocs`.
    - Lesart:
      Ein kleiner, konkreter Familienkern bleibt ueber F-G und G-H stabil.
      Gleichzeitig zeigen 170 Kategorieverschiebungen, dass Bedeutung nicht
      starr kopiert wird, sondern unter neuer Weltvarianz umgeordnet wird.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Die 14 stabilen Kernfamilien mit ihren Textinseln genauer lesen:
      Sind sie echte Anker des inneren Universums oder nur kurze
      formale Wiederholungen?
177. Passive Inner-Core Anchor Lupe umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_inner_core_anchor_lupe.py`.
    - Zweck:
      Die stabilen und wiederkehrenden Familien aus der Cross-Lupe danach
      klassifizieren, ob sie tiefe Anker, flache Einzelformen,
      Variantenbruecken, Drift-Anker oder Kategorieverschiebungen sind.
    - Report:
      `debug/dio_mini_passive_inner_core_anchor_lupe_FG_vs_GH_20260607_v1`.
    - Befund:
      `category_shift_anchor=170`,
      `drift_sensitive_anchor=47`,
      `exact_single_form_anchor=14`,
      `variant_bridge_anchor=10`.
    - Lesart:
      Die 14 stabilen Kernfamilien sind exakt wiederkehrende Einzelformen:
      gleiche Familie, gleiche Textinsel, `stable_core -> stable_core`,
      minimale Score-Abweichung. Das ist stabile Realitaetsbindung, aber
      noch flach.
    - Wichtiger Satz:
      `Stabiler Kern != automatisch tiefer Kern.`
    - Vertiefung:
      Tiefere Anker zeigen sich eher bei `variant_bridge_anchor`, weil dort
      die Familie wiederkehrt, aber die Textinsel wechseln darf. Das ist
      naeher an tragender Semantik unter Varianz.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Die 10 `variant_bridge_anchor` genauer lesen. Dort liegt vermutlich
      die interessantere Schicht: gleiche innere Familie, aber wechselnde
      Textinsel als Zeichen semantischer Beweglichkeit.
178. Passive Variant Bridge Lupe umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_variant_bridge_lupe.py`.
    - Zweck:
      `variant_bridge_anchor` nach Textinsel-Uebergang gruppieren, um zu
      pruefen, ob mehrere Familien denselben semantischen Wechsel tragen.
    - Report:
      `debug/dio_mini_passive_variant_bridge_lupe_FG_vs_GH_20260607_v1`.
    - Befund:
      `shared_variant_bridge`:
      `dio_text_15hzmqv -> dio_text_jwkf1a`,
      Familien `dio_095l`, `dio_0g9z`, `dio_0xkp`, `dio_1ocs`,
      `avg_delta=-0.052447867`.
    - Befund:
      `strengthening_variant_bridge`:
      `dio_text_1456g6j -> dio_text_1ne15hk`,
      Familien `dio_0x52`, `dio_1lg2`,
      `avg_delta=0.079008733`.
    - Befund:
      `thin_variant_bridge`:
      `dio_text_mr2id7 -> dio_text_zle8sl`,
      Familien `dio_1ffn`, `dio_1i05`,
      `avg_delta=-0.011845333`.
    - Lesart:
      Die interessanteste Bruecke ist aktuell `dio_0x52 | dio_1lg2`, weil
      sie denselben Textinselwechsel traegt und sich dabei verstaerkt.
      Das ist ein besserer Kandidat fuer semantische Tiefe als ein exakt
      wiederholter Einzelform-Anker.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      `dio_0x52 | dio_1lg2` als Bruecken-Kandidat ueber weitere Varianten
      oder frische Reproduktion pruefen.
179. Passive Family Bridge Lineage fuer `dio_0x52 | dio_1lg2` umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_family_bridge_lineage.py`.
    - Zweck:
      Ausgewaehlte dio_*-Familien ueber mehrere passive Inner-Maps verfolgen,
      um Reifung, Drift, Textinselwechsel und erneute Staerkung sichtbar zu
      machen.
    - Report:
      `debug/dio_mini_passive_family_bridge_lineage_dio_0x52_dio_1lg2_20260607_v1`.
    - Befund `dio_0x52`:
      Sichtbar in `C|D|E|F|F_G|G_H`.
      Textinsel-Sequenz:
      `dio_text_cmxrx4 -> dio_text_cmxrx4 -> dio_text_cmxrx4 -> dio_text_cmxrx4 -> dio_text_1456g6j -> dio_text_1ne15hk`.
      Score:
      `0.6272642 -> 0.658346867 -> 0.673354733 -> 0.572545067 -> 0.393777267 -> 0.472786`.
    - Befund `dio_1lg2`:
      Sichtbar in `F_G|G_H`.
      Textinsel-Sequenz:
      `dio_text_1456g6j -> dio_text_1ne15hk`.
      Score:
      `0.393777267 -> 0.472786`.
    - Lesart:
      `dio_0x52` ist kein kurzer Einmalanker. Die Familie reift, driftet,
      wechselt Textinsel und staerkt sich spaeter zusammen mit `dio_1lg2`.
      Das ist ein Kandidat fuer semantische Beweglichkeit im inneren
      Universum.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Diesen Kandidaten mit frischer Reproduktion oder weiterer Variante
      pruefen. Entscheidend ist, ob `dio_0x52` wieder eine vergleichbare
      Reifung/Drift/Brueckenbewegung zeigt.
180. F-Repro gegen `dio_0x52 | dio_1lg2` geprueft:
    - Report:
      `debug/dio_mini_passive_family_bridge_lineage_dio_0x52_dio_1lg2_F_vs_F_repro_20260607_v1`.
    - Befund `dio_0x52`:
      In `F` sichtbar als `dio_text_cmxrx4`,
      `inner_drift_watch_space`, Score `0.572545067`.
      In `F_REPRO` sichtbar als `dio_text_1456g6j`,
      `inner_stable_recurrence_space`, Score `0.476246133`.
    - Befund `dio_1lg2`:
      In diesem F-Repro-Schnitt nicht sichtbar.
    - Lesart:
      `dio_0x52` reproduziert sich als Familie, aber nicht als identische
      Textinsel-Kopie. Die Familie bewegt sich von Drift-Beobachtung in
      stabilere Wiederkehr. Das ist eher organische Bedeutungsumordnung als
      mechanisches Kopieren.
    - Grenze:
      Die Bruecke `dio_0x52 | dio_1lg2` ist dadurch noch nicht voll
      reproduziert, sondern bleibt ein starker Kandidat fuer weitere
      kontrollierte Varianten.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Eine kontrollierte Repro-Kette mit F-G/G-H-Logik pruefen. Entscheidend
      ist, ob `dio_1lg2` wieder an `dio_0x52` koppelt oder ob `dio_0x52`
      allein als bewegliche Familie weiterreift.
181. Passive Inner-Universe Repro Pipeline ergaenzt:
    - Neues Modul:
      `DIO_MINI/run_passive_inner_universe_repro_pipeline.py`.
    - Zweck:
      Standardisierte passive Repro-Kette fuer kontrollierte Varianten F/G/H:
      Mini-DIO-Runs, Meaning-Space, Neighbor, Semantic Matrix, Density,
      diagnostische Semantic-Matrix-Memory, Textinsel-Reife, Innenkarte und
      optionaler Vergleich/Lineage.
    - Geprueft:
      `python -m py_compile DIO_MINI\run_passive_inner_universe_repro_pipeline.py`
      erfolgreich.
    - Dry-Run:
      Variante F mit `dio_0x52` und `dio_1lg2` gegen F-Original aufgeloest.
      Alle Probe20-26-Datenpfade und Report-Kommandos wurden korrekt
      gebildet.
    - Wirkungsgrenze:
      reine Diagnose-Orchestrierung. Keine Runtime-Lesung, keine Handlung,
      kein Gate, kein Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Bei Bedarf die Pipeline real fuer F-G/G-H-Reproduktion laufen lassen und
      danach pruefen, ob die Bruecke `dio_0x52 | dio_1lg2` erneut entsteht.
182. G-Repro gegen F-Repro ausgefuehrt:
    - Pipeline:
      `DIO_MINI/run_passive_inner_universe_repro_pipeline.py`.
    - Fix waehrend der Ausfuehrung:
      Pipeline-Pfade fuer `passive_cluster_meaning_space.csv`,
      `passive_cluster_neighbors.csv` und `passive_text_island_maturity.csv`
      korrigiert. Die Reportmodule erwarten CSV-Dateien, nicht Ordner.
    - Outputs:
      `debug/dio_mini_passive_semantic_matrix_6episoden_varianteG_repro_check_20260607_v1`,
      `debug/dio_mini_passive_text_island_inner_map_varianteG_repro_check_20260607_v1`,
      `debug/dio_mini_passive_family_bridge_lineage_varianteG_repro_check_20260607_v1`.
    - Matrixvergleich F_REPRO -> G_REPRO:
      `node_count_reference=253`,
      `node_count_candidate=277`,
      `shared_node_count=207`,
      `node_reproduction_rate=0.818182`,
      `edge_count_reference=120`,
      `edge_count_candidate=12`,
      `shared_edge_count=1`,
      `edge_reproduction_rate=0.008333`,
      `island_count_reference=161`,
      `island_count_candidate=265`.
    - Innenkartenvergleich:
      `stable_recurrence=105`,
      `new_in_right_inner_map=160`,
      `missing_in_right_inner_map=56`.
    - Befund `dio_0x52`:
      F_REPRO und G_REPRO bleiben beide auf `dio_text_1456g6j` im
      `inner_stable_recurrence_space`. Score steigt von `0.476246133` auf
      `0.483333333`.
    - Befund `dio_1lg2`:
      In G_REPRO wieder sichtbar, aber als eigene Textinsel
      `dio_text_13ycr5k`, ebenfalls `inner_stable_recurrence_space`, Score
      `0.483333333`.
    - Lesart:
      Die Bruecke `dio_0x52 | dio_1lg2` wurde nicht als gemeinsame Textinsel
      reproduziert. Stattdessen stabilisiert sich `dio_0x52` und `dio_1lg2`
      erscheint separat. Das zeigt Wiederkehr auf Familienebene, aber
      Reorganisation auf Beziehungsebene.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      H-Repro als Strukturkontrast ausfuehren oder zuerst die G-Repro-Kanten
      genauer lesen. Entscheidend ist, ob die getrennten Inseln spaeter wieder
      Naehe finden oder stabil getrennt bleiben.
183. H-Repro und G-Kantenpruefung parallel ausgefuehrt:
    - H-Repro Pipeline:
      `DIO_MINI/run_passive_inner_universe_repro_pipeline.py`.
    - Outputs H:
      `debug/dio_mini_passive_semantic_matrix_6episoden_varianteH_repro_check_20260607_v1`,
      `debug/dio_mini_passive_text_island_inner_map_varianteH_repro_check_20260607_v1`,
      `debug/dio_mini_passive_family_bridge_lineage_varianteH_repro_check_20260607_v1`.
    - Matrixvergleich G_REPRO -> H_REPRO:
      `node_count_reference=277`,
      `node_count_candidate=300`,
      `shared_node_count=63`,
      `node_reproduction_rate=0.227437`,
      `edge_count_reference=12`,
      `edge_count_candidate=12`,
      `shared_edge_count=0`,
      `edge_reproduction_rate=0.0`,
      `island_count_reference=265`,
      `island_count_candidate=288`.
    - Innenkartenvergleich:
      `inner_state_softened=56`,
      `missing_in_right_inner_map=209`,
      `new_in_right_inner_map=232`.
    - Lineage `dio_0x52`:
      G_REPRO: `dio_text_1456g6j`, `inner_stable_recurrence_space`,
      Score `0.483333333`.
      H_REPRO: gleiche Textinsel, aber `inner_unconfirmed_raw_space`,
      Score `0.206666667`.
    - Lineage `dio_1lg2`:
      G_REPRO: `dio_text_13ycr5k`, `inner_stable_recurrence_space`,
      Score `0.483333333`.
      H_REPRO: gleiche Textinsel, aber `inner_unconfirmed_raw_space`,
      Score `0.206666667`.
    - Kantenpruefung:
      In G_REPRO und H_REPRO gibt es keine direkte Matrix- oder Neighbor-Kante
      an `dio_0x52` oder `dio_1lg2`.
    - Node-Befund:
      G_REPRO `dio_0x52`: `episodes=8`, `mcm_coherence=0.979900`,
      `matrix_node_state=recurring_raw_semantic_trace`.
      G_REPRO `dio_1lg2`: `episodes=2`, `mcm_coherence=0.970369`,
      `matrix_node_state=raw_semantic_trace`.
      H_REPRO beide: `episodes=2`, hohe MCM-Kohaerenz, aber rohe
      Syntaxspuren.
    - Lesart:
      H bestaetigt den Strukturkontrast. Syntaxnamen bleiben sichtbar,
      aber Reife und Beziehungskanten tragen nicht. Das trennt Wort,
      Feldkohaerenz und semantische Beziehung sauberer.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Einen gezielten Bericht fuer "Syntax bleibt, Reife kippt" bauen. Dieser
      soll Familien markieren, die unter Strukturkontrast ihren Namen behalten,
      aber von stabiler Wiederkehr in rohen Raum fallen.
184. Passiver Bericht "Syntax bleibt, Reife kippt" umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_syntax_maturity_shift.py`.
    - Pipeline erweitert:
      `DIO_MINI/run_passive_inner_universe_repro_pipeline.py` fuehrt den
      Bericht automatisch aus, wenn `--compare-inner-map` gesetzt ist.
    - Report:
      `debug/dio_mini_passive_syntax_maturity_shift_G_REPRO_vs_H_REPRO_20260607_v1`.
    - Ergebnis G_REPRO -> H_REPRO:
      `compared_anchors=63`,
      `syntax_survives_reife_kippt=63`,
      davon `text_island_anchors=56` und `family_anchors=7`.
      Durchschnittlich faellt der Score um `-0.276772486`, Rawness steigt um
      `+0.276772486`.
    - Kernbeispiele:
      `dio_0x52` bleibt auf `dio_text_1456g6j`, kippt aber von
      `inner_stable_recurrence_space` nach `inner_unconfirmed_raw_space`.
      `dio_1lg2` bleibt auf `dio_text_13ycr5k`, kippt ebenfalls von stabil
      nach roh.
    - Lesart:
      Mini-DIO kann Syntax reproduzieren, ohne dass Reife automatisch
      reproduziert wird. Damit sind Syntax, MCM-Kohaerenz, Beziehung und
      Reife als getrennte Ebenen messbar.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Die gekippten Anker gegen die zugrunde liegenden Sensor-/Feldlagen
      legen: bleibt die Syntax wegen gleicher Wahrnehmung erhalten, oder
      bleibt sie nur als roher Name ohne tragenden Zusammenhang sichtbar?
185. Passiver Sensor-/Feldabgleich fuer gekippte Syntaxanker umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_shift_sensory_field_alignment.py`.
    - Pipeline erweitert:
      `DIO_MINI/run_passive_inner_universe_repro_pipeline.py` kann den Bericht
      automatisch erzeugen, wenn neben `--compare-inner-map` auch
      `--compare-meaning-space` gesetzt ist.
    - Report:
      `debug/dio_mini_passive_shift_sensory_field_alignment_G_REPRO_vs_H_REPRO_20260607_v1`.
    - Ergebnis:
      `families=63`.
      `same_sensory_field_visible=34`,
      `same_sensory_field_but_reife_kippt=11`,
      `same_sensory_field_but_less_lived_support=8`,
      `near_mcm_field_with_sensory_variation=9`,
      `syntax_survives_but_context_changed=1`.
    - Befund `dio_0x52`:
      gleiche Textinsel `dio_text_1456g6j`, Episoden `8 -> 2`,
      `sensory_field_distance=0.007631226`,
      MCM-Kohaerenz `0.979900 -> 0.981866`,
      Zustand `same_sensory_field_but_less_lived_support`.
    - Befund `dio_1lg2`:
      gleiche Textinsel `dio_text_13ycr5k`, Episoden `2 -> 2`,
      `sensory_field_distance=0.011317391`,
      MCM-Kohaerenz `0.970369 -> 0.980784`,
      Zustand `same_sensory_field_but_reife_kippt`.
    - Lesart:
      In diesem Vergleich bricht nicht zuerst die Wahrnehmungsnaehe. Sehen,
      Hoeren und Fuehlen bleiben haeufig nah. Die Reife kippt trotzdem, weil
      gelebte Bestaetigung und tragende Integration nicht automatisch aus
      Aehnlichkeit entstehen.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Die Kippung zeitlich untersuchen: An welcher Episoden-/Probegrenze
      verliert eine aehnliche Sinneslage ihre Reife? Das ist der naechste
      Hinweis auf Reorganisation statt einfacher Kopie.
186. Passiver Richtungs-/Weltstuetzungsbericht umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_direction_support_shift.py`.
    - Report:
      `debug/dio_mini_passive_direction_support_shift_G_REPRO_vs_H_REPRO_20260607_v1`.
    - Der Bericht liest die gekippten Familien und prueft episodisch:
      `best_action_training`, `observation_learning_action`,
      `best_reward_training`, `trade_readiness`, Episodenzahl,
      Zeitstatus und Neuroton.
    - Ergebnis ueber Probe20 bis Probe26:
      `families=63`,
      `same_sensory_field_same_direction_but_reife_kippt=41`,
      `same_sensory_field_less_lived_direction_support=8`,
      `direction_support_reorganized=8`,
      `direction_support_flips=4`,
      `same_sensory_field_direction_reward_weakens=2`.
    - Befund `dio_0x52`:
      Richtung bleibt `SHORT -> SHORT`,
      Beobachtungsrichtung bleibt `SHORT -> SHORT`,
      hypothetischer Best-Reward bleibt `1.0 -> 1.0`,
      Episoden fallen `8 -> 2`,
      Trade-Readiness faellt `0.025963375 -> 0.0037115`.
      Lesart: gleiche Richtung, gleiche Sinnesnaehe, aber weniger gelebte
      Richtungsstuetzung.
    - Befund `dio_1lg2`:
      Richtung bleibt `SHORT -> SHORT`,
      Beobachtungsrichtung bleibt `SHORT -> SHORT`,
      hypothetischer Best-Reward bleibt `1.0 -> 1.0`,
      Episoden bleiben `2 -> 2`.
      Lesart: Richtung bleibt sichtbar, Reife kippt trotzdem.
    - Gesamtlesart:
      Die Kippung entsteht nicht nur durch falsche Richtung. Oft bleibt
      Richtung erhalten. Wahrscheinlicher ist: eine innere Ordnung oder ein
      emergenter Gedanke bleibt sichtbar, wird aber von der Aussenwelt nicht
      mehr stabil genug getragen.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Die Probefolge zeitlich aufschluesseln: welche Familien kippen zuerst,
      und entsteht vor dem Kippen Drift in Zeitstatus, Neuroton oder
      Trade-Readiness?
187. Begriff "situationsbedingter emergenter Gedanke" festgehalten:
    - Erkenntnis:
      Ein emergenter Gedanke kann sichtbar bleiben, wird aber von der
      Aussenwelt nicht immer stabil genug getragen.
    - Bedeutung:
      Dadurch entstehen situative Daten, die nicht programmiert sind. Sie
      entstehen aus Wahrnehmung, MCM-Feldlage, Zeitkontakt, Wiederkehr und
      Weltreaktion.
    - Wichtig:
      Diese Spur ist keine absolute Realitaet und kein Handlungssignal. Sie ist
      eine passive innere Ordnungsform im Kontext.
    - Fachliche Trennung:
      Syntax kann bleiben, Sinnesnaehe kann bleiben, Richtung kann sichtbar
      bleiben, aber Reife und getragene Einbettung koennen trotzdem kippen.
    - Dokumentiert in:
      `DIO_BAUPLAN/konstruktion/42_DIO_MINI_DIAGNOSEMODULE.md` und
      `DIO_BAUPLAN/konstruktion/43_MCM_THEORIEANKER_EMERGENZ.md`.
    - Naechster Schritt:
      Zeitliche Kipp-Punkte passiv markieren: Wann wird aus einer stabilen
      situativen Spur eine rohe, driftende oder fragmentierte Spur?
188. Passiver Bericht fuer zeitliche Kipp-Punkte umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_temporal_kipp_points.py`.
    - Report:
      `debug/dio_mini_passive_temporal_kipp_points_G_REPRO_vs_H_REPRO_20260607_v1`.
    - Der Bericht vergleicht die gekippten Familien ueber Probe20 bis Probe26
      und markiert den ersten sichtbaren Bruch:
      Richtungsflip, Beobachtungsrichtungsflip, Verlust gelebter
      Episodenstuetzung, abgeschwaechter hypothetischer Weltnutzen,
      weichere Trade-Readiness oder Neuro-/Zeit-Umordnung.
    - Ergebnis:
      `families=63`, `detail_rows=161`.
      `family_loses_lived_support=39`,
      `family_no_visible_temporal_kipp=8`,
      `family_neuro_temporal_reorganizes=7`,
      `family_trade_readiness_softens=5`,
      `family_has_direction_flip=3`,
      `family_best_reward_softens=1`.
    - Befund `dio_0x52`:
      `family_loses_lived_support`.
      Erster Kipp-Punkt `probe20 / probe_lived_support_drop`.
      Danach erneut Stuetzungsverlust, dann `trade_readiness_softens`,
      danach wieder Stuetzungsverlust.
    - Befund `dio_1lg2`:
      Ebenfalls `family_loses_lived_support`, aber erster sichtbarer Bruch ist
      `probe20 / probe_neuro_tone_reorganizes`, danach
      `probe_lived_support_drop`.
    - Lesart:
      Der haeufigste Bruch ist nicht Richtungsflip. Die Spur bleibt als
      Syntax/Ordnung sichtbar, verliert aber gelebte Breite in der Weltfolge.
      Damit wird "getragen sein" als eigene MCM-Groesse sichtbar.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Aus den Kipp-Punkten eine passive "Tragekurve" bauen: Wie lange bleibt
      eine situative Spur getragen, bevor sie roher, driftender oder
      fragmentierter wird?
189. Passive Tragekurve umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_trace_carry_curve.py`.
    - Report:
      `debug/dio_mini_passive_trace_carry_curve_G_REPRO_vs_H_REPRO_20260607_v1`.
    - Der Bericht liest:
      `passive_temporal_kipp_points_detail.csv` und
      `passive_temporal_kipp_points_families.csv`.
    - Ergebnis:
      `families=63`, `probes=7`.
      `trace_immediate_or_continuous_kipp=46`,
      `trace_fully_carried=8`,
      `trace_carries_then_kipps=3`,
      `trace_kipps_then_recarries=3`,
      `trace_mixed_mostly_kipped=3`.
    - Probe-Kurve:
      `probe20 carry_ratio=0.040000000`,
      `probe21 carry_ratio=0.058823529`,
      `probe22 carry_ratio=0.103448276`,
      `probe23 carry_ratio=0.350000000`,
      `probe24 carry_ratio=0.076923077`,
      `probe25 carry_ratio=0.173913043`,
      `probe26 carry_ratio=0.095238095`.
    - Befund `dio_0x52`:
      `trace_immediate_or_continuous_kipp`, sichtbar in 4 Proben, getragen in
      0 Proben. Dominanter Bruch: `probe_lived_support_drop`.
    - Befund `dio_1lg2`:
      `trace_immediate_or_continuous_kipp`, sichtbar in 2 Proben, getragen in
      0 Proben. Erster Bruch: `probe_neuro_tone_reorganizes`.
    - Befund `dio_11vr`:
      `trace_fully_carried`, sichtbar in 3 Proben, getragen in 3 Proben,
      Textinsel bleibt `dio_text_38zk5e`.
    - Lesart:
      Sichtbarkeit ist noch keine Reife. Eine situative Spur muss ueber
      Weltkontakt getragen bleiben. Tragedauer wird damit als passive
      Entwicklungsqualitaet messbar.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Naechster Schritt:
      Die getragenen Familien wie `dio_11vr` mit den sofort kippenden Familien
      vergleichen: Welche Sensor-/Feld-/Zeitstruktur unterscheidet stabile
      Tragung von sofortiger Kippung?
190. Passive Carry Contrast umgesetzt:
    - Neues Modul:
      `DIO_MINI/report_passive_carry_contrast.py`.
    - Report:
      `debug/dio_mini_passive_carry_contrast_G_REPRO_vs_H_REPRO_20260607_v1`.
    - Der Bericht vergleicht getragene situative Spuren mit sofort oder
      dauerhaft kippenden Spuren. Verknüpft werden Tragekurve,
      Sensor-Feld-Abstand, Richtung, gelebte Stützung und neurotonale
      Umordnung.
    - Ergebnis:
      `families=63`.
      `immediate_or_continuous_kipp_trace=46`,
      `single_probe_carried_trace=7`,
      `carries_then_kipps_trace=3`,
      `kipps_then_recarries_trace=3`,
      `mixed_or_unclear_trace=3`,
      `multi_probe_carried_trace=1`.
    - Stärkster Kandidat:
      `dio_11vr`.
      Sichtbar in 3 Proben, getragen in 3 Proben,
      Textinsel `dio_text_38zk5e -> dio_text_38zk5e`,
      `sensory_field_distance=0.004459482`,
      keine gelebte Stützungsabnahme,
      keine neurotonale Umordnung.
    - Kontrast:
      `dio_0x52` und `dio_1lg2` bleiben syntaktisch sichtbar, kippen aber im
      Tragen. Damit ist Sichtbarkeit nicht gleich Reife.
    - Lesart:
      Stabile Tragung braucht wiederkehrende Form/Feld-Nähe plus erhaltene
      gelebte Stützung. Eine Syntax kann sichtbar bleiben und trotzdem nicht
      getragen sein.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Nächster Schritt:
      Für `dio_11vr` ein passives Trageprofil bauen und kippende Familien
      dagegen legen. Ziel ist nicht Handlung, sondern die Frage: Welche
      innere Struktur macht eine emergente Spur tragfähig?
191. Passive Repro-Pipeline erweitert:
    - Datei:
      `DIO_MINI/run_passive_inner_universe_repro_pipeline.py`.
    - Ergänzt wurden optionale Argumente für:
      `--temporal-kipp-direction`,
      `--temporal-left-debug-root`,
      `--temporal-right-debug-root`,
      `--build-trace-carry-curve`,
      `--build-carry-contrast`.
    - Die Pipeline kann damit Temporal-Kipp-Punkte, Tragekurve und
      Carry-Contrast reproduzierbar nachbauen, sofern die benötigten
      Referenzdaten angegeben werden.
    - `--temporal-left-debug-root` und `--temporal-right-debug-root` können
      mehrfach gesetzt werden, damit Mehr-Proben-Vergleiche erhalten bleiben.
    - Prüfung:
      Import mit `python -B` erfolgreich.
      Dry-Run erzeugt die erwarteten Temporal- und Trace-Carry-Befehle.
      `py_compile` wurde durch Windows-`__pycache__`-Replace blockiert
      (`WinError 5`), nicht durch Syntax.
192. Passives Trageprofil für `dio_11vr` gebaut:
    - Neues Modul:
      `DIO_MINI/report_passive_carry_profile.py`.
    - Report:
      `debug/dio_mini_passive_carry_profile_dio_11vr_G_REPRO_vs_H_REPRO_20260607_v1`.
    - Referenz:
      `dio_11vr`,
      `multi_probe_carried_trace`,
      `trace_fully_carried`,
      3 sichtbare Proben,
      3 getragene Proben,
      Textinsel `dio_text_38zk5e`.
    - Nächste Gegenlage:
      `dio_0ocv`.
      Lesart:
      `weak_carried_like_reference_needs_more_world_contact`.
    - Korrektur:
      Ein-Proben-Träger werden nicht als volle stabile Reife gelesen. Sie sind
      ähnlich, brauchen aber mehr Weltkontakt.
    - Lesart:
      Reife ist nicht nur Form-/Feldnähe. Reife braucht Tragedauer über
      wiederholten Weltkontakt.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Nächster Schritt:
      Die Ein-Proben-Träger gezielt in einer weiteren kontrollierten Variante
      prüfen: werden sie zu Mehr-Proben-Trägern, kippen sie, oder bleiben sie
      nur kurze situative Aufleuchtungen?
193. Passive Follow-Up-Kandidaten für schwache Träger gebaut:
    - Neues Modul:
      `DIO_MINI/report_passive_carry_followup_candidates.py`.
    - Report:
      `debug/dio_mini_passive_carry_followup_candidates_dio_11vr_G_REPRO_vs_H_REPRO_20260607_v1`.
    - Ergebnis:
      7 Kandidaten.
      `high=2`, `medium=4`, `low=1`.
    - High-Kandidaten:
      `dio_0ocv`,
      `dio_1fck`.
    - Medium-Kandidaten:
      `dio_0rwa`,
      `dio_1ndv`,
      `dio_19b6`,
      `dio_0bde`.
    - Low-Kandidat:
      `dio_0jx1`.
    - Lesart:
      Diese Familien sind keine stabile Reife, sondern mögliche Keime. Die
      nächste Prüfung ist, ob sie bei mehr Weltkontakt zu Mehr-Proben-Trägern
      werden oder kippen.
    - Pipeline:
      `DIO_MINI/run_passive_inner_universe_repro_pipeline.py` kann jetzt
      optional nach Carry-Contrast auch Carry-Profile und Follow-Up-Kandidaten
      bauen:
      `--carry-profile-family`,
      `--carry-profile-topn`,
      `--build-carry-followup-candidates`,
      `--carry-followup-limit`.
    - Prüfung:
      Import mit `python -B` erfolgreich.
      Dry-Run zeigt die korrekte Reihenfolge:
      Carry-Contrast -> Carry-Profile -> Follow-Up-Kandidaten.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Nächster Schritt:
      Eine weitere kontrollierte Weltvariante oder Reproduktion gegen diese
      Kandidaten laufen lassen und prüfen:
      `dio_0ocv` / `dio_1fck` werden stabiler, kippen oder bleiben situativ.
194. Passive Follow-Up-Ergebnisauswertung vorbereitet:
    - Neues Modul:
      `DIO_MINI/report_passive_carry_followup_result.py`.
    - Selfcheck-Report:
      `debug/dio_mini_passive_carry_followup_result_selfcheck_dio_11vr_G_REPRO_vs_H_REPRO_20260607_v1`.
    - Funktion:
      Eine spätere Carry-Contrast-Datei wird gegen die Kandidatenliste gelegt.
      Pro Kandidat wird bewertet:
      `matured_to_multi_probe_carried`,
      `still_single_probe_carried`,
      `partial_carry_with_kipp`,
      `kipped_in_followup`,
      `candidate_not_visible_in_followup`.
    - Selfcheck:
      Gegen denselben G_REPRO/H_REPRO-Kontrast bleiben alle 7 Kandidaten
      `still_single_probe_carried`. Das ist erwartbar, weil noch keine neue
      Weltvariante vorliegt.
    - Wirkungsgrenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate, kein
      Entry-Signal, kein Richtungssignal.
    - Nächster Schritt:
      Neuer kontrollierter Repro-/Variantenlauf. Danach diesen Result-Report
      mit der neuen Carry-Contrast-Datei laufen lassen.
195. Variante I als Weltkontakt-Folgeprüfung erstellt:
    - Neues Modul:
      `DIO_MINI/create_controlled_variant_i.py`.
    - Erzeugt wurden 7 CSV-Dateien:
      Probe20 bis Probe26 mit `varianteI_weltkontakt`.
    - Quelle:
      Variante H.
    - Wirkung:
      Nur OHLCV wird deterministisch leicht weitergeführt.
      Keine Mini-DIO-Logik, kein Gate, kein Entry, kein Memory-Eingriff.
    - Prüfung:
      Import erfolgreich.
      CSV-Dateien wurden geschrieben.
196. Variante I gelaufen und passiv gegen H ausgewertet:
    - Lauf:
      `python -m DIO_MINI.run_passive_inner_universe_repro_pipeline`
      mit Variante `I`, Tag `weltkontakt`, `runs=2`, Probes 20..26.
    - Runtime-Memory:
      `bot_memory/dio_mini_repro_pipeline_I_runtime_memory_20260607.json`.
    - Semantic-Memory:
      `bot_memory/dio_mini_passive_repro_pipeline_I_semantic_matrix_memory_20260607.json`.
    - Basisbefund:
      916 Episoden, 0 Trades, rein passiv.
      `clusters=310`, `nodes=310`, `text_islands=298`.
    - H -> I Shift:
      `syntax_survives_raw=241`.
      Sensorfeld:
      `same_sensory_field_visible=244`,
      `near_mcm_field_with_sensory_variation=3`.
    - Direction-Support:
      `same_sensory_field_same_direction_but_reife_kippt=242`,
      `direction_support_reorganized=3`,
      `same_sensory_field_direction_reward_weakens=1`,
      `direction_support_not_visible_right=1`.
    - Temporal-Kipp:
      `family_no_visible_temporal_kipp=96`,
      `family_trade_readiness_softens=86`,
      `family_loses_lived_support=30`,
      `family_best_reward_softens=28`,
      `family_neuro_temporal_reorganizes=6`,
      `family_has_direction_flip=1`.
    - Tragekurve:
      `trace_fully_carried=96`,
      `trace_immediate_or_continuous_kipp=123`,
      `trace_carries_then_kipps=15`,
      `trace_kipps_then_recarries=9`,
      `trace_mixed_mostly_carried=3`,
      `trace_mixed_mostly_kipped=1`.
197. Follow-Up-Kandidaten gegen Variante I geprüft:
    - Report:
      `debug/dio_mini_passive_carry_followup_result_dio_11vr_H_REPRO_vs_I_WELTKONTAKT_20260607_v1`.
    - Ergebnis:
      `still_single_probe_carried=4`,
      `kipped_in_followup=2`,
      `candidate_not_visible_in_followup=1`.
    - Weiterhin Ein-Proben-Träger:
      `dio_0ocv`,
      `dio_0rwa`,
      `dio_19b6`,
      `dio_0jx1`.
    - Gekippt:
      `dio_1ndv`,
      `dio_0bde`.
    - Nicht erneut sichtbar:
      `dio_1fck`.
    - Referenz:
      `dio_11vr` bleibt in H/I erneut `multi_probe_carried_trace`:
      visible=3, carried=3, carry_ratio=1.0,
      Textinsel `dio_text_38zk5e -> dio_text_38zk5e`.
    - Lesart:
      Die schwachen Kandidaten aus G/H zeigen noch keine Mehr-Proben-Reife.
      `dio_11vr` wird dagegen als stabile emergente Tragespur stärker
      bestätigt.
198. Passive Repro-Pipeline weiter geschlossen:
    - Datei:
      `DIO_MINI/run_passive_inner_universe_repro_pipeline.py`.
    - Neu:
      `--build-direction-support-shift`.
    - Neu:
      `--carry-followup-candidates`.
    - Damit kann die Pipeline jetzt Direction-Support, Temporal-Kipp,
      Tragekurve, Carry-Contrast und Follow-Up-Result in einem passiven
      Ablauf reproduzieren.
    - Prüfung:
      Import erfolgreich.
      Dry-Run zeigt die erwarteten Befehle für
      `report_passive_direction_support_shift` und
      `report_passive_carry_followup_result`.
199. Passive Carry Separator gebaut:
    - Datei:
      `DIO_MINI/report_passive_carry_separator.py`.
    - Report:
      `debug/dio_mini_passive_carry_separator_dio_11vr_H_REPRO_vs_I_WELTKONTAKT_20260607_v1`.
    - Zweck:
      Trennung zwischen stabil getragener Referenzspur und schwachen
      Keimen.
    - Referenz:
      `dio_11vr`, visible=3, carried=3, carry_ratio=1.0,
      Textinsel `dio_text_38zk5e`.
    - Ergebnis:
      `weak_single_contact_keim=4`,
      `kipped_under_world_contact=2`,
      `not_reproduced=1`.
    - Lesart:
      `dio_11vr` ist stabiler als die bisherigen Keime.
      Die schwachen Kandidaten sind keine Fehler, aber noch keine Reife.
      Einmalige Tragung reicht nicht; wiederholter Weltkontakt trennt
      Aufleuchten von Tragespur.
    - Grenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate,
      kein Entry-Signal, kein Richtungssignal.
219. Passive Folgewelt P und LMNOP-Latent-Island-Fortsetzung gebaut:
    - Datei:
      `DIO_MINI/create_controlled_variant_p.py`.
    - Erzeugte Daten:
      `kontrolliert_sensor_relation_probe20..26_*_6episoden_varianteP_folgekontakt7_5m_SOLUSDT.csv`.
    - Pipeline:
      Variante `P`, Tag `folgekontakt7`, Vergleich gegen `O_FOLGEKONTAKT6`.
    - Matrixvergleich O -> P:
      `node_reproduction_rate=0.950166`,
      `edge_reproduction_rate=0.75`,
      `shared_node_count=286`,
      `shared_edge_count=9`,
      `island_count_reference=289`,
      `island_count_candidate=294`.
    - Inner-Spacetime-Autoscan L/M/N/O/P:
      `spacetime_latent_persistent_trace=233`,
      `spacetime_fading_trace=143`,
      `spacetime_stable_coupled_core=2`,
      `spacetime_open_trace=1`.
    - Latent-Island-Lupe L/M/N/O/P:
      `candidate_count=233`,
      `total_latent_edge_count=17`,
      `total_nontrivial_component_count=17`,
      `max_largest_component_size=2`.
    - Stufen:
      L/M/N jeweils `latent_edge_count=3`.
      O/P jeweils `latent_edge_count=4`.
      O/P jeweils `connected_latent_family_count=8`,
      `isolated_latent_family_count=225`.
    - Paarbewegung:
      Durchgehend stabil:
      `dio_07kj|dio_09u3`,
      `dio_0r8l|dio_10xx`.
      L/M/N/O sichtbar, in P nicht mehr in der latenten Paarliste:
      `dio_0zkk|dio_12x0`.
      In O entstanden und in P gehalten:
      `dio_0dki|dio_0eeh`.
      In P neu entstanden:
      `dio_0j34|dio_0xt9`.
    - Lesart:
      Die latente Nebenordnung ist keine starre Kopie.
      Sie zeigt stabile Paare, ausfallende Paare und neu entstehende Paare.
      Das ist passiv gemessene dynamische Teilordnung unter Folgeweltkontakt.
    - Grenze:
      rein passiv, kontrollierter Datensatz-Kontext, keine Runtime-Lesung,
      keine Memory-Wirkung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.

214. Passive Latent Trace Persistence Lupe gebaut:
    - Datei:
      `DIO_MINI/report_passive_latent_trace_persistence_lupe.py`.
    - Report:
      `debug/dio_mini_passive_latent_trace_persistence_lupe_LMN_dio_0325_20260607_v1`.
    - Zweck:
      Pruefung, ob `dio_0325` nach der Entkopplung aus M/N auslaeuft,
      latent sichtbar bleibt oder wieder an die reduzierte Paarform
      `dio_10qz -- dio_114i` ankoppelt.
    - Ergebnis:
      `visible_count=3/3`,
      `coupled_stage_count=0`,
      `latent_visible_count=3`,
      `manifesting_count=0`,
      `summary_state=persistent_latent_trace`.
    - Timeline:
      L, M und N zeigen jeweils
      `trace_state=island_visible_uncoupled_trace`.
      Die Spur liegt weiter in einer Insel, koppelt aber nicht an
      `dio_10qz` oder `dio_114i`.
    - Lesart:
      `dio_0325` ist keine aktuell manifestierende Erweiterung.
      Es ist eine persistente latente Spur: vorhanden, relativ stabil,
      aber nicht in der beobachteten Zielkopplung getragen.
    - Grenze:
      rein passiv, kontrollierter Datensatz-Kontext, keine Runtime-Lesung,
      keine Memory-Wirkung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.

215. Passive Folgewelt O als Rekopplungsprobe fuer `dio_0325` gebaut:
    - Datei:
      `DIO_MINI/create_controlled_variant_o.py`.
    - Erzeugte Daten:
      `kontrolliert_sensor_relation_probe20..26_*_6episoden_varianteO_folgekontakt6_5m_SOLUSDT.csv`.
    - Pipeline:
      Variante `O`, Tag `folgekontakt6`, Vergleich gegen `N_FOLGEKONTAKT5`.
    - Matrixvergleich N -> O:
      `node_reproduction_rate=0.940789`,
      `edge_reproduction_rate=0.75`,
      `shared_node_count=286`,
      `shared_edge_count=9`.
    - Latent-Trace-Persistence L/M/N/O:
      `dio_0325` bleibt `visible_count=4/4`,
      `coupled_stage_count=0`,
      `latent_visible_count=4`,
      `manifesting_count=0`,
      `summary_state=persistent_latent_trace`.
    - Zero-Extension O:
      `dio_0325` ist `visible_but_uncoupled_extension`,
      `attached_base_members=-`,
      `extension_degree=0`.
      `dio_1ytc` ist in O `extension_not_visible`.
    - Lesart:
      O erzeugt keine Rekopplung von `dio_0325`.
      Die Spur bleibt stabil latent: sichtbar und insel-sichtbar,
      aber nicht an die reduzierte Paarform `dio_10qz -- dio_114i`
      gekoppelt.
    - Korrektur:
      `DIO_MINI/report_passive_zero_extension_lupe.py` wurde geschaerft:
      nicht sichtbare Extensions werden jetzt als `extension_not_visible`
      gelesen und nicht mehr sprachlich als sichtbare Spur formuliert.
    - Grenze:
      rein passiv, kontrollierter Datensatz-Kontext, keine Runtime-Lesung,
      keine Memory-Wirkung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.

216. Passive Inner Spacetime Lupe gebaut:
    - Datei:
      `DIO_MINI/report_passive_inner_spacetime_lupe.py`.
    - Report:
      `debug/dio_mini_passive_inner_spacetime_lupe_LMNO_core_20260607_v1`.
    - Zweck:
      Familien ueber L/M/N/O nicht nur als sichtbar/unsichtbar,
      sondern als innere Raumzeit-Spuren lesen:
      Lage/Kopplung/Inselkontakt als Raum,
      Sichtbarkeit/Drift/Wiederkehr als Zeit.
    - Ergebnis:
      `dio_10qz`:
      `spacetime_stable_coupled_core`,
      sichtbar `4/4`,
      gekoppelt `4/4`,
      avg drift `0.001130073`.
    - Ergebnis:
      `dio_114i`:
      `spacetime_stable_coupled_core`,
      sichtbar `4/4`,
      gekoppelt `4/4`,
      avg drift `0.001715314`.
    - Ergebnis:
      `dio_0325`:
      `spacetime_latent_persistent_trace`,
      sichtbar `4/4`,
      gekoppelt `0/4`,
      avg drift `0.001637146`.
    - Ergebnis:
      `dio_1ytc`:
      `spacetime_open_trace`,
      sichtbar `1/4`,
      gekoppelt `1/4`.
    - Lesart:
      Erste saubere Trennung zwischen stabilem inneren Kern,
      persistentem latenten Nachhall und offener/verblassender Spur.
      Das stuetzt den Begriff der inneren Raumzeit als Diagnosebegriff.
    - Grenze:
      rein passiv, kontrollierter Datensatz-Kontext, keine Runtime-Lesung,
      keine Memory-Wirkung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.

217. Passive Inner Spacetime Auto-Scan gebaut:
    - Datei:
      `DIO_MINI/report_passive_inner_spacetime_lupe.py`.
    - Aenderung:
      `--family` ist optional.
      Ohne manuelle Familienliste scannt die Lupe alle Familien aus den
      angegebenen Meaning-Spaces.
    - Report:
      `debug/dio_mini_passive_inner_spacetime_lupe_LMNO_auto_20260607_v1`.
    - Neue Ausgabe:
      `passive_inner_spacetime_distribution.csv`.
    - Verteilung:
      `spacetime_latent_persistent_trace=240`,
      `spacetime_fading_trace=123`,
      `spacetime_stable_coupled_core=2`,
      `spacetime_open_trace=1`.
    - Stabiler Kern:
      `dio_10qz`,
      `dio_114i`.
    - Ruhige latente Kandidaten:
      `dio_1si6`,
      `dio_1n79`,
      `dio_0u61`,
      `dio_11jn`,
      `dio_0hl8`,
      `dio_17p4`,
      `dio_0lu5`,
      `dio_1xbs`,
      `dio_14ai`,
      `dio_1k9e`.
    - Offene Spur:
      `dio_1ytc`.
    - Lesart:
      Mini-DIO bildet in L/M/N/O eine geschichtete innere Raumzeit:
      kleiner stabiler Kern,
      viele kern-entkoppelte Nachhallspuren,
      viele auslaufende Spuren,
      eine offene Restspur.
    - Grenze:
      `latent` bedeutet hier relativ zur beobachteten Kernkopplung
      `dio_10qz -- dio_114i`.
      Es ist kein endgueltiges Bedeutungsurteil.
      Rein passiv, keine Runtime-Lesung, keine Memory-Wirkung, keine Handlung,
      kein Gate, kein Entry-Signal, kein Richtungssignal.

218. Passive Latent Island Lupe gebaut:
    - Datei:
      `DIO_MINI/report_passive_latent_island_lupe.py`.
    - Report:
      `debug/dio_mini_passive_latent_island_lupe_LMNO_auto_20260607_v1`.
    - Zweck:
      Pruefung, ob die 240 kern-entkoppelten latenten Raumzeit-Spuren
      nur isolierte Reste sind oder untereinander eigene Teilmuster bilden.
    - Ergebnis:
      `candidate_count=240`,
      `total_latent_edge_count=13`,
      `total_nontrivial_component_count=13`,
      `max_largest_component_size=2`.
    - Stufen:
      L, M und N haben jeweils `latent_edge_count=3`,
      `connected_latent_family_count=6`,
      `isolated_latent_family_count=234`.
      O hat `latent_edge_count=4`,
      `connected_latent_family_count=8`,
      `isolated_latent_family_count=232`.
    - Stabile Zweierinseln:
      `dio_07kj|dio_09u3`,
      `dio_0r8l|dio_10xx`,
      `dio_0zkk|dio_12x0`.
    - Neue Zweierinsel in O:
      `dio_0dki|dio_0eeh`.
    - Lesart:
      Die latenten Spuren bilden nicht nur isolierten Nachhall.
      Ein kleiner Teil bildet eigene Nebenmuster ausserhalb der Kernkopplung.
      Die Struktur ist aber noch klein: groesste Komponente `2`.
    - Grenze:
      rein passiv, kontrollierter Datensatz-Kontext, keine Runtime-Lesung,
      keine Memory-Wirkung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.
208. Passive Zero Topology Lupe gebaut:
    - Datei:
      `DIO_MINI/report_passive_zero_topology_lupe.py`.
    - Zweck:
      Pruefung, ob Mini-DIO in kontrollierten Datensaetzen offene
      Zentrum-Peripherie-Strukturen bildet.
    - Forschungsanker:
      `12` Einheiten, `4` Gruppen, `0` als Dreiecks-/Zentrumsform,
      offene Kopplung statt Vollvernetzung.
    - Wichtig:
      Das ist keine Aussage ueber Leonardo und kein Langlauf-Beweis.
      Es ist eine vom Nutzer erkannte MCM-Formidee, die technisch als
      pruefbare Topologie-Diagnose genutzt wird.
    - Reports:
      `debug/dio_mini_passive_zero_topology_lupe_I_weltkontakt_20260607_v1`,
      `debug/dio_mini_passive_zero_topology_lupe_J_folgekontakt_20260607_v1`,
      `debug/dio_mini_passive_zero_topology_lupe_K_folgekontakt2_20260607_v1`.
    - Ergebnis I:
      `zero_topology_candidate_count=3`.
      Die Insel `dio_10qz|dio_114i|dio_1ytc` ist
      `open_zero_form_bridge_center` mit Zentrum `dio_10qz`.
    - Ergebnis J:
      `zero_topology_candidate_count=1`.
      Die Insel `dio_10qz|dio_114i|dio_1ytc` bleibt
      `open_zero_form_bridge_center` mit Zentrum `dio_10qz`.
    - Ergebnis K:
      `zero_topology_candidate_count=0`.
      Die betroffene Insel erweitert sich zu
      `dio_0325|dio_10qz|dio_114i|dio_1ytc`.
      Der Zustand wird `multi_center_open_field`, weil `dio_10qz`
      und `dio_1ytc` beide zentrumsnah werden.
    - Lesart:
      I/J zeigen offene 0-Form-Kandidatur.
      K zeigt keine starre Wiederholung, sondern Erweiterung mit
      mehrdeutigerem Zentrum.
    - Grenze:
      rein passiv, nur kontrollierte Datensaetze, kein Langlauf-Beweis,
      keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.
210. Passive Zero Center Shift Lupe gebaut:
    - Datei:
      `DIO_MINI/report_passive_zero_center_shift_lupe.py`.
    - Report:
      `debug/dio_mini_passive_zero_center_shift_lupe_IJK_20260607_v1`.
    - Zweck:
      Rollenverlauf der Familien `dio_10qz`, `dio_114i`,
      `dio_1ytc`, `dio_0325` ueber `I -> J -> K`.
    - Ergebnis:
      `dio_10qz` bleibt `center_candidate` mit degree `2`.
      `dio_114i` bleibt `center_near_partner` mit degree `1`.
      `dio_1ytc` verschiebt sich von `center_near_partner`
      zu `center_candidate`, degree `1 -> 2`.
      `dio_0325` verschiebt sich von `single_trace`
      zu `center_near_partner`, degree `0 -> 1`.
    - Lesart:
      Die K-Erweiterung beginnt an der Randseite `dio_1ytc`.
      Dadurch wird `dio_1ytc` zweiter zentrumsnaher Pol neben
      `dio_10qz`.
      Das ist eine passive Zentrumsspannungsverschiebung im
      kontrollierten Datensatz.
    - Grenze:
      rein passiv, nur kontrollierte Datensaetze, kein Langlauf-Beweis,
      keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.
211. Passive Folgewelt L und Mehrzentrum-Stabilisierung geprueft:
    - Datei:
      `DIO_MINI/create_controlled_variant_l.py`.
    - Zweck:
      Weitere kontrollierte Folgewelt nach K, um zu pruefen, ob die
      erweiterte Viererinsel kollabiert, driftet oder als offene
      Mehrzentrum-Struktur getragen bleibt.
    - Erzeugte Daten:
      `kontrolliert_sensor_relation_probe20..26_*_6episoden_varianteL_folgekontakt3_5m_SOLUSDT.csv`.
    - Pipeline:
      Variante `L`, Tag `folgekontakt3`, Vergleich gegen `K_FOLGEKONTAKT2`.
    - Globaler Vergleich K -> L:
      `node_reproduction_rate=0.904918`,
      `edge_reproduction_rate=0.5`,
      `shared_node_count=276`,
      `shared_edge_count=6`.
    - Zero-Topology-Befund L:
      `zero_topology_candidate_count=0`,
      betroffene Insel
      `dio_0325|dio_10qz|dio_114i|dio_1ytc`,
      `center_candidates=dio_10qz|dio_1ytc`,
      `topology_state=multi_center_open_field`.
    - Extension-Befund L:
      `dio_0325` bleibt ueber `dio_1ytc` an die Insel gekoppelt.
      Da `dio_1ytc` in L selbst Zentrumskandidat bleibt, wird
      `dio_0325` als `center_attached_extension` gelesen.
    - Center-Shift-Befund I -> J -> K -> L:
      `dio_10qz` bleibt `center_candidate`.
      `dio_114i` bleibt `center_near_partner`.
      `dio_1ytc` bleibt zweiter `center_candidate`.
      `dio_0325` bleibt `center_near_partner`.
    - Lesart:
      Die K-Erweiterung war kein einmaliges Aufleuchten.
      In L bleibt die Viererinsel als offene Mehrzentrum-Struktur sichtbar.
      Das ist keine geschlossene Clique und keine starre Kopie, sondern
      stabile Rollennaehe unter weiterer Folgewelt.
    - Vierer-Zerlegung L:
      Report
      `debug/dio_mini_passive_emergent_triad_lupe_L_dio_0325_dio_10qz_dio_114i_dio_1ytc_20260607_v1`.
      Sichtbare Kanten:
      `dio_0325<->dio_1ytc`,
      `dio_10qz<->dio_114i`,
      `dio_10qz<->dio_1ytc`.
      Fehlende Kanten:
      `dio_0325<->dio_10qz`,
      `dio_0325<->dio_114i`,
      `dio_114i<->dio_1ytc`.
      Befund:
      `visible_edge_count=3/6`,
      `semantic_density=0.759971`,
      `variant_attraction=0.839968`,
      `island_growth=0.999990`,
      `island_fragmentation=0.000081`,
      `semantic_vorticity=0.672804`.
    - MCM-Lesart:
      Die L-Struktur ist eine brueckenartige Bedeutungsform:
      `dio_114i -- dio_10qz -- dio_1ytc -- dio_0325`.
      Ordnung entsteht hier nicht durch Vollvernetzung, sondern durch
      offene, getragene Nachbarschaft.
    - Grenze:
      rein passiv, nur kontrollierte Datensaetze, kein Langlauf-Beweis,
      keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.
212. Passive Folgewelt M als Trennungs-/Reorganisationsprobe gebaut:
    - Datei:
      `DIO_MINI/create_controlled_variant_m.py`.
    - Zweck:
      Weitere kontrollierte Folgewelt nach L, um zu pruefen, ob die
      offene Viererbruecke stabil bleibt, kippt oder sich in Teilspuren
      trennt.
    - Erzeugte Daten:
      `kontrolliert_sensor_relation_probe20..26_*_6episoden_varianteM_folgekontakt4_5m_SOLUSDT.csv`.
    - Pipeline:
      Variante `M`, Tag `folgekontakt4`, Vergleich gegen
      `L_FOLGEKONTAKT3`.
    - Globaler Vergleich L -> M:
      `node_reproduction_rate=0.890728`,
      `edge_reproduction_rate=0.333333`,
      `shared_node_count=269`,
      `shared_edge_count=4`,
      `island_count_reference=290`,
      `island_count_candidate=294`.
    - Zielstruktur-Befund:
      Angefragt wurde
      `dio_0325|dio_10qz|dio_114i|dio_1ytc`.
      Sichtbar in der Zielstruktur sind
      `dio_0325|dio_10qz|dio_114i`.
      `dio_1ytc` ist dort nicht mehr sichtbar.
      Sichtbare Kante:
      `dio_10qz<->dio_114i`.
      Nicht sichtbar:
      `dio_0325<->dio_10qz`,
      `dio_0325<->dio_114i`,
      `dio_0325<->dio_1ytc`,
      `dio_10qz<->dio_1ytc`,
      `dio_114i<->dio_1ytc`.
    - Extension-Befund:
      `dio_0325` bleibt sichtbar, aber ohne Kante zur Basisinsel.
      `extension_state=visible_but_uncoupled_extension`.
    - Center-Shift-Befund:
      `dio_10qz` bleibt sichtbar, verliert aber Kopplungsgrad.
      `dio_114i` wird in M Zentrumskandidat der reduzierten Paarform.
      `dio_1ytc` verliert sichtbare Tragung in der Zielstruktur.
      `dio_0325` bleibt als entkoppelte Spur sichtbar.
    - Wichtige Abgrenzung:
      M enthaelt zwar wieder eine `open_zero_form_bridge_center`,
      diese gehoert aber nicht zur alten Zielinsel.
      Die alte Zielinsel wird nicht als Viererform weitergetragen.
    - MCM-Lesart:
      L zeigt eine getragene offene Mehrzentrum-Bruecke.
      M zeigt die Grenze dieser Tragung:
      Ein Teil bleibt als Paarform,
      ein Teil bleibt als entkoppelte Spur,
      ein Teil verschwindet aus der Zielstruktur.
      Das ist ein Hinweis auf situationsbedingte Emergenz und
      Reorganisation, nicht auf starre Kopie.
    - Bridge-Separation-Lupe:
      Datei:
      `DIO_MINI/report_passive_bridge_separation_lupe.py`.
      Report:
      `debug/dio_mini_passive_bridge_separation_lupe_L_to_M_target_20260607_v1`.
      Ergebnis:
      `family_carried=1`,
      `family_not_carried=1`,
      `family_visible_but_decoupled=2`,
      `edge_carried=1`,
      `edge_lost=2`,
      `edge_absent=3`.
      Getragen bleibt:
      `dio_10qz<->dio_114i`.
      Verloren gehen:
      `dio_0325<->dio_1ytc`,
      `dio_10qz<->dio_1ytc`.
      Lesart:
      Der Bruch liegt nicht primaer in einem grossen Einzelwertbruch,
      sondern in der relationalen Kopplung. Eine Familie kann sichtbar
      bleiben und trotzdem nicht mehr in der Zielinsel gekoppelt sein.
    - Grenze:
      rein passiv, nur kontrollierte Datensaetze, kein Langlauf-Beweis,
      keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.
213. Passive Folgewelt N als Rueckkopplungsprobe fuer `dio_0325` gebaut:
    - Datei:
      `DIO_MINI/create_controlled_variant_n.py`.
    - Zweck:
      Nach M gezielt pruefen, ob die entkoppelte Spur `dio_0325`
      isoliert bleibt, an `dio_114i` ankoppelt oder zurueck zu
      `dio_1ytc` findet.
    - Erzeugte Daten:
      `kontrolliert_sensor_relation_probe20..26_*_6episoden_varianteN_folgekontakt5_5m_SOLUSDT.csv`.
    - Pipeline:
      Variante `N`, Tag `folgekontakt5`, Vergleich gegen
      `M_FOLGEKONTAKT4`.
    - Globaler Vergleich M -> N:
      `node_reproduction_rate=0.921569`,
      `edge_reproduction_rate=0.666667`,
      `shared_node_count=282`,
      `shared_edge_count=8`,
      `island_count_reference=294`,
      `island_count_candidate=292`.
    - Bridge-Separation-Befund:
      `family_carried=3`,
      `family_absent=1`,
      `edge_carried=1`,
      `edge_absent=5`.
    - Zielstruktur-Befund:
      Sichtbar:
      `dio_0325`,
      `dio_10qz`,
      `dio_114i`.
      Nicht sichtbar:
      `dio_1ytc`.
      Getragen bleibt:
      `dio_10qz<->dio_114i`.
      `dio_0325` koppelt nicht an
      `dio_10qz`,
      `dio_114i`
      oder `dio_1ytc`.
    - Extension-Befund:
      `dio_0325` bleibt
      `visible_but_uncoupled_extension`.
    - Center-Shift-Befund:
      `dio_10qz` bleibt Zentrumskandidat mit reduziertem Kopplungsgrad.
      `dio_114i` ist Zentrumskandidat der reduzierten Paarform.
      `dio_1ytc` bleibt ohne Tragung.
      `dio_0325` bleibt Einzelspur ohne Kante.
    - Lesart:
      N stabilisiert nicht die alte Viererbruecke.
      N stabilisiert die reduzierte Paarform
      `dio_10qz<->dio_114i`.
      `dio_0325` bleibt als Spur sichtbar, aber ohne relationale
      Tragung. Das ist keine erneute Manifestation, sondern eine
      entkoppelte Spurform.
    - Grenze:
      rein passiv, nur kontrollierte Datensaetze, kein Langlauf-Beweis,
      keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.
209. Passive Zero Extension Lupe gebaut:
    - Datei:
      `DIO_MINI/report_passive_zero_extension_lupe.py`.
    - Report:
      `debug/dio_mini_passive_zero_extension_lupe_K_dio_0325_20260607_v1`.
    - Zweck:
      Isoliert `dio_0325` als neue Spur in der erweiterten K-Insel und
      prueft, ob die Spur an das alte Zentrum oder an eine Randseite
      koppelt.
    - Basis:
      `dio_10qz|dio_114i|dio_1ytc`.
    - Altes Zentrum:
      `dio_10qz`.
    - Erweiterung:
      `dio_0325`.
    - Befund:
      `dio_0325 <-> dio_1ytc` ist sichtbar.
      `dio_0325 <-> dio_10qz` ist nicht sichtbar.
      `dio_0325 <-> dio_114i` ist nicht sichtbar.
      `extension_state=periphery_extension_shifts_center_tension`.
    - Lesart:
      `dio_0325` erweitert nicht direkt das alte Zentrum.
      Die Spur koppelt an die Randseite `dio_1ytc` und macht diese
      zentrumsnaeher. Dadurch wird aus der offenen 0-Form in K ein
      Multi-Center-Feld.
    - Grenze:
      rein passiv, nur kontrollierte Datensaetze, kein Langlauf-Beweis,
      keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry-Signal,
      kein Richtungssignal.
207. Passive Folgewelt K nach Triaden-Zerlegung gebaut:
    - Datei:
      `DIO_MINI/create_controlled_variant_k.py`.
    - Zweck:
      Nach dem Auseinandernehmen der Triade wird ein weiterer
      deterministischer Weltkontakt erzeugt, ohne Mini-DIO-Logik,
      Speicherlesen, Gates, Entry oder Richtung zu veraendern.
    - Erzeugte Daten:
      `kontrolliert_sensor_relation_probe20..26_*_6episoden_varianteK_folgekontakt2_5m_SOLUSDT.csv`.
    - Pipeline:
      Variante `K`, Tag `folgekontakt2`, Vergleich gegen `J_FOLGEKONTAKT`.
    - Globaler Vergleich J -> K:
      `node_reproduction_rate=0.868687`,
      `edge_reproduction_rate=0.333333`,
      `shared_node_count=258`,
      `shared_edge_count=4`.
      Viele Knoten bleiben erhalten, aber Kanten organisieren sich
      deutlich staerker um.
    - Triaden-Befund:
      `I_WELTKONTAKT` und `J_FOLGEKONTAKT`:
      exakte offene Triade
      `dio_10qz|dio_114i|dio_1ytc`,
      `visible_edge_count=2/3`,
      `dio_10qz=bridge_core`.
      `K_FOLGEKONTAKT2`:
      alte Triade bleibt sichtbar,
      aber als Teil der erweiterten Viererinsel
      `dio_0325|dio_10qz|dio_114i|dio_1ytc`.
    - Lesart:
      `dio_114i` bleibt getragen, aber nicht als geschlossenes Dreieck.
      Die Kopplung laeuft weiter ueber `dio_10qz`.
      In `K` entsteht zusaetzlich eine Erweiterung ueber `dio_0325`.
      Das spricht fuer Insel-Expansion unter Folgeweltkontakt, nicht fuer
      starres Kopieren.
    - Grenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate,
      kein Entry-Signal, kein Richtungssignal.
206. Passive Emergent Triad Lupe gebaut:
    - Datei:
      `DIO_MINI/report_passive_emergent_triad_lupe.py`.
    - Reports:
      `debug/dio_mini_passive_emergent_triad_lupe_I_dio_10qz_dio_114i_dio_1ytc_20260607_v1`,
      `debug/dio_mini_passive_emergent_triad_lupe_J_dio_10qz_dio_114i_dio_1ytc_20260607_v1`.
    - Zweck:
      Die Insel `dio_10qz|dio_114i|dio_1ytc` wird vor weiterer
      Folgewelt nicht nur als Partnerliste gelesen, sondern in direkte
      Kanten und Knotenrollen zerlegt.
    - Ergebnis I:
      `visible_edge_count=2/3`,
      `triad_reading=bridge_held_open_triad`,
      `dio_10qz=bridge_core`,
      `dio_114i=close_partner`,
      `dio_1ytc=close_partner`,
      fehlende direkte Kante `dio_114i <-> dio_1ytc`.
    - Ergebnis J:
      `visible_edge_count=2/3`,
      `triad_reading=bridge_held_open_triad`,
      `dio_10qz=bridge_core`,
      `dio_114i=close_partner`,
      `dio_1ytc=close_partner`,
      fehlende direkte Kante `dio_114i <-> dio_1ytc`.
    - Lesart:
      Die Insel bleibt stabil, aber als offene, brueckengehaltene
      Triade. `dio_10qz` traegt die Kopplung. `dio_114i` bleibt
      Manifestationskandidat, aber nicht als geschlossenes Dreieck,
      sondern ueber einen Brueckenkern.
    - Grenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate,
      kein Entry-Signal, kein Richtungssignal.
200. Passive Emergent Candidate Lupe gebaut:
    - Datei:
      `DIO_MINI/report_passive_emergent_candidate_lupe.py`.
    - Report:
      `debug/dio_mini_passive_emergent_candidate_lupe_G_REPRO_H_REPRO_I_WELTKONTAKT_20260607_v1`.
    - Kandidaten:
      `dio_005q`,
      `dio_1wx6`,
      `dio_114i`,
      `dio_0scd`.
    - Ergebnis:
      `dio_005q` zeigt isolierte Variation, staerker aus Sehen/Hoeren.
      `dio_1wx6` zeigt starke isolierte Variation aus Feld und Sensorik.
      `dio_114i` koppelt spaeter mit `dio_10qz` und `dio_1ytc`.
      `dio_0scd` koppelt spaeter mit `dio_0axn` und `dio_122f`.
    - Lesart:
      Eigentliche Emergenz erscheint derzeit als isolierte Variation oder
      als spaetere Reorganisation durch Kopplung.
    - Grenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate,
      kein Entry-Signal, kein Richtungssignal.
201. Passive Emergent Lifecycle gebaut:
    - Datei:
      `DIO_MINI/report_passive_emergent_lifecycle.py`.
    - Report:
      `debug/dio_mini_passive_emergent_lifecycle_G_REPRO_H_REPRO_I_WELTKONTAKT_20260607_v1`.
    - Zweck:
      Trennung zwischen realitaetsbezogener Ordnung und eigentlicher
      emergenter Bewegung.
    - Ergebnis:
      `sporadic_popup=297`,
      `reality_bound_manifestation_candidate=118`,
      `reality_order_trace=66`,
      `recurring_soft_order_trace=72`,
      `isolated_emergent_variation_candidate=4`,
      `isolated_emergent_variation_trace=3`,
      `emergent_split_drift_trace=4`,
      `emergent_reorganization_trace=2`.
    - Wichtige Korrektur:
      `dio_11vr` ist eher realitaetsgebundene Ordnung als eigentliche
      Emergenz.
      Eigentliche Emergenz liegt staerker bei Variation, Drift, Kopplung,
      Teilung und Reorganisation.
    - Auffaellige Kandidaten:
      `dio_005q`,
      `dio_1wx6`,
      `dio_0lrt`,
      `dio_1xka`,
      `dio_114i`,
      `dio_0scd`.
    - Grenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate,
      kein Entry-Signal, kein Richtungssignal.
202. Carry Separator an Repro-Pipeline angeschlossen:
    - Datei:
      `DIO_MINI/run_passive_inner_universe_repro_pipeline.py`.
    - Neue Schalter:
      `--build-carry-separator`,
      `--carry-separator-reference`.
    - Verhalten:
      Der Separator wird nur nach einem vorhandenen Follow-Up-Result
      aufgerufen.
    - PrÃ¼fung:
      Import erfolgreich.
      Dry-Run zeigt den erwarteten Aufruf von
      `DIO_MINI.report_passive_carry_separator`.
    - Grenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate,
      kein Entry-Signal, kein Richtungssignal.
203. Passive Emergent Partner Lupe gebaut:
    - Datei:
      `DIO_MINI/report_passive_emergent_partner_lupe.py`.
    - Report:
      `debug/dio_mini_passive_emergent_partner_lupe_H_REPRO_I_WELTKONTAKT_20260607_v1`.
    - Kandidaten:
      `dio_114i`,
      `dio_0scd`.
    - Ergebnis:
      `dio_114i` war in `H_REPRO` sichtbar, aber isoliert.
      In `I_WELTKONTAKT` koppelt die Spur mit `dio_10qz`
      und `dio_1ytc`.
      `dio_0scd` war in `H_REPRO` sichtbar, aber isoliert.
      In `I_WELTKONTAKT` koppelt die Spur mit `dio_0axn`
      und `dio_122f`.
    - Messung:
      `dio_114i`: avg whole distance `0.008542394`,
      avg sensory distance `0.014158917`,
      avg MCM distance `0.010337658`.
      `dio_0scd`: avg whole distance `0.013329276`,
      avg sensory distance `0.024295865`,
      avg MCM distance `0.012350938`.
    - Lesart:
      Das ist passive Reorganisation:
      eine vorhandene innere Spur bleibt erkennbar,
      findet unter neuem Weltkontakt eine eng verwandte Nachbarschaft,
      und bildet daraus eine neue semantische Inselstruktur.
    - Grenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate,
      kein Entry-Signal, kein Richtungssignal.
204. Passive Emergent Island Growth Lupe gebaut:
    - Datei:
      `DIO_MINI/report_passive_emergent_island_growth_lupe.py`.
    - Report:
      `debug/dio_mini_passive_emergent_island_growth_lupe_H_REPRO_I_WELTKONTAKT_20260607_v1`.
    - Zweck:
      Pruefung, ob emergente Spuren nur isoliert aufploppen oder unter
      neuem Weltkontakt zu Bedeutungsinseln verdichten.
    - Ergebnis:
      `dio_114i`:
      `visible_isolated -> coupled_density_center`,
      Partner `dio_10qz|dio_1ytc`,
      semantic_density `0.080000 -> 0.793305`,
      island_growth `0.306667 -> 0.999985`,
      fragmentation `1.000000 -> 0.000053`.
      `dio_0scd`:
      `visible_isolated -> coupled_density_center`,
      Partner `dio_0axn|dio_122f`,
      semantic_density `0.080000 -> 0.793304`,
      island_growth `0.306667 -> 0.999984`,
      fragmentation `1.000000 -> 0.000054`.
    - Lesart:
      Das ist die Entwicklungsfigur:
      isolierter Keim -> Weltkontakt -> Partnerbildung -> Dichtezentrum.
      Es bleibt passiv und ist noch keine Handlung.
    - Grenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate,
      kein Entry-Signal, kein Richtungssignal.
205. Passive Folgewelt J und Manifestations-Test gebaut:
    - Datei:
      `DIO_MINI/create_controlled_variant_j.py`.
    - Zweck:
      Zweiter deterministischer Weltkontakt nach Variante I.
      Damit wird geprueft, ob Dichtezentren stabil bleiben,
      kippen oder verschwinden.
    - Erzeugte Daten:
      `kontrolliert_sensor_relation_probe20..26_*_6episoden_varianteJ_folgekontakt_5m_SOLUSDT.csv`.
    - Pipeline:
      Variante `J`, Tag `folgekontakt`, Vergleich gegen `I_WELTKONTAKT`.
    - Matrix-Befund:
      `node_reproduction_rate=0.761290`,
      `edge_reproduction_rate=0.416667`.
      Viele Knoten bleiben sichtbar, aber weniger Kanten bleiben gleich.
      Das spricht fuer Reorganisation statt starrer Kopie.
    - Kandidaten-Befund:
      `dio_114i` bleibt von I nach J als `coupled_density_center`
      mit Partnern `dio_10qz|dio_1ytc` erhalten.
      `dio_0scd` war in I ein `coupled_density_center`,
      ist in J aber `not_visible`.
    - Korrektur:
      `DIO_MINI/report_passive_emergent_island_growth_lupe.py`
      wurde korrigiert, damit ein verlorenes Dichtezentrum nicht mehr
      faelschlich als stabile Stufe gelesen wird.
    - Lesart:
      `dio_114i` ist aktuell ein stabiler Manifestationskandidat.
      `dio_0scd` ist eine situationsgebundene Dichteinsel,
      die im Folgekontakt nicht mehr getragen wurde.
    - Grenze:
      rein passiv, keine Runtime-Lesung, keine Handlung, kein Gate,
      kein Entry-Signal, kein Richtungssignal.
