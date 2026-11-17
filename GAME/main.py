import pygame
from classes.arme import Weapon
from END.init import init_game, init_player, init_ennemy, init_vie, init_score, L_screen, H_screen
from END.affichage import afficher_score, afficher_vie, game_over
from END.physique import collision_bullets_ennemies, collision_ennemi_bas
from pygame import mixer

clock = pygame.time.Clock()  # gère les fps
running = True  # variable on/off

#TODO ranger les variables


def main(clock, running):
    # création envirronement
    pygame.init()
    print("Audio :", pygame.mixer.get_init())

    screen = pygame.display.set_mode((L_screen, H_screen))

    # Initialisation du son
    pygame.mixer.init()

    # Musique de fond
    pygame.mixer.music.load("GAME/assets/pvz.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    # bruitages
    explosionSound = pygame.mixer.Sound("GAME/assets/boom2.wav")
    explosionSound.set_volume(0.1)

    hitSound = pygame.mixer.Sound("GAME/assets/roblox.wav")
    hitSound.set_volume(0.5)

    soundGameOver = pygame.mixer.Sound("GAME/assets/gameover.wav")
    soundGameOver.set_volume(0.5)

    background = init_game()  
    background_y1 = 0
    background_y2 = -H_screen # pour le déroulement

    joueur = init_player()
    vies, max_vies, largeur, hauteur, x, y = init_vie()
    score, font = init_score()
    score_timer = 0
    bonus_timer = 0 # ennemi touché +50 points affiché pendant 1 seconde
    bonus_alpha = 0 # transparence

    # création des armes
    weapons = Weapon(screen)
    spawn_timer = 0
    # TODO intergrer dans ennemi manager
    ennemis = []
    ennemis.extend(init_ennemy())

    while running:

        dt = clock.tick(60)
        print(clock.get_fps()) # checker performances
        print(pygame.display.get_driver())
        
        ## ----------- PYGAME -----------
        spawn_timer += dt # timer
        for event in pygame.event.get(): # gestion des événements
            if event.type == pygame.QUIT:
                running = False

        ## ----------- SCORE -----------
        score_timer += dt
        if score_timer > 50: 
            score_timer = 0
            score += 1

        ## ----------- AFFICHAGE -----------
        # background défilant entre 2 images continues
        background_y1 += 2
        background_y2 += 2

        if background_y1 >= H_screen:
            background_y1 = -H_screen

        if background_y2 >= H_screen:
            background_y2 = -H_screen

        screen.blit(background, (0, background_y1))
        screen.blit(background, (0, background_y2))
        ### JOUEUR ###
        joueur.afficher(screen)  # player
        ### ENNEMI ###
        if spawn_timer > 500:  # 500 ms = 0.5 sec
            spawn_timer = 0
            ennemis.extend(init_ennemy())
        for e in ennemis: 
            e.afficher(screen)
            e.move()

        ## ----------- AFFICHAGE SCORE-----------
        afficher_score(screen, score, font, bonus_alpha)

        ## ----------- GESTION DEPLACEMENT JOUEUR -----------
        keys = pygame.key.get_pressed()  # gestion des touches
        # Deplacement continu
        direction = 0

        if keys[pygame.K_LEFT]:
            direction = -1
            joueur.move(-1)

        elif keys[pygame.K_RIGHT]:
            direction = 1
            joueur.move(1)

        joueur.changer_image(vies, direction)

        # Tirs continus
        if keys[pygame.K_SPACE]:
            weapons.shoot_continuous(joueur.x + 30, joueur.y)

        ## -----------  COLLISION - ENNEMI TOUCHÉ -----------
        ennemis_detruits = collision_bullets_ennemies(weapons.bullets, ennemis, explosionSound)
        score += ennemis_detruits * 50
        if ennemis_detruits > 0:
            bonus_timer = 1000

        if bonus_timer > 0:
            bonus_timer -= dt
            bonus_alpha = int(255 * bonus_timer / 1000)
        else:
            bonus_alpha = 0

        ## ----------- COLLISION - REDUCTION DE VIE -----------
        vies -= collision_ennemi_bas(ennemis, H_screen, hitSound)
        joueur.changer_image(vies, direction)

        afficher_vie(screen, vies, max_vies, largeur, hauteur, x, y)

        if vies <= 0:
            pygame.mixer.music.stop() # stop musique de fond
            soundGameOver.play() # bruitage game over
            screen.blit(background, (0, 0))
            game_over(screen, score)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
            break

        weapons.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    # ?? le menu devra lancer cette fonction avec un button "jouer"
    main(clock, running)