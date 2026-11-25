ARME ET BALLES

Variable :

- position (x, y) de chaque balle
- etat de la balle : "ready" (à supprimer) ou "fire" (en vol)
- hitbox de chaque balle
- liste des balles en vol (une liste par arme)
- moment du dernier tir (ms)
- arme en main (index dans la liste des armes)
- shuriken : position de départ (x, y) et sens de la courbe (-1 gauche, 1 droite)

Constante (arme 1 : balles) :

- touche de tir : espace (tir continu tant qu'elle est enfoncée)
- délai entre deux tirs : 600 ms
- 2 balles par tir, une sur chaque aile (joueur.x + 25 et joueur.x + 85)
- vitesse : 10, vers le haut
- image : bullet.png

Constante (arme 2 : shurikens) :

- même touche de tir, même délai (600 ms), même vitesse de montée (10)
- 2 shurikens par tir, qui partent du centre de l'avion
- trajectoire en courbe : un shuriken part vers la gauche, l'autre vers la droite, puis ils se croisent
- SHURIKEN_AMPLITUDE = 120 -> largeur de la courbe en pixels
- SHURIKEN_LONGUEUR = 80 -> plus c'est grand, plus la courbe est étirée
- image : shuriken.png, 32 x 32 pixels

Constante (changement d'arme) :

- touche : flèche du haut, 1 appui = arme suivante (balles -> shurikens -> balles)

Constante (ennemi tireur) :

- délai entre deux tirs : 5000 ms
- 1 balle par tir, vitesse 4
- direction : vers le centre du joueur au moment du tir (ne le suit pas ensuite)
- image : enemy_bullet.png, 20 x 30 pixels
- hitbox réduite de 17 pixels (plus facile à esquiver)

Application :

- classe Bullet (hérite de Entite) : fire(x, y), update(dt)
    - y -= vitesse x (dt / REFERENCE_FRAME)
    - si y < 0 (sortie par le haut) : etat = "ready"
- classe Weapon : shoot_continuous(x, y), update(dt), afficher(screen)
    - tire seulement si le délai est écoulé depuis le dernier tir
    - supprime de la liste les balles à l'état "ready"
- classe Shuriken (hérite de Bullet) : update(dt)
    - la montée est celle de Bullet (réutilisée, pas réécrite)
    - x = x de départ + sens x SHURIKEN_AMPLITUDE x sin(distance parcourue / SHURIKEN_LONGUEUR)
    - la hitbox suit x
- classe WeaponShuriken (hérite de Weapon) : redéfinit seulement la création des projectiles
  -> le minuteur, la suppression hors écran, l'affichage et les collisions sont hérités
- changement d'arme (dans Partie) :
    - armes = [Weapon, WeaponShuriken], weapons = l'arme en main
    - changer_arme() : passe à l'arme suivante de la liste
    - toutes les armes sont mises à jour, affichées et testées en collision
      (les projectiles déjà tirés continuent après un changement), une seule tire
    - main.py : événement KEYDOWN sur la flèche du haut (1 seul déclenchement par appui,
      contrairement à get_pressed qui se répète tant que la touche est enfoncée)
- ajouter une arme = une classe qui hérite de Weapon + une ligne dans la liste
- classe EnemyBullet (hérite de Entite) : avance selon sa direction (x et y)
- classe EnemyWeapon : shoot(x, y, joueur), update(dt), afficher(screen)
    - supprime les balles sorties de l'écran
- collisions : voir collision.md
    - balle ou shuriken du joueur sur ennemi -> les deux disparaissent
    - balle ennemie sur joueur -> la balle disparaît, -1 vie
