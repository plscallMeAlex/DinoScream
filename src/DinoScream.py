import pygame
from src.Game import Game
from src.Dino import Dino
from src.Tile import Tile
from src.obstacles.Cactus import Cactus
from src.modules.Mpu_6050_md import get_tilt_angle
from src.modules.KY_037_md import start_serial_reader, JUMP_EVENT, CROUCH_EVENT


class DinoScream(Game):
    def __init__(self):
        super().__init__()
        self.__dino = Dino()
        self.__tile = Tile(self.__dino.rect)
        self.__cactus = Cactus(10)
        self.init()

    def init(self):
        super().init()
        pygame.display.set_caption("DinoScream")

    def run(self):
        clock = pygame.time.Clock()
        start_serial_reader()
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                # Handle jump and crouch events
                elif event.type == JUMP_EVENT:
                    self.__dino.jump()
                elif event.type == CROUCH_EVENT:
                    self.__dino.crouch()

                # Manual control using keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # Space triggers jump
                        self.__dino.jump()
                    elif event.key == pygame.K_DOWN:  # Down arrow triggers crouch
                        self.__dino.crouch()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:  # Release down arrow to stand up
                        self.__dino.stand_up()

            # draw state
            self._screen.fill((255, 255, 255))  # filling the background to white
            self.__dino.draw(self._screen)
            self.__tile.draw(self._screen)
            self.__cactus.draw(self._screen)

            # pygame.draw.rect(self._screen, (0, 255, 0), self.__dino.rect, 2)
            # pygame.draw.circle(self._screen, (255, 0, 0), self.__dino.rect.midbottom, 1)

            # update game state
            """
            Dino update function
            param: screen_width: width of the screen for range of movement
            param: tilt_angle: angle of the gyro make sure the direction of tilting
            """
            self.__dino.update(
                self._screen.get_width(),
                tilt_angle=get_tilt_angle(),
                elapsed_time=pygame.time.get_ticks(),
            )
            self.__cactus.update()
            pygame.display.update()

            clock.tick(60)
