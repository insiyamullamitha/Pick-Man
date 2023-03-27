from constants import *
from helperFunctions import *
from player import *
import random
import math
from maze import *

class SimplePathFindingGhost:
  def __init__(self, givenX, givenY, givenImage, givenName, givenNextX = 0, givenNextY = 0):
    self.posX = givenX
    self.posY = givenY
    self.__startPosX = givenX
    self.__startPosY = givenY
    self.__image = givenImage
    self.__name = givenName
    self.__moving = True
    self.__firstXMovement = givenNextX
    self.__firstYMovement = givenNextY
    self.__nextDirection = [givenNextX, givenNextY]
    self.__movements = 0

  #setters and getters
  def getName(self):
    return self.__name 
  def setName(self, givenName):
    self.__name = givenName
  
  def getMoving(self):
    return self.__moving
  def setMoving(self, givenMoving):
    self.__moving = givenMoving

  def getPosX(self):
    return self.posX
  def setPosX(self, givenX):
    self.posX = givenX

  def getPosY(self):
    return self.posY
  def setPosY(self, givenY):
    self.posY = givenY
  
  def getStartPosX(self):
    return self.__startPosX
  def setStartPosX(self, givenX):
    self.__startPosX = givenX

  def getStartPosY(self):
    return self.__startPosY
  def setStartPosY(self, givenY):
    self.__startPosY = givenY

  def getMovements(self):
    return self.__movements
  def setMovements(self, givenMovements):
    self.__movements = givenMovements
  def resetMovements(self):
    self.__movements = 0

  def getImage(self):
    return self.__image
  def setImage(self, givenImage):
    self.__image = givenImage
  
  def getNextDirection(self):
    return self.__nextDirection
  def resetNextDirection(self):
    self.__nextDirection = [self.__firstXMovement, self.__firstYMovement]

  def respawn(self):
    self.posX = self.__startPosX
    self.posY = self.__startPosY
    self.__nextDirection = [self.__firstXMovement, self.__firstYMovement]
    self.__movements = 0

  def setTarget(self, game): # create list of directions for ghost to get to player
    playerPosition = (int(game.player.getPosX()), int(game.player.getPosY()))
    potentialDirections = []
    # for each direction the ghost can move in, add to potentialDirections array
    if (self.posX - 1, self.posY) not in game.maze.getWalls() and (self.posX - 1, self.posY) not in game.maze.getGhosts():
      potentialDirections.append((-1,0))
    if (self.posX + 1, self.posY) not in game.maze.getWalls() and (self.posX + 1, self.posY) not in game.maze.getGhosts():
      potentialDirections.append((1,0))
    if (self.posX, self.posY - 1) not in game.maze.getWalls() and (self.posX, self.posY - 1) not in game.maze.getGhosts():
      potentialDirections.append((0,-1))
    if (self.posX, self.posY + 1) not in game.maze.getWalls() and (self.posX, self.posY + 1) not in game.maze.getGhosts():
      potentialDirections.append((0,1))
    # check which direction allows the ghost to be closest to the player
    distanceFromPlayer = float('inf')
    for direction in potentialDirections:
      if distanceFromPlayer > abs(self.posX + direction[0] - playerPosition[0]) + abs(self.posY + direction[1] - playerPosition[1]):
        distanceFromPlayer = abs(self.posX + direction[0] - playerPosition[0]) + abs(self.posY + direction[1] - playerPosition[1])
        directionToMove = direction
    # change the direction the ghost should move in 
    self.__nextDirection = [directionToMove[0], directionToMove[1]]
    self.__movements = 0
  
  def move(self, game): # update position of ghost
    if self.__moving:
      if self.__movements >= 4:
        # reset new direction if ghost has just moved 1 unit
        self.setTarget(game)
      # increment position by 0.1 * x and y movement to slow down
      self.posX += self.__nextDirection[0]/4
      self.posY += self.__nextDirection[1]/4
      # decrease number of movements so that at 0 the direction can change
      self.__movements += 1
  
  def setUpInitialPosition(self, posX, posY):
    self.posX = posX
    self.posY = posY
    self.__startPosX = posX
    self.__startPosY = posY
    self.resetNextDirection()
    self.resetMovements()

class WanderingGhost(SimplePathFindingGhost):
  def __init__(self, givenX, givenY, givenImage, givenName):
    SimplePathFindingGhost.__init__(self, givenX, givenY, givenImage, givenName)
    self.__moving = True
    self.__direction = random.choice(["left", "right", "up", "down"])
    self.__movements = 0
  
  def getDirection(self):
    return self.__direction
  def setDirection(self, givenDirection):
    self.__direction = givenDirection

  def move(self, game): # ghost move function
    if self.__moving:
      changeX, changeY = 0, 0
      match (self.__direction): # update changeX and changeY depending on direction of player
        # check if new coordinates would cause wall collision
        case "left":
          if (math.floor(self.posX - 0.1), self.posY) in game.maze.getPaths() or (math.floor(self.posX - 0.1), self.posY) in game.maze.getGhosts(): 
            changeX = -0.1
        case "right":
          if (math.ceil(self.posX + 0.1), self.posY) in game.maze.getPaths() or (math.ceil(self.posX + 0.1), self.posY) in game.maze.getGhosts(): 
            changeX = 0.1
        case "up":
          if (self.posX, math.floor(self.posY - 0.1)) in game.maze.getPaths() or (self.posX, math.floor(self.posY - 0.1)) in game.maze.getGhosts(): 
            changeY = -0.1
        case "down":
          if (self.posX, math.ceil(self.posY + 0.1)) in game.maze.getPaths() or (self.posX, math.ceil(self.posY + 0.1)) in game.maze.getGhosts(): 
            changeY = 0.1

      # if no movement or movement in one direction many times, reset movements and change direction
      if changeX == 0 and changeY == 0 or self.__movements <= 0: 
        self.__direction = random.choice(["left", "right", "up", "down"])
        self.__movements = random.choice([10, 20, 30, 40, 50])

      else: # check if new coordinates collide with wall
        self.__movements += 0.1
        self.posX += changeX # update new positions
        self.posY += changeY


class AStarGhost(SimplePathFindingGhost):
  
  def __init__(self, givenX, givenY, givenImage, givenName, givenNextX, givenNextY):
    SimplePathFindingGhost.__init__(self, givenX, givenY, givenImage, givenName, givenNextX, givenNextY)
    self.__startPosX = givenX
    self.__startPosY = givenY
    self.__moving = True
    self.__route = []
    self.__movements = 0
    self.__nextDirection = []
  
  def respawn(self):
    self.posX = self.__startPosX
    self.posY = self.__startPosY
    self.__route = []
    self.__movements = 0
    self.__nextDirection = []
    self.__route = [(self.posX, self.posY)]

  def getHeuristic(self, givenPosX, givenPosY, playerPosX, playerPosY):
    # find manhattan distance from given position to goal
    return abs(givenPosX -  playerPosX) + abs(givenPosY - playerPosY)

  def getPath(self, givenMaze, playerPosX, playerPosY):
    currentPosition = (round(self.posX), round(self.posY))
    # list of possible four directions ghost can move in
    neighbours = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    # list items that have been considered
    closedList = []
    # list of items whose neighbours should be considered
    openList = []
    # contains dictionary of previous nodes to each visited node
    previousPositions = {}
    # movement cost from start to current
    gMovementCost = {(currentPosition[0], currentPosition[1]): 0}
    # heuristic movement cost from current to goal 
    fHeuristic = {(currentPosition[0], currentPosition[1]): self.getHeuristic(currentPosition[0], currentPosition[1], playerPosX, playerPosY)}
    # place start position in open list to be considered
    openList.append((fHeuristic[(currentPosition[0], currentPosition[1])], (currentPosition[0], currentPosition[1])))
    # list of directions ghost will follow
    self.__route = []

    while len(openList) > 0:

      # find position of node with the lowest heuristic cost in the open list and set this as current node

      lowestFScore = float('inf')
      for item in openList:
        if item[0] < lowestFScore:
          lowestFScore = item[0]
          currentNode = item[1]
          indexToRemove = openList.index(item)

      openList.pop(indexToRemove)
      
      # if current node is the goal node (i.e. player has been found) then return found route

      if currentNode == (playerPosX, playerPosY):
        while currentNode in previousPositions:
          # backtrack and find each previous node 
          self.__route.append(currentNode)
          currentNode = previousPositions[currentNode]
        # flip route as it is currently player to ghost
        self.__route.reverse()
        print(self.__route)
        return
      
      # otherwise place current node in closed list as its neighbours will be considered

      closedList.append(currentNode)

      # find neighbour to current node with the smaller costs and add this to the open list

      for neighbour in neighbours:
        # calculate new neighbour position and total distance
        currentNeighbour = (currentNode[0] + neighbour[0], currentNode[1] + neighbour[1])
        currentGScore = gMovementCost[(currentNode)] + self.getHeuristic(currentNode[0], currentNode[1], currentNeighbour[0], currentNeighbour[1])
        # check whether neighbour is a viable maze position 
        if currentNeighbour in givenMaze.getElements():
          # check whether neighbour is a wall
          if currentNeighbour not in givenMaze.getWalls():
            # check whether neighbour has been considered and has a lower g cost
            if not (currentNeighbour in closedList and currentGScore >= gMovementCost.get(currentNeighbour, 0)):
              if currentGScore < gMovementCost.get(currentNeighbour, 0) or currentNeighbour not in [i[1] for i in openList]:
                # add the current node as the previous position to the neighbour
                previousPositions[currentNeighbour] = currentNode
                # add the costs for the neighbour
                gMovementCost[currentNeighbour] = currentGScore
                fHeuristic[currentNeighbour] = currentGScore + self.getHeuristic(currentNeighbour[0], currentNeighbour[1], playerPosX, playerPosY)
                # add the neighbour in the open list so its neighbours can be considered
                openList.append((fHeuristic[currentNeighbour], currentNeighbour))
      
    return False
  
  def move(self, game):
    if self.__moving:

      # check if ghost has moved one full unit 
      if self.__movements >= 5 or self.__nextDirection == []:
        # remove coordinate of position ghost is currently in from route
        self.__route.pop(0)
        # check if the current route is empty and reset if so
        if len(self.__route) <= 0:
          self.getPath(game.maze, round(game.player.getPosX()), round(game.player.getPosY()))
        # reset number of movements
        self.__movements = 0
        # create direction for player to move in in the form (0, 0)/(1,0) etc. by finding the difference between current and next coordinate
        self.__nextDirection = [(self.__route[0][0]-round(self.posX)), (self.__route[0][1]-round(self.posY))]

      # update current position at a speed of 0.2
      self.posX += self.__nextDirection[0]/5
      self.posY += self.__nextDirection[1]/5
      # increment number of movements 
      self.__movements += 1


  def setUpInitialPosition(self, posX, posY):
    self.posX = posX
    self.posY = posY
    self.__startPosX = posX
    self.__startPosY = posY
    self.__movements = 0 
    self.__route = [(self.posX, self.posY)]
    self.__nextDirection = []
  
  



blinky = WanderingGhost(None, None, "redghost.png", "Blinky")
inky = AStarGhost(None, None, "blueghost.png", "Inky", 1, 0)
winky = SimplePathFindingGhost(None, None, "purpleghost.png", "Winky", -1, 0)