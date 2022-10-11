from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout, QLineEdit, QLayout, QComboBox

from imgmanip.models.resize_type import ResizeType
from imgmanip.models.task import ResizeTask
from imgmanip.widgets.horizontal_line import HorizontalLine


class ResizeTaskFrame(QFrame):
    def __init__(self, task=None):
        super().__init__()

        if task and type(task) == ResizeTask:
            self.task = task
        else:
            self.task = ResizeTask(resize_type=ResizeType.SIZE, new_width=800, new_height=600)

        self.resize_box = QVBoxLayout()
        self.resize_box.setObjectName(u"resize_box")
        self.resize_box.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.description_label = QLabel()
        self.description_label.setText(
            "This task resizes the images to the given resolution or by percentage.")

        # Resize types
        self.resize_type_picker = QComboBox()
        for resize_type in ResizeType:
            self.resize_type_picker.addItem(resize_type.value)

        self.resize_type_picker.setCurrentText(self.task.resize_type.value)
        self.resize_type_picker.currentTextChanged.connect(self.change_type)

        # Name label
        self.resize_label = QLabel(self)
        self.resize_label.setObjectName(u"name_label")
        size_policy_resize_label = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy_resize_label.setHorizontalStretch(0)
        size_policy_resize_label.setVerticalStretch(0)
        size_policy_resize_label.setHeightForWidth(self.resize_label.sizePolicy().hasHeightForWidth())
        self.resize_label.setSizePolicy(size_policy_resize_label)
        self.resize_label.setText("New size")

        # Resize size type
        # validator
        int_validator = QIntValidator()

        self.resize_size_frame = QFrame()
        self.resize_size_frame.setContentsMargins(0, 0, 0, 0)
        self.resize_inputs_h_box = QHBoxLayout()
        self.resize_inputs_h_box.setContentsMargins(0, 0, 0, 0)
        self.resize_width_input = QLineEdit(self)
        self.resize_width_input.setObjectName(u"resize_width_input")
        self.resize_width_input.setText(str(self.task.new_width))
        self.resize_width_input.setValidator(int_validator)
        self.resize_width_input.textEdited.connect(self.change_resize)

        # X label between width and height -> width x height
        self.x_label = QLabel(self)
        self.x_label.setObjectName(u"name_label")
        self.x_label.setText('x')

        self.resize_height_input = QLineEdit(self)
        self.resize_height_input.setObjectName(u"resize_height_input")
        self.resize_height_input.setText(str(self.task.new_height))
        self.resize_height_input.setValidator(int_validator)
        self.resize_height_input.textEdited.connect(self.change_resize)

        self.resize_inputs_h_box.addWidget(self.resize_width_input)
        self.resize_inputs_h_box.addWidget(self.x_label)
        self.resize_inputs_h_box.addWidget(self.resize_height_input)
        self.resize_size_frame.setLayout(self.resize_inputs_h_box)
        # Resize percentage type
        self.resize_percentage_frame = QFrame()
        self.resize_percentage_frame.setContentsMargins(0, 0, 0, 0)
        self.resize_percentage_h_box = QHBoxLayout()
        self.resize_percentage_h_box.setContentsMargins(0, 0, 0, 0)
        self.percentage_input = QLineEdit(self)
        self.percentage_input.setObjectName(u"percentage_input")
        self.percentage_input.setText(str(self.task.percent))
        self.percentage_input.setValidator(int_validator)
        self.percentage_input.textEdited.connect(self.change_resize)
        # % char
        self.percent_label = QLabel(self)
        self.percent_label.setObjectName(u"name_label")
        self.percent_label.setText('%')

        self.resize_percentage_h_box.addWidget(self.percentage_input)
        self.resize_percentage_h_box.addWidget(self.percent_label)
        self.resize_percentage_frame.setLayout(self.resize_percentage_h_box)

        self.resize_percentage_frame.hide()

        self.resize_box.addWidget(self.description_label)
        self.resize_box.addWidget(HorizontalLine())

        self.resize_box.addWidget(self.resize_label)
        self.resize_box.addWidget(self.resize_type_picker)
        self.resize_box.addWidget(self.resize_size_frame)
        self.resize_box.addWidget(self.resize_percentage_frame)

        self.setLayout(self.resize_box)
        self.change_type()
        self.hide()

    # Change text event for
    def change_resize(self):
        self.task.new_width = int(self.resize_width_input.text())
        self.task.new_height = int(self.resize_height_input.text())
        self.task.percent = float(self.percentage_input.text())

    # Change type of resize
    def change_type(self):
        current_type = self.resize_type_picker.currentText()
        if current_type == 'Size':
            self.resize_size_frame.show()
            self.resize_percentage_frame.hide()
        elif current_type == 'Percentage':
            self.resize_size_frame.hide()
            self.resize_percentage_frame.show()

        self.task.resize_type = ResizeType(current_type)
