import pygame
from .Animation import Animation


JUMP_STRENGTH = 15
GRAVITY = 1


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Dino's position and movement attributes
        self.rect = pygame.Rect(100, 400, 44, 47)  # Initial position and size
        self.y_velocity = 0  # Vertical velocity
        self.is_jumping = False  # Flag to check if Dino is jumping
        self.animation_index = 0  # Frame index for animation
        self.animation_speed = 0.3  # Controls frame switching speed
        self.frame_counter = 0  # Tracks time between frame changes

        # Creating an animation instance for the dino
        self.dino_animations = {
            "run": Animation((936, 2), 44, 47, 2),
            "jump": Animation((848, 2), 44, 47, 1),
            "crouch": Animation((1112, 19), 59, 30, 2),
            "dead": Animation((1024, 2), 44, 47, 1),
        }

        self.state = "run"  # Start with running animation
        self.set_animation(self.state)

    def set_animation(self, state):
        """Sets the current animation based on the state."""
        self.state = state
        # Get the list of frames for the current animation
        self.dino_current_animation = self.dino_animations[state].getAnimationFrames()
        self.animation_index = 0  # Reset frame index

        # Update the size of the rect based on the new animation frame
        if self.dino_current_animation:
            self.rect.size = self.dino_current_animation[0].get_size()
        self.image = self.dino_current_animation[self.animation_index]

    def update(self):
        """Updates the animation and position of the Dino."""
        self.update_animation()  # Update the animation frames

        if self.is_jumping:  # Handle jumping mechanics
            self.rect.y += self.y_velocity
            self.y_velocity += GRAVITY  # Apply gravity

            # Check if the Dino has landed on the ground
            if self.rect.y >= 400:  # Assuming 100 is ground level
                self.rect.y = 400
                self.y_velocity = 0
                self.is_jumping = False
                self.set_animation("run")  # Switch back to running

    def update_animation(self):
        """Updates the animation frame based on frame speed."""
        self.frame_counter += self.animation_speed
        if self.frame_counter >= 1:
            self.frame_counter = 0
            self.animation_index = (self.animation_index + 1) % len(
                self.dino_current_animation
            )
            self.image = self.dino_current_animation[self.animation_index]

    def jump(self):
        """Triggers the jump animation and movement."""
        if not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = -JUMP_STRENGTH
            self.set_animation("jump")

    def crouch(self):
        """Triggers the crouching animation."""
        if not self.is_jumping:
            self.set_animation("crouch")

    def stand_up(self):
        """Switches back to the running animation from crouching."""
        if self.state == "crouch":
            self.set_animation("run")

    def die(self):
        """Triggers the dead animation."""
        self.set_animation("dead")