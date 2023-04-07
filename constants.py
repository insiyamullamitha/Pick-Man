#declare constant values that will not change while the game is running
import pygame
from pygame.locals import *
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
# load sound effects/music
WIDTH = 1000
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
PILLSOUND = pygame.mixer.Sound("media/pilleatensound.wav")
LOSINGLIFESOUND = pygame.mixer.Sound("media/losinglifesound.wav")
POWERUPSOUND = pygame.mixer.Sound("media/powerupsound.wav")
STARSOUND = pygame.mixer.Sound("media/starsound.wav")
KILLGHOSTSOUND = pygame.mixer.Sound("media/killsound.wav")
INTROMUSIC  = pygame.mixer.Sound('media/intromusic.wav')  
# screen size
FRAMESPERSECOND = 60
# colours
BLACK = [(0, 0, 0), (0, 0, 0)]
WHITE = [(255, 255, 255), (65, 173, 116)]
PINK = [(255, 0, 127), (0, 255, 153)]  
RED = (255, 0, 0)
GREEN = [(153, 250, 118), (0, 153, 51)]
BLUE = [(39, 160, 194), (255, 255, 255)]
LIGHTBLUE = [(31,176,245),(45,117,50)]
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