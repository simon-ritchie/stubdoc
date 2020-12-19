import os
import shutil
from types import ModuleType
from typing import List
import sys

import pytest

from stubdoc import stubdoc
from stubdoc.stubdoc import _get_callable_names_from_module


def setup() -> None:
    _delete_test_modules_and_stubs()


def teardown() -> None:
    _delete_test_modules_and_stubs()


_TEST_MODS_AND_STUBS_DIR_PATH: str = './tests/tmp_mods_and_stubs/'


def _delete_test_modules_and_stubs() -> None:
    """
    Delete modules and stubs added for testing.
    """
    shutil.rmtree(
        _TEST_MODS_AND_STUBS_DIR_PATH,
        ignore_errors=True,
    )


def test__read_txt() -> None:
    txt: str = stubdoc._read_txt(
        file_path='stubdoc/__init__.py')
    assert '__version__' in txt


def test__read_module() -> None:
    module: ModuleType = stubdoc._read_module(
        module_path='./stubdoc/stubdoc.py')
    assert module == stubdoc

    module = stubdoc._read_module(
        module_path='.\\stubdoc\\stubdoc.py')
    assert module == stubdoc


class _TestClass1:

    test_val: int = 100

    def __init__(self):
        """Test docstring of __init__.
        """
        ...

    def test_method(self):
        """Test docstring of test_method.
        """
        ...

    @property
    def test_property(self) -> int:
        """Test docstring of property.
        """
        return 5

    def test_no_docstring_method(self) -> None:
        ...

    def __eq__(self, other) -> bool:
        return True

    class _TestClass2:
        ...


test_value: list = []


def test__append_class_callable_names_to_list() -> None:

    callable_names: List[str] = []
    stubdoc._append_class_callable_names_to_list(
        callable_names= callable_names,
        class_name='_TestClass1',
        class_val=_TestClass1)
    assert sorted(callable_names) == \
        sorted([
            '_TestClass1.__init__',
            '_TestClass1.test_method',
            '_TestClass1.test_no_docstring_method',
            '_TestClass1.test_property'])


def test__get_callable_names_from_module():
    this_module: ModuleType = sys.modules[__name__]
    callable_names: List[str] = _get_callable_names_from_module(
        module=this_module,
    )
    assert 'test__get_callable_names_from_module' in callable_names
    assert '_TestClass1.__init__' in callable_names
    assert 'test_value' not in callable_names
    assert 'ModuleType' not in callable_names
    assert '_get_callable_names_from_module' not in callable_names


def _test_docstring_existing_func(a: int) -> int:
    """Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    laboris nisi ut aliquip ex ea commodo consequat.
    """
    ...


def _test_docstring_not_existing_func():
    ...


def test__get_docstring_from_top_level_func() -> None:
    this_module: ModuleType = sys.modules[__name__]
    docstring: str = stubdoc._get_docstring_from_top_level_func(
        function_name='_test_docstring_existing_func',
        module=this_module)
    assert docstring.startswith('Lorem ipsum dolor sit amet,')
    assert docstring.endswith('ex ea commodo consequat.')

    docstring = stubdoc._get_docstring_from_top_level_func(
        function_name='_test_docstring_not_existing_func',
        module=this_module)
    assert docstring == ''

    docstring = stubdoc._get_docstring_from_top_level_func(
        function_name='not_existing_func',
        module=this_module)
    assert docstring == ''


def test__remove_doc_not_existing_func_from_callable_names() -> None:
    this_module: ModuleType = sys.modules[__name__]
    callable_names: List[str] = [
        '_TestClass1.__init__',
        '_test_docstring_existing_func',
        '_test_docstring_not_existing_func',
    ]
    callable_names = stubdoc.\
        _remove_doc_not_existing_func_from_callable_names(
            callable_names= callable_names,
            module=this_module)
    expected_list: List[str] = [
        '_TestClass1.__init__',
        '_test_docstring_existing_func',
    ]
    assert callable_names == expected_list


def test__remove_line_end_ellipsis_or_pass_keyword():
    line: str = stubdoc._remove_line_end_ellipsis_or_pass_keyword(
        line='def test_func(a: int) -> int: ...')
    assert line == 'def test_func(a: int) -> int:'

    line = stubdoc._remove_line_end_ellipsis_or_pass_keyword(
        line='def test_func(a:i nt) -> int: pass')
    assert line == 'def test_func(a:i nt) -> int:'

    line = stubdoc._remove_line_end_ellipsis_or_pass_keyword(
        line='test_val: int = 100')
    assert line == 'test_val: int = 100'


def test__add_docstring_to_top_level_func():

    line: str = stubdoc._add_docstring_to_top_level_func(
        line='def test_func(a: int) -> int:',
        docstring=(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit,'
            '\nsed do eiusmod tempor incididunt ut labore et dolore magna.'
        ))
    expected_line: str = (
        'def test_func(a: int) -> int:'
        '\n    """'
        '\n    Lorem ipsum dolor sit amet, consectetur adipiscing elit,'
        '\n    sed do eiusmod tempor incididunt ut labore et dolore magna.'
        '\n    """'
    )
    assert line == expected_line


def test__add_doctring_to_target_function() -> None:
    this_module: ModuleType = sys.modules[__name__]
    stub_str: str = (
        'def _test_docstring_existing_func(a: int) -> int: ...'
        '\ndef _test_docstring_not_existing_func(): pass'
    )
    result_stub_str: str = stubdoc._add_doctring_to_target_function(
        stub_str=stub_str,
        function_name='_test_docstring_existing_func',
        module=this_module,
    )
    expected_str: str = (
        'def _test_docstring_existing_func(a: int) -> int:'
        '\n    """'
        '\n    Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        '\n'
        '\n    laboris nisi ut aliquip ex ea commodo consequat.'
        '\n    """'
        '\ndef _test_docstring_not_existing_func(): pass'
    )
    assert result_stub_str == expected_str


def test__ClassScopeLineRange() -> None:
    stub_str: str = """test_value: int = 100

def test_func_1(a: str) -> int: ...

class TestClass1:
    def test_func_2(self) -> None: pass

class TestClass2:
    def test_func_3(self) -> None: pass

    def test_func_4(self) -> None: ...

class TestClass3(object):
    ...
"""
    class_scope_line_range = stubdoc._ClassScopeLineRange(
        class_name='TestClass1',
        stub_str=stub_str,
    )
    assert class_scope_line_range.start_line == 5
    assert class_scope_line_range.end_line == 7

    class_scope_line_range = stubdoc._ClassScopeLineRange(
        class_name='TestClass2',
        stub_str=stub_str,
    )
    assert class_scope_line_range.start_line == 8
    assert class_scope_line_range.end_line == 12

    class_scope_line_range = stubdoc._ClassScopeLineRange(
        class_name='TestClass3',
        stub_str=stub_str,
    )
    assert class_scope_line_range.start_line == 13
    assert class_scope_line_range.end_line == 14

    with pytest.raises(Exception):  # type: ignore
        class_scope_line_range = stubdoc._ClassScopeLineRange(
            class_name='TestClass4',
            stub_str=stub_str,
        )


def test__get_docstring_from_top_level_class_method() -> None:
    this_module: ModuleType = sys.modules[__name__]

    docstring: str = stubdoc._get_docstring_from_top_level_class_method(
        class_name='_TestClass1',
        method_name='__init__',
        module=this_module,
    )
    assert docstring == 'Test docstring of __init__.'

    docstring: str = stubdoc._get_docstring_from_top_level_class_method(
        class_name='_TestClass1',
        method_name='test_method',
        module=this_module,
    )
    assert docstring == 'Test docstring of test_method.'

    docstring = stubdoc._get_docstring_from_top_level_class_method(
        class_name='_TestClass1',
        method_name='test_property',
        module=this_module,
    )
    assert docstring == 'Test docstring of property.'

    docstring = stubdoc._get_docstring_from_top_level_class_method(
        class_name='_TestClass1',
        method_name='test_no_docstring_method',
        module=this_module,
    )
    assert docstring == ''

    docstring = stubdoc._get_docstring_from_top_level_class_method(
        class_name='_TestClass1',
        method_name='not_existing_method',
        module=this_module,
    )
    assert docstring == ''


def test__add_docstring_to_top_level_class_method() -> None:
    line: str = '    def test_method(a: int) -> None:'
    docstring: str = \
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit.

        laboris nisi ut aliquip ex ea commodo consequat.
        """
    line = stubdoc._add_docstring_to_top_level_class_method(
        line=line,
        docstring=docstring,
    )
    expected_line: str = '''    def test_method(a: int) -> None:
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

        laboris nisi ut aliquip ex ea commodo consequat.
        """'''
    assert line == expected_line


def test__add_docstring_to_class_method() -> None:
    this_module: ModuleType = sys.modules[__name__]
    stub_str: str = """test_value: int = 100

class _TestClass1:

    def __init__(self): ...
    def test_method(self): pass
"""
    result_stub_str: str = stubdoc._add_docstring_to_class_method(
        stub_str=stub_str,
        method_name='_TestClass1.__init__',
        module=this_module,
    )
    expected_stub_str: str = '''test_value: int = 100

class _TestClass1:

    def __init__(self):
        """
        Test docstring of __init__.
        """
    def test_method(self): pass'''
    assert result_stub_str == expected_stub_str


def test_add_docstring_to_stubfile() -> None:
    _delete_test_modules_and_stubs()
    os.makedirs(_TEST_MODS_AND_STUBS_DIR_PATH, exist_ok=True)

    tmp_module_path: str = os.path.join(
        _TEST_MODS_AND_STUBS_DIR_PATH,
        'test_module_1.py',
    )
    tmp_stub_path: str = os.path.join(
        _TEST_MODS_AND_STUBS_DIR_PATH,
        'test_module_1.pyi',
    )
    test_module_str: str = '''
test_value_1: int = 100


def test_function_1(a:int, b: str) -> None:
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    laboris nisi ut aliquip ex ea commodo consequat.

    Parameters
    ----------
    a : int
        Test argument 1.
    b : str
        Test argument 2.
    """

class TestClass1:

    def __init__(self, c: int) -> None:
        """Test constructor.

        Parameters
        ----------
        c : int
            Test argument 3.
        """
        print(100)

    @property
    def test_property(self) -> int:
        """
        Test Property

        Returns
        -------
        test_value_1 : int
            Test return value 1.
        """
        return 100
'''
    with open(tmp_module_path, 'w') as f:
        f.write(test_module_str)

    test_stub_str: str = """test_value_1: int = ...

def test_function_1(a:int, b: str) -> None: ...

class TestClass1:
    def __init__(self, c: int) -> None: pass
    @property
    def test_property(self) -> int: ...
"""
    with open(tmp_stub_path, 'w') as f:
        f.write(test_stub_str)

    tmp_init_file_path: str = os.path.join(
        _TEST_MODS_AND_STUBS_DIR_PATH, '__init__.py',
    )
    with open(tmp_init_file_path, 'w') as f:
        f.write('\n')

    stubdoc.add_docstring_to_stubfile(
        original_module_path=tmp_module_path,
        stub_file_path=tmp_stub_path,
    )
    with open(tmp_stub_path, 'r') as f:
        result_stub_str: str = f.read()

    with open('./tmp.txt', 'w') as f:
        f.write(result_stub_str)

    expected_stub_str: str = '''test_value_1: int = ...

def test_function_1(a:int, b: str) -> None:
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    laboris nisi ut aliquip ex ea commodo consequat.

    Parameters
    ----------
    a : int
        Test argument 1.
    b : str
        Test argument 2.
    """

class TestClass1:
    def __init__(self, c: int) -> None:
        """
        Test constructor.

        Parameters
        ----------
        c : int
            Test argument 3.
        """
    @property
    def test_property(self) -> int:
        """
        Test Property

        Returns
        -------
        test_value_1 : int
            Test return value 1.
        """
'''
    assert result_stub_str == expected_stub_str
    _delete_test_modules_and_stubs()
