from maze import *
from player import *

class Powerup:
    def __init__(self, givenType, givenMode, givenSpeed, givenPosX, givenPosY, givenScoreValue, givenImage):
        self.image = givenImage
        self.mode = givenMode
        self.type = givenType
        self.speedValue = givenSpeed
        self.posX = givenPosX
        self.posY = givenPosY
        self.scoreValue = givenScoreValue
    
    def getMode(self):
        return self.mode
    def setMode(self, givenMode):
        self.mode = givenMode
    
    def getImage(self):
        return self.image
    def setImage(self, givenImage):
        self.image = givenImage
    
    def getType(self):
        return self.type
    def setType(self, givenType):
        self.type = givenType

    def getSpeedValue(self):
        return self.speedValue
    def setSpeedValue(self, givenSpeedValue):
        self.speedValue = givenSpeedValue
    
    def getPosX(self):
        return self.posX
    def setPosX(self, givenPosX):
        self.posX = givenPosX

    def getPosY(self):
        return self.posY
    def setPosX(self, givenPosY):
        self.posY = givenPosY

    def getScoreValue(self):
        return self.scoreValue
    def setScoreValue(self, givenScoreValue):
        self.scoreValue = givenScoreValue
