from PyQt5.QtCore import QRunnable, QMetaObject, Q_ARG, Qt, QVariant
from PyQt5.QtWidgets import QDialog

from src.lang.words_processor import process_words


class TokensProcessor(QRunnable):
    def __init__(self, tokens_gen: callable, parent: QDialog):
        QRunnable.__init__(self)
        self._tokens_gen = tokens_gen
        self._parent = parent

    def run(self) -> None:
        result = Q_ARG(QVariant, QVariant(process_words(self._tokens_gen())))
        QMetaObject.invokeMethod(self._parent, "on_finish_processing", Qt.QueuedConnection, result)
