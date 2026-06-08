# 36 DIO Mini: episodischer MCM-Kern

## Zweck

Der Mini-Kern ist ein isolierter Neustart.

Er soll pruefen, ob DIO mit einer sehr kleinen MCM-Neuronenstruktur aus
Episoden lernen kann:

```text
sehen -> hoeren -> fuehlen -> Handlung -> Konsequenz -> eigene Syntax
```

Der Kern nutzt keine Setup-Begriffe.

Verboten im Input:

```text
Pullback
Trend
Support
Resistance
Strategie
```

Erlaubt im Input:

```text
sehen
hoeren
fuehlen
```

## Sehen

Sehen beschreibt nur Formwirkung:

- `form_flow`
- `form_stability`
- `form_change`

Das sind keine Labels. Es sind Sinneswerte.

## Hoeren

Hoeren beschreibt Marktenergie:

- `energy_tone`
- `energy_shift`

Der Markt wird als energetische Veraenderung gehoert, nicht als Entry-Signal.

## Fuehlen

Fuehlen beschreibt die MCM-Lage:

- `mcm_coherence`
- `mcm_tension`
- `mcm_asymmetry`

Das MCM-Feld ist hier der innere Resonanzraum.

## Eigene Syntax

Aus Sehen, Hoeren, Fuehlen und Feldsignatur entsteht ein internes Wort:

```text
dio_...
```

Dieses Wort ist DIOs eigene Verdichtung.

Der Mensch darf es im Report auswerten, aber DIO selbst arbeitet mit dem
Symbol und seiner Konsequenzspur.

## Episodisches Lernen

Eine Episode speichert:

```text
Symbol
Sinneslage
Aktion
Konsequenz
bessere Entry-Lage im Training
```

Die bessere Entry-Lage ist nur Trainingsfeedback nach dem Ergebnis. Sie ist
kein Live-Lookahead.

## Aktueller Teststand

Kontrollierter Datensatz:

```text
data/kontrolliert_long_short_5m_SOLUSDT.csv
```

Erster Mini-Test:

- Lauf 1: 0 Trades, Beobachtung.
- Lauf 2: 6 Trades, positives Trainingsreward.
- Lauf 3: 7 Trades, positives Trainingsreward.

Befund:

```text
Das semantische Gedachtnis wirkt.
Die eigene Syntax bildet wiederkehrende Aktionsspuren.
Der Kern ist aber noch zu aktiv fuer die 2-Referenz-Struktur.
```

Naechster Schritt:

Episoden weiter verdichten:

- weniger Einzelkontakte,
- mehr Wiedererkennung,
- groessere Handlung nur bei stabiler Symbolfamilie,
- keine harten Strategie-Regeln.

## Symbolfamilien-Reife

Erweiterung:

- einzelne `dio_...` Symbole lernen weiter,
- zusaetzlich reifen `syntax_family` Gruppen,
- Handlungsnaehe entsteht staerker aus wiederkehrender Familienerfahrung.

Test nach Familienreife:

```text
Lauf 1: 0 Trades, Beobachtung
Lauf 2: 1 Trade, noch negativ
Lauf 3: 6 Trades, positives Reward
Lauf 4: 6 Trades, positives Reward
Lauf 5: 6 Trades, positives Reward
```

Befund:

```text
Familiengedaechtnis wirkt.
DIO wird nicht mehr sofort aus Einzelzeichen aktiv.
Aber fuer die kontrollierte 2-Struktur-Welt handelt er noch zu oft.
```

Naechste Korrektur:

Nicht jede tragende Symbolfamilie erzeugt eine neue Handlung. DIO braucht eine
uebergeordnete Episodenphase:

```text
Ich befinde mich noch in derselben Handlungsbewegung.
Ich muss nicht erneut handeln.
```

Damit soll aus mehreren nahen Einzelkontakten eine zusammenhaengende Episode
werden.

## Strenger 2-Episoden-Datensatz

Kontrollierter Datensatz:

```text
data/kontrolliert_2episoden_5m_SOLUSDT.csv
```

Dieser Datensatz enthaelt nur zwei klare Referenzbewegungen:

- eine Long-nahe Episode,
- eine Short-nahe Episode.

Der Datensatz enthaelt keine Setup-Labels. DIO bekommt weiterhin nur OHLCV,
Zeit und daraus abgeleitete Sinneslagen:

```text
sehen
hoeren
fuehlen
```

Test mit frischem Mini-Gedaechtnis:

```text
Lauf 1: 0 Trades, Beobachtung
Lauf 2: 0 Trades, Beobachtung
Lauf 3: 2 Trades, positives Reward
Lauf 4: 2 Trades, positives Reward
Lauf 5: 2 Trades, positives Reward
Lauf 6: 2 Trades, positives Reward
```

Lauf 6:

```text
Trades: 2
Long: 1
Short: 1
Reward: 3.0941
Symbole: 4
Top-Long-Familie: dio_0byw
Top-Short-Familien: dio_0zlr, dio_14zx
```

Befund:

```text
Der Mini-Kern zeigt erstmals eine saubere kontrollierte Reifung.
Er beobachtet zuerst, bildet eigene Syntaxfamilien und wird danach stabil
handlungsnah.
```

Wichtig:

Das ist kein Profitabilitaetsnachweis fuer den grossen DIO. Es ist ein
Konstruktionsnachweis fuer den isolierten Kern:

```text
MCM-Neuron + sehen/hoeren/fuehlen + eigene Syntax + Konsequenzgedaechtnis
kann auf einer kontrollierten Welt Lauf fuer Lauf reifen.
```

Naechster Schritt:

Die Reifung soll automatisch ausgewertet werden:

- Trades pro Lauf,
- Long/Short-Verteilung,
- Reward pro Lauf,
- Symbolfamilien,
- wann aus Beobachtung Handlung wird.

## Zweite kontrollierte Varianz-Welt

Kontrollierter Datensatz:

```text
data/kontrolliert_varianz_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Nicht die gleiche Strecke wiederholen, sondern pruefen, ob DIO bei veraenderter
Reihenfolge und veraenderter Kerzen-/Volumenform erneut reifen kann.
```

Test mit frischem Mini-Gedaechtnis:

```text
Lauf 1: 0 Trades, Beobachtung
Lauf 2: 0 Trades, Beobachtung
Lauf 3: 2 Trades, positives Reward
Lauf 4: 2 Trades, positives Reward
Lauf 5: 3 Trades, positives Reward
Lauf 6: 3 Trades, positives Reward
```

Lauf 6:

```text
Trades: 3
Long: 2
Short: 1
Reward: 3.3858
Symbole: 4
Top-Long-Familie: dio_0uct
Top-Short-Familie: dio_0n4c
```

Befund:

```text
Der Mini-Kern zeigt auch auf einer zweiten kontrollierten Welt Reifung.
Er startet beobachtend, bildet Syntaxfamilien und wird danach handlungsnah.
```

Einschraenkung:

```text
Die zweite Welt erzeugt im Long-Abschnitt zwei tragende Kontaktfenster.
Der dritte Trade ist deshalb nicht automatisch falsch, muss aber als
Episodenverdichtung beobachtet werden.
```

Diagnosewerkzeug:

```text
python -m DIO_MINI.analyze_runs --debug-root debug\dio_mini_varianz_test --output-dir debug\dio_mini_varianz_test
```

Erzeugt:

```text
debug/dio_mini_varianz_test/dio_mini_summary.csv
debug/dio_mini_varianz_test/dio_mini_summary.json
```

Naechster Schritt:

Die Mini-Welt braucht eine saubere Episodenqualitaet:

- nicht jeden nahen Kontakt einzeln ueberbewerten,
- nicht durch harte Strategie-Begriffe verdichten,
- sondern aus wiederkehrender eigener Syntax erkennen, ob es noch dieselbe
  zusammenhaengende Bewegung ist oder ein neuer Kontakt.

## Episodenqualitaet als Diagnose

Die Mini-Auswertung unterscheidet jetzt:

```text
raw_trade_pressure
phase_suppressed
compressed_contacts
executed_trades
```

Bedeutung:

```text
raw_trade_pressure: DIOs roher Handlungsdruck aus Sehen/Hoeren/Fuehlen.
phase_suppressed: Handlung wurde gehalten, weil sie noch zur gleichen Episode gehoert.
compressed_contacts: roher Druck minus ausgefuehrte Trades.
executed_trades: tatsaechlich ausgefuehrte Handlung.
```

Befund erste kontrollierte Welt:

```text
Ab Lauf 4 entsteht 3x roher Trade-Druck, aber nur 2 Trades werden ausgefuehrt.
Ein Kontakt wird als gleiche Episode gehalten.
```

Befund zweite kontrollierte Varianz-Welt:

```text
Ab Lauf 5 entsteht 3x roher Trade-Druck und 3 Trades werden ausgefuehrt.
Hier erkennt DIO die Kontakte aktuell als getrennte Episoden.
```

Das ist der naechste Pruefpunkt:

```text
Sind diese getrennten Kontakte fachlich eigene Wahrnehmungsereignisse,
oder muss DIO aehnliche Kontaktfenster staerker episodisch zusammenfassen?
```

## Weiche Episodenbindung

Die alte Mini-Bindung nutzte nur Sinnesnaehe:

```text
Wenn die neue Sinneslage nah genug ist, dann gleiche Episode.
```

Das war zu flach. Eine laufende Bewegung darf sich sensorisch veraendern und
trotzdem dieselbe Episode bleiben.

Die neue Bindung vergleicht daher zwei Druckrichtungen:

```text
episode_binding_pressure
episode_release_pressure
```

Bedeutung:

```text
episode_binding_pressure:
  Wie stark wirkt der neue Kontakt wie Nachhall derselben Bewegung?

episode_release_pressure:
  Wie stark wirkt der neue Kontakt wie ein eigenstaendiges neues Ereignis?
```

Nur wenn Freigabedruck staerker wird, entsteht ein neuer Tradekontakt.
Wenn Bindungsdruck staerker bleibt, wird der rohe Handlungsdruck als gleiche
Episode gehalten.

Wichtig:

```text
Das ist keine Strategie-Regel.
Es ist eine episodische Wahrnehmungsbindung:
Ich bin noch in derselben Bewegung und muss nicht jedes innere Signal
als neue Handlung ausfuehren.
```

Aktueller Befund nach weicher Bindung:

```text
Referenz-Welt Lauf 6:
  raw_trade_pressure: 3
  executed_trades: 2
  compressed_contacts: 1

Varianz-Welt Lauf 6:
  raw_trade_pressure: 3
  executed_trades: 2
  compressed_contacts: 1
```

Damit entsteht in beiden kontrollierten Welten:

```text
Beobachten -> Reifung -> 2 Handlungen -> 1 ueberzaehliger Kontakt wird gehalten.
```

## Dritte kontrollierte Welt mit Rauschen

Kontrollierter Datensatz:

```text
data/kontrolliert_rauschen_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Zwei Bewegungen bleiben vorhanden, aber dazwischen liegt eine rauschende
Seitwaertszone. DIO soll nicht jede kleine positive Konsequenz sofort als
voll tragende Handlung werten.
```

Korrektur:

Schwache positive Konsequenz bleibt Lernspur, aber sie erzeugt weniger direkte
Handlungsnaehe als eine klar tragende Konsequenz.

Das ist keine Sperre:

```text
Kleine positive Erfahrung wird behalten.
Sie wird nur nicht sofort gleich stark handlungsnah wie klare Erfahrung.
```

Test mit frischem Mini-Gedaechtnis:

```text
Lauf 1: 0 Trades, Beobachtung
Lauf 2: 0 Trades, Beobachtung
Lauf 3: 2 Trades, positives Reward
Lauf 4: 2 Trades, positives Reward
Lauf 5: 2 Trades, positives Reward
Lauf 6: 2 Trades, positives Reward
Lauf 7: 2 Trades, positives Reward
Lauf 8: 2 Trades, positives Reward
```

Lauf 8:

```text
raw_trade_pressure: 3
executed_trades: 2
compressed_contacts: 1
Reward: 2.0480
```

Befund:

```text
DIO kann in der Mini-Welt Rauschen beobachten, schwache Kontakte lernen und
trotzdem nur die zwei tragenden Episoden handeln.
```

Damit liegen drei kontrollierte Mini-Befunde vor:

```text
Referenz-Welt: 2 Trades stabil
Varianz-Welt: 2 Trades stabil
Rausch-Welt: 2 Trades stabil
```

## Assoziativer Transfer zwischen Welten

Erweiterung:

```text
DIO speichert nicht nur einzelne dio_... Woerter.
DIO speichert intern auch einen kompakten Sinnesvektor:

sehen + hoeren + fuehlen + MCM-Feldsignatur
```

Dieser Vektor wird nicht als menschliches Setup benutzt. Er dient nur dazu,
nahe eigene Syntaxfamilien wiederzuerkennen.

Bedeutung:

```text
Diese neue Lage ist nicht exakt gleich.
Aber sie liegt nahe an einer Familie, die schon Konsequenz getragen hat.
```

Das ist der erste Mini-Schritt in Richtung:

```text
Ich kenne nicht genau dieses Zeichen.
Aber die Feld-/Sinneslage erinnert mich an etwas Tragendes.
```

Wichtig:

```text
Der assoziative Transfer ist gedaempft.
Er darf Verwandtschaft anzeigen, aber nicht sofort Handlung erzwingen.
```

Diagnosebefehl:

```text
python -m DIO_MINI.run_transfer --reset-memory --debug-root debug\dio_mini_transfer_diag --memory bot_memory\dio_mini_transfer_diag_memory.json
```

Standard-Auswertung einzelner Mini-Laeufe:

```text
python -m DIO_MINI.analyze_runs --debug-root debug\dio_mini_transfer_diag2\referenz --output-dir debug\dio_mini_transfer_diag2\referenz_summary
```

Die Standard-Auswertung fuehrt dieselben Transferwerte:

```text
trade_readiness
associative_trade
maturity_gap
mature_transfer
```

Aktueller Transfer-Befund:

```text
Referenz:
  Lauf 1-2: Beobachtung
  Lauf 3-6: 2 Trades stabil

Varianz nach Referenz-Memory:
  Lauf 1-2: Beobachtung
  Lauf 3-4: 2 Trades stabil

Rauschen nach Referenz- und Varianz-Memory:
  Lauf 1-2: Beobachtung
  Lauf 3-4: 2 Trades stabil
```

Diagnosewerte:

```text
avg_trade_readiness
max_trade_readiness
avg_associative_trade
max_associative_trade
avg_maturity_gap
max_maturity_gap
avg_mature_transfer
max_mature_transfer
```

Lesart:

```text
associative_trade:
  Wie stark erinnert die neue Sinnes-/Feldlage an eine gelernte Familie?

trade_readiness:
  Wie stark wird daraus bereits tragende Handlungsnaehe?

maturity_gap:
  Wie stark ist die Erinnerung groesser als die aktuelle Reife?

mature_transfer:
  Wie stark fallen Erinnerung und aktuelle Reife zusammen?
```

Befund aus dem Transferlauf:

```text
Beim Wechsel in die Varianz- und Rausch-Welt entsteht bereits
assoziative Erinnerung.

Die Handlungsreife bleibt aber in den ersten neuen Laeufen niedrig.
DIO erkennt also Verwandtschaft im Hintergrund, handelt aber erst nach
lokaler Wiederbestaetigung.
```

Beispiel aus dem Transferlauf:

```text
Varianz Lauf 1:
  max_associative_trade: 0.192199
  max_mature_transfer: 0.013454
  Lesart: erkannt, aber unreif.

Varianz Lauf 4:
  max_associative_trade: 0.117041
  max_mature_transfer: 0.117041
  Lesart: erkannt und lokal tragender.

Rauschen Lauf 1:
  max_associative_trade: 0.120338
  max_mature_transfer: 0.008424
  Lesart: erkannt, aber noch nicht handlungsnah.
```

Das ist fachlich sauberer als sofortiger Transfer:

```text
Nicht: Ich kenne etwas Aehnliches, also handle ich sofort.
Sondern: Ich kenne eine Verwandtschaft, aber diese Welt muss sich erst
lokal als tragend bestaetigen.
```

Naechster Schritt:

```text
Die Transferdiagnose bleibt sichtbar.
Danach wird geprueft, ob DIO zwischen:

1. nicht erkannt,
2. erkannt aber unreif,
3. erkannt und tragend

unterscheiden kann.
```

## Beobachtungsreife ohne Handlung

Erweiterung:

```text
DIO speichert jetzt auch erkannte, aber nicht ausgefuehrte Moeglichkeiten.
```

Diese Spur ist getrennt von Handlungstrust.

Sie bedeutet:

```text
Ich habe hier eine moegliche LONG- oder SHORT-Naehe gesehen.
Ich habe nicht gehandelt.
Aber die Konsequenz dieser Moeglichkeit darf als Beobachtung reifen.
```

Das ist wichtig, damit DIO nicht nur durch ausgefuehrte Trades lernt.
Gleichzeitig darf Beobachtung nicht automatisch zur Handlung werden.

Neue Diagnosewerte:

```text
observation_learning_events
avg_observation_learning_pressure
max_observation_learning_pressure
avg_observation_trade_signal
max_observation_trade_signal
avg_observation_trade_readiness
max_observation_trade_readiness
```

Lesart:

```text
observation_learning_events:
  Wie oft hat DIO eine moegliche Handlung beobachtet, ohne sie auszufuehren?

observation_learning_pressure:
  Wie stark war diese erkannte, aber unreife Handlungsnaehe?

observation_trade_signal:
  Wie stark wirkt die gespeicherte Beobachtung inzwischen als erkannte
  Handlungsnaehe?

observation_trade_readiness:
  Wie stark darf diese Beobachtung die aktuelle Reife mittragen?
```

Befund nach Umsetzung:

```text
Referenz, Varianz und Rauschen bleiben stabil.
DIO beobachtet frueh viele Moeglichkeiten, handelt aber nicht sofort.
Erst nach lokaler Reifung entstehen wieder 2 Trades pro Welt.
```

Beispiel:

```text
Varianz Lauf 1:
  observation_learning_events: 12
  Trades: 0

Varianz Lauf 3:
  observation_learning_events: 2
  Trades: 2
```

Damit ist die Trennung sauberer:

```text
Wahrnehmen
Erinnern
Beobachtend lernen
Handlungsreife entwickeln
Handeln
```

## Beobachtung wird gedämpft handlungsnah

Erweiterung:

```text
Beobachtung bleibt nicht nur passiver Report.
Sie fliesst gedaempft in die Aktionsdiagnose zurueck.
```

Dabei gilt:

```text
Beobachtung erzeugt keine direkte Handlung.
Beobachtung erzeugt einen kleinen Reifeanteil.
Dieser Anteil wirkt nur zusammen mit Feldscore, Symbolfamilie,
assoziativer Erinnerung und Konsequenzspur.
```

Technische Spur:

```text
observation_signal
observation_bias
observation_readiness
```

Befund nach Test:

```text
Der Transferlauf bleibt stabil:
Referenz: 2 Trades nach Reifung
Varianz: 2 Trades nach Reifung
Rauschen: 2 Trades nach Reifung
```

Der Beobachtungsanteil bleibt bewusst klein:

```text
Rauschen Lauf 4:
  max_observation_trade_signal: 0.015763
  max_observation_trade_readiness: 0.001734
```

Lesart:

```text
DIO lernt aus nicht ausgefuehrten Moeglichkeiten.
Diese Spur hilft spaeter bei Reife, uebernimmt aber nicht die Motorik.
```

## Syntaxverdichtung als Diagnose

Erweiterung:

```text
python -m DIO_MINI.analyze_syntax --debug-root debug\dio_mini_observation_maturity\referenz --output-dir debug\dio_mini_observation_maturity\referenz_summary
```

Erzeugt:

```text
dio_mini_syntax_families.csv
dio_mini_syntax_families.json
```

Zweck:

```text
Pruefen, ob DIOs eigene Sprache in Einzelzeichen zerfaellt oder ob sich
stabile Familien bilden.
```

Diagnosewerte:

```text
family
run_count
symbol_count
rows
symbols_per_row
executed_long
executed_short
best_long
best_short
reward_sum
observation_learning_events
```

Befund auf den drei kontrollierten Welten:

```text
Referenz:
  dio_0byw: 6 Runs, 6 Rows, 1 Symbol, Reward 7.9042
  dio_0lt6: 6 Runs, 6 Rows, 1 Symbol, Reward 2.1305

Varianz:
  dio_0n4c: 4 Runs, 4 Rows, 1 Symbol, Reward 2.9390
  dio_0uct: 4 Runs, 4 Rows, 1 Symbol, Reward 0.9564

Rauschen:
  dio_1r0h: 4 Runs, 4 Rows, 1 Symbol, Reward 3.2757
  dio_0f4h: 4 Runs, 4 Rows, 1 Symbol, Reward 0.8174
```

Lesart:

```text
Die Mini-Welten sind derzeit so sauber, dass DIO nicht in viele Worte
zerfaellt. Wiederkehrende Familien bleiben stabil.
```

Einschraenkung:

```text
Das beweist noch keine freie Sprachvarianz.
Dafuer braucht DIO als naechstes eine kontrollierte Welt mit aehnlichen,
aber nicht identischen Form-/Hoer-/Fuehlvarianten.
```

Naechster Schritt:

```text
Eine vierte kontrollierte Welt bauen:
gleiche Grundbedeutung, aber veraenderte sensorische Auspraegung.

Dann pruefen:
Bleibt DIO bei derselben Familie?
Bildet DIO neue Familien?
Kann er beide ueber Beobachtung und Konsequenz verbinden?
```

## Vierte Welt: sensorische Varianz

Kontrollierter Datensatz:

```text
data/kontrolliert_sensorische_varianz_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Die Grundbedeutung bleibt gleich:
zwei tragende Episoden.

Die sensorische Auspraegung ist anders:
andere Kerzenfolge,
andere Lautstaerke,
andere Volumenbewegung,
andere Zwischenzone.
```

Der Datensatz enthaelt weiterhin keine Setup-Labels.

Transferlauf:

```text
python -m DIO_MINI.run_transfer --reset-memory --debug-root debug\dio_mini_sensor_transfer --memory bot_memory\dio_mini_sensor_transfer_memory.json
```

Befund:

```text
Sensorische Varianz Lauf 1:
  Trades: 0
  Beobachtung

Sensorische Varianz Lauf 2:
  Trades: 0
  Beobachtung

Sensorische Varianz Lauf 3:
  Trades: 2
  Reward: 2.9077

Sensorische Varianz Lauf 4:
  Trades: 2
  Reward: 1.8782
```

Syntaxanalyse:

```text
python -m DIO_MINI.analyze_syntax --debug-root debug\dio_mini_sensor_transfer\sensorische_varianz --output-dir debug\dio_mini_sensor_transfer\sensorische_varianz_summary
```

Wichtige Familien:

```text
dio_052z: 4 Runs, 4 Rows, 1 Symbol, Reward 2.1629
dio_0fp8: 4 Runs, 4 Rows, 1 Symbol, Reward 0.7968
dio_0nv8: 3 Runs, 3 Rows, 1 Symbol, Reward 1.8262
```

Lesart:

```text
DIO uebernimmt nicht einfach alte Worte.
DIO bildet fuer die sensorisch veraenderte Welt neue stabile Familien.
```

Gleichzeitig zeigt der Transferbericht weiter alte Erfahrungsfamilien im
Hintergrund:

```text
top_long_family: dio_0byw
top_short_family: dio_1r0h
```

Das ist der wichtige Zwischenbefund:

```text
Neue sensorische Auspraegung erzeugt neue DIO-Sprache.
Alte Erfahrung bleibt assoziativ im Hintergrund.
Handlung entsteht erst nach lokaler Reifung.
```

Naechster Schritt:

```text
Familienverwandtschaft explizit analysieren:

Welche neuen Familien liegen sensorisch/MCM-nah an alten Familien?
Welche neuen Familien tragen dieselbe Konsequenzrichtung?
Welche Familien sind nur zufaellig aehnlich, aber nicht tragend?
```

## Familienverwandtschaft

Werkzeug:

```text
python -m DIO_MINI.analyze_family_relations --memory bot_memory\dio_mini_sensor_transfer_memory.json --output-dir debug\dio_mini_sensor_transfer\family_relations --topn 120
```

Erzeugt:

```text
dio_mini_family_relations.csv
dio_mini_family_relations.json
```

Zweck:

```text
Nicht nur fragen:
Kenne ich dieses Wort?

Sondern:
Welche Wortfamilie liegt sensorisch/MCM-nah an einer anderen?
Traegt sie dieselbe Konsequenzrichtung?
Oder ist sie nah, aber gegensinnig?
```

Diagnosewerte:

```text
distance
similarity
left_action
right_action
same_action
long_alignment
short_alignment
cross_alignment
```

Wichtiger Befund:

```text
dio_052z <-> dio_0byw
  similarity: 0.960513
  actions: LONG / LONG
  Lesart: neue sensorische LONG-Familie ist nahe an alter LONG-Familie.

dio_0fp8 <-> dio_0lt6
  similarity: 0.970988
  actions: SHORT / SHORT
  Lesart: neue sensorische SHORT-Familie ist nahe an alter SHORT-Familie.

dio_0nv8 <-> dio_0vyd
  similarity: 0.962667
  actions: SHORT / SHORT
  Lesart: weitere neue SHORT-Familie findet verwandte alte Richtung.
```

Ebenso wichtig:

```text
dio_0byw <-> dio_0n4c
  similarity: 0.997430
  actions: LONG / SHORT
  Lesart: sehr nahe Feld-/Sinneslage, aber gegensinnige Konsequenz.
```

Damit wird sichtbar:

```text
Naehesignal allein reicht nicht.
DIO braucht Naehe plus Konsequenzrichtung plus lokale Reife.
```

Das ist fachlich wichtig, weil sonst Transfer zu grob wuerde.

Zwischenstand:

```text
DIO bildet neue Sprache fuer neue sensorische Auspraegung.
DIO findet gleichzeitig verwandte alte Familien.
DIO kann auch Konfliktverwandtschaften sichtbar machen.
```

Naechster Schritt:

```text
Verwandtschaft nicht als Handlungssignal benutzen,
sondern als Reflexions-/Lernkarte:

Diese neue Familie erinnert an diese alte Familie.
Aber die Richtung muss lokal bestaetigt werden.
```

## Reflexionskarte

Werkzeug:

```text
python -m DIO_MINI.build_reflection_map --memory bot_memory\dio_mini_sensor_transfer_memory.json --output-dir debug\dio_mini_sensor_transfer\reflection_map
```

Erzeugt:

```text
dio_mini_reflection_map.csv
dio_mini_reflection_map.json
```

Zweck:

```text
Pro DIO-Wortfamilie wird sichtbar:

Welche andere Familie unterstuetzt meine Richtung?
Welche andere Familie ist nah, aber gegensinnig?
Wie stark ist Support?
Wie stark ist Konflikt?
```

Diagnosewerte:

```text
support_count
conflict_count
best_support_family
best_support_action
best_support_similarity
best_support_score
best_conflict_family
best_conflict_actions
best_conflict_similarity
best_conflict_score
support_ratio
conflict_ratio
```

Befund:

```text
dio_052z:
  best_support_family: dio_0byw
  best_support_action: LONG
  best_support_similarity: 0.960513

dio_0fp8:
  best_support_family: dio_0lt6
  best_support_action: SHORT
  best_support_similarity: 0.970988

dio_0nv8:
  best_support_family: dio_0vyd
  best_support_action: SHORT
  best_support_similarity: 0.962667
```

Damit wird sichtbar:

```text
Neue Familien koennen alte Erfahrung wiederfinden,
ohne alte Worte einfach zu kopieren.
```

Konfliktbeispiel:

```text
dio_0byw:
  best_support_family: dio_052z
  best_support_action: LONG
  best_conflict_family: dio_0n4c
  best_conflict_actions: LONG/SHORT
```

Lesart:

```text
Eine Familie kann zugleich tragende Verwandtschaft und Konfliktverwandtschaft
besitzen.
```

Das ist genau der Grund, warum die Reflexionskarte nicht direkt handeln darf.
Sie ist eine innere Lesekarte:

```text
Diese Familie erinnert mich an jene.
Aber die Richtung ist entweder bestaetigend oder widersprechend.
Ich muss die lokale Realitaet weiter pruefen.
```

Zwischenstand:

```text
DIO_MINI besitzt jetzt:

1. eigene Syntax,
2. Familienreife,
3. Beobachtungslernen,
4. assoziativen Transfer,
5. Familienverwandtschaft,
6. Reflexionskarte fuer Support und Konflikt.
```

Naechster Schritt:

```text
Die Reflexionskarte mit lokaler Bestaetigung verbinden:

Nicht handeln.
Nur sichtbar machen:
Diese Familie hat verwandte Erfahrung,
aber die aktuelle Welt hat sie schon lokal bestaetigt oder noch nicht.
```

## Lokale Bestaetigung der Reflexionskarte

Werkzeug:

```text
python -m DIO_MINI.local_confirmation --debug-root debug\dio_mini_sensor_transfer\sensorische_varianz --reflection-map debug\dio_mini_sensor_transfer\reflection_map\dio_mini_reflection_map.csv --output-dir debug\dio_mini_sensor_transfer\sensorische_varianz_confirmation
```

Erzeugt:

```text
dio_mini_local_confirmation.csv
dio_mini_local_confirmation.json
```

Zweck:

```text
Die Reflexionskarte zeigt Verwandtschaft.
Die lokale Bestaetigung zeigt, ob diese Verwandtschaft in der aktuellen Welt
bereits durch reale Handlung/Konsequenz getragen wurde.
```

Damit wird getrennt:

```text
executed_local_confirmation:
  Die Familie wurde in der aktuellen Welt gehandelt und durch Konsequenz
  lokal bestaetigt.

observed_related_potential:
  Die Familie sieht verwandte Erfahrung und wurde beobachtet, aber noch nicht
  als reale Handlung bestaetigt.

unexecuted_local_potential:
  Es gibt lokale Naehe, aber keine ausgefuehrte Konsequenz.

unconfirmed:
  Keine ausreichende lokale Spur.
```

Befund aus der vierten sensorischen Varianz-Welt:

```text
dio_052z:
  label: executed_local_confirmation
  local_action: LONG
  support: dio_0byw

dio_0nv8:
  label: executed_local_confirmation
  local_action: SHORT
  support: dio_0vyd

dio_0fp8:
  label: executed_local_confirmation
  local_action: SHORT
  support: dio_0lt6
```

Beobachtete, aber nicht gehandelte Verwandtschaften bleiben sichtbar:

```text
dio_18iw:
  label: observed_related_potential
  local_action: SHORT
  support: dio_0309
```

Fachliche Lesart:

```text
Erinnerung ist nicht Realitaet.
Verwandtschaft ist nicht Handlung.
Lokale Bestaetigung ist der Realitaetsanker.
```

Damit wird verhindert, dass DIO aus reiner Erinnerung oder Gedankennaehe
handelt. Eine Familie darf verwandt wirken, sie muss aber in der aktuellen
Welt durch reale Konsequenz oder wiederholte Beobachtung reifen.

Zwischenstand:

```text
DIO_MINI kann jetzt unterscheiden:

1. Ich erkenne eine Familie.
2. Diese Familie erinnert an andere Erfahrung.
3. Diese Erinnerung unterstuetzt oder widerspricht.
4. Die aktuelle Welt hat diese Familie lokal bestaetigt oder nur beobachtet.
```

Naechster Schritt:

```text
Die lokale Bestaetigung nicht in Motorik zurueckfuehren.
Zuerst als Lernkarte halten:

Welche Familien werden wiederholt lokal bestaetigt?
Welche bleiben nur beobachtetes Potenzial?
Welche geraten in Konflikt mit aehnlicher alter Erfahrung?
```

## Bestaetigungshistorie ueber mehrere Welten

Werkzeug:

```text
python -m DIO_MINI.analyze_confirmation_history --debug-root debug\dio_mini_sensor_transfer --reflection-map debug\dio_mini_sensor_transfer\reflection_map\dio_mini_reflection_map.csv --output-dir debug\dio_mini_sensor_transfer\confirmation_history
```

Erzeugt:

```text
dio_mini_confirmation_history_summary.csv
dio_mini_confirmation_history_details.csv
dio_mini_confirmation_relation_summary.csv
```

Zweck:

```text
Nicht nur gleiche Wortfamilien zaehlen.
DIO darf in einer neuen Welt neue Woerter bilden.

Wichtiger ist:
Welche neue Familie findet eine verwandte alte Familie?
Wurde diese Verwandtschaft lokal bestaetigt?
Bleibt sie nur beobachtetes Potenzial?
```

Befund:

```text
relation=dio_052z<->dio_0byw
  phases: 2
  executed_local_confirmation: 2

relation=dio_0n4c<->dio_1r0h
  phases: 2
  executed_local_confirmation: 2

relation=dio_0fp8<->dio_0lt6
  phases: 2
  executed_local_confirmation: 2
```

Weitere Relationen zeigen Mischzustand:

```text
relation=dio_0nv8<->dio_0vyd
  phases: 2
  executed_local_confirmation: 1
  observed_related_potential: 1
```

Fachliche Lesart:

```text
Die exakte Sprache muss nicht identisch bleiben.
Die Form-/MCM-Verwandtschaft kann trotzdem wiederkehren.
```

Das ist wichtig fuer emergente Sprachentwicklung:

```text
Nicht: Ich erkenne nur dasselbe Wort wieder.
Sondern: Ich erkenne, dass ein neues Wort eine aehnliche Feld-/Sinneslage
traegt wie eine alte Erfahrung.
```

Aktueller Status:

```text
DIO_MINI hat noch keine Motorik aus dieser Historie.
Die Historie bleibt Lern- und Reflexionskarte.
```

Naechster Schritt:

```text
Pruefen, welche dieser Relationen stabil bleiben, wenn ein neuer kontrollierter
Datensatz mit anderer Reihenfolge oder anderer Lautstaerke/Formauspraegung
hinzukommt.

Erst wenn Relationen wiederholt lokal bestaetigt werden, darf spaeter eine
weiche Reifenaehe entstehen.
```

## Fuenfte kontrollierte Welt: sensorischer Drift

Kontrollierter Datensatz:

```text
data/kontrolliert_sensorischer_drift_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Gleiche Grundaufgabe, aber andere Drift, andere Lautstaerke,
andere Volumenwirkung und veraenderte Formauspraegung.
```

Transferlauf mit frischem Memory:

```text
python -m DIO_MINI.run_transfer --reset-memory --debug-root debug\dio_mini_drift_transfer --memory bot_memory\dio_mini_drift_transfer_memory.json
```

Befund:

```text
Referenz:
  Lauf 1-2: 0 Trades
  Lauf 3-6: 2 Trades

Varianz:
  Lauf 1-2: 0 Trades
  Lauf 3-4: 2 Trades

Rauschen:
  Lauf 1-2: 0 Trades
  Lauf 3-4: 2 Trades

Sensorische Varianz:
  Lauf 1-2: 0 Trades
  Lauf 3-4: 2 Trades

Sensorischer Drift:
  Lauf 1-4: 2 Trades
```

Lesart:

```text
In der fuenften Welt beginnt DIO nicht mehr bei null.
Die frueheren Syntax-/MCM-Familien tragen bereits genug Verwandtschaft,
dass DIO sofort zwei reale Kontakte findet.
```

Lokale Drift-Bestaetigung:

```text
dio_0byw:
  label: executed_local_confirmation
  local_action: LONG
  support: dio_052z

dio_0b0d:
  label: executed_local_confirmation
  local_action: SHORT
  support: dio_074d
```

Relationenhistorie nach fuenf Welten:

```text
relation=dio_052z<->dio_0byw
  phases: 3
  executed_local_confirmation: 3

relation=dio_0n4c<->dio_1r0h
  phases: 2
  executed_local_confirmation: 2

relation=dio_0fp8<->dio_0lt6
  phases: 2
  executed_local_confirmation: 2
```

Bedeutung:

```text
Die Sprache variiert.
Die verwandte Sinnes-/MCM-Struktur bleibt trotzdem tragbar.
```

Aktuelle Grenze:

```text
Diese Relationen bleiben Diagnose und Lernkarte.
Sie werden noch nicht als Entry-Regel benutzt.
```

Naechster Schritt:

```text
Die stabilsten Relationen als semantische Reifespur im Mini-Memory halten,
ohne Motorik daraus abzuleiten.

Danach pruefen:
Kann DIO bei neuer Welt frueher erkennen, aber weiterhin nur handeln,
wenn lokale Realitaet und Konsequenz mittragen?
```

## Passive Relationsspur im Mini-Memory

Erweiterung:

```text
DIO_MINI.semantic_memory.SemanticMemory
```

enthaelt jetzt zusaetzlich:

```text
relations
```

Diese Ebene speichert bestaetigte oder beobachtete Verwandtschaftspaare:

```text
support_pair
families
phases
executed_local_confirmation
observed_related_potential
avg_local_confirmation
max_local_confirmation
reward_sum
passive_only
```

Wichtig:

```text
relations wird nicht von action_diagnostics gelesen.
relations erzeugt keine action_bias.
relations erzeugt keine action_readiness.
```

Die Relationenspur ist damit nur:

```text
Reflexionskarte
semantische Reifespur
spaetere Vergleichsgrundlage
```

Werkzeug:

```text
python -m DIO_MINI.store_confirmation_relations --memory bot_memory\dio_mini_drift_transfer_memory.json --relation-summary debug\dio_mini_drift_transfer\confirmation_history\dio_mini_confirmation_relation_summary.csv
```

Befund:

```text
44 Relationen im Mini-Memory gespeichert.
Alle sind mit passive_only markiert.
```

Staerkste gespeicherte Relation:

```text
dio_052z<->dio_0byw:
  phase_count: 3
  executed_local_confirmation: 3
  passive_only: true
```

Fachliche Lesart:

```text
DIO erinnert jetzt nicht nur einzelne Woerter.
DIO kann auch merken, dass zwei unterschiedliche Woerter eine verwandte
Sinnes-/MCM-Struktur getragen haben.
```

Das ist noch kein Handeln.
Es ist eine semantische Tiefenspur.

Naechster Schritt:

```text
Eine neue Welt mit bestehendem relations-Memory laufen lassen.
Pruefen, ob Erkennung frueher entsteht, ohne dass die Motorik automatisch
aus Relationsnaehe handelt.
```

## Passivitaetspruefung der Relationsspur

Neue kontrollierte Welt:

```text
data/kontrolliert_sensorischer_shift_2episoden_5m_SOLUSDT.csv
```

Pruefaufbau:

```text
Gleicher Memory-Zustand A:
  mit relations

Gleicher Memory-Zustand B:
  ohne relations
```

Beide Memories liefen gegen dieselbe neue Welt:

```text
python -m DIO_MINI.run_transfer --phase sensorischer_shift:data/kontrolliert_sensorischer_shift_2episoden_5m_SOLUSDT.csv:4 --debug-root debug\dio_mini_relation_passive_with --memory bot_memory\dio_mini_relation_with_memory.json

python -m DIO_MINI.run_transfer --phase sensorischer_shift:data/kontrolliert_sensorischer_shift_2episoden_5m_SOLUSDT.csv:4 --debug-root debug\dio_mini_relation_passive_without --memory bot_memory\dio_mini_relation_without_memory.json
```

Ergebnis:

```text
Mit relations:
  Lauf 1: 0 Trades
  Lauf 2: 0 Trades
  Lauf 3: 2 Trades
  Lauf 4: 3 Trades

Ohne relations:
  Lauf 1: 0 Trades
  Lauf 2: 0 Trades
  Lauf 3: 2 Trades
  Lauf 4: 3 Trades
```

Die `transfer_summary.csv` Dateien waren identisch.

Lesart:

```text
relations beeinflusst die Motorik aktuell nicht.
Die Relationsspur ist wirklich passiv.
```

Semantischer Befund der Shift-Welt:

```text
dio_1lam:
  label: executed_local_confirmation
  local_action: LONG
  support: dio_0byw

dio_1hzf:
  label: executed_local_confirmation
  local_action: SHORT
  support: dio_1bzs

dio_1r0b:
  label: executed_local_confirmation
  local_action: SHORT
  support: dio_0fp8

dio_1mml:
  label: executed_local_confirmation
  local_action: LONG
  support: dio_0uct
```

Bedeutung:

```text
Neue Woerter entstehen.
Diese neuen Woerter finden alte Support-Familien.
Aber diese Support-Familien steuern die Handlung nicht direkt.
```

Technischer Hinweis:

```text
build_reflection_map und local_confirmation muessen sequenziell laufen.
Wenn local_confirmation parallel zur Map-Erzeugung gestartet wird,
kann eine alte oder unvollstaendige Map gelesen werden.
```

Naechster Schritt:

```text
Die 3 Trades im vierten Shift-Lauf untersuchen:

Ist der dritte Trade eine echte zweite Long-Nahe,
oder ist es ein noch zu schwach gebundener Kontakt derselben Episode?
```

## Kontaktanalyse ohne harte Kontaktklassen

Werkzeug:

```text
python -m DIO_MINI.analyze_episode_contacts --debug-root debug\dio_mini_relation_passive_with\sensorischer_shift --output-dir debug\dio_mini_relation_passive_with\sensorischer_shift_contacts
```

Erzeugt:

```text
dio_mini_episode_contacts.csv
dio_mini_episode_contact_summary.csv
```

Zweck:

```text
Nicht neue Regeln bauen.
Nur sichtbar machen:
Welche Kontakte wurden ausgefuehrt?
Welche Kontakte wurden als gleiche Episode gehalten?
Wie stark war die Konsequenz relativ zu den anderen positiven Kontakten?
```

Wichtig:

```text
Die Diagnose nutzt keine harte starke/schwache Kontaktklasse.
Sie schreibt positive Kontakte und eine relative_positive_reward-Spur.
```

Befund im vierten Shift-Lauf:

```text
tick 1:
  family: dio_1lam
  action: LONG
  reward: 1.29944
  relative_positive_reward: 0.872683

tick 7:
  family: dio_1r0b
  action: SHORT
  reward: 0.979702
  relative_positive_reward: 0.657952

tick 15:
  family: dio_1mml
  action: LONG
  reward: 0.237245
  relative_positive_reward: 0.15933
```

Lesart:

```text
Der dritte LONG war positiv, aber deutlich kleiner getragen als die beiden
Hauptkontakte.
```

Das ist kein Fehlerbeweis. Es zeigt aber den naechsten Mini-Pruefpunkt:

```text
DIO soll positive kleine Nachkontakte speichern duerfen.
Aber diese Spur muss als kleinere Konsequenz reifen und darf nicht gleich stark
wie ein klarer Hauptkontakt wirken.
```

Aktueller Stand:

```text
Das passiert bereits teilweise ueber die Reward-Hoehe.
Die naechste Pruefung ist, ob diese schwachere Konsequenz im Familiengedaechtnis
auch sichtbar schwach bleibt.
```

## Passive Timing-Konsequenz

Erweiterung:

```text
SemanticMemory.learn(..., timing_improvement=...)
```

speichert jetzt passiv:

```text
timing_improvement_sum
last_timing_improvement
```

pro Symbol-/Familien-Aktion.

Bedeutung:

```text
Ich habe gehandelt.
Die Konsequenz war positiv oder negativ.
Zusaetzlich merke ich:
Haette es im gleichen Zukunftsfenster einen besseren erreichbaren Kontaktpreis
gegeben?
```

Wichtig:

```text
Timing-Konsequenz steuert keine Motorik.
Sie veraendert keine action_bias.
Sie veraendert keine action_readiness.
```

Sie ist nur eine passive Reifespur:

```text
Dieser Kontakt hat getragen,
aber mein Einstieg hatte noch Verbesserungsraum.
```

Neue Debug-Spalten in `episodes.csv`:

```text
entry_price
entry_improvement_room
```

Diagnosewerkzeug:

```text
python -m DIO_MINI.analyze_contact_timing --debug-root debug\dio_mini_shift_followup\sensorischer_shift --data data\kontrolliert_sensorischer_shift_2episoden_5m_SOLUSDT.csv --output-dir debug\dio_mini_shift_followup\sensorischer_shift_timing
```

Befund Follow-up:

```text
dio_0odx:
  avg_reward: 0.2605
  avg_entry_improvement_room: 0.003736

dio_1cpq:
  avg_reward: 1.2922
  avg_entry_improvement_room: 0.001591

dio_1lam:
  avg_reward: 1.2994
  avg_entry_improvement_room: 0.001799
```

Lesart:

```text
dio_0odx traegt positiv, aber mit groesserem Timing-Verbesserungsraum.
Das spricht fuer frueheren Kontakt vor besserem erreichbaren Preisbereich.
```

Fachlich:

```text
Nicht blockieren.
Nicht als Regel behandeln.
Nur als Koerpererfahrung speichern:
Dieser Kontakt war nutzbar, aber nicht optimal getragen.
```

## Timing-Memory-Stabilitaet

Werkzeug:

```text
python -m DIO_MINI.analyze_timing_memory --memory bot_memory\dio_mini_timing_stability_memory.json --output-dir debug\dio_mini_timing_stability\timing_memory
```

Erzeugt:

```text
dio_mini_timing_memory_families.csv
dio_mini_timing_memory_symbols.csv
```

Zweck:

```text
Die Timing-Erfahrung direkt aus dem Mini-Gedaechtnis lesen.
Nicht nur aus einem einzelnen Lauf.
```

Stabilitaetslauf:

```text
python -m DIO_MINI.run_transfer --phase timing_stability:data\kontrolliert_sensorischer_shift_2episoden_5m_SOLUSDT.csv:4 --debug-root debug\dio_mini_timing_stability --memory bot_memory\dio_mini_timing_stability_memory.json
```

Befund:

```text
Lauf 32: 3 Trades, Reward 3.3688
Lauf 33: 3 Trades, Reward 3.3688
Lauf 34: 3 Trades, Reward 3.3688
Lauf 35: 3 Trades, Reward 3.3688
```

Memory-Befund:

```text
dio_0odx SHORT:
  count: 13
  avg_reward: 0.20637
  avg_timing_improvement: 0.001437

dio_0t45 SHORT:
  count: 9
  avg_reward: 1.44712
  avg_timing_improvement: 0.000878

dio_1lam LONG:
  count: 13
  avg_reward: 1.209479
  avg_timing_improvement: 0.000692
```

Lesart:

```text
dio_0odx bleibt positiv, aber mit niedrigerem Reward und groesserem
Timing-Verbesserungsraum.

dio_0t45 und dio_1lam tragen deutlich besser und haben geringeren
Timing-Verbesserungsraum.
```

Das ist eine saubere passive Koerpererfahrung:

```text
Nicht jeder positive Kontakt traegt gleich.
Ein Kontakt kann positiv sein und trotzdem zeigen:
Mein Timing war noch unreif.
```

Naechster Schritt:

```text
Kontaktqualitaet als Diagnose sichtbar machen:

Reward-Tragfaehigkeit
Timing-Verbesserungsraum
Trust
Caution

Aber weiterhin ohne Motorik-Rueckfuehrung.
```

## Kontaktqualitaet als kontinuierliche Diagnose

Werkzeug:

```text
python -m DIO_MINI.analyze_contact_quality --memory bot_memory\dio_mini_timing_stability_memory.json --output-dir debug\dio_mini_timing_stability\contact_quality
```

Erzeugt:

```text
dio_mini_contact_quality.csv
dio_mini_contact_quality.json
```

Wichtig:

```text
Diese Diagnose nutzt keine harten Qualitaetsklassen.
Sie schreibt nur kontinuierliche Spuren.
```

Werte:

```text
carrying_trace:
  positive Konsequenzspur multipliziert mit Vertrauen minus Vorsicht.

consequence_balance:
  Vertrauen minus Vorsicht.

timing_residue:
  gespeicherter Timing-Verbesserungsraum.

timing_to_carrying:
  Verhaeltnis zwischen Timing-Rest und tragender Spur.
```

Befund:

```text
dio_0t45 SHORT:
  carrying_trace: 1.4471
  timing_residue: 0.000878
  timing_to_carrying: 0.000607

dio_1lam LONG:
  carrying_trace: 1.2095
  timing_residue: 0.000692
  timing_to_carrying: 0.000572

dio_0byw LONG:
  carrying_trace: 1.4312
  timing_residue: 0.000000
  timing_to_carrying: 0.000000
```

Lesart:

```text
Die Diagnose zeigt nur Relationen.
Sie entscheidet nicht.
```

Das bleibt fachlich wichtig:

```text
DIO bekommt Erfahrungsspuren, keine Regel:
So war mein Kontakt.
So stark hat er getragen.
So viel Timing-Rest war noch vorhanden.
```

## Reihenfolge-Shift als Transferpruefung

Kontrollierter Datensatz:

```text
data/kontrolliert_reihenfolge_shift_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Die Kontaktreihenfolge wird veraendert.
Die Welt beginnt mit einer Short-naeheren Bewegung und spaeter entsteht die
Long-naehere Bewegung.
```

Lauf:

```text
python -m DIO_MINI.run_transfer --phase order_shift:data\kontrolliert_reihenfolge_shift_2episoden_5m_SOLUSDT.csv:4 --debug-root debug\dio_mini_order_shift --memory bot_memory\dio_mini_order_shift_memory.json
```

Befund:

```text
Lauf 36: 1 Trade, Reward 2.0000
Lauf 37: 2 Trades, Reward 1.5689
Lauf 38: 2 Trades, Reward 3.1736
Lauf 39: 2 Trades, Reward 2.6650
```

Interpretation:

```text
Der Reihenfolgewechsel ist nicht trivial.
DIO beginnt nicht sofort perfekt, stabilisiert sich aber wieder auf zwei
Kontakte.
```

Belastete Spur:

```text
dio_00eh SHORT:
  avg_reward: 0.143564
  trust: 0.070059
  caution: 0.060361
  consequence_balance: 0.009698
  avg_timing_improvement: 0.001033
  timing_to_carrying: 0.741947
```

Lesart:

```text
dio_00eh SHORT ist keine tragende Hauptspur.
Die Familie hat etwas gelernt, aber die Balance bleibt sehr klein und der
Timing-Rest ist im Verhaeltnis zur Tragspur gross.
```

Wichtig:

```text
Diese Spur wird nicht geloescht.
Sie wird auch nicht hart blockiert.
Sie bleibt als schwache, vorsichtige Konsequenzspur erhalten.
```

Tragendere neue Reihenfolge-Spuren:

```text
dio_121e SHORT:
  avg_reward: 1.1789
  consequence_balance: 0.4912

dio_1d6j LONG:
  avg_reward: 0.7578
  consequence_balance: 0.2799
```

Naechster Schritt:

```text
Die schwache Vorsichtsspur von dio_00eh beobachten:
Taucht sie bei weiterer Variation erneut belastet auf,
oder verschwindet sie zugunsten tragenderer Familien?
```

## Zweite Reihenfolge-Variation

Kontrollierter Datensatz:

```text
data/kontrolliert_reihenfolge_shift_varianz_2episoden_5m_SOLUSDT.csv
```

Lauf:

```text
python -m DIO_MINI.run_transfer --phase order_shift_varianz:data\kontrolliert_reihenfolge_shift_varianz_2episoden_5m_SOLUSDT.csv:4 --debug-root debug\dio_mini_order_shift_varianz --memory bot_memory\dio_mini_order_shift_varianz_memory.json
```

Befund:

```text
Lauf 40: 1 Trade, Reward 0.9061
Lauf 41: 2 Trades, Reward 1.8999
Lauf 42: 2 Trades, Reward 2.5759
Lauf 43: 2 Trades, Reward 2.5759
```

Kontaktbefund:

```text
positive_executed_contact: 7
burdened_executed_contact: 0
held_same_episode_contact: 5
```

`dio_00eh`:

```text
taucht in dieser Variation nicht mehr als Kontakt auf.
bleibt nur als alte schwache Memory-Spur vorhanden.
```

Neue tragende Spuren:

```text
dio_1ioc SHORT:
  Lauf 40-41: beobachtet
  Lauf 42-43: ausgefuehrt

dio_1d6j LONG:
  Lauf 40-43: ausgefuehrt
```

Werkzeug:

```text
python -m DIO_MINI.analyze_family_persistence --debug-root debug\dio_mini_order_shift_varianz\order_shift_varianz --family dio_00eh --family dio_1ioc --family dio_1d6j --family dio_1sxo --output-dir debug\dio_mini_order_shift_varianz\persistence
```

Lesart:

```text
Die belastete Familie wurde nicht geloescht und nicht hart blockiert.
Sie wurde in der naechsten Variation schlicht nicht wieder aufgenommen.

Stattdessen reifen andere Familien:
eine durchgehende Long-Spur und eine Short-Spur, die erst beobachtet und dann
gehandelt wird.
```

Das ist fachlich der gewuenschte Mechanismus:

```text
Nicht: Verbot.
Sondern: Erfahrung bleibt liegen, neue tragendere Verknuepfung uebernimmt.
```

Naechster Schritt:

```text
Persistenzdiagnose allgemeiner machen:
Nicht nur manuell ausgewaehlte Familien,
sondern alle Familien, die von Beobachtung zu Handlung wechseln,
oder von Handlung zu reiner Memory-Spur verschwinden.
```

## Allgemeine Familienpersistenz

Werkzeug:

```text
python -m DIO_MINI.analyze_family_persistence --debug-root debug\dio_mini_order_shift_varianz\order_shift_varianz --output-dir debug\dio_mini_order_shift_varianz\persistence_all
```

Erzeugt:

```text
dio_mini_family_persistence.csv
dio_mini_family_persistence_summary.csv
```

Zweck:

```text
Nicht nur ausgewaehlte Familien pruefen.
Alle Familien werden darauf untersucht, ob sie:

1. beobachtet bleiben,
2. von Beobachtung zu Handlung reifen,
3. durchgehend handlungsnah bleiben,
4. rohen Druck erzeugen, aber gehalten werden.
```

Befund zweite Reihenfolge-Variation:

```text
dio_1ioc:
  transition: observation_to_execution
  runs: 4
  executed_runs: 2
  observed_runs: 2
  reward: 3.3397

dio_1sxo:
  transition: observation_to_execution
  runs: 2
  executed_runs: 1
  observed_runs: 1
  reward: 0.9938

dio_1d6j:
  transition: persistent_execution
  runs: 4
  executed_runs: 4
  reward: 3.6243
```

Weitere Spuren:

```text
dio_03fl, dio_1hkr, dio_1ytj:
  transition: raw_pressure_held

dio_151h, dio_066x, dio_0iy2:
  transition: stable_observation
```

Lesart:

```text
DIO bildet nicht nur Aktion.
DIO bildet Uebergangszustaende:

Ich sehe es.
Ich halte es.
Ich beobachte es wieder.
Ich handle spaeter.
Oder ich lasse es als Beobachtung liegen.
```

Das ist der wichtigste Mini-Befund dieser Stufe:

```text
Reifung ist als Prozess sichtbar, nicht nur als Tradezaehler.
```

Naechster Schritt:

```text
Diese Persistenzdiagnose fuer mehrere kontrollierte Welten vergleichbar
machen, damit sichtbar wird:

Welche Familien reifen weltuebergreifend?
Welche bleiben nur lokale Sprache einer einzelnen Welt?
```

## Weltuebergreifende Persistenz

Werkzeug:

```text
python -m DIO_MINI.analyze_cross_world_persistence --phase shift:debug\dio_mini_shift_followup\sensorischer_shift --phase order_shift:debug\dio_mini_order_shift\order_shift --phase order_shift_varianz:debug\dio_mini_order_shift_varianz\order_shift_varianz --output-dir debug\dio_mini_cross_world_persistence
```

Erzeugt:

```text
dio_mini_cross_world_persistence_details.csv
dio_mini_cross_world_persistence_phase_summary.csv
dio_mini_cross_world_persistence_world_summary.csv
```

Zweck:

```text
Lokale Woerter von weltuebergreifenden Reifemustern unterscheiden.
```

Befund:

```text
dio_1d6j:
  phases: order_shift, order_shift_varianz
  phase_count: 2
  executed_runs: 5
  observed_runs: 3
  reward_sum: 4.7681
```

Phasenvergleich:

```text
order_shift:
  dio_1d6j
  executed_runs: 1
  observed_runs: 3
  reward_sum: 1.143781

order_shift_varianz:
  dio_1d6j
  executed_runs: 4
  observed_runs: 0
  reward_sum: 3.624284
```

Lesart:

```text
dio_1d6j ist aktuell das erste sichtbare weltuebergreifende Reifemuster.
Es beginnt in einer Welt noch stark beobachtend und wird in der naechsten
aehnlichen Welt persistent handlungsnah.
```

Gegenbeispiel:

```text
dio_00eh:
  phase_count: 1
  transition: execution_to_nonexecution
  reward_sum: -0.431148
```

Lesart:

```text
dio_00eh bleibt lokale Belastungsspur.
Sie persistiert nicht weltuebergreifend als Handlung.
```

Fachliche Bedeutung:

```text
DIO_MINI beginnt zu unterscheiden:

lokale Sprache
lokale Belastung
beobachtete Spur
weltuebergreifende Reifespur
```

Naechster Schritt:

```text
Nicht handeln daraus ableiten.
Zuerst weitere Welten hinzufuegen und pruefen,
ob dio_1d6j oder verwandte Familien weiter weltuebergreifend tragen.
```

## Drift-Welt als naechste Belastungsvarianz

Kontrollierter Datensatz:

```text
data/kontrolliert_reihenfolge_shift_drift_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Die Reihenfolge-Shift-Welt wird nicht nur anders sortiert, sondern sensorisch
leicht verschoben. DIO soll nicht eine Strecke auswendig erkennen, sondern
pruefen, ob seine eigene Form-/MCM-Sprache unter Drift weiter tragfaehige
Familien bildet.
```

Start:

```text
Memory-Basis:
bot_memory\dio_mini_order_shift_varianz_memory.json

Neue Drift-Memory:
bot_memory\dio_mini_order_shift_drift_memory.json
```

Test:

```text
python -m DIO_MINI.run_transfer --phase order_shift_drift:data\kontrolliert_reihenfolge_shift_drift_2episoden_5m_SOLUSDT.csv:4 --debug-root debug\dio_mini_order_shift_drift --memory bot_memory\dio_mini_order_shift_drift_memory.json
```

Befund:

```text
Lauf 44: 1 Trade, Reward 1.1478
Lauf 45: 1 Trade, Reward 1.1478
Lauf 46: 3 Trades, Reward 2.6023
Lauf 47: 3 Trades, Reward 3.6442
```

Kontaktqualitaet:

```text
positive_executed_contact:
  count: 7
  avg_reward: 1.2559
  max_reward: 1.5550

burdened_executed_contact:
  count: 1
  avg_reward: -0.2495

observed_potential:
  count: 27
```

Wichtige Familien:

```text
dio_1fqy:
  transition: observation_to_execution
  executed_runs: 2
  observed_runs: 2
  reward: 3.1099

dio_1ytj:
  transition: persistent_execution in der Drift-Welt
  executed_runs: 3
  reward: 3.4434

dio_0lt6:
  einzelner belasteter Kontakt
  reward: -0.2495
  kein weltuebergreifender Nachweis
```

Lesart:

```text
Die Drift-Welt bestaetigt nicht einfach die alten Familien.
Sie erzeugt eine neue lokale tragende Spur und einen einzelnen belasteten
Kontakt. Dieser belastete Kontakt wird nicht blockiert und nicht geloescht,
sondern bleibt als Konsequenzspur im Gedaechtnis.
```

## Cross-World-Persistenz mit Drift

Werkzeug:

```text
python -m DIO_MINI.analyze_cross_world_persistence --phase shift:debug\dio_mini_shift_followup\sensorischer_shift --phase order_shift:debug\dio_mini_order_shift\order_shift --phase order_shift_varianz:debug\dio_mini_order_shift_varianz\order_shift_varianz --phase order_shift_drift:debug\dio_mini_order_shift_drift\order_shift_drift --output-dir debug\dio_mini_cross_world_persistence_v2
```

Befund:

```text
dio_1d6j:
  phases: order_shift, order_shift_varianz
  phase_count: 2
  dominant_transition: observation_to_execution
  executed_runs: 5
  observed_runs: 3
  reward_sum: 4.7681

dio_1ytj:
  phases: order_shift_varianz, order_shift_drift
  phase_count: 2
  dominant_transition: raw_pressure_held
  executed_runs: 3
  observed_runs: 4
  held_runs: 2
  reward_sum: 3.4434
```

Lesart:

```text
dio_1d6j bleibt die stabilste weltuebergreifende Reifespur.
dio_1ytj ist eine zweite weltuebergreifende Spur, aber noch nicht voll
ruhig gereift: sie traegt in der Drift-Welt, hatte vorher aber noch rohen
Druck und gehaltene Naehe.
```

Fachlich wichtig:

```text
Die Diagnose bleibt passiv.
Weltuebergreifende Persistenz erzeugt keine Entry-Regel.
Sie zeigt nur, welche eigene DIO-Syntax wiederkehrt, gehalten wird,
handlungsnah wird oder als belastete lokale Spur liegen bleibt.
```

Naechster Schritt:

```text
Die naechste Mini-Stufe ist keine neue Strategie.
Sie ist eine sauberere Reifediagnose:

1. Was bleibt nur lokale Sprache?
2. Was wird weltuebergreifende Reifespur?
3. Was erzeugt Druck, ohne stabil handlungsnah zu werden?
4. Welche Sensorik aus Sehen, Hoeren und Fuehlen war bei diesen Spuren
   gemeinsam tragend?
```

## Sensorische Reifediagnose

Werkzeug:

```text
python -m DIO_MINI.analyze_sensor_maturity --debug-root debug\dio_mini_order_shift_drift\order_shift_drift --output-dir debug\dio_mini_order_shift_drift\sensor_maturity
```

Erzeugt:

```text
dio_mini_sensor_maturity.csv
dio_mini_sensor_maturity.json
```

Zweck:

```text
Nicht entscheiden.
Nur lesen, wie eine Symbolfamilie sensorisch getragen wurde:

Sehen:
  form_flow
  form_stability
  form_change

Hoeren:
  energy_tone
  energy_shift

Fuehlen:
  mcm_coherence
  mcm_tension
  mcm_asymmetry
```

Zusaetzliche passive Spuren:

```text
visual_mcm_alignment_trace:
  Wie nah sichtbare Formbewegung und MCM-Asymmetrie zusammenlagen.

tone_tension_resonance_trace:
  Wie nah Marktton und MCM-Spannung zusammenlagen.
```

Befund Drift-Welt:

```text
dio_1ytj:
  executed: 3
  reward: 3.4434
  visual_mcm_alignment_trace: 0.9805
  tone_tension_resonance_trace: 0.8703

dio_1fqy:
  executed: 2
  observed: 2
  reward: 3.1099
  visual_mcm_alignment_trace: 0.9269
  tone_tension_resonance_trace: 0.9576

dio_0lt6:
  executed: 1
  reward: -0.2495
  visual_mcm_alignment_trace: 0.8893
  tone_tension_resonance_trace: 0.5367
```

Lesart:

```text
Der negative Kontakt war kein Beweis fuer Feldkollaps.
Er war eine lokale schwache Ton/Spannungs-Kopplung bei realem Kontakt.

Die tragenden Familien zeigen dagegen eine staerkere gemeinsame Spur aus
Sehen, Hoeren und Fuehlen.
```

Wichtig:

```text
Diese Werte sind Diagnose.
Sie sind keine neue Entry-Regel und kein Gate.
```

Gegenpruefung ueber mehrere Mini-Welten:

```text
sensorischer_shift:
  dio_1lam
    executed: 4
    reward: 5.1978
    visual_mcm_alignment_trace: 0.9957
    tone_tension_resonance_trace: 0.9706

order_shift:
  dio_1d6j
    executed: 1
    observed: 3
    reward: 1.1438
    visual_mcm_alignment_trace: 0.9950
    tone_tension_resonance_trace: 0.9424

order_shift_varianz:
  dio_1d6j
    executed: 4
    reward: 3.6243
    visual_mcm_alignment_trace: 0.9888
    tone_tension_resonance_trace: 0.9886

order_shift_drift:
  dio_1ytj
    executed: 3
    reward: 3.4434
    visual_mcm_alignment_trace: 0.9805
    tone_tension_resonance_trace: 0.8703
```

Belastete Gegenbeispiele:

```text
order_shift:
  dio_00eh
    executed: 1
    observed: 1
    reward: -0.4311
    visual_mcm_alignment_trace: 0.8878
    tone_tension_resonance_trace: 0.6646

order_shift_drift:
  dio_0lt6
    executed: 1
    reward: -0.2495
    visual_mcm_alignment_trace: 0.8893
    tone_tension_resonance_trace: 0.5367
```

Lesart:

```text
Tragende Familien zeigen haeufig eine gemeinsame Spur aus Form/MCM-Kopplung
und Ton/Spannungs-Resonanz.

Aber hohe Sensorikspur allein wird nicht als Trade-Regel verwendet.
Erst Konsequenz, Wiederkehr und Familienreife zeigen, ob daraus tragende
Handlungsnaehe entstehen kann.
```

## Weltuebergreifende Sensorik-Reife

Werkzeug:

```text
python -m DIO_MINI.analyze_cross_world_sensor_maturity --phase shift:debug\dio_mini_shift_followup\sensorischer_shift --phase order_shift:debug\dio_mini_order_shift\order_shift --phase order_shift_varianz:debug\dio_mini_order_shift_varianz\order_shift_varianz --phase order_shift_drift:debug\dio_mini_order_shift_drift\order_shift_drift --output-dir debug\dio_mini_cross_world_sensor_maturity_v1
```

Erzeugt:

```text
dio_mini_cross_world_sensor_maturity_phase_rows.csv
dio_mini_cross_world_sensor_maturity_world_summary.csv
```

Befund:

```text
dio_1d6j:
  phases: 2
  executed: 5
  observed: 3
  reward: 4.7681
  avg_visual_mcm_alignment_trace: 0.9919
  avg_tone_tension_resonance_trace: 0.9655

dio_1ytj:
  phases: 2
  executed: 3
  observed: 2
  reward: 3.4434
  avg_visual_mcm_alignment_trace: 0.9913
  avg_tone_tension_resonance_trace: 0.8674
```

Lesart:

```text
Die Sensorik bestaetigt die Familienpersistenz.

dio_1d6j ist aktuell die sauberste weltuebergreifende Reifespur:
Form/MCM und Ton/Spannung liegen beide eng zusammen.

dio_1ytj ist ebenfalls weltuebergreifend, wirkt aber tonal/spannungsseitig
noch unruhiger. Das passt zur Persistenzdiagnose als Spur mit rohem Druckanteil.
```

Naechster Schritt:

```text
Diese Diagnose nicht in Motorik rueckfuehren.
Zuerst weitere kontrollierte Welten bauen und pruefen,
ob dieselben oder verwandte Familien unter neuer sensorischer Varianz
weiter auftauchen.
```

## Resonanz-Welt als weiterer Gegenlauf

Kontrollierter Datensatz:

```text
data/kontrolliert_reihenfolge_shift_resonanz_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Eine weitere kleine Welt mit zwei Episoden, aber anderer Reihenfolge,
anderer Amplitude und anderem Ton-/Volumenprofil.

Die Pruefung ist nicht:
Kann DIO eine bekannte Strecke auswendig handeln?

Sondern:
Welche eigene DIO-Syntax bleibt unter veraenderter Sensorik wiedererkennbar,
welche lokale Syntax entsteht neu, und welche Familien reifen erst durch
den neuen Kontakt?
```

Start:

```text
Memory-Basis:
bot_memory\dio_mini_order_shift_drift_memory.json

Neue Resonanz-Memory:
bot_memory\dio_mini_order_shift_resonanz_memory.json
```

Test:

```text
python -m DIO_MINI.run_transfer --phase order_shift_resonanz:data\kontrolliert_reihenfolge_shift_resonanz_2episoden_5m_SOLUSDT.csv:4 --debug-root debug\dio_mini_order_shift_resonanz --memory bot_memory\dio_mini_order_shift_resonanz_memory.json
```

Befund:

```text
Lauf 48: 1 Trade, Reward 1.7624
Lauf 49: 1 Trade, Reward 1.7624
Lauf 50: 3 Trades, Reward 3.8029
Lauf 51: 3 Trades, Reward 3.7561
```

Kontaktqualitaet:

```text
positive_executed_contact:
  count: 8
  avg_reward: 1.3855
  max_reward: 1.7624

observed_potential:
  count: 33

burdened_executed_contact:
  count: 0
```

Wichtige Familien:

```text
dio_1iuo:
  transition: persistent_execution in der Resonanz-Welt
  executed_runs: 2
  reward: 3.5248
  visual_mcm_alignment_trace: 0.9456
  tone_tension_resonance_trace: 0.9328

dio_0pw5:
  transition: observation_to_execution
  executed_runs: 2
  observed_runs: 2
  reward: 2.7076
  visual_mcm_alignment_trace: 0.9457
  tone_tension_resonance_trace: 0.9598

dio_1r42:
  transition: observation_to_execution
  executed_runs: 2
  observed_runs: 2
  reward: 2.4212
  visual_mcm_alignment_trace: 0.9966
  tone_tension_resonance_trace: 0.9229
```

Lesart:

```text
Die Resonanz-Welt erzeugt keine Belastungstrades.
Sie zeigt eine neue reife lokale Ausfuehrung und mehrere Beobachtung-zu-
Handlung-Uebergaenge.

Wichtig ist dio_1iuo:
Diese Familie war in einer frueheren Welt bereits als Beobachtung sichtbar
und wird in der Resonanz-Welt handlungsnah.
```

## Cross-World-Persistenz mit Resonanz

Werkzeug:

```text
python -m DIO_MINI.analyze_cross_world_persistence --phase shift:debug\dio_mini_shift_followup\sensorischer_shift --phase order_shift:debug\dio_mini_order_shift\order_shift --phase order_shift_varianz:debug\dio_mini_order_shift_varianz\order_shift_varianz --phase order_shift_drift:debug\dio_mini_order_shift_drift\order_shift_drift --phase order_shift_resonanz:debug\dio_mini_order_shift_resonanz\order_shift_resonanz --output-dir debug\dio_mini_cross_world_persistence_v3
```

Weltuebergreifende Familien:

```text
dio_1d6j:
  phases: 2
  executed: 5
  observed: 3
  reward: 4.7681
  visual_mcm: 0.9919
  tone_tension: 0.9655

dio_1ytj:
  phases: 2
  executed: 3
  observed: 2
  reward: 3.4434
  visual_mcm: 0.9913
  tone_tension: 0.8674

dio_1iuo:
  phases: 2
  executed: 2
  observed: 2
  reward: 3.5248
  visual_mcm: 0.9539
  tone_tension: 0.9405
```

Lesart:

```text
Nach der Resonanz-Welt sind drei weltuebergreifende Spuren sichtbar:

dio_1d6j:
  bisher sauberste Reifespur.

dio_1ytj:
  tragend, aber tonal/spannungsseitig rauer.

dio_1iuo:
  vorher beobachtet, spaeter handlungsnah.
```

Fachlich:

```text
Das ist weiterhin kein Entry-System.
Es ist der Nachweis, dass DIO_MINI eigene Syntaxspuren unter veraenderter
Sensorik wiederfinden, liegen lassen oder in Handlung bringen kann.
```

## Sensorisch verwandte Familien

Werkzeug:

```text
python -m DIO_MINI.analyze_sensor_family_relations --sensor-csv debug\dio_mini_cross_world_sensor_maturity_v2\dio_mini_cross_world_sensor_maturity_phase_rows.csv --output-dir debug\dio_mini_cross_world_sensor_relations_v1 --min-relation-trace 0.82
```

Zweck:

```text
Nicht nur gleiche `dio_...` Namen vergleichen.

DIO kann unter Varianz eine andere eigene Bezeichnung bilden, obwohl die
sensorische Spur verwandt ist.

Deshalb wird geprueft:
Welche Familien haben aehnliche Sehen/Hoeren/Fuehlen-Vektoren,
obwohl sie unterschiedlich benannt sind?
```

Befund gleiche Familie ueber Phasen:

```text
dio_1ytj <-> dio_1ytj
  phases: order_shift_varianz / order_shift_drift
  relation_kind: same_family_cross_phase
  sensor_relation_trace: 0.9837
  reward: 0.0000 / 3.4434

dio_1iuo <-> dio_1iuo
  phases: order_shift_drift / order_shift_resonanz
  relation_kind: same_family_cross_phase
  sensor_relation_trace: 0.9808
  reward: 0.0000 / 3.5248

dio_1d6j <-> dio_1d6j
  phases: order_shift / order_shift_varianz
  relation_kind: same_family_cross_phase
  sensor_relation_trace: 0.9729
  reward: 1.1438 / 3.6243
```

Befund verwandte Familien trotz anderer Namen:

```text
dio_121e <-> dio_0pw5
  relation_kind: bearing_sensor_neighbor
  sensor_relation_trace: 0.9904
  reward: 3.0424 / 2.7076

dio_121e <-> dio_1fqy
  relation_kind: bearing_sensor_neighbor
  sensor_relation_trace: 0.9903
  reward: 3.0424 / 3.1099

dio_1fqy <-> dio_0pw5
  relation_kind: bearing_sensor_neighbor
  sensor_relation_trace: 0.9825
  reward: 3.1099 / 2.7076
```

Lesart:

```text
Das ist der erste saubere Hinweis auf sensorische Verwandtschaft:

Die genaue DIO-Syntax kann variieren,
aber darunter koennen aehnliche Sehen/Hoeren/Fuehlen-Spuren liegen.
```

Wichtig:

```text
Auch diese Relation ist passiv.
Sie darf nicht automatisch handeln lassen.
Sie dient spaeter dazu, Erinnerung nicht nur exakt,
sondern ueber verwandte Sinnesfamilien zu verdichten.
```

## Passive Speicherung sensorischer Relationen

Erweiterung:

```text
DIO_MINI.store_sensor_relations
SemanticMemory.sensor_relations
```

Zweck:

```text
Sensorische Familienverwandtschaft wird im Mini-Gedaechtnis gespeichert,
aber nicht von action_diagnostics, action_bias oder action_readiness gelesen.
```

Beispiel:

```text
order_shift_varianz:dio_1ytj <-> order_shift_drift:dio_1ytj
  relation_kind: same_family_cross_phase
  trace: 0.9837

order_shift:dio_121e <-> order_shift_resonanz:dio_0pw5
  relation_kind: bearing_sensor_neighbor
  trace: 0.9904
```

Passivitaetspruefung:

```text
Memory mit sensor_relations:
  3 Trades
  Reward 3.142792
  Long: 1
  Short: 2

Memory ohne sensor_relations:
  3 Trades
  Reward 3.142792
  Long: 1
  Short: 2
```

Befund:

```text
Die sensorischen Relationen veraendern die Handlung nicht.
Sie sind aktuell reine Erinnerungs- und Diagnosekarten.
```

## Sensor-Relation-Probe

Kontrollierter Datensatz:

```text
data/kontrolliert_sensor_relation_probe_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Pruefen, ob sensorisch verwandte Familien unter einer neuen kleinen Welt
wieder als Beobachtung oder Handlung sichtbar werden.

Die gespeicherten sensor_relations bleiben dabei passiv.
```

Start:

```text
Memory-Basis:
bot_memory\dio_mini_order_shift_resonanz_memory.json

Neue Probe-Memory:
bot_memory\dio_mini_sensor_relation_probe_memory.json
```

Test:

```text
python -m DIO_MINI.run_transfer --phase sensor_relation_probe:data\kontrolliert_sensor_relation_probe_2episoden_5m_SOLUSDT.csv:4 --debug-root debug\dio_mini_sensor_relation_probe --memory bot_memory\dio_mini_sensor_relation_probe_memory.json
```

Befund:

```text
Lauf 52: 2 Trades, Reward 1.1516
Lauf 53: 2 Trades, Reward 1.1516
Lauf 54: 2 Trades, Reward 2.4407
Lauf 55: 4 Trades, Reward 2.8761
```

Kontaktqualitaet:

```text
positive_executed_contact:
  count: 10
  avg_reward: 0.7620
  max_reward: 1.3555

burdened_executed_contact:
  count: 0

held_same_episode_contact:
  count: 2
```

Wichtige Familien:

```text
dio_0n4c:
  transition: persistent_execution
  executed_runs: 4
  reward: 4.3409
  visual_mcm_alignment_trace: 0.9501
  tone_tension_resonance_trace: 0.9755

dio_1hkr:
  transition: persistent_execution
  executed_runs: 3
  reward: 0.1990
  visual_mcm_alignment_trace: 0.9446
  tone_tension_resonance_trace: 0.7876

dio_0ga4:
  transition: observation_to_execution
  executed_runs: 1
  observed_runs: 2
  reward: 1.3555
```

Lesart:

```text
Die Probe-Welt ist positiv, aber nicht jede Ausfuehrung ist gleich tragend.

dio_0n4c zeigt eine starke lokale Reifespur.
dio_1hkr zeigt, dass Ausfuehrung allein nicht ausreicht:
Die Konsequenz ist nur schwach positiv und die Ton/Spannungs-Resonanz
ist deutlich flacher.
```

## Sensorische Nachbarschaften nach Probe

Werkzeug:

```text
python -m DIO_MINI.analyze_sensor_family_relations --sensor-csv debug\dio_mini_cross_world_sensor_maturity_v3\dio_mini_cross_world_sensor_maturity_phase_rows.csv --output-dir debug\dio_mini_cross_world_sensor_relations_v2 --min-relation-trace 0.82
```

Befund:

```text
dio_0pw5 <-> dio_0n4c
  relation_kind: bearing_sensor_neighbor
  sensor_relation_trace: 0.9845
  reward: 2.7076 / 4.3409

dio_1ioc <-> dio_0n4c
  relation_kind: bearing_sensor_neighbor
  sensor_relation_trace: 0.9821
  reward: 3.3397 / 4.3409

dio_121e <-> dio_0n4c
  relation_kind: bearing_sensor_neighbor
  sensor_relation_trace: 0.9784
  reward: 3.0424 / 4.3409

dio_1hkr <-> dio_1hkr
  relation_kind: same_family_cross_phase
  sensor_relation_trace: 0.9846
  reward: 0.0000 / 0.1990
```

Lesart:

```text
dio_0n4c ist eine neue lokale Familie, aber sensorisch nah an frueher
tragenden Familien.

dio_1hkr ist gleiche Familie ueber Phasen, aber noch keine starke
tragende Konsequenzspur.
```

Fachlich:

```text
Das zeigt zwei verschiedene Arten von Wiederkehr:

1. Verwandte Sensorik mit anderem Namen und guter Konsequenz.
2. Gleicher Name ueber Phasen, aber nur schwache Konsequenz.

DIO_MINI darf beides speichern, aber nicht automatisch daraus handeln.
```

## Kompakte Reifekarte

Werkzeug:

```text
python -m DIO_MINI.build_family_maturity_map --persistence-csv debug\dio_mini_cross_world_persistence_v4\dio_mini_cross_world_persistence_world_summary.csv --sensor-csv debug\dio_mini_cross_world_sensor_maturity_v3\dio_mini_cross_world_sensor_maturity_world_summary.csv --relations-csv debug\dio_mini_cross_world_sensor_relations_v2\dio_mini_sensor_family_relations.csv --output-dir debug\dio_mini_family_maturity_map_v1
```

Erzeugt:

```text
dio_mini_family_maturity_map.csv
dio_mini_family_maturity_map.json
```

Zweck:

```text
Persistenz, Konsequenz, Sensorik und sensorische Nachbarschaft in einer
kompakten passiven Karte zusammenfuehren.
```

Befund:

```text
dio_1d6j:
  weltuebergreifend
  ausgefuehrt
  beobachtet
  positive Konsequenz
  sensorische Nachbarn
  gleiche Familie ueber Phasen
  reward: 4.7681

dio_1iuo:
  weltuebergreifend
  ausgefuehrt
  beobachtet
  positive Konsequenz
  sensorische Nachbarn
  gleiche Familie ueber Phasen
  reward: 3.5248

dio_1ytj:
  weltuebergreifend
  ausgefuehrt
  beobachtet
  Nachhall gehalten
  positive Konsequenz
  reward: 3.4434

dio_1hkr:
  weltuebergreifend
  ausgefuehrt
  beobachtet
  Nachhall gehalten
  positive Konsequenz, aber schwach
  reward: 0.1990

dio_0n4c:
  lokale starke Ausfuehrung
  positive Konsequenz
  sensorische Nachbarn
  reward: 4.3409
```

Lesart:

```text
Die Reifekarte trennt:

1. stabile weltuebergreifende Reifespur,
2. weltuebergreifende Spur mit Nachhall,
3. starke lokale Sensorikspur,
4. schwache Ausfuehrung trotz gleicher Familie.
```

Wichtig:

```text
Auch diese Karte ist passiv.
Sie beschreibt DIOs innere Entwicklung,
aber sie ist keine Entry-Liste und kein Gate.
```

## Sensor-Relation-Probe 2

Kontrollierter Datensatz:

```text
data/kontrolliert_sensor_relation_probe2_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Weitere kleine Welt mit anderer Amplitude und Zwischenrauschen.
Die Reifekarte wird gestresst, ohne Motorik oder Regeln zu veraendern.
```

Start:

```text
Memory-Basis:
bot_memory\dio_mini_sensor_relation_probe_memory.json

Neue Probe2-Memory:
bot_memory\dio_mini_sensor_relation_probe2_memory.json
```

Befund:

```text
Lauf 56: 1 Trade, Reward 1.5903
Lauf 57: 1 Trade, Reward 1.5903
Lauf 58: 3 Trades, Reward 4.0630
Lauf 59: 3 Trades, Reward 3.0022
```

Kontaktqualitaet:

```text
positive_executed_contact:
  count: 8
  avg_reward: 1.2807
  max_reward: 1.5903

burdened_executed_contact:
  count: 0
```

Wichtige Familien:

```text
dio_0nmi:
  transition: persistent_execution in Probe2
  executed_runs: 3
  reward: 4.7710
  visual_mcm_alignment_trace: 0.9743
  tone_tension_resonance_trace: 0.9239

dio_1uyk:
  transition: observation_to_execution
  executed_runs: 2
  observed_runs: 2
  reward: 2.4699
  tone_tension_resonance_trace: 0.9952

dio_060l:
  transition: observation_to_execution
  executed_runs: 1
  observed_runs: 3
  reward: 1.1907
```

Cross-World-Befund nach Probe2:

```text
dio_0nmi:
  phases: order_shift, sensor_relation_probe2
  executed_runs: 4
  observed_runs: 1
  reward_sum: 6.7710
  visual_mcm: 0.9740
  tone_tension: 0.9315

dio_1d6j:
  phases: order_shift, order_shift_varianz
  reward_sum: 4.7681

dio_1iuo:
  phases: order_shift_drift, order_shift_resonanz
  reward_sum: 3.5248
```

Aktuelle Reifekarte:

```text
dio_0nmi:
  staerkste weltuebergreifende Reifespur
  reward: 6.7710
  sensorische Nachbarn: 8
  gleiche Familie ueber Phasen

dio_1d6j:
  stabile weltuebergreifende Reifespur
  reward: 4.7681
  sensorische Nachbarn: 8

dio_1iuo:
  beobachtet und spaeter handlungsnah
  reward: 3.5248

dio_1ytj:
  tragend, aber mit Nachhall
  reward: 3.4434

dio_1hkr:
  gleiche Familie ueber Phasen,
  aber nur schwache Konsequenz
  reward: 0.1990
```

Lesart:

```text
Probe2 bestaetigt:

Eine Familie kann in einer frueheren Welt kurz auftauchen,
spaeter unter anderer Sensorik wieder erscheinen
und dann staerker tragen.

Das ist keine Strategie-Regel.
Es ist episodische Reifung ueber eigene Syntax, Sensorik und Konsequenz.
```

## Maturity Diagnosis

Werkzeug:

```text
python -m DIO_MINI.summarize_maturity_map --maturity-map debug\dio_mini_family_maturity_map_v2\dio_mini_family_maturity_map.csv --output-dir debug\dio_mini_maturity_diagnosis_v1
```

Erzeugt:

```text
dio_mini_maturity_diagnosis.csv
dio_mini_maturity_diagnosis.json
dio_mini_maturity_diagnosis_overview.json
dio_mini_maturity_diagnosis.md
```

Zweck:

```text
Die Reifekarte menschlich lesbar zusammenfassen.
Keine Handlung.
Keine Regel.
Nur Entwicklungsdiagnose.
```

Aktuelle Klassen:

```text
stabile_reifespur:
  3 Spuren
  Reward 15.0638
  dio_0nmi, dio_1d6j, dio_1iuo

starke_lokale_sensorikspur:
  8 Spuren
  Reward 26.6293
  dio_1lam, dio_0n4c, dio_1ioc, dio_1fqy, dio_121e

reifespur_mit_nachhall:
  2 Spuren
  Reward 3.6424
  dio_1ytj, dio_1hkr

stabile_beobachtung:
  57 Spuren

beobachteter_nachhall:
  4 Spuren

belastete_spur:
  negative Konsequenzspuren
```

Lesart:

```text
DIO_MINI kann aktuell nicht nur Trade/kein Trade zeigen.

Die Diagnose trennt:

1. gereifte wiederkehrende Sprache,
2. starke lokale Sensorik,
3. Nachhall und rohen Druck,
4. reine Beobachtung,
5. belastete Konsequenz.
```

## Speicherhygiene fuer passive Relationen

Erweiterung:

```text
SemanticMemory.compact_sensor_relations
DIO_MINI.compact_memory
```

Zweck:

```text
Passive sensor_relations duerfen wachsen,
aber sie sollen DIOs Mini-Gedaechtnis nicht ueberladen.

Verdichtet wird nur die passive Relationsebene.
Symbole, Familien, Aktionsstatistik und Konsequenzspuren bleiben erhalten.
```

Rangfolge der Verdichtung:

```text
1. gleiche Familie ueber Phasen
2. tragende sensorische Nachbarn
3. hohe sensor_relation_trace
4. mehr ausgefuehrte Kontakte
5. mehr positive Konsequenz
```

Test auf Kopie:

```text
Vorher:
  sensor_relations: 128
  Speicher: 660799 Bytes

Nachher:
  sensor_relations: 64
  Speicher: 619543 Bytes

Entfernt:
  64 passive Relationen
```

Passivitaetspruefung:

```text
Unkompaktierte Memory:
  3 Trades
  Reward 3.002186
  Long: 1
  Short: 2

Kompaktierte Memory:
  3 Trades
  Reward 3.002186
  Long: 1
  Short: 2
```

Befund:

```text
Die Kompaktierung veraendert die Handlung nicht.
Sie reduziert nur passive Relationseintraege.
```

Aktueller Stand:

```text
bot_memory\dio_mini_sensor_relation_probe2_memory.json
  sensor_relations: 64
  symbols: 159
  families: 159
  relations: 44
  Speicher: 619543 Bytes
```

## Sensor-Relation-Probe 3

Kontrollierter Datensatz:

```text
data/kontrolliert_sensor_relation_probe3_2episoden_5m_SOLUSDT.csv
```

Ausgang:

```text
Memory-Basis:
bot_memory\dio_mini_sensor_relation_probe2_memory.json

Neue Probe3-Memory:
bot_memory\dio_mini_sensor_relation_probe3_memory.json
```

Laufbild:

```text
Lauf 60:
  Trades: 2
  Reward: 2.5331
  Symbols: 10

Lauf 61:
  Trades: 2
  Reward: 2.5331
  Symbols: 10

Lauf 62:
  Trades: 3
  Reward: 4.1213
  Symbols: 7

Lauf 63:
  Trades: 3
  Reward: 3.6832
  Symbols: 7
```

Befund:

```text
Probe3 bestaetigt die passive Relationsspur weiter.

DIO_MINI handelt nicht aus einer Regel heraus.
Es tauchen wiederkehrende Familien auf, die ueber verschiedene
kontrollierte Welten Sensorik, MCM-Lage und Konsequenz zusammen tragen.
```

Wichtige lokale Spuren:

```text
dio_1k0r:
  transition: persistent_execution
  runs: 3
  executed: 3
  reward: 4.7844
  visual_mcm_alignment_trace: 0.9632
  tone_tension_resonance_trace: 0.9276

dio_1mx6:
  transition: observation_to_execution
  runs: 4
  executed: 2
  observed: 2
  reward: 2.5728
  visual_mcm_alignment_trace: 0.9271
  tone_tension_resonance_trace: 0.9847

dio_1dmh:
  transition: observation_to_execution
  reward: 2.4802
  visual_mcm_alignment_trace: 0.8605
```

Kontaktbild:

```text
positive_executed_contact:
  count: 10
  avg_reward: 1.2871
  max_reward: 1.5948

observed_potential:
  count: 24
```

## Cross-World-Reife nach Probe3

Neue Cross-World-Befunde:

```text
dio_0nmi:
  phases: 2
  executed: 4
  observed: 1
  reward: 6.7710
  visual_mcm_alignment_trace: 0.9740
  tone_tension_resonance_trace: 0.9315

dio_1k0r:
  phases: 2
  executed: 3
  observed: 2
  reward: 4.7844
  visual_mcm_alignment_trace: 0.9625
  tone_tension_resonance_trace: 0.9303

dio_1d6j:
  phases: 2
  executed: 5
  observed: 3
  reward: 4.7681
  visual_mcm_alignment_trace: 0.9919
  tone_tension_resonance_trace: 0.9655

dio_1iuo:
  phases: 2
  reward: 3.5248

dio_1ytj:
  phases: 2
  reward: 3.4434
  Reifung mit Nachhall
```

Aktuelle Reifekarte nach Probe3:

```text
stabile_reifespur:
  dio_0nmi
  dio_1k0r
  dio_1d6j
  dio_1iuo

reifespur_mit_nachhall:
  dio_1ytj
  dio_1hkr
```

Lesart:

```text
dio_1k0r ist neu in die stabile Reifespur gerutscht.
Das ist kein Motoriksignal.
Es ist ein Nachweis, dass eine Familie ueber Weltvariation hinweg
sensorisch und konsequenzbezogen tragfaehig wiederkehrt.
```

## Speicherstand nach Probe3

Kompaktierung:

```text
bot_memory\dio_mini_sensor_relation_probe3_memory.json

Vorher:
  sensor_relations: 97
  Speicher: 679088 Bytes

Nachher:
  sensor_relations: 64
  Speicher: 657194 Bytes

Entfernt:
  33 passive Relationen
```

Aktueller Stand:

```text
symbols: 169
families: 169
relations: 44
sensor_relations: 64
```

Befund:

```text
Die passive Relationsschicht bleibt begrenzt.
Die Verdichtung betrifft nur sensorische Nachbarschaften.
Die episodische Erfahrung, Familien und Konsequenzspuren bleiben erhalten.
```

## Passive Speicherwachstumsdiagnose

Werkzeug:

```text
python -m DIO_MINI.analyze_memory_growth
```

Zweck:

```text
Pruefen, ob Symbol- und Familienwachstum echte episodische Entwicklung ist
oder nur Speicherballast.

Das Werkzeug veraendert die Memory nicht.
Es schreibt nur Diagnose:

debug\dio_mini_memory_growth_probe3
```

Probe3 gegen Probe2:

```text
Memory:
bot_memory\dio_mini_sensor_relation_probe3_memory.json

Vorherige Memory:
bot_memory\dio_mini_sensor_relation_probe2_memory.json
```

Ergebnis:

```text
symbols: 169
families: 169
relations: 44
sensor_relations: 64

new_families_since_previous: 10
compact_candidate_count: 0

executed_positive_trace:
  166 Familien
  Reward 346.054872
  davon neu: 10

repeated_quiet_trace:
  3 Familien
  Reward 0.0

burden_traces:
  keine
```

Befund:

```text
Eine Familien-Kompaktierung ist an dieser Stelle nicht sinnvoll.

Die neuen Familien sind nicht leer.
Sie tragen positive Ausfuehrungsspuren oder wiederholte ruhige Spuren.

Fachliche Grenze:
Familien duerfen nicht geloescht werden, nur weil sie neu oder klein sind.
Geloescht oder verdichtet wird erst, wenn eine Spur ueber mehrere Welten
keine Beobachtung, keine Handlung und keine Konsequenzbindung mehr traegt.
```

## Sensor-Relation-Probe 4

Kontrollierter Datensatz:

```text
data/kontrolliert_sensor_relation_probe4_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Weitere kleine Welt mit gleicher Grundstruktur,
aber anderer Reihenfolge, gedaempfterem Volumenimpuls
und verschobener Gegenbewegung.

Ziel:
Wiedererkennung ohne mechanisch identische Wiederholung pruefen.
```

Transfer mit bestehender Probe3-Memory:

```text
Memory-Basis:
bot_memory\dio_mini_sensor_relation_probe3_memory.json

Neue Memory:
bot_memory\dio_mini_sensor_relation_probe4_memory.json
```

Laufbild:

```text
Lauf 64:
  Trades: 1
  Reward: 1.1411
  Symbols: 17

Lauf 65:
  Trades: 1
  Reward: 1.1411
  Symbols: 17

Lauf 66:
  Trades: 2
  Reward: 1.7153
  Symbols: 13

Lauf 67:
  Trades: 3
  Reward: 2.4975
  Symbols: 7
```

Befund:

```text
Probe4 zeigt wieder gestufte Oeffnung:
erst vorsichtig, dann mehr Handlung bei weniger neuer Syntax.

Das ist kein harter Beweis fuer Intelligenz.
Es ist aber ein sauberer Hinweis, dass die Mini-Struktur
mit vorhandener Erfahrung eine neue kleine Welt zunehmend verdichtet.
```

Lokale Probe4-Spuren:

```text
dio_0v36:
  persistent_execution
  executed_runs: 3
  reward: 3.4232
  visual_mcm_alignment_trace: 0.9661
  tone_tension_resonance_trace: 0.9466

dio_0a54:
  observation_to_execution
  executed_runs: 2
  observed_runs: 2
  reward: 1.1484
  gleiche Familie in Probe3 und Probe4 sichtbar

dio_0nm2:
  observation_to_execution
  reward: 1.0241

dio_14wi:
  observation_to_execution
  reward: 0.8992
```

Cross-World-Reife nach Probe4:

```text
stabile_reifespur:
  dio_0nmi
  dio_1d6j

starke_lokale_sensorikspur:
  dio_1k0r
  dio_0v36
  dio_1ioc
  dio_121e
  dio_1mx6
  dio_1uyk

positive_einzelspur:
  12 Spuren

stabile_beobachtung:
  46 Spuren

beobachteter_nachhall:
  4 Spuren

belastete_spur:
  1 alte Spur
```

Lesart:

```text
Nach Probe4 sind dio_0nmi und dio_1d6j die robustesten
weltuebergreifenden Reifespuren.

dio_1k0r bleibt positiv und sensorisch stark,
wird aber nach dieser Auswertung wieder als lokale Sensorikspur gelesen,
weil die aktuelle Cross-World-Auswahl es nicht ueber mehrere Phasen traegt.

dio_0a54 ist wichtig:
Die gleiche Familie taucht in Probe3 und Probe4 auf und wandert
von Beobachtung zu Handlung.
```

Speicherstand nach Probe4:

```text
bot_memory\dio_mini_sensor_relation_probe4_memory.json

runs: 67
symbols: 184
families: 184
relations: 44
sensor_relations: 64
Speicher: 713794 Bytes
```

Korrektur Speicherhygiene:

```text
DIO_MINI.store_sensor_relations setzt jetzt memory.max_sensor_relations
auf den uebergebenen Wert.

Damit gilt --max-relations 64 nicht nur beim Lesen der Relationsdatei,
sondern auch beim anschliessenden Speichern der Memory.
```

## Probe4-Wiederholungsprobe

Datensatz:

```text
data/kontrolliert_sensor_relation_probe4_2episoden_5m_SOLUSDT.csv
```

Ausgang:

```text
Memory-Basis:
bot_memory\dio_mini_sensor_relation_probe4_memory.json

Neue Repeat-Memory:
bot_memory\dio_mini_sensor_relation_probe4_repeat_memory.json
```

Laufbild:

```text
Lauf 68:
  Trades: 3
  Reward: 2.0002
  Symbols: 6

Lauf 69:
  Trades: 3
  Reward: 2.0002
  Symbols: 6

Lauf 70:
  Trades: 3
  Reward: 2.0002
  Symbols: 6

Lauf 71:
  Trades: 3
  Reward: 2.0002
  Symbols: 6
```

Befund:

```text
Die Wiederholungsprobe erzeugt keine neuen Familien.
Die Symbolzahl bleibt konstant niedrig.
Die Handlung bleibt stabil.
```

Speicherwachstum:

```text
new_families_since_previous: 0
compact_candidate_count: 0
burden_traces: keine

symbols: 184
families: 184
relations: 44
sensor_relations: 64
```

Wichtige Repeat-Spuren:

```text
dio_14wi:
  persistent_execution
  reward: 3.5968
  visual_mcm_alignment_trace: 0.9524
  tone_tension_resonance_trace: 0.9925

dio_0a54:
  persistent_execution
  reward: 2.2969

dio_1alf:
  persistent_execution
  reward: 2.1073
```

Neue Reifekarte nach Repeat:

```text
stabile_reifespur:
  dio_0nmi
  dio_1d6j
  dio_14wi
  dio_0a54

starke_lokale_sensorikspur:
  dio_1k0r
  dio_0v36
  dio_1ioc
  dio_121e
  dio_1mx6
  dio_1dmh
  dio_1uyk
```

Lesart:

```text
dio_0a54 ist der wichtigste neue Befund:

Probe3:
  beobachtet

Probe4:
  Beobachtung -> Handlung

Probe4-Repeat:
  persistente Handlung

Das ist eine saubere episodische Reifespur.
Nicht als Regel, sondern als dokumentierte Entwicklung der eigenen Syntax.
```

## Sensor-Relation-Probe 5

Kontrollierter Datensatz:

```text
data/kontrolliert_sensor_relation_probe5_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Kleine Variation von Probe4:
frueherer Impuls,
flacherer erster Ruecklauf,
staerkerer zweiter Druck.

Die Welt ist nah genug fuer Uebertragung,
aber nicht identisch.
```

Transfer mit Probe4-Repeat-Memory:

```text
Memory-Basis:
bot_memory\dio_mini_sensor_relation_probe4_repeat_memory.json

Neue Memory:
bot_memory\dio_mini_sensor_relation_probe5_memory.json
```

Laufbild:

```text
Lauf 72:
  Trades: 1
  Reward: 0.6056
  Symbols: 14

Lauf 73:
  Trades: 1
  Reward: 0.6056
  Symbols: 14

Lauf 74:
  Trades: 2
  Reward: 1.7905
  Symbols: 11

Lauf 75:
  Trades: 3
  Reward: 2.5890
  Symbols: 7
```

Befund:

```text
Probe5 bleibt positiv,
aber DIO_MINI uebertraegt nicht einfach die gleichen Familien.

dio_0a54 und dio_14wi bleiben in der Reifekarte stabil,
werden in Probe5 aber nicht direkt weiter als Hauptfamilie gehandelt.

Stattdessen bildet Probe5 neue lokale Sprache.
Das ist fachlich plausibel:
Variation fuehrt nicht zu mechanischer Wiederholung,
sondern zu neuer Syntax mit Bezug zur vorhandenen Reifekarte.
```

Lokale Probe5-Spuren:

```text
dio_0qb3:
  persistent_execution
  reward: 2.4226
  visual_mcm_alignment_trace: 0.9737
  tone_tension_resonance_trace: 0.9808

dio_1vm7:
  observation_to_execution
  reward: 2.3697

dio_0x52:
  observation_to_execution
  reward: 0.7986
```

Cross-World nach Probe5:

```text
stabile_reifespur:
  dio_0nmi
  dio_1d6j
  dio_14wi
  dio_0a54

entwickelnde_reifespur:
  dio_0qb3
  dio_1alf
  dio_01yf

starke_lokale_sensorikspur:
  dio_1k0r
  dio_0v36
  dio_1ioc
  dio_121e
  dio_1mx6
  dio_1dmh
  dio_1uyk
  dio_1vm7
```

Diagnosekorrektur:

```text
DIO_MINI.summarize_maturity_map trennt jetzt:

stabile_reifespur:
  mehrfach bestaetigte, starke Reifespur

entwickelnde_reifespur:
  weltuebergreifende positive Spur mit gleicher Familie,
  aber noch nicht stark genug fuer stabile Reifeklasse

positive_einzelspur:
  positive Spur ohne ausreichende Weltuebertragung
```

Speicherstand:

```text
bot_memory\dio_mini_sensor_relation_probe5_memory.json

runs: 75
symbols: 197
families: 197
relations: 44
sensor_relations: 64
Speicher: 762725 Bytes
```

Lesart:

```text
Probe5 zeigt keine starre Strategiewiederholung.
Die Mini-Struktur bleibt organischer:

1. vorhandene Reifespuren bleiben erhalten,
2. neue Weltvariation erzeugt neue lokale Sprache,
3. einzelne neue Familien werden sofort als entwickelnde Reifespur sichtbar,
4. Sensor-Relationen bleiben passiv und begrenzt.
```

## Handlungsnaehe und Uebergang Beobachtung zu Handlung

Werkzeug:

```text
python -m DIO_MINI.analyze_action_transition
```

Zweck:

```text
Lesen, wann eine Familie nur beobachtet wird,
wann sie direkt handelt
und wann sie von Beobachtung zu positiver Handlung uebergeht.

Das Werkzeug ist passiv.
Es veraendert keine Memory und keine Motorik.
```

Probe5:

```text
debug\dio_mini_action_transition_probe5
```

Klassen:

```text
direct_positive_action:
  1 Familie
  Reward: 2.422580
  dio_0qb3

observation_to_positive_action:
  2 Familien
  Reward: 3.168240
  dio_1vm7
  dio_0x52

held_observation:
  11 Familien
```

Wichtige Uebergangsspuren:

```text
dio_1vm7:
  Beobachtung ab Lauf 72
  Handlung ab Lauf 74
  observed_trade_readiness: 0.010571
  executed_trade_readiness: 0.106987
  observed_mature_transfer: 0.010571
  executed_mature_transfer: 0.059405
  reward: 2.369678

dio_0x52:
  Beobachtung ab Lauf 72
  Handlung ab Lauf 75
  observed_trade_readiness: 0.017514
  executed_trade_readiness: 0.067184
  observed_mature_transfer: 0.017514
  executed_mature_transfer: 0.067184
  reward: 0.798562

dio_0qb3:
  direkte positive Handlung ab Lauf 72
  executed_trade_readiness: 0.244881
  executed_mature_transfer: 0.063796
  reward: 2.422580
```

Lesart:

```text
Bei dio_1vm7 und dio_0x52 bleibt die sensorische Signatur stabil.
Der Uebergang entsteht nicht, weil DIO_MINI ploetzlich andere Rohdaten sieht.

Der Uebergang entsteht dadurch, dass Handlungsnaehe und mature_transfer
bei gleicher Signatur steigen.

Das ist fachlich wichtig:
Handlung ist nicht Regelkontakt,
sondern gereifte Naehe zu einer bereits beobachteten Form.
```

Probe4-Repeat als Gegenbild:

```text
debug\dio_mini_action_transition_probe4_repeat

direct_positive_action:
  3 Familien
  Reward: 8.000932
  dio_14wi
  dio_0a54
  dio_1alf

held_observation:
  3 Familien
```

Lesart:

```text
Probe4-Repeat zeigt gereifte direkte Handlung.
Probe5 zeigt wieder Variation:
ein Teil wird direkt gehandelt,
ein Teil reift von Beobachtung zu Handlung,
ein Teil bleibt Beobachtung.
```

## Cross-World-Handlungsnaehe

Werkzeug:

```text
python -m DIO_MINI.analyze_cross_world_action_transition
```

Zweck:

```text
Handlungsnaehe nicht nur lokal lesen,
sondern ueber mehrere kontrollierte Welten zusammenfuehren.

Damit wird sichtbar:

1. welche Familien ueber Welten gereift handeln,
2. welche Familien direkt gereift handeln,
3. welche nur lokal von Beobachtung zu Handlung wechseln,
4. welche gehaltene Beobachtung bleiben,
5. welche belastete Handlungsspuren tragen.
```

Auswertung:

```text
debug\dio_mini_cross_world_action_transition_v1
```

Klassen:

```text
matured_action_pattern:
  5 Familien
  Reward: 22.479495
  dio_0a54
  dio_0nmi
  dio_1d6j
  dio_14wi
  dio_0qb3

direct_mature_pattern:
  2 Familien
  Reward: 3.983890
  dio_1alf
  dio_01yf

local_observation_to_action:
  13 Familien
  Reward: 24.328632

local_direct_action:
  3 Familien
  Reward: 10.207592

held_observation_pattern:
  60 Familien
  Reward: 0.0

burdened_action_pattern:
  1 Familie
  Reward: -0.431148
```

Lesart der Klassen:

```text
matured_action_pattern:
  Familie kommt ueber mehrere Welten vor
  und zeigt sowohl Beobachtung als auch positive Handlung.

direct_mature_pattern:
  Familie kommt ueber mehrere Welten vor
  und handelt positiv, ohne lokale Beobachtung-zu-Handlung-Phase.

local_observation_to_action:
  Familie reift innerhalb einer Welt von Beobachtung zu Handlung.

local_direct_action:
  Familie handelt lokal direkt positiv.

held_observation_pattern:
  Familie wird wiederholt gesehen, aber nicht gehandelt.

burdened_action_pattern:
  Handlung war belastend und bleibt als Konsequenzspur sichtbar.
```

Befund:

```text
DIO_MINI zeigt jetzt ein lesbares Reifeverhalten:

Nicht jede wahrgenommene Familie wird gehandelt.
Ein grosser Anteil bleibt Beobachtung.
Ein kleiner Teil wird lokal handlungsnah.
Ein noch kleinerer Teil wird weltuebergreifend gereifte Handlung.

Das entspricht der Zielrichtung:
Handlung entsteht nicht aus einer harten Regel,
sondern aus wiederkehrender Wahrnehmung, Konsequenz und gereifter Naehe.
```

## DIO-eigene Handlungs-Trace-Sprache

Neue Leseschicht:

```text
python -m DIO_MINI.build_action_trace_language --world-summary debug\dio_mini_cross_world_action_transition_v1\dio_mini_cross_world_action_transition_world_summary.csv --output-dir debug\dio_mini_action_trace_language_v1
```

Ausgabe:

```text
debug\dio_mini_action_trace_language_v1\dio_mini_action_trace_language.md
debug\dio_mini_action_trace_language_v1\dio_mini_action_trace_language.csv
debug\dio_mini_action_trace_language_v1\dio_mini_action_trace_language.json
debug\dio_mini_action_trace_language_v1\dio_mini_action_trace_language_overview.json
```

Wichtig:

```text
Diese Trace-Sprache ist eine passive Lesebruecke.
Sie veraendert keine Motorik.
Sie ist keine Entry-Regel.
Sie behauptet nicht, dass DIO menschlichen Text denkt.

Sie uebersetzt nur:
Familie -> Reifeverhalten -> kurze DIO-Syntax-Spur
```

Trace-Codes:

```text
dio_trace_reif_handlung:
  gesehen -> beobachtet -> gehandelt -> bestaetigt

dio_trace_direkt_reif:
  wiederkehrend gehandelt, ohne lokale Uebergangsphase

dio_trace_reif_beobachtung:
  wiederkehrend beobachtet und handlungsnah

dio_trace_lokal_reift:
  lokal beobachtet und spaeter gehandelt

dio_trace_lokal_direkt:
  lokal direkt gehandelt

dio_trace_gehaltene_beobachtung:
  gesehen, aber nicht gehandelt

dio_trace_belastet:
  Handlung erzeugte Belastung

dio_trace_ruhig:
  keine tragende Handlungsnaehe
```

Aktueller Befund:

```text
dio_trace_reif_handlung: 5
dio_trace_direkt_reif: 2
dio_trace_lokal_reift: 13
dio_trace_lokal_direkt: 3
dio_trace_gehaltene_beobachtung: 60
dio_trace_belastet: 1
```

Top-Spuren:

```text
dio_0nmi | dio_trace_reif_handlung | strength=1.000000 | reward=6.770993
dio_1d6j | dio_trace_reif_handlung | strength=1.000000 | reward=4.768065
dio_14wi | dio_trace_reif_handlung | strength=1.000000 | reward=4.496005
dio_0a54 | dio_trace_reif_handlung | strength=1.000000 | reward=3.445308
dio_0qb3 | dio_trace_reif_handlung | strength=0.999747 | reward=2.999124
```

Lesart:

```text
DIO_MINI kann jetzt nicht nur Familien, Sensorik und Konsequenz lesen,
sondern auch eine kompakte Handlungsspur ausdruecken:

Ich habe diese Familie gesehen.
Ich habe sie gehalten oder spaeter gehandelt.
Die Konsequenz hat sie bestaetigt oder belastet.

Das bleibt eine Landkarte.
Die Motorik darf daraus spaeter nur dann lernen,
wenn diese Spur ueber reale Konsequenz und wiederkehrende Wahrnehmung getragen ist.
```

## Trace-Stabilitaet

Neue Diagnose:

```text
python -m DIO_MINI.compare_action_trace_language --baseline debug\dio_mini_action_trace_language_v1\dio_mini_action_trace_language.csv --current debug\dio_mini_action_trace_language_v1\dio_mini_action_trace_language.csv --output-dir debug\dio_mini_action_trace_stability_selfcheck_v1
```

Zweck:

```text
Trace-Sprache nicht nur erzeugen,
sondern zwischen zwei Staenden vergleichen.

Damit wird sichtbar:

- gleiche Familie, gleiche Trace-Spur
- gleiche Familie, veraenderte Trace-Spur
- neue Trace-Familie
- verschwundene Trace-Familie
- staerker oder schwaecher gewordene Spur
```

Selfcheck:

```text
stable_trace: 84
trace_shift: 0
new_trace_family: 0
missing_trace_family: 0
```

Stable reif Handlung:

```text
dio_0nmi
dio_1d6j
dio_14wi
dio_0a54
dio_0qb3
```

Lesart:

```text
Das Werkzeug ist technisch sauber.
Der Selfcheck zeigt keine kuenstliche Drift.

Der naechste echte Test ist ein neuer kontrollierter Lauf:
alte Trace-Sprache gegen neue Trace-Sprache.

Erst dann sieht man,
ob DIO gleiche Reifespuren wiederfindet
oder ob die Syntax driftet.
```

## Trace-Stabilitaet nach Probe5-Repeat

Neuer kontrollierter Repeat:

```text
python -m DIO_MINI.run_mini --data data\kontrolliert_sensor_relation_probe5_2episoden_5m_SOLUSDT.csv --runs 4 --memory bot_memory\dio_mini_sensor_relation_probe5_memory.json --debug-root debug\dio_mini_sensor_relation_probe5_repeat
```

Laeufe:

```text
Run 76: 3 Trades, Reward 2.4217, 7 Symbole
Run 77: 3 Trades, Reward 1.5499, 6 Symbole
Run 78: 3 Trades, Reward 1.5499, 6 Symbole
Run 79: 3 Trades, Reward 1.5499, 6 Symbole
```

Lokale Handlungsnaehe:

```text
debug\dio_mini_action_transition_probe5_repeat

direct_positive_action:
  3 Familien
  Reward: 6.132231
  dio_0x52
  dio_18jg
  dio_1vm7

observation_to_positive_action:
  1 Familie
  Reward: 0.939096
  dio_09jn

held_observation:
  3 Familien
```

Neue Cross-World-Sicht:

```text
debug\dio_mini_cross_world_action_transition_v2
```

Klassen:

```text
matured_action_pattern:
  7 Familien
  Reward: 30.026822

direct_mature_pattern:
  3 Familien
  Reward: 5.737034

observation_maturing_pattern:
  1 Familie
  Reward: 0.939096

local_observation_to_action:
  11 Familien
  Reward: 21.160392

local_direct_action:
  3 Familien
  Reward: 10.207592

held_observation_pattern:
  59 Familien
  Reward: 0.0

burdened_action_pattern:
  1 Familie
  Reward: -0.431148
```

Neue reife Handlungsspuren:

```text
dio_0nmi
dio_1d6j
dio_14wi
dio_0x52
dio_1vm7
dio_0a54
dio_0qb3
```

Trace-Vergleich v1 zu v2:

```text
python -m DIO_MINI.compare_action_trace_language --baseline debug\dio_mini_action_trace_language_v1\dio_mini_action_trace_language.csv --current debug\dio_mini_action_trace_language_v2\dio_mini_action_trace_language.csv --output-dir debug\dio_mini_action_trace_stability_v1_to_v2
```

Ergebnis:

```text
stable_trace: 78
same_trace_stronger: 2
trace_shift: 4
new_trace_family: 1
```

Wichtige Trace-Wechsel:

```text
dio_0x52:
  dio_trace_lokal_reift -> dio_trace_reif_handlung
  reward 0.798562 -> 3.992810

dio_1vm7:
  dio_trace_lokal_reift -> dio_trace_reif_handlung
  reward 2.369678 -> 3.554517

dio_18jg:
  dio_trace_gehaltene_beobachtung -> dio_trace_direkt_reif
  reward 0.0 -> 1.753144

dio_09jn:
  dio_trace_gehaltene_beobachtung -> dio_trace_reif_beobachtung
  reward 0.0 -> 0.939096
```

Befund:

```text
Die Syntax driftet nicht chaotisch.
Der groesste Teil bleibt stabil.

Die relevanten Veraenderungen sind Reifungsbewegungen:
lokal reifende Familien werden weltuebergreifend reife Handlung,
gehaltene Beobachtung wird direkte oder reifende Spur.

Das ist ein guter Mini-DIO-Befund:
Wiederkehr, Konsequenz und Handlung naehern sich an,
ohne dass Motorik oder Gates geaendert wurden.
```

## Sensorische Basis gereifter Familien

Neue Diagnose:

```text
python -m DIO_MINI.inspect_family_senses --phase-rows debug\dio_mini_cross_world_action_transition_v2\dio_mini_cross_world_action_transition_phase_rows.csv --family dio_0x52 --family dio_1vm7 --output-dir debug\dio_mini_family_senses_probe5_reifung_v1
```

Zweck:

```text
Lesen, welche sensorische Basis eine gereifte Familie traegt:

- Sehen: Formfluss, Formstabilitaet, Formwechsel
- Hoeren: Energieton, Energieverschiebung
- Fuehlen: MCM-Kohaerenz, MCM-Spannung, MCM-Asymmetrie
```

Ergebnis:

```text
dio_0x52:
  Reward: 3.992810
  executed_rows: 5
  observed_rows: 3
  sensor_delta_in_observation_to_action: 0.0

dio_1vm7:
  Reward: 3.554517
  executed_rows: 3
  observed_rows: 2
  sensor_delta_in_observation_to_action: 0.0
```

Sensorische Signatur:

```text
dio_0x52:
  sehen_flow: 0.077762
  sehen_stability: 1.0
  hoeren_tone: 0.090378
  hoeren_shift: 0.3
  mcm_coherence: 0.974694
  mcm_tension: 0.095503
  mcm_asymmetry: 0.140873

dio_1vm7:
  sehen_flow: 0.813389
  sehen_stability: 1.0
  hoeren_tone: -0.021276
  hoeren_shift: -0.245098
  mcm_coherence: 0.994043
  mcm_tension: 0.366362
  mcm_asymmetry: 0.382774
```

Befund:

```text
Bei beiden Familien ist die sensorische Signatur in der echten
Beobachtung-zu-Handlung-Phase identisch:

observed -> executed delta = 0.0

Das bedeutet:
DIO_MINI handelt spaeter nicht, weil es ploetzlich andere Sinnesdaten bekommt.
Es handelt bei gleicher Sinneslage mit gereifter Naehe.

Das ist fachlich wichtig:
Reife entsteht hier aus Wiederkehr, Memory und Konsequenz,
nicht aus einer neu eingeschobenen Regel.
```

## Transfer auf leichte Variantenwelt

Neue kontrollierte Variantenwelt:

```text
data\kontrolliert_sensor_relation_probe5_variation_2episoden_5m_SOLUSDT.csv
```

Zweck:

```text
Probe5 leicht veraendern,
ohne den Charakter der Welt vollstaendig zu wechseln.

Damit wird geprueft:

- bleiben gereifte Familien stabil?
- entstehen neue lokale Familien?
- wird Reife chaotisch oder nachvollziehbar verschoben?
```

Lauf:

```text
python -m DIO_MINI.run_mini --data data\kontrolliert_sensor_relation_probe5_variation_2episoden_5m_SOLUSDT.csv --runs 4 --memory bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json --debug-root debug\dio_mini_sensor_relation_probe5_variation
```

Ergebnis:

```text
Run 80: 2 Trades, Reward 0.9014, 10 Symbole
Run 81: 2 Trades, Reward 0.9014, 10 Symbole
Run 82: 2 Trades, Reward 0.9014, 10 Symbole
Run 83: 3 Trades, Reward 1.6998, 6 Symbole
```

Lokale Handlungsnaehe:

```text
debug\dio_mini_action_transition_probe5_variation

direct_positive_action:
  2 Familien
  Reward: 3.605736
  dio_0qb3
  dio_09jn

observation_to_positive_action:
  1 Familie
  Reward: 0.798383
  dio_14mj

held_observation:
  7 Familien
```

Cross-World v3:

```text
debug\dio_mini_cross_world_action_transition_v3
```

Reife Handlung:

```text
matured_action_pattern:
  8 Familien
  Reward: 34.571654

dio_0qb3
dio_0a54
dio_09jn
dio_0nmi
dio_1d6j
dio_14wi
dio_0x52
dio_1vm7
```

Trace-Vergleich v2 zu v3:

```text
stable_trace: 83
same_trace_stronger: 1
trace_shift: 1
new_trace_family: 7
```

Wichtiger Trace-Wechsel:

```text
dio_09jn:
  dio_trace_reif_beobachtung -> dio_trace_reif_handlung
  reward 0.939096 -> 2.190568
```

Lesart:

```text
Die Variantenwelt erzeugt neue lokale Syntaxfamilien,
aber keinen chaotischen Zusammenbruch.

83 Familien bleiben stabil.
Nur eine Familie wechselt ihre Trace-Klasse:
dio_09jn reift von Beobachtung zu reifer Handlung.

Die vorher gereiften Familien dio_0x52 und dio_1vm7 bleiben in der
Cross-World-Sicht reif, werden in der Variante aber nicht erneut motorisch
dominant. Das ist fachlich sauber:
Reife bleibt erhalten, aber nicht jede reife Spur muss in jeder Welt handeln.
```

Sensorische Basis der Variation:

```text
debug\dio_mini_family_senses_probe5_variation_v1
```

```text
dio_09jn:
  Phasen: probe5, probe5_repeat, probe5_variation
  Reward: 2.190568
  sensor_delta_in_observation_to_action: 0.0

dio_0qb3:
  Phasen: probe2, probe5, probe5_variation
  Reward: 5.353388
  sensor_delta_in_observation_to_action: 0.0

dio_14mj:
  neue lokale Familie in probe5_variation
  Reward: 0.798383
  sensor_delta_in_observation_to_action: 0.0
```

Befund:

```text
Auch in der Variantenwelt entsteht Handlung nicht durch veraenderte
Sinnesdaten innerhalb der Reifungsphase.

Die sensorische Lage bleibt gleich,
aber die Reifung und Konsequenzspur veraendert die Handlungnaehe.

Das bestaetigt den Mini-Kern:
Sehen, Hoeren und Fuehlen bilden die Signatur.
Memory und Konsequenz bestimmen, ob daraus spaeter Handlungnaehe entsteht.
```

## Sensorische Nachbarschaft statt nur gleiche Familie

Neue Diagnose:

```text
python -m DIO_MINI.analyze_family_sense_neighbors --phase-rows debug\dio_mini_cross_world_action_transition_v3\dio_mini_cross_world_action_transition_phase_rows.csv --target dio_14mj --reference dio_0nmi --reference dio_0qb3 --reference dio_1d6j --reference dio_14wi --reference dio_0x52 --reference dio_1vm7 --reference dio_0a54 --reference dio_09jn --top 8 --output-dir debug\dio_mini_family_sense_neighbors_variation_v1
```

Zweck:

```text
Nicht nur pruefen:
Ist das dieselbe Familie?

Sondern pruefen:
Liegt eine neue Familie sensorisch in der Naehe einer gereiften Familie?

Das ist wichtig fuer Aehnlichkeitsreife:
DIO soll nicht nur exakt wiedererkennen,
sondern verwandte Sinneslagen als Nachbarschaft lesen koennen.
```

Ergebnis fuer die neue lokale Familie `dio_14mj`:

```text
dio_14mj -> dio_14wi:
  distance: 0.017364
  similarity: 0.982636

dio_14mj -> dio_0x52:
  distance: 0.028501
  similarity: 0.971499

dio_14mj -> dio_09jn:
  distance: 0.328191
  similarity: 0.671809

dio_14mj -> dio_1vm7:
  distance: 0.376183
  similarity: 0.623817
```

Befund:

```text
dio_14mj ist eine neue lokale Syntaxfamilie,
aber sensorisch sehr nah an zwei gereiften Familien:

- dio_14wi
- dio_0x52

Damit entsteht ein wichtiger Mini-DIO-Schritt:
Neue Syntax muss nicht isoliert sein.
Sie kann als Nachbar einer gereiften Sinneslage gelesen werden.

Das ist noch keine Motorik.
Es ist eine passive Reifelandkarte fuer verwandte Formen.
```

Lesart:

```text
Mini-DIO beginnt damit,
nicht nur gleiche Formfamilien ueber Wiederkehr zu lesen,
sondern auch verwandte Sinneslagen zu erkennen.

Das ist der Anfang von emergenter Aehnlichkeitsreife:

Ich sehe nicht exakt dasselbe,
aber es liegt nah an etwas,
das bereits getragen hat.
```

## Aehnlichkeitskarte neuer Variantenfamilien

Erweiterte Diagnose:

```text
python -m DIO_MINI.analyze_family_sense_neighbors --phase-rows debug\dio_mini_cross_world_action_transition_v3\dio_mini_cross_world_action_transition_phase_rows.csv --target dio_14mj --target dio_1tik --target dio_0kpn --target dio_0p8l --target dio_1kfx --target dio_05pr --target dio_1et3 --reference dio_0nmi --reference dio_0qb3 --reference dio_1d6j --reference dio_14wi --reference dio_0x52 --reference dio_1vm7 --reference dio_0a54 --reference dio_09jn --top 3 --output-dir debug\dio_mini_family_sense_neighbors_variation_all_v1
```

Ziel:

```text
Alle neuen/lokalen Variantenfamilien gegen den reifen Kern lesen.

Das bleibt passiv:
keine Motorik,
kein Gate,
keine Entry-Regel.
```

Starke Nachbarschaften:

```text
dio_14mj -> dio_14wi:
  similarity: 0.982636

dio_14mj -> dio_0x52:
  similarity: 0.971499

dio_1tik -> dio_0a54:
  similarity: 0.895276

dio_0kpn -> dio_0nmi:
  similarity: 0.884960

dio_0p8l -> dio_1d6j:
  similarity: 0.800650

dio_0p8l -> dio_0qb3:
  similarity: 0.749026
```

Schwaechere Nachbarschaften:

```text
dio_05pr:
  naechste Reifespur nur similarity 0.499039

dio_1et3:
  naechste Reifespur similarity 0.569757

dio_1kfx:
  naechste Reifespur similarity 0.580551
```

Befund:

```text
Nicht jede neue Syntaxfamilie ist gleich wertvoll.

Ein Teil der neuen Variantenfamilien liegt sehr nah an gereiften Sinneslagen.
Ein anderer Teil bleibt sensorisch weiter entfernt.

Damit entsteht eine saubere passive Aehnlichkeitskarte:
Neue Formen koennen als Nachbarn gereifter Erfahrung gelesen werden,
ohne sie automatisch zu handeln.
```

## Nachbarschaft mit Konsequenz gekoppelt

Neue Diagnose:

```text
python -m DIO_MINI.analyze_neighbor_consequence --neighbors debug\dio_mini_family_sense_neighbors_variation_all_v1\dio_mini_family_sense_neighbors.csv --world-summary debug\dio_mini_cross_world_action_transition_v3\dio_mini_cross_world_action_transition_world_summary.csv --output-dir debug\dio_mini_neighbor_consequence_variation_v1
```

Zweck:

```text
Sensorische Nachbarschaft nicht als Handlungssignal verwenden,
sondern mit Konsequenz lesen.

Moegliche passive Zustaende:

reifende_verwandtschaft:
  neue/lokale Familie liegt sensorisch nahe an gereifter Erfahrung
  und hat selbst positive Konsequenz getragen.

beobachtete_verwandtschaft:
  neue/lokale Familie liegt sensorisch nahe an gereifter Erfahrung,
  wurde aber noch nicht positiv gehandelt.

vorsichtige_verwandtschaft:
  Nachbarschaft zu Erfahrung ist da,
  aber Konsequenz oder Belastung spricht fuer Vorsicht.

offene_verwandtschaft:
  Nachbarschaft ist lesbar,
  Konsequenz ist aber noch nicht aussagekraeftig.
```

Ergebnis:

```text
reifende_verwandtschaft: 3
beobachtete_verwandtschaft: 18
```

Reifende Verwandtschaft:

```text
dio_14mj -> dio_14wi:
  similarity: 0.982636
  target_reward: 0.798383
  reference_reward: 4.496005

dio_14mj -> dio_0x52:
  similarity: 0.971499
  target_reward: 0.798383
  reference_reward: 3.992810

dio_14mj -> dio_09jn:
  similarity: 0.671809
  target_reward: 0.798383
  reference_reward: 2.190568
```

Beobachtete Verwandtschaft:

```text
dio_1tik -> dio_0a54:
  similarity: 0.895276
  target_reward: 0.0

dio_0kpn -> dio_0nmi:
  similarity: 0.884960
  target_reward: 0.0

dio_0p8l -> dio_1d6j:
  similarity: 0.800650
  target_reward: 0.0
```

Befund:

```text
Die Aehnlichkeitskarte wird jetzt mit Konsequenz lesbar.

dio_14mj ist nicht nur sensorisch nah an reifen Familien,
sondern hat selbst positive Konsequenz getragen.
Das macht daraus eine reifende Verwandtschaft.

Andere Familien sind zwar sensorisch nah,
haben aber noch keine positive Handlungskonsequenz.
Sie bleiben beobachtete Verwandtschaft.

Das ist fachlich sauber:
Nachbarschaft allein reicht nicht.
Erst reale Konsequenz gibt der Verwandtschaft Reifung.
```

## Passive Verwandtschaft im Memory gespeichert

Neue Memory-Struktur:

```text
SemanticMemory.neighbor_consequences
```

Neue Methoden:

```text
SemanticMemory.set_neighbor_consequence_summary
SemanticMemory.compact_neighbor_consequences
```

Neues Store-Werkzeug:

```text
python -m DIO_MINI.store_neighbor_consequences --memory bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json --relations debug\dio_mini_neighbor_consequence_variation_v1\dio_mini_neighbor_consequence.csv --max-relations 64
```

Wichtig:

```text
neighbor_consequences ist passiv.
Diese Map wird nicht von action_diagnostics gelesen.
Sie veraendert keine Motorik.
Sie erzeugt keine Entry-Regel.
```

Gespeicherter Stand:

```text
neighbor_consequences: 21

reifende_verwandtschaft: 3
beobachtete_verwandtschaft: 18
```

Beispiele:

```text
dio_14mj -> dio_14wi:
  state: reifende_verwandtschaft
  similarity: 0.982636
  passive_only: true

dio_14mj -> dio_0x52:
  state: reifende_verwandtschaft
  similarity: 0.971499
  passive_only: true

dio_0kpn -> dio_0nmi:
  state: beobachtete_verwandtschaft
  similarity: 0.884960
  passive_only: true
```

Befund:

```text
DIO_MINI kann jetzt eine neue Form nicht nur als Familie speichern,
sondern auch als Verwandtschaft zu bereits gereiften Sinneslagen.

Der Unterschied bleibt sauber:

Familie:
  Das ist meine eigene Syntax fuer diese Sinneslage.

Verwandtschaft:
  Diese neue Syntax liegt sensorisch nahe an einer Erfahrung.

Konsequenz:
  Diese Naehe hat getragen, blieb Beobachtung oder muss vorsichtig gelesen werden.
```

## Stabilitaet nach gespeicherter Verwandtschaft

Nach dem passiven Speichern der Nachbarschafts-Konsequenzen wurde dieselbe
Probe5-Variation erneut ausgefuehrt:

```text
python -m DIO_MINI.run_mini --data data\kontrolliert_sensor_relation_probe5_variation_2episoden_5m_SOLUSDT.csv --runs 4 --memory bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json --debug-root debug\dio_mini_sensor_relation_probe5_variation_after_neighbor_store
```

Ergebnis:

```text
Run 88: trades=3 reward=1.5662
Run 89: trades=3 reward=1.5662
Run 90: trades=3 reward=1.5662
Run 91: trades=3 reward=1.5662
```

Lokale Uebergangsanalyse:

```text
direct_positive_action: 3
held_observation: 3

direkt positiv:
  dio_14mj
  dio_1tik
  dio_09jn

gehaltene Beobachtung:
  dio_0xgj
  dio_0kpn
  dio_1kqv
```

Trace-Stabilitaet v3 -> v4:

```text
stable_trace: 87
same_trace_stronger: 3
trace_shift: 2

trace_shift:
  dio_14mj
  dio_1tik
```

Nachbarschafts-Konsequenz v4:

```text
reifende_verwandtschaft: 6
beobachtete_verwandtschaft: 9
```

Reifende Verwandtschaften:

```text
dio_14mj -> dio_14wi:
  similarity: 0.982636
  target_reward: 3.991915

dio_14mj -> dio_0x52:
  similarity: 0.971499
  target_reward: 3.991915

dio_1tik -> dio_0a54:
  similarity: 0.895276
  target_reward: 1.819980

dio_14mj -> dio_09jn:
  similarity: 0.671134
  target_reward: 3.991915

dio_1tik -> dio_0nmi:
  similarity: 0.615206
  target_reward: 1.819980

dio_1tik -> dio_0qb3:
  similarity: 0.529643
  target_reward: 1.819980
```

Gespeicherter Memory-Stand:

```text
symbols: 205
sensor_relations: 64
neighbor_consequences: 27

beobachtete_verwandtschaft: 21
reifende_verwandtschaft: 6
```

Befund:

```text
Die gespeicherte Verwandtschaft bleibt passiv.
Sie veraendert die Motorik im Kontrolllauf nicht.

Die Reifung entsteht nicht aus einer Regel:
"Wenn Nachbar, dann handeln."

Sie entsteht aus:
1. sensorischer Naehe,
2. wiederholter eigener Syntax,
3. realer Konsequenz,
4. stabiler Spur ueber Weltvariation.

Damit ist die Verwandtschaftskarte ein episodisches Gedaechtnisorgan,
kein Entry-System.
```

Naechster Schritt:

```text
Die passiven Verwandtschaften duerfen als Reife- und Vorsichtslandkarte
auswertbar bleiben.

Sie duerfen aber erst dann in aktive Handlungsnaehe einfliessen,
wenn dafuer eine eigene organische Rueckkopplung gebaut ist:
sehen/hoeren/fuehlen -> Familiennaehe -> Konsequenzgedaechtnis ->
lokale Gegenwart -> Handlung oder Beobachtung.
```

## Cross-World v5 nach Kontrolllauf

Der Kontrolllauf nach gespeicherter Verwandtschaft wurde in die
weltuebergreifende Karte aufgenommen:

```text
debug\dio_mini_cross_world_action_transition_v5
debug\dio_mini_action_trace_language_v5
debug\dio_mini_action_trace_stability_v4_to_v5
debug\dio_mini_family_sense_neighbors_v5
debug\dio_mini_neighbor_consequence_v5
```

Cross-World-Kern:

```text
dio_09jn:
  matured_action_pattern
  phases: 5
  executed: 15
  observed: 5
  reward: 4.6935

dio_14mj:
  matured_action_pattern
  phases: 3
  executed: 9
  observed: 3
  reward: 7.1854

dio_1tik:
  direct_mature_pattern
  phases: 3
  executed: 8
  observed: 4
  reward: 3.6400

dio_1kqv:
  held_observation_pattern
  phases: 5
  executed: 0
  observed: 20

dio_0xgj:
  held_observation_pattern
  phases: 3
  executed: 0
  observed: 12

dio_0kpn:
  held_observation_pattern
  phases: 3
  executed: 0
  observed: 12
```

Trace-Stabilitaet v4 -> v5:

```text
stable_trace: 88
same_trace_stronger: 4
trace_shift: 0
```

Nachbarschafts-Konsequenz v5:

```text
reifende_verwandtschaft: 6
beobachtete_verwandtschaft: 9
```

Staerkste reifende Verwandtschaft:

```text
dio_14mj -> dio_14wi:
  similarity: 0.982636
  target_reward: 7.185447

dio_14mj -> dio_0x52:
  similarity: 0.971499
  target_reward: 7.185447

dio_1tik -> dio_0a54:
  similarity: 0.895276
  target_reward: 3.639960
```

Befund:

```text
Die sensorische Nachbarschaft selbst bleibt stabil.
Die Konsequenzspur dahinter wird staerker.

Das ist der wichtige Unterschied:
DIO_MINI sieht nicht einfach "gleich".
DIO_MINI sieht Naehe, beobachtet Wiederkehr und bindet diese Naehe
erst ueber reale Konsequenz an Reife.

Beobachtete Verwandtschaft bleibt Beobachtung,
solange keine eigene ausgefuehrte Konsequenz getragen wurde.
```

## Probe6: weitere kleine Weltvariation

Neue kontrollierte Variation:

```text
data\kontrolliert_sensor_relation_probe6_variation_2episoden_5m_SOLUSDT.csv
```

Ziel:

```text
Keine Wiederholung messen,
sondern leichte Verschiebung von Reihenfolge und Amplitude.

Pruefung:
Kann DIO_MINI bestehende Sinnes-/Konsequenznaehe auf eine leicht
veraenderte Welt uebertragen?
```

Lauf:

```text
python -m DIO_MINI.run_mini --data data\kontrolliert_sensor_relation_probe6_variation_2episoden_5m_SOLUSDT.csv --runs 4 --memory bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json --debug-root debug\dio_mini_sensor_relation_probe6_variation
```

Ergebnis:

```text
Run 92: trades=1 reward=0.8889
Run 93: trades=2 reward=2.2297
Run 94: trades=2 reward=2.1876
Run 95: trades=3 reward=3.0054
```

Lokale Uebergangsanalyse:

```text
direct_positive_action: 1
observation_to_positive_action: 4
held_observation: 10
quiet_family: 1

observation_to_positive_action:
  dio_1vpi
  dio_01nr
  dio_0wv3
  dio_07wx

direct_positive_action:
  dio_1nlc
```

Sinnesbefund:

```text
dio_01nr:
  phases: sensor_relation_probe2, sensor_relation_probe6_variation
  observed_rows: 3
  executed_rows: 1
  reward_sum: 1.340779
  max_sensor_delta_in_observation_to_action: 0.0

dio_1vpi:
  phases: sensor_relation_probe6_variation
  observed_rows: 2
  executed_rows: 2
  reward_sum: 2.597526
  max_sensor_delta_in_observation_to_action: 0.0

dio_0wv3:
  observed_rows: 3
  executed_rows: 1
  reward_sum: 0.947695
  max_sensor_delta_in_observation_to_action: 0.0

dio_07wx:
  observed_rows: 3
  executed_rows: 1
  reward_sum: 0.758933
  max_sensor_delta_in_observation_to_action: 0.0
```

Befund:

```text
Wieder entsteht Handlung nicht durch veraenderte Sensorik.
Die Sinneslage bleibt gleich.

Der Uebergang entsteht durch:
  Beobachtung,
  Wiederkehr,
  Memory,
  Konsequenzbindung.
```

Cross-World v6:

```text
debug\dio_mini_cross_world_action_transition_v6
```

Neue relevante Spur:

```text
dio_01nr:
  observation_maturing_pattern
  phases: 2
  executed: 1
  observed: 3
  reward: 1.340779
```

Trace-Stabilitaet v5 -> v6:

```text
stable_trace: 90
same_trace_stronger: 1
trace_shift: 1
new_trace_family: 14

trace_shift:
  dio_01nr
```

Interpretation:

```text
dio_01nr ist die wichtige Spur:
Sie war Beobachtung,
taucht in einer spaeteren Weltvariation wieder auf,
handelt positiv
und wird damit zur Beobachtung-Reifung.
```

Nachbarschafts-Konsequenz v6:

```text
debug\dio_mini_neighbor_consequence_v6

reifende_verwandtschaft: 15
beobachtete_verwandtschaft: 6
```

Beispiele:

```text
dio_01nr -> dio_1d6j:
  state: reifende_verwandtschaft
  similarity: 0.773828
  target_reward: 1.340779

dio_0wv3 -> dio_0x52:
  state: reifende_verwandtschaft
  similarity: 0.967591
  target_reward: 0.947695

dio_1vpi -> dio_1vm7:
  state: reifende_verwandtschaft
  similarity: 0.926423
  target_reward: 2.597526

dio_0kpn -> dio_0nmi:
  state: beobachtete_verwandtschaft
  similarity: 0.884592
  target_reward: 0.0

dio_1kqv -> dio_09jn:
  state: beobachtete_verwandtschaft
  similarity: 0.886535
  target_reward: 0.0
```

Gespeicherter Memory-Stand nach v6:

```text
symbols: 218
sensor_relations: 64
neighbor_consequences: 42

reifende_verwandtschaft: 21
beobachtete_verwandtschaft: 21
```

Befund:

```text
Probe6 bestaetigt die Mini-Richtung.

DIO_MINI lernt nicht nur gleiche Namen.
Es erkennt sensorische Verwandtschaften,
laesst manche als Beobachtung stehen
und laesst andere durch reale Konsequenz reifen.

Das bleibt weiterhin passiv gespeichert.
Keine dieser Verwandtschaften ist eine Entry-Regel.
```

## Probe7: Belastungsversuch wurde Reifeprobe

Neue Gegenprobe:

```text
data\kontrolliert_sensor_relation_probe7_belastung_2episoden_5m_SOLUSDT.csv
```

Ziel:

```text
Eine sensorisch nahe Struktur mit frueher Reversal-Wirkung anbieten.
Pruefen, ob negative Konsequenz entsteht und daraus
vorsichtige_verwandtschaft gebildet wird.
```

Lauf:

```text
debug\dio_mini_sensor_relation_probe7_belastung
```

Ergebnis:

```text
Run 96: trades=1 reward=0.7483
Run 97: trades=1 reward=0.7483
Run 98: trades=1 reward=0.7483
Run 99: trades=3 reward=2.6009
```

Lokale Uebergangsanalyse:

```text
direct_positive_action: 1
observation_to_positive_action: 2
held_observation: 11
quiet_family: 1

direct_positive_action:
  dio_0wv3

observation_to_positive_action:
  dio_0u8f
  dio_19i4
```

Sinnesbefund:

```text
dio_0wv3:
  phases: sensor_relation_probe6_variation, sensor_relation_probe7_belastung
  observed_rows: 3
  executed_rows: 5
  reward_sum: 3.940907
  max_sensor_delta_in_observation_to_action: 0.0

dio_0u8f:
  observed_rows: 3
  executed_rows: 1
  reward_sum: 0.992290
  max_sensor_delta_in_observation_to_action: 0.0

dio_19i4:
  observed_rows: 3
  executed_rows: 1
  reward_sum: 0.860328
  max_sensor_delta_in_observation_to_action: 0.0
```

Befund:

```text
Die geplante Belastung wurde nicht als negative Konsequenz sichtbar.
DIO_MINI hat die Struktur positiv verarbeitet.

Damit war Probe7 kein Schmerztest,
sondern eine weitere Reifeprobe.
```

Cross-World v7:

```text
debug\dio_mini_cross_world_action_transition_v7
```

Neue Reifespur:

```text
dio_0wv3:
  matured_action_pattern
  phases: sensor_relation_probe6_variation, sensor_relation_probe7_belastung
  executed: 5
  observed: 3
  reward: 3.940907
```

Trace-Stabilitaet v6 -> v7:

```text
stable_trace: 105
trace_shift: 1
new_trace_family: 14

trace_shift:
  dio_0wv3
```

Nachbarschafts-Konsequenz v7:

```text
reifende_verwandtschaft: 9
beobachtete_verwandtschaft: 9
```

Beispiele:

```text
dio_0wv3 -> dio_0x52:
  state: reifende_verwandtschaft
  similarity: 0.967267
  target_reward: 3.940907

dio_0u8f -> dio_1tik:
  state: reifende_verwandtschaft
  similarity: 0.838616
  target_reward: 0.992290

dio_19p6 -> dio_0a54:
  state: beobachtete_verwandtschaft
  similarity: 0.908890
  target_reward: 0.0

dio_1kqv -> dio_09jn:
  state: beobachtete_verwandtschaft
  similarity: 0.886535
  target_reward: 0.0
```

Gespeicherter Memory-Stand nach Probe7:

```text
symbols: 232
sensor_relations: 64
neighbor_consequences: 54

reifende_verwandtschaft: 27
beobachtete_verwandtschaft: 27
```

Interpretation:

```text
DIO_MINI kann inzwischen nahe Formen weiter positiv reifen lassen,
ohne dass aus jeder Naehe automatisch Handlung wird.

Eine echte vorsichtige_verwandtschaft wurde noch nicht erzeugt.
Dafuer braucht es eine kontrollierte negative Konsequenz,
nicht nur eine anders strukturierte Gegenbewegung.
```

## Probe8: echter Negativkontakt und vorsichtige Verwandtschaft

Neue gezielte Negativprobe:

```text
data\kontrolliert_sensor_relation_probe8_negativkontakt_2episoden_5m_SOLUSDT.csv
```

Konstruktion:

```text
Der Anfangskontakt entspricht der bekannten dio_0wv3-Sinneslage.
DIO_MINI hatte dort ueber Memory eine starke SHORT-Naehe.

Danach laufen die naechsten 5 Kerzen klar gegen SHORT.
Damit wird nicht nur Variation erzeugt,
sondern eine echte negative Konsequenz fuer den vertrauten Kontakt.
```

Lauf:

```text
debug\dio_mini_sensor_relation_probe8_negativkontakt
```

Ergebnis:

```text
Run 100: trades=1 reward=-1.5305
Run 101: trades=1 reward=-1.5305
Run 102: trades=2 reward=2.7513
Run 103: trades=3 reward=3.4940
```

Tick-1-Befund:

```text
family: dio_0wv3
action: SHORT
best_action_training: LONG
reward: -1.530472
best_reward_training: 1.330472

readiness_short: 0.478880
readiness_long: 0.004655
```

Interpretation:

```text
DIO_MINI ging mit vertrauter SHORT-Reife in Kontakt.
Die Realitaet lief dagegen.
Der Kontakt wurde belastet.
Danach reorganisierte DIO_MINI:
  Run 102 und 103 wurden wieder positiv.
```

Memory-Befund fuer dio_0wv3:

```text
SHORT:
  last_reward: -1.530472
  caution: hoch

LONG:
  trust steigt
```

Lokale Diagnose:

```text
direct_burdened_action: 1
observation_to_positive_action: 2
held_observation: 11
```

Cross-World v8:

```text
debug\dio_mini_cross_world_action_transition_v8

dio_0wv3:
  matured_action_pattern
  phases: 3
  executed: 9
  observed: 3
  burdened_action: 1
  reward_sum: 3.540907
```

Befund:

```text
Die Familie wird nicht verworfen.
Sie bleibt insgesamt reif,
aber sie traegt jetzt eine vorsichtige Teilspur.

Das ist fachlich wichtig:
Ein Organismus lernt nicht "alles schlecht",
sondern "dieser vertraute Kontakt kann in dieser Richtung verletzen".
```

Nachbarschafts-Konsequenz v8:

```text
debug\dio_mini_neighbor_consequence_v8

reifende_verwandtschaft: 4
beobachtete_verwandtschaft: 8
vorsichtige_verwandtschaft: 6
```

Vorsichtige Verwandtschaft:

```text
dio_0wv3 -> dio_0x52:
  similarity: 0.967230
  target_reward: 3.540907

dio_0wv3 -> dio_14wi:
  similarity: 0.954838
  target_reward: 3.540907

dio_0wv3 -> dio_14mj:
  similarity: 0.939965
  target_reward: 3.540907

dio_14eb -> dio_0wv3:
  similarity: 0.646102
  target_reward: 2.841602

dio_0eh8 -> dio_0wv3:
  similarity: 0.565858
  target_reward: 0.742752

dio_1ayy -> dio_0wv3:
  similarity: 0.594309
  target_reward: 0.0
```

Passive Memory-Rangfolge korrigiert:

```text
vorsichtige_verwandtschaft wird beim Kompaktieren nicht mehr
hinter reiner Beobachtung verdraengt.

Die Karte bleibt weiterhin passiv_only.
Keine Motorik liest daraus eine Entry-Regel.
```

Gespeicherter Memory-Stand nach Probe8:

```text
symbols: 244
sensor_relations: 64
neighbor_consequences: 64

reifende_verwandtschaft: 28
beobachtete_verwandtschaft: 30
vorsichtige_verwandtschaft: 6
```

Befund:

```text
Probe8 bestaetigt den kompletten Mini-Lernkreis:

1. vertraute Sinneslage,
2. Handlung aus gereifter Naehe,
3. negative Konsequenz,
4. Reorganisation,
5. vorsichtige Verwandtschaft,
6. keine harte Sperre,
7. spaetere positive Anpassung.
```

## Probe8-Repeat: Vorsicht wirkt ohne harte Sperre

Nach dem gespeicherten Negativkontakt wurde dieselbe Probe8-Welt erneut
ausgefuehrt:

```text
debug\dio_mini_sensor_relation_probe8_negativkontakt_repeat

run 104: trades=3 reward=3.4940
run 105: trades=3 reward=3.4467
run 106: trades=3 reward=3.4467
run 107: trades=3 reward=3.4467
```

Entscheidender Befund:

```text
dio_0wv3 fiel nicht erneut in den belasteten SHORT-Kontakt.
Der erste Kontakt wurde als LONG gehandelt und positiv bestaetigt.

run 104 tick 1:
  family: dio_0wv3
  action: LONG
  best_action_training: LONG
  reward: 1.330472
  readiness_long: 0.365780
  readiness_short: -0.087277

run 107 tick 1:
  family: dio_0wv3
  action: LONG
  reward: 1.330472
  readiness_long: 0.777705
  readiness_short: -0.086974
```

Lokale Diagnose:

```text
direct_positive_action: 3
observation_to_positive_action: 1
held_observation: 3
direct_burdened_action: 0
```

Cross-World v9:

```text
dio_0wv3:
  matured_action_pattern
  phases: 4
  executed: 13
  observed: 3
  reward_sum: 8.862795
```

Trace-Sprache v8 -> v9:

```text
stable_trace: 126
same_trace_stronger: 3
trace_shift: 3
```

Nachbarschafts-Konsequenz v9:

```text
reifende_verwandtschaft: 7
vorsichtige_verwandtschaft: 5
```

Gespeicherter Memory-Stand nach Probe8-Repeat:

```text
symbols: 244
sensor_relations: 64
neighbor_consequences: 64

reifende_verwandtschaft: 31
beobachtete_verwandtschaft: 27
vorsichtige_verwandtschaft: 6
```

Fachlicher Befund:

```text
Die vorsichtige Verwandtschaft wirkt als Erfahrung,
aber nicht als mechanischer Blocker.

DIO_MINI reagiert auf denselben Sinneskontakt nicht mehr mit
kopierter alter Handlung, sondern mit umgelenkter Konsequenznaehe.

Das ist der erste klare Mini-Nachweis fuer:
Kontakt -> Konsequenz -> vorsichtige Reorganisation -> bessere
Wiederbegegnung.
```

## Probe9: Aehnlichkeitsuebertragung statt exakter Wiederholung

Probe9 ist keine Kopie von Probe8. Die ersten Sinneskontakte sind leicht
verschoben, behalten aber die gleiche Grundfamilie:

```text
data\kontrolliert_sensor_relation_probe9_aehnlichkeit_2episoden_5m_SOLUSDT.csv
debug\dio_mini_sensor_relation_probe9_aehnlichkeit
```

Runs:

```text
run 108: trades=3 reward=3.3899
run 109: trades=3 reward=3.3899
run 110: trades=3 reward=3.3899
run 111: trades=4 reward=3.4855
```

Lokale Diagnose:

```text
direct_positive_action: 3
observation_to_positive_action: 2
held_observation: 2
direct_burdened_action: 0
```

Cross-World v10:

```text
dio_0wv3:
  matured_action_pattern
  phases: 5
  executed: 17
  observed: 3
  reward_sum: 14.018907

dio_14eb:
  matured_action_pattern
  phases: 3
  executed: 10
  observed: 2
  reward_sum: 14.113418

dio_0szn:
  matured_action_pattern
  phases: 3
  executed: 6
  observed: 5
  reward_sum: 4.197417
```

Trace-Stabilitaet v9 -> v10:

```text
stable_trace: 127
same_trace_stronger: 2
trace_shift: 3
```

Sensorischer Befund:

```text
max_sensor_delta_in_observation_to_action: 0.0

Die Handlung entsteht nicht durch einen neuen harten Reiz,
sondern durch Wiederkehr, Reife und Konsequenznaehe.
```

Nachbarschafts-Konsequenz v10:

```text
reifende_verwandtschaft: 12
vorsichtige_verwandtschaft: 3
```

Gespeicherter Memory-Stand nach Probe9:

```text
symbols: 244
sensor_relations: 64
neighbor_consequences: 64

reifende_verwandtschaft: 38
beobachtete_verwandtschaft: 20
vorsichtige_verwandtschaft: 6
```

Fachlicher Befund:

```text
Probe9 zeigt erstmals Aehnlichkeitsuebertragung im Mini-Kern:
Ein leicht veraenderter Sinneskontakt wird nicht als komplett neue Welt
behandelt, sondern an vorhandene reifende und vorsichtige Spuren
angebunden.

Das ist keine Strategie-Regel.
Es ist eine passive Verwandtschafts- und Konsequenzkarte,
aus der DIO_MINI seine eigene Handlungnaehe entwickeln kann.
```

## Probe10: Grenze der Aehnlichkeit

Probe10 ist weiter von Probe8/Probe9 entfernt:

```text
data\kontrolliert_sensor_relation_probe10_ferne_aehnlichkeit_2episoden_5m_SOLUSDT.csv
debug\dio_mini_sensor_relation_probe10_ferne_aehnlichkeit
```

Die Welt hat mehr Stoerung, anderes Volumenprofil und weniger sauberen
Anfangskontakt. Ziel ist nicht sofortige Wiedererkennung, sondern die
Grenze zwischen Verwandtschaft und neuer Orientierung.

Runs:

```text
run 112: trades=0 reward=0.0000
run 113: trades=0 reward=0.0000
run 114: trades=1 reward=1.4161
run 115: trades=3 reward=3.1705
```

Lokale Diagnose:

```text
held_observation: 16
observation_to_positive_action: 3
quiet_family: 1
direct_positive_action: 0
```

Das ist ein anderer Befund als Probe9:

```text
Probe9:
  sofortige positive Handlung in aehnlicher Welt

Probe10:
  zuerst Beobachtung,
  dann lokale Reifung,
  dann positive Handlung
```

Neue lokale Reifung:

```text
dio_1tmf:
  executed: 2
  observed: 2
  reward_sum: 2.832120

dio_0y4s:
  executed: 1
  observed: 3
  reward_sum: 1.045363

dio_1gp1:
  executed: 1
  observed: 3
  reward_sum: 0.709061
```

Trace-Stabilitaet v10 -> v11:

```text
stable_trace: 132
new_trace_family: 20
```

Nachbarschafts-Konsequenz v11:

```text
beobachtete_verwandtschaft: 3
reifende_verwandtschaft: 8
vorsichtige_verwandtschaft: 1
```

Wichtige Nachbarschaft:

```text
dio_1tmf -> dio_0wv3:
  vorsichtige_verwandtschaft
  similarity: 0.804764
  target_reward: 2.832120
  reference_reward: 14.018907
```

Gespeicherter Memory-Stand nach Probe10:

```text
symbols: 264
sensor_relations: 64
neighbor_consequences: 64

reifende_verwandtschaft: 46
beobachtete_verwandtschaft: 11
vorsichtige_verwandtschaft: 7
```

Fachlicher Befund:

```text
Probe10 zeigt die Aehnlichkeitsgrenze:
Eine weiter entfernte Welt wird nicht sofort als bekannte Handlungswelt
behandelt. DIO_MINI beobachtet zuerst, bildet neue Syntaxfamilien und
laesst nur wenige Familien lokal in Handlung reifen.

Das ist organisch sauberer als ein hartes Pattern-Matching:
Nicht alles Aehnliche wird gehandelt.
Nicht alles Neue wird blockiert.
Ein Teil wird beobachtet, ein Teil reift, ein Teil bleibt ruhig.
```

## Auslagerung Kontaktlagen

Die drei Kontaktlagen werden ab jetzt in einer eigenen Referenzdatei
gefuehrt:

```text
DIO_BAUPLAN\konstruktion\37_KONTAKTLAGEN_REFERENZPROTOKOLL.md
```

Technische Ausgabe:

```text
debug\dio_mini_contact_reference_protocol_v1
```

Speicherpfad im Mini-Memory:

```text
contact_lagen
```

Wichtig:

```text
contact_lagen sind passive Erfahrung.
Sie werden nicht fuer direkte Handlung gelesen.
```

## Konfliktkontakt als Realitaetstrennung

Probe11 erweitert den episodischen Kern um einen wichtigen Fall:

```text
gleiches Formwort
andere Kontaktlage
anderes Erleben
andere Konsequenz
```

Referenz:

```text
debug\dio_mini_sensor_relation_probe11_konfliktkontakt
debug\dio_mini_contact_family_map_konflikt_v1
debug\dio_mini_contact_sentence_trace_v2
DIO_BAUPLAN\konstruktion\37_KONTAKTLAGEN_REFERENZPROTOKOLL.md
```

Kernbeispiel:

```text
dio_0wv3 war in exakter und naher Wiederbegegnung LONG-bestaetigt.
In Probe11 war derselbe Formname zuerst LONG-belastet.
Spaeter wurde derselbe Formname im Konfliktkontakt SHORT-bestaetigt.
```

Fachliche Grenze:

```text
Das ist keine Strategie.
Das ist eine saubere Trennung von:

Formwiedererkennung
Kontaktlage
Erleben
Konsequenz
```

Damit wird verhindert, dass ein Gedanke oder ein alter Formname als
absolute Realitaet behandelt wird.
