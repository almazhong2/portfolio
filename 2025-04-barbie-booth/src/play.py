
import pygame
import game
from button import Button, ImageButton
import fonts
from pathlib import Path

class Play:
    def __init__(self, screen, image, skinValue, hair_idx, hairValue, eyeValue):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        #indices
        self.skinValue = skinValue
        self.hair_idx = hair_idx
        self.hairValue = hairValue
        self.eyeValue = eyeValue
        self.doll = image
        self.option = 0

        #skin
        self.skin = pygame.image.load('graphics/base/skin_base.png').convert_alpha()
        self.skinMask = pygame.mask.from_surface(self.skin)
        self.skinSurface = self.skinMask.to_surface(setcolor=self.getSkinColor(), unsetcolor=(0,0,0,0))
        self.reveal = self.skinSurface.copy()

        #hair
        self.hair = []
        for file in Path('graphics/hair').glob("*.png"):
            if file.is_file():
                self.hair.append(pygame.image.load(str(file)))
        self.hairMask = pygame.mask.from_surface(self.hair[self.hair_idx])
        self.hairSurface = self.hairMask.to_surface(setcolor = self.getHairColor(), unsetcolor = (0,0,0,0))

        #eyes
        self.eyes = pygame.image.load('graphics/eyes/eyes.png')
        self.eyeMask = pygame.mask.from_surface(self.eyes)
        self.eyeSurface = self.eyeMask.to_surface(setcolor = self.getEyeColor(), unsetcolor = (0,0,0,0))

        #outfit
        self.outfit = pygame.image.load(game.OUTFITS[self.option])
        self.hat = pygame.image.load(game.HATS[self.option+1])

        #makeup
        self.mascara = pygame.image.load('graphics/mascara/m_2.png').convert_alpha()

        #tools
        self.eraser_radius = 30
        self.revealing = False

        self.step = 'mascara'

        #ui/buttons
        self.font = fonts.load_main_font(int(self.width/25))
        self.corner = Button("", 4*self.width/5,
                             self.height/12,
                             self.width/8, self.width/8, game.PINK, game.LIGHT_PINK)
        self.width = screen.get_width()
        self.height = screen.get_height()
        arrow_size = self.width/20
        doll_left_corner = self.width/2 - self.outfit.get_width()/2
        self.buttons = [ImageButton('graphics/buttons/r_arrow.png', doll_left_corner - arrow_size,
                                    (self.height-arrow_size)/2, True, arrow_size, True),
                        ImageButton('graphics/buttons/r_arrow.png', doll_left_corner + self.outfit.get_width(),
                                    (self.height-arrow_size)/2, False, arrow_size, True)]
        self.select = Button("select", (3*self.width/4)/2, 4*self.height/5, self.width/4, self.height/12, game.PINK, game.LIGHT_PINK)


        self.pop = False
        pop_width, pop_height = self.width / 2, self.height / 2
        pop_x = (self.width - pop_width) // 2
        pop_y = (self.height - pop_height) // 2
        self.popup = pygame.Rect(pop_x, pop_y, pop_width, pop_height)

        button_width, button_height = self.width/4, self.height/12
        button_x = pop_x + (pop_width - button_width) // 2

        self.finish = Button("finish", (self.width - button_width)/2,
                             2*self.height/5,
                             button_width, button_height, game.WHITE, game.LIGHT_PINK)
        self.resume = Button("resume", (self.width - button_width)/2,
                              self.height/2,
                               button_width, button_height, game.WHITE, game.LIGHT_PINK)

    
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

        #ix = (self.width - self.doll.get_width()) / 2 
        #iy = (self.height - self.doll.get_height()) / 2
        #self.screen.blit(self.doll, (ix, iy))
        #scale = 0.5
        half = self.width / 2
        iwidth = half - self.outfit.get_width()*0.5
        iheight = self.height/2 - 600
        #ix = (self.width - iwidth)/2
        #iy = (self.height - iheight)/2

        #skin
        self.screen.blit(self.doll, (iwidth, iheight))
        self.screen.blit(self.skinSurface, (iwidth, iheight))

        self.screen.blit(self.mascara, (iwidth, iheight))

        #second skin layer
        self.screen.blit(self.skin, (iwidth, iheight))
        self.screen.blit(self.reveal, (iwidth, iheight))

    
        self.screen.blit(self.outfit, (iwidth,iheight))
        self.screen.blit(self.eyeSurface, (iwidth, iheight))
        self.screen.blit(self.hair[self.hair_idx], (iwidth, iheight))
        self.screen.blit(self.hairSurface, (iwidth, iheight))
        if self.option != 0:
            self.screen.blit(self.hat, (iwidth, iheight))

        if self.step == 'outfit':
            for button in self.buttons:
                button.draw(self.screen)
        
        #self.screen.blit(self.top, (iwidth, iheight))

        #self.screen.blit(self.lineSurface, (ix, iy)

        #self.screen.blit(self.bottom_cover, (0, 1300))
        #self.screen.blit(self.beautybar, (0,0))

        self.corner.draw(self.screen, self.font)

        if self.pop:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0,0))

            self.finish.draw(self.screen, self.font)
            self.resume.draw(self.screen, self.font)
        
        #list steps for now
        if self.step != 'finish':
            self.select.draw(self.screen, self.font)
    
        self.font = fonts.load_main_font(int(self.screen.get_width()/20))
        if self.step == 'mascara':
            self.text = self.font.render("Mascara", True, (0, 0, 0))
        elif self.step == 'blush':
            self.text = self.font.render("Blush", True, (0, 0, 0))
        elif self.step == 'lipstick':
            self.text = self.font.render("Lipstick", True, (0, 0, 0))
        elif self.step == 'outfit':
            self.text = self.font.render("Outfit", True, (0, 0, 0))
        else:
            self.text = self.font.render("Finished!", True, (0, 0, 0))
        
        self.screen.blit(self.text, (self.screen.get_width()/2 - self.text.get_width()/2, 100))
    
        pygame.display.flip()
        

    def state(self, event):
        iwidth = int(self.width/2 - self.outfit.get_width()*0.5)
        iheight = int(self.height/2 - 600)
        pos = pygame.mouse.get_pos()
        relative = (pos[0] - iwidth, pos[1] - iheight)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.select.clicked(pos):
                if self.step == 'mascara':
                    self.step = 'blush'
                elif self.step == 'blush':
                    self.step = 'lipstick'
                elif self.step == 'lipstick':
                    self.step = 'outfit'
                elif self.step == 'outfit':     
                    self.step = 'finish'
            if self.pop:
                if self.finish.clicked(pos):
                    return "end"
                elif self.resume.clicked(pos):
                    self.pop = False
            else:
                if self.corner.clicked(pos):
                    self.pop = True
                self.revealing = True
            
            #outfit selection
            if self.step == 'outfit':
                if (self.buttons[1].clicked(pygame.mouse.get_pos())):
                    if self.option < len(game.OUTFITS) - 1:
                        self.option += 1
                        self.outfit = pygame.image.load(game.OUTFITS[self.option])
                        self.hat = pygame.image.load(game.HATS[self.option])
                elif self.buttons[0].clicked(pygame.mouse.get_pos()):
                    if self.option > 0:   
                        self.option -= 1
                        if self.option != 0:
                            self.hat = pygame.image.load(game.HATS[self.option])
                        self.outfit = pygame.image.load(game.OUTFITS[self.option])

            
        elif event.type == pygame.MOUSEBUTTONUP:
            self.revealing = False
        
        if self.revealing:
            if self.step == 'mascara':
                pygame.draw.circle(self.reveal, (0,0,0,0), relative, self.eraser_radius)
                pygame.draw.circle(self.skin, (0,0,0,0), relative, self.eraser_radius )

        if self.pop:
            self.finish.collide(pygame.mouse.get_pos())
            self.resume.collide(pygame.mouse.get_pos())
        else:
            self.corner.collide(pygame.mouse.get_pos())
            self.select.collide(pygame.mouse.get_pos())

        return "play"
