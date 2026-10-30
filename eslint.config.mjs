// Règles d'architecture du projet — voir .claude/rules/frontend-guidelines.md
//
// Lancer : npx eslint src/
//          npx eslint src/app/features/relay/  (un dossier précis)
//
// Les features sont auto-découvertes en scannant `src/app/features/` récursivement.
// Une feature peut nidifier des sous-features dans son propre dossier `features/` :
//
//   features/orders/
//   ├── features/
//   │   ├── cart/         ← sous-feature, isolée de checkout
//   │   └── checkout/     ← sous-feature, isolée de cart
//   └── orders.service.ts
//
// Règle d'isolation (récursive) : une feature ne peut importer que ses propres
// ancêtres et descendants. Toutes les autres features (siblings, cousines) sont bloquées.

import { readdirSync, existsSync, statSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join, relative, sep } from 'path';

import tseslint from 'typescript-eslint';

const __dirname = dirname(fileURLToPath(import.meta.url));
const srcApp = join(__dirname, 'src/app');

// Auto-discovery récursive : un dossier `features/<X>/` à n'importe quelle profondeur est une feature.
function findFeatures(basePath, results = []) {
  const featuresDir = join(basePath, 'features');
  if (!existsSync(featuresDir) || !statSync(featuresDir).isDirectory()) return results;

  const children = readdirSync(featuresDir).filter((name) =>
    statSync(join(featuresDir, name)).isDirectory(),
  );

  for (const name of children) {
    const featurePath = join(featuresDir, name);
    const relPath = relative(srcApp, featurePath).split(sep).join('/');
    results.push({ relPath, alias: '@' + relPath });
    findFeatures(featurePath, results);
  }

  return results;
}

const features = findFeatures(srcApp);

const featureBoundaryMessage =
  "Une feature ne peut importer que ses propres ancêtres et descendants. " +
  "Pour partager du code entre features, passe par shared/ ou compose dans pages/. " +
  "Une sous-feature reste interne à sa feature mère.";

const coreUpwardMessage =
  "core/ ne peut pas dépendre de shared/ ou features/. " +
  "Inverse la dépendance ou extrais le concept commun dans core/.";

const sharedUpwardMessage =
  "shared/ ne peut pas dépendre de features/. " +
  "Inverse la dépendance ou extrais le concept commun dans shared/.";

const isAncestorOf = (a, b) => b.startsWith(a + '/');

// Tri par profondeur croissante : les configs des features profondes viennent après
// celles de leurs ancêtres, donc surchargent leurs règles pour les fichiers partagés.
const featuresSorted = [...features].sort(
  (a, b) => a.relPath.split('/').length - b.relPath.split('/').length,
);

const featureBoundaryConfigs = featuresSorted.map((self) => {
  const forbidden = features.filter(
    (other) =>
      other.relPath !== self.relPath &&
      !isAncestorOf(other.relPath, self.relPath) && // pas un ancêtre de self
      !isAncestorOf(self.relPath, other.relPath),   // pas un descendant de self
  );

  return {
    files: [`src/app/${self.relPath}/**/*.ts`],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: forbidden.flatMap((other) => [
            { group: [other.alias], message: featureBoundaryMessage },
            { group: [`${other.alias}/*`], message: featureBoundaryMessage },
          ]),
        },
      ],
    },
  };
});

export default [
  // Base : registre tous les fichiers .ts du projet
  {
    files: ['src/**/*.ts'],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
    },
  },

  // Ignore les builds, node_modules, fichiers générés
  {
    ignores: ['dist/**', 'coverage/**', '.angular/**', 'node_modules/**'],
  },

  // Règle 1 : core/ ne dépend que de core/
  {
    files: ['src/app/core/**/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            { group: ['@shared/*', '@shared/**'], message: coreUpwardMessage },
            { group: ['@features/*', '@features/**'], message: coreUpwardMessage },
          ],
        },
      ],
    },
  },

  // Règle 2 : shared/ ne dépend que de core/ et shared/
  {
    files: ['src/app/shared/**/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            { group: ['@features/*', '@features/**'], message: sharedUpwardMessage },
          ],
        },
      ],
    },
  },

  // Règle 3 : isolation des features (auto-découvertes, récursif via sous-features)
  ...featureBoundaryConfigs,
];
