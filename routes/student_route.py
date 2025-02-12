import pydantic
import rapidfuzz
from fastapi import Request, status
from fastapi.responses import JSONResponse

from errors import AlreadyExistsException, NotFoundException
from models.student import Student
from .base_route import AbstractRoute, APIRoute


class StudentPutModel(pydantic.BaseModel):
	name: str
	age: int


class StudentPatchModel(pydantic.BaseModel):
	name: str | None = pydantic.Field(None)
	age: int | None = pydantic.Field(None)


class StudentGradesPatchModel(pydantic.BaseModel):
	course: int
	grades: list[int] = pydantic.Field(default_factory=list)


class StudentRoute(AbstractRoute):
	def init(self) -> None:
		self.base_path = "/api/student"
		self.routes = (
			APIRoute(f"{self.base_path}/", self.students_list, methods=("GET",)),
			APIRoute(f"{self.base_path}/search", self.students_search, methods=("GET",)),
			APIRoute(f"{self.base_path}/{"{student_id}"}", self.students_get, methods=("GET",)),
			APIRoute(f"{self.base_path}/{"{student_id}"}", self.students_put, methods=("PUT",)),
			APIRoute(f"{self.base_path}/{"{student_id}"}", self.students_patch, methods=("PATCH",)),
			APIRoute(f"{self.base_path}/{"{student_id}/grades"}", self.students_grades_patch, methods=("PATCH",)),
		)

	async def students_list(self, request: Request) -> JSONResponse:
		school = self.config.school

		students = [student.model_dump() for student in school.students.values()]

		return JSONResponse({"students": students}, status.HTTP_200_OK)

	async def students_search(self, request: Request, name: str) -> JSONResponse:
		school = self.config.school

		student_names = [fuzz[0] for fuzz in rapidfuzz.process.extract(name, choices=[student.name for student in school.students.values()], scorer=rapidfuzz.fuzz.partial_token_set_ratio, score_cutoff=30)]

		students = [student.model_dump() for student in school.students.values() if student.name in student_names]

		return JSONResponse({"students": students}, status.HTTP_200_OK)

	async def students_get(self, request: Request, student_id: int) -> JSONResponse:
		student = self.get_student(student_id)

		return JSONResponse(student.model_dump(), status.HTTP_200_OK)

	async def students_put(self, request: Request, student_id: int, student_put_model: StudentPutModel) -> JSONResponse:
		school = self.config.school

		if student := school.students.get(student_id):
			raise AlreadyExistsException(f"Student {student_id} already exists")

		student = Student(student_id=student_id, name=student_put_model.name, age=student_put_model.age, grades={})
		school.add_student(student)

		self.config.save()

		return JSONResponse(student.model_dump(), status.HTTP_200_OK)

	async def students_patch(self, request: Request, student_id: int, student_patch_model: StudentPatchModel) -> JSONResponse:
		student = self.get_student(student_id=student_id)

		for key, value in student_patch_model.model_dump(exclude_unset=True, exclude_defaults=True).items():
			setattr(student, key, value)

		self.config.save()

		return JSONResponse(student.model_dump(), status.HTTP_200_OK)

	async def students_grades_patch(self, request: Request, student_id: int, student_grades_patch_model: StudentGradesPatchModel) -> JSONResponse:
		student = self.get_student(student_id=student_id)
		course = self.get_course(student_grades_patch_model.course)

		if student.student_id not in course.enrolled_students:
			raise NotFoundException(f"Student is not enrolled in course {course.course_code}")

		if student_grades_patch_model.course not in student.grades:
			student.grades[course.course_code] = []

		student.grades[course.course_code] = student_grades_patch_model.grades

		self.config.save()

		return JSONResponse(student.model_dump(), status.HTTP_200_OK)
