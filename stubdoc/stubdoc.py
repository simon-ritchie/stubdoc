"""The module that implements core functions.
"""

import sys
import os
import re
import inspect
import importlib
import traceback
from types import ModuleType
from typing import Any, Callable, List, Optional, Tuple, Pattern
from typing import Match, Type


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
        stub_str = _add_docstring_to_class_method(
            stub_str=stub_str,
            method_name=callable_name,
            module=module,
        )

    class_names: List[str] = _get_top_level_class_names(
        stub_str=stub_str)
    class_names = _remove_doc_not_existing_class_from_class_names(
        class_names=class_names, module=module)
    for class_name in class_names:
        stub_str = _add_doctring_to_target_class(
            stub_str=stub_str,
            class_name=class_name,
            module=module,
        )

    if not stub_str.endswith('\n'):
        stub_str += '\n'
    with open(stub_file_path, 'w') as f:
        f.write(stub_str)


def _add_doctring_to_target_class(
        *, stub_str: str,
        class_name: str,
        module: ModuleType) -> str:
    """
    Add a docstring to a specified class.

    Parameters
    ----------
    stub_str : str
        A Target stub file string.
    class_name : str
        A target class name.
    module : ModuleType
        Stub file's original module.

    Returns
    -------
    result_stub_str : str
        Stub file string after docstring added.
    """
    docstring: str = _get_docstring_from_top_level_class(
        class_name=class_name, module=module)
    result_docstring: str = '    """'
    docstring_lines: List[str] = docstring.splitlines()
    for i, docstring_line in enumerate(docstring_lines):
        result_docstring += '\n'
        if i == 0:
            result_docstring += '    '
        result_docstring += f'{docstring_line}'
    result_docstring += '\n    """'

    result_stub_str = re.sub(
        pattern=rf'^class {class_name}(.*?)\:',
        repl=rf'class {class_name}\1:\n{result_docstring}',
        string=stub_str,
        count=1,
        flags=re.MULTILINE | re.DOTALL)
    return result_stub_str


def _remove_doc_not_existing_class_from_class_names(
        *, class_names: List[str], module: ModuleType) -> List[str]:
    """
    Remove top-level class names from a class names list
    that docstring does not exist.

    Parameters
    ----------
    class_names : List[str]
        Class names list.
    module : ModuleType
        A module that specified classes are defined.

    Returns
    -------
    result_class_names : List[str]
        A list after removing.
    """
    result_class_names: List[str] = []
    for class_name in class_names:
        docstring: str = _get_docstring_from_top_level_class(
            class_name=class_name,
            module=module)
        if docstring == '':
            continue
        result_class_names.append(class_name)
    return result_class_names


def _get_docstring_from_top_level_class(
        *, class_name: str, module: ModuleType) -> str:
    """
    Get a docstring from a specified top-level class.

    Parameters
    ----------
    class_name : str
        A target class name.
    module : ModuleType
        A module that a specified class is defined.

    Returns
    -------
    docstring : str
        An extracted class docstring.
    """
    members: List[Tuple[str, Type]] = inspect.getmembers(
        object=module, predicate=inspect.isclass)
    for member_name, member_class in members:
        if member_name != class_name:
            continue
        if member_class.__doc__ is None:
            return ''
        docstring: str = member_class.__doc__.strip()
        return docstring
    return ''


def _get_top_level_class_names(*, stub_str: str) -> List[str]:
    """
    Get top-level class names from a specified stub string.

    Parameters
    ----------
    stub_str : str
        A target stub string.

    Returns
    -------
    class_names : List[str]
        Extracted top-level class names.
    """
    class_names: List[str] = []
    lines: List[str] = stub_str.splitlines()
    pattern: Pattern = re.compile(pattern=r'^class (.+?)[\(\:]')
    for line in lines:
        match: Optional[Match] = pattern.match(string=line)
        if match is None:
            continue
        class_name: str = match.group(1).strip()
        class_names.append(class_name)
    return class_names


class _ClassScopeLineRange:
    """
    The class that stores specified class's scope line range
    in stub string.
    """

    _class_name: str
    _stub_str: str
    start_line: int
    end_line: int

    def __init__(self, class_name: str, stub_str: str) -> None:
        """
        The class that stores specified class's scope line range
        in stub string.
        e.g., if that class scope is starting at line 10, then
        start_line attribute will set to 10. end_line attribute is
        also same.

        Parameters
        ----------
        class_name : str
            Target class name that defined in stub string.
        stub_str : str
            Overall stub string.

        Raises
        ------
        Exception
            If specified class name not found in the stub string.
        """
        self._class_name = class_name
        self._stub_str = stub_str
        pattern = r'^class ' + class_name + r'[\(:].*$'
        stub_lines: List[str] = stub_str.splitlines()
        start_line: Optional[int] = None
        end_line: Optional[int] = None
        last_line: int = 1
        for i, stub_line in enumerate(stub_lines):
            last_line = i + 1
            if start_line is None:
                match: Optional[re.Match] = re.search(
                    pattern=pattern, string=stub_line)
                if match is None:
                    continue
                start_line = i + 1
                continue
            if stub_line == '' or stub_line == '    ':
                continue
            if not stub_line.startswith('    '):
                end_line = i
                break
        if start_line is not None and end_line is None:
            end_line = last_line
        if start_line is None or end_line is None:
            raise Exception(f'Target class name not found: {class_name}')
        self.start_line = start_line
        self.end_line = end_line


def _add_docstring_to_class_method(
        stub_str: str, method_name: str, module: ModuleType) -> str:
    """
    Add a docstring to a specified class method.

    Parameters
    ----------
    stub_str : str
        Target stub file string.
    method_name : str
        Target method name (top-level class method only).
        Class name and method name need to be concatenated by comma.
        e.g. `ClassName.method_name`
    module: ModuleType
        Stub file's original module.

    Returns
    -------
    result_stub_str : str
        Stub file string after docstring added.
    """
    class_name: str = method_name.split('.')[0]
    method_name = method_name.split('.')[1]
    line_range: _ClassScopeLineRange = _ClassScopeLineRange(
        class_name=class_name, stub_str=stub_str)
    stub_lines: List[str] = stub_str.splitlines()
    result_stub_str: str = ''
    pattern = re.compile(pattern=r'    def ' + method_name + r'\(.+$')
    for i, stub_line in enumerate(stub_lines):
        if result_stub_str != '':
            result_stub_str += '\n'
        line_num: int = i + 1
        if line_num < line_range.start_line or line_range.end_line < line_num:
            result_stub_str += stub_line
            continue
        match: Optional[re.Match] = pattern.search(string=stub_line)
        if match is None:
            result_stub_str += stub_line
            continue
        docstring: str = _get_docstring_from_top_level_class_method(
            class_name=class_name,
            method_name=method_name,
            module=module,
        )
        stub_line = _remove_line_end_ellipsis_or_pass_keyword(line=stub_line)
        stub_line = _add_docstring_to_top_level_class_method(
            line=stub_line, docstring=docstring)
        result_stub_str += stub_line
    return result_stub_str


def _add_docstring_to_top_level_class_method(
        line: str, docstring: str) -> str:
    """
    Add docstring to the line string of top-level class's method.

    Parameters
    ----------
    line : str
        Target class's method line string.
        e.g., `    def sample_method(self) -> None:`
    docstring : str
        A doctring to add.

    Returns
    -------
    line : str
        Docstring added line str.
    """
    eight_tabs: str = '        '
    line += f'\n{eight_tabs}"""'
    docstring_lines: List[str] = docstring.splitlines()
    for docstring_line in docstring_lines:
        if docstring_line == '':
            line += '\n'
            continue
        if not docstring_line.startswith(eight_tabs):
            docstring_line = f'{eight_tabs}{docstring_line}'
        line += f'\n{docstring_line}'
    line = line.rstrip()
    line += f'\n{eight_tabs}"""'
    return line


def _get_docstring_from_top_level_class_method(
        class_name: str, method_name: str, module: ModuleType) -> str:
    """
    Get docstring from method of top-level class.

    Parameters
    ----------
    class_name : str
        Target class name.
    method_name : str
        Target class's method name.
    module : ModuleType
        Stub file's original module.

    Returns
    -------
    docstring : str
        Class method's docstring.
    """
    members: List[Tuple[str, Any]] = inspect.getmembers(
        module, predicate=inspect.isclass)
    target_class: Optional[type] = None
    for member_name, member_val in members:
        if member_name != class_name:
            continue
        target_class = member_val
    members = inspect.getmembers(target_class)
    for member_name, member_val in members:
        if member_name != method_name:
            continue
        target_method: Callable = member_val
        if target_method.__doc__ is None:
            return ''
        docstring: str = target_method.__doc__
        docstring = docstring.strip()
        return docstring
    return ''


def _remove_doc_not_existing_func_from_callable_names(
        callable_names: List[str], module: ModuleType) -> List[str]:
    """
    Remove top-level function names from a callable names list
    that docstring does not exist.

    Parameters
    ----------
    callable_names : list of str
        Callable names list to check.
    module : ModuleType
        A module that specified callables are defined.

    Returns
    -------
    result_callable_names : list of str
        A list after removing.
    """
    result_callable_names: List[str] = []
    for callable_name in callable_names:
        if '.' in callable_name:
            result_callable_names.append(callable_name)
            continue
        docstring: str = _get_docstring_from_top_level_func(
            function_name=callable_name,
            module=module)
        if docstring == '':
            continue
        result_callable_names.append(callable_name)
    return result_callable_names


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
        docstring: str = target_function.__doc__
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
    file_name: str = os.path.basename(module_path)
    dir_path: str = module_path.replace(file_name, '', 1)
    sys.path.append(dir_path)
    sys.path.append('./')
    package_name: str = ''
    all_suffixes: List[str] = importlib.machinery.all_suffixes()  # type: ignore
    for ending in all_suffixes:
        if module_path.endswith(ending):
            package_name = module_path[:-len(ending)]
            break
    package_name = package_name.replace('/', '.')
    package_name = package_name.replace('\\', '.')
    while package_name.startswith('.'):
        package_name = package_name.replace('.', '', 1)
    try:
        module: ModuleType = importlib.import_module(package_name)
    except Exception:
        raise Exception(
            f'{traceback.format_exc()}\n\n'
            'Specified module import failed. Please check specified path'
            ' is not a upper level directory or root directory (need to be'
            f' able to import by package path style): {package_name}')
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
        if not hasattr(member_val, '__module__'):
            continue
        if member_val.__module__ != module.__name__:
            continue
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
