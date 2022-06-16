import pygame
pygame.init()

CLOCK = pygame.time.Clock()

FONT = pygame.font.SysFont("Clear Sans Regular", 72)

NUMBER_OF_ROWS = 5
NUMBER_OF_COLUMNS = 5

PADDING = 10
TILE_SIZE = 125

SCREEN_WIDTH = NUMBER_OF_COLUMNS * TILE_SIZE + (NUMBER_OF_COLUMNS + 1) * PADDING
SCREEN_HEIGHT = NUMBER_OF_ROWS * TILE_SIZE + (NUMBER_OF_ROWS + 1) * PADDING

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN.fill((0, 0, 0))

BACKGROUND_COLOR = (146, 135, 125)

SURFACE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
SURFACE.fill(BACKGROUND_COLOR)

BACKGROUND_COLOR_EMPTY_TILE = (158, 148, 138)
BACKGROUND_TILE_COLORS = {2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121), 16: (245, 149, 99),
                          32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97),
                          512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46), 4096: (237, 191, 30),
                          8192: (0, 0, 0), 16384: (0, 0, 0)}
TILE_TEXT_COLORS = {2: (119, 110, 101), 4: (119, 110, 101), 8: (249, 246, 242), 16: (249, 246, 242),
               32: (249, 246, 242), 64: (249, 246, 242), 128: (249, 246, 242), 256: (249, 246, 242),
               512: (249, 246, 242), 1024: (249, 246, 242), 2048: (249, 246, 242), 4096: (249, 246, 242),
               8192: (249, 246, 242), 16384: (249, 246, 242)}