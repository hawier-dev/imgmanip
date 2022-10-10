from PySide6.QtWidgets import QLayout, QVBoxLayout, QFrame, QComboBox, QLabel

from imgmanip.models.image_extension import ImageExtension
from imgmanip.models.task import ConvertTask
from imgmanip.widgets.horizontal_line import HorizontalLine


class ConvertTaskFrame(QFrame):
    def __init__(self, task=None):
        super().__init__()

        if task and type(task) == ConvertTask:
            self.task = task
        else:
            self.task = ConvertTask(convert_ext=ImageExtension.PNG)

        self.convert_box = QVBoxLayout()

        self.description_label = QLabel()
        self.description_label.setText(
            "This task converts the image to the other format.")

        self.convert_box.setObjectName(u"convert_box")
        self.convert_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        # Extension picker label
        self.extension_picker_label = QLabel()
        self.extension_picker_label.setText("New file extension")
        # Extension picker
        self.extension_picker = QComboBox(self)
        self.extension_picker.addItems([ext.value for ext in ImageExtension])
        self.extension_picker.setCurrentText(self.task.convert_ext.value)
        self.extension_picker.currentTextChanged.connect(self.change_values)

        self.extension_picker.setObjectName(u"extension_picker")

        # self.extension_picker.currentTextChanged.connect(self.change_extension)
        self.convert_box.addWidget(self.description_label)
        self.convert_box.addWidget(HorizontalLine())
        self.convert_box.addWidget(self.extension_picker_label)
        self.convert_box.addWidget(self.extension_picker)
        self.setLayout(self.convert_box)
        self.hide()

    # Change values
    def change_values(self):
        self.task.convert_ext = ImageExtension(self.extension_picker.currentText())
