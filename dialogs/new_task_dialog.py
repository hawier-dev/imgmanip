from PySide6.QtCore import (QMetaObject,
                            Qt)
from PySide6.QtWidgets import (QDialog, QDialogButtonBox,
                               QSizePolicy, QGridLayout, QVBoxLayout, QLayout, QLabel, QComboBox, QLineEdit,
                               QFrame, QHBoxLayout, QSlider)

from models.task import ImageExtension, TaskResize, TaskInvert, TaskConvert, TaskCompress


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

        # Task input
        self.task_picker = QComboBox(self)

        self.task_picker.addItem("resize")
        self.task_picker.addItem("invert")
        self.task_picker.addItem("convert")
        self.task_picker.addItem("compress")

        self.task_picker.setObjectName(u"combo_box")
        self.task_picker.currentTextChanged.connect(self.change_task)
        self.task_picker_box.addWidget(self.task_label)
        self.task_picker_box.addWidget(self.task_picker)
        self.task_picker_frame.setLayout(self.task_picker_box)

        # region RESIZE_TASK
        # Resize box
        self.resize_frame = QFrame()
        self.resize_box = QVBoxLayout()
        self.resize_box.setObjectName(u"resize_box")
        self.resize_box.setSizeConstraint(QLayout.SetDefaultConstraint)

        # Name label
        self.resize_label = QLabel(self)
        self.resize_label.setObjectName(u"name_label")
        size_policy_resize_label = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy_resize_label.setHorizontalStretch(0)
        size_policy_resize_label.setVerticalStretch(0)
        size_policy_resize_label.setHeightForWidth(self.resize_label.sizePolicy().hasHeightForWidth())
        self.resize_label.setSizePolicy(size_policy_resize_label)
        self.resize_label.setText("New size")

        # Resize inputs
        self.resize_inputs_h_box = QHBoxLayout()
        self.resize_width_input = QLineEdit(self)
        self.resize_width_input.setObjectName(u"resize_width_input")

        # X label between width and height -> width x height
        self.x_label = QLabel(self)
        self.x_label.setObjectName(u"name_label")
        self.x_label.setText('x')

        self.resize_height_input = QLineEdit(self)
        self.resize_height_input.setObjectName(u"resize_height_input")

        # size_policy_resize_input = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # size_policy_resize_input.setHorizontalStretch(0)
        # size_policy_resize_input.setVerticalStretch(0)
        # size_policy_resize_input.setHeightForWidth(self.resize_width_input.sizePolicy().hasHeightForWidth())
        # self.resize_width_input.setSizePolicy(size_policy_resize_input)
        self.resize_inputs_h_box.addWidget(self.resize_width_input)
        self.resize_inputs_h_box.addWidget(self.x_label)
        self.resize_inputs_h_box.addWidget(self.resize_height_input)
        self.resize_box.addWidget(self.resize_label)
        self.resize_box.addLayout(self.resize_inputs_h_box)

        self.resize_frame.setLayout(self.resize_box)
        # endregion

        # region INVERSE_TASK
        # Inverse box
        self.inverse_frame = QFrame()
        self.inverse_box = QVBoxLayout()
        self.inverse_box.setObjectName(u"inverse_box")
        self.inverse_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.inverse_frame.setLayout(self.inverse_box)
        # endregion

        # region CONVERT_TASK
        # Convert box
        self.convert_frame = QFrame()
        self.convert_box = QVBoxLayout()
        self.convert_box.setObjectName(u"convert_box")
        self.convert_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        # Extension picker label
        self.extension_picker_label = QLabel()
        self.extension_picker_label.setText("New file extension")
        # Extension picker
        self.extension_picker = QComboBox(self)
        self.extension_picker.addItem(ImageExtension.TIFF.value)
        self.extension_picker.addItem(ImageExtension.PNG.value)
        self.extension_picker.addItem(ImageExtension.JPEG.value)
        self.extension_picker.addItem(ImageExtension.GIF.value)

        self.extension_picker.setObjectName(u"extension_picker")

        # self.extension_picker.currentTextChanged.connect(self.change_extension)
        self.convert_box.addWidget(self.extension_picker_label)
        self.convert_box.addWidget(self.extension_picker)
        self.convert_frame.setLayout(self.convert_box)
        self.convert_frame.hide()
        # endregion

        # region COMPRESS_TASK
        # Compress box
        self.compress_frame = QFrame()
        self.compress_box = QVBoxLayout()
        self.compress_box.setObjectName(u"compress_box")
        self.compress_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        # Label + slider box
        self.compress_quality_box = QHBoxLayout()
        # compress quality label
        self.compress_quality_label = QLabel()
        self.compress_quality_label.setText('Quality')
        # compress quality slider label
        self.compress_quality_value_label = QLabel()
        # compress quality slider
        self.compress_quality_slider = QSlider(Qt.Horizontal)
        self.compress_quality_slider.setMinimum(1)
        self.compress_quality_slider.setMaximum(100)
        self.compress_quality_slider.setValue(95)
        self.compress_quality_slider.setTickPosition(QSlider.TicksBelow)
        self.compress_quality_slider.setTickInterval(5)
        self.compress_quality_slider.valueChanged.connect(self.update_slider_value)
        self.compress_quality_value_label.setText(f'{self.compress_quality_slider.value()}%')
        self.compress_quality_value_label.setFixedWidth(50)

        self.compress_quality_box.addWidget(self.compress_quality_value_label)
        self.compress_quality_box.addWidget(self.compress_quality_slider)
        self.compress_box.addWidget(self.compress_quality_label)
        self.compress_box.addLayout(self.compress_quality_box)
        self.compress_frame.setLayout(self.compress_box)
        self.compress_frame.hide()
        # endregion

        # region Color detection
        # Color detection box
        self.color_detection_frame = QFrame()
        self.color_detection_box = QVBoxLayout()
        self.color_detection_box.setObjectName(u"color_detection_box")
        self.color_detection_box.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.color_detection_frame.setLayout(self.color_detection_box)
        self.color_detection_frame.hide()
        # endregion

        self.vertical_layout.addWidget(self.task_picker_frame)
        self.vertical_layout.addWidget(self.resize_frame)
        self.vertical_layout.addWidget(self.inverse_frame)
        self.vertical_layout.addWidget(self.convert_frame)
        self.vertical_layout.addWidget(self.compress_frame)
        self.vertical_layout.addWidget(self.color_detection_frame)
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

        QMetaObject.connectSlotsByName(self)

    # Change labels and inputs
    def change_task(self):
        # RESIZE TASK
        if self.task_picker.currentText() == 'resize':
            self.resize_frame.show()
            self.inverse_frame.hide()
            self.convert_frame.hide()
            self.compress_frame.hide()
        # INVERT TASK
        elif self.task_picker.currentText() == 'invert':
            self.resize_frame.hide()
            self.inverse_frame.show()
            self.convert_frame.hide()
            self.compress_frame.hide()
        # CONVERT TASK
        elif self.task_picker.currentText() == 'convert':
            self.resize_frame.hide()
            self.inverse_frame.hide()
            self.convert_frame.show()
            self.compress_frame.hide()
        # COMPRESS TASK
        elif self.task_picker.currentText() == 'compress':
            self.resize_frame.hide()
            self.inverse_frame.hide()
            self.convert_frame.hide()
            self.compress_frame.show()

    # Edit dialog
    def edit_dialog(self):
        if type(self.task) == TaskResize:
            self.task_picker.setCurrentText("resize")
            self.resize_width_input.setText(self.task.new_width)
            self.resize_height_input.setText(self.task.new_height)
        elif type(self.task) == TaskInvert:
            self.task_picker.setCurrentText("invert")
        elif type(self.task) == TaskConvert:
            self.task_picker.setCurrentText("convert")
            self.extension_picker.setCurrentText(self.task.convert_ext.value)
        elif type(self.task) == TaskCompress:
            self.task_picker.setCurrentText("compress")
            self.compress_quality_slider.setValue(self.task.quality)
        self.change_task()

    # Compress slider value
    def update_slider_value(self):
        self.compress_quality_value_label.setText(f'{self.compress_quality_slider.value()}%')
