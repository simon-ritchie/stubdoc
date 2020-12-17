import pytest

from stubdoc import stubdoc


def test__read_txt() -> None:
    txt: str = stubdoc._read_txt(
        file_path='stubdoc/__init__.py')
    assert '__version__' in txt
