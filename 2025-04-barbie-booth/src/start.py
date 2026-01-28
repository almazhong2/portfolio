import pygame
from button import Button, ImageButton
import game
from fonts import *
import positioning

window = pygame.display.set_mode((game.screen_width, game.screen_height))

class Start:
    def __init__(self, screen):
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.button_width = 471
        self.button_height = 193
        self.howto_dimension = self.width/2
        self.button_centered = positioning.centerScreen(screen, self.button_width, self.button_height)

        self.buttons = [ImageButton("buttons/rectangle button.png", self.button_centered[0],
                               self.button_centered[1], text="Start Game"),
                        ImageButton("buttons/rectangle button.png", self.button_centered[0],
                               self.button_centered[1] + self.button_height + 10, text="More Help")]

        self.xout = Button("X", (self.width + self.howto_dimension) / 2 - self.howto_dimension / 6,
                      (self.height - self.howto_dimension) / 2 + self.howto_dimension / 12,
                      self.howto_dimension / 12, self.howto_dimension / 12, game.PINK, game.LIGHT_PINK)

        self.font = load_main_font(int(screen.get_width()/20))
        self.text = self.font.render("Barbie Makeover Madness", True, (0, 0, 0))
        self.howto = False
        self.screen = screen
        self.barbie = pygame.image.load('graphics/barbies/Barbie_doing_makeup.png').convert_alpha()
    
    def draw(self):
        self.screen.fill(game.BACKGROUND)
        self.screen.blit(self.barbie, (0,0))
        self.screen.blit(self.text, (self.screen.get_width()/2 - self.text.get_width()/2, 100))
        for button in self.buttons:
            button.draw(self.screen)
        
        if self.howto:
            pygame.draw.rect(self.screen, game.WHITE, ((self.width - self.howto_dimension)/2,
                                                       (self.height - self.howto_dimension)/2,
                                                       self.howto_dimension, self.howto_dimension))

            self.xout.draw(self.screen)


    def state(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.howto:
                if self.xout.clicked(pygame.mouse.get_pos()):
                    self.howto = False
                return "start"
            if self.buttons[0].clicked(pygame.mouse.get_pos()):
                return "character"
            elif self.buttons[1].clicked(pygame.mouse.get_pos()):
                self.howto = True

        return "start"