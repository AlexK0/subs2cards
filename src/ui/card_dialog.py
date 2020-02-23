from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QDialog

from src.lang.token import CountedToken
from src.ui.widget import make_button, make_label, make_combobox
from src.ui.translate_dialog import TranslateDialog


class WordCardDialog(QDialog):
    def __init__(self, parent: QMainWindow, words: Dict[str, CountedToken]):
        QDialog.__init__(self, parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Card")
        self.setFixedSize(400, 155)

        self._words_list = sorted(words.values(), key=lambda k: k.ref_counter, reverse=True)
        self._word_id = 0
        self.skip_list = set()

        self._word_label = make_label(self, 380, 30, 10, 5, QFont("Calibri", 20, QFont.Bold))
        self._eng_example = make_label(self, 380, 30, 10, 45, QFont("Calibri", 10, QFont.Light))
        self._native_example = make_label(self, 380, 30, 10, 80, QFont("Calibri", 10, QFont.Light))
        self._counter = make_label(self, 100, 15, 150, 125)

        self._show_next()

        self._stop_button = make_button(self, "Check", 50, 10, 120, self._show_google_translate)
        self._ignore_word = make_button(self, "Mark as known", 90, 70, 120, lambda: self._show_next(True))
        self._next_button = make_button(self, "Next", 50, 280, 120, self._show_next)
        self._stop_button = make_button(self, "Exit", 50, 340, 120, self.reject)

    def _show_next(self, add_in_skip_list=False) -> None:
        if add_in_skip_list:
            self.skip_list.add(self._words_list[self._word_id - 1].token.word)
        if self._word_id == len(self._words_list):
            self.accept()
        else:
            counted_token = self._words_list[self._word_id]
            self._word_label.setText(counted_token.token.word)
            self._eng_example.setText(counted_token.token.context_sentence_en)
            self._native_example.setText(counted_token.token.context_sentence_native)

            self._word_id += 1
            self._counter.setText("%s/%s" % (self._word_id, len(self._words_list)))
            if self._word_id == len(self._words_list):
                self._next_button.setText("Finish")

    def _show_google_translate(self) -> None:
        google_translate = TranslateDialog(self, self._word_label.text())
        google_translate.exec_()
