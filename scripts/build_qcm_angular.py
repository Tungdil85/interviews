"""Génère public/data/qcm-angular.json (questions originales)."""
import json, pathlib

E, M, H = "easy", "medium", "hard"
Q = [
(E, "Comment lit-on la valeur d'un signal `count` dans le code TypeScript ?", ["count", "count()", "count.value", "count.get()"], [1],
 "Un signal est une fonction : on l'appelle pour lire sa valeur (`count()`). Dans un template on écrit aussi `{{ count() }}`.", None),
(E, "Quelle méthode modifie la valeur d'un signal inscriptible en fonction de sa valeur précédente ?", ["count.set(fn)", "count.update(fn)", "count.mutate(fn)", "count.next(fn)"], [1],
 "`set(valeur)` remplace la valeur, `update(fn)` calcule la nouvelle valeur à partir de l'ancienne. `mutate` a été retiré.", None),
(M, "Que garantit un `computed()` ?", ["Il est recalculé à chaque détection de changement", "Il est en lecture seule, évalué paresseusement et mémoïsé tant que ses dépendances ne changent pas", "Il peut être modifié avec set()", "Il s'exécute uniquement au démarrage de l'application"], [1],
 "`computed` dérive une valeur d'autres signaux : lecture seule, calcul paresseux (à la première lecture) et mise en cache jusqu'à changement d'une dépendance.", None),
(M, "À quoi sert principalement `effect()` ?", ["À dériver une valeur d'autres signaux", "À exécuter des effets de bord (log, stockage, synchro externe) quand des signaux lus changent", "À remplacer le pipe async", "À déclarer des routes"], [1],
 "`effect` sert aux effets de bord. Pour dériver une valeur, utilise `computed` ; évite d'écrire dans d'autres signaux depuis un effect.", None),
(E, "Quelle syntaxe de template est la bonne pour une condition avec le nouveau control flow ?", ["*ngIf=\"cond\"", "@if (cond) { ... }", "{% if cond %}", "<ng-if cond>"], [1],
 "Depuis Angular 17, `@if`, `@for`, `@switch` sont intégrés au compilateur. `*ngIf` est déprécié.", None),
(E, "Que doit obligatoirement contenir un bloc `@for` ?", ["Une clause `track`", "Un pipe async", "Un `*ngFor`", "Un `trackBy` facultatif"], [0],
 "`@for (item of items; track item.id)` : `track` est obligatoire pour que le DOM soit réutilisé efficacement.", None),
(E, "Depuis Angular 19, que faut-il écrire pour déclarer un composant standalone ?", ["standalone: true est obligatoire", "Rien : les composants sont standalone par défaut", "Il faut déclarer le composant dans un NgModule", "Il faut utiliser @Standalone()"], [1],
 "Depuis la v19, `standalone: true` est la valeur par défaut. Pour un composant lié à un NgModule il faudrait écrire `standalone: false`.", None),
(E, "Comment déclare-t-on une entrée obligatoire avec l'API signal ?", ["@Input() name!: string", "name = input.required<string>()", "name = input<string>()!", "name = required('name')"], [1],
 "`input.required<T>()` crée une entrée signal sans valeur par défaut ; le parent doit la fournir.", None),
(M, "Quels cas déclenchent la vérification d'un composant `OnPush` ?", ["Changement de référence d'un @Input / input()", "Événement DOM déclenché dans son template", "Changement d'un signal lu dans son template", "Un setTimeout dans un autre composant sans rapport"], [0, 1, 2],
 "OnPush vérifie le composant sur changement d'input (référence), événement de son template, signal lu qui change, `markForCheck` ou `async` pipe qui émet. Pas à cause d'un timer sans lien.", None),
(E, "Quelle fonction permet de récupérer un service sans passer par le constructeur ?", ["get()", "inject()", "resolve()", "require()"], [1],
 "`inject(MonService)` fonctionne dans un contexte d'injection (champ de classe, constructeur, factory) et facilite l'héritage et les fonctions réutilisables.", None),
(E, "Que signifie `@Injectable({ providedIn: 'root' })` ?", ["Le service est instancié par composant", "Le service est un singleton disponible dans toute l'application et tree-shakable", "Le service n'est utilisable que dans AppComponent", "Le service est chargé en lazy loading uniquement"], [1],
 "`providedIn: 'root'` enregistre le service dans l'injecteur racine : une instance unique, supprimée du bundle si inutilisée.", None),
(E, "Comment active-t-on HttpClient dans une application standalone ?", ["imports: [HttpClientModule] dans AppComponent", "provideHttpClient() dans les providers de l'application", "new HttpClient() dans le service", "Il est actif par défaut"], [1],
 "On ajoute `provideHttpClient()` (avec éventuellement `withFetch()`, `withInterceptors([...])`) dans `ApplicationConfig`.", None),
(M, "Quel est le bon format d'un guard de route moderne ?", ["Une classe implémentant CanActivate obligatoirement", "Une fonction `CanActivateFn` pouvant utiliser inject()", "Un décorateur @Guard", "Un pipe"], [1],
 "Les guards fonctionnels (`CanActivateFn`) sont la forme recommandée ; les guards à classe sont dépréciés.", None),
(E, "Comment charger paresseusement un composant standalone dans une route ?", ["component: lazy(MonComposant)", "loadComponent: () => import('./mon').then(m => m.Mon)", "lazy: true", "loadModule: ..."], [1],
 "`loadComponent` avec un `import()` dynamique crée un chunk séparé chargé à la navigation.", None),
(M, "Dans quel ordre s'exécutent ces hooks ?", ["ngOnInit, ngOnChanges, ngAfterViewInit", "ngOnChanges, ngOnInit, ngAfterViewInit", "ngAfterViewInit, ngOnInit, ngOnChanges", "ngOnInit, ngAfterViewInit, ngOnChanges"], [1],
 "constructor → ngOnChanges → ngOnInit → ngDoCheck → ngAfterContentInit → ngAfterViewInit → … → ngOnDestroy.", None),
(M, "À quoi sert un bloc `@defer` ?", ["À retarder le chargement d'une partie du template et de ses dépendances (viewport, idle, interaction…)", "À différer l'envoi d'une requête HTTP", "À mettre un composant en cache", "À désactiver la détection de changement"], [0],
 "`@defer (on viewport) { <heavy-cmp /> } @placeholder { ... }` charge le code du composant à la demande, réduisant le bundle initial.", None),
(M, "Quelle différence entre un pipe pur et un pipe impur ?", ["Aucune", "Un pipe pur n'est recalculé que si ses entrées changent (référence) ; un impur l'est à chaque cycle de détection", "Le pur est asynchrone", "L'impur est mis en cache"], [1],
 "Par défaut `pure: true`. Un pipe impur (`pure: false`) s'exécute à chaque cycle : à réserver aux cas particuliers (ex. `async`).", None),
(E, "Que fait le pipe `async` ?", ["Il convertit une valeur en Promise", "Il s'abonne à un Observable/Promise, expose la dernière valeur et se désabonne automatiquement", "Il rend la requête HTTP synchrone", "Il retarde le rendu de 1 seconde"], [1],
 "`async` gère l'abonnement/désabonnement et déclenche la détection de changement : idéal avec OnPush.", None),
(M, "Comment réaliser un binding bidirectionnel avec les signaux ?", ["input() + output() sont suffisants sans rien d'autre", "model() permet d'écrire `[(value)]` côté parent", "@TwoWay()", "ngModel uniquement"], [1],
 "`model<T>()` crée une entrée/sortie signal combinée ; le parent peut lier `[(value)]=\"state\"`.", None),
(H, "À quoi sert `linkedSignal` ?", ["Lier deux composants", "Créer un signal inscriptible dont la valeur est réinitialisée par un calcul dépendant d'autres signaux", "Convertir un Observable en signal", "Partager un signal entre onglets"], [1],
 "`linkedSignal` est un signal modifiable via `set` mais qui repart d'une valeur dérivée quand sa source change (ex. sélection réinitialisée quand la liste change).", None),
(M, "Comment éviter les fuites mémoire d'un abonnement dans un composant, sans `ngOnDestroy` ?", ["takeUntilDestroyed()", "Ne jamais s'abonner", "unsubscribe() dans le constructeur", "setTimeout"], [0],
 "`takeUntilDestroyed()` (de `@angular/core/rxjs-interop`) complète l'Observable à la destruction du contexte d'injection.", None),
(M, "Quelle est la différence entre `@ViewChild` et `@ContentChild` ?", ["Aucune", "ViewChild interroge le template du composant ; ContentChild interroge le contenu projeté via <ng-content>", "ContentChild n'existe plus", "ViewChild ne fonctionne qu'avec des directives"], [1],
 "View = ce que le composant déclare dans son propre template ; Content = ce que le parent projette entre ses balises. Les versions signal sont `viewChild()` et `contentChild()`.", None),
(E, "Comment projeter le contenu fourni par le parent dans un composant ?", ["<ng-content></ng-content>", "<router-outlet>", "<ng-template-outlet>", "@Content()"], [0],
 "`<ng-content>` (éventuellement avec `select`) définit où le contenu projeté apparaît.", None),
(H, "Quelle est la cause classique de l'erreur NG0100 ExpressionChangedAfterItHasBeenChecked ?", ["Un template trop long", "Une valeur liée change pendant la vérification (ex. un enfant modifie un état lu par le parent après son rendu)", "Un import manquant", "Un guard asynchrone"], [1],
 "En mode dev, Angular revérifie après le cycle ; si une liaison a changé entre-temps (effets de bord dans un getter, hooks tardifs), il lève NG0100.", None),
(M, "Comment enregistre-t-on un interceptor HTTP fonctionnel ?", ["provideHttpClient(withInterceptors([monInterceptor]))", "providers: [{provide: HTTP_INTERCEPTORS ...}] uniquement", "app.use(interceptor)", "@Interceptor()"], [0],
 "`withInterceptors([...])` accepte des fonctions `HttpInterceptorFn(req, next)`.", None),
(E, "Quel mécanisme permet à un enfant de notifier son parent avec l'API moderne ?", ["output()", "input()", "inject(Parent)", "signal()"], [0],
 "`clicked = output<string>()` puis `this.clicked.emit('x')`. Le parent écoute avec `(clicked)=\"...\"`.", None),
(M, "Quel est l'intérêt de `ChangeDetectionStrategy.OnPush` ?", ["Il désactive Angular", "Il limite les vérifications aux cas où le composant peut avoir changé, améliorant les performances", "Il rend le composant immuable", "Il force un rendu serveur"], [1],
 "OnPush réduit le travail de détection de changement ; il est recommandé par défaut, surtout combiné aux signaux.", None),
(M, "Quel est l'avantage des formulaires réactifs sur les formulaires pilotés par le template ?", ["Aucun", "Le modèle est défini dans le code (FormGroup/FormControl), plus testable et adapté aux validations complexes", "Ils n'ont pas de validation", "Ils ne fonctionnent qu'avec ngModel"], [1],
 "Les Reactive Forms exposent un modèle explicite et synchrone, composable et facile à tester.", None),
(H, "Comment écrire un test de composant avec attente des tâches asynchrones stables ?", ["await fixture.whenStable()", "sleep(1000)", "fixture.destroy()", "TestBed.flush()"], [0],
 "Avec TestBed : `fixture.detectChanges()` pour rendre, `await fixture.whenStable()` pour attendre promesses/effets en cours.", None),
(H, "Que permet `host: { '[class.active]': 'isActive()' }` dans @Component ?", ["Définir des liaisons et listeners sur l'élément hôte sans @HostBinding/@HostListener", "Changer le sélecteur", "Déclarer un host Docker", "Créer un composant enfant"], [0],
 "La propriété `host` du décorateur remplace `@HostBinding` / `@HostListener`, et est recommandée aujourd'hui.", None),
(M, "Comment les providers déclarés dans la liste `providers` d'un composant se comportent-ils ?", ["Singleton global", "Une nouvelle instance est créée pour chaque instance du composant (et ses enfants)", "Ils sont ignorés", "Ils sont partagés entre routes"], [1],
 "Les providers de composant créent un injecteur d'élément : utile pour un état local isolé par instance.", None),
]

out = []
for i, (d, q, opts, ans, expl, code) in enumerate(Q, 1):
    item = {"id": f"ng-{i:03d}", "category": "angular", "difficulty": d, "question": q}
    if code: item["code"] = code
    item.update({"options": opts, "answer": ans, "explanation": expl})
    out.append(item)
pathlib.Path(__file__).resolve().parent.parent.joinpath("public/data/qcm-angular.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(out), "questions angular")
