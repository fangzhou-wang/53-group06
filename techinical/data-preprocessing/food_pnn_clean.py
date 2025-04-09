import pandas as pd
import os

# ==== 路径配置 ====
input_path = "data/processed-data/food_sampled_by_pnns.csv"
output_path = "data/processed-data/food_clean_final.csv"

# ==== 读取数据 ====
df = pd.read_csv(input_path)

# ==== 统一小写、去空格 ====
df['nutriscore_grade'] = df['nutriscore_grade'].astype(str).str.strip().str.lower()
df['pnns_groups_1'] = df['pnns_groups_1'].astype(str).str.strip().str.lower()

# ==== 保留合法评级 a–e ====
valid_grades = ['a', 'b', 'c', 'd', 'e']
df = df[df['nutriscore_grade'].isin(valid_grades)]

# ==== 删除类别为 unknown 的行 ====
df = df[df['pnns_groups_1'] != 'unknown']

# ==== 重置索引 & 保存 ====
df = df.reset_index(drop=True)
df.to_csv(output_path, index=False)

print(f"✅ 清洗完成！共保留 {df.shape[0]} 条记录")
print(f"📄 已保存至：{output_path}")
