# itp-endterm

python ItP endterm project

> Built with [FastAPI](https://github.com/fastapi)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/license/mit/)


## Installation

clone repository

```sh
git clone https://github.com/pythonsogood/itp-endterm.git
cd itp-endterm
```

install poetry
```sh
pip install poetry
```

create virtual environment

```sh
poetry env use python
```

activate virtual environment

```sh
poetry shell
```

install dependencies

```sh
poetry install
```

## Usage

activate virtual environment

```sh
poetry shell
```

run `main.py`

```sh
python main.py
```

Server opens on http://localhost:8000

API Endpoints can be checked on [/docs](http://localhost:8000/docs) page via [Swagger-UI](https://github.com/swagger-api/swagger-ui)

Reports routes are:
* [/report/students](http://localhost:8000/report/students)
* [/report/student/{student_id}/grades](http://localhost:8000/report/student/{student_id}/grades)
* [/report/course/{course_id}/grades](http://localhost:8000/report/course/{course_id}/grades)

## Requirements

* Python: `3.12`, `3.13`[^1]

[^1]: Tested on Python `3.12` and `3.13`, but *should work* on `3.10`+

## Dependencies

* Can be found in [pyproject.toml](/pyproject.toml)

## Project criteria checklist

### Core Classes and Attributes

- [x] [Student](/models/student.py#L4)
- [x] [Course](/models/course.py)
- [x] [School](/config/school.py)
- [x] [GraduateStudent (Inheritance)](/models/student.py#L26)

### Improved Functionality Section
- [x] [Student Management](/routes/student_route.py)
- [x] [Course Enrollment and Management](/routes/course_route.py)
- [x] [Search](/routes/student_route.py#L38) and [Reporting](/routes/report_route.py)
- [x] [User Data Persistence](/config/config.py)
- [x] [Error Handling](/util/errors.py)
- [x] [Extensibility via Inheritance](/models/student.py#L26)

### Improved User Scenario Section
- [x] [Student Enrollment and Record Management](/routes/student_route.py)
- [x] [Course Registration and Enrollment](/routes/course_route.py)
- [x] [Grade Input](/routes/student_route.py#L92) and [Analysis](/routes/report_route.py)
- [x] [Search and Retrieval](/routes/student_route.py#L49)
- [x] [Reporting and Analytics](/routes/report_route.py)