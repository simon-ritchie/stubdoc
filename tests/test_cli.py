from argparse import ArgumentParser
from argparse import Namespace

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
                required=True,
            ))

    with pytest.raises(ValueError):  # type: ignore
        cli._add_arg(
            parser=parser,
            arg=cli.Arg(
                short_name='test_arg',
                long_name='--test_arg',
                type_=str,
                help='test help.',
                required=True,
            ))

    with pytest.raises(ValueError):  # type: ignore
        cli._add_arg(
            parser=parser,
            arg=cli.Arg(
                short_name='-t',
                long_name='-test_arg',
                type_=str,
                help='test help.',
                required=True,
            ))

    cli._add_arg(
        parser=parser,
        arg=cli.Arg(
            short_name='-t',
            long_name='--test_arg',
            type_=str,
            help='test help.',
            required=True,
        ))
