from constants import *
import pygame
from pygame.locals import *
from helperFunctions import *
from maze import *
# declare player class 

class Player:
  def __init__(self, givenRotation, givenPosX, givenPosY):
    self.mode = "chased"
    self.speed = 1
    self.startingPosition = (givenPosX, givenPosY)
    self.posX = givenPosX
    self.posY = givenPosY
    self.rotate = givenRotation
    
  # add getters and setters
  def getMode(self):
    return self.mode
  def setMode(self, givenMode):
    self.mode = givenMode
  def changeMode(self):
    if self.mode == "chased":
      self.mode = "chasing"
    else:
      self.mode = "chased"

  def getSpeed(self):
    return self.speed 
  def setSpeed(self, givenSpeed):
    self.speed = givenSpeed   
  
  def getPosX(self):
    return self.posX
  def setPosX(self, givenPosX):
    self.posX = givenPosX
  
  def getPosY(self):
    return self.posY
  def setPosY(self, givenPosY):
    self.posY = givenPosY

  #rotate pacman image so it faces towards the direction it moves in
  def getRotate(self):
    return self.rotate
  def setRotate(self, givenRotation):
    self.rotate = givenRotation

  def move(self, direction):  # takes in direction of movement and updates player coordinates
    match direction:
      case "left": # move left
        if (self.getPosX() - 1, self.getPosY()) not in maze.getWalls():
          self.setPosX(self.getPosX() - 1)
          self.setRotate(0)
      case "right": # move right
        if (self.getPosX() + 1, self.getPosY()) not in maze.getWalls():
          self.setPosX(self.getPosX() + 1)
          self.setRotate(180)
      case "up": # move up
        if (self.getPosX(), self.getPosY()-1) not in maze.getWalls():          
          self.setPosY(self.getPosY() - 1)
          self.setRotate(270)
      case "down": # move down
        if (self.getPosX(), self.getPosY()+1) not in maze.getWalls():
          self.setPosY(self.getPosY() + 1)
          self.setRotate(90)

  def collisions(self): # after new movement check for collisions between players and ghosts/pills/powerups
    if (self.getPosX(), self.getPosY()) in maze.getWalls():
      return "walls"
    if (self.getPosX(), self.getPosY()) in maze.getPills(): # check if player position is in pill position
      playSoundEffects(PILLSOUND)
      self.eatPills()
      return "pills"
    if (self.getPosX(), self.getPosY()) in maze.getPowerups():
      playSoundEffects(POWERUPSOUND)
      return "powerups"
  
  def eatPills(self): # remove pill vector from pills array if player is in same position
    pillToBeEaten = maze.getPills().index((self.getPosX(), self.getPosY()))
    maze.removePill(pillToBeEaten)

player = Player(0, 1, 7)