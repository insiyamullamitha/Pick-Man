from helperFunctions import *
from pygame.locals import *
from constants import *
import math

class Button:
    def __init__(self, givenText, givenImage, givenColour, givenShape, givenX, givenY, givenRadius, givenLength, givenWidth, givenState):
        self.text = givenText
        self.image = givenImage
        self.colour = givenColour
        self.shape = givenShape
        self.x = givenX
        self.y = givenY
        self.radius = givenRadius
        self.length = givenLength
        self.width = givenWidth
        self.newState = givenState
    
    def render(self, givenTheme):# draws shape of button onto screen with image or text
        if self.shape == "circle":
            pygame.draw.circle(SCREEN,  self.colour[givenTheme], (self.x, self.y), self.radius, 0)
            if self.image != "":
                uploadImage(self.image, 0.6, self.x-20, self.y-22)
            drawText(self.text, self.x-5, self.y-5, BLACK, 25, givenTheme)
        elif self.shape == "rectangle":
            pygame.draw.rect(SCREEN, self.colour[givenTheme], pygame.Rect(self.x, self.y, self.length, self.width), 0, 3)
            drawText(self.text, self.x + 23, self.y + 10, BLACK, 25, givenTheme)

    def click(self): # checks for collision detection for button and returns true if button has been clicked
        mouseX, mouseY = pygame.mouse.get_pos()

        if self.shape == "circle":
            sqx = (mouseX - self.x)**2
            sqy = (mouseY - self.y)**2
            if math.sqrt(sqx + sqy) < self.radius:
                return self.newState
        
        if self.shape == "rectangle":
            if mouseX >= self.x and mouseX <= (self.x + self.length) and mouseY >= self.y and mouseY <= (self.y + self.width):
                return self.newState

# initialise all buttons
musicButton = Button("", 'musicsymbol.png', BLUE, "circle", 60, 555, 35, 0, 0, "music")
soundButton = Button("", 'soundsymbol.png', BLUE, "circle", 150, 555, 35, 0, 0, "sound")
statsButton = Button("", 'statssymbol.png', BLUE, "circle", 240, 555, 35, 0, 0, "stats")
starButton = Button("", 'starsymbol.png', BLUE, "circle", 330, 555, 35, 0, 0, "buy powerups")
helpButton = Button("", 'helpsymbol.png', BLUE, "circle", 420, 555, 35, 0, 0, "help")
pauseButton = Button("", 'pausedsymbol.png', BLUE, "circle", 510, 555, 35, 0, 0, "pause")
menuPlayButton = Button("", "playsymbol.png", GREEN, "circle", WIDTH//2, HEIGHT//2, 35, 0, 0, "levels")
changeCharacterButton = Button("CHANGE CHARACTER/THEME", "", PINK, "rectangle", 350, 350, 0, 300, 40, "change theme")
level1Button = Button("1", "", GREEN, "circle", 60, 180, 35, 0, 0, "instructions")
level2Button = Button("2", "", GREY, "circle", 200, 180, 35, 0, 0, "instructions")
usernameButton = Button("", "", PINK, "rectangle", 350, 370, 0, 300, 40, "instructions")
# add buttons for each game state to array within allButtons 2D array
# allButtons[0] for side buttons, allButtons[1] for menu page, allButtons[2] for levels etc.
allButtons = [[musicButton, soundButton, statsButton, starButton, helpButton], [menuPlayButton, changeCharacterButton],
              [level1Button, level2Button], [pauseButton]]
