import pygame
import random

from src.gamescene.GameState import GameState
from src.Dino import Dino
from src.Tile import Tile, SCROLL_SPEED
from src.obstacles.Cactus import Cactus
from src.obstacles.bird import Bird
from src.modules.Mpu_6050_md import get_tilt_angle, get_tiltX_angle
from src.modules.KY_037_md import JUMP_EVENT, detected_module
from src.modules.Switch_md import check_button_press


class Gameplay(GameState):
    def __init__(self, screenManager):
        self._screenManager = screenManager

        self.__dino = Dino()
        self.__tile = Tile(self.__dino.rect)
        self.__obstacles = []
        self.__obstacles_last_spawn = 0
        self.__game_over = False

        # random spawn obstacles speed (if the value is greater, the obstacles will spawn less)
        self.__obstacles_spawn_speed = 1000

        # Score
        self.__score = 0
        self.__scorePS = 0

        # Font for the "GAME OVER" text
        pygame.font.init()
        self.font = pygame.font.SysFont("mononokinerdfontmono", 74)
        self.score_font = pygame.font.SysFont("mononokinerdfontmono", 36)
        self.option_font = pygame.font.SysFont("mononokinerdfontmono", 25)

        # Button click checking
        self.button_last_pressed = 0

        # game over options
        self.__default_option = 0
        self.restart_text = self.option_font.render("Retry", True, (0, 0, 0))
        self.quit_text = self.option_font.render("Quit", True, (0, 0, 0))
        self.__game_over_options = ["RESTART", "QUIT"]

        pygame.display.set_caption("DinoScream")

    def update(self, delta_time, screen):
        if self.__game_over:
            self.__dino.die()
            self.__dino.update_animation()
            return

        # Randomly spawn obstacles
        self.__obstacles_last_spawn += delta_time
        if self.__obstacles_last_spawn >= self.__obstacles_spawn_speed:
            self.random_obstacle()
            self.__obstacles_last_spawn = 0

        """
        Dino update function
        param: screen_width: width of the screen for range of movement
        param: tilt_angle: angle of the gyro make sure the direction of tilting
        """
        self.__dino.update(
            screen.get_width(),
            tilt_angle=get_tilt_angle(),
            elapsed_time=delta_time,
        )

        # Update the obstacles objects
        for obj in self.__obstacles:
            obj.update()
            if obj.check_collision(self.__dino.rect):
                self.__game_over = True

        # Score increment mechanism
        if self.__scorePS >= 90:
            self.__score += 1
            self.__scorePS = 0
        self.__scorePS += delta_time

        # Score mechanism increase game difficulty
        match self.__score:
            case 100:
                self.__obstacles_spawn_speed = 1800
            case 300:
                self.__obstacles_spawn_speed = 1600
            case 500:
                self.__obstacles_spawn_speed = 1200
            case 700:
                self.__obstacles_spawn_speed = 1000
            case 1000:
                self.__obstacles_spawn_speed = 800
            case 1500:
                self.__obstacles_spawn_speed = 600

        # Check if the score is reach 99,999 will end the game
        if self.__score >= 99999:
            self.__game_over = True

        if self.__game_over:
            screen.blit(
                self.restart_text,
                (screen.get_width() // 2 - 150, screen.get_height() // 2 + 100),
            )
            screen.blit(
                self.quit_text,
                (screen.get_width() // 2 + 100, screen.get_height() // 2 + 100),
            )

    def render(self, screen):
        screen.fill((255, 255, 255))  # filling the background to white
        self.__dino.draw(screen)

        # Stop the tile scrolling if the game is over
        scroll_speed = 0 if self.__game_over else SCROLL_SPEED
        self.__tile.draw(screen, scroll_speed)

        if not self.__game_over:
            for obj in self.__obstacles:
                obj.draw(screen)
        else:
            # Display "GAME OVER" in the center of the screen
            game_over_text = self.font.render("GAME OVER", True, (0, 0, 0))
            text_rect = game_over_text.get_rect(
                center=(screen.get_width() // 2, screen.get_height() // 2)
            )
            screen.blit(game_over_text, text_rect)
            screen.blit(
                self.restart_text,
                (screen.get_width() // 2 - 150, screen.get_height() // 2 + 100),
            )
            screen.blit(
                self.quit_text,
                (screen.get_width() // 2 + 100, screen.get_height() // 2 + 100),
            )

        score_text = self.score_font.render(f"Score: {self.__score}", True, (0, 0, 0))
        screen.blit(score_text, (screen.get_width() - score_text.get_width() - 10, 10))

    def handle_event(self, events):

        for event in events:
            if event.type == pygame.QUIT:
                self._running = False

            # Handle jump events separate platform controls
            elif event.type == JUMP_EVENT or (
                detected_module() is False
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_UP
            ):
                self.__dino.jump()
            # Handle crouch event if it doesn't connect to the module
            elif (
                get_tiltX_angle() is None
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_DOWN
            ):
                self.__dino.crouch()
            # Handle the stand up after crouching
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.__dino.stand_up()
            # Handle if there is no modules switch
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.__game_over:
                        if self.__default_option == 0:
                            self.reset_game()
                        elif self.__default_option == 1:
                            self.reset_game()
                            self._screenManager.change_scene("main_menu")

        # Check if the game is over
        if self.__game_over:
            current_time = pygame.time.get_ticks()

            # Button selection logic based on press timing
            if check_button_press():
                if current_time - self.button_last_pressed <= 500:
                    # Double press to select the option
                    if self.__default_option == 0:
                        self.reset_game()
                    elif self.__default_option == 1:
                        self.reset_game()
                        self._screenManager.change_scene("main_menu")
                    self.button_last_pressed = 0
                else:
                    # Toggle option with single press
                    self.__default_option = (
                        1 - self.__default_option
                    )  # toggles between 0 and 1
                    self.select_option(self.__default_option)

                    # Update last pressed time
                    self.button_last_pressed = current_time

    def select_option(self, option):
        selected = self.__game_over_options[option]
        if selected == "RESTART":
            self.__default_option = 0
            self.restart_text = self.option_font.render("Retry", True, (255, 0, 0))
            self.quit_text = self.option_font.render("Quit", True, (0, 0, 0))
        elif selected == "QUIT":
            self.__default_option = 1
            self.restart_text = self.option_font.render("Retry", True, (0, 0, 0))
            self.quit_text = self.option_font.render("Quit", True, (255, 0, 0))

    def random_obstacle(self):
        rand = random.randint(0, 100)
        if rand <= 20:
            bird = Bird()
            self.__obstacles.append(bird)
        else:
            cactus = Cactus()
            self.__obstacles.append(cactus)

    def reset_game(self):
        """Resets the game state to start a new game."""
        self.__dino = Dino()  # Reset Dino instance
        self.__tile = Tile(self.__dino.rect)
        self.__obstacles = []
        self.__obstacles_last_spawn = 0
        self.__game_over = False
        self.__score = 0
        self.__default_option = 0

    def run(self, delta_time, screen, events):
        self.handle_event(events)
        self.render(screen)
        self.update(delta_time, screen)
        # pygame.draw.rect(self._screen, (0, 255, 0), self.__dino.rect, 2)
        # pygame.draw.circle(self._screen, (255, 0, 0), self.__dino.rect.midbottom, 1)
        # update game state
