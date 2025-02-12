import pydantic


class Course(pydantic.BaseModel):
    course_code: int
    course_name: str
    enrolled_students: set[int] = pydantic.Field(default_factory=set)

    @pydantic.field_serializer("enrolled_students")
    def serialize_enrolled_students(self, enroll_students: set[int]) -> list[int]:
        return list(enroll_students)
