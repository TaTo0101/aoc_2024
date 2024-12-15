"""Some basic utility functions"""

import os
from types import NoneType
from typing import Optional, Union


def puzzle_input_reader(
    path: str, strip: bool = True, split_char: Optional[str] = None
) -> list:
    """Helper function to read in the puzzle input. Reads file line by line.

    Allows one to strip line break chars like \n and also optionally specify a split character to
    split the lines into.

    Args:
        path (str): Path to the file that one wants to read
        strip (bool, optional): Whether to strip line break characters. Defaults to True.
        split_char (Optional[str], optional): String to split lines into. Defaults to None.

    Returns:
        ndarray: List of lists, where each element is the read in line possibly split by split_char
            and with linebreak characters removed.
    """
    if not isinstance(path, str):
        raise TypeError(f"path must be string but got {type(path)} instead")

    # Check that path has been correctly specified
    if not os.path.exists(path):
        raise ValueError(f"No such file or directory for {path}!")

    if not isinstance(strip, bool):
        raise TypeError(f"strip must be bool but got {type(strip)} instead")
    if not isinstance(split_char, Union[NoneType, str]):
        raise TypeError(
            f"split_char must either be string or None but got {type(split_char)} instead"
        )

    # Instantiate empty output
    read_in_file = []

    # Read file line by line
    with open(path, "r") as file:
        for line in file:
            if strip:
                # Omit \n
                if split_char is not None:
                    read_in_file.append(line.strip().split(split_char))
                else:
                    read_in_file.append(line.strip())
            else:
                if split_char is not None:
                    read_in_file.append(line.split(split_char))
                else:
                    read_in_file.append(line)

    return read_in_file
