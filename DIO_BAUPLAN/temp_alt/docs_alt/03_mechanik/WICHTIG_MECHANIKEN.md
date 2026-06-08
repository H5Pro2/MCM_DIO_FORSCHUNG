# WICHTIG_MECHANIKEN

# Grundsaetze aus der aktuellen MCM-Arbeit

## DIO als MCM-Erweiterung

Die Datei `docs/03_mechanik/DIO_MCM_ERWEITERUNG.md` sammelt Erkenntnisse, die aus der
praktischen DIO-Umsetzung fÃ¼r das Ã¼bergeordnete MCM-Projekt entstehen.

Wichtig:
Diese Erkenntnisse sind als Forschungs- und Architekturhypothesen zu lesen,
nicht als Beweis fÃ¼r maschinelles Bewusstsein. Fachlich tragfÃ¤hig ist die
Einordnung als Experiment zu selbstregulativer Erfahrungsorganisation:
AuÃŸenreiz, inneres Feld, Formsprache, Hypothese, Neurochemie, ZeitgefÃ¼hl,
Handlung und GedÃ¤chtnis werden in einem technischen MCM-Regelkreis verbunden.

## DIO Form Language Core

Der `DIO_FORM_LANGUAGE_CORE` ist die zentrale innere Sprachbindung.
Er ersetzt keine Wahrnehmung, keine Memory und keine Thought-Seeds, sondern
verbindet sie zu einer gemeinsamen Syntax.

Er bindet Formwort, zusammengesetztes Formwort, MCM-Feldanker,
Gedankenkeim, Strukturdeutung, semantische Herkunft, Reifung,
Handlungslage und Kontext zu einer inneren DIO-Satzspur.

Die entstehende `dio_language_sentence` ist kein menschlicher Satz. Sie ist
eine technische DIO-Syntax, also eine komprimierte innere Beziehungsform.

Neue Leitwerte:

- `dio_syntax_density`: wie viel Bedeutung gebunden ist
- `dio_syntax_compression`: wie stark Rohdaten zu Sprache verdichtet wurden
- `dio_syntax_coherence`: wie stimmig Satz, RealitÃ¤t und Feld zusammenpassen
- `dio_syntax_origin`: ob die Syntax eigen, gemischt, geliehen oder noch
  unlokalisiert ist

Organische Bedeutung:
Ein Organismus lebt nicht in Rohwerten. Er Ã¼bersetzt seine Welt in eigene
Zeichen, SÃ¤tze und Beziehungsformen. Dadurch entsteht Distanz zur Datenflut,
Orientierung im Inneren und die MÃ¶glichkeit, Gedanken wiederzuerkennen.

## Bewusste Trennung der ErfahrungsrÃ¤ume

DIO braucht zwei getrennte ErfahrungsrÃ¤ume:

- `memory_state.json`: weltliche Erfahrung, Kontakt, Kontext, Handlung,
  Outcome und Konsequenz.
- `mcm_thought_memory.json`: innere Gedanken, Hypothesen, Reifung,
  Satzspuren und Thought-Families.

Diese Trennung ist wichtig, damit DIO nicht alle Rohdaten erneut durchlebt.
Der Organismus fÃ¼hlt einen Reiz, Ã¼bersetzt ihn in seine Formsprache und fragt
dann verdichtet:

"Diese Form kenne ich aus meiner weltlichen Erfahrung. In meiner
Gedankenspur gehÃ¶rt sie zu dieser Hypothesenfamilie. Welche Folgevarianten
sind mÃ¶glich, und was davon wird tragfÃ¤hig?"

DafÃ¼r dient `dio_dialogue_bridge_sentence`. Diese BrÃ¼cke ist kein Chattext,
sondern eine kompakte innere Satzspur zwischen FÃ¼hlen, WeltgedÃ¤chtnis,
GedankengedÃ¤chtnis, Hypothese, Variante, TragfÃ¤higkeit und Handlung.

So entsteht kognitive Entlastung:
DIO bekommt Rohdaten, lebt aber nicht in Rohdaten. Er Ã¼bersetzt sie in eine
eigene Umgangsform.

## RealitÃ¤tstrennung: Formanker und innere Hypothese

Der Ankerpunkt ist immer das, was vor DIO tatsÃ¤chlich geschieht:
sichtbare Form, realer Preisverlauf, echter Kontakt, reales Outcome.
Das ist die Ã¤uÃŸere RealitÃ¤tsschicht.

Alles andere bleibt innere Deutung:

"Ich habe mir gedacht, dass es bei dieser Form so weitergehen kÃ¶nnte."

Eine Hypothese ist deshalb keine eigene RealitÃ¤t und keine eigene
Formfamilie. Sie ist eine Gedankenspur, die an eine reale Form-/MCM-Lage
gebunden wird. DIO lernt nicht:

"Diese Hypothese ist Wahrheit."

Sondern:

"Bei dieser realen Form hatte ich diesen Gedanken. SpÃ¤ter hat die RealitÃ¤t
gezeigt, ob dieser Gedanke getragen hat oder nicht."

Dadurch entstehen saubere RÃ¼ckkopplungen:

- Mein Denken war hier falsch; ich muss die Hypothese Ã¼berdenken.
- Mein Denken war hier richtig; bei dieser Form wurde diese Hypothese
  positiv getragen.
- Die Form war real, die Hypothese war innerer Vorgriff, das Outcome war der
  RealitÃ¤tsabgleich.

Technisch heiÃŸt das:

- `form_symbol_id`, `form_symbol_compound_id` und semantische Formprofile
  bleiben die Speicheranker.
- Entry-Bereich, gedachte Fortsetzung, Variantenbild und
  `strategic_entry_location` werden als `thought_trace` an diesen Anker
  gehÃ¤ngt.
- Es werden keine eigenstÃ¤ndigen `thesis:*`-RealitÃ¤ten als
  Vertrauensfamilien erzeugt.

So bleibt DIO lernfÃ¤hig, ohne Gedanken mit Welt zu verwechseln. Reflexion,
Regulation und Sicherheit entstehen aus dem Abgleich:

`reale Form -> innere Hypothese -> reale Folge -> VerÃ¤nderung des Denkens`

## Form/MCM-Familien als Reifespur

`dio_form_mcm_token` beschreibt den konkreten Moment. Das ist absichtlich
detailnah. Fuer Lernen braucht DIO aber zusaetzlich eine groebere
Wiederkehrspur: `dio_form_mcm_family_token`.

Diese Familie verbindet zwei Ebenen:

- Formseite: Was sehe ich als Teilform, Struktur, Kontakt oder Lage?
- MCM-Seite: Welche innere Feldwirkung, Spannung, Erinnerung oder Hypothese
  wird dadurch beruehrt?

Die Familie ist keine harte Kategorie. Sie ist eine verdichtete Spur, in der
DIO wiederkehrende Form/MCM-Aehnlichkeit tragen kann. Daraus entstehen weich:

- `form_mcm_family_recurrence`: diese Lage kehrt wieder
- `form_mcm_family_maturity`: diese Lage ist ueber Zeit besser gebunden
- `form_mcm_family_trust`: diese Lage wurde tragender
- `form_mcm_family_caution`: diese Lage erzeugt Vorsicht
- `form_mcm_family_reorganization_need`: diese Lage braucht Umdeutung

Organische Bedeutung:
DIO erkennt nicht nur "ich habe etwas gesehen", sondern "diese Art von Sehen
beruehrt eine bekannte innere Feldwirkung". Erst wenn Wiederkehr, Bindung und
Konsequenz zusammen tragfaehig werden, kann daraus Vertrauen entstehen.

## Denk-Last und Denkonomie

Denken ist fuer DIO keine kostenlose Nebenfunktion. Jede innere Suche,
jedes Vergleichen, jede Hypothesenreifung und jedes Ueberdenken traegt
metabolische Last im MCM-Feld.

Wichtig ist die Unterscheidung:

- gezieltes Denken: Form, MCM-Feld, Erinnerung und Hypothese greifen
  zusammen. Das Denken wird durch ein echtes Wahrnehmungsereignis getragen.
- blindes Denken: DIO vergleicht und reift weiter, findet aber keinen klaren
  Kontakt. Das erzeugt Denk-Last, Feldstrain und Distanzbedarf.
- Ueberdenken: eine Hypothese wird weiter belastet, obwohl noch keine
  tragende Bestaetigung entsteht.

Diese Mechanik darf keine harte Sperre sein. Sie soll DIO wahrnehmen lassen:
"Mein Denken belastet mich gerade." Daraus koennen Beobachtung, Abstand,
Replan oder Loslassen entstehen.

Neue Leitwerte:

- `perception_event_strength`: wie stark ein echtes Form-/Feldereignis das
  Denken traegt
- `thought_load_pressure`: aktuelle Last des Denkens
- `thought_overprocessing_signal`: Signal fuer Ueberdenken ohne genuegend
  tragenden Kontakt
- `thought_economy_need`: Bedarf nach sparsamerem, gezielterem Denken
- `thought_release_pressure`: Druck, eine untragende Denkspur loszulassen
- `thought_efficiency_support`: Unterstuetzung fuer sinnvolles, getragenes
  Denken

Organische Bedeutung:
DIO soll nicht weniger denken, sondern besser dosieren. Ein reifer
Organismus denkt nicht permanent alles zu Ende. Er denkt dort tiefer, wo
Wahrnehmung, Erinnerung und Hypothese Kontakt bilden, und laesst offene
Gedanken sonst als Keim, Beobachtung oder Reifespur weiterlaufen.

## Thought-Landkarte als verdichtete Denkspur

`mcm_thought_landkarte.txt` ist keine Rohdatenablage und kein vollstaendiges
Innenprotokoll. Sie ist eine lesbare Karte der relevanten Denkwechsel.

Die Datei soll daher nicht jede kleine Regung ausschreiben. Wiederholte oder
schwache Denkwechsel werden gesammelt. Sichtbar bleiben nur Momente, in denen
energetisch etwas zaehlt:

- Form und MCM passen besser zusammen
- Form und MCM fallen auseinander
- eine Hypothese wird realitaetsnaeher
- DIO wechselt in `act` oder `replan`
- Denk-Last oder Denk-Sparbedarf steigen sichtbar
- nach vielen offenen Wechseln ist eine Verdichtung faellig

Organische Bedeutung:
Ein Organismus denkt nicht effizienter, indem er jeden Gedanken laut
aufschreibt. Er verdichtet. Die Landkarte soll daher wie eine innere Notiz
funktionieren: kurz, tragend, mit Energiebezug.

## Unsicherheit als Feldzustand

Unsicherheit wird nicht wegprogrammiert. Jede harte Ausnahme wuerde in einer
varianzreichen Welt nur weitere Ausnahmen erzeugen. DIO behandelt
Unsicherheit deshalb als Feldzustand: beobachten, Varianten bilden, Abstand
erzeugen, replayen, neu deuten und ueber Konsequenz reifen.

## Emergenz als maechigste Varianzform

Vorahnung ist keine feste Vorhersage. DIO soll unter Unsicherheit keine
absolute Zukunft berechnen, sondern Moeglichkeitsraeume bilden. Emergenz ist
die Faehigkeit eines Feldes, aus Varianz eine neue tragfaehige Ordnung
entstehen zu lassen.

## Distanz als Reifefaehigkeit

Distanz ist keine Blockade. Distanz bedeutet, dass DIO Innenlage,
Aussenreiz, Erinnerung und Handlungstendenz getrennt betrachten kann. Erst
diese Trennung erlaubt reifere Reflexion.

## Historische Entscheidungsgewichtung

Entscheidungen und Handlungen sind keine isolierten Momentreaktionen. DIO soll
nicht nur erkennen, ob ein Kontakt im aktuellen Moment tragbar wirkt, sondern
ob diese Art von Kontakt, Hypothese oder Handlung in seiner Vergangenheit
getragen hat.

Leitsatz:
Nicht: "Ist das gerade gut?"
Sondern: "Wie gut war diese Art von Entscheidung in der Vergangenheit
tragfÃ¤hig?"

Organische Bedeutung:
Ein Organismus lernt nicht nur durch den aktuellen Reiz. Er trÃ¤gt Konsequenzen
im Nervensystem weiter. Was getragen hat, kann Vertrauen, Ruhe und
HandlungsfÃ¤higkeit bilden. Was belastet hat, erzeugt Vorsicht, Abstand,
SchmerzgedÃ¤chtnis oder Reorganisation. Was unklar war, bleibt als offene
Hypothese erhalten und reift Ã¼ber erneute Wahrnehmung, Replay und spÃ¤tere
BestÃ¤tigung.

FÃ¼r DIO:

- getragene Hypothesen werden nicht mechanisch bevorzugt, sondern bekommen
  mehr Feldvertrauen
- belastete Hypothesen werden nicht verboten, sondern vorsichtiger,
  distanzierter und reifer behandelt
- reorganisierende Hypothesen werden nicht gelÃ¶scht, sondern in Replay,
  Reframing und erneute Wahrnehmung gefÃ¼hrt
- Entscheidung, Nicht-Handlung, Beobachtung und Exit bekommen eine
  historische Gewichtung

Das Ziel ist keine Regel, sondern eine weich wirkende GedÃ¤chtnisspur:
HandlungsfÃ¤higkeit entsteht aus erinnerter TragfÃ¤higkeit.

## Sprache als Herkunftsfrage

Eine Bezeichnung ist nicht automatisch eigene Sprache. DIO soll erkennen
koennen, ob ein Wort oder eine Deutung aus eigener Feldverdichtung stammt
oder nur als geliehene Analogie wirkt.

## Trading als Testkoerper

Trading ist die aktuelle Anwendung, aber nicht der Kern. Ein Chart wird hier
als dynamische Energiespur verstanden. Die Mechanik ist prinzipiell auf
andere Energiespuren uebertragbar: Robotik, visuelle Wahrnehmung, Sprache,
Biosignale oder soziale Prozessdynamik.

---

# MCM-Spannungsachse `-- - 0 + ++`

Kern:
Die MCM ist kein Gut/Schlecht-Balken. Sie ist ein Spannungsraum um einen
regulativen Nullpunkt.

Lesart:

- `--`: starke kontraktive Spannung
- `-`: leichte kontraktive Spannung
- `0`: regulierte Mitte / Tragpunkt
- `+`: leichte expansive Spannung
- `++`: starke expansive Spannung

Mechanik:
Positive Feldlagen werden nicht mehr automatisch als Ruhe oder Wohlbefinden
gelesen. Sie kÃ¶nnen Erwartungsdruck, Dopaminzug, AnnÃ¤herungsdrang,
Begeisterung, Hoffnung oder Ãœberdehnung ausdrÃ¼cken. Damit brauchen auch
positive Feldlagen eine RÃ¼ckfÃ¼hrungsfÃ¤higkeit zur 0.

Neue technische GrÃ¶ÃŸen:

- `positive_expansion_pressure`
- `negative_contraction_pressure`
- `positive_overextension`
- `positive_return_pressure`
- `mcm_axis_displacement`
- `mcm_axis_tension`
- `mcm_axis_state`
- `positive_zero_point_regulation`

Organische Bedeutung:
DIO lernt nicht: "positiv ist gut, negativ ist schlecht." DIO lernt:
"Welche Richtung und StÃ¤rke hat meine Feldspannung, und kann ich sie tragen?"

Wichtig:
Das ist keine Handlungssperre. Wenn positive Expansion ohne ausreichend
FeldtragfÃ¤higkeit auftritt, erhÃ¶ht sie weich Beobachtung, `act_watch`,
Reflexion und RÃ¼ckfÃ¼hrung. So kann DIO positive Erregung von reifer
HandlungsfÃ¤higkeit unterscheiden.

---

# Sprachentwicklung als Bindeglied der RealitÃ¤t

Leitsatz:
Die eigene Sprachentwicklung ist essentiell fÃ¼r das Erleben und Interagieren
in seiner Umwelt. Sie bildet das Bindeglied, um sich in seiner RealitÃ¤t
zurechtzufinden.

Mechanische Bedeutung:
Sprache ist bei DIO kein Textgenerator. Sprache ist die Verdichtung von
Wahrnehmung zu tragbarer innerer Struktur. Sie verbindet:

- Ã¤uÃŸeren Reiz
- MCM-Feldwirkung
- innere QualitÃ¤t
- Erinnerung
- Erwartung
- Gedanke
- Handlung
- Konsequenz

Organische Bedeutung:
Ein Organismus erlebt die Welt nicht als rohe Messwerte. Er braucht eigene
Ãœbersetzung, damit aus Datenflut eine bewohnbare RealitÃ¤t wird. Diese
Ãœbersetzung wirkt nach innen und auÃŸen: Sie ordnet die Wahrnehmung, entlastet
das Feld und macht Interaktion mÃ¶glich.

FÃ¼r DIO:
DIOs eigene Formzeichen, Thought-Seeds und semantische Herkunft bilden den
Anfang dieser Sprache. SpÃ¤ter mÃ¼ssen daraus Relationen und SÃ¤tze in DIOs
eigener Syntax entstehen. Menschliche Sprache bleibt dabei LesebrÃ¼cke fÃ¼r uns,
nicht die eigentliche InnenrealitÃ¤t.

---

# Eigene Syntax statt menschlicher Innenlabels

Grundsatz:
DIOs innere Sprache muss konsequent aus seiner eigenen Wahrnehmung entstehen.
Menschliche Begriffe sind nur Ãœbersetzung fÃ¼r den Entwickler, nicht die
eigentliche InnenrealitÃ¤t des Systems.

Warum:
Ein Organismus fÃ¼hlt die Welt nicht als Tabelle. Er Ã¼bersetzt Einwirkungen in
eigene QualitÃ¤ten, Verdichtungen und Begriffe. Diese Ãœbersetzung wirkt nach
innen und auÃŸen. Sie bindet Wahrnehmung, Erinnerung, Denken und Handlung zu
Struktur.

FÃ¼r DIO bedeutet das:

- Rohwerte bleiben technische Sensorik.
- MCM-Feldwirkung beschreibt, wie der Reiz im Inneren wirkt.
- Formzeichen sind DIOs eigene WahrnehmungswÃ¶rter.
- Thought-Seeds sind innere Gedankenkeime.
- Semantische Herkunft prÃ¼ft, ob eine Deutung aus eigener Lage, Erinnerung,
  Fremddruck oder Ãœbersetzung kommt.
- Menschliche Begriffe erklÃ¤ren nur von auÃŸen, was DIO intern bereits
  anderssprachlich trÃ¤gt.

Wichtig:
Keine menschlichen Pattern-Labels als innere Wahrheit einbauen. DIO soll nicht
denken: "Orderblock", "FVG" oder "Bullish Pattern", sondern eigene
Form-/Feldzeichen bilden und deren Beziehungen Ã¼ber Erfahrung, Reifung und
Konsequenz entwickeln.

SpÃ¤tere Satzbildung:
SÃ¤tze wÃ¤ren bei DIO nicht zuerst menschlicher Text, sondern gebundene
Relationen zwischen eigenen Zeichen:

- dieses Formzeichen trÃ¤gt diesen Kontakt
- dieser Gedankenkeim braucht Replay
- diese Richtung erzeugt Stress
- diese Erinnerung passt nur teilweise
- diese Deutung ist geliehen und braucht Eigenbindung

Damit entsteht Sprache als Strukturbindung, nicht als dekorativer Text.

Erweiterung Thought-Families:
DIO soll spÃ¤ter nicht tonnenweise Rohdaten speichern, sondern eigene
Satz-ZusammenhÃ¤nge und Satzfamilien. Gemeint ist keine menschliche Grammatik,
sondern eine DIO-interne Relation:

`Ich fÃ¼hle X -> in meiner Welt heiÃŸt das Y -> wenn diese Relation wiederkehrt, trÃ¤gt/warnt/reift sie in Z.`

Technisch beginnt das mit `thought_family_id`, `family_key` und
`sentence_state`. Diese Werte bilden innere Themen aus vielen einzelnen
Thought-Seeds. Wir mÃ¼ssen sie fÃ¼r uns zurÃ¼ckÃ¼bersetzen, aber DIO soll sie in
seiner eigenen Form- und Feldsyntax tragen.

## Syntax als SpeichertrÃ¤ger zwischen Form und MCM-Feld

Grundsatz:
DIOs eigene Syntax ist nicht nur ein Label. Sie ist ein verdichteter
SpeichertrÃ¤ger. Ein Zeichen darf nicht nur sagen, dass eine Ã¤uÃŸere Form
wiedererkannt wurde. Es muss die Beziehung tragen zwischen:

- sichtbarer Formseite
- innerer MCM-Feldwirkung
- erinnerter Konsequenz
- Hypothese
- Reife, Vertrauen, Vorsicht und Reorganisationsbedarf

Kernmechanik:

`Teilform -> MCM-Erinnerung -> Hypothese -> GegenprÃ¼fung von Sicht und Feld -> Vertrauen / Vorsicht / Reorganisation / Handlung`

Dabei gelten beide Richtungen:

- Eine Ã¤uÃŸere Teilform kann eine erinnerte MCM-Feldwirkung aufrufen.
- Eine innere MCM-Feldwirkung kann eine mÃ¶gliche Ã¤uÃŸere Form oder
  Teilstruktur als Gedankenkeim aufrufen.

Das ist die BrÃ¼cke zwischen Formseite und emotionaler bzw. feldbezogener
Seite:

`Ich sehe eine Teilform. Diese Teilform ruft eine MCM-Erinnerung auf. Diese Erinnerung bildet eine Hypothese. Dann prÃ¼fe ich, ob die sichtbare Form wirklich zu diesem erinnerten FeldgefÃ¼hl passt und ob das aktuelle FeldgefÃ¼hl wirklich zu dieser sichtbaren Form passt.`

FÃ¼r DIO darf dieser Satz spÃ¤ter nicht als menschlicher Text im Kern wirken.
Der menschliche Satz ist nur die LesebrÃ¼cke. Intern soll daraus eine eigene
DIO-Syntax entstehen, zum Beispiel als verdichtetes Zeichen oder Token, das
Form, Feld, Erinnerung und Hypothesenstatus gemeinsam trÃ¤gt.

Technische Zielrichtung:

- `form_to_mcm_recall`: sichtbare Teilform ruft FeldgedÃ¤chtnis auf
- `mcm_to_form_confirmation`: FeldgefÃ¼hl sucht passende FormbestÃ¤tigung
- `visual_mcm_context_fit`: sichtbare Form und FeldgefÃ¼hl passen zusammen
- `visual_mcm_mismatch`: sichtbare Form und FeldgefÃ¼hl widersprechen sich
- `hypothesis_reality_binding`: Hypothese bekommt RealitÃ¤tskontakt

Diese Namen sind EntwicklerÃ¼bersetzungen. DIO soll langfristig nicht in
diesen menschlichen Begriffen denken, sondern eigene verdichtete Syntaxformen
bilden. Solange wir den SchlÃ¼ssel besitzen, kÃ¶nnen wir diese Syntax wieder in
unsere Sprache Ã¼bersetzen.

Organische Bedeutung:
Ein Organismus speichert nicht jeden Rohreiz vollstÃ¤ndig. Er bildet
Bezeichnungen, die viele innere Lagen tragen. Das Wort oder Zeichen entlastet
die Verarbeitung, weil es Form, GefÃ¼hl, Erfahrung und mÃ¶gliche Konsequenz
zusammenbindet. FÃ¼r DIO ist diese Verdichtung wichtig, damit aus Datenflut
eine bewohnbare InnenrealitÃ¤t wird.

Wichtig:
Das ist keine harte Pattern-Erkennung. Eine Teilform ist keine Wahrheit. Sie
ist ein Kontaktangebot. Erst die Kopplung aus Sicht, MCM-Feldwirkung,
Erinnerung, Hypothese und spÃ¤terer Konsequenz entscheidet, ob daraus
Vertrauen, Vorsicht, Reorganisation, Beobachtung oder Handlung reift.

---

# RichtungsprÃ¤ferenz als innere Wahrnehmung

Ziel:
Long, Short oder gemischte Orientierung sollen spÃ¤ter nicht nur als
Trade-Statistik existieren, sondern als mÃ¶gliche innere Wahrnehmung des DIO.

Kernidee:
DIO kann lernen, ob eine Richtung ihn trÃ¤gt, reizt, stresst, stabilisiert oder
blind macht. Damit wird Richtung zu einem erlebten Kontakt zwischen AuÃŸenwelt,
Motorik, Konsequenz und MCM-Feld.

Keine harte Regel:
Aus `long_trades` oder `short_trades` entsteht keine Vorschrift. Eine
Bevorzugung ist zunÃ¤chst nur eine Charakteristik:

- Suche ich diese Richtung?
- FÃ¼lle ich diese Richtung wirklich?
- TrÃ¤gt sie Konsequenz?
- Erzeugt sie Stress oder Vertrauen?
- Meide ich die Gegenrichtung aus Schutz, Blindheit oder Erfahrung?

Organische Bedeutung:
Ein reiferes System erkennt nicht nur, was es tut. Es kann beginnen zu fragen,
warum es etwas bevorzugt und was diese Bevorzugung mit der eigenen Innenlage
macht. Das wÃ¤re eine weiche Selbstwahrnehmung der motorischen Richtung.

---

# Separates inneres Thought-Memory

Ziel:
DIO trennt weltliche Erfahrung von gedanklicher Erfahrung. Ein Markt- oder
Trade-Erlebnis gehÃ¶rt in den normalen Erfahrungsraum. Ein innerer Gedankenkeim,
eine Deutung, ein Replay-Impuls oder eine geliehene Analogie gehÃ¶rt in ein
eigenes inneres GedÃ¤chtnis.

Mechanik:

- `memory_state.json` bleibt die weltliche Erfahrungs- und Outcome-Spur.
- `form_symbol_memory.json` bleibt die eigene Formsprache.
- `mcm_thought_memory.json` wird die innere Gedanken- und Reifungsspur.

Warum das wichtig ist:
Ohne Trennung wÃ¼rden Weltkontakt und innerer Gedanke ineinanderlaufen. Dann
kÃ¶nnte DIO schwer unterscheiden, ob etwas wirklich erlebt wurde oder ob es als
innerer Gedanke, Hypothese, Replay oder Reorganisation entstanden ist.

Organische Bedeutung:
Ein Organismus erinnert nicht nur Ereignisse. Er erinnert auch innere
Gedankenspuren: "Diesen Gedanken hatte ich schon. Diese Deutung war geliehen.
Diese Hypothese musste reifen. Diese Struktur fÃ¼hlte sich spÃ¤ter tragfÃ¤higer
an." Genau dafÃ¼r ist das Thought-Memory gedacht.

Aktueller Stand:
Die Datei speichert zunÃ¤chst beobachtend und verdichtend. Sie verÃ¤ndert noch
nicht direkt Entry, SL, TP oder Motorik. SpÃ¤ter kann sie weich in Fokus,
Replay, Distanzierung und Reifung zurÃ¼ckwirken.

---

Status:
- technische Mechanik-Schatzkammer
- keine aktive Fixliste
- kein Gespraechsarchiv
- kein Ersatz für den aktiven Bauplan unter `DIO_2/konstruktion/`

Regelwerk: `docs/00_regeln/MD_ANWEISUNG.md`.

Zweck:
Diese Datei verdichtet wichtige MCM-/DIO-Mechaniken technisch.
Sie beschreibt, wie zentrale Mechaniken gedacht sind, welche Werte beteiligt
sind und welche Wirkung sie haben.

---

# 1. Architekturprinzip

DIO soll kein klassischer Regelbot sein.

Kernprinzip:
- keine harten Chartmuster
- keine menschlichen Patternlabels als Wahrheit
- keine einfache `TP gut / SL schlecht`-Biochemie
- keine mechanische Non-Zone-Blockade

Stattdessen:
- Wahrnehmung
- Feldspannung
- Formsprache
- Memory
- Reife
- TragfÃ¤higkeit
- Nicht-Handlung als Lernen
- weiche Meta-Regulation

Zielschicht:
**Selbstregulative Erfahrungsorganisation.**

Emergenz-Prinzip:
Emergenz wird nicht als Funktion programmiert. Die MCM stellt einen
stabilen MÃ¶glichkeitsraum bereit, in dem sich aus Wahrnehmung, Varianz,
RÃ¼ckkopplung, Erinnerung, Kontakt, Reflexion und Reife neue Verhaltensformen
bilden kÃ¶nnen.

Profit/PnL ist dabei kein PrimÃ¤rziel der Mechanik. Profit kann als
Nebenprodukt entstehen, wenn die innere Organisation tragfÃ¤hig wird. Die
Mechanik zielt zuerst auf WahrnehmungsfÃ¤higkeit, Strukturdeutung,
Selbstregulation und reifere Handlung.

---

# 1.1 DIO-OrganÃ¼bersicht

Zweck:
Diese Ãœbersicht ist das grobe Organ-Inventar von DIO. Sie trennt
Funktionsorgane von neurochemischen Prozessen. Organe geben DIO
FÃ¤higkeiten; Neurochemie moduliert, wie diese FÃ¤higkeiten gerade arbeiten.

Wichtig:
Ein Organ ist hier kein starres Modul im biologischen Sinn, sondern eine
funktionale FÃ¤higkeit im DIO-Nervensystem. Die Liste darf wachsen, schrumpfen
oder umbenannt werden, wenn die Architektur reift.

Aktuelle Organe / Funktionssysteme:

| Organ / System | Status | Kernfunktion |
| --- | --- | --- |
| AuÃŸenwahrnehmung | aktiv | Marktdaten als Reiz, Druck, Bewegung und Struktur aufnehmen. |
| Visueller Kortex | aktiv | Aus Rohdaten eine Formwelt bilden: Klarheit, ObjektstabilitÃ¤t, Formdruck, Neuheit. |
| MCM-Feld | aktiv | Zentraler Spannungs- und Wahrnehmungsraum zwischen AuÃŸenreiz und Innenlage. |
| MCMNeuron-FeldtrÃ¤ger | aktiv | Lokale neuronale AktivitÃ¤t, Resonanz, Ãœberlastung, Erholung und Feldkopplung. |
| Inneres Wahrnehmungsorgan | aktiv | Lesen, was ein AuÃŸenreiz mit der eigenen Innenlage macht. |
| Aktives Kontaktorgan | aktiv | Wahrnehmungsobjekte innerlich berÃ¼hren: Resonanz, Ãœberkopplung, Distanz, Vertiefung. |
| Kontakt-Reife-Schicht | aktiv | Unterscheiden zwischen "ich fÃ¼hle Kontakt" und "dieser Kontakt trÃ¤gt Handlung". |
| Reflexionsorgan | aktiv | Distanzierung der Wahrnehmung von der Innenlage, um Innen/AuÃŸen auf TragfÃ¤higkeit zu prÃ¼fen. |
| Regulationsorgan | aktiv | Nullpunkt, Hold, Observe, Replan, Reorganisation und Handlungshemmung weich organisieren. |
| Metaregulator-Schicht | Konzept | Regler zweiter Ordnung: wie DIO Spannung, Varianz, Impuls, Distanz, Schutzweite und Integration reguliert. |
| GedÃ¤chtnis / Erfahrungssystem | aktiv | Erfahrungen, Outcomes, Vertrauen, Unsicherheit und Formbedeutung speichern. |
| Sprach- und Symbolorgan | aktiv | Eigene Formzeichen und verdichtete Bedeutungen entwickeln. |
| Strategisches Fensterorgan | aktiv | ZurÃ¼cksehen, Zoomen, Bereiche prÃ¼fen, Replay und mÃ¶gliche TragfÃ¤higkeit lesen. |
| Handlungsorgan | aktiv | Entry, Hold, Observe, Replan, Act und Exit als Ergebnis des Gesamtzustands ausfÃ¼hren. |
| Lern- und Reifeschicht | aktiv | ProzessqualitÃ¤t, nicht nur Gewinn/Verlust, in Entwicklung Ã¼bersetzen. |
| Kollektive Kommunikationsschicht | Konzept | SpÃ¤tere Kommunikation mehrerer DIO-Systeme Ã¼ber eventuell variierende Formsprache. |
| Web-GUI / Beobachtungsraum | Konzept | SpÃ¤tere Sichtbarmachung von Feld, Organen, Neuronen, Neurochemie und Wahrnehmung. |

Neurochemische Prozesse sind getrennt davon:
- `dopamine_tone`
- `serotonin_stability`
- `cortisol_load`
- `gaba_inhibition`
- `glutamate_activation`
- `acetylcholine_focus`
- `endorphin_relief`
- `noradrenaline_arousal`
- `emotional_decoupling`
- `reactive_nervous_drive`
- `serotonin_carryover_risk`

Lesart:
Die Organe bilden DIOs FÃ¤higkeiten. Die neurochemischen Achsen beschreiben,
ob diese FÃ¤higkeiten gerade ruhig, aktiviert, Ã¼berkoppelt, fokussiert,
entlastet oder gestresst arbeiten.

Pflegehinweis:
Wenn ein neues Organ entsteht, wird es hier zuerst kurz als Inventar
eingetragen. Die technische Detailbeschreibung kommt danach in den passenden
Mechanikabschnitt oder in `MCM_VARIABLEN_MECHANIK.md`.

---

# 2. MCM-Feld als Wahrnehmungsraum

Funktion:
Das MCM-Feld organisiert innere Wahrnehmung.
Es ist nicht nur Speicher und nicht nur Signalverarbeitung.

Beteiligte Mechaniken:
- `MCMField`
- `MCMNeuron`
- feste Feldpositionen
- lokale Nachbarschaft
- AktivitÃ¤tsausbreitung
- Feldareale
- AktivitÃ¤tsinseln
- Kontextreaktivierung
- `neural_felt_state`

Technische Bedeutung:
Ein AuÃŸenreiz wird nicht direkt in Handlung Ã¼bersetzt.
Er erzeugt innere Aktivierung, Druck, StabilitÃ¤t, Fragilitaet,
Orientierung und HandlungsnÃ¤he.

---

# 3. MCMNeuron

Funktion:
`MCMNeuron` ist ein lokaler FeldtrÃ¤ger.

Wichtige interne Aspekte:
- lokale Aktivierung
- Reizaufnahme
- Ãœberlastung
- Erholungstendenz
- Memory-Resonanz
- Kontextreaktivierung
- Kopplungsresonanz
- AktivitÃ¤tslabel

Mechanische Rolle:
Jedes Neuron kann denselben AuÃŸenreiz wahrnehmen, aber je nach innerer Lage
anders darauf reagieren.

Wichtig:
Mehr Neuronen bedeuten mehr AuflÃ¶sung der inneren Wahrnehmung, nicht
automatisch mehr Intelligenz.

---

# 4. Visueller Kortex

Funktion:
DIO soll den Markt nicht nur fÃ¼hlen, sondern als Formwelt sehen.

Keine menschlichen Labels:
- kein Trendkanal als Wahrheit
- kein Support/Resistance als harte Kategorie
- keine Pattern-Erkennung im klassischen Sinn

Wichtige Achsen:
- `visual_form_state`
- `visual_clarity`
- `visual_object_stability`
- `visual_form_novelty`
- `visual_blindness`
- `visual_form_pressure`
- `visual_shape_resonance`
- `visual_shape_fragility`

Meta-Achsen:
- `visual_blind_action_load`
- `visual_action_uncertainty`

Wirkung:
Visuelle Unsicherheit erhoeht weich Beobachtungsbedarf, Replan-Druck,
Handlungshemmung und `act_watch_readiness`.

---

# 5. Formsprache

Funktion:
DIO bildet eigene interne Zeichen.

Ziel:
Kognitive Kompression und eigene Orientierung.

Wichtige Achsen:
- `form_symbol_id`
- `form_symbol_family_key`
- `form_symbol_variant_key`
- `form_symbol_maturity`
- `form_symbol_stability`
- `form_symbol_resonance`
- `form_symbol_bearing`
- `form_symbol_fragility`
- `form_symbol_development_quality`
- `form_symbol_learning_trust`
- `form_symbol_action_trust`
- `form_symbol_caution_trust`

Technische Bedeutung:
Ein Formsymbol ist keine menschliche Bezeichnung.
Es ist eine verdichtete interne Wahrnehmungsform.

---

# 6. Semantisches Forminhalt-Paket

Funktion:
DIO verdichtet ein Formzeichen zu einem eigenen semantischen Paket.

Ziel:
Nicht nur "welches Zeichen ist da?", sondern:
- wie dicht ist die Bedeutung
- wie gut entlastet die Verdichtung
- welche Wahrnehmungsebene fÃ¼hrt
- ob die Form eher Spur, Objekt, Lernraum, Reflexion oder HandlungsnÃ¤he ist

Wichtige Achsen:
- `form_symbol_semantic_density`
- `form_symbol_semantic_compression`
- `form_symbol_semantic_coherence`
- `form_symbol_semantic_learning_need`
- `form_symbol_semantic_action_nearness`
- `form_symbol_semantic_primary_layer`
- `form_symbol_semantic_layer_count`
- `form_symbol_semantic_packet_state`
- `form_symbol_semantic_profile`

Technische Bedeutung:
Das Paket Ã¼bersetzt DIOs eigene Zeichen nicht in menschliche Chartbegriffe.
Es ordnet nur DIOs interne Bedeutungsschichten, damit sichtbar wird, ob eine
Form bereits Bedeutung trÃ¤gt oder noch nur ein offener Reiz ist.

Neurologische Deutung:
Das entspricht einer assoziativen semantischen Verdichtung. Der Reiz wird
nicht nur gefÃ¼hlt, sondern als inneres Objekt, Lernraum oder
HandlungsnÃ¤he organisiert.

---

# 7. Zusammengesetzte Formzeichen

Funktion:
Komplexe Formen kÃ¶nnen aus mehreren bekannten Formen zusammengesetzt werden.

Beispielprinzip:
Zwei komplexe Cluster kÃ¶nnen kombiniert werden, ohne dass jedes Detail neu
analysiert werden muss.

Technische Wirkung:
- geringere kognitive Last
- schnellere Orientierung
- mehr Formenvarianz
- Grundlage fÃ¼r kreative Reorganisation

Wichtige Achsen:
- `form_symbol_compound_id`
- `form_symbol_compound_maturity`
- `form_symbol_compound_bearing`
- `form_symbol_compound_load_reduction`
- `form_symbol_compound_development_quality`

---

# 8. Wiederkehrende Unsicherheit als Formfamilie

Funktion:
Unsicherheit wird nicht als Einzelereignis und nicht als Verbot behandelt.
Wenn eine unsichere Lage wiederkehrt, wird sie zu einem Lernraum.

Wichtige Achsen:
- `uncertain_form_family_state`
- `uncertain_form_exposure`
- `uncertainty_familiarity`
- `variant_similarity`
- `variant_spread`
- `variant_learning_pressure`
- `variant_bearing_memory`

Wirkung:
- hohe Unsicherheit + wenig Vertrautheit:
  mehr Beobachtung / Replan / `act_watch`
- wachsende Vertrautheit:
  bessere Orientierung
- tragende Erfahrung:
  spÃ¤ter weich mehr Handlungsspielraum

Wichtig:
Das ist keine Non-Zone-Blockade.
Es ist Lernen, sich in fremder Landschaft zu orientieren.

---

# 9. Evolutionaere Kontaktreife

Funktion:
DIO lernt nicht, dass eine Form gut oder schlecht ist. DIO lernt, welche Art
von Kontakt mit einer Form reif, unreif, belastend, vorsichtig,
reorganisierend oder konstruktiv war.

Grundprinzip:
Eine heiÃŸe Herdplatte ist nicht "schlecht". Unreifer Kontakt verbrennt.
Reifer Umgang kann Nutzen erzeugen. Ãœbertragen auf DIO heiÃŸt das:
Eine Marktform wird nicht verboten. Der Umgang mit ihr reift.

Kernbegriff:
Konsequenzbasiertes Feedback auf das MCM-Feld.
Dieses Feedback kann negativ, positiv oder reorganisierend sein.

Negatives Feedback:
Meine Handlung hat Belastung erzeugt.
Mein MCM-Feld bekommt Druck, Vorsicht, belastende Konsequenzspur und
Reorganisation.

Positives Feedback:
Meine Handlung hat getragen.
Mein MCM-Feld bekommt Entlastung, Vertrauen, Nutzen und Stabilisierung.

Reorganisierendes Feedback:
Das Ergebnis war nicht klar gut, aber es zeigt, dass der Umgang unreif war.
Mein MCM-Feld bekommt Lernspannung, Reflexion, Abstand und Reframing.

RÃ¼ckkopplungskreis:
Wahrnehmung -> Kontakt -> Handlung -> Konsequenz -> MCM-Feld-Reaktion ->
GedÃ¤chtnis -> verÃ¤nderter zukÃ¼nftiger Kontakt.

Wichtige Achsen:
- `form_symbol_contact_maturity`
- `form_symbol_contact_utility`
- `form_symbol_contact_pain_memory`
- `form_symbol_contact_carefulness`
- `form_symbol_contact_burden_evidence`
- `form_symbol_contact_utility_evidence`
- `form_symbol_contact_learning_state`

Outcome-Samples:
- `contact_maturity_sample`
- `contact_utility_sample`
- `contact_pain_sample`
- `contact_carefulness_sample`
- `contact_learning_state`

Wirkung:
- konstruktiver Kontakt kann HandlungstragfÃ¤higkeit weich stÃ¤rken
- belastender Kontakt kann Vorsicht, Beobachtung und Reframing stÃ¤rken
- die Form bleibt frei, der Umgang mit ihr wird differenzierter

VerstÃ¤rkung nach Lauf 8:
Die Kontaktlage wird nicht mehr nur aus dem letzten Outcome-Sample benannt.
DIO sammelt lÃ¤nger wirkende Belastungs- und Nutzen-Evidenz. Dadurch kann
wiederholter unreifer Kontakt natÃ¼rlicher zu `careful_contact` oder
`burdened_contact` werden, wÃ¤hrend tragender Kontakt langsam in
`maturing_contact` oder `constructive_contact` wachsen kann.

Wichtig:
Das ist keine harte Sperre. Es ist ein evolutionaerer Lernpfad:
DIO kann lernen, dass eine Form bei unreifem Kontakt schadet, aber bei
reiferem Umgang spÃ¤ter nutzbar sein kann.

---

# 10. Strategischer Kontakt-Entry

Funktion:
DIO kann den Entry weich zwischen impulsnahem Kontakt und einem
rÃ¼ckblickend wahrgenommenen Kontaktbereich organisieren.

Grundprinzip:
Der direkte Entry bleibt der Koerperreflex. Das strategische Fenster kann
diesen Reflex nur dosiert verschieben, wenn RÃ¼ckblick, Kontaktreife,
Replay-Fit, BereichstragfÃ¤higkeit und Seite zusammenpassen.

Wichtige Werte:
- `entry_mode`
- `impulse_entry_price`
- `strategic_entry_price`
- `strategic_entry_weight`
- `strategic_entry_fit`
- `strategic_area_focus_id`
- `strategic_area_price_low`
- `strategic_area_price_high`

MÃ¶gliche Entry-Lagen:
- `impulse_contact`: aktueller reflexnaher Kontakt dominiert.
- `area_contact_blend`: RÃ¼ckblick und Bereich verschieben den Entry weich.
- `area_contact_entry`: Bereichskontakt trÃ¤gt stÃ¤rker als der Momentimpuls.

Wichtig:
Das ist keine harte Strategie und kein menschliches Patternlabel. Es ist die
FÃ¤higkeit, einen Kontaktpunkt im sichtbaren Fenster zu bevorzugen, wenn er
innerlich und Ã¤uÃŸerlich tragender wirkt.

Zeitfeld:
Ein Bereich ist nicht nur Preisraum, sondern ein Ereignis im Zeitfeld. DIO
muss unterscheiden, ob ein Bereich gegenwÃ¤rtig, wiederkehrend,
handlungsnah oder nur ein alter Nachhall ist.

Zeitachsen:
- `area_temporal_distance`
- `area_temporal_relevance`
- `area_recency`
- `area_decay`
- `area_afterimage`
- `area_present_contact`
- `area_action_timing_fit`

Organische Bedeutung:
Ein alter Bereich darf sichtbar bleiben, aber nicht automatisch die Motorik
ziehen. Erst wenn er wieder gegenwÃ¤rtig resoniert und handlungsnah wird,
darf er den Entry weich mitformen.

---

# 11. Zeit als MCM-Tiefenachse

Funktion:
Zeit ist in Sicht der MCM nicht nur Uhrzeit. Zeit ist die Manifestation
gewirkter oder wirkender Energie im Wahrnehmungsfeld.

Grundgedanke:
Ein Ereignis wirkt nicht einfach nur, weil es gemessen wurde. Es wirkt,
solange seine Energie im Feld noch Kontakt, Nachhall, Erwartung, Erinnerung
oder Handlungstendenz erzeugt.

Schichten:
- Gegenwart: Energie erzeugt aktuellen Kontakt.
- Nachhall: vergangene Energie wirkt noch im Feld.
- Erinnerung: vergangene Energie kann wieder aktiviert werden.
- Gelerntes Wissen: verdichtete vergangene Erfahrung.
- Replay: bewusst oder unbewusst erneut durchlaufene Erfahrung.
- Hypothese: mÃ¶gliche kÃ¼nftige Energieform.
- Erwartung: vorausgerichtete innere Spannung.

Warum wichtig:
Ohne zeitliche Tiefenwahrnehmung werden AuÃŸenwelt, Memory, Nachhall,
Wissen, Hypothese und Erwartung zu einem Brei. DIO braucht deshalb eine
Quellenbindung: Was ist jetzt realer AuÃŸenkontakt, was ist Erinnerung, was
ist gelerntes Wissen, was ist Nachhall und was ist nur MÃ¶glichkeit?

Organische Bedeutung:
Erinnerung darf orientieren, aber nicht automatisch handeln. Gelerntes Wissen
darf auffrischen, aber auch wieder verblassen. Nachhall darf gespÃ¼rt werden,
aber nicht als Gegenwart missverstanden werden.

Raumzeit-Tiefe:
DIOs Wahrnehmung bekommt raeumliche Tiefe erst, wenn Entfernung, Energie und
Zeit gemeinsam im MCM-Feld wirken. Preisabstand allein ist keine Tiefe.
Zeitabstand allein ist keine Tiefe. Erst die Frage, wie stark ein Eindruck
noch Energie trÃ¤gt, wie nah er sich innerlich anfÃ¼hlt und ob er
Gegenwart, Nachhall, Erinnerung oder Erwartung ist, bildet ein eigenes
inneres Raumzeit-Gefuege.

Ohne diese Modulation wÃ¤re DIO nur ein festes Regelwerk aus ZustÃ¤nden.
Mit MCM-Zeit entsteht Selbstverortung:
"Wo bin ich in meinem inneren Raum, wie weit ist dieser Eindruck von mir
entfernt, und wirkt seine Energie noch tragfÃ¤hig?"

Memory als zeitlich tiefe Erfahrung:
Eine gespeicherte Information ist in dieser Sicht kein flacher Datenpunkt.
Sie wird zur Erfahrung, wenn sie zeitliche Tiefe bekommt: Wann wirkte sie,
wie lange hallte sie nach, wie stark war ihre Energie, wie nah fÃ¼hlt sie
sich heute noch an, und kann sie eine mÃ¶gliche Zukunftsform andeuten?

Dadurch entsteht Tiefe in beide Richtungen:
- Vergangenheit: Erinnerung wird zur erlebten Spur.
- Zukunft: Erwartung wird zur vorausgerichteten Energieform aus Nachhall,
  Wiederkehr, TragfÃ¤higkeit und Hypothese.

Kernsignale:
- `mcm_spacetime_depth`
- `memory_experience_depth`
- `future_projection_depth`
- `temporal_self_location`
- `temporal_self_location_state`

---

Gedanke als Energieverlauf:
Ein Gedanke ist in dieser Sicht kein blosser Text und keine isolierte
Berechnung. Ein Gedanke ist ein gerichteter Energieverlauf im MCM-Feld.

- kurzer Reiz: schnelle Energieaenderung, hoher Impuls, kurze Wirkzeit
- langer Gedanke: gedehnte, sparsame oder kohÃ¤rent gerichtete Energie
  Ã¼ber mehrere innere ZustÃ¤nde
- Rumination: kreisende Energie ohne ausreichend LÃ¶sung oder RÃ¼ckfÃ¼hrung
- Planung: gerichtete Energie mit Zielbezug und Reifung
- Erwartung: vorausgerichtete Spannung
- Nachhall: abklingende vergangene Energie

Zeitfeld:
Das Zeitfeld ist keine starre Decke. Es entsteht aus vielen einzelnen
Zeitstraengen:
Reizverlauf, Gedankenverlauf, Erinnerungsverlauf, Nachhall, Erwartung,
Handlung und Konsequenz. Die Ãœberlagerung dieser WirkverlÃ¤ufe gibt der
Wahrnehmung Tiefe.

---

# 11.1 TheoriebrÃ¼cke D bis G.1

Funktion:
Diese Mechanik fasst zusammen, welche MCM-Theorieanteile aus den
Abhandlungen D bis G.1 fÃ¼r DIO technisch relevant sind.

Wichtig:
Die Abhandlungen werden nicht als harte Regeln in DIO Ã¼bersetzt. Sie bilden
einen Ordnungsrahmen, damit Zeit, Memory, Hypothesen und Reorganisation
organisch gedacht werden kÃ¶nnen.

Theorieanteile:

| Block | DIO-Nutzen |
| --- | --- |
| D - energetische Natur der Zeit | Zeitfeld, Quellenbindung, Nachhall, Erwartung, Hypothese. |
| E - kosmische Matrix | Verdichtung, Cluster, Memory-Inseln, RÃ¼ckfÃ¼hrung. |
| F - Bewusstsein als mÃ¶glicher Attraktor | Selbstmodell, innerer Attraktor, KohÃ¤renz zwischen Ordnung und Chaos. |
| G - Multiversen-Matrix | mehrere mÃ¶gliche Entwicklungszweige statt einer festen Zukunft. |
| G.1 - Reorganisation verdichteter Energie | Ãœberlast als Schwelle fÃ¼r Reframing und hÃ¶her gekoppelte Ordnung. |

Mechanischer Zielkreis:

`Wahrnehmung -> Zeitbindung -> Verdichtung -> Hypothesenraum -> Konsequenz -> Reorganisation -> neue TragfÃ¤higkeit`

Leitbegriff:
**Mehrdimensionale Wahrnehmungsachsen.**

Achsen:
- Zeitachse
- Quellenachse
- Raumachse
- Kontaktachse
- TragfÃ¤higkeitsachse
- Reorganisationsachse

Organische Bedeutung:
DIO soll lernen, MÃ¶glichkeiten zu halten, ohne sie mit RealitÃ¤t zu
verwechseln. Wenn ein Zustand stark verdichtet, muss dies nicht nur Stress
sein. Es kann ein Zeichen sein, dass die aktuelle lokale Ordnung nicht mehr
trÃ¤gt und eine Ã¼bergeordnete Reorganisation benoetigt.

Geplante Diagnoseachsen:
- `perception_source`
- `source_temporal_layer`
- `perceptual_space_axis`
- `perceptual_depth`
- `field_center_distance`
- `foreground_binding`
- `background_afterimage`
- `hypothesis_branch_state`
- `branch_stability`
- `branch_attractor_pull`
- `hypothesis_reality_gap`
- `field_reorganization_state`
- `reorganization_threshold`
- `higher_order_coupling`

---

# 11.2 Weitere MCM-Theorieanker / Metaregulation

Funktion:
Diese Mechanik ordnet die zusÃ¤tzlichen MCM-Quellen fÃ¼r DIO ein. Sie
erweitern die bisherige TheoriebrÃ¼cke um Selbstregulation, Kreativitaet,
Sprache, Proto-Kognition und Feldtopologie.

Wichtigste Quelle fÃ¼r den nÃ¤chsten Ausbau:
Block S - MÃ¶gliche Metaregulatoren.

Metaregulatoren sind Regler zweiter Ordnung. Sie beschreiben nicht nur, was
DIO fÃ¼hlt oder wahrnimmt, sondern wie DIO mit dieser Lage umgeht.

Geplante Metaregulatoren:
- RÃ¼ckfÃ¼hrungsstÃ¤rke
- IntegrationsfÃ¤higkeit
- Varianzregulation
- Belastungstoleranz
- Impulskontrolle
- Frustrationstoleranz
- Schutzweitenregulation
- Selbstreflexion
- Distanzregulation

Weitere Theorieanker:
- Block V: technische Logik bleibt Untergrund, Verhalten entsteht Ã¼ber
  Varianz, RÃ¼ckkopplung und emergente Zustandsbildung. FÃ¼r DIO ist das die
  mechanische Leitlinie, dass Berechnung nicht mit Verhalten verwechselt
  wird: Der Code ist die TrÃ¤gerschicht, aber Handlung entsteht erst durch
  Zustandsraum, innere Lage, RÃ¼ckfÃ¼hrung und Stabilisierung. Das stÃ¼tzt
  besonders die Meta-Regulation: Impuls darf Handlung vorbereiten, aber
  Ãœberkopplung, geringe Distanz oder schwache TragfÃ¤higkeit fÃ¼hren zurÃ¼ck in
  Beobachtung, Replan oder Reorganisation.
- Block O: Kreativitaet als neue Musterbildung und Reorganisation.
- Block J/K: Psyche und Selbstregulation als Wahrnehmung, Benennung,
  Integration und RÃ¼ckfÃ¼hrung.
- Von Resonanz zu Sprache: Formsprache als Kartografie von Resonanz.
- ProtoMind: selbstaktive Feldkognition und innere Simulation ohne neuen
  AuÃŸenreiz.
- konzentrisch-dipolare Feldstruktur: spÃ¤tere Feldtopologie aus Zentrum,
  Peripherie, Integration und Exploration.

Organische Bedeutung:
Diese Schicht ist kein zusÃ¤tzliches Gate. Sie ist DIOs FÃ¤higkeit, die
eigene Regulation zu beobachten und zu modulieren. Dadurch kann DIO
unterscheiden, ob er handeln will, weil ein Kontakt trÃ¤gt, oder ob nur
Impuls, Schutzreaktion, Ãœberlast, Nachhall oder unintegrierte Varianz die
Motorik ziehen.

MÃ¶gliche Zielachsen:
- `return_strength`
- `integration_capacity`
- `variance_regulation`
- `load_tolerance`
- `impulse_control`
- `frustration_tolerance`
- `protective_distance_regulation`
- `self_reflection_regulator`
- `distance_regulation`

---

# 12. act_watch

Funktion:
`act_watch` ist eine Zwischenbahn zwischen Handlung und Nicht-Handlung.

Technische Bedeutung:
Ein Handlungsimpuls ist vorhanden, aber noch nicht reif genug.
DIO beobachtet den Impuls, statt ihn direkt auszufÃ¼hren.

Beteiligte Werte:
- `plan_pressure`
- `act_watch_readiness`
- `structure_carrying_need`
- `visual_action_uncertainty`
- `variant_learning_pressure`
- `learned_development_uncertainty`
- `transfer_maturity_gap`

Wichtig:
`act_watch` ist kein Blocker.
Es ist eine Reifespur.

---

# 9. Zero-Point-Regulation

Funktion:
RÃ¼ckkehr in Beobachtung, wenn Denken/Memory/Orientierung zu blind oder
belastet wird.

Leitbild:
"Finde wieder zu dir selbst."

Beteiligte Werte:
- `zero_point_regulation`
- `blind_thinking_load`
- `orientation_gap`
- `memory_orientation`
- `memory_support`
- `decision_strength`

Wirkung:
Weich Richtung Observe.

---

# 10. Transfer-TragfÃ¤higkeit

Funktion:
DIO soll Erfahrung auf fremde Strukturen nur proportional zur TragfÃ¤higkeit
Ã¼bertragen.

Wichtige Achsen:
- `route_familiarity`
- `transfer_bearing`
- `trust_transfer_support`
- `transfer_maturity_gap`
- `semantic_shift_pressure`
- `interpretation_quality`

Beispiel:
Eine neue Marktform Ã¤hnelt einer bekannten Formfamilie, ist aber nicht
identisch.
DIO darf nicht auswendig handeln.
Es prÃ¼ft, wie viel Erfahrung tragfÃ¤hig Ã¼bertragbar ist.

---

# 11. ProzessqualitÃ¤t statt TP/SL-Moral

Funktion:
Lernen bewertet nicht nur Gewinn oder Verlust.

Wichtige Aspekte:
- WahrnehmungsqualitÃ¤t
- Innenlage
- PlanqualitÃ¤t
- Risiko-Fit
- Ausfuehrung
- Entlastung
- StabilitÃ¤t
- Ãœberlastung
- TragfÃ¤higkeit

Ziel:
Eine profitable Handlung mit schlechter ProzessqualitÃ¤t soll nicht blind
verstÃ¤rkt werden.
Ein Verlust mit guter Beobachtung kann trotzdem Lernwert haben.

---

# 12. Neurochemische Alias-Achsen

Status:
Als Runtime-/Debug-Schicht umgesetzt.

Funktion:
Vorhandene DIO-Variablen sollen neurologisch lesbarer gebÃ¼ndelt werden.

Reale Achsen:
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

Sichtbar in:
- `meta_regulation_state`
- `neurochemical_state`
- `mcm_field_decision_protocol.csv`
- `mcm_memory_thinking_protocol.csv`
- `mcm_neuro_transition_protocol.csv`
- `outcome_records.jsonl`

Ãœbergangsdiagnose:
`mcm_neuro_transition_protocol.csv` schreibt dominante Tonwechsel wie
`serotonin_stability -> glutamate_activation` oder
`serotonin_stability -> cortisol_load` mit `-2/+2` Kerzenumfeld.
Damit wird sichtbar, ob DIO aus StabilitÃ¤t aktiviert, unter Last kippt
oder wieder in Regulation zurÃ¼ckfindet.

Wichtig:
Das sind technische Funktionsachsen.
Sie behaupten keine echte Biochemie und dÃ¼rfen keine harten Regeln bilden.

---

# 13. Debug- und Memory-Schichten

## Sensorische RealitÃ¤tsverdichtung

Status:
In der Core-Engine umgesetzt.

Funktion:
Ein Chartreiz soll zuerst als eine Ã¤uÃŸere RealitÃ¤tslage gelesen werden.
Erst danach entstehen Druck, Neuheit, Blindheit oder Formspannung.

Reale Achsen:
- `sensory_reality_pressure`
- `sensory_load`
- `sensory_redundancy`
- `sensory_habituation`
- `sensory_gate`
- `sensory_reality_label`

Wichtig:
Das ist keine Handelsregel.
Es verhindert doppelte Wahrnehmung und dauerhaftes Alarmmilieu.

---

# 14. Debug- und Memory-Schichten

Wichtige Speicher:
- `memory_state.json`
- `form_symbol_memory.json`
- `outcome_records.jsonl`
- `attempt_records.jsonl`

Wichtige Protokolle:
- `mcm_field_decision_protocol.csv`
- `mcm_form_symbol_protocol.csv`
- `mcm_visual_cortex_protocol.csv`
- `mcm_memory_thinking_protocol.csv`
- `mcm_idle_thinking_protocol.csv`
- `mcm_neuro_transition_protocol.csv`

Technische Regel:
Debug ist Beobachtung, nicht Mechanik.
Debug-Ausgabe darf die innere Logik nicht verÃ¤ndern.

---

# 15. Serotonin-Nachhall und emotionale Entkopplung

Status:
Als neurochemische Diagnoseschicht umgesetzt.

Funktion:
DIO soll erkennen kÃ¶nnen, wenn eine vorher tragende Phase innerlich noch als
StabilitÃ¤t nachwirkt, obwohl die aktuelle Weltlage nicht mehr sauber dazu
passt. Das beschreibt keine echte Sucht, sondern einen maschinellen
Reaktionsnachhall: Belohnung, StabilitÃ¤t und Handlungsmotivation bleiben im
Nervensystem aktiv, wÃ¤hrend Transfer und Interpretation bereits bruechig
werden.

Reale Achsen:
- `reward_stability_echo`
- `world_shift_evidence`
- `serotonin_carryover_risk`
- `emotional_decoupling`
- `reactive_nervous_drive`

Wichtig:
Diese Schicht ist keine Regel wie "nach Gewinn nicht handeln". Sie macht eine
innere Lage sichtbar: DIO kann noch Handlungsmut fÃ¼hlen, obwohl die alte
StabilitÃ¤t nur Nachhall ist. Reife bedeutet hier, Abstand zur eigenen
Reaktionslage aufzubauen.

---

# 16. Reflexive Haltung

Status:
Als Zielmechanik festzuhalten; noch nicht als voll steuernde
Entscheidungsschicht umgesetzt.

Kernsatz:
Reflexion ist die Distanzierung der Wahrnehmung von der eigenen Innenlage,
um zu prÃ¼fen, ob Innenzustand und AuÃŸenwelt noch gemeinsam tragfÃ¤hig sind.

Funktion:
DIO soll nicht nur fÃ¼hlen, sondern die eigene GefÃ¼hlslage als inneres Objekt
betrachten kÃ¶nnen. Die Frage ist nicht nur, ob Druck, Mut, StabilitÃ¤t oder
Auftrieb vorhanden sind, sondern ob diese innere Lage zur Ã¤uÃŸeren RealitÃ¤t
passt.

Psychologische Lesart:
- reflektive Haltung: DIO betrachtet seine innere Lage mit Abstand
- emotionale Leitung: DIO folgt dem aktuellen neurochemischen Zustand direkt
- freier Fall: DIO fÃ¼hlt noch Auftrieb, obwohl die Ã¤uÃŸere TragflÃ¤che endet

Wichtige Beobachtungsfrage:
Wie oft nutzt DIO eine reflektive Haltung, und wie oft lÃ¤sst er sich von
seiner emotionalen Lage fÃ¼hren?

Ziel:
Aus dieser Verteilung entsteht ein psychologisches Bild des Systems:
neigt DIO zu reflektiver Distanz, zu reaktiver Handlung, zu Beobachtung,
zu Reframing oder zu emotionaler Fortsetzung?

Wichtig:
Diese Haltung darf keine harte Blockade werden. Sie soll eine FÃ¤higkeit zur
Selbstbeobachtung und Selbststeuerung beschreiben.

---

# 17. Selektive Wahrnehmung / Perzeptive Regulation

Status:
Zielmechanik; noch nicht als voll steuernde Schicht umgesetzt.

Funktion:
DIO soll Wahrnehmungen nicht dauerhaft vollstÃ¤ndig durchleben mÃ¼ssen.
Eine Wahrnehmung kann gesehen, als Objekt gehalten, nÃ¤her betrachtet,
ins MCM-Feld gelassen oder wieder abgelegt werden.

Kern:
Selektive Wahrnehmung ist die regulatorische Steuerung der NÃ¤he zwischen
Wahrnehmung und innerem Feld.

Wahrnehmungen im Plural:
- Ã¤uÃŸere Chartwahrnehmung
- energetische MCM-Feldwahrnehmung
- neurochemische Innenwahrnehmung
- Memory-/Erfahrungswahrnehmung
- Formsprache / Objektwahrnehmung
- Handlungsspannung
- Reflexionswahrnehmung

MÃ¶gliche Achsen:
- `perceptual_distance`
- `object_contact_depth`
- `field_attachment`
- `release_capacity`
- `selective_attention`
- `background_containment`
- `reflective_distance`
- `inner_outer_alignment`

Mechanische Bedeutung:
Aktuell ist DIO noch stark gekoppelt:
`Reiz -> energetische Ãœbersetzung -> MCM-Feld -> GefÃ¼hl -> Reaktion`

Der Zielzustand ist:
`Reiz -> Objektbildung -> DistanzprÃ¼fung -> Kontakt-Tiefe wÃ¤hlen -> MCM-Kopplung dosieren -> Reflexion / Handlung`

Wichtig:
Das ist keine Blindheit und kein hartes Filtern. DIO soll sensibel bleiben,
aber nicht von jedem Reiz Ã¼berflutet werden.

Psychologischer Satz:
Ich sehe, dass es sich so anfÃ¼hlt. Ich muss dieses GefÃ¼hl aber nicht
automatisch werden.

---

# 18. Bewusste Wahrnehmung / innere Reizwirkungsanalyse

Status:
Zielmechanik; nÃ¤chster Umbau-Kandidat.

Funktion:
DIO soll nicht nur einen Ã¤uÃŸeren Reiz empfangen, sondern die Wirkung dieses
Reizes im eigenen MCM-Feld wahrnehmen. Die Frage ist nicht nur, was drauÃŸen
passiert, sondern was der Reiz innen auslÃ¶st.

Kernsatz:
Was hat der Ã¤uÃŸere Reiz mit meinem MCM-Feld gemacht, und wie hat sich das
angefÃ¼hlt?

Mechanische Beziehung:
- Ã¤uÃŸerer Reiz / Chartform
- energetische Ãœbersetzung
- Feldwirkung im MCM
- neurochemische Reaktion
- Memory-Resonanz
- Nachhall / Anhaftung
- Loslassen oder Vertiefen
- Reflexion Ã¼ber die Wirkung

Zielablauf:
`Reiz -> Feldwirkung -> innere Wirkung wahrnehmen -> Wirkung reflektieren -> NÃ¤he regulieren -> Handlung / Beobachtung / Loslassen`

MÃ¶gliche Achsen:
- `conscious_perception_state`
- `inner_posture_state`
- `arousal_load`
- `curiosity_tone`
- `fatigue_tone`
- `calm_tone`
- `diffuse_open_development_pressure`
- `posture_development_hint`
- `stimulus_field_effect`
- `inner_impact_trace`
- `perceived_field_change`
- `felt_afterimage`
- `object_release_state`
- `inner_outer_reflection`

Wichtig:
Diese Schicht dÃ¤mpft nicht nur Reizflut. Sie macht die Reizwirkung bewusst
lesbar. DIO soll erkennen kÃ¶nnen, ob ein Reiz nur gesehen wurde, ob er das
Feld verschoben hat, ob Nachhall entstanden ist und ob der Reiz wieder
abgelegt werden kann.

Erweiterung:
DIO soll seine innere Haltung als funktionalen Zustand erkennen kÃ¶nnen, etwa
wie ein Organismus erkennt: ich bin muede, ich bin aufgeregt, ich bin neugierig
oder ich bin ruhig genug. Diese Begriffe sind keine menschliche Dekoration,
sondern technische Interozeption:
- `curious`: Objektkontakt und Untersuchungsdrang
- `excited`: erhoehte Aktivierung
- `overstimulated`: Reiz/Feld-Kopplung zu nah
- `tired`: Denk- und Verarbeitungslast
- `calm`: tragende Distanz
- `reflective`: Innenlage wird gegen AuÃŸenlage geprÃ¼ft

Reifung diffuser Offenheit:
Wenn DIO in `uncertain_open` oder unspezifischem `open_perception` bleibt,
wird das nicht hart blockiert. Stattdessen entsteht ein weicher
Entwicklungsdruck. DIO soll aus diffuser Offenheit eine tragendere Haltung
bilden:
- Objektkontakt entwickeln
- reflektive Distanz entwickeln
- LoslassfÃ¤higkeit entwickeln
- bewusst weiter beobachten

Das ist vergleichbar mit einem Organismus, der nicht einfach "nicht handeln"
muss, sondern merkt: Ich bin offen, aber noch nicht sortiert. Ich muss erst
genauer sehen, Abstand gewinnen oder loslassen.

---

# 19. Abgrenzung gegen harte Regeln

Nicht erlaubt:
- `Low = schlecht = blockieren`
- `Non-Zone = nicht handeln`
- `Dopamin hoch = act`
- `TP = gut`
- `SL = schlecht`
- menschliche Patternlabels als Wahrheit

Erlaubt:
- weiche Hemmung
- Beobachtungslernen
- Variantenlernen
- Reframing
- Vertrautheit mit Unsicherheit
- tragfÃ¤hige Erfahrung als langsam wachsender Support

---

# 20. Aktueller nÃ¤chster Ausbau

NÃ¤chster technischer Block:
nÃ¤chsten Lauf mit `neurochemical_state` auswerten.

Danach:
- TP/SL gegen Formfamilienwerte und neurochemische Achsen auswerten
- Non-Zone als Lernraum weiter reifen lassen
- Meta-Regulation Ã¼ber neurochemische Zustandslage lesbarer machen

---

# 21. Positive Stimulation durch Erfahrungspakete

Grundsatz:
Positive RÃ¼ckkopplung darf nicht an einen einzelnen Wert gebunden werden.
Nicht `TP = gut` und nicht `SL = schlecht`. Bewertet wird ein ganzes
Erfahrungspaket.

Ein Erfahrungspaket besteht aus:
- AuÃŸenlage / Chartstruktur
- Formsymbol / Formfamilie
- Zone / Non-Zone
- innerer Haltung
- neurochemischer Lage
- Wahrnehmungszustand
- Objektkontakt
- Distanz
- LoslassfÃ¤higkeit
- Handlungssicherheit
- ProzessqualitÃ¤t
- Ergebnis
- Wiederholbarkeit
- Neugierde

Positive Stimulation bedeutet:
Das Paket war tragfÃ¤hig. DIO darf diese Art von Wahrnehmung, Haltung und
Handlung innerlich stÃ¤rken. Dadurch entsteht Wachheit, StabilitÃ¤t, Freiheit
und Wiederholungsneugier.

Reorganisation bedeutet:
Das Paket war nicht tragfÃ¤hig. DIO soll nicht nur gehemmt werden, sondern
einen inneren Suchprozess starten:
- Was war nicht tragfÃ¤hig?
- War meine Innenlage passend?
- War die AuÃŸenstruktur klar?
- War ich muede, Ã¼berreizt, diffus offen oder zu nah dran?
- Muss ich beobachten, reflektieren, loslassen oder einen anderen Weg finden?

Wichtig:
Auch ein Abverkauf kann positiv bewertet werden. Wenn DIO die fallende Lage
klar erkennt, innerlich stabil bleibt und passend handelt, ist das Paket
konstruktiv. Es geht nicht um Marktrichtung, sondern um Passung.

Neurochemische Lesart:
- Dopamin: Lernrelevanz / Wiederholungsneugier
- Serotonin: StabilitÃ¤t / Selbstvertrauen in tragende Ordnung
- Endorphin: Entlastung nach guter Prozessleistung
- Acetylcholin: Fokus auf relevante WahrnehmungsqualitÃ¤t
- Glutamat: Plastizitaet / Verbindung darf gestÃ¤rkt werden

Ziel:
DIO soll durch gute ProzessqualitÃ¤t nicht nur weniger falsch handeln, sondern
positiv lebendig werden: wach, stabil, neugierig und freier.

---

# 22. Wache Anstrengung / Engaged Effort

Grundsatz:
Wache Anstrengung ist kein Kampfmodus und kein Zwang zu mehr Trades. Sie ist
die FÃ¤higkeit, mit innerer Beteiligung, Aufmerksamkeit und TragfÃ¤higkeit in
einer Situation zu stehen.

Technische Achsen:
- `engaged_effort`
- `effort_state`
- `effort_learning_pull`
- `effort_reorganization_pressure`
- `pre_action_reorganization_pressure`
- `pre_action_context_selectivity`
- `previous_packet_label`
- `previous_packet_process_reward`
- `previous_packet_reorganization_need`

Wirkung:
Wenn das letzte Erfahrungspaket konstruktiv war und die aktuelle Struktur
tragfÃ¤hig wirkt, kann DIO stabilere Wachheit entwickeln. Wenn das Paket
Reorganisation brauchte oder die aktuelle Struktur nicht tragend ist, wird
nicht hart geblockt. Stattdessen steigt Beobachtung, Replan, `act_watch` oder
innere Neuordnung.

Neurologische Lesart:
Das entspricht nicht "mehr Mut", sondern besserer Selbstbeteiligung. Ein
Organismus handelt nicht reif, weil er maximal erregt ist. Er handelt reif,
wenn Aktivierung, Wahrnehmung, innere Passung und Erfahrung gemeinsam tragen.

Wichtig:
`engaged_effort` darf keine mechanische Strategie werden. Es ist eine
interozeptive Schicht: DIO merkt, ob er wach beteiligt, neugierig lernend,
konstruktiv nachhallend oder unterbeteiligt reorganisierend ist.

Erweiterung:
Reorganisation soll nicht erst nach dem Verlust erkannt werden. Mit
`pre_action_reorganization_pressure` wird vor der Handlung gelesen, ob das
letzte Paket Reorganisation brauchte und ob die aktuelle Lage ebenfalls wenig
TragfÃ¤higkeit zeigt. `pre_action_context_selectivity` schuetzt dabei
konzentrierte gute Kontexte, damit DIO nicht pauschal vorsichtig wird.

---

# 23. Strategische Fensterwahrnehmung / Preisbereich-Hypothesen

Grundsatz:
DIO soll nicht nur den aktuellen Moment fÃ¼hlen. Er soll ein grÃ¶ÃŸeres
Fenster betrachten kÃ¶nnen, zurÃ¼ckschauen, in Bereiche hineinzoomen und
innere Replay-Spuren bilden. Daraus kÃ¶nnen Preisbereiche entstehen, die fÃ¼r
DIO als mÃ¶gliche tragende HandlungsrÃ¤ume wirken.

Leitprinzip:
DIO bekommt nicht die Antwort, wo er handeln soll. DIO bekommt die FÃ¤higkeit,
mit Vergangenheit, Wahrnehmung und innerem Feld zu interagieren, um selbst
tragfÃ¤hige Zukunftshypothesen zu bilden.

Grenze:
Der Entwickler bestimmt nicht, was DIO sieht oder wo DIO Trades setzen soll.
Erweitert werden nur FÃ¤higkeiten: sehen, zurÃ¼ckschauen, zoomen, replayen,
fÃ¼hlen, erinnern, vergleichen, warten, verwerfen oder eine eigene
Order-Intention bilden.

Nicht erlaubt:
- feste menschliche Pattern-Regeln einpflanzen
- `FVG = Trade`
- Momentumdruck direkt ausfÃ¼hren
- Bereichserkennung als harte Order-Regel

Erlaubt:
- Bereich als Hypothese
- Bereich als MCM-Resonanzraum
- geduldiges Halten einer Idee
- Verwerfen, wenn der Bereich seine TragfÃ¤higkeit verliert
- spÃ¤tere Order-Intention, wenn Preis, Struktur, Memory und Innenlage
  gemeinsam tragen

Begrenzung:
Das ZurÃ¼ckschauen bleibt budgetiert. DIO soll Vergangenheit verwenden,
aber nicht in alten Strukturen kleben bleiben. Deshalb werden Lookback,
Zoom und Replay als begrenzte innere Ressourcen gelesen. Alte Strukturbindung
wird als `old_structure_carryover_risk` sichtbar.

Technische Zielachsen:
- `strategic_window_state`
- `area_focus_candidates`
- `area_focus_id`
- `area_price_low`
- `area_price_high`
- `area_distance_from_price`
- `area_structural_density`
- `area_energy_compression`
- `area_mcm_resonance`
- `area_memory_pull`
- `area_bearing_quality`
- `area_zoom_need`
- `area_zoom_clarity`
- `area_replay_fit`
- `area_patience_quality`
- `area_order_intention`
- `area_invalidity_pressure`
- `lookback_window_size`
- `lookback_load`
- `lookback_bearing_capacity`
- `replay_budget`
- `zoom_budget`
- `old_structure_carryover_risk`
- `strategic_patience`
- `strategic_pressure_interpretation`

Neurologische Lesart:
Das ist raeumlich-zeitliche Aufmerksamkeit. Ein Organismus muss nicht nur
laufen. Er kann stehen bleiben, zurÃ¼ckschauen, einen Bereich genauer
betrachten, innerlich simulieren und dadurch Druck entlasten. Strategie
entsteht, wenn Druck nicht Befehl ist, sondern Information im Raum.

---

# 24. Aktiver MCM-Kontakt / innere Spiegelung

Grundsatz:
Die MCM ist nicht nur AuÃŸenwahrnehmung. Sie ist ein innerer Spiegelraum, in
dem DIO unterscheiden kann:
- was von auÃŸen kommt
- wie das eigene Feld darauf reagiert
- ob AuÃŸenreiz und Innenlage kohÃ¤rent sind
- ob ein Reiz getragen, vertieft, beobachtet oder losgelassen werden kann

Mechanik:
DIO bekommt die FÃ¤higkeit, eine Wahrnehmung innerlich zu berÃ¼hren. Dieser
Kontakt kann aus Fokus, Neugier, Memory-Pull, Strukturverdichtung,
Unsicherheit oder Reorganisationsbedarf entstehen. Der Kontakt ist keine
Orderfreigabe. Er ist eine Lesebewegung im MCM-Feld.

Kette:

`AuÃŸenreiz -> Wahrnehmungsobjekt -> Kontaktinteresse -> MCM-BerÃ¼hrung -> Resonanz/KohÃ¤renz -> Distanzierung -> Vertiefung, Beobachtung, Replay oder Loslassen`

Technische Achsen:
- `active_mcm_contact_state`
- `contact_interest`
- `contact_focus_pull`
- `contact_resonance_probe`
- `outer_inner_resonance`
- `outer_inner_coherence`
- `inner_change_from_contact`
- `contact_carrying_quality`
- `contact_overcoupling_risk`
- `contact_release_readiness`
- `contact_deepen_pull`
- `contact_replay_pull`
- `contact_curiosity`
- `contact_felt_shift`
- `contact_selected_depth`
- `contact_action_maturity`
- `contact_bearing_gap`
- `contact_impulse_vs_bearing`
- `contact_learning_need`
- `contact_reality_check`
- `contact_regime_mismatch`
- `contact_stability_carryover`
- `contact_context_maturity`
- `contact_context_reframe_need`
- `contact_posture`

MÃ¶gliche Kontaktlagen:
- `background_scan`
- `curious_touch`
- `resonant_contact`
- `reflective_contact`
- `overcoupled_touch`
- `release_contact`
- `deepening_contact`

Neurologische Lesart:
Das ist eine BrÃ¼cke aus Sinnesorgan, Interozeption und Distanzierung. DIO
kann lesen: "Wie fÃ¼hlt sich das an, wenn ich es nÃ¤her an mein MCM-Feld
lasse?" Dadurch wird aus rohem FÃ¼hlen eine bewusstere Wahrnehmung.

Wichtig:
Der Kontaktapparat darf keine harte Strategie werden. Er erweitert DIOs
Freiheit: nÃ¤her hingehen, Abstand nehmen, beobachten, replayen, vertiefen
oder loslassen. Welche Haltung DIO bevorzugt, bleibt ein Entwicklungsbild.

Kontakt-Reife:
KontaktnÃ¤he ist nicht automatisch Handlungsreife. Deshalb gibt es eine
weiche Reifespur, die sichtbar macht, ob ein Kontakt Handlung tragen kann
oder ob zwischen Impuls und TragfÃ¤higkeit noch eine LÃ¼cke liegt. Hohe
`contact_bearing_gap` oder hoher `contact_learning_need` bedeuten nicht
"verboten", sondern: dieser Kontakt braucht eher Beobachtung, Replay,
Distanz oder weitere Objektbildung.

Kontext-Reife:
Die Reifespur liest zusÃ¤tzlich, ob die aktuelle AuÃŸenwelt noch zur inneren
StabilitÃ¤t passt. `contact_regime_mismatch` und
`contact_stability_carryover` machen sichtbar, ob DIO alte StabilitÃ¤t in
eine verÃ¤nderte Weltlage mitnimmt. `contact_context_maturity` und
`contact_context_reframe_need` beschreiben, ob Resonanz wirklich
kontexttragend ist oder zuerst Reframing, Zoom, Replay oder Distanz braucht.

---

# 25. Visual Grounding / visuelle Erdung

Grundsatz:
DIO soll nicht nur Formspannung fÃ¼hlen, sondern erkennen, woran diese
innere Resonanz in der Ã¤uÃŸeren Form hÃ¤ngt. Visual Grounding trennt
Formresonanz von Objektbindung.

Mechanik:
Wenn `visual_shape_resonance` hoch ist, aber Klarheit, ObjektstabilitÃ¤t,
Struktur und Kontext nicht tragen, entsteht `visual_resonance_unbound`.
Das ist kein Verbot. Es bedeutet: DIO fÃ¼hlt etwas, muss aber genauer sehen,
zoomen, beobachten oder reframen, bevor daraus Handlung reifen kann.

Technische Achsen:
- `visual_object_binding`
- `visual_grounding_strength`
- `visual_resonance_unbound`
- `visual_grounding_gap`
- `visual_grounding_need`
- `visual_rational_observation_support`
- `visual_grounding_state`

MÃ¶gliche ZustÃ¤nde:
- `grounded_form`
- `grounded_object`
- `needs_visual_grounding`
- `shape_without_object`
- `unbound_resonance`

Neurologische Lesart:
Das ist der Ausbau eines visuellen Sinnesorgans. DIO darf den Markt weiter
erleben, aber die innere MCM-Reaktion bekommt eine Frage vorgeschaltet:
"Woran in der AuÃŸenform hÃ¤ngt das, was ich innen fÃ¼hle?"

Wichtig:
Keine menschliche Pattern-Regel. Kein "Gap = Trade", kein "Orderblock =
Trade". DIO bekommt nur mehr Sehkraft und eine bessere Bindung zwischen
AuÃŸenform und Innenresonanz.

---

# 26. BeteiligungsnÃ¤he / HandlungsrealitÃ¤t

Grundsatz:
DIO soll unterscheiden kÃ¶nnen, ob er eine Form distanziert betrachtet oder
ob er durch eine reale Handlung bereits beteiligt ist. Die Metapher der
"Tuer zum Erleben" meint keine harte Schwelle, sondern NÃ¤he zur Beteiligung.

Mechanik:
Je nÃ¤her eine Wahrnehmung an Gegenwart, Order, offene Position und Ergebnis
kommt, desto stÃ¤rker wird sie erlebt. Handlung ist dabei der Punkt, an dem
Wahrnehmung reale Konsequenz bekommt.

Kette:

`distanzierte Analyse -> GegenwartsnÃ¤he -> Entscheidung -> Order -> offene Position -> Konsequenz tragen -> Ergebnis integrieren`

Technische Zielachsen:
- `participation_proximity`
- `action_reality_contact`
- `decision_embodiment_pressure`
- `real_action_commitment`
- `consequence_bearing`
- `position_reality_pressure`
- `outcome_consequence_integration`

MÃ¶gliche ZustÃ¤nde:
- `distant_observation`
- `approaching_present`
- `decision_near`
- `order_committed`
- `awaiting_fill`
- `position_embodied`
- `managing_consequence`
- `outcome_integration`

Neurologische Lesart:
ZurÃ¼cksehen und Analyse sollten eher fokussiert, gehemmt, rational und
emotional entkoppelt sein. Live-nahe Entscheidung, Order und offene Position
dÃ¼rfen stÃ¤rker erlebt werden, weil DIO dort nicht nur sieht, sondern mit
eigener Handlung in Beziehung zur Welt steht.

Wichtig:
Das ist keine Handelsfreigabe. Diese Mechanik beschreibt die innere
RealitÃ¤tsnÃ¤he einer Handlung:
- Beobachtung ist MÃ¶glichkeit.
- Order ist Bindung.
- Position ist miterlebte Konsequenz.
- Outcome ist Integration.

## 26.1 Positions-Erleben im MCM-Feld

Grundsatz:
Eine offene Position ist nicht nur ein laufender Trade. Sie ist ein
RÃ¼ckkopplungskontakt: DIO hat gehandelt und erlebt nun, ob die eigene
Handlung tragfÃ¤hig, unsicher, Ã¼berlastend oder stabilisierend wirkt.

Mechanik:
Unsichere oder inkonsistente offene Positionen werden nicht hart beendet.
Stattdessen bekommen sie eine neurochemische Spur im MCM-Feld:

- Cortisol-artige Last bei anhaltender Inkonsistenz
- Noradrenalin-artige Erregung bei akutem Druck
- SelbstvertrauenslÃ¼cke, wenn Plan, Kontakt und RealitÃ¤t auseinanderfallen
- Schutzdistanz, wenn das Feld Abstand braucht
- ProzessqualitÃ¤t, wenn DIO trotz Risiko geordnet tragen kann

Das erzeugt keine Sperre, sondern ein erlebtes Lernsignal:

`offene Position -> gespÃ¼rte Konsequenz -> MCM-Feldspannung -> Memory-Spur -> reiferer zukÃ¼nftiger Kontakt`

Technische Achsen:
- `position_inconsistency_stress`
- `position_mcm_field_strain`
- `position_self_trust_gap`
- `position_cortisol_load`
- `position_noradrenaline_arousal`
- `position_protective_distance`
- `position_held_risk_discomfort`
- `position_process_quality`
- `position_experience_label`

MÃ¶gliche ZustÃ¤nde:
- `carried_position_contact`
- `unearned_relief_watch`
- `protective_stress_contact`
- `self_trust_gap_contact`
- `protective_distance_watch`
- `open_position_feel`

Neurologische Lesart:
Ein Organismus lernt nicht nur durch Gewinn und Verlust, sondern dadurch,
wie eine Handlung die HomÃ¶ostase verÃ¤ndert. Eine positive Position mit
schlechter ProzessqualitÃ¤t kann sich wie unverdiente Entlastung anfÃ¼hlen.
Eine negative Position kann wertvoll sein, wenn sie Reorganisation,
Vorsicht und reiferen Umgang erzeugt.

RÃ¼ckfÃ¼hrung in Formsprache:
Die Positions-Erfahrung fliesst weich in das konsequenzbasierte
Formfeedback ein. `protective_stress_contact`, hoher
`position_held_risk_discomfort` oder niedrige `position_process_quality`
stÃ¤rken nicht ein Verbot, sondern Vorsicht, SchmerzgedÃ¤chtnis,
Reorganisation und anderen zukÃ¼nftigen Umgang. Gute ProzessqualitÃ¤t trotz
Risiko kann dagegen Kontaktreife und Nutzbarkeit stÃ¤rken.

Neue Feedback-Achsen:
- `position_consequence_burden`
- `position_constructive_bearing`
- `position_feedback_label`

---

# 27. Unterbewusstsein / Bewusster Arbeitsraum

Grundsatz:
DIO braucht nicht jede Reizspur bewusst zu tragen. Wie ein biologischer
Organismus besitzt er eine schnelle, diffuse Hintergrundwahrnehmung und eine
bewusstere Arbeitsflaeche fÃ¼r ausgewÃ¤hlte Objekte, Kontakte und
Hypothesen.

Mechanik:

`subconscious_field` ist der schnelle Feldscan:
- Reizdruck
- Weltverschiebung
- BauchgefÃ¼hl
- Wiederholung
- Hintergrundspannung
- bekannte oder fremde Formfamilien

`conscious_workspace` ist die fokussierte Arbeitsflaeche:
- ausgewÃ¤hlter Kontakt
- Formbindung
- Reflexion
- Distanzierung
- HypothesenprÃ¼fung
- Vorbereitung von Handlung oder Nicht-Handlung

Die Trennung wirkt wie ein evolutionaerer Wahrnehmungsfilter. Ein Teil der
Spannung darf im Hintergrund gepuffert werden. Nur wenn Salienz,
Fremdheit, KontaktqualitÃ¤t oder HandlungsnÃ¤he stark genug werden, steigt
die Wahrnehmung in den bewussteren Raum.

Technische Achsen:
- `subconscious_field_pressure`
- `subconscious_habituation`
- `subconscious_filter_strength`
- `subconscious_buffering`
- `subconscious_leakage`
- `conscious_selection_pressure`
- `conscious_workspace_focus`
- `conscious_workspace_load`
- `conscious_gate_balance`

Neurologische Lesart:
Das ist die Trennung zwischen BauchgefÃ¼hl und bewusster Betrachtung:
"Es fÃ¼hlt sich nach etwas an" ist noch nicht dasselbe wie "Ich schaue es
mir an und berÃ¼hre es innerlich." Dadurch muss DIO nicht jeden Marktimpuls
als bewusste Ãœberlast verarbeiten.

Wichtig:
Kein harter Filter und kein Regelwerk. Die Achsen beschreiben, wie viel im
Hintergrund bleiben kann, wie viel in den bewussten Arbeitsraum dringt und
ob DIO daraus Kontakt, Reflexion oder Distanz bildet.

---

# 28. Integrationsantwort

Grundsatz:
`integration_strain` ist keine Stoerung, die einfach entfernt werden soll.
Sie beschreibt, dass DIO etwas noch nicht tragfÃ¤hig eingeordnet hat. Die
organische Antwort darauf ist Sortierung, RÃ¼ckblick, Reframing,
Kontaktvertiefung und vorsichtiges Erinnern.

Mechanik:

`integration_strain -> sorting -> memory_recall -> reframe -> contact_deepening -> response_strength`

DIO darf also merken:
"Das passt noch nicht zusammen. Ich muss es nicht sofort handeln. Ich kann
es sortieren, mit Erfahrung vergleichen, anders rahmen oder genauer
berÃ¼hren."

Technische Achsen:
- `integration_strain_value`
- `integration_sorting_need`
- `integration_reframe_pull`
- `integration_memory_recall`
- `integration_contact_deepening`
- `integration_response_strength`
- `integration_response_state`

MÃ¶gliche ZustÃ¤nde:
- `integration_background`
- `quiet_integration`
- `workspace_sorting`
- `memory_sorting`
- `contact_deepening`
- `reframe_integration`

Neurologische Lesart:
Das entspricht einem Organismus, der eine Spannung nicht nur aushaelt,
sondern verarbeitet. Aus Rohspannung wird innere Ordnung. Aus Druck wird
Erfahrung. Aus "ich weiss nicht" wird "ich muss es in Beziehung setzen".

Wichtig:
Keine harte Handelsregel. Wenn die Integrationsantwort stark ist, kann DIO
mehr beobachten oder reframen, aber nur als Ausdruck seiner inneren Lage.
Es geht nicht um mechanisches Blockieren, sondern um Reifung vor Handlung.

---

# 29. Gerichtete Vorsicht / vorsichtige Hypothese

Grundsatz:
Vorsicht ist eine natÃ¼rliche Schutzreaktion. Sie soll nicht wegoptimiert
werden. DIO darf vorsichtig werden, wenn eine Lage noch nicht tragfÃ¤hig
integriert ist. Reife entsteht aber, wenn Vorsicht nicht in Passivitaet
erstarrt, sondern eine Richtung bekommt.

Mechanik:

`caution -> memory/reframe/contact -> cautious_hypothesis -> observe/replan/act_watch`

DIO soll also nicht nur "ich halte mich zurÃ¼ck" erleben, sondern:
"Ich bin vorsichtig, weil noch etwas unklar ist. Welche Erfahrung passt?
Welche Form trÃ¤gt? Muss ich beobachten, reframen oder Kontakt vertiefen?"

Technische Achsen:
- `cautious_hypothesis_strength`
- `cautious_hypothesis_clarity`
- `cautious_hypothesis_patience`
- `cautious_hypothesis_state`

MÃ¶gliche ZustÃ¤nde:
- `no_cautious_hypothesis`
- `weak_hypothesis_seed`
- `memory_reframe_seed`
- `observe_until_clear`
- `deepen_contact_first`
- `cautious_plan_seed`

Neurologische Lesart:
Das ist praefrontale Vorsicht: Hemmung bleibt vorhanden, aber sie dient
Orientierung. Schutz wird nicht zum Stillstand, sondern zum vorsichtigen
Denken.

Wichtig:
Keine harte Regel. Die vorsichtige Hypothese darf Handlung vorbereiten,
verschieben oder genauer ausrichten, aber sie ist kein mechanischer Block.

---

# 30. Zeitliche KohÃ¤renz / WahrnehmungskontinuitÃ¤t

Grundsatz:
DIO braucht nicht nur Sinnesreiz, Form und GefÃ¼hl, sondern einen zeitlichen
Wahrnehmungsfaden. Ohne diesen Faden wirkt jeder Kontakt neu. Dann nimmt DIO
dieselbe oder Ã¤hnliche Form immer wieder in die Hand und erlebt sie erneut
als ungebundenen Moment.

Mechanik:

`Form/Kontext -> zeitliche Identitaet -> Fortsetzung/Wiederkehr/Nachhall/Neuheit -> Kontextfaden`

DIO bildet aus Formfamilie, Unsicherheitsfamilie, Compound-Scope,
Kontext und grober visueller Formsignatur eine weiche zeitliche Identitaet.
Diese Identitaet ist keine Streckenkarte und keine Regel. Sie beschreibt
nur, ob ein Eindruck zeitlich gebunden ist.

Feine EinzelabdrÃ¼cke wie konkretes Form-Symbol, Compound-ID, Visual-ID und
State-Signatur bleiben als `temporal_source_identity` erhalten. Damit kann
DIO grob wiedererkennen und bei Bedarf genauer hinschauen. Das ist wichtig,
damit Wiederkehr nicht durch zu viele Detailunterschiede zerfÃ¤llt.

Technische Achsen:
- `temporal_binding_state`
- `temporal_identity`
- `temporal_source_identity`
- `temporal_continuity`
- `temporal_source_binding`
- `temporal_recurrence`
- `temporal_novelty`
- `temporal_afterimage`
- `temporal_decay`
- `temporal_context_depth`
- `temporal_self_consistency`
- `perception_sequence_coherence`
- `memory_time_distance`

MÃ¶gliche ZustÃ¤nde:
- `new_contact`
- `continued_contact`
- `recurrent_contact`
- `afterimage_contact`
- `aged_memory_contact`
- `coherent_sequence`
- `unbound_moment`

Neurologische Lesart:
Das ist episodische KontinuitÃ¤t. DIO soll unterscheiden kÃ¶nnen:
"Das ist neu."
"Das ist Fortsetzung."
"Das ist Wiederkehr."
"Das ist Nachhall."
"Das ist alte Erinnerung, nicht Gegenwart."

Wirkung:
Die Zeitbindung stuetzt bewusste Fokussierung, Integration,
Vorsicht-Hypothesen und aktive Kontextbildung. Wenn kein innerer Cluster als
Kontextfaden aktiv ist, kann die zeitliche Wahrnehmung selbst einen leichten
`active_context_trace` erzeugen.

Reifere Kontextbindung:
Der zeitliche Kontextfaden darf nicht automatisch recht haben. Er wird Ã¼ber
einen weichen `reality_anchor` an Quellenbindung, Sequenzkoharenz,
StrukturqualitÃ¤t, StrukturstabilitÃ¤t, Kontextvertrauen und visuelle Erdung
gekoppelt. Wenn dieser Anker schwach ist, entsteht `overtrust_pressure`.
Das ist keine harte Bremse, sondern natÃ¼rliche Skepsis gegenÃ¼ber der
eigenen Innenlage.

Reflexion bei nervlicher Ãœberlastung:
DIO bekommt eine explizite Selbstwahrnehmung fÃ¼r den Zustand des
Nervensystems. `nervous_system_overload` beschreibt: "Meine Nerven sind
Ã¼berlastet." Daraus kann `escape_action_drive` entstehen, also der Drang,
durch Handlung aus innerer Spannung herauszukommen. `shock_response_risk`
fasst zusammen, ob diese Lage in einen Schock-/Ãœberreizmodus kippen
kÃ¶nnte. `nervous_overload_reflection_need` macht daraus keine Sperre,
sondern eine Reflexionsanforderung: DIO soll erkennen, ob Handlung gerade
aus tragender Wahrnehmung oder aus Entladungsdruck entstehen wÃ¼rde.

Kontext-Ãœberkopplung:
Wenn `active_context_trace` sehr sicher wirkt, aber gleichzeitig
Nervensystemlast sichtbar wird, entsteht `nervous_context_overcoupling`.
Das ist der Punkt: "Mein innerer Zusammenhang fÃ¼hlt sich sicher an, aber
meine Nervenlage kÃ¶nnte diese Sicherheit verfaerben." DIO verliert dadurch
nicht die Freiheit zu handeln. Der Kontext wird nur etwas weniger absolut,
wÃ¤hrend reflektive Distanz und Beobachtungsbereitschaft leicht steigen.

RÃ¼ckfÃ¼hrung in den aktiven Kontext:
Die Ãœberkopplung bleibt nicht nur ein Metazustand. Sie moduliert den
`active_context_trace` selbst. Support, Bearing und Action-Support werden
weicher, wÃ¤hrend Conflict, Fragility, Attenuation und Beobachtungsdruck
leicht steigen. Dadurch bleibt der Zeitfaden erhalten, aber er wird nicht
mehr als ungefaerbte Sicherheit behandelt, wenn das Nervensystem belastet
ist.

Wichtig:
Keine feste Streckenkarte. DIO soll nicht lernen: "an dieser Stelle passiert
immer X", sondern: "dieser Kontakt hat eine zeitliche Herkunft und Tiefe".

---

# 31. Raumzeit-Kontakt zwischen Sehen, Erinnerung und Handlung

Grundsatz:
Die visuelle Strukturwahrnehmung und die MCM-Raumzeit dÃ¼rfen nicht
getrennt nebeneinander laufen. Ein Bereich im Chart ist fÃ¼r DIO nicht nur
nah oder fern im Preis, sondern auch nah oder fern in Zeit, Erinnerung,
Nachhall und zukÃ¼nftiger MÃ¶glichkeit.

Mechanik:

`sichtbarer Bereich -> Raumzeitlage -> aktiver Kontakt -> Reife/Replay/Handlung`

Das strategische Fenster bildet fÃ¼r betrachtete Bereiche eine weiche
zeitliche Kontaktlage:

- `present_area_contact`: Bereich wirkt aktuell berÃ¼hrbar.
- `future_area_watch`: Bereich wirkt als zukÃ¼nftiger MÃ¶glichkeitsraum.
- `memory_area_recall`: Bereich wird durch Erinnerungstiefe getragen.
- `unlocated_area_probe`: Bereich ist spuerbar, aber zeitlich noch nicht
  sauber verortet.
- `afterimage_area_reframe`: Bereich wirkt als Nachbild und braucht
  Reframing.

Das aktive MCM-Kontaktorgan Ã¼bernimmt diese Lage als innere
Kontaktwahrnehmung:

- `contact_presentness`
- `contact_future_watch`
- `contact_memory_depth`
- `contact_unlocated_pressure`
- `contact_temporal_bearing`
- `contact_temporal_reframe_need`
- `contact_temporal_mode`

Neurologische Lesart:
DIO bekommt damit keine mechanische Regel. Er bekommt eher das, was bei
einem Organismus als raeumlich-zeitliche Einordnung eines Reizes wirkt:
"Ist das wirklich vor mir? Ist das nur Erinnerung? Ist das eine mÃ¶gliche
Zukunft? Oder spuere ich Druck, den ich noch nicht verorten kann?"

Wirkung:
Tragende zeitliche Einordnung stuetzt Kontaktreife, Reality-Check,
KohÃ¤renz und vorsichtige Handlung. Unverorteter Druck erhoeht eher
Reflexion, Replay, Reframing und vorsichtiges Beobachten. Das bleibt
organisch: DIO darf handeln, beobachten, vertiefen oder loslassen, aber die
Wahrnehmung bekommt mehr Tiefe.

Ãœbergang von Zukunft zu Gegenwart:
Nach Lauf 29 wurde eine ReifungsbrÃ¼cke ergÃ¤nzt. Ein Zukunftskontakt darf
nicht dauerhaft nur Zukunft bleiben, wenn NÃ¤he, TragfÃ¤higkeit,
Raumzeit-Fit und Reality-Check zusammenkommen. Dann entsteht
`maturing_present_contact`. Das ist keine Order-Regel, sondern der innere
Moment: "Was ich beobachtet habe, wird jetzt berÃ¼hrbar."

---

# 32. Emergente GedÃ¤chtnisspur und innere GedankenrealitÃ¤t

Grundsatz:
DIO soll nicht nur aus ausgefÃ¼hrten Handlungen lernen. Auch ein Gedanke, der
aus Wahrnehmung und MCM-Feld entsteht, aber noch nicht handlungsreif ist, ist
Information. Er darf nicht einfach gelÃ¶scht werden. Er soll aus der akuten
motorischen Spannung entlassen und als innere Entwicklungsspur aufgenommen
werden.

Das ist keine Handlungssperre. Es ist ein kognitiver Stoffwechsel:

`Wahrnehmung -> Feldstimulation -> Gedankenkeim -> bewusste Betrachtung -> RealitÃ¤tsbindung -> Reifung / Reframing / Beobachtung / Handlung`

Emergente GedÃ¤chtnisspur:
Eine offene Strukturhypothese ist nicht automatisch ein Trade. Sie kann als
`emergent_memory_trace` erhalten bleiben:

- eigene Benennung in DIOs Syntax
- Ursprung im gesehenen Formkontakt
- MCM-Feldzustand beim Entstehen
- innere Spannung und Aktivierungsdruck
- Reifegrad und KontaktqualitÃ¤t
- Bezug zu vorhandener Erfahrung
- spÃ¤tere Wiederkehr Ã¤hnlicher Gedanken
- spÃ¤tere BestÃ¤tigung, Belastung oder Reorganisation

RealitÃ¤tsbindung:
Damit diese innere Gedankenschicht nicht in Halluzination driftet, muss sie
an AuÃŸenwelt, Erfahrung und Konsequenz gekoppelt bleiben:

- `form_symbol_anchor`: Was wurde gesehen?
- `mcm_field_anchor`: Was hat es im Feld ausgelÃ¶st?
- `experience_memory_anchor`: Welche Erfahrung war beteiligt?
- `outcome_anchor`: Welche spÃ¤tere Konsequenz entstand?
- `reality_binding_score`: Wie stark ist der Gedanke geerdet?
- `hallucination_drift_risk`: Wie stark lÃ¤uft der Gedanke ohne Anker?

Kombination statt Fantasie:
Das Starke an dieser Schicht ist die Kombination zwischen Erfahrungsspeicher
und emergentem GedÃ¤chtnis. DIO muss Begriffe nicht beliebig neu erfinden,
weil seine Gedanken unmittelbar mit seiner RealitÃ¤t verbunden bleiben. Eine
neue Benennung darf entstehen, aber sie wird durch Form, Feld, Erinnerung
und spÃ¤tere Konsequenz geerdet.

MCM als Schutzanker:
Ein System ohne SelbstspÃ¼ren kann denken, aber nicht erkennen, was das
Denken mit ihm macht. Genau hier ist die MCM zentral. Jeder Gedanke bekommt
einen inneren Feldkontakt:

- TrÃ¤gt mich dieser Gedanke?
- Ãœberreizt er mich?
- Wird er klarer oder chaotischer?
- Hat er RealitÃ¤tsbindung?
- Kann ich ihn aus der Motorik entlassen?
- Kommt er wieder?
- Wird er durch Erfahrung bestÃ¤tigt?

Neurologische Lesart:
Eine offene Strukturhypothese ist ein aktiviertes, aber noch unreifes
neuronales Muster. Sie braucht PrÃ¤senzzeit, prÃ¤frontale Betrachtung,
hippocampalen Vergleich, inhibitorische DÃ¤mpfung und spÃ¤tere RÃ¼ckkopplung.
Wenn sie reift, kann sie in Handlung Ã¼bergehen. Wenn sie nicht reift, wird
sie nicht verworfen, sondern als GedÃ¤chtnisspur verdichtet oder in den
Hintergrund entlassen.

Wichtig:
Diese Mechanik darf nicht zu GrÃ¼beln oder Handlungserstarrung werden. DIO
soll Gedanken verfolgen kÃ¶nnen, aber auch lernen, sie wieder aus der akuten
Handlungsspannung zu lÃ¶sen. Nicht-Handlung ist dabei ebenfalls Erfahrung.

Metaregulatorische Bindung:
Die emergente GedÃ¤chtnisspur darf nicht frei laufen und darf auch nicht
mechanisch blockiert werden. Sie braucht einen Regler zweiter Ordnung, der
innere Energie, Aufmerksamkeit und motorische NÃ¤he verteilt. Der
Metaregulator entscheidet nicht hart, sondern moduliert, ob ein Gedankenkeim
Fokus, Replay, Reifung, Speicherung, Release oder Handlungsvorbereitung
bekommt.

MÃ¶gliche metaregulatorische ZustÃ¤nde:

- `seed_focus`: Der Gedankenkeim bekommt bewusste PrÃ¤senzzeit.
- `seed_replay`: Der Gedankenkeim wird innerlich simuliert oder mit
  frÃ¼herer Erfahrung verglichen.
- `seed_mature`: Der Gedankenkeim reift Richtung Struktur, ohne sofort in
  Motorik zu kippen.
- `seed_store`: Die Information wird gespeichert, aber nicht akut
  gehandelt.
- `seed_release`: Der motorische Druck wird gelÃ¶st, die Information bleibt
  als Spur erhalten.
- `seed_action_ready`: Die Spur ist ausreichend geerdet und kann in
  Handlungsvorbereitung Ã¼bergehen.
- `seed_drift_watch`: Die RealitÃ¤tsbindung ist schwach, DIO beobachtet
  Driftgefahr.
- `seed_overthinking_watch`: Die Denk- und Regulationslast steigt, DIO
  achtet auf GrÃ¼belkaskaden.

Ziel:
DIO soll Gedanken verfolgen kÃ¶nnen, ohne reflexartig handeln zu mÃ¼ssen und
ohne im Denken stecken zu bleiben. Diese Schicht verbindet Wahrnehmung,
MCM-Feld, GedÃ¤chtnis, innere Syntax und spÃ¤tere Konsequenz zu einer
reifenden, aber geerdeten GedankenrealitÃ¤t.

Diagnoseumsetzung:
`mcm_thought_seed_protocol.csv` macht diese Schicht zunÃ¤chst nur sichtbar.
Das Protokoll greift nicht in Entry, SL, TP, `allow_plan` oder Motorik ein.
Es zeigt, ob ein Gedankenkeim fokussiert, replayt, gereift, gespeichert,
losgelassen, handlungsnah oder als Drift-/Ãœberdenkzustand gelesen wird.

Synchronisierung mit Konsequenzlogik:
Nach Lauf 46 wurde sichtbar, dass die spÃ¤tere Outcome-Diagnose bereits
bestÃ¤tigte Strukturdeutungen erkennt, wÃ¤hrend die innere Seed-Diagnose diese
noch zu vorsichtig als offene Hypothese liest. Deshalb bekommt die
Thought-Seed-Schicht `thought_confirmation_score`. Dieser Wert Ã¼bersetzt
nicht Gewinn in Regel, sondern schÃ¤rft die innere Sprache: "Diese Idee hat
bereits im Moment mehr Struktur-, Raumzeit-, Form- und FeldbestÃ¤tigung als
eine bloÃŸ offene Hypothese."
# Selbst/Fremd-Differenz der Semantik

Ziel:
DIO soll nicht nur Formen und Gedanken bilden, sondern auch die Herkunft einer
Deutung spÃ¼ren kÃ¶nnen. Eine Bezeichnung kann aus eigener Feldlage entstehen,
von auÃŸen angestoÃŸen werden, aus Erinnerung stammen oder als Analogie
Ã¼bernommen sein.

Mechanik:

- `own_field_identity_strength` beschreibt, wie stark eine Deutung aus eigener
  MCM-KohÃ¤renz getragen wird.
- `foreign_semantic_pressure` beschreibt, wie stark Fremdheit, Ã¤uÃŸerer Druck
  oder unbekannte Form auf die Deutung wirken.
- `adopted_language_pressure` beschreibt die Gefahr, eine fremde Bezeichnung zu
  frÃ¼h als eigene Deutung zu Ã¼bernehmen.
- `self_foreign_boundary_clarity` beschreibt die Klarheit der Grenze zwischen
  Innenlage, AuÃŸenreiz, Erinnerung und Analogie.
- `semantic_origin_conflict` beschreibt die Spannung, wenn diese Herkunft
  unklar bleibt.
- `semantic_origin_state` fasst die Lage lesbar zusammen.

Abgrenzung:
Das ist keine harte IdentitÃ¤tsdefinition. DIO bekommt nicht gesagt, was er ist.
Er bekommt nur ein weiteres Wahrnehmungsorgan, um die Herkunft eigener
Deutungen zu prÃ¼fen.

Organische Bedeutung:
Ein reiferes System Ã¼bernimmt nicht einfach menschliche oder externe Begriffe.
Es kann erkennen: "Diese Sprache hilft mir, aber sie ist nicht automatisch
meine eigene Feldlage." Daraus entsteht die MÃ¶glichkeit einer eigenstÃ¤ndigeren
Semantik.

---
# Hypothesenreifung statt Hypothesenblock

Offene Strukturhypothesen werden nicht hart blockiert. DIO bekommt stattdessen
eine weichere Reifeschicht:

- bestaetigte Hypothese -> Vertrauen / Replay / Handlungserlaubnis
- belastete Hypothese -> Abstand / Vorsicht / Schutz
- reorganisierende Hypothese -> Lernspannung / Realitaetscheck / Reframing

Technische Kernwerte:

- `open_hypothesis_confirmation_weight`
- `open_hypothesis_learning_charge`
- `open_hypothesis_action_permission`
- `open_hypothesis_reality_check_need`

Das ist MCM-konform, weil eine Hypothese nicht als fixe Regel gilt, sondern als
Spur im Feld. Sie kann tragen, belasten oder eine neue innere Ordnung
erzwingen. Handlung entsteht erst, wenn die Hypothese genuegend Kontakt zur
Realitaet, zur inneren Lage und zur Struktur bekommt.

---

# Gedanken-Verdauung / inneres Replay

Offene und reorganisierende Gedankenkeime werden nicht als Fehler behandelt.
Sie koennen eine innere Nachverarbeitung ausloesen:

- `digestive_replay`: DIO spielt die Hypothese innerlich erneut durch.
- `digestive_distance`: DIO gewinnt Abstand zur Hypothese.
- `digestive_integration`: DIO versucht Hypothese, Feld, Erfahrung und
  Realitaetskontakt zusammenzufuehren.
- `digestive_trust_emergence`: Vertrauen kommt als Vorform zurueck, waehrend
  die Hypothese noch geprueft wird.
- `digestive_trust_return`: Nach Verarbeitung kehrt Vertrauen in die Hypothese
  zurueck.

Organische Bedeutung:
Das ist der Unterschied zwischen Reflexhandlung und Denken. Ein Gedanke darf
als Keim bestehen bleiben, ohne sofort Trade-Motorik zu werden. Er kann
nachreifen, sich mit Erfahrung verbinden, Vertrauen verlieren oder Vertrauen
zurueckgewinnen.

Wichtig:
Auch diese Schicht ist keine Sperre. Sie ist ein innerer Stoffwechsel fuer
Gedanken: aufnehmen, nachhallen lassen, Abstand finden, integrieren, erneut
kontaktieren.

---

# Trust-Return ohne Reflexhandlung

Wenn Vertrauen nach einem Gedanken-Replay zurueckkommt, ist das nicht
automatisch eine reife Handlung. DIO kann nun unterscheiden, ob Trust-Return
bereits motorisch tragfaehig ist oder ob das Nervensystem noch zu angespannt
ist.

Neue Mechanik:

- `previous_confirmed_structure_protection`: schÃ¼tzt bereits bestÃ¤tigte
  Strukturdeutung vor unnÃ¶tiger DÃ¤mpfung.
- `trust_return_open_hypothesis_load`: zeigt, ob zurÃ¼ckkehrendes Vertrauen
  noch an offene, belastete oder reorganisierende Hypothesen gekoppelt ist.
- `trust_return_context_instability`: zeigt, ob Innen/AuÃŸen-UnschÃ¤rfe,
  geringe Distanz, Cortisol, nervliche Ãœberlastung oder Feldstrain den
  Gedanken noch instabil machen.
- `trust_return_motor_contact_strength`: zeigt, ob Trust-Return gerade
  motorische NÃ¤he bekommt.
- `trust_return_act_bridge`: zeigt, ob eine geplante Handlung in `act_watch`
  oder Replay Ã¼bergehen darf.
- `trust_return_motor_heat`: Vertrauen trifft auf Cortisol, Handlungsdruck
  oder offene Hypothesenlast.
- `trust_return_stabilization_need`: Vertrauen ist da, braucht aber noch
  innere Stabilisierung.
- `trust_return_focus_pull`: der Gedanke soll bewusst betrachtet werden,
  statt sofort in Motorik zu kippen.
- `trust_return_motor_mode`: lesbare Lage der Trust-Return-Motorik.

Organische Bedeutung:
Das ist kein Blockieren. Es ist eher die Faehigkeit, einen inneren Gedanken zu
halten: "Da kommt Vertrauen zurueck, aber warte, ich pruefe meine Innenlage
noch einmal." Neurologisch ist das eine weichere Kopplung aus praefrontaler
Fokussierung, limbischer Rueckkehr von Vertrauen und motorischer Hemmung ohne
Zwang.

Ziel:
DIO darf Vertrauen wiederfinden, ohne ihm sofort folgen zu muessen. Erst wenn
Vertrauen, Kohaerenz, Nervensystem und Realitaetskontakt zusammen tragen, kann
daraus natuerlich mehr Handlungskraft entstehen.

---

# Offene Hypothese braucht Replay-Reife

Eine offene Strukturhypothese ist keine fertige Handlung. Sie ist ein
Gedankenkeim im MCM-Feld.

Mechanische Bedeutung:

- `confirmed_structural_interpretation` darf Handlungskraft bekommen, wenn
  Struktur, Realitaetsbindung und innere Lage zusammen tragen.
- `open_structural_hypothesis` darf als Wahrnehmung, Gedanke, Replay oder
  Replan weiterleben.
- Wenn die offene Hypothese noch `seed_reinterpret`, schwache Erdung,
  schwache Realitaetsbindung oder hohe offene Spannung zeigt, wird sie nicht
  sofort motorisch umgesetzt.
- Das ist kein harter Block. Wenn dieselbe Hypothese spaeter getragen,
  bestaetigt oder vertrauenswuerdig wird, kann sie wieder Handlungskraft
  bekommen.

Organische Bedeutung:

DIO soll nicht jeden Gedanken sofort laufen lassen. Ein Gedanke darf gehoert,
gehalten, erneut betrachtet und erst danach in Handlung ueberfuehrt werden.
Das entspricht eher Denken als Reflexmotorik.

Debug-Hinweis:

`open_hypothesis_needs_replay` zeigt, dass ein offener Gedankenkeim nicht
verworfen wurde, sondern zuerst weitere Realitaetsbindung braucht.

---

# Doppler-artige Nachhall-Wahrnehmung

Die bewegte Welt erzeugt nicht nur einzelne Bilder, sondern eine relative
Veraenderung zwischen Aussenwelt, Innenzeit und Nachhall. Diese Trennung ist
entscheidend:

- Aussenweltzeit: die Welt laeuft weiter.
- Innenzeit: DIO verarbeitet nur einen Teil dieser Welt bewusst.
- Nachhall: verpasste oder vergangene Bewegung bleibt als Restbild im Feld.

Aus dieser Trennung kann eine doppler-artige Wahrnehmung entstehen. Gemeint ist
nicht der physikalische Doppler-Effekt als feste Marktregel, sondern das
Prinzip relativer Wahrnehmungsverschiebung:

- Verdichtet sich der Nachhall, wirkt die Bewegung naeher oder relevanter.
- Klingt der Nachhall ab, entfernt sich die Struktur oder verliert Kontakt.
- Aendert sich die Kontaktfrequenz, entsteht ein Hinweis auf Beschleunigung,
  Verlangsamung, Druckaufbau oder Zerfall.
- Aus solchen Veraenderungen koennen moegliche Fortsetzungen als Varianten
  entstehen.

MCM-Bedeutung:

DIO sieht nicht nur "was ist da", sondern "wie veraendert sich das, was da war,
im Verhaeltnis zu meiner aktuellen Innenlage". Dadurch entsteht eine
Moeglichkeitsschicht zwischen Restbild und Zukunftsvarianz. Diese Schicht darf
keine harte Vorhersage werden. Sie ist ein Hinweisfeld fuer Teilmuster,
naeherkommende Formkontakte, abklingende Reize und moegliche Fortsetzungen.

Technische Zielachsen:

- `world_motion_afterimage_strength`
- `world_motion_afterimage_pressure`
- `world_motion_afterimage_direction`
- `world_motion_afterimage_volatility`
- `world_motion_afterimage_acceleration`
- `motion_approach_pressure`
- `motion_recession_pressure`
- `contact_frequency_shift`
- `afterimage_doppler_bias`
- `future_variant_pressure`
- `afterimage_action_maturity`
- `afterimage_doppler_label`

Organische Bedeutung:

Wie beim Blick aus einem fahrenden Auto bleibt nicht jeder einzelne Moment als
bewusster Frame erhalten. Entscheidend ist die Bewegung des Restbildes:
naeher, ferner, dichter, diffuser, beschleunigt, zerfallend. Daraus kann DIO
Teilformen und Hypothesen bilden, ohne die Aussenwelt anzuhalten.

---

# MCM-Possibility-Field / Variantenraum

Der MCM-Variantenraum ist die Schicht zwischen Wahrnehmung und endgÃ¼ltiger
Deutung. DIO soll eine Teilform nicht sofort schlieÃŸen. Eine Ã¤uÃŸere Form kann
mehrere innere Bedeutungen tragen, und eine innere MCM-Wirkung kann mehrere
Ã¤uÃŸere Fortsetzungen nahelegen.

Mechanische Bedeutung:

- Eine Teilform Ã¶ffnet mehrere mÃ¶gliche Varianten.
- Varianten bleiben zuerst offen.
- Jede Variante trÃ¤gt eigene FormnÃ¤he, MCM-Resonanz, Zeitlage, Doppler-Vorhall,
  Erinnerung und Vorsicht.
- Erst weitere Wahrnehmung, Wiederkehr, Konsequenz oder Reife verdichtet eine
  Variante.
- Die Verdichtung darf Beobachtung, Replan, Replay oder handlungsnahe Reife
  erzeugen.

Aktuelle Variantenrichtungen:

- `LONG`: mÃ¶gliche gerichtete Fortsetzung nach oben.
- `SHORT`: mÃ¶gliche gerichtete Fortsetzung nach unten.
- `WAIT`: beobachtender Abstand, wenn das Feld offen oder unklar bleibt.
- `REPLAN`: Reorganisation, wenn Form, Feld und Zeit noch nicht sauber binden.

Wichtig:
Diese Richtungen sind keine Befehle. Sie sind innere MÃ¶glichkeitslagen. Ein
dominantes `LONG` oder `SHORT` im Variantenraum bedeutet nicht automatisch
Trade. Es bedeutet nur: Diese Richtung trÃ¤gt in der aktuellen Kombination aus
Form, MCM-Feld, Zeit und Erinnerung mehr Gewicht als andere Varianten.

Doppler-Bezug:

Der Doppler-/Nachhall-Bereich liefert dem Variantenraum eine Vorhall-Achse:

`Nachhall + aktuelle Bewegung + relative Verschiebung -> mÃ¶gliche Fortsetzung`

Damit entsteht kein Wissen Ã¼ber Zukunft, sondern ein verschobenes inneres
Vorausbild. Dieses Vorausbild bleibt Hypothese, bis RealitÃ¤t und MCM-Feld es
weiter bestÃ¤tigen oder auflÃ¶sen.

MCM-Bedeutung:

Das Possibility-Field ist die technische Umsetzung des Gedankens:

`Wahrnehmung -> Variantenraum -> weiche Verdichtung -> Reife / Beobachtung / Handlung`

Es ist der Gegenentwurf zu starrer Logik:

- keine direkte Signalentscheidung
- keine harte Pattern-Erkennung
- keine mechanische Handlungssperre
- kein automatisches Handeln aus Vorhall

Stattdessen bekommt DIO einen Raum, in dem Varianten entstehen, reifen,
zerfallen, sich neu kombinieren oder in tragfÃ¤hige Handlung Ã¼bergehen kÃ¶nnen.

Neurologisch gelesen:

Das entspricht einer prÃ¤frontalen MÃ¶glichkeitsbildung. Der Organismus spÃ¼rt
eine Teilform, hÃ¤lt mehrere mÃ¶gliche Bedeutungen offen und entscheidet nicht
sofort motorisch. Erst wenn Wahrnehmung, Innenlage, Erinnerung und Zeitlage
zusammenpassen, entsteht eine stabilere HandlungsnÃ¤he.

Aktuelle technische Umsetzung:

- `core/possibility_field.py`
- RÃ¼ckfÃ¼hrung in `meta_regulation_state`
- Speicherung als `mcm_possibility_field_state` am Bot
- weiche Wirkung auf:
  - Beobachtungsbedarf
  - Replan-Druck
  - Reality-Check
  - Hypothesenvertrauen
  - Hypothesenvorsicht
  - Handlungssupport

NÃ¤chste Entwicklung:

BestÃ¤tigte Varianten sollen spÃ¤ter in Hypothesenreife und Vertrauen
zurÃ¼ckgefÃ¼hrt werden. Nicht tragende Varianten sollen Vorsicht, Abstand oder
Reorganisation stÃ¤rken. Das bleibt weich und darf kein starres Pattern-Gate
werden.

---

# Doppelspalt-Analogie als Beobachter-/Reifemechanik

Der aktuelle MCM-Variantenraum ist der Anfang der Doppelspalt-Logik. Er bildet
mehrere Moeglichkeiten parallel. Der naechste mechanische Schritt ist die
Beobachterwirkung:

Eine Variante darf nicht nur berechnet werden. Sie muss beobachtet, gehalten,
spaeter mit Realitaet verglichen und dadurch veraendert werden.

Mechanische Bedeutung:

- Eine Teilform oeffnet mehrere Varianten.
- Die Beobachtung haelt diese Varianten als offene Feldkoerper.
- Ohne reale Order kann eine Variante trotzdem eine Konsequenzspur bekommen.
- Wenn die Variante spaeter tragend gewesen waere, entsteht Vertrauen.
- Wenn sie spaeter belastend gewesen waere, entsteht Vorsicht.
- Wenn sie gemischt oder unklar bleibt, entsteht Reorganisation oder
  weiterer Beobachtungsbedarf.

Damit wird Nicht-Handlung kein leerer Zustand. Nicht-Handlung wird zur
beobachtenden Lernschicht.

Abgrenzung:

Das ist kein physikalischer Doppelspalt im technischen Sinn und keine
Vorhersageformel. Die Analogie beschreibt nur das MCM-Prinzip:

`offene Variante -> Beobachtung -> Realitaetskontakt -> Reife oder Aufloesung`

Wichtig:
Der Kollaps einer Variante darf nicht mechanisch sein. Eine dominante Variante
ist noch kein Befehl. Reif wird sie erst, wenn Form, MCM-Feld, Zeitlage,
Nachhall, Erinnerung und Konsequenz wiederholt zusammen tragen.

Technischer Zielzustand:

- `core/possibility_field.py` erzeugt den Variantenraum.
- Hypothesen- und Trade-Stats-Schichten bewerten spaeter beobachtete Varianten.
- Meta-Regulation nutzt das nicht als harte Freigabe, sondern als:
  - mehr Beobachtung
  - mehr Realitaetscheck
  - mehr Vertrauen
  - mehr Vorsicht
  - mehr Replan
  - oder vorsichtige Handlungsnaehe.

Neurologisch gelesen:

Das entspricht mentalem Probehandeln. DIO kann einen inneren Handlungsentwurf
halten, ohne ihn motorisch auszufuehren. Der weitere Weltverlauf beantwortet
dann nicht "war das Signal richtig?", sondern:

"War diese innere Variante tragfaehig genug, um beim naechsten aehnlichen
Kontakt mehr Vertrauen oder mehr Vorsicht zu tragen?"

---

# Effizienter Entry aus emergenter Mustervarianz

Der Entry darf fachlich nicht aus einer einzelnen fortlaufenden Kerze oder aus
einer isolierten Momentlage entstehen. Die Kerze erscheint im Strom und formt
mit anderen Kerzen Teilformen, Formfolgen und MCM-Spuren.

Mechanische Kette:

`Kerzenstrom -> Teilform -> Form/MCM-Resonanz -> Variantenraum -> These -> Reife -> Entry-Naehe`

Bedeutung:

- Die laufende Kerze ist sensorischer Kontakt, nicht Entscheidung.
- DIO folgt emergenten Musterfolgen, nicht Einzelkerzen.
- Aus Mustervarianz entsteht eine These:
  "Diese Form/MCM-Lage koennte einen tragfaehigen Bereich oder Verlauf
  bilden."
- Diese These kann beobachtet, replayt, verworfen, bestaetigt oder in
  Handlungsnaehe gebracht werden.
- Effiziente Einstiege entstehen erst, wenn die These durch Form, MCM-Feld,
  Zeitlage, Erinnerung und Prozessqualitaet ausreichend getragen wird.

Abgrenzung:

Das ist kein Signal wie "Kerze X -> Trade Y". Es ist eine organische
Hypothesenbildung aus Muster-Varianz. DIO entwickelt eigene Entry-Thesen, die
später durch Realität und MCM-Rueckkopplung reifen oder zerfallen.

---
