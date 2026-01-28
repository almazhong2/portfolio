from cmu_graphics import *
import random as py_random
import util
from player import *
import world
from Car import *
from Collectible import *

#big game functions
def onAppStart(app):

    #menu starters
    app.background = gradient('gray', 'gainsboro', start = 'top')
    app.width = 1600
    app.height = 1050
    
    #modes
    app.gameMode = False
    app.charMode = False
    app.menuMode = True
    app.aboutMode = False
    app.gameOver = False
    app.popUp = False
    app.state = 'game over!'

    #button colors
    app.playColor = 'gray'
    app.charColor = 'gray'
    app.aboutColor = 'gray'

    #world lists
    app.world = ['grass', 'road', 'road', 'grass', 'grass', 
                 'road', 'grass', 'grass', 'road', 'grass', 'road']
    app.seen = []

    #terrain generation
    app.cars = [[] for i in range(len(app.world))]
    app.greenery = [[] for i in range(len(app.world))]
    app.logs = [[] for i in range(len(app.world))]
    app.collectibles = [[] for i in range(len(app.world))]
    app.prevTerrain = None

    #timer events
    app.stepsPerSecond = 30
    app.counter = 0
    
    #player animations
    app.player = Player(0, 0, 50, app.stepsPerSecond//5, 75, 50, 25)
    app.playerYIndex = len(app.world)//2
    app.playerXIndex = 7
    startX, startY = app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex)
    app.player = Player(startX, startY, 50, app.stepsPerSecond//5, 75, 50, 25)
    app.charPlayer = Player(app.width*4/5, app.height*0.7, 20, 
                            app.stepsPerSecond//5, 450, 300, 150)
    
    #game counts
    app.hopCount = 0
    app.coinCount = 0
    app.totalCoins = 0
    app.backCount = 5 
    app.powerupCount = 0
    app.highScore = 0
    app.powerdownCount = 0 

    #powerup/powerdown functions
    #starpower
    app.playerColor = 'violet'
    app.characterColor = app.playerColor
    app.selectedColor = 'violet'
    app.powerup = False
    app.powerupColors = ['lightCoral', 'orange', 'lemonChiffon', 
                         'paleGreen', 'lightCyan', 'mediumPurple']
    app.colorIndex = 0
    app.poweruptimer = 150
    app.paused = False
    app.popup = False

    #skiplanes
    app.skip = False
    app.drawSkip = False
    app.skipLabelTimer = 25
    app.skiptimer = 150


    #boosted/dragged
    app.boost = False
    app.drag = False

    #ink
    app.ink = False
    app.balls = []

    #board variables
    app.currRow = None
    app.currCol = None

    #sounds

    #https://pixabay.com/sound-effects/swing-whoosh-110410/ 
    app.hopSound = Sound('sounds/hop.mp3')

    #https://pixabay.com/sound-effects/car-pass-by-9111/  
    app.whoosh = Sound('sounds/car.mp3')

    #https://www.myinstants.com/en/instant/mario-power-up/  
    app.powerUpSound = Sound('sounds/skip.mp3')

    #https://pixabay.com/sound-effects/water-splash-199583/  
    app.splash = Sound('sounds/splash.mp3')

    #https://www.myinstants.com/en/instant/mario-star-power/  
    app.starSound = Sound('sounds/starpower.mp3')
    app.playStar = True
    
    #https://pixabay.com/sound-effects/wah-103118/ 
    app.fail = Sound('sounds/fail.mp3')

    #https://pixabay.com/sound-effects/slime-splat-1-219248/ 
    app.inkSound = Sound('sounds/splat.mp3')

def redrawAll(app):
    if app.menuMode:
        util.drawMenu(app)
        util.drawStars(app)
        util.drawButtons(app)
    
    if app.charMode:
        util.drawBoard(app)
        app.charPlayer.drawPlayer(app)
        
        #back button
        drawRect(50, 50, app.width//8, app.height//10, 
                 fill = 'white', border = 'black', borderWidth = 5)
        drawLabel('back', 50+(app.width//16), 50+app.height//20, 
                  size = 50, font = 'orbitron', bold = True, fill = 'black', 
                  borderWidth = 2, align = 'center')
        
        #label
        drawRect(app.width*.6, 200, app.width//4, app.height//5, 
                 fill = 'white', border = 'black', borderWidth = 5)
        drawLabel('choose a color!', app.width*.6 +(app.width//8), 
                  200 + app.height//10, size = 50, font = 'orbitron', 
                  bold = True, fill = 'black', borderWidth = 2, align = 'center')
        
    if app.aboutMode:
        util.popup(app)

    if app.gameMode:
        world.drawWorld(app)
        for i in range (len(app.world)):
            terrain = app.world[i]
            if terrain == 'road' and i < len(app.cars):
                world.drawCars(app, app.cars[i], i)
        
        app.player.drawPlayer(app)
        
        if not app.gameOver and not app.paused:
            drawRect(50, 50, app.width//8, app.height//10, 
                    fill = 'white', border = 'black', borderWidth = 5)
            drawLabel('pause', 50+(app.width//16), 50+app.height//20, 
                      size = 50, font = 'orbitron', bold = True, fill = 'black', 
                      borderWidth = 2, align = 'center')
            
            drawRect(app.width//5, 50, app.width//6, app.height//10,
                    fill = 'white', border = 'black', borderWidth = 5)
            drawLabel(f'Back Hops Left: {app.backCount}', 
                    app.width//5 + app.width//12, 50 + app.height//20, 
                    size = 30, font = 'orbitron', bold = True, fill = 'black', 
                    borderWidth = 2, align = 'center')

            drawRect(app.width//5 + app.width//6 + app.width//20, 50, app.width//6, app.height//10,
                    fill = 'white', border = 'black', borderWidth = 5)    
            drawLabel(f'Total Hops: {app.hopCount}', app.width//5 + app.width//6 + app.width//20 + app.width//12, 
                      50 + app.height//20, size = 30, font = 'orbitron', bold = True, fill = 'black', 
                      borderWidth = 2, align = 'center')

            drawRect(app.width - 50, 50, app.width//8, app.height//10, 
                    fill = 'white', border = 'black', borderWidth = 5, align = 'right-top')    
            drawLabel(f'Coins: {app.coinCount}', app.width - 50 - app.width//8 + app.width//16,
                      50 + app.height//20,  size = 50, font = 'orbitron', bold = True, fill = 'black', 
                      borderWidth = 2, align = 'center')
        
        elif app.paused and app.popup:
            util.popup(app)
        
        #powerup/powerdown conditions
        if app.boost:
            #add rectangles in
            drawRect(app.width//2, app.height * .4, app.width//3, app.height//3, 
                     fill = 'white', border = 'black', borderWidth = 3, align = 'center')
            drawLabel('BOOSTED! +10 Hops', app.width//2, app.height * .4, 
                      size = 50, font = 'orbitron', bold = True, fill = 'black', 
                      borderWidth = 2, align = 'center')
            drawLabel('press enter to proceed', app.width//2, app.height//2, size = 20, font = 'orbitron',
                      fill = 'black', align = 'center')
        
        if app.drag:
            drawRect(app.width//2, app.height * .4, app.width//3, app.height//3, 
                     fill = 'white', border = 'black', borderWidth = 3, align = 'center')
            drawLabel('DRAGGED! -10 Hops', app.width//2, app.height * .4, 
                      size =50, font = 'orbitron', bold = True, fill = 'black', 
                      borderWidth = 2, align = 'center')
            drawLabel('press enter to proceed', app.width//2, app.height//2, size = 20, font = 'orbitron',
                      fill = 'black', align = 'center')

        
        if app.drawSkip:
            drawRect(app.width//2, app.height//2, app.width//5, app.height//10, 
                     fill = 'white', border = 'black', borderWidth = 3, align = 'center')
            drawLabel('Skip Lanes!!', app.width//2, app.height//2, size  =50, font = 'orbitron', 
                      bold = True, fill = 'black', 
                      borderWidth = 2, align = 'center')
        
        if app.ink:
            world.drawInk(app)

        if app.gameOver:
            util.popup(app)
    
def onStep(app):
    app.counter += 1 #consistent events timer

    if app.paused and app.gameMode:
        app.state = 'resume'
    #menu changes
    if app.menuMode:
        app.starAngle = (app.starAngle + app.starSpeed) % 360
        app.background = gradient('gray', 'gainsboro', start = 'top')
        app.state = 'details'
    
    if app.charMode:
        app.background = 'lightSkyBlue'
    
    if app.aboutMode:
        app.background = gradient('gray', 'gainsboro', start = 'top')


    if app.gameMode: 
        #player updates
        app.player.updateHop()
        app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex)        
        
        #world updates
        world.updateCars(app)
        world.updateCollectibles(app)
        
        if carCollision(app, app.player) and not app.player.isHopping and not app.powerup and not app.gameOver:
            app.whoosh.play()
            app.gameOver = True
        
        #collectible events
        if app.powerup:
            app.skip = False
            app.boost = False
            app.ink = False
            app.drag = False
            
            app.poweruptimer -= 1
            app.colorIndex = (app.colorIndex + 1) % len(app.powerupColors)
            app.playerColor = app.powerupColors[app.colorIndex]
            
            if app.poweruptimer <= 0:
                app.starSound.pause()
                app.playerColor = app.selectedColor
                app.powerup = False
        
        if app.ink:
            app.powerup = False
            app.skip = False
            app.boost = False
            app.drag = False

            app.inktimer -= 1
            if app.inktimer <= 0:
                app.ink = False
            else:
                #CMU CS Academy 6.3.3 Bouncing Motion
                for ball in app.balls:
                    ball['x'] += ball['dx']
                    ball['y'] += ball['dy']

                    if ball['x'] + ball['r'] >= app.width:
                        ball['x'] = app.width - ball['r']
                        ball['dx'] = -1 * ball['dx']
                    elif ball['x'] - ball['r'] <= 0:
                        ball['x'] = ball['r']
                        ball['dx'] = -1 * ball['dx']
                    
                    if ball['y'] + ball['r'] >= app.height:
                        ball['y'] = app.height - ball['r']
                        ball['dy'] = -1 * ball['dy']
                    elif ball['y'] - ball['r'] <= 0:
                        ball['y'] = ball['r']
                        ball['dy'] = -1 * ball['dy']
                        
        if app.drawSkip:
            app.powerup = False
            app.boost = False
            app.ink = False
            app.drag = False
            app.paused = True

            app.skipLabelTimer -= 1

            if app.skipLabelTimer <= 0:
                app.skip = True
                app.drawSkip = False
        
        if app.boost:
            app.powerup = False
            app.ink = False
            app.drag = False
            app.skip = False

            app.paused = True
        
        if app.drag:
            app.powerup = False
            app.ink = False
            app.boost = False
            app.skip = False

            app.paused = True

        if app.skip:
            app.paused = False
            app.skiptimer -= 1
            if app.skiptimer <= 0:
                app.skip = False

    if app.gameOver:
        app.state = 'game over!'
        app.paused = True
        if app.hopCount > app.highScore:
            app.highScore = app.hopCount
          
def onKeyPress(app, key):
    popCols(app)
    if app.boost:
        if key == 'enter':
            for i in range(10):
                updateWorld(app)
            while app.world[4] != 'grass':
                updateWorld(app)
            app.hopCount += 10 
            app.boost = False
            app.paused = False
    elif app.drag:
        if key == 'enter':
            for i in range(10):
                updateWorld(app)
                while app.world[4] != 'grass':
                    updateWorld(app)
            app.hopCount -= 10
            app.drag = False
            app.paused = False
    elif app.gameMode and not app.paused:  
        if app.powerup:
            if (key == 'up' or key == 'w'):
                app.hopSound.play()
                app.player.hop()
                updateWorld(app)
                app.hopCount += 1
                app.backCount = 5 
                
            elif (key == 'down' or key == 's'):
                reverseWorld(app)
                if app.backCount > 0:
                    app.backCount -=1
                else:
                    app.backCount = 0
                app.hopCount -= 1

            elif (key == 'left' or key == 'a') and app.player.x > 0:
                app.playerXIndex -= 1
                newX, newY = newX, newY = app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex)
                app.player.x = newX
            
            elif (key == 'right' or key == 'd') and app.player.x < app.width:
                app.playerXIndex += 1
                newX, newY = newX, newY = app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex)
                app.player.x = newX
        
        elif app.skip:
            if (key == 'up' or key == 'w') and doubleForwardLegal(app):
                app.hopSound.play()
                if inWater(app, key):
                    app.gameOver = True                
                app.player.hop()
                updateWorld(app)
                updateWorld(app)
                app.hopCount += 2
                app.backCount = 5                

            elif (key == 'down' or key == 's') and backwardLegal(app):
                reverseWorld(app)
                if app.backCount > 0:
                    app.backCount -=1
                else:
                    app.backCount = 0
                app.hopCount -= 1

            elif (key == 'left' or key == 'a') and leftLegal(app) and app.player.x > 0:
                if inWater(app, key):
                    app.gameOver = True
                app.playerXIndex -= 1
                newX, newY = newX, newY = app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex)
                app.player.x = newX
            
            elif (key == 'right' or key == 'd') and rightLegal(app) and app.player.x < app.width:
                if inWater(app, key):
                    app.gameOver = True
                app.playerXIndex += 1
                newX, newY = newX, newY = app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex)
                app.player.x = newX
        else:
            if (key == 'up' or key == 'w') and forwardLegal(app):
                app.hopSound.play()
                if inWater(app, key):
                    app.gameOver = True                
                app.player.hop()
                updateWorld(app)
                app.hopCount += 1
                app.backCount = 5                

            elif (key == 'down' or key == 's') and backwardLegal(app):
                reverseWorld(app)
                if app.backCount > 0:
                    app.backCount -=1
                else:
                    app.backCount = 0
                app.hopCount -= 1

            elif (key == 'left' or key == 'a') and leftLegal(app) and app.player.x > 0:
                if inWater(app, key):
                    app.gameOver = True
                app.playerXIndex -= 1
                newX, newY = newX, newY = app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex)
                app.player.x = newX
            
            elif (key == 'right' or key == 'd') and rightLegal(app) and app.player.x < app.width:
                if inWater(app, key):
                    app.gameOver = True
                app.playerXIndex += 1
                newX, newY = newX, newY = app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex)
                app.player.x = newX      
            
def onMousePress(app, mouseX, mouseY):
    #menu edits
    if app.menuMode:
        if util.playButton(mouseX, mouseY):
            app.gameMode = True
            app.menuMode = False
            app.charMode = False
            app.background = 'lightGray'
        elif util.charButton(mouseX, mouseY):
            app.gameMode = False
            app.charMode = True
            app.menuMode = False
        elif util.aboutButton(mouseX, mouseY):
            app.gameMode = False
            app.charMode = False
            app.menuMode = False
            app.aboutMode = True
            
    
    if app.aboutMode:
        if util.restartButton(mouseX, mouseY):
            app.menuMode = True
            app.aboutMode = False

    if app.charMode:
        app.background = 'lightSkyBlue'
        row, col = util.getCurrentCell(app)
        if row != None and col != None:
            app.playerColor = app.charColors[row][col]
            app.selectedColor = app.charColors[row][col]
        
        if util.backButton(mouseX, mouseY):
            app.charMode = False
            app.menuMode = True
    
    if app.gameMode:
        if util.backButton(mouseX, mouseY):
            app.popup = True
            app.paused = True

        if app.paused:
            if not app.gameOver and util.unpauseButton(mouseX, mouseY):
                app.popup = False
                app.paused = False
            elif util.restartButton(mouseX, mouseY):
                restart(app)

def onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY

    #button color edits
    if app.menuMode:
        if util.playButton(mouseX, mouseY):
            app.playColor = 'gainsboro'
        else:
            app.playColor = 'gray'
        
        if util.charButton(mouseX, mouseY):
            app.charColor = 'gainsboro'
        else:
            app.charColor = 'gray'
        
        if util.aboutButton(mouseX, mouseY):
            app.aboutColor = 'gainsboro'
        else:
            app.aboutColor = 'gray'
    
    if app.charMode:
        app.currRow, app.currCol = util.getCurrentCell(app)

def restart(app):

    #menu starters
    app.background = gradient('gray', 'gainsboro', start = 'top')
    app.width = 1600
    app.height = 1050

    #modes
    app.gameMode = False
    app.charMode = False
    app.menuMode = True
    app.aboutMode = False
    app.gameOver = False
    app.popUp = False
    app.state = 'details'

    #button colors
    app.playColor = 'gray'
    app.charColor = 'gray'
    app.aboutColor = 'gray'

    #world lists
    app.world = ['grass', 'road', 'road', 'grass', 'grass', 
                 'road', 'grass', 'grass', 'road', 'grass', 'road']
    app.seen = []

    #terrain generation
    app.cars = [[] for i in range(len(app.world))]
    app.greenery = [[] for i in range(len(app.world))]
    app.logs = [[] for i in range(len(app.world))]
    app.collectibles = [[] for i in range(len(app.world))]
    app.prevTerrain = None

    #timer events
    app.stepsPerSecond = 30
    app.counter = 0
    
    #player animations
    app.player = Player(0, 0, 50, app.stepsPerSecond//5, 75, 50, 25)
    app.playerYIndex = len(app.world)//2
    app.playerXIndex = 7
    startX, startY = app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex)
    app.player = Player(startX, startY, 50, app.stepsPerSecond//5, 75, 50, 25)
    app.charPlayer = Player(app.width*4/5, app.height*0.7, 20, 
                            app.stepsPerSecond//5, 450, 300, 150)
    
    #game counts
    app.hopCount = 0
    app.totalCoins += app.coinCount
    app.coinCount = 0
    app.backCount = 5 
    app.powerupCount = 0
    app.powerdownCount = 0 

    #powerup/powerdown functions
    #starpower
    app.powerup = False
    app.powerupColors = ['lightCoral', 'orange', 'lemonChiffon', 
                         'paleGreen', 'lightCyan', 'mediumPurple']
    app.colorIndex = 0
    app.poweruptimer = 150
    app.paused = False
    app.popup = False

    #skiplanes
    app.skip = False
    app.drawSkip = False
    app.skipLabelTimer = 25
    app.skiptimer = 150

    #boosted/dragged
    app.boost = False
    app.drag = False

    #ink
    app.ink = False
    app.balls = []

    #board variables
    app.currRow = None
    app.currCol = None

    #sounds (cited in on app start)
    app.hopSound = Sound('sounds/hop.mp3')
    app.whoosh = Sound('sounds/car.mp3')
    app.powerUpSound = Sound('sounds/skip.mp3')
    app.splash = Sound('sounds/splash.mp3')
    app.starSound = Sound('sounds/starpower.mp3')
    app.playStar = True
    app.fail = Sound('sounds/fail.mp3')
    app.inkSound = Sound('sounds/splat.mp3')


#helper functions
def carCollision(app, obj):
    for index in range(len(app.cars)):
        cars = app.cars[index]
        for xindex in range(len(cars)):
            car = cars[xindex]
            if util.collision(obj, car):
                return True
    return False

def powerUp(app): 
    choices = ['starpower', 'skiplanes', 'rocketboost']
    choice = py_random.choice(choices)
    if choice == 'starpower':
        app.starSound.play()
        app.powerup = True
        app.poweruptimer = 300
    elif choice == 'rocketboost':
        app.powerUpSound.play()
        app.boost = True
    elif choice == 'skiplanes':
        app.powerUpSound.play()
        app.drawSkip = True
        app.skipLabelTimer = 25
        app.skiptimer = 150

def powerDown(app):
    choices = ['drag', 'ink']
    choice = py_random.choice(choices)

    if choice == 'drag':
        app.fail.play()
        app.drag = True
        app.dragTimer = 150
    elif choice == 'ink':
        app.inkSound.play()
        app.ink = True
        app.inktimer = 200
        getInk(app)

def popCols(app):
     for tier in range(len(app.collectibles)):
        colList = app.collectibles[tier]
        for xindex in range(len(colList)):
            col = colList[xindex]
            if isinstance(col, Collectible):
                x1 = getXIndex(app, col.x)
                x2 = getXIndex(app, app.player.x)
                y = app.height - (tier + 2) * (app.height // len(app.world)) + 50
                if x1 == x2 and int(abs(app.player.y - y)) < 25:
                    if type(col) == Coin:
                        app.coinCount += 1
                    elif type(col) == Powerup:
                        powerUp(app)
                        app.powerupCount += 1
                    elif type(col) == Powerdown: 
                        powerDown(app)
                        app.powerdownCount += 1
                    col.collected = True  
                    app.collectibles[tier][xindex] = 'no'  

#movement checkers
def backwardLegal(app):
    tier = 5
    plantList = app.greenery[tier - 2]    
    for xindex in range(len(plantList)):
        plant = plantList[xindex]
        if plant =='bush' or plant == 'tree':
            x = world.snapTerrain(app, xindex)
            if abs(app.player.x - x) == 0:
                return False
    if app.backCount == 0:
        app.gameOver = True
    return app.backCount > 0

def inWater(app, key):
    if key in ['up','w']:
        tier = 5
        if app.skip:
            tier = tier+1
        if app.world[tier] == 'lake':
            logList = app.logs[tier]
            index = app.playerXIndex 
            if index < len(logList):
                log = logList[index]
                if log == 'no' and logList[index + 1] == 'no' and logList[index - 1] == 'no':
                    app.splash.play()
                    return True  
    elif key in ['right', 'd']:
        tier = 3
        if app.world[tier + 1] == 'lake':
            logList = app.logs[tier + 1]
            index = app.playerXIndex + 1
            if index < len(logList):
                log = logList[index]
                if log == 'no':
                    if index + 1 < len(logList) and logList[index + 1] == 'log':
                        return False
                    elif logList[index - 1] == 'no':
                        app.splash.play()
                        return True
                
    elif key in ['left', 'a']:
        tier = 3
        if app.world[tier + 1] == 'lake':
            logList = app.logs[tier + 1]
            index = app.playerXIndex 
            if index < len(logList):
                log = logList[index]
                if log == 'no':
                    if logList[index - 2] == 'log':
                        return False
                    elif logList[index - 1] == 'no':
                        app.splash.play()
                        return True
    return False

def forwardLegal(app):
    tier = 5
    plantList = app.greenery[tier]    
    for xindex in range(len(plantList)):
        plant = plantList[xindex]
        if plant =='bush' or plant == 'tree':
            x = world.snapTerrain(app, xindex)
            if abs(app.player.x - x) == 0:
                return False
    return True

def doubleForwardLegal(app):
    tier = 5
    plantList = app.greenery[tier + 1]
    for xindex in range(len(plantList)):
        plant = plantList[xindex]
        if plant =='bush' or plant == 'tree':
            x = world.snapTerrain(app, xindex)
            if abs(app.player.x - x) == 0:
                return False
    return True       

def rightLegal(app):
    tier = 4
    plantList = app.greenery[tier]
    for xindex in range(len(plantList)):
        plant = plantList[xindex]
        newX, newY = app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex + 1)
        if plant =='bush' or plant == 'tree':
            x = world.snapTerrain(app, xindex)
            if abs(newX - x) == 0:
                return False
    return True

def leftLegal(app):
    tier = 4
    plantList = app.greenery[tier]
    for xindex in range(len(plantList)):
        plant = plantList[xindex]
        newX, newY = app.player.snapTerrain(app, app.playerYIndex, app.playerXIndex - 1)
        if plant =='bush' or plant == 'tree':
            x = world.snapTerrain(app, xindex)
            if abs(newX - x) == 0:
                return False
    return True

#world updates
def updateWorld(app):
    maxBackward = 5
    if len(app.seen) == maxBackward:
        app.seen.pop(0)

    prevTier = {'world': app.world[0], 
                'cols': app.collectibles[0],
                'plants': app.greenery[0],
                'logs': app.logs[0],
                'cars': app.cars[0]
                }
    app.seen.append(prevTier)

    if app.prevTerrain == 'lake':
        terrain = py_random.choice(['grass', 'road'])
    else:
        terrain = py_random.choice(['grass', 'road', 'lake'])


    if terrain == 'road':
        cars = []
        totalCars = py_random.randint(2, 4)
        direction = py_random.choice(['left', 'right'])
        if direction == 'right':
            for i in range(totalCars):
                offset = 400
                colors = ['oliveDrab', 'cornflowerBlue', 'darkMagenta', 'deepPink']
                width = py_random.randint(50, 130)
                height = py_random.randint(50, 70)
                speed = 15
                x = -(i*offset)
                cars.append(Car(x, width, height, py_random.choice(colors), 
                                speed, len(app.world) - 1, direction))
        else:
            for i in range(totalCars):
                offset = 400
                colors = ['oliveDrab', 'cornflowerBlue', 'darkMagenta', 'deepPink']
                width = py_random.randint(50, 130)
                height = py_random.randint(20, 70)
                speed = 15
                x = app.width + (i*offset)
                cars.append(Car(x, width, height, py_random.choice(colors), 
                                speed, len(app.world) - 1, direction))
        app.cars.append(cars)
    else:
        app.cars.append([])
    
    collectibles = ['no'] * 15
    if terrain == 'grass':
        app.greenery.append(getPlants(app))
        for index in range(15):
            if app.greenery[-1][index] == 'no':
                collectibles[index] = getCollectible(app, index, len(app.world) - 1)
    else:
        app.greenery.append(['no'] * 15)

    
    if terrain == 'lake':
        app.logs.append(getLogs(app))
        for index in range(15):
            if app.logs[-1][index] == 'log':
                collectibles[index] = getCollectible(app, index, len(app.world) - 1) 
    else:
        app.logs.append(['no']*15)

    app.collectibles.append(collectibles)
    app.world.pop(0)
    app.collectibles.pop(0)
    app.greenery.pop(0)
    app.logs.pop(0)
    app.cars.pop(0)
    
    
    app.world.append(terrain)
    app.prevTerrain = terrain

def reverseWorld(app):
    if len(app.seen) > 0:
        lastTier = app.seen[-1]
        app.world.insert(0, lastTier['world'])
        app.collectibles.insert(0, lastTier['cols'])
        app.greenery.insert(0, lastTier['plants'])
        app.logs.insert(0, lastTier['logs'])
        app.cars.insert(0, lastTier['cars'])

        app.world.pop()
        app.collectibles.pop()
        app.greenery.pop()
        app.logs.pop()
        app.cars.pop()
        app.seen.pop()
    else:
        app.gameOver = True

#getters
def getLogs(app):
    logs = ['no' for xindex in range(15)]
    totalLogs = py_random.randint(1, 3)
    if totalLogs == 1:
        j = py_random.randint(5, 10)
        logs[j] = 'log'
        if j + 10 < 12:
            logs[j + 10] = 'log'
        else:
            logs[py_random.choice([3,7,10])] = 'log'
    for _ in range(totalLogs):
        j = py_random.randint(1,7)
        if j*3 < 15:
            logs[j*3] = 'log'
        else:
            logs[py_random.choice([3,7,10])] = 'log'
    return logs

def getPlants(app):
    greenery = ['no' for xindex in range(15)]
    greenCount = py_random.randint(1, 4)
    green = ['tree', 'bush']
    
    for _ in range(greenCount):
        j = py_random.randint(0, 15)
        if j < len(app.greenery):
            greenery[j] = py_random.choice(green)
    return greenery

def getCollectible(app, xindex, tier):
    chances = ['0']*9 + ['1']
    choice = py_random.choice(chances)
    types = ['coin']*12 + ['up', 'down']
    obj = 'no'
    if choice == '1':
        colType = py_random.choice(types)
        if colType == 'coin':
            obj = Coin(app, xindex, tier)
        elif colType == 'up':
            obj = Powerup(app, xindex, tier)
        elif colType == 'down':
            obj = Powerdown(app, xindex, tier)
    return obj

def getInk(app):
    app.balls = []

    inkCount = py_random.randint(10, 20)

    for i in range(inkCount):
        radius = py_random.randint(50, 200)
        startX = py_random.randint(radius, app.width - radius)
        startY = py_random.randint(radius, app.height - radius)
        dX = py_random.randint(10, 20)
        dY = py_random.randint(10, 20)

        #chatGPT: storing each ball as a dictionary
        ball = {
            'x': startX,
            'y': startY,
            'dx': dX,
            'dy': dY,
            'r': radius
        }
        
        app.balls.append(ball)
        
def getXIndex(app, x):
    tierWidth = app.width//15  
    xindex = int(x//tierWidth)
    return xindex

def getTier(app, y): 
    tierHeight = app.height // len(app.world) 
    yindex = int((app.height - y) // tierHeight)

    return yindex

def main():
    runApp()
    

main()