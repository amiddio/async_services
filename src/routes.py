from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from parse_text.coros import parser
from utils.utils import is_valid_url
from website_speed.coros import make_website_requests

routes = web.RouteTableDef()


@routes.get('/website_speed')
async def website_speed(request: Request) -> Response:
    url: str = request.query.get('url').strip()
    times: int = int(request.query.get('times', 100))

    if not is_valid_url(url):
        return web.HTTPBadRequest()

    result = await make_website_requests(url=url, times=times)
    return web.json_response(result)


@routes.post('/parse_text')
async def parse_text(request: Request) -> Response:
    post_data = await request.post()

    urls: str = post_data.get('urls', '').strip()
    limit: int = int(post_data.get('limit', 0))
    exclude_words_le: int = int(post_data.get('exclude_words_le', 0))
    include_words: str = post_data.get('include_words_only', '').strip()

    if not urls:
        return web.HTTPBadRequest()
    else:
        urls: list = urls.split(',')

    if include_words:
        include_words: list = include_words.split(',')

    if not all([is_valid_url(url) for url in urls]):
        return web.HTTPBadRequest()

    result = await parser(urls=urls, limit=limit, exclude_words_le=exclude_words_le, include_words=include_words)
    return web.json_response(result)
