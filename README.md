# stubdoc

stubdoc is a Python library that append docstring to stub files.

# What problem will be solved by this library?

mypy's stubgen command that create stub files does not append docstring. So if stub file exists and IDE prioritize stub's completion then docstring will not appear on IDE.

So that this library add docstring to stub files to display that.

For more mypy's stubgen command details, please see mypy documentation, [Automatic stub generation (stubgen)](https://mypy.readthedocs.io/en/stable/stubgen.html).

For example, suppose that the following code's module exists (`sample/sample.py`):

```py
from random import randint

sample_int: int = 100


def sample_func(a: int, b: str) -> bool:
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    ed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

    Parameters
    ----------
    a : int
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    b : str
        ed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

    Returns
    -------
    c : bool
        Ut enim ad minim veniam, quis nostrud exercitation.
    """
    return True


class SampleClass:

    def __init__(self) -> None:
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        """

    @property
    def sample_property(self) -> int:
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

        Returns
        -------
        d : int
            ed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """
        return randint(0, 100)
```

mypy's stubgen command will generate stub files as follows (stubgen command will not add docstring):

```py
sample_int: int

def sample_func(a: int, b: str) -> bool: ...

class SampleClass:
    def __init__(self) -> None: ...
    @property
    def sample_property(self) -> int: ...
```

And then, this library's command will add the docstring to stub doc as follows, so IDE's code completion will show docstring:

```py
sample_int: int

def sample_func(a: int, b: str) -> bool:
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    ed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

    Parameters
    ----------
    a : int
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    b : str
        ed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

    Returns
    -------
    c : bool
        Ut enim ad minim veniam, quis nostrud exercitation.
    """

class SampleClass:
    def __init__(self) -> None:
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        """
    @property
    def sample_property(self) -> int:
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

        Returns
        -------
        d : int
            ed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """
```

# Installing

Installation via pip command is provided:

```
$ pip install stubdoc
```

# Dependencies

- Supported Python 3.8 or later (tested on 3.8.5). Probably works on Python 3.6.x or later (but not tested).

# Usage

Notes: specified module need to be able to import. Stubdoc will replace paths to package path (e.g., 'sample/path.py' to 'sample.path'), so that paths argument can not be specified upper level directory or root directory (e.g., '/sample/path.py' or '../sample/path').

```
This command will add docstring to stub file. Currently supported one-line stub implementation, like mypy's stubgen
command, something as follows: def any_func(a: int, b: str) -> None: ... If line break exists after colon, this
command will not work correctly. Also not supported nested function, etc.

optional arguments:
  -h, --help            show this help message and exit
  -m MODULE_PATH, --module_path MODULE_PATH
                        Stub file's original module path. e.g., sample/path.py
  -s STUB_PATH, --stub_path STUB_PATH
                        Target stub file path. e.g., sample/path.pyi
```

Command example:

```
$ stubdoc -m samples/sample.py -s out/samples/sample.pyi
```

or

```
$ stubdoc --module_path samples/sample.py --stub_path out/samples/sample.pyi
```

Or maybe Python interface is useful, like Django environment:

```py
from stubdoc import add_docstring_to_stubfile

add_docstring_to_stubfile(
    original_module_path='sample/path.py',
    stub_file_path='sample/path.pyi')
```

# Limitations

This library supported only one-line stub implementation, like this:

```py
def sample_func(a: int, b: str) -> bool: ...

class SampleClass:
    def __init__(self) -> None: ...
    @property
    def sample_property(self) -> int: ...
```

Not supported line breaks after function's colon:

```py
def sample_func(a: int, b: str) -> bool:
    ...

class SampleClass:
    def __init__(self) -> None:
        ...
    @property
    def sample_property(self) -> int:
        pass
```

Also not supported nested functions, like this (docstring will add to only top-level function):

```py
def sample_func_1(a: int, b: str) -> bool:
    def sample_func_2(c: list) -> None: ...
```
