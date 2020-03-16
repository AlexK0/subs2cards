from typing import List
import re
from tempfile import NamedTemporaryFile
import os

import nltk
import textract

from src.lang.token import Token, text_to_raw_tokens

_SPLIT_LINES_REGEX = re.compile(r"\t|\n\s+|\r\n\s+")


def _split_long_sentence(sentence: str):
    max_len = 150
    if len(sentence) <= max_len:
        return [sentence]
    parts = 1 + int(len(sentence) / max_len)

    part_len = int(len(sentence) / parts)

    result = []
    start = 0
    end = part_len
    while True:
        end = sentence.find(" ", end)
        if end == -1:
            short = sentence[start:].strip()
            if short:
                result.append(short)
            return result
        short = sentence[start:end].strip()
        if short:
            result.append(short)
        start = end + 1
        end += part_len


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
                for short_sentence in _split_long_sentence(sentence_parts[part]):
                    for word, tag in text_to_raw_tokens(short_sentence):
                        text_tokens.append(Token(word, tag, short_sentence))

    return text_tokens


def get_tokens_from_html(html: str) -> List[Token]:
    try:
        html_file = NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.html', delete=False)
        html_file.write(html)
        html_file.close()
        tokens = get_tokens_from_document_file(html_file.name)
        os.unlink(html_file.name)
    except:
        try:
            os.unlink(html_file.name)
        except:
            pass
        raise

    return tokens
