"""The module that handles command line interface implementations.
"""

from typing import Optional
import argparse

_DESCRIPTION: str = (
    'This command will add docstring to stub file.'
)


def main(args: Optional[argparse.Namespace] = None):
    """
    Entry point of the command line interface.

    Parameters
    ----------
    args : Namespace or None, default None
        instance that stores arguments data. Only specified None at testing.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=_DESCRIPTION)

    parser.add_argument(
        '-m', '--module_path', type=str,
        help='Stub file\'s original module path. e.g., sample/path.py',
    )
    parser.add_argument(
        '-s', '--stub_path', type=str,
        help='Target stub file path. e.g., sample/path.pyi',
    )
    print('module_path' ,args.module_path)
    print('stub_path', args.stub_path)

