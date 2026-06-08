# 25 Bausatz-Struktur

Diese Datei beschreibt den Ãœbergang vom Textbauplan zu einer spÃ¤teren Library.

## Ziel

DIO soll nicht als Monolith neu aufgebaut werden.

DIO soll als Bausatz entstehen:

- Module
- Contracts
- ZustÃ¤nde
- klare Ãœbergaben
- austauschbare Welten
- keine versteckten Entscheidungsregeln im Kern
- MCM als GefÃ¼hlswahrnehmung
- Hypothesen als Denk-Wahrnehmung
- Strategie nur als emergente Folge, nicht als Vorgabe

## Technischer Ort

Die Bausatzstruktur liegt unter:

```text
DIO_BAUPLAN/bausatz/
```

## Wichtig

Der Bausatz ist noch kein Programm.

Er ist eine technische Landkarte.

Er zeigt:

- welche Teile DIO braucht
- welche Verantwortung jedes Teil hat
- wo spÃ¤tere Codebausteine einsortiert werden
- was ein Modul nicht tun darf

## SpÃ¤tere Library-Idee

Eine spÃ¤tere Library kÃ¶nnte so aufgebaut sein:

```text
dio/
  contracts/
  world/
  seeing/
  mcm_field/
  memory/
  thought/
  reality_check/
  action/
  consequence/
  regulation/
  neurons/
  neurochemistry/
  language/
  time_space/
  debug/
```

Der aktuelle Ordner `DIO_BAUPLAN/bausatz` beschreibt diese Struktur nur schriftlich.

`seeing/` ist dabei bewusst kein rein optisches Modul. Es ist die
Sinnesaufnahme fÃ¼r sichtbare Form und hÃ¶rbare Marktmelodie. Dadurch entsteht
kein zweiter paralleler Wahrnehmungsbauplan.

## PrÃ¼fregel

Bestehender Code wird spÃ¤ter nicht einfach verschoben.

Zuerst wird jede Funktion gefragt:

```text
Welche Baukasten-Rolle erfÃ¼llst du?
Welche Eingabe brauchst du?
Welche Ausgabe gibst du?
Vermischst du Welt, Thought, Regulation oder Handlung?
```

Wenn eine Funktion mehrere Rollen vermischt, ist sie ein RÃ¼ckbaukandidat.
