from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

import fastapi
from fastapi.datastructures import Default

from config import Config


@dataclass()
class BaseRoute():
	path: str
	endpoint: Callable[..., Any]


@dataclass()
class Route(BaseRoute):
	methods: Sequence[str] = field(default_factory=lambda : ("GET",))
	response_model: Any = field(default_factory=lambda : Default(None))
	include_in_schema: bool = True
	deprecated: bool = False


@dataclass()
class WebSocketRoute(BaseRoute):
	pass


class AbstractRoute():
	def __init__(self, app: fastapi.FastAPI, config: Config, *args, **kwargs):
		self._app = app
		self._config = config
		self._routes = ()

		self.init(*args, **kwargs)

		for route in self.routes:
			if isinstance(route, WebSocketRoute):
				self._app.add_websocket_route(route.path, route.endpoint)
			elif isinstance(route, Route):
				self._app.add_api_route(route.path, route.endpoint, methods=route.methods, response_model=route.response_model, deprecated=route.deprecated, include_in_schema=route.include_in_schema)

	def init(self, *args, **kwargs) -> None:
		pass

	@property
	def app(self) -> fastapi.FastAPI:
		return self._app

	@property
	def config(self) -> Config:
		return self._config

	@property
	def routes(self) -> Sequence[Route]:
		return self._routes

	@routes.setter
	def routes(self, value: Sequence[Route]):
		self._routes = value
