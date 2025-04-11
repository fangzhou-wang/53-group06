import pandas as pd
import os

input_path = "data/processed-data/food_sampled_raw.csv"
output_path = "data/raw-data/food_sampled_cleaned.csv"

print("Cleaning sampling data...")
df = pd.read_csv(input_path)

# Standardization
df['nutriscore_grade'] = df['nutriscore_grade'].astype(str).str.strip().str.lower()
df['pnns_groups_1'] = df['pnns_groups_1'].astype(str).str.strip().str.lower()

# Remove unknown categories
df = df[df['nutriscore_grade'].isin(['a', 'b', 'c', 'd', 'e'])]
df = df[df['pnns_groups_1'].notna() & (df['pnns_groups_1'] != 'unknown')]

df.to_csv(output_path, index=False)
print(f"Cleaning completed, remaining records: {df.shape[0]}")
print(f"The cleaning results are saved to: {output_path}")
