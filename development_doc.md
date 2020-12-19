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

# Create stub files

Notes: this command maybe hang-up on Windows. In that case it is necessary to press Ctrl + C to stop.

```
$ stubgen --include-private ./
```

# Try to apply stubdoc to generated stub

Notes: If you have not installed stubdoc yet, you need to install that before command.

```
$ stubdoc -m stubdoc/stubdoc.py -s out/stubdoc/stubdoc.pyi
$ stubdoc -m samples/sample.py -s out/samples/sample.pyi
$ stubdoc -m tests/test_stubdoc.py -s out/tests/test_stubdoc.pyi
```

And check that stub files.

# PyPI

Build project for PyPI:

```
$ poetry run python build.py
```

Install built package via pip command (need to replace `<version_num>`, for example, `0.1.4`):

```
$ pip install dist/stubdoc-<version_num>-py3-none-any.whl
```

Upload to PyPI:

```
$ twine upload dist/*
```


