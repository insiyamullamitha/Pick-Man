from constants import *
from helperFunctions import *
from player import *
import random
import math

class PathFindingGhost:
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
    self.__movements = 4

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
    self.__movements = 4

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
    self.__movements = 4
  
  def move(self, game): # update position of ghost
    if self.__moving:
      if self.__movements <= 0:
        # reset new direction if ghost has just moved 1 unit
        self.setTarget(game)
      # increment position by 0.1 * x and y movement to slow down
      self.posX += self.__nextDirection[0]/4
      self.posY += self.__nextDirection[1]/4
      # decrease number of movements so that at 0 the direction can change
      self.__movements -= 1
      game.player.collisions(game)

class WanderingGhost(PathFindingGhost):
  def __init__(self, givenX, givenY, givenImage, givenName):
    PathFindingGhost.__init__(self, givenX, givenY, givenImage, givenName)
    self.__moving = True
    self.__direction = random.choice(["left", "right", "up", "down"])
    self.__movements = 10
  
  def getDirection(self):
    return self.__direction
  def setDirection(self, givenDirection):
    self.__direction = givenDirection

  def getMovements(self):
    return self.__movements
  def setMovements(self, givenMovements):
    self.__movements = givenMovements

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
        self.__movements -= 0.1
        self.posX += changeX # update new positions
        self.posY += changeY

class AStarGhost(PathFindingGhost):
  pass



blinky = PathFindingGhost(None, None, "redghost.png", "Blinky", 1, 0)
inky = WanderingGhost(None, None, "blueghost.png", "Inky")
winky = PathFindingGhost(None, None, "purpleghost.png", "Winky", -1, 0)