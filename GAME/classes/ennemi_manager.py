# =============================================================================
#  GESTIONNAIRE D'ENNEMIS
#  Gere la flotte : apparition reguliere, deplacement, tirs et affichage.
#  Le reste du jeu ne manipule que ce gestionnaire, jamais la liste.
# =============================================================================

from backend.init import init_ennemy
from config.config import ENEMY_SPAWN_DELAY


class EnnemiManager:
    def __init__(self, enemy_images, enemy_bullet_image):
        self.enemy_images = enemy_images
        self.enemy_bullet_image = enemy_bullet_image
        self.ennemis = []
        self.spawn_timer = 0

    # --- Fait apparaitre, deplacer et tirer tous les ennemis ---
    def update(self, dt, joueur, score):
        # Apparition des ennemis
        self.spawn_timer += dt

        if self.spawn_timer > ENEMY_SPAWN_DELAY:
            self.spawn_timer = 0
            self.ennemis.extend(
                init_ennemy(
                    self.enemy_images,
                    self.enemy_bullet_image,
                    score
                )
            )

        # Déplacement et tirs des ennemis
        for ennemi in self.ennemis:
            ennemi.move(dt)

            if hasattr(ennemi, "update_tirs"):
                ennemi.update_tirs(dt, joueur)

    # --- Dessine tous les ennemis de la liste ---
    def afficher(self, screen):
        for ennemi in self.ennemis:
            ennemi.afficher(screen)

    # --- Un projectile ennemi touche-t-il le joueur ? ---
    def verifier_collisions(self, joueur):
        for ennemi in self.ennemis:
            if hasattr(ennemi, "weapon"):
                for bullet in ennemi.weapon.bullets[:]:
                    if bullet.hitbox.colliderect(joueur.hitbox):
                        ennemi.weapon.bullets.remove(bullet)
                        return True

        return False