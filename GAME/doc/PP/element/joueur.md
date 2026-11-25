JOUEUR (avion)

Variable :

- position x (y ne change pas)
- direction (-1 gauche, 0 immobile, 1 droite)
- image affichée (selon les vies et la direction)
- hitbox
- temps d'invulnérabilité restant (ms)

Constante :

- taille : 150 x 150 pixels
- vitesse : 8
- position de départ : centré en bas de l'écran (x = 565, y = 650)
- limites : x entre 0 et L_SCREEN - 150
- touches : flèche gauche / flèche droite
- 9 images : 3 états (normal, damaged, critical) x 3 inclinaisons (droit, gauche, droite)
- invulnérabilité après un dégât : 1000 ms

Application :

- classe Player : move(direction, dt)
    - x += vitesse x direction x (dt / REFERENCE_FRAME)
    - x bloqué entre 0 et la limite droite
    - la hitbox suit x
- classe Avion (hérite de Player et de Entite) : changer_image(vies, direction)
    - 3 vies ou plus -> normal, 2 vies -> damaged, sinon -> critical
    - direction -1 -> image penchée à gauche, 1 -> penchée à droite
- backend/init.py, init_player() : charge les 9 images une seule fois, crée l'avion
- backend/controle.py, lire_clavier() : retourne direction et tir
- invulnérabilité (dans Partie) : pendant 1 s après un dégât, l'avion clignote
  (transparent une fois sur deux, toutes les 100 ms) et ne perd pas de vie
