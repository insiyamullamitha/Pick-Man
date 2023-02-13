import pygame
from pygame.locals import *
from helperFunctions import *
from constants import *
from ghost import *
from maze import *
from player import *
from powerup import *
from button import *
from stats import *

class Game:
  """a class for initialising a game object for pick-man"""
  def __init__(self):
    self.state = "start-up"
    self.previousState = "menu"
    self.running = True
    self.clock = pygame.time.Clock()
    self.score = 0
    self.music = False
    self.soundEffects = False
    self.stars = 0
    self.lives = 3
    self.currentLevel = None
    self.character = "pacmandefault.PNG"
    self.theme = "default"
    self.username = ""
    self.powerupObjects = []
    self.player = Player(0, None, None)
    self.ghostObjects = [blinky, inky, winky]
    self.maze = Maze()

  #getters and setters for app class attributes - except clock as this will not change
  
  def getState(self):
    return self.state
  def setState(self, givenState):
    self.state = givenState

  def getPreviousState(self):
    return self.previousState
  def setPreviousState(self, givenState):
    self.previousState = givenState

  def getRunning(self):
    return self.running
  def setRunning(self, givenRunning):
    self.running = givenRunning

  def getScore(self):
    return self.score
  def setScore(self, givenScore):
    self.score = givenScore
  
  def getMusic(self):
    return self.music
  def setMusic(self, givenMusic):
    self.music = givenMusic

  def getSoundEffects(self):
    return self.soundEffects
  def setSoundEffects(self, givenSoundEffects):
    self.soundEffects = givenSoundEffects

  def getStars(self):
    return self.stars
  def setStars(self, givenStars):
    self.stars = givenStars
  
  def getLives(self):
    return self.lives
  def setLives(self, givenLives):
    self.lives = givenLives

  def getLevel(self):
    return self.currentLevel
  def setLevel(self, givenLevel):
    self.currentLevel = givenLevel

  def getCharacter(self):
    return self.character
  def setCharacter(self, givenCharacter):
    self.character = givenCharacter

  def getTheme(self):
    return self.theme
  def setTheme(self, givenTheme):
    self.theme = givenTheme
  
  def getUsername(self):
    return self.username
  def setUsername(self, givenUsername):
    self.username = givenUsername
  
  def getPowerupObjects(self):
    return self.powerupObjects
  def appendPowerupObjects(self, newPowerup):
    self.powerupObjects.append(newPowerup)
  def resetPowerupObjects(self):
    self.powerupObjects = []

  def getGhostObjects(self):
    return self.ghostObjects
  
  def draw_maze(self): # load maze on screen
    for wall in self.maze.getWalls(): # draw walls
      pygame.draw.rect(SCREEN, BLACK, pygame.Rect((275 + (wall.x*30)), 65 + (wall.y*30), 30, 30),0)
    for path in self.maze.getPaths(): # draw white squares representing path
      pygame.draw.rect(SCREEN, WHITE, pygame.Rect((275 + (path.x*30)), 65 + (path.y*30), 30, 30),0)
    for pill in self.maze.getPills(): # draw pills
      pygame.draw.circle(SCREEN, PINK, (289+pill.x*30, 78+pill.y*30), 5, 0)
    for ghost in self.getGhostObjects(): # ghost objects must be instantiated
      if ghost.move(self.player, self.maze) == "collision":
        self.setLives(self.getLives()-1)
        ghost.moving = False
      uploadImage(ghost.getImage(), 0.8, 275+ghost.getPosX()*30, 65 + ghost.getPosY()*30)
    for powerup in self.getPowerupObjects(): # powerup objects must be instantiated
      uploadImage(powerup.getImage(), 0.7, 280+powerup.getPosX()*30, 70+powerup.getPosY()*30)

  def clickButtons(self):# detects whether button has been clicked and changes game state
    # if any button on the screen has been clicked change game state 
    for buttons in allButtons:
      for button in buttons:
        if button.click() != None:
          if button in allButtons[1] and self.getState() != "menu":
            return
          if button in allButtons[2] and self.getState() == "levels":
            self.setLevel(button.text)
          if button in allButtons[2] and self.getState() != "levels":
            return
          if button in allButtons[3] and self.getState() != "play":
            return
          self.setPreviousState(self.getState())
          self.setState(button.newState)

  def loadPlayer(self):
    uploadImage(self.getCharacter(), 1, 275+self.player.getPosX()*30, 65 + self.player.getPosY()*30)

  
  # check that username is between 3 and 10 characters and save as game username
  def verifyUsername(self):
    if len(usernameButton.text) > 2 and len(usernameButton.text) < 11:
      self.setState("play")
      self.setUsername(usernameButton.text.upper())
    
  def createPowerups(self): # loaded in game loop to instantiate powerup objects
    self.resetPowerupObjects()
    for powerup in self.maze.getPowerups():
      # create new powerup object with random attributes
      newPowerup = Powerup(random.choice(["speed", "score"]), "positive", 2, powerup.x, powerup.y, 10, "cherrypowerup.png")
      self.appendPowerupObjects(newPowerup) # add to attribute of array of powerups

  def playGame(self):

    while self.getRunning():

      self.clock.tick(FRAMESPERSECOND)

      pygame.init()    
      pygame.display.set_caption("PICKMAN")  
      pacman = pygame.image.load('media/pacmandefault.png')
      pygame.display.set_icon(pacman)

      if self.getMusic():
        pass
        #MUSIC.play(12)

      #event handling for ending game, key presses, mouse clicks, arrow key movement
      for event in pygame.event.get(): # check if user has quit
        if event.type == pygame.QUIT:
          self.setState("end program")
        if event.type == pygame.KEYDOWN: # return to menu when "p"
          if event.key == pygame.K_SPACE: # pause/unpause game when space par is pressed 
            if self.getState() == "play":
              self.setState("pause")
            elif self.getState() == "pause":
              self.setState("play")
          if event.key == pygame.K_ESCAPE:
            self.setState(self.getPreviousState())
          if self.getState() == "instructions": # input username
            usertext = usernameButton.text
            if event.key == pygame.K_RETURN: # verify if enter is clicked
              self.verifyUsername()
              usertext = ""
            elif event.key == pygame.K_BACKSPACE: # remove last character when backspace
              usertext = usernameButton.text[0:-1]
            elif event.unicode in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ": # only valid characters entered
              usertext += event.unicode
            usernameButton.text = usertext # update new input 
          elif self.getState() == "play": # detect arrow key movement during game 
            direction = ""
            if event.key == pygame.K_LEFT: # move left
              direction = "left"
            elif event.key == pygame.K_RIGHT: # move right
              direction = "right"
            elif event.key == pygame.K_UP: # move up
              direction = "up"
            elif event.key == pygame.K_DOWN: # move down
              direction = "down"
            if direction in ["left", "right", "up", "down"]: # if player has can move, move and check for collision with pill and increase score
              for x in range(self.player.getSpeed()): # move one place for every unit of speed
                self.player.move(direction, self.maze)
                if self.player.collisions(self.maze) == "pills": # check for collisions after each movement
                  self.setScore(self.getScore() + 1)
                  if len(self.maze.getPills()) == 0:
                    self.setState("game over")
                if self.player.collisions(self.maze) == "powerups": # if player collides with powerup, powerup should affect game 
                  powerupIndex = self.maze.getPowerups().index((self.player.getPosX(), self.player.getPosY())) # find which powerup is being eaten in maze
                  powerupEaten = self.getPowerupObjects()[powerupIndex] # find object vector corresponds to
                  if powerupEaten.getType() == "score": # change score
                    self.setScore(self.getScore() + powerupEaten.getScoreValue()) 
                  elif powerupEaten.getType() == "speed": # change speed
                    self.player.setSpeed(powerupEaten.getSpeedValue())
                  elif powerupEaten.getType() == "mode": # change mode
                    self.player.changeMode()
                  self.maze.removePowerup(powerupIndex) # remove powerup from array so you can't eat it again 
        if event.type == MOUSEBUTTONDOWN:
          if self.getState() != "start-up":
            self.clickButtons()

      # start up screen game state
      if self.getState() == "start-up":
        SCREEN.fill((WHITE))
        for x in range(300):
          uploadImage(random.choice(["redghost.png", "pinkghost.png", "purpleghost.png", "blueghost.png", "pacmandefault.PNG"]),0.5, random.randint(-30,1000), random.randint(-30,600))
        draw_text("PICKMAN", -7, 175, BLACK, 300)
        draw_text("BY INSIYA MULLAMITHA", 320, 400, BLACK, 40)
        pygame.display.flip()
        pygame.time.delay(2500)
        self.setState("menu")

      #menu gamestate
      if self.getState() == "menu": 
        SCREEN.fill((WHITE)) 
        for x in range(5):
          uploadImage(random.choice(["redghost.png", "pinkghost.png", "purpleghost.png", "blueghost.png"]),0.8, random.randint(-30,1000), random.randint(-30,600))
        for button in allButtons[0]:
          button.render()   
        for button in allButtons[1]:
          button.render()
        draw_text("PICKMAN", 0, 0, BLACK, 300)
        draw_text("PICKMAN", -8, 0, BLUE, 300)

      #background music game state
      elif self.getState() == "music":
        SCREEN.fill(WHITE)
        if self.getMusic() == True:
          pass
        else:
          pass
      
      elif self.getState() == "sound":
        SCREEN.fill(WHITE)

      #leaderboard/statistics game state
      elif self.getState() == "stats":
        SCREEN.fill(WHITE)
        draw_text("LEADERBOARD AND STATISTICS", 0, 20, BLACK, 87)
        # statistics methods
      
      #powerups/stars game state
      elif self.getState() == "buy powerups":
        SCREEN.fill(WHITE)
        draw_text("STARS AND POWERUPS", 10, 20, BLACK, 120)
        draw_text("You currently have " + str(self.stars) + " stars", 10, 100, BLACK, 30)

      #help game state
      elif self.getState() == "help":#function displays new screen with help instructions
        SCREEN.fill((WHITE))
        draw_text("HELP", 50, 0, BLACK, 200)
        draw_text("HELP", 45, 0, BLUE, 200 )
        pygame.draw.rect(SCREEN, BLUE, pygame.Rect(50, 125, 900, 425))
        #bullet points of game features 
        draw_text("• Click the play button to begin the game.", 60, 140, BLACK, 30)
        draw_text("• Instructions on how to earn will display just before you start!", 60, 170, BLACK, 30)
        draw_text("• Use the up, down, left and right arrow keys on your keyboard to control movement", 60, 200, BLACK, 30)
        draw_text("• Click on 'Change Character' to change default theme and character image", 60, 230, BLACK, 30)
        draw_text("• Collect stars and use these to buy powerups", 60, 260, BLACK, 30)
        draw_text("• Compete with your friends with the leaderboard feature!", 60, 290, BLACK, 30)

      #change character and theme game state  
      elif self.getState() == "change character":
        SCREEN.fill(WHITE)
        draw_text("CHANGE CHARACTER/THEME", 5, 20, BLACK, 95)
        uploadImage("pacman.PNG", 0.1, 50, 150 )
        uploadImage("jellyfish.PNG", 0.1, 300, 160)


      elif self.getState() == "levels": #function displays levels page
        self.setPreviousState("menu")
        SCREEN.fill(WHITE)
        for button in allButtons[0]:
          button.render()
        for button in allButtons[2]:
          button.render()
        draw_text("LEVELS PAGE", 27, 0, BLACK, 200)
        draw_text("LEVELS PAGE", 22, 0, BLUE, 200)

      #paused game state  
      elif self.getState() == "pause":
        self.setPreviousState("play")
        SCREEN.fill((WHITE))
        draw_text("PAUSED", 0, 0, BLACK, 200)

      elif self.getState() == "instructions": # display instructions for individual level
        self.setPreviousState("levels")
        SCREEN.fill(WHITE)
        for button in allButtons[0]: #display side buttons 
          button.render()
        for star in range(3):# displays stars and instructions for level
          uploadImage('starsymbol.png', 2, 240 + 200*star, 100)
        draw_text("LEVEL " + self.currentLevel + " INSTRUCTIONS", 4, 5, BLACK, 118)
        draw_text("LEVEL " + self.currentLevel + " INSTRUCTIONS", -1, 5, BLUE, 118)
        if self.getLevel() == "1":
          draw_text("kill one ghost", 280, 170, YELLOW, 15)
          draw_text("earn 100 points", 475, 170, YELLOW, 15)
          draw_text("no lives lost", 680, 170, YELLOW, 15)
          self.maze.load_maze(level1Maze)
        self.player.setPosX(self.maze.getPlayer().x)
        self.player.setPosY(self.maze.getPlayer().y)
        for ghost in range(len(self.getGhostObjects())):
          self.ghostObjects[ghost].setPosX(self.maze.getGhosts()[ghost].x)
          self.ghostObjects[ghost].setPosY(self.maze.getGhosts()[ghost].y)
        #display input box for username button
        usernameButton.render()
        draw_text("Enter username below and press enter", 350, 330, BLACK, 20)

      #playing game state
      elif self.getState() == "play":
        self.setPreviousState("pause")
        SCREEN.fill(WHITE)
        draw_text("LEVEL " + self.currentLevel, 2, 5, BLACK, 100)
        draw_text("LEVEL " + self.currentLevel, -3, 5, BLUE, 100)
        for button in allButtons[0]: # display side buttons
          button.render()
        for button in allButtons[3]: # display play state specific buttons
          button.render()
        self.draw_maze()
        self.loadPlayer()
        self.createPowerups()
        #uploadImage(self.ghostObjects[0].getImage(), 0.8, 275+self.ghostObjects[0].getPosX()*30, 65 + self.ghostObjects[0].getPosY()*30)
        #uploadImage(inky.getImage(), 0.8, 275+inky.getPosX()*30, 65 + inky.getPosY()*30)
        #uploadImage(winky.getImage(), 0.8, 275+winky.getPosX()*30, 65 + winky.getPosY()*30)
        draw_text("username: " + self.getUsername(), 10, 150, BLACK, 40)
        draw_text("score: " + str(self.getScore()), 10, 100, BLACK, 40)

      elif self.getState() == "game over":
        self.setPreviousState("menu")
        SCREEN.fill(WHITE)
        draw_text("GAME OVER", 24, 190, BLACK, 225)
        draw_text("GAME OVER", 19, 190, BLUE, 225 )
        for button in allButtons[0]:
          button.render()
        # update statistics text file
        # display number of stars/score/success or fail
        # replay button
        # next level button
        # reset current game statistics
      
      elif self.getState() == "end program":
        SCREEN.fill(BLACK)
        # add animation
        playSoundEffects(LOSINGLIFE)
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()

      pygame.display.update()

game = Game()
game.playGame()
