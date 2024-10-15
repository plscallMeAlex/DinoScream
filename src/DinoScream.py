from .Game import Game, pygame
from .Dino import Dino


class DinoScream(Game):
    def __init__(self):
        super().__init__()
        self.__dino = Dino()
        self.init()

    def init(self):
        super().init()
        pygame.display.set_caption("DinoScream")

    def run(self):
        clock = pygame.time.Clock()
        key_pressed = None
        while self._running:
            self.__dino.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # Space triggers jump
                        self.__dino.jump()
                    elif event.key == pygame.K_DOWN:  # Down arrow triggers crouch
                        self.__dino.crouch()
                    elif event.key == pygame.K_LEFT:  # Left arrow pressed
                        key_pressed = "left"
                    elif event.key == pygame.K_RIGHT:  # Right arrow pressed
                        key_pressed = "right"
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:  # Release down arrow to stand up
                        self.__dino.stand_up()
                    elif (
                        event.key == pygame.K_LEFT and key_pressed == "left"
                    ):  # Reset key pressed
                        key_pressed = None
                    elif (
                        event.key == pygame.K_RIGHT and key_pressed == "right"
                    ):  # Reset key pressed
                        key_pressed = None

            # for gyro
            tilt_angle = 0
            self.__dino.tilt_move(
                screen_width=self._screen.get_width(),
                key_pressed=key_pressed,
                tilt_angle=tilt_angle,
            )

            self._screen.fill((255, 255, 255))
            self._screen.blit(self.__dino.image, self.__dino.rect)

            # pygame.draw.rect(self._screen, (0, 255, 0), self.__dino.rect, 2)
            # pygame.draw.circle(self._screen, (255, 0, 0), self.__dino.rect.midbottom, 1)

            pygame.display.update()

            clock.tick(60)
