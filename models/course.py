import pydantic


class Course(pydantic.BaseModel):
	course_code: int
	course_name: str
	enrolled_students: list[int]
