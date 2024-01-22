import asyncio
import time

from aiohttp import ClientSession


async def get_website_detail(session: ClientSession, url: str) -> dict:
    start = time.time()
    async with session.get(url) as response:
        end = time.time()
        return {
            'status_code': response.status,
            'time': end - start
        }


async def make_website_requests(url: str, times: int):
    async with ClientSession() as session:
        requests = [get_website_detail(session, url) for _ in range(times)]
        results = await asyncio.gather(*requests, return_exceptions=True)

        successful = [result for result in results if not isinstance(result, Exception)]
        failed = [result for result in results if isinstance(result, Exception)]

        total_successful, total_failed = len(successful), len(failed)

        avg_time_loading = sum([item.get('time') for item in successful]) / total_successful

        return {
            'website': url,
            'total_requests': total_successful + total_failed,
            'successful_requests': total_successful,
            'failed_requests': total_failed,
            'average_website_loading_sec': f'{avg_time_loading:.4f}',
        }