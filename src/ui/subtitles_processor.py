from PyQt5.QtCore import QRunnable, QMetaObject, Q_ARG, Qt, QVariant
from PyQt5.QtWidgets import QDialog

from src.lang.phrasal_verbs import get_phrasal_verbs
from src.lang.token import add_words_from, remove_similar_words
from src.lang.subs2tokens import get_tokens_from_subs_file


class SubtitlesProcessor(QRunnable):
    def __init__(self, en_subs_file: str, native_subs_file: str, parent: QDialog):
        QRunnable.__init__(self)
        self._en_subs_file = en_subs_file
        self._native_subs_file = native_subs_file
        self._parent = parent

    def run(self) -> None:
        words_from_subs = get_tokens_from_subs_file(self._en_subs_file, self._native_subs_file)
        phrasal_verbs = get_phrasal_verbs(words_from_subs)

        words = add_words_from({}, words_from_subs)
        words = add_words_from(words, phrasal_verbs)
        words = remove_similar_words(words)

        result = Q_ARG(QVariant, QVariant(words))
        QMetaObject.invokeMethod(self._parent, "on_finish_processing", Qt.QueuedConnection, result)
