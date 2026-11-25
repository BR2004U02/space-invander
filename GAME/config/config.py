# Constantes utilisées dans le code du jeu

# Dimensions de la fenêtre
L_SCREEN = 1280
H_SCREEN = 800

# Joueur
PLAYER_WIDTH = 150
PLAYER_HEIGHT = 150
PLAYER_SPEED = 8

# Ennemis
ENEMY_WIDTH = 80
ENEMY_HEIGHT = 80
ENEMY_SPEED = 5
ENEMY_SPEED_DOWN = 1
ENEMY_SPAWN_DELAY = 500  # millisecondes

# Projectiles
BULLET_SPEED = 10
SHOOT_DELAY = 600  # millisecondes

# Décor
BACKGROUND_SPEED = 2

# Score
SCORE_UPDATE_DELAY = 50  # millisecondes
ENEMY_POINTS = 50
SCORE_FONT_SIZE = 36
SCORE_X = 20
SCORE_Y = 50
BONUS_DURATION = 1000  # millisecondes

# Vies
PLAYER_MAX_LIVES = 3
LIFE_BAR_WIDTH = 150
LIFE_BAR_HEIGHT = 20
LIFE_BAR_X = 20
LIFE_BAR_Y = 20

# Couleurs RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Jeu
FPS = 60
REFERENCE_FRAME = 1000 / FPS # 16.67 ms par frame

SHURIKEN_AMPLITUDE = 120    # largeur de la courbe, en pixels
SHURIKEN_LONGUEUR = 80      # plus c'est grand, plus la courbe est étirée

# Indication du changement d'arme (sous la barre de vie et le score)
HINT_TEXT = "Flèche du haut : changer d'arme"
HINT_FONT_SIZE = 22
HINT_X = 20
HINT_Y = 82
