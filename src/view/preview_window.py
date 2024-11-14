import moderngl_window as mglw
from moderngl_window.context.pyqt5.window import Window as PyQt5Window
from moderngl_window.timers.clock import Timer


class PreviewWindow(PyQt5Window):
    """
    Previews the Manim animations...

    is a subclass of ModernGL's PyQt5 window
    """

    def __init__(self, app, renderer, close_handler) -> None:
        super().__init__()
        self.close_handler = close_handler
        self.app = app
        self._widget.setGeometry(550, 250, 900, 520)
        self.title = "Render Preview Window"

        self.renderer = renderer

        mglw.activate_context(window=self)
        self.timer = Timer()
        self.config = mglw.WindowConfig(ctx=self.ctx, wnd=self, timer=self.timer)
        self.timer.start()

        self.swap_buffers()

    def mouse_move_event(self, event):
        super().mouse_move_event(event)
        x, y = event.x(), event.y()
        dx, dy = self._calc_mouse_delta(x, y)
        point = self.renderer.pixel_coords_to_space_coords(x, y, top_left=True)
        d_point = self.renderer.pixel_coords_to_space_coords(
            dx, dy, relative=True, top_left=True
        )
        self.renderer.scene.mouse_move_event(point, d_point)

    def mouse_press_event(self, event):
        super().mouse_press_event(event)
        x, y = event.x(), event.y()
        button = self._mouse_button_map.get(event.button())
        modifiers = event.modifiers()
        point = self.renderer.pixel_coords_to_space_coords(x, y, top_left=True)
        mouse_button_map = {
            1: "LEFT",
            2: "RIGHT",
        }
        self.renderer.scene.on_mouse_press(point, mouse_button_map[button], modifiers)

    def mouse_release_event(self, event):
        super().mouse_press_event(event)
        x, y = event.x(), event.y()
        button = self._mouse_button_map.get(event.button())
        modifiers = event.modifiers()
        point = self.renderer.pixel_coords_to_space_coords(x, y, top_left=True)
        mouse_button_map = {
            1: "LEFT",
            2: "RIGHT",
        }
        self.renderer.scene.on_mouse_release(point, mouse_button_map[button], modifiers)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.close_handler()
        event.accept()
