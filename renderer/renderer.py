import moderngl as gl
from moderngl_window import run_window_config

import renderer.window

def run_event_loop():
    run_window_config(renderer.window.CameraWindow)
