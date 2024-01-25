import asyncio
import time

from aiohttp import ClientSession

from utils.utils import timed_it


async def get_website_detail(session: ClientSession, url: str) -> dict:
    """
    Корутина делает запрос к сайту возвращается словарь с кодом статуса и временем загрузки

    :param session: ClientSession
    :param url: str
    :return: dict
    """

    start = time.time()
    async with session.get(url) as response:
        end = time.time()
        return {
            'status_code': response.status,
            'time': end - start
        }


@timed_it('script_loading')
async def make_website_requests(url: str, times: int) -> dict:
    """
    Главная сопрограмма сервиса.
    Осуществляет times запросов к сайту и считает среднее время запросов.

    :param url: str
    :param times: int
    :return: dict
    """

    async with ClientSession() as session:
        requests = [get_website_detail(session, url) for _ in range(times)]
        results = await asyncio.gather(*requests, return_exceptions=True)

        successful = [result for result in results if not isinstance(result, Exception)]
        failed = [result for result in results if isinstance(result, Exception)]

        total_successful, total_failed = len(successful), len(failed)

        answer = {
            'meta': {
                'website': url,
                'total_requests': total_successful + total_failed,
                'successful_requests': total_successful,
                'failed_requests': total_failed,
            }
        }

        if total_successful:
            avg_time_loading = sum([item.get('time') for item in successful]) / total_successful
            answer['meta']['average_website_loading'] = f'{avg_time_loading:.4f}'

        return answer
