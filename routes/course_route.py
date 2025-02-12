from typing import Annotated

from fastapi import Body, Path, Request, status
from fastapi.responses import JSONResponse

from models.course import Course
from util.errors import AlreadyExistsException, NotFoundException

from .base_route import AbstractRoute, APIRoute


class CourseRoute(AbstractRoute):
	def init(self) -> None:
		self.base_path = "/api/course"
		self.routes = (
			APIRoute(f"{self.base_path}/", self.courses_list, methods=("GET",), name="Courses list", description="Returns a list of all courses"),
			APIRoute(f"{self.base_path}/{'{course_id}'}", self.courses_get, methods=("GET",), name="Course get", description="Returns a course by ID"),
			APIRoute(f"{self.base_path}/{'{course_id}'}", self.courses_put, methods=("PUT",), name="Course put", description="Creates a new course"),
			APIRoute(f"{self.base_path}/{'{course_id}'}", self.courses_patch, methods=("PATCH",), name="Course update", description="Updates a course by ID"),
			APIRoute(f"{self.base_path}/{'{course_id}'}/enroll_student", self.courses_enroll_student, methods=("PUT",), name="Course enroll student", description="Enrolls a student to a course"),
			APIRoute(f"{self.base_path}/{'{course_id}'}/enroll_student", self.courses_delete_student, methods=("DELETE",), name="Course delete student", description="Deletes a student from a course"),
		)

	async def courses_list(self, request: Request) -> JSONResponse:
		school = self.config.school

		courses = [course.model_dump() for course in school.courses.values()]

		return JSONResponse({"courses": courses}, status.HTTP_200_OK)

	async def courses_get(self, request: Request, course_id: int) -> JSONResponse:
		course = self.get_course(course_id)

		return JSONResponse(course.model_dump(), status.HTTP_200_OK)

	async def courses_put(self, request: Request, course_id: Annotated[int, Path(title="Course ID")], course_name: Annotated[str, Body(title="Course Name", embed=True)]) -> JSONResponse:
		school = self.config.school

		if course := school.courses.get(course_id):
			raise AlreadyExistsException(f"Course {course_id} already exists")

		course = Course(course_code=course_id, course_name=course_name, enrolled_students=set())
		school.add_course(course)

		self.config.save()

		return JSONResponse(course.model_dump(), status.HTTP_200_OK)

	async def courses_patch(self, request: Request, course_id: Annotated[int, Path(title="Course ID")], course_name: Annotated[str, Body(title="Course Name", embed=True)]) -> JSONResponse:
		course = self.get_course(course_id)

		course.course_name = course_name

		self.config.save()

		return JSONResponse(course.model_dump(), status.HTTP_200_OK)

	async def courses_enroll_student(self, request: Request, course_id: Annotated[int, Path(title="Course ID")], student_id: Annotated[int, Body(title="Student ID", embed=True)]) -> JSONResponse:
		course = self.get_course(course_id)
		student = self.get_student(student_id)

		if student.student_id in course.enrolled_students:
			raise AlreadyExistsException(f"Student {student.student_id} is already enrolled to course {course_id}")

		course.enrolled_students.add(student.student_id)

		self.config.save()

		return JSONResponse(course.model_dump(), status.HTTP_200_OK)

	async def courses_delete_student(self, request: Request, course_id: Annotated[int, Path(title="Course ID")], student_id: Annotated[int, Body(title="Student ID", embed=True)]) -> JSONResponse:
		course = self.get_course(course_id)
		student = self.get_student(student_id)

		if student.student_id not in course.enrolled_students:
			raise NotFoundException(f"Student {student.student_id} is not enrolled to course {course_id}")

		course.enrolled_students.remove(student.student_id)

		self.config.save()

		return JSONResponse(course.model_dump(), status.HTTP_200_OK)
