import os

from PyQt5.QtWidgets import QMainWindow, QStyle
from qt5_t5darkstyle import darkstyle_css

from src.lang.words_database import WordsDatabase

from src.ui.subtitles_processor import SubtitlesProcessor
from src.ui.settings_dialog import SettingsDialog, Settings
from src.ui.words_dialog import WordsDialog
from src.ui.widget import make_button, make_edit_line_with_button
from src.ui.word_card_dialog import WordCardDialog
from src.ui.subtitles_dialog import SubtitlesDialog


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

        self.setFixedSize(310, 125)
        self.setWindowTitle("subs2cards")

        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))

        make_button(self, "Subtitles", 80, 70, 10, 10, self.show_subtitles_dialog)

        make_button(self, "Settings", 60, 25, 10, 90, self.show_settings)
        make_button(self, "Exit", 60, 25, 240, 90, self.close)

        self._background_subtitle_processing = None
        self._words_database = None

    def load_words_database(self) -> None:
        if not self._words_database:
            self._words_database = WordsDatabase(self._settings.words_database)

    def show_settings(self):
        settings_dialog = SettingsDialog(self, self._settings)
        if settings_dialog.exec_():
            self._settings = settings_dialog.settings
            self._settings.save_to_file(self._SETTINGS_FILE)
            self._words_database = None

    def show_subtitles_dialog(self):
        self.load_words_database()
        subtitles_dialog = SubtitlesDialog(self, self._words_database)
        subtitles_dialog.exec_()
