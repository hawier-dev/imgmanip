import multiprocessing

from PySide6.QtCore import (QMetaObject, Qt)
from PySide6.QtGui import QIntValidator, QFont
from PySide6.QtWidgets import (QDialog, QDialogButtonBox,
                               QSizePolicy, QGridLayout, QVBoxLayout, QLayout, QLabel, QLineEdit, QCheckBox)


class PreferencesDialog(QDialog):
    def __init__(self, config):
        super().__init__()
        if not self.objectName():
            self.setObjectName(u"self")

        self.config = config
        self.cpu_count_max = multiprocessing.cpu_count() - 1
        self.setWindowTitle('Preferences')

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName(u"grid_layout")

        # Main layout
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.vertical_layout.setSizeConstraint(QLayout.SetDefaultConstraint)

        int_validator = QIntValidator()
        smaller_font = QFont()
        smaller_font.setPixelSize(12)

        self.cpu_count_label = QLabel()
        self.cpu_count_label.setText('CPU threads')
        self.cpu_max_label = QLabel()
        self.cpu_max_label.setText(f'max: {self.cpu_count_max}')
        self.cpu_max_label.setFont(smaller_font)
        self.cpu_count_input = QLineEdit(self)
        self.cpu_count_input.setObjectName(u"cpu_count")
        self.cpu_count_input.setText(str(self.config['cpu_count']))
        self.cpu_count_input.textChanged.connect(self.value_changed)
        self.cpu_count_input.setValidator(int_validator)

        self.vertical_layout.addWidget(self.cpu_count_label)
        self.vertical_layout.addWidget(self.cpu_count_input)
        self.vertical_layout.addWidget(self.cpu_max_label)

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
        self.setFixedSize(self.sizeHint())

        QMetaObject.connectSlotsByName(self)

    # Update config values
    def value_changed(self):
        try:
            cpu_count = int(self.cpu_count_input.text().strip())
            if cpu_count > self.cpu_count_max:
                self.cpu_count_input.setText(str(self.config['cpu_count']))
            else:
                self.config['cpu_count'] = int(self.cpu_count_input.text().strip())

        except ValueError:
            pass
