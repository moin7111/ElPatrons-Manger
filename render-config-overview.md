# Render.yaml Konfiguration - Übersicht

## Projekt: BLFantasy (ElPatrons-Manger)
**Repository:** moin7111/ElPatrons-Manger  
**Datum:** 2024

## Konfigurierte Services

### 1. PostgreSQL Datenbank
- **Name:** `blfantasy-postgres`
- **Instance Type:** Basic-256mb
- **Monatliche Kosten:** $10.50

### 2. Web Service (API)
- **Name:** `blfantasy-api`
- **Instance Type:** Starter (impliziert)
- **Umgebungsvariablen:**
  - `API_KEY`: [in Render Secret gesetzt]
- **Monatliche Kosten:** Im Gesamtpreis enthalten

### 3. Background Worker
- **Name:** `blfantasy-worker`
- **Instance Type:** Starter (impliziert)
- **Monatliche Kosten:** Im Gesamtpreis enthalten

### 4. Cron Jobs
#### a) Daily Ingest
- **Name:** `daily-ingest`
- **Instance Type:** Starter
- **Kosten:** $0.00016 / Minute

#### b) Prematch Pull
- **Name:** `prematch-pull`
- **Instance Type:** Starter
- **Kosten:** $0.00016 / Minute

## Gesamtkosten
- **Basis Services (3):** $10.50 / Monat
- **Cron Jobs:** Nutzungsabhängig (nicht in Basiskosten enthalten)

## Wichtige Hinweise
- ⚠️ Alle zukünftigen Updates zur render.yaml werden automatisch synchronisiert
- ⚠️ Änderungen können Ihre Kosten beeinflussen
- 💡 Compute-Kosten werden sekundengenau abgerechnet
- 💡 Abrechnung erfolgt zu Beginn des Monats