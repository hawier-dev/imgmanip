from PySide6 import QtWidgets
from PySide6.QtGui import QCursor, Qt, QFont
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QCheckBox, QDialog

from dialogs.new_task_dialog import NewTaskDialog
from models.image_extension import ImageExtension
from models.task import ResizeTask, InvertTask, ConvertTask, CompressTask


class RightPart(QVBoxLayout):
    def __init__(self):
        # Right part

        super().__init__()
        self.list_of_tasks = []

        self.setObjectName(u"right_vbox")

        self.default_list_font = QFont()
        self.default_list_font.setPixelSize(13)

        # "Tasks" text
        self.tasks_label = QLabel()
        self.tasks_label.setObjectName(u"tasks_label")
        self.tasks_label.setText('Tasks')

        # List of the created tasks
        self.tasks_list = QListWidget()
        self.tasks_list.setObjectName(u"tasks_list")
        self.tasks_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tasks_list.setMaximumWidth(300)

        # Horizontal layout with add and remove button (TASKS)
        self.tasks_buttons_h_box = QHBoxLayout()
        self.tasks_buttons_h_box.setObjectName(u"tasks_buttons_h_box")
        # add button
        self.add_task_button = QPushButton()
        self.add_task_button.setObjectName(u"add_task_button")
        self.add_task_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_task_button.setText("Add")
        self.add_task_button.clicked.connect(self.add_task)
        # Edit button
        self.edit_task_button = QPushButton()
        self.edit_task_button.setObjectName(u"edit_task_button")
        self.edit_task_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.edit_task_button.setText("Edit")
        self.edit_task_button.clicked.connect(self.edit_task)
        # remove button
        self.remove_task_button = QPushButton()
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
        self.addWidget(self.tasks_label)
        self.addWidget(self.tasks_list)
        self.addWidget(self.overwrite_checkbox)
        self.addLayout(self.tasks_buttons_h_box)

    # Edit task
    def edit_task(self):
        if self.tasks_list.selectedIndexes():
            task_index = self.tasks_list.row(self.tasks_list.selectedItems()[0])
            edit_task_dialog = NewTaskDialog(
                self.list_of_tasks[task_index])
            if edit_task_dialog.exec_() == QDialog.Accepted:
                # RESIZE TASK
                if edit_task_dialog.task_picker.currentText() == 'resize':
                    self.list_of_tasks[task_index] = ResizeTask(
                        new_width=edit_task_dialog.tasks['resize'].resize_width_input.text(),
                        new_height=edit_task_dialog.tasks['resize'].resize_height_input.text())

                # INVERT TASK
                elif edit_task_dialog.task_picker.currentText() == 'invert':
                    self.list_of_tasks[task_index] = InvertTask()

                # CONVERT TASK
                elif edit_task_dialog.task_picker.currentText() == 'convert':
                    self.list_of_tasks[task_index] = ConvertTask(
                        convert_ext=ImageExtension(edit_task_dialog.tasks['convert'].extension_picker.currentText()))

                elif edit_task_dialog.task_picker.currentText() == 'compress':
                    self.list_of_tasks[task_index] = CompressTask(
                        quality=edit_task_dialog.tasks['compress'].compress_quality_slider.value())

                self.generate_list_of_tasks()

            else:
                pass

    # Add new task
    def add_task(self):
        new_task_dialog = NewTaskDialog()
        if new_task_dialog.exec_() == QDialog.Accepted:
            # RESIZE TASK
            if new_task_dialog.task_picker.currentText() == 'resize':
                self.list_of_tasks.append(ResizeTask(
                    new_width=new_task_dialog.tasks['resize'].resize_width_input.text(),
                    new_height=new_task_dialog.tasks['resize'].resize_height_input.text()))
            # INVERT TASK
            elif new_task_dialog.task_picker.currentText() == 'invert':
                self.list_of_tasks.append(InvertTask())
            # CONVERT TASK
            elif new_task_dialog.task_picker.currentText() == 'convert':
                self.list_of_tasks.append(
                    ConvertTask(
                        convert_ext=ImageExtension(new_task_dialog.tasks['convert'].extension_picker.currentText())))
            # COMPRESS TASK
            elif new_task_dialog.task_picker.currentText() == 'compress':
                self.list_of_tasks.append(
                    CompressTask(quality=new_task_dialog.tasks['compress'].compress_quality_slider.value()))

        else:
            pass

        self.generate_list_of_tasks()

    def generate_list_of_tasks(self):
        self.tasks_list.clear()
        for item in self.list_of_tasks:
            if type(item) == ResizeTask:
                self.tasks_list.addItem(f'Resize {item.new_width}x{item.new_height}')
            elif type(item) == InvertTask:
                self.tasks_list.addItem('Invert')
            elif type(item) == ConvertTask:
                self.tasks_list.addItem(f'Convert {item.convert_ext.value}')
            elif type(item) == CompressTask:
                self.tasks_list.addItem(f'Compress q: {item.quality}%')

    # Remove task
    def remove_task(self):
        for selected_task in self.tasks_list.selectedItems():
            index = self.tasks_list.row(selected_task)
            self.list_of_tasks.remove(self.list_of_tasks[self.tasks_list.row(selected_task)])
            self.generate_list_of_tasks()
            try:
                self.tasks_list.setCurrentRow(index)
            except IndexError:
                pass
