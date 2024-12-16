import os
import sys

import numpy as np
from scipy.ndimage import shift

sys.path.append("src")

from utils import puzzle_input_reader

day_4_path = "data/day_4_data.txt"

puzzle_input = puzzle_input_reader(path=day_4_path)

input_data = np.array([list(line) for line in puzzle_input])

## Task 1.1
# The initial idea heavily leans on the concepts of convolutions and how they are used in signal
# processing of multi-dimensional input spaces. We first create and indicator like matrix, where
# X = 1, ..., S = 4, for every character entry. Then we construct kernel matrices, to detect for
# each entry whether it starts with X, is then followed by M, then by A, and finally S by leveraging
# the fact that given our mapping the sequence must be 1,2,3,4 and nothing else is allowed.

## Convert to indicator matrix
input_matrix = np.where(
    input_data == "X",
    1,
    np.where(
        input_data == "M",
        2,
        np.where(input_data == "A", 3, np.where(input_data == "S", 4, 0)),
    ),
)

print(input_matrix[0])
# We now write a function that performs aformentioned filtering by using kernel matrices of the
# same size as the input and just "move it" from right to left in 4 steps to construct the output
# matrix (i.e. the filtered "image"). NA values are filled with 0

channel_outputs = []
shift_pattern = np.array([-1, 0])  # right
for i in range(3):
    shift_adjust = shift_pattern * (i + 1)
    channel_outputs.append(shift(input_matrix, shift=shift_adjust, cval=0))

# sum up channel outputs in specifc way to enforce 0 creation where sequence 1,2,3,4 starts
factors = [5, 9, -37]
filtered_output = (
    input_matrix
    + factors[0] * channel_outputs[0]
    + factors[1] * channel_outputs[1]
    + factors[2] * channel_outputs[2]
)

# Technically counting the 0 would be enough but let us verify that it worked.
# We now want to grab the indices where in the filtered matrix the entry is 0 and all three
# entries to the right of this. Here we can again utilize shifting
start_indices = np.argwhere(filtered_output == 0)

# Create a mask for the input
rows, cols = start_indices[:, 0], start_indices[:, 1]
mask = np.zeros_like(input_data, dtype=bool)

# Update the mask for the indices and the next three columns
for row, col in zip(rows, cols):
    # mask[row, col : col + 4] = True  # Include the next three columns (if they exist)
    mask[row : row + 4, col] = True  # Include the next three columns (if they exist)
    # mask[row : row + 4, col : col + 4] = True  # Include the next three columns (if they exist)

# Apply the mask to the input
applied_filter = np.where(
    mask, input_data, ""
)  # Replace non-selected elements with NaN (or ignore them)

# When using the debugger one can view the tables to see that it works

# Now the only thing left is to cycle through all shifts for the XMAS code word, adjust the
# factor order and repeat this for all shifts again and at each step count the number of zeros

# For the diagonal ones, we also need bottom left to top right, the other direction are already
# captured by also searching for the mirrored word
shifts_to_check = [
    # left to right
    np.array([0, -1]),  # horizontal
    np.array([-1, 0]),  # vertical
    np.array([-1, -1]),  # diagonal top right, bottom left
    # right to left
    np.array([1, -1]),  # diagonal bottom right, top left
]
factors_to_check = [
    [5, 9, -38 / 4],  # XMAS = 1, 2, 3, 4
    [5, 9, -37],  # SAMX = 4, 3, 2, 1
]

xmas_count = 0
for factors in factors_to_check:
    for direction in shifts_to_check:
        channel_outputs = []  # For storing result of each shift
        for i in range(3):
            shift_adjust = direction * (i + 1)
            channel_outputs.append(shift(input_matrix, shift=shift_adjust, cval=0))

        # Calculate filtered image
        filtered_output = (
            input_matrix
            + factors[0] * channel_outputs[0]
            + factors[1] * channel_outputs[1]
            + factors[2] * channel_outputs[2]
        )

        # Count number of 0s
        zero_filter = filtered_output == 0
        xmas_count = xmas_count + filtered_output[zero_filter].shape[0]

print(f"Number of XMAS occurences in all directions: {xmas_count}")
