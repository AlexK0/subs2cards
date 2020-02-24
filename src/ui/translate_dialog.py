from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView

from src.ui.widget import make_button, make_combobox


class TranslateDialog(QDialog):
    _GOOGLE_TRANSLATE = "google translate"
    _TRANSLATE_PAGES = {
        _GOOGLE_TRANSLATE: "https://translate.google.com/#view=home&op=translate&sl=en&tl=ru&text=%s",
        "yandex translate": "https://translate.yandex.ru/?lang=en-ru&text=%s",
        "cambridge dictionary": "https://dictionary.cambridge.org/dictionary/english/%s",
        "urban dictionary": "https://www.urbandictionary.com/define.php?term=%s"
    }

    def __init__(self, parent: QDialog, word: str):
        QDialog.__init__(self, parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Check word")
        self.setFixedSize(1100, 600)

        self._word = word
        self._web = QWebEngineView(self)
        self._web.setFixedSize(self.width() - 20, self.height() - 20 - 35)
        self._web.move(10, 10)

        make_combobox(self, self._TRANSLATE_PAGES.keys(), 130, 10, self._web.height() + 20, self._show_translation)
        self._translation = QLineEdit(self)
        self._translation.setFixedSize(820, 25)
        self._translation.move(150, self._web.height() + 20)
        self._translation.setPlaceholderText("Write the translation here, use \",\" as a separator")

        make_button(self, "Cancel", 50, 1040, self._web.height() + 20, self.reject)
        make_button(self, "OK", 50, 980, self._web.height() + 20, self.accept)
        self._show_translation(self._GOOGLE_TRANSLATE)

    def _show_translation(self, page: str) -> None:
        self._web.load(QUrl(self._TRANSLATE_PAGES[page] % self._word))
        self._web.show()
