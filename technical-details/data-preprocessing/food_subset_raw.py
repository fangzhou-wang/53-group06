import pandas as pd
import os

# ========== 路径配置 ==========
input_path = "data/raw-data/en.openfoodfacts.org.products.csv.gz"
output_path = "data/processed-data/food_subset_raw.csv"

# ========== 要提取的字段 ==========
columns_to_keep = [
    "product_name", "main_category_en", "pnns_groups_1", "pnns_groups_2", "countries_en",
    "serving_size", "serving_quantity", "quantity", "product_quantity", "additives_n",
    "labels_en", "nutriscore_grade",
    # 营养成分相关
    "energy-kcal_100g", "fat_100g", "saturated-fat_100g", "sugars_100g",
    "fiber_100g", "proteins_100g", "salt_100g"
]

# ========== 解压并提取列 ==========
print("📦 正在解压和读取指定字段...")
df = pd.read_csv(input_path, sep="\t", usecols=lambda c: c in columns_to_keep, low_memory=False)

# ========== 保存 ==========
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)

print(f"✅ 已保存字段子集到：{output_path}")
print(f"🔢 共提取 {df.shape[0]} 行，{df.shape[1]} 列")
