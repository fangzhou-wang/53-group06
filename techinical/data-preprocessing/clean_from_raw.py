import pandas as pd
import os

# ========= 路径配置（根据你自己的实际路径修改） =========
gz_path = "C:/Users/Administrator/Desktop/5300/data/raw-data/en.openfoodfacts.org.products.csv.gz"
output_path = "C:/Users/Administrator/Desktop/5300/data/processed-data/food_sampled_by_pnns.csv"

# ========= 参数配置 =========
sample_frac = 0.2
min_samples_per_class = 30
random_seed = 42
chunksize = 10000

# ========= 要提取的字段 =========
selected_columns = [
    'product_name', 'quantity', 'product_quantity',
    'pnns_groups_1', 'pnns_groups_2', 'main_category_en',
    'labels_en', 'countries_en', 'serving_size', 'serving_quantity',
    'energy-kcal_100g', 'fat_100g', 'saturated-fat_100g',
    'carbohydrates_100g', 'sugars_100g', 'added-sugars_100g',
    'fiber_100g', 'proteins_100g', 'salt_100g', 'sodium_100g',
    'cholesterol_100g', 'vitamin-c_100g',
    'fruits-vegetables-nuts-estimate_100g',
    'additives_n', 'nova_group', 'nutriscore_grade'
]

# ========= 创建目录（若不存在） =========
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# ========= 分块读取 + 清洗 + 合并 =========
print("⏳ 正在读取并筛选数据...")
chunks = []
for chunk in pd.read_csv(gz_path, sep='\t', usecols=lambda x: x in selected_columns,
                         chunksize=chunksize, low_memory=False):
    chunk['nutriscore_grade'] = chunk['nutriscore_grade'].astype(str).str.strip().str.lower()
    filtered = chunk[
        chunk['nutriscore_grade'].isin(['a', 'b', 'c', 'd', 'e']) &
        chunk['pnns_groups_1'].notna()
    ]
    chunks.append(filtered)

df_all = pd.concat(chunks, ignore_index=True)

# ========= 按分类抽样 20% =========
print("🔍 正在按分类抽样 20%...")
df_sampled = df_all.groupby('pnns_groups_1', group_keys=False).apply(
    lambda x: x.sample(frac=sample_frac, random_state=random_seed) if len(x) > min_samples_per_class else x
).reset_index(drop=True)

# ========= 保存输出 =========
df_sampled.to_csv(output_path, index=False)
print(f"✅ 抽样完成，共 {df_sampled.shape[0]} 条记录")
print(f"📄 文件保存至：{output_path}")
