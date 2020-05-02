import time

import nltk

from PyQt5.QtCore import QRunnable, QMetaObject, Qt


class NLTKDataUpdater(QRunnable):
    _MODULES = {
        "taggers": ["averaged_perceptron_tagger", "universal_tagset"],
        "corpora": ["brown", "wordnet", "words", "reuters"],
        "tokenizers": ["punkt"]
    }

    def __init__(self, parent: 'QDialog'):
        QRunnable.__init__(self)
        self._parent = parent

    def run(self) -> None:
        for modules in self._MODULES.values():
            for module in modules:
                nltk.download(module)
                time.sleep(0.1)

        time.sleep(1)
        QMetaObject.invokeMethod(self._parent, "on_finish_nltk_data_updating", Qt.QueuedConnection)
