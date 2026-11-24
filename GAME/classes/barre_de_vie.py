import pygame

from config import (
    PLAYER_MAX_LIVES,
    LIFE_BAR_WIDTH,
    LIFE_BAR_HEIGHT,
    LIFE_BAR_X,
    LIFE_BAR_Y,
    RED,
    GREEN,
    WHITE
)


class BarreDeVie:
    def __init__(self):
        self.vies = PLAYER_MAX_LIVES
        self.max_vies = PLAYER_MAX_LIVES

        self.largeur = LIFE_BAR_WIDTH
        self.hauteur = LIFE_BAR_HEIGHT

        self.x = LIFE_BAR_X
        self.y = LIFE_BAR_Y

    def perdre_vies(self, nombre):
        self.vies -= nombre

    def afficher(self, screen):
        pygame.draw.rect( # rectangle 
            screen, RED,
            (self.x, self.y, self.largeur, self.hauteur)
        )

        largeur_vie = self.largeur * max(0, self.vies) / self.max_vies

        pygame.draw.rect(
            screen, GREEN,
            (self.x, self.y, largeur_vie, self.hauteur)
        )

        pygame.draw.rect(
            screen, WHITE,
            (self.x, self.y, self.largeur, self.hauteur), 2
        )