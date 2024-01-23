from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

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
