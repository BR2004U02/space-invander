class Entite:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.hitbox = image.get_rect(topleft=(x, y))

    def afficher(self, screen):
        screen.blit(self.image, (self.x, self.y))