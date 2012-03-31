'''
Created on 14.03.2012

@author: omni
'''
import pygame
import random
import time

import collision

screen = None
zplanes = []
zplanes_next = []
level = (10, 10, 10)

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
    
    #for x in range(level[0]):
    #    for y in range(level[1]):
    #        addObject((x,y,0))
    
    for i in range(30):
        x,y,z = random.randint(0,level[0]-1), random.randint(0,level[1]-1), random.randint(0,level[2]-1)
        if not hasObject((x,y,z)):
            addObject((x,y,z))                
    
    for i in range(200):
		updateLevel()
		drawLevel()
		time.sleep(2)
    
def initLevel():
    global planes
    global level
    
    for i in range(max(level[0], level[1], level[2])):        
        zplanes.append([])
        
def hasObject(position):
    return collision.hasBlock(position) or collision.hasStaticBlock(position)

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
		
	if (nx,ny) in zplanes[nz]:
		raise BlockError("object can only be inserted at empty position (" + str(nx) + ", " + str(ny) + ", " + str(nz) + ")")
		
	zplanes[nz].append((nx, ny))
	zplanes[nz].sort(key= lambda (x,y): x-y)

	collision.blocks[position] = True
    
def removeObject(position):
	if not hasObject(position):
		raise BlockError("No object at position (" + str(position[0]) + ", " + str(position[1]) + ", " + str(position[2]) + ")")
	zplanes[position[2]].remove((position[0], position[1]))

	collision.blocks.pop(position)
    
class BlockError(Exception):
    def __init__(self, str):
        Exception.__init__(self, str)
    
def updateLevel():
	for position in collision.blocks.keys():
		collision.fallBlock(position)
		collision.carryBlock(position)
	for position, direction in collision.pushed.items():
		try:
			removeObject(position)
			addObject(collision.add(position, direction))
		except BlockError:
			pass
	collision.getfilled.clear()
	collision.pushed.clear()

	x,y,z = random.randint(0,level[0]-1), random.randint(0,level[1]-1), random.randint(0,level[2]-1)	
	collision.pushBlock((x,y,z), (0,0,1))
    
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
	#import cProfile
	#cProfile.run('main()')
    main()
    
