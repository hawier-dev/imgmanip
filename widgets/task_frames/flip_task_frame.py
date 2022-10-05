from PySide6.QtWidgets import QFrame, QVBoxLayout, QLayout, QLabel, QComboBox

from models.axis import Axis
from models.task import FlipTask
from widgets.horizontal_line import HorizontalLine


class FlipTaskFrame(QFrame):
    def __init__(self, task=None):
        super().__init__()

        if task and type(task) == FlipTask:
            print(task.axis.value)
            self.task = task
        else:
            self.task = FlipTask(axis=Axis.HORIZONTAL)

        self.flip_box = QVBoxLayout()

        self.description_label = QLabel()
        self.description_label.setText("This task flips the image in horizontal or vertical axis.")

        self.flip_box.setObjectName(u"flip_box")
        self.flip_box.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.axis_picker = QComboBox()

        for axis in Axis:
            self.axis_picker.addItem(axis.value)

        self.axis_picker.setCurrentText(self.task.axis.value)
        self.axis_picker.currentTextChanged.connect(self.change_values)

        self.flip_box.addWidget(self.description_label)
        self.flip_box.addWidget(HorizontalLine())
        self.flip_box.addWidget(self.axis_picker)

        self.setLayout(self.flip_box)
        self.hide()

    # Change values
    def change_values(self):
        self.task.axis = Axis(self.axis_picker.currentText())
