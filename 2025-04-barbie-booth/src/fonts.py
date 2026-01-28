import pygame

# Initialize font system (only needed once in your whole app)
pygame.font.init()

# Load a custom font (or use a system font fallback)
def load_main_font(size=32):
    return pygame.font.Font("fonts/bartex.ttf", size)  # Custom font

# OR if you want to use a system font
def load_system_font(size=32):
    return pygame.font.SysFont("arial", size)