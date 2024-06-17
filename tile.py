import pygame
from config import screen_size, fullscreen

# class for each individual tile on minesweeper board
class Tile(pygame.sprite.Sprite):
    # initialization with parameters x and y coordinates and difficulty level of the board
    def __init__(self,x,y,difficulty):
        super().__init__()
        #load possible images for tiles
        image1 = pygame.image.load('graphics/tile.jpg').convert()
        image2 = pygame.image.load('graphics/clicked_0.jpg').convert()
        image3 = pygame.image.load('graphics/clicked_1.jpg').convert()
        image4 = pygame.image.load('graphics/clicked_2.jpg').convert()
        image5 = pygame.image.load('graphics/clicked_3.jpg').convert()
        image6 = pygame.image.load('graphics/clicked_4.jpg').convert()
        image7 = pygame.image.load('graphics/clicked_5.jpg').convert()
        image8 = pygame.image.load('graphics/clicked_6.jpg').convert()
        image9 = pygame.image.load('graphics/clicked_7.jpg').convert()
        image10 = pygame.image.load('graphics/clicked_8.jpg').convert()
        image11 = pygame.image.load('graphics/flag.jpg').convert()
        self.image_index = 0
        self.images = [image1,image2,image3,image4,image5,image6,image7,image8,image9,image10,image11]
        self.image = self.images[self.image_index]
        self.x = x
        self.y = y
        self.difficulty = difficulty
        self.offsetx = 0
        self.offsety = 0
        self.scale = 0
        self.pic_size = 0
        #configure tile size based on the difficulty level
        if not fullscreen:
            if self.difficulty == 1:
                self.scale = 60
                self.offsetx = 130
                self.offsety = 5
            elif self.difficulty == 2:
                self.scale = 40
                self.offsetx = 100
                self.offsety = 24
            elif self.difficulty == 3:
                self.scale = 30
                self.offsetx = 118
                self.offsety = 30
        else:
            if self.difficulty == 1:
                self.scale = 80
                self.offsetx = screen_size[0]/6
                self.offsety = screen_size[1]/100
            elif self.difficulty == 2:
                self.scale = 40
                self.offsetx = 100
                self.offsety = 24
            elif self.difficulty == 3:
                self.scale = 30
                self.offsetx = 118
                self.offsety = 30
        self.image = pygame.transform.scale(self.image,(self.scale,self.scale))
        pos_x, pos_y = 0, 0
        if self.x == 0:
            pos_x = self.scale
        else:
            pos_x = self.x*self.scale
        if self.y == 0:
            pos_y = self.scale
        else:
            pos_y = self.y*self.scale
        self.rect = self.image.get_rect(topleft = (pos_x+self.offsetx,pos_y+self.offsety))
        self.has_bomb = False
        self.adjacent_bombs = 0
        self.flag = False
        self.clicked = False
        self.first_clicked = False
        self.loser = False
        
    # handle right click action for flagging or un-flagging a tile
    def right_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.clicked:
                if not self.flag:
                    self.flag = True
                else:
                    self.flag = False
    
    # handle left click action for checking if a tile has a bomb
    def click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.flag:
                self.first_clicked = True
                if self.has_bomb:
                    self.loser = True

    # change the image of tile based on its current state
    def state(self):
        if self.first_clicked or self.clicked:
            if not self.has_bomb and not self.flag:
                self.image_index = self.adjacent_bombs+1
        elif self.flag:
            self.image_index = 10
        else:
            self.image_index = 0
        self.image = self.images[self.image_index]
        self.image = pygame.transform.scale(self.image,(self.scale,self.scale))
    
    #resize tile based on the difficulty and if its fullscreen 
    def resize(self):
        global fullscreen
        if not fullscreen:
            if self.difficulty == 1:
                self.scale = 60
                self.offsetx = 130
                self.offsety = 5
            elif self.difficulty == 2:
                self.scale = 40
                self.offsetx = 100
                self.offsety = 24
            elif self.difficulty == 3:
                self.scale = 30
                self.offsetx = 118
                self.offsety = 30
        else:
            if self.difficulty == 1:
                self.scale = 80
                self.offsetx = screen_size[0]/6
                self.offsety = screen_size[1]/100
            elif self.difficulty == 2:
                self.scale = 55
                self.offsetx = screen_size[0]/8
                self.offsety = screen_size[1]/120
            elif self.difficulty == 3:
                self.scale = 40
                self.offsetx = screen_size[0]/7
                self.offsety = screen_size[1]/50
        self.image = pygame.transform.scale(self.image,(self.scale,self.scale))
        if self.x == 0:
            pos_x = self.scale
        else:
            pos_x = self.x*self.scale
        if self.y == 0:
            pos_y = self.scale
        else:
            pos_y = self.y*self.scale
        self.rect = self.image.get_rect(topleft = (pos_x+self.offsetx,pos_y+self.offsety))
            
    # update state of tile
    def update(self):
        self.click()
        self.state()
        if self.first_clicked:
            if not self.loser:
                return (self.x,self.y)
            else:
                return (-2,-2)
        else:
            return (-1,-1)
            