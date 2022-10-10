from PySide6.QtWidgets import QFrame, QVBoxLayout, QCheckBox, QLayout, QLabel, QPushButton, QColorDialog

from imgmanip.models.task import ColorDetectionTask
from imgmanip.widgets.horizontal_line import HorizontalLine


class ColorDetectionTaskFrame(QFrame):
    def __init__(self, task=None):
        super().__init__()

        if task and type(task) == ColorDetectionTask:
            self.task = task
        else:
            self.task = ColorDetectionTask(save_mask=True)

        self.description_label = QLabel()
        self.description_label.setText(
            "This task marks where the given color appears in the image."
            "\n"
            "Additionally, it can save the mask in .png format, "
            "\n"
            "shapefile and geojson file."
        )

        self.color_detection_frame = QFrame()
        self.color_detection_box = QVBoxLayout()
        self.color_detection_box.setObjectName(u"color_detection_box")
        self.color_detection_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        # Color picker
        self.color_picker_button = QPushButton()
        self.color_picker_button.setText('Pick color')
        self.color_picker_button.clicked.connect(self.color_picker)

        if task and type(task) == ColorDetectionTask:
            if task.color:
                self.color_picker_button.setText(f'RGB: {task.color}')

        # Save mask
        self.save_mask_checkbox = QCheckBox()
        self.save_mask_checkbox.setText('Save image mask')
        self.save_mask_checkbox.setChecked(self.task.save_mask)
        self.save_mask_checkbox.stateChanged.connect(self.change_values)

        self.color_detection_box.addWidget(self.description_label)
        self.color_detection_box.addWidget(HorizontalLine())
        self.color_detection_box.addWidget(self.color_picker_button)
        self.color_detection_box.addWidget(self.save_mask_checkbox)
        self.setLayout(self.color_detection_box)
        self.hide()

    # Change values
    def change_values(self):
        self.task.save_mask = self.save_mask_checkbox.isChecked()

    # Pick color
    def color_picker(self):
        color = QColorDialog.getColor()
        selected_color = [color.getRgb()[0], color.getRgb()[1], color.getRgb()[2]]
        self.color_picker_button.setText(f'RGB: {selected_color}')
        self.task.color = selected_color
