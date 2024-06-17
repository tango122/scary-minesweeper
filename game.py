import pygame
import random
from tile import Tile
from config import screen

# class for the minesweeper game
class Game:
    # initialize game and its elements
    def __init__(self):
        self.difficulty = 0
        self.rows = 0
        self.columns = 0
        self.all_tiles = pygame.sprite.Group()
        self.ended = False
        self.first_click = False
        self.bombs = 0
        self.bomb_pos = []
        self.win = False
        
    # checks if player has won the game
    def check_win(self):
        for i in self.all_tiles:
            if i.y == 0 or i.x == 0:
                pass
            elif not i.clicked and not i.first_clicked and not i.has_bomb:
                return False
        return True
        
    # sets difficulty of the game
    def set_difficulty(self):
        if self.difficulty == 1:
            self.rows = 10
            self.columns = 10
            self.bombs = 10
        elif self.difficulty == 2:
            self.rows = 14
            self.columns = 18
            self.bombs = 40
        elif self.difficulty == 3:
            self.rows = 20
            self.columns = 24
            self.bombs = 99
    
    # construct the game grid with the Tile object
    def make_grid(self):
        self.first_click = False
        self.ended = False
        self.set_difficulty()
        for i in range(0,self.columns+1):
            for j in range(0,self.rows+1):
                self.all_tiles.add(Tile(i,j,self.difficulty))
                
    # clears adjacent tiles after a click
    def clear_tiles(self,x,y):
        if self.get_tile(x,y) == None:
            return
        if self.get_tile(x,y).clicked:
            return
        if self.get_tile(x,y).adjacent_bombs > 0:
            self.get_tile(x,y).clicked = True
            return
        if self.get_tile(x,y).adjacent_bombs == 0:  
            self.get_tile(x,y).clicked = True
            self.clear_tiles(x+1,y)
            self.clear_tiles(x-1,y)
            self.clear_tiles(x,y+1)
            self.clear_tiles(x,y-1)
            self.clear_tiles(x-1,y-1)
            self.clear_tiles(x+1,y+1)
            self.clear_tiles(x+1,y-1)
            self.clear_tiles(x-1,y+1)
            
        
    #returns the Tile object of the input coordinate 
    def get_tile(self,x,y):
        for i in self.all_tiles:
            if i.x == x and i.y == y:
                return i
        return
                
    # place bombs randomly on game grid and initialize adjacent bomb states for tiles
    def place_bombs(self):
        placed = 0
        while placed < self.bombs:
            x = random.randint(1,self.columns)
            y = random.randint(1,self.rows)
            tile = self.get_tile(x,y)
            if not tile.clicked:
                if not tile.has_bomb:
                    tile.has_bomb = True
                    placed += 1
                    self.bomb_pos.append((x,y))
        for i in self.bomb_pos:
            right = self.get_tile(i[0]+1,i[1])
            left = self.get_tile(i[0]-1,i[1])
            up = self.get_tile(i[0],i[1]-1)
            down = self.get_tile(i[0],i[1]+1)
            topleft = self.get_tile(i[0]-1,i[1]-1)
            topright = self.get_tile(i[0]+1,i[1]-1)
            bottomleft = self.get_tile(i[0]-1,i[1]+1)
            bottomright = self.get_tile(i[0]+1,i[1]+1)
            if not right == None:
                if not right.has_bomb:
                    right.adjacent_bombs+=1
            if not left == None:
                if not left.has_bomb:
                    left.adjacent_bombs+=1
            if not up == None:
                if not up.has_bomb:
                    up.adjacent_bombs+=1
            if not down == None:
                if not down.has_bomb:
                    down.adjacent_bombs+=1
            if not topleft == None:
                if not topleft.has_bomb:
                    topleft.adjacent_bombs+=1
            if not topright == None:
                if not topright.has_bomb:
                    topright.adjacent_bombs+=1
            if not bottomleft == None:
                if not bottomleft.has_bomb:
                    bottomleft.adjacent_bombs+=1
            if not bottomright == None:
                if not bottomright.has_bomb:
                    bottomright.adjacent_bombs+=1
            
    # handles right click action
    def right_click(self):
        for i in self.all_tiles:
            i.right_click()
            i.state()
        
    # handles left click action; places bombs if the first click and updates game state
    def click(self):
        if not self.first_click:
            self.first_click = True
            for i in self.all_tiles:
                i.update()
            self.place_bombs()
            
        for i in self.all_tiles:
            clicked_tile = i.update()
            if clicked_tile[0] == -2:
                self.all_tiles.empty()
                self.bomb_pos.clear()
                self.ended = True
                return True
            if not clicked_tile[0] == -1:
                self.clear_tiles(clicked_tile[0],clicked_tile[1])
            i.update()
        self.win = self.check_win()
        return False
                
    # updates visual of board and resets game state if game ends with a win
    def update(self):
        if not self.ended:
            if self.first_click:
                if self.win:
                    global win
                    global game_over
                    self.all_tiles.empty()
                    self.bomb_pos.clear()
                    self.first_click = False
                    win = True
                    game_over = True
        for i in self.all_tiles:
            i.resize()
        self.all_tiles.draw(screen)
        