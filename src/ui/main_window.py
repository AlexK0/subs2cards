from typing import Set, Dict

from PyQt5.QtCore import QThreadPool, pyqtSlot, QVariant
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QLineEdit, QStyle
from qt5_t5darkstyle import darkstyle_css

from src.lang.token import SharedTranslatedToken
from src.ui.subtitles_processor import SubtitlesProcessor
from src.ui.words_dialog import WordsDialog
from src.ui.nltk_data_updater import NLTKDataUpdater
from src.ui.widget import make_button
from src.ui.word_card_dialog import WordCardDialog


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setStyleSheet(darkstyle_css())

        self.setFixedSize(460, 185)
        self.setWindowTitle("subs2cards")

        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))

        self._en_subs_line = self._make_edit_line_with_button('Eng subtitles', 10, 10, True)
        self._native_subs_line = self._make_edit_line_with_button('Native subtitles', 10, 45, False)
        self._skip_list = self._make_edit_line_with_button('Known words', 10, 80, False)
        self._tsv_base_file = self._make_edit_line_with_button('Save as tsv', 10, 115, False)

        go_button_x = self._tsv_base_file.pos().x() + self._tsv_base_file.width() - 60
        self._go_button = make_button(self, "Go!", 60, go_button_x, 150, self.start_subtitles_processing)
        exit_button_x = self._go_button.pos().x() + self._go_button.width() + 10
        self._exit = make_button(self, "Exit", 60, exit_button_x, 150, self.close)
        self._nltk_data_update = make_button(self, "Update NLTK", 110, 10, 150, self.start_nltk_data_updating)

        self._background_nltk_uploading = None
        self._background_subtitle_processing = None

    def __del__(self):
        QThreadPool.globalInstance().waitForDone()

    def _make_edit_line_with_button(self, label: str, x: int, y: int, required: bool) -> QLineEdit:
        line = QLineEdit(self)
        line.resize(250, 25)
        line.move(x + 110 + 10, y)
        make_button(self, label, 110, x, y, lambda: self.show_open_dialog(label, line))

        line_label = QLabel(self)
        if required:
            line_label.setText("(Required)")
            line_label.setStyleSheet("color: red")
        else:
            line_label.setText("(Optional)")
            line_label.setStyleSheet("color: green")
        line_label.resize(60, 25)
        line_label.move(line.pos().x() + line.width() + 10, y)

        return line

    def show_open_dialog(self, label: str, line: QLineEdit) -> None:
        file_name = QFileDialog.getOpenFileName(self, label)[0]
        if file_name:
            line.setText(file_name)

    def start_subtitles_processing(self) -> None:
        self._go_button.setText("Wait..")
        self._go_button.setDisabled(True)

        self._background_subtitle_processing = SubtitlesProcessor(
            skip_list_file=self._skip_list.text().strip(),
            en_subs_file=self._en_subs_line.text().strip(),
            native_subs_file=self._native_subs_line.text().strip(),
            tsv_base_file=self._tsv_base_file.text().strip(),
            main_window=self
        )

        QThreadPool.globalInstance().start(self._background_subtitle_processing)

    def start_nltk_data_updating(self) -> None:
        self._nltk_data_update.setText("Wait..")
        self._nltk_data_update.setDisabled(True)

        self._background_nltk_uploading = NLTKDataUpdater(self)
        QThreadPool.globalInstance().start(self._background_nltk_uploading)

    @pyqtSlot()
    def on_finish_processing(self) -> None:
        self._go_button.setText("Go!")
        self._go_button.setDisabled(False)

    @pyqtSlot()
    def on_finish_nltk_data_updating(self) -> None:
        self._nltk_data_update.setText("Update NLTK")
        self._nltk_data_update.setDisabled(False)

    @pyqtSlot(QVariant, QVariant, result=QVariant)
    def on_word_list_show(self, ignored_words: Set[str], words: Dict[str, SharedTranslatedToken]) -> Set[str]:
        skip_list_window = WordsDialog(self, ignored_words, words)
        show_cards = False
        if skip_list_window.exec_():
            show_cards = True
            skip_list_window.save_current_state()

        ignored_words = ignored_words.difference(words)
        ignored_words.update(skip_list_window.ignored_words)

        if show_cards:
            words = {word: token for word, token in words.items() if word not in ignored_words}
            if words:
                card_dialog = WordCardDialog(self, words)
                card_dialog.exec_()
                ignored_words.update(card_dialog.skip_list)
                card_dialog.deleteLater()

        skip_list_window.deleteLater()
        return ignored_words
