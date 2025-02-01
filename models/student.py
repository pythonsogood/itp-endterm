import pydantic


class Student(pydantic.BaseModel):
	name: str
	student_id: int
	age: int
	grades: dict[str, list[int]]


class GraduateStudent(Student):
	thesis_topic: str
