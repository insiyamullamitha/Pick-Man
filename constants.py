#declare constant values that will not change while the game is running
import pygame
from pygame.locals import *
pygame.init()

WIDTH = 1000
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CELLWIDTH = 2
CELLHEIGHT = 2
FRAMESPERSECOND = 60
BLACK = [(0, 0, 0), (0,0,0)]
WHITE = [(255, 255, 255), [65, 173, 116]]
PINK = [(255, 0, 127), (0, 255, 153)]  
GREEN = [(153, 250, 118), (0, 153, 51), (0, 204, 102)]
BLUE = [(39, 160, 194), (255, 255, 255)]
LIGHTBLUE = [(31,176,245),(45,117,50) ]
GREY = [(157, 154, 161), (255,114,118)]
FONT = pygame.font.SysFont(None, 36)
MUSIC = pygame.mixer.Sound('media/backgroundmusic.wav')
PILLSOUND = pygame.mixer.Sound('media/wakkawakkasound.wav')
LOSINGLIFE = pygame.mixer.Sound('media/losinglifesound.wav')
POWERUPSOUND = pygame.mixer.Sound('media/powerupsound.wav')
allCharacters = [[["pacmandefault.png", "redghost.png", "purpleghost.png", "blueghost.png"], 
                  ["jerry.png", "tom.png", "tom.png", "tom.png"], 
                  ["gru.png", "kevin.png", "stuart.png", "bob.png"]],
                 [["jellyfishgame.PNG", "lightbluenet.png", "bluenet.png", "purplenet.png"], 
                  ["nemo.png", "shark.png", "shark.png", "shark.png"], 
                  ["turtle.png", "shark.png", "shark.png", "shark.png"]]]