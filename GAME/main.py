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

        ## ----------- GESTION DEPLACEMENT JOUEUR -----------
        keys = pygame.key.get_pressed()  # gestion des touches

        # Deplacement  + tir
        direction, tir = lire_clavier()
        direction, tir = lire_clavier()

        partie.joueur.move(direction, dt)

        partie.joueur.changer_image(partie.barre_vie.vies, direction)

        if tir:
            partie.weapons.shoot_continuous(partie.joueur.x + 30, partie.joueur.y)

        ## ----------- MISE A JOUR ET AFFICHAGE -----------
        partie.update(dt)

        ## ----------- GAME OVER -----------
        partie.dessiner(screen)
        if partie.game_over(screen, sons):
            break
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    # ?? le menu devra lancer cette fonction avec un button "jouer"
    main()
