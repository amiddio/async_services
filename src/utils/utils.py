import time
import re

from collections import Counter
from typing import Callable, Any
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def timed_it(label: str) -> Callable:
    def inner(func: Callable):
        async def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            result = await func(*args, **kwargs)
            if isinstance(result, dict):
                result[label] = f'{time.time() - start:.4f}'
            return result

        return wrapper

    return inner


def get_data_chunk(data: str, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]


def remove_extra_whitespace(text: str) -> str:
    return ' '.join(text.split())


def remove_punctuation(text: str) -> str:
    return re.sub(r'[^\w\s]', '', text)


def set_lowercase(text: str) -> str:
    return text.lower()


def map_cleaner(text: str, chunk_num: int) -> str:
    length = len(text)
    print(f"Start cleaning text chunk {chunk_num} ({length})")
    text = remove_punctuation(text)
    text = remove_extra_whitespace(text)
    text = set_lowercase(text)
    print(f"End cleaning text chunk {chunk_num} ({length})")
    return text


def map_words_frequencies(text: str, chunk_num: int) -> dict:
    print(f"Start creating words frequencies from chunk {chunk_num}")
    words_freq_dct = Counter(text.split())
    print(f"End creating words frequencies from chunk {chunk_num}. Done for {len(words_freq_dct)} words.")
    return words_freq_dct


def merge_words_frequencies(dict_a: dict, dict_b: dict) -> dict:
    len_dict_b = len(dict_b)
    print(f"Start merging dictionaries {len(dict_a)} and {len_dict_b}")
    for word in dict_b:
        if word in dict_a:
            dict_a[word] += dict_b[word]
        else:
            dict_a[word] = dict_b[word]
    print(f"End merging dictionaries {len(dict_a)} and {len_dict_b}")
    return dict_a
