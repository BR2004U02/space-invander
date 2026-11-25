import pygame


def lire_clavier():
    """Traduit l'état du clavier en intentions de jeu."""
    keys = pygame.key.get_pressed()

    direction = 0
    if keys[pygame.K_LEFT]:
        direction = -1
    elif keys[pygame.K_RIGHT]:
        direction = 1

    tir = keys[pygame.K_SPACE]

    return direction, tir