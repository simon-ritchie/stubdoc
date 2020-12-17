"""The module that implements core functions.
"""

import sys
import importlib
from types import ModuleType

from typing import List


def add_docstring_to_stubfile(
        original_module_path: str, stub_file_path: str) -> None:
    """
    Add docstring to specified stub file.

    Parameters
    ----------
    original_module_path : str
        The path of stub file's original module.
    stub_file_path : str
        Target stub file path.
    """
    module = _read_module(module_path=original_module_path)
    module_str: str = _read_txt(file_path=original_module_path)
    stub_str: str = _read_txt(file_path=stub_file_path)
    callable_names: List[str] = _get_callable_names_from_module(
        module_str=module_str)


def _read_module(module_path: str) -> ModuleType:
    """
    Read specified path's module.

    Parameters
    ----------
    module_path : str
        Target module path to read.

    Returns
    -------
    module : ModuleType
        Read module.
    """
    name: str = module_path.replace('.py', '')
    name = name.replace('/', '.')
    name = name.replace('\\', '.')
    while name.startswith('.'):
        name = name.replace('.', '', 1)
    module: ModuleType = importlib.import_module(name)
    return module


def _get_callable_names_from_module(module_str: str) -> List[str]:
    """
    Get callable names in the module string.

    Parameters
    ----------
    module_str : str
        Target module string.

    Returns
    -------
    callable_names : list of str
        Result callable names in module str.
        If class method or nested function, name will be concatenated
        by comma.
        e.g., `_read_txt`, `SampleClass._read_text`,
        `any_function.nested_function`.
    """
    pass



def _read_txt(file_path: str) -> str:
    """
    Read specified file path's text.

    Parameters
    ----------
    file_path : str
        Target file path to read.

    Returns
    -------
    txt : str
        Read txt.
    """
    with open(file_path) as f:
        txt: str = f.read()
    return txt
