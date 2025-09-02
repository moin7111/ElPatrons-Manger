# Render Services - Kostenaufstellung

## Monatliche Basiskosten

| Service | Instance Type | Monatliche Kosten |
|---------|--------------|-------------------|
| **blfantasy-postgres** | Basic-256mb | $10.50 |
| **blfantasy-api** | Starter | Inkludiert* |
| **blfantasy-worker** | Starter | Inkludiert* |
| **GESAMT** | | **$10.50** |

*Web Service und Background Worker sind im Gesamtpreis von $10.50 enthalten

## Cron Job Kosten (Pay-per-Use)

| Cron Job | Frequenz | Kosten pro Minute | Geschätzte monatliche Kosten |
|----------|----------|-------------------|------------------------------|
| **daily-ingest** | Täglich (1x) | $0.00016 | ~$0.15** |
| **prematch-pull** | Alle 30 Min (48x täglich) | $0.00016 | ~$7.20*** |

** Annahme: 30 Minuten Laufzeit pro Ausführung
*** Annahme: 5 Minuten Laufzeit pro Ausführung

## Kostenberechnung für Cron Jobs

### Daily Ingest
- Ausführungen pro Monat: 30
- Geschätzte Laufzeit: 30 Minuten
- Berechnung: 30 × 30 × $0.00016 = $0.144

### Prematch Pull
- Ausführungen pro Monat: 1,440 (48 × 30)
- Geschätzte Laufzeit: 5 Minuten
- Berechnung: 1,440 × 5 × $0.00016 = $1.152

## Gesamtkosten-Szenarien

| Szenario | Monatliche Kosten |
|----------|-------------------|
| **Minimum** (ohne Cron Jobs) | $10.50 |
| **Typisch** (mit geschätzten Cron Jobs) | ~$11.80 |
| **Maximum** (intensive Cron Job Nutzung) | Variable |

## Wichtige Hinweise zur Abrechnung

1. **Abrechnungszyklus**: Monatlich, zu Beginn des Monats
2. **Compute-Kosten**: Sekundengenau abgerechnet
3. **Cron Jobs**: Nur tatsächliche Laufzeit wird berechnet
4. **Automatische Synchronisation**: Änderungen an render.yaml werden automatisch übernommen und können Kosten beeinflussen

## Kostenoptimierung Tipps

1. **Cron Job Optimierung**: 
   - Minimieren Sie die Laufzeit der Jobs
   - Überprüfen Sie die Notwendigkeit der Ausführungsfrequenz

2. **Database Sizing**:
   - Basic-256mb ist für kleine bis mittlere Anwendungen geeignet
   - Upgrade nur bei nachgewiesenem Bedarf

3. **Monitoring**:
   - Überwachen Sie regelmäßig die tatsächlichen Kosten im Render Dashboard
   - Setzen Sie Billing-Alerts für unerwartete Kostensteigerungen

## Zusätzliche potenzielle Kosten

- **Bandbreite**: Bei hohem Traffic können zusätzliche Kosten entstehen
- **Speicher**: Bei Überschreitung der inkludierten Limits
- **Custom Domains**: SSL-Zertifikate sind kostenlos inkludiert
- **Team Members**: Zusätzliche Team-Mitglieder können Kosten verursachen