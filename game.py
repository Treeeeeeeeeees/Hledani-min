from data.parameters import *
from data.player import Player
from data.tiles import Tiles
from data.draw_lib import *

NUMPAD_KEYS = {pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9}

icon = pygame.image.load("data/pictures/img_icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Hledání min")

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((x, y))
        self.display = pygame.Surface((x,y)) #zvlášť povrch na hracím okně na který se všechno vykresluje pro jednodušší manipulaci
        self.running = True #dokud je tato hodnota "True", běží hra
        self.clock = pygame.time.Clock() #počítá uběhnuté milisekundy
        self.time = 0 #hodnota důležitá pro hodiny ve hře
        self.display_time = ""
        self.p_sprites = pygame.sprite.Group() #Player sprite
        self.t_sprites = pygame.sprite.Group() #Tiles sprite
        self.tile_list = [] 
        self.isPlaying = False
        self.gameOverType = ""
        self.shake_duration = 0
        self.shake_check = False
        self.bomb_list_double = []
        self.neigh_num = 0
        self.player = 0
        self.type_screen = 0
        self.bombs = 0
        self.difficulty = [0, 0, 0]
        self.rows = 0
        self.columns = 0
        self.num_input = ["", ""]
        self.num_input_index = 3
        self.start_x = 0
        self.start_y = 0
        self.save = False
        self.save_check = False
        self.name = ""
        self.name_check = False
        self.text_duration = 0
        self.text_type = 0
    
    def valid_neighbors_num(self, i, j, double_array):
        valid_neigh = []
        neighbor_directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] #směry, ve kterých jsou sousedé v dvojitém listu

        for di, dj in neighbor_directions: #pro každou položku (di, dj)
            ni, nj = i + di, j + dj #přesná souřadnice souseda (i, j)

            if 0 <= ni < self.rows and 0 <= nj < self.columns: #kontrola, jestli sousedi existují
                valid_neigh.append(double_array[ni][nj])
        
        neigh_num = 0

        for k in valid_neigh:
            neigh_num += k
        
        return neigh_num
    
    def restart(self): #restartuje všechny relevantní hodnoty do svojí původní podoby
        self.time = 0
        self.p_sprites = pygame.sprite.Group()
        self.t_sprites = pygame.sprite.Group()
        self.tile_list = []
        self.isPlaying = False
        self.gameOverType = ""
        self.shake_duration = 0
        self.shake_check = False
        self.bomb_list_double = []
        self.neigh_num = 0
        self.player = 0
        self.save = False
        self.save_check = False
        self.name = ""

    def create_bomb_list_double(self):
        bomb_num = self.bombs
        bomb_list = []

        for i in range(self.rows * self.columns):

            if bomb_num > 0:
                obj = 1
                bomb_num -= 1
            else:
                obj = 0
            
            bomb_list.append(obj)
        
        random.shuffle(bomb_list)
        k = 0
        for i in range(self.rows):
            bomb_list_double_in = []

            for j in range(self.columns):
                obj2 = bomb_list[k]
                k += 1
                bomb_list_double_in.append(obj2)
            
            self.bomb_list_double.append(bomb_list_double_in)


    def draw_tiles(self, row, column):
        row_neighbors = [row - 1, row, row + 1]
        column_neighbors = [column - 1, column, column + 1]
        self.tile_list.clear()
        placeholder_bomb = 1 if self.bomb_list_double[row][column] == 1 else 0
        self.bomb_list_double[row][column] = 0

        for i in range(self.rows):
            tile_double_list = []

            for j in range(self.columns):
                covered = True

                if self.bomb_list_double[i][j] == 1:
                    bomb = True
                elif self.bomb_list_double[i][j] == 0:

                    if placeholder_bomb == 1 and i != row and j != column:
                        self.bomb_list_double[i][j] = 1
                        bomb = True
                        placeholder_bomb -= 1
                    else:
                        bomb = False

                if j in column_neighbors and i in row_neighbors and self.bomb_list_double[i][j] != 1:
                    covered = False
                
                self.neigh_num = self.valid_neighbors_num(i, j, self.bomb_list_double)
                tile = Tiles((self.start_x + (w_size * j), self.start_y + (w_size * i)), bomb, self.neigh_num, covered, i, j, self.rows, self.columns, self.t_sprites)
                tile_double_list.append(tile)

            self.tile_list.append(tile_double_list)

    def draw_player(self, row, column):
        self.player = Player((self.start_x + column * w_size, self.start_y + row * w_size), self.rows, self.columns, self.bombs, self.p_sprites)

    def update(self, timing, tiles, player_flagging, player_destruction):
        self.display.blit(pygame.image.load("data/pictures/img_bg1.png"), [0,0])
        self.t_sprites.update(tiles)
        self.p_sprites.update(timing, tiles, player_flagging, player_destruction)

        if self.type_screen == 0:
            draw_title_screen(self.display)
        elif self.type_screen == 1:
            draw_other_screens(self.display)
            draw_leaderboard_full(self.display)
        elif self.type_screen == 2:
            draw_other_screens(self.display)
            self.display.blit(pygame.image.load("data/pictures/img_tutorial.png"), [100, 100])
        elif self.type_screen == 3:
            self.difficulty = calculate_difficulty(self.rows, self.columns)
            draw_other_screens(self.display)
            draw_parameters(self.display, self.num_input, self.difficulty)
            draw_button(self.display, x // 2 - 4 * w_size ,y - 150 - 2 * w_size, 8 * w_size, 2 * w_size, w_size, "Hrát")

            if self.num_input[0] != "" and self.num_input[0] != "|":
                if "|" in self.num_input[0]:
                    provisional_rows_with = self.num_input[0]
                    provisional_rows = provisional_rows_with[:-1]
                else:
                    provisional_rows = self.num_input[0]
                self.rows = int(provisional_rows)

            if self.num_input[1] != "" and self.num_input[1] != "|":
                if "|" in self.num_input[1]:
                    provisional_columns_with = self.num_input[1]
                    provisional_columns = provisional_columns_with[:-1]
                else:
                    provisional_columns = self.num_input[1]
                self.columns = int(provisional_columns)

        elif self.type_screen == 4:
            pygame.draw.rect(self.display, (100, 145, 69), pygame.Rect(self.start_x, self.start_y, self.columns * w_size, self.rows * w_size), 0)
            self.t_sprites.draw(self.display)
            self.p_sprites.draw(self.display)
            draw_grid(self.display, self.rows, self.columns, self.start_x, self.start_y, w_size)
            draw_clock(self.display, self.isPlaying, self.time, self.display_time, self.start_x, self.start_y, timing)
            self.time = draw_clock_time(self.isPlaying, self.time, timing)
            self.display_time = draw_clock_display(self.isPlaying, self.time, self.display_time,timing)
            draw_button(self.display, 50, 50, 2 * w_size, 2 * w_size, w_size, "<")

            if self.isPlaying == True:
                draw_remaining_bombs(self.display, self.start_x, self.start_y, self.columns, self.player.flagged)
                self.isPlaying = self.player.isPlaying
            else:
                if self.player != 0:
                    draw_remaining_bombs(self.display, self.start_x, self.start_y, self.columns, self.player.flagged)
                    self.gameOverType = self.player.gameOverType
                    draw_restart(self.display, self.gameOverType)

                    if self.gameOverType == "Loss":

                        if self.shake_check == False:
                            self.shake_duration = 50
                            self.shake_check = True

                    if self.gameOverType == "Win":

                        if self.save == True:
                            draw_leaderboard_save(self.display, self.name)
                    
    #game loop
    def run(self): 
        while self.running:
            timing = self.clock.tick() / 1000
            player_flagging = False
            player_destruction = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE): #vypnutí hry
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:

                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()

                        if self.type_screen == 0: #Titulní stránka

                            if (x // 2 - 4 * w_size) < mouse_pos[0] < (x // 2 + 4 * w_size) and (y // 2) < mouse_pos[1] < (y // 2 + 2 * w_size): #Tlačítko "Nová hra": začít novou hru
                                self.type_screen = 3
                            elif (x // 2 - 4 * w_size) < mouse_pos[0] < (x // 2 + 4 * w_size) and (y // 2 + 3 * w_size) < mouse_pos[1] < (y // 2 + 5 * w_size): #Tlačítko "Žebříček": zobrazit žebříček
                                self.type_screen = 1
                            elif (x // 2 - 4 * w_size) < mouse_pos[0] < (x // 2 + 4 * w_size) and (y // 2 + 6 * w_size) < mouse_pos[1] < (y // 2 + 8 * w_size): #Tlačítko "Jak hrát": zobrazit jednoduchý obrázek s instrukcemi jak hrát
                                self.type_screen = 2
                            elif (x // 2 - 4 * w_size) < mouse_pos[0] < (x // 2 + 4 * w_size) and (y // 2 + 9 * w_size) < mouse_pos[1] < (y // 2 + 11 * w_size): #Tlačítko "Konec": vypnutí hry
                                self.running = False
                        elif self.type_screen == 1: #Stránka s žebříckem

                            if 50 < mouse_pos[0] < (50 + 2 * w_size) and 50 < mouse_pos[1] < (50 + 2 * w_size): #Tlačítko "<": zpátky na titulní stránku
                                self.type_screen = 0
                            elif (x // 2 - 4 * w_size) < mouse_pos[0] < (x // 2 + 4 * w_size) and (y - 150 - 2 * w_size) < mouse_pos[1] < (y - 150): #Tlačítko "Vyčistit": vyčistit žebříček
                                with open('data/leaderboard.json', 'r+') as file:
                                    try:
                                        current_json = json.load(file)
                                        current_leaderboard = current_json["Leaderboard"]
                                    except json.decoder.JSONDecodeError:
                                        current_leaderboard = []
                                    current_leaderboard = []
                                    current_json["Leaderboard"] = current_leaderboard
                                    file.seek(0)
                                    json.dump(current_json, file)
                                    file.truncate()            
                        elif self.type_screen == 2: #Stránka, jak hrát

                            if 50 < mouse_pos[0] < (50 + 2 * w_size) and 50 < mouse_pos[1] < (50 + 2 * w_size): #Tlačítko "<": zpátky na titulní stránku
                                self.type_screen = 0

                        elif self.type_screen == 3: #Stránka s nastavitelnými parametry hry

                            if 50 < mouse_pos[0] < (50 + 2 * w_size) and 50 < mouse_pos[1] < (50 + 2 * w_size): #Tlačítko "<": zpátky na titulní stránku
                                self.type_screen = 0

                            elif (x // 2 - 5 * w_size) < mouse_pos[0] < (x // 2 + 5 * w_size) and (y // 2 - 6 * w_size) < mouse_pos[1] < (y // 2 - 5 * w_size): #Zapisovací pole "Řádky"
                                self.num_input_index = 0

                            elif (x // 2 - 5 * w_size) < mouse_pos[0] < (x // 2 + 5 * w_size) and (y // 2 - 3 * w_size) < mouse_pos[1] < (y // 2 - 2 * w_size): #Zapisovací pole "Sloupce"
                                self.num_input_index = 1

                            elif (x // 2 - 10 * w_size) < mouse_pos[0] < (x // 2 - 4 * w_size) and (y // 2 + 2 * w_size) < mouse_pos[1] < (y // 2 + 4 * w_size): #Tlačítko lehká obtížnost
                                self.bombs = self.difficulty[0]
                                self.text_duration = 200
                                self.text_type = 0
                                self.num_input_index = 2

                            elif (x // 2 - 3 * w_size) < mouse_pos[0] < (x // 2 + 3 * w_size) and (y // 2 + 2 * w_size) < mouse_pos[1] < (y // 2 + 4 * w_size): #Tlačítko střední obtížnost
                                self.bombs = self.difficulty[1]
                                self.text_duration = 200
                                self.text_type = 1
                                self.num_input_index = 2

                            elif (x // 2 + 4 * w_size) < mouse_pos[0] < (x // 2 + 10 * w_size) and (y // 2 + 2 * w_size) < mouse_pos[1] < (y // 2 + 4 * w_size): #Tlačítko těžká obtížnost
                                self.bombs = self.difficulty[2]
                                self.text_duration = 200
                                self.text_type = 2
                                self.num_input_index = 2

                            elif (x // 2 - 4 * w_size) < mouse_pos[0] < (x // 2 + 4 * w_size) and (y - 150 - 2 * w_size) < mouse_pos[1] < (y - 150): #Tlačítko "Hrát": spustit hru

                                if 10 <= self.rows <= 23 and 10 <= self.columns <= 30 and 1 <= self.bombs < (self.rows * self.columns - 20):
                                    self.type_screen = 4
                                    self.start_x = (x - w_size * self.columns) // 2
                                    self.start_y = (y - w_size * self.rows) // 2
                                else:
                                    self.text_duration = 200
                                    self.text_type = 3
                            else:
                                self.num_input_index = 2

                            for i in range(len(self.num_input)):
                                current_index = self.num_input[i]

                                if i == self.num_input_index and i < 2:
                                    if current_index == "":
                                        current_index = "|"
                                    
                                    if "|" not in current_index:
                                        current_index = current_index + "|"
                                else:
                                    if current_index == "|":
                                        current_index = ""
                                    else:
                                        if "|" in current_index:
                                            current_index = current_index[:-1]
                                
                                self.num_input[i] = current_index
                        elif self.type_screen == 4: #Stránka, na které je hra samotná

                            if self.gameOverType == "": #Kontroluje, jestli není konec hry

                                if self.start_x < mouse_pos[0] < (self.start_x + self.columns * w_size) and self.start_y < mouse_pos[1] < (self.start_y + self.rows * w_size): #Určení počáteční pozice před začátkem hry
                                    row = (mouse_pos[1] - self.start_y) // w_size
                                    column = (mouse_pos[0] - self.start_x) // w_size

                                    if self.isPlaying == False:
                                        self.isPlaying = True
                                        self.create_bomb_list_double()
                                        self.draw_tiles(row, column)
                                        self.draw_player(row, column)
                            elif self.gameOverType == "Loss": #Konec hry, prohra

                                if (x // 2 - 3 * w_size) < mouse_pos[0] < (x // 2 + 3 * w_size) and (y // 2 + w_size) < mouse_pos[1] < (y // 2 + 3 * w_size): #Tlačítko "Restart": restart hry se stejnými parametry
                                    self.restart()
                            else: #Konec hry, výhra

                                if self.save == False: #Okénko bez uložení

                                    if (x // 2 - 7 * w_size) < mouse_pos[0] < (x // 2 - w_size) and (y // 2 + w_size) < mouse_pos[1] < (y // 2 + 3 * w_size): #Tlačítko "Restart": restart hry se stejnými parametry
                                        self.restart()
                                    elif (x // 2 + w_size) < mouse_pos[0] < (x // 2 + 7 * w_size) and (y // 2 + w_size) < mouse_pos[1] < (y // 2 + 3 * w_size): #Tlačítko "Uložit": přesunutí na stránku s možností uložit výsledek
                                        self.save = True
                                else: #Okénko s uložením

                                    if (x // 2 - 7 * w_size) < mouse_pos[0] < (x // 2 - w_size) and (y // 2 + w_size) < mouse_pos[1] < (y // 2 + 3 * w_size): #Tlačítko "Zpět": zpátky na předchozí stránku
                                        self.save = False
                                        self.name_check = False
                                        self.name = ""
                                    elif (x // 2 + w_size) < mouse_pos[0] < (x // 2 + 7 * w_size) and (y // 2 + w_size) < mouse_pos[1] < (y // 2 + 3 * w_size): #Tlačítko "Uložit": uložit výsledek
                                        self.text_duration = 200
                                        
                                        if (self.name != "" or self.name != "|") and self.save_check == False:
                                            if "|" in self.name:
                                                saved_name = self.name[:-1]
                                            else:
                                                saved_name = self.name

                                            data = {
                                                "name": saved_name,
                                                "display_time": self.display_time,
                                                "time": self.time
                                            }
                                            with open('data/leaderboard.json', 'r+') as file:
                                                try:
                                                    current_json = json.load(file)
                                                    current_leaderboard = current_json["Leaderboard"]
                                                except json.decoder.JSONDecodeError:
                                                    current_leaderboard = []
                                                
                                                leaderboard_length = len(current_leaderboard)

                                                if leaderboard_length != 0:
                                                    for i in range(leaderboard_length):
                                                        current_point = current_leaderboard[i]
                                                        if current_point == data:
                                                            break
                                                        if current_point["time"] > self.time:
                                                            current_leaderboard.insert(i, data)
                                                            self.text_type = 4
                                                            self.save_check = True
                                                            if leaderboard_length >= 12:
                                                                current_leaderboard.pop()
                                                            break
                                                        if i == 11:
                                                            self.text_type = 6
                                                            break
                                                        else:
                                                            if i == (leaderboard_length - 1):
                                                                self.text_type = 4
                                                                self.save_check = True
                                                                current_leaderboard.append(data)
                                                else:
                                                    current_leaderboard.append(data)
                                                    self.text_type = 4
                                                    self.save_check = True

                                                current_json["Leaderboard"] = current_leaderboard
                                                file.seek(0)
                                                json.dump(current_json, file)
                                        else:
                                            if self.save_check == True:
                                                self.text_type = 5
                                            else:
                                                self.text_type = 7

                                    elif (x // 2 - 7 * w_size) < mouse_pos[0] < (x // 2 + 7 * w_size) and (y // 2 - w_size) < mouse_pos[1] < (y // 2): #Zapisovací okénko "Jméno"
                                        self.name_check = True
                                        if "|" not in self.name:
                                            self.name = self.name + "|"
                                    else:
                                        self.name_check = False
                                        if "|" in self.name:
                                            self.name = self.name[:-1]
                                        else:
                                            self.name = self.name

                            if 50 < mouse_pos[0] < (50 + 2 * w_size) and 50 < mouse_pos[1] < (50 + 2 * w_size): #Tlačítko "<": zpátky na titulní stránku
                                self.type_screen = 0
                                self.restart()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and self.isPlaying == True:
                    player_flagging = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.isPlaying == True:
                    player_destruction = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:

                    if self.type_screen == 3:
                        if self.num_input_index < 2:
                            current_input = self.num_input[self.num_input_index]
                            current_input = current_input[:len(current_input) - 2]
                            self.num_input[self.num_input_index] = current_input + "|"

                            if self.num_input_index == 0:
                                self.rows = 0
                            if self.num_input_index == 1:
                                self.columns = 0

                    if self.type_screen == 4:
                        self.name = self.name[:len(self.name) - 2] + "|"

                if self.type_screen == 3:

                    if self.num_input_index < 2:

                        if event.type == pygame.KEYDOWN and event.key != pygame.K_BACKSPACE:

                            if self.num_input[self.num_input_index] == "|":
                                self.num_input[self.num_input_index] = ""

                            provisional_var1 = self.num_input[self.num_input_index]
                            provisional_var2 = provisional_var1[:-1]

                            if pygame.key.name(event.key).isdigit():
                                self.num_input[self.num_input_index] = provisional_var2 + pygame.key.name(event.key) + "|"

                            if event.key in NUMPAD_KEYS:
                                self.num_input[self.num_input_index] = provisional_var2 + event.unicode + "|"

                if self.type_screen == 4 and self.save == True and self.name_check == True:

                    if event.type == pygame.KEYDOWN and event.key != pygame.K_BACKSPACE and len(self.name) <= 20:

                        if self.name == "|":
                            self.name = ""
                        if "|" in self.name:
                            placeholder_name = self.name[:-1]
                        else:
                            placeholder_name = self.name

                        self.name = placeholder_name + event.unicode + "|"

            self.update(timing, self.tile_list, player_flagging, player_destruction)
            
            if self.text_duration > 0: #Zobrazení textu na pár sekund jako vizuální indikátor spuštěného tlačítka
                self.text_duration -= 1

                if self.type_screen == 3:
                    if self.text_type == 0:
                        warning = "Vybrána lehká obtížnost!"
                    elif self.text_type == 1:
                        warning = "Vybrána střední obtížnost!"
                    elif self.text_type == 2:
                        warning = "Vybrána těžká obtížnost!"
                    elif self.text_type == 3:
                        warning = "Tyto parametry nejsou povoleny!"
                    else:
                        warning = ""
                
                if self.type_screen == 4 and self.save == True:
                    if self.text_type == 4:
                        warning = "Uloženo!"
                    elif self.text_type == 5:
                        warning = "Toto kolo už jsi uložil!"
                    elif self.text_type == 6:
                        warning = "Plný žebříček, pomalý výsledek!"
                    elif self.text_type == 7:
                        warning = "Jiný problém, nevím co."
                    else:
                        warning = ""
                
                font = pygame.font.Font("freesansbold.ttf", w_size)
                text = font.render(warning, True, "white")
                textRect = text.get_rect()

                if self.type_screen == 3:
                    textRect.center = (x // 2, y - 150 + w_size)
                    self.display.blit(text, textRect)

                elif self.type_screen == 4 and self.save == True:
                    textRect.center = (x // 2, y // 2 - 3 * w_size)
                    self.display.blit(text, textRect)
                else:
                    pass
            
            render_offset = [0, 0]

            if self.shake_duration > 0: #zatřesení displeje
                self.shake_duration -= 1
                render_offset[0] = random.randint(0,8) - 4
                render_offset[1] = random.randint(0,8) - 4
            
            self.screen.blit(self.display, render_offset)
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    newGame = Game()
    newGame.run()