from constants import *
from helperFunctions import *
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
    self.__target = None

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

  def setTarget(self, game):
    self.__target = (int(game.player.getPosX()-self.posX), int(game.player.getPosY()-self.posY))
    print(self.__target)
    directions = []
    changeX = 0
    if self.__target[0] > 0:
      changeX = 1
    else:
        changeX = -1
    changeY = 0
    if self.__target[1] > 0:
      changeY = 1
    else:
      changeY = -1
        
    for change in abs(self.__target[0]):
      directions.append(changeX, 0)
    for change in abs(self.__target[1]):
      directions.append(0, changeY)


  #add move, draw, kill and reset methods
  def move(self, game):
    if self.__moving:
      moved = False
      self.setTarget(game)
      if self.__target != (0,0):
          if self.__target[0] != 0:
            if (self.posX - 1, self.posY) in game.maze.getPaths():
              self.posX -= 1
              moved = True
            elif (self.posX + 1, self.posY) in game.maze.getPaths():
              self.posX += 1
              moved = True
          
          """if self.__target:
          elif self.__target[1] < 0 or not moved:
            if (self.posX, self.posY-1) in game.maze.getPaths():
              self.posY -= 1
              moved = True
          elif self.__target[1] > 0 or not moved:
            if (self.posX, self.posY+1) in game.maze.getPaths():
              self.posY += 1
              moved = True"""
      
      if moved:
        self.kill(game)


  
  def kill(self, game):
    # check for collisions with player. and return true if collision has occurred
    if (math.ceil(self.posX) == math.ceil(game.player.getPosX()) or math.floor(self.posX) == math.floor(game.player.getPosX())) and (math.ceil(self.posY) == math.ceil(game.player.getPosY()) or math.floor(self.posY) == math.floor(game.player.getPosY())): 
      if game.player.getMode() == "chased":
        game.player.resetPosition()
        self.respawn()
        playSoundEffects(LOSINGLIFE)
        game.lives -= 1 
        if game.lives <= 0:
          game.state = "game over"
          for instruction in range(len(game.instructions)):
            if game.instructions[instruction][0] == 1:
              game.updateFileStarStatus(instruction)

        else:
          self.setMoving(False)
          game.drawMaze()
          pygame.display.flip()
          pygame.time.delay(2000)
          self.setMoving(True)
    
    else:
      game.player.setMode("chased")
      game.character = "pacmandefault.png"
      game.score += 30
      self.respawn()
      self.setMoving(False)


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

  def move(self, game): # ghost move function
    if self.__moving:
      print(self.setTarget(game))
      changeX, changeY = 0, 0
      match (self.__direction): # update changeX and changeY depending on direction of player
        # check if new coordinates would cause wall collision
        case "left":
          if (math.floor(self.posX - 1), self.posY) in game.maze.getPaths() or (math.floor(self.posX - 1), self.posY) in game.maze.getGhosts(): 
            changeX = -1
        case "right":
          if (math.ceil(self.posX + 1), self.posY) in game.maze.getPaths() or (math.ceil(self.posX + 1), self.posY) in game.maze.getGhosts(): 
            changeX = 1
        case "up":
          if (self.posX, math.floor(self.posY - 1)) in game.maze.getPaths() or (self.posX, math.floor(self.posY - 1)) in game.maze.getGhosts(): 
            changeY = -1
        case "down":
          if (self.posX, math.ceil(self.posY + 1)) in game.maze.getPaths() or (self.posX, math.ceil(self.posY + 1)) in game.maze.getGhosts(): 
            changeY = 1

      # if no movement or movement in one direction many times, reset movements and change direction
      if changeX == 0 and changeY == 0 or self.__movements <= 0: 
        self.__direction = random.choice(["left", "right", "up", "down"])
        self.__movements = random.choice([10, 20, 30, 40, 50])

      else: # check if new coordinates collide with wall
        self.__movements -= 1
        self.posX += changeX # update new positions
        self.posY += changeY



blinky = Ghost(None, None, "redghost.png", "Blinky")
inky = Ghost(None, None, "blueghost.png", "Inky")
winky = Ghost(None, None, "purpleghost.png", "Winky")