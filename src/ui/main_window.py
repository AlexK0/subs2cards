from typing import Set, Dict

from PyQt5.QtCore import QThreadPool, pyqtSlot, QVariant
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QLabel, QLineEdit, QMessageBox, QStyle
from qt5_t5darkstyle import darkstyle_css

from src.lang.token import CountedToken
from .subtitles_processor import SubtitlesProcessor
from .update_skip_list_dialog import UpdateSkipListDialog
from .nltk_data_updater import NLTKDataUpdater


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setStyleSheet(darkstyle_css())

        self.setFixedSize(460, 185)
        self.setWindowTitle("Awesome")

        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))

        self._en_subs_line = self._make_edit_line_with_button('Open en subtitles', 10, 10, True)
        self._native_subs_line = self._make_edit_line_with_button('Open native subtitles', 10, 45, False)
        self._skip_list = self._make_edit_line_with_button('Open skip list', 10, 80, False)
        self._tsv_base_file = self._make_edit_line_with_button('Save in tsv file', 10, 115, False)

        self._go_button = QPushButton(self)
        self._go_button.setText("Go!")
        self._go_button.resize(60, 25)
        self._go_button.move(self._tsv_base_file.pos().x() + self._tsv_base_file.width() - self._go_button.width(), 150)
        self._go_button.clicked.connect(self.start_subtitles_processing)

        self._nltk_data_update = QPushButton(self)
        self._nltk_data_update.setText("Update NLTK data")
        self._nltk_data_update.resize(120, 25)
        self._nltk_data_update.move(10, 150)
        self._nltk_data_update.clicked.connect(self.start_nltk_data_updating)

        self._background_nltk_uploading = None
        self._background_subtitle_processing = None
        self._progress_label = QLabel(self)
        self._progress_label.move(self._go_button.pos().x() + self._go_button.width() + 25, 145)
        self._progress_label.setText("0/0")

    def __del__(self):
        QThreadPool.globalInstance().waitForDone()

    def _make_edit_line_with_button(self, label: str, x: int, y: int, required: bool) -> QLineEdit:
        button = QPushButton(label, self)
        button.resize(120, 25)
        button.move(x, y)

        line = QLineEdit(self)
        line.resize(250, 25)
        line.move(button.pos().x() + button.width() + 10, y)

        button.clicked.connect(lambda: self.show_open_dialog(label, line))

        line_label = QLabel(self)
        if required:
            line_label.setText("(Required)")
            line_label.setStyleSheet("color: red")
        else:
            line_label.setText("(Optional)")
            line_label.setStyleSheet("color: green")
        line_label.resize(50, 25)
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

    @pyqtSlot(int, int)
    def on_finish_processing(self, words_from_tsv_base_count: int, total_words_count: int) -> None:
        msg = QMessageBox(self)
        msg.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Done")
        msg.setText(
            "Words in tsv before: %s\n"
            "Words in tsv after: %s"
            % (words_from_tsv_base_count, total_words_count))
        msg.show()

        self._go_button.setText("Go!")
        self._go_button.setDisabled(False)

    @pyqtSlot()
    def on_finish_nltk_data_updating(self) -> None:
        self._nltk_data_update.setText("Update NLTK data")
        self._nltk_data_update.setDisabled(False)

    @pyqtSlot(int, int)
    def on_processing_progress(self, current: int, total: int) -> None:
        self._progress_label.setText("%s/%s" % (current, total))

    @pyqtSlot(QVariant, QVariant, result=QVariant)
    def on_skip_list_update(self, ignored_words: Set[str], words: Dict[str, CountedToken]) -> Set[str]:
        skip_list_window = UpdateSkipListDialog(self, ignored_words, words)
        if skip_list_window.exec_():
            skip_list_window.save_current_state()

        ignored_words = ignored_words.difference(words)
        ignored_words.update(skip_list_window.ignored_words)

        skip_list_window.deleteLater()
        return ignored_words
