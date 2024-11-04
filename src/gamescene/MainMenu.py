import sys
from src.gamescene.GameState import GameState
import pygame
from src.Dino import Dino

class MainMenu(GameState):
    def __init__(self, screenManager):
        self._screenManager = screenManager
        self.__titleFont = pygame.font.SysFont("mononokinerdfontmono", 50)
        self.__font = pygame.font.SysFont("mononokinerdfontmono", 20)
        self.__fontColor = (0, 0, 0)
        self.__blink = True  # To toggle visibility
        self.__blink_timer = 0  # Timer to track time for blinking
        self.__gear_icon = pygame.image.load("resources/gear.png")
        self.__dino = pygame.transform.scale(Dino().image, (200, 200))

    def draw_text(self, text, font, text_col, x, y, screen):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def new_game(self):
        self._screenManager.change_scene("gameplay")

    def update(self, delta_time, screen):
        # Update the blink timer
        self.__blink_timer += delta_time
        # Toggle blink every 500ms
        if self.__blink_timer >= 500:
            self.__blink = not self.__blink
            self.__blink_timer = 0

    def render(self, screen):
        screen.fill((255, 255, 255))  # filling the background to white
        self.draw_text("Dino Scream", self.__titleFont, self.__fontColor, 240, 20, screen)  # game title
        if self.__blink:
            self.draw_text("- Press SPACE to start -", self.__font, self.__fontColor, 250, 500, screen)
        # draw the gear icon
        screen.blit(self.__gear_icon, (760, 10))
        screen.blit(self.__dino, (300, 200))

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.new_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 760 <= event.pos[0] <= 790 and 10 <= event.pos[1] <= 42:
                        print("settings clicked") 

    def run(self, delta_time, screen, events):
        self.handle_event(events)
        self.render(screen)
        self.update(delta_time, screen)

    def quit(self):
        print("Quitting game...")
        sys.exit(0)
