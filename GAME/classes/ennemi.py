# =============================================================================
#  ENNEMIS - deplacement, affichage et types
#  Ennemi gere le deplacement, Extra y ajoute l'affichage, puis chaque type
#  d'ennemi herite de Extra en ne changeant que ce qui le distingue.
# =============================================================================

from classes.entite import Entite
from classes.arme import EnemyWeapon
from config.config import REFERENCE_FRAME


# =============================================================================
#  DEPLACEMENT DE BASE
# =============================================================================

class Ennemi:
    def __init__(self, x, y, speed, speed_down, limite_gauche, limite_droite, limite_bas, dh, dv):
        self.x = x
        self.y = y
        self.speed = speed
        self.speed_down = speed_down
        self.limite_gauche = limite_gauche
        self.limite_droite = limite_droite
        self.limite_bas = limite_bas
        self.dh = dh
        self.dv = dv

    # --- Va-et-vient horizontal + descente progressive ---
    def move(self, dt):

        #G / D
        self.x += self.speed * self.dh * (dt / REFERENCE_FRAME)

        if self.x >= self.limite_droite:
            self.dh = -1
        if self.x <= self.limite_gauche:
            self.dh = 1
        
        #B / H
        self.y += self.speed_down * self.dv * (dt / REFERENCE_FRAME)

        if self.y >= self.limite_bas:
            self.dv = 0
        
        #hit box
        self.hitbox.x = self.x
        self.hitbox.y = self.y  
        


# =============================================================================
#  ENNEMI AFFICHABLE
# =============================================================================

class Extra(Ennemi, Entite): # ennemi pour les déplacements, entite pour l'image/hitbox/affichage
    def __init__(self, x, y, limite_gauche, limite_droite, limite_bas, enemyImg, dh, dv):
        Ennemi.__init__(
            self, x, y, 5, 1,
            limite_gauche, limite_droite, limite_bas, dh, dv
        )
        Entite.__init__(self, x, y, enemyImg)

    def afficher(self, screen):
        super().afficher(screen)


# Les différents ennemis (héritage depuis Extra)


# =============================================================================
#  LES DIFFERENTS TYPES D'ENNEMIS
# =============================================================================

# Chaque type ne redefinit que sa vitesse ou son comportement propre.

# --- Ennemi de base : vitesse 5 ---
class EnnemiClassique(Extra):
    pass


# --- Plus rapide : vitesse 9 ---
class EnnemiRapide(Extra):
    def __init__(self, x, y, limite_gauche, limite_droite,
                 limite_bas, enemyImg, dh, dv):
        super().__init__(
            x, y, limite_gauche, limite_droite,
            limite_bas, enemyImg, dh, dv
        )
        self.speed = 9


# --- Lent, mais tire vers le joueur (composition : il possede une arme) ---
class EnnemiTireur(Extra):
    def __init__(self, x, y, limite_gauche, limite_droite,
                 limite_bas, enemyImg, dh, dv, bullet_image):
        super().__init__(
            x, y, limite_gauche, limite_droite,
            limite_bas, enemyImg, dh, dv
        )
        self.speed = 2
        self.weapon = EnemyWeapon(bullet_image)

    # --- Tire depuis le bas de l'ennemi, vers le joueur ---
    def update_tirs(self, dt, joueur):
        self.weapon.shoot(
            self.x + self.hitbox.width // 2,
            self.y + self.hitbox.height,
            joueur
        )
        self.weapon.update(dt)

    def afficher(self, screen):
        super().afficher(screen)
        self.weapon.afficher(screen)

# --- A IMPLEMENTER : boss resistant a plusieurs tirs ---
class EnnemiBoss(Extra):
    pass