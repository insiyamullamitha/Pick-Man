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
import time

class Game:
  """a class for initialising a game object for pick-man"""
  def __init__(self):
    self.state = "start-up"
    self.previousState = "menu"
    self.running = True
    self.playingGame = False
    self.clock = pygame.time.Clock()
    self.score = 0
    self.music = False
    self.soundEffects = False
    self.stars = 0
    self.lives = 3
    self.time = [0, 0]
    self.startTime = 0
    self.currentLevel = None
    self.character = "pacmandefault.png"
    self.theme = 0
    self.username = ""
    self.player = Player(0, None, None)
    self.ghostObjects = [blinky, inky, winky]
    self.maze = Maze()
    self.stars = 0
    self.instructions = []
    self.success = False

  def drawMaze(self): # load maze on screen
    for wall in self.maze.getWalls(): # draw walls
      pygame.draw.rect(SCREEN, BLACK[self.theme], pygame.Rect((250 + (wall.x*30)), 65 + (wall.y*30), 30, 30),0)
    for path in self.maze.getPaths(): # draw white squares representing path
      pygame.draw.rect(SCREEN, WHITE[self.theme], pygame.Rect((250 + (path.x*30)), 65 + (path.y*30), 30, 30),0)
    for pill in self.maze.getPills(): # draw pills
      pygame.draw.circle(SCREEN, PINK[self.theme], (264+pill.x*30, 78+pill.y*30), 5, 0)
    for powerup in self.maze.getPowerups(): # powerup objects must be instantiated
      uploadImage(powerup.getImage(), 1/7, 252+powerup.getPosX()*30, 68+powerup.getPosY()*30)
    # draw player 
    uploadImage(self.character, 1/6, 250+self.player.getPosX()*30, 65 + self.player.getPosY()*30, self.player.getRotate())
    for ghost in self.ghostObjects: # ghost objects must be instantiated
      ghost.move(self) # ghost object move
      uploadImage(ghost.getImage(), 1/6, 250+ghost.getPosX()*30, 65 + ghost.getPosY()*30)

  def loadInstructions(self):
    with open ("levelStarsInstructions.txt") as file: # find instructions for level and store in array
      lines = file.readlines()
      startInstruction = int(self.currentLevel) * 3 - 3
      # update self.instructions with star status of zero (at the start of the game) and type of instruction
      self.instructions = [[0, lines[startInstruction][1:].strip('\n')],
                          [0, lines[startInstruction + 1][1:].strip('\n')], 
                          [0, lines[startInstruction + 2][1:].strip('\n')]]
      self.displayInstructions()

  def displayInstructions(self):
      # display each instruction and star
    for instruction in range(3):
      image = "emptystar.png"
      if self.instructions[instruction][0] == 1:
        image = "yellowstar.png"
      uploadImage(image, 0.1, 245 + 200*instruction, 170)
      drawText(self.instructions[instruction][1], 260 + instruction * 200, 290, BLACK, 15, self.theme)
      uploadImage(self.character, 0.25, 3, 215)
      for x in range(6):
        pygame.draw.circle(SCREEN, PINK[self.theme], (55 + x*40, 235), 7.5, 0)
      for x in range(4):
        pygame.draw.circle(SCREEN, PINK[self.theme], (340 + x*40, 235), 7.5, 0)
      for x in range(4):
        pygame.draw.circle(SCREEN, PINK[self.theme], (540+ x*40, 235), 7.5, 0)
      for x in range(8):
        pygame.draw.circle(SCREEN, PINK[self.theme], (740 + x*40, 235), 7.5, 0)

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
        if self.instructions[0][0] != 1 and self.score >= 50:
          self.instructions[0][0] = 1
          self.stars += 1
        if self.instructions[1][0] != 1 and self.score >= 100:
          self.instructions[1][0] = 1
          self.stars += 1
        if self.instructions[2][0] != 1 and self.score >= 150:
          self.instructions[2][0] = 1
          self.stars += 1

  def updateFileStarStatus(self, instructionNumber): # update which stars have been achieved at the end of game 
    startInstruction = int(self.currentLevel) * 3 - 3 # find the line from which the level's instructions start
    file = open("levelStarsInstructions.txt", "r")
    lines = file.readlines()
    lines[startInstruction + instructionNumber] = "1" + self.instructions[instructionNumber][1] + "\n" #change 0 to 1 to represent achieved
    stats.updateFile(lines, "levelStarsInstructions.txt")#update file
     
  def displayGameStars(self): # displays stars and instructions during game
    self.updateStars()
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
    # set default character in case the user forgets/exits before they select
    matchingCharacter = False
    for characters in allCharacters[self.theme]:
      if self.character == characters[0]:
        matchingCharacter = True
    if matchingCharacter == False:
      self.changeCharacter(0)

  def changeCharacter(self, givenCharacter):
    # change character
    self.character = allCharacters[self.theme][givenCharacter][0]
    # change ghosts images depending on character chosen
    for ghost in range(len(self.ghostObjects)):
      self.ghostObjects[ghost].setImage(allCharacters[self.theme][givenCharacter][ghost + 1])
    self.player.setRotate(0)

  def clickButtons(self):# detects whether button has been clicked and changes game state
    # if any button on the screen has been clicked change game state 
    for buttons in allButtons:
      for button in buttons:
        if button.click() != None:
          if button in allButtons[0] and self.state not in ["menu", "levels", "instructions", "play", "game over"]:
            return
          if button in allButtons[1] and self.state != "menu":
            return
          if button in allButtons[2]:
            if self.state == "levels":
              self.currentLevel = button.text
            else:
              return
          if button in allButtons[3] and self.state != "play":
            return
          self.previousState = self.state
          self.state = button.newState
          if button.newState == "play":
            self.playingGame = True
            self.startTime = pygame.time.get_ticks()
          SCREEN.fill((WHITE[self.theme]))
  
  # check that username is between 3 and 10 characters and save as game username
  def verifyUsername(self):
    if len(usernameButton.text) > 2 and len(usernameButton.text) < 11:
      self.state = "play"
      self.username = usernameButton.text.upper()
      self.playingGame = True

  def gameTimer(self):
    # find time in minutes and seconds and store as tuple
    if self.playingGame:
      self.time[1] += 0.001
      if self.time[1] >= 60000:
        self.time[0] += 1
        self.time[1] = 0
      #self.time = (abs(math.floor((pygame.time.get_ticks()-self.startTime)/1000))//60, int((pygame.time.get_ticks()-self.startTime)/1000) - (60 * (math.floor((pygame.time.get_ticks()-self.startTime)/1000)//60)))

  def playGame(self):
    while self.running:

      self.clock.tick(FRAMESPERSECOND)

      pygame.init()    

      pygame.display.set_caption("PICKMAN")  
      pacman = pygame.image.load('media/' + self.character)
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
              self.playingGame = False
            elif self.state == "pause":
              self.state = "play"
              self.startTime = pygame.time.get_ticks()
              self.playingGame = True
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
          if self.state == "play":
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]:
              self.player.setDirection(event.key)
        if event.type == MOUSEBUTTONDOWN:
          posX, posY = pygame.mouse.get_pos()
          if self.state == "change theme":
            # check if user has decided to change theme
            if posY >= 120 and posY <= 520:
              # bright theme = theme 0
              if posX >= 85 and posX <= 489:
                self.changeTheme(0)
              # ocean theme = theme 1
              elif posX >= 515 and posX <= 919:
                self.changeTheme(1)
          elif self.state == "change character":
            # change character if image is clicked
            if posY >= 210 and posY <= 390:
              for x in range(3):
                if posX >= (90 + x*300) and posX <= (270 + x*300):
                  self.changeCharacter(x)
          elif self.state == "buy powerups":
            # if user has enough stars then update number of stars and increase extra powerups
            if stats.getNumberOfStars() >= 100:
              stats.changeNumberOfStars(-100)
              stats.changePowerups(1)
          elif self.state != "start-up":
            self.clickButtons()
        if event.type == pygame.KEYUP:
          if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP]:
            self.player.setDirection("")

      # start up screen game state
      if self.state == "start-up":
        SCREEN.fill((WHITE[self.theme]))
        for x in range(300):
          uploadImage(random.choice(["redghost.png", "purpleghost.png", "blueghost.png"]),0.1, random.randint(-30,1000), random.randint(-30,600))
        drawText("PICKMAN", -7, 175, BLACK, 300, self.theme)
        drawText("BY INSIYA MULLAMITHA", 320, 400, BLACK, 40, self.theme)
        pygame.display.flip()
        pygame.time.delay(2500)
        self.state = "menu"

      #menu gamestate
      if self.state == "menu": 
        self.previousState = "menu"
        SCREEN.fill((WHITE[self.theme])) 
        # display ghosts specific to theme and character chosen
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
        drawText("PICKMAN", 0, 0, BLACK, 300, self.theme)
        drawText("PICKMAN", -8, 0, BLUE, 300, self.theme)

      #background music game state
      elif self.state == "music":
        SCREEN.fill((WHITE[self.theme]))
        if self.music == True:
          pass
        else:
          pass
      
      elif self.state == "sound":
        SCREEN.fill((WHITE[self.theme]))

      #leaderboard/statistics game state
      elif self.state == "stats":
        SCREEN.fill((WHITE[self.theme]))
        drawText("LEADERBOARD AND STATISTICS", 2, 25, BLACK, 88, self.theme)
        drawText("LEADERBOARD AND STATISTICS", 2, 20, BLUE, 88, self.theme)
        stats.displayLeaderboard(self.theme)
      
      #powerups/stars game state
      elif self.state == "buy powerups":
        SCREEN.fill((WHITE[self.theme]))
        drawText("STARS AND POWERUPS", 10, 20, BLACK, 120, self.theme)
        drawText("STARS AND POWERUPS", 5, 20, BLUE, 120, self.theme)
        # display number of powerups
        drawText("YOU CURRENTLY HAVE " + str(stats.getNumberOfStars()) + " STARS", 10, 100, BLACK, 30, self.theme)
        drawText("YOU CURRENTLY HAVE " + str(stats.getPowerups()) + " POWERUPS", 10, 130, BLACK, 30, self.theme)
        # check if user has enough powerups and display good/bad message accordingly
        if stats.getNumberOfStars() >= 100:
          uploadImage("")
          drawText("CLICK BELOW TO BUY EXTRA POWERUPS YOU CAN ADD TO YOUR NEXT GAME", 10, 160, BLACK, 30, self.theme)
        else:
          drawText("YOU NEED " + str(100 - stats.getNumberOfStars()) + " MORE STARS TO BUY EXTRA POWERUPS", 10, 160, BLACK, 30, self.theme)
          drawText("PLAY MORE GAMES TO EARN MORE STARS!!", 10, 190, BLACK, 30, self.theme)
        uploadImage(allCharacters[2][0][self.theme], 1, 30, 200)

      #help game state
      elif self.state == "help":#function displays new screen with help instructions
        SCREEN.fill((WHITE[self.theme]))
        drawText("HELP", 50, 0, BLACK, 200, self.theme)
        drawText("HELP", 45, 0, BLUE, 200, self.theme)
        pygame.draw.rect(SCREEN, BLUE[self.theme], pygame.Rect(50, 125, 900, 425))
        #bullet points of game features 
        drawText("??? Click the play button to begin the game.", 60, 140, BLACK, 30)
        drawText("??? Instructions on how to earn will display just before you start!", 60, 170, BLACK, 30, self.theme)
        drawText("??? Use the up, down, left and right arrow keys on your keyboard to control movement", 60, 200, BLACK, 30, self.theme)
        drawText("??? Click on 'Change Character' to change default theme and character image", 60, 230, BLACK, 30, self.theme)
        drawText("??? Collect stars and use these to buy powerups", 60, 260, BLACK, 30, self.theme)
        drawText("??? Compete with your friends with the leaderboard feature!", 60, 290, BLACK, 30, self.theme)

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
        drawText("CLICK ON THE THEME YOU WANT TO APPLY", 265, 550, BLACK, 30)
      
      elif self.state == "change character":
        SCREEN.fill((WHITE[self.theme]))
        drawText("CHANGE CHARACTER", 40, 20, BLACK, 120, self.theme)
        drawText("CHANGE CHARACTER", 35, 20, BLUE, 120, self.theme)
        # display characters specific to theme chosen
        for x in range(len(allCharacters[self.theme])):
          uploadImage(allCharacters[self.theme][x][0], 1, 90 + x* 300, 210)
          # if character has been selected draw green box around the 
          if allCharacters[self.theme][x][0] == self.character:
            pygame.draw.rect(SCREEN, GREEN[self.theme], pygame.Rect(80 + x*300, 200, 200, 200), 2, 3)

      elif self.state == "levels": #displays levels page
        self.previousState = "menu" # return to menu if escape key is pressed
        SCREEN.fill((WHITE[self.theme]))
        for button in allButtons[0]: # display side buttons
          button.render(self.theme)
        for button in allButtons[2]: # display level number
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

        drawText("LEVELS PAGE", 27, 0, BLACK, 200, self.theme)

        drawText("LEVELS PAGE", 22, 0, BLUE, 200, self.theme)

      elif self.state == "instructions": # display instructions for individual level
        self.previousState = "levels"
        SCREEN.fill((WHITE[self.theme]))
        for button in allButtons[0]: #display side buttons 
          button.render(self.theme)
        drawText("LEVEL " + self.currentLevel + " INSTRUCTIONS", 4, 5, BLACK, 118, self.theme)
        drawText("LEVEL " + self.currentLevel + " INSTRUCTIONS", -1, 5, BLUE, 118, self.theme)
        self.loadInstructions()
        if self.currentLevel == "1": # load level 1 maze
          mazeLayout = level1Maze
        elif self.currentLevel == "2": # load level 2 maze
          # level 2 instructions
          mazeLayout = level2Maze
        self.maze.loadMaze(mazeLayout, self.theme)
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
        usernameButton.render(self.theme)
        drawText("Enter username below and press enter", 350, 350, BLACK, 20, self.theme)
        self.success = False

      #playing game state
      elif self.state == "play":
        self.startTime = 0 
        self.previousState = "pause"
        SCREEN.fill((WHITE[self.theme]))
        drawText("LEVEL " + self.currentLevel, 2, 5, BLACK, 100, self.theme)
        drawText("LEVEL " + self.currentLevel, -3, 5, BLUE, 100, self.theme)
        for x in range(18):
          pygame.draw.circle(SCREEN, PINK[self.theme], (300+ x*40, 35), 7.5, 0)
        for button in allButtons[0]: # display side buttons
          button.render(self.theme)
        for button in allButtons[3]: # display play state specific buttons
          button.render(self.theme)
        self.player.move(self)
        self.displayGameStars()
        self.displayLives()
        self.drawMaze()
        pygame.draw.rect(SCREEN, GREEN[self.theme], pygame.Rect(570, 540, 120, 40), 0, 3)
        #drawText(str(self.time[0]) + "m " + str(self.time[1]) + "s", 580, 545, BLACK, 40)
        pygame.draw.rect(SCREEN, GREEN[self.theme], pygame.Rect(50, 90, 150, 40), 0, 3)
        drawText("score: " + str(self.score), 55, 95, BLACK, 40, self.theme)
      
      #paused game state  
      elif self.state == "pause":
        self.previousState = "play"
        SCREEN.fill((WHITE[self.theme]))
        drawText("PAUSED", 0, 0, BLACK, 200, self.theme)
        drawText("PAUSED", 0, -5, BLUE, 200, self.theme)

      elif self.state == "game over":
        self.previousState = "menu"
        SCREEN.fill((WHITE[self.theme]))
        drawText("GAME OVER", 175, 20, BLACK, 155, self.theme)
        drawText("GAME OVER", 170, 20, BLUE, 155, self.theme )
        for button in allButtons[0]:
          button.render(self.theme)
        self.displayInstructions()
        if not self.success:
          drawText("TRY AGAIN TO COLLECT ALL STARS", 125, 350, BLACK, 40, self.theme)
          stats.updateStatistics(self.stars)
          # display replay button
        else:
          drawText("WELL DONE", 160, 350, BLACK, 40, self.theme)
          stats.updateStatistics(self.stars, self.score, self.username, (self.time[0] * 60) + self.time[1])
        # reset current game statistics for next game
        self.score = 0
        self.stars = 0
        self.username = ""
        # display next level button
      
      elif self.state == "end program":
        SCREEN.fill(BLACK[self.theme])
        # add animation
        playSoundEffects(LOSINGLIFE)
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
  
      pygame.display.update()

game = Game()
game.playGame()
