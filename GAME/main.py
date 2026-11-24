import pygame
from jeu import Partie
from end.audio import Sons
from config import L_SCREEN, H_SCREEN
from end.affichage import game_over


def main():

    ## ----------- DEMARRAGE -----------
    pygame.init()
    screen = pygame.display.set_mode((L_SCREEN, H_SCREEN))
    pygame.display.set_caption("Space Invaders")

    sons = Sons()

    partie = Partie(sons)

    clock = pygame.time.Clock()  # gere les fps
    running = True               # variable on/off

    while running:

        dt = clock.tick(60)

        ## ----------- PYGAME -----------
        for event in pygame.event.get(): # gestion des evenements
            if event.type == pygame.QUIT:
                running = False

        ## ----------- GESTION DEPLACEMENT JOUEUR -----------
        keys = pygame.key.get_pressed()  # gestion des touches

        # Deplacement continu

        direction = 0

        if keys[pygame.K_LEFT]:
            direction = -1
            partie.joueur.move(-1, dt)

        elif keys[pygame.K_RIGHT]:
            direction = 1
            partie.joueur.move(1, dt)

        partie.joueur.changer_image(partie.barre_vie.vies, direction)

        # Tirs continus
        if keys[pygame.K_SPACE]:
            partie.weapons.shoot_continuous(
                partie.joueur.x + 30,
                partie.joueur.y
            )

        ## ----------- MISE A JOUR ET AFFICHAGE -----------
        partie.update(dt)

        ## ----------- GAME OVER -----------
        if partie.barre_vie.vies <= 0:
            sons.stopper_musique()
            sons.game_over.play()

            partie.fond.afficher(screen)
            game_over(screen, partie.score.value)

            pygame.display.flip()
            pygame.time.wait(3000)

            running = False
            break

        partie.dessiner(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    # ?? le menu devra lancer cette fonction avec un button "jouer"
    main()
