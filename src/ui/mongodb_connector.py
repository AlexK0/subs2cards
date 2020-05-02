import time

import pymongo

from PyQt5.QtCore import QRunnable, QMetaObject, Qt, Q_ARG, QVariant


class MongodbGlobalConnection:
    client = None
    mongodb_url = None

    @staticmethod
    def connect(mongodb_url: str) -> None:
        MongodbGlobalConnection.client = None
        MongodbGlobalConnection.mongodb_url = None
        connecting_client = pymongo.MongoClient(mongodb_url, connect=True)
        connecting_client.server_info()
        MongodbGlobalConnection.client = connecting_client
        MongodbGlobalConnection.mongodb_url = mongodb_url

    @staticmethod
    def try_connect(mongodb_url: str) -> None:
        try:
            MongodbGlobalConnection.connect(mongodb_url)
        except:
            pass


class MongodbConnector(QRunnable):
    def __init__(self, parent: 'QDialog', mongodb_url: str):
        QRunnable.__init__(self)
        self._parent = parent
        self._mongodb_url = mongodb_url

    def run(self) -> None:
        exception = None
        try:
            MongodbGlobalConnection.connect(self._mongodb_url)
        except Exception as ex:
            exception = ex

        time.sleep(1)

        exception = Q_ARG(QVariant, QVariant(exception))
        QMetaObject.invokeMethod(self._parent, "on_mongodb_connection_finished", Qt.QueuedConnection, exception)
