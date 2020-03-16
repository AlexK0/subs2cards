from typing import Iterable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QLabel, QLineEdit, QFileDialog, QMessageBox


def make_button(parent: QWidget, text: str, width: int, height: int, x_pos: int, y_pos: int, action: callable) -> QPushButton:
    button = QPushButton(parent)
    button.setText(text)
    button.resize(width, height)
    button.move(x_pos, y_pos)
    button.clicked.connect(action)
    return button


def make_combobox(parent: QWidget, items: Iterable, width: int, x_pos: int, y_pos: int, action: callable) -> QComboBox:
    combo_box = QComboBox(parent)
    combo_box.addItems(items)
    combo_box.resize(width, 25)
    combo_box.move(x_pos, y_pos)
    combo_box.activated[str].connect(action)
    return combo_box


def make_label(parent: QWidget,  width: int, high: int, x_pos: int, y_pos: int, font=None) -> QLabel:
    label = QLabel(parent)
    if font:
        label.setFont(font)
    label.setFixedSize(width, high)
    label.move(x_pos, y_pos)
    label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
    label.setTextInteractionFlags(Qt.TextSelectableByMouse)
    label.setWordWrap(True)
    return label


def show_open_dialog(parent: QWidget, label: str, extensions: str, line: QLineEdit) -> None:
    file_name = QFileDialog.getOpenFileName(parent, label, line.text() or "/", extensions + ";;Any (*.*)")[0]
    if file_name:
        line.setText(file_name)


def make_edit_line_with_button(parent: QWidget, label: str, extensions: str,
                               x: int, y: int, show_required_label=None) -> QLineEdit:
    line = QLineEdit(parent)
    line.resize(250, 25)
    line.move(x + 110 + 10, y)

    make_button(parent, label, 110, 25, x, y, lambda: show_open_dialog(parent, label, extensions, line))

    if show_required_label is not None:
        line_label = QLabel(parent)
        if show_required_label:
            line_label.setText("(Required)")
            line_label.setStyleSheet("color: red")
        else:
            line_label.setText("(Optional)")
            line_label.setStyleSheet("color: green")
        line_label.resize(60, 25)
        line_label.move(line.pos().x() + line.width() + 10, y)

    return line


def show_error(parent: QWidget, error_msg: str, exception: Exception) -> None:
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Warning)
    msg.setText(error_msg)
    msg.setDetailedText(str(exception))
    msg.setWindowTitle("Error")
    msg.exec_()
