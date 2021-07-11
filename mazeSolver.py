import pygame
import random
#inspired by https://www.youtube.com/watch?v=Xthh4SEMA2o&ab_channel=DavisMT

#define width and height of window and initialize window
WINDOW_WIDTH, WINDOW_HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#sets caption of window
pygame.display.set_caption("Maze")

#define cell width and height, calculate number of rows/columns
CELL_WIDTH, CELL_HEIGHT = 25,25
MATRIX_WIDTH = int(WINDOW_WIDTH/CELL_WIDTH)		#number of rows
MATRIX_HEIGHT = int(WINDOW_HEIGHT/CELL_HEIGHT)	#number of columns

#define directional movements
MOVE_UP		= 0
MOVE_LEFT	= 1
MOVE_RIGHT	= 2
MOVE_DOWN	= 3

FPS = 30

#Colors as (R,G,B)
BACKGROUND = (30,30,30)
CELL_COLOR = (50,50,50)
BLACK = (0,0,0)
CYAN = (100,255,255)
BLUE = (100,255,100)
WHITE = (255,255,255)
RED = (255,100,100)

#global variables
position_x, position_y = 0, 0
next_x, next_y = 0, 0
run = True
generateMaze = False
validMove = False

#arrays used to generate maze
visited = [[0 for y in range(MATRIX_HEIGHT)] for x in range(MATRIX_WIDTH)]	#for all visited cells
stack = [[0,0]]																#visit history
move = [position_x,position_y] 												#move
possibleMove = [[[]for y in range(MATRIX_HEIGHT)] for x in range(MATRIX_WIDTH)]

#arrays used to solve maze
solverMove = [position_x,position_y]
solverPath = [[0,0]]
splitLocationList = []


##code below for generating maze

#draw initial grid
def drawGrid():
	WINDOW.fill(BACKGROUND)#color background

	#check window size
	if (WINDOW_WIDTH%CELL_WIDTH != 0) or (WINDOW_HEIGHT%CELL_HEIGHT != 0):
		print("Window width/height incompatible with cell width/height. Terminating program")
		pygame.quit()

	#create grid
	for x in range (0, WINDOW_WIDTH, CELL_WIDTH):
		for y in range(0, WINDOW_HEIGHT, CELL_HEIGHT):
			rect = pygame.Rect(x,y,CELL_WIDTH, CELL_HEIGHT)	#create new rectangle object
			pygame.draw.rect(WINDOW, CYAN, rect, 1)			#draw border around object

	pygame.display.update()	#updates window with grid

#visit each cell in grid and remove wall to make paths
def visitGrid():
	global move, visited

	#get x and y positions
	x = move[0]
	y = move[1]

	#convert cell number to pixel
	xgrid = x * CELL_WIDTH
	ygrid = y * CELL_HEIGHT
	visited[x][y] = True	#flag visited

	removeWall()

#removes walls between visited cells, creates visual representation of path
def removeWall():
	if len(stack) > 1:	#while stack is not empty
		recentStack = stack[-1]		#get most recent
		previousStack = stack[-2]	#get position before recent

		#get x and y values
		recent_x = recentStack[0]
		recent_y = recentStack[1]
		prev_x = previousStack[0]
		prev_y = previousStack[1]

		#define wall width/height and draw new rectangle to "erase" border
		wallWidth = ((recent_x + prev_x)/2) * CELL_WIDTH
		wallHeight = ((recent_y + prev_y)/2) * CELL_HEIGHT
		wall = pygame.Rect(wallWidth+1,wallHeight+1,CELL_WIDTH-2,CELL_HEIGHT-2)#draw over wall
		pygame.draw.rect(WINDOW,BACKGROUND,wall)

#places circles at 0,0 and matrix_width,matrix_height
def placeGoal():
	#starting point
	startCircleXY = (CELL_WIDTH/2,CELL_HEIGHT/2)
	circle_radius = int(CELL_WIDTH/3)
	pygame.draw.circle(WINDOW,WHITE,startCircleXY,circle_radius,0)

	#endpoint
	goalCircleXY = (WINDOW_WIDTH - (CELL_WIDTH/2), WINDOW_HEIGHT - (CELL_HEIGHT/2))
	pygame.draw.circle(WINDOW,WHITE,goalCircleXY,circle_radius,0)
	pygame.display.update()

#checks neighbors
def neighbors():
	global move, stack, visited, validMove
	global next_x, next_y

	#get current position
	x = move[0]
	y = move[1]

	#initialize next position and set flags
	next_x = 0
	next_y = 0
	validMove = True
	upNeighbor, downNeighbor, leftNeighbor, rightNeighbor = False, False, False, False
	
	while validMove == True:

		#no valid neighbors available to visit
		if upNeighbor and downNeighbor and leftNeighbor and rightNeighbor:
			backtrack()	#backtrack to previous
			break

		#determine random neighbor according to directions from 0 to 3
		randNeighbor = random.randint(0,3)

		if randNeighbor == MOVE_UP:
			#check if neighbor is valid
			if y > 0:
				if visited[x][y-1] != True: #if not already visited
					next_x = x 				#set coordinates
					next_y = y - 1
					possibleMove[x][y].append(MOVE_UP) #set position as valid movement from initial position
					validMove = False
				else:
					upNeighbor = True	#set as can't move here
			else:
				upNeighbor = True		#set as can't move here

		elif randNeighbor == MOVE_LEFT:#1
			if x > 0:
				if visited[x-1][y] != True: #check if not already visited
					next_x = x - 1
					next_y = y
					possibleMove[x][y].append(MOVE_LEFT)
					validMove = False
				else:
					leftNeighbor = True	#invalid movement
			else:
				leftNeighbor = True		#invalid movement

		elif randNeighbor == MOVE_RIGHT:#2
			if x < MATRIX_WIDTH - 1:
				if visited[x+1][y] != True:
					next_x = x + 1
					next_y = y
					possibleMove[x][y].append(MOVE_RIGHT)
					validMove = False
				else:
					rightNeighbor = True
			else:
				rightNeighbor = True

		elif randNeighbor == MOVE_DOWN:#3
			if y < MATRIX_HEIGHT - 1:
				if visited[x][y+1] != True:
					next_x = x
					next_y = y + 1
					possibleMove[x][y].append(MOVE_DOWN)
					validMove = False
				else:
					downNeighbor = True
			else:
				downNeighbor = True

	#set coordinate of next move
	move = [next_x,next_y]

	#add to stack
	if stack[-1] != move:
		stack.append(move)

#for no neighbors, backtracks through stack
def backtrack():
	global stack, generateMaze
	global next_x, next_y

	if len(stack) > 1:#move back
		stack.pop()					#pop most recent
		lastLocation = stack[-1]	#get next recent
		next_x = lastLocation[0]	#get coordinates
		next_y = lastLocation[1]
	else:
		generateMaze = False		#if back to origin
		print("finished maze generation")
##end of code required to generate maze


##code below for solving maze

#draw a green circle wherever visited
def drawStep(x,y):
	#calculate coordinates and draw point
	circleXY = ((x*CELL_WIDTH) + (CELL_WIDTH/2), (y*CELL_HEIGHT) + (CELL_HEIGHT/2))
	circle_radius = int(CELL_WIDTH/3)
	pygame.draw.circle(WINDOW,BLUE,circleXY,circle_radius,0)
	pygame.display.update()

#draw path from start to end with red circles
def drawPath():
	global solverPath

	for i in range(len(solverPath)):
		#get coordinates
		x = solverPath[i][0]
		y = solverPath[i][1]

		#create circle object and draw
		circleXY = ((x*CELL_WIDTH) + (CELL_WIDTH/2), (y*CELL_HEIGHT) + (CELL_HEIGHT/2))
		circle_radius = int(CELL_WIDTH/3)
		pygame.draw.circle(WINDOW,RED,circleXY,circle_radius,0)

	#udpate display
	pygame.display.update()	

#solve maze
def solveMaze():
	global possibleMove, solverMove, solverPath, mazeSolved, splitLocationList

	#define position being visited
	solverx = solverMove[0]
	solvery = solverMove[1]

	#set as previous location
	previousLocation = solverMove

	#determine number of possible directions for location
	numberDirections = len(possibleMove[solverx][solvery])

	#if cannot move
	if numberDirections == 0:
		moveDirection = -1					#set to invalid direction
		lastSplit = splitLocationList[-1]	#get last branch in path
		solverx = lastSplit[0]				#set coordinates to branch
		solvery = lastSplit[1]
		splitLocationList.pop()				#pop branch so doesn't keep visiting

		while solverPath[-1] != lastSplit:	#remove all coordinates in path after branch
			solverPath.pop()
	
	#if only one path, set movement direction
	elif numberDirections == 1:
		moveDirection = possibleMove[solverx][solvery][0]
	
	#if multiple paths
	else:
		randDirection = random.randint(0,numberDirections-1)	#generate random direction
		splitLocationList.append([solverx,solvery])				#this location is a branch so append
		moveDirection = possibleMove[solverx][solvery][randDirection]
		possibleMove[solverx][solvery].remove(moveDirection)#so doesn't go into same path
	
	#update coordinates according to movement direction
	if moveDirection == MOVE_UP:
		solvery = solvery - 1
	elif moveDirection == MOVE_LEFT:
		solverx = solverx - 1
	elif moveDirection == MOVE_RIGHT:
		solverx = solverx + 1
	elif moveDirection == MOVE_DOWN:
		solvery = solvery + 1	

	#update position, add to path solution and draw circle
	solverMove = [solverx,solvery]
	solverPath.append(solverMove)
	drawStep(solverx,solvery)

	#if reached bottom right corner, finished solving maze
	if solverMove == [MATRIX_WIDTH-1, MATRIX_HEIGHT-1]:
		mazeSolved = True
		print("solved maze")
		print("Printing maze solution path:")
		print(solverPath)
#end of code for solving maze

#main function
def main():
	global run, generateMaze, mazeSolved
	run = True
	mazeSolved = False
	clock = pygame.time.Clock()				#get clock
	drawGrid()								#draws initial grid
	
	#main loop
	while run:
		clock.tick(FPS)						#update clock by FPS
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):	#exits game
				run = False

			#generate maze if hit enter and solve
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				generateMaze = True

				#loop generates maze
				while generateMaze:	
					visitGrid()				#visit grid cell
					neighbors()				#check neighbors and move
					pygame.display.update()	#udpate window
				
				placeGoal()					#place start and end goal
				
				#loop solves maze
				while mazeSolved == False:
					solveMaze()				#solve maze
				drawPath()					#draws maze path
	pygame.quit()							#quit game

if __name__ == "__main__":
	main()










