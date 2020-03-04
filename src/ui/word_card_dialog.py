from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPen, QColor, QPainter
from PyQt5.QtWidgets import QMainWindow, QDialog, QProgressBar

from src.lang.token import SharedTranslatedToken
from src.ui.widget import make_button, make_label
from src.ui.translate_dialog import TranslateDialog


class WordCardDialog(QDialog):
    def __init__(self, parent: QMainWindow, words: Dict[str, SharedTranslatedToken]):
        QDialog.__init__(self, parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Card")
        self.setFixedSize(400, 220)

        self._words_list = sorted(words.values(), key=lambda k: k.ref_counter, reverse=True)
        self._word_id = 0
        self.skip_list = set()

        self._word_label = make_label(self, 380, 35, 10, 5, QFont("Calibri", 20, QFont.Bold))

        self._frequency_bar = QProgressBar(self)
        self._frequency_bar.setFixedSize(100, 15)
        self._frequency_bar.move(150, 45)
        self._frequency_bar.setFormat("")
        self._frequency_bar.setRange(0, self._words_list[0].ref_counter)

        self._translation_label = make_label(self, 380, 20, 10, 65, QFont("Calibri", 10, QFont.Light))

        self._eng_example = make_label(self, 380, 30, 10, 95, QFont("Calibri", 10, QFont.Light))
        self._native_example = make_label(self, 380, 30, 10, 135, QFont("Calibri", 10, QFont.Light))
        self._counter = make_label(self, 100, 15, 150, 190)

        make_button(self, "Check", 50, 10, 185, self._open_translate_dialog)
        make_button(self, "Mark as known", 90, 70, 185, lambda: self._show_next(True))
        self._next_button = make_button(self, "Next", 50, 280, 185, self._show_next)
        make_button(self, "Exit", 50, 340, 185, self.reject)

        self._current_word = None
        self._show_next()

    def paintEvent(self, *args, **kwargs):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.lightGray, 2, Qt.SolidLine))
        painter.drawLine(20, 90, 380, 90)
        painter.setPen(QPen(Qt.lightGray, 1, Qt.SolidLine))
        painter.drawLine(20, 130, 380, 130)

    def _show_next(self, add_in_skip_list=False) -> None:
        if add_in_skip_list:
            self.skip_list.add(self._words_list[self._word_id - 1].token.word)

        if self._word_id == len(self._words_list):
            self.accept()
        else:
            self._current_word = self._words_list[self._word_id]
            self._frequency_bar.setValue(self._current_word.ref_counter)
            rate = self._current_word.ref_counter / self._words_list[0].ref_counter
            if rate >= 0.75:
                self._frequency_bar.setFormat("useful")
            elif rate >= 0.5:
                self._frequency_bar.setFormat("frequent")
            elif rate >= 0.25:
                self._frequency_bar.setFormat("normal")
            else:
                self._frequency_bar.setFormat("rare")

            self._word_label.setText(self._current_word.token.word)
            self._eng_example.setText(self._current_word.token.context_sentence_en)
            self._native_example.setText(self._current_word.token.context_sentence_native)
            self._update_translation()

            self._word_id += 1
            self._counter.setText("%s/%s" % (self._word_id, len(self._words_list)))
            if self._word_id == len(self._words_list):
                self._next_button.setText("Finish")

    def _open_translate_dialog(self) -> None:
        google_translate = TranslateDialog(self, self._current_word)
        if google_translate.exec_():
            self._current_word.native_translations = google_translate.get_translations()
            self._update_translation()

        google_translate.deleteLater()

    def _update_translation(self) -> None:
        self._next_button.setDisabled(not self._current_word.native_translations)
        if not self._current_word.native_translations:
            self._translation_label.setText("")
            self._translation_label.setToolTip("")
            return

        translations = "..."
        for i in reversed(range(len(self._current_word.native_translations) + 1)):
            translations = ", ".join(self._current_word.native_translations[0:i])
            if not translations:
                translations = "..."
            elif i != len(self._current_word.native_translations):
                translations = ", ".join((translations, "..."))
            width = self._translation_label.fontMetrics().boundingRect(translations).width()
            if width + 10 < self._translation_label.width():
                break

        self._translation_label.setText(translations)
        self._translation_label.setToolTip(", ".join(self._current_word.native_translations))
