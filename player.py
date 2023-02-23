from constants import *
import pygame
#from ghost import *
from pygame.locals import *
from helperFunctions import *
from maze import *
import math
# declare player class 

class Player:
  def __init__(self, givenRotation, givenPosX, givenPosY):
    self.__mode = "chased"
    self.__speed = 0.5
    self.__startPosX = givenPosX
    self.__startPosY = givenPosY
    self.__posX = givenPosX
    self.__posY = givenPosY
    self.__rotate = givenRotation
    self.__direction = ""
    self.__changeX = 0
    self.__changeY = 0
    
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
  
  def getChangeX(self):
    return self.__changeX
  def setChangeX(self, givenX):
    self.__changeX = givenX
  
  def getChangeY(self):
    return self.__changeY
  def setChangeY(self, givenY):
    self.__changeY = givenY

  def getStartPosX(self):
    return self.__startPosX
  def setStartPosX(self, givenPosX):
    self.__startPosX = givenPosX
  
  def getStartPosY(self):
    return self.__startPosY
  def setStartPosY(self, givenPosY):
    self.__startPosY = givenPosY

  def getDirection(self):
    return self.__direction
  def setDirection(self, givenDirection):
    match givenDirection:
      case pygame.K_LEFT:
        self.__direction = "left"
      case pygame.K_RIGHT:
        self.__direction = "right"
      case pygame.K_UP:
        self.__direction = "up"
      case pygame.K_DOWN:
        self.__direction = "down"
      case "":
        self.__direction = ""

  def resetPosition(self):
    self.__posX = self.__startPosX
    self.__posY = self.__startPosY
    self.__rotate = 0


  #rotate pacman image so it faces towards the direction it moves in
  def getRotate(self):
    return self.__rotate
  def setRotate(self, givenRotation):
    self.__rotate = givenRotation

  def move(self, game):  # takes in direction of movement and updates player coordinates
    movement = False
    for x in range(int(self.__speed/0.5)):
      match self.__direction:
        case "left":
          if (math.floor(self.__posX - 0.5), self.__posY) in game.maze.getPaths():
            self.__changeX += -0.5
            self.__rotate = 180
            movement = True
        case "right":
          if (math.ceil(self.__posX + 0.5), self.__posY) in game.maze.getPaths():
            self.__changeX += 0.5
            self.__rotate = 0
            movement = True
        case "up":
          if (self.__posX, math.floor(self.__posY-0.5)) in game.maze.getPaths():          
            self.__changeY += -0.5
            self.__rotate = 90
            movement = True
        case "down":
          if (self.__posX, math.ceil(self.__posY+0.5)) in game.maze.getPaths():
            self.__changeY += 0.5
            self.__rotate = 270
            movement = True
        case __:
          return
      if movement:
        self.update(game)

  def collisions(self, game): # after new movement check for collisions between players and ghosts/pills/powerups
    if (round(self.__posX), round(self.__posY)) in game.maze.getPills(): # check if player position is in pill position
      playSoundEffects(PILLSOUND)
      self.eatPills(game)
      return "pills"
    for powerup in game.maze.getPowerups():
      if (round(self.__posX), round(self.__posY)) == (powerup.getPosX(), powerup.getPosY()): # check if player position is in powerup position
        playSoundEffects(POWERUPSOUND)
        game.maze.getPowerups().remove(powerup)
        if powerup.getType() == "score":
          game.score += powerup.getScoreValue()
        elif powerup.getType() == "speed":
          self.__speed = powerup.getSpeedValue()
        elif powerup.getType() == "mode":
          self.__mode = "chasing"
          game.character = "bluepacmandefault.png"

  def update(self, game):
    self.__posX += self.__changeX 
    self.__posY += self.__changeY 
    self.__changeX = 0
    self.__changeY = 0
    self.collisions(game)

  def eatPills(self, game): # remove pill vector from pills array if player is in same position
    game.score += 1
    pillToBeEaten = game.maze.getPills().index((round(self.__posX), round(self.__posY)))
    game.maze.removePill(pillToBeEaten)

