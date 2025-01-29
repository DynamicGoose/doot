import moderngl_window as glw
from moderngl_window.conf import settings

def create_window(title):
    settings.WINDOW['class'] = 'moderngl_window.context.glfw.Window'
    settings.WINDOW['gl_version'] = (4, 1)
    settings.WINDOW['title'] = title

    return glw.create_window_from_settings()
