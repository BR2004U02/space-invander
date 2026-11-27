# =============================================================================
#  FOND DEFILANT
#  Deux copies de la meme image se suivent : quand l'une sort par le bas,
#  elle repart en haut. Le defilement parait ainsi continu.
# =============================================================================

from backend.init import init_game
from config.config import H_SCREEN, BACKGROUND_SPEED, REFERENCE_FRAME


class Fond:
    def __init__(self):
        self.image = init_game()
        self.y1 = 0
        self.y2 = -H_SCREEN

    # --- Descend les deux copies et les fait reboucler ---
    def update(self, dt):
        self.y1 += BACKGROUND_SPEED * (dt / REFERENCE_FRAME)
        self.y2 += BACKGROUND_SPEED * (dt / REFERENCE_FRAME)

        if self.y1 >= H_SCREEN:
            self.y1 = -H_SCREEN

        if self.y2 >= H_SCREEN:
            self.y2 = -H_SCREEN

    # --- Dessine les deux copies l'une au-dessus de l'autre ---
    def afficher(self, screen):
        screen.blit(self.image, (0, self.y1))
        screen.blit(self.image, (0, self.y2))