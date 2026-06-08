# ==================================================
# FIX-LISTE â€“ AKTUALISIERT AUF REALEN CODESTAND
# ==================================================

Diese Liste enthÃ¤lt nur noch reale offene Punkte aus dem aktuellen Dateistand.

Bereits umgesetzte Korrekturen wurden aus dem offenen PRIO-1-Block entfernt.
Architektur-Ausbau und fachlicher Ausbau bleiben getrennt.

---

# --------------------------------------------------
# 0. AKTUELLER FIX AUS DEM NEUESTEN DEBUG
# --------------------------------------------------

Abgeschlossen:

- [x] `docs/03_mechanik/WICHTIG_MECHANIKEN.md` als Mechanik-Schatzkammer eingeordnet.
  Ergebnis: Die Datei bleibt erhalten, wird aber nicht mehr als tagesaktueller
  Umsetzungsplan gelesen. Ein Statusblock erklÃ¤rt, dass sie ein Konzeptarchiv
  fÃ¼r wichtige MCM-Denkspuren ist und beim Lesen mit neueren Mechaniken wie
  Formsprache, Transfer-TragfÃ¤higkeit, Beobachtungslernen, ProzessqualitÃ¤t
  und DIO zusammengedacht werden muss.
- [x] `README.md` um MCM als Spannungsraum ergÃ¤nzt.
  Ergebnis: Der Chart wird fachlich als Ã¤uÃŸerer Spannungsverlauf beschrieben,
  der im MCM-Innenfeld Druck, Entlastung, Resonanz, TragfÃ¤higkeit,
  Regulationslast, Beobachtungsbedarf und Handlungstendenz erzeugt. Zudem
  wurden im bearbeiteten README-Bereich Umlaute sauber korrigiert.
- [x] Automatische Debug-Laufordner eingebaut.
  Ergebnis: Neue Backtests schreiben Debug-Dateien automatisch nach
  `debug/debug_lauf_X`. Zentrale alte Pfade werden Ã¼ber `debug_reader.py`
  auf den aktuellen Laufordner umgeleitet.
- [x] Debug nach Split `symbolic_inner_regulation` / `symbolic_action_regulation` geprÃ¼ft.
  Ergebnis: handlungsnahe Sprachentlastung bleibt klein; der Lauf ist deutlich besser
  als der vorherige Absturz, aber mit ca. -1.47 Netto-PnL noch nicht tragfÃ¤hig.
- [x] Struktur-TragfÃ¤higkeitsfilter vor Handlung eingebaut.
  Ergebnis: `structure_action_bearing` und `structure_action_gap` ergÃ¤nzen die MCM-
  Entscheidung. Schwache/mittlere Struktur mit fehlendem Support wird eher beobachtet
  statt gehandelt.
- [x] Kompositorische Formsprache eingebaut.
  Ergebnis: Einzelne Formzeichen kÃ¶nnen sich zu `form_symbol_compound`-Objekten
  verbinden. Diese zusammengesetzten Zeichen besitzen eigene Reife, StabilitÃ¤t,
  Resonanz, TragfÃ¤higkeit und Lastreduktion. Sie wirken weich als kognitive
  Verdichtung und nicht als harte Pattern-/Handelsregel.

Nach nÃ¤chstem Backtest prÃ¼fen:

- [ ] PnL / Profit Factor
- [ ] Tradezahl und withheld/observe/act-Verteilung
- [ ] High/Mid/Low-Strukturverteilung
- [ ] neue Gruende `development_reframe_observe`, `development_reframe_replan`,
  `structure_bearing_observe` und `structure_development_observe`
- [ ] ob gute Mid-Setups zu stark in Beobachten/Reframing gezogen werden
- [ ] `form_symbol_compound_count`, Compound-Reife und Compound-Lastreduktion
- [ ] ob zusammengesetzte Zeichen die innere Last senken, ohne `act` zu stark zu erleichtern
- [ ] neue Werte `form_symbol_action_binding`, `form_symbol_observation_binding`,
  `form_symbol_reframe_binding` und `learned_development_uncertainty`

Neu aus dem letzten Debug:

- [x] Kompositorische Formsprache im ersten Lauf geprÃ¼ft.
  Ergebnis: Profit Factor ca. 1.05, Netto-PnL ca. +0.90. Compounds entstehen und
  bleiben noch jung/leicht, also keine harte Ãœbersteuerung.
- [x] Low-Struktur als organische Unsicherheit nachgeschaerft.
  Ergebnis: `structure_action_uncertainty` erhoeht Beobachtungsbedarf und
  Handlunghemmung weich, ohne Low-Struktur technisch absolut zu verbieten.
- [x] Entwicklungsbindung statt Blocker eingebaut.
  Ergebnis: Formzeichen und zusammengesetzte Zeichen lernen aus Ergebnis- und
  ProzessqualitÃ¤t eine weiche `development_quality`, `action_affinity`,
  `observation_affinity` und `context_reframe_potential`. Schwache Erfahrung
  verbietet eine Form nicht, sondern senkt ihre Handlungsanziehung und erhoeht
  Beobachten/Reframing. Das entspricht dem Ziel: Freiheit statt harter Blocker.
- [ ] Nach nÃ¤chstem Lauf prÃ¼fen, ob Low-Struktur-Trades durch gelernte
  EntwicklungsqualitÃ¤t von selbst seltener werden und ob High/Mid weiterhin
  frei genug handeln kÃ¶nnen.
- [x] `debug_lauf_2` nach Entwicklungsbindung geprÃ¼ft.
  Ergebnis: Netto-PnL ca. +7.89, Profit Factor ca. 1.39. High und Mid sind
  positiv, Low bleibt negativ. Die neue Entwicklungsbindung ist im Formprotokoll
  sichtbar, aber im Denkprotokoll fehlten noch die Spalten.
- [x] Denkprotokoll fÃ¼r Entwicklungsbindung erweitert.
  Ergebnis: Ab dem nÃ¤chsten Lauf schreibt `mcm_memory_thinking_protocol.csv`
  auch `form_symbol_development_quality`, `form_symbol_action_binding`,
  `form_symbol_observation_binding`, `form_symbol_reframe_binding` und
  `learned_development_uncertainty`.
- [x] `debug_lauf_3` geprÃ¼ft und Entwicklungsbindung nachgeschaerft.
  Ergebnis: PnL ca. -2.40, High/Mid bleiben positiv, Low verursacht ca. -12.47.
  `learned_development_uncertainty` ist messbar, aber noch zu schwach gekoppelt.
  Reframing-Schwelle wurde weicher/frÃ¼her gemacht und die Wirkung auf
  Beobachtung, Replan-Druck und Handlungsbindung leicht verstÃ¤rkt.
- [x] `debug_lauf_4` geprÃ¼ft und Verlustintensitaet ins Lernen aufgenommen.
  Ergebnis: Low-Trades sinken von 23 auf 9, bleiben aber mit 0 TP / 9 SL zu teuer.
  Neu: `risk_width_pressure` verstÃ¤rkt bei breiten SL-Verlusten die negative
  EntwicklungsrÃ¼ckmeldung, ohne daraus einen harten Blocker zu machen.
- [x] `debug_lauf_5` geprÃ¼ft und Handlungsbindung plastischer gemacht.
  Ergebnis: High sehr positiv, Mid fast neutral, Low wieder zu hÃ¤ufig und negativ.
  Die Formsprache lernt negative QualitÃ¤t, aber `action_affinity` blieb zu neutral.
  Anpassung: negative Entwicklungsproben und `risk_width_pressure` senken die
  Handlungsanziehung stÃ¤rker; Beobachtungs-/Reframe-Bindung reduziert
  `form_symbol_action_binding` weich.
- [x] `debug_lauf_6` geprÃ¼ft und Outcome-Debug fÃ¼r Formbindung erweitert.
  Ergebnis: Gesamt-PnL wieder positiv, High stark, Mid leicht positiv, Low weiterhin
  0 TP / 15 SL. `development_reframe_observe` steigt deutlich. Ab nÃ¤chstem Lauf
  schreibt `outcome_records.jsonl` die Form-ID und Form-Bindungswerte direkt mit,
  damit Low-Verluste einzelnen internen Zeichen zugeordnet werden kÃ¶nnen.
- [x] `debug_lauf_7` geprÃ¼ft und Form-Kontext-Fallback eingebaut.
  Ergebnis: PnL ca. +4.30, High/Mid positiv, Low weiter 0 TP / 16 SL.
  Die Formfelder im Outcome waren noch leer, weil der Entry-Kontext teils ein
  leeres `form_symbol_state` bekam. Fallback auf `bot.form_symbol_state`
  eingebaut, damit Lauf 8 Low-Verluste nach interner Form gruppierbar macht.
- [x] `debug_lauf_8` geprÃ¼ft und Vertrauensschicht fÃ¼r Formsprache eingebaut.
  Ergebnis: PnL ca. +0.30, High/Mid positiv, Low weiter 0 TP / 13 SL.
  Befund: Varianz ist vorhanden, aber die gelernte Erfahrung wird noch nicht
  stabil genug als Vertrauen gebunden. Neu: `learning_trust`, `action_trust`
  und `caution_trust` fÃ¼r Einzel- und Compound-Zeichen. Ziel: Nicht auswendig
  lernen, sondern konsistenter der eigenen Erfahrung vertrauen.
- [x] `debug_lauf_9` geprÃ¼ft und Vorsichtsvertrauen konsolidiert.
  Ergebnis: PnL ca. +0.96, High stark, Low weiterhin 0 TP / 11 SL, Mid negativ.
  `learning_trust` entsteht, aber `caution_trust` ist noch zu zart. Wiederholte
  negative Erfahrung und `risk_width_pressure` stÃ¤rken nun `caution_trust`
  schneller; `caution_trust` reduziert Handlungsbindung etwas deutlicher.
- [x] `debug_lauf_10` geprÃ¼ft.
  Ergebnis: PnL ca. +3.43, Profit Factor ca. 1.30, Drawdown ca. 2.20.
  High und Mid positiv, Low weiter negativ aber weniger teuer. Trust-Schicht zeigt
  erste Stabilisierung. Keine weitere Code-Nachschaerfung, erst Lauf 11 zur
  StabilitÃ¤tsprÃ¼fung.
- [x] `debug_lauf_11` geprÃ¼ft.
  Ergebnis: PnL ca. +5.16, Profit Factor ca. 1.32. High und Mid positiv,
  Low weiter negativ. `learning_trust` und `caution_trust` steigen weiter.
  Kein Code-Fix, weil zwei positive LÃ¤ufe in Folge auf Stabilisierung hindeuten.
- [x] `debug_lauf_12` geprÃ¼ft.
  Ergebnis: PnL ca. +11.23, Profit Factor ca. 1.73. High trÃ¤gt massiv,
  Low bleibt negativ, Mid leicht negativ. Keine Code-Aenderung, weil die Trust-
  Schicht gerade einen starken StabilitÃ¤tsbefund zeigt.
- [x] `debug_lauf_13` und `debug_lauf_14` geprÃ¼ft.
  Ergebnis: PnL fÃ¤llt von ca. +11.23 auf +7.22 und +2.87. Die Kurve entsteht
  nicht durch einen kompletten Systembruch, sondern durch weniger High-Trades
  und weiter negative Non-Zone-/Low-Handlungen. Zone bleibt positiv
  (`lauf_14`: ca. +12.43), Non-Zone bleibt 0 TP / 15 SL und ca. -9.55.
- [ ] NÃ¤chster Fix: Transfer-TragfÃ¤higkeit technisch vorbereiten.
  Ziel: fremde/nicht tragende Struktur soll nicht hart geblockt werden,
  aber Erfahrung darf nur proportional zur TragfÃ¤higkeit in Handlung Ã¼bertragen
  werden. Besonders Non-Zone/Low braucht mehr Reframing, Beobachtung oder
  kleinere kontrollierte Handlung statt voller HandlungsÃ¼bertragung.
- [x] `debug_lauf_15` geprÃ¼ft.
  Ergebnis: PnL ca. +15.90, Profit Factor ca. 1.97, Drawdown ca. 1.96.
  Lauf 15 dreht die Kurve stark nach oben. Zone trÃ¤gt ca. +24.08 PnL,
  High ca. +18.91 und Mid ca. +5.17. Non-Zone/Low bleibt aber 0 TP / 13 SL
  und ca. -8.18 PnL. Befund: Trust/Formbindung kann tragende Erfahrung wieder
  aktivieren, aber Transfer-TragfÃ¤higkeit fÃ¼r fremde/nicht tragende Struktur
  bleibt der nÃ¤chste offene Fix.
- [x] Beobachtungslernen als Reifeschicht umsetzen.
  Ziel: Low/Non-Zone soll nicht nur weniger handeln, sondern aus bewusstem
  Zusehen lernen. Beobachtung wird damit zu einer eigenen Erfahrungsspur:
  Was wÃ¤re passiert, wenn gehandelt worden wÃ¤re? War Nicht-Handlung reifer
  als Aktion? Daraus soll spÃ¤ter `maturity_trust` bzw. Beobachtungsreife
  entstehen, ohne harte Low-Sperre.
  Umsetzung: `TradeStats` fÃ¼hrt jetzt `pending_observations`,
  `observation_learning` und `recent_observation_learning`. Beobachtete
  Non-Zone/Low-Situationen werden virtuell weiterverfolgt und als
  `saved_loss`, `missed_gain` oder `neutral` bewertet. `observation_maturity_trust`
  und `observation_action_pressure` fliessen weich in die Entscheidungsneigung
  und werden im Denkprotokoll sichtbar.
- [ ] NÃ¤chsten Lauf prÃ¼fen:
  `observation_learning`, `observation_maturity_trust`,
  `observation_action_pressure`, Low/Non-Zone-Trades, Zone/High/Mid-PnL und
  ob die gute Zone frei bleibt.
- [x] `debug_lauf_16` geprÃ¼ft.
  Ergebnis: PnL ca. +11.11, Profit Factor ca. 1.62, 54 Trades. High/Zone
  trÃ¤gt weiter deutlich, aber Non-Zone/Low bleibt mit 0 TP / 20 SL und
  ca. -12.05 PnL der klare Schmerzkanal. Das System ist nicht zusammengebrochen,
  aber die Reifeschicht hat im echten Lauf noch nicht gelernt.
- [x] Beobachtungslernen nach Lauf 16 diagnostiziert.
  Ergebnis: `observation_learning.low_observations`, `saved_loss`,
  `missed_gain` und `observation_maturity_trust` blieben 0. Ursache:
  beobachtete Low-/Non-Zone-Situationen kamen im Attempt-Kontext oft als
  `WAIT` mit Entry/SL/TP = 0 an. Damit gab es keine virtuelle Handlungsbahn,
  aus der Zusehen lernen konnte.
- [x] Virtuellen Beobachtungsplan eingebaut.
  Ergebnis: Nicht freigegebene LONG-/SHORT-Tendenzen erzeugen jetzt einen
  `virtual_observation_plan`. Der Attempt-Kontext fÃ¼hrt eine
  `proposed_decision`, damit Beobachtung trotz realem `WAIT` spÃ¤ter als
  `saved_loss`, `missed_gain` oder `neutral` bewertet werden kann. Keine harte
  Low-Sperre, sondern organisches Beobachtungslernen.
- [ ] NÃ¤chsten Lauf prÃ¼fen:
  `observation_learning.low_observations`, offene/aufgelÃ¶ste Beobachtungen,
  `saved_loss`, `missed_gain`, `observation_maturity_trust`,
  `observation_action_pressure`, Low/Non-Zone-Trades und ob Zone/High frei
  genug bleiben.
- [x] `debug_lauf_17` geprÃ¼ft.
  Ergebnis: PnL ca. +12.09 bei 42 Trades. Gegen Lauf 16 weniger Trades und
  leicht besseres Ergebnis. Zone bleibt tragend mit ca. +20.15 PnL, Non-Zone
  bleibt negativ mit ca. -8.07 PnL.
- [x] Beobachtungslernen nach Lauf 17 erneut diagnostiziert.
  Ergebnis: Die Werte blieben weiterhin bei 0. Grund: `meta_regulation_state`
  enthielt bei Observe/Withhold teils LONG/SHORT, aber `trade_plan.decision`
  blieb WAIT und Entry/SL/TP blieben 0. Die innere Richtung wurde also noch
  nicht als virtuelle Beobachtungsbahn konserviert.
- [x] Ãœberschreibung von `proposed_decision` korrigiert.
  Ergebnis: Bei reifem Beobachten bleibt die reale Handlung `WAIT`, wÃ¤hrend
  die innere Beobachtungsrichtung LONG/SHORT erhalten bleibt. Dadurch kann der
  virtuelle Beobachtungsplan im nÃ¤chsten Lauf in `TradeStats` ankommen.
- [ ] Lauf 18 prÃ¼fen:
  `observation_learning.low_observations`, `pending_observations`, `resolved`,
  `saved_loss`, `missed_gain`, `maturity_trust`, `action_pressure`, Tradezahl
  und Non-Zone/Low-PnL. Lauf 18 ist der erste echte Nachweis fÃ¼r die
  vollstÃ¤ndige Beobachtungslernmechanik.
- [x] `debug_lauf_18` geprÃ¼ft.
  Ergebnis: PnL ca. +14.19 bei 37 Trades. Gegen Lauf 17 erneut weniger
  Trades und besseres Ergebnis. Zone trÃ¤gt ca. +20.27 PnL. Non-Zone bleibt
  negativ, aber reduziert auf 11 Trades und ca. -6.08 PnL.
- [x] Beobachtungslernen nach Lauf 18 erneut diagnostiziert.
  Ergebnis: `observation_learning` blieb wieder bei 0. Non-Zone-Observe,
  Withhold und Skip kamen weiter ohne Entry/SL/TP an. In vielen FÃ¤llen gab es
  keine explizite LONG-/SHORT-Hypothese mehr, sondern nur noch ein schwaches
  Signalbild.
- [x] Signalbasierte Beobachtungshypothese eingebaut.
  Ergebnis: Der Attempt-Kontext fÃ¼hrt jetzt `world_state.current_price` und
  `world_state.candle_state`. `TradeStats` kann aus Non-Zone + Preis +
  Signalspannung eine virtuelle Beobachtungshypothese erzeugen. Das ist kein
  echter Trade und kein harter Blocker, sondern eine Lernspur fÃ¼r
  Nicht-Handlung.
- [x] Mini-Mechaniktest fÃ¼r Beobachtungslernen erfolgreich.
  Ergebnis: Non-Zone + Observe + Preis + Signal erzeugt jetzt
  `low_observations = 1` und eine offene Beobachtung.
- [ ] Lauf 19 prÃ¼fen:
  `low_observations`, offene/aufgelÃ¶ste Beobachtungen, `saved_loss`,
  `missed_gain`, `maturity_trust`, `action_pressure`, Non-Zone/Low-PnL,
  Tradezahl und ob Zone/High frei genug bleiben.
- [x] `debug_lauf_19` geprÃ¼ft.
  Ergebnis: PnL ca. +13.67 bei 41 Trades. Zone trÃ¤gt ca. +19.66 PnL,
  Non-Zone bleibt mit 11 Trades und ca. -6.00 PnL negativ, aber nicht
  schlechter als Lauf 18.
- [x] Signalbasierte Beobachtungslernspur erstmals real aktiv.
  Ergebnis: `low_observations = 948`, `resolved = 948`, `saved_loss = 519`,
  `missed_gain = 424`, `neutral = 5`, `maturity_trust` ca. 0.549 und
  `action_pressure` ca. 0.447. Damit lernt das System jetzt tatsÃ¤chlich aus
  Nicht-Handlung.
- [x] Lauf 19 fachlich eingeordnet.
  Ergebnis: Low/Non-Zone ist nicht einfach schlecht, sondern ein ambivalenter
  Spannungsraum. Mehr als die Haelfte der hypothetischen Low-Handlungen hÃ¤tte
  Verlust gespart, aber ein groÃŸer Anteil hÃ¤tte auch Gewinn verpasst. Das
  spricht fÃ¼r Reifung mit Gegenspannung statt fÃ¼r harte Vermeidung.
- [ ] Lauf 20 prÃ¼fen, bevor an der Kopplung gedreht wird.
  Ziel: Erst beobachten, ob `maturity_trust` und `action_pressure` stabil
  bleiben, ob Non-Zone/Low weiter sinkt oder ob die Ambivalenz zu viel
  Handlungsdruck erzeugt. Keine sofortige Code-Drosselung nach nur einem
  echten Aktivierungslauf.
- [x] `debug_lauf_20` geprÃ¼ft.
  Ergebnis: PnL ca. +12.64 bei 47 Trades. Zone trÃ¤gt weiter mit ca. +19.84
  PnL, Non-Zone bleibt mit 10 Trades und ca. -7.20 PnL negativ.
- [x] Beobachtungsreife als stabil bestÃ¤tigt.
  Ergebnis: `low_observations = 903`, `resolved = 891`,
  `saved_loss = 507`, `missed_gain = 378`, `maturity_trust` steigt auf
  ca. 0.571 und `action_pressure` sinkt auf ca. 0.424. Die Reifespur ist
  also aktiv und stabil.
- [x] Reife-Kopplung leicht nachgeschaerft.
  Ergebnis: Neu ist `observation_maturity_balance =
  maturity_trust - action_pressure`. Positive Balance reduziert `act_push`
  leicht, stÃ¤rkt `observe_pull` und gibt `replan_pull` eine minimale
  Zusatzspannung. Keine harte Low-Sperre, sondern weichere Ãœbersetzung von
  Beobachtungsreife in ZurÃ¼ckhaltung/Reorganisation.
- [ ] Lauf 21 prÃ¼fen:
  Tradezahl, Zone-Freiheit, Non-Zone/Low-PnL, `maturity_trust`,
  `action_pressure`, `observation_maturity_balance` und ob die neue Kopplung
  unreife Handlung reduziert, ohne gute Chancen zu ersticken.
- [x] `debug_lauf_21` geprÃ¼ft.
  Ergebnis: PnL fÃ¤llt auf ca. +10.30 bei 46 Trades. Zone bleibt positiv
  mit ca. +18.55 PnL, Non-Zone wird mit 16 Trades und ca. -8.25 PnL wieder
  teurer.
- [x] Reife-Kopplung als zu global erkannt.
  Ergebnis: Die Beobachtungslernspur bleibt aktiv
  (`low_observations = 1026`, `saved_loss = 566`, `missed_gain = 440`),
  aber die globale Reife-Balance kann gute Zone-Handlungen mitdÃ¤mpfen und
  lÃ¶st das Strukturkippen wÃ¤hrend offener Positionen nicht sauber.
- [x] Reife-Balance an StrukturtragfÃ¤higkeit gekoppelt.
  Ergebnis: Neu sind `observation_maturity_scope` und
  `observation_scoped_balance`. Die Reife-Balance wirkt jetzt stÃ¤rker bei
  niedriger StrukturtragfÃ¤higkeit und weniger pauschal auf tragende Zone.
  Ziel: Low-Spannung regulieren, ohne Zone-Mut global zu entziehen.
- [ ] Lauf 22 prÃ¼fen:
  PnL, Zone-Freiheit, Non-Zone-Outcomes, Tradezahl,
  `observation_maturity_scope`, `observation_scoped_balance` und ob die
  Reife-Regulation jetzt gezielter wirkt.
- [x] `debug_lauf_22` geprÃ¼ft.
  Ergebnis: PnL fÃ¤llt stark auf ca. +1.67 bei 40 Trades. Zone-PnL sinkt auf
  ca. +11.24, Non-Zone bleibt mit 15 Trades und ca. -9.56 PnL deutlich
  negativ. Weniger Trades bedeuten hier nicht bessere QualitÃ¤t.
- [x] Fehler in `observation_maturity_scope` diagnostiziert.
  Ergebnis: Der Scope stand auch bei hoher realer `structure_quality` oft fast
  auf 1.0. Dadurch wirkte die Reife-Balance weiterhin zu breit und konnte
  tragende Zone mitdÃ¤mpfen.
- [x] Scope an reale StrukturqualitÃ¤t gebunden.
  Ergebnis: `observation_maturity_scope` wird jetzt aus
  `structure_perception_state.structure_quality` berechnet. Nur bei niedriger
  realer StrukturqualitÃ¤t wirkt die Reife-Balance stark. Ziel: Low-Spannung
  regulieren, ohne tragende Zone pauschal zu bremsen.
- [ ] Lauf 23 prÃ¼fen:
  PnL-Erholung, Zone-TP/SL-Verhaeltnis, Non-Zone-Verlust, Tradezahl,
  `observation_maturity_scope` und `observation_scoped_balance`.
- [x] `debug_lauf_23` geprÃ¼ft.
  Ergebnis: PnL erholt sich stark auf ca. +16.13 bei 41 Trades. Zone trÃ¤gt
  ca. +20.09 PnL, Non-Zone fÃ¤llt auf nur 7 Trades und ca. -3.96 PnL. Der
  reale Struktur-Scope wirkt damit deutlich besser.
- [x] Equity-Peak und RÃ¼cklauf ausgewertet.
  Ergebnis: Lauf 23 erreichte kurzzeitig ca. +18.28 PnL und schloss bei
  ca. +16.13. Der RÃ¼cklauf vom Peak betrÃ¤gt ca. -2.15. Das ist kein
  Kollaps, aber ein Hinweis auf fehlende Halte-/Exit-Reife nach gutem Lauf.
- [x] Scoped Reife als verbessert bestÃ¤tigt.
  Ergebnis: `observation_maturity_scope` liegt im Schnitt nur noch bei ca.
  0.121 und fÃ¤llt bei tragender Struktur hÃ¤ufig auf 0. Reife wirkt damit
  deutlich lokaler auf Low-/Non-Zone-Spannung.
- [ ] NÃ¤chster Fix: Halte-/Exit-Reife vorbereiten.
  Ziel: Nicht neue Entry-DÃ¤mpfung, sondern bessere Wahrnehmung offener
  Positionen. Wenn Gewinn aufgebaut ist oder Struktur wÃ¤hrend der Position
  kippt, soll DIO RÃ¼ckgabe, TragfÃ¤higkeitsverlust und Reorganisationsbedarf
  erkennen kÃ¶nnen, ohne gute Trendfortsetzung hart abzuwuergen.
- [x] Schalter fÃ¼r Halte-/Exit-Reife eingebaut.
  Ergebnis: `config.py` enthÃ¤lt jetzt `MCM_MATURED_EXIT_MODE` mit den Modi
  `fixed`, `observe` und `active`. Standard ist `fixed`, also weiterhin nur
  klassisches TP/SL-Auslaufen. `observe` protokolliert gereifte Exit-Reife nur,
  `active` darf im Backtest eine Position Ã¼ber `matured_exit` schliessen.
- [x] Gereifte Exit-Hypothese technisch vorbereitet.
  Ergebnis: Offene Positionen kÃ¶nnen anhand von MFE, RÃ¼ckgabe vom Peak,
  StrukturqualitÃ¤t, Druck/KapazitÃ¤t und Recovery-Lage eine Exit-Reife bilden.
  Fester TP/SL hat Vorrang. Im Live-Modus wird `matured_exit` aus Sicherheit
  noch nicht automatisch ausgefÃ¼hrt.
- [x] `TradeStats` fÃ¼r `matured_exit` erweitert.
  Ergebnis: Gereifte Exits kÃ¶nnen mit echtem Exit-Preis abgerechnet und als
  eigenes Outcome sichtbar gemacht werden.
- [ ] NÃ¤chster Test:
  Erst mit `MCM_MATURED_EXIT_MODE = "observe"` laufen lassen, um zu prÃ¼fen,
  wann DIO Exit-Reife erkannt hÃ¤tte. Danach erst optional `active` im
  Backtest testen.
- [x] `debug_lauf_24` mit `MCM_MATURED_EXIT_MODE = "observe"` geprÃ¼ft.
  Ergebnis: PnL ca. +7.05 bei 39 Trades. Es wurden keine aktiven
  `matured_exits` ausgefÃ¼hrt, wie gewuenscht. Es wurden aber auch keine
  `matured_exit_observe`-Ereignisse gefunden.
- [x] Exit-Reife-Beobachtung diagnostisch nachgeschaerft.
  Ergebnis: Die Schwellen waren zu streng und die Positionslage war im
  Nachweisraum noch zu schwach sichtbar. `MCM_MATURED_EXIT_MIN_MFE_R` wurde
  auf 0.70 und `MCM_MATURED_EXIT_GIVEBACK_R` auf 0.25 gesetzt. ZusÃ¤tzlich
  schreibt der Position-Kontext jetzt MFE/MAE/R-Werte und bei erkannter
  Exit-Reife wird `matured_exit_debug.csv` geschrieben.
- [x] Lauf 25 im Modus `observe` geprÃ¼ft.
  Gibt es `matured_exit_debug.csv`? Wie viele Exit-Reife-Signale entstehen?
  Kamen sie vor spÃ¤teren SLs oder hÃ¤tten sie gute TPs zu frÃ¼h beschnitten?
  Ergebnis: Lauf 25 schlieÃŸt bei ca. +12.76 PnL mit 43 Trades. Zone trÃ¤gt
  stark mit ca. +21.39 PnL, Non-Zone bleibt mit 0 TP / 12 SL und ca. -8.62 PnL
  der klare Verlustkanal. `matured_exit_debug.csv` enthÃ¤lt 7
  Exit-Reife-Beobachtungen. Da `observe` aktiv ist, wurden keine echten
  `matured_exits` ausgefÃ¼hrt.
- [x] Exit-Reife-Debug fÃ¼r Lauf 26 erweitert.
  Ergebnis: `matured_exit_debug.csv` schreibt ab dem nÃ¤chsten Lauf zusÃ¤tzlich
  Timestamp, Entry, TP, SL und Risiko. Damit kann die gereifte Exit-Wahrnehmung
  besser gegen den spÃ¤teren Tradeausgang geprÃ¼ft werden.
- [ ] NÃ¤chster mÃ¶glicher Ausbau:
  Lauf 26 im Modus `observe` laufen lassen und die 7+ Exit-Reife-Signale gegen
  echte Outcomes spiegeln: schuetzen sie vor spÃ¤teren SLs oder wÃ¼rden sie gute
  TP-Bewegungen zu frÃ¼h beenden? Erst danach `active` Ã¼berhaupt als
  Backtest-Experiment erwaegen.
- [x] Lauf 26 im Modus `observe` geprÃ¼ft.
  Ergebnis: PnL ca. +2.99 bei 39 Trades. Zone bleibt positiv mit ca. +10.17 PnL,
  Non-Zone bleibt 0 TP / 13 SL und ca. -7.18 PnL. `matured_exit_debug.csv`
  enthÃ¤lt 11 Exit-Reife-Beobachtungen. 6 Signale lagen vor spÃ¤teren SLs
  und hÃ¤tten tendenziell geschuetzt, 5 Signale lagen vor spÃ¤teren TPs und
  hÃ¤tten Gewinn zu frÃ¼h begrenzt.
- [ ] NÃ¤chster Fix:
  Exit-Reife nicht aktivieren, sondern eine BestÃ¤tigungsschicht vorbereiten.
  Ein einzelnes Signal ist Wahrnehmung, keine Handlung. Handlung darf erst
  nÃ¤her rÃ¼cken, wenn Reife-Signale Ã¼ber mehrere Bars stabil bleiben oder
  wenn RÃ¼ckgabe, Strukturverlust und Druck/KapazitÃ¤ts-Konflikt gemeinsam
  kippen.
- [x] `debug_lauf_27` mit versehentlich aktivem `matured_exit` geprÃ¼ft.
  Ergebnis: PnL ca. +1.93 bei 33 Trades. Es gab 15 aktive `matured_exit`-
  Schluesse. Nach `outcome_records` waren diese netto ca. -0.67 PnL
  nach GebÃ¼hren. Das bestÃ¤tigt: Active ist noch zu frÃ¼h und beschneidet
  Gewinner bzw. normale Gewinnatmung zu oft.
- [x] `MCM_MATURED_EXIT_MODE` wieder auf `observe` gesetzt.
  Ergebnis: Der nÃ¤chste Lauf beobachtet Exit-Reife wieder nur und schlieÃŸt
  nicht aktiv.
- [x] `matured_exit_pnl` netto korrigiert.
  Ergebnis: `trade_stats.py` zaehlt `matured_exit_pnl` ab jetzt nach GebÃ¼hren,
  passend zu `outcome_records`. Lauf 27 zeigte hier den Unterschied zwischen
  Brutto-Wahrnehmung und realem Netto-Ergebnis.
- [ ] NÃ¤chster Fix:
  Exit-Reife-BestÃ¤tigungsschicht einbauen. Idee: einzelne Reife-Wahrnehmung
  bleibt Observe; erst wiederholte oder gekoppelte BestÃ¤tigung aus RÃ¼ckgabe,
  Strukturverlust, negativem `current_r` und Druck/KapazitÃ¤ts-Konflikt darf
  einen Backtest-Exit-Kandidaten erzeugen.
- [x] Positionslast und reife Nicht-Intervention dokumentiert.
  Ergebnis: `docs/01_plan/UMSETZUNGSPLAN.md` und `README.md` halten jetzt fest,
  dass laufende Exit-Bewertung kognitive und regulatorische Last erzeugt.
  Hohe Belastung ist nicht automatisch ein Exit-Grund, sondern kann bedeuten,
  dass die aktuelle innere Lage keine tragfÃ¤hige neue Entscheidung erlaubt.
- [x] NÃ¤chster Fix:
  `position_cognitive_load`, `exit_decision_pressure`, `holding_stability`,
  `plan_trust`, `intervention_fatigue`, `inner_noise` und
  `intervention_fitness` als DiagnosegrÃ¶ÃŸen vorbereiten. Ziel:
  Exit-Reife von Exit-Nervositaet unterscheiden.
- [x] Positionslast-/Interventionsdiagnose technisch vorbereitet.
  Ergebnis: `bot.py` baut pro offener Position `position_intervention_state`.
  Enthalten sind kognitive Positionslast, Exit-Druck, Planvertrauen,
  HaltestabilitÃ¤t, Interventionsmuedigkeit, inneres Rauschen,
  Exit-Evidenz, Interventionseignung und `intervention_unfit_state`.
  Die Werte laufen in Position-Events, Exit-Kontexte, `matured_exit_debug.csv`
  und `outcome_records.jsonl`.
- [x] Neues Protokoll fÃ¼r Positionslast eingebaut.
  Ergebnis: `mcm_position_intervention_protocol.csv` schreibt kompakte
  Positionslast-/Exit-Nervositaetswerte. Gesteuert Ã¼ber
  `MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG` und
  `MCM_POSITION_INTERVENTION_PROTOCOL_EVERY_N`.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Lauf 28 im Modus `observe` laufen lassen. Danach prÃ¼fen:
  - steigen `exit_decision_pressure` und `intervention_unfit_state` vor
    schlechten aktiven Exit-Situationen?
  - bleibt `plan_trust` bei spÃ¤teren TP-Trades hÃ¶her?
  - unterscheidet `intervention_fitness` echte Schutzlagen besser als die alte
    einfache `matured_exit`-Wahrnehmung?
- [x] Lauf 28 im Modus `observe` geprÃ¼ft.
  Ergebnis: PnL ca. +8.90 bei 49 Trades. Zone trÃ¤gt ca. +15.81 PnL,
  Non-Zone bleibt 0 TP / 12 SL und ca. -6.91 PnL. Es gab 8
  `matured_exit`-Beobachtungen, aber keine aktiven Exits.
- [x] Positionslast-Diagnose gegen Outcomes geprÃ¼ft.
  Ergebnis: `plan_holding_trust` trennt sehr stark:
  23 Trades, 20 TP / 3 SL, ca. +23.43 PnL. `exit_nervousness_observe`
  markiert dagegen 24 Trades, 0 TP / 24 SL, ca. -13.51 PnL.
  Damit ist die neue Schicht deutlich aussagekraeftiger als die alte
  Einzelwahrnehmung `matured_exit`.
- [x] NÃ¤chster Fix:
  Exit-BestÃ¤tigungsschicht aus Positionslast bauen, aber weiter nur
  diagnostisch oder sehr vorsichtig als Kandidat. Bedingungen mÃ¼ssen
  gekoppelt sein: niedriger `plan_trust`, hohe `exit_decision_pressure`,
  sinkende `holding_stability`, relevante `exit_evidence` und genug
  `intervention_fitness`. Kein einzelnes Signal darf aktiv schliessen.
- [x] `exit_candidate_observe` als reine Kandidaten-Schicht eingebaut.
  Ergebnis: `bot.py` baut `exit_candidate_observe_state` aus gekoppelter
  Positionslast-BestÃ¤tigung. Es gibt kein aktives SchlieÃŸen. Kandidaten werden
  als Runtime-Event `exit_candidate_observe`, im Matured-Exit-Kontext und in
  `outcome_records.jsonl` sichtbar.
- [x] Neues Kandidaten-Protokoll eingebaut.
  Ergebnis: `mcm_exit_candidate_observe.csv` schreibt gekoppelte Kandidaten
  und unfit-Drucklagen. Config-Schwellen:
  `MCM_EXIT_CANDIDATE_MIN_PRESSURE`,
  `MCM_EXIT_CANDIDATE_MAX_PLAN_TRUST`,
  `MCM_EXIT_CANDIDATE_MAX_HOLDING_STABILITY`,
  `MCM_EXIT_CANDIDATE_MIN_FITNESS`,
  `MCM_EXIT_CANDIDATE_MIN_EVIDENCE`.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Lauf 29 im Modus `observe` laufen lassen. Danach prÃ¼fen:
  - wie viele `exit_candidate_observe` entstehen
  - ob Kandidaten vor spÃ¤teren SLs liegen
  - ob Kandidaten spÃ¤tere TPs verschonen
  - ob `exit_pressure_unfit_observe` tatsÃ¤chlich Belastung ohne tragfÃ¤hige
    Intervention markiert
- [x] Lauf 29 im Modus `observe` geprÃ¼ft.
  Ergebnis: PnL ca. +5.81 bei 36 Trades. Zone trÃ¤gt ca. +10.89 PnL,
  Non-Zone bleibt 0 TP / 9 SL und ca. -5.08 PnL. Der Lauf ist schwaecher
  als Lauf 28, aber weiterhin positiv.
- [x] `exit_candidate_observe` gegen Outcomes geprÃ¼ft.
  Ergebnis: In den Outcome-Kontexten lagen 13 `exit_candidate_observe`-
  Markierungen auf 13 spÃ¤teren SLs und 0 TPs. Die 3 konkreten Kandidaten-
  Events aus `mcm_exit_candidate_observe.csv` lagen ebenfalls alle vor
  spÃ¤teren SLs. Keine TP-Zerstoerung durch Kandidatenlogik sichtbar.
- [x] Positionslast-Diagnose erneut bestÃ¤tigt.
  Ergebnis: `plan_holding_trust` war in Lauf 29 sehr sauber:
  14 Trades, 14 TP / 0 SL, ca. +18.07 PnL. `exit_nervousness_observe`
  markierte 20 Trades, 0 TP / 20 SL, ca. -11.02 PnL.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Noch einen Observe-Lauf mit gleicher Datenbasis laufen lassen. Danach
  prÃ¼fen, ob `exit_candidate_observe` erneut nur SL-Lagen markiert.
  Wenn ja, hypothetisches Kandidaten-PnL-Protokoll bauen:
  Wie wÃ¤re der Lauf ausgefallen, wenn nur Kandidaten geschlossen hÃ¤tten?
- [x] Lauf 30 im Modus `observe` geprÃ¼ft.
  Ergebnis: PnL ca. +11.60 bei 33 Trades. Zone trÃ¤gt ca. +14.30 PnL,
  Non-Zone bleibt 0 TP / 5 SL und ca. -2.71 PnL. Der Lauf erholt sich
  deutlich gegen Lauf 29.
- [x] Exit-Kandidaten erneut gegen Outcomes geprÃ¼ft.
  Ergebnis: `exit_candidate_observe` lag in den Outcome-Kontexten auf
  7 Trades, 0 TP / 7 SL, ca. -3.88 PnL. Das konkrete Kandidatenereignis
  aus `mcm_exit_candidate_observe.csv` lag ebenfalls vor einem spÃ¤teren SL.
  Keine TP-Zerstoerung durch die Kandidatenschicht sichtbar.
- [x] Positionslast-Diagnose in Lauf 30 erneut bestÃ¤tigt.
  Ergebnis: `plan_holding_trust` war sehr sauber:
  16 Trades, 16 TP / 0 SL, ca. +20.75 PnL. `exit_nervousness_observe`
  markierte 17 Trades, 0 TP / 17 SL, ca. -9.16 PnL.
- [x] Hypothetisches Kandidaten-PnL-Protokoll gebaut.
  Ergebnis: Der erste echte `exit_candidate_observe` einer offenen Position
  wird jetzt als `exit_candidate_replay_state` gemerkt, aber erst nachdem
  klar ist, dass TP/SL auf derselben Kerze nicht bereits ausgelÃ¶st haben.
  Beim echten Exit berechnet `trade_stats.py`, wie der Trade ausgegangen wÃ¤re,
  wenn DIO am Kandidatenpreis geschlossen hÃ¤tte.
- [x] Neues Replay-Debug eingebaut.
  Ergebnis: `mcm_exit_candidate_replay.csv` schreibt pro betroffener Position:
  Kandidatenzeit, Kandidatenpreis, echten Exit, echten PnL, hypothetischen PnL,
  PnL-Differenz, Score, Exit-Druck, Planvertrauen und Interventionseignung.
  `trade_stats.json` fÃ¼hrt zusÃ¤tzliche Summen:
  `exit_candidate_replay_count`, `exit_candidate_replay_actual_pnl`,
  `exit_candidate_replay_hypothetical_pnl`, `exit_candidate_replay_delta_pnl`,
  `saved_loss_count`, `saved_giveback_count`, `harmed_count` und `tp_cut_count`.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Einen neuen Observe-Lauf starten und `mcm_exit_candidate_replay.csv`
  auswerten. Wichtig ist nicht nur, ob Kandidaten vor SLs liegen, sondern
  ob der hypothetische Exit netto wirklich besser gewesen wÃ¤re.
- [ ] Danach:
  Erst wenn mehrere LÃ¤ufe zeigen, dass Kandidaten Verlust oder Giveback
  sauber reduzieren und keine tragenden TP-Lagen zerstoeren, darf Ã¼ber einen
  schaltbaren Active-Modus nachgedacht werden.
- [x] Live-Mechanik statisch und mit Fake-Exchange geprÃ¼ft.
  Ergebnis: Order setzen, aktive Order erkennen, Snapshot bilden, Cancel senden
  und Cancel-Cause konsumieren funktionieren im isolierten Exchange-Test.
- [x] Live-Symbolpfad korrigiert.
  Ergebnis: `ph_ohlcv.resolve_exchange_symbol()` normalisiert Swap-Symbole.
  Live-OHLCV, Ticker, Order-Setzen und Monitor nutzen konsistent
  `SOL/USDT:USDT`; der Workspace bleibt als Datenablage erhalten.
- [x] Live-Exit gegen lokale Fehlfinalisierung abgesichert.
  Ergebnis: Im Live-Modus wird eine Position nicht mehr allein wegen lokalem
  Candle-TP/SL intern finalisiert. Der Bot wartet, bis
  `get_active_order_snapshot()` keinen offenen Exchange-Kontext mehr meldet.
  Solange die Exchange noch Order/Position sieht, wird `LIVE_EXIT_WAIT`
  protokolliert.
- [ ] NÃ¤chster Live-PrÃ¼fpunkt:
  Mit echten API-Daten im kleinsten Setup testen:
  `Config.MODE = "LIVE"`, `AKTIV_ORDER = True`, sehr kleine `ORDER_SIZE`,
  dann `order_debug.csv`, `live_backtest_debug.csv`, Workspace-Schreibung und
  Exchange-Status parallel beobachten.
- [x] Lauf 31 ausgewertet.
  Ergebnis: bisher stÃ¤rkster Lauf der aktuellen Sequenz mit ca. +17.46 PnL,
  47 Trades, 24 TP / 23 SL und Profit Factor ca. 2.30. Zone trÃ¤gt ca.
  +23.12 PnL, Non-Zone bleibt 0 TP / 10 SL und ca. -5.67 PnL.
- [x] Kandidaten-Replay aus Lauf 31 bewertet.
  Ergebnis: 6 Replay-FÃ¤lle. 5 hÃ¤tten Verlust reduziert, aber 1 Fall hÃ¤tte
  einen spÃ¤teren TP zu frÃ¼h abgeschnitten. Netto wÃ¤re das Replay ca.
  -0.87 PnL schlechter gewesen. Aktiver Kandidaten-Exit bleibt daher unreif.
- [x] Replay-CSV-Sampling-Fehler korrigiert.
  Ergebnis: `mcm_exit_candidate_replay.csv` wurde in Lauf 31 nicht geschrieben,
  weil `dbr_debug` wegen `DEBUG_WRITE_EVERY_N = 8` sampelt und nur 6 Replay-
  FÃ¤lle entstanden. `trade_stats.py` schreibt diese seltene Replay-Datei jetzt
  direkt und samplingfrei.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Neuen Observe-Lauf starten und prÃ¼fen, ob die samplingfreie
  `mcm_exit_candidate_replay.csv` entsteht. Fachlich besonders prÃ¼fen:
  ob TP-Cuts durch zusÃ¤tzliche Bedingungen vermeidbar sind.
- [x] Lauf 32 ausgewertet.
  Ergebnis: ca. +9.81 PnL bei 48 Trades, 20 TP / 28 SL und Profit Factor
  ca. 1.63. Der Lauf ist schwaecher als Lauf 31, bleibt aber positiv.
- [x] RÃ¼ckgang gegen Lauf 31 eingeordnet.
  Ergebnis: Hauptursache ist die Strukturverteilung. High-Trades sinken
  von 25 auf 18, Low-Trades steigen von 10 auf 17. Low/Non-Zone bleibt
  0 TP / 17 SL und kostet ca. -9.41 PnL.
- [x] Kandidaten-Replay aus Lauf 32 bewertet.
  Ergebnis: 10 Replay-FÃ¤lle. 9 hÃ¤tten Verlust reduziert, 1 Fall hÃ¤tte
  einen spÃ¤teren TP zu frÃ¼h abgeschnitten. Netto wÃ¤re Replay ca.
  -0.57 PnL schlechter gewesen. Aktiver Exit bleibt unreif.
- [x] Replay-CSV-Verschmutzung korrigiert.
  Ergebnis: Die strukturierte `mcm_exit_candidate_replay.csv` wurde noch
  durch eine gesampelte Textdebug-Zeile verschmutzt. Textdebug schreibt jetzt
  in `mcm_exit_candidate_replay_debug.log`.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Lauf 33 starten. PrÃ¼fen:
  - ob `mcm_exit_candidate_replay.csv` sauber strukturiert bleibt
  - ob TP-Cuts wieder auftreten
  - welche Zusatzbedingung TP-Cuts verhindert, ohne SL-Schutz komplett zu
    verlieren
- [x] Lauf 33 ausgewertet.
  Ergebnis: ca. +7.78 PnL bei 25 Trades, 12 TP / 13 SL und Profit Factor
  ca. 2.01. Der Lauf ist kleiner, bleibt aber positiv.
- [x] Replay-CSV nach Korrektur geprÃ¼ft.
  Ergebnis: `mcm_exit_candidate_replay.csv` ist sauber strukturiert und
  enthÃ¤lt 5 Replay-FÃ¤lle.
- [x] TP-Cut erneut bestÃ¤tigt und Ursache eingegrenzt.
  Ergebnis: 4 Replay-FÃ¤lle hÃ¤tten Verlust reduziert, 1 Fall hÃ¤tte einen
  spÃ¤teren TP abgeschnitten. Der schÃ¤dliche Fall war nur leicht negativ
  (`current_r` ca. -0.17R), kam aber nach starkem Gewinnlauf (`mfe_r`
  ca. 2.62R). Das ist eher RÃ¼ckatmung als reife Exit-Intervention.
- [x] `exit_pullback_observe` eingebaut.
  Ergebnis: `MCM_EXIT_CANDIDATE_MAX_CURRENT_R = -0.45` verlangt echte adverse
  Tiefe fÃ¼r einen Exit-Kandidaten. Leichte RÃ¼ckatmung bei hohem vorherigem
  MFE wird jetzt als `exit_pullback_observe` beobachtet, nicht als echter
  Exit-Kandidat.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Lauf 34 starten. PrÃ¼fen:
  - ob der bekannte TP-Cut verschwindet
  - wie viele SL-SchutzfÃ¤lle durch `adverse_depth_ok` erhalten bleiben
  - ob `exit_pullback_observe` spÃ¤tere TPs sauberer schuetzt
- [x] Lauf 34 ausgewertet.
  Ergebnis: sehr starker Lauf mit ca. +19.67 PnL, 39 Trades,
  22 TP / 17 SL, Profit Factor ca. 3.03 und Max Drawdown ca. 1.73.
- [x] Plan-Halten als tragende Reife erneut bestÃ¤tigt.
  Ergebnis: `plan_holding_trust` trennt perfekt:
  22 Trades, 22 TP / 0 SL, ca. +29.34 PnL.
- [x] Low-/Non-Zone-Verlust deutlich reduziert.
  Ergebnis: Low/Non-Zone war mit 7 Trades nur noch ca. -0.53 PnL
  statt wie zuvor stark destruktiv. Das erklÃ¤rt einen groÃŸen Teil des
  starken Laufs.
- [x] Exit-Reife bleibt unreif.
  Ergebnis: Replay hatte 3 FÃ¤lle. 2 hÃ¤tten Verlust reduziert, 1 hÃ¤tte
  einen spÃ¤teren TP abgeschnitten. Netto wÃ¤re Replay ca. -1.39 PnL
  schlechter gewesen.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Weiterhin Observe-Lauf starten. Nicht vorschnell Schwelle haerter setzen,
  sondern TP-Cut-Muster sammeln:
  - current_r beim Kandidaten
  - vorheriges MFE
  - Planvertrauen
  - HaltestabilitÃ¤t
  - ob der Kandidat nach Gegenbewegung oder echter Strukturzerstoerung kam
- [x] Lauf 35 ausgewertet.
  Ergebnis: ca. +13.62 PnL bei 45 Trades, 21 TP / 24 SL,
  Profit Factor ca. 1.91. `plan_holding_trust` bleibt stark positiv
  mit ca. +28.13 PnL. Replay: 6 FÃ¤lle, alle hÃ¤tten Verlust reduziert,
  kein harmed/TP-Cut.
- [x] Lauf 36 ausgewertet.
  Ergebnis: ca. +11.93 PnL bei 36 Trades, 18 TP / 18 SL,
  Profit Factor ca. 2.05. `plan_holding_trust` trennt perfekt
  mit 18 TP / 0 SL und ca. +23.27 PnL. Replay: 3 FÃ¤lle,
  alle hÃ¤tten Verlust reduziert, kein harmed/TP-Cut.
- [x] TP-Cut-Lage nach Lauf 35/36 neu bewertet.
  Ergebnis: Der adverse-depth-Filter scheint den bekannten TP-Cut deutlich
  besser zu entschÃ¤rfen. Aktiver Exit bleibt trotzdem observe-only,
  weil die Stichprobe klein ist.
- [ ] Offener Schwerpunkt nach Lauf 35/36:
  Low/Non-Zone und negative Formentwicklung bleiben die schwache Stelle.
  Lauf 36: Low/Non-Zone 10 Trades, 0 TP / 10 SL, ca. -6.92 PnL.
  Ziel: Nicht hart blockieren, sondern Ã¼ber Zielerwartung,
  TP-Erreichbarkeit und Erwartungsbruch lernen, wann eine Handlung
  nicht tragfÃ¤hig genug ist.
- [x] Zielerwartung einer Handlung fachlich ausgearbeitet.
  Ergebnis: Entry/TP/SL werden nicht mehr nur technisch verstanden.
  Ein Entry trÃ¤gt eine Erwartung, der TP ist ein Zielraum und der SL eine
  TragfÃ¤higkeitsgrenze. Damit kann DIO spÃ¤ter unterscheiden, ob eine
  Position nur belastet oder ob die ursprÃ¼ngliche Erwartung wirklich
  gebrochen ist.
- [x] Zielerwartung in Dokumentation Ã¼bernommen.
  Ergebnis: `README.md`, `docs/01_plan/UMSETZUNGSPLAN.md` und
  `docs/02_status/AKTUELLER_STAND.md` enthalten die neue Semantik.
- [ ] NÃ¤chster Umsetzungspunkt:
  Erwartungsdiagnose observe-only einbauen:
  - `target_expectation_context`
  - `tp_reachability`
  - `target_path_integrity`
  - `expectation_deviation`
  - `expectation_break_pressure`
  - `expectation_hold_support`
  Ziel: TP-Cuts besser von echten SL-Schutzmomenten unterscheiden,
  ohne aktive Exit-Entscheidung zu verÃ¤ndern.
- [x] Erwartungsdiagnose observe-only eingebaut.
  Ergebnis:
  - `config.py` enthÃ¤lt `MCM_TARGET_EXPECTATION_PROTOCOL_DEBUG`
    und `MCM_TARGET_EXPECTATION_PROTOCOL_EVERY_N`
  - `bot.py` erzeugt `target_expectation_state`
  - neues Debug-Protokoll: `mcm_target_expectation_protocol.csv`
  - Exit-Kandidaten und Replay erhalten die Erwartungsfelder
  - `trade_stats.py` schreibt die Felder in Outcome-Kontext und Replay-CSV
  Wichtig: Die Felder beeinflussen noch keine aktive Exit-Entscheidung.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Lauf 37 starten und auswerten:
  - zeigen spÃ¤tere SL-Kandidaten hohe `expectation_break_pressure`?
  - behalten spÃ¤tere TP/Plan-Holds hohe `tp_reachability`?
  - trennt `expectation_hold_support` TP-Cuts besser von echtem Schutz?
  - bleibt Low/Non-Zone Ã¼ber Zielerwartung als nicht tragfÃ¤hig sichtbar?
- [x] Lauf 37 ausgewertet.
  Ergebnis: ca. +5.97 PnL bei 46 Trades, 18 TP / 28 SL,
  Profit Factor ca. 1.35. Der Lauf ist schwaecher, bleibt aber positiv.
- [x] Erwartungsdiagnose aus Lauf 37 bewertet.
  Ergebnis:
  - `target_expectation_holds`: 19 Trades, 18 TP / 1 SL,
    ca. +22.69 PnL
  - `expectation_break_observe`: 23 Trades, 0 TP / 23 SL,
    ca. -14.43 PnL
  - TP-Outcomes: `tp_reachability` ca. 0.77,
    `expectation_break_pressure` ca. 0.19,
    `expectation_hold_support` ca. 0.77
  - SL-Outcomes: `tp_reachability` ca. 0.40,
    `expectation_break_pressure` ca. 0.64,
    `expectation_hold_support` ca. 0.43
- [x] Exit-Kandidaten-Replay Lauf 37 bewertet.
  Ergebnis: 6 Replay-FÃ¤lle, alle spÃ¤ter SL,
  alle `expectation_break_observe`, alle hÃ¤tten Verlust reduziert,
  kein harmed/TP-Cut. Das bestÃ¤tigt die neue Zielerwartungssemantik.
- [ ] NÃ¤chster Umsetzungspunkt:
  Zielerwartung vor Handlung/Entry nutzbar machen,
  aber ohne harte Blocks:
  Low/Non-Zone und negative Formen sollen eher in Beobachtung,
  Reframing oder spÃ¤tere Handlung gehen,
  wenn `tp_reachability`/Zielpfad nicht tragfÃ¤hig genug wirkt.
  Ziel ist reife HandlungszurÃ¼ckhaltung,
  nicht mechanisches Verbieten.
- [x] Lauf 38 ausgewertet.
  Ergebnis: ca. +14.97 PnL bei 40 Trades, 20 TP / 20 SL,
  Profit Factor ca. 2.19. Das bestÃ¤tigt die Vermutung,
  dass Lauf 37 eher eine Reorganisationsphase nach neuer Wahrnehmungsachse
  war als ein struktureller RÃ¼ckschritt.
- [x] Erwartungsdiagnose Lauf 38 bewertet.
  Ergebnis:
  - `target_expectation_holds`: 21 Trades, 20 TP / 1 SL,
    ca. +27.04 PnL
  - `expectation_break_observe`: 14 Trades, 0 TP / 14 SL,
    ca. -9.03 PnL
  - TP/SL-Mittelwerte bleiben fast identisch zu Lauf 37:
    TP ca. `tp_reachability` 0.77 / `expectation_break_pressure` 0.19,
    SL ca. `tp_reachability` 0.40 / `expectation_break_pressure` 0.62
- [x] Reorganisations-/TP-Cut-Fall Lauf 38 festgehalten.
  Ergebnis: Replay hatte 4 FÃ¤lle. 3 hÃ¤tten Verlust reduziert,
  1 Fall hÃ¤tte einen spÃ¤teren TP stark abgeschnitten.
  Dieser Fall war als `expectation_break_observe` markiert,
  wurde spÃ¤ter aber wieder zu `target_expectation_holds` und lief in TP.
- [ ] NÃ¤chster Fixpunkt:
  Erwartungsbruch nicht sofort als endgueltigen Bruch lesen.
  ErgÃ¤nzen einer weichen Reorganisations-/Recovery-Diagnose:
  - `target_recovery_potential`
  - `prior_target_hold_support`
  - `expectation_break_persistence`
  - `deep_pullback_recovery_watch`
  Ziel: echte Erwartungsbrueche von tiefer RÃ¼ckatmung unterscheiden,
  ohne harte Exit-Blocks.
- [x] Recovery-/Reorganisationsdiagnose observe-only eingebaut.
  Ergebnis:
  - `bot.py` fÃ¼hrt eine kurzfristige Zielpfad-Erinnerung pro offener
    Position:
    `target_hold_support_peak`, `tp_reachability_peak`,
    `target_path_integrity_peak`, `expectation_break_count`
  - `target_expectation_state` enthÃ¤lt jetzt:
    `target_recovery_potential`, `prior_target_hold_support`,
    `prior_tp_reachability`, `prior_target_path_integrity`,
    `expectation_break_persistence`, `expectation_break_count`,
    `deep_pullback_recovery_watch`
  - Replay/Outcome-Kontexte schreiben diese Felder mit.
  Wichtig: Noch keine aktive Exit-Aenderung.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Lauf 39 starten und auswerten:
  - wird der TP-Cut-Typ aus Lauf 38 als `deep_pullback_recovery_watch`
    sichtbar?
  - bleiben echte SL-Kandidaten bei hoher `expectation_break_persistence`
    und niedriger Recovery?
  - bleibt `target_expectation_holds` weiter TP-lastig?
  - bleibt Low/Non-Zone als schwache TragfÃ¤higkeit sichtbar?
- [x] Lauf 39 ausgewertet.
  Ergebnis: ca. +15.30 PnL bei 47 Trades, 23 TP / 24 SL,
  Profit Factor ca. 2.10. Der Lauf bleibt stark positiv.
- [x] Zielerwartungsachse Lauf 39 bestÃ¤tigt.
  Ergebnis:
  - `target_expectation_holds`: 24 Trades, 23 TP / 1 SL,
    ca. +28.66 PnL
  - `expectation_break_observe`: 9 Trades, 0 TP / 9 SL,
    ca. -5.29 PnL
  - TP-Outcomes: `tp_reachability` ca. 0.78,
    `expectation_break_pressure` ca. 0.18,
    `expectation_hold_support` ca. 0.78
  - SL-Outcomes: `tp_reachability` ca. 0.43,
    `expectation_break_pressure` ca. 0.62,
    `expectation_hold_support` ca. 0.46
- [x] Recovery-Schicht Lauf 39 bewertet.
  Ergebnis:
  `deep_pullback_recovery_watch` wurde sichtbar,
  markierte aber in diesem Lauf nur spÃ¤tere SLs.
  Outcome: 9 Trades, 0 TP / 9 SL, ca. -5.01 PnL.
  Replay: 2 Kandidaten mit `deep_pullback_recovery_watch`,
  beide spÃ¤ter SL.
  Folgerung: Vorheriger Zielhalt reicht nicht als Recovery-Beweis.
- [ ] NÃ¤chster Fixpunkt:
  Recovery nicht aus frÃ¼herer TragfÃ¤higkeit allein ableiten.
  ErgÃ¤nzen einer echten RÃ¼ckkehrdiagnose nach Bruch:
  - `target_recovery_momentum`
  - `target_recovery_confirmation`
  - `break_to_recovery_delta`
  - `recovery_after_break_watch`
  Ziel: tiefe RÃ¼ckatmung erst erkennen,
  wenn nach dem Bruch wieder Zielpfad-StÃ¤rke entsteht.
  Weiterhin observe-only, keine aktive Exit-Aenderung.
- [x] Recovery-RÃ¼ckkehrdiagnose observe-only eingebaut.
  Ergebnis:
  - `deep_pullback_recovery_watch` braucht jetzt neben Recovery-Potential
    auch `target_recovery_momentum`,
    `target_recovery_confirmation` und begrenzte
    `expectation_break_persistence`
  - neues Label `recovery_after_break_watch` erkennt RÃ¼ckkehr nach
    vorherigem Erwartungsbruch
  - neue Felder in Zielerwartung, Candidate-Log, Replay und Outcome:
    `target_recovery_momentum`, `target_recovery_confirmation`,
    `break_to_recovery_delta`, `recovery_after_break_watch`
  - die offene Position merkt sich letzte Zielpfadwerte,
    damit echte Verbesserung messbar wird.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Lauf 40 starten und auswerten:
  - fÃ¤llt `deep_pullback_recovery_watch` weniger auf echte SLs?
  - erscheint `recovery_after_break_watch` bei echter RÃ¼ckkehr?
  - bleibt `target_expectation_holds` TP-lastig?
  - bleibt `expectation_break_observe` SL-lastig?
  - gibt es erneut TP-Cuts im Replay?
- [x] Lauf 40 ausgewertet.
  Ergebnis: ca. +14.59 PnL bei 40 Trades, 20 TP / 20 SL,
  Profit Factor ca. 2.29. Der Lauf bleibt stark positiv.
- [x] Zielerwartungsachse Lauf 40 bestÃ¤tigt.
  Ergebnis:
  - `target_expectation_holds`: 20 Trades, 20 TP / 0 SL,
    ca. +25.94 PnL
  - `expectation_break_observe`: 13 Trades, 0 TP / 13 SL,
    ca. -7.38 PnL
  - TP-Outcomes: `tp_reachability` ca. 0.78,
    `expectation_break_pressure` ca. 0.18,
    `expectation_hold_support` ca. 0.78
  - SL-Outcomes: `tp_reachability` ca. 0.40,
    `expectation_break_pressure` ca. 0.63,
    `expectation_hold_support` ca. 0.43
- [x] Recovery-RÃ¼ckkehrdiagnose Lauf 40 bewertet.
  Ergebnis:
  `deep_pullback_recovery_watch` taucht im Outcome/Replay nicht mehr
  als Problem auf. Replay: 2 Kandidaten, beide spÃ¤ter SL,
  beide `expectation_break_observe`, beide hÃ¤tten Verlust reduziert,
  kein harmed/TP-Cut.
  Folgerung: Die strengere Momentum-Bedingung ist fachlich besser
  als die Recovery-Potential-Logik aus Lauf 39.
- [ ] NÃ¤chster PrÃ¼fpunkt:
  Noch 1-2 Observe-LÃ¤ufe sammeln:
  - bleibt `deep_pullback_recovery_watch` selten?
  - erscheint `recovery_after_break_watch` bei echten RÃ¼ckkehrfÃ¤llen?
  - bleibt Replay ohne TP-Cut?
  - bleibt Low/Non-Zone Verlustquelle?
- [x] MCM-Feld-Benennung geschaerft.
  Ergebnis:
  Die alte FeldgrÃ¶ÃŸen-Variable wurde in `MCM_FIELD_NEURON` umbenannt.
  Betroffen:
  - `config.py`
  - `MCM_Brain_Modell.py`
  Fachlich passt die Bezeichnung besser zum MCM-Feld als neuronaler
  Wahrnehmungsstruktur.
- [x] Kollektive MCM-Erweiterung dokumentiert.
  Ergebnis:
  `README.md` und `docs/01_plan/UMSETZUNGSPLAN.md` enthalten jetzt den
  spÃ¤teren Forschungszweig:
  DIO-Studienraum, soziale Semantik, kollektive Reflexion und
  Ãœbersetzung gleicher Formen bei eventuell variierender Sprache.
  Wichtig:
  Das ist keine aktuelle Kernanforderung und kein Ensemble-Regelwerk,
  sondern eine mÃ¶gliche Erweiterungsform nach stabilisiertem Einzel-DIO.
- [ ] SpÃ¤terer Forschungsfix:
  Semantische Reproduzierbarkeit prÃ¼fen:
  - identische Daten, leerer Speicher, mehrere getrennte DIO-LÃ¤ufe
  - unterschiedliche DatenrÃ¤ume vergleichen
  - Formsymbol-/Outcome-/Zielerwartungs-Ã„hnlichkeit messen
  - prÃ¼fen, ob Sprache Ã¤hnlich, variierend oder laufabhÃ¤ngig entsteht
  - erst danach DIO-zu-DIO-Kommunikation als Studienraum vorbereiten

---

# --------------------------------------------------
# 1. STATUS
# --------------------------------------------------

Das Projekt ist nicht mehr in einer frÃ¼hen Fix- oder Basisphase.

Die Kernmechanik steht bereits:

- Ã¤uÃŸere Wahrnehmung
- innere Runtime
- Entscheidungstendenz
- Action-Intent / Execution-State
- technische Handlungsbahn
- Episode / Review / Experience
- Persistenz
- Snapshot-/GUI-Basis

Offen sind jetzt nicht mehr die alten Basisfehler,
sondern ein kleiner Restblock im Nachweisraum sowie der weitere Architektur-Endausbau.

Aktuelle PrioritÃ¤t:

- PRIO 1 ist ab jetzt die Fertigstellung der neuronalen AktivitÃ¤t und kognitiven Innenfunktion
- danach folgt die saubere Funktion des MCM-Feldes als Mental-Core-Matrix-Wahrnehmungsfeld
- saubere Backtest-Logik bleibt der Kontrollpfad, ist aber nicht als Testdatei-Arbeit die aktuelle HauptprioritÃ¤t
- Live-Handoff / echter Exchange-Test bleibt wichtig, wird aber erst am Schluss validiert
- GUI-Ausbau bleibt nachrangig, solange Brain-Mechanik und Experience-Logik nicht fachlich fertig sind
- Testdateien / dedizierter Testausbau bleiben ebenfalls nachrangig, bis die neuronale und kognitive Mechanik steht

Der aktive Arbeitsfokus liegt damit zuerst auf `MCMNeuron`, neuronaler Aktivierung,
lokaler Kopplung, Regulation, Nachhall, Kontext-Memory und kognitiver Innenfunktion.
Danach liegt der Fokus auf `MCMField`, Feldtopologie, Innenmustern,
`inner_context_clusters` und Experience-Bewertung.

---

# --------------------------------------------------
# 2. BEREITS KORRIGIERT IM AKTUELLEN CODESTAND
# --------------------------------------------------

# --------------------------------------------------
# 2.1 state_delta korrigiert
# --------------------------------------------------

Bereits umgesetzt:

- ereignislokale Bildung von `state_before`, `state_after`, `state_delta`
- gemeinsamer Ãœbergang fÃ¼r Stats-Kontext und Episode-Payload
- Snapshot-Commit erst nach dem jeweiligen Event
- alte Null-/Doppelsnapshot-Pfade in Entry-/Pending-/Nicht-Handlungs-Pfaden bereinigt

Folge:

- Episode / Experience arbeiten an diesen Stellen wieder auf realen ZustandsÃ¼bergÃ¤ngen

---

# --------------------------------------------------
# 2.2 Statistik-Semantik korrigiert
# --------------------------------------------------

Bereits umgesetzt:

- `pnl_netto` startet als reiner Nettowert bei `0.0`
- `current_equity` wird getrennt als `start_equity + pnl_netto` gefÃ¼hrt
- `expectancy` baut damit auf realem Nettowert statt auf Equity-Basis auf

Folge:

- Nettoergebnis und Erwartungswert sind semantisch wieder sauber getrennt

---

# --------------------------------------------------
# 2.3 structure_bands / Exit-Strukturdiagnose korrigiert
# --------------------------------------------------

Bereits umgesetzt:

- Exit-/Cancel-Pfade nutzen aktuellen Exit-Kontext statt alten Entry-Kontext
- aktuelle `structure_perception_state` lÃ¤uft bis in `on_exit()` / `on_cancel()`
- `outcome_records` tragen reale Exit-StrukturqualitÃ¤t
- `structure_bands` werden daraus sauber neu aufgebaut

Folge:

- Exit-KPI Ã¼ber StrukturqualitÃ¤t ist im aktuellen Backtest-/Bot-Pfad wieder fachlich belastbar

---

# --------------------------------------------------
# 2.4 attempt_feedback / proof-Felder korrigiert
# --------------------------------------------------

Bereits umgesetzt:

- Proof-/Regulationsfelder werden im Attempt-Feedback sauber aggregiert
- Snapshot-Fallbacks sind vorhanden
- In-Trade-Update-Pfade tragen die fehlenden Felder weiter
- Experience-Linking / Episode-History fÃ¼hrt diese Felder weiter

Bereits sauber gefÃ¼hrt insbesondere:

- `regulatory_load`
- `action_capacity`
- `survival_pressure`
- `pressure_release`
- `load_bearing_capacity`
- `state_stability`
- `capacity_reserve`
- `recovery_balance`

Folge:

- die alte statistische Abflachung dieser DiagnosegrÃ¶ÃŸen ist im aktuellen Code nicht mehr der Hauptfehler

---

# --------------------------------------------------
# 3. PRIO 1 â€“ BRAIN-LOGIK / NEURONALE MECHANIK
# --------------------------------------------------

# --------------------------------------------------
# 3.1 Brain-Mechanik zuerst fertigstellen
# --------------------------------------------------

Aktive Arbeitsrichtung:

- zuerst `MCMNeuron` und neuronale AktivitÃ¤t als tragende Innenmechanik stabilisieren
- lokale Nachbarschaft, Kopplung, Regulation, Nachhall und Kontext-Memory fachlich sauber halten
- kognitive Innenfunktion aus Wahrnehmung, Verarbeitung, Felt-State, Thought-State, Meta-Regulation und Erwartung sauber fÃ¼hren
- danach `MCMField` als Mental-Core-Matrix-Feld und Wahrnehmungsraum stabilisieren
- Feldtopologie, Arealbildung und Feldverlauf weiter als echte Innenraum-Mechanik ausbauen
- `inner_context_clusters` vom formalen Cluster-Speicher zum Innenmuster- und Innenfeldspeicher vertiefen
- Experience-Bewertung weiter auf Zustandswirkung, TragfÃ¤higkeit, Belastung, Entlastung und HandlungsfÃ¤higkeit ausrichten
- Backtest-Pfade als sauberen Kontroll- und AusfÃ¼hrungspfad erhalten

Nicht aktive HauptprioritÃ¤t:

- Live-Exchange-Validierung
- GUI-Umbau
- Testdatei-Ausbau

Diese Punkte bleiben wichtig, folgen aber erst nach der fachlichen Stabilisierung des Brains.

---

# --------------------------------------------------
# 3.2 Nachweisraum / Live-Handoff zwischen Pending, Fill und Position schlieÃŸen
# --------------------------------------------------

Teilweise korrigiert:

- `_handle_pending_entry()` fragt im Live-Pfad `get_active_order_snapshot()` ab
- `source="position_context"` wird an `_finalize_pending_fill_handoff()` Ã¼bergeben
- `_finalize_pending_fill_handoff()` schreibt `stats.on_attempt(status="filled")`, Episode-Event und `self.position`
- `get_active_order_snapshot()` erzwingt vor der Snapshot-Auswertung einmalig einen synchronen Bootstrap-/Exchange-Sync
- `get_active_order_snapshot()` liest offene Order-TP/SL jetzt aus `takeProfitPrice/stopLossPrice` und `takeProfitRp/stopLossRp`
- `get_active_order_snapshot()` bleibt bei offener Order auch ohne Exchange-`timestamp` verwertbar
- `place_order()` Ã¼bernimmt identische offene Orders jetzt inklusive `_ACTIVE_TP`, `_ACTIVE_SIDE` und Entry-/Risk-Kontext
- `_sync_with_exchange()` Ã¼bernimmt eindeutig offene Orders jetzt inklusive `_ACTIVE_TP`, `_ACTIVE_SIDE` und Entry-/Risk-Kontext
- `_sync_with_exchange()` ergÃ¤nzt bei bereits bestÃ¤tigter aktiver Order fehlenden `_ACTIVE_TP`, `_ACTIVE_SIDE` und Entry-/Risk-Kontext aus `open_orders`
- `get_active_order_snapshot()` synchronisiert jetzt bei verschwundener aktiver Order aktiv nach
- wenn nach dem Sync eine Position offen ist, bleibt der Positionskontext fÃ¼r den Bot-Handoff erhalten
- wenn keine Position offen ist, wird die verschwundene Order als `exchange_disappeared` in das Cancel-Tracking gegeben
- Live-Fill schreibt den `live_handoff`-Kontext inklusive `pending_order_id`, `snapshot_id`, Entry/TP/SL, `entry_ts` und `handoff_reason` in `position_meta`
- Restart-Recovery schreibt `recovery_source` und `recovery_snapshot` in `meta`
- aktive Restart-Positionen erhalten einen verwertbaren `entry_ts` / `last_checked_ts`
- Restart-Recovery setzt `execution_state` auf `pending_recovered` oder `position_recovered`
- Restart-Recovery schreibt ein technisches Episode-Event Ã¼ber `pending_update` oder `position_update`
- Restart-Recovery markiert Memory-State als dirty und committet den Regulationssnapshot
- Restart-Recovery speichert den wiederhergestellten Zustand sofort per Forced-Save

Weiter zu prÃ¼fen:

- echter Live-Test `pending -> filled -> position` gegen Exchange-Zustand
- ob TP/SL/Entry-Kontext nach Restart im echten Exchange-Fall vollstÃ¤ndig belastbar bleibt

Folge:

- der Live-Fill-Handoff ist bot-seitig nachgezogen, aber noch nicht real-live-validiert
- dieser Punkt bleibt bewusst nachrangig, bis Brain-Mechanik und Backtest-Logik fachlich stabil sind

---

# --------------------------------------------------
# 3.3 MCMField-Speicherfehler korrigiert / feste Feldtopologie vorbereiten
# --------------------------------------------------

Bereits korrigiert im aktuellen Dateistand:

- `_build_local_neighbor_state_map()` nutzt feste Topologie-Nachbarschaften
- der alte permanente `N x N x D`-Zwischenspeicher ist an dieser Stelle entfernt
- lokale `N x K` Nachbarschaften bleiben erhalten
- jedes Neuron erhÃ¤lt `field_position` und `topology_neighbors`
- der Feldzustand selbst bleibt als `N x D` erhalten
- `MCMField.read_snapshot()` liefert `topology_rows`, `topology_cols`, `topology_positions` und `topology_neighbor_indices`

Fachliche Bedeutung:

- Neuronen dÃ¼rfen denselben Umweltreiz wahrnehmen
- sie sollen aber nicht alle global vom gesamten Feld gleichgeschaltet werden
- lokale Eigenreaktion, Nachbarschaft, KohÃ¤renz und Resonanz bilden die Informationsinseln
- `velocity` ist als Zustandsbewegung zu verstehen, nicht als Ortsbewegung des Neurons
- Zielbild ist ein neuronales Gewebe aus festen Feldknoten mit beweglichen MCM-ZustÃ¤nden

Weiter zu beobachten:

- `_build_areal_state()` baut Areale jetzt ohne dauerhafte vollstÃ¤ndige `N x N`-Distanzmatrix auf
- `_build_areal_components()` berechnet Distanzen zeilenweise pro Neuron
- interne Areal-Dichte wird pro Komponente zeilenweise berechnet
- Arealbildung soll lokale Informationsinseln sichtbar machen, nicht globale Feldgleichschaltung erzeugen

Offene Zielkorrektur:

- Cluster-/Areal-Lesung weiter auf gekoppelte Zustandsmuster im festen Feld ausrichten
- lokale Erfahrungsmodulation noch nicht stark an feste Feldknoten zurÃ¼ckfÃ¼hren
- hÃ¶here FeldauflÃ¶sung weiter als hÃ¶here WahrnehmungsauflÃ¶sung behandeln
- `energy` / `velocity` kompatibel als bestehende Runtime-OberflÃ¤che erhalten
- GUI-Snapshot/Visualisierung erst nach fertiger Topologie auf neuronales Gewebe angleichen

PrioritÃ¤t:

1. `field_topology_layout_state` weiter als Wahrnehmungs- und Nachweiswert fÃ¼hren
2. bestehende Runtime-KompatibilitÃ¤t erhalten
3. Cluster-/Areal-Lesung weiter auf feste Feldknoten nachziehen
4. lokale RÃ¼ckwirkung erst nach stabiler Topologie vertiefen
5. GUI-Darstellung danach auf neuronales Gewebe angleichen

---

# --------------------------------------------------
# 4. PRIO 2 â€“ STRUKTURELLE KORREKTUREN
# --------------------------------------------------

# --------------------------------------------------
# 4.1 Persistenz weiter entkoppeln
# --------------------------------------------------

Offen, aber nicht mehr maximal kritisch:

- Persistenz ist bereits Ã¼ber Dirty-Flag und Cooldown teilweise entschÃ¤rft
- trotzdem liegen Save-/Flush-Pfade weiter nah am Kernlauf

Folge:

- Bot-Kern bleibt unnÃ¶tig eng mit Save-/Flush-Logik gekoppelt

Wichtig:

- das ist ein realer Punkt
- aber kein ungefilterter Dauer-Schreibfehler mehr

---

# --------------------------------------------------
# 4.2 Runtime / Bot-State weiter trennen
# --------------------------------------------------

Offen:

- `Bot` bÃ¼ndelt weiter AuÃŸenwahrnehmung, Runtime, Handlungsbahn, Experience, Persistenz und Snapshot-Orchestrierung
- die Zieltrennung Ebene 1 / Ebene 2 / Ebene 3 ist damit noch nicht strukturell verhÃ¤rtet

Ziel:

- weniger Vermischung von Runtime und Bot-State
- klarere Trennung von Wahrnehmung / Innenprozess / Entwicklung

---

# --------------------------------------------------
# 4.3 Innenkontextcluster als Innenfeldspeicher und aktive Kontextspur vertiefen
# --------------------------------------------------

Teilweise umgesetzt:

- `MCMNeuron` fÃ¼hrt jetzt eine explizitere neuronale AktivitÃ¤tslesung
- neue Neuronwerte: `receptivity`, `overload`, `recovery_tendency`, `memory_resonance`, `context_reactivation`, `coupling_resonance`, `activity_label`, `activation_components`
- AuÃŸenreiz wird pro Neuron lokal Ã¼ber Eigenzustand, Memory-Ausrichtung, Topologie-Bias und Regulationsdruck moduliert
- `activation` entsteht jetzt aus AuÃŸenreiz, Replay, Kontext-Memory, lokaler Kopplung, Memory-Feedback, Velocity und Resonanz
- `neural_felt_state` nutzt die neuen Werte fÃ¼r Ãœberlast, Erholung, Kopplungsresonanz und Kontextreaktivierung
- `MCMField` fÃ¼hrt jetzt eine schwache AktivitÃ¤tsdiffusion Ã¼ber feste Topologie-Nachbarn
- `field_perception_state` liest lokale AktivitÃ¤tsinseln als Wahrnehmungsstruktur
- AktivitÃ¤tsinseln fÃ¼hren Masse, Aktivierung, Druck, KohÃ¤renz, Kontextreaktivierung, Spread und `state_label`
- Feldwahrnehmung fÃ¼hrt jetzt zusÃ¤tzlich Fokus, Klarheit, StabilitÃ¤t, Fragmentierung, Strain und dominante AktivitÃ¤tsinsel
- Feldwahrnehmungslabels wie `active_perception_field`, `coherent_perception_field`, `fragmented_perception_field`, `memory_reactivated_field` und `strained_field` sind angebunden
- `field_perception_state` lÃ¤uft in den MCM-Snapshot und in `inner_field_perception_state`
- AktivitÃ¤tsinseln und `field_perception_label` laufen jetzt in `inner_pattern_identity`, `field_pattern_signature`, `field_pattern_vector`, `inner_context_clusters`, `memory_state` und `mcm_experience_space`
- der Kontextcluster-Vektor enthÃ¤lt die AktivitÃ¤tsinselachsen, damit Ã¤hnliche Innenkontexte nicht nur nach globalem Feldzustand, sondern auch nach lokaler Feldwahrnehmung gruppiert werden
- `processing_state`, `felt_state` und `thought_state` nutzen die Feldwahrnehmung jetzt als kognitive Evidenzschicht
- neue Lesewerte: `field_perception_pressure`, `field_perception_support`, `field_perception_clarity`, `field_perception_focus`, `field_perception_stability`, `field_perception_fragmentation`, `field_perception_strain` plus Inselmetriken in Verarbeitung, GefÃ¼hl und Denken
- `meta_regulation_state` nutzt die Feldwahrnehmung jetzt fÃ¼r Handlungshemmung, Handlungsfreigabe, Beobachtungsbedarf und Replan-Druck
- neue Meta-Werte: `field_perception_instability`, `field_observation_need`, `field_replan_pressure`, `field_action_support`
- harte Feldwahrnehmungs-Gates sind ergÃ¤nzt: starke Fragmentierung fÃ¼hrt zu `field_island_fragmentation_guard`, starker Strain zu `field_island_strain_guard`, klare/stabile Feldwahrnehmung zu kontrolliertem `field_perception_clear_act`
- Experience-Umbau ist fachlich geschÃ¤rft: kein binÃ¤res `TP gut / SL schlecht`, sondern neurochemisch gedÃ¤mpfte Erfahrungswirkung
- ProfitabilitÃ¤t bleibt als innere Zielspannung wichtig, aber nur gefiltert Ã¼ber RegelqualitÃ¤t, TragfÃ¤higkeit, StabilitÃ¤t, Varianz, Entlastung und Ãœberlast
- `build_experience_neurochemical_effect()` ist umgesetzt und trennt Profitspannung, Entlastung, StabilitÃ¤t, Disziplin, Confidence, Ãœberaktivierung, Chaos, Varianz, Ãœberlast, TragfÃ¤higkeit und Selbstvertrauen
- `_experience_reward_delta()` ist nur noch ein KompatibilitÃ¤ts-Wrapper auf `experience_effect_score`
- die neurochemischen Wirkachsen laufen in Experience-Summary, Episode-History, Experience-Space, Link-Buckets und Experience-Similarity-Achsen
- SL-Episoden werden nach oben gedeckelt, damit sauberer Verlust ProzessqualitÃ¤t bestÃ¤tigen kann, aber kein starkes Gewinnsignal wird
- chaotische TP-Episoden werden durch Chaos-, Varianz- und Ãœberaktivierungsachsen gedÃ¤mpft
- `inner_context_clusters` tragen jetzt `experience_neurochemical_profile`, `neurochemical_support`, `neurochemical_strain` und gleitende neurochemische `avg_*` / `last_*` Werte
- `pattern_reinforcement`, `pattern_attenuation` und `trust` werden schwach durch TragfÃ¤higkeit/StabilitÃ¤t oder Chaos/Ãœberaktivierung moduliert
- `active_context_trace` nutzt die neurochemischen Achsen schwach fÃ¼r Nachhall, HandlungsstÃ¼tze, Beobachtungsdruck, Replan-Druck und Replay-Impuls
- `memory_state.py` persistiert die neuen neurochemischen Clusterprofile
- der Innenraum wird real Ã¼ber `felt_state`, `thought_state`, `meta_regulation_state`, `expectation_state`, `state_before`, `state_after`, `state_delta` und `mcm_experience_space` getragen
- `inner_context_clusters` sind im aktuellen Code formal vorhanden, werden aktualisiert und persistiert
- Pattern-Verdichtung ist begonnen Ã¼ber `inner_pattern_support`, `inner_pattern_conflict`, `inner_pattern_fragility`, `inner_pattern_bearing`, `pattern_reinforcement` und `pattern_attenuation`
- `active_context_trace` ist als Runtime-Nachhall eingefÃ¼hrt
- aktive Kontextspur besitzt `activation`, Decay und Reaktivierung aus `inner_context_clusters`
- aktive Kontextspur wirkt schwach auf Pattern-Modulation zurÃ¼ck
- aktive Kontextspur wirkt schwach auf Replay-/Feldimpuls zurÃ¼ck
- aktive Kontextspur wird zusÃ¤tzlich neurochemisch gedÃ¤mpft: tragfÃ¤hige Muster bleiben erreichbarer, chaotische/Ã¼beraktive Muster werden vorsichtiger reaktiviert
- RÃ¼ckfÃ¼hrung in lokale `MCMNeuron.memory_trace` ist als erste schwache aktive Kontextspur umgesetzt
- `context_memory_impulse` wird im Inner-Snapshot als eigene lokale Kontext-Memory-Kennzahl sichtbar; die Neuron-GUI-Datei ist im aktuellen Upload nicht enthalten und daher nicht geprÃ¼ft
- `field_neuron_context_memory_impulse_norm_mean` lÃ¤uft jetzt in `inner_context_clusters`, `current_vector`, Experience-Link-Achsen und bleibt Ã¼ber `memory_state` persistierbar
- `context_memory_impulse` wird in der inneren Musterbeschriftung als `memory_reactivated_neurons` sichtbar, wenn lokale Kontextreaktivierung dominiert
- Experience-Similarity fÃ¼hrt `context_memory_impulse_axis`, `active_context_activation_axis`, `active_context_balance_axis` und `context_memory_reactivation_axis`
- `neural_felt_state` ist als lesende neuronale Felt-Schicht angebunden
- `neural_felt_bearing`, `neural_felt_pressure`, `neural_felt_memory_resonance`, `neural_felt_context_reactivation` und `neural_felt_label` bleiben Ã¼ber `memory_state` persistierbar
- `neural_felt_*` lÃ¤uft zusÃ¤tzlich in Experience-Summary, Episode-Felt-Summary, Similarity-Achsen, Runtime-Snapshot, Decision-State, Brain-Snapshot und `active_context_trace`
- `active_context_trace` trÃ¤gt `neural_felt_*` als Lesefeld ohne stÃ¤rkere Replay-/Feldimpuls-Gewichtung
- `inner_field_history` ist als lesender Feldverlauf Ã¼ber mehrere Ticks angebunden und Ã¼ber `memory_state` persistierbar
- `inner_field_history_*` lÃ¤uft in `inner_context_clusters`, `current_vector`, Experience-Summary, Runtime-/Brain-Snapshot, `active_context_trace` und `episode_internal["signal"]`
- `active_context_trace` trÃ¤gt `inner_field_history_*` als Lesefeld ohne stÃ¤rkere Replay-/Feldimpuls-Gewichtung
- feste Feldtopologie ist begonnen: `MCMField` fÃ¼hrt feste `field_position` und `topology_neighbors` je `MCMNeuron`
- `field_topology_layout_state` lÃ¤uft in `inner_field_perception_state`, `inner_context_clusters`, `current_vector`, `active_context_trace` und Experience-Similarity-Achsen
- `active_context_trace` trÃ¤gt `field_topology_layout_state` als Lesefeld ohne stÃ¤rkere Replay-/Feldimpuls-Gewichtung
- `field_areal_topology_*` lÃ¤uft in `inner_context_clusters`, `current_vector`, `active_context_trace`, `episode_internal["signal"]` und Experience-Similarity-Achsen
- `field_areal_topology_*` bleibt Lesewert ohne stÃ¤rkere Replay-/Feldimpuls-Gewichtung
- `inner_pattern_identity` ist als erste Innenmuster-IdentitÃ¤t begonnen und lÃ¤uft in `inner_context_clusters`, `current_vector`, Cluster-RÃ¼ckgabe, `memory_state` und `active_context_trace`
- `active_context_trace` trÃ¤gt `field_pattern_signature_key`, `inner_pattern_identity`, `inner_pattern_identity_label` und `inner_pattern_identity_confidence` ohne stÃ¤rkere Replay-/Feldimpuls-Gewichtung
- `inner_pattern_identity_stability` ist als Lesewert ergÃ¤nzt und lÃ¤uft in Cluster-RÃ¼ckgabe, `active_context_trace`, `mcm_runtime_brain_snapshot["signal"]`, `episode_internal["signal"]`, `mcm_experience_space` und `memory_state`
- `inner_pattern_identity_streak`, `inner_pattern_identity_recurrent`, `inner_pattern_identity_changed` und `inner_pattern_identity_last_seen_tick` bleiben reine Wiedererkennungs-/StabilitÃ¤tswerte ohne stÃ¤rkere Replay-/Feldimpuls-Gewichtung
- Runtime-Profiling ist als Debug-Schicht angebunden und schreibt nach `debug/mcm_profile.csv`


Offen:

- wiederkehrende Feldformen sind noch nicht als echte lokale Erfahrungsareale im Neuronenfeld verankert
- Replay-RÃ¼ckwirkung bleibt bewusst schwach begrenzt und ist noch kein vollstÃ¤ndiger lokaler Erfahrungsumbau

ErgÃ¤nzte Zieldefinition:

- Informationscluster werden nicht durch Felddruck gelÃ¶scht
- Felddruck verÃ¤ndert PrioritÃ¤t, Aktivierung und ZugÃ¤nglichkeit
- nicht genutzte oder nicht mehr resonante Information verliert aktive BindungsstÃ¤rke
- diese Information bleibt als Nachhall oder latente Erfahrung reaktivierbar
- dadurch wird lokaler Organisationsraum frei fÃ¼r neue Clusterbildung
- Reorganisation bedeutet Informationsumschichtung statt Informationsverlust
- KohÃ¤renzstÃ¤rke beschreibt Verdichtung, TragfÃ¤higkeit und aktuelle Bindung eines Clusters
- GUI-Farben sollen spÃ¤ter diese KohÃ¤renzstÃ¤rke und den Clusterzustand sichtbar machen

Ziel:

- `context_clusters` als Ã¤uÃŸerer / gesamt-situativer Signaturraum klar halten
- `inner_context_clusters` fachlich davon getrennt als Innenmuster- / Innenfeldspeicher vertiefen
- aktive Kontextspur im Replay-/Feldimpuls weiter kontrolliert beobachten und begrenzen
- Vermeidungs-, Entlastungs-, Reorganisations- und Wiedererkennungslernen sauber auf Innenmuster abbilden
- ClusterzustÃ¤nde als aktiv getragen, nachhallend, latent oder frei werdend unterscheidbar machen

---

# --------------------------------------------------
# 4.4 Experience-Bewertungslogik weiter auf Zustandswirkung umstellen
# --------------------------------------------------

Umgesetzt:

- `build_experience_neurochemical_effect()` nutzt `state_support`, `state_strain` und `state_effect_delta` als Bewertungszentrum
- Areal-StÃ¼tze, Areal-Konflikt, Felt-Bearing und Regulationskosten laufen in die Bewertung ein
- aktive Kontextspur und `field_neuron_context_memory_impulse_norm_mean` laufen als schwacher Experience-Wirkraum in Support/Strain ein
- formale Outcomes wirken weiter als Ereigniskontext, aber ihre Wirkung wird stÃ¤rker an `state_effect_delta` gebunden
- `_experience_reward_delta()` ist nur noch ein Wrapper auf die neurochemische Wirkfunktion
- Experience-Link-Buckets speichern gleitende `avg_*` und `last_*` Profile der neurochemischen Wirkachsen

Offen:

- die neurochemischen Link-Profile sind jetzt schwach als lokale Muster-/Replay-Modulation aktiv, aber noch nicht als tiefes lokales Neuronenareal gelernt
- lokale RÃ¼ckfÃ¼hrung auf Feldmuster und neuronale TeiltrÃ¤ger bleibt bewusst schwach und muss real beobachtet werden
- `neural_felt_state` ist noch Diagnose-/Wahrnehmungsschicht und kein starker lokaler LernverstÃ¤rker
- `neural_felt_*` wird im `active_context_trace` nur sichtbar mitgetragen und verÃ¤ndert keine Replay-Gewichtung
- `inner_field_history_*` wird im `active_context_trace` und in `episode_internal["signal"]` nur sichtbar mitgetragen und verÃ¤ndert keine Replay-Gewichtung
- `field_topology_layout_state` wird im `active_context_trace` und in Experience-Similarity-Achsen nur sichtbar mitgetragen und verÃ¤ndert keine Replay-Gewichtung
- `field_areal_topology_*` wird im `active_context_trace`, in `episode_internal["signal"]` und in Experience-Similarity-Achsen nur sichtbar mitgetragen und verÃ¤ndert keine Replay-Gewichtung
- `inner_pattern_identity` wird im `active_context_trace` und in `episode_internal["signal"]` nur sichtbar mitgetragen und verÃ¤ndert keine Replay-Gewichtung
- Runtime-Profiling misst nur Laufzeiten und verÃ¤ndert keine Entscheidung, keine Replay-Gewichtung und keine Feldimpulse

Ziel:

- Experience bewertet primÃ¤r `state_before`, `state_after`, `state_delta` und TragfÃ¤higkeitswirkung
- `tp_hit`, `sl_hit`, `cancel`, `timeout` bleiben nur Ereigniskontext
- positive und negative RÃ¼ckfÃ¼hrung entsteht aus Belastung, Entlastung, Stabilisierung, Fragilisierung und HandlungsfÃ¤higkeit
- aktive Kontextspuren verstÃ¤rken oder schwÃ¤chen sich aus Wiedererkennung und Zustandswirkung, nicht aus starren Ergebnisetiketten
- Lernen wird dadurch sauberer als UmgangsfÃ¤higkeit statt Ergebnisreflex modelliert

---

# --------------------------------------------------
# 4.5 MCM-Feldtopologie / Feldverlauf / Innenfeldspeicher ausbauen
# --------------------------------------------------

Teilweise umgesetzt:

- `field_cluster_links` und `field_areal_links` werden zu `field_topology_state` verdichtet
- `field_topology_state` fÃ¼hrt Link-Anzahl, Link-Dichte, mittlere Distanz, Topologie-KohÃ¤renz, Topologie-Spannung und Topologie-Label
- Feldtopologie lÃ¤uft jetzt in `inner_field_perception_state`, `inner_context_clusters`, `current_vector`, Experience-Summary, Experience-Space, Experience-Link-Buckets und `memory_state`
- `field_topology_state` steht fÃ¼r die Neuron-GUI als Topologie-Zustand, LinkverhÃ¤ltnis, Link-Dichte, KohÃ¤renz und Spannung bereit; die Neuron-GUI-Datei ist im aktuellen Upload nicht enthalten und daher nicht geprÃ¼ft

Offen:

- ein eigener persistenter Speicher fÃ¼r wiederkehrende Feldformen, Driftmuster und RegulationsverlÃ¤ufe fehlt aktuell
- Feldverlauf Ã¼ber mehrere Ticks ist noch nicht als eigener Innenfeldpfad gespeichert
- die Visualisierung zeigt Feldformen, fÃ¼hrt aber noch keinen persistenten Feldformverlauf

Ziel:

- Feldcluster nicht nur erkennen, sondern in ihrer GrÃ¶ÃŸe, Dichte, StabilitÃ¤t, Verschiebung und Beziehung zueinander lesbar machen
- die Gesamtform des MCM-Feldes als Feldtopologie beschreiben: Verdichtung, Streuung, BrÃ¼cken, Trennung, Polarisierung, RÃ¼ckfÃ¼hrung
- Feldverlauf Ã¼ber Zeit mitfÃ¼hren, damit kognitive Verlagerung, Drift und regulatorische Reorganisation als Zustandsweg erkennbar werden
- einen verdichteten Innenfeldspeicher fÃ¼r wiederkehrende Clusterkonfigurationen, Feldformen, Driftmuster und RÃ¼ckfÃ¼hrungsbewegungen aufbauen
- diese Feldwahrnehmung direkt fÃ¼r Meta-Regulation, Handlungstendenz und Visualisierung nutzbar machen

---

# --------------------------------------------------
# 5. PRIO 3 â€“ FACHLICHER AUSBAU
# --------------------------------------------------

# --------------------------------------------------
# 5.1 Review / Cluster-Bewertung weiter vertiefen
# --------------------------------------------------

Teilweise bereits umgesetzt:

- TragfÃ¤higkeit ist bereits stÃ¤rker als explizite BewertungsgrÃ¶ÃŸe verankert
- Lernen ist bereits erkennbar stÃ¤rker als UmgangsfÃ¤higkeit modelliert
- Reibung / Energie sind bereits Ã¼ber `bearing_regulation_cost`, `relief_quality`, `carrying_room`, `felt_bearing`, `felt_regulation_quality`, `experience_friction_cost` und `experience_energy_cost` technisch verankert
- `review_notes` bewertet bereits stÃ¤rker TragfÃ¤higkeit, Regulationskosten, Entlastung und Handlungsspielraum statt nur klassisch Ergebnis / Trade-Ausgang

Noch offen:

- Review und Cluster-Bewertung stÃ¤rker auf TragfÃ¤higkeit statt Ergebnis ausrichten
- innere Musterbewertung deutlicher von Geld- und Trade-Etiketten lÃ¶sen
- Outcome noch klarer als Zustandswirkung statt Geldwirkung ausformen
- Lernen als UmgangsfÃ¤higkeit technisch noch konsequenter durchziehen
- nach der Grundumstellung der Experience-Bewertung die Folgeauswertung in Reviews, Link-Buckets und Cluster-Scoring nachziehen

---

# --------------------------------------------------
# 5.2 KPI / Auswertung umbauen
# --------------------------------------------------

Noch offen:

- klassische Trade-KPIs als Hauptbewertung weiter zurÃ¼ckbauen oder umordnen
- TragfÃ¤higkeit, innere Reibung, Belastung, Entlastung und HandlungsfÃ¤higkeit stÃ¤rker als NachweisgrÃ¶ÃŸen aufbauen
- alte Ergebnislogik weiter zurÃ¼ckdrÃ¤ngen

Aktuell weiterhin alt geprÃ¤gt:

- `pnl_tp`
- `pnl_sl`
- `equity_peak`
- `max_drawdown_abs`
- `max_drawdown_pct`
- `winrate`
- `profit_factor`

---

# --------------------------------------------------
# 5.3 GUI / Visualisierung umbauen
# --------------------------------------------------

Noch offen:

- GUI weiter von alter KPI-Zentrierung lÃ¶sen
- AuÃŸenwelt / Innenwelt / Entwicklung noch klarer trennen
- Experience- und TragfÃ¤higkeitsverlauf stÃ¤rker in den Mittelpunkt stellen

Wichtig:

- Snapshot-/GUI-Basis ist vorhanden
- Datenpufferung ist bereits umgesetzt
- offen ist der inhaltliche Umbau, nicht mehr die reine Grundanzeige

---

# --------------------------------------------------
# 5.4 Tests spÃ¤ter nachziehen
# --------------------------------------------------

Nachrangig, nicht aktuelle Hauptarbeit:

- dedizierte Tests fÃ¼r `bot_gate_funktions.py`
- dedizierte Tests fÃ¼r `mcm_core_engine.py`
- Fokus auf Zustandsentwicklung und Experience-Konsistenz
- Fokus nicht primÃ¤r auf klassische Trade-Erfolgsmetriken

Wichtig:

- Testdateien werden erst priorisiert, wenn neuronale AktivitÃ¤t, kognitive Innenfunktion und MCM-Feldmechanik fachlich stabiler sind
- bis dahin bleibt Backtest-Logik der praktische Kontrollpfad fÃ¼r saubere Brain-Funktion

---

# --------------------------------------------------

---

# --------------------------------------------------
# 6. Feldentscheidungs-Protokoll fÃ¼r Backtest / Replay
# --------------------------------------------------

Status 2026-05-03: umgesetzt.

Umgesetzt:

- `MCM_FIELD_DECISION_PROTOCOL_DEBUG` und `MCM_FIELD_DECISION_PROTOCOL_EVERY_N` in `config.py` angelegt.
- `MCM_Brain_Modell.py` schreibt ein kompaktes `debug/mcm_field_decision_protocol.csv`.
- Der erste Feldentscheid wird sofort geschrieben; danach greifen Sampling und Phasenwechsel.
- Laufende Zaehler fÃ¼r `observe`, `replan`, `hold`, `act`, Gruende und Feldlabels liegen in `bot.mcm_field_decision_protocol`.
- Experience-Space fÃ¼hrt `field_decision_outcome_protocol`, um Phasen spÃ¤ter gegen ProzessqualitÃ¤t, TragfÃ¤higkeit und StabilitÃ¤t zu prÃ¼fen.

NÃ¤chster sinnvoller Anschluss:

- Backtest-Lauf auswerten und prÃ¼fen, ob Fragmentierung/Strain zu vielen `observe`/`replan` Phasen fÃ¼hrt.
- Danach Geschwindigkeit/Mem-Write-Last messen und die Speicherlogik verschlanken.

---

# --------------------------------------------------
# 7. Schreiblast-/Speicher-Performance messen
# --------------------------------------------------

Status 2026-05-03: erster Diagnose-Haken umgesetzt.

Umgesetzt:

- `MCM_FILE_WRITE_PROFILE_DEBUG`, `MCM_FILE_WRITE_PROFILE_MIN_MS` und `MCM_FILE_WRITE_PROFILE_EVERY_N` in `config.py` angelegt.
- `debug_reader.py` schreibt bei aktivierter Messung `debug/mcm_file_write_profile.csv`.
- Erfasst werden Pfad, Operation, Dauer, Bytes und Kontext.
- Messpunkte liegen auf Debug-Schreiber, Runtime-Profil, Memory-State-JSON, Runtime-Snapshot-JSON und Feldentscheidungs-Protokoll.

NÃ¤chster sinnvoller Anschluss:

- Einen echten Backtest laufen lassen und `debug/mcm_file_write_profile.csv` auswerten.
- Danach entscheiden:
  - Sampling/Intervalle hochsetzen
  - groÃŸe JSON-Strukturen kappen
  - Hot/Cold-Memory trennen
  - oder Experience/Replay in SQLite bzw. Delta-Logs verschieben.

Ergebnis aus dem Lauf `1-2_2026_5m_SOLUSDT.csv` ohne GedÃ¤chtnis:

- `attempt_records.jsonl` war mit ca. 106 MB zu groÃŸ.
- Inner-/Visual-Snapshots und `memory_state.json` erzeugten zusammen deutlich messbare Schreiblast.
- `primary_field_step` ist ebenfalls ein groÃŸer Laufzeitblock und muss separat betrachtet werden.

Erste Optimierung umgesetzt:

- Attempt-JSONL wird Ã¼ber `TRADE_STATS_ATTEMPT_RECORD_EVERY_N` gesampelt.
- Attempt-Kontext wird Ã¼ber `TRADE_STATS_ATTEMPT_RECORD_COMPACT` verschlankt.
- `trade_stats.json` wird Ã¼ber `TRADE_STATS_JSON_SAVE_EVERY_N` auf Attempt-Pfaden periodisch statt bei jedem Attempt geschrieben.
- Outcome-/Exit-Pfade schreiben weiterhin sofort.

NÃ¤chster sinnvoller Anschluss:

- Gleichen Backtest erneut laufen lassen und DateigrÃ¶ÃŸen plus `mcm_file_write_profile.csv` vergleichen.
- Danach Snapshot-Frequenz und MCM-Feld-Rechenlast optimieren.

Nachvergleich `debug/alter_debug` gegen neuen `debug`-Lauf:

- `attempt_records.jsonl` fiel von ca. 101,15 MB auf ca. 2,14 MB.
- Die Attempt-Record-Entlastung greift.
- Snapshot-Writes bleiben nach der Entlastung der grÃ¶ÃŸte Schreibblock.
- `primary_field_step` bleibt der grÃ¶ÃŸte Rechenblock.

Zweite Optimierung umgesetzt:

- `MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N` von 10 auf 25 gesetzt.
- `MCM_VISUAL_SNAPSHOT_FORCE_ON_STATE_CHANGE` fÃ¼r Backtest-/Brain-PrioritÃ¤t deaktiviert.

NÃ¤chster sinnvoller Anschluss:

- Erneut denselben Backtest laufen lassen.
- Danach prÃ¼fen, ob Snapshot-Writes wie erwartet weiter fallen.
- Danach `primary_field_step` fachlich optimieren, ohne die MCM-Wahrnehmungsmechanik platt zu machen.

Fairer Nachvergleich mit gleicher Datei `test_5m_SOLUSDT`:

- Snapshot-Writes fielen von 141 auf 32 je Snapshot-Art.
- `write_visualization_snapshot_bundle.total` fiel von ca. 1.824 ms auf ca. 259 ms.
- `attempt_records.jsonl` fiel von 2,136 MB auf 1,975 MB.
- `mcm_file_write_profile.csv` fiel von 0,146 MB auf 0,108 MB.
- `primary_field_step` blieb pro Schritt nahezu gleich bei ca. 101-102 ms.

NÃ¤chster sinnvoller Anschluss:

- Nicht weiter zuerst an Debug schreiben optimieren.
- Jetzt `primary_field_step` untersuchen:
  - Agentenanzahl
  - lokale Nachbarschaften
  - Insel-/Topologie-Ableitung
  - Snapshot-Feldableitung
  - MÃ¶glichkeit, teure Feldmetriken nur jeden n-ten Tick voll zu berechnen und dazwischen fortzuschreiben.

Erster Schritt umgesetzt:

- `MCMField.step()` besitzt nun Detailprofile fÃ¼r Sync, Neighbor-Map, Neuron-Loop, Diffusion, Areal-State, Field-Perception und Total.
- Lokale Nachbarschaften werden als Arrays vorgehalten.
- Kopplung kann vektorisiert aus Neighbor-State-Arrays berechnet werden.
- Ein redundanter zweiter Sync/Refresh nach dem Feldstep wurde entfernt.

NÃ¤chster sinnvoller Anschluss:

- `test_5m_SOLUSDT` ohne Memory erneut laufen lassen.
- Danach `mcm_profile.csv` nach `mcm_field.step.*` auswerten.
- Wenn `neuron_loop` dominiert: Kopplung/Neuron-Step weiter vektorisieren.
- Wenn `refresh_areal_state` oder `field_perception_state` dominiert: schwere Areal-/Inselmetriken nur jeden n-ten Tick voll berechnen und dazwischen fortschreiben.

Auswertung nach dem ersten Feldprofil-Lauf:

- `primary_field_step` sank leicht von ca. 101,50 ms auf ca. 98,51 ms je Profilpunkt.
- Dominanter Innenblock ist `mcm_field.step.neuron_loop`.
- Danach folgen `refresh_areal_state` und `activity_diffusion`.
- `field_perception_state` ist nicht der Hauptengpass.

Zweiter Feld-Performance-Schritt umgesetzt:

- Kontext-Memory-Vektor wird pro Feldstep nur noch einmal gebaut.
- `MCM_NEURON_STEP_RETURN_SNAPSHOT=False` verhindert ungenutzte Snapshots aus jedem einzelnen `MCMNeuron.step()`.
- `MCMField.step()` liefert weiterhin den zentralen Snapshot.
- Micro-Benchmark mit 230 Agenten: ca. 98 ms Mittelwert.

NÃ¤chster sinnvoller Anschluss:

- `test_5m_SOLUSDT` ohne Memory erneut laufen lassen.
- Danach prÃ¼fen, ob `mcm_field.step.neuron_loop` im echten Lauf sinkt.
- Wenn ja: nÃ¤chster Hebel `activity_diffusion` und/oder `refresh_areal_state` nur jeden n-ten Tick voll berechnen.

Auswertung des folgenden Debuglaufs:

- Der aktuelle Lauf lag in `debug`, der alte Stand in `debug/lauf_3_mit_test_5m_SOLUSDT_ohne_memory`.
- `lauf_3` enthÃ¤lt nur wenige Profilzeilen, daher bleibt `lauf_2` die letzte vollstÃ¤ndige Performance-Basis.
- Gegen diese Basis fiel `primary_field_step` von ca. 101,50 ms auf ca. 85,46 ms je Profilpunkt.
- Aktuell dominieren:
  - `mcm_field.step.neuron_loop`
  - `mcm_field.step.refresh_areal_state`
  - `mcm_field.step.activity_diffusion`

Dritter Feld-Performance-Schritt umgesetzt:

- `MCM_FIELD_AREAL_REFRESH_EVERY_N=2` eingefÃ¼hrt.
- Areal-/Topologie-Metriken werden nur jeden zweiten Feldtick voll berechnet.
- Ãœbersprungene Ticks tragen den letzten Areal-State mit `areal_refresh_skipped=True`.
- `field_perception_state` wird weiterhin jeden Feldstep aktualisiert.
- Micro-Benchmark mit 230 Agenten: ca. 89,6 ms Mittelwert.

NÃ¤chster sinnvoller Anschluss:

- `test_5m_SOLUSDT` ohne Memory erneut laufen lassen.
- Danach prÃ¼fen:
  - sinkt `mcm_field.step.refresh_areal_state` erwartungsgemaess?
  - bleibt Feldentscheidung stabil?
  - dominiert danach `activity_diffusion` oder weiter `neuron_loop`?

Auswertung neuer Lauf gegen `lauf_4` und Profilbasis:

- `debug/lauf_4_mit_test_5m_SOLUSDT_ohne_memory` ist als Ergebnisvergleich brauchbar, enthÃ¤lt aber fast keine Profilzeilen.
- FÃ¼r Performance bleibt `lauf_2` die letzte vollstÃ¤ndige Profilbasis.
- Neuer Lauf:
  - `primary_field_step`: ca. 74,59 ms statt ca. 101,50 ms in der Basis
  - `step_mcm_brain.total`: ca. 103,39 ms statt ca. 124,98 ms
  - `compute_runtime_result.total`: ca. 36,79 ms statt ca. 50,94 ms
  - MCM-Phasen: `hold` 1480, `act` 157, `observe` 12
- Die Areal-DÃ¤mpfung wirkt damit in der echten Replay-Logik, ohne die Feldentscheidung sichtbar zu destabilisieren.

Vierter Performance-Schritt geprÃ¼ft und korrigiert:

- Erster Ansatz: primaeren Snapshot aus `MCMField.step()` direkt in `step_mcm_brain` weiterverwenden.
- Messung `lauf_5` gegen neuen `debug`-Lauf:
  - `snapshot_field_read`: ca. 17,92 ms auf ca. 8,51 ms
  - `step_mcm_brain.total`: ca. 103,39 ms auf ca. 87,91 ms
  - MCM-Phasen blieben grundsaetzlich stabil, aber die Handelslage verschob sich zu stark.
- Bewertung: Der Snapshot war fachlich zu frÃ¼h im Brain-Tick, weil danach noch Regulation/Feldanpassung erfolgt.
- Korrektur umgesetzt:
  - `MCMField.step(..., return_snapshot=False)` eingefÃ¼hrt.
  - Primaerer Feldstep in `step_mcm_brain` baut keinen ungenutzten Snapshot mehr.
  - Der finale Snapshot nach Regulation bleibt erhalten.

NÃ¤chster sinnvoller Anschluss:

- Gleichen Backtest ohne Memory erneut laufen lassen.
- Danach kontrollieren:
  - Ergebnis-/Phasenlage gegen `lauf_5`
  - `primary_field_step`, weil dort der ungenutzte frÃ¼he Snapshot wegfallen sollte
  - `snapshot_field_read`, der als finaler Wahrnehmungsread bewusst erhalten bleibt
- Wenn das stabil ist, als nÃ¤chstes `mcm_field.step.neuron_loop` weiter vektorisieren.

Korrektur bestÃ¤tigt mit neuem Lauf:

- Alter Lauf: `debug/lauf_6_mit_test_5m_SOLUSDT_ohne_memory`.
- Neuer Lauf: `debug`.
- Ergebnis:
  - `lauf_6`: 119 Trades, Equity ca. 85,46
  - neuer Lauf: 111 Trades, Equity ca. 89,39
  - Phasen neuer Lauf: `hold` 1417, `act` 161, `observe` 16
- Performance:
  - `primary_field_step`: ca. 75,63 ms auf ca. 68,28 ms
  - `step_mcm_brain.total`: ca. 87,91 ms auf ca. 90,73 ms
  - `compute_runtime_result.total`: ca. 30,44 ms auf ca. 30,03 ms
  - `snapshot_field_read`: wieder ca. 18,12 ms, weil finaler Snapshot bewusst erhalten bleibt
- Bewertung:
  - fachliche Korrektur erfolgreich
  - frÃ¼her ungenutzter Snapshot entfernt
  - finale MCM-Feldwahrnehmung bleibt erhalten

NÃ¤chster sinnvoller Anschluss:

- `mcm_field.step.neuron_loop` weiter entlasten.
- Fokus:
  - lokale Kontextimpulse pro Neuron vorvektorisieren
  - Python-Objektzugriffe im Loop reduzieren
  - Kopplungsvorbereitung weiter in Arrays halten
- Danach gleicher Backtest ohne Memory als StabilitÃ¤tsvergleich.

Neuron-Loop-Entlastung umgesetzt:

- `_build_local_context_memory_matrix(...)` eingefÃ¼hrt.
- Lokale Kontextimpulse werden nun pro Feldstep als Matrix vorbereitet.
- Die alte Einzel-Neuron-Formel bleibt erhalten:
  - lokale AktivitÃ¤t
  - lokaler Memory-Trace
  - Aktivierung
  - Regulationsdruck
  - Resonanz-Clamp von 0,12 bis 1,0
- Externe und Replay-Impulsvektoren werden ebenfalls einmal pro Feldstep vorbereitet.
- `MCMNeuron.step(...)` akzeptiert vorbereitete Vektoren und bleibt mit der bisherigen Schnittstelle kompatibel.
- Neue Profilpunkte:
  - `mcm_field.step.context_memory_matrix`
  - `mcm_field.step.prepare_impulse_vectors`

Verifikation:

- `py_compile` erfolgreich.
- Matrix gegen alte Einzelberechnung: `max_delta = 0.0`.
- Lokaler 230-Agenten-Smoke: ca. 64,7 ms Mittelwert fÃ¼r Feldstep ohne Snapshot.

NÃ¤chster sinnvoller Anschluss:

- Gleichen Backtest ohne Memory laufen lassen.
- Danach kontrollieren:
  - sinkt `mcm_field.step.neuron_loop`?
  - bleiben `hold`, `act`, `observe` stabil?
  - wie groÃŸ sind die neuen Matrix-/Prepare-Profilpunkte?
- Wenn stabil: Kopplungsberechnung/Neighbor-Forces weiter vektorisieren.

Neuer Fixpunkt nach dem Ohne-Memory-Test:

- Denkstruktur-Komplexitaet mit Memory sichtbar machen.
- Ziel ist nicht, Memory hart zu beschneiden.
- Ziel ist eine energieeffiziente Meta-Regulation der Entscheidung:
  - wie komplex ist die aktuelle Denkstruktur?
  - wie viel Memory-Vergleich findet statt?
  - wie stark hemmt, stuetzt oder widerspricht Memory?
  - wie viel kognitive Last entsteht daraus?
  - fÃ¼hrt die Last zu weniger `act`, mehr `hold` oder mehr `observe`?
- Diagnosefelder fÃ¼r spÃ¤teres Protokoll:
  - `thinking_complexity`
  - `memory_compare_load`
  - `memory_match_count`
  - `memory_support`
  - `memory_inhibition`
  - `memory_conflict`
  - `cognitive_load`
  - `decision_energy_cost`
  - `meta_regulation_need`
- Fachliche Idee:
  - stabile Erfahrung soll Entscheidungen effizienter und tragfÃ¤higer machen
  - widerspruechliche oder duenne Erfahrung soll nicht chaotisch bremsen, sondern Meta-Regulation auslÃ¶sen
  - weniger Trades mit Memory ist nur dann gut, wenn schlechte Trades selektiv reduziert werden
- Reihenfolge:
  - zuerst aktueller Ohne-Memory-Test fÃ¼r Brain/MCM-Feld abschliessen
  - danach identischer Lauf mit Memory
  - dann Komplexitaets-/Meta-Regulations-Protokoll umsetzen

ErgÃ¤nzung fÃ¼r die spÃ¤tere Umsetzung:

- Reflexion und innere Wahrnehmung mÃ¼ssen als eigene gekoppelte Ebene sichtbar werden.
- Das System hat nicht nur AuÃŸenwahrnehmung, sondern auch eine Innenwahrnehmung der eigenen TragfÃ¤higkeit.
- ZusammenhÃ¤ngende Akteure:
  - AuÃŸenwahrnehmung: Reiz, Marktstruktur, Risiko, Timing
  - Innenwahrnehmung: StabilitÃ¤t, Spannung, Ãœberlastung, Klarheit, Mut, Hemmung
  - Denken/Organisieren: Musterdeutung, Teilmuster-ErgÃ¤nzung, Erfahrungsvergleich, Reorganisation, Informationsverdichtung
  - Handlung: `observe`, `hold`, `replan`, kontrolliertes `act`
  - Lernen: ProzessqualitÃ¤t, TragfÃ¤higkeit, StabilitÃ¤t, Varianz, Erfahrungsspuren
- Memory darf nicht nur als Archiv oder Bremse wirken.
- Memory soll Resonanz, Unterstuetzung, Konflikt und Teilmuster-ErgÃ¤nzung sichtbar machen.
- Kognitive Last durch Denken selbst muss gemessen werden, weil zu viel Organisation Handlung unklar oder teuer machen kann.
- SpÃ¤tere Meta-Regulation soll nicht hart regeln, sondern energieeffizient entscheiden:
  - weiterdenken
  - verdichten
  - beobachten
  - halten
  - reorganisieren
  - kontrolliert handeln

Dokumentation ergÃ¤nzt:

- `README.md` enthÃ¤lt jetzt eine kurze Einstiegsklammer zu Reflexion, Denkkomplexitaet und energieeffizienter Meta-Regulation.
- `README.md` verweist bei den Kerndokumenten auf die realen Pfade unter `files/`.
- `docs/01_plan/UMSETZUNGSPLAN.md` enthÃ¤lt jetzt mit Zustimmung den Architekturpunkt `Denkkomplexitaet und energieeffiziente Meta-Regulation`.
- Der offene Folgefix bleibt die konkrete Messung nach dem Ohne-Memory-Test und dem anschliessenden Memory-Vergleich.

Neuer Architektur-/Folgefix: Emergente MusterergÃ¤nzung

- Ziel ist keine reine Pattern-Erkennung.
- Ziel ist Teilmuster-ErgÃ¤nzung unter Unsicherheit.
- Ein Gehirn sieht ein Ereignis selten zu 100 Prozent klar; oft ist nur ein Teilmuster sichtbar.
- Das System soll spÃ¤ter Ã¤hnlich arbeiten:
  - aktuelles Teilmuster erkennen
  - Ã¤hnliche ErfahrungsrÃ¤ume aktivieren
  - mÃ¶gliche Musterfortsetzungen bilden
  - Varianten mit Varianz und Unsicherheit tragen
  - innere TragfÃ¤higkeit und Feldklarheit prÃ¼fen
  - erst dann `observe`, `hold`, `replan` oder kontrolliertes `act` ableiten
- Deutung kann teilweise reif sein; die konkrete Reife ist variabel und darf kein fester Prozentwert sein.
- Wichtig: keine Fantasie-Handlung und keine harte Vorhersage.
- Memory dient dabei als Material fÃ¼r mÃ¶gliche Musterfortsetzungen, nicht nur als Archiv bekannter FÃ¤lle.

SpÃ¤tere Diagnosefelder:

- `partial_pattern_strength`
- `completion_candidates`
- `completion_confidence`
- `completion_variance`
- `experience_resonance`
- `pattern_projection_support`
- `pattern_projection_risk`
- `inner_image_clarity`
- `completion_meta_action`

Reihenfolge:

- zuerst Ohne-Memory-Test nach Neuron-Loop-Optimierung auswerten
- danach Memory-/Denkkomplexitaetsprotokoll
- danach emergente MusterergÃ¤nzung als eigene Diagnose- und SpÃ¤ter-Regulationsschicht vorbereiten

Ohne-Memory-Test nach Neuron-Loop-Optimierung ausgewertet:

- Vergleich: `debug/lauf_7_mit_test_5m_SOLUSDT_ohne_memory` gegen aktuellen `debug`-Lauf.
- Ergebnis:
  - 111 Trades auf 114 Trades
  - 28 TP / 83 SL auf 35 TP / 79 SL
  - Equity ca. 89,39 auf ca. 102,07
  - Attempts 2114 auf 2033
- MCM-Phasen:
  - `observe`: 16 auf 15
  - `act`: 161 auf 163
  - `hold`: 1417 auf 1348
- Performance:
  - `primary_field_step`: ca. 68,28 ms auf ca. 64,11 ms
  - `mcm_field.step.neuron_loop`: ca. 41,60 ms auf ca. 37,17 ms
  - `mcm_field.step.total`: ca. 70,56 ms auf ca. 68,49 ms
  - `compute_runtime_result.total`: ca. 30,03 ms auf ca. 28,17 ms
  - `step_mcm_brain.total`: ca. 90,73 ms auf ca. 88,22 ms
  - `snapshot_field_read`: stabil bei ca. 18,2 ms als finaler Wahrnehmungsread
- Neue Profilpunkte:
  - `context_memory_matrix`: ca. 0,05 ms
  - `prepare_impulse_vectors`: unter Profil-Schwelle, unkritisch
- Bewertung:
  - Neuron-Loop-Entlastung greift.
  - MCM-Phasen bleiben stabil.
  - Die bessere Equity ist positiv, aber noch kein alleiniger QualitÃ¤tsbeweis.

NÃ¤chster sinnvoller Anschluss:

- Entweder:
  - noch eine Feld-Performance-Runde fÃ¼r Kopplung/Neighbor-Forces
- Oder:
  - identischer Lauf mit Memory
  - danach Denkkomplexitaets-/Memory-Protokoll vorbereiten
  - dort messen, ob Memory sinnvoll selektiert oder die Entscheidung nur schwerfÃ¤lliger macht

Memory-Lauf mit vorhandener Erfahrung ausgewertet:

- Hinweis: Der direkte vorherige Ohne-Memory-Lauf wurde nicht separat archiviert.
- Vergleich erfolgt gegen die zuletzt dokumentierte Ohne-Memory-Basis:
  - Ohne Memory: 114 Trades, 35 TP, 79 SL, Equity ca. 102,07
  - Mit vorhandener Memory-Erfahrung: 56 Trades, 17 TP, 39 SL, Equity ca. 99,34
- Attempts:
  - 2033 ohne Memory dokumentiert
  - 2675 mit Memory
- Submitted:
  - 114 ohne Memory dokumentiert
  - 56 mit Memory
- Withheld:
  - 1565 ohne Memory dokumentiert
  - 2501 mit Memory
- MCM-Phasen mit Memory:
  - `hold`: 1841
  - `act`: 74
  - `observe`: 17
- Haupthemmgrund:
  - `context_cluster_negative`: 976
- Weitere Gruende:
  - `maturity_block`: 334
  - `fused_score_too_low`: 286
  - `pause_mode`: 139
  - `stressed_block`: 101
  - `plan_allowed`: 74
- Laufzeitbefund:
  - `primary_field_step` bleibt bei ca. 64 ms und ist nicht das Problem.
  - `compute_runtime_result.total` steigt auf ca. 40,45 ms.
  - Memory wirkt daher vor allem Ã¼ber Entscheidungs-/Denkstruktur, nicht Ã¼ber Feldsimulation.
- Bewertung:
  - Memory reduziert Trades stark.
  - Die Equity bleibt fast Break-even, daher ist Memory nicht einfach kaputt.
  - Aber die Hemmung ist nicht transparent genug.
  - `context_cluster_negative` muss auf Support/Inhibition/Konflikt und Vergleichslast aufgeteilt werden.

Fix umgesetzt: Denkkomplexitaets-/Memory-Wirkungsprotokoll:

- Neues Protokoll `debug/mcm_memory_thinking_protocol.csv` eingebaut.
- Neue Config:
  - `MCM_MEMORY_THINKING_PROTOCOL_DEBUG`
  - `MCM_MEMORY_THINKING_PROTOCOL_EVERY_N`
- Sichtbar sind jetzt:
  - `thinking_complexity`
  - `memory_compare_load`
  - `memory_match_count`
  - `memory_support`
  - `memory_inhibition`
  - `memory_conflict`
  - `cognitive_load`
  - `decision_energy_cost`
  - `context_cluster_negative_source`
  - `memory_effect_on_phase`
- `context_cluster_negative` wird in `cluster_score`, `low_hit_ratio` und `mixed` zerlegt.
- Alle Entscheidungsabbrueche und Trade-Ergebnisse fÃ¼hren den aktuellen `memory_complexity_state` mit.
- SyntaxprÃ¼fung erfolgreich:
  - `python -m py_compile .\MCM_Brain_Modell.py .\config.py`

NÃ¤chster Fix:

- Neuen Memory-Lauf auswerten.
- Danach die Verteilung aus `mcm_memory_thinking_protocol.csv` prÃ¼fen:
  - `hard_inhibit`
  - `inhibit`
  - `support`
  - `conflict`
  - `neutral_match`
  - `no_match`
- Ergebnis der Auswertung:
  - 36 Trades, 9 TP, 27 SL, Equity ca. 94,54
  - `hard_inhibit`: 1514
  - `inhibit`: 444
  - `neutral_match`: 241
  - `no_match`: 53
  - `memory_support`: praktisch 0
  - `memory_conflict`: praktisch 0
  - `context_cluster_negative` bleibt dominanter Hemmgrund
- Fachlicher Befund:
  - Memory ist im aktuellen Zustand zu einseitig hemmend.
  - `low_hit_ratio` darf nicht automatisch harter Block sein, wenn die negative Evidenz hauptsaechlich aus Cancel/Timeout statt echten SL-Verlusten stammt.
  - Das ist naehr an der ProzessqualitÃ¤ts-Idee als an simpler `TP gut / alles andere schlecht`-Logik.

Fix umgesetzt: `low_hit_ratio` prozessqualitativ gedÃ¤mpft:

- Harte `context_cluster_negative`-Blockade bleibt bei stark negativem Cluster-Score erhalten.
- Niedrige Trefferquote blockiert nur noch hart, wenn echter Verlustdruck bestÃ¤tigt ist:
  - ausreichend SL-Evidenz
  - hoher Loss-Anteil
  - negativer Score
- Cancel-/Timeout-lastige Cluster erzeugen kÃ¼nftig eher Vorsicht (`low_hit_caution`) statt harte Blockade.
- Neues Protokollfeld:
  - `context_cluster_loss_ratio`
  - `context_cluster_cancel_timeout_ratio`
  - `context_cluster_negative_evidence`
- RÃ¼ckrechnung auf den letzten Lauf:
  - ca. 155 von 803 bisherigen `low_hit_ratio`-Blocks blieben hart
  - ca. 648 wÃ¼rden nur noch dÃ¤mpfen
- SyntaxprÃ¼fung erfolgreich:
  - `python -m py_compile .\MCM_Brain_Modell.py .\config.py`

NÃ¤chster Fix:

- Neuen Lauf mit bestehendem Memory nach dieser DÃ¤mpfung auswerten.
- PrÃ¼fen:
  - ob `hard_inhibit` deutlich sinkt
  - ob `act` wieder steigt, ohne dass Low-Quality-Trades explodieren
  - ob ehemals Cancel-/Timeout-lastige Cluster eher brauchbare Setups freigeben
  - ob danach zusÃ¤tzlich positiver Memory-Support aufgebaut werden muss

Fix umgesetzt: Zero-Point-Regulation:

- Leitidee: `MCM, finde wieder zu dir selbst`.
- Eingebaut in die Meta-Regulation.
- Neue Werte:
  - `memory_orientation`
  - `orientation_gap`
  - `blind_thinking_load`
  - `zero_point_regulation`
  - `zero_point_hint`
- Das Memory-Thinking-Protokoll schreibt diese Werte mit.
- Wirkung:
  - Bei viel Denk-/Memory-Last ohne Orientierung wird nicht weiter starr gehalten.
  - Die MCM wird in ruhiges `observe` zurÃ¼ckgefÃ¼hrt.
  - Rejection-Grund: `zero_point_regulation`.
- Keine Trade-Freigabe:
  - Der Nullpunkt ist WahrnehmungsrÃ¼ckkehr, nicht Aktion.
  - Ziel ist weniger blindes Aushalten und mehr innere Reorientierung.
- SyntaxprÃ¼fung erfolgreich:
  - `python -m py_compile .\MCM_Brain_Modell.py .\config.py`

NÃ¤chster Fix:

- Neuen Lauf mit bestehendem Memory auswerten.
- PrÃ¼fen:
  - Anzahl `zero_point_regulation`
  - VerÃ¤nderung von `hard_inhibit`
  - VerÃ¤nderung von `observe`
  - ob `memory_orientation` Ã¼berhaupt entsteht
  - ob als nÃ¤chstes positiver Memory-Support/Orientierung aufgebaut werden muss

Dokumentation umgesetzt: MCM als maschinelle Wahrnehmung:

- `README.md` ergÃ¤nzt.
- `docs/01_plan/UMSETZUNGSPLAN.md` mit Zustimmung ergÃ¤nzt.
- Inhalt:
  - Wahrnehmung wird nicht als rein menschliche FÃ¤higkeit verstanden.
  - Wahrnehmung entsteht, wenn ein Reiz im Innenzustand eines Systems Bedeutung bekommt.
  - Die MCM soll aus AuÃŸenreiz, innerem Feld, Memory, Regulation, TragfÃ¤higkeit und Handlungstendenz ein maschinelles Wahrnehmungsfeld bilden.

NÃ¤chster Fix:

- Debug-Lauf mit bestehendem Memory fortsetzen.
- Danach auswerten:
  - `zero_point_regulation`
  - `memory_orientation`
  - `orientation_gap`
  - `blind_thinking_load`
  - VerÃ¤nderung von `hard_inhibit`, `observe`, `act`

Neuer Debug-Lauf nach Low-Hit-DÃ¤mpfung ausgewertet:

- Ergebnis:
  - 65 Trades
  - 16 TP
  - 49 SL
  - Netto-PnL ca. -8,22
  - Equity ca. 91,78
- GegenÃ¼ber Vorlauf:
  - Trades 36 auf 65
  - Netto-PnL ca. -5,46 auf ca. -8,22
  - `hard_inhibit` 1514 auf 1020
  - `inhibit` 444 auf 1133
- Bewertung:
  - Die Low-Hit-DÃ¤mpfung funktioniert mechanisch.
  - Sie hat harte Blockade in weiche DÃ¤mpfung verschoben.
  - Aber die freigegebenen Trades waren qualitativ nicht stabil genug.
- Kritischer Befund:
  - Zone-Trades: 45 Trades, 16 TP, 29 SL, PnL ca. +3,54
  - Non-Zone-Trades: 20 Trades, 0 TP, 20 SL, PnL ca. -11,76
  - Non-Zone ohne tragende Orientierung ist aktuell toxisch.
- Technischer Hinweis:
  - Der Lauf enthÃ¤lt die Low-Hit-DÃ¤mpfungsfelder.
  - Der Lauf enthÃ¤lt noch keine Zero-Point-Spalten.
  - Vermutlich wurde der Backtest-Prozess nicht mit dem neuesten Code/Import neu gestartet.

NÃ¤chster Fix:

- NÃ¤chsten Lauf nach sicherem Neustart mit Zero-Point-Regulation auswerten.
- Falls Non-Zone wieder negativ bleibt:
  - Non-Zone + kein Memory-Support + Low-Hit-Caution soll eher `observe` statt `act` werden.
  - Das darf keine starre Tradingregel sein, sondern eine MCM-Orientierungsfrage:
    - Ist Struktur tragfÃ¤hig?
    - Gibt Memory Support?
    - Gibt das Feld Orientierung?
    - Falls nein: zurÃ¼ck in Wahrnehmung.

Neuer Debug-Lauf mit Zero-Point-Regulation ausgewertet:

- Ergebnis:
  - 51 Trades
  - 10 TP
  - 41 SL
  - Netto-PnL ca. -10,58
  - Equity ca. 89,42
- Zero-Point wirkt mechanisch:
  - `zero_point_regulation` im Memory-Protokoll: 1280
  - `zero_point_regulation` im Feldprotokoll: 1098
  - Observe steigt stark auf Ã¼ber 1100 Feldentscheidungen.
- Bewertung:
  - Die MCM findet aus starrer Blockade in Wahrnehmung zurÃ¼ck.
  - Das Ziel `finde wieder zu dir selbst` funktioniert mechanisch.
  - Oekonomisch reicht es noch nicht, weil die verbliebenen Acts nicht tragfÃ¤hig genug sind.
- Kritischer Befund:
  - Non-Zone: 12 Trades, 0 TP, 12 SL, PnL ca. -7,72
  - Zone: 39 Trades, 10 TP, 29 SL, PnL ca. -2,86
  - Memory-Support bleibt praktisch 0.

Fix umgesetzt: Struktur-Orientierung vor Handlung:

- Neue Meta-Regulationswerte:
  - `structure_quality`
  - `context_confidence`
  - `structure_orientation`
  - `structure_orientation_gap`
  - `structure_orientation_guard`
- Das Memory-Thinking-Protokoll schreibt `structure_quality`, `context_confidence`, `structure_orientation`, `structure_orientation_gap` mit.
- Wirkung:
  - Wenn Struktur, Kontextvertrauen, Memory-Support und Memory-Orientierung fehlen,
    wird `act` zu `observe`.
  - Neuer Grund: `structure_orientation_observe`.
- Ziel:
  - Non-Zone ohne tragende Orientierung nicht handeln.
  - Keine RÃ¼ckkehr zur harten Blockade.
  - Mehr Wahrnehmung, weniger blindes Act.
- SyntaxprÃ¼fung erfolgreich:
  - `python -m py_compile .\MCM_Brain_Modell.py .\config.py`

NÃ¤chster Fix:

- Neuen Lauf nach Prozess-Neustart auswerten.
- PrÃ¼fen:
  - sinken Non-Zone-Trades?
  - erscheint `structure_orientation_observe`?
  - verbessert sich Non-Zone-PnL?
  - bleibt Zone positiv oder braucht die Tradeplan-/ZielqualitÃ¤t als nÃ¤chste Orientierungsebene?

Architektur-Erkenntnis dokumentiert: eigene Sprache / kognitive Kompression:

- `README.md` ergÃ¤nzt:
  - Abschnitt `Eigene Sprache und kognitive Kompression`
- `docs/01_plan/UMSETZUNGSPLAN.md` ergÃ¤nzt:
  - Abschnitt `Eigene Sprache als Feldverdichtung`
  - Abschnitt `Kognitive Kompression`
- Inhalt:
  - Das System soll keine menschlichen Patternlabels als Wahrnehmungskern nutzen.
  - Eigene interne Zeichen sollen aus Feldvarianz, Memory-Resonanz, Spannung,
    TragfÃ¤higkeit und Erfahrung entstehen.
  - Diese Zeichen wirken als komprimierte Information.
  - Tiefe Analyse soll erst bei Relevanz, Abweichung oder HandlungsnÃ¤he starten.
- Fachlicher Nutzen:
  - kognitive Entlastung
  - weniger Memory-Vergleich ohne Orientierung
  - bessere selektive Aufmerksamkeit
  - Grundlage fÃ¼r emergente Musterfindung
  - mehr kreative Varianz im Bedeutungsraum

Fix umgesetzt: diagnostischer Eigenzeichenraum / eigene Form-Sprache:

- Diagnostischer Eigenzeichenraum ist vorbereitet.
- Neue Runtime-/Debug-Felder:
  - `form_symbol_id`
  - `form_symbol_seen`
  - `form_symbol_maturity`
  - `form_symbol_stability`
  - `form_symbol_resonance`
  - `form_symbol_load_reduction`
  - `form_symbol_zoom_need`
  - `form_symbol_split_pressure`
  - `form_symbol_merge_pressure`
  - `form_symbol_bearing`
  - `form_symbol_fragility`
  - `form_symbol_relevance`
  - `form_symbol_novelty`
  - `form_symbol_distance`
- Ziel:
  - eigene maschinelle Sprache als Entlastungs- und Emergenzschicht
  - keine menschliche Marktsprache als Kernlogik
- Neues Protokoll:
  - `debug/mcm_form_symbol_protocol.csv`
- Aktueller Status:
  - diagnostisch aktiv
  - noch kein harter Einfluss auf Entry/Exit
  - Runtime-Ergebnisse, Brain-Snapshot, Tendency-State und Episoden fÃ¼hren `form_symbol_state` mit.
- SyntaxprÃ¼fung erfolgreich:
  - `python -m py_compile .\MCM_Brain_Modell.py .\config.py`

NÃ¤chster Fix-/PrÃ¼fschritt:

- Neuen Backtest-Lauf mit bestehendem Memory starten.
- Danach auswerten:
  - Anzahl verschiedener `form_symbol_id`
  - Wiederholungsrate je Zeichen
  - Reife/StabilitÃ¤t/Resonanz der hÃ¤ufigsten Zeichen
  - `form_symbol_zoom_need` bei Observe/Replan/Act
  - Zusammenhang zwischen `form_symbol_load_reduction` und Memory-/Denk-Last
  - ob instabile Zeichen mit schlechten Non-Zone-Trades zusammenfallen

Debug-Befund: Eigenzeichen zu atomisiert:

- Erster Lauf mit `mcm_form_symbol_protocol.csv`:
  - 2417 Form-Protokollzeilen
  - 2403 unterschiedliche `form_symbol_id`
- Problem:
  - Fast jede Wahrnehmung erzeugt ein neues Zeichen.
  - Dadurch kann keine Reife, Resonanz oder kognitive Entlastung entstehen.
  - Das ist noch Rohwahrnehmung, keine eigene Sprache.

Fix umgesetzt:

- `form_symbol_id` wird nun aus einer groben Form-Familie gebildet.
- Die feine Detailform bleibt als Variante erhalten:
  - `form_symbol_family_key`
  - `form_symbol_variant_key`
- Erwartete Wirkung:
  - weniger Symbol-Atomisierung
  - mehr Wiedererkennung
  - steigende `form_symbol_seen`
  - stabilere `form_symbol_maturity`
  - `form_symbol_resonance` und `form_symbol_load_reduction` kÃ¶nnen wachsen.
- SyntaxprÃ¼fung erfolgreich:
  - `python -m py_compile .\MCM_Brain_Modell.py .\config.py`

NÃ¤chster PrÃ¼fpunkt:

- Neuen Lauf starten und prÃ¼fen:
  - Ziel ist nicht eine feste Symbolzahl.
  - Ziel ist eine sichtbare Wiederholungsstruktur.
  - Top-Form-Familien sollten mehrfach bis oft vorkommen.
  - Wenn weiterhin fast jedes Zeichen einzigartig bleibt, muss die Familienbildung weiter abstrahieren.

Zusatz-Fix umgesetzt: AuflÃ¶sungsabhÃ¤ngige Zeichenbildung:

- Problem aus der Reflexion:
  - Wenn die AuflÃ¶sung niedrig ist, darf das System nicht jeden Abschnitt einzeln benennen.
  - Sonst entsteht keine Denkverdichtung.
- Umsetzung:
  - niedrige AuflÃ¶sung => breites Zeichen `wide_trace`
  - mittlere AuflÃ¶sung => `wide_form`
  - hohe AuflÃ¶sung => `structured_form`
- Neue Felder:
  - `form_symbol_scope`
  - `form_symbol_abstraction_level`
  - `form_symbol_resolution_quality`
  - `form_symbol_detail_pressure`
- Erwartete Wirkung:
  - grobe Wahrnehmung bleibt grob
  - Details werden als Varianten gefÃ¼hrt
  - Fokus/Zoom entsteht erst bei Detaildruck
  - weniger Symbolinflation, mehr kognitive Kompression

Debug-Befund nach Zusatz-Fix:

- Sprachebene funktioniert mechanisch deutlich besser:
  - 2572 Form-Protokollzeilen
  - 268 Form-Familien
  - vorher 2403 fast eindeutige Zeichen
- Wiederholung:
  - Top-Zeichen bis 205 Wiederholungen
  - 30 Zeichen mindestens 20-mal
  - 10 Zeichen mindestens 50-mal
- Reife:
  - `form_symbol_maturity` ca. 0,596
  - `form_symbol_resonance` ca. 0,360
  - `form_symbol_load_reduction` ca. 0,232
- Oekonomik im selben Lauf:
  - 55 Trades
  - 14 TP / 41 SL
  - Netto-PnL ca. -6,46
- Bewertung:
  - Sprachverdichtung ist gelungen.
  - Trading-Ergebnis ist nicht gut.
  - Da die Sprachebene aktuell diagnostisch ist, nicht voreilig als Ursache werten.
  - Erst separate Sprachentwicklung speichern und danach sauber vergleichen.

NÃ¤chster Fix:

- Separaten persistenten Form-Sprach-Memory bauen.
- Nicht in normalen Trade-Memory mischen.
- Geplanter Speicher:
  - `memory/form_symbol_memory.json`
- Inhalt:
  - Form-Familien
  - Scope/AuflÃ¶sung
  - Reife
  - StabilitÃ¤t
  - Resonanz
  - Load-Reduction
  - Varianten
  - Ergebnis-/Erfahrungszaehler spÃ¤ter optional
- Ziel:
  - Sprache wird Entwicklung, nicht nur Laufzustand.

Fix umgesetzt: Sprache als regulatorische Distanz:

- Erkenntnis:
  - Bezeichnung schafft Abstand zum Objekt.
  - Eine Form kann analytisch gehalten werden, ohne das Innenfeld roh zu Ã¼berfluten.
- Neue Werte im Form-Symbol:
  - `form_symbol_object_distance`
  - `form_symbol_containment`
  - `form_symbol_field_decoupling`
- Neue Werte in der Meta-Regulation:
  - `symbolic_object_distance`
  - `symbolic_containment`
  - `symbolic_field_decoupling`
  - `symbolic_regulation`
- Wirkung:
  - leichte DÃ¤mpfung von Feld-Observation/Replan-Druck
  - leichte DÃ¤mpfung von `action_inhibition`
  - leichte DÃ¤mpfung von `orientation_gap`
  - leichte DÃ¤mpfung von `blind_thinking_load`
- Wichtig:
  - bewusst weich und nicht als harte Trade-Regel
  - Ziel ist innere Distanz/Ordnung, nicht mehr Mut um jeden Preis
- NÃ¤chster Debug:
  - prÃ¼fen, ob `symbolic_regulation` die Denk-/Memory-Last senkt
  - prÃ¼fen, ob Zero-Point weniger oft aus Chaos heraus greifen muss
  - prÃ¼fen, ob Trading nicht Ã¼berenthemmt wird

Fix umgesetzt: separater persistenter Form-Sprach-Memory:

- Datei:
  - `bot_memory/form_symbol_memory.json`
- Trennung:
  - nicht im normalen Trade-/State-Memory
  - eigener Entwicklungsraum fÃ¼r Form-Sprache
- Neue Konfig:
  - `MCM_FORM_SYMBOL_MEMORY_ENABLED`
  - `MCM_FORM_SYMBOL_MEMORY_PATH`
  - `MCM_FORM_SYMBOL_MEMORY_SAVE_EVERY_N`
  - `MCM_FORM_SYMBOL_MEMORY_MAX_SYMBOLS`
  - `MCM_FORM_SYMBOL_MEMORY_MAX_VARIANTS`
- Funktionen:
  - Laden beim ersten Form-Symbol-Zugriff
  - Mischen mit laufendem `form_symbol_space`
  - Aktualisieren von Reife/StabilitÃ¤t/Resonanz/Distanz
  - Zaehlen und Begrenzen von Varianten
  - periodisches Speichern
  - finaler Flush beim normalen Bot-Memory-Save
- Debug-Erweiterung:
  - `form_symbol_memory_loaded`
  - `form_symbol_memory_symbol_count`
- Smoke-Test erfolgreich.
- SyntaxprÃ¼fung erfolgreich:
  - `python -m py_compile .\MCM_Brain_Modell.py .\config.py .\bot.py`

NÃ¤chster PrÃ¼fpunkt:

- Backtest laufen lassen.
- Danach kontrollieren:
  - existiert `bot_memory/form_symbol_memory.json`
  - wachsen gespeicherte Form-Familien Ã¼ber LÃ¤ufe
  - sinken `blind_thinking_load` und `orientation_gap`
  - bleibt Trading kontrolliert und wird nicht Ã¼berenthemmt

Debug-Befund: persistenter Form-Sprach-Memory funktioniert:

- Datei existiert:
  - `bot_memory/form_symbol_memory.json`
- Speicherstand:
  - 260 Form-Familien
  - 2571 Gesamtwahrnehmungen / `total_seen`
  - Top-Familie mit 209 Wiederholungen
  - mehrere Top-Familien mit hoher Reife Ã¼ber 0,90
- Debug-Protokoll:
  - `form_symbol_memory_loaded = 1`
  - `form_symbol_memory_symbol_count` steigt im Lauf bis 260
- Lauf-Ergebnis:
  - 55 Trades
  - 17 TP / 38 SL
  - Netto-PnL ca. +0,72
- Last-Befund:
  - `symbolic_regulation` ca. 0,135 im Mittel
  - `blind_thinking_load` niedriger bei hÃ¶herer symbolischer Regulation
  - `orientation_gap` niedriger bei hÃ¶herer symbolischer Regulation
- Performance:
  - Schreibkosten fÃ¼r `form_symbol_memory.json` ca. 0,7 bis 1,8 ms
  - aktuell kein groÃŸer Performance-Blocker
- Bewertung:
  - Speicher-Fix erfolgreich.
  - Erste Hinweise: Sprache wirkt ordnend/regulatorisch.
  - Noch nicht Ã¼berbewerten, ein weiterer Lauf ist noetig.

NÃ¤chster PrÃ¼fpunkt:

- Noch einen Backtest mit bestehendem `form_symbol_memory.json`.
- Danach:
  - Wachstum der Top-Familien prÃ¼fen
  - StabilitÃ¤t von PnL prÃ¼fen
  - Zero-Point-HÃ¤ufigkeit vergleichen
  - ggf. separate Sprach-Reorganisation planen:
    - seltene Zeichen decay
    - instabile Zeichen splitten
    - sehr nahe Familien mergen

Debug-Befund zweiter Persistenzlauf:

- Sprache waechst stark:
  - 303 gespeicherte Form-Familien
  - `total_seen`: 5809
  - Top-Familie: 489 Wiederholungen
  - mittlere `maturity`: ca. 0,792
  - mittlere `load_reduction`: ca. 0,302
- Innere Last sinkt weiter:
  - `blind_thinking_load`: ca. 0,467
  - `orientation_gap`: ca. 0,415
  - `symbolic_regulation`: ca. 0,190
- Trading kippt:
  - 47 Trades
  - 8 TP / 39 SL
  - Netto-PnL ca. -11,66
  - starker LONG-Bias: 46 LONG, 1 SHORT
- Interpretation:
  - Sprache erkennt/ordnet die Lage.
  - Aber Sprache ist noch keine Outcome-Wahrheit.
  - Ein bekanntes Objekt darf das Innenfeld beruhigen,
    aber darf Handlung nicht stark erleichtern.

Fix umgesetzt: symbolische Regulation getrennt:

- Neu:
  - `symbolic_inner_regulation`
  - `symbolic_action_regulation`
- `symbolic_inner_regulation`:
  - darf Denk-/Memory-Last und OrientierungslÃ¼cke dÃ¤mpfen
- `symbolic_action_regulation`:
  - stark gedeckelt
  - nur minimale Wirkung auf `field_action_support` und `action_inhibition`
- Ziel:
  - Sprache wirkt als Ordnung und Distanz
  - keine voreilige Handlungsenthemmung ohne Outcome-Spur
- Debug:
  - `mcm_memory_thinking_protocol.csv` schreibt beide Werte mit.

NÃ¤chster PrÃ¼fpunkt:

- Neuen Lauf starten.
- PrÃ¼fen:
  - PnL nach Sicherheitsfix
  - LONG/SHORT-Verteilung
  - `symbolic_action_regulation` bleibt klein
  - `symbolic_inner_regulation` senkt weiter Last
  - ob als nÃ¤chstes Outcome-Spur im Form-Sprach-Memory noetig ist

---

# Erweiterter Datensatz / Lauf 41

Abgeschlossen:

- [x] Ersten Lauf auf erweitertem SOLUSDT-Datensatz geprÃ¼ft.
  Quelle: `debug/debug_lauf_1`
  Ergebnis:
  - 107 Trades
  - 36 TP / 71 SL
  - Netto-PnL ca. +8,10
  - Equity-Peak ca. 122,61
  - End-Equity ca. 108,10
- [x] Phasenverhalten auf dem lÃ¤ngeren Datensatz ausgewertet.
  Befund:
  - Phase A / vertraute Pull-Strecke:
    - 48 Trades
    - 26 TP / 22 SL
    - PnL ca. +22,61
    - `target_expectation_holds` trÃ¤gt fast den gesamten Aufbau.
  - Phase B / Regimewechsel in lÃ¤ngere Short-Richtung:
    - 33 Trades
    - 2 TP / 31 SL
    - PnL ca. -14,30
    - `expectation_break_observe` dominiert.
    - Das System erkennt Bruch/UntragfÃ¤higkeit, handelt aber noch zu oft in
      diese fremde Semantik hinein.
  - Phase C / seitwÃ¤rtsere Re-Exploration:
    - 26 Trades
    - 8 TP / 18 SL
    - PnL ca. -0,21
    - `target_expectation_holds` wird wieder positiver.
    - Verhalten wird flacher, aber experimentierender.
- [x] Nutzerinterpretation fachlich bestÃ¤tigt.
  Bewertung:
  - Der Lauf wirkt nicht wie ein simpler Systemabsturz.
  - DIO baut auf bekannterer Strecke Kapital auf.
  - Beim neuen MarktgefÃ¼hl entsteht ZurÃ¼ckhaltung und Bruchwahrnehmung.
  - In der spÃ¤teren SeitwÃ¤rtsphase wird wieder vorsichtiger getestet.
  - Die Semantik ist auf neuer Strecke noch nicht ausreichend gelernt, aber die
    Wahrnehmung unterscheidet bereits tragende und brechende Zielerwartung.

NÃ¤chster sinnvoller Fix:

- [x] Semantische Fremdheit / Regimewechsel als eigene DiagnosegrÃ¶ÃŸe einbauen.
  Ziel:
  - erkennen, wann die bekannte Route endet
  - nicht hart blockieren, sondern in Lern-/Beobachtungsmodus wechseln
  - Erfahrung nur proportional zur Transfer-TragfÃ¤higkeit Ã¼bertragen
  - neue Werte umgesetzt:
    - `semantic_shift_pressure`
    - `route_familiarity`
    - `adaptation_phase`
    - `transfer_bearing`
    - `known_form_support`
    - `interpretation_quality`
  Umsetzung:
  - keine menschlichen Pattern-/Chartlabels
  - keine harte mechanische Regel
  - DIO bewertet, ob die eigene Formsprache, Memory-Orientierung und
    Entwicklungserfahrung die aktuelle Lage tragen
  - bei hoher semantischer Fremdheit und niedriger Transfer-TragfÃ¤higkeit
    wird Handlung weich zu `new_market_grammar_observe` oder
    `new_market_grammar_replan`
  - offene Positionen schreiben zusÃ¤tzlich `semantic_transfer_stress`,
    Entry-/Current-Familiarity und Transfer-Deltas
  - SyntaxprÃ¼fung erfolgreich:
    - `python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py`

NÃ¤chster PrÃ¼fpunkt:

- [x] Neuen Lauf auf erweitertem Datensatz starten.
- [x] Lauf 2 nach semantischer Fremdheitsdiagnose geprÃ¼ft.
  Ergebnis:
  - 90 Trades
  - 35 TP / 55 SL
  - Netto-PnL ca. +9,62
  - Profit Factor ca. 1,35
  - Peak ca. 110,21, End ca. 109,62
  - Peak-Giveback nur ca. 0,59
  Bewertung:
  - Lauf 2 ist stabiler als Lauf 1.
  - Weniger Trades und weniger Peak-Aufbau, aber kaum RÃ¼ckgabe der Equity.
  - Die kritische Phase B bleibt nahezu flach statt stark wegzukippen.
  - `new_market_grammar_*` greift noch nicht; die Schicht bleibt Ã¼berwiegend
    diagnostisch in `interpretation_watch`.
  - Keine harte Nachschaerfung, erst Wiederholungslauf.
- [ ] Lauf 3 prÃ¼fen:
  - PnL / Profit Factor
  - Equity-Phasen A/B/C
  - HÃ¤ufigkeit `new_market_grammar_observe` und `new_market_grammar_replan`
  - Mittelwerte `route_familiarity`, `semantic_shift_pressure`,
    `transfer_bearing`, `interpretation_quality`
  - ob Phase B weniger Verlust durch fremde Semantik erzeugt
  - ob Phase A nicht zu stark gehemmt wird
  - ob Phase C kontrollierter re-exploriert

- [x] Lauf 3 geprÃ¼ft.
  Ergebnis:
  - 62 Trades
  - 19 TP / 43 SL
  - Netto-PnL ca. -2,27
  - Profit Factor ca. 0,91
  - Peak ca. 107,98, End ca. 97,73
  Befund:
  - Kein Ãœberhandeln, sondern zu wenig tragender Aufbau plus Verlustserie.
  - Zone bleibt positiv.
  - Non-Zone bleibt der Verlustkanal:
    - Phase A ca. -5,01
    - Phase B ca. -4,61
    - Phase C ca. -2,33
  - `new_market_grammar_*` taucht weiterhin nicht auf.
  - `semantic_shift_pressure` und `transfer_bearing` messen Fremdheit,
    greifen aber noch zu passiv.

NÃ¤chster Fix:

- [x] `transfer_maturity_gap` organisch einbauen.
  Ziel:
  - keine harte Non-Zone-/Low-Regel
  - keine menschliche Chart-Kategorie
  - DIO soll erkennen:
    - Meine eigene Erfahrung trÃ¤gt diese Fremdheit nicht ausreichend.
    - Also beobachte/reorganisiere ich mehr und Ã¼bertrage Erfahrung gedÃ¤mpfter.
  MÃ¶gliche Komponenten:
  - niedrige `transfer_bearing`
  - niedrige `route_familiarity`
  - hohe `structure_action_uncertainty`
  - niedrige `structure_action_bearing`
  - negative Entwicklungsbindung / `learned_development_uncertainty`
  - Bruchwahrnehmung aus `expectation_break_observe`
  Umsetzung:
  - `trust_transfer_base`
  - `trust_transfer_support`
  - `transfer_maturity_gap`
  - `trust_transfer_mode`
  - weiche Gruende:
    - `immature_transfer_observe`
    - `immature_transfer_replan`
  - Debug in `mcm_memory_thinking_protocol.csv` und kompakten Kontexten.
  - SyntaxprÃ¼fung erfolgreich:
    - `python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`

NÃ¤chster PrÃ¼fpunkt:

- [ ] Lauf 4 auf gleichem erweitertem Datensatz prÃ¼fen:
  - PnL / Profit Factor
  - Tradezahl
  - Zone- und Non-Zone-PnL
  - `immature_transfer_observe` / `immature_transfer_replan`
  - Mittelwerte `trust_transfer_support` und `transfer_maturity_gap`
  - ob `transfer_maturity_gap` Verlustphasen sinnvoll markiert

- [x] Lauf 4 geprÃ¼ft.
  Ergebnis:
  - 56 Trades
  - 25 TP / 31 SL
  - Netto-PnL ca. +10,82
  - Profit Factor ca. 1,70
  - Peak und End-Equity ca. 110,82
  - finaler Giveback ca. 0,00
  Befund:
  - DIO hat nach Lauf 3 deutlich stabiler gekaempft.
  - Zone bleibt stark positiv.
  - Non-Zone bleibt negativ, aber der Schaden sinkt, besonders in Phase C.
  - `transfer_maturity_gap` ist im Denkprotokoll deutlich sichtbar.
  - `immature_transfer_watch` erscheint stark als Innenfeldzustand.
  - `immature_transfer_observe` erscheint erst 1x als direkter Grund.
  Bewertung:
  - Die Schnittstelle wirkt organisch und nicht als harter Eingriff.
  - Erst Wiederholungslauf, bevor weiter nachgeschaerft wird.

NÃ¤chster PrÃ¼fpunkt:

- [ ] Lauf 5 auf gleichem Datensatz prÃ¼fen:
  - Reproduzierbarkeit von Lauf 4
  - Non-Zone-Schaden
  - Zone-Freiheit
  - `transfer_maturity_gap` Mittel/Max
  - `trust_transfer_mode`
  - ob `immature_transfer_observe` zu selten sichtbar wird

- [x] Lauf 5 geprÃ¼ft.
  Ergebnis:
  - 73 Trades
  - 27 TP / 46 SL
  - Netto-PnL ca. +6,40
  - Profit Factor ca. 1,28
  - Peak ca. 108,62, End ca. 106,40
  - Giveback ca. 2,22
  Befund:
  - Lauf 5 bleibt profitabel, aber weniger sauber als Lauf 4.
  - Zone bleibt in allen Phasen positiv.
  - Non-Zone bleibt negativ, aber nicht mehr so zerstoererisch wie Lauf 3.
  - Phase C gibt wieder leicht ab.
  - `transfer_maturity_gap` und `immature_transfer_watch` bleiben stark sichtbar.
  - Direkte `immature_transfer_*` Entscheidungsgruende erscheinen nicht.
  - Exit-Replay: 8 Kandidaten, 8 saved, 0 harmed, 0 TP-Cuts.

NÃ¤chster Fix-Kandidat:

- [x] `transfer_break_fatigue` prÃ¼fen/umsetzen.
  Ziel:
  - keine harte Regel
  - keine Non-Zone-Sperre
  - wenn unreifer Trust-Transfer und wiederholte Zielbrueche zusammenkommen,
    soll DIO sichtbarer in Beobachten/Replan wechseln
  - besonders fÃ¼r spÃ¤te Phasen, in denen `expectation_break_observe`
    hÃ¤ufig wird und `target_expectation_holds` nicht mehr sauber trÃ¤gt
  Umsetzung:
  - `transfer_break_fatigue`
  - `transfer_recovery_need`
  - weiche Gruende:
    - `transfer_break_observe`
    - `transfer_break_replan`
  - wirkt auf Beobachtungsbedarf, Replan-Druck, Action-Support,
    Action-Inhibition und Action-Clearance
  - SyntaxprÃ¼fung erfolgreich:
    - `python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`

NÃ¤chster PrÃ¼fpunkt:

- [ ] Lauf 6 auf gleichem Datensatz prÃ¼fen:
  - PnL / Profit Factor / Giveback
  - Tradezahl
  - `transfer_break_fatigue`
  - `transfer_recovery_need`
  - `transfer_break_observe` / `transfer_break_replan`
  - Phase C
  - Zone-Freiheit
  - Non-Zone-Schaden

- [x] Lauf 6 geprÃ¼ft.
  Ergebnis:
  - 51 Trades
  - 17 TP / 34 SL
  - Netto-PnL ca. -0,23
  - Profit Factor ca. 0,99
  - Peak ca. 105,37, End ca. 99,77
  - Giveback ca. 5,60
  Befund:
  - Phase A baut gut auf.
  - Phase B verliert den Aufbau wieder.
  - Phase C bleibt fast neutral.
  - `transfer_break_fatigue` wird gemessen, taucht aber kaum als sichtbare
    Entscheidung auf.
  - Globale DÃ¤mpfung wirkt bereits, aber ohne ausreichende klare
    Observe/Replan-Ãœbersetzung.
  - Non-Zone bleibt in Phase B/C der Verlustkanal.

NÃ¤chster Fix:

- [x] `transfer_break_fatigue` neu balancieren:
  - weniger permanente DÃ¤mpfung auf Action-Clearance/Inhibition
  - sichtbarer, aber seltener Observe/Replan, wenn:
    - unreifer Transfer
    - Zielbruch-/Nachwirkungsdruck
    - fehlende Struktur-TragfÃ¤higkeit
    zusammenkommen
  - Zone-Freiheit erhalten
  - Non-Zone nicht sperren, sondern reifer beobachten lassen
  Umsetzung:
  - globale Fatigue-Wirkung reduziert
  - Wirkung nur noch Ã¼ber `fatigue_excess`
  - neue Werte:
    - `transfer_break_trigger`
    - `transfer_break_ready`
  - sichtbare `transfer_break_*` Entscheidungen hÃ¤ngen jetzt an
    mehreren gleichzeitigen Reife-/TragfÃ¤higkeitsbedingungen
  - SyntaxprÃ¼fung erfolgreich:
    - `python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`

NÃ¤chster PrÃ¼fpunkt:

- [ ] Lauf 7 auf gleichem Datensatz prÃ¼fen:
  - PnL / PF / Giveback
  - Tradezahl gegen Lauf 6
  - `transfer_break_trigger`
  - `transfer_break_ready`
  - `transfer_break_observe` / `transfer_break_replan`
  - Phase B Non-Zone-Schaden
  - Zone-Freiheit

- [x] Lauf 7 geprÃ¼ft.
  Ergebnis:
  - 65 Trades
  - 35 TP / 30 SL
  - Netto-PnL ca. +19,90
  - Profit Factor ca. 2,43
  - Peak ca. 119,90, End ca. 119,90
  - Giveback ca. 0,00
  Befund:
  - Rebalance hat die Dauerbremse gelÃ¶st.
  - Zone trÃ¤gt massiv.
  - Non-Zone-Schaden ist stark reduziert.
  - `transfer_break_trigger` und `transfer_break_ready` sind im Denkprotokoll
    sichtbar, ohne staendig harte Entscheidungen zu erzwingen.
  - Direkte `transfer_break_*` Gruende erscheinen nicht; das war in diesem
    Lauf nicht negativ, weil die tragende Struktur frei genutzt wurde.
  - Exit-Replay: 8 saved, 1 harmed/TP-Cut.

NÃ¤chster PrÃ¼fpunkt:

- [ ] Lauf 8 auf gleichem Datensatz prÃ¼fen:
  - Reproduzierbarkeit Lauf 7
  - Zone-Freiheit
  - Non-Zone-Schaden
  - `transfer_break_trigger`
  - `transfer_break_ready`
  - `immature_transfer_observe`
  - Exit-Replay TP-Cut-Risiko

- [x] Lauf 8 geprÃ¼ft.
  Ergebnis:
  - 77 Trades
  - 34 TP / 43 SL
  - Netto-PnL ca. +7,91
  - Profit Factor ca. 1,30
  - Peak und End-Equity ca. 107,91
  - finaler Giveback ca. 0,00
  Befund:
  - Lauf 8 ist profitabel, aber deutlich variabler als Lauf 7.
  - Phase B fÃ¤llt stark ab, Phase C reorganisiert stark.
  - Zone bleibt tragend.
  - Non-Zone bleibt Verlust-/Stresskanal.
  - `transfer_break_trigger` und `transfer_break_ready` sind messbar,
    aber direkte `transfer_break_*` Gruende erscheinen nicht.
  - Exit-Replay: 11 saved, 0 harmed, 0 TP-Cuts.
  Bewertung:
  - DIO wirkt nicht konstant, sondern wie ein plastisches Nervensystem.
  - Der Lauf zeigt Ãœberlebenskampf plus Reorganisation.

NÃ¤chster Fix-/Analyse-Kandidat:

- [ ] Nervliche Varianz diagnostisch erfassen:
  - `nervous_variance`
  - `regulation_oscillation`
  - `recovery_after_stress`
  - `stress_to_recovery_delta`
  Ziel:
  - nicht Varianz hart entfernen
  - erkennen, ob DIO nach Stress reif reorganisiert oder nur kompensiert
  - Phase-B-Stress und Phase-C-Recovery messbar machen
