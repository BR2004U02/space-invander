FOND DEFILANT

Variable :

- y1 : position verticale de la 1re copie de l'image
- y2 : position verticale de la 2e copie

Constante :

- image : background.png, redimensionnée à la taille de l'écran (1280 x 800)
- vitesse de défilement : 2
- départ : y1 = 0, y2 = -H_SCREEN (la 2e copie est juste au-dessus de la 1re)

Application :

- classe Fond dans classes/fond.py : update(dt), afficher(screen)
- update :
    - y1 et y2 += vitesse x (dt / REFERENCE_FRAME)
    - si une copie sort par le bas (y >= H_SCREEN) : elle repart en haut (y = -H_SCREEN)
- afficher : dessine les 2 copies -> le fond défile sans coupure
- le fond est dessiné en premier, avant tous les autres objets
