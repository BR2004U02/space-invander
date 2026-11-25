ENNEMIS (flotte)

Variable :

- position (x, y) de chaque ennemi
- dh : direction horizontale (-1 gauche, 1 droite)
- dv : descente (1 descend, 0 arrêté)
- hitbox
- liste des ennemis à l'écran
- timer d'apparition (ms)

Constante :

- taille : 80 x 80 pixels
- apparition : 1 ennemi toutes les 500 ms, x au hasard, y = 50, direction au hasard
- limites : gauche 0, droite L_SCREEN - 80, bas H_SCREEN - 15
- vitesse de descente : 1

Types d'ennemis :

| Type | Vitesse | Particularité |
| --- | --- | --- |
| EnnemiClassique | 5 | aucune |
| EnnemiRapide | 9 | plus rapide |
| EnnemiTireur | 2 | tire vers le joueur toutes les 5000 ms |
| EnnemiBoss | — | classe vide, A FAIRE |

Apparition selon le score :

- moins de 2000 points : classique uniquement
- de 2000 à 5000 points : 70 % classique, 30 % rapide
- plus de 5000 points : 50 % classique, 30 % rapide, 20 % tireur

Application :

- classe Ennemi : move(dt)
    - x += vitesse x dh x (dt / REFERENCE_FRAME)
    - limite droite atteinte -> dh = -1, limite gauche atteinte -> dh = 1
    - y += vitesse de descente x dv x (dt / REFERENCE_FRAME)
    - la hitbox suit (x, y)
- classe Extra (hérite de Ennemi et de Entite) : ennemi affichable
- un type d'ennemi = une classe qui hérite de Extra et change la vitesse / le comportement
- backend/init.py, init_ennemy() : choisit le type selon le score et crée l'ennemi
- classe EnnemiManager : liste des ennemis, apparition, déplacement, tirs, affichage
- disparition :
    - touché par une balle du joueur -> supprimé, +50 points
    - arrivé en bas de l'écran -> supprimé, -1 vie
