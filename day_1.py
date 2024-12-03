import numpy as np

# Initialize two empty lists to store the values
list1 = []
list2 = []

# Open the text file and read it line by line
with open("task_1_1", "r") as file:
    for line in file:
        # Split the line by whitespace and extract the two numbers
        numbers = line.strip().split(
            "  "
        )  # Adjust the number of spaces here if needed
        if len(numbers) == 2:  # Ensure there are exactly two numbers in the line
            list1.append(int(numbers[0]))
            list2.append(int(numbers[1]))
list1.sort()
list2.sort()
# Sort each list, convert to np array
array1_sorted = np.array(list1)
array2_sorted = np.array(list2)


# Calculate difference and sum
val = np.abs(array1_sorted - array2_sorted).sum()
print(val)


# Count unique
left_unique = np.unique(array1_sorted)
right_unique, right_unique_counts = np.unique(array2_sorted, return_counts=True)

# Ignore all entries that are not in right
mask = np.isin(left_unique, right_unique)
rel_entries_left = left_unique[mask]
# get all from left that match
mask = np.isin(right_unique, rel_entries_left)
rel_entries_right = right_unique[mask]
rel_counts = right_unique_counts[mask]

# left only contains elements in right
# since both arrays are sorted they are in parallel


score = (rel_entries_left * rel_counts).sum()
print(score)
