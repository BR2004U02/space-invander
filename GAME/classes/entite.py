# =============================================================================
#  ENTITE - classe mere de tout objet affiche a l'ecran
#  Regroupe ce que le joueur, les ennemis et les projectiles ont en commun :
#  une position, une image et une boite de collision (hitbox).
# =============================================================================

class Entite:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.hitbox = image.get_rect(topleft=(x, y))

    # --- Dessine l'image de l'objet a sa position ---
    def afficher(self, screen):
        screen.blit(self.image, (self.x, self.y))