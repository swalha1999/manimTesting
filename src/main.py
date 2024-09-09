import sys
import signal
import moderngl
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLRenderer

from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWidgets import (
    QApplication,
)

from pathlib import Path
from os import path
import scene.manim_scene as manim_scene
from view.preview_window import PreviewWindow
from controllers.scene_controller import SceneController

windows = set()

def close_all():
    for window in windows:
        window.close()

    # sys.exit()


def main():
    # read_tokens = Reader("scene/manim_scene.py")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
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

        format = QSurfaceFormat()
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setVersion(3, 2)
        format.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(format)
        renderer = OpenGLRenderer()
        preview_window = PreviewWindow(app, renderer, close_all)
        windows.add(preview_window._widget)
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
        
        scene.render()

    sys.exit(app.exec())



if __name__ == "__main__":
    main()