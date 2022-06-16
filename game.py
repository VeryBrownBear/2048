import pygame
pygame.init()
import config
from numpy import array, array_equal, zeros, rot90
from random import random, randint
from sys import maxsize
from math import pow
from copy import deepcopy

class Game:
    def __init__(self):
        self.game_over = False
        self.pressed = False
        self.player = 0 # 0 for tile mover, 1 for tile placer
        self.grid = zeros((config.NUMBER_OF_ROWS, config.NUMBER_OF_COLUMNS))
        self.score = 0
        self.moves = []
    
    def draw_board(self):
        row = pygame.Surface((config.SCREEN_WIDTH, config.TILE_SIZE + config.PADDING), pygame.SRCALPHA, 32)
        row = row.convert_alpha()

        for c in range(config.NUMBER_OF_COLUMNS):
            tile = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE))
            tile.fill(config.BACKGROUND_COLOR_EMPTY_TILE)
            row.blit(tile, (config.PADDING + c *(config.PADDING + config.TILE_SIZE), config.PADDING))

        for r in range(config.NUMBER_OF_ROWS):
            config.SURFACE.blit(row, (0, (config.PADDING + config.TILE_SIZE) * r))

    def draw_tile(self, row, col, tile_value):
        tile = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE))
        tile.fill(config.BACKGROUND_TILE_COLORS[tile_value])
        text = config.FONT.render(str(int(tile_value)), True, config.TILE_TEXT_COLORS[tile_value])
        text_width, text_height = text.get_size()
        tile.blit(text, ((config.TILE_SIZE - text_width) // 2, (config.TILE_SIZE - text_height) // 2))
        config.SURFACE.blit(tile, (config.PADDING + (config.PADDING + config.TILE_SIZE) * col, config.PADDING + (config.PADDING + config.TILE_SIZE) * row))

    def draw_tiles(self):
        for r in range(config.NUMBER_OF_ROWS):
            for c in range(config.NUMBER_OF_COLUMNS):
                if self.grid[r][c] != 0:
                    self.draw_tile(r, c, self.grid[r][c])

    def add_random_tile(self):
        i, j = (self.grid == 0).nonzero()
        if i.size != 0:
            random_index = randint(0, i.size - 1)
            self.grid[i[random_index], j[random_index]] = 2 * ((random() > 0.9) + 1)

    def move_left(self, col):
        new_col = zeros((config.NUMBER_OF_COLUMNS), dtype = col.dtype)
        j = 0
        previous = None
        for i in range(col.size):
            if col[i] != 0:
                if previous == None:
                    previous = col[i]
                else:
                    if previous == col[i]:
                        new_value = 2 * col[i]
                        new_col[j] = new_value
                        self.score += new_value
                        j += 1
                        previous = None
                    else:
                        new_col[j] = previous
                        j += 1
                        previous = col[i]
        if previous != None:
            new_col[j] = previous
        return new_col
    
    def move(self):
        rotated_board = rot90(self.grid, self.direction)
        cols = [rotated_board[i, :] for i in range(config.NUMBER_OF_COLUMNS)]
        new_board = array([self.move_left(col) for col in cols])
        self.grid = rot90(new_board, -self.direction)
        changed = False
        if not array_equal(rotated_board, new_board):
            changed = True
            self.add_random_tile()
        return changed

    def play_move(self, direction):
        self.direction = direction
        self.move()
        self.game_over = self.is_game_over()

    # Checks if there are any mergable or empty spaces in the rows
    def check_rows(self):
        for row in self.grid:
            for x, y in zip(row[:-1], row[1:]):
                if x == y or x == 0 or y == 0:
                    return True
        return False
    
    # Checks if there are any mergable or empty spaces in the columns
    def check_cols(self):
        for col in zip(*self.grid):
            for x, y in zip(col[:-1], col[1:]):
                if x == y or x == 0 or y == 0:
                    return True
        return False

    # Checks if the game is over by checking if there are no mergable or empty spaces
    def is_game_over(self):
        return not self.check_rows() and not self.check_cols()

    # Creates a new game board with move played
    def make_new_game(self, direction):
        new_game = deepcopy(self)
        new_game.direction = direction
        new_game.move()
        new_game.player = 1
        return new_game

    def make_new_game_with_tile_placed(self, position, tile_value):
        new_game = deepcopy(self)
        new_game.grid[position[0]][position[1]] = tile_value
        new_game.player = 0
        return new_game

    def scoring(self):
        if self.is_game_over(): return -maxsize

        snake_line = []
        for i, col in enumerate(zip(*self.grid)):
            snake_line.extend(reversed(col) if i % 2 == 0 else col)

        m = max(snake_line)
        return sum(x / 10 ** n for n, x in enumerate(snake_line)) - pow((self.grid[config.NUMBER_OF_ROWS - 1][0] != m) * abs(self.grid[config.NUMBER_OF_ROWS - 1][0] - m), 2)

    def expectimax(self, depth):
        if depth == 0 or (self.player == 0 and self.is_game_over()):
            return self.scoring()

        score = -maxsize

        # Tile mover
        if self.player == 0:
            for direction in range(0, 4):
                new_game = self.make_new_game(direction)
                new_score = new_game.expectimax(depth - 1)
                if new_score > score:
                    score = new_score
                self.moves.append((direction, new_score))
        # Tile placer
        else:
            score = 0
            i, j = (self.grid == 0).nonzero()
            for x, y in zip(i, j):
                new_game_2 = self.make_new_game_with_tile_placed((x, y), 2)
                new_game_4 = self.make_new_game_with_tile_placed((x, y), 4)
                score += .9 * new_game_2.expectimax(depth - 1) / i.size + .1 * new_game_4.expectimax(depth - 1) / i.size
        return score

    # Game loop logic
    def play(self, ai_playing):
        self.draw_board()
        self.add_random_tile()
        self.add_random_tile() 
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN and self.pressed == False:
                    self.pressed = True
                if event.type == pygame.KEYUP and self.pressed == True:
                    self.pressed = False
                    if event.key == pygame.K_LEFT:
                        self.play_move(0)
                    if event.key == pygame.K_UP:
                        self.play_move(1)
                    if event.key == pygame.K_RIGHT:
                        self.play_move(2)
                    if event.key == pygame.K_DOWN:
                        self.play_move(3)
            if ai_playing:
                self.old_grid = self.grid
                self.expectimax(3)
                self.moves = sorted(self.moves, key=lambda x:x[1], reverse=True)
                print(self.moves)
                best_move = self.moves[0][0]
                self.play_move(best_move)
                i = 1
                while array_equal(self.grid, self.old_grid):
                    best_move = self.moves[i][0]
                    self.play_move(best_move)
                    i += 1
                self.moves = []
            self.draw_board()
            self.draw_tiles()
            config.SCREEN.blit(config.SURFACE, (0, 0))
            pygame.display.flip()
        pygame.time.wait(2000)