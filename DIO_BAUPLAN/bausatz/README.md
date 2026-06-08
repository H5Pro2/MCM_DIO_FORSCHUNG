# DIO Bausatz

Dieser Ordner beschreibt DIO als spätere Library-Struktur.

Wichtig:

Dies ist noch kein Programm.

Es ist ein Baukasten:

- klare Module
- klare Zuständigkeiten
- klare Schnittstellen
- keine versteckte Wenn-Dann-Logik
- keine Trading-Spezialisierung im Kern
- MCM als Gefühlswahrnehmung
- Hypothese als Denk-Wahrnehmung, nicht als Wahrheit
- Strategie nur als mögliche emergente Folge, nicht als Vorgabe

## Ziel

DIO soll als wiederverwendbare Architektur gedacht werden.

Trading ist nur eine Testwelt. Der Kern soll so aufgebaut sein, dass später
auch andere Welten möglich sind:

- Chartdaten
- Sensorik
- Robotik
- optische Wahrnehmung
- andere sequenzielle Umwelten

## Modulordnung

```text
00_contracts
01_world
02_seeing
03_mcm_field
04_memory
05_thought
06_reality_check
07_action
08_consequence
09_regulation
10_neurons
11_neurochemistry
12_language
13_time_space
14_debug
```

## Grundregel

Jedes Modul macht eine Sache.

Wenn ein Modul mehrere Ebenen vermischt, wird es später nicht direkt umgesetzt,
sondern zuerst aufgeteilt.

## Datenfluss

```text
World
-> Seeing / Hearing
-> MCM Field
-> Memory
-> Thought
-> Reality Check
-> Action
-> Consequence
-> Regulation
```

`02_seeing` ist fachlich die Sinnesaufnahme. Sie enthält sichtbare Form und
hörbare Marktmelodie, damit kein zweites Sinnesmodul parallel entsteht.

Neuron, Neurochemie, Sprache und Raumzeit sind keine Seitenteile.
Sie wirken als Querschnittsbausteine im ganzen Baukasten.
