# Interview Trainer

Application web d'entraînement aux entretiens techniques **Angular** : QCM, exercices de code avec aperçu interactif, et exercices d'algorithmique en TypeScript au format entretien. Tout tourne dans le navigateur, sans backend.

Construit avec Angular 22 (composants standalone, signaux, `OnPush`), Tailwind 4 et Vitest.

---

## Fonctionnalités

| Section | Contenu |
|---------|---------|
| **QCM** (`/quiz`) | 203 questions : Angular, TypeScript, RxJS, CSS. Mode **entraînement** (correction immédiate, retour arrière possible) ou **examen** chronométré. Choix unique ou multiple, explications, révision des erreurs. |
| **Exercices Angular** (`/exercises`) | 15 exercices : pipe, composant, directive, service, formulaire réactif, intercepteur HTTP, RxJS. Tu écris du vrai code Angular, vois un **aperçu interactif** (mis à jour 2 s après ta dernière frappe), puis lances les tests. |
| **Algo TypeScript** (`/algo`) | 11 exercices de 20 à 35 minutes (Two Sum, LRU, BFS, fenêtre glissante…), avec **chronomètre** d'entretien. Les tests incluent de grosses entrées : une solution trop lente échoue après 5 s. |
| **Progression** (`/progress`) | Scores par catégorie, historique, questions à retravailler, exercices résolus. Stockée dans le `localStorage`. |

Dans l'éditeur d'exercice : erreurs de compilation avec ligne et colonne, console (`console.log` du code et de l'aperçu), indices progressifs, solution masquée, code sauvegardé automatiquement. `Tab` indente ; `Échap` puis `Tab` quitte l'éditeur au clavier.

---

## Démarrage

**Prérequis** : Node.js **≥ 22.22 ou ≥ 24.15** (exigé par la CLI Angular 22). Avec [Volta](https://volta.sh) : `volta install node@24`.

```bash
npm install          # si npm signale un conflit de peer dependencies : npm install --legacy-peer-deps
npm run dev          # http://localhost:4200
```

| Commande | Rôle |
|----------|------|
| `npm run dev` | Serveur de développement |
| `npm run build` | Build de production (`dist/`) |
| `npm test` | Tests unitaires (Vitest). Une seule passe : `npx ng test --no-watch` |
| `npm run lint` | ESLint, dont les règles d'architecture |

> Le serveur de développement ne relit pas `angular.json` à chaud : redémarre-le si tu modifies ce fichier.

---

## Architecture

Architecture en couches descendantes, détaillée dans [.claude/rules/frontend-guidelines.md](.claude/rules/frontend-guidelines.md) et contrôlée par [eslint.config.mjs](eslint.config.mjs) :

```
pages/  ──→  features/  ──→  shared/  ──→  core/
```

```
src/app/
├── core/storage/                  → wrapper localStorage
├── shared/question/               → modèles Question, catégories, difficultés
├── features/
│   ├── quiz/                      → gateway / mapper / service / store + carte de question
│   ├── progress/                  → progression (sessions, erreurs, exercices résolus)
│   └── exercises/                 → exercices, éditeur, résultats, console, chrono
│       └── features/
│           ├── runner-angular/    → moteur des exercices Angular (voir plus bas)
│           └── runner-algo/       → moteur des exercices d'algo (Web Workers)
├── pages/                         → home, quiz-*, exercises-list, exercise-detail, progress, credits
└── components/header/
```

Chaque feature suit `gateway → mapper → service → store` : seul le gateway fait des appels HTTP, les données (JSON) sont servies depuis `public/data/`. Chaque fichier exécutable a son `.spec.ts`.

### Les deux moteurs d'exécution

Le code de l'utilisateur est du **TypeScript**, transpilé dans le navigateur avec `typescript.js` (≈ 9 Mo, copié dans `vendor/` au build et chargé à la demande).

- **`RunnerAngularService`** (exercices Angular) : transpile, puis laisse le **compilateur JIT d'Angular** compiler les composants. Un `require` maison donne accès à `@angular/core`, `common`, `forms`, `common/http`, `rxjs`. Un harnais de test (`render`, `click`, `type`…) rend les composants dans l'aperçu et les teste sur le DOM. Les `input()`, `output()` et `model()` sont supportés grâce à un pré-traitement qui ajoute les décorateurs que le compilateur AOT ajoute normalement.
- **`RunnerAlgoService`** (algo) : un **Web Worker par test**, exécutés en parallèle et interrompus après 5 s (boucle infinie ou complexité trop élevée). La durée de chaque test est affichée.

Limites : pas de vérification de types (seules les erreurs de syntaxe sont remontées) ; le code des exercices Angular tourne dans le thread principal, donc une boucle infinie y gèle l'onglet.

---

## Contenu et données

Les données sont des fichiers JSON dans [public/data/](public/data/), **générés** par les scripts de [scripts/](scripts/) (Python 3) : ne modifie pas les JSON à la main.

| Fichier | Source |
|---------|--------|
| `qcm-angular.json`, `qcm-typescript.json`, `qcm-rxjs.json` | [build_qcm_angular.py](scripts/build_qcm_angular.py), [build_qcm_other.py](scripts/build_qcm_other.py) |
| `qcm-css.json` | questions originales + 122 questions importées de freeCodeCamp |
| `exercises.json` | [build_exercises.py](scripts/build_exercises.py) (Angular) et [algo_exercises.py](scripts/algo_exercises.py) (algo) |

Les options des QCM sont équilibrées (longueur et position de la bonne réponse) par [qcm_options.py](scripts/qcm_options.py) et [qcm_options_patch.py](scripts/qcm_options_patch.py), puis mélangées à chaque partie.

**Régénérer les données** (dans cet ordre, depuis la racine) :

```bash
python3 scripts/build_qcm_angular.py
python3 scripts/build_qcm_other.py
python3 scripts/import_fcc_css.py <chemin/vers/css-quiz.ts>   # fichier freeCodeCamp, voir ci-dessous
python3 scripts/build_exercises.py
```

`build_qcm_other.py` repart des questions originales : il faut donc relancer `import_fcc_css.py` après lui. Le fichier source se récupère avec :

```bash
gh api repos/freeCodeCamp/developer_quiz_site/contents/src/data/css-quiz.ts --jq .content | base64 -d > css-quiz.ts
```

Les tests valident les données : chaque solution d'exercice doit passer tous ses tests, chaque code de départ doit échouer, et chaque QCM doit être bien formé.

**Ajouter un exercice** : ajoute un appel `ex(...)` dans `build_exercises.py` (ou `algo(...)` dans `algo_exercises.py`) avec sa consigne, son code de départ, ses tests, ses indices et sa solution, puis relance `build_exercises.py` et `npm test`.

---

## Licences et crédits

- Les 122 questions CSS importées viennent de [freeCodeCamp/developer_quiz_site](https://github.com/freeCodeCamp/developer_quiz_site), licence **BSD 3-Clause** (© 2023 freeCodeCamp). L'attribution figure dans la page *Crédits* de l'application et dans les champs `source` / `license` des données.
- Le reste du contenu (questions et exercices) est original.
- `typescript.js` est distribué sous licence Apache 2.0 par Microsoft.

---

## Harnais Claude Code

Le dépôt est configuré pour travailler avec [Claude Code](https://claude.com/claude-code) :

| Mécanisme | Fichier / dossier | Rôle |
|-----------|-------------------|------|
| Instructions permanentes | [CLAUDE.md](CLAUDE.md) → [frontend-guidelines.md](.claude/rules/frontend-guidelines.md) | Règles d'architecture, conventions Angular, tests, UX et accessibilité |
| Skills | [.claude/skills/](.claude/skills/) (liens vers `.agents/skills/`) | `angular-new-app`, `angular-developer` |
| MCP | [.mcp.json](.mcp.json) | Outils Angular CLI (`@angular/cli mcp`), à approuver au premier lancement |

Pour la personnalisation (ajouter une règle, un skill ou un MCP), voir [.claude/README.md](.claude/README.md). Les préférences locales (`.claude/settings.local.json`) ne sont pas versionnées.

### Garde-fous ESLint

[eslint.config.mjs](eslint.config.mjs) mécanise les frontières d'architecture :

- `core/` ne peut pas importer `shared/` ni `features/` ;
- `shared/` ne peut pas importer `features/` ;
- une feature ne peut importer que ses propres **ancêtres et descendants** (à chaque niveau d'imbrication). Les features sont découvertes automatiquement dans `src/app/features/`.

Limites connues : les imports relatifs (`../../features/x`) contournent la règle, qui ne vérifie que les alias `@features/*` ; utilise toujours les alias. Une page peut aussi importer un fichier interne d'une feature au lieu de passer par sa façade `index.ts`.

---

## Ressources

- [Angular](https://angular.dev)
- [Documentation Claude Code](https://docs.claude.com/claude-code)
