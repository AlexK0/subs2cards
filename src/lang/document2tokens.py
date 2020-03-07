from typing import List
import re

import textract

from src.lang.token import Token, text_to_raw_tokens

_FINDALL_REGEX = re.compile(r".*?[\.\!\?]+[\s]")
_REPLACING_SPACES_REGEX = re.compile(r"\n\n+|\r\n(\r\n)+|\t+|\v+")
_REMOVING_SPACES_REGEX = re.compile(r"\n|\r\n")


def get_tokens_from_document_file(document_file: str) -> List[Token]:
    text = textract.process(document_file).decode()
    text = _REPLACING_SPACES_REGEX.sub(".", text)
    text = _REMOVING_SPACES_REGEX.sub(" ", text)
    text_tokens = []
    for sentence in _FINDALL_REGEX.findall(text):
        sentence = sentence.strip()
        if sentence:
            print(sentence)
            for word, tag in text_to_raw_tokens(sentence):
                text_tokens.append(Token(word, tag, sentence))

    return text_tokens
