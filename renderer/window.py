import moderngl_window as glw

class Window(glw.WindowConfig):
    gl_version = (3, 3)
    window_size = (1920, 1080)
    resource_dir = "assets"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # initialization
        self.prog = self.ctx.program(...)
        self.vao = self.ctx.vertex_array(...)
        self.texture = self.ctx.texture(self.wnd.size, 4)
