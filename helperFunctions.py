#helper function file to contain functions that are used repeatedly throughout the game
import pygame
pygame.init()
from constants import *
from pygame.locals import *

def drawText(string, x, y, colour, size):
    #function to render inputted string onto a given position
    font = pygame.font.SysFont(None, size)
    text = font.render(str(string), True, colour)
    SCREEN.blit(text, (x, y))

def uploadImage(image, scale, x, y, rotation = 0):
    imageToUpload = pygame.image.load("media/" + image).convert_alpha()
    width = imageToUpload.get_rect().width
    height = imageToUpload.get_rect().height
    imageToUpload = pygame.transform.scale(imageToUpload, (width*scale, height*scale))
    screenToUpload = pygame.transform.rotate(imageToUpload, rotation)
    SCREEN.blit(screenToUpload, (x, y))

def playSoundEffects(audio):#generate sound effect when pacman eats a pill
    audio.play()