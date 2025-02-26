from moderngl_window.resources import programs
from moderngl_window.scene.programs import MeshProgram
from renderer.window import RenderWindow
import glm
import moderngl_window as glw
from moderngl_window.meta import ProgramDescription
import moderngl

class LightingProgram(MeshProgram):
    def __init__(self, **kwargs) -> None:
        super().__init__(program=programs.load(ProgramDescription(path="shaders/phong.glsl")))

    def draw(self, mesh, projection_matrix, model_matrix, camera_matrix, time):
        mesh.material.mat_texture.texture.use()
        self.program["texture0"].value = 0
        self.program["m_proj"].write(projection_matrix)
        self.program["m_model"].write(model_matrix)
        self.program["m_cam"].write(camera_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        if not mesh.material:
            return None
        if not mesh.attributes.get("NORMAL"):
            return None
        if not mesh.attributes.get("TEXCOORD_0"):
            return None
        if mesh.material.mat_texture is not None:
            return self
        return None


class DootWindow(RenderWindow):
    title = "DOOT"
    resource_dir = "assets"
    fullscreen = False

    def __init__(self, **kwargs):
        super().__init__("test/test.gltf", **kwargs)
        
glw.run_window_config(DootWindow)
