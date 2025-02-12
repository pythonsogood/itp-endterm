# itp-endterm

python ItP endterm project

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
API Endpoints can be checked via [Swagger-UI](https://github.com/swagger-api/swagger-ui) on [/docs](http://localhost:8000/docs)

## Requirements

* OS: Windows 10 or greater

* Python: 3.12[^1]

[^1]: Tested on Python 3.12 and 3.13, but should work on 3.10+

## Dependencies

* Can be found in [pyproject.toml](/pyproject.toml)