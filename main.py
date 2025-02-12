from typing import Type

import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import routes
from config import Config
from routes.base_route import AbstractRoute


app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

config = Config("config.json")
config.read()


for route_name in routes.__all__:
    route_cls: Type[AbstractRoute] = getattr(routes, route_name)
    route = route_cls(app, templates, config)


@app.route("/")
async def _index(request: fastapi.Request):
    return fastapi.responses.PlainTextResponse("hello, world!", status_code=fastapi.status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
