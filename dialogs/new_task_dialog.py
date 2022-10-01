from PySide6.QtCore import (QMetaObject,
                            Qt)
from PySide6.QtWidgets import (QDialog, QDialogButtonBox,
                               QSizePolicy, QGridLayout, QVBoxLayout, QLayout, QLabel, QComboBox, QLineEdit,
                               QFrame, QHBoxLayout, QSlider, QCheckBox)

from models.task import ResizeTask, InvertTask, ConvertTask, CompressTask, ColorDetectionTask
from models.image_extension import ImageExtension
from widgets.new_tasks.color_detection_task_frame import ColorDetectionTaskFrame
from widgets.new_tasks.compress_task_frame import CompressTaskFrame
from widgets.new_tasks.convert_task_frame import ConvertTaskFrame
from widgets.new_tasks.invert_task_frame import InvertTaskFrame
from widgets.new_tasks.resize_task_frame import ResizeTaskFrame


class NewTaskDialog(QDialog):
    def __init__(self, task=None):
        super().__init__()
        if not self.objectName():
            self.setObjectName(u"self")

        self.setWindowTitle('New task')
        self.task = task

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName(u"grid_layout")

        # Main layout
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.vertical_layout.setSizeConstraint(QLayout.SetDefaultConstraint)

        # Task label
        self.task_picker_frame = QFrame()
        self.task_picker_box = QVBoxLayout()

        self.task_label = QLabel(self)
        self.task_label.setObjectName(u"condition_label")
        self.task_label.setText("Task")

        self.tasks = {
            'resize': ResizeTaskFrame(),
            'invert': InvertTaskFrame(),
            'convert': ConvertTaskFrame(),
            'compress': CompressTaskFrame(),
            'color_detection': ColorDetectionTaskFrame(),
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

        self.vertical_layout.addStretch(20)

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

        if task:
            self.edit_dialog()

        self.change_task()

        QMetaObject.connectSlotsByName(self)

    # Change labels and inputs
    def change_task(self):
        # RESIZE TASK
        selected_task = self.task_picker.currentText()
        for task in self.tasks:
            if selected_task == task:
                self.tasks[task].show()
            else:
                self.tasks[task].hide()

    # Edit dialog
    def edit_dialog(self):
        if type(self.task) == ResizeTask:
            self.task_picker.setCurrentText("resize")
            self.tasks['resize'].resize_width_input.setText(self.task.new_width)
            self.tasks['resize'].resize_height_input.setText(self.task.new_height)
        elif type(self.task) == InvertTask:
            self.task_picker.setCurrentText("invert")
        elif type(self.task) == ConvertTask:
            self.task_picker.setCurrentText("convert")
            self.tasks['convert'].extension_picker.setCurrentText(self.task.convert_ext.value)
        elif type(self.task) == CompressTask:
            self.task_picker.setCurrentText("compress")
            self.tasks['compress'].compress_quality_slider.setValue(self.task.quality)
        elif type(self.task) == ColorDetectionTask:
            self.task_picker.setCurrentText("color_detection")
        self.change_task()
