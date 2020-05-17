import json
import os

from PyQt5.QtCore import Qt, QThreadPool, pyqtSlot, QVariant
from PyQt5.QtWidgets import QMainWindow, QDialog, QLineEdit

from src.ui.nltk_data_updater import NLTKDataUpdater
from src.ui.mongodb_connector import MongodbConnector, MongodbGlobalConnection
from src.ui.widget import make_button, make_edit_line_with_button, show_error


class Settings:
    def __init__(self, settings_file: str):
        self._settings_file = settings_file
        self.words_database_json_file = "words_database.json"
        self.words_database_mongodb_url = ""

        if os.path.exists(self._settings_file):
            self.read_from_file()
        else:
            self.save_to_file()

    def read_from_file(self) -> 'None':
        with open(self._settings_file, 'r') as fp:
            settings = json.load(fp)
            if "words_database_json_file" in settings:
                self.words_database_json_file = settings["words_database_json_file"]
            if "words_database_mongodb_url" in settings:
                self.words_database_mongodb_url = settings["words_database_mongodb_url"]

    def save_to_file(self):
        with open(self._settings_file, 'w') as fp:
            json.dump(self.__dict__, fp, indent=2, sort_keys=True)


class SettingsDialog(QDialog):
    def __init__(self, parent: QMainWindow, settings: Settings):
        QDialog.__init__(self, parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Settings")
        self.setFixedSize(390, 115)

        self.settings = settings

        self._nltk_data_update = make_button(self, "Update NLTK", 110, 25, 10, 80, self.start_nltk_data_updating)
        self._background_nltk_uploading = None

        self._ok_button = make_button(self, "OK", 70, 25, 230, 80, self.on_accept)
        self._connect_button = make_button(self, "Connect", 80, 25, 10, 45, self.connect_to_mongodb)
        self._buttons = (
            self._connect_button,
            self._nltk_data_update,
            self._ok_button,
            make_button(self, "Cancel", 70, 25, 310, 80, self.reject),
        )

        self._words_database = make_edit_line_with_button(self, 'Database file', "JSON file (*.json)", 10, 10)
        self._words_database.textChanged.connect(lambda: self._ok_button.setDisabled(not self._words_database.text()))
        self._words_database.setText(self.settings.words_database_json_file)

        self._mongodb_url = QLineEdit(self)
        self._mongodb_url.resize(280, 25)
        self._mongodb_url.move(100, 45)
        self._mongodb_url.setPlaceholderText("Mongodb url..")
        self._mongodb_url.setToolTip("Enter mongodb url like mongodb+srv://<user>:<password>@<host>/")
        self._mongodb_url.textChanged.connect(self.update_buttons_state)
        self._mongodb_url.setText(self.settings.words_database_mongodb_url)
        self.update_buttons_state()
        self._background_mongodb_connecting = None

    def start_nltk_data_updating(self) -> None:
        self._nltk_data_update.setText("Wait..")
        for button in self._buttons:
            button.setDisabled(True)

        self._background_nltk_uploading = NLTKDataUpdater(self)
        QThreadPool.globalInstance().start(self._background_nltk_uploading)

    def connect_to_mongodb(self) -> None:
        self._connect_button.setText("Wait..")
        for button in self._buttons:
            button.setDisabled(True)

        self._background_mongodb_connecting = MongodbConnector(self, self._mongodb_url.text())
        QThreadPool.globalInstance().start(self._background_mongodb_connecting)

    def update_buttons_state(self) -> None:
        empty_url = not self._mongodb_url.text()
        self._connect_button.setDisabled(empty_url)
        mongodb_connected = MongodbGlobalConnection.client is not None \
            and MongodbGlobalConnection.mongodb_url == self._mongodb_url.text()
        self._ok_button.setDisabled((not empty_url and not mongodb_connected) or not self._words_database.text())

    @pyqtSlot()
    def on_finish_nltk_data_updating(self) -> None:
        self._nltk_data_update.setText("Update NLTK")
        for button in self._buttons:
            button.setDisabled(False)
        self.update_buttons_state()

    @pyqtSlot(QVariant)
    def on_mongodb_connection_finished(self, exception: Exception):
        self._connect_button.setText("Connect")
        for button in self._buttons:
            button.setDisabled(False)

        self.update_buttons_state()
        if exception:
            show_error(self, "Can't connect to mongodb", exception)

    def on_accept(self):
        self.settings.words_database_mongodb_url = self._mongodb_url.text()
        self.settings.words_database_json_file = self._words_database.text()
        self.settings.save_to_file()
        self.accept()
