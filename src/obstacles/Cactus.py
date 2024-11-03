import pygame
import random
from ..Configuration import Setting
from ..Animation import Animation


class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=-5):
        super().__init__()

        # placeholder image
        self.image = None
        self.rect = pygame.Rect(Setting.screen_width, 400, 44, 47 * 2)
        self.cactusShort_image = Animation((228, 2), 17, 35, 6).getAnimationFrames()
        self.cactusTall_image = Animation((332, 2), 25, 50, 4).getAnimationFrames()
        self.x_velocity = speed
        self.set_image()

    # Draw the cactus on the screen 20% chance of tall cactus and 80% chance of short cactus
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.x_velocity
        if self.check_out_of_screen():
            self.kill()

    def set_image(self):
        rd_num = random.randint(0, 100)
        if rd_num < 20:
            self.image = self.cactusTall_image[rd_num % 4]
            self.rect = self.image.get_rect()
            self.rect.y = 395
        else:
            self.image = self.cactusShort_image[rd_num % 6]
            self.rect = self.image.get_rect()
            self.rect.y = 410

        # self.rect = self.image.get_rect()
        self.rect.x = Setting.screen_width
        # self.rect.y = 400

    def kill(self):
        super().kill()
        del self

    def check_out_of_screen(self):
        if self.rect.right < -20:
            return True
        return False
