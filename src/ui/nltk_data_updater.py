import nltk

from PyQt5.QtCore import QRunnable, QMetaObject, Qt


class NLTKDataUpdater(QRunnable):
    _MODULES = ("averaged_perceptron_tagger", "brown", "punkt", "universal_tagset", "wordnet")

    def __init__(self, main_window: 'MainWindow'):
        QRunnable.__init__(self)
        self._main_window = main_window

    def run(self) -> None:
        for i, module in enumerate(self._MODULES):
            nltk.download(module)

        QMetaObject.invokeMethod(self._main_window, "on_finish_nltk_data_updating", Qt.QueuedConnection)
