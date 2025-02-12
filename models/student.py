import pydantic


class Student(pydantic.BaseModel):
	student_id: int
	name: str
	age: int
	grades: dict[int, list[int]] = pydantic.Field(default_factory=dict)

	def calculate_course_average_grades(self, course_id: int) -> float:
		try:
			return sum(self.grades[course_id]) / len(self.grades[course_id])
		except ZeroDivisionError:
			return 0.0

	def calculate_total_grade(self) -> int:
		return sum(sum(grades) for grades in self.grades.values())

	def calculate_total_average_grade(self) -> float:
		try:
			return self.calculate_total_grade() / sum(len(grades) for grades in self.grades.values())
		except ZeroDivisionError:
			return 0.0


class GraduateStudent(Student):
	thesis_topic: str
