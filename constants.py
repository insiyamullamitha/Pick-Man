#declare constant values that will not change while the game is running
import pygame
from pygame.locals import *
pygame.init()

WIDTH = 1000
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CELLWIDTH = 2
CELLHEIGHT = 2
FRAMESPERSECOND = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 22, 12)
PINK = (255, 0, 127)
ORANGE = (255, 139, 40)
GREEN = (153, 250, 118)
DARKGREEN = (0,100,0)
BLUE = (39, 160, 194)
DARKBLUE = (0, 0, 139)
PURPLE = (186,7,243)
GREY = (157, 154, 161)
BROWN = (165,42,42)
FONT = pygame.font.SysFont(None, 36)
MUSIC = pygame.mixer.Sound('media/backgroundmusic.wav')
PILLSOUND = pygame.mixer.Sound('media/wakkawakkasound.wav')
LOSINGLIFE = pygame.mixer.Sound('media/losinglifesound.wav')
POWERUPSOUND = pygame.mixer.Sound('media/powerupsound.wav')
