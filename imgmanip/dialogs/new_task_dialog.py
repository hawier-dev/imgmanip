from PySide6.QtCore import (QMetaObject,
                            Qt)
from PySide6.QtWidgets import (QDialog, QDialogButtonBox,
                               QSizePolicy, QGridLayout, QVBoxLayout, QLayout, QLabel, QComboBox, QFrame)

from imgmanip.widgets.task_frames.color_detection_task_frame import ColorDetectionTaskFrame
from imgmanip.widgets.task_frames.compress_task_frame import CompressTaskFrame
from imgmanip.widgets.task_frames.convert_task_frame import ConvertTaskFrame
from imgmanip.widgets.task_frames.flip_task_frame import FlipTaskFrame
from imgmanip.widgets.task_frames.invert_task_frame import InvertTaskFrame
from imgmanip.widgets.task_frames.resize_task_frame import ResizeTaskFrame


class NewTaskDialog(QDialog):
    def __init__(self, task_to_edit=None):
        super().__init__()
        if not self.objectName():
            self.setObjectName(u"self")

        self.setWindowTitle('New task')
        self.task_to_edit = task_to_edit

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName(u"grid_layout")

        # Main layout
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.vertical_layout.setSizeConstraint(QLayout.SetDefaultConstraint)

        # Task label
        self.task_picker_frame = QFrame()
        self.task_picker_box = QVBoxLayout()
        self.task_picker_box.setContentsMargins(10, 0, 10, 0)

        self.task_label = QLabel(self)
        self.task_label.setObjectName(u"condition_label")
        self.task_label.setText("Task")

        self.tasks = {
            'resize': ResizeTaskFrame(self.task_to_edit),
            'invert': InvertTaskFrame(self.task_to_edit),
            'flip': FlipTaskFrame(self.task_to_edit),
            'convert': ConvertTaskFrame(self.task_to_edit),
            'compress': CompressTaskFrame(self.task_to_edit),
            'color_detection': ColorDetectionTaskFrame(self.task_to_edit),
        }

        # Task input
        self.task_picker = QComboBox(self)
        self.task_picker.addItems([task for task in self.tasks])

        self.task_picker.setObjectName(u"combo_box")
        self.task_picker.currentTextChanged.connect(self.change_task)
        self.task_picker_box.addWidget(self.task_label)
        self.task_picker_box.addWidget(self.task_picker)
        self.task_picker_frame.setLayout(self.task_picker_box)

        self.vertical_layout.addWidget(self.task_picker_frame)

        # Widget frames
        for task in self.tasks:
            self.vertical_layout.addWidget(self.tasks[task])

        self.grid_layout.addLayout(self.vertical_layout, 0, 0, 1, 1)

        # Button "Cancel" and "Ok"
        self.button_box = QDialogButtonBox(self)
        self.button_box.setObjectName(u"button_box")
        size_policy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy3.setHorizontalStretch(0)
        size_policy3.setVerticalStretch(0)
        size_policy3.setHeightForWidth(self.button_box.sizePolicy().hasHeightForWidth())
        self.button_box.setSizePolicy(size_policy3)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.button(QDialogButtonBox.Cancel).setStyleSheet(
            'border: 0.5px solid #555555; background-color: #202124; color: #99A2FF')

        self.button_box.button(QDialogButtonBox.Ok).setStyleSheet('background-color: #99A2FF; color: #111111;')
        self.button_box.setCenterButtons(True)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.grid_layout.addWidget(self.button_box, 1, 0, 1, 1)

        if task_to_edit:
            self.edit_dialog()

        self.change_task()

        QMetaObject.connectSlotsByName(self)

    # Change labels and inputs
    def change_task(self):
        # RESIZE TASK
        selected_task = self.task_picker.currentText()
        for task in self.tasks:
            self.tasks[task].hide()

        self.tasks[selected_task].show()
        self.setFixedSize(self.sizeHint())

    # Edit dialog
    def edit_dialog(self):
        self.task_picker.setCurrentText(self.task_to_edit.name)
        self.tasks[self.task_to_edit.name].task = self.task_to_edit

        self.change_task()
