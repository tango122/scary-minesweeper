import pygame
from sys import exit
import random
import os
import time
from game import Game
from config import *
        
# title screen setup
pygame.display.set_caption("Scary Minesweeper")
background = pygame.image.load('graphics/background.jpg').convert()
scary_font = pygame.font.Font('font/scary_font.ttf',50)
title_surf = scary_font.render('Scary Minesweeper',True,(235,238,245))
title_surf = pygame.transform.scale(title_surf,(300,150))
easy_surf = scary_font.render('Easy',True,(178,180,184))
medium_surf = scary_font.render('Medium',True,(178,180,184))
hard_surf = scary_font.render('Hard',True,(178,180,184))
f_surf = scary_font.render('F to toggle fullscreen',True,(178,180,184))
f_surf = pygame.transform.scale(f_surf,(200,50))
q_surf = scary_font.render('Q if you are scared',True,(178,180,184))
q_surf = pygame.transform.scale(q_surf,(200,50))

# background music setup
bg_music = pygame.mixer.Sound('audio/bg.mp3')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)

# initial game conditions and Game object creation
game_active = False
game_over = False
win = False
test = Game()

# main game loop
while True:
    # handle game over state
    if game_over:
        # display win screen according to screen size
        if win:
            screen.fill('Black')
            win_surf = scary_font.render('YOU WIN',True,(235,238,245))
            if fullscreen:
                win_rect = win_surf.get_rect(midbottom = (screen_size[0]/2,screen_size[1]*.56))
            else:
                win_rect = win_surf.get_rect(midbottom = (500,210))
            screen.blit(win_surf,win_rect)
        # display jumpscare pic according to screen size and play jumpscare sound
        else:
            jumpscare = pygame.image.load('graphics/jumpscare/'+random.choice(os.listdir('graphics/jumpscare'))).convert()
            if fullscreen:
                jumpscare = pygame.transform.scale(jumpscare,screen_size)
            else:
                jumpscare = pygame.transform.scale(jumpscare,(1000,667))
            jumpscare_sound = pygame.mixer.Sound('audio/jumpscare/'+random.choice(os.listdir('audio/jumpscare')))
            jumpscare_sound.set_volume(1)
            jumpscare_sound.play()
            screen.blit(jumpscare,(0,0))
        # reset initial game conditions
        game_active = False
        pygame.display.update()
        time.sleep(5)
        game_over = False
        win = False
    else:
        # set up background visuals
        if not fullscreen:
            screen.blit(background,(0,0))
            f_rect = f_surf.get_rect(topright = (990,10))
            q_rect = q_surf.get_rect(topleft = (10,10))
            screen.blit(f_surf,f_rect)
            screen.blit(q_surf,q_rect)
        else:
            screen.blit(pygame.transform.scale(background,screen_size),(0,0))
            f_rect = f_surf.get_rect(topright = (screen_size[0]-10,10))
            screen.blit(q_surf,q_rect)
            screen.blit(f_surf,f_rect)
        # display title screen
        if not game_active:
            if not fullscreen:
                title_rect = title_surf.get_rect(midbottom = (500,200))
                easy_rect = easy_surf.get_rect(midbottom = (500,300))
                medium_rect = medium_surf.get_rect(midbottom = (500,375))
                hard_rect = hard_surf.get_rect(midbottom = (500,450))
            else:
                title_rect = title_surf.get_rect(midbottom = (screen_size[0]/2,screen_size[1]*.3))
                easy_rect = easy_surf.get_rect(midbottom = (screen_size[0]/2,screen_size[1]*.45))
                medium_rect = medium_surf.get_rect(midbottom = (screen_size[0]/2,screen_size[1]*.56))
                hard_rect = hard_surf.get_rect(midbottom = (screen_size[0]/2,screen_size[1]*.67))
            screen.blit(title_surf,title_rect)
            screen.blit(easy_surf,easy_rect)
            screen.blit(medium_surf,medium_rect)
            screen.blit(hard_surf,hard_rect)
        test.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # handle fullscreen toggle with "f"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:    
                    if fullscreen:
                        screen = pygame.display.set_mode((1000,667))
                        fullscreen = False
                    else:
                        screen = pygame.display.set_mode(screen_size,pygame.FULLSCREEN)
                        fullscreen = True
                # handle quit game with "q"
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
            # handle mouse click action and its effects for title screen and game
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = pygame.mouse.get_pressed()
                if game_active:
                    if state[2]:
                        test.right_click()
                    if state[0] and not state[2] and not state[1]:
                        game_over = test.click()
                        test.click()
                else:
                    if easy_rect.collidepoint(event.pos):
                        test.difficulty = 1
                        game_active = True
                        test.make_grid()
                    if medium_rect.collidepoint(event.pos):
                        test.difficulty = 2
                        game_active = True
                        test.make_grid()
                    if hard_rect.collidepoint(event.pos):
                        test.difficulty = 3
                        game_active = True
                        test.make_grid()
                         
    pygame.display.update()