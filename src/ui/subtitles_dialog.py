import os
import json
from typing import Set, Dict

from PyQt5.QtCore import QThreadPool, pyqtSlot, QVariant
from PyQt5.QtWidgets import QMainWindow, QStyle, QDialog, QWidget

from src.lang.token import Token
from src.lang.words_database import WordsDatabase

from src.ui.subtitles_processor import SubtitlesProcessor
from src.ui.settings_dialog import SettingsDialog, Settings
from src.ui.words_dialog import WordsDialog
from src.ui.widget import make_button, make_edit_line_with_button
from src.ui.word_card_dialog import WordCardDialog


class SubtitlesDialog(QDialog):
    def __init__(self, parent: QWidget, words_database: WordsDatabase):
        QDialog.__init__(self, parent)

        self.setFixedSize(460, 115)
        self.setWindowTitle("Subtitles")

        self._words_database = words_database
        self._en_subs_line = make_edit_line_with_button(self, 'Eng subtitles', 10, 10, True)
        self._native_subs_line = make_edit_line_with_button(self, 'Native subtitles', 10, 45, False)

        go_button_x = self._native_subs_line.pos().x() + self._native_subs_line.width() - 60
        self._go_button = make_button(self, "Go!", 60, 25, go_button_x, 80, self.start_subtitles_processing)
        exit_button_x = self._go_button.pos().x() + self._go_button.width() + 10
        make_button(self, "Exit", 60, 25, exit_button_x, 80, self.close)

        self._background_subtitle_processing = None

    def __del__(self):
        QThreadPool.globalInstance().waitForDone()

    def start_subtitles_processing(self) -> None:
        self._go_button.setText("Wait..")
        self._go_button.setDisabled(True)

        self._background_subtitle_processing = SubtitlesProcessor(
            en_subs_file=self._en_subs_line.text().strip(),
            native_subs_file=self._native_subs_line.text().strip(),
            parent=self
        )

        QThreadPool.globalInstance().start(self._background_subtitle_processing)

    @pyqtSlot(QVariant)
    def on_finish_processing(self, words: Dict[str, Token]) -> None:
        skip_list_window = WordsDialog(self, self._words_database, words)
        if skip_list_window.exec_():
            skip_list_window.save_current_state_to_words_database()
            self._words_database = skip_list_window.words_database
            words = {word: token for word, token in words.items() if not self._words_database.is_known_word(word)}
            if words:
                card_dialog = WordCardDialog(self, words, self._words_database)
                card_dialog.exec_()
                card_dialog.deleteLater()

        skip_list_window.deleteLater()

        self._go_button.setText("Go!")
        self._go_button.setDisabled(False)

