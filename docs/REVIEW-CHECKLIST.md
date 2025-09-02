### Code-Review Checkliste (leichtgewichtig)

- **Problemverständnis**: Deckt der PR das beschriebene Problem/Issue?
- **Architektur/Boundary**: Respektiert der PR bestehende Module/Schichten? Keine heimlichen Couplings.
- **Korrektheit**: Offensichtliche Logikfehler? Edge-Cases bedacht?
- **Tests**: Sinnvolle Unit/Integration-Checks vorhanden oder bewusst begründet.
- **Sicherheit**: Secrets/Token, SQL Injection, gefährliche Deserialisierung vermeiden.
- **Performance**: Offensichtliche Hotpaths, N+1, große Payloads.
- **Lesbarkeit**: Benennungen, kleine Funktionen, keine duplizierte Logik.
- **DX**: Klare README/Changelog/Docs für Nutzer des Codes.
- **CI grün**: Lint/Tests/Build laufen in CI.