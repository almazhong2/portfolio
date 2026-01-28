from cmu_graphics import *
import math
import random as py_random

#3D projection (~2.5D): from CMU CS Academy 3D graphics video
#https://youtu.be/ledW6-k0BLY?feature=shared 
app.x, app.y, app.z = 0.25, 2, 3

app.verticalView = -30
app.horizontalView = 0

#converting 3D points in 2D points
#mathematical formula from https://en.wikipedia.org/wiki/3D_projection
def convert2D(point, x, y, z):
    aX, aY, aZ = point
    cX, cY, cZ = x, y, z

    #angles for a the correct view
    xAngle = app.horizontalView
    yAngle = app.verticalView

    thetaX, thetaY = yAngle, xAngle
    eX, eY, eZ = (app.width//2, app.height//2, min(app.width, app.height) * 0.714) #eye position
    x, y, z = aX - cX, aY - cY, aZ - cZ #translated point

    cX = dcos(thetaX)
    cY = dcos(thetaY)

    sX = dsin(thetaX)
    sY = dsin(thetaY)

    dX = cY * x - sY * z
    dY = sX * (cY * z + sY * x) + cX * y
    dZ = cX * (cY * z + sY * x) - sX * y

    if dZ == 0 or dZ < -30:
        return [None, None]
    
    elif dZ > 0:
        return [None, None]
    
    bX = eZ/dZ * dX + eX
    bY = eZ/dZ * dY + eY

    return [bX, bY]

def drawPlane(corners, color):
    #corners is a list of 4 3D coordinates
    #convert each point in corners to a 2D point
    newCorners = []
    for point in corners:
        newPoint  = convert2D(point, app.x, app.y, app.z)
        newCorners += newPoint

    #draw a polygn with the new 2D corners
    Polygon(*newCorners, fill = color, border = 'black')
    

def drawBlock3D(length, width, height, color):
    #draw top, front, and right side (points in (x, y, z))
    if app.z > 0:
        front = [(0, 0, width),
                (length, 0, width),
                (length, height, width), 
                (0, height, width)
                ]
    else:
        front = [ (0, 0, 0),
                (length, 0, 0),
                (length, height, 0),
                (0, height, 0)
        ]
    drawPlane(front, color)


    top = [(0, height, 0),
           (length, height, 0),
           (length, height, width), 
           (0, height, width)
           ]
    drawPlane(top, color)

def drawMenu(app):
    #made via www.cooltext.com 
    drawImage('src/krossykartlogo.png', app.width//2, app.height//3, align = 'center')

#Inspired by CMU CS Academy: 6.3.6 Fancy Wheel 1
#star variables
app.starAngle = 90
app.starRadius = app.height*0.8 - 50
app.starSpeed = 5

app.starX = app.width
app.starY = app.height
app.starWidth = app.width //2
app.starHeight = app.height//2

def getRadiusEndpoint(cx, cy, r, theta):
    return (cx + r*math.cos(math.radians(theta)),
            cy - r*math.sin(math.radians(theta)))

def drawStars(app):
    x, y = getRadiusEndpoint(app.starX, app.starY, app.starRadius, app.starAngle)
    #https://m.media-amazon.com/images/I/31TuRoKarfL._AC_UF894,1000_QL80_.jpg 
    drawImage('src/star.png', x - app.starWidth // 2, y - app.starHeight//2, 
              width = app.starWidth, height = app.starHeight)

app.playLeft = app.width/3.2 + 100
app.playTop = app.height*0.5
app.playWidth = app.width//4
app.playHeight = app.height*0.1

def drawButtons(app):
    #play button
    drawRect(app.width/3.2 + 100, app.height*0.5, 
             app.width//4, app.height*0.1, 
             fill = app.playColor, border = 'black')
    drawLabel('Start', app.width/3.2 + 100 + (app.width//4) // 2, 
              app.height*0.5 + (app.height*.1)//2, size = app.height*.05, 
              font = 'arial', bold = True, fill = 'paleTurquoise', align = 'center')
    
    #char button
    drawRect(app.width/3.2 + 100, app.height*0.625, 
             app.width//4, app.height*0.1, 
             fill = app.charColor, border = 'black')
    drawLabel('Characters', app.width/3.2 + 100 + (app.width//4) // 2,
              app.height*0.625 + (app.height*.1)//2, size = app.height*.05, 
              font = 'arial', bold = True, fill = 'paleTurquoise', align = 'center')
    
    #about button
    drawRect(app.width/3.2 + 100, app.height*0.75, 
             app.width//4, app.height*0.1, 
             fill = app.aboutColor, border = 'black')
    drawLabel('About', app.width/3.2 + 100 + (app.width//4) // 2, 
              app.height*0.75 + (app.height*.1)//2, size = app.height*.05, 
              font = 'arial', bold = True, fill = 'paleTurquoise', align = 'center')


#CS academy intersection conditions (4.3.5)    
def playButton(mouseX, mouseY):
    right = app.width/3.2 + 100 + app.width//4
    bottom = app.height*0.5 + app.height*0.1
    if (app.width/3.2 + 100 <= mouseX <= right) and (app.height*0.5 <= mouseY <= bottom):
        return True
    return False

def charButton(mouseX, mouseY):
    right = app.width/3.2 + 100 + app.width//4
    bottom = app.height*0.625 + app.height*0.1
    if (app.width/3.2 + 100 <= mouseX <= right) and (app.height*0.625 <= mouseY <= bottom):
        return True
    return False

def aboutButton(mouseX, mouseY):
    right = app.width/3.2 + 100 + app.width//4
    bottom = app.height*0.75 + app.height*0.1
    if (app.width/3.2 + 100 <= mouseX <= right) and (app.height*0.75 <= mouseY <= bottom):
        return True
    return False

def backButton(mouseX, mouseY):
    right = 50 + app.width//8
    bottom = 50 + app.height//10
    if (50 <= mouseX <= right) and (50 <= mouseY <= bottom):
        return True
    return False

def restartButton(mouseX, mouseY):
    index = 5
    rectHeight = app.height*0.6

    x = app.width//2
    y = app.height//2 - rectHeight//2 + index*rectHeight//6 + 50
    
    buttonWidth = app.width //6
    buttonHeight = rectHeight//6 - 50

    left = x - buttonWidth//2
    right = x + buttonWidth//2
    top = y - buttonHeight//2
    bottom = y + buttonHeight//2

    if (left <= mouseX <= right) and (top <= mouseY <= bottom):
        return True
    return False

def unpauseButton(mouseX, mouseY):
    index = 0
    rectHeight = app.height*0.6

    x = app.width//2
    y = app.height//2 - rectHeight//2 + index*rectHeight//6 + 50
    
    buttonWidth = app.width //6
    buttonHeight = rectHeight//6 - 50

    left = x - buttonWidth//2
    right = x + buttonWidth//2
    top = y - buttonHeight//2
    bottom = y + buttonHeight//2

    if (left <= mouseX <= right) and (top <= mouseY <= bottom):
        return True
    return False

#characterselection
#All drawBoard functions from CMU CS Academy 7.3.7 Creative Task: Tetris
app.charColors = [['violet', 'dodgerBlue', 'hotPink'], 
              ['darkGray', 'darkSlateBlue', 'lime']]

hoverColors = [['plum', 'deepSkyBlue', 'lightPink'], 
               ['lightGray', 'slateBlue', 'chartreuse']]

app.cellBorderWidth = 2

def drawBoard(app):
    for row in range(2):
        for col in range(3):
            if app.currRow == row and app.currCol == col:
                color = hoverColors[row][col]
            else:
                color = app.charColors[row][col]
            drawCell(app, row, col, color)
    drawBoardBorder(app)

#draws a rectangular cell utilizing cell coordinate and size
def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill= color, border='black',
             borderWidth=app.cellBorderWidth)

#cell helper to get top-left coordinate
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.width//5 + col * cellWidth
    cellTop = app.height//3 + row * cellHeight
    return (cellLeft, cellTop)

#size of the cells
def getCellSize(app):
    cellWidth = app.width//5 / 3
    cellHeight = app.height//5 / 2
    return (cellWidth, cellHeight)

#final border for board
def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.width//5, app.height//3, 3*getCellSize(app)[0], 2*getCellSize(app)[1],
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

#gets cell mouse is hovering over
def getCurrentCell(app):
    for row in range(2):
        for col in range(3):
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)

            #if within cell
            if (cellLeft <= app.mouseX <= cellLeft + cellWidth) and (cellTop <= app.mouseY <= cellTop + cellHeight):
                return row, col
    
    return None, None

#get vertices for drawing block
def getVertices(x, y, width, height, depth):
    w, h = width//2, height//2
    
    #adjust away from center point by half of each dimension's size
    #base vertices
    bottomFrontLeft = (x - w, y + h) 
    bottomFrontRight = (x + w, y + h)
    bottomBackRight = (x + w + depth, y + h - depth)
    bottomBackLeft = (x - w + depth, y + h - depth)
    
    #top vertices
    topFrontLeft = (x - w, y - h)
    topFrontRight = (x + w, y - h)
    topBackRight = (x + w + depth, y - h - depth)
    topBackLeft = (x - w + depth, y - h - depth)

    vertex = [bottomFrontLeft, bottomFrontRight,
            bottomBackRight, bottomBackLeft,
            topFrontLeft, topFrontRight,
            topBackRight, topBackLeft
            ]
    
    return [bottomFrontLeft, bottomFrontRight,
            bottomBackRight, bottomBackLeft,
            topFrontLeft, topFrontRight,
            topBackRight, topBackLeft
            ]

#similar to 2d: getting a left, top, right, bottom for a rectangle (boundaries of a block) 
def getBoundaries(vertices):
    left, right, top, bottom = 0, 0, 0, 0
    
    xvals = []
    yvals = []
    for vertex in vertices:
        x = vertex[0]
        y = vertex[1]
        xvals.append(x)
        yvals.append(y)

    left = min(xvals)
    right = max(xvals)
    top = min(yvals)
    bottom = max(yvals)

    return left, right, top, bottom

#draw 3 polygons using depth perception
def drawBlock(x, y, width, height, depth, color):
    vertices = getVertices(x, y, width, height, depth)

    #dictionary of 3 sides visible, and the index of vertex to access from vertices
    faceVertices = {'front': [0, 1, 5, 4],
                    'top': [4, 5, 6, 7],
                    'side': [1, 2, 6, 5]
                    }
    
    for side in faceVertices:
        indexList = faceVertices[side]
        points = [] 
        for index in indexList:
            vx, vy = vertices[index]
            points.extend([vx, vy]) #in format for polygon
        drawPolygon(*points, fill = color)

def drawBorderBlock(x, y, width, height, depth, color):
    vertices = getVertices(x, y, width, height, depth)

    #dictionary of 3 sides visible, and the index of vertex to access from vertices
    faceVertices = {'front': [0, 1, 5, 4],
                    'top': [4, 5, 6, 7],
                    'side': [1, 2, 6, 5]
                    }
    
    for side in faceVertices:
        indexList = faceVertices[side]
        points = [] 
        for index in indexList:
            vx, vy = vertices[index]
            points.extend([vx, vy]) #in format for polygon
        drawPolygon(*points, fill = color, border = 'black')

def popup(app):
    rectHeight = app.height*0.6
    rectWidth = app.width//3
    drawRect(app.width//2, app.height//2, app.width//3, rectHeight, 
             fill = 'lightSkyBlue', border = 'black', borderWidth = 10, align = 'center')
    
    if app.gameMode:
        labels = [f'{app.state}', f'score: {app.hopCount}', f'coins collected: {app.coinCount}', 
              f'powerups: {app.powerupCount}', f'powerdowns: {app.powerdownCount}',
              f'highscore: {app.highScore}', 'restart']
    elif app.aboutMode:
        labels = [f'{app.state}', f'use arrows to move', f'coins collected: {app.totalCoins}', 
              f'blue powerups', f'red powerdowns',
              f'highscore: {app.highScore}', 'exit']

    for index in range(len(labels)):
        label = labels[index]
        x, y = app.width//2, app.height//2 - rectHeight//2 + index*rectHeight//(len(labels)) + 50
        drawRect(x, y, app.width//6, rectHeight//(len(labels)) -50, fill = 'white', 
                 borderWidth = 3, border = 'black', align = 'center')
        drawLabel(label, x, y, size = 30, font = 'orbitron',
                  bold = True, fill = 'black',
                  borderWidth = 2, align = 'center')

#check if 2 objects collide
def collision(obj1, obj2):
    left1, right1, top1, bottom1 = getBoundaries(getVertices(obj1.x, obj1.y, obj1.width, obj1.height, obj1.depth))
    left2, right2, top2, bottom2 = getBoundaries(getVertices(obj2.x, obj2.y, obj2.width, obj2.height, obj2.depth))
    
    #CMU CS Academy 4.3.5 rectangle-rectangle intersection (with some leeway for moving objects)
    c1 = right2 - 5 > left1 and right1 - 5 > left2 #x intersect
    c2 = bottom2 - 5 > top1 and bottom1 - 5 > top2 #y intersect


    return c1 and c2


