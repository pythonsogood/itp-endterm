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
		if self._school is None:
			raise ValueError("Config is not initialized!")
		return self._school

	def read(self):
		if os.path.exists(self._file_path):
			with open(self._file_path, "rb") as f:
				try:
					self._config = orjson.loads(f.read())
				except orjson.JSONDecodeError as e:
					print(f"JSON Decode error: {e.args}")
					self._config = {}
		else:
			self._config = {}

		self._school = School(**self._config.get("school", {}))

	def reload(self):
		self.read()

	def save(self):
		self._config["school"] = self.school.model_dump(mode="json")

		with open(self._file_path, "wb") as f:
			f.write(orjson.dumps(self._config, option=orjson.OPT_INDENT_2))
