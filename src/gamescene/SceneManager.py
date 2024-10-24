from src.gamescene.Gameplay import Gameplay
from src.gamescene.MainMenu import MainMenu


class SceneManager:
    def __init__(self, initial_scene):
        self.__scene = {"gameplay": Gameplay(self), "main_menu": MainMenu(self)}
        self.current_scene = self.__scene[initial_scene]

    def change_scene(self, new_scene):
        self.current_scene = new_scene
        return self.current_scene

    def get_current_scene(self):
        return self.current_scene

    def run(self, delta_time, screen, events):
        if self.current_scene:
            self.current_scene.run(delta_time, screen, events)
