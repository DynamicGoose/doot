from renderer.window import CameraWindow
import glm
import moderngl_window as glw
import moderngl

class DootWindow(CameraWindow):
    title = "DOOT"
    resource_dir = "assets"
    fullscreen = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scene = self.load_scene("Sponza/Sponza.gltf")
        
        self.camera.position = (
            self.scene.get_center()
            + glm.vec3(0.0, 0.0, self.scene.diagonal_size / 1.75)
        )
        
    def on_render(self, time: float, frame_time: float):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        self.scene.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=self.camera.matrix,
            time=time,
        )
        
glw.run_window_config(DootWindow)
