### Status-Updates und SLA

Dieser Leitfaden definiert, wie Projektfortschritt transparent gemacht wird, wie schnell reagiert wird (SLA) und wann aktiv alarmiert wird.

## Frequenz
- **Tägliches Kurzupdate (Mo–Fr)**: 3–5 Stichpunkte zu Fortschritt, Nächstes, Risiken/Blocker, Kennzahlen. Ziel: < 5 Minuten Lesezeit.
- **Wöchentlicher Rückblick (Fr)**: Erreichtes, Abweichungen, Risiken mit Trend, Nächste Woche, Metriken.
- **Ad-hoc-Alert**: Bei kritischen Problemen (Rot) sofortige Kurzmeldung mit Handlungsempfehlung.

## Inhalt je Update
- **Was geändert wurde**: Merge/Commits, Tickets, Ergebnisse.
- **Was als Nächstes kommt**: Konkrete nächste Schritte und Eigentümer.
- **Blocker & Risiken**: Status (Grün/Gelb/Rot) mit kurzer Begründung.
- **Metriken**: PR-Durchlaufzeit, offene PRs, Build-Status, Milestone-Fortschritt.

## SLA (Reaktions-/Bearbeitungszeiten)
- **PR-Review**: Erst-Feedback ≤ 24h (Werktage).
- **Build-/CI-Fehler**: Triage ≤ 1h, Fix/Workaround ≤ 24h.
- **Security/Secrets-Vorfälle**: Sofort (≤ 30 Min) mit Maßnahmenplan.
- **Neue Issue/Frage**: Triage/Antwort ≤ 12h.

## Ampellogik
- **Grün**: Planmäßig, keine Maßnahmen nötig.
- **Gelb**: Risiko sichtbar; Gegenmaßnahmen definiert, Termin im Blick.
- **Rot**: Ziel gefährdet; Sofort-Alert und Re-Priorisierung.

## Kanäle
- **Primär**: GitHub Issues/PR-Kommentare, täglicher Status in diesem Cursor-Thread.
- **Optional**: E-Mail/Chat für Alerts (falls vereinbart).

## Service-Zeitfenster
- **Standard**: Werktags 09–18 Uhr (Europa/Berlin). Abweichungen werden vorab kommuniziert.

## Getrackte Kernmetriken (leichtgewichtig)
- **PR-Durchlaufzeit** (Erstellung → Merge)
- **Offene PRs > 2 Tage** (Anzahl)
- **Build-Stabilität** (letzte 10 Runs)
- **Meilenstein-Fortschritt** (% abgeschlossen)
