#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.lang.token import Token

if __name__ == '__main__':
    async_init = Thread(target=Token.preload_nltk_data)
    async_init.start()
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
