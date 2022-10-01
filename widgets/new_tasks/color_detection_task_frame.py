from PySide6.QtWidgets import QFrame, QVBoxLayout, QCheckBox, QLayout, QLabel

from widgets.horizontal_line import HorizontalLine


class ColorDetectionTaskFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.description_label = QLabel()
        self.description_label.setText(
            "This task marks where the given color appears in \nthe image. Additionally, it can save the mask in .png \n"
            "format, shapefile file and geojson file.")

        self.color_detection_frame = QFrame()
        self.color_detection_box = QVBoxLayout()
        self.color_detection_box.setObjectName(u"color_detection_box")
        self.color_detection_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        # Save mask
        self.save_mask_checkbox = QCheckBox()
        self.save_mask_checkbox.setText('Save image mask')
        self.save_mask_checkbox.setChecked(False)
        # Save SHAPEFILE
        self.save_shp_checkbox = QCheckBox()
        self.save_shp_checkbox.setText('Save shapefile(.shp) file')
        self.save_shp_checkbox.setChecked(False)
        # Save GEOJSON
        self.save_geojson_checkbox = QCheckBox()
        self.save_geojson_checkbox.setText('Save geojson file')
        self.save_geojson_checkbox.setChecked(False)
        self.color_detection_box.addWidget(self.description_label)
        self.color_detection_box.addWidget(HorizontalLine())
        self.color_detection_box.addWidget(self.save_mask_checkbox)
        self.color_detection_box.addWidget(self.save_shp_checkbox)
        self.color_detection_box.addWidget(self.save_geojson_checkbox)
        self.setLayout(self.color_detection_box)
        self.hide()
