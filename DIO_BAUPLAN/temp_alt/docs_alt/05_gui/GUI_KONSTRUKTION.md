# GUI_KONSTRUKTION

Status:
- Konzeptdatei fÃ¼r eine spÃ¤tere Web-Oberflaeche
- keine aktuelle PrioritÃ¤t vor Brain-/MCM-Mechanik
- kein Ersatz für den aktiven Bauplan unter `DIO_2/konstruktion/`

Regelwerk:
- `docs/00_regeln/MD_ANWEISUNG.md`
- keine harte Trading-Logik aus der GUI ableiten
- GUI ist Beobachtung, nicht Steuerungszwang

---

# 1. Grundidee

DIO soll nicht als klassische Trading-GUI dargestellt werden.

Die Oberflaeche soll ein Beobachtungsraum sein:
- Ã¤uÃŸere Wahrnehmung
- innere Feldwahrnehmung
- neuronale AktivitÃ¤t
- neurochemische Last und Unterstuetzung
- Handlungstendenz
- Reife / Observe / Act-Watch / Act

Ziel:
Der Mensch soll nicht mit Variablen Ã¼berladen werden, sondern sehen kÃ¶nnen,
wie DIO seine Welt gerade organisiert.

---

# 2. Bevorzugte Form

Bevorzugt:
**lokale Web-Oberflaeche**

Gruende:
- gut fÃ¼r Backtest-Replay
- gut fÃ¼r spÃ¤teren Live-Monitor
- Canvas/WebGL fÃ¼r Feldvisualisierung mÃ¶glich
- mehrere Fenster/Panels flexibel anordenbar
- spÃ¤ter leicht mit WebSocket oder Debug-Dateien verbindbar

MÃ¶gliche technische Richtung:
- Backend liest Runtime-/Debug-Zustand
- Frontend rendert Panels
- Backtest zuerst aus Debug-Dateien
- Live spÃ¤ter Ã¼ber laufenden State/Stream

---

# 3. Hauptfenster

## AuÃŸenwahrnehmungsfenster

Funktion:
Darstellung dessen, was DIO von der Markt-AuÃŸenwelt sieht.

Nicht als menschliches Chartmuster:
- kein starres Patternlabel
- keine harte Bull/Bear-Schublade
- keine mechanische "das ist X"-Anzeige

Sichtbar machen:
- Marktform
- visuelle Klarheit
- ObjektstabilitÃ¤t
- visuelle Blindheit
- Formdruck
- Resonanz / Fragilitaet
- eventuell DIO-interne Formzeichen

MÃ¶gliche Darstellung:
- Chart oder vereinfachter Marktverlauf
- darÃ¼ber transparente Formzonen
- Fokusbereich / Zoomfenster
- Formzeichen nur als interne IDs oder abstrakte Symbole

## MCM-Feldfenster

Funktion:
Darstellung des inneren Wahrnehmungsfeldes.

Sichtbar machen:
- `MCMNeuron`
- lokale AktivitÃ¤t
- AktivitÃ¤tsinseln
- Feldspannung
- Feldklarheit
- Fragmentierung
- Kopplung / Verknuepfungen
- Informationsbewegung
- Kontextreaktivierung

MÃ¶gliche Darstellung:
- Punkte/Neuronen als Feldkarte
- Linien fÃ¼r Kopplung und Informationsfluss
- Pulsieren fÃ¼r Aktivierung
- Drift/Bewegung als Nachhall
- AktivitÃ¤tsinseln als Areale

Wichtig:
Mehr AktivitÃ¤t bedeutet nicht automatisch bessere Entscheidung.
Die GUI muss sichtbar machen, ob AktivitÃ¤t Ordnung oder Last erzeugt.

## Neurochemisches Feldfenster

Funktion:
Darstellung der neurologisch lesbaren Innenlage.

Die neurochemische Wirkung kann als Farbfeld Ã¼ber dem MCM-Feld liegen.
Dabei muss nicht angenommen werden, dass "eine Chemie" direkt Ã¼ber dem Feld
liegt. Es kann auch sein, dass bestimmte Feldareale eine bestimmte
neurochemische Faerbung tragen.

MÃ¶gliche Farblogik:
- `cortisol_load`: Last / Stress / Ãœberforderung
- `gaba_inhibition`: Hemmung / Reifebremse
- `noradrenaline_arousal`: Wachheit / Alarm / Spannung
- `acetylcholine_focus`: Fokus / genaues Sehen
- `serotonin_stability`: StabilitÃ¤t / Geduld / TragfÃ¤higkeit
- `endorphin_relief`: Entlastung / Prozesswohlbefinden
- `dopamine_tone`: Lernwert / Erwartung / Entwicklungston
- `glutamate_activation`: neuronale Aktivierung / Feldenergie

Darstellungsprinzip:
- Farbwolken statt Zahlenwand
- dominante Toene sichtbar
- Mischung statt harte Kategorie
- Balance aus Last und Support sichtbar

## Entscheidungs-/Reifeleiste

Funktion:
Kompakte Zustandsanzeige.

Sichtbar machen:
- `observe`
- `hold`
- `replan`
- `act_watch`
- `act`
- dominanter Grund
- neurochemische Balance
- TragfÃ¤higkeit
- Handlungsspannung

Keine Ãœberladung:
Diese Leiste soll wenige klare Zustandsworte zeigen, nicht alle Variablen.

---

# 4. Zeit- und Replay-Konzept

Die GUI sollte zuerst als Backtest-Replay funktionieren.

Wichtige Modi:
- Lauf laden
- Timeline abspielen
- Schritt vor/zurÃ¼ck
- Geschwindigkeit wÃ¤hlen
- Phasenwechsel markieren
- Trade-Einstiege/Exits markieren
- Observe-/Act-Watch-Abschnitte sichtbar machen

Warum zuerst Replay:
- Debug-Daten sind stabil vorhanden
- kein Live-API-Risiko
- DIOs Wahrnehmungsentwicklung kann nachtrÃ¤glich betrachtet werden
- Regimewechsel kÃ¶nnen besser verstanden werden

Live-Modus spÃ¤ter:
- gleiche Fenster
- laufender State
- neue Kerzen / neue Wahrnehmung
- Positionen und Orders nur als Zusatz, nicht als Kern der GUI

---

# 5. Datenquellen

Geeignete Quellen:
- `mcm_field_decision_protocol.csv`
- `mcm_memory_thinking_protocol.csv`
- `mcm_visual_cortex_protocol.csv`
- `mcm_form_symbol_protocol.csv`
- `mcm_position_intervention_protocol.csv`
- `outcome_records.jsonl`
- `trade_equity.csv`
- Runtime-Snapshots spÃ¤ter live

Wichtige neue Achsen:
- `neurochemical_state_label`
- `neurochemical_dominant_tone`
- `dopamine_tone`
- `gaba_inhibition`
- `noradrenaline_arousal`
- `acetylcholine_focus`
- `serotonin_stability`
- `cortisol_load`
- `endorphin_relief`
- `glutamate_activation`
- `neurochemical_load`
- `neurochemical_support`
- `neurochemical_balance`

---

# 6. Gestaltungsregeln

Die GUI soll nicht kompliziert und Ã¼berladen sein.

Erlaubt:
- wenige starke Fenster
- Farbwolken
- neuronale AktivitÃ¤tskarte
- Timeline
- kompakte Zustandsleiste
- Detailwerte erst bei Hover/Klick
- Replay statt permanenter Zahlenflut

Nicht gewuenscht:
- reine Tabellenoberflaeche
- alle Variablen gleichzeitig zeigen
- Trading-Dashboard als Hauptform
- harte Ampellogik
- "gut/schlecht"-Labels fÃ¼r komplexe Zustandslagen

Leitfrage:
Kann ein Mensch beim Zuschauen verstehen, ob DIO sieht, fÃ¼hlt, Ã¼berlastet
ist, sich hemmt, reift oder tragfÃ¤hig handelt?

---

# 7. MÃ¶gliche erste Version

Minimal brauchbare Web-GUI:

1. Backtest-Lauf aus `debug/debug_lauf_X` laden.
2. Equity-Kurve und Trades anzeigen.
3. Timeline mit Phasen:
   `observe`, `hold`, `replan`, `act_watch`, `act`.
4. MCM-Feld als einfache Neuronenkarte darstellen.
5. Neurochemische Achsen als Farbwolke oder radialer Zustand anzeigen.
6. AuÃŸenwahrnehmung als Chart plus visuelle Klarheit/Blindheit anzeigen.
7. Klick auf Zeitpunkt zeigt kompakte Innenlage.

Erst danach:
- Live-Streaming
- WebSocket
- interaktive Feldnavigation
- mehrere ZeitauflÃ¶sungen
- Vergleich zweier LÃ¤ufe

---

# 8. Philosophische Abgrenzung

Die GUI soll DIO nicht menschlich labeln.

Sie soll nicht sagen:
"Das ist ein menschliches Muster."

Sie soll zeigen:
"So organisiert DIO gerade AuÃŸenreiz, Innenfeld, Erfahrung,
neurochemische Last und Handlungstendenz."

Damit wird die GUI ein Fenster in die MCM, nicht nur ein Trading-Frontend.
