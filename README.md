# stubdoc

stubdoc is a Python library that append docstring to stub files.

Notes: currently developing.

# Example

# Installing

# Dependencies

- Supported Python 3.8 or later (tested on 3.8.5). Probably works on Python 3.6.x or later (but not tested).

# Usage

# Create development environment

This project uses poetry==1.1.4 to make development environment.  
Poetry can install via pip command:

```
$ pip install poetry==1.1.4
```

Then install dependencies (Maybe target version's Python install is necessary before command):

```
$ poetry install --no-root --no-dev
```

# Testing

The following command will run overall testing:

```
$ poetry run pytest --cov=./ tests/ -v -s
```

If module or function name specification is necessary, add `-k` keyword argument to command.

```
$ poetry run pytest --cov=./ tests/ -v -s -k <module_or_func_name>
```

# PyPI

Build project for PyPI:

```
$ poetry run python build.py
```

Upload to PyPI:

```
$ twine upload dist/*
```





