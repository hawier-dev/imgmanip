from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout, QLineEdit, QLayout


class ResizeTaskFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.resize_box = QVBoxLayout()
        self.resize_box.setObjectName(u"resize_box")
        self.resize_box.setSizeConstraint(QLayout.SetDefaultConstraint)

        # Name label
        self.resize_label = QLabel(self)
        self.resize_label.setObjectName(u"name_label")
        size_policy_resize_label = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy_resize_label.setHorizontalStretch(0)
        size_policy_resize_label.setVerticalStretch(0)
        size_policy_resize_label.setHeightForWidth(self.resize_label.sizePolicy().hasHeightForWidth())
        self.resize_label.setSizePolicy(size_policy_resize_label)
        self.resize_label.setText("New size")

        # Resize inputs
        self.resize_inputs_h_box = QHBoxLayout()
        self.resize_width_input = QLineEdit(self)
        self.resize_width_input.setObjectName(u"resize_width_input")

        # X label between width and height -> width x height
        self.x_label = QLabel(self)
        self.x_label.setObjectName(u"name_label")
        self.x_label.setText('x')

        self.resize_height_input = QLineEdit(self)
        self.resize_height_input.setObjectName(u"resize_height_input")

        # size_policy_resize_input = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # size_policy_resize_input.setHorizontalStretch(0)
        # size_policy_resize_input.setVerticalStretch(0)
        # size_policy_resize_input.setHeightForWidth(self.resize_width_input.sizePolicy().hasHeightForWidth())
        # self.resize_width_input.setSizePolicy(size_policy_resize_input)
        self.resize_inputs_h_box.addWidget(self.resize_width_input)
        self.resize_inputs_h_box.addWidget(self.x_label)
        self.resize_inputs_h_box.addWidget(self.resize_height_input)
        self.resize_box.addWidget(self.resize_label)
        self.resize_box.addLayout(self.resize_inputs_h_box)

        self.setLayout(self.resize_box)
        self.hide()
