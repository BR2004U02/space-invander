COLLISION

Variable:
 
 - position balle (x,y)
 - position ennemi (x,y)

Constante:
- dimension en pixel d'ennemi
- dimension en pixel de bullet

 Application :

 - ajouter fonction "return position" aux deux classe
 - crée une "hit box" à partir des positions
 - ajouter fonction dans le main " verifier colision"
 - question d'optimisation ( est ce mieux de faire ...)
    - ennemi manager


"DEPOP" ENNEMI



 Application : 

- resultat de la fonction main " verifier collision"
- remplacer l'element ennemi toucher de la liste "Ennemies" par None

COLLISION ENNEMI - BAS DE L'ÉCRAN 

- si hauteur_ennemi <= 0 (bas de l'écran):
    disparître ennmie et -1 vie au joueur
- si 3 collision:
    Game Over