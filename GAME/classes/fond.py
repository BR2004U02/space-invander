from end.init import init_game
from config import H_SCREEN, BACKGROUND_SPEED, REFERENCE_FRAME


class Fond:
    def __init__(self):
        self.image = init_game()
        self.y1 = 0
        self.y2 = -H_SCREEN

    def update(self, dt):
        self.y1 += BACKGROUND_SPEED * (dt / REFERENCE_FRAME)
        self.y2 += BACKGROUND_SPEED * (dt / REFERENCE_FRAME)

        if self.y1 >= H_SCREEN:
            self.y1 = -H_SCREEN

        if self.y2 >= H_SCREEN:
            self.y2 = -H_SCREEN

    def afficher(self, screen):
        screen.blit(self.image, (0, self.y1))
        screen.blit(self.image, (0, self.y2))