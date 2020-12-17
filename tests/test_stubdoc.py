from types import ModuleType

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
