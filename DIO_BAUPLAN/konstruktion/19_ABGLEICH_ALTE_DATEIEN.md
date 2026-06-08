# 19 Abgleich alte Dateien

Diese Datei hÃ¤lt fest, welche wichtigen Punkte aus den alten Dokumenten in den
neuen DIO-Aufbau Ã¼bernommen wurden.

## GeprÃ¼fte Hauptquellen

- `DIO_BAUPLAN/temp_alt/docs_alt/99_temp_alt/01_plan/UMSETZUNGSPLAN.md`
- `DIO_BAUPLAN/temp_alt/docs_alt/03_mechanik/WICHTIG_MECHANIKEN.md`
- `DIO_BAUPLAN/temp_alt/docs_alt/03_mechanik/MCM_VARIABLEN_MECHANIK.md`
- `DIO_BAUPLAN/temp_alt/docs_alt/03_mechanik/MCM_REZEPTOR_MATRIX.md`
- `DIO_BAUPLAN/temp_alt/docs_alt/03_mechanik/DIO_MCM_ERWEITERUNG.md`
- `DIO_BAUPLAN/temp_alt/docs_alt/07_konstruktion/*`

## Ãœbernommene fehlende Punkte

### Formsprache und eigene Syntax

Ãœbernommen nach:

- `16_FORMSPRACHE_SYNTAX.md`

Kern:

DIO braucht eigene Formzeichen und Satzspuren. Menschliche Labels sind nur
Ãœbersetzung.

### Raumzeit, Nachhall, Doppler und Variantenraum

Ãœbernommen nach:

- `17_RAUMZEIT_VARIANTEN.md`

Kern:

DIO muss Gegenwart, Erinnerung, Nachhall, Erwartung und Hypothese zeitlich
unterscheiden. Varianten sind MÃ¶glichkeiten, keine Befehle.

### Rezeptorik und Selbst/Fremd-Grenze

Ãœbernommen nach:

- `18_REZEPTORIK_UND_GRENZEN.md`

Kern:

Ãœberlappungen sind erlaubt, wenn Ebene, Zeitlage, Rezeptor oder Speicherpfad
klar getrennt sind. DIO muss eigene und fremde Deutung unterscheiden.

### MCM-Spannungsachse und Zero Point

Ãœbernommen nach:

- `20_SPANNUNGSACHSE_ZERO_POINT.md`

Kern:

Positive und negative Spannung sind beide FeldzustÃ¤nde. RÃ¼ckfÃ¼hrung zum
Zero Point ist Selbstkontakt, keine Belohnungsregel.

### Kontaktreife und Beobachtungslernen

Ãœbernommen nach:

- `21_KONTAKTREIFE_BEOBACHTUNG.md`

Kern:

Nicht-Handlung, Beobachtung und ausgelassene Trades sind echte Erfahrungsspuren.
Kontaktreife entsteht aus Konsequenz und Reife, nicht aus Verbot.

### Position und Beteiligung

Ãœbernommen nach:

- `22_POSITION_UND_BETEILIGUNG.md`

Kern:

Eine offene Position ist reale Beteiligung. Sie erzeugt Positionslast,
Exit-Druck, ProzessqualitÃ¤t und Konsequenzspuren.

### OrganÃ¼bersicht

Ãœbernommen nach:

- `23_ORGANUEBERSICHT.md`

Kern:

DIO wird als Zusammenspiel mehrerer Funktionsorgane beschrieben, nicht als
einzelner Entscheidungsblock.

### Variablenmechanik und Rezeptormatrix

Ãœbernommen nach:

- `29_VARIABLEN_UND_WIRKPFAD.md`

Kern:

Die alte Variablenmechanik wurde nicht 1:1 kopiert, sondern als aktive
Wirkpfad-Ordnung verdichtet: Variable, Ebene, Rezeptorfamilie, Wirkung,
Zielregler, Speicherpfad und verbotene Doppelwirkung.

### WICHTIG_MECHANIKEN als geprüfte Quelle

Übernommen nach:

- `30_MECHANIK_ABGLEICH_WICHTIG.md`

Kern:

Die alte `WICHTIG_MECHANIKEN.md` bleibt wertvolle Historie, aber keine aktive
Arbeitsdatei. Der Abgleich hält fest, welche Punkte bereits im Bauplan liegen,
welche Begriffe nur Übergangs-Kompatibilität sind und welche alten Muster
nicht wieder aktiviert werden dürfen.

## Bereits ausreichend vorhanden

Diese Punkte waren im neuen Aufbau bereits sauber genug enthalten:

- Welt als reale AuÃŸenwelt
- Sehen als Formspur, nicht Handlung
- MCM-Feld als Spannungsraum, nicht Signalgeber
- Memory als reale Erfahrung
- Thought als Gedankenspur
- RealitÃ¤tsprÃ¼fung zwischen Gedanke, Welt und MCM
- Handlung nur aus tragender NÃ¤he
- Konsequenz als RÃ¼ckkopplung
- Neurochemie als Feldmodulation
- MCM-Neuron als lokaler Wirkpunkt
- Variablen werden Ã¼ber Wirkpfad und Rezeptorfamilie geprÃ¼ft

## Noch offen fÃ¼r Code-Abgleich

1. Bestehende Funktionen den neuen Schichten zuordnen.
2. Doppelte Zielregler nach Rezeptorfamilie prÃ¼fen.
3. Hypothesenpfad gegen RealitÃ¤tstrennung prÃ¼fen.
4. Core-Daten auf Welt, Sehen und MCM-Feld reduzieren.
5. Debug-Ausgaben an die neuen Schichten anpassen.
