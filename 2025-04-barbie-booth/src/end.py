import pygame
import game
from button import Button
import random
from pathlib import Path
import fonts
import positioning

class End:
    def __init__(self, screen, doll, skinValue, hair_idx, hairValue, eyeValue, outfit):
        self.screen = screen
        self.font = pygame.font.SysFont('arial', int(game.screen_width/25))
        self.mainFont = fonts.load_main_font(int(screen.get_width()/20))
        self.words = ["Fabulous!", "Perfect!", "Awesome!", "Super!"]
        self.word = random.choice(self.words)

        self.width = game.screen_width
        self.height = game.screen_height
        button_width = game.screen_width/4
        button_height = game.screen_height/12

        self.email = Button("email", 4*self.width/5,
                            4*self.height/5, button_width, button_height,
                            game.PINK, game.LIGHT_PINK)

        self.restart = Button("restart", 4*self.width/5,
                            4*self.height/5 + 6*button_height/5, button_width, button_height,
                            game.PINK, game.LIGHT_PINK)
        
        self.doll = doll
        self.skinValue = skinValue
        self.hair_idx = hair_idx
        self.hairValue = hairValue
        self.eyeValue = eyeValue


        self.skin = pygame.image.load('graphics/base/skin_base.png').convert_alpha()
        self.skinMask = pygame.mask.from_surface(self.skin)
        self.skinSurface = self.skinMask.to_surface(setcolor=self.getSkinColor(), unsetcolor=(0,0,0,0))

        self.hair = []
        for file in Path('graphics/hair').glob("*.png"):
            if file.is_file():
                self.hair.append(pygame.image.load(str(file)))
        self.hairMask = pygame.mask.from_surface(self.hair[self.hair_idx])
        self.hairSurface = self.hairMask.to_surface(setcolor = self.getHairColor(), unsetcolor = (0,0,0,0))

        self.eyes = pygame.image.load('graphics/eyes/eyes.png')
        self.eyeMask = pygame.mask.from_surface(self.eyes)
        self.eyeSurface = self.eyeMask.to_surface(setcolor = self.getEyeColor(), unsetcolor = (0,0,0,0))

        self.outfit = pygame.image.load(game.OUTFITS[outfit])
        self.option = outfit
        self.hat = pygame.image.load(game.HATS[1])

    def getSkinColor(self, alpha=100):
        sc = game.SKIN_COLORS[self.skinValue]
        return (sc[0], sc[1], sc[2], alpha)
    
    def getHairColor(self, alpha=125):
        hc = game.HAIR_COLORS[self.hairValue]
        return (hc[0], hc[1], hc[2], alpha)
    
    def getEyeColor(self, alpha = 125):
        ec = game.EYE_COLORS[self.eyeValue]
        return (ec[0], ec[1], ec[2], alpha)
    
    def draw(self):
        
        self.screen.fill(game.WHITE)
        text = self.mainFont.render(self.word, True, game.PINK)
        self.screen.blit(text, (4*self.width/5 + text.get_width()/4, self.height/2))
                         
        #pygame.draw.rect(self.screen, game.PINK, [framex, framey, frame, frame], 10)
        #self.screen.blit(pygame.transform.scale(self.doll, (iwidth, iheight)), (ix, iy))

        self.email.draw(self.screen, self.font)
        self.restart.draw(self.screen, self.font)
        
        scale = 0.5
        pos = 2* self.width / 5
        iwidth = pos - self.outfit.get_width()*0.5
        iheight = self.height/2 - 300
        ix = (self.width - iwidth)/2
        iy = (self.height - iheight)/2
        self.screen.blit(self.doll, (iwidth, iheight))
        self.screen.blit(self.skinSurface, (iwidth, iheight))
        #self.screen.blit(self.lineSurface, (ix, iy))
        
        self.screen.blit(self.hair[self.hair_idx], (iwidth, iheight))
        self.screen.blit(self.hairSurface, (iwidth, iheight))

        self.screen.blit(self.outfit, (iwidth,iheight))
        if self.option != 0:
            self.hat = pygame.image.load(game.HATS[self.option])
            self.screen.blit(self.hat, (iwidth, iheight))
        self.screen.blit(self.eyeSurface, (iwidth, iheight))



    def state(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart.clicked(pygame.mouse.get_pos()):
                return "start"

        self.restart.collide(pygame.mouse.get_pos())
        self.email.collide(pygame.mouse.get_pos())

        return "end"
