import sys
import signal
import moderngl
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLRenderer

from PySide6.QtWidgets import (
    QApplication,
)

from PyQt5.QtGui import QSurfaceFormat as QSurfaceFormatPyQt5
from PyQt5.QtWidgets import QApplication as QApplicationPyQt5, QMainWindow, QPushButton, QVBoxLayout, QWidget


from pathlib import Path
from os import path
from controllers.scene_state_controller import SceneStateController
from controllers.scene_controller import SceneController
import scene.manim_scene as manim_scene
from view.details_bar import DetailsBar
from view.objects_bar import ObjectsBar
from view.state_bar import StateWidget
from view.preview_window import PreviewWindow
from view.code_preview_window import CodePreviewWindow

windows = set()
pyQt5_windows = set()


def main():
    # read_tokens = Reader("scene/manim_scene.py")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    pyqt5_app = QApplicationPyQt5(sys.argv)
    this_dir, _ = path.split(__file__)
    with tempconfig(
        {
            "input_file": path.join(this_dir, "scene", "manim_scene.py"),
            "disable_caching": True,
            "renderer": "opengl",
            "preview": True,
            "write_to_movie": False,
            "format": None,
        }
    ):

        format = QSurfaceFormatPyQt5()
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setVersion(3, 2)
        format.setProfile(QSurfaceFormatPyQt5.CoreProfile)
        QSurfaceFormatPyQt5.setDefaultFormat(format)
        renderer = OpenGLRenderer()
        preview_window = PreviewWindow(pyqt5_app, renderer, close_all)
        pyQt5_windows.add(preview_window._widget)
        renderer.window = preview_window
        renderer.frame_buffer_object = preview_window.ctx.detect_framebuffer()
        renderer.context = preview_window.ctx
        renderer.context.enable(moderngl.BLEND)
        renderer.context.wireframe = config["enable_wireframe"]
        renderer.context.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE_MINUS_SRC_ALPHA,
            moderngl.ONE,
            moderngl.ONE,
        )

        scene = manim_scene.PreviewScene(renderer)
        renderer.scene = scene

        scene_controller = SceneController(scene, renderer)
        scenes_state_controller = SceneStateController(scene_controller)
        scene_controller.set_scene_state_controller(scenes_state_controller)

        objects_bar = ObjectsBar(scenes_state_controller, close_all)
        objects_bar.show()

        state_bar = StateWidget(scene_controller, scenes_state_controller, close_all)
        state_bar.show()

        details_bar = DetailsBar(scene_controller, scenes_state_controller, close_all)
        # details_bar.show()

        # Add the new CodePreviewWindow
        code_preview = CodePreviewWindow(scenes_state_controller, close_all)
        code_preview.show()

        print(path.join(this_dir, "view", "styles.qss"))
        with open(path.join(this_dir, "view", "styles.qss"), "r") as f:
            _style = f.read()
            for w in (objects_bar, details_bar, state_bar, code_preview):
                windows.add(w)
                w.setStyleSheet(_style)

        scene.render()

    sys.exit(app.exec() and pyqt5_app.exec())



def close_all_pyqt5():
    for window in pyQt5_windows:
        window.close()
    sys.exit()



def close_all():
    for window in windows:
        window.close()
    for window in pyQt5_windows:
        window.close()
    sys.exit()

if __name__ == "__main__":
    main()
