import os
import pytest
import build


def test__run_command() -> None:
    with pytest.raises(Exception):  # type: ignore
        build._run_command(command='not existing command')

    build._run_command(command='cd .')


def test__remove_build_dirs() -> None:
    os.makedirs(build._REMOVING_DIR_PATHS[0], exist_ok=True)
    build._remove_build_dirs()
    for removing_dir_path in build._REMOVING_DIR_PATHS:
        assert not os.path.exists(removing_dir_path)


def test__main() -> None:
    build._remove_build_dirs()
    build._main()
    for removing_dir_path in build._REMOVING_DIR_PATHS:
        assert os.path.isdir(removing_dir_path)
