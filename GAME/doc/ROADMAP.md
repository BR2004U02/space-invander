# ROADMAP

## Processus

1. Compréhension du code d'origine
2. Réorganisation en classes et en modules — objectif : morceler le code au maximum
   pour qu'un autre groupe puisse le reprendre rapidement, et que l'ajout d'ennemis
   ou d'armes se fasse par héritage
3. Optimisation selon la matière du cours (décorateurs, etc.)
4. Ajout de fonctionnalités **BONUS**

---

## Fait

### Architecture
- [x] Découpage en modules : `backend/`, `frontend/`, `classes/`, `config/`
- [x] Classe `Entite` comme base commune (position, image, hitbox, affichage)
- [x] Classe `Partie` centralisant l'état du jeu
- [x] Constantes rassemblées dans `config/config.py`
- [x] Chemins des ressources dans `config/asset_paths.py`, assets rangés en sous-dossiers
- [x] Lecture du clavier isolée dans `backend/controle.py`
- [x] `main.py` réduit à la boucle de jeu

### Jeu
- [x] Déplacement du joueur et tir continu
- [x] Trois types d'ennemis : classique, rapide, tireur
- [x] Apparition pondérée selon le score
- [x] Deux types de projectiles : tir droit du joueur, tir dirigé des ennemis
- [x] Collisions balle-ennemi, ennemi-bas, balle ennemie-joueur
- [x] Score (temps + ennemis détruits) avec bonus « +50 »
- [x] Barre de vie, états du vaisseau selon les dégâts, inclinaison au déplacement
- [x] Invulnérabilité d'une seconde avec clignotement
- [x] Fond défilant
- [x] Musique et bruitages
- [x] Écran de game over

### Optimisation
- [x] Images chargées une seule fois au démarrage (`charger_images()`)
- [x] `convert()` / `convert_alpha()` sur toutes les images
- [x] Déplacements indépendants du framerate (`dt` / `REFERENCE_FRAME`)
- [x] Suppression des objets sortis de l'écran ou détruits

### Dépôt
- [x] `requirements.txt`
- [x] `README.md` à jour
- [x] `.gitignore` complet

---

## À faire

### Priorité haute — exigences de l'énoncé
- [ ] **Polymorphisme** : supprimer les `hasattr()` de `ennemi_manager.py` au profit
      d'une méthode `update_tirs()` vide par défaut dans `Extra`
- [ ] **Seconde arme pour le joueur** : sous-classe de `Weapon` (tir en éventail,
      laser, cadence différente)
- [ ] **Points de vie des ennemis** : attribut `resistance`, le boss en nécessitant 3
- [ ] Implémenter `EnnemiBoss`, aujourd'hui une classe vide
- [ ] Rapport de conception (PDF, 5 pages) + diagramme de classes

### Priorité moyenne — séparation logique / affichage
- [ ] Sortir les méthodes `afficher()` des classes métier vers `frontend/`
- [ ] `backend/jeu.py` ne doit plus importer `frontend.affichage`
- [ ] `Bullet.update()` : séparer déplacement et dessin
- [ ] Sortir les sons de `backend/physique.py`

### Priorité basse — matière du cours
- [ ] `@property` pour la hitbox, calculée depuis `x` / `y`
- [ ] Décorateur de cache pour le chargement des images
- [ ] Décorateur `@chronometre` pour mesurer les fonctions lentes
- [ ] `@dataclass` pour la configuration

### Menu et états
- [ ] Classe `Game` avec états : menu, partie, game over
- [ ] Bouton « Jouer », rejouer après un game over
- [ ] Taille d'écran dynamique

### Bonus
- [ ] Barre de vie des ennemis
- [ ] Bonus ramassables en jeu
- [ ] Obstacles
- [ ] Niveaux de difficulté
- [ ] Sauvegarde des meilleurs scores

---

## Répartition

### Luka Parmentier
- Fenêtre et affichage du joueur, déplacements
- Réorganisation en classes et en modules, fichier d'initialisation
- Affichage et déplacement des ennemis, apparition en boucle
- Collisions balle / ennemi

### Roméo (rizuka04)
- Tir et projectiles, centrage des deux balles, hitboxes indépendantes
- Game over et barre de santé
- Score dynamique (temps et ennemis détruits)
- Images du vaisseau selon l'inclinaison et les dégâts
- Bruitages et musique de fond
- `test_fps.py` pour mesurer les performances
- Rangement des assets et `asset_paths.py`

---

## Utilisation de l'IA

Points sur lesquels l'IA a été sollicitée, à mentionner dans le compte rendu :

- Gestion de la taille d'une image avec Pygame
- Intégration de la vitesse du joueur selon le vaisseau choisi
- **Delta time** (`dt` / `REFERENCE_FRAME`) pour rendre les déplacements indépendants
  du nombre d'images par seconde
- Correction de bugs :
  - `enemyX = random.randrange(...)` sur deux lignes plutôt qu'en affectation multiple
  - récupération de la liste `bullets` de `Weapon` : utiliser l'instance, pas la classe
  - chute du framerate causée par le rechargement des images à chaque tour de boucle
- Résolution de conflits git et nettoyage des `__pycache__` suivis par erreur
- Découpage de `main()` : extraction des classes `Partie` et `Sons`
- Relecture d'architecture et identification des limites

---

## À retrouver pour le compte rendu

- [x] Phase prépa « structure et déroulement du jeu » → `doc/PP/structure_jeu.md`
- [x] Phases prépa collision et score → `doc/PP/`
- [ ] Justifier le choix de l'héritage multiple pour `Avion` et `Extra`
- [ ] Justifier le découpage backend / frontend / classes / config
