import sys
from src.gamescene.GameState import GameState


class MainMenu(GameState):
    def __init__(self, screenManager):
        self._screenManager = screenManager

    def new_game(self):
        self._screenManager.change_scene("gameplay")

    def update(self):
        pass

    def render(self):
        pass

    def handle_event(self):
        pass

    def run(self, delta_time, screen, events):
        self.handle_event()
        self.render()
        self.update()

    def quit(self):
        print("Quitting game...")
        sys.exit(0)
