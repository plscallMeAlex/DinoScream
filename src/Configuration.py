import pygame


# Setting file
class Setting:
    fullscreen = False
    screen_width = 800  # default screen width
    screen_height = 600  # default screen height

    audio_volume = 1.0
    audio_mute = False

    # Screen settings
    def getVideoMode(self):
        if self.fullscreen:
            return (0, 0), pygame.FULLSCREEN
        else:
            return (self.screen_width, self.screen_height), pygame.RESIZABLE

    def setFullscreen(self, fullscreen: bool) -> None:
        self.fullscreen = fullscreen