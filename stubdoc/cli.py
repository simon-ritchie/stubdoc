"""The module that handles command line interface implementations.
"""

from typing import List, Optional
import argparse
from argparse import ArgumentParser
from argparse import Namespace

_DESCRIPTION: str = (
    'This command will add docstring to stub file.'
)


class Arg:

    short_name: str
    long_name: str
    type_: type
    help: str

    def __init__(
            self, short_name: str, long_name: str, type_: type,
            help: str, required: bool) -> None:
        """
        The class that store single argument setting.

        Parameters
        ----------
        short_name : str
            Argument short name. e.g., '-s'
            Necessary to start with single hyphen.
        long_name : str
            Argument long name. e.g., '--sample_arg'
            Necessary to start with double hyphen.
        type_ : type
            Argument type. e.g., str, int, etc.
        help : str
            The argument's help text.
        required : bool
            If set to True, this argument will be required.
        """
        self.short_name = short_name
        self.long_name = long_name
        self.type_ = type_
        self.help = help


def _add_arg(
        parser: ArgumentParser, arg: Arg) -> None:
    """
    Add argument to argument parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser to add argument.
    arg: Arg
        Single argument to add to the parser.

    Raises
    ------
    ValueError
        - If short_name not starts with single hyphen.
        - If long_name not starts with double hyphen.
    """
    if arg.short_name.startswith('--'):
        raise ValueError(
            'Double hyphen not allowed for short_name argument: '
            f'{arg.short_name}')
    if not arg.short_name.startswith('-'):
        raise ValueError(
            'short_name is not starts with single hyphen: '
            f'{arg.short_name}')
    if not arg.long_name.startswith('--'):
        raise ValueError(
            'long_name is not starts with double hyphen: '
            f'{arg.long_name}')

    parser.add_argument(
        arg.short_name, arg.long_name, type=arg.type_, help=arg.help)


ARGS: List[Arg] = [
    Arg(short_name='-m',
        long_name='--module_path',
        type_=str,
        help='Stub file\'s original module path. e.g., sample/path.py',
        required=True),
    Arg(short_name='-s',
        long_name='--stub_path',
        type_=str,
        help='Target stub file path. e.g., sample/path.pyi',
        required=True),
]


def main():
    """
    Entry point of the command line interface.

    Parameters
    ----------
    args : Namespace or None, default None
        instance that stores arguments data. Only specified None at testing.
    """
    parser: ArgumentParser = argparse.ArgumentParser(
        description=_DESCRIPTION)

    for arg in ARGS:
        _add_arg(parser=parser, arg=arg)
    args: Namespace = parser.parse_args()
    print('module_path' , args.module_path)
    print('stub_path', args.stub_path)

