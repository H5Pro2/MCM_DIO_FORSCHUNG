# MD_ANWEISUNG

Diese Datei legt fest, welche Markdown-Dateien aktiv sind und welche nur noch
historische Referenz sind. Ziel ist weniger Doppelpflege und ein klarer
Konstruktionspfad für DIO.

## Aktiver Bauplan

Die einzige aktive Bauanleitung und der spätere Konstruktionsplan liegen hier:

- `DIO_2/konstruktion/README.md`
- `DIO_2/konstruktion/00_BAUPLAN.md`
- `DIO_2/konstruktion/01_WELT.md` bis `10_KORTEX.md`
- `DIO_2/konstruktion/12_ARBEITSSPUR.md`
- `DIO_2/konstruktion/28_UEBERTRAGUNGSMATRIX_CODE.md`

Es gibt keine zweite aktive Anleitung in `docs/`.

## Archiv

Die alten Hauptdateien sind nicht gelöscht, sondern verschoben:

- `docs/99_temp_alt/01_plan/UMSETZUNGSPLAN.md`
- `docs/99_temp_alt/01_plan/BAUPLAN_BRUECKE_ALT.md`
- `docs/99_temp_alt/02_status/FIX_LISTE.md`
- `docs/99_temp_alt/02_status/FIX_LISTE_ARCHIV.md`

Diese Dateien sind nur historische Referenz. Neue Architektur, neue Mechaniken
und neue Arbeitsstände werden dort nicht mehr ergänzt.

## Zuständigkeiten

`README.md`

- Einstieg für Menschen
- kurze Begriffsklärung
- grobe Architektur
- Verweise auf aktive Konstruktionsdateien

`DIO_2/konstruktion/`

- aktive Konstruktionslogik
- Schichtenmodell
- Bausteine, Code-Skizzen und spätere Übertragungsmatrix
- Ort für neue Architekturentscheidungen

`docs/02_status/AKTUELLER_STAND.md`

- kurzer realer Projektzustand
- keine lange Laufhistorie
- keine doppelte Arbeitsspur

`docs/02_status/ARBEITSSPUR.md`

- kein zweiter Arbeitsplan
- nur Verweis auf `DIO_2/konstruktion/12_ARBEITSSPUR.md`

`docs/03_mechanik/`

- technische Mechanik-Erklärung
- Variablen, Rezeptoren, MCM-Wirkpfade
- keine Chat-Mitschriften
- keine langen Laufberichte

`docs/04_berichte/`

- Erfahrungsberichte und zusammenfassende Entwicklungsberichte
- keine aktive Aufgabensteuerung

`docs/05_gui/`

- GUI-Konzept
- keine Brain-Priorität

`docs/06_struktur/`

- Projektstruktur, Refactoring, Modulverantwortung

`docs/07_konstruktion/`

- Rekonstruktionsreferenzen aus dem alten Code
- nur als technische Vergleichsbasis

## Schreibregeln

- Jede Information hat einen Hauptort.
- Laufanalysen werden nicht in mehreren Dateien ausgeschrieben.
- Beispiele des Nutzers, Prozentwerte oder Vergleichszahlen sind Beispiele,
  keine festen Regeln.
- Hypothesen sind Gedanken, nicht Realität.
- Realität ist das, was im Markt tatsächlich geschieht.
- Strategie wird nicht hart vorgegeben; sie darf nur als tragende Reaktion aus
  Form, Feld, Erinnerung, Konsequenz und Reife entstehen.
- Harte Gates werden vermieden. Hart bleibt nur die ökonomische Prüfung einer
  real ausführbaren Order.

## Pflegeablauf

Bei neuen Erkenntnissen:

1. Architektur oder Schichtidee zuerst in `DIO_2/konstruktion/` einordnen.
2. Wenn nötig, technische Mechanik in `docs/03_mechanik/` verdichten.
3. Aktive Arbeit in `DIO_2/konstruktion/12_ARBEITSSPUR.md` halten.
4. Kurzen Gesamtzustand in `docs/02_status/AKTUELLER_STAND.md` aktualisieren.
5. Alte Dateien unter `docs/99_temp_alt/` nicht weiter ausbauen.
