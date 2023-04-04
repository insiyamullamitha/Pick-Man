from constants import *
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
    self.__image = "pacmandefault.png"
    
  # getters and setters for private attributes

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
  
  def getImage(self):
    return self.__image
  def setImage(self, givenImage):
    self.__image = givenImage
  
  # rotate = direction player is facing according to their key movement (i.e. right/left etc.)
  def getRotate(self):
    return self.__rotate
  def setRotate(self, givenRotation):
    self.__rotate = givenRotation

  def getDirection(self):
    return self.__direction
  def setDirection(self, givenDirection):
    # set direction of player according to key movement given in event loop
    if givenDirection == pygame.K_LEFT: # left
      self.__direction = "left"
    elif givenDirection == pygame.K_RIGHT: # right
      self.__direction = "right"
    elif givenDirection == pygame.K_UP: # up
      self.__direction = "up"
    elif givenDirection == pygame.K_DOWN: # down
      self.__direction = "down"
    else:
      self.__direction = ""

  def resetPosition(self): 
    # return to starting position of pacman
    self.__posX = self.__startPosX
    self.__posY = self.__startPosY
    self.__rotate = 0

  def move(self, game):  # takes in direction of movement and updates player coordinates
    movement = False
    for x in range(int(self.__speed/0.5)):
      # check direction
      if self.__direction == "left":
        # check if movement would cause wall collisionand update change in coordinates
        if (math.floor(self.__posX - 0.5), self.__posY) in game.maze.getPaths():
          self.__changeX += -0.5
          movement = True
        # check if new user position would cause them to move into a door and change coordinates
        else:
          if (math.floor(self.__posX), self.__posY) == game.maze.getDoor1():
            self.__posX = game.maze.getDoor2().x
            self.__posY = game.maze.getDoor2().y
      elif self.__direction == "right":
        # check if movement would cause wall collision and update change in coordinates
        if (math.ceil(self.__posX + 0.5), self.__posY) in game.maze.getPaths():
          self.__changeX += 0.5
          movement = True
        else:
          # check if new user position would cause them to move into a door and change coordinates
          if (math.ceil(self.__posX), self.__posY) == game.maze.getDoor2():
            self.__posX = game.maze.getDoor1().x
            self.__posY = game.maze.getDoor1().y
      elif self.__direction == "up":
        # check if movement would cause wall collision and update change in coordinates
        if (self.__posX, math.floor(self.__posY-0.5)) in game.maze.getPaths():          
          self.__changeY += -0.5
          movement = True
      elif self.__direction == "down":
        # check if movement would cause wall collision and update change in coordinates
        if (self.__posX, math.ceil(self.__posY+0.5)) in game.maze.getPaths():
          self.__changeY += 0.5
          movement = True
      else:
        return
      # if movement has occurred update new position
    if movement:
      # change rotation of player according to their direction if they are original pacman
      if self.__image == "pacmandefault.png":
        self.__rotate = playerRotations[self.__direction]
      return self.update()

  def checkForCollisions(self, game): # after new movement check for collisions between players and ghosts/pills/powerups
    returnValue = None, None
    # check for pill collision and return pill coordinate
    if (round(self.__posX), round(self.__posY)) in game.maze.getPills(): 
      returnValue =  "pill", (round(self.__posX), round(self.__posY))
    # check if player position is in powerup position and return powerup object
    for powerup in game.maze.getPowerups():
      if (round(self.__posX), round(self.__posY)) == (powerup.getPosX(), powerup.getPosY()): 
        returnValue = "powerup", powerup
    # check for collisions with ghosts and return ghost object
    for ghost in game.ghostObjects: 
      # if player is in chased mode
      if (math.ceil(self.__posX) == math.ceil(ghost.getPosX()) or math.floor(self.__posX) == math.floor(ghost.getPosX())) and (math.ceil(self.__posY) == math.ceil(ghost.getPosY()) or math.floor(self.__posY) == math.floor(ghost.getPosY())): 
        returnValue = "ghost", ghost
    return returnValue

  def update(self):
    # change player position
    self.__posX += self.__changeX 
    self.__posY += self.__changeY 
    # reset changes in coordinates so that the position is not continually updated
    self.__changeX = 0
    self.__changeY = 0
  
  def setUpInitialPosition(self, givenPosX, givenPosY):
    # set player coordinates to start position
    self.__posX = givenPosX
    self.__posY = givenPosY
    # also set separate start coordinates player can return to when resetting
    self.__startPosX = givenPosX
    self.__startPosY = givenPosY
