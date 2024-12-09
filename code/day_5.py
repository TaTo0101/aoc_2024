import numpy as np

# Initialize empty lists to store both rules and sequences
raw_data = []

# Open the text file and read it line by line
with open("data/day_5_data", "r") as file:
    for line in file:
        report_with_string_entries = line.strip()
        raw_data.append(report_with_string_entries)

# Seperate rules from reports
rules_raw = [e for e in raw_data if "|" in e]
seq_raw = [e for e in raw_data if not "|" in e and e != ""]

# Convert each rule into a list of integers
rules = [list(map(int, e.split("|"))) for e in rules_raw]  # converted to int

rules_dict = {}
for first, second in rules:
    # if key does not exist, create list value
    if second not in rules_dict:
        rules_dict[second] = []
    rules_dict[second].append(first)

# Now sequences
sequences = [list(map(int, seq.split(","))) for seq in seq_raw]

print(sequences[:2])
# Values for key are values that must preceede key in sequences
print(rules_dict[24])

## Task 5.1
# We iterate now through every sequence and every value 1,..k in it
# To verify that sequence follows the rules it suffices to check, for each value i<=k
# whether in the rules for this value there is any value which matches with any of the
# yet unchecked values i+1,...,k as if this is the case, the rule cannot be satisfied.
# Already checked values 1, ..., i-1 don't need to be checked again, as if they are in
# the values of the rules dict for the current value as key i, they already preceed it.
correct_sequences = []
incorrect_sequences = []
for seq in sequences:
    violates = False
    # to keep track which vals where already checked
    vals_checked = set(seq)  # set so easier to check
    for val in seq:
        vals_checked.remove(val)

        # If no elements would be left, all are correct
        if len(vals_checked) == 0:
            continue
        # Get preceeding values based on rules
        vals_to_preceed_val = set(rules_dict[val])
        # Check if any unchecked vals is contained
        violates = not vals_checked.isdisjoint(vals_to_preceed_val)

        if violates:
            # For task 5.2
            incorrect_sequences.append(seq)
            # Don't need to check remaining sequence elements
            break
    # If loop was terminated via break, sequence doesn't get added
    if not violates:
        correct_sequences.append(seq)

print(f"Number of correct sequences {len(correct_sequences)}")

middle_pages = [seq[int((len(seq) - 1) / 2)] for seq in correct_sequences]
print(f"Sum of all middle pages: {sum(middle_pages)}")


## Task 5.2
# We essentially repeat the approach, but now if a violation is detected, we
# use intersection to put the values before the current value, resulting in the
# correct order
corrected_sequences = []
for seq in sequences:
    violates = False

    # to keep track which vals where already checked
    vals_checked = set(seq)  # set so easier to check

    # placeholder for reordered sequence
    reordered_sequence = []
    for val in seq:
        # Add value to reordered sequence
        # If values should preceed, they will be added before this

        vals_checked.remove(val)

        # If no elements would be left, all are correct
        if len(vals_checked) == 0:
            continue
        # Get preceeding values based on rules
        vals_to_preceed_val = set(rules_dict[val])

        # If the value is correct, we can proceed to the next value
        violates = not vals_checked.isdisjoint(vals_to_preceed_val)

        if violates:
            # Get values which should preceed current one
            should_preceed = vals_checked.intersection(vals_to_preceed_val)

        # Manipulate sequence by first removing them and then inserting them

    # If loop was terminated via break, sequence doesn't get added
    if not violates:
        corrected_sequences.append(seq)
