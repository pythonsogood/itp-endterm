import orjson
import os
from typing import TypeAlias

from .school import School


PathType: TypeAlias = os.PathLike[str] | os.PathLike[bytes]


class Config():
	def __init__(self, file_path: PathType):
		self._file_path = file_path
		self._config = {}
		self._school = None

	@property
	def file_path(self) -> PathType:
		return self._file_path

	@file_path.setter
	def file_path(self, value: PathType):
		self._file_path = value

	@property
	def school(self) -> School:
		return self._school

	def read(self):
		with open(self._file_path, "rb") as f:
			self._config = orjson.loads(f.read())
		self._school = School(**self._config)

	def reload(self):
		self.read()

	def save(self):
		with open(self._file_path, "wb") as f:
			f.write(orjson.dumps(self._config, option=orjson.OPT_INDENT_2))
