from argparse import ArgumentParser
from argparse import Namespace
import os

import pytest

from stubdoc import cli


def test__add_arg() -> None:
    parser = ArgumentParser()

    with pytest.raises(ValueError):  # type: ignore
        cli._add_arg(
            parser=parser,
            arg=cli.Arg(
                short_name='--test_arg',
                long_name='--test_arg',
                type_=str,
                help='test help.',
            ))

    with pytest.raises(ValueError):  # type: ignore
        cli._add_arg(
            parser=parser,
            arg=cli.Arg(
                short_name='test_arg',
                long_name='--test_arg',
                type_=str,
                help='test help.',
            ))

    with pytest.raises(ValueError):  # type: ignore
        cli._add_arg(
            parser=parser,
            arg=cli.Arg(
                short_name='-t',
                long_name='-test_arg',
                type_=str,
                help='test help.',
            ))

    cli._add_arg(
        parser=parser,
        arg=cli.Arg(
            short_name='-t',
            long_name='--test_arg',
            type_=str,
            help='test help.',
        ))


def test__validate_module_path_arg() -> None:
    with pytest.raises(ValueError):  # type: ignore
        cli._validate_module_path_arg(module_path_arg=None)

    with pytest.raises(ValueError):  # type: ignore
        cli._validate_module_path_arg(
            module_path_arg='not_existing_module.py')

    with pytest.raises(ValueError):  # type: ignore
        cli._validate_module_path_arg(
            module_path_arg='README.md')

    cli._validate_module_path_arg(
        module_path_arg='stubdoc/cli.py')


def test__validate_stub_path_arg() -> None:
    with pytest.raises(ValueError):  # type: ignore
        cli._validate_stub_path_arg(stub_path_arg=None)

    test_tmp_stub_file_path = './tmp_test_stub.pyi'
    if os.path.exists(test_tmp_stub_file_path):
        os.remove(test_tmp_stub_file_path)
    with pytest.raises(ValueError):  # type: ignore
        cli._validate_stub_path_arg(
            stub_path_arg=test_tmp_stub_file_path)

    with pytest.raises(ValueError):  # type: ignore
        cli._validate_stub_path_arg(
            stub_path_arg='stubdoc/cli.py')

    with open(test_tmp_stub_file_path, 'w') as f:
        f.write('\n')
    cli._validate_stub_path_arg(stub_path_arg=test_tmp_stub_file_path)
    os.remove(test_tmp_stub_file_path)
