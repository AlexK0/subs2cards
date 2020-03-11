from typing import Dict

from PyQt5.QtCore import QThreadPool, pyqtSlot, QVariant
from PyQt5.QtWidgets import QDialog, QWidget

from src.lang.token import Token
from src.lang.words_database import WordsDatabase
from src.lang.document2tokens import get_tokens_from_document_file

from src.ui.words_dialog import show_words_dialog
from src.ui.widget import make_button, make_edit_line_with_button
from src.ui.tokens_processor import TokensProcessor


class DocumentDialog(QDialog):
    def __init__(self, parent: QWidget, words_database: WordsDatabase):
        QDialog.__init__(self, parent)

        self.setFixedSize(460, 80)
        self.setWindowTitle("Document")

        self._words_database = words_database

        extensions = ";;".join((
            "Document file (*.doc *.docx *.pptx *.rtf *.pdf *.odt)",
            "E-mail file (*.eml *.msg)",
            "E-book file (*.epub)",
            "HTML file (*.html *.htm)",
            "TXT file (*.txt)",
            "JSON file (*.json)",
            "CSV file (*.csv)",
            "XLS file (*.xls *.xlsx)"
        ))
        self._document_line = make_edit_line_with_button(self, 'Document', extensions, 10, 10, True)

        go_button_x = self._document_line.pos().x() + self._document_line.width() - 60
        self._go_button = make_button(self, "Go!", 60, 25, go_button_x, 45, self.start_document_processing)
        exit_button_x = self._go_button.pos().x() + self._go_button.width() + 10
        make_button(self, "Exit", 60, 25, exit_button_x, 45, self.close)

        self._background = None

    def __del__(self):
        QThreadPool.globalInstance().waitForDone()

    def start_document_processing(self) -> None:
        self._go_button.setText("Wait..")
        self._go_button.setDisabled(True)

        document_file = self._document_line.text().strip()
        self._background = TokensProcessor(lambda: get_tokens_from_document_file(document_file), self)
        QThreadPool.globalInstance().start(self._background)

    @pyqtSlot(QVariant, str)
    def on_finish_processing(self, words: Dict[str, Token], exception: str) -> None:
        self._words_database = show_words_dialog(self, self._words_database, words)
        self._go_button.setText("Go!")
        self._go_button.setDisabled(False)

