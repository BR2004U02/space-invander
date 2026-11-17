import pygame

score_value = 0

scoreX = 20
scoreY = 50
# position du score en dessous de la barre de vie


def afficher_score(screen, score_value, font, bonus_alpha):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (scoreX, scoreY))

    # +50 à côté du score si ennemi touché
    if bonus_alpha > 0:
        bonus = font.render("+50", True, (0, 255, 0))
        bonus.set_alpha(bonus_alpha)
        screen.blit(bonus, (scoreX + score.get_width() + 15, scoreY))

# show_score(textX, testY) => GAME LOOP / afficher score

def afficher_vie(screen, vies, max_vies, largeur, hauteur, x, y):
    pygame.draw.rect(screen, (255, 0, 0), (x, y, largeur, hauteur))

    largeur_vie = largeur * max(0, vies) / max_vies

    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (x, y, largeur_vie, hauteur)
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (x, y, largeur, hauteur),
        2
    )

def game_over(screen, score):
    over_font = pygame.font.Font(None, 64)
    score_font = pygame.font.Font(None, 36)

    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    score_text = score_font.render("Score : " + str(score), True, (255, 255, 255))

    screen.blit(over_text, (screen.get_width() // 2 - over_text.get_width() // 2, 300))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 380))