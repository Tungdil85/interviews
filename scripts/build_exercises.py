"""Génère public/data/exercises.json (exercices originaux, JavaScript).

Chaque test est le corps d'une fonction async qui voit le code de l'utilisateur et reçoit `assert`.
exercises.data.spec.ts vérifie que chaque solution passe tous les tests et que le code de départ échoue.
"""
import json, pathlib

E, M, H = "easy", "medium", "hard"
X = []
def ex(id, title, diff, topic, desc, starter, tests, hints, solution):
    X.append({"id": id, "title": title, "difficulty": diff, "topic": topic, "description": desc,
              "starterCode": starter, "tests": [{"name": n, "code": c} for n, c in tests],
              "hints": hints, "solution": solution})

ex("to-selector", "Nom de classe → sélecteur", E, "Angular / chaînes",
 "Angular génère des sélecteurs en kebab-case. Écris `toSelector(className)` qui transforme 'MyAwesomeCmp' en 'my-awesome-cmp'.",
 "function toSelector(className) {\n  // TODO\n}\n",
 [("Cas simple", "assert.equal(toSelector('MyAwesomeCmp'), 'my-awesome-cmp')"),
  ("Un seul mot", "assert.equal(toSelector('Header'), 'header')"),
  ("Déjà en minuscules", "assert.equal(toSelector('app'), 'app')")],
 ["Insère un tiret avant chaque majuscule qui n'est pas en première position.", "Une regex avec replace(/([a-z])([A-Z])/g, ...) fait l'essentiel."],
 "function toSelector(className) {\n  return className.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();\n}\n")

ex("parse-query", "Parser des query params", E, "Routing",
 "Écris `parseQuery(qs)` qui transforme 'a=1&b=hello&c=' (avec ou sans '?' initial) en objet { a: '1', b: 'hello', c: '' }. Les valeurs sont décodées avec decodeURIComponent.",
 "function parseQuery(qs) {\n  // TODO\n}\n",
 [("Cas simple", "assert.deepEqual(parseQuery('a=1&b=hello'), { a: '1', b: 'hello' })"),
  ("Ignore le ? initial", "assert.deepEqual(parseQuery('?x=2'), { x: '2' })"),
  ("Valeur vide", "assert.deepEqual(parseQuery('c='), { c: '' })"),
  ("Décodage", "assert.deepEqual(parseQuery('q=a%20b'), { q: 'a b' })"),
  ("Chaîne vide", "assert.deepEqual(parseQuery(''), {})")],
 ["Retire le '?' avec replace(/^\\?/, '').", "split('&') puis split('=') sur chaque paire."],
 "function parseQuery(qs) {\n  const result = {};\n  const clean = qs.replace(/^\\?/, '');\n  if (!clean) return result;\n  for (const pair of clean.split('&')) {\n    const [key, value = ''] = pair.split('=');\n    result[decodeURIComponent(key)] = decodeURIComponent(value);\n  }\n  return result;\n}\n")

ex("flatten", "Aplatir un tableau", E, "JavaScript",
 "Écris `flatten(arr)` qui aplatit récursivement un tableau imbriqué, sans utiliser Array.prototype.flat. flatten([1,[2,[3,[4]]]]) → [1,2,3,4].",
 "function flatten(arr) {\n  // TODO\n}\n",
 [("Imbrication profonde", "assert.deepEqual(flatten([1,[2,[3,[4]]]]), [1,2,3,4])"),
  ("Déjà plat", "assert.deepEqual(flatten([1,2]), [1,2])"),
  ("Vide", "assert.deepEqual(flatten([]), [])"),
  ("Sans flat natif", "const orig = Array.prototype.flat; Array.prototype.flat = () => { throw new Error('flat interdit'); }; try { assert.deepEqual(flatten([1,[2]]), [1,2]); } finally { Array.prototype.flat = orig; }")],
 ["Parcours avec reduce et teste Array.isArray.", "Appelle flatten récursivement sur les sous-tableaux."],
 "function flatten(arr) {\n  return arr.reduce((acc, item) => acc.concat(Array.isArray(item) ? flatten(item) : item), []);\n}\n")

ex("group-by", "groupBy", E, "JavaScript",
 "Écris `groupBy(items, keyFn)` qui retourne un objet regroupant les éléments selon la clé calculée. groupBy([1,2,3,4], n => n % 2 ? 'impair' : 'pair') → { impair: [1,3], pair: [2,4] }.",
 "function groupBy(items, keyFn) {\n  // TODO\n}\n",
 [("Pair / impair", "assert.deepEqual(groupBy([1,2,3,4], n => n % 2 ? 'impair' : 'pair'), { impair: [1,3], pair: [2,4] })"),
  ("Par propriété", "assert.deepEqual(groupBy([{t:'a'},{t:'b'},{t:'a'}], o => o.t), { a: [{t:'a'},{t:'a'}], b: [{t:'b'}] })"),
  ("Liste vide", "assert.deepEqual(groupBy([], x => x), {})")],
 ["reduce avec un objet accumulateur.", "Initialise acc[key] à [] si elle n'existe pas."],
 "function groupBy(items, keyFn) {\n  return items.reduce((acc, item) => {\n    const key = keyFn(item);\n    (acc[key] ??= []).push(item);\n    return acc;\n  }, {});\n}\n")

ex("pipe", "Composer des fonctions (pipe)", E, "Programmation fonctionnelle",
 "Écris `pipe(...fns)` qui retourne une fonction appliquant les fonctions de gauche à droite : pipe(f, g)(x) = g(f(x)). Comme l'opérateur pipe de RxJS, version synchrone.",
 "function pipe(...fns) {\n  // TODO\n}\n",
 [("Deux fonctions", "assert.equal(pipe(x => x + 1, x => x * 2)(3), 8)"),
  ("Aucune fonction : identité", "assert.equal(pipe()(5), 5)"),
  ("Ordre gauche → droite", "assert.equal(pipe(s => s + 'a', s => s + 'b')(''), 'ab')")],
 ["reduce sur la liste des fonctions avec la valeur initiale en accumulateur."],
 "function pipe(...fns) {\n  return (input) => fns.reduce((acc, fn) => fn(acc), input);\n}\n")

ex("memoize", "memoize", M, "Performance",
 "Écris `memoize(fn)` qui met en cache le résultat de fn selon ses arguments (ils sont tous sérialisables en JSON). fn ne doit être appelée qu'une fois par jeu d'arguments.",
 "function memoize(fn) {\n  // TODO\n}\n",
 [("Résultat correct", "const f = memoize((a,b) => a + b); assert.equal(f(1,2), 3)"),
  ("Mise en cache", "let calls = 0; const f = memoize(x => { calls++; return x * 2; }); f(2); f(2); f(3); assert.equal(calls, 2)"),
  ("Arguments multiples distincts", "let calls = 0; const f = memoize((a,b) => { calls++; return a + b; }); f(1,2); f(2,1); assert.equal(calls, 2)"),
  ("Cache aussi les valeurs falsy", "let calls = 0; const f = memoize(() => { calls++; return 0; }); f(); f(); assert.equal(calls, 1)")],
 ["Utilise une Map dont la clé est JSON.stringify(args).", "Teste cache.has(key) plutôt que la valeur (0 est falsy)."],
 "function memoize(fn) {\n  const cache = new Map();\n  return (...args) => {\n    const key = JSON.stringify(args);\n    if (!cache.has(key)) cache.set(key, fn(...args));\n    return cache.get(key);\n  };\n}\n")

ex("debounce", "debounce", M, "RxJS / Performance",
 "Écris `debounce(fn, ms)` : la fonction retournée n'appelle fn qu'après ms millisecondes sans nouvel appel, avec les derniers arguments (comme debounceTime sur une saisie).",
 "function debounce(fn, ms) {\n  // TODO\n}\n",
 [("Un seul appel après rafale", "let calls = []; const d = debounce(v => calls.push(v), 30); d(1); d(2); d(3); await new Promise(r => setTimeout(r, 80)); assert.deepEqual(calls, [3])"),
  ("Pas d'appel immédiat", "let called = false; const d = debounce(() => { called = true; }, 30); d(); assert.equal(called, false); await new Promise(r => setTimeout(r, 80)); assert.equal(called, true)"),
  ("Appels espacés = plusieurs exécutions", "let n = 0; const d = debounce(() => n++, 20); d(); await new Promise(r => setTimeout(r, 60)); d(); await new Promise(r => setTimeout(r, 60)); assert.equal(n, 2)")],
 ["Garde l'identifiant du timer dans une variable de closure.", "clearTimeout avant chaque nouveau setTimeout."],
 "function debounce(fn, ms) {\n  let timer;\n  return (...args) => {\n    clearTimeout(timer);\n    timer = setTimeout(() => fn(...args), ms);\n  };\n}\n")

ex("event-emitter", "EventEmitter (comme @Output)", M, "Angular / Patterns",
 "Implémente la classe `EventEmitter` avec `on(event, handler)`, `off(event, handler)` et `emit(event, ...args)`. `on` retourne une fonction de désabonnement. Un événement sans écouteur ne doit pas lever d'erreur.",
 "class EventEmitter {\n  // TODO\n}\n",
 [("on + emit", "const e = new EventEmitter(); const got = []; e.on('x', v => got.push(v)); e.emit('x', 1); e.emit('x', 2); assert.deepEqual(got, [1,2])"),
  ("off", "const e = new EventEmitter(); let n = 0; const h = () => n++; e.on('x', h); e.off('x', h); e.emit('x'); assert.equal(n, 0)"),
  ("on retourne unsubscribe", "const e = new EventEmitter(); let n = 0; const un = e.on('x', () => n++); e.emit('x'); un(); e.emit('x'); assert.equal(n, 1)"),
  ("Plusieurs écouteurs", "const e = new EventEmitter(); let n = 0; e.on('x', () => n++); e.on('x', () => n++); e.emit('x'); assert.equal(n, 2)"),
  ("Événement inconnu", "const e = new EventEmitter(); e.emit('rien'); assert.ok(true)")],
 ["Stocke un Map<string, Set<Function>>.", "emit : boucle sur le Set s'il existe."],
 "class EventEmitter {\n  #handlers = new Map();\n  on(event, handler) {\n    if (!this.#handlers.has(event)) this.#handlers.set(event, new Set());\n    this.#handlers.get(event).add(handler);\n    return () => this.off(event, handler);\n  }\n  off(event, handler) {\n    this.#handlers.get(event)?.delete(handler);\n  }\n  emit(event, ...args) {\n    this.#handlers.get(event)?.forEach((h) => h(...args));\n  }\n}\n")

ex("mini-signal", "Mini signal", M, "Angular / Signals",
 "Implémente `signal(initial)` qui retourne une fonction getter : s() lit la valeur, s.set(v) la remplace et s.update(fn) la calcule depuis l'ancienne. Implémente aussi `computed(fn)` retournant un getter qui recalcule fn() à chaque lecture (version simplifiée).",
 "function signal(initial) {\n  // TODO\n}\n\nfunction computed(fn) {\n  // TODO\n}\n",
 [("Lecture initiale", "assert.equal(signal(5)(), 5)"),
  ("set", "const s = signal(1); s.set(2); assert.equal(s(), 2)"),
  ("update", "const s = signal(1); s.update(v => v + 10); assert.equal(s(), 11)"),
  ("computed suit le signal", "const a = signal(2); const double = computed(() => a() * 2); assert.equal(double(), 4); a.set(5); assert.equal(double(), 10)")],
 ["Garde la valeur dans une variable de closure et attache set/update à la fonction getter (Object.assign).", "computed(fn) peut simplement retourner fn."],
 "function signal(initial) {\n  let value = initial;\n  const getter = () => value;\n  getter.set = (v) => { value = v; };\n  getter.update = (fn) => { value = fn(value); };\n  return getter;\n}\n\nfunction computed(fn) {\n  return () => fn();\n}\n")

ex("behavior-subject", "BehaviorSubject", M, "RxJS",
 "Implémente `BehaviorSubject` : constructeur(initial), propriété/getter `value`, `next(v)`, et `subscribe(observer)` qui appelle immédiatement observer avec la valeur courante, puis à chaque next. subscribe retourne une fonction de désabonnement.",
 "class BehaviorSubject {\n  // TODO\n}\n",
 [("Émet la valeur initiale à l'abonnement", "const s = new BehaviorSubject(1); const got = []; s.subscribe(v => got.push(v)); assert.deepEqual(got, [1])"),
  ("Émet les next suivants", "const s = new BehaviorSubject(0); const got = []; s.subscribe(v => got.push(v)); s.next(1); s.next(2); assert.deepEqual(got, [0,1,2])"),
  ("value reflète la dernière valeur", "const s = new BehaviorSubject('a'); s.next('b'); assert.equal(s.value, 'b')"),
  ("Nouvel abonné reçoit la dernière valeur", "const s = new BehaviorSubject(0); s.next(9); const got = []; s.subscribe(v => got.push(v)); assert.deepEqual(got, [9])"),
  ("Désabonnement", "const s = new BehaviorSubject(0); const got = []; const un = s.subscribe(v => got.push(v)); un(); s.next(1); assert.deepEqual(got, [0])")],
 ["Garde un Set d'observers.", "Dans subscribe : appelle observer(this.value) avant de retourner la fonction de désabonnement."],
 "class BehaviorSubject {\n  #value;\n  #observers = new Set();\n  constructor(initial) { this.#value = initial; }\n  get value() { return this.#value; }\n  next(v) {\n    this.#value = v;\n    this.#observers.forEach((o) => o(v));\n  }\n  subscribe(observer) {\n    this.#observers.add(observer);\n    observer(this.#value);\n    return () => this.#observers.delete(observer);\n  }\n}\n")

ex("di-container", "Conteneur d'injection", H, "Angular / DI",
 "Implémente `Container` avec `register(token, factory)` et `resolve(token)`. Chaque service est un singleton (la factory n'est appelée qu'une fois). La factory reçoit le container pour résoudre ses dépendances. Résoudre un token inconnu lève une erreur, et une dépendance circulaire aussi.",
 "class Container {\n  // TODO\n}\n",
 [("Résolution simple", "const c = new Container(); c.register('a', () => 1); assert.equal(c.resolve('a'), 1)"),
  ("Singleton", "const c = new Container(); let n = 0; c.register('a', () => ({ id: ++n })); assert.equal(c.resolve('a'), c.resolve('a')); assert.equal(n, 1)"),
  ("Dépendances", "const c = new Container(); c.register('cfg', () => ({ url: 'x' })); c.register('http', (ct) => ({ base: ct.resolve('cfg').url })); assert.equal(c.resolve('http').base, 'x')"),
  ("Token inconnu", "const c = new Container(); assert.throws(() => c.resolve('nope'))"),
  ("Dépendance circulaire", "const c = new Container(); c.register('a', (ct) => ct.resolve('b')); c.register('b', (ct) => ct.resolve('a')); assert.throws(() => c.resolve('a'))")],
 ["Deux Map : factories et instances.", "Pour détecter la circularité, garde un Set des tokens en cours de résolution."],
 "class Container {\n  #factories = new Map();\n  #instances = new Map();\n  #resolving = new Set();\n  register(token, factory) {\n    this.#factories.set(token, factory);\n  }\n  resolve(token) {\n    if (this.#instances.has(token)) return this.#instances.get(token);\n    const factory = this.#factories.get(token);\n    if (!factory) throw new Error('Token inconnu : ' + String(token));\n    if (this.#resolving.has(token)) throw new Error('Dépendance circulaire : ' + String(token));\n    this.#resolving.add(token);\n    try {\n      const instance = factory(this);\n      this.#instances.set(token, instance);\n      return instance;\n    } finally {\n      this.#resolving.delete(token);\n    }\n  }\n}\n")

ex("mini-observable", "Mini Observable + map", H, "RxJS",
 "Implémente la classe `Observable` : constructeur(subscribeFn) où subscribeFn(observer) peut retourner une fonction de nettoyage ; `subscribe(next)` retourne une fonction de désabonnement qui appelle ce nettoyage ; `pipe(...operators)` applique des opérateurs (fonctions Observable → Observable). Écris aussi l'opérateur `map(fn)`.",
 "class Observable {\n  // TODO\n}\n\nfunction map(fn) {\n  // TODO\n}\n",
 [("subscribe reçoit les valeurs", "const got = []; new Observable(o => { o.next(1); o.next(2); }).subscribe(v => got.push(v)); assert.deepEqual(got, [1,2])"),
  ("map", "const got = []; new Observable(o => { o.next(1); o.next(2); }).pipe(map(x => x * 10)).subscribe(v => got.push(v)); assert.deepEqual(got, [10,20])"),
  ("pipe enchaîne les opérateurs", "const got = []; new Observable(o => o.next(2)).pipe(map(x => x + 1), map(x => x * 2)).subscribe(v => got.push(v)); assert.deepEqual(got, [6])"),
  ("Désabonnement appelle le nettoyage", "let cleaned = false; const un = new Observable(() => () => { cleaned = true; }).subscribe(() => {}); assert.equal(cleaned, false); un(); assert.equal(cleaned, true)"),
  ("Cold : chaque abonnement relance la source", "let runs = 0; const o = new Observable(ob => { runs++; ob.next(1); }); o.subscribe(() => {}); o.subscribe(() => {}); assert.equal(runs, 2)")],
 ["L'observer passé à subscribeFn est { next }.", "pipe : operators.reduce((source, op) => op(source), this).", "map(fn) retourne source => new Observable(o => source.subscribe(v => o.next(fn(v))))."],
 "class Observable {\n  constructor(subscribeFn) { this._subscribe = subscribeFn; }\n  subscribe(next) {\n    const cleanup = this._subscribe({ next });\n    return () => { if (typeof cleanup === 'function') cleanup(); };\n  }\n  pipe(...operators) {\n    return operators.reduce((source, op) => op(source), this);\n  }\n}\n\nfunction map(fn) {\n  return (source) => new Observable((observer) => {\n    const unsubscribe = source.subscribe((v) => observer.next(fn(v)));\n    return unsubscribe;\n  });\n}\n")

ex("brackets", "Parenthèses équilibrées", M, "Algorithmique",
 "Écris `isBalanced(str)` qui retourne true si les (), [] et {} sont correctement fermés et imbriqués (les autres caractères sont ignorés). Utile pour valider un template !",
 "function isBalanced(str) {\n  // TODO\n}\n",
 [("Équilibré", "assert.equal(isBalanced('{[()]}'), true)"),
  ("Mauvais ordre", "assert.equal(isBalanced('([)]'), false)"),
  ("Fermeture manquante", "assert.equal(isBalanced('(('), false)"),
  ("Fermeture en trop", "assert.equal(isBalanced('())'), false)"),
  ("Texte ignoré", "assert.equal(isBalanced('a(b[c]{d})e'), true)"),
  ("Chaîne vide", "assert.equal(isBalanced(''), true)")],
 ["Utilise une pile (tableau).", "À chaque fermant, le dernier ouvrant empilé doit correspondre."],
 "function isBalanced(str) {\n  const pairs = { ')': '(', ']': '[', '}': '{' };\n  const stack = [];\n  for (const ch of str) {\n    if ('([{'.includes(ch)) stack.push(ch);\n    else if (ch in pairs && stack.pop() !== pairs[ch]) return false;\n  }\n  return stack.length === 0;\n}\n")

ex("chunk", "Découper en lots", E, "JavaScript",
 "Écris `chunk(arr, size)` qui découpe un tableau en sous-tableaux de taille size (le dernier peut être plus court). chunk([1,2,3,4,5], 2) → [[1,2],[3,4],[5]]. Utile pour la pagination.",
 "function chunk(arr, size) {\n  // TODO\n}\n",
 [("Reste", "assert.deepEqual(chunk([1,2,3,4,5], 2), [[1,2],[3,4],[5]])"),
  ("Taille multiple", "assert.deepEqual(chunk([1,2,3,4], 2), [[1,2],[3,4]])"),
  ("Taille supérieure", "assert.deepEqual(chunk([1,2], 5), [[1,2]])"),
  ("Vide", "assert.deepEqual(chunk([], 3), [])"),
  ("Ne modifie pas l'entrée", "const a = [1,2,3]; chunk(a, 2); assert.deepEqual(a, [1,2,3])")],
 ["Boucle avec un pas de size et slice(i, i + size)."],
 "function chunk(arr, size) {\n  const result = [];\n  for (let i = 0; i < arr.length; i += size) result.push(arr.slice(i, i + size));\n  return result;\n}\n")

ex("deep-equal-immutable", "Mise à jour immuable", M, "Angular / Signals & NgRx",
 "Avec OnPush et les signaux, on met l'état à jour de façon immuable. Écris `updateTodo(state, id, patch)` qui retourne un NOUVEL état { todos: [...] } où le todo d'identifiant id est fusionné avec patch, sans muter l'état d'origine ni les todos non concernés (ils gardent la même référence).",
 "function updateTodo(state, id, patch) {\n  // TODO\n}\n",
 [("Fusionne le patch", "const s = { todos: [{id:1,done:false},{id:2,done:false}] }; const n = updateTodo(s, 2, { done: true }); assert.deepEqual(n.todos[1], { id: 2, done: true })"),
  ("Ne mute pas l'original", "const s = { todos: [{id:1,done:false}] }; updateTodo(s, 1, { done: true }); assert.equal(s.todos[0].done, false)"),
  ("Nouvelle référence d'état", "const s = { todos: [{id:1}] }; assert.ok(updateTodo(s, 1, {}) !== s)"),
  ("Todos inchangés conservent leur référence", "const s = { todos: [{id:1},{id:2}] }; const n = updateTodo(s, 2, { x: 1 }); assert.ok(n.todos[0] === s.todos[0])")],
 ["map sur state.todos : retourne {...todo, ...patch} seulement si todo.id === id."],
 "function updateTodo(state, id, patch) {\n  return { ...state, todos: state.todos.map((t) => (t.id === id ? { ...t, ...patch } : t)) };\n}\n")

pathlib.Path(__file__).resolve().parent.parent.joinpath("public/data/exercises.json").write_text(
    json.dumps(X, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(X), "exercices")
