# Space Invaders — rapport d'adaptation structurelle et d'optimisation

24 novembre 2026

Le jeu est passé d'un script procédural de 193 lignes, basé sur des variables globales, à un projet de 10 modules et 8 classes (525 lignes), en 36 commits du 10 au 23 novembre 2026. Les optimisations portent surtout sur le chargement des ressources et la régularité de la boucle de jeu.

## Structure d'origine

Le point de départ est un tutoriel Space Invaders écrit comme un seul script : pas de fonction principale, pas de classe, tout en variables globales. Au premier commit, il était déjà découpé en six fichiers, mais par simple copier-coller : les morceaux ne s'importaient pas entre eux.

| Fichier d'origine | Lignes | Contenu |
| --- | --- | --- |
| `main.py` | 94 | La boucle de jeu, avec toute la logique dedans |
| `objets/affichage.py` | 36 | Fenêtre, fond, musique, score, texte game over |
| `objets/ennemi.py` | 29 | Cinq listes parallèles pour 6 ennemis |
| `objets/arme.py` | 15 | Une seule balle, en variables globales |
| `objets/perso.py` | 11 | Position du joueur en variables globales |
| `objets/physique` | 8 | `isCollision()` par calcul de distance |

Cinq limites rendaient ce code difficile à faire évoluer :

- **Variables globales partout.** `playerX`, `bulletY`, `bullet_state`, `score_value` sont modifiées depuis n'importe où.
- **Ennemis en listes parallèles.** `enemyX[i]`, `enemyY[i]`, `enemyX_change[i]`, `enemyY_change[i]`, `enemyImg[i]` : un ennemi est éparpillé sur cinq listes, et leur nombre est fixé à 6.
- **Une seule balle.** Impossible de tirer tant que la précédente n'a pas quitté l'écran.
- **Valeurs écrites en dur.** `736`, `480`, `440`, `27` : la taille de l'écran (800×600) est recopiée sous forme de nombres dans toute la boucle.
- **Vitesse dépendante de la machine.** Aucune limite d'images par seconde : le jeu va plus vite sur un ordinateur plus rapide.

## Adaptation structurelle

Chaque élément du jeu est devenu un objet qui porte ses propres données, et chaque fichier a désormais un seul rôle.

| Élément | Avant | Après |
| --- | --- | --- |
| Joueur | `playerX`, `playerY` globales + fonction `player()` | Classes `Player` et `Avion` : position, vitesse, 9 images selon les vies et l'inclinaison |
| Ennemis | 5 listes parallèles, 6 ennemis fixes | Classes `Ennemi` et `Extra`, une liste d'objets, un nouvel ennemi toutes les 500 ms |
| Tir | 1 balle en variables globales | Classes `Bullet` et `Weapon` : 2 balles par tir, cadence de 600 ms, nombre de balles libre |
| Collision | Distance entre deux points inférieure à 27 | Hitbox rectangulaire par objet + `colliderect()`, dans `physique.py` |
| Sons | Chargés et joués au milieu de la boucle | Classe `Sons` : musique et 3 bruitages |
| État de la partie | Variables globales dispersées | Classe `Partie` : fond, joueur, vies, score, timers, arme, ennemis |
| Initialisation | Code au niveau module, exécuté à l'import | Fonctions `init_*` dans `end/init.py` |
| Clavier | Événements `KEYDOWN` / `KEYUP` + `playerX_change` | `get_pressed()` : déplacement et tir continus |
| Boucle | Code au niveau module | Fonction `main()` + `if __name__ == "__main__"` |
| Ressources | Fichiers à la racine, noms écrits en dur | Sous-dossiers `images/` et `audio/` + `asset_paths.py` |

### Arborescence actuelle

```text
GAME/
  main.py           démarrage + boucle de jeu
  jeu.py            classe Partie
  asset_paths.py    chemins des images et des sons
  classes/
    player.py       Player, Avion
    ennemi.py       Ennemi, Extra
    arme.py         Bullet, Weapon
  end/
    init.py         taille d'écran, limites, création des objets
    affichage.py    score, barre de vie, game over
    physique.py     collisions
    audio.py        classe Sons
  assets/           images/ et audio/
  doc/              ROADMAP.md et phases prépa (PP/)
```

### Étapes

| Période | Travail |
| --- | --- |
| 10-11 novembre | Création du dépôt, premier découpage en fichiers, documentation et roadmap |
| 11-13 novembre | Passage en classes (joueur, arme et balles, ennemis), dossier `classes/`, fichier d'initialisation, collisions par hitbox |
| 17 novembre | Score, barre de vie, game over, images d'avion selon les dégâts, fond défilant, bruitages |
| 23 novembre | Rangement des ressources et `asset_paths.py` ; classes `Partie` et `Sons`, `main.py` réduit de 158 à 126 lignes |

## Optimisations apportées

La plupart suivent la même idée : charger une ressource une seule fois au démarrage, et ne rien faire d'inutile dans la boucle, qui tourne 60 fois par seconde.

| Problème | Solution | Effet |
| --- | --- | --- |
| Sons relus sur le disque à chaque tir et à chaque collision | Classe `Sons` : tout est chargé une fois au démarrage | Plus d'accès disque pendant le jeu |
| Images du joueur rechargées à chaque tour de boucle | Les 9 images sont chargées et redimensionnées une fois dans `init_player()` | A corrigé une chute du nombre d'images par seconde |
| Images affichées dans leur format de fichier | `convert()` et `convert_alpha()` au chargement | Affichage plus rapide à chaque image |
| Vitesse du jeu liée à la machine | `clock.tick(60)` + timers basés sur `dt` (apparition, score, bonus) | Même vitesse sur tous les ordinateurs |
| Deux `print` à chaque tour de boucle | Supprimés | 120 écritures console par seconde en moins |
| Fenêtre créée trois fois (`set_mode`) | Un seul appel, dans `main()` | Démarrage propre, ordre d'initialisation clair |
| Collision par racine carrée et puissance, entre deux points | `colliderect()` entre deux rectangles | Calcul plus simple et collision fidèle à la taille des images |
| Objets jamais retirés (ennemis replacés, balle recyclée) | Balles et ennemis supprimés des listes dès qu'ils sortent ou sont touchés | Les listes ne contiennent que les objets actifs |
| Dictionnaire d'images global écrasé au chargement | Un nouveau dictionnaire est construit à chaque initialisation | La partie peut être relancée sans plantage |
| Code de chargement des sons répété trois fois | Méthode `_charger(nom, volume)` | Un bruitage ajouté = une ligne |
| `__pycache__` et `.venv` suivis par git | Ajoutés au `.gitignore` | Fin des conflits de fusion sur des fichiers générés |

## Limites restantes

Quatre points ne sont pas encore traités ; le détail est dans la roadmap.

- `enemy.png` est encore relu à chaque apparition d'ennemi, et `bullet.png` à chaque tir, sans `convert_alpha()`.
- L'affichage et la logique restent mêlés : `Bullet.update()` déplace et dessine, et la boucle de `main()` alterne calcul et dessin.
- Les constantes (tailles, vitesses, délais) sont réparties dans cinq fichiers.
- `Ennemi` utilise `enemyX` / `enemyY` là où les autres classes utilisent `x` / `y`, ce qui empêche une classe mère commune.
