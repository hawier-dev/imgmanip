from PySide6.QtCore import (QMetaObject, Qt)
from PySide6.QtWidgets import (QDialog, QDialogButtonBox,
                               QSizePolicy, QGridLayout, QVBoxLayout, QLayout, QLabel, QComboBox, QFrame)

from imgmanip.models.sort import Sort


class SortImagesDialog(QDialog):
    def __init__(self, sort_type: Sort):
        super().__init__()
        self.sort_type = sort_type

        if not self.objectName():
            self.setObjectName(u"self")

        self.setWindowTitle('Sort images')

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName(u"grid_layout")

        # Main layout
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.vertical_layout.setSizeConstraint(QLayout.SetDefaultConstraint)

        # Sort label
        self.sort_picker_frame = QFrame()
        self.sort_picker_box = QVBoxLayout()

        self.sort_label = QLabel(self)
        self.sort_label.setObjectName(u"sort_label")
        self.sort_label.setText("Sort")

        # Task input
        self.sort_picker = QComboBox(self)
        self.sort_picker.addItem("unsorted")
        self.sort_picker.addItem("alphabetically")
        self.sort_picker.addItem("types")
        self.sort_picker.setCurrentText(self.sort_type.value)
        self.sort_picker.setObjectName(u"sort_picker")

        self.sort_picker_box.addWidget(self.sort_label)
        self.sort_picker_box.addWidget(self.sort_picker)
        self.sort_picker_frame.setLayout(self.sort_picker_box)

        self.vertical_layout.addWidget(self.sort_picker_frame)
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

        QMetaObject.connectSlotsByName(self)
