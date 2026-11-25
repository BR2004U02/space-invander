# Space Invaders — Rapport de conception

**Luka Parmentier** et **Roméo** — UE43 Programmation, HELMo A2 — novembre 2026

**Dépôt GitHub :** <https://github.com/Brukzer/Space-invander>

---

## 1. Analyse du programme initial

Le programme de départ est un script procédural de 193 lignes réparties en six fichiers, mais ce découpage est trompeur : les fichiers ne s'importent pas entre eux et partagent un espace de noms global unique. Toute la logique tient dans une boucle `while` de 80 lignes.

**L'état du jeu est global et dispersé.** `playerX`, `bulletY`, `bullet_state`, `score_value` sont des variables modifiables depuis n'importe quel point du programme. Aucun objet ne possède ses propres données, donc rien ne garantit la cohérence : `fire_bullet()` modifie `bullet_state` via `global`, et la boucle la relit vingt lignes plus loin.

**Les entités sont représentées par des listes parallèles.** Un ennemi n'existe pas en tant qu'objet : il est éparpillé sur cinq listes indexées par le même `i`.

```python
enemyImg, enemyX, enemyY = [], [], []
enemyX_change, enemyY_change = [], []
num_of_enemies = 6
```

Ajouter un attribut — des points de vie, par exemple — impose de créer une sixième liste et de modifier chaque boucle qui itère sur les ennemis. Le nombre d'ennemis est figé à six, et un ennemi « détruit » n'est pas supprimé mais repositionné au hasard, ce qui rend impossible toute notion de flotte variable.

**Aucune abstraction ne permet la variation.** Il n'existe qu'une seule balle, représentée par les variables `bulletX`, `bulletY` et `bullet_state` : le joueur ne peut pas tirer tant que la précédente n'a pas quitté l'écran. Créer un second type d'ennemi ou une seconde arme supposerait de dupliquer tout le jeu de variables et toutes les boucles associées.

**Logique et affichage sont confondus.** La fonction `fire_bullet()` change l'état de la balle *et* la dessine dans le même appel. Il est donc impossible de calculer une image de jeu sans l'afficher, donc impossible de tester quoi que ce soit sans ouvrir une fenêtre.

**Les valeurs sont écrites en dur et la vitesse dépend de la machine.** Les nombres `736`, `480`, `440` et `27` encodent implicitement une fenêtre de 800 × 600. Surtout, aucune limite d'images par seconde n'est fixée et les déplacements s'expriment en pixels par image : le jeu tourne deux fois plus vite sur un ordinateur deux fois plus rapide.

**Conséquence.** Chacune de ces limites conduit au même résultat : la moindre évolution oblige à rouvrir la boucle principale et à y insérer du code, qui s'ajoute à celui déjà présent. Le coût d'un ajout croît avec la taille de ce qui existe déjà.

---

## 2. Architecture proposée

Le code est réparti en quatre packages aux responsabilités distinctes.

| Package | Rôle |
| --- | --- |
| `classes/` | Les objets du jeu : vaisseau, ennemis, projectiles, armes, score, barre de vie, fond |
| `backend/` | La logique : état d'une partie, chargement des ressources, collisions, lecture du clavier, son |
| `frontend/` | L'affichage dépendant de l'écran de fin |
| `config/` | Les constantes et les chemins des ressources |
| `assets/` | Les assets : image, sons |

`main.py` se limite à créer la fenêtre et à dérouler la boucle de jeu sous forme d'appel.

### 2.1 Hiérarchie d'héritage

![Diagramme d'héritage](heritage.png)

### 2.2 Relations de composition

![Diagramme de composition](composition.png)

---

## 3. Justification des choix

**`Entite` comme racine de tout ce qui s'affiche.** Le vaisseau, les ennemis et les projectiles partagent exactement quatre données — une position, une image, une boîte de collision — et un comportement : se dessiner. Les rassembler dans une classe mère évite d'écrire quatre fois le même `afficher()` et garantit que tout objet possède une hitbox, condition nécessaire au fonctionnement des collisions.

**Séparer le déplacement de l'affichage par héritage multiple.** `Player` décrit comment un vaisseau se déplace, `Ennemi` comment un ennemi patrouille et descend ; ni l'un ni l'autre ne sait s'afficher. `Avion` et `Extra` combinent chacun une logique de déplacement avec `Entite` :

```python
class Extra(Ennemi, Entite):
    def __init__(self, x, y, limite_gauche, limite_droite, limite_bas, enemyImg, dh, dv):
        Ennemi.__init__(self, x, y, 5, 1, limite_gauche, limite_droite, limite_bas, dh, dv)
        Entite.__init__(self, x, y, enemyImg)
```

L'intérêt est de pouvoir faire varier les deux axes indépendamment : un nouvel ennemi change sa façon de bouger sans toucher à son affichage. Ce choix a un coût, discuté en section 5.

**`Partie` comme unique dépositaire de l'état.** Plutôt que de laisser la boucle manipuler une douzaine de variables, `Partie` compose les objets du jeu et n'expose que cinq méthodes. La boucle de `main.py` ne connaît donc ni le nombre de vies, ni la liste des ennemis, ni les timers — elle enchaîne des appels. C'est la composition, et non l'héritage, qui convient ici : une partie n'*est* pas un score, elle *possède* un score.

**Un gestionnaire dédié aux ennemis.** `EnnemiManager` concentre l'apparition, le déplacement et les tirs de la flotte. Sans lui, ces responsabilités seraient retombées dans `Partie`, qui serait redevenue le fourre-tout que la boucle initiale était déjà. Le gestionnaire permet aussi de faire dépendre la composition de la flotte du score, règle de difficulté qui n'a sa place ni dans `Partie` ni dans les classes d'ennemis.

**Des fonctions, et non des classes, pour ce qui n'a pas d'état.** `physique.py` et `controle.py` contiennent des fonctions libres. Une collision est un calcul sans mémoire, la lecture du clavier interroge un périphérique unique : aucun des deux n'a de données à conserver entre deux appels. Les transformer en classes aurait ajouté une indirection sans rien apporter.

**Des constantes centralisées.** `config/config.py` rassemble dimensions, vitesses, délais et couleurs. Équilibrer le jeu ne demande plus de parcourir cinq fichiers à la recherche de nombres isolés. La constante `REFERENCE_FRAME` — la durée d'une image à 60 ips — sert de référence à tous les déplacements, qui s'expriment désormais en `vitesse × (dt / REFERENCE_FRAME)` : la vitesse à l'écran est identique quelle que soit la machine.

---

## 4. Extensibilité

**Ajouter un type d'ennemi** demande une sous-classe et rien d'autre :

```python
class EnnemiRapide(Extra):
    def __init__(self, x, y, limite_gauche, limite_droite, limite_bas, enemyImg, dh, dv):
        super().__init__(x, y, limite_gauche, limite_droite, limite_bas, enemyImg, dh, dv)
        self.speed = 9
```

`EnnemiManager` itère sur `self.ennemis` sans connaître les types concrets ; aucune de ses lignes ne change. C'est la vérification faite en pratique : `EnnemiTireur` a été ajouté après coup, avec sa propre arme et un comportement de tir dirigé, sans modifier `main.py` ni `Partie`.

**Ajouter une arme** suit le même principe. `Weapon` expose `shoot_continuous()` et `update()` ; une sous-classe qui redéfinit la création des projectiles obtient un comportement différent sans que l'appelant s'en aperçoive :

```python
class WeaponEventail(Weapon):
    def create_2_bullets(self, x, y):
        for decalage in (-40, 0, 40):
            bullet = Bullet(self.bullet_image)
            bullet.fire(x + decalage, y)
            self.bullets.append(bullet)
```

**Faire varier un projectile** se fait au niveau de `Entite`. `EnemyBullet` se distingue de `Bullet` par un vecteur de direction calculé au moment du tir vers la position du joueur ; les deux restent des `Entite` et sont affichés par le même mécanisme.

**Modifier l'équilibrage** ne touche qu'un fichier. Changer la cadence de tir, la vitesse des ennemis ou les points par ennemi détruit se fait dans `config.py`, sans ouvrir une seule classe.

---

## 5. Limites

**Le polymorphisme est contourné là où il devrait s'appliquer.** `EnnemiManager` teste la présence d'une méthode plutôt que de l'appeler :

```python
if hasattr(ennemi, "update_tirs"):
    ennemi.update_tirs(dt, joueur)
```

Chaque nouveau comportement optionnel ajouterait un test du même genre. Le correctif consiste à définir `update_tirs()` vide dans `Extra` et à l'appeler sans condition : les ennemis qui ne tirent pas héritent d'un comportement neutre. Le même défaut affecte `verifier_collisions()`, qui teste `hasattr(ennemi, "weapon")`.

**La séparation entre logique et affichage reste incomplète.** Les classes métier portent toutes une méthode `afficher()`, et `backend/jeu.py` importe `frontend.affichage` pour l'écran de fin. Une partie ne peut donc pas être simulée sans Pygame. La correction passerait par des fonctions d'affichage recevant les objets en paramètre, les classes se limitant à leurs données.

**L'héritage multiple est fragile.** `Avion(Player, Entite)` et `Extra(Ennemi, Entite)` imposent d'appeler explicitement les deux constructeurs dans le bon ordre, `super()` ne suffisant plus. Une composition — un attribut `sprite` contenant l'`Entite` — serait plus robuste, au prix d'une indirection supplémentaire à chaque accès.

**La résistance des ennemis n'est pas implémentée.** Tous meurent au premier tir. `EnnemiBoss` existe mais est une classe vide. Un attribut `resistance` dans `Ennemi`, décrémenté à chaque collision plutôt que de supprimer l'ennemi immédiatement, suffirait à l'introduire.

**Le joueur ne dispose que d'une arme.** La seconde arme du jeu, `EnemyWeapon`, appartient aux ennemis. L'exemple de la section 4 montre que l'ajout est direct, mais il n'est pas fait.

**La création des ennemis connaît tous les types.** `init_ennemy()` contient un dictionnaire associant un nom à chaque classe, plus un cas particulier pour l'ennemi tireur, dont le constructeur prend un argument de plus. Ajouter un type impose donc de modifier cette fonction. Un registre où chaque classe s'enregistre elle-même, et une signature uniforme pour tous les constructeurs, supprimeraient ce point de passage obligé.

**Il n'existe pas de gestion d'états.** Le jeu démarre directement sur une partie et se ferme au game over. Un menu, une pause ou la possibilité de rejouer supposeraient une classe `Game` orchestrant plusieurs états, dont `Partie` ne serait qu'un.
