# BLFantasy - Render Deployment Konfiguration

## 📁 Projektstruktur

Dieses Repository enthält alle wichtigen Informationen und Konfigurationsdateien für das BLFantasy-Projekt (ElPatrons-Manger) auf der Render-Plattform.

## 📄 Verfügbare Dateien

| Datei | Beschreibung |
|-------|--------------|
| **[render-config-overview.md](./render-config-overview.md)** | Übersicht aller konfigurierten Services und deren Spezifikationen |
| **[render-services.json](./render-services.json)** | Detaillierte JSON-Struktur mit allen Service-Definitionen |
| **[render-costs.md](./render-costs.md)** | Vollständige Kostenaufstellung und Optimierungstipps |
| **[render.yaml](./render.yaml)** | Produktionsreife render.yaml Konfigurationsdatei |
| **[deployment-notes.md](./deployment-notes.md)** | Wichtige Hinweise, Checklisten und Best Practices |

## 🚀 Quick Start

1. **Konfiguration reviewen**: Beginnen Sie mit `render-config-overview.md`
2. **Kosten verstehen**: Lesen Sie `render-costs.md` für die Kostenplanung
3. **Deployment vorbereiten**: Folgen Sie der Checkliste in `deployment-notes.md`
4. **render.yaml anpassen**: Nutzen Sie die Vorlage und passen Sie sie an Ihre Bedürfnisse an

## 💰 Kostenzusammenfassung

- **Monatliche Basiskosten**: $10.50
- **Zusätzliche Kosten**: Cron Jobs ($0.00016/Minute bei Ausführung)
- **Geschätzte Gesamtkosten**: ~$11.80/Monat

## ⚠️ Wichtige Sicherheitshinweise

1. **API Key Rotation**: Der in der Konfiguration sichtbare API Key sollte rotiert werden
2. **Secrets Management**: Verwenden Sie Render's Environment Groups für sensitive Daten
3. **Auto-Sync**: Beachten Sie, dass Änderungen an render.yaml automatisch deployed werden

## 🔗 Services

- **Database**: blfantasy-postgres (PostgreSQL, Basic-256mb)
- **API**: blfantasy-api (Web Service)
- **Worker**: blfantasy-worker (Background Worker)
- **Cron Jobs**: 
  - daily-ingest (täglich)
  - prematch-pull (alle 30 Minuten)

## 📚 Weitere Ressourcen

- [Render Dokumentation](https://render.com/docs)
- [Render Pricing](https://render.com/pricing)
- [Repository: moin7111/ElPatrons-Manger](https://github.com/moin7111/ElPatrons-Manger)

## 📝 Lizenz

Diese Konfigurationsdateien sind für das BLFantasy-Projekt erstellt und sollten entsprechend den Projektanforderungen angepasst werden.