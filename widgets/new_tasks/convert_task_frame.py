from PySide6.QtWidgets import QWidget, QLayout, QVBoxLayout, QFrame, QComboBox, QLabel

from models.image_extension import ImageExtension


class ConvertTaskFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.convert_box = QVBoxLayout()
        self.convert_box.setObjectName(u"convert_box")
        self.convert_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        # Extension picker label
        self.extension_picker_label = QLabel()
        self.extension_picker_label.setText("New file extension")
        # Extension picker
        self.extension_picker = QComboBox(self)
        self.extension_picker.addItems([ext.value for ext in ImageExtension])

        self.extension_picker.setObjectName(u"extension_picker")

        # self.extension_picker.currentTextChanged.connect(self.change_extension)
        self.convert_box.addWidget(self.extension_picker_label)
        self.convert_box.addWidget(self.extension_picker)
        self.setLayout(self.convert_box)
        self.hide()
