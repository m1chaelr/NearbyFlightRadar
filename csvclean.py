# Script to clean a CSV file by removing rows with empty 'typecode' values
import pandas as pd

# Load the data from the Excel file
df = pd.read_csv("aircraftDataset.csv", on_bad_lines='skip', low_memory=False)

# Create a boolean mask to identify rows where 'typecode' is NOT = ''
rows_to_keep = df["'typecode'"] != "''"

# Filter the DataFrame to keep only the rows that satisfy the condition
df_modified = df[rows_to_keep]

# Save the new DataFrame to a new Excel file without the index column
df_modified.to_csv("aircraftDetailDataset.csv", index=False)

# Debug - keep track of how much was changed
print(f"Original number of rows: {len(df)}")
print(f"Number of rows after dropping: {len(df_modified)}")
print(f"Number of rows dropped: {len(df) - len(df_modified)}")