import os
import sys

sys.path.append(os.path.abspath(".."))


__all__ = (
	"Course",
	"GraduateStudent",
	"Student",
)


from .course import Course
from .student import GraduateStudent, Student
