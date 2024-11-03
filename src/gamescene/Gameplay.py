import pygame
import random
from src.gamescene.GameState import GameState
from src.Dino import Dino
from src.Tile import Tile, SCROLL_SPEED
from src.obstacles.Cactus import Cactus
from src.obstacles.Bird import Bird
from src.modules.Mpu_6050_md import get_tilt_angle
from src.modules.KY_037_md import JUMP_EVENT, CROUCH_EVENT


class Gameplay(GameState):
    def __init__(self, screenManager):
        self._screenManager = screenManager

        self.__dino = Dino()
        self.__tile = Tile(self.__dino.rect)
        self.__obstacles = []
        self.__obstacles_last_spawn = 0
        self.__game_over = False

        # Font for the "GAME OVER" text
        pygame.font.init()
        self.font = pygame.font.Font(None, 74)

        pygame.display.set_caption("DinoScream")

    def update(self, delta_time, screen):
        if self.__game_over:
            self.__dino.die()
            self.__dino.update_animation()
            return

        # Randomly spawn obstacles
        self.__obstacles_last_spawn += delta_time
        if self.__obstacles_last_spawn >= 2000:
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
            game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(
                center=(screen.get_width() // 2, screen.get_height() // 2)
            )
            screen.blit(game_over_text, text_rect)

    def handle_event(self, events):

        for event in events:
            if event.type == pygame.QUIT:
                self._running = False

            # Handle jump and crouch events
            elif event.type == JUMP_EVENT:
                self.__dino.jump()
            elif event.type == CROUCH_EVENT:
                self.__dino.crouch()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.__game_over:
                        self.reset_game()

    def random_obstacle(self):
        rand = random.randint(0, 100)
        if rand <= 20:
            print("Bird Spawn")
            bird = Bird()
            self.__obstacles.append(bird)
        else:
            print("Cactus Spawn")
            cactus = Cactus()
            self.__obstacles.append(cactus)

    def reset_game(self):
        """Resets the game state to start a new game."""
        self.__dino = Dino()  # Reset Dino instance
        self.__tile = Tile(self.__dino.rect)
        self.__obstacles = []
        self.__obstacles_last_spawn = 0
        self.__game_over = False

    def run(self, delta_time, screen, events):
        self.handle_event(events)
        self.render(screen)
        self.update(delta_time, screen)
        # pygame.draw.rect(self._screen, (0, 255, 0), self.__dino.rect, 2)
        # pygame.draw.circle(self._screen, (255, 0, 0), self.__dino.rect.midbottom, 1)
        # update game state
