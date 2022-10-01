from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLayout, QLabel, QHBoxLayout, QSlider


class CompressTaskFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.compress_box = QVBoxLayout()
        self.compress_box.setObjectName(u"compress_box")
        self.compress_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        # Label + slider box
        self.compress_quality_box = QHBoxLayout()
        # compress quality label
        self.compress_quality_label = QLabel()
        self.compress_quality_label.setText('Quality')
        # compress quality slider label
        self.compress_quality_value_label = QLabel()
        # compress quality slider
        self.compress_quality_slider = QSlider(Qt.Horizontal)
        self.compress_quality_slider.setMinimum(1)
        self.compress_quality_slider.setMaximum(100)
        self.compress_quality_slider.setValue(95)
        self.compress_quality_slider.setTickPosition(QSlider.TicksBelow)
        self.compress_quality_slider.setTickInterval(5)
        self.compress_quality_slider.valueChanged.connect(self.update_slider_value)
        self.compress_quality_value_label.setText(f'{self.compress_quality_slider.value()}%')
        self.compress_quality_value_label.setFixedWidth(50)

        self.compress_quality_box.addWidget(self.compress_quality_value_label)
        self.compress_quality_box.addWidget(self.compress_quality_slider)
        self.compress_box.addWidget(self.compress_quality_label)
        self.compress_box.addLayout(self.compress_quality_box)
        self.setLayout(self.compress_box)
        self.hide()

    # Compress slider value
    def update_slider_value(self):
        self.compress_quality_value_label.setText(f'{self.compress_quality_slider.value()}%')