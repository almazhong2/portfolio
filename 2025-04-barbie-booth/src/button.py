import pygame
import game
import fonts

class Button:
    def __init__(self, text, x, y, width, height, color, hover):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover = hover
        self.curr_color = color
    
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.curr_color, (self.x, self.y, self.width, self.height))
        txt = font.render(self.text, True, (0, 0, 0))
        screen.blit(txt, (self.x + (self.width - txt.get_width())/ 2, self.y + (self.height - txt.get_height()) / 2))

    def collide(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            self.curr_color = self.hover
        else:
            self.curr_color = self.color
    
    def clicked(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

class ImageButton:
    def __init__(self, path, x, y, flipped=False, scale=1, should_scale=False, text=None):
        self.image = pygame.image.load(path).convert_alpha()
        if flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        if should_scale:
            self.image = pygame.transform.scale(self.image, (scale, scale))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.text = text
        if text:
            self.font = fonts.load_main_font(int(self.image.get_width()/10))
            self.text_surface = self.font.render(text, True, (0,0,0))
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.text:
            screen.blit(self.text_surface, (self.rect[0] + self.image.get_width()/2 - self.text_surface.get_width()/2, self.rect[1] + self.image.get_height()/2 - self.text_surface.get_height()/2))

    def clicked(self, mouse_pos):
        #go back to this
        return self.rect.collidepoint(mouse_pos)