from constants import*
from helperFunctions import *
import random
from powerup import *
vec = pygame.math.Vector2()

# maze class to instantiate structure of maze
class Maze:
    def __init__(self):
        #self.maze = givenMaze
        self.__walls = []
        self.__pills = []
        self.__ghosts = []
        self.__door1 = None
        self.__door2 = None
        self.__powerups = []
        self.__paths = []
        self.__player = None
        self.__mazeLayout = None
        self.__elements = []

    #render maze on screen 
    def getMaze(self):
        return self.__maze
    def setMaze(self, givenMaze):
        self.__maze = givenMaze
    def changeMaze(self, column, row, newCharacter):
        self.__maze[row][column] = newCharacter

    def getWalls(self):
        return self.__walls
    def getAWall(self, pos):
        return self.__walls[pos]
    def appendWalls(self, givenWalls):
        self.__walls.append(givenWalls)
    def resetWalls(self):
        self.__walls = []

    def getPaths(self):
        return self.__paths
    def getAPath(self, pos):
        return self.__paths[pos]
    def appendPath(self, givenPath):
        self.__paths.append(givenPath)
    def resetPaths(self):
        self.__paths = []

    def getPills(self):
        return self.__pills
    def getAPill(self, pos):
        return self.__pills[pos]
    def removePill(self, index):
        self.__pills.pop(index)
    def appendPills(self, givenPill):
        self.__pills.append(givenPill)
    def resetPills(self):
        self.__pills = []

    def getGhosts(self):
        return self.__ghosts
    def getAGhost(self, pos):
        return self.__ghosts[pos]
    def appendGhosts(self, givenGhost):
        self.__ghosts.append(givenGhost)
    def resetGhosts(self):
        self.__ghosts = []

    def getDoor1(self):
        return self.__door1
    def resetDoor1(self):
        self.__door1 = None
    
    def getDoor2(self):
        return self.__door2
    def resetDoor2(self):
        self.__door2 = None
    
    def getPowerups(self):
        return self.__powerups
    def getAPowerup(self, pos):
        return self.__powerups[pos]
    def appendPowerups(self, givenPowerup):
        self.__powerups.append(givenPowerup)
    def removePowerup(self, index):
        self.__powerups.pop(index)
    def resetPowerups(self):
        self.__powerups = []

    def getPlayer(self):
        return self.__player
    def setPlayer(self, givenPlayer):
        self.__player = givenPlayer
    def resetPlayer(self):
        self.__player = None
    
    def getElements(self):
        return self.__elements

    def loadMaze(self, maze, givenTheme):
        self.__mazeLayout = maze 
        self.resetDoor1()
        self.resetDoor2()
        self.resetPowerups()
        self.resetPills()
        self.resetGhosts()
        self.resetPlayer()
        self.resetPaths()
        self.resetWalls()
        # reset arrays for each component so they do not end up having more vectors than there are every time the method is run
        for row in range(0, len(self.__mazeLayout)):
            for column in range(0, len(self.__mazeLayout[row])):
                self.__elements.append((column, row))
                if self.__mazeLayout[row][column] == "1":#walls
                    self.__walls.append(pygame.math.Vector2(column, row))
                elif self.__mazeLayout[row][column] != "G":
                    self.__paths.append(pygame.math.Vector2(column, row))
                if "P" in self.__mazeLayout[row][column]:#pills
                    self.__pills.append(pygame.math.Vector2(column, row))
                if "G" in self.__mazeLayout[row][column]:#ghosts
                    self.__ghosts.append(pygame.math.Vector2(column, row))
                    #pygame.draw.rect(SCREEN, BLACK, pygame.Rect((275 + (column*30)), 65 + (row*30), 30, 30),0)
                    pass
                if "D" in self.__mazeLayout[row][column]:#doors
                    # door 1 user moves left into
                    if "1" in self.__mazeLayout[row][column]:
                        self.__door1 = pygame.math.Vector2(column, row)
                    # door 2 moves right into
                    elif "2" in self.__mazeLayout[row][column]:
                        self.__door2 = pygame.math.Vector2(column, row)
                if self.__mazeLayout[row][column] == "B":#booster
                    newPowerup = Powerup(random.choice(["score", "speed", "mode"]), "positive", 1, column, row, random.choice([5, 10, 50, 100]), allCharacters[2][0][givenTheme])
                    self.__powerups.append(newPowerup) # add to attribute of array of powerups
                if "U" in self.__mazeLayout[row][column]:#user sprite position
                    self.__player = pygame.math.Vector2(column, row)

    def addPowerup(self, givenTheme): # append new powerup object 
        # choose random pill to convert to powerup
        powerupPosition = random.choice(self.__pills)
        newPowerup = Powerup(random.choice(["score", "speed", "mode"]), "positive", 1, powerupPosition.x, powerupPosition.y, random.choice([5, 10, 50, 100]), allCharacters[2][0][givenTheme])
        # update new powerup and pill object arrays
        self.__powerups.append(newPowerup)
        self.__pills.remove(powerupPosition)


level1Maze = [["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
              ["1", "P", "P", "P", "P", "PD2", "1", "P", "P", "P", "P", "B", "P", "P", "P", "P", "P", "1", "P", "P", "P", "P", "P", "1"],
              ["1", "P", "1", "1", "1", "P", "1", "P", "1", "1", "1", "1", "1", "1", "1", "1", "P", "1", "P", "P", "P", "B", "P", "1"],
              ["1", "P", "1", "B", "P", "P", "1", "P", "P", "P", "P", "1", "P", "P", "P", "P", "P", "1", "P", "P", "P", "P", "P", "1"],
              ["1", "P", "P", "P", "1", "P", "1", "P", "1", "1", "P", "1", "P", "1", "1", "1", "P", "1", "1", "1", "P", "P", "P", "1"],
              ["1", "1", "1", "P", "1", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "1", "1", "1", "P", "1"],
              ["1", "P", "1", "P", "P", "P", "P", "P", "P", "1", "1", "P", "0", "1", "P", "1", "1", "1", "P", "P", "1", "P", "P", "1"],
              ["1", "P", "1", "1", "1", "P", "1", "1", "1", "1", "G", "G", "G", "1", "1", "1", "B", "P", "P", "P", "P", "P", "P", "1"],
              ["1", "P", "P", "B", "P", "P", "1", "P", "P", "1", "1", "1", "1", "1", "B", "1", "P", "1", "P", "1", "1", "1", "P", "1"],
              ["1", "1", "1", "P", "1", "P", "1", "P", "P", "P", "P", "1", "P", "P", "P", "1", "P", "P", "P", "1", "P", "P", "P", "1"],
              ["1", "P", "P", "P", "1", "P", "1", "1", "1", "P", "P", "1", "P", "P", "P", "1", "P", "1", "1", "1", "P", "P", "P", "1"],
              ["1", "P", "P", "P", "1", "P", "1", "P", "P", "P", "P", "1", "P", "P", "P", "P", "P", "1", "P", "P", "P", "1", "P", "1"],
              ["1", "P", "1", "1", "1", "P", "1", "P", "1", "1", "1", "1", "1", "1", "1", "1", "P", "1", "P", "1", "1", "1", "P", "1"],
              ["1", "B", "1", "P", "P", "P", "P", "P", "P", "P", "P", "U", "P", "P", "P", "P", "P", "1", "PD1", "B", "P", "P", "P", "1"],
              ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]]

level2Maze = [["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
              ["1", "P", "P", "P", "1", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "1", "1", "1", "P", "P", "P", "1"],
              ["1", "P", "1", "P", "1", "P", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "P", "1", "1", "1", "P", "1", "P", "1"],
              ["1", "P", "1", "B", "1", "P", "P", "P", "1", "1", "1", "1", "1", "1", "1", "1", "P", "P", "P", "P", "P", "1", "B", "1"],
              ["1", "1", "1", "P", "P", "P", "1", "P", "P", "B", "1", "1", "1", "1", "1", "P", "P", "PD2", "1", "1", "P", "1", "1", "1"],
              ["1", "P", "1", "P", "1", "1", "1", "1", "1", "P", "P", "P", "P", "P", "P", "P", "1", "1", "1", "1", "P", "1", "P", "1"],
              ["1", "P", "1", "P", "P", "P", "1", "P", "P", "P", "1", "1", "0", "1", "1", "P", "P", "P", "1", "P", "P", "1", "P", "1"],
              ["1", "P", "P", "U", "1", "P", "P", "P", "1", "P", "1", "G", "G", "G", "1", "P", "1", "P", "P", "P", "P", "P", "P", "1"],
              ["1", "P", "1", "P", "P", "P", "1", "P", "P", "P", "1", "1", "1", "1", "1", "P", "P", "P", "1", "P", "P", "1", "P", "1"],
              ["1", "P", "1", "P", "1", "1", "1", "1", "1", "P", "P", "P", "P", "P", "P", "P", "1", "1", "1", "1", "P", "1", "P", "1"],
              ["1", "1", "1", "P", "P", "P", "1", "P", "P", "P", "1", "P", "1", "1", "1", "1", "1", "P", "1", "P", "P", "1", "P", "1"],
              ["1", "P", "1", "P", "1", "P", "B", "P", "1", "1", "1", "B", "P", "P", "P", "P", "P", "P", "P", "P", "1", "1", "P", "1"],
              ["1", "P", "1", "P", "1", "P", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "P", "1"],
              ["1", "P", "P", "P", "1", "PD1", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "B", "P", "1"],
              ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]]


level3Maze = [["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"],
              ["1","P","1","1","1","P","1","1","1","1","1","P","1","1","1","P","1"],
              ["1","P","P","P","P","P","P","P","P","P","B","P","P","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","P","1","1","P","1","1","1","P","1"],
              ["1","B","P","P","1","P","P","1","P","1","P","P","1","P","P","P","1"],
              ["1","1","1","P","1","P","P","P","P","P","P","P","1","P","1","1","1"],
              ["1","1","1","P","1","P","1","1","0","1","1","P","1","P","1","1","1"],
              ["1","UD1","P","P","P","P","1","G","G","G","1","P","P","P","P","PD2","1"],
              ["1","1","1","P","1","P","1","1","1","1","1","P","1","B","1","1","1"],
              ["1","1","1","P","1","P","P","P","P","P","P","P","1","P","1","1","1"],
              ["1","P","P","P","1","P","P","1","P","1","P","P","1","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","P","1","1","P","1","1","1","P","1"],
              ["1","P","P","P","P","P","P","P","P","B","P","P","P","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","1","1","1","P","1","1","1","P","1"],
              ["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"]]




