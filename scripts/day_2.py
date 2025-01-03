import numpy as np
import pandas as pd

# Initialize two empty lists to store the values
list_of_reports = []

# Open the text file and read it line by line
with open("data/day_2_data", "r") as file:
    for line in file:
        report_with_strin_entries = line.strip().split(" ")
        list_of_reports.append(np.array(report_with_strin_entries).astype(int))

print(list_of_reports)

## Task 1
# diff approach
list_of_diffs = [np.diff(report) for report in list_of_reports]

# get all monotone increasing or decreasing reports
list_of_monotone_seq = [
    diff for diff in list_of_diffs if all(diff < 0) | all(diff > 0)
]

# keep only those were not more than 3 apart
list_of_safe_diffs = [diff for diff in list_of_monotone_seq if np.abs(diff).max() <= 3]
print(f"Number of save reports: {len(list_of_safe_diffs):2d}")

## Task 2
# Each unsafe report now gets a second change, thus need only to look at all reports
# which only failed in one aspect
list_of_non_monotone_seq = [diff for diff in list_of_diffs if np.abs(diff).max() <= 3]
# How many could be made safe when removing one level?
list_of_savable_nm_seq = [
    diff
    for diff in list_of_non_monotone_seq
    if ((diff == 0).sum() <= 1) & ((all(diff <= 0)) | (all(diff >= 0)))
]

# Same for max diff
list_of_savable_diffs = [
    diff for diff in list_of_diffs if all(diff < 0) | all(diff > 0)
]
list_of_savable_diffs = [
    diff for diff in list_of_savable_diffs if np.sort(np.abs(diff))[-2] <= 3
]

# Let us just get the number of reports that have more than one flaw and substract
diffs_of_more_than_one = [
    diff
    for diff in list_of_diffs
    if ((diff == 0).sum() <= 1)
    & ((all(diff <= 0)) | (all(diff >= 0)))
    & (np.sort(np.abs(diff))[-2] <= 3)
]

result = len(list_of_diffs) - len(diffs_of_more_than_one)
# We just sort, then get second largest element
list_of_safe_diffs = [
    diff for diff in list_of_monotone_seq if np.sort(np.abs(diff))[-2] <= 3
]

# Let us first store all in a pandas, so we keep track
df = pd.DataFrame({"diffs": list_of_diffs})
df["monotone"] = np.where(
    (df["diffs"].apply(lambda x: x < 0)).apply(all)
    | (df["diffs"].apply(lambda x: x > 0)).apply(all),
    1,
    0,
)
df["level_thresh"] = np.where(
    df["diffs"]
    .abs()
    .reset_index(drop=True)
    .apply(np.sort)
    .apply(lambda x: x[-1] <= 3),
    1,
    0,
)

# Now any that have only on indicator to true but not both get a second chance
filter = df["monotone"] == 1
df.loc[filter, "add_level_thresh"] = np.where(
    df.loc[filter, "diffs"]
    .abs()
    .reset_index(drop=True)
    .apply(np.sort)
    .apply(lambda x: x[-2] <= 3),
    1,
    0,
)
df.loc[df["add_level_thresh"].isnull(), "add_level_thresh"] = 0
filter = df["level_thresh"] == 1
df["diffs_sign"] = df["diffs"].apply(lambda x: np.sign(x))
df["number_sign_changes"] = (
    df["diffs_sign"].apply(lambda x: sum((np.roll(x, 1) - x) != 0)).astype(int)
)
df["remove_zero"] = np.where(
    (df["diffs"].apply(lambda x: x <= 0)).apply(all)
    | (df["diffs"].apply(lambda x: x >= 0)).apply(all)
    & ((df["diffs"].apply(lambda x: x == 0)).apply(sum) <= 1),
    1,
    0,
)

df["remove_change_point"] = np.where(
    (df["number_sign_changes"] <= 1)
    & ((df["diffs"].apply(lambda x: x == 0)).apply(sum) == 0),
    1,
    0,
)

df["save"] = np.where((df["monotone"] == 1) & (df["level_thresh"] == 1), 1, 0)
filter = ((df["remove_change_point"] == 1) ^ (df["remove_zero"] == 1)) | (
    df["add_level_thresh"] == 1
)
df["additional_save"] = np.where(filter, 1, 0)

print(f"Number of save reports with tolerance: {len(list_of_safe_diffs):2d}")
