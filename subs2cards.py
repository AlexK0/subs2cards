#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from threading import Thread

from PyQt5.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.ui.settings_dialog import Settings
from src.ui.mongodb_connector import MongodbGlobalConnection
from src.lang.token import Token

_SETTINGS_FILE = "settings.json"

if __name__ == '__main__':
    async_init = Thread(target=Token.preload_nltk_data)
    async_init.start()

    settings = Settings(_SETTINGS_FILE)
    if settings.words_database_mongodb_url:
        async_connector = Thread(
            target=lambda: MongodbGlobalConnection.try_connect(settings.words_database_mongodb_url))
        async_connector.start()

    app = QApplication(sys.argv)
    mainWin = MainWindow(settings)
    mainWin.show()
    sys.exit(app.exec_())
