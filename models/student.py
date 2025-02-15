import pydantic


class Student(pydantic.BaseModel):
	student_id: int
	name: str
	age: int
	grades: dict[int, list[int]] = pydantic.Field(default_factory=dict)

	def calculate_course_average_grades(self, course_id: int) -> float:
		try:
			grades = self.grades.get(course_id, [])
			return round(sum(grades) / len(grades), 2)
		except ZeroDivisionError:
			return 0.0

	def calculate_total_grade(self) -> int:
		return sum(sum(grades) for grades in self.grades.values())

	def calculate_total_average_grade(self) -> float:
		try:
			return round(self.calculate_total_grade() / sum(len(grades) for grades in self.grades.values()), 2)
		except ZeroDivisionError:
			return 0.0


class GraduateStudent(Student):
	thesis_topic: str
