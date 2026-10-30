# template-angular-claude

Template de démarrage pour projets Angular, pré-configuré pour travailler avec [Claude Code](https://claude.com/claude-code).

Le template fournit un harnais Claude Code complet : règles d'architecture frontend, skills Angular officiels, et MCP Angular CLI — afin que Claude génère du code conforme aux standards dès la première interaction.

---

## Démarrage rapide

```bash
# 1. Cloner le template
git clone <url> mon-projet
cd mon-projet

# 2. Initialiser l'app Angular dans le template
#    (Claude peut le faire pour toi : invoque le skill angular-new-app)

# 3. Lancer Claude Code à la racine
claude
```

Au premier lancement, Claude Code demande l'**approbation du serveur MCP `angular-cli`** déclaré dans [.mcp.json](.mcp.json). Accepte pour activer les outils Angular CLI.

---

## Structure du template

```
.
├── CLAUDE.md                      → instructions chargées en permanence (importe les règles)
├── .mcp.json                      → serveurs MCP du projet (Angular CLI)
├── .claude/
│   ├── README.md                  → détails de la config Claude
│   ├── rules/
│   │   └── frontend-guidelines.md → standards Angular (architecture, mobile, UX/UI, a11y)
│   ├── skills/                    → symlinks vers .agents/skills/
│   └── settings.local.json        → settings locaux (non versionnés)
├── .agents/
│   └── skills/                    → skills Angular officiels installés
│       ├── angular-developer/     → guidance architecture & code Angular
│       └── angular-new-app/       → création d'une nouvelle app Angular
└── skills-lock.json               → version lock des skills (intégrité)
```

---

## Comment Claude utilise ce template

| Mécanisme | Fichier / dossier | Rôle |
|-----------|-------------------|------|
| **Instructions permanentes** | [CLAUDE.md](CLAUDE.md) → [frontend-guidelines.md](.claude/rules/frontend-guidelines.md) | Règles toujours actives dans le contexte |
| **Skills** | [.claude/skills/](.claude/skills/) | Procédures invoquées à la demande (ex: nouvelle app, nouveau composant) |
| **MCP** | [.mcp.json](.mcp.json) | Outils Angular CLI exposés à Claude (build, generate, etc.) |

### Règles frontend

Le fichier [.claude/rules/frontend-guidelines.md](.claude/rules/frontend-guidelines.md) définit :

- **Architecture** par domaines métier isolés (`domains/`, `pages/`, `shared/`, `layout/`)
- **Mobile (Capacitor)** : safe areas, plugins natifs, contraintes de performance
- **UX / UI** : palette de couleurs, conventions PrimeNG, responsive Tailwind
- **Accessibilité** : RGAA, ARIA, navigation clavier

Ces règles sont chargées automatiquement au démarrage de Claude Code via l'import dans `CLAUDE.md`.

### Skills disponibles

- **[angular-new-app](.agents/skills/angular-new-app/)** — créer une nouvelle app Angular avec les bonnes pratiques
- **[angular-developer](.agents/skills/angular-developer/)** — guidance pour signals, formulaires, DI, routing, SSR, tests, etc.

Pour les invoquer : demande simplement à Claude (« crée une nouvelle app », « génère un composant ») — il chargera le skill pertinent automatiquement.

### MCP Angular CLI

Le MCP [`@angular/cli mcp`](https://angular.dev) expose les commandes Angular CLI à Claude. Une fois approuvé, les outils apparaissent avec le préfixe `mcp__angular-cli__…`.

---

## Linter (ESLint)

Le fichier [eslint.config.mjs](eslint.config.mjs) à la racine **mécanise les frontières d'architecture** définies dans [frontend-guidelines.md](.claude/rules/frontend-guidelines.md) :

- `core/` ne peut pas importer `shared/` ni `features/`
- `shared/` ne peut pas importer `features/`
- Une feature ne peut importer que ses propres **ancêtres et descendants** (récursif via sous-features)

Les features sont **auto-découvertes** en scannant `src/app/features/` récursivement — pas de liste à maintenir.

### Sous-features (récursif)

Une feature peut nidifier ses propres sous-features dans son dossier `features/` :

```
features/orders/
├── features/
│   ├── cart/         ← sous-feature, isolée de checkout
│   └── checkout/     ← sous-feature, isolée de cart
└── orders.service.ts
```

Règle : à chaque niveau, les features sont mutuellement isolées. Une feature ne peut importer **que** ses ancêtres et descendants. Voir la section [Sous-features](.claude/rules/frontend-guidelines.md#sous-features) pour le détail.

### Mise en place

Le linter est posé mais **pas encore actif** : il a besoin d'un projet Angular initialisé et des dépendances installées.

```bash
# 1. Installer les dépendances (après que l'app Angular existe)
npm install -D eslint typescript-eslint

# 2. Ajouter les scripts à package.json
#    "lint":     "eslint src/"
#    "lint:fix": "eslint --fix src/"

# 3. Lancer
npm run lint
```

Commandes ad-hoc utiles :
```bash
npx eslint src/                          # tout le projet
npx eslint src/app/features/relay/       # un dossier précis
npx eslint --fix src/                    # auto-fix
```

### Limitations restantes

| Limitation | Détail | Contournement |
|------------|--------|---------------|
| **Imports relatifs invisibles** | `../../features/relay/...` contourne la règle (qui matche seulement `@features/*`) | Discipline d'équipe : toujours utiliser les path aliases |
| **Façade non enforced depuis `pages/`** | Une page peut importer un fichier interne de feature (`@features/relay/relay.gateway`) au lieu de passer par `@features/relay` | Ajouter une règle ciblant `pages/**` qui bloque les deep imports |

Demande à Claude d'enrichir le config si tu veux durcir l'une de ces limitations.

---

## Personnalisation

- **Modifier les règles** : édite [.claude/rules/frontend-guidelines.md](.claude/rules/frontend-guidelines.md) — les changements sont actifs au prochain redémarrage de Claude.
- **Ajouter des règles** : crée un nouveau fichier dans `.claude/rules/` puis ajoute `@.claude/rules/<nom>.md` dans [CLAUDE.md](CLAUDE.md).
- **Ajouter un skill** : place-le dans `.agents/skills/<nom>/SKILL.md` et ajoute un symlink dans `.claude/skills/`.
- **Ajouter un MCP** : ajoute une entrée sous `mcpServers` dans [.mcp.json](.mcp.json).

---

## Versionnement

Sont **versionnés** (partagés avec l'équipe) :
- `CLAUDE.md`, `.claude/rules/`, `.claude/skills/` (symlinks)
- `.agents/skills/` (skills installés)
- `.mcp.json`, `skills-lock.json`

Sont **locaux** (non versionnés) :
- `.claude/settings.local.json` (préférences perso)

---

## Ressources

- [Documentation Claude Code](https://docs.claude.com/claude-code)
- [Angular](https://angular.dev)
- [Skills Angular officiels](https://github.com/angular/skills)
