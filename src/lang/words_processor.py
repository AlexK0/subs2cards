from typing import List, Dict

from src.lang.token import Token
from src.lang.phrasal_verbs import get_phrasal_verbs


def _add_words_from(dest: Dict[str, Token], tokens: List[Token]) -> Dict[str, Token]:
    for token in tokens:
        if not token.is_interesting():
            continue

        fixed_token = token.lemmatize()
        if not fixed_token.is_interesting():
            continue

        if fixed_token.word not in dest:
            dest[fixed_token.word] = fixed_token
        else:
            other_token = dest[fixed_token.word]
            if other_token.is_context_worse_then(fixed_token):
                fixed_token.ref_counter += other_token.ref_counter
                dest[fixed_token.word] = fixed_token
            else:
                other_token.ref_counter += fixed_token.ref_counter

    return dest


def _remove_similar_words(words: Dict[str, Token]) -> Dict[str, Token]:
    for word in list(words):
        word_without_end = words[word].try_remove_end()
        if word_without_end and word_without_end in words:
            words[word_without_end].ref_counter += words[word].ref_counter
            del words[word]

    return words


def process_words(words: List[Token]) -> Dict[str, Token]:
    phrasal_verbs = get_phrasal_verbs(words)

    words = _add_words_from({}, words)
    words = _add_words_from(words, phrasal_verbs)
    return _remove_similar_words(words)
