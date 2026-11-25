import pygame
from classes.arme import Weapon
from classes.arme import Weapon, WeaponShuriken
from classes.fond import Fond
from classes.score import Score
from classes.barre_de_vie import BarreDeVie
from classes.ennemi_manager import EnnemiManager
from backend.init import init_player, init_ennemy, charger_images
from backend.physique import collision_bullets_ennemies, collision_ennemi_bas
from config.config import H_SCREEN, HINT_TEXT, HINT_FONT_SIZE, HINT_X, HINT_Y, WHITE
from frontend.affichage import game_over_screen

class Partie:
    """Regroupe tout l'état d'une partie en cours : fond, joueur, score, armes, ennemis."""

    def __init__(self, sons):

        self.enemy_images, self.bullet_images, self.enemy_bullet_images, self.shuriken_image = charger_images() # charger les images une seule fois

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
        self.armes = [Weapon(self.bullet_images), WeaponShuriken(self.shuriken_image)]
        self.index_arme = 0
        self.weapons = self.armes[0]          # l'arme en main

        # Indication du changement d'arme (texte préparé une seule fois)
        self.indication = pygame.font.Font(None, HINT_FONT_SIZE).render(HINT_TEXT, True, WHITE)
        # Ennemis
        self.ennemi_manager = EnnemiManager(
        self.enemy_images,
        self.enemy_bullet_images
)
        self.ennemi_manager.ennemis.extend(
            init_ennemy(self.enemy_images, self.enemy_bullet_images, self.score.value)
        )
        
        
    def changer_arme(self):
        self.index_arme = (self.index_arme + 1) % len(self.armes)
        self.weapons = self.armes[self.index_arme]  
        self.game_over_screen = game_over_screen
        
        
    def update(self, dt):
        # Mise à jour du décor
        self.fond.update(dt)

        # Mise à jour du score
        self.score.update(dt)

        # Mise à jour des ennemis
        self.ennemi_manager.update(dt, self.joueur, self.score.value)

        # Mise à jour des projectiles
        for arme in self.armes:
            arme.update(dt)

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

        # Indication du changement d'arme
        screen.blit(self.indication, (HINT_X, HINT_Y))

        # Projectiles
        for arme in self.armes:
            arme.afficher(screen)

    def gerer_collisions(self):
        # Collision entre les projectiles et les ennemis
        ennemis_detruits = 0
        for arme in self.armes:
            ennemis_detruits += collision_bullets_ennemies(
            arme.bullets,
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
                
    def game_over(self,screen,sons):
        if self.barre_vie.vies <= 0:
            sons.stopper_musique()
            sons.game_over.play()

            self.fond.afficher(screen)
            game_over_screen(screen, self.score.value)

            pygame.display.flip()
            pygame.time.wait(3000)

            running = False
            return True