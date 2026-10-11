# 1.导入库
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['SimHei']  # Windows显示中文

# 2.导入数据
df = pd.read_csv("data/raw/dataproducts.csv", encoding="utf-8-sig")

# 3.数据概览
print('总记录数：', len(df))
print('字段数量：', len(df.columns))
print(df.head(5))
print(df.info())

#4.数据清洗
#删除无用的数据列
df.drop(columns='url', inplace=True)

#检查是否有缺失值
df.isna().sum()


#删除缺失值
df.dropna(inplace=True)
print('删除缺失值后记录数：', len(df))

#检查是否有重复值
df.duplicated().sum()


#删除重复值
df.drop_duplicates(inplace=True)
print('删除重复值后记录数：', len(df))

#数据转换
df['price'] = df['price'].str.replace('£', '').astype(float)
print(df.head(5))




# 定义保存路径（保存在当前目录下的 data/cleaned 文件夹中）
save_path = './data/cleaned/dataproducts_cleaned.csv'

# 自动创建文件夹（如果不存在的话），避免报错
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# 保存为CSV文件，index=False表示不保存行索引
df.to_csv(save_path, index=False, encoding='utf-8-sig')

print(f"✅ 清洗完成！干净的数据已保存至: {save_path}")