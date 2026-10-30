# Claude Setup

## rules/

- [frontend-guidelines.md](rules/frontend-guidelines.md) → règles de développement (architecture, mobile, UX/UI, a11y)

## skills/

Templates de prompts à invoquer manuellement (`@.claude/skills/<nom>.md` ou « utilise le skill <nom> sur … »).

### Génération
- [generate-component.md](skills/generate-component.md) → nouveau composant Angular conforme architecture
- [generate-feature.md](skills/generate-feature.md) → nouvelle feature complète (gateway / mapper / service / store / façade index.ts)
- [generate-unit-tests.md](skills/generate-unit-tests.md) → tests Vitest pour un fichier existant

### Review
- [review-architecture.md](skills/review-architecture.md) → audit isolation des domains, séparation des couches
- [review-accessibility.md](skills/review-accessibility.md) → audit RGAA 4.1
- [review-ui-conventions.md](skills/review-ui-conventions.md) → audit couleurs / PrimeNG / Tailwind / UX patterns
- [review-mobile-capacitor.md](skills/review-mobile-capacitor.md) → audit conformité Capacitor (APIs natives, safe areas, perf)
- [review-angular-units-test.md](skills/review-angular-units-test.md) → audit qualité de tests existants
