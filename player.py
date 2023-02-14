from constants import *
import pygame
from ghost import *
from pygame.locals import *
from helperFunctions import *
from maze import *
# declare player class 

class Player:
  def __init__(self, givenRotation, givenPosX, givenPosY):
    self.mode = "chased"
    self.speed = 1
    self.startPosX = givenPosX
    self.startPosY = givenPosY
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
  
  def getStartPosX(self):
    return self.startPosX
  def setStartPosX(self, givenPosX):
    self.startPosX = givenPosX
  
  def getStartPosY(self):
    return self.startPosY
  def setStartPosY(self, givenPosY):
    self.startPosY = givenPosY


  #rotate pacman image so it faces towards the direction it moves in
  def getRotate(self):
    return self.rotate
  def setRotate(self, givenRotation):
    self.rotate = givenRotation

  def move(self, direction, maze):  # takes in direction of movement and updates player coordinates
    match direction:
      case "left": # move left
        if (self.posX - 1, self.posY) not in maze.getWalls():
          self.posX -= 1
          self.rotate = 0
      case "right": # move right
        if (self.posX + 1, self.posY) not in maze.getWalls():
          self.posX += 1
          self.rotate = 180
      case "up": # move up
        if (self.posX, self.posY-1) not in maze.getWalls():          
          self.posY -= 1
          self.rotate = 270
      case "down": # move down
        if (self.posX, self.posY+1) not in maze.getWalls():
          self.posY += 1
          self.rotate = 270

  def collisions(self, maze): # after new movement check for collisions between players and ghosts/pills/powerups
    if (self.posX, self.posY) in maze.getPills(): # check if player position is in pill position
      playSoundEffects(PILLSOUND)
      self.eatPills(maze)
      return "pills"
    for powerup in maze.getPowerups():
      if (self.posX, self.posY) == (powerup.getPosX(), powerup.getPosY()):
        playSoundEffects(POWERUPSOUND)
        return "powerups"
  
  def eatPills(self, maze): # remove pill vector from pills array if player is in same position
    pillToBeEaten = maze.getPills().index((self.posX, self.posY))
    maze.removePill(pillToBeEaten)
  
