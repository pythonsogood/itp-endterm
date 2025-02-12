import os
import sys

sys.path.append(os.path.abspath(".."))


__all__ = (
	"Config",
	"School",
)


from .config import Config
from .school import School
