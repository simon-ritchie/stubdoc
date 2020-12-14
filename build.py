"""Build this project for PyPI.
"""

import os
import shutil
from typing import List


def _main() -> None:
    """Script entry point.
    """
    _REMOVING_DIR_PATHS: List[str] = [
        './build',
        './dist',
        './stubdoc.egg-info',
    ]
    for removing_dir_path in _REMOVING_DIR_PATHS:
        shutil.rmtree(removing_dir_path, ignore_errors=True)

    command: str = 'poetry run python setup.py sdist'
    status_code: int = os.system(command)
    if status_code != 0:
        raise Exception(
            f'Build command failed: {command}\nstatus code: {status_code}')

    command = 'poetry run setup.py bdist_wheel'
    status_code = os.system('poetry run setup.py bdist_wheel')
    if status_code != 0:
        raise Exception(
            f'Build command failed: {command}\nstatus code: {status_code}')

    print('Build completed.')


if __name__ == "__main__":
    _main()
