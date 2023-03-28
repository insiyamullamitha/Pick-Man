#helper function file to contain functions that are used repeatedly throughout the game
import pygame
pygame.init()
from constants import *
from pygame.locals import *

def drawText(string, x, y, colour, size, givenTheme = 0):
    #function to render inputted string onto a given position
    font = pygame.font.SysFont(None, size)
    text = font.render(str(string), True, colour[givenTheme])
    SCREEN.blit(text, (x, y))

def uploadImage(image, scale, x, y, rotation = 0): # scale, rotate and upload image on to screen
    imageToUpload = pygame.image.load("media/" + image).convert_alpha()
    width = imageToUpload.get_rect().width
    height = imageToUpload.get_rect().height
    # scale
    imageToUpload = pygame.transform.scale(imageToUpload, (width*scale, height*scale))
    # rotate
    screenToUpload = pygame.transform.rotate(imageToUpload, rotation)
    # blit
    SCREEN.blit(screenToUpload, (x, y))

#generate given sound effect if sound effect settings are turned on
def playSoundEffects(soundEffects, sound):
    if soundEffects:
        print(sound)
        sound.play()