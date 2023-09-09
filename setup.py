import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

DEFAULT_FONT = pygame.font.Font("font.ttf", 100)
TITLE_FONT = pygame.font.Font("font.ttf", 140)
SMALL_FONT = pygame.font.Font("font.ttf", 60)

SOUND_MUSIC = pygame.mixer.Sound("music.wav")
SOUND_SELECT = pygame.mixer.Sound("select.wav")
SOUND_EXPLOSION = pygame.mixer.Sound("explosion.wav")

