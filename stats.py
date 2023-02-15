#from constants import *

class Statistics:
  def __init__(self):
    self.__leaderboard = []
    self.__time = []
    self.__numberOfStars = 0
    self.__powerups = 0

  def getLeaderboard(self): # retrieve leaderboard usernames and scores from text file
    with open("statistics.txt") as file:
      lines = file.readlines()
      for x in range(5):
        # split each line into score and username
        line = lines[x].strip('\n').split(',') 
        line[0] = int(line[0])
        self.__leaderboard.append(line)
    return self.__leaderboard

  def updateLeaderboard(self, givenScore, givenName): # compare new game statistics and add to leaderboard if appropriate
    self.__leaderboard = self.getLeaderboard()
    for x in range(4, -1, -1): # loop through each line in the leaderboard 
      if givenScore <= self.__leaderboard[x][0]:
        if x == 4:
          return
      else: # if the new score is higher than the one currently at this position then flag this as the line to be changed
        lineToBeChangedIndex = x
    #update the leaderboard
    self.__leaderboard.insert(lineToBeChangedIndex, [givenScore, givenName])
    #remove 6th person in leaderboard
    self.__leaderboard.pop()

    # write the new statistics to the statistics text file
    file = open('statistics.txt', 'r')
    lines = file.readlines()
    for x in range(5):
      lines[x] = str(self.__leaderboard[x][0]) + ',' + self.__leaderboard[x][1] + '\n'
    file = open('statistics.txt', 'w')
    for line in lines:
      file.write(line)
    file.close()

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


stats = Statistics()
stats.updateLeaderboard(4, 'INSIYA')
print(stats.getLeaderboard())