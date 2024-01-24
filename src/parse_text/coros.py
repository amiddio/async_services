import asyncio
import functools
from concurrent.futures import ProcessPoolExecutor

import aiohttp.web
from aiohttp import ClientSession

from utils.utils import get_data_chunk, map_cleaner, timed_it

PARTITION_SIZE = 50_000


async def get_text(session: ClientSession, url: str) -> dict:
    print(f"Start loading website {url}")
    async with session.get(url) as response:
        if response.status == 200:
            text = await response.text()
            print(f"Text from website {url} received")
            return {
                'url': url,
                'length': len(text),
                'data': text,
            }
        else:
            print(f"Text from website {url} loading failed")
            raise RuntimeError('Expected 200')


@timed_it('content_loading_sec')
async def get_content(urls: list) -> dict:
    # https://tululu.org/txt.php?id=77440,https://tululu.org/txt.php?id=77441,https://tululu.org/txt.php?id=77442,https://tululu.org/txt.php?id=77443
    async with ClientSession() as session:
        requests = [get_text(session, url) for url in urls]
        results = await asyncio.gather(*requests, return_exceptions=True)

        successful = [result for result in results if not isinstance(result, Exception)]

        answer = {'meta': [], 'data': ''}
        data = []

        for item in successful:
            s = f"{item['url']} (length: {item['length']})"
            answer['meta'].append(s)
            data.append(item['data'])
        answer['data'] = ''.join(data)

        return answer


@timed_it('content_cleaning_sec')
async def clean_text(data: dict) -> dict:
    loop = asyncio.get_event_loop()
    tasks = []

    with ProcessPoolExecutor() as pool:
        for num, chunk in enumerate(get_data_chunk(data['data'], PARTITION_SIZE), start=1):
            task = loop.run_in_executor(pool, functools.partial(map_cleaner, chunk, num))
            tasks.append(task)

        intermediate_results = await asyncio.gather(*tasks)
        final_result = functools.reduce(lambda a, b: a + b, intermediate_results)

    data['data'] = final_result

    return data


async def parser(urls: list):
    data = await get_content(urls=urls)
    data = await clean_text(data=data)

