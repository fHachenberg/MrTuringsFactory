'''
Created on 14.03.2012

@author: omni
'''
import pygame
import random

screen = None
zplanes = []
zplanes_next = []
level = [10, 10, 10]

blockimage = None
blockwidth = 47
blockheight = 23
blockdepth = 58

def main():
    global screen
    global blockimage
    
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    
    blockimage = pygame.image.load("../../data/graphics/block02.png")
    
    initLevel()
    
    for x in range(level[0]):
        for y in range(level[1]):
            addObject((x,y,0))
    
    for i in range(30):
        x,y,z = random.randint(0,level[0]-1), random.randint(0,level[1]-1), random.randint(0,level[2]-1)
        if not hasObject((x,y,z)):
            addObject((x,y,z))                
    
    for i in range(20):
        updateLevel()
        drawLevel()
    
def initLevel():
    global planes
    global level
    
    for i in range(max(level[0], level[1], level[2])):        
        zplanes.append([])
        
def hasObject(position):
    x, y, z = position
    return (x,y) in zplanes[z]

def addObject(position):
    global level
    global objpos
    global zplanes
    nx, ny, nz = position
    
    if nx < 0 or nx >= level[0]:
        raise BlockError("invalid x coordinate " + str(nx))
    if ny < 0 or ny >= level[1]:
        raise BlockError("invalid y coordinate " + str(ny))
    if nz < 0 or nz >= level[2]:
        raise BlockError("invalid z coordinate " + str(nz))
        
    collision = filter(lambda (x,y): x == nx and y == ny, zplanes[nz])
    if len(collision) != 0:
        raise BlockError("object can only be inserted at empty position (" + str(nx) + ", " + str(ny) + ", " + str(nz) + ")")
        
    zplanes[nz].append((nx, ny))
    zplanes[nz].sort(key= lambda (x,y): x-y)
    
def removeObject(position):
    if not hasObject(position):
        raise BlockError("No object at position (" + str(position[0]) + ", " + str(position[1]) + ", " + str(position[2]) + ")")
    zplanes[position[2]].remove((position[0], position[1]))
    
class BlockError(Exception):
    def __init__(self, str):
        Exception.__init__(self, str)
    
def moveObject(position, direction):
    #if not hasObject(position):
    #    raise BlockError("position (" + str(position[0]) + ", " + str(position[1]) + ", " + str(position[2]) + ") is vacant")    
    newposition = (position[0]+direction[0], position[1]+direction[1], position[2]+direction[2])
    #if newposition[0] < 0 or newposition[0] >= level[0]:
    #    raise BlockError("invalid x coordinate " + str(newposition[0]))
    #if newposition[1] < 0 or newposition[1] >= level[1]:
    #    raise BlockError("invalid y coordinate " + str(newposition[1]))
    if newposition[2] < 0 or newposition[2] >= level[2]:
        raise BlockError("invalid z coordinate " + str(newposition[2]))
    if hasObject(newposition):        
        raise BlockError("position (" + str(newposition[0]) + ", " + str(newposition[1]) + ", " + str(newposition[2]) + ") not vacant")
    try:
        removeObject(position)
        addObject(newposition)
    except BlockError:
        pass
    
def updateLevel():
    for z, zplane in enumerate(zplanes):
        for x,y in zplane:
            try:
                moveObject((x,y,z), (0,0,-1))
            except BlockError:
                pass
    
def drawLevel():
    screen.fill((0,0,0))
    
    global zplanes
    global blochwidth, blockheight, blockdepth
    for z, zplane in enumerate(zplanes):
        for x, y in zplane:             
            xpos = 0 + x*blockwidth + y*blockwidth
            ypos = 500 + x*blockheight - y*blockheight - z * blockdepth
            screen.blit(blockimage, (xpos,ypos))
    #for x,y
    pygame.display.flip()

if __name__ == '__main__':
    main()
    