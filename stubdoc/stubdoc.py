"""The module that implements core functions.
"""


def add_docstring_to_stubfile(
        original_module_path: str, stub_file_path: str) -> None:
    """
    Add docstring to specified stub file.

    Parameters
    ----------
    original_module_path : str
        The path of stub file's original module.
    stub_file_path : str
        Target stub file path.
    """
    module_str: str = _read_txt(file_path=original_module_path)
    pass


def _read_txt(file_path: str) -> str:
    """
    Read specified file path's text.

    Parameters
    ----------
    file_path : str
        Target file path to read.

    Returns
    -------
    txt : str
        Read txt.
    """
    with open(file_path) as f:
        txt: str = f.read()
    return txt
