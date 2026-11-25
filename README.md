# Space Invaders

Clone de Space Invaders développé en Python avec Pygame, dans le cadre du cours de
programmation (UE43, HELMo — A2).

Le projet part de l'implémentation de référence
[attreyabhatt/Space-Invaders-Pygame](https://github.com/attreyabhatt/Space-Invaders-Pygame)
et la réorganise entièrement selon une architecture orientée objet.

**Dépôt :** https://github.com/Brukzer/Space-invander

---

## Installation

Python 3.10 ou supérieur est requis.

```bash
git clone https://github.com/Brukzer/Space-invander.git
cd Space-invander
```

Création d'un environnement virtuel (recommandé) :

```bash
python -m venv .venv
```

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

Installation des dépendances :

```bash
pip install -r requirements.txt
```

---

## Lancement

Depuis la **racine du dépôt** :

```bash
python GAME/main.py
```

> Le jeu doit être lancé depuis la racine : les chemins des ressources
> (`GAME/assets/...`) sont relatifs à ce dossier.

---

## Contrôles

| Touche | Action |
| --- | --- |
| ← | Déplacement vers la gauche |
| → | Déplacement vers la droite |
| Espace | Tir (automatique tant que la touche est maintenue) |

Pour quitter, fermer la fenêtre.

---

## Règles du jeu

- Le joueur dispose de **3 vies**, affichées par la barre de vie en haut à gauche.
- Le score augmente **avec le temps**, et de **50 points** par ennemi détruit.
- Une vie est perdue lorsqu'un ennemi atteint le bas de l'écran ou qu'un projectile
  ennemi touche le vaisseau. Le joueur est ensuite invulnérable pendant 1 seconde
  (le vaisseau clignote).
- Le vaisseau change d'apparence selon les vies restantes : normal, endommagé, critique.
- La partie se termine lorsque les vies tombent à zéro.

### Types d'ennemis

Les ennemis apparaissent toutes les 500 ms. Leur variété dépend du score atteint :

| Ennemi | Vitesse | Comportement | Apparaît à partir de |
| --- | --- | --- | --- |
| Classique | 5 | Déplacement horizontal, descente progressive | 0 point |
| Rapide | 9 | Même trajectoire, plus rapide | 2 000 points |
| Tireur | 2 | Lent, tire vers la position du joueur toutes les 5 s | 5 000 points |

---

## Structure du projet

```text
Space-invander/
├── GAME/
│   ├── main.py              Point d'entrée : fenêtre et boucle de jeu
│   │
│   ├── backend/             Logique du jeu
│   │   ├── jeu.py           Classe Partie : état et règles d'une partie
│   │   ├── init.py          Chargement des ressources, création des objets
│   │   ├── physique.py      Détection des collisions
│   │   ├── controle.py      Lecture du clavier
│   │   ├── audio.py         Classe Sons : musique et bruitages
│   │   └── test_fps.py      Outil de mesure des performances
│   │
│   ├── classes/             Objets du jeu
│   │   ├── entite.py        Entite : position, image, hitbox, affichage
│   │   ├── player.py        Player, Avion
│   │   ├── ennemi.py        Ennemi, Extra et les types d'ennemis
│   │   ├── ennemi_manager.py  Apparition et mise à jour de la flotte
│   │   ├── arme.py          Bullet, EnemyBullet, Weapon, EnemyWeapon
│   │   ├── fond.py          Fond défilant
│   │   ├── score.py         Score et bonus
│   │   └── barre_de_vie.py  Vies et barre de vie
│   │
│   ├── frontend/            Affichage
│   │   └── affichage.py     Écran de fin de partie
│   │
│   ├── config/              Constantes et chemins
│   │   ├── config.py        Dimensions, vitesses, délais, couleurs
│   │   └── asset_paths.py   Chemins des ressources
│   │
│   ├── assets/              Images et sons
│   └── doc/                 Documentation et phases préparatoires
│
├── requirements.txt
└── README.md
```

---

## Architecture

Le code suit trois principes :

**Chaque objet du jeu est une classe** qui porte ses propres données. `Entite` fournit la
base commune — position, image, hitbox, affichage — dont héritent le vaisseau, les ennemis
et les projectiles.

**L'état d'une partie est centralisé** dans la classe `Partie`, qui compose les autres
objets (joueur, score, barre de vie, armes, gestionnaire d'ennemis) et expose trois
méthodes à la boucle : `appliquer_controles()`, `update()` et `dessiner()`.

**Les responsabilités sont réparties par dossier** : `backend/` pour la logique,
`frontend/` pour l'affichage, `classes/` pour les objets, `config/` pour les constantes.

Le détail des choix de conception figure dans le rapport, et la documentation
préparatoire dans `GAME/doc/`.

---

## Améliorations prévues

Voir `GAME/doc/ROADMAP.md`.

---

## Auteurs

Projet réalisé en binôme :

- **Luka Parmentier** — [@Brukzer](https://github.com/Brukzer)
- **Roméo** — [@rizuka04](https://github.com/rizuka04)

---

## Licence

MIT.
