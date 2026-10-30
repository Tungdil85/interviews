"""Exercices d'algorithmique en TypeScript (format entretien, 20 à 35 minutes).

Importé par build_exercises.py. Chaque test est le corps d'une fonction async qui voit le code de
l'utilisateur et reçoit `assert` et `console`. Les tests « grosse entrée » vérifient la complexité :
le moteur interrompt un test après 5 s. exercises.data.spec.ts valide chaque solution.
"""

E, M, H = "easy", "medium", "hard"
ALGOS = []


def algo(id, title, diff, topic, minutes, description, starter, tests, hints, solution):
    ALGOS.append({
        "id": id, "kind": "algo", "title": title, "difficulty": diff, "topic": topic, "durationMin": minutes,
        "description": description.strip(), "starterCode": starter.lstrip("\n"),
        "tests": [{"name": n, "code": c.strip()} for n, c in tests],
        "hints": hints, "solution": solution.lstrip("\n"), "preview": "",
    })


algo("algo-two-sum", "Two Sum", E, "Tableaux · Table de hachage", 20,
 r"""**Objectif** : trouver deux nombres d'un tableau dont la somme vaut une cible.

**Exemples**
```ts
twoSum([2, 7, 11, 15], 9)   // [0, 1]  car 2 + 7 = 9
twoSum([3, 2, 4], 6)        // [1, 2]
twoSum([1, 2, 3], 10)       // null    (aucune paire)
```

**Contraintes**
• renvoie les indices `[i, j]` avec `i < j` ; un même élément ne peut pas être utilisé deux fois ;
• s'il n'existe aucune paire, renvoie `null` ; il y a au plus une paire valide ;
• le tableau peut contenir 100 000 éléments : une double boucle (O(n²)) sera trop lente.

**À faire** : implémente `twoSum`. Vise une complexité **O(n)**.""",
 r'''
/**
 * Retourne les indices [i, j] (i < j) de deux éléments dont la somme vaut `target`,
 * ou null s'il n'existe aucune paire.
 */
export function twoSum(nums: number[], target: number): [number, number] | null {
  // TODO
  return null;
}
''',
 [("Exemple de base", r'''assert.deepEqual(twoSum([2, 7, 11, 15], 9), [0, 1]);'''),
  ("Indices dans l'ordre croissant", r'''assert.deepEqual(twoSum([3, 2, 4], 6), [1, 2]);'''),
  ("Doublons", r'''assert.deepEqual(twoSum([3, 3], 6), [0, 1]);'''),
  ("Nombres négatifs", r'''assert.deepEqual(twoSum([-1, -2, -3, -4, -5], -8), [2, 4]);'''),
  ("Aucune paire", r'''assert.equal(twoSum([1, 2, 3], 10), null);'''),
  ("Un élément ne compte pas deux fois", r'''assert.equal(twoSum([5, 1], 10), null); assert.equal(twoSum([5], 10), null);'''),
  ("100 000 éléments (O(n) attendu)", r'''const nums = Array.from({ length: 100000 }, (_, i) => i * 2); assert.deepEqual(twoSum(nums, 399994), [99998, 99999]);''')],
 ["Pour chaque nombre `x`, tu cherches `target - x` : comment le retrouver sans reparcourir le tableau ?", "Une `Map<valeur, indice>` remplie au fil du parcours donne la réponse en O(1) par élément.", "Vérifie le complément AVANT d'insérer l'élément courant, pour ne pas l'utiliser deux fois."],
 r'''
export function twoSum(nums: number[], target: number): [number, number] | null {
  const seen = new Map<number, number>(); // valeur -> indice
  for (let j = 0; j < nums.length; j++) {
    const i = seen.get(target - nums[j]);
    if (i !== undefined) return [i, j];
    seen.set(nums[j], j);
  }
  return null;
}
// Complexité : O(n) en temps, O(n) en mémoire.
''')

algo("algo-valid-brackets", "Parenthèses équilibrées", E, "Pile", 20,
 r"""**Objectif** : vérifier qu'un texte contient des parenthèses, crochets et accolades correctement ouverts, fermés et imbriqués.

**Exemples**
```ts
isBalanced('{[()]}')     // true
isBalanced('([)]')       // false  (mauvais ordre de fermeture)
isBalanced('((')         // false  (fermetures manquantes)
isBalanced('a(b[c]d)e')  // true   (les autres caractères sont ignorés)
```

**Contraintes**
• seuls `()`, `[]` et `{}` comptent, tous les autres caractères sont ignorés ;
• une chaîne vide est équilibrée ;
• le texte peut faire 100 000 caractères.

**À faire** : implémente `isBalanced`.""",
 r'''
export function isBalanced(s: string): boolean {
  // TODO
  return false;
}
''',
 [("Cas équilibrés", r'''assert.equal(isBalanced('()[]{}'), true); assert.equal(isBalanced('{[()]}'), true);'''),
  ("Mauvais type de fermeture", r'''assert.equal(isBalanced('(]'), false);'''),
  ("Mauvais ordre", r'''assert.equal(isBalanced('([)]'), false);'''),
  ("Ouvertures sans fermeture", r'''assert.equal(isBalanced('(('), false);'''),
  ("Fermeture en trop", r'''assert.equal(isBalanced('())'), false); assert.equal(isBalanced(')'), false);'''),
  ("Chaîne vide", r'''assert.equal(isBalanced(''), true);'''),
  ("Autres caractères ignorés", r'''assert.equal(isBalanced('a(b[c]d)e'), true); assert.equal(isBalanced('abc'), true);'''),
  ("100 000 caractères", r'''assert.equal(isBalanced('('.repeat(50000) + ')'.repeat(50000)), true); assert.equal(isBalanced('('.repeat(50000) + ']'), false);''')],
 ["Le dernier symbole ouvert doit être le premier fermé : quelle structure de données fonctionne ainsi ?", "Empile chaque ouvrant ; sur un fermant, dépile et compare avec l'ouvrant attendu.", "À la fin, la pile doit être vide."],
 r'''
export function isBalanced(s: string): boolean {
  const pairs: Record<string, string> = { ')': '(', ']': '[', '}': '{' };
  const stack: string[] = [];
  for (const ch of s) {
    if (ch === '(' || ch === '[' || ch === '{') {
      stack.push(ch);
    } else if (ch in pairs && stack.pop() !== pairs[ch]) {
      return false;
    }
  }
  return stack.length === 0;
}
// Complexité : O(n).
''')

algo("algo-group-anagrams", "Grouper les anagrammes", M, "Table de hachage · Chaînes", 25,
 r"""**Objectif** : regrouper les mots qui sont des anagrammes les uns des autres (mêmes lettres, ordre différent).

**Exemple**
```ts
groupAnagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
// [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

**Contraintes**
• les groupes sont dans l'ordre de première apparition de leur premier mot ;
• dans un groupe, les mots gardent leur ordre d'origine ;
• jusqu'à 50 000 mots : comparer chaque mot à tous les groupes (O(n²)) sera trop lent.

**À faire** : implémente `groupAnagrams`. Trouve une « clé » commune à tous les anagrammes d'un mot.""",
 r'''
export function groupAnagrams(words: string[]): string[][] {
  // TODO
  return [];
}
''',
 [("Exemple de base", r'''assert.deepEqual(groupAnagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat']), [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]);'''),
  ("Mot vide et mot d'une lettre", r'''assert.deepEqual(groupAnagrams(['']), [['']]); assert.deepEqual(groupAnagrams(['a']), [['a']]);'''),
  ("Liste vide", r'''assert.deepEqual(groupAnagrams([]), []);'''),
  ("Pas de regroupement abusif", r'''assert.deepEqual(groupAnagrams(['ab', 'abc', 'ba']), [['ab', 'ba'], ['abc']]);'''),
  ("Mots identiques", r'''assert.deepEqual(groupAnagrams(['aa', 'aa']), [['aa', 'aa']]);'''),
  ("50 000 mots", r'''const words = []; for (let i = 0; i < 25000; i++) { const w = i.toString(36).padStart(6, 'a'); words.push(w, w.split('').reverse().join('')); }
const groups = groupAnagrams(words);
assert.equal(groups.flat().length, 50000);
const key = (w) => w.split('').sort().join('');
assert.ok(groups.every((g) => g.every((w) => key(w) === key(g[0]))), 'chaque groupe doit contenir des anagrammes');
assert.equal(new Set(groups.map((g) => key(g[0]))).size, groups.length, 'une même famille ne doit pas être coupée en deux groupes');''')],
 ["Deux mots sont des anagrammes si leurs lettres triées sont identiques.", "Utilise cette version triée comme clé d'une `Map<string, string[]>`.", "Une `Map` conserve l'ordre d'insertion : les groupes sortent déjà dans le bon ordre."],
 r'''
export function groupAnagrams(words: string[]): string[][] {
  const groups = new Map<string, string[]>();
  for (const word of words) {
    const key = word.split('').sort().join('');
    const group = groups.get(key);
    if (group) group.push(word);
    else groups.set(key, [word]);
  }
  return [...groups.values()];
}
// Complexité : O(n · k log k) avec k la longueur moyenne d'un mot.
''')

algo("algo-longest-unique-substring", "Plus longue sous-chaîne sans répétition", M, "Fenêtre glissante", 30,
 r"""**Objectif** : trouver la longueur de la plus longue sous-chaîne **contiguë** dont tous les caractères sont différents.

**Exemples**
```ts
lengthOfLongestSubstring('abcabcbb')   // 3  ("abc")
lengthOfLongestSubstring('bbbbb')      // 1  ("b")
lengthOfLongestSubstring('pwwkew')     // 3  ("wke")
lengthOfLongestSubstring('abba')       // 2  ("ab" ou "ba")
```

**Contraintes**
• la chaîne peut faire 200 000 caractères : pas de recalcul depuis zéro à chaque position (O(n²)) ;
• une chaîne vide donne 0.

**À faire** : implémente `lengthOfLongestSubstring` en un seul parcours, avec une fenêtre glissante.""",
 r'''
export function lengthOfLongestSubstring(s: string): number {
  // TODO
  return 0;
}
''',
 [("Exemple abcabcbb", r'''assert.equal(lengthOfLongestSubstring('abcabcbb'), 3);'''),
  ("Un seul caractère répété", r'''assert.equal(lengthOfLongestSubstring('bbbbb'), 1);'''),
  ("pwwkew", r'''assert.equal(lengthOfLongestSubstring('pwwkew'), 3);'''),
  ("Chaîne vide", r'''assert.equal(lengthOfLongestSubstring(''), 0);'''),
  ("Piège : abba", r'''assert.equal(lengthOfLongestSubstring('abba'), 2);'''),
  ("dvdf", r'''assert.equal(lengthOfLongestSubstring('dvdf'), 3);'''),
  ("Espace et un caractère", r'''assert.equal(lengthOfLongestSubstring(' '), 1); assert.equal(lengthOfLongestSubstring('a'), 1);'''),
  ("200 000 caractères (O(n) attendu)", r'''assert.equal(lengthOfLongestSubstring('abcdefghij'.repeat(20000)), 10);''')],
 ["Garde une fenêtre [gauche, droite] qui ne contient jamais de doublon.", "Quand le caractère courant a déjà été vu DANS la fenêtre, avance `gauche` juste après sa dernière position.", "Attention au cas `abba` : ne recule jamais `gauche` (prends le maximum)."],
 r'''
export function lengthOfLongestSubstring(s: string): number {
  const lastSeen = new Map<string, number>();
  let left = 0;
  let best = 0;
  for (let right = 0; right < s.length; right++) {
    const previous = lastSeen.get(s[right]);
    if (previous !== undefined && previous >= left) left = previous + 1;
    lastSeen.set(s[right], right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}
// Complexité : O(n).
''')

algo("algo-merge-intervals", "Fusionner des intervalles", M, "Tri · Intervalles", 30,
 r"""**Objectif** : fusionner tous les intervalles qui se chevauchent ou se touchent.

**Exemples**
```ts
mergeIntervals([[1, 3], [2, 6], [8, 10], [15, 18]])   // [[1, 6], [8, 10], [15, 18]]
mergeIntervals([[1, 4], [4, 5]])                      // [[1, 5]]   (ils se touchent)
mergeIntervals([[8, 10], [1, 3], [2, 6]])             // [[1, 6], [8, 10]]   (entrée non triée)
```

**Contraintes**
• chaque intervalle est `[début, fin]` avec `début <= fin` ;
• la liste n'est pas forcément triée ;
• ne modifie pas le tableau reçu ;
• jusqu'à 100 000 intervalles.

**À faire** : implémente `mergeIntervals`. Réfléchis à ce qui devient simple une fois les intervalles triés.""",
 r'''
export function mergeIntervals(intervals: [number, number][]): [number, number][] {
  // TODO
  return [];
}
''',
 [("Exemple de base", r'''assert.deepEqual(mergeIntervals([[1, 3], [2, 6], [8, 10], [15, 18]]), [[1, 6], [8, 10], [15, 18]]);'''),
  ("Intervalles qui se touchent", r'''assert.deepEqual(mergeIntervals([[1, 4], [4, 5]]), [[1, 5]]);'''),
  ("Entrée non triée", r'''assert.deepEqual(mergeIntervals([[8, 10], [1, 3], [2, 6]]), [[1, 6], [8, 10]]);'''),
  ("Intervalle contenu dans un autre", r'''assert.deepEqual(mergeIntervals([[1, 10], [2, 3]]), [[1, 10]]);'''),
  ("Fusion en chaîne", r'''assert.deepEqual(mergeIntervals([[1, 4], [0, 2], [3, 5]]), [[0, 5]]);'''),
  ("Vide et un seul intervalle", r'''assert.deepEqual(mergeIntervals([]), []); assert.deepEqual(mergeIntervals([[2, 3]]), [[2, 3]]);'''),
  ("Ne modifie pas l'entrée", r'''const input = [[5, 6], [1, 3], [2, 4]]; const copy = JSON.parse(JSON.stringify(input)); mergeIntervals(input); assert.deepEqual(input, copy);'''),
  ("100 000 intervalles", r'''const input = Array.from({ length: 100000 }, (_, i) => [i * 3, i * 3 + 2]).reverse(); const out = mergeIntervals(input); assert.equal(out.length, 100000); assert.deepEqual(out[0], [0, 2]);''')],
 ["Trie une copie des intervalles par début.", "Parcours-les dans l'ordre : l'intervalle courant chevauche le dernier fusionné si `début <= fin du dernier`.", "Dans ce cas, étends la fin du dernier avec `Math.max` ; sinon, ouvre un nouvel intervalle."],
 r'''
export function mergeIntervals(intervals: [number, number][]): [number, number][] {
  const sorted = [...intervals].sort((a, b) => a[0] - b[0]);
  const merged: [number, number][] = [];
  for (const [start, end] of sorted) {
    const last = merged[merged.length - 1];
    if (last && start <= last[1]) last[1] = Math.max(last[1], end);
    else merged.push([start, end]);
  }
  return merged;
}
// Complexité : O(n log n) à cause du tri.
''')

algo("algo-spiral-matrix", "Parcours en spirale", M, "Matrices", 25,
 r"""**Objectif** : parcourir une matrice en spirale (vers la droite, puis le bas, puis la gauche, puis le haut, en se rapprochant du centre).

**Exemple**
```ts
spiralOrder([
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
])
// [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

**Contraintes**
• la matrice n'est pas forcément carrée (ex. 3 lignes × 4 colonnes) ;
• elle peut avoir une seule ligne, une seule colonne, ou être vide (`[]` donne `[]`) ;
• chaque case doit apparaître exactement une fois.

**À faire** : implémente `spiralOrder`. Pense à 4 bornes (haut, bas, gauche, droite) qui se resserrent.""",
 r'''
export function spiralOrder(matrix: number[][]): number[] {
  // TODO
  return [];
}
''',
 [("Matrice 3×3", r'''assert.deepEqual(spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), [1, 2, 3, 6, 9, 8, 7, 4, 5]);'''),
  ("Matrice 3×4", r'''assert.deepEqual(spiralOrder([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]), [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]);'''),
  ("Une seule ligne", r'''assert.deepEqual(spiralOrder([[1, 2, 3]]), [1, 2, 3]);'''),
  ("Une seule colonne", r'''assert.deepEqual(spiralOrder([[1], [2], [3]]), [1, 2, 3]);'''),
  ("Une case et matrice vide", r'''assert.deepEqual(spiralOrder([[7]]), [7]); assert.deepEqual(spiralOrder([]), []);'''),
  ("Plus de lignes que de colonnes", r'''assert.deepEqual(spiralOrder([[1, 2], [3, 4], [5, 6], [7, 8]]), [1, 2, 4, 6, 8, 7, 5, 3]);'''),
  ("300×300 : chaque case une fois", r'''const n = 300; const m = Array.from({ length: n }, (_, r) => Array.from({ length: n }, (_, c) => r * n + c)); const out = spiralOrder(m); assert.equal(out.length, n * n); assert.equal(new Set(out).size, n * n); assert.deepEqual(out.slice(0, n), m[0]);''')],
 ["Garde 4 bornes : `top`, `bottom`, `left`, `right`.", "À chaque tour : ligne du haut (gauche→droite), colonne de droite (haut→bas), ligne du bas (droite→gauche), colonne de gauche (bas→haut), puis resserre les bornes.", "Après avoir resserré, revérifie `top <= bottom` et `left <= right` avant la ligne du bas et la colonne de gauche (cas d'une seule ligne ou colonne)."],
 r'''
export function spiralOrder(matrix: number[][]): number[] {
  const result: number[] = [];
  if (matrix.length === 0) return result;
  let top = 0, bottom = matrix.length - 1, left = 0, right = matrix[0].length - 1;
  while (top <= bottom && left <= right) {
    for (let c = left; c <= right; c++) result.push(matrix[top][c]);
    top++;
    for (let r = top; r <= bottom; r++) result.push(matrix[r][right]);
    right--;
    if (top <= bottom) {
      for (let c = right; c >= left; c--) result.push(matrix[bottom][c]);
      bottom--;
    }
    if (left <= right) {
      for (let r = bottom; r >= top; r--) result.push(matrix[r][left]);
      left++;
    }
  }
  return result;
}
// Complexité : O(lignes × colonnes).
''')

algo("algo-top-k-words", "Les k mots les plus fréquents", M, "Table de hachage · Tri", 30,
 r"""**Objectif** : renvoyer les `k` mots qui apparaissent le plus souvent.

**Exemples**
```ts
topKFrequent(['i', 'love', 'leetcode', 'i', 'love', 'coding'], 2)   // ['i', 'love']
topKFrequent(['the', 'day', 'is', 'sunny', 'the', 'the', 'the', 'sunny', 'is', 'is'], 4)
// ['the', 'is', 'sunny', 'day']   (fréquences 4, 3, 2, 1)
```

**Contraintes**
• tri par fréquence **décroissante** ;
• à fréquence égale, par ordre **alphabétique** croissant ;
• si `k` dépasse le nombre de mots distincts, renvoie tous les mots ; `k = 0` donne `[]` ;
• jusqu'à 200 000 mots.

**À faire** : implémente `topKFrequent`.""",
 r'''
export function topKFrequent(words: string[], k: number): string[] {
  // TODO
  return [];
}
''',
 [("Exemple de base", r'''assert.deepEqual(topKFrequent(['i', 'love', 'leetcode', 'i', 'love', 'coding'], 2), ['i', 'love']);'''),
  ("Ordre par fréquence décroissante", r'''assert.deepEqual(topKFrequent(['the', 'day', 'is', 'sunny', 'the', 'the', 'the', 'sunny', 'is', 'is'], 4), ['the', 'is', 'sunny', 'day']);'''),
  ("Égalité : ordre alphabétique", r'''assert.deepEqual(topKFrequent(['b', 'a', 'c'], 2), ['a', 'b']);'''),
  ("k plus grand que le nombre de mots distincts", r'''assert.deepEqual(topKFrequent(['a', 'a', 'b'], 5), ['a', 'b']);'''),
  ("k = 0", r'''assert.deepEqual(topKFrequent(['a', 'b'], 0), []);'''),
  ("200 000 mots", r'''const words = Array.from({ length: 200000 }, (_, i) => 'w' + (i % 1000)); assert.deepEqual(topKFrequent(words, 3), ['w0', 'w1', 'w10']);''')],
 ["Compte d'abord les occurrences avec une `Map<mot, nombre>`.", "Trie ensuite les mots distincts avec un comparateur à deux critères : fréquence décroissante, puis ordre alphabétique.", "Compare les chaînes avec `<` / `>` pour un ordre alphabétique simple."],
 r'''
export function topKFrequent(words: string[], k: number): string[] {
  const counts = new Map<string, number>();
  for (const word of words) counts.set(word, (counts.get(word) ?? 0) + 1);
  return [...counts.keys()]
    .sort((a, b) => counts.get(b)! - counts.get(a)! || (a < b ? -1 : a > b ? 1 : 0))
    .slice(0, k);
}
// Complexité : O(n + d log d) avec d le nombre de mots distincts.
''')

algo("algo-islands", "Nombre d'îles", M, "Graphes · Parcours de grille", 30,
 r"""**Objectif** : compter les îles d'une carte. Une île est un groupe de cases de terre (`'1'`) reliées horizontalement ou verticalement, entourées d'eau (`'0'`).

**Exemple**
```ts
countIslands([
  '11000',
  '11000',
  '00100',
  '00011',
])
// 3
```

**Contraintes**
• deux cases en diagonale ne sont **pas** reliées ;
• une carte vide ou sans terre donne 0 ;
• la carte peut faire 600 × 600 : une récursion profonde provoquera un dépassement de pile.

**À faire** : implémente `countIslands`. Parcours chaque île une seule fois, sans récursion.""",
 r'''
export function countIslands(grid: string[]): number {
  // TODO
  return 0;
}
''',
 [("Une grande île", r'''assert.equal(countIslands(['11110', '11010', '11000', '00000']), 1);'''),
  ("Trois îles", r'''assert.equal(countIslands(['11000', '11000', '00100', '00011']), 3);'''),
  ("Que de l'eau, ou carte vide", r'''assert.equal(countIslands(['000', '000']), 0); assert.equal(countIslands([]), 0);'''),
  ("Les diagonales ne comptent pas", r'''assert.equal(countIslands(['10', '01']), 2);'''),
  ("Une seule case", r'''assert.equal(countIslands(['1']), 1);'''),
  ("Île en forme de U", r'''assert.equal(countIslands(['101', '101', '111']), 1);'''),
  ("Île géante 600×600 (pas de récursion)", r'''const grid = Array.from({ length: 600 }, () => '1'.repeat(600)); assert.equal(countIslands(grid), 1);'''),
  ("Damier 400×400 : 80 000 îles", r'''const grid = Array.from({ length: 400 }, (_, r) => Array.from({ length: 400 }, (_, c) => ((r + c) % 2 === 0 ? '1' : '0')).join('')); assert.equal(countIslands(grid), 80000);''')],
 ["Parcours toutes les cases ; quand tu trouves une terre non visitée, c'est une nouvelle île : incrémente le compteur.", "Puis « noie » toute l'île (marque ses cases visitées) avec un parcours en largeur ou en profondeur.", "Utilise une pile ou une file explicite plutôt que la récursion, pour les très grandes îles."],
 r'''
export function countIslands(grid: string[]): number {
  const rows = grid.length;
  if (rows === 0) return 0;
  const cols = grid[0].length;
  const visited = new Uint8Array(rows * cols);
  let islands = 0;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] !== '1' || visited[r * cols + c]) continue;
      islands++;
      const stack = [r * cols + c];
      visited[r * cols + c] = 1;
      while (stack.length > 0) {
        const cell = stack.pop()!;
        const cr = Math.floor(cell / cols);
        const cc = cell % cols;
        for (const [dr, dc] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          const nr = cr + dr;
          const nc = cc + dc;
          if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
          const next = nr * cols + nc;
          if (grid[nr][nc] === '1' && !visited[next]) {
            visited[next] = 1;
            stack.push(next);
          }
        }
      }
    }
  }
  return islands;
}
// Complexité : O(lignes × colonnes).
''')

algo("algo-maze", "Labyrinthe : plus court chemin", M, "Graphes · BFS", 35,
 r"""**Objectif** (façon CodinGame) : trouver le plus court chemin entre l'entrée `S` et la sortie `E` d'un labyrinthe.

**Exemple**
```ts
shortestPath([
  'S#E',
  '...',
])
// 4  (bas, droite, droite, haut)
```

**Légende** : `S` départ · `E` arrivée · `.` case libre · `#` mur.

**Contraintes**
• déplacements dans les 4 directions (haut, bas, gauche, droite), un pas = 1 ;
• renvoie le nombre minimal de pas, ou `-1` si la sortie est inaccessible ;
• la grille peut faire 500 × 500 : attention à la complexité et à la récursion.

**À faire** : implémente `shortestPath`. Quel parcours garantit de trouver le chemin le plus court dans un graphe non pondéré ?""",
 r'''
export function shortestPath(grid: string[]): number {
  // TODO
  return -1;
}
''',
 [("Ligne droite", r'''assert.equal(shortestPath(['S.E']), 2);'''),
  ("Départ à côté de la sortie", r'''assert.equal(shortestPath(['SE']), 1);'''),
  ("Contournement d'un mur", r'''assert.equal(shortestPath(['S#E', '...']), 4);'''),
  ("Sortie inaccessible", r'''assert.equal(shortestPath(['S#E']), -1);'''),
  ("Serpent : le chemin le plus court", r'''assert.equal(shortestPath(['S.....', '#####.', '......', '.#####', '....E.']), 18);'''),
  ("Chemin direct malgré des impasses", r'''assert.equal(shortestPath(['S.E', '.#.', '...']), 2);'''),
  ("Grille 500×500 (BFS attendu)", r'''const n = 500; const grid = Array.from({ length: n }, (_, r) => Array.from({ length: n }, (_, c) => (r === 0 && c === 0 ? 'S' : r === n - 1 && c === n - 1 ? 'E' : '.')).join('')); assert.equal(shortestPath(grid), 998);''')],
 ["Un parcours en profondeur (DFS) ne garantit PAS le plus court chemin. Pense au parcours en largeur (BFS).", "Utilise une file de cases à explorer et un tableau `visited` : chaque case est visitée au plus une fois.", "`array.shift()` est lent sur de grands tableaux : avance un indice de tête au lieu de retirer les éléments."],
 r'''
export function shortestPath(grid: string[]): number {
  const rows = grid.length;
  const cols = grid[0]?.length ?? 0;
  let start = -1;
  for (let r = 0; r < rows; r++) {
    const c = grid[r].indexOf('S');
    if (c !== -1) start = r * cols + c;
  }
  if (start === -1) return -1;

  const distance = new Int32Array(rows * cols).fill(-1);
  const queue: number[] = [start];
  distance[start] = 0;
  for (let head = 0; head < queue.length; head++) {
    const cell = queue[head];
    const r = Math.floor(cell / cols);
    const c = cell % cols;
    if (grid[r][c] === 'E') return distance[cell];
    for (const [dr, dc] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nr = r + dr;
      const nc = c + dc;
      if (nr < 0 || nc < 0 || nr >= rows || nc >= cols || grid[nr][nc] === '#') continue;
      const next = nr * cols + nc;
      if (distance[next] === -1) {
        distance[next] = distance[cell] + 1;
        queue.push(next);
      }
    }
  }
  return -1;
}
// Complexité : O(lignes × colonnes).
''')

algo("algo-lru-cache", "Cache LRU", H, "Structures de données", 35,
 r"""**Objectif** : implémenter un cache à capacité limitée qui, une fois plein, évince l'élément **le moins récemment utilisé** (LRU = Least Recently Used). Question classique d'entretien.

**Exemple**
```ts
const cache = new LRUCache<number, string>(2);
cache.put(1, 'a');
cache.put(2, 'b');
cache.get(1);        // 'a'  → la clé 1 devient la plus récente
cache.put(3, 'c');   // plein : évince la clé 2 (la moins récente)
cache.get(2);        // undefined
```

**Contraintes**
• `get(key)` renvoie la valeur, ou `undefined` si absente ; lire une clé la rend « récente » ;
• `put(key, value)` ajoute ou met à jour (et rend la clé récente) ; au-delà de la capacité, évince la plus ancienne ;
• les valeurs falsy (`0`, `''`, `false`) sont des valeurs valides ;
• les deux opérations doivent être en **O(1)** : les tests utilisent une capacité de 30 000.

**À faire** : implémente la classe `LRUCache`. Une `Map` JavaScript garde l'ordre d'insertion : comment l'exploiter ?""",
 r'''
export class LRUCache<K, V> {
  constructor(private readonly capacity: number) {}

  get(key: K): V | undefined {
    // TODO
    return undefined;
  }

  put(key: K, value: V): void {
    // TODO
  }
}
''',
 [("Clé absente", r'''const c = new LRUCache(2); assert.equal(c.get(1), undefined);'''),
  ("put puis get", r'''const c = new LRUCache(2); c.put(1, 'a'); assert.equal(c.get(1), 'a');'''),
  ("Évince la moins récemment utilisée", r'''const c = new LRUCache(2); c.put(1, 1); c.put(2, 2); c.put(3, 3); assert.equal(c.get(1), undefined); assert.equal(c.get(2), 2); assert.equal(c.get(3), 3);'''),
  ("get rend la clé récente", r'''const c = new LRUCache(2); c.put(1, 1); c.put(2, 2); assert.equal(c.get(1), 1); c.put(3, 3); assert.equal(c.get(2), undefined); c.put(4, 4); assert.equal(c.get(1), undefined); assert.equal(c.get(3), 3); assert.equal(c.get(4), 4);'''),
  ("put sur une clé existante : met à jour et rafraîchit", r'''const c = new LRUCache(2); c.put(1, 1); c.put(2, 2); c.put(1, 10); c.put(3, 3); assert.equal(c.get(2), undefined); assert.equal(c.get(1), 10);'''),
  ("Capacité 1", r'''const c = new LRUCache(1); c.put(1, 1); c.put(2, 2); assert.equal(c.get(1), undefined); assert.equal(c.get(2), 2);'''),
  ("Valeurs falsy conservées", r'''const c = new LRUCache(2); c.put('a', 0); c.put('b', ''); assert.equal(c.get('a'), 0); assert.equal(c.get('b'), '');'''),
  ("90 000 opérations, capacité 30 000 (O(1) attendu)", r'''const c = new LRUCache(30000); for (let i = 0; i < 90000; i++) c.put(i, i); assert.equal(c.get(89999), 89999); assert.equal(c.get(60000), 60000); assert.equal(c.get(59999), undefined); assert.equal(c.get(0), undefined);''')],
 ["Une `Map` itère ses clés dans l'ordre d'insertion : la première clé est la plus ancienne.", "Pour « rafraîchir » une clé : supprime-la puis réinsère-la (elle passe en dernier).", "Pour évincer : `this.entries.keys().next().value` donne la clé la plus ancienne, en O(1)."],
 r'''
export class LRUCache<K, V> {
  private readonly entries = new Map<K, V>(); // ordre d'insertion = du moins au plus récent

  constructor(private readonly capacity: number) {}

  get(key: K): V | undefined {
    if (!this.entries.has(key)) return undefined;
    const value = this.entries.get(key) as V;
    this.entries.delete(key);
    this.entries.set(key, value); // redevient le plus récent
    return value;
  }

  put(key: K, value: V): void {
    this.entries.delete(key);
    this.entries.set(key, value);
    if (this.entries.size > this.capacity) {
      this.entries.delete(this.entries.keys().next().value as K); // évince le plus ancien
    }
  }
}
// get et put : O(1).
''')

algo("algo-promise-pool", "Pool de promesses (concurrence limitée)", H, "Asynchrone · Promesses", 35,
 r"""**Objectif** : exécuter une liste de tâches asynchrones en **limitant le nombre de tâches en cours** (par exemple pour ne pas envoyer 1000 requêtes HTTP d'un coup). Question fréquente en entretien front.

**Exemple**
```ts
const tasks = urls.map((url) => () => fetch(url).then((r) => r.json()));
const results = await promisePool(tasks, 3);
// jamais plus de 3 requêtes simultanées ; results est dans le même ordre que tasks
```

**Contraintes**
• `tasks` est un tableau de fonctions qui **retournent une promesse** (la tâche démarre quand on appelle la fonction) ;
• au plus `limit` tâches s'exécutent en même temps ;
• dès qu'une tâche se termine, la suivante démarre (pas par lots) ;
• les résultats sont renvoyés dans l'ordre des tâches, quel que soit leur ordre de fin ;
• si une tâche échoue, `promisePool` est rejetée avec cette erreur ;
• une liste vide donne `[]`.

**À faire** : implémente `promisePool`.""",
 r'''
export async function promisePool<T>(tasks: Array<() => Promise<T>>, limit: number): Promise<T[]> {
  // TODO
  return [];
}
''',
 [("Résultats dans l'ordre des tâches", r'''const delays = [30, 10, 20]; const tasks = delays.map((d, i) => () => new Promise((r) => setTimeout(() => r(i), d))); assert.deepEqual(await promisePool(tasks, 2), [0, 1, 2]);'''),
  ("Liste vide", r'''assert.deepEqual(await promisePool([], 3), []);'''),
  ("Ne dépasse jamais la limite", r'''let running = 0, max = 0; const tasks = Array.from({ length: 10 }, (_, i) => async () => { running++; max = Math.max(max, running); await new Promise((r) => setTimeout(r, 10)); running--; return i; }); const out = await promisePool(tasks, 3); assert.equal(max, 3); assert.deepEqual(out, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);'''),
  ("Limite supérieure au nombre de tâches", r'''let running = 0, max = 0; const tasks = Array.from({ length: 2 }, (_, i) => async () => { running++; max = Math.max(max, running); await new Promise((r) => setTimeout(r, 10)); running--; return i; }); await promisePool(tasks, 5); assert.equal(max, 2);'''),
  ("Limite 1 : exécution séquentielle", r'''const events = []; const task = (i) => async () => { events.push('start' + i); await new Promise((r) => setTimeout(r, 5)); events.push('end' + i); return i; }; await promisePool([task(0), task(1), task(2)], 1); assert.deepEqual(events, ['start0', 'end0', 'start1', 'end1', 'start2', 'end2']);'''),
  ("La tâche suivante démarre dès qu'une place se libère", r'''const events = []; const task = (i, d) => async () => { events.push('start' + i); await new Promise((r) => setTimeout(r, d)); events.push('end' + i); return i; }; await promisePool([task(0, 80), task(1, 10), task(2, 10), task(3, 10)], 2); assert.ok(events.indexOf('start2') < events.indexOf('end0'), 'la tâche 2 doit démarrer avant la fin de la tâche 0 (pas de traitement par lots)');'''),
  ("Une tâche en échec rejette le pool", r'''const tasks = [async () => 1, async () => { throw new Error('boom'); }, async () => 3]; let message = ''; try { await promisePool(tasks, 2); } catch (e) { message = e.message; } assert.equal(message, 'boom');''')],
 ["Lance `limit` « workers » en parallèle ; chacun répète : prendre la prochaine tâche, l'attendre, ranger son résultat.", "Un compteur partagé `next` indique la prochaine tâche à prendre ; range le résultat à l'index de la tâche pour garder l'ordre.", "`await Promise.all(workers)` attend la fin de tous les workers et propage la première erreur."],
 r'''
export async function promisePool<T>(tasks: Array<() => Promise<T>>, limit: number): Promise<T[]> {
  const results: T[] = new Array(tasks.length);
  let next = 0;

  async function worker(): Promise<void> {
    while (next < tasks.length) {
      const index = next++;
      results[index] = await tasks[index]();
    }
  }

  const workers = Array.from({ length: Math.min(limit, tasks.length) }, worker);
  await Promise.all(workers);
  return results;
}
''')
