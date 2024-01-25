from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from parse_text.coros import parser
from utils.utils import is_valid_url
from website_speed.coros import make_website_requests

routes = web.RouteTableDef()


@routes.get('/website_speed')
async def website_speed(request: Request) -> Response:
    """
    Роут определяет среднее время загрузки сайта, на основании нескольких запросов.
    Необходимо передать GET запрос со следующими значениями:
    - url: урл сайта с протоколом (например https://example.com)
    - times: количество запросов к сайту

    :param request: Request
    :return: Response
    """

    url: str = request.query.get('url').strip()
    times: int = int(request.query.get('times', 100))

    if not is_valid_url(url):
        return web.HTTPBadRequest()

    result = await make_website_requests(url=url, times=times)
    return web.json_response(result)


@routes.post('/parse_text')
async def parse_text(request: Request) -> Response:
    """
    Роут парсит сайты с книгами в формате txt, и формирует словарь с частотой повторения всех слов.
    Необходимо передать POST запрос со следующими значениями:
    - urls: список урл-ов на txt книги через запятую
    - limit: ограничение слов в результате. 0 (значение по умолчанию) вернет все слова
    - exclude_words_le: исключает слова из результата меньше или равно переданой длины.
                        например, если передать 3, то из результата будут исключены слова длиной <= 3.
                        0 (значение по умолчанию) вернет все слова
    - include_words: список слов через запятую которые будут в результате. Пустая строка по умолчанию.

    :param request: Request
    :return: Response
    """

    post_data = await request.post()

    urls: str = post_data.get('urls', '').strip()
    limit: int = int(post_data.get('limit', 0))
    exclude_words_le: int = int(post_data.get('exclude_words_le', 0))
    include_words: str = post_data.get('include_words_only', '').strip()

    if not urls:
        return web.HTTPBadRequest()
    else:
        urls: list = urls.split(',')
        if not all([is_valid_url(url) for url in urls]):
            return web.HTTPBadRequest()

    if include_words:
        include_words: list = include_words.split(',')

    result = await parser(urls=urls, limit=limit, exclude_words_le=exclude_words_le, include_words=include_words)
    return web.json_response(result)
