from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

from src.ui.widget import make_button, make_label, make_combobox


class TranslateDialog(QDialog):
    _TRANSLATE_PAGES = {
        "google translate": "https://translate.google.com/#view=home&op=translate&sl=en&tl=ru&text=%s",
        "yandex translate": "https://translate.yandex.ru/?lang=en-ru&text=%s",
        "cambridge dictionary": "https://dictionary.cambridge.org/dictionary/english/%s",
        "urban dictionary": "https://www.urbandictionary.com/define.php?term=%s"
    }

    def __init__(self, parent: QDialog, word: str):
        QDialog.__init__(self, parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Google translate")
        self.setFixedSize(1100, 600)

        self._word = word
        self._web = QWebEngineView(self)
        self._web.setFixedSize(self.width() - 20, self.height() - 20 - 35)
        self._web.move(10, 10)

        make_combobox(self, self._TRANSLATE_PAGES.keys(), 110, 10, self._web.height() + 20, self._show_translation)
        self._show_translation(next(iter(self._TRANSLATE_PAGES.keys())))

    def _show_translation(self, page: str) -> None:
        self._web.load(QUrl(self._TRANSLATE_PAGES[page] % self._word))
        self._web.show()
