from constants import *

class Statistics:
  def __init__(self):
    self.__leaderboard = []
    self.__fastestTime = []
    self.__numberOfStars = 0

  def getLeaderboard(self):
    return self.leaderboard
  def setLeaderboard(self, newStat):
    self.leaderboard.append(newStat)

  def getFastestTime(self):
    return self.fastestTime
  def setFastestTime(self, fastestTimeStats):
    self.fastestTime = fastestTimeStats

  def getNumberOfStars(self):
    return self.numberOfStars
  def setNumberOfStars(self, stars):
    self.numberOfStars = stars