import asyncio
import functools

from concurrent.futures import ProcessPoolExecutor
from operator import itemgetter
from typing import Callable
from aiohttp import ClientSession

from utils.utils import get_data_chunk, map_cleaner, timed_it, map_words_frequencies, merge_words_frequencies, \
    logging_action

PARTITION_SIZE = 50_000


async def get_text(session: ClientSession, url: str) -> dict:
    logging_action(f"Start loading website {url}")
    async with session.get(url) as response:
        if response.status == 200:
            text = await response.text()
            logging_action(f"Text from website {url} received")
            return {
                'url': url,
                'length': len(text),
                'data': text,
            }
        else:
            logging_action(f"Text from website {url} loading failed")
            raise RuntimeError('Expected 200')


@timed_it('content_loading_sec')
async def get_content(urls: list) -> dict:
    async with ClientSession() as session:
        requests = [get_text(session, url) for url in urls]
        results = await asyncio.gather(*requests, return_exceptions=True)

        successful = [result for result in results if not isinstance(result, Exception)]

        answer = {
            'meta': {
                'urls': []
            },
            'data': ''
        }
        _data = []

        for item in successful:
            s = f"{item['url']} (length: {item['length']})"
            answer['meta']['urls'].append(s)
            _data.append(item['data'])
        answer['data'] = ''.join(_data)

        return answer


async def map_reduce(data: dict, map_func: Callable, reduce_func: Callable) -> dict:
    loop = asyncio.get_event_loop()
    tasks = []

    with ProcessPoolExecutor() as pool:
        for num, chunk in enumerate(get_data_chunk(data, PARTITION_SIZE), start=1):
            task = loop.run_in_executor(pool, functools.partial(map_func, chunk, num))
            tasks.append(task)

        intermediate_results = await asyncio.gather(*tasks)
        final_result = functools.reduce(reduce_func, intermediate_results)

    return final_result


@timed_it('content_cleaning_sec')
async def clean_text(data: dict) -> dict:
    data['data'] = await map_reduce(
        data=data['data'], map_func=map_cleaner, reduce_func=lambda a, b: a + b
    )
    return data


@timed_it('words_frequencies_sec')
async def get_words_frequencies(data: dict) -> dict:
    data['data'] = await map_reduce(
        data=data['data'], map_func=map_words_frequencies, reduce_func=merge_words_frequencies
    )
    return data


@timed_it('dictionary_sort_sec')
async def sort_dictionary(data: dict) -> dict:
    logging_action(f"Start sorting words frequencies")
    data['data'] = dict(sorted(data['data'].items(), key=itemgetter(1), reverse=True))
    logging_action(f"End sorting words frequencies")
    return data


async def filter_result(data: dict, limit: int, exclude_words_le: int, include_words: list) -> dict:
    if not include_words:
        if exclude_words_le > 0:
            data = {k: v for k, v in data.items() if len(k) > exclude_words_le}
        if limit > 0:
            data = dict(list(data.items())[:limit])
    else:
        data = {k: v for k, v in data.items() if k in include_words}
    return data


async def parser(urls: list, limit: int, exclude_words_le: int, include_words: list) -> dict:
    data = await get_content(urls=urls)
    data = await clean_text(data=data)
    data = await get_words_frequencies(data=data)
    data = await sort_dictionary(data=data)
    data['data'] = await filter_result(
        data=data['data'], limit=limit, exclude_words_le=exclude_words_le, include_words=include_words
    )
    return data
