
import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 800))
clock = pygame.time.Clock()

running = True

while running:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()

    print(f"FPS : {clock.get_fps():.1f}")

pygame.quit()
