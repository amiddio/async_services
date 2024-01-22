from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from utils.utils import clean_url
from website_speed.coros import make_website_requests

routes = web.RouteTableDef()


@routes.get('/website_speed')
async def website_speed(request: Request) -> Response:
    url: str = clean_url(request.query.get('url'))
    times: int = int(request.query.get('times', 100))
    result = await make_website_requests(url=url, times=times)
    return web.json_response(result)
