import os
import sys

sys.path.append(os.path.abspath(".."))


__all__ = (
	"ConfigRoute",
	"CourseRoute",
	"StudentRoute",
	"ReportRoute",
)


from .config_route import ConfigRoute
from .course_route import CourseRoute
from .student_route import StudentRoute
from .report_route import ReportRoute
