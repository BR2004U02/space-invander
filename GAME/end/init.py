
import pygame
from classes.player import Avion,images_avion
from classes.ennemi import Extra, EnnemiClassique, EnnemiRapide, EnnemiTireur # EnnemiBoss
from asset_paths import BACKGROUND, PLAYER, ENEMY, PROJECTILE
from config import L_SCREEN, H_SCREEN, PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT
import random

# Chargement unique des images utilisées plusieurs fois => optimisation des performances
def charger_images():

    enemy_images = {
        "classique": pygame.image.load(ENEMY + "/enemy.png").convert_alpha(),
        "rapide": pygame.image.load(ENEMY + "/enemy_fast.png").convert_alpha(),
        "tireur": pygame.image.load(ENEMY + "/enemy_shooter.png").convert_alpha(),
        "boss": pygame.image.load(ENEMY + "/enemy_boss.png").convert_alpha()
    }

    for nom in enemy_images:
        enemy_images[nom] = pygame.transform.scale(
            enemy_images[nom],
            (ENEMY_WIDTH, ENEMY_HEIGHT)
        )

    # projectile joueur
    bullet_img = pygame.image.load(PROJECTILE + "/bullet.png").convert_alpha()

    # projectile ennemi
    enemy_bullet_img = pygame.image.load(
        PROJECTILE + "/enemy_bullet.png"
    ).convert_alpha()

    enemy_bullet_img = pygame.transform.scale(
        enemy_bullet_img, (20, 30)
    )

    return enemy_images, bullet_img, enemy_bullet_img

# Initialisation du jeu
def init_game():
    # La fenetre est creee par main() : ici on ne charge que le fond.
    background = pygame.image.load(BACKGROUND + "/background.png").convert()
    background = pygame.transform.scale(background, (L_SCREEN, H_SCREEN))
    return background

# Initialisation du joueur
def init_player():

    images_chargees = {}
    for nom, fichier in images_avion.items():
        image = pygame.image.load(PLAYER + "/" + fichier).convert_alpha()
        #TODO attribuer 150 à une variable
        images_chargees[nom] = pygame.transform.scale(image, (150, 150))
    #TODO ne pas faire des calcul dans l'attribution de joueur, utiliser des variable nommées
    # TODO pour une meilleur relecture et garder un format de code unifier !!!
    joueur = Avion(
        (L_SCREEN - PLAYER_WIDTH) // 2,
        H_SCREEN - PLAYER_HEIGHT,
        0,
        None,
        L_SCREEN - 150,
        images_chargees
    )

    return joueur

# Initialisation des différents ennemis
def init_ennemy(enemy_images, enemy_bullet_image, score):
    limite_gauche = 0
    limite_droite = L_SCREEN - ENEMY_WIDTH
    limite_bas = H_SCREEN - 15

    x = random.randint(limite_gauche, limite_droite - 80)
    y = 50
    direction = random.choice([-1, 1])
    vitesse_descente = 1

    if score < 2000: # 70% classique | 30% rapide
        type_ennemi = "classique"

    elif score < 5000: # 50% classique | 30% rapide | 20% tireur
        type_ennemi = random.choices(
            ["classique", "rapide"],
            weights=[70, 30]
        )[0]

    else:
        type_ennemi = random.choices(
            ["classique", "rapide", "tireur"],
            weights=[50, 30, 20]
        )[0]

    classes_ennemis = {
        "classique": EnnemiClassique,
        "rapide": EnnemiRapide,
        "tireur": EnnemiTireur
        # "boss": EnnemiBoss
    }

    if type_ennemi == "tireur":
        ennemi = EnnemiTireur(
            x, y,
            limite_gauche, limite_droite, limite_bas,
            enemy_images[type_ennemi],
            direction, vitesse_descente,
            enemy_bullet_image
        )
    else:
        ennemi = classes_ennemis[type_ennemi](
            x, y,
            limite_gauche, limite_droite, limite_bas,
            enemy_images[type_ennemi],
            direction, vitesse_descente
        )

    return [ennemi]