import pygame
from .Animation import Animation


JUMP_STRENGTH = 17
GRAVITY = 1
JUMP_MOVE_FACTOR = 0.8
MOVE_SPEED = 5


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Dino's position and movement attributes
        self.rect = pygame.Rect(100, 400, 44, 47)  # Initial position and size
        self.y_velocity = 0  # Vertical velocity
        self.is_jumping = False  # Flag to check if Dino is jumping
        self.is_crouching = False  # Flag to check if Dino is crouching
        self.crouching_time = 0  # Time spent crouching
        self.animation_index = 0  # Frame index for animation
        self.animation_speed = 0.2  # Controls frame switching speed
        self.frame_counter = 0  # Tracks time between frame changes

        # Creating an animation instance for the dino
        self.dino_animations = {
            "run": Animation((936, 2), 44, 47, 2),
            "jump": Animation((848, 2), 44, 47, 1),
            "crouch": Animation((1112, 19), 59, 30, 2),
            "dead": Animation((1024, 2), 44, 47, 1),
        }

        self.state = None  # Start with running animation
        self.set_animation("run")

    def set_animation(self, state):
        """Sets the current animation based on the state."""
        if self.state == state:
            return

        self.state = state
        # Get the list of frames for the current animation
        self.dino_current_animation = self.dino_animations[state].getAnimationFrames()
        self.animation_index = 0  # Reset frame index

        # Update the size of the rect based on the new animation frame
        if self.dino_current_animation:

            current_bottom_center = self.rect.midbottom
            self.rect.size = self.dino_current_animation[0].get_size()

            self.rect.midbottom = current_bottom_center
        self.image = self.dino_current_animation[self.animation_index]

    def update(self, screen_width, tilt_angle, elapsed_time):
        """Updates the animation and position of the Dino."""
        self.update_animation()  # Update the animation frames
        self.tilt_move(screen_width, tilt_angle)
        self.handle_jumping()
        self.handle_crouch()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update_animation(self):
        """Updates the animation frame based on frame speed."""
        self.frame_counter += self.animation_speed
        if self.frame_counter >= 1:
            self.frame_counter = 0
            self.animation_index = (self.animation_index + 1) % len(
                self.dino_current_animation
            )
            self.image = self.dino_current_animation[self.animation_index]

    def handle_jumping(self):
        if self.is_jumping:  # Handle jumping mechanics
            self.rect.y += self.y_velocity
            self.y_velocity += GRAVITY  # Apply gravity

            # Check if the Dino has landed on the ground
            if self.rect.y >= 400:  # Assuming 100 is ground level
                self.rect.y = 400
                self.y_velocity = 0
                self.set_animation("run")  # Switch back to running
                self.is_jumping = False
                self.state = "run"

    def jump(self):
        """Triggers the jump animation and movement."""
        if not self.is_jumping and not self.is_crouching:
            self.is_jumping = True
            self.y_velocity = -JUMP_STRENGTH
            self.set_animation("jump")

    def handle_crouch(self):
        if self.is_crouching:
            current_time = pygame.time.get_ticks()
            if current_time - self.crouching_time >= 800:
                self.stand_up()

    def crouch(self):
        """Triggers the crouching animation."""
        if not self.is_jumping and not self.is_crouching:
            self.set_animation("crouch")
            self.is_crouching = True
            self.crouching_time = pygame.time.get_ticks()

    def stand_up(self):
        """Switches back to the running animation from crouching."""
        if self.state == "crouch":
            self.set_animation("run")
            self.is_crouching = False

    def die(self):
        """Triggers the dead animation."""
        self.set_animation("dead")
        self.state = "dead"

    # temporary key_pressed parameter
    def tilt_move(self, screen_width, tilt_angle):
        """
        Moves the Dino forward or backward based on the tilt angle.
        Positive tilt_angle indicates forward movement, negative indicates backward.
        """

        # Determine the movement speed based on whether the Dino is jumping
        move_speed = MOVE_SPEED * (JUMP_MOVE_FACTOR if self.is_jumping else 1)

        if tilt_angle >= 4:  # Threshold for forward tilt
            self.rect.x -= move_speed
        elif tilt_angle <= -4:  # Threshold for backward tilt
            self.rect.x += move_speed

        # Prevent the Dino from moving out of bounds
        if self.rect.x < 0:
            self.rect.x = 0
        elif (
            self.rect.x > screen_width - self.rect.width
        ):  # Assuming screen width is 800
            self.rect.x = screen_width - self.rect.width
