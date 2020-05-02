import json
import os
from typing import Dict, List, Optional

import pymongo


class WordRecord:
    def __init__(self, known: bool = True, translations: Optional[List[str]] = None):
        self.known = known
        self.translations = translations or []

    @staticmethod
    def from_dict(w: Dict) -> 'WordRecord':
        return WordRecord(w.get("known", True), w.get("translations", []))


class WordsDatabase:
    def __init__(self, words_database_path: str):
        self._words_database_path = words_database_path

        words_db_dict = {}
        if os.path.exists(self._words_database_path):
            with open(self._words_database_path, 'r') as fp:
                words_db_dict = json.load(fp)

        self._words = {word: WordRecord.from_dict(w) for word, w in words_db_dict.items()}
        self._save_required = []

    def get_word(self, word: str) -> Optional[WordRecord]:
        return self._words.get(word)

    def is_known_word(self, word: str) -> bool:
        word_record = self._words.get(word)
        return word_record and word_record.known

    def update_word(self, word: str, known: Optional[bool] = None, translations: Optional[List[str]] = None) -> None:
        record = self._words.setdefault(word, WordRecord())
        if known is not None:
            record.known = known
        if translations is not None:
            record.translations = translations
        if (known is not None) or (translations is not None):
            self._save_required.append(word)

    def save_to_disk(self) -> None:
        if self._save_required:
            self._save_required = []
            with open(self._words_database_path, 'w') as fp:
                json.dump({w: r.__dict__ for w, r in self._words.items()}, fp, indent=2, sort_keys=True)
