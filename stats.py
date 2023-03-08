from constants import *
from helperFunctions import *

class Statistics:
  def __init__(self):
    self.__leaderboard = []
    self.__time = []
    self.__numberOfStars = 0
    self.__powerups = 0

  def getLeaderboard(self): # retrieve leaderboard usernames and scores from text file
    with open("statistics.txt") as file:
      self.__leaderboard = []
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
    # update the new leaderboard in the statistics text file
    file = open('statistics.txt', 'r')
    lines = file.readlines()
    for x in range(5):
      lines[x] = str(self.__leaderboard[x][0]) + ',' + self.__leaderboard[x][1] + '\n'

    self.updateFile(lines, "statistics.txt")

  def getFastestTime(self): # retrieve fastest time user has played level in from text file
    with open("statistics.txt") as file:
      lines = file.readlines() 
      # convert to integer form so it can be compared in changeFastestTime()
      self.__time = int(lines[5][5:].strip('\n')) 
    return self.__time

  def changeFastestTime(self, givenTime): # if new time is lower update fastest time
    if givenTime >= self.getFastestTime():
      return
    self.__time = givenTime
    with open("statistics.txt") as file: # update line for time in file 
      lines = file.readlines()
      lines[5] = 'time,' + str(self.__time) + '\n'
    self.updateFile(lines, "statistics.txt")

  def getNumberOfStars(self): # get number of stars the user currently has available
    with open("statistics.txt") as file:
      lines = file.readlines() 
      # convert to integer form so it can be operated on in changeNumberOfStars()
      self.__numberOfStars = int(lines[6][6:].strip('\n')) 
    return self.__numberOfStars

  def changeNumberOfStars(self, changeInStars): # update number of stars when new game or powerup bought
    self.__numberOfStars = self.getNumberOfStars() + changeInStars
    with open("statistics.txt") as file: # update line for stars in file
      lines = file.readlines()
      lines[6] = 'stars,' + str(self.__numberOfStars) + '\n'
    self.updateFile(lines, "statistics.txt")
  
  def getPowerups(self): # get number of extra powerups that user has bought
    with open("statistics.txt") as file:
      lines = file.readlines() 
      # convert to integer form so it can be operated on in changeNumberOfStars()
      self.__powerups = int(lines[7][9:].strip('\n')) 
    return self.__powerups

  def changePowerups(self, changeInPowerups):
    self.__powerups = self.getPowerups() + changeInPowerups
    with open("statistics.txt") as file: # update line for powerups in file
      lines = file.readlines()
      lines[7] = 'powerups,' + str(self.__powerups) + '\n'
    self.updateFile(lines, "statistics.txt")

  def updateFile(self, updatedFile, fileToWriteTo): # update file with new lines
    with open(fileToWriteTo, "w") as file:
      for line in updatedFile:
        file.write(line)
      file.close()
  
  def updateStatistics(self, stars, score = 0, username = "", time = 100): # use to update all statistics at once
    self.updateLeaderboard(score, username)
    self.changeNumberOfStars(stars)
    self.changeFastestTime(time)

  def displayLeaderboard(self): # draw leaderboard table and other stats
    self.__leaderboard = self.getLeaderboard()
    # draw table
    pygame.draw.rect(SCREEN, LIGHTBLUE, pygame.Rect(100, 135, 800, 305), 0, 3)
    pygame.draw.rect(SCREEN, BLACK, pygame.Rect(100, 135, 800, 305), 1, 3)
    for x in range(5):
      pygame.draw.line(SCREEN, BLACK, (100, 50 * x + 190), (900, 50 * x + 190))
    for x in range(2):
      pygame.draw.line(SCREEN, BLACK, (300 + x * 400, 135), (300 + x * 400, 440))
    # table headers
    drawText("RANK", 140, 145, BLACK, 50)
    drawText("PLAYER", 420, 145, BLACK, 50)
    drawText("SCORE", 745, 145, BLACK, 50)
    # draw each leader's username and score
    for leader in range(len(self.__leaderboard)):
      drawText(leader+1, 180, leader*50 + 200, BLACK, 50)
      drawText(self.__leaderboard[leader][1], 427, leader * 50 + 200, BLACK, 50)
      drawText(self.__leaderboard[leader][0], 770, leader * 50 + 200, BLACK, 50)
    # upload star image and number of total stars
    uploadImage("yellowstar.png", 0.08, 100, 470)
    drawText(self.getNumberOfStars(), 200, 500, BLACK, 40)
    # draw text for fastest time
    drawText("FASTEST TIME: " + str(self.getFastestTime()) + " SECONDS", 450, 500, BLACK, 40)

stats = Statistics()
