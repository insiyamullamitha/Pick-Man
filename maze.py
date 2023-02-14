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
        self.walls = []
        self.pills = []
        self.ghosts = []
        self.doors = []
        self.powerups = []
        self.paths = []
        self.player = None

    #render maze on screen 
    def getMaze(self):
        return self.maze
    def setMaze(self, givenMaze):
        self.maze = givenMaze
    def changeMaze(self, column, row, newCharacter):
        self.maze[row][column] = newCharacter

    def getWalls(self):
        return self.walls
    def getAWall(self, pos):
        return self.walls[pos]
    def appendWalls(self, givenWalls):
        self.walls.append(givenWalls)
    def resetWalls(self):
        self.walls = []

    def getPaths(self):
        return self.paths
    def getAPath(self, pos):
        return self.paths[pos]
    def appendPath(self, givenPath):
        self.paths.append(givenPath)
    def resetPaths(self):
        self.paths = []

    def getPills(self):
        return self.pills
    def getAPill(self, pos):
        return self.pills[pos]
    def removePill(self, index):
        self.pills.pop(index)
    def appendPills(self, givenPill):
        self.pills.append(givenPill)
    def resetPills(self):
        self.pills = []

    def getGhosts(self):
        return self.ghosts
    def getAGhost(self, pos):
        return self.ghosts[pos]
    def appendGhosts(self, givenGhost):
        self.ghosts.append(givenGhost)
    def resetGhosts(self):
        self.ghosts = []

    def getDoors(self):
        return self.doors
    def getADoor(self, pos):
        return self.doors[pos]
    def appendDoors(self, givenDoor):
        self.doors.append(givenDoor)
    def resetDoors(self):
        self.doors = []
    
    def getPowerups(self):
        return self.powerups
    def getAPowerup(self, pos):
        return self.powerups[pos]
    def appendPowerups(self, givenPowerup):
        self.powerups.append(givenPowerup)
    def removePowerup(self, index):
        self.powerups.pop(index)
    def resetPowerups(self):
        self.powerups = []

    def getPlayer(self):
        return self.player
    def setPlayer(self, givenPlayer):
        self.player = givenPlayer
    def resetPlayer(self):
        self.player = None

    def load_maze(self, maze): 
        self.resetDoors()
        self.resetPowerups()
        self.resetPills()
        self.resetGhosts()
        self.resetPlayer()
        self.resetPaths()
        self.resetWalls()
        # reset arrays for each component so they do not end up having more vectors than there are every time the method is run
        for row in range(0, len(maze)):
            for column in range(0, len(maze)+2):
                if maze[row][column] == "1" or maze[row][column] == "G":#walls
                    self.walls.append(pygame.math.Vector2(column, row))
                else:
                    self.paths.append(pygame.math.Vector2(column, row))
                if "P" in maze[row][column]:#pills
                    self.pills.append(pygame.math.Vector2(column, row))
                if "G" in maze[row][column]:#ghosts
                    self.ghosts.append(pygame.math.Vector2(column, row))
                    #pygame.draw.rect(SCREEN, BLACK, pygame.Rect((275 + (column*30)), 65 + (row*30), 30, 30),0)
                    pass
                if "D" in maze[row][column]:#doors
                    self.doors.append(pygame.math.Vector2(column, row))
                if maze[row][column] == "B":#booster
                    newPowerup = Powerup(random.choice(["speed", "score", "mode"]), "positive", 2, column, row, 10, random.choice(["cherrypowerup.png", "grapepowerup.png"]))
                    self.powerups.append(newPowerup) # add to attribute of array of powerups
                if "U" in maze[row][column]:#user sprite position
                    self.player = pygame.math.Vector2(column, row)
    
    def draw_maze(self):
        pass



level1Maze = [["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"],
              ["1","P","1","1","1","P","1","1","1","1","1","P","1","1","1","P","1"],
              ["1","P","P","P","P","P","P","P","P","P","B","P","P","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","P","1","1","P","1","1","1","P","1"],
              ["1","B","P","P","1","P","P","1","P","1","P","P","1","P","P","P","1"],
              ["1","1","1","P","1","P","P","P","P","P","P","P","1","P","1","1","1"],
              ["1","1","1","P","1","P","1","1","1","1","1","P","1","P","1","1","1"],
              ["1","DU","P","P","P","P","1","WG","WG","WG","1","P","P","P","P","DP","1"],
              ["1","1","1","P","1","P","1","1","1","1","1","P","1","B","1","1","1"],
              ["1","1","1","P","1","P","P","P","P","P","P","P","1","P","1","1","1"],
              ["1","P","P","P","1","P","P","1","P","1","P","P","1","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","P","1","1","P","1","1","1","P","1"],
              ["1","P","P","P","P","P","P","P","P","B","P","P","P","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","1","1","1","P","1","1","1","P","1"],
              ["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"]]


level1Maze = [["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"],
              ["1","P","1","1","1","P","1","1","1","1","1","P","1","1","1","P","1"],
              ["1","P","P","P","P","P","P","P","P","P","B","P","P","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","P","1","1","P","1","1","1","P","1"],
              ["1","B","P","P","1","P","P","1","P","1","P","P","1","P","P","P","1"],
              ["1","1","1","P","1","P","P","P","P","P","P","P","1","P","1","1","1"],
              ["1","1","1","P","1","P","P","P","P","P","P","P","1","P","1","1","1"],
              ["1","D1U","P","P","P","P","P","G","G","G","P","P","P","P","P","D2P","1"],
              ["1","1","1","P","1","P","P","P","P","P","P","P","1","B","1","1","1"],
              ["1","1","1","P","1","P","P","P","P","P","P","P","1","P","1","1","1"],
              ["1","P","P","P","1","P","P","1","P","1","P","P","1","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","P","1","1","P","1","1","1","P","1"],
              ["1","P","P","P","P","P","P","P","P","B","P","P","P","P","P","P","1"],
              ["1","P","1","1","1","P","1","1","1","1","1","P","1","1","1","P","1"],
              ["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"]]

level2Maze = []




