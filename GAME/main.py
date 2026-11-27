# =============================================================================
#  POINT D'ENTREE DU JEU
#  Cree la fenetre puis deroule la boucle de jeu : lire les touches,
#  mettre a jour, afficher. Toute la logique est dans Partie.
# =============================================================================

import pygame
from backend.jeu import Partie
from backend.audio import Sons
from config.config import L_SCREEN, H_SCREEN
from frontend.affichage import game_over_screen
from backend.controle import lire_clavier


def main():

    ## ----------- DEMARRAGE -----------
    pygame.init()
    screen = pygame.display.set_mode((L_SCREEN, H_SCREEN))
    pygame.display.set_caption("Space Invaders")

    sons = Sons()

    partie = Partie(sons)

    clock = pygame.time.Clock()  # gere les fps
    running = True  # variable on/off

    while running:

        dt = clock.tick(60)

        ## ----------- PYGAME -----------
        for event in pygame.event.get():  # gestion des evenements
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                partie.changer_arme()

        # Un appui = un seul changement d'arme (contrairement a get_pressed,
        # qui se repete tant que la touche reste enfoncee).
        ## ----------- GESTION DEPLACEMENT JOUEUR -----------
        keys = pygame.key.get_pressed()  # gestion des touches

        # Deplacement  + tir
        direction, tir = lire_clavier()

        # Deplacement, image selon les degats, puis tir
        partie.joueur.move(direction, dt)

        partie.joueur.changer_image(partie.barre_vie.vies, direction)

        if tir:
            partie.weapons.shoot_continuous(partie.joueur.x + 30, partie.joueur.y)

        ## ----------- MISE A JOUR ET AFFICHAGE -----------
        partie.update(dt)

        # On dessine AVANT de tester le game over, sinon l'ecran de fin
        # serait recouvert par l'image suivante.
        ## ----------- GAME OVER -----------
        partie.dessiner(screen)
        if partie.game_over(screen, sons):
            break
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    # ?? le menu devra lancer cette fonction avec un button "jouer"
    main()
