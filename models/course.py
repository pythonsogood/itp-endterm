import pydantic


class Course(pydantic.BaseModel):
	course_name: str
	course_code: int
	enrolled_students: list[int]
