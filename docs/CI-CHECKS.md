### Empfohlene CI-Checks (minimal start)

- **Lint**: Basis-Linter abhängig vom Stack (Python: ruff/flake8; Node: eslint).
- **Format**: Black/Prettier im Check-Modus.
- **Tests**: Schnelle Unit-Tests (falls vorhanden) mit Coverage-Snapshot.
- **Security**: Secret-Scan (trufflehog/gitleaks) und dep audit (pip-audit/npm audit --omit=dev).
- **Build**: Falls baubar (Docker/Package), smoke build.

Skalierung später: Caching, Matrix-Builds, CD, Preview-Deploys.