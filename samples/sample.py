from random import randint

sample_int: int = 100


def sample_func(a: int, b: str) -> bool:
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    ed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

    Parameters
    ----------
    a : int
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    b : str
        ed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

    Returns
    -------
    c : bool
        Ut enim ad minim veniam, quis nostrud exercitation.
    """
    return True


class SampleClass:

    def __init__(self) -> None:
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        """

    @property
    def sample_property(self) -> int:
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

        Returns
        -------
        d : int
            ed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """
        return randint(0, 100)
