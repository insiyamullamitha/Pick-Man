from constants import *
from helperFunctions import *
from maze import *
from player import *
import random

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
  def move(self, player):
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



    uploadImage(self.getImage(), 1, self.getPosX(), self.getPosY())

class WanderingGhost(Ghost):
  def __init__(self, givenX, givenY, givenImage, givenName):
    Ghost.__init__(self, givenX, givenY, givenImage, givenName)
    self.moving = True
    self.direction = random.choice(["left", "right", "up", "down"])
    self.movements = 0
  
  def move(self, player): # ghost move function
    if self.moving:
      moved = False # check if ghost has moved at all in one pass
      changeX, changeY = 0, 0
      match (self.direction): # update changeX and changeY depending on direction of player
        case "left":
          changeX, changeY = -1, 0
        case "right":
          changeX, changeY = 1, 0
        case "up":
          changeX, changeY = 0, -1
        case "down":
          changeX, changeY = 0, 1
      if (self.getPosX() + changeX, self.getPosY() + changeY) not in maze.getWalls(): # check if new coordinates collide with wall
        self.movements += 1
        self.setPosX(self.getPosX() + changeX) # update new positions
        self.setPosY(self.getPosY() + changeY)
        moved = True
      if self.movements >= 4 or not moved: # if no movement or movement in one direction many times, reset movements and change direction
        self.direction = random.choice(["left", "right", "up", "down"])
        self.movements = 0

      if self.getPosX() == player.getPosX() and self.getPosY() == player.getPosY(): # check for collisions with player and stop moving if true
        self.moving = False
        return "collision"

blinky = WanderingGhost(maze.getGhosts()[0].x, maze.getGhosts()[0].y, "redghost.png", "Blinky")
inky = Ghost(maze.getGhosts()[1].x, maze.getGhosts()[1].y, "blueghost.png", "Inky")
winky = Ghost(maze.getGhosts()[2].x, maze.getGhosts()[2].y, "purpleghost.png", "Winky")