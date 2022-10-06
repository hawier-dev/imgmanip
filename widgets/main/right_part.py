from PySide6 import QtWidgets
from PySide6.QtGui import QCursor, Qt, QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QDialog, QComboBox, \
    QFrame, QLineEdit, QFileDialog

from dialogs.new_task_dialog import NewTaskDialog
from models.save_type import SaveType


class RightPart(QVBoxLayout):
    def __init__(self, root_widget):
        # Right part

        super().__init__()
        self.list_of_tasks = []

        self.setObjectName(u"right_vbox")
        self.root_widget = root_widget

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

        # Save type label
        self.save_path_label = QLabel()
        self.save_path_label.setText('Save path')

        # Save type picker
        self.save_type_picker = QComboBox()
        for save_type in SaveType:
            self.save_type_picker.addItem(save_type.value)
        self.save_type_picker.currentTextChanged.connect(self.change_save_type)

        self.path_select_box = QFrame()
        self.path_select_box.setMaximumWidth(300)
        self.path_select_h_box = QHBoxLayout()
        self.path_select_h_box.setContentsMargins(0, 0, 0, 0)
        self.path_input = QLineEdit()
        self.path_input.setObjectName(u"path_label")
        self.path_input.setText('None')

        self.path_pick_button = QPushButton()
        self.path_pick_button.setText('Select path')
        self.path_pick_button.clicked.connect(self.select_save_path)

        self.path_select_h_box.addWidget(self.path_input)
        self.path_select_h_box.addWidget(self.path_pick_button)
        self.path_select_box.setLayout(self.path_select_h_box)

        # Adding widgets to right part
        self.addWidget(self.tasks_label)
        self.addWidget(self.tasks_list)
        self.addWidget(self.save_path_label)
        self.addWidget(self.save_type_picker)
        self.addWidget(self.path_select_box)
        self.addLayout(self.tasks_buttons_h_box)

        self.change_save_type()

    # Save type
    def change_save_type(self):
        if self.save_type_picker.currentText() == SaveType.SELECT_PATH.value:
            self.path_select_box.show()
        else:
            self.path_select_box.hide()

    # Select path to save the image
    def select_save_path(self):
        select_save_path = QFileDialog.getExistingDirectory(self.root_widget, 'Open directory')
        self.path_input.setText(select_save_path)

    # Edit task
    def edit_task(self):
        if self.tasks_list.selectedIndexes():
            task_index = self.tasks_list.row(self.tasks_list.selectedItems()[0])
            edit_task_dialog = NewTaskDialog(
                self.list_of_tasks[task_index])
            if edit_task_dialog.exec_() == QDialog.Accepted:
                self.list_of_tasks[task_index] = edit_task_dialog.tasks[edit_task_dialog.task_picker.currentText()].task

                self.generate_list_of_tasks()

            else:
                pass

    # Add new task
    def add_task(self):
        new_task_dialog = NewTaskDialog()
        if new_task_dialog.exec_() == QDialog.Accepted:
            self.list_of_tasks.append(new_task_dialog.tasks[new_task_dialog.task_picker.currentText()].task)

        self.generate_list_of_tasks()

    def generate_list_of_tasks(self):
        self.tasks_list.clear()
        for item in self.list_of_tasks:
            self.tasks_list.addItem(item.name)

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
