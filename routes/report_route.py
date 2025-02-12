from fastapi import Request
from fastapi.responses import HTMLResponse

from models.student import Student
from util.errors import NotFoundException

from .base_route import AbstractRoute, Route


class ReportRoute(AbstractRoute):
	def init(self) -> None:
		self.base_path = "/report"
		self.routes = (
			Route(f"{self.base_path}/students", self.students, methods=("GET",)),
			Route(f"{self.base_path}/student/{'{student_id}'}/grades", self.student_grades, methods=("GET",)),
			Route(f"{self.base_path}/course/{'{course_id}'}/grades", self.course_grades, methods=("GET",)),
		)

	async def students(self, request: Request) -> HTMLResponse:
		school = self.config.school

		students = []
		for student in school.students.values():
			data = student.model_dump()
			data["student_id"] = f"<a href='{self.base_path}/student/{student.student_id}/grades'>{data['student_id']}</a>"
			data["courses"] = ", ".join(
				[f"<a href='{self.base_path}/course/{course.course_code}/grades'>{course.course_name}</a>" for course in school.get_student_courses(student_id=student.student_id)]
			)
			data["total_average_grade"] = student.calculate_total_average_grade()
			students.append(data)

		return self.templates.TemplateResponse(
			"report.html",
			{
				"request": request,
				"fields": [name for name, field in Student.model_fields.items() if all(i not in field.annotation.mro() for i in (list, dict))]  # pyright: ignore [reportOptionalMemberAccess]
				+ ["courses", "total_average_grade"],
				"rows": students,
			},
		)

	async def student_grades(self, request: Request) -> HTMLResponse:
		school = self.config.school

		student = self.get_student(int(request.path_params.get("student_id")))

		grades = {}
		grades_average = {}
		for course in school.get_student_courses(student_id=student.student_id):
			course_grades = student.grades.get(course.course_code, [])
			grades[course.course_name] = ", ".join([str(grade) for grade in course_grades])
			grades_average[course.course_name] = student.calculate_course_average_grades(course.course_code)

		grades["total"] = student.calculate_total_grade()
		grades_average["total"] = student.calculate_total_average_grade()

		return self.templates.TemplateResponse("report.html", {"request": request, "fields": list(grades.keys()), "rows": [grades, grades_average]})

	async def course_grades(self, request: Request) -> HTMLResponse:
		course = self.get_course(int(request.path_params.get("course_id")))

		grades = []

		for student_id in course.enrolled_students:
			try:
				student = self.get_student(student_id)
			except NotFoundException:
				continue

			data = {}

			course_grades = student.grades.get(course.course_code, [])
			data["student_id"] = f"<a href='{self.base_path}/student/{student.student_id}/grades'>{student.student_id}</a>"
			data["name"] = student.name
			data["grades"] = ", ".join([str(grade) for grade in course_grades])
			data["average"] = student.calculate_course_average_grades(course.course_code)

			grades.append(data)

		return self.templates.TemplateResponse("report.html", {"request": request, "fields": ["student_id", "name", "grades", "average"], "rows": grades})
