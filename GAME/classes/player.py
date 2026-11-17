import pygame
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
class Player:
    def __init__(self, x, y, speed, direction, vy, limite_droite):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.vy = vy  # deplacement animation
        self.limite_droite = limite_droite

    def move(self, direction):
        self.x += self.speed * direction
        self.x = max(0, min(self.x, self.limite_droite)) # min pour droite , max pour gauche


class Avion(Player):
    def __init__(self, x, y, direction, vy, limite_droite, images):
        super().__init__(x, y, 8, direction, vy, limite_droite)

        self.images = images
        self.playerImg = images["normal"]

        self.playerImg_normal = images["normal"]
        self.playerImg_left = images["normal_left"]
        self.playerImg_right = images["normal_right"]

    def changer_image(self, vies, direction):
        if vies >= 3:
            etat = "normal"
        elif vies == 2:
            etat = "damaged"
        else:
            etat = "critical"

        if direction == -1:
            self.playerImg = self.images[etat + "_left"]
        elif direction == 1:
            self.playerImg = self.images[etat + "_right"]
        else:
            self.playerImg = self.images[etat]

    # TODO mettre dans class Player
    def afficher(self, screen):
        screen.blit(self.playerImg, (self.x, self.y))
   
