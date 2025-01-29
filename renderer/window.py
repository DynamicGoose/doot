import moderngl
import glm
import moderngl_window as glw
from moderngl_window.context.base.keys import BaseKeys
from moderngl_window.scene.camera import KeyboardCamera


class CameraWindow(glw.WindowConfig):
    """Base class with built in 3D camera support"""
    title = "DOOT"
    resource_dir = "assets"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scene = self.load_scene("Cube/Cube.gltf")
        self.camera = KeyboardCamera(
            BaseKeys(),
            fov=96.0,
            aspect_ratio=self.wnd.aspect_ratio,
            near=0.1,
            far=1000.0,
        )
        self.camera.velocity = 10.0
        self.camera.mouse_sensitivity = 0.25
        self.camera.position = (
            self.scene.get_center()
            + glm.vec3(0.0, 0.0, self.scene.diagonal_size / 1.75)
        )
        self.camera_enabled = True

    def on_key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            self.camera.key_input(key, action, modifiers)

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

    def on_render(self, time: float, frame_time: float):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        self.scene.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=self.camera.matrix,
            time=time,
        )
