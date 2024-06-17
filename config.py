import pygame

# screen config and initialization

# pygame initialization
pygame.init()

# screen config
screen_size = [pygame.display.Info().current_w,pygame.display.Info().current_h]
screen = pygame.display.set_mode((1000,667))
fullscreen = False