from constants import *
import pygame
from ghost import *
from pygame.locals import *
from helperFunctions import *
from maze import *
import math
# declare player class 

class Player:
  def __init__(self, givenRotation, givenPosX, givenPosY):
    self.__mode = "chased"
    self.__speed = 1
    self.__startPosX = givenPosX
    self.__startPosY = givenPosY
    self.__posX = givenPosX
    self.__posY = givenPosY
    self.__rotate = givenRotation
    
  # add getters and setters
  def getMode(self):
    return self.__mode
  def setMode(self, givenMode):
    self.__mode = givenMode

  def getSpeed(self):
    return self.__speed 
  def setSpeed(self, givenSpeed):
    self.__speed = givenSpeed   
  
  def getPosX(self):
    return self.__posX
  def setPosX(self, givenPosX):
    self.__posX = givenPosX
  
  def getPosY(self):
    return self.__posY
  def setPosY(self, givenPosY):
    self.__posY = givenPosY
  
  def getStartPosX(self):
    return self.__startPosX
  def setStartPosX(self, givenPosX):
    self.__startPosX = givenPosX
  
  def getStartPosY(self):
    return self.__startPosY
  def setStartPosY(self, givenPosY):
    self.__startPosY = givenPosY

  def resetPosition(self):
    self.__posX = self.__startPosX
    self.__posY = self.__startPosY
    self.__rotate = 0


  #rotate pacman image so it faces towards the direction it moves in
  def getRotate(self):
    return self.__rotate
  def setRotate(self, givenRotation):
    self.__rotate = givenRotation

  def move(self, direction, maze):  # takes in direction of movement and updates player coordinates
    match direction:
      case "left": # move left
        if (math.floor(self.__posX - 0.2), self.__posY) in maze.getPaths():
          self.__posX -= 0.2
          self.__rotate = 180
      case "right": # move right
        if (math.ceil(self.__posX + 0.2), self.__posY) in maze.getPaths():
          self.__posX += 0.2
          self.__rotate = 0
      case "up": # move up
        if (self.__posX, math.floor(self.__posY-0.2)) in maze.getPaths():          
          self.__posY -= 0.2
          self.__rotate = 90
      case "down": # move down
        if (self.__posX, math.ceil(self.__posY+0.2)) in maze.getPaths():
          self.__posY += 0.2
          self.__rotate = 270

  def collisions(self, maze, direction): # after new movement check for collisions between players and ghosts/pills/powerups
    if (math.ceil(self.__posX), math.ceil(self.__posY)) in maze.getPills() or (math.ceil(self.__posX), math.floor(self.__posY)) in maze.getPills() or (math.floor(self.__posX), math.ceil(self.__posY)) in maze.getPills() or (math.floor(self.__posX), math.floor(self.__posY)) in maze.getPills(): # check if player position is in pill position
      playSoundEffects(PILLSOUND)
      self.eatPills(maze, direction)
      return "pills"
    for powerup in maze.getPowerups():
      if (math.ceil(self.__posX), math.ceil(self.__posY)) in maze.getPowerups() or (math.ceil(self.__posX), math.floor(self.__posY)) in maze.getPowerups() or (math.floor(self.__posX), math.ceil(self.__posY)) in maze.getPowerups() or (math.floor(self.__posX), math.floor(self.__posY)) in maze.getPowerups(): # check if player position is in powerup position
        playSoundEffects(POWERUPSOUND)
        return "powerups"
  
  def eatPills(self, maze, direction): # remove pill vector from pills array if player is in same position
    match direction:
      case "left":
        pillToBeEaten = maze.getPills().index((math.floor(self.__posX), round(self.__posY)))
      case "right":
        pillToBeEaten = maze.getPills().index((math.ceil(self.__posX), round(self.__posY)))
      case "up":
        pillToBeEaten = maze.getPills().index((round(self.__posX), math.floor(self.__posY)))
      case "down":
        pillToBeEaten = maze.getPills().index((round(self.__posX), math.ceil(self.__posY)))

    maze.removePill(pillToBeEaten)
  
