"""Génère public/data/exercises.json : exercices Angular concrets (pipe, composant, directive, service…).

Le code de départ et la solution sont du TypeScript Angular réel, compilé dans le navigateur (JIT).
Chaque test est le corps d'une fonction async qui voit le code de l'utilisateur et reçoit
`assert`, `render(template | Composant, options)`, `createInjector(providers)` et `wait(ms)`.
exercises.data.spec.ts vérifie que chaque solution passe tous les tests et que le départ en échoue.
"""
import json, pathlib

E, M, H = "easy", "medium", "hard"
X = []
def ex(id, title, diff, topic, desc, starter, tests, hints, solution):
    X.append({"id": id, "title": title, "difficulty": diff, "topic": topic, "description": desc.strip(),
              "starterCode": starter.lstrip("\n"), "tests": [{"name": n, "code": c.strip()} for n, c in tests],
              "hints": hints, "solution": solution.lstrip("\n")})

# ───────────────────────── Pipes ─────────────────────────
ex("pipe-truncate", "Pipe truncate", E, "Pipe",
 """Complète le pipe `truncate` : `{{ 'Bonjour tout le monde' | truncate:7 }}` doit afficher « Bonjour… ».
• Au-delà de `max` caractères, on coupe et on ajoute « … » (un seul caractère).
• Si le texte tient dans `max`, il reste inchangé.
• `max` vaut 20 par défaut.""",
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
 """Écris un pipe `filesize` qui convertit un nombre d'octets en texte lisible :
512 → « 512 o » · 1024 → « 1 Ko » · 1536 → « 1.5 Ko » · 1048576 → « 1 Mo » · 5368709120 → « 5 Go ».
• Une décimale maximum, sans « .0 » inutile.
• `null` ou `undefined` → chaîne vide.""",
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
 """Complète le composant `CounterComponent` avec un signal :
• le bouton « + » incrémente, le bouton « − » décrémente ;
• la valeur ne descend jamais sous 0 ;
• le bouton « − » est désactivé quand la valeur vaut 0 ;
• la valeur est affichée dans l'élément `data-test="value"`.""",
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
 """Le composant `TodoListComponent` reçoit une liste de tâches via l'entrée `todos`. Complète son template :
• une ligne `<li data-test="todo">` par tâche, avec son titre ;
• la classe CSS `done` sur les tâches terminées ;
• s'il n'y a aucune tâche : `<p data-test="empty">Aucune tâche</p>` ;
• le nombre de tâches non terminées dans `data-test="remaining"` au format « 2 restante(s) ».""",
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
 """Un composant `CardComponent` doit afficher le contenu fourni par son parent à trois endroits :
• `<header data-test="header">` : l'élément portant l'attribut `card-title` ;
• `<div data-test="body">` : tout le reste du contenu ;
• `<footer data-test="footer">` : l'élément portant l'attribut `card-footer`.
Utilise `<ng-content>` avec `select`.""",
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
 """Complète `RatingComponent` :
• affiche `max` boutons `data-test="star"` (5 par défaut) ;
• les `value` premières étoiles portent la classe `filled` ;
• un clic sur la n-ième étoile émet `n` via la sortie `rated`.""",
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
 """`ProductListComponent` affiche des produits et les filtre pendant la frappe :
• un champ `data-test="search"` met à jour le signal `query` à chaque saisie ;
• `filtered` (computed) garde les produits dont le nom contient `query`, sans tenir compte de la casse ;
• une ligne `data-test="product"` par produit (« Nom – 12 € ») ;
• `data-test="count"` affiche « 2 résultat(s) » ;
• aucun résultat : `<p data-test="empty">Aucun résultat</p>`.""",
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
 """Complète `LoginComponent` (formulaire réactif) :
• `email` : obligatoire et au format email ; `password` : obligatoire, 6 caractères minimum ;
• le bouton `data-test="submit"` est désactivé tant que le formulaire est invalide ;
• quand le champ email a été touché (blur) et qu'il est invalide, affiche `<p data-test="email-error">Email invalide</p>` ;
• à la soumission, la sortie `submitted` émet `{ email, password }`.""",
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
ex("directive-highlight", "Directive highlight", E, "Directive",
 """Complète `HighlightDirective` (attribut `appHighlight`) :
• au survol (`mouseenter`), l'élément prend la couleur de fond `appHighlight` (« yellow » par défaut) ;
• à la sortie (`mouseleave`), le fond est retiré.
Exemple : `<p appHighlight="lightblue">…</p>`.""",
 r'''
import { Directive, ElementRef, HostListener, Input, inject } from '@angular/core';

@Directive({ selector: '[appHighlight]' })
export class HighlightDirective {
  @Input() appHighlight = 'yellow';
  private el = inject<ElementRef<HTMLElement>>(ElementRef);

  // TODO : @HostListener('mouseenter') et @HostListener('mouseleave')
}
''',
 [("Couleur par défaut au survol", r'''const v = render("<p appHighlight>Texte</p>", { imports: [HighlightDirective] }); v.trigger("p", "mouseenter"); assert.equal(v.query("p").style.backgroundColor, "yellow");'''),
  ("Couleur personnalisée", r'''const v = render('<p appHighlight="lightblue">Texte</p>', { imports: [HighlightDirective] }); v.trigger("p", "mouseenter"); assert.equal(v.query("p").style.backgroundColor, "lightblue");'''),
  ("Fond retiré à la sortie", r'''const v = render("<p appHighlight>Texte</p>", { imports: [HighlightDirective] }); v.trigger("p", "mouseenter"); v.trigger("p", "mouseleave"); assert.equal(v.query("p").style.backgroundColor, "");'''),
  ("Pas de fond avant le survol", r'''const v = render("<p appHighlight>Texte</p>", { imports: [HighlightDirective] }); assert.equal(v.query("p").style.backgroundColor, "");''')],
 ["`@HostListener('mouseenter') onEnter() { ... }` écoute un événement de l'élément hôte.", "`this.el.nativeElement.style.backgroundColor = this.appHighlight` applique la couleur."],
 r'''
import { Directive, ElementRef, HostListener, Input, inject } from '@angular/core';

@Directive({ selector: '[appHighlight]' })
export class HighlightDirective {
  @Input() appHighlight = 'yellow';
  private el = inject<ElementRef<HTMLElement>>(ElementRef);

  @HostListener('mouseenter')
  onEnter() {
    this.el.nativeElement.style.backgroundColor = this.appHighlight || 'yellow';
  }

  @HostListener('mouseleave')
  onLeave() {
    this.el.nativeElement.style.backgroundColor = '';
  }
}
''')

ex("directive-click-outside", "Directive clic extérieur", M, "Directive · HostListener",
 """Écris `ClickOutsideDirective` (sélecteur `[appClickOutside]`) : elle émet sa sortie `appClickOutside` quand l'utilisateur clique **en dehors** de l'élément qui la porte (utile pour fermer un menu ou une modale).
• Écoute les clics sur le `document` avec `@HostListener('document:click', ['$event'])`.
• Un clic à l'intérieur de l'élément (ou d'un de ses enfants) n'émet rien.""",
 r'''
import { Directive, ElementRef, HostListener, inject, output } from '@angular/core';

@Directive({ selector: '[appClickOutside]' })
export class ClickOutsideDirective {
  appClickOutside = output<void>();
  private el = inject<ElementRef<HTMLElement>>(ElementRef);

  // TODO : écouter document:click et émettre si la cible est hors de l'élément
}
''',
 [("Un clic à l'extérieur émet", r'''const v = render('<div><div appClickOutside (appClickOutside)="n = n + 1"><button id="in">dedans</button></div><button id="out">dehors</button></div>', { imports: [ClickOutsideDirective], props: { n: 0 } }); v.click("#out"); assert.equal(v.component.n, 1);'''),
  ("Un clic à l'intérieur n'émet pas", r'''const v = render('<div><div appClickOutside (appClickOutside)="n = n + 1"><button id="in">dedans</button></div><button id="out">dehors</button></div>', { imports: [ClickOutsideDirective], props: { n: 0 } }); v.click("#in"); assert.equal(v.component.n, 0);'''),
  ("Chaque clic extérieur émet", r'''const v = render('<div><div appClickOutside (appClickOutside)="n = n + 1">x</div><button id="out">dehors</button></div>', { imports: [ClickOutsideDirective], props: { n: 0 } }); v.click("#out"); v.click("#out"); assert.equal(v.component.n, 2);''')],
 ["`event.target` est le noeud cliqué : `this.el.nativeElement.contains(event.target as Node)` dit s'il est à l'intérieur.", "`this.appClickOutside.emit()` pour notifier le parent."],
 r'''
import { Directive, ElementRef, HostListener, inject, output } from '@angular/core';

@Directive({ selector: '[appClickOutside]' })
export class ClickOutsideDirective {
  appClickOutside = output<void>();
  private el = inject<ElementRef<HTMLElement>>(ElementRef);

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent) {
    if (!this.el.nativeElement.contains(event.target as Node)) {
      this.appClickOutside.emit();
    }
  }
}
''')

ex("directive-unless", "Directive structurelle *appUnless", H, "Directive structurelle",
 """Écris la directive structurelle `*appUnless` : l'inverse de `*ngIf`. Le contenu est affiché quand la condition est **fausse**.
`<p *appUnless="hidden">Visible</p>` → affiché si `hidden` vaut `false`.
• Utilise `TemplateRef` et `ViewContainerRef`.
• Ne crée jamais deux fois la vue : change de condition = créer ou détruire, pas dupliquer.""",
 r'''
import { Directive, Input, TemplateRef, ViewContainerRef, inject } from '@angular/core';

@Directive({ selector: '[appUnless]' })
export class UnlessDirective {
  private template = inject(TemplateRef<unknown>);
  private container = inject(ViewContainerRef);

  @Input() set appUnless(condition: boolean) {
    // TODO : afficher le template quand `condition` est faux, le retirer sinon
  }
}
''',
 [("Affiché quand la condition est fausse", r'''const v = render("<p *appUnless=\"hidden\">Visible</p>", { imports: [UnlessDirective], props: { hidden: false } }); assert.equal(v.text("p"), "Visible");'''),
  ("Masqué quand la condition est vraie", r'''const v = render("<p *appUnless=\"hidden\">Visible</p>", { imports: [UnlessDirective], props: { hidden: true } }); assert.equal(v.query("p"), null);'''),
  ("Réagit aux changements", r'''const v = render("<p *appUnless=\"hidden\">Visible</p>", { imports: [UnlessDirective], props: { hidden: false } }); v.component.hidden = true; v.detectChanges(); assert.equal(v.query("p"), null); v.component.hidden = false; v.detectChanges(); assert.equal(v.queryAll("p").length, 1);'''),
  ("Jamais de doublon", r'''const v = render("<p *appUnless=\"hidden\">Visible</p>", { imports: [UnlessDirective], props: { hidden: 0 } }); v.component.hidden = false; v.detectChanges(); v.component.hidden = null; v.detectChanges(); assert.equal(v.queryAll("p").length, 1);''')],
 ["`this.container.createEmbeddedView(this.template)` crée la vue ; `this.container.clear()` la détruit.", "Mémorise dans un booléen si la vue est déjà affichée pour éviter les doublons."],
 r'''
import { Directive, Input, TemplateRef, ViewContainerRef, inject } from '@angular/core';

@Directive({ selector: '[appUnless]' })
export class UnlessDirective {
  private template = inject(TemplateRef<unknown>);
  private container = inject(ViewContainerRef);
  private shown = false;

  @Input() set appUnless(condition: boolean) {
    if (!condition && !this.shown) {
      this.container.createEmbeddedView(this.template);
      this.shown = true;
    } else if (condition && this.shown) {
      this.container.clear();
      this.shown = false;
    }
  }
}
''')

# ───────────────────────── Services / HTTP ─────────────────────────
ex("service-cart", "Service panier (signals)", E, "Service · Signals",
 """Complète `CartService`, un service injectable qui gère un panier avec des signaux :
• `add(product)` : ajoute un produit `{ id, name, price }` ; s'il est déjà dans le panier, incrémente sa quantité ;
• `remove(id)` : retire la ligne correspondante ;
• `count` (computed) : nombre total d'articles (somme des quantités) ;
• `total` (computed) : somme des `price × quantité` ;
• `clear()` : vide le panier.""",
 r'''
import { Injectable, computed, signal } from '@angular/core';

export interface Product {
  id: number;
  name: string;
  price: number;
}

export interface CartLine extends Product {
  qty: number;
}

@Injectable({ providedIn: 'root' })
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
import { Injectable, computed, signal } from '@angular/core';

export interface Product {
  id: number;
  name: string;
  price: number;
}

export interface CartLine extends Product {
  qty: number;
}

@Injectable({ providedIn: 'root' })
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
 """Complète `UserService`, qui utilise `HttpClient` :
• `getActiveUsers()` : GET `/api/users?active=true` (paramètre de requête via `params`) ; la réponse est un tableau `{ id, name }` ; retourne un Observable des **noms** seulement ;
• en cas d'erreur HTTP, `getActiveUsers()` retourne un tableau vide (`catchError`) ;
• `getUser(id)` : GET `/api/users/:id`, retourne l'utilisateur tel quel.""",
 r'''
import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, map, of } from 'rxjs';

export interface User {
  id: number;
  name: string;
}

@Injectable({ providedIn: 'root' })
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
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, map, of } from 'rxjs';

export interface User {
  id: number;
  name: string;
}

@Injectable({ providedIn: 'root' })
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
 """Écris `authInterceptor` (un `HttpInterceptorFn`) : il ajoute l'en-tête `Authorization: Bearer <token>` à chaque requête sortante.
• Le token vient de `TokenService.token()` (signal, `null` si non connecté) — utilise `inject()` dans l'intercepteur ;
• sans token, la requête part inchangée (pas d'en-tête) ;
• les requêtes HttpRequest sont immuables : utilise `req.clone(...)`.""",
 r'''
import { HttpInterceptorFn } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
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
import { Injectable, inject, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
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
 """`SearchComponent` interroge `SearchService.search(q)` pendant la frappe. Branche le flux de `query.valueChanges` :
• `debounceTime(300)` : attend 300 ms sans frappe ;
• n'appelle le service que pour 2 caractères minimum ;
• `distinctUntilChanged()` : pas de nouvel appel pour la même valeur ;
• `switchMap` : une réponse tardive d'une ancienne recherche est ignorée ;
• les résultats arrivent dans le signal `results`, affichés en `<li data-test="result">`.
Désabonne proprement avec `takeUntilDestroyed()`.""",
 r'''
import { Component, inject, Injectable, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Observable, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, filter, switchMap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
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
  results = signal<string[]>([]);

  constructor() {
    // TODO : query.valueChanges.pipe(...).subscribe(r => this.results.set(r))
  }
}
''',
 [("Attend 300 ms avant de chercher", r'''const calls = []; const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => { calls.push(q); return require("rxjs").of([q + "-1"]); } } }] }); v.type("[data-test=search]", "ng"); assert.equal(calls.length, 0); await wait(380); assert.deepEqual(calls, ["ng"]);'''),
  ("Affiche les résultats", r'''const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => require("rxjs").of([q + "-1", q + "-2"]) } }] }); v.type("[data-test=search]", "ng"); await wait(380); await v.stable(); assert.deepEqual(v.queryAll("[data-test=result]").map((e) => e.textContent.trim()), ["ng-1", "ng-2"]);'''),
  ("Une seule recherche pour une rafale de frappes", r'''const calls = []; const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => { calls.push(q); return require("rxjs").of([]); } } }] }); v.type("[data-test=search]", "ng"); await wait(100); v.type("[data-test=search]", "ngx"); await wait(100); v.type("[data-test=search]", "ngxs"); await wait(380); assert.deepEqual(calls, ["ngxs"]);'''),
  ("Ignore moins de 2 caractères", r'''const calls = []; const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => { calls.push(q); return require("rxjs").of([]); } } }] }); v.type("[data-test=search]", "a"); await wait(380); assert.equal(calls.length, 0);'''),
  ("Pas de nouvel appel pour la même valeur", r'''const calls = []; const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => { calls.push(q); return require("rxjs").of([]); } } }] }); v.type("[data-test=search]", "angular"); await wait(380); v.type("[data-test=search]", "angular"); await wait(380); assert.equal(calls.length, 1);'''),
  ("Ignore la réponse d'une ancienne recherche (switchMap)", r'''const { timer } = require("rxjs"); const { map } = require("rxjs/operators"); const v = render(SearchComponent, { providers: [{ provide: SearchService, useValue: { search: (q) => timer(q === "ab" ? 400 : 20).pipe(map(() => [q])) } }] }); v.type("[data-test=search]", "ab"); await wait(340); v.type("[data-test=search]", "abc"); await wait(340); await wait(500); await v.stable(); assert.deepEqual(v.queryAll("[data-test=result]").map((e) => e.textContent.trim()), ["abc"]);''')],
 ["`this.query.valueChanges.pipe(debounceTime(300), filter(q => q.length >= 2), distinctUntilChanged(), switchMap(q => this.service.search(q)), takeUntilDestroyed())`.", "Appelle `.subscribe(r => this.results.set(r))` à la fin du pipe.", "`takeUntilDestroyed()` sans argument ne marche que dans le constructeur (contexte d'injection)."],
 r'''
import { Component, inject, Injectable, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Observable, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, filter, switchMap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
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
  results = signal<string[]>([]);

  constructor() {
    this.query.valueChanges
      .pipe(
        debounceTime(300),
        filter((q) => q.length >= 2),
        distinctUntilChanged(),
        switchMap((q) => this.service.search(q)),
        takeUntilDestroyed(),
      )
      .subscribe((r) => this.results.set(r));
  }
}
''')

pathlib.Path(__file__).resolve().parent.parent.joinpath("public/data/exercises.json").write_text(
    json.dumps(X, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(X), "exercices")
