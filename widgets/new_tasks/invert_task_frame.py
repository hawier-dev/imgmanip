from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLayout


class InvertTaskFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.inverse_box = QVBoxLayout()
        self.inverse_box.setObjectName(u"inverse_box")
        self.inverse_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.setLayout(self.inverse_box)
        self.hide()
