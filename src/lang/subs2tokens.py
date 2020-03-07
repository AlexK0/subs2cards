from typing import List

import pysubs2

from src.lang.token import Token, normalize_text, text_to_raw_tokens


def _is_overlap(event1: pysubs2.SSAEvent, event2: pysubs2.SSAEvent) -> bool:
    return event1.start <= event2.end and event1.end >= event2.start


def _overlap_interval(event1: pysubs2.SSAEvent, event2: pysubs2.SSAEvent) -> int:
    return min(event1.end, event2.end) - max(event1.start, event2.start)


def _is_less(event1: pysubs2.SSAEvent, event2: pysubs2.SSAEvent) -> bool:
    return not _is_overlap(event1, event2) and event1.start < event2.start


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

        while native_i < len(native_lines) and _is_less(native_lines[native_i], en_line):
            native_i += 1

        normalized_native_text = ""
        if native_i < len(native_lines) and _is_overlap(native_lines[native_i], en_line):
            interval = _overlap_interval(native_lines[native_i], en_line)
            overlap_rate = interval / en_line.duration
            if overlap_rate > 0.5:
                normalized_native_text = normalize_text(native_lines[native_i].text)

        for word, tag in text_to_raw_tokens(normalized_text):
            text_tokens.append(Token(word, tag, normalized_text, normalized_native_text))

    return text_tokens
