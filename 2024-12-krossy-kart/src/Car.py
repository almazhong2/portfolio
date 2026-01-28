from cmu_graphics import *
import random as py_random

class Car: #in 2D for now
    def __init__(self, x, width, height, color, speed, index, direction):
        self.x = x
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed 
        self.index = index
        self.depth = 25
        self.direction = direction
        #self.y = app.height - (tier + 1) * (app.height // len(app.world))
    
    def move(self):
        if self.direction == 'left':
            self.x -= self.speed
        else:
            self.x += self.speed
        
    
    def __repr__(self):
        return 'car'
    