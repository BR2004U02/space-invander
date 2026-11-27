# =============================================================================
#  JOUEUR - deplacement et apparence du vaisseau
#  Player gere le deplacement, Avion y ajoute l'image et son changement
#  selon les vies restantes et l'inclinaison.
# =============================================================================

import pygame
from classes.entite import Entite
from config.config import REFERENCE_FRAME


# =============================================================================
#  DEPLACEMENT DU VAISSEAU
# =============================================================================

class Player:
    def __init__(self, x, y, speed, direction, vy, limite_droite):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.vy = vy  # deplacement animation
        self.limite_droite = limite_droite

    # --- Deplacement horizontal, borne aux limites de l'ecran ---
    def move(self, direction, dt):
        self.x += self.speed * direction * (dt / REFERENCE_FRAME)
        self.x = max(0, min(self.x, self.limite_droite))
        self.hitbox.x = self.x
        

# =============================================================================
#  LES 9 IMAGES DU VAISSEAU
# =============================================================================

# 3 etats de degats (normal / damaged / critical) x 3 inclinaisons.
images_avion = {
        "normal": "player.png",
        "normal_left": "player_tilt_left.png",
        "normal_right": "player_tilt_right.png",

        "damaged": "player_damaged.png",
        "damaged_left": "player_damaged_tilt_left.png",
        "damaged_right": "player_damaged_tilt_right.png",

        "critical": "player_critical.png",
        "critical_left": "player_critical_tilt_left.png",
        "critical_right": "player_critical_tilt_right.png"
    }


# =============================================================================
#  LE VAISSEAU AFFICHABLE
# =============================================================================

class Avion(Player, Entite):
    def __init__(self, x, y, direction, vy, limite_droite, images):
        Player.__init__(self, x, y, 8, direction, vy, limite_droite)
        self.images = images
        Entite.__init__(self, x, y, images["normal"])

    # --- Choisit l'image selon les vies et la direction ---
    def changer_image(self, vies, direction):
        if vies >= 3:
            etat = "normal"
        elif vies == 2:
            etat = "damaged"
        else:
            etat = "critical"

        if direction == -1:
            self.image = self.images[etat + "_left"] # tilt left
        elif direction == 1:
            self.image = self.images[etat + "_right"] # tilt right
        else:
            self.image = self.images[etat] # aucun tilt, normal
   
