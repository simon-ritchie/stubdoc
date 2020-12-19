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


# Dependencies

- Supported Python 3.8 or later (tested on 3.8.5). Probably works on Python 3.6.x or later (but not tested).

# Usage

# Limitations


