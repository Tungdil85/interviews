"""Génère public/data/qcm-{typescript,rxjs,css}.json (questions originales).

Le CSS est ensuite enrichi par scripts/import_fcc_css.py (questions BSD-3 de freeCodeCamp).
"""
import json, pathlib
from qcm_options import finalize

E, M, H = "easy", "medium", "hard"
DATA = pathlib.Path(__file__).resolve().parent.parent / "public/data"

TS = [
(E, "Quelle différence principale entre `unknown` et `any` ?", ["Aucune", "`unknown` oblige à vérifier/restreindre le type avant usage ; `any` désactive le contrôle de type", "`any` est plus sûr", "`unknown` n'existe qu'en JavaScript"], [1],
 "`unknown` est la version sûre de `any` : on doit narrower (typeof, instanceof, garde de type) avant de l'utiliser.", None),
(E, "Quelle syntaxe déclare un tableau de chaînes ?", ["string[]", "Array<string>", "[string]", "string{}"], [0, 1],
 "`string[]` et `Array<string>` sont équivalents. `[string]` est un tuple d'un seul élément.", None),
(M, "Que produit ce type ?", ["{ id?: number; name?: string }", "{ id: number; name: string }", "{ readonly id: number }", "never"], [0],
 "`Partial<T>` rend toutes les propriétés de T optionnelles.", "type User = { id: number; name: string };\ntype T = Partial<User>;"),
(M, "Que fait `Omit<User, 'password'>` ?", ["Supprime le type User", "Crée un type identique à User sans la propriété `password`", "Rend password optionnel", "Ajoute password"], [1],
 "`Omit<T, K>` retire les clés K de T ; `Pick<T, K>` fait l'inverse en ne gardant que K.", None),
(M, "Quel est l'intérêt d'une union discriminée ?", ["Réduire la taille du bundle", "Permettre au compilateur de restreindre le type via une propriété littérale commune (ex. `kind`)", "Éviter les interfaces", "Accélérer l'exécution"], [1],
 "Avec `type Shape = {kind:'c'; r:number} | {kind:'s'; side:number}`, un `switch (shape.kind)` restreint automatiquement le type.", None),
(M, "Quel est le type de `x` ?", ["string", "'a' | 'b'", "readonly ['a','b']", "string[]"], [2],
 "`as const` fige les littéraux et rend le tableau `readonly` avec types littéraux.", "const x = ['a', 'b'] as const;"),
(M, "Que signifie `keyof User` ?", ["Les valeurs de User", "L'union des noms de propriétés de User", "Une clé de chiffrement", "Le constructeur"], [1],
 "Si `User = {id:number; name:string}`, alors `keyof User` vaut `'id' | 'name'`.", None),
(M, "Quand préférer `interface` à `type` ?", ["Jamais", "Pour décrire la forme d'objets extensibles (extends, fusion de déclarations)", "Pour les unions", "Pour les tuples uniquement"], [1],
 "Les deux se recoupent largement ; `type` est nécessaire pour unions/tuples/mapped types, `interface` pour l'héritage et la fusion de déclarations.", None),
(H, "À quoi sert l'opérateur `satisfies` ?", ["À caster sans vérification", "À valider qu'une valeur respecte un type tout en conservant son type inféré précis", "À importer un type", "À déclarer une classe"], [1],
 "`const c = {...} satisfies Config` vérifie la conformité sans élargir le type (contrairement à une annotation).", None),
(M, "Que retourne cette fonction de garde ?", ["boolean simple, sans effet sur le typage", "boolean, et restreint `v` à string dans la branche vraie", "string", "void"], [1],
 "Un prédicat de type (`v is string`) informe le compilateur du narrowing.", "function isString(v: unknown): v is string {\n  return typeof v === 'string';\n}"),
(E, "Que fait l'opérateur `?.` ?", ["Déclare une propriété optionnelle", "Évalue à undefined si la valeur à gauche est null/undefined au lieu de lever une erreur", "Compare deux valeurs", "Force le type non-null"], [1],
 "L'optional chaining court-circuite : `user?.address?.city`.", None),
(M, "Que fait l'opérateur `!` en suffixe (`value!`) ?", ["Nie la valeur", "Affirme au compilateur que la valeur n'est ni null ni undefined, sans aucune vérification à l'exécution", "Convertit en booléen", "Lance une erreur si null"], [1],
 "Le non-null assertion supprime l'erreur de compilation mais n'ajoute aucun contrôle runtime : à utiliser avec parcimonie.", None),
(M, "Que décrit `Record<string, number>` ?", ["Un tableau de nombres", "Un objet dont toutes les clés sont des chaînes et les valeurs des nombres", "Un tuple", "Une classe"], [1],
 "`Record<K, V>` est un mapped type : `{ [P in K]: V }`.", None),
(H, "Que signifie le type `never` ?", ["Une valeur qui peut être null", "Le type des valeurs qui n'existent jamais (fonction qui ne retourne pas, cas exhaustif impossible)", "Identique à void", "Un alias de unknown"], [1],
 "`never` sert aux fonctions qui lèvent une exception en permanence et aux vérifications d'exhaustivité d'un switch.", None),
(E, "Quelle option tsconfig active l'ensemble des vérifications strictes ?", ["\"strict\": true", "\"safe\": true", "\"lint\": true", "\"noAny\": true"], [0],
 "`strict` active notamment `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `strictPropertyInitialization`.", None),
]

RX = [
(M, "Quelle différence entre `switchMap` et `mergeMap` ?", ["Aucune", "switchMap annule l'Observable interne précédent à chaque nouvelle valeur ; mergeMap les exécute en parallèle", "mergeMap annule les précédents", "switchMap est synchrone"], [1],
 "`switchMap` convient aux recherches (annuler la requête obsolète) ; `mergeMap` aux traitements parallèles indépendants.", None),
(M, "Quel opérateur choisir pour exécuter des requêtes en série dans l'ordre ?", ["switchMap", "concatMap", "exhaustMap", "mergeMap"], [1],
 "`concatMap` met en file : chaque interne attend la fin du précédent, l'ordre est conservé.", None),
(M, "Que fait `exhaustMap` ?", ["Ignore les nouvelles valeurs tant que l'Observable interne courant n'est pas terminé", "Annule l'interne courant", "Fusionne tout", "Épuise la mémoire"], [0],
 "Typique du clic « Se connecter » : on ignore les clics tant que la requête est en cours.", None),
(E, "Quelle différence entre `Subject` et `BehaviorSubject` ?", ["Aucune", "BehaviorSubject a une valeur initiale et émet immédiatement sa dernière valeur à tout nouvel abonné", "Subject conserve la dernière valeur", "BehaviorSubject n'émet qu'une fois"], [1],
 "`BehaviorSubject` possède toujours une valeur courante (`.value`). `ReplaySubject(n)` rejoue les n dernières.", None),
(M, "Un Observable « cold » signifie que…", ["Il n'émet jamais", "Chaque abonnement déclenche sa propre exécution du producteur", "Il partage une seule source", "Il est terminé"], [1],
 "Un HTTP via HttpClient est cold : chaque `subscribe` refait la requête. `share`/`shareReplay` rendent « hot » en partageant.", None),
(M, "Quel est l'effet de `shareReplay(1)` ?", ["Relance la source à chaque abonné", "Partage une seule souscription à la source et rejoue la dernière valeur aux nouveaux abonnés", "Supprime les doublons", "Retarde l'émission"], [1],
 "Utile pour mettre en cache le résultat d'un appel HTTP partagé par plusieurs consommateurs.", None),
(M, "Quand `forkJoin` émet-il ?", ["À chaque valeur de n'importe quelle source", "Une seule fois, quand toutes les sources sont terminées, avec leur dernière valeur chacune", "Dès la première source", "Jamais"], [1],
 "`forkJoin([a$, b$])` ≈ `Promise.all` ; `combineLatest` émet à chaque changement après que chaque source a émis une fois.", None),
(E, "Quel opérateur attend une pause dans les émissions avant de laisser passer la dernière valeur ?", ["throttleTime", "debounceTime", "delay", "sampleTime"], [1],
 "`debounceTime(300)` est classique pour la saisie utilisateur dans un champ de recherche.", None),
(E, "À quoi sert `distinctUntilChanged` ?", ["À trier", "À ignorer une valeur identique à la précédente", "À supprimer tous les doublons de la séquence", "À terminer le flux"], [1],
 "Il ne compare qu'avec la valeur immédiatement précédente (comparateur personnalisable).", None),
(M, "Comment gérer une erreur HTTP sans interrompre le flux principal d'un switchMap ?", ["try/catch autour du subscribe", "catchError à l'intérieur du Observable interne, retournant of(valeurDeRepli)", "Ignorer l'erreur", "Utiliser Subject"], [1],
 "Placer `catchError` dans l'Observable interne évite que l'erreur ne termine le flux externe.", "search$.pipe(\n  switchMap(q => http.get(url, { params: { q } }).pipe(\n    catchError(() => of([]))\n  ))\n)"),
(M, "Que fait `takeUntil(destroy$)` ?", ["Prend la première valeur", "Termine l'abonnement quand destroy$ émet", "Retarde jusqu'à destroy$", "Filtre les valeurs"], [1],
 "Pattern historique de désabonnement ; aujourd'hui remplaçable par `takeUntilDestroyed()`.", None),
(M, "Quelle différence entre `combineLatest` et `withLatestFrom` ?", ["Aucune", "withLatestFrom n'émet que quand la source principale émet, en prenant la dernière valeur de l'autre", "combineLatest n'émet qu'une fois", "withLatestFrom est asynchrone"], [1],
 "`a$.pipe(withLatestFrom(b$))` est déclenché par a$ seulement ; `combineLatest` par n'importe laquelle.", None),
(E, "Que fait l'opérateur `tap` ?", ["Transforme les valeurs", "Exécute un effet de bord (log…) sans modifier le flux", "Filtre", "Complète le flux"], [1],
 "`tap` est transparent pour les valeurs émises.", None),
(H, "Quelle est la conséquence de ne pas se désabonner d'un `interval(1000)` dans un composant détruit ?", ["Aucune", "Le timer continue de tourner et le callback reste référencé : fuite mémoire et effets indésirables", "Angular le stoppe seul", "Une erreur de compilation"], [1],
 "Les Observables infinis exigent un désabonnement explicite (`takeUntilDestroyed`, `async` pipe, `unsubscribe`).", None),
(M, "Quelle différence entre `of(1,2,3)` et `from([1,2,3])` ?", ["`of` émet chaque argument ; `from` convertit une source itérable/Promise en Observable (ici émet aussi 1,2,3)", "of est asynchrone", "from ne gère que les Promises", "Aucune pour un tableau passé sans spread"], [0],
 "`of([1,2,3])` émettrait le tableau entier ; `from([1,2,3])` émet 1, 2, 3. Les deux émettent ici de façon synchrone.", None),
]

CSS = [
(E, "Quel effet a `box-sizing: border-box` ?", ["Le padding et la bordure sont inclus dans la largeur/hauteur déclarée", "Le padding s'ajoute à la largeur", "Supprime les marges", "Ajoute une bordure"], [0],
 "Avec `border-box`, `width: 200px` inclut padding et border : le dimensionnement est plus prévisible.", None),
(M, "Quel sélecteur a la plus forte spécificité ?", ["`.card .title`", "`#title`", "`div p`", "`p.title`"], [1],
 "Spécificité (id, classe/attribut/pseudo-classe, élément) : `#title` = (1,0,0) l'emporte sur `.card .title` (0,2,0).", None),
(E, "Comment centrer un élément enfant horizontalement ET verticalement avec flexbox ?", ["justify-content: center; align-items: center;", "text-align: center;", "margin: 0 auto;", "float: center;"], [0],
 "Sur le conteneur : `display:flex; justify-content:center; align-items:center;`. Avec Grid : `place-items:center`.", None),
(M, "Que fait `flex: 1` sur un élément flex ?", ["Fixe la largeur à 1px", "Équivaut à flex-grow:1 ; flex-shrink:1 ; flex-basis:0%, l'élément occupe l'espace disponible", "Désactive flex", "Fait passer à la ligne"], [1],
 "`flex: 1` répartit l'espace restant de manière égale entre éléments partageant cette valeur.", None),
(M, "Quelle propriété crée des colonnes de tailles proportionnelles avec Grid ?", ["grid-template-columns: 1fr 2fr", "columns: 1fr 2fr", "flex-columns", "grid-gap"], [0],
 "L'unité `fr` répartit l'espace libre : ici 1/3 et 2/3.", None),
(E, "Quelle position retire l'élément du flux et le place par rapport à son ancêtre positionné le plus proche ?", ["static", "relative", "absolute", "sticky"], [2],
 "`absolute` se positionne par rapport au plus proche ancêtre non `static` (souvent `position: relative`).", None),
(M, "`position: sticky` …", ["Fixe l'élément définitivement à l'écran", "Se comporte comme relative puis « colle » au seuil défini (top…) pendant le défilement de son conteneur", "Supprime l'élément du flux", "Équivaut à absolute"], [1],
 "Sticky = relative jusqu'à un seuil de scroll, puis fixed dans les limites de son parent.", None),
(H, "Pourquoi un `z-index` élevé peut-il ne pas passer au-dessus d'un autre élément ?", ["Le z-index n'existe plus", "Les contextes d'empilement (stacking contexts) isolent les z-index de leurs descendants", "Il faut utiliser !important", "Il faut utiliser opacity:1"], [1],
 "Un parent avec `position + z-index`, `transform`, `opacity<1`, etc. crée un contexte : ses enfants ne peuvent pas sortir de ce niveau.", None),
(E, "`em` et `rem` : quelle différence ?", ["Aucune", "`em` est relatif à la taille de police de l'élément (ou parent) ; `rem` à celle de la racine `<html>`", "`rem` est relatif au parent", "`em` vaut toujours 16px"], [1],
 "`rem` évite l'effet de composition des `em` imbriqués et facilite l'accessibilité.", None),
(E, "Comment cibler les écrans d'au moins 768px (mobile-first) ?", ["@media (min-width: 768px)", "@media (max-width: 768px)", "@screen 768", "@viewport 768"], [0],
 "Approche mobile-first : styles de base pour petit écran, puis `min-width` pour élargir.", None),
(M, "Différence entre `:hover` et `::before` ?", ["Aucune", "`:hover` est une pseudo-classe (état) ; `::before` est un pseudo-élément (contenu généré)", "`::before` est un état", "Les deux sont des pseudo-éléments"], [1],
 "Une pseudo-classe cible un état d'un élément existant (un seul `:`), un pseudo-élément une partie générée (`::`).", None),
(M, "Que fait `display: none` par rapport à `visibility: hidden` ?", ["Idem", "`none` retire l'élément du flux (aucun espace), `hidden` le cache mais conserve son espace", "`hidden` retire l'élément du DOM", "`none` conserve l'espace"], [1],
 "`opacity: 0` cache aussi mais l'élément reste interactif ; `display:none` est ignoré des lecteurs d'écran.", None),
(M, "Comment déclare-t-on et utilise-t-on une variable CSS ?", ["--gap: 8px; puis var(--gap)", "$gap: 8px; puis $gap", "@gap: 8px;", "let gap = 8px"], [0],
 "Les custom properties se déclarent avec `--nom` et s'héritent via la cascade ; `var(--nom, fallback)`.", None),
(M, "Que fait `clamp(1rem, 2.5vw, 2rem)` ?", ["Découpe l'élément", "Retourne une valeur fluide bornée entre un minimum (1rem) et un maximum (2rem)", "Arrondit", "Active une animation"], [1],
 "Pratique pour une typographie fluide sans media queries.", None),
(H, "Qu'est-ce que l'effondrement des marges (margin collapsing) ?", ["Une marge supprimée par erreur", "Les marges verticales adjacentes de blocs en flux normal fusionnent en prenant la plus grande", "Un bug de Grid", "Un reset CSS"], [1],
 "Ne s'applique pas aux éléments flex/grid ni aux blocs créant un nouveau contexte de formatage (BFC).", None),
(H, "Quelles propriétés sont les plus performantes à animer ?", ["width et height", "transform et opacity", "top et left", "margin"], [1],
 "`transform` et `opacity` peuvent être animées par le compositeur GPU sans relayout/repaint coûteux.", None),
(M, "Que fait `gap` en Flex ou Grid ?", ["Ajoute des marges aux bords", "Définit l'espacement entre les éléments enfants", "Supprime les bordures", "Aligne verticalement"], [1],
 "`gap` n'ajoute pas d'espace avant le premier ni après le dernier élément, contrairement aux marges.", None),
(H, "À quoi servent les container queries (`@container`) ?", ["À styler selon la taille du conteneur parent plutôt que celle du viewport", "À conteneuriser Docker", "À remplacer Grid", "À imprimer"], [0],
 "Le composant s'adapte à l'espace dont il dispose (`container-type: inline-size`), indépendamment de la page.", None),
(M, "Que fait `object-fit: cover` sur une image ?", ["Étire l'image", "Remplit la boîte en conservant le ratio, en rognant l'excédent", "Réduit sans rogner", "Masque l'image"], [1],
 "`contain` conserve l'image entière avec éventuelles bandes vides ; `cover` remplit en rognant.", None),
(H, "Quelle est la différence entre `:is()` et `:where()` ?", ["Aucune", "`:where()` a une spécificité de 0 ; `:is()` prend celle de son argument le plus spécifique", "`:is()` est déprécié", "`:where()` ne supporte pas les listes"], [1],
 "`:where()` est idéal pour des styles de base faciles à surcharger.", None),
]

def dump(name, items, prefix, cat):
    out = []
    for i, (d, q, opts, ans, expl, code) in enumerate(items, 1):
        item = {"id": f"{prefix}-{i:03d}", "category": cat, "difficulty": d, "question": q}
        if code: item["code"] = code
        item.update({"options": opts, "answer": ans, "explanation": expl})
        out.append(finalize(item))
    (DATA / f"qcm-{name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(name, len(out))

dump("typescript", TS, "ts", "typescript")
dump("rxjs", RX, "rx", "rxjs")
dump("css", CSS, "css", "css")
