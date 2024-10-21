class SceneManager:

    def __init__(self, current_scene):
        self.current_scene = current_scene

    def change_scene(self, new_scene):
        self.current_scen = new_scene
        return self.current_scene

    def get_current_scene(self):
        return self.current_scene

    def run(self, delta_time, screen):
        if self.current_scene:
            self.current_scene.run(delta_time, screen)
