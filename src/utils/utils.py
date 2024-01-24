import time
import re

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
