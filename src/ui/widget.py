from typing import Iterable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QComboBox, QLabel)


def make_button(parent: QWidget, text: str, width: int, x_pos: int, y_pos: int, action: callable) -> QPushButton:
    button = QPushButton(parent)
    button.setText(text)
    button.resize(width, 25)
    button.move(x_pos, y_pos)
    button.clicked.connect(action)
    return button


def make_combobox(parent: QWidget, items: Iterable, x_pos: int, y_pos: int, action: callable) -> QComboBox:
    combo_box = QComboBox(parent)
    combo_box.addItems(items)
    combo_box.resize(100, 25)
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
