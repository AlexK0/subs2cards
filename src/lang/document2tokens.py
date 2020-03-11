from typing import List
import re

import nltk
import textract

from src.lang.token import Token, text_to_raw_tokens

_SUB_SPACES_LINES_REGEX = re.compile(r"\s+")
_SPLIT_LINES_REGEX = re.compile(r"\t|\n\s+|\r\n\s+")


def get_tokens_from_document_file(document_file: str) -> List[Token]:
    text = textract.process(document_file).decode()
    text_tokens = []

    for line in _SPLIT_LINES_REGEX.split(text):
        for sentence in nltk.sent_tokenize(line.strip()):
            sentence_parts = []
            for part in sentence.splitlines():
                part = part.strip()
                if part:
                    sentence_parts.append(part)
            i = 0
            out_i = 0
            while i + 1 < len(sentence_parts):
                if sentence_parts[i][0].isupper() and sentence_parts[i][-1] != '.' \
                        and not sentence_parts[i + 1][0].isupper() and sentence_parts[i + 1][-1] == '.':
                    sentence_parts[out_i] = " ".join((sentence_parts[i], sentence_parts[i + 1]))
                    i += 2
                else:
                    sentence_parts[out_i] = sentence_parts[i]
                    i += 1
                out_i += 1
            if i < len(sentence_parts):
                sentence_parts[out_i] = sentence_parts[i]

            for part in range(out_i + 1):
                for word, tag in text_to_raw_tokens(sentence_parts[part]):
                    text_tokens.append(Token(word, tag, sentence_parts[part]))

    return text_tokens
