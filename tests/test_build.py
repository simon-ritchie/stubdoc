import pytest
import build


def test__run_command() -> None:
    with pytest.raises(Exception):  # type: ignore
        build._run_command(command='not existing command')

    build._run_command(command='cd .')

