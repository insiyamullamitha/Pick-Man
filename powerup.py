from maze import *
from player import *

class Powerup:
    def __init__(self, givenType, givenMode, givenSpeed, givenPosX, givenPosY, givenScoreValue, givenImage):
        self.__image = givenImage
        self.__mode = givenMode
        self.__type = givenType
        self.__speedValue = givenSpeed
        self.__posX = givenPosX
        self.__posY = givenPosY
        self.__scoreValue = givenScoreValue
    
    def getMode(self):
        return self.__mode
    def setMode(self, givenMode):
        self.__mode = givenMode
    
    def getImage(self):
        return self.__image
    def setImage(self, givenImage):
        self.__image = givenImage
    
    def getType(self):
        return self.__type
    def setType(self, givenType):
        self.__type = givenType

    def getSpeedValue(self):
        return self.__speedValue
    def setSpeedValue(self, givenSpeedValue):
        self.__speedValue = givenSpeedValue
    
    def getPosX(self):
        return self.__posX
    def setPosX(self, givenPosX):
        self.__posX = givenPosX

    def getPosY(self):
        return self.__posY
    def setPosX(self, givenPosY):
        self.__posY = givenPosY

    def getScoreValue(self):
        return self.__scoreValue
    def setScoreValue(self, givenScoreValue):
        self.__scoreValue = givenScoreValue
