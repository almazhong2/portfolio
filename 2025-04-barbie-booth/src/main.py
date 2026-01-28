import pygame
from start import Start
import game
from character import Character
from play import Play
from end import End
from fonts import *

pygame.init()

window = screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, display=0)

pygame.display.set_caption("Start")
run = True

state = "start"

start = Start(window)
character = Character(window)
play = None
end = None
my_font = load_main_font(int(screen.get_width() / 15))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and (event.mod & pygame.KMOD_CTRL):
                run = False
    
        if state == "start":
            result = start.state(event)
            if result == "character":
                state = "character"
        elif state == "character":
            result = character.state(event)
            if result == "play":
                play = Play(window, character.dolls[character.currImage], 
                            character.skinValue, character.hair_idx, character.hairValue, character.eyeValue)
                state = "play"
        elif state == "play":
            result = play.state(event)
            if result == "end":
                end = End(window, play.doll, 
                          play.skinValue, play.hair_idx, play.hairValue, play.eyeValue, play.option)
                state = "end"
        elif state == "end":
            result = end.state(event)
            if result == "start":
                start = Start(window)
                character = Character(window)
                state = "start"


    if state == "character":
        character.draw()
    elif state == "start":
        start.draw()
    elif state == "play":
        play.draw()
    elif state == "end":
       end.draw()
    
    pygame.display.update()

pygame.quit()