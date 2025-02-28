from moderngl_window.resources import programs
from moderngl_window.scene.programs import MeshProgram
from renderer.window import CollisionWindow, RenderWindow
import glm
import moderngl_window as glw
from moderngl_window.meta import ProgramDescription
import moderngl

class DootWindow(CollisionWindow):
    title = "DOOT"
    resource_dir = "assets"
    fullscreen = False

    def __init__(self, **kwargs):
        super().__init__("test/test.gltf", **kwargs)
        self.camera.set_position(0.0, 0.0, 5.0)
        self.camera.velocity = 1.0
                
glw.run_window_config(DootWindow)
