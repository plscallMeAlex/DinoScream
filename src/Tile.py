import pygame

# Load the image that contains the game sprites
IMAGE = pygame.image.load("resources/game_sprites.png")

# Constants position of the tile in the image
START_POS = (0, 53)
TILE_WIDTH = 1203
TILE_HEIGHT = 14

GAP_DINO = 10
SCROLL_SPEED = 5


class Tile:
    def __init__(self, dino_rect):
        self.under_dino = dino_rect.bottom
        self.tile_width = TILE_WIDTH  # Width of each tile
        self.tile_rect = pygame.Rect(
            START_POS[0], START_POS[1], TILE_WIDTH, TILE_HEIGHT
        )

        self.offset = 0  # Scrolling offset

    def draw(self, screen):
        """Draws the tiles on the screen with a looping effect."""
        y_pos = self.under_dino - GAP_DINO
        screen.blit(IMAGE, (self.offset, y_pos), self.tile_rect)
        screen.blit(IMAGE, (self.offset + self.tile_width, y_pos), self.tile_rect)

        self.offset -= SCROLL_SPEED
        if self.offset <= -self.tile_width:
            self.offset = 0

    def stop(self):
        self.offset = 0