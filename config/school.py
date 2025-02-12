import pydantic

from models import Course, GraduateStudent, Student


class School(pydantic.BaseModel):
    students: dict[int, Student | GraduateStudent] = pydantic.Field(default_factory=dict)
    courses: dict[int, Course] = pydantic.Field(default_factory=dict)

    def add_student(self, student: Student):
        if student.student_id in self.students:
            raise ValueError(f"Student with id {student.student_id} already exists")
        self.students[student.student_id] = student

    def remove_student(self, student_id: int):
        if student_id not in self.students:
            raise ValueError(f"Student with id {student_id} does not exist")
        del self.students[student_id]

    def add_course(self, course: Course):
        if course.course_code in self.courses:
            raise ValueError(f"Course with code {course.course_code} already exists")
        self.courses[course.course_code] = course

    def remove_course(self, course_code: int):
        if course_code not in self.courses:
            raise ValueError(f"Course with code {course_code} does not exist")
        del self.courses[course_code]

    def get_student_courses(self, student_id: int) -> list[Course]:
        return [course for course in self.courses.values() if student_id in course.enrolled_students]
