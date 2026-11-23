from classes.arme import Weapon
from end.init import init_game, init_player, init_ennemy, init_vie, init_score, H_screen


class Partie:
    """Regroupe tout l'état d'une partie en cours : fond, joueur, score, armes, ennemis."""

    def __init__(self, screen):
        # Fond défilant (deux copies qui se suivent)
        self.background = init_game()
        self.background_y1 = 0
        self.background_y2 = -H_screen

        # Joueur
        self.joueur = init_player()

        # Vies et barre de vie
        (self.vies, self.max_vies,
         self.barre_largeur, self.barre_hauteur,
         self.barre_x, self.barre_y) = init_vie()

        # Score
        self.score, self.font = init_score()
        self.score_timer = 0
        self.bonus_timer = 0   # "+50" affiché pendant 1 seconde
        self.bonus_alpha = 0   # transparence du "+50"

        # Armes
        self.weapons = Weapon(screen)

        # Ennemis
        # TODO intergrer dans ennemi manager
        self.spawn_timer = 0
        self.ennemis = list(init_ennemy())
