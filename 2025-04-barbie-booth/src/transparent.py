import pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Reveal Image Tool")

# Load or create two images
bottom_image = pygame.image.load('graphics/barbies/barbie.png').convert_alpha()
#bottom_image.fill((0, 150, 255))  # Simulate an image with a blue fill

top_image = pygame.image.load('graphics/clothes/construction.png').convert_alpha()
#top_image.fill((100, 100, 100, 255))  # Gray overlay

screen.blit(bottom_image, (0, 0))
screen.blit(top_image, (0, 0))

# Eraser tool setup
eraser_radius = 30
revealing = False

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            revealing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            revealing = False

    if revealing:
        mouse_pos = pygame.mouse.get_pos()
        # Draw transparent circle on top image to "reveal" bottom image
        pygame.draw.circle(top_image, (0, 0, 0, 0), mouse_pos, eraser_radius)

    # Draw everything
    screen.blit(bottom_image, (0, 0))
    screen.blit(top_image, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

