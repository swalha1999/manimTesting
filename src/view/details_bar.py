from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QComboBox,
    QHBoxLayout,
    QGroupBox,
    QFormLayout,
    QSpinBox,
    QDoubleSpinBox,
    QColorDialog,
    QMessageBox,
    QInputDialog,
)

from intermediate.ianimation import ICreate, IFadeIn, IReplacementTransform
from intermediate.imobject import ICircle, IGroup, INone, ISquare, IStar, ITriangle
import controllers.mobject_helper as mh
from manim import VGroup


TOP_WIDGETS_NUM = 1  # stretch n groupbox

class DetailsBar(QWidget):
    """
    Right widget which contains information for currently
    selected Mobject and current state
    """

    def __init__(self, scene_controller, scene_state_controller, close_handler):
        super().__init__()

        self.scene_controller = scene_controller
        self.scene_state_controller = scene_state_controller
        self.close_handler = close_handler

        self.selected_imobject = INone()

        self.setWindowTitle(" ")

        self.setGeometry(1450, 250, 150, 600)

        self.layout = QVBoxLayout()

        self.animation_run_time = QDoubleSpinBox()
        self.animation_run_time.setMinimum(0)
        self.animation_run_time.setSuffix("s")
        self.animation_run_time.valueChanged.connect(
            self.change_animation_run_time_handler
        )
        self.animation_run_time.setValue(scene_state_controller.curr.run_time)
        
        self.loop_cb = QComboBox()
        self.loop_cb.addItem("None")
        self.loop_cb.addItems([f"State {n}" for n in range(1, scene_state_controller.end.idx)])
        self.loop_cb.currentIndexChanged.connect(self.loop_cb_handler)

        self.loop_times = QSpinBox()
        self.loop_times.setMinimum(0)
        self.loop_times.setSuffix(" times")
        self.loop_times.valueChanged.connect(self.change_loop_times_handler)

        self.state_group_box = QGroupBox(f"State {scene_state_controller.curr.idx}")
        state_layout = QFormLayout()
        state_layout.addRow(QLabel("Run time:"), self.animation_run_time)
        state_layout.addRow(QLabel("Loop to:"), self.loop_cb)
        state_layout.addRow(QLabel("for:"), self.loop_times)

        self.state_group_box.setLayout(state_layout)
        self.layout.addWidget(self.state_group_box)
        self.layout.addStretch()
        self.empty_label = QLabel("nothing selected")
        self.layout.addWidget(self.empty_label)
        self.layout.addStretch()

        self.intro_cb = QComboBox()
        self.intro_cb.addItems(["None", "Create", "FadeIn"])
        self.intro_cb.currentIndexChanged.connect(self.intro_anim_handler)

        self.change_color_btn = QPushButton("change colour")
        self.change_color_btn.clicked.connect(self.change_color_btn_handler)

        self.scale_box = QDoubleSpinBox()
        self.scale_box.setMinimum(0)
        self.scale_box.setSingleStep(0.5)
        self.scale_box.valueChanged.connect(self.scale_box_handler)

        remove_btn = QPushButton("remove mobject")
        remove_btn.clicked.connect(self.remove_mobject_handler)

        transform_btn = QPushButton("add transform")
        transform_btn.clicked.connect(self.add_transform_handler)

        self.group_cb = QComboBox()
        self.group_cb.currentIndexChanged.connect(self.group_change_handler)

        self.new_group_btn = QPushButton("+")
        self.new_group_btn.clicked.connect(self.new_group_handler)

        self.group_row = QHBoxLayout()
        self.group_row.addWidget(self.group_cb)
        self.group_row.addWidget(self.new_group_btn)

        self.mobj_group_box = QGroupBox(
            f"Selected: {mh.get_name(self.selected_imobject)}"
        )
        mobj_layout = QFormLayout()
        mobj_layout.addRow(QLabel("Appear animation:"), self.intro_cb)
        mobj_layout.addRow(QLabel("Colour:"), self.change_color_btn)
        mobj_layout.addRow(QLabel("Scale:"), self.scale_box)
        mobj_layout.addRow(QLabel("Grouping:"), self.group_row)
        mobj_layout.addRow(QLabel("Remove:"), remove_btn)
        mobj_layout.addRow(QLabel("Add transform:"), transform_btn)
        self.mobj_group_box.setLayout(mobj_layout)

        self.all_widgets = (self.mobj_group_box,)

        self.change_parent_cb = QComboBox()
        self.change_parent_cb.addItem("None")
        self.change_parent_cb.currentIndexChanged.connect(self.change_parent_handler)

        self.change_node_text = QLineEdit()
        self.change_node_text.editingFinished.connect(self.change_node_text_handler)

        self.add_child_btn = QPushButton("add child")
        self.align_children_btn = QPushButton("align children")
        
        self.curr_idx = -1

        scene_controller.selectedMobjectChange.connect(self.refresh)
        scene_state_controller.stateChange.connect(lambda i: self.refresh())
        
        self.setLayout(self.layout)

    def refresh(self, imobject=None):
        if (
            imobject == self.selected_imobject
            and self.curr_idx == self.scene_state_controller.curr.idx
        ):
            return  # nothing happened
        if imobject is None:
            imobject = self.selected_imobject
        self.curr_idx = self.scene_state_controller.curr.idx
        self.clear_items()
        self.selected_imobject = imobject
        self.add_items(imobject)

    def add_items(self, imobject):
        self.state_group_box.setTitle(f"State {self.scene_state_controller.curr.idx}")
        self.animation_run_time.setValue(self.scene_state_controller.curr.run_time)
        self.loop_cb.addItem("None")
        self.loop_cb.addItems(
            [f"State {n}" for n in range(1, self.scene_state_controller.end.idx)]
        )
        self.loop_cb.setCurrentIndex(
            self.loop_cb.findText(f"State {self.scene_state_controller.curr.loop[0]}")
            if self.scene_state_controller.curr.loop is not None
            else 0
        )
        self.loop_times.setValue(
            self.scene_state_controller.curr.loop_cnt
            if self.scene_state_controller.curr.loop_cnt is not None
            else 0
        )
        self.loop_times.blockSignals(False)
        self.loop_cb.blockSignals(False)
        if isinstance(imobject, INone):
            self.layout.insertWidget(
                self.layout.count() - 1, QLabel("nothing selected")
            )
            return

        # fresh add
        for w in self.all_widgets:
            self.layout.insertWidget(self.layout.count() - 1, w)

        
        self.mobj_group_box.setTitle(f"Selected: {mh.get_name(imobject)}")
        # print("REFRESHED INTRO", imobject.intro_anim.__class__.__name__ if imobject.intro_anim is not None else 'None')
        self.intro_cb.blockSignals(True)
        self.intro_cb.setCurrentIndex(
            self.intro_cb.findText(imobject.intro_anim.__class__.__name__[1:])
            if imobject.intro_anim is not None
            else 0
        )
        self.intro_cb.blockSignals(False)

        self.group_cb.addItem("None")
        self.group_cb.addItems([mh.get_name(im) for im in mh.get_groups()])
        self.group_cb.setCurrentIndex(
            self.group_cb.findText(
                mh.get_name(imobject.group) if imobject.group is not None else "None"
            )
        )
        self.group_cb.blockSignals(False)

        self.scale_box.blockSignals(True)
        self.scale_box.setValue(self.scene_state_controller.get_curr_scale(imobject))
        self.scale_box.blockSignals(False)

    def clear_items(self):
        self.change_node_text.blockSignals(True)
        self.loop_cb.blockSignals(True)
        self.loop_times.blockSignals(True)
        self.group_cb.blockSignals(True)
        for i in range(self.layout.count() - 2, TOP_WIDGETS_NUM, -1):
            child = self.layout.itemAt(i).widget()
            # print("clearing " + child.__class__.__name__ if child is not None else "NONE")
            if child is None:
                child = self.layout.itemAt(i).layout()
            if child is not None:
                child.setParent(None)

        
        self.loop_cb.clear()
        self.group_cb.clear()

    def loop_cb_handler(self, i):
        if self.change_parent_cb.count == 0 or not self.loop_cb.currentText():
            return

        if self.loop_cb.currentText() == "None":
            self.scene_state_controller.curr.loop = None
        else:
            state_num = int(self.loop_cb.currentText()[6:])
            if not self.loop_times.text:
                self.loop_times.setValue(1)

            self.scene_state_controller.curr.loop = (state_num, 1)
            self.scene_state_controller.curr.loop_cnt = 1

    def change_loop_times_handler(self, value):
        self.scene_state_controller.curr.loop_cnt = value

    def change_node_text_handler(self):
        self.selected_imobject.edited_at = self.scene_state_controller.curr.idx
        text = self.change_node_text.text()
        self.selected_imobject.change_label_text(text)

    def change_animation_run_time_handler(self, value):
        self.scene_state_controller.curr.run_time = value

    def change_parent_handler(self, i):
        # print("CHANGE PARENT")
        imobj_name = self.change_parent_cb.currentText()
        imobj = mh.get_imobject_by_name(imobj_name) if imobj_name is not None else None

        self.selected_imobject.change_parent(imobj)

    def intro_anim_handler(self, i):
        if isinstance(self.selected_imobject, INone):
            return

        imobject = self.selected_imobject
        affected_imobjects = [imobject]
        
        for aff_imobj in affected_imobjects:
            if aff_imobj.intro_anim is not None:
                aff_imobj.added_state.animations.remove(aff_imobj.intro_anim)
            else:
                aff_imobj.added_state.added.remove(aff_imobj)

            # self.scene_controller.remove(aff_imobj)
            match i:
                case 0:
                    aff_imobj.intro_anim = None
                case 1:
                    aff_imobj.intro_anim = ICreate(aff_imobj)
                case 2:
                    aff_imobj.intro_anim = IFadeIn(aff_imobj)

            if aff_imobj.intro_anim is not None:
                aff_imobj.added_state.animations.append(aff_imobj.intro_anim)
                # aff_imobj.added_state.play_copy(aff_imobj.intro_anim, self.scene_controller.scene)
            else:
                aff_imobj.added_state.added.append(aff_imobj)
                # self.scene_controller.addCopy(aff_imobj)

    def remove_mobject_handler(self):
        imobject = self.selected_imobject

        msg = QMessageBox()
        msg.setWindowTitle("Manimate")
        msg.setText(f"Are you sure you want to remove this MObject?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setDetailedText(f"You will remove {mh.get_name(imobject)} from this state, you could potentially lose this MObject forever.")
        ret = msg.exec_()
        if ret == QMessageBox.Ok:
            affected_imobjects = [imobject]
            for aff_imobj in affected_imobjects:
                self.scene_state_controller.instant_remove_obj_at_curr(aff_imobj)
            self.refresh()

    def new_group_handler(self):
        group = IGroup()
        self.scene_state_controller.instant_add_object_to_curr(group, select=False)
        mh.groups.add(group)

        self.refresh()  # show new igroup in combobox

    def group_change_handler(self, i):
        if isinstance(self.selected_imobject, INone):
            return

        imobject = self.selected_imobject

        if self.scene_state_controller.created_at_curr_state(imobject):
            self.show_creation_error()
            return

        mobject = mh.get_copy(imobject)
        if imobject.group is not None:
            mh.get_copy(imobject.group).remove(mobject)
            self.scene_controller.scene.add(mobject)

        group_name = self.group_cb.currentText()
        if group_name != "None":
            igroup = mh.get_imobject_by_name(group_name)
            group = mh.get_copy(igroup)

            igroup.add(imobject)
            self.scene_state_controller.curr.called_mobject_functions[igroup]["add"].add(
                imobject
            )

        else:
            pass  # TODO: tabs for each child

    def change_color_btn_handler(self):
        color = QColorDialog.getColor()

        if color.isValid():
            imobject = self.selected_imobject
            mcopy = mh.get_copy(imobject)

            mcopy.set_color(color.name())
            imobject.color_changed = color.name()
            self.scene_controller.selected[mcopy] = color.name()
            target = mcopy.copy()

            self.scene_state_controller.edit_transform_target(
                imobject, target, color=color.name()
            )
            if not imobject.user_defined and isinstance(imobject.mobject, VGroup):
                for child in imobject.vgroup_children:
                    child_mobject = mh.get_copy(child)
                    child_mobject.set_color(color.name())
                    if child in self.scene_state_controller.curr.targets:
                        self.scene_state_controller.curr.targets[child].set_color(color.name())
                    # self.fsm_controller.edit_transform_target(child, child_mobject , color=color.name())

    def scale_box_handler(self, value):
        imobject = self.selected_imobject
        mcopy = mh.get_copy(imobject)

        old_scale = self.scene_state_controller.get_curr_scale(imobject)
        new_scale = self.scene_state_controller.clean_scale(value)
        mcopy.scale(new_scale / old_scale)
        target = mcopy.copy()
    
        if "past_scale" not in self.scene_state_controller.curr.rev_attributes[imobject]:
            self.scene_state_controller.curr.rev_attributes[imobject][
                "past_scale"
            ] = imobject.past_scale
        self.scene_state_controller.curr.changed_mobject_attributes[imobject][
            "past_scale"
        ] = new_scale
        imobject.past_scale = new_scale

        self.scene_state_controller.edit_transform_target(
            imobject, target, scale=new_scale
        )

    def name_edit_handler(self):

        new_name = self.name_edit.text
        if not mh.set_name(self.selected_imobject, new_name):
            msg = QMessageBox()
            msg.setWindowTitle("Manimate")
            msg.setText("Name is already in use!")
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            conflict_mobj = mh.get_imobject_by_name(new_name)
            msg.setDetailedText(
                f"There is another {conflict_mobj.__class__.__name__} with the same name {new_name}."
            )

            msg.exec_()

        self.refresh()

    def show_creation_error(self):
        self.show_error_box(
            "Cannot perform this action when you just created this object!",
            "You can perform this action on the next frame.",
        )

    def show_error_box(self, text, detailed_text):
        msg = QMessageBox()
        msg.setWindowTitle("Manimate")
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)

        if detailed_text:
            msg.setDetailedText(detailed_text)

        msg.exec_()

    def add_transform_handler(self):
        imobject = self.selected_imobject
        if isinstance(imobject.mobject, VGroup):
            self.show_error_box("Transforms unsupported for groups for now.", None)
            return

        if self.scene_state_controller.created_at_curr_state(imobject):
            self.show_creation_error()
            return

        curr_state = self.scene_state_controller.curr
        items = ["Circle", "Square", "Star", "Triangle"]
        item, ok = QInputDialog.getItem(
            self, "Choose Target", "Select Target MObject", items, 0, False
        )
        if ok:
            print("TRANSFORM GET COPY")
            mobject = mh.get_copy(imobject)
            center_point = mobject.get_center().copy()

            itarget = None
            match item:
                case "Circle":
                    itarget = ICircle()
                case "Square":
                    itarget = ISquare()
                case "Star":
                    itarget = IStar()
                case "Triangle":
                    itarget = ITriangle()
            curr_state.capture_prev(mobject)
            itarget.added_state = curr_state

            imobject.edited_at = curr_state.idx

            target = itarget.mobject

            curr_state.add_replacement_transform(imobject, itarget)

            print("1")
            curr_state.targets[itarget] = target.move_to(center_point)
            curr_state.target_decl_str[itarget] = itarget.decl_str()

            curr_state.play_copy(
                IReplacementTransform(imobject, itarget), self.scene_controller.scene
            )
            
            
            curr_state.called_target_functions[itarget]["move_to"] = {
                str(center_point.tolist())
            }

            self.scene_controller.set_selected_mobject(mh.get_copy(itarget))

    def closeEvent(self, e):
        self.close_handler()
        e.accept()
