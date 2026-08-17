import pygame  # type: ignore

pygame.init()
screen = pygame.display.set_mode((400, 300))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    pygame.draw.circle(screen, "red", (100, 150), 40)
    pygame.draw.rect(screen, "blue", (200, 100, 120, 80))
    pygame.draw.line(screen, "black", (0, 0), (400, 300), 3)
    pygame.display.flip()

pygame.quit()
