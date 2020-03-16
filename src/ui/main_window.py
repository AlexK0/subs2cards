import os

from PyQt5.QtWidgets import QMainWindow, QStyle
from qt5_t5darkstyle import darkstyle_css

from src.lang.words_database import WordsDatabase

from src.ui.settings_dialog import SettingsDialog, Settings
from src.ui.widget import make_button
from src.ui.subtitles_dialog import SubtitlesDialog
from src.ui.document_dialog import DocumentDialog
from src.ui.youtube_subtitles_dialog import YoutubeSubtitlesDialog


class MainWindow(QMainWindow):
    _SETTINGS_FILE = "settings.json"

    def __init__(self):
        QMainWindow.__init__(self)
        self._settings = Settings()
        if os.path.exists(self._SETTINGS_FILE):
            self._settings.read_from_file(self._SETTINGS_FILE)
        else:
            self._settings.save_to_file(self._SETTINGS_FILE)

        self.setStyleSheet(darkstyle_css())

        self.setFixedSize(370, 125)
        self.setWindowTitle("subs2cards")

        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))

        subs_button = make_button(self, "Subtitles", 80, 70, 10, 10, self.show_subtitles_dialog)
        subs_button.setToolTip("Make cards from subtitles")

        youtube_button = make_button(self, "Youtube\nsubtitles", 80, 70, 100, 10, self.show_youtube_subtitles_dialog)
        youtube_button.setToolTip("Make cards from youtube subtitles")

        doc_button = make_button(self, "Document", 80, 70, 190, 10, self.show_document_dialog)
        doc_button.setToolTip("Make cards from document")

        web_page_button = make_button(self, "Web page", 80, 70, 280, 10, self.show_document_dialog)
        web_page_button.setToolTip("Make cards from web page")

        make_button(self, "Settings", 60, 25, 10, 90, self.show_settings)
        make_button(self, "Exit", 60, 25, 300, 90, self.close)

        self._background_subtitle_processing = None
        self._words_database = None

    def load_words_database(self) -> WordsDatabase:
        if not self._words_database:
            self._words_database = WordsDatabase(self._settings.words_database)
        return self._words_database

    def show_settings(self):
        settings_dialog = SettingsDialog(self, self._settings)
        if settings_dialog.exec_():
            self._settings = settings_dialog.settings
            self._settings.save_to_file(self._SETTINGS_FILE)
            self._words_database = None

    def show_subtitles_dialog(self):
        subtitles_dialog = SubtitlesDialog(self, self.load_words_database())
        subtitles_dialog.exec_()

    def show_youtube_subtitles_dialog(self):
        subtitles_dialog = YoutubeSubtitlesDialog(self, self.load_words_database())
        subtitles_dialog.exec_()

    def show_document_dialog(self):
        document_dialog = DocumentDialog(self, self.load_words_database())
        document_dialog.exec_()
