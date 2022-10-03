import os
import sys

import pyperclip
from PIL import Image
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import (QMetaObject)
from PySide6.QtGui import (QPixmap, QAction)
from PySide6.QtWidgets import (QGridLayout, QHBoxLayout, QWidget,
                               QDialog, QMenuBar)

from dialogs.confirm_dialog import ConfirmDialog
from dialogs.error_dialog import ErrorDialog
from dialogs.rename_dialog import RenameDialog
from functions.color_detection import detect_color
from functions.compress import compress_image
from functions.convert import convert_image
from functions.flip import flip_image
from functions.invert import invert_image
from functions.resize import resize_image
from models.task import ResizeTask, InvertTask, ConvertTask, CompressTask, ColorDetectionTask, FlipTask
from widgets.main.center_part import CenterPart
from widgets.main.left_part import LeftPart
from widgets.main.right_part import RightPart

Image.MAX_IMAGE_PIXELS = 933120000

platform_path = '/'
if sys.platform == 'win32':
    platform_path = '\\'


class UiMainWindow(QWidget):
    def __init__(self, main_window):
        # Main window
        super().__init__()
        if not main_window.objectName():
            main_window.setObjectName(u"MainWindow")
        main_window.resize(1000, 600)
        main_window.setWindowTitle('IMGManip')
        # main_window.setMaximumHeight(600)
        self.main_window = main_window

        # Creating FILE actions
        self.new_action = QAction("&New", self)
        self.exit_action = QAction("&Exit", self)
        self.exit_action.triggered.connect(self.exit_tool)
        # Creating EDIT actions
        self.fit_in_view_action = QAction("&Fit in view", self, checkable=True)
        self.fit_in_view_action.setChecked(True)

        self.create_menu_bar()

        # Main central widget
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.gridLayout = QGridLayout(self.central_widget)
        self.gridLayout.setObjectName(u"gridLayout")

        # Horizontal layout split on 3 parts
        self.main_h_layout = QHBoxLayout()
        self.main_h_layout.setObjectName(u"main_h_layout")

        self.left_part = LeftPart(self)
        self.left_part.images_list.installEventFilter(self)
        self.left_part.properties_list.installEventFilter(self)

        self.center_part = CenterPart(self)
        self.right_part = RightPart()
        # Adding parts to the main widget (main_h_layout)
        self.main_h_layout.addLayout(self.left_part)
        self.main_h_layout.addLayout(self.center_part)
        self.main_h_layout.addLayout(self.right_part)

        self.gridLayout.addLayout(self.main_h_layout, 0, 0, 1, 1)

        main_window.setCentralWidget(self.central_widget)

        QMetaObject.connectSlotsByName(main_window)

    def create_menu_bar(self):
        menu_bar = QMenuBar(self)
        # Creating menus
        file_menu = menu_bar.addMenu("&File")
        view_menu = menu_bar.addMenu("&View")

        file_menu.addAction(self.new_action)
        file_menu.addAction(self.exit_action)
        view_menu.addAction(self.fit_in_view_action)

        self.main_window.setMenuBar(menu_bar)

    # Exit tool
    def exit_tool(self):
        sys.exit()

    # Menus on right click
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and
                source is self.left_part.images_list):

            # Menu for every item
            menu = QtWidgets.QMenu()
            menu.addAction('Copy path')
            menu.addAction('Rename')
            menu.addAction('Remove')
            menu.addAction('Remove from disk')

            action = menu.exec_(event.globalPos())
            if action:
                item = source.itemAt(event.pos())
                if item:
                    # COPY PATH
                    if action.toolTip() == 'Copy path':
                        pyperclip.copy(item.text())
                    # RENAME IMAGE FILE
                    elif action.toolTip() == 'Rename':
                        rename_dialog = RenameDialog(old_name=item.text())
                        if rename_dialog.exec_() == QDialog.Accepted:
                            new_name = rename_dialog.new_name_input.text()
                            self.left_part.list_of_images[self.left_part.list_of_images.index(item.text())] = new_name
                            os.rename(item.text(), new_name)
                            self.left_part.sort_images()
                            self.preview_image()
                        else:
                            rename_dialog.close()

                    # REMOVE IMAGE FROM LIST
                    elif action.toolTip() == 'Remove':
                        self.left_part.remove_image(False, item)

                    # REMOVE IMAGE FROM DISK
                    elif action.toolTip() == 'Remove from disk':
                        confirm_delete = ConfirmDialog(title='Remove file from disk', desc='Are you sure?')
                        if confirm_delete.exec_() == QDialog.Accepted:
                            self.left_part.remove_image(True, item)
                        else:
                            confirm_delete.close()
            return True

        if (event.type() == QtCore.QEvent.ContextMenu and
                source is self.left_part.properties_list):
            # Menu for every item
            menu = QtWidgets.QMenu()
            menu.addAction('Copy')
            menu.addAction('Copy value')
            menu.addAction('Copy property name')

            action = menu.exec_(event.globalPos())
            if action:
                item = source.itemAt(event.pos())
                if action.toolTip() == "Copy":
                    pyperclip.copy(item.text())
                elif action.toolTip() == "Copy value":
                    pyperclip.copy(item.text().split(': ')[-1])
                elif action.toolTip() == "Copy property name":
                    pyperclip.copy(item.text().split(': ')[0])

        return super(UiMainWindow, self).eventFilter(source, event)

    # Preview image
    def preview_image(self, file_name=None):
        if file_name:
            try:
                pix = QPixmap(file_name)
                self.left_part.generate_image_properties(file_name)
            except IndexError:
                pix = QPixmap(self.left_part.images_list.item(0).text())
                self.left_part.generate_image_properties(self.left_part.images_list.item(0).text())
        else:
            try:
                pix = QPixmap(self.left_part.images_list.selectedItems()[0].text())
                self.left_part.generate_image_properties(self.left_part.images_list.selectedItems()[0].text())
            except IndexError:
                pix = QPixmap(self.left_part.images_list.item(0).text())
                self.left_part.generate_image_properties(self.left_part.images_list.item(0).text())

        pix_size = pix.size()

        self.center_part.image_preview.setPixmap(
            pix.scaled(pix_size)
        )

        if self.fit_in_view_action.isChecked():
            self.center_part.fit_in_view()

        self.center_part.image_preview_scene.setSceneRect(0, 0, pix_size.toTuple()[0],
                                                          pix_size.toTuple()[1])

    # Start tasks
    def start_tasks(self):
        # If no image added
        if not self.left_part.list_of_images:
            error_dialog = ErrorDialog(title='Start tasks',
                                       error='You need to select at least one image.')
            if error_dialog.exec_() == QDialog.Accepted:
                return
        # If no task added
        if not self.right_part.list_of_tasks:
            error_dialog = ErrorDialog(title='Start tasks',
                                       error='You need to select at least one task.')
            if error_dialog.exec_() == QDialog.Accepted:
                return

        # Overwrite warning
        if self.right_part.overwrite_checkbox.isChecked():
            confirm_delete = ConfirmDialog(title='Start tasks',
                                           desc='This process will overwrite all selected files!\nAre you sure?')
            if confirm_delete.exec_() == QDialog.Accepted:
                confirm_delete.close()
            else:
                confirm_delete.close()
                return
        self.center_part.start_button.setVisible(False)
        self.center_part.progress.setVisible(True)

        try:
            self.left_part.images_list.setCurrentRow(0)
            self.preview_image(self.left_part.images_list.item(0).text())
        except IndexError:
            pass

        progress = 0
        images_list = [self.left_part.images_list.item(index).text() for index in
                       range(self.left_part.images_list.count())]

        for index in range(len(images_list)):
            image = images_list[index]
            self.center_part.progress.setValue(progress)
            for task in self.right_part.list_of_tasks:
                # RESIZE TASK
                if type(task) == ResizeTask:
                    file_name = resize_image(image, task, self.right_part.overwrite_checkbox.isChecked())
                    image = file_name
                # INVERT TASK
                elif type(task) == InvertTask:
                    file_name = invert_image(image, task, self.right_part.overwrite_checkbox.isChecked())
                    image = file_name
                # FLIP TASK
                elif type(task) == FlipTask:
                    file_name = flip_image(image, task, self.right_part.overwrite_checkbox.isChecked())
                    image = file_name
                # CONVERT TASK
                elif type(task) == ConvertTask:
                    file_name = convert_image(image, task, self.right_part.overwrite_checkbox.isChecked())
                    image = file_name
                    if self.right_part.overwrite_checkbox.isChecked():
                        self.left_part.images_list.item(index).setText(file_name)
                        self.left_part.list_of_images[index] = file_name
                # COMPRESS TASK
                elif type(task) == CompressTask:
                    file_name = compress_image(image, task, self.right_part.overwrite_checkbox.isChecked())
                    image = file_name
                # COLOR DETECTION TASK
                elif type(task) == ColorDetectionTask:
                    file_name = detect_color(image, task, self.right_part.overwrite_checkbox.isChecked())
                    image = file_name

                self.left_part.images_list.setCurrentRow(index)
                self.preview_image(image)

            progress = (index / len(images_list)) * 100
            if progress > 55:
                self.center_part.progress.setStyleSheet('color: #111111')

        self.center_part.progress.setStyleSheet('color: white')
        self.center_part.progress.setVisible(False)
        self.center_part.start_button.setVisible(True)
