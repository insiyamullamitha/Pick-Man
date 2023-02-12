import pygame
from pygame.locals import *
from constants import *
from helperFunctions import *
from maze import *
from player import *

class Pill:
  def __init__(self, givenPosX, givenPosY):
    self.value = 3
    self.posX = givenPosX
    self.posY = givenPosY

  def getValue(self):
    return self.value
  def setValue(self, givenValue):
    self.value = givenValue

  def getPosX(self):
    return self.posX
  def setPosX(self, givenPosX):
    self.posX = givenPosX
  
  def getPosY(self):
    return self.posY
  def setPosY(self, givenPosY):
    self.posY = givenPosY

  def draw(self, x, y):#upload pill image in given position
    pygame.draw.circle(SCREEN, PINK, (self.posX,self.posY), 15, 0)
          
pills = []