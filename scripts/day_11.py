import numpy as np
from numpy import ndarray

from utils import puzzle_input_reader

# Load in the file
file_path = "data/day_11_data.txt"
input_data = puzzle_input_reader(path=file_path, split_char=" ")[0]

print(input_data)


def apply_rules(input_str: str, mult_fac: int = 2024) -> list:
    """Apply rule given by task description for a single engraved stone.

    Rules are:
    1. input_str == "0" -> set output to "1"
    2. len(input_str) % 2 == 0 -> split face value string in half and remove leading zeros in right
        one
    3. else -> multiply input with 2024

    Args:
        input_str (str): The face value of the stone as string
        mult_fac (int): Multiplicative factor to use for the else statement. Defaults to 2024.

    Returns:
        list: A list either containing the updated stone face value or the two new stones (and their
        face values with leading 0 removed).
    """
    if not isinstance(input_str, str):
        raise ValueError(
            f"Unsupported type for input_str, must be string but got {type(input_str)}"
        )

    num_digits = len(input_str)
    if input_str == "0":
        output = ["1"]
    elif (num_digits % 2) == 0:
        # Get halfway index
        halfpoint = int(num_digits / 2)
        left, right = input_str[:halfpoint], input_str[halfpoint:]
        # remove leading zeros if present
        right = str(int(right))
        output = [left, right]
    else:
        output = [str(2024 * int(input_str))]

    return output


# Define a function to split a single string into two halves
def split_half(s):
    half = len(s) // 2
    return s[:half], s[half:]


def apply_rules_vectorized(input_array: ndarray, mult_fac: int = 2024) -> ndarray:
    """Apply rule given by task description for an array of engraved stones.

    Rules are:
    1. input_str == "0" -> set output to "1"
    2. len(input_str) % 2 == 0 -> split face value string in half and remove leading zeros in right
        one
    3. else -> multiply input with 2024

    Args:
        input_array (ndarray): The face values of the stones as as an string array
        mult_fac (int): Multiplicative factor to use for the else statement. Defaults to 2024.

    Returns:
        ndarray: An array either containing the updated stone face values
    """
    # Get all 0 flips
    zero_cond = input_array == "0"
    number_of_flips = np.sum(zero_cond)
    flipped = np.ones(number_of_flips, dtype=np.int8)

    ## Perform the split for even digit lengths
    even_digit_condition = (np.strings.str_len(input_array) % 2) == 0
    to_split = input_array[even_digit_condition]
    # Vectorize the function so it applies to each element of the array
    split_ufunc = np.vectorize(split_half)

    # Apply the vectorized function to get left and right halves
    left, right = split_ufunc(to_split)

    # Remove leading zeros
    right = right.astype(int).astype(str)

    splitted_values = np.concatenate((left, right), axis=0)

    # Perform the multiplication but ignore zeros
    multiplied_vals = (
        input_array[(~even_digit_condition) & (~zero_cond)].astype(int) * mult_fac
    ).astype(str)

    # order doesn't matter so we can just concat
    output = np.concat((flipped, splitted_values, multiplied_vals), axis=0)

    return output


def count_even_digits(stone_line: list[str]) -> int:
    """Helper function that counts the number of digits with even lengths in a list of strings.

    Args:
        stone_line (list[str]): A list of strings, where each string represents a number.

    Returns:
        int: Number of digits with even length.
    """
    even_digits = [digit for digit in stone_line if (len(digit) % 2) == 0]
    return len(even_digits)


# Perform blinking algorithm
# at each step count number items in list

import timeit


def comprehension_method(val_list, steps=25):
    for i in range(num_steps):
        val_list = [result for stone in val_list for result in apply_rules(stone)]
    return val_list


def vectorized_method(val_array, steps=25):
    for i in range(num_steps):
        print(i)
        val_array = apply_rules_vectorized(val_array)
    return val_array


num_steps = 40
stone_list = input_data
stone_array = np.array(input_data)

# t1 = timeit.Timer(lambda: comprehension_method(stone_list, steps=num_steps))
# t2 = timeit.Timer(lambda: vectorized_method(stone_array, steps=num_steps))

# print("Comprehension: ", t1.timeit(10))
# print("Vectorized: ", t2.timeit(10))
# output_list = comprehension_method(stone_list)
output_array = vectorized_method(stone_array)

# print(f"Number of stones after {num_steps} steps: {len(output_list)}")
print(f"Number of stones after {num_steps} steps: {len(output_array)}")
