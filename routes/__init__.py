import os
import sys

sys.path.append(os.path.abspath(".."))


__all__ = (
	"ConfigRoute",
	"CourseRoute",
)


from .config_route import ConfigRoute
from .course_route import CourseRoute
