import pydantic
from fastapi import Request, status
from fastapi.responses import JSONResponse

from errors import AlreadyExistsException, NotFoundException
from models.course import Course
from .base_route import AbstractRoute, Route


class CoursePutModel(pydantic.BaseModel):
	name: str


class CoursePatchModel(pydantic.BaseModel):
	name: str | None = pydantic.Field(None)


class CourseEnrollStudentModel(pydantic.BaseModel):
	student_id: int


class CourseDeleteStudentModel(pydantic.BaseModel):
	student_id: int


class CourseRoute(AbstractRoute):
	def init(self) -> None:
		self.base_path = "/course"
		self.routes = (
			Route(f"{self.base_path}/", self.courses_list, methods=("GET",)),
			Route(f"{self.base_path}/{"{course_id}"}", self.courses_get, methods=("GET",)),
			Route(f"{self.base_path}/{"{course_id}"}", self.courses_put, methods=("PUT",)),
			Route(f"{self.base_path}/{"{course_id}"}", self.courses_patch, methods=("PATCH",)),
			Route(f"{self.base_path}/{"{course_id}"}/enroll_student", self.courses_enroll_student, methods=("PUT",)),
			Route(f"{self.base_path}/{"{course_id}"}/enroll_student", self.courses_delete_student, methods=("DELETE",)),
		)

	async def courses_list(self, request: Request) -> JSONResponse:
		school = self.config.school

		courses = [course.model_dump() for course in school.courses.values()]

		return JSONResponse({"courses": courses}, status.HTTP_200_OK)

	async def courses_get(self, request: Request, course_id: int) -> JSONResponse:
		course = self.get_course(course_id)

		return JSONResponse(course.model_dump(), status.HTTP_200_OK)

	async def courses_put(self, request: Request, course_id: int, course_put_model: CoursePutModel) -> JSONResponse:
		school = self.config.school

		if course := school.courses.get(course_id):
			raise AlreadyExistsException(f"Course {course_id} already exists")

		course = Course(course_code=course_id, course_name=course_put_model.name, enrolled_students=set())
		school.add_course(course)

		self.config.save()

		return JSONResponse(course.model_dump(), status.HTTP_200_OK)

	async def courses_patch(self, request: Request, course_id: int, course_patch_model: CoursePatchModel) -> JSONResponse:
		course = self.get_course(course_id=course_id)

		for key, value in course_patch_model.model_dump(exclude_unset=True, exclude_defaults=True).items():
			setattr(course, key, value)

		self.config.save()

		return JSONResponse(course.model_dump(), status.HTTP_200_OK)

	async def courses_enroll_student(self, request: Request, course_id: int, course_enroll_student_model: CourseEnrollStudentModel) -> JSONResponse:
		course = self.get_course(course_id=course_id)
		student = self.get_student(student_id=course_enroll_student_model.student_id)

		if student.student_id in course.enrolled_students:
			raise AlreadyExistsException(f"Student {student.student_id} is already enrolled to course {course_id}")

		course.enrolled_students.add(student.student_id)

		self.config.save()

		return JSONResponse(course.model_dump(), status.HTTP_200_OK)

	async def courses_delete_student(self, request: Request, course_id: int, course_delete_student_model: CourseDeleteStudentModel) -> JSONResponse:
		course = self.get_course(course_id=course_id)
		student = self.get_student(student_id=course_delete_student_model.student_id)

		if student.student_id not in course.enrolled_students:
			raise NotFoundException(f"Student {student.student_id} is not enrolled to course {course_id}")

		course.enrolled_students.remove(student.student_id)

		self.config.save()

		return JSONResponse(course.model_dump(), status.HTTP_200_OK)
