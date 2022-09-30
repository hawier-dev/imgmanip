import os
import re
import sys
from datetime import datetime
from os.path import basename

import pyperclip
from PIL import Image
from PIL.ExifTags import TAGS
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import (QMetaObject, Qt)
from PySide6.QtGui import (QCursor, QPixmap, QFont, QAction)
from PySide6.QtWidgets import (QGridLayout, QHBoxLayout, QLabel,
                               QListWidget, QPushButton, QSizePolicy, QVBoxLayout, QWidget,
                               QProgressBar, QDialog, QCheckBox, QGraphicsView, QGraphicsPixmapItem,
                               QGraphicsScene, QMenu, QMenuBar)
from natsort import natsorted
from plyer import filechooser

from dialogs.confirm_dialog import ConfirmDialog
from dialogs.new_task_dialog import NewTaskDialog
from dialogs.rename_dialog import RenameDialog
from dialogs.sort_images_dialog import SortImagesDialog
from file_size import file_size
from functions.compress import compress_image
from functions.convert import convert_image
from functions.invert import invert_image
from functions.resize import resize_image
from models.sort import Sort
from models.task import TaskResize, TaskInvert, TaskConvert, TaskCompress
from models.image_extension import ImageExtension

Image.MAX_IMAGE_PIXELS = 933120000

platform_path = '/'
if sys.platform == 'win32':
    platform_path = '\\'


class UiMainWindow(QWidget):
    zoom = 1

    def __init__(self, main_window):
        # Main window
        super().__init__()
        if not main_window.objectName():
            main_window.setObjectName(u"MainWindow")
        main_window.resize(1000, 600)
        main_window.setWindowTitle('IMGManip')
        # main_window.setMaximumHeight(600)
        self.main_window = main_window

        # region ACTIONS
        # Creating FILE actions
        self.new_action = QAction("&New", self)
        self.exit_action = QAction("&Exit", self)
        self.exit_action.triggered.connect(self.exit_tool)
        # Creating EDIT actions
        self.fit_in_view_action = QAction("&Fit in view", self, checkable=True)
        self.fit_in_view_action.setChecked(True)
        # endregion

        self.create_menu_bar()

        # Default sort_type
        self.sort_type = Sort.UNSORTED

        self.list_of_tasks = []
        self.list_of_images = []

        self.default_list_font = QFont()
        self.default_list_font.setPixelSize(13)

        # Main central widget
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.gridLayout = QGridLayout(self.central_widget)
        self.gridLayout.setObjectName(u"gridLayout")

        # Horizontal layout split on 3 parts
        self.main_h_layout = QHBoxLayout()
        self.main_h_layout.setObjectName(u"main_h_layout")

        # Left part
        self.left_vbox = QVBoxLayout()
        self.left_vbox.setObjectName(u"left_vbox")
        # "Images" text
        self.images_label = QLabel(self.central_widget)
        self.images_label.setObjectName(u"images_label")
        self.images_label.setText('Images')
        # List of the images
        self.images_list = QListWidget(self.central_widget)
        self.images_list.setObjectName(u"images_list")
        self.images_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.images_list.setStyleSheet(
            'QListView::item:selected{background-color: #99A2FF; color: #111111; font-weight: bold}')
        self.images_list.itemSelectionChanged.connect(self.preview_image)
        self.images_list.setFont(self.default_list_font)
        self.images_list.setMaximumWidth(300)
        self.images_list.installEventFilter(self)
        # Properties of the image
        self.properties_list = QListWidget(self.central_widget)
        self.properties_list.setObjectName(u"properties_list")
        self.properties_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.properties_list.setStyleSheet(
            'QListView::item:selected{background-color: #99A2FF; color: #111111; font-weight: bold;}')
        self.properties_list.setFont(self.default_list_font)
        self.properties_list.setMaximumWidth(300)
        self.properties_list.installEventFilter(self)

        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.images_list.sizePolicy().hasHeightForWidth())
        self.images_list.setSizePolicy(size_policy)

        # Horizontal layout with add and remove button (IMAGES)
        self.images_buttons_h_box = QHBoxLayout()
        self.images_buttons_h_box.setObjectName(u"images_buttons_h_box")
        # add button
        self.add_images_button = QPushButton(self.central_widget)
        self.add_images_button.setObjectName(u"add_images_button")
        self.add_images_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_images_button.setText('Add')
        self.add_images_button.clicked.connect(self.pick_files)
        # sort button
        self.sort_images_button = QPushButton(self.central_widget)
        self.sort_images_button.setObjectName(u"sort_images_button")
        self.sort_images_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.sort_images_button.setText('Sort')
        self.sort_images_button.clicked.connect(self.pick_sort_type)
        # remove button
        self.remove_images_button = QPushButton(self.central_widget)
        self.remove_images_button.setObjectName(u"remove_images_button")
        self.remove_images_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.remove_images_button.setText('Remove')
        self.remove_images_button.clicked.connect(self.remove_image)
        # adding buttons to h_layout
        self.images_buttons_h_box.addWidget(self.add_images_button)
        self.images_buttons_h_box.addWidget(self.sort_images_button)
        self.images_buttons_h_box.addWidget(self.remove_images_button)

        # Adding widgets to left part
        self.left_vbox.addWidget(self.images_label)
        self.left_vbox.addWidget(self.images_list)
        self.left_vbox.addWidget(self.properties_list)
        self.left_vbox.addLayout(self.images_buttons_h_box)

        # Center part
        self.center_vbox = QVBoxLayout()
        self.center_vbox.setObjectName(u"left_vbox")

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
        self.start_button = QPushButton(self.central_widget)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_button.setText('Start')
        self.start_button.clicked.connect(self.start_tasks)
        self.start_button.setMaximumWidth(100)
        self.start_button.setStyleSheet("background-color: #99A2FF; color: #111111; font-weight: bold")

        # Fit in view button
        self.fit_in_view_button = QPushButton()
        self.fit_in_view_button.setText('Fit in view')
        self.fit_in_view_button.setMaximumWidth(100)
        self.fit_in_view_button.clicked.connect(self.fit_in_view)

        self.bottom_center_h_box.addWidget(self.fit_in_view_button, alignment=Qt.AlignLeft)
        self.bottom_center_h_box.addWidget(self.start_button)
        # self.center_vbox.addWidget(self.image_preview)
        self.center_vbox.addWidget(self.image_preview_view)
        self.center_vbox.addWidget(self.progress)
        self.center_vbox.addLayout(self.bottom_center_h_box)

        # Right part
        self.right_vbox = QVBoxLayout()
        self.right_vbox.setObjectName(u"right_vbox")

        # "Tasks" text
        self.tasks_label = QLabel(self.central_widget)
        self.tasks_label.setObjectName(u"tasks_label")
        self.tasks_label.setText('Tasks')

        # List of the created tasks
        self.tasks_list = QListWidget(self.central_widget)
        self.tasks_list.setObjectName(u"tasks_list")
        self.tasks_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tasks_list.setMaximumWidth(300)

        # Horizontal layout with add and remove button (TASKS)
        self.tasks_buttons_h_box = QHBoxLayout()
        self.tasks_buttons_h_box.setObjectName(u"tasks_buttons_h_box")
        # add button
        self.add_task_button = QPushButton(self.central_widget)
        self.add_task_button.setObjectName(u"add_task_button")
        self.add_task_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_task_button.setText("Add")
        self.add_task_button.clicked.connect(self.add_task)
        # Edit button
        self.edit_task_button = QPushButton(self.central_widget)
        self.edit_task_button.setObjectName(u"edit_task_button")
        self.edit_task_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.edit_task_button.setText("Edit")
        self.edit_task_button.clicked.connect(self.edit_task)
        # remove button
        self.remove_task_button = QPushButton(self.central_widget)
        self.remove_task_button.setObjectName(u"remove_task_button")
        self.remove_task_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.remove_task_button.setText("Remove")
        self.remove_task_button.clicked.connect(self.remove_task)
        # adding button to horizontal box
        self.tasks_buttons_h_box.addWidget(self.add_task_button)
        self.tasks_buttons_h_box.addWidget(self.edit_task_button)
        self.tasks_buttons_h_box.addWidget(self.remove_task_button)
        # Overwrite checkbox
        self.overwrite_checkbox = QCheckBox()
        self.overwrite_checkbox.setText('Overwrite')
        self.overwrite_checkbox.setChecked(False)
        # Adding widgets to right part
        self.right_vbox.addWidget(self.tasks_label)
        self.right_vbox.addWidget(self.tasks_list)
        self.right_vbox.addWidget(self.overwrite_checkbox)
        self.right_vbox.addLayout(self.tasks_buttons_h_box)

        # Adding parts to the main widget (main_h_layout)
        self.main_h_layout.addLayout(self.left_vbox)
        self.main_h_layout.addLayout(self.center_vbox)
        self.main_h_layout.addLayout(self.right_vbox)

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

    # Zooming event
    def wheel_event(self, event):
        if event.angleDelta().y() > 0:
            self.zoom = 1.2
        else:
            self.zoom = .8
        if event.modifiers() == Qt.CTRL:
            self.image_preview_view.scale(self.zoom, self.zoom)
        elif event.modifiers() == Qt.SHIFT:
            hor_scroll_value = self.image_preview_view.horizontalScrollBar().value() + -1 * event.angleDelta().y()
            self.image_preview_view.horizontalScrollBar().setValue(hor_scroll_value)
        else:
            ver_scroll_value = self.image_preview_view.verticalScrollBar().value() + -1 * event.angleDelta().y()
            self.image_preview_view.verticalScrollBar().setValue(ver_scroll_value)

    # Exit tool
    def exit_tool(self):
        sys.exit()

    # Fit in view image preview
    def fit_in_view(self):
        self.image_preview_view.fitInView(self.image_preview, Qt.KeepAspectRatio)

    # region Menus
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and
                source is self.images_list):

            # Menu for every item
            menu = QtWidgets.QMenu()
            menu.addAction('Rename')
            menu.addAction('Remove')
            menu.addAction('Remove from disk')

            action = menu.exec_(event.globalPos())
            if action:
                item = source.itemAt(event.pos())
                if item:
                    # RENAME IMAGE FILE
                    if action.toolTip() == 'Rename':
                        rename_dialog = RenameDialog(old_name=item.text())
                        if rename_dialog.exec_() == QDialog.Accepted:
                            new_name = rename_dialog.new_name_input.text()
                            self.list_of_images[self.list_of_images.index(item.text())] = new_name
                            os.rename(item.text(), new_name)
                            self.sort_images()
                            self.preview_image()
                        else:
                            rename_dialog.close()

                    # REMOVE IMAGE FROM LIST
                    elif action.toolTip() == 'Remove':
                        self.remove_image(False)

                    # REMOVE IMAGE FROM DISK
                    elif action.toolTip() == 'Remove from disk':
                        confirm_delete = ConfirmDialog(title='Remove file from disk', desc='Are you sure?')
                        if confirm_delete.exec_() == QDialog.Accepted:
                            self.remove_image(True)
                        else:
                            confirm_delete.close()
            return True

        if (event.type() == QtCore.QEvent.ContextMenu and
                source is self.properties_list):
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

    # endregion

    # Open file dialog
    def pick_files(self):
        selected_files = filechooser.open_file(multiple=True,
                                               filters=[('Image files', '*.png', '*.jpg', '*.jpeg', '*.tif')])
        if selected_files:
            for file in selected_files:
                if os.path.isfile(file):
                    if file not in self.list_of_images:
                        self.list_of_images.append(file)

        self.sort_images()

    # Display properties of the image
    def generate_image_properties(self, file_name):
        ignored_exif_list = [
            'ImageWidth',
            'ImageHeight',
            'TileOffsets',
            'TileByteCounts',
            'StripByteCounts',
            'StripOffsets',
        ]
        try:
            img = Image.open(file_name)
        except FileNotFoundError:
            return
        width, height = img.size
        file_base_name = basename(file_name)
        image_file_size = file_size(file_name)
        image_ext = img.format
        modification_time = os.path.getmtime(file_name)
        modification_time = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
        image_mode = img.mode

        exif_tags = {}

        for k, v in img.getexif().items():
            tag = TAGS.get(k)
            exif_tags[tag] = v

        self.properties_list.clear()
        self.properties_list.addItem(f'Filename: {file_base_name}')
        self.properties_list.addItem(f'File size: {image_file_size}')
        self.properties_list.addItem(f'Modified: {modification_time}')
        self.properties_list.addItem(f'Format: {image_ext}')
        self.properties_list.addItem(f'Width: {width}')
        self.properties_list.addItem(f'Height: {height}')
        self.properties_list.addItem(f'Mode: {image_mode}')
        # EXIF
        for exif_tag in exif_tags:
            if exif_tag not in ignored_exif_list:
                exif_tag_split = re.sub(r"(\w)([A-Z])", r"\1 \2", str(exif_tag))
                self.properties_list.addItem(f'{exif_tag_split}: {exif_tags[exif_tag]}')

    # Preview image
    def preview_image(self, file_name=None):
        if file_name:
            try:
                pix = QPixmap(file_name)
                self.generate_image_properties(file_name)
            except IndexError:
                pix = QPixmap(self.images_list.item(0).text())
                self.generate_image_properties(self.images_list.item(0).text())
        else:
            try:
                pix = QPixmap(self.images_list.selectedItems()[0].text())
                self.generate_image_properties(self.images_list.selectedItems()[0].text())
            except IndexError:
                pix = QPixmap(self.images_list.item(0).text())
                self.generate_image_properties(self.images_list.item(0).text())

        pix_size = pix.size()  # .toTuple()

        # if pix_size[0] > pix_size[1]:
        #     pix_size = QtCore.QSize(600, 600 * (pix_size[1] / pix_size[0]))
        # else:
        #     pix_size = QtCore.QSize(600 * (pix_size[0] / pix_size[1]), 600)

        self.image_preview.setPixmap(
            pix.scaled(pix_size)
        )

        if self.fit_in_view_action.isChecked():
            self.fit_in_view()

        self.image_preview_scene.setSceneRect(0, 0, pix_size.toTuple()[0],
                                              pix_size.toTuple()[1])

    # Dialog with sort type picker
    def pick_sort_type(self):
        new_task_dialog = SortImagesDialog(self.sort_type)
        if new_task_dialog.exec_() == QDialog.Accepted:
            if new_task_dialog.sort_picker.currentText() == 'unsorted':
                self.sort_type = Sort.UNSORTED
            elif new_task_dialog.sort_picker.currentText() == 'alphabetically':
                self.sort_type = Sort.ALPHABETICALLY
            elif new_task_dialog.sort_picker.currentText() == 'types':
                self.sort_type = Sort.TYPES
        else:
            pass

        self.sort_images()

    # Sorting images
    def sort_images(self):
        new_images_list = []
        if self.sort_type == Sort.UNSORTED:
            new_images_list = self.list_of_images
        elif self.sort_type == Sort.ALPHABETICALLY:
            new_images_list = self.list_of_images
            new_images_list = natsorted(new_images_list)

        self.images_list.clear()
        self.images_list.addItems(new_images_list)

    # Preview image
    def remove_image(self, remove_from_disk=False):
        for selected_image in self.images_list.selectedItems():
            index = self.images_list.row(selected_image)
            self.images_list.takeItem(self.images_list.row(selected_image))
            self.list_of_images.remove(selected_image.text())
            if remove_from_disk:
                os.remove(selected_image.text())
            try:
                self.images_list.setCurrentRow(index)
            except IndexError:
                self.image_preview.setText('Preview')

            if self.images_list.count() == 0:
                self.properties_list.clear()

    # Start tasks
    def start_tasks(self):
        self.start_button.setVisible(False)
        self.progress.setVisible(True)

        progress = 0
        images_list = [self.images_list.item(index).text() for index in range(self.images_list.count())]

        for index in range(len(images_list)):
            image = images_list[index]
            self.progress.setValue(progress)
            for task in self.list_of_tasks:
                # RESIZE TASK
                if type(task) == TaskResize:
                    file_name = resize_image(image, task, self.overwrite_checkbox.isChecked())
                    image = file_name
                # INVERT TASK
                elif type(task) == TaskInvert:
                    file_name = invert_image(image, task, self.overwrite_checkbox.isChecked())
                    image = file_name
                # CONVERT TASK
                elif type(task) == TaskConvert:
                    file_name = convert_image(image, task, self.overwrite_checkbox.isChecked())
                    image = file_name
                    if self.overwrite_checkbox.isChecked():
                        self.images_list.item(index).setText(file_name)
                        self.list_of_images[index] = file_name
                # COMPRESS TASK
                elif type(task) == TaskCompress:
                    file_name = compress_image(image, task, self.overwrite_checkbox.isChecked())
                    image = file_name

                self.images_list.setCurrentRow(index)
                self.preview_image(image)

            progress = (index / len(images_list)) * 100
            if progress > 55:
                self.progress.setStyleSheet('color: #111111')

        self.progress.setStyleSheet('color: white')
        self.progress.setVisible(False)
        self.start_button.setVisible(True)

    # Edit task
    def edit_task(self):
        if self.tasks_list.selectedIndexes():
            task_index = self.tasks_list.row(self.tasks_list.selectedItems()[0])
            edit_task_dialog = NewTaskDialog(
                self.list_of_tasks[task_index])
            if edit_task_dialog.exec_() == QDialog.Accepted:
                # RESIZE TASK
                if edit_task_dialog.task_picker.currentText() == 'resize':
                    self.list_of_tasks[task_index] = TaskResize(
                        new_width=edit_task_dialog.resize_width_input.text(),
                        new_height=edit_task_dialog.resize_height_input.text())

                # INVERT TASK
                elif edit_task_dialog.task_picker.currentText() == 'invert':
                    self.list_of_tasks[task_index] = TaskInvert()

                # CONVERT TASK
                elif edit_task_dialog.task_picker.currentText() == 'convert':
                    self.list_of_tasks[task_index] = TaskConvert(
                        convert_ext=ImageExtension(edit_task_dialog.extension_picker.currentText()))

                elif edit_task_dialog.task_picker.currentText() == 'compress':
                    self.list_of_tasks[task_index] = TaskCompress(
                        quality=edit_task_dialog.compress_quality_slider.value())

                self.tasks_list.currentItem().setText(edit_task_dialog.task_picker.currentText())

            else:
                pass

    # Add new task
    def add_task(self):
        new_task_dialog = NewTaskDialog()
        if new_task_dialog.exec_() == QDialog.Accepted:
            # RESIZE TASK
            if new_task_dialog.task_picker.currentText() == 'resize':
                self.list_of_tasks.append(TaskResize(
                    new_width=new_task_dialog.resize_width_input.text(),
                    new_height=new_task_dialog.resize_height_input.text()))
            # INVERT TASK
            elif new_task_dialog.task_picker.currentText() == 'invert':
                self.list_of_tasks.append(TaskInvert())
            # CONVERT TASK
            elif new_task_dialog.task_picker.currentText() == 'convert':
                self.list_of_tasks.append(
                    TaskConvert(convert_ext=ImageExtension(new_task_dialog.extension_picker.currentText())))
            # COMPRESS TASK
            elif new_task_dialog.task_picker.currentText() == 'compress':
                self.list_of_tasks.append(
                    TaskCompress(quality=new_task_dialog.compress_quality_slider.value()))

            self.tasks_list.addItem(new_task_dialog.task_picker.currentText())
        else:
            pass

    # Remove task
    def remove_task(self):
        for selected_task in self.tasks_list.selectedItems():
            index = self.tasks_list.row(selected_task)
            self.tasks_list.takeItem(self.tasks_list.row(selected_task))
            self.list_of_tasks.remove(self.list_of_tasks[self.tasks_list.row(selected_task)])
            try:
                self.tasks_list.setCurrentRow(index)
            except IndexError:
                pass
