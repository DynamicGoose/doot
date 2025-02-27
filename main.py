from moderngl_window.resources import programs
from moderngl_window.scene.programs import MeshProgram
from renderer.window import RenderWindow
import glm
import moderngl_window as glw
from moderngl_window.meta import ProgramDescription
import moderngl

class DootWindow(RenderWindow):
    title = "DOOT"
    resource_dir = "assets"
    fullscreen = False

    def __init__(self, **kwargs):
        super().__init__("test/test.gltf", **kwargs)
                
glw.run_window_config(DootWindow)
