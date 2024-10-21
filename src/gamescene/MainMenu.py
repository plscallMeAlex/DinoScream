import sys
from src.gamescene.GameState import GameState


class MainMenu(GameState):
    def __init__(self):
        self._menu = None
        self._menu.add_item("New Game", self._new_game)
        self._menu.add_item("Load Game", self._load_game)
        self._menu.add_item("Quit", self._quit)
        self._menu.show()

    def _new_game(self):
        print("Starting new game...")

    def _load_game(self):
        print("Loading game...")

    def _quit(self):
        print("Quitting game...")
        sys.exit(0)
