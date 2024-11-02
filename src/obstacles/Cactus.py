import pygame
from ..Configuration import Setting


class Cactus(pygame.sprite.Sprite):
    def __init__(self, size, speed=-5):
        super().__init__()

        # placeholder imgage
        self.image = pygame.image.load("resources/cactus.png")
        self.rect = pygame.Rect(Setting.screen_height + 100, 400, size, 47)
        self.x_velocity = speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.x_velocity
        if self.check_out_of_screen():
            self.kill()

    def kill(self):
        super().kill()
        del self

    def check_out_of_screen(self):
        if self.rect.right < -20:
            return True
        return False
