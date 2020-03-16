from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QHeaderView, QAbstractItemView, QDialog, QTableWidget, QTableWidgetItem)

from src.lang.token import Token
from src.lang.words_database import WordsDatabase

from src.ui.widget import make_button, make_combobox, make_label
from src.ui.word_card_dialog import WordCardDialog


class WordTableDialog(QDialog):
    _CHECK_STATE_TO_STR = {Qt.Checked: "unknown", Qt.Unchecked: "known"}
    _ALL = "all"
    _COLUMNS = (("word", 110), ("ref cnt", 55), ("class", 85),
                ("translations", 200), ("english example", 500), ("native example", 500))

    def __init__(self, parent: QDialog, words_database: WordsDatabase, words: Dict[str, Token]):
        QDialog.__init__(self, parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        if any(token.context_sentence_native for token in words.values()):
            self._columns = self._COLUMNS
        else:
            self._columns = self._COLUMNS[:-1]

        total_width = sum(column_width for column_name, column_width in self._columns) + 20
        self.words_database = words_database
        self.setFixedSize(total_width, 545)
        self.setWindowTitle("Choose useful words")

        self._table = QTableWidget(self)
        self._table.resize(total_width, 500)
        self._table.setFocusPolicy(Qt.NoFocus)
        self._table.setSelectionMode(QAbstractItemView.NoSelection)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)

        self._table.setColumnCount(len(self._columns))
        for row_id, header in enumerate(self._columns):
            self._table.setColumnWidth(row_id, header[1])
            self._table.setHorizontalHeaderItem(row_id, QTableWidgetItem(header[0]))
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self._table.setRowCount(len(words))

        used_parts_of_speech = set()
        for row_id, word in enumerate(sorted(words)):
            self._table.setRowHeight(row_id, 10)

            word_checkbox = QTableWidgetItem(word)
            word_checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            word_checkbox.setCheckState(Qt.Unchecked if self.words_database.is_known_word(word) else Qt.Checked)

            word_token = words[word]
            self._table.setItem(row_id, 0, word_checkbox)

            ref_counter = QTableWidgetItem()
            ref_counter.setData(Qt.DisplayRole, word_token.ref_counter)
            ref_counter.setTextAlignment(Qt.AlignCenter)
            self._table.setItem(row_id, 1, ref_counter)

            part_of_speech_str = word_token.get_pretty_part_of_speech()
            used_parts_of_speech.add(part_of_speech_str)
            part_of_speech = QTableWidgetItem(part_of_speech_str)
            part_of_speech.setTextAlignment(Qt.AlignCenter)
            self._table.setItem(row_id, 2, part_of_speech)

            word_record = self.words_database.get_word(word)
            translations_text = ", ".join(word_record.translations if word_record else [])
            translations = QTableWidgetItem(translations_text)
            translations.setToolTip(translations_text)
            self._table.setItem(row_id, 3, translations)

            en_sentence = QTableWidgetItem(word_token.context_sentence_en)
            en_sentence.setToolTip(word_token.context_sentence_en)
            self._table.setItem(row_id, 4, en_sentence)

            if word_token.context_sentence_native:
                native_sentence = QTableWidgetItem(word_token.context_sentence_native)
                native_sentence.setToolTip(word_token.context_sentence_native)
                self._table.setItem(row_id, 5, native_sentence)

        self._save_button = make_button(self, "Save", 60, 25, total_width - 3 * 70, 510,
                                        self.save_current_state_to_words_database)
        self._save_button.setDisabled(True)

        make_button(self, "Start", 60, 25, total_width - 2 * 70, 510, self.accept),
        make_button(self, "Cancel", 60, 25, total_width - 70, 510, self.reject)

        self._part_of_speech_filter = self._ALL
        self._check_state_filter = self._ALL

        make_combobox(self, (self._ALL, *self._CHECK_STATE_TO_STR.values()), 100, 10, 510, self._filter_by_checks)
        make_combobox(self, (self._ALL, *sorted(used_parts_of_speech)), 100, 120, 510, self._filter_by_part_of_speech)

        self._known_label = make_label(self, 100, 25, int(total_width / 2) - 50, 511, QFont("Calibri", 13))

        self._table.itemChanged.connect(self._on_table_update)
        self._table.setSortingEnabled(True)
        self._table.show()

        self._on_table_update()
        self._save_button.setDisabled(True)

    def _on_table_update(self):
        unknown_count = 0
        total_count = self._table.rowCount()
        for row_id in range(total_count):
            if self._table.item(row_id, 0).checkState() == Qt.Checked:
                unknown_count += 1

        self._save_button.setDisabled(False)
        self._known_label.setText("{}/{}".format(unknown_count, total_count))

    def save_current_state_to_words_database(self) -> None:
        self._save_button.setDisabled(True)

        for row_id in range(self._table.rowCount()):
            word_checkbox = self._table.item(row_id, 0)
            known = word_checkbox.checkState() == Qt.Unchecked
            self.words_database.update_word(word_checkbox.text(), known)

        self.words_database.save_to_disk()

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


def show_word_table_dialog(parent: QDialog, words_database: WordsDatabase, words: Dict[str, Token]) -> WordsDatabase:
    skip_list_window = WordTableDialog(parent, words_database, words)
    if skip_list_window.exec_():
        skip_list_window.save_current_state_to_words_database()
        words_database = skip_list_window.words_database
        words = {word: token for word, token in words.items() if not words_database.is_known_word(word)}
        if words:
            card_dialog = WordCardDialog(parent, words, words_database)
            card_dialog.exec_()
            card_dialog.deleteLater()

    skip_list_window.deleteLater()
    return words_database
