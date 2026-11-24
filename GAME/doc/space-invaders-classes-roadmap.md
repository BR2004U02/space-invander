# Space Invaders — classes à créer et roadmap

23 novembre 2026

Six éléments du jeu méritent leur propre classe, et le travail restant tient en cinq blocs : finir la réorganisation, optimiser avec la matière du cours, ajouter le menu, les fonctionnalités bonus, puis le compte rendu.

## Ce qui devrait devenir une classe

| Élément actuel | Classe | Pourquoi |
| --- | --- | --- |
| `spawn_timer` + liste `ennemis` + `init_ennemy()` + la boucle de déplacement | `EnnemiManager` | Tout ce qui concerne les ennemis est éparpillé entre `main`, `Partie` et `init.py`. C'est le `TODO` déjà noté dans le code. |
| `x`, `y`, image, hitbox, `afficher()` répétés dans `Avion`, `Extra`, `Bullet` | `Entite` (classe mère) | Supprime la duplication. Demande d'abord de renommer `enemyX`/`enemyY` en `x`/`y`. |
| `background`, `background_y1`, `background_y2` + le défilement | `Fond` | Un objet avec `update()` et `afficher()`, comme les autres. |
| `score`, `score_timer`, `bonus_timer` | `Score` | Méthodes `update(dt)` et `ajouter(points)`. |
| Le tuple de 6 valeurs de `init_vie()` | `BarreDeVie` | `vies`, `max_vies` et les dimensions vont ensemble. |
| La boucle + le futur menu + le game over | `Game` avec des états | Menu → partie → game over → rejouer. |

**À ne pas mettre en classe** : les constantes (un module `config.py` suffit), les chemins d'assets, et les fonctions de collision, qui n'ont pas d'état à garder.

## Roadmap

Le bloc 4 dépend du bloc 1 : avec `Entite` et `EnnemiManager` en place, un nouvel ennemi ou une nouvelle arme devient une sous-classe de dix lignes.

### 1. Finir la réorganisation

- [ ] `config.py` : toutes les constantes (tailles, vitesses, délais, points).
- [ ] Charger `enemy.png` et `bullet.png` une seule fois.
- [ ] Renommer `enemyX`/`enemyY`, puis créer `Entite`.
- [ ] `Bullet` : séparer `update()` et `afficher()`, retirer `screen`.
- [ ] Créer `Fond`, `Score`, `BarreDeVie`, `EnnemiManager`.
- [ ] `Partie.update(dt)` + `dessiner_partie(screen, partie)` : `main` tombe à environ 25 lignes.
- [ ] Sortir les sons de `physique.py`.
- [ ] Nettoyage : code mort, `postion_ennemi`, `hitbox.y` dans `fire()`, `__pycache__` encore suivi par git sous `GAME/END/`.

### 2. Optimisation avec la matière du cours

- [ ] `@property` pour la hitbox, calculée depuis `x`/`y` au lieu d'être resynchronisée à la main.
- [ ] Un décorateur de cache pour le chargement des images.
- [ ] Un décorateur `@chronometre` pour mesurer les fonctions lentes, à la place de `test_fps.py`.
- [ ] `@dataclass` pour la configuration.

### 3. Menu et états

- [ ] Classe `Game`, écran menu avec bouton « Jouer », rejouer après un game over.
- [ ] Taille d'écran dynamique.

### 4. Fonctionnalités bonus

Dans l'ordre le plus simple à implémenter.

- [ ] Hitbox du joueur + collision joueur/ennemi.
- [ ] Ennemis différents (sous-classes d'`Ennemi`) + barre de vie ennemi.
- [ ] Armes différentes (sous-classes de `Weapon`).
- [ ] Tir des ennemis.
- [ ] Bonus en jeu, obstacles.
- [ ] Niveaux, puis boss.

### 5. Compte rendu

- [ ] Noter les choix d'architecture au fur et à mesure.
- [ ] Une phase prépa par fonctionnalité dans `doc/PP/`.
