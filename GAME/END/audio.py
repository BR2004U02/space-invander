import pygame
from asset_paths import MUSIC, SFX


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

    def _charger(self, nom_fichier, volume):
        son = pygame.mixer.Sound(SFX + "/" + nom_fichier)
        son.set_volume(volume)
        return son

    def stopper_musique(self):
        pygame.mixer.music.stop()
