import pandas as pd
import os

input_path = "data/processed-data/food_subset_raw.csv"
output_path = "data/processed-data/food_sampled_raw.csv"

# Sampling Parameters
sample_frac = 0.1
min_samples_per_class = 30
random_seed = 42

print("Reading raw field data...")
df = pd.read_csv(input_path, low_memory=False)

# Sampling
df = df[df['pnns_groups_1'].notna()]

df_sampled = df.groupby('pnns_groups_1', group_keys=False).apply(
    lambda x: x.sample(frac=sample_frac, random_state=random_seed) if len(x) > min_samples_per_class else x
).reset_index(drop=True)

os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_sampled.to_csv(output_path, index=False)

print(f"Sampling completed: {df_sampled.shape[0]} records")
print(f"The sampling results are saved to: {output_path}")
