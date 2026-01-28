from cmu_graphics import *
import util

#will snap the player to be aligned with the terrain
def snapTerrainY(app, i):
    tierHeight = app.height // len(app.world)
    y = app.height - (i + 1)*tierHeight + 60
    return y

def snapTerrainX(app, j):
    tierWidth = app.width // 15 #allow 15 hops width
    x = tierWidth * (j) 
    return x

class Player:

    def __init__(self, x, y, hopHeight, frames, width, height, depth):
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height
        self.depth = depth

        #hopping coordinates start off stationary
        self.x1 = x
        self.y1 = y

        self.x2 = x
        self.y2 = y

        self.depth = 25

        self.hopHeight = hopHeight
        self.currentFrame = 0
        self.totalFrames = frames
        self.isHopping = False
        
    def getTier(self, app):
        y = self.y
        tierHeight = app.height // len(app.world)
        tier = ((app.height - y) // tierHeight) - 1

        if tier < 0:
            tier = 0
        elif tier >= len(app.world):
            tier = len(app.world) - 1
    
    def hop(self):
        if self.isHopping == False:
            self.currentFrame = 0
            self.isHopping = True

    def updateHop(self):
        if self.isHopping:
            time = self.currentFrame / self.totalFrames
            #chatGPT: formula for frame by frame hopping (in a parabolic motion)
            self.y = self.y = (1-time)*self.y1 + time*self.y2
            self.y += 4*self.hopHeight*(time - 0.5)**2

            self.currentFrame +=1

            if self.currentFrame >= self.totalFrames:
                self.y = self.y
                self.isHopping = False
    
    def snapTerrain(self, app, i, j):
        x = snapTerrainX(app, j)
        y = snapTerrainY(app, i)
        return x, y

    def drawPlayer(self, app):
        util.drawBorderBlock(self.x, self.y, self.width, self.height, self.depth, app.playerColor)


