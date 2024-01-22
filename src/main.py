from aiohttp import web

from routes import routes

PORT = 8008

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=PORT)
