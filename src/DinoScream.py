import pygame
from src.gamescene.SceneManager import SceneManager
from src.gamescene.Gameplay import Gameplay
from src.gamescene.MainMenu import MainMenu
from src.modules.KY_037_md import start_serial_reader
from src.Configuration import Setting

FPS = 60


class DinoScream:
    def __init__(self):
        self.__setting = Setting()
        self.__screen = pygame.display.set_mode(*self.__setting.getVideoMode())
        self.__scene = {
            "gameplay": Gameplay(),
            # "main_menu": MainMenu(),
        }
        self.__sceneManager = SceneManager(self.__scene["gameplay"])

    def run(self):
        clock = pygame.time.Clock()
        start_serial_reader()
        while True:
            delta_time = clock.tick(FPS)

            # handle quiting the game event.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.__sceneManager.run(delta_time, self.__screen)
            pygame.display.update()
