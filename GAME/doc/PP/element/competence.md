competence, elle se recharge en 5s et permet de faire apparaitre un arme (defiler imager) qui tire en continu(toute les 0,5 sec) UNE petite balle , pour les balles on reprend la vitesse et l image retrecié des balles classique , genere moi ensuite la suite d image qui affiche un petit trape sur le dos de l avion qui s ouvre (chaque image durera donc le temp d une iteration de main) COMPETENCE : MITRAILLEUSE

Une trappe s'ouvre au centre de l'avion, une mitrailleuse se déplie,
puis tire en continu une petite balle. A la fin, elle se replie et la compétence se recharge.

Etats :

- "recharge" : 5 s, case grisée + temps restant + barre de progression
- "prete" : case en couleur, attend la touche (flèche du haut)
- "ouverture" : la trappe s'ouvre, la mitrailleuse se déplie (24 images)
- "tir" : 1 petite balle toutes les 0,2 s + animation de tir (6 images),
  le canon tourne entre deux tirs (6 images en boucle)
- "fermeture" : les images d'ouverture rejouées à l'envers (23 -> 00)

recharge -> prete -> ouverture -> tir -> fermeture -> recharge

Variable :

- etat de la compétence
- temps de recharge restant (ms)
- temps de tir restant (ms)
- timer du tir (ms depuis la dernière balle)
- index de l'image affichée (ouverture, tir, rotation ou fermeture)
- liste des balles de la compétence

Constante (config.py) :

- COMPETENCE_KEY = pygame.K_UP -> touche d'activation (config.py devra importer pygame)
- COMPETENCE_COOLDOWN = 5000 -> recharge en ms
- COMPETENCE_SHOOT_DELAY = 200 -> 1 balle toutes les 0,2 s (12 itérations : 6 images de tir + 6 de rotation)
- COMPETENCE_DURATION -> durée du tir en ms (A DEFINIR, voir plus bas)
- COMPETENCE_BULLET_SCALE = 0.5 -> image de bullet.png rétrécie (32 x 32 -> 16 x 16)
- vitesse des balles = BULLET_SPEED (la même que les balles classiques)
- COMPETENCE_MUZZLE_Y = 100 -> la bouche du canon est 100 px au-dessus du centre de l'avion
- NB_IMAGES_OUVERTURE = 24, NB_IMAGES_TIR = 6, NB_IMAGES_ROTATION = 6
- COMPETENCE_ICON_SIZE = 64 -> taille de la case
- position de la case : en haut à droite (L_SCREEN - 64 - 20, 20)

Constante (asset_paths.py) :

- COMPETENCE = ASSETS + "/images/competence"

Images (GAME/assets/images/competence/) :

| Fichier | Nombre | Taille | Contenu |
| --- | --- | --- | --- |
| ouverture_00.png à ouverture_23.png | 24 | 150 x 320 | trappe fermée -> ouverte (00 à 05), mitrailleuse qui se déplie (06 à 22), position finale (23) |
| tir_00.png à tir_05.png | 6 | 150 x 320 | éclair, flammes, fumée, recul du canon, douille éjectée, canon qui tourne |
| rotation_00.png à rotation_05.png | 6 | 150 x 320 | canon qui tourne sans tirer (boucle, rotation_00 = ouverture_23) |
| icone.png | 1 | 64 x 64 | case en couleur (compétence prête) |
| icone_grise.png | 1 | 64 x 64 | case grisée (recharge) |

- chaque image ne contient QUE la trappe et la mitrailleuse (fond transparent, pas d'avion)
- la trappe est au centre de l'image
- en jeu : centre de l'image = centre de l'image de l'avion, dessinée par-dessus l'avion
  -> image.get_rect(center=joueur.hitbox.center)
- 1 image = 1 itération du main -> ouverture = 24 itérations = 0,4 s à 60 FPS
- entre deux tirs : rotation_00 à rotation_05 en boucle (le canon continue de tourner)
- fermeture : aucune image en plus, on relit ouverture_23 -> ouverture_00
- départ d'une balle : x = centre de l'avion, y = centre de l'avion - COMPETENCE_MUZZLE_Y

Application :

- config.py + asset_paths.py : ajouter les constantes
- backend/init.py, charger_images() : charger les 38 images une seule fois
  + créer l'image rétrécie de la balle
- backend/controle.py, lire_clavier() : retourner une 3e valeur "competence"
  (touche COMPETENCE_KEY enfoncée)
- classes/competence.py : nouvelle classe Competence
    - update(dt, activer, joueur) -> gère les états, les timers et les balles
    - afficher(screen, joueur) -> calque de la mitrailleuse + balles
    - afficher_case(screen) -> case en haut à droite
- backend/jeu.py, Partie : créer la Competence, l'appeler dans appliquer_controles,
  update et dessiner (après l'avion, avant le score)
- backend/physique.py : les balles de la compétence détruisent les ennemis
  comme les balles classiques (même fonction de collision)

Déroulement (à chaque itération du main) :

1. etat "recharge"
    - temps de recharge -= dt
    - case : icone_grise.png + temps restant en secondes + barre de progression
    - si temps de recharge <= 0 : etat = "prete"
2. etat "prete"
    - case : icone.png, barre pleine
    - si touche enfoncée : etat = "ouverture", index = 0
3. etat "ouverture"
    - afficher ouverture_[index], puis index += 1
    - si index = 24 : etat = "tir", timer du tir = 0
4. etat "tir"
    - temps de tir -= dt, timer du tir += dt
    - si timer du tir >= 200 : créer 1 petite balle, timer = 0, index = 0
    - afficher tir_[index] pendant 6 itérations, puis rotation_[index % 6] en boucle
    - si temps de tir <= 0 : etat = "fermeture", index = 23
5. etat "fermeture"
    - afficher ouverture_[index], puis index -= 1
    - si index < 0 : etat = "recharge", temps de recharge = 5000

Case (en haut à droite) :

- barre de progression sous la case : largeur = largeur totale x (1 - temps restant / 5000)
- temps restant affiché au centre de la case, arrondi au dixième (ex : "3.2")


