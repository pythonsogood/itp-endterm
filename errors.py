from fastapi import HTTPException
from fastapi import status as status_codes


class RequestException(HTTPException):
	def __init__(self, message: str, status_code: int, headers: dict=None):
		super().__init__(status_code, message, headers)


class NotFoundException(RequestException):
	def __init__(self, message: str):
		super().__init__(message, status_codes.HTTP_404_NOT_FOUND)


class AlreadyExistsException(RequestException):
	def __init__(self, message: str):
		super().__init__(message, status_codes.HTTP_400_BAD_REQUEST)
