from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QProgressBar, QHBoxLayout, QGraphicsPixmapItem, QGraphicsView, \
    QGraphicsScene


class CenterPart(QVBoxLayout):
    def __init__(self, root_widget):
        super().__init__()
        self.root_widget = root_widget

        self.setObjectName(u"left_vbox")

        # Image preview with scrolling, zooming
        self.image_preview_scene = QGraphicsScene()
        self.image_preview_view = QGraphicsView(self.image_preview_scene)
        self.image_preview_view.setMinimumSize(600, 600)
        # self.image_preview_view.setMaximumSize(1200, 800)
        # self.image_preview_view.contextMenuEvent = self.image_preview_menu
        self.image_preview_view.wheelEvent = self.wheel_event
        self.image_preview = QGraphicsPixmapItem()
        # self.image_preview.setPixmap(QPixmap.fromImage(QImage('assets/logo.png')))
        self.image_preview_scene.addItem(self.image_preview)
        self.image_preview_view.show()

        # ProgressBar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setVisible(False)

        # Bottom Horizontal box
        self.bottom_center_h_box = QHBoxLayout()
        self.bottom_center_h_box.setObjectName(u"bottom_center_h_box")
        # Start Button
        self.start_button = QPushButton()
        self.start_button.setObjectName(u"start_button")
        self.start_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_button.setText('Start')
        self.start_button.clicked.connect(self.root_widget.start_tasks)
        self.start_button.setMaximumWidth(100)
        self.start_button.setStyleSheet("background-color: #99A2FF; color: #111111; font-weight: bold")

        # Fit in view button
        self.fit_in_view_button = QPushButton()
        self.fit_in_view_button.setText('Fit in view')
        self.fit_in_view_button.setMaximumWidth(100)
        self.fit_in_view_button.clicked.connect(self.fit_in_view)

        self.bottom_center_h_box.addWidget(self.fit_in_view_button, alignment=Qt.AlignLeft)
        self.bottom_center_h_box.addWidget(self.start_button)
        # self.addWidget(self.image_preview)
        self.addWidget(self.image_preview_view)
        self.addWidget(self.progress)
        self.addLayout(self.bottom_center_h_box)

    # Zooming event
    def wheel_event(self, event):
        if event.angleDelta().y() > 0:
            zoom = 1.2
        else:
            zoom = .8
        if event.modifiers() == Qt.CTRL:
            self.image_preview_view.scale(zoom, zoom)
        elif event.modifiers() == Qt.SHIFT:
            hor_scroll_value = self.image_preview_view.horizontalScrollBar().value() + -1 * event.angleDelta().y()
            self.image_preview_view.horizontalScrollBar().setValue(hor_scroll_value)
        else:
            ver_scroll_value = self.image_preview_view.verticalScrollBar().value() + -1 * event.angleDelta().y()
            self.image_preview_view.verticalScrollBar().setValue(ver_scroll_value)

    # Fit in view image preview
    def fit_in_view(self):
        self.image_preview_view.fitInView(self.image_preview, Qt.KeepAspectRatio)
