from typing import Set, Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QHeaderView, QAbstractItemView, QDialog, QTableWidget, QTableWidgetItem)

from src.lang.token import SharedTranslatedToken
from src.ui.widget import make_button, make_combobox


class WordsDialog(QDialog):
    _CHECK_STATE_TO_STR = {Qt.Checked: "checked", Qt.Unchecked: "unchecked"}
    _ALL = "all"
    _COLUMNS = (("word", 110), ("ref cnt", 55), ("class", 85), ("english example", 500), ("native example", 500))

    def __init__(self, parent, ignored_words: Set[str], words: Dict[str, SharedTranslatedToken]):
        QDialog.__init__(self, parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        self.ignored_words = ignored_words
        self.setFixedSize(1270, 545)
        self.setWindowTitle("Choose useful words")

        self._table = QTableWidget(self)
        self._table.resize(1270, 500)
        self._table.setFocusPolicy(Qt.NoFocus)
        self._table.setSelectionMode(QAbstractItemView.NoSelection)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)

        self._table.setColumnCount(len(self._COLUMNS))
        for row_id, header in enumerate(self._COLUMNS):
            self._table.setColumnWidth(row_id, header[1])
            self._table.setHorizontalHeaderItem(row_id, QTableWidgetItem(header[0]))
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self._table.setRowCount(len(words))

        used_parts_of_speech = set()
        for row_id, word in enumerate(sorted(words)):
            self._table.setRowHeight(row_id, 10)

            word_checkbox = QTableWidgetItem(word)
            word_checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            word_checkbox.setCheckState(Qt.Unchecked if word in self.ignored_words else Qt.Checked)

            word_token = words[word]
            self._table.setItem(row_id, 0, word_checkbox)

            ref_counter = QTableWidgetItem()
            ref_counter.setData(Qt.DisplayRole, word_token.ref_counter)
            ref_counter.setTextAlignment(Qt.AlignCenter)
            self._table.setItem(row_id, 1, ref_counter)

            part_of_speech_str = word_token.token.get_pretty_part_of_speech()
            used_parts_of_speech.add(part_of_speech_str)
            part_of_speech = QTableWidgetItem(part_of_speech_str)
            part_of_speech.setTextAlignment(Qt.AlignCenter)
            self._table.setItem(row_id, 2, part_of_speech)

            en_sentence = QTableWidgetItem(word_token.token.context_sentence_en)
            en_sentence.setToolTip(word_token.token.context_sentence_en)
            self._table.setItem(row_id, 3, en_sentence)

            native_sentence = QTableWidgetItem(word_token.token.context_sentence_native)
            native_sentence.setToolTip(word_token.token.context_sentence_native)
            self._table.setItem(row_id, 4, native_sentence)

        self._save_button = make_button(self, "Save", 60, 1060, 510, self.save_current_state)
        self._save_button.setDisabled(True)

        make_button(self, "Start", 60, 1130, 510, self.accept),
        make_button(self, "Cancel", 60, 1200, 510, self.reject)

        self._part_of_speech_filter = self._ALL
        self._check_state_filter = self._ALL

        make_combobox(self, (self._ALL, *self._CHECK_STATE_TO_STR.values()), 100, 10, 510, self._filter_by_checks)
        make_combobox(self, (self._ALL, *sorted(used_parts_of_speech)), 100, 120, 510, self._filter_by_part_of_speech)

        self._table.itemChanged.connect(lambda: self._save_button.setDisabled(False))
        self._table.setSortingEnabled(True)
        self._table.show()

    def save_current_state(self) -> None:
        self._save_button.setDisabled(True)

        self.ignored_words = set()
        for row_id in range(self._table.rowCount()):
            word_checkbox = self._table.item(row_id, 0)
            if word_checkbox.checkState() == Qt.Unchecked:
                self.ignored_words.add(word_checkbox.text())

    def _filter_by_checks(self, state: str) -> None:
        self._check_state_filter = state
        self._apply_filters()

    def _filter_by_part_of_speech(self, part_of_speech: str) -> None:
        self._part_of_speech_filter = part_of_speech
        self._apply_filters()

    def _apply_filters(self):
        for row_id in range(self._table.rowCount()):
            show_row = True
            if self._part_of_speech_filter not in (self._ALL, self._table.item(row_id, 2).text()):
                show_row = False
            elif self._check_state_filter != self._ALL and \
                    self._CHECK_STATE_TO_STR[self._table.item(row_id, 0).checkState()] != self._check_state_filter:
                show_row = False

            self._table.showRow(row_id) if show_row else self._table.hideRow(row_id)
