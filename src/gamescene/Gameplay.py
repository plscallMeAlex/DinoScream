import pygame
from src.gamescene.GameState import GameState
from src.Dino import Dino
from src.Tile import Tile
from src.obstacles.Cactus import Cactus
from src.modules.Mpu_6050_md import get_tilt_angle
from src.modules.KY_037_md import JUMP_EVENT, CROUCH_EVENT


class Gameplay(GameState):
    def __init__(self):
        self.__dino = Dino()
        self.__tile = Tile(self.__dino.rect)
        self.__cactus = Cactus(10)
        pygame.display.set_caption("DinoScream")

    def update(self, delta_time, screen):
        """
        Dino update function
        param: screen_width: width of the screen for range of movement
        param: tilt_angle: angle of the gyro make sure the direction of tilting
        """
        self.__dino.update(
            screen.get_width(),
            tilt_angle=get_tilt_angle(),
            elapsed_time=delta_time,
        )
        self.__cactus.update()

    def render(self, screen):
        screen.fill((255, 255, 255))  # filling the background to white
        self.__dino.draw(screen)
        self.__tile.draw(screen)
        self.__cactus.draw(screen)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            # Handle jump and crouch events
            elif event.type == JUMP_EVENT:
                self.__dino.jump()
            elif event.type == CROUCH_EVENT:
                self.__dino.crouch()

    def run(self, delta_time, screen):
        self.handle_event()
        self.render(screen)
        self.update(delta_time, screen)

        # pygame.draw.rect(self._screen, (0, 255, 0), self.__dino.rect, 2)
        # pygame.draw.circle(self._screen, (255, 0, 0), self.__dino.rect.midbottom, 1)
        # update game state
