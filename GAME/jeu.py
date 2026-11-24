from classes.arme import Weapon
from classes.fond import Fond
from classes.score import Score
from classes.barre_de_vie import BarreDeVie
from classes.ennemi_manager import EnnemiManager
from end.init import init_player, init_ennemy, charger_images
from end.physique import collision_bullets_ennemies, collision_ennemi_bas
from config import H_SCREEN


class Partie:
    """Regroupe tout l'état d'une partie en cours : fond, joueur, score, armes, ennemis."""

    def __init__(self, sons):

        self.enemy_images, self.bullet_images, self.enemy_bullet_images = charger_images() # charger les images une seule fois

        # Fond défilant (deux copies qui se suivent)
        self.fond = Fond()

        # Sons
        self.sons = sons

        # Joueur
        self.joueur = init_player()

        # Invulnérabilité lors de dégâts
        self.temps_invulnerable = 0
        self.delai_invulnerabilite = 1000  # 1 seconde

        # Barre de vie
        self.barre_vie = BarreDeVie()

        # Score
        self.score = Score()

        # Armes
        self.weapons = Weapon(self.bullet_images)

        # Ennemis
        self.ennemi_manager = EnnemiManager(
        self.enemy_images,
        self.enemy_bullet_images
)
        self.ennemi_manager.ennemis.extend(
            init_ennemy(self.enemy_images, self.enemy_bullet_images, self.score.value)
        )

    def update(self, dt):
        # Mise à jour du décor
        self.fond.update(dt)

        # Mise à jour du score
        self.score.update(dt)

        # Mise à jour des ennemis
        self.ennemi_manager.update(dt, self.joueur, self.score.value)

        # Mise à jour des projectiles
        self.weapons.update(dt)

        # Invulnérabilité
        self.temps_invulnerable = max(
            0,
            self.temps_invulnerable - dt
        )

        # Gestion des collisions
        self.gerer_collisions()


    def dessiner(self, screen):
        # Décor
        self.fond.afficher(screen)

        # Joueur | invulnéraibilité (clignotement)
        if self.temps_invulnerable > 0:
            temps_ecoule = self.delai_invulnerabilite - self.temps_invulnerable

            if int(temps_ecoule / 100) % 2 == 0:
                image = self.joueur.image.copy()
                image.set_alpha(80)
                screen.blit(image, (self.joueur.x, self.joueur.y))
            else:
                self.joueur.afficher(screen)
        else:
            self.joueur.afficher(screen)

        # Ennemis
        self.ennemi_manager.afficher(screen)

        # Score
        self.score.afficher(screen)

        # Barre de vie
        self.barre_vie.afficher(screen)

        # Projectiles
        self.weapons.afficher(screen)

    def gerer_collisions(self):
        # Collision entre les projectiles et les ennemis
        ennemis_detruits = collision_bullets_ennemies(
            self.weapons.bullets,
            self.ennemi_manager.ennemis,
            self.sons.explosion
        )

        self.score.ajouter_points(ennemis_detruits)

        # Collision entre les ennemis et le bas de l'écran
        perte_vies = collision_ennemi_bas(
            self.ennemi_manager.ennemis,
            H_SCREEN,
            self.sons.hit
        )

        if perte_vies > 0 and self.temps_invulnerable <= 0:
            self.barre_vie.perdre_vies(perte_vies)
            self.temps_invulnerable = self.delai_invulnerabilite

        # Collision entre les projectiles ennemis et le joueur
        if self.ennemi_manager.verifier_collisions(self.joueur):
            if self.temps_invulnerable <= 0:
                self.barre_vie.perdre_vies(1)
                self.sons.hit.play()
                self.temps_invulnerable = self.delai_invulnerabilite
