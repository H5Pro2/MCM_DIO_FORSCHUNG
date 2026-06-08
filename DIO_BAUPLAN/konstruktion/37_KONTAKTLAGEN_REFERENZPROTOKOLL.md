# Kontaktlagen Referenzprotokoll

Diese Datei beschreibt die passive Kontaktlagen-Schicht von DIO_MINI.

Die Schicht ist keine Strategie und kein Gate. Sie speichert, wie eine
Weltbegegnung getragen wurde:

```text
exakte_wiederbegegnung
nahe_aehnlichkeit
ferne_aehnlichkeit
```

## Zweck

DIO_MINI soll nicht nur einzelne Formfamilien speichern, sondern auch
die Art der Begegnung tragen:

```text
War das derselbe Kontakt?
War es eine nahe Aehnlichkeit?
War es eine ferne Aehnlichkeit, die erst Orientierung brauchte?
```

Die Kontaktlage bleibt passiv. Die Handlung wird nicht direkt daraus
abgeleitet.

## Referenzprotokoll v1

Quelle:

```text
debug\dio_mini_contact_reference_protocol_v1
```

### Exakte Wiederbegegnung

```text
contact_id: kontakt_exakt_probe8_repeat
state: exakte_wiederbegegnung
runs: 4
trades_total: 12
reward_total: 13.834005
contact_reward_sum: 13.834005

direct_positive_action: 3
observation_to_positive_action: 1
held_observation: 3

top_direct_action:
  dio_14eb
  dio_0wv3
  dio_0eh8

top_observation_to_action:
  dio_0szn
```

Deutung:

```text
Der Kontakt war bekannt genug, um schnell positiv reorganisiert zu
handeln.
```

### Nahe Aehnlichkeit

```text
contact_id: kontakt_nah_probe9
state: nahe_aehnlichkeit
runs: 4
trades_total: 13
reward_total: 13.655328
contact_reward_sum: 13.655330

direct_positive_action: 3
observation_to_positive_action: 2
held_observation: 2

top_direct_action:
  dio_14eb
  dio_0wv3
  dio_0szn

top_observation_to_action:
  dio_16kb
  dio_1l2h
```

Deutung:

```text
Die Welt war nicht identisch, aber nah genug, dass vorhandene reifende
und vorsichtige Erfahrung tragend mitwirkte.
```

### Ferne Aehnlichkeit

```text
contact_id: kontakt_fern_probe10
state: ferne_aehnlichkeit
runs: 4
trades_total: 4
reward_total: 4.586545
contact_reward_sum: 4.586544

direct_positive_action: 0
observation_to_positive_action: 3
held_observation: 16

top_direct_action:
  -

top_observation_to_action:
  dio_1tmf
  dio_0y4s
  dio_1gp1
```

Deutung:

```text
Die Welt war weit genug entfernt, dass DIO_MINI nicht sofort handelte.
Erst Beobachtung, neue Syntaxfamilien und lokale Reifung fuehrten zu
wenigen positiven Handlungen.
```

## Speicherzustand

Nach Import in den Mini-Memory:

```text
contact_lagen: 3

exakte_wiederbegegnung: 1
nahe_aehnlichkeit: 1
ferne_aehnlichkeit: 1
```

DIO-eigene Kontaktlagen-Syntax:

```text
kontakt_exakt_probe8_repeat:
  dio_contact_0w23dz5

kontakt_nah_probe9:
  dio_contact_10xiwzq

kontakt_fern_probe10:
  dio_contact_10rb13a
```

Technischer Speicherort:

```text
bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json
  contact_lagen
```

## Mechanische Grenze

Diese Kontaktlagen duerfen nicht als harte Schwelle verwendet werden.

Zulaessig:

```text
Kontaktlage beobachten
Kontaktlage speichern
Kontaktlage in DIO-Syntax verdichten
Kontaktlage spaeter fuer Reflexion und Berichte ausgeben
```

Nicht zulaessig:

```text
Wenn exakte_wiederbegegnung, dann handeln.
Wenn ferne_aehnlichkeit, dann blockieren.
Wenn nahe_aehnlichkeit, dann LONG oder SHORT.
```

## Naechster Ausbau

Der naechste sinnvolle Schritt ist eine eigene DIO-Syntax fuer
Kontaktlagen:

```text
kontakt_exakt_probe8_repeat -> dio_contact_...
kontakt_nah_probe9          -> dio_contact_...
kontakt_fern_probe10        -> dio_contact_...
```

Diese Syntax soll nicht den Menschenbegriff ersetzen, sondern die
Kontaktlage als DIO-eigenes Wort tragbar machen.

Status:

```text
Umgesetzt.
Die Kontaktlage hat jetzt ein eigenes DIO-Wort,
wird aber weiterhin nicht fuer direkte Motorik gelesen.
```

## Diagnosebericht

Kontaktlagen koennen als Bericht ausgegeben werden:

```text
python -m DIO_MINI.report_contact_lagen ^
  --memory bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json ^
  --output-dir debug\dio_mini_contact_lagen_report_v1
```

Aktueller Bericht:

```text
dio_contact_0w23dz5 exakte_wiederbegegnung reward=13.834005 passive_only=1
dio_contact_10xiwzq nahe_aehnlichkeit reward=13.655330 passive_only=1
dio_contact_10rb13a ferne_aehnlichkeit reward=4.586544 passive_only=1
```

## Kontakt-Familien-Landkarte

Kontaktlage und Formfamilie koennen gemeinsam berichtet werden:

```text
python -m DIO_MINI.build_contact_family_map ^
  --contact-report debug\dio_mini_contact_lagen_report_v1\dio_mini_contact_lagen_report.csv ^
  --contact-id kontakt_exakt_probe8_repeat ^
  --debug-root debug\dio_mini_sensor_relation_probe8_negativkontakt_repeat ^
  --output-dir debug\dio_mini_contact_family_map_exakt_v1
```

Ausgaben:

```text
debug\dio_mini_contact_family_map_exakt_v1
debug\dio_mini_contact_family_map_nah_v1
debug\dio_mini_contact_family_map_fern_v1
```

Kurzbefund:

```text
exakte_wiederbegegnung:
  rows: 24
  kontakt_handlung_bestaetigt: 12
  kontakt_beobachtet_reift: 12

nahe_aehnlichkeit:
  rows: 24
  kontakt_handlung_bestaetigt: 13
  kontakt_beobachtet_reift: 11

ferne_aehnlichkeit:
  rows: 56
  kontakt_handlung_bestaetigt: 4
  kontakt_beobachtet_reift: 49
  kontakt_ruhend: 3
```

Deutung:

```text
Exakt und nah tragen viele bestaetigte Handlungen.
Fern traegt hauptsaechlich Beobachtung und lokale Reifung.

Damit wird sichtbar:
DIO_MINI erlebt nicht nur eine Formfamilie,
sondern eine Formfamilie innerhalb einer Kontaktlage.
```

## Kontakt-Satzspur

Aus Kontaktlage und Formfamilie kann eine einfache DIO-Satzspur gebildet
werden:

```text
Kontaktwort + Formwort + Erleben
```

Technischer Baustein:

```text
DIO_MINI\build_contact_sentence_trace.py
```

Ausgabe:

```text
debug\dio_mini_contact_sentence_trace_v1
```

Ergebnis:

```text
sentence_traces: 40
```

Verteilung:

```text
exakte_wiederbegegnung + kontakt_beobachtet_reift:        4
exakte_wiederbegegnung + kontakt_handlung_bestaetigt:     4

nahe_aehnlichkeit + kontakt_beobachtet_reift:              4
nahe_aehnlichkeit + kontakt_handlung_bestaetigt:           5

ferne_aehnlichkeit + kontakt_beobachtet_reift:            19
ferne_aehnlichkeit + kontakt_handlung_bestaetigt:          3
ferne_aehnlichkeit + kontakt_ruhend:                       1
```

Staerkste Satzspuren:

```text
dio_sentence_03q0guk:
  dio_contact_0w23dz5 + dio_14eb -> kontakt_handlung_bestaetigt
  reward_sum: 5.683204
  actions: SHORT:4

dio_sentence_0vkd3n3:
  dio_contact_10xiwzq + dio_14eb -> kontakt_handlung_bestaetigt
  reward_sum: 5.588612
  actions: SHORT:4

dio_sentence_0cx8x5c:
  dio_contact_0w23dz5 + dio_0wv3 -> kontakt_handlung_bestaetigt
  reward_sum: 5.321888
  actions: LONG:4

dio_sentence_0aq7ulj:
  dio_contact_10xiwzq + dio_0wv3 -> kontakt_handlung_bestaetigt
  reward_sum: 5.156112
  actions: LONG:4
```

Mechanische Grenze:

```text
Diese Satzspur ist noch kein Handlungsprogramm.
Sie ist eine lesbare Verdichtung von Erfahrung:

"In dieser Kontaktlage erschien diese Formfamilie
 und wurde so erlebt."
```

## Satzspur im Memory

Die Satzspuren werden passiv im Mini-Memory gespeichert:

```text
DIO_MINI\store_sentence_traces.py
DIO_MINI\report_sentence_traces.py
```

Speicherpfad:

```text
bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json
  sentence_traces
```

Aktueller Speicherstand:

```text
sentence_traces: 40

kontakt_beobachtet_reift: 27
kontakt_handlung_bestaetigt: 12
kontakt_ruhend: 1
```

Bericht:

```text
debug\dio_mini_sentence_trace_report_v1
```

Staerkste gespeicherte Satzspuren:

```text
dio_sentence_03q0guk:
  dio_contact_0w23dz5 + dio_14eb -> kontakt_handlung_bestaetigt
  reward_sum: 5.683204

dio_sentence_0vkd3n3:
  dio_contact_10xiwzq + dio_14eb -> kontakt_handlung_bestaetigt
  reward_sum: 5.588612

dio_sentence_0cx8x5c:
  dio_contact_0w23dz5 + dio_0wv3 -> kontakt_handlung_bestaetigt
  reward_sum: 5.321888

dio_sentence_0aq7ulj:
  dio_contact_10xiwzq + dio_0wv3 -> kontakt_handlung_bestaetigt
  reward_sum: 5.156112
```

Status:

```text
Umgesetzt.
Die Satzspur ist gespeichert und berichtbar,
wird aber nicht von der Motorik gelesen.
```

## Lesemodus fuer Formfamilien

Zu einer Formfamilie kann DIO_MINI jetzt bekannte Satzspuren lesen:

```text
DIO_MINI\read_form_sentence_traces.py
```

Beispiel Kernfamilien:

```text
python -m DIO_MINI.read_form_sentence_traces ^
  --memory bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json ^
  --family dio_0wv3 ^
  --family dio_14eb ^
  --output-dir debug\dio_mini_form_sentence_read_core_v1
```

Befund:

```text
dio_0wv3:
  dio_sentence_0cx8x5c
    exakte_wiederbegegnung -> kontakt_handlung_bestaetigt
    reward_sum: 5.321888
    actions: LONG:4

  dio_sentence_0aq7ulj
    nahe_aehnlichkeit -> kontakt_handlung_bestaetigt
    reward_sum: 5.156112
    actions: LONG:4

dio_14eb:
  dio_sentence_03q0guk
    exakte_wiederbegegnung -> kontakt_handlung_bestaetigt
    reward_sum: 5.683204
    actions: SHORT:4

  dio_sentence_0vkd3n3
    nahe_aehnlichkeit -> kontakt_handlung_bestaetigt
    reward_sum: 5.588612
    actions: SHORT:4
```

Beispiel ferne Familien:

```text
debug\dio_mini_form_sentence_read_fern_v1

dio_0ux2:
  ferne_aehnlichkeit -> kontakt_beobachtet_reift

dio_1tmf:
  ferne_aehnlichkeit -> kontakt_handlung_bestaetigt
  ferne_aehnlichkeit -> kontakt_beobachtet_reift
```

Deutung:

```text
DIO_MINI kann jetzt lesen:
"Dieses Formwort kenne ich in diesen Kontaktlagen mit diesem Erleben."

Das ist weiterhin keine Entscheidungsschicht.
Es ist ein passiver Lesemodus fuer eigene Erfahrung.
```

## Probe11 - Konfliktwiederbegegnung

Neue Quelle:

```text
data\kontrolliert_sensor_relation_probe11_konfliktkontakt_2episoden_5m_SOLUSDT.csv
debug\dio_mini_contact_reference_protocol_probe11_v1
debug\dio_mini_contact_family_map_konflikt_v1
debug\dio_mini_contact_sentence_trace_v2
```

Kontakt:

```text
contact_id: kontakt_konflikt_probe11
contact_symbol: dio_contact_0iicj44
state: konflikt_wiederbegegnung
runs: 4
trades_total: 7
reward_total: -1.579871
contact_reward_sum: 2.146809

direct_positive_action: 1
observation_to_positive_action: 2
held_observation: 11
quiet_family: 1
```

Deutung:

```text
Eine bekannte Form-/Kontaktnaehe trifft auf eine andere reale Konsequenz.
Der Kontakt ist nicht einfach positiv oder negativ.
Er enthaelt alte Handlungsnaehe, neue Belastung und spaetere Reorganisation.
```

Wichtiges Beispiel:

```text
dio_0wv3:
  alte Satzspuren:
    exakte_wiederbegegnung -> kontakt_handlung_bestaetigt -> LONG
    nahe_aehnlichkeit -> kontakt_handlung_bestaetigt -> LONG

  neue Konfliktspur:
    konflikt_wiederbegegnung -> kontakt_handlung_belastet -> LONG
    konflikt_wiederbegegnung -> kontakt_handlung_bestaetigt -> SHORT
```

Konkrete Zeilen:

```text
RUN 116, tick 1:
  dio_0wv3
  action: LONG
  best_action_training: SHORT
  reward: -1.763340

RUN 119, tick 1:
  dio_0wv3
  action: SHORT
  best_action_training: SHORT
  reward: 1.563340
```

Mechanischer Befund:

```text
Ein Formwort ist nicht die Realitaet.
Ein Formwort ist eine verdichtete Wiedererkennung.

Erst Kontaktlage, Erleben und Konsequenz entscheiden,
wie diese Wiedererkennung im Gedaechtnis getragen wird.
```

Speicherstand nach Probe11:

```text
contact_lagen: 4
sentence_traces: 59
```

Neue Satzspuren fuer `dio_0wv3`:

```text
dio_sentence_0cx8x5c:
  exakte_wiederbegegnung
  kontakt_handlung_bestaetigt
  reward_sum: 5.321888
  actions: LONG:4

dio_sentence_0aq7ulj:
  nahe_aehnlichkeit
  kontakt_handlung_bestaetigt
  reward_sum: 5.156112
  actions: LONG:4

dio_sentence_0g19qiw:
  konflikt_wiederbegegnung
  kontakt_handlung_bestaetigt
  reward_sum: 1.563340
  actions: SHORT:1

dio_sentence_0sxgj20:
  konflikt_wiederbegegnung
  kontakt_handlung_belastet
  reward_sum: -5.290020
  actions: LONG:3
```

Grenze:

```text
Diese Information darf nicht direkt Motorik ausloesen.
Sie ist eine passive Realitaetstrennung:

Ich sehe eine bekannte Form.
Diese Begegnung fuehlt sich anders an.
Meine alte Handlung hat diesmal nicht getragen.
Eine andere Handlung wurde spaeter positiv bestaetigt.
```

## Passive Konfliktlesung

Neues Lesewerkzeug:

```text
DIO_MINI\read_sentence_conflicts.py
```

Ausgabe:

```text
debug\dio_mini_sentence_conflict_read_v1
```

Befund:

```text
families: 43
conflicts: 1

dio_0wv3:
  state: form_erleben_konflikt
  positive_reward_sum: 12.041340
  burden_reward_sum: -5.290020
  actions: LONG:11,SHORT:1
```

Deutung:

```text
Eine Familie kann gleichzeitig positive und belastete Satzspuren tragen.
Das ist kein Fehler.
Es ist der Hinweis:

"Ich kenne diese Form,
aber ich kenne sie nicht mehr eindeutig."
```

Grenze:

```text
Die Konfliktlesung bleibt passiv.
Sie ist kein Gate und keine Strategie.
Sie macht nur sichtbar, wo Erfahrung differenziert werden muss.
```

## Erfahrungslandschaft

Neues Berichtswerkzeug:

```text
DIO_MINI\report_experience_landscape.py
debug\dio_mini_experience_landscape_v1
```

Aktueller Befund:

```text
Konfliktfamilien: 1
Bestaetigte Familien: 11
Belastete Familien: 0
Beobachtende Familien: 31
```

Lesart:

```text
Die Kontaktlagen- und Satzspur-Schicht ist jetzt nicht nur speicherbar,
sondern als einfache innere Erfahrungslandschaft lesbar.

Das beantwortet passiv:

Welche Form ist bestaetigt?
Welche Form ist widerspruechlich?
Welche Form bleibt Beobachtung?
```

Grenze:

```text
Auch die Erfahrungslandschaft ist nicht Motorik.
Sie ist ein Diagnosebild des inneren Speichers.
```

## Probe12 - Bestaetigte Sensorvarianz

Neue Quelle:

```text
data\kontrolliert_sensor_relation_probe12_short_reife_varianz_2episoden_5m_SOLUSDT.csv
debug\dio_mini_contact_reference_protocol_probe12_v1
debug\dio_mini_contact_family_map_sensorvarianz_v1
debug\dio_mini_contact_sentence_trace_v3
```

Kontakt:

```text
contact_id: kontakt_sensorvarianz_probe12
contact_symbol: dio_contact_0tb1y1t
state: bestaetigte_sensorvarianz
runs: 4
trades_total: 11
reward_total: 6.776098
contact_reward_sum: 8.440308

direct_positive_action: 2
held_observation: 7
```

Deutung:

```text
Eine bekannte Reifespur wird nicht exakt wiederholt,
sondern unter leicht veraenderter Sensorik neu erlebt.
```

Wichtige Familien:

```text
dio_14eb:
  bestaetigte_sensorvarianz
  kontakt_handlung_bestaetigt
  reward_sum: 5.623700
  actions: SHORT:4

dio_0szn:
  bestaetigte_sensorvarianz
  kontakt_handlung_bestaetigt
  reward_sum: 2.816608
  actions: SHORT:4
```

Stabilitaetsbefund:

```text
dio_14eb ist jetzt ueber drei Kontaktlagen SHORT-bestaetigt:

exakte_wiederbegegnung
nahe_aehnlichkeit
bestaetigte_sensorvarianz
```

Gleichzeitig bleibt `dio_0wv3` Konfliktfamilie.
Das ist wichtig: neue Sensorik macht nicht automatisch alles positiv.

Grenze:

```text
Auch bestaetigte_sensorvarianz ist keine Handlungsregel.
Sie beschreibt nur:
"Diese Art der veraenderten Begegnung wurde positiv getragen."
```

## Passive Stabilitaetslesung

Neues Lesewerkzeug:

```text
DIO_MINI\read_stable_direction_traces.py
debug\dio_mini_stable_direction_traces_v2
```

Aktueller Befund:

```text
families: 49
kontaktlagenuebergreifend_bestaetigt: 2
lokal_bestaetigt: 9
conflict_or_burden: 1
```

Kontaktlagenuebergreifend bestaetigt:

```text
dio_14eb:
  stable_action: SHORT
  positive_contact_count: 3
  positive_reward_sum: 16.895516

dio_0szn:
  stable_action: SHORT
  positive_contact_count: 3
  positive_reward_sum: 7.014025
```

Deutung:

```text
Diese Familien sind nicht nur lokal positiv.
Sie tragen dieselbe Richtung ueber mehrere Kontaktlagen.
```

Grenze:

```text
Auch das ist keine Strategie.
Die Lesung beschreibt nur stabile Erfahrungsspuren.
```

## Probe13 - Verschobene Sensorvarianz

Neue Quelle:

```text
data\kontrolliert_sensor_relation_probe13_short_reife_varianz_shift_2episoden_5m_SOLUSDT.csv
debug\dio_mini_contact_reference_protocol_probe13_v1
debug\dio_mini_contact_family_map_sensorvarianz_shift_v1
debug\dio_mini_contact_sentence_trace_v4
```

Kontakt:

```text
contact_id: kontakt_sensorvarianz_probe13_shift
contact_symbol: dio_contact_00ebb6g
state: verschobene_sensorvarianz
runs: 4
trades_total: 5
reward_total: 6.009557
contact_reward_sum: 6.009556

observation_to_positive_action: 3
held_observation: 15
```

Deutung:

```text
Die Welt ist aehnlich genug, um positive lokale Kontakte zu bilden,
aber verschoben genug, dass sie nicht einfach als alte Familie gelesen wird.
```

Neue lokale Familien:

```text
dio_0hd3:
  kontakt_handlung_bestaetigt
  action: SHORT
  reward_sum: 2.918570

dio_0c6o:
  kontakt_handlung_bestaetigt
  action: LONG
  reward_sum: 2.296328

dio_1wie:
  kontakt_handlung_bestaetigt
  action: SHORT
  reward_sum: 0.794658
```

Befund:

```text
Die Kontaktlagen-Schicht zeigt jetzt zwei unterschiedliche Arten von
Sensorvarianz:

bestaetigte_sensorvarianz:
  bekannte Familien werden erneut bestaetigt.

verschobene_sensorvarianz:
  neue lokale Familien entstehen aus Beobachtung.
```

Grenze:

```text
Auch verschobene_sensorvarianz bleibt passiv.
Sie ist eine Speicher- und Leselage, kein Entry-Ausloeser.
```
