from constants import*
from helperFunctions import *
import pygame
from pygame.locals import *
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
        self.__doors = []
        self.__powerups = []
        self.__paths = []
        self.__player = None

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

    def getDoors(self):
        return self.__doors
    def getADoor(self, pos):
        return self.__doors[pos]
    def appendDoors(self, givenDoor):
        self.__doors.append(givenDoor)
    def resetDoors(self):
        self.__doors = []
    
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

    def loadMaze(self, maze, givenTheme): 
        self.resetDoors()
        self.resetPowerups()
        self.resetPills()
        self.resetGhosts()
        self.resetPlayer()
        self.resetPaths()
        self.resetWalls()
        # reset arrays for each component so they do not end up having more vectors than there are every time the method is run
        for row in range(0, len(maze)):
            for column in range(0, len(maze[row])):
                if maze[row][column] == "1":#walls
                    self.__walls.append(pygame.math.Vector2(column, row))
                elif maze[row][column] != "G":
                    self.__paths.append(pygame.math.Vector2(column, row))
                if "P" in maze[row][column]:#pills
                    self.__pills.append(pygame.math.Vector2(column, row))
                if "G" in maze[row][column]:#ghosts
                    self.__ghosts.append(pygame.math.Vector2(column, row))
                    #pygame.draw.rect(SCREEN, BLACK, pygame.Rect((275 + (column*30)), 65 + (row*30), 30, 30),0)
                    pass
                if "D" in maze[row][column]:#doors
                    self.__doors.append(pygame.math.Vector2(column, row))
                if maze[row][column] == "B":#booster
                    newPowerup = Powerup(random.choice(["score", "speed", "mode"]), "positive", 1, column, row, random.choice([5, 10, 50, 100]), allCharacters[2][0][givenTheme])
                    self.__powerups.append(newPowerup) # add to attribute of array of powerups
                if "U" in maze[row][column]:#user sprite position
                    self.__player = pygame.math.Vector2(column, row)

    def addPowerup(self, givenTheme): # append new powerup object 
        # choose random pill to convert to powerup
        powerupPosition = random.choice(self.__pills)
        newPowerup = Powerup(random.choice(["score", "speed", "mode"]), "positive", 1, powerupPosition.x, powerupPosition.y, random.choice([5, 10, 50, 100]), allCharacters[2][0][givenTheme])
        # update new powerup and pill object arrays
        self.__powerups.append(newPowerup)
        self.__pills.remove(powerupPosition)


level1Maze = [["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
              ["1", "P", "P", "P", "P", "P", "1", "P", "P", "P", "P", "B", "P", "P", "P", "P", "P", "1", "P", "P", "P", "P", "P", "1"],
              ["1", "P", "1", "1", "1", "P", "1", "P", "1", "1", "1", "1", "1", "1", "1", "1", "P", "1", "P", "P", "P", "B", "P", "1"],
              ["1", "P", "1", "B", "P", "P", "1", "P", "P", "P", "P", "1", "P", "P", "P", "P", "P", "1", "P", "P", "P", "P", "P", "1"],
              ["1", "P", "P", "P", "1", "P", "1", "P", "1", "1", "P", "1", "P", "1", "1", "1", "P", "1", "1", "1", "P", "P", "P", "1"],
              ["1", "1", "1", "P", "1", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "1", "1", "1", "P", "1"],
              ["1", "P", "1", "P", "P", "P", "P", "P", "P", "1", "1", "P", "1", "1", "P", "1", "1", "1", "P", "P", "1", "P", "P", "1"],
              ["1", "P", "1", "1", "1", "P", "1", "1", "1", "1", "G", "G", "G", "1", "1", "1", "B", "P", "P", "P", "P", "P", "P", "1"],
              ["1", "P", "P", "B", "P", "P", "1", "P", "P", "1", "1", "1", "1", "1", "B", "1", "P", "1", "P", "1", "1", "1", "P", "1"],
              ["1", "1", "1", "P", "1", "P", "1", "P", "P", "P", "P", "1", "P", "P", "P", "1", "P", "P", "P", "1", "P", "P", "P", "1"],
              ["1", "P", "P", "P", "1", "P", "1", "1", "1", "P", "P", "1", "P", "P", "P", "1", "P", "1", "1", "1", "P", "P", "P", "1"],
              ["1", "P", "P", "P", "1", "P", "1", "P", "P", "P", "P", "1", "P", "P", "P", "P", "P", "1", "P", "P", "P", "1", "P", "1"],
              ["1", "P", "1", "1", "1", "P", "1", "P", "1", "1", "1", "1", "1", "1", "1", "1", "P", "1", "P", "1", "1", "1", "P", "1"],
              ["1", "B", "1", "P", "P", "P", "P", "P", "P", "P", "P", "U", "P", "P", "P", "P", "P", "1", "P", "B", "P", "P", "P", "1"],
              ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]]


level2Maze = [["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"],
              ["1","P","1","1","1","P","1","1","1","1","1","P","1","1","1","P","1"],
              ["1","P","P","P","P","P","P","P","P","P","B","P","P","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","P","1","1","P","1","1","1","P","1"],
              ["1","B","P","P","1","P","P","1","P","1","P","P","1","P","P","P","1"],
              ["1","1","1","P","1","P","P","P","P","P","P","P","1","P","1","1","1"],
              ["1","1","1","P","1","P","1","1","0","1","1","P","1","P","1","1","1"],
              ["1","DU","P","P","P","P","1","G","G","G","1","P","P","P","P","DP","1"],
              ["1","1","1","P","1","P","1","1","1","1","1","P","1","B","1","1","1"],
              ["1","1","1","P","1","P","P","P","P","P","P","P","1","P","1","1","1"],
              ["1","P","P","P","1","P","P","1","P","1","P","P","1","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","P","1","1","P","1","1","1","P","1"],
              ["1","P","P","P","P","P","P","P","P","B","P","P","P","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","1","1","1","P","1","1","1","P","1"],
              ["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"]]




