import pygame
import random
from .Dino import Dino
from .Tile import Tile
from .game import Game 
from .obstacles import cactus, bird

class DinoScream(Game):
    def __init__(self):
        super().__init__()
        self.__dino = Dino()
        self.__tile = Tile(self.__dino.rect)
        self.obstacles = []
        self.init()

    def init(self):
        super().init()
        pygame.display.set_caption("DinoScream")

    def run(self):
        self.clock = pygame.time.Clock()
        key_pressed = None
        last_obstacle_time = pygame.time.get_ticks()
        obstacle_interval = 500

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # Space triggers jump
                        self.__dino.jump()
                    elif event.key == pygame.K_DOWN:  # Down arrow triggers crouch
                        self.__dino.crouch()
                    elif event.key == pygame.K_LEFT:  # Left arrow pressed
                        key_pressed = "left"
                    elif event.key == pygame.K_RIGHT:  # Right arrow pressed
                        key_pressed = "right"
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:  # Release down arrow to stand up
                        self.__dino.stand_up()
                    elif (
                        event.key == pygame.K_LEFT and key_pressed == "left"
                    ):  # Reset key pressed
                        key_pressed = None
                    elif (
                        event.key == pygame.K_RIGHT and key_pressed == "right"
                    ):  # Reset key pressed
                        key_pressed = None

            # update game state
            """
            param: key_pressed: temporary param it will be removed after adding gyro
            param: tilt_angle: angle of the gyro make sure the direction of tilting
            """
            self.__dino.update(self._screen.get_width(), key_pressed, 0)
            
            # draw state
            self._screen.fill((255, 255, 255))  # filling the background to white
            self.__dino.draw(self._screen)
            self.__tile.draw(self._screen)
            # pygame.draw.rect(self._screen, (0, 255, 0), self.__dino.rect, 2)
            # pygame.draw.circle(self._screen, (255, 0, 0), self.__dino.rect.midbottom, 1)
            
            # check if enough time has passed before spawning a new obstacle
            current_time = pygame.time.get_ticks()
            if current_time - last_obstacle_time > obstacle_interval:
                self.obstacles.append(self.random_obstacle())
                last_obstacle_time = current_time
        
            for obs in self.obstacles[:]:
                if obs is not None:
                    updated = obs.update()
                    if updated:
                        self.obstacles.remove(obs)
                    obs.draw(self._screen)
                    self.check_collision(obs, self.__dino) # check for collision every frame
                
            pygame.display.update()

            self.clock.tick(60)
    
    def check_collision(self, object, dino):
        if pygame.sprite.collide_rect(dino, object):
            self.__dino.die()
            # need to stop the game in some way

    def random_obstacle(self):
        rand = random.randint(0, 5)
        if rand <= 2:
        #     print("cactus spawned")
        #     self.__cactus = cactus.Cactus(20)
        #     self.__cactus.draw(self._screen)
        #     return self.__cactus
        # elif rand == 0:
            print("bird spawned")
            self.__bird = bird.Bird()
            self.__bird.draw(self._screen)
            return self.__bird
        else:
            return None