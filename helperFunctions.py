#helper function file to contain functions that are used repeatedly throughout the game
from constants import *
import time

def drawText(string, x, y, colour, size, givenTheme = 0):
    #function to render inputted string onto a given position
    font = pygame.font.SysFont(None, size)
    text = font.render(str(string), True, colour[givenTheme])
    SCREEN.blit(text, (x, y))

def uploadImage(imageFileName, scale, x, y, rotation = 0): # scale, rotate and upload image on to screen
    # load image file to pygame
    imageToUpload = pygame.image.load("media/" + imageFileName).convert_alpha()
    width = imageToUpload.get_rect().width
    height = imageToUpload.get_rect().height
    # scale
    imageToUpload = pygame.transform.scale(imageToUpload, (width*scale, height*scale))
    # rotate
    screenToUpload = pygame.transform.rotate(imageToUpload, rotation)
    # blit
    SCREEN.blit(screenToUpload, (x, y))

def playSoundEffect(soundEffect): # plays given sound effect via first available channel
    emptyChannel = None
    i = 0
    # find empty channel from default number of channels 
    while emptyChannel is not None and i <= pygame.mixer.get_num_channels():
        if not pygame.mixer.Channel(i).get_busy():
            emptyChannel = i
        else:
            i += 1
    # if no channels are empty, use the first one
    if emptyChannel is None:
        emptyChannel = 0
    # play sound effect via the channel selected
    pygame.mixer.Channel(emptyChannel).play(soundEffect)


    