from constants import *
from helperFunctions import *
from maze import *
from player import *

class Ghost:
  def __init__(self, givenX, givenY, givenImage, givenName):
    self.posX = givenX
    self.posY = givenY
    self.startPosX = givenX
    self.startPosY = givenY
    self.image = givenImage
    self.name = givenName
    self.moving = False

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
  def move(self):
    while self.getMoving() and (self.getPosX(), self.getPosY()) != (player.getPosX(), player.getPosY()):
      destination = (player.getPosX(), player.getPosY())




    uploadImage(self.getImage(), 1, self.getPosX(), self.getPosY())

blinky = Ghost(maze.getGhosts()[0].x, maze.getGhosts()[0].y, "redghost.png", "Blinky")
inky = Ghost(maze.getGhosts()[1].x, maze.getGhosts()[1].y, "blueghost.png", "Inky")
winky = Ghost(maze.getGhosts()[2].x, maze.getGhosts()[2].y, "purpleghost.png", "Winky")