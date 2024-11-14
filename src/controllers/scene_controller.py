from manim.utils.color import *
from manim import *
from PySide6.QtCore import Signal, QObject

from intermediate.imobject import IMobject, INone,IGroup
import controllers.mobject_helper as mh



class SceneController(QObject):
    """
    Handles any rendering on the manim scene
    """

    selectedMobjectChange = Signal(IMobject)

    def __init__(self, scene, renderer):
        super().__init__()
        self.scene = scene
        self.renderer = renderer
        scene.handler = self
        self.selected = {}
        self.scene_state_controller = None
        self.ctrldown = False

    def set_scene_state_controller(self, scene_state_controller):
        self.scene_state_controller = scene_state_controller

    def add_copy(self, imobject):
        self.scene.add(mh.get_copy(imobject))

    def remove(self, imobject):
        self.scene.remove(mh.get_copy(imobject))

    """ Selection functions """

    def set_selected_mobject(self, mobject, ctrldown=False):
        if ctrldown:
            self.ctrldown = True

        if not self.ctrldown:  # TODO
            self.unselect_mobjects()

        imobject = mh.get_original(mobject)
        self.set_selected_imobject(imobject)

    def set_selected_imobject(self, imobject):
        if imobject.parent_imobject is not None:
            imobject = imobject.parent_imobject

        if imobject.group is not None:
            imobject = imobject.group

        mobject = mh.get_copy(imobject)
        if mobject in self.selected:
            return

        self.selected[mobject] = mobject.get_color().to_hex()

        self.scene_state_controller.curr.capture_prev(mobject)

        self.selectedMobjectChange.emit(imobject)

    def unselect_mobjects(self):
        self.ctrldown = False
        for mobject, color in self.selected.items():
            imobject = mh.get_original(mobject)

            if not isinstance(mobject, MarkupText) and not isinstance(imobject, IGroup):
                mobject.set_color(color)


        self.selected = {}

        self.selectedMobjectChange.emit(INone())

    """" Movement functions """
    # TODO: refactor non-scene related functions out
    def confirm_selected_shift(self, delta, altdown):
        for mcopy in self.selected:
            self.scene_state_controller.confirm_move(mcopy, delta, altdown)

    def created_at_curr_state_with_anim(self, mcopy):
        imobject = mh.get_original(mcopy)

        if imobject is None:
            return True  # block any interaction with it

        return self.scene_state_controller.created_at_curr_state_with_anim(imobject)

    def move_selected_by(self, delta):
        if not self.selected:
            return
        for mobject in self.selected:
            mobject.shift(delta)
