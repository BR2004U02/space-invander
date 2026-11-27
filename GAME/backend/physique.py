# =============================================================================
#  PHYSIQUE - detection des collisions
#  Des fonctions simples, sans etat : elles comparent des hitbox et
#  retournent un nombre a l'appelant, qui decide quoi en faire.
# =============================================================================

# contrôle des collisions

import pygame
from pygame import mixer



# =============================================================================
#  PROJECTILE DU JOUEUR CONTRE ENNEMI
# =============================================================================

# Les deux disparaissent. Retourne le nombre d'ennemis detruits (pour le score).
def collision_bullets_ennemies(bullets, ennemis, explosionSound):

    ennemis_detruits = 0 # comptage score

    for bullet in bullets[:]:
        for ennemi in ennemis[:]:
            if bullet.hitbox.colliderect(ennemi.hitbox):

                explosionSound.play()
                bullets.remove(bullet)
                ennemis.remove(ennemi)

                ennemis_detruits += 1
                break

    return ennemis_detruits


# =============================================================================
#  ENNEMI ARRIVE EN BAS DE L'ECRAN
# =============================================================================

# L'ennemi disparait. Retourne le nombre de vies perdues.
def collision_ennemi_bas(ennemis, limite_bas, explosionSound):

    vies_perdues = 0

    for ennemi in ennemis[:]:
        if ennemi.hitbox.bottom >= limite_bas:
            explosionSound.play()
            ennemis.remove(ennemi)
            vies_perdues += 1

    return vies_perdues