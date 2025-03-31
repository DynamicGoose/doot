from moderngl_window.resources import programs
from moderngl_window.scene.programs import MeshProgram
from moderngl_window.meta import ProgramDescription
import glm

# Shader-Programme definieren. draw Funktion setzt auch uniforms.

class DirectionalLightProgram(MeshProgram):
    def __init__(self, lightDir: glm.vec3, **kwargs):
        super().__init__(program=programs.load(ProgramDescription(path="shaders/directional_light.glsl")))
        self.lightDir = glm.vec4(lightDir, 1.0)
        self.shadowProgram = programs.load(ProgramDescription(path="shaders/shadow_map.glsl"))

    def draw(self, mesh, projection_matrix, model_matrix, camera_matrix, time):
        mesh.material.mat_texture.texture.use()
        self.program["texture0"].value = 0
        self.program["m_proj"].write(projection_matrix)
        self.program["m_model"].write(model_matrix)
        self.program["m_cam"].write(camera_matrix)
        self.program["light_dir"].write(self.lightDir)
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

class ShadowMapProgram(MeshProgram):
    def __init__(self, **kwargs):
        super().__init__(program=programs.load(ProgramDescription(path="shaders/shadow_map/shadow_map.glsl")))

        self.depth_mvp = glm.mat4(0)

    def draw(self, mesh, projection_matrix, model_matrix, camera_matrix, time):
        self.program["mvp"].write(self.depth_mvp)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        return self

class ShadowMapLightProgram(MeshProgram):
    def __init__(self, lightPos: glm.vec3, **kwargs):
        super().__init__(program=programs.load(ProgramDescription(path="shaders/shadow_map/light_texture.glsl")))
        self.shadow_bias = glm.mat4(0)
        self.lightPos = lightPos
        
    def draw(self, mesh, projection_matrix, model_matrix, camera_matrix, time):
        mesh.material.mat_texture.texture.use(location=0)
        self.program["texture0"].value = 0
        # self.program["shadowMap"].value = 1
        self.program["m_proj"].write(projection_matrix)
        self.program["m_model"].write(model_matrix)
        self.program["m_camera"].write(camera_matrix)
        # self.program["m_shadow_bias"].write(self.shadow_bias)
        # self.program["lightDir"].write(self.lightPos)
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
