from manim import *

class ArabicTex(Tex):
    def __init__(self, *text, font="Amiri", **kwargs):
        # Define the custom template for Arabic text
        mytxtmplt = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
        mytxtmplt.add_to_preamble(
            r"\usepackage{fontspec}"
            r"\usepackage{polyglossia}"
            r"\setmainlanguage{arabic}"
            f"\\setmainfont{{{font}}}"  # Use the specified font
        )
        # Initialize the Tex object with the custom template
        super().__init__(*text, tex_template=mytxtmplt, **kwargs)
        # Reverse the submobjects for correct RTL rendering for each part of the text
        for submob in self.submobjects:
            submob.submobjects.reverse()
        # __________________Fonts Should be downloaded___________________________
        # Noto Naskh Arabic
        # Scheherazade
        # Almarai
        # Cairo
        # KacstOne
        # Lateef

# Example usage of the custom ArabicTex class
class ArabicTextScene(Scene):
    def construct(self):
        txt = ArabicTex(r"\raggedleft هذا نص", r"\\ هذا نص آخر").to_edge(UR)
        self.play(Write(txt))
        self.wait(2)