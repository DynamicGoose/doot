import glm
import moderngl_window as glw
from moderngl_window.scene.camera import KeyboardCamera
from moderngl_window import geometry
import moderngl
import math

class CameraWindow(glw.WindowConfig):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = KeyboardCamera(
            self.wnd.keys,
            fov=70.0,
            aspect_ratio=self.wnd.aspect_ratio,
            near=0.1,
            far=1000.0,
        )
        self.camera.velocity = 10.0
        self.camera.mouse_sensitivity = 0.25
        self.camera_enabled = True

    def on_key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            self.camera.key_input(key, action, modifiers)
            self.wnd.mouse_exclusivity = True
            self.wnd.cursor = False
            
        if action == keys.ACTION_PRESS:
            if key == keys.C:
                self.camera_enabled = not self.camera_enabled
                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.cursor = not self.camera_enabled
            if key == keys.SPACE:
                self.timer.toggle_pause()

    def on_mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx, -dy)

    def on_resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

    def on_mouse_scroll_event(self, x_offset: float, y_offset: float) -> None:
        velocity = self.camera.velocity + y_offset
        self.camera.velocity = max(velocity, 1.0)

class RenderWindow(CameraWindow):
    resource_dir = "assets"

    def __init__(self, scene: str(), **kwargs):
        super().__init__(**kwargs)

        # Offscreen buffer
        offscreen_size = 4096, 4096
        self.offscreen_depth = self.ctx.depth_texture(offscreen_size)
        self.offscreen_depth.compare_func = ""
        self.offscreen_depth.repeat_x = False
        self.offscreen_depth.repeat_y = False
        # Less ugly by default with linear. May need to be NEAREST for some techniques
        self.offscreen_depth.filter = moderngl.LINEAR, moderngl.LINEAR

        self.offscreen = self.ctx.framebuffer(
            depth_attachment=self.offscreen_depth,
        )

        self.scene = self.load_scene(scene)
        
        # Scene geometry
        self.sun = geometry.sphere(radius=1.0)

        # Programs
        self.basic_light = self.load_program("programs/shadow_mapping/directional_light.glsl")
        self.basic_light["shadowMap"].value = 0
        self.shadowmap_program = self.load_program("programs/shadow_mapping/shadowmap.glsl")
        self.sun_prog = self.load_program("programs/sun_debug.glsl")
        self.sun_prog["color"].value = 1, 1, 0, 1
        self.lightpos = 0, 0, 0

    def on_render(self, time, frametime):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.lightpos = glm.vec3(math.sin(time * 0.1) * 10, 20, math.cos(time * 0.1) * 10)
        # self.lightpos = glm.vec3(10, 20, 10)

        # --- PASS 1: Render shadow map
        self.offscreen.clear()
        self.offscreen.use()

        depth_projection = glm.ortho(-40.0, 40.0, -40.0, 40.0, 1, 150.0)
        depth_view = glm.lookAt(self.lightpos, (0, 0, 0), (0, 1, 0))
        depth_mvp = depth_projection * depth_view
        self.shadowmap_program["mvp"].write(depth_mvp)

        for node in self.scene.nodes:
            self.draw_nodes_depth(node)

        # --- PASS 2: Render scene to screen
        self.wnd.use()
        self.basic_light["m_proj"].write(self.camera.projection.matrix)
        self.basic_light["m_camera"].write(self.camera.matrix)
        self.basic_light["mvp"].write(depth_mvp)
        self.basic_light["lightPos"].write(self.lightpos)
        self.basic_light["viewPos"].write(self.camera.position)
        self.offscreen_depth.use(location=0)

        for node in self.scene.nodes:
            self.draw_nodes_light(node)
                        
        # Render the sun position
        self.sun_prog["m_proj"].write(self.camera.projection.matrix)
        self.sun_prog["m_camera"].write(self.camera.matrix)
        self.sun_prog["m_model"].write(glm.translate(glm.vec3(self.lightpos)))
        self.sun.render(self.sun_prog)

    def draw_nodes_light(self, node):
        if node.mesh:
            self.basic_light["m_model"].write(node.matrix_global)
            node.mesh.material.mat_texture.texture.use(location=1)
            self.basic_light["texture1"].value = 1
            node.mesh.vao.render(self.basic_light)
        for child in node.children:
            self.draw_nodes_light(child)

    def draw_nodes_depth(self, node):
        if node.mesh:
            self.shadowmap_program["m_model"].write(node.matrix_global)
            node.mesh.vao.render(self.shadowmap_program)
        for child in node.children:
            self.draw_nodes_depth(child)
