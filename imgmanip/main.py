import os
import sys

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication

from widgets.main_screen import UiMainWindow
import qdarktheme

os.environ['QT_IMAGEIO_MAXALLOC'] = "10000000000000000000000000000000000000000000000000000000000000000"
QtGui.QImageReader.setAllocationLimit(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMouseTracking(True)
        self.ui = UiMainWindow(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    app.setAttribute(Qt.AA_DontUseNativeDialogs)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
