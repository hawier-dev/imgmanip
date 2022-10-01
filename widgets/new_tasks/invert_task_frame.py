from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLayout, QLabel

from widgets.horizontal_line import HorizontalLine


class InvertTaskFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.inverse_box = QVBoxLayout()

        self.description_label = QLabel()
        self.description_label.setText(
            "This task inverts the colors of the image.")

        self.inverse_box.setObjectName(u"inverse_box")
        self.inverse_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.inverse_box.addWidget(self.description_label)
        self.inverse_box.addWidget(HorizontalLine())
        self.setLayout(self.inverse_box)
        self.hide()
