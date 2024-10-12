# Setting file
class Setting():
    __fullscreen = False
    __screen_width = 800    # default screen width
    __screen_height = 600   # default screen height

    __audio_volume = 1.0
    __audio_mute = False


    # Screen settings
    def set_fullscreen(self, fullscreen: bool) -> None:
        self.__fullscreen = fullscreen

    def get_screen_size(self) -> tuple:
        return (self.__screen_width, self.__screen_height)

    def set_screen_size(self, width, height) -> None:
        self.__screen_width = width
        self.__screen_height = height


    # Audio settings
    def set_audio_mute(self, mute: bool) -> None:
        self.__audio_mute = mute

    def set_audio_volume(self, volume: float) -> None:
        self.__audio_volume = volume

    def get_audio_volume(self) -> float:
        return self.__audio_volume