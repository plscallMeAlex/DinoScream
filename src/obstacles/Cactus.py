import pygame
from src.Animation import Animation
from src.Configuration import Setting


class Cactus(pygame.sprite.Sprite):
    def __init__(self, size, speed=-5):
        super().__init__()

        # placeholder imgage
        self.image = pygame.image.load("resources/cactus.png")
        self.rect = pygame.Rect(Setting.screen_height, 200, 20, size)
        self.x_velocity = speed

    def update(self):
        self.rect.x += self.x_velocity

        if self.rect.right < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def kill(self):
        super().kill()
        del self
