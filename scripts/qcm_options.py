"""Réécritures d'options pour équilibrer longueur/précision des bonnes et fausses réponses.

OVERRIDES[id] = (bonnes réponses, mauvaises réponses). L'ordre final est mélangé de façon
déterministe par `finalize`, qui recalcule les indices de réponse.
"""
import random

OVERRIDES = {
# --- Angular
"ng-003": (["Il est en lecture seule et mémoïsé : recalculé seulement si une dépendance change"],
  ["Il est recalculé à chaque cycle de détection de changement", "Il est inscriptible et modifiable avec set() à tout moment", "Il s'exécute une seule fois au démarrage de l'application"]),
"ng-004": (["Exécuter un effet de bord quand les signaux lus changent (log, stockage…)"],
  ["Dériver une valeur calculée à partir d'autres signaux en lecture seule", "Remplacer le pipe async pour s'abonner aux Observables HTTP", "Déclarer les routes lazy-loadées de l'application"]),
"ng-007": (["Rien : les composants sont standalone par défaut depuis Angular 19"],
  ["Écrire standalone: true, obligatoire dans chaque décorateur", "Déclarer le composant dans le tableau declarations d'un NgModule", "Ajouter le décorateur @Standalone() sur la classe"]),
"ng-011": (["Une instance unique partagée dans toute l'application, supprimée du bundle si inutilisée"],
  ["Une nouvelle instance créée pour chaque composant qui l'injecte", "Le service reste disponible uniquement dans AppComponent et ses enfants", "Le service n'est chargé que lorsqu'une route lazy l'utilise"]),
"ng-012": (["Ajouter provideHttpClient() aux providers de l'application"],
  ["Importer BrowserModule dans le composant racine", "Instancier new HttpClient() dans chaque service qui en a besoin", "Rien à faire : HttpClient est fourni par défaut dans chaque composant"]),
"ng-013": (["Une fonction CanActivateFn, qui peut appeler inject() pour accéder aux services"],
  ["Une classe implémentant obligatoirement l'interface CanActivate", "Un décorateur @Guard() posé sur le composant de la route", "Un pipe appliqué dans le template de la route"]),
"ng-014": (["loadComponent: () => import('./page').then(m => m.Page)"],
  ["component: lazy(Page) dans la définition de la route", "lazy: true ajouté sur la route concernée", "loadModule: () => Page avec un NgModule dédié"]),
"ng-016": (["Retarder le chargement d'une partie du template selon un déclencheur (viewport, idle…)"],
  ["Différer l'envoi d'une requête HTTP jusqu'à la fin du cycle", "Mettre en cache un composant déjà rendu pour le réutiliser", "Désactiver la détection de changement sur un sous-arbre"]),
"ng-017": (["Le pipe pur ne se réévalue que si ses entrées changent ; l'impur à chaque cycle"],
  ["Le pipe pur s'exécute à chaque cycle ; l'impur seulement au démarrage", "Le pipe pur est asynchrone ; l'impur est synchrone", "Le pipe impur met son résultat en cache, contrairement au pur"]),
"ng-018": (["S'abonne à un Observable ou une Promise, expose la dernière valeur et se désabonne seul"],
  ["Convertit n'importe quelle valeur en Promise pour l'attendre", "Rend synchrone une requête HTTP pour bloquer le rendu", "Retarde le rendu du template d'une seconde après l'émission"]),
"ng-019": (["model() crée une entrée/sortie combinée utilisable en [(value)] côté parent"],
  ["La directive ngModel est la seule solution, avec FormsModule", "Le décorateur @TwoWay() sur une propriété de la classe", "Un pipe two-way à placer dans le template du parent"]),
"ng-020": (["Créer un signal inscriptible qui se réinitialise quand un signal source change"],
  ["Lier deux composants frères pour qu'ils partagent leur état", "Convertir un Observable en signal en lecture seule", "Synchroniser un signal entre plusieurs onglets du navigateur"]),
"ng-022": (["ViewChild lit le propre template du composant ; ContentChild le contenu projeté"],
  ["ViewChild lit le contenu projeté ; ContentChild le propre template", "ContentChild est déprécié au profit de ViewChild partout", "ViewChild ne fonctionne qu'avec des directives, pas des composants"]),
"ng-024": (["Une valeur liée change pendant la vérification, après avoir déjà été évaluée"],
  ["Un template trop long qui dépasse la limite de lignes autorisée", "Un import manquant dans le tableau imports du composant", "Un guard de route asynchrone qui ne renvoie jamais de valeur"]),
"ng-025": (["provideHttpClient(withInterceptors([monInterceptor]))"],
  ["providers: [{ provide: HTTP_INTERCEPTORS, useValue: monInterceptor }]", "app.use(monInterceptor) dans le fichier de bootstrap", "Décorer la fonction avec @Interceptor() puis l'importer"]),
"ng-027": (["Il limite les vérifications aux cas où le composant a pu changer"],
  ["Il désactive complètement la détection de changement d'Angular", "Il rend le composant et son état immuables à l'exécution", "Il force le rendu côté serveur de ce composant"]),
"ng-028": (["Le modèle est explicite dans le code : testable et adapté aux validations complexes"],
  ["Ils n'offrent aucune validation, contrairement au template-driven", "Ils ne fonctionnent qu'avec la directive ngModel dans le template", "Ils exigent un NgModule dédié pour chaque formulaire"]),
"ng-030": (["Déclarer liaisons et écouteurs sur l'élément hôte sans @HostBinding"],
  ["Changer le sélecteur CSS du composant depuis son décorateur", "Configurer l'hôte du serveur de développement Angular", "Créer dynamiquement un composant enfant dans le template"]),
"ng-031": (["Une nouvelle instance par instance du composant, partagée avec ses enfants"],
  ["Un singleton global partagé par toute l'application", "Elles sont ignorées : seul providedIn: 'root' compte", "Elles sont partagées entre toutes les routes de l'application"]),
# --- CSS
"css-001": (["Le padding et la bordure sont inclus dans la largeur et la hauteur déclarées"],
  ["Le padding s'ajoute à la largeur déclarée de l'élément", "Les marges sont incluses dans la largeur déclarée", "La bordure est retirée du calcul de la hauteur"]),
"css-004": (["Équivaut à flex-grow:1, flex-shrink:1, flex-basis:0% : l'élément prend l'espace libre"],
  ["Fixe la largeur de l'élément à 1px quel que soit le contenu", "Désactive flex et remet l'élément en display:block", "Force les éléments à passer à la ligne à chaque itération"]),
"css-007": (["Se comporte comme relative puis colle au seuil défini pendant le défilement"],
  ["Fixe l'élément définitivement à l'écran, indépendamment du défilement", "Retire l'élément du flux, comme absolute, par rapport au viewport", "Équivaut à static mais autorise z-index sans autre effet"]),
"css-008": (["Les contextes d'empilement isolent les z-index de leurs descendants"],
  ["Le z-index a été retiré de la spécification CSS moderne", "Il faut ajouter !important sur la valeur du z-index", "Il faut définir opacity: 1 sur l'élément concerné"]),
"css-009": (["em dépend de la police de l'élément ou du parent ; rem de celle de <html>"],
  ["em dépend de la racine <html> ; rem de la police du parent", "Les deux dépendent de la largeur du viewport", "em vaut toujours 16px ; rem s'adapte au contenu"]),
"css-011": ([":hover est une pseudo-classe d'état ; ::before un pseudo-élément généré"],
  [":hover est un pseudo-élément ; ::before une pseudo-classe d'état", "Les deux sont des pseudo-classes, avec une syntaxe différente", "Les deux sont des pseudo-éléments qui génèrent du contenu"]),
"css-012": (["none retire l'élément du flux ; hidden le cache mais garde sa place"],
  ["none garde la place de l'élément ; hidden la libère", "Les deux retirent l'élément du DOM de la page", "none cache seulement visuellement ; hidden retire du flux"]),
"css-014": (["Retourne une valeur fluide bornée entre un minimum et un maximum"],
  ["Découpe l'élément pour qu'il ne dépasse pas son conteneur", "Arrondit la valeur au pixel entier le plus proche", "Active une animation entre deux tailles de police"]),
"css-015": (["Les marges verticales adjacentes fusionnent et seule la plus grande est conservée"],
  ["Une marge est supprimée par erreur quand elle dépasse le parent", "Un bug de Grid qui ajoute les marges de deux cellules", "Un reset CSS qui remet toutes les marges à zéro"]),
"css-017": (["Définit l'espacement entre les éléments enfants, sans marge aux bords"],
  ["Ajoute des marges autour de chaque élément, aux bords inclus", "Supprime les bordures entre les cellules adjacentes", "Aligne verticalement les éléments sur leur ligne de base"]),
"css-018": (["Styler un composant selon la taille de son conteneur, pas du viewport"],
  ["Conteneuriser une application web avec Docker pour la déployer", "Remplacer les grilles CSS par des tableaux responsive", "Adapter les styles lors de l'impression de la page"]),
"css-019": (["Remplit la boîte en gardant le ratio, quitte à rogner l'excédent"],
  ["Étire l'image pour remplir la boîte sans garder le ratio", "Réduit l'image entière pour qu'elle tienne sans rognage", "Masque l'image et affiche à la place le texte alternatif"]),
"css-020": ([":where() a une spécificité nulle ; :is() prend celle de son argument le plus fort"],
  [":is() a une spécificité nulle ; :where() prend celle du plus fort", "Les deux ont toujours la spécificité d'une classe unique", ":is() est déprécié au profit de :where() dans la spécification"]),
# --- RxJS
"rx-001": (["switchMap annule l'interne précédent ; mergeMap les exécute en parallèle"],
  ["mergeMap annule l'interne précédent ; switchMap les exécute en parallèle", "Les deux exécutent les internes l'un après l'autre en file", "switchMap est synchrone ; mergeMap toujours asynchrone"]),
"rx-003": (["Ignore les nouvelles valeurs tant que l'interne en cours n'est pas terminé"],
  ["Annule l'interne en cours dès qu'une nouvelle valeur arrive", "Met les nouvelles valeurs en file et les traite dans l'ordre", "Exécute tous les internes en parallèle sans limite"]),
"rx-004": (["BehaviorSubject a une valeur initiale et la rejoue à chaque nouvel abonné"],
  ["Subject conserve la dernière valeur et la rejoue aux abonnés", "BehaviorSubject n'émet qu'une seule fois puis se complète", "Les deux sont identiques, seul le nom change"]),
"rx-005": (["Chaque abonnement déclenche sa propre exécution de la source"],
  ["Il n'émet jamais de valeur tant qu'il n'est pas complété", "Il partage une seule exécution entre tous les abonnés", "Il est déjà terminé avant le premier abonnement"]),
"rx-006": (["Partage une seule souscription et rejoue la dernière valeur aux nouveaux abonnés"],
  ["Relance la source à chaque nouvel abonné, sans partage", "Supprime les valeurs en doublon consécutives du flux", "Retarde chaque émission d'une unité de temps"]),
"rx-007": (["Une seule fois, quand toutes les sources sont terminées, avec leurs dernières valeurs"],
  ["À chaque valeur émise par n'importe laquelle des sources", "Dès que la première source émet, puis se complète aussitôt", "Jamais tant qu'une source n'a pas émis deux valeurs"]),
"rx-009": (["Ignore une valeur identique à la précédente émission"],
  ["Trie les valeurs émises dans l'ordre croissant", "Supprime tous les doublons de l'ensemble de la séquence", "Termine le flux dès qu'une valeur est répétée"]),
"rx-010": (["catchError dans l'Observable interne, qui retourne of(valeurDeRepli)"],
  ["Un try/catch autour de l'appel à subscribe() du flux externe", "Ignorer l'erreur : le flux externe continue de lui-même", "Remplacer l'Observable HTTP par un Subject pour absorber l'erreur"]),
"rx-011": (["Termine l'abonnement dès que destroy$ émet une valeur"],
  ["Ne prend que la première valeur de la source puis se complète", "Retarde les émissions jusqu'à ce que destroy$ émette", "Filtre les valeurs jusqu'à ce que destroy$ se complète"]),
"rx-012": (["withLatestFrom n'émet que quand la source principale émet"],
  ["withLatestFrom émet à chaque émission de n'importe quelle source", "combineLatest n'émet qu'une seule fois puis se complète", "withLatestFrom est toujours asynchrone, contrairement à combineLatest"]),
"rx-013": (["Exécute un effet de bord sans modifier les valeurs du flux"],
  ["Transforme chaque valeur du flux en une autre valeur", "Filtre les valeurs qui ne respectent pas un prédicat", "Complète le flux après la première valeur émise"]),
"rx-014": (["Le timer continue : fuite mémoire et callbacks exécutés après la destruction"],
  ["Aucune conséquence : Angular stoppe seul les timers du composant", "Une erreur de compilation signale l'abonnement non géré", "L'abonnement est annulé automatiquement au prochain changement de route"]),
"rx-015": (["of émet chaque argument ; from convertit un itérable ou une Promise en Observable"],
  ["of est asynchrone alors que from est toujours synchrone", "from ne gère que les Promises, jamais les tableaux", "from ne peut convertir qu'un Observable en un autre Observable"]),
# --- TypeScript
"ts-001": (["unknown impose de restreindre le type avant usage ; any désactive le contrôle"],
  ["any est plus sûr car il impose un contrôle avant chaque usage", "unknown n'existe qu'en JavaScript et pas dans le compilateur", "Les deux sont strictement équivalents pour le compilateur"]),
"ts-004": (["Crée un type identique à User, sans la propriété password"],
  ["Supprime entièrement le type User du programme compilé", "Rend la propriété password optionnelle dans le type User", "Ajoute la propriété password à une copie du type User"]),
"ts-005": (["Le compilateur restreint le type grâce à une propriété littérale commune"],
  ["Cela réduit automatiquement la taille du bundle JavaScript généré", "Cela remplace entièrement l'usage des interfaces et des classes", "Cela accélère l'exécution du code transpilé en production"]),
"ts-007": (["L'union des noms de propriétés de User, sous forme de littéraux"],
  ["L'union des types de valeurs des propriétés de User", "Une clé de chiffrement associée au type User", "Le constructeur de la classe User sous forme de type"]),
"ts-008": (["Pour décrire des objets extensibles via extends ou la fusion de déclarations"],
  ["Jamais : type remplace interface dans tous les cas d'usage", "Pour déclarer des unions et des tuples de types", "Uniquement pour typer des fonctions et des callbacks"]),
"ts-009": (["Valider qu'une valeur respecte un type en gardant son type inféré précis"],
  ["Caster une valeur vers un type en ignorant toute vérification", "Importer un type depuis un module externe sans l'exécuter", "Déclarer qu'une classe implémente plusieurs interfaces à la fois"]),
"ts-010": (["Un booléen qui, vrai, restreint v au type string dans la branche"],
  ["Un booléen simple, sans effet sur le typage dans la branche", "Une chaîne de caractères décrivant le type de v", "void : la fonction ne retourne rien d'exploitable"]),
"ts-011": (["Court-circuite en undefined si la valeur à gauche est null ou undefined"],
  ["Déclare qu'une propriété d'une interface est optionnelle", "Compare deux valeurs en ignorant leur type", "Force le type en non-null sans vérification à l'exécution"]),
"ts-012": (["Affirme que la valeur n'est ni null ni undefined, sans vérification à l'exécution"],
  ["Nie la valeur et retourne son booléen opposé", "Convertit la valeur en booléen strict", "Lance une erreur à l'exécution si la valeur est null"]),
"ts-013": (["Un objet dont toutes les clés sont des chaînes et les valeurs des nombres"],
  ["Un tableau dont tous les éléments sont des nombres", "Un tuple fixe contenant une chaîne puis un nombre", "Une classe générique avec une clé et une valeur"]),
"ts-014": (["Le type des valeurs qui n'existent jamais, comme une fonction qui lève toujours"],
  ["Le type d'une valeur qui peut être null ou undefined", "Un alias strictement identique à void", "Un alias de unknown utilisé pour les entrées externes"]),
}

from qcm_options_patch import PATCH  # noqa: E402
OVERRIDES.update(PATCH)


def finalize(item: dict) -> dict:
    """Applique l'éventuelle réécriture, puis mélange les options (déterministe) et recalcule `answer`."""
    if item["id"] in OVERRIDES:
        correct, wrong = OVERRIDES[item["id"]]
        options = correct + wrong
        answer = list(range(len(correct)))
    else:
        options = item["options"]
        answer = item["answer"]
    order = list(range(len(options)))
    random.Random(item["id"]).shuffle(order)
    item["options"] = [options[i] for i in order]
    item["answer"] = sorted(order.index(a) for a in answer)
    return item
