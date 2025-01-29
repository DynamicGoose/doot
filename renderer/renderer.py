import moderngl as gl
from renderer.window import create_window

def run_event_loop():
    window = create_window("DOOT")
    while not window.is_closing:
        window.clear()

        window.swap_buffers()
