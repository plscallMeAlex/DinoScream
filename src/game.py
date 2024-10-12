from .settings import Setting
import pygame

class Game():
    __setting = Setting()

    def __init__(self):
        self.__running = False
        self.__screen = None

    def init(self):
        pygame.init()
        self.__screen = pygame.display.set_mode(self.__setting.get_screen_size())
        print(self.__screen)
        self.__running = True

    def run(self):
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False

            self.__screen.fill((0, 0, 0))
            pygame.display.flip()

    def quit(self):
        pygame.quit()

    def get_setting(self):
        return self.__setting

    def set_setting(self, setting: Setting):
        self.__setting = setting

    def save_setting(self):
        pass

    def load_setting(self):
        pass