from types import ModuleType
from typing import List
import sys

import pytest

from stubdoc import stubdoc


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
        ...

    def test_method(self):
        ...

    @property
    def test_property(self) -> int:
        return 5

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
            '_TestClass1.test_property'])

    print(callable_names)


def test__get_callable_names_from_module():
    this_module: ModuleType = sys.modules[__name__]
    callable_names: List[str] = stubdoc._get_callable_names_from_module(
        module=this_module,
    )
    assert 'test__get_callable_names_from_module' in callable_names
    assert '_TestClass1.__init__' in callable_names
    assert 'test_value' not in callable_names
