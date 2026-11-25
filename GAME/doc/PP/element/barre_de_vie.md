BARRE DE VIE

Variable :

- vies restantes

Constante :

- vies au départ : 3 (= maximum)
- taille de la barre : 150 x 20 pixels
- position : en haut à gauche (20, 20)
- couleurs : fond rouge, vie verte, contour blanc (2 pixels)

Application :

- classe BarreDeVie dans classes/barre_de_vie.py : perdre_vies(nombre), afficher(screen)
- afficher :
    - rectangle rouge de la taille complète
    - rectangle vert par-dessus : largeur = largeur totale x vies / vies maximum
    - contour blanc
- perte d'une vie :
    - un ennemi arrive en bas de l'écran
    - une balle ennemie touche le joueur
    - sauf pendant l'invulnérabilité (1 s après un dégât)
- vies <= 0 -> Game Over
- les vies décident aussi de l'image de l'avion (voir joueur.md)
