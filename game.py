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

  def draw_maze(self): # load maze on screen
    for wall in self.maze.getWalls(): # draw walls
      pygame.draw.rect(SCREEN, BLACK, pygame.Rect((275 + (wall.x*30)), 65 + (wall.y*30), 30, 30),0)
    for path in self.maze.getPaths(): # draw white squares representing path
      pygame.draw.rect(SCREEN, WHITE, pygame.Rect((275 + (path.x*30)), 65 + (path.y*30), 30, 30),0)
    for pill in self.maze.getPills(): # draw pills
      pygame.draw.circle(SCREEN, PINK, (289+pill.x*30, 78+pill.y*30), 5, 0)
    for powerup in self.maze.getPowerups(): # powerup objects must be instantiated
      uploadImage(powerup.getImage(), 0.7, 280+powerup.getPosX()*30, 70+powerup.getPosY()*30)
    # draw player 
    uploadImage(self.character, 1, 275+self.player.getPosX()*30, 65 + self.player.getPosY()*30)
    for ghost in self.ghostObjects: # ghost objects must be instantiated
      ghost.move(self.maze) # ghost object move
      uploadImage(ghost.getImage(), 0.8, 275+ghost.getPosX()*30, 65 + ghost.getPosY()*30)
      if ghost.kill(self.player): # if player and ghost collide then handle in ghostCollisions function based on player mode
        pygame.display.flip()
        self.ghostCollisions(ghost)

  def ghostCollisions(self, ghost): # ghost and player collisions
    print("collision")
    if self.player.getMode() == "chased": # if player being chased
      # reset all character positions
      self.player.setPosX(self.player.getStartPosX()) 
      self.player.setPosY(self.player.getStartPosY())
      for ghostObject in self.ghostObjects:
        ghostObject.respawn()
        #ghostObject.setMoving(False)
      # play sound effects and update lives
      playSoundEffects(LOSINGLIFE)
      self.lives -= 1
      if self.lives <= 0:
        self.state = "game over"
      # redraw maze and wait a few seconds before continuing
      ghost.setMoving(False)
      self.draw_maze()
      pygame.display.flip()
      pygame.time.delay(2000)
      ghost.setMoving(True)
    else: # player in kill mode (chasing)
      # reset ghost position and prevent it from moving
      self.score += 30
      ghost.respawn()
      ghost.setMoving(False)

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
                self.draw_maze()
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
                    self.player.changeMode()
                  self.maze.getPowerups().remove(powerupEaten)
        if event.type == MOUSEBUTTONDOWN:
          if self.state != "start-up":
            self.clickButtons()

      # start up screen game state
      if self.state == "start-up":
        SCREEN.fill((WHITE))
        for x in range(300):
          uploadImage(random.choice(["redghost.png", "pinkghost.png", "purpleghost.png", "blueghost.png", "pacmandefault.PNG"]),0.5, random.randint(-30,1000), random.randint(-30,600))
        draw_text("PICKMAN", -7, 175, BLACK, 300)
        draw_text("BY INSIYA MULLAMITHA", 320, 400, BLACK, 40)
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
        draw_text("PICKMAN", 0, 0, BLACK, 300)
        draw_text("PICKMAN", -8, 0, BLUE, 300)

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
        draw_text("LEADERBOARD AND STATISTICS", 0, 20, BLACK, 87)
        # statistics methods
      
      #powerups/stars game state
      elif self.state == "buy powerups":
        SCREEN.fill(WHITE)
        draw_text("STARS AND POWERUPS", 10, 20, BLACK, 120)
        draw_text("You currently have " + str(self.stars) + " stars", 10, 100, BLACK, 30)

      #help game state
      elif self.state == "help":#function displays new screen with help instructions
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
      elif self.state == "change character":
        SCREEN.fill(WHITE)
        draw_text("CHANGE CHARACTER/THEME", 5, 20, BLACK, 95)
        uploadImage("pacman.PNG", 0.1, 50, 150 )
        uploadImage("jellyfish.PNG", 0.1, 300, 160)


      elif self.state == "levels": #function displays levels page
        self.previousState = "menu"
        SCREEN.fill(WHITE)
        for button in allButtons[0]:
          button.render()
        for button in allButtons[2]:
          button.render()
        draw_text("LEVELS PAGE", 27, 0, BLACK, 200)
        draw_text("LEVELS PAGE", 22, 0, BLUE, 200)

      #paused game state  
      elif self.state == "pause":
        self.previousState = "play"
        SCREEN.fill((WHITE))
        draw_text("PAUSED", 0, 0, BLACK, 200)

      elif self.state == "instructions": # display instructions for individual level
        self.previousState = "levels"
        SCREEN.fill(WHITE)
        for button in allButtons[0]: #display side buttons 
          button.render()
        for star in range(3):# displays stars and instructions for level
          uploadImage('starsymbol.png', 2, 240 + 200*star, 100)
        draw_text("LEVEL " + self.currentLevel + " INSTRUCTIONS", 4, 5, BLACK, 118)
        draw_text("LEVEL " + self.currentLevel + " INSTRUCTIONS", -1, 5, BLUE, 118)
        if self.currentLevel == "1":
          draw_text("kill one ghost", 280, 170, YELLOW, 15)
          draw_text("earn 100 points", 475, 170, YELLOW, 15)
          draw_text("no lives lost", 680, 170, YELLOW, 15)
          self.maze.load_maze(level1Maze)
        elif self.currentLevel == "2":
          # level 2 instructions
          self.maze.load_maze(level2Maze)
        self.player.setPosX(self.maze.getPlayer().x)
        self.player.setPosY(self.maze.getPlayer().y)
        self.player.setStartPosX(self.maze.getPlayer().x)
        self.player.setStartPosY(self.maze.getPlayer().y)
        for ghost in range(len(self.ghostObjects)):
          self.ghostObjects[ghost].setPosX(self.maze.getGhosts()[ghost].x)
          self.ghostObjects[ghost].setPosY(self.maze.getGhosts()[ghost].y)
          self.ghostObjects[ghost].setStartPosX(self.maze.getGhosts()[ghost].x)
          self.ghostObjects[ghost].setStartPosY(self.maze.getGhosts()[ghost].y)
        #display input box for username button
        usernameButton.render()
        draw_text("Enter username below and press enter", 350, 330, BLACK, 20)

      #playing game state
      elif self.state == "play":
        self.previousState = "pause"
        SCREEN.fill(WHITE)
        draw_text("LEVEL " + self.currentLevel, 2, 5, BLACK, 100)
        draw_text("LEVEL " + self.currentLevel, -3, 5, BLUE, 100)
        for button in allButtons[0]: # display side buttons
          button.render()
        for button in allButtons[3]: # display play state specific buttons
          button.render()
        self.draw_maze()
        draw_text("username: " + self.username, 10, 150, BLACK, 40)
        draw_text("score: " + str(self.score), 10, 100, BLACK, 40)

      elif self.state == "game over":
        self.previousState = "menu"
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
