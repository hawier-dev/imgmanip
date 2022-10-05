from PySide6.QtWidgets import QFrame, QVBoxLayout, QLayout, QLabel

from models.task import InvertTask
from widgets.horizontal_line import HorizontalLine


class InvertTaskFrame(QFrame):
    def __init__(self, task=None):
        super().__init__()

        if task and type(task) == InvertTask:
            self.task = task
        else:
            self.task = InvertTask()

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
