# contrôle des collisions

import pygame
from pygame import mixer


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

def collision_ennemi_bas(ennemis, limite_bas, explosionSound):

    vies_perdues = 0

    for ennemi in ennemis[:]:
        if ennemi.hitbox.bottom >= limite_bas:
            explosionSound.play()
            ennemis.remove(ennemi)
            vies_perdues += 1

    return vies_perdues