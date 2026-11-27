# =============================================================================
#  SONS - musique de fond et bruitages
#  Tout est charge une fois au demarrage : aucun acces disque pendant le jeu.
# =============================================================================

import pygame
from config.asset_paths import MUSIC, SFX


class Sons:
    """Charge la musique de fond et les bruitages, et règle leurs volumes."""

    def __init__(self):
        pygame.mixer.init()

        # Musique de fond, en boucle
        pygame.mixer.music.load(MUSIC + "/pvz.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        # Bruitages
        self.explosion = self._charger("boom2.wav", 0.1)
        self.hit = self._charger("roblox.wav", 0.5)
        self.game_over = self._charger("gameover.wav", 0.5)

    # --- Charge un bruitage et regle son volume (evite de repeter 3 lignes) ---
    def _charger(self, nom_fichier, volume):
        son = pygame.mixer.Sound(SFX + "/" + nom_fichier)
        son.set_volume(volume)
        return son

    # --- Coupe la musique (utilise au game over) ---
    def stopper_musique(self):
        pygame.mixer.music.stop()
