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
PILLSOUND = 'media/wakkawakkasound.wav'
LOSINGLIFESOUND = 'media/losinglifesound.wav'
POWERUPSOUND = 'media/earnstarsound.wav'
STARSOUND = "media/powerupsound.wav"
KILLGHOSTSOUND = "media/playerkillssound.wav"
INTRODUCTIONMUSIC = "media/intromusic.wav"
allCharacters = [[["pacmandefault.png", "redghost.png", "purpleghost.png", "blueghost.png"], 
                  ["jerry.png", "tom.png", "tom.png", "tom.png"], 
                  ["gru.png", "kevin.png", "stuart.png", "bob.png"]],
                 [["jellyfishgame.PNG", "lightbluenet.png", "bluenet.png", "purplenet.png"], 
                  ["nemo.png", "shark.png", "shark.png", "shark.png"], 
                  ["turtle.png", "shark.png", "shark.png", "shark.png"]],
                 [["cherrypowerup.png", "seashellpowerup.png"]]]