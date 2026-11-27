# =============================================================================
#  SCORE
#  Score qui monte avec le temps, plus un bonus a chaque ennemi detruit,
#  affiche en vert et s'estompant progressivement.
# =============================================================================

import pygame

from config.config import (
    SCORE_UPDATE_DELAY,
    ENEMY_POINTS,
    SCORE_FONT_SIZE,
    SCORE_X,
    SCORE_Y,
    BONUS_DURATION,
    WHITE,
    GREEN
)
#TODO integrer a player + separer affichage ???

class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font(None, SCORE_FONT_SIZE)
        self.timer = 0
        self.bonus_timer = 0
        self.bonus_alpha = 0

    # --- Avance les deux minuteurs : score et bonus ---
    def update(self, dt):
        # Augmentation progressive du score
        self.timer += dt

        if self.timer > SCORE_UPDATE_DELAY:
            self.timer = 0
            self.value += 1

        # Gestion du bonus
        if self.bonus_timer > 0:
            self.bonus_timer -= dt
            self.bonus_alpha = int(
                255 * self.bonus_timer / BONUS_DURATION
            )
        else:
            self.bonus_alpha = 0

    # --- Ennemis detruits : ajoute les points et declenche le bonus ---
    def ajouter_points(self, nombre_ennemis):
        self.value += nombre_ennemis * ENEMY_POINTS

        if nombre_ennemis > 0:
            self.bonus_timer = BONUS_DURATION

    # --- Dessine le score, et le +50 tant qu'il n'a pas disparu ---
    def afficher(self, screen):
        score = self.font.render(
            "Score : " + str(self.value),
            True,
            WHITE
        )
        screen.blit(score, (SCORE_X, SCORE_Y))

        if self.bonus_alpha > 0:
            bonus = self.font.render("+50", True, GREEN)
            bonus.set_alpha(self.bonus_alpha)
            screen.blit(
                bonus,
                (SCORE_X + score.get_width() + 15, SCORE_Y)
            )
