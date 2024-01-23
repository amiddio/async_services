import os

from dotenv import load_dotenv
from aiohttp import web

from routes import routes

load_dotenv()

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=int(os.environ.get('PORT')))
