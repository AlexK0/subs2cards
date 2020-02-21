import nltk

from PyQt5.QtCore import QRunnable, QMetaObject, Q_ARG, Qt


class NLTKDataUpdater(QRunnable):
    def __init__(self, main_window: 'MainWindow'):
        QRunnable.__init__(self)
        self._main_window = main_window

    def run(self) -> None:
        modules = ("averaged_perceptron_tagger", "brown", "punkt", "universal_tagset", "wordnet")

        QMetaObject.invokeMethod(
            self._main_window,
            "on_processing_progress",
            Qt.QueuedConnection,
            Q_ARG(int, 0),
            Q_ARG(int, len(modules))
        )
        for i, module in enumerate(modules):
            nltk.download(module)
            QMetaObject.invokeMethod(
                self._main_window,
                "on_processing_progress",
                Qt.QueuedConnection,
                Q_ARG(int, i + 1),
                Q_ARG(int, len(modules))
            )

        QMetaObject.invokeMethod(self._main_window, "on_finish_nltk_data_updating", Qt.QueuedConnection)
