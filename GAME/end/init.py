
import pygame
from classes.player import Avion,images_avion
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
    background_y1 = 0
    background_y2 = -H_screen # background défilants
    background = pygame.transform.scale(background, (L_screen, H_screen))
    return background

# Initialisation du joueur
def init_player():

    images_chargees = {}
    for nom, fichier in images_avion.items():
        image = pygame.image.load("GAME/assets/" + fichier).convert_alpha()
        #TODO attribuer 150 à une variable
        images_chargees[nom] = pygame.transform.scale(image, (150, 150))
    #TODO ne pas faire des calcul dans l'attribution de joueur, utiliser des variable nommées
    # TODO pour une meilleur relecture et garder un format de code unifier !!!
    joueur = Avion(
        (L_screen - 150) // 2,
        H_screen - 150,
        0,
        None,
        L_screen - 150,
        images_chargees
    )

    return joueur

# Initialisation des ennemis
def init_ennemy():
    enemyImg = pygame.image.load("GAME/assets/enemy.png").convert_alpha()
    enemyImg = pygame.transform.scale(enemyImg, (80, 80))

    ennemis = []
    enemyX = random.randint(limite_gauche, limite_droite - 80)
    enemyY = 50
    # demarre vers la gauche ou la droite
    direction = random.choice([-1, 1])
    vitesse_descente = 0.5

    ennemi = Extra(
        enemyX, enemyY,
        limite_gauche, limite_droite, limite_bas,
        enemyImg, direction, vitesse_descente
    ) # 1 ???

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
