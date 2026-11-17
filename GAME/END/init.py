
import pygame
from classes.player import Avion
from classes.ennemi import Extra
import random

# Dimensions de la fenêtre
L_screen, H_screen = 1280, 800

# Limites de déplacement
limite_gauche = 0
limite_droite = L_screen - 30
limite_bas = H_screen - 15

# Initialisation du jeu
def init_game():
    screen = pygame.display.set_mode((L_screen, H_screen))
    pygame.display.set_caption("Space Invaders")
    background = pygame.image.load("GAME/assets/background.png").convert()
    background = pygame.transform.scale(background, (L_screen, H_screen))
    return background

# Initialisation du joueur
def init_player():
    images = {
        "normal": "player.png",
        "normal_left": "player_tilt_left.png",
        "normal_right": "player_tilt_right.png",

        "damaged": "player_damaged.png",
        "damaged_left": "player_damaged_tilt_left.png",
        "damaged_right": "player_damaged_tilt_right.png",

        "critical": "player_critical.png",
        "critical_left": "player_critical_tilt_left.png",
        "critical_right": "player_critical_tilt_right.png"
    }

    for nom in images:
        image = pygame.image.load("GAME/assets/" + images[nom]).convert_alpha()
        images[nom] = pygame.transform.scale(image, (150, 150))

    joueur = Avion(
        (L_screen - 150) // 2,
        H_screen - 150,
        0,
        0,
        L_screen - 150,
        images
    )

    return joueur

# Initialisation des ennemis
def init_ennemy():
    enemyImg = pygame.image.load("GAME/assets/enemy.png").convert_alpha()
    enemyImg = pygame.transform.scale(enemyImg, (80, 80))

    ennemis = []
    enemyX = random.randint(limite_gauche, limite_droite - 80)
    enemyY = 50
    direction = random.choice([-1, 1])

    ennemi = Extra(
        enemyX, enemyY,
        limite_gauche, limite_droite, limite_bas,
        enemyImg, direction, 1
    )

    ennemis.append(ennemi)
    return ennemis

# Initialisation des vies
def init_vie():
    vies = 3
    max_vies = 3
    largeur = 150
    hauteur = 20
    position_x = 20
    position_y = 20
    return vies, max_vies, largeur, hauteur, position_x, position_y

# Initialisation du score
def init_score():
    score = 0
    font = pygame.font.Font(None, 36)
    return score, font
