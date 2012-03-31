#encoding: utf-8

def under(position):
	return (position[0], position[1], position[2]-1)

def delta(old, new):
	return (new[0]-old[0], new[1]-old[1], new[2]-old[2])

def add(position, delta):
	return (position[0]+delta[0], position[1]+delta[1], position[2]+delta[2])
		
pushed = {}
statics = {}
getfilled = {}
blocks = {}

xlimit = 10
ylimit = 10
zlimit = 10

def isPushed(position, direction=None):
	if not position in pushed.keys():
		return False
	if direction == None:
		return True
	else:
		return pushed[position] == direction
		
def hasStaticBlock(position):
	if position[0] < 0 or position[0] > xlimit-1:
		return True
	if position[1] < 0 or position[1] > ylimit-1:
		return True
	if position[2] < 0 or position[2] > zlimit-1:
		return True
	return position in statics.keys()

def getsFilled(position):
	return position in getfilled.keys()

def hasBlock(position):
	if position[0] < 0 or position[0] > xlimit-1:
		return False
	if position[1] < 0 or position[1] > ylimit-1:
		return False
	if position[2] < 0 or position[2] > zlimit-1:
		return False
	return position in blocks.keys()

def pushBlock(position, direction):
	if not hasBlock(position):
		print "has no block"
		return False
	if hasStaticBlock(position):
		print "is static block"
		return False
	if isPushed(position):
		print "is pushed already"
		return False
	if not hasBlock(add(position, direction)):
		if getsFilled(add(position, direction)):
			print "target block gets filled already"
			return False	
	else:
		if not pushBlock(add(position, direction), direction):
			print "target block is not pushed in the same direction"
			return False
	pushed[position] = direction
	getfilled[add(position, direction)] = position
	return True

def fallBlock(position):
	if not hasBlock(position):
		return False
	if hasStaticBlock(under(position)):
		return False
	if isPushed(position):
		if isPushed((0,0,-1)):
			return True
		else:
			return False
	if getsFilled(position):
		return False
	else:
		if hasBlock(add(position, (0,0,-1))):
			if not fallBlock(under(position)):
				return False
		pushed[position] = (0,0,-1)
		getfilled[add(position, (0,0,-1))] = position
		return True
	
def carryBlock(position):
	if not hasBlock(position):
		return False
	if not isPushed(under(position)):
		print "block under (", under(position), ") does not move"
		return False
	if isPushed(under(position), (0,0,1)) or isPushed(under(position), (0,0,-1)):
		#block wird hoch- oder runtergeschoben
		print "block under is lifted or lowered"
		return False
	direction = pushed[under(position)]
	if getsFilled(add(position, direction)):
		#zielblock wird schon gefüllt
		print "target block (", add(position, direction), ") gets filled already by (", getfilled[add(position, direction)], ")"
		return False
	if isPushed(add(position, direction)):
		if not isPushed(add(position, direction), direction):
			#zielblock wird verschoben aber nicht in gleicher richtung
			print "target block gets pushed in another direction"
			return False
	else:
		#zielblock bewegt sich nicht
		if hasBlock(add(position, direction)):
			#zielblock ist gefüllt
			print "target block (", add(position, direction), ") is blocked"
			return False
		if hasStaticBlock(add(position, direction)):
			#zielblock ist statischer block
			print "target block (", add(position, direction), ") is static block"
			return False
	pushed[position] = direction
	getfilled[add(position, direction)] = position
	carryBlock(add(position, (0,0,1)))
	return True

def applylists():
	for position, direction in pushed.items():
		blocks.pop(position)
		blocks[add(position, direction)] = True
	getfilled.clear()
	pushed.clear()

def reset(a_xlimit, a_ylimit, a_zlimit):
	global xlimit
	global ylimit
	global zlimit
	getfilled.clear()
	pushed.clear()
	statics.clear()
	blocks.clear()
	xlimit = a_xlimit
	ylimit = a_ylimit
	zlimit = a_zlimit

def addBox(position):
	'''adds a dynamic box to the game'''
	blocks[position] = True

def step(remove, add):
	'''One simulation step'''
	for position in blocks:
		fallBlock(position)
		carryBlock(position)

#statics = {(1,0,2):True}
#blocks = {(0,0,0):True, (0,0,1):True, (0,0,2):True}
#pushBlock((0,0,0), (1,0,0))
#for pos in blocks:
#	fallBlock(pos)
#	carryBlock(pos)
#print "blocks:", blocks, "gefilled:", getfilled, "pushed:", pushed, "statics:", statics
#applylists()
#pushBlock((1,0,0), (1,0,0))
#for pos in blocks:
#	fallBlock(pos)
#	carryBlock(pos)
#print "blocks:", blocks, "gefilled:", getfilled, "pushed:", pushed, "statics:", statics
#applylists()

