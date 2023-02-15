from constants import *

class Statistics:
  def __init__(self):
    self.__leaderboard = []
    self.__time = []
    self.__numberOfStars = 0
    self.__powerups = 0

  def getLeaderboard(self):
    return self.__leaderboard
  def updateLeaderboard(self):
    pass
  def setLeaderboard(self, newStat):
    self.__leaderboard.append(newStat)

  def getFastestTime(self):
    return self.__time
  def setFastestTime(self, givenTime):
    self.__time = givenTime

  def getNumberOfStars(self):
    return self.__numberOfStars
  def setNumberOfStars(self, stars):
    self.__numberOfStars = stars
  
  def getPowerups(self):
    return self.__powerups
  def setPowerups(self, powerups):
    self.__powerups = powerups