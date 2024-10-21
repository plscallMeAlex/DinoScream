"""Abstract class for game states."""


class GameState:
    def __init__(self):
        pass

    def update(self):
        """Update the game state."""
        pass

    def render(self):
        """Render the current game state"""
        pass

    def handle_event(self):
        """Handle the events of the current game state."""
        pass

    def run(self):
        """Run the current game state."""
        pass
