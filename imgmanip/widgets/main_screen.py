import multiprocessing
import os
import sys
import time
from pathlib import Path

from imgmanip import config
from functools import partial
import webbrowser

import pyperclip
from PIL import Image
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import (QMetaObject, Qt)
from PySide6.QtGui import (QPixmap, QAction)
from PySide6.QtWidgets import (QGridLayout, QHBoxLayout, QWidget,
                               QDialog, QMenuBar, QFileDialog)

from imgmanip.dialogs.confirm_dialog import ConfirmDialog
from imgmanip.dialogs.info_dialog import InfoDialog
from imgmanip.dialogs.preferences_dialog import PreferencesDialog
from imgmanip.dialogs.rename_dialog import RenameDialog
from imgmanip.functions.create_time_str import create_time_str
from imgmanip.functions.run_tasks import run_task
from imgmanip.logs import save_images_names_to_txt
from imgmanip.models.save_type import SaveType
from imgmanip.widgets.main.center_part import CenterPart
from imgmanip.widgets.main.left_part import LeftPart
from imgmanip.widgets.main.right_part import RightPart

Image.MAX_IMAGE_PIXELS = 933120000
cpu_count = multiprocessing.cpu_count()

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
        self.config = config.read_config()

        # main_window.setMaximumHeight(600)
        self.main_window = main_window

        # Creating FILE actions
        self.preferences_action = QAction("&Preferences", self)
        self.preferences_action.triggered.connect(self.open_preferences)
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
        # self.left_part.images_list.itemClicked.connect(self.preview_image)
        self.left_part.images_list.itemActivated.connect(self.preview_image)
        self.left_part.properties_list.installEventFilter(self)

        self.center_part = CenterPart(self)
        self.right_part = RightPart(self)
        # Adding parts to the main widget (main_h_layout)
        self.main_h_layout.addLayout(self.left_part)
        self.main_h_layout.addLayout(self.center_part)
        self.main_h_layout.addLayout(self.right_part)

        self.gridLayout.addLayout(self.main_h_layout, 0, 0, 1, 1)

        main_window.setCentralWidget(self.central_widget)

        QMetaObject.connectSlotsByName(main_window)

    # Create menu bar
    def create_menu_bar(self):
        menu_bar = QMenuBar(self)
        # Creating menus
        file_menu = menu_bar.addMenu("&File")
        view_menu = menu_bar.addMenu("&View")

        file_menu.addAction(self.preferences_action)
        file_menu.addAction(self.exit_action)
        view_menu.addAction(self.fit_in_view_action)

        self.main_window.setMenuBar(menu_bar)

    # Open preferences dialog
    def open_preferences(self):
        preferences_dialog = PreferencesDialog(self.config)
        if preferences_dialog.exec_() == QDialog.Accepted:
            self.config = preferences_dialog.config
            config.write_config(preferences_dialog.config)
            self.left_part.sort_images()

    # Exit tool
    @staticmethod
    def exit_tool():
        sys.exit()

    # Menus on right click
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and
                source is self.left_part.images_list):

            # Menu for every item
            menu = QtWidgets.QMenu()
            menu.addAction('Copy path')
            menu.addAction('Open containing folder')
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
                    # OPEN CONTAINING FOLDER
                    elif action.toolTip() == 'Open containing folder':
                        webbrowser.open(os.path.dirname(item.text()))
                    # RENAME IMAGE FILE
                    elif action.toolTip() == 'Rename':
                        rename_dialog = RenameDialog(old_name=item.text())
                        if rename_dialog.exec_() == QDialog.Accepted:
                            new_name = rename_dialog.new_name_input.text()
                            self.left_part.list_of_images[self.left_part.list_of_images.index(item.text())] = new_name
                            os.rename(item.text(), new_name)
                            self.left_part.sort_images()
                            self.preview_image(self.left_part.images_list.findItems(new_name, Qt.MatchContains)[0])
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
    def preview_image(self, item):
        file_name = item.text()
        if file_name:
            try:
                pix = QPixmap(file_name)
                self.left_part.generate_image_properties(file_name)
            except IndexError or TypeError:
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
        start_time = time.time()

        # If no image added
        if not self.left_part.list_of_images:
            error_dialog = InfoDialog(title='Start tasks',
                                      text='You need to select at least one image.')
            if error_dialog.exec_() == QDialog.Accepted:
                return
        # If no task added
        if not self.right_part.list_of_tasks:
            error_dialog = InfoDialog(title='Start tasks',
                                      text='You need to select at least one task.')
            if error_dialog.exec_() == QDialog.Accepted:
                return

        # If no path selected
        if not os.path.exists(
                self.right_part.path_input.text()) \
                and \
                self.right_part.save_type_picker.currentText() == SaveType.SELECT_PATH.value:

            error_dialog = InfoDialog(title='Start tasks',
                                      text='You need to select valid path.')
            if error_dialog.exec_() == QDialog.Accepted:
                return
        # Overwrite warning
        if self.right_part.save_type_picker.currentText() == SaveType.OVERWRITE.value:
            confirm_delete = ConfirmDialog(title='Start tasks',
                                           desc='This process will overwrite all selected files!\nAre you sure?')
            if confirm_delete.exec_() == QDialog.Accepted:
                confirm_delete.close()
            else:
                confirm_delete.close()
                return
        self.center_part.start_button.setText('Stop')
        self.center_part.progress.setVisible(True)

        # try:
        #     self.left_part.images_list.setCurrentRow(0)
        #     self.preview_image(self.left_part.images_list.item(0).text())
        # except IndexError:
        #     pass

        images_list = [self.left_part.images_list.item(index).text() for index in
                       range(self.left_part.images_list.count())]

        # Multiprocessing
        pool = multiprocessing.Pool(processes=self.config['cpu_count'])
        run_func = partial(run_task, images_list=images_list,
                           list_of_tasks=self.right_part.list_of_tasks,
                           save_type=SaveType(self.right_part.save_type_picker.currentText()),
                           out_path=self.right_part.path_input.text())
        jobs = []
        job_count = 0
        images_count = len(images_list)
        for job in pool.imap_unordered(run_func, range(images_count)):
            jobs.append(job)
            job_count += 1
            progress = round((job_count / len(images_list)) * 100, 1)
            self.center_part.progress.setValue(progress)
            self.center_part.progress.setFormat(f'{progress}% {job_count}/{images_count}')

        pool.close()
        end_time = time.time()

        error_images = [ele for ele in jobs if ele is not None]
        if error_images:
            save_log_dialog = ConfirmDialog(title=f'Could not process {len(error_images)} files',
                                            desc=f"Could not process {len(error_images)} files. \n"
                                                 "Do you want to save a text file with the names of this files?")
            if save_log_dialog.exec_() == QDialog.Accepted:
                txt_file = QFileDialog.getSaveFileName(self, 'Save text file', str(Path.home()) + '/error-images.txt',
                                                       'Text file (*.txt)')
                if txt_file[0] != '':
                    save_images_names_to_txt(error_images, txt_file[0])

        self.center_part.progress.setStyleSheet('color: white')
        self.center_part.progress.setVisible(False)
        self.center_part.start_button.setText('Start')

        done_text = f'Done in:'
        done_text = create_time_str(done_text, end_time - start_time)

        time_dialog = InfoDialog(title='Done', text=done_text)
        time_dialog.exec()
