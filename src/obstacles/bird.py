import pygame
from ..Animation import Animation
from ..Configuration import Setting


class Bird(pygame.sprite.Sprite):
    def __init__(self, speed=-5):
        super().__init__()

        self.rect = pygame.Rect(
            Setting.screen_width, Setting.screen_height // 2 + 80, 46, 40
        )
        self.x_velocity = speed
        self.animation_index = 0
        self.animation_speed = 0.2
        self.frame_counter = 0
        # self.image = pygame.image.load("resources/hackerman.jpg")

        self.bird_animations = Animation((134, 2), 46, 40, 2).getAnimationFrames()
        self.image = self.bird_animations[self.animation_index]

    def update(self):
        self.rect.x += self.x_velocity
        if self.check_out_of_screen():
            self.kill()

        self.update_animation()

    def update_animation(self):
        self.frame_counter += self.animation_speed
        if self.frame_counter >= 1:
            self.frame_counter = 0
            self.animation_index = (self.animation_index + 1) % 2
            self.image = self.bird_animations[self.animation_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def kill(self):
        super().kill()
        del self

    def check_out_of_screen(self):
        if self.rect.right < -20:
            return True
        return False
