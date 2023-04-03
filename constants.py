#declare constant values that will not change while the game is running
import pygame
from pygame.locals import *

pygame.mixer.init()

# sound effects/music
PILLSOUND = pygame.mixer.Sound("media/pillsound.wav")
LOSINGLIFESOUND = pygame.mixer.Sound("media/losinglifesound.wav")
POWERUPSOUND = pygame.mixer.Sound("media/powerupsound.wav")
STARSOUND = pygame.mixer.Sound("media/earnstarsound.wav")
KILLGHOSTSOUND = pygame.mixer.Sound("media/playerkillssound.wav")

pygame.init()

# screen size
WIDTH = 1000
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CELLWIDTH = 2
CELLHEIGHT = 2
FRAMESPERSECOND = 60
# colours
BLACK = [(0, 0, 0), (0, 0, 0), (6,85,99)]
WHITE = [(255, 255, 255), [65, 173, 116]]
PINK = [(255, 0, 127), (0, 255, 153)]  
RED = (255, 0, 0)
GREEN = [(153, 250, 118), (0, 153, 51), (0, 204, 102)]
BLUE = [(39, 160, 194), (255, 255, 255)]
LIGHTBLUE = [(31,176,245),(45,117,50) ]
GREY = [(157, 154, 161), (255,114,118)]
PURPLE = [(191, 0, 255), (144, 109, 203)]
FONT = pygame.font.SysFont(None, 36)
# maze element images
allCharacters = [[["pacmandefault.png", "redghost.png", "purpleghost.png", "blueghost.png"], 
                  ["jerry.png", "tom.png", "tom.png", "tom.png"], 
                  ["gru.png", "kevin.png", "stuart.png", "bob.png"]],
                 [["jellyfishgame.PNG", "lightbluenet.png", "bluenet.png", "purplenet.png"], 
                  ["nemo.png", "shark.png", "shark.png", "shark.png"], 
                  ["turtle.png", "shark.png", "shark.png", "shark.png"]],
                 [["cherrypowerup.png", "seashellpowerup.png"]]]
playerRotations = {"left": 180, "right": 0, "down": 270, "up": 90}