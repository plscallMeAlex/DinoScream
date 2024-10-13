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
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:  # Release down arrow to stand up
                        self.__dino.stand_up()

            self._screen.fill((255, 255, 255))
            self._screen.blit(self.__dino.image, self.__dino.rect)
            pygame.display.update()
            clock.tick(30)
