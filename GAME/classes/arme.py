# arme + balle
# recuperer la position du canon  pour y tirer la balle correctement positionné 
# bonus tirer grace a la souris + viser


import pygame
import math

from classes.entite import Entite
from config.config import REFERENCE_FRAME


class Bullet(Entite):
    def __init__(self, image):
        super().__init__(0, 0, image)
        self.speed = 10
        self.state = "ready"

    def fire(self, x, y):
        if self.state == "ready":
            self.x = x
            self.y = y
            self.hitbox.topleft = (self.x, self.y)
            self.state = "fire"

    def update(self, dt):
        if self.state == "fire":
            self.y -= self.speed * (dt / REFERENCE_FRAME)
            self.hitbox.y = self.y

            if self.y < 0:
                self.state = "ready"

    def afficher(self, screen):
        if self.state == "fire":
            super().afficher(screen)

class EnemyBullet(Entite): # va vers la position du joueur lors du tir
    def __init__(self, image, x, y, target_x, target_y):
        super().__init__(x, y, image)
        self.speed = 4 # vitesse de balles ennemies

        dx = target_x - x # diff entre balle au début et joueur
        dy = target_y - y
        distance = math.hypot(dx, dy)

        self.direction_x = dx / distance # direction à prendre
        self.direction_y = dy / distance

        self.hitbox = self.hitbox.inflate(-17, -17) # à changer si trop faicile/compliqué à esquiver les tirs ennemis

    def update(self, dt):
        self.x += self.direction_x * self.speed * (dt / REFERENCE_FRAME) # déplacemeent (vecteur de déplacement)
        self.y += self.direction_y * self.speed * (dt / REFERENCE_FRAME)

        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def afficher(self, screen):
        super().afficher(screen)


class Weapon:
    def __init__(self, bullet_image):

        self.bullet_image = bullet_image
        self.bullets = []

        self.last_shot = 0
        self.shoot_delay = 600 # firerate (en millisecondes)

    def create_2_bullets(self, x, y):

        bullet1 = Bullet(self.bullet_image)
        bullet2 = Bullet(self.bullet_image)

        bullet1.fire(x - 5, y)
        bullet2.fire(x + 55, y)

        self.bullets.append(bullet1)
        self.bullets.append(bullet2)

    def shoot_continuous(self, x, y):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot >= self.shoot_delay:
            self.create_2_bullets(x, y)
            self.last_shot = current_time

    def update(self, dt):
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.state == "ready":
                self.bullets.remove(bullet)

    def afficher(self, screen):
        for bullet in self.bullets:
            bullet.afficher(screen)

class EnemyWeapon:
    def __init__(self, bullet_image):
        self.bullet_image = bullet_image
        self.bullets = []
        self.last_shot = 0
        self.shoot_delay = 5000 # délai entre les tirs 

    def shoot(self, x, y, player):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot >= self.shoot_delay:
            bullet = EnemyBullet(
                self.bullet_image,
                x, y,
                player.x + player.hitbox.width / 2,
                player.y + player.hitbox.height / 2
            )

            self.bullets.append(bullet)
            self.last_shot = current_time

    def update(self, dt):
        for bullet in self.bullets[:]:
            bullet.update(dt)

            if bullet.y > 800 or bullet.x < 0 or bullet.x > 1280:
                self.bullets.remove(bullet)

    def afficher(self, screen):
        for bullet in self.bullets:
            bullet.afficher(screen)