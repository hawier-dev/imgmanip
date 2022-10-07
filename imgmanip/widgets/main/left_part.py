import os
import re
from datetime import datetime
from os.path import basename
from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS
from PySide6 import QtWidgets
from PySide6.QtGui import QCursor, Qt, QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QDialog, \
    QSizePolicy, QFileDialog
from natsort import natsorted

from dialogs.sort_images_dialog import SortImagesDialog
from functions.file_size import file_size
from models.sort import Sort


class LeftPart(QVBoxLayout):
    def __init__(self, root_widget):
        # Right part
        super().__init__()

        self.root_widget = root_widget
        # Default sort_type
        self.sort_type = Sort.UNSORTED

        self.list_of_images = []

        self.default_list_font = QFont()
        self.default_list_font.setPixelSize(13)

        smaller_font = QFont()
        smaller_font.setPixelSize(12)

        self.setObjectName(u"left_vbox")

        # "Images" text
        self.images_label = QLabel()
        self.images_label.setObjectName(u"images_label")
        self.images_label.setText('Images')
        # List of the images
        self.images_list = QListWidget()
        self.images_list.setObjectName(u"images_list")
        self.images_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.images_list.setStyleSheet(
            'QListView::item:selected{background-color: #99A2FF; color: #111111; font-weight: bold}')
        # self.images_list.itemSelectionChanged.connect(self.root_widget.preview_image)
        self.images_list.setFont(self.default_list_font)
        self.images_list.setMaximumWidth(300)
        self.images_list.installEventFilter(self)
        # Images count
        self.images_count_label = QLabel()
        self.images_count_label.setFont(smaller_font)
        self.images_count_label.setText(f'Images count: {len(self.list_of_images)}')
        # Properties of the image
        self.properties_list = QListWidget()
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
        self.add_images_button = QPushButton()
        self.add_images_button.setObjectName(u"add_images_button")
        self.add_images_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_images_button.setText('Add')
        self.add_images_button.clicked.connect(self.pick_files)
        # sort button
        self.sort_images_button = QPushButton()
        self.sort_images_button.setObjectName(u"sort_images_button")
        self.sort_images_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.sort_images_button.setText('Sort')
        self.sort_images_button.clicked.connect(self.pick_sort_type)
        # remove button
        self.remove_images_button = QPushButton()
        self.remove_images_button.setObjectName(u"remove_images_button")
        self.remove_images_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.remove_images_button.setText('Remove')
        self.remove_images_button.clicked.connect(self.remove_image)
        # adding buttons to h_layout
        self.images_buttons_h_box.addWidget(self.add_images_button)
        self.images_buttons_h_box.addWidget(self.sort_images_button)
        self.images_buttons_h_box.addWidget(self.remove_images_button)

        # Adding widgets to left part
        self.addWidget(self.images_label)
        self.addWidget(self.images_list)
        self.addWidget(self.images_count_label)
        self.addWidget(self.properties_list)
        self.addLayout(self.images_buttons_h_box)

    # Open file dialog
    def pick_files(self):
        file_dialog = QFileDialog()
        selected_files = file_dialog.getOpenFileNames(self.root_widget, 'Open files',
                                                      str(Path.home()),
                                                      'Image files (*.png *.jpg *.jpeg *.tif *.gif)', )
        selected_files = selected_files[0]

        if selected_files:
            for file in selected_files:
                if os.path.isfile(file):
                    if file not in self.list_of_images:
                        self.list_of_images.append(file)

        self.sort_images()
        self.images_count_label.setText(f'Images count: {len(self.list_of_images)}')

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
        mode_to_bpp = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32, 'CMYK': 32, 'YCbCr': 24, 'I': 32, 'F': 32}

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
        self.properties_list.addItem(f'Bit depth: {mode_to_bpp[image_mode]}')
        # EXIF
        for exif_tag in exif_tags:
            if exif_tag not in ignored_exif_list:
                pattern = re.compile(r'((?<=[^\W[A-Z])[A-Z]|(?<=\S)[A-Z](?=[a-z]))')
                exif_tag_split = pattern.sub(r' \1', str(exif_tag))
                self.properties_list.addItem(f'{exif_tag_split}: {exif_tags[exif_tag]}')

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
    def remove_image(self, remove_from_disk=False, item=None):
        # If item specified
        if item:
            index = self.images_list.row(item)
            self.images_list.takeItem(index)
            self.list_of_images.remove(item.text())
            if remove_from_disk:
                os.remove(item.text())
            try:
                self.images_list.setCurrentRow(index)
            except IndexError:
                pass

            if self.images_list.count() == 0:
                self.properties_list.clear()

            return

        # If item not specified
        for selected_image in self.images_list.selectedItems():
            index = self.images_list.row(selected_image)
            self.images_list.takeItem(index)
            self.list_of_images.remove(selected_image.text())
            if remove_from_disk:
                os.remove(selected_image.text())
            try:
                self.images_list.setCurrentRow(index)
            except IndexError:
                pass

            if self.images_list.count() == 0:
                self.properties_list.clear()

        self.images_count_label.setText(f'Images count: {len(self.list_of_images)}')
