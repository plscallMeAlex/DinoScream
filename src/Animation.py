import pygame

SPRITE_SHEET = pygame.image.load("resources/game_sprites.png")


# Animation class to store the animation of the sprite


class Animation:
    def __init__(self, start_point=(0, 0), width=50, height=50, frames: int = 1):
        self.start_point = start_point
        self.width = width
        self.height = height
        self.frames = frames

    def getAnimationFrames(self) -> list:
        frames = []
        for i in range(self.frames):
            frames.append(
                SPRITE_SHEET.subsurface(
                    (
                        self.start_point[0] + self.width * i,
                        self.start_point[1],
                        self.width,
                        self.height,
                    )
                )
            )
        return frames
