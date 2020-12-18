"""The module that implements core functions.
"""

import inspect
import sys
import importlib
from types import ModuleType

from typing import Any, Callable, List, Tuple


def add_docstring_to_stubfile(
        original_module_path: str, stub_file_path: str) -> None:
    """
    Add docstring to specified stub file.

    Notes
    -----
    Currently only applied top level function or top level class
    methods. Not to be applied to nested function.

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
        module=module)


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


def _get_callable_names_from_module(module: ModuleType) -> List[str]:
    """
    Get callable names defined in specified module.

    Parameters
    ----------
    module : ModuleType
        Target module.

    Returns
    -------
    callable_names : list of str
        Result callable names in module str.
        If class method exists, name will be concatenated by comma.
        e.g., `_read_txt`, `SampleClass._read_text`.
        Nested function will not be included.
    """
    callable_names: List[str] = []
    members: List[Tuple[str, Any]] = inspect.getmembers(module)
    for member_name, member_val in members:
        if inspect.isfunction(member_val):
            callable_names.append(member_name)
            continue
        if inspect.isclass(member_val):
            _append_class_callable_names_to_list(
                callable_names= callable_names,
                class_name=member_name,
                class_val=member_val)
            continue
    return callable_names


def _append_class_callable_names_to_list(
        callable_names: List[str], class_name: str,
        class_val: type) -> None:
    """
    Append class's member method names to list.
    Name will be added as following format:
    <class_name>.<method_name>

    Parameters
    ----------
    callable_names : list of str
        The list that append names to.
    class_name : str
        Target Class name.
    class_val : type
        Target class.
    """
    members: List[Tuple[str, Any]] = inspect.getmembers(
        class_val,
    )
    for member_name, member_val in members:
        if (not isinstance(member_val, Callable)
                and not isinstance(member_val, property)):
            continue
        if (member_name.startswith('__') and member_name != '__init__'):
            continue
        if inspect.isclass(member_val):
            continue
        name: str = f'{class_name}.{member_name}'
        callable_names.append(name)


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
