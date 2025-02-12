from typing import Annotated

import rapidfuzz
from fastapi import Body, Path, Request, status
from fastapi.responses import JSONResponse

from models.student import Student
from util.errors import AlreadyExistsException, NotFoundException

from .base_route import AbstractRoute, APIRoute


class StudentRoute(AbstractRoute):
	def init(self) -> None:
		self.base_path = "/api/student"
		self.routes = (
			APIRoute(f"{self.base_path}/", self.students_list, methods=("GET",), name="Students list", description="Returns a list of all students"),
			APIRoute(
				f"{self.base_path}/search",
				self.students_search,
				methods=("GET",),
				name="Students search",
				description="Returns a list of students by name using normalized partial token set ratio Levenshtein distance",
			),
			APIRoute(f"{self.base_path}/{'{student_id}'}", self.students_get, methods=("GET",), name="Student get", description="Returns a student by ID"),
			APIRoute(f"{self.base_path}/{'{student_id}'}", self.students_put, methods=("PUT",), name="Student put", description="Creates a new student"),
			APIRoute(f"{self.base_path}/{'{student_id}'}", self.students_patch, methods=("PATCH",), name="Student update", description="Updates a student by ID"),
			APIRoute(f"{self.base_path}/{'{student_id}/grades'}", self.students_grades_patch, methods=("PATCH",), name="Student update", description="Updates a student by ID"),
		)

	async def students_list(self, request: Request) -> JSONResponse:
		school = self.config.school

		students = [student.model_dump() for student in school.students.values()]

		return JSONResponse({"students": students}, status.HTTP_200_OK)

	async def students_search(self, request: Request, name: str) -> JSONResponse:
		school = self.config.school

		student_names = [
			fuzz[0] for fuzz in rapidfuzz.process.extract(name, choices=[student.name for student in school.students.values()], scorer=rapidfuzz.fuzz.partial_token_set_ratio, score_cutoff=30)
		]

		students = [student.model_dump() for student in school.students.values() if student.name in student_names]

		return JSONResponse({"students": students}, status.HTTP_200_OK)

	async def students_get(self, request: Request, student_id: Annotated[int, Path(title="Student ID")]) -> JSONResponse:
		student = self.get_student(student_id)

		return JSONResponse(student.model_dump(), status.HTTP_200_OK)

	async def students_put(
		self,
		request: Request,
		student_id: Annotated[int, Path(title="Student ID")],
		student_name: Annotated[str, Body(title="Student Name", embed=True)],
		student_age: Annotated[int, Body(title="Student Age", embed=True)],
	) -> JSONResponse:
		school = self.config.school

		if student := school.students.get(student_id):
			raise AlreadyExistsException(f"Student {student_id} already exists")

		student = Student(student_id=student_id, name=student_name, age=student_age, grades={})
		school.add_student(student)

		self.config.save()

		return JSONResponse(student.model_dump(), status.HTTP_200_OK)

	async def students_patch(
		self,
		request: Request,
		student_id: Annotated[int, Path(title="Student ID")],
		student_name: Annotated[str | None, Body(title="Student Name", embed=True)],
		student_age: Annotated[int | None, Body(title="Student Age", embed=True)],
	) -> JSONResponse:
		student = self.get_student(student_id)

		if student_name is not None:
			student.name = student_name

		if student_age is not None:
			student.age = student_age

		self.config.save()

		return JSONResponse(student.model_dump(), status.HTTP_200_OK)

	async def students_grades_patch(
		self,
		request: Request,
		student_id: Annotated[int, Path(title="Student ID")],
		course_code: Annotated[int, Body(title="Course Code", embed=True)],
		grades: Annotated[list[int], Body(title="Grades", description="Overwrites all grades for course", embed=True)],
	) -> JSONResponse:
		student = self.get_student(student_id)
		course = self.get_course(course_code)

		if student.student_id not in course.enrolled_students:
			raise NotFoundException(f"Student is not enrolled in course {course.course_code}")

		if course_code not in student.grades:
			student.grades[course.course_code] = []

		student.grades[course.course_code] = grades

		self.config.save()

		return JSONResponse(student.model_dump(), status.HTTP_200_OK)
