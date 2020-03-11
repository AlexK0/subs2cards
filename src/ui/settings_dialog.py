import json

from PyQt5.QtCore import Qt, QThreadPool, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QDialog

from src.ui.nltk_data_updater import NLTKDataUpdater
from src.ui.widget import make_button, make_edit_line_with_button


class Settings:
    def __init__(self):
        self.words_database = "words_database.json"

    def read_from_file(self, file: str) -> 'None':
        with open(file, 'r') as fp:
            settings = json.load(fp)
            if "words_database" in settings:
                self.words_database = settings["words_database"]

    def save_to_file(self, file: str):
        with open(file, 'w') as fp:
            json.dump(self.__dict__, fp)


class SettingsDialog(QDialog):
    def __init__(self, parent: QMainWindow, settings: Settings):
        QDialog.__init__(self, parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 80)

        self.settings = settings

        self._nltk_data_update = make_button(self, "Update NLTK", 110, 25, 10, 45, self.start_nltk_data_updating)
        self._background_nltk_uploading = None

        self._ok_button = make_button(self, "OK", 70, 25, 240, 45, self.on_accept)
        self._buttons = (
            self._nltk_data_update,
            self._ok_button,
            make_button(self, "Cancel", 70, 25, 320, 45, self.reject),
        )

        self._words_database = make_edit_line_with_button(self, 'Database file', "JSON file (*.json)", 10, 10)
        self._words_database.textChanged.connect(lambda: self._ok_button.setDisabled(not self._words_database.text()))
        self._words_database.setText(self.settings.words_database)

    def start_nltk_data_updating(self) -> None:
        self._nltk_data_update.setText("Wait..")
        for button in self._buttons:
            button.setDisabled(True)

        self._background_nltk_uploading = NLTKDataUpdater(self)
        QThreadPool.globalInstance().start(self._background_nltk_uploading)

    @pyqtSlot()
    def on_finish_nltk_data_updating(self) -> None:
        self._nltk_data_update.setText("Update NLTK")
        for button in self._buttons:
            button.setDisabled(False)
        self._ok_button.setDisabled(not self._words_database.text())

    def on_accept(self):
        self.settings.words_database = self._words_database.text()
        self.accept()
