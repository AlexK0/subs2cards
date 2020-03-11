from typing import List
import re

import pysubs2
from youtube_transcript_api import YouTubeTranscriptApi

from src.lang.token import Token, text_to_raw_tokens


_NORMALIZATION_REGEX = re.compile(r"\{.+\}|\"")
_URL_REGEX = re.compile(r"(https?://)|(\w\.ru)|(\w\.com)")


def _normalize_text(text: str) -> str:
    if _URL_REGEX.search(text):
        return ""
    return _NORMALIZATION_REGEX.sub("", text.replace("\\N", " "))


class SubEvent:
    def __init__(self, start, duration, text):
        self.start = start
        self.duration = duration
        self.end = self.start + self.duration
        self.text = text


def _is_overlap(event1: SubEvent, event2: SubEvent) -> bool:
    return event1.start <= event2.end and event1.end >= event2.start


def _overlap_interval(event1: SubEvent, event2: SubEvent) -> float:
    return min(event1.end, event2.end) - max(event1.start, event2.start)


def _is_less(event1: SubEvent, event2: SubEvent) -> bool:
    return not _is_overlap(event1, event2) and event1.start < event2.start


def _subs_to_tokens(en_subs: List[SubEvent], native_subs: List[SubEvent]) -> List[Token]:
    text_tokens = []
    native_i = 0
    for en_i, en_line in enumerate(en_subs):
        normalized_text = _normalize_text(en_line.text)
        if not normalized_text:
            continue

        while native_i < len(native_subs) and _is_less(native_subs[native_i], en_line):
            native_i += 1

        normalized_native_text = ""
        if native_i < len(native_subs) and _is_overlap(native_subs[native_i], en_line):
            interval = _overlap_interval(native_subs[native_i], en_line)
            overlap_rate = interval / en_line.duration
            if overlap_rate > 0.5:
                normalized_native_text = _normalize_text(native_subs[native_i].text)

        for word, tag in text_to_raw_tokens(normalized_text):
            text_tokens.append(Token(word, tag, normalized_text, normalized_native_text))

    return text_tokens


def get_tokens_from_youtube(video_id: str) -> List[Token]:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['en'])
    en_subs = transcript.fetch()

    # TODO native?
    native = 'ru'
    try:
        native_subs = transcript_list.find_transcript([native]).fetch()
    except:
        # TODO who care?
        native_subs = transcript.translate(native).fetch()

    en_lines = [SubEvent(line["start"], line["duration"], line["text"]) for line in en_subs]
    native_lines = [SubEvent(line["start"], line["duration"], line["text"]) for line in native_subs]
    return _subs_to_tokens(en_lines, native_lines)


def get_tokens_from_subs_file(en_subs_file: str, native_subs_file: str) -> List[Token]:
    en_subs = pysubs2.load(en_subs_file, encoding="utf-8")
    native_subs = pysubs2.load(native_subs_file, encoding="utf-8") if native_subs_file else []

    en_lines = [SubEvent(line.start, line.duration, line.text) for line in en_subs]
    native_lines = [SubEvent(line.start, line.duration, line.text) for line in native_subs]
    return _subs_to_tokens(en_lines, native_lines)
