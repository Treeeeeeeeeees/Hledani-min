from data.parameters import *

class Tiles(pygame.sprite.Sprite):

    def __init__(self, pos, bomb, neighbours, covered, row, column, rows, columns, groups):
        super().__init__(groups)
        self.isBomb = bomb
        self.neighbours = neighbours
        self.isCovered = covered
        if self.neighbours > 0:
            self.isNumber = True
        else:
            self.isNumber = False
        self.isFlagged = False
        self.image_display()
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.row = row
        self.column = column
        self.rows = rows
        self.columns = columns

    def image_display(self): #načítání obrázků
        if self.isCovered == True:
            if self.isFlagged:
                self.image = pygame.image.load("data/pictures/img_flag.png")
            else:
                self.image = pygame.image.load("data/pictures/img_covered.png")
        elif self.isCovered == False:
            if self.isBomb == True:
                self.image = pygame.image.load("data/pictures/img_bomb.png")

            elif self.neighbours > 0: 
                if self.neighbours == 1:
                    self.image = pygame.image.load("data/pictures/img_num1.png")
                elif self.neighbours == 2:
                    self.image = pygame.image.load("data/pictures/img_num2.png")
                elif self.neighbours == 3:
                    self.image = pygame.image.load("data/pictures/img_num3.png")
                elif self.neighbours == 4:
                    self.image = pygame.image.load("data/pictures/img_num4.png")
                elif self.neighbours == 5:
                    self.image = pygame.image.load("data/pictures/img_num5.png")
                elif self.neighbours == 6:
                    self.image = pygame.image.load("data/pictures/img_num6.png")
                elif self.neighbours == 7:
                    self.image = pygame.image.load("data/pictures/img_num7.png")
                elif self.neighbours == 8:
                    self.image = pygame.image.load("data/pictures/img_num8.png")

            else:
                self.image = pygame.image.load("data/pictures/img_empty.png")
    
    def valid_neighbors(self, tiles):
        valid_neigh = []
        neighbor_directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for di, dj in neighbor_directions:
            ni, nj = self.row + di, self.column + dj
            if 0 <= ni < self.rows and 0 <= nj < self.columns:
                neighbor_tile = tiles[ni][nj]
                if neighbor_tile.isCovered and not neighbor_tile.isBomb:
                    valid_neigh.append(neighbor_tile)
        return valid_neigh
    
    def reveal_neighbors(self, tiles):
        neighbors = self.valid_neighbors(tiles)
        for neighbor in neighbors:
            if neighbor.isCovered == True and neighbor.isBomb == False and neighbor.isFlagged == False:
                neighbor.isCovered = False
    
    def update(self, tiles):
        if self.isCovered == False:
            if self.isNumber == False and self.isBomb == False:
                self.reveal_neighbors(tiles)
        self.image_display()