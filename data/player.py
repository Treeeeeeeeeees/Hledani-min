from types import NoneType
from data.parameters import *

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, rows, columns, bombs, groups):
        super().__init__(groups)
        self.facing = 0
        self.moving = False
        self.display_timer_1 = 0
        self.display_timer_2 = 0
        self.image_display(False, False)
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = self.pos
        self.speed = 100
        self.flagged = bombs
        self.bombs = bombs
        self.flagged_correctly = 0
        self.isPlaying = True
        self.gameOverType = ""
        self.rows = rows
        self.columns = columns
        self.start_x = (x - w_size * self.columns) // 2
        self.start_y = (y - w_size * self.rows) // 2

    def image_display(self, player_flagging, player_destruction): #Vybírá sprite, který se zobrazí jako hráč dle situace
        if self.facing == 0:
            if self.moving == True:
                self.image = self.image = pygame.image.load("data/pictures/img_player_back_2.png")
            else:
                
                if player_destruction == True:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_back_3.png")
                    self.display_timer_1 = 30

                elif self.display_timer_1 > 0:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_back_3.png")
                    self.display_timer_1 -= 1

                elif player_flagging == True:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_back_4.png")
                    self.display_timer_2 = 30

                elif self.display_timer_2 > 0:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_back_4.png")
                    self.display_timer_2 -= 1

                else:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_back_1.png")

        elif self.facing == 1:
            
            if self.moving == True:
                self.image = self.image = pygame.image.load("data/pictures/img_player_front_2.png")
            else:

                if player_destruction == True:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_front_3.png")
                    self.display_timer_1 = 30

                elif self.display_timer_1 > 0:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_front_3.png")
                    self.display_timer_1 -= 1
                
                elif player_flagging == True:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_front_4.png")
                    self.display_timer_2 = 30

                elif self.display_timer_2 > 0:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_front_4.png")
                    self.display_timer_2 -= 1
                    
                else:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_front_1.png")
        
        elif self.facing == 2:
            if self.moving == True:
                self.image = self.image = pygame.image.load("data/pictures/img_player_left_2.png")
            else:
                
                if player_destruction == True:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_left_3.png")
                    self.display_timer_1 = 30

                elif self.display_timer_1 > 0:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_left_3.png")
                    self.display_timer_1 -= 1

                elif player_flagging == True:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_left_4.png")
                    self.display_timer_2 = 30

                elif self.display_timer_2 > 0:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_left_4.png")
                    self.display_timer_2 -= 1
                    
                else:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_left_1.png")

        elif self.facing == 3:
            if self.moving == True:
                self.image = self.image = pygame.image.load("data/pictures/img_player_right_2.png")
            else:
                
                if player_destruction == True:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_right_3.png")
                    self.display_timer_1 = 30

                elif self.display_timer_1 > 0:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_right_3.png")
                    self.display_timer_1 -= 1

                elif player_flagging == True:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_right_4.png")
                    self.display_timer_2 = 30

                elif self.display_timer_2 > 0:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_right_4.png")
                    self.display_timer_2 -= 1
                    
                else:
                    self.image = self.image = pygame.image.load("data/pictures/img_player_right_1.png")

    def get_input(self): #Hledá vstupy
        pressed_keys = pygame.key.get_pressed()

        #pohyb

        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:

            if self.pos[1] > (self.start_y + w_size):
                self.direction = self.pos + pygame.math.Vector2(0, -w_size)
                self.moving = True
                self.facing = 0

        elif pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:

            if self.pos[1] < (self.start_y + (self.rows - 1) * w_size):
                self.direction = self.pos + pygame.math.Vector2(0, w_size)
                self.moving = True
                self.facing = 1

        elif pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:

            if self.pos[0] > (self.start_x + w_size):
                self.direction = self.pos + pygame.math.Vector2(-w_size, 0)
                self.moving = True
                self.facing = 2

        elif pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:

            if self.pos[0] < (self.start_x + (self.columns - 1) * w_size):
                self.direction = self.pos + pygame.math.Vector2(w_size, 0)
                self.moving = True
                self.facing = 3
        
        else:
            self.direction = self.pos

    def target_tile(self, tiles): #Mezi objekty Tiles najde ten, který je před hráčem

        for i in range(self.rows):

            for j in range(self.columns):
                tile = tiles[i][j]

                if self.direction == tile.pos:
                    current_i = i
                    current_j = j
                    break

        neighbor_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        target_direction = neighbor_directions[self.facing]
        target_i, target_j = current_i + target_direction[1], current_j + target_direction[0]

        if 0 <= target_i < self.rows and 0 <= target_j < self.columns:
            target_tile = tiles[target_i][target_j]
            return target_tile

    def destruction(self, tiles): #Odhalí objekt Tiles před ním
        target_tile = self.target_tile(tiles)

        if target_tile != NoneType():

            if target_tile.isCovered == True and target_tile.isFlagged == False:
                target_tile.isCovered = False
                break_sfx = pygame.mixer.Sound("data/sound/break_sfx.mp3")
                break_sfx.play()

                if target_tile.isBomb == True:
                    self.gameOverType = "Loss"
                    self.game_over(tiles)

    def flagging(self, tiles): #Označí objekt Tiles vlaječkou
        target_tile = self.target_tile(tiles)

        if target_tile != NoneType():

            if target_tile.isCovered == True:
                place_sfx = pygame.mixer.Sound("data/sound/place_sfx.mp3")
                place_sfx.play()
                
                if target_tile.isFlagged == False:
                    if self.flagged != 0:
                        target_tile.isFlagged = True
                        self.flagged -= 1
                        if target_tile.isBomb == True:
                            self.flagged_correctly += 1

                else:
                    target_tile.isFlagged = False
                    self.flagged += 1
                    if target_tile.isBomb == True:
                        self.flagged_correctly -= 1
                        
        if self.flagged_correctly == self.bombs:
                self.gameOverType = "Win"
                self.game_over(tiles)

    def collision(self, tiles): #Kolize

        for i in range(self.rows):

            for j in range(self.columns):
                tile = tiles[i][j]

                if self.direction == tile.pos:
                    if tile.isFlagged == False and tile.isCovered == True:
                        self.direction = self.pos
                    break

    def movement(self, timing): #Realizuje plynulý pohyb
        if self.moving == True:
            self.pos = self.pos.move_towards(self.direction, self.speed * timing)

        if self.pos == self.direction:
            self.moving = False

        self.rect.center = self.pos
    
    def update(self, timing, tiles, player_flagging, player_destruction): #Vyvolá se každý tick
        if self.isPlaying == True:

            if not self.moving:
                self.get_input()
                self.collision(tiles)
                
            self.movement(timing)

            if player_flagging == True:
                self.flagging(tiles)
            elif player_destruction == True:
                self.destruction(tiles)
            
            self.image_display(player_flagging, player_destruction)
        
    def game_over(self, tiles): #Kontroluje konec hry

        for i in range(self.rows):

            for j in range(self.columns):
                tile = tiles[i][j]

                if tile.isBomb == True and tile.isFlagged == False:
                    tile.isCovered = False
        self.isPlaying = False
        if self.gameOverType == "Win":
            endgame_sfx = pygame.mixer.Sound("data/sound/victory_sfx.mp3")
        else:
            endgame_sfx = pygame.mixer.Sound("data/sound/loss_sfx.mp3")

        endgame_sfx.play()