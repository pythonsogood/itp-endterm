from fastapi import Request, status
from fastapi.responses import JSONResponse

from errors import NotFoundException
from .base_route import AbstractRoute, Route


class CourseRoute(AbstractRoute):
	def init(self) -> None:
		self.base_path = "/course"
		self.routes = (
			Route(f"{self.base_path}/", self.courses_list, methods=("GET",)),
			Route(f"{self.base_path}/{"{course_id}"}", self.courses_get, methods=("GET",)),
		)

	async def courses_list(self, request: Request) -> JSONResponse:
		school = self.config.school
		courses = [course.model_dump() for course in school.courses.values()]
		return JSONResponse({"courses": courses}, status.HTTP_200_OK)

	async def courses_get(self, request: Request) -> JSONResponse:
		school = self.config.school
		course_id = request.path_params["course_id"]
		course = school.courses.get(course_id)
		if course is None:
			raise NotFoundException(f"Course {course_id} not found")
		return JSONResponse(course.model_dump(), status.HTTP_200_OK)
