# Guide de Développement Frontend Angular — Version Simon

## 🎯 Objectif

Ce document définit les standards de développement frontend Angular afin de garantir :
- Cohérence entre projets
- Maintenabilité
- Scalabilité
- Qualité du code

---

# 🏗️ Architecture Frontend

## Principes

- Architecture **en couches descendantes**
- Séparation stricte des responsabilités
- Une couche ne peut dépendre que des couches situées « en-dessous »

---

## Structure globale

```
src/
├── app/
│   ├── core/         ← infrastructure & cross-cutting
│   ├── shared/       ← kernel partagé entre features
│   ├── features/     ← métier (bounded contexts)
│   ├── pages/        ← orchestration UI (compose des features)
│   ├── components/   ← UI globale (header, language, redirect…)
│   ├── guards/
│   ├── interceptors/
│   ├── animations/
│   └── routes/
│
├── assets/
├── config/
└── styles/
```

---

## Règle de dépendance (critique)

```
pages/  ──→  features/  ──→  shared/  ──→  core/
```

- `core/` ne dépend de **rien** d'autre que `core/`
- `shared/` peut dépendre de `core/`
- `features/` peuvent dépendre de `shared/` et `core/`
- `features/X` **ne peut PAS** dépendre de `features/Y` ← **règle critique**
- `pages/` peuvent tout importer (couche d'orchestration)
- Une feature peut **nidifier des sous-features** dans son propre dossier `features/` (voir [Sous-features](#sous-features))

❌ Aucun import inverse (core qui dépend de features, etc.)
❌ Aucun import inter-features (à n'importe quel niveau)

---

## Path aliases

Configurés dans `tsconfig.json` :

| Alias | Chemin |
|---|---|
| `@core/*` | `src/app/core/*` |
| `@shared/*` | `src/app/shared/*` |
| `@features/*` | `src/app/features/*` |

```ts
import { RelayService } from '@features/relay';                  // ✅
import { ValidatorsService } from '@core/utils';                 // ✅
import { ... } from '../../../features/relay/relay.service';     // ❌
```

---

## Couche `core/`

Services techniques transverses, **sans logique métier**.

```
core/
├── context/      ← langue, état applicatif global
├── errors/       ← gestion d'erreurs UI + types d'erreur métier
├── storage/      ← wrappers localStorage / sessionStorage
└── utils/        ← validators, directives, helpers
```

---

## Couche `shared/`

Concepts partagés entre plusieurs features (« kernel »). Pas de logique métier de feature spécifique.

```
shared/
├── address/        ← géocoding, adresses
├── identity/       ← user, rôles, droits, profil, token
├── task-types/     ← types de tâche (utilisé par tasks et relay)
└── tarification/   ← contrats / tarifs
```

---

## Couche `features/`

Bounded contexts métier. Chaque feature suit une structure 3-couches stricte :

```
features/relay/
├── relay.gateway.ts     ← SEUL endroit autorisé pour HttpClient
├── relay.mapper.ts      ← DTO ↔ Model uniquement
├── relay.service.ts     ← orchestration (gateway + mapper)
├── relay.store.ts       ← (optionnel) signal store @ngrx/signals
├── components/          ← composants métier de la feature
├── dto/                 ← interfaces alignées sur l'API (internes)
├── models/              ← modèles domaine (publics)
├── enums/               ← énumérations
└── index.ts             ← façade publique
```

### Règles par fichier

| Fichier | Rôle | Restrictions |
|---|---|---|
| `*.gateway.ts` | Appels HTTP, retourne des DTOs bruts | Seul endroit autorisé pour `HttpClient` |
| `*.mapper.ts` | Conversion DTO ↔ Model | **Pas** d'appel HTTP, pas d'orchestration |
| `*.service.ts` | Compose gateway + mapper, expose des modèles | Pas d'HTTP direct |
| `*.store.ts` | État local complexe (multi-section, save/reset) | Optionnel — éviter les god-stores |
| `dto/*` | Contrat backend | **Interne**, jamais exposé via la façade |

---

## Sous-features

Quand une feature devient grosse et regroupe plusieurs sous-domaines **indépendants entre eux mais consommés uniquement par la feature mère**, elle peut nidifier ses propres sous-features dans son dossier `features/` interne.

```
features/orders/
├── features/                 ← sous-features de orders/
│   ├── cart/
│   │   ├── cart.gateway.ts
│   │   ├── cart.mapper.ts
│   │   ├── cart.service.ts
│   │   └── index.ts          ← façade interne
│   └── checkout/
│       ├── checkout.service.ts
│       └── index.ts
├── orders.service.ts
├── orders.store.ts
└── index.ts                  ← façade publique de orders/
```

### Règles d'isolation (récursives)

À **chaque niveau** d'imbrication, les features sont mutuellement isolées :

| Origine | Cible | Autorisé ? |
|---|---|---|
| `features/orders/features/cart/` | `features/orders/features/checkout/` | ❌ siblings : isolation stricte |
| `features/orders/features/cart/` | `features/orders/orders.service.ts` | ✅ accès à la mère (ancêtre) |
| `features/orders/` (mère) | `features/orders/features/cart/` | ✅ accès aux descendants |
| `features/billing/` (autre feature top-level) | `features/orders/features/cart/` | ❌ une sous-feature reste interne |
| `pages/` | `features/orders/features/cart/` | ❌ pages passent par `@features/orders` (façade) |

**Principe général** : une feature peut importer **uniquement** ses ancêtres et ses descendants. Tout le reste (siblings, cousines, branches parallèles) est bloqué par ESLint.

### Quand introduire une sous-feature ?

- ✅ Plusieurs sous-domaines clairement indépendants au sein d'un domaine métier (ex : `orders/{cart,checkout,payment}`)
- ✅ Ces sous-domaines ne sont consommés que par la feature mère ou ses autres descendants
- ❌ Si une sous-feature est utilisée par plusieurs features top-level → la promouvoir dans `shared/`
- ❌ Si la feature est petite → garder à plat, ne pas sur-architecturer

### Façade

La feature mère (`orders/index.ts`) décide ce qu'elle expose au monde extérieur. Pour exposer un service de sous-feature, la mère le ré-exporte explicitement :

```ts
// features/orders/index.ts
export { OrdersService } from './orders.service';
export { CartService } from './features/cart';   // ré-export explicite
```

Depuis l'extérieur, on importe toujours **via la façade de la feature top-level** :

```ts
import { CartService } from '@features/orders';                       // ✅
import { CartService } from '@features/orders/features/cart';         // ❌ contourne la façade
```

---

## Façade publique (`index.ts`)

Chaque module (core / shared / feature) expose son API via un `index.ts`.

**Exposé** :
- ✅ Service principal
- ✅ Store éventuel
- ✅ Models (types domaine)
- ✅ Enums
- ✅ Composants réutilisables hors du module

**Non exposé** :
- ❌ Gateway
- ❌ Mapper
- ❌ DTOs

```ts
import { RelayService, type Relay } from '@features/relay';        // ✅
import { RelayGateway } from '@features/relay/relay.gateway';      // ❌ interne
```

---

## Couche `pages/`

- Composants routés uniquement
- 1 page = 1 écran
- Peut composer plusieurs features (c'est légitime à ce niveau)

❌ Pas d'appel HTTP direct (passer par un service de feature)
❌ Pas de logique métier propre (déléguer à un service ou store)

---

## Couche `components/`

Composants UI globaux (header, language switcher, redirect…). Aucune logique métier.

---

## Garde-fou ESLint

Le fichier [`eslint.config.mjs`](../../eslint.config.mjs) à la racine mécanise les règles de frontière.

```bash
npx eslint src/                          # check tout le projet
npx eslint src/app/features/relay/       # un dossier précis
npx eslint --fix src/                    # auto-fix ce qui peut l'être
```

Règles appliquées :
- `core/` ne peut pas importer `shared/` ou `features/`
- `shared/` ne peut pas importer `features/`
- une feature ne peut importer que ses propres ancêtres et descendants (à n'importe quel niveau d'imbrication)

Les features sont **auto-découvertes** : tout dossier `features/<X>/` (à n'importe quelle profondeur) est traité comme une feature. Pas besoin de maintenir une liste manuellement.

---

## Anti-patterns

❌ Import inter-feature (`@features/X` depuis `features/Y/`)
❌ Import des internes d'un module (`@features/X/relay.gateway` depuis l'extérieur)
❌ HTTP dans un composant, une page, un service hors gateway
❌ Mapping DTO ailleurs que dans un mapper
❌ Logique métier dans la couche UI (composants, pages)
❌ `shared/` ou `core/` qui dépendent d'une feature

---

# 🅰️ Conventions Angular

## Templates

**Règle absolue : un fichier `.html` séparé par composant.** Pas d'exception.

- ✅ `templateUrl: './foo.html'` (chemin relatif au fichier `.ts`)
- ❌ `template: \`...\`` inline, même pour un composant minuscule

Pourquoi : lisibilité, diff Git propre, séparation des préoccupations, consistance entre tous les composants du projet.

```ts
@Component({
  selector: 'app-foo',
  templateUrl: './foo.html',   // ✅
  styleUrl: './foo.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Foo { … }
```

Même règle pour les **styles** : `styleUrl: './foo.scss'` séparé, jamais `styles: [...]` inline.

---

## Tests unitaires

**Règle absolue : un `.spec.ts` à côté de chaque fichier produisant du code exécutable.** Pas d'exception.

| Fichier | Spec attendu |
|---|---|
| `foo.component.ts` | `foo.component.spec.ts` |
| `foo.service.ts` | `foo.service.spec.ts` |
| `foo.gateway.ts` | `foo.gateway.spec.ts` |
| `foo.mapper.ts` | `foo.mapper.spec.ts` |
| `foo.store.ts` | `foo.store.spec.ts` |
| `foo.pipe.ts` / `foo.directive.ts` / `foo.guard.ts` | spec correspondant |
| DTOs / models / enums purs | pas de spec (pas de comportement) |

### Couverture minimale

- **Composant** : montage sans erreur + un test par `@Output` + un test par `computed`/branche métier visible
- **Service / Store** : un test par méthode publique (cas nominal + au moins un cas limite)
- **Mapper** : aller-retour DTO ↔ Model + valeurs limites (vide, null, valeurs hors-domaine)
- **Gateway** : mock `HttpTestingController`, vérifier URL + méthode + body + parsing de la réponse

### Outillage

- **Runner** : Vitest (configuré au scaffold via `--skip-tests=false`)
- `npx ng test` lance la suite complète
- `TestBed` pour les composants, `RouterTestingHarness` pour le routing, `HttpTestingController` pour les gateways

❌ Ne jamais merger un fichier sans son spec
❌ Ne jamais créer un composant via `Write` sans créer le spec dans la foulée — préférer `npx ng generate component <nom>` qui génère le spec automatiquement

---

# 📱 Mobile — Capacitor

## Principe

Application Angular embarquée dans une WebView native.

---

## Règles

- ❌ Ne jamais utiliser userAgent
- ✅ Utiliser API Capacitor

---

## Safe areas

- Utiliser variables CSS natives
- Ne jamais hardcoder padding

---

## UI Mobile

- Zone tactile min : 44x44px
- ❌ Pas de hover-only
- Feedback visuel obligatoire

---

## Performances

- Animations uniquement :
  - transform
  - opacity

- ❌ Jamais :
  - margin
  - top
  - left

---

## Plugins obligatoires

- push → @capacitor/push-notifications
- network → @capacitor/network
- filesystem → @capacitor/filesystem
- etc.

---

## Règles critiques

❌ Ne jamais appeler API browser native  
✅ Toujours passer par Capacitor

---

## Tests

- Tester sur vrais devices
- Tester iOS + Android

---

# 🎨 UX / UI

## Couleurs principales

- primary : #AB79FF
- purple-dark : #450c69
- green : #003E3D
- red : #810038

---

## Typographie

- Police système
- h1 / h2 / h3 hiérarchisés

---

## Spacing

- Utilisation Tailwind
- Classes utilitaires SCSS

---

## Layout

### Sidebar

- largeur : min(250px, 25vw)

### Responsive

- sm ≥ 640px
- md ≥ 768px
- lg ≥ 1024px

---

## Composants (PrimeNG)

### Boutons

- border-radius = 0
- variants : primary, secondary, success, danger

---

### Inputs

- hauteur : 2rem
- états :
  - focus → violet
  - erreur → rouge

---

### Modales

- non draggable
- non resizable
- modal obligatoire

---

### Tables

- bordures inter-colonnes

---

## UX Rules

### Boutons d’action

- toujours en bas à droite

---

### Feedback save

- success → vert
- error → rouge

---

### Gestion erreurs

- messages inline
- sous les champs

---

# ♿ Accessibilité

## Images

- informatives → alt obligatoire
- décoratives → alt=""

---

## Navigation

- aria-label obligatoire

---

## Formulaires

- aria-label obligatoire
- fieldset + legend

---

## Labels

- toujours liés via for/id

---

## Boutons

❌ pas de div/span cliquable  
✅ utiliser button

---

## Clavier

- support Enter / Space

---

## Autocomplete

- utiliser valeurs HTML standard

---

## PrimeNG fixes

- p-sortIcon → span aria-hidden
- p-columnFilter → custom icon
- traductions aria obligatoires

---

# 🧠 Philosophie

Ce guide vise à :

- faciliter onboarding
- réduire dette technique
- standardiser pratiques
- garantir qualité long terme

---

# 🚀 Conclusion

Ce document est une base évolutive.

Toute modification doit :
- être discutée
- être validée
- améliorer la qualité globale