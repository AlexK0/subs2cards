from typing import Dict
import re

from PyQt5.QtCore import QThreadPool, pyqtSlot, QVariant, QUrl, Qt
from PyQt5.QtWidgets import QDialog, QWidget, QLineEdit, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

from src.lang.token import Token
from src.lang.words_database import WordsDatabase
from src.lang.document2tokens import get_tokens_from_html

from src.ui.words_dialog import show_words_dialog
from src.ui.widget import make_button, show_error
from src.ui.tokens_processor import TokensProcessor


class _WebPagePreview(QDialog):
    def __init__(self, parent: QDialog, url: str):
        QDialog.__init__(self, parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Web page preview")
        self.setFixedSize(1100, 600)

        self._web = QWebEngineView(self)
        self._web.setFixedSize(self.width() - 20, self.height() - 20 - 35)
        self._web.move(10, 10)

        self._web.load(QUrl(url))
        self._web.show()
        self._web.loadFinished.connect(self._page_loaded)

        make_button(self, "Cancel", 50, 25, 1040, self._web.height() + 20, self.reject)
        self._ok_button = make_button(self, "Go!", 50, 25, 980, self._web.height() + 20, self.accept)
        self._ok_button.setDisabled(True)

        self.page_html = ""

    def _save_html(self, html):
        self.page_html = html
        self._ok_button.setDisabled(False)

    def _page_loaded(self):
        self._web.page().runJavaScript("document.documentElement.outerHTML", self._save_html)


class WebPageDialog(QDialog):
    _URL_REGEX = re.compile(r"^https?://.+$")

    def __init__(self, parent: QWidget, words_database: WordsDatabase):
        QDialog.__init__(self, parent)

        self.setFixedSize(460, 80)
        self.setWindowTitle("Web page")

        self._words_database = words_database

        self._page_url = QLineEdit(self)
        self._page_url.resize(440, 25)
        self._page_url.move(10, 10)
        self._page_url.setPlaceholderText("Web page url..")
        self._page_url.setToolTip("Enter youtube url like https://www.google.com")
        self._page_url.textChanged.connect(self._on_url_changed)
        self._youtube_video_id = ""

        go_button_x = self._page_url.pos().x() + self._page_url.width() - 160
        self._show_button = make_button(self, "Page preview", 90, 25, go_button_x, 45, self.show_web_page)
        exit_button_x = self._show_button.pos().x() + self._show_button.width() + 10
        make_button(self, "Exit", 60, 25, exit_button_x, 45, self.close)

        self._show_button.setDisabled(True)

        self._background = None

    def __del__(self):
        QThreadPool.globalInstance().waitForDone()

    def _on_url_changed(self):
        url = self._page_url.text()
        self._show_button.setDisabled(not self._URL_REGEX.match(url))

    def show_web_page(self) -> None:
        web_page_preview = _WebPagePreview(self, self._page_url.text());
        if web_page_preview.exec_():
            self._show_button.setText("Wait..")
            self._show_button.setDisabled(True)
            self._page_url.setDisabled(True)
            self._background = TokensProcessor(lambda: get_tokens_from_html(web_page_preview.page_html), self)
            QThreadPool.globalInstance().start(self._background)

        web_page_preview.deleteLater()

    @pyqtSlot(QVariant, QVariant)
    def on_finish_processing(self, words: Dict[str, Token], exception: Exception) -> None:
        if exception is not None:
            show_error(self, "Can't load web page text :(   ", exception)
        else:
            self._words_database = show_words_dialog(self, self._words_database, words)
        self._show_button.setText("Page preview")
        self._show_button.setDisabled(False)
        self._page_url.setDisabled(False)
