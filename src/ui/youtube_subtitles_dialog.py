from typing import Dict
import re

from PyQt5.QtCore import QThreadPool, pyqtSlot, QVariant
from PyQt5.QtWidgets import QDialog, QWidget, QLineEdit, QMessageBox

from src.lang.token import Token
from src.lang.words_database import WordsDatabase
from src.lang.subs2tokens import get_tokens_from_youtube

from src.ui.words_dialog import show_words_dialog
from src.ui.widget import make_button
from src.ui.tokens_processor import TokensProcessor


class YoutubeSubtitlesDialog(QDialog):

    _URL_REGEX = re.compile(r"^https?://www\.youtube\.com/watch\?v=([a-zA-Z0-9_\-]+)$")

    def __init__(self, parent: QWidget, words_database: WordsDatabase):
        QDialog.__init__(self, parent)

        self.setFixedSize(460, 80)
        self.setWindowTitle("Youtube subtitles")

        self._words_database = words_database

        self._youtube_video_url_line = QLineEdit(self)
        self._youtube_video_url_line.resize(440, 25)
        self._youtube_video_url_line.move(10, 10)
        self._youtube_video_url_line.setPlaceholderText("Youtube video url..")
        self._youtube_video_url_line.setToolTip("Enter youtube url like https://www.youtube.com/watch?v=abcdefg")
        self._youtube_video_url_line.textChanged.connect(self._on_url_changed)
        self._youtube_video_id = ""

        go_button_x = self._youtube_video_url_line.pos().x() + self._youtube_video_url_line.width() - 130
        self._go_button = make_button(self, "Go!", 60, 25, go_button_x, 45, self.start_subtitles_processing)
        exit_button_x = self._go_button.pos().x() + self._go_button.width() + 10
        make_button(self, "Exit", 60, 25, exit_button_x, 45, self.close)

        self._go_button.setDisabled(True)

        self._background = None

    def __del__(self):
        QThreadPool.globalInstance().waitForDone()

    def _on_url_changed(self):
        url = self._youtube_video_url_line.text()
        match = self._URL_REGEX.match(url)
        self._youtube_video_id = match.groups()[0] if match else ""
        self._go_button.setDisabled(not self._youtube_video_id)

    def start_subtitles_processing(self) -> None:
        self._go_button.setText("Wait..")
        self._go_button.setDisabled(True)
        self._youtube_video_url_line.setDisabled(True)

        self._background = TokensProcessor(lambda: get_tokens_from_youtube(self._youtube_video_id), self)
        QThreadPool.globalInstance().start(self._background)

    @pyqtSlot(QVariant, str)
    def on_finish_processing(self, words: Dict[str, Token], exception: str) -> None:
        if exception:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Can't load youtube subtitles :(   ")
            msg.setDetailedText(exception)
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            self._words_database = show_words_dialog(self, self._words_database, words)
        self._go_button.setText("Go!")
        self._go_button.setDisabled(False)
        self._youtube_video_url_line.setDisabled(False)
