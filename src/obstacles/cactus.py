import pygame
from ..Animation import Animation
from ..Configuration import Setting
from ..game import Game

class Cactus(pygame.sprite.Sprite):
    def __init__(self, size, speed=-5):
        super().__init__()

        # placeholder imgage
        self.image = pygame.image.load("resources/cactus.png")
        self.rect = pygame.Rect(Setting.screen_height, 400, size, 47)
        self.x_velocity = speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.x_velocity

        if self.rect.right < 0:
            self.kill()

    def kill(self):
        super().kill()
        del self



    
