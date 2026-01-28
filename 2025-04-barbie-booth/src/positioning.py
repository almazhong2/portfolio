import pygame

# input the screen, and object size, and will return (left coord, top coord)
def centerScreen(screen, width, height):
    left = screen.get_width()/2 - width/2
    top = screen.get_height()/2 - height/2
    return (left, top)

def centerWidth(left_coord, width, obj_width):
    return left_coord + width/2 - obj_width/2

def centerHeight(top_coord, height, obj_height):
    return top_coord + height/2 - obj_height/2