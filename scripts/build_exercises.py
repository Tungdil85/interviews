"""Génère public/data/exercises.json : exercices Angular concrets (pipe, composant, directive, service…).

Le code de départ et la solution sont du TypeScript Angular réel, compilé dans le navigateur (JIT).
Chaque test est le corps d'une fonction async qui voit le code de l'utilisateur et reçoit
`assert`, `render(template | Composant, options)`, `createInjector(providers)` et `wait(ms)`.
exercises.data.spec.ts vérifie que chaque solution passe tous les tests et que le départ en échoue.
"""
import json, pathlib
from algo_exercises import ALGOS

E, M, H = "easy", "medium", "hard"
X = []
# ───────────────────────── Consignes ─────────────────────────
# Mini-format affiché par la page : **gras**, `code`, blocs ```…```, listes « • ».
# Chaque consigne suit le même plan : objectif · exemple d'utilisation · résultat attendu · à faire.
DESCRIPTIONS = {
"pipe-truncate": r"""**Objectif** : écrire un pipe `truncate` qui raccourcit un texte trop long.

**Exemple d'utilisation** (dans un template) :
```html
{{ 'Bonjour tout le monde' | truncate:7 }}   <!-- affiche : Bonjour… -->
{{ 'Salut' | truncate:10 }}                  <!-- affiche : Salut (déjà assez court) -->
{{ unTexte | truncate }}                     <!-- sans paramètre : limite de 20 caractères -->
```

**À faire** dans la méthode `transform(value, max)` :
• si le texte fait plus de `max` caractères, garder les `max` premiers et ajouter « … » (un seul caractère) ;
• sinon, renvoyer le texte tel quel (un texte d'exactement `max` caractères n'est pas coupé).""",

"pipe-filesize": r"""**Objectif** : écrire un pipe `filesize` qui transforme un nombre d'octets en taille lisible.

**Exemple d'utilisation** :
```html
{{ 512 | filesize }}          <!-- 512 o   -->
{{ 1024 | filesize }}         <!-- 1 Ko    -->
{{ 1536 | filesize }}         <!-- 1.5 Ko  -->
{{ 1048576 | filesize }}      <!-- 1 Mo    -->
{{ 5368709120 | filesize }}   <!-- 5 Go    -->
{{ null | filesize }}         <!-- (rien)  -->
```

**À faire** dans `transform(bytes)` :
• 1 Ko = 1024 octets, 1 Mo = 1024 Ko, 1 Go = 1024 Mo ;
• garder au maximum une décimale, sans « .0 » inutile (« 1 Ko », pas « 1.0 Ko ») ;
• `null` ou `undefined` donnent une chaîne vide.""",

"component-counter": r"""**Objectif** : un compteur avec deux boutons, qui s'affiche ainsi :
```html
[ − ]  3  [ + ]
```

**À faire** dans `CounterComponent` (le template contient déjà les 3 éléments, repérés par `data-test`) :
• le bouton « + » ajoute 1 au signal `count`, le bouton « − » enlève 1 : écris les méthodes `increment()` et `decrement()` ;
• relie-les aux boutons avec `(click)` ;
• affiche la valeur du signal dans le `<span data-test="value">` avec `{{ count() }}` ;
• la valeur ne descend jamais sous 0, et le bouton « − » est désactivé (`[disabled]`) quand elle vaut 0.""",

"component-todo-list": r"""**Objectif** : afficher une liste de tâches reçue du parent.

**Exemple d'utilisation** (côté parent) :
```html
<app-todo-list [todos]="[
  { id: 1, title: 'Lire', done: false },
  { id: 2, title: 'Écrire', done: true }
]" />
```

**Résultat attendu** (HTML produit par `TodoListComponent`) :
```html
<ul>
  <li data-test="todo">Lire</li>
  <li data-test="todo" class="done">Écrire</li>
</ul>
<p data-test="remaining">1 restante(s)</p>
```

**À faire** dans le template :
• une ligne `<li data-test="todo">` par tâche, avec son `title` (boucle `@for`) ;
• la classe `done` seulement sur les tâches terminées ;
• si la liste est vide, afficher `<p data-test="empty">Aucune tâche</p>` à la place (bloc `@empty`) ;
• compléter le `computed` `remaining` (nombre de tâches non terminées) et l'afficher dans `data-test="remaining"` au format « 2 restante(s) ».""",

"card-projection": r"""**Objectif** : un composant « carte » qui affiche le contenu placé par le parent **entre ses balises**, chaque morceau au bon endroit. C'est la projection de contenu avec `<ng-content>`.

**Exemple d'utilisation** (côté parent) :
```html
<app-card>
  <h2 card-title>Ma carte</h2>
  <p>Un texte libre</p>
  <button card-footer>Valider</button>
</app-card>
```

**Résultat attendu** (HTML produit par `CardComponent`) :
```html
<header data-test="header"><h2 card-title>Ma carte</h2></header>
<div data-test="body"><p>Un texte libre</p></div>
<footer data-test="footer"><button card-footer>Valider</button></footer>
```

**À faire** : le template de `CardComponent` a déjà ses 3 zones, mais elles sont vides. Mets un `<ng-content>` dans chacune :
• dans `<header>` : seulement l'élément qui porte l'attribut `card-title` ;
• dans `<footer>` : seulement l'élément qui porte l'attribut `card-footer` ;
• dans `<div data-test="body">` : tout le reste du contenu.
Indice : `<ng-content select="[attribut]">` choisit les éléments portant cet attribut.""",

"component-rating": r"""**Objectif** : une notation par étoiles, cliquable.

**Exemple d'utilisation** (côté parent) :
```html
<app-rating [value]="3" [max]="5" (rated)="onRated($event)" />
```

**Résultat attendu** : 5 boutons étoiles, les 3 premiers remplis. Un clic sur la 4e étoile appelle `onRated(4)`.
```html
<button data-test="star" class="filled">★</button>  ×3
<button data-test="star">★</button>                 ×2
```

**À faire** dans `RatingComponent` :
• `stars` (computed) doit contenir `[1, 2, …, max]` ;
• dans le template, une boucle `@for` affiche un `<button data-test="star">` par étoile ;
• les `value` premières étoiles portent la classe `filled` (`[class.filled]`) ;
• un clic sur l'étoile n° `n` émet `n` avec la sortie `rated`.""",

"component-product-filter": r"""**Objectif** : une liste de produits que l'on filtre en tapant dans un champ de recherche.

**Exemple d'utilisation** (côté parent) :
```html
<app-product-list [products]="[
  { name: 'Laptop', price: 900 },
  { name: 'Phone', price: 500 },
  { name: 'Phone case', price: 15 }
]" />
```

**Résultat attendu** : en tapant « pho », il ne reste que 2 lignes.
```html
<p data-test="count">2 résultat(s)</p>
<li data-test="product">Phone – 500 €</li>
<li data-test="product">Phone case – 15 €</li>
```

**À faire** dans `ProductListComponent` :
• à chaque saisie dans le champ, mettre à jour le signal `query` (événement `(input)`) ;
• `filtered` (computed) garde les produits dont le nom contient `query`, sans tenir compte des majuscules ;
• afficher une ligne `data-test="product"` par produit filtré, au format « Nom – 500 € » ;
• afficher « N résultat(s) » dans `data-test="count"` ;
• s'il n'y a aucun résultat : `<p data-test="empty">Aucun résultat</p>`.""",

"form-login": r"""**Objectif** : un formulaire de connexion avec validation.

**Exemple d'utilisation** (côté parent) :
```html
<app-login (submitted)="onLogin($event)" />
<!-- onLogin reçoit : { email: 'a@b.fr', password: '123456' } -->
```

**Comportement attendu** :
• le bouton « Se connecter » est grisé tant que le formulaire est invalide ;
• si l'email est mal formé, **après avoir quitté le champ**, le message « Email invalide » apparaît ;
• quand tout est valide, la soumission émet `{ email, password }`.

**À faire** dans `LoginComponent` :
• ajouter les validateurs : `email` obligatoire et au format email ; `password` obligatoire, 6 caractères minimum (`Validators`) ;
• sur le bouton : `[disabled]="form.invalid"` ;
• afficher `<p data-test="email-error">Email invalide</p>` quand le champ email est invalide **et** touché (`touched`) ;
• dans `submit()`, émettre la valeur du formulaire avec la sortie `submitted`.""",

"directive-highlight": r"""**Objectif** : une directive d'attribut qui surligne un élément quand la souris le survole. Version moderne : une entrée `input()` (signal) et des `host` bindings, sans toucher au DOM à la main.

**Exemple d'utilisation** :
```html
<p appHighlight>Surlignage jaune (par défaut)</p>
<p appHighlight="lightblue">Surlignage bleu clair</p>
```

**Comportement attendu** :
• la souris entre sur l'élément : sa couleur de fond devient celle donnée à `appHighlight` (« yellow » si aucune) ;
• la souris sort : la couleur de fond est retirée.

**À faire** dans `HighlightDirective` (l'entrée et le signal sont déjà déclarés) :
• lis l'entrée avec `this.appHighlight()` : c'est un signal, une chaîne vide signifie « pas de couleur donnée » ;
• dans `host: { … }` du décorateur, écoute `(mouseenter)` et `(mouseleave)` pour modifier le signal `hovered` ;
• toujours dans `host`, lie `[style.background-color]` à une expression qui donne la couleur quand `hovered()` est vrai, sinon `null` ;
• ni `ElementRef`, ni `@HostListener`, ni `@Input` : c'est Angular qui applique le style.""",

"directive-click-outside": r"""**Objectif** : une directive qui prévient quand l'utilisateur clique **en dehors** d'un élément (pratique pour fermer un menu ou une modale).

**Exemple d'utilisation** :
```html
<div appClickOutside (appClickOutside)="fermerLeMenu()">
  <button>Un clic ici ne fait rien</button>
</div>
<!-- un clic n'importe où ailleurs sur la page appelle fermerLeMenu() -->
```

**À faire** dans `ClickOutsideDirective` (la sortie `output()` et l'élément injecté sont déjà déclarés) :
• dans `host: { … }` du décorateur, écoute les clics sur **tout le document** avec la clé `'(document:click)'`, qui appelle `onDocumentClick($event)` ;
• dans `onDocumentClick`, si l'élément cliqué (`event.target`) n'est ni l'élément de la directive ni l'un de ses enfants (`this.el.nativeElement.contains(...)`), émets la sortie `appClickOutside` ;
• un clic à l'intérieur n'émet rien.""",

"directive-unless": r"""**Objectif** : une directive structurelle `*appUnless`, l'inverse de `*ngIf` : elle affiche son contenu quand la condition est **fausse**.

**Exemple d'utilisation** :
```html
<p *appUnless="connecte">Connecte-toi pour continuer</p>
<!-- affiché quand connecte vaut false, retiré du DOM quand il vaut true -->
```

**À faire** dans `UnlessDirective` : l'entrée `appUnless` est un **signal** (`input.required`). Réagis à ses changements dans l'`effect()` du constructeur :
• lis la condition avec `this.appUnless()` ;
• condition fausse : crée la vue avec `this.container.createEmbeddedView(this.template)` ;
• condition vraie : détruis-la avec `this.container.clear()` ;
• ne crée jamais la vue deux fois (mémorise si elle est déjà affichée) ;
• enveloppe la création et la destruction de la vue dans `untracked(() => …)` : l'effet ne doit dépendre que de la condition.""",

"service-cart": r"""**Objectif** : un service de panier d'achat, avec des signaux.

**Exemple d'utilisation** :
```ts
const cart = inject(CartService);
cart.add({ id: 1, name: 'Stylo', price: 2 });
cart.add({ id: 1, name: 'Stylo', price: 2 });   // même produit : quantité 2, pas de 2e ligne
cart.add({ id: 2, name: 'Cahier', price: 5 });
cart.count();   // 3  (articles au total)
cart.total();   // 9  (2 × 2 + 5)
cart.remove(1); // retire la ligne du stylo
cart.clear();   // vide le panier
```

**À faire** dans `CartService` :
• `add` : si le produit est déjà dans `lines`, augmenter sa quantité `qty` de 1, sinon l'ajouter avec `qty: 1` ;
• `remove` et `clear` modifient `lines` ;
• `count` et `total` sont des `computed` calculés depuis `lines` ;
• ne modifie jamais un objet existant : crée toujours un nouveau tableau (`update`).""",

"service-http-users": r"""**Objectif** : un service qui récupère des utilisateurs depuis une API avec `HttpClient`.

**Exemple d'utilisation** :
```ts
const users = inject(UserService);
users.getActiveUsers().subscribe((noms) => console.log(noms));
// requête : GET /api/users?active=true
// réponse : [{ id: 1, name: 'Ada' }, { id: 2, name: 'Linus' }]
// noms    : ['Ada', 'Linus']
users.getUser(7).subscribe(...);   // requête : GET /api/users/7
```

**À faire** dans `UserService` :
• `getActiveUsers()` : faire la requête avec le paramètre `active=true` (option `params`), puis ne garder que les noms (`map`) ;
• en cas d'erreur HTTP, `getActiveUsers()` renvoie un tableau vide (`catchError` + `of([])`) ;
• `getUser(id)` : requête GET sur `/api/users/` + l'id, résultat renvoyé tel quel.""",

"interceptor-auth": r"""**Objectif** : un intercepteur HTTP qui ajoute automatiquement le token de connexion à chaque requête.

**Exemple** : quand `TokenService.token()` vaut `'abc123'`, toute requête part avec l'en-tête :
```html
Authorization: Bearer abc123
```
Sans token (`null`), la requête part inchangée.

**À faire** dans `authInterceptor` (une fonction `(req, next) => …`) :
• lire le token avec `inject(TokenService).token()` ;
• s'il n'y en a pas, renvoyer `next(req)` sans rien changer ;
• sinon, une requête est immuable : crée une copie avec `req.clone({ setHeaders: { … } })` et passe-la à `next(...)` ;
• les autres en-têtes de la requête doivent être conservés.""",

"rxjs-search": r"""**Objectif** : une recherche « pendant la frappe » qui n'appelle pas le serveur à chaque touche.

**Chronologie attendue** quand l'utilisateur tape « ngxs » :
```html
n, ng, ngx, ngxs   (frappes rapides)   → aucun appel
…300 ms sans frappe…                   → un seul appel : service.search('ngxs')
```

**À faire** : `this.query.valueChanges` émet à chaque frappe. Dans la déclaration de `results`, enchaîne ces opérateurs RxJS dans un `.pipe(...)` :
• `debounceTime(300)` : attendre 300 ms sans frappe ;
• `filter` : ignorer les textes de moins de 2 caractères ;
• `distinctUntilChanged()` : ignorer une valeur identique à la précédente ;
• `switchMap` vers `this.service.search(q)` : si une nouvelle recherche part, l'ancienne réponse est ignorée.
`toSignal(…, { initialValue: [] })` convertit déjà le flux en signal et se désabonne tout seul à la destruction du composant : pas de `subscribe` ni de `takeUntilDestroyed`.""",
}

def ex(id, title, diff, topic, starter, tests, hints, solution):
    X.append({"id": id, "title": title, "difficulty": diff, "topic": topic, "description": DESCRIPTIONS[id].strip(),
              "starterCode": starter.lstrip("\n"), "tests": [{"name": n, "code": c.strip()} for n, c in tests],
              "hints": hints, "solution": solution.lstrip("\n")})

# ───────────────────────── Pipes ─────────────────────────
ex("pipe-truncate", "Pipe truncate", E, "Pipe",
 r'''
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'truncate' })
export class TruncatePipe implements PipeTransform {
  transform(value: string, max = 20): string {
    // TODO : couper à `max` caractères et ajouter « … »
    return value;
  }
}
''',
 [("Coupe et ajoute …", r'''const v = render("{{ t | truncate:7 }}", { imports: [TruncatePipe], props: { t: "Bonjour tout le monde" } }); assert.equal(v.text(), "Bonjour…");'''),
  ("Texte court inchangé", r'''const v = render("{{ t | truncate:10 }}", { imports: [TruncatePipe], props: { t: "Salut" } }); assert.equal(v.text(), "Salut");'''),
  ("Longueur exacte inchangée", r'''const v = render("{{ t | truncate:5 }}", { imports: [TruncatePipe], props: { t: "abcde" } }); assert.equal(v.text(), "abcde");'''),
  ("Valeur par défaut : 20", r'''const v = render("{{ t | truncate }}", { imports: [TruncatePipe], props: { t: "a".repeat(25) } }); assert.equal(v.text(), "a".repeat(20) + "…");''')],
 ["`value.slice(0, max)` récupère le début du texte.", "Compare `value.length` à `max` avant de couper."],
 r'''
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'truncate' })
export class TruncatePipe implements PipeTransform {
  transform(value: string, max = 20): string {
    return value.length > max ? value.slice(0, max) + '…' : value;
  }
}
''')

ex("pipe-filesize", "Pipe filesize", M, "Pipe",
 r'''
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'filesize' })
export class FileSizePipe implements PipeTransform {
  transform(bytes: number | null | undefined): string {
    // TODO
    return '';
  }
}
''',
 [("Octets", r'''const v = render("{{ n | filesize }}", { imports: [FileSizePipe], props: { n: 512 } }); assert.equal(v.text(), "512 o");'''),
  ("Kilo-octets", r'''const v = render("{{ n | filesize }}", { imports: [FileSizePipe], props: { n: 1024 } }); assert.equal(v.text(), "1 Ko");'''),
  ("Une décimale", r'''const v = render("{{ n | filesize }}", { imports: [FileSizePipe], props: { n: 1536 } }); assert.equal(v.text(), "1.5 Ko");'''),
  ("Mégaoctets", r'''const v = render("{{ n | filesize }}", { imports: [FileSizePipe], props: { n: 1048576 } }); assert.equal(v.text(), "1 Mo");'''),
  ("Gigaoctets", r'''const v = render("{{ n | filesize }}", { imports: [FileSizePipe], props: { n: 5 * 1024 ** 3 } }); assert.equal(v.text(), "5 Go");'''),
  ("null et undefined", r'''const v = render("[{{ a | filesize }}][{{ b | filesize }}]", { imports: [FileSizePipe], props: { a: null, b: undefined } }); assert.equal(v.text(), "[][]");''')],
 ["Divise par 1024 tant que la valeur est ≥ 1024, en avançant dans un tableau d'unités ['o', 'Ko', 'Mo', 'Go'].", "`Math.round(v * 10) / 10` donne une décimale et supprime le « .0 »."],
 r'''
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'filesize' })
export class FileSizePipe implements PipeTransform {
  transform(bytes: number | null | undefined): string {
    if (bytes == null) return '';
    const units = ['o', 'Ko', 'Mo', 'Go'];
    let value = bytes;
    let unit = 0;
    while (value >= 1024 && unit < units.length - 1) {
      value /= 1024;
      unit++;
    }
    return `${Math.round(value * 10) / 10} ${units[unit]}`;
  }
}
''')

# ───────────────────────── Composants ─────────────────────────
ex("component-counter", "Composant compteur", E, "Composant · Signals",
 r'''
import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-counter',
  template: `
    <button data-test="dec">−</button>
    <span data-test="value">0</span>
    <button data-test="inc">+</button>
  `,
})
export class CounterComponent {
  count = signal(0);

  // TODO : increment() et decrement(), puis les relier au template
}
''',
 [("Affiche 0 au départ", r'''const v = render(CounterComponent); assert.equal(v.text("[data-test=value]"), "0");'''),
  ("Le bouton + incrémente", r'''const v = render(CounterComponent); v.click("[data-test=inc]"); v.click("[data-test=inc]"); assert.equal(v.text("[data-test=value]"), "2");'''),
  ("Le bouton − décrémente", r'''const v = render(CounterComponent); v.click("[data-test=inc]"); v.click("[data-test=inc]"); v.click("[data-test=dec]"); assert.equal(v.text("[data-test=value]"), "1");'''),
  ("Jamais sous 0", r'''const v = render(CounterComponent); v.click("[data-test=dec]"); v.click("[data-test=dec]"); assert.equal(v.text("[data-test=value]"), "0");'''),
  ("− désactivé à 0 seulement", r'''const v = render(CounterComponent); assert.equal(v.query("[data-test=dec]").disabled, true); v.click("[data-test=inc]"); assert.equal(v.query("[data-test=dec]").disabled, false);''')],
 ["`count.update(n => n + 1)` incrémente un signal.", "Dans le template : `{{ count() }}`, `(click)=\"increment()\"` et `[disabled]=\"count() === 0\"`.", "`Math.max(0, n - 1)` évite de passer sous zéro."],
 r'''
import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-counter',
  template: `
    <button data-test="dec" [disabled]="count() === 0" (click)="decrement()">−</button>
    <span data-test="value">{{ count() }}</span>
    <button data-test="inc" (click)="increment()">+</button>
  `,
})
export class CounterComponent {
  count = signal(0);

  increment() {
    this.count.update((n) => n + 1);
  }

  decrement() {
    this.count.update((n) => Math.max(0, n - 1));
  }
}
''')

ex("component-todo-list", "Liste de tâches (control flow)", E, "Composant · @for / @if",
 r'''
import { Component, computed, input } from '@angular/core';

interface Todo {
  id: number;
  title: string;
  done: boolean;
}

@Component({
  selector: 'app-todo-list',
  template: `
    <ul>
      <!-- TODO : @for / @empty -->
    </ul>
    <p data-test="remaining"></p>
  `,
})
export class TodoListComponent {
  todos = input<Todo[]>([]);
  remaining = computed(() => 0); // TODO
}
''',
 [("Une ligne par tâche", r'''const v = render(TodoListComponent, { inputs: { todos: [{ id: 1, title: "Lire", done: false }, { id: 2, title: "Écrire", done: true }, { id: 3, title: "Tester", done: false }] } }); assert.equal(v.queryAll("[data-test=todo]").length, 3); assert.equal(v.queryAll("[data-test=todo]")[0].textContent.trim(), "Lire");'''),
  ("Classe done sur les tâches terminées", r'''const v = render(TodoListComponent, { inputs: { todos: [{ id: 1, title: "A", done: false }, { id: 2, title: "B", done: true }] } }); const items = v.queryAll("[data-test=todo]"); assert.equal(items[0].classList.contains("done"), false); assert.equal(items[1].classList.contains("done"), true);'''),
  ("Message quand la liste est vide", r'''const v = render(TodoListComponent, { inputs: { todos: [] } }); assert.equal(v.text("[data-test=empty]"), "Aucune tâche"); assert.equal(v.queryAll("[data-test=todo]").length, 0);'''),
  ("Pas de message quand il y a des tâches", r'''const v = render(TodoListComponent, { inputs: { todos: [{ id: 1, title: "A", done: false }] } }); assert.equal(v.query("[data-test=empty]"), null);'''),
  ("Compteur de tâches restantes", r'''const v = render(TodoListComponent, { inputs: { todos: [{ id: 1, title: "A", done: false }, { id: 2, title: "B", done: true }, { id: 3, title: "C", done: false }] } }); assert.equal(v.text("[data-test=remaining]"), "2 restante(s)");'''),
  ("Se met à jour quand l'entrée change", r'''const v = render(TodoListComponent, { inputs: { todos: [] } }); v.setInput("todos", [{ id: 1, title: "Nouveau", done: false }]); assert.equal(v.queryAll("[data-test=todo]").length, 1); assert.equal(v.text("[data-test=remaining]"), "1 restante(s)");''')],
 ["`@for (todo of todos(); track todo.id) { ... } @empty { ... }` gère aussi le cas vide.", "`[class.done]=\"todo.done\"` ajoute la classe conditionnellement.", "`remaining = computed(() => this.todos().filter(t => !t.done).length)`."],
 r'''
import { Component, computed, input } from '@angular/core';

interface Todo {
  id: number;
  title: string;
  done: boolean;
}

@Component({
  selector: 'app-todo-list',
  template: `
    <ul>
      @for (todo of todos(); track todo.id) {
        <li data-test="todo" [class.done]="todo.done">{{ todo.title }}</li>
      } @empty {
        <p data-test="empty">Aucune tâche</p>
      }
    </ul>
    <p data-test="remaining">{{ remaining() }} restante(s)</p>
  `,
})
export class TodoListComponent {
  todos = input<Todo[]>([]);
  remaining = computed(() => this.todos().filter((t) => !t.done).length);
}
''')

ex("card-projection", "Carte avec projection de contenu", E, "Composant · ng-content",
 r'''
import { Component } from '@angular/core';

@Component({
  selector: 'app-card',
  template: `
    <header data-test="header"></header>
    <div data-test="body"></div>
    <footer data-test="footer"></footer>
  `,
})
export class CardComponent {}
''',
 [("Titre projeté dans le header", r'''const v = render('<app-card><h2 card-title>Mon titre</h2><p>Du texte</p></app-card>', { imports: [CardComponent] }); assert.equal(v.text("[data-test=header]"), "Mon titre");'''),
  ("Contenu libre dans le body", r'''const v = render('<app-card><h2 card-title>T</h2><p>Du texte</p></app-card>', { imports: [CardComponent] }); assert.equal(v.text("[data-test=body]"), "Du texte");'''),
  ("Pied de carte projeté", r'''const v = render('<app-card><p>x</p><button card-footer>Valider</button></app-card>', { imports: [CardComponent] }); assert.equal(v.text("[data-test=footer]"), "Valider");'''),
  ("Chaque contenu reste à sa place", r'''const v = render('<app-card><h2 card-title>T</h2><p>Corps</p><button card-footer>OK</button></app-card>', { imports: [CardComponent] }); assert.equal(v.text("[data-test=header]").includes("Corps"), false); assert.equal(v.text("[data-test=body]").includes("OK"), false);''')],
 ["`<ng-content select=\"[card-title]\"></ng-content>` projette les éléments portant cet attribut.", "Un `<ng-content></ng-content>` sans `select` récupère tout le contenu restant."],
 r'''
import { Component } from '@angular/core';

@Component({
  selector: 'app-card',
  template: `
    <header data-test="header"><ng-content select="[card-title]"></ng-content></header>
    <div data-test="body"><ng-content></ng-content></div>
    <footer data-test="footer"><ng-content select="[card-footer]"></ng-content></footer>
  `,
})
export class CardComponent {}
''')

ex("component-rating", "Notation par étoiles (input / output)", M, "Composant · input / output",
 r'''
import { Component, computed, input, output } from '@angular/core';

@Component({
  selector: 'app-rating',
  template: `
    <!-- TODO : une étoile cliquable par note -->
  `,
})
export class RatingComponent {
  value = input(0);
  max = input(5);
  rated = output<number>();

  stars = computed(() => [] as number[]); // TODO : [1, 2, …, max]
}
''',
 [("5 étoiles par défaut", r'''const v = render(RatingComponent); assert.equal(v.queryAll("[data-test=star]").length, 5);'''),
  ("Nombre d'étoiles configurable", r'''const v = render(RatingComponent, { inputs: { max: 3 } }); assert.equal(v.queryAll("[data-test=star]").length, 3);'''),
  ("Étoiles remplies selon value", r'''const v = render(RatingComponent, { inputs: { value: 2 } }); assert.equal(v.queryAll("[data-test=star].filled").length, 2);'''),
  ("Mise à jour quand value change", r'''const v = render(RatingComponent, { inputs: { value: 1 } }); v.setInput("value", 4); assert.equal(v.queryAll("[data-test=star].filled").length, 4);'''),
  ("Émet la note au clic", r'''const v = render('<app-rating [value]="v" (rated)="last = $event" />', { imports: [RatingComponent], props: { v: 1, last: null } }); v.queryAll("[data-test=star]")[2].click(); v.detectChanges(); assert.equal(v.component.last, 3);''')],
 ["`stars = computed(() => Array.from({ length: this.max() }, (_, i) => i + 1))`.", "Dans le template : `(click)=\"rated.emit(star)\"` et `[class.filled]=\"star <= value()\"`."],
 r'''
import { Component, computed, input, output } from '@angular/core';

@Component({
  selector: 'app-rating',
  template: `
    @for (star of stars(); track star) {
      <button data-test="star" type="button" [class.filled]="star <= value()" (click)="rated.emit(star)">★</button>
    }
  `,
})
export class RatingComponent {
  value = input(0);
  max = input(5);
  rated = output<number>();

  stars = computed(() => Array.from({ length: this.max() }, (_, i) => i + 1));
}
''')

ex("component-product-filter", "Liste filtrable (signals)", M, "Composant · Signals",
 r'''
import { Component, computed, input, signal } from '@angular/core';

interface Product {
  name: string;
  price: number;
}

@Component({
  selector: 'app-product-list',
  template: `
    <input data-test="search" placeholder="Rechercher" />
    <p data-test="count"></p>
    <ul>
      <!-- TODO -->
    </ul>
  `,
})
export class ProductListComponent {
  products = input<Product[]>([]);
  query = signal('');
  filtered = computed(() => this.products()); // TODO : filtrer avec query()
}
''',
 [("Affiche tous les produits au départ", r'''const v = render(ProductListComponent, { inputs: { products: [{ name: "Laptop", price: 900 }, { name: "Phone", price: 500 }, { name: "Phone case", price: 15 }] } }); assert.equal(v.queryAll("[data-test=product]").length, 3); assert.equal(v.queryAll("[data-test=product]")[1].textContent.trim(), "Phone – 500 €");'''),
  ("Filtre pendant la saisie", r'''const v = render(ProductListComponent, { inputs: { products: [{ name: "Laptop", price: 900 }, { name: "Phone", price: 500 }] } }); v.type("[data-test=search]", "pho"); assert.equal(v.queryAll("[data-test=product]").length, 1); assert.equal(v.component.query(), "pho");'''),
  ("Insensible à la casse", r'''const v = render(ProductListComponent, { inputs: { products: [{ name: "Laptop", price: 900 }, { name: "Phone", price: 500 }] } }); v.type("[data-test=search]", "LAPTOP"); assert.equal(v.queryAll("[data-test=product]").length, 1);'''),
  ("Compteur de résultats", r'''const v = render(ProductListComponent, { inputs: { products: [{ name: "Phone", price: 500 }, { name: "Phone case", price: 15 }, { name: "Laptop", price: 900 }] } }); v.type("[data-test=search]", "phone"); assert.equal(v.text("[data-test=count]"), "2 résultat(s)");'''),
  ("Message quand rien ne correspond", r'''const v = render(ProductListComponent, { inputs: { products: [{ name: "Laptop", price: 900 }] } }); v.type("[data-test=search]", "zzz"); assert.equal(v.text("[data-test=empty]"), "Aucun résultat"); assert.equal(v.queryAll("[data-test=product]").length, 0);''')],
 ["`(input)=\"query.set($any($event.target).value)\"` met le signal à jour.", "`filtered = computed(() => this.products().filter(p => p.name.toLowerCase().includes(this.query().toLowerCase())))`.", "Pense à `@empty` dans le `@for`."],
 r'''
import { Component, computed, input, signal } from '@angular/core';

interface Product {
  name: string;
  price: number;
}

@Component({
  selector: 'app-product-list',
  template: `
    <input data-test="search" placeholder="Rechercher" (input)="query.set($any($event.target).value)" />
    <p data-test="count">{{ filtered().length }} résultat(s)</p>
    <ul>
      @for (p of filtered(); track p.name) {
        <li data-test="product">{{ p.name }} – {{ p.price }} €</li>
      } @empty {
        <p data-test="empty">Aucun résultat</p>
      }
    </ul>
  `,
})
export class ProductListComponent {
  products = input<Product[]>([]);
  query = signal('');
  filtered = computed(() => {
    const q = this.query().toLowerCase();
    return this.products().filter((p) => p.name.toLowerCase().includes(q));
  });
}
''')

ex("form-login", "Formulaire de connexion réactif", M, "Formulaires réactifs",
 r'''
import { Component, output } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <input data-test="email" formControlName="email" type="email" />
      <input data-test="password" formControlName="password" type="password" />
      <button data-test="submit" type="submit">Se connecter</button>
    </form>
  `,
})
export class LoginComponent {
  submitted = output<{ email: string; password: string }>();

  form = new FormGroup({
    email: new FormControl('', { nonNullable: true }),
    password: new FormControl('', { nonNullable: true }),
  });

  submit() {
    // TODO
  }
}
''',
 [("Bouton désactivé au départ", r'''const v = render(LoginComponent); assert.equal(v.query("[data-test=submit]").disabled, true);'''),
  ("Email invalide : bouton désactivé", r'''const v = render(LoginComponent); v.type("[data-test=email]", "pas-un-email"); v.type("[data-test=password]", "123456"); assert.equal(v.query("[data-test=submit]").disabled, true);'''),
  ("Mot de passe trop court : bouton désactivé", r'''const v = render(LoginComponent); v.type("[data-test=email]", "a@b.fr"); v.type("[data-test=password]", "123"); assert.equal(v.query("[data-test=submit]").disabled, true);'''),
  ("Formulaire valide : bouton actif", r'''const v = render(LoginComponent); v.type("[data-test=email]", "a@b.fr"); v.type("[data-test=password]", "123456"); assert.equal(v.query("[data-test=submit]").disabled, false);'''),
  ("Message d'erreur après blur", r'''const v = render(LoginComponent); assert.equal(v.query("[data-test=email-error]"), null); v.type("[data-test=email]", "nope"); v.trigger("[data-test=email]", "blur"); assert.equal(v.text("[data-test=email-error]"), "Email invalide");'''),
  ("Pas d'erreur sur un email valide", r'''const v = render(LoginComponent); v.type("[data-test=email]", "a@b.fr"); v.trigger("[data-test=email]", "blur"); assert.equal(v.query("[data-test=email-error]"), null);'''),
  ("Émet la valeur à la soumission", r'''const v = render('<app-login (submitted)="data = $event" />', { imports: [LoginComponent], props: { data: null } }); v.type("[data-test=email]", "a@b.fr"); v.type("[data-test=password]", "123456"); v.trigger("form", "submit"); assert.deepEqual(v.component.data, { email: "a@b.fr", password: "123456" });''')],
 ["`Validators.required`, `Validators.email` et `Validators.minLength(6)` se passent dans l'option `validators` du FormControl.", "`[disabled]=\"form.invalid\"` sur le bouton.", "`form.controls.email.touched && form.controls.email.invalid` dans un `@if`.", "`this.submitted.emit(this.form.getRawValue())`."],
 r'''
import { Component, output } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <input data-test="email" formControlName="email" type="email" />
      @if (form.controls.email.touched && form.controls.email.invalid) {
        <p data-test="email-error">Email invalide</p>
      }
      <input data-test="password" formControlName="password" type="password" />
      <button data-test="submit" type="submit" [disabled]="form.invalid">Se connecter</button>
    </form>
  `,
})
export class LoginComponent {
  submitted = output<{ email: string; password: string }>();

  form = new FormGroup({
    email: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.email] }),
    password: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.minLength(6)] }),
  });

  submit() {
    if (this.form.valid) this.submitted.emit(this.form.getRawValue());
  }
}
''')

# ───────────────────────── Directives ─────────────────────────
ex("directive-highlight", "Directive highlight", E, "Directive · host · input()",
 r'''
import { Directive, input, signal } from '@angular/core';

@Directive({
  selector: '[appHighlight]',
  host: {
    // TODO : '(mouseenter)', '(mouseleave)' et '[style.background-color]'
  },
})
export class HighlightDirective {
  /** Couleur du surlignage (chaîne vide = aucune couleur donnée). */
  appHighlight = input('yellow');
  hovered = signal(false);
}
''',
 [("Couleur par défaut au survol", r'''const v = render("<p appHighlight>Texte</p>", { imports: [HighlightDirective] }); v.trigger("p", "mouseenter"); assert.equal(v.query("p").style.backgroundColor, "yellow");'''),
  ("Couleur personnalisée", r'''const v = render('<p appHighlight="lightblue">Texte</p>', { imports: [HighlightDirective] }); v.trigger("p", "mouseenter"); assert.equal(v.query("p").style.backgroundColor, "lightblue");'''),
  ("Fond retiré à la sortie", r'''const v = render("<p appHighlight>Texte</p>", { imports: [HighlightDirective] }); v.trigger("p", "mouseenter"); v.trigger("p", "mouseleave"); assert.equal(v.query("p").style.backgroundColor, "");'''),
  ("Pas de fond avant le survol", r'''const v = render("<p appHighlight>Texte</p>", { imports: [HighlightDirective] }); assert.equal(v.query("p").style.backgroundColor, "");'''),
  ("Suit un changement de couleur", r'''const v = render('<p [appHighlight]="color">Texte</p>', { imports: [HighlightDirective], props: { color: "red" } }); v.trigger("p", "mouseenter"); assert.equal(v.query("p").style.backgroundColor, "red"); v.component.color = "green"; v.detectChanges(); assert.equal(v.query("p").style.backgroundColor, "green");''')],
 ["`host: { '(mouseenter)': 'hovered.set(true)' }` écoute un événement de l'élément hôte et exécute l'expression.", "`'[style.background-color]': 'hovered() ? couleur : null'` lie un style : Angular le met à jour tout seul quand le signal change.", "Une chaîne vide est « falsy » : `this.appHighlight() || 'yellow'` donne la couleur par défaut."],
 r'''
import { Directive, input, signal } from '@angular/core';

@Directive({
  selector: '[appHighlight]',
  host: {
    '(mouseenter)': 'hovered.set(true)',
    '(mouseleave)': 'hovered.set(false)',
    '[style.background-color]': 'hovered() ? (appHighlight() || "yellow") : null',
  },
})
export class HighlightDirective {
  /** Couleur du surlignage (chaîne vide = aucune couleur donnée). */
  appHighlight = input('yellow');
  hovered = signal(false);
}
''')

ex("directive-click-outside", "Directive clic extérieur", M, "Directive · host · output()",
 r'''
import { Directive, ElementRef, inject, output } from '@angular/core';

@Directive({
  selector: '[appClickOutside]',
  host: {
    // TODO : écouter '(document:click)'
  },
})
export class ClickOutsideDirective {
  appClickOutside = output<void>();
  private el = inject<ElementRef<HTMLElement>>(ElementRef);

  onDocumentClick(event: MouseEvent) {
    // TODO : émettre appClickOutside si le clic est en dehors de l'élément
  }
}
''',
 [("Un clic à l'extérieur émet", r'''const v = render('<div><div appClickOutside (appClickOutside)="n = n + 1"><button id="in">dedans</button></div><button id="out">dehors</button></div>', { imports: [ClickOutsideDirective], props: { n: 0 } }); v.click("#out"); assert.equal(v.component.n, 1);'''),
  ("Un clic à l'intérieur n'émet pas", r'''const v = render('<div><div appClickOutside (appClickOutside)="n = n + 1"><button id="in">dedans</button></div><button id="out">dehors</button></div>', { imports: [ClickOutsideDirective], props: { n: 0 } }); v.click("#in"); assert.equal(v.component.n, 0);'''),
  ("Chaque clic extérieur émet", r'''const v = render('<div><div appClickOutside (appClickOutside)="n = n + 1">x</div><button id="out">dehors</button></div>', { imports: [ClickOutsideDirective], props: { n: 0 } }); v.click("#out"); v.click("#out"); assert.equal(v.component.n, 2);''')],
 ["`host: { '(document:click)': 'onDocumentClick($event)' }` écoute les clics sur tout le document et appelle la méthode.", "`event.target` est le noeud cliqué : `this.el.nativeElement.contains(event.target as Node)` dit s'il est à l'intérieur.", "`this.appClickOutside.emit()` pour notifier le parent."],
 r'''
import { Directive, ElementRef, inject, output } from '@angular/core';

@Directive({
  selector: '[appClickOutside]',
  host: {
    '(document:click)': 'onDocumentClick($event)',
  },
})
export class ClickOutsideDirective {
  appClickOutside = output<void>();
  private el = inject<ElementRef<HTMLElement>>(ElementRef);

  onDocumentClick(event: MouseEvent) {
    if (!this.el.nativeElement.contains(event.target as Node)) {
      this.appClickOutside.emit();
    }
  }
}
''')

ex("directive-unless", "Directive structurelle *appUnless", H, "Directive structurelle · input() · effect()",
 r'''
import { Directive, TemplateRef, ViewContainerRef, effect, inject, input, untracked } from '@angular/core';

@Directive({ selector: '[appUnless]' })
export class UnlessDirective {
  private template = inject(TemplateRef<unknown>);
  private container = inject(ViewContainerRef);

  /** La condition : le contenu est affiché quand elle est fausse. */
  appUnless = input.required<unknown>();

  constructor() {
    effect(() => {
      // TODO : lire this.appUnless() puis afficher ou retirer le template
    });
  }
}
''',
 [("Affiché quand la condition est fausse", r'''const v = render("<p *appUnless=\"hidden\">Visible</p>", { imports: [UnlessDirective], props: { hidden: false } }); assert.equal(v.text("p"), "Visible");'''),
  ("Masqué quand la condition est vraie", r'''const v = render("<p *appUnless=\"hidden\">Visible</p>", { imports: [UnlessDirective], props: { hidden: true } }); assert.equal(v.query("p"), null);'''),
  ("Réagit aux changements", r'''const v = render("<p *appUnless=\"hidden\">Visible</p>", { imports: [UnlessDirective], props: { hidden: false } }); v.component.hidden = true; v.detectChanges(); assert.equal(v.query("p"), null); v.component.hidden = false; v.detectChanges(); assert.equal(v.queryAll("p").length, 1);'''),
  ("Jamais de doublon", r'''const v = render("<p *appUnless=\"hidden\">Visible</p>", { imports: [UnlessDirective], props: { hidden: 0 } }); v.component.hidden = false; v.detectChanges(); v.component.hidden = null; v.detectChanges(); assert.equal(v.queryAll("p").length, 1);''')],
 ["L'entrée est un signal : `this.appUnless()` lu dans l'`effect()` relance l'effet à chaque changement.", "`this.container.createEmbeddedView(this.template)` crée la vue ; `this.container.clear()` la détruit.", "Mémorise dans un booléen si la vue est déjà affichée, et fais la création / destruction dans `untracked(() => …)`."],
 r'''
import { Directive, TemplateRef, ViewContainerRef, effect, inject, input, untracked } from '@angular/core';

@Directive({ selector: '[appUnless]' })
export class UnlessDirective {
  private template = inject(TemplateRef<unknown>);
  private container = inject(ViewContainerRef);
  private shown = false;

  /** La condition : le contenu est affiché quand elle est fausse. */
  appUnless = input.required<unknown>();

  constructor() {
    effect(() => {
      const condition = this.appUnless();
      untracked(() => {
        if (!condition && !this.shown) {
          this.container.createEmbeddedView(this.template);
          this.shown = true;
        } else if (condition && this.shown) {
          this.container.clear();
          this.shown = false;
        }
      });
    });
  }
}
''')

# ───────────────────────── Services / HTTP ─────────────────────────
ex("service-cart", "Service panier (signals)", E, "Service · Signals",
 r'''
import { Service, computed, signal } from '@angular/core';

export interface Product {
  id: number;
  name: string;
  price: number;
}

export interface CartLine extends Product {
  qty: number;
}

@Service()
export class CartService {
  readonly lines = signal<CartLine[]>([]);

  readonly count = computed(() => 0); // TODO
  readonly total = computed(() => 0); // TODO

  add(product: Product) {
    // TODO
  }

  remove(id: number) {
    // TODO
  }

  clear() {
    // TODO
  }
}
''',
 [("Ajoute un produit", r'''const cart = createInjector([CartService]).get(CartService); cart.add({ id: 1, name: "Stylo", price: 2 }); assert.equal(cart.lines().length, 1); assert.equal(cart.lines()[0].qty, 1);'''),
  ("Incrémente la quantité d'un produit existant", r'''const cart = createInjector([CartService]).get(CartService); cart.add({ id: 1, name: "Stylo", price: 2 }); cart.add({ id: 1, name: "Stylo", price: 2 }); assert.equal(cart.lines().length, 1); assert.equal(cart.lines()[0].qty, 2);'''),
  ("count = total des quantités", r'''const cart = createInjector([CartService]).get(CartService); cart.add({ id: 1, name: "A", price: 2 }); cart.add({ id: 1, name: "A", price: 2 }); cart.add({ id: 2, name: "B", price: 5 }); assert.equal(cart.count(), 3);'''),
  ("total = somme prix × quantité", r'''const cart = createInjector([CartService]).get(CartService); cart.add({ id: 1, name: "A", price: 2 }); cart.add({ id: 1, name: "A", price: 2 }); cart.add({ id: 2, name: "B", price: 5 }); assert.equal(cart.total(), 9);'''),
  ("remove retire la ligne", r'''const cart = createInjector([CartService]).get(CartService); cart.add({ id: 1, name: "A", price: 2 }); cart.add({ id: 2, name: "B", price: 5 }); cart.remove(1); assert.deepEqual(cart.lines().map((l) => l.id), [2]);'''),
  ("clear vide le panier", r'''const cart = createInjector([CartService]).get(CartService); cart.add({ id: 1, name: "A", price: 2 }); cart.clear(); assert.equal(cart.count(), 0); assert.equal(cart.total(), 0);'''),
  ("Ne mute pas les lignes existantes (immutabilité)", r'''const cart = createInjector([CartService]).get(CartService); cart.add({ id: 1, name: "A", price: 2 }); const before = cart.lines(); cart.add({ id: 1, name: "A", price: 2 }); assert.ok(before !== cart.lines()); assert.equal(before[0].qty, 1);''')],
 ["`this.lines.update(lines => ...)` : retourne toujours un nouveau tableau.", "Cherche la ligne avec `find`, puis `map` pour créer une copie `{ ...line, qty: line.qty + 1 }`.", "`reduce` calcule les deux totaux dans les `computed`."],
 r'''
import { Service, computed, signal } from '@angular/core';

export interface Product {
  id: number;
  name: string;
  price: number;
}

export interface CartLine extends Product {
  qty: number;
}

@Service()
export class CartService {
  readonly lines = signal<CartLine[]>([]);

  readonly count = computed(() => this.lines().reduce((n, l) => n + l.qty, 0));
  readonly total = computed(() => this.lines().reduce((sum, l) => sum + l.price * l.qty, 0));

  add(product: Product) {
    this.lines.update((lines) =>
      lines.some((l) => l.id === product.id)
        ? lines.map((l) => (l.id === product.id ? { ...l, qty: l.qty + 1 } : l))
        : [...lines, { ...product, qty: 1 }],
    );
  }

  remove(id: number) {
    this.lines.update((lines) => lines.filter((l) => l.id !== id));
  }

  clear() {
    this.lines.set([]);
  }
}
''')

ex("service-http-users", "Service HTTP (HttpClient)", M, "Service · HttpClient",
 r'''
import { HttpClient } from '@angular/common/http';
import { Service, inject } from '@angular/core';
import { Observable, catchError, map, of } from 'rxjs';

export interface User {
  id: number;
  name: string;
}

@Service()
export class UserService {
  private http = inject(HttpClient);

  getActiveUsers(): Observable<string[]> {
    // TODO
    return of([]);
  }

  getUser(id: number): Observable<User> {
    // TODO
    return of({ id, name: '' });
  }
}
''',
 [("getActiveUsers : bonne requête", r'''const { provideHttpClient } = require("@angular/common/http"); const { provideHttpClientTesting, HttpTestingController } = require("@angular/common/http/testing"); const injector = createInjector([UserService, provideHttpClient(), provideHttpClientTesting()]); const http = injector.get(HttpTestingController); injector.get(UserService).getActiveUsers().subscribe(); const req = http.expectOne("/api/users?active=true"); assert.equal(req.request.method, "GET");'''),
  ("getActiveUsers : retourne les noms", r'''const { provideHttpClient } = require("@angular/common/http"); const { provideHttpClientTesting, HttpTestingController } = require("@angular/common/http/testing"); const injector = createInjector([UserService, provideHttpClient(), provideHttpClientTesting()]); const http = injector.get(HttpTestingController); let result; injector.get(UserService).getActiveUsers().subscribe((r) => (result = r)); http.expectOne("/api/users?active=true").flush([{ id: 1, name: "Ada" }, { id: 2, name: "Linus" }]); assert.deepEqual(result, ["Ada", "Linus"]);'''),
  ("getActiveUsers : tableau vide en cas d'erreur", r'''const { provideHttpClient } = require("@angular/common/http"); const { provideHttpClientTesting, HttpTestingController } = require("@angular/common/http/testing"); const injector = createInjector([UserService, provideHttpClient(), provideHttpClientTesting()]); const http = injector.get(HttpTestingController); let result = "pas de valeur"; injector.get(UserService).getActiveUsers().subscribe((r) => (result = r)); http.expectOne("/api/users?active=true").flush("boom", { status: 500, statusText: "Server Error" }); assert.deepEqual(result, []);'''),
  ("getUser : GET /api/users/:id", r'''const { provideHttpClient } = require("@angular/common/http"); const { provideHttpClientTesting, HttpTestingController } = require("@angular/common/http/testing"); const injector = createInjector([UserService, provideHttpClient(), provideHttpClientTesting()]); const http = injector.get(HttpTestingController); let result; injector.get(UserService).getUser(7).subscribe((r) => (result = r)); const req = http.expectOne("/api/users/7"); assert.equal(req.request.method, "GET"); req.flush({ id: 7, name: "Grace" }); assert.deepEqual(result, { id: 7, name: "Grace" });''')],
 ["`this.http.get<User[]>('/api/users', { params: { active: true } })`.", "`.pipe(map(users => users.map(u => u.name)), catchError(() => of([])))`."],
 r'''
import { HttpClient } from '@angular/common/http';
import { Service, inject } from '@angular/core';
import { Observable, catchError, map, of } from 'rxjs';

export interface User {
  id: number;
  name: string;
}

@Service()
export class UserService {
  private http = inject(HttpClient);

  getActiveUsers(): Observable<string[]> {
    return this.http.get<User[]>('/api/users', { params: { active: true } }).pipe(
      map((users) => users.map((u) => u.name)),
      catchError(() => of([] as string[])),
    );
  }

  getUser(id: number): Observable<User> {
    return this.http.get<User>(`/api/users/${id}`);
  }
}
''')

ex("interceptor-auth", "Intercepteur d'authentification", M, "HttpInterceptor",
 r'''
import { HttpInterceptorFn } from '@angular/common/http';
import { Service, inject, signal } from '@angular/core';

@Service()
export class TokenService {
  token = signal<string | null>(null);
}

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // TODO : ajouter l'en-tête Authorization si un token existe
  return next(req);
};
''',
 [("Ajoute l'en-tête Authorization", r'''const { HttpClient, provideHttpClient, withInterceptors } = require("@angular/common/http"); const { provideHttpClientTesting, HttpTestingController } = require("@angular/common/http/testing"); const injector = createInjector([TokenService, provideHttpClient(withInterceptors([authInterceptor])), provideHttpClientTesting()]); injector.get(TokenService).token.set("abc123"); injector.get(HttpClient).get("/api/me").subscribe(); const req = injector.get(HttpTestingController).expectOne("/api/me"); assert.equal(req.request.headers.get("Authorization"), "Bearer abc123");'''),
  ("Sans token : requête inchangée", r'''const { HttpClient, provideHttpClient, withInterceptors } = require("@angular/common/http"); const { provideHttpClientTesting, HttpTestingController } = require("@angular/common/http/testing"); const injector = createInjector([TokenService, provideHttpClient(withInterceptors([authInterceptor])), provideHttpClientTesting()]); injector.get(HttpClient).get("/api/me").subscribe(); const req = injector.get(HttpTestingController).expectOne("/api/me"); assert.equal(req.request.headers.has("Authorization"), false);'''),
  ("Utilise le token courant à chaque requête", r'''const { HttpClient, provideHttpClient, withInterceptors } = require("@angular/common/http"); const { provideHttpClientTesting, HttpTestingController } = require("@angular/common/http/testing"); const injector = createInjector([TokenService, provideHttpClient(withInterceptors([authInterceptor])), provideHttpClientTesting()]); const http = injector.get(HttpClient); const ctrl = injector.get(HttpTestingController); const tokens = injector.get(TokenService); tokens.token.set("first"); http.get("/a").subscribe(); assert.equal(ctrl.expectOne("/a").request.headers.get("Authorization"), "Bearer first"); tokens.token.set("second"); http.get("/b").subscribe(); assert.equal(ctrl.expectOne("/b").request.headers.get("Authorization"), "Bearer second");'''),
  ("Conserve les autres en-têtes", r'''const { HttpClient, provideHttpClient, withInterceptors } = require("@angular/common/http"); const { provideHttpClientTesting, HttpTestingController } = require("@angular/common/http/testing"); const injector = createInjector([TokenService, provideHttpClient(withInterceptors([authInterceptor])), provideHttpClientTesting()]); injector.get(TokenService).token.set("t"); injector.get(HttpClient).get("/x", { headers: { "X-Custom": "1" } }).subscribe(); const req = injector.get(HttpTestingController).expectOne("/x"); assert.equal(req.request.headers.get("X-Custom"), "1"); assert.equal(req.request.headers.get("Authorization"), "Bearer t");''')],
 ["`const token = inject(TokenService).token();` fonctionne dans un intercepteur fonctionnel.", "`req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })` retourne une nouvelle requête."],
 r'''
import { HttpInterceptorFn } from '@angular/common/http';
import { Service, inject, signal } from '@angular/core';

@Service()
export class TokenService {
  token = signal<string | null>(null);
}

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(TokenService).token();
  if (!token) return next(req);
  return next(req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }));
};
''')

# ───────────────────────── RxJS dans un composant ─────────────────────────
ex("rxjs-search", "Recherche avec debounce (RxJS)", H, "RxJS · Composant",
 r'''
import { Component, inject, Service } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Observable, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, filter, switchMap } from 'rxjs/operators';

@Service()
export class SearchService {
  search(query: string): Observable<string[]> {
    return of([]); // remplacé par un faux service dans les tests
  }
}

@Component({
  selector: 'app-search',
  imports: [ReactiveFormsModule],
  template: `
    <input data-test="search" [formControl]="query" />
    <ul>
      @for (r of results(); track r) {
        <li data-test="result">{{ r }}</li>
      }
    </ul>
  `,
})
export class SearchComponent {
  private service = inject(SearchService);
  query = new FormControl('', { nonNullable: true });

  // TODO : enchaîner les opérateurs RxJS (debounceTime, filter, distinctUntilChanged, switchMap)
  results = toSignal(
    this.query.valueChanges.pipe(switchMap(() => of([] as string[]))),
    { initialValue: [] as string[] },
  );
}
''',
 [("Attend 300 ms avant de chercher", r'''const calls = []; const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => { calls.push(q); return require("rxjs").of([q + "-1"]); } } }] }); v.type("[data-test=search]", "ng"); assert.equal(calls.length, 0); await wait(380); assert.deepEqual(calls, ["ng"]);'''),
  ("Affiche les résultats", r'''const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => require("rxjs").of([q + "-1", q + "-2"]) } }] }); v.type("[data-test=search]", "ng"); await wait(380); await v.stable(); assert.deepEqual(v.queryAll("[data-test=result]").map((e) => e.textContent.trim()), ["ng-1", "ng-2"]);'''),
  ("Une seule recherche pour une rafale de frappes", r'''const calls = []; const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => { calls.push(q); return require("rxjs").of([]); } } }] }); v.type("[data-test=search]", "ng"); await wait(100); v.type("[data-test=search]", "ngx"); await wait(100); v.type("[data-test=search]", "ngxs"); await wait(380); assert.deepEqual(calls, ["ngxs"]);'''),
  ("Ignore moins de 2 caractères", r'''const calls = []; const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => { calls.push(q); return require("rxjs").of([]); } } }] }); v.type("[data-test=search]", "a"); await wait(380); assert.equal(calls.length, 0);'''),
  ("Pas de nouvel appel pour la même valeur", r'''const calls = []; const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => { calls.push(q); return require("rxjs").of([]); } } }] }); v.type("[data-test=search]", "angular"); await wait(380); v.type("[data-test=search]", "angular"); await wait(380); assert.equal(calls.length, 1);'''),
  ("Ignore la réponse d'une ancienne recherche (switchMap)", r'''const { timer } = require("rxjs"); const { map } = require("rxjs/operators"); const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => timer(q === "ab" ? 400 : 20).pipe(map(() => [q])) } }] }); v.type("[data-test=search]", "ab"); await wait(340); v.type("[data-test=search]", "abc"); await wait(340); await wait(500); await v.stable(); assert.deepEqual(v.queryAll("[data-test=result]").map((e) => e.textContent.trim()), ["abc"]);''')],
 ["`toSignal(this.query.valueChanges.pipe(debounceTime(300), filter(q => q.length >= 2), distinctUntilChanged(), switchMap(q => this.service.search(q))), { initialValue: [] })`.", "`toSignal` s'abonne et se désabonne seul : plus besoin de `subscribe` ni de `takeUntilDestroyed`.", "`initialValue: []` est la valeur du signal tant qu'aucune recherche n'a répondu."],
 r'''
import { Component, inject, Service } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Observable, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, filter, switchMap } from 'rxjs/operators';

@Service()
export class SearchService {
  search(query: string): Observable<string[]> {
    return of([]); // remplacé par un faux service dans les tests
  }
}

@Component({
  selector: 'app-search',
  imports: [ReactiveFormsModule],
  template: `
    <input data-test="search" [formControl]="query" />
    <ul>
      @for (r of results(); track r) {
        <li data-test="result">{{ r }}</li>
      }
    </ul>
  `,
})
export class SearchComponent {
  private service = inject(SearchService);
  query = new FormControl('', { nonNullable: true });

  results = toSignal(
    this.query.valueChanges.pipe(
      debounceTime(300),
      filter((q) => q.length >= 2),
      distinctUntilChanged(),
      switchMap((q) => this.service.search(q)),
    ),
    { initialValue: [] as string[] },
  );
}
''')


# ───────────────────────── Aperçus interactifs ─────────────────────────
# Code exécuté après les tests (même portée que le code de l'utilisateur) pour rendre un exemple
# avec lequel on peut jouer ; `console.log` alimente la console de la page.
PREVIEWS = {
"pipe-truncate": r"""render('<p>{{ "Bonjour tout le monde" | truncate:7 }}</p><p>{{ "Court" | truncate }}</p>', { imports: [TruncatePipe] });""",
"pipe-filesize": r"""render('<ul><li>{{ 512 | filesize }}</li><li>{{ 1536 | filesize }}</li><li>{{ 1048576 | filesize }}</li><li>{{ 5368709120 | filesize }}</li></ul>', { imports: [FileSizePipe] });""",
"component-counter": r"""render(CounterComponent);""",
"component-todo-list": r"""render(TodoListComponent, { inputs: { todos: [{ id: 1, title: "Lire la doc Angular", done: true }, { id: 2, title: "Écrire un pipe", done: false }, { id: 3, title: "Passer l'entretien", done: false }] } });""",
"card-projection": r"""render('<app-card><h2 card-title>Ma carte</h2><p>Un contenu projeté.</p><button card-footer>Valider</button></app-card>', { imports: [CardComponent] });""",
"component-rating": r"""render('<app-rating [value]="3" (rated)="log($event)" />', { imports: [RatingComponent], props: { log: (n) => console.log("Note choisie :", n) } });""",
"component-product-filter": r"""render(ProductListComponent, { inputs: { products: [{ name: "Laptop", price: 900 }, { name: "Phone", price: 500 }, { name: "Phone case", price: 15 }, { name: "Écran", price: 250 }] } });""",
"form-login": r"""render('<app-login (submitted)="log($event)" />', { imports: [LoginComponent], props: { log: (v) => console.log("Formulaire soumis :", v) } });""",
"directive-highlight": r"""render('<p appHighlight="lightblue">Survole-moi (bleu)</p><p appHighlight>Survole-moi (jaune)</p>', { imports: [HighlightDirective] });""",
"directive-click-outside": r"""render('<div appClickOutside (appClickOutside)="log()" style="padding:16px;border:2px dashed #ab79ff">Clique ici, puis en dehors de ce cadre</div>', { imports: [ClickOutsideDirective], props: { log: () => console.log("Clic à l'extérieur !") } });""",
"directive-unless": r"""render('<button (click)="hidden = !hidden">Basculer hidden ({{ hidden }})</button><p *appUnless="hidden">Visible quand hidden vaut false</p>', { imports: [UnlessDirective], props: { hidden: false } });""",
"service-cart": r"""class Demo { cart = __ng.inject(CartService); products = [{ id: 1, name: "Stylo", price: 2 }, { id: 2, name: "Cahier", price: 5 }]; }
__ng.Component({ selector: "app-demo", template: `@for (p of products; track p.id) { <button (click)="cart.add(p)">Ajouter {{ p.name }}</button> } <button (click)="cart.clear()">Vider</button><p>{{ cart.count() }} article(s) — {{ cart.total() }} €</p>` })(Demo);
render(Demo, { providers: [CartService] });""",
"service-http-users": r"""const { provideHttpClient } = require("@angular/common/http");
const { provideHttpClientTesting, HttpTestingController } = require("@angular/common/http/testing");
const injector = createInjector([UserService, provideHttpClient(), provideHttpClientTesting()]);
injector.get(UserService).getActiveUsers().subscribe((names) => console.log("Utilisateurs actifs :", names));
injector.get(HttpTestingController).expectOne("/api/users?active=true").flush([{ id: 1, name: "Ada" }, { id: 2, name: "Linus" }]);""",
"interceptor-auth": r"""const { HttpClient, provideHttpClient, withInterceptors } = require("@angular/common/http");
const { provideHttpClientTesting, HttpTestingController } = require("@angular/common/http/testing");
const injector = createInjector([TokenService, provideHttpClient(withInterceptors([authInterceptor])), provideHttpClientTesting()]);
injector.get(TokenService).token.set("abc123");
injector.get(HttpClient).get("/api/me").subscribe();
const req = injector.get(HttpTestingController).expectOne("/api/me");
console.log("Authorization :", req.request.headers.get("Authorization"));""",
"rxjs-search": r"""const { of } = require("rxjs");
render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => { console.log("Recherche :", q); return of([q + " – résultat 1", q + " – résultat 2"]); } } }] });""",
}
for item in X:
    item["kind"] = "angular"
    item["preview"] = PREVIEWS.get(item["id"], "")
X.extend(ALGOS)

pathlib.Path(__file__).resolve().parent.parent.joinpath("public/data/exercises.json").write_text(
    json.dumps(X, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(X), "exercices")
