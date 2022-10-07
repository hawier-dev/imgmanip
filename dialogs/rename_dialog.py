from PySide6.QtCore import (QMetaObject, Qt)
from PySide6.QtWidgets import (QDialog, QDialogButtonBox,
                               QSizePolicy, QGridLayout, QVBoxLayout, QLayout, QLineEdit)


class RenameDialog(QDialog):
    def __init__(self, old_name: str):
        super().__init__()
        if not self.objectName():
            self.setObjectName(u"self")

        self.setWindowTitle('Rename')
        self.resize(400, 50)

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName(u"grid_layout")

        # Main layout
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.vertical_layout.setSizeConstraint(QLayout.SetDefaultConstraint)

        # Error label
        self.new_name_input = QLineEdit()
        self.new_name_input.setText(old_name)
        self.vertical_layout.addWidget(self.new_name_input)

        self.button_box = QDialogButtonBox(self)
        self.button_box.setObjectName(u"button_box")
        size_policy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy3.setHorizontalStretch(0)
        size_policy3.setVerticalStretch(0)
        size_policy3.setHeightForWidth(self.button_box.sizePolicy().hasHeightForWidth())
        self.button_box.setSizePolicy(size_policy3)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        self.button_box.setCenterButtons(True)

        self.grid_layout.addLayout(self.vertical_layout, 0, 0, 1, 1)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.grid_layout.addWidget(self.button_box, 1, 0, 1, 1)
        QMetaObject.connectSlotsByName(self)
