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
    while self.getMoving() and heuristic >= 0:
      for availablePathX in range(1, -2, -1):
        for availablePathY in range(1, -2, -1):
          if abs(availablePathX) != abs(availablePathY):
            if (self.getPosX() + availablePathX, self.getPosY() + availablePathY) not in maze.getWalls():
              tempheuristic = abs(player.getPosX() - (self.getPosX() + availablePathX)) + abs(player.getPosY() - (self.getPosY()+ availablePathY))
              print(heuristic)
              print(tempheuristic)
              if heuristic > tempheuristic:
                heuristic = tempheuristic
                newX = self.getPosX() + availablePathX
                newY = self.getPosY() + availablePathY
    self.setPosX(newX)
    self.setPosY(newY)
    print(self.getPosX(), self.getPosY())

class WanderingGhost(Ghost):
  def __init__(self, givenX, givenY, givenImage, givenName):
    Ghost.__init__(self, givenX, givenY, givenImage, givenName)
    self.moving = True
    self.direction = random.choice(["left", "right", "up", "down"])
    self.movements = random.choice([10, 20, 30, 40, 50])
  
  def move(self, player, maze): # ghost move function
    if self.moving:
      changeX, changeY = 0, 0
      match (self.direction): # update changeX and changeY depending on direction of player
        # check if new coordinates would cause wall collision
        case "left":
          if (math.floor(self.getPosX() - 0.1), self.getPosY()) in maze.getPaths(): 
            changeX = -0.1
        case "right":
          if (math.ceil(self.getPosX() + 0.1), self.getPosY()) in maze.getPaths():
            changeX = 0.1
        case "up":
          if (self.getPosX(), math.floor(self.getPosY() - 0.1)) in maze.getPaths():
            changeY = -0.1
        case "down":
          if (self.getPosX(), math.ceil(self.getPosY() + 0.1)) in maze.getPaths():
            changeY = 0.1

      # if no movement or movement in one direction many times, reset movements and change direction
      if changeX == 0 and changeY == 0 or self.movements <= 0: 
        self.direction = random.choice(["left", "right", "up", "down"])
        self.movements = random.choice([10, 20, 30, 40, 50])

      else: # check if new coordinates collide with wall
        self.movements -= 1
        self.setPosX(self.getPosX() + changeX) # update new positions
        self.setPosY(self.getPosY() + changeY)
      
      if self.getPosX() == player.getPosX() and self.getPosY() == player.getPosY(): # check for collisions with player and stop moving if true
        return "collision"

blinky = WanderingGhost(None, None, "redghost.png", "Blinky")
inky = WanderingGhost(None, None, "blueghost.png", "Inky")
winky = WanderingGhost(None, None, "purpleghost.png", "Winky")