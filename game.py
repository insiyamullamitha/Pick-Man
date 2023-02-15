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
    self.player = Player(0, None, None)
    self.ghostObjects = [blinky, inky, winky]
    self.maze = Maze()
    self.stars = 0
    self.instructions = []

  def drawMaze(self): # load maze on screen
    for wall in self.maze.getWalls(): # draw walls
      pygame.draw.rect(SCREEN, BLACK, pygame.Rect((250 + (wall.x*30)), 65 + (wall.y*30), 30, 30),0)
    for path in self.maze.getPaths(): # draw white squares representing path
      pygame.draw.rect(SCREEN, WHITE, pygame.Rect((250 + (path.x*30)), 65 + (path.y*30), 30, 30),0)
    for pill in self.maze.getPills(): # draw pills
      pygame.draw.circle(SCREEN, PINK, (264+pill.x*30, 78+pill.y*30), 5, 0)
    for powerup in self.maze.getPowerups(): # powerup objects must be instantiated
      uploadImage(powerup.getImage(), 0.7, 255+powerup.getPosX()*30, 70+powerup.getPosY()*30)
    # draw player 
    uploadImage(self.character, 1, 250+self.player.getPosX()*30, 65 + self.player.getPosY()*30, self.player.getRotate())
    for ghost in self.ghostObjects: # ghost objects must be instantiated
      ghost.move(self.maze) # ghost object move
      uploadImage(ghost.getImage(), 0.8, 250+ghost.getPosX()*30, 65 + ghost.getPosY()*30)
      if ghost.kill(self.player): # if player and ghost collide then handle in ghostCollisions function based on player mode
        pygame.display.flip()
        self.ghostCollisions(ghost)

  def ghostCollisions(self, ghost): # ghost and player collisions
    if self.player.getMode() == "chased": # if player being chased
      # reset all character positions
      self.player.resetPosition()
      for ghostObject in self.ghostObjects:
        ghostObject.respawn()
        #ghostObject.setMoving(False)
      # play sound effects and update lives
      playSoundEffects(LOSINGLIFE)
      self.lives -= 1 
      self.drawMaze()
      if self.lives <= 0:
        self.state = "game over"
      # redraw maze and wait a few seconds before continuing
      else:
        ghost.setMoving(False)
        self.drawMaze()
        pygame.display.flip()
        pygame.time.delay(2000)
        ghost.setMoving(True)
    
    else: # player in kill mode (chasing)
      # reset ghost position and prevent it from moving
      self.player.setMode("chased")
      self.character = "pacmandefault.png"
      self.score += 30
      ghost.respawn()
      ghost.setMoving(False)

  def displayLives(self): # display number of lives using red/empty hearts during game
    for x in range(self.lives): # display red hearts for lives still remaining 
      uploadImage("fulllife.png", 0.7, 35 + x * 70, 150)
    if self.lives < 3: # if less than 3 lives display an empty heart representing life 3
      uploadImage("emptylife.png", 0.7, 175, 150)
    if self.lives < 2: # if less than 2 hearts display an empty heart representing life 2
      uploadImage("emptylife.png", 0.7, 105, 150)

  def updateStars(self): # change star status if instruction has been completed
    match self.currentLevel:
      case "1": # instructions for level 1
        if self.instructions[2][0] != 1 and self.score >= 300:
          self.instructions[2][0] = 1
          self.stars += 1
        elif self.instructions[1][0] != 1 and self.score >= 200:
          self.instructions[1][0] = 1
          self.stars += 1
        elif self.instructions[0][0] != 1 and self.score >= 100:
          self.instructions[0][0] = 1
          self.stars += 1

  def displayGameStars(self): # displays stars and instructions during game
    self.updateStars()
    for instruction in self.instructions:
      # determine whether star has been achieved or not and accordingly load empty/yellow star
      image = "emptystar.png"
      if instruction[0] == 1:
        image = "yellowstar.png"
      # display star and its instruction next to it
      uploadImage(image, 0.08, 20, 200 + self.instructions.index(instruction)*100)
      drawText(instruction[1], 115, 240 + self.instructions.index(instruction) * 100, BLACK, 20 )

  def clickButtons(self):# detects whether button has been clicked and changes game state
    # if any button on the screen has been clicked change game state 
    for buttons in allButtons:
      for button in buttons:
        if button.click() != None:
          if button in allButtons[1] and self.state != "menu":
            return
          if button in allButtons[2] and self.state == "levels":
            self.currentLevel = button.text
          if button in allButtons[2] and self.state != "levels":
            return
          if button in allButtons[3] and self.state != "play":
            return
          self.previousState = self.state
          self.state = button.newState
          SCREEN.fill(WHITE)
  
  # check that username is between 3 and 10 characters and save as game username
  def verifyUsername(self):
    if len(usernameButton.text) > 2 and len(usernameButton.text) < 11:
      self.state = "play"
      self.username = usernameButton.text.upper()

  def playGame(self):

    while self.running:

      self.clock.tick(FRAMESPERSECOND)

      pygame.init()    
      pygame.display.set_caption("PICKMAN")  
      pacman = pygame.image.load('media/pacmandefault.png')
      pygame.display.set_icon(pacman)

      if self.music:
        pass
        #MUSIC.play(12)

      #event handling for ending game, key presses, mouse clicks, arrow key movement
      for event in pygame.event.get(): # check if user has quit
        if event.type == pygame.QUIT:
          self.state = "end program"
        if event.type == pygame.KEYDOWN: # return to menu when "p"
          if event.key == pygame.K_SPACE: # pause/unpause game when space par is pressed 
            if self.state == "play":
              self.state = "pause"
            elif self.state == "pause":
              self.state = "play"
          if event.key == pygame.K_ESCAPE:
            self.state = self.previousState
          if self.state == "instructions": # input username
            usertext = usernameButton.text
            if event.key == pygame.K_RETURN: # verify if enter is clicked
              self.verifyUsername()
              usertext = ""
            elif event.key == pygame.K_BACKSPACE: # remove last character when backspace
              usertext = usernameButton.text[0:-1]
            elif event.unicode in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ": # only valid characters entered
              usertext += event.unicode
            usernameButton.text = usertext # update new input 
          elif self.state == "play": # detect arrow key movement during game 
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
                self.drawMaze()
                pygame.display.flip()
                if self.player.collisions(self.maze) == "pills": # check for collisions after each movement
                  self.score += 1
                  if len(self.maze.getPills()) == 0:
                    self.state = "game over"
                if self.player.collisions(self.maze) == "powerups": # if player collides with powerup, powerup should affect game 
                  found = False
                  while not found:
                    for powerup in self.maze.getPowerups():
                      if powerup.getPosX() == self.player.getPosX() and powerup.getPosY() == self.player.getPosY():
                        powerupEaten = powerup
                        found = True
                  if powerupEaten.getType() == "score": # change score
                    self.score += powerupEaten.getScoreValue()
                  elif powerupEaten.getType() == "speed": # change speed
                    self.player.setSpeed(powerupEaten.getSpeedValue())
                  elif powerupEaten.getType() == "mode": # change mode
                    self.player.setMode("chasing")
                    self.character = "bluepacmandefault.png"
                  self.maze.getPowerups().remove(powerupEaten)
        if event.type == MOUSEBUTTONDOWN:
          if self.state != "start-up":
            self.clickButtons()

      # start up screen game state
      if self.state == "start-up":
        SCREEN.fill((WHITE))
        for x in range(300):
          uploadImage(random.choice(["redghost.png", "pinkghost.png", "purpleghost.png", "blueghost.png", "pacmandefault.PNG"]),0.5, random.randint(-30,1000), random.randint(-30,600))
        drawText("PICKMAN", -7, 175, BLACK, 300)
        drawText("BY INSIYA MULLAMITHA", 320, 400, BLACK, 40)
        pygame.display.flip()
        pygame.time.delay(2500)
        self.state = "menu"

      #menu gamestate
      if self.state == "menu": 
        SCREEN.fill((WHITE)) 
        for x in range(5):
          uploadImage(random.choice(["redghost.png", "pinkghost.png", "purpleghost.png", "blueghost.png"]),0.8, random.randint(-30,1000), random.randint(-30,600))
        for button in allButtons[0]:
          button.render()   
        for button in allButtons[1]:
          button.render()
        drawText("PICKMAN", 0, 0, BLACK, 300)
        drawText("PICKMAN", -8, 0, BLUE, 300)

      #background music game state
      elif self.state == "music":
        SCREEN.fill(WHITE)
        if self.music == True:
          pass
        else:
          pass
      
      elif self.state == "sound":
        SCREEN.fill(WHITE)

      #leaderboard/statistics game state
      elif self.state == "stats":
        SCREEN.fill(WHITE)
        drawText("LEADERBOARD AND STATISTICS", 0, 20, BLACK, 87)
        # statistics methods
      
      #powerups/stars game state
      elif self.state == "buy powerups":
        SCREEN.fill(WHITE)
        drawText("STARS AND POWERUPS", 10, 20, BLACK, 120)
        drawText("You currently have " + str(self.stars) + " stars", 10, 100, BLACK, 30)

      #help game state
      elif self.state == "help":#function displays new screen with help instructions
        SCREEN.fill((WHITE))
        drawText("HELP", 50, 0, BLACK, 200)
        drawText("HELP", 45, 0, BLUE, 200 )
        pygame.draw.rect(SCREEN, BLUE, pygame.Rect(50, 125, 900, 425))
        #bullet points of game features 
        drawText("• Click the play button to begin the game.", 60, 140, BLACK, 30)
        drawText("• Instructions on how to earn will display just before you start!", 60, 170, BLACK, 30)
        drawText("• Use the up, down, left and right arrow keys on your keyboard to control movement", 60, 200, BLACK, 30)
        drawText("• Click on 'Change Character' to change default theme and character image", 60, 230, BLACK, 30)
        drawText("• Collect stars and use these to buy powerups", 60, 260, BLACK, 30)
        drawText("• Compete with your friends with the leaderboard feature!", 60, 290, BLACK, 30)

      #change character and theme game state  
      elif self.state == "change character":
        SCREEN.fill(WHITE)
        drawText("CHANGE CHARACTER/THEME", 5, 20, BLACK, 95)
        uploadImage("pacman.PNG", 0.1, 50, 150 )
        uploadImage("jellyfish.PNG", 0.1, 300, 160)

      elif self.state == "levels": #displays levels page
        self.previousState = "menu" # return to menu if escape key is pressed
        SCREEN.fill(WHITE)
        for button in allButtons[0]: # display side buttons
          button.render()
        for button in allButtons[2]: # display level number
          button.render()
          level = int(button.text)
          with open ("levelStarsInstructions.txt") as file: # for each level find number of stars
            lines = file.readlines()
            startLine = level * 3 - 3
            stars = int(lines[startLine][0]) + int(lines[startLine + 1][0]) + int(lines[startLine + 2][0])
            for star in range(stars): # display number of stars below level
              uploadImage("yellowstar.png", 0.02, 30 * star + button.x - 35, button.y + 40)

        drawText("LEVELS PAGE", 27, 0, BLACK, 200)
        drawText("LEVELS PAGE", 22, 0, BLUE, 200)

      elif self.state == "instructions": # display instructions for individual level
        self.previousState = "levels"
        SCREEN.fill(WHITE)
        for button in allButtons[0]: #display side buttons 
          button.render()
        drawText("LEVEL " + self.currentLevel + " INSTRUCTIONS", 4, 5, BLACK, 118)
        drawText("LEVEL " + self.currentLevel + " INSTRUCTIONS", -1, 5, BLUE, 118)
        uploadImage("pacmandefault.png", 1.5, 10, 215)
        for x in range(6):
          pygame.draw.circle(SCREEN, PINK, (60 + x*40, 235), 7.5, 0)
        for x in range(8):
          pygame.draw.circle(SCREEN, PINK, (740 + x*40, 235), 7.5, 0)
        with open ("levelStarsInstructions.txt") as file: # find instructions for level and store in array
          lines = file.readlines()
          startInstruction = int(self.currentLevel) * 3 - 3
          # update self.instructions with star status of zero (at the start of the game) and type of instruction
          self.instructions = [[0, lines[startInstruction][1:].strip('\n')],
                              [0, lines[startInstruction + 1][1:].strip('\n')], 
                              [0, lines[startInstruction + 2][1:].strip('\n')]]
        # display each instruction and star
        for instruction in range(3):
          uploadImage("emptystar.png", 0.1, 250 + 200*instruction, 170)
          drawText(self.instructions[instruction][1], 262 + instruction * 200, 290, BLACK, 15)
        if self.currentLevel == "1": # load level 1 maze 
          self.maze.loadMaze(level1Maze)
        elif self.currentLevel == "2": # load level 2 maze
          # level 2 instructions
          self.maze.loadMaze(level2Maze)
        # set initial coordinates for player
        self.player.setPosX(self.maze.getPlayer().x) 
        self.player.setPosY(self.maze.getPlayer().y)
        self.player.setStartPosX(self.maze.getPlayer().x)
        self.player.setStartPosY(self.maze.getPlayer().y)
        # set initial coordinates for each ghost
        for ghost in range(len(self.ghostObjects)):
          self.ghostObjects[ghost].setPosX(self.maze.getGhosts()[ghost].x)
          self.ghostObjects[ghost].setPosY(self.maze.getGhosts()[ghost].y)
          self.ghostObjects[ghost].setStartPosX(self.maze.getGhosts()[ghost].x)
          self.ghostObjects[ghost].setStartPosY(self.maze.getGhosts()[ghost].y)
        #display input box for username button
        usernameButton.render()
        drawText("Enter username below and press enter", 350, 350, BLACK, 20)

      #playing game state
      elif self.state == "play":
        self.previousState = "pause"
        SCREEN.fill(WHITE)
        drawText("LEVEL " + self.currentLevel, 2, 5, BLACK, 100)
        drawText("LEVEL " + self.currentLevel, -3, 5, BLUE, 100)
        for x in range(18):
          pygame.draw.circle(SCREEN, PINK, (300+ x*40, 35), 7.5, 0)
        for button in allButtons[0]: # display side buttons
          button.render()
        for button in allButtons[3]: # display play state specific buttons
          button.render()
        self.drawMaze()
        self.displayGameStars()
        self.displayLives()
        pygame.draw.rect(SCREEN, GREEN, pygame.Rect(50, 90, 150, 40), 0, 3)
        drawText("score: " + str(self.score), 55, 95, BLACK, 40)
      
      #paused game state  
      elif self.state == "pause":
        self.previousState = "play"
        SCREEN.fill((WHITE))
        drawText("PAUSED", 0, 0, BLACK, 200)

      elif self.state == "game over":
        self.previousState = "menu"
        SCREEN.fill(WHITE)
        drawText("GAME OVER", 24, 190, BLACK, 225)
        drawText("GAME OVER", 19, 190, BLUE, 225 )
        for button in allButtons[0]:
          button.render()
        # update statistics text file
        # display number of stars/score/success or fail
        # replay button
        # next level button
        # reset current game statistics
      
      elif self.state == "end program":
        SCREEN.fill(BLACK)
        # add animation
        playSoundEffects(LOSINGLIFE)
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()

      pygame.display.update()

game = Game()
game.playGame()
