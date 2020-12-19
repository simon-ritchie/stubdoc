"""The module that implements core functions.
"""

import re
import inspect
import sys
import importlib
from types import ModuleType

from typing import Any, Callable, List, Optional, Tuple


def add_docstring_to_stubfile(
        original_module_path: str, stub_file_path: str) -> None:
    """
    Add docstring to a specified stub file.

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
    callable_names = _remove_doc_not_existing_func_from_callable_names(
        callable_names=callable_names, module=module)
    for callable_name in callable_names:
        if '.' not in callable_name:
            stub_str = _add_doctring_to_target_function(
                stub_str=stub_str,
                function_name=callable_name,
                module=module,
            )
            continue


def _remove_doc_not_existing_func_from_callable_names(
        callable_names: List[str], module: ModuleType) -> List[str]:
    """
    Remove top-level function that docstring not existing from callable
    names list.

    Parameters
    ----------
    callable_names : list of str
        Callable names list to check.
    module : ModuleType
        The module that specified callables are defined.

    Returns
    -------
    remove_callable_names : list of str
        The list that removed docstring not existing functions.
    """
    remove_callable_names: List[str] = []
    for callable_name in callable_names:
        if '.' in callable_name:
            remove_callable_names.append(callable_name)
            continue
        docstring: str = _get_docstring_from_top_level_func(
            function_name=callable_name,
            module=module)
        if docstring == '':
            continue
        remove_callable_names.append(callable_name)
    return remove_callable_names


def _add_doctring_to_target_function(
        stub_str: str, function_name: str,
        module: ModuleType) -> str:
    """
    Add doctring to a specified function.

    Parameters
    ----------
    stub_str : str
        Target stub file's string.
    function_name : str
        Target function name (top-level function only).
    module: ModuleType
        Stub file's original module.

    Returns
    -------
    result_stub_str : str
        Stub file's string after docstring added.
    """
    result_stub_str: str = ''
    lines: List[str] = stub_str.splitlines()
    pattern = re.compile(pattern=r'^def ' + function_name + r'\(.+$')
    for line in lines:
        if result_stub_str != '':
            result_stub_str += '\n'
        match: Optional[re.Match] = pattern.search(string=line)
        if match is None:
            result_stub_str += line
            continue
        docstring: str = _get_docstring_from_top_level_func(
            function_name=function_name,
            module=module,
        )
        line = _remove_line_end_ellipsis_or_pass_keyword(line=line)
        line = _add_docstring_to_top_level_func(
            line=line, docstring=docstring)
        result_stub_str += line

    return result_stub_str


def _add_docstring_to_top_level_func(line: str, docstring: str) -> str:
    """
    Add docstring to the top-level function line string.

    Parameters
    ----------
    line : str
        Target function line string.
        e.g., `def sample_func(a: int) -> None:`
    docstring : str
        A doctring to add.

    Returns
    -------
    line : str
        Docstring added line str.
    """
    line += '\n    """'
    docstring_lines: List[str] = docstring.splitlines()
    for docstring_line in docstring_lines:
        if docstring_line == '':
            line += '\n'
            continue
        if not docstring_line.startswith('    '):
            docstring_line = f'    {docstring_line}'
        line += f'\n{docstring_line}'
    line += '\n    """'
    return line


def _remove_line_end_ellipsis_or_pass_keyword(line: str) -> str:
    """
    Remove ellipsis or pass keyword from end of line
    (e.g., `def sample_func(): ...` or `def sample_func(): pass`).

    Parameters
    ----------
    line : str
        Target line string.

    Returns
    -------
    result_line : str
        Line string that removed ellipsis or pass keyword string.
    """
    if line.endswith(' ...'):
        line = re.sub(pattern=r' ...$', repl='', string=line)
        return line
    if line.endswith(' pass'):
        line = re.sub(pattern=r' pass$', repl='', string=line)
        return line
    return line


def _get_docstring_from_top_level_func(
        function_name: str, module: ModuleType) -> str:
    """
    Get docstring of the specified top-level function name.

    Parameters
    ----------
    function_name : str
        Target function name.
    module : ModuleType
        Target module that specified function exists.

    Returns
    -------
    docstring : str
        Specified function's docstring.
    """
    members: List[Tuple[str, Any]] = inspect.getmembers(module)
    for member_name, member_val in members:
        if member_name != function_name:
            continue
        target_function: Callable = member_val
        if target_function.__doc__ is None:
            return ''
        docstring : str = target_function.__doc__
        docstring = docstring.strip()
        return docstring
    return ''


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
