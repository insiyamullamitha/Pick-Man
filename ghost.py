from constants import *
from helperFunctions import *
from player import *
import random
import math

class Ghost:
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
    self.__nextCoordinates = [0,0]

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
    self.__nextCoordinates[0] = givenX + self.__firstXMovement
  def resetStartPosX(self):
    self.posX = self.__startPosX
    self.__nextCoordinates[0] = self.posX + self.__firstXMovement

  def getStartPosY(self):
    return self.__startPosY
  def setStartPosY(self, givenY):
    self.__startPosY = givenY
    self.__nextCoordinates[1] = givenY + self.__firstYMovement
  def resetStartPosY(self):
    self.posY = self.__startPosY
    self.__nextCoordinates[1] = self.posY + self.__firstYMovement

  def getImage(self):
    return self.__image
  def setImage(self, givenImage):
    self.__image = givenImage

  def respawn(self):
    self.resetStartPosX()
    self.resetStartPosY()

  def setTarget(self, game): # create list of directions for ghost to get to player
    playerPosition = (int(game.player.getPosX()), int(game.player.getPosY()))
    currentPosition = [self.posX, self.posY]
    distanceFromPlayer = float('inf')
    if distanceFromPlayer != 0: # if ghost and player have not collided find new position
      potentialPositions = []
      # for each direction the ghost can move in, add to potentialPositions array
      if (math.floor(currentPosition[0] - 0.1), currentPosition[1]) not in game.maze.getWalls() and (math.floor(currentPosition[0] - 0.1), currentPosition[1]) not in game.maze.getGhosts():
        potentialPositions.append((currentPosition[0] - 0.1, currentPosition[1])) 
      if (math.ceil(currentPosition[0] + 0.1), currentPosition[1]) not in game.maze.getWalls() and (math.ceil(currentPosition[0] + 0.1), currentPosition[1]) not in game.maze.getGhosts():
        potentialPositions.append((currentPosition[0] + 0.1, currentPosition[1]))
      if (currentPosition[0], math.floor(currentPosition[1] - 0.1)) not in game.maze.getWalls() and (currentPosition[0], math.floor(currentPosition[1] - 0.1)) not in game.maze.getGhosts():
        potentialPositions.append((currentPosition[0], currentPosition[1] - 0.1))
      if (currentPosition[0], math.ceil(currentPosition[1] + 0.1)) not in game.maze.getWalls() and (currentPosition[0], math.ceil(currentPosition[1] + 0.1)) not in game.maze.getGhosts():
        potentialPositions.append((currentPosition[0], currentPosition[1] + 0.1))
      # check which position allows the ghost to be closest to the player
      for position in potentialPositions:
        if distanceFromPlayer > (abs(position[0] - playerPosition[0]) +  abs(position[1] - playerPosition[1])):
          distanceFromPlayer = (abs(position[0] - playerPosition[0]) +  abs(position[1] - playerPosition[1]))
          currentPosition = [position[0], position[1]]
      self.__nextCoordinates = currentPosition
  
  def move(self, game): # update position of ghost
    if self.__moving:
      self.posX = self.__nextCoordinates[0]
      self.posY = self.__nextCoordinates[1]
      self.setTarget(game)

class WanderingGhost(Ghost):
  def __init__(self, givenX, givenY, givenImage, givenName):
    Ghost.__init__(self, givenX, givenY, givenImage, givenName)
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

blinky = Ghost(None, None, "redghost.png", "Blinky", 1, 0)
inky = Ghost(None, None, "blueghost.png", "Inky")
winky = Ghost(None, None, "purpleghost.png", "Winky", -1, 0)