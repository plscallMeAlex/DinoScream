import pygame
from src.gamescene.SceneManager import SceneManager
from src.modules.KY_037_md import start_serial_reader
from src.Configuration import Setting

FPS = 60


class DinoScream:
    def __init__(self):
        self.__setting = Setting()
        self.__screen = pygame.display.set_mode(*self.__setting.getVideoMode())
        self.__sceneManager = SceneManager("main_menu")

    def run(self):
        clock = pygame.time.Clock()
        start_serial_reader()
        while True:
            delta_time = clock.tick(FPS)

            events = pygame.event.get()
            # handle quiting the game event.
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.__sceneManager.run(delta_time, self.__screen, events)
            pygame.display.update()
