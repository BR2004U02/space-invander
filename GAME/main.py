import pygame
from jeu import Partie
from end.audio import Sons
from end.init import init_ennemy, L_screen, H_screen
from end.affichage import afficher_score, afficher_vie, game_over
from end.physique import collision_bullets_ennemies, collision_ennemi_bas


def main():

    ## ----------- DEMARRAGE -----------
    pygame.init()
    screen = pygame.display.set_mode((L_screen, H_screen))
    pygame.display.set_caption("Space Invaders")

    sons = Sons()
    partie = Partie(screen)

    clock = pygame.time.Clock()  # gere les fps
    running = True               # variable on/off

    while running:

        dt = clock.tick(60)

        ## ----------- PYGAME -----------
        partie.spawn_timer += dt # timer
        for event in pygame.event.get(): # gestion des evenements
            if event.type == pygame.QUIT:
                running = False

        ## ----------- SCORE -----------
        partie.score_timer += dt
        if partie.score_timer > 50:
            partie.score_timer = 0
            partie.score += 1

        ## ----------- AFFICHAGE -----------
        # background defilant entre 2 images continues
        partie.background_y1 += 2
        partie.background_y2 += 2

        if partie.background_y1 >= H_screen:
            partie.background_y1 = -H_screen

        if partie.background_y2 >= H_screen:
            partie.background_y2 = -H_screen

        screen.blit(partie.background, (0, partie.background_y1))
        screen.blit(partie.background, (0, partie.background_y2))
        ### JOUEUR ###
        partie.joueur.afficher(screen)  # player
        ### ENNEMI ###
        if partie.spawn_timer > 500:  # 500 ms = 0.5 sec
            partie.spawn_timer = 0
            partie.ennemis.extend(init_ennemy())
        for e in partie.ennemis:
            e.afficher(screen)
            e.move()

        ## ----------- AFFICHAGE SCORE-----------
        afficher_score(screen, partie.score, partie.font, partie.bonus_alpha)

        ## ----------- GESTION DEPLACEMENT JOUEUR -----------
        keys = pygame.key.get_pressed()  # gestion des touches
        # Deplacement continu
        direction = 0

        if keys[pygame.K_LEFT]:
            direction = -1
            partie.joueur.move(-1)

        elif keys[pygame.K_RIGHT]:
            direction = 1
            partie.joueur.move(1)

        partie.joueur.changer_image(partie.vies, direction)

        # Tirs continus
        if keys[pygame.K_SPACE]:
            partie.weapons.shoot_continuous(partie.joueur.x + 30, partie.joueur.y)

        ## -----------  COLLISION - ENNEMI TOUCHE -----------
        ennemis_detruits = collision_bullets_ennemies(
            partie.weapons.bullets, partie.ennemis, sons.explosion
        )
        partie.score += ennemis_detruits * 50
        if ennemis_detruits > 0:
            partie.bonus_timer = 1000

        if partie.bonus_timer > 0:
            partie.bonus_timer -= dt
            partie.bonus_alpha = int(255 * partie.bonus_timer / 1000)
        else:
            partie.bonus_alpha = 0

        ## ----------- COLLISION - REDUCTION DE VIE -----------
        partie.vies -= collision_ennemi_bas(partie.ennemis, H_screen, sons.hit)
        partie.joueur.changer_image(partie.vies, direction)

        afficher_vie(
            screen, partie.vies, partie.max_vies,
            partie.barre_largeur, partie.barre_hauteur,
            partie.barre_x, partie.barre_y
        )

        ## ----------- GAME OVER -----------
        if partie.vies <= 0:
            sons.stopper_musique()
            sons.game_over.play()
            screen.blit(partie.background, (0, 0))
            game_over(screen, partie.score)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
            break

        partie.weapons.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    # ?? le menu devra lancer cette fonction avec un button "jouer"
    main()
