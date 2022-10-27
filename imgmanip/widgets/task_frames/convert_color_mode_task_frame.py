from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QCheckBox,
    QLayout,
    QLabel,
    QPushButton,
    QColorDialog,
    QComboBox,
)

from imgmanip.models.color_mode import ColorMode
from imgmanip.models.task import ConvertColorModeTask
from imgmanip.widgets.horizontal_line import HorizontalLine


class ConvertColorModeTaskFrame(QFrame):
    def __init__(self, task=None):
        super().__init__()

        if task and type(task) == ConvertColorModeTask:
            self.task = task
        else:
            self.task = ConvertColorModeTask(color_mode=ColorMode.RGB)

        self.description_label = QLabel()
        self.description_label.setText(
            "This task marks convert the image to selected color mode."
        )

        self.color_mode_box = QVBoxLayout()
        self.color_mode_box.setObjectName("color_mode_box")
        self.color_mode_box.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.color_mode_picker = QComboBox(self)
        self.color_mode_picker.addItems([color_mode.value for color_mode in ColorMode])
        self.color_mode_picker.setCurrentText(self.task.color_mode.value)
        self.color_mode_picker.currentTextChanged.connect(self.change_values)

        self.color_mode_box.addWidget(self.description_label)
        self.color_mode_box.addWidget(HorizontalLine())
        self.color_mode_box.addWidget(self.color_mode_picker)

        self.setLayout(self.color_mode_box)
        self.hide()

    # Change values
    def change_values(self):
        self.task.color_mode = ColorMode(self.color_mode_picker.currentText())
        self.task.name_extended = (
            f"Convert color mode: {self.color_mode_picker.currentText()}"
        )
