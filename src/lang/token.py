import re
from typing import List, Dict

import nltk
import pysubs2
import os


class Token:
    _IGNORING_TAGS = ['.', 'NUM']
    _LONG_WORD_TAGS = ['ADP', 'CONJ', 'DET', 'PRT', 'PRON']
    PHRASAL_VERB_TAG = "PHRASAL_VERB"
    _SAME_LETTER_IN_ROW = re.compile(r"(([a-z])\2\2)")
    _WNL = nltk.stem.WordNetLemmatizer()
    _PART_OF_SPEECH_SHORT2LONG = {
        "ADJ": "adjective",
        "ADP": "adposition",
        "ADV": "adverb",
        "CONJ": "conjunction",
        "DET": "determiner",
        "NOUN": "noun",
        "NUM": "numeral",
        "PRT": "particle",
        "PRON": "pronoun",
        "VERB": "verb",
        PHRASAL_VERB_TAG: "phrasal verb"
    }
    _PART_OF_SPEECH_LONG2SHORT = {y: x for x, y in _PART_OF_SPEECH_SHORT2LONG.items()}
    _ENGLISH_VOCAB = None
    _REMOVABE_ENDINGS = ("ally", "ing", "ed", "ly")
    _NORMAL_CHARS_IN_CONTEXT = {",", ".", ":", ";", "!", "?", "-", "'", " "}

    @staticmethod
    def preload_nltk_data():
        Token._WNL.lemmatize("")
        Token.is_word_in_english_vocab("")

    def __init__(self, word: str, tag: str, context_sentence_en: str, context_sentence_native: str):
        self.word = word
        self.tag = tag
        self.context_sentence_en = context_sentence_en
        self.context_sentence_native = context_sentence_native

    def clone(self, new_word: str, new_tag=None) -> 'Token':
        return Token(new_word, new_tag or self.tag, self.context_sentence_en, self.context_sentence_native)

    def lemmatize(self) -> 'Token':
        if self.tag == "ADJ":
            return self.clone(self._WNL.lemmatize(self.word, 'a'))
        if self.tag == "ADV":
            return self.clone(self._WNL.lemmatize(self.word, 'r'))
        if self.tag == "NOUN":
            return self.clone(self._WNL.lemmatize(self.word, 'n'))
        if self.tag == "VERB":
            return self.clone(self._WNL.lemmatize(self.word, 'v'))
        return self

    def try_remove_end(self):
        new_word = None
        if self.tag == "NOUN":
            new_word = self._WNL.lemmatize(self.word, 'v')
            if new_word == self.word:
                new_word = None

        if not new_word:
            for ending in self._REMOVABE_ENDINGS:
                if self.word.endswith(ending):
                    new_word = self.word[0:len(self.word) - len(ending)]
                    break

        if new_word and self.is_word_in_english_vocab(new_word):
            return new_word

        return None

    def is_interesting(self) -> bool:
        if self.tag not in self._PART_OF_SPEECH_SHORT2LONG:
            return False

        if self.tag in self._IGNORING_TAGS:
            return False

        if self.tag in self._LONG_WORD_TAGS and len(self.word) < 4:
            return False

        if len(self.word) < 3:
            return False

        if self._SAME_LETTER_IN_ROW.search(self.word):
            return False

        if self.tag == self.PHRASAL_VERB_TAG:
            return True

        return self.word.find("'") == -1 and self.is_word_in_english_vocab(self.word)

    @staticmethod
    def is_word_in_english_vocab(word: str) -> bool:
        if not Token._ENGLISH_VOCAB:
            Token._ENGLISH_VOCAB = set(w.lower() for w in nltk.corpus.brown.words())
        return word in Token._ENGLISH_VOCAB

    def is_context_worse_then(self, other: 'Token') -> bool:
        if bool(self.context_sentence_native) != bool(other.context_sentence_native):
            return bool(other.context_sentence_native)

        def is_bad_char(char: str) -> bool:
            return not char.isalpha() and char not in self._NORMAL_CHARS_IN_CONTEXT
        this_bad_chars = sum(1 for char in self.context_sentence_en if is_bad_char(char))
        other_bad_chars = sum(1 for char in other.context_sentence_en if is_bad_char(char))

        if this_bad_chars != other_bad_chars:
            return this_bad_chars > other_bad_chars

        this_en_context_words = sum(1 for char in self.context_sentence_en if char.isspace()) + 1
        this_native_context_words = sum(1 for char in self.context_sentence_native if char.isspace()) + 1
        this_diff = abs(this_en_context_words - this_native_context_words)

        other_en_context_words = sum(1 for char in other.context_sentence_en if char.isspace()) + 1
        other_native_context_words = sum(1 for char in other.context_sentence_native if char.isspace()) + 1
        other_diff = abs(other_en_context_words - other_native_context_words)

        return this_diff > other_diff

    def get_pretty_part_of_speech(self) -> str:
        part_of_speech = "UNKNOWN"
        if self.tag in self._PART_OF_SPEECH_SHORT2LONG:
            part_of_speech = self._PART_OF_SPEECH_SHORT2LONG[self.tag]
        return part_of_speech

    def to_tsv_line(self) -> str:
        long_part_of_speech = self.get_pretty_part_of_speech()

        return "%s\t%s\t%s\t%s\n" % \
               (self.word, long_part_of_speech, self.context_sentence_en, self.context_sentence_native)

    @staticmethod
    def from_tsv_line(tsv_line: str) -> 'Token':
        if tsv_line[-1] == "\n":
            tsv_line = tsv_line[:-1]
        (word, tag, context_sentence_en, context_sentence_native) = tsv_line.split("\t")
        if tag in Token._PART_OF_SPEECH_LONG2SHORT:
            tag = Token._PART_OF_SPEECH_LONG2SHORT[tag]
        return Token(word, tag, context_sentence_en, context_sentence_native)


_NORMALIZATION_REGEX = re.compile(r"\{.+\}|\"")
_URL_REGEX = re.compile(r"(https?://)|(\w\.ru)|(\w\.com)")


def normalize_text(text: str) -> str:
    if _URL_REGEX.search(text):
        return ""
    return _NORMALIZATION_REGEX.sub("", text.replace("\\N", " "))


def is_overlap(event1: pysubs2.SSAEvent, event2: pysubs2.SSAEvent) -> bool:
    return event1.start <= event2.end and event1.end >= event2.start


def overlap_interval(event1: pysubs2.SSAEvent, event2: pysubs2.SSAEvent) -> int:
    return min(event1.end, event2.end) - max(event1.start, event2.start)


def is_less(event1: pysubs2.SSAEvent, event2: pysubs2.SSAEvent) -> bool:
    return not is_overlap(event1, event2) and event1.start < event2.start


def get_tokens_from_subs_file(en_subs_file: str, native_subs_file: str) -> List[Token]:
    en_subs = pysubs2.load(en_subs_file, encoding="utf-8")
    native_subs = pysubs2.load(native_subs_file, encoding="utf-8") if native_subs_file else []

    en_lines = [line for line in en_subs]
    native_lines = [line for line in native_subs]

    text_tokens = []
    native_i = 0
    for en_i, en_line in enumerate(en_lines):
        normalized_text = normalize_text(en_line.text)
        if not normalized_text:
            continue

        while native_i < len(native_lines) and is_less(native_lines[native_i], en_line):
            native_i += 1

        normalized_native_text = ""
        if native_i < len(native_lines) and is_overlap(native_lines[native_i], en_line):
            interval = overlap_interval(native_lines[native_i], en_line)
            overlap_rate = interval / en_line.duration
            if overlap_rate > 0.5:
                normalized_native_text = normalize_text(native_lines[native_i].text)

        tokens_raw = nltk.word_tokenize(normalized_text.lower())
        tagged_raw_tokens = nltk.pos_tag(tokens_raw, tagset='universal')

        for word, tag in tagged_raw_tokens:
            text_tokens.append(Token(word, tag, normalized_text, normalized_native_text))

    return text_tokens


def get_tokens_from_tsv_base(tsv_base_file: str) -> List[Token]:
    if not tsv_base_file or not os.path.exists(tsv_base_file):
        return []

    with open(tsv_base_file, "r", encoding="utf-8") as f:
        return [Token.from_tsv_line(line) for line in f.readlines() if line]


class SharedTranslatedToken:
    def __init__(self, token: Token):
        self.token = token
        self.ref_counter = 1
        self.native_translations = []


def add_words_from(dest: Dict[str, SharedTranslatedToken], tokens: List[Token]) -> Dict[str, SharedTranslatedToken]:
    for token in tokens:
        if not token.is_interesting():
            continue

        fixed_token = token.lemmatize()
        if not fixed_token.is_interesting():
            continue

        if fixed_token.word not in dest:
            dest[fixed_token.word] = SharedTranslatedToken(fixed_token)
        else:
            counted_token = dest[fixed_token.word]
            counted_token.ref_counter += 1
            if counted_token.token.is_context_worse_then(fixed_token):
                counted_token.token = fixed_token

    return dest


def remove_similar_words(words: Dict[str, SharedTranslatedToken]) -> Dict[str, SharedTranslatedToken]:
    for word in list(words):
        word_without_end = words[word].token.try_remove_end()
        if word_without_end and word_without_end in words:
            words[word_without_end].ref_counter += 1
            del words[word]

    return words
