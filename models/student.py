import pydantic


class Student(pydantic.BaseModel):
	student_id: int
	name: str
	age: int
	grades: dict[str, list[int]]


class GraduateStudent(Student):
	thesis_topic: str
