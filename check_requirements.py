import sys
import warnings
import ctypes
import pkg_resources
import tkinter as tk
from tkinter import messagebox

from PySide6.QtWidgets import QApplication

dependencies = [
    'pyside6',
    'numpy',
    'opencv-python',
    'pillow',
    'natsort',
    'pyqtdarktheme',
    'pyperclip',
]

error = ''
requirements_satisfied = True
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for dep in dependencies:
        try:
            pkg_resources.require(dep)
        except pkg_resources.DistributionNotFound as e:
            error += f'{e}\n'
            requirements_satisfied = False

if not requirements_satisfied:
    try:
        from dialogs.error_dialog import ErrorDialog

        app = QApplication(sys.argv)

        dialog = ErrorDialog(title='Dependency error', error=error)
        dialog.exec()
        app.exit(0)
    except:
        print(error)
    sys.exit(0)
