import pygame
import game
from button import Button, ImageButton
from pathlib import Path

window = pygame.display.set_mode((game.screen_width, game.screen_height))

def calculateLineColor(skinColor):
    r = skinColor[0] * game.LINE_RATIO[0]
    g = skinColor[1] * game.LINE_RATIO[1]
    b = skinColor[2] * game.LINE_RATIO[2]
    return (r,g,b)

def draw_character():
    window.fill(game.BACKGROUND)

class Character:
    def __init__(self, screen, skinval = 0, hair_idx = 0, hairval = 0, eyeval = 0):
        self.screen = screen
        self.dolls = [pygame.image.load('graphics/base/base_model.png').convert_alpha()]

        #0: skin 1: hairstyle 2: hair color 3: eye color
        self.option = 0
        
        #skin
        self.skin = pygame.image.load('graphics/base/skin_base.png').convert_alpha()
        self.skinMask = pygame.mask.from_surface(self.skin)
        self.skinValue = skinval
        self.skinSurface = self.skinMask.to_surface(setcolor=self.getSkinColor(), unsetcolor=(0,0,0,0))
        
        
        #base
        self.lines = pygame.image.load('graphics/base/lineart.png').convert_alpha()
        self.linesMask = pygame.mask.from_surface(self.lines)
        self.lineColor = ()
        self.lineSurface = self.linesMask.to_surface(setcolor=calculateLineColor(self.getSkinColor()), unsetcolor=(0,0,0,0))
        
        #hair
        self.hair = []
        for file in Path('graphics/hair').glob("*.png"):
            if file.is_file():
                self.hair.append(pygame.image.load(str(file)))
        self.hair_idx = hair_idx
        self.hairMask = pygame.mask.from_surface(self.hair[self.hair_idx])
        self.hairValue = hairval
        self.hairSurface = self.hairMask.to_surface(setcolor = self.getHairColor(), unsetcolor = (0,0,0,0))
        
        #eyes
        self.eyes = pygame.image.load('graphics/eyes/eyes.png')
        self.eyeMask = pygame.mask.from_surface(self.eyes)
        self.eyeValue = eyeval
        self.eyeSurface = self.eyeMask.to_surface(setcolor = self.getEyeColor(), unsetcolor = (0,0,0,0))
        
        #clothes
        self.robe = pygame.image.load('graphics/clothes/robe.png')
        
        self.currImage = 0
        self.font = pygame.font.SysFont('arial', int(game.screen_width/25))

        self.width = screen.get_width()
        self.height = screen.get_height()
        arrow_size = self.width/20
        doll_left_corner = self.width/2 - self.robe.get_width()/2


        self.buttons = [ImageButton('graphics/buttons/r_arrow.png', doll_left_corner - arrow_size,
                                    (self.height-arrow_size)/2, True, arrow_size, True),
                        ImageButton('graphics/buttons/r_arrow.png', doll_left_corner + self.robe.get_width(),
                                    (self.height-arrow_size)/2, False, arrow_size, True)]
        self.select = Button("select", (3*self.width/4)/2, 4*self.height/5, self.width/4, self.height/12, game.PINK, game.LIGHT_PINK)
        self.play = False
        self.beautybar = pygame.image.load('graphics/buttons/bar.png').convert_alpha()
        self.bottom_cover = pygame.Surface((2560, 300))
        self.bottom_cover.fill(game.BACKGROUND)

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
        self.screen.fill(game.BACKGROUND)
        
        if not self.play:
            scale = 0.5
            half = self.width / 2
            iwidth = half - self.robe.get_width()*0.5
            iheight = self.height/2 - 600
            ix = (self.width - iwidth)/2
            iy = (self.height - iheight)/2
            self.screen.blit(self.dolls[self.currImage], (iwidth, iheight))
            self.screen.blit(self.skinSurface, (iwidth, iheight))
            #self.screen.blit(self.lineSurface, (ix, iy))
            self.screen.blit(self.robe, (iwidth,iheight))
            self.screen.blit(self.eyeSurface, (iwidth, iheight))


            self.screen.blit(self.hair[self.hair_idx], (iwidth, iheight))
            self.screen.blit(self.hairSurface, (iwidth, iheight))


            self.screen.blit(self.bottom_cover, (0, 1300))
            self.screen.blit(self.beautybar, (0,0))
            
            

        for button in self.buttons:
            button.draw(self.screen)

        self.select.draw(self.screen, self.font)


    def state(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.play:
            if self.select.clicked(pygame.mouse.get_pos()):
                if self.option != 3:
                    self.option += 1
                elif self.option == 3:
                    self.option = 0
                    self.play = True
            elif (self.buttons[1].clicked(pygame.mouse.get_pos())):
                if self.option == 0:
                    if self.skinValue < len(game.SKIN_COLORS) - 1:
                        self.skinValue += 1
                        self.skinSurface = self.skinMask.to_surface(setcolor=self.getSkinColor(), unsetcolor=(0,0,0,0))
                        self.linesMask.to_surface(setcolor=calculateLineColor(self.getSkinColor()), unsetcolor=(0,0,0,0))
                if self.option == 1:
                    if self.hair_idx < len(self.hair) - 1:
                        self.hair_idx += 1
                        self.hairMask = pygame.mask.from_surface(self.hair[self.hair_idx])
                        self.hairSurface = self.hairMask.to_surface(setcolor=self.getHairColor(), unsetcolor = (0,0,0,0))
                if self.option == 2:
                    if self.hairValue < len(game.HAIR_COLORS) - 1:
                        self.hairValue += 1
                        self.hairSurface = self.hairMask.to_surface(setcolor=self.getHairColor(), unsetcolor = (0,0,0,0))
                if self.option == 3:
                    if self.eyeValue < len(game.EYE_COLORS) - 1:
                        self.eyeValue += 1
                        self.eyeSurface = self.eyeMask.to_surface(setcolor=self.getEyeColor(), unsetcolor = (0,0,0,0))
            elif self.buttons[0].clicked(pygame.mouse.get_pos()):
                if self.option == 0:
                    if self.skinValue > 0:
                        self.skinValue -= 1
                        self.skinSurface = self.skinMask.to_surface(setcolor=self.getSkinColor(), unsetcolor=(0,0,0,0))
                        self.linesMask.to_surface(setcolor=calculateLineColor(self.getSkinColor()), unsetcolor=(0,0,0,0))
                if self.option == 1:
                    if self.hair_idx > 0:
                        self.hair_idx -= 1
                        self.hairMask = pygame.mask.from_surface(self.hair[self.hair_idx])
                        self.hairSurface = self.hairMask.to_surface(setcolor=self.getHairColor(), unsetcolor = (0,0,0,0))
                if self.option == 2:
                    if self.hairValue > 0:
                        self.hairValue -= 1
                        self.hairSurface = self.hairMask.to_surface(setcolor = self.getHairColor(), unsetcolor = (0,0,0,0))
                if self.option == 3:
                    if self.eyeValue > 0:
                        self.eyeValue -= 1
                        self.eyeSurface = self.eyeMask.to_surface(setcolor=self.getEyeColor(), unsetcolor=(0,0,0,0))
        if self.play:
            self.play = False
            return "play"

        self.select.collide(pygame.mouse.get_pos())

        return "character"