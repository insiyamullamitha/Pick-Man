from constants import *
from helperFunctions import *
from maze import *
from player import *
import random
import math
from operator import xor

class Ghost:
  def __init__(self, givenX, givenY, givenImage, givenName):
    self.posX = givenX
    self.posY = givenY
    self.__startPosX = givenX
    self.__startPosY = givenY
    self.__image = givenImage
    self.__name = givenName
    self.__moving = True

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

  def respawn(self):
    self.posX = self.__startPosX
    self.posY = self.__startPosY
    
  #add move, draw, kill and reset methods
  def move(self, player, maze):
    heuristic = float('inf')
    while self.__moving and heuristic >= 0:
      for availablePathX in range(1, -2, -1):
        for availablePathY in range(1, -2, -1):
          if abs(availablePathX) != abs(availablePathY):
            if (self.posX + availablePathX, self.posY + availablePathY) not in maze.getWalls():
              tempheuristic = abs(player.getPosX() - (self.posX + availablePathX)) + abs(player.getPosY() - (self.posY+ availablePathY))
              print(heuristic)
              print(tempheuristic)
              if heuristic > tempheuristic:
                heuristic = tempheuristic
                newX = self.posX + availablePathX
                newY = self.posY + availablePathY
    self.posX = newX
    self.posY = newY
    print(self.posX, self.posY)

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

  def move(self, maze): # ghost move function
    if self.__moving:
      changeX, changeY = 0, 0
      match (self.__direction): # update changeX and changeY depending on direction of player
        # check if new coordinates would cause wall collision
        case "left":
          if (math.floor(self.posX - 0.1), self.posY) in maze.getPaths() or (math.floor(self.posX - 0.1), self.posY) in maze.getGhosts(): 
            changeX = -0.1
        case "right":
          if (math.ceil(self.posX + 0.1), self.posY) in maze.getPaths() or (math.ceil(self.posX + 0.1), self.posY) in maze.getGhosts(): 
            changeX = 0.1
        case "up":
          if (self.posX, math.floor(self.posY - 0.1)) in maze.getPaths() or (self.posX, math.floor(self.posY - 0.1)) in maze.getGhosts(): 
            changeY = -0.1
        case "down":
          if (self.posX, math.ceil(self.posY + 0.1)) in maze.getPaths() or (self.posX, math.ceil(self.posY + 0.1)) in maze.getGhosts(): 
            changeY = 0.1

      # if no movement or movement in one direction many times, reset movements and change direction
      if changeX == 0 and changeY == 0 or self.__movements <= 0: 
        self.__direction = random.choice(["left", "right", "up", "down"])
        self.__movements = random.choice([10, 20, 30, 40, 50])

      else: # check if new coordinates collide with wall
        self.__movements -= 1
        self.posX += changeX # update new positions
        self.posY += changeY

  def kill(self, player):
    # check for collisions with player and return true if collision has occurred
    if (math.ceil(self.posX) == player.getPosX() or math.floor(self.posX) == player.getPosX()) and (math.ceil(self.posY) == player.getPosY() or math.floor(self.posY) == player.getPosY()): 
      return True


blinky = WanderingGhost(None, None, "redghost.png", "Blinky")
inky = WanderingGhost(None, None, "blueghost.png", "Inky")
winky = WanderingGhost(None, None, "purpleghost.png", "Winky")