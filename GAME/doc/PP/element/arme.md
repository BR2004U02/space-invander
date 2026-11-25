ARME ET BALLES

Variable :

- position (x, y) de chaque balle
- etat de la balle : "ready" (à supprimer) ou "fire" (en vol)
- hitbox de chaque balle
- liste des balles en vol
- moment du dernier tir (ms)

Constante (joueur) :

- touche de tir : espace (tir continu tant qu'elle est enfoncée)
- délai entre deux tirs : 600 ms
- 2 balles par tir, une sur chaque aile (joueur.x + 25 et joueur.x + 85)
- vitesse : 10, vers le haut
- image : bullet.png

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
- classe EnemyBullet (hérite de Entite) : avance selon sa direction (x et y)
- classe EnemyWeapon : shoot(x, y, joueur), update(dt), afficher(screen)
    - supprime les balles sorties de l'écran
- collisions : voir collision.md
    - balle du joueur sur ennemi -> les deux disparaissent
    - balle ennemie sur joueur -> la balle disparaît, -1 vie
