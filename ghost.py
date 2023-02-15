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
    self.startPosX = givenX
    self.startPosY = givenY
    self.image = givenImage
    self.name = givenName
    self.moving = True

  #setters and getters
  def getName(self):
    return self.name 
  def setName(self, givenName):
    self.name = givenName
  
  def getMoving(self):
    return self.moving
  def setMoving(self, givenMoving):
    self.moving = givenMoving

  def getPosX(self):
    return self.posX
  def setPosX(self, givenX):
    self.posX = givenX

  def getPosY(self):
    return self.posY
  def setPosY(self, givenY):
    self.posY = givenY
  
  def getStartPosX(self):
    return self.startPosX
  def setStartPosX(self, givenX):
    self.startPosX = givenX

  def getStartPosY(self):
    return self.startPosY
  def setStartPosY(self, givenY):
    self.startPosY = givenY

  def getImage(self):
    return self.image
  def setImage(self, givenImage):
    self.image = givenImage

  def respawn(self):
    self.posX = self.startPosX
    self.posY = self.startPosY
    
  #add move, draw, kill and reset methods
  def move(self, player, maze):
    heuristic = float('inf')
    while self.moving and heuristic >= 0:
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
    self.moving = True
    self.direction = random.choice(["left", "right", "up", "down"])
    self.movements = random.choice([10, 20, 30, 40, 50])
  
  def getDirection(self):
    return self.direction
  def setDirection(self, givenDirection):
    self.direction = givenDirection

  def getMovements(self):
    return self.movements
  def setMovements(self, givenMovements):
    self.movements = givenMovements

  def move(self, maze): # ghost move function
    if self.moving:
      changeX, changeY = 0, 0
      match (self.direction): # update changeX and changeY depending on direction of player
        # check if new coordinates would cause wall collision
        case "left":
          if (math.floor(self.posX - 0.1), self.posY) in maze.getPaths(): 
            changeX = -0.1
        case "right":
          if (math.ceil(self.posX + 0.1), self.posY) in maze.getPaths():
            changeX = 0.1
        case "up":
          if (self.posX, math.floor(self.posY - 0.1)) in maze.getPaths():
            changeY = -0.1
        case "down":
          if (self.posX, math.ceil(self.posY + 0.1)) in maze.getPaths():
            changeY = 0.1

      # if no movement or movement in one direction many times, reset movements and change direction
      if changeX == 0 and changeY == 0 or self.movements <= 0: 
        self.direction = random.choice(["left", "right", "up", "down"])
        self.movements = random.choice([10, 20, 30, 40, 50])

      else: # check if new coordinates collide with wall
        self.movements -= 1
        self.posX += changeX # update new positions
        self.posY += changeY

  def kill(self, player):
    # check for collisions with player and return true if collision has occurred
    if round(self.posX) == player.getPosX() and round(self.posY == player.getPosY()): #or round(self.posX) == player.getPosX() and math.floor(self.posY == player.getPosY()): 
      return True


blinky = WanderingGhost(None, None, "redghost.png", "Blinky")
inky = WanderingGhost(None, None, "blueghost.png", "Inky")
winky = WanderingGhost(None, None, "purpleghost.png", "Winky")