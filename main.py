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
    vsync = False
    
    def __init__(self, **kwargs):        
        super().__init__("test/test.gltf", ["test/cube_entity.gltf"], **kwargs)
        self.camera.set_position(0.0, 0.0, 5.0)
        self.camera.velocity = 1.0
        self.jump_vel = 0.0

    def on_render(self, time, frametime):
        for node in self.dynamic[0].nodes:
            node._matrix_global = node._matrix_global * glm.translate(glm.vec3(0, 0, 0.001))
        print(self.camera.position)
        
        super().on_render(time, frametime)
    
                        
glw.run_window_config(DootWindow)
