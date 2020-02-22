from typing import Set, Dict
import os

from PyQt5.QtCore import QRunnable, QMetaObject, Q_ARG, Qt, Q_RETURN_ARG, QVariant

from src.lang.phrasal_verbs import get_phrasal_verbs
from src.lang.token import (get_tokens_from_subs_file, get_tokens_from_tsv_base,
                            add_words_from, remove_similar_words, CountedToken)


class SubtitlesProcessor(QRunnable):
    def __init__(self, skip_list_file: str, en_subs_file: str,
                 native_subs_file: str, tsv_base_file: str,
                 main_window: 'MainWindow'):
        QRunnable.__init__(self)
        self._skip_list_file = skip_list_file
        self._en_subs_file = en_subs_file
        self._native_subs_file = native_subs_file
        self._tsv_base_file = tsv_base_file
        self._main_window = main_window

    def _read_skip_list(self) -> Set[str]:
        if not self._skip_list_file or not os.path.exists(self._skip_list_file):
            return set()
        ignored_words = set()
        with open(self._skip_list_file, 'r') as fp:
            for word in fp:
                ignored_word = word.strip()
                if ignored_word:
                    ignored_words.add(ignored_word)
        return ignored_words

    def _show_words(self, ignored_words: Set[str], words: Dict[str, CountedToken]) -> Set[str]:
        ignored_words = QMetaObject.invokeMethod(
            self._main_window,
            "on_word_list_show",
            Qt.BlockingQueuedConnection,
            Q_RETURN_ARG(QVariant),
            Q_ARG(QVariant, QVariant(ignored_words)),
            Q_ARG(QVariant, QVariant(words))
        )
        if self._skip_list_file:
            with open(self._skip_list_file, 'w', encoding='utf-8') as out_fp:
                for ignored_word in sorted(ignored_words):
                    out_fp.write(ignored_word)
                    out_fp.write("\n")
        return ignored_words

    def run(self) -> None:
        ignored_words = self._read_skip_list()
        words_from_tsv_base = get_tokens_from_tsv_base(self._tsv_base_file)

        words_from_subs = get_tokens_from_subs_file(self._en_subs_file, self._native_subs_file)
        phrasal_verbs = get_phrasal_verbs(words_from_subs)

        words = add_words_from({}, words_from_tsv_base)
        words = add_words_from(words, words_from_subs)
        words = add_words_from(words, phrasal_verbs)

        words = remove_similar_words(words)
        ignored_words = self._show_words(ignored_words, words)

        words = {word: token for word, token in words.items() if word not in ignored_words}
        if self._tsv_base_file:
            with open(self._tsv_base_file, 'w', encoding='utf-8') as out_fp:
                for word in sorted(words):
                    out_fp.write(words[word].token.to_tsv_line())

        QMetaObject.invokeMethod(self._main_window, "on_finish_processing", Qt.QueuedConnection)
