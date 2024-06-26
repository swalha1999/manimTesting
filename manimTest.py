from manim import *
from manim.opengl import *
import numpy as np

class OpenGLShow(Scene):
    def construct(self):
        angle = 0
        circle = Circle()
        square = Square()
        square.rotate(PI / 4)
        cube = Cube(fill_color=RED, fill_opacity=0.2)
        cube.set_color(BLUE)
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))        
        self.play(GrowFromCenter(cube))

        def callback(sender, data):
            nonlocal angle  # Declare angle as nonlocal to modify it within the callback
            new_angle = dpg.get_value(sender)
            rotation_amount = new_angle - angle
            cube.rotate(rotation_amount)
            angle = new_angle  # Update the angle to the new value

        # Define a widget for the interactive slider (example using Dear PyGui-like pseudo-code)
        self.widgets.append(
            {
                "name": "cube_rotation",
                "widget": "slider_float",
                "callback": callback,
                "min_value": 0,
                "max_value": 2*PI,
                "default_value": 0,
            }
        )

        # self.interactive_embed()

