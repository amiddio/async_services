from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

routes = web.RouteTableDef()

PORT = 8008


@routes.get('/website_speed')
async def website_speed(request: Request) -> Response:
    result = {
        'answer': 'Hello world!'
    }

    return web.json_response(result)


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=PORT)
