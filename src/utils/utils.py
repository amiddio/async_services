import os
import time
import re

from collections import Counter
from typing import Callable, Any
from urllib.parse import urlparse


def logging_action(s: str) -> None:
    """
    Выводим в консоль результат работы скрипта

    :param s: str
    :return: None
    """

    if os.environ.get('LOGGING') in ('True', '1', 'On', 'on'):
        print(s)


def is_valid_url(url: str) -> bool:
    """
    Проверка на валидность url-а

    :param url: str
    :return: bool
    """

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def timed_it(label: str) -> Callable:
    """
    Декоратор фиксирует время работы ф-ии и добавляет его в результат,
    если результат является словарем

    :param label: str
    :return: Callable
    """

    def inner(func: Callable):
        async def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            result = await func(*args, **kwargs)
            if isinstance(result, dict):
                result['meta'][label] = f'{time.time() - start:.4f}'
            return result

        return wrapper

    return inner


def get_data_chunk(data: str, size: int) -> str:
    """
    Генератор дробит входящие данные на куски размерами size

    :param data: str
    :param size: int
    :return: str
    """

    for i in range(0, len(data), size):
        yield data[i:i + size]


def remove_extra_whitespace(text: str) -> str:
    """
    Функция избавляет от избыточных пробелов

    :param text: str
    :return: str
    """

    return ' '.join(text.split())


def remove_punctuation(text: str) -> str:
    """
    Функция удаления знаков препинания

    :param text: str
    :return: str
    """

    return re.sub(r'[^\w\s]', '', text)


def set_lowercase(text: str) -> str:
    """
    Функция переводит текст в нижний регистр

    :param text: str
    :return: str
    """

    return text.lower()


def map_cleaner(text: str, chunk_num: int) -> str:
    """
    Функция проводит необходимую очистку текста:
    - удаляются знаки препинания
    - избавляемся от лишних пробелов
    - переводим буквы в нижний регистр

    :param text: str
    :param chunk_num: int
    :return: str
    """

    length = len(text)
    logging_action(f"Start cleaning text chunk {chunk_num} ({length})")
    text = remove_punctuation(text)
    text = remove_extra_whitespace(text)
    text = set_lowercase(text)
    logging_action(f"End cleaning text chunk {chunk_num} ({length})")
    return text


def map_words_frequencies(text: str, chunk_num: int) -> dict:
    """
    Функция создает словарь частоты повторений слов, из переданной строки

    :param text: str
    :param chunk_num: int
    :return: dict
    """

    logging_action(f"Start creating words frequencies from chunk {chunk_num}")
    words_freq_dct = Counter(text.split())
    logging_action(f"End creating words frequencies from chunk {chunk_num}. Done for {len(words_freq_dct)} words.")
    return words_freq_dct


def merge_words_frequencies(dict_a: dict, dict_b: dict) -> dict:
    """
    Функция склеивает два словаря, и суммирует значения повторений

    :param dict_a: dict
    :param dict_b: dict
    :return: dict
    """

    len_dict_b = len(dict_b)
    logging_action(f"Start merging dictionaries {len(dict_a)} and {len_dict_b}")
    for word in dict_b:
        if word in dict_a:
            dict_a[word] += dict_b[word]
        else:
            dict_a[word] = dict_b[word]
    logging_action(f"End merging dictionaries {len(dict_a)} and {len_dict_b}")
    return dict_a
