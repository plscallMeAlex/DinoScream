import pygame
from ..Animation import Animation
from ..Configuration import Setting

class Bird(pygame.sprite.Sprite):
    def __init__(self, speed=-5):
        super().__init__()

        self.rect = pygame.Rect(Setting.screen_height, 300, 100, 100)
        self.x_velocity = speed
        self.animation_index = 0
        self.animation_speed = 0.5
        self.frame_counter = 0
        self.image = pygame.image.load("resources/cactus.png")

        self.bird_animations = {
            "fly": Animation((134, 7), 35, 35, 2),
        }

    def update(self):
        self.rect.x += self.x_velocity
        self.check_out_of_screen()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_out_of_screen(self):
        if self.rect.right < -20:
            return True
        return False