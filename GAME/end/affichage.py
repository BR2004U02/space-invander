import pygame

score_value = 0

scoreX = 20
scoreY = 50
# position du score en dessous de la barre de vie

def game_over(screen, score):
    over_font = pygame.font.Font(None, 64)
    score_font = pygame.font.Font(None, 36)

    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    score_text = score_font.render("Score : " + str(score), True, (255, 255, 255))

    screen.blit(over_text, (screen.get_width() // 2 - over_text.get_width() // 2, 300))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 380))