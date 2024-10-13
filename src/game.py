from .Configuration import Setting
import pygame


class Game:
    def __init__(self):
        self._running = False
        self._screen = None
        self._setting = Setting()

    def init(self):
        self._game = pygame.init()
        self._screen = pygame.display.set_mode(*self._setting.getVideoMode())
        pygame.display.set_caption("Game")
        self._running = True

    def run(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self._screen.fill((0, 0, 0))
            pygame.display.flip()

    def quit(self):
        pygame.quit()

    def get_setting(self):
        return self.__setting

    def set_setting(self, setting: Setting):
        self.__setting = setting