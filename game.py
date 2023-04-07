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
    self.playingGame = False
    self.clock = pygame.time.Clock()
    self.score = 0
    self.soundEffects = False
    self.stars = 0
    self.lives = 3
    self.time = [0, 0]
    self.startTime = 0
    self.currentLevel = None
    self.theme = 0
    self.username = ""
    self.player = Player(0, None, None)
    self.ghostObjects = [blinky, inky, winky]
    self.maze = Maze()
    self.stars = 0
    self.instructions = []
    self.extraPowerups = 0

  def drawMaze(self): 
    # load maze and all maze objects on screen
    for wall in self.maze.getWalls(): # draw walls
      pygame.draw.rect(SCREEN, BLACK[self.theme], pygame.Rect((250 + (wall.x*30)), 65 + (wall.y*30), 30, 30),0)
    for path in self.maze.getPaths(): # draw white squares representing path
      pygame.draw.rect(SCREEN, WHITE[self.theme], pygame.Rect((250 + (path.x*30)), 65 + (path.y*30), 30, 30),0)
    for pill in self.maze.getPills(): # draw pills
      pygame.draw.circle(SCREEN, PINK[self.theme], (264+pill.x*30, 78+pill.y*30), 5, 0)
      pygame.draw.circle(SCREEN, BLACK[self.theme], (264+pill.x*30, 78+pill.y*30), 5, 1)
    for powerup in self.maze.getPowerups(): # powerup objects must be instantiated
      uploadImage(powerup.getImage(), 1/7, 252+powerup.getPosX()*30, 68+powerup.getPosY()*30)
    # draw player after updating its position
    self.player.move(self)
    uploadImage(self.player.getImage(), 1/6, 250+self.player.getPosX()*30, 65 + self.player.getPosY()*30, self.player.getRotate())
    # draw ghosts after updating their positions
    for ghost in self.ghostObjects: 
      ghost.move(self) 
      uploadImage(ghost.getImage(), 1/6, 250+ghost.getPosX()*30, 65 + ghost.getPosY()*30)
    pygame.display.flip()
    # check for collisions between player and other maze objects
    collided = self.player.checkForCollisions(self)
    if collided != (None, None):
      self.handleCollisionEffects((collided))

  def handleCollisionEffects(self, collisionObject):
    # check what type of collision has occurred and accordingly make changes to maze/score/lives/mode
    soundEffect = None

    # pill collision
    if collisionObject[0] == "pill":
      # remove pill collided with from pill array
      pillPosition = collisionObject[1]
      self.maze.getPills().remove(pillPosition)
      # play sound effect
      if self.soundEffects:
        playSoundEffect(PILLSOUND)
      # increase score
      self.score += 1
    # powerup collision

    if collisionObject[0] == "powerup":
      # find specific powerup collided with
      powerup = collisionObject[1]
      # remove powerup from array
      self.maze.getPowerups().remove(powerup)
      # visually display type of powerup to user
      self.displayPowerupAlert(powerup)
      # play sound effect
      if self.soundEffects:
        playSoundEffect(POWERUPSOUND)
      # determine type of powerup and accordingly adjust game/player values
      if powerup.getType() == "score": # increase score
        game.score += powerup.getScoreValue()
      elif powerup.getType() == "speed": # change player speed
        self.player.setSpeed(powerup.getSpeedValue())
        # make sure player is in viable maze position so it doesn't end up in a wall
        self.player.setPosX(powerup.getPosX())
        self.player.setPosY(powerup.getPosY())
      else: # change player mode
        self.player.setMode("chasing")

    # ghost collision
    if collisionObject[0] == "ghost":
      # reset player and ghost positions
      self.player.resetPosition()
      for ghostObject in self.ghostObjects:
        ghostObject.respawn()
      # if player is in chase mode reduce number of lives
      if self.player.getMode() == "chased":
        soundEffect = LOSINGLIFESOUND
        self.lives -= 1
      # if player is in chasing/kill mode increase score and reset mode
      else:
        soundEffect = KILLGHOSTSOUND
        self.player.setMode("chased")
        self.score += 30
      # play sound effects
      if self.soundEffects:
        playSoundEffect(soundEffect)
      pygame.time.delay(3000)

  def checkGameOver(self):
    # check if player has lost all lives or eaten all pills and powerups (game over)
    if self.lives <= 0 or (len(self.maze.getPills()) == 0 and len(self.maze.getPowerups()) == 0):
      self.beginGameOver()
    return

  def loadInstructions(self):
    # load instructions for particular level from text file 
    with open ("levelStarsInstructions.txt") as file: # open file containing instructions
      # read all lines in file and store in lines 
      lines = file.readlines() 
      # find line from which instructions start using level number
      startInstruction = int(self.currentLevel) * 3 - 3 
      # update self.instructions with star status of zero (at the start of the game) and type of instruction
      self.instructions = [[0, lines[startInstruction][1:].strip('\n')],
                          [0, lines[startInstruction + 1][1:].strip('\n')], 
                          [0, lines[startInstruction + 2][1:].strip('\n')]]
      # display instructions on screen
      self.displayInstructions()

  def resetGameStatistics(self):
    # reset game statistics ready for the new game
    self.score = 0
    self.stars = 0
    self.lives = 3

  def displayInstructions(self):
    # display instructions and matching star status on screen
    for x in range(25): # draw pill circles around stars (visual purpose)
      if x not in[6, 11, 16]:
        pygame.draw.circle(SCREEN, PINK[self.theme], (55 + x*40, 235), 7.5, 0)
        pygame.draw.circle(SCREEN, BLACK[self.theme], (55 + x*40, 235), 7.5, 1)
    # display each instruction and star#
    for instruction in range(3):
      # change star image from clear to yellow depending on star status (default empty)
      image = "emptystar.png" 
      if self.instructions[instruction][0] == 1:
        image = "yellowstar.png"
      uploadImage(image, 0.1, 245 + 200*instruction, 170)
      # draw instruction under star
      drawText(self.instructions[instruction][1], 260 + instruction * 200, 290, BLACK, 15, self.theme)
      # draw player image on side of screen (visual purpose)
      uploadImage(self.player.getImage(), 0.25, 3, 215)

  def beginGameOver(self):
    # update new star statuses and game statistics
    self.state = "game over"
    if self.soundEffects:
      if self.lives == 0:
        playSoundEffect(LOSINGLIFESOUND)
      else:
        playSoundEffect(STARSOUND)
    # update stars that the user has achieved to the text file
    for instruction in range(len(self.instructions)):
      # check if player has achieved task that completes at the end of the game
      self.updateStars()
      if self.instructions[instruction][0] == 1:
        self.updateFileStarStatus(instruction)
    # update all game statistics (stars, leaderboard)
    stats.updateStatistics(self.stars, self.score, self.username)

  # visually display powerup function to user
  def displayPowerupAlert(self, powerup):
    # display number of points awarded
    if powerup.getType() == "score":
      pygame.draw.circle(SCREEN, PINK[self.theme], (265 + powerup.getPosX() * 30, 80 + powerup.getPosY()*30), 15, 0)
      pygame.draw.circle(SCREEN, BLACK[self.theme], (265 + powerup.getPosX() * 30, 80 + powerup.getPosY()*30), 15, 1)
      drawText("+ " + str(powerup.getScoreValue()), 256 + powerup.getPosX()*30, 78 + powerup.getPosY()*30, BLACK, 15, self.theme)
    # display speed multiplier
    elif powerup.getType() == "speed":
      pygame.draw.circle(SCREEN, BLACK[self.theme], (265 + powerup.getPosX() * 30, 80 + powerup.getPosY()*30), 15, 0)
      drawText("2X", 256 + powerup.getPosX()*30, 78 + powerup.getPosY()*30, WHITE, 15)
    # display skull representing kill modeS
    else:
      uploadImage("skull.png", 1/6, 250 + powerup.getPosX() * 30, 65 + powerup.getPosY() * 30)
    pygame.display.flip()
    pygame.time.delay(1000)


  def setupMazeAndObjects(self):
    # load correct level maze
    if self.currentLevel == "1":
      mazeLayout = level1Maze
    elif self.currentLevel == "2":
      mazeLayout = level2Maze
    self.maze.loadMaze(mazeLayout, self.theme)
    # set initial coordinates for player
    self.player.setUpInitialPosition(self.maze.getPlayer().x, self.maze.getPlayer().y)
    # set initial coordinates for each ghost
    for g, ghost in enumerate(self.ghostObjects):
      ghost.setUpInitialPosition(self.maze.getGhosts()[g].x, self.maze.getGhosts()[g].y)

  def displayLives(self): # display number of lives using red/empty hearts during game
    for x in range(self.lives): # display red hearts for lives still remaining 
      uploadImage("fulllife.png", 0.7, 35 + x * 70, 150)
    if self.lives < 3: # if less than 3 lives display an empty heart representing life 3
      uploadImage("emptylife.png", 0.7, 175, 150)
    if self.lives < 2: # if less than 2 hearts display an empty heart representing life 2
      uploadImage("emptylife.png", 0.7, 105, 150)

  def updateStars(self): 
    # change star status if instruction has been completed depending on particular level
    increaseStars = False
    # level 1
    if self.currentLevel == "1":
       # win 50 points
      if self.instructions[0][0] != 1 and self.score >= 50:
        self.instructions[0][0] = 1
        increaseStars = True
      # win 100 points
      if self.instructions[1][0] != 1 and self.score >= 100:
        self.instructions[1][0] = 1
        increaseStars = True
      # win 160 points
      if self.instructions[2][0] != 1 and self.score >= 150:
        self.instructions[2][0] = 1
        increaseStars = True 
    # increase number of stars and play sound effect
    if increaseStars:
      self.stars += 1
      if self.soundEffects:
        playSoundEffect(STARSOUND)

  def changeSoundSettings(self): 
    # toggle sound effect settings and change sound effect button image to represent state
    if self.soundEffects:
      self.soundEffects = False
      soundButton.image = "soundoffsymbol.png"
    else:
      self.soundEffects = True
      soundButton.image = "soundsymbol.png"
    self.state = self.previousState

  def updateFileStarStatus(self, instructionNumber): 
    # update particular instruction star that has been achieved at the end of the level
    startInstruction = int(self.currentLevel) * 3 - 3 # find the line from which the level's instructions start
    file = open("levelStarsInstructions.txt", "r")
    lines = file.readlines() # read instructions from file and store in lines
    lines[startInstruction + instructionNumber] = "1" + self.instructions[instructionNumber][1] + "\n" #change 0 to 1 to represent achieved
    stats.updateFile(lines, "levelStarsInstructions.txt")#update file
     
  def displayGameStars(self): 
    # displays stars and instructions during game
    self.updateStars() # update stars achieved
    for instruction in self.instructions:
      # determine whether star has been achieved or not and accordingly load empty/yellow star
      image = "emptystar.png"
      if instruction[0] == 1:
        image = "yellowstar.png"
      # display star and its instruction next to it
      uploadImage(image, 0.08, 20, 200 + self.instructions.index(instruction)*100)
      drawText(instruction[1], 115, 240 + self.instructions.index(instruction) * 100, BLACK, 20, self.theme)

  def changeTheme(self, givenTheme):
    # change theme to theme selected by user and change game state to character
    self.theme = givenTheme
    self.state = "change character"
    self.previousState = "change theme"
    # check if the user has a matching theme and character
    matchingCharacterAndTheme = False
    for characters in allCharacters[self.theme]:
      # if user has character from theme chosen then all good
      if self.player.getImage() == characters[0]:
        matchingCharacterAndTheme = True
    # if not, set the player image to the default character from the theme chosen to keep everything matching
    if not matchingCharacterAndTheme:
      self.changeCharacter(0)

  def addExtraPowerups(self):
    # place additional powerups user has chosen to implement in maze
    for powerup in range(self.extraPowerups):
      self.maze.addPowerup(self.theme)
    # update user's number of remaining powerups 
    stats.changePowerups(-self.extraPowerups)
    self.extraPowerups = 0

  def changeCharacter(self, givenCharacter):
    # change character
    self.player.setImage(allCharacters[self.theme][givenCharacter][0])
    # change ghosts images depending on character chosen
    for ghost in range(len(self.ghostObjects)):
      self.ghostObjects[ghost].setImage(allCharacters[self.theme][givenCharacter][ghost + 1])
    self.player.setRotate(0)

  def clickButtons(self):# detects whether button has been clicked and changes game state
    # if any button on the screen has been clicked change game state 
    for buttons in allButtons:
      for button in buttons:
        if button.click() != None:
          # side buttons only clicked in certain states
          if button in allButtons[0] and self.state not in ["menu", "levels", "instructions", "play", "game over", "pause"]:
            return
          # change character and play button only available in menu
          if button in allButtons[1] and self.state != "menu":
            return
          # level buttons only available in levels game state
          if button in allButtons[2]:
            if self.state == "levels":
              self.currentLevel = button.text
            else:
              return
          if button in allButtons[3] and self.state != "play":
            return
          if button == replayButton and self.state in ["game over", "pause"]:
            pass
          elif button in allButtons[4] and self.state != "pause":
            if button == returnHomeButton and self.state == "game over":
              button = nextLevelButton
            else:
              return
          elif button in allButtons[5] and self.state != "game over":
            if button == nextLevelButton and self.state == "pause":
              button = returnHomeButton
            else:
              return
          # change game state
          self.previousState = self.state
          self.state = button.newState
          if self.state == "play":
            self.playingGame = True
          # increase level if next level button and set up new maze
          elif self.state == "instructions":
            if button == nextLevelButton:
              # cast level number into integer, increment, and cast into string again
              self.currentLevel = str(int(self.currentLevel) + 1)
            self.setupMazeAndObjects()
            self.resetGameStatistics()
            usernameButton.text = ""
            self.extraPowerups = 0
          elif self.state == "sound":
            self.changeSoundSettings()
   
  def buyPowerup(self):
    # check if user has enough stars to buy powerup
    if stats.getNumberOfStars() >= 100:
      # reduce number of remaining stars
      stats.changeNumberOfStars(-100)
      # increase user's number of extra powerups
      stats.changePowerups(1)

  def displayLeaderboard(self): # draw leaderboard table and other stats
    # draw table
    SCREEN.fill((WHITE[self.theme]))
    drawText("LEADERBOARD AND STATISTICS", 2, 25, BLACK, 88, self.theme)
    drawText("LEADERBOARD AND STATISTICS", 2, 20, BLUE, 88, self.theme)
    pygame.draw.rect(SCREEN, LIGHTBLUE[self.theme], pygame.Rect(100, 135, 800, 305), 0, 3)
    pygame.draw.rect(SCREEN, BLACK[self.theme], pygame.Rect(100, 135, 800, 305), 1, 3)
    for x in range(5):
      pygame.draw.line(SCREEN, BLACK[self.theme], (100, 50 * x + 190), (900, 50 * x + 190))
    for x in range(2):
      pygame.draw.line(SCREEN, BLACK[self.theme], (300 + x * 400, 135), (300 + x * 400, 440))
    # table headers
    drawText("RANK", 140, 145, BLACK, 50, self.theme)
    drawText("PLAYER", 420, 145, BLACK, 50, self.theme)
    drawText("SCORE", 745, 145, BLACK, 50, self.theme)
    # draw each leader's username and score
    for leader in range(len(stats.getLeaderboard())):
      drawText(leader+1, 180, leader*50 + 200, BLACK, 50, self.theme)
      drawText(stats.getLeaderboard()[leader][1], 427, leader * 50 + 200, BLACK, 50, self.theme)
      drawText(stats.getLeaderboard()[leader][0], 770, leader * 50 + 200, BLACK, 50, self.theme)
    # upload star image and number of total stars
    uploadImage("yellowstar.png", 0.08, 100, 470)
    drawText(stats.getNumberOfStars(), 200, 500, BLACK, 40, self.theme)
    # draw text for fastest time
    drawText("FASTEST TIME: " + str(stats.getFastestTime()) + " SECONDS", 450, 500, BLACK, 40, self.theme)
  
  def setUsername(self, event):
    # update user's chosen username for the game using keyboard input
    if event.key == pygame.K_RETURN: # return = enter
      self.verifyUsername() # check if user's password meets the criteria and begin game
      usernameButton.text = "" 
    elif event.key == pygame.K_BACKSPACE: # backspace = delete last character
      usernameButton.text = usernameButton.text[0:-1]
    elif event.unicode in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ": # only letters allowed to be entered
      usernameButton.text += event.unicode # update username

  # check that username is between 3 and 10 characters and save as game username, enter play game state
  def verifyUsername(self):
    if len(usernameButton.text) > 2 and len(usernameButton.text) < 11: # length check
      self.state = "play" # start play state
      self.username = usernameButton.text.upper()
      self.addExtraPowerups() # implement extra powerups user has chosen to add


  def playGame(self):

    while self.running:

      self.clock.tick(FRAMESPERSECOND)  

      #event handling for ending game, key presses, mouse clicks, arrow key movement
      for event in pygame.event.get(): # check if user has quit
        if event.type == pygame.QUIT:
          self.state = "end program"
        if event.type == pygame.KEYDOWN: # return to menu when "p"
          if event.key == pygame.K_SPACE: # pause/unpause game when space par is pressed 
            if self.state == "play":
              self.state = "pause"
              self.playingGame = False
            elif self.state == "pause":
              self.state = "play"
              self.startTime = pygame.time.get_ticks()
              self.playingGame = True
          if event.key == pygame.K_ESCAPE:
            self.state = self.previousState
          if self.state == "instructions": # input username
            self.setUsername(event)
          if self.state == "play":
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]:
              self.player.setDirection(event.key)
        if event.type == MOUSEBUTTONDOWN:
          posX, posY = pygame.mouse.get_pos()
          clicked = False
          if self.state == "change theme":
            # check if user has decided to change theme
            if posY >= 120 and posY <= 520:
              # bright theme = theme 0
              if posX >= 85 and posX <= 489:
                self.changeTheme(0)
                clicked = True
              # ocean theme = theme 1
              elif posX >= 515 and posX <= 919:
                self.changeTheme(1)
                clicked = True
          elif self.state == "change character":
            # change character if image is clicked
            if posY >= 210 and posY <= 390:
              for x in range(3):
                if posX >= (90 + x*300) and posX <= (270 + x*300):
                  self.changeCharacter(x) 
                  clicked = True        
            if posX >= 380 and posX <= 630 and posY >= 460 and posY <= 510:
              self.state = "menu"
              clicked = True
          elif self.state == "buy powerups":
            if posX >= 620 and posX <= 820 and posY >= 285 and posY <= 335 and self.previousState != "pause":
              # update number of stars and increase extra powerups
              self.buyPowerup()
              clicked = True
          elif self.state == "instructions":
            # check if user has clicked on reduce number of extra powerups button and reduce powerups
            if SCREEN.get_at((posX, posY)) == RED:
              self.extraPowerups -= 1
              clicked = True
            # check if user has clicked on increase number of extra powerups button and increase powerups
            elif SCREEN.get_at((posX, posY)) == GREEN[self.theme]:
              self.extraPowerups += 1
              clicked = True
          # user cannot click on buttons during game load-up
          if self.state != "start-up" and not clicked:
            self.clickButtons()
        # change player direction to None when they are not pressing on an arrow key to allow continuous movement
        if event.type == pygame.KEYUP:
          if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP]:
            self.player.setDirection(None)

      # start up screen game state
      if self.state == "start-up":
        SCREEN.fill((WHITE[self.theme]))
        # random ghosts background
        for x in range(300):
          uploadImage(random.choice(["redghost.png", "purpleghost.png", "blueghost.png"]),0.1, random.randint(-30,1000), random.randint(-30,600))
        # game title and credits
        drawText("PICKMAN", 0, 175, BLACK, 300, self.theme)
        drawText("PICKMAN", -8, 175, BLUE, 300, self.theme)
        drawText("BY INSIYA MULLAMITHA", 320, 400, BLACK, 40, self.theme)
        pygame.display.flip() 
        # load page for 2000ms as a start-up screen before moving on to menu
        pygame.time.delay(2000)
        self.state = "menu"

      #menu gamestate
      if self.state == "menu": 
        self.previousState = "menu"
        SCREEN.fill((WHITE[self.theme])) 
        # display ghosts specific to theme and character chosen and keep updating 
        ghostImages = []
        for ghost in self.ghostObjects:
          ghostImages.append(ghost.getImage())
        for x in range(5):
          uploadImage(random.choice(ghostImages),0.15, random.randint(-30,1000), random.randint(-30,600))
        # display side buttons
        for button in allButtons[0]:
          button.render(self.theme)
        # display change character/ play button
        for button in allButtons[1]:
          button.render(self.theme)
        # title
        drawText("PICKMAN", 0, 0, BLACK, 300, self.theme)
        drawText("PICKMAN", -8, 0, BLUE, 300, self.theme)

      #leaderboard/statistics game state
      elif self.state == "stats":
        SCREEN.fill((WHITE[self.theme]))
        # title
        drawText("LEADERBOARD AND STATISTICS", 2, 20, BLACK, 88, self.theme)
        drawText("LEADERBOARD AND STATISTICS", -3, 20, BLUE, 88, self.theme)
        # draw table
        self.displayLeaderboard()
      
      #powerups/stars game state
      elif self.state == "buy powerups":
        SCREEN.fill((WHITE[self.theme]))
        # title
        drawText("STARS AND POWERUPS", 10, 20, BLACK, 120, self.theme)
        drawText("STARS AND POWERUPS", 5, 20, BLUE, 120, self.theme)
        # display number of stars over large star image
        uploadImage("yellowstar.png", 0.35, 80, 150 )
        drawText(stats.getNumberOfStars(), 230, 325, BLACK, 50, self.theme)
        drawText("Earn more stars by playing more games!", 70, 530, BLACK, 30, self.theme)
        # display powerup image
        uploadImage(allCharacters[2][0][self.theme], 2, 550, 140)
        # change buy button to red/green depending on whether user has enough stars
        if stats.getNumberOfStars() >= 100 and self.previousState != "pause":
          colour = GREEN[1]
        else:
          colour = RED
        # draw buy button over large powerup image
        pygame.draw.rect(SCREEN, colour, pygame.Rect(620, 285, 200, 50), 0, 0)
        pygame.draw.rect(SCREEN, BLACK[0], pygame.Rect(620, 285, 200, 50), 1, 0)
        # display number of remaining powerups the user has
        drawText("BUY", 676, 292, BLACK, 60, self.theme)
        drawText("You currently have " + str(stats.getPowerups()) + " powerups", 570, 530, BLACK, 30, self.theme)

      #help game state
      elif self.state == "help":#function displays new screen with help instructions
        SCREEN.fill((WHITE[self.theme]))
        # title
        drawText("HELP", 50, 0, BLACK, 200, self.theme)
        drawText("HELP", 45, 0, BLUE, 200, self.theme)
        # text box layout ish
        pygame.draw.rect(SCREEN, BLUE[self.theme], pygame.Rect(50, 125, 900, 425))
        #bullet points of game features 
        drawText("• Use the escape key on the keyboard to return to the previous page.", 60, 140, BLACK, 30, self.theme)
        drawText("• Click the play button to begin the game.", 60, 170, BLACK, 30, self.theme)
        drawText("• Use the up, down, left and right arrow keys on your keyboard to control movement", 60, 200, BLACK, 30, self.theme)
        drawText("• Avoid the ghosts as you only have three lives...", 60, 230, BLACK, 30, self.theme)
        drawText("• Powerups can give you more points, higher speed or ability to kill ghosts!", 60, 260, BLACK, 30, self.theme)
        drawText("• Collect stars and use these to buy powerups", 60, 290, BLACK, 30, self.theme)
        drawText("• Instructions on how to earn stars will display just before you start!", 60, 320, BLACK, 30, self.theme)
        drawText("• Click on 'Change Character' to change default theme and character image", 60, 350, BLACK, 30, self.theme)
        drawText("• Compete with your friends with the leaderboard feature!", 60, 380, BLACK, 30, self.theme)

      #change character and theme game state  
      elif self.state == "change theme":
        self.previousState = "menu"
        SCREEN.fill((WHITE[self.theme]))
        # display title
        drawText("CHANGE THEME", 15, 20, BLACK, 170, self.theme)
        drawText("CHANGE THEME", 10, 20, BLUE, 170, self.theme)
        # upload theme choices
        uploadImage("brighttheme.png", 0.4, 85, 120)
        uploadImage("oceantheme.png", 0.4, 515, 120)
        # instruction for selecting theme
        drawText("CLICK ON THE THEME YOU WANT TO APPLY", 265, 550, BLACK, 30)
      
      elif self.state == "change character":
        SCREEN.fill((WHITE[self.theme]))
        # title
        drawText("CHANGE CHARACTER", 40, 20, BLACK, 120, self.theme)
        drawText("CHANGE CHARACTER", 35, 20, BLUE, 120, self.theme)
        # display characters specific to theme chosen
        for x in range(len(allCharacters[self.theme])):
          uploadImage(allCharacters[self.theme][x][0], 1, 90 + x* 300, 210)
          # if character has been selected draw green box around the 
          if allCharacters[self.theme][x][0] == self.player.getImage():
            pygame.draw.rect(SCREEN, GREEN[self.theme], pygame.Rect(80 + x*300, 200, 200, 200), 2, 3)
        # return to menu button gives user shortcut
        pygame.draw.rect(SCREEN, GREEN[self.theme], pygame.Rect(380, 460, 250, 50), 0, 3)
        pygame.draw.rect(SCREEN, BLACK[self.theme], pygame.Rect(380, 460, 250, 50), 1, 3)
        drawText("RETURN TO MENU", 388, 475, BLACK, 38, self.theme)

      elif self.state == "levels": #displays levels page
        self.previousState = "menu" # return to menu if escape key is pressed
        SCREEN.fill((WHITE[self.theme]))
        # display side buttons
        for button in allButtons[0]: 
          button.render(self.theme)
        # display level number
        for button in allButtons[2]: 
          button.render(self.theme)
          level = int(button.text)
          # for each level find number of stars
          with open ("levelStarsInstructions.txt") as file: 
            lines = file.readlines()
            startLine = level * 3 - 3
            stars = int(lines[startLine][0]) + int(lines[startLine + 1][0]) + int(lines[startLine + 2][0])
            # display number of stars below level 
            for star in range(stars): 
              uploadImage("yellowstar.png", 0.02, 25 * star + button.x - 36, button.y + 40)
        # title
        drawText("LEVELS PAGE", 27, 0, BLACK, 200, self.theme)
        drawText("LEVELS PAGE", 22, 0, BLUE, 200, self.theme)

      elif self.state == "instructions": 
        # display instructions and username textbox for individual level
        self.previousState = "levels"
        SCREEN.fill((WHITE[self.theme]))
        # display side buttons
        for button in allButtons[0]: 
          button.render(self.theme)
        # title
        drawText("LEVEL " + self.currentLevel + " INSTRUCTIONS", 4, 5, BLACK, 118, self.theme)
        drawText("LEVEL " + self.currentLevel + " INSTRUCTIONS", -1, 5, BLUE, 118, self.theme)
        # load and display instructions
        self.loadInstructions()
        #display input box for username button
        usernameButton.render(self.theme)
        drawText("Enter username (between 3-10 characters) and press enter", 320, 350, BLACK, 20, self.theme)
        # red remove extra powerup button if user has more than 1
        if self.extraPowerups > 0:
          pygame.draw.circle(SCREEN, RED, (500, 555), 12, 0)
          pygame.draw.circle(SCREEN, BLACK[self.theme], (500, 555), 12, 1)
          pygame.draw.line(SCREEN, BLACK[self.theme], (495, 555), (505, 555))
        # green add extra powerup button if user has enough
        if stats.getPowerups() - self.extraPowerups - 1 >= 0 and self.extraPowerups <= 4:
          pygame.draw.circle(SCREEN, GREEN[self.theme], (600, 555), 12, 0)
          pygame.draw.circle(SCREEN, BLACK[self.theme], (600, 555), 12, 1)
          pygame.draw.line(SCREEN, BLACK[self.theme], (595, 555), (605, 555))
          pygame.draw.line(SCREEN, BLACK[self.theme], (600, 550), (600, 560))
        # display number of extra powerups
        drawText("EXTRA POWERUPS", 630, 550, BLACK, 30, self.theme)
        drawText(self.extraPowerups, 540, 545, BLACK, 50, self.theme)
        pygame.draw.rect(SCREEN, BLACK[self.theme], pygame.Rect(525, 535, 50, 50), 1, 3)
        
      #playing game state
      elif self.state == "play":
        self.startTime = 0 
        self.previousState = "pause"
        SCREEN.fill((WHITE[self.theme]))
        # title and pills near title for visual effect
        drawText("LEVEL " + self.currentLevel, 2, 5, BLACK, 100, self.theme)
        drawText("LEVEL " + self.currentLevel, -3, 5, BLUE, 100, self.theme)
        for x in range(18):
          pygame.draw.circle(SCREEN, PINK[self.theme], (300+ x*40, 35), 7.5, 0)
          pygame.draw.circle(SCREEN, BLACK[self.theme], (300 + x*40, 35), 7.5, 1)
        # display side buttons
        for button in allButtons[0]: 
          button.render(self.theme)
        # display play state specific buttons i.e. pause button
        for button in allButtons[3]: 
          button.render(self.theme)
        # score box
        pygame.draw.rect(SCREEN, GREEN[self.theme], pygame.Rect(50, 90, 150, 40), 0, 3)
        pygame.draw.rect(SCREEN, BLACK[self.theme], pygame.Rect(50, 90, 150, 40), 1, 3)
        # draw current game score 
        drawText("score: " + str(self.score), 55, 95, BLACK, 40, self.theme)
        # display stars and instructions
        self.displayGameStars()
        # display number of lives
        self.displayLives()
        # draw maze and all elements within
        self.drawMaze()
        # check if player has eaten all pills/powerups
        self.checkGameOver()
      
      #paused game state  
      elif self.state == "pause":
        self.previousState = "play"
        SCREEN.fill((WHITE[self.theme]))
        # display level instructions and stars (including whether they have been achieved yet)
        self.displayInstructions()
        # side buttons
        for button in allButtons[0]:
          button.render(self.theme)
        # replay, continue and return to menu buttons
        for button in allButtons[4]:
          button.render(self.theme)
        drawText("REPLAY", 375, 450, BLACK, 20, self.theme)
        drawText("CONTINUE", 470, 450, BLACK, 20, self.theme)
        drawText("MENU", 582, 450, BLACK, 20, self.theme)
        # title
        drawText("PAUSED", 220, 0, BLACK, 200, self.theme)
        drawText("PAUSED", 215, -5, BLUE, 200, self.theme)

      elif self.state == "game over":
        self.previousState = "menu"
        SCREEN.fill((WHITE[self.theme]))
        # title
        drawText("GAME OVER", 175, 20, BLACK, 155, self.theme)
        drawText("GAME OVER", 170, 20, BLUE, 155, self.theme)
        # side buttons
        for button in allButtons[0]:
          button.render(self.theme)
        # replay and next level buttton
        for button in allButtons[5]:
          button.render(self.theme)
        drawText("REPLAY", 365, 450, BLACK, 30, self.theme)
        drawText("NEXT LEVEL", 550, 450, BLACK, 30, self.theme)
        # display level instructions and stars (and whether they have been achieved)
        self.displayInstructions()
      elif self.state == "end program":
        SCREEN.fill(BLACK[self.theme])
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
  
      pygame.display.update()

# initialise game object
game = Game()

# play intro music 
playSoundEffect(INTROMUSIC)

# play game
game.playGame()


